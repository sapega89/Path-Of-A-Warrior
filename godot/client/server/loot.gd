extends RefCounted
## Loot of the online battles (pyport pow_server/loot.py): items of the single-player tables
## (data/items.json). One drop roll per foe beaten, the best item kept; equipment can come out
## Special (301..) or Rare (501..), which the single player does not drop. The client puts the
## item into the hero's backpack.

const Items := preload("res://scripts/core/items.gd")

const STORY_ONLY := [502]  # Silk Rushnyk: the reward of an ending, never a drop
## 0 soldier, 1 general, 2 boss
const DROP_CHANCE := [5, 10, 20]  # % that something drops
const EQUIP_CHANCE := [10, 30, 60]  # % of a drop that is gear (else a potion or a bomb, 1..11)
const TIER_LEVELS := [69, 44, 24, 9, 0]  # hero level above -> the row of TIER_ODDS
const TIER_ODDS := [[0, 0, 33, 77, 100], [5, 30, 55, 80, 100], [30, 60, 90, 100, 100],
	[40, 80, 100, 100, 100], [80, 100, 100, 100, 100]]
## the share of the gear drops that is Special / Rare instead of Normal
const SPECIAL_SHARE := 20
const RARE_SHARE := 2


## The item id a drop of `kind` gives a hero of `level`, or 0. Above level 69 the odds of
## levels 45..69, as the single player's drops.
static func sp_drop(rng: RandomNumberGenerator, level: int, kind: int) -> int:
	if rng.randi_range(0, 99) >= DROP_CHANCE[kind]:
		return 0
	if rng.randi_range(0, 99) >= EQUIP_CHANCE[kind]:
		return rng.randi_range(1, 11)
	var row := 0
	while row < TIER_LEVELS.size() - 1 and level <= TIER_LEVELS[row]:
		row += 1
	row = maxi(row, 1)
	var r := rng.randi_range(0, 99)
	var tier := 0
	while r >= TIER_ODDS[row][tier]:
		tier += 1
	return 101 + tier + 5 * rng.randi_range(0, 19)


## [id, required level] of the Special (table "treasures") or Rare things.
static func _table(name: String) -> Array:
	var out: Array = []
	var t: Dictionary = Items.data().get(name, {})
	for id in t:
		if not int(id) in STORY_ONLY:
			out.append([int(id), int(t[id].get("level", 0))])
	return out


## A Special / Rare thing the hero can use soon: required level up to level + reach, the
## closest more often.
static func _pick(rng: RandomNumberGenerator, things: Array, level: int, reach: int) -> int:
	var pool := things.filter(func(x): return x[1] <= level + reach)
	if pool.is_empty():
		var low: Array = things[0]
		for x in things:
			if x[1] < low[1]:
				low = x
		pool = [low]
	var weights: Array = pool.map(func(x): return 1 + maxi(0, 40 - absi(level - x[1])))
	var total := 0
	for w in weights:
		total += w
	var r := rng.randi_range(0, total - 1)
	for i in pool.size():
		r -= weights[i]
		if r < 0:
			return pool[i][0]
	return pool[-1][0]


## The thing of an id as the battle gives it, with its name: Normal gear gets 0..its range
## on its stat; 1..11 are the potions and bombs (the hero's quick slots).
static func thing(rng: RandomNumberGenerator, id: int) -> Dictionary:
	if id <= 11:
		var potion := Items.empty()
		potion.id = id
		potion.name = Items.POTION_NAMES[id - 1].strip_edges()
		return potion
	var item := Items.make(id)
	if id <= 300:
		var rec := Items.info(id)
		item[Items.GEAR_STATS[int(rec.stat)]] += rng.randi_range(0, int(rec.range))
	item.name = Items.name_of(id)
	return item


## The loot of one battle (kills: the kinds of the foes beaten, 0 soldier, 1 general, 2 boss),
## or {} for nothing.
static func roll(rng: RandomNumberGenerator, level: int, kills: Array) -> Dictionary:
	var best := 0
	for kind in kills:
		var got := sp_drop(rng, level, kind)
		if got > 100:
			var r := rng.randi_range(0, 99)
			if r < RARE_SHARE:
				got = _pick(rng, _table("rare"), level, 25)
			elif r < RARE_SHARE + SPECIAL_SHARE:
				got = _pick(rng, _table("treasures"), level, 15)
		best = maxi(best, got)
	return thing(rng, best) if best > 0 else {}
