extends Node
## Loads the UI strings from res://i18n/strings.json into TranslationServer.
##
## The file maps a key to its text per locale:
##   {"menu.play": {"en": "Play", "uk": "Грати"}, ...}
## Controls translate their text automatically, code uses tr("menu.play").
## JSON (not CSV) so that tests and headless runs need no import step.

const STRINGS_PATH := "res://i18n/strings.json"
const LOCALES: Array[String] = ["en", "uk"]
const FALLBACK := "en"

var _loaded: Array[Translation] = []


func _ready() -> void:
	load_strings(STRINGS_PATH)


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


## Loads the file and registers one Translation per locale. Returns the number of keys.
func load_strings(path: String) -> int:
	for t in _loaded:
		TranslationServer.remove_translation(t)
	_loaded.clear()
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("i18n: cannot open %s" % path)
		return 0
	var table := parse(file.get_as_text())
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
