class_name RoomFill
extends RefCounted
## What stands in the rooms of a map being made (MapDraft), by the rules of its biome
## (map_rules.json biomes). First the ways through the rooms of the routes are kept free: a door
## of three cells on each side a route passes (the same cells for the rooms on both sides of it),
## the middle of the room (wider where generals fight), the way from each door to the middle and
## from the start to it. The room where a mission is won gets doors on enough sides for the ways
## on, two to a side. Then the sides of those rooms are closed by the biome's barrier but for
## their doors, so is the ring around the rooms (with the ring's own barrier where the biome has
## one: the land past the map goes on as the ring's ground), the rooms off every route are filled
## with the biome's land, and the rooms of the routes get its obstacles until they take the share
## of the room the crowding says. In front of a fight (the front rows of a room on a route, where
## the camera looks over them, and the row below it) the barrier is the biome's low one and no
## tall thing stands (a fir, a tent). Of a column of firs every other one is a bush: the game
## draws a single fir for the cells of one column.
##
## An obstacle in the rules: shape (single, line, block, clump), size [fewest, most] (cells of a
## line or a clump, a side of a block), kind (the ground of its cells, a letter of
## MapArt.KIND_LETTERS), prop (what stands on them), face (the kind of a block's last row: the
## face of a cliff), weight (how often it comes). A barrier (barrier, low_barrier, ring): the kind
## and the prop of each of its cells.

## Cells of a door along its side, and the first and the last cell of the side it may start at.
const DOOR := 3
const DOOR_FIRST := 1
const DOOR_LAST := 3
## A side of the middle of a room kept free, and of the middle where generals fight.
const MIDDLE := 3
const ARENA := 5
## What stands tall: kept out of the rows in front of a fight.
const TALL: Array[String] = ["fir", "tent", "hut", "palisade", "well"]
## Rows at the front (the bottom) of a room on a route kept clear of tall things.
const FRONT_ROWS := 2
## Tries at an obstacle for a room before it is left as it is.
const TRIES := 60
## Steps of the growth of a clump for each cell it has to get.
const CLUMP_STEPS := 4
## Ways on the campaign shows on one side of the room where a mission is won.
const WAYS_A_SIDE := 2

var draft: MapDraft
var biome: Dictionary
var random: GameRandom
## Rooms on any route -> true.
var _on_route := {}
## Rooms where generals fight -> true.
var _arenas := {}
## Room -> its doors: side (0 down, 1 left, 2 up, 3 right) -> the cell of the side it starts at.
var _doors := {}


func _init(map_draft: MapDraft, biome_rules: Dictionary, rng: GameRandom) -> void:
	draft = map_draft
	biome = biome_rules
	random = rng


## Fills the rooms of the plan's map; crowding: the fewest and the most of a room on a route that
## its obstacles take.
func fill(plan: MapPlan, crowding: Vector2) -> void:
	var layout := draft.layout
	for m in layout.routes.size():
		for i in layout.routes[m].size():
			_on_route[layout.routes[m][i]] = true
		for i in layout.stops[m].size():
			if not plan.missions[m][i]["generals"].is_empty():
				_arenas[layout.routes[m][layout.stops[m][i]]] = true
	for m in layout.routes.size():
		_find_doors(m, plan.ways_on)
	for m in layout.routes.size():
		_keep_ways(m)
	_close_sides()
	var land: Dictionary = biome["land"]
	for room in layout.rooms_x * layout.rooms_y:
		if _on_route.has(room):
			var share := crowding.x + (crowding.y - crowding.x) * random.below(1000) / 1000.0
			_crowd(room, share, biome["obstacles"])
		else:
			_crowd(room, float(land["crowding"]), land["obstacles"])
	_show_firs()
	_scatter_loose()


## The doors a mission passes: between the rooms of its route, out of its last room the way the
## route goes, and out of the last room on more sides while they are too few for the ways on.
func _find_doors(mission: int, ways_on: int) -> void:
	var layout := draft.layout
	var route: Array = layout.routes[mission]
	for i in route.size():
		var exits: Array[int] = layout.exits(mission, route[i])
		_add_door(route[i], exits.find(1))
	var last: int = route.back()
	var sides := [0, 1, 2, 3].filter(func(s: int) -> bool: return not _has_door(last, s))
	sides = RoomLayout.shuffled(sides, random)
	while 4 - sides.size() < maxi(ceili(ways_on / float(WAYS_A_SIDE)), 1):
		_add_door(last, sides.pop_back())


func _has_door(room: int, side: int) -> bool:
	return _doors.has(room) and _doors[room].has(side)


## A door on a side of a room, and the same one on the room past it.
func _add_door(room: int, side: int) -> void:
	if _has_door(room, side):
		return
	var from := random.range_of(DOOR_FIRST, DOOR_LAST + 1)
	if not _doors.has(room):
		_doors[room] = {}
	_doors[room][side] = from
	var other := draft.layout.beside(room, side)
	if other >= 0:
		if not _doors.has(other):
			_doors[other] = {}
		_doors[other][(side + 2) % 4] = from


## Keeps free the ways through the rooms of a mission's route: the doors and the cells past them,
## the middles, the ways from the doors and the start to the middles; marks the path on them.
func _keep_ways(mission: int) -> void:
	var layout := draft.layout
	for room: int in layout.routes[mission]:
		var o := draft.corner(room)
		var size := ARENA if _arenas.has(room) else MIDDLE
		var low := o + Vector2i.ONE * ((RoomLayout.ROOM - size) / 2)
		_keep_box(low, low + Vector2i.ONE * (size - 1))
		var middle := o + Vector2i.ONE * (RoomLayout.ROOM / 2)
		for side: int in _doors.get(room, {}):
			var cells := door_cells(room, side)
			var step := RoomLayout.STEP[side]
			for c in cells:
				_keep_box(c + step, c + step)
			_keep_box(cells[0], cells[-1] - step * (RoomLayout.ROOM / 2 - 1))
			_mark_path(cells[1] + step, middle)
	var start := layout.start(mission)
	var first := draft.corner(layout.routes[mission][0]) + Vector2i.ONE * (RoomLayout.ROOM / 2)
	_keep_box(start - Vector2i.ONE, start + Vector2i.ONE)
	_mark_path(start, first)


## The cells of a room's door, along its side from its start on.
func door_cells(room: int, side: int) -> Array[Vector2i]:
	const ALONG: Array[Vector2i] = [Vector2i(1, 0), Vector2i(0, 1), Vector2i(1, 0), Vector2i(0, 1)]
	const EDGE: Array[Vector2i] = [Vector2i(0, 6), Vector2i(0, 0), Vector2i(0, 0), Vector2i(6, 0)]
	var first: Vector2i = draft.corner(room) + EDGE[side] + ALONG[side] * int(_doors[room][side])
	var out: Array[Vector2i] = []
	for i in DOOR:
		out.append(first + ALONG[side] * i)
	return out


## Keeps free the cells of the box from one corner to the other, within the rooms.
func _keep_box(a: Vector2i, b: Vector2i) -> void:
	for y in range(mini(a.y, b.y), maxi(a.y, b.y) + 1):
		for x in range(mini(a.x, b.x), maxi(a.x, b.x) + 1):
			if draft.inside(Vector2i(x, y)):
				draft.keep[draft.at(Vector2i(x, y))] = 1


## The path from a cell to another: straight on the way the longer distance goes, then across.
func _mark_path(from: Vector2i, to: Vector2i) -> void:
	var d := to - from
	var turn := Vector2i(to.x, from.y) if absi(d.x) >= absi(d.y) else Vector2i(from.x, to.y)
	for leg: Array in [[from, turn], [turn, to]]:
		var c: Vector2i = leg[0]
		var end: Vector2i = leg[1]
		var step := (end - c).sign()
		while c != end:
			draft.path[draft.at(c)] = 1
			c += step
		draft.path[draft.at(end)] = 1


## Closes the sides of the rooms on the routes but their doors, so that the hero walks from room
## to room only through them, and the ring around the rooms but past the doors.
func _close_sides() -> void:
	## Where the line closing each side starts: the top row of the room below, the room's own
	## left column, its top row, its right column.
	const LINE: Array[Vector2i] = [Vector2i(0, 7), Vector2i(0, 0), Vector2i(0, 0), Vector2i(6, 0)]
	var layout := draft.layout
	for room: int in _on_route:
		var o := draft.corner(room)
		for side in 4:
			var other := layout.beside(room, side)
			if other < 0:
				continue  # the ring closes it
			if side == 1 and _on_route.has(other):
				continue  # the room on the left closes it, in its own column
			var along := Vector2i(1, 0) if side % 2 == 0 else Vector2i(0, 1)
			for i in RoomLayout.ROOM:
				_bar(o + LINE[side] + along * i)
	for y in draft.h:
		for x in draft.w:
			if draft.in_ring(Vector2i(x, y)):
				_bar(Vector2i(x, y))


## A cell of the biome's barrier: the low one in front of a room on a route, the ring's own in
## the ring around the rooms where the biome has one.
func _bar(c: Vector2i) -> void:
	if not draft.open(c):
		return
	var bar: Dictionary = biome["barrier"]
	if _in_front(c):
		bar = biome["low_barrier"]
	elif draft.in_ring(c):
		bar = biome.get("ring", bar)
	draft.put(c, str(bar.get("kind", "")), str(bar.get("prop", "")))


## Whether a cell is in front of a fight: in the front rows (the bottom ones) of a room on a
## route, or in the row right below one.
func _in_front(c: Vector2i) -> bool:
	var room := draft.room_of(c)
	if _on_route.has(room) and c.y - draft.corner(room).y >= RoomLayout.ROOM - FRONT_ROWS:
		return true
	var above := draft.room_of(c - Vector2i(0, 1))
	return _on_route.has(above) and c.y - draft.corner(above).y == RoomLayout.ROOM


## Puts the obstacles into a room until they take `share` of it (with what is there already).
func _crowd(room: int, share: float, obstacles: Array) -> void:
	var o := draft.corner(room)
	var target := roundi(share * RoomLayout.ROOM * RoomLayout.ROOM)
	for i in TRIES:
		if _taken(room) >= target:
			return
		var spec := _pick(obstacles)
		var at := o + Vector2i(random.below(RoomLayout.ROOM), random.below(RoomLayout.ROOM))
		var cells := _shape(spec, at)
		if _fits(room, cells, spec):
			_place(cells, spec)


## The blocked cells of a room.
func _taken(room: int) -> int:
	var o := draft.corner(room)
	var n := 0
	for y in RoomLayout.ROOM:
		for x in RoomLayout.ROOM:
			n += draft.blocked[draft.at(o + Vector2i(x, y))]
	return n


## One of the obstacles, the more often the more weight it has.
func _pick(obstacles: Array) -> Dictionary:
	var total := 0
	for spec: Dictionary in obstacles:
		total += int(spec["weight"])
	var roll := random.below(total)
	for spec: Dictionary in obstacles:
		roll -= int(spec["weight"])
		if roll < 0:
			return spec
	return obstacles.back()


## The cells of an obstacle from a cell on (its top left one, or where a clump grows from).
func _shape(spec: Dictionary, at: Vector2i) -> Array[Vector2i]:
	var size: Array = spec["size"]
	var n := random.range_of(int(size[0]), int(size[1]) + 1)
	var out: Array[Vector2i] = [at]
	match str(spec["shape"]):
		"line":
			var along := Vector2i(1, 0) if random.below(2) == 0 else Vector2i(0, 1)
			for i in range(1, n):
				out.append(at + along * i)
		"block":
			var down := random.range_of(int(size[0]), int(size[1]) + 1)
			out.clear()
			for y in down:
				for x in n:
					out.append(at + Vector2i(x, y))
		"clump":
			for i in n * CLUMP_STEPS:
				if out.size() >= n:
					break
				var c: Vector2i = out[random.below(out.size())] + RoomLayout.STEP[random.below(4)]
				if not out.has(c):
					out.append(c)
	return out


## Whether an obstacle's cells may go into a room: all in it, open, a tall one not in front of
## a fight, a tent or a hut not touching another one (they would be drawn as one).
func _fits(room: int, cells: Array[Vector2i], spec: Dictionary) -> bool:
	var prop := str(spec.get("prop", ""))
	for c in cells:
		if draft.room_of(c) != room or not draft.open(c):
			return false
		if prop in TALL and _in_front(c):
			return false
		if MapArt.CLUSTERS.has(prop):
			for step in RoomLayout.STEP:
				var n := c + step
				if draft.inside(n) and draft.props[draft.at(n)] == prop and not cells.has(n):
					return false
	return true


func _place(cells: Array[Vector2i], spec: Dictionary) -> void:
	var last_row := -1
	for c in cells:
		last_row = maxi(last_row, c.y)
	var face := str(spec.get("face", ""))
	for c in cells:
		var kind := face if face != "" and c.y == last_row else str(spec.get("kind", ""))
		draft.put(c, kind, str(spec.get("prop", "")))


## Of the firs in a column, from its foot up, every other one becomes a bush.
func _show_firs() -> void:
	for x in draft.w:
		for y in range(draft.h - 2, -1, -1):
			var i := draft.at(Vector2i(x, y))
			if draft.props[i] == "fir" and draft.props[i + draft.w] == "fir":
				draft.props[i] = "bush"


## Small things lying on the free cells off the path (tufts, pebbles), each at its share of them.
func _scatter_loose() -> void:
	const IN := 1000
	for i in draft.w * draft.h:
		if draft.blocked[i] == 1 or draft.path[i] == 1 or draft.props[i] != "":
			continue
		var roll := random.below(IN)
		for loose: Array in biome["loose"]:
			roll -= roundi(float(loose[1]) * IN)
			if roll < 0:
				draft.props[i] = str(loose[0])
				break
