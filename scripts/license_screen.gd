extends Control
## Страница лицензии из оригинала (MANIFEST.MF, Gamevil, Thanhdaik).

signal closed

## Текст из оригинальной J2ME-игры: MANIFEST и упоминания в коде.
const LICENSE_TEXT := """Path of a Warrior

Версия: 1.4.0
MIDlet-Version: 1.4.0
MIDlet-Vendor: Thanhdaik
MIDlet-Name: Path of a Warrior

Оригинал: J2ME (MIDP-1.0, CLDC-1.0).
Порт на Godot 4.5.

GAMEVIL_SERVER: gamehub.pro
GAMEVIL_MOREGAMES: http://gamehub.pro
BUILD_ID: POW_CIN_NK_N75

© Thanhdaik. Все права защищены."""

var _shell: Control

func _ready() -> void:
	_shell = $Shell
	_shell.set_menu("Лицензия", [])
	var content: Node = _shell.get_content()
	var scroll := ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	var lbl := Label.new()
	lbl.text = LICENSE_TEXT
	lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	lbl.add_theme_font_size_override("font_size", 11)
	lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(lbl)
	content.add_child(scroll)
	var back_btn: BaseButton = _shell.get_node_or_null("MainLayer/BackBtnWrap/BackBtn")
	if back_btn != null:
		back_btn.focus_mode = Control.FOCUS_ALL
	if _shell.has_signal("closed"):
		_shell.closed.connect(_close)

func _input(event: InputEvent) -> void:
	if event.is_action_pressed(&"menu_confirm"):
		_close()
		get_viewport().set_input_as_handled()

func process_menu_input(event: InputEvent) -> void:
	if event.is_action_pressed(&"menu_confirm"):
		_close()
		get_viewport().set_input_as_handled()

func _on_back() -> void:
	_close()

func _close() -> void:
	closed.emit()
