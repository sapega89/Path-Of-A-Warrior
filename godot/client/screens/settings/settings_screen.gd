class_name SettingsScreen
extends BaseScreen
## Settings: language, music and sound volume, the game speed, the hit effects on the map (all
## of them, the screen shake, the vibration), fullscreen (desktop only), and Training
## (training_screen.gd) to take the training again (not over the mission's pause).

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
## Shown over another screen (the mission's pause menu): what Back does instead of going back.
var close := Callable()


## The settings as they are now; the rows a platform has not (fullscreen) or a screen opened
## over another does not offer (Training) are taken away.
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
	if Settings.can_fullscreen():
		fullscreen.set_pressed_no_signal(Settings.get_value("fullscreen"))
	else:
		fullscreen.get_parent().free()
		fullscreen = null
	if close.is_valid():
		%Training.free()
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


func _on_rumble(on: bool) -> void:
	Settings.set_value("rumble", on)


func _on_fullscreen(on: bool) -> void:
	Settings.set_value("fullscreen", on)


func _on_training() -> void:
	Router.push("training", {})


## A volume is set, and the sound of the setting plays at it.
func _volume_changed(v: float, key: String) -> void:
	Settings.set_value(key, v)
	if v > 0.0:
		Audio.play_sound(8)


func go_back() -> void:
	_back()
