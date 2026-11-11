extends "res://tests/test_case.gd"
## The run (HeroRun): flasks of living water bought with fame, a lost mission spends one or ends
## the run, an ending back to the start ends it and one on to a main camp fills a flask. Before a
## run, in the start camp: the starting skill and the perks bought with fame; the attributes,
## enchanting and combining only there.

const TEST_PATH := "user://test_hero_run.json"


## A hero halfway through a run: a skill learnt on it, a colonel's progress, a mission won.
func _hero_mid_run() -> Profile:
	var p := Profile.new()
	p.skill_levels[2] = 3
	p.hotkeys = [12, 17, 14, 0, 0]
	p.progress = {"5": 10}
	p.done = {"2:0": true}
	p.place = 2
	p.heading = 3
	p.fame = 5000
	p.gold = 700
	return p


func _sim(won: bool) -> RefCounted:
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	sim.won = won
	return sim


func test_flasks_are_bought_with_fame() -> void:
	var p := Profile.new()
	p.fame = int(HeroRun.FLASK_PRICES[0]) - 1
	check(not p.run.buy_flask(p), "not enough fame")
	eq(p.run.flasks, 0, "none bought")
	var total := 0
	for price in HeroRun.FLASK_PRICES:
		total += int(price)
	p.fame = total + 5
	for i in HeroRun.MAX_FLASKS:
		check(p.run.buy_flask(p), "flask %d" % (i + 1))
	eq(p.run.flasks, HeroRun.MAX_FLASKS, "three at most")
	eq(p.run.flasks_left, HeroRun.MAX_FLASKS, "each is full at once")
	eq(p.fame, 5, "each costs its price")
	check(not p.run.buy_flask(p), "no fourth")
	eq(p.run.flask_price(), 0, "nothing more to buy")


func test_a_lost_mission_spends_a_flask() -> void:
	var p := _hero_mid_run()
	p.run.flasks = 1
	p.run.flasks_left = 1
	var cost: Dictionary = p.run.lose_mission(p, false, JavaRandom.new(1))
	check(not cost.over, "the run goes on")
	eq(p.run.flasks_left, 0, "the flask is empty")
	eq(p.place, 2, "the same camp")
	eq(int(p.skill_levels[2]), 3, "the skills of the run are kept")
	eq(p.done, {"2:0": true}, "and the missions won")


func test_a_lost_mission_with_no_flask_ends_the_run() -> void:
	var p := _hero_mid_run()
	p.run.flasks = 2  # bought, both spent
	p.run.flasks_left = 0
	var cost: Dictionary = p.run.lose_mission(p, false, JavaRandom.new(1))
	check(cost.over, "the run is over")
	eq(p.place, 0, "back at the start")
	eq(p.heading, 0, "heading nowhere")
	eq(p.progress, {}, "the colonels' progress is gone")
	eq(p.done, {}, "the missions of the run can be won again")
	eq(int(p.skill_levels[2]), 0, "a skill learnt on the run is gone")
	eq(int(p.skill_levels[0]), 1, "the starting skill is back")
	eq(int(p.skill_levels[5]), 0, "and only it")
	eq(p.hotkeys, [12, 0, 0, 0, 0], "on key 1")
	eq(p.run.flasks_left, 2, "every flask bought is full again")
	eq(p.gold, 700, "the gold is kept")
	eq(p.fame, 5000, "and the fame")


func test_a_loss_that_ends_the_story_costs_no_flask() -> void:
	var p := _hero_mid_run()
	var cost: Dictionary = p.run.lose_mission(p, true, JavaRandom.new(1))
	check(not cost.over, "the ending comes instead")
	eq(p.place, 2, "nothing is reset here")


func test_endings_end_the_run_or_fill_a_flask() -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 3
	var p := _hero_mid_run()
	p.run.flasks = 2
	p.run.flasks_left = 0
	eq(p.advance(_sim(true), 9, {"general": 206, "reward": 0}, rng), 6, "ending 6")
	eq(p.place, 11, "on to its main camp")
	eq(p.run.flasks_left, 1, "one flask is full again")
	eq(int(p.skill_levels[2]), 3, "the run goes on with its skills")
	eq(p.advance(_sim(true), 5, {"general": 200, "reward": 0}, rng), 0, "ending 0")
	eq(p.place, 0, "back to the start")
	eq(int(p.skill_levels[2]), 0, "the run is over: its skills are gone")
	eq(p.run.flasks_left, 2, "every flask is full")
	eq(p.done, {"2:0": true}, "the missions won stay, as after an ending")


func test_the_flasks_are_saved() -> void:
	var p := Profile.new()
	p.run.flasks = 3
	p.run.flasks_left = 1
	check(p.save(TEST_PATH), "saved")
	var q := Profile.load_or_new(TEST_PATH) as Profile
	eq(q.run.flasks, 3, "bought")
	eq(q.run.flasks_left, 1, "full")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))


func test_the_town_hall_of_the_start_opens_the_run_setup() -> void:
	Profile.new().save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var hall: Control = Router.make(Router.SCREENS["town_hall"])
	root.add_child(hall)
	check(hall.prepare.visible, "before the run")
	check(hall.flasks.text.contains("0"), "which shows the flasks: %s" % hall.flasks.text)
	hall.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))


func test_the_starting_skill() -> void:
	var p := Profile.new()
	var run: HeroRun = p.run
	eq(run.start_skills, [0] as Array[int], "Whirlwind Sabre at first")
	run.known_skills = [3, 8]  # learnt in runs before
	check(run.choose_start_skill(p, 3), "Healing Herbs")
	eq(int(p.skill_levels[3]), 1, "learnt")
	eq(int(p.skill_levels[0]) + int(p.skill_levels[5]), 0, "and nothing else")
	eq(p.hotkeys, [15, 0, 0, 0, 0], "on key 1")
	check(not run.choose_start_skill(p, 1), "Storm Sabre is not a first skill")
	eq(run.start_choices(p), [0, 3, 5, 8] as Array[int], "Whirlwind Sabre and Fury stay known")
	p.fame = int(HeroRun.PERK_PRICES["second_skill"])
	check(run.buy_perk(p, "second_skill"), "a second skill bought")
	run.choose_start_skill(p, 5)
	eq(run.start_skills, [3, 5] as Array[int], "two skills")
	eq(p.hotkeys, [15, 17, 0, 0, 0], "on keys 1 and 2")
	run.choose_start_skill(p, 8)
	eq(run.start_skills, [5, 8] as Array[int], "a third: the oldest goes")
	run.choose_start_skill(p, 8)
	eq(run.start_skills, [5] as Array[int], "pressed again: dropped")
	run.choose_start_skill(p, 5)
	eq(run.start_skills, [5] as Array[int], "the last one stays")
	run.end(p)
	eq(int(p.skill_levels[5]), 1, "a new run starts with it")


## A run may start only with a skill the hero has learnt in a run: a new hero with his first
## run's two, then what a run taught him too; kept in the save.
func test_only_the_skills_learnt_in_a_run_to_start_with() -> void:
	var p := Profile.new()
	var run: HeroRun = p.run
	eq(run.start_choices(p), [0, 5] as Array[int], "a new hero: Whirlwind Sabre and Fury")
	check(not run.choose_start_skill(p, 11), "not Ring of Fire, never learnt")
	p.skill_levels[11] = 2  # a gift in the run
	run.end(p)
	eq(int(p.skill_levels[11]), 0, "gone with the run")
	eq(run.start_choices(p), [0, 5, 11] as Array[int], "but a choice for the next one")
	check(p.save(TEST_PATH), "saved")
	var q := Profile.load_or_new(TEST_PATH)
	eq(q.run.known_skills, [0, 5, 11] as Array[int], "kept")
	check(q.run.choose_start_skill(q, 11), "Ring of Fire chosen")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))


func test_perks_bought_with_fame() -> void:
	var p := Profile.new()
	var run: HeroRun = p.run
	check(not run.buy_perk(p, "card"), "no fame")
	p.fame = int(HeroRun.PERK_PRICES["card"]) + int(HeroRun.PERK_PRICES["reroll"])
	check(run.buy_perk(p, "card"), "a 4th card")
	check(not run.buy_perk(p, "card"), "once")
	check(not run.buy_perk(p, "nothing"), "only what is sold")
	eq(run.gift_cards(), 4, "four cards")
	var rng := RandomNumberGenerator.new()
	run.offer_gift(p, 4, rng)
	eq(run.gift.size(), 4, "offered")
	check(not run.can_reroll(), "no reroll yet")
	check(run.buy_perk(p, "reroll"), "a reroll")
	eq(p.fame, 0, "each for its price")
	check(run.reroll_gift(p, rng), "the cards rolled again")
	eq(run.gift.size(), 4, "as many")
	check(not run.reroll_gift(p, rng), "once a run")
	check(p.save(TEST_PATH), "saved")
	var q := Profile.load_or_new(TEST_PATH)
	check(q.run.has_perk("card") and q.run.has_perk("reroll"), "the perks are kept")
	check(q.run.reroll_used, "and the reroll spent")
	q.run.end(q)
	check(not q.run.reroll_used, "a new run: the reroll is back")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))


func test_the_run_setup_screen() -> void:
	var p := Profile.new()
	p.fame = int(HeroRun.FLASK_PRICES[0]) + int(HeroRun.PERK_PRICES["second_skill"])
	p.run.known_skills = [11]
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var screen: Control = Router.make(Router.SCREENS["run_setup"])
	root.add_child(screen)
	eq(screen.skills.size(), HeroRun.START_CHOICES.size(), "six first skills")
	var shown: Array = screen.skills.keys().filter(
		func(k: int) -> bool: return screen.skills[k].visible
	)
	eq(shown, [0, 5, 11], "only those learnt in a run")
	check(screen.skills[0].button_pressed, "Whirlwind Sabre chosen")
	check(screen.skills[0].icon != null, "with its icon")
	screen.choose(11)
	check(screen.skills[11].button_pressed and not screen.skills[0].button_pressed, "Ring of Fire")
	eq(Profile.load_or_new(TEST_PATH).run.start_skills, [11] as Array[int], "saved")
	check(not screen.flask.disabled, "a flask for its fame")
	screen.buy_flask()
	eq(Profile.load_or_new(TEST_PATH).run.flasks, 1, "bought and saved")
	screen.buy_perk("second_skill")
	check(Profile.load_or_new(TEST_PATH).run.has_perk("second_skill"), "the second skill")
	eq(screen.fame.text, tr("run_setup.fame") % 0, "the fame spent")
	check(screen.perk_list.get_node("Card").disabled, "nothing more to pay with")
	screen.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))


func test_attributes_and_the_smith_only_at_the_start() -> void:
	var p := Profile.new()
	p.stat_points = 3
	p.place = 7
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var attributes: Control = Router.make(Router.SCREENS["attributes"])
	root.add_child(attributes)
	check(attributes.plus["HP"].disabled, "no point spent in a camp of the run")
	check(attributes.start_only.visible, "and a note says so")
	check(not attributes.spend(Profile.Stat.HP), "not even by a call")
	attributes.free()
	var smith: Control = Router.make(Router.SCREENS["blacksmith"])
	root.add_child(smith)
	check(not smith.buttons[2].visible and not smith.buttons[3].visible, "no enchant, no combine")
	check(smith.buttons[0].visible and smith.buttons[1].visible, "the shop is open")
	check(not smith.open_page("enchant"), "enchant does not open")
	smith.free()
	p.place = 0
	p.save(TEST_PATH)
	smith = Router.make(Router.SCREENS["blacksmith"])
	root.add_child(smith)
	check(smith.buttons[2].visible and smith.buttons[3].visible, "the start: enchant and combine")
	smith.free()
	attributes = Router.make(Router.SCREENS["attributes"])
	root.add_child(attributes)
	check(not attributes.start_only.visible, "the start camp")
	check(attributes.spend(Profile.Stat.HP), "spends a point")
	attributes.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))


func test_the_run_end_screen() -> void:
	var p := Profile.new()
	p.level = 7
	p.gold = 321
	p.fame = 45
	p.run.flasks = 2
	p.run.flasks_left = 2
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var screen: Control = Router.make(Router.SCREENS["run_end"])
	root.add_child(screen)
	eq(screen.kept.text, tr("run_end.kept") % [7, 321, 45], "what the hero keeps")
	eq(screen.flasks.text, tr("run_end.flasks") % 2, "the flasks full again")
	screen.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))
