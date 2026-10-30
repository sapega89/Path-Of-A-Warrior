extends Control
## [dialog] [visiting_dialog] Базова сцена діалогу: тільки для розмов з генералом і з лордом (l.java: 210 px, 20 px між рядками). Після закриття: +5 до дружби (макс 100%).

signal closed

## Індекс генерала (0..GENERALS_COUNT-1) для оновлення relationship при закритті.
var general_index: int = 0

@onready var _btn_back: BaseButton = $Margin/VBox/BtnBack

func _ready() -> void:
	if _btn_back != null:
		_btn_back.pressed.connect(_on_back)
		_btn_back.focus_mode = Control.FOCUS_ALL

func _input(event: InputEvent) -> void:
	if event.is_action_pressed(&"menu_confirm"):
		_close()
		get_viewport().set_input_as_handled()

func _on_back() -> void:
	_close()

func _close() -> void:
	_apply_visit_reward()
	closed.emit()

func _apply_visit_reward() -> void:
	if general_index < 0 or general_index >= GameState.GENERALS_COUNT:
		return
	GameState._init_generals_if_needed()
	var rel: int = GameState.general_relationship[general_index]
	GameState.general_relationship[general_index] = mini(rel + 5, 100)
