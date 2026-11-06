extends "res://tests/test_case.gd"

const MissionScreen := preload("res://scripts/screens/mission_screen.gd")


func test_pause_menu() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = MissionScreen.new()
	root.add_child(screen)
	check(screen.is_processing(), "the mission runs")
	screen.pause()
	check(not screen.is_processing(), "paused: the game stops")
	check(screen.pause_menu != null, "the pause menu shows")
	var names: Array = screen.pause_menu.buttons.map(func(b): return str(b.name))
	eq(names.slice(0, 3), ["Resume", "Options", "Exit"], "its rows")
	screen.pause_menu.open_options()
	check(screen.pause_menu.settings != null, "the settings over it")
	check(not screen.pause_menu.menu.visible, "the rows hidden meanwhile")
	screen.pause_menu.settings._back()
	check(screen.pause_menu.settings == null, "Back returns to the pause menu")
	check(screen.pause_menu.menu.visible, "the rows again")
	screen.pause_menu.resumed.emit()
	check(screen.pause_menu == null, "resumed: the menu goes")
	check(screen.is_processing(), "and the game runs on")
	screen.free()
	Router.params = old
