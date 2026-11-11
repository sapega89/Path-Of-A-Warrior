class_name ItemSlot
extends RefCounted
## Icon buttons of the Gear, Inventory and Skills pages (scenes/ui/item_slot.tscn): an icon of
## the new art (assets/art/icons, made by godot/tools/art/icons.py) in a dark hollow with a thin
## rim, a gold border on the chosen one (the theme's ItemSlot and ItemSlotChosen). The same icons
## serve the shops, the HUD and the things on the ground.

const SCENE := "res://scenes/ui/item_slot.tscn"
const PLAIN := &"ItemSlot"
const CHOSEN := &"ItemSlotChosen"
const SHEET := "res://assets/art/icons/%s.svg"
const ART := 128  # the size of an icon in its sheet

static var _sheets := {}
static var _icons := {}


static func button(node_name: String) -> Button:
	var b: Button = (load(SCENE) as PackedScene).instantiate()
	b.name = node_name
	return b


## Gives a place the brass border of the chosen one, or takes it away.
static func choose(place: Button, chosen: bool) -> void:
	place.theme_type_variation = CHOSEN if chosen else PLAIN


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
