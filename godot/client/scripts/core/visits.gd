extends RefCounted
## Visiting the generals: after a won mission the hero may invite one of the generals he is
## friends with (data/visit.json, made by godot/tools/import_original.py). The general greets
## him, warmer the more friendship there is; the hero picks one of four things to talk about;
## the visit adds 5 friendship and, with a chance of the friendship in percent, the general
## gives a gift: a skill of his, a stat, fame, a gear or a potion. One visit per mission won.
## With the Emperor's Seal in the backpack all 44 generals one can visit are on the list.

const PATH := "res://data/visit.json"
const Items := preload("res://scripts/core/items.gd")
const SEAL := 504
const FRIENDSHIP_PER_VISIT := 5
const MAX_FRIENDSHIP := 100
## Above this a general leaves the list (as when it falls to 0).
const LEAVES_ABOVE := 200
const TOPICS := ["Sword", "Books", "Tactics", "People"]
const STAT_TEXTS := ["Atk Up : 1", "Def Up : 1", "HP Up : 5", "MP Up : 3", "Fame Up : 10"]
## Per gift table (a general's gift_table) and topic: a roll of 0..999 below the n-th number
## gives gift n: 0 a skill, 1 attack, 2 defence, 3 HP, 4 MP, 5 fame, 6 a gear, 7 a potion.
const GIFT_ODDS := [
	[[500, 800, 900, 960, 990, 995, 998], [60, 61, 91, 92, 392, 892, 992],
		[100, 600, 900, 930, 990, 995, 996], [1, 2, 5, 305, 310, 410, 910]],
	[[1, 101, 106, 606, 609, 610, 910], [30, 31, 91, 92, 592, 892, 992],
		[300, 360, 860, 960, 961, 991, 996], [1, 2, 5, 10, 40, 100, 200]]]
enum Gift { SKILL, ATTACK, DEFENSE, HP, MP, FAME, GEAR, POTION, NONE }
## The gear a gift is: the hero's level picks the odds of its tier.
const TIER_MIN_LEVEL := [69, 44, 24, 9, 0]
const TIER_ODDS := [[0, 0, 33, 77, 100], [5, 30, 55, 80, 100], [30, 60, 90, 100, 100],
	[40, 80, 100, 100, 100], [80, 100, 100, 100, 100]]
const MAX_SKILL_LEVEL := 10

static var _data: Dictionary = {}


static func data() -> Dictionary:
	if _data.is_empty():
		var f := FileAccess.open(PATH, FileAccess.READ)
		if f != null:
			var d: Variant = JSON.parse_string(f.get_as_text())
			if typeof(d) == TYPE_DICTIONARY:
				_data = d
	return _data


static func line(i: int) -> String:
	var lines: Array = data().get("lines", [])
	return str(lines[i]) if i >= 0 and i < lines.size() else ""


## Can the hero invite someone now: a mission won since the last visit, and a friend.
static func can_visit(profile: RefCounted) -> bool:
	return profile.can_visit and not profile.friendship.is_empty()


## The generals on the list, in the order the hero met them: [[id, friendship], ...].
## With the Emperor's Seal: all generals one can visit, 0 for those not met.
static func generals(profile: RefCounted) -> Array:
	var out: Array = []
	if profile.has_item(SEAL):
		for id in data().get("generals", []):
			out.append([int(id), int(profile.friendship.get(str(int(id)), 0))])
		return out
	for k in profile.friendship:
		out.append([int(k), int(profile.friendship[k])])
	return out


## The greeting: three lines, the hero, the general, the hero. Ten points of friendship
## choose the next three lines; a general of topic 1 has his own thirty.
static func greeting(friendship: int, topic: int, hero_name: String, general_name: String) -> Array:
	var first := mini(clampi(friendship, 0, 100), 99) / 10 * 3 + (30 if topic == 1 else 0)
	var out: Array = []
	for k in 3:
		out.append(_said(general_name if k & 1 else hero_name, line(first + k)))
	return out


## What the hero says about the thing he chose to talk about (0..3), and the general's answer.
static func talk(topic: int, chosen: int, hero_name: String, general_name: String) -> Array:
	var first := 60 + (topic * 4 + chosen) * 2
	return [_said(hero_name, line(first)), _said(general_name, line(first + 1))]


static func _said(who: String, text: String) -> String:
	return "[%s] %s" % [who, text]


## Adds friendship to a general (met or, with amount > 0, one of the 44 one can visit).
## Over 100 it stays 100; at 0 or over 200 he leaves the list. True when it reached 100.
static func add_friendship(profile: RefCounted, id: int, amount: int) -> bool:
	var key := str(id)
	if not profile.friendship.has(key):
		if amount <= 0 or not (id in data().get("generals", []).map(func(g): return int(g))):
			return false
	var points := int(profile.friendship.get(key, 0)) + amount
	if points <= 0 or points > LEAVES_ABOVE:
		profile.friendship.erase(key)
		return false
	if points >= MAX_FRIENDSHIP:
		profile.friendship[key] = MAX_FRIENDSHIP
		return true
	profile.friendship[key] = points
	return false


## The gift after a talk about `chosen` with general `general` (campaign.json generals):
## with a chance of his friendship in percent, a roll picks the kind. Gives it to the hero.
## Returns {kind: Gift, text, title}; kind NONE when there is none (or no room for it).
static func give_gift(profile: RefCounted, general_id: int, general: Dictionary, chosen: int,
		rng: RandomNumberGenerator) -> Dictionary:
	var none := {"kind": Gift.NONE, "text": "", "title": ""}
	var points := int(profile.friendship.get(str(general_id), 0))
	if rng.randi_range(0, 99) >= points:
		return none
	var table: Array = GIFT_ODDS[clampi(int(general.get("gift_table", 0)), 0, 1)][clampi(chosen, 0, 3)]
	var roll := rng.randi_range(0, 999)
	var kind := 0
	while kind < 7 and roll >= int(table[kind]):
		kind += 1
	match kind:
		Gift.SKILL:
			var skills: Array = []
			for s in general.get("skills", []):
				if int(s) == 0:
					break
				skills.append(int(s))
			if skills.is_empty():
				return none
			var skill: int = skills[rng.randi_range(0, skills.size() - 1)]
			var i := skill - 1
			if i < 0 or i >= profile.skill_levels.size() or int(profile.skill_levels[i]) >= MAX_SKILL_LEVEL:
				return none
			profile.skill_levels[i] = int(profile.skill_levels[i]) + 1
			var title := "Skill :" if int(profile.skill_levels[i]) == 1 else "Skill up :"
			return {"kind": kind, "text": skill_name(i), "title": title}
		Gift.ATTACK:
			if profile.base_attack >= 10000:
				return none
			profile.base_attack += 1
		Gift.DEFENSE:
			if profile.base_defense >= 10000:
				return none
			profile.base_defense += 1
		Gift.HP:
			if profile.base_hp >= 25000:
				return none
			profile.base_hp += 5
		Gift.MP:
			if profile.base_mp >= 20000:
				return none
			profile.base_mp += 3
		Gift.FAME:
			profile.fame += 10
		Gift.GEAR:
			var id := gift_gear(int(profile.level), rng)
			if not profile.add_item(Items.make(id, rng)):
				return none
			return {"kind": kind, "text": Items.name_of(id), "title": "Item Acquired!"}
		_:
			var potion := rng.randi_range(1, 11)
			if not profile.add_potion(potion):
				return none
			return {"kind": Gift.POTION, "text": str(Items.POTION_NAMES[potion - 1]).strip_edges(), "title": "Item Acquired!"}
	return {"kind": kind, "text": STAT_TEXTS[kind - 1], "title": ""}


## A gear of a tier the hero's level finds.
static func gift_gear(hero_level: int, rng: RandomNumberGenerator) -> int:
	for b in range(1, 5):
		if hero_level > TIER_MIN_LEVEL[b]:
			var i := rng.randi_range(0, 99)
			for tier in 5:
				if i < TIER_ODDS[b][tier]:
					return 101 + tier + 5 * rng.randi_range(0, 19)
	return 101 + 5 * rng.randi_range(0, 19)


static func skill_name(i: int) -> String:
	var f := FileAccess.open("res://data/skills.json", FileAccess.READ)
	if f == null:
		return ""
	var d: Variant = JSON.parse_string(f.get_as_text())
	var names: Array = d.get("names", []) if typeof(d) == TYPE_DICTIONARY else []
	return String(TranslationServer.translate(str(names[i]))) if i >= 0 and i < names.size() else ""


## Ends a visit: no more until the next mission won, the gift, 5 more friendship.
## Returns the gift (give_gift) and "full": whether the friendship reached 100.
static func finish(profile: RefCounted, general_id: int, general: Dictionary, chosen: int,
		rng: RandomNumberGenerator) -> Dictionary:
	profile.can_visit = false
	var gift := give_gift(profile, general_id, general, chosen, rng)
	gift["full"] = add_friendship(profile, general_id, FRIENDSHIP_PER_VISIT)
	return gift
