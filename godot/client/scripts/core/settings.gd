extends Node
## Player settings, kept on this computer in user://settings.cfg and applied to the engine.

signal changed(key: String)

const DEFAULT_PATH := "user://settings.cfg"
const SECTION := "settings"
const DEFAULTS := {
	"locale": "",  # "" = follow the system language
	"music_volume": 0.8,
	"sfx_volume": 0.8,
	"fullscreen": false,
	"game_speed": 2,  # the missions' speed: 0 Slow .. 4 Fast (SPEED_MS)
	"hit_feel": true,  # the hitstop, shake, flash, flight and sound of a hit on the map
	"screen_shake": true,  # of those, the camera shake
	"rumble": true,  # of those, the pad's (or the phone's) rumble
	"brightness": 0.5,  # the 3D world's: 0.5 as it is drawn, 0 darker, 1 brighter (world_gamma)
	"graphics": 1,  # 0 Low, 1 Medium (the engine's own but the sun map), 2 High (GRAPHICS)
	"window_size": 0,  # the window when not in full screen (WINDOW_SIZES; desktop only)
	"controls": {},  # the keys and pad buttons changed by the player (KeyBindings.changes())
}
## One tick of a mission at each game speed, in ms (2, Med, is the simulation's own tick).
const SPEED_MS := [250, 180, 120, 90, 50]
const BUSES := {"music_volume": "Music", "sfx_volume": "SFX"}
## What each graphics quality (Low, Medium, High) draws: the sun's shadow map (pixels a side) and
## how soft its edges are, the lamps' and fires' shadow maps in each 3D view (never 0: the
## compatibility renderer then draws the world white), and whether the camp's fires cast shadows
## (each is a cube map: the scene drawn six more times a frame, 2/3 of the camp's triangles; not
## on Low). The world is drawn about 360 pixels high, so a sun map of 2048 is already finer than
## the picture: Medium is the engine's own but for the sun, whose map of 4096 would cost four
## times the pixels each frame for the same picture.
const GRAPHICS := [
	{
		"sun": 1024,
		"soft": RenderingServer.SHADOW_QUALITY_HARD,
		"lamps": 1024,
		"fire_shadows": false,
	},
	{
		"sun": 2048,
		"soft": RenderingServer.SHADOW_QUALITY_SOFT_LOW,
		"lamps": 2048,
		"fire_shadows": true,
	},
	{
		"sun": 4096,
		"soft": RenderingServer.SHADOW_QUALITY_SOFT_HIGH,
		"lamps": 4096,
		"fire_shadows": true,
	},
]
## The window's sizes to choose from (the first is the game's own); those larger than the screen
## are not offered.
const WINDOW_SIZES := [
	Vector2i(1280, 720), Vector2i(1600, 900), Vector2i(1920, 1080), Vector2i(2560, 1440)
]
## The choices of each whole-number setting: its value is a place in them.
const INT_CHOICES := {"game_speed": SPEED_MS, "graphics": GRAPHICS, "window_size": WINDOW_SIZES}
## How far the brightness goes: at 0 and 1 the world's gamma is 2 to the power of plus or minus
## half of it.
const GAMMA_RANGE := 1.5

var path := DEFAULT_PATH
var _values := {}


func _ready() -> void:
	_ensure_buses()
	load_from_disk()
	apply_all()


func get_value(key: String) -> Variant:
	return _values.get(key, DEFAULTS.get(key))


## Changes a setting, applies it and saves. Unknown keys and wrong types are ignored.
func set_value(key: String, value: Variant) -> bool:
	if not DEFAULTS.has(key):
		push_warning("settings: unknown key %s" % key)
		return false
	value = _coerce(key, value)
	if value == null:
		return false
	if get_value(key) == value:
		return true
	_values[key] = value
	_apply(key)
	save_to_disk()
	changed.emit(key)
	return true


func reset() -> void:
	_values = DEFAULTS.duplicate()


func load_from_disk() -> void:
	reset()
	var cfg := ConfigFile.new()
	if cfg.load(path) != OK:
		return
	for key in DEFAULTS:
		var v: Variant = _coerce(key, cfg.get_value(SECTION, key, DEFAULTS[key]))
		if v != null:
			_values[key] = v


func save_to_disk() -> Error:
	var cfg := ConfigFile.new()
	for key in DEFAULTS:
		cfg.set_value(SECTION, key, get_value(key))
	return cfg.save(path)


func apply_all() -> void:
	for key in DEFAULTS:
		_apply(key)


## The locale the game shows now.
func current_locale() -> String:
	return I18n.pick_locale(get_value("locale"), OS.get_locale_language())


## A mission's tick at the chosen game speed, in seconds.
func tick_seconds() -> float:
	return SPEED_MS[int(get_value("game_speed"))] / 1000.0


static func can_fullscreen() -> bool:
	return (
		not (OS.has_feature("mobile") or OS.has_feature("web"))
		and DisplayServer.get_name() != "headless"
	)


func _coerce(key: String, value: Variant) -> Variant:
	match typeof(DEFAULTS[key]):
		TYPE_FLOAT:
			if typeof(value) in [TYPE_FLOAT, TYPE_INT]:
				return clampf(float(value), 0.0, 1.0)
		TYPE_BOOL:
			if typeof(value) == TYPE_BOOL:
				return value
		TYPE_INT:
			if typeof(value) in [TYPE_FLOAT, TYPE_INT]:
				return clampi(int(value), 0, INT_CHOICES[key].size() - 1)
		TYPE_STRING:
			if typeof(value) == TYPE_STRING:
				return value
		TYPE_DICTIONARY:
			if typeof(value) == TYPE_DICTIONARY:
				return value
	return null


func _apply(key: String) -> void:
	match key:
		"locale":
			TranslationServer.set_locale(current_locale())
		"music_volume", "sfx_volume":
			var bus := AudioServer.get_bus_index(BUSES[key])
			if bus >= 0:
				var v: float = get_value(key)
				AudioServer.set_bus_volume_db(bus, volume_db(v))
				AudioServer.set_bus_mute(bus, v <= 0.0)
		"brightness":
			RenderingServer.global_shader_parameter_set(&"world_gamma", world_gamma(get_value(key)))
		"fullscreen":
			if can_fullscreen():
				DisplayServer.window_set_mode(
					(
						DisplayServer.WINDOW_MODE_FULLSCREEN
						if get_value(key)
						else DisplayServer.WINDOW_MODE_WINDOWED
					)
				)
				_size_window()
		"window_size":
			_size_window()
		"graphics":
			var g: Dictionary = graphics()
			RenderingServer.directional_shadow_atlas_set_size(g.sun, true)
			RenderingServer.directional_soft_shadow_filter_set_quality(g.soft)
			RenderingServer.positional_soft_shadow_filter_set_quality(g.soft)


## What the chosen graphics quality draws (GRAPHICS).
func graphics() -> Dictionary:
	return GRAPHICS[int(get_value("graphics"))]


## The window at its chosen size, in the middle of its screen (in full screen nothing changes).
func _size_window() -> void:
	if not can_fullscreen() or get_value("fullscreen"):
		return
	var size: Vector2i = WINDOW_SIZES[int(get_value("window_size"))]
	var screen := DisplayServer.window_get_current_screen()
	var room := DisplayServer.screen_get_usable_rect(screen)
	DisplayServer.window_set_size(size)
	DisplayServer.window_set_position(room.position + (room.size - size) / 2)


## The window's sizes that fit in `room` (the screen), as indexes of WINDOW_SIZES; the first
## always.
static func window_sizes_within(room: Vector2i) -> Array[int]:
	var fit: Array[int] = [0]
	for i in range(1, WINDOW_SIZES.size()):
		if WINDOW_SIZES[i].x <= room.x and WINDOW_SIZES[i].y <= room.y:
			fit.append(i)
	return fit


## The gamma the world is shown with (pixel_view.gd) at a brightness (0..1): 1 at the middle,
## below 1 (the shade lifted) above it, over 1 (the shade deeper) under it.
static func world_gamma(brightness: float) -> float:
	return pow(2.0, (0.5 - brightness) * GAMMA_RANGE)


## A volume (0..1) as its bus's dB, by ear: the amplitude is the volume squared,
## so a quarter is -24 dB, a half -12 dB, three quarters -5 dB.
static func volume_db(volume: float) -> float:
	return linear_to_db(maxf(volume * volume, 0.000001))


static func _ensure_buses() -> void:
	for bus_name in BUSES.values():
		if AudioServer.get_bus_index(bus_name) < 0:
			AudioServer.add_bus()
			var idx := AudioServer.bus_count - 1
			AudioServer.set_bus_name(idx, bus_name)
			AudioServer.set_bus_send(idx, "Master")
