extends "res://tests/test_case.gd"
## The keys and pad buttons the player changes (Settings -> Controls): KeyBindings swaps them,
## Settings keeps them, InputSetup binds them, and the screen asks for them.

const InputSetupScript := preload("res://scripts/core/input_setup.gd")
const SettingsScript := preload("res://scripts/core/settings.gd")
const SETTINGS_PATH := "user://test_controls_settings.cfg"

var _old_path := ""


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


func _own_settings() -> void:
	_old_path = Settings.path
	Settings.path = SETTINGS_PATH


func _settings_back() -> void:
	Settings.set_value("controls", {})
	Settings.path = _old_path
	DirAccess.remove_absolute(ProjectSettings.globalize_path(SETTINGS_PATH))


func test_a_key_given_to_another_action_swaps() -> void:
	var b: KeyBindings = InputSetupScript.default_bindings()
	check(b.bind_key("attack", KEY_K), "attack on K")
	eq(
		b.keys.attack,
		[KEY_K, KEY_SPACE, KEY_ENTER, KEY_KP_ENTER, KEY_KP_5],
		"J gives way, the rest stay"
	)
	eq(b.keys.skill_5, [KEY_5, KEY_KP_0], "K was the fifth skill's other key: taken from it")
	check(b.bind_key("attack", KEY_Z), "attack on Z")
	eq(b.keys.belt_1, [KEY_K], "Z was the first belt slot's: it gets attack's old K")
	eq(b.keys.attack[0], KEY_Z, "Z attacks")
	check(b.bind_key("move_up", KEY_I), "up on I")
	eq(b.keys.move_up, [KEY_I, KEY_UP, KEY_KP_8], "the arrow and Num 8 still go up")
	eq(b.keys.skill_2, [KEY_2, KEY_KP_3], "I is no more the second skill's")
	check(b.bind_key("skill_1", KEY_1), "a key it has already")
	eq(b.keys.skill_1, [KEY_1, KEY_U, KEY_KP_1], "nothing changes")
	check(b.bind_key("skill_1", KEY_U), "its own other key")
	eq(b.keys.skill_1, [KEY_U, KEY_1, KEY_KP_1], "U first, and 1 still works")
	check(not b.bind_key("skill_1", KEY_ESCAPE), "Esc stays pause and BACK")
	check(not b.bind_key("skill_1", KEY_BACKSPACE), "Backspace stays BACK")
	check(not b.bind_key("pause", KEY_P), "pause does not change")
	check(not b.bind_key("nope", KEY_P), "nor what is no action")
	b.reset()
	eq(b.keys.attack, InputSetupScript.KEYS.attack, "Reset: the keys the game came with")


func test_a_pad_button_swaps_and_skip_follows_auto() -> void:
	var b: KeyBindings = InputSetupScript.default_bindings()
	eq(b.pads.skill_5, KeyBindings.trigger(JOY_AXIS_TRIGGER_LEFT), "LT is a pad input")
	check(b.bind_pad("attack", JOY_BUTTON_X), "attack on X")
	eq([b.pads.attack, b.pads.skill_1], [JOY_BUTTON_X, JOY_BUTTON_A], "the first skill gets A")
	check(b.bind_pad("skill_5", JOY_BUTTON_Y), "the fifth skill on Y")
	eq(b.pads.skill_2, KeyBindings.trigger(JOY_AXIS_TRIGGER_LEFT), "the second gets LT")
	check(b.bind_pad("auto", JOY_BUTTON_LEFT_SHOULDER), "auto-hunt on LB")
	eq(b.pads.skill_3, JOY_BUTTON_BACK, "the third skill gets Back")
	eq(b.pads.skip, JOY_BUTTON_LEFT_SHOULDER, "SKIP is the AUTO button")
	check(not b.can_change_pad("skip"), "so it is not changed by itself")
	check(not b.can_change_pad("move_up"), "the hero walks with the stick")
	check(b.can_change("move_up"), "but his keys change")
	check(not b.bind_pad("skill_1", JOY_BUTTON_B), "B stays BACK")
	check(not b.bind_pad("skill_1", JOY_BUTTON_START), "Start stays pause")


func test_the_changes_are_kept_and_taken_back() -> void:
	var b: KeyBindings = InputSetupScript.default_bindings()
	eq(b.changes(), {}, "nothing changed")
	b.bind_key("attack", KEY_K)
	b.bind_pad("auto", JOY_BUTTON_Y)
	var kept := b.changes()
	eq(kept["keys"].keys(), ["attack", "skill_5"], "only what differs")
	eq(kept.pads, {"skill_2": JOY_BUTTON_BACK, "auto": JOY_BUTTON_Y, "skip": JOY_BUTTON_Y}, "pads")
	var again: KeyBindings = InputSetupScript.default_bindings()
	again.take(kept)
	eq([again.keys, again.pads], [b.keys, b.pads], "taken back as they were")
	(
		again
		. take(
			{
				"keys": {"attack": [KEY_ESCAPE], "skill_1": [], "pause": [KEY_P], "nope": [KEY_P]},
				"pads": {"attack": JOY_BUTTON_START, "move_up": JOY_BUTTON_A, "skill_1": "A"},
			}
		)
	)
	eq(again.changes(), {}, "nothing that is BACK, pause, empty, unknown or not a number")
	again.take("garbage")
	eq(again.changes(), {}, "nor what is not a table")


func test_the_kept_controls_are_bound() -> void:
	_own_settings()
	var b: KeyBindings = InputSetupScript.default_bindings()
	b.bind_key("attack", KEY_K)
	b.bind_pad("attack", JOY_BUTTON_X)
	Settings.set_value("controls", b.changes())
	check(_key_press(KEY_K).is_action("attack"), "K attacks")
	check(not _key_press(KEY_J).is_action("attack"), "J no more")
	check(_key_press(KEY_SPACE).is_action("attack"), "the space bar still does")
	check(not _key_press(KEY_K).is_action("skill_5"), "K is no more a skill")
	var x := _pad_press(JOY_BUTTON_X)
	x.device = 2
	check(x.is_action("attack") and not x.is_action("skill_1"), "X attacks, on every pad")
	check(_pad_press(JOY_BUTTON_A).is_action("skill_1"), "A is the first skill")
	check(_pad_press(JOY_BUTTON_A).is_action("ui_accept"), "and still OK in the menus")
	eq(Glyphs.name_of("attack", "keys"), "K", "the hints name the new key")
	var stick := InputEventJoypadMotion.new()
	stick.axis = JOY_AXIS_LEFT_Y
	stick.axis_value = -1.0
	check(stick.is_action("move_up"), "the stick still walks")
	var later: Node = SettingsScript.new()
	later.path = SETTINGS_PATH
	later.load_from_disk()
	eq(later.get_value("controls"), b.changes(), "kept on the device")
	later.free()
	_settings_back()
	check(_key_press(KEY_J).is_action("attack"), "the defaults again")


func test_the_controls_screen_asks_for_the_new_key() -> void:
	_own_settings()
	var screen: ControlsScreen = Router.make(Router.SCREENS["controls"])
	root.add_child(screen)
	eq(screen.rows.size(), InputSetupScript.KEYS.size() - 1, "every action but pause")
	var attack: ControlsRow = screen.rows.attack
	eq(attack.key.text, "J", "the key the hints name")
	check(screen.rows.move_up.pad.disabled, "the stick walks: no pad button to change")
	check(screen.rows.skip.pad.disabled, "SKIP is the AUTO button")
	check(not attack.pad.disabled, "attack's button changes")
	attack.key.pressed.emit()
	eq(screen.waiting, {"action": "attack", "pad": false}, "waits for a key")
	check(screen.hint.text.contains(tr("controls.attack")), "says for what")
	screen._input(_key_press(KEY_K))
	eq(screen.waiting, {}, "taken")
	eq(attack.key.text, "K", "the new key")
	eq(screen.rows.skill_5.key.text, "5", "the fifth skill keeps its 5")
	check(_key_press(KEY_K).is_action("attack"), "bound at once")
	eq(Settings.get_value("controls")["keys"]["attack"][0], KEY_K, "and kept")
	attack.key.pressed.emit()
	screen._input(_key_press(KEY_ESCAPE))
	eq([screen.waiting, attack.key.text], [{}, "K"], "Esc: not now")
	attack.pad.pressed.emit()
	screen._input(_key_press(KEY_L))
	eq(screen.waiting.get("action"), "attack", "a pad button is awaited, not a key")
	screen._input(_pad_press(JOY_BUTTON_START))
	check(screen.hint.text == tr("controls.kept_for_back"), "Start stays pause")
	screen._input(_pad_press(JOY_BUTTON_X))
	check(_pad_press(JOY_BUTTON_X).is_action("attack"), "X attacks")
	eq(
		screen.rows.skill_1.pad.text,
		Glyphs.name_of("skill_1", "pad", InputSetup.pad_brand),
		"the first skill shows its new button"
	)
	screen.rows.potion_2.pad.pressed.emit()
	var rt := InputEventJoypadMotion.new()
	rt.axis = JOY_AXIS_TRIGGER_RIGHT
	rt.axis_value = 0.2
	screen._input(rt)
	eq(screen.waiting.get("action"), "potion_2", "a trigger barely pressed is not yet a press")
	rt.axis_value = 0.9
	screen._input(rt)
	check(rt.is_action("potion_2") and not rt.is_action("potion_1"), "RT: the second potion")
	screen.rows.skill_2.key.pressed.emit()
	screen.go_back()
	eq(screen.waiting, {}, "BACK while waiting: not now")
	screen.reset()
	eq([attack.key.text, Settings.get_value("controls")], ["J", {}], "Reset")
	var closed := []
	screen.close = func() -> void: closed.append(true)
	screen.go_back()
	eq(closed, [true], "Back over the settings closes it")
	screen.free()
	_settings_back()


func test_the_settings_show_the_controls_over_them() -> void:
	var settings: SettingsScreen = Router.make(Router.SCREENS["settings"])
	root.add_child(settings)
	var controls := settings.open_controls()
	check(controls.get_parent() == settings, "over the settings")
	check(not settings.column.visible, "their rows hidden meanwhile")
	controls.go_back()
	check(settings.column.visible, "Back: the settings again")
	check((settings.get_node("%Controls") as Button).has_focus(), "on Controls")
	settings.free()
