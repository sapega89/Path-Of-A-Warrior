class_name RoomLayout
extends RefCounted
## The rooms of a place's map as the map generator lays them out: the grid of rooms and the
## route of each mission, a way through the grid that never comes back to a room it passed, from
## the room of the start to the room of the mission's own general. The stops of the mission's
## plan (MapPlan.missions) are spread evenly along its route, never in the first room, the
## mission's own general in the last. The grid has more rooms than the longest route, so the
## missions of one place take different routes over the same ground.

## Tiles a side of a room: room (x, y) covers tiles 1 + 7 x .. 7 + 7 x across, 1 + 7 y .. down.
const ROOM := 7
## The middle cell of room (0, 0).
const FIRST_MIDDLE := Vector2i(4, 4)
## Rooms across or down the grid at most.
const MAX_SIDE := 5
## The step to the room past each side (Rooms.EXIT_* - 1: down, left, up, right).
const STEP: Array[Vector2i] = [Vector2i(0, 1), Vector2i(-1, 0), Vector2i(0, -1), Vector2i(1, 0)]
## Cells from the middle of the first room to the start, away from the room's exit.
const START_BACK := 2

var rooms_x := 1
var rooms_y := 1
## Per mission, the rooms of its route in the order the hero walks them (y * rooms_x + x).
var routes: Array[Array] = []
## Per mission, for each stop of its plan, the place of the stop's room on the route.
var stops: Array[Array] = []


## The layout of the plan's map: a route has from route_rooms.x to route_rooms.y rooms, or one more
## than the mission has stops when that is more.
func _init(plan: MapPlan, route_rooms: Vector2i, random: GameRandom) -> void:
	var lengths: Array[int] = []
	for mission: Array in plan.missions:
		var rooms := random.range_of(route_rooms.x, route_rooms.y + 1)
		lengths.append(maxi(rooms, mission.size() + 1))
	_pick_grid(int(lengths.max()), random)
	for i in lengths.size():
		routes.append(_route(lengths[i], random))
		stops.append(spread(plan.missions[i].size(), lengths[i]))


## Where `count` stops go on a route of `length` rooms: spread evenly over its rooms but the
## first, the last stop in the last room.
static func spread(count: int, length: int) -> Array[int]:
	var out: Array[int] = []
	for i in count:
		out.append((i + 1) * (length - 1) / count)
	return out


## The exits of a room in a mission ([down, left, up, right], 1 open): a room of the route opens
## to the next one, its last room on the same side as the one before it (where the soldiers of
## the last room come in); the other rooms are closed.
func exits(mission: int, room: int) -> Array[int]:
	var out: Array[int] = [0, 0, 0, 0]
	var route: Array = routes[mission]
	var at := route.find(room)
	if at >= 0:
		var step := mini(at, route.size() - 2)
		out[_side(route[step], route[step + 1])] = 1
	return out


## The cell where the hero starts a mission: in the first room of its route, START_BACK cells
## from the room's middle, away from its exit.
func start(mission: int) -> Vector2i:
	var route: Array = routes[mission]
	var middle := room_xy(route[0]) * ROOM + FIRST_MIDDLE
	return middle - STEP[_side(route[0], route[1])] * START_BACK


func room_xy(room: int) -> Vector2i:
	return Vector2i(room % rooms_x, room / rooms_x)


## The room past side `side` of a room (Rooms.EXIT_* - 1), -1 past the edge of the grid.
func beside(room: int, side: int) -> int:
	var p := room_xy(room) + STEP[side]
	if p.x < 0 or p.y < 0 or p.x >= rooms_x or p.y >= rooms_y:
		return -1
	return p.y * rooms_x + p.x


## The side of room `from` that leads to the room `to` beside it (Rooms.EXIT_* - 1).
func _side(from: int, to: int) -> int:
	return STEP.find(room_xy(to) - room_xy(from))


## A grid of more rooms than the longest route and at most twice as many, MAX_SIDE a side at
## most.
func _pick_grid(longest: int, random: GameRandom) -> void:
	var grids: Array[Vector2i] = []
	for across in range(1, MAX_SIDE + 1):
		for down in range(1, MAX_SIDE + 1):
			if across * down > longest and across * down <= longest * 2:
				grids.append(Vector2i(across, down))
	var grid := grids[random.below(grids.size())]
	rooms_x = grid.x
	rooms_y = grid.y


## A route of `length` rooms unlike the routes of the missions before: from each room in a random
## order, the first one found going on to the rooms beside in a random order ([]: none).
func _route(length: int, random: GameRandom) -> Array[int]:
	for first: int in shuffled(range(rooms_x * rooms_y), random):
		var path: Array[int] = [first]
		if _walk(path, length, random):
			return path
	return []


## Walks the route on from its last room until it has `length` rooms (true), or finds no way on
## (false: the route as it was).
func _walk(path: Array[int], length: int, random: GameRandom) -> bool:
	if path.size() == length:
		return not routes.has(path)
	var at := room_xy(path[-1])
	for side: int in shuffled([0, 1, 2, 3], random):
		var p := at + STEP[side]
		var room := p.y * rooms_x + p.x
		if p.x >= 0 and p.y >= 0 and p.x < rooms_x and p.y < rooms_y and not path.has(room):
			path.append(room)
			if _walk(path, length, random):
				return true
			path.pop_back()
	return false


## The items in a random order.
static func shuffled(items: Array, random: GameRandom) -> Array:
	var out := items.duplicate()
	for i in range(out.size() - 1, 0, -1):
		var j := random.below(i + 1)
		var item: Variant = out[i]
		out[i] = out[j]
		out[j] = item
	return out
