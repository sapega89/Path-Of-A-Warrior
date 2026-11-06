extends Control
## A mission of the original campaign on its map. The game itself runs in MapSim
## (original pixels and ticks); this screen reads the input, ticks the simulation every
## 120 ms and draws its state in 3D: the hero sprite, the camera on the current room,
## the exit arrows and the "Stage" banners, the soldiers and their arrows, the effects of
## skills, potions and scrolls, and the HUD.
## Params: {lord, mission, seed (optional: the same enemies every run)}.
## The mouse, as pyport's: the left button beside the hero walks that way while it is held
## (dragging turns him, two quick clicks run), a click on the hero or the right button attacks,
## a click on the skill bar uses the slot, on AUTO toggles the auto-hunt, on PAUSE pauses.

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
const Autopilot := preload("res://scripts/sim/autopilot.gd")
const Effects := preload("res://scripts/world/effects.gd")
const Profile := preload("res://scripts/core/profile.gd")
const MissionPause := preload("res://scripts/ui/mission_pause.gd")

## One tick of the game, by the game speed of the settings (MapSim.TICK_MS at Med).
var tick := MapSim.TICK_MS / 1000.0
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
var profile: Profile
var effects: Effects
var banner: PanelContainer
var banner_text: Label
var arrows: Array[TextureRect] = []
var soldiers := {}  # sim actor -> Soldier node
var shots: Array[MeshInstance3D] = []  # the archers' arrows
var tint := 0
var loot := {}  # sim drop -> Sprite3D
var trails: Array = []  # the weapon trails of this tick
var _trail_pick := RandomNumberGenerator.new()
var _tool_tex: Texture2D = preload("res://assets/original/ui/tool.png")
var _gold_tex: Texture2D = preload("res://assets/original/ui/gold.png")
var _acc := 0.0
var _pressed := -1
var _fire := false
var _hotkey := -1  # a skill key pressed since the last tick
var _potion := -1  # a potion key pressed since the last tick
var _belt := -1  # a belt slot used by its key or a click on the skill bar since the last tick
var autopilot := Autopilot.new()
var _keys_down := {}  # attack, skill and potion keys held at the last frame
var _last_held := -1
var _mouse_dir := -1  # the direction the left mouse button holds, -1: none
var _blink := 0
var pause_menu: MissionPause  # shown while the game is paused


func _ready() -> void:
	var p: Dictionary = Router.params
	tick = Settings.tick_seconds()
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
	profile = Profile.load_or_new()
	var s: Array = mission_info.get("start", [4, 4])
	var resume := bool(p.get("resume", false)) and not profile.on_map.is_empty()
	if resume:
		s = [int(profile.on_map.get("x", s[0])), int(profile.on_map.get("y", s[1]))]
	sim = MapSim.new(map, mission, Vector2i(int(s[0]), int(s[1])))
	if p.has("seed"):
		sim.rng = JavaRandom.new(int(p.seed))
	tint = int(mission_info.get("tint", 0))
	sim.boss_type = int(mission_info.get("boss_type", 0))
	sim.mission_gold = int(mission_info.get("gold", 0))
	sim.mission_general = int(mission_info.get("general", 0))
	sim.time_limit = int(mission_info.get("time_limit", 0))
	profile.apply_to(sim)
	if resume:
		profile.resume_on_map(sim)

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
	hero.set_look(profile.head, sim.hero.weapon_kind)
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
	if held == -1:
		held = _mouse_dir
	if held != -1 and held != _last_held:
		_pressed = held  # a new direction this tick: the original's key press
	_last_held = held
	if _pressed_now("auto"):
		toggle_auto()
	if _pressed_now("attack"):
		_fire = true
	for i in 5:
		if _pressed_now("skill_%d" % (i + 1)):
			_hotkey = i
	for i in 2:
		if _pressed_now("potion_%d" % (i + 1)):
			_potion = i
	for i in 5:
		if _pressed_now("belt_%d" % (i + 1)):
			_belt = i
	if held != -1 or _fire or _hotkey != -1 or _potion != -1 or _belt != -1:
		autopilot.player_key()
	_acc += delta
	while _acc >= tick:
		_acc -= tick
		var auto: Dictionary = autopilot.decide(sim)
		if int(auto.held) != -1 and held == -1:
			held = int(auto.held)
		if bool(auto.fire):
			_fire = true
		if int(auto.hotkey) != -1 and _hotkey == -1:
			_hotkey = int(auto.hotkey)
		if int(auto.belt) != -1 and _belt == -1:
			_belt = int(auto.belt)
		sim.tick(held, _pressed, _fire, _hotkey, _potion, _belt)
		for n in sim.sounds:
			Audio.play_sound(n)
		_pressed = -1
		_fire = false
		_hotkey = -1
		_potion = -1
		_belt = -1
		hud.tick()
		_blink += 1
		trails = sim.trails(_trail_pick)
	if sim.finished:
		set_process(false)
		profile.take_from(sim, lord_id, mission, int(mission_info.get("id", 0)))
		var ending: int = profile.advance(sim, lord_id, mission_info)
		profile.save()
		Router.back()
		if ending >= 0:
			Router.push("story", {"story": ending, "reward_item": profile.reward_item,
				"opened_lord": profile.opened_lord})
		return
	_update_view(_acc / tick)


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
	var shown: Array = sim.effects()
	for sp in sim.sparks():
		shown.append(["spark", sp[0], sp[1]])
	shown.append_array(trails)
	effects.show_effects(shown)
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
	elif sim.banner == MapSim.BANNER_TOTAL_EXP or sim.banner == MapSim.BANNER_TIME_EXP:
		if sim.banner == MapSim.BANNER_TOTAL_EXP:
			stage = "%s\n%d" % [tr("mission.total_exp"), sim.exp_reward()]
		else:
			stage = "%s\n%s %s\n%s %s" % [tr("mission.time_exp"), tr("mission.time_limit"),
				clock(sim.time_limit), tr("mission.time_taken"), clock(sim.play_seconds())]
		var lv := profile.level_with(sim.exp_reward())
		if lv > profile.level:
			stage += "\n" + tr("mission.level_up") % lv
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


## Stops the mission and shows the pause menu (Resume, Options, Exit to Menu, Exit Game).
func pause() -> void:
	if pause_menu != null:
		return
	set_process(false)
	_release_keys()
	pause_menu = MissionPause.new()
	pause_menu.name = "Pause"
	pause_menu.sim = sim
	pause_menu.save_game = save_on_map
	pause_menu.resumed.connect(resume)
	add_child(pause_menu)


func resume() -> void:
	if pause_menu == null:
		return
	pause_menu.queue_free()
	pause_menu = null
	_acc = 0.0
	_last_held = -1
	set_process(not sim.finished)


## Pause menu Save: the mission is saved on its map, once the room is cleared; Continue comes
## back to this room. False (nothing saved) while an enemy is alive or still to come.
func save_on_map() -> bool:
	if not sim.can_save():
		return false
	profile = Profile.load_or_new()
	return profile.save_on_map(sim, lord_id, mission, int(mission_info.get("id", 0)))


## Forgets the keys held when the game stopped, so the hero does not walk on by himself.
func _release_keys() -> void:
	_pressed = -1
	_fire = false
	_hotkey = -1
	_potion = -1
	_belt = -1
	_mouse_dir = -1
	_keys_down.clear()


func _unhandled_input(event: InputEvent) -> void:
	if pause_menu != null:
		return
	if event.is_action_pressed("pause") or event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		pause()


## The mouse (and a touch, which comes as a click too) over the map: the screen itself takes
## it, as the controls over the map let it through.
func _gui_input(event: InputEvent) -> void:
	if pause_menu != null:
		return
	if event is InputEventMouseButton:
		_mouse_button(event)
	elif event is InputEventMouseMotion and _mouse_dir != -1:
		var d := pointer_dir(event.position)
		if d != -1 and not hud.panel_at(event.position) and hud.slot_at(event.position).is_empty():
			_mouse_dir = d  # dragging turns the hero


func _mouse_button(event: InputEventMouseButton) -> void:
	if event.button_index == MOUSE_BUTTON_LEFT and not event.pressed:
		_mouse_dir = -1
		return
	if not event.pressed:
		return
	if event.button_index == MOUSE_BUTTON_LEFT:
		if click_bar(event.position):
			return
		if hud.pause_at(event.position):
			get_viewport().set_input_as_handled()
			pause()
			return
	# a touch comes as a click too: on a phone the touch controls walk and attack
	if event.device == InputEvent.DEVICE_ID_EMULATION or not is_processing():
		return
	if event.button_index == MOUSE_BUTTON_RIGHT:
		get_viewport().set_input_as_handled()
		_fire = true  # attack where the hero faces
	elif event.button_index == MOUSE_BUTTON_LEFT:
		get_viewport().set_input_as_handled()
		var d := pointer_dir(event.position)
		if d == -1:
			_fire = true  # a click on the hero
		else:
			_pressed = d  # a press of that direction, held while the button is
			_mouse_dir = d


## The direction from the hero to a point of the screen (6 right, 2 left, 4 up, 0 down), or -1
## on the hero himself: within 14 x 20 original pixels of the middle of his body, 20 px above
## his position, as pyport's pointer.
func pointer_dir(at: Vector2) -> int:
	var middle := hero.global_position + Vector3(0, (20 + Hero.FOOT_PX) * Hero.PIXEL_SIZE, 0)
	var c := camera.unproject_position(middle)
	var box := Vector2(
		absf(camera.unproject_position(middle + Vector3(14 * Hero.PIXEL_SIZE, 0, 0)).x - c.x),
		absf(camera.unproject_position(middle + Vector3(0, 20 * Hero.PIXEL_SIZE, 0)).y - c.y))
	var d := at - c
	if absf(d.x) < box.x and absf(d.y) < box.y:
		return -1
	if absf(d.x) >= absf(d.y):
		return 6 if d.x > 0.0 else 2
	return 0 if d.y > 0.0 else 4


## Auto-hunt on / off (Tab, F, R3 or a click on AUTO).
func toggle_auto() -> void:
	autopilot.toggle()
	hud.auto_on = autopilot.on
	hud.queue_redraw()


## A click on the skill bar: a belt slot is used, a skill cast. False when it missed the bar.
func click_bar(at: Vector2) -> bool:
	if hud.auto_at(at):
		get_viewport().set_input_as_handled()
		toggle_auto()
		return true
	var hit: Array = hud.slot_at(at)
	if hit.is_empty():
		return false
	get_viewport().set_input_as_handled()
	if hit[0] == "belt":
		_belt = hit[1]
	elif hit[0] == "skill":
		_hotkey = hit[1]
	return true
