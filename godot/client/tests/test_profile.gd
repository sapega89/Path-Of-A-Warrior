extends "res://tests/test_case.gd"

const Profile := preload("res://scripts/core/profile.gd")
const MapBuilder := preload("res://scripts/world/map_builder.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")
const Items := preload("res://scripts/core/items.gd")
const TEST_PATH := "user://test_hero.json"


func test_new_hero() -> void:
	var p := Profile.new()
	eq(p.level, 1, "level 1")
	eq(p.attack(), 6, "attack 5 and the claymore's 1")
	eq(p.defense(), 4, "defence 4")
	eq(p.max_hp(), 30, "30 HP")
	eq(p.max_mp(), 10, "10 MP")
	eq(p.stat_points, 5, "5 free points")


func test_exp_and_levels() -> void:
	var p := Profile.new()
	eq(Profile.exp_needed(1), 50, "50 exp to level 2")
	eq(p.level_with(160), 3, "50 + 104 exp: level 3")
	eq(p.gain_exp(160), 2, "two levels")
	eq(p.level, 3, "level 3")
	eq(p.experience, 6, "6 exp into level 3")
	eq(p.stat_points, 11, "3 points a level")


## The mission knows the places left in the Inventory (a gear found with none stays on the floor).
func test_the_mission_knows_the_places_left() -> void:
	var p := Profile.new()
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	p.apply_to(sim)
	var empty: int = sim.free_places
	check(empty > 0 and empty <= p.backpack.size(), "the places left: %d" % empty)
	p.add_item(Items.make(101))
	p.apply_to(sim)
	eq(sim.free_places, empty - 1, "a place less")


func test_mission_goes_in_and_out() -> void:
	var p := Profile.new()
	p.quick_slots[0] = [4, 2]
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	p.apply_to(sim)
	eq(sim.hero.attack, 6, "the hero's attack")
	eq(int(sim.quick_slots[0][1]), 2, "his potions")
	eq(sim.hero.weapon_kind, 1, "the claymore's sword type")
	sim.quick_slots[0][1] = 1  # one drunk
	sim.items.append(131)
	sim.gold = 30
	sim.friendship[5] = 10
	sim.won = true
	sim.mission_gold = 3
	sim.mission_exp = 30
	eq(p.take_from(sim, 1, 0, 1), 1, "60 exp: a level")
	eq(p.gold, 30 + 450, "picked up and the mission's gold")
	eq(int(p.quick_slots[0][1]), 1, "one potion left")
	eq(int(p.backpack[0].id), 131, "the helmet found")
	var def_bonus := int(p.backpack[0].defense)
	check(def_bonus >= 1 and def_bonus <= 3, "with its bonus and the random extra: %d" % def_bonus)
	eq(int(p.friendship["5"]), 10, "friendship kept")
	check(p.is_done(1, 0), "the mission is done")
	eq(int(p.progress["1"]), 5, "progress for the ruler")


func test_saved_and_loaded() -> void:
	var p := Profile.new()
	p.gold = 123
	p.gain_exp(60)
	p.friendship["5"] = 15
	check(p.save(TEST_PATH), "saved")
	var q: RefCounted = Profile.load_or_new(TEST_PATH)
	eq(q.gold, 123, "gold")
	eq(q.level, 2, "level")
	eq(q.experience, 10, "exp")
	eq(int(q.friendship["5"]), 15, "friendship")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))


func _sim_won(won: bool) -> RefCounted:
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	sim.won = won
	sim.mission_gold = 2
	return sim


func test_campaign_moves_on() -> void:
	var p := Profile.new()
	eq(p.place, 0, "a new hero starts at chapter 0")
	check(p.is_lord_open(1), "The Rise is open")
	check(not p.is_lord_open(8), "lord 8 is not open yet")
	eq(p.advance(_sim_won(false), 2, {"general": 6, "reward": 0}), -1, "a lost mission")
	eq(p.place, 0, "stays")
	eq(p.advance(_sim_won(true), 2, {"general": 6, "reward": 0}), -1, "a won mission")
	eq(p.place, 2, "goes to the lord's place")


func test_endings() -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 3
	var p := Profile.new()
	var open_before := p.lords_open
	eq(p.advance(_sim_won(true), 5, {"general": 202, "reward": 0}, rng), 2, "ending 2")
	check(p.endings & (1 << 2) != 0, "seen")
	eq(p.place, 0, "back to the start")
	check(p.has_item(Profile.SCARF), "Catherine's scarf")
	check(p.lords_open != open_before, "one more lord open")
	eq(p.advance(_sim_won(true), 9, {"general": 206, "reward": 0}, rng), 6, "ending 6")
	eq(p.place, 11, "its place")
	var q := Profile.new()
	q.gold = 0
	eq(q.advance(_sim_won(false), 1, {"general": 6, "reward": 210}, rng), 10, "ending 10 by losing")
	eq(q.gold, 300, "the mission's gold anyway (2 x 150 on normal)")
	eq(q.place, 15, "its place")
	var r := Profile.new()
	eq(r.advance(_sim_won(true), 5, {"general": 203, "reward": 0}, rng), 3, "ending 3")
	check(r.endings & (1 << 3) == 0, "not seen without the scarf")
	eq(r.place, 4, "back to chapter 4")
