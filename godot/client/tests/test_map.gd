extends "res://tests/test_case.gd"


func test_all_maps_load() -> void:
	eq(MapBuilder.map_count(), 45, "map count")
	for n in range(1, 46):
		var m := MapBuilder.load_map(n)
		var size: int = int(m.w) * int(m.h)
		for layer in ["parts", "props", "objects", "flags"]:
			eq(m[layer].size(), size, "map %d %s" % [n, layer])
		check(m.rooms.missions.size() > 0, "map %d has missions" % n)
		eq(m.starts.size(), m.rooms.missions.size(), "map %d: a start for each mission" % n)
		eq(m.time_limits.size(), m.rooms.missions.size(), "map %d: a time for each mission" % n)
		for mission in m.starts.size():
			var s := MapBuilder.mission_start(m, mission)
			eq(
				int(m.flags[s.y * int(m.w) + s.x]) & 1,
				0,
				"map %d: mission %d starts free" % [n, mission]
			)


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


func test_mission_start_and_time() -> void:
	var m := MapBuilder.load_map(1)
	eq(MapBuilder.mission_start(m, 0), Vector2i(4, 2), "the first mission starts at (4, 2)")
	eq(MapBuilder.mission_time(m, 0), 192, "in 192 seconds")
	eq(MapBuilder.mission_start(m, 99), MapBuilder.DEFAULT_START, "a mission the map has not")
	eq(MapBuilder.mission_time(m, 99), 0, "no time limit then")
