extends Node3D
## The field of a multiplayer battle in the new art: the steppe ground of the maps with a
## trodden strip where the fighters stand, and behind it one of four sceneries made of the
## maps' things, after the battle's background byte (bits 0-1 the scenery, 4-5 the ground,
## 6-7 day or night):
##   0 a Sich camp: a palisade with a gate between two banners, a marquee behind it; tents, a
##     cannon, barrels, a spear rack and a fireplace inside;
##   1 a village: two huts, wattle fences, a well sweep, haystacks, poplars and an oak;
##   2 a road among rocks: big rocks on both sides, oaks, a poplar and bushes, the road
##     winding away;
##   3 a forest edge: rows of firs and oaks, bushes and stumps.
## The ground is a green meadow, lush dark grass, dry steppe or red trodden earth. The light
## is the maps' (a warm sun with soft shadows, a cool shade) or a cold moon, and far away the
## land fades into the colour of the sky's horizon. The sky itself is painted behind the 3D
## view (sky_settings(): assets/art/shaders/story_sky.gdshader).

const ArtKit := preload("res://scripts/art/art_kit.gd")
const ArtGround := preload("res://scripts/art/art_ground.gd")

## The flat part of the ground: the fighters, the scenery and the camera's view of it.
const PLAY := Rect2(-18, -9, 36, 21)
const DAY := {"top": Color("4a6896"), "horizon": Color("e3d2aa"), "horizon_y": 0.34,
	"glow": Color("f6e4b4"), "glow_size": 0.5, "sun": Vector2(0.18, 0.06), "sun_size": 0.0,
	"sun_colour": Color("fff0c8"), "clouds": 0.42, "cloud_dark": Color("8f97ab"),
	"cloud_lit": Color("fbf1dc"), "stars": 0.0, "bolt": -1.0, "seed": 3.0}
const NIGHT := {"top": Color("0c1222"), "horizon": Color("2c3854"), "horizon_y": 0.34,
	"glow": Color("5a6a90"), "glow_size": 0.3, "sun": Vector2(0.78, 0.1), "sun_size": 0.035,
	"sun_colour": Color("ece6cf"), "clouds": 0.25, "cloud_dark": Color("1a2238"),
	"cloud_lit": Color("6a7898"), "stars": 1.0, "bolt": -1.0, "seed": 7.0}
## The ground's colours by its kind: [soil, dry grass, green grass], and how green it is.
const GROUNDS := [
	[Color("c9a15b"), Color("9e9a5c"), Color("6f8a4a"), 1.0],  # a green meadow
	[Color("8f7448"), Color("6f7a48"), Color("4d6a36"), 1.4],  # lush dark grass
	[Color("c9a15b"), Color("aaa067"), Color("8a8a4e"), 0.0],  # dry steppe
	[Color("a0704a"), Color("8f7d50"), Color("6f7a44"), 0.4],  # red trodden earth
]

var scenery := -1
var ground_kind := -1
var night := false
var ground: Node3D  # an ArtGround
var sun: DirectionalLight3D
var env: Environment
var _things: Node3D


func _init() -> void:
	sun = DirectionalLight3D.new()
	sun.name = "Sun"
	sun.shadow_enabled = true
	sun.directional_shadow_mode = DirectionalLight3D.SHADOW_ORTHOGONAL
	sun.directional_shadow_max_distance = 40.0
	sun.shadow_blur = 1.5
	add_child(sun)
	env = Environment.new()
	env.background_mode = Environment.BG_CLEAR_COLOR
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	env.fog_enabled = true
	env.fog_mode = Environment.FOG_MODE_DEPTH
	env.fog_density = 1.0
	env.fog_depth_begin = 16.0
	env.fog_depth_end = 44.0
	env.fog_sky_affect = 0.0
	var we := WorldEnvironment.new()
	we.environment = env
	add_child(we)


static func scenery_of(bg: int) -> int:
	return bg & 3


static func ground_of(bg: int) -> int:
	return (bg >> 4) & 3


static func is_night(bg: int) -> bool:
	return (bg >> 6) & 3 == 1


## Builds the field for a background byte (again only when it changes).
func build(bg: int) -> void:
	if scenery == scenery_of(bg) and ground_kind == ground_of(bg) and night == is_night(bg):
		return
	scenery = scenery_of(bg)
	ground_kind = ground_of(bg)
	night = is_night(bg)
	if _things != null:
		_things.free()
	_things = Node3D.new()
	_things.name = "Field"
	add_child(_things)
	_light()
	_ground()
	call(["_sich", "_village", "_road", "_forest"][scenery])


## The sky's settings for story_sky.gdshader.
func sky_settings() -> Dictionary:
	return NIGHT if night else DAY


func _light() -> void:
	var sky := sky_settings()
	if night:
		sun.light_color = Color("aab8e0")
		sun.light_energy = 0.32
		env.ambient_light_color = Color("44507a")
		env.ambient_light_energy = 0.55
	else:
		sun.light_color = Color("ffe6c0")
		sun.light_energy = 0.62
		env.ambient_light_color = Color("9aa2c0")
		env.ambient_light_energy = 0.42
	sun.transform = Transform3D(Basis.looking_at(Vector3(0.5, -0.7, -0.5).normalized(), Vector3.UP), Vector3.ZERO)
	env.fog_light_color = sky.horizon


func _ground() -> void:
	ground = ArtGround.new()
	ground.play = PLAY
	ground.tufts = 420
	ground.seed_value = 5 + scenery
	var colours: Array = GROUNDS[ground_kind]
	var green: float = colours[3]
	if green > 0.0:
		ground.greens = [Vector3(-9, -4, 6.0 * green), Vector3(8, -5, 7.0 * green), Vector3(-2, 6, 5.0 * green),
			Vector3(12, 4, 6.0 * green), Vector3(-14, 3, 5.0 * green)]
	# the strip trodden by the fighters; the road of scenery 2 winds away from it
	ground.paths = [PackedVector2Array([Vector2(-9.5, 0.1), Vector2(9.5, -0.1)])]
	ground.path_width = 2.6 if ground_kind == 3 else 1.8
	if scenery == 2:
		ground.paths.append(PackedVector2Array([Vector2(0.4, 0.0), Vector2(1.6, -5.0), Vector2(0.2, -10.0),
			Vector2(2.5, -16.0), Vector2(1.0, -24.0)]))
	_things.add_child(ground)
	ground.build()
	var m := (ground.get_node("Ground") as MeshInstance3D).material_override as ShaderMaterial
	m.set_shader_parameter("soil", colours[0])
	m.set_shader_parameter("grass_dry", colours[1])
	m.set_shader_parameter("grass_green", colours[2])


## A thing of the maps standing on the ground at (x, z).
func _put(prop: String, x: float, z: float, yaw := 0.0, scale_by := 1.0) -> Node3D:
	var node := ArtKit.prop(prop, false)
	node.position = Vector3(x, ground.height(x, z), z)
	node.rotation_degrees.y = yaw
	node.scale = Vector3.ONE * scale_by
	_things.add_child(node)
	return node


func _sich() -> void:
	for i in 17:
		var x := -16.0 + i * 2.0
		if absf(x) < 1.5:
			continue  # the gate
		_put("palisade", x, -11.0 - 0.15 * sin(i * 1.7), 0.0, 0.9)
	_put("banner", -1.7, -10.6)
	_put("banner", 1.7, -10.6)
	_put("shatro", -7.5, -14.5, 20.0)
	_put("namet", 7.0, -8.2, 65.0)
	_put("namet", -11.5, -7.6, 115.0, 0.9)
	_put("harmata", -6.2, -6.4, 30.0)
	_put("stoiak", 3.6, -8.8)
	_put("bochka", 9.6, -6.0)
	_put("bochka", 10.3, -6.5, 40.0)
	_put("drova", -3.8, -8.6, -20.0)
	_put("vohnyshche", 11.8, -8.6)
	_put("topolia", -15.0, -15.5, 0.0, 1.1)
	_put("topolia", 14.5, -16.0, 0.0, 1.2)


func _village() -> void:
	_put("khata", -7.5, -11.5, 15.0)
	_put("khata", 7.0, -13.0, -20.0)
	for i in 5:
		_put("tyn", -12.0 + i * 2.1, -7.6 + 0.12 * sin(i * 2.3), 0.0)
		_put("tyn", 3.6 + i * 2.1, -7.8 + 0.12 * cos(i * 1.9), 0.0)
	_put("zhuravel", 2.3, -10.0, 70.0)
	_put("stih", 11.2, -9.2, 10.0)
	_put("stih", -12.5, -9.6, -20.0, 0.9)
	_put("topolia", -2.5, -14.5, 0.0, 1.15)
	_put("topolia", 12.8, -14.2, 0.0, 1.05)
	_put("topolia", -14.8, -13.0, 0.0, 1.2)
	_put("dub", -16.0, -6.5, 30.0, 1.1)
	_put("kushch", 9.0, -6.6, 15.0)
	_put("bochka", -4.0, -6.8)


func _road() -> void:
	_put("skelia", -9.0, -10.5, 20.0, 2.6)
	_put("skelia", -11.8, -7.4, 110.0, 1.7)
	_put("skelia", -6.4, -12.8, 200.0, 2.0)
	_put("skelia", 9.6, -11.0, -30.0, 3.0)
	_put("skelia", 12.4, -7.8, 60.0, 1.8)
	_put("skelia", 6.8, -13.5, 140.0, 1.6)
	_put("dub", -3.8, -14.0, 10.0, 1.1)
	_put("dub", 14.8, -12.5, -40.0, 1.0)
	_put("topolia", 4.6, -15.5, 0.0, 1.1)
	_put("kushch", -6.6, -6.4, 0.0, 1.2)
	_put("kushch", 6.6, -6.0, 50.0)
	_put("kushch", 3.4, -8.6, 120.0, 0.8)
	_put("penok", -8.2, -4.6, 0.0)
	_put("yalyna", -15.0, -10.0, 0.0, 1.2)


func _forest() -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 11
	for row in 3:
		var z := -12.0 - row * 3.0
		var x := -20.0 + row * 1.3
		while x < 20.0:
			var tree := "dub" if rng.randf() < 0.2 else "yalyna"
			_put(tree, x + rng.randf_range(-0.6, 0.6), z + rng.randf_range(-0.8, 0.8), rng.randf() * 360.0,
				rng.randf_range(0.85, 1.2) if tree == "yalyna" else rng.randf_range(0.7, 0.9))
			x += rng.randf_range(2.6, 3.6)
	for x in [-11.0, -6.2, 5.4, 10.6]:
		_put("kushch", x, -8.0 + rng.randf_range(-0.6, 0.6), rng.randf() * 360.0, rng.randf_range(0.9, 1.3))
	_put("yalyna", -9.0, -9.5, 20.0, 0.75)
	_put("yalyna", 8.2, -10.0, 70.0, 0.7)
	_put("penok", -8.6, -5.2)
	_put("penok", 8.0, -5.6, 40.0)
	_put("skelia", 12.6, -7.4, 30.0, 1.2)
