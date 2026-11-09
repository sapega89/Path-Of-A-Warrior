extends Node
## Runs every tests/test_*.gd and quits with exit code 1 if anything failed. A test that hits
## a script error (a wrong type, a missing property: GDScript goes on after it) fails too.
##   godot --headless --path godot/client --import
##   godot --headless --path godot/client res://tests/runner.tscn

const TEST_DIR := "res://tests/"


## Counts the script errors and their first lines.
class ScriptErrors:
	extends Logger
	var count := 0
	var first := ""

	func _log_error(
		_function: String,
		file: String,
		line: int,
		code: String,
		rationale: String,
		_editor_notify: bool,
		error_type: int,
		_backtraces: Array[ScriptBacktrace]
	) -> void:
		if error_type != ERROR_TYPE_SCRIPT:
			return
		count += 1
		if first.is_empty():
			first = "%s:%d %s" % [file, line, rationale if not rationale.is_empty() else code]


func _ready() -> void:
	await get_tree().process_frame
	var failed := 0
	var passed := 0
	var errors := ScriptErrors.new()
	OS.add_logger(errors)
	for file in DirAccess.get_files_at(TEST_DIR):
		if not (file.begins_with("test_") and file.ends_with(".gd")) or file == "test_case.gd":
			continue
		var script: GDScript = load(TEST_DIR + file)
		if script == null or not script.can_instantiate():
			print("FAIL %s: does not compile" % file)
			failed += 1
			continue
		for m in script.get_script_method_list():
			var method: String = m.name
			if not method.begins_with("test_"):
				continue
			var test: RefCounted = script.new()
			test.root = self
			test.current = "%s:%s" % [file, method]
			errors.count = 0
			errors.first = ""
			test.call(method)
			if errors.count > 0:
				test.failures.append(
					"%s: %d script error(s), first: %s" % [test.current, errors.count, errors.first]
				)
			if test.failures.is_empty():
				passed += 1
				print("ok   %s" % test.current)
			else:
				failed += 1
				for f in test.failures:
					print("FAIL %s" % f)
	print("\n%d passed, %d failed" % [passed, failed])
	get_tree().quit(1 if failed > 0 else 0)
