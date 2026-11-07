extends Control
## The stop between missions (scripts/world/camp_map.gd): the hero walks about the camp of
## his place, and each way on from there is a gap in the pines with a colonel inside it.
## Talking to the colonel (attack / OK next to him) or walking out through the gap opens the
## missions of that place; a mission accepted from here comes back here when it is over (won:
## the camp of the new place; lost: this one again, to try once more with the same hero). A
## closed way is fenced. A main camp also has the town hall (every colonel and general) and the
## blacksmith. The game is saved when the hero comes into a camp. Pause opens the camp menu:
## the game menu, the world map, the main menu.
## Router.params: profile_path; first: true starts the first mission at once (a new game).

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Campaign := preload("res://scripts/core/campaign.gd")
const WorldMap := preload("res://scripts/core/world_map.gd")
const CampMap := preload("res://scripts/world/camp_map.gd")
const MapBuilder := preload("res://scripts/world/map_builder.gd")
const Hero := preload("res://scripts/world/hero.gd")
const Soldier := preload("res://scripts/world/soldier.gd")
const FollowCamera := preload("res://scripts/world/follow_camera.gd")
const TouchControls := preload("res://scripts/ui/touch_controls.gd")
const TALK_RANGE := 1.4  # tiles
const COLONEL_LOOKS := 6
const CAMERA_DISTANCE := 19.0  # the whole camp on the screen, the camera does not move

var path: String = Profile.PATH
var profile: RefCounted
var campaign := Campaign.new()
var world_map: RefCounted
var camp: RefCounted
var place := 0
var viewport: SubViewport
var world: Node3D
var builder: Node3D
var hero: CharacterBody3D
var camera: Camera3D
var title: Label
var hint: Label
var menu: PanelContainer
var menu_buttons: Array[Button] = []
## What the hero can use where he stands: {kind: "way"|"hall"|"smith", place, at: Vector3}
var spots: Array = []
var near := {}  # the spot in reach, or empty
var _leaving := false


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	profile = Profile.load_or_new(path)
	place = int(profile.place)
	world_map = WorldMap.new(campaign)
	var ways: Array = []
	for id in world_map.next_places(place):
		ways.append([id, profile.is_lord_open(id)])
	camp = CampMap.new(ways, CampMap.is_main(place))
	_build_world()
	_build_ui()
	if profile.on_map.is_empty():
		profile.save(path)  # the game is kept between missions, here
	if bool(Router.params.get("first", false)) and profile.done.is_empty():
		Router.params.erase("first")
		start_mission.call_deferred(1, 0)


func _build_world() -> void:
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
	builder = MapBuilder.new()
	builder.name = "Map"
	world.add_child(builder)
	builder.build(camp.data)
	hero = Hero.new()
	hero.name = "Hero"
	world.add_child(hero)
	hero.set_look(int(profile.head), profile.weapon_kind())
	hero.global_position = MapBuilder.cell_to_world(camp.start) + Vector3(0, 0.05, 0)
	hero.dir8 = 4  # facing up, into the camp
	camera = FollowCamera.new()
	camera.name = "Camera"
	camera.focus = Vector3(CampMap.W / 2.0, 0.0, CampMap.H / 2.0 + 0.5)
	camera.distance = CAMERA_DISTANCE
	world.add_child(camera)
	camera.make_current()
	camera.snap()
	for e in camp.exits:
		var at := MapBuilder.cell_to_world(e.inside)
		var names: Array = rulers(e.place).map(func(id): return tr(ruler_name(id)))
		var colonel: String = names[0] if not names.is_empty() else ""
		if names.size() > 1:
			colonel += " +%d" % (names.size() - 1)
		if e.open:
			var npc := Soldier.new()
			npc.name = "Colonel%d" % e.place
			var look := 1 + (_first_ruler(e.place) % COLONEL_LOOKS)
			npc.setup(1, 0, [], {"look": look, "side": 0})
			npc.set_frame(0, 0)
			npc.position = at
			world.add_child(npc)
		_label3d("Way%d" % e.place, "%s\n%s" % [campaign.lord_name(e.place), colonel if e.open else tr("world.closed")],
			at + Vector3(0, 2.6, 0), UiTheme.ACCENT if e.open else UiTheme.TEXT_DIM)
		spots.append({"kind": "way", "place": int(e.place), "open": bool(e.open), "at": at})
	if camp.main:
		var door := MapBuilder.cell_to_world(camp.hall_door())
		_label3d("Hall", tr("camp.hall"), door + Vector3(0, 2.8, -1.0), UiTheme.TEXT)
		spots.append({"kind": "hall", "at": door})
		var smith := MapBuilder.cell_to_world(camp.smith_spot())
		_label3d("Smith", tr("menu.blacksmith"), smith + Vector3(0, 2.0, -1.0), UiTheme.TEXT)
		spots.append({"kind": "smith", "at": smith})


func _label3d(node_name: String, text: String, at: Vector3, color: Color) -> void:
	var l := Label3D.new()
	l.name = node_name
	l.text = text
	l.font_size = 44
	l.outline_size = 12
	l.pixel_size = 0.009
	l.modulate = color
	l.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	l.no_depth_test = true
	l.position = at
	world.add_child(l)


func _build_ui() -> void:
	title = UiTheme.heading("", 32)
	title.name = "Place"
	title.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	title.set_anchors_preset(Control.PRESET_TOP_WIDE)
	title.offset_top = 12
	var kind := tr("camp.main") if camp.main else tr("camp.stop")
	title.text = "%s · %s" % [kind, campaign.lord_name(place) if place > 0 else tr("camp.start")]
	add_child(title)
	hint = UiTheme.note("Hint")
	hint.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	hint.offset_top = -64
	hint.offset_bottom = -24
	add_child(hint)
	add_child(TouchControls.new())
	menu = PanelContainer.new()
	menu.name = "Menu"
	menu.visible = false
	var center := CenterContainer.new()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)
	center.add_child(menu)
	var col := VBoxContainer.new()
	col.custom_minimum_size = Vector2(420, 0)
	col.add_theme_constant_override("separation", 8)
	menu.add_child(col)
	for item in [["GameMenu", "menu.game", open_game_menu], ["WorldMap", "campaign.world", open_world_map],
			["MainMenu", "camp.main_menu", func(): Router.go("main_menu")],
			["Back", "camp.back", toggle_menu]]:
		var b := Button.new()
		b.name = item[0]
		b.text = item[1]
		b.pressed.connect(item[2])
		col.add_child(b)
		menu_buttons.append(b)


## The colonels (ruler ids) who give missions at a place, in mission order.
func rulers(id: int) -> Array:
	var out: Array = []
	for m in campaign.lord_missions(id):
		var r := int(m.get("id", 0))
		if not r in out:
			out.append(r)
	return out


func _first_ruler(id: int) -> int:
	var r := rulers(id)
	return int(r[0]) if not r.is_empty() else 0


func ruler_name(ruler: int) -> String:
	for m in campaign.missions:
		if int(m.get("id", 0)) == ruler:
			return str(m.get("name", ""))
	return ""


func _physics_process(_delta: float) -> void:
	if menu.visible or _leaving:
		hero.external = true
		return
	hero.external = false
	near = spot_near(hero.global_position)
	hint.text = _hint_text(near)
	var e := exit_crossed(hero.global_position)
	if not e.is_empty():
		use(e)
		return
	if not near.is_empty() and (Input.is_action_just_pressed("attack") or Input.is_action_just_pressed("ui_accept")):
		use(near)


## The spot in talking range of a position, or empty.
func spot_near(pos: Vector3) -> Dictionary:
	for s in spots:
		var d := Vector2(pos.x - s.at.x, pos.z - s.at.z).length()
		if d <= TALK_RANGE:
			return s
	return {}


## The open way whose gap the position has walked out of, or empty.
func exit_crossed(pos: Vector3) -> Dictionary:
	if pos.z > 0.6 and pos.x > 0.6 and pos.x < CampMap.W - 0.6:
		return {}
	for i in camp.exits.size():
		var e: Dictionary = camp.exits[i]
		if not e.open:
			continue
		var c: Vector2i = e.gap[1]
		var hit := false
		match int(e.side):
			0:
				hit = pos.z <= 0.6 and absf(pos.x - (c.x + 0.5)) < 1.6
			1:
				hit = pos.x >= CampMap.W - 0.6 and absf(pos.z - (c.y + 0.5)) < 1.6
			2:
				hit = pos.x <= 0.6 and absf(pos.z - (c.y + 0.5)) < 1.6
		if hit:
			return spots[i]
	return {}


func _hint_text(s: Dictionary) -> String:
	if s.is_empty():
		return InputSetup.hint("camp.hint_walk")
	match str(s.kind):
		"way":
			if not s.open:
				return tr("camp.way_closed") % campaign.lord_name(s.place)
			return InputSetup.hint("camp.talk") % campaign.lord_name(s.place)
		"hall":
			return InputSetup.hint("camp.enter_hall")
		"smith":
			return InputSetup.hint("camp.enter_smith")
	return ""


func use(s: Dictionary) -> void:
	match str(s.get("kind", "")):
		"way":
			if s.open:
				_leaving = true
				Router.push("campaign", {"level": 2, "lord": int(s.place), "camp": true, "profile_path": path})
		"hall":
			Router.push("town_hall", {"profile_path": path})
		"smith":
			Router.push("blacksmith", {"profile_path": path})


## Straight into a mission's briefing (the first mission of a new game).
func start_mission(lord_id: int, mission: int) -> void:
	if not is_inside_tree():
		return
	var line: int = profile.next_briefing(RandomNumberGenerator.new())
	profile.save_keeping_map(path)
	_leaving = true
	Router.push("briefing", {"lord": lord_id, "mission": mission, "line": line, "profile_path": path})


func toggle_menu() -> void:
	menu.visible = not menu.visible
	if menu.visible:
		menu_buttons[0].grab_focus()


func open_game_menu() -> void:
	Router.push("game_menu", {"profile_path": path})


func open_world_map() -> void:
	Router.push("campaign", {"level": 1, "profile_path": path})


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause") or event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		toggle_menu()
