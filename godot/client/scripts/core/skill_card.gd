extends RefCounted
## The skill card of the Skills screen (as pyport's SKILL_CARD): the skill's name and level,
## what it is, its MP and what it does at this level (damage and strikes, heal, buff and how
## long) and at the next one. The numbers come from the formulas of the fight (MapSim).

const MapSim := preload("res://scripts/sim/map_sim.gd")
const MAX_LEVEL := 10
## The hit frame of the one-strike skills.
const HIT_FRAME := {21: 5, 22: 6, 23: 5, 24: 5}
## Attack / defence buff = stat * level / this, for skills 17, 18, 19.
const BUFF_DIV := {17: 20, 18: 20, 19: 25}


## The MP a skill costs at a level (from 1).
static func mp_need(skill: int, level: int) -> int:
	if skill < 12 or skill > 30:
		return 0
	var k := skill - 12
	return int(MapSim.SKILL_BASE_COST[k]) + (maxi(level, 1) - 1) * int(MapSim.SKILL_COST_PER_LEVEL[k])


## The frames of the hero's action `skill`.
static func frames(skill: int) -> int:
	var seq: Array = MapSim.hero_anim(skill, 0)
	var n := 0
	while n < seq.size() and int(seq[n]) <= 200:
		n += 1
	return n


## How many times the skill strikes.
static func strikes(skill: int) -> int:
	var n := frames(skill)
	if n == 0:
		n = 30
	var count := 0
	for f in n:
		match skill:
			12:
				count += 1 if f > 2 and f < 6 else 0
			13:
				count += 1 if f > 4 and f < 8 else 0
			14:
				count += 1 if f in [2, 4, 6, 8] else 0
			20, 25:
				count += f & 1
	if skill in HIT_FRAME or skill in [26, 27, 28, 29, 30]:
		return 1
	return count


## What the skill does at a level, for a hero of this attack, defence and max HP.
## speed_seconds: the seconds of one tick (Settings.tick_seconds()).
static func effect(skill: int, level: int, attack: int, defense: int, max_hp: int, tick_seconds: float) -> String:
	var i := skill - 12
	if skill in [12, 13, 14] or (skill >= 20 and skill <= 30):
		var bonus := attack * level / int(MapSim.table("skill_attack_div")[i])
		var n := strikes(skill)
		return "DMG %d%s%s" % [attack + bonus, " x%d" % n if n > 1 else "", " all" if skill >= 28 else ""]
	if skill == 15:
		return "HP+%d" % (max_hp * (4 + level) / 25)
	if skill == 16:
		return "HP+%d" % (max_hp * (9 + level) / 20)
	if BUFF_DIV.has(skill):
		var ticks := 50 if level < 4 else (100 if level < 8 else 150)
		var parts: Array = []
		if skill != 18:
			parts.append("ATK+%d" % maxi(1, attack * level / int(BUFF_DIV[skill])))
		if skill != 17:
			parts.append("DEF+%d" % maxi(1, defense * level / int(BUFF_DIV[skill])))
		return "%s %ds" % [" ".join(PackedStringArray(parts)), int(ticks * tick_seconds)]
	return ""


## The card's lines: [text, heading?]. names / about: the skills' names and what they are.
static func lines(skill: int, level: int, names: Array, about: Array, attack: int, defense: int,
		max_hp: int, tick_seconds: float) -> Array:
	var i := skill - 12
	if i < 0 or i >= names.size():
		return [["Empty slot", false], ["OK: put a skill here", false]]
	var out: Array = [[str(names[i]) + ("  Lv%d" % level if level > 0 else ""), true]]
	if i < about.size():
		out.append([str(about[i]), false])
	var fx := func(lv: int) -> String:
		var e := effect(skill, lv, attack, defense, max_hp, tick_seconds)
		return "MP %d" % mp_need(skill, lv) + (", " + e if not e.is_empty() else "")
	if level == 0:
		out.append(["Not learned", false])
		out.append(["Lv1: " + fx.call(1), false])
		return out
	out.append([fx.call(level), false])
	out.append(["Lv%d: %s" % [level + 1, fx.call(level + 1)] if level < MAX_LEVEL else "Max level", false])
	return out
