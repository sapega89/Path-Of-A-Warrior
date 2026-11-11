class_name AskDialog
extends Control
## The game's own question (Yes / No) and notice (OK), in place of Godot's ConfirmationDialog and
## AcceptDialog, which have an English title bar ("Please Confirm..."), a close cross and the
## engine's look (scenes/ui/ask_dialog.tscn): a dim layer over the screen and a panel in the
## game's theme with the text and its buttons. While it shows, the keys and buttons go only to
## it: left / right choose, OK presses, Back (Esc, B, the right button) answers No (or closes a
## notice). The focus starts on Yes, or on No with `safe_default` (a question whose Yes loses
## something: a save, a mission), and goes back to where it was once answered.
## It is asked as the dialogs it replaces: dialog_text, popup_centered(), hide(), the confirmed
## and canceled signals.

signal confirmed
signal canceled

const SCENE := "res://scenes/ui/ask_dialog.tscn"

## A notice with OK alone ("Saving Success!"), else a question with Yes and No.
@export var notice := false
## The focus starts on No: Yes loses something.
@export var safe_default := false

var dialog_text := "":
	set(v):
		dialog_text = v
		if is_node_ready():
			label.text = v
var _focus_before: Control

@onready var panel: PanelContainer = %Panel
@onready var label: Label = %Text
@onready var ok: Button = %Ok
@onready var cancel: Button = %Cancel


func _ready() -> void:
	label.text = dialog_text
	cancel.visible = not notice
	if notice:
		ok.text = "ask.ok"
	# the focus stays on the two buttons: left / right between them, up / down nowhere
	for b: Button in [ok, cancel]:
		var other: Button = cancel if b == ok and not notice else ok
		for side in ["focus_neighbor_left", "focus_neighbor_right", "focus_next", "focus_previous"]:
			b.set(side, b.get_path_to(other))
		for side in ["focus_neighbor_top", "focus_neighbor_bottom"]:
			b.set(side, b.get_path_to(b))


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


## Shows it over everything else of its parent, the focus on Yes (on No with safe_default).
func popup_centered() -> void:
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
