class_name WorldMapView
extends Control
## The world map of the campaign (scripts/core/world_map.gd): a button for each place, the
## ways between them, the hero's place lit and the places he can go to now marked. A place
## the hero can go to and fight for opens its missions (`place_chosen`); the line under the
## map names the place in focus, how it is for the hero and the missions won there.

signal place_chosen(id: int)

const NODE := 38.0  # a place's button, px
const WON := Color("7fb069")
const WAY := Color(0.6, 0.57, 0.65, 0.35)

var world: WorldMap
var profile: Profile
var here := 0
var buttons := {}  # place id -> Button
var info: Label
var _area := Rect2()


func _init(w: WorldMap, p: Profile, place: int) -> void:
	world = w
	profile = p
	here = place
	name = "WorldMap"
	info = UiTheme.note("Info", 40)
	info.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	info.offset_top = -48
	add_child(info)
	for id in range(1, world.place_count() + 1):
		var b := Button.new()
		b.name = "Place%d" % id
		b.text = str(id)
		b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		b.custom_minimum_size = Vector2(NODE, NODE)
		b.size = Vector2(NODE, NODE)
		b.add_theme_font_size_override("font_size", 16)
		b.add_theme_constant_override("h_separation", 0)
		for style in ["normal", "hover", "pressed", "disabled", "focus"]:
			var sb := UiTheme.box(UiTheme.BUTTON)
			sb.set_content_margin_all(0)
			sb.set_corner_radius_all(int(NODE / 2))
			b.add_theme_stylebox_override(style, sb)
		_style(b, id)
		b.pressed.connect(_on_press.bind(id))
		b.focus_entered.connect(_show_info.bind(id))
		b.mouse_entered.connect(_show_info.bind(id))
		add_child(b)
		buttons[id] = b
	resized.connect(_place_buttons)


func _ready() -> void:
	_place_buttons()
	_show_info(here if buttons.has(here) else first_focus())


## The button to start on: the first place the hero can go to now, else his own.
func first_focus() -> int:
	for id in world.next_places(here):
		if world.state(id, here, profile) == WorldMap.State.NEXT:
			return id
	return here if buttons.has(here) else 1


func focus_first() -> void:
	if is_inside_tree():
		(buttons[first_focus()] as Button).grab_focus()


func can_choose(id: int) -> bool:
	return world.state(id, here, profile) == WorldMap.State.NEXT


func _on_press(id: int) -> void:
	if can_choose(id):
		place_chosen.emit(id)


func _style(b: Button, id: int) -> void:
	var st: int = world.state(id, here, profile)
	var w: Vector2i = world.won(id, profile)
	var fill: Color = UiTheme.PANEL
	var border := Color.TRANSPARENT
	var font: Color = UiTheme.TEXT_DIM
	match st:
		WorldMap.State.HERE:
			fill = UiTheme.ACCENT
			font = UiTheme.BG
		WorldMap.State.NEXT:
			fill = UiTheme.BUTTON
			border = UiTheme.ACCENT
			font = UiTheme.TEXT
		WorldMap.State.CLOSED:
			fill = UiTheme.BG
			border = UiTheme.TEXT_DIM
	if st != WorldMap.State.HERE and w.y > 0 and w.x == w.y:
		border = WON
	for style in ["normal", "hover", "pressed", "disabled"]:
		var sb := b.get_theme_stylebox(style) as StyleBoxFlat
		sb.bg_color = fill.lightened(0.15) if style == "hover" else fill
		sb.border_color = border
		sb.set_border_width_all(2 if border.a > 0 else 0)
	var focus := b.get_theme_stylebox("focus") as StyleBoxFlat
	focus.bg_color = Color.TRANSPARENT
	focus.border_color = UiTheme.TEXT
	focus.set_border_width_all(3)
	for c in ["font_color", "font_hover_color", "font_focus_color", "font_pressed_color"]:
		b.add_theme_color_override(c, font)


## Where the places go: the columns across, the rows down, inside the space above the line.
func _place_buttons() -> void:
	_area = Rect2(Vector2(NODE / 2, NODE / 2), size - Vector2(NODE, NODE + 56))
	var cols := maxi(world.columns - 1, 1)
	var half := maxf((world.rows - 1) / 2.0, 1.0)
	for id in buttons:
		var c: Vector2 = world.cells.get(id, Vector2.ZERO)
		var p := Vector2(
			_area.position.x + _area.size.x * c.x / cols,
			_area.position.y + _area.size.y * (0.5 + c.y / (2.0 * half))
		)
		(buttons[id] as Button).position = p - Vector2(NODE, NODE) / 2
	queue_redraw()


func center_of(id: int) -> Vector2:
	var b: Button = buttons[id]
	return b.position + b.size / 2


func _draw() -> void:
	for w in world.ways():
		var lit: bool = w[0] == here
		var a := center_of(w[0])
		var b := center_of(w[1])
		var col: Color = UiTheme.ACCENT if lit else WAY
		draw_line(a, b, col, 3.0 if lit else 2.0, true)
		if lit:  # an arrow head where the way arrives
			var d := (b - a).normalized()
			var tip := b - d * (NODE / 2 + 2)
			var side := d.orthogonal() * 7
			draw_colored_polygon(
				PackedVector2Array([tip, tip - d * 12 + side, tip - d * 12 - side]), col
			)
	if here == 0 and buttons.has(1):  # before the first mission: a way in from the left
		var b1 := center_of(1)
		draw_line(
			b1 - Vector2(NODE * 1.2, 0), b1 - Vector2(NODE / 2 + 2, 0), UiTheme.ACCENT, 3.0, true
		)


func _show_info(id: int) -> void:
	if not buttons.has(id):
		info.text = ""
		return
	var key: String = ["world.here", "world.next", "world.closed", "world.away"][world.state(
		id, here, profile
	)]
	var w: Vector2i = world.won(id, profile)
	info.text = (
		"%d. %s — %s · %s"
		% [id, world.campaign.lord_name(id), tr(key), tr("world.won") % [w.x, w.y]]
	)
