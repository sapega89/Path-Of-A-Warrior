class_name HeroRun
extends RefCounted
## The run: from the start camp to an ending that leads back there, or to a mission lost with
## no flask of living water left. What the hero learns in a run (his skills) lives one run; his
## level, gear, gold and fame stay. The flasks are bought with fame in the start camp's town
## hall, once and for good, and are full again at every new run: a mission lost empties one,
## and the hero tries again from the same camp. An ending that goes on to a main camp fills one.

const MAX_FLASKS := 3
## The fame the first, second and third flask cost.
const FLASK_PRICES := [200, 1000, 3000]
## The skills a run starts with (their places in Profile.skill_levels): Whirlwind Sabre on key 1
## and Fury on key 2.
const START_SKILLS := [0, 5]
const START_HOTKEYS := [12, 17, 0, 0, 0]

var flasks := 0  # bought, 0..MAX_FLASKS
var flasks_left := 0  # still full in this run


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
	return {"flasks": flasks, "flasks_left": flasks_left}


func from_dict(d: Dictionary) -> void:
	flasks = clampi(int(d.get("flasks", 0)), 0, MAX_FLASKS)
	flasks_left = clampi(int(d.get("flasks_left", flasks)), 0, flasks)
