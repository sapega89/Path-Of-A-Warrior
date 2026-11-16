class_name RoomPath
extends RefCounted
## Walking through the hero's room by its free cells (MapWalls.cell_free), or through the
## things to break on them too, as the autopilot does: how many steps each cell is from some
## others, and the direction to hold to step from the hero's cell to the next one.
## The hero is 24 px wide and 26 px tall in cells of 27 px: he goes between two walls only when
## he stands across the step in the middle of his cell. The game's slide along a wall puts him
## there (MapWalls.slide_corner), but for a step up or down with a wall on its left: that slide
## stops 8 px into the cell, where he still reaches the cell on the left, so he steps right
## first.
## Static functions over the state of a MapSim.

const CELL := 27
const ROOM := 7  # cells a side
## The steps by direction / 2: down, left, up, right (the directions 0, 2, 4, 6).
const STEPS: Array[Vector2i] = [Vector2i(0, 1), Vector2i(-1, 0), Vector2i(0, -1), Vector2i(1, 0)]
const LEFT := 2
const RIGHT := 6
## Nearer than this to the left side of his cell, the hero reaches into the cell on its left.
const LEFT_FIT := 12


## The cell of a position (its feet, as the game's slide takes it), kept in the room.
static func cell_of(sim: MapSim, pos: Vector2i) -> Vector2i:
	var corner := _corner(sim)
	return Vector2i(
		clampi(pos.x / CELL, corner.x, corner.x + ROOM - 1),
		clampi(pos.y / CELL, corner.y, corner.y + ROOM - 1)
	)


## How many steps each free cell of the room (with `through_things`, each cell but the walls) is
## from the nearest of `from` (those count 0, free or not): cell -> steps.
static func steps_from(
	sim: MapSim, from: Array[Vector2i], through_things: bool = false
) -> Dictionary:
	var room := Rect2i(_corner(sim), Vector2i.ONE * ROOM)
	var out := {}
	var todo: Array[Vector2i] = []
	for c in from:
		if not out.has(c):
			out[c] = 0
			todo.append(c)
	var i := 0
	while i < todo.size():
		var c := todo[i]
		i += 1
		for step in STEPS:
			var n := c + step
			if room.has_point(n) and not out.has(n) and _open(sim, n, through_things):
				out[n] = int(out[c]) + 1
				todo.append(n)
	return out


## The steps (steps_from) to cell `c`, or to the nearest free cell next to it when it is not
## free (an archer up on a wall); -1 none.
static func steps_to(steps: Dictionary, c: Vector2i) -> int:
	if steps.has(c):
		return int(steps[c])
	var out := -1
	for step in STEPS:
		var n := int(steps.get(c + step, -1))
		if n >= 0 and (out < 0 or n + 1 < out):
			out = n + 1
	return out


## The free cells (with `through_things`, those but the walls) along side `side` (0 down, 1 left,
## 2 up, 3 right) of the room with such a cell outside the room behind them: where the hero
## walks out on that side.
static func ways_out(sim: MapSim, side: int, through_things: bool = false) -> Array[Vector2i]:
	var corner := _corner(sim)
	var room := Rect2i(corner, Vector2i.ONE * ROOM)
	var out: Array[Vector2i] = []
	for y in range(corner.y, corner.y + ROOM):
		for x in range(corner.x, corner.x + ROOM):
			var c := Vector2i(x, y)
			var behind := c + STEPS[side]
			var open := _open(sim, c, through_things) and _open(sim, behind, through_things)
			if open and not room.has_point(behind):
				out.append(c)
	return out


## The direction (0, 2, 4, 6) of the step from the hero's cell to a cell one step nearer by
## `steps` (steps_from the goal); of two as near, the one most along `toward` (a vector). -1: the
## hero's cell is the goal, or no way leads from it.
static func next_step(sim: MapSim, steps: Dictionary, toward: Vector2i) -> int:
	var at := cell_of(sim, sim.hero.pos)
	var left := int(steps.get(at, -1))
	if left <= 0:
		return -1
	var best := -1
	for d in STEPS.size():
		if int(steps.get(at + STEPS[d], -1)) != left - 1:
			continue
		if best < 0 or _along(toward, d) > _along(toward, best):
			best = d
	return best * 2


## The direction to hold to step from cell `at` towards `direction` (0, 2, 4, 6): that one, or
## right first when a step up or down would catch a wall on the left.
static func step_to(sim: MapSim, at: Vector2i, direction: int) -> int:
	if direction == LEFT or direction == RIGHT:
		return direction
	var left := at + STEPS[direction >> 1] + Vector2i.LEFT
	if sim.hero.pos.x - at.x * CELL < LEFT_FIT and not _open(sim, left, false):
		return RIGHT
	return direction


static func _corner(sim: MapSim) -> Vector2i:
	return sim.rooms.room_xy(sim.cell) * ROOM + Vector2i.ONE


## A free cell, or with `through_things` one with no wall.
static func _open(sim: MapSim, c: Vector2i, through_things: bool) -> bool:
	if c.x < 0 or c.x >= sim.w or c.y < 0 or c.y >= sim.h:
		return false
	var q := c.y * sim.w + c.x
	return int(sim.flags[q]) & 1 == 0 and (through_things or int(sim.objects[q]) == 0)


static func _along(toward: Vector2i, d: int) -> int:
	return toward.x * STEPS[d].x + toward.y * STEPS[d].y
