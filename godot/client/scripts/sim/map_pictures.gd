class_name MapPictures
extends RefCounted
## What the screen draws of the map's effects: the scrolls' blasts, the generals' skills, fires,
## auras, hit sparks and the trails of the strikes.
## Static functions over the state of a MapSim (MapSim.tick() runs them).

## MP of skill 12..30 at level 1, and per level above.
## The three flames of a fire scroll around its point.
const FIRE_SHIFT := [Vector2i(3, -6), Vector2i(-10, 0), Vector2i(10, 5)]


## A whirling swing turns its trail round with the frames.
static func _trail_picture(dir: int, whirl: bool, frame: int, step: int) -> int:
	var i := (dir + (frame >> 1 << 1)) & 7 if whirl else dir
	return (i >> 1) * 3 + step


## The fires burning on the hero and the enemies: ["fire", picture 0..5, where he stands].
static func fires(sim: MapSim) -> Array:
	var out: Array = []
	for a in [sim.hero] + sim.enemies:
		if a.on_fire and a.fire_frame >= 0:
			out.append(["fire", a.fire_frame, a.pos])
	return out


## The auras of buffs: on the hero while he glows, on a general while a buff of his lasts. A
## glowing ring on the ground behind him (pictures 0-2, the 4th value true: behind) and the
## light rising in front of him (3-5), the next picture each tick.
static func auras(sim: MapSim) -> Array:
	var out: Array = []
	var who: Array = [sim.hero] if sim.hero_glows else []
	for e in sim.enemies:
		if (
			e.type < 200
			and (e.attack_buff_ticks > 0 or e.defense_buff_ticks > 0)
			and MapAnims.enemy_sprite_frame(e) < 180
		):
			who.append(e)
	for a in who:
		var at: Vector2i = a.pos + Vector2i(0, 3)
		out.append(["aura", sim.ticks % 3, at, true])
		out.append(["aura", 3 + sim.ticks % 3, at])
	return out


## The hit sparks to draw: [frame, position]. An enemy's pair of pictures is chosen by the
## hit (frames 0-1 or 2-3); the hero's are always the first pair.
static func sparks(sim: MapSim) -> Array:
	var out: Array = []
	if sim.hero.hit_fx_kind != 0 and sim.hero.hit_fx_frame >= 0:
		out.append([sim.hero.hit_fx_frame, sim.hero.hit_fx_pos])
	for e in sim.enemies:
		if e.hit_fx_kind != 0 and e.hit_fx_frame >= 0:
			out.append([e.hit_fx_frame + ((e.hit_fx_kind - 1) << 1), e.hit_fx_pos])
	return out


## The effects to draw now: [sheet, frame, point in map pixels] (sheets fx_<name>.png). The
## hero's skill shows its effect on him (the big skills 28-30 over the middle of the room),
## a potion or scroll shows where it is in use, a general's skill on the general.
static func effects(sim: MapSim) -> Array:
	var out: Array = []
	var a := sim.hero.action
	var f := sim.hero.frame
	var p := sim.hero.pos
	match a:
		2:
			out.append(["slash", sim.hero.dir + (f & 1), p])
		12:
			if f > 2 and f < 6:
				out.append(["slash", sim.hero.dir + (f & 1), p])
		13:
			if f > 4 and f < 8:
				out.append(["slash", sim.hero.dir + (f & 1), p])
		14:
			if f > 0 and f < 9:
				out.append(["slash", sim.hero.dir + (f & 1), p])
		15:
			if f > 3:
				out.append(["heal", f - 4, p])
		19:
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
				out.append(["blast", 1, MapEnemyPlay.front_of(p, sim.hero.shown_dir)])
			elif f > 1 and f < 9:
				out.append(["wave", f - 2 + (sim.hero.dir >> 1) * 7, p])
		28:
			if f > 3 and f < 22:
				if f > 9:
					for i in 3:
						out.append(["storm", (f - 10) * 3 + 6 + i, MapRoomPlay.room_middle(sim)])
				else:
					out.append(["storm", f - 4, MapRoomPlay.room_middle(sim)])
		29:
			if f > 6 and f < 22:
				out.append(["quake", f - 7, MapRoomPlay.room_middle(sim)])
		30:
			if f > 3 and f < 9:
				for i in 5:
					out.append(["rain", (f - 4) * 5 + i, MapRoomPlay.room_middle(sim)])
			elif f > 12 and f < 15:
				for i in 3:
					out.append(["blast", (f - 13) * 5 + 2 + i, MapRoomPlay.room_middle(sim)])
	skill_effects(a, f, p, sim.hero.dir, out)
	match sim.effect_item:
		0:
			pass
		-2:
			out.append(["blast", sim.effect_step, sim.effect_pos])
		-1:
			for i in 3:
				out.append(["fire", sim.effect_step, sim.effect_pos + FIRE_SHIFT[i]])
		10, 11:
			if sim.effect_step > 0:
				out.append(["scroll", sim.effect_step - 1 + (sim.effect_dir << 2), sim.effect_pos])
		_:
			out.append(["buff", sim.effect_step + 4, sim.effect_pos])
	for e in sim.enemies:
		if e.type < 200:
			_general_effects(e, out)
	return out


## The pictures of a general's skill (his actions 6..21), as the hero's: the same sheets.
static func _general_effects(e: MapActor, out: Array) -> void:
	var f := e.frame
	var p := e.pos
	match e.action:
		6:
			if f > 2 and f < 6:
				out.append(["slash", e.dir + (f & 1), p])
		7:
			if f > 4 and f < 8:
				out.append(["slash", e.dir + (f & 1), p])
		8:
			if f > 0 and f < 9:
				out.append(["slash", e.dir + (f & 1), p])
		9:
			if f > 3:
				out.append(["heal", f - 4, p])
		13:
			if f > 3 and f < 10:
				out.append(["buff", f - 4, p])
		15:
			if f == 5 or f == 6:
				out.append(["whirl", f - 5, p])
		16:
			if f > 1 and f < 6:
				out.append(["slash", f & 1, p])
		17:
			if f == 5 or f == 6:
				out.append(["slash", f - 5, p])
		18:
			if f == 5:
				out.append(["burst", 0, p + MapSim.BURST_FIRST_SHIFT])
			elif f == 6:
				out.append(["burst", 1, p])
		20, 21:
			if e.action == 21 and f == 9:
				out.append(["blast", 1, MapEnemyPlay.front_of(p, e.dir)])
			elif f > 1 and f < 9:
				out.append(["wave", f - 2 + (e.dir >> 1) * 7, p])
	if e.action >= 6 and e.action <= 21:
		skill_effects(e.action + 6, f, p, e.dir, out)


## The skills' own effects (SkillEffects), the hero's and a general's alike: the skill 12..30,
## its frame f, and where the one using it stands and which way he faces.
static func skill_effects(skill: int, f: int, p: Vector2i, dir: int, out: Array) -> void:
	match skill:
		12:
			if f > 1 and f < 6:
				out.append(["whirlwind", dir * 4 + f - 2, p])
		13:
			if f > 4 and f < 8:
				out.append(["smash", dir * 3 + f - 5, p])
		14:
			if f > 0 and f < 9:
				out.append(["thrust", dir * 8 + f - 1, p])
		16:
			if f > 3 and f < 13:
				out.append(["spring", f - 4, p])
		17:
			if f > 3 and f < 10:
				out.append(["fury", f - 4, p])
		18:
			if f > 3 and f < 10:
				out.append(["charm", f - 4, p])
		20:
			out.append(["surge", dir * 4 + f % 4, p])
		22:
			if f > 1 and f < 8:
				out.append(["flood", dir * 6 + f - 2, p])
		23:
			if f > 3 and f < 10:
				out.append(["fire_ring", f - 4, p])
		24:
			if f > 0 and f < 7:
				out.append(["fire_whirl", f - 1, p])
		25:
			if f < 8:
				out.append(["blaze", f, p])


## The weapon trails to draw: ["trail", picture, position]. The picture is the direction
## (4 of them) times 3 steps. pick gives the steps that are chosen at random each time the
## trail is drawn (a swing that whirls, a general's strike).
static func trails(sim: MapSim, pick: RandomNumberGenerator) -> Array:
	var out: Array = []
	var step := hero_trail_step(sim, pick)
	if step > -1:
		out.append(
			[
				"trail",
				_trail_picture(sim.hero.dir, sim.hero.action == 25, sim.hero.frame, step),
				sim.hero.pos
			]
		)
	for e in sim.enemies:
		if e.type >= 200:
			continue
		step = general_trail_step(e, pick)
		if step > -1:
			out.append(["trail", _trail_picture(e.dir, e.action == 19, e.frame, step), e.pos])
	return out


## The step of the hero's weapon trail now, or -1 for none.
static func hero_trail_step(sim: MapSim, _pick: RandomNumberGenerator = null) -> int:
	var a := sim.hero.action
	var f := sim.hero.frame
	if a < 12:
		var sf := MapAnims.hero_sprite_frame(sim)
		if sf > 11 and sf < 36 and (sf & 1) != 0:
			return ((sf - 12) & 0xFFFE) % 6 >> 1
		return -1
	match a:
		12:
			if f > 2 and f < 6:
				return 1
		13:
			if f > 4 and f < 8:
				return 1
		14:
			if f > 0 and f < 9 and (f & 1) == 0:
				return 1
		20:
			if (f & 1) != 0:
				return sim.hero.combo
		21:
			if f == 5:
				return 2
		22:
			if f == 6:
				return 2
		25:
			if (f & 1) != 0:
				return 2
	return -1


## The step of a general's weapon trail now, or -1 for none.
static func general_trail_step(e: MapActor, pick: RandomNumberGenerator) -> int:
	var f := e.frame
	match e.action:
		6:
			if f > 2 and f < 6:
				return 1
		7:
			if f > 4 and f < 8:
				return 1
		8:
			if f in [2, 4, 6, 8]:
				return 1
		14:
			if (f & 1) == 0:
				return pick.randi_range(0, 2)
		15:
			if f == 5:
				return 2
		16:
			if f == 6:
				return 2
		19:
			if (f & 1) != 0:
				return 2
		_:
			if e.action < 6:
				var sf := MapAnims.enemy_sprite_frame(e)
				if sf > 8 and sf < 16 and (sf & 1) != 0:
					return pick.randi_range(0, 2)
	return -1
