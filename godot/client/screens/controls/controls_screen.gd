class_name ControlsScreen
extends BaseScreen
## Controls (Settings -> Controls): each game action the player can change, with its key and
## its pad button. Pressing one waits for the new key or button (Esc, Backspace or B: not now);
## the action that had it gets the old one in its place (KeyBindings). Reset puts back the keys
## the game came with. Each change is kept at once (Settings "controls") and bound by InputSetup,
## so the hints and the HUD name the new keys.

var bindings: KeyBindings
## Shown over another screen (Settings): what Back does instead of going back.
var close := Callable()
## The action whose new key ({"action", "pad": false}) or pad button (pad: true) is awaited.
var waiting := {}
var rows := {}  # action -> ControlsRow

@onready var list: VBoxContainer = %Rows
@onready var hint: Label = %Hint


func _ready() -> void:
	bindings = InputSetup.saved_bindings()
	for action in InputSetup.actions():
		if bindings.can_change(action):
			var row := ControlsRow.add(list, action, bindings.can_change_pad(action))
			row.asked.connect(ask.bind(action))
			rows[action] = row
	_show_names()
	(rows.values()[0] as ControlsRow).key.grab_focus()


## Waits for the action's new key, or its new pad button.
func ask(pad: bool, action: String) -> void:
	waiting = {"action": action, "pad": pad}
	hint.text = tr("controls.press_pad" if pad else "controls.press_key") % tr("controls." + action)


## While a key is awaited, the next press is it (and nothing else gets it).
func _input(event: InputEvent) -> void:
	if waiting.is_empty():
		return
	var pad := -1
	if event is InputEventKey and event.pressed and not event.echo:
		if event.physical_keycode in KeyBindings.BACK_KEYS:
			_stop()
		elif not waiting.pad:
			_bound(bindings.bind_key(waiting.action, event.physical_keycode))
	elif event is InputEventJoypadButton and event.pressed:
		if event.button_index == JOY_BUTTON_B:
			_stop()
		elif waiting.pad:
			pad = event.button_index
	elif event is InputEventJoypadMotion and waiting.pad and event.axis in KeyBindings.TRIGGERS:
		if event.axis_value < InputSetup.PAD_MOTION:
			return
		pad = KeyBindings.trigger(event.axis)
	else:
		return
	get_viewport().set_input_as_handled()
	if pad >= 0:
		_bound(bindings.bind_pad(waiting.action, pad))


## The keys the game came with.
func reset() -> void:
	bindings.reset()
	_keep()
	_stop()


func go_back() -> void:
	if not waiting.is_empty():
		_stop()
	elif close.is_valid():
		close.call()
	else:
		Router.back()


func _bound(ok: bool) -> void:
	if not ok:
		hint.text = tr("controls.kept_for_back")
		return
	_keep()
	_stop()


## Keeps the change: Settings saves it and InputSetup binds it.
func _keep() -> void:
	Settings.set_value("controls", bindings.changes())
	_show_names()


func _stop() -> void:
	waiting = {}
	hint.text = tr("controls.hint")


func _show_names() -> void:
	for action in rows:
		(rows[action] as ControlsRow).show_names(
			Glyphs.name_of(action, "keys"), Glyphs.name_of(action, "pad", InputSetup.pad_brand)
		)
