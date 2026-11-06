extends RefCounted
## The map part of the game, tick by tick, as the original runs it (pyport/pow/game
## map_engine.py and map_scene.py are the reference). Everything is in original pixels
## (a tile is 27 px) and whole numbers; one tick is 120 ms. The 3D screen only draws
## this state, so the behaviour stays the original one whatever the picture looks like.
##
## Ported so far: rooms and their phases (banners, cleared, exits, scrolling to the next
## room), the hero's walking and running with the original wall, corner and room checks.
## Enemies are not ported yet: like the original's "map without enemies" mode, a room's
## enemy list counts as defeated at once, and a room with a general stays closed.

const Rooms := preload("res://scripts/world/rooms.gd")
const TABLES_PATH := "res://data/tables.json"
const TICK_MS := 120  # speed 2 of the original (speed_frame_ms)
const END := 200  # animation frame numbers above this end the animation (222 = loop end)

## Banners shown over the map (the original's popups 8 and 9).
const BANNER_STAGE := 8
const BANNER_STAGE_CLEAR := 9
const BANNER_TICKS := 20

static var _tables: Dictionary = {}


class Actor:
	var pos := Vector2i.ZERO
	var dir := 0  # 8-direction: 0 down, 2 left, 4 up, 6 right
	var facing := 0
	var action := 0  # 0 stand, 1 walk, 2 run, ...
	var frame := 0
	var slide := Vector2i.ZERO  # the corner-slide step (slide_target)
	var shown_dir := 0  # the direction of the last drawn tick
	var idle_ticks := 20


var map: Dictionary
var w := 0
var h := 0
var flags: Array = []
var objects: Array = []
var rooms: RefCounted
var cell := 0  # the current room
var room_phase := 2  # 0 playing, 1 cleared (exits open), 2 entered (banner), 3 just cleared
var room_phase_timer := 1
var exit_dir := 0  # 1 down 2 left 3 up 4 right while scrolling to the next room
var exit_blink := 0
var scrolling := false
var rooms_visited := 1
var waves: Array = []  # the current room's enemy list, flat: kind, count, kind, count, ...
var banner := 0
var banner_timer := 0
var hero := Actor.new()
var dir_history: Array[int] = [-1, -1, -1, -1, -1]
var hold_to_move := true  # the port's option (the player asked for it): walk while held


static func tables() -> Dictionary:
	if _tables.is_empty():
		var f := FileAccess.open(TABLES_PATH, FileAccess.READ)
		if f != null:
			var data: Variant = JSON.parse_string(f.get_as_text())
			if typeof(data) == TYPE_DICTIONARY:
				_tables = data
	return _tables


static func table(name: String) -> Array:
	return tables().get(name, [])


func _init(map_data: Dictionary = {}, mission: int = 0, start_tile: Vector2i = Vector2i(4, 4)) -> void:
	if map_data.is_empty():
		return
	map = map_data
	w = int(map.w)
	h = int(map.h)
	flags = map.flags
	objects = map.objects
	rooms = Rooms.new(map, mission)
	hero.pos = Vector2i(start_tile.x * 27 + 12, start_tile.y * 27 + 20)
	cell = room_of(hero.pos)
	enter_room()


## The room of a pixel position (the original takes the cell of (x, y - 6)).
func room_of(p: Vector2i) -> int:
	return rooms.room_at(Vector3(p.x / 27.0, 0.0, p.y / 27.0))


func room_origin() -> Vector2i:
	return rooms.room_xy(cell)


func enter_room() -> void:
	waves.clear()
	var list: Array = rooms.cells[cell].get("waves", []) if cell < rooms.cells.size() else []
	for v in list:
		waves.append(int(v))
	while waves.size() < 14:
		waves.append(0)
	room_phase = 2
	room_phase_timer = 1


# ---- one tick ----------------------------------------------------------------------------

## One tick. held: the 8-direction of the held direction key (0, 2, 4, 6) or -1.
## pressed: a direction key pressed this tick (-1 none), for the original's tap-to-walk.
func tick(held: int, pressed: int = -1, fire: bool = false) -> void:
	if banner != 0:
		_tick_banner(fire)
		return
	if scrolling:
		_tick_scroll()
		return
	_tick_scene(held, pressed)
	_end_tick()


func _tick_banner(fire: bool) -> void:
	if fire and banner_timer > 2:
		banner_timer = 2
	banner_timer -= 1
	if banner_timer <= 0:
		var b := banner
		banner = 0
		if b == BANNER_STAGE_CLEAR:
			# Room cleared: the exits open (a room with the mission's general talks instead).
			room_phase = 1
			room_phase_timer = 5


func _show_banner(kind: int) -> void:
	banner = kind
	banner_timer = BANNER_TICKS


func _tick_scene(held: int, pressed: int) -> void:
	_spawn_next_enemy()
	hero.frame += 1
	dir_history[0] = pressed
	var anim := hero_anim(hero.action, hero.dir)
	if hero.frame >= anim.size() or int(anim[hero.frame]) > END:
		if hero.action == 2:
			for i in 5:
				dir_history[i] = -1
			pressed = -1
		hero.frame = 0
		if hero.action != 1:
			hero.action = 0
	if hold_to_move and pressed == -1 and hero.action < 2:
		_hold_to_move(held)
	if hero.action < 2:
		_start_hero_action(pressed)
	_move_hero()


func _hold_to_move(held: int) -> void:
	if held < 0:
		if hero.action == 1:
			hero.action = 0
			hero.frame = 0
	elif hero.action == 0 or hero.facing != held:
		hero.dir = held
		hero.facing = held
		hero.action = 1
		hero.frame = 0


func _start_hero_action(pressed: int) -> void:
	if pressed > -1:
		if check_run():
			hero.action = 2
			hero.frame = 0
			hero.dir = pressed
			hero.facing = pressed
		elif hero.facing == pressed:
			hero.action = (hero.action + 1) & 1
			hero.frame = 0
		else:
			hero.dir = pressed
			hero.facing = pressed
			hero.action = 1
			hero.frame = 0


## A direction pressed twice quickly: run.
func check_run() -> bool:
	if dir_history[0] > -1:
		return dir_history[0] == dir_history[1] or dir_history[0] == dir_history[2]
	return false


func _move_hero() -> void:
	var dx8 := table("dir_dx8")
	var dy8 := table("dir_dy8")
	var step_x := 0
	var step_y := 0
	var move_dir := hero.facing
	match hero.action:
		1:
			step_x = int(dx8[move_dir])
			step_y = int(dy8[move_dir])
		2:
			step_x = int(dx8[move_dir]) << 2
			step_y = int(dy8[move_dir]) << 2
	if step_x != 0 or step_y != 0:
		var i := move(hero.pos, step_x, step_y, move_dir, hero)
		if hero.action == 1:
			if hero.facing in [0, 2, 4, 6]:
				if i == -1:  # a wall: slide around the corner
					i = slide_corner(hero.pos, hero.dir, hero)
					if i != -1:
						i = move(hero.pos, int(dx8[i]), int(dy8[i]), i, hero)
						if i > -1 and i < 8:
							hero.dir = i
			elif i != -1 and i != 9:
				hero.dir = i


func _end_tick() -> void:
	# The tick is drawn with the direction it moved in (a slide can turn it), then the
	# hero looks where he faces again.
	hero.shown_dir = hero.dir
	hero.dir = hero.facing
	hero.idle_ticks += 1
	for i in range(4, 0, -1):
		dir_history[i] = dir_history[i - 1]
	dir_history[0] = -1
	if room_phase == 0:
		return
	if room_phase_timer < 1:
		match room_phase:
			1:
				if exit_dir != 0:
					scrolling = true
					room_phase = 0
					exit_blink = 1
				if room_phase_timer == 0:
					exit_blink = 2
					room_phase_timer -= 1
			2:
				_show_banner(BANNER_STAGE)
				room_phase = 0
			3:
				_show_banner(BANNER_STAGE_CLEAR)
				room_phase = 0
		return
	room_phase_timer -= 1


## The exits are open and their arrows shown.
func exits_open() -> bool:
	return room_phase == 1 and room_phase_timer < 0


# ---- enemies (not ported yet) --------------------------------------------------------------

func _spawn_next_enemy() -> void:
	# As the original's map without enemies: the room's list counts as defeated at once,
	# except a list with a general (kind < 200), which only the combat can end.
	for k in range(0, 14, 2):
		if waves[k] > 0 and waves[k] < 200:
			return
	if room_phase == 0 and waves[0] != 0:
		for k in 14:
			waves[k] = 0
		room_phase = 3
		room_phase_timer = 5


# ---- rooms and walls (map_engine) ------------------------------------------------------------

## Room edges in pixels: 27 + 189 k, as the original's table (x 3 / 2).
static func edge(k: int) -> int:
	return 27 + 189 * k


## Keeps a step inside the room; touching an edge while the room is open leaves it.
func keep_in_room(pos: Vector2i, dx: int, dy: int) -> Vector2i:
	var o := room_origin()
	var dest := pos + Vector2i(dx, dy)
	if dest.x < edge(o.x) + 12:
		dx = edge(o.x) + 12 - pos.x
		if room_phase == 1:
			leave_room(Rooms.EXIT_LEFT)
	elif dest.x > edge(o.x + 1) - 12:
		dx = edge(o.x + 1) - 12 - pos.x
		if room_phase == 1:
			leave_room(Rooms.EXIT_RIGHT)
	if dest.y < edge(o.y) + 10:
		dy = edge(o.y) + 10 - pos.y
		if room_phase == 1:
			leave_room(Rooms.EXIT_UP)
	elif dest.y > edge(o.y + 1) + 10:
		dy = edge(o.y + 1) + 10 - pos.y
		if room_phase == 1:
			leave_room(Rooms.EXIT_DOWN)
	return Vector2i(dx, dy)


func leave_room(exit_no: int) -> void:
	if room_phase_timer < 0 and rooms.has_exit(cell, exit_no):
		exit_dir = exit_no
		var next: int = rooms.neighbour(cell, exit_no)
		if next >= 0 and next < rooms.count():
			cell = next
		exit_blink = 0


## Scrolling to the next room: the hero is pushed inside it, after 6 ticks the room starts.
func _tick_scroll() -> void:
	var d := keep_in_room(hero.pos, 0, 0)
	hero.pos += d
	exit_blink += 1
	if exit_blink > 6:
		scrolling = false
		exit_dir = 0
		rooms_visited += 1
		enter_room()


func cell_free(q: int) -> bool:
	if q < 0 or q >= w * h:
		return false
	return (int(flags[q]) & 1) == 0 and int(objects[q]) == 0


func _cell_at(q: int) -> int:
	return clampi(q, 0, w * h - 1)


## Steps `step` px towards `direction` (0, 2, 4, 6) and shortens it until no wall is hit.
func step_until_free(pos: Vector2i, step: int, direction: int) -> int:
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
			var q := _cell_at(c.y * w + c.x)
			if (int(flags[q]) & 1) != 0 or int(objects[q]) != 0:
				walls += 1
		if walls == 0:
			return step
		step = step - signi(step)
		if step == 0:
			return 0
	return 0


static func straighten_step(delta: int, row: int) -> int:
	const STEPS := [[0, 1, 1, 2, 3, 4, 4, 5, 6, 7, 7, 8, 8, 9, 10, 10, 11],
		[0, 2, 3, 4, 6, 7, 8, 9, 11, 13, 14, 16, 17, 18, 20, 21, 23]]
	if delta < 0:
		return -int(STEPS[row][mini(16, -delta)])
	return int(STEPS[row][mini(16, delta)])


## Moves pos (in place). Returns the direction moved, -1 blocked, 9 stopped by an actor.
func move(pos: Vector2i, dx: int, dy: int, direction: int, actor: Actor) -> int:
	var sx := 0
	var sy := 0
	if direction == 8:
		dx = actor.slide.x
		dy = actor.slide.y
	else:
		if dx > 0:
			sx = step_until_free(pos, dx, 6)
		elif dx < 0:
			sx = step_until_free(pos, dx, 2)
		if dy > 0:
			sy = step_until_free(pos, dy, 0)
		elif dy < 0:
			sy = step_until_free(pos, dy, 4)
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
				sx = step_until_free(pos, straighten_step(dx, 1), hx)
			elif sy != 0:
				direction = vy
				sy = step_until_free(pos, straighten_step(dy, 1), vy)
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
	var d := keep_in_room(pos, sx, sy)
	if d != Vector2i.ZERO:
		d = blocked_by_actor(pos, d.x, d.y, actor)
		if d == Vector2i.ZERO:
			return 9
	actor.pos = pos + d
	return direction


## Not walking into other actors (no enemies yet: nothing blocks).
func blocked_by_actor(_pos: Vector2i, dx: int, dy: int, _actor: Actor) -> Vector2i:
	return Vector2i(dx, dy)


## Slide around a corner: the new direction (8 = the slide step in actor.slide) or -1.
func slide_corner(pos: Vector2i, direction: int, actor: Actor) -> int:
	var tx := pos.x / 27
	var ty := pos.y / 27
	var c := tx + ty * w
	var free_side := [false, false]
	var open_side := [true, true]
	var side := 1 if direction in [0, 6] else -1
	if direction in [0, 4]:
		if cell_free(c + w * side):
			actor.slide.y = 0
			var e := tx * 27 + 8
			if pos.x > e:
				actor.slide.x = -3 if pos.x - e > 3 else e - pos.x
			else:
				actor.slide.x = 3 if e - pos.x > 3 else e - pos.x
			return 8
		for b in range(1, 6):
			if tx + b < w:
				if cell_free(c + b) and open_side[0]:
					if cell_free(c + b + w * side):
						free_side[0] = true
				else:
					open_side[0] = false
			if tx - b > -1:
				if cell_free(c - b) and open_side[1]:
					if cell_free(c - b + w * side):
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
		if cell_free(c + side):
			actor.slide.x = 0
			var e := ty * 27 + 20
			if pos.y > e:
				actor.slide.y = -4 if pos.y - e > 4 else e - pos.y
			else:
				actor.slide.y = 4 if e - pos.y > 4 else e - pos.y
			return 8
		for b in range(1, 6):
			if ty + b < h:
				if cell_free(c + b * w) and open_side[0]:
					if cell_free(c + b * w + side):
						free_side[0] = true
				else:
					open_side[0] = false
			if ty - b > -1:
				if cell_free(c - b * w) and open_side[1]:
					if cell_free(c - b * w + side):
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


# ---- the hero's animation tables ---------------------------------------------------------------

## The hero's frame list for an action and 8-direction (as the original builds hero.anims).
func hero_anim(action: int, dir8: int) -> Array:
	var dir4: int = int(table("dir8_to_dir4")[dir8])
	var names := {0: "hero_anim_0", 1: "hero_anim_1", 2: "hero_anim_2", 9: "hero_anim_9",
		3: "hero_anim_3", 4: "hero_anim_4", 5: "hero_anim_5", 6: "hero_anim_6", 7: "hero_anim_7",
		8: "hero_anim_8", 11: "hero_anim_11", 12: "hero_anim_12", 13: "hero_anim_13",
		14: "hero_anim_14", 20: "hero_anim_20", 21: "hero_anim_21", 22: "hero_anim_22",
		25: "hero_anim_25", 26: "hero_anim_26_27", 27: "hero_anim_26_27"}
	var flat := {10: "hero_anim_10", 15: "hero_anim_15_19", 16: "hero_anim_15_19",
		17: "hero_anim_15_19", 18: "hero_anim_15_19", 19: "hero_anim_15_19",
		23: "hero_anim_23_24", 24: "hero_anim_23_24", 28: "hero_anim_28", 29: "hero_anim_29",
		30: "hero_anim_30"}
	if names.has(action):
		return table(names[action])[dir4]
	if flat.has(action):
		return table(flat[action])
	return [0, 222]


## The sprite frame the hero shows now.
func hero_sprite_frame() -> int:
	var anim := hero_anim(hero.action, hero.shown_dir)
	var f := clampi(hero.frame, 0, anim.size() - 1)
	var v := int(anim[f])
	return v if v <= END else int(anim[0])
