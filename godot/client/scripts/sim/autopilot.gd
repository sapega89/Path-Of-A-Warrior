class_name Autopilot
extends RefCounted
## Auto-hunt on a mission's map (Tab, F or a pad's Back, or a click on
## AUTO in the bottom-left corner). It plays like a player: every tick it may hold a direction
## and press one key (attack, a skill key, a belt slot), so the game's rules stay the same:
##   - potions: an HP potion below 30 % HP when no heal skill can be cast, an MP potion when the
##     MP is too low for any skill while enemies are around;
##   - heal (Medium / Living Water) below 40 % HP; the MP of a heal is kept for it otherwise;
##   - a soul when no aura is up and the fight is big (3+ enemies, or a general);
##   - whole-room skills on 3+ enemies, the near ones on 2+ within 45 px;
##   - a ranged skill when the target stands about 60 px ahead, out of the sword's reach;
##   - a strike skill on a general, on 2+ enemies in reach or with the MP nearly full, else the
##     attack combo;
##   - it goes for the nearest living enemy within the sword's reach, else for the one fewest
##     steps away, by the shortest way over the free cells of the room (RoomPath), or, when
##     there is none, through things to break, which it breaks on the way; an enemy it has no
##     way to (an archer up on a wall), or comes no nearer to for a while, it leaves alone in
##     this room till it comes within the sword's reach;
##   - a cleared room (or one where only such enemies are left): out through an open exit by
##     the shortest way, to a room not seen yet when it can.
## Talks, banners and the pause menu stay the player's; any key of the player hands off for a
## moment.

const HEALS := [15, 16]
const WHOLE := [28, 29, 30]
const NEAR := [23, 24, 25]
const RANGED := [26, 27]
const STRIKES := [12, 13, 14, 20, 21, 22]
const HP_POTIONS := [1, 2, 3, 7, 8, 9]
const MP_POTIONS := [4, 5, 6, 7, 8, 9]
const MANUAL_PAUSE := 12  # ticks it waits after a key of the player
const GIVE_UP_TICKS := 64  # ticks without a step nearer the target: it is out of reach
const THROUGH_THINGS := 49  # steps more that a way through things to break counts for

var on := false
var manual := 0
var _target: MapActor = null  # the enemy it walks to
var _closest := 0  # the fewest steps it has been from the target
var _no_closer := 0  # ticks since it last came a step nearer
var _out_of_reach: Array = []  # the enemies of this room it leaves alone
var _hunt_cell := -1  # the room _out_of_reach belongs to
var _seen := {}
var _exit_cell := -1
var _exit := -1


func toggle() -> void:
	on = not on


## The player pressed a key: hands off for a moment.
func player_key() -> void:
	manual = MANUAL_PAUSE


## This tick's input: {held: direction or -1, fire, hotkey (0..4 or -1), belt (0..4 or -1)}.
func decide(sim: MapSim) -> Dictionary:
	var out := {"held": -1, "fire": false, "hotkey": -1, "belt": -1}
	if not on or sim.banner != 0 or not sim.talk.is_empty() or sim.scrolling or sim.finished:
		return out
	if manual > 0:
		manual -= 1
		return out
	var h := sim.hero
	if h.action >= 2 or sim.effect_item != 0:  # busy: a strike, a skill, hurt, a potion
		return out
	var foes: Array = []
	for e in sim.enemies:
		if e.hp > 0:
			foes.append(e)
	var belt := _potion(sim, foes)
	if belt >= 0:
		out.belt = belt
		return out
	var key := _heal(sim)
	if key >= 0:
		out.hotkey = key
		return out
	var reach := int(MapSim.table("weapon_reach")[h.weapon_kind]) - 6
	var target := _nearest(sim, _hunted(sim, foes, reach), reach)
	if target == null:
		if not sim.exits_open():
			_out_of_reach.clear()  # no way out yet: it tries them again
		_to_exit(sim, out)
		return out
	var dist := MapGeometry.distance(h.pos, target.pos)
	key = _skill(sim, foes, target, dist, reach)
	if key >= 0 or dist <= reach:
		_target = null  # a fight: its way to the next target starts afresh
		h.dir = MapGeometry.dir4(h.pos, target.pos)  # turns the hero
		h.facing = h.dir
		if key >= 0:
			out.hotkey = key
		else:
			out.fire = true
		return out
	_walk(sim, target, out)
	return out


## The enemies it goes for: the living ones, but those it left alone in this room unless they
## come within the sword's reach.
func _hunted(sim: MapSim, foes: Array, reach: int) -> Array:
	if _hunt_cell != sim.cell:
		_hunt_cell = sim.cell
		_out_of_reach.clear()
		_target = null
	_out_of_reach = _out_of_reach.filter(func(e): return e in foes)
	var h := sim.hero
	return foes.filter(
		func(e: MapActor) -> bool:
			return not e in _out_of_reach or MapGeometry.distance(h.pos, e.pos) <= reach
	)


## The enemy it goes for: the nearest within the sword's reach, else the one fewest steps away
## (the nearest of those); one it has no way to it leaves alone in this room. Null: none.
func _nearest(sim: MapSim, hunt: Array, reach: int) -> MapActor:
	var h := sim.hero
	var from: Array[Vector2i] = [RoomPath.cell_of(sim, h.pos)]
	var free := RoomPath.steps_from(sim, from)
	var through := RoomPath.steps_from(sim, from, true)
	var best: MapActor = null
	var best_key := Vector2i.ZERO
	for e: MapActor in hunt:
		var dist := MapGeometry.distance(h.pos, e.pos)
		var away := 0 if dist <= reach else _away(free, through, RoomPath.cell_of(sim, e.pos))
		if away < 0:
			_out_of_reach.append(e)
			continue
		if best == null or Vector2i(away, dist) < best_key:
			best = e
			best_key = Vector2i(away, dist)
	return best


## The steps to cell `c` by the free cells (steps `free`), else THROUGH_THINGS more by the way
## through things to break (`through`); -1 no way.
static func _away(free: Dictionary, through: Dictionary, c: Vector2i) -> int:
	var away := RoomPath.steps_to(free, c)
	if away < 0:
		away = RoomPath.steps_to(through, c)
		away += THROUGH_THINGS if away >= 0 else 0
	return away


## A step nearer the target by the way through the room, or straight at it from its cell or the
## one next to it; a target it comes no nearer to for GIVE_UP_TICKS it leaves alone in this room.
func _walk(sim: MapSim, target: MapActor, out: Dictionary) -> void:
	var h := sim.hero
	var goal: Array[Vector2i] = [RoomPath.cell_of(sim, target.pos)]
	var at := RoomPath.cell_of(sim, h.pos)
	var steps := RoomPath.steps_from(sim, goal)
	if not steps.has(at):
		steps = RoomPath.steps_from(sim, goal, true)
	var left := int(steps.get(at, -1))
	if target != _target or left < _closest:
		_target = target
		_closest = left
		_no_closer = 0
	else:
		_no_closer += 1
	if _no_closer >= GIVE_UP_TICKS:
		_out_of_reach.append(target)
		_target = null
	elif not _step(sim, steps, target.pos - h.pos, out):
		out.held = MapGeometry.dir4(h.pos, target.pos)
	elif out.fire:
		_no_closer = 0  # breaking a thing in the way


## A step on the way `steps` leads (RoomPath.steps_from its goal), the one most along `toward`
## of those as short; false: the hero stands on the goal or has no way from here.
func _step(sim: MapSim, steps: Dictionary, toward: Vector2i, out: Dictionary) -> bool:
	var d := RoomPath.next_step(sim, steps, toward)
	if d < 0:
		return false
	_step_into(sim, d, out)
	return true


## Into the next cell towards `direction` (0, 2, 4, 6), or a blow at the thing to break on it.
func _step_into(sim: MapSim, direction: int, out: Dictionary) -> void:
	var h := sim.hero
	var at := RoomPath.cell_of(sim, h.pos)
	var next := at + RoomPath.STEPS[direction >> 1]
	for b: MapBreakable in sim.breakables:
		if b.tile == next and b.active and b.hp > 0:
			h.dir = MapGeometry.dir4(h.pos, b.pos)  # turns the hero
			h.facing = h.dir
			out.fire = true
			return
	out.held = RoomPath.step_to(sim, at, direction)


## A belt slot to drink from, or -1.
func _potion(sim: MapSim, foes: Array) -> int:
	var h := sim.hero
	var hp_low: bool = h.hp * 100 < h.max_hp * 30
	if hp_low and not _castable(sim, HEALS).is_empty():
		hp_low = false  # the heal skill comes first
	var skills: Array = []
	for s in sim.hotkeys:
		if int(s) >= 12 and int(s) <= 30:
			skills.append(int(s))
	var mp_low: bool = (
		not foes.is_empty()
		and h.max_mp > 0
		and not skills.is_empty()
		and _castable(sim, skills).is_empty()
	)
	for i in 5:
		var slot: Array = sim.quick_slots[i]
		if int(slot[1]) < 1:
			continue
		if hp_low and int(slot[0]) in HP_POTIONS:
			return i
		if mp_low and int(slot[0]) in MP_POTIONS and h.mp * 100 < h.max_mp * 50:
			return i
	return -1


## [key, skill] of the learned skills on the keys.
func _slots(sim: MapSim) -> Array:
	var out: Array = []
	for k in sim.hotkeys.size():
		var s := int(sim.hotkeys[k])
		if s >= 12 and s <= 30 and int(sim.skill_levels[s - 12]) > 0:
			out.append([k, s])
	return out


func _castable(sim: MapSim, kinds: Array) -> Array:
	var out: Array = []
	for ks in _slots(sim):
		if ks[1] in kinds and sim.skill_mp_need(ks[1]) <= sim.hero.mp:
			out.append(ks[1])
	return out


## The key of each skill on the keys (the first key holding it).
func _key_of(sim: MapSim) -> Dictionary:
	var out := {}
	var slots := _slots(sim)
	slots.reverse()
	for ks in slots:
		out[ks[1]] = ks[0]
	return out


## Healing Herbs below 40 % HP, Living Water first below 25 %. A skill key or -1.
func _heal(sim: MapSim) -> int:
	var h := sim.hero
	var pct: int = h.hp * 100 / maxi(1, h.max_hp)
	if pct >= 40:
		return -1
	var key_of := _key_of(sim)
	for s in [16, 15] if pct < 25 else [15, 16]:
		if key_of.has(s) and sim.skill_mp_need(s) <= h.mp:
			return key_of[s]
	return -1


## The room is clear and its exits open: walk out by the shortest way (through things to
## break when there is no other), to a room not seen yet when there is one.
func _to_exit(sim: MapSim, out: Dictionary) -> void:
	if not sim.exits_open():
		return
	_seen[sim.cell] = true
	if _exit_cell != sim.cell:
		_exit_cell = sim.cell
		_exit = _pick_exit(sim)
	if _exit < 0:
		return
	var at := RoomPath.cell_of(sim, sim.hero.pos)
	var steps := RoomPath.steps_from(sim, RoomPath.ways_out(sim, _exit))
	if not steps.has(at):
		steps = RoomPath.steps_from(sim, RoomPath.ways_out(sim, _exit, true), true)
	if int(steps.get(at, -1)) == 0:
		_step_into(sim, _exit * 2, out)
	elif not _step(sim, steps, RoomPath.STEPS[_exit], out):
		out.held = _exit * 2


## The exit it walks out of: one it has a way to and to a room not seen yet, else one it has a
## way to (through things to break too), else any open one; -1 none.
func _pick_exit(sim: MapSim) -> int:
	var exits: Array = sim.rooms.exits(sim.cell)
	var from: Array[Vector2i] = [RoomPath.cell_of(sim, sim.hero.pos)]
	var steps := RoomPath.steps_from(sim, from, true)
	var fresh: Array[int] = []
	var ways: Array[int] = []
	var open: Array[int] = []
	for b in 4:
		if int(exits[b]) == 0:
			continue
		open.append(b)
		if RoomPath.ways_out(sim, b, true).any(func(c: Vector2i) -> bool: return steps.has(c)):
			ways.append(b)
			if not _seen.has(sim.rooms.neighbour(sim.cell, b + 1)):
				fresh.append(b)
	for pick: Array[int] in [fresh, ways, open]:
		if not pick.is_empty():
			return pick[sim.play_ticks % pick.size()]
	return -1


## A skill key for the fight, or -1.
func _skill(sim: MapSim, foes: Array, target: MapActor, dist: int, reach: int) -> int:
	var h := sim.hero
	var key_of := _key_of(sim)
	if key_of.is_empty():
		return -1
	var heal_mp := _heal_mp(sim, key_of)
	var near := 0
	var general := false
	for e in foes:
		if MapGeometry.distance(h.pos, e.pos) <= 45:
			near += 1
		if e.type < 200:
			general = true
	var picks: Array = []
	if (foes.size() >= 3 or general) and h.attack_buff_ticks <= 0 and h.defense_buff_ticks <= 0:
		for s in [19, 17, 18]:
			picks.append_array(_usable(sim, key_of, heal_mp, [s]))
	if foes.size() >= 3:
		picks.append_array(_usable(sim, key_of, heal_mp, WHOLE))
	if near >= 2:
		picks.append_array(_usable(sim, key_of, heal_mp, NEAR))
	if not picks.is_empty():
		return key_of[picks[0]]
	if dist > reach:
		if _in_ranged_reach(h, target):
			var u := _usable(sim, key_of, heal_mp, RANGED)
			if not u.is_empty():
				return key_of[u[0]]
		return -1
	var crowd := 0
	for e in foes:
		if MapGeometry.distance(h.pos, e.pos) <= reach:
			crowd += 1
	if (general and target.type < 200) or crowd >= 2 or h.mp * 100 >= h.max_mp * 80:
		var u := _usable(sim, key_of, heal_mp, STRIKES)
		if not u.is_empty():
			return key_of[u[0]]
	return -1


## The MP the cheapest heal on a key needs (kept for it), 0 with none.
func _heal_mp(sim: MapSim, key_of: Dictionary) -> int:
	var heal_mp := 0
	for s in HEALS:
		if key_of.has(s):
			heal_mp = sim.skill_mp_need(s) if heal_mp == 0 else mini(heal_mp, sim.skill_mp_need(s))
	return heal_mp


## The skills of `group` on a key that the hero's MP pays for, the MP of a heal kept, the
## dearest first.
func _usable(sim: MapSim, key_of: Dictionary, heal_mp: int, group: Array) -> Array:
	var mp := sim.hero.mp
	var out: Array = []
	for s in group:
		var need := sim.skill_mp_need(s)
		if key_of.has(s) and need <= mp and mp - need >= heal_mp:
			out.append(s)
	out.sort_custom(
		func(a: int, b: int) -> bool: return sim.skill_mp_need(a) > sim.skill_mp_need(b)
	)
	return out


## Whether the target stands within 35 px of the point in front of the hero, where a ranged
## skill lands.
func _in_ranged_reach(h: MapActor, target: MapActor) -> bool:
	var d := MapGeometry.dir4(h.pos, target.pos)
	var ax: int = h.pos.x + int(MapSim.table("front_dx")[d >> 1])
	var ay: int = h.pos.y + int(MapSim.table("front_dy")[d >> 1])
	return (
		(ax - target.pos.x) * (ax - target.pos.x) + (ay - target.pos.y) * (ay - target.pos.y)
		<= 35 * 35
	)
