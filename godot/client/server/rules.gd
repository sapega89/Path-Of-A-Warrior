class_name Rules
extends RefCounted
## The numbers of the single-player game that the online game plays with (pyport
## pow_server/sp_rules.py): the heroes' stats, the soldiers, what a skill costs on the online
## game's 0..100 MP gauge and what it does, the rewards, and the shop's gear of a level.

## [HP, MP, ATK, DEF] of each face (0 Cossack, 1 Serdiuk, 2 Kharakternyk, 3 Haidamaka).
const HERO_BASES: Array = Profile.HERO_BASES
## a new hero has 5 free points, +3 a level; a point gives HP +5 / MP +3 / ATK +1 / DEF +1
const POINTS_START := 5
const POINTS_PER_LEVEL := 3
const POINT_GAIN := {"atk": 1, "def": 1, "hp": 5, "mp": 3}
## soldiers: 0 swordsman, 1 archer, 2 squad
const SOLDIER_BASE := [3, 2, 3]
const SOLDIER_MULT := [100, 100, 150]
const SOLDIER_HP := [7, 5, 7]
## online skill code (3..13) -> the single-player skill index
const SP_INDEX := {3: 0, 4: 1, 5: 2, 9: 3, 10: 4, 11: 5, 12: 6, 13: 7, 6: 8, 7: 9, 8: 10}
## MP a skill takes in the single player: base + (level - 1) * inc, by the single-player index
const SKILL_MP_BASE := [5, 6, 7, 10, 15, 7, 10, 10, 8, 9, 10, 5, 6, 7, 9, 12, 20, 20, 20]
const SKILL_MP_INC := [3, 4, 5, 3, 4, 3, 3, 5, 3, 4, 5, 3, 4, 5, 5, 6, 5, 5, 5]
## an attack skill adds ATK * level / AU to every hit (by the single-player index)
const AU := [20, 20, 20, 0, 0, 0, 0, 0, 30, 25, 20]
## hits of the attack skills: Wind, Storm, Thunder, Tide, Wave, Tidal
const SKILL_HITS := {3: 3, 4: 3, 5: 4, 6: 6, 7: 1, 8: 1}
## the shop's tiers of every kind of gear (the level they are sold from)
const TIER_LEVELS := [1, 10, 25, 45, 70]
## the gear a hero of the shop wears: [kind, stat (0 ATK, 1 DEF, 2 HP)], one of each
const KIT := [[0, 0], [2, 1], [3, 1], [4, 2], [5, 2], [6, 2]]


## {hp, mp, atk, def} of a new hero of a face.
static func hero_base(face: int) -> Dictionary:
	var b: Array = HERO_BASES[face & 3]
	return {"hp": b[0], "mp": b[1], "atk": b[2], "def": b[3]}


## {atk, def, hp, mp} of a hero of `level` and `face` whose points went by `build` {stat: share}
## (the last stat gets what the shares leave).
static func hero_stats(level: int, build: Dictionary, face := 0) -> Dictionary:
	var points := POINTS_START + POINTS_PER_LEVEL * (level - 1)
	var total := 0
	for k in build:
		total += int(build[k])
	var out := hero_base(face)
	var given := 0
	var keys := build.keys()
	for i in keys.size():
		var n: int = (
			points - given
			if i == keys.size() - 1
			else points * int(build[keys[i]]) / maxi(1, total)
		)
		out[keys[i]] += n * int(POINT_GAIN[keys[i]])
		given += n
	return out


static func soldier_level(rng: RandomNumberGenerator, lp: int) -> int:
	if lp < 21:
		return maxi(1, lp + rng.randi_range(0, 4) - 2)
	if lp < 41:
		return lp + rng.randi_range(0, 8) - 3
	return lp + rng.randi_range(0, 15) - 5


static func soldier_stats(t: int, level: int) -> Dictionary:
	return {
		"atk": (SOLDIER_BASE[t] + level) * SOLDIER_MULT[t] / 100,
		"def": level - 1,
		"hp": SOLDIER_HP[t] + 3 * level
	}


## MP of an online skill (3..13) at `level` in the single player.
static func skill_mp(skill: int, level: int) -> int:
	var i: int = SP_INDEX[skill]
	return SKILL_MP_BASE[i] + (maxi(1, level) - 1) * SKILL_MP_INC[i]


## The cost on the 0..100 MP gauge: the share of the hero's MP the skill takes in the single
## player (Whirlwind Sabre Lv1 = 5 MP of a new hero's 10 -> 50); above the hero's MP, a full gauge.
static func skill_cost(skill: int, level: int, max_mp: int) -> int:
	var mp := skill_mp(skill, level)
	var per := maxi(1, max_mp)
	return clampi((100 * mp + per - 1) / per, 1, 100)


## The extra damage of every hit of an attack skill.
static func skill_bonus(skill: int, atk: int, level: int) -> int:
	var au: int = AU[SP_INDEX[skill]]
	return atk * level / au if au > 0 else 0


## HP of Healing Herbs (maxHP * (4 + lvl) / 25) and Living Water (maxHP * (9 + lvl) / 20).
static func heal(skill: int, max_hp: int, level: int) -> int:
	return max_hp * (4 + level) / 25 if skill == 9 else max_hp * (9 + level) / 20


## [ATK bonus, DEF bonus, ticks] of a soul: Devil max(1, ATK * lvl / 20), Guardian
## max(1, DEF * lvl / 20), Arch angel ATK * lvl / 25 and DEF * lvl / 25; 50 / 100 / 150 ticks
## below level 4 / 8 / above.
static func soul(skill: int, atk: int, def: int, level: int) -> Array:
	var ticks := 50 if level < 4 else (100 if level < 8 else 150)
	if skill == 11:
		return [maxi(1, atk * level / 20), 0, ticks]
	if skill == 12:
		return [0, maxi(1, def * level / 20), ticks]
	return [atk * level / 25, def * level / 25, ticks]


## What a beaten foe adds up for the rewards: its level, twice for a general.
static func kill_value(level: int, general: bool) -> int:
	return 2 * level if general else level


## [fame, exp, gold] of a mission accomplished on Normal: Fame dY, EXP (dY + dY / 20 in time)
## * 2, gold h * 150.
static func mission_end(dy: int, in_time: bool, h: int) -> Array:
	return [dy, (dy + (dy / 20 if in_time else 0)) * 2, h * 150]


## {atk, def, hp} of the best Normal gear of each kind a hero of `level` can buy: what a CPU
## fighter wears. Below the second tier a new hero's Iron Broadsword.
static func shop_kit(level: int) -> Dictionary:
	if level < TIER_LEVELS[1]:
		return {"atk": 1, "def": 0, "hp": 0}
	var tier := -1
	for lv in TIER_LEVELS:
		if level >= lv:
			tier += 1
	var out := {"atk": 0, "def": 0, "hp": 0}
	var gear: Dictionary = Items.data().get("gear", {})
	for k in KIT:
		var best := 0
		for id in gear:
			var rec: Dictionary = gear[id]
			if (int(id) - 101) % 5 == tier and int(rec.slot) == k[0] and int(rec.stat) == k[1]:
				best = maxi(best, int(rec.bonus))
		out[["atk", "def", "hp"][k[1]]] += best
	return out
