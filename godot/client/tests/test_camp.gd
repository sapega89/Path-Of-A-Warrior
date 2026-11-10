extends "res://tests/test_case.gd"
## The camp between missions on the marsh: its plan (gates on the sides of the world, what is
## blocked, which gate is walked out of, the spots), the fort built from it, and the screen.

const CAMP_PATH := "user://test_camp_plavni.json"


## n ways: [[place, open, mission], ...], the second one closed.
func _ways(n: int) -> Array:
	var ways: Array = []
	for i in n:
		ways.append([i + 1, i != 1, 0])
	return ways


func test_gates_on_the_sides_of_the_world() -> void:
	for n in range(0, 7):
		eq(CampPlan.new(_ways(n)).exits.size(), n, "%d ways, %d gates" % [n, n])
	var four := CampPlan.new(_ways(4))
	eq(
		four.exits.map(func(e: Dictionary) -> float: return e.angle),
		[CampPlan.NORTH, CampPlan.EAST, CampPlan.WEST, CampPlan.SOUTH],
		"four ways: north, east, west and south"
	)
	eq(CampPlan.gate_pieces(CampPlan.SOUTH), 2, "the main gate in the south is two pieces wide")
	eq(CampPlan.gate_pieces(CampPlan.EAST), 1, "a side gate one")
	var north: Dictionary = four.exits[0]
	check(north.gate.distance_to(Vector3(0, 0, -CampPlan.RADIUS)) < 0.01, "north is -Z")
	check(north.out.is_equal_approx(Vector3(0, 0, -1)), "its way on goes north")
	check(CampPlan.is_main(0) and CampPlan.is_main(30) and not CampPlan.is_main(27), "main camps")


func test_walking_out_of_a_gate() -> void:
	var plan := CampPlan.new(_ways(4))
	var past := CampPlan.RADIUS + CampPlan.OUT + 0.2
	eq(plan.exit_crossed(CampPlan.on_ring(CampPlan.NORTH, past)), 0, "out of the north gate")
	eq(plan.exit_crossed(CampPlan.on_ring(CampPlan.EAST, past)), -1, "the east one is barred")
	eq(plan.exit_crossed(CampPlan.on_ring(CampPlan.SOUTH, past)), 3, "out of the south gate")
	eq(plan.exit_crossed(CampPlan.on_ring(CampPlan.NORTH, 10.0)), -1, "still inside")
	eq(plan.exit_crossed(CampPlan.on_ring(45.0, past)), -1, "not where there is no gate")
	check(not plan.blocked(CampPlan.on_ring(CampPlan.NORTH, CampPlan.RADIUS)), "an open gate")
	check(plan.blocked(CampPlan.on_ring(CampPlan.EAST, CampPlan.RADIUS)), "a barred gate")
	check(plan.blocked(CampPlan.on_ring(45.0, CampPlan.RADIUS)), "the palisade")
	check(not plan.blocked(CampPlan.START), "the yard")
	plan.add_solid(Vector2(2, 2), 1.0)
	check(plan.blocked(Vector3(2.5, 0, 2)), "something standing")


func test_the_town_hall_from_farther_off() -> void:
	var plan := CampPlan.new(_ways(1))
	var spots := plan.spots()
	eq(
		spots.map(func(s: Dictionary) -> String: return s.kind),
		["way", "smith", "store", "hall", "auction"],
		"a way per gate, then the smithy, the stores, the town hall and the auctioneer"
	)
	var door: Vector3 = CampPlan.SPOTS["hall"][0]
	var smith: Vector3 = CampPlan.SPOTS["smith"][0]
	eq(CampPlan.spot_near(spots, door + Vector3(0, 0, 2.8)).kind, "hall", "the hall from 2.8 m")
	eq(CampPlan.spot_near(spots, smith + Vector3(0, 0, 2.8)), {}, "not the smithy from 2.8 m")
	eq(CampPlan.spot_near(spots, smith + Vector3(0, 0, 1.0)).kind, "smith", "near the anvil")
	eq(CampPlan.spot_near(spots, CampPlan.START), {}, "nothing in the yard")


func test_the_fort_leaves_every_way_and_spot_free() -> void:
	for n in [1, 4, 6]:
		var plan := CampPlan.new(_ways(n))
		var fort: CampFort = load("res://screens/camp/camp_fort.tscn").instantiate()
		root.add_child(fort)
		fort.build(plan, ["steppe", "forest", "lake", "town", "mountains", "steppe"], n)
		var seen := plan.reachable(CampPlan.START)
		for s in plan.spots():
			if s.kind != "way" or s.open:
				check(seen.has(CampPlan.cell_of(s.at)), "%d ways: %s can be reached" % [n, s.kind])
		check(fort.auctioneer != null and fort.auctioneer.name == "Auctioneer", "the auctioneer")
		check(fort.find_child("Land*", false, false) != null, "the land past the gates")
		check(fort.body.get_child_count() > plan.solids.size(), "the palisade stands")
		var lights := fort.find_children("*", "OmniLight3D", true, false)
		check(lights.size() <= CampFort.LIGHTS, "%d lights at most (%d)" % [n, lights.size()])
		fort.free()


func test_camp_screen_ways_lead_to_the_missions() -> void:
	var p: RefCounted = Profile.new()
	p.place = 4
	p.save(CAMP_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": CAMP_PATH}
	var camp: Control = Router.make(Router.SCREENS["camp"])
	root.add_child(camp)
	eq(camp.place, 4, "the camp of the hero's place")
	eq(
		camp.spots.map(func(s): return s.kind),
		["way", "way", "smith", "store", "hall", "auction"],
		"a way per place on, then the blacksmith, the warehouse, the town hall, the auctioneer"
	)
	var ways: Array = camp.spots.filter(func(s): return s.kind == "way")
	var open: Array = ways.filter(func(s): return s.open)
	eq(ways.filter(func(s): return not s.open).map(func(s): return s.place), [5], "Regalia barred")
	eq(open.map(func(s): return [s.place, s.mission]), [[6, 0]], "Harvest, its first mission")
	check(not camp.plan.main, "Korsun is a stop")
	var harvest: Dictionary = open[0]
	eq(camp.spot_near(harvest.at + Vector3(0.5, 0, 0.5)), harvest, "next to the way in")
	var e: Dictionary = camp.plan.exits[camp.spots.find(harvest)]
	var out: Vector3 = e.out * (CampPlan.RADIUS + CampPlan.OUT + 0.5)
	eq(camp.exit_crossed(out), harvest, "out through the gate")
	eq(camp.exit_crossed(CampPlan.START), {}, "inside")
	var auction: Dictionary = camp.spots[5]
	eq(camp.spot_near(auction.at), auction, "at the auctioneer's stall")
	check(camp._hint_text(auction).contains(tr("camp.auction")), "says who is there")
	check(camp.rulers(1).size() == 4, "four colonels give the missions at Uprising")
	eq(camp.arrows.size(), 1, "an arrow on the open way only")
	eq(camp.camera.target, camp.hero, "the camera follows the hero")
	eq(camp.hero.global_position.distance_to(CampPlan.START) < 0.1, true, "he starts in the yard")
	var world_light: WorldEnvironment = (
		camp.world.find_children("*", "WorldEnvironment", false, false)[0]
	)
	eq(world_light.environment, CampFort.DUSK, "dusk over the marsh")
	p.done["6:0"] = true
	camp.profile = p
	eq(camp.choices().filter(func(w): return w[1]), [[6, true, 1]], "the next mission not won yet")
	camp.place = 27
	eq(
		camp.choices().map(func(w): return w[0]).size(),
		camp.world_map.next_places(27).size(),
		"one way per place on"
	)
	eq(CampScreen.terrain(33), "mountains", "Chyhyryn's hills")
	eq(CampScreen.terrain(19), "forest", "a forest")
	eq(CampScreen.terrain(24), "lake", "down the Dnipro")
	eq(CampScreen.terrain(2), "steppe", "the steppe")
	camp.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(CAMP_PATH))


func test_the_arrow_points_the_way_out() -> void:
	eq(CampScreen.arrow_side(Vector3(0, 0, -1)), CampScreen.ARROW_UP, "north: up")
	eq(CampScreen.arrow_side(Vector3(1, 0, 0)), CampScreen.ARROW_RIGHT, "east: right")
	eq(CampScreen.arrow_side(Vector3(-1, 0, 0)), CampScreen.ARROW_LEFT, "west: left")
	eq(CampScreen.arrow_side(Vector3(0, 0, 1)), CampScreen.ARROW_DOWN, "south: down")
