extends Node
## Game actions and their default bindings (keyboard, gamepad).
##
## Game code reads only actions ("attack", "skill_1"), never keys, so the
## same code works with a keyboard, a gamepad and the touch buttons.
## Menus use Godot's built-in ui_* actions, which already cover all three.

const KEYS := {
	"move_left": [KEY_A, KEY_LEFT],
	"move_right": [KEY_D, KEY_RIGHT],
	"move_up": [KEY_W, KEY_UP],
	"move_down": [KEY_S, KEY_DOWN],
	"attack": [KEY_J, KEY_SPACE],
	"skill_1": [KEY_1, KEY_U],
	"skill_2": [KEY_2, KEY_I],
	"skill_3": [KEY_3, KEY_O],
	"skill_4": [KEY_4, KEY_P],
	"potion_1": [KEY_5, KEY_K],
	"potion_2": [KEY_6, KEY_L],
	"pause": [KEY_ESCAPE],
}
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
	"potion_1": JOY_BUTTON_LEFT_STICK,
	"potion_2": JOY_BUTTON_RIGHT_STICK,
	"pause": JOY_BUTTON_START,
}
## action: [axis, direction]
const PAD_AXES := {
	"move_left": [JOY_AXIS_LEFT_X, -1.0],
	"move_right": [JOY_AXIS_LEFT_X, 1.0],
	"move_up": [JOY_AXIS_LEFT_Y, -1.0],
	"move_down": [JOY_AXIS_LEFT_Y, 1.0],
}
const DEADZONE := 0.3


func _ready() -> void:
	register()


static func actions() -> Array:
	return KEYS.keys()


## Adds the actions and default bindings to InputMap. Safe to call twice.
static func register() -> void:
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
	if not InputMap.action_has_event(action, ev):
		InputMap.action_add_event(action, ev)
