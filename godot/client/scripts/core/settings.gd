extends Node
## Player settings, kept in user://settings.cfg and applied to the engine.

signal changed(key: String)

const I18nScript := preload("res://scripts/core/i18n.gd")
const DEFAULT_PATH := "user://settings.cfg"
const SECTION := "settings"
const DEFAULTS := {
	"locale": "",  # "" = follow the system language
	"music_volume": 0.8,
	"sfx_volume": 0.8,
	"fullscreen": false,
	"server_url": "ws://127.0.0.1:28300",  # the game server (godot/server)
	"game_speed": 2,  # the missions' speed: 0 Slow .. 4 Fast (SPEED_MS)
}
## One tick of a mission at each game speed, in ms (2, Med, is the simulation's own tick).
const SPEED_MS := [250, 180, 120, 90, 50]
const BUSES := {"music_volume": "Music", "sfx_volume": "SFX"}

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
				AudioServer.set_bus_volume_db(bus, linear_to_db(maxf(v, 0.0001)))
				AudioServer.set_bus_mute(bus, v <= 0.0)
		"fullscreen":
			if can_fullscreen():
				DisplayServer.window_set_mode(
					DisplayServer.WINDOW_MODE_FULLSCREEN if get_value(key)
					else DisplayServer.WINDOW_MODE_WINDOWED)


static func _ensure_buses() -> void:
	for bus_name in BUSES.values():
		if AudioServer.get_bus_index(bus_name) < 0:
			AudioServer.add_bus()
			var idx := AudioServer.bus_count - 1
			AudioServer.set_bus_name(idx, bus_name)
			AudioServer.set_bus_send(idx, "Master")
