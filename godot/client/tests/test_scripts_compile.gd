extends "res://tests/test_case.gd"
## Every script of the project compiles, also the tools and the lab that no other test runs.

const DIRS: Array[String] = ["res://scripts", "res://screens", "res://tools", "res://lab"]


func test_every_script_compiles() -> void:
	var count := 0
	for d in DIRS:
		for path in _scripts(d):
			var script: GDScript = load(path)
			check(script != null and script.can_instantiate(), "%s compiles" % path)
			count += 1
	check(count > 100, "found %d scripts" % count)


func _scripts(dir: String) -> Array[String]:
	var found: Array[String] = []
	for f in DirAccess.get_files_at(dir):
		if f.ends_with(".gd"):
			found.append(dir.path_join(f))
	for sub in DirAccess.get_directories_at(dir):
		found.append_array(_scripts(dir.path_join(sub)))
	return found
