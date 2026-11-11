extends "res://tests/test_case.gd"
## The run (HeroRun): flasks of living water bought with fame, a lost mission spends one or ends
## the run, an ending back to the start ends it and one on to a main camp fills a flask.

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
	eq(int(p.skill_levels[0]), 1, "the first skill is back")
	eq(int(p.skill_levels[5]), 1, "and the second")
	eq(p.hotkeys, HeroRun.START_HOTKEYS, "on keys 1 and 2")
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


func test_the_town_hall_of_the_start_sells_flasks() -> void:
	var p := Profile.new()
	p.fame = int(HeroRun.FLASK_PRICES[0])
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH, "start": true}
	var hall: Control = Router.make(Router.SCREENS["town_hall"])
	root.add_child(hall)
	check(hall.buy.visible, "the start camp sells a flask")
	check(not hall.buy.disabled, "the fame is enough")
	hall.buy_flask()
	var q := Profile.load_or_new(TEST_PATH) as Profile
	eq(q.run.flasks, 1, "bought and saved")
	eq(q.fame, 0, "for its fame")
	check(hall.buy.disabled, "the next one costs more")
	hall.free()
	Router.params = {"profile_path": TEST_PATH, "start": false}
	hall = Router.make(Router.SCREENS["town_hall"])
	root.add_child(hall)
	check(not hall.buy.visible, "another camp sells none")
	check(hall.flasks.text.contains("1"), "but shows the flasks: %s" % hall.flasks.text)
	hall.free()
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
