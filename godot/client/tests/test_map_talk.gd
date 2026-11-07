extends "res://tests/test_case.gd"
## A talk on the map, as pyport's: the hero speaks by his own name, and the portrait of who
## speaks stands beside the line, just above the HUD.

const MapSim := preload("res://scripts/sim/map_sim.gd")
const MapBuilder := preload("res://scripts/world/map_builder.gd")
const MissionScreen := preload("res://scripts/screens/mission_screen.gd")
const Profile := preload("res://scripts/core/profile.gd")
const MapHud := preload("res://scripts/ui/map_hud.gd")


func test_the_hero_speaks_by_his_name() -> void:
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	var p := Profile.new()
	p.hero_name = "Ann"
	p.apply_to(sim)
	eq(sim.hero_name, "Ann", "the hero's name")
	sim.set_general(1)
	sim._start_map_talk()
	check(sim.talk[0].begins_with("[Waclaw Krzeminski]"), "the general first")
	check(not sim.hero_talks(), "he talks")
	eq(sim.talk[1], "[Ann] ...", "then the hero, by his name")
	sim.talk_line = 1
	check(sim.hero_talks(), "the hero talks")


func test_the_talk_shows_who_speaks() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = MissionScreen.new()
	root.add_child(screen)
	screen._show_banner()
	check(not screen.talk_box.visible, "nobody talks")
	screen.sim._start_general_talk(5, 0)
	for t in 3:
		screen.sim.tick(-1, -1)
	screen._show_banner()
	check(screen.talk_box.visible and not screen.banner.visible, "a talk, not a banner")
	eq(screen.talk_text.text, screen.sim.talk_text(), "the line as far as it is typed")
	var general := int(screen.sim.general.get("portrait", -1))
	check(screen.talk_portrait.texture.resource_path.ends_with("/%d.png" % general), "the general's portrait")
	screen.sim.talk_line = 1
	screen._show_banner()
	check(screen.talk_portrait.texture.resource_path.ends_with("/%d.png" % (38 + int(screen.profile.head))),
		"the hero's for his line")
	var view: Vector2 = screen.get_viewport_rect().size
	var k: float = screen.hud.scale_of(view)
	var hud_top: float = view.y - (MapHud.PANEL_H + MapHud.BAR_H) * k
	eq(screen.talk_face.position.y + screen.talk_face.size.y, hud_top - 2 * k, "just above the HUD")
	check(screen.talk_panel.position.x > screen.talk_face.position.x + screen.talk_face.size.x, "the line beside it")
	screen.free()
	Router.params = old

