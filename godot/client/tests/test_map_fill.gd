extends "res://tests/test_case.gd"
## What stands in the rooms of the generated maps and the ground under it (scripts/mapgen/:
## RoomFill and GroundPaint, by the biomes of data/map_rules.json), on the map of every place:
## the middles of the rooms of the routes stay free for the fight, wider where generals fight;
## nothing tall stands in front of a fight; each fir of a column shows; the ground takes the
## shares the biome gives it, with the path, the water and its banks; the lab
## (lab/map_gen_lab.tscn) shows the maps.

## The maps made, by place: each made once for all the tests here.
static var _made := {}


func _map(place: int) -> Dictionary:
	if not _made.has(place):
		_made[place] = MapGenerator.new().make(MapPlan.of(place))
	return _made[place]


func _places() -> Array:
	return range(1, MapBuilder.map_count() + 1)


## The rooms on the routes of a map's missions, and the rooms where generals fight.
func _rooms(plan: MapPlan, layout: RoomLayout) -> Array[Dictionary]:
	var on_route := {}
	var arenas := {}
	for m in layout.routes.size():
		for room: int in layout.routes[m]:
			on_route[room] = true
		for i in layout.stops[m].size():
			if not plan.missions[m][i].generals.is_empty():
				arenas[layout.routes[m][layout.stops[m][i]]] = true
	return [on_route, arenas]


func _free(map: Dictionary, c: Vector2i) -> bool:
	var i := c.y * int(map.w) + c.x
	return int(map.flags[i]) & 1 == 0 and int(map.objects[i]) == 0


func test_the_middles_stay_free() -> void:
	for n: int in _places():
		var plan := MapPlan.of(n)
		var map := _map(n)
		var layout := MapGenerator.layout_of(plan, int(map.seed))
		var rooms := _rooms(plan, layout)
		for room: int in rooms[0]:
			var size := RoomFill.ARENA if rooms[1].has(room) else RoomFill.MIDDLE
			var low := layout.room_xy(room) * RoomLayout.ROOM + RoomLayout.FIRST_MIDDLE
			low -= Vector2i.ONE * (size / 2)
			var blocked := 0
			for y in size:
				for x in size:
					blocked += 0 if _free(map, low + Vector2i(x, y)) else 1
			eq(blocked, 0, "place %d, room %d: its middle %dx%d free" % [n, room, size, size])


func test_nothing_tall_in_front_of_a_fight() -> void:
	for n: int in _places():
		var plan := MapPlan.of(n)
		var map := _map(n)
		var layout := MapGenerator.layout_of(plan, int(map.seed))
		var tall: Array[String] = []
		for room: int in _rooms(plan, layout)[0]:
			var corner := layout.room_xy(room) * RoomLayout.ROOM + Vector2i.ONE
			for y in range(RoomLayout.ROOM - RoomFill.FRONT_ROWS, RoomLayout.ROOM + 1):
				for x in RoomLayout.ROOM:
					var c := corner + Vector2i(x, y)
					var what := str(map.props[c.y * int(map.w) + c.x])
					if what in RoomFill.TALL and not _free(map, c):
						tall.append("%s at %s" % [what, c])
		eq(tall, [] as Array[String], "place %d" % n)


func test_each_fir_of_a_column_shows() -> void:
	for n: int in _places():
		var map := _map(n)
		var w := int(map.w)
		var stacked := 0
		for i in w * (int(map.h) - 1):
			if map.props[i] == "fir" and map.props[i + w] == "fir":
				stacked += 1
		eq(stacked, 0, "place %d: no fir right above another one" % n)


func test_the_ground_takes_its_shares() -> void:
	var plan := MapPlan.of(1)
	var draft := MapDraft.new(MapGenerator.layout_of(plan, plan.seed))
	var path := Vector2i(4, 4)
	var water := Vector2i(10, 10)
	draft.path[draft.at(path)] = 1
	draft.put(water, "w", "")
	var biome := {"ground": "m", "patches": [["g", 0.3], ["d", 0.1]], "path": "o"}
	GroundPaint.new(draft, biome, GameRandom.new(1)).paint()
	var count := {}
	for letters in draft.parts:
		for letter in letters:
			count[letter] = int(count.get(letter, 0)) + 1
	var parts := draft.w * draft.h * MapArt.PARTS * MapArt.PARTS
	var dirt := float(count.d) / parts
	var grass := float(count.g) / parts
	check(absf(dirt - 0.1) < 0.01, "a tenth of the ground dirt: %.3f" % dirt)
	check(grass > 0.18 and grass < 0.3, "the grass under the dirt here and there: %.3f" % grass)
	eq(draft.parts[draft.at(path)], "ooooooooo", "the path all over its cell")
	eq(draft.parts[draft.at(water)], "wwwwwwwww", "the water all over its cell")
	var right := draft.parts[draft.at(water + Vector2i(1, 0))]
	eq([right[0], right[3], right[6]], ["s", "s", "s"], "sand on the bank, the side by the water")


func test_the_lab_shows_the_maps() -> void:
	var lab: Control = load("res://lab/map_gen_lab.tscn").instantiate()
	root.add_child(lab)
	eq([lab.place, lab.map_seed], [1, MapPlan.of(1).seed], "place 1 from its own seed")
	var first := JSON.stringify(lab.map)
	var key := InputEventKey.new()
	key.pressed = true
	key.keycode = KEY_N
	lab._unhandled_input(key)
	eq(lab.map_seed, MapPlan.of(1).seed + 1, "N: the next seed")
	check(JSON.stringify(lab.map) != first, "another seed, another map")
	key.keycode = KEY_M
	lab._unhandled_input(key)
	eq(lab.mission, 1, "M: the route of the second mission")
	key.keycode = KEY_LEFT
	lab._unhandled_input(key)
	eq([lab.place, lab.mission], [MapBuilder.map_count(), 0], "Left from the first: the last place")
	check(lab.info.text.begins_with("Place %d " % lab.place), lab.info.text)
	check(lab.info.text.ends_with("plays"), "its map plays: " + lab.info.text)
	lab.free()
