extends "res://tests/test_case.gd"

const Keys := preload("res://scripts/core/input_setup.gd")


func test_help_screen() -> void:
	var old: Dictionary = Router.params
	Router.params = {}
	var screen: Control = Router.make(Router.SCREENS["help"])
	root.add_child(screen)
	eq(
		screen.topics.size(),
		10 if OnlineSection.BATTLES else 8,
		"eight of the campaign, two of the multiplayer while its battles are shown"
	)
	eq(str(screen.list.get_child(0).text), "Missions", "the first")
	screen.open(2)
	eq(screen.heading.text, "Blacksmith", "a topic")
	eq(screen.page_label.text, "1 / 6", "its pages")
	eq(screen.text.text, "The smith buys and sells things.", "its first page")
	screen.turn_page(-1)
	eq(screen.page, 5, "back from the first page to the last")
	screen.open(HelpScreen.CONTROL_TOPIC)
	eq(
		screen.pages_of(HelpScreen.CONTROL_TOPIC).size(),
		4 if OnlineSection.BATTLES else 2,
		"Control: this version's keys, on the map (and online while the battles are shown)"
	)
	check(not screen.text.text.contains("keypad"), "not the phone's keypad")
	screen.go_back()
	eq(screen.topic, -1, "back: the topics again")
	var closed := [false]
	screen.close = func(): closed[0] = true
	screen.go_back()
	check(closed[0], "and then out")
	screen.free()
	Router.params = old


func test_multiplayer_topics_in_the_same_help() -> void:
	var old: Dictionary = Router.params
	Router.params = {}
	var screen: Control = Router.make(Router.SCREENS["help"])
	root.add_child(screen)
	if not OnlineSection.BATTLES:
		eq(
			screen.topics.slice(8),
			[],
			"no Duel or Online Missions while the online battles are hidden"
		)
		eq(
			screen.pages_of(HelpScreen.CONTROL_TOPIC),
			[tr("help.control_1"), tr("help.control_2")],
			"Control: only the map's keys"
		)
		screen.free()
		Router.params = old
		return
	eq(
		screen.topics.slice(8).map(func(t): return t.name),
		[tr("online.duel"), tr("menu.online_missions")]
	)
	eq(screen.pages_of(8).size(), 18, "Duel")
	eq(screen.pages_of(9).size(), 8, "Online Missions")
	eq(
		screen.pages_of(HelpScreen.CONTROL_TOPIC).slice(2),
		[tr("help.mp_control_1"), tr("help.mp_control_2")],
		"Control: then the online battle's keys"
	)
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
	check(
		page.contains(
			"Skills 1-5: 1-5, or %s, or Num 1 3 7 9 0 (X, Y, LB, RB, LT)" % " ".join(skills)
		),
		"skills"
	)
	var pad := []
	for i in 5:
		pad.append(OS.get_keycode_string(Keys.KEYS["skill_%d" % (i + 1)][2]))
	eq(pad, ["Kp 1", "Kp 3", "Kp 7", "Kp 9", "Kp 0"], "the phone's keys on the numeric keypad")
	check(page.contains("Belt: %s" % " ".join(belt)), "belt")
	eq(Keys.KEYS["potion_1"], [KEY_KP_MULTIPLY], "potion *")
	eq(Keys.KEYS["potion_2"], [KEY_KP_DIVIDE], "potion #")
	check(page.contains("Num * and Num / (RT, L3)"), "potions")
	check(
		page.contains("(the d-pad up, right, down, left; a press of the right stick, R3, for B)"),
		"belt: the d-pad"
	)
	eq(
		[Keys.PAD_BUTTONS["belt_1"], Keys.PAD_BUTTONS["belt_5"]],
		[JOY_BUTTON_DPAD_UP, JOY_BUTTON_RIGHT_STICK],
		"belt: the d-pad up, R3"
	)
	eq(Keys.PAD_BUTTONS["auto"], JOY_BUTTON_BACK, "auto-hunt: Back")
	eq(Keys.PAD_BUTTONS["potion_2"], JOY_BUTTON_LEFT_STICK, "L3")
	eq(Keys.PAD_AXES["potion_1"][0], JOY_AXIS_TRIGGER_RIGHT, "RT")
	eq(Keys.PAD_AXES["skill_5"][0], JOY_AXIS_TRIGGER_LEFT, "LT")
	eq(Keys.KEYS["auto"], [KEY_TAB, KEY_F], "auto-hunt keys")
	check(tr("help.control_2").contains("Auto-hunt: Tab or F (Back)"), "auto-hunt")
	eq(
		[Keys.KEYS["skip"], Keys.PAD_BUTTONS["skip"]],
		[[KEY_Q, KEY_F1], JOY_BUTTON_BACK],
		"skip keys"
	)
	check(
		tr("help.control_2").contains("Skip a talk, the briefing or the story: Q or F1 (Back)"),
		"skip"
	)
