extends "res://tests/test_case.gd"
## A talk on the map, as pyport's: the hero speaks by his own name, and the portrait of who
## speaks stands beside the line, just above the HUD.


func test_the_hero_speaks_by_his_name() -> void:
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	var p := Profile.new()
	p.hero_name = "Ann"
	p.apply_to(sim)
	eq(sim.hero_name, "Ann", "the hero's name")
	sim.set_general(1)
	MapTalks.start_map_talk(sim, 1)
	check(sim.talk[0].begins_with("[Zdzislaw Krzeminski]"), "the general first")
	check(not sim.hero_talks(), "he talks")
	eq(sim.talk[1], "[Ann] ...", "then the hero, by his name")
	sim.talk_line = 1
	check(sim.hero_talks(), "the hero talks")


## Met as a foe in battle, a general likes the hero less (not below 0), and his talk after that
## fight brings no friendship; another's talk does.
func test_a_fight_with_a_general_costs_friendship() -> void:
	var sim := MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	sim.friendship = {1: 20}
	sim.set_general(1)
	MapTalks.start_map_talk(sim, 1)
	eq(sim.friendship[1], 20 - MapTalks.FRIENDSHIP_PER_FIGHT, "less after the meeting")
	MapTalks.start_general_talk(sim, 1, 0)
	eq(sim.friendship[1], 20 - MapTalks.FRIENDSHIP_PER_FIGHT, "his talk after the fight: nothing")
	MapTalks.start_general_talk(sim, 5, 0)
	eq(sim.friendship[5], MapTalks.FRIENDSHIP_PER_TALK, "an ally's talk: more")
	sim.friendship[3] = 2
	MapTalks.start_map_talk(sim, 3)
	eq(sim.friendship[3], 0, "not below nothing")


func test_the_talk_shows_who_speaks() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = Router.make(Router.SCREENS["mission"])
	root.add_child(screen)
	screen._show_banner()
	check(not screen.talk_box.visible, "nobody talks")
	MapTalks.start_general_talk(screen.sim, 5, 0)
	for t in 3:
		screen.sim.tick(-1, -1)
	screen._show_banner()
	check(screen.talk_box.visible and not screen.banner.visible, "a talk, not a banner")
	eq(screen.talk_box.line.text, screen.sim.talk_text(), "the line as far as it is typed")
	var general := int(screen.sim.general.get("portrait", -1))
	check(
		screen.talk_box.portrait.texture.resource_path.ends_with("/%d.png" % general),
		"the general's portrait"
	)
	screen.sim.talk_line = 1
	screen._show_banner()
	check(
		screen.talk_box.portrait.texture.resource_path.ends_with(
			"/%d.png" % (38 + int(screen.profile.head))
		),
		"the hero's for his line"
	)
	var view: Vector2 = screen.get_viewport_rect().size
	var k: float = screen.hud.scale_of(view)
	var hud_top: float = view.y - (MapHud.PANEL_H + MapHud.BAR_H) * k
	eq(
		screen.talk_box.face.position.y + screen.talk_box.face.size.y,
		hud_top - 2 * k,
		"just above the HUD"
	)
	check(
		(
			screen.talk_box.box.position.x
			> screen.talk_box.face.position.x + screen.talk_box.face.size.x
		),
		"the line beside it"
	)
	screen.free()
	Router.params = old
