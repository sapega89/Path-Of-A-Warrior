extends "res://tests/test_case.gd"

const TEST_PATH := "user://test_endings.json"


func test_titles() -> void:
	eq(EndingsScreen.title(0), "The Long Road", "the first")
	eq(EndingsScreen.title(23), "Banner Knight", "the last")
	eq(EndingsScreen.pages(), 5, "five pages of five")


func test_endings_screen() -> void:
	var p := Profile.new()
	p.endings = (1 << 0) | (1 << 7)
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var screen: Control = Router.make(Router.SCREENS["endings"])
	root.add_child(screen)
	eq(screen.list.get_child_count(), 5, "five on a page")
	eq(screen.list.get_child(0).theme_type_variation, &"", "one reached as any button")
	eq(screen.list.get_child(3).theme_type_variation, &"LockedButton", "one not reached greyed")
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
