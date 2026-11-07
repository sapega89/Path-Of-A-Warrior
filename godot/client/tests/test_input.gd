extends "res://tests/test_case.gd"

const InputSetupScript := preload("res://scripts/core/input_setup.gd")
const Offline := preload("res://scripts/screens/offline_screen.gd")
const MapViewer := preload("res://scripts/screens/map_viewer.gd")
const Help := preload("res://scripts/screens/help_screen.gd")
const MissionScreen := preload("res://scripts/screens/mission_screen.gd")


func test_actions_have_keys_and_pad() -> void:
	InputSetupScript.register()
	InputSetupScript.register()  # twice must not add duplicates
	for action in InputSetupScript.actions():
		check(InputMap.has_action(action), "%s missing" % action)
		var keys := 0
		var pad := 0
		for ev in InputMap.action_get_events(action):
			if ev is InputEventKey:
				keys += 1
			elif ev is InputEventJoypadButton or ev is InputEventJoypadMotion:
				pad += 1
		eq(keys, InputSetupScript.KEYS[action].size(), "%s keys" % action)
		if action != "belt_5":  # the fifth belt slot only by key (or put on * / #)
			check(pad >= 1, "%s has no gamepad binding" % action)


func _key_press(code: Key) -> InputEventKey:
	var ev := InputEventKey.new()
	ev.physical_keycode = code
	ev.pressed = true
	return ev


func _pad_press(button: JoyButton) -> InputEventJoypadButton:
	var ev := InputEventJoypadButton.new()
	ev.button_index = button
	ev.pressed = true
	return ev


func test_device_of_a_press() -> void:
	eq(InputSetupScript.device_of(_key_press(KEY_ENTER)), "keys", "a key")
	var echo := _key_press(KEY_ENTER)
	echo.echo = true
	eq(InputSetupScript.device_of(echo), "", "a held key's repeat changes nothing")
	eq(InputSetupScript.device_of(InputEventKey.new()), "", "nor a release")
	eq(InputSetupScript.device_of(_pad_press(JOY_BUTTON_A)), "pad", "a pad button")
	var stick := InputEventJoypadMotion.new()
	stick.axis = JOY_AXIS_LEFT_X
	stick.axis_value = 0.2
	eq(InputSetupScript.device_of(stick), "", "a stick near rest")
	stick.axis_value = -0.8
	eq(InputSetupScript.device_of(stick), "pad", "a stick pushed")
	var click := InputEventMouseButton.new()
	click.button_index = MOUSE_BUTTON_LEFT
	click.pressed = true
	eq(InputSetupScript.device_of(click), "", "the mouse changes nothing")
	var touch := InputEventScreenTouch.new()
	touch.pressed = true
	eq(InputSetupScript.device_of(touch), "touch", "a touch")


func test_hints_name_the_device_last_used() -> void:
	var was: String = InputSetup.device
	InputSetup.device = "keys"
	var seen := []
	var on_change := func(d: String) -> void: seen.append(d)
	InputSetup.device_changed.connect(on_change)
	eq(InputSetup.hint("online.battle_hint_bar"), "Enter / Space: stop the bar at the mark", "keys")
	eq(InputSetup.hint("offline.try_again"), "Enter: try again", "keys: Enter")
	InputSetup._input(_pad_press(JOY_BUTTON_A))
	eq(InputSetup.device, "pad", "a pad button")
	eq(InputSetup.hint("online.battle_hint_bar"), "A: stop the bar at the mark", "pad")
	eq(InputSetup.hint("offline.other_account"), "B: other account", "pad: B")
	var click := InputEventMouseButton.new()
	click.button_index = MOUSE_BUTTON_LEFT
	click.pressed = true
	InputSetup._input(click)
	eq(InputSetup.device, "pad", "a click changes nothing")
	InputSetup._input(_key_press(KEY_ESCAPE))
	eq(InputSetup.device, "keys", "a key")
	var touch := InputEventScreenTouch.new()
	touch.pressed = true
	InputSetup._input(touch)
	eq(InputSetup.hint("offline.try_again"), "OK: try again", "touch: OK, as before")
	eq(InputSetup.hint("viewer.info"), tr("viewer.info"), "no touch text: the keyboard's")
	eq(seen, ["pad", "keys", "touch"], "device_changed, once for each change")
	InputSetup.device_changed.disconnect(on_change)
	InputSetup.device = was


func test_offline_screen_and_map_viewer_follow_the_device() -> void:
	var was: String = InputSetup.device
	InputSetup.device = "keys"
	var offline: Control = Offline.new()
	root.add_child(offline)
	check(offline.text.text.ends_with("Enter: try again"), "the keyboard's OK")
	var viewer: Control = MapViewer.new()
	root.add_child(viewer)
	eq(viewer.info.text, "Map 1 / %d   [3] [4] change map   [Esc] back" % viewer.map_total, "keys")
	InputSetup._input(_pad_press(JOY_BUTTON_B))
	check(offline.text.text.ends_with("A: try again"), "the pad's OK")
	eq(viewer.info.text, "Map 1 / %d   [LB] [RB] change map   [B] back" % viewer.map_total, "pad")
	var click := InputEventMouseButton.new()
	click.button_index = MOUSE_BUTTON_LEFT
	click.pressed = true
	offline._gui_input(click)  # a click anywhere tries again
	InputSetup._input(_key_press(KEY_ENTER))
	eq(offline.text.text, tr("offline.connecting"), "a click tried again; Connecting... stays")
	offline.free()
	viewer.free()
	InputSetup.device = was


func _right_click() -> InputEventMouseButton:
	var ev := InputEventMouseButton.new()
	ev.button_index = MOUSE_BUTTON_RIGHT
	ev.pressed = true
	return ev


func test_right_click_is_back() -> void:
	check(InputSetupScript.is_back_click(_right_click()), "the right button")
	var up := _right_click()
	up.pressed = false
	check(not InputSetupScript.is_back_click(up), "not its release")
	var left := _right_click()
	left.button_index = MOUSE_BUTTON_LEFT
	check(not InputSetupScript.is_back_click(left), "not the left button")
	var old: Dictionary = Router.params
	Router.params = {}
	var help: Control = Help.new()
	root.add_child(help)
	help.open(2)
	help.get_viewport().push_input(_right_click())
	Input.flush_buffered_events()
	eq(help.topic, -1, "Help: back from a topic to the topics, as Esc")
	help.free()
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var mission: Control = MissionScreen.new()
	root.add_child(mission)
	mission.get_viewport().push_input(_right_click())
	Input.flush_buffered_events()
	check(mission.pause_menu == null, "on the map the right button is not BACK (it attacks)")
	mission.pause()
	check(mission.pause_menu != null, "paused")
	mission.get_viewport().push_input(_right_click())
	Input.flush_buffered_events()
	check(mission.pause_menu == null, "in the pause menu it is BACK: the game goes on")
	mission.free()
	Router.params = old


## The keyboard as pyport's: WASD and the numeric keypad move and choose in menus (5 and J are
## OK), Enter and Num 5 attack, Num 1 3 7 9 0 are the skills, and Backspace is BACK, except in
## a text field, where it deletes.
func test_keyboard_as_pyport() -> void:
	InputSetupScript.register()
	for pair in [[KEY_W, "ui_up"], [KEY_S, "ui_down"], [KEY_A, "ui_left"], [KEY_D, "ui_right"],
			[KEY_KP_8, "ui_up"], [KEY_KP_2, "ui_down"], [KEY_KP_4, "ui_left"], [KEY_KP_6, "ui_right"],
			[KEY_J, "ui_accept"], [KEY_KP_5, "ui_accept"], [KEY_ENTER, "attack"], [KEY_KP_5, "attack"],
			[KEY_KP_8, "move_up"], [KEY_KP_1, "skill_1"], [KEY_KP_0, "skill_5"]]:
		check(_key_press(pair[0]).is_action_pressed(pair[1]), "%s: %s" % [OS.get_keycode_string(pair[0]), pair[1]])
	check(InputSetupScript.is_back_key(_key_press(KEY_BACKSPACE)), "Backspace")
	check(not InputSetupScript.is_back_key(_key_press(KEY_ESCAPE)), "(Esc is ui_cancel itself)")
	var old: Dictionary = Router.params
	Router.params = {}
	var help: Control = Help.new()
	root.add_child(help)
	help.open(2)
	help.get_viewport().push_input(_key_press(KEY_BACKSPACE))
	Input.flush_buffered_events()
	eq(help.topic, -1, "Help: Backspace goes back, as Esc")
	help.open(2)
	var field := LineEdit.new()
	help.add_child(field)
	field.grab_focus()
	check(InputSetup.typing(), "a text field has the focus")
	help.get_viewport().push_input(_key_press(KEY_BACKSPACE))
	Input.flush_buffered_events()
	eq(help.topic, 2, "there Backspace deletes")
	help.free()
	Router.params = old


## The phone's Back button is BACK, and the game does not quit on it.
func test_phone_back_button() -> void:
	eq(ProjectSettings.get_setting("application/config/quit_on_go_back"), false, "no quitting on Back")
	var old: Dictionary = Router.params
	Router.params = {}
	var help: Control = Help.new()
	root.add_child(help)
	help.open(2)
	InputSetup._notification(Node.NOTIFICATION_WM_GO_BACK_REQUEST)
	Input.flush_buffered_events()
	eq(help.topic, -1, "Help: back from a topic, as Esc")
	help.free()
	Router.params = old



func test_the_pad_works_the_menus() -> void:
	InputSetupScript.register()
	var a := _pad_press(JOY_BUTTON_A)
	a.device = 1  # not only the first pad
	check(a.is_action("ui_accept") and a.is_action("attack"), "A: OK in the menus, attack on the map")
	var b := _pad_press(JOY_BUTTON_B)
	b.device = 3
	check(b.is_action("ui_cancel"), "B: BACK")
	var up := _pad_press(JOY_BUTTON_DPAD_UP)
	up.device = 2
	check(up.is_action("ui_up") and up.is_action("move_up"), "the d-pad moves in the menus and on the map")
	var stick := InputEventJoypadMotion.new()
	stick.device = 2
	stick.axis = JOY_AXIS_LEFT_X
	stick.axis_value = 1.0
	check(stick.is_action("ui_right"), "so does the left stick")
	var screen := Button.new()
	root.add_child(screen)
	var pressed := []
	screen.pressed.connect(func() -> void: pressed.append(true))
	screen.grab_focus()
	var release := _pad_press(JOY_BUTTON_A)
	release.pressed = false
	root.get_viewport().push_input(_pad_press(JOY_BUTTON_A))
	root.get_viewport().push_input(release)
	eq(pressed.size(), 1, "A pressed the focused button")
	screen.free()
