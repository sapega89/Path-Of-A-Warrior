extends Control
## A mission of the original campaign on its map: the hero starts where the mission says,
## the camera shows the current room, and the rooms open and lead to each other as in the
## original. Params: {lord, mission}.
##
## Enemies and combat are not ported yet, so every room is cleared as soon as it is
## entered, like the original's "map without enemies" mode; a room with a general stays
## closed (the mission is won only by defeating him).

const MapBuilder := preload("res://scripts/world/map_builder.gd")
const Rooms := preload("res://scripts/world/rooms.gd")
const Campaign := preload("res://scripts/core/campaign.gd")
const Hero := preload("res://scripts/world/hero.gd")
const FollowCamera := preload("res://scripts/world/follow_camera.gd")
const TouchControls := preload("res://scripts/ui/touch_controls.gd")

const TICK := 0.1  # one original map tick
const CLEAR_DELAY := 5  # ticks from "cleared" to the exits opening (popup time in the original)
const SCROLL_TIME := 0.6  # 6 ticks
const ARROW_SCALE := 3.0
const ARROW_PATH := "res://assets/original/ui/arrow%d.png"

enum Phase { CLOSED, CLEARING, OPEN, SCROLLING }

var lord_id := 1
var mission := 0
var mission_info := {}
var viewport: SubViewport
var world: Node3D
var builder: Node3D
var hero: CharacterBody3D
var camera: Camera3D
var rooms: RefCounted
var room := 0
var phase := Phase.CLOSED
var rooms_visited := 1
var info: Label
var arrows: Array[TextureRect] = []
var _timer := 0.0
var _blink := 0


func _ready() -> void:
	var p: Dictionary = Router.params
	lord_id = int(p.get("lord", 1))
	mission = int(p.get("mission", 0))
	var campaign := Campaign.new()
	var ms := campaign.lord_missions(lord_id)
	mission_info = ms[mission] if mission < ms.size() else {}

	var container := SubViewportContainer.new()
	container.name = "World"
	container.stretch = true
	container.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(container)
	viewport = SubViewport.new()
	viewport.own_world_3d = true
	viewport.msaa_3d = Viewport.MSAA_2X
	container.add_child(viewport)
	world = Node3D.new()
	world.name = "WorldRoot"
	viewport.add_child(world)
	MapBuilder.add_environment(world)

	var map := MapBuilder.load_map(Campaign.lord_map(lord_id))
	builder = MapBuilder.new()
	builder.name = "Map"
	world.add_child(builder)
	builder.build(map)
	rooms = Rooms.new(map, mission)

	hero = Hero.new()
	hero.name = "Hero"
	world.add_child(hero)
	hero.global_position = start_position(mission_info)
	room = rooms.room_at(hero.global_position)

	camera = FollowCamera.new()
	camera.name = "Camera"
	world.add_child(camera)
	camera.focus = rooms.center(room)
	camera.make_current()
	camera.snap()

	for i in 4:
		var a := TextureRect.new()
		a.name = "Arrow%d" % i
		a.texture = load(ARROW_PATH % i)
		a.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		a.stretch_mode = TextureRect.STRETCH_SCALE
		a.mouse_filter = Control.MOUSE_FILTER_IGNORE
		a.visible = false
		add_child(a)
		arrows.append(a)

	info = Label.new()
	info.name = "Info"
	info.position = Vector2(24, 16)
	info.add_theme_font_size_override("font_size", 20)
	info.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	add_child(info)

	var touch := TouchControls.new()
	touch.name = "Touch"
	add_child(touch)
	enter_room(room)


## The mission's start tile to a world position (the original puts the hero at
## tile * 27 + (12, 20) px).
static func start_position(m: Dictionary) -> Vector3:
	var s: Array = m.get("start", [4, 4])
	return Vector3((float(s[0]) * 27.0 + 12.0) / 27.0, 0.05, (float(s[1]) * 27.0 + 20.0) / 27.0)


func enter_room(r: int) -> void:
	room = r
	phase = Phase.CLOSED
	_timer = 0.0
	if not rooms.has_general(room):
		phase = Phase.CLEARING  # no enemies yet: the room is cleared at once
	_update_info()


func _physics_process(_delta: float) -> void:
	if phase == Phase.SCROLLING:
		return
	var kept: Dictionary = rooms.keep_inside(room, hero.global_position)
	var pos: Vector3 = kept.pos
	pos.y = hero.global_position.y
	hero.global_position = pos
	var edge: int = kept.edge
	if phase == Phase.OPEN and edge != 0 and rooms.has_exit(room, edge) and hero.walking:
		leave_room(edge)


func _process(delta: float) -> void:
	_timer += delta
	if phase == Phase.CLEARING and _timer >= CLEAR_DELAY * TICK:
		phase = Phase.OPEN
		_timer = 0.0
	_blink = int(_timer / TICK)
	_place_arrows()


func leave_room(exit_no: int) -> void:
	var next: int = rooms.neighbour(room, exit_no)
	if next < 0 or next >= rooms.count():
		return
	phase = Phase.SCROLLING
	hero.set_physics_process(false)
	var tw := create_tween()
	tw.tween_property(camera, "focus", rooms.center(next), SCROLL_TIME).set_trans(Tween.TRANS_SINE)
	# The hero steps over the edge into the new room.
	var kept: Dictionary = rooms.keep_inside(next, hero.global_position)
	tw.parallel().tween_property(hero, "global_position", kept.pos, SCROLL_TIME)
	tw.tween_callback(func():
		hero.set_physics_process(true)
		rooms_visited += 1
		enter_room(next))


func _place_arrows() -> void:
	var view := get_viewport_rect().size
	var lit := phase == Phase.OPEN and (_blink & 2) != 0
	for i in 4:
		var a := arrows[i]
		a.visible = lit and rooms.has_exit(room, i + 1)
		var s := a.texture.get_size() * ARROW_SCALE
		a.size = s
		match i:
			0: a.position = Vector2((view.x - s.x) / 2.0, view.y - s.y - 16)
			1: a.position = Vector2(16, (view.y - s.y) / 2.0)
			2: a.position = Vector2((view.x - s.x) / 2.0, 16)
			3: a.position = Vector2(view.x - s.x - 16, (view.y - s.y) / 2.0)


func _update_info() -> void:
	var p: Vector2i = rooms.room_xy(room)
	info.text = "%s: %s   %s %d,%d" % [Campaign.new().lord_name(lord_id), mission_info.get("name", ""),
		tr("mission.room"), p.x + 1, p.y + 1]


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause") or event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
