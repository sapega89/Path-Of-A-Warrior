class_name GearScreen
extends BaseScreen
## Gear: the hero as a 3D figure of the new art (his class, his blade) standing on a round
## stage in the middle of a panel, and the nine places around him (weapon, head, body, ...),
## each with what is worn there; an empty place shows a faint picture of what goes there.
## Picking a place takes off what is worn there into the backpack and opens the Inventory to
## choose what to wear instead. The line at the bottom says what the thing under the cursor is.

const SCALE := 2
const BOARD := Vector2(158, 162)  # the panel, in grid pixels
const FIGURE := Vector2i(200, 220)  # the picture of the hero, in screen pixels
## The places around the middle of the panel, in grid pixels (top-left of the 28 px icon).
const PLACE_DX := [-77, -77, -77, -33, 3, 47, 47, 47, -15]
const PLACE_DY := [21, -15, -51, -79, -79, -51, -15, 21, 49]

var profile: RefCounted
var path: String = Profile.PATH
var places: Array[Button] = []
var ghosts: Array[TextureRect] = []  # the faint pictures of the empty places
var figure: Node3D  # the hero (an ArtFigure)
var info: Label


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	var col := UiTheme.menu_column(self, 640)
	col.add_child(UiTheme.heading("gear.title", 44))

	var board := Control.new()
	board.name = "Board"
	var size_px := BOARD * SCALE
	board.custom_minimum_size = size_px + Vector2(0, 8)
	var center := CenterContainer.new()
	center.add_child(board)
	col.add_child(center)
	var mid := Vector2(size_px.x / 2.0, size_px.y / 2.0)
	var panel := Panel.new()
	panel.name = "Frame"
	panel.size = size_px
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	board.add_child(panel)
	var stage := Stage.new()
	stage.position = mid + Vector2(-80, 30)
	stage.size = Vector2(160, 70)
	board.add_child(stage)
	board.add_child(_hero_view(mid))
	for i in Items.EQUIPPED:
		var b := ItemSlot.button("Place%d" % i)
		b.position = mid + Vector2(PLACE_DX[i] - 1, PLACE_DY[i] - 1) * SCALE - Vector2(3, 3)
		b.size = b.custom_minimum_size
		var ghost := TextureRect.new()
		ghost.name = "Ghost"
		ghost.texture = ItemSlot.item_icon(_sample(i))
		ghost.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		ghost.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		ghost.modulate = Color(0.55, 0.6, 0.72, 0.28)
		ghost.mouse_filter = Control.MOUSE_FILTER_IGNORE
		ghost.set_anchors_preset(Control.PRESET_FULL_RECT)
		ghost.set_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 8)
		b.add_child(ghost)
		ghosts.append(ghost)
		var at := i
		b.pressed.connect(func(): press_place(at))
		b.focus_entered.connect(func(): _show_info(at))
		b.mouse_entered.connect(func(): _show_info(at))
		board.add_child(b)
		places.append(b)

	info = Label.new()
	info.name = "Info"
	info.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	info.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	info.custom_minimum_size = Vector2(0, 72)
	col.add_child(info)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	refresh()
	_show_info(0)
	places[0].grab_focus.call_deferred()


## Takes off what is worn in the place and opens the Inventory.
func press_place(i: int) -> void:
	if profile.unequip(i):
		profile.save(path)
	refresh()
	Router.push("inventory", Router.params)


func refresh() -> void:
	for i in places.size():
		places[i].icon = ItemSlot.item_icon(int(profile.equipped[i].id))
		ghosts[i].visible = places[i].icon == null


func describe(i: int) -> String:
	return Items.describe(profile.equipped[i])


func _show_info(i: int) -> void:
	info.text = describe(i)


## A thing worn in place i (the first gear that goes there), for the picture of an empty place.
static func _sample(i: int) -> int:
	for id in range(101, 601):
		if not Items.info(id).is_empty() and Items.place(id) == i:
			return id
	return 0


## The hero standing in his own small world (a light, the air), turned a little to the side,
## breathing in his idle clip; his picture fills the middle of the panel.
func _hero_view(mid: Vector2) -> TextureRect:
	var view := SubViewport.new()
	view.name = "HeroView"
	view.size = FIGURE
	view.own_world_3d = true
	view.transparent_bg = true
	view.msaa_3d = Viewport.MSAA_4X
	add_child(view)
	var sun := DirectionalLight3D.new()
	sun.transform = Transform3D(
		Basis.looking_at(Vector3(-0.4, -0.6, -0.7).normalized(), Vector3.UP), Vector3.ZERO
	)
	view.add_child(sun)
	var env := Environment.new()
	ArtKit.light(sun, env)
	sun.light_energy = 1.0  # a figure on a stand, not a field: more light on it
	env.ambient_light_energy = 0.45
	env.background_mode = Environment.BG_CLEAR_COLOR
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	var we := WorldEnvironment.new()
	we.environment = env
	view.add_child(we)
	figure = ArtFigure.new()
	figure.name = "Hero"
	view.add_child(figure)
	figure.setup(MapPeople.HEROES[clampi(int(profile.head), 0, 3)])
	figure.unequip_all()
	figure.equip(MapPeople.BLADES[clampi(profile.weapon_kind(), 0, 1)])
	figure.rotation.y = 0.45
	figure.play("idle", 0.0)
	var camera := Camera3D.new()
	camera.fov = 20.0
	camera.position = Vector3(0, 1.15, 6.4)
	camera.rotation.x = -0.035
	view.add_child(camera)
	var r := TextureRect.new()
	r.name = "Hero"
	r.texture = view.get_texture()
	r.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	r.size = Vector2(FIGURE)
	r.position = mid - Vector2(FIGURE) / 2.0 + Vector2(0, -4)
	r.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return r


## The round stage under the hero: a dark ellipse with an iron rim and rivets around it.
class Stage:
	extends Control

	func _ready() -> void:
		mouse_filter = Control.MOUSE_FILTER_IGNORE

	func _draw() -> void:
		var c := size / 2.0
		var rx := size.x / 2.0
		var ry := size.y / 2.0
		var rim := PackedVector2Array()
		for i in 49:
			var t := TAU * i / 48.0
			rim.append(c + Vector2(cos(t) * rx, sin(t) * ry))
		draw_colored_polygon(rim, Color(UiTheme.SLOT, 0.85))
		draw_polyline(rim, UiTheme.IRON, 2.0, true)
		var inner := PackedVector2Array()
		for p in rim:
			inner.append(c + (p - c) * 0.8)
		draw_polyline(inner, Color(UiTheme.IRON_LIGHT, 0.25), 1.0, true)
		for i in 8:
			var t := TAU * (i + 0.5) / 8.0
			UiTheme.rivet(get_canvas_item(), c + Vector2(cos(t) * rx * 0.9, sin(t) * ry * 0.9), 2.8)


## The line of control hints under the screen (scripts/ui/hint_bar.gd): what picking a thing does.
func controls_hint() -> String:
	return InputSetup.hint("hint.grid_gear")
