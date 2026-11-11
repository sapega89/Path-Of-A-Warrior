class_name HudPanel
extends Panel
## The panel at the bottom of the mission's HUD under the orbs: a dark plate with an iron rim
## along its top (its theme style), two thin lines and a riveted iron bar between the orbs with a
## folk lozenge in its middle.

const WIDTH := 240.0  # on the 240x320 grid
const TOP := 3.0  # the plate starts this far below the panel's row 0


func _draw() -> void:
	var k := size.x / WIDTH
	var origin := Vector2(0, -TOP * k)
	var line := Color(UiTheme.IRON_LIGHT, 0.4)
	for y in [12.0, 54.0]:
		draw_line(origin + Vector2(52, y) * k, origin + Vector2(188, y) * k, line, k, true)
	var to := get_canvas_item()
	var bar := Rect2(origin + Vector2(54, 29) * k, Vector2(132, 8) * k)
	draw_style_box(get_theme_stylebox("iron"), bar)
	draw_line(
		bar.position + Vector2(k, k),
		Vector2(bar.end.x - k, bar.position.y + k),
		Color(UiTheme.IRON_LIGHT, 0.5),
		k,
		true
	)
	for i in range(-4, 5):
		var c := origin + Vector2(120 + i * 15, 33) * k
		if i == 0:
			UiTheme.rhombus(to, c, 6.5 * k, UiTheme.INK)
			UiTheme.rhombus(to, c, 5.5 * k, UiTheme.ACCENT_DARK)
			UiTheme.rhombus(to, c, 2.5 * k, UiTheme.RED)
		else:
			UiTheme.rivet(to, c, 2.6 * k)
	for side in [-1, 1]:
		UiTheme.rivet(to, origin + Vector2(120 + side * 66, 12) * k, 1.8 * k)
		UiTheme.rivet(to, origin + Vector2(120 + side * 66, 54) * k, 1.8 * k)
