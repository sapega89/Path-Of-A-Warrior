extends Control
## Екран довідки (Help) з титульного меню.

signal closed

var _shell: Control

func _ready() -> void:
	_shell = $Shell
	_shell.set_menu("Help", [])
	var content: Node = _shell.get_content()
	var scroll := ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	var lbl := Label.new()
	lbl.text = "Управление: стрелки или ← → для меню. Enter или клик — выбор."
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
