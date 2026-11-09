extends "res://tests/test_case.gd"
## The effects of a mission in the new art (scripts/world/map_effects.gd): every frame of
## every kind is drawn in code, the rigs are reused, room-wide strikes keep their places, the
## arrows fly their way.

const MapEffects := preload("res://scripts/world/map_effects.gd")
const MapPeople := preload("res://scripts/world/map_people.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")
const MapBuilder := preload("res://scripts/world/map_builder.gd")
const Motion := preload("res://scripts/world/motion.gd")
const MissionScreen := preload("res://scripts/screens/mission_screen.gd")


func _shown_parts(rig: Node3D) -> int:
	var n := 0
	for c in rig.get_children():
		if (c as Node3D).visible:
			n += 1
	return n


func test_every_frame_of_every_kind_is_drawn() -> void:
	var fx: Node3D = MapEffects.new()
	root.add_child(fx)
	for kind in MapEffects.FRAMES:
		for frame in int(MapEffects.FRAMES[kind]):
			for t in [0.0, 0.5, 1.0]:
				fx.show_effects([[kind, frame, Vector2i(100, 100)]], t)
				eq(fx.shown(), 1, "%s %d at %.1f" % [kind, frame, t])
				var rig: Node3D = fx.drawn[0][2]
				check(
					rig.visible and _shown_parts(rig) > 0,
					"%s %d at %.1f shows something" % [kind, frame, t]
				)
	fx.free()


func test_rigs_are_reused() -> void:
	var fx: Node3D = MapEffects.new()
	var list := [
		["spark", 0, Vector2i(10, 10)],
		["spark", 2, Vector2i(40, 10)],
		["fire", 3, Vector2i(10, 40)]
	]
	fx.show_effects(list)
	var children := fx.get_child_count()
	fx.show_effects(list, 0.5)
	eq(fx.get_child_count(), children, "the same effects again: no new nodes")
	check(fx.drawn[0][2] != fx.drawn[1][2], "two sparks, two rigs")
	fx.show_effects([["spark", 1, Vector2i(10, 10)]])
	var shown := 0
	for c in fx.get_children():
		shown += 1 if (c as Node3D).visible else 0
	eq(shown, 1, "the ones not in the list are hidden")
	fx.show_effects([])
	eq(fx.shown(), 0, "nothing")
	fx.free()


func test_effects_stand_where_the_sim_puts_them() -> void:
	var fx: Node3D = MapEffects.new()
	var p := Vector2i(135, 81)
	fx.show_effects([["fire", 4, p]])
	var ground: Node3D = fx.drawn[0][2].get_node("Ground")
	check(
		ground.position.distance_to(MapPeople.to_world(Vector2(p))) < 0.05,
		"the fire burns where he stands"
	)
	fx.show_effects([["blast", 1, p]])
	var scorch: Node3D = fx.drawn[0][2].get_node("Scorch")
	check(
		(
			Vector2(scorch.position.x, scorch.position.z).distance_to(
				Vector2(MapPeople.to_world(Vector2(p)).x, MapPeople.to_world(Vector2(p)).z)
			)
			< 0.05
		),
		"a scroll's blast lands on its point"
	)
	fx.free()


func test_room_wide_strikes_keep_their_places() -> void:
	eq(
		MapEffects.scatter("storm", 9, 100.0, 80.0),
		MapEffects.scatter("storm", 9, 100.0, 80.0),
		"the same frame, the same place"
	)
	check(
		MapEffects.scatter("storm", 9, 100.0, 80.0) != MapEffects.scatter("storm", 10, 100.0, 80.0),
		"another frame, another place"
	)
	for f in 42:
		var s := MapEffects.scatter("storm", f, 100.0, 80.0)
		check(absf(s.x) <= 100.0 and absf(s.y) <= 80.0, "within the room: %s" % s)
	var fx: Node3D = MapEffects.new()
	var middle := Vector2i(120, 131)
	fx.show_effects([["rain", 3, middle], ["rain", 4, middle]], 1.0)
	var a: Node3D = fx.drawn[0][2].get_node("Ground")
	var b: Node3D = fx.drawn[1][2].get_node("Ground")
	check(a.position.distance_to(b.position) > 0.01, "two fireballs fall on two places")
	fx.free()


func test_the_aura_ring_lies_on_the_ground() -> void:
	var fx: Node3D = MapEffects.new()
	fx.show_effects([["aura", 1, Vector2i(50, 53), true], ["aura", 4, Vector2i(50, 53)]])
	var ring: Node3D = fx.drawn[0][2].get_node("Ring")
	check(ring.visible, "the ring")
	check(absf(ring.transform.basis.y.normalized().y) < 0.01, "flat on the ground")
	check(fx.drawn[1][2].get_node("Light").visible, "the light around him")
	fx.free()


func test_a_blow_shows_its_trail() -> void:
	var fx: Node3D = MapEffects.new()
	for blow in 3:
		fx.show_effects([["trail", 3 * 3 + blow, Vector2i(50, 50)]], 0.5)
		var rig: Node3D = fx.drawn[0][2]
		for i in 3:
			eq(rig.get_node("Blow%d" % i).visible, i == blow, "blow %d: trail %d" % [blow, i])
		check(is_equal_approx(rig.rotation.y, Motion.yaw_of(6)), "to the right")
	fx.free()


func test_arrows_fly_their_way() -> void:
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	var fx: Node3D = MapEffects.new()
	var a = sim.arrows[0]
	a.active = true
	a.dir = 3
	a.pos = Vector2i(100, 60)
	a.w = 11
	a.h = 2
	a.ticks = 0
	fx.show_shots(sim.arrows, 0.5)
	var node: Node3D = fx.get_child(0)
	check(node.visible, "an arrow in flight")
	check(not fx.get_child(1).visible, "the others are not")
	check(is_equal_approx(node.rotation.y, Motion.yaw_of(6)), "it points right")
	var at := node.position.x
	a.ticks = 1
	fx.show_shots(sim.arrows, 0.0)
	check(node.position.x < at, "on its way it is drawn behind its place")
	fx.show_shots(sim.arrows, 1.0)
	check(is_equal_approx(node.position.x, at), "and reaches it by the next tick")
	fx.show_shots(sim.arrows, 0.0, false)
	check(is_equal_approx(node.position.x, at), "it stands while the room is held")
	a.active = false
	fx.show_shots(sim.arrows, 0.0)
	check(not node.visible, "gone")
	fx.free()


func test_the_mission_draws_effects_in_code() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = MissionScreen.new()
	root.add_child(screen)
	screen.set_process(false)
	check(screen.effects is MapEffects, "the effects are the new ones")
	screen.sim.hero.on_fire = true
	screen.sim.hero.fire_frame = 2
	screen._update_view(0.5)
	var kinds: Array = []
	for d in screen.effects.drawn:
		kinds.append(d[0])
	check("fire" in kinds, "the hero burns: %s" % [kinds])
	screen.queue_free()
	Router.params = old
