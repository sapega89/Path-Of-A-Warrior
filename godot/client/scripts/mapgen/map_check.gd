class_name MapCheck
extends RefCounted
## What the game needs of a map, checked mission by mission the way MapSim plays it: the hero
## starts on a free cell; whichever way he comes into a room, he can walk on to a next room, and
## its soldiers have a place to come in by its exits (MapRoomPlay.edge_cells), up to the room of
## the mission's own general; once that general falls, the hero can walk out of his room on enough
## sides for the ways on, two to a side (MissionScreen.ways_on); every kind of ground, prop and
## breakable thing on the map is one the game draws. The map generator checks each map it makes,
## the tests check the maps of the campaign and their own.

## The cell past each side of a room (Rooms.EXIT_* - 1: down, left, up, right).
const PAST: Array[Vector2i] = [Vector2i(0, 1), Vector2i(-1, 0), Vector2i(0, -1), Vector2i(1, 0)]


## The problems of a map, a line each (none: the game can play it). bosses: the general whose
## fall wins each mission (MapPlan.bosses); ways_on: how many places the campaign goes on to.
static func problems(map: Dictionary, bosses: Array[int], ways_on: int) -> Array[String]:
	var out := unknown_things(map)
	for mission in bosses.size():
		out.append_array(_mission(map, mission, bosses[mission], ways_on))
	return out


## The kinds of ground, props and breakable things on the map that the game does not draw.
static func unknown_things(map: Dictionary) -> Array[String]:
	var unknown := {}
	for letters: String in map.get("parts", []):
		if letters.length() != MapArt.PARTS * MapArt.PARTS:
			unknown[letters] = true
		for letter in letters:
			if not letter in MapArt.KIND_LETTERS:
				unknown[letter] = true
	for what: String in map.get("props", []):
		if what != "" and not (MapArt.PROP.has(what) or MapArt.CLUSTERS.has(what)):
			unknown[what] = true
	var breakable: Array = MapSim.table("breakable_prop")
	for code in map.get("objects", []):
		if int(code) < 0 or int(code) >= breakable.size():
			unknown[code] = true
	var out: Array[String] = []
	for what in unknown:
		out.append("unknown on the map: %s" % [what])
	return out


## One mission: the rooms the hero can come into, from the start on, each from every cell he can
## come in on (a room split by walls is checked from each side).
static func _mission(map: Dictionary, mission: int, boss: int, ways_on: int) -> Array[String]:
	var out: Array[String] = []
	var start := MapBuilder.mission_start(map, mission)
	var sim := MapSim.new(map, mission, start)
	if not MapWalls.cell_free(sim, start.y * sim.w + start.x):
		out.append("mission %d: the start %s is not free" % [mission, start])
	var todo: Array[Vector3i] = [Vector3i(start.x, start.y, sim.cell)]
	var seen := {todo[0]: true}
	var faulty := {}  # the rooms already told of
	var won := false
	while not todo.is_empty():
		var at: Vector3i = todo.pop_front()
		sim.cell = at.z
		sim.hero.pos = Vector2i(at.x * 27 + 12, at.y * 27 + 20)
		var o := sim.rooms.room_xy(sim.cell)
		var reach := MapRoomPlay.find_reachable(sim, o.x * 7 + 1, o.y * 7 + 1, sim.hero.pos)
		var next: Array[Vector3i] = []
		var problems := _soldiers_problems(sim, reach)
		if sim.rooms.waves(at.z).any(func(wave: Array) -> bool: return wave[0] == boss):
			won = true
			problems.append_array(_won_problems(sim, ways_on))
		else:
			next = _ways_in_next(sim, reach)
			if next.is_empty():
				problems.append("no way on to the next room")
		if not problems.is_empty() and not faulty.has(at.z):
			faulty[at.z] = true
			var room := "mission %d, room %d (in at %d, %d)" % [mission, at.z, at.x, at.y]
			out.append("%s: %s" % [room, "; ".join(problems)])
		for n in next:
			if not seen.has(n):
				seen[n] = true
				todo.append(n)
	if not won:
		out.append("mission %d: no way to the room of general %d" % [mission, boss])
	return out


## The room has soldiers to come and no place for them to come in by its exits (none: fine).
static func _soldiers_problems(sim: MapSim, reach: Array) -> Array[String]:
	if sim.rooms.waves(sim.cell).is_empty():
		return []
	for side in 4:
		if (
			sim.rooms.has_exit(sim.cell, side + 1)
			and not MapRoomPlay.edge_cells(sim, reach, side).is_empty()
		):
			return []
	return ["its soldiers have no place to come in"]


## The room where the mission is won has too few sides to walk out on for the ways on, two to a
## side (none: fine).
static func _won_problems(sim: MapSim, ways_on: int) -> Array[String]:
	var sides := MapRoomPlay.open_sides(sim).size()
	if sides > 0 and sides * 2 >= ways_on:
		return []
	return ["%d open sides for %d ways on" % [sides, ways_on]]


## Where the hero comes into the next rooms from his room (reach: the cells he can get to): past
## each cell of an exit side he can walk out on, Vector3i(x, y, the next room).
static func _ways_in_next(sim: MapSim, reach: Array) -> Array[Vector3i]:
	var out: Array[Vector3i] = []
	for side in 4:
		var next := sim.rooms.beside(sim.cell, side + 1)
		if not sim.rooms.has_exit(sim.cell, side + 1) or next < 0:
			continue
		for c in MapRoomPlay.edge_cells(sim, reach, side):
			var past := Vector2i(c.x, c.y) + PAST[side]
			out.append(Vector3i(past.x, past.y, next))
	return out
