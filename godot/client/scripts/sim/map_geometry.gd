class_name MapGeometry
extends RefCounted
## Distances, directions and reaches on the map, in pixels (a tile is 27 px).

## How far to the side of the line he faces the hero's sword still hits (one cell).
const STRIKE_BAND := 27


## Rounded distance in pixels.
static func distance(a: Vector2i, b: Vector2i) -> int:
	var dx := absi(a.x - b.x)
	var dy := absi(a.y - b.y)
	var d2 := dx * dx + dy * dy
	var i := maxi(dy, dx)
	while i * i < d2:
		i += 2
	i -= 1
	if i * i < d2:
		i += 1
	return i


## Direction 0 / 2 / 4 / 6 from a to b.
static func dir4(a: Vector2i, b: Vector2i) -> int:
	var i := b.x - a.x
	var dy := b.y - a.y
	if dy > i:
		return 0 if dy > -i else 2
	return 6 if dy > -i else 4


## Direction 0..7 from a to b.
static func dir8(a: Vector2i, b: Vector2i) -> int:
	var i := b.x - a.x
	var dy := b.y - a.y
	if i + i < dy:
		if i + i > -dy:
			return 0
		if -i < dy + dy:
			return 1
		if i < dy + dy:
			return 2
		return 3
	if i + i < -dy:
		return 4
	if -i > dy + dy:
		return 5
	if i > dy + dy:
		return 6
	return 7


## The two boxes overlap (the game's own test, kept as it is).
static func boxes_touch(
	x1: int, y1: int, w1: int, h1: int, x2: int, y2: int, w2: int, h2: int
) -> bool:
	var dx := x1 + w1 / 2 - x2 + w2 / 2
	var dy := y1 + h1 / 2 - y2 + h2 / 2
	return absi(dx) < (w1 + w2) / 2 and absi(dy) < (h1 + h2) / 2


static func is_in_front(a: Vector2i, b: Vector2i, d8: int) -> bool:
	match d8:
		2:
			return a.x > b.x
		6:
			return a.x < b.x
		0:
			return a.y < b.y
		4:
			return a.y > b.y
	return false


## What the hero's sword reaches: within reach, and either in the quarter he faces or ahead of
## him and no farther than STRIKE_BAND to the side, so an enemy a little above or below (or
## beside, when he faces up or down) is hit too, also close up where the quarter is narrow.
static func in_strike_reach(a: Vector2i, b: Vector2i, d8: int, reach: int) -> bool:
	if distance(a, b) > reach:
		return false
	if d8 == dir4(a, b):
		return true
	var d := b - a
	match d8:
		0:
			return d.y >= 0 and absi(d.x) <= STRIKE_BAND
		4:
			return d.y <= 0 and absi(d.x) <= STRIKE_BAND
		6:
			return d.x >= 0 and absi(d.y) <= STRIKE_BAND
		2:
			return d.x <= 0 and absi(d.y) <= STRIKE_BAND
	return false


## Room edges in pixels: 27 + 189 k, as the original's table (x 3 / 2).
static func edge(k: int) -> int:
	return 27 + 189 * k


static func straighten_step(delta: int, row: int) -> int:
	const STEPS := [
		[0, 1, 1, 2, 3, 4, 4, 5, 6, 7, 7, 8, 8, 9, 10, 10, 11],
		[0, 2, 3, 4, 6, 7, 8, 9, 11, 13, 14, 16, 17, 18, 20, 21, 23]
	]
	if delta < 0:
		return -int(STEPS[row][mini(16, -delta)])
	return int(STEPS[row][mini(16, delta)])
