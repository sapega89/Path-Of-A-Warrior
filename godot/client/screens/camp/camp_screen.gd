class_name CampScreen
extends BaseScreen
## The stop between missions (scripts/world/camp_map.gd): the hero walks about the camp of
## his place, and each way on from there (one, two or three places, as the campaign goes) is a
## gap in the trees with a blinking arrow; past the gap lies the land of that place (a lake,
## mountains, a forest, a town or the steppe, from its map: terrain()), nothing more, so which
## way is better is learnt by playing. Walking out tells the story of the next mission of that
## place not won yet (choices()), then its briefing; the mission comes back
## here when it is over (won: the camp of the new place; lost: this one again, to try once
## more with the same hero). A closed way is fenced. Every camp has the blacksmith (buy, sell,
## enchant,
## combine), the warehouse and the town hall (every colonel and general, and the visits of
## the generals: one after each mission won, scripts/core/visits.gd). The game is saved when the
## hero comes into a camp. Pause opens the camp menu:
## the game menu, the world map, the main menu.
## Router.params: profile_path; first: true starts the first mission at once (a new game).

const TALK_RANGE := 1.4  # tiles
## The arrow picture for a gap on the top, the right and the left side (arrow0..3: down,
## left, up, right).
const ARROW_OF_SIDE := [2, 3, 1]
const BLINK_TIME := 0.25
const MAX_WAYS := 6  # gaps in a camp
## What lies past a gap, by the land of its place: pieces of the new art (MapArt.PROP) and,
## for a lake, its water.
const LAND := {
	"mountains":
	[
		["boulder", 1.8, -2.6, 1.6],
		["crag", 2.8, 2.4, 2.4],
		["boulder", 4.0, -1.4, 2.4],
		["crag", 4.4, 2.2, 3.4],
		["rock", 2.0, 1.4, 1.0]
	],
	"forest":
	[
		["fir", 1.8, -2.4, 1.0],
		["fir", 2.2, 2.4, 1.1],
		["fir", 3.8, -3.4, 1.2],
		["fir", 4.2, 3.2, 1.2],
		["bush", 1.4, -1.4, 1.0]
	],
	"town":
	[
		["palisade", 1.4, -2.0, 1.0],
		["palisade", 1.4, -2.8, 1.0],
		["palisade", 1.4, 2.0, 1.0],
		["palisade", 1.4, 2.8, 1.0],
		["hut", 3.6, -2.8, 0.6]
	],
	"steppe":
	[
		["hay", 1.6, -2.0, 0.6],
		["bush", 2.4, 2.2, 1.0],
		["pebbles", 3.0, -1.4, 1.0],
		["hay", 3.6, 2.8, 0.7]
	],
	"lake": [["bush", 1.4, -1.8, 0.9], ["rock", 1.6, 2.0, 1.0]],
}
const CAMERA_DISTANCE := 19.0  # the whole camp on the screen, the camera does not move

var path: String = Profile.PATH
var profile: RefCounted
var campaign := Campaign.new()
var world_map: RefCounted
var camp: RefCounted
var place := 0
## What the hero can use where he stands: {kind: "way"|"hall"|"smith", place, at: Vector3}
var spots: Array = []
var near := {}  # the spot in reach, or empty
var arrows: Array[Sprite3D] = []
var rng := RandomNumberGenerator.new()
var _blink := 0.0
var _leaving := false

@onready var world: Node3D = $World/Viewport/WorldRoot
@onready var builder: MapArt = $World/Viewport/WorldRoot/Map
@onready var hero: Hero = $World/Viewport/WorldRoot/Hero
@onready var figure: ArtFigure = $World/Viewport/WorldRoot/Hero/Figure
@onready var camera: FollowCamera = $World/Viewport/WorldRoot/Camera
@onready var title: Label = %Place
@onready var hint: Label = %Hint
@onready var menu: PanelContainer = %Menu


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	place = int(profile.place)
	world_map = WorldMap.new(campaign)
	rng.seed = hash([place, profile.done.size()])  # the same ways each time back here
	camp = CampMap.new(choices(), CampMap.is_main(camp_place()), camp_place())
	_build_world()
	_show_place()
	if profile.on_map.is_empty():
		profile.save(path)  # the game is kept between missions, here
	if bool(Router.params.get("first", false)) and profile.done.is_empty():
		Router.params.erase("first")
		start_mission.call_deferred(1, 0)


func _build_world() -> void:
	builder.build(camp.data)
	hero.set_look(int(profile.head), profile.weapon_kind())
	hero.global_position = MapBuilder.cell_to_world(camp.start) + Vector3(0, 0.05, 0)
	hero.dir8 = 4  # facing up, into the camp
	# The hero as the missions show him: the figure of his class with his blade (the body
	# walks, the figure plays idle or walk and turns the way he goes).
	figure.setup(MapPeople.HEROES[clampi(int(profile.head), 0, 3)])
	figure.unequip_all()
	figure.equip(MapPeople.BLADES[clampi(profile.weapon_kind(), 0, 1)])
	figure.rotation.y = Motion.yaw_of(hero.dir8)
	figure.play("idle", 0.0)
	if hero.sprite != null:
		hero.sprite.visible = false
	# a little of the land past the top
	camera.focus = Vector3(CampMap.W / 2.0, 0.0, CampMap.H / 2.0 - 0.3)
	camera.distance = CAMERA_DISTANCE
	camera.snap()
	# Each open way: only the blinking arrow of the original rooms in its gap; nothing says
	# where it leads (that is learnt by playing).
	for e in camp.exits:
		var at := MapBuilder.cell_to_world(e.inside)
		if e.open:
			var arrow := Sprite3D.new()
			arrow.name = "Arrow%d_%d" % [e.place, e.mission]
			arrow.texture = MissionScreen.exit_arrow(ARROW_OF_SIDE[int(e.side)])
			arrow.pixel_size = 1.0 / 72.0
			arrow.billboard = BaseMaterial3D.BILLBOARD_ENABLED
			arrow.no_depth_test = true
			arrow.position = MapBuilder.cell_to_world(e.gap[1]).lerp(at, 0.5) + Vector3(0, 0.6, 0)
			world.add_child(arrow)
			arrows.append(arrow)
		_scenery(e, terrain(int(e.place)))
		spots.append(
			{
				"kind": "way",
				"place": int(e.place),
				"mission": int(e.mission),
				"open": bool(e.open),
				"at": at
			}
		)
	var smith := MapBuilder.cell_to_world(camp.smith_spot())
	%Smith.position = smith + Vector3(0, 2.1, -0.6)
	spots.append({"kind": "smith", "at": smith})
	var store := MapBuilder.cell_to_world(camp.store_spot())
	%Store.position = store + Vector3(0, 1.3, -0.5)
	spots.append({"kind": "store", "at": store})
	var door := MapBuilder.cell_to_world(camp.hall_door())
	%Hall.position = door + Vector3(0, 2.8, -1.0)
	spots.append({"kind": "hall", "at": door})


func _show_place() -> void:
	var kind := tr("camp.main") if camp.main else tr("camp.stop")
	title.text = (
		"%s · %s"
		% [kind, campaign.lord_name(camp_place()) if camp_place() > 0 else tr("camp.start")]
	)


## The colonels (ruler ids) who give missions at a place, in mission order.
func rulers(id: int) -> Array:
	var out: Array = []
	for m in campaign.lord_missions(id):
		var r := int(m.get("id", 0))
		if not r in out:
			out.append(r)
	return out


func ruler_name(ruler: int) -> String:
	for m in campaign.missions:
		if int(m.get("id", 0)) == ruler:
			return str(m.get("name", ""))
	return ""


func _process(delta: float) -> void:
	_blink += delta
	if figure != null:
		if hero.sprite != null:
			hero.sprite.visible = false
		figure.play("walk" if hero.walking else "idle")
		figure.rotation.y = lerp_angle(
			figure.rotation.y, Motion.yaw_of(hero.dir8), 1.0 - exp(-16.0 * delta)
		)
	for a in arrows:
		a.visible = int(_blink / BLINK_TIME) % 2 == 0


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
	if (
		not near.is_empty()
		and near.kind != "way"
		and (Input.is_action_just_pressed("attack") or Input.is_action_just_pressed("ui_accept"))
	):
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
	match str(s.get("kind", "")):
		"hall":
			return InputSetup.hint("camp.enter_hall")
		"smith":
			return InputSetup.hint("camp.enter_smith")
		"store":
			return InputSetup.hint("camp.enter_store")
	return InputSetup.hint("camp.hint_walk")


func use(s: Dictionary) -> void:
	match str(s.get("kind", "")):
		"way":
			if s.open:
				_leaving = true
				Router.push(
					"campaign",
					{
						"level": 3,
						"lord": int(s.place),
						"mission": int(s.mission),
						"camp": true,
						"profile_path": path
					}
				)
		"hall":
			Router.push("town_hall", {"profile_path": path})
		"smith":
			Router.push("blacksmith", {"profile_path": path})
		"store":
			Router.push("live_warehouse", {"profile_path": path})


## The ways out of the camp, one gap each: [place, open, mission], in a shuffled order so a
## gap's side says nothing. When the hero chose the way on at the end of his last mission
## (profile.heading), the camp is that place's: a way per mission of it not won yet (each its
## general to beat; all of them when all are won). Otherwise (the start, after an ending) a way
## per place on from here, to the first mission of it not won yet; a closed place is fenced.
func choices() -> Array:
	var out: Array = []
	var to: int = int(profile.heading)
	if to > 0 and to in world_map.next_places(place) and profile.is_lord_open(to):
		var n: int = campaign.lord_missions(to).size()
		var left: Array = range(n).filter(func(i): return not profile.is_done(to, i))
		if left.is_empty():
			left = range(n)
		for m in left.slice(0, MAX_WAYS):
			out.append([to, true, m])
		_shuffle(out)
		return out
	for id in world_map.next_places(place):
		if out.size() >= MAX_WAYS:
			break
		var open: bool = profile.is_lord_open(id)
		var n: int = campaign.lord_missions(id).size()
		var m := 0
		for i in n:
			if not profile.is_done(id, i):
				m = i
				break
		out.append([id, open, m if open else -1])
	_shuffle(out)
	return out


## The place whose camp this is: the one the hero is heading for, else his own.
func camp_place() -> int:
	var to: int = int(profile.heading)
	return to if to > 0 and to in world_map.next_places(place) else place


## The land of a place, from its map: "lake", "mountains", "forest", "town" or "steppe".
static func terrain(id: int) -> String:
	return terrain_of(MapBuilder.load_map(id))


static func terrain_of(map: Dictionary) -> String:
	var n := maxi(int(map.get("w", 0)) * int(map.get("h", 0)), 1)
	var count := {"lake": 0, "mountains": 0, "forest": 0, "town": 0}
	for layer in ["ground", "upper"]:
		for t in map.get(layer, []):
			var k := int(t)
			if (k >= 73 and k <= 81) or k == 145 or k == 149:
				count.lake += 1
			elif (k >= 69 and k <= 72) or k == 101 or k == 102 or (k >= 36 and k <= 48):
				count.mountains += 1
			elif k >= 63 and k <= 68:
				count.forest += 1
			elif (k >= 146 and k <= 188) or (k >= 193 and k <= 236):
				count.town += 1
	if count.lake >= 0.08 * n:
		return "lake"
	if count.mountains >= 0.1 * n:
		return "mountains"
	if count.forest >= 0.1 * n:
		return "forest"
	if count.town >= 0.2 * n:
		return "town"
	return "steppe"


## The land past an open or closed gap: a few pictures beside the road on, outside the camp.
func _scenery(e: Dictionary, land: String) -> void:
	var out := Vector2.ZERO  # the way out of the gap
	var across := Vector2.ZERO  # along the edge
	match int(e.side):
		0:
			out = Vector2(0, -1)
			across = Vector2(1, 0)
		1:
			out = Vector2(1, 0)
			across = Vector2(0, 1)
		2:
			out = Vector2(-1, 0)
			across = Vector2(0, 1)
	# The middle of the gap's outer edge (its road is the two cells from the gap's centre on).
	var c: Vector2i = e.gap[1]
	var mid := Vector2(c.x + 0.5, c.y + 0.5)
	if int(e.side) == 0:
		mid = Vector2(c.x + 1.0, 0.0)
	elif int(e.side) == 1:
		mid = Vector2(CampMap.W, c.y + 1.0)
	else:
		mid = Vector2(0.0, c.y + 1.0)
	var at := func(ahead: float, side: float) -> Vector3:
		var p: Vector2 = mid + out * ahead + across * side
		return Vector3(p.x, 0.0, p.y)
	for piece in LAND.get(land, LAND["steppe"]):
		_land_piece(str(piece[0]), at.call(float(piece[1]), float(piece[2])), float(piece[3]))
	if land == "lake":
		_lake(at.call(3.2, 0.0) + Vector3(across.x, 0, across.y) * -2.6)
		_lake(at.call(4.2, 0.0) + Vector3(across.x, 0, across.y) * 3.0)


## A piece of the new art standing on the land past the trees (on its hills).
func _land_piece(what: String, at: Vector3, scale_by: float) -> void:
	var node: Node3D
	if what == "hut":
		node = ArtKit.prop(MapArt.CLUSTERS["hut"])
	else:
		var spec: Array = MapArt.PROP.get(what, [])
		if spec.is_empty():
			return
		node = ArtKit.prop(spec[0], false)
		scale_by *= float(spec[1].x)
	node.name = "Land%d" % world.get_child_count()
	node.scale = Vector3.ONE * scale_by
	node.rotation.y = float(hash(Vector2(at.x, at.z)) % 628) / 100.0
	node.position = Vector3(at.x, builder.hills(at.x, at.z), at.z)
	world.add_child(node)


## A pond past the trees: a disc of the maps' water on the land.
func _lake(centre: Vector3) -> void:
	var mesh := CylinderMesh.new()
	mesh.top_radius = 1.6
	mesh.bottom_radius = 1.6
	mesh.height = 0.02
	var mi := MeshInstance3D.new()
	mi.name = "Land%d" % world.get_child_count()
	mi.mesh = mesh
	var m := ShaderMaterial.new()
	m.shader = MapArt.WATER_SHADER
	mi.material_override = m
	mi.scale = Vector3(1.4, 1.0, 1.0)
	mi.position = Vector3(centre.x, builder.hills(centre.x, centre.z) + 0.03, centre.z)
	world.add_child(mi)


func _shuffle(a: Array) -> void:
	for i in range(a.size() - 1, 0, -1):
		var j := rng.randi_range(0, i)
		var t: Variant = a[i]
		a[i] = a[j]
		a[j] = t


## Straight into a mission's briefing (the first mission of a new game).
func start_mission(lord_id: int, mission: int) -> void:
	if not is_inside_tree():
		return
	var line: int = profile.next_briefing(RandomNumberGenerator.new())
	profile.save_keeping_map(path)
	_leaving = true
	Router.push(
		"briefing", {"lord": lord_id, "mission": mission, "line": line, "profile_path": path}
	)


func toggle_menu() -> void:
	menu.visible = not menu.visible
	if menu.visible:
		%GameMenu.grab_focus()


func open_game_menu() -> void:
	Router.push("game_menu", {"profile_path": path})


func open_world_map() -> void:
	Router.push("campaign", {"level": 1, "profile_path": path})


func open_main_menu() -> void:
	Router.go("main_menu")


func go_back() -> void:
	toggle_menu()


func _screen_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause"):
		get_viewport().set_input_as_handled()
		toggle_menu()
