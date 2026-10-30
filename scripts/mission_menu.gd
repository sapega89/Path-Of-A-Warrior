extends Control
## [mission] Підменю Mission: сітка місій 4×2, без Active Quests/Completed. Після вибору місії — вибір генерала/лорда в game_menu.

signal mission_selected(mission_index: int)

const MISSION_GRID_SCENE := preload("res://scenes/menus/mission_grid.tscn")

var _shell: Control

func _ready() -> void:
	_shell = $SubmenuShell
	_shell.set_menu("Mission", [])

	var links_vbox: VBoxContainer = _shell.get_node_or_null("MainLayer/MenuFrame/LinksVBox")
	if links_vbox == null:
		return
	for child in links_vbox.get_children():
		child.queue_free()

	var grid: GridContainer = MISSION_GRID_SCENE.instantiate()
	links_vbox.add_child(grid)

	var idx := 0
	for child in grid.get_children():
		if child is BaseButton:
			child.pressed.connect(_on_cell_pressed.bind(idx))
			idx += 1

	if _shell.has_signal("back_pressed"):
		_shell.back_pressed.connect(_on_back)

func _on_cell_pressed(mission_index: int) -> void:
	mission_selected.emit(mission_index)

func _on_back() -> void:
	pass
