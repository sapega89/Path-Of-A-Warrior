class_name MapWalls
extends RefCounted
## Moving on the map: the walls and objects of the cells, steps that stop at them, and the slide
## round a corner.
## Static functions over the state of a MapSim (MapSim.tick() runs them).


static func cell_free(sim: MapSim, q: int) -> bool:
	if q < 0 or q >= sim.w * sim.h:
		return false
	return (int(sim.flags[q]) & 1) == 0 and int(sim.objects[q]) == 0


static func _cell_at(sim: MapSim, q: int) -> int:
	return clampi(q, 0, sim.w * sim.h - 1)


## Steps `step` px towards `direction` (0, 2, 4, 6) and shortens it until no wall is hit.
static func step_until_free(sim: MapSim, pos: Vector2i, step: int, direction: int) -> int:
	while true:
		var c0 := Vector2i.ZERO
		var c1 := Vector2i.ZERO
		match direction:
			2:
				c0 = Vector2i((pos.x + step - 12) / 27, (pos.y - 20) / 27)
				c1 = Vector2i(c0.x, (pos.y + 6) / 27)
			6:
				c0 = Vector2i((pos.x + step + 12) / 27, (pos.y - 20) / 27)
				c1 = Vector2i(c0.x, (pos.y + 6) / 27)
			4:
				c0 = Vector2i((pos.x - 12) / 27, (pos.y + step - 20) / 27)
				c1 = Vector2i((pos.x + 12) / 27, c0.y)
			0:
				c0 = Vector2i((pos.x - 12) / 27, (pos.y + step + 6) / 27)
				c1 = Vector2i((pos.x + 12) / 27, c0.y)
		var walls := 0
		for c in [c0, c1]:
			var q := _cell_at(sim, c.y * sim.w + c.x)
			if (int(sim.flags[q]) & 1) != 0 or int(sim.objects[q]) != 0:
				walls += 1
		if walls == 0:
			return step
		step = step - signi(step)
		if step == 0:
			return 0
	return 0


## The step (dx, dy) shortened on each axis until no wall is hit.
static func free_step(sim: MapSim, pos: Vector2i, dx: int, dy: int) -> Vector2i:
	var sx := 0
	var sy := 0
	if dx > 0:
		sx = step_until_free(sim, pos, dx, 6)
	elif dx < 0:
		sx = step_until_free(sim, pos, dx, 2)
	if dy > 0:
		sy = step_until_free(sim, pos, dy, 0)
	elif dy < 0:
		sy = step_until_free(sim, pos, dy, 4)
	return Vector2i(sx, sy)


## One step towards the 8-direction `dir` (the table dir_dx8 / dir_dy8).
static func dir_step(dir: int) -> Vector2i:
	return Vector2i(int(MapSim.table("dir_dx8")[dir]), int(MapSim.table("dir_dy8")[dir]))


## The step of a skill's frame towards `dir`, by the hero's numbers of the skills (a general's
## are 6 lower); the other skills stand still:
## 12 a step four times as long on frames 3..5; 13 a dash on frames 5..7 (the actor first
## moves four steps at once, as far as the walls let) and a step; 14 a step on frames 1..8;
## 20 a step on its even frames.
static func skill_step(sim: MapSim, actor: MapActor, skill: int, frame: int, dir: int) -> Vector2i:
	var step := dir_step(dir)
	match skill:
		12:
			if frame > 2 and frame < 6:
				return step * 4
		13:
			if frame > 4 and frame < 8:
				var d := free_step(sim, actor.pos, step.x * 4, step.y * 4)
				actor.pos += MapRoomPlay.keep_in_room(sim, actor.pos, d.x, d.y)
				return step
		14:
			if frame > 0 and frame < 9:
				return step
		20:
			if (frame & 1) == 0:
				return step
	return Vector2i.ZERO


## Moves pos (in place). Returns the direction moved, -1 blocked, 9 stopped by an actor.
static func move(
	sim: MapSim, pos: Vector2i, dx: int, dy: int, direction: int, actor: MapActor
) -> int:
	var s := actor.slide
	if direction != 8:
		s = free_step(sim, pos, dx, dy)
	if direction in [2, 6]:
		if s.x == 0:
			return -1
	elif direction in [0, 4]:
		if s.y == 0:
			return -1
	elif direction in [1, 3, 5, 7]:
		if s.x == 0 or s.y == 0:
			# diagonal: one axis is blocked, go straight along the other one
			var straight := _straighten(sim, pos, dx, dy, direction, s)
			if straight.is_empty():
				return -1
			direction = straight[0]
			s = straight[1]
	elif direction == 8:
		direction = _slide_direction(s)
	var d := MapRoomPlay.keep_in_room(sim, pos, s.x, s.y)
	if d != Vector2i.ZERO:
		d = blocked_by_actor(pos, d.x, d.y, actor)
		if d == Vector2i.ZERO:
			return 9
	actor.pos = pos + d
	return direction


## A diagonal step `s` with an axis blocked: [the straight direction, its step] along the
## free axis, [] when both are blocked.
static func _straighten(
	sim: MapSim, pos: Vector2i, dx: int, dy: int, direction: int, s: Vector2i
) -> Array:
	if s.x != 0:
		var hx: int = {1: 2, 3: 2, 5: 6, 7: 6}[direction]
		var sx := step_until_free(sim, pos, MapGeometry.straighten_step(dx, 1), hx)
		return [hx, Vector2i(sx, s.y)]
	if s.y != 0:
		var vy: int = {1: 0, 3: 4, 5: 4, 7: 0}[direction]
		var sy := step_until_free(sim, pos, MapGeometry.straighten_step(dy, 1), vy)
		return [vy, Vector2i(s.x, sy)]
	return []


## The direction (0, 2, 4, 6) of a corner-slide step.
static func _slide_direction(s: Vector2i) -> int:
	if s.x > 0:
		return 6
	if s.x < 0:
		return 2
	if s.y > 0:
		return 0
	if s.y < 0:
		return 4
	return 8


## Not walking into other actors. The game's own check shortens nothing (its result is
## never used), so actors pass through each other, as in the original.
static func blocked_by_actor(_pos: Vector2i, dx: int, dy: int, _actor: MapActor) -> Vector2i:
	return Vector2i(dx, dy)


## Slide around a corner: the new direction (8 = the slide step in actor.slide) or -1.
static func slide_corner(sim: MapSim, pos: Vector2i, direction: int, actor: MapActor) -> int:
	var side := 1 if direction in [0, 6] else -1
	if direction in [0, 4]:
		return _slide_up_down(sim, pos, side, actor)
	if direction in [2, 6]:
		return _slide_left_right(sim, pos, side, actor)
	return -1


## Walking down (side 1) or up (-1) into a wall: a slide step onto the free cell ahead, or the
## way along the wall (6 right, 2 left) to the nearest opening, -1 none within five cells.
static func _slide_up_down(sim: MapSim, pos: Vector2i, side: int, actor: MapActor) -> int:
	var tx := pos.x / 27
	var c := tx + pos.y / 27 * sim.w
	if cell_free(sim, c + sim.w * side):
		actor.slide.y = 0
		actor.slide.x = _slide_step(pos.x, tx * 27 + 8, 3)
		return 8
	var free_side := [false, false]
	var open_side := [true, true]
	for b in range(1, 6):
		if tx + b < sim.w:
			if cell_free(sim, c + b) and open_side[0]:
				if cell_free(sim, c + b + sim.w * side):
					free_side[0] = true
			else:
				open_side[0] = false
		if tx - b > -1:
			if cell_free(sim, c - b) and open_side[1]:
				if cell_free(sim, c - b + sim.w * side):
					free_side[1] = true
			else:
				open_side[1] = false
		if free_side[0] and free_side[1]:
			return 6 if pos.x - tx * 27 > 8 else 2
		if free_side[0]:
			return 6
		if free_side[1]:
			return 2
	return -1


## Walking right (side 1) or left (-1) into a wall: as _slide_up_down, along the wall down (0)
## or up (4).
static func _slide_left_right(sim: MapSim, pos: Vector2i, side: int, actor: MapActor) -> int:
	var ty := pos.y / 27
	var c := pos.x / 27 + ty * sim.w
	if cell_free(sim, c + side):
		actor.slide.x = 0
		actor.slide.y = _slide_step(pos.y, ty * 27 + 20, 4)
		return 8
	var free_side := [false, false]
	var open_side := [true, true]
	for b in range(1, 6):
		if ty + b < sim.h:
			if cell_free(sim, c + b * sim.w) and open_side[0]:
				if cell_free(sim, c + b * sim.w + side):
					free_side[0] = true
			else:
				open_side[0] = false
		if ty - b > -1:
			if cell_free(sim, c - b * sim.w) and open_side[1]:
				if cell_free(sim, c - b * sim.w + side):
					free_side[1] = true
			else:
				open_side[1] = false
		if free_side[0] and free_side[1]:
			return 0 if pos.y - ty * 27 > 8 else 4
		if free_side[0]:
			return 0
		if free_side[1]:
			return 4
	return -1


## From `at` towards `to`, at most `most` px.
static func _slide_step(at: int, to: int, most: int) -> int:
	if at > to:
		return -most if at - to > most else to - at
	return most if to - at > most else to - at
