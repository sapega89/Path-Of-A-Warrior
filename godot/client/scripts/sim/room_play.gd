class_name MapRoomPlay
extends RefCounted
## The rooms of a mission as they are played: entering one, its waves and cell scripts, where
## soldiers come in, clearing it, leaving it and scrolling to the next.
## Static functions over the state of a MapSim (MapSim.tick() runs them).


## The room of a pixel position (the original takes the cell of (x, y - 6)).
static func room_of(sim: MapSim, p: Vector2i) -> int:
	return sim.rooms.room_at(Vector3(p.x / 27.0, 0.0, p.y / 27.0))


static func room_origin(sim: MapSim) -> Vector2i:
	return sim.rooms.room_xy(sim.cell)


static func enter_room(sim: MapSim) -> void:
	sim.enemies.clear()
	sim.enemies_alive = 0
	sim.waves.clear()
	var list: Array = (
		sim.rooms.cells[sim.cell].get("waves", []) if sim.cell < sim.rooms.cells.size() else []
	)
	for v in list:
		sim.waves.append(int(v))
	while sim.waves.size() < 14:
		sim.waves.append(0)
	_find_spawn_spots(sim)
	run_cell_scripts(sim)
	MapLoot.find_breakables(sim)
	sim.room_phase = 2
	sim.room_phase_timer = 1


## The scripts of the room's cells (the map's `scripts`): an op [0, mission + 1, kind] puts an
## enemy of kind 200 + kind on its cell in that mission, the archers standing in the room. A
## cell runs its first script, row by row.
static func run_cell_scripts(sim: MapSim) -> void:
	if sim.no_enemies:
		return
	var o := room_origin(sim)
	var rtx := o.x * 7 + 1
	var rty := o.y * 7 + 1
	var cells := {}
	for sc in sim.map.get("scripts", []):
		var at := Vector2i(int(sc.x), int(sc.y))
		if not cells.has(at):
			cells[at] = sc.ops
	for y in range(rty, rty + 7):
		for x in range(rtx, rtx + 7):
			for op in cells.get(Vector2i(x, y), []):
				if int(op[0]) == 0 and int(op[1]) - 1 == sim.mission:
					MapEnemyPlay.create_enemy(sim, int(op[2]) + 200, x, y, 4)


static func max_enemies(sim: MapSim) -> int:
	return (
		int(sim.rooms.cells[sim.cell].get("max_enemies", 0))
		if sim.cell < sim.rooms.cells.size()
		else 0
	)


## The cells of the room the hero can reach (flood fill from his cell over unblocked cells):
## 7x7, 1 reachable, -1 blocked, 0 not reached.
static func find_reachable(sim: MapSim, room_tx: int, room_ty: int, p: Vector2i) -> Array:
	var reach: Array = []
	for x in 7:
		var col: Array = []
		for y in 7:
			col.append(-1 if (int(sim.flags[room_tx + x + (room_ty + y) * sim.w]) & 1) != 0 else 0)
		reach.append(col)
	var sx := clampi(p.x / 27, room_tx, room_tx + 6) - room_tx
	var sy := clampi(p.y / 27, room_ty, room_ty + 6) - room_ty
	reach[sx][sy] = 1  # the hero's own cell, even when it is blocked
	var todo: Array[Vector2i] = [Vector2i(sx, sy)]
	while not todo.is_empty():
		var c: Vector2i = todo.pop_back()
		for d in [Vector2i(0, 1), Vector2i(-1, 0), Vector2i(0, -1), Vector2i(1, 0)]:
			var n: Vector2i = c + d
			if n.x > -1 and n.x < 7 and n.y > -1 and n.y < 7 and reach[n.x][n.y] == 0:
				reach[n.x][n.y] = 1
				todo.append(n)
	return reach


## Where the enemies come in: free cells along each open exit that the hero can reach and
## that have a free cell outside the room behind them.
static func _find_spawn_spots(sim: MapSim) -> void:
	sim.spawn_spots.clear()
	var reach := _reach_from_hero(sim)
	var exits: Array = sim.rooms.exits(sim.cell)
	for side in 4:
		if int(exits[side]) != 0:
			sim.spawn_spots.append_array(_edge_cells(sim, reach, side))


## The sides of the hero's room he can walk out of (Rooms.EXIT_*): a cell along the side he can
## reach with a free cell outside the room behind it, whether or not the side is an exit.
static func open_sides(sim: MapSim) -> Array[int]:
	var reach := _reach_from_hero(sim)
	var out: Array[int] = []
	for side in 4:
		if not _edge_cells(sim, reach, side).is_empty():
			out.append(side + 1)
	return out


static func _reach_from_hero(sim: MapSim) -> Array:
	var o := room_origin(sim)
	return find_reachable(sim, o.x * 7 + 1, o.y * 7 + 1, sim.hero.pos)


## The cells along side `side` (0 down, 1 left, 2 up, 3 right) of the hero's room that he can
## reach (reach: find_reachable) and that have a free cell outside the room behind them:
## Vector3i(x, y, side) each.
static func _edge_cells(sim: MapSim, reach: Array, side: int) -> Array[Vector3i]:
	const EXIT_DX := [0, 0, 0, 6]
	const EXIT_DY := [6, 0, 0, 0]
	const EXIT_STEP := [1, -1, -1, 1]
	var o := room_origin(sim)
	var rtx := o.x * 7 + 1
	var rty := o.y * 7 + 1
	var k: int = rtx + EXIT_DX[side]
	var m: int = rty + EXIT_DY[side]
	var out: Array[Vector3i] = []
	for b in 7:
		if (side & 1) != 0:
			if reach[k - rtx][b] == 1:
				var q := k + (m + b) * sim.w
				if int(sim.objects[q]) == 0 and MapWalls.cell_free(sim, q + EXIT_STEP[side]):
					out.append(Vector3i(k, m + b, side))
		elif reach[b][m - rty] == 1:
			var q := k + b + m * sim.w
			if int(sim.objects[q]) == 0 and MapWalls.cell_free(sim, q + EXIT_STEP[side] * sim.w):
				out.append(Vector3i(k + b, m, side))
	return out


## Keeps a step inside the room; touching an edge while the room is open leaves it.
static func keep_in_room(sim: MapSim, pos: Vector2i, dx: int, dy: int) -> Vector2i:
	var o := room_origin(sim)
	var dest := pos + Vector2i(dx, dy)
	var touched := 0
	if dest.x < MapGeometry.edge(o.x) + 12:
		dx = MapGeometry.edge(o.x) + 12 - pos.x
		touched = Rooms.EXIT_LEFT
	elif dest.x > MapGeometry.edge(o.x + 1) - 12:
		dx = MapGeometry.edge(o.x + 1) - 12 - pos.x
		touched = Rooms.EXIT_RIGHT
	if touched != 0 and sim.room_phase == 1:
		leave_room(sim, touched)
	var touched_y := 0
	if dest.y < MapGeometry.edge(o.y) + 10:
		dy = MapGeometry.edge(o.y) + 10 - pos.y
		touched_y = Rooms.EXIT_UP
	elif dest.y > MapGeometry.edge(o.y + 1) + 10:
		dy = MapGeometry.edge(o.y + 1) + 10 - pos.y
		touched_y = Rooms.EXIT_DOWN
	if touched_y != 0 and sim.room_phase == 1:
		leave_room(sim, touched_y)
	if sim.choosing and (touched != 0 or touched_y != 0):
		sim.way_out = touched_y if touched_y != 0 else touched
	return Vector2i(dx, dy)


static func leave_room(sim: MapSim, exit_no: int) -> void:
	if sim.room_phase_timer < 0 and sim.rooms.has_exit(sim.cell, exit_no):
		sim.exit_dir = exit_no
		var next: int = sim.rooms.neighbour(sim.cell, exit_no)
		if next >= 0 and next < sim.rooms.count():
			sim.cell = next
		sim.exit_blink = 0


## Scrolling to the next room: the hero is pushed inside it, after 6 ticks the room starts.
static func tick_scroll(sim: MapSim) -> void:
	var d := keep_in_room(sim, sim.hero.pos, 0, 0)
	sim.hero.pos += d
	sim.exit_blink += 1
	if sim.exit_blink > 6:
		sim.scrolling = false
		sim.exit_dir = 0
		sim.rooms_visited += 1
		enter_room(sim)


## The middle of the room on the screen, where the big skills show.
static func room_middle(sim: MapSim) -> Vector2i:
	var o := room_origin(sim)
	return Vector2i(o.x * 7 * 27 + 120, o.y * 7 * 27 + 131)
