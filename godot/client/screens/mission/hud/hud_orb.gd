class_name HudOrb
extends TextureProgressBar
## An orb of glass on the panel of the mission's HUD (HP or MP, hud_orb.tscn): the liquid
## (texture_progress) fills it from the bottom and has a light surface; over it the glass with a
## shine and an iron rim, and the value in the middle (%Value). Its textures are SVG drawn at the
## HUD's scale.

const BOX := 50.0  # the orb's box on the 240x320 grid
const RADIUS := 22.0  # the glass, inside the ink rim
const LIQUID_INSET := 3.5  # where the liquid's texture starts in the box
const LEVELS := 35  # how full an orb is: 0..LEVELS (max_value)

## The colour at the top of the liquid; its surface is a little lighter.
@export var liquid_top := Color.WHITE

@onready var _value: Label = %Value


func _ready() -> void:
	resized.connect(_fit)
	_fit()


## How full an orb is for v of most: 0..LEVELS, a little always seen while anything is left.
static func level(v: int, most: int) -> int:
	var f := LEVELS * v / maxi(most, 1)
	return maxi(f, 3) if f != 0 else 0


## The liquid at the level of v of most, and v in the middle.
func show_value(v: int, most: int) -> void:
	value = level(v, most)
	_value.text = str(v)


## The SVG textures are drawn as big as the orb is on the screen.
func _fit() -> void:
	var k := size.x / BOX
	(texture_under as DPITexture).base_scale = k
	(texture_progress as DPITexture).base_scale = k
	texture_progress_offset = Vector2.ONE * LIQUID_INSET * k


## Over the liquid: its surface, then the glass: a dark ring inside the rim, a shine at the upper
## left, the iron rim.
func _draw() -> void:
	var k := size.x / BOX
	var c := size / 2.0
	var r := RADIUS * k
	var f := value / max_value
	if f > 0.0 and f < 0.98:
		var s := 1.0 - 2.0 * f
		var half := sqrt(maxf(0.0, 1.0 - s * s)) * (r - 0.5 * k)
		var y := c.y + s * r
		draw_line(
			Vector2(c.x - half, y),
			Vector2(c.x + half, y),
			liquid_top.lightened(0.35),
			1.2 * k,
			true
		)
	draw_arc(c, r - 1.5 * k, 0.0, TAU, 48, Color(0, 0, 0, 0.35), 3.0 * k, true)
	var shine := PackedVector2Array()
	for i in 13:
		var t := lerpf(PI * 1.02, PI * 1.5, i / 12.0)
		shine.append(c + Vector2(cos(t), sin(t)) * r * 0.84)
	for i in 13:
		var t := lerpf(PI * 1.5, PI * 1.02, i / 12.0)
		shine.append(c + Vector2(0.1, 0.12) * r + Vector2(cos(t), sin(t)) * r * 0.76)
	draw_colored_polygon(shine, Color(1, 1, 1, 0.2))
	draw_circle(c + Vector2(-0.38, -0.52) * r, r * 0.07, Color(1, 1, 1, 0.45), true, -1.0, true)
	draw_arc(c, r + 0.8 * k, 0.0, TAU, 64, UiTheme.IRON_LIGHT, 2.2 * k, true)
