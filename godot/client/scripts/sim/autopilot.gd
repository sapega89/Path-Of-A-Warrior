class_name Autopilot
extends RefCounted
## Auto-hunt on a mission's map (as pyport's autopilot.py; Tab, F or a pad's Back, or a click on
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
##   - it walks to the nearest living enemy, and around a wall when it stops moving or comes
##     no closer (each way around longer than the one before, to the other side); an enemy that
##     four ways around bring no closer (an archer up on a wall) it leaves alone in this room;
##   - a cleared room (or one where only such enemies are left): out through an open exit, to
##     a room not seen yet when it can.
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
const STUCK_TICKS := 4  # ticks without moving: go around
const NO_CLOSER_TICKS := 16  # ticks without coming closer to the target: go around
const DETOUR_TICKS := 8  # the first way around; the n-th is n times as long
const GIVE_UP_TRIES := 4  # ways around that bring it no closer: the target is out of reach
const CLOSER := 27  # px closer than where the ways around began: they worked
const DOWN := 0
const LEFT := 2
const UP := 4
const RIGHT := 6

var on := false
var manual := 0
var _last := Vector2i(-1, -1)
var _still := 0
var _detour := -1
var _detour_ticks := 0
var _target = null  # the enemy it walks to
var _closest := 0  # its nearest distance to the target so far
var _no_closer := 0  # ticks since it last came closer
var _tries := 0  # ways around the target in a row
var _try_from := 0  # the nearest distance when they began
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
func decide(sim: RefCounted) -> Dictionary:
	var out := {"held": -1, "fire": false, "hotkey": -1, "belt": -1}
	if not on or sim.banner != 0 or not sim.talk.is_empty() or sim.scrolling or sim.finished:
		return out
	if manual > 0:
		manual -= 1
		return out
	var h = sim.hero
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
	var hunt := _hunted(sim, foes)
	if hunt.is_empty():
		if not sim.exits_open():
			_out_of_reach.clear()  # no way out yet: it tries them again
		out.held = _to_exit(sim)
		return out
	var target = hunt[0]
	var dist := MapGeometry.distance(h.pos, target.pos)
	for e in hunt:
		var d := MapGeometry.distance(h.pos, e.pos)
		if d < dist:
			dist = d
			target = e
	var reach := int(MapSim.table("weapon_reach")[h.weapon_kind]) - 6
	key = _skill(sim, foes, target, dist, reach)
	if key >= 0 or dist <= reach:
		h.dir = MapGeometry.dir4(h.pos, target.pos)  # turns the hero
		h.facing = h.dir
		if key >= 0:
			out.hotkey = key
		else:
			out.fire = true
		return out
	out.held = _walk(sim, target)
	return out


## The enemies it goes for: the living ones, but those it left alone in this room.
func _hunted(sim: RefCounted, foes: Array) -> Array:
	if _hunt_cell != sim.cell:
		_hunt_cell = sim.cell
		_out_of_reach.clear()
		_target = null
	_out_of_reach = _out_of_reach.filter(func(e): return e in foes)
	return foes.filter(func(e): return not e in _out_of_reach)


func _walk(sim: RefCounted, target) -> int:
	var h = sim.hero
	_still = _still + 1 if h.pos == _last and h.action == 1 else 0
	_last = h.pos
	var dist := MapGeometry.distance(h.pos, target.pos)
	if target != _target:
		_target = target
		_closest = dist
		_no_closer = 0
		_tries = 0
	elif dist < _closest:
		_closest = dist
		_no_closer = 0
		if _tries > 0 and dist <= _try_from - CLOSER:
			_tries = 0
	else:
		_no_closer += 1
	if _detour_ticks > 0:
		_detour_ticks -= 1
		_no_closer = 0
		return _detour
	var want := MapGeometry.dir4(h.pos, target.pos)
	if _still < STUCK_TICKS and _no_closer < NO_CLOSER_TICKS:
		return want
	# a wall, or a corner it goes to and fro at: along it, toward the target's other axis first,
	# then to the other side
	_still = 0
	_no_closer = 0
	_tries += 1
	if _tries == 1:
		_try_from = _closest
	if _tries > GIVE_UP_TRIES:
		_out_of_reach.append(target)
		_target = null
		return -1
	var dx: int = target.pos.x - h.pos.x
	var dy: int = target.pos.y - h.pos.y
	if want == DOWN or want == UP:
		_detour = RIGHT if dx > 0 else LEFT
	else:
		_detour = DOWN if dy > 0 else UP
	if _tries % 2 == 0:
		_detour = (_detour + 4) & 7
	_detour_ticks = DETOUR_TICKS * _tries
	return _detour


## A belt slot to drink from, or -1.
func _potion(sim: RefCounted, foes: Array) -> int:
	var h = sim.hero
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
func _slots(sim: RefCounted) -> Array:
	var out: Array = []
	for k in sim.hotkeys.size():
		var s := int(sim.hotkeys[k])
		if s >= 12 and s <= 30 and int(sim.skill_levels[s - 12]) > 0:
			out.append([k, s])
	return out


func _castable(sim: RefCounted, kinds: Array) -> Array:
	var out: Array = []
	for ks in _slots(sim):
		if ks[1] in kinds and sim.skill_mp_need(ks[1]) <= sim.hero.mp:
			out.append(ks[1])
	return out


## The key of each skill on the keys (the first key holding it).
func _key_of(sim: RefCounted) -> Dictionary:
	var out := {}
	var slots := _slots(sim)
	slots.reverse()
	for ks in slots:
		out[ks[1]] = ks[0]
	return out


## Healing Herbs below 40 % HP, Living Water first below 25 %. A skill key or -1.
func _heal(sim: RefCounted) -> int:
	var h = sim.hero
	var pct: int = h.hp * 100 / maxi(1, h.max_hp)
	if pct >= 40:
		return -1
	var key_of := _key_of(sim)
	for s in [16, 15] if pct < 25 else [15, 16]:
		if key_of.has(s) and sim.skill_mp_need(s) <= h.mp:
			return key_of[s]
	return -1


## The room is clear and its exits open: walk out, to a room not seen yet when there is one.
func _to_exit(sim: RefCounted) -> int:
	if not sim.exits_open():
		return -1
	var cell: int = sim.cell
	_seen[cell] = true
	if _exit_cell != cell:
		_exit_cell = cell
		var exits: Array = sim.rooms.exits(cell)
		var open: Array = []
		var fresh: Array = []
		for b in 4:
			if int(exits[b]) != 0:
				open.append(b)
				if not _seen.has(sim.rooms.neighbour(cell, b + 1)):
					fresh.append(b)
		var pick: Array = fresh if not fresh.is_empty() else open
		_exit = -1 if pick.is_empty() else int(pick[sim.play_ticks % pick.size()])
	if _exit < 0:
		return -1
	if _detour_ticks > 0:
		_detour_ticks -= 1
		return _detour
	var h = sim.hero
	_still = _still + 1 if h.pos == _last and h.action == 1 else 0
	_last = h.pos
	var want: int = [DOWN, LEFT, UP, RIGHT][_exit]
	if _still >= STUCK_TICKS:
		_still = 0
		_detour = (want + 2 + 4 * (sim.play_ticks & 1)) & 7
		_detour_ticks = DETOUR_TICKS
		return _detour
	return want


## A skill key for the fight, or -1.
func _skill(sim: RefCounted, foes: Array, target, dist: int, reach: int) -> int:
	var h = sim.hero
	var key_of := _key_of(sim)
	if key_of.is_empty():
		return -1
	var heal_mp := 0
	for s in HEALS:
		if key_of.has(s):
			heal_mp = sim.skill_mp_need(s) if heal_mp == 0 else mini(heal_mp, sim.skill_mp_need(s))
	var usable := func(group: Array) -> Array:
		var out: Array = []
		for s in group:
			if (
				key_of.has(s)
				and sim.skill_mp_need(s) <= h.mp
				and h.mp - sim.skill_mp_need(s) >= heal_mp
			):
				out.append(s)
		out.sort_custom(func(a, b): return sim.skill_mp_need(a) > sim.skill_mp_need(b))
		return out
	var near := 0
	var general := false
	for e in foes:
		if MapGeometry.distance(h.pos, e.pos) <= 45:
			near += 1
		if e.type < 200:
			general = true
	if (foes.size() >= 3 or general) and h.attack_buff_ticks <= 0 and h.defense_buff_ticks <= 0:
		for s in [19, 17, 18]:
			if s in usable.call([s]):
				return key_of[s]
	if foes.size() >= 3:
		var u: Array = usable.call(WHOLE)
		if not u.is_empty():
			return key_of[u[0]]
	if near >= 2:
		var u: Array = usable.call(NEAR)
		if not u.is_empty():
			return key_of[u[0]]
	if dist > reach:
		var d := MapGeometry.dir4(h.pos, target.pos)
		var ax: int = h.pos.x + int(MapSim.table("front_dx")[d >> 1])
		var ay: int = h.pos.y + int(MapSim.table("front_dy")[d >> 1])
		if (
			(ax - target.pos.x) * (ax - target.pos.x) + (ay - target.pos.y) * (ay - target.pos.y)
			<= 35 * 35
		):
			var u: Array = usable.call(RANGED)
			if not u.is_empty():
				return key_of[u[0]]
		return -1
	var crowd := 0
	for e in foes:
		if MapGeometry.distance(h.pos, e.pos) <= reach:
			crowd += 1
	if (general and target.type < 200) or crowd >= 2 or h.mp * 100 >= h.max_mp * 80:
		var u: Array = usable.call(STRIKES)
		if not u.is_empty():
			return key_of[u[0]]
	return -1
