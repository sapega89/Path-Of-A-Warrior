extends "res://tests/test_case.gd"
## MapCheck (scripts/mapgen/map_check.gd): what the game needs of a map. The tests' own three
## rooms pass it, a copy of them broken one way at a time is told what is wrong, and the maps of
## the campaign pass it but for one fault of place 27.


## The three rooms: generals 1 and 2 win their two missions.
func _problems(map: Dictionary, ways_on: int = 4) -> Array[String]:
	var bosses: Array[int] = [1, 2]
	return MapCheck.problems(map, bosses, ways_on)


## The problems of mission 0 only.
func _first_mission(problems: Array[String]) -> Array[String]:
	return problems.filter(func(p: String) -> bool: return p.begins_with("mission 0"))


func _put(map: Dictionary, layer: String, cells: Array[Vector2i], value: Variant) -> void:
	for c in cells:
		map[layer][c.y * int(map.w) + c.x] = value


func test_the_three_rooms_pass() -> void:
	eq(_problems(own_map("three_rooms")), [] as Array[String], "nothing wrong")


func test_the_start_on_a_wall() -> void:
	var map := own_map("three_rooms")
	map.starts[0] = [0, 9]
	eq(
		_first_mission(_problems(map)),
		["mission 0: the start (0, 9) is not free"] as Array[String],
		"the wall left of the middle room"
	)


func test_a_wall_across_the_way() -> void:
	var map := own_map("three_rooms")
	var row: Array[Vector2i] = [Vector2i(1, 11), Vector2i(2, 11), Vector2i(3, 11), Vector2i(4, 11)]
	_put(map, "flags", row, 1)
	eq(
		_first_mission(_problems(map)),
		(
			[
				(
					"mission 0, room 1 (in at 1, 8): its soldiers have no place to come in;"
					+ " no way on to the next room"
				),
				"mission 0: no way to the room of general 1"
			]
			as Array[String]
		),
		"the middle room cut in two: the last room is never reached"
	)


func test_soldiers_with_nowhere_to_come_in() -> void:
	var map := own_map("three_rooms")
	var below: Array[Vector2i] = []
	for x in range(2, 7):
		below.append(Vector2i(x, 22))
	_put(map, "flags", below, 1)  # the last room's only exit, down, walled behind
	eq(
		_first_mission(_problems(map)),
		["mission 0, room 2 (in at 1, 15): its soldiers have no place to come in"] as Array[String],
		"the wave would never start"
	)


func test_too_few_sides_for_the_ways_on() -> void:
	var map := own_map("three_rooms")
	eq(_problems(map, 6), [] as Array[String], "three sides out of the last room: six ways")
	eq(
		_first_mission(_problems(map, 7)),
		["mission 0, room 2 (in at 1, 15): 3 open sides for 7 ways on"] as Array[String],
		"seven ways need four sides"
	)


func test_unknown_things() -> void:
	var map := own_map("three_rooms")
	_put(map, "props", [Vector2i(2, 2)] as Array[Vector2i], "dragon")
	_put(map, "parts", [Vector2i(3, 3)] as Array[Vector2i], "mmmmmmmmz")
	_put(map, "objects", [Vector2i(2, 3)] as Array[Vector2i], 99)
	eq(
		MapCheck.unknown_things(map),
		(
			["unknown on the map: z", "unknown on the map: dragon", "unknown on the map: 99"]
			as Array[String]
		),
		"a letter, a prop and a breakable thing the game does not draw"
	)


## The maps of the campaign pass, but for place 27 (Dawn over the Dnipro): it has six ways on
## and the room where each of its missions is won has two sides to walk out on, so once five or
## six of those places are open, ways go on a walled side too. Its generated map mends it.
func test_the_maps_of_the_campaign_pass() -> void:
	var found := {}
	for n in range(1, MapBuilder.map_count() + 1):
		var plan := MapPlan.of(n)
		var problems := MapCheck.problems(MapBuilder.load_map(n), plan.bosses, plan.ways_on)
		if not problems.is_empty():
			found[n] = problems
	eq(
		found,
		{
			27:
			[
				"mission 0, room 11 (in at 22, 21): 2 open sides for 6 ways on",
				"mission 1, room 7 (in at 22, 8): 2 open sides for 6 ways on"
			]
		},
		"one fault: place 27"
	)
