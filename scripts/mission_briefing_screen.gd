extends Control
## Бріфінг місії (Java ag.D(): dn = dA[dm], текст з v(56) — a(arrayOfByte1, du[dk]+dm), b(..., 190, 0)).
## Тільки заголовок (назва місії) + текст, без лорда й портрета.

signal continue_pressed
signal back_pressed

var _shell: Control
var _body_label: Label

func _ready() -> void:
	_shell = $SubmenuShell
	var content = _shell.get_content()
	if content == null:
		return
	for c in content.get_children():
		c.queue_free()
	var scroll := ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	content.add_child(scroll)
	_body_label = Label.new()
	_body_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_body_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_body_label.custom_minimum_size = Vector2(190, 0)  # Java D(): b(..., 190, 0)
	scroll.add_child(_body_label)
	var btn := Button.new()
	btn.text = "Continue"
	btn.custom_minimum_size = Vector2(180, 20)
	btn.size_flags_horizontal = Control.SIZE_SHRINK_END
	btn.pressed.connect(_on_continue)
	content.add_child(btn)
	if _shell.has_signal("back_pressed"):
		_shell.back_pressed.connect(_on_back)

func set_briefing(mission_title: String, mission_text: String) -> void:
	# Java: dn = dA[dm] — заголовок; текст з v(56)
	if _shell != null:
		_shell.set_title(mission_title)
	if _body_label != null:
		_body_label.text = mission_text

func _on_continue() -> void:
	continue_pressed.emit()

func _on_back() -> void:
	back_pressed.emit()
