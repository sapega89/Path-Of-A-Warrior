extends Control
## A mission of the original campaign on its map. The game itself runs in MapSim
## (original pixels and ticks); this screen reads the input, ticks the simulation every
## 120 ms and draws its state in 3D: the hero sprite, the camera on the current room,
## the exit arrows and the "Stage" banners. Params: {lord, mission}.

const MapBuilder := preload("res://scripts/world/map_builder.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")
const Campaign := preload("res://scripts/core/campaign.gd")
const Hero := preload("res://scripts/world/hero.gd")
const FollowCamera := preload("res://scripts/world/follow_camera.gd")
const TouchControls := preload("res://scripts/ui/touch_controls.gd")
const UiTheme := preload("res://scripts/ui/ui_theme.gd")

const TICK := MapSim.TICK_MS / 1000.0
const ARROW_SCALE := 3.0
const ARROW_PATH := "res://assets/original/ui/arrow%d.png"

var lord_id := 1
var mission := 0
var mission_info := {}
var lord_name := ""
var sim: RefCounted
var viewport: SubViewport
var world: Node3D
var builder: Node3D
var hero: CharacterBody3D
var camera: Camera3D
var info: Label
var banner: PanelContainer
var banner_text: Label
var arrows: Array[TextureRect] = []
var _acc := 0.0
var _prev_pos := Vector2i.ZERO
var _pressed := -1
var _fire := false
var _last_held := -1
var _blink := 0


func _ready() -> void:
	var p: Dictionary = Router.params
	lord_id = int(p.get("lord", 1))
	mission = int(p.get("mission", 0))
	var campaign := Campaign.new()
	var ms := campaign.lord_missions(lord_id)
	mission_info = ms[mission] if mission < ms.size() else {}
	lord_name = campaign.lord_name(lord_id)

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
	var s: Array = mission_info.get("start", [4, 4])
	sim = MapSim.new(map, mission, Vector2i(int(s[0]), int(s[1])))
	_prev_pos = sim.hero.pos

	hero = Hero.new()
	hero.name = "Hero"
	hero.external = true
	world.add_child(hero)
	hero.global_position = Hero.px_to_world(Vector2(sim.hero.pos))

	camera = FollowCamera.new()
	camera.name = "Camera"
	world.add_child(camera)
	camera.focus = sim.rooms.center(sim.cell)
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

	banner = PanelContainer.new()
	banner.name = "Banner"
	banner.visible = false
	banner.mouse_filter = Control.MOUSE_FILTER_IGNORE
	banner_text = Label.new()
	banner_text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	banner_text.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	banner.add_child(banner_text)
	add_child(banner)

	var touch := TouchControls.new()
	touch.name = "Touch"
	add_child(touch)
	_update_view(0.0)


## The 4-direction of a stick or keys (the original hero walks in 4 directions), or -1.
static func dir4_of(v: Vector2) -> int:
	if v.length() < 0.3:
		return -1
	if absf(v.x) > absf(v.y):
		return 6 if v.x > 0.0 else 2
	return 0 if v.y > 0.0 else 4


func _process(delta: float) -> void:
	var held := dir4_of(Input.get_vector("move_left", "move_right", "move_up", "move_down"))
	if held != -1 and held != _last_held:
		_pressed = held  # a new direction this tick: the original's key press
	_last_held = held
	if Input.is_action_just_pressed("attack"):
		_fire = true
	_acc += delta
	while _acc >= TICK:
		_acc -= TICK
		_prev_pos = sim.hero.pos
		sim.tick(held, _pressed, _fire)
		_pressed = -1
		_fire = false
		_blink += 1
	_update_view(_acc / TICK)


func _update_view(t: float) -> void:
	var p := Vector2(_prev_pos).lerp(Vector2(sim.hero.pos), clampf(t, 0.0, 1.0))
	if (sim.hero.pos - _prev_pos).length() > 40:
		p = Vector2(sim.hero.pos)
	hero.global_position = Hero.px_to_world(p)
	hero.set_frame(sim.hero_sprite_frame())
	camera.focus = sim.rooms.center(sim.cell)
	info.text = "%s: %s   %s %d" % [lord_name, mission_info.get("name", ""), tr("mission.stage"), sim.rooms_visited]
	_place_arrows()
	_show_banner()


func _show_banner() -> void:
	banner.visible = sim.banner != 0
	if not banner.visible:
		return
	var stage := tr("mission.stage") + " " + str(sim.rooms_visited)
	if sim.banner == MapSim.BANNER_STAGE_CLEAR:
		stage += " " + tr("mission.complete")
	banner_text.text = "%s\n%s\n%s" % [lord_name, mission_info.get("name", ""), stage]
	var view := get_viewport_rect().size
	banner.size = Vector2(520, 0)
	banner.reset_size()
	banner.position = Vector2((view.x - banner.size.x) / 2.0, view.y * 0.3)


func _place_arrows() -> void:
	var view := get_viewport_rect().size
	var lit: bool = sim.exits_open() and (_blink & 2) != 0
	for i in 4:
		var a := arrows[i]
		a.visible = lit and sim.rooms.has_exit(sim.cell, i + 1)
		var s := a.texture.get_size() * ARROW_SCALE
		a.size = s
		match i:
			0: a.position = Vector2((view.x - s.x) / 2.0, view.y - s.y - 16)
			1: a.position = Vector2(16, (view.y - s.y) / 2.0)
			2: a.position = Vector2((view.x - s.x) / 2.0, 16)
			3: a.position = Vector2(view.x - s.x - 16, (view.y - s.y) / 2.0)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause") or event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
