class_name CampScreen
extends BaseScreen
## The stop between missions: the hero walks about the camp on the marsh, «Плавні», at dusk
## (camp_fort.gd builds it from its plan, camp_plan.gd), and the camera follows him. Each way
## on (one, two or three places, as the campaign goes) is a gate in the palisade on a side of
## the world (north, east, west, south, then north-east and north-west) with a blinking arrow;
## past the gate lies the land of that place (a lake, mountains, a forest, a town or the steppe,
## from its map: terrain()), nothing more, so which way is better is learnt by playing. Walking
## out tells the story of the next mission of that place not won yet (choices()), then its
## briefing; the mission comes back here when it is over (won: the camp of the new place; lost:
## this one again, to try once more with the same hero). A closed way's gate is barred. Every
## camp has the blacksmith (buy, sell, enchant, combine), the stores (the warehouse), the
## auctioneer (trade: buy, sell, the hero's own lots) and the town hall (every colonel and
## general, and the visits of the generals: one after each mission won,
## scripts/core/visits.gd), which the hero enters from a few steps off its door. The game is
## saved when the hero comes into a camp. Pause opens the camp menu: the game menu, the world
## map, the settings, the main menu.
## Router.params: profile_path; first: true starts the first mission at once (a new game).

const BLINK_TIME := 0.25
const MAX_WAYS := 6  # gates in a camp
const CAMERA_DISTANCE := 15.0  # it follows the hero, a good part of the camp in view
## The name over each thing to use: its spot's kind and where it hangs from the spot.
const LABELS := {
	"Smith": ["smith", Vector3(0.0, 2.4, -1.6)],
	"Store": ["store", Vector3(0.0, 2.0, -1.6)],
	"Hall": ["hall", Vector3(0.0, 3.2, -1.2)],
	"Auction": ["auction", Vector3(0.0, 2.7, -2.1)],
}
## The blinking arrow in an open gate: how high, how big.
const ARROW_HEIGHT := 0.6
const ARROW_PIXEL := 1.0 / 72.0
## The arrow picture for a way out going down (south), left, up and right.
const ARROW_DOWN := 0
const ARROW_LEFT := 1
const ARROW_UP := 2
const ARROW_RIGHT := 3

var path: String = Profile.PATH
var profile: RefCounted
var campaign := Campaign.new()
var world_map: RefCounted
var plan: CampPlan
var place := 0
## What the hero can use where he stands (CampPlan.spots()): the ways first, in the order of
## plan.exits, then the smithy, the stores, the town hall and the auctioneer.
var spots: Array[Dictionary] = []
var near := {}  # the spot in reach, or empty
var arrows: Array[Sprite3D] = []
var rng := RandomNumberGenerator.new()
var _blink := 0.0
var _leaving := false

@onready var world: Node3D = $World/Viewport/WorldRoot
@onready var fort: CampFort = $World/Viewport/WorldRoot/Fort
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
	plan = CampPlan.new(choices(), CampPlan.is_main(camp_place()))
	spots = plan.spots()
	_build_world()
	_show_place()
	if profile.on_map.is_empty():
		profile.save(path)  # the game is kept between missions, here
	if bool(Router.params.get("first", false)) and profile.done.is_empty():
		Router.params.erase("first")
		start_mission.call_deferred(1, 0)


func _build_world() -> void:
	var lands: Array = plan.exits.map(func(e: Dictionary) -> String: return terrain(e.place))
	fort.build(plan, lands, hash(camp_place()))
	var light: WorldEnvironment = world.find_children("*", "WorldEnvironment", false, false)[0]
	CampFort.dusk(light, world.get_node("Sun"))
	_place_hero()
	camera.target = hero
	camera.distance = CAMERA_DISTANCE
	camera.snap()
	for e in plan.exits:
		if e.open:
			_add_arrow(e)
	for label_name in LABELS:
		var spot := spot_of(LABELS[label_name][0])
		(get_node("%" + label_name) as Node3D).position = spot.at + LABELS[label_name][1]


## The spot of a kind ("smith", "store", "hall", "auction"; the first way for "way").
func spot_of(kind: String) -> Dictionary:
	for s in spots:
		if s.kind == kind:
			return s
	return {}


## The hero as the missions show him (the figure of his class with his blade: the body walks,
## the figure plays idle or walk and turns the way he goes), in the yard facing north.
func _place_hero() -> void:
	hero.set_look(int(profile.head), profile.weapon_kind())
	hero.global_position = CampPlan.START + Vector3(0, 0.05, 0)
	hero.dir8 = 4  # facing up, into the camp
	figure.setup(MapPeople.HEROES[clampi(int(profile.head), 0, 3)])
	figure.unequip_all()
	figure.equip(MapPeople.BLADES[clampi(profile.weapon_kind(), 0, 1)])
	figure.rotation.y = Motion.yaw_of(hero.dir8)
	figure.play("idle", 0.0)
	if hero.sprite != null:
		hero.sprite.visible = false


## The blinking arrow in an open gate, pointing the way out; nothing says where it leads.
func _add_arrow(e: Dictionary) -> void:
	var arrow := Sprite3D.new()
	arrow.name = "Arrow%d_%d" % [e.place, e.mission]
	arrow.texture = MissionScreen.exit_arrow(arrow_side(e.out))
	arrow.pixel_size = ARROW_PIXEL
	arrow.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	arrow.no_depth_test = true
	var at: Vector3 = e.gate.lerp(e.inside, 0.5)
	arrow.position = at + Vector3(0, ARROW_HEIGHT, 0)
	world.add_child(arrow)
	arrows.append(arrow)


## The arrow picture (MissionScreen.exit_arrow) for a way out going `out` on the ground.
static func arrow_side(out: Vector3) -> int:
	if absf(out.z) >= absf(out.x):
		return ARROW_UP if out.z < 0.0 else ARROW_DOWN
	return ARROW_RIGHT if out.x > 0.0 else ARROW_LEFT


func _show_place() -> void:
	var kind := tr("camp.main") if plan.main else tr("camp.stop")
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


## The nearest spot whose range reaches a position, or empty.
func spot_near(pos: Vector3) -> Dictionary:
	return CampPlan.spot_near(spots, pos)


## The open way whose gate the position has walked out of, or empty.
func exit_crossed(pos: Vector3) -> Dictionary:
	var i := plan.exit_crossed(pos)
	return {} if i < 0 else spots[i]


func _hint_text(s: Dictionary) -> String:
	match str(s.get("kind", "")):
		"hall":
			return InputSetup.hint("camp.enter_hall")
		"smith":
			return InputSetup.hint("camp.enter_smith")
		"store":
			return InputSetup.hint("camp.enter_store")
		"auction":
			return InputSetup.hint("camp.enter_auction")
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
		"auction":
			Router.push("live_trade", {"profile_path": path})


## The ways out of the camp, one gate each: [place, open, mission], in a shuffled order so a
## gate's side says nothing. When the hero chose the way on at the end of his last mission
## (profile.heading), the camp is that place's: a way per mission of it not won yet (each its
## general to beat; all of them when all are won). Otherwise (the start, after an ending) a way
## per place on from here, to the first mission of it not won yet; a closed place is barred.
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


func open_settings() -> void:
	Router.push("settings")


func open_main_menu() -> void:
	Router.go("main_menu")


func go_back() -> void:
	toggle_menu()


func _screen_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause"):
		get_viewport().set_input_as_handled()
		toggle_menu()
