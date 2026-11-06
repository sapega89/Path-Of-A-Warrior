extends RefCounted
## The hero between missions: level, exp, gold, stats, skills, quick slots, the friendship of
## the generals and the missions done. Kept in user://hero.json. A mission starts from it
## (apply_to) and gives it back what happened (take_from): the gold and potions picked up and
## used, the friendship of the talks and, when won, the mission's gold and exp.

const PATH := "user://hero.json"
const CAMPAIGN_PATH := "res://data/campaign.json"
## A new hero: HP, MP, attack, defence, and the free stat points.
const BASE_HP := 30
const BASE_MP := 10
const BASE_ATTACK := 5
const BASE_DEFENSE := 4
const START_POINTS := 5
const POINTS_PER_LEVEL := 3
## The weapon a new hero holds: the Iron Claymore (a long sword, attack +1).
const START_WEAPON := {"id": 116, "name": "Iron Claymore", "attack": 1, "kind": 0}
const PROGRESS_PER_WIN := 5
## What one stat point adds: HP, MP, attack, defence.
const POINT_GAINS := [5, 3, 1, 1]
enum Stat { HP, MP, ATTACK, DEFENSE }

var hero_name := "Hero"
var level := 1
var experience := 0  # exp into the current level
var fame := 0
var gold := 0
var stat_points := START_POINTS
var base_hp := BASE_HP
var base_mp := BASE_MP
var base_attack := BASE_ATTACK
var base_defense := BASE_DEFENSE
var weapon: Dictionary = START_WEAPON.duplicate()
var skill_levels: Array = []
var hotkeys: Array = [12, 17, 0, 0, 0]
var quick_slots: Array = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
var quick_keys: Array = [0, 1]
var items: Array = []  # things picked up on the maps (ids), for the backpack
var friendship := {}  # general id (as text) -> points
var progress := {}  # ruler id (as text) -> 0..100, 5 a won mission
var done := {}  # "lord:mission" of the missions won

static var _exp_table: Array = []


func _init() -> void:
	for i in 19:
		skill_levels.append(0)
	skill_levels[0] = 1  # the first skills: 12 (on key 1) and 17 (on key 2)
	skill_levels[5] = 1


## The exp from level n to n + 1.
static func exp_needed(at_level: int) -> int:
	if _exp_table.is_empty():
		var f := FileAccess.open(CAMPAIGN_PATH, FileAccess.READ)
		if f != null:
			var data: Variant = JSON.parse_string(f.get_as_text())
			if typeof(data) == TYPE_DICTIONARY:
				_exp_table = data.get("exp_table", [])
	var i := at_level - 1
	return int(_exp_table[i]) if i >= 0 and i < _exp_table.size() else 0


## Adds exp; every full level gives a level and its stat points. Returns the levels gained.
func gain_exp(amount: int) -> int:
	experience += amount
	var gained := 0
	while true:
		var need := exp_needed(level)
		if need <= 0 or experience < need:
			break
		experience -= need
		level += 1
		stat_points += POINTS_PER_LEVEL
		gained += 1
	return gained


## The level the hero would have with this much more exp.
func level_with(amount: int) -> int:
	var lv := level
	var left := experience + amount
	while exp_needed(lv) > 0 and left >= exp_needed(lv):
		left -= exp_needed(lv)
		lv += 1
	return lv


func attack() -> int:
	return base_attack + int(weapon.get("attack", 0))


func defense() -> int:
	return base_defense + int(weapon.get("defense", 0))


func max_hp() -> int:
	return base_hp + int(weapon.get("hp", 0))


func max_mp() -> int:
	return base_mp + int(weapon.get("mp", 0))


## Spends a free stat point on HP (+5), MP (+3), attack (+1) or defence (+1).
## False when there is no point left.
func spend_point(stat: int) -> bool:
	if stat_points <= 0 or stat < 0 or stat >= POINT_GAINS.size():
		return false
	stat_points -= 1
	match stat:
		Stat.HP:
			base_hp += POINT_GAINS[stat]
		Stat.MP:
			base_mp += POINT_GAINS[stat]
		Stat.ATTACK:
			base_attack += POINT_GAINS[stat]
		Stat.DEFENSE:
			base_defense += POINT_GAINS[stat]
	return true


## The hero of a mission starts with this hero's numbers, full HP and MP.
func apply_to(sim: RefCounted) -> void:
	var h = sim.hero
	h.level = level
	h.attack = attack()
	h.defense = defense()
	h.max_hp = max_hp()
	h.hp = h.max_hp
	h.max_mp = max_mp()
	h.mp = h.max_mp
	h.weapon_kind = int(weapon.get("kind", 0))
	for i in mini(skill_levels.size(), sim.skill_levels.size()):
		sim.skill_levels[i] = int(skill_levels[i])
	for i in mini(hotkeys.size(), sim.hotkeys.size()):
		sim.hotkeys[i] = int(hotkeys[i])
	sim.quick_slots = _copy_slots(quick_slots)
	for i in mini(quick_keys.size(), sim.quick_keys.size()):
		sim.quick_keys[i] = int(quick_keys[i])
	sim.friendship = {}
	for k in friendship:
		sim.friendship[int(k)] = int(friendship[k])


## What the mission left: picked gold and things, used potions, friendship; if won, the
## mission's gold and exp, its progress and its place among the missions done.
## Returns the levels gained.
func take_from(sim: RefCounted, lord_id: int, mission: int, ruler_id: int) -> int:
	gold += int(sim.gold)
	items.append_array(sim.items)
	quick_slots = _copy_slots(sim.quick_slots)
	for k in sim.friendship:
		friendship[str(k)] = int(sim.friendship[k])
	if not sim.won:
		return 0
	gold += int(sim.gold_reward())
	fame += int(sim.mission_exp) - int(sim.time_exp)
	var key := str(ruler_id)
	progress[key] = mini(int(progress.get(key, 0)) + PROGRESS_PER_WIN, 100)
	done["%d:%d" % [lord_id, mission]] = true
	return gain_exp(int(sim.exp_reward()))


func is_done(lord_id: int, mission: int) -> bool:
	return done.has("%d:%d" % [lord_id, mission])


func to_dict() -> Dictionary:
	return {"name": hero_name, "level": level, "exp": experience, "fame": fame, "gold": gold, "stat_points": stat_points,
		"base": [base_hp, base_mp, base_attack, base_defense], "weapon": weapon,
		"skill_levels": skill_levels, "hotkeys": hotkeys, "quick_slots": quick_slots,
		"quick_keys": quick_keys, "items": items, "friendship": friendship,
		"progress": progress, "done": done}


func from_dict(d: Dictionary) -> void:
	hero_name = str(d.get("name", hero_name))
	level = int(d.get("level", level))
	experience = int(d.get("exp", experience))
	fame = int(d.get("fame", fame))
	gold = int(d.get("gold", gold))
	stat_points = int(d.get("stat_points", stat_points))
	var b: Array = d.get("base", [base_hp, base_mp, base_attack, base_defense])
	if b.size() == 4:
		base_hp = int(b[0])
		base_mp = int(b[1])
		base_attack = int(b[2])
		base_defense = int(b[3])
	weapon = d.get("weapon", weapon)
	skill_levels = d.get("skill_levels", skill_levels)
	hotkeys = d.get("hotkeys", hotkeys)
	quick_slots = _copy_slots(d.get("quick_slots", quick_slots))
	quick_keys = d.get("quick_keys", quick_keys)
	items = d.get("items", items)
	friendship = d.get("friendship", friendship)
	progress = d.get("progress", progress)
	done = d.get("done", done)


func save(path: String = PATH) -> bool:
	var f := FileAccess.open(path, FileAccess.WRITE)
	if f == null:
		return false
	f.store_string(JSON.stringify(to_dict()))
	return true


## The saved hero, or a new one.
static func load_or_new(path: String = PATH) -> RefCounted:
	var p: RefCounted = load("res://scripts/core/profile.gd").new()
	var f := FileAccess.open(path, FileAccess.READ)
	if f != null:
		var data: Variant = JSON.parse_string(f.get_as_text())
		if typeof(data) == TYPE_DICTIONARY:
			p.from_dict(data)
	return p


static func _copy_slots(slots: Array) -> Array:
	var out: Array = []
	for s in slots:
		out.append([int(s[0]), int(s[1])])
	return out
