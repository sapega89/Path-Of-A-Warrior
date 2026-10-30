extends Control
## [title] Титульний екран: порядок і кількість пунктів з M_text.png (індекси 0–8).

signal start_game
signal new_game
signal exit_game
signal show_license
signal show_help
signal show_options
signal show_endings
signal show_about
signal show_more_games
signal show_multiplayer

const VIEW_W := GameState.VIEW_W
const VIEW_H := GameState.VIEW_H

## Джерело правди: M_text.png — 9 пунктів у порядку рядків.
const MENU_ITEMS: Array[String] = [
	"Continue", "New Game", "Options", "Help", "Endings", "About", "More Games", "Multiplayer", "Exit"
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

func _handle_menu_input(event: InputEvent) -> void:
	if _menu_row != null and _menu_row.has_method("process_menu_input"):
		_menu_row.process_menu_input(event)

func _on_item_selected(index: int) -> void:
	match index:
		0:
			start_game.emit()
		1:
			new_game.emit()
		2:
			show_options.emit()
		3:
			show_help.emit()
		4:
			show_endings.emit()
		5:
			show_about.emit()
		6:
			show_more_games.emit()
		7:
			show_multiplayer.emit()
		8:
			exit_game.emit()
