extends Control
## Главный экран: титул + «Press any key» → меню со стрелками.

signal start_game
signal new_game
signal exit_game
signal show_license
signal show_help
signal show_options
signal show_endings

const VIEW_W := GameState.VIEW_W
const VIEW_H := GameState.VIEW_H

const MENU_ITEMS: Array[String] = [
	"Играть", "Продолжить", "Help", "Options", "Endings", "Лицензия", "Выход"
]

var _show_menu := false

@onready var _press_any_key: TextureRect = $PressAnyKey
@onready var _menu_frame: Control = $MenuFrame
@onready var _menu_row: Control = $MenuFrame/VBox/MenuRow

func _ready() -> void:
	if _menu_row.has_method("setup_menu_items"):
		_menu_row.setup_menu_items(MENU_ITEMS)
	if _menu_row.has_signal("item_selected"):
		_menu_row.item_selected.connect(_on_item_selected)
	# Сначала показываем «Press any key», рамка меню скрыта
	_show_menu = false
	_press_any_key.visible = true
	_menu_frame.visible = false

func _input(event: InputEvent) -> void:
	if not _show_menu:
		if _is_any_press(event):
			_go_to_menu()
			get_viewport().set_input_as_handled()
		return
	_handle_menu_input(event)

func process_menu_input(event: InputEvent) -> void:
	if not _show_menu:
		if _is_any_press(event):
			_go_to_menu()
			get_viewport().set_input_as_handled()
		return
	_handle_menu_input(event)

func _is_any_press(event: InputEvent) -> bool:
	return (event is InputEventKey and event.pressed) \
		or (event is InputEventMouseButton and event.pressed) \
		or (event is InputEventScreenTouch and event.pressed) \
		or (event is InputEventJoypadButton and event.pressed)

func _go_to_menu() -> void:
	_show_menu = true
	_press_any_key.visible = false
	_menu_frame.visible = true
	# Фокус на кнопку рядка — показує box_01 (стиль кнопок)
	var btn := _menu_row.get_node_or_null("Row/BtnSelect")
	if btn is Control:
		btn.grab_focus()

func _handle_menu_input(event: InputEvent) -> void:
	if _menu_row != null and _menu_row.has_method("process_menu_input"):
		_menu_row.process_menu_input(event)

func _on_item_selected(index: int) -> void:
	match index:
		0:
			new_game.emit()
		1:
			start_game.emit()
		2:
			show_help.emit()
		3:
			show_options.emit()
		4:
			show_endings.emit()
		5:
			show_license.emit()
		6:
			exit_game.emit()
