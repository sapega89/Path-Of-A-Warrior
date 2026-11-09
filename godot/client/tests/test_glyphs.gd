extends "res://tests/test_case.gd"
## The names of keys and buttons in the hints and the HUD (scripts/ui/glyphs.gd): read from the
## bindings, for the device just used and the maker of the pad.

const Glyphs := preload("res://scripts/ui/glyphs.gd")
const InputSetupScript := preload("res://scripts/core/input_setup.gd")
const LoginScreen := preload("res://scripts/screens/login_screen.gd")
const NewGame := preload("res://scripts/screens/new_game_screen.gd")


func test_the_pad_maker_from_its_name() -> void:
	eq(Glyphs.brand_of("Xbox Series Controller"), "xbox", "Xbox")
	eq(Glyphs.brand_of("XInput Gamepad (GLFW)"), "xbox", "XInput")
	eq(Glyphs.brand_of("PS5 Controller"), "ps", "PS5")
	eq(Glyphs.brand_of("Sony DualShock 4"), "ps", "DualShock")
	eq(Glyphs.brand_of("Nintendo Switch Pro Controller"), "nintendo", "Switch Pro")
	eq(Glyphs.brand_of("Logitech F310"), "generic", "another pad")
	eq(Glyphs.brand_of(""), "generic", "no name")


func test_keyboard_names() -> void:
	InputSetupScript.register()
	eq(Glyphs.name_of("ui_accept", "keys"), "Enter", "OK")
	eq(Glyphs.name_of("ui_cancel", "keys"), "Esc", "BACK")
	eq(Glyphs.name_of("attack", "keys"), "J", "attack: its first key")
	eq(Glyphs.name_of("skill_1", "keys"), "1", "a skill")
	eq(Glyphs.name_of("belt_5", "keys"), "B", "the belt")
	eq(Glyphs.name_of("potion_1", "keys"), "Num *", "a potion key on the numeric keypad")
	eq(Glyphs.name_of("ui_move", "keys"), "Arrows / WASD", "the menus' arrows")
	eq(Glyphs.name_of("ui_click", "keys"), "Enter / click", "OK or a click")
	eq(Glyphs.name_of("skip", "touch"), "Q", "touch: the keyboard's names")
	eq(Glyphs.name_of("no_such_action", "keys"), "", "nothing bound")


func test_pad_names_by_maker() -> void:
	InputSetupScript.register()
	var cases := {
		"ui_accept": ["A", "A", "Cross", "B"],
		"ui_cancel": ["B", "B", "Circle", "A"],
		"skill_1": ["X", "X", "Square", "Y"],
		"skill_3": ["LB", "LB", "L1", "L"],
		"skill_5": ["LT", "LT", "L2", "ZL"],
		"potion_1": ["RT", "RT", "R2", "ZR"],
		"belt_5": ["R3", "RS", "R3", "RS"],
		"auto": ["Back", "View", "Share", "-"],
		"pause": ["Start", "Menu", "Options", "+"],
	}
	for action in cases:
		var got := []
		for brand in ["generic", "xbox", "ps", "nintendo"]:
			got.append(Glyphs.name_of(action, "pad", brand))
		eq(got, cases[action], action)
	eq(Glyphs.name_of("belt_1", "pad"), "D-pad up", "the belt on the d-pad")
	eq(Glyphs.name_of("move", "pad"), "Left stick", "the hero moves with the left stick")
	eq(Glyphs.name_of("ui_move", "pad"), "D-pad / stick", "the menus' d-pad")
	eq(Glyphs.name_of("ui_click", "pad"), "A", "no click on a pad")


func test_templates() -> void:
	InputSetupScript.register()
	var t := "{ui_accept}: OK · {ui_cancel}: back"
	eq(Glyphs.fill(t, "keys"), "Enter: OK · Esc: back", "the keyboard")
	eq(Glyphs.fill(t, "pad"), "A: OK · B: back", "a pad")
	eq(Glyphs.fill(t, "pad", "ps"), "Cross: OK · Circle: back", "a PlayStation pad")
	eq(Glyphs.fill("{nothing} {ui_accept}", "keys"), "{nothing} Enter", "a word that is no action stays")
	eq(Glyphs.fill("no braces", "pad"), "no braces", "a plain text")


## Every {word} of the strings is an action or one of the groups, so no hint shows braces.
func test_every_template_names_an_action() -> void:
	InputSetupScript.register()
	var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://i18n/strings.json"))
	var token := RegEx.create_from_string(Glyphs.TOKEN)
	var bad := []
	for key in data:
		for lang in data[key]:
			for m in token.search_all(str(data[key][lang])):
				var action := m.get_string(1)
				for device in ["keys", "pad"]:
					if Glyphs.name_of(action, device).is_empty():
						bad.append("%s %s: {%s} on %s" % [key, lang, action, device])
	eq(bad, [], "unknown words in braces")


func test_a_key_bound_later_is_named() -> void:
	InputMap.add_action("test_glyph")
	var ev := InputEventKey.new()
	ev.physical_keycode = KEY_K
	InputMap.action_add_event("test_glyph", ev)
	eq(Glyphs.fill("{test_glyph}: go", "keys"), "K: go", "as it is bound")
	InputMap.erase_action("test_glyph")


func test_hud_labels() -> void:
	InputSetupScript.register()
	eq(Glyphs.short_of("belt_1", "keys"), {"text": "Z"}, "a key")
	eq(Glyphs.short_of("skill_3", "pad", "xbox"), {"text": "LB"}, "a shoulder")
	eq(Glyphs.short_of("belt_1", "pad"), {"dpad": Vector2.UP}, "the d-pad up")
	eq(Glyphs.short_of("belt_4", "pad", "ps"), {"dpad": Vector2.LEFT}, "the d-pad left, on any pad")
	eq(Glyphs.short_of("belt_5", "pad", "ps"), {"text": "R3"}, "a press of the right stick")
	eq(Glyphs.short_of("skill_2", "pad", "ps"), {"shape": "triangle"}, "PlayStation: its shape")
	eq(Glyphs.short_of("skill_1", "touch"), {}, "no label on touch")


func test_hints_follow_the_pad_maker() -> void:
	var was: Array = [InputSetup.device, InputSetup.pad_brand]
	InputSetup.device = "keys"
	eq(InputSetup.hint("hint.menu"), "Arrows / WASD: choose · Enter: OK · Esc / right click: back",
		"the keyboard")
	InputSetup.device = "pad"
	InputSetup.pad_brand = "generic"
	eq(InputSetup.hint("hint.menu"), "D-pad / stick: choose · A: OK · B: back", "a pad")
	InputSetup.pad_brand = "ps"
	eq(InputSetup.hint("hint.menu"), "D-pad / stick: choose · Cross: OK · Circle: back", "PlayStation")
	eq(InputSetup.hint("hint.skip"), "Cross: next · Share / Circle: skip", "its Share skips")
	InputSetup.pad_brand = "nintendo"
	eq(InputSetup.key_name("ui_accept"), "B", "Nintendo: OK is the bottom button, B")
	InputSetup.device = "touch"
	eq(InputSetup.hint("hint.menu"), tr("hint.menu_touch"), "touch: its own words")
	InputSetup.device = was[0]
	InputSetup.pad_brand = was[1]


## The login says what a field takes while it types, not the menus' arrows.
func test_login_hint_while_typing() -> void:
	var old: Dictionary = Router.params
	var was: String = InputSetup.device
	Router.params = {}
	var screen: Control = LoginScreen.new()
	root.add_child(screen)
	InputSetup.device = "keys"
	screen.user_id.grab_focus()
	eq(screen.controls_hint(), "UserID: letters A–Z · Enter: to the password", "the UserID")
	screen.password.grab_focus()
	eq(screen.controls_hint(), "Password: digits 0–9 · Enter: log in", "the password")
	screen.login_button.grab_focus()
	eq(screen.controls_hint(), InputSetup.hint("hint.menu"), "a button: the menus' line")
	InputSetup.device = "pad"
	screen.user_id.grab_focus()
	eq(screen.controls_hint(), InputSetup.hint("hint.menu"), "a pad types on the keys below")
	screen.free()
	InputSetup.device = was
	Router.params = old


func test_normal_comes_first() -> void:
	var old: Dictionary = Router.params
	Router.params = {"profile_path": "user://test_glyphs.json"}
	var screen: Control = NewGame.new()
	root.add_child(screen)
	eq(str(screen.body.get_child(0).name), "Difficulty1", "Normal first")
	eq(str(screen.body.get_child(1).name), "Difficulty0", "then Hard")
	check(tr("newgame.mode_0").contains("AUTO"), "Hard says it has no AUTO: %s" % tr("newgame.mode_0"))
	screen.free()
	Router.params = old
