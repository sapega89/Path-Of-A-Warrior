extends "res://tests/test_case.gd"

const Profile := preload("res://scripts/core/profile.gd")
const Attributes := preload("res://scripts/screens/attributes_screen.gd")
const TEST_PATH := "user://test_attributes.json"


func test_points_spent() -> void:
	var p := Profile.new()
	check(p.spend_point(Profile.Stat.HP), "HP")
	check(p.spend_point(Profile.Stat.MP), "MP")
	check(p.spend_point(Profile.Stat.ATTACK), "attack")
	check(p.spend_point(Profile.Stat.DEFENSE), "defence")
	eq(p.max_hp(), 35, "HP +5")
	eq(p.max_mp(), 13, "MP +3")
	eq(p.attack(), 7, "attack +1")
	eq(p.defense(), 5, "defence +1")
	eq(p.stat_points, 1, "one point left")
	check(p.spend_point(Profile.Stat.HP), "the last point")
	check(not p.spend_point(Profile.Stat.HP), "no point left")
	eq(p.max_hp(), 40, "nothing more")


func test_attributes_screen() -> void:
	var p := Profile.new()
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var screen: Control = Attributes.new()
	root.add_child(screen)
	eq(screen.values["Points"].text, "5", "five points")
	eq(screen.values["ATK"].text, "5+1", "own attack and the claymore's")
	eq(screen.values["HP"].text, "30", "HP")
	for i in 3:
		screen.plus["HP"].pressed.emit()
	screen.plus["DEF"].pressed.emit()
	screen.plus["DEF"].pressed.emit()
	eq(screen.values["HP"].text, "45", "three points on HP")
	eq(screen.values["DEF"].text, "6", "two on defence")
	eq(screen.values["Points"].text, "0", "none left")
	check(screen.plus["MP"].disabled, "the + buttons are off")
	check(not screen.spend(Profile.Stat.MP), "nothing to spend")
	var saved: RefCounted = Profile.load_or_new(TEST_PATH)
	eq(saved.max_hp(), 45, "saved")
	eq(saved.stat_points, 0, "the points saved")
	screen.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))
