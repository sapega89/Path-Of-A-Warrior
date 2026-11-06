extends "res://tests/test_case.gd"

const MapBuilder := preload("res://scripts/world/map_builder.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")
const JavaRandom := preload("res://scripts/sim/java_random.gd")


## Mission 1 of lord 1 on map 1, the same random numbers every run.
func _sim(enemies: bool = true) -> RefCounted:
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	sim.rng = JavaRandom.new(1)
	sim.no_enemies = not enemies
	return sim


## An empty, open room with one swordsman standing below the hero.
func _duel() -> Array:
	var sim := _sim(false)
	for t in 200:
		if sim.exits_open():
			break
		sim.tick(-1, -1, sim.banner != 0)  # the key closes a banner (in the room it strikes)
	var e = sim.create_enemy(MapSim.KIND_SWORDS, 4, 7, 0)
	e.type = MapSim.KIND_SWORDS
	e.pos = sim.hero.pos + Vector2i(0, 30)
	e.alerted = 1
	e.think_ticks = 100  # does not choose an action during the test
	sim.hero.facing = 0
	sim.hero.dir = 0
	return [sim, e]


func test_random_numbers() -> void:
	var r := JavaRandom.new(42)
	eq(r.next_int(), -1170105035, "first number of seed 42")
	eq(r.next_int(), 234785527, "second number")
	for i in 100:
		var v := r.below(7)
		if v < 0 or v > 6:
			check(false, "below(7) out of range: %d" % v)
			break


func test_directions_and_distance() -> void:
	eq(MapSim.distance(Vector2i(0, 0), Vector2i(30, 40)), 50, "3-4-5")
	eq(MapSim.dir4(Vector2i(0, 0), Vector2i(0, 30)), 0, "down")
	eq(MapSim.dir4(Vector2i(0, 0), Vector2i(-30, 5)), 2, "left")
	eq(MapSim.dir8(Vector2i(0, 0), Vector2i(10, 30)), 0, "almost down")
	eq(MapSim.dir8(Vector2i(0, 0), Vector2i(30, 30)), 7, "down right")


func test_spawn_spots_on_the_open_exit() -> void:
	var sim := _sim()
	check(sim.spawn_spots.size() > 0, "room 1 has places to come in")
	for s in sim.spawn_spots:
		eq(s.z, 0, "room 1 opens down only")
		eq(s.y, 7, "the bottom row of the room")


func test_soldiers_come_in() -> void:
	var sim := _sim()
	var most := 0
	var first_y := -1
	for t in 80:
		sim.tick(-1, -1, true)
		if first_y == -1 and sim.enemies.size() > 0:
			first_y = sim.enemies[0].pos.y
		most = maxi(most, sim.enemies.size())
	check(first_y > MapSim.edge(1), "the first one starts outside, below the room: %d" % first_y)
	check(most > 0 and most <= sim.max_enemies(), "at most the room's maximum at once: %d" % most)
	for e in sim.enemies:
		check(e.type == MapSim.KIND_SWORDS or e.type == MapSim.KIND_SQUAD, "room 1 sends swords")
	check(not sim.exits_open(), "the room stays closed while they live")


func test_sword_hits() -> void:
	var d := _duel()
	var sim: RefCounted = d[0]
	var e = d[1]
	var hp: int = e.hp
	sim.tick(-1, -1, true)
	check(sim.hero.action >= 3 and sim.hero.action <= 8, "a sword action: %d" % sim.hero.action)
	sim.tick(-1, -1)
	check(e.hp < hp, "the strike took HP: %d -> %d" % [hp, e.hp])
	eq(e.action, 2, "the soldier reels")
	eq(sim.target_info.get("name", ""), "Swords", "the target's name is shown")


func test_last_enemy_clears_the_room() -> void:
	var d := _duel()
	var sim: RefCounted = d[0]
	var e = d[1]
	sim.room_phase = 0
	e.hp = 1
	sim.tick(-1, -1, true)
	sim.tick(-1, -1)
	eq(e.hp, 0, "struck down")
	var cleared := false
	for t in 40:
		sim.tick(-1, -1)
		if sim.banner == MapSim.BANNER_STAGE_CLEAR:
			cleared = true
			break
	check(sim.enemies.is_empty(), "the body is gone")
	eq(sim.kills, 1, "one kill")
	check(cleared, "Stage Complete")


func test_hero_falls() -> void:
	var d := _duel()
	var sim: RefCounted = d[0]
	sim.hero.hp = 1
	sim.hero_is_hit(d[1])
	eq(sim.hero.hp, 0, "no HP left")
	eq(sim.hero.action, 10, "falls")
	for t in 30:
		sim.tick(-1, -1)
	eq(sim.banner, MapSim.BANNER_FAILED, "Mission fail!")
	check(not sim.finished, "waits for a key")
	sim.tick(-1, -1, true)
	check(sim.finished, "a key ends the mission")


func test_barrel_breaks() -> void:
	var sim := _sim(false)
	for t in 200:
		if sim.exits_open():
			break
		sim.tick(-1, -1, sim.banner != 0)
	var barrel = null
	for b in sim.breakables:
		if b.tile == Vector2i(4, 6):
			barrel = b
	check(barrel != null, "the barrel at (4, 6) is in the room")
	if barrel == null:
		return
	eq(barrel.hp, 41, "a barrel takes 41")
	sim.hero.pos = Vector2i(120, 150)
	sim.hero.facing = 0
	sim.hero.dir = 0
	for t in 120:
		sim.tick(-1, -1, t % 4 == 0)
		if barrel.hp < 1:
			break
	check(barrel.hp < 1, "broken by the sword: %d" % barrel.hp)
	eq(int(sim.objects[6 * sim.w + 4]), 0, "the cell is free")
	for t in 13:
		sim.tick(-1, -1)
	check(not barrel.active, "gone after blinking")


func test_gold_is_picked_up() -> void:
	var sim := _sim(false)
	var d = MapSim.Drop.new()
	d.item = 10020
	d.pos = sim.hero.pos
	sim.drops.append(d)
	sim.tick(-1, -1)
	sim.tick(-1, -1)
	eq(sim.gold, 20, "20 gold")
	check(sim.drops.is_empty(), "nothing left on the floor")
