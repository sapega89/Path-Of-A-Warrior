class_name ControlsRow
extends HBoxContainer
## A row of the Controls (controls_row.tscn): the action's name, its key and its pad button.
## Pressing one of the two asks for a new one (asked).

signal asked(pad: bool)

const SCENE := "res://screens/controls/controls_row.tscn"

@onready var key: Button = %Key
@onready var pad: Button = %Pad


## A row of `action` added to `parent`; its pad button cannot be pressed when the pad does not
## change it.
static func add(parent: Container, action: String, pad_changes: bool) -> ControlsRow:
	var row: ControlsRow = (load(SCENE) as PackedScene).instantiate()
	parent.add_child(row)
	row.name = action
	(row.get_node("%Name") as Label).text = "controls." + action
	row.pad.disabled = not pad_changes
	return row


## The names of the action's key and pad button as they are bound now.
func show_names(key_name: String, pad_name: String) -> void:
	key.text = key_name
	pad.text = pad_name


func _on_key() -> void:
	asked.emit(false)


func _on_pad() -> void:
	asked.emit(true)
