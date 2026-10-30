extends Control
## Діалог з лордом (Java ag.z(): str1 = dC.a/dA[dm]/B(); "[str1] " + текст з v(57+dG); b(..., 150, s)).
## Лорд: ag.dl = dt[dk] (bi()). Портрет — bB: jang_1..jang_37 для аватар (imgchar.scr).

signal continue_pressed
signal back_pressed

var _shell: Control
var _portrait: TextureRect
var _name_label: Label
var _body_label: Label

func _ready() -> void:
	_shell = $SubmenuShell
	_shell.set_title("")
	var content = _shell.get_content()
	if content == null:
		return
	for c in content.get_children():
		c.queue_free()
	var hbox := HBoxContainer.new()
	hbox.size_flags_vertical = Control.SIZE_EXPAND_FILL
	hbox.add_theme_constant_override("separation", 16)
	content.add_child(hbox)
	_portrait = TextureRect.new()
	_portrait.custom_minimum_size = Vector2(46, 46)  # Java: великі портрети ju_* 46×46; для лордів jang_*
	_portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	hbox.add_child(_portrait)
	var vbox := VBoxContainer.new()
	vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	vbox.size_flags_vertical = Control.SIZE_EXPAND_FILL
	vbox.add_theme_constant_override("separation", 8)
	hbox.add_child(vbox)
	_name_label = Label.new()
	_name_label.add_theme_font_size_override("font_size", 14)
	vbox.add_child(_name_label)
	var scroll := ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	vbox.add_child(scroll)
	_body_label = Label.new()
	_body_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_body_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_body_label.custom_minimum_size = Vector2(150, 0)  # Java z(): b(..., 150, s)
	scroll.add_child(_body_label)
	var btn := Button.new()
	btn.text = "Continue"
	btn.custom_minimum_size = Vector2(180, 20)
	btn.size_flags_horizontal = Control.SIZE_SHRINK_END
	btn.pressed.connect(_on_continue)
	vbox.add_child(btn)
	if _shell.has_signal("back_pressed"):
		_shell.back_pressed.connect(_on_back)

func _update_portrait(lord_index: int) -> void:
	if _portrait == null:
		return
	if lord_index < 0:
		_portrait.texture = null
		return
	# Java imgchar: bB.a(0+paramInt) — jang_1..jang_37 (аватарки)
	var path := "res://jang_%d.png" % (lord_index + 1)
	var tex = load(path) as Texture2D
	_portrait.texture = tex

func set_lord_dialog(lord_name: String, lord_index: int, dialog_text: String) -> void:
	# Java: str1 = dt[dk] (ім'я лорда) або dA[dm]/dC.a за dG; arrayOfString[1] = "[" + str1 + "] "
	if _name_label != null:
		_name_label.text = "[%s]" % lord_name
	if _body_label != null:
		_body_label.text = dialog_text
	_update_portrait(lord_index)

func _on_continue() -> void:
	continue_pressed.emit()

func _on_back() -> void:
	back_pressed.emit()
