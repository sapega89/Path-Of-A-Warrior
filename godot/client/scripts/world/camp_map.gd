extends RefCounted
## The stop between missions: a small map in the format of data/maps/N.json (so MapBuilder
## builds it), made in code from the original tiles. Pines close it in; each way on from the
## hero's place (WorldMap.next_places) is a gap in the pines, with a colonel who gives the
## missions there standing inside it, and a fence across it while that place is closed. The
## hero comes in at the bottom. A main camp (the start and the places the endings lead to)
## also has the town hall, where every colonel and general is, and the blacksmith.

const W := 17
const H := 13
const GRASS := 1
const PINE := 64  # a pine, stood up and drawn over the hero
const BUSH := 136
const STONES := 137
const CAMPFIRE := 140
const BRAZIER := 141
const FENCE := [85, 86]
## The town hall: the big tent of the original maps, four tiles across and two down.
const HALL := [[193, 194, 195, 196], [197, 198, 199, 200]]
const HALL_AT := Vector2i(2, 7)  # its top-left cell
const SMITH_AT := Vector2i(13, 8)
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
## One per way: {place, open, gap: [cells], inside: Vector2i (where its colonel stands), side}
var exits: Array = []
var main := false
var start := Vector2i(8, 10)


static func is_main(place: int) -> bool:
	return place in MAIN


## ways: [[place id, open], ...] in the order of WorldMap.next_places.
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
	# The pines all round: the top row stands up; on the sides every other one, so that each
	# stands on its own (a long run of blocked cells would lie flat); the bottom is closed
	# without a picture, so nothing stands between the camera and the hero.
	for x in W:
		_put(x, 0, PINE, BLOCKED | OVER)
		_put(x, H - 1, 0, BLOCKED)
	for y in range(1, H - 1):
		for x in [0, W - 1]:
			_put(x, y, PINE if y % 2 == 1 else 0, BLOCKED | (OVER if y % 2 == 1 else 0))
	var gaps: Array = GAPS[clampi(ways.size(), 0, GAPS.size() - 1)]
	for i in mini(ways.size(), gaps.size()):
		var side: int = gaps[i][0]
		var c: int = gaps[i][1]
		var cells: Array = []
		var inside := Vector2i.ZERO
		match side:
			0:
				cells = [Vector2i(c - 1, 0), Vector2i(c, 0), Vector2i(c + 1, 0)]
				inside = Vector2i(c, 2)
			1:
				cells = [Vector2i(W - 1, c - 1), Vector2i(W - 1, c), Vector2i(W - 1, c + 1)]
				inside = Vector2i(W - 3, c)
			2:
				cells = [Vector2i(0, c - 1), Vector2i(0, c), Vector2i(0, c + 1)]
				inside = Vector2i(2, c)
		var open: bool = ways[i][1]
		for k in cells.size():
			var p: Vector2i = cells[k]
			if open:
				_put(p.x, p.y, 0, 0)
			elif side == 0:
				_put(p.x, p.y, FENCE[k % 2], BLOCKED)
			else:  # a closed way on a side: a bush in each cell of it
				_put(p.x, p.y, BUSH, BLOCKED)
		exits.append({"place": ways[i][0], "open": open, "gap": cells, "inside": inside, "side": side})
	_put(8, 6, CAMPFIRE, BLOCKED)
	_put(6, 8, STONES, 0)
	_put(11, 4, BUSH, BLOCKED)
	if main:
		for row in HALL.size():
			for col in HALL[row].size():
				_put(HALL_AT.x + col, HALL_AT.y + row, HALL[row][col], BLOCKED | OVER)
		_put(SMITH_AT.x, SMITH_AT.y, BRAZIER, BLOCKED)


## Where one stands to use the town hall's door and the blacksmith's fire.
func hall_door() -> Vector2i:
	return HALL_AT + Vector2i(2, HALL.size())


func smith_spot() -> Vector2i:
	return SMITH_AT + Vector2i(0, 1)


func _put(x: int, y: int, tile: int, flag: int) -> void:
	data.upper[y * W + x] = tile
	data.flags[y * W + x] = flag
