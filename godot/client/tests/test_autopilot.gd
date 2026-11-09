extends "res://tests/test_case.gd"
## Auto-hunt: it walks to the enemies and fights, drinks and heals, and leaves a cleared room.


func _sim() -> RefCounted:
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	sim.rng = JavaRandom.new(5)
	return sim


func _run(sim: RefCounted, a: RefCounted, ticks: int) -> void:
	for t in ticks:
		var d: Dictionary = a.decide(sim)
		sim.tick(int(d.held), -1, bool(d.fire) or sim.banner != 0, int(d.hotkey), -1, int(d.belt))
		if sim.finished or sim.hero.hp <= 0:
			return


func test_off_does_nothing() -> void:
	var a := Autopilot.new()
	eq(a.decide(_sim()), {"held": -1, "fire": false, "hotkey": -1, "belt": -1}, "off: no keys")


func test_clears_the_first_room() -> void:
	var sim := _sim()
	sim.hero.attack = 60  # strong enough to finish the room in the test's time
	sim.hero.max_hp = 500
	sim.hero.hp = 500
	var a := Autopilot.new()
	a.toggle()
	_run(sim, a, 1500)
	check(sim.kills > 0, "it fought: %d kills" % sim.kills)
	check(sim.exits_open() or sim.cell != 0 or sim.rooms_visited > 1, "the room cleared or left")


func test_potion_when_low() -> void:
	var sim := _sim()
	sim.quick_slots[2] = [1, 3]
	sim.hotkeys.assign([12, 0, 0, 0, 0])
	sim.hero.hp = 5
	var e = sim.create_enemy(MapSim.KIND_SWORDS, 4, 7, 0)
	e.pos = sim.hero.pos + Vector2i(100, 0)
	var a := Autopilot.new()
	a.toggle()
	eq(int(a.decide(sim).belt), 2, "an HP potion from the belt's third slot")


func test_heal_skill_first() -> void:
	var sim := _sim()
	sim.quick_slots[0] = [1, 3]
	sim.hotkeys.assign([12, 15, 0, 0, 0])
	sim.skill_levels[3] = 1
	sim.hero.hp = 5
	var a := Autopilot.new()
	a.toggle()
	eq(int(a.decide(sim).hotkey), 1, "Healing Herbs on its key, not the potion")


func test_a_key_of_the_player_hands_off() -> void:
	var sim := _sim()
	sim.hero.hp = 5
	sim.quick_slots[0] = [1, 3]
	var a := Autopilot.new()
	a.toggle()
	a.player_key()
	eq(int(a.decide(sim).belt), -1, "waits a moment")


func test_leaves_an_archer_it_cannot_reach() -> void:
	# Lord 6's first mission, its second room: two archers, one in the room, one up in a walled
	# nook, out of the hero's reach. The room is clear and its exit open (archers do not keep it
	# shut): the hero kills the first, gives up on the second and walks out.
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(Campaign.lord_map(6)), 0, Vector2i(11, 4))
	sim.rng = JavaRandom.new(60)
	sim.continue_in_clear_room()
	sim._run_cell_scripts()
	eq(
		sim.enemies.map(func(e): return [e.type, e.pos / 27]),
		[[MapSim.KIND_ARCHERS, Vector2i(13, 2)], [MapSim.KIND_ARCHERS, Vector2i(14, 5)]],
		"the archers"
	)
	var room: int = sim.cell
	var a := Autopilot.new()
	a.toggle()
	var left := -1
	for t in 900:
		var d: Dictionary = a.decide(sim)
		sim.tick(int(d.held), -1, bool(d.fire) or sim.banner != 0, int(d.hotkey), -1, int(d.belt))
		if sim.cell != room:
			left = t
			break
	eq(sim.kills, 1, "the one in the room killed")
	check(left > 0, "out of the room after %d ticks" % left)
