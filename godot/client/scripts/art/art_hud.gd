extends Control
## HUD in the new art: a round portrait drawn live from the hero's model, health and
## spirit bars, the skill keys with folk-print icons, the purse and the place name.
## Shapes and colours come from the palette; icons are SVG (assets/art/ui).

const ArtKit := preload("res://scripts/art/art_kit.gd")
const UI := "res://assets/art/ui/%s.svg"
const SKILLS := ["sabre", "shield", "fire", "wind", "potion"]
const PLACE_NAMES := {"camp": "Корсунь", "battle": "Крута балка"}

const INK := Color("0F0D0C")
const GOLD := Color("B08D4A")  # tarnished brass
const GOLD_DARK := Color("4E4A45")  # iron
const PAPER := Color("DCD3C2")
const DUSK := Color("1D1B1A")
const RED := Color("7E241F")
const BLUE := Color("2D3F57")

const PORTRAIT_MASK := """
shader_type canvas_item;
void fragment() {
	float d = distance(UV, vec2(0.5));
	COLOR = texture(TEXTURE, UV);
	COLOR.a *= 1.0 - smoothstep(0.47, 0.5, d);
}
"""

var hero: Node3D
var title_font: Font
var text_font: Font
var bold_font: Font
var portrait_view: SubViewport
var portrait_camera: Camera3D
var screen := Vector2(1280, 720)


static func icon(icon_name: String, px: int) -> Texture2D:
	var f := FileAccess.open(UI % icon_name, FileAccess.READ)
	if f == null:
		return null
	var svg := f.get_as_text()
	var img := Image.new()
	var probe := Image.new()
	probe.load_svg_from_string(svg, 1.0)
	var scale_by := float(px) / float(maxi(probe.get_width(), 1))
	img.load_svg_from_string(svg, scale_by)
	return ImageTexture.create_from_image(img)


static func font(files: Array) -> Font:
	var main: FontFile = load(files[0])
	var rest: Array[Font] = []
	for i in range(1, files.size()):
		rest.append(load(files[i]))
	main.fallbacks = rest
	return main


func setup(hero_node: Node3D, place: String) -> void:
	hero = hero_node
	screen = get_viewport_rect().size
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	title_font = font(
		[
			"res://assets/art/fonts/kurale-latin-400-normal.woff2",
			"res://assets/art/fonts/kurale-cyrillic-400-normal.woff2"
		]
	)
	text_font = font(
		[
			"res://assets/art/fonts/pt-sans-latin-400-normal.woff2",
			"res://assets/art/fonts/pt-sans-cyrillic-400-normal.woff2"
		]
	)
	bold_font = font(
		[
			"res://assets/art/fonts/pt-sans-latin-700-normal.woff2",
			"res://assets/art/fonts/pt-sans-cyrillic-700-normal.woff2"
		]
	)
	_portrait()
	_bars()
	_skills(place)
	_purse()
	_place(PLACE_NAMES.get(place, place))


func _box(bg: Color, border: Color, width: int, radius: int) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(width)
	sb.set_corner_radius_all(radius)
	sb.anti_aliasing = true
	return sb


func _label(text: String, f: Font, size: int, color: Color, outline := 0) -> Label:
	var l := Label.new()
	l.text = text
	l.add_theme_font_override("font", f)
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", color)
	if outline > 0:
		l.add_theme_color_override("font_outline_color", INK)
		l.add_theme_constant_override("outline_size", outline)
	return l


# -- portrait ---------------------------------------------------------------------------
func _portrait() -> void:
	var ring := Panel.new()
	ring.position = Vector2(18, 14)
	ring.size = Vector2(132, 132)
	ring.add_theme_stylebox_override("panel", _box(DUSK, GOLD_DARK, 5, 66))
	add_child(ring)
	portrait_view = SubViewport.new()
	portrait_view.size = Vector2i(256, 256)
	portrait_view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	portrait_view.msaa_3d = Viewport.MSAA_4X
	add_child(portrait_view)
	portrait_camera = Camera3D.new()
	portrait_camera.fov = 24.0
	portrait_view.add_child(portrait_camera)
	var face := TextureRect.new()
	face.texture = portrait_view.get_texture()
	face.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	face.position = Vector2(24, 20)
	face.size = Vector2(120, 120)
	var mask := ShaderMaterial.new()
	var sh := Shader.new()
	sh.code = PORTRAIT_MASK
	mask.shader = sh
	face.material = mask
	add_child(face)
	var level := Panel.new()
	level.position = Vector2(110, 104)
	level.size = Vector2(44, 44)
	level.add_theme_stylebox_override("panel", _box(RED, GOLD, 4, 22))
	add_child(level)
	var num := _label("12", bold_font, 22, PAPER, 4)
	num.position = Vector2(110, 108)
	num.size = Vector2(44, 32)
	num.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	add_child(num)
	var orn := TextureRect.new()
	orn.texture = icon("ornament", 300)
	orn.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	orn.position = Vector2(150, 108)
	orn.size = Vector2(300, 75)
	orn.modulate = Color(1, 1, 1, 0.95)
	add_child(orn)


func _process(_delta: float) -> void:
	if hero == null or portrait_camera == null or not is_instance_valid(hero):
		return
	var forward := Vector3(sin(hero.rotation.y), 0.0, cos(hero.rotation.y))
	var head := hero.global_position + Vector3(0, 1.66, 0)
	portrait_camera.global_position = (
		head + forward * 1.25 + Vector3(0.25, 0.12, 0).rotated(Vector3.UP, hero.rotation.y)
	)
	portrait_camera.look_at(head + Vector3(0, 0.02, 0), Vector3.UP)


# -- bars -------------------------------------------------------------------------------
func _bars() -> void:
	var name_label := _label("Козак Іван", title_font, 30, PAPER, 6)
	name_label.position = Vector2(164, 14)
	add_child(name_label)
	_bar(Vector2(164, 56), 300, RED, 0.78, "117 / 150")
	_bar(Vector2(164, 88), 240, BLUE, 0.55, "33 / 60")


func _bar(at: Vector2, width: float, fill: Color, value: float, text: String) -> void:
	var bar := ProgressBar.new()
	bar.position = at
	bar.size = Vector2(width, 26)
	bar.show_percentage = false
	bar.max_value = 1.0
	bar.value = value
	bar.add_theme_stylebox_override("background", _box(DUSK.lerp(INK, 0.3), GOLD_DARK, 3, 2))
	var f := _box(fill, Color(0, 0, 0, 0), 0, 1)
	f.set_expand_margin_all(-3)
	bar.add_theme_stylebox_override("fill", f)
	add_child(bar)
	var shine := ColorRect.new()
	shine.color = Color(1, 1, 1, 0.16)
	shine.position = at + Vector2(6, 5)
	shine.size = Vector2((width - 12) * value, 5)
	add_child(shine)
	var l := _label(text, bold_font, 17, PAPER, 4)
	l.position = at
	l.size = Vector2(width, 26)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	add_child(l)


# -- skills -----------------------------------------------------------------------------
func _skills(place: String) -> void:
	var slot := 78.0
	var gap := 12.0
	var count := SKILLS.size()
	var start := Vector2(screen.x - 24 - count * slot - (count - 1) * gap, screen.y - 24 - slot)
	var plate := Panel.new()
	plate.position = start - Vector2(14, 14)
	plate.size = Vector2(count * slot + (count - 1) * gap + 28, slot + 28)
	plate.add_theme_stylebox_override("panel", _box(Color(DUSK, 0.8), GOLD_DARK, 2, 3))
	add_child(plate)
	for i in count:
		var at := start + Vector2(i * (slot + gap), 0)
		var p := Panel.new()
		p.position = at
		p.size = Vector2(slot, slot)
		var active := i == 0 and place == "battle"
		p.add_theme_stylebox_override(
			"panel", _box(Color("2a2623"), GOLD if active else GOLD_DARK, 4 if active else 3, 2)
		)
		add_child(p)
		var t := TextureRect.new()
		t.texture = icon(SKILLS[i], 128)
		t.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		t.position = at + Vector2(9, 9)
		t.size = Vector2(slot - 18, slot - 18)
		add_child(t)
		if i == 2:
			var cool := ColorRect.new()
			cool.color = Color(DUSK, 0.66)
			cool.position = at + Vector2(4, 4)
			cool.size = Vector2(slot - 8, (slot - 8) * 0.6)
			add_child(cool)
			var n := _label("4", title_font, 34, PAPER, 6)
			n.position = at
			n.size = Vector2(slot, slot)
			n.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			n.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
			add_child(n)
		var key := _label(str(i + 1), bold_font, 16, GOLD, 4)
		key.position = at + Vector2(slot - 20, slot - 24)
		add_child(key)


# -- purse and place --------------------------------------------------------------------
func _purse() -> void:
	var t := TextureRect.new()
	t.texture = icon("coin", 64)
	t.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	t.position = Vector2(screen.x - 200, 22)
	t.size = Vector2(40, 40)
	add_child(t)
	var l := _label("1 250", title_font, 30, Color("F2D58A"), 6)
	l.position = Vector2(screen.x - 152, 20)
	add_child(l)


func _place(text: String) -> void:
	var ribbon := PanelContainer.new()
	var sb := _box(PAPER, RED, 3, 4)
	sb.content_margin_left = 26
	sb.content_margin_right = 26
	sb.content_margin_top = 4
	sb.content_margin_bottom = 6
	ribbon.add_theme_stylebox_override("panel", sb)
	var l := _label(text, title_font, 28, INK)
	ribbon.add_child(l)
	add_child(ribbon)
	ribbon.position = Vector2(screen.x / 2.0 - 90, 18)
	ribbon.reset_size()
	ribbon.position.x = screen.x / 2.0 - ribbon.size.x / 2.0


func _draw() -> void:
	# touch stick, as on a phone
	var c := Vector2(130, screen.y - 130)
	draw_circle(c, 86, Color(DUSK, 0.28))
	draw_arc(c, 86, 0, TAU, 64, Color(PAPER, 0.45), 3.0, true)
	draw_circle(c + Vector2(18, -10), 34, Color(PAPER, 0.35))
	draw_arc(c + Vector2(18, -10), 34, 0, TAU, 48, Color(GOLD, 0.8), 3.0, true)
