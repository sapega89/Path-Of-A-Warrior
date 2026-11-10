class_name Motion
extends RefCounted
## Which clip of the shared library (assets/art/characters/humanoid_clips.glb) a person on the
## map plays for the action MapSim gives him, and how: [clip, mode, speed].
##   "loop": repeats at `speed` (walking and running are matched to the ground speed),
##   "fit":  plays once over the action's ticks (but not quicker than MIN_FIT seconds),
##   "once": plays once at `speed` and keeps its last pose (a hit, a fall).
## The simulation stays in charge: the clip only shows what the action does.

## A strike shorter than this is stretched to it, so the swing reads.
const MIN_FIT := 0.42
## Ground speed (m/s) at which the walk and run clips play at speed 1.
const WALK_SPEED := 1.9
const RUN_SPEED := 4.2

## The hero's skills 12..30: [clip, mode, speed].
const SKILLS := {
	12: ["attack_spin", "fit", 1.0],  # Whirlwind Sabre: a dash and a whirl
	13: ["attack_2h_slash", "fit", 1.0],  # Storm Sabre: smash through
	14: ["attack_stab", "loop", 2.6],  # Thunder Sabre: a series of thrusts
	15: ["cast_raise", "fit", 1.0],  # Healing Herbs
	16: ["cast_raise", "fit", 1.0],  # Living Water
	17: ["cheer", "fit", 1.0],  # Fury
	18: ["cast_raise", "fit", 1.0],  # Charm
	19: ["cast_raise", "fit", 1.0],  # Protection of the Virgin
	20: ["attack_sweep", "loop", 2.2],  # Dnipro Wave: blow after blow
	21: ["attack_2h_slash", "fit", 1.0],  # Rapids: knocks back
	22: ["attack_2h_stab", "fit", 1.0],  # Flood: straight ahead
	23: ["attack_spin", "fit", 1.0],  # Ring of Fire
	24: ["attack_spin", "fit", 1.0],  # Fire Whirl
	25: ["attack_spin", "loop", 1.6],  # Steppe Blaze
	26: ["cast", "fit", 1.0],  # Lightning
	27: ["cast", "fit", 1.0],  # Perun's Arrow
	28: ["cast_raise", "fit", 1.0],  # Thunderstorm
	29: ["cast_raise", "fit", 1.0],  # Serpent's Breath
	30: ["cast_raise", "fit", 1.0],  # Rain of Fire
}
## The three blows of the combo with a short weapon (actions 3..5): quick cuts.
const COMBO := ["attack_slash", "attack_sweep", "attack_chop"]
## And with a long one (actions 6..8, slower): a thrust, a cut from above with both hands, a
## sweeping thrust.
const LONG_COMBO := ["attack_stab", "attack_2h_slash", "attack_2h_stab"]
## MapActor.weapon_kind of a long weapon (its reach 63 px, the short one's 53).
const LONG_WEAPON := 0
## A general's actions 6..21 are the hero's skills.
const GENERAL_SKILL := [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]


## The hero's clip for his action; ground_speed: m/s he moves now, weapon_kind: his
## MapActor.weapon_kind (a long weapon he holds ready in both hands).
static func hero(action: int, ground_speed: float = 0.0, weapon_kind := 1) -> Array:
	match action:
		0:
			return [idle(weapon_kind), "loop", 1.0]
		1:
			return ["walk", "loop", _pace(ground_speed, WALK_SPEED)]
		2:
			return ["run", "loop", _pace(ground_speed, RUN_SPEED)]
		9:
			return ["hit", "once", 1.0]
		10:
			return ["death", "once", 0.8]
		11:
			return ["use_item", "fit", 1.0]
	if action >= 3 and action <= 5:
		return [COMBO[action - 3], "fit", 1.0]
	if action >= 6 and action <= 8:
		return [LONG_COMBO[action - 6], "fit", 1.0]
	return SKILLS.get(action, ["idle", "loop", 1.0])


## How one stands with a weapon of this kind: a long one ready in both hands.
static func idle(weapon_kind: int) -> String:
	return "idle_2h" if weapon_kind == LONG_WEAPON else "idle"


## A soldier's (201 swords, 202 archers, 203 a squad) or a general's (type < 200) clip.
## Soldiers' actions: 0 walk, 1 attack, 2 hurt, 3 dying; generals also 4, 5 strikes and
## 6..21 skills.
static func enemy(type: int, action: int, ground_speed: float = 0.0, knocked := false) -> Array:
	match action:
		0:
			if ground_speed < 0.2:
				return ["idle", "loop", 1.0]
			return ["walk", "loop", _pace(ground_speed, WALK_SPEED)]
		1:
			if type == MapSim.KIND_ARCHERS:
				return ["shoot_bow", "fit", 1.0]
			return ["attack_slash", "fit", 1.0]
		2:
			return ["hit_heavy" if knocked else "hit", "once", 1.0]
		3:
			return ["death", "once", 0.8]
		4:
			return ["attack_sweep", "fit", 1.0]
		5:
			return ["attack_chop", "fit", 1.0]
	if type < 200 and action >= 6 and action <= 21:
		return hero(GENERAL_SKILL[action - 6])
	return ["idle", "loop", 1.0]


## How long an action lasts in ticks: its frame list up to the end mark.
static func ticks(anim: Array) -> int:
	var n := 0
	for f in anim:
		if int(f) > MapSim.END:
			break
		n += 1
	return maxi(n, 1)


static func _pace(ground_speed: float, nominal: float) -> float:
	return clampf(ground_speed / nominal, 0.6, 2.2) if ground_speed > 0.05 else 1.0


## The original 8-direction (0 down, 2 left, 4 up, 6 right) as a turn about Y: the figure
## faces +Z at 0.
static func yaw_of(dir8: int) -> float:
	return [0.0, -PI / 4.0, -PI / 2.0, -3.0 * PI / 4.0, PI, 3.0 * PI / 4.0, PI / 2.0, PI / 4.0][posmod(
		dir8, 8
	)]
