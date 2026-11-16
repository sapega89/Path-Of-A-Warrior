class_name Heading
extends Label


## A heading: its text with an iron rule on each side, a rhombus of brass near the words and a
## rivet at the far end.
func _draw() -> void:
	var f := get_theme_font("font")
	var font_size := get_theme_font_size("font_size")
	var w := f.get_string_size(atr(text), HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x
	var free := (size.x - w) / 2.0
	if free < 48.0 or text.is_empty():
		return
	var y := size.y / 2.0 + font_size * 0.06
	var r := clampf(font_size * 0.11, 4.0, 7.0)
	var reach := minf(free - 20.0, font_size * 3.0)
	var to := get_canvas_item()
	for side in [-1.0, 1.0]:
		var near := Vector2(size.x / 2.0 + side * (w / 2.0 + 12.0 + r), y)
		var far := near + Vector2(side * reach, 0)
		draw_line(
			near + Vector2(side * r * 1.6, 1.5),
			far + Vector2(0, 1.5),
			Color(0, 0, 0, 0.5),
			3.0,
			true
		)
		draw_line(near + Vector2(side * r * 1.6, 0), far, Color(UiTheme.IRON_LIGHT, 0.8), 2.0, true)
		Ornament.rhombus(to, near, r, UiTheme.ACCENT_DARK)
		Ornament.rhombus(to, near, r * 0.45, UiTheme.INK)
		Ornament.rivet(to, far, r * 0.6)
