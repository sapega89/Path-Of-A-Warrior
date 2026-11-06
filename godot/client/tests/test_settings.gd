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
