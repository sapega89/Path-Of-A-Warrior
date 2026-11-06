extends "res://tests/test_case.gd"

const Help := preload("res://scripts/screens/help_screen.gd")
const Keys := preload("res://scripts/core/input_setup.gd")


func test_help_screen() -> void:
	var old: Dictionary = Router.params
	Router.params = {}
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
	Router.params = old


func test_multiplayer_help() -> void:
	var old: Dictionary = Router.params
	Router.params = {"kind": "mp"}
	var screen: Control = Help.new()
	root.add_child(screen)
	eq(screen.topics.map(func(t): return t.name), ["Controls", "Menu", "Duel", "Missions", "About", "Network"])
	screen.open(1)
	eq(screen.page_label.text, "1 / 8", "Menu: its pages")
	eq(screen.text.text, "Duel\n\nDuel mode allows you to battle against enemies in a '1-on-1' or '2-on-2' battle.")
	screen.open(2)
	eq(screen.pages_of(2).size(), 18, "Duel")
	screen.open(0)
	eq(screen.pages_of(0), [tr("help.mp_control_1"), tr("help.mp_control_2")], "Controls: this version's battle keys")
	screen.free()
	Router.params = old


## Help > Control names the keys the game binds (scripts/core/input_setup.gd).
func test_control_names_the_bound_keys() -> void:
	var page := tr("help.control_1")
	var skills := []
	var belt := []
	for i in 5:
		skills.append(OS.get_keycode_string(Keys.KEYS["skill_%d" % (i + 1)][1]))
		belt.append(OS.get_keycode_string(Keys.KEYS["belt_%d" % (i + 1)][0]))
	check(page.contains("Skills 1-5: 1-5, or %s (X, Y, LB, RB, LT)" % " ".join(skills)), "skills")
	check(page.contains("Belt: %s" % " ".join(belt)), "belt")
	eq(Keys.KEYS["potion_1"], [KEY_KP_MULTIPLY], "potion *")
	eq(Keys.KEYS["potion_2"], [KEY_KP_DIVIDE], "potion #")
	check(page.contains("Num * and Num / (RT, L3)"), "potions")
	eq(Keys.PAD_BUTTONS["potion_2"], JOY_BUTTON_LEFT_STICK, "L3")
	eq(Keys.PAD_AXES["potion_1"][0], JOY_AXIS_TRIGGER_RIGHT, "RT")
	eq(Keys.PAD_AXES["skill_5"][0], JOY_AXIS_TRIGGER_LEFT, "LT")
	eq(Keys.KEYS["auto"], [KEY_TAB, KEY_F], "auto-hunt keys")
	check(tr("help.control_2").contains("Auto-hunt: Tab or F (R3)"), "auto-hunt")
	eq([Keys.KEYS["skip"], Keys.PAD_BUTTONS["skip"]], [[KEY_Q, KEY_F1], JOY_BUTTON_BACK], "skip keys")
	check(tr("help.control_2").contains("Skip a talk, the briefing or the story: Q or F1 (Back)"), "skip")
