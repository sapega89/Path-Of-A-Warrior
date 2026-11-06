extends "res://tests/test_case.gd"

const MapHud := preload("res://scripts/ui/map_hud.gd")
const MapBuilder := preload("res://scripts/world/map_builder.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")


func test_ball_fill() -> void:
	eq(MapHud._fill(30, 30), 35, "full")
	eq(MapHud._fill(0, 30), 0, "empty")
	eq(MapHud._fill(1, 30), 3, "a little is always seen")
	eq(MapHud._fill(15, 30), 17, "half")


func test_scale() -> void:
	var hud := MapHud.new()
	eq(hud.scale_of(Vector2(1280, 720)), 2.0, "720 rows: twice")
	eq(hud.scale_of(Vector2(240, 320)), 1.0, "the original size")
	hud.free()


func test_clock_and_kills() -> void:
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	sim.no_enemies = true
	for t in 200:
		sim.tick(-1, -1, sim.banner != 0)
	check(sim.play_seconds() > 0, "the clock runs: %d s" % sim.play_seconds())
	var hud := MapHud.new()
	hud.sim = sim
	sim.kills = 2
	hud.tick()
	eq(hud.kills_shown, 1, "the kills count up one a tick")
	hud.tick()
	hud.tick()
	eq(hud.kills_shown, 2, "up to the kills")
	hud.free()
