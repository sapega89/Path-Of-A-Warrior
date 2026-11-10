extends "res://tests/test_case.gd"

const TEST_PATH := "user://test_visits.json"


func test_data() -> void:
	eq(Visits.data().get("lines", []).size(), 76, "76 lines")
	eq(Visits.data().get("generals", []).size(), 44, "44 generals one can visit")
	eq(Visits.line(0), "Good day.", "the first greeting")


func test_a_won_mission_allows_a_visit() -> void:
	var p := Profile.new()
	check(not Visits.can_visit(p), "a new hero has no one to invite")
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	p.apply_to(sim)
	sim.friendship[4] = 10
	p.take_from(sim, 1, 0, 1)
	check(not Visits.can_visit(p), "a lost mission does not")
	sim.won = true
	p.take_from(sim, 1, 0, 1)
	check(Visits.can_visit(p), "a won one with a friend does")
	check(p.save(TEST_PATH), "saved")
	check(Profile.load_or_new(TEST_PATH).can_visit, "and it is kept")
	eq(Visits.generals(p), [[4, 10]], "the friend and his points")
	p.add_item(
		{"id": Visits.SEAL, "attack": 0, "defense": 0, "hp": 0, "mp": 0, "enchant": 0, "extra": 0}
	)
	eq(Visits.generals(p).size(), 44, "with the Hetman's Seal all of them")
	eq(Visits.generals(p)[0], [4, 10], "points of a friend")
	eq(Visits.generals(p)[1], [5, 0], "0 for one not met")


func test_greetings_by_friendship() -> void:
	var g := Visits.greeting(0, 0, "Hero", "Jan Gorski")
	eq(
		g,
		["[Hero] Good day.", "[Jan Gorski] Good day to you.", "[Hero] Thank you for having me."],
		"the coolest"
	)
	eq(Visits.greeting(100, 0, "H", "K")[0], "[H] " + Visits.line(27), "100 points: the warmest")
	eq(Visits.greeting(15, 1, "H", "K")[0], "[H] " + Visits.line(33), "a general of topic 1")
	eq(
		Visits.talk(0, 0, "H", "K"),
		["[H] Nobody handles a sabre the way you do!", "[K] Thanks."],
		"the sword"
	)
	eq(Visits.talk(1, 3, "H", "K")[1], "[K] That is a generous heart you have.", "people, topic 1")


func test_friendship() -> void:
	var p := Profile.new()
	check(not Visits.add_friendship(p, 3, 5), "a general one cannot visit is not added")
	check(not Visits.add_friendship(p, 4, 5), "one who can")
	eq(int(p.friendship["4"]), 5, "with 5 points")
	p.friendship["4"] = 98
	check(Visits.add_friendship(p, 4, 5), "100 reached")
	eq(int(p.friendship["4"]), 100, "and kept at 100")
	Visits.add_friendship(p, 4, -100)
	check(not p.friendship.has("4"), "at 0 he leaves")


func test_gifts() -> void:
	var p := Profile.new()
	var rng := RandomNumberGenerator.new()
	var g := MapSim.general_data(4)
	p.friendship["4"] = 0
	eq(int(Visits.give_gift(p, 4, g, 0, rng).kind), Visits.Gift.NONE, "no friendship, no gift")
	p.friendship["4"] = 100
	var kinds := {}
	var hp := p.base_hp
	for i in 300:
		rng.seed = i
		var gift := Visits.give_gift(p, 4, g, 2, rng)
		kinds[int(gift.kind)] = true
		check(
			int(gift.kind) == Visits.Gift.NONE or not str(gift.text).is_empty(),
			"a gift has a name: %s" % gift
		)
	check(
		kinds.has(Visits.Gift.SKILL) and kinds.has(Visits.Gift.ATTACK),
		"skills and attack about tactics"
	)
	check(p.base_attack > Profile.BASE_ATTACK, "attack given")
	check(p.base_hp >= hp, "HP not lost")
	eq((Visits.gift_gear(1, rng) - 101) % 5 <= 1, true, "a new hero gets low tiers")


func test_visiting_screen() -> void:
	var p := Profile.new()
	p.friendship["4"] = 100
	p.can_visit = true
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH, "seed": 1}
	var screen: Control = Router.make(Router.SCREENS["visiting"])
	root.add_child(screen)
	eq(screen.list.get_child_count(), 3, "the header, Jan Gorski, Back")
	screen.open(4)
	eq(screen.step, VisitingScreen.Step.GREETING, "he greets")
	eq(screen.hero_says.visible_characters, 0, "typed out")
	var click := InputEventMouseButton.new()
	click.button_index = MOUSE_BUTTON_LEFT
	click.pressed = true
	screen._gui_input(click)  # a click beside the buttons, as OK
	for i in 5:
		screen.press()
	eq(screen.step, VisitingScreen.Step.TOPIC, "then the question")
	check(screen.topics.visible, "with four topics")
	screen.choose(2)
	eq(screen.step, VisitingScreen.Step.TALK, "they talk")
	for i in 4:
		screen.press()
	eq(screen.step, VisitingScreen.Step.DISCUSSED, "what was discussed")
	check(screen.text.text.contains("Tactics"), screen.text.text)
	screen.press()
	eq(screen.step, VisitingScreen.Step.VISITED, "the visit's end")
	check(
		screen.text.text.begins_with("You visited Jan Gorski.\nFriendship:100%"), screen.text.text
	)
	var saved: RefCounted = Profile.load_or_new(TEST_PATH)
	check(not saved.can_visit, "one visit per mission")
	screen.free()
	Router.params = old
	Router.params = {"profile_path": TEST_PATH}
	screen = Router.make(Router.SCREENS["visiting"])
	root.add_child(screen)
	eq(str(screen.list.get_child(0).name), "Notice", "not now")
	screen.free()
	Router.params = old


## As pyport's: a line typed out goes on by itself after 15 ticks, the last greeting to the
## topics and the last line of the talk to what was discussed.
func test_visiting_talk_goes_on_by_itself() -> void:
	var p := Profile.new()
	p.friendship["4"] = 100
	p.can_visit = true
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH, "seed": 1}
	var screen: Control = Router.make(Router.SCREENS["visiting"])
	root.add_child(screen)
	var wait: float = VisitingScreen.WAIT_TICKS * Settings.tick_seconds()
	screen.open(4)
	screen._process(100.0)
	eq(screen.hero_says.visible_characters, -1, "the line typed out")
	screen._process(wait * 0.5)
	eq(screen.line_at, 0, "it stays a moment")
	screen._process(wait)
	eq([screen.line_at, screen.typing], [1, screen.general_says], "then the general's line")
	for i in 10:
		screen._process(100.0)
	eq(screen.step, VisitingScreen.Step.TOPIC, "the greeting over: the question")
	screen._process(100.0)
	eq(screen.step, VisitingScreen.Step.TOPIC, "which waits for a topic")
	screen.choose(2)
	screen.press()
	eq(screen.typing.visible_characters, -1, "a press: the whole line")
	screen.press()
	eq(screen.line_at, 1, "another: the next one at once")
	for i in 10:
		screen._process(100.0)
	eq(screen.step, VisitingScreen.Step.DISCUSSED, "the talk over: what was discussed")
	screen._process(100.0)
	eq(screen.step, VisitingScreen.Step.DISCUSSED, "which waits for OK")
	screen.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))
