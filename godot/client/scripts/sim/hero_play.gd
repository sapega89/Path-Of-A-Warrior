class_name MapHeroPlay
extends RefCounted
## The hero on the map: his walking, running, sword and skills, his potions and scrolls, and his
## blows landing on enemies.
## Static functions over the state of a MapSim (MapSim.tick() runs them).

## The frame of an attack that hits, by action (sword 3..8, skills 21..24).
const HIT_FRAME := [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 6, 5, 5]
## Potions 1..9 restore HP (1), MP (2) or both (3) by 30 / 60 / 100 %.
const RESTORES := [1, 1, 1, 2, 2, 2, 3, 3, 3]
const RESTORE_PCT := [30, 60, 100, 30, 60, 100, 30, 60, 100]
## How many ticks an effect lasts, by effect item + 2 (-2, -1 scrolls in flight, 1..9 potions).
const EFFECT_STEPS := [2, 10, 100, 2, 2, 2, 2, 2, 2, 2, 2, 2, 100, 100]


static func walk_while_held(sim: MapSim, held: int) -> void:
	if held < 0:
		if sim.hero.action == 1:
			sim.hero.action = 0
			sim.hero.frame = 0
	elif sim.hero.action == 0 or sim.hero.facing != held:
		sim.hero.dir = held
		sim.hero.facing = held
		sim.hero.action = 1
		sim.hero.frame = 0


static func start_hero_action(sim: MapSim, pressed: int, skill: int = 0) -> void:
	if pressed > -1:
		if check_run(sim):
			sim.hero.action = 2
			sim.hero.frame = 0
			sim.hero.dir = pressed
			sim.hero.facing = pressed
		elif sim.hero.facing == pressed:
			sim.hero.action = (sim.hero.action + 1) & 1
			sim.hero.frame = 0
		else:
			sim.hero.dir = pressed
			sim.hero.facing = pressed
			sim.hero.action = 1
			sim.hero.frame = 0
	if skill == 3:
		# The sword: strikes in quick succession make a combo (actions 3-5 short, 6-8 long sword).
		if sim.hero.idle_ticks < 7:
			sim.hero.combo = (sim.hero.combo + 1) % 3
		else:
			sim.hero.combo = 0
		sim.hero.idle_ticks = 0
		sim.hero.action = 3 + sim.hero.combo + (sim.hero.weapon_kind ^ 1) * 3
		sim.hero.frame = 0
		sim.hero.facing = int(MapSim.table("dir8_to_dir4")[sim.hero.facing]) << 1
		sim.hero.dir = sim.hero.facing
	elif skill > 0 and skill_mp_cost(sim, skill) != 0:
		sim.hero.facing = int(MapSim.table("dir8_to_dir4")[sim.hero.facing]) << 1
		sim.hero.dir = sim.hero.facing
		sim.hero.action = skill
		sim.hero.frame = 0
		if skill in [15, 16, 21, 22, 23, 24, 25]:
			sim.sound(11)


## The MP a skill (12..30) costs at a level (at its own level when level is -1).
static func skill_mp_need(sim: MapSim, skill: int, level: int = -1) -> int:
	if skill < 12 or skill > 30:
		return 0
	var k := skill - 12
	if level < 0:
		level = sim.skill_levels[k]
	return MapSim.SKILL_BASE_COST[k] + (level - 1) * MapSim.SKILL_COST_PER_LEVEL[k]


## Takes the MP of a skill (12..30) at its level; 0 = not enough MP (nothing is taken).
static func skill_mp_cost(sim: MapSim, skill: int) -> int:
	var cost := skill_mp_need(sim, skill)
	if cost > sim.hero.mp:
		return 0
	sim.hero.mp -= cost
	return cost


## A direction pressed twice quickly: run.
static func check_run(sim: MapSim) -> bool:
	if sim.dir_history[0] > -1:
		return sim.dir_history[0] == sim.dir_history[1] or sim.dir_history[0] == sim.dir_history[2]
	return false


static func move_hero(sim: MapSim) -> void:
	var move_dir := sim.hero.facing
	var step := MapWalls.dir_step(move_dir)
	var frame := sim.hero.frame
	match sim.hero.action:
		1:
			pass
		2:
			step *= 4
		3, 4, 5, 6, 7, 8:
			step /= 3
		10:
			step = Vector2i.ZERO
			if frame < 10:
				sim.hero.pos.x += -1 if (frame & 1) != 0 else 1
		9:
			move_dir = (sim.hero.facing + 4) & 7
			step = MapWalls.dir_step(move_dir)
			if sim.hero.hurt_ticks > 0:
				sim.hero.hurt_ticks -= 1
				step *= 4
			elif frame == 1:
				step = step * 3 / 4
			else:
				step = Vector2i.ZERO
		_:
			step = MapWalls.skill_step(sim, sim.hero, sim.hero.action, frame, move_dir)
	if step != Vector2i.ZERO:
		_walk_step(sim, step, move_dir)


## The hero steps; walking straight into a wall, he slides round its corner.
static func _walk_step(sim: MapSim, step: Vector2i, move_dir: int) -> void:
	var i := MapWalls.move(sim, sim.hero.pos, step.x, step.y, move_dir, sim.hero)
	if sim.hero.action != 1:
		return
	if sim.hero.facing in [0, 2, 4, 6]:
		if i == -1:  # a wall: slide around the corner
			i = MapWalls.slide_corner(sim, sim.hero.pos, sim.hero.dir, sim.hero)
			if i != -1:
				var slide := MapWalls.dir_step(i)
				i = MapWalls.move(sim, sim.hero.pos, slide.x, slide.y, i, sim.hero)
				if i > -1 and i < 8:
					sim.hero.dir = i
	elif i != -1 and i != 9:
		sim.hero.dir = i


## The frames of the hero's action that hit, heal or buff. False: a skill's cinematic
## stops the world this tick (arrows and enemies wait).
static func hero_action_hits(sim: MapSim) -> bool:
	var action := sim.hero.action
	var frame := sim.hero.frame
	if action >= 26:
		return _cinematic_frame(sim, action, frame)
	if action == 15 or action == 16:
		if frame == 11:
			_heal(sim, action)
	elif action >= 17 and action <= 19:
		_buff_frame(sim, action, frame)
	else:
		_strike_frame(sim, action, frame)
	return true


## The frames of the sword and of the strike skills that hit, and their sounds.
static func _strike_frame(sim: MapSim, action: int, frame: int) -> void:
	if (action >= 3 and action <= 8) or (action >= 21 and action <= 24):
		if frame == HIT_FRAME[action]:
			if action <= 8:
				_turn_to_nearest(sim)
			if action in [3, 4, 6, 7]:
				sim.sound(15)
			elif action in [5, 8, 21, 22]:
				sim.sound(16)
			else:
				sim.sound(9)
			_strike(sim)
		return
	match action:
		2:
			if frame == 1:
				sim.sound(7)
		12:
			if frame > 2 and frame < 6:
				if frame == 3:
					sim.sound(7)
				_strike(sim)
		13:
			if frame > 4 and frame < 8:
				if frame == 5:
					sim.sound(7)
				_strike(sim)
		14:
			if frame in [2, 4, 6, 8]:
				sim.sound(15)
				_strike(sim)
		20:
			if (frame & 1) != 0:
				sim.sound(15)
				sim.hero.combo = 0 if frame in [1, 5, 9] else 2
				_strike(sim)
		25:
			if (frame & 1) != 0:
				sim.sound(9)
				_strike(sim)


## The heals: 15 a little, 16 more, by their levels.
static func _heal(sim: MapSim, action: int) -> void:
	sim.sound(8)
	if action == 15:
		sim.hero.hp += sim.hero.max_hp * (4 + sim.skill_levels[3]) / 25
	else:
		sim.hero.hp += sim.hero.max_hp * (9 + sim.skill_levels[4]) / 20
	_clamp_hero(sim)


## The buffs: attack (17), defence (18), both (19), for longer at higher levels.
static func _buff_frame(sim: MapSim, action: int, frame: int) -> void:
	if frame == 4:
		sim.sound(12)
	if frame != 11:
		return
	var lv := sim.skill_levels[action - 12]
	var ticks := 50 if lv < 4 else (100 if lv < 8 else 150)
	var div := int(MapSim.BUFF_DIV[action - 17])
	if action != 18:
		sim.hero.attack_buff = maxi(sim.hero.attack * lv / div, 1)
		sim.hero.attack_buff_ticks = ticks
	if action != 17:
		sim.hero.defense_buff = maxi(sim.hero.defense * lv / div, 1)
		sim.hero.defense_buff_ticks = ticks


## The skills that stop the world while they play (26..30): false on those frames.
static func _cinematic_frame(sim: MapSim, action: int, frame: int) -> bool:
	match action:
		26, 27:
			if frame == 8:
				if action == 27:
					sim.sound(9)
				_strike(sim)
			if frame > 1 and frame < 9:
				if frame == 2:
					sim.sound(13)
				return false
		28:
			if frame == 22:
				_strike(sim)
			elif frame > 3:
				if frame == 6:
					sim.sound(13)
				return false
		29:
			if frame == 22:
				_strike(sim)
			elif frame > 6:
				if frame == 7:
					sim.sound(14)
				return false
		30:
			if frame == 4:
				sim.sound(11)
			elif frame == 13:
				sim.sound(9)
			if frame > 3 and frame < 15:
				return false
			if frame == 15:
				_strike(sim)
	return true


## The hero's blow lands on the enemies and the breakables in its reach.
static func _strike(sim: MapSim) -> void:
	_hero_attack(sim, 0)
	MapLoot.hero_hits_breakables(sim)


static func _clamp_hero(sim: MapSim) -> void:
	sim.hero.hp = mini(sim.hero.hp, sim.hero.max_hp)
	sim.hero.mp = mini(sim.hero.mp, sim.hero.max_mp)


## The item of a quick slot (0..4) goes into use, by a potion key or the slot's belt key (a
## scroll only while standing or walking: the hero holds it up first).
static func use_slot(sim: MapSim, sel: int) -> void:
	if sim.effect_item != 0 or sim.hero.action >= 10 or sel < 0 or sel >= sim.quick_slots.size():
		return
	var item := int(sim.quick_slots[sel][0])
	if item == 0:
		return
	if item > 9:
		if sim.hero.action > 1:
			return
		sim.hero.action = 11
	else:
		sim.sound(8)
	sim.effect_item = item
	sim.effect_slot = sel
	sim.effect_step = 0
	sim.effect_pos = sim.hero.pos
	sim.effect_dir = int(MapSim.table("dir8_to_dir4")[sim.hero.dir])


## One tick of the item in use: a potion restores after 2 ticks; a scroll is read for 5
## ticks, then its blast flies in front of the hero and strikes (-2 fire once, -1 lightning
## three times) everyone within 35 px.
static func tick_effect(sim: MapSim) -> void:
	if sim.effect_item == 0:
		return
	if sim.effect_item == -1:
		if sim.effect_step in [1, 4, 7]:
			_hero_attack(sim, -1)
	elif sim.effect_item == -2 and sim.effect_step == 1:
		_hero_attack(sim, -2)
	sim.effect_step += 1
	if sim.effect_item > 9 and sim.effect_step > 4:
		sim.sound(9)
		sim.effect_pos = MapEnemyPlay.front_of(sim.effect_pos, sim.effect_dir << 1)
		sim.effect_item -= 12
		sim.effect_step = 0
	if sim.effect_step >= EFFECT_STEPS[sim.effect_item + 2]:
		if sim.effect_item > 0:
			var k := sim.effect_item - 1
			if (RESTORES[k] & 1) != 0:
				sim.hero.hp += sim.hero.max_hp * RESTORE_PCT[k] / 100
			if (RESTORES[k] & 2) != 0:
				sim.hero.mp += sim.hero.max_mp * RESTORE_PCT[k] / 100
			_clamp_hero(sim)
		var slot: Array = sim.quick_slots[sim.effect_slot]
		slot[1] -= 1
		if slot[1] < 1:
			slot[0] = 0
			slot[1] = 0
		sim.effect_item = 0


## A potion or scroll picked up goes to its quick slot (5 of a kind at most); false if full.
static func add_quick_item(sim: MapSim, item: int) -> bool:
	var free := -1
	for b in sim.quick_slots.size():
		if int(sim.quick_slots[b][0]) == item:
			if int(sim.quick_slots[b][1]) > 4:
				return false
			sim.quick_slots[b][1] += 1
			return true
		if int(sim.quick_slots[b][0]) == 0 and free < 0:
			free = b
	if free < 0:
		return false
	sim.quick_slots[free] = [item, 1]
	return true


## The hero is hit by an enemy (e) or by an arrow (a).
static func hero_is_hit(sim: MapSim, e: MapActor, a: MapArrow = null) -> void:
	var dmg := 0
	if e != null:
		sim.hero.facing = MapGeometry.dir8(sim.hero.pos, e.pos)
		dmg = e.attack + e.attack_buff - sim.hero.defense - sim.hero.defense_buff
		if e.action in [6, 7, 8, 14, 15, 16, 17, 18, 19, 20, 21]:
			dmg += e.attack / int(MapSim.table("skill_attack_div")[e.action - 6])
	else:
		sim.hero.facing = ((a.dir << 1) + 4) & 7
		dmg = a.attack - sim.hero.defense - sim.hero.defense_buff
	sim.hero.dir = sim.hero.facing
	dmg = maxi(dmg, 1)
	sim.hero.hp = sim.hero.hp - dmg if sim.hero.hp > dmg else 0
	if e != null:
		_show_target_info(sim, e)
	sim.hero.hit_fx_kind = 1
	MapEnemyPlay.spark_at(sim.hero)
	sim.hero.frame = 0
	sim.hero.action = 9
	sim.sound(4 if sim.hero.hurt_ticks != 0 else 16)
	if sim.hero.hp < 1:
		sim.hero.hp = 0
		sim.hero.action = 10


static func _show_target_info(sim: MapSim, e: MapActor) -> void:
	var names := MapSim.table("troop_names")
	var name := (
		String(TranslationServer.translate(str(sim.general.get("name", ""))))
		if e.type < 200
		else (str(names[e.type - 201]) if e.type - 201 < names.size() else "")
	)
	sim.target_info = {
		"name": name, "level": e.level, "hp_bar": e.hp * 60 / maxi(e.max_hp, 1), "ticks": 10
	}


## The hero's attack (kind 0, by his action) or a scroll's blast (-1, -2) against the enemies.
static func _hero_attack(sim: MapSim, kind: int) -> void:
	var reach := int(MapSim.table("weapon_reach")[sim.hero.weapon_kind])
	for e in sim.enemies.duplicate():
		if not (e.hp > 0 and e.alerted != 0 and e.action < 6):
			continue
		if kind == 0:
			match sim.hero.action:
				13:
					var side := sim.hero.dir >> 1
					if MapGeometry.boxes_touch(
						sim.hero.pos.x + int(MapSim.table("hit_box_x")[side]),
						sim.hero.pos.y + int(MapSim.table("hit_box_y")[side]),
						int(MapSim.table("hit_box_w")[side]),
						int(MapSim.table("hit_box_h")[side]),
						e.pos.x - 8,
						e.pos.y - 8,
						17,
						17
					):
						_hero_hits_enemy(sim, e, sim.hero.action)
						sim.sound(3)
				22:
					if MapGeometry.is_in_front(sim.hero.pos, e.pos, sim.hero.dir):
						_hero_strike_if_near(sim, e, reach)
				23, 24:
					_hero_strike_if_near(sim, e, 45)
				25:
					if (
						((sim.hero.dir + (sim.hero.frame >> 1 << 1)) & 7)
						== MapGeometry.dir4(sim.hero.pos, e.pos)
					):
						_hero_strike_if_near(sim, e, reach)
				26, 27:
					if (
						MapGeometry.distance(
							MapEnemyPlay.front_of(sim.hero.pos, sim.hero.dir), e.pos
						)
						<= 35
					):
						strike_enemy(sim, e)
				28, 29, 30:
					strike_enemy(sim, e)
			# every action also strikes what is in front, within the strike band
			if MapGeometry.in_strike_reach(sim.hero.pos, e.pos, sim.hero.dir, reach):
				strike_enemy(sim, e)
		elif MapGeometry.distance(sim.effect_pos, e.pos) <= 35:
			_hero_hits_enemy(sim, e, sim.effect_item)
			sim.sound(4)


static func _hero_strike_if_near(sim: MapSim, e: MapActor, reach: int) -> void:
	if MapGeometry.distance(sim.hero.pos, e.pos) <= reach:
		strike_enemy(sim, e)


## A strike of the hero lands: the damage, and what the skill does to the enemy.
static func strike_enemy(sim: MapSim, e: MapActor) -> void:
	if e.action > 5:
		return
	_hero_hits_enemy(sim, e, sim.hero.action)
	if sim.hero.combo > 1 and sim.hero.action < 12:
		e.ai_mode = 1  # the third strike of a combo knocks back
	match sim.hero.action:
		12:
			sim.hero.frame = 5
			e.ai_mode = 2
		14, 22:
			e.ai_mode = 2
		20:
			e.hit_fx_kind = sim.rng.below(2) + 1
			e.ai_mode = 0
		21:
			e.ai_mode = 5
		23:
			set_on_fire(sim, e)
		24:
			e.ai_mode = 5
			set_on_fire(sim, e)
		25, 27:
			e.ai_mode = 5
		26:
			pass
		29:
			set_on_fire(sim, e)
	if sim.hero.action >= 25 and sim.hero.action <= 27:
		e.hit_fx_kind = 2
		var f := MapEnemyPlay.front_of(sim.hero.pos, sim.hero.dir)
		e.dir = MapGeometry.dir8(e.pos, f)
		e.facing = e.dir
	sim.sound(16)


## A fire skill hits him (Ring of Fire, Fire Whirl, Serpent's Breath; a general's fire
## skills on the hero): the fire burns on him from this tick's picture on.
static func set_on_fire(sim: MapSim, a: MapActor) -> void:
	a.on_fire = true
	a.fire_frame = -1
	sim.sound(13)


## The damage of a hit: a strike (3..8), a skill (its level adds attack), or a scroll.
static func _hero_hits_enemy(sim: MapSim, e: MapActor, action: int) -> void:
	e.hit_fx_kind = 1
	if action > -1:
		e.dir = MapGeometry.dir8(e.pos, sim.hero.pos)
	else:
		e.dir = MapGeometry.dir8(e.pos, sim.effect_pos)
	e.facing = e.dir
	if action >= 3 and action <= 8:
		var dmg := sim.hero.attack + sim.hero.attack_buff - e.defense - e.defense_buff
		e.hp -= maxi(dmg, 1)
	elif action in [12, 13, 14] or (action >= 20 and action <= 30):
		var k := action - 12
		var dmg := (
			sim.hero.attack
			+ sim.hero.attack_buff
			+ sim.hero.attack * sim.skill_levels[k] / int(MapSim.table("skill_attack_div")[k])
			- e.defense
			- e.defense_buff
		)
		e.hp -= maxi(dmg, 1)
	elif action == -2:
		e.ai_mode = 2
		e.hp -= mini(sim.hero.level << 1, 50)
		sim.sound(4)
	elif action == -1:
		e.hp -= mini(sim.hero.level, 30)
		sim.sound(3)
	if e.hp < 1:
		e.hp = 0
		e.frame = 3
	else:
		e.frame = 0
	_show_target_info(sim, e)
	MapEnemyPlay.spark_at(e)
	e.action = 2
	if e.type < 200 and sim.rng.below(1000) < 150 and e.hp > 0:
		MapEnemyPlay.general_pick_skill(sim, e, true)


## The hero turns to the nearest enemy (closer than 50 px) as he strikes: only on normal (on
## hard the player aims by hand).
static func _turn_to_nearest(sim: MapSim) -> void:
	if sim.difficulty == 0:
		return
	var best := 50
	var found: MapActor = null
	for e in sim.enemies:
		var d := MapGeometry.distance(e.pos, sim.hero.pos)
		if best > d and e.hp > 0:
			best = d
			found = e
	if found != null:
		sim.hero.facing = MapGeometry.dir4(sim.hero.pos, found.pos)
		sim.hero.dir = sim.hero.facing
