extends "res://tests/test_case.gd"
## The rooms made by hand (scripts/mapgen/set_piece.gd, data/set_pieces.json) and where the map
## generator lays them (RoomFill): each piece a room of known things, each biome with an arena
## for its generals and a start of its own; a piece lies its eight ways; on the map of every
## place the last room of each mission is the arena of a general, the first one a start, the
## pieces on the way stay out of the rooms where generals fight, and the ways through the rooms
## stay free and dry, on a bridge where they cross a piece's water.

const ROLES: Array[String] = ["general", "start", "crossing", "village", "gate"]

## The fills of the maps made, by place: each made once for all the tests here.
static var _fills := {}


## The fill of a place's map from its own seed, as the generator makes it.
func _filled(place: int) -> RoomFill:
	if not _fills.has(place):
		var plan := MapPlan.of(place)
		var crowding: Array = MapGenerator.curve(plan.depth)["crowding"]
		var fill := RoomFill.new(
			MapDraft.new(MapGenerator.layout_of(plan, plan.seed)),
			_rules()["biomes"][plan.biome],
			MapGenerator.stream(plan.seed, "fill")
		)
		fill.fill(plan, Vector2(crowding[0], crowding[1]))
		_fills[place] = fill
	return _fills[place]


func _rules() -> Dictionary:
	return JSON.parse_string(FileAccess.get_file_as_string(MapGenerator.RULES_PATH))


func _places() -> Array:
	return range(1, MapBuilder.map_count() + 1)


func _piece(piece_name: String) -> SetPiece:
	for piece in SetPiece.all():
		if piece.name == piece_name:
			return piece
	return null


## The role of the piece laid in a room, "" none.
func _role(fill: RoomFill, room: int) -> String:
	return _piece(fill.pieces[room]).role if fill.pieces.has(room) else ""


func test_each_piece_a_room_of_known_things() -> void:
	var key := SetPiece.key()
	for letter: String in key:
		var kind := str(key[letter].get("kind", ""))
		var prop := str(key[letter].get("prop", ""))
		var known := kind == "" or (kind.length() == 1 and kind in MapArt.KIND_LETTERS)
		check(known, "%s: kind %s" % [letter, kind])
		check(prop == "" or prop in MapArt.PROP or prop in MapArt.CLUSTERS, letter + ": " + prop)
	var pieces := SetPiece.all()
	check(pieces.size() >= 12 and pieces.size() <= 16, "12 to 16 pieces: %d" % pieces.size())
	var biomes: Dictionary = _rules()["biomes"]
	for piece in pieces:
		check(piece.role in ROLES, "%s: role %s" % [piece.name, piece.role])
		for biome in piece.biomes:
			check(biomes.has(biome), "%s: biome %s" % [piece.name, biome])
		eq(piece.rows.size(), SetPiece.SIDE, piece.name + ": its rows")
		for row in piece.rows:
			eq(row.length(), SetPiece.SIDE, piece.name + ": " + row)
			for letter in row:
				check(key.has(letter), "%s: %s in the key" % [piece.name, letter])
	for biome: String in biomes:
		for role: String in ["general", "start"]:
			check(not SetPiece.fitting(role, biome).is_empty(), "%s: a %s piece" % [biome, role])


## Where a piece laid the `way`-th way has its fir and its bush.
func _where(piece: SetPiece, way: int) -> Array[Vector2i]:
	var out: Array[Vector2i] = []
	for prop: String in ["fir", "bush"]:
		for y in SetPiece.SIDE:
			for x in SetPiece.SIDE:
				if piece.cell(Vector2i(x, y), way).get("prop", "") == prop:
					out.append(Vector2i(x, y))
	return out


func test_a_piece_lies_its_eight_ways() -> void:
	var piece := SetPiece.new()
	piece.rows.assign(["Tb.....", ".......", ".......", ".......", ".......", ".......", "......."])
	eq(_where(piece, 0), [Vector2i(0, 0), Vector2i(1, 0)] as Array[Vector2i], "as drawn")
	eq(
		_where(piece, 1),
		[Vector2i(6, 0), Vector2i(6, 1)] as Array[Vector2i],
		"a quarter turn: the top row on the right"
	)
	eq(_where(piece, 4), [Vector2i(6, 0), Vector2i(5, 0)] as Array[Vector2i], "mirrored")
	var ways := {}
	for way in SetPiece.WAYS:
		var where := _where(piece, way)
		eq(where.size(), 2, "way %d: one fir and one bush" % way)
		ways[str(where)] = true
	eq(ways.size(), SetPiece.WAYS, "each way another one")


func test_the_rooms_where_the_pieces_lie() -> void:
	var on_the_way := 0
	for n: int in _places():
		var plan := MapPlan.of(n)
		var fill := _filled(n)
		var layout := fill.draft.layout
		var lasts := {}
		var firsts := {}
		var arenas := {}
		for m in layout.routes.size():
			lasts[layout.routes[m].back()] = true
			firsts[layout.routes[m][0]] = true
			for i in layout.stops[m].size():
				if not plan.missions[m][i].generals.is_empty():
					arenas[layout.routes[m][layout.stops[m][i]]] = true
		for m in layout.routes.size():
			var route: Array = layout.routes[m]
			eq(_role(fill, route.back()), "general", "place %d, mission %d: its last room" % [n, m])
			if not lasts.has(route[0]):
				eq(_role(fill, route[0]), "start", "place %d, mission %d: its first room" % [n, m])
		for room: int in fill.pieces:
			var piece := _piece(fill.pieces[room])
			check(plan.biome in piece.biomes, "place %d: %s fits" % [n, piece.name])
			if not lasts.has(room) and not firsts.has(room):
				check(piece.role in RoomFill.ON_THE_WAY, "place %d: %s" % [n, piece.name])
				check(not arenas.has(room), "place %d, room %d: no %s" % [n, room, piece.name])
				on_the_way += 1
	check(on_the_way > 0, "crossings, villages and gates on the way: %d" % on_the_way)


func test_the_ways_stay_free_and_dry() -> void:
	var bridges := 0
	for n: int in _places():
		var draft := _filled(n).draft
		var shut: Array[Vector2i] = []
		for i in draft.w * draft.h:
			if draft.keep[i] == 0:
				continue
			if draft.blocked[i] == 1 or draft.kinds[i] == RoomFill.WATER:
				shut.append(Vector2i(i % draft.w, i / draft.w))
			bridges += 1 if draft.kinds[i] == RoomFill.BRIDGE else 0
		eq(shut, [] as Array[Vector2i], "place %d: the kept cells free and dry" % n)
	check(bridges > 0, "bridges where the ways cross a piece's water: %d" % bridges)
