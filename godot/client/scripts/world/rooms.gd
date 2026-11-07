extends RefCounted
## The rooms of a map, as in the original: the map is a grid of 7x7-tile rooms
## shifted by one tile (room (rx, ry) covers tiles 1 + 7 rx .. 7 + 7 rx across and
## 1 + 7 ry .. 7 + 7 ry down). The hero stays inside the current room; when the room
## is cleared its exits open, and walking into an open edge moves to the next room.
##
## Positions here are world units (1 = one 27 px tile), x across and z down the screen,
## the same as the original pixel position / 27.

const EXIT_DOWN := 1
const EXIT_LEFT := 2
const EXIT_UP := 3
const EXIT_RIGHT := 4
const PX := 27.0
const ROOM_PX := 189.0  # 7 tiles
## Margins of the hero inside the room, original pixels.
const MARGIN_X := 12.0
const MARGIN_TOP := 10.0
const MARGIN_BOTTOM := -10.0  # the bottom edge lets the feet 10 px past the room

var rooms_x := 1
var rooms_y := 1
## Per room: {exits: [down, left, up, right], max_enemies, waves: [12], general}
var cells: Array = []


func _init(map: Dictionary = {}, mission: int = 0) -> void:
	if map.is_empty():
		return
	var r: Dictionary = map.get("rooms", {})
	rooms_x = maxi(int(r.get("rooms_x", 1)), 1)
	rooms_y = maxi(int(r.get("rooms_y", 1)), 1)
	var missions: Array = r.get("missions", [])
	if missions.size() > 0:
		cells = missions[clampi(mission, 0, missions.size() - 1)]


func count() -> int:
	return rooms_x * rooms_y


## The room the position is in (the original takes the cell of (x, z - 6 px)).
func room_at(pos: Vector3) -> int:
	var tx := floori(pos.x)
	var tz := floori(pos.z - 6.0 / PX)
	var rx := clampi(floori((tx - 1) / 7.0), 0, rooms_x - 1)
	var ry := clampi(floori((tz - 1) / 7.0), 0, rooms_y - 1)
	return ry * rooms_x + rx


func room_xy(room: int) -> Vector2i:
	return Vector2i(room % rooms_x, room / rooms_x)


## Where the hero may stand in the room: x and z ranges.
func bounds(room: int) -> Rect2:
	var p := room_xy(room)
	var left := (PX + ROOM_PX * p.x + MARGIN_X) / PX
	var right := (PX + ROOM_PX * (p.x + 1) - MARGIN_X) / PX
	var top := (PX + ROOM_PX * p.y + MARGIN_TOP) / PX
	var bottom := (PX + ROOM_PX * (p.y + 1) - MARGIN_BOTTOM) / PX
	return Rect2(left, top, right - left, bottom - top)


## The middle of the room's 9x9-tile view, for the camera.
func center(room: int) -> Vector3:
	var p := room_xy(room)
	return Vector3(7 * p.x + 4.5, 0.0, 7 * p.y + 4.5)


func exits(room: int) -> Array:
	if room < 0 or room >= cells.size():
		return [0, 0, 0, 0]
	return cells[room].get("exits", [0, 0, 0, 0])


func has_exit(room: int, exit_no: int) -> bool:
	return int(exits(room)[exit_no - 1]) != 0


func neighbour(room: int, exit_no: int) -> int:
	match exit_no:
		EXIT_DOWN:
			return room + rooms_x
		EXIT_LEFT:
			return room - 1
		EXIT_UP:
			return room - rooms_x
		EXIT_RIGHT:
			return room + 1
	return room


## The room's enemy list: [[kind, count], ...] in order (kind >= 200 = soldiers, < 200 = a general).
func waves(room: int) -> Array:
	var out: Array = []
	if room < 0 or room >= cells.size():
		return out
	var w: Array = cells[room].get("waves", [])
	var i := 0
	while i + 1 < w.size() and int(w[i]) != 0:
		out.append([int(w[i]), int(w[i + 1])])
		i += 2
	return out


func has_general(room: int) -> bool:
	for wave in waves(room):
		if wave[0] > 0 and wave[0] < 200:
			return true
	return false


## Keeps a position inside the room. Returns {pos, edge}: edge is the exit number of the
## side that was touched (0 = none), as the original's keep-in-room check.
func keep_inside(room: int, pos: Vector3) -> Dictionary:
	var b := bounds(room)
	var edge := 0
	var p := pos
	if p.x < b.position.x:
		p.x = b.position.x
		edge = EXIT_LEFT
	elif p.x > b.end.x:
		p.x = b.end.x
		edge = EXIT_RIGHT
	if p.z < b.position.y:
		p.z = b.position.y
		edge = EXIT_UP
	elif p.z > b.end.y:
		p.z = b.end.y
		edge = EXIT_DOWN
	return {"pos": p, "edge": edge}


## The room of a start tile (a mission's "start" in campaign.json).
func start_room(tile: Vector2i) -> int:
	return room_at(Vector3(tile.x + 0.5, 0.0, tile.y + 0.75))


## The rooms the hero can walk to from `room` through the exits, `room` first.
func reachable_from(room: int) -> Array:
	var seen := {room: true}
	var out: Array = [room]
	var i := 0
	while i < out.size():
		var r: int = out[i]
		i += 1
		for exit_no in range(EXIT_DOWN, EXIT_RIGHT + 1):
			var n := neighbour(r, exit_no)
			if has_exit(r, exit_no) and n >= 0 and n < count() and not seen.has(n):
				seen[n] = true
				out.append(n)
	return out
