extends Control
## Список місій (Java cM[0]=2, bi() → dE=dA[], cN=dv[dk]; e.java f() малює dE[b1+cM[2]]).
## Назви місій з dA[] (v(55), 3+((dz[b]).a-1)*15). Без портретів — тільки текст.

signal mission_selected(mission_index: int)
signal back_to_lords
signal back_to_main

## Якщо -1 — перший екран: загальний список місій (до вибору лорда).
var lord_index: int = -1

var _shell: Control
var _mission_buttons: Array[Button] = []

func _ready() -> void:
	_build_ui()

func _build_ui() -> void:
	_shell = $SubmenuShell
	_shell.set_menu("Mission", [])
	var links_vbox: VBoxContainer = _shell.get_node_or_null("MainLayer/MenuFrame/LinksVBox")
	if links_vbox == null:
		return
	for c in links_vbox.get_children():
		c.queue_free()
	_mission_buttons.clear()
	GameState._init_generals_if_needed()
	var count: int
	if lord_index < 0:
		count = GameState.missions_count_in_chapter
	else:
		count = _get_mission_count_for_lord(lord_index)
	for i in range(count):
		var name_str := GameState.get_mission_name(i)
		var btn := Button.new()
		btn.theme = preload("res://theme_list_button.tres")
		btn.text = name_str
		btn.custom_minimum_size = Vector2(180, 20)  # Java f(): 180×20
		btn.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
		var available: bool = lord_index < 0 or GameState.is_mission_available(lord_index, i)
		btn.disabled = not available
		btn.pressed.connect(_on_mission_pressed.bind(i))
		links_vbox.add_child(btn)
		_mission_buttons.append(btn)
	if _shell.has_signal("back_pressed"):
		_shell.back_pressed.connect(_on_back)

func _on_back() -> void:
	if lord_index < 0:
		back_to_main.emit()
	else:
		back_to_lords.emit()

func _get_mission_count_for_lord(_lord: int) -> int:
	# Java: cN = dv[dk]; ae.z[ej+1]-ae.z[ej]
	const Z_RANGES: Array[int] = [5, 3, 6, 3, 5, 6, 7, 2, 2]
	if lord_index >= Z_RANGES.size():
		return 5
	return Z_RANGES[lord_index]

func _on_mission_pressed(mission_index: int) -> void:
	mission_selected.emit(mission_index)
