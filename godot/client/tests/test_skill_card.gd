extends "res://tests/test_case.gd"
## The numbers of the skill card, from the formulas of the fight.

const SkillCard := preload("res://scripts/core/skill_card.gd")


func test_mp_and_strikes() -> void:
	eq(SkillCard.mp_need(12, 1), 5, "Wind Slasher Lv1")
	eq(SkillCard.mp_need(12, 3), 11, "+3 a level")
	eq(SkillCard.strikes(12), 3, "Wind Slasher strikes three times")
	eq(SkillCard.strikes(14), 4, "Thunder Slasher four")
	eq(SkillCard.strikes(28), 1, "a whole-screen skill once")


func test_effects() -> void:
	eq(SkillCard.effect(15, 1, 10, 10, 100, 0.12), "HP+20", "a small heal: max HP * 5 / 25")
	eq(SkillCard.effect(17, 1, 40, 10, 100, 0.12), "ATK+2 6s", "an attack buff for 50 ticks")
	eq(SkillCard.effect(19, 8, 50, 25, 100, 0.12), "ATK+16 DEF+8 18s", "both, 150 ticks from Lv8")
	eq(SkillCard.effect(28, 2, 100, 0, 100, 0.12), "DMG 110 all", "Lv2 adds attack * 2 / 20, on all")
	var lines: Array = SkillCard.lines(12, 10, ["Wind Slasher"], ["Dash & Slash"], 20, 5, 100, 0.12)
	eq(lines[-1][0], "Max level", "nothing after Lv10")
