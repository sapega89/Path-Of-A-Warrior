class_name SettingsScreen
extends BaseScreen
## Settings: language, music and sound volume, the game speed, the hit effects on the map (all
## of them, the screen shake, the vibration), the world's brightness, the graphics quality,
## fullscreen and the window's size (desktop only), and Controls (controls_screen.gd: the keys and
## pad buttons, shown over these settings). The options scroll; Controls and Back stay in a row
## under them.

## Language names are shown in their own language, not translated.
const LANGUAGE_NAMES := {"en": "English", "uk": "Українська"}

## Shown over another screen (the mission's pause menu): what Back does instead of going back.
var close := Callable()

@onready var language: OptionButton = %Language
@onready var music: HSlider = %Music
@onready var sfx: HSlider = %Sfx
@onready var fullscreen: CheckBox = %Fullscreen  # desktop only (freed elsewhere)
@onready var speed: OptionButton = %Speed  # the game speed of the missions
@onready var hit_feel: CheckBox = %HitFeel
@onready var screen_shake: CheckBox = %ScreenShake
@onready var rumble: CheckBox = %Rumble
@onready var brightness: HSlider = %Brightness
@onready var graphics: OptionButton = %Graphics
@onready var window_size: OptionButton = %WindowSize  # desktop only (freed elsewhere)
@onready var column: VBoxContainer = %Column


## The settings as they are now; the rows the platform has not (fullscreen, the window's size)
## are taken away.
func _ready() -> void:
	for i in I18n.LOCALES.size():
		var code: String = I18n.LOCALES[i]
		language.add_item(LANGUAGE_NAMES.get(code, code), i)
		language.set_item_metadata(i, code)
	language.select(I18n.LOCALES.find(Settings.current_locale()))
	for i in Settings.SPEED_MS.size():
		speed.add_item(tr("settings.speed_%d" % i), i)
	speed.select(int(Settings.get_value("game_speed")))
	music.set_value_no_signal(Settings.get_value("music_volume"))
	sfx.set_value_no_signal(Settings.get_value("sfx_volume"))
	hit_feel.set_pressed_no_signal(Settings.get_value("hit_feel"))
	screen_shake.set_pressed_no_signal(Settings.get_value("screen_shake"))
	rumble.set_pressed_no_signal(Settings.get_value("rumble"))
	brightness.set_value_no_signal(Settings.get_value("brightness"))
	for i in Settings.GRAPHICS.size():
		graphics.add_item(tr("settings.graphics_%d" % i), i)
	graphics.select(int(Settings.get_value("graphics")))
	if Settings.can_fullscreen():
		fullscreen.set_pressed_no_signal(Settings.get_value("fullscreen"))
		_list_window_sizes()
	else:
		fullscreen.get_parent().free()
		fullscreen = null
		window_size.get_parent().free()
		window_size = null
	language.grab_focus()


## The window's sizes that fit the screen; each item's id is its place in Settings.WINDOW_SIZES.
func _list_window_sizes() -> void:
	var screen := DisplayServer.window_get_current_screen()
	for i in Settings.window_sizes_within(DisplayServer.screen_get_usable_rect(screen).size):
		var s: Vector2i = Settings.WINDOW_SIZES[i]
		window_size.add_item("%d × %d" % [s.x, s.y], i)
	window_size.select(window_size.get_item_index(int(Settings.get_value("window_size"))))


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


func _on_brightness(v: float) -> void:
	Settings.set_value("brightness", v)


func _on_rumble(on: bool) -> void:
	Settings.set_value("rumble", on)


func _on_fullscreen(on: bool) -> void:
	Settings.set_value("fullscreen", on)


func _on_graphics(i: int) -> void:
	Settings.set_value("graphics", i)


func _on_window_size(i: int) -> void:
	Settings.set_value("window_size", window_size.get_item_id(i))


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
