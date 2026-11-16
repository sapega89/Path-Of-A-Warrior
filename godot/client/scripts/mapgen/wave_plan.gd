class_name WavePlan
extends RefCounted
## The fights of a map being made (MapDraft), mission by mission along the routes of its rooms
## (RoomLayout): the soldiers of each room of a route, as many a room as the curve gives for the
## place's depth, the first room lighter and the last one heavier; in the room of each stop of
## the plan its generals, the room's soldiers before them and a third after them, as the game
## sends them (Rooms.waves); archers standing in the rooms past the first; the time of the
## mission for its speed bonus. Things to break stand in the rooms of the routes. Archers and
## things to break stand on cells the ways through the room do not keep (RoomFill) and the hero
## can walk to from its middle.
##
## In the rules (map_rules.json): per band of the curve, soldiers and archers: [fewest, most] a
## room of a route; breakables: [fewest, most] things to break in a room of a route, of the
## biome's breakables (names of MapSim.table("breakable_prop")); time: base seconds and seconds
## per room of the route, per enemy and per general.

## Numbers in a room's waves: [kind, count] pairs (a general: [kind, levels over the hero]),
## zeros after the last.
const WAVE_NUMBERS := 12
## The share of the soldiers of the mission that a room takes: the first room of the route, the
## last one, a room where generals fight; any other takes 1.
const FIRST_SHARE := 0.6
const LAST_SHARE := 1.25
const GENERALS_SHARE := 1.1
## Of the soldiers of a room where generals fight, one in AFTER_GENERALS comes after them.
const AFTER_GENERALS := 3
const ARCHERS_A_ROOM := 2
const IN := 1000

var draft: MapDraft
var plan: MapPlan
var rules: Dictionary
var random: GameRandom
## Per mission, per room of the map: its waves, WAVE_NUMBERS numbers.
var waves: Array[Array] = []
## Per cell: the code of the thing to break on it (MapSim.table("breakable_prop")), 0 none.
var objects: Array[int] = []
## The map's scripts: {x, y, ops}, the archers of the missions on a cell ([0, mission + 1, 2]).
var scripts: Array[Dictionary] = []
## Per mission: its time for the speed bonus, in seconds.
var time_limits: Array[int] = []


func _init(map_draft: MapDraft, map_plan: MapPlan, map_rules: Dictionary, rng: GameRandom) -> void:
	draft = map_draft
	plan = map_plan
	rules = map_rules
	random = rng


## Plans the fights of every mission of the plan.
func make() -> void:
	objects.resize(draft.w * draft.h)
	objects.fill(0)
	_break_things()
	var band := MapGenerator.curve(plan.depth)
	var ops := {}
	for m in draft.layout.routes.size():
		var soldiers := _mission_waves(m, _between(band["soldiers"]))
		var archers := _archers(m, _between(band["archers"]), ops)
		time_limits.append(_time(m, soldiers + archers))
	for c: Vector2i in ops:
		scripts.append({"x": c.x, "y": c.y, "ops": ops[c]})


## A number from [fewest, most].
func _between(fewest_most: Array) -> float:
	var fewest := float(fewest_most[0])
	return fewest + (float(fewest_most[1]) - fewest) * random.below(IN) / IN


## The things to break in the rooms of the routes, each room once.
func _break_things() -> void:
	var names: Array = rules["biomes"][plan.biome]["breakables"]
	var codes: Array = MapSim.table("breakable_prop")
	var count: Array = rules["breakables"]
	var done := {}
	for route: Array in draft.layout.routes:
		for room: int in route:
			if done.has(room):
				continue
			done[room] = true
			for k in random.range_of(int(count[0]), int(count[1]) + 1):
				var cells := _free_cells(room)
				if cells.is_empty():
					break
				var i := draft.at(cells[random.below(cells.size())])
				objects[i] = codes.find(names[random.below(names.size())])
				draft.props[i] = ""


## The waves of the rooms of a mission, `per_room` soldiers a room of its route on the whole;
## how many soldiers they have.
func _mission_waves(mission: int, per_room: float) -> int:
	var route: Array = draft.layout.routes[mission]
	var generals := {}  # index on the route -> the stop's generals
	for i in plan.missions[mission].size():
		generals[draft.layout.stops[mission][i]] = plan.missions[mission][i]["generals"]
	var shares: Array[float] = []
	for i in route.size():
		if i == 0:
			shares.append(FIRST_SHARE)
		elif i == route.size() - 1:
			shares.append(LAST_SHARE)
		else:
			shares.append(GENERALS_SHARE if not generals.get(i, []).is_empty() else 1.0)
	var total := roundi(per_room * route.size())
	var counts := _shared(total, shares)
	var rooms: Array = []
	for room in draft.layout.rooms_x * draft.layout.rooms_y:
		var none: Array[int] = []
		none.resize(WAVE_NUMBERS)
		rooms.append(none)
	for i in route.size():
		rooms[route[i]] = _room_waves(counts[i], generals.get(i, []))
	waves.append(rooms)
	return total


## `total` shared by `shares`, whole numbers that add up to it (the biggest leftovers get one
## more).
static func _shared(total: int, shares: Array[float]) -> Array[int]:
	var sum := 0.0
	for share in shares:
		sum += share
	var out: Array[int] = []
	var left: Array[float] = []
	var given := 0
	for share in shares:
		var exact := total * share / sum
		out.append(floori(exact))
		left.append(exact - floori(exact))
		given += floori(exact)
	while given < total:
		var most := 0
		for i in left.size():
			if left[i] > left[most]:
				most = i
		out[most] += 1
		left[most] = -1.0
		given += 1
	return out


## A room's waves: its soldiers and generals ([kind, levels over the hero]); the soldiers before
## the generals, a third of them after them as long as the waves have room.
static func _room_waves(soldiers: int, generals: Array) -> Array[int]:
	var waves_after := mini(generals.size(), WAVE_NUMBERS / 2 - 1 - generals.size())
	var after := soldiers / AFTER_GENERALS if waves_after > 0 else 0
	var out: Array[int] = []
	_add_soldiers(out, soldiers - after)
	for g in generals.size():
		out.append(int(generals[g][0]))
		out.append(int(generals[g][1]))
		if g < waves_after:
			_add_soldiers(out, after / waves_after + (1 if g < after % waves_after else 0))
	out.resize(WAVE_NUMBERS)
	return out


static func _add_soldiers(to: Array[int], count: int) -> void:
	if count > 0:
		to.append(MapSim.KIND_SWORDS)
		to.append(count)


## The archers of a mission, `per_room` a room of its route on the whole, up to ARCHERS_A_ROOM in
## each room past the first (ops: cell -> its scripts' ops); how many stand.
func _archers(mission: int, per_room: float, ops: Dictionary) -> int:
	var route: Array = draft.layout.routes[mission]
	var spots: Array = []
	for room: int in route.slice(1):
		spots.append_array(RoomLayout.shuffled(_free_cells(room), random).slice(0, ARCHERS_A_ROOM))
	spots = RoomLayout.shuffled(spots, random).slice(0, roundi(per_room * route.size()))
	for c: Vector2i in spots:
		if not ops.has(c):
			ops[c] = []
		ops[c].append([0, mission + 1, MapSim.KIND_ARCHERS - 200])
	return spots.size()


## The mission's time: base seconds, and seconds per room of its route, per enemy and per
## general.
func _time(mission: int, enemies: int) -> int:
	var seconds: Dictionary = rules["time"]
	var generals := 0
	for stop: Dictionary in plan.missions[mission]:
		generals += stop["generals"].size()
	return roundi(
		(
			float(seconds["base"])
			+ float(seconds["room"]) * draft.layout.routes[mission].size()
			+ float(seconds["enemy"]) * enemies
			+ float(seconds["general"]) * generals
		)
	)


## The cells of a room the hero can walk to from its middle, nothing on them (a wall, a thing to
## break), but for those the ways through the room keep.
func _free_cells(room: int) -> Array[Vector2i]:
	var middle := draft.corner(room) + Vector2i.ONE * (RoomLayout.ROOM / 2)
	var seen := {middle: true}
	var todo: Array[Vector2i] = [middle]
	var out: Array[Vector2i] = []
	while not todo.is_empty():
		var c: Vector2i = todo.pop_back()
		if draft.keep[draft.at(c)] == 0:
			out.append(c)
		for step in RoomLayout.STEP:
			var n := c + step
			var i := draft.at(n)
			if seen.has(n) or draft.room_of(n) != room or draft.blocked[i] == 1 or objects[i] != 0:
				continue
			seen[n] = true
			todo.append(n)
	return out
