extends Control
## Вибір лорда для місії (Java cM[0]=1, C() → ds[], dt[] з v(48), cN=dr до 6).
## Список без портретів: тільки dt[] — імена лордів. Заблоковані — сірим (e.java f() case 1: dw & 1<<ds[i]-1).

signal lord_selected(lord_index: int)
signal back_pressed

var _shell: Control
var _lord_buttons: Array[Button] = []

func _ready() -> void:
	GameState._init_generals_if_needed()
	_build_ui()

func _build_ui() -> void:
	_shell = $SubmenuShell
	_shell.set_menu("Select Lord", [])  # Java: заголовок підменю
	var links_vbox: VBoxContainer = _shell.get_node_or_null("MainLayer/MenuFrame/LinksVBox")
	if links_vbox == null:
		return
	for c in links_vbox.get_children():
		c.queue_free()
	_lord_buttons.clear()
	var count := mini(GameState.LORDS_MAX, 6)
	for i in range(count):
		var btn := Button.new()
		btn.theme = preload("res://theme_list_button.tres")
		btn.text = _lord_name(i)
		btn.custom_minimum_size = Vector2(180, 20)  # Java f(): a(m, j, 180, 20, bool)
		btn.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
		var unlocked: bool = i < GameState.lord_unlocked.size() and GameState.lord_unlocked[i]
		if not unlocked:
			btn.disabled = true
			btn.add_theme_color_override("font_color", Color(0.5, 0.5, 0.5, 1))
		else:
			btn.pressed.connect(_on_lord_pressed.bind(i))
		links_vbox.add_child(btn)
		_lord_buttons.append(btn)
	if _shell.has_signal("back_pressed"):
		_shell.back_pressed.connect(_on_back)

func _lord_name(index: int) -> String:
	# Java: dt[b] з v(48) — ім'я лорда; поки placeholder
	if index < GameState.general_names.size() and GameState.general_names[index] != "":
		return GameState.general_names[index]
	return "Lord %d" % (index + 1)

func _on_lord_pressed(lord_index: int) -> void:
	lord_selected.emit(lord_index)

func _on_back() -> void:
	back_pressed.emit()
