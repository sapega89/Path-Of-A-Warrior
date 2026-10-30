extends Control
## Екран введення імені (ag.bz). Мінімум 4 символи (as.java 1309). cz.k = player_name.

signal name_confirmed(player_name: String)
signal back_requested

const MIN_NAME_LENGTH := 4

@onready var _shell: Control = $SubmenuShell
@onready var _line_edit: LineEdit = $SubmenuShell/MainLayer/MenuFrame/LinksVBox/LineEdit
@onready var _hint: Label = $SubmenuShell/MainLayer/MenuFrame/LinksVBox/Hint
@onready var _btn_confirm: Button = $SubmenuShell/MainLayer/MenuFrame/LinksVBox/BtnConfirm


func _ready() -> void:
	_shell.set_title("NAME")
	_shell.back_pressed.connect(func() -> void: back_requested.emit())
	_line_edit.text = GameState.player_name
	_line_edit.placeholder_text = "Enter name (min %d chars)" % MIN_NAME_LENGTH
	_update_hint()
	_line_edit.text_changed.connect(_on_text_changed)
	_btn_confirm.pressed.connect(_on_confirm)
	_line_edit.grab_focus()


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
