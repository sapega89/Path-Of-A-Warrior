extends Control
## Settings: language, music and sound volume, fullscreen (desktop only).

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const I18nScript := preload("res://scripts/core/i18n.gd")
## Language names are shown in their own language, not translated.
const LANGUAGE_NAMES := {"en": "English", "uk": "Українська"}

var language: OptionButton
var music: HSlider
var sfx: HSlider
var fullscreen: CheckBox
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

	if Settings.can_fullscreen():
		fullscreen = CheckBox.new()
		fullscreen.name = "Fullscreen"
		fullscreen.button_pressed = Settings.get_value("fullscreen")
		fullscreen.toggled.connect(func(on: bool): Settings.set_value("fullscreen", on))
		_row(col, "settings.fullscreen", fullscreen)

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
