class_name Ornament
extends RefCounted
## The drawing of the ornaments (the classes below share it).
static var _leather: Texture2D


static func rhombus(to: RID, c: Vector2, r: float, color: Color) -> void:
	var points := PackedVector2Array(
		[c + Vector2(0, -r), c + Vector2(r, 0), c + Vector2(0, r), c + Vector2(-r, 0)]
	)
	RenderingServer.canvas_item_add_polygon(to, points, PackedColorArray([color]))
	points.append(points[0])
	RenderingServer.canvas_item_add_polyline(to, points, PackedColorArray([color]), 1.0, true)


## A round dot of radius r at c, its edge smoothed.
static func disc(to: RID, c: Vector2, r: float, color: Color) -> void:
	var points := PackedVector2Array()
	var n := clampi(int(r * 2.5), 10, 32)
	for i in n:
		points.append(c + Vector2.from_angle(TAU * i / n) * r)
	RenderingServer.canvas_item_add_polygon(to, points, PackedColorArray([color]))
	points.append(points[0])
	RenderingServer.canvas_item_add_polyline(to, points, PackedColorArray([color]), 1.0, true)


## An iron rivet of radius r at c: a dark ring, the dome, its worn top lit from the upper left.
static func rivet(to: RID, c: Vector2, r: float) -> void:
	disc(to, c + Vector2(0.6, 1.0) * r * 0.3, r + 1.0, Color(0, 0, 0, 0.55))
	disc(to, c, r, UiTheme.IRON)
	disc(to, c - Vector2(0.25, 0.3) * r, r * 0.55, UiTheme.IRON_LIGHT)
	disc(to, c - Vector2(0.35, 0.4) * r, r * 0.2, Color(1, 1, 1, 0.35))


## A seam of stitches along the rect's edge.
static func seam(to: RID, rect: Rect2, color: Color) -> void:
	var stitches := PackedVector2Array()
	var edges := [
		[rect.position, Vector2(rect.end.x, rect.position.y)],
		[Vector2(rect.end.x, rect.position.y), rect.end],
		[rect.end, Vector2(rect.position.x, rect.end.y)],
		[Vector2(rect.position.x, rect.end.y), rect.position]
	]
	for e in edges:
		var a: Vector2 = e[0]
		var b: Vector2 = e[1]
		var n := maxi(1, int(a.distance_to(b) / 10.0))
		for i in n:
			stitches.append(a.lerp(b, (i + 0.15) / n))
			stitches.append(a.lerp(b, (i + 0.6) / n))
	RenderingServer.canvas_item_add_multiline(to, stitches, PackedColorArray([color]), 1.5)


## The grain of old leather over the rect: soft blotches and fine creases, in dark see-through
## spots, the same picture repeated (made once).
static func grain(to: RID, rect: Rect2) -> void:
	if _leather == null:
		_leather = _make_leather()
	var tile := _leather.get_size()
	var y := rect.position.y
	while y < rect.end.y:
		var x := rect.position.x
		var h := minf(tile.y, rect.end.y - y)
		while x < rect.end.x:
			var w := minf(tile.x, rect.end.x - x)
			RenderingServer.canvas_item_add_texture_rect_region(
				to, Rect2(x, y, w, h), _leather.get_rid(), Rect2(0, 0, w, h)
			)
			x += tile.x
		y += tile.y


static func _make_leather() -> Texture2D:
	var cells := FastNoiseLite.new()
	cells.noise_type = FastNoiseLite.TYPE_CELLULAR
	cells.cellular_return_type = FastNoiseLite.RETURN_DISTANCE2_SUB
	cells.frequency = 0.09
	cells.seed = 7
	var blotches := FastNoiseLite.new()
	blotches.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
	blotches.frequency = 0.012
	blotches.fractal_octaves = 3
	blotches.seed = 3
	var a := cells.get_seamless_image(256, 256)
	var b := blotches.get_seamless_image(256, 256)
	var img := Image.create(256, 256, false, Image.FORMAT_RGBA8)
	for y in 256:
		for x in 256:
			var crease := 1.0 - smoothstep(0.0, 0.35, a.get_pixel(x, y).r)
			var patch := smoothstep(0.35, 0.8, b.get_pixel(x, y).r)
			img.set_pixel(x, y, Color(0, 0, 0, crease * 0.22 + patch * 0.2))
	return ImageTexture.create_from_image(img)
