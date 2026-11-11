class_name MapEnemyPlay
extends RefCounted
## The enemies on the map: soldiers coming in by waves, their AI, their strikes and arrows, the
## generals' skills, their deaths and the hit sparks.
## Static functions over the state of a MapSim (MapSim.tick() runs them).

const SPAWN_DX := [0, -56, 0, 56, 0]
const SPAWN_DY := [56, 0, -56, 0, 0]
const TURNS := [-2, -1, 0, 0, 0, 0, 1, 2]
const ATTACK_PCT := [100, 100, 150]
const BASE_ATTACK := [3, 2, 3]
const BASE_HP := [7, 5, 7]
const ARROW_DX := [-1, -15, -1, 5]
const ARROW_DY := [-5, -13, -30, -13]
## A squad moves as if it stood this far aside (the side its men stand on), by direction.
const SQUAD_SHIFT := {
	3: Vector2i(-20, 0),
	1: Vector2i(-20, 20),
	2: Vector2i(-20, 0),
	0: Vector2i(0, 20),
	5: Vector2i(20, 0),
	7: Vector2i(20, 20),
	6: Vector2i(20, 0)
}
const GENERAL_REACH := [60, 50]


## The next enemy of the room's list comes in while fewer than the room's maximum are alive.
static func spawn_next_enemy(sim: MapSim) -> void:
	if sim.no_enemies:
		# The map without enemies: the room's list counts as defeated at once, except a
		# list with a general (kind < 200), which only the fight with him can end.
		for k in range(0, 14, 2):
			if sim.waves[k] > 0 and sim.waves[k] < 200:
				return
		if sim.room_phase == 0 and sim.waves[0] != 0:
			for k in 14:
				sim.waves[k] = 0
			sim.room_phase = 3
			sim.room_phase_timer = 5
		return
	if sim.enemies_alive >= MapRoomPlay.max_enemies(sim) or sim.waves[0] == 0:
		return
	if not (sim.waves[0] >= 200 or not sim.boss_spawned) or sim.spawn_spots.is_empty():
		return  # one general at a time
	var spot: Vector3i = sim.spawn_spots[sim.rng.below(sim.spawn_spots.size())]
	create_enemy(sim, sim.waves[0], spot.x, spot.y, spot.z)
	sim.waves[1] -= 1
	if sim.waves[1] < 1:
		for b in 12:
			sim.waves[b] = sim.waves[b + 2]


## A soldier or a general (kind < 200) outside the room behind exit `side`, looking in.
static func create_enemy(sim: MapSim, kind: int, tx: int, ty: int, side: int) -> MapActor:
	var e := MapActor.new()
	e.pos = Vector2i(tx * 27 + 12 + SPAWN_DX[side], ty * 27 + 20 + SPAWN_DY[side])
	e.prev_pos = e.pos
	e.dir = ((side << 1) + 4) & 7
	e.facing = e.dir
	if kind == MapSim.KIND_SWORDS and sim.rng.range_of(0, 2) != 0:
		kind = MapSim.KIND_SQUAD
	e.type = kind
	e.think_ticks = 14
	if kind == MapSim.KIND_ARCHERS:
		e.alerted = 1
		e.think_ticks = 15
	if kind > 200:
		enemy_stats(sim, e, kind - 201)
	else:
		if kind == sim.boss_type:
			sim.boss_fight = true
		sim.boss_spawned = true
		set_general(sim, kind)
		MapTalks.start_map_talk(sim)
		general_stats(sim, e)
		sim.waves[1] = 1
	sim.enemies.append(e)
	if kind != MapSim.KIND_ARCHERS:
		sim.enemies_alive += 1
	return e


## Level, attack, defence and HP of a new soldier (kind 0 swords, 1 archers, 2 squad).
static func enemy_stats(sim: MapSim, e: MapActor, kind: int) -> void:
	if sim.hero.level < 21:
		e.level = maxi(sim.hero.level + sim.rng.range_of(0, 5) - 2, 1)
	elif sim.hero.level < 41:
		e.level = sim.hero.level + sim.rng.below(9) - 3
	else:
		e.level = sim.hero.level + sim.rng.below(16) - 5
	e.attack = (BASE_ATTACK[kind] + e.level) * ATTACK_PCT[kind] / 100
	e.defense = e.level - 1
	e.hp = BASE_HP[kind] + 3 * e.level
	e.max_hp = e.hp


## A general's stats: his own, raised by his level (the hero's plus the list's count).
static func general_stats(sim: MapSim, e: MapActor) -> void:
	e.level = sim.hero.level + sim.waves[1]
	e.attack = (int(sim.general.get("attack", 0)) + e.level - 1) * 6 / 5
	e.defense = (int(sim.general.get("defense", 0)) + e.level - 1) * 6 / 5
	e.hp = int(sim.general.get("hp", 1)) + (e.level - 1) * 3
	e.max_hp = e.hp


static func set_general(sim: MapSim, id: int) -> void:
	sim.general = MapSim.general_data(id)
	sim.general_side = int(sim.general.get("side", 0))


## Direction 0..7 to the hero, straight within 27 px.
static func dir_to_hero(sim: MapSim, p: Vector2i) -> int:
	var i := sim.hero.pos.x - p.x
	var dy := sim.hero.pos.y - p.y
	if i > 27:
		return 7 if dy > 27 else (5 if dy < -27 else 6)
	if i < -27:
		return 1 if dy > 27 else (3 if dy < -27 else 2)
	return 0 if dy > 0 else 4


## The enemy's next action, every 6 ticks while it stands or walks.
static func choose_enemy_action(sim: MapSim, e: MapActor) -> void:
	var dist := MapGeometry.distance(sim.hero.pos, e.pos)
	e.frame = 0
	var roll := sim.rng.below(1000)
	var to_hero := dir_to_hero(sim, e.pos)
	if e.type == MapSim.KIND_SWORDS or e.type == MapSim.KIND_SQUAD:
		_soldier_action(sim, e, dist, roll, to_hero)
	elif e.type == MapSim.KIND_ARCHERS:
		e.action = 1
		e.think_ticks = 15
		shoot_arrow(sim, e)
	elif roll < 150:
		general_pick_skill(sim, e, false)
	elif roll < 350:
		if (
			dist <= 60
			and (sim.hero.action != 9 or sim.hero.frame >= 6)
			and sim.hero.action != 10
			and sim.hero.action < 12
		):
			e.action = 1
			e.dir = MapGeometry.dir4(e.pos, sim.hero.pos)
			e.facing = e.dir
	else:
		e.dir = to_hero
		e.facing = to_hero


## A swordsman (or a squad) walks about, closer to the hero when he is near (90 px), and
## strikes him within 45 px.
static func _soldier_action(sim: MapSim, e: MapActor, dist: int, roll: int, to_hero: int) -> void:
	var near := 1 if dist < 90 else 0
	e.action = 0
	if roll < 150 + near * 300:
		e.dir = (to_hero + TURNS[roll & 7]) & 7
	elif roll < 850 - near * 100:
		if near == 0:
			e.dir = (e.dir + TURNS[roll & 7]) & 7
		elif dist <= 45 and sim.hero.action != 9 and sim.hero.action != 10 and sim.hero.action < 12:
			e.action = 1
			e.dir = MapGeometry.dir4(e.pos, sim.hero.pos)
			e.facing = e.dir
			MapHeroPlay.hero_is_hit(sim, e)
			return
		else:
			e.dir = (to_hero + TURNS[roll & 7]) & 7
	elif near != 0:
		e.dir = roll & 7
	else:
		e.dir = (e.dir + TURNS[roll & 7]) & 7
	e.facing = e.dir


## A general picks one of his four skills (an empty slot is a plain strike); a heal only
## while below half HP and four times at most; force: no buff (he was just hit).
static func general_pick_skill(sim: MapSim, e: MapActor, force: bool) -> void:
	var skills: Array = sim.general.get("skills", [0, 0, 0, 0])
	e.action = 6 + int(skills[sim.rng.below(4)]) - 1
	if e.action == 9 or e.action == 10:
		if e.skill_step > 3:
			e.action = 1
		elif e.max_hp >> 1 > e.hp:
			e.skill_step += 1
		else:
			e.action = 1
	elif e.action in [11, 12, 13] and force:
		e.action = 1
	e.dir = MapGeometry.dir4(e.pos, sim.hero.pos)
	e.facing = e.dir


static func shoot_arrow(sim: MapSim, e: MapActor) -> void:
	var i := e.dir >> 1
	for a in sim.arrows:
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
static func tick_enemies(sim: MapSim) -> void:
	var b := 0
	while b < sim.enemies.size():
		_tick_enemy(sim, sim.enemies[b])
		b += 1


## One tick of an enemy. One that dies leaves the list, so the one after it waits a tick.
static func _tick_enemy(sim: MapSim, e: MapActor) -> void:
	e.action = mini(e.action, MapAnims.enemy_actions(e) - 1)
	e.frame += 1
	e.think_ticks -= 1
	var anim := MapAnims.enemy_anim(e, e.action)
	var anim_frame := int(anim[mini(e.frame, anim.size() - 1)])
	_tick_buffs(e)
	if e.action == 3:
		if anim_frame > MapSim.END:
			_enemy_dies(sim, e)
			if sim.enemies_alive < 1 and sim.waves[0] == 0 and e.type != MapSim.KIND_ARCHERS:
				_room_won(sim)
		return
	if anim_frame > MapSim.END:
		e.action = 3 if e.hp < 1 else 0
		e.frame = 0
	if e.think_ticks < 1:
		e.alerted = 1
		e.think_ticks = 6
		if e.action == 0:
			choose_enemy_action(sim, e)
	if e.type == MapSim.KIND_ARCHERS:
		e.dir = MapGeometry.dir4(e.pos, sim.hero.pos)
		e.facing = e.dir
		return
	if e.alerted == 0:
		# still outside: walks straight in, through anything
		e.pos += MapWalls.dir_step(e.facing)
		return
	_move_enemy(sim, e)
	_action_frame(sim, e)


static func _tick_buffs(e: MapActor) -> void:
	if e.attack_buff_ticks > 0:
		e.attack_buff_ticks -= 1
		if e.attack_buff_ticks < 1:
			e.attack_buff = 0
	if e.defense_buff_ticks > 0:
		e.defense_buff_ticks -= 1
		if e.defense_buff_ticks < 1:
			e.defense_buff = 0


## The last enemy of the room's list is dead: the room is cleared, or the mission's general
## defeated.
static func _room_won(sim: MapSim) -> void:
	if sim.boss_fight:
		sim.room_phase = 4
		sim.room_phase_timer = 22
	else:
		sim.room_phase = 3
		sim.room_phase_timer = 5


## The enemy's step this tick, by its action: walking, a strike's small step, knocked back,
## or a general's skill (MapWalls.skill_step).
static func _move_enemy(sim: MapSim, e: MapActor) -> void:
	var move_dir := e.facing
	var step := Vector2i.ZERO
	match e.action:
		0:
			step = MapWalls.dir_step(move_dir)
		1, 4, 5:
			step = MapWalls.dir_step(e.dir) / 3
		2:
			move_dir = (e.facing + 4) & 7
			if e.ai_mode > 0:
				e.ai_mode -= 1
				step = MapWalls.dir_step(move_dir) * 4
			elif e.frame == 1:
				step = MapWalls.dir_step(move_dir) * 3 / 4
		_:
			if e.action >= 6:
				step = MapWalls.skill_step(sim, e, e.action + 6, e.frame, e.dir)
	if step != Vector2i.ZERO:
		_enemy_step(sim, e, step, move_dir)


## The enemy steps (a squad as if it stood aside, where its men are); walking straight into a
## wall, it slides round its corner.
static func _enemy_step(sim: MapSim, e: MapActor, step: Vector2i, move_dir: int) -> void:
	var i: int
	if e.type == MapSim.KIND_SQUAD:
		var shift: Vector2i = SQUAD_SHIFT.get(move_dir, Vector2i.ZERO)
		i = MapWalls.move(sim, e.pos + shift, step.x, step.y, move_dir, e)
		if i != -1:
			e.pos -= shift
	else:
		i = MapWalls.move(sim, e.pos, step.x, step.y, move_dir, e)
	if e.action == 0 and move_dir in [0, 2, 4, 6] and i == -1:
		i = MapWalls.slide_corner(sim, e.pos, e.facing, e)
		if i != -1:
			var slide := MapWalls.dir_step(i)
			MapWalls.move(sim, e.pos, slide.x, slide.y, i, e)


## What the enemy's action does on this frame: a strike at the hero, a general's heal
## (9: 20 %, 10: 50 %) or his buffs for 50 ticks (11 attack, 12 defence, 13 both).
static func _action_frame(sim: MapSim, e: MapActor) -> void:
	var action := e.action
	if _strikes_now(action, e.frame):
		_enemy_strikes_hero(sim, e)
	elif e.frame != 11:
		return
	elif action == 9 or action == 10:
		e.hp = mini(e.hp + e.max_hp * (20 if action == 9 else 50) / 100, e.max_hp)
	elif action >= 11 and action <= 13:
		var div := int(MapSim.BUFF_DIV[action - 11])
		if action != 12:
			e.attack_buff = maxi(e.attack / div, 1)
			e.attack_buff_ticks = 50
		if action != 11:
			e.defense_buff = maxi(e.defense / div, 1)
			e.defense_buff_ticks = 50


## Whether the enemy's action strikes on this frame.
static func _strikes_now(action: int, frame: int) -> bool:
	match action:
		1, 4, 5:
			return frame == 1
		6:
			return frame > 2 and frame < 6
		7:
			return frame > 4 and frame < 8
		8:
			return frame in [2, 4, 6, 8]
		14, 19:
			return (frame & 1) != 0
		15, 17, 18:
			return frame == 5
		16:
			return frame == 6
		20, 21:
			return frame == 8
	return false


static func _general_reach(sim: MapSim) -> int:
	return GENERAL_REACH[sim.general_side]


## The enemy's strike or skill lands on the hero if he is where it reaches.
static func _enemy_strikes_hero(sim: MapSim, e: MapActor) -> void:
	var action := e.action
	if sim.hero.action != 9 and sim.hero.action != 10:
		if sim.hero.action >= 12:
			return
		match action:
			7:
				var side := e.dir >> 1
				if MapGeometry.boxes_touch(
					e.pos.x + int(MapSim.table("hit_box_x")[side]),
					e.pos.y + int(MapSim.table("hit_box_y")[side]),
					int(MapSim.table("hit_box_w")[side]),
					int(MapSim.table("hit_box_h")[side]),
					sim.hero.pos.x - 8,
					sim.hero.pos.y - 8,
					17,
					17
				):
					MapHeroPlay.hero_is_hit(sim, e)
				return
			16:
				if MapGeometry.is_in_front(e.pos, sim.hero.pos, e.dir):
					_general_strike_if_near(sim, e, _general_reach(sim))
				return
			17, 18:
				_general_strike_if_near(sim, e, 45)
				return
			19:
				if ((e.dir + (e.frame >> 1 << 1)) & 7) == MapGeometry.dir4(e.pos, sim.hero.pos):
					_general_strike_if_near(sim, e, _general_reach(sim))
				return
			20, 21:
				if MapGeometry.distance(front_of(e.pos, e.dir), sim.hero.pos) <= 35:
					general_skill_hits_hero(sim, e)
				return
		if e.dir == MapGeometry.dir4(e.pos, sim.hero.pos):
			_general_strike_if_near(sim, e, _general_reach(sim))
	elif sim.hero.action == 9:
		if action == 8 or action == 14:
			if e.dir == MapGeometry.dir4(e.pos, sim.hero.pos):
				_general_strike_if_near(sim, e, _general_reach(sim))
		elif action == 20 or action == 21:
			if MapGeometry.distance(front_of(e.pos, sim.hero.dir), sim.hero.pos) <= 35:
				general_skill_hits_hero(sim, e)


static func front_of(p: Vector2i, d8: int) -> Vector2i:
	return (
		p + Vector2i(int(MapSim.table("front_dx")[d8 >> 1]), int(MapSim.table("front_dy")[d8 >> 1]))
	)


static func _general_strike_if_near(sim: MapSim, e: MapActor, reach: int) -> void:
	if MapGeometry.distance(sim.hero.pos, e.pos) <= reach:
		general_skill_hits_hero(sim, e)


## A skill pushes the hero back (hurt ticks) as well as hurting him.
static func general_skill_hits_hero(sim: MapSim, e: MapActor) -> void:
	match e.action:
		6:
			e.frame = 5
			sim.hero.hurt_ticks = 2
		8, 16:
			sim.hero.hurt_ticks = 2
		15, 21:
			sim.hero.hurt_ticks = 5
		17:
			MapHeroPlay.set_on_fire(sim, sim.hero)
		18:
			sim.hero.hurt_ticks = 5
			MapHeroPlay.set_on_fire(sim, sim.hero)
		19:
			sim.hero.hurt_ticks = 2
			MapHeroPlay.set_on_fire(sim, sim.hero)
	MapHeroPlay.hero_is_hit(sim, e)


static func _enemy_dies(sim: MapSim, e: MapActor) -> void:
	if e.type < 200:
		sim.mission_exp += e.level << 1
		sim.boss_spawned = false
		MapLoot.drop_item(sim, 2 if sim.boss_fight else 1, e.pos)
	else:
		sim.mission_exp += e.level
		MapLoot.drop_item(sim, 0, e.pos)
	sim.kills += 3 if e.type == MapSim.KIND_SQUAD else 1
	sim.enemies.erase(e)
	if e.type != MapSim.KIND_ARCHERS:
		sim.enemies_alive -= 1


static func sort_enemies(sim: MapSim) -> void:
	for b in range(sim.enemies.size() - 1):
		for i in range(b + 1, sim.enemies.size()):
			if sim.enemies[b].pos.y > sim.enemies[i].pos.y:
				var t: MapActor = sim.enemies[b]
				sim.enemies[b] = sim.enemies[i]
				sim.enemies[i] = t


## A hit spark starts where the actor stands; it shows the next two ticks.
static func spark_at(a: MapActor) -> void:
	a.hit_fx_pos = a.pos
	a.hit_fx_frame = -1


static func advance_sparks(sim: MapSim) -> void:
	for a in [sim.hero] + sim.enemies:
		if a.hit_fx_kind != 0:
			a.hit_fx_frame += 1
			if a.hit_fx_frame > 1:
				a.hit_fx_kind = 0
		if a.on_fire:
			a.fire_frame += 1
			if a.fire_frame > 5:
				a.on_fire = false


## Arrows fly 12 px a tick for 22 ticks; one that touches the hero hits him.
static func tick_arrows(sim: MapSim) -> void:
	for a in sim.arrows:
		if not a.active:
			continue
		if (
			MapGeometry.boxes_touch(
				a.pos.x, a.pos.y + 8, a.w, a.h, sim.hero.pos.x - 12, sim.hero.pos.y - 20, 17, 18
			)
			and sim.hero.action < 12
		):
			a.active = false
			MapHeroPlay.hero_is_hit(sim, null, a)
			continue
		if arrows_wait(sim):
			continue
		a.ticks += 1
		if a.ticks > 22:
			a.active = false
			continue
		match a.dir:
			0:
				a.pos.y += 12
			1:
				a.pos.x -= 12
			2:
				a.pos.y -= 12
			3:
				a.pos.x += 12


## The arrows stand still while a big skill of the hero holds the room (by the
## hero's action and frame of the last tick): skills 26 and 27 on their
## frames 2 to 8, 28 from frame 4 on, 29 from frame 7 on, 30 on frames 4 to 14.
static func arrows_wait(sim: MapSim) -> bool:
	var action := sim.hero.last_action
	var frame := sim.hero.last_frame
	if action == 26 or action == 27:
		return frame > 1 and frame < 9
	if action == 28:
		return frame > 3
	if action == 29:
		return frame > 6
	return action == 30 and frame > 3 and frame < 15
