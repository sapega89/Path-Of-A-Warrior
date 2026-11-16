extends "res://tests/test_case.gd"


func test_all_maps_load() -> void:
	eq(MapBuilder.map_count(), 45, "map count")
	for n in range(1, 46):
		var m := MapBuilder.load_map(n)
		var size: int = int(m.w) * int(m.h)
		for layer in ["ground", "upper", "objects", "flags"]:
			eq(m[layer].size(), size, "map %d %s" % [n, layer])
		check(m.rooms.missions.size() > 0, "map %d has missions" % n)


func test_map_1_layout() -> void:
	var b: Node3D = MapArt.new()
	root.add_child(b)
	b.build(MapBuilder.load_map(1))
	eq(b.w, 9, "width")
	eq(b.h, 23, "height")
	# One collision box per blocked cell or object, plus 4 edges and the ground.
	var blocked := 0
	for y in b.h:
		for x in b.w:
			if b.is_blocked(x, y):
				blocked += 1
	eq(b.get_node("Collision").get_child_count(), blocked + 5, "collision boxes")
	eq(b.breakables.size(), 10, "breakable objects")
	var start: Vector2i = b.start_cell(0)
	check(not b.is_blocked(start.x, start.y), "start cell is free")
	b.free()
