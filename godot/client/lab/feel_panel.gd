extends PanelContainer
## The lab's panel (lab/combat_feel_lab.gd), on the right: a switch for each effect of
## lab/combat_feel.gd, sliders for its main numbers, and the arena's own switches (waves, god
## mode) and buttons (a wave, archers, a general). H hides it.

const EFFECTS := [
	["hitstop", "Хитстоп"], ["shake", "Тряска камеры"], ["flash", "Вспышка"],
	["recoil", "Отдача при ударе"], ["knock_ease", "Резкий отброс"],
	["launch", "Отлёт убитого"], ["sound", "Звук с разбросом"],
]
## [key of CombatFeel.p, label, min, max, step]
const SLIDERS := [
	["stop_scale", "Хитстоп ×", 0.0, 3.0, 0.1],
	["stop_hit", "Хитстоп: удар, с", 0.0, 0.2, 0.01],
	["stop_kill", "Хитстоп: убийство, с", 0.0, 0.3, 0.01],
	["shake_scale", "Тряска ×", 0.0, 3.0, 0.1],
	["shake_px", "Тряска: амплитуда, px", 0.0, 24.0, 0.5],
	["shake_decay", "Тряска: затухание /с", 0.5, 6.0, 0.1],
	["flash_hit", "Вспышка: удар, с", 0.0, 0.3, 0.01],
	["recoil_px", "Отдача, px", 0.0, 12.0, 0.5],
	["launch_px", "Отлёт, px", 0.0, 60.0, 1.0],
	["launch_hop_px", "Подскок, px", 0.0, 20.0, 1.0],
	["pitch_spread", "Разброс высоты звука", 0.0, 0.3, 0.01],
]

var feel: RefCounted
var lab: Node
var _boxes := {}
var _sliders := {}
var _god: CheckBox
var _waves: CheckBox


func _ready() -> void:
	set_anchors_preset(Control.PRESET_RIGHT_WIDE)
	custom_minimum_size = Vector2(300, 0)
	offset_left = -310
	offset_right = -10
	offset_top = 96  # below the HUD's top bars (the enemy hit, on the right)
	offset_bottom = -40
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.05, 0.05, 0.07, 0.82)
	style.set_content_margin_all(10)
	style.set_corner_radius_all(6)
	add_theme_stylebox_override("panel", style)
	clip_contents = true
	var scroll := ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	add_child(scroll)
	var col := VBoxContainer.new()
	col.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	col.add_theme_constant_override("separation", 2)
	scroll.add_child(col)
	_title(col, "Ощущение боя")
	for e in EFFECTS:
		var key: String = e[0]
		var b := _check(col, e[1], bool(feel.on[key]))
		b.toggled.connect(func(v: bool) -> void: feel.on[key] = v)
		_boxes[key] = b
	var all := Button.new()
	all.text = "Все эффекты вкл / выкл (E)"
	all.focus_mode = Control.FOCUS_NONE
	all.clip_text = true
	all.add_theme_font_size_override("font_size", 14)
	all.pressed.connect(func() -> void: lab.toggle_all())
	col.add_child(all)
	_title(col, "Параметры")
	for s in SLIDERS:
		_slider(col, s)
	_title(col, "Арена")
	_waves = _check(col, "Волны мечников сами", lab.waves_on)
	_waves.toggled.connect(func(v: bool) -> void: lab.waves_on = v)
	_god = _check(col, "Бессмертие (F6)", lab.god)
	_god.toggled.connect(func(v: bool) -> void: lab.god = v)
	var row := HBoxContainer.new()
	col.add_child(row)
	_button(row, "Мечники", func() -> void: lab.spawn(201, 3))
	_button(row, "Лучники", func() -> void: lab.spawn(202, 2))
	_button(row, "Генерал", func() -> void: lab.spawn_general())


## Shows the switches as they are now (after E or F6).
func refresh() -> void:
	for key in _boxes:
		_boxes[key].set_pressed_no_signal(bool(feel.on[key]))
	if _god != null:
		_god.set_pressed_no_signal(lab.god)


func _title(col: VBoxContainer, text: String) -> void:
	var l := Label.new()
	l.text = text
	l.add_theme_font_size_override("font_size", 16)
	l.add_theme_color_override("font_color", Color(1.0, 0.82, 0.45))
	col.add_child(l)


func _check(col: VBoxContainer, text: String, value: bool) -> CheckBox:
	var b := CheckBox.new()
	b.text = text
	b.button_pressed = value
	b.focus_mode = Control.FOCUS_NONE
	b.add_theme_font_size_override("font_size", 14)
	for st in ["normal", "hover", "pressed", "hover_pressed", "focus", "disabled"]:
		b.add_theme_stylebox_override(st, StyleBoxEmpty.new())
	col.add_child(b)
	return b


func _button(row: HBoxContainer, text: String, call: Callable) -> void:
	var b := Button.new()
	b.text = text
	b.focus_mode = Control.FOCUS_NONE
	b.add_theme_font_size_override("font_size", 13)
	b.clip_text = true
	b.custom_minimum_size = Vector2(0, 30)
	b.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	b.pressed.connect(call)
	row.add_child(b)


func _slider(col: VBoxContainer, s: Array) -> void:
	var key: String = s[0]
	var label := Label.new()
	label.add_theme_font_size_override("font_size", 13)
	col.add_child(label)
	var slider := HSlider.new()
	slider.min_value = s[2]
	slider.max_value = s[3]
	slider.step = s[4]
	slider.value = float(feel.p[key])
	slider.focus_mode = Control.FOCUS_NONE
	slider.custom_minimum_size = Vector2(0, 18)
	col.add_child(slider)
	var show := func(v: float) -> void:
		label.text = "%s: %s" % [s[1], str(snappedf(v, s[4]))]
	show.call(slider.value)
	slider.value_changed.connect(func(v: float) -> void:
		feel.p[key] = v
		show.call(v))
	_sliders[key] = slider
