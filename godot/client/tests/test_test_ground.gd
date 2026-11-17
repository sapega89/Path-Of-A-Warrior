extends "res://tests/test_case.gd"
## The test ground (screens/test_ground), opened from the main menu: a button for every map of
## the campaign; its mission is the map's own with a hero who takes no damage, PageUp / PageDown
## change the map, a mission won goes on to the next one, and nothing is saved.

## A hero's file the test ground must not write.
const PROFILE := "user://test_ground_hero.json"


func _press(action: String) -> void:
	for pressed: bool in [true, false]:
		var ev := InputEventAction.new()
		ev.action = action
		ev.pressed = pressed
		Input.parse_input_event(ev)
		Input.flush_buffered_events()


func _shown() -> Vector2i:
	return Vector2i(int(Router.params.get("lord", 0)), int(Router.params.get("mission", -1)))


func test_an_immortal_hero_takes_no_damage() -> void:
	var sim := MapSim.new(own_map("three_rooms"), 0, Vector2i(4, 2))
	var foe := MapActor.new()
	foe.type = MapSim.KIND_SWORDS
	foe.attack = 500
	foe.pos = sim.hero.pos + Vector2i(20, 0)
	var hp := sim.hero.hp
	sim.immortal = true
	MapHeroPlay.hero_is_hit(sim, foe)
	eq(sim.hero.hp, hp, "the HP stays")
	eq(sim.hero.action, 9, "the hit still shows")
	sim.immortal = false
	MapHeroPlay.hero_is_hit(sim, foe)
	eq(sim.hero.action, 10, "a hero who is not immortal falls")


func test_a_button_for_every_map_from_the_main_menu() -> void:
	var host := Control.new()
	root.add_child(host)
	Router.attach(host)
	Router.go("main_menu")
	(Router.current as MainMenu).open_test_ground()
	eq(Router.current_name(), "test_ground", "the test ground")
	var ground: TestGroundScreen = Router.current
	eq(ground.maps.get_child_count(), MapBuilder.map_count(), "a button a map")
	var first: Button = ground.maps.get_child(0)
	eq(first.text, "1. " + Campaign.new().lord_name(1), "its number and place")
	(ground.maps.get_child(2) as Button).pressed.emit()
	eq(Router.current_name(), "test_mission", "a button opens its map")
	var test: TestMissionScreen = Router.current
	eq(Vector2i(test.lord_id, test.mission), Vector2i(3, 0), "the first mission of map 3")
	check(test.sim.immortal, "the hero cannot die")
	check(test.auto_allowed(), "AUTO")
	check(test.where.text.begins_with(tr("test_ground.where").left(4)), "the line on top")
	Router.back()
	eq(Router.current_name(), "test_ground", "back to the maps")
	eq(int(Router.params.get("map", 0)), 3, "the map opened last is kept")
	Router.attach(null)
	host.free()


func test_a_mission_won_goes_on_and_the_keys_change_the_map() -> void:
	var host := Control.new()
	root.add_child(host)
	Router.attach(host)
	Router.go("test_ground")
	Router.push("test_mission", {"lord": 1, "mission": 0, "profile_path": PROFILE})
	var test: TestMissionScreen = Router.current
	test.sim.won = true
	test.sim.finished = true
	test._process(0.0)
	eq(_shown(), Vector2i(1, 1), "a mission won: the next one of the map")
	check(not FileAccess.file_exists(PROFILE), "nothing saved")
	_press("map_prev")
	eq(_shown(), Vector2i(MapBuilder.map_count(), 0), "before the first map, the last")
	_press("map_next")
	eq(_shown(), Vector2i(1, 0), "after the last, the first")
	_press("map_next")
	eq(_shown(), Vector2i(2, 0), "the next map")
	eq(Router.depth(), 2, "the maps under it still")
	var last := Campaign.new().lord_missions(1).size() - 1
	eq(TestMissionScreen.mission_after(1, last), Vector2i(2, 0), "after a map's last mission")
	var end := MapBuilder.map_count()
	last = Campaign.new().lord_missions(end).size() - 1
	eq(TestMissionScreen.mission_after(end, last), Vector2i(1, 0), "and after the last map's")
	Router.attach(null)
	host.free()
