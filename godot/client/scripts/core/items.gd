extends RefCounted
## The things the hero carries: gear (ids 101..300), treasures (301..500) and rare things
## (501..), read from data/items.json. A carried thing is a Dictionary {id, attack, defense,
## hp, mp, enchant}; id 0 is an empty place. Potions (ids 1..11) live in the quick slots.

const DATA_PATH := "res://data/items.json"
const EQUIPPED := 9
const BACKPACK := 25
## Slot type of a thing -> its place on the Gear page (0 the weapon: both sword types).
const EQUIP_PLACE := [0, 0, 3, 5, 2, 8, 6, 1, 4, 7]
## Things that are used up from the backpack: what each adds to the hero.
const STAT_ITEMS := {
	434: {"stat": "hp", "add": 5, "text": "HP Up : 5"},
	435: {"stat": "mp", "add": 3, "text": "MP Up : 3"},
	436: {"stat": "defense", "add": 1, "text": "Def Up : 1"},
	437: {"stat": "attack", "add": 1, "text": "Atk Up : 1"},
}
## Things that can be carried but not worn.
const NOT_WORN := [502, 504]
const SUFFIX := {434: " / Hp 5 Increased", 435: " / MP 3 Increased", 436: " / DEF 1 Increased",
	437: " / ATK 1 Increased", 502: " / Catherine's scarf", 504: " / all General Visiting"}
const GEAR_STATS := ["attack", "defense", "hp", "mp"]
## Icon sheets: potions, gear, treasures, rare things (28 px icons in a row).
const SHEETS := ["tool", "kibo", "sungbo", "shinki"]

static var _data: Dictionary = {}


static func data() -> Dictionary:
	if _data.is_empty():
		var f := FileAccess.open(DATA_PATH, FileAccess.READ)
		if f != null:
			var d: Variant = JSON.parse_string(f.get_as_text())
			if typeof(d) == TYPE_DICTIONARY:
				_data = d
	return _data


## The record of a thing (name, slot, stats, icon, level), or {} for an unknown id.
static func info(id: int) -> Dictionary:
	var table := "gear" if id <= 300 else ("treasures" if id <= 500 else "rare")
	return data().get(table, {}).get(str(id), {})


static func empty() -> Dictionary:
	return {"id": 0, "attack": 0, "defense": 0, "hp": 0, "mp": 0, "enchant": 0}


## A new thing with its stats. A found gear gets a random extra (0..its range) when an rng
## is given; without one it has just its bonus.
static func make(id: int, rng: RandomNumberGenerator = null) -> Dictionary:
	var item := empty()
	var rec := info(id)
	if rec.is_empty():
		return item
	item.id = id
	if id <= 300:
		var bonus := int(rec.bonus)
		if rng != null:
			bonus += rng.randi_range(0, int(rec.range))
		var stat := int(rec.stat)
		if stat >= 0 and stat < GEAR_STATS.size():
			item[GEAR_STATS[stat]] = bonus
	else:
		for k in GEAR_STATS:
			item[k] = int(rec.get(k, 0))
	return item


static func slot_type(id: int) -> int:
	return int(info(id).get("slot", 0))


## The place on the Gear page a thing is worn in.
static func place(id: int) -> int:
	var t := slot_type(id)
	return EQUIP_PLACE[t] if t >= 0 and t < EQUIP_PLACE.size() else 0


static func level_needed(id: int) -> int:
	return int(info(id).get("level", 0))


static func name_of(id: int) -> String:
	return str(info(id).get("name", ""))


## "Iron Claymore / ATK+1 / Available at Lv1", the line under the Gear and Inventory pages.
static func describe(item: Dictionary) -> String:
	var id := int(item.get("id", 0))
	if id == 0:
		return ""
	var text := name_of(id) + SUFFIX.get(id, "")
	for k in [["attack", "ATK"], ["defense", "DEF"], ["hp", "HP"], ["mp", "MP"]]:
		var v := int(item.get(k[0], 0))
		if v != 0:
			text += " / %s+%d" % [k[1], v]
	var enchant := int(item.get("enchant", 0))
	if enchant != 0:
		text += " / Enchanted Lv%d" % enchant
	var level := level_needed(id)
	if level != 0:
		text += " / Available at Lv%d" % level
	return text


## [sheet name, icon index] of a thing, or ["", -1] for none.
static func icon(id: int) -> Array:
	if id > 500:
		return [SHEETS[3], id - 501]
	if id > 300:
		return [SHEETS[2], int(info(id).get("icon", -1))]
	if id > 100:
		return [SHEETS[1], int(info(id).get("icon", -1))]
	if id > 0:
		return [SHEETS[0], id - 1]
	return ["", -1]
