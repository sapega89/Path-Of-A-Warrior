class_name MapLoot
extends RefCounted
## The breakable objects of a room and what lies on the floor: barrels and crates under the sword,
## the gold and items they and the enemies drop, picking them up.
## Static functions over the state of a MapSim (MapSim.tick() runs them).


## The objects of the room's 9x9-tile view.
static func find_breakables(sim: MapSim) -> void:
	sim.breakables.clear()
	var o := MapRoomPlay.room_origin(sim)
	for y in range(o.y * 7, mini(o.y * 7 + 9, sim.h)):
		for x in range(o.x * 7, mini(o.x * 7 + 9, sim.w)):
			var kind := int(sim.objects[y * sim.w + x])
			if kind == 0:
				continue
			var b := MapBreakable.new()
			b.tile = Vector2i(x, y)
			b.pos = Vector2i(x * 27 + 12, y * 27 + 20)
			b.kind = kind
			b.hp = 41 if kind in [101, 113] else 21
			sim.breakables.append(b)


static func hero_hits_breakables(sim: MapSim) -> void:
	var reach := int(MapSim.table("weapon_reach")[sim.hero.weapon_kind])
	for b in sim.breakables:
		if not (b.active and b.hp > 0):
			continue
		match sim.hero.action:
			13:
				var side := sim.hero.dir >> 1
				if MapGeometry.boxes_touch(
					sim.hero.pos.x + int(MapSim.table("hit_box_x")[side]),
					sim.hero.pos.y + int(MapSim.table("hit_box_y")[side]),
					int(MapSim.table("hit_box_w")[side]),
					int(MapSim.table("hit_box_h")[side]),
					b.pos.x - 8,
					b.pos.y - 8,
					18,
					18
				):
					hit_breakable(sim, b)
			22:
				if (
					MapGeometry.is_in_front(sim.hero.pos, b.pos, sim.hero.dir)
					and MapGeometry.distance(sim.hero.pos, b.pos) <= reach
				):
					hit_breakable(sim, b)
			23, 24:
				if MapGeometry.distance(sim.hero.pos, b.pos) <= 45:
					hit_breakable(sim, b)
			25:
				if (
					(
						((sim.hero.dir + (sim.hero.frame >> 1 << 1)) & 7)
						== MapGeometry.dir4(sim.hero.pos, b.pos)
					)
					and MapGeometry.distance(sim.hero.pos, b.pos) <= reach
				):
					hit_breakable(sim, b)
			26, 27:
				if (
					MapGeometry.distance(MapEnemyPlay.front_of(sim.hero.pos, sim.hero.dir), b.pos)
					<= 35
				):
					hit_breakable(sim, b)
			28, 29, 30:
				hit_breakable(sim, b)
			_:
				if MapGeometry.in_strike_reach(sim.hero.pos, b.pos, sim.hero.dir, reach):
					hit_breakable(sim, b)


static func hit_breakable(sim: MapSim, b: MapBreakable) -> void:
	b.hp = b.hp - sim.hero.attack + sim.hero.attack_buff
	b.break_frame = 2
	sim.sound(3)
	if b.hp < 1:
		b.break_ticks = 12
		sim.objects[b.tile.y * sim.w + b.tile.x] = 0  # the cell is free from now on


## A broken object blinks for 12 ticks, then is gone and may leave something behind.
static func tick_broken(sim: MapSim) -> void:
	for b in sim.breakables:
		if b.active and b.break_ticks != 0:
			b.break_ticks -= 1
			if b.break_ticks == 0:
				drop_item(sim, 3, b.pos)
				b.active = false


## The object shows this tick (it blinks while breaking).
static func breakable_shown(b: MapBreakable) -> bool:
	return b.active and (b.break_ticks == 0 or (b.break_ticks & 2) != 0)


## Something may drop at p: kind 0 soldier, 1 general, 2 the mission's general, 3 object.
## Only in the part of the room the game's view checks (its upper left), as the original.
static func drop_item(sim: MapSim, kind: int, p: Vector2i) -> void:
	var o := MapRoomPlay.room_origin(sim)
	var cam := Vector2i(o.x * 7 * 27 + 1, o.y * 7 * 27)
	if p.y <= cam.y + 27 or p.y >= cam.y + 162 or p.x <= cam.x + 27 or p.x >= cam.x + 162:
		return
	var item := random_drop(sim, kind)
	if item == 0 or (int(sim.flags[(p.y / 27) * sim.w + p.x / 27]) & 1) != 0:
		return
	var live := 0
	for d in sim.drops:
		if d.item != 0:
			live += 1
	if live > 9:
		return
	var d := MapDrop.new()
	d.item = item
	d.pos = p
	sim.drops.append(d)


static func random_drop(sim: MapSim, kind: int) -> int:
	const DROP_ODDS := [5, 10, 20, 5, 100]
	const POTION_ODDS := [10, 30, 60, 1, 100]
	const TIER_MIN_LEVEL := [69, 44, 24, 9, 0]
	const TIER_ODDS := [
		[0, 0, 33, 77, 100],
		[5, 30, 55, 80, 100],
		[30, 60, 90, 100, 100],
		[40, 80, 100, 100, 100],
		[80, 100, 100, 100, 100]
	]
	if sim.rng.below(100) < DROP_ODDS[kind]:
		var i := sim.rng.below(100)
		if i < POTION_ODDS[kind]:
			for b in range(1, 5):  # above Lv69 the odds of Lv45-69
				if sim.hero.level > TIER_MIN_LEVEL[b]:
					i = sim.rng.below(100)
					for tier in 5:
						if i < TIER_ODDS[b][tier]:
							return 101 + tier + 5 * sim.rng.below(20)
		else:
			return sim.rng.below(11) + 1
	elif sim.rng.below(100) < 25:
		return 10020 + (sim.difficulty ^ 1) * 20
	return 0


static func pick_up_drops(sim: MapSim) -> void:
	for d in sim.drops.duplicate():
		if d.item != 0 and MapGeometry.distance(sim.hero.pos, d.pos) < 20:
			if d.item > 10000:
				sim.gold += d.item - 10000
			elif d.item < 100:
				if not MapHeroPlay.add_quick_item(sim, d.item):
					d.ticks -= 1
					continue  # no room: it stays on the floor
			else:
				if sim.free_places < 1:
					d.ticks -= 1
					continue  # no place in the Inventory: it stays on the floor
				sim.items.append(d.item)
				sim.free_places -= 1
				sim.acquired = d.item
				sim.show_banner(MapSim.BANNER_ACQUIRED)
			d.item = 0
			sim.hero_glows = true
		d.ticks -= 1
		if d.ticks < 1 or d.item == 0:
			sim.drops.erase(d)
