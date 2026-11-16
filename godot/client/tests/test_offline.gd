extends "res://tests/test_case.gd"
## The game is offline: the hero and the settings are kept in files on this computer, and the
## main menu goes on to the game without a server or a login.

const HERO_PATH := "user://test_offline_hero.json"
const SETTINGS_PATH := "user://test_offline_settings.cfg"


func test_the_hero_is_kept_in_a_file() -> void:
	DirAccess.remove_absolute(ProjectSettings.globalize_path(HERO_PATH))
	check(not Profile.exists(HERO_PATH), "no hero yet")
	var p: RefCounted = Profile.new()
	p.gold = 123
	check(p.save(HERO_PATH), "saved")
	check(FileAccess.file_exists(HERO_PATH), "in its own file")
	check(Profile.exists(HERO_PATH), "a hero now")
	eq(Profile.load_or_new(HERO_PATH).gold, 123, "read back from the file")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(HERO_PATH))


func test_the_settings_file_has_only_the_settings() -> void:
	DirAccess.remove_absolute(ProjectSettings.globalize_path(SETTINGS_PATH))
	var s: Node = load("res://scripts/core/settings.gd").new()
	s.path = SETTINGS_PATH
	s.load_from_disk()
	check(s.set_value("music_volume", 0.3), "a volume changed")
	var cfg := ConfigFile.new()
	eq(cfg.load(SETTINGS_PATH), OK, "saved on this computer")
	eq(Array(cfg.get_sections()), ["settings"], "no account's copy beside them")
	eq(cfg.get_value("settings", "music_volume"), 0.3, "the volume")
	s.free()
	DirAccess.remove_absolute(ProjectSettings.globalize_path(SETTINGS_PATH))


func test_the_menu_goes_on_without_a_login() -> void:
	check(not Router.SCREENS.has("login"), "no login screen")
	check(not Router.SCREENS.has("offline"), "no No connection screen")
	check(root.get_node_or_null("/root/Cloud") == null, "nothing talks to a server")
	var host := Control.new()
	root.add_child(host)
	Router.attach(host)
	Router.go("main_menu")
	var had_hero := Profile.exists()
	(Router.current as MainMenu).new_game()
	eq(
		Router.current_name(),
		"main_menu" if had_hero else "new_game",
		"New game: a new hero at once, or the question over a saved one"
	)
	Router.attach(null)
	host.free()
