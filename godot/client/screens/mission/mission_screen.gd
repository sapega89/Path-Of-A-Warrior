class_name MissionScreen
extends BaseScreen
## A mission of the original campaign on its map. The game itself runs in MapSim
## (original pixels and ticks); this screen reads the input, ticks the simulation every
## 120 ms and draws its state in 3D: the hero, the camera on the current room,
## the exit arrows and the "Stage" banners (after a won mission the exp bar on the
## pages Total Exp and Time Exp, the level gone up on it), the soldiers (the people as 3D
## figures playing the clips of their actions, scripts/world/map_people.gd), the effects made
## in code (scripts/world/map_effects.gd: skills, potions and scrolls, the fire on whoever a
## fire skill hits, the auras of buffs, the blood of hits, weapon trails, the archers' arrows), and
## the HUD. A talk on the map shows the portrait of who speaks beside the line, just
## above the HUD.
## Params: {lord, mission, seed (optional: the same enemies every run)}.
## A hit on the map is felt (scripts/world/combat_feel.gd, the options Hit effects, Screen shake,
## Vibration): the picture stands still a moment, the camera shakes, the one hit flashes white and
## recoils, the one killed flies off, the hit sound varies a little and the pad rumbles.
## The mouse: the left button beside the hero walks that way while it is held
## (dragging turns him, two quick clicks run), a click on the hero or the right button attacks.
## The HUD's buttons (screens/mission/hud/map_hud.gd): a slot of the skill bar uses it, AUTO
## toggles the auto-hunt, PAUSE pauses. While someone talks on the map, SKIP (Q, F1, the pad's
## Back, the button SKIP in AUTO's corner) skips the talk.

const GOLD_ICON := 12  # the heap of gold in the tool icons
const LOOT := preload("res://scenes/world/loot.tscn")
const FADE_TIME := 0.35

## One tick of the game, by the game speed of the settings (MapSim.TICK_MS at Med).
var tick := MapSim.TICK_MS / 1000.0
var lord_id := 1
var mission := 0
var mission_info := {}
var lost_gear := {}  # what the hero lost with the mission (Profile.lose_gear), shown on its banner
var lord_name := ""
var sim: MapSim
var hero: Node3D  # the hero's figure (people.hero)
var profile: Profile
## After a mission won: the ways on, one per open place the campaign goes to next:
## [{exit: Rooms.EXIT_*, half: -1 the whole side | 0 its first half | 1 its second, place}]
var ways_out: Array = []
var tint := 0
var loot := {}  # sim drop -> Sprite3D
var trails: Array = []  # the weapon trails of this tick
var autopilot := Autopilot.new()
var pause_menu: MissionPause  # shown while the game is paused
var feel := CombatFeel.new()  # how a hit feels: the hitstop, shake, flash, flight, sound, rumble

var _fail_seen := false
var _last_cell := -1
var _fade_tween: Tween
var _trails_before: Array = []  # and of the last one, fading
var _trail_pick := RandomNumberGenerator.new()
var _acc := 0.0
var _pressed := -1
var _fire := false
var _hotkey := -1  # a skill key pressed since the last tick
var _potion := -1  # a potion key pressed since the last tick
var _belt := -1  # a belt slot used by its key or a click on the skill bar since the last tick
var _skip := false  # SKIP since the last tick: the talk on the map is skipped
var _last_held := -1
var _mouse_dir := -1  # the direction the left mouse button holds, -1: none
var _blink := 0
var _flash_mats := {}  # Sprite3D -> its flash material
var _anim_dt := 0.0  # seconds the figures' clips move on this frame (0 while a hit holds)

@onready var world: Node3D = $World/Viewport/WorldRoot
@onready var builder: MapArt = $World/Viewport/WorldRoot/Map
@onready var camera: FollowCamera = $World/Viewport/WorldRoot/Camera
@onready var people: MapPeople = $World/Viewport/WorldRoot/People  # the hero and enemies
@onready var effects: MapEffects = $World/Viewport/WorldRoot/Effects  # arrows in flight too
@onready var hud: MapHud = %Hud
@onready var fade: ColorRect = %Fade  # the short dark between two rooms
@onready var exit_arrows: ExitArrows = $Arrows
@onready var banner: MissionBanner = %Banner
## A talk over the map: the portrait of who speaks and the line beside it, just above the HUD.
@onready var talk_box: MapTalk = %Talk


func _ready() -> void:
	var p: Dictionary = Router.params
	tick = Settings.tick_seconds()
	lord_id = int(p.get("lord", 1))
	mission = int(p.get("mission", 0))
	var campaign := Campaign.new()
	var ms := campaign.lord_missions(lord_id)
	mission_info = ms[mission] if mission < ms.size() else {}
	lord_name = campaign.lord_name(lord_id)

	var map := MapBuilder.load_map(Campaign.lord_map(lord_id))
	builder.build(map)
	profile = Profile.load_or_new(profile_path())
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

	people.setup(sim, profile.head)
	hero = people.hero
	camera.focus = sim.rooms.center(sim.cell)
	camera.snap()

	hud.sim = sim
	hud.auto_allowed = auto_allowed()
	banner.exp_bar.bars = sim.exp_bars
	add_to_group(InputSetup.RIGHT_BUTTON)  # the right button attacks, not BACK
	feel.use_settings(Settings)
	Settings.changed.connect(_on_setting_changed)
	_update_view(0.0)


## Leaving the mission from its pause menu (Exit to Menu) lets the game run again.
func _exit_tree() -> void:
	if pause_menu != null:
		get_tree().paused = false


## A setting changed over the pause menu: the hit effects and the game speed apply at once.
func _on_setting_changed(_key: String) -> void:
	feel.use_settings(Settings)
	tick = Settings.tick_seconds()


## The 4-direction of a stick or keys (the original hero walks in 4 directions), or -1.
static func dir4_of(v: Vector2) -> int:
	if v.length() < 0.3:
		return -1
	if absf(v.x) > absf(v.y):
		return 6 if v.x > 0.0 else 2
	return 0 if v.y > 0.0 else 4


func _process(delta: float) -> void:
	var held := _held_dir()
	feel.advance(delta)
	_anim_dt = delta if feel.freeze <= 0.0 else 0.0
	if feel.freeze <= 0.0:
		_acc += delta  # while a hit holds the picture, no tick goes by
	while _acc >= tick and feel.freeze <= 0.0:
		_acc -= tick
		held = _one_tick(held)
	if sim.failed and not _fail_seen:
		_fail_seen = true
		lost_gear = profile.lose_gear(sim.rng)
	if sim.choosing and sim.way_out != 0:
		var to := way_for(sim.way_out, Hero.px_to_world(Vector2(sim.hero.pos)))
		if to > 0:
			set_process(false)
			profile.heading = to
			profile.save()
			Router.back()
			return
		sim.way_out = 0
	if sim.finished:
		_finish()
		return
	_update_view(_acc / tick)


## The direction held this frame (a key or the mouse), -1 none. A key of the player hands the
## autopilot off for a while.
func _held_dir() -> int:
	var held := dir4_of(Input.get_vector("move_left", "move_right", "move_up", "move_down"))
	if held == -1:
		held = _mouse_dir
	if held != -1 and held != _last_held:
		_pressed = held  # a new direction this tick: a key press (tap to walk)
	_last_held = held
	if held != -1 or _fire or _hotkey != -1 or _potion != -1 or _belt != -1:
		autopilot.player_key()
	return held


## One tick of the map with the player's keys and the autopilot's, and how its hits feel.
## Returns the direction held (the autopilot's, when the player holds none).
func _one_tick(held: int) -> int:
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
	_trails_before = trails
	trails = sim.trails(_trail_pick)
	return held


## The mission is over: the hero takes what he won, and the screen leaves, to the story of an
## ending; or, won with places to go on to, the hero chooses his way out in the last room.
func _finish() -> void:
	profile.take_from(sim, lord_id, mission, int(mission_info.get("id", 0)))
	var ending: int = profile.advance(sim, lord_id, mission_info)
	profile.save()
	if ending < 0 and sim.won:
		ways_out = ways_on(lord_id)
		if not ways_out.is_empty():
			# The way on is chosen here, in the last room: an arrow per place on.
			sim.start_choosing()
			_update_view(_acc / tick)
			return
	set_process(false)
	Router.back()
	if ending >= 0:
		Router.push(
			"story",
			{
				"story": ending,
				"reward_item": profile.reward_item,
				"opened_lord": profile.opened_lord
			}
		)


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
	if sim.cell != _last_cell:
		if _last_cell >= 0 and fade != null:
			if _fade_tween != null:
				_fade_tween.kill()
			fade.color.a = 1.0
			_fade_tween = create_tween()
			_fade_tween.tween_property(fade, "color:a", 0.0, FADE_TIME)
		_last_cell = sim.cell
		# Only this room and the next ones it leads to; the rest is the ground around the map.
		builder.show_only(sim.rooms.view_cells(sim.cell))
	people.update(t, _anim_dt, tick, feel)
	_anim_dt = 0.0
	hero = people.hero
	camera.focus = sim.rooms.center(sim.cell)
	feel.shake_camera(camera, Hero.PIXEL_SIZE)
	hud.refresh()
	effects.show_shots(sim.arrows, t, not sim.arrows_wait())
	var shown: Array = sim.auras()
	shown.append_array(sim.effects())
	shown.append_array(sim.fires())
	for sp in sim.sparks():  # the hits of MapSim land on people: a flash and blood
		shown.append(["spark", sp[0], sp[1]])
		shown.append(["blood", sp[0], sp[1]])
	shown.append_array(MapPictures.trails_with_fading(trails, _trails_before))
	effects.show_effects(shown, t)
	_place_objects()
	_place_loot()
	exit_arrows.show_exits(sim, ways_out, (_blink & 2) != 0)
	_show_banner()


## Breakable objects: they blink while breaking and are gone once broken.
func _place_objects() -> void:
	for b in sim.breakables:
		var node := builder.get_node_or_null("Object_%d_%d" % [b.tile.x, b.tile.y]) as Node3D
		if node != null:
			node.visible = sim.breakable_shown(b) and builder.is_shown(b.tile.x, b.tile.y)
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
		var s: Sprite3D = LOOT.instantiate()
		# an icon of the new art, 28 px of the map high (gold: 24 px)
		var px := 24.0 if d.item > 10000 else 28.0
		s.texture = ItemSlot.icon(
			"tool", GOLD_ICON if d.item > 10000 else (11 if d.item > 100 else d.item - 1)
		)
		s.pixel_size = px / 27.0 / ItemSlot.ART
		world.add_child(s)
		s.global_position = Hero.px_to_world(Vector2(d.pos)) + Vector3(0.0, px / 54.0, 0.0)
		loot[d] = s


## The talk on the map, or the banner of the page the mission is on.
func _show_banner() -> void:
	talk_box.visible = sim.banner == 0 and not sim.talk.is_empty()
	if talk_box.visible:
		talk_box.show_line(Pictures.portrait(talk_portrait_id()), sim.talk_text())
	banner.show_page(sim, lord_name, tr(str(mission_info.get("name", ""))), lost_gear)


## The portrait of who speaks the line shown now: the general's, or the hero's for his own lines.
func talk_portrait_id() -> int:
	if sim.hero_talks():
		return Stories.HERO_PORTRAIT + int(profile.head)
	return int(sim.general.get("portrait", 0))


## The ways on from a place won: one per open place the campaign goes to next, each on a side
## of the room in a shuffled order (a side says nothing). Only the sides the hero can walk out
## of (MapSim.open_sides) carry ways while they are enough; with more places than sides, some
## sides carry two, one on each half.
func ways_on(won_place: int) -> Array:
	var places: Array = WorldMap.new(Campaign.new()).next_places(won_place).filter(
		func(id): return profile.is_lord_open(id)
	)
	var sides: Array = [Rooms.EXIT_UP, Rooms.EXIT_RIGHT, Rooms.EXIT_LEFT, Rooms.EXIT_DOWN]
	var pick := RandomNumberGenerator.new()
	pick.seed = hash([won_place, profile.done.size()])
	for i in range(sides.size() - 1, 0, -1):
		var j := pick.randi_range(0, i)
		var t: int = sides[i]
		sides[i] = sides[j]
		sides[j] = t
	var open: Array[int] = sim.open_sides()
	var walled: Array = sides.filter(func(s: int) -> bool: return not s in open)
	sides = sides.filter(func(s: int) -> bool: return s in open)
	while sides.is_empty() or sides.size() * 2 < places.size() and not walled.is_empty():
		sides.append(walled.pop_front())  # too few open sides: a walled one too
	var slots: Array = []
	var split := maxi(places.size() - sides.size(), 0)  # sides that carry two
	for k in mini(sides.size(), places.size()):
		if k < split:
			slots.append({"exit": sides[k], "half": 0})
			slots.append({"exit": sides[k], "half": 1})
		else:
			slots.append({"exit": sides[k], "half": -1})
	var out: Array = []
	for k in mini(slots.size(), places.size()):
		var w: Dictionary = slots[k]
		w["place"] = places[k]
		out.append(w)
	return out


## The place of the way on the hero walked into (a side, and on a side with two, the half
## he stands in), or 0.
func way_for(exit_no: int, at: Vector3) -> int:
	var mid: Vector3 = sim.rooms.center(sim.cell)
	for w in ways_out:
		if int(w.exit) != exit_no:
			continue
		if int(w.half) == -1:
			return int(w.place)
		var along: float = (
			at.x - mid.x if exit_no == Rooms.EXIT_UP or exit_no == Rooms.EXIT_DOWN else at.z - mid.z
		)
		if (along < 0.0) == (int(w.half) == 0):
			return int(w.place)
	return 0


## Stops the mission and shows the pause menu (Resume, Options, Exit to Menu, Exit Game): the
## scene tree is paused, and only the menu (and what it opens) runs.
func pause() -> void:
	if pause_menu != null:
		return
	get_tree().paused = true
	_release_keys()
	pause_menu = (load(MissionPause.SCENE) as PackedScene).instantiate()
	pause_menu.sim = sim
	pause_menu.save_game = save_on_map
	pause_menu.resumed.connect(resume)
	add_child(pause_menu)


func resume() -> void:
	if pause_menu == null:
		return
	pause_menu.queue_free()
	pause_menu = null
	get_tree().paused = false
	_acc = 0.0
	_last_held = -1


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


## Back pauses the mission (below), so the base does not take it.
func handles_back() -> bool:
	return false


func _screen_input(event: InputEvent) -> void:
	if pause_menu != null:
		return
	if event.is_action_pressed("pause") or event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		pause()
	elif is_processing():
		_take_key(event)


## A key of the game pressed while it plays: kept until the next tick takes it.
func _take_key(event: InputEvent) -> void:
	# the pad's Back is both, as the HUD's corner: SKIP while someone talks, AUTO otherwise
	var skip := event.is_action_pressed("skip")
	if event.is_action_pressed("auto") and not (skip and hud.talking()):
		toggle_auto()
	if skip:
		_skip = true
	if event.is_action_pressed("attack"):
		_fire = true
	for i in 5:
		if event.is_action_pressed("skill_%d" % (i + 1)):
			_hotkey = i
		if event.is_action_pressed("belt_%d" % (i + 1)):
			_belt = i
	for i in 2:
		if event.is_action_pressed("potion_%d" % (i + 1)):
			_potion = i


## The mouse (and a touch, which comes as a click too) over the map: the screen itself takes
## it, as the controls over the map let it through.
func _gui_input(event: InputEvent) -> void:
	if pause_menu != null:
		return
	if event is InputEventMouseButton:
		_mouse_button(event)
	elif event is InputEventMouseMotion and _mouse_dir != -1:
		var d := pointer_dir(event.position)
		if d != -1 and not hud.covers(event.position):
			_mouse_dir = d  # dragging turns the hero


func _mouse_button(event: InputEventMouseButton) -> void:
	if event.button_index == MOUSE_BUTTON_LEFT and not event.pressed:
		_mouse_dir = -1
		return
	if not event.pressed:
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
## his position.
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
		absf(camera.unproject_position(middle + Vector3(0, 20 * Hero.PIXEL_SIZE, 0)).y - c.y)
	)
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
	hud.refresh()


## The auto-hunt is there only on normal: on hard the player fights by hand.
func auto_allowed() -> bool:
	return sim != null and sim.difficulty != 0


## The HUD's buttons, while the pause menu is not open: a belt slot is used, a skill cast,
## AUTO toggles the auto-hunt, SKIP skips the talk, PAUSE pauses.
func _on_hud_belt_pressed(slot: int) -> void:
	if pause_menu == null:
		_belt = slot


func _on_hud_skill_pressed(slot: int) -> void:
	if pause_menu == null:
		_hotkey = slot


func _on_hud_auto_pressed() -> void:
	if pause_menu == null:
		toggle_auto()


func _on_hud_skip_pressed() -> void:
	if pause_menu == null:
		_skip = true


func _on_hud_pause_pressed() -> void:
	pause()


## No line of control hints under this screen: it shows its own (scripts/ui/hint_bar.gd).
func controls_hint() -> String:
	return ""
