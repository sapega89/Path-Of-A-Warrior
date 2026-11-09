extends Control
## Settings: language, music and sound volume, the game speed, the hit effects on the map (all
## of them, the screen shake, the vibration), the world as pixel art or smooth, fullscreen
## (desktop only), and Training
## (training_screen.gd) to take the training again (not over the mission's pause).

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const I18nScript := preload("res://scripts/core/i18n.gd")
## Language names are shown in their own language, not translated.
const LANGUAGE_NAMES := {"en": "English", "uk": "Українська"}

var language: OptionButton
var music: HSlider
var sfx: HSlider
var fullscreen: CheckBox
var speed: OptionButton  # the game speed of the missions
var hit_feel: CheckBox
var screen_shake: CheckBox
var rumble: CheckBox
var pixel_art: CheckBox
## Shown over another screen (the mission's pause menu): what Back does instead of going back.
var close := Callable()


func _ready() -> void:
	var col := UiTheme.menu_column(self, 600)
	col.add_child(UiTheme.heading("settings.title", 44))

	language = OptionButton.new()
	language.name = "Language"
	for i in I18nScript.LOCALES.size():
		var code: String = I18nScript.LOCALES[i]
		language.add_item(LANGUAGE_NAMES.get(code, code), i)
		language.set_item_metadata(i, code)
	language.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	language.select(I18nScript.LOCALES.find(Settings.current_locale()))
	language.item_selected.connect(func(i: int): Settings.set_value("locale", language.get_item_metadata(i)))
	_row(col, "settings.language", language)

	music = _slider("Music", "music_volume")
	_row(col, "settings.music", music)
	sfx = _slider("Sfx", "sfx_volume")
	_row(col, "settings.sfx", sfx)

	speed = OptionButton.new()
	speed.name = "Speed"
	for i in Settings.SPEED_MS.size():
		speed.add_item(tr("settings.speed_%d" % i), i)
	speed.select(int(Settings.get_value("game_speed")))
	speed.item_selected.connect(func(i: int): Settings.set_value("game_speed", i))
	_row(col, "settings.speed", speed)

	hit_feel = _check("HitFeel", "hit_feel")
	_row(col, "settings.hit_feel", hit_feel)
	screen_shake = _check("ScreenShake", "screen_shake")
	_row(col, "settings.screen_shake", screen_shake)
	rumble = _check("Rumble", "rumble")
	_row(col, "settings.rumble", rumble)
	pixel_art = _check("PixelArt", "pixel_art")
	_row(col, "settings.pixel_art", pixel_art)

	if Settings.can_fullscreen():
		fullscreen = CheckBox.new()
		fullscreen.name = "Fullscreen"
		fullscreen.button_pressed = Settings.get_value("fullscreen")
		fullscreen.toggled.connect(func(on: bool): Settings.set_value("fullscreen", on))
		_row(col, "settings.fullscreen", fullscreen)

	if not close.is_valid():
		var training := Button.new()
		training.name = "Training"
		training.text = "settings.training"
		training.pressed.connect(func(): Router.push("training", {}))
		col.add_child(training)

	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(_back)
	col.add_child(back)
	language.grab_focus.call_deferred()


func _back() -> void:
	if close.is_valid():
		close.call()
	else:
		Router.back()


func _check(node_name: String, key: String) -> CheckBox:
	var b := CheckBox.new()
	b.name = node_name
	b.button_pressed = Settings.get_value(key)
	b.toggled.connect(func(on: bool): Settings.set_value(key, on))
	return b


func _slider(node_name: String, key: String) -> HSlider:
	var s := HSlider.new()
	s.name = node_name
	s.min_value = 0.0
	s.max_value = 1.0
	s.step = 0.05
	s.value = Settings.get_value(key)
	s.custom_minimum_size = Vector2(260, 28)
	s.value_changed.connect(_volume_changed.bind(key))
	return s


## A volume is set, and the sound of the setting plays at it.
func _volume_changed(v: float, key: String) -> void:
	Settings.set_value(key, v)
	if v > 0.0:
		Audio.play_sound(8)


func _row(col: VBoxContainer, label_key: String, control: Control) -> void:
	var row := HBoxContainer.new()
	var l := Label.new()
	l.text = label_key
	l.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(l)
	control.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(control)
	col.add_child(row)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		_back()
