extends RefCounted
## The things the hero carries: gear (ids 101..300), treasures (301..500) and rare things
## (501..), read from data/items.json. A carried thing is a Dictionary {id, attack, defense,
## hp, mp, enchant}; id 0 is an empty place. Potions (ids 1..11) live in the quick slots.

const DATA_PATH := "res://data/items.json"
const EQUIPPED := 9
const BACKPACK := 45  # 25 in the original; more room, as in pyport (BACKPACK_SIZE)
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
	437: " / ATK 1 Increased", 502: " / Oksana's scarf", 504: " / all General Visiting"}
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


## A new thing with its stats. A found gear gets a random extra (below its range) when an rng
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
			bonus += rng.randi_range(0, int(rec.range) - 1) if int(rec.range) > 0 else 0
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
	return String(TranslationServer.translate(str(info(id).get("name", ""))))


## "Iron Broadsword / ATK+1 / Available at Lv1", the line under the Gear and Inventory pages.
static func describe(item: Dictionary) -> String:
	var id := int(item.get("id", 0))
	if id == 0:
		return ""
	var text: String = name_of(id) + str(SUFFIX.get(id, ""))
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


const POTION_NAMES := ["Red Potion (S)", "Red Potion (M)", "Red Potion (L)", "Blue Potion(S)",
	"Blue Potion(M)", "Blue Potion(L)", "H.M.Potion(S)", "H.M.Potion(M)", "H.M.Potion(M)",
	" Powerful Bomb", "Handy Dynamite"]
const POTION_KINDS := ["HP", "MP", "HP&MP"]
const POTION_PERCENTS := [30, 60, 100]
## What the bomb and the dynamite do (the texts of skills 26 and 27; potions recover a share).
const SCROLL_TEXTS := ["Ranged ATK", "Ranged ATK & Knocks back"]


## "Red Potion (S) / Recover 30% of total HP", the line under the Assign Items page.
static func describe_potion(potion: int) -> String:
	var i := potion - 1
	if i < 0 or i >= POTION_NAMES.size():
		return ""
	if i < 9:
		return "%s / Recover %d%% of total %s" % [POTION_NAMES[i], POTION_PERCENTS[i % 3], POTION_KINDS[i / 3]]
	return "%s / %s" % [POTION_NAMES[i], SCROLL_TEXTS[i - 9]]


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


# ---- the Blacksmith: prices, the shop, enchanting -----------------------------------------

const POTION_PRICES := [60, 100, 150, 60, 100, 150, 100, 250, 400, 150, 200]
## The potions and scrolls the shop always has, before its 17 gears.
const SHOP_POTIONS := [1, 2, 3, 4, 5, 6, 10, 11]
const SHOP_GEAR := 17
## The hero's level from which each of the 5 tiers of gear is found, and per tier reached the
## odds (in %, a byte each, lowest first) of finding a gear of tier 0, 1, 2, 3 (else 4).
const TIER_LEVELS := [1, 10, 25, 45, 70]
const TIER_ODDS := [5200, 1321000, 169745950, 421075205, 572588032]
## Enchanting a thing enchanted n times: the chance (%) it works, and when it does not, the
## chance (%) the thing is lost.
const ENCHANT_SUCCESS := [100, 90, 80, 70, 60, 45, 30, 10, 1]
const ENCHANT_LOST := [0, 10, 20, 40, 50, 60, 70, 80, 90]
## How much one enchanting adds: 50, 60, ... 100 % of a tenth of each stat, with these odds.
const ENCHANT_ODDS := [30, 25, 20, 15, 9, 1]


## The tier (0..4) of a gear found by a hero of this level, for a roll of 0..99.
static func tier(hero_level: int, roll: int) -> int:
	var t := 0
	while t < 5 and hero_level >= int(TIER_LEVELS[t]):
		t += 1
	var odds := int(TIER_ODDS[t - 1])
	var limit := 0
	var b := 0
	while b < 4:
		limit += odds & 0xFF
		if roll < limit:
			break
		odds >>= 8
		b += 1
	return b


## What a thing costs in the shop (it sells for half).
static func price(item: Dictionary) -> int:
	var id := int(item.get("id", 0))
	if id <= 0:
		return 0
	if id < 100:
		return int(POTION_PRICES[id - 1]) if id <= POTION_PRICES.size() else 0
	var stats := int(item.attack) + int(item.defense) + int(item.hp) / 5 + int(item.mp) / 3
	if id < 300:
		return int(info(id).get("price", 0)) + stats * 100
	if id < 500:
		return stats * (800 if enchant_max(id) == 0 else 400)
	return int(info(id).get("price", 0))


## How many times a thing can be enchanted (0: never).
static func enchant_max(id: int) -> int:
	if id <= 100 or id >= 500:
		return 0
	return int(info(id).get("enchant_max", 0))


## The price of enchanting a thing once more.
static func enchant_price(item: Dictionary) -> int:
	return int(item.attack) * 100 + int(item.defense) * 100 + int(item.hp) * 100 / 5 + int(item.mp) * 100 / 3


## Enchants a thing: each of its stats above 0 grows by a share of a tenth of it (at least 1).
static func enchant(item: Dictionary, rng: RandomNumberGenerator) -> void:
	var roll := rng.randi_range(0, 100)
	var step := 0
	var sum := 0
	while step < 5:
		sum += int(ENCHANT_ODDS[step])
		if roll < sum:
			break
		step += 1
	var pct := (step + 5) * 10
	for k in GEAR_STATS:
		var v := int(item[k])
		if v > 0:
			item[k] = v + maxi((v * pct / 10 + 50) / 100, 1)
	item.enchant = int(item.enchant) + 1


## "Iron Sabre / Price: 120 / ATK+2 ...", the line under the shop: the name, the price
## (half of it when selling) and what the thing gives.
static func describe_for_sale(item: Dictionary, selling: bool) -> String:
	var id := int(item.get("id", 0))
	if id == 0:
		return ""
	var p := price(item)
	if selling:
		p /= 2
	if id < 100:
		return "%s / Price: %d" % [describe_potion(id), p]
	return "%s / Price: %d" % [describe(item), p]


## The Combine table: [id, id, id (smallest first), what they make], data/mixing.json.
const MIXING_PATH := "res://data/mixing.json"
static var _mixing: Array = []


## What three things can make (one of them, at random): their ids in any order.
static func mixes(ids: Array) -> Array:
	if _mixing.is_empty():
		var f := FileAccess.open(MIXING_PATH, FileAccess.READ)
		if f != null:
			var d: Variant = JSON.parse_string(f.get_as_text())
			if typeof(d) == TYPE_ARRAY:
				_mixing = d
	var key := ids.duplicate()
	key.sort()
	var out: Array = []
	for row in _mixing:
		if int(row[0]) == int(key[0]) and int(row[1]) == int(key[1]) and int(row[2]) == int(key[2]):
			out.append(int(row[3]))
	return out
