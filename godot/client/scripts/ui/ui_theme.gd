extends RefCounted
## The game's UI theme, built in code so it is easy to read and change.
## Base size 1280x720 (decision R3: landscape 16:9). Placeholder look until the real art arrives (decision R7).

const BG := Color("1d1a24")
const PANEL := Color("2b2633")
const BUTTON := Color("3a3345")
const BUTTON_HOVER := Color("4a4158")
const BUTTON_PRESSED := Color("2b2633")
const ACCENT := Color("c59a3e")
const TEXT := Color("e8e2d4")
const TEXT_DIM := Color("9a93a6")

const FONT_SIZE := 28
const TITLE_SIZE := 56


static func box(color: Color, border: Color = Color.TRANSPARENT, width: int = 0) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = color
	sb.border_color = border
	sb.set_border_width_all(width)
	sb.set_content_margin_all(10)
	sb.content_margin_left = 20
	sb.content_margin_right = 20
	return sb


static func build() -> Theme:
	var t := Theme.new()
	t.default_font_size = FONT_SIZE

	t.set_stylebox("normal", "Button", box(BUTTON))
	t.set_stylebox("hover", "Button", box(BUTTON_HOVER))
	t.set_stylebox("pressed", "Button", box(BUTTON_PRESSED, ACCENT, 1))
	t.set_stylebox("disabled", "Button", box(PANEL))
	t.set_stylebox("focus", "Button", box(Color.TRANSPARENT, ACCENT, 2))
	t.set_color("font_color", "Button", TEXT)
	t.set_color("font_hover_color", "Button", TEXT)
	t.set_color("font_focus_color", "Button", ACCENT)
	t.set_color("font_pressed_color", "Button", ACCENT)
	t.set_color("font_disabled_color", "Button", TEXT_DIM)

	t.set_color("font_color", "Label", TEXT)
	t.set_stylebox("panel", "PanelContainer", box(PANEL, ACCENT, 1))

	for type in ["OptionButton", "CheckBox"]:
		t.set_stylebox("focus", type, box(Color.TRANSPARENT, ACCENT, 2))
		t.set_color("font_color", type, TEXT)
		t.set_color("font_focus_color", type, ACCENT)
	t.set_stylebox("normal", "OptionButton", box(BUTTON))
	t.set_stylebox("hover", "OptionButton", box(BUTTON_HOVER))
	t.set_stylebox("pressed", "OptionButton", box(BUTTON_PRESSED, ACCENT, 1))

	t.set_stylebox("slider", "HSlider", box(BUTTON))
	t.set_stylebox("grabber_area", "HSlider", box(ACCENT))
	t.set_stylebox("grabber_area_highlight", "HSlider", box(ACCENT))
	t.set_stylebox("focus", "HSlider", box(Color.TRANSPARENT, ACCENT, 2))
	return t


## The game's theme with lower buttons, for a menu of many.
static func compact() -> Theme:
	var t := build()
	for style in ["normal", "hover", "pressed", "disabled", "focus"]:
		var sb := t.get_stylebox(style, "Button").duplicate() as StyleBoxFlat
		sb.content_margin_top = 4
		sb.content_margin_bottom = 4
		t.set_stylebox(style, "Button", sb)
	return t


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


static func heading(text_key: String, size: int = TITLE_SIZE) -> Label:
	var l := Label.new()
	l.text = text_key
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", ACCENT)
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


## The gold coin and a number after it (the row's child "Value"), centred.
static func gold_row(node_name: String) -> HBoxContainer:
	var row := HBoxContainer.new()
	row.name = node_name
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	var coin := TextureRect.new()
	coin.texture = load("res://assets/original/ui/gold.png")
	coin.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	coin.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	coin.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	coin.custom_minimum_size = Vector2(56, 40)
	row.add_child(coin)
	var value := Label.new()
	value.name = "Value"
	value.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	value.custom_minimum_size = Vector2(160, 0)
	value.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	row.add_child(value)
	return row
