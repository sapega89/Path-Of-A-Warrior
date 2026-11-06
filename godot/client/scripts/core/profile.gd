extends RefCounted
## The hero between missions: level, exp, gold, stats, skills, gear and backpack, quick slots,
## the friendship of the generals and the missions done. Kept in user://hero.json. A mission
## starts from it (apply_to) and gives it back what happened (take_from): the gold, gear and
## potions picked up and used, the friendship of the talks and, when won, the mission's gold
## and exp.

const PATH := "user://hero.json"
const CAMPAIGN_PATH := "res://data/campaign.json"
const Items := preload("res://scripts/core/items.gd")
## A new hero: HP, MP, attack, defence, and the free stat points.
const BASE_HP := 30
const BASE_MP := 10
const BASE_ATTACK := 5
const BASE_DEFENSE := 4
const START_POINTS := 5
const POINTS_PER_LEVEL := 3
## The weapon a new hero holds: the Iron Claymore (attack +1).
const START_WEAPON := 116
const PROGRESS_PER_WIN := 5
## The lords a new hero can fight for: bit (id - 1) set.
const START_LORDS_OPEN := 35113052110447
const LORD_COUNT := 45
## Where the hero goes after ending i (0: back to the start, the progress of the rulers lost).
const NEXT_PLACE := [0, 0, 0, 0, 0, 0, 11, 8, 0, 15, 15, 20, 17, 19, 19, 0, 30, 22, 35, 38, 39, 33, 33, 44]
const ENDING_BASE := 200
const SCARF := 502  # Catherine's scarf: the reward of ending 2, needed to see ending 3
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
var equipped: Array = []  # the 9 places of the Gear page, 0 the weapon (Items dictionaries)
var backpack: Array = []  # the 25 places of the Inventory
var skill_levels: Array = []
var hotkeys: Array = [12, 17, 0, 0, 0]
var quick_slots: Array = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
var quick_keys: Array = [0, 1]
var friendship := {}  # general id (as text) -> points
var progress := {}  # ruler id (as text) -> 0..100, 5 a won mission
var done := {}  # "lord:mission" of the missions won
var place := 0  # where the hero is: the lords of campaign chapter `place` can be fought for
var lords_open := START_LORDS_OPEN  # bit (id - 1) set: that lord can be fought for
var endings := 0  # bit i set: ending i was reached
var reward_item := 0  # what the last ending gave (not saved)
var opened_lord := 0  # the lord the last ending opened (not saved)

static var _exp_table: Array = []


func _init() -> void:
	for i in 19:
		skill_levels.append(0)
	skill_levels[0] = 1  # the first skills: 12 (on key 1) and 17 (on key 2)
	skill_levels[5] = 1
	for i in Items.EQUIPPED:
		equipped.append(Items.empty())
	for i in Items.BACKPACK:
		backpack.append(Items.empty())
	equipped[0] = Items.make(START_WEAPON)


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
	return base_attack + gear("attack")


func defense() -> int:
	return base_defense + gear("defense")


func max_hp() -> int:
	return base_hp + gear("hp")


func max_mp() -> int:
	return base_mp + gear("mp")


## What the worn gear adds to a stat ("attack", "defense", "hp", "mp").
func gear(stat: String) -> int:
	var total := 0
	for it in equipped:
		if int(it.id) != 0:
			total += int(it.get(stat, 0))
	return total


## The sword the hero fights with: 0 or 1, the slot type of the weapon worn.
func weapon_kind() -> int:
	var id := int(equipped[0].id)
	return clampi(Items.slot_type(id), 0, 1) if id != 0 else 1


## Puts a found thing into the first free place of the backpack. False when it is full.
func add_item(item: Dictionary) -> bool:
	for i in backpack.size():
		if int(backpack[i].id) == 0:
			backpack[i] = item
			return true
	return false


## Moves the backpack's things up so there are no holes between them.
func compact_backpack() -> void:
	var things: Array = []
	for it in backpack:
		if int(it.id) != 0:
			things.append(it)
	for i in backpack.size():
		backpack[i] = things[i] if i < things.size() else Items.empty()


## Takes off what is worn in a place of the Gear page into the backpack. False when there is
## nothing there or the backpack is full.
func unequip(place: int) -> bool:
	if place < 0 or place >= equipped.size() or int(equipped[place].id) == 0:
		return false
	if not add_item(equipped[place]):
		return false
	equipped[place] = Items.empty()
	return true


## Uses the backpack's thing at i: gear is worn (what was worn in its place takes its place in
## the backpack), a stat item is used up. Returns the line to show: "" when worn, the stat's
## line when used, "cannot" when the hero cannot take it (too low a level or not wearable).
func use_item(i: int) -> String:
	if i < 0 or i >= backpack.size():
		return "cannot"
	var it: Dictionary = backpack[i]
	var id := int(it.id)
	if id == 0:
		return ""
	if Items.level_needed(id) > level or id in Items.NOT_WORN:
		return "cannot"
	if Items.STAT_ITEMS.has(id):
		var s: Dictionary = Items.STAT_ITEMS[id]
		match str(s.stat):
			"hp": base_hp += int(s.add)
			"mp": base_mp += int(s.add)
			"defense": base_defense += int(s.add)
			"attack": base_attack += int(s.add)
		backpack[i] = Items.empty()
		return str(s.text)
	var place := Items.place(id)
	backpack[i] = equipped[place]
	equipped[place] = it
	return ""


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


## The level of skill 12..30, 0 when not learned.
func skill_level(skill: int) -> int:
	var i := skill - 12
	return int(skill_levels[i]) if i >= 0 and i < skill_levels.size() else 0


## Puts a learned skill on a skill key (slot 0..4). False when the skill is not learned.
func assign_hotkey(slot: int, skill: int) -> bool:
	if slot < 0 or slot >= hotkeys.size() or skill_level(skill) == 0:
		return false
	hotkeys[slot] = skill
	return true


## Puts the potion slot (0..4) on potion key 0 or 1. A slot the other key holds swaps the two
## keys. False when the slot is empty or already on that key.
func assign_quick_key(key: int, slot: int) -> bool:
	if key < 0 or key > 1 or slot < 0 or slot >= quick_slots.size():
		return false
	if int(quick_slots[slot][0]) == 0 or int(quick_keys[key]) == slot:
		return false
	var other := (key + 1) & 1
	if int(quick_keys[other]) == slot:
		quick_keys[other] = quick_keys[key]
	quick_keys[key] = slot
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
	h.weapon_kind = weapon_kind()
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


## What the mission left: picked gold and things (a found gear gets its random extra from
## rng; what does not fit in the backpack is lost), used potions, friendship; if won, the
## mission's gold and exp, its progress and its place among the missions done.
## Returns the levels gained.
func take_from(sim: RefCounted, lord_id: int, mission: int, ruler_id: int,
		rng: RandomNumberGenerator = null) -> int:
	gold += int(sim.gold)
	if rng == null:
		rng = RandomNumberGenerator.new()
	for id in sim.items:
		add_item(Items.make(int(id), rng))
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


## Where the campaign goes after a mission (info: its campaign.json record). A won mission
## takes the hero to the lord's place. A mission whose general is 200 + i (won) or whose
## reward is 200 + i (lost) ends the story with ending i: the hero goes to that ending's
## place, gets the mission's gold anyway when lost, sometimes a gear (Catherine's scarf
## after ending 2), and one more lord opens. Returns the ending reached, or -1.
func advance(sim: RefCounted, lord_id: int, info: Dictionary, rng: RandomNumberGenerator = null) -> int:
	if rng == null:
		rng = RandomNumberGenerator.new()
	var general := int(info.get("general", 0))
	var reward := int(info.get("reward", 0))
	var ending := -1
	if sim.won:
		place = lord_id
		if general >= ENDING_BASE:
			ending = general - ENDING_BASE
	elif reward > ENDING_BASE:
		place = lord_id
		ending = reward - ENDING_BASE
		gold += int(sim.gold_reward())
	reward_item = 0
	opened_lord = 0
	if ending < 0:
		return -1
	if ending != 3 or has_item(SCARF):
		endings |= 1 << ending
	place = NEXT_PLACE[ending] if ending < NEXT_PLACE.size() else 0
	if place == 0:
		progress = {}
	var item := 0
	if ending == 2:
		item = SCARF
	elif rng.randi_range(0, 9) == 0:
		item = 101 + (4 if level / 20 > 4 else level / 20) + 5 * rng.randi_range(0, 19)
	var closed: Array = []
	for i in LORD_COUNT:
		if lords_open & (1 << i) == 0:
			closed.append(i)
	if not closed.is_empty():
		var i := int(closed[rng.randi_range(0, closed.size() - 1)])
		lords_open |= 1 << i
		opened_lord = i + 1
	if item != 0 and add_item(Items.make(item, rng)):
		reward_item = item
	if ending == 3 and not has_item(SCARF):
		place = 4  # without the scarf the story of ending 3 is not told: back to chapter 4
	return ending


func is_lord_open(id: int) -> bool:
	return id >= 1 and lords_open & (1 << (id - 1)) != 0


func has_item(id: int) -> bool:
	for it in backpack:
		if int(it.id) == id:
			return true
	return false


func is_done(lord_id: int, mission: int) -> bool:
	return done.has("%d:%d" % [lord_id, mission])


func to_dict() -> Dictionary:
	return {"name": hero_name, "level": level, "exp": experience, "fame": fame, "gold": gold, "stat_points": stat_points,
		"base": [base_hp, base_mp, base_attack, base_defense], "equipped": equipped,
		"backpack": backpack,
		"skill_levels": skill_levels, "hotkeys": hotkeys, "quick_slots": quick_slots,
		"quick_keys": quick_keys, "friendship": friendship,
		"progress": progress, "done": done, "place": place, "lords_open": lords_open,
		"endings": endings}


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
	equipped = _copy_items(d.get("equipped", []), Items.EQUIPPED, equipped)
	backpack = _copy_items(d.get("backpack", []), Items.BACKPACK, backpack)
	skill_levels = d.get("skill_levels", skill_levels)
	hotkeys = d.get("hotkeys", hotkeys)
	quick_slots = _copy_slots(d.get("quick_slots", quick_slots))
	quick_keys = d.get("quick_keys", quick_keys)
	friendship = d.get("friendship", friendship)
	progress = d.get("progress", progress)
	done = d.get("done", done)
	place = int(d.get("place", place))
	lords_open = int(d.get("lords_open", lords_open))
	endings = int(d.get("endings", endings))


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


## A saved list of things, as many places as the hero has; the default when none was saved.
static func _copy_items(saved: Array, size: int, default: Array) -> Array:
	if saved.is_empty():
		return default
	var out: Array = []
	for i in size:
		var it := Items.empty()
		if i < saved.size() and typeof(saved[i]) == TYPE_DICTIONARY:
			for k in it:
				it[k] = int(saved[i].get(k, 0))
		out.append(it)
	return out


static func _copy_slots(slots: Array) -> Array:
	var out: Array = []
	for s in slots:
		out.append([int(s[0]), int(s[1])])
	return out
