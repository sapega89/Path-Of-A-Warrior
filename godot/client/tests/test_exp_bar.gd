extends "res://tests/test_case.gd"
## The exp bar of the pages after a won mission (pyport's draw_exp_bar): what the hero had,
## what the mission gives growing 4 px a tick, a level up at the end of the bar.

const Profile := preload("res://scripts/core/profile.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")
const ExpBar := preload("res://scripts/ui/exp_bar.gd")
const MissionScreen := preload("res://scripts/screens/mission_screen.gd")


func test_the_bar_grows_and_goes_up_a_level() -> void:
	var bar: Control = ExpBar.new()
	eq(Profile.exp_needed(1), 50, "level 1 needs 50")
	eq(Profile.exp_needed(2), 104, "level 2 needs 104")
	bar.begin(1, 25, 50)
	eq(bar.bars, [50, 124, 124], "half of level 1; 25 of 104 into level 2 after the mission")
	eq(bar.grown(), [0, 0], "nothing grown yet")
	for t in 13:
		bar.tick()
	eq(bar.grown(), [50, 1], "the bar is full")
	eq(bar.level, 1, "the level up comes on the next tick")
	bar.tick()
	eq([bar.level, bar.level_up_ticks], [2, ExpBar.LEVEL_UP_TICKS], "Level Up : Lv 2, for 20 ticks")
	eq(bar.bars, [0, 24, 24], "the bar starts again with the rest")
	for t in ExpBar.LEVEL_UP_TICKS:
		bar.tick()
	eq([bar.level_up_ticks, bar.step], [0, 0], "it waits while Level Up shows")
	for t in 7:
		bar.tick()
	eq(bar.grown(), [24, 2], "all of it shown")
	var p: RefCounted = Profile.new()
	p.experience = 25
	p.gain_exp(50)
	eq([p.level, p.experience * 100 / Profile.exp_needed(p.level)], [bar.level, 24],
		"the bar ends where the hero is after the mission")
	bar.begin_time(60)
	eq(bar.bars, [0, 24, 33], "Time Exp: 10 more, from the end of the mission's part")
	eq(bar.part, 1, "the time's part grows")
	bar.tick()
	bar.tick()
	eq(bar.grown(), [8, 0], "4 px a tick")
	bar.begin(1, 0, 0)
	eq(bar.bars, [0, 1, 1], "nothing gained: at least a little into the level")
	bar.free()


func test_the_exp_pages_show_the_bar() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = MissionScreen.new()
	root.add_child(screen)
	var sim: RefCounted = screen.sim
	screen.profile.level = 1
	screen.profile.experience = 45
	sim.mission_exp = 10
	sim.difficulty = 1
	sim.banner = MapSim.BANNER_TOTAL_EXP
	screen.tick_exp_bar()
	screen._show_banner()
	check(screen.exp_bar.visible, "Total Exp: the bar under the text")
	eq(screen.exp_bar.bars[0], 90, "45 of 50")
	check(not screen.banner_text.text.contains("Lv"), "no level up yet")
	for t in 4:
		screen.tick_exp_bar()
	screen._show_banner()
	check(screen.banner_text.text.ends_with(screen.tr("mission.level_up") % 2), screen.banner_text.text)
	sim.banner = MapSim.BANNER_TIME_EXP
	screen.tick_exp_bar()
	eq(screen.exp_bar.part, 1, "Time Exp: the time's part")
	sim.banner = MapSim.BANNER_STAGE_CLEAR
	screen._show_banner()
	check(not screen.exp_bar.visible, "no bar on other banners")
	screen.free()
	Router.params = old
