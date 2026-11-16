extends Control
## The map generator lab: the map the generator makes for a place (MapGenerator.build), in the
## game's art seen from above, with the route of one of its missions over it (its rooms joined
## from the start, a ring on the rooms of its stops, a wider one on the last). The line at the top
## says how many rooms, soldiers and archers the mission has and its time. It shows the map of any
## seed, also one the game could not play (the line says what MapCheck finds), so that the look
## of the rules can be seen quickly on many places and seeds.
##
## Run: godot --path godot/client res://lab/map_gen_lab.tscn (in the editor: open the scene, F6).
## Keys: Left / Right the place before / after, N another seed, R the place's own seed again,
## M the route of the next mission, Esc quit. With `-- shot <file.png> <place>` it saves the
## picture of the place's map from its own seed and quits.

## How steeply the camera looks down at the map, in degrees.
const PITCH := 58.0
## How far the camera is from the map, and the fog and the shadows pushed past it.
const CAMERA_DISTANCE := 80.0
const FOG_FROM := 300.0
const FOG_TO := 400.0
const SHADOWS_TO := 250.0
## Map cells of air around the map in the picture, at the sides and at the bottom.
const AIR := Vector2(1.0, 1.5)
const ROUTE_COLOUR := Color(1.0, 0.85, 0.3, 0.9)
const ROUTE_WIDTH := 4.0
const STOP_RADIUS := 12.0
## Frames and seconds to wait for the map to be drawn before a shot.
const SHOT_FRAMES := 6
const SHOT_WAIT := 1.0

var place := 1
var map_seed := 0
var mission := 0
var plan: MapPlan
var map: Dictionary
var layout: RoomLayout

@onready var art: MapArt = $World/Viewport/Map
@onready var camera: Camera3D = $World/Viewport/Camera
@onready var light: MapLight = $World/Viewport/Light
@onready var route_line: Control = %Route
@onready var info: Label = %Info


func _ready() -> void:
	light.air.environment.fog_depth_begin = FOG_FROM
	light.air.environment.fog_depth_end = FOG_TO
	light.sun.directional_shadow_max_distance = SHADOWS_TO
	route_line.draw.connect(_draw_route)
	var args := OS.get_cmdline_user_args()
	if args.size() >= 3 and args[0] == "shot":
		show_place(int(args[2]))
		await _save(args[1])
		get_tree().quit()
		return
	show_place(place)


## The map of a place from a seed (-1: the place's own), the route of its first mission.
func show_place(place_id: int, from_seed: int = -1) -> void:
	place = wrapi(place_id, 1, MapBuilder.map_count() + 1)
	plan = MapPlan.of(place)
	map_seed = plan.seed if from_seed < 0 else from_seed
	map = MapGenerator.build(plan, map_seed)
	layout = MapGenerator.layout_of(plan, map_seed)
	mission = 0
	art.build(map)
	_fit_camera()
	_show_info()


func _fit_camera() -> void:
	var w := float(map.w)
	var h := float(map.h)
	var p := deg_to_rad(PITCH)
	var aspect := size.x / maxf(size.y, 1.0)
	camera.size = maxf((h + AIR.y) * sin(p) + AIR.y * cos(p), (w + AIR.x * 2.0) / aspect)
	camera.position = (
		Vector3(w / 2.0, 0.0, h / 2.0) + Vector3(0.0, sin(p), cos(p)) * CAMERA_DISTANCE
	)
	camera.rotation_degrees = Vector3(-PITCH, 0.0, 0.0)


func _show_info() -> void:
	var problems := MapCheck.problems(map, plan.bosses, plan.ways_on)
	var check := (
		"plays" if problems.is_empty() else "%d problems: %s" % [problems.size(), problems[0]]
	)
	info.text = (
		"Place %d (%s, depth %d), seed %d, mission %d of %d: %s. %s"
		% [
			place,
			plan.biome,
			plan.depth,
			map_seed,
			mission + 1,
			plan.missions.size(),
			_fights(),
			check
		]
	)
	route_line.queue_redraw()


## The mission's rooms, soldiers and archers, and its time.
func _fights() -> String:
	var rooms := Rooms.new(map, mission)
	var soldiers := 0
	for room: int in layout.routes[mission]:
		for wave: Array in rooms.waves(room):
			soldiers += int(wave[1]) if wave[0] == MapSim.KIND_SWORDS else 0
	var archers := 0
	for script: Dictionary in map.scripts:
		archers += script.ops.count([0, mission + 1, MapSim.KIND_ARCHERS - 200])
	return (
		"%d rooms, %d soldiers, %d archers, %d s"
		% [layout.routes[mission].size(), soldiers, archers, MapBuilder.mission_time(map, mission)]
	)


## The route of the mission over the map: its rooms joined, rings on the rooms of its stops.
func _draw_route() -> void:
	if layout == null:
		return
	var route: Array = layout.routes[mission]
	var points := PackedVector2Array()
	for room: int in route:
		var xy := layout.room_xy(room) * RoomLayout.ROOM + RoomLayout.FIRST_MIDDLE
		points.append(camera.unproject_position(Vector3(xy.x + 0.5, 0.0, xy.y + 0.5)))
	route_line.draw_polyline(points, ROUTE_COLOUR, ROUTE_WIDTH)
	for i: int in layout.stops[mission]:
		var last := i == route.size() - 1
		var radius := STOP_RADIUS * (1.5 if last else 1.0)
		route_line.draw_arc(points[i], radius, 0.0, TAU, 24, ROUTE_COLOUR, ROUTE_WIDTH)


func _save(path: String) -> void:
	for i in SHOT_FRAMES:
		await get_tree().process_frame
	await get_tree().create_timer(SHOT_WAIT).timeout
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png(path)


func _unhandled_input(event: InputEvent) -> void:
	if not (event is InputEventKey and event.pressed and not event.echo):
		return
	match (event as InputEventKey).keycode:
		KEY_LEFT:
			show_place(place - 1)
		KEY_RIGHT:
			show_place(place + 1)
		KEY_N:
			show_place(place, map_seed + 1)
		KEY_R:
			show_place(place)
		KEY_M:
			mission = (mission + 1) % plan.missions.size()
			_show_info()
		KEY_ESCAPE:
			get_tree().quit()
		_:
			return
	get_viewport().set_input_as_handled()
