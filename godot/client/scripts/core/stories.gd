class_name Stories
extends RefCounted
## The stories of data/stories.json as pages: the opening of a new game (OPENING) and the 24
## endings. A page is {kind: "talk", speaker, text} (speaker: a portrait, HERO for the hero),
## {kind: "picture", picture, text} (a picture of assets/art/story, from 0) or {kind: "stats"},
## the last page of an ending: how much of the game is done.

const PATH := "res://data/stories.json"
const OPENING := 100
const HERO := -1
const NOFACE := 0
## The hero's portraits by head (imgchar 38..41).
const HERO_PORTRAIT := 38
## The lords of the hidden missions are the ones whose bit is clear here.
const SHOWN_LORDS := 0x1FEF64FF7E6F
const MISSIONS := 102
const HIDDEN_MISSIONS := 18
const ENDINGS := 24
const GENERALS := 44

static var _data: Dictionary = {}


static func data() -> Dictionary:
	if _data.is_empty():
		var f := FileAccess.open(PATH, FileAccess.READ)
		if f != null:
			var d: Variant = JSON.parse_string(f.get_as_text())
			if typeof(d) == TYPE_DICTIONARY:
				_data = d
	return _data


## The pages of a story, in order, in the player's language (I18n.text). The hero's lines
## carry his name, the master's the name of his office (strings.json story.master).
static func pages(story: int, hero_name: String) -> Array:
	var out: Array = []
	var d := data()
	if story == OPENING:
		var lines: Array = d.get("opening", [])
		for i in lines.size():
			if i < 2:
				out.append(
					{"kind": "picture", "picture": 1 if i == 0 else 10, "text": I18n.text(lines[i])}
				)
			elif i % 2 == 0:
				out.append(
					{
						"kind": "talk",
						"speaker": NOFACE,
						"text":
						(
							"[%s] %s"
							% [TranslationServer.translate("story.master"), I18n.text(lines[i])]
						)
					}
				)
			else:
				out.append(
					{
						"kind": "talk",
						"speaker": HERO,
						"text": "[%s] %s" % [hero_name, I18n.text(lines[i])]
					}
				)
		return out
	var endings: Array = d.get("endings", [])
	if story < 0 or story >= endings.size():
		return out
	var gamestr: Array = d.get("gamestr", ["", ""])
	var talk: Array = endings[story].get("talk", [])
	for i in talk.size():
		var line := str(talk[i])
		if story == 0 and i == 2:
			out.append({"kind": "talk", "speaker": NOFACE, "text": I18n.text(gamestr[1])})
		elif _numbered(line):
			var parts := _split(line)
			out.append({"kind": "talk", "speaker": parts[0], "text": I18n.text(parts[1])})
		else:
			out.append(
				{"kind": "talk", "speaker": HERO, "text": "[%s] %s" % [hero_name, I18n.text(line)]}
			)
	var pictures: Array = endings[story].get("pictures", [])
	for i in pictures.size():
		if story == 0 and i == 0:
			out.append({"kind": "picture", "picture": 0, "text": I18n.text(gamestr[0])})
		else:
			var parts := _split(str(pictures[i]))
			out.append(
				{"kind": "picture", "picture": int(parts[0]) - 1, "text": I18n.text(parts[1])}
			)
	out.append({"kind": "stats"})
	return out


## The lines of the last page of an ending: missions, hidden missions, endings and generals
## done, in per cent, and their average.
static func stats_lines(profile: RefCounted) -> Array:
	var missions := 0
	var hidden := 0
	for key in profile.done:
		missions += 1
		var lord := int(str(key).get_slice(":", 0))
		if lord >= 1 and SHOWN_LORDS & (1 << (lord - 1)) == 0:
			hidden += 1
	var endings := 0
	for i in ENDINGS:
		if profile.endings & (1 << i) != 0:
			endings += 1
	var m := missions * 100 / MISSIONS
	var h := hidden * 100 / HIDDEN_MISSIONS
	var e := endings * 100 / ENDINGS
	var g: int = profile.friendship.size() * 100 / GENERALS
	return [
		"Mission",
		"Accomplished",
		"%d %%" % m,
		"Hidden Mission",
		"Accomplished",
		"%d %%" % h,
		"Ending Collected",
		"%d %%" % e,
		"Warrior Collected",
		"%d %%" % g,
		"Total Accomplished",
		"%d %%" % ((m + h + e + g) >> 2)
	]


static func _numbered(line: String) -> bool:
	return not line.is_empty() and line[0] >= "0" and line[0] <= "9"


## "12|text" -> [12, "text"]; a line with no "|" is all number.
static func _split(line: String) -> Array:
	var bar := line.find("|")
	if bar < 0:
		return [int(line), ""]
	return [int(line.substr(0, bar)), line.substr(bar + 1)]
