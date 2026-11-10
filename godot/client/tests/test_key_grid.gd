extends "res://tests/test_case.gd"
## The on-screen keys (scripts/ui/key_grid.gd): the hero's name typed without a keyboard.


func _type(keys: VBoxContainer, labels: Array) -> void:
	for k in labels:
		keys.key(k).pressed.emit()


func test_the_heros_name_on_the_keys() -> void:
	var old: Dictionary = Router.params
	Router.params = {"profile_path": "user://test_key_grid.json"}
	var screen: Control = Router.make(Router.SCREENS["new_game"])
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


func test_the_keys_show_only_for_the_gamepad() -> void:
	var was: String = InputSetup.device
	var old: Dictionary = Router.params
	InputSetup.device = "keys"
	Router.params = {"profile_path": "user://test_key_grid.json"}
	var screen: Control = Router.make(Router.SCREENS["new_game"])
	root.add_child(screen)
	screen.choose_head(1)
	var keys: KeyGrid = screen.body.get_node("Keys")
	check(not keys.visible, "a keyboard: no keys on the screen")
	var pad := InputEventJoypadButton.new()
	pad.button_index = JOY_BUTTON_DPAD_DOWN
	pad.pressed = true
	InputSetup._input(pad)
	check(keys.visible, "the gamepad: the keys")
	keys.key("A").grab_focus()
	var touch := InputEventScreenTouch.new()
	touch.pressed = true
	InputSetup._input(touch)
	check(not keys.visible, "a touch: the phone's own keyboard")
	check(screen.name_edit.has_focus(), "the field has the focus back")
	screen.free()
	InputSetup.device = was
	Router.params = old
