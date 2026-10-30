extends Control
## Єдиний шаблон екрану: рамка, заголовок, слот контенту (список посилань або довільний вміст), BACK.
## Режим посилань: set_menu(title, links). Режим контенту: set_menu(title, []), потім set_content_message() або get_content().add_child().
## [submenu_shell] [elem_list_btn] [elem_back_btn]

signal link_selected(action_id: int)
signal back_pressed
signal closed

const THEME_LIST_BUTTON := preload("res://theme_list_button.tres")
const THEME_LIST_BUTTON_SELECTED := preload("res://theme_list_button_selected.tres")

## Заголовок екрану (аналог as.hw[as.gP])
@export var menu_title: String = ""

## Список посилань: кожен елемент — Dictionary з ключами "label" (String) та "action_id" (int)
var links: Array[Dictionary] = []

## Індекс обраного пункту: обраний = біла рамка + червоний текст, необраний = сіра рамка + білий текст
var _selected_link_index: int = 0

@onready var _title_label: Label = $MainLayer/TitleBox/TitleLabel
@onready var _links_vbox: VBoxContainer = $MainLayer/MenuFrame/LinksVBox
@onready var _back_btn: BaseButton = $MainLayer/BackBtnWrap/BackBtn

var _link_buttons: Array[Button] = []

func _ready() -> void:
	if _back_btn != null:
		_back_btn.pressed.connect(_on_back_pressed)
	_update_ui()

func get_links_container() -> VBoxContainer:
	return _links_vbox

## Слот для довільного вмісту (той самий контейнер, що й для посилань). Для екранів типу License/Help.
func get_content() -> Node:
	return _links_vbox

func set_title(t: String) -> void:
	menu_title = t
	if _title_label != null:
		_title_label.text = t

func set_display_title(t: String) -> void:
	set_title(t)

## Режим контенту: один рядок тексту в слоті (очищає слот, додає Label).
func set_content_message(msg: String) -> void:
	if _links_vbox == null:
		return
	for c in _links_vbox.get_children():
		c.queue_free()
	var label := Label.new()
	label.text = msg
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_links_vbox.add_child(label)

func set_menu(title: String, link_list: Array) -> void:
	menu_title = title
	links.clear()
	for item in link_list:
		if item is Dictionary:
			links.append(item)
		elif item is String:
			links.append({"label": item, "action_id": links.size()})
	_update_ui()

func _update_ui() -> void:
	if _title_label != null:
		_title_label.text = menu_title
	_repopulate_links()
	_update_selection()

func _repopulate_links() -> void:
	# Clear existing if needed or reuse
	for btn in _link_buttons:
		btn.queue_free()
	_link_buttons.clear()
	
	if _links_vbox == null:
		return
		
	for i in range(links.size()):
		var link: Dictionary = links[i]
		var btn := Button.new()
		btn.theme = THEME_LIST_BUTTON
		btn.text = link.get("label", "")
		btn.set_meta("action_id", link.get("action_id", i))
		btn.custom_minimum_size = Vector2(200, 22)
		btn.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
		btn.pressed.connect(_on_link_btn_pressed.bind(i))
		_links_vbox.add_child(btn)
		_link_buttons.append(btn)

func _update_selection() -> void:
	for i in range(_link_buttons.size()):
		var btn: Button = _link_buttons[i]
		if i == _selected_link_index:
			btn.add_theme_color_override("font_color", Color(0.9, 0.15, 0.15, 1))
			var sel_style = THEME_LIST_BUTTON_SELECTED.get_stylebox("normal", "Button")
			if sel_style != null:
				btn.add_theme_stylebox_override("normal", sel_style)
		else:
			btn.remove_theme_color_override("font_color")
			btn.remove_theme_stylebox_override("normal")

func _on_link_btn_pressed(button_index: int) -> void:
	_selected_link_index = button_index
	_update_selection()
	var btn: Button = _link_buttons[button_index]
	link_selected.emit(btn.get_meta("action_id"))

func _on_back_pressed() -> void:
	back_pressed.emit()
	closed.emit()

func _input(event: InputEvent) -> void:
	if not visible: return
	if event.is_action_pressed(&"ui_cancel"):
		_on_back_pressed()
		get_viewport().set_input_as_handled()
		return
	if _link_buttons.is_empty(): return

	if event.is_action_pressed(&"ui_down") or event.is_action_pressed(&"menu_next"):
		_selected_link_index = (_selected_link_index + 1) % _link_buttons.size()
		_update_selection()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"ui_up") or event.is_action_pressed(&"menu_prev"):
		_selected_link_index = (_selected_link_index - 1 + _link_buttons.size()) % _link_buttons.size()
		_update_selection()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"menu_confirm"):
		_on_link_btn_pressed(_selected_link_index)
		get_viewport().set_input_as_handled()
