class_name AskDialog
extends Control
## The game's own question (Yes / No) and notice (OK), in place of Godot's ConfirmationDialog and
## AcceptDialog, which have an English title bar ("Please Confirm..."), a close cross and the
## engine's look: a dim layer over the screen and a panel in the game's theme with the text and
## its buttons. While it shows, the keys and buttons go only to it: left / right choose, OK
## presses, Back (Esc, B, the right button) answers No (or closes a notice). The focus starts on
## Yes, or on No with `safe_default` (a question whose Yes loses something: a save, a mission),
## and goes back to where it was once answered.
## It is asked as the dialogs it replaces: dialog_text, ok_button_text, cancel_button_text,
## popup_centered(), hide(), the confirmed and canceled signals, get_ok_button(),
## get_cancel_button().

signal confirmed
signal canceled

const WIDTH := 620
const BUTTON_WIDTH := 200

var dialog_text := "":
	set(v):
		dialog_text = v
		label.text = v
var ok_button_text := "ask.yes":
	set(v):
		ok_button_text = v
		ok.text = v
var cancel_button_text := "ask.no":
	set(v):
		cancel_button_text = v
		cancel.text = v
var safe_default := false
var notice := false  # OK alone
var panel: PanelContainer
var label: Label
var ok: Button
var cancel: Button
var _focus_before: Control


## notice: a notice with OK alone ("Saving Success!"), else a question with Yes and No.
func _init(is_notice := false) -> void:
	notice = is_notice
	name = "Ask"
	visible = false
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP  # nothing under it is clicked
	var dim := ColorRect.new()
	dim.name = "Dim"
	dim.color = Color(0, 0, 0, 0.6)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	dim.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(dim)
	var center := CenterContainer.new()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)
	panel = PanelContainer.new()
	panel.name = "Panel"
	var sb := UiTheme.PanelBox.new()  # the dialogs' leather with its seam and rivets
	sb.set_content_margin_all(28)
	panel.add_theme_stylebox_override("panel", sb)
	panel.custom_minimum_size = Vector2(WIDTH, 0)
	center.add_child(panel)
	var col := VBoxContainer.new()
	col.add_theme_constant_override("separation", 28)
	panel.add_child(col)
	label = Label.new()
	label.name = "Text"
	label.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED  # the caller translates it
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.custom_minimum_size = Vector2(WIDTH - 56, 0)
	col.add_child(label)
	var row := HBoxContainer.new()
	row.name = "Buttons"
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	row.add_theme_constant_override("separation", 24)
	col.add_child(row)
	ok = _button(row, "Ok", "ask.ok" if notice else "ask.yes", _answer.bind(true))
	cancel = _button(row, "Cancel", "ask.no", _answer.bind(false))
	cancel.visible = not notice
	if notice:
		ok_button_text = "ask.ok"
	# the focus stays on the two buttons: left / right between them, up / down nowhere
	for b in [ok, cancel]:
		var other: Button = cancel if b == ok and not notice else ok
		for side in ["focus_neighbor_left", "focus_neighbor_right", "focus_next", "focus_previous"]:
			b.set(side, b.get_path_to(other))
		for side in ["focus_neighbor_top", "focus_neighbor_bottom"]:
			b.set(side, b.get_path_to(b))


func _button(row: HBoxContainer, node_name: String, text: String, on_press: Callable) -> Button:
	var b := Button.new()
	b.name = node_name
	b.text = text
	b.custom_minimum_size = Vector2(BUTTON_WIDTH, 0)
	b.pressed.connect(on_press)
	row.add_child(b)
	return b


func get_ok_button() -> Button:
	return ok


func get_cancel_button() -> Button:
	return cancel


## Shows it over everything else of its parent, the focus on Yes (on No with safe_default).
func popup_centered(_size := Vector2i.ZERO) -> void:
	if is_inside_tree():
		_focus_before = get_viewport().gui_get_focus_owner()
		move_to_front()
	show()
	_focus_first()
	_focus_first.call_deferred()  # again, over a focus the screen asked for later in this frame


## The focus on its first button, unless it is on one of its buttons already or it is hidden.
func _focus_first() -> void:
	var first := cancel if safe_default and not notice else ok
	if not visible or not first.is_inside_tree():
		return
	var f := get_viewport().gui_get_focus_owner()
	if f != ok and f != cancel:
		first.grab_focus()


func _answer(yes: bool) -> void:
	hide()
	if (
		is_instance_valid(_focus_before)
		and _focus_before.is_inside_tree()
		and _focus_before.is_visible_in_tree()
	):
		_focus_before.grab_focus()
	_focus_before = null
	if yes:
		confirmed.emit()
	else:
		canceled.emit()


## Back answers No; before the screen under it sees the key.
func _input(event: InputEvent) -> void:
	if visible and event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		_answer(false)


## The keys and buttons its own buttons did not take go nowhere else while it shows.
func _unhandled_input(event: InputEvent) -> void:
	if (
		visible
		and (
			event is InputEventKey
			or event is InputEventJoypadButton
			or event is InputEventJoypadMotion
			or event is InputEventAction
		)
	):
		get_viewport().set_input_as_handled()
