class_name HeroRun
extends RefCounted
## The run: from the start camp to an ending that leads back there, or to a mission lost with
## no flask of living water left. What the hero learns in a run (his skills) lives one run; his
## level, gear, gold and fame stay. The flasks are bought with fame in the start camp's town
## hall, once and for good, and are full again at every new run: a mission lost empties one,
## and the hero tries again from the same camp. An ending that goes on to a main camp fills one.
## A mission won leaves the gift of its general (Gifts) here until the hero takes a card.

const MAX_FLASKS := 3
## The fame the first, second and third flask cost.
const FLASK_PRICES := [200, 1000, 3000]
## The skills a run starts with (their places in Profile.skill_levels): Whirlwind Sabre on key 1
## and Fury on key 2.
const START_SKILLS := [0, 5]
const START_HOTKEYS := [12, 17, 0, 0, 0]

var flasks := 0  # bought, 0..MAX_FLASKS
var flasks_left := 0  # still full in this run
var gift: Array[Dictionary] = []  # the cards of the last mission won, until one is taken
var gift_from := 0  # the general who offers them (0: none)


## What a mission lost costs: the gear it may take (Profile.lose_gear, rolled with rng), and a
## flask, or the run when none is left. A mission whose loss ends the story (story_ends) costs
## no flask: the ending comes. Returns {gear: the thing lost or {}, over: the run is over}.
func lose_mission(profile: Profile, story_ends: bool, rng: JavaRandom) -> Dictionary:
	var lost: Dictionary = profile.lose_gear(rng)
	var over := false
	if not story_ends:
		if flasks_left > 0:
			flasks_left -= 1
		else:
			over = true
			profile.done = {}  # the missions of this run can be won again
			end(profile)
	return {"gear": lost, "over": over}


## The run is over: the skills go back to the first ones, the colonels' progress is lost, the
## hero is at the start and every flask he bought is full again.
func end(profile: Profile) -> void:
	for i in profile.skill_levels.size():
		profile.skill_levels[i] = 1 if i in START_SKILLS else 0
	profile.hotkeys = START_HOTKEYS.duplicate()
	profile.progress = {}
	profile.place = 0
	profile.heading = 0
	flasks_left = flasks


## An ending that takes the hero on to a main camp fills one flask.
func fill_one() -> void:
	flasks_left = mini(flasks_left + 1, flasks)


## A mission won: its general (campaign.json generals; 0 or an ending: none) offers his cards.
func offer_gift(profile: Profile, general_id: int, rng: RandomNumberGenerator) -> void:
	gift_from = general_id
	gift = Gifts.offer(profile, general_id, rng)


## The hero takes card i of the gift; the others are gone. False when there was no such card or
## no room for it any more.
func take_gift(profile: Profile, i: int, rng: RandomNumberGenerator) -> bool:
	if i < 0 or i >= gift.size():
		return false
	var card: Dictionary = gift[i]
	gift = []
	return Gifts.take(profile, card, rng)


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


func to_dict() -> Dictionary:
	return {"flasks": flasks, "flasks_left": flasks_left, "gift": gift, "gift_from": gift_from}


func from_dict(d: Dictionary) -> void:
	flasks = clampi(int(d.get("flasks", 0)), 0, MAX_FLASKS)
	flasks_left = clampi(int(d.get("flasks_left", flasks)), 0, flasks)
	gift = []
	var cards: Variant = d.get("gift", [])
	if typeof(cards) == TYPE_ARRAY:
		for c: Variant in cards:
			if typeof(c) == TYPE_DICTIONARY:
				gift.append({"kind": int(c.get("kind", -1)), "id": int(c.get("id", 0))})
	gift_from = int(d.get("gift_from", 0))
