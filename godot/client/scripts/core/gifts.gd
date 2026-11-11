class_name Gifts
extends RefCounted
## The gifts of a mission won: its general offers three cards (four with the perk) and the hero
## takes one. A card is a skill the general knows (new at level 1 or one level up, to 10), a
## stat (+1 attack, +1 defence, +5 HP or +3 MP), a gear of the hero's level or a potion. The
## skill lasts the run (HeroRun ends it); the rest is the hero's for good. The kind of each card
## is rolled on the general's gift table, a random row of it; no fame. A general who knows a
## later skill of a row offers the first one of the row the hero lacks. The general's friendship
## (Profile.friendship, 5 a talk) is the percent chance, at most FRIEND_MAX, that one of the cards
## is his skill. A mission with no general (an ending, two missions of the campaign) offers a
## stat, a gear and a potion.

enum Kind { SKILL, ATTACK, DEFENSE, HP, MP, GEAR, POTION }

const CARDS := 3
## The most a general's friendship makes the chance of his skill among the cards, in percent.
const FRIEND_MAX := 90
const TRIES := 40  # rolls before three different cards are given up
## Per gift table (a general's gift_table), four rows: a roll of 0..999 below the n-th number
## gives the n-th of ROLLED (the last one when below none).
const ODDS := [
	[
		[500, 800, 900, 960, 990, 995, 998],
		[60, 61, 91, 92, 392, 892, 992],
		[100, 600, 900, 930, 990, 995, 996],
		[1, 2, 5, 305, 310, 410, 910]
	],
	[
		[1, 101, 106, 606, 609, 610, 910],
		[30, 31, 91, 92, 592, 892, 992],
		[300, 360, 860, 960, 961, 991, 996],
		[1, 2, 5, 10, 40, 100, 200]
	]
]
## What a roll gives; -1 is fame, which is no gift here: that card is rolled again.
const ROLLED := [
	Kind.SKILL, Kind.ATTACK, Kind.DEFENSE, Kind.HP, Kind.MP, -1, Kind.GEAR, Kind.POTION
]
const STATS := [Kind.ATTACK, Kind.DEFENSE, Kind.HP, Kind.MP]
## What a stat card adds, and up to where the stat may grow.
const STAT_GAINS := {Kind.ATTACK: 1, Kind.DEFENSE: 1, Kind.HP: 5, Kind.MP: 3}
const STAT_CAPS := {Kind.ATTACK: 10000, Kind.DEFENSE: 10000, Kind.HP: 25000, Kind.MP: 20000}
const STAT_FIELDS := {
	Kind.ATTACK: "base_attack", Kind.DEFENSE: "base_defense", Kind.HP: "base_hp", Kind.MP: "base_mp"
}
const STAT_TEXTS := {
	Kind.ATTACK: "gift.attack", Kind.DEFENSE: "gift.defense", Kind.HP: "gift.hp", Kind.MP: "gift.mp"
}
const MAX_SKILL_LEVEL := 10
## The rows of skills whose later skills come after the first (places in Profile.skill_levels);
## the ultimate skills (the last row of skills.json) are each their own.
const ORDERED_ROWS := [[0, 1, 2], [3, 4], [5, 6, 7], [8, 9, 10], [11, 12, 13], [14, 15]]
const FIRST_SKILL_ID := 12  # the id of the skill in place 0 (the hotkeys hold ids)
const POTIONS := 11
const SLOT_SIZE := 5  # potions of one kind a quick slot holds (Profile.add_potion)
## The gear a gift is: the hero's level picks the odds of its tier.
const TIER_MIN_LEVEL := [69, 44, 24, 9, 0]
const TIER_ODDS := [
	[0, 0, 33, 77, 100],
	[5, 30, 55, 80, 100],
	[30, 60, 90, 100, 100],
	[40, 80, 100, 100, 100],
	[80, 100, 100, 100, 100]
]


## Up to `count` different cards (three; four with the perk, HeroRun) from general `general_id`
## (campaign.json generals; 0 or an ending's number: no general) for the hero: [{kind: Kind, id}],
## id the skill's place, the gear's or the potion's id. Fewer when there are not so many to give.
## With no general: a stat, a gear, a potion and another stat.
static func offer(
	profile: Profile, general_id: int, count: int, rng: RandomNumberGenerator
) -> Array[Dictionary]:
	var general := MapSim.general_data(general_id)
	var cards: Array[Dictionary] = []
	if general.is_empty():
		var first := rng.randi_range(0, STATS.size() - 1)
		var other := (first + rng.randi_range(1, STATS.size() - 1)) % STATS.size()
		var kinds: Array = [STATS[first], Kind.GEAR, Kind.POTION, STATS[other]]
		for kind: int in kinds.slice(0, count):
			_add(cards, card_of(profile, general, kind, rng))
		return cards
	var table: Array = ODDS[clampi(int(general.get("gift_table", 0)), 0, ODDS.size() - 1)]
	for t in TRIES:
		if cards.size() >= count:
			break
		var kind := roll(table[rng.randi_range(0, table.size() - 1)], rng)
		if kind >= 0:
			_add(cards, card_of(profile, general, kind, rng))
	_friends_skill(profile, general_id, cards, count, rng)
	return cards


## With the chance of the general's friendship (at most FRIEND_MAX percent), his skill is one of
## the cards when none is yet: it comes first and the last card gives way.
static func _friends_skill(
	profile: Profile,
	general_id: int,
	cards: Array[Dictionary],
	count: int,
	rng: RandomNumberGenerator
) -> void:
	var friend := mini(int(profile.friendship.get(str(general_id), 0)), FRIEND_MAX)
	if friend <= 0 or cards.any(func(c: Dictionary) -> bool: return int(c.kind) == Kind.SKILL):
		return
	if rng.randi_range(0, 99) >= friend:
		return
	var card := card_of(profile, MapSim.general_data(general_id), Kind.SKILL, rng)
	if card.is_empty():
		return
	if cards.size() >= count:
		cards.pop_back()
	cards.push_front(card)


## The kind a roll on one row of a gift table gives (-1: fame, none).
static func roll(row: Array, rng: RandomNumberGenerator) -> int:
	var r := rng.randi_range(0, 999)
	var n := 0
	while n < row.size() and r >= int(row[n]):
		n += 1
	return int(ROLLED[n])


## A card of `kind` for the hero, {} when there is none to give: no skill of the general's left
## to learn, the stat at its cap, no room in the backpack or the quick slots.
static func card_of(
	profile: Profile, general: Dictionary, kind: int, rng: RandomNumberGenerator
) -> Dictionary:
	match kind:
		Kind.SKILL:
			var known: Array[int] = []
			for s in general.get("skills", []):
				if int(s) > 0:
					known.append(int(s) - 1)
			if known.is_empty():
				return {}
			var place := first_lacking(profile, known[rng.randi_range(0, known.size() - 1)])
			if int(profile.skill_levels[place]) >= MAX_SKILL_LEVEL:
				return {}
			return {"kind": kind, "id": place}
		Kind.GEAR:
			if not profile.backpack.any(func(it: Dictionary) -> bool: return int(it.id) == 0):
				return {}
			return {"kind": kind, "id": gear(profile.level, rng)}
		Kind.POTION:
			var potion := rng.randi_range(1, POTIONS)
			if not profile.quick_slots.any(
				func(s: Array) -> bool:
					return int(s[0]) == 0 or (int(s[0]) == potion and int(s[1]) < SLOT_SIZE)
			):
				return {}
			return {"kind": kind, "id": potion}
	if int(profile.get(STAT_FIELDS[kind])) >= int(STAT_CAPS[kind]):
		return {}
	return {"kind": kind, "id": 0}


## The skill a general who knows skill `place` teaches: the first of its row the hero lacks,
## or that one itself.
static func first_lacking(profile: Profile, place: int) -> int:
	for row: Array in ORDERED_ROWS:
		if place in row:
			for p: int in row:
				if p == place or int(profile.skill_levels[p]) == 0:
					return p
	return place


## A gear of a tier the hero's level finds.
static func gear(hero_level: int, rng: RandomNumberGenerator) -> int:
	for b in range(1, 5):
		if hero_level > TIER_MIN_LEVEL[b]:
			var i := rng.randi_range(0, 99)
			for tier in 5:
				if i < TIER_ODDS[b][tier]:
					return 101 + tier + 5 * rng.randi_range(0, 19)
	return 101 + 5 * rng.randi_range(0, 19)


## Gives the hero a card. A skill learnt anew goes on the first free skill key. False when it
## could not be given (no room any more).
static func take(profile: Profile, card: Dictionary, rng: RandomNumberGenerator) -> bool:
	var kind := int(card.get("kind", -1))
	var id := int(card.get("id", 0))
	match kind:
		Kind.SKILL:
			if id < 0 or id >= profile.skill_levels.size():
				return false
			profile.skill_levels[id] = mini(int(profile.skill_levels[id]) + 1, MAX_SKILL_LEVEL)
			var free := profile.hotkeys.find(0)
			if int(profile.skill_levels[id]) == 1 and free >= 0:
				profile.assign_hotkey(free, FIRST_SKILL_ID + id)
			return true
		Kind.GEAR:
			return profile.add_item(Items.make(id, rng))
		Kind.POTION:
			return profile.add_potion(id)
	if not STAT_FIELDS.has(kind):
		return false
	var field: String = STAT_FIELDS[kind]
	profile.set(field, mini(int(profile.get(field)) + int(STAT_GAINS[kind]), int(STAT_CAPS[kind])))
	return true


## What kind of card it is (a translation key): a skill for the run, a stat, a gear, a potion.
static func kind_key(card: Dictionary) -> String:
	match int(card.get("kind", -1)):
		Kind.SKILL:
			return "gift.kind_skill"
		Kind.GEAR:
			return "gift.kind_gear"
		Kind.POTION:
			return "gift.kind_potion"
	return "gift.kind_stat"


## What the card gives, in words: the skill and its level after it, the stat, the thing's name.
static func text(profile: Profile, card: Dictionary) -> String:
	var kind := int(card.get("kind", -1))
	var id := int(card.get("id", 0))
	match kind:
		Kind.SKILL:
			var level := mini(int(profile.skill_levels[id]) + 1, MAX_SKILL_LEVEL)
			return _tr("gift.skill_level") % [skill_name(id), level]
		Kind.GEAR:
			return Items.name_of(id)
		Kind.POTION:
			return _tr(str(Items.POTION_NAMES[id - 1]).strip_edges())
	return _tr(STAT_TEXTS.get(kind, ""))


## The name of the skill in place i of Profile.skill_levels, in the player's language.
static func skill_name(i: int) -> String:
	var d: Variant = JSON.parse_string(FileAccess.get_file_as_string("res://data/skills.json"))
	var names: Array = d.get("names", []) if typeof(d) == TYPE_DICTIONARY else []
	return _tr(str(names[i])) if i >= 0 and i < names.size() else ""


static func _add(cards: Array[Dictionary], card: Dictionary) -> void:
	if not card.is_empty() and not cards.has(card):
		cards.append(card)


static func _tr(key: String) -> String:
	return String(TranslationServer.translate(key))
