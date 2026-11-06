extends RefCounted
## The map part of the game, tick by tick, as the original runs it (pyport/pow/game
## map_engine.py and map_scene.py are the reference). Everything is in original pixels
## (a tile is 27 px) and whole numbers; one tick is 120 ms. The 3D screen only draws
## this state, so the behaviour stays the original one whatever the picture looks like.
##
## Ported so far: rooms and their phases (banners, cleared, exits, scrolling to the next
## room), the hero's walking, running and sword attacks with the original wall, corner and
## room checks, and the soldiers: the room's waves come in through its exits, swordsmen
## (one or a squad of three) and archers walk, attack and shoot by the original AI, are hit,
## knocked back and die; the last one clears the room. Not yet: generals (a room whose list
## reaches a general waits there), skills, potions, drops and breakable objects.

const Rooms := preload("res://scripts/world/rooms.gd")
const JavaRandom := preload("res://scripts/sim/java_random.gd")
const TABLES_PATH := "res://data/tables.json"
const TICK_MS := 120  # speed 2 of the original (speed_frame_ms)
const END := 200  # animation frame numbers above this end the animation (222 = loop end)

## Banners shown over the map (the original's popups 8 and 9).
const BANNER_STAGE := 8
const BANNER_STAGE_CLEAR := 9
const BANNER_FAILED := 22  # "Mission fail!": waits for a key, then the mission ends
const BANNER_TICKS := 20

const KIND_SWORDS := 201
const KIND_ARCHERS := 202
const KIND_SQUAD := 203  # three swordsmen drawn together, one actor
const SPAWN_DX := [0, -56, 0, 56, 0]
const SPAWN_DY := [56, 0, -56, 0, 0]
const TURNS := [-2, -1, 0, 0, 0, 0, 1, 2]
const ATTACK_PCT := [100, 100, 150]
const BASE_ATTACK := [3, 2, 3]
const BASE_HP := [7, 5, 7]
const ARROW_DX := [-1, -15, -1, 5]
const ARROW_DY := [-5, -13, -30, -13]
const HIT_FRAME := [0, 0, 0, 1, 1, 1, 1, 1, 1]  # the frame of a sword attack (3..8) that hits
## A squad moves as if it stood this far aside (the side its men stand on), by direction.
const SQUAD_SHIFT := {3: Vector2i(-20, 0), 1: Vector2i(-20, 20), 2: Vector2i(-20, 0),
	0: Vector2i(0, 20), 5: Vector2i(20, 0), 7: Vector2i(20, 20), 6: Vector2i(20, 0)}
const GENERAL_REACH := [60, 50]

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
	var prev_pos := Vector2i.ZERO  # the position at the start of the tick (for drawing)
	var type := 0  # enemies: 201 swords, 202 archers, 203 a squad of swords
	var level := 1
	var attack := 0
	var defense := 0
	var attack_buff := 0
	var defense_buff := 0
	var hp := 0
	var max_hp := 0
	var alerted := 0  # 0 while walking in through the exit
	var think_ticks := 0
	var ai_mode := 0  # > 0: knocked back that many ticks
	var hurt_ticks := 0
	var combo := 0
	var weapon_kind := 0  # 0 long sword, 1 short sword


class Arrow:
	var active := false
	var pos := Vector2i.ZERO
	var dir := 0  # 0 down, 1 left, 2 up, 3 right
	var ticks := 0
	var attack := 0
	var w := 2
	var h := 11


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
## The map without enemies (pyport's POW_NO_ENEMIES): a room's list counts as defeated.
var no_enemies := false
var difficulty := 1  # 0 hard, 1 normal (turns the hero to the nearest enemy when he strikes)
var general_side := 0
var rng := JavaRandom.new()
var enemies: Array[Actor] = []  # in drawing order (sorted by y each tick)
var enemies_alive := 0  # archers do not count
var spawn_spots: Array[Vector3i] = []  # tile x, tile y, exit side (0 down 1 left 2 up 3 right)
var arrows: Array[Arrow] = [Arrow.new(), Arrow.new(), Arrow.new()]
var kills := 0
var mission_exp := 0
var failed := false
var finished := false  # the mission is over: the screen leaves
## The last enemy hit or hitting: {name, level, hp_bar (0..60), ticks}.
var target_info := {}


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
	hero.prev_pos = hero.pos
	# A new hero: the base stats (ATK 5, DEF 4, HP 30) and the first sword (+1 ATK).
	hero.level = 1
	hero.attack = 6
	hero.defense = 4
	hero.hp = 30
	hero.max_hp = 30
	cell = room_of(hero.pos)
	enter_room()


## The room of a pixel position (the original takes the cell of (x, y - 6)).
func room_of(p: Vector2i) -> int:
	return rooms.room_at(Vector3(p.x / 27.0, 0.0, p.y / 27.0))


func room_origin() -> Vector2i:
	return rooms.room_xy(cell)


func enter_room() -> void:
	enemies.clear()
	enemies_alive = 0
	waves.clear()
	var list: Array = rooms.cells[cell].get("waves", []) if cell < rooms.cells.size() else []
	for v in list:
		waves.append(int(v))
	while waves.size() < 14:
		waves.append(0)
	_find_spawn_spots()
	room_phase = 2
	room_phase_timer = 1


func max_enemies() -> int:
	return int(rooms.cells[cell].get("max_enemies", 0)) if cell < rooms.cells.size() else 0


## The cells of the room the hero can reach (flood fill from his cell over unblocked cells):
## 7x7, 1 reachable, -1 blocked, 0 not reached.
func find_reachable(room_tx: int, room_ty: int, p: Vector2i) -> Array:
	var reach: Array = []
	for x in 7:
		var col: Array = []
		for y in 7:
			col.append(-1 if (int(flags[room_tx + x + (room_ty + y) * w]) & 1) != 0 else 0)
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
func _find_spawn_spots() -> void:
	spawn_spots.clear()
	var o := room_origin()
	var rtx := o.x * 7 + 1
	var rty := o.y * 7 + 1
	var reach := find_reachable(rtx, rty, hero.pos)
	const EXIT_DX := [0, 0, 0, 6]
	const EXIT_DY := [6, 0, 0, 0]
	const EXIT_STEP := [1, -1, -1, 1]
	var exits: Array = rooms.exits(cell)
	for side in 4:
		if int(exits[side]) == 0:
			continue
		var k: int = rtx + EXIT_DX[side]
		var m: int = rty + EXIT_DY[side]
		for b in 7:
			if (side & 1) != 0:
				if reach[k - rtx][b] == 1:
					var q := k + (m + b) * w
					if int(objects[q]) == 0 and cell_free(q + EXIT_STEP[side]):
						spawn_spots.append(Vector3i(k, m + b, side))
			elif reach[b][m - rty] == 1:
				var q := k + b + m * w
				if int(objects[q]) == 0 and cell_free(q + EXIT_STEP[side] * w):
					spawn_spots.append(Vector3i(k + b, m, side))


# ---- one tick ----------------------------------------------------------------------------

## One tick. held: the 8-direction of the held direction key (0, 2, 4, 6) or -1.
## pressed: a direction key pressed this tick (-1 none), for the original's tap-to-walk.
## fire: the attack key was pressed (it also closes a banner).
func tick(held: int, pressed: int = -1, fire: bool = false) -> void:
	hero.prev_pos = hero.pos
	for e in enemies:
		e.prev_pos = e.pos
	if banner != 0:
		_tick_banner(fire)
		return
	if scrolling:
		_tick_scroll()
		return
	_tick_scene(held, pressed, 3 if fire else 0)
	if banner == 0:
		_end_tick()


func _tick_banner(fire: bool) -> void:
	if banner == BANNER_FAILED:
		if fire:
			finished = true
		return
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


func _tick_scene(held: int, pressed: int, skill: int) -> void:
	_spawn_next_enemy()
	hero.frame += 1
	dir_history[0] = pressed
	var anim := hero_anim(hero.action, hero.dir)
	if hero.frame >= anim.size() or int(anim[hero.frame]) > END:
		if hero.action == 2:
			for i in 5:
				dir_history[i] = -1
			pressed = -1
		elif hero.action == 10:
			# The hero fell: "Mission fail!", then back to the menu.
			hero.frame = 10
			failed = true
			banner = BANNER_FAILED
			return
		hero.frame = 0
		if hero.action != 1:
			hero.action = 0
	if hold_to_move and pressed == -1 and hero.action < 2:
		_hold_to_move(held)
	if hero.action < 2:
		_start_hero_action(pressed, skill)
	_move_hero()
	_hero_action_hits()
	_tick_arrows()
	_tick_enemies()
	_sort_enemies()


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


func _start_hero_action(pressed: int, skill: int = 0) -> void:
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
	if skill == 3:
		# The sword: strikes in quick succession make a combo (actions 3-5 short, 6-8 long sword).
		if hero.idle_ticks < 7:
			hero.combo = (hero.combo + 1) % 3
		else:
			hero.combo = 0
		hero.idle_ticks = 0
		hero.action = 3 + hero.combo + (hero.weapon_kind ^ 1) * 3
		hero.frame = 0
		hero.facing = int(table("dir8_to_dir4")[hero.facing]) << 1
		hero.dir = hero.facing


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
	var action := hero.action
	var frame := hero.frame
	if action == 1:
		step_x = int(dx8[move_dir])
		step_y = int(dy8[move_dir])
	elif action == 2:
		step_x = int(dx8[move_dir]) << 2
		step_y = int(dy8[move_dir]) << 2
	elif action >= 3 and action <= 8:
		step_x = int(dx8[move_dir]) / 3
		step_y = int(dy8[move_dir]) / 3
	elif action == 10:
		if frame < 10:
			hero.pos.x += -1 if (frame & 1) != 0 else 1
	elif action == 9 and hero.hurt_ticks > 0:
		hero.hurt_ticks -= 1
		move_dir = (hero.facing + 4) & 7
		step_x = int(dx8[move_dir]) << 2
		step_y = int(dy8[move_dir]) << 2
	elif action == 9 and frame == 1:
		move_dir = (hero.facing + 4) & 7
		step_x = int(dx8[move_dir]) * 3 / 4
		step_y = int(dy8[move_dir]) * 3 / 4
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


## The frame of the hero's action that hits: the enemies in reach are struck.
func _hero_action_hits() -> void:
	var action := hero.action
	if action >= 3 and action <= 8 and hero.frame == HIT_FRAME[action]:
		_turn_to_nearest()
		_hero_attack()


func _end_tick() -> void:
	# The tick is drawn with the direction it moved in (a slide can turn it), then the
	# hero looks where he faces again.
	hero.shown_dir = hero.dir
	hero.dir = hero.facing
	hero.idle_ticks += 1
	if not target_info.is_empty():
		target_info.ticks -= 1
		if target_info.ticks < 1:
			target_info = {}
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


# ---- enemies: waves, AI, hits -------------------------------------------------------------

## The next enemy of the room's list comes in while fewer than the room's maximum are alive.
func _spawn_next_enemy() -> void:
	if no_enemies:
		# The map without enemies: the room's list counts as defeated at once, except a
		# list with a general (kind < 200), which only the fight with him can end.
		for k in range(0, 14, 2):
			if waves[k] > 0 and waves[k] < 200:
				return
		if room_phase == 0 and waves[0] != 0:
			for k in 14:
				waves[k] = 0
			room_phase = 3
			room_phase_timer = 5
		return
	if enemies_alive >= max_enemies() or waves[0] == 0:
		return
	if waves[0] < 200:
		return  # a general: his talk and fight are not ported yet, the room waits here
	if spawn_spots.is_empty():
		return
	var spot: Vector3i = spawn_spots[rng.below(spawn_spots.size())]
	create_enemy(waves[0], spot.x, spot.y, spot.z)
	waves[1] -= 1
	if waves[1] < 1:
		for b in 12:
			waves[b] = waves[b + 2]


## A soldier outside the room behind exit `side`, looking in.
func create_enemy(kind: int, tx: int, ty: int, side: int) -> Actor:
	var e := Actor.new()
	e.pos = Vector2i(tx * 27 + 12 + SPAWN_DX[side], ty * 27 + 20 + SPAWN_DY[side])
	e.prev_pos = e.pos
	e.dir = ((side << 1) + 4) & 7
	e.facing = e.dir
	if kind == KIND_SWORDS and rng.range_of(0, 2) != 0:
		kind = KIND_SQUAD
	e.type = kind
	e.think_ticks = 14
	if kind == KIND_ARCHERS:
		e.alerted = 1
		e.think_ticks = 15
	enemy_stats(e, kind - 201)
	enemies.append(e)
	if kind != KIND_ARCHERS:
		enemies_alive += 1
	return e


## Level, attack, defence and HP of a new soldier (kind 0 swords, 1 archers, 2 squad).
func enemy_stats(e: Actor, kind: int) -> void:
	if hero.level < 21:
		e.level = maxi(hero.level + rng.range_of(0, 5) - 2, 1)
	elif hero.level < 41:
		e.level = hero.level + rng.below(9) - 3
	else:
		e.level = hero.level + rng.below(16) - 5
	e.attack = (BASE_ATTACK[kind] + e.level) * ATTACK_PCT[kind] / 100
	e.defense = e.level - 1
	e.hp = BASE_HP[kind] + 3 * e.level
	e.max_hp = e.hp


## A soldier's frame list for its action (0 walk, 1 attack, 2 hurt, 3 dying).
func enemy_anim(e: Actor, action: int) -> Array:
	var dir4 := int(table("dir8_to_dir4")[e.dir])
	var prefix := "body_anim_" if e.type == KIND_ARCHERS else "head_anim_"
	return table(prefix + str(clampi(action, 0, 3)))[dir4]


## The sprite frame an enemy shows now; 100 and more is not drawn (the dying blink).
func enemy_sprite_frame(e: Actor) -> int:
	var anim := enemy_anim(e, e.action)
	return int(anim[clampi(e.frame, 0, anim.size() - 1)])


## Rounded distance in pixels.
static func distance(a: Vector2i, b: Vector2i) -> int:
	var dx := absi(a.x - b.x)
	var dy := absi(a.y - b.y)
	var d2 := dx * dx + dy * dy
	var i := maxi(dy, dx)
	while i * i < d2:
		i += 2
	i -= 1
	if i * i < d2:
		i += 1
	return i


## Direction 0 / 2 / 4 / 6 from a to b.
static func dir4(a: Vector2i, b: Vector2i) -> int:
	var i := b.x - a.x
	var dy := b.y - a.y
	if dy > i:
		return 0 if dy > -i else 2
	return 6 if dy > -i else 4


## Direction 0..7 from a to b.
static func dir8(a: Vector2i, b: Vector2i) -> int:
	var i := b.x - a.x
	var dy := b.y - a.y
	if i + i < dy:
		if i + i > -dy:
			return 0
		if -i < dy + dy:
			return 1
		if i < dy + dy:
			return 2
		return 3
	if i + i < -dy:
		return 4
	if -i > dy + dy:
		return 5
	if i > dy + dy:
		return 6
	return 7


## Direction 0..7 to the hero, straight within 27 px.
func dir_to_hero(p: Vector2i) -> int:
	var i := hero.pos.x - p.x
	var dy := hero.pos.y - p.y
	if i > 27:
		return 7 if dy > 27 else (5 if dy < -27 else 6)
	if i < -27:
		return 1 if dy > 27 else (3 if dy < -27 else 2)
	return 0 if dy > 0 else 4


## The two boxes overlap (the game's own test, kept as it is).
static func boxes_touch(x1: int, y1: int, w1: int, h1: int, x2: int, y2: int, w2: int, h2: int) -> bool:
	var dx := x1 + w1 / 2 - x2 + w2 / 2
	var dy := y1 + h1 / 2 - y2 + h2 / 2
	return absi(dx) < (w1 + w2) / 2 and absi(dy) < (h1 + h2) / 2


## The enemy's next action, every 6 ticks while it stands or walks.
func choose_enemy_action(e: Actor) -> void:
	var i := distance(hero.pos, e.pos)
	var near := 1 if i < 90 else 0
	e.frame = 0
	var roll := rng.below(1000)
	var to_hero := dir_to_hero(e.pos)
	if e.type == KIND_SWORDS or e.type == KIND_SQUAD:
		if roll < 150 + near * 300:
			e.action = 0
			e.dir = (to_hero + TURNS[roll & 7]) & 7
		elif roll < 850 - near * 100:
			if near != 0:
				if i <= 45 and hero.action != 9 and hero.action != 10 and hero.action < 12:
					e.action = 1
					e.dir = dir4(e.pos, hero.pos)
					e.facing = e.dir
					hero_is_hit(e)
					return
				e.action = 0
				e.dir = (to_hero + TURNS[roll & 7]) & 7
			else:
				e.action = 0
				e.dir = (e.dir + TURNS[roll & 7]) & 7
		else:
			e.action = 0
			if near != 0:
				e.dir = roll & 7
			else:
				e.dir = (e.dir + TURNS[roll & 7]) & 7
		e.facing = e.dir
	elif e.type == KIND_ARCHERS:
		e.action = 1
		e.think_ticks = 15
		shoot_arrow(e)


func shoot_arrow(e: Actor) -> void:
	var i := e.dir >> 1
	for a in arrows:
		if not a.active:
			a.active = true
			a.pos = e.pos + Vector2i(ARROW_DX[i], ARROW_DY[i])
			a.dir = i
			a.ticks = 0
			a.attack = e.attack
			if (i & 1) != 0:
				a.w = 11
				a.h = 2
			else:
				a.w = 2
				a.h = 11
			return


## One tick of every enemy: animation, AI, movement and strikes.
func _tick_enemies() -> void:
	var dx8 := table("dir_dx8")
	var dy8 := table("dir_dy8")
	var b := -1
	while true:
		b += 1
		if b >= enemies.size():
			break
		var e: Actor = enemies[b]
		e.action = mini(e.action, 3)
		e.frame += 1
		e.think_ticks -= 1
		var anim := enemy_anim(e, e.action)
		var anim_frame := int(anim[mini(e.frame, anim.size() - 1)])
		if e.action == 3:
			if anim_frame > END:
				_enemy_dies(e)
				# (the next enemy waits a tick, as in the original's loop)
				if enemies_alive < 1 and waves[0] == 0 and e.type != KIND_ARCHERS:
					room_phase = 3
					room_phase_timer = 5
			continue
		if anim_frame > END:
			e.action = 3 if e.hp < 1 else 0
			e.frame = 0
		if e.think_ticks < 1:
			e.alerted = 1
			e.think_ticks = 6
			if e.action == 0:
				choose_enemy_action(e)
		if e.type == KIND_ARCHERS:
			e.dir = dir4(e.pos, hero.pos)
			e.facing = e.dir
			continue
		var move_dir := e.facing
		if e.alerted == 0:
			# still outside: walks straight in, through anything
			e.pos += Vector2i(int(dx8[move_dir]), int(dy8[move_dir]))
			continue
		var step_x := 0
		var step_y := 0
		var action := e.action
		var frame := e.frame
		if action == 0:
			step_x = int(dx8[move_dir])
			step_y = int(dy8[move_dir])
		elif action == 1:
			step_x = int(dx8[e.dir]) / 3
			step_y = int(dy8[e.dir]) / 3
		elif action == 2 and e.ai_mode > 0:
			e.ai_mode -= 1
			move_dir = (move_dir + 4) & 7
			step_x = int(dx8[move_dir]) << 2
			step_y = int(dy8[move_dir]) << 2
		elif action == 2 and frame == 1:
			move_dir = (e.facing + 4) & 7
			step_x = int(dx8[move_dir]) * 3 / 4
			step_y = int(dy8[move_dir]) * 3 / 4
		if step_x != 0 or step_y != 0:
			var i: int
			if e.type == KIND_SQUAD:
				var shift: Vector2i = SQUAD_SHIFT.get(move_dir, Vector2i.ZERO)
				i = move(e.pos + shift, step_x, step_y, move_dir, e)
				if i != -1:
					e.pos -= shift
			else:
				i = move(e.pos, step_x, step_y, move_dir, e)
			if e.action == 0 and move_dir in [0, 2, 4, 6] and i == -1:
				i = slide_corner(e.pos, e.facing, e)
				if i != -1:
					move(e.pos, int(dx8[i]), int(dy8[i]), i, e)
		if e.action == 1 and e.frame == 1:
			_enemy_strikes_hero(e)


func _enemy_strikes_hero(e: Actor) -> void:
	if hero.action != 9 and hero.action != 10 and hero.action < 12:
		if e.dir == dir4(e.pos, hero.pos) and distance(hero.pos, e.pos) <= GENERAL_REACH[general_side]:
			hero_is_hit(e)


func _enemy_dies(e: Actor) -> void:
	mission_exp += e.level
	kills += 3 if e.type == KIND_SQUAD else 1
	enemies.erase(e)
	if e.type != KIND_ARCHERS:
		enemies_alive -= 1


func _sort_enemies() -> void:
	for b in range(enemies.size() - 1):
		for i in range(b + 1, enemies.size()):
			if enemies[b].pos.y > enemies[i].pos.y:
				var t: Actor = enemies[b]
				enemies[b] = enemies[i]
				enemies[i] = t


## The hero is hit by an enemy (e) or by an arrow (a).
func hero_is_hit(e: Actor, a: Arrow = null) -> void:
	var dmg := 0
	if e != null:
		hero.facing = dir8(hero.pos, e.pos)
		dmg = e.attack + e.attack_buff - hero.defense - hero.defense_buff
	else:
		hero.facing = ((a.dir << 1) + 4) & 7
		dmg = a.attack - hero.defense - hero.defense_buff
	hero.dir = hero.facing
	dmg = maxi(dmg, 1)
	hero.hp = hero.hp - dmg if hero.hp > dmg else 0
	if e != null:
		_show_target_info(e)
	hero.frame = 0
	hero.action = 9
	if hero.hp < 1:
		hero.hp = 0
		hero.action = 10


func _show_target_info(e: Actor) -> void:
	var names := table("troop_names")
	target_info = {"name": str(names[e.type - 201]) if e.type - 201 < names.size() else "",
		"level": e.level, "hp_bar": e.hp * 60 / maxi(e.max_hp, 1), "ticks": 10}


## The hero's sword: every enemy in front of him and in reach is struck.
func _hero_attack() -> void:
	var reach := int(table("weapon_reach")[hero.weapon_kind])
	for e in enemies.duplicate():
		if e.hp > 0 and e.alerted != 0 and e.action < 6:
			if hero.dir == dir4(hero.pos, e.pos) and distance(hero.pos, e.pos) <= reach:
				_strike_enemy(e)


func _strike_enemy(e: Actor) -> void:
	if e.action > 5:
		return
	_hero_hits_enemy(e)
	if hero.combo > 1 and hero.action < 12:
		e.ai_mode = 1  # the third strike of a combo knocks back


func _hero_hits_enemy(e: Actor) -> void:
	e.dir = dir8(e.pos, hero.pos)
	e.facing = e.dir
	if hero.action >= 3 and hero.action <= 8:
		var dmg := hero.attack + hero.attack_buff - e.defense - e.defense_buff
		e.hp -= maxi(dmg, 1)
	if e.hp < 1:
		e.hp = 0
		e.frame = 3
	else:
		e.frame = 0
	_show_target_info(e)
	e.action = 2


## Normal difficulty: the hero turns to the nearest enemy (closer than 50 px) as he strikes.
func _turn_to_nearest() -> void:
	if difficulty == 0:
		return
	var best := 50
	var found: Actor = null
	for e in enemies:
		var d := distance(e.pos, hero.pos)
		if best > d and e.hp > 0:
			best = d
			found = e
	if found != null:
		hero.facing = dir4(hero.pos, found.pos)
		hero.dir = hero.facing


## Arrows fly 12 px a tick for 22 ticks; one that touches the hero hits him.
func _tick_arrows() -> void:
	for a in arrows:
		if not a.active:
			continue
		if boxes_touch(a.pos.x, a.pos.y + 8, a.w, a.h, hero.pos.x - 12, hero.pos.y - 20, 17, 18) \
				and hero.action < 12:
			a.active = false
			hero_is_hit(null, a)
			continue
		a.ticks += 1
		if a.ticks > 22:
			a.active = false
			continue
		match a.dir:
			0: a.pos.y += 12
			1: a.pos.x -= 12
			2: a.pos.y -= 12
			3: a.pos.x += 12


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


## Not walking into other actors. The game's own check shortens nothing (its result is
## never used), so actors pass through each other, as in the original.
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
