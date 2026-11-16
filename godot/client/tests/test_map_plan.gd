extends "res://tests/test_case.gd"
## MapPlan (scripts/mapgen/map_plan.gd, data/map_plans.json): what the map generator keeps of the
## campaign, place by place. The plan says what the maps say: the biome, and the generals of
## each mission in the order the hero meets them, the mission's own general last; each place has
## a seed of its own and a depth, its fewest steps from the start.


func test_a_plan_for_every_place() -> void:
	var campaign := Campaign.new()
	for n in range(1, MapBuilder.map_count() + 1):
		var plan := MapPlan.of(n)
		var missions := campaign.lord_missions(n).size()
		eq([plan.missions.size(), plan.bosses.size()], [missions, missions], "place %d" % n)
		eq(plan.biome, str(MapBuilder.load_map(n).biome), "place %d: the biome of its map" % n)
	eq(MapPlan.of(1).bosses, [1, 2, 3, 6] as Array[int], "the generals who win Uprising's missions")
	eq(MapPlan.of(27).ways_on, 6, "six ways on from Dawn over the Dnipro")


func test_the_seed_and_the_depth_of_each_place() -> void:
	var seeds := {}
	var depths: Array[int] = []
	for n in range(1, MapBuilder.map_count() + 1):
		var plan := MapPlan.of(n)
		check(plan.seed > 0 and not seeds.has(plan.seed), "place %d: a seed of its own" % n)
		seeds[plan.seed] = true
		depths.append(plan.depth)
	eq([MapPlan.of(1).depth, MapPlan.of(4).depth], [1, 4], "one step a place at the start")
	eq(MapPlan.of(10).depth, 6, "The Oath: 6 steps by the shortest way, 7 by the longest")
	eq(depths.max(), 19, "the farthest places 19 steps from the start")
	eq(depths.filter(func(d: int) -> bool: return d <= 8).size(), 13, "13 places at depth 1 to 8")


func test_the_generals_as_the_hero_meets_them() -> void:
	for n in range(1, MapBuilder.map_count() + 1):
		var plan := MapPlan.of(n)
		var map := MapBuilder.load_map(n)
		for m in plan.missions.size():
			var at := "place %d, mission %d" % [n, m]
			eq(MapPlan.stops_of(map, m, plan.bosses[m]), plan.missions[m], at)
			var last: Dictionary = plan.missions[m].back()
			check(
				last.generals.any(func(g: Array) -> bool: return g[0] == plan.bosses[m]),
				"%s: its own general last" % at
			)


func test_the_stops_of_the_three_rooms() -> void:
	var map := own_map("three_rooms")
	eq(
		MapPlan.stops_of(map, 0, 1),
		[{"generals": [[1, 1]], "talk": 0}] as Array[Dictionary],
		"general 1 in the last room"
	)
	map.rooms.missions[0][0]["general"] = 77
	map.rooms.missions[0][1]["waves"] = [201, 2, 5, 3, 0, 0]
	eq(
		MapPlan.stops_of(map, 0, 1),
		(
			[
				{"generals": [], "talk": 77},
				{"generals": [[5, 3]], "talk": 0},
				{"generals": [[1, 1]], "talk": 0}
			]
			as Array[Dictionary]
		),
		"the one who talks in the first room, general 5 in the middle one, then general 1"
	)
	eq(
		MapPlan.stops_of(map, 0, 5),
		[{"generals": [], "talk": 77}, {"generals": [[5, 3]], "talk": 0}] as Array[Dictionary],
		"the mission won with general 5: the last room is never met"
	)
