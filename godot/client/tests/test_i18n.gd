extends "res://tests/test_case.gd"

const I18nScript := preload("res://scripts/core/i18n.gd")
const Profile := preload("res://scripts/core/profile.gd")
const OnlineClient := preload("res://scripts/net/online_client.gd")


func _table() -> Dictionary:
	return I18nScript.parse(FileAccess.get_file_as_string(I18nScript.STRINGS_PATH))


func test_parse() -> void:
	var t := I18nScript.parse('{"a.b": {"en": "A", "uk": "Б"}, "bad": 3}')
	eq(t["en"], {"a.b": "A"}, "en")
	eq(t["uk"], {"a.b": "Б"}, "uk")
	eq(I18nScript.parse("not json"), {}, "bad file")


func test_every_key_has_every_language() -> void:
	var t := _table()
	check(t["en"].size() > 0, "no strings")
	for key in t["en"]:
		for locale in I18nScript.LOCALES:
			check(t[locale].get(key, "") != "", "%s has no %s text" % [key, locale])


func test_keys_used_in_code_exist() -> void:
	var t := _table()
	var re := RegEx.create_from_string('"((?:game|title|menu|settings|common|viewer)\\.[a-z_]+)"')
	for path in _scripts("res://scripts"):
		for m in re.search_all(FileAccess.get_file_as_string(path)):
			check(t["en"].has(m.get_string(1)), "%s uses unknown key %s" % [path, m.get_string(1)])


func test_pick_locale() -> void:
	eq(I18nScript.pick_locale("uk", "en"), "uk", "saved wins")
	eq(I18nScript.pick_locale("", "uk"), "uk", "system language")
	eq(I18nScript.pick_locale("", "de"), "en", "fallback")
	eq(I18nScript.pick_locale("xx", "de"), "en", "unknown saved")


func test_translation_server_has_strings() -> void:
	var before := TranslationServer.get_locale()
	TranslationServer.set_locale("uk")
	eq(String(TranslationServer.translate("menu.play")), "Грати", "uk text")
	TranslationServer.set_locale("en")
	eq(String(TranslationServer.translate("menu.play")), "Play", "en text")
	TranslationServer.set_locale(before)


static func _scripts(dir: String) -> Array[String]:
	var out: Array[String] = []
	for f in DirAccess.get_files_at(dir):
		if f.ends_with(".gd"):
			out.append(dir + "/" + f)
	for d in DirAccess.get_directories_at(dir):
		out.append_array(_scripts(dir + "/" + d))
	return out


func test_names_have_every_language() -> void:
	var t := I18nScript.parse(FileAccess.get_file_as_string(I18nScript.NAMES_PATH))
	for name in Profile.HERO_CLASSES + OnlineClient.SKILL_NAMES:
		for locale in I18nScript.LOCALES:
			check(t[locale].get(name, "") != "", "%s has no %s name" % [name, locale])


func test_a_name_in_the_players_language() -> void:
	var before := TranslationServer.get_locale()
	TranslationServer.set_locale("uk")
	eq(String(TranslationServer.translate("Cossack")), "Козак", "a hero class")
	eq(OnlineClient.skill_name(3), "Шабля-вихор", "an online skill")
	TranslationServer.set_locale(before)
