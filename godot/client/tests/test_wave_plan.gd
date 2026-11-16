extends "res://tests/test_case.gd"
## The fights of the generated maps (scripts/mapgen/wave_plan.gd, WavePlan, by the rules of
## data/map_rules.json), on the map of every place: each mission's soldiers as many a room of its
## route as the curve gives, the first room lighter than the last; in a general's room soldiers
## before him and fewer after; archers on free cells of the rooms past the first, none at the
## start of the campaign; things to break in the rooms of the routes, of the biome's own; the
## time of each mission by its formula; the autopilot wins generated missions.

## The maps made, by place: each made once for all the tests here.
static var _made := {}


func _map(place: int) -> Dictionary:
	if not _made.has(place):
		_made[place] = MapGenerator.new().make(MapPlan.of(place))
	return _made[place]


func _places() -> Array:
	return range(1, MapBuilder.map_count() + 1)


func _rules() -> Dictionary:
	return JSON.parse_string(FileAccess.get_file_as_string(MapGenerator.RULES_PATH))


func _soldiers(rooms: Rooms, room: int) -> int:
	var count := 0
	for wave: Array in rooms.waves(room):
		count += int(wave[1]) if wave[0] == MapSim.KIND_SWORDS else 0
	return count


## The archers of a mission on the map: their cells.
func _archers(map: Dictionary, mission: int) -> Array[Vector2i]:
	var out: Array[Vector2i] = []
	for script: Dictionary in map.scripts:
		for op: Array in script.ops:
			if op == [0, mission + 1, MapSim.KIND_ARCHERS - 200]:
				out.append(Vector2i(int(script.x), int(script.y)))
	return out


## The cells of a room the hero can walk to from its middle: cell -> true.
func _walkable(map: Dictionary, room_xy: Vector2i) -> Dictionary:
	var corner := room_xy * RoomLayout.ROOM + Vector2i.ONE
	var middle := corner + Vector2i.ONE * (RoomLayout.ROOM / 2)
	var room := Rect2i(corner, Vector2i.ONE * RoomLayout.ROOM)
	var seen := {middle: true}
	var todo: Array[Vector2i] = [middle]
	while not todo.is_empty():
		var c: Vector2i = todo.pop_back()
		for step in RoomLayout.STEP:
			var n := c + step
			if room.has_point(n) and not seen.has(n) and int(map.flags[n.y * map.w + n.x]) & 1 == 0:
				seen[n] = true
				todo.append(n)
	return seen


func test_the_soldiers_of_the_curve() -> void:
	for n: int in _places():
		var plan := MapPlan.of(n)
		var map := _map(n)
		var layout := MapGenerator.layout_of(plan, int(map.seed))
		var per_room: Array = MapGenerator.curve(plan.depth)["soldiers"]
		for m in plan.missions.size():
			var at := "place %d, mission %d" % [n, m]
			var route: Array = layout.routes[m]
			var rooms := Rooms.new(map, m)
			var total := 0
			for room: int in route:
				check(_soldiers(rooms, room) > 0, "%s, room %d: soldiers" % [at, room])
				total += _soldiers(rooms, room)
			var fewest := floori(float(per_room[0]) * route.size())
			var most := ceili(float(per_room[1]) * route.size())
			check(total >= fewest and total <= most, "%s: %d soldiers" % [at, total])
			check(
				_soldiers(rooms, route[0]) < _soldiers(rooms, route.back()),
				"%s: the first room lighter than the last" % at
			)
			for room in rooms.cells.size():
				if not room in route:
					eq(rooms.waves(room), [], "%s, room %d: off the route, no one" % [at, room])


func test_soldiers_before_the_generals_and_after() -> void:
	var after := 0
	for n: int in _places():
		var map := _map(n)
		for m in MapPlan.of(n).missions.size():
			var rooms := Rooms.new(map, m)
			for room in rooms.cells.size():
				var waves := rooms.waves(room)
				if not rooms.has_general(room):
					continue
				var at := "place %d, mission %d, room %d" % [n, m, room]
				eq(waves[0][0], MapSim.KIND_SWORDS, at + ": soldiers first")
				var later := _soldiers(rooms, room) - int(waves[0][1])
				check(later < int(waves[0][1]), "%s: fewer after the generals: %d" % [at, later])
				after += later
	check(after > 0, "soldiers after the generals: %d" % after)


func test_the_archers_on_free_cells() -> void:
	var count := 0
	for n: int in _places():
		var plan := MapPlan.of(n)
		var map := _map(n)
		var layout := MapGenerator.layout_of(plan, int(map.seed))
		var per_room: Array = MapGenerator.curve(plan.depth)["archers"]
		for m in plan.missions.size():
			var at := "place %d, mission %d" % [n, m]
			var route: Array = layout.routes[m]
			var archers := _archers(map, m)
			check(archers.size() <= ceili(float(per_room[1]) * route.size()), at + ": archers")
			var in_room := {}
			for c in archers:
				var room := (c - Vector2i.ONE) / RoomLayout.ROOM
				var number := room.y * layout.rooms_x + room.x
				check(number in route and number != route[0], "%s: an archer at %s" % [at, c])
				check(_walkable(map, room).has(c), "%s: the hero walks to %s" % [at, c])
				eq(int(map.objects[c.y * map.w + c.x]), 0, "%s: nothing to break at %s" % [at, c])
				in_room[number] = int(in_room.get(number, 0)) + 1
				check(in_room[number] <= WavePlan.ARCHERS_A_ROOM, "%s, room %d" % [at, number])
			if plan.depth <= 4:
				eq(archers.size(), 0, at + ": none at the start of the campaign")
			count += archers.size()
	check(count > 0, "archers on the maps: %d" % count)


func test_the_things_to_break() -> void:
	var rules := _rules()
	var codes: Array = MapSim.table("breakable_prop")
	var most := int(rules.breakables[1])
	for n: int in _places():
		var plan := MapPlan.of(n)
		var map := _map(n)
		var layout := MapGenerator.layout_of(plan, int(map.seed))
		var on_route := {}
		for route: Array in layout.routes:
			for room: int in route:
				on_route[room] = true
		var own: Array = rules.biomes[plan.biome].breakables
		var in_room := {}
		for i in map.objects.size():
			if int(map.objects[i]) == 0:
				continue
			var c := Vector2i(i % int(map.w), i / int(map.w))
			var room := (c - Vector2i.ONE) / RoomLayout.ROOM
			var number := room.y * layout.rooms_x + room.x
			var at := "place %d, %s at %s" % [n, codes[int(map.objects[i])], c]
			check(on_route.has(number), at + ": in a room of a route")
			check(codes[int(map.objects[i])] in own, at + ": the biome's own")
			check(_walkable(map, room).has(c), at + ": the hero walks to it")
			eq(str(map.props[i]), "", at + ": nothing else on its cell")
			in_room[number] = int(in_room.get(number, 0)) + 1
		for room: int in on_route:
			check(int(in_room.get(room, 0)) <= most, "place %d, room %d: things" % [n, room])
		check(not in_room.is_empty(), "place %d: things to break" % n)


func test_the_time_of_a_mission() -> void:
	var seconds: Dictionary = _rules().time
	for n: int in _places():
		var plan := MapPlan.of(n)
		var map := _map(n)
		var layout := MapGenerator.layout_of(plan, int(map.seed))
		for m in plan.missions.size():
			var route: Array = layout.routes[m]
			var rooms := Rooms.new(map, m)
			var enemies := _archers(map, m).size()
			var generals := 0
			for room: int in route:
				enemies += _soldiers(rooms, room)
			for stop: Dictionary in plan.missions[m]:
				generals += stop.generals.size()
			var time := (
				float(seconds.base)
				+ float(seconds.room) * route.size()
				+ float(seconds.enemy) * enemies
				+ float(seconds.general) * generals
			)
			eq(MapBuilder.mission_time(map, m), roundi(time), "place %d, mission %d" % [n, m])


## Plays a mission of a generated map with the autopilot, a strong hero, up to `ticks` ticks.
func _played(place: int, mission: int, ticks: int) -> MapSim:
	var map := _map(place)
	var sim := MapSim.new(map, mission, MapBuilder.mission_start(map, mission))
	sim.rng = GameRandom.new(7)
	sim.boss_type = MapPlan.of(place).bosses[mission]
	sim.hero.attack = 80
	sim.hero.max_hp = 2000
	sim.hero.hp = 2000
	var pilot := Autopilot.new()
	pilot.toggle()
	for t in ticks:
		if not sim.talk.is_empty():
			sim.skip_talk()
		var d: Dictionary = pilot.decide(sim)
		sim.tick(int(d.held), -1, bool(d.fire) or sim.banner != 0, int(d.hotkey), -1, int(d.belt))
		if sim.finished or sim.failed:
			break
	return sim


func test_the_autopilot_wins_generated_missions() -> void:
	for at: Vector2i in [Vector2i(1, 0), Vector2i(8, 0)]:
		var sim := _played(at.x, at.y, 5000)
		check(sim.won, "place %d, mission %d won in %d ticks" % [at.x, at.y + 1, sim.ticks])
