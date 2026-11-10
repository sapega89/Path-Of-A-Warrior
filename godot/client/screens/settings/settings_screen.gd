class_name SettingsScreen
extends BaseScreen
## Settings: language, music and sound volume, the game speed, the hit effects on the map (all
## of them, the screen shake, the vibration), the world as pixel art or smooth, its brightness,
## fullscreen (desktop only), and Controls (controls_screen.gd: the keys and pad buttons, shown
## over these settings). The options scroll; Controls and Back stay in a row under them.

const I18nScript := preload("res://scripts/core/i18n.gd")
## Language names are shown in their own language, not translated.
const LANGUAGE_NAMES := {"en": "English", "uk": "Українська"}

@onready var language: OptionButton = %Language
@onready var music: HSlider = %Music
@onready var sfx: HSlider = %Sfx
@onready var fullscreen: CheckBox = %Fullscreen  # desktop only (freed elsewhere)
@onready var speed: OptionButton = %Speed  # the game speed of the missions
@onready var hit_feel: CheckBox = %HitFeel
@onready var screen_shake: CheckBox = %ScreenShake
@onready var rumble: CheckBox = %Rumble
@onready var pixel_art: CheckBox = %PixelArt
@onready var brightness: HSlider = %Brightness
@onready var column: VBoxContainer = %Column
## Shown over another screen (the mission's pause menu): what Back does instead of going back.
var close := Callable()


## The settings as they are now; a row the platform has not (fullscreen) is taken away.
func _ready() -> void:
	for i in I18nScript.LOCALES.size():
		var code: String = I18nScript.LOCALES[i]
		language.add_item(LANGUAGE_NAMES.get(code, code), i)
		language.set_item_metadata(i, code)
	language.select(I18nScript.LOCALES.find(Settings.current_locale()))
	for i in Settings.SPEED_MS.size():
		speed.add_item(tr("settings.speed_%d" % i), i)
	speed.select(int(Settings.get_value("game_speed")))
	music.set_value_no_signal(Settings.get_value("music_volume"))
	sfx.set_value_no_signal(Settings.get_value("sfx_volume"))
	hit_feel.set_pressed_no_signal(Settings.get_value("hit_feel"))
	screen_shake.set_pressed_no_signal(Settings.get_value("screen_shake"))
	rumble.set_pressed_no_signal(Settings.get_value("rumble"))
	pixel_art.set_pressed_no_signal(Settings.get_value("pixel_art"))
	brightness.set_value_no_signal(Settings.get_value("brightness"))
	if Settings.can_fullscreen():
		fullscreen.set_pressed_no_signal(Settings.get_value("fullscreen"))
	else:
		fullscreen.get_parent().free()
		fullscreen = null
	language.grab_focus.call_deferred()


func _back() -> void:
	if close.is_valid():
		close.call()
	else:
		Router.back()


func _on_language(i: int) -> void:
	Settings.set_value("locale", language.get_item_metadata(i))


func _on_speed(i: int) -> void:
	Settings.set_value("game_speed", i)


func _on_music(v: float) -> void:
	_volume_changed(v, "music_volume")


func _on_sfx(v: float) -> void:
	_volume_changed(v, "sfx_volume")


func _on_hit_feel(on: bool) -> void:
	Settings.set_value("hit_feel", on)


func _on_screen_shake(on: bool) -> void:
	Settings.set_value("screen_shake", on)


func _on_pixel_art(on: bool) -> void:
	Settings.set_value("pixel_art", on)


func _on_brightness(v: float) -> void:
	Settings.set_value("brightness", v)


func _on_rumble(on: bool) -> void:
	Settings.set_value("rumble", on)


func _on_fullscreen(on: bool) -> void:
	Settings.set_value("fullscreen", on)


## The Controls over these settings; their Back comes back here.
func open_controls() -> ControlsScreen:
	var controls: ControlsScreen = Router.make(Router.SCREENS["controls"])
	controls.name = "Controls"
	controls.set_anchors_preset(Control.PRESET_FULL_RECT)
	controls.close = _close_controls.bind(controls)
	column.visible = false
	add_child(controls)
	return controls


func _close_controls(controls: ControlsScreen) -> void:
	controls.queue_free()
	column.visible = true
	(%Controls as Button).grab_focus()


## A volume is set, and the sound of the setting plays at it.
func _volume_changed(v: float, key: String) -> void:
	Settings.set_value(key, v)
	if v > 0.0:
		Audio.play_sound(8)


func go_back() -> void:
	_back()
