extends Control
## Екран концовок (Endings): зараз усі заблоковані, дані можна заповнити з edat/gamestr.

signal closed

var _shell: Control

func _ready() -> void:
	_shell = $Shell
	_shell.set_menu("Endings", [])
	var content: Node = _shell.get_content()
	var scroll := ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	var vbox := VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 6)
	vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	for i in range(1, 4):
		var lbl := Label.new()
		lbl.text = str(i) + ". ??? (заблокировано)"
		lbl.add_theme_font_size_override("font_size", 11)
		lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		vbox.add_child(lbl)
	scroll.add_child(vbox)
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
