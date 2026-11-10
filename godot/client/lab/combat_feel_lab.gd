extends Control
## The combat feel lab: the first room of mission 1 with soldiers coming in wave after wave, to
## try and tune how a hit feels (scripts/world/combat_feel.gd, as the missions use it: hitstop,
## camera shake, flash, recoil, the flight of the one killed, the hit sound, the pad's rumble)
## with every effect and number at hand. The game's own map, people (scripts/world/map_people.gd),
## effects and HUD are used as they are.
## Nothing is saved: the hero is a new one (Profile.new(), never written), he does not die
## (god mode), the room never ends.
##
## Run: godot --path godot/client res://lab/combat_feel_lab.tscn (in the editor: open the scene,
## F6). Keys as in a mission (WASD / arrows, J or Space strikes, 1-5 skills, Tab or F auto-hunt),
## and: H the panel, E all effects off / on (to compare), F2 a wave of swordsmen, F3 archers,
## F4 a general, F6 god mode, Esc quit.

const LORD := 1
const MISSION := 0
const WAVE := 3  # swordsmen in a wave
const GENERAL := 5  # the general who comes on F4 (mission 1's)
const PX := 1.0 / 27.0

var tick := MapSim.TICK_MS / 1000.0
var sim: RefCounted
var feel := CombatFeel.new()
var profile: Profile
var map: Dictionary
var tint := 0
var world: Node3D
var builder: Node3D
var hero: Node3D  # the hero's figure (people.hero)
var people: MapPeople  # the hero and the soldiers as figures
var _anim_dt := 0.0  # seconds the figures' clips move on this frame (0 while a hit holds)
var camera: Camera3D
var effects: MapEffects  # the effects, arrows in flight among them
var hud: MapHud
var panel: FeelPanel
var help: Label
var status: Label  # whether the effects are on, at the top in the middle
var loot := {}
var trails: Array = []
var god := true
## The random numbers of the arena; -1: new ones every start.
var seed := -1
var waves_on := true
var autopilot := Autopilot.new()
## The effects as they were before E switched them all off.
var _saved_on := {}
var _acc := 0.0
var _pressed := -1
var _fire := false
var _hotkey := -1
var _potion := -1
var _belt := -1
var _keys_down := {}
var _last_held := -1
var _trail_pick := RandomNumberGenerator.new()
var _flash_mats := {}  # Sprite3D -> StandardMaterial3D
var _tool_tex: Texture2D = preload("res://assets/original/ui/tool.png")
var _gold_tex: Texture2D = preload("res://assets/original/ui/gold.png")


func _ready() -> void:
	theme = UiTheme.theme(UiTheme.THEME)
	set_anchors_preset(Control.PRESET_FULL_RECT)
	tick = Settings.tick_seconds()
	var bg := ColorRect.new()
	bg.color = UiTheme.BG
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(bg)
	var container := SubViewportContainer.new()
	container.name = "World"
	container.stretch = true
	container.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(container)
	var viewport := SubViewport.new()
	viewport.own_world_3d = true
	viewport.msaa_3d = Viewport.MSAA_2X
	container.add_child(viewport)
	world = Node3D.new()
	world.name = "WorldRoot"
	viewport.add_child(world)
	MapArt.add_environment(world)
	map = MapBuilder.load_map(Campaign.lord_map(LORD))
	builder = MapArt.new()
	builder.name = "Map"
	world.add_child(builder)
	builder.build(map)

	effects = MapEffects.new()
	world.add_child(effects)
	camera = FollowCamera.new()
	world.add_child(camera)
	camera.make_current()

	hud = MapHud.new()
	hud.auto_allowed = true
	add_child(hud)
	panel = FeelPanel.new()
	panel.name = "Panel"
	panel.feel = feel
	panel.lab = self
	add_child(panel)
	help = Label.new()
	# gdlint:ignore = max-line-length
	help.text = "H панель · E эффекты вкл/выкл · F2 мечники · F3 лучники · F4 генерал · F6 бессмертие · Tab автоохота · Esc выход"
	help.add_theme_font_size_override("font_size", 13)
	help.position = Vector2(12, 78)
	help.modulate = Color(1, 1, 1, 0.75)
	add_child(help)
	status = Label.new()
	status.add_theme_font_size_override("font_size", 22)
	status.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	status.set_anchors_preset(Control.PRESET_CENTER_TOP)
	status.offset_left = -200
	status.offset_right = 200
	status.offset_top = 8
	add_child(status)
	Audio.play_music(1)
	start()


## A new arena: the hero (new, level 1) in the first room, the room cleared, the first wave.
func start() -> void:
	for n in loot.values():
		n.queue_free()
	loot.clear()
	var info: Dictionary = Campaign.new().lord_missions(LORD)[MISSION]
	var s: Array = info.get("start", [4, 2])
	sim = MapSim.new(map, MISSION, Vector2i(int(s[0]), int(s[1])))
	sim.rng = JavaRandom.new(seed if seed >= 0 else int(Time.get_ticks_usec() & 0x7fffffff))
	sim.no_enemies = true  # the lab brings the enemies itself
	tint = int(info.get("tint", 0))
	profile = Profile.new()
	profile.apply_to(sim)
	sim.difficulty = 1  # normal: the hero turns to the enemy, the auto-hunt is there
	for t in 400:
		if sim.exits_open() and sim.banner == 0 and sim.talk.is_empty():
			break
		sim.tick(-1, -1, sim.banner != 0 or not sim.talk.is_empty())
	# from now on the room's own list never ends: the soldiers keep coming in as in a fight
	# of the game, the room is never cleared and its exits stay shut
	sim.no_enemies = false
	_fill_waves()
	sim.room_phase = 0
	if people != null:
		people.free()
	people = MapPeople.new()
	people.name = "People"
	world.add_child(people)
	people.setup(sim, profile.head)
	people.side = MapPeople.side_of(GENERAL)  # mission 1's soldiers
	hero = people.hero
	hud.sim = sim
	camera.focus = sim.rooms.center(sim.cell)
	camera.snap()
	feel.freeze = 0.0
	_acc = 0.0
	_update_view(1.0)


## A wave: n of a kind come in through the room's exits (swordsmen are sometimes a squad).
func spawn(kind: int, n: int) -> void:
	if sim.spawn_spots.is_empty():
		return
	for i in n:
		var spot: Vector3i = sim.spawn_spots[sim.rng.below(sim.spawn_spots.size())]
		sim.create_enemy(kind, spot.x, spot.y, spot.z)


## A general comes in (one at a time, of the hero's level + 1); his words are skipped.
func spawn_general() -> void:
	for e in sim.enemies:
		if e.type < 200:
			return
	sim.waves[1] = 1  # his level is the hero's plus this
	spawn(GENERAL, 1)
	sim.skip_talk()
	_fill_waves()


## The room's list: swordsmen without end while the waves are on, nobody more while off.
func _fill_waves() -> void:
	sim.waves[0] = MapSim.KIND_SWORDS if waves_on else 0
	sim.waves[1] = 9999 if waves_on else 0


func _process(delta: float) -> void:
	var held := dir4_of(Input.get_vector("move_left", "move_right", "move_up", "move_down"))
	if held != -1 and held != _last_held:
		_pressed = held
	_last_held = held
	if _pressed_now("auto"):
		autopilot.toggle()
		hud.auto_on = autopilot.on
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
	if held != -1 or _fire or _hotkey != -1:
		autopilot.player_key()
	feel.advance(delta)
	_anim_dt = delta if feel.freeze <= 0.0 else 0.0
	if feel.freeze <= 0.0:
		_acc += delta
	while _acc >= tick and feel.freeze <= 0.0:
		_acc -= tick
		_tick(held)
	_update_view(_acc / tick)


func _tick(held: int) -> void:
	var auto: Dictionary = autopilot.decide(sim)
	if int(auto.held) != -1 and held == -1:
		held = int(auto.held)
	if bool(auto.fire):
		_fire = true
	if int(auto.hotkey) != -1 and _hotkey == -1:
		_hotkey = int(auto.hotkey)
	var before := CombatFeel.snapshot(sim)
	sim.tick(held, _pressed, _fire or sim.banner != 0, _hotkey, _potion, _belt)
	_pressed = -1
	_fire = false
	_hotkey = -1
	_potion = -1
	_belt = -1
	var list := CombatFeel.hits(sim, before)
	feel.react(list)
	feel.play_sounds(sim.sounds, list)
	feel.rumble(InputSetup.device)
	if not sim.talk.is_empty():
		sim.skip_talk()
	if god:
		sim.hero.hp = sim.hero.max_hp
		sim.hero.mp = sim.hero.max_mp
	if sim.failed or sim.finished or sim.hero.action == 10:
		start()
		return
	_fill_waves()
	if sim.room_phase == 1:
		sim.room_phase = 0  # a cleared room does not open: the hero stays in the arena
	hud.tick()
	trails = sim.trails(_trail_pick)
	var alive := {sim.hero: true}
	for e in sim.enemies:
		alive[e] = true
	for b in sim.breakables:
		alive[b] = true
	feel.forget_except(alive)


static func dir4_of(v: Vector2) -> int:
	if v.length() < 0.3:
		return -1
	if absf(v.x) > absf(v.y):
		return 6 if v.x > 0.0 else 2
	return 0 if v.y > 0.0 else 4


func _pressed_now(action: String) -> bool:
	var down := Input.is_action_pressed(action)
	var was: bool = _keys_down.get(action, false)
	_keys_down[action] = down
	return down and not was


## The position between the last two ticks (a jump, such as a new room, is not smoothed).
func _smooth(prev: Vector2i, now: Vector2i, t: float) -> Vector2:
	if (now - prev).length() > 40:
		return Vector2(now)
	return Vector2(prev).lerp(Vector2(now), clampf(t, 0.0, 1.0))


func _update_view(t: float) -> void:
	var n := 0
	for k in feel.on:
		n += 1 if feel.on[k] else 0
	status.text = (
		"Эффекты: ВКЛ" if n == feel.on.size() else ("Эффекты: ВЫКЛ" if n == 0 else "Эффекты: часть")
	)
	status.modulate = Color(0.6, 1.0, 0.6) if n > 0 else Color(1.0, 0.6, 0.6)
	people.update(t, _anim_dt, tick, feel)
	_anim_dt = 0.0
	hero = people.hero
	camera.focus = sim.rooms.center(sim.cell)
	feel.shake_camera(camera, PX)
	hud.queue_redraw()
	effects.show_shots(sim.arrows, t, not sim.arrows_wait())
	var shown: Array = sim.auras()
	shown.append_array(sim.effects())
	shown.append_array(sim.fires())
	for sp in sim.sparks():
		shown.append(["spark", sp[0], sp[1]])
	shown.append_array(trails)
	effects.show_effects(shown, t)
	for b in sim.breakables:
		var node := builder.get_node_or_null("Object_%d_%d" % [b.tile.x, b.tile.y]) as Node3D
		if node != null:
			node.visible = sim.breakable_shown(b)
			if node is Sprite3D:
				CombatFeel.flash_sprite(node as Sprite3D, feel.flash_of(b), _flash_mats)
			elif node.has_meta("material"):
				CombatFeel.flash_material(node.get_meta("material"), feel.flash_of(b))
	_place_loot()


func _place_loot() -> void:
	for d in loot.keys():
		if not sim.drops.has(d):
			loot[d].queue_free()
			loot.erase(d)
	for d in sim.drops:
		if loot.has(d):
			continue
		var s := Sprite3D.new()
		s.region_enabled = true
		if d.item > 10000:
			s.texture = _gold_tex
			s.region_rect = Rect2(Vector2.ZERO, _gold_tex.get_size())
		else:
			s.texture = _tool_tex
			var f: int = 11 if d.item > 100 else d.item - 1
			s.region_rect = Rect2(f * 28, 0, 28, 28)
		s.pixel_size = PX
		s.billboard = BaseMaterial3D.BILLBOARD_FIXED_Y
		s.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
		s.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
		world.add_child(s)
		s.global_position = (
			Hero.px_to_world(Vector2(d.pos)) + Vector3(0.0, s.region_rect.size.y / 54.0, 0.0)
		)
		loot[d] = s


## All effects off, or back to what they were: the same fight with and without them.
func toggle_all() -> void:
	var any_on := false
	for k in feel.on:
		any_on = any_on or feel.on[k]
	if any_on:
		_saved_on = feel.on.duplicate()
		for k in feel.on:
			feel.on[k] = false
	else:
		for k in feel.on:
			feel.on[k] = bool(_saved_on.get(k, true))
	panel.refresh()


func _unhandled_input(event: InputEvent) -> void:
	if not (event is InputEventKey and event.pressed and not event.echo):
		return
	match (event as InputEventKey).keycode:
		KEY_H:
			panel.visible = not panel.visible
		KEY_E:
			toggle_all()
		KEY_F2:
			spawn(MapSim.KIND_SWORDS, WAVE)
		KEY_F3:
			spawn(MapSim.KIND_ARCHERS, 2)
		KEY_F4:
			spawn_general()
		KEY_F6:
			god = not god
			panel.refresh()
		KEY_ESCAPE:
			get_tree().quit()
		_:
			return
	get_viewport().set_input_as_handled()
