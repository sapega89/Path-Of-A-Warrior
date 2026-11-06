extends RefCounted
## Icon buttons of the Gear, Inventory and Skills pages: a 28 px original icon drawn twice
## as big on a dark place, a gold border on the chosen one.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Items := preload("res://scripts/core/items.gd")
const UI := "res://assets/original/ui/%s.png"
const ICON := 28
const SCALE := 2

static var _sheets := {}


static func button(node_name: String) -> Button:
	var b := Button.new()
	b.name = node_name
	b.custom_minimum_size = Vector2(ICON * SCALE + 8, ICON * SCALE + 8)
	b.expand_icon = true
	b.icon_alignment = HORIZONTAL_ALIGNMENT_CENTER
	b.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	b.add_theme_stylebox_override("normal", box(false))
	return b


## The look of a place; the chosen one has a gold border.
static func box(selected: bool) -> StyleBoxFlat:
	var sb := UiTheme.box(UiTheme.BUTTON, UiTheme.ACCENT if selected else Color.TRANSPARENT, 3 if selected else 0)
	sb.set_content_margin_all(4)
	return sb


## Icon i of a sheet of 28 px icons (tool, kibo, sungbo, shinki, skill, skillgray).
static func icon(sheet: String, i: int) -> Texture2D:
	if sheet.is_empty() or i < 0:
		return null
	if not _sheets.has(sheet):
		_sheets[sheet] = load(UI % sheet)
	var t := AtlasTexture.new()
	t.atlas = _sheets[sheet]
	t.region = Rect2(i * ICON, 0, ICON, ICON)
	return t


## The icon of a carried thing, null for an empty place.
static func item_icon(id: int) -> Texture2D:
	var at: Array = Items.icon(id)
	return icon(at[0], at[1])
