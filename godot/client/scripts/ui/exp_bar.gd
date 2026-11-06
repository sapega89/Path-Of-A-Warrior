extends Control
## Draws the exp bar of the pages after a won mission (MapSim.exp_bars, scripts/sim/exp_bars.gd)
## as pyport's menus.draw_exp_bar: a black frame of 102 x 7 original pixels, the empty bar
## grey, what the hero had red, what the mission gave blue, what the time gave orange; each
## part in three lines of colour, lighter to the middle.

const W := 100
const H := 7
## Each part's three colours, from the edge to the middle line.
const COLORS := [
	[Color8(115, 142, 140), Color8(181, 178, 181), Color8(255, 255, 255)],
	[Color8(99, 0, 0), Color8(181, 0, 0), Color8(247, 73, 0)],
	[Color8(0, 65, 255), Color8(0, 146, 255), Color8(0, 255, 173)],
	[Color8(247, 73, 0), Color8(255, 162, 0), Color8(255, 223, 0)],
]

var px := 3.0  # screen pixels to an original pixel
var bars: RefCounted  # the sim's exp bar


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	custom_minimum_size = Vector2(W + 2, H) * px


func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO, Vector2(W + 2, H) * px), Color.BLACK)
	if bars == null:
		return
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
