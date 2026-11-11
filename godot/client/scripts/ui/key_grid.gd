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
const KEY_SIZE := Vector2(48, 44)
const KEY_THEME := "res://assets/art/ui/key_theme.tres"
const FONT_SIZE := 24
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
static func create(rows: Array, field: LineEdit) -> VBoxContainer:
	var g: VBoxContainer = (load("res://scripts/ui/key_grid.gd") as GDScript).new()
	g.name = "Keys"
	g.target = field
	g.alignment = BoxContainer.ALIGNMENT_CENTER
	g.add_theme_constant_override("separation", 4)
	g.theme = key_theme()
	for r in rows + [[BACK, OK]]:
		var labels: Array = []
		for c in r:
			labels.append(c)
		var row := HBoxContainer.new()
		row.alignment = BoxContainer.ALIGNMENT_CENTER
		row.add_theme_constant_override("separation", 4)
		for label: String in labels:
			row.add_child(g._key(label))
		g.add_child(row)
	return g


func _key(label: String) -> Button:
	var b := Button.new()
	b.name = "Key_" + ("Back" if label == BACK else label)
	b.text = label
	b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	var wide := label == BACK or label == OK  # two keys wide
	b.custom_minimum_size = Vector2(KEY_SIZE.x * 2 + 4 if wide else KEY_SIZE.x, KEY_SIZE.y)
	b.add_theme_font_size_override("font_size", FONT_SIZE)
	b.pressed.connect(press.bind(label))
	keys.append(b)
	return b


## The buttons of the game's theme with narrow margins, so that every key is as wide as the
## others (the rest of the theme comes from the screen around the grid).
static func key_theme() -> Theme:
	return UiTheme.theme(KEY_THEME)


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
