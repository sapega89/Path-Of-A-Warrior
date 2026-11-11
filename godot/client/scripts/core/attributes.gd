class_name Attributes
extends RefCounted
## The hero's attributes: the base set of each face, the stat points spent over it, and the
## reset of the Attributes page (the base stats back to the face's set and the points spent
## free again, paid with gold by level or with an elixir).

## What one stat point adds: HP, MP, attack, defence.
const POINT_GAINS := [5, 3, 1, 1]
## The four heroes (the faces) start with their own HP, MP, attack and defence. Every set is
## worth the same stat points (POINT_GAINS), so no hero is stronger, only different. Face 0
## has the numbers every hero had in the original.
const HERO_BASES := [[30, 10, 5, 4], [40, 7, 3, 5], [25, 16, 4, 4], [25, 10, 7, 3]]
## The gold a reset costs per hero level.
const RESET_GOLD_PER_LEVEL := 100
## The elixirs that pay for a reset: St John's Wort Tincture, Cornflower Tincture, Rapids /
## Forest Remedy.
const RESET_ELIXIRS := [434, 435, 436, 437]


## The face's base stats: [HP, MP, attack, defence].
static func hero_base(face: int) -> Array:
	return HERO_BASES[face & 3]


## "HP30 MP10 ATK5 DEF4": a face's base stats.
static func stats_line(face: int) -> String:
	return "HP%d MP%d ATK%d DEF%d" % hero_base(face)


## The stat points in the base stats over the face's set (the elixirs drunk too).
static func spent_points(hero: Profile) -> int:
	var b := hero_base(hero.head)
	var own := [hero.base_hp, hero.base_mp, hero.base_attack, hero.base_defense]
	var n := 0
	for i in 4:
		n += (int(own[i]) - int(b[i])) / int(POINT_GAINS[i])
	return maxi(0, n)


static func reset_gold(hero: Profile) -> int:
	return RESET_GOLD_PER_LEVEL * maxi(1, hero.level)


## The backpack place of the first elixir that pays for a reset, or -1.
static func reset_elixir_slot(hero: Profile) -> int:
	for i in hero.backpack.size():
		if int(hero.backpack[i].id) in RESET_ELIXIRS:
			return i
	return -1


## Resets the attributes, paid with gold (by_item false) or an elixir. Returns "" when done,
## else why not: "nothing", "gold", "item".
static func reset(hero: Profile, by_item: bool) -> String:
	var n := spent_points(hero)
	if n == 0:
		return "nothing"
	if by_item:
		var i := reset_elixir_slot(hero)
		if i < 0:
			return "item"
		hero.backpack[i] = Items.empty()
	else:
		if hero.gold < reset_gold(hero):
			return "gold"
		hero.gold -= reset_gold(hero)
	hero.set_head(hero.head)
	hero.stat_points += n
	return ""
