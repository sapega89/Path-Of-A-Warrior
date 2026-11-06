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
## knocked back and die; the last one clears the room. Barrels and other objects break under
## the sword; soldiers and objects drop gold and items that the hero picks up. Generals come
## with their talk, fight with their skills, and the mission's own general ends the mission
## ("Mission Success!"). The hero's skills (on their keys, for MP) and his potions and
## scrolls work, and effects() tells which pictures of their effects show. Not yet: the
## talk after a cleared room and the mission's rewards.

const Rooms := preload("res://scripts/world/rooms.gd")
const JavaRandom := preload("res://scripts/sim/java_random.gd")
const TABLES_PATH := "res://data/tables.json"
const TICK_MS := 120  # speed 2 of the original (speed_frame_ms)
const END := 200  # animation frame numbers above this end the animation (222 = loop end)

## Banners shown over the map (the original's popups 8 and 9).
const BANNER_STAGE := 8
const BANNER_STAGE_CLEAR := 9
const BANNER_SUCCESS := 10  # "Mission Success!": waits for a key, then the mission ends
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
## The frame of an attack that hits, by action (sword 3..8, skills 21..24).
const HIT_FRAME := [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 6, 5, 5]
## MP of skill 12..30 at level 1, and per level above.
## The three flames of a fire scroll around its point.
const FIRE_SHIFT := [Vector2i(3, -6), Vector2i(-10, 0), Vector2i(10, 5)]
const SKILL_BASE_COST := [5, 6, 7, 10, 15, 7, 10, 10, 8, 9, 10, 5, 6, 7, 9, 12, 20, 20, 20]
const SKILL_COST_PER_LEVEL := [3, 4, 5, 3, 4, 3, 3, 5, 3, 4, 5, 3, 4, 5, 5, 6, 5, 5, 5]
## Potions 1..9 restore HP (1), MP (2) or both (3) by 30 / 60 / 100 %.
const RESTORES := [1, 1, 1, 2, 2, 2, 3, 3, 3]
const RESTORE_PCT := [30, 60, 100, 30, 60, 100, 30, 60, 100]
## How many ticks an effect lasts, by effect item + 2 (-2, -1 scrolls in flight, 1..9 potions).
const EFFECT_STEPS := [2, 10, 100, 2, 2, 2, 2, 2, 2, 2, 2, 2, 100, 100]
## A squad moves as if it stood this far aside (the side its men stand on), by direction.
const SQUAD_SHIFT := {3: Vector2i(-20, 0), 1: Vector2i(-20, 20), 2: Vector2i(-20, 0),
	0: Vector2i(0, 20), 5: Vector2i(20, 0), 7: Vector2i(20, 20), 6: Vector2i(20, 0)}
const GENERAL_REACH := [60, 50]
const CAMPAIGN_PATH := "res://data/campaign.json"
const TALK_PATH := "res://data/talk.json"
const BUFF_DIV := [20, 20, 25]
const TALK_STEPS := 3  # a general met on the map: he, the hero, he
const VICTORY_TALK_STEPS := 5  # a general after his room or mission: he, the hero, ...
const FRIENDSHIP_PER_TALK := 5
## The pages after "Mission Success!" (which shows the gold): the exp, the exp for time.
const BANNER_TOTAL_EXP := 11
const BANNER_TIME_EXP := 12
const HERO_NAME := "Hero"

static var _tables: Dictionary = {}
static var _generals: Dictionary = {}
static var _talk: Dictionary = {}


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
	var weapon_kind := 0  # the sword type, 0 or 1 (the weapon's slot type; the Iron Claymore 1)
	var skill_step := 0  # a general's heals so far
	var mp := 0
	var max_mp := 0
	var attack_buff_ticks := 0
	var defense_buff_ticks := 0


## A breakable object of the room (barrels, crates, ...): a cell of the objects layer.
class Breakable:
	var active := true
	var tile := Vector2i.ZERO
	var pos := Vector2i.ZERO
	var kind := 0
	var hp := 21
	var break_frame := 0  # > 0: the hit spark shows
	var break_ticks := 0  # > 0: broken, blinking out


## Something lying on the floor: an item id (< 100 potion, < 10000 gear, 10000 + n = n gold).
class Drop:
	var item := 0
	var pos := Vector2i.ZERO
	var ticks := 75


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
var general_side := 0  # the side (weapon) of the last general met: 0 long, 1 short sword
var general := {}  # the last general met (campaign.json generals)
var boss_type := 0  # the mission's own general: defeating him wins the mission
var boss_fight := false
var boss_spawned := false
var won := false
## A talk over the map (the world waits): lines with their speaker, the line shown, how much.
var talk: Array[String] = []
var talk_line := 0
var talk_chars := 0
var talk_wait := 0
var rng := JavaRandom.new()
var enemies: Array[Actor] = []  # in drawing order (sorted by y each tick)
var enemies_alive := 0  # archers do not count
var spawn_spots: Array[Vector3i] = []  # tile x, tile y, exit side (0 down 1 left 2 up 3 right)
var arrows: Array[Arrow] = [Arrow.new(), Arrow.new(), Arrow.new()]
var kills := 0
var play_ticks := 0  # ticks of play on the map (not banners, talks or room scrolls)
var mission_exp := 0
## The mission's rewards and its general who talks after it (0 none, >= 200 none).
var mission_gold := 0
var mission_general := 0
var time_limit := 0  # seconds; in time the exp grows
var time_exp := 0  # the exp for time, given when the mission was won in time
## Friendship points of the generals the hero talked with (general id -> points).
var friendship := {}
## What follows the talk: 0 the map goes on, 1 the exits open, 2 the mission is over.
var talk_after := 0
var failed := false
var finished := false  # the mission is over: the screen leaves
## The hero's skill levels (skills 12..30), the skills on his keys, his quick slots
## ([item, count], potions and scrolls) and which slots the two potion keys use.
var skill_levels: Array[int] = []
var hotkeys: Array[int] = [12, 17, 0, 0, 0]
var quick_slots: Array = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
var quick_keys: Array[int] = [0, 1]
## A potion or scroll in use: item (> 9 scroll in the hero's hand, < 0 its blast), step.
var effect_item := 0
var effect_step := 0
var effect_slot := 0
var effect_pos := Vector2i.ZERO
var effect_dir := 0
## The last enemy hit or hitting: {name, level, hp_bar (0..60), ticks}.
var target_info := {}
var breakables: Array[Breakable] = []
var drops: Array[Drop] = []
var gold := 0
var items: Array[int] = []  # picked up this mission (potions and gear), in order


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


static func _load_json(path: String) -> Dictionary:
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return {}
	var data: Variant = JSON.parse_string(f.get_as_text())
	return data if typeof(data) == TYPE_DICTIONARY else {}


## A general's data: name, look, side, skills, attack, defense, hp.
static func general_data(id: int) -> Dictionary:
	if _generals.is_empty():
		_generals = _load_json(CAMPAIGN_PATH).get("generals", {})
	return _generals.get(str(id), {})


static func talk_lines(kind: String) -> Array:
	if _talk.is_empty():
		_talk = _load_json(TALK_PATH)
	return _talk.get(kind, [])


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
	hero.mp = 10
	hero.max_mp = 10
	for i in 19:
		skill_levels.append(0)
	skill_levels[0] = 1  # the first skills of a new hero: 12 and 17
	skill_levels[5] = 1
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
	_find_breakables()
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
## fire: the attack key was pressed (it also closes a banner). hotkey: a skill key (0..4)
## pressed, -1 none; potion: a potion key (0, 1), -1 none.
func tick(held: int, pressed: int = -1, fire: bool = false, hotkey: int = -1, potion: int = -1) -> void:
	hero.prev_pos = hero.pos
	for e in enemies:
		e.prev_pos = e.pos
	if banner != 0:
		_tick_banner(fire)
		return
	if not talk.is_empty():
		_tick_talk(fire)
		return
	if scrolling:
		_tick_scroll()
		return
	var skill := 3 if fire else 0
	if hotkey >= 0 and hotkey < hotkeys.size():
		skill = hotkeys[hotkey]
	_tick_scene(held, pressed, skill, potion)
	if banner == 0:
		_end_tick()


func _tick_banner(fire: bool) -> void:
	if banner == BANNER_FAILED:
		if fire:
			finished = true
		return
	if banner == BANNER_SUCCESS or banner == BANNER_TOTAL_EXP or banner == BANNER_TIME_EXP:
		if fire:
			_next_result_page()
		return
	if fire and banner_timer > 2:
		banner_timer = 2
	banner_timer -= 1
	if banner_timer <= 0:
		var b := banner
		banner = 0
		if b == BANNER_STAGE_CLEAR:
			# Room cleared: the exits open (a room with a general: he talks first).
			var g := room_general()
			if g != 0:
				_start_general_talk(g, 1)
			else:
				room_phase = 1
				room_phase_timer = 5


func _show_banner(kind: int) -> void:
	banner = kind
	banner_timer = BANNER_TICKS


func _tick_scene(held: int, pressed: int, skill: int, potion: int = -1) -> void:
	play_ticks += 1
	for o in breakables:
		if o.active and o.break_frame != 0:
			o.break_frame -= 1
	_tick_effect()
	if potion >= 0:
		_use_quick_slot(potion)
	if effect_item > 0:
		# a potion being drunk or a scroll being read: the world waits
		if effect_item > 9:
			hero.frame = effect_step
		return
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
	if _hero_action_hits():
		_tick_arrows()
		_pick_up_drops()
		_tick_enemies()
		_sort_enemies()
	_tick_broken()


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
	elif skill > 0 and skill_mp_cost(skill) != 0:
		hero.facing = int(table("dir8_to_dir4")[hero.facing]) << 1
		hero.dir = hero.facing
		hero.action = skill
		hero.frame = 0


## Takes the MP of a skill (12..30) at its level; 0 = not enough MP (nothing is taken).
func skill_mp_cost(skill: int) -> int:
	var cost := 0
	if skill >= 12 and skill <= 30:
		var k := skill - 12
		cost = SKILL_BASE_COST[k] + (skill_levels[k] - 1) * SKILL_COST_PER_LEVEL[k]
	if cost > hero.mp:
		return 0
	hero.mp -= cost
	return cost


## The mission clock: seconds of play.
func play_seconds() -> int:
	return play_ticks * TICK_MS / 1000


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
	elif action == 12:
		if frame > 2 and frame < 6:
			step_x = int(dx8[move_dir]) << 2
			step_y = int(dy8[move_dir]) << 2
	elif action == 13 or action == 14:
		var lunge := action == 14
		if action == 13 and frame > 4 and frame < 8:
			var sx := int(dx8[move_dir]) << 2
			var sy := int(dy8[move_dir]) << 2
			if sx > 0:
				sx = step_until_free(hero.pos, sx, 6)
			elif sx < 0:
				sx = step_until_free(hero.pos, sx, 2)
			if sy > 0:
				sy = step_until_free(hero.pos, sy, 0)
			elif sy < 0:
				sy = step_until_free(hero.pos, sy, 4)
			hero.pos += keep_in_room(hero.pos, sx, sy)
			lunge = true
		if lunge and frame > 0 and frame < 9:
			step_x = int(dx8[move_dir])
			step_y = int(dy8[move_dir])
	elif action == 20:
		if (frame & 1) == 0:
			step_x = int(dx8[move_dir])
			step_y = int(dy8[move_dir])
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


## The frames of the hero's action that hit, heal or buff. False: a skill's cinematic
## stops the world this tick (arrows and enemies wait).
func _hero_action_hits() -> bool:
	var world_runs := true
	var action := hero.action
	var frame := hero.frame
	if (action >= 3 and action <= 8) or (action >= 21 and action <= 24):
		if frame == HIT_FRAME[action]:
			if action <= 8:
				_turn_to_nearest()
			_hero_attack(0)
			_hero_hits_breakables()
	elif action == 12:
		if frame > 2 and frame < 6:
			_hero_attack(0)
			_hero_hits_breakables()
	elif action == 13:
		if frame > 4 and frame < 8:
			_hero_attack(0)
			_hero_hits_breakables()
	elif action == 14:
		if frame in [2, 4, 6, 8]:
			_hero_attack(0)
			_hero_hits_breakables()
	elif action == 15 or action == 16:
		if frame == 11:  # heals
			if action == 15:
				hero.hp += hero.max_hp * (4 + skill_levels[3]) / 25
			else:
				hero.hp += hero.max_hp * (9 + skill_levels[4]) / 20
			_clamp_hero()
	elif action >= 17 and action <= 19:
		if frame == 11:  # buffs: attack (17), defence (18), both (19)
			var lv := skill_levels[action - 12]
			var ticks := 50 if lv < 4 else (100 if lv < 8 else 150)
			if action != 18:
				hero.attack_buff = maxi(hero.attack * lv / int(BUFF_DIV[action - 17]), 1)
				hero.attack_buff_ticks = ticks
			if action != 17:
				hero.defense_buff = maxi(hero.defense * lv / int(BUFF_DIV[action - 17]), 1)
				hero.defense_buff_ticks = ticks
	elif action == 20:
		if (frame & 1) != 0:
			hero.combo = 0 if frame in [1, 5, 9] else 2
			_hero_attack(0)
			_hero_hits_breakables()
	elif action == 25:
		if (frame & 1) != 0:
			_hero_attack(0)
			_hero_hits_breakables()
	elif action == 26 or action == 27:
		if frame == 8:
			_hero_attack(0)
			_hero_hits_breakables()
		if frame > 1 and frame < 9:
			world_runs = false
	elif action == 28:
		if frame == 22:
			_hero_attack(0)
			_hero_hits_breakables()
		elif frame > 3:
			world_runs = false
	elif action == 29:
		if frame == 22:
			_hero_attack(0)
			_hero_hits_breakables()
		elif frame > 6:
			world_runs = false
	elif action == 30:
		if frame > 3:
			if frame < 15:
				world_runs = false
			elif frame == 15:
				_hero_attack(0)
				_hero_hits_breakables()
	return world_runs


func _clamp_hero() -> void:
	hero.hp = mini(hero.hp, hero.max_hp)
	hero.mp = mini(hero.mp, hero.max_mp)


# ---- potions and scrolls -------------------------------------------------------------------

## A potion key: the item of its quick slot goes into use (a scroll only while standing
## or walking: the hero holds it up first).
func _use_quick_slot(key: int) -> void:
	if effect_item != 0 or hero.action >= 10 or key < 0 or key >= quick_keys.size():
		return
	var sel := quick_keys[key]
	var item := int(quick_slots[sel][0])
	if item == 0:
		return
	if item > 9:
		if hero.action > 1:
			return
		hero.action = 11
	effect_item = item
	effect_slot = sel
	effect_step = 0
	effect_pos = hero.pos
	effect_dir = int(table("dir8_to_dir4")[hero.dir])


## One tick of the item in use: a potion restores after 2 ticks; a scroll is read for 5
## ticks, then its blast flies in front of the hero and strikes (-2 fire once, -1 lightning
## three times) everyone within 35 px.
func _tick_effect() -> void:
	if effect_item == 0:
		return
	if effect_item == -1:
		if effect_step in [1, 4, 7]:
			_hero_attack(-1)
	elif effect_item == -2 and effect_step == 1:
		_hero_attack(-2)
	effect_step += 1
	if effect_item > 9 and effect_step > 4:
		effect_pos = _front_of(effect_pos, effect_dir << 1)
		effect_item -= 12
		effect_step = 0
	if effect_step >= EFFECT_STEPS[effect_item + 2]:
		if effect_item > 0:
			var k := effect_item - 1
			if (RESTORES[k] & 1) != 0:
				hero.hp += hero.max_hp * RESTORE_PCT[k] / 100
			if (RESTORES[k] & 2) != 0:
				hero.mp += hero.max_mp * RESTORE_PCT[k] / 100
			_clamp_hero()
		var slot: Array = quick_slots[effect_slot]
		slot[1] -= 1
		if slot[1] < 1:
			slot[0] = 0
			slot[1] = 0
		effect_item = 0


## A potion or scroll picked up goes to its quick slot (5 of a kind at most); false if full.
func add_quick_item(item: int) -> bool:
	var free := -1
	for b in quick_slots.size():
		if int(quick_slots[b][0]) == item:
			if int(quick_slots[b][1]) > 4:
				return false
			quick_slots[b][1] += 1
			return true
		if int(quick_slots[b][0]) == 0 and free < 0:
			free = b
	if free < 0:
		return false
	quick_slots[free] = [item, 1]
	return true


func _end_tick() -> void:
	# The tick is drawn with the direction it moved in (a slide can turn it), then the
	# hero looks where he faces again.
	hero.shown_dir = hero.dir
	hero.dir = hero.facing
	hero.idle_ticks += 1
	if hero.attack_buff_ticks > 0:
		hero.attack_buff_ticks -= 1
		if hero.attack_buff_ticks < 1:
			hero.attack_buff = 0
	if hero.defense_buff_ticks > 0:
		hero.defense_buff_ticks -= 1
		if hero.defense_buff_ticks < 1:
			hero.defense_buff = 0
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
			4:
				# the mission's general is defeated
				won = true
				banner = BANNER_SUCCESS
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
	if not (waves[0] >= 200 or not boss_spawned) or spawn_spots.is_empty():
		return  # one general at a time
	var spot: Vector3i = spawn_spots[rng.below(spawn_spots.size())]
	create_enemy(waves[0], spot.x, spot.y, spot.z)
	waves[1] -= 1
	if waves[1] < 1:
		for b in 12:
			waves[b] = waves[b + 2]


## A soldier or a general (kind < 200) outside the room behind exit `side`, looking in.
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
	if kind > 200:
		enemy_stats(e, kind - 201)
	else:
		if kind == boss_type:
			boss_fight = true
		boss_spawned = true
		set_general(kind)
		_start_map_talk()
		general_stats(e)
		waves[1] = 1
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


## A general's stats: his own, raised by his level (the hero's plus the list's count).
func general_stats(e: Actor) -> void:
	e.level = hero.level + waves[1]
	e.attack = (int(general.get("attack", 0)) + e.level - 1) * 6 / 5
	e.defense = (int(general.get("defense", 0)) + e.level - 1) * 6 / 5
	e.hp = int(general.get("hp", 1)) + (e.level - 1) * 3
	e.max_hp = e.hp


func set_general(id: int) -> void:
	general = general_data(id)
	general_side = int(general.get("side", 0))


## How many actions an enemy has (its animation table's size).
func enemy_actions(e: Actor) -> int:
	return 22 if e.type < 200 else 4


## An enemy's frame list for its action. Soldiers: 0 walk, 1 attack, 2 hurt, 3 dying;
## generals: the same, 4 and 5 strikes, 6..21 skills (the hero's skill animations).
func enemy_anim(e: Actor, action: int) -> Array:
	var dir4 := int(table("dir8_to_dir4")[e.dir])
	if e.type > 200:
		var prefix := "body_anim_" if e.type == KIND_ARCHERS else "head_anim_"
		return table(prefix + str(clampi(action, 0, 3)))[dir4]
	match clampi(action, 0, 21):
		0: return table("head_anim_0")[dir4]
		1, 4, 5: return table("weapon_anim_1")[dir4]
		2: return table("weapon_anim_2")[dir4]
		3: return table("weapon_anim_3")
		6: return table("hero_anim_12")[dir4]
		7: return table("hero_anim_13")[dir4]
		8: return table("hero_anim_14")[dir4]
		9, 10, 11, 12, 13: return table("hero_anim_15_19")
		14: return table("hero_anim_20")[dir4]
		15: return table("hero_anim_21")[dir4]
		16: return table("hero_anim_22")[dir4]
		17, 18: return table("hero_anim_23_24")
		19: return table("hero_anim_25")[dir4]
	return table("hero_anim_26_27")[dir4]


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
	elif roll < 150:
		general_pick_skill(e, false)
	elif roll < 350:
		if i <= 60 and (hero.action != 9 or hero.frame >= 6) and hero.action != 10 and hero.action < 12:
			e.action = 1
			e.dir = dir4(e.pos, hero.pos)
			e.facing = e.dir
	else:
		e.dir = to_hero
		e.facing = to_hero


## A general picks one of his four skills (an empty slot is a plain strike); a heal only
## while below half HP and four times at most; force: no buff (he was just hit).
func general_pick_skill(e: Actor, force: bool) -> void:
	var skills: Array = general.get("skills", [0, 0, 0, 0])
	e.action = 6 + int(skills[rng.below(4)]) - 1
	if e.action == 9 or e.action == 10:
		if e.skill_step > 3:
			e.action = 1
		elif e.max_hp >> 1 > e.hp:
			e.skill_step += 1
		else:
			e.action = 1
	elif e.action in [11, 12, 13] and force:
		e.action = 1
	e.dir = dir4(e.pos, hero.pos)
	e.facing = e.dir


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
		e.action = mini(e.action, enemy_actions(e) - 1)
		e.frame += 1
		e.think_ticks -= 1
		var anim := enemy_anim(e, e.action)
		var anim_frame := int(anim[mini(e.frame, anim.size() - 1)])
		if e.attack_buff_ticks > 0:
			e.attack_buff_ticks -= 1
			if e.attack_buff_ticks < 1:
				e.attack_buff = 0
		if e.defense_buff_ticks > 0:
			e.defense_buff_ticks -= 1
			if e.defense_buff_ticks < 1:
				e.defense_buff = 0
		if e.action == 3:
			if anim_frame > END:
				_enemy_dies(e)
				# (the next enemy waits a tick, as in the original's loop)
				if enemies_alive < 1 and waves[0] == 0 and e.type != KIND_ARCHERS:
					if boss_fight:
						room_phase = 4
						room_phase_timer = 22
					else:
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
		var dir := e.dir
		if action == 0:
			step_x = int(dx8[move_dir])
			step_y = int(dy8[move_dir])
		elif action in [1, 4, 5]:
			step_x = int(dx8[dir]) / 3
			step_y = int(dy8[dir]) / 3
		elif action == 6:
			if frame > 2 and frame < 6:
				step_x = int(dx8[dir]) << 2
				step_y = int(dy8[dir]) << 2
		elif action == 7 or action == 8:
			var lunge := action == 8
			if action == 7 and frame > 4 and frame < 8:
				# a dash: straight on until a wall, then the step of action 8 as well
				var sx := int(dx8[dir]) << 2
				var sy := int(dy8[dir]) << 2
				if sx > 0:
					sx = step_until_free(e.pos, sx, 6)
				elif sx < 0:
					sx = step_until_free(e.pos, sx, 2)
				if sy > 0:
					sy = step_until_free(e.pos, sy, 0)
				elif sy < 0:
					sy = step_until_free(e.pos, sy, 4)
				e.pos += keep_in_room(e.pos, sx, sy)
				lunge = true
			if lunge and frame > 0 and frame < 9:
				step_x = int(dx8[dir])
				step_y = int(dy8[dir])
		elif action == 14:
			if (frame & 1) == 0:
				step_x = int(dx8[dir])
				step_y = int(dy8[dir])
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
		action = e.action
		frame = e.frame
		match action:
			1, 4, 5:
				if frame == 1:
					_enemy_strikes_hero(e)
			6:
				if frame > 2 and frame < 6:
					_enemy_strikes_hero(e)
			7:
				if frame > 4 and frame < 8:
					_enemy_strikes_hero(e)
			8:
				if frame in [2, 4, 6, 8]:
					_enemy_strikes_hero(e)
			9, 10:
				if frame == 11:  # heals 20 / 50 %
					e.hp = mini(e.hp + e.max_hp * (20 if action == 9 else 50) / 100, e.max_hp)
			11, 12, 13:
				if frame == 11:  # attack / defence buffs for 50 ticks
					if action != 12:
						e.attack_buff = maxi(e.attack / int(BUFF_DIV[action - 11]), 1)
						e.attack_buff_ticks = 50
					if action != 11:
						e.defense_buff = maxi(e.defense / int(BUFF_DIV[action - 11]), 1)
						e.defense_buff_ticks = 50
			14, 19:
				if (frame & 1) != 0:
					_enemy_strikes_hero(e)
			15:
				if frame == 5:
					_enemy_strikes_hero(e)
			16:
				if frame == 6:
					_enemy_strikes_hero(e)
			17, 18:
				if frame == 5:
					_enemy_strikes_hero(e)
			20, 21:
				if frame == 8:
					_enemy_strikes_hero(e)


func _general_reach() -> int:
	return GENERAL_REACH[general_side]


## The enemy's strike or skill lands on the hero if he is where it reaches.
func _enemy_strikes_hero(e: Actor) -> void:
	var action := e.action
	if hero.action != 9 and hero.action != 10:
		if hero.action >= 12:
			return
		match action:
			7:
				var side := e.dir >> 1
				if boxes_touch(e.pos.x + int(table("hit_box_x")[side]), e.pos.y + int(table("hit_box_y")[side]),
						int(table("hit_box_w")[side]), int(table("hit_box_h")[side]),
						hero.pos.x - 8, hero.pos.y - 8, 17, 17):
					hero_is_hit(e)
				return
			16:
				if _is_in_front(e.pos, hero.pos, e.dir):
					_general_strike_if_near(e, _general_reach())
				return
			17, 18:
				_general_strike_if_near(e, 45)
				return
			19:
				if ((e.dir + (e.frame >> 1 << 1)) & 7) == dir4(e.pos, hero.pos):
					_general_strike_if_near(e, _general_reach())
				return
			20, 21:
				if distance(_front_of(e.pos, e.dir), hero.pos) <= 35:
					_general_skill_hits_hero(e)
				return
		if e.dir == dir4(e.pos, hero.pos):
			_general_strike_if_near(e, _general_reach())
	elif hero.action == 9:
		if action == 8 or action == 14:
			if e.dir == dir4(e.pos, hero.pos):
				_general_strike_if_near(e, _general_reach())
		elif action == 20 or action == 21:
			if distance(_front_of(e.pos, hero.dir), hero.pos) <= 35:
				_general_skill_hits_hero(e)


func _front_of(p: Vector2i, d8: int) -> Vector2i:
	return p + Vector2i(int(table("front_dx")[d8 >> 1]), int(table("front_dy")[d8 >> 1]))


static func _is_in_front(a: Vector2i, b: Vector2i, d8: int) -> bool:
	match d8:
		2: return a.x > b.x
		6: return a.x < b.x
		0: return a.y < b.y
		4: return a.y > b.y
	return false


func _general_strike_if_near(e: Actor, reach: int) -> void:
	if distance(hero.pos, e.pos) <= reach:
		_general_skill_hits_hero(e)


## A skill pushes the hero back (hurt ticks) as well as hurting him.
func _general_skill_hits_hero(e: Actor) -> void:
	match e.action:
		6:
			e.frame = 5
			hero.hurt_ticks = 2
		8, 16, 19:
			hero.hurt_ticks = 2
		15, 18, 21:
			hero.hurt_ticks = 5
	hero_is_hit(e)


func _enemy_dies(e: Actor) -> void:
	if e.type < 200:
		mission_exp += e.level << 1
		boss_spawned = false
		drop_item(2 if boss_fight else 1, e.pos)
	else:
		mission_exp += e.level
		drop_item(0, e.pos)
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
		if e.action in [6, 7, 8, 14, 15, 16, 17, 18, 19, 20, 21]:
			dmg += e.attack / int(table("skill_attack_div")[e.action - 6])
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
	var name := str(general.get("name", "")) if e.type < 200 else \
		(str(names[e.type - 201]) if e.type - 201 < names.size() else "")
	target_info = {"name": name,
		"level": e.level, "hp_bar": e.hp * 60 / maxi(e.max_hp, 1), "ticks": 10}


## The hero's attack (kind 0, by his action) or a scroll's blast (-1, -2) against the enemies.
func _hero_attack(kind: int) -> void:
	var reach := int(table("weapon_reach")[hero.weapon_kind])
	for e in enemies.duplicate():
		if not (e.hp > 0 and e.alerted != 0 and e.action < 6):
			continue
		if kind == 0:
			match hero.action:
				13:
					var side := hero.dir >> 1
					if boxes_touch(hero.pos.x + int(table("hit_box_x")[side]), hero.pos.y + int(table("hit_box_y")[side]),
							int(table("hit_box_w")[side]), int(table("hit_box_h")[side]),
							e.pos.x - 8, e.pos.y - 8, 17, 17):
						_hero_hits_enemy(e, hero.action)
				22:
					if _is_in_front(hero.pos, e.pos, hero.dir):
						_hero_strike_if_near(e, reach)
				23, 24:
					_hero_strike_if_near(e, 45)
				25:
					if ((hero.dir + (hero.frame >> 1 << 1)) & 7) == dir4(hero.pos, e.pos):
						_hero_strike_if_near(e, reach)
				26, 27:
					if distance(_front_of(hero.pos, hero.dir), e.pos) <= 35:
						_strike_enemy(e)
				28, 29, 30:
					_strike_enemy(e)
			# (every action also strikes what is straight in front, as the original does)
			if hero.dir == dir4(hero.pos, e.pos):
				_hero_strike_if_near(e, reach)
		elif distance(effect_pos, e.pos) <= 35:
			_hero_hits_enemy(e, effect_item)


func _hero_strike_if_near(e: Actor, reach: int) -> void:
	if distance(hero.pos, e.pos) <= reach:
		_strike_enemy(e)


## A strike of the hero lands: the damage, and what the skill does to the enemy.
func _strike_enemy(e: Actor) -> void:
	if e.action > 5:
		return
	_hero_hits_enemy(e, hero.action)
	if hero.combo > 1 and hero.action < 12:
		e.ai_mode = 1  # the third strike of a combo knocks back
	match hero.action:
		12:
			hero.frame = 5
			e.ai_mode = 2
		14, 22:
			e.ai_mode = 2
		20:
			e.ai_mode = 0
		21, 24:
			e.ai_mode = 5
		25, 27:
			e.ai_mode = 5
		26:
			pass
	if hero.action >= 25 and hero.action <= 27:
		var f := _front_of(hero.pos, hero.dir)
		e.dir = dir8(e.pos, f)
		e.facing = e.dir


## The damage of a hit: a strike (3..8), a skill (its level adds attack), or a scroll.
func _hero_hits_enemy(e: Actor, action: int) -> void:
	if action > -1:
		e.dir = dir8(e.pos, hero.pos)
	else:
		e.dir = dir8(e.pos, effect_pos)
	e.facing = e.dir
	if action >= 3 and action <= 8:
		var dmg := hero.attack + hero.attack_buff - e.defense - e.defense_buff
		e.hp -= maxi(dmg, 1)
	elif action in [12, 13, 14] or (action >= 20 and action <= 30):
		var k := action - 12
		var dmg := hero.attack + hero.attack_buff + hero.attack * skill_levels[k] / int(table("skill_attack_div")[k]) \
			- e.defense - e.defense_buff
		e.hp -= maxi(dmg, 1)
	elif action == -2:
		e.ai_mode = 2
		e.hp -= mini(hero.level << 1, 50)
	elif action == -1:
		e.hp -= mini(hero.level, 30)
	if e.hp < 1:
		e.hp = 0
		e.frame = 3
	else:
		e.frame = 0
	_show_target_info(e)
	e.action = 2
	if e.type < 200 and rng.below(1000) < 150 and e.hp > 0:
		general_pick_skill(e, true)


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


# ---- talks over the map ------------------------------------------------------------------

## A general met on the map: "<name> is here!!!", the hero's "...", his "Come on!".
func _start_map_talk() -> void:
	var lines := talk_lines("map")
	talk.clear()
	var name := str(general.get("name", ""))
	for k in TALK_STEPS:
		var speaker := name if (k & 1) == 0 else HERO_NAME
		var text := str(lines[21 + k]) if 21 + k < lines.size() else ""
		talk.append("[%s] %s" % [speaker, text.replace("&", speaker)])
	talk_line = 0
	talk_chars = 0
	talk_wait = 0


## The line shown now, as far as it is typed.
func talk_text() -> String:
	if talk.is_empty():
		return ""
	return talk[talk_line].substr(0, talk_chars)


## A letter a tick; the key shows the whole line, or goes on once it is shown. A shown
## line waits 15 ticks.
func _tick_talk(fire: bool) -> void:
	var line := talk[talk_line]
	if talk_wait > 0:
		talk_wait -= 1
		if fire:
			talk_wait = 0
		if talk_wait < 1:
			talk_line += 1
			talk_chars = 0
			if talk_line >= talk.size():
				talk.clear()
				talk_line = 0
				_talk_done()
		return
	if fire:
		talk_chars = line.length()
		talk_wait = 3
		return
	talk_chars += 1
	if talk_chars >= line.length():
		talk_wait = 15


# ---- after a room or the mission: the general's talk, the rewards ------------------------

## The general of the room (0 none), who talks once it is cleared.
func room_general() -> int:
	return int(rooms.cells[cell].get("general", 0)) if cell < rooms.cells.size() else 0


## "Mission Success!" (with the gold) -> the exp -> the exp for time if in time -> the
## general's talk -> the mission is over.
func _next_result_page() -> void:
	match banner:
		BANNER_SUCCESS:
			banner = BANNER_TOTAL_EXP
		BANNER_TOTAL_EXP:
			if play_seconds() < time_limit:
				time_exp = ((time_limit - play_seconds()) / time_limit / 10 + 1) * mission_exp / 20
				mission_exp += time_exp
				banner = BANNER_TIME_EXP
			else:
				_mission_over()
		_:
			_mission_over()


func _mission_over() -> void:
	banner = 0
	if mission_general > 0 and mission_general < 200:
		_start_general_talk(mission_general, 2)
	else:
		finished = true


## The gold of the mission (twice on hard difficulty, 0).
func gold_reward() -> int:
	return mission_gold * 150 * (1 + (difficulty ^ 1))


## The exp the mission gives (twice its kills' worth, four times on hard difficulty).
func exp_reward() -> int:
	return mission_exp << (1 + (difficulty ^ 1))


## A general's words after his room or the mission; the more friendship, the warmer
## (five lines for every ten points). after: what follows (talk_after).
func _start_general_talk(id: int, after: int) -> void:
	set_general(id)
	var points := mini(int(friendship.get(id, 0)) + FRIENDSHIP_PER_TALK, 100)
	friendship[id] = points
	var first := mini(points, 95) / 10 * VICTORY_TALK_STEPS
	var lines := talk_lines("general")
	var name := str(general.get("name", ""))
	talk.clear()
	for k in VICTORY_TALK_STEPS:
		var speaker := name if (k & 1) == 0 else HERO_NAME
		var text := str(lines[first + k]) if first + k < lines.size() else ""
		talk.append("[%s] %s" % [speaker, text.replace("&", speaker)])
	talk_line = 0
	talk_chars = 0
	talk_wait = 0
	talk_after = after


func _talk_done() -> void:
	var after := talk_after
	talk_after = 0
	if after == 1:
		room_phase = 1
		room_phase_timer = 5
	elif after == 2:
		finished = true


# ---- breakable objects and drops ----------------------------------------------------------

## The objects of the room's 9x9-tile view.
func _find_breakables() -> void:
	breakables.clear()
	var o := room_origin()
	for y in range(o.y * 7, mini(o.y * 7 + 9, h)):
		for x in range(o.x * 7, mini(o.x * 7 + 9, w)):
			var kind := int(objects[y * w + x])
			if kind == 0:
				continue
			var b := Breakable.new()
			b.tile = Vector2i(x, y)
			b.pos = Vector2i(x * 27 + 12, y * 27 + 20)
			b.kind = kind
			b.hp = 41 if kind in [101, 113] else 21
			breakables.append(b)


func _hero_hits_breakables() -> void:
	var reach := int(table("weapon_reach")[hero.weapon_kind])
	for b in breakables:
		if not (b.active and b.hp > 0):
			continue
		match hero.action:
			13:
				var side := hero.dir >> 1
				if boxes_touch(hero.pos.x + int(table("hit_box_x")[side]), hero.pos.y + int(table("hit_box_y")[side]),
						int(table("hit_box_w")[side]), int(table("hit_box_h")[side]),
						b.pos.x - 8, b.pos.y - 8, 18, 18):
					hit_breakable(b)
			22:
				if _is_in_front(hero.pos, b.pos, hero.dir) and distance(hero.pos, b.pos) <= reach:
					hit_breakable(b)
			23, 24:
				if distance(hero.pos, b.pos) <= 45:
					hit_breakable(b)
			25:
				if ((hero.dir + (hero.frame >> 1 << 1)) & 7) == dir4(hero.pos, b.pos) \
						and distance(hero.pos, b.pos) <= reach:
					hit_breakable(b)
			26, 27:
				if distance(_front_of(hero.pos, hero.dir), b.pos) <= 35:
					hit_breakable(b)
			28, 29, 30:
				hit_breakable(b)
			_:
				if hero.dir == dir4(hero.pos, b.pos) and distance(hero.pos, b.pos) <= reach:
					hit_breakable(b)


func hit_breakable(b: Breakable) -> void:
	b.hp = b.hp - hero.attack + hero.attack_buff
	b.break_frame = 2
	if b.hp < 1:
		b.break_ticks = 12
		objects[b.tile.y * w + b.tile.x] = 0  # the cell is free from now on


## A broken object blinks for 12 ticks, then is gone and may leave something behind.
func _tick_broken() -> void:
	for b in breakables:
		if b.active and b.break_ticks != 0:
			b.break_ticks -= 1
			if b.break_ticks == 0:
				drop_item(3, b.pos)
				b.active = false


## The object shows this tick (it blinks while breaking).
func breakable_shown(b: Breakable) -> bool:
	return b.active and (b.break_ticks == 0 or (b.break_ticks & 2) != 0)


## Something may drop at p: kind 0 soldier, 1 general, 2 the mission's general, 3 object.
## Only in the part of the room the game's view checks (its upper left), as the original.
func drop_item(kind: int, p: Vector2i) -> void:
	var o := room_origin()
	var cam := Vector2i(o.x * 7 * 27 + 1, o.y * 7 * 27)
	if p.y <= cam.y + 27 or p.y >= cam.y + 162 or p.x <= cam.x + 27 or p.x >= cam.x + 162:
		return
	var item := random_drop(kind)
	if item == 0 or (int(flags[(p.y / 27) * w + p.x / 27]) & 1) != 0:
		return
	var live := 0
	for d in drops:
		if d.item != 0:
			live += 1
	if live > 9:
		return
	var d := Drop.new()
	d.item = item
	d.pos = p
	drops.append(d)


func random_drop(kind: int) -> int:
	const DROP_ODDS := [5, 10, 20, 5, 100]
	const POTION_ODDS := [10, 30, 60, 1, 100]
	const TIER_MIN_LEVEL := [69, 44, 24, 9, 0]
	const TIER_ODDS := [[0, 0, 33, 77, 100], [5, 30, 55, 80, 100], [30, 60, 90, 100, 100],
		[40, 80, 100, 100, 100], [80, 100, 100, 100, 100]]
	if rng.below(100) < DROP_ODDS[kind]:
		var i := rng.below(100)
		if i < POTION_ODDS[kind]:
			for b in range(1, 5):  # above Lv69 the odds of Lv45-69 (pyport's DROPS_AFTER_69)
				if hero.level > TIER_MIN_LEVEL[b]:
					i = rng.below(100)
					for tier in 5:
						if i < TIER_ODDS[b][tier]:
							return 101 + tier + 5 * rng.below(20)
		else:
			return rng.below(11) + 1
	elif rng.below(100) < 25:
		return 10020 + (difficulty ^ 1) * 20
	return 0


func _pick_up_drops() -> void:
	for d in drops.duplicate():
		if d.item != 0 and distance(hero.pos, d.pos) < 20:
			if d.item > 10000:
				gold += d.item - 10000
			elif d.item < 100:
				if not add_quick_item(d.item):
					d.ticks -= 1
					continue  # no room: it stays on the floor
			else:
				items.append(d.item)
			d.item = 0
		d.ticks -= 1
		if d.ticks < 1 or d.item == 0:
			drops.erase(d)


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


# ---- the pictures of the effects ---------------------------------------------------------

## The effects to draw now: [sheet, frame, point in map pixels] (sheets fx_<name>.png). The
## hero's skill shows its effect on him (the big skills 28-30 over the middle of the room),
## a potion or scroll shows where it is in use.
func effects() -> Array:
	var out: Array = []
	var a := hero.action
	var f := hero.frame
	var p := hero.pos
	match a:
		2:
			out.append(["slash", hero.dir + (f & 1), p])
		12:
			if f > 2 and f < 6:
				out.append(["slash", hero.dir + (f & 1), p])
		13:
			if f > 4 and f < 8:
				out.append(["slash", hero.dir + (f & 1), p])
		14:
			if f > 0 and f < 9:
				out.append(["slash", hero.dir + (f & 1), p])
		15, 16:
			if f > 3:
				out.append(["heal", f - 4, p])
		17, 18, 19:
			if f > 3 and f < 10:
				out.append(["buff", f - 4, p])
		21:
			if f == 5 or f == 6:
				out.append(["whirl", f - 5, p])
		22:
			if f > 1 and f < 6:
				out.append(["slash", f & 1, p])
		23:
			if f == 5 or f == 6:
				out.append(["slash", f - 5, p])
		24:
			if f == 5 or f == 6:
				out.append(["burst", f - 5, p])
		26, 27:
			if a == 27 and f == 9:
				out.append(["blast", 1, _front_of(p, hero.shown_dir)])
			elif f > 1 and f < 9:
				out.append(["wave", f - 2 + (hero.dir >> 1) * 7, p])
		28:
			if f > 3 and f < 22:
				if f > 9:
					for i in 3:
						out.append(["storm", (f - 10) * 3 + 6 + i, _room_middle()])
				else:
					out.append(["storm", f - 4, _room_middle()])
		29:
			if f > 6 and f < 22:
				out.append(["quake", f - 7, _room_middle()])
		30:
			if f > 3 and f < 9:
				for i in 5:
					out.append(["rain", (f - 4) * 5 + i, _room_middle()])
			elif f > 12 and f < 15:
				for i in 3:
					out.append(["blast", (f - 13) * 5 + 2 + i, _room_middle()])
	match effect_item:
		0:
			pass
		-2:
			out.append(["blast", effect_step, effect_pos])
		-1:
			for i in 3:
				out.append(["fire", effect_step, effect_pos + FIRE_SHIFT[i]])
		10, 11:
			if effect_step > 0:
				out.append(["scroll", effect_step - 1 + (effect_dir << 2), effect_pos])
		_:
			out.append(["buff", effect_step + 4, effect_pos])
	return out


## The middle of the room on the screen, where the big skills show.
func _room_middle() -> Vector2i:
	var o := room_origin()
	return Vector2i(o.x * 7 * 27 + 120, o.y * 7 * 27 + 131)


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
