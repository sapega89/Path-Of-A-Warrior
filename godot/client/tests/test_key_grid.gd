extends "res://tests/test_case.gd"
## The on-screen keys (scripts/ui/key_grid.gd): the hero's name and the registration typed
## without a keyboard.


func _type(keys: VBoxContainer, labels: Array) -> void:
	for k in labels:
		keys.key(k).pressed.emit()


func test_the_heros_name_on_the_keys() -> void:
	var old: Dictionary = Router.params
	Router.params = {"profile_path": "user://test_key_grid.json"}
	var screen: Control = NewGameScreen.new()
	root.add_child(screen)
	screen.choose_head(1)
	var keys: VBoxContainer = screen.body.get_node("Keys")
	eq(keys.keys.size(), 26 * 2 + 2, "the letters in both cases, BACK and OK")
	_type(keys, ["I", "v", "a", "x", KeyGrid.BACK, "n"])
	eq(screen.name_edit.text, "Ivan", "typed, one taken back")
	_type(keys, ["o", "v", "i", "c", "h", "e", "s"])
	eq(screen.name_edit.text, "Ivanovic", "no more than 8")
	keys.key(KeyGrid.OK).pressed.emit()
	eq(
		[screen.step, screen.profile.hero_name],
		[NewGameScreen.Step.POINTS, "Ivanovic"],
		"OK: as Enter in the field"
	)
	screen.free()
	Router.params = old


func test_the_login_on_the_keys() -> void:
	var screen: Control = LoginScreen.new()
	root.add_child(screen)
	var keys: VBoxContainer = screen.keys
	_type(keys, ["A", "N", "7", "D", "Y"])
	eq(screen.user_id.text, "ANDY", "the UserID keeps only letters")
	keys.key(KeyGrid.OK).pressed.emit()
	check(screen.password.has_focus(), "OK: on to the password")
	_type(keys, ["1", "2", "Q", "3"])
	eq(screen.password.text, "123", "the password only digits")
	keys.key(KeyGrid.OK).pressed.emit()
	eq(screen.info.text, tr("register.bad_password"), "OK: as Enter, the account is checked")
	screen.free()


func test_the_keys_show_only_for_the_gamepad() -> void:
	var was: String = InputSetup.device
	InputSetup.device = "keys"
	var screen: Control = LoginScreen.new()
	root.add_child(screen)
	check(not screen.keys.visible, "a keyboard: no keys on the screen")
	var pad := InputEventJoypadButton.new()
	pad.button_index = JOY_BUTTON_DPAD_DOWN
	pad.pressed = true
	InputSetup._input(pad)
	check(screen.keys.visible, "the gamepad: the keys")
	screen.keys.key("A").grab_focus()
	var touch := InputEventScreenTouch.new()
	touch.pressed = true
	InputSetup._input(touch)
	check(not screen.keys.visible, "a touch: the phone's own keyboard")
	check(screen.user_id.has_focus(), "the field has the focus back")
	screen.free()
	InputSetup.device = was
