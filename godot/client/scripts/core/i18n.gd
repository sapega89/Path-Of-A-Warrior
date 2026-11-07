extends Node
## Loads the UI strings from res://i18n/strings.json into TranslationServer.
##
## The file maps a key to its text per locale:
##   {"menu.play": {"en": "Play", "uk": "Грати"}, ...}
## Controls translate their text automatically, code uses tr("menu.play").
## JSON (not CSV) so that tests and headless runs need no import step.
## res://i18n/names.json (made by godot/tools/import_original.py) has the same shape: the
## English names of heroes, skills and things -> their text per locale, so tr(name) shows a
## name in the player's language.

const STRINGS_PATH := "res://i18n/strings.json"
const NAMES_PATH := "res://i18n/names.json"
const LOCALES: Array[String] = ["en", "uk"]
const FALLBACK := "en"

var _loaded: Array[Translation] = []


func _ready() -> void:
	load_files([STRINGS_PATH, NAMES_PATH])


## Parses the strings file. Returns {locale: {key: text}}, or {} on bad input.
static func parse(text: String) -> Dictionary:
	var data: Variant = JSON.parse_string(text)
	if typeof(data) != TYPE_DICTIONARY:
		return {}
	var out := {}
	for locale in LOCALES:
		out[locale] = {}
	for key in data:
		var entry: Variant = data[key]
		if typeof(entry) != TYPE_DICTIONARY:
			continue
		for locale in LOCALES:
			if entry.has(locale):
				out[locale][str(key)] = str(entry[locale])
	return out


## Loads the files into one Translation per locale (replacing the ones loaded before).
## Returns the number of keys.
func load_files(paths: Array) -> int:
	for t in _loaded:
		TranslationServer.remove_translation(t)
	_loaded.clear()
	var table := {}
	for locale in LOCALES:
		table[locale] = {}
	for path in paths:
		var file := FileAccess.open(path, FileAccess.READ)
		if file == null:
			push_error("i18n: cannot open %s" % path)
			continue
		var part := parse(file.get_as_text())
		for locale in part:
			table[locale].merge(part[locale], true)
	var keys := 0
	for locale in table:
		var t := Translation.new()
		t.locale = locale
		for key in table[locale]:
			t.add_message(key, table[locale][key])
		TranslationServer.add_translation(t)
		_loaded.append(t)
		keys = maxi(keys, table[locale].size())
	return keys


## Which locale to use: the saved choice, else the system language, else English.
static func pick_locale(saved: String, os_language: String) -> String:
	if saved in LOCALES:
		return saved
	if os_language in LOCALES:
		return os_language
	return FALLBACK
