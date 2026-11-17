extends "res://tests/test_case.gd"
## The map generator (scripts/mapgen/: MapGenerator, RoomLayout): the map of every place made
## from its plan. The same seed makes the same map on any computer; each mission's route never
## comes back to a room, is as long as the curve of data/map_rules.json says and leads from the
## start to the room of the mission's own general, the plan's other stops spread along it; the
## game can play every map (MapCheck), from its own seed and the next ones; the maps of the
## campaign the generator made (data/maps/N.json with a seed) are the ones it makes now.

## The maps made, by place: each made once for all the tests here.
static var _made := {}


func _map(place: int) -> Dictionary:
	if not _made.has(place):
		_made[place] = MapGenerator.new().make(MapPlan.of(place))
	return _made[place]


func _places() -> Array:
	return range(1, MapBuilder.map_count() + 1)


func test_the_curve_covers_every_depth() -> void:
	var bands: Array = (
		JSON.parse_string(FileAccess.get_file_as_string(MapGenerator.RULES_PATH)).curve
	)
	var next := 1
	for band: Dictionary in bands:
		eq(int(band.depths[0]), next, "the band from depth %d on" % next)
		check(int(band.route_rooms[0]) >= 2, "a route has a first room and a last one")
		next = int(band.depths[1]) + 1
	var deepest := 0
	for n: int in _places():
		deepest = maxi(deepest, MapPlan.of(n).depth)
	eq(next - 1, deepest, "the last band to the deepest place")
	eq(MapGenerator.route_rooms(1), Vector2i(3, 4), "3 to 4 rooms at the start of the campaign")
	eq(MapGenerator.route_rooms(19), Vector2i(6, 8), "6 to 8 rooms at its end")


func test_the_random_numbers_of_a_step() -> void:
	var layout := MapGenerator.stream(1, "layout")
	eq(
		[layout.next_int(), layout.next_int(), layout.next_int()],
		[334137365, -573773870, 363337902],
		"the same numbers on any computer"
	)
	var waves := MapGenerator.stream(1, "waves")
	eq(waves.next_int(), 608498680, "another step, other numbers")
	eq(MapGenerator.stream(2, "layout").next_int(), -2084216205, "another seed, other numbers")


func test_the_same_seed_the_same_map() -> void:
	for n: int in _places():
		var plan := MapPlan.of(n)
		var map := JSON.stringify(MapGenerator.build(plan, plan.seed))
		eq(JSON.stringify(MapGenerator.build(plan, plan.seed)), map, "place %d" % n)
		var others := {}
		for i in range(1, 3):
			others[JSON.stringify(MapGenerator.build(plan, plan.seed + i).rooms)] = true
		check(others.size() > 1, "place %d: other seeds, other rooms" % n)


func test_the_stops_spread_along_the_route() -> void:
	eq(RoomLayout.spread(1, 4), [3] as Array[int], "the only general in the last room")
	eq(RoomLayout.spread(3, 4), [1, 2, 3] as Array[int], "a general in every room but the first")
	eq(RoomLayout.spread(2, 7), [3, 6] as Array[int], "halfway, then the last room")
	eq(RoomLayout.spread(3, 7), [2, 4, 6] as Array[int], "every second room")


func test_the_routes() -> void:
	for n: int in _places():
		var plan := MapPlan.of(n)
		var layout := MapGenerator.layout_of(plan, plan.seed)
		var band := MapGenerator.route_rooms(plan.depth)
		for m in plan.missions.size():
			var at := "place %d, mission %d" % [n, m]
			var route: Array = layout.routes[m]
			var shortest := maxi(band.x, plan.missions[m].size() + 1)
			var longest := maxi(band.y, plan.missions[m].size() + 1)
			check(
				route.size() >= shortest and route.size() <= longest,
				"%s: as long as the curve says" % at
			)
			_check_route(layout, route, at)
			check(not layout.routes.slice(0, m).has(route), "%s: a route of its own" % at)


## The rooms of a route are all different, in the grid, each beside the one before.
func _check_route(layout: RoomLayout, route: Array, at: String) -> void:
	var seen := {}
	for i in route.size():
		var room: int = route[i]
		check(
			room >= 0 and room < layout.rooms_x * layout.rooms_y,
			"%s: room %d in the grid" % [at, room]
		)
		check(not seen.has(room), "%s: room %d only once" % [at, room])
		seen[room] = true
		if i > 0:
			var step := layout.room_xy(room) - layout.room_xy(route[i - 1])
			eq(absi(step.x) + absi(step.y), 1, "%s: room %d beside the one before" % [at, room])


func test_every_map_the_game_can_play() -> void:
	for n: int in _places():
		var plan := MapPlan.of(n)
		var maker := MapGenerator.new()
		var map := maker.make(plan)
		eq(maker.problems, [] as Array[String], "place %d" % n)
		eq(map.get("seed"), plan.seed, "place %d: from its own seed" % n)
		eq(MapCheck.unknown_things(map), [] as Array[String], "place %d: all of it drawn" % n)


func test_five_seeds_of_every_place() -> void:
	const SEEDS := 5
	for n: int in _places():
		var plan := MapPlan.of(n)
		for i in range(1, SEEDS + 1):
			var map := MapGenerator.build(plan, plan.seed + i)
			var problems := MapCheck.problems(map, plan.bosses, plan.ways_on)
			eq(problems, [] as Array[String], "place %d, seed %d" % [n, plan.seed + i])


func test_the_maps_of_the_campaign_as_made_now() -> void:
	var made := 0
	for n: int in _places():
		var saved := MapBuilder.load_map(n)
		if not saved.has("seed"):
			continue  # a map the generator has not made yet
		made += 1
		var now: Variant = JSON.parse_string(JSON.stringify(_map(n)))
		check(
			JSON.stringify(now) == JSON.stringify(saved),
			"place %d: data/maps/%d.json made again by tools/gen_maps.tscn" % [n, n]
		)
	check(made > 0, "maps of the campaign the generator made: %d" % made)


func test_the_generals_where_the_plan_puts_them() -> void:
	for n: int in _places():
		var plan := MapPlan.of(n)
		var map := _map(n)
		var layout := MapGenerator.layout_of(plan, int(map.seed))
		for m in plan.missions.size():
			var at := "place %d, mission %d" % [n, m]
			var route: Array = layout.routes[m]
			var rooms := Rooms.new(map, m)
			eq(MapPlan.stops_of(map, m, plan.bosses[m]), plan.missions[m], at)
			check(
				rooms.waves(route.back()).any(
					func(w: Array) -> bool: return w[0] == plan.bosses[m]
				),
				"%s: its own general in the last room" % at
			)
			check(not rooms.has_general(route[0]), "%s: no general in the first room" % at)
			eq(int(rooms.cells[route[0]].general), 0, "%s: no talk in the first room" % at)


func test_the_exits_lead_along_the_route() -> void:
	for n: int in _places():
		var plan := MapPlan.of(n)
		var map := _map(n)
		var layout := MapGenerator.layout_of(plan, int(map.seed))
		for m in plan.missions.size():
			var at := "place %d, mission %d" % [n, m]
			var route: Array = layout.routes[m]
			var rooms := Rooms.new(map, m)
			var start := MapBuilder.mission_start(map, m)
			var walked: Array = [rooms.room_at(Vector3(start.x + 0.5, 0.0, start.y + 0.5))]
			while walked.size() < route.size() and rooms.next_rooms(walked.back()).size() == 1:
				walked.append(rooms.next_rooms(walked.back())[0])
			eq(walked, route, "%s: from the start room one exit at a time" % at)
			eq(rooms.exits(route.back()).count(1), 1, "%s: the last room's soldiers come in" % at)
			var closed := range(rooms.count()).filter(func(r: int) -> bool: return not route.has(r))
			check(
				closed.all(func(r: int) -> bool: return rooms.exits(r) == [0, 0, 0, 0]),
				"%s: the rooms off the route closed" % at
			)
