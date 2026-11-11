extends RefCounted
## Base class of the tests: methods named test_* are run by runner.gd.

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
