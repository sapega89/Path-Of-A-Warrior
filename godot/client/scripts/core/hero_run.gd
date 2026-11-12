class_name HeroRun
extends RefCounted
## The run: from the start camp to an ending that leads back there, or to a mission lost with
## no flask of living water left. What the hero learns in a run (his skills) lives one run; his
## level, gear, gold and fame stay. A run starts with the starting skill chosen in the start
## camp (one of the first skills of the rows; two with the perk). The flasks are bought with
## fame in the start camp, once and for good, and are full again at every new run: a mission
## lost empties one, and the hero tries again from the same camp. An ending that goes on to a
## main camp fills one. A run may start only with a skill the hero has learnt in a run before
## (known_skills). A mission won leaves the gift of its general (Gifts) here until the hero
## takes a card. Fame also buys the perks, once and for good. The vows (Vows) are kept here too.

const MAX_FLASKS := 3
## The fame the first, second and third flask cost.
const FLASK_PRICES := [200, 1000, 3000]
## The skills a run may start with (places in Profile.skill_levels), the first of each row:
## Whirlwind Sabre, Healing Herbs, Fury, Dnipro Wave, Ring of Fire, Lightning.
const START_CHOICES := [0, 3, 5, 8, 11, 14]
const FIRST_SKILL_ID := 12  # the id of the skill in place 0 (the hotkeys hold ids)
const HOTKEYS := 5
## What else fame buys, once and for good: a 4th gift card, one reroll of a gift each run, a
## second starting skill.
const PERK_PRICES := {"card": 1500, "reroll": 800, "second_skill": 2000}

var flasks := 0  # bought, 0..MAX_FLASKS
var flasks_left := 0  # still full in this run
var start_skills: Array[int] = [0]  # places in Profile.skill_levels, one of START_CHOICES each
var known_skills: Array[int] = []  # the START_CHOICES the hero has learnt in a run so far
var perks := {}  # PERK_PRICES name -> true, once bought
var reroll_used := false  # the reroll of this run is spent
var gift: Array[Dictionary] = []  # the cards of the last mission won, until one is taken
var gift_from := 0  # the general who offers them (0: none)
var vows := Vows.new()  # taken in the start camp, for the runs until changed


## The hero is in the start camp, where the run begins (and where nothing of it is learnt yet).
static func at_start(profile: Profile) -> bool:
	return profile.place == 0


## What a mission lost costs: the gear it may take (Profile.lose_gear, rolled with rng), and a
## flask, or the run when none is left. A mission whose loss ends the story (story_ends) costs
## no flask: the ending comes. Returns {gear: the thing lost or {}, over: the run is over}.
func lose_mission(profile: Profile, story_ends: bool, rng: JavaRandom) -> Dictionary:
	var lost: Dictionary = profile.lose_gear(rng)
	var over := false
	if not story_ends:
		if flasks_left > 0 and not vows.has("no_flasks"):
			flasks_left -= 1
		else:
			over = true
			profile.done = {}  # the missions of this run can be won again
			end(profile)
	return {"gear": lost, "over": over}


## The run is over: the skills go back to the starting ones, the colonels' progress is lost, the
## hero is at the start, every flask he bought is full again and the reroll is back.
func end(profile: Profile) -> void:
	note_skills(profile)
	reset_skills(profile)
	profile.progress = {}
	profile.place = 0
	profile.heading = 0
	flasks_left = flasks
	reroll_used = false


## The skills of a new run: the starting ones at level 1 on the first keys, nothing else.
func reset_skills(profile: Profile) -> void:
	for i in profile.skill_levels.size():
		profile.skill_levels[i] = 1 if i in start_skills else 0
	profile.hotkeys = []
	for k in HOTKEYS:
		profile.hotkeys.append(FIRST_SKILL_ID + start_skills[k] if k < start_skills.size() else 0)


## Remembers the starting skills (START_CHOICES) the hero has now: later runs may start with
## them.
func note_skills(profile: Profile) -> void:
	for place: int in START_CHOICES:
		if int(profile.skill_levels[place]) > 0 and not place in known_skills:
			known_skills.append(place)


## The skills a run may start with: those of START_CHOICES the hero has learnt in a run before,
## or has now (a new hero: Whirlwind Sabre and Fury, his first run's).
func start_choices(profile: Profile) -> Array[int]:
	var out: Array[int] = []
	for place: int in START_CHOICES:
		if place in known_skills or int(profile.skill_levels[place]) > 0:
			out.append(place)
	return out


## Picks a starting skill (a place of start_choices): it replaces the one chosen, or with the
## second skill bought is added to it (the older one goes when there are two; pressing one of
## the two drops it while the other stays). The hero is at the start, so his skills are those of
## a new run at once. False for a skill that is not one of the choices.
func choose_start_skill(profile: Profile, place: int) -> bool:
	if not place in start_choices(profile):
		return false
	note_skills(profile)  # what he has now stays a choice after the reset
	if not has_perk("second_skill"):
		start_skills = [place]
	elif place in start_skills:
		if start_skills.size() > 1:
			start_skills.erase(place)
	else:
		start_skills.append(place)
		if start_skills.size() > 2:
			start_skills.remove_at(0)
	reset_skills(profile)
	return true


## An ending that takes the hero on to a main camp fills one flask.
func fill_one() -> void:
	flasks_left = mini(flasks_left + 1, flasks)


## A mission won: its general (campaign.json generals; 0 or an ending: none) offers his cards.
func offer_gift(profile: Profile, general_id: int, rng: RandomNumberGenerator) -> void:
	gift_from = general_id
	gift = Gifts.offer(profile, general_id, gift_cards(), rng)


## How many cards a gift has: three, four with the perk.
func gift_cards() -> int:
	return Gifts.CARDS + (1 if has_perk("card") else 0)


## The hero takes card i of the gift; the others are gone. False when there was no such card or
## no room for it any more.
func take_gift(profile: Profile, i: int, rng: RandomNumberGenerator) -> bool:
	if i < 0 or i >= gift.size():
		return false
	var card: Dictionary = gift[i]
	gift = []
	return Gifts.take(profile, card, rng)


## The gift's cards may be rolled again: the perk is bought and not used in this run.
func can_reroll() -> bool:
	return has_perk("reroll") and not reroll_used and not gift.is_empty()


## Rolls the gift's cards again, once a run. False when it may not.
func reroll_gift(profile: Profile, rng: RandomNumberGenerator) -> bool:
	if not can_reroll():
		return false
	reroll_used = true
	gift = Gifts.offer(profile, gift_from, gift_cards(), rng)
	return true


## What the next flask costs in fame (0: all are bought).
func flask_price() -> int:
	return int(FLASK_PRICES[flasks]) if flasks < MAX_FLASKS else 0


## Buys the next flask with fame; it is full at once. False when all are bought or the fame
## is not enough.
func buy_flask(profile: Profile) -> bool:
	var price := flask_price()
	if flasks >= MAX_FLASKS or profile.fame < price:
		return false
	profile.fame -= price
	flasks += 1
	flasks_left += 1
	return true


func has_perk(perk: String) -> bool:
	return perks.has(perk)


## Buys a perk with fame. False when it is bought already, unknown, or the fame is not enough.
func buy_perk(profile: Profile, perk: String) -> bool:
	if has_perk(perk) or not PERK_PRICES.has(perk) or profile.fame < int(PERK_PRICES[perk]):
		return false
	profile.fame -= int(PERK_PRICES[perk])
	perks[perk] = true
	return true


func to_dict() -> Dictionary:
	return {
		"flasks": flasks,
		"flasks_left": flasks_left,
		"start_skills": start_skills,
		"known_skills": known_skills,
		"perks": perks.keys(),
		"reroll_used": reroll_used,
		"gift": gift,
		"gift_from": gift_from,
		"vows": vows.to_dict()
	}


func from_dict(d: Dictionary) -> void:
	flasks = clampi(int(d.get("flasks", 0)), 0, MAX_FLASKS)
	flasks_left = clampi(int(d.get("flasks_left", flasks)), 0, flasks)
	start_skills = []
	for s: Variant in _array(d.get("start_skills", [])):
		if int(s) in START_CHOICES and not int(s) in start_skills and start_skills.size() < 2:
			start_skills.append(int(s))
	if start_skills.is_empty():
		start_skills = [int(START_CHOICES[0])]
	known_skills = []
	for s: Variant in _array(d.get("known_skills", [])):
		if int(s) in START_CHOICES and not int(s) in known_skills:
			known_skills.append(int(s))
	perks = {}
	for p: Variant in _array(d.get("perks", [])):
		if PERK_PRICES.has(str(p)):
			perks[str(p)] = true
	reroll_used = bool(d.get("reroll_used", false))
	gift = []
	for c: Variant in _array(d.get("gift", [])):
		if typeof(c) == TYPE_DICTIONARY:
			gift.append({"kind": int(c.get("kind", -1)), "id": int(c.get("id", 0))})
	gift_from = int(d.get("gift_from", 0))
	var v: Variant = d.get("vows", {})
	vows.from_dict(v if typeof(v) == TYPE_DICTIONARY else {})


static func _array(v: Variant) -> Array:
	return v if typeof(v) == TYPE_ARRAY else []
