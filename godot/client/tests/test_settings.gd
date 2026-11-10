extends "res://tests/test_case.gd"

const SettingsScript := preload("res://scripts/core/settings.gd")
const PATH := "user://test_settings.cfg"


func _fresh() -> Node:
	DirAccess.remove_absolute(ProjectSettings.globalize_path(PATH))
	var s: Node = SettingsScript.new()
	s.path = PATH
	s.load_from_disk()
	return s


func test_defaults() -> void:
	var s := _fresh()
	for key in SettingsScript.DEFAULTS:
		eq(s.get_value(key), SettingsScript.DEFAULTS[key], key)
	s.free()


func test_save_and_load() -> void:
	var s := _fresh()
	check(s.set_value("music_volume", 0.25), "set music")
	check(s.set_value("locale", "uk"), "set locale")
	var s2: Node = SettingsScript.new()
	s2.path = PATH
	s2.load_from_disk()
	eq(s2.get_value("music_volume"), 0.25, "music saved")
	eq(s2.get_value("locale"), "uk", "locale saved")
	s.set_value("locale", "")
	s.free()
	s2.free()
	DirAccess.remove_absolute(ProjectSettings.globalize_path(PATH))


func test_bad_values() -> void:
	var s := _fresh()
	check(not s.set_value("nope", 1), "unknown key")
	check(not s.set_value("fullscreen", "yes"), "wrong type")
	s.set_value("sfx_volume", 5)
	eq(s.get_value("sfx_volume"), 1.0, "clamped, int accepted")
	s.free()
	DirAccess.remove_absolute(ProjectSettings.globalize_path(PATH))


func test_game_speed() -> void:
	var s := _fresh()
	eq(s.tick_seconds(), 0.12, "Med: the simulation's own 120 ms")
	check(s.set_value("game_speed", 4), "Fast")
	eq(s.tick_seconds(), 0.05, "50 ms a tick")
	s.set_value("game_speed", 9)
	eq(s.get_value("game_speed"), 4, "clamped")
	s.set_value("game_speed", 0)
	eq(s.tick_seconds(), 0.25, "Slow: 250 ms")
	var s2: Node = SettingsScript.new()
	s2.path = PATH
	s2.load_from_disk()
	eq(s2.get_value("game_speed"), 0, "saved")
	s.free()
	s2.free()
	DirAccess.remove_absolute(ProjectSettings.globalize_path(PATH))


func test_volume_by_ear() -> void:
	eq(
		[0.25, 0.5, 0.75, 1.0].map(func(v): return roundi(SettingsScript.volume_db(v))),
		[-24, -12, -5, 0],
		"the amplitude is the volume squared, as in pyport"
	)
	var s := _fresh()
	s.set_value("music_volume", 0.5)
	eq(
		roundi(AudioServer.get_bus_volume_db(AudioServer.get_bus_index("Music"))),
		-12,
		"on the Music bus"
	)
	s.free()
	root.get_node("/root/Settings").apply_all()  # the game's own volumes again
	DirAccess.remove_absolute(ProjectSettings.globalize_path(PATH))


func test_brightness() -> void:
	var s := _fresh()
	eq(s.get_value("brightness"), 0.5, "the middle by default")
	eq(SettingsScript.world_gamma(0.5), 1.0, "the middle: the world as it is drawn")
	check(SettingsScript.world_gamma(1.0) < 1.0, "brighter: the shade lifted")
	check(SettingsScript.world_gamma(0.0) > 1.0, "darker: the shade deeper")
	check(
		SettingsScript.world_gamma(0.75) < 1.0 and SettingsScript.world_gamma(0.75) > 0.5,
		"a step up stays mild"
	)
	check(s.set_value("brightness", 3.0), "too bright")
	eq(s.get_value("brightness"), 1.0, "clamped")
	check(not "brightness" in SettingsScript.CLOUD_KEYS, "the screen's own, not the account's")
	s.free()
	DirAccess.remove_absolute(ProjectSettings.globalize_path(PATH))


func test_the_brightness_slider() -> void:
	var old_path: String = Settings.path
	Settings.path = PATH
	var screen: SettingsScreen = Router.make(Router.SCREENS["settings"])
	root.add_child(screen)
	eq(screen.brightness.value, Settings.get_value("brightness"), "shows the setting")
	screen.brightness.value = 0.7
	check(is_equal_approx(Settings.get_value("brightness"), 0.7), "and sets it")
	Settings.set_value("brightness", 0.5)
	screen.free()
	Settings.path = old_path
	DirAccess.remove_absolute(ProjectSettings.globalize_path(PATH))


func test_graphics_and_the_window() -> void:
	var s := _fresh()
	eq(s.get_value("graphics"), 1, "Medium by default")
	eq(SettingsScript.GRAPHICS[1].msaa, Viewport.MSAA_2X, "Medium smooths as the game did")
	check(
		0 < SettingsScript.GRAPHICS[0].lamps and SettingsScript.GRAPHICS[0].lamps < 2048,
		"Low: the lamps' and fires' shadows coarser (never none: the world went white)"
	)
	check(SettingsScript.GRAPHICS[2].lamps > SettingsScript.GRAPHICS[1].lamps, "High: finer")
	check(s.set_value("graphics", 9), "too high")
	eq(s.graphics(), SettingsScript.GRAPHICS[2], "clamped to High")
	check(s.set_value("game_speed", 4), "each number has its own range")
	eq(s.get_value("game_speed"), 4, "Fast is still there")
	eq(s.get_value("window_size"), 0, "the game's own window by default")
	s.set_value("window_size", 99)
	eq(s.get_value("window_size"), SettingsScript.WINDOW_SIZES.size() - 1, "clamped")
	eq(
		Array(SettingsScript.window_sizes_within(Vector2i(1920, 1080))),
		[0, 1, 2],
		"the sizes that fit the screen"
	)
	eq(Array(SettingsScript.window_sizes_within(Vector2i(1024, 600))), [0], "the first always")
	s.set_value("graphics", 1)
	s.free()
	DirAccess.remove_absolute(ProjectSettings.globalize_path(PATH))


func test_the_graphics_on_the_settings_screen() -> void:
	var old_path: String = Settings.path
	Settings.path = PATH
	var screen: SettingsScreen = Router.make(Router.SCREENS["settings"])
	root.add_child(screen)
	eq(screen.graphics.selected, 1, "Medium")
	screen.graphics.select(0)
	screen.graphics.item_selected.emit(0)
	eq(Settings.get_value("graphics"), 0, "Low chosen")
	check(screen.window_size == null, "no window here (headless), so no window size")
	Settings.set_value("graphics", 1)
	screen.free()
	Settings.path = old_path
	DirAccess.remove_absolute(ProjectSettings.globalize_path(PATH))
