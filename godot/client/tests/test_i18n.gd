extends "res://tests/test_case.gd"


func _table() -> Dictionary:
	return I18n.parse(FileAccess.get_file_as_string(I18n.STRINGS_PATH))


func test_parse() -> void:
	var t := I18n.parse('{"a.b": {"en": "A", "uk": "Б"}, "bad": 3}')
	eq(t["en"], {"a.b": "A"}, "en")
	eq(t["uk"], {"a.b": "Б"}, "uk")
	eq(I18n.parse("not json"), {}, "bad file")


func test_every_key_has_every_language() -> void:
	var t := _table()
	check(t["en"].size() > 0, "no strings")
	for key in t["en"]:
		for locale in I18n.LOCALES:
			check(t[locale].get(key, "") != "", "%s has no %s text" % [key, locale])


func test_keys_used_in_code_exist() -> void:
	var t := _table()
	var re := RegEx.create_from_string('"((?:game|title|menu|settings|common|viewer)\\.[a-z_]+)"')
	for path in _scripts("res://scripts"):
		for m in re.search_all(FileAccess.get_file_as_string(path)):
			check(t["en"].has(m.get_string(1)), "%s uses unknown key %s" % [path, m.get_string(1)])


func test_pick_locale() -> void:
	eq(I18n.pick_locale("uk", "en"), "uk", "saved wins")
	eq(I18n.pick_locale("", "uk"), "uk", "system language")
	eq(I18n.pick_locale("", "de"), "en", "fallback")
	eq(I18n.pick_locale("xx", "de"), "en", "unknown saved")


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
	var t := I18n.parse(FileAccess.get_file_as_string(I18n.NAMES_PATH))
	var skills: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/skills.json")
	)
	for name in Profile.HERO_CLASSES + skills.names:
		for locale in I18n.LOCALES:
			check(t[locale].get(name, "") != "", "%s has no %s name" % [name, locale])


func test_a_name_in_the_players_language() -> void:
	var before := TranslationServer.get_locale()
	TranslationServer.set_locale("uk")
	eq(String(TranslationServer.translate("Cossack")), "Козак", "a hero class")
	eq(String(TranslationServer.translate("Whirlwind Sabre")), "Шабля-вихор", "a skill")
	TranslationServer.set_locale(before)


func test_every_item_has_a_name_in_every_language() -> void:
	var t := I18n.parse(FileAccess.get_file_as_string(I18n.NAMES_PATH))
	var items: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/items.json")
	)
	for part in items.values():
		for item in part.values():
			for locale in I18n.LOCALES:
				check(
					t[locale].get(str(item.name), "") != "",
					"%s has no %s name" % [item.name, locale]
				)


func test_campaign_names_in_every_language() -> void:
	var t := I18n.parse(FileAccess.get_file_as_string(I18n.NAMES_PATH))
	var c: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/campaign.json"))
	var names: Array = []
	for part in ["lords", "generals"]:
		for v in c[part].values():
			names.append(str(v.name))
	for m in c.missions:
		if str(m.name) != "":
			names.append(str(m.name))
	for name in names:
		for locale in I18n.LOCALES:
			check(t[locale].get(name, "") != "", "%s has no %s name" % [name, locale])


func test_story_texts_in_the_players_language() -> void:
	var t := I18n.parse(FileAccess.get_file_as_string(I18n.STORY_PATH))
	check(t["en"].size() > 500, "the story texts are there: %d" % t["en"].size())
	for key in t["en"]:
		check(t["uk"].get(key, "") != "", "%s has no uk text" % key)
	var before := TranslationServer.get_locale()
	TranslationServer.set_locale("uk")
	eq(
		Stories.pages(Stories.OPENING, "Лесь")[2].text,
		"[Настоятель] Отже, ти знайшов дорогу до Мотронинського монастиря.",
		"the prior's first line"
	)
	eq(EndingsScreen.title(0), "Довга дорога", "an ending's title")
	eq(MapSim.talk_lines("map")[21], "& is here!", "the data stays English")
	eq(
		I18n.text(MapSim.talk_lines("map")[21]),
		"& тут!",
		"and I18n.text gives the player's language"
	)
	TranslationServer.set_locale(before)
