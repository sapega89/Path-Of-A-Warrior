extends "res://tests/test_case.gd"
## The combat feel lab (lab/combat_feel.gd, lab/combat_feel_lab.gd): the hits it sees, the
## hitstop and its limit, the shake and the flash fading, and the arena running by itself.

const MapBuilder := preload("res://scripts/world/map_builder.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")
const JavaRandom := preload("res://scripts/sim/java_random.gd")
const CombatFeel := preload("res://lab/combat_feel.gd")


## An empty, open room with one swordsman standing below the hero, looking at him.
func _duel() -> Array:
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	sim.rng = JavaRandom.new(1)
	sim.no_enemies = true
	for t in 200:
		if sim.exits_open():
			break
		sim.tick(-1, -1, sim.banner != 0)
	var e = sim.create_enemy(MapSim.KIND_SWORDS, 4, 7, 0)
	e.type = MapSim.KIND_SWORDS
	e.pos = sim.hero.pos + Vector2i(0, 30)
	e.alerted = 1
	e.think_ticks = 100
	sim.hero.facing = 0
	sim.hero.dir = 0
	return [sim, e]


## Strikes until the swordsman is hit: the hits of that tick.
func _strike(sim: RefCounted) -> Array:
	for t in 12:
		var before := CombatFeel.snapshot(sim)
		sim.tick(-1, -1, t == 0)
		var list := CombatFeel.hits(sim, before)
		if not list.is_empty():
			return list
	return []


func test_a_strike_is_one_hit_away_from_the_hero() -> void:
	var d := _duel()
	var list := _strike(d[0])
	eq(list.size(), 1, "one hit")
	if list.is_empty():
		return
	var h: Dictionary = list[0]
	eq(h.who, "enemy", "on the swordsman")
	check(h.actor == d[1], "that swordsman")
	check(h.dir.y > 0.9, "away from the hero (down): %s" % h.dir)
	eq(CombatFeel.grade(h), "hit", "an ordinary hit")


func test_a_kill_is_seen() -> void:
	var d := _duel()
	d[1].hp = 1
	var list := _strike(d[0])
	check(not list.is_empty() and list[0].killed, "killed")
	if not list.is_empty():
		eq(CombatFeel.grade(list[0]), "kill", "graded a kill")


func test_the_hero_hit_is_seen() -> void:
	var d := _duel()
	var sim: RefCounted = d[0]
	var before := CombatFeel.snapshot(sim)
	sim.hero_is_hit(d[1])
	var list := CombatFeel.hits(sim, before)
	eq(list.size(), 1, "one hit")
	if not list.is_empty():
		eq(CombatFeel.grade(list[0]), "hurt", "the hero is hurt")


func _kill_on(actor) -> Dictionary:
	return {"who": "enemy", "actor": actor, "pos": Vector2i.ZERO, "dir": Vector2.DOWN,
		"killed": true, "heavy": false, "boss": false}


func test_the_strongest_hit_of_a_tick_sets_the_stop() -> void:
	var f := CombatFeel.new()
	var a := RefCounted.new()
	var b := RefCounted.new()
	var hit := _kill_on(a)
	hit.killed = false
	f.react([hit, _kill_on(b)])
	check(is_equal_approx(f.freeze, float(f.p.stop_kill)), "the kill's stop, not the sum: %f" % f.freeze)
	check(is_equal_approx(f.trauma, float(f.p.trauma_kill)), "the kill's shake, not the sum: %f" % f.trauma)
	eq(f.flashes.size(), 2, "both flash")
	check(f.launches.has(b) and f.recoils.has(a), "the killed flies, the hit recoils")


func test_the_stop_has_a_limit() -> void:
	var f := CombatFeel.new()
	var total := 0.0
	for i in 10:
		f.freeze = 0.0
		f.react([_kill_on(RefCounted.new())])
		total += f.freeze
	check(total <= float(f.p.stop_budget) + 0.0001, "ten kills at once stop at most %f s: %f" % [f.p.stop_budget, total])


func test_shake_and_flash_fade() -> void:
	var f := CombatFeel.new()
	var a := RefCounted.new()
	f.react([_kill_on(a)])
	check(f.camera_shake() != Vector3.ZERO or f.trauma > 0.0, "it shakes")
	check(f.flash_of(a)[0] > 0.9, "white at once")
	for i in 120:
		f.advance(1.0 / 60.0)
	eq(f.trauma, 0.0, "the shake is over after 2 s")
	eq(f.flash_of(a)[0], 0.0, "the flash is over")
	var o := f.offset_of(a)
	check(Vector2(o.x, o.y).length() > float(f.p.launch_px) * 0.9, "he flew off: %s" % o)


func test_the_flight_waits_while_the_picture_stands() -> void:
	var f := CombatFeel.new()
	var a := RefCounted.new()
	f.react([_kill_on(a)])
	check(f.freeze > 0.0, "a stop")
	f.advance(0.01)
	eq(f.offset_of(a), Vector3.ZERO, "frozen: not moved yet")


func test_switched_off_does_nothing() -> void:
	var f := CombatFeel.new()
	for k in f.on:
		f.on[k] = false
	var a := RefCounted.new()
	f.react([_kill_on(a)])
	eq(f.freeze, 0.0, "no stop")
	eq(f.trauma, 0.0, "no shake")
	check(f.flashes.is_empty() and f.launches.is_empty() and f.recoils.is_empty(), "no flash, no flight")


## The arena fights by itself (auto-hunt) for a minute of ticks: the hero stays in its room,
## does not die, and the soldiers keep coming and get hit.
func test_the_arena_runs() -> void:
	var lab: Control = load("res://lab/combat_feel_lab.tscn").instantiate()
	lab.seed = 3
	root.add_child(lab)
	lab.set_process(false)
	lab.autopilot.on = true
	var cell: int = lab.sim.cell
	var hits := 0
	for t in 500:
		var before := CombatFeel.snapshot(lab.sim)
		lab._tick(-1)
		hits += CombatFeel.hits(lab.sim, before).size()
		lab.feel.freeze = 0.0
	eq(lab.sim.cell, cell, "still in its room")
	check(lab.sim.enemies.size() > 0, "soldiers there")
	check(lab.sim.hero.hp > 0, "the hero alive")
	check(hits > 5, "hits seen: %d" % hits)
	lab.free()
