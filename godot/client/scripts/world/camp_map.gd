class_name CampMap
extends RefCounted
## The stop between missions: a small map in the format of data/maps/N.json (so MapBuilder
## builds it), made in code from the original tiles. Big trees close it in (three tiles deep
## at the top, two wide on the sides); each way on (a mission, see camp_screen.gd) is a gap in
## the trees (`inside` is the cell just within it), with a fence across it while its place is
## closed. The hero comes in at the bottom. Every camp has the blacksmith's fire (buy, sell,
## enchant,
## combine), the stores (the warehouse) and the town hall (every colonel and general, and
## the visits of the generals). Dirt roads run from the campfire to each way and down to where
## the hero comes in; the smithy and the stores have their racks, crates and hay, and bushes,
## stumps and stones lie about, placed by the camp's own seed (so each place looks its own and
## the same each time) and only where every way, door and spot can still be reached.

const W := 17
const H := 13
const GRASS := 4
## The big tree of the original maps: two tiles across, three down, stood up over the hero.
const TREE := [[63, 64], [65, 66], [67, 68]]
const TOP := 3  # rows of trees at the top
const SIDE := 2  # columns of trees on each side
const BUSH := 136
const STONES := 137
const CAMPFIRE := 140
const BRAZIER := 140  # the blacksmith's fire
const FENCE := [85, 86]
## The town hall: the big tent of the original maps, four tiles across and two down.
const HALL := [[193, 194, 195, 196], [197, 198, 199, 200]]
const HALL_AT := Vector2i(2, 7)  # its top-left cell
const SMITH_AT := Vector2i(13, 7)
const STORE_AT := Vector2i(11, 10)  # barrels and a crate, left to right
const STORE := [97, 97, 105]
const BLOCKED := 1
const OVER := 2
const DIRT := 2
## The edges of a dirt road, by the sides that have no road: north-west, north, ...
const ROAD_EDGE := {"nw": 20, "n": 21, "ne": 22, "w": 23, "e": 24, "sw": 25, "s": 26, "se": 27}
const HUB := Vector2i(8, 6)  # the campfire, where the roads meet
## A soldiers' tent, three across and two down; it stands in the first of these places it fits.
const TENT := [[217, 218, 219], [220, 221, 222]]
const TENT_AT := [Vector2i(2, 4), Vector2i(11, 4), Vector2i(4, 4), Vector2i(10, 4)]
## Things that stand at their place in every camp where they fit: [tile, cell].
const PROPS := [
	[125, Vector2i(14, 7)],
	[126, Vector2i(12, 7)],  # weapon racks by the blacksmith's fire
	[106, Vector2i(14, 10)],
	[111, Vector2i(10, 11)],  # a crate and hay by the stores
	[115, Vector2i(7, 7)],
	[116, Vector2i(9, 5)],  # stumps to sit on by the fire
	[113, Vector2i(11, 4)],
	[113, Vector2i(5, 4)],  # the well (the first place that fits)
]
## Scattered about: bushes, stumps and hay stand and block; stones lie flat.
const SCATTER_UP := [136, 136, 117, 118, 115, 116, 111]
const SCATTER_FLAT := [137, 137, 137]
## Where the gaps go for 1..6 ways: [side, centre]; side 0 top, 1 right, 2 left.
const GAPS := [
	[],
	[[0, 8]],
	[[0, 4], [0, 12]],
	[[0, 3], [0, 8], [0, 13]],
	[[2, 5], [0, 4], [0, 12], [1, 5]],
	[[2, 5], [0, 3], [0, 8], [0, 13], [1, 5]],
	[[2, 5], [0, 3], [0, 8], [0, 13], [1, 5], [2, 9]],
]
## The places the endings take the hero to (Profile.NEXT_PLACE) and the start: main camps.
const MAIN := [0, 8, 11, 15, 17, 19, 20, 22, 30, 33, 35, 38, 39, 44]

var data := {}
## One per way: {place, mission, open, gap: [cells], inside: Vector2i, side}
var exits: Array = []
var main := false
var start := Vector2i(8, 10)


static func is_main(place: int) -> bool:
	return place in MAIN


## ways: [[place id, open], ...] or [[place id, open, mission], ...], at most six.
func _init(ways: Array = [], main_camp: bool = false, seed: int = 0) -> void:
	main = main_camp
	var rng := RandomNumberGenerator.new()
	rng.seed = seed
	var ground: Array = []
	var upper: Array = []
	var flags: Array = []
	var objects: Array = []
	ground.resize(W * H)
	ground.fill(GRASS)
	upper.resize(W * H)
	upper.fill(0)
	flags.resize(W * H)
	flags.fill(0)
	objects.resize(W * H)
	objects.fill(0)
	data = {
		"w": W,
		"h": H,
		"ground": ground,
		"upper": upper,
		"objects": objects,
		"flags": flags,
		"scripts": [],
		"number": 0,
		"rooms": {"rooms_x": 1, "rooms_y": 1, "missions": []}
	}
	# The border is blocked all round; the bottom without a picture, so nothing stands between
	# the camera and the hero. The trees go on after the gaps are known.
	for x in W:
		for y in TOP:
			_put(x, y, 0, BLOCKED)
		_put(x, H - 1, 0, BLOCKED)
	for y in range(TOP, H - 1):
		for x in [0, 1, W - 2, W - 1]:
			_put(x, y, 0, BLOCKED)
	var gaps: Array = GAPS[clampi(ways.size(), 0, GAPS.size() - 1)]
	var gap_cells := {}
	for i in mini(ways.size(), gaps.size()):
		var side: int = gaps[i][0]
		var c: int = gaps[i][1]
		var cells: Array = []
		var inside := Vector2i.ZERO
		match side:
			0:
				for y in TOP:
					for dx in [-1, 0, 1]:
						cells.append(Vector2i(c + dx, y))
				inside = Vector2i(c, TOP)
			1:
				for x in [W - 2, W - 1]:
					for dy in [-1, 0, 1]:
						cells.append(Vector2i(x, c + dy))
				inside = Vector2i(W - 3, c)
			2:
				for x in [0, 1]:
					for dy in [-1, 0, 1]:
						cells.append(Vector2i(x, c + dy))
				inside = Vector2i(2, c)
		var open: bool = ways[i][1]
		for p in cells:
			gap_cells[p] = true
			_put(p.x, p.y, 0, 0 if open else BLOCKED)
		if not open:  # a fence across the inner end of a closed gap
			for p in cells:
				var inner: bool = (
					(side == 0 and p.y == TOP - 1)
					or (side == 1 and p.x == W - 2)
					or (side == 2 and p.x == 1)
				)
				if inner:
					_put(p.x, p.y, FENCE[(p.x + p.y) % 2] if side == 0 else BUSH, BLOCKED)
		var mission: int = int(ways[i][2]) if ways[i].size() > 2 else -1
		# gap[1] is the middle of the gap's outer edge, where the hero walks out
		exits.append(
			{
				"place": ways[i][0],
				"mission": mission,
				"open": open,
				"gap": cells,
				"inside": inside,
				"side": side
			}
		)
	_plant(gap_cells)
	_put(8, 6, CAMPFIRE, BLOCKED)
	_put(6, 8, STONES, 0)
	_put(SMITH_AT.x, SMITH_AT.y, BRAZIER, BLOCKED)
	for i in STORE.size():
		_put(STORE_AT.x + i, STORE_AT.y, STORE[i], BLOCKED)
	for row in HALL.size():
		for col in HALL[row].size():
			_put(HALL_AT.x + col, HALL_AT.y + row, HALL[row][col], BLOCKED | OVER)
	var dirt := _roads()
	_decorate(dirt, gap_cells, rng)
	_lay_roads(dirt)


## Where one stands to use the town hall's door and the blacksmith's fire.
func hall_door() -> Vector2i:
	return HALL_AT + Vector2i(2, HALL.size())


func smith_spot() -> Vector2i:
	return SMITH_AT + Vector2i(0, 1)


func store_spot() -> Vector2i:
	return STORE_AT + Vector2i(1, 1)


## The cells everyone must be able to walk to from the start: each way's inside and its
## gap (when open), the hall's door, the blacksmith's and the stores' spots.
func must_reach() -> Array:
	var cells: Array = [hall_door(), smith_spot(), store_spot()]
	for e in exits:
		cells.append(e.inside)
		if e.open:
			cells.append(e.gap[1])
	return cells


func is_free(c: Vector2i) -> bool:
	return (
		c.x >= 0
		and c.y >= 0
		and c.x < W
		and c.y < H
		and (int(data.flags[c.y * W + c.x]) & BLOCKED) == 0
	)


## Whether every cell of must_reach() can be walked to from the start.
func all_reachable() -> bool:
	var seen := {start: true}
	var todo: Array = [start]
	while not todo.is_empty():
		var c: Vector2i = todo.pop_back()
		for d in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
			var n: Vector2i = c + d
			if not seen.has(n) and is_free(n):
				seen[n] = true
				todo.append(n)
	return must_reach().all(func(c): return seen.has(c))


## The road cells: a ring round the campfire, a road down to the bottom edge and one to each
## way (out through the gap when it is open): along the column, then the row, two wide.
func _roads() -> Dictionary:
	var dirt := {}
	for dy in range(-1, 2):
		for dx in range(-1, 2):
			dirt[HUB + Vector2i(dx, dy)] = true
	_road(dirt, Vector2i(HUB.x, H - 2), true)
	for e in exits:
		var to: Vector2i = e.inside
		if e.open:
			match int(e.side):
				0:
					to = Vector2i(e.inside.x, 0)
				1:
					to = Vector2i(W - 1, e.inside.y)
				2:
					to = Vector2i(0, e.inside.y)
		_road(dirt, to, int(e.side) == 0)
	return dirt


## A road from `to` to the campfire: first along its column (down_first) or its row.
func _road(dirt: Dictionary, to: Vector2i, down_first: bool) -> void:
	var corner := Vector2i(to.x, HUB.y) if down_first else Vector2i(HUB.x, to.y)
	for y in range(mini(to.y, corner.y), maxi(to.y, corner.y) + 1):
		for dx in 2:
			dirt[Vector2i(corner.x + dx, y)] = true
	var row := HUB.y if down_first else to.y
	var x_from := HUB.x if down_first else to.x
	var x_to := to.x if down_first else HUB.x
	if not down_first:
		for y in range(mini(to.y, HUB.y), maxi(to.y, HUB.y) + 1):
			for dx in 2:
				dirt[Vector2i(HUB.x + dx, y)] = true
	for x in range(mini(x_from, x_to), maxi(x_from, x_to) + 1):
		for dy in 2:
			dirt[Vector2i(x, row + dy)] = true


## The roads on the ground: plain dirt inside, a soft edge where the grass begins (the edge
## lies over the grass, so it goes only where nothing else stands).
func _lay_roads(dirt: Dictionary) -> void:
	for c in dirt:
		if c.x < 0 or c.y < 0 or c.x >= W or c.y >= H:
			continue
		var on := func(dx: int, dy: int) -> bool:
			var n: Vector2i = c + Vector2i(dx, dy)
			return dirt.has(n)
		var key := ""
		if not on.call(0, -1):
			key = "n"
		elif not on.call(0, 1):
			key = "s"
		if not on.call(-1, 0):
			key += "w"
		elif not on.call(1, 0):
			key += "e"
		var i: int = c.y * W + c.x
		if key == "" or int(data.upper[i]) != 0 or int(data.flags[i]) != 0:
			data.ground[i] = DIRT
		else:
			data.upper[i] = ROAD_EDGE[key]


## Whether a thing standing up at c stays a picture of its own: nothing raised just above or
## below it in its column (that would join it to a taller one, or lay a long run flat).
func _stands_alone(c: Vector2i, rows: int = 1) -> bool:
	for y in [c.y - 1, c.y + rows]:
		if y >= 0 and y < H:
			var i: int = y * W + c.x
			if int(data.upper[i]) != 0 and int(data.flags[i]) & (BLOCKED | OVER) != 0:
				return false
	return true


## Whether c is open ground for a thing: no road, no gap, nothing there, not next to a way in.
func _room_for(c: Vector2i, dirt: Dictionary, gaps: Dictionary) -> bool:
	if c.x < SIDE or c.x >= W - SIDE or c.y < TOP or c.y >= H - 1:
		return false
	if dirt.has(c) or gaps.has(c) or c == start:
		return false
	var i: int = c.y * W + c.x
	if int(data.upper[i]) != 0 or int(data.flags[i]) != 0:
		return false
	for e in exits:
		if absi(e.inside.x - c.x) <= 1 and absi(e.inside.y - c.y) <= 1:
			return false
	for s in [hall_door(), smith_spot(), store_spot()]:
		if s == c:
			return false
	return true


## Puts the cells' tiles (blocked, standing up) and keeps them only if all can still be reached.
func _try(cells: Array, tiles: Array) -> bool:
	for i in cells.size():
		_put(cells[i].x, cells[i].y, tiles[i], BLOCKED | OVER)
	if all_reachable():
		return true
	for c in cells:
		_put(c.x, c.y, 0, 0)
	return false


func _decorate(dirt: Dictionary, gaps: Dictionary, rng: RandomNumberGenerator) -> void:
	for at in TENT_AT:
		var cells: Array = []
		var tiles: Array = []
		var fits := true
		for row in TENT.size():
			for col in TENT[row].size():
				var c: Vector2i = at + Vector2i(col, row)
				fits = fits and _room_for(c, dirt, gaps)
				cells.append(c)
				tiles.append(TENT[row][col])
		for col in TENT[0].size():
			fits = fits and _stands_alone(at + Vector2i(col, 0), TENT.size())
		if fits and _try(cells, tiles):
			break
	var well := false
	for p in PROPS:
		var c: Vector2i = p[1]
		if p[0] == 113 and well:
			continue
		if _room_for(c, dirt, gaps) or (p[0] in [115, 116] and dirt.has(c)):
			if _stands_alone(c) and _try([c], [p[0]]):
				well = well or p[0] == 113
	var free: Array = []
	for y in range(TOP, H - 1):
		for x in range(SIDE, W - SIDE):
			if _room_for(Vector2i(x, y), dirt, gaps):
				free.append(Vector2i(x, y))
	for n in 9:
		if free.is_empty():
			break
		var c: Vector2i = free.pop_at(rng.randi_range(0, free.size() - 1))
		if not _room_for(c, dirt, gaps):
			continue
		if n < 6:
			if _stands_alone(c):
				_try([c], [SCATTER_UP[rng.randi_range(0, SCATTER_UP.size() - 1)]])
		else:
			_put(c.x, c.y, SCATTER_FLAT[rng.randi_range(0, SCATTER_FLAT.size() - 1)], 0)
	# Bushes on the sides where a gap left no room for a tree.
	for x in [1, W - 2]:
		for y in range(TOP, H - 1):
			var c := Vector2i(x, y)
			var i: int = y * W + x
			if gaps.has(c) or int(data.upper[i]) != 0:
				continue
			if _stands_alone(c) and rng.randf() < 0.8:
				_put(x, y, [136, 117, 118][rng.randi_range(0, 2)], BLOCKED | OVER)


## Big trees on the border where they fit whole (not over a gap); a tree's three rows stand up
## as one picture (a longer blocked run would lie flat, so trees on a side leave a row between
## them). Where no tree fits, the border is only blocked.
func _plant(gaps: Dictionary) -> void:
	var x := 0
	while x < W:
		if x + 1 < W and _free_for_tree(x, 0, gaps):
			_tree(x, 0)
			x += 2
		else:
			x += 1
	for side_x in [0, W - 2]:
		var y := TOP + 1
		while y + 2 < H - 1:
			if _free_for_tree(side_x, y, gaps):
				_tree(side_x, y)
				y += 4
			else:
				y += 1


func _free_for_tree(x: int, y: int, gaps: Dictionary) -> bool:
	for row in TREE.size():
		for col in 2:
			if gaps.has(Vector2i(x + col, y + row)):
				return false
	return true


func _tree(x: int, y: int) -> void:
	for row in TREE.size():
		for col in 2:
			_put(x + col, y + row, TREE[row][col], BLOCKED | OVER)


func _put(x: int, y: int, tile: int, flag: int) -> void:
	data.upper[y * W + x] = tile
	data.flags[y * W + x] = flag
