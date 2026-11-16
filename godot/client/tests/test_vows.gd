extends "res://tests/test_case.gd"
## The vows of a run (Vows), taken in the start camp once an ending has led back there: tougher
## enemies, a shorter time limit, no potions from the shop, no flasks; each adds 10% to the gold
## and the fame of the run. And the roads the endings open (Profile.ROAD_OF_ENDING).

const TEST_PATH := "user://test_vows.json"


func _sim(won: bool) -> MapSim:
	var sim := MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	sim.won = won
	return sim


func test_the_vows_open_after_an_ending_back_to_the_start() -> void:
	var p := Profile.new()
	check(not Vows.open(p), "a new hero has none")
	p.endings |= 1 << 6
	check(not Vows.open(p), "ending 6 goes on to a main camp")
	p.endings |= 1 << 2
	check(Vows.open(p), "ending 2 led back to the start")


func test_taking_and_giving_up_the_vows() -> void:
	var v := Vows.new()
	eq(v.bonus_percent(), 100, "none taken")
	for step in Vows.MAX_HP_STEPS:
		v.next_hp_step()
	eq(v.enemy_hp_percent(), 100 + Vows.HP_STEP * Vows.MAX_HP_STEPS, "the last step")
	v.next_hp_step()
	eq(v.hp_steps, 0, "and back to none")
	v.next_hp_step()
	check(v.switch("short_time"), "the short time")
	check(v.switch("no_flasks"), "no flasks")
	check(not v.switch("no_hero"), "no such vow")
	eq(v.count(), 3, "a step and two vows")
	eq(v.bonus_percent(), 130, "+10% each")
	eq(v.time_limit(400), 300, "a quarter of the time gone")
	check(v.switch("no_flasks"), "given up")
	check(not v.has("no_flasks"), "no more")
	eq(Vows.new().time_limit(400), 400, "the whole time without the vow")


func test_the_vows_are_saved() -> void:
	var p := Profile.new()
	p.run.vows.next_hp_step()
	p.run.vows.next_hp_step()
	p.run.vows.switch("no_shop_potions")
	check(p.save(TEST_PATH), "saved")
	var q := Profile.load_or_new(TEST_PATH)
	eq(q.run.vows.hp_steps, 2, "the steps")
	check(q.run.vows.has("no_shop_potions"), "and the vow")
	var bad := Vows.new()
	bad.from_dict({"hp_steps": 9, "taken": ["no_hero", "short_time"]})
	eq(bad.hp_steps, Vows.MAX_HP_STEPS, "no more steps than there are")
	eq(bad.taken.keys(), ["short_time"], "only the vows there are")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))


func test_the_mission_under_the_vows() -> void:
	var p := Profile.new()
	p.run.vows.next_hp_step()
	p.run.vows.next_hp_step()
	p.run.vows.switch("short_time")
	var sim := _sim(false)
	sim.time_limit = 600
	p.apply_to(sim)
	eq(sim.enemy_hp_percent, 140, "the enemies +40% HP")
	eq(sim.time_limit, 450, "the time limit")
	var e := MapActor.new()
	MapEnemyPlay.enemy_stats(sim, e, 0)
	eq(e.hp, (int(MapEnemyPlay.BASE_HP[0]) + 3 * e.level) * 140 / 100, "a soldier's HP")
	eq(e.max_hp, e.hp, "full")


func test_the_vows_add_to_the_gold_and_the_fame() -> void:
	var plain := Profile.new()
	var vowed := Profile.new()
	vowed.run.vows.switch("short_time")
	vowed.run.vows.switch("no_flasks")
	var reward := 0
	for p: Profile in [plain, vowed]:
		p.gold = 0
		var sim := _sim(true)
		sim.gold = 100
		sim.mission_gold = 50
		sim.mission_exp = 200
		reward = sim.gold_reward()
		p.take_from(sim, 1, 0, 1, RandomNumberGenerator.new())
	check(reward > 0, "the mission pays")
	eq(plain.gold, 100 + reward, "the gold as it is")
	eq(vowed.gold, 120 + reward * 120 / 100, "+20% gold")
	eq(vowed.fame, plain.fame + 200 * 20 / 100, "+20% fame")


func test_no_flasks_and_no_shop_potions() -> void:
	var p := Profile.new()
	p.place = 3
	p.run.flasks = 2
	p.run.flasks_left = 2
	p.run.vows.switch("no_flasks")
	var lost := p.run.lose_mission(p, false, JavaRandom.new(1))
	check(bool(lost.over), "the first lost mission ends the run")
	eq(p.place, 0, "back to the start")
	Blacksmith.fill_shop(p, RandomNumberGenerator.new())
	p.gold = 100000
	p.run.vows.switch("no_shop_potions")
	eq(Blacksmith.buy(p, 0), "vow", "no potion from the shop")
	eq(Blacksmith.buy(p, Items.SHOP_POTIONS.size()), "bought", "a gear still")


func test_the_endings_open_their_roads() -> void:
	var rng := RandomNumberGenerator.new()
	for ending: int in Profile.ROAD_OF_ENDING:
		var road := int(Profile.ROAD_OF_ENDING[ending])
		var p := Profile.new()
		var info := {"general": Profile.ENDING_BASE + ending, "reward": 0}
		check(not p.is_lord_open(road), "place %d closed at the start" % road)
		p.advance(_sim(true), 5, info, rng)
		if ending == 3:
			check(not p.is_lord_open(road), "ending 3 unseen without the scarf opens nothing")
			p.add_item(Items.make(Profile.SCARF))
			p.advance(_sim(true), 5, info, rng)
		check(p.is_lord_open(road), "ending %d opens place %d" % [ending, road])
		eq(p.opened_lord, road, "and says so")
	var q := Profile.new()
	var open_before := q.lords_open
	q.advance(_sim(true), 9, {"general": Profile.ENDING_BASE + 6, "reward": 0}, rng)
	eq(q.lords_open, open_before, "ending 6 opens no road")


func test_the_vows_on_the_run_setup_screen() -> void:
	var p := Profile.new()
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var screen: RunSetupScreen = Router.make(Router.SCREENS["run_setup"])
	root.add_child(screen)
	check(not screen.vow_list.visible, "no vows before an ending back to the start")
	screen.free()
	p.endings |= 1 << 2
	p.save(TEST_PATH)
	screen = Router.make(Router.SCREENS["run_setup"])
	root.add_child(screen)
	check(screen.vow_list.visible, "then they are there")
	eq(screen.vows_title.text, tr("run_setup.vows") % 0, "nothing added yet")
	screen.vow_list.get_node("Hp").pressed.emit()
	screen.vow_list.get_node("ShortTime").pressed.emit()
	var q := Profile.load_or_new(TEST_PATH)
	eq(q.run.vows.hp_steps, 1, "a step saved")
	check(q.run.vows.has("short_time"), "and the short time")
	eq(screen.vows_title.text, tr("run_setup.vows") % 20, "+20%")
	eq(
		screen.vow_list.get_node("ShortTime").text,
		tr("vow.on") % tr("vow.short_time"),
		"the vow shows it is taken"
	)
	eq(screen.vow_list.get_node("Hp").text, tr("vow.hp") % [1, Vows.MAX_HP_STEPS], "the step")
	screen.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))
