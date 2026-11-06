extends Node
## Runs every tests/test_*.gd and quits with exit code 1 if anything failed.
##   godot --headless --path godot/client --import
##   godot --headless --path godot/client res://tests/runner.tscn

const TEST_DIR := "res://tests/"


func _ready() -> void:
	await get_tree().process_frame
	var failed := 0
	var passed := 0
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
			test.call(method)
			if test.failures.is_empty():
				passed += 1
				print("ok   %s" % test.current)
			else:
				failed += 1
				for f in test.failures:
					print("FAIL %s" % f)
	print("\n%d passed, %d failed" % [passed, failed])
	get_tree().quit(1 if failed > 0 else 0)
