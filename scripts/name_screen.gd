extends Control
## Екран введення імені (ag.bz). Мінімум 4 символи (as.java 1309). cz.k = player_name.

signal name_confirmed(player_name: String)
signal back_requested

const MIN_NAME_LENGTH := 4

@onready var _line_edit: LineEdit = $Margin/VBox/Center/LineEdit
@onready var _hint: Label = $Margin/VBox/Hint
@onready var _btn_confirm: Button = $Margin/VBox/BottomRow/BtnConfirm
@onready var _btn_back: Button = $Margin/VBox/BottomRow/BtnBack


func _ready() -> void:
	_line_edit.text = GameState.player_name
	_line_edit.placeholder_text = "Enter name (min %d chars)" % MIN_NAME_LENGTH
	_update_hint()
	_line_edit.text_changed.connect(_on_text_changed)
	_btn_confirm.pressed.connect(_on_confirm)
	_btn_back.pressed.connect(_on_back)
	_line_edit.grab_focus()


func _input(event: InputEvent) -> void:
	if event.is_action_pressed(&"ui_cancel"):
		_on_back()
		get_viewport().set_input_as_handled()


func process_menu_input(event: InputEvent) -> void:
	if event.is_action_pressed(&"ui_cancel"):
		_on_back()
		get_viewport().set_input_as_handled()


func _on_text_changed(_new_text: String) -> void:
	_update_hint()


func _update_hint() -> void:
	var len: int = _line_edit.text.length()
	if len > 0 and len < MIN_NAME_LENGTH:
		_hint.text = "Minimum %d characters." % MIN_NAME_LENGTH
		_hint.add_theme_color_override("font_color", Color(1.0, 0.6, 0.4))
	else:
		_hint.text = ""


func _on_confirm() -> void:
	var name_str: String = _line_edit.text.strip_edges()
	if name_str.length() < MIN_NAME_LENGTH:
		_hint.text = "Minimum %d characters." % MIN_NAME_LENGTH
		_hint.add_theme_color_override("font_color", Color(1.0, 0.6, 0.4))
		return
	GameState.player_name = name_str
	name_confirmed.emit(name_str)


func _on_back() -> void:
	back_requested.emit()
