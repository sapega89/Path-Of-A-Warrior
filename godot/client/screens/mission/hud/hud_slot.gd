class_name HudSlot
extends Button
## A slot of the skill bar on the mission's HUD (hud_slot.tscn): a dark hollow with an icon,
## how many of it are left (a potion of the belt) at the bottom right, and the key or pad button
## that uses it at the top left: a word, a small d-pad with the arm to press lit, or a PlayStation
## button's shape (the font has no such signs). The one in use has a light rim. A click or a tap
## on it is its pressed signal.

const GLYPH_BOX := 13.0  # the sign of the key, on the 240x320 grid

var _glyph_label := {}

@onready var _icon: TextureRect = %Icon
@onready var _count: Label = %Count
@onready var _key: Label = %Key
@onready var _glyph: Control = %Glyph


func _ready() -> void:
	_glyph.draw.connect(_draw_glyph)


## The icon (or none), how many (shown from two), and the light rim of the one in use.
func show_item(icon: Texture2D, count: int, hot: bool) -> void:
	_icon.texture = icon
	_count.text = str(count) if count > 1 else ""
	theme_type_variation = &"HudSlotHot" if hot else &"HudSlot"


## The slot's key for the device just used (Glyphs.short_of): nothing for {}.
func show_key(label: Dictionary) -> void:
	_key.text = str(label.get("text", ""))
	if label != _glyph_label:
		_glyph_label = label
		_glyph.queue_redraw()


func _draw_glyph() -> void:
	var k := _glyph.size.x / GLYPH_BOX
	if _glyph_label.has("shape"):
		_shape(str(_glyph_label.shape), Vector2(5.5, 5.5) * k, 3.0 * k)
	elif _glyph_label.has("dpad"):
		_dpad(_glyph_label.dpad, Vector2(6.5, 6.5) * k, 5.0 * k)


## A small d-pad of half-width r around c, outlined in ink: dark iron, the arm towards `dir` brass.
func _dpad(dir: Vector2, c: Vector2, r: float) -> void:
	var a := maxf(1.0, r * 0.36)  # half an arm's width
	var bars := [
		Rect2(c - Vector2(r, a), Vector2(r, a) * 2), Rect2(c - Vector2(a, r), Vector2(a, r) * 2)
	]
	for b: Rect2 in bars:
		_glyph.draw_rect(b.grow(maxf(1.0, r / 6.0)), UiTheme.INK)
	for b: Rect2 in bars:
		_glyph.draw_rect(b, UiTheme.IRON)
	var side := Vector2(-dir.y, dir.x)
	_glyph.draw_rect(
		Rect2(c + side * a + dir * a, Vector2.ZERO).expand(c - side * a + dir * r), UiTheme.ACCENT
	)


## A PlayStation face button's sign of radius r around c, in brass outlined in ink.
func _shape(shape: String, c: Vector2, r: float) -> void:
	var w := maxf(1.5, r / 2.5)
	for stroke in [[UiTheme.INK, w + 2.0], [UiTheme.ACCENT, w]]:
		var color: Color = stroke[0]
		var width: float = stroke[1]
		match shape:
			"cross":
				for d in [Vector2(1, 1), Vector2(1, -1)]:
					_glyph.draw_line(c - d * r, c + d * r, color, width, true)
			"circle":
				_glyph.draw_arc(c, r, 0, TAU, 16, color, width, true)
			"square":
				_glyph.draw_rect(Rect2(c - Vector2(r, r), Vector2(r, r) * 2), color, false, width)
			"triangle":
				_glyph.draw_polyline(
					PackedVector2Array(
						[
							c + Vector2(0, -r),
							c + Vector2(r, r * 0.8),
							c + Vector2(-r, r * 0.8),
							c + Vector2(0, -r)
						]
					),
					color,
					width,
					true
				)
