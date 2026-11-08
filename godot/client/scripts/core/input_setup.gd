extends Node
## Game actions and their default bindings (keyboard, gamepad).
##
## Game code reads only actions ("attack", "skill_1"), never keys, so the
## same code works with a keyboard, a gamepad and the touch buttons.
## Menus use Godot's built-in ui_* actions, with MENU_KEYS and MENU_PAD (A: OK, B: BACK) added.
## As in pyport: 1-5 (or U I O P K) the five skills, Z X C V B the five belt slots, * and #
## (the numeric keypad, RT and L3 of a pad) the two potion keys; the pad's right stick
## up / right / down / left uses the belt slots Z X C V. Tab, F or R3: auto-hunt on / off.
## Q, F1 or the pad's Back / Select: SKIP (pyport's left soft key), the talk on the map, the
## briefing and the story skipped. The numeric keypad is the phone's, as in pyport: 8 2 4 6 move,
## 5 attacks (Enter too), 1 3 7 9 0 are the five skills.
##
## Key hints, as pyport's: `device` is what the last key came from ("keys", "pad"; "touch" on a
## phone or after a touch; the mouse changes nothing), and hint(key) is the text `key` + "_" +
## device when the strings have one (Enter / Esc after the keyboard, A / B after the pad).
##
## The right mouse button is BACK (ui_cancel), as pyport's, on every screen and over any control,
## except where a node of the group RIGHT_BUTTON uses it itself (the mission's map attacks with
## it while the hero plays). The phone's own Back button is BACK too (the game does not quit on
## it: application/config/quit_on_go_back is off).

const KEYS := {
	"move_left": [KEY_A, KEY_LEFT, KEY_KP_4],
	"move_right": [KEY_D, KEY_RIGHT, KEY_KP_6],
	"move_up": [KEY_W, KEY_UP, KEY_KP_8],
	"move_down": [KEY_S, KEY_DOWN, KEY_KP_2],
	"attack": [KEY_J, KEY_SPACE, KEY_ENTER, KEY_KP_ENTER, KEY_KP_5],
	"skill_1": [KEY_1, KEY_U, KEY_KP_1],
	"skill_2": [KEY_2, KEY_I, KEY_KP_3],
	"skill_3": [KEY_3, KEY_O, KEY_KP_7],
	"skill_4": [KEY_4, KEY_P, KEY_KP_9],
	"skill_5": [KEY_5, KEY_K, KEY_KP_0],
	"potion_1": [KEY_KP_MULTIPLY],
	"potion_2": [KEY_KP_DIVIDE],
	"belt_1": [KEY_Z],
	"belt_2": [KEY_X],
	"belt_3": [KEY_C],
	"belt_4": [KEY_V],
	"belt_5": [KEY_B],
	"pause": [KEY_ESCAPE],
	"auto": [KEY_TAB, KEY_F],
	"skip": [KEY_Q, KEY_F1],
}
## The menus' own keys besides Godot's (the arrows, Enter, Space, Esc), as pyport's: WASD and the
## numeric keypad (8 2 4 6, 5 OK) move and choose, J is OK too. Backspace is BACK (see _input).
const MENU_KEYS := {
	"ui_up": [KEY_W, KEY_KP_8],
	"ui_down": [KEY_S, KEY_KP_2],
	"ui_left": [KEY_A, KEY_KP_4],
	"ui_right": [KEY_D, KEY_KP_6],
	"ui_accept": [KEY_J, KEY_KP_5],
}
## The pad in the menus: Godot's own ui_accept and ui_cancel have no pad button (A pressed no
## button, B went nowhere), and its d-pad and stick are only for the first pad (device 0).
const MENU_PAD := {
	"ui_accept": JOY_BUTTON_A,
	"ui_cancel": JOY_BUTTON_B,
	"ui_up": JOY_BUTTON_DPAD_UP,
	"ui_down": JOY_BUTTON_DPAD_DOWN,
	"ui_left": JOY_BUTTON_DPAD_LEFT,
	"ui_right": JOY_BUTTON_DPAD_RIGHT,
}
const MENU_AXES := {
	"ui_up": [JOY_AXIS_LEFT_Y, -1.0],
	"ui_down": [JOY_AXIS_LEFT_Y, 1.0],
	"ui_left": [JOY_AXIS_LEFT_X, -1.0],
	"ui_right": [JOY_AXIS_LEFT_X, 1.0],
}
## Pad bindings match every pad, not only the first one Windows or Android numbered 0 (a
## second pad, or one that came back with another number, did nothing).
const ALL_PADS := -1
const PAD_BUTTONS := {
	"move_left": JOY_BUTTON_DPAD_LEFT,
	"move_right": JOY_BUTTON_DPAD_RIGHT,
	"move_up": JOY_BUTTON_DPAD_UP,
	"move_down": JOY_BUTTON_DPAD_DOWN,
	"attack": JOY_BUTTON_A,
	"skill_1": JOY_BUTTON_X,
	"skill_2": JOY_BUTTON_Y,
	"skill_3": JOY_BUTTON_LEFT_SHOULDER,
	"skill_4": JOY_BUTTON_RIGHT_SHOULDER,
	"potion_2": JOY_BUTTON_LEFT_STICK,
	"pause": JOY_BUTTON_START,
	"auto": JOY_BUTTON_RIGHT_STICK,
	"skip": JOY_BUTTON_BACK,
}
## action: [axis, direction]
const PAD_AXES := {
	"move_left": [JOY_AXIS_LEFT_X, -1.0],
	"move_right": [JOY_AXIS_LEFT_X, 1.0],
	"move_up": [JOY_AXIS_LEFT_Y, -1.0],
	"move_down": [JOY_AXIS_LEFT_Y, 1.0],
	"skill_5": [JOY_AXIS_TRIGGER_LEFT, 1.0],
	"potion_1": [JOY_AXIS_TRIGGER_RIGHT, 1.0],
	"belt_1": [JOY_AXIS_RIGHT_Y, -1.0],
	"belt_2": [JOY_AXIS_RIGHT_X, 1.0],
	"belt_3": [JOY_AXIS_RIGHT_Y, 1.0],
	"belt_4": [JOY_AXIS_RIGHT_X, -1.0],
}
const DEADZONE := 0.3
## A stick or trigger moved this far counts as the pad being used.
const PAD_MOTION := 0.5
## Nodes that use the right mouse button themselves: uses_right_button() says when.
const RIGHT_BUTTON := "right_button"

signal device_changed(device: String)

var device := "touch" if OS.has_feature("mobile") else "keys"


func _ready() -> void:
	register()


func _input(event: InputEvent) -> void:
	var from := device_of(event)
	if not from.is_empty() and from != device:
		device = from
		device_changed.emit(device)
	if (is_back_click(event) and not right_button_taken()) or (is_back_key(event) and not typing()):
		get_viewport().set_input_as_handled()
		send_back()


func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_GO_BACK_REQUEST:
		send_back()


## A node of the group RIGHT_BUTTON uses the right button now.
func right_button_taken() -> bool:
	for n in get_tree().get_nodes_in_group(RIGHT_BUTTON):
		if n.uses_right_button():
			return true
	return false


## Backspace pressed: BACK, as pyport's (Esc is BACK through ui_cancel itself).
static func is_back_key(event: InputEvent) -> bool:
	return event is InputEventKey and event.pressed and not event.echo \
		and event.physical_keycode == KEY_BACKSPACE


## A text field has the focus: Backspace deletes there.
func typing() -> bool:
	var f := get_viewport().gui_get_focus_owner()
	return f is LineEdit or f is TextEdit


## A press of the right mouse button (not a touch).
static func is_back_click(event: InputEvent) -> bool:
	return event is InputEventMouseButton and event.pressed \
		and event.button_index == MOUSE_BUTTON_RIGHT and event.device != InputEvent.DEVICE_ID_EMULATION


## BACK: ui_cancel pressed and let go, as from Esc.
static func send_back() -> void:
	for pressed in [true, false]:
		var ev := InputEventAction.new()
		ev.action = "ui_cancel"
		ev.pressed = pressed
		Input.parse_input_event(ev)


## "keys", "pad" or "touch" for a press, "" for anything else (the mouse, a release, a stick
## at rest).
static func device_of(event: InputEvent) -> String:
	if event is InputEventKey:
		return "keys" if event.pressed and not event.echo else ""
	if event is InputEventJoypadButton:
		return "pad" if event.pressed else ""
	if event is InputEventJoypadMotion:
		return "pad" if absf(event.axis_value) >= PAD_MOTION else ""
	if event is InputEventScreenTouch:
		return "touch" if event.pressed else ""
	return ""


## The text of `key` for the device in use: `key`_pad, `key`_keys or `key`_touch when the
## strings have it, `key` itself otherwise.
func hint(key: String) -> String:
	var own := key + "_" + device
	var text := tr(own)
	return tr(key) if text == own else text


static func actions() -> Array:
	return KEYS.keys()


## Adds the actions and default bindings to InputMap. Safe to call twice.
static func register() -> void:
	for action in MENU_KEYS:
		for key in MENU_KEYS[action]:
			var mk := InputEventKey.new()
			mk.physical_keycode = key
			_add(action, mk)
	for action in MENU_PAD:
		var mb := InputEventJoypadButton.new()
		mb.button_index = MENU_PAD[action]
		_add(action, mb)
	for action in MENU_AXES:
		var ma := InputEventJoypadMotion.new()
		ma.axis = MENU_AXES[action][0]
		ma.axis_value = MENU_AXES[action][1]
		_add(action, ma)
	for action in KEYS:
		if not InputMap.has_action(action):
			InputMap.add_action(action, DEADZONE)
		for key in KEYS[action]:
			var ev := InputEventKey.new()
			ev.physical_keycode = key
			_add(action, ev)
		if PAD_BUTTONS.has(action):
			var jb := InputEventJoypadButton.new()
			jb.button_index = PAD_BUTTONS[action]
			_add(action, jb)
		if PAD_AXES.has(action):
			var jm := InputEventJoypadMotion.new()
			jm.axis = PAD_AXES[action][0]
			jm.axis_value = PAD_AXES[action][1]
			_add(action, jm)


static func _add(action: String, ev: InputEvent) -> void:
	if ev is InputEventJoypadButton or ev is InputEventJoypadMotion:
		ev.device = ALL_PADS
	if not InputMap.action_has_event(action, ev):
		InputMap.action_add_event(action, ev)
