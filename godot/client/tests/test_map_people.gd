extends "res://tests/test_case.gd"
## The people of a mission in the new art (scripts/world/map_people.gd, motion.gd): every action
## has a clip, the figures follow the simulation, the sides come from the generals.

const MapSim := preload("res://scripts/sim/map_sim.gd")
const MapBuilder := preload("res://scripts/world/map_builder.gd")
const MapPeople := preload("res://scripts/world/map_people.gd")
const Motion := preload("res://scripts/world/motion.gd")
const ArtKit := preload("res://scripts/art/art_kit.gd")
const MissionScreen := preload("res://scripts/screens/mission_screen.gd")


func _sim() -> RefCounted:
	return MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))


func test_every_action_has_a_clip() -> void:
	var lib := ArtKit.clips()
	for action in range(0, 31):
		var m := Motion.hero(action, 1.5)
		check(lib.has_animation(m[0]), "hero action %d: %s" % [action, m[0]])
		check(m[1] in ["loop", "fit", "once"], "hero action %d: mode %s" % [action, m[1]])
	for type in [MapSim.KIND_SWORDS, MapSim.KIND_ARCHERS, MapSim.KIND_SQUAD, 5]:
		for action in range(0, 22 if type < 200 else 4):
			var m := Motion.enemy(type, action, 1.0)
			check(lib.has_animation(m[0]), "enemy %d action %d: %s" % [type, action, m[0]])


func test_what_the_actions_look_like() -> void:
	eq(Motion.hero(0)[0], "idle", "standing")
	eq(Motion.hero(1, 1.9)[0], "walk", "walking")
	eq(Motion.hero(2, 7.0)[0], "run", "running")
	eq(Motion.hero(3)[0], "attack_slash", "the first blow of the combo")
	eq(Motion.hero(4)[0], "attack_sweep", "the second")
	eq(Motion.hero(8)[0], "attack_chop", "the third, with the other blade")
	eq(Motion.hero(9)[1], "once", "a hit plays once")
	eq(Motion.hero(10)[0], "death", "the fall")
	eq(Motion.enemy(MapSim.KIND_ARCHERS, 1)[0], "shoot_bow", "an archer shoots")
	eq(Motion.enemy(MapSim.KIND_SWORDS, 0, 0.0)[0], "idle", "a soldier standing")
	eq(Motion.enemy(MapSim.KIND_SWORDS, 0, 1.8)[0], "walk", "a soldier walking")
	eq(Motion.enemy(MapSim.KIND_SWORDS, 2, 0.0, true)[0], "hit_heavy", "knocked back")
	eq(Motion.enemy(5, 7), Motion.hero(13), "a general's skill is the hero's")
	check(Motion.hero(1, 3.8)[2] > Motion.hero(1, 1.9)[2], "a quicker step plays quicker")


func test_turns_follow_the_eight_directions() -> void:
	var dx: Array = MapSim.table("dir_dx8")
	var dy: Array = MapSim.table("dir_dy8")
	for d in 8:
		var want := atan2(float(dx[d]), float(dy[d]))
		check(is_equal_approx(wrapf(Motion.yaw_of(d) - want, -PI, PI), 0.0), "direction %d" % d)


func test_sides_of_the_generals() -> void:
	eq(MapPeople.side_of(1), "crown", "Zdzislaw Krzeminski")
	eq(MapPeople.side_of(7), "horde", "Kara-murza")
	eq(MapPeople.side_of(5), "cossack", "Andrii Nedolia")
	eq(MapPeople.side_of_general(MapSim.general_data(24)), "horde", "Ahmat-bey by his data")


func test_the_hero_by_class_and_blade() -> void:
	var sim := _sim()
	var people: Node3D = MapPeople.new()
	root.add_child(people)
	people.setup(sim, 2)
	eq(people.hero.kind, "kharakternyk", "the third class")
	check(people.hero.skeleton.find_child("sabre", true, false) != null, "a sabre")
	people.set_hero_look(1, 1)
	eq(people.hero.kind, "serdiuk", "another class")
	check(people.hero.skeleton.find_child("palash", true, false) != null, "the broadsword")
	check(people.hero.skeleton.find_child("sabre", true, false) == null, "and no sabre")
	people.free()


func test_figures_follow_the_simulation() -> void:
	var sim := _sim()
	sim.mission_general = 24  # a mission of the horde
	var people: Node3D = MapPeople.new()
	root.add_child(people)
	people.setup(sim, 0)
	eq(people.side, "horde", "the mission's side")
	var e = sim.create_enemy(MapSim.KIND_ARCHERS, 4, 7, 0)
	people.update(1.0, 0.0, 0.12, null)
	var node: Node3D = people.enemies[e]
	eq(node.get_child_count(), 1, "one archer")
	eq(node.get_child(0).kind, "tatar_luk", "a horde archer")
	check(node.position.distance_to(MapPeople.to_world(Vector2(e.pos))) < 0.01, "on his place")
	sim.hero.action = 3
	sim.hero.frame = 0
	people.update(0.5, 0.05, 0.12, null)
	eq(people.hero.shown_clip, "attack_slash", "the hero strikes")
	sim.hero.action = 1
	people.update(0.5, 0.05, 0.12, null)
	eq(people.hero.shown_clip, "attack_slash", "a step does not cut the blow off")
	people.hero.advance(1.0)
	people.update(0.6, 0.05, 0.12, null)
	eq(people.hero.shown_clip, "walk", "then he walks")
	sim.enemies.erase(e)
	people.update(1.0, 0.0, 0.12, null)
	check(not people.enemies.has(e), "the one gone is taken away")
	people.free()


func test_a_squad_is_three() -> void:
	var sim := _sim()
	var people: Node3D = MapPeople.new()
	root.add_child(people)
	people.setup(sim, 0)
	var e = sim.create_enemy(MapSim.KIND_SWORDS, 4, 7, 0)
	e.type = MapSim.KIND_SQUAD
	people.update(1.0, 0.0, 0.12, null)
	eq(people.enemies[e].get_child_count(), 3, "three men")
	people.free()


func test_the_mission_draws_figures() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = MissionScreen.new()
	root.add_child(screen)
	screen.set_process(false)
	eq(screen.hero.kind, "kozak", "the hero as a figure")
	eq(screen.people.side, "cossack", "mission 1: a rival colonel's men")
	for i in 40:
		screen._process(screen.tick)
	eq(screen.people.enemies.size(), screen.sim.enemies.size(), "a figure for each enemy")
	screen.queue_free()
	Router.params = old
