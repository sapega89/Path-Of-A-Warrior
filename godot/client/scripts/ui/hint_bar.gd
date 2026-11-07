extends PanelContainer
## The line of control hints at the bottom of every screen: which keys choose, confirm and go
## back, named for the device just used (InputSetup.hint: the keyboard's, the pad's or touch).
## A screen says its own line with `controls_hint() -> String` (already translated; "" hides the
## bar, e.g. on the map, where the HUD shows the keys); without it the menus' line is shown.
## The bar takes HEIGHT px off the bottom of the screen area while it shows.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const HEIGHT := 40
const FONT_SIZE := 20
const MENU_HINT := "hint.menu"

var label: Label
var host: Control  # the screen area, made shorter while the bar shows


func _init() -> void:
	name = "HintBar"
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	offset_top = -HEIGHT
	var sb := UiTheme.box(UiTheme.PANEL)
	sb.content_margin_top = 4
	sb.content_margin_bottom = 4
	add_theme_stylebox_override("panel", sb)
	label = Label.new()
	label.name = "Text"
	label.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	label.add_theme_font_size_override("font_size", FONT_SIZE)
	label.add_theme_color_override("font_color", UiTheme.TEXT_DIM)
	add_child(label)


func _ready() -> void:
	Router.screen_changed.connect(func(_s): refresh())
	InputSetup.device_changed.connect(func(_d): refresh())
	refresh()


## Read again every frame: a screen may change its line (the next step, the device).
func _process(_delta: float) -> void:
	refresh()


## The line for the screen shown now.
static func text_for(screen: Node) -> String:
	if screen == null:
		return ""
	if screen.has_method("controls_hint"):
		return str(screen.controls_hint())
	return InputSetup.hint(MENU_HINT)


func refresh() -> void:
	var t := text_for(Router.current)
	if label.text != t:
		label.text = t
	var on := not t.is_empty()
	if visible != on:
		visible = on
	if host != null:
		var bottom := -HEIGHT if on else 0
		if host.offset_bottom != bottom:
			host.offset_bottom = bottom
