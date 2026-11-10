class_name EnchantSparkle
extends Control
## The light that plays over a thing being enchanted or combined, in the new art: a brass glow
## that swells and fades, a ring running out, a turning star of light and glints flying away.
## It is added onto the screen's colours (the node's material). The screen tells it where and
## how far it has played (show_over); with no places nothing is drawn.

const CORE := Color("fff3d0")  # the light at its heart
const SIZE := 0.6  # its radius, as a part of the cell's width
const GLOW_DISCS := 10  # soft discs, each a little wider, so it is brightest in the middle
const GLOW_ALPHA := 0.05  # of one disc, at the sparkle's height
const RING_POINTS := 48
const RING_ALPHA := 0.85
const TURN := 0.7  # how far the star turns over the whole sparkle, radians
const GLINTS := 6

var places: Array[Rect2] = []  # the cells it plays on, on the screen
var phase := 0.0  # how far it has played, 0..1


## Plays over the cells `rects` as it is at `t` (0..1); no rects: nothing shows.
func show_over(rects: Array[Rect2], t: float) -> void:
	places = rects
	phase = t
	queue_redraw()


func _draw() -> void:
	var rise := sin(PI * phase)  # up and down again over the whole sparkle
	var out := 1.0 - pow(1.0 - phase, 2.0)  # fast, then slower
	for rect in places:
		var mid := rect.get_center()
		var r := rect.size.x * SIZE
		_glow(mid, r * (0.6 + 0.4 * out), rise)
		_ring(mid, r * lerpf(0.3, 1.15, out))
		var turn := TURN * phase
		_star(mid, r * 0.95 * pow(rise, 0.7), r * 0.09, turn, _faded(CORE, 0.95 * rise))
		var cross := _faded(UiTheme.HIGHLIGHT, 0.7 * rise)
		_star(mid, r * 0.5 * pow(rise, 0.7), r * 0.07, turn + PI / 4.0, cross)
		_glints(mid, r)


## The glow: GLOW_DISCS discs up to `r` wide, as bright as `rise`.
func _glow(mid: Vector2, r: float, rise: float) -> void:
	var color := _faded(UiTheme.HIGHLIGHT, GLOW_ALPHA * rise)
	for k in GLOW_DISCS:
		draw_circle(mid, r * (0.3 + 0.7 * k / (GLOW_DISCS - 1.0)), color)


## The ring running out to `r`, thinner and fainter as the sparkle ends.
func _ring(mid: Vector2, r: float) -> void:
	var color := _faded(UiTheme.ACCENT, RING_ALPHA * (1.0 - phase))
	draw_arc(mid, r, 0.0, TAU, RING_POINTS, color, 1.0 + 3.0 * (1.0 - phase), true)


## The glints flying out from the middle, one after another, up to `r` away.
func _glints(mid: Vector2, r: float) -> void:
	var tint := CORE.lerp(UiTheme.HIGHLIGHT, 0.4)
	for g in GLINTS:
		var when := clampf(phase * 1.25 - 0.04 * g, 0.0, 1.0)
		var a := TAU * g / GLINTS + 0.35 + 0.5 * phase
		var at := mid + Vector2.from_angle(a) * r * (0.25 + 0.75 * when)
		_star(at, r * 0.2 * sin(PI * when), r * 0.04, a, _faded(tint, sin(PI * when)))


## A four-pointed star of light: long points `long` from c, `thin` across, turned by `turn`.
func _star(c: Vector2, long: float, thin: float, turn: float, color: Color) -> void:
	if long <= 0.5 or color.a <= 0.01:
		return
	var points := PackedVector2Array()
	for k in 8:
		points.append(c + Vector2.from_angle(turn + k * PI / 4.0) * (long if k % 2 == 0 else thin))
	draw_colored_polygon(points, color)


static func _faded(color: Color, alpha: float) -> Color:
	return Color(color, alpha)
