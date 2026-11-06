extends RefCounted
## The original campaign tables (data/campaign.json, made by godot/tools/import_original.py):
## chapters list the lords you can fight for, each lord has one map and a run of missions.

const PATH := "res://data/campaign.json"

var chapters: Array = []
var lords: Dictionary = {}
var missions: Array = []


func _init() -> void:
	var f := FileAccess.open(PATH, FileAccess.READ)
	if f == null:
		return
	var data: Variant = JSON.parse_string(f.get_as_text())
	if typeof(data) != TYPE_DICTIONARY:
		return
	chapters = data.get("chapters", [])
	lords = data.get("lords", {})
	missions = data.get("missions", [])


func lord(id: int) -> Dictionary:
	return lords.get(str(id), {})


func lord_name(id: int) -> String:
	return str(lord(id).get("name", "?"))


## Lord ids of a chapter (0-based).
func chapter_lords(chapter: int) -> Array:
	if chapter < 0 or chapter >= chapters.size():
		return []
	return chapters[chapter]


## The missions of a lord, in order: their index in the list is the mission number on the
## lord's map (which room data and start position it uses).
func lord_missions(id: int) -> Array:
	var l := lord(id)
	var first := int(l.get("first_mission", 0))
	var n := int(l.get("missions", 0))
	return missions.slice(first, first + n)


## The map of a lord is the map with the lord's number.
static func lord_map(id: int) -> int:
	return id
