extends "res://tests/test_case.gd"

const Help := preload("res://scripts/screens/help_screen.gd")


func test_help_screen() -> void:
	var screen: Control = Help.new()
	root.add_child(screen)
	eq(screen.topics.size(), 8, "eight topics")
	eq(str(screen.list.get_child(0).text), "Missions", "the first")
	screen.open(2)
	eq(screen.heading.text, "Blacksmith", "a topic")
	eq(screen.page_label.text, "1 / 6", "its pages")
	eq(screen.text.text, "You can sell and buy items at the Blacksmith.", "its first page")
	screen.turn_page(-1)
	eq(screen.page, 5, "back from the first page to the last")
	screen.open(Help.CONTROL_TOPIC)
	eq(screen.pages_of(Help.CONTROL_TOPIC).size(), 2, "Control: this version's keys")
	check(not screen.text.text.contains("keypad"), "not the phone's keypad")
	screen.go_back()
	eq(screen.topic, -1, "back: the topics again")
	var closed := [false]
	screen.close = func(): closed[0] = true
	screen.go_back()
	check(closed[0], "and then out")
	screen.free()
