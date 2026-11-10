class_name VisitRow
extends Button
## A row of the visiting list (visit_row.tscn): a general's name on the left, his friendship
## points on the right.

const SCENE := "res://screens/visiting/visit_row.tscn"

@onready var _name: Label = $Name
@onready var _points: Label = $Points


## A row added to `parent`: a general's name (a translation key) and his points.
static func add(parent: Container, general_name: String, points: String) -> VisitRow:
	var row: VisitRow = (load(SCENE) as PackedScene).instantiate()
	parent.add_child(row)
	row.show_general(general_name, points)
	return row


func show_general(general_name: String, points: String) -> void:
	_name.text = general_name
	_points.text = points
