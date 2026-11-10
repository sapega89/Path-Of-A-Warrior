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
## How far the body goes in a skill's move (body_pose()): metres up, radians of turn.
const LUNGE_LEAN := 0.22
const LEAP_HEIGHT := 0.9
const LEAP_LEAN := 0.3
const STOMP_HEIGHT := 0.35
const STOMP_LEAN := 0.12
const RISE_HEIGHT := 0.45
const TREMBLE_TURN := 0.06
const TREMBLE_LEAN := 0.05

## The hero's skills 12..30: [clip, mode, speed, body], each its own move: the clip, and how
## the whole body goes with it (body_pose()): "lunge" leans into the blow, "leap" jumps and
## comes down with it, "stomp" hops and lands hard, "spin" turns round once more, "rise" is
## lifted off the ground, "tremble" shakes, "" stands.
const SKILLS := {
	12: ["attack_spin", "fit", 1.0, "lunge"],  # Whirlwind Sabre: a dash and a whirl
	13: ["attack_2h_slash", "fit", 1.0, "leap"],  # Storm Sabre: a leap and a smash
	14: ["attack_stab", "loop", 2.6, "lunge"],  # Thunder Sabre: a series of thrusts
	15: ["pick_up", "fit", 1.0, ""],  # Healing Herbs: gathers herbs
	16: ["interact", "fit", 1.0, ""],  # Living Water: pours it out
	17: ["cheer", "fit", 1.0, "tremble"],  # Fury: a war cry, shaking with rage
	18: ["cast", "fit", 1.0, "rise"],  # Charm: a guarding spell lifts him
	19: ["block", "fit", 1.0, ""],  # Protection of the Virgin: on guard under the veil
	20: ["attack_sweep", "loop", 2.2, "lunge"],  # Dnipro Wave: blow after blow
	21: ["attack_chop", "fit", 1.0, "stomp"],  # Rapids: a chop into the ground
	22: ["attack_2h_stab", "fit", 1.0, "lunge"],  # Flood: straight ahead
	23: ["attack_spin", "fit", 1.0, "stomp"],  # Ring of Fire: a whirl and a stamp
	24: ["attack_spin", "fit", 1.0, "spin"],  # Fire Whirl: whirls twice
	25: ["attack_spin", "loop", 1.6, ""],  # Steppe Blaze: whirl after whirl
	26: ["cast", "fit", 1.0, ""],  # Lightning
	27: ["throw", "fit", 1.0, ""],  # Perun's Arrow: hurls it
	28: ["cast_raise", "fit", 1.0, "rise"],  # Thunderstorm: lifted to the clouds
	29: ["cast_raise", "fit", 1.0, "spin"],  # Serpent's Breath: turns with the serpent
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


## How the whole body goes with a skill's move (SKILLS) at x, 0..1 of the action: Vector3(lift
## in metres, extra turn about Y, lean forward), both turns in radians. Any other motion: none.
static func body_pose(motion: Array, x: float) -> Vector3:
	var move: String = motion[3] if motion.size() > 3 else ""
	var swell := sin(PI * clampf(x, 0.0, 1.0))
	match move:
		"lunge":
			return Vector3(0.0, 0.0, LUNGE_LEAN * swell)
		"leap":
			var up := sin(PI * clampf(x / 0.6, 0.0, 1.0))
			return Vector3(LEAP_HEIGHT * up, 0.0, LEAP_LEAN * smoothstep(0.35, 0.6, x) * (1.0 - x))
		"stomp":
			var hop := sin(PI * clampf((x - 0.15) / 0.4, 0.0, 1.0))
			return Vector3(STOMP_HEIGHT * hop, 0.0, STOMP_LEAN * swell)
		"spin":
			return Vector3(0.0, TAU * smoothstep(0.1, 0.9, x), 0.0)
		"rise":
			var lifted := smoothstep(0.0, 0.3, x) * (1.0 - smoothstep(0.75, 1.0, x))
			return Vector3(RISE_HEIGHT * lifted, 0.0, 0.0)
		"tremble":
			return Vector3(0.0, TREMBLE_TURN * sin(x * 90.0) * swell, TREMBLE_LEAN * swell)
	return Vector3.ZERO
