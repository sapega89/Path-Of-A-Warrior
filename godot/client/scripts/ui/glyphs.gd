extends RefCounted
## The names of an action's keys and buttons, for the hints and the HUD, read from InputMap (so
## a key bound later is named as it is bound).
##
## On the keyboard: the first key bound ("Enter", "Esc", "J"; the space bar as the strings say
## it). On a pad: the button as the pad's maker prints it, found from Input.get_joy_name()
## (brand_of): Xbox A B X Y, LB RB, LT RT, LS RS, View Menu; PlayStation Cross Circle Square
## Triangle, L1 R1, L2 R2, L3 R3, Share (Create on a PS5) Options; Nintendo B A Y X (the button
## at the bottom is B there), L R, ZL ZR, LS RS, - +; any other pad as an Xbox one with L3 R3 and
## Back Start. The words are strings (glyph.*), so they are translated.
##
## fill(text) puts the name of every {action} into a text: "{ui_accept}: OK · {ui_cancel}: back"
## is "Enter: OK · Esc: back" after the keyboard and "A: OK · B: back" after an Xbox pad. Two
## words stand for a group of keys: {ui_move} (the menus' arrows and WASD, or the d-pad and the
## stick) and {move} (the hero's: WASD and the arrows, or the left stick). On touch the keyboard's names are used (a text for touch says
## its own words: the _touch strings). {ui_click} and {ui_back_click} are OK and BACK, with
## "/ click" and "/ right click" after them on the keyboard.
##
## short_of() is the HUD's label over a slot: a key, a pad button, a d-pad direction drawn as a
## small d-pad with that arm lit, or a PlayStation shape drawn as such (the font has no such
## signs).

const GROUPS := {
	"ui_move": ["glyph.arrows_wasd", "glyph.dpad_stick"],
	"move": ["glyph.wasd_arrows", "glyph.left_stick"],
}
const CLICKS := {
	"ui_click": ["ui_accept", "glyph.click"],
	"ui_back_click": ["ui_cancel", "glyph.right_click"],
}
const BRANDS := ["xbox", "ps", "nintendo", "generic"]
## Each brand's names: the buttons by JOY_BUTTON_*, then "lt" / "rt" for the triggers.
const NAMES := {
	"xbox": {
		JOY_BUTTON_A: "A", JOY_BUTTON_B: "B", JOY_BUTTON_X: "X", JOY_BUTTON_Y: "Y",
		JOY_BUTTON_LEFT_SHOULDER: "LB", JOY_BUTTON_RIGHT_SHOULDER: "RB",
		JOY_BUTTON_LEFT_STICK: "LS", JOY_BUTTON_RIGHT_STICK: "RS",
		JOY_BUTTON_BACK: "View", JOY_BUTTON_START: "Menu", "lt": "LT", "rt": "RT",
	},
	"ps": {
		JOY_BUTTON_A: "glyph.ps_cross", JOY_BUTTON_B: "glyph.ps_circle",
		JOY_BUTTON_X: "glyph.ps_square", JOY_BUTTON_Y: "glyph.ps_triangle",
		JOY_BUTTON_LEFT_SHOULDER: "L1", JOY_BUTTON_RIGHT_SHOULDER: "R1",
		JOY_BUTTON_LEFT_STICK: "L3", JOY_BUTTON_RIGHT_STICK: "R3",
		JOY_BUTTON_BACK: "Share", JOY_BUTTON_START: "Options", "lt": "L2", "rt": "R2",
	},
	"nintendo": {
		JOY_BUTTON_A: "B", JOY_BUTTON_B: "A", JOY_BUTTON_X: "Y", JOY_BUTTON_Y: "X",
		JOY_BUTTON_LEFT_SHOULDER: "L", JOY_BUTTON_RIGHT_SHOULDER: "R",
		JOY_BUTTON_LEFT_STICK: "LS", JOY_BUTTON_RIGHT_STICK: "RS",
		JOY_BUTTON_BACK: "-", JOY_BUTTON_START: "+", "lt": "ZL", "rt": "ZR",
	},
	"generic": {
		JOY_BUTTON_A: "A", JOY_BUTTON_B: "B", JOY_BUTTON_X: "X", JOY_BUTTON_Y: "Y",
		JOY_BUTTON_LEFT_SHOULDER: "LB", JOY_BUTTON_RIGHT_SHOULDER: "RB",
		JOY_BUTTON_LEFT_STICK: "L3", JOY_BUTTON_RIGHT_STICK: "R3",
		JOY_BUTTON_BACK: "Back", JOY_BUTTON_START: "Start", "lt": "LT", "rt": "RT",
	},
}
## The shapes of PlayStation's face buttons, drawn on the HUD.
const PS_SHAPES := {
	JOY_BUTTON_A: "cross", JOY_BUTTON_B: "circle", JOY_BUTTON_X: "square", JOY_BUTTON_Y: "triangle",
}
const DPAD := {
	JOY_BUTTON_DPAD_UP: "glyph.dpad_up", JOY_BUTTON_DPAD_DOWN: "glyph.dpad_down",
	JOY_BUTTON_DPAD_LEFT: "glyph.dpad_left", JOY_BUTTON_DPAD_RIGHT: "glyph.dpad_right",
}
const DPAD_DIRS := {
	JOY_BUTTON_DPAD_UP: Vector2.UP, JOY_BUTTON_DPAD_DOWN: Vector2.DOWN,
	JOY_BUTTON_DPAD_LEFT: Vector2.LEFT, JOY_BUTTON_DPAD_RIGHT: Vector2.RIGHT,
}
## Keys with a shorter or a translated name than OS.get_keycode_string() gives.
const KEY_NAMES := {
	KEY_ESCAPE: "Esc", KEY_SPACE: "glyph.space", KEY_KP_ENTER: "Enter",
	KEY_UP: "glyph.up", KEY_DOWN: "glyph.down", KEY_LEFT: "glyph.left", KEY_RIGHT: "glyph.right",
	KEY_KP_MULTIPLY: "Num *", KEY_KP_DIVIDE: "Num /",
}
const TOKEN := "\\{([a-z0-9_]+)\\}"

static var _token: RegEx


## "xbox", "ps", "nintendo" or "generic" for a pad's name (Input.get_joy_name).
static func brand_of(joy_name: String) -> String:
	var n := joy_name.to_lower()
	if n.contains("xbox") or n.contains("xinput"):
		return "xbox"
	for word in ["playstation", "dualshock", "dualsense", "ps3", "ps4", "ps5", "sony"]:
		if n.contains(word):
			return "ps"
	for word in ["nintendo", "switch", "joy-con", "joycon"]:
		if n.contains(word):
			return "nintendo"
	return "generic"


## The name of the action's key (device "keys" or "touch") or pad button (device "pad"), or ""
## when nothing of that device is bound to it.
static func name_of(action: String, device: String, brand: String = "generic") -> String:
	var pad := device == "pad"
	if GROUPS.has(action):
		return _t(GROUPS[action][1 if pad else 0])
	if CLICKS.has(action):
		var n := name_of(CLICKS[action][0], device, brand)
		return n if pad or n.is_empty() else n + " / " + _t(CLICKS[action][1])
	if not InputMap.has_action(action):
		return ""
	for ev in InputMap.action_get_events(action):
		if pad and ev is InputEventJoypadButton:
			return _button(ev.button_index, brand)
		if pad and ev is InputEventJoypadMotion:
			return _axis(ev.axis, brand)
		if not pad and ev is InputEventKey:
			return key_name(ev)
	return ""


## The text with every {action} named for the device ({word} that is no action stays).
static func fill(text: String, device: String, brand: String = "generic") -> String:
	if not text.contains("{"):
		return text
	if _token == null:
		_token = RegEx.create_from_string(TOKEN)
	var out := ""
	var from := 0
	for m in _token.search_all(text):
		var name := name_of(m.get_string(1), device, brand)
		if name.is_empty():
			continue
		out += text.substr(from, m.get_start() - from) + name
		from = m.get_end()
	return out + text.substr(from)


## The HUD's label of the action: {"text": "Z"}, {"text": "RB"}, {"dpad": Vector2.UP} (a direction
## of the d-pad), {"shape": "cross"} (PlayStation); {} on touch (the slots are tapped there) or
## when the device has nothing bound to it.
static func short_of(action: String, device: String, brand: String = "generic") -> Dictionary:
	if device == "touch" or not InputMap.has_action(action):
		return {}
	for ev in InputMap.action_get_events(action):
		if device == "pad" and ev is InputEventJoypadButton:
			if DPAD_DIRS.has(ev.button_index):
				return {"dpad": DPAD_DIRS[ev.button_index]}
			if brand == "ps" and PS_SHAPES.has(ev.button_index):
				return {"shape": PS_SHAPES[ev.button_index]}
			return {"text": _button(ev.button_index, brand)}
		if device == "pad" and ev is InputEventJoypadMotion:
			return {"text": _axis(ev.axis, brand)}
		if device != "pad" and ev is InputEventKey:
			return {"text": key_name(ev)}
	return {}


## A key's name: Esc, Enter, the space bar and the arrows as the strings say them, the others
## as Godot names them (J, Tab, F1).
static func key_name(ev: InputEventKey) -> String:
	var code: Key = ev.keycode if ev.keycode != KEY_NONE else ev.physical_keycode
	if KEY_NAMES.has(code):
		return _t(KEY_NAMES[code])
	if code >= KEY_KP_0 and code <= KEY_KP_9:
		return "Num %d" % (code - KEY_KP_0)
	return OS.get_keycode_string(code)


static func _button(button: int, brand: String) -> String:
	if DPAD.has(button):
		return _t(DPAD[button])
	var names: Dictionary = NAMES.get(brand, NAMES.generic)
	return _t(names[button]) if names.has(button) else str(button)


static func _axis(axis: int, brand: String) -> String:
	var names: Dictionary = NAMES.get(brand, NAMES.generic)
	match axis:
		JOY_AXIS_TRIGGER_LEFT:
			return names.lt
		JOY_AXIS_TRIGGER_RIGHT:
			return names.rt
		JOY_AXIS_LEFT_X, JOY_AXIS_LEFT_Y:
			return _t("glyph.left_stick")
	return ""


## Translated when it is a string's key (glyph.*), as it is otherwise.
static func _t(s: String) -> String:
	return String(TranslationServer.translate(s)) if s.begins_with("glyph.") else s
