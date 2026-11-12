extends "res://tests/test_case.gd"
## Every scene of the game keeps all its nodes in the exported game. The export saves each scene
## again from an instance of it, and a node put inside another scene's instance (the camp's hero
## in World/Viewport/WorldRoot of the map view, the key letter of a belt slot) is saved only when
## that instance is editable: [editable path="World"] at the end of the .tscn. Without it the game
## runs from the editor, but the exported one loses the node.

const DIRS: Array[String] = ["res://scenes", "res://screens"]


func test_every_scene_keeps_its_nodes_when_saved_again() -> void:
	var count := 0
	for d in DIRS:
		for path in _scenes(d):
			var scene: PackedScene = load(path)
			var node: Node = scene.instantiate(PackedScene.GEN_EDIT_STATE_INSTANCE)
			var again := PackedScene.new()
			again.pack(node)
			node.free()
			var kept := _nodes(again.get_state())
			for n in _nodes(scene.get_state()):
				check(n in kept, "%s keeps %s" % [path, n])
			count += 1
	check(count > 50, "found %d scenes" % count)


## The paths of a scene's nodes, without the "./" that a saved scene puts before some of them.
func _nodes(state: SceneState) -> Array[String]:
	var paths: Array[String] = []
	for i in state.get_node_count():
		paths.append(str(state.get_node_path(i)).trim_prefix("./"))
	return paths


func _scenes(dir: String) -> Array[String]:
	var found: Array[String] = []
	for f in DirAccess.get_files_at(dir):
		if f.ends_with(".tscn"):
			found.append(dir.path_join(f))
	for sub in DirAccess.get_directories_at(dir):
		found.append_array(_scenes(dir.path_join(sub)))
	return found
