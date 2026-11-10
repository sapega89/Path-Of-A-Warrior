extends "res://tests/test_case.gd"
## The world map of the campaign: 45 places joined by the ways of campaign.json, and the
## rooms a mission walks on its place's map.

const RouterScript := preload("res://scripts/core/router.gd")
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
		for place in 46:
			check(
				CampMap.new(ways, false, place).all_reachable(),
				(
					"%d ways at place %d: the things about the camp leave every way and spot free"
					% [n, place]
				)
			)
		for e in c.exits:
			for p in e.gap:
				var f: int = c.data.flags[p.y * CampMap.W + p.x]
				eq(f & 1 == 0, bool(e.open), "an open way is free, a closed one fenced")
			eq(
				int(c.data.flags[e.inside.y * CampMap.W + e.inside.x]) & 1,
				0,
				"its colonel stands on free ground"
			)
	check(CampMap.is_main(0) and CampMap.is_main(30) and not CampMap.is_main(27), "the main camps")
	var plain: RefCounted = CampMap.new([[1, true]])
	for spot in [plain.smith_spot(), plain.store_spot(), plain.hall_door(), plain.start]:
		eq(
			int(plain.data.flags[spot.y * CampMap.W + spot.x]) & 1,
			0,
			"the blacksmith, the stores, the hall and the start can be reached"
		)
	eq(plain.data.upper[0], CampMap.TREE[0][0], "a big tree in the corner")


func test_camp_screen_ways_lead_to_the_missions() -> void:
	var p: RefCounted = Profile.new()
	p.place = 4
	p.save(CAMP_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": CAMP_PATH}
	var camp: Control = Router.make(Router.SCREENS["camp"])
	root.add_child(camp)
	eq(camp.place, 4, "the camp of the hero's place")
	eq(
		camp.spots.map(func(s): return s.kind),
		["way", "way", "smith", "store", "hall"],
		"a way per place on, then the blacksmith, the warehouse and the town hall in every camp"
	)
	var ways: Array = camp.spots.filter(func(s): return s.kind == "way")
	var open: Array = ways.filter(func(s): return s.open)
	eq(
		ways.filter(func(s): return not s.open).map(func(s): return s.place),
		[5],
		"The Regalia fenced"
	)
	eq(open.map(func(s): return [s.place, s.mission]), [[6, 0]], "Harvest, its first mission")
	check(not camp.camp.main, "Korsun is a stop")
	var harvest: Dictionary = open[0]
	eq(camp.spot_near(harvest.at + Vector3(0.5, 0, 0.5)), harvest, "next to the way in")
	eq(camp.spot_near(Vector3(8.5, 0, 10.5)), {}, "far from everyone")
	var k: int = camp.spots.find(harvest)
	var e: Dictionary = camp.camp.exits[k]
	var out := Vector3(e.gap[1].x + 0.5, 0, 0.3)
	if int(e.side) == 1:
		out = Vector3(CampMap.W - 0.3, 0, e.gap[1].y + 0.5)
	elif int(e.side) == 2:
		out = Vector3(0.3, 0, e.gap[1].y + 0.5)
	eq(camp.exit_crossed(out), harvest, "out through the gap")
	eq(camp.exit_crossed(Vector3(8.5, 0, 6.0)), {}, "inside")
	var smith: Dictionary = camp.spots[2]
	eq(camp.spot_near(smith.at), smith, "at the blacksmith's fire")
	check(camp._hint_text(smith).contains(tr("menu.blacksmith")), "says what is there")
	check(camp.rulers(1).size() == 4, "four colonels give the missions at Uprising")
	eq(camp.arrows.size(), 1, "an arrow on the open way only")
	check(
		camp.world.get_children().any(func(n): return str(n.name).begins_with("Land")),
		"the land of the places past the gaps"
	)
	p.done["6:0"] = true
	camp.profile = p
	var again: Array = camp.choices().filter(func(w): return w[1])
	eq(again, [[6, true, 1]], "the next mission not won yet")
	camp.place = 27
	eq(
		camp.choices().map(func(w): return w[0]).size(),
		camp.world_map.next_places(27).size(),
		"one way per place on"
	)
	eq(CampScreen.terrain(33), "mountains", "Chyhyryn's hills")
	eq(CampScreen.terrain(19), "forest", "a forest")
	eq(CampScreen.terrain(24), "lake", "down the Dnipro")
	eq(CampScreen.terrain(2), "steppe", "the steppe")
	camp.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(CAMP_PATH))


func test_a_room_shows_only_itself_and_the_next() -> void:
	var map: Dictionary = MapBuilder.load_map(6)
	var rooms: RefCounted = Rooms.new(map, 0)
	var next: Array = rooms.next_rooms(0)
	check(not next.is_empty(), "the first room leads on")
	var cells: Dictionary = rooms.view_cells(0)
	check(cells.has(Vector2i(4, 4)), "its own tiles")
	var p: Vector2i = rooms.room_xy(next[0])
	check(cells.has(Vector2i(7 * p.x + 4, 7 * p.y + 4)), "the next room's tiles")
	for r in rooms.count():
		if r != 0 and not r in next:
			var q: Vector2i = rooms.room_xy(r)
			check(not cells.has(Vector2i(7 * q.x + 4, 7 * q.y + 4)), "not room %d" % r)
	var b: Node3D = MapBuilder.new()
	root.add_child(b)
	b.build(map)
	b.show_only(cells)
	for r in rooms.count():
		var q: Vector2i = rooms.room_xy(r)
		eq(
			b.is_shown(7 * q.x + 4, 7 * q.y + 4),
			r == 0 or r in next,
			"room %d drawn only if current or next" % r
		)
	b.free()


func test_after_a_mission_won_the_way_on_is_chosen_in_the_room() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 4, "mission": 0, "seed": 2}
	var screen: Control = Router.make(Router.SCREENS["mission"])
	root.add_child(screen)
	var p: RefCounted = Profile.new()
	screen.profile = p
	eq(
		screen.ways_on(4).map(func(w): return w.place),
		[6],
		"Korsun: Harvest only, The Regalia is closed"
	)
	p.lords_open = -1
	var two: Array = screen.ways_on(4)
	eq(two.map(func(w): return w.place), [5, 6], "both open: a way each")
	check(
		two[0].exit != two[1].exit and two.all(func(w): return w.half == -1),
		"each on a side of its own"
	)
	var six: Array = screen.ways_on(27)
	eq(six.size(), 6, "six places on from Dawn over the Dnipro")
	eq(six.filter(func(w): return w.half != -1).size(), 4, "two sides carry two ways")
	screen.ways_out = six
	var mid: Vector3 = screen.sim.rooms.center(screen.sim.cell)
	var seen := {}
	for w in six:
		var off := -1.0 if int(w.half) == 0 else 1.0
		if int(w.half) == -1:
			off = 0.0
		var at := (
			mid
			+ (
				Vector3(off, 0, 0)
				if int(w.exit) in [Rooms.EXIT_UP, Rooms.EXIT_DOWN]
				else Vector3(0, 0, off)
			)
		)
		eq(screen.way_for(int(w.exit), at), int(w.place), "the way to %d" % w.place)
		seen[w.place] = true
	eq(seen.size(), 6, "every place has its way")
	var sim: RefCounted = screen.sim
	sim.start_choosing()
	check(sim.choosing and not sim.finished and sim.enemies.is_empty(), "the room is quiet")
	sim.keep_in_room(sim.hero.pos, 0, -2000)
	eq(sim.way_out, Rooms.EXIT_UP, "walked into the top side")
	screen.free()
	Router.params = old


func test_the_camp_of_the_way_chosen_offers_its_generals() -> void:
	var p: RefCounted = Profile.new()
	p.place = 1
	p.heading = 2
	p.save(CAMP_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": CAMP_PATH}
	var camp: Control = Router.make(Router.SCREENS["camp"])
	root.add_child(camp)
	var ways: Array = camp.spots.filter(func(s): return s.kind == "way")
	var n: int = camp.campaign.lord_missions(2).size()
	eq(ways.size(), n, "a way per mission of the place chosen")
	check(ways.all(func(s): return s.place == 2 and s.open), "all of it, all open")
	eq(camp.camp_place(), 2, "the camp is that place's")
	camp.free()
	Router.params = old
	var back: RefCounted = Profile.load_or_new(CAMP_PATH)
	eq(back.heading, 2, "the way chosen is kept")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(CAMP_PATH))


## The town hall names every colonel; how far the hero has come with one only once it is
## something.
func test_town_hall_colonels_without_zero() -> void:
	Profile.new().save(CAMP_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": CAMP_PATH}
	var hall: Control = Router.make(Router.SCREENS["town_hall"])
	root.add_child(hall)
	var lines: Array = hall.list.get_node("Colonels").get_children()
	eq(lines.size(), hall.colonels().size(), "a line per colonel")
	for l in lines:
		check(not (l as Label).text.contains("%"), "no 0% for a colonel the hero has not won with")
	var first: Array = hall.colonels()[0]
	eq(hall.colonel_line(first), tr(str(first[1])), "only his name")
	hall.profile.progress[str(first[0])] = 15
	eq(
		hall.colonel_line(first),
		tr("hall.progress") % [tr(str(first[1])), 15],
		"15% once he has won with him"
	)
	hall.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(CAMP_PATH))
