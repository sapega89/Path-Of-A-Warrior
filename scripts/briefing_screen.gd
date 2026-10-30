extends Control
## Два режими: 1) Бріфінг — тільки текст місії (без лорда). 2) Діалог з лордом — портрет + ім'я + репліка.

signal continue_pressed
signal back_pressed

@export var lord_name: String = "Lord"
@export var lord_index: int = -1
@export var dialog_text: String = "Complete the objective."

var _shell: Control
var _portrait: TextureRect
var _name_label: Label
var _body_label: Label
var _continue_btn: Button
var _is_briefing_only: bool = true

func _ready() -> void:
	_shell = $SubmenuShell
	_shell.set_menu("", [])
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
	_portrait.custom_minimum_size = Vector2(64, 64)
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
	scroll.add_child(_body_label)
	_continue_btn = Button.new()
	_continue_btn.text = "Continue"
	_continue_btn.custom_minimum_size = Vector2(200, 28)
	_continue_btn.size_flags_horizontal = Control.SIZE_SHRINK_END
	_continue_btn.pressed.connect(_on_continue)
	vbox.add_child(_continue_btn)
	if _shell.has_signal("back_pressed"):
		_shell.back_pressed.connect(_on_back)

func _update_visibility() -> void:
	if _portrait != null:
		_portrait.visible = not _is_briefing_only
	if _name_label != null:
		_name_label.visible = not _is_briefing_only

func _update_portrait() -> void:
	if _portrait == null:
		return
	if lord_index < 0:
		_portrait.texture = null
		return
	var path := "res://jang_%d.png" % (lord_index + 1)
	var tex = load(path) as Texture2D
	_portrait.texture = tex

func _on_back() -> void:
	back_pressed.emit()

## Крок 3: тільки текст місії (бріфінг), без портрета й імені лорда.
func set_mission_briefing(mission_name: String, mission_text: String) -> void:
	_is_briefing_only = true
	lord_index = -1
	if _shell != null:
		_shell.set_title(mission_name)
	if _name_label != null:
		_name_label.text = ""
	if _body_label != null:
		_body_label.text = mission_text
	_update_visibility()
	_update_portrait()

## Заповнити діалог: промовець (лорд), індекс для портрета jang_*, текст репліки.
func set_briefing(title: String, text: String) -> void:
	lord_name = title
	dialog_text = text
	if _name_label != null:
		_name_label.text = "[%s]" % lord_name
	if _body_label != null:
		_body_label.text = dialog_text

## Крок 5: діалог з лордом — портрет, ім'я, репліка.
func set_lord_dialog(p_lord_name: String, p_lord_index: int, p_dialog_text: String) -> void:
	_is_briefing_only = false
	lord_name = p_lord_name
	lord_index = p_lord_index
	dialog_text = p_dialog_text
	if _shell != null:
		_shell.set_title("")
	if _name_label != null:
		_name_label.text = "[%s]" % lord_name
	if _body_label != null:
		_body_label.text = dialog_text
	_update_visibility()
	_update_portrait()

func _on_continue() -> void:
	continue_pressed.emit()
