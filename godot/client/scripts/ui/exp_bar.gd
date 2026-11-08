extends Control
## Draws the exp bar of the pages after a won mission (MapSim.exp_bars, scripts/sim/exp_bars.gd)
## in the new art: a dark hollow of 102 x 7 grid pixels with an iron rim and hard ends, what the
## hero had blood-red, what the mission gave blue, what the time gave brass; each part in three
## lines of colour, lighter to the middle, and a shine along its top.

const W := 100
const H := 7
## Each part's three colours, from the edge to the middle line.
const COLORS := [
	[Color("0f0f10"), Color("161514"), Color("1d1b19")],
	[Color("4a0f0c"), Color("7e241f"), Color("bf3a2e")],
	[Color("101d36"), Color("2d3f57"), Color("4f78b0")],
	[Color("6f5a33"), Color("b08d4a"), Color("dcc48e")],
]
const RIM := Color("4e4a45")

var px := 3.0  # screen pixels to an original pixel
var bars: RefCounted  # the sim's exp bar


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	custom_minimum_size = Vector2(W + 2, H) * px


func _draw() -> void:
	var hollow := StyleBoxFlat.new()
	hollow.bg_color = Color("0b0b0c")
	hollow.set_corner_radius_all(int(px / 2.0))
	hollow.anti_aliasing = true
	draw_style_box(hollow, Rect2(Vector2.ZERO, Vector2(W + 2, H) * px))
	if bars != null:
		_draw_parts()
	var rim := StyleBoxFlat.new()
	rim.draw_center = false
	rim.border_color = RIM
	rim.set_border_width_all(maxi(1, int(px / 2.0)))
	rim.set_corner_radius_all(int(px / 2.0))
	rim.anti_aliasing = true
	draw_style_box(rim, Rect2(Vector2.ZERO, Vector2(W + 2, H) * px))


func _draw_parts() -> void:
	var b: Array = bars.bars
	var width: int = bars.grown()[0]
	var parts := [[0, W], [0, int(b[0])]]
	if bars.part == 0:
		parts.append([int(b[0]), width])
	else:
		parts.append([int(b[0]), int(b[1]) - int(b[0])])
		parts.append([int(b[1]), width])
	for p in parts.size():
		var x0 := clampi(int(parts[p][0]), 0, W)
		var x1 := clampi(int(parts[p][0]) + int(parts[p][1]), 0, W)
		if x1 <= x0:
			continue
		for line in 3:
			draw_rect(Rect2(Vector2(1 + x0, 1 + line) * px, Vector2(x1 - x0, H - 2 - 2 * line) * px),
				COLORS[p][line])
	draw_rect(Rect2(Vector2(2, 1.4) * px, Vector2(W - 2, 0.6) * px), Color(1, 1, 1, 0.18))
