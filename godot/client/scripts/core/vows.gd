class_name Vows
extends RefCounted
## The vows a hero may take before a run, once an ending has led him back to the start camp:
## tougher enemies (+20% HP a step, three steps at most), a time limit a quarter shorter, no
## potions from the shop, no flasks of living water. Each vow (each step of the enemies' HP)
## adds 10% to the gold and the fame of the run. They hold until changed, in the start camp only.

const HP_STEP := 20  # percent of HP the enemies get a step
const MAX_HP_STEPS := 3
const TIME_LEFT := 75  # percent of the time limit left with the short time
const BONUS_STEP := 10  # percent of gold and fame each vow adds
## The vows besides the enemies' HP, by name.
const SWITCHES := ["short_time", "no_shop_potions", "no_flasks"]

var hp_steps := 0
var taken := {}  # SWITCHES name -> true


## The vows open once the hero has reached an ending that leads back to the start.
static func open(profile: Profile) -> bool:
	for e in Profile.NEXT_PLACE.size():
		if profile.endings & (1 << e) and int(Profile.NEXT_PLACE[e]) == 0:
			return true
	return false


func has(vow: String) -> bool:
	return taken.has(vow)


## The enemies' HP one step up, and from the last step back to none.
func next_hp_step() -> void:
	hp_steps = (hp_steps + 1) % (MAX_HP_STEPS + 1)


## Takes a vow of SWITCHES, or gives it up. False for one that is not.
func switch(vow: String) -> bool:
	if not vow in SWITCHES:
		return false
	if taken.has(vow):
		taken.erase(vow)
	else:
		taken[vow] = true
	return true


## How many vows are taken (each step of the enemies' HP counts).
func count() -> int:
	return hp_steps + taken.size()


## The gold and the fame of the run, in percent.
func bonus_percent() -> int:
	return 100 + BONUS_STEP * count()


## The enemies' HP, in percent.
func enemy_hp_percent() -> int:
	return 100 + HP_STEP * hp_steps


## A mission's time limit under the vows.
func time_limit(limit: int) -> int:
	return limit * TIME_LEFT / 100 if has("short_time") else limit


func to_dict() -> Dictionary:
	return {"hp_steps": hp_steps, "taken": taken.keys()}


func from_dict(d: Dictionary) -> void:
	hp_steps = clampi(int(d.get("hp_steps", 0)), 0, MAX_HP_STEPS)
	taken = {}
	var names: Variant = d.get("taken", [])
	if typeof(names) == TYPE_ARRAY:
		for v: Variant in names:
			if str(v) in SWITCHES:
				taken[str(v)] = true
