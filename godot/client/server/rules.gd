extends RefCounted
## The numbers of the single-player game that the online game plays with (pyport
## pow_server/sp_rules.py): the four heroes' base stats and what a skill costs on the online
## game's 0..100 MP gauge.

const Profile := preload("res://scripts/core/profile.gd")

## [HP, MP, ATK, DEF] of each face (0 Warrior, 1 Guardian, 2 Mystic, 3 Berserker).
const HERO_BASES: Array = Profile.HERO_BASES
## online skill code (3..13) -> the single-player skill index
const SP_INDEX := {3: 0, 4: 1, 5: 2, 9: 3, 10: 4, 11: 5, 12: 6, 13: 7, 6: 8, 7: 9, 8: 10}
## MP a skill takes in the single player: base + (level - 1) * inc, by the single-player index
const SKILL_MP_BASE := [5, 6, 7, 10, 15, 7, 10, 10, 8, 9, 10, 5, 6, 7, 9, 12, 20, 20, 20]
const SKILL_MP_INC := [3, 4, 5, 3, 4, 3, 3, 5, 3, 4, 5, 3, 4, 5, 5, 6, 5, 5, 5]


## MP of an online skill (3..13) at `level` in the single player.
static func skill_mp(skill: int, level: int) -> int:
	var i: int = SP_INDEX[skill]
	return SKILL_MP_BASE[i] + (maxi(1, level) - 1) * SKILL_MP_INC[i]


## The cost on the 0..100 MP gauge: the share of the hero's MP the skill takes in the single
## player (Wind Slasher Lv1 = 5 MP of a new hero's 10 -> 50); above the hero's MP, a full gauge.
static func skill_cost(skill: int, level: int, max_mp: int) -> int:
	var mp := skill_mp(skill, level)
	var per := maxi(1, max_mp)
	return clampi((100 * mp + per - 1) / per, 1, 100)
