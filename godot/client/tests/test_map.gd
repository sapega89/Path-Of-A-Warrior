extends "res://tests/test_case.gd"

const MapBuilder := preload("res://scripts/world/map_builder.gd")


func test_all_maps_load() -> void:
	eq(MapBuilder.map_count(), 45, "map count")
	for n in range(1, 46):
		var m := MapBuilder.load_map(n)
		var size: int = int(m.w) * int(m.h)
		for layer in ["ground", "upper", "objects", "flags"]:
			eq(m[layer].size(), size, "map %d %s" % [n, layer])
		check(m.rooms.missions.size() > 0, "map %d has missions" % n)


func test_map_1_layout() -> void:
	var b: Node3D = MapBuilder.new()
	root.add_child(b)
	b.build(MapBuilder.load_map(1))
	eq(b.w, 9, "width")
	eq(b.h, 23, "height")
	# The house at x 7..8, y 10..12 of map 1 stands up from its front row y = 12.
	check(b.standing_runs().has({"x": 7, "top": 10, "bottom": 12}), "house column")
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


func test_tile_uv() -> void:
	var uv := MapBuilder.tile_uv(1)
	check(uv.position.x < 0.001 and uv.position.y < 0.001, "tile 1 top-left")
	uv = MapBuilder.tile_uv(17)
	check(absf(uv.position.y - 1.0 / 15.0) < 0.001, "tile 17 second row")
