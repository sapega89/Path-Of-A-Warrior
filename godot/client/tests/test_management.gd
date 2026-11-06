extends "res://tests/test_case.gd"

const Profile := preload("res://scripts/core/profile.gd")
const Attributes := preload("res://scripts/screens/attributes_screen.gd")
const Skills := preload("res://scripts/screens/skills_screen.gd")
const Items := preload("res://scripts/core/items.gd")
const AssignItems := preload("res://scripts/screens/assign_items_screen.gd")
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


func test_skills_data() -> void:
	var d: Dictionary = Skills.load_data()
	eq(d["names"].size(), 19, "19 skills")
	eq(d["names"][0], "Wind Slasher", "the first skill")
	eq(d["effects"][0], "Dash & Slash", "what it does")
	eq(d["groups"].size(), 7, "seven groups")
	eq(d["groups"][0], "MOVE", "the first group")
	eq(d["rows"].size(), 7, "a row a group")


func test_skills_screen() -> void:
	var p := Profile.new()
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var screen: Control = Skills.new()
	root.add_child(screen)
	eq(screen.keys.size(), 5, "five skill keys")
	eq(screen.describe(12), "Wind Slasher / Lv1 Dash & Slash", "a learned skill")
	check(screen.describe(13).ends_with("/ (Not Available)"), "a skill not learned: %s" % screen.describe(13))
	screen.press_key(2)
	eq(screen.slot, 2, "the third key is set")
	check(not screen.press_skill(13), "a skill not learned stays off the keys")
	check(screen.press_skill(17), "a learned one goes on")
	eq(int(screen.profile.hotkeys[2]), 17, "on the third key")
	screen.press_key(0)
	eq(int(screen.profile.hotkeys[0]), 0, "picking a key that holds a skill takes it off")
	var saved: RefCounted = Profile.load_or_new(TEST_PATH)
	var saved_keys: Array = []
	for k in saved.hotkeys:
		saved_keys.append(int(k))
	eq(saved_keys, [0, 17, 17, 0, 0], "saved")
	screen.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))


func test_potion_keys() -> void:
	var p := Profile.new()
	p.quick_slots[0] = [1, 3]
	p.quick_slots[2] = [4, 1]
	check(not p.assign_quick_key(0, 1), "an empty slot")
	check(not p.assign_quick_key(0, 0), "already on that key")
	check(p.assign_quick_key(1, 2), "the blue potion on the second key")
	eq(p.quick_keys, [0, 2], "keys")
	check(p.assign_quick_key(0, 2), "the slot the other key holds")
	eq(p.quick_keys, [2, 0], "the keys swapped")
	eq(Items.describe_potion(1), "Red Potion (S) / Recover 30% of total HP", "a potion")
	eq(Items.describe_potion(10), " Powerful Bomb / Ranged ATK", "the bomb")


func test_assign_items_screen() -> void:
	var p := Profile.new()
	p.quick_slots[0] = [1, 3]
	p.quick_slots[3] = [5, 2]
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var screen: Control = AssignItems.new()
	root.add_child(screen)
	eq(screen.marks[0].text, "Z *", "the first key drinks from slot 1")
	eq(screen.marks[1].text, "X #", "the second from slot 2")
	check(screen.slots[3].icon != null, "the blue potion's icon")
	screen.press_slot(3)
	check(screen.press_key(1), "slot 4 on the second key")
	eq(screen.marks[3].text, "V #", "its mark moved")
	eq(screen.marks[1].text, "X", "slot 2 has no potion key now")
	eq(screen.describe(3), "Blue Potion(M) / Recover 60% of total MP", "the line")
	screen.free()
	var saved: RefCounted = Profile.load_or_new(TEST_PATH)
	eq(int(saved.quick_keys[1]), 3, "saved")
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))
