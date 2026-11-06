extends "res://tests/test_case.gd"

const InputSetupScript := preload("res://scripts/core/input_setup.gd")
const Offline := preload("res://scripts/screens/offline_screen.gd")
const MapViewer := preload("res://scripts/screens/map_viewer.gd")


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
	offline.try_again()
	InputSetup._input(_key_press(KEY_ENTER))
	eq(offline.text.text, tr("offline.connecting"), "Connecting... stays")
	offline.free()
	viewer.free()
	InputSetup.device = was
