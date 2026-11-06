extends Control
## On-screen controls for phones: a floating stick on the left half and action
## buttons on the right. They press the same actions as keys and gamepads, so
## game code does not know which device is used. Shown only on touch screens.
## A button sends its action as an input event (press_action), as a key does: the screens that
## wait for the event (PAUSE) get it, and the action is held for the ones that poll it.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const STICK_RADIUS := 90.0
const BUTTON_RADIUS := 52.0
## action -> centre, measured from the bottom-right corner
const BUTTONS := {
	"attack": Vector2(-150, -150),
	"skill_1": Vector2(-290, -110),
	"skill_2": Vector2(-250, -250),
	"skill_3": Vector2(-120, -290),
	"pause": Vector2(-70, -650),
}
const MOVE_ACTIONS := {
	"move_left": Vector2.LEFT, "move_right": Vector2.RIGHT,
	"move_up": Vector2.UP, "move_down": Vector2.DOWN,
}

## Show even without a touch screen (for tests and screenshots).
var force_visible := false
var stick_vector := Vector2.ZERO
var _stick_finger := -1
var _stick_origin := Vector2.ZERO
var _stick_pos := Vector2.ZERO
var _button_fingers := {}  # finger index -> action


func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	visible = force_visible or DisplayServer.is_touchscreen_available()


## Stick offset to a move vector of length 0..1.
static func stick_value(origin: Vector2, pos: Vector2, radius: float = STICK_RADIUS) -> Vector2:
	var d := (pos - origin) / radius
	return d.limit_length(1.0)


## Presses the move_* actions with the right strength for a stick vector.
static func apply_move(v: Vector2) -> void:
	for action in MOVE_ACTIONS:
		var strength := maxf(v.dot(MOVE_ACTIONS[action]), 0.0)
		if strength > 0.05:
			Input.action_press(action, strength)
		else:
			Input.action_release(action)


func button_center(action: String) -> Vector2:
	return size + BUTTONS[action]


func button_at(pos: Vector2) -> String:
	for action in BUTTONS:
		if pos.distance_to(button_center(action)) <= BUTTON_RADIUS:
			return action
	return ""


func _input(event: InputEvent) -> void:
	if not visible:
		return
	if event is InputEventScreenTouch:
		_touch(event.index, event.position, event.pressed)
	elif event is InputEventScreenDrag and event.index == _stick_finger:
		_stick_pos = event.position
		stick_vector = stick_value(_stick_origin, _stick_pos)
		apply_move(stick_vector)
		queue_redraw()


func _touch(finger: int, pos: Vector2, pressed: bool) -> void:
	if pressed:
		var action := button_at(pos)
		if action != "":
			_button_fingers[finger] = action
			press_action(action, true)
		elif pos.x < size.x / 2.0 and _stick_finger < 0:
			_stick_finger = finger
			_stick_origin = pos
			_stick_pos = pos
	else:
		if _button_fingers.has(finger):
			press_action(_button_fingers[finger], false)
			_button_fingers.erase(finger)
		elif finger == _stick_finger:
			_stick_finger = -1
			stick_vector = Vector2.ZERO
			apply_move(stick_vector)
	queue_redraw()


## An action pressed or let go as an input event, as from a key.
static func press_action(action: String, pressed: bool) -> void:
	var ev := InputEventAction.new()
	ev.action = action
	ev.pressed = pressed
	Input.parse_input_event(ev)


func _exit_tree() -> void:
	apply_move(Vector2.ZERO)
	for finger in _button_fingers:
		Input.action_release(_button_fingers[finger])
	_button_fingers.clear()


func _draw() -> void:
	var dim := Color(UiTheme.TEXT, 0.25)
	var lit := Color(UiTheme.ACCENT, 0.6)
	if _stick_finger >= 0:
		draw_circle(_stick_origin, STICK_RADIUS, dim)
		draw_circle(_stick_origin + stick_vector * STICK_RADIUS, 36.0, lit)
	var held := _button_fingers.values()
	for action in BUTTONS:
		var r := BUTTON_RADIUS * (0.6 if action == "pause" else 1.0)
		draw_circle(button_center(action), r, lit if action in held else dim)
