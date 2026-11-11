class_name UiTheme
extends RefCounted
## The game's UI in the new art: its colours and sizes, the theme files (THEME, edited in the
## editor) and the pieces the screens build from them.
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

const COIN := "res://assets/art/ui/coin.svg"
const FONT_PATH := "res://assets/art/fonts/%s-normal.woff2"
## Each font: its Latin file and its Cyrillic one.
const FONT_FILES := {
	"title": ["kurale-latin-400", "kurale-cyrillic-400"],
	"text": ["pt-sans-latin-400", "pt-sans-cyrillic-400"],
	"bold": ["pt-sans-latin-700", "pt-sans-cyrillic-700"],
}
## The game's theme, and the same with lower buttons for a menu of many.
const THEME := "res://assets/art/ui/theme.tres"
const COMPACT_THEME := "res://assets/art/ui/compact_theme.tres"

static var _fonts := {}

static var _coin: Texture2D


## A font of the new art: "title" (Kurale), "text" (PT Sans) or "bold" (PT Sans Bold). Its
## Cyrillic file and then the engine's own font fill in what its Latin file lacks. They are
## added here to the loaded file, which the theme files use too (a file cannot name the
## engine's font), and the file is kept so that it is not loaded again without them.
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


## A theme file (THEME, COMPACT_THEME, ...) with its fonts ready (font()).
static func theme(path: String) -> Theme:
	for kind in FONT_FILES:
		font(kind)
	return load(path)


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
	l.theme_type_variation = &"Heading"
	l.text = text_key
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if size != TITLE_SIZE:
		l.add_theme_font_size_override("font_size", size)
		l.add_theme_constant_override("outline_size", maxi(4, size / 9))
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
