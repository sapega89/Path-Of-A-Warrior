extends Control
## [visiting] Екран Visiting: одразу таблиця, заголовок «Select». Показуються лише генерали, які вже запросили гравця (GameState.general_invited).

signal closed
signal general_selected(general_index: int)

## Індекси генералів, що відображаються (тільки запрошені)
var _visible_general_indices: Array[int] = []

var _shell: Control
var _table: VBoxContainer
var _scroll: ScrollContainer
var _selected_index: int = 0
var _row_nodes: Array[HBoxContainer] = []
var _row_buttons: Array[Button] = []
var _row_relationship_labels: Array[Label] = []

func _ready() -> void:
	_build_visible_list()
	_shell = $SubmenuShell
	_shell.set_menu("Select", [])

	var table_node = _shell.get_node_or_null("MainLayer/MenuFrame/LinksVBox/GeneralsTable")
	_table = table_node as VBoxContainer
	if _table == null:
		return

	_scroll = _table.get_parent() as ScrollContainer
	if _scroll == null:
		var parent = _table.get_parent()
		var idx = _table.get_index()
		parent.remove_child(_table)
		_scroll = ScrollContainer.new()
		_scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
		_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
		parent.add_child(_scroll)
		parent.move_child(_scroll, idx)
		_scroll.add_child(_table)

	var row_template = _table.get_node_or_null("Row0")
	if row_template == null:
		return

	for child in _table.get_children():
		if child.name != "HeaderRow" and child.name != "Row0":
			child.queue_free()

	for row_i in range(_visible_general_indices.size()):
		var general_index: int = _visible_general_indices[row_i]
		var row: HBoxContainer
		if row_i == 0:
			row = row_template
		else:
			row = row_template.duplicate()
			_table.add_child(row)

		row.name = "Row" + str(row_i)
		_row_nodes.append(row)

		var btn := row.get_node_or_null("NameCell/Button") as Button
		var rel := row.get_node_or_null("RelCell/RelationshipLabel") as Label

		var name_cell = row.get_node_or_null("NameCell")
		var icon = name_cell.get_node_or_null("Icon") as TextureRect if name_cell else null
		if name_cell != null and icon == null:
			icon = TextureRect.new()
			icon.name = "Icon"
			icon.custom_minimum_size = Vector2(24, 24)
			icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
			icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
			name_cell.add_child(icon)
			name_cell.move_child(icon, 0)
		if icon != null:
			var icon_tex = load("res://jang_%d.png" % (general_index + 1))
			if icon_tex:
				icon.texture = icon_tex

		_row_buttons.append(btn)
		_row_relationship_labels.append(rel)

		if btn != null:
			btn.text = GameState.general_names[general_index]
		if rel != null:
			rel.text = str(GameState.general_relationship[general_index])

	_update_selection()

	if _shell.has_signal("back_pressed"):
		_shell.back_pressed.connect(_on_back)
	var back_btn: BaseButton = _shell.get_node_or_null("MainLayer/BackBtnWrap/BackBtn")
	if back_btn != null:
		back_btn.focus_mode = Control.FOCUS_ALL

func _build_visible_list() -> void:
	_visible_general_indices.clear()
	GameState._init_generals_if_needed()
	for i in range(GameState.GENERALS_COUNT):
		if GameState.general_invited[i]:
			_visible_general_indices.append(i)

func _update_selection() -> void:
	for i in range(_row_nodes.size()):
		var row := _row_nodes[i]
		var btn := _row_buttons[i]
		var rel := _row_relationship_labels[i]
		
		if btn != null:
			if i == _selected_index:
				btn.add_theme_color_override("font_color", Color(1, 0.55, 0, 1))
				# Скролимо до вибраного елемента
				if _scroll:
					_scroll.ensure_control_visible(row)
			else:
				btn.add_theme_color_override("font_color", Color(1, 1, 1, 1))
				
		if rel != null:
			if i == _selected_index:
				rel.add_theme_color_override("font_color", Color(1, 0.55, 0, 1))
			else:
				rel.add_theme_color_override("font_color", Color(1, 1, 1, 1))

func _get_current_general_index() -> int:
	if _selected_index < 0 or _selected_index >= _visible_general_indices.size():
		return 0
	return _visible_general_indices[_selected_index]

func _input(event: InputEvent) -> void:
	if event.is_action_pressed(&"menu_confirm"):
		general_selected.emit(_get_current_general_index())
		get_viewport().set_input_as_handled()
		return

	if event.is_action_pressed(&"ui_down") or event.is_action_pressed(&"menu_next"):
		if _selected_index < _row_nodes.size() - 1:
			_selected_index += 1
			_update_selection()
			get_viewport().set_input_as_handled()

	if event.is_action_pressed(&"ui_up") or event.is_action_pressed(&"menu_prev"):
		if _selected_index > 0:
			_selected_index -= 1
			_update_selection()
			get_viewport().set_input_as_handled()

func _on_back() -> void:
	closed.emit()
