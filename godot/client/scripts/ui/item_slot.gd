class_name ItemSlot
extends RefCounted
## Icon buttons of the Gear, Inventory and Skills pages: an icon of the new art
## (assets/art/icons, made by godot/tools/art/icons.py) in a dark hollow with a thin rim, a gold
## border on the chosen one. The same icons serve the shops, the HUD and the things on the ground.

const SHEET := "res://assets/art/icons/%s.svg"
const ICON := 28  # the size of an icon place, in the original pixels
const SCALE := 2
const ART := 128  # the size of an icon in its sheet

static var _sheets := {}
static var _icons := {}


static func button(node_name: String) -> Button:
	var b := Button.new()
	b.name = node_name
	b.custom_minimum_size = Vector2(ICON * SCALE + 8, ICON * SCALE + 8)
	b.expand_icon = true
	b.icon_alignment = HORIZONTAL_ALIGNMENT_CENTER
	b.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	b.add_theme_stylebox_override("normal", box(false))
	b.add_theme_stylebox_override(
		"hover", _place(UiTheme.SLOT.lightened(0.08), UiTheme.ACCENT_DARK, 2)
	)
	b.add_theme_stylebox_override("pressed", _place(UiTheme.SLOT, UiTheme.ACCENT, 2))
	b.add_theme_stylebox_override("hover_pressed", _place(UiTheme.SLOT, UiTheme.ACCENT, 2))
	b.add_theme_stylebox_override("disabled", _place(Color(UiTheme.SLOT, 0.6), UiTheme.SLOT_RIM, 1))
	return b


## The look of a place: a dark hollow with a thin rim; the chosen one has a brass border.
static func box(selected: bool) -> StyleBoxFlat:
	return _place(
		UiTheme.SLOT, UiTheme.ACCENT if selected else UiTheme.SLOT_RIM, 3 if selected else 1
	)


static func _place(fill: Color, rim: Color, width: int) -> StyleBoxFlat:
	var sb := UiTheme.box(fill, rim, width)
	sb.set_corner_radius_all(UiTheme.RADIUS)
	sb.set_content_margin_all(4)
	return sb


## Icon i of a sheet (tool, kibo, sungbo, shinki, skill, skillgray), in the order of the
## original sheets; its own texture with mipmaps, so it stays smooth at any size.
static func icon(sheet: String, i: int) -> Texture2D:
	if sheet.is_empty() or i < 0:
		return null
	var key := "%s %d" % [sheet, i]
	if not _icons.has(key):
		if not _sheets.has(sheet):
			_sheets[sheet] = (load(SHEET % sheet) as Texture2D).get_image()
		var all: Image = _sheets[sheet]
		if (i + 1) * ART > all.get_width():
			return null
		_icons[key] = smooth(all.get_region(Rect2i(i * ART, 0, ART, ART)))
	return _icons[key]


## A texture with mipmaps of a picture of the new art (smooth when drawn small).
static func smooth(image: Image) -> ImageTexture:
	var img := image.duplicate() as Image
	if img.is_compressed():
		img.decompress()
	img.convert(Image.FORMAT_RGBA8)
	img.generate_mipmaps()
	return ImageTexture.create_from_image(img)


## The icon of a carried thing, null for an empty place.
static func item_icon(id: int) -> Texture2D:
	var at: Array = Items.icon(id)
	return icon(at[0], at[1])
