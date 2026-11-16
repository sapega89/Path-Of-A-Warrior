extends "res://tests/test_case.gd"
## The game runs on its own files: no folder of old pictures and sounds, and no scene, script,
## resource or data file that points into one.

const OLD_FOLDER := "res://assets/original"
const LOOKED_IN: Array[String] = [
	"res://scenes", "res://screens", "res://scripts", "res://assets", "res://data", "res://lab"
]
const TEXT_FILES: Array[String] = ["gd", "tscn", "tres", "gdshader", "gdshaderinc", "json"]


func test_no_old_folder() -> void:
	check(not DirAccess.dir_exists_absolute(OLD_FOLDER), "assets/original is gone")


func test_nothing_points_into_it() -> void:
	var files: Array[String] = []
	for dir in LOOKED_IN:
		_text_files(dir, files)
	check(files.size() > 100, "the files were read")
	for path in files:
		check(not FileAccess.get_file_as_string(path).contains(OLD_FOLDER), path)


func test_the_sounds_are_ours() -> void:
	check(Audio.SFX_PATH.begins_with("res://assets/sound/"), "the effects made in code")


func _text_files(dir: String, out: Array[String]) -> void:
	for sub in DirAccess.get_directories_at(dir):
		_text_files(dir.path_join(sub), out)
	for file in DirAccess.get_files_at(dir):
		if file.get_extension() in TEXT_FILES:
			out.append(dir.path_join(file))
