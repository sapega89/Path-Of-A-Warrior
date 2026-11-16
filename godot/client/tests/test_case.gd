extends RefCounted
## Base class of the tests: methods named test_* are run by runner.gd.

## The tests' own small maps (tests/maps/<name>.json): the tests play these, never the maps of the
## campaign, so a change of the campaign's maps breaks no test about something else.
## three_rooms: a column of three rooms, the dirt path down the middle; the first room open on
## every side, the other two between stone walls (the last open on the left too), a walled
## nook in the middle one; two missions, the archers of the second in the middle room.
## terrain: two rooms across, a cliff with a pit in its top, a river with a log bridge, tents.
const OWN_MAPS := "res://tests/maps/"

var failures: Array[String] = []
var current := ""
## The runner's node, for tests that need the scene tree.
var root: Node


func check(condition: bool, message: String = "") -> void:
	if not condition:
		failures.append("%s: %s" % [current, message])


func eq(actual: Variant, expected: Variant, message: String = "") -> void:
	if typeof(actual) != typeof(expected) or actual != expected:
		failures.append(
			(
				"%s: %s expected %s, got %s"
				% [current, message, var_to_str(expected), var_to_str(actual)]
			)
		)


## Moves a Dialogue's typing (and the stay after the line) `seconds` on, as frames would.
func step_dialogue(dialogue: Dialogue, seconds: float) -> void:
	if dialogue.tween != null and dialogue.tween.is_valid():
		dialogue.tween.custom_step(seconds)


static func own_map_path(name: String) -> String:
	return OWN_MAPS + name + ".json"


## One of the tests' own maps (OWN_MAPS).
static func own_map(name: String) -> Dictionary:
	return MapBuilder.load_map_file(own_map_path(name))
