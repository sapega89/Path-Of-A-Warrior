extends Control
## A mission of the original campaign on its map. The game itself runs in MapSim
## (original pixels and ticks); this screen reads the input, ticks the simulation every
## 120 ms and draws its state in 3D: the hero sprite, the camera on the current room,
## the exit arrows and the "Stage" banners, the soldiers and their arrows, the effects of
## skills, potions and scrolls, and the HUD.
## Params: {lord, mission, seed (optional: the same enemies every run)}.

const MapBuilder := preload("res://scripts/world/map_builder.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")
const Campaign := preload("res://scripts/core/campaign.gd")
const Hero := preload("res://scripts/world/hero.gd")
const FollowCamera := preload("res://scripts/world/follow_camera.gd")
const Soldier := preload("res://scripts/world/soldier.gd")
const JavaRandom := preload("res://scripts/sim/java_random.gd")
const TouchControls := preload("res://scripts/ui/touch_controls.gd")
const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const MapHud := preload("res://scripts/ui/map_hud.gd")
const Effects := preload("res://scripts/world/effects.gd")

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
var hud: MapHud
var effects: Effects
var banner: PanelContainer
var banner_text: Label
var arrows: Array[TextureRect] = []
var soldiers := {}  # sim actor -> Soldier node
var shots: Array[MeshInstance3D] = []  # the archers' arrows
var tint := 0
var loot := {}  # sim drop -> Sprite3D
var _tool_tex: Texture2D = preload("res://assets/original/ui/tool.png")
var _gold_tex: Texture2D = preload("res://assets/original/ui/gold.png")
var _acc := 0.0
var _pressed := -1
var _fire := false
var _hotkey := -1  # a skill key pressed since the last tick
var _potion := -1  # a potion key pressed since the last tick
var _keys_down := {}  # skill and potion keys held at the last frame
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
	if p.has("seed"):
		sim.rng = JavaRandom.new(int(p.seed))
	tint = int(mission_info.get("tint", 0))
	sim.boss_type = int(mission_info.get("boss_type", 0))
	sim.mission_gold = int(mission_info.get("gold", 0))
	sim.mission_general = int(mission_info.get("general", 0))
	sim.time_limit = int(mission_info.get("time_limit", 0))

	var arrow_mat := StandardMaterial3D.new()
	arrow_mat.albedo_color = Color8(240, 142, 53)
	arrow_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	for i in sim.arrows.size():
		var m := MeshInstance3D.new()
		m.name = "Shot%d" % i
		m.mesh = BoxMesh.new()
		m.material_override = arrow_mat
		m.visible = false
		world.add_child(m)
		shots.append(m)

	hero = Hero.new()
	hero.name = "Hero"
	hero.external = true
	world.add_child(hero)
	effects = Effects.new()
	effects.name = "Effects"
	world.add_child(effects)
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

	hud = MapHud.new()
	hud.name = "Hud"
	hud.sim = sim
	add_child(hud)

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
	for i in 4:
		if _pressed_now("skill_%d" % (i + 1)):
			_hotkey = i
	for i in 2:
		if _pressed_now("potion_%d" % (i + 1)):
			_potion = i
	_acc += delta
	while _acc >= TICK:
		_acc -= TICK
		sim.tick(held, _pressed, _fire, _hotkey, _potion)
		_pressed = -1
		_fire = false
		_hotkey = -1
		_potion = -1
		hud.tick()
		_blink += 1
	if sim.finished:
		set_process(false)
		Router.back()
		return
	_update_view(_acc / TICK)


## The key went down since the last frame (a press seen once, whenever the frame runs).
func _pressed_now(action: String) -> bool:
	var down := Input.is_action_pressed(action)
	var was: bool = _keys_down.get(action, false)
	_keys_down[action] = down
	return down and not was


## The position between the last two ticks (a jump, such as a new room, is not smoothed).
static func smooth(prev: Vector2i, now: Vector2i, t: float) -> Vector2:
	if (now - prev).length() > 40:
		return Vector2(now)
	return Vector2(prev).lerp(Vector2(now), clampf(t, 0.0, 1.0))


func _update_view(t: float) -> void:
	hero.global_position = Hero.px_to_world(smooth(sim.hero.prev_pos, sim.hero.pos, t))
	hero.set_frame(sim.hero_sprite_frame(), sim.hero.action >= 12)
	camera.focus = sim.rooms.center(sim.cell)
	hud.queue_redraw()
	_place_soldiers(t)
	_place_shots()
	effects.show_effects(sim.effects())
	_place_objects()
	_place_loot()
	_place_arrows()
	_show_banner()


func _place_soldiers(t: float) -> void:
	for e in soldiers.keys():
		if not sim.enemies.has(e):
			soldiers[e].queue_free()
			soldiers.erase(e)
	var map4 := MapSim.table("dir8_to_dir4")
	for e in sim.enemies:
		var node = soldiers.get(e)
		if node == null:
			node = Soldier.new()
			node.name = "Soldier"
			world.add_child(node)
			node.setup(e.type, tint, MapSim.table("squad_offsets"), sim.general)
			soldiers[e] = node
		node.global_position = Hero.px_to_world(smooth(e.prev_pos, e.pos, t))
		node.set_frame(sim.enemy_sprite_frame(e), int(map4[e.dir]), e.action >= 6)


## Breakable objects: they blink while breaking and are gone once broken.
func _place_objects() -> void:
	for b in sim.breakables:
		var node := builder.get_node_or_null("Object_%d_%d" % [b.tile.x, b.tile.y]) as Node3D
		if node != null:
			node.visible = sim.breakable_shown(b)


## Gold and items on the floor.
func _place_loot() -> void:
	for d in loot.keys():
		if not sim.drops.has(d):
			loot[d].queue_free()
			loot.erase(d)
	for d in sim.drops:
		if loot.has(d):
			continue
		var s := Sprite3D.new()
		s.name = "Loot"
		s.region_enabled = true
		if d.item > 10000:
			s.texture = _gold_tex
			s.region_rect = Rect2(Vector2.ZERO, _gold_tex.get_size())
		else:
			s.texture = _tool_tex
			var f: int = 11 if d.item > 100 else d.item - 1
			s.region_rect = Rect2(f * 28, 0, 28, 28)
		s.pixel_size = 1.0 / 27.0
		s.billboard = BaseMaterial3D.BILLBOARD_FIXED_Y
		s.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
		s.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
		world.add_child(s)
		s.global_position = Hero.px_to_world(Vector2(d.pos)) + Vector3(0.0, s.region_rect.size.y / 54.0, 0.0)
		loot[d] = s


func _place_shots() -> void:
	for i in shots.size():
		var a = sim.arrows[i]
		shots[i].visible = a.active
		if a.active:
			(shots[i].mesh as BoxMesh).size = Vector3(a.w / 27.0, 0.07, a.h / 27.0)
			shots[i].global_position = Vector3((a.pos.x + a.w / 2.0) / 27.0, 0.6,
				(a.pos.y + 8 + a.h / 2.0 + Hero.FOOT_PX) / 27.0)


func _show_banner() -> void:
	var talk: String = sim.talk_text()
	banner.visible = sim.banner != 0 or not sim.talk.is_empty()
	if not banner.visible:
		return
	if sim.banner == 0:
		banner_text.text = talk
		_place_banner(0.72)  # the talk box sits low, over the map
		return
	var stage := tr("mission.stage") + " " + str(sim.rooms_visited)
	if sim.banner == MapSim.BANNER_STAGE_CLEAR:
		stage += " " + tr("mission.complete")
	elif sim.banner == MapSim.BANNER_FAILED:
		stage = tr("mission.failed")
	elif sim.banner == MapSim.BANNER_SUCCESS:
		stage = "%s\n%s\n%d" % [tr("mission.success"), tr("mission.gold"), sim.gold_reward()]
	elif sim.banner == MapSim.BANNER_TOTAL_EXP:
		stage = "%s\n%d" % [tr("mission.total_exp"), sim.exp_reward()]
	elif sim.banner == MapSim.BANNER_TIME_EXP:
		stage = "%s\n%s %s\n%s %s" % [tr("mission.time_exp"), tr("mission.time_limit"),
			clock(sim.time_limit), tr("mission.time_taken"), clock(sim.play_seconds())]
	banner_text.text = "%s\n%s\n%s" % [lord_name, mission_info.get("name", ""), stage]
	_place_banner(0.3)


## mm:ss
static func clock(secs: int) -> String:
	return "%02d:%02d" % [secs / 60, secs % 60]


func _place_banner(y: float) -> void:
	var view := get_viewport_rect().size
	banner.size = Vector2(520, 0)
	banner.reset_size()
	banner.position = Vector2((view.x - banner.size.x) / 2.0, view.y * y)


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
