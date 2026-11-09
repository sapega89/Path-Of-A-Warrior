class_name GridSides
extends HBoxContainer
## The two buttons that switch Live's grids between the backpack and the Warehouse
## (scenes/ui/grid_sides.tscn), the backpack chosen first.

## The Warehouse (true) or the backpack (false) was picked.
signal chosen(warehouse: bool)

const SCENE := "res://scenes/ui/grid_sides.tscn"


## The two buttons: the backpack's and the Warehouse's.
func tabs() -> Array[Button]:
	return [$Backpack, $Warehouse]


func _on_backpack() -> void:
	chosen.emit(false)


func _on_warehouse() -> void:
	chosen.emit(true)
