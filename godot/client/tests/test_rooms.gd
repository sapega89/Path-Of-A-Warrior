extends "res://tests/test_case.gd"

const MapBuilder := preload("res://scripts/world/map_builder.gd")
const Rooms := preload("res://scripts/world/rooms.gd")
const Campaign := preload("res://scripts/core/campaign.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")


func test_map_1_rooms() -> void:
	var r: RefCounted = Rooms.new(MapBuilder.load_map(1), 0)
	eq(r.count(), 3, "map 1 is one column of 3 rooms")
	eq(r.room_at(Vector3(4.5, 0, 4.5)), 0, "top room")
	eq(r.room_at(Vector3(4.5, 0, 11.5)), 1, "middle room")
	eq(r.room_at(Vector3(4.5, 0, 20.0)), 2, "bottom room")
	eq(r.exits(0), [1.0, 0.0, 0.0, 0.0], "room 1 exits down (JSON numbers)")
	eq(r.neighbour(0, Rooms.EXIT_DOWN), 1, "down = next row")
	eq(r.waves(0), [[201, 5]], "five soldiers 201")
	check(not r.has_general(0), "no general")


func test_bounds_are_the_original_pixels() -> void:
	var r: RefCounted = Rooms.new(MapBuilder.load_map(1), 0)
	var b: Rect2 = r.bounds(0)
	# x: 27 + 12 .. 216 - 12 px, z: 27 + 10 .. 216 + 10 px
	check(absf(b.position.x - 39.0 / 27.0) < 0.001, "left")
	check(absf(b.end.x - 204.0 / 27.0) < 0.001, "right")
	check(absf(b.position.y - 37.0 / 27.0) < 0.001, "top")
	check(absf(b.end.y - 226.0 / 27.0) < 0.001, "bottom")


func test_keep_inside_reports_the_edge() -> void:
	var r: RefCounted = Rooms.new(MapBuilder.load_map(1), 0)
	var k: Dictionary = r.keep_inside(0, Vector3(4, 0, 20))
	eq(k.edge, Rooms.EXIT_DOWN, "bottom edge")
	check(absf(k.pos.z - 226.0 / 27.0) < 0.001, "kept at the bottom")
	k = r.keep_inside(0, Vector3(0, 0, 4))
	eq(k.edge, Rooms.EXIT_LEFT, "left edge")
	k = r.keep_inside(0, Vector3(4, 0, 4))
	eq(k.edge, 0, "inside")


func test_campaign_tables() -> void:
	var c: RefCounted = Campaign.new()
	eq(c.chapters.size(), 45, "chapters")
	eq(c.chapter_lords(0), [1.0], "chapter 1: lord 1")
	eq(c.lord_name(1), "Uprising", "lord 1")
	var ms: Array = c.lord_missions(1)
	eq(ms.size(), 4, "lord 1 has 4 missions")
	eq(ms[0].name, "Colonel Bairak", "first mission")
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(int(ms[0].start[0]), int(ms[0].start[1])))
	eq(sim.hero.pos, Vector2i(4 * 27 + 12, 2 * 27 + 20), "start position in pixels")
	# Every lord's map exists and its missions have room data.
	for id in c.lords:
		var map := MapBuilder.load_map(Campaign.lord_map(int(id)))
		check(not map.is_empty(), "map of lord %s" % id)
		check(map.rooms.missions.size() >= c.lord_missions(int(id)).size(), "room data for every mission of lord %s" % id)
