extends Control
## Екран вибору складності (cM[0]==28). ae.aX = ["Hard", "Normal"], ae.aY — описи.

signal difficulty_confirmed(difficulty_index: int)
signal back_requested

const DIFFICULTIES := ["Hard", "Normal"]
const DESCRIPTIONS := [
	["Manual", "Targetting", "Gold/Exp x2"],
	["Auto ", "Targetting", "Gold/Exp x1"]
]

var _difficulty_index: int = 1

@onready var _label_opt_0: Label = $Margin/VBox/Options/Opt0/Label
@onready var _label_opt_1: Label = $Margin/VBox/Options/Opt1/Label
@onready var _desc_panel: PanelContainer = $Margin/VBox/DescPanel
@onready var _desc_label: Label = $Margin/VBox/DescPanel/DescText
@onready var _btn_confirm: Button = $Margin/VBox/BottomRow/BtnConfirm
@onready var _btn_back: Button = $Margin/VBox/BottomRow/BtnBack


func _ready() -> void:
	_difficulty_index = clampi(GameState.difficulty_index, 0, 1)
	_update_options()
	_update_description()
	_btn_confirm.pressed.connect(_on_confirm)
	_btn_back.pressed.connect(_on_back)
	_btn_confirm.grab_focus()


func _input(event: InputEvent) -> void:
	if event.is_action_pressed(&"menu_prev") or event.is_action_pressed(&"menu_next"):
		_difficulty_index = 1 - _difficulty_index
		_update_options()
		_update_description()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"ui_cancel"):
		_on_back()
		get_viewport().set_input_as_handled()


func process_menu_input(event: InputEvent) -> void:
	if event.is_action_pressed(&"menu_prev") or event.is_action_pressed(&"menu_next"):
		_difficulty_index = 1 - _difficulty_index
		_update_options()
		_update_description()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"ui_cancel"):
		_on_back()
		get_viewport().set_input_as_handled()


func _update_options() -> void:
	_label_opt_0.text = DIFFICULTIES[0]
	_label_opt_1.text = DIFFICULTIES[1]
	if _difficulty_index == 0:
		_label_opt_0.add_theme_color_override("font_color", Color(1.0, 0.55, 0.0))
		_label_opt_1.add_theme_color_override("font_color", Color(1, 1, 1))
	else:
		_label_opt_0.add_theme_color_override("font_color", Color(1, 1, 1))
		_label_opt_1.add_theme_color_override("font_color", Color(1.0, 0.55, 0.0))


func _update_description() -> void:
	var lines: Array = DESCRIPTIONS[_difficulty_index]
	_desc_label.text = "\n".join(lines)


func _on_confirm() -> void:
	GameState.difficulty_index = _difficulty_index
	difficulty_confirmed.emit(_difficulty_index)


func _on_back() -> void:
	back_requested.emit()
