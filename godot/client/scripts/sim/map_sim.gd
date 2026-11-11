# gdlint: disable=max-public-methods
class_name MapSim
extends RefCounted
## A mission's map, tick by tick: its rooms and their phases, the hero, the enemies, the talks,
## the loot and the pages after the mission. Everything is in map pixels (a tile is 27 px) and
## whole numbers; one tick is 120 ms. The 3D screen only draws this state.
##
## MapSim holds the state and runs the tick; the parts of the game are static modules over it:
## MapRoomPlay (rooms), MapWalls (moving), MapHeroPlay (the hero), MapEnemyPlay (enemies),
## MapTalks (talks and rewards), MapLoot (objects and drops), MapAnims (animation tables),
## MapPictures (what the screen draws of the effects) and MapGeometry (distances, directions).

const TABLES_PATH := "res://data/tables.json"
const TICK_MS := 120  # speed 2 of the original (speed_frame_ms)
const END := 200  # animation frame numbers above this end the animation (222 = loop end)
## Banners shown over the map (the original's popups 8 and 9).
const BANNER_STAGE := 8
const BANNER_STAGE_CLEAR := 9
const BANNER_SUCCESS := 10  # "Mission Success!": 20 ticks, a key does not end it
const BANNER_FAILED := 22  # "Mission fail!": 20 ticks (a key: 2 more), then the mission ends
const BANNER_ACQUIRED := 13  # a gear picked up: "<its name> Acquired!!"
const BANNER_TICKS := 20
const EXP_PAGE_TICKS := 16  # an exp page stays after its bar is all shown
const KIND_SWORDS := 201
const KIND_ARCHERS := 202
const KIND_SQUAD := 203  # three swordsmen drawn together, one actor
## A general's Fire Whirl shows its first picture with the sheet's other part: the burst
## sheet's picture 0 drawn this much aside lands where that part puts it.
const BURST_FIRST_SHIFT := Vector2i(16, 5)
const SKILL_BASE_COST := [5, 6, 7, 10, 15, 7, 10, 10, 8, 9, 10, 5, 6, 7, 9, 12, 20, 20, 20]
const SKILL_COST_PER_LEVEL := [3, 4, 5, 3, 4, 3, 3, 5, 3, 4, 5, 3, 4, 5, 5, 6, 5, 5, 5]
const CAMPAIGN_PATH := "res://data/campaign.json"
const TALK_PATH := "res://data/talk.json"
const BUFF_DIV := [20, 20, 25]
## The pages after "Mission Success!" (which shows the gold): the exp, the exp for time.
const BANNER_TOTAL_EXP := 11
const BANNER_TIME_EXP := 12
const HERO_NAME := "Hero"

static var _tables: Dictionary = {}
static var _generals: Dictionary = {}
static var _talk: Dictionary = {}

var map: Dictionary
var w := 0
var h := 0
var flags: Array = []
var objects: Array = []
var rooms: Rooms
var cell := 0  # the current room
var room_phase := 2  # 0 playing, 1 cleared (exits open), 2 entered (banner), 3 just cleared
var room_phase_timer := 1
var exit_dir := 0  # 1 down 2 left 3 up 4 right while scrolling to the next room
var exit_blink := 0
var scrolling := false
var rooms_visited := 1
var mission := 0  # the mission of the map (its rooms' lists and the archers of its cells)
var waves: Array = []  # the current room's enemy list, flat: kind, count, kind, count, ...
var banner := 0
var banner_timer := 0
var acquired := 0  # the gear of the BANNER_ACQUIRED banner
## Places left in the hero's Inventory: a gear with no place stays on the floor.
var free_places := 45
var hero := MapActor.new()
var dir_history: Array[int] = [-1, -1, -1, -1, -1]
var hold_to_move := true  # the player's option: walk while the key is held
## The map without enemies (a test option): a room's list counts as defeated.
var no_enemies := false
var difficulty := 1  # 0 hard (gold and exp x2), 1 normal
var general_side := 0  # the side (weapon) of the last general met: 0 long, 1 short sword
var general := {}  # the last general met (campaign.json generals)
var hero_name := HERO_NAME  # how the hero is called in the talks (the hero's own name)
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
var enemies: Array[MapActor] = []  # in drawing order (sorted by y each tick)
var enemies_alive := 0  # archers do not count
var spawn_spots: Array[Vector3i] = []  # tile x, tile y, exit side (0 down 1 left 2 up 3 right)
var arrows: Array[MapArrow] = [MapArrow.new(), MapArrow.new(), MapArrow.new()]
var kills := 0
var play_ticks := 0  # ticks of play on the map (not banners, talks or room scrolls)
var ticks := 0  # every tick of the map: the aura's pictures go round with it
## The aura shows on the hero: a buff of his was on at the end of the last tick of play, or
## he picked something up in this one.
var hero_glows := false
var mission_exp := 0
## The mission's rewards and its general who talks after it (0 none, >= 200 none).
var mission_gold := 0
var mission_general := 0
var time_limit := 0  # seconds; in time the exp grows
var enemy_hp_percent := 100  # the vows of the run (Vows) make the enemies tougher
var time_exp := 0  # the exp for time, given when the mission was won in time
var hero_exp := 0  # the hero's exp into his level before the mission
var exp_bars := ExpBars.new()  # the exp bar of the pages Total Exp and Time Exp
## Friendship points of the generals the hero talked with (general id -> points).
var friendship := {}
var fought := {}  # the generals met as foes in this mission (general id -> true)
## What follows the talk: 0 the map goes on, 1 the exits open, 2 the mission is over.
var talk_after := 0
var failed := false
var finished := false  # the mission is over: the screen leaves
## The mission is won and its pages shown: the hero walks the last room to a side of it, the
## way on to the next place (the screen puts the arrows); way_out is the side walked into.
var choosing := false
var way_out := 0
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
var breakables: Array[MapBreakable] = []
var drops: Array[MapDrop] = []
var gold := 0
var items: Array[int] = []  # picked up this mission (potions and gear), in order
## The sound effects of this tick (sound numbers 3..16), for the screen to play.
var sounds: Array[int] = []

var _buffed := false


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


## The lines of data/talk.json `kind` (in English; I18n.text gives the player's language).
static func talk_lines(kind: String) -> Array:
	if _talk.is_empty():
		_talk = _load_json(TALK_PATH)
	return _talk.get(kind, [])


func _init(
	map_data: Dictionary = {}, mission_no: int = 0, start_tile: Vector2i = Vector2i(4, 4)
) -> void:
	if map_data.is_empty():
		return
	map = map_data
	mission = mission_no
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
	cell = MapRoomPlay.room_of(self, hero.pos)
	MapRoomPlay.enter_room(self)


## One tick. held: the 8-direction of the held direction key (0, 2, 4, 6) or -1.
## pressed: a direction key pressed this tick (-1 none), for the original's tap-to-walk.
## fire: the attack key was pressed (it also closes a banner). hotkey: a skill key (0..4)
## pressed, -1 none; potion: a potion key (0, 1), -1 none; belt: a belt slot (0..4) used by
## its own key (the skill bar's Z X C V B), -1 none.
func tick(
	held: int,
	pressed: int = -1,
	fire: bool = false,
	hotkey: int = -1,
	potion: int = -1,
	belt: int = -1
) -> void:
	sounds.clear()
	ticks += 1
	hero.prev_pos = hero.pos
	for e in enemies:
		e.prev_pos = e.pos
	if choosing:
		_tick_scene(held, pressed, 3 if fire else 0, potion)
		_hero_drawn()
		return
	if banner != 0:
		_tick_banner(fire)
		return
	if not talk.is_empty():
		MapTalks.tick_talk(self, fire)
		return
	if scrolling:
		MapRoomPlay.tick_scroll(self)
		return
	var skill := 3 if fire else 0
	if hotkey >= 0 and hotkey < hotkeys.size():
		skill = hotkeys[hotkey]
	if belt >= 0 and belt < quick_slots.size():
		potion = 10 + belt
	_tick_scene(held, pressed, skill, potion)
	if banner == 0 or banner == BANNER_ACQUIRED:
		_end_tick()


## The banners go on by themselves: a key shortens a "Stage" banner
## and "Mission fail!" to 2 more ticks, and "Level Up" on an exp bar, but not "Mission
## Success!" nor the exp pages.
func _tick_banner(fire: bool) -> void:
	if banner == BANNER_TOTAL_EXP or banner == BANNER_TIME_EXP:
		MapTalks.tick_exp_page(self, fire)
		return
	if fire and banner_timer > 2 and banner != BANNER_SUCCESS:
		banner_timer = 2
	banner_timer -= 1
	if banner_timer <= 0:
		var b := banner
		if b == BANNER_FAILED:
			finished = true
			return
		if b == BANNER_SUCCESS:
			MapTalks.next_result_page(self)
			return
		banner = 0
		if b == BANNER_STAGE_CLEAR:
			# Room cleared: the exits open (a room with a general: he talks first).
			var g := MapTalks.room_general(self)
			if g != 0:
				MapTalks.start_general_talk(self, g, 1)
			else:
				room_phase = 1
				room_phase_timer = 5


func show_banner(kind: int) -> void:
	banner = kind
	banner_timer = BANNER_TICKS


func _tick_scene(held: int, pressed: int, skill: int, potion: int = -1) -> void:
	play_ticks += 1
	hero_glows = _buffed
	for o in breakables:
		if o.active and o.break_frame != 0:
			o.break_frame -= 1
	MapHeroPlay.tick_effect(self)
	if potion >= 10:
		MapHeroPlay.use_slot(self, potion - 10)
	elif potion >= 0 and potion < quick_keys.size():
		MapHeroPlay.use_slot(self, quick_keys[potion])
	if effect_item > 0:
		# a potion being drunk or a scroll being read: the world waits
		if effect_item > 9:
			hero.frame = effect_step
		return
	MapEnemyPlay.spawn_next_enemy(self)
	hero.frame += 1
	dir_history[0] = pressed
	var anim := MapAnims.hero_anim(hero.action, hero.dir)
	if hero.frame >= anim.size() or int(anim[hero.frame]) > END:
		if hero.action == 2:
			for i in 5:
				dir_history[i] = -1
			pressed = -1
		elif hero.action == 10:
			# The hero fell: "Mission fail!" with its sound, then back to the menu.
			sound(6)
			hero.frame = 10
			failed = true
			show_banner(BANNER_FAILED)
			return
		hero.frame = 0
		if hero.action != 1:
			hero.action = 0
	if hold_to_move and pressed == -1 and hero.action < 2:
		MapHeroPlay.walk_while_held(self, held)
	if hero.action < 2:
		MapHeroPlay.start_hero_action(self, pressed, skill)
	MapHeroPlay.move_hero(self)
	if MapHeroPlay.hero_action_hits(self):
		MapEnemyPlay.tick_arrows(self)
		MapLoot.pick_up_drops(self)
		MapEnemyPlay.tick_enemies(self)
		MapEnemyPlay.sort_enemies(self)
	MapLoot.tick_broken(self)


## The mission clock: seconds of play.
func play_seconds() -> int:
	return play_ticks * TICK_MS / 1000


## The tick is drawn with the direction the hero moved in (a slide can turn it), then he looks
## where he faces again.
func _hero_drawn() -> void:
	hero.shown_dir = hero.dir
	hero.dir = hero.facing
	hero.last_action = hero.action
	hero.last_frame = hero.frame


func sound(n: int) -> void:
	sounds.append(n)


func _end_tick() -> void:
	MapEnemyPlay.advance_sparks(self)
	_hero_drawn()
	hero.idle_ticks += 1
	_buffed = hero.attack_buff_ticks > 0 or hero.defense_buff_ticks > 0
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
				show_banner(BANNER_STAGE)
				room_phase = 0
			3:
				show_banner(BANNER_STAGE_CLEAR)
				sound(5)
				room_phase = 0
			4:
				# the mission's general is defeated
				won = true
				show_banner(BANNER_SUCCESS)
				room_phase = 0
		return
	room_phase_timer -= 1


## Continuing a save on the map: the room was clear when it was saved, so it
## stays clear (no waves, no archers, no "Stage" banner) and its exits open.
func continue_in_clear_room() -> void:
	enemies.clear()
	enemies_alive = 0
	for i in waves.size():
		waves[i] = 0
	room_phase = 1
	room_phase_timer = 5


## The game can be saved on the map: no enemy alive, no general fighting, no wave to come.
func can_save() -> bool:
	for e in enemies:
		if e.hp > 0:
			return false
	return not boss_fight and (waves.is_empty() or int(waves[0]) == 0)


## After the mission's pages: the room empty and quiet, the hero free to walk to a side.
func start_choosing() -> void:
	choosing = true
	finished = false
	way_out = 0
	banner = 0
	talk.clear()
	enemies.clear()
	enemies_alive = 0
	for i in waves.size():
		waves[i] = 0
	room_phase = 0


## The exits are open and their arrows shown.
func exits_open() -> bool:
	return room_phase == 1 and room_phase_timer < 0


# ---- what the screens and the world ask of the map, done by its modules ----


## See MapRoomPlay.room_origin().
func room_origin() -> Vector2i:
	return MapRoomPlay.room_origin(self)


## See MapRoomPlay.enter_room().
func enter_room() -> void:
	MapRoomPlay.enter_room(self)


## See MapRoomPlay.max_enemies().
func max_enemies() -> int:
	return MapRoomPlay.max_enemies(self)


## See MapHeroPlay.skill_mp_need().
func skill_mp_need(skill: int, level: int = -1) -> int:
	return MapHeroPlay.skill_mp_need(self, skill, level)


## See MapHeroPlay.add_quick_item().
func add_quick_item(item: int) -> bool:
	return MapHeroPlay.add_quick_item(self, item)


## See MapEnemyPlay.create_enemy().
func create_enemy(kind: int, tx: int, ty: int, side: int) -> MapActor:
	return MapEnemyPlay.create_enemy(self, kind, tx, ty, side)


## See MapEnemyPlay.set_general().
func set_general(id: int) -> void:
	MapEnemyPlay.set_general(self, id)


## See MapAnims.enemy_actions().
func enemy_actions(e: MapActor) -> int:
	return MapAnims.enemy_actions(e)


## See MapAnims.enemy_anim().
func enemy_anim(e: MapActor, action: int) -> Array:
	return MapAnims.enemy_anim(e, action)


## See MapAnims.enemy_sprite_frame().
func enemy_sprite_frame(e: MapActor) -> int:
	return MapAnims.enemy_sprite_frame(e)


## See MapEnemyPlay.general_pick_skill().
func general_pick_skill(e: MapActor, force: bool) -> void:
	MapEnemyPlay.general_pick_skill(self, e, force)


## See MapHeroPlay.hero_is_hit().
func hero_is_hit(e: MapActor, a: MapArrow = null) -> void:
	MapHeroPlay.hero_is_hit(self, e, a)


## See MapPictures.fires().
func fires() -> Array:
	return MapPictures.fires(self)


## See MapPictures.auras().
func auras() -> Array:
	return MapPictures.auras(self)


## See MapPictures.sparks().
func sparks() -> Array:
	return MapPictures.sparks(self)


## See MapEnemyPlay.arrows_wait().
func arrows_wait() -> bool:
	return MapEnemyPlay.arrows_wait(self)


## See MapTalks.hero_talks().
func hero_talks() -> bool:
	return MapTalks.hero_talks(self)


## See MapTalks.talk_text().
func talk_text() -> String:
	return MapTalks.talk_text(self)


## See MapTalks.skip_talk().
func skip_talk() -> void:
	MapTalks.skip_talk(self)


## See MapTalks.gold_reward().
func gold_reward() -> int:
	return MapTalks.gold_reward(self)


## See MapTalks.exp_reward().
func exp_reward() -> int:
	return MapTalks.exp_reward(self)


## See MapLoot.breakable_shown().
func breakable_shown(b: MapBreakable) -> bool:
	return MapLoot.breakable_shown(b)


## See MapLoot.drop_item().
func drop_item(kind: int, p: Vector2i) -> void:
	MapLoot.drop_item(self, kind, p)


## See MapRoomPlay.open_sides().
func open_sides() -> Array[int]:
	return MapRoomPlay.open_sides(self)


## See MapRoomPlay.keep_in_room().
func keep_in_room(pos: Vector2i, dx: int, dy: int) -> Vector2i:
	return MapRoomPlay.keep_in_room(self, pos, dx, dy)


## See MapWalls.cell_free().
func cell_free(q: int) -> bool:
	return MapWalls.cell_free(self, q)


## See MapWalls.step_until_free().
func step_until_free(pos: Vector2i, step: int, direction: int) -> int:
	return MapWalls.step_until_free(self, pos, step, direction)


## See MapWalls.move().
func move(pos: Vector2i, dx: int, dy: int, direction: int, actor: MapActor) -> int:
	return MapWalls.move(self, pos, dx, dy, direction, actor)


## See MapWalls.slide_corner().
func slide_corner(pos: Vector2i, direction: int, actor: MapActor) -> int:
	return MapWalls.slide_corner(self, pos, direction, actor)


## See MapPictures.effects().
func effects() -> Array:
	return MapPictures.effects(self)


## See MapPictures.trails().
func trails(pick: RandomNumberGenerator) -> Array:
	return MapPictures.trails(self, pick)


## See MapAnims.hero_sprite_frame().
func hero_sprite_frame() -> int:
	return MapAnims.hero_sprite_frame(self)
