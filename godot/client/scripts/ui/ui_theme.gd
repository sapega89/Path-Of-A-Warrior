extends RefCounted
## The game's UI theme in the new art, built in code so it is easy to read and change.
## A grim look of dark iron and worn leather: soot-black plates, tarnished brass, the dried red
## of blood, bone-white letters; the fonts of the new art (assets/art/fonts: Kurale for
## headings, PT Sans for text and buttons); plaques with hard corners and an iron rim, panels
## and windows of dark leather with a stitched seam and an iron rivet in each corner, headings
## between two iron rules, the forged backdrop of the menus. Base size 1280x720 (landscape 16:9).

const BG := Color("141416")  # soot, under the backdrop
const PANEL := Color("1d1b1a")  # dark leather
const BUTTON := Color("2a2623")
const BUTTON_HOVER := Color("3a332d")
const BUTTON_PRESSED := Color("6e211d")  # dried blood
const ACCENT := Color("b08d4a")  # tarnished brass
const ACCENT_DARK := Color("6f5a33")
const HIGHLIGHT := Color("dcc48e")  # the brass of the line in focus
const TEXT := Color("dcd3c2")  # bone
const TEXT_DIM := Color("8c867c")
const INK := Color("0f0d0c")  # outlines of the letters
const RED := Color("7e241f")
const BLUE := Color("2d3f57")
const SLOT := Color("0f0f10")  # the place of an icon
const SLOT_RIM := Color("38342f")
const IRON := Color("4e4a45")  # the rims of plaques and panels
const IRON_LIGHT := Color("8a847b")  # the worn top of a rivet
const THREAD := Color(0.62, 0.55, 0.43, 0.42)  # the stitches of a leather seam

const FONT_SIZE := 28
const TITLE_SIZE := 56
const RADIUS := 2

const FONT_PATH := "res://assets/art/fonts/%s-normal.woff2"
## Each font: its Latin file and its Cyrillic one.
const FONT_FILES := {
	"title": ["kurale-latin-400", "kurale-cyrillic-400"],
	"text": ["pt-sans-latin-400", "pt-sans-cyrillic-400"],
	"bold": ["pt-sans-latin-700", "pt-sans-cyrillic-700"],
}
const BACKDROP := preload("res://assets/art/shaders/ui_backdrop.gdshader")
const COIN := "res://assets/art/ui/coin.svg"

## Small pictures of the controls (SVG, drawn at their size).
# gdlint:ignore = max-line-length
const CHECK_OFF := '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect x="3" y="3" width="26" height="26" rx="1.5" fill="#0f0f10" stroke="#4e4a45" stroke-width="2.5"/></svg>'
# gdlint:ignore = max-line-length
const CHECK_ON := '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect x="3" y="3" width="26" height="26" rx="1.5" fill="#0f0f10" stroke="#b08d4a" stroke-width="2.5"/><path d="M8 16.5 L13.5 22 L24 9.5" fill="none" stroke="#b08d4a" stroke-width="4" stroke-linecap="square"/></svg>'
# gdlint:ignore = max-line-length
const ARROW_DOWN := '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 8 L12 17 L20 8" fill="none" stroke="#b08d4a" stroke-width="3.5" stroke-linecap="square" stroke-linejoin="miter"/></svg>'
# gdlint:ignore = max-line-length
const KNOB := '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><circle cx="16" cy="16" r="12.5" fill="#4e4a45" stroke="#0f0d0c" stroke-width="2.5"/><circle cx="14" cy="13.5" r="7" fill="#8a847b"/><circle cx="16" cy="16" r="4" fill="#b08d4a"/></svg>'
# gdlint:ignore = max-line-length
const CROSS := '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M6 6 L18 18 M18 6 L6 18" stroke="#b08d4a" stroke-width="3.5" stroke-linecap="square"/></svg>'

static var _fonts := {}
static var _coin: Texture2D


## A font of the new art: "title" (Kurale), "text" (PT Sans) or "bold" (PT Sans Bold). Its
## Cyrillic file and then the engine's own font fill in what its Latin file lacks.
static func font(kind: String) -> Font:
	if not _fonts.has(kind):
		var files: Array = FONT_FILES[kind]
		var main: FontFile = load(FONT_PATH % files[0])
		var rest: Array[Font] = [load(FONT_PATH % files[1]) as Font]
		if ThemeDB.fallback_font != null:
			rest.append(ThemeDB.fallback_font)
		main.fallbacks = rest
		_fonts[kind] = main
	return _fonts[kind]


## A plaque: hard corners, a rim, room for its text.
static func box(color: Color, border: Color = Color.TRANSPARENT, width: int = 0) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = color
	sb.border_color = border
	sb.set_border_width_all(width)
	sb.set_corner_radius_all(RADIUS)
	sb.anti_aliasing = true
	sb.set_content_margin_all(10)
	sb.content_margin_left = 20
	sb.content_margin_right = 20
	return sb


## A plaque of a button: as box(), with a heavy shadow under it.
static func plaque(color: Color, border: Color, width: int) -> StyleBoxFlat:
	var sb := box(color, border, width)
	sb.shadow_color = Color(0, 0, 0, 0.5)
	sb.shadow_size = 5
	sb.shadow_offset = Vector2(0, 3)
	return sb


## The ring of the control in focus, drawn over its plaque.
static func focus_ring() -> StyleBoxFlat:
	var sb := box(Color.TRANSPARENT, ACCENT, 3)
	sb.draw_center = false
	sb.set_expand_margin_all(2)
	sb.set_corner_radius_all(RADIUS + 2)
	return sb


static func build() -> Theme:
	var t := Theme.new()
	t.default_font = font("text")
	t.default_font_size = FONT_SIZE

	t.set_font("font", "Button", font("bold"))
	t.set_stylebox("normal", "Button", plaque(BUTTON, IRON, 2))
	t.set_stylebox("hover", "Button", plaque(BUTTON_HOVER, ACCENT_DARK, 2))
	t.set_stylebox("pressed", "Button", plaque(BUTTON_PRESSED, ACCENT, 2))
	t.set_stylebox("hover_pressed", "Button", plaque(BUTTON_PRESSED, HIGHLIGHT, 2))
	t.set_stylebox("disabled", "Button", box(Color(BUTTON, 0.6), SLOT_RIM, 1))
	t.set_stylebox("focus", "Button", focus_ring())
	t.set_color("font_color", "Button", TEXT)
	t.set_color("font_hover_color", "Button", TEXT)
	t.set_color("font_focus_color", "Button", HIGHLIGHT)
	t.set_color("font_pressed_color", "Button", TEXT)
	t.set_color("font_hover_pressed_color", "Button", TEXT)
	t.set_color("font_disabled_color", "Button", TEXT_DIM)
	# an ink outline: a flat button (Skip) stays readable over the backdrop's band
	t.set_color("font_outline_color", "Button", INK)
	t.set_constant("outline_size", "Button", 5)

	t.set_color("font_color", "Label", TEXT)
	t.set_stylebox("panel", "PanelContainer", PanelBox.new())
	t.set_stylebox("panel", "Panel", PanelBox.new())

	for type in ["OptionButton", "CheckBox"]:
		t.set_stylebox("focus", type, focus_ring())
		t.set_color("font_color", type, TEXT)
		t.set_color("font_hover_color", type, TEXT)
		t.set_color("font_focus_color", type, HIGHLIGHT)
		t.set_color("font_pressed_color", type, TEXT)
		t.set_font("font", type, font("bold"))
	t.set_stylebox("normal", "OptionButton", plaque(BUTTON, IRON, 2))
	t.set_stylebox("hover", "OptionButton", plaque(BUTTON_HOVER, ACCENT_DARK, 2))
	t.set_stylebox("pressed", "OptionButton", plaque(BUTTON_PRESSED, ACCENT, 2))
	for style in ["normal", "hover", "pressed", "hover_pressed"]:
		var sb := box(Color.TRANSPARENT)
		sb.draw_center = false
		t.set_stylebox(style, "CheckBox", sb)
	var on := _icon(CHECK_ON, 30)
	var off := _icon(CHECK_OFF, 30)
	for icon_name in ["checked", "radio_checked"]:
		t.set_icon(icon_name, "CheckBox", on)
	for icon_name in ["unchecked", "radio_unchecked"]:
		t.set_icon(icon_name, "CheckBox", off)
	t.set_icon("arrow", "OptionButton", _icon(ARROW_DOWN, 18))
	t.set_icon("grabber", "HSlider", _icon(KNOB, 26))
	t.set_icon("grabber_highlight", "HSlider", _icon(KNOB, 26))

	t.set_stylebox("slider", "HSlider", _strip(SLOT, SLOT_RIM, 8))
	t.set_stylebox("grabber_area", "HSlider", _strip(ACCENT_DARK, ACCENT_DARK, 8))
	t.set_stylebox("grabber_area_highlight", "HSlider", _strip(ACCENT, ACCENT, 8))
	t.set_stylebox("focus", "HSlider", focus_ring())

	t.set_stylebox("scroll", "VScrollBar", _strip(Color(SLOT, 0.8), Color.TRANSPARENT, 10))
	t.set_stylebox("grabber", "VScrollBar", _strip(IRON, IRON, 10))
	t.set_stylebox("grabber_highlight", "VScrollBar", _strip(IRON_LIGHT, IRON_LIGHT, 10))
	t.set_stylebox("grabber_pressed", "VScrollBar", _strip(ACCENT, ACCENT, 10))

	var field := box(SLOT, SLOT_RIM, 2)
	t.set_stylebox("normal", "LineEdit", field)
	t.set_stylebox("focus", "LineEdit", focus_ring())
	t.set_stylebox("read_only", "LineEdit", box(Color(SLOT, 0.6), SLOT_RIM, 1))
	t.set_color("font_color", "LineEdit", TEXT)
	t.set_color("font_placeholder_color", "LineEdit", Color(TEXT_DIM, 0.7))
	t.set_color("caret_color", "LineEdit", HIGHLIGHT)
	t.set_color("selection_color", "LineEdit", Color(ACCENT, 0.35))

	# the dialogs (embedded windows): a panel with its rivets, the title in brass
	var frame := PanelBox.new()
	frame.outset = [8.0, 44.0, 8.0, 8.0]
	t.set_stylebox("embedded_border", "Window", frame)
	t.set_stylebox("embedded_unfocused_border", "Window", frame)
	t.set_font("title_font", "Window", font("title"))
	t.set_font_size("title_font_size", "Window", 30)
	t.set_color("title_color", "Window", ACCENT)
	t.set_color("title_outline_modulate", "Window", INK)
	t.set_constant("title_height", "Window", 40)
	t.set_icon("close", "Window", _icon(CROSS, 20))
	t.set_icon("close_pressed", "Window", _icon(CROSS, 20))
	var inside := box(Color(PANEL, 0.96))
	inside.set_corner_radius_all(0)
	inside.set_content_margin_all(12)
	t.set_stylebox("panel", "AcceptDialog", inside)
	t.set_constant("buttons_separation", "AcceptDialog", 12)

	t.set_stylebox("panel", "PopupMenu", PanelBox.new())
	t.set_stylebox("hover", "PopupMenu", box(BUTTON_HOVER, ACCENT_DARK, 1))
	t.set_color("font_color", "PopupMenu", TEXT)
	t.set_color("font_hover_color", "PopupMenu", HIGHLIGHT)
	return t


## A picture of an SVG at px pixels wide.
static func _icon(svg: String, px: int) -> ImageTexture:
	var img := Image.new()
	img.load_svg_from_string(svg, px / 32.0 if svg.contains("0 0 32 32") else px / 24.0)
	return ImageTexture.create_from_image(img)


## A strip with hard ends (a slider, a scroll bar).
static func _strip(color: Color, border: Color, thickness: int) -> StyleBoxFlat:
	var sb := box(color, border, 1 if border.a > 0.0 else 0)
	sb.set_corner_radius_all(mini(RADIUS, thickness / 2))
	sb.set_content_margin_all(thickness / 2)
	return sb


## The game's theme with lower buttons, for a menu of many.
static func compact() -> Theme:
	var t := build()
	for style in ["normal", "hover", "pressed", "disabled", "focus"]:
		var sb := t.get_stylebox(style, "Button").duplicate() as StyleBoxFlat
		sb.content_margin_top = 4
		sb.content_margin_bottom = 4
		t.set_stylebox(style, "Button", sb)
	return t


## The forged backdrop of the menus: soot-black, mottled like old leather and darker to the
## edges, a riveted iron strip along the top and the bottom
## (assets/art/shaders/ui_backdrop.gdshader).
static func backdrop() -> ColorRect:
	var bg := ColorRect.new()
	bg.name = "Backdrop"
	bg.color = BG
	var m := ShaderMaterial.new()
	m.shader = BACKDROP
	bg.material = m
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return bg


## A centred column for menu screens.
static func menu_column(parent: Control, width: int = 460) -> VBoxContainer:
	var center := CenterContainer.new()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	parent.add_child(center)
	var col := VBoxContainer.new()
	col.custom_minimum_size = Vector2(width, 0)
	col.add_theme_constant_override("separation", 8)
	center.add_child(col)
	return col


## A heading in Kurale, tarnished brass with a dark outline, between two iron rules.
static func heading(text_key: String, size: int = TITLE_SIZE) -> Label:
	var l := Heading.new()
	l.text = text_key
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.add_theme_font_override("font", font("title"))
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", ACCENT)
	l.add_theme_color_override("font_outline_color", INK)
	l.add_theme_constant_override("outline_size", maxi(4, size / 9))
	l.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.45))
	l.add_theme_constant_override("shadow_offset_y", 3)
	return l


## A centred line of text set from code (already translated), wrapped when long.
static func note(node_name: String, min_height: int = 0) -> Label:
	var l := Label.new()
	l.name = node_name
	l.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	l.custom_minimum_size = Vector2(0, min_height)
	return l


## The gold coin of the new art (assets/art/ui/coin.svg), smooth at any size.
static func coin() -> Texture2D:
	if _coin == null:
		var img := Image.new()
		img.load_svg_from_string(FileAccess.get_file_as_string(COIN), 1.0)
		img.generate_mipmaps()
		_coin = ImageTexture.create_from_image(img)
	return _coin


## The coin as a picture in a row (a purse: the coin and the gold after it).
static func coin_rect() -> TextureRect:
	var r := TextureRect.new()
	r.name = "Coin"
	r.texture = coin()
	r.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	r.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	r.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	r.custom_minimum_size = Vector2(56, 40)
	return r


## The gold coin and a number after it (the row's child "Value"), centred.
static func gold_row(node_name: String) -> HBoxContainer:
	var row := HBoxContainer.new()
	row.name = node_name
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	row.add_child(coin_rect())
	var value := Label.new()
	value.name = "Value"
	value.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	value.custom_minimum_size = Vector2(160, 0)
	value.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	row.add_child(value)
	return row


## A rhombus (a folk lozenge) of half-width r at c, its edge smoothed.
static func rhombus(to: RID, c: Vector2, r: float, color: Color) -> void:
	Ornament.rhombus(to, c, r, color)


## An iron rivet of radius r at c.
static func rivet(to: RID, c: Vector2, r: float) -> void:
	Ornament.rivet(to, c, r)


## The drawing of the ornaments (the classes below share it).
class Ornament:
	static var _leather: Texture2D

	static func rhombus(to: RID, c: Vector2, r: float, color: Color) -> void:
		var points := PackedVector2Array(
			[c + Vector2(0, -r), c + Vector2(r, 0), c + Vector2(0, r), c + Vector2(-r, 0)]
		)
		RenderingServer.canvas_item_add_polygon(to, points, PackedColorArray([color]))
		points.append(points[0])
		RenderingServer.canvas_item_add_polyline(to, points, PackedColorArray([color]), 1.0, true)

	static func flat(color: Color, border: Color, width: int, radius: int) -> StyleBoxFlat:
		var sb := StyleBoxFlat.new()
		sb.bg_color = color
		sb.border_color = border
		sb.set_border_width_all(width)
		sb.set_corner_radius_all(radius)
		sb.anti_aliasing = true
		return sb

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
		disc(to, c, r, IRON)
		disc(to, c - Vector2(0.25, 0.3) * r, r * 0.55, IRON_LIGHT)
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


## The plate of a panel or a window: dark leather in an iron rim, a stitched seam inside it and
## an iron rivet in each corner.
class PanelBox:
	extends StyleBox
	var plate: StyleBoxFlat
	## How far it reaches out of its rect: left, top, right, bottom (a window's frame and title).
	var outset := [0.0, 0.0, 0.0, 0.0]

	func _init() -> void:
		plate = Ornament.flat(Color(PANEL, 0.97), IRON, 3, RADIUS)
		plate.shadow_color = Color(0, 0, 0, 0.55)
		plate.shadow_size = 10
		plate.shadow_offset = Vector2(0, 4)
		set_content_margin_all(14)
		content_margin_left = 22
		content_margin_right = 22

	func _get_draw_rect(rect: Rect2) -> Rect2:
		return rect.grow_individual(outset[0], outset[1], outset[2], outset[3])

	func _draw(to: RID, rect: Rect2) -> void:
		rect = _get_draw_rect(rect)
		plate.draw(to, rect)
		if rect.size.x < 40 or rect.size.y < 40:
			return
		Ornament.grain(to, rect.grow(-3))
		Ornament.seam(to, rect.grow(-8), THREAD)
		for corner in [
			rect.position,
			Vector2(rect.end.x, rect.position.y),
			rect.end,
			Vector2(rect.position.x, rect.end.y)
		]:
			var c: Vector2 = corner + (rect.get_center() - corner).sign() * 8.0
			Ornament.rivet(to, c, 4.5)


## A heading: its text with an iron rule on each side, a rhombus of brass near the words and a
## rivet at the far end.
class Heading:
	extends Label

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
			draw_line(near + Vector2(side * r * 1.6, 0), far, Color(IRON_LIGHT, 0.8), 2.0, true)
			Ornament.rhombus(to, near, r, ACCENT_DARK)
			Ornament.rhombus(to, near, r * 0.45, INK)
			Ornament.rivet(to, far, r * 0.6)
