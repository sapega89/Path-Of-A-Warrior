extends "res://tests/test_case.gd"
## The world map of the campaign: 45 places joined by the ways of campaign.json, and the
## rooms a mission walks on its place's map.

const WorldMap := preload("res://scripts/core/world_map.gd")
const WorldMapView := preload("res://scripts/ui/world_map_view.gd")
const Rooms := preload("res://scripts/world/rooms.gd")
const MapBuilder := preload("res://scripts/world/map_builder.gd")
const Profile := preload("res://scripts/core/profile.gd")
const RouterScript := preload("res://scripts/core/router.gd")
const CampMap := preload("res://scripts/world/camp_map.gd")
const CampScreen := preload("res://scripts/screens/camp_screen.gd")
const CAMP_PATH := "user://test_camp.json"


func test_places_and_ways() -> void:
	var w: RefCounted = WorldMap.new()
	eq(w.place_count(), 45, "45 places, one per map")
	eq(w.ways().size(), 68, "68 ways between them (and one in from the start)")
	eq(w.next_places(0), [1], "the start leads to Uprising")
	eq(w.next_places(4), [5, 6], "Korsun forks")
	eq(w.next_places(45), [], "The Duma is the last")
	eq(w.comes_from(24), [22, 23, 25, 26], "four ways into Down the Dnipro")


func test_layout_goes_one_way() -> void:
	var w: RefCounted = WorldMap.new()
	eq(w.cells.size(), 45, "every place has a cell")
	for way in w.ways():
		check(w.cells[way[1]].x > w.cells[way[0]].x, "the way %d -> %d goes right" % way)
	eq(w.cells[1].x, 0.0, "Uprising in the first column")
	var seen := {}
	for id in w.cells:
		var key := str(w.cells[id])
		check(not seen.has(key), "two places in one cell: %s" % key)
		seen[key] = true
	check(w.columns >= 20 and w.rows <= 8, "%d columns, %d rows" % [w.columns, w.rows])


func test_state_follows_the_hero() -> void:
	var w: RefCounted = WorldMap.new()
	var p: RefCounted = Profile.new()
	eq(w.state(1, 0, p), WorldMap.State.NEXT, "a new hero can go to Uprising")
	eq(w.state(2, 0, p), WorldMap.State.AWAY, "not further")
	p.place = 4
	eq(w.state(4, 4, p), WorldMap.State.HERE, "his place")
	eq(w.state(5, 4, p), WorldMap.State.CLOSED, "The Regalia is closed for a new hero")
	eq(w.state(6, 4, p), WorldMap.State.NEXT, "Harvest is open")
	p.done["1:0"] = true
	p.done["1:2"] = true
	eq(w.won(1, p), Vector2i(2, 4), "two of Uprising's four missions won")


func test_campaign_screen_opens_a_place_from_the_map() -> void:
	var host := Control.new()
	host.size = Vector2(1280, 720)
	root.add_child(host)
	var r: Node = RouterScript.new()
	r.attach(host)
	r.go("campaign", {"profile_path": "user://test_world_map.json"})
	var screen: Node = r.current
	var view: Control = screen.world_view
	check(view.visible, "level 1 is the world map")
	eq(view.buttons.size(), 45, "a button per place")
	check(view.can_choose(1) and not view.can_choose(2), "only Uprising for a new hero")
	view.buttons[2].pressed.emit()
	eq(screen.level, 1, "a place further on does not open")
	view.buttons[1].pressed.emit()
	eq([screen.level, screen.lord_id], [2, 1], "Uprising opens its missions")
	check(not view.visible, "the map hides")
	screen._open_mission(0)
	check(screen.list.get_node_or_null("Description") != null, "a mission shows its story")
	r.free()
	host.free()
	DirAccess.remove_absolute(ProjectSettings.globalize_path("user://test_world_map.json"))


func test_camp_map_has_a_gap_per_way() -> void:
	for n in range(0, 7):
		var ways: Array = []
		for i in n:
			ways.append([i + 1, i != 1])
		var c: RefCounted = CampMap.new(ways)
		eq(c.exits.size(), n, "%d ways, %d gaps" % [n, n])
		for e in c.exits:
			for p in e.gap:
				var f: int = c.data.flags[p.y * CampMap.W + p.x]
				eq(f & 1 == 0, bool(e.open), "an open way is free, a closed one fenced")
			eq(int(c.data.flags[e.inside.y * CampMap.W + e.inside.x]) & 1, 0, "its colonel stands on free ground")
	check(CampMap.is_main(0) and CampMap.is_main(30) and not CampMap.is_main(27), "the main camps")
	var plain: RefCounted = CampMap.new([[1, true]])
	for spot in [plain.smith_spot(), plain.store_spot(), CampMap.GUEST_AT]:
		eq(int(plain.data.flags[spot.y * CampMap.W + spot.x]) & 1, 0, "the blacksmith, the stores and the guest can be reached")
	var main: RefCounted = CampMap.new([[1, true]], true)
	eq(int(main.data.flags[main.hall_door().y * CampMap.W + main.hall_door().x]) & 1, 0, "the hall's door is free")


func test_camp_screen_ways_lead_to_the_missions() -> void:
	var p: RefCounted = Profile.new()
	p.place = 4
	p.save(CAMP_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": CAMP_PATH}
	var camp: Control = CampScreen.new()
	root.add_child(camp)
	eq(camp.place, 4, "the camp of the hero's place")
	eq(camp.spots.map(func(s): return s.kind), ["way", "way", "smith", "store"],
		"the ways, the blacksmith and the warehouse in every camp; no guest without a won mission")
	eq(camp.spots.slice(0, 2).map(func(s): return [s.place, s.open]), [[5, false], [6, true]],
		"Korsun: The Regalia closed, Harvest open")
	check(not camp.camp.main, "Korsun is a stop")
	var harvest: Dictionary = camp.spots[1]
	eq(camp.spot_near(harvest.at + Vector3(0.5, 0, 0.5)), harvest, "next to the colonel")
	eq(camp.spot_near(Vector3(8.5, 0, 10.5)), {}, "far from everyone")
	var gap: Vector2i = camp.camp.exits[1].gap[1]
	eq(camp.exit_crossed(Vector3(gap.x + 0.5, 0, 0.3)), harvest, "out through the gap")
	eq(camp.exit_crossed(Vector3(8.5, 0, 6.0)), {}, "inside")
	var smith: Dictionary = camp.spots[2]
	eq(camp.spot_near(smith.at), smith, "at the blacksmith's fire")
	check(camp._hint_text(smith).contains(tr("menu.blacksmith")), "says what is there")
	check(camp.rulers(1).size() == 4, "four colonels give the missions at Uprising")
	eq(camp.arrows.size(), 1, "an arrow on the open way only")
	for i in 20:
		var m: int = camp.pick_mission(6)
		check(m == 0 or m == 1, "a mission of Harvest")
	p.done["6:0"] = true
	camp.profile = p
	eq(camp.pick_mission(6), 1, "not one won already")
	camp.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(CAMP_PATH))
