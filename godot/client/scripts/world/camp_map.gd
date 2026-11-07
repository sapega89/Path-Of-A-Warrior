extends RefCounted
## The stop between missions: a small map in the format of data/maps/N.json (so MapBuilder
## builds it), made in code from the original tiles. Big trees close it in (three tiles deep
## at the top, two wide on the sides); each way on (a mission, see camp_screen.gd) is a gap in
## the trees (`inside` is the cell just within it), with a fence across it while its place is
## closed. The hero comes in at the bottom. Every camp has the blacksmith's fire (buy, sell, enchant,
## combine), the stores (the warehouse) and the town hall (every colonel and general, and
## the visits of the generals).

const W := 17
const H := 13
const GRASS := 1
## The big tree of the original maps: two tiles across, three down, stood up over the hero.
const TREE := [[63, 64], [65, 66], [67, 68]]
const TOP := 3  # rows of trees at the top
const SIDE := 2  # columns of trees on each side
const BUSH := 136
const STONES := 137
const CAMPFIRE := 140
const BRAZIER := 141
const FENCE := [85, 86]
## The town hall: the big tent of the original maps, four tiles across and two down.
const HALL := [[193, 194, 195, 196], [197, 198, 199, 200]]
const HALL_AT := Vector2i(2, 7)  # its top-left cell
const SMITH_AT := Vector2i(13, 8)
const STORE_AT := Vector2i(11, 5)  # barrels and a crate, left to right
const STORE := [97, 97, 105]
const BLOCKED := 1
const OVER := 2
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
func _init(ways: Array = [], main_camp: bool = false) -> void:
	main = main_camp
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
	data = {"w": W, "h": H, "ground": ground, "upper": upper, "objects": objects, "flags": flags,
		"scripts": [], "number": 0, "rooms": {"rooms_x": 1, "rooms_y": 1, "missions": []}}
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
				var inner: bool = (side == 0 and p.y == TOP - 1) or (side == 1 and p.x == W - 2) \
					or (side == 2 and p.x == 1)
				if inner:
					_put(p.x, p.y, FENCE[(p.x + p.y) % 2] if side == 0 else BUSH, BLOCKED)
		var mission: int = int(ways[i][2]) if ways[i].size() > 2 else -1
		# gap[1] is the middle of the gap's outer edge, where the hero walks out
		exits.append({"place": ways[i][0], "mission": mission, "open": open, "gap": cells,
			"inside": inside, "side": side})
	_plant(gap_cells)
	_put(8, 6, CAMPFIRE, BLOCKED)
	_put(6, 8, STONES, 0)
	_put(SMITH_AT.x, SMITH_AT.y, BRAZIER, BLOCKED)
	for i in STORE.size():
		_put(STORE_AT.x + i, STORE_AT.y, STORE[i], BLOCKED)
	for row in HALL.size():
		for col in HALL[row].size():
			_put(HALL_AT.x + col, HALL_AT.y + row, HALL[row][col], BLOCKED | OVER)


## Where one stands to use the town hall's door and the blacksmith's fire.
func hall_door() -> Vector2i:
	return HALL_AT + Vector2i(2, HALL.size())


func smith_spot() -> Vector2i:
	return SMITH_AT + Vector2i(0, 1)


func store_spot() -> Vector2i:
	return STORE_AT + Vector2i(1, 1)


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
