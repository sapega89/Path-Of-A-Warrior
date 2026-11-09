extends Node
## Player settings, kept in user://settings.cfg and applied to the engine.
## The volumes and the game speed (CLOUD_KEYS) are kept on the server too, with the account
## (scripts/net/cloud_sync.gd): the newer copy wins, and on a device the account is new to,
## the server's. The language and the full screen belong to the device.

signal changed(key: String)

const I18nScript := preload("res://scripts/core/i18n.gd")
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
	"pixel_art": true,  # the 3D world drawn as pixel art (pixel_view.gd), or smooth
}
## One tick of a mission at each game speed, in ms (2, Med, is the simulation's own tick).
const SPEED_MS := [250, 180, 120, 90, 50]
const BUSES := {"music_volume": "Music", "sfx_volume": "SFX"}
const CLOUD_KEYS := ["music_volume", "sfx_volume", "game_speed"]
const CLOUD_SECTION := "cloud"

var path := DEFAULT_PATH
var _values := {}
## The copy on the server: the account it is of ("" none yet), its revision, when these
## options last changed (unix ms) and whether that change still has to reach the server.
var cloud := {"user": "", "rev": 0, "at": 0, "dirty": false}
var clock: Callable = func() -> int: return int(Time.get_unix_time_from_system() * 1000.0)


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
	if key in CLOUD_KEYS:
		cloud.at = maxi(int(clock.call()), int(cloud.at) + 1)
		cloud.dirty = true
	_apply(key)
	save_to_disk()
	changed.emit(key)
	return true


func reset() -> void:
	_values = DEFAULTS.duplicate()
	cloud = {"user": "", "rev": 0, "at": 0, "dirty": false}


func load_from_disk() -> void:
	reset()
	var cfg := ConfigFile.new()
	if cfg.load(path) != OK:
		return
	for key in DEFAULTS:
		var v: Variant = _coerce(key, cfg.get_value(SECTION, key, DEFAULTS[key]))
		if v != null:
			_values[key] = v
	cloud.user = str(cfg.get_value(CLOUD_SECTION, "user", ""))
	cloud.rev = int(cfg.get_value(CLOUD_SECTION, "rev", 0))
	cloud.at = int(cfg.get_value(CLOUD_SECTION, "at", 0))
	cloud.dirty = bool(cfg.get_value(CLOUD_SECTION, "dirty", false))


func save_to_disk() -> Error:
	var cfg := ConfigFile.new()
	for key in DEFAULTS:
		cfg.set_value(SECTION, key, get_value(key))
	for key in cloud:
		cfg.set_value(CLOUD_SECTION, key, cloud[key])
	return cfg.save(path)


## The options kept on the server.
func cloud_values() -> Dictionary:
	var d := {}
	for key in CLOUD_KEYS:
		d[key] = get_value(key)
	return d


## The server's copy of the options: applied and saved, nothing to send back.
func take_cloud(values: Dictionary) -> void:
	for key in CLOUD_KEYS:
		var v: Variant = _coerce(key, values.get(key))
		if v == null or v == get_value(key):
			continue
		_values[key] = v
		_apply(key)
		changed.emit(key)
	save_to_disk()


## Keeps `cloud` (changed by the sync) with the options.
func save_cloud() -> void:
	save_to_disk()


func apply_all() -> void:
	for key in DEFAULTS:
		_apply(key)


## The locale the game shows now.
func current_locale() -> String:
	return I18nScript.pick_locale(get_value("locale"), OS.get_locale_language())


## A mission's tick at the chosen game speed, in seconds.
func tick_seconds() -> float:
	return SPEED_MS[int(get_value("game_speed"))] / 1000.0


static func can_fullscreen() -> bool:
	return not (OS.has_feature("mobile") or OS.has_feature("web")) \
		and DisplayServer.get_name() != "headless"


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
				return clampi(int(value), 0, SPEED_MS.size() - 1)
		TYPE_STRING:
			if typeof(value) == TYPE_STRING:
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
		"pixel_art":
			# the shaders of the world draw for it: hard steps of light, no grain finer than a pixel
			RenderingServer.global_shader_parameter_set(&"pixel_art", 1.0 if get_value(key) else 0.0)
		"fullscreen":
			if can_fullscreen():
				DisplayServer.window_set_mode(
					DisplayServer.WINDOW_MODE_FULLSCREEN if get_value(key)
					else DisplayServer.WINDOW_MODE_WINDOWED)


## A volume (0..1) as its bus's dB, by ear as in pyport: the amplitude is the volume squared,
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
