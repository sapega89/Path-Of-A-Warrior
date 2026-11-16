extends "res://tests/test_case.gd"
## The gifts of a mission won (Gifts): three different cards from the mission's general, a skill
## of his in the order of its row, a stat, a gear or a potion; kept in the run until one is taken
## on the gift screen.

const TEST_PATH := "user://test_gifts.json"
const GORSKI := 4  # Jan Gorski: Storm Sabre, Thunder Sabre, Healing Herbs, Fury


func _rng(seed_value: int) -> RandomNumberGenerator:
	var rng := RandomNumberGenerator.new()
	rng.seed = seed_value
	return rng


func test_a_general_offers_three_different_cards() -> void:
	var p := Profile.new()
	var kinds := {}
	for s in 50:
		var cards := Gifts.offer(p, GORSKI, Gifts.CARDS, _rng(s))
		eq(cards.size(), Gifts.CARDS, "three cards (seed %d)" % s)
		for i in cards.size():
			kinds[int(cards[i].kind)] = true
			for j in i:
				check(cards[i] != cards[j], "all different: %s" % [cards])
			check(not Gifts.text(p, cards[i]).is_empty(), "said in words: %s" % cards[i])
	check(kinds.has(Gifts.Kind.SKILL), "his skills come")
	check(kinds.has(Gifts.Kind.ATTACK) or kinds.has(Gifts.Kind.DEFENSE), "and stats")


## A general's friendship is the chance, never all of it, that his skill is among the cards.
func test_friendship_brings_his_skill() -> void:
	var with_skill := func(p: Profile) -> int:
		var n := 0
		for s in 200:
			var cards := Gifts.offer(p, GORSKI, Gifts.CARDS, _rng(s))
			eq(cards.size(), Gifts.CARDS, "still three cards")
			if cards.any(func(c: Dictionary) -> bool: return int(c.kind) == Gifts.Kind.SKILL):
				n += 1
		return n
	var p := Profile.new()
	var strangers: int = with_skill.call(p)
	p.friendship = {str(GORSKI): 100}
	var friends: int = with_skill.call(p)
	check(
		friends > strangers + 40, "more often his skill: %d of 200, not %d" % [friends, strangers]
	)
	check(friends < 200, "but not always: %d of 200" % friends)


func test_skills_come_in_the_order_of_their_row() -> void:
	var p := Profile.new()
	var storm := {"skills": [2, 0, 0, 0]}  # Storm Sabre, the second of the sabres
	p.skill_levels[0] = 0
	eq(
		Gifts.card_of(p, storm, Gifts.Kind.SKILL, _rng(1)),
		{"kind": Gifts.Kind.SKILL, "id": 0},
		"Whirlwind Sabre first"
	)
	p.skill_levels[0] = 1
	eq(Gifts.first_lacking(p, 1), 1, "then Storm Sabre itself")
	eq(Gifts.first_lacking(p, 7), 6, "Charm before Protection of the Virgin, Fury known")
	eq(Gifts.first_lacking(p, 16), 16, "an ultimate skill is its own")
	p.skill_levels[1] = Gifts.MAX_SKILL_LEVEL
	eq(Gifts.card_of(p, storm, Gifts.Kind.SKILL, _rng(1)), {}, "no card for a skill at level 10")


func test_no_general_offers_a_stat_a_gear_and_a_potion() -> void:
	var p := Profile.new()
	for general in [0, Profile.ENDING_BASE + 6]:
		var cards := Gifts.offer(p, general, Gifts.CARDS, _rng(3))
		eq(cards.size(), 3, "three cards (%d)" % general)
		check(int(cards[0].kind) in Gifts.STATS, "a stat")
		eq(int(cards[1].kind), Gifts.Kind.GEAR, "a gear")
		eq(int(cards[2].kind), Gifts.Kind.POTION, "a potion")


func test_taking_a_card() -> void:
	var p := Profile.new()
	var rng := _rng(2)
	check(Gifts.take(p, {"kind": Gifts.Kind.SKILL, "id": 3}, rng), "Healing Herbs")
	eq(int(p.skill_levels[3]), 1, "learnt")
	eq(p.hotkeys, [12, 17, 15, 0, 0], "on the first free key")
	Gifts.take(p, {"kind": Gifts.Kind.SKILL, "id": 0}, rng)
	eq(int(p.skill_levels[0]), 2, "a skill known goes up")
	eq(p.hotkeys, [12, 17, 15, 0, 0], "on its key already")
	Gifts.take(p, {"kind": Gifts.Kind.ATTACK, "id": 0}, rng)
	Gifts.take(p, {"kind": Gifts.Kind.HP, "id": 0}, rng)
	eq(p.base_attack, Profile.BASE_ATTACK + 1, "attack +1")
	eq(p.base_hp, Profile.BASE_HP + 5, "HP +5")
	check(Gifts.take(p, {"kind": Gifts.Kind.GEAR, "id": 106}, rng), "a gear")
	check(p.has_item(106), "in the backpack")
	check(Gifts.take(p, {"kind": Gifts.Kind.POTION, "id": 2}, rng), "a potion")
	eq(p.quick_slots[0], [2, 1], "in a quick slot")


func test_no_room_no_card() -> void:
	var p := Profile.new()
	for i in p.backpack.size():
		p.backpack[i] = Items.make(106)
	eq(Gifts.card_of(p, {}, Gifts.Kind.GEAR, _rng(1)), {}, "the backpack is full")
	for s in p.quick_slots.size():
		p.quick_slots[s] = [s + 1, Gifts.SLOT_SIZE]
	for s in 20:
		eq(Gifts.card_of(p, {}, Gifts.Kind.POTION, _rng(s)), {}, "every quick slot is full")
	p.base_attack = Gifts.STAT_CAPS[Gifts.Kind.ATTACK]
	eq(Gifts.card_of(p, {}, Gifts.Kind.ATTACK, _rng(1)), {}, "the attack at its cap")
	eq((Gifts.gear(1, _rng(4)) - 101) % 5 <= 1, true, "a new hero gets low tiers")


func test_a_won_mission_leaves_the_gift_until_taken() -> void:
	var p := Profile.new()
	var sim: MapSim = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	sim.mission_general = GORSKI
	p.take_from(sim, 1, 0, 1, _rng(5))
	check(p.run.gift.is_empty(), "a lost mission gives none")
	sim.won = true
	p.take_from(sim, 1, 0, 1, _rng(5))
	eq(p.run.gift.size(), 3, "a won one: three cards")
	eq(p.run.gift_from, GORSKI, "from its general")
	check(p.save(TEST_PATH), "saved")
	var q := Profile.load_or_new(TEST_PATH)
	eq(q.run.gift, p.run.gift, "the cards are kept")
	eq(q.run.gift_from, GORSKI, "and who gives them")
	q.run.take_gift(q, 0, _rng(1))
	check(q.run.gift.is_empty(), "the others are gone")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))


func test_the_gift_screen() -> void:
	var p := Profile.new()
	p.run.gift_from = GORSKI
	p.run.gift = [
		{"kind": Gifts.Kind.SKILL, "id": 1},
		{"kind": Gifts.Kind.DEFENSE, "id": 0},
		{"kind": Gifts.Kind.POTION, "id": 4},
	]
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var screen: Control = Router.make(Router.SCREENS["gift"])
	root.add_child(screen)
	eq(screen.cards.size(), 3, "three cards")
	check(
		screen.title.text.contains(tr("Jan Gorski")), "the general's name: %s" % screen.title.text
	)
	check(screen.portrait.visible, "and his portrait")
	eq(
		screen.cards[0].text,
		"%s\n%s" % [tr("gift.kind_skill"), tr("gift.skill_level") % [Gifts.skill_name(1), 1]],
		"a skill for the run, at level 1"
	)
	check(screen.cards[0].icon != null, "with its icon")
	eq(screen.cards[1].text, "%s\n%s" % [tr("gift.kind_stat"), tr("gift.defense")], "a stat")
	screen.take(1)
	var q := Profile.load_or_new(TEST_PATH)
	eq(q.base_defense, p.base_defense + 1, "taken and saved")
	check(q.run.gift.is_empty(), "the gift is over")
	screen.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))
