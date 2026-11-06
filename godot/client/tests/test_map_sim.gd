extends "res://tests/test_case.gd"

const MapBuilder := preload("res://scripts/world/map_builder.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")


func _sim() -> RefCounted:
	return MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))


## Ticks until the room's exits are open (banners skipped with fire).
func _open(sim: RefCounted) -> int:
	for t in 200:
		if sim.exits_open():
			return t
		sim.tick(-1, -1, true)
	return -1


func test_tables_loaded() -> void:
	eq(MapSim.table("dir_dx8").size(), 9, "dir_dx8")
	eq(MapSim.table("hero_anim_1").size(), 4, "walk table per dir4")


func test_room_opens_after_banners() -> void:
	var sim := _sim()
	eq(sim.cell, 0, "starts in room 1")
	var t := _open(sim)
	check(t > 0, "exits open after the Stage and Stage Complete banners")
	eq(sim.rooms_visited, 1, "first room")


func test_walk_and_stand() -> void:
	var sim := _sim()
	_open(sim)
	var start: Vector2i = sim.hero.pos
	sim.tick(6, -1)  # hold right
	eq(sim.hero.action, 1, "walking")
	eq(sim.hero.pos.x - start.x, 6, "6 px per tick to the right")
	sim.tick(-1, -1)  # released
	eq(sim.hero.action, 0, "stands when released (hold to move)")


func test_walls_stop_the_step() -> void:
	var sim := _sim()
	# The house of map 1 is blocked at x 7..8, y 10..12; 2 px fit before it.
	eq(sim.step_until_free(Vector2i(174, 317), 6, 6), 2, "shortened before the wall")
	eq(sim.step_until_free(Vector2i(120, 74), 6, 6), 6, "free floor")


func test_walk_down_into_the_next_room() -> void:
	var sim := _sim()
	_open(sim)
	for t in 200:
		sim.tick(0, -1, true)
		if sim.rooms_visited == 2:
			break
	if sim.cell != 1:
		print("walk down: pos ", sim.hero.pos, " action ", sim.hero.action, " phase ", sim.room_phase,
			" timer ", sim.room_phase_timer, " banner ", sim.banner, " scrolling ", sim.scrolling)
	eq(sim.cell, 1, "in room 2")
	eq(sim.rooms_visited, 2, "second stage")
	var b: Rect2 = sim.rooms.bounds(1)
	check(sim.hero.pos.y / 27.0 >= b.position.y - 0.01, "pushed inside the new room")


func test_run_on_double_tap() -> void:
	var sim := _sim()
	_open(sim)
	sim.tick(-1, 6)
	sim.tick(-1, 6)
	eq(sim.hero.action, 2, "two taps in a row: run")
