extends Control
## The round stage under the hero on the Gear page: a dark ellipse with an iron rim and rivets
## around it.


func _draw() -> void:
	var c := size / 2.0
	var rx := size.x / 2.0
	var ry := size.y / 2.0
	var rim := PackedVector2Array()
	for i in 49:
		var t := TAU * i / 48.0
		rim.append(c + Vector2(cos(t) * rx, sin(t) * ry))
	draw_colored_polygon(rim, Color(UiTheme.SLOT, 0.85))
	draw_polyline(rim, UiTheme.IRON, 2.0, true)
	var inner := PackedVector2Array()
	for p in rim:
		inner.append(c + (p - c) * 0.8)
	draw_polyline(inner, Color(UiTheme.IRON_LIGHT, 0.25), 1.0, true)
	for i in 8:
		var t := TAU * (i + 0.5) / 8.0
		UiTheme.rivet(get_canvas_item(), c + Vector2(cos(t) * rx * 0.9, sin(t) * ry * 0.9), 2.8)
