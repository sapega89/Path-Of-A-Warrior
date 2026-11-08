extends Control
## A mission of the original campaign on its map. The game itself runs in MapSim
## (original pixels and ticks); this screen reads the input, ticks the simulation every
## 120 ms and draws its state in 3D: the hero, the camera on the current room,
## the exit arrows and the "Stage" banners (after a won mission the exp bar of pyport on the
## pages Total Exp and Time Exp, the level gone up on it), the soldiers (the people as 3D
## figures playing the clips of their actions, scripts/world/map_people.gd), the effects made
## in code (scripts/world/map_effects.gd: skills, potions and scrolls, the fire on whoever a
## fire skill hits, the auras of buffs, the blood of hits, weapon trails, the archers' arrows), and
## the HUD. A talk on the map shows the portrait of who speaks beside the line, just
## above the HUD, as pyport's.
## Params: {lord, mission, seed (optional: the same enemies every run)}.
## A hit on the map is felt (scripts/world/combat_feel.gd, the options Hit effects, Screen shake,
## Vibration): the picture stands still a moment, the camera shakes, the one hit flashes white and
## recoils, the one killed flies off, the hit sound varies a little and the pad rumbles.
## The mouse, as pyport's: the left button beside the hero walks that way while it is held
## (dragging turns him, two quick clicks run), a click on the hero or the right button attacks,
## a click on the skill bar uses the slot, on AUTO toggles the auto-hunt, on PAUSE pauses.
## While someone talks on the map, SKIP (Q, F1, the pad's Back, a click on SKIP in AUTO's
## corner) skips the talk.

const MapBuilder := preload("res://scripts/world/map_builder.gd")
const MapArt := preload("res://scripts/world/map_art.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")
const Campaign := preload("res://scripts/core/campaign.gd")
const Hero := preload("res://scripts/world/hero.gd")
const FollowCamera := preload("res://scripts/world/follow_camera.gd")
const MapPeople := preload("res://scripts/world/map_people.gd")
const JavaRandom := preload("res://scripts/sim/java_random.gd")
const TouchControls := preload("res://scripts/ui/touch_controls.gd")
const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const MapHud := preload("res://scripts/ui/map_hud.gd")
const Autopilot := preload("res://scripts/sim/autopilot.gd")
const MapEffects := preload("res://scripts/world/map_effects.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Items := preload("res://scripts/core/items.gd")
const MissionPause := preload("res://scripts/ui/mission_pause.gd")
const ExpBar := preload("res://scripts/ui/exp_bar.gd")
const Stories := preload("res://scripts/core/stories.gd")
const CombatFeel := preload("res://scripts/world/combat_feel.gd")
const ItemSlot := preload("res://scripts/ui/item_slot.gd")

## One tick of the game, by the game speed of the settings (MapSim.TICK_MS at Med).
var tick := MapSim.TICK_MS / 1000.0
const GOLD_ICON := 12  # the heap of gold in the tool icons
## The exit arrow of the new art, pointing down: two brass chevrons in ink, the near one fainter.
const EXIT_ARROW := '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 40"><g fill="#b89550" stroke="#0f0d0c" stroke-width="2.5" stroke-linejoin="round"><path d="M4 3 L24 17 L44 3 L44 11 L24 25 L4 11 Z" fill-opacity="0.55"/><path d="M4 15 L24 29 L44 15 L44 23 L24 37 L4 23 Z"/></g><path d="M24 30.5 l3 2.5 l-3 2.5 l-3 -2.5 z" fill="#7e241f"/></svg>'
const Pictures := preload("res://scripts/ui/pictures.gd")
const WorldView := preload("res://scripts/world/world_view.gd")

var lord_id := 1
var mission := 0
var mission_info := {}
var lost_gear := {}  # what the hero lost with the mission (Profile.lose_gear), shown on its banner
var _fail_seen := false
var lord_name := ""
var sim: RefCounted
var viewport: SubViewport
var world: Node3D
var builder: Node3D
var people: MapPeople  # the hero and the enemies as figures
var hero: Node3D  # the hero's figure (people.hero)
var camera: Camera3D
var hud: MapHud
var profile: Profile
var effects: MapEffects  # the effects, arrows in flight among them
var banner: PanelContainer
var banner_text: Label
var exp_bar: ExpBar  # under the text of the pages Total Exp and Time Exp
## A talk over the map, as pyport's: the portrait of who speaks and the line beside it, just
## above the HUD.
var talk_box: Control
var talk_face: PanelContainer
var talk_portrait: TextureRect
var talk_panel: PanelContainer
var talk_text: Label
var arrows: Array[TextureRect] = []
var tint := 0
var loot := {}  # sim drop -> Sprite3D
var trails: Array = []  # the weapon trails of this tick
var _trail_pick := RandomNumberGenerator.new()
var _acc := 0.0
var _pressed := -1
var _fire := false
var _hotkey := -1  # a skill key pressed since the last tick
var _potion := -1  # a potion key pressed since the last tick
var _belt := -1  # a belt slot used by its key or a click on the skill bar since the last tick
var _skip := false  # SKIP since the last tick: the talk on the map is skipped
var autopilot := Autopilot.new()
var _keys_down := {}  # attack, skill and potion keys held at the last frame
var _last_held := -1
var _mouse_dir := -1  # the direction the left mouse button holds, -1: none
var _blink := 0
var pause_menu: MissionPause  # shown while the game is paused
var feel := CombatFeel.new()  # how a hit feels: the hitstop, shake, flash, flight, sound, rumble
var _flash_mats := {}  # Sprite3D -> its flash material
var _anim_dt := 0.0  # seconds the figures' clips move on this frame (0 while a hit holds)


## The mission to play: Router.params (the training gives its own).
func mission_params() -> Dictionary:
	return Router.params


func _ready() -> void:
	var p: Dictionary = mission_params()
	tick = Settings.tick_seconds()
	lord_id = int(p.get("lord", 1))
	mission = int(p.get("mission", 0))
	var campaign := Campaign.new()
	var ms := campaign.lord_missions(lord_id)
	mission_info = ms[mission] if mission < ms.size() else {}
	lord_name = campaign.lord_name(lord_id)

	var container := WorldView.new()
	container.name = "World"
	add_child(container)
	viewport = container.viewport
	viewport.own_world_3d = true
	world = Node3D.new()
	world.name = "WorldRoot"
	viewport.add_child(world)
	MapArt.add_environment(world)

	var map := MapBuilder.load_map(Campaign.lord_map(lord_id))
	builder = MapArt.new()
	builder.name = "Map"
	world.add_child(builder)
	builder.build(map)
	profile = Profile.load_or_new(str(p.get("profile_path", Profile.PATH)))
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


	people = MapPeople.new()
	people.name = "People"
	world.add_child(people)
	people.setup(sim, profile.head)
	hero = people.hero
	effects = MapEffects.new()
	effects.name = "Effects"
	world.add_child(effects)

	camera = FollowCamera.new()
	camera.name = "Camera"
	world.add_child(camera)
	camera.focus = sim.rooms.center(sim.cell)
	camera.make_current()
	camera.snap()

	for i in 4:
		var a := TextureRect.new()
		a.name = "Arrow%d" % i
		a.texture = exit_arrow(i)
		a.stretch_mode = TextureRect.STRETCH_SCALE
		a.mouse_filter = Control.MOUSE_FILTER_IGNORE
		a.visible = false
		add_child(a)
		arrows.append(a)

	hud = MapHud.new()
	hud.name = "Hud"
	hud.sim = sim
	hud.auto_allowed = auto_allowed()
	add_child(hud)

	banner = PanelContainer.new()
	banner.name = "Banner"
	banner.visible = false
	banner.mouse_filter = Control.MOUSE_FILTER_IGNORE
	banner_text = Label.new()
	banner_text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	banner_text.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	var lines := VBoxContainer.new()
	lines.mouse_filter = Control.MOUSE_FILTER_IGNORE
	lines.add_child(banner_text)
	exp_bar = ExpBar.new()
	exp_bar.name = "ExpBar"
	exp_bar.visible = false
	exp_bar.bars = sim.exp_bars
	exp_bar.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	lines.add_child(exp_bar)
	banner.add_child(lines)
	add_child(banner)
	_make_talk_box()

	var touch := TouchControls.new()
	touch.name = "Touch"
	add_child(touch)
	add_to_group(InputSetup.RIGHT_BUTTON)  # the right button attacks, not BACK
	feel.use_settings(Settings)
	Settings.changed.connect(_on_setting_changed)
	_update_view(0.0)


func _on_setting_changed(_key: String) -> void:
	feel.use_settings(Settings)


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
	# the pad's Back is both, as the HUD's corner: SKIP while someone talks, AUTO otherwise
	var skip_now := _pressed_now("skip")
	if _pressed_now("auto") and not (skip_now and hud.talking()):
		toggle_auto()
	if skip_now:
		_skip = true
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
	feel.advance(delta)
	_anim_dt = delta if feel.freeze <= 0.0 else 0.0
	if feel.freeze <= 0.0:
		_acc += delta  # while a hit holds the picture, no tick goes by
	while _acc >= tick and feel.freeze <= 0.0:
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
		if _skip:
			sim.skip_talk()
			_skip = false
		var before := CombatFeel.snapshot(sim)
		sim.tick(held, _pressed, _fire, _hotkey, _potion, _belt)
		var hits := CombatFeel.hits(sim, before)
		feel.react(hits)
		feel.play_sounds(sim.sounds, hits)
		feel.rumble(InputSetup.device)
		_forget_feel()
		_pressed = -1
		_fire = false
		_hotkey = -1
		_potion = -1
		_belt = -1
		hud.tick()
		_blink += 1
		trails = sim.trails(_trail_pick)
	if sim.failed and not _fail_seen:
		_fail_seen = true
		lost_gear = profile.lose_gear(sim.rng)
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


## The hit effects of those gone from the map are dropped.
func _forget_feel() -> void:
	var alive := {sim.hero: true}
	for e in sim.enemies:
		alive[e] = true
	for b in sim.breakables:
		alive[b] = true
	feel.forget_except(alive)


func _update_view(t: float) -> void:
	people.update(t, _anim_dt, tick, feel)
	_anim_dt = 0.0
	hero = people.hero
	camera.focus = sim.rooms.center(sim.cell)
	feel.shake_camera(camera, Hero.PIXEL_SIZE)
	hud.queue_redraw()
	effects.show_shots(sim.arrows, t, not sim.arrows_wait())
	var shown: Array = sim.auras()
	shown.append_array(sim.effects())
	shown.append_array(sim.fires())
	for sp in sim.sparks():
		shown.append(["blood", sp[0], sp[1]])  # the hits of MapSim land on people
	shown.append_array(trails)
	effects.show_effects(shown, t)
	_place_objects()
	_place_loot()
	_place_arrows()
	_show_banner()


## Breakable objects: they blink while breaking and are gone once broken.
func _place_objects() -> void:
	for b in sim.breakables:
		var node := builder.get_node_or_null("Object_%d_%d" % [b.tile.x, b.tile.y]) as Node3D
		if node != null:
			node.visible = sim.breakable_shown(b)
			if node is Sprite3D:
				CombatFeel.flash_sprite(node as Sprite3D, feel.flash_of(b), _flash_mats)
			elif node.has_meta("material"):
				CombatFeel.flash_material(node.get_meta("material"), feel.flash_of(b))


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
		# an icon of the new art, as big as the original's 28 px (gold: 24 px)
		var px := 24.0 if d.item > 10000 else 28.0
		s.texture = ItemSlot.icon("tool", GOLD_ICON if d.item > 10000 else (11 if d.item > 100 else d.item - 1))
		s.pixel_size = px / 27.0 / ItemSlot.ART
		s.billboard = BaseMaterial3D.BILLBOARD_FIXED_Y
		s.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
		world.add_child(s)
		s.global_position = Hero.px_to_world(Vector2(d.pos)) + Vector3(0.0, px / 54.0, 0.0)
		loot[d] = s


func _show_banner() -> void:
	talk_box.visible = sim.banner == 0 and not sim.talk.is_empty()
	if talk_box.visible:
		_place_talk()
	banner.visible = sim.banner != 0
	exp_bar.visible = sim.banner == MapSim.BANNER_TOTAL_EXP or sim.banner == MapSim.BANNER_TIME_EXP
	exp_bar.queue_redraw()
	if not banner.visible:
		return
	if sim.banner == MapSim.BANNER_ACQUIRED:
		banner_text.text = "%s\n%s" % [Items.name_of(sim.acquired), tr("mission.acquired")]
		_place_banner(0.3)
		return
	var stage := tr("mission.stage") + " " + str(sim.rooms_visited)
	if sim.banner == MapSim.BANNER_STAGE_CLEAR:
		stage += " " + tr("mission.complete")
	elif sim.banner == MapSim.BANNER_FAILED:
		stage = tr("mission.failed")
		if not lost_gear.is_empty():
			stage += "\n%s\n%s" % [tr("mission.lost"), Items.name_of(int(lost_gear.id))]
	elif sim.banner == MapSim.BANNER_SUCCESS:
		stage = "%s\n%s\n%d" % [tr("mission.success"), tr("mission.gold"), sim.gold_reward()]
	elif sim.banner == MapSim.BANNER_TOTAL_EXP or sim.banner == MapSim.BANNER_TIME_EXP:
		if sim.banner == MapSim.BANNER_TOTAL_EXP:
			stage = "%s\n%d" % [tr("mission.total_exp"), sim.exp_reward()]
		else:
			stage = "%s\n%s %s\n%s %s" % [tr("mission.time_exp"), tr("mission.time_limit"),
				clock(sim.time_limit), tr("mission.time_taken"), clock(sim.play_seconds())]
		if sim.exp_bars.level_up_ticks > 0:
			stage += "\n" + tr("mission.level_up") % sim.exp_bars.level
	banner_text.text = "%s\n%s\n%s" % [lord_name, tr(str(mission_info.get("name", ""))), stage]
	_place_banner(0.3)


## mm:ss
static func clock(secs: int) -> String:
	return "%02d:%02d" % [secs / 60, secs % 60]


func _make_talk_box() -> void:
	talk_box = Control.new()
	talk_box.name = "Talk"
	talk_box.visible = false
	talk_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	talk_box.set_anchors_preset(Control.PRESET_FULL_RECT)
	var style := UiTheme.box(Color(UiTheme.PANEL, 0.92), UiTheme.ACCENT_DARK, 2)
	talk_face = PanelContainer.new()
	talk_face.name = "Face"
	talk_face.mouse_filter = Control.MOUSE_FILTER_IGNORE
	talk_face.add_theme_stylebox_override("panel", StyleBoxEmpty.new())  # the portrait has its frame
	talk_portrait = Pictures.framed("Portrait", Vector2(46, 46))
	talk_portrait.mouse_filter = Control.MOUSE_FILTER_IGNORE
	talk_face.add_child(talk_portrait)
	talk_box.add_child(talk_face)
	talk_panel = PanelContainer.new()
	talk_panel.name = "Box"
	talk_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var box_style := style.duplicate()
	box_style.set_content_margin_all(8)
	talk_panel.add_theme_stylebox_override("panel", box_style)
	talk_text = Label.new()
	talk_text.name = "Line"
	talk_text.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	talk_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	talk_text.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	talk_panel.add_child(talk_text)
	talk_box.add_child(talk_panel)
	add_child(talk_box)


## The portrait of who speaks the line shown now: the general's, or the hero's for his own lines.
func talk_portrait_id() -> int:
	if sim.hero_talks():
		return Stories.HERO_PORTRAIT + int(profile.head)
	return int(sim.general.get("portrait", 0))


## As pyport's map talk (in its pixels, over the HUD's width): a 48 px portrait box at the left
## and the speech box from x 54, 38 high, both just above the HUD (and its skill bar).
func _place_talk() -> void:
	var view := get_viewport_rect().size
	var k := hud.scale_of(view)
	var top := view.y - (MapHud.PANEL_H + (MapHud.BAR_H if hud.show_bar else 0)) * k
	var left := view.x / 2.0 - 120.0 * k
	talk_portrait.texture = Pictures.portrait(talk_portrait_id())
	talk_portrait.custom_minimum_size = Vector2(46, 46) * k
	talk_face.position = Vector2(left + 2 * k, top - 50 * k)
	talk_face.size = Vector2(48, 48) * k
	talk_text.text = sim.talk_text()
	talk_text.add_theme_font_size_override("font_size", int(11 * k))
	talk_panel.custom_minimum_size = Vector2(184, 38) * k
	talk_panel.size = talk_panel.custom_minimum_size
	talk_panel.reset_size()
	talk_panel.position = Vector2(left + 54 * k, top - 2 * k - talk_panel.size.y)


func _place_banner(y: float) -> void:
	var view := get_viewport_rect().size
	banner.size = Vector2(520, 0)
	banner.reset_size()
	banner.position = Vector2((view.x - banner.size.x) / 2.0, view.y * y)


## The exit arrow to side i (0 down, 1 left, 2 up, 3 right), 72 px across.
static func exit_arrow(i: int) -> Texture2D:
	var img := Image.new()
	img.load_svg_from_string(EXIT_ARROW, 1.5)
	match i:
		1: img.rotate_90(CLOCKWISE)
		2: img.rotate_180()
		3: img.rotate_90(COUNTERCLOCKWISE)
	return ImageTexture.create_from_image(img)


## The exit arrows at the screen's edges, blinking while the exits are open; the one down sits
## above the HUD (at the very bottom the HUD hid it).
func _place_arrows() -> void:
	var view := get_viewport_rect().size
	var lit: bool = sim.exits_open() and (_blink & 2) != 0
	for i in 4:
		var a := arrows[i]
		a.visible = lit and sim.rooms.has_exit(sim.cell, i + 1)
		var s := a.texture.get_size()
		a.size = s
		match i:
			0: a.position = Vector2((view.x - s.x) / 2.0, hud.top_of(view) - s.y - 8)  # above the HUD
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
	_pause_menu_ready(pause_menu)
	add_child(pause_menu)


## The pause menu before it is shown (the training makes its Exit skip the training).
func _pause_menu_ready(_menu: MissionPause) -> void:
	pass


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


## The right mouse button attacks while the hero plays; in the pause menu or after the end it is
## BACK, as everywhere (InputSetup).
func uses_right_button() -> bool:
	return pause_menu == null and is_processing()


## The direction from the hero to a point of the screen (6 right, 2 left, 4 up, 0 down), or -1
## on the hero himself: within 14 x 20 original pixels of the middle of his body, 20 px above
## his position, as pyport's pointer.
func pointer_dir(at: Vector2) -> int:
	var middle := hero.global_position + Vector3(0, (20 + Hero.FOOT_PX) * Hero.PIXEL_SIZE, 0)
	# measured on the still camera: the shake of a hit does not turn the hero
	var shaken := [camera.h_offset, camera.v_offset, camera.rotation.z]
	camera.h_offset = 0.0
	camera.v_offset = 0.0
	camera.rotation.z = 0.0
	var c := camera.unproject_position(middle)
	var box := Vector2(
		absf(camera.unproject_position(middle + Vector3(14 * Hero.PIXEL_SIZE, 0, 0)).x - c.x),
		absf(camera.unproject_position(middle + Vector3(0, 20 * Hero.PIXEL_SIZE, 0)).y - c.y))
	camera.h_offset = shaken[0]
	camera.v_offset = shaken[1]
	camera.rotation.z = shaken[2]
	var d := at - c
	if absf(d.x) < box.x and absf(d.y) < box.y:
		return -1
	if absf(d.x) >= absf(d.y):
		return 6 if d.x > 0.0 else 2
	return 0 if d.y > 0.0 else 4


## Auto-hunt on / off (Tab, F, the pad's Back or a click on AUTO); only on normal, hard has no AUTO.
func toggle_auto() -> void:
	if not auto_allowed():
		return
	autopilot.toggle()
	hud.auto_on = autopilot.on
	hud.queue_redraw()



## The auto-hunt is there only on normal: on hard the player fights by hand.
func auto_allowed() -> bool:
	return sim != null and sim.difficulty != 0


## A click on the skill bar: a belt slot is used, a skill cast; on the corner AUTO / SKIP. False
## when it missed them.
func click_bar(at: Vector2) -> bool:
	if hud.skip_at(at):
		get_viewport().set_input_as_handled()
		_skip = true
		return true
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


## No line of control hints under this screen: it shows its own (scripts/ui/hint_bar.gd).
func controls_hint() -> String:
	return ""
