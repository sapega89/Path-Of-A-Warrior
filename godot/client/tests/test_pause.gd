extends "res://tests/test_case.gd"

const SETTINGS_PATH := "user://test_pause_settings.cfg"


func test_pause_menu() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = Router.make(Router.SCREENS["mission"])
	root.add_child(screen)
	check(screen.is_processing(), "the mission runs")
	screen.pause()
	check(not screen.is_processing(), "paused: the game stops")
	check(screen.pause_menu != null, "the pause menu shows")
	var names: Array = screen.pause_menu.buttons.map(func(b): return str(b.name))
	eq(
		names.slice(0, 5),
		["Resume", "Items", "Options", "Help", "Exit"],
		"its rows: no Save, the camps keep the game"
	)
	eq(screen.pause_menu.name, &"Pause", "from its scene")
	check(screen.pause_menu.ask.safe_default, "exit asked with No first")
	check(screen.pause_menu.note.notice, "the notice has OK alone")
	screen.sim.quick_slots[2] = [4, 1]
	screen.pause_menu.open_items()
	var items: Control = screen.pause_menu.settings
	check(items is AssignItemsScreen, "Assign Items over it")
	items.press_slot(2)
	check(items.press_key(0), "slot 3 on the * key")
	eq(int(screen.sim.quick_keys[0]), 2, "the mission's key changed at once")
	items.go_back()
	check(screen.pause_menu.settings == null, "back to the pause menu")
	screen.pause_menu.buttons[4].pressed.emit()
	check(screen.pause_menu.ask.visible, "exit is asked first")
	screen.pause_menu.ask.hide()
	screen.pause_menu.open_options()
	check(screen.pause_menu.settings != null, "the settings over it")
	check(not screen.pause_menu.menu.visible, "the rows hidden meanwhile")
	screen.pause_menu.settings._back()
	check(screen.pause_menu.settings == null, "Back returns to the pause menu")
	check(screen.pause_menu.menu.visible, "the rows again")
	screen.pause_menu.open_help()
	check(screen.pause_menu.settings is HelpScreen, "the help over it")
	screen.pause_menu.settings.go_back()
	check(screen.pause_menu.settings == null, "leaving the help returns to the pause menu")
	screen.pause_menu.buttons[0].pressed.emit()
	check(screen.pause_menu == null, "Resume: the menu goes")
	check(screen.is_processing(), "and the game runs on")
	screen.free()
	Router.params = old


func test_game_speed_changed_in_the_pause_applies_at_once() -> void:
	var old_params: Dictionary = Router.params
	var old_path: String = Settings.path
	var old_speed: int = int(Settings.get_value("game_speed"))
	Settings.path = SETTINGS_PATH
	Settings.set_value("game_speed", 2)
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = Router.make(Router.SCREENS["mission"])
	root.add_child(screen)
	eq(screen.tick, Settings.SPEED_MS[2] / 1000.0, "the mission starts at Med")
	screen.pause()
	screen.pause_menu.open_options()
	var options: SettingsScreen = screen.pause_menu.settings
	options.speed.select(4)
	options.speed.item_selected.emit(4)
	eq(screen.tick, Settings.SPEED_MS[4] / 1000.0, "Fast at once, not from the next mission")
	options._back()
	screen.pause_menu.resumed.emit()
	eq(screen.tick, Settings.SPEED_MS[4] / 1000.0, "and on after the pause")
	screen.free()
	Settings.set_value("game_speed", old_speed)
	Settings.path = old_path
	DirAccess.remove_absolute(ProjectSettings.globalize_path(SETTINGS_PATH))
	Router.params = old_params
