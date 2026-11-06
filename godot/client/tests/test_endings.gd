extends "res://tests/test_case.gd"

const Profile := preload("res://scripts/core/profile.gd")
const Endings := preload("res://scripts/screens/endings_screen.gd")
const TEST_PATH := "user://test_endings.json"


func test_titles() -> void:
	eq(Endings.title(0), "Main Ending", "the first")
	eq(Endings.title(23), "Battle Dragon", "the last")
	eq(Endings.pages(), 5, "five pages of five")


func test_endings_screen() -> void:
	var p := Profile.new()
	p.endings = (1 << 0) | (1 << 7)
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var screen: Control = Endings.new()
	root.add_child(screen)
	eq(screen.list.get_child_count(), 5, "five on a page")
	eq(screen.page_label.text, "1 / 5", "page 1")
	check(not screen.open(3), "an ending not reached does not play")
	eq(screen.info.text, "endings.locked", "it says why")
	screen.turn_page(-1)
	eq(screen.page, 4, "back from the first page to the last")
	eq(screen.list.get_child_count(), 4, "the last page has four")
	screen.turn_page(1)
	screen.turn_page(1)
	check(screen.reached(7), "ending 7 reached")
	check(not screen.reached(8), "8 not")
	screen.free()
	Router.params = old
