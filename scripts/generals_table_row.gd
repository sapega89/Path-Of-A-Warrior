extends HBoxContainer
## Один рядок таблиці генералів: дві ячейки з бордерами (ім'я, рівень відносин).

@onready var _name_cell: PanelContainer = $NameCell
@onready var _btn: Button = $NameCell/Button
@onready var _rel_label: Label = $RelCell/RelationshipLabel

func set_data(name_text: String, relationship: int) -> void:
	if _btn != null:
		_btn.text = name_text
	if _rel_label != null:
		_rel_label.text = str(relationship)

func set_icon_texture(tex: Texture2D) -> void:
	if _name_cell == null:
		return
	var icon: TextureRect = _name_cell.get_node_or_null("Icon") as TextureRect
	if icon == null:
		icon = TextureRect.new()
		icon.name = "Icon"
		icon.custom_minimum_size = Vector2(24, 24)
		icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		_name_cell.add_child(icon)
		_name_cell.move_child(icon, 0)
	icon.texture = tex

func set_selected(selected: bool) -> void:
	var color := Color(1, 0.55, 0, 1) if selected else Color(1, 1, 1, 1)
	if _btn != null:
		_btn.add_theme_color_override("font_color", color)
	if _rel_label != null:
		_rel_label.add_theme_color_override("font_color", color)
