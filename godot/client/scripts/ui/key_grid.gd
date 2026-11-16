class_name KeyGrid
extends VBoxContainer
## An on-screen keyboard, so that a gamepad (or touch, or the mouse) can type too: rows of keys
## that type into a text field. The keys are buttons, so the d-pad moves between them and A (or
## a click) types one; BACK deletes the last character, OK does what Enter does in the field.
## Typing goes through the field's text_changed, so the screen's own filter still holds.
## With several fields the keys type into the one that had the focus last (follow()).
## The keys show only while the gamepad is in use (InputSetup.device "pad"): a PC has its
## keyboard and a phone its own on-screen one when the field is tapped.

const BACK := "⌫"
const OK := "OK"
const KEY_GAP := 4  # between the keys and the rows (key_theme.tres)
## The game's buttons with narrow margins, so that every key is as wide as the others, their
## letters' size and the gaps (the rest of the theme comes from the screen around the grid).
const KEY_THEME := "res://assets/art/ui/key_theme.tres"
const SCENE := "res://scenes/ui/key_grid.tscn"
const ROW_SCENE := preload("res://scenes/ui/key_row.tscn")
const KEY_SCENE := preload("res://scenes/ui/key_button.tscn")
## The hero's name: letters in both cases.
const LETTERS := ["ABCDEFGHIJKLM", "NOPQRSTUVWXYZ", "abcdefghijklm", "nopqrstuvwxyz"]

var target: LineEdit
var keys: Array[Button] = []


func _ready() -> void:
	var setup := get_node_or_null("/root/InputSetup")
	if setup == null:
		return
	shown_for(setup.device)
	setup.device_changed.connect(shown_for)


## Shown for the gamepad only; a key that had the focus gives it back to the field.
func shown_for(device: String) -> void:
	var on := device == "pad"
	if visible == on:
		return
	var had_focus := false
	for b in keys:
		had_focus = had_focus or b.has_focus()
	visible = on
	if had_focus and target != null and target.is_inside_tree():
		target.grab_focus()


## A keyboard of these rows (each a string of keys) and a last row of BACK and OK, typing
## into `field`.
static func create(rows: Array, field: LineEdit) -> KeyGrid:
	var g: KeyGrid = (load(SCENE) as PackedScene).instantiate()
	g.target = field
	for r in rows + [[BACK, OK]]:
		var row: HBoxContainer = ROW_SCENE.instantiate()
		for c in r:
			row.add_child(g._key(c))
		g.add_child(row)
	return g


func _key(label: String) -> Button:
	var b: Button = KEY_SCENE.instantiate()
	b.name = "Key_" + ("Back" if label == BACK else label)
	b.text = label
	if label == BACK or label == OK:  # two keys wide
		b.custom_minimum_size.x = b.custom_minimum_size.x * 2 + KEY_GAP
	b.pressed.connect(press.bind(label))
	keys.append(b)
	return b


## The keys type into `field` once it has had the focus.
func follow(field: LineEdit) -> void:
	field.focus_entered.connect(func() -> void: target = field)


## A key pressed: types its character, deletes one (BACK) or submits the field (OK).
func press(label: String) -> void:
	if target == null:
		return
	target.caret_column = target.text.length()
	if label == OK:
		target.text_submitted.emit(target.text)
		return
	var was := target.text
	if label == BACK:
		if not was.is_empty():
			target.delete_text(was.length() - 1, was.length())
	else:
		target.insert_text_at_caret(label)  # not past max_length
	if target.text != was:
		target.text_changed.emit(target.text)  # as typing does: the screen's filter


## The key with this label, null when there is none.
func key(label: String) -> Button:
	for b in keys:
		if b.text == label:
			return b
	return null
