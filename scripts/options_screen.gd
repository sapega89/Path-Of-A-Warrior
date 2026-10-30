extends Control
## Екран налаштувань (Options) з титульного меню.

signal closed

var _shell: Control

func _ready() -> void:
	_shell = $Shell
	_shell.set_menu("Options", [])
	var content: Node = _shell.get_content()
	var lbl := Label.new()
	lbl.text = "Громкость и прочие настройки — скоро."
	lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	lbl.add_theme_font_size_override("font_size", 11)
	content.add_child(lbl)
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
