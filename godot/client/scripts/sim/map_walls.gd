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


## Moves pos (in place). Returns the direction moved, -1 blocked, 9 stopped by an actor.
static func move(
	sim: MapSim, pos: Vector2i, dx: int, dy: int, direction: int, actor: MapActor
) -> int:
	var sx := 0
	var sy := 0
	if direction == 8:
		dx = actor.slide.x
		dy = actor.slide.y
	else:
		if dx > 0:
			sx = step_until_free(sim, pos, dx, 6)
		elif dx < 0:
			sx = step_until_free(sim, pos, dx, 2)
		if dy > 0:
			sy = step_until_free(sim, pos, dy, 0)
		elif dy < 0:
			sy = step_until_free(sim, pos, dy, 4)
	if direction in [2, 6]:
		if sx == 0:
			return -1
	elif direction in [0, 4]:
		if sy == 0:
			return -1
	elif direction in [1, 3, 5, 7]:
		# diagonal: if one axis is blocked, go straight along the other one
		var hx: int = {1: 2, 3: 2, 5: 6, 7: 6}[direction]
		var vy: int = {1: 0, 3: 4, 5: 4, 7: 0}[direction]
		if not (sx != 0 and sy != 0):
			if sx != 0:
				direction = hx
				sx = step_until_free(sim, pos, MapGeometry.straighten_step(dx, 1), hx)
			elif sy != 0:
				direction = vy
				sy = step_until_free(sim, pos, MapGeometry.straighten_step(dy, 1), vy)
			else:
				return -1
	elif direction == 8:
		sx = actor.slide.x
		sy = actor.slide.y
		if sx > 0:
			direction = 6
		elif sx < 0:
			direction = 2
		elif sy > 0:
			direction = 0
		elif sy < 0:
			direction = 4
	var d := MapRoomPlay.keep_in_room(sim, pos, sx, sy)
	if d != Vector2i.ZERO:
		d = blocked_by_actor(pos, d.x, d.y, actor)
		if d == Vector2i.ZERO:
			return 9
	actor.pos = pos + d
	return direction


## Not walking into other actors. The game's own check shortens nothing (its result is
## never used), so actors pass through each other, as in the original.
static func blocked_by_actor(_pos: Vector2i, dx: int, dy: int, _actor: MapActor) -> Vector2i:
	return Vector2i(dx, dy)


## Slide around a corner: the new direction (8 = the slide step in actor.slide) or -1.
static func slide_corner(sim: MapSim, pos: Vector2i, direction: int, actor: MapActor) -> int:
	var tx := pos.x / 27
	var ty := pos.y / 27
	var c := tx + ty * sim.w
	var free_side := [false, false]
	var open_side := [true, true]
	var side := 1 if direction in [0, 6] else -1
	if direction in [0, 4]:
		if cell_free(sim, c + sim.w * side):
			actor.slide.y = 0
			var e := tx * 27 + 8
			if pos.x > e:
				actor.slide.x = -3 if pos.x - e > 3 else e - pos.x
			else:
				actor.slide.x = 3 if e - pos.x > 3 else e - pos.x
			return 8
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
	elif direction in [2, 6]:
		if cell_free(sim, c + side):
			actor.slide.x = 0
			var e := ty * 27 + 20
			if pos.y > e:
				actor.slide.y = -4 if pos.y - e > 4 else e - pos.y
			else:
				actor.slide.y = 4 if e - pos.y > 4 else e - pos.y
			return 8
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
