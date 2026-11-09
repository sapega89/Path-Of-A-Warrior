extends Node
## Paints the story pictures of the new art (needs a display, not --headless):
##   godot --path godot/client --resolution 1040x800 res://tools/story_pictures.tscn [-- 2 5 ...]
## Each of the 15 pictures is a small scene of the maps' people and things (the painted shader
## with the ink outline) under a painted sky (assets/art/shaders/story_sky.gdshader), with rain,
## dark corners and grain over it (story_overlay.gdshader), graded as the game (ArtKit.GRADE:
## muted and harder), saved as assets/art/story/e<n>.png.
## The numbers after -- paint only those pictures.

const ArtKit := preload("res://scripts/art/art_kit.gd")
const ArtFigure := preload("res://scripts/art/art_figure.gd")
const ArtGround := preload("res://scripts/art/art_ground.gd")
const ArtEffects := preload("res://scripts/art/art_effects.gd")
const DIR := "res://assets/art/story/"
const SIZE := Vector2i(1040, 800)  # painted at, then made smaller
const OUT := Vector2i(520, 400)
const PICTURES := 15
const EARTH := Color("7a5a3a")
const GRASS := Color("5f6a3c")
const WOOD := Color("4a3324")
## The sky's settings before a picture changes them.
const SKY := {
	"top": Color("33405f"),
	"horizon": Color("d9b98a"),
	"horizon_y": 0.6,
	"glow": Color("f2cc8a"),
	"glow_size": 0.35,
	"sun": Vector2(0.7, 0.5),
	"sun_size": 0.0,
	"sun_colour": Color("ffe6a0"),
	"clouds": 0.4,
	"cloud_dark": Color("4a4a60"),
	"cloud_lit": Color("f0d8b0"),
	"stars": 0.0,
	"bolt": -1.0,
	"seed": 0.0
}

var view: SubViewport  # the scene, on a clear background
var canvas: SubViewport  # the sky, the scene and what lies over it
var sky: ShaderMaterial
var overlay: ShaderMaterial
var env: Environment
var sun: DirectionalLight3D
var camera: Camera3D
var world: Node3D  # the scene of the picture being painted


func _ready() -> void:
	var only := OS.get_cmdline_user_args()
	_stage()
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(DIR))
	for n in range(1, PICTURES + 1):
		if not only.is_empty() and not (str(n) in only):
			continue
		world = Node3D.new()
		view.add_child(world)
		_reset()
		call("_e%d" % n)
		await _frames(8)
		await RenderingServer.frame_post_draw
		var img := canvas.get_texture().get_image()
		img.adjust_bcs(ArtKit.GRADE.x, ArtKit.GRADE.y, ArtKit.GRADE.z)  # the game's grade, sky and all
		img.resize(OUT.x, OUT.y, Image.INTERPOLATE_LANCZOS)
		img.save_png(ProjectSettings.globalize_path(DIR + "e%d.png" % n))
		print("picture ", n)
		world.free()
	get_tree().quit()


func _stage() -> void:
	view = SubViewport.new()
	view.size = SIZE
	view.own_world_3d = true
	view.transparent_bg = true
	view.msaa_3d = Viewport.MSAA_8X
	view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	add_child(view)
	env = Environment.new()
	env.background_mode = Environment.BG_CLEAR_COLOR
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	env.fog_enabled = true
	env.fog_mode = Environment.FOG_MODE_DEPTH
	env.fog_density = 1.0
	env.fog_sky_affect = 0.0
	var we := WorldEnvironment.new()
	we.environment = env
	view.add_child(we)
	sun = DirectionalLight3D.new()
	sun.shadow_enabled = true
	sun.directional_shadow_mode = DirectionalLight3D.SHADOW_ORTHOGONAL
	sun.directional_shadow_max_distance = 40.0
	sun.shadow_blur = 1.5
	view.add_child(sun)
	camera = Camera3D.new()
	view.add_child(camera)

	canvas = SubViewport.new()
	canvas.size = SIZE
	canvas.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	add_child(canvas)
	sky = _layer(preload("res://assets/art/shaders/story_sky.gdshader"))
	var scene := TextureRect.new()
	scene.texture = view.get_texture()
	scene.size = Vector2(SIZE)
	canvas.add_child(scene)
	overlay = _layer(preload("res://assets/art/shaders/story_overlay.gdshader"))


func _layer(shader: Shader) -> ShaderMaterial:
	var rect := ColorRect.new()
	rect.size = Vector2(SIZE)
	var m := ShaderMaterial.new()
	m.shader = shader
	m.set_shader_parameter("aspect", float(SIZE.x) / SIZE.y)
	rect.material = m
	canvas.add_child(rect)
	return m


func _reset() -> void:
	for key in SKY:
		sky.set_shader_parameter(key, SKY[key])
	overlay.set_shader_parameter("rain", 0.0)
	overlay.set_shader_parameter("vignette", 0.5)
	_light(Vector3(-0.5, -0.6, -0.6), Color("ffe6c0"), 1.0, Color("9aa2c0"), 0.45)
	_fog(Color("d9b98a"), 14.0, 50.0)


## The sky: any of SKY's settings.
func _sky(settings: Dictionary) -> void:
	for key in settings:
		sky.set_shader_parameter(key, settings[key])


## The sun (the way its light goes) and the light of the air.
func _light(towards: Vector3, colour: Color, energy: float, air: Color, air_energy: float) -> void:
	sun.transform = Transform3D(Basis.looking_at(towards.normalized(), Vector3.UP), Vector3.ZERO)
	sun.light_color = colour
	sun.light_energy = energy
	env.ambient_light_color = air
	env.ambient_light_energy = air_energy


func _fog(colour: Color, begin: float, end: float) -> void:
	env.fog_light_color = colour
	env.fog_depth_begin = begin
	env.fog_depth_end = end


func _look(from: Vector3, at: Vector3, fov: float) -> void:
	camera.fov = fov
	camera.look_at_from_position(from, at, Vector3.UP)


## The steppe: flat in play, rising into hills round it; greens are Vector3(x, z, radius).
func _ground(play: Rect2, greens: Array = [], paths: Array = [], colours: Dictionary = {}) -> void:
	var g: Node3D = ArtGround.new()
	g.play = play
	g.greens = greens
	g.paths = paths
	g.tufts = 220
	world.add_child(g)
	g.build()
	var m := (g.get_node("Ground") as MeshInstance3D).material_override as ShaderMaterial
	for key in colours:
		m.set_shader_parameter(key, colours[key])


func _prop(
	prop_name: String, at: Vector3, yaw := 0.0, tilt := Vector3.ZERO, scale_by := 1.0
) -> Node3D:
	var node := ArtKit.prop(prop_name, true)
	node.position = at
	node.rotation_degrees = Vector3(tilt.x, yaw, tilt.z)
	node.scale = Vector3.ONE * scale_by
	world.add_child(node)
	return node


## A person in a clip, held at a part of it (0 its start, 1 its end), facing a point.
func _person(kind: String, at: Vector3, face_to: Vector3, clip := "idle", part := 0.3) -> Node3D:
	var f: Node3D = ArtFigure.new()
	world.add_child(f)
	f.setup(kind)
	f.position = at
	f.face(face_to - at)
	var length: float = f.player.get_animation(clip).length if f.player.has_animation(clip) else 1.0
	f.pose(clip, length * part)
	return f


## A plain shape in one colour, with the ink outline.
func _shape(
	mesh: PrimitiveMesh, at: Vector3, colour: Color, rot := Vector3.ZERO, scale_by := Vector3.ONE
) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	mi.mesh = mesh
	var m := ArtKit.painted(true)
	m.set_shader_parameter("tint", colour)
	mi.material_override = m
	mi.position = at
	mi.rotation_degrees = rot
	mi.scale = scale_by
	world.add_child(mi)
	return mi


## A wooden grave cross, leaning a little.
func _cross(at: Vector3, lean := 0.0, yaw := 0.0, tall := 1.5) -> void:
	var root := Node3D.new()
	root.position = at
	root.rotation_degrees = Vector3(0, yaw, lean)
	world.add_child(root)
	var post := BoxMesh.new()
	post.size = Vector3(0.11, tall, 0.09)
	var arm := BoxMesh.new()
	arm.size = Vector3(tall * 0.5, 0.1, 0.09)
	for part in [[post, Vector3(0, tall * 0.5 - 0.15, 0)], [arm, Vector3(0, tall * 0.72, 0)]]:
		var mi := _shape(part[0], Vector3.ZERO, WOOD)
		world.remove_child(mi)
		root.add_child(mi)
		mi.position = part[1]


## A mound of earth (a grave, a hill).
func _mound(at: Vector3, radius: float, height: float, colour := EARTH) -> void:
	var s := SphereMesh.new()
	s.radius = 1.0
	s.height = 2.0
	s.radial_segments = 24
	s.rings = 12
	_shape(s, at, colour, Vector3.ZERO, Vector3(radius, height, radius * 0.8))


## A blade from characters/weapons.glb stuck point down in the ground.
func _stuck(weapon: String, at: Vector3, lean := 10.0, yaw := 0.0) -> void:
	var source: Node = ArtKit.scene("characters/weapons.glb").instantiate()
	var mesh := source.find_child(weapon, true, false) as MeshInstance3D
	var box := mesh.mesh.get_aabb()
	var mi := MeshInstance3D.new()
	mi.mesh = mesh.mesh
	mi.material_override = ArtKit.painted(true)
	# the blade lies along the mesh's Z, its point at the far end: Z to down, the point in the ground
	var tip := Vector3(box.get_center().x, box.get_center().y, box.end.z - 0.18)
	var turn := (
		Basis(Vector3.UP, deg_to_rad(yaw))
		* Basis(Vector3.BACK, deg_to_rad(lean))
		* Basis(Vector3.RIGHT, PI / 2.0)
	)
	mi.transform = Transform3D(turn, at) * Transform3D(Basis(), -tip)
	world.add_child(mi)
	source.free()


## A gold cup in a person's right hand.
func _cup(person: Node3D) -> void:
	var attach := BoneAttachment3D.new()
	attach.bone_name = "handslot.r"
	person.skeleton.add_child(attach)
	var cup := CylinderMesh.new()
	cup.top_radius = 0.055
	cup.bottom_radius = 0.035
	cup.height = 0.12
	var mi := _shape(cup, Vector3.ZERO, ArtKit.color("gold"))
	world.remove_child(mi)
	attach.add_child(mi)


## A campfire burning, its flames dimmer than by day so that they do not burn white in the dark.
func _fire(at: Vector3) -> void:
	_prop("vohnyshche", at)
	var fire := ArtEffects.campfire(world, at)
	for p in fire.find_children("*", "CPUParticles3D", true, false):
		var particles := p as CPUParticles3D
		particles.preprocess = 3.0
		if particles.mesh is QuadMesh:
			particles.amount = 12
			((particles.mesh as QuadMesh).material as StandardMaterial3D).albedo_color = Color(
				0.62, 0.5, 0.42
			)


func _frames(n: int) -> void:
	for i in n:
		await get_tree().process_frame


# -- the pictures -------------------------------------------------------------------------


## 1. Peace: a village in the gold of the afternoon, Cossacks at home.
func _e1() -> void:
	_sky(
		{
			"top": Color("5f86b4"),
			"horizon": Color("f0d8a0"),
			"glow": Color("f8d890"),
			"glow_size": 0.45,
			"sun": Vector2(0.88, 0.32),
			"clouds": 0.35,
			"cloud_dark": Color("b4a28c"),
			"cloud_lit": Color("fff2d6"),
			"seed": 1.0
		}
	)
	_light(Vector3(-0.55, -0.55, -0.6), Color("ffe2b0"), 1.05, Color("9aa6c8"), 0.45)
	_fog(Color("e8d2a2"), 16.0, 48.0)
	_ground(
		Rect2(-16, -18, 32, 30),
		[Vector3(-4, -2, 4.0), Vector3(5, -7, 5.0), Vector3(-7, -12, 5.0)],
		[PackedVector2Array([Vector2(0.5, 8), Vector2(0.2, 0), Vector2(-1.5, -6)])]
	)
	_prop("khata", Vector3(-4.2, 0, -7.0), 18.0)
	_prop("zhuravel", Vector3(4.2, 0, -5.5), -30.0)
	_prop("tyn", Vector3(-1.4, 0, -3.6), 8.0)
	_prop("tyn", Vector3(-3.5, 0, -3.3), -4.0)
	_prop("stih", Vector3(7.5, 0, -11.0))
	_prop("topolia", Vector3(-9.0, 0, -12.0))
	_prop("topolia", Vector3(10.5, 0, -14.0))
	_prop("dub", Vector3(-11.0, 0, -5.0), 40.0)
	_prop("kushch", Vector3(3.0, 0, -1.6))
	_person("kozak_svyta", Vector3(-2.2, 0, -2.5), Vector3(0.4, 0, 6), "sit", 0.4)
	var a := _person("kozak", Vector3(0.9, 0, -1.6), Vector3(2.0, 0, -1.0), "idle", 0.2)
	a.unequip_all()
	_person("kozak_camp", Vector3(1.9, 0, -1.2), Vector3(0.9, 0, -1.8), "idle", 0.6)
	_person("divchyna", Vector3(3.9, 0, -4.4), Vector3(4.2, 0, -5.5), "interact", 0.5)
	_look(Vector3(0.4, 1.5, 6.0), Vector3(0.0, 1.3, -2.5), 42.0)


## 2. The storm: three men on the road under lightning and rain.
func _e2() -> void:
	_sky(
		{
			"top": Color("1c1830"),
			"horizon": Color("6e5482"),
			"glow": Color("9c88cc"),
			"glow_size": 0.3,
			"sun": Vector2(0.3, 0.25),
			"clouds": 0.78,
			"cloud_dark": Color("27223c"),
			"cloud_lit": Color("8e80b6"),
			"bolt": 0.27,
			"seed": 4.0,
			"horizon_y": 0.66
		}
	)
	_light(Vector3(0.35, -0.55, -0.75), Color("bcb2e6"), 0.75, Color("625c8c"), 0.5)
	_fog(Color("4c3e66"), 8.0, 36.0)
	overlay.set_shader_parameter("rain", 1.0)
	overlay.set_shader_parameter("vignette", 0.65)
	_ground(
		Rect2(-14, -24, 28, 32),
		[],
		[PackedVector2Array([Vector2(0, 8), Vector2(0.6, -6), Vector2(-1, -20)])],
		{"soil": Color("8a7a66"), "grass_dry": Color("6c6a58")}
	)
	_prop("yalyna", Vector3(-5.5, 0, -7.0))
	_prop("yalyna", Vector3(5.0, 0, -11.0), 30.0)
	_prop("kamin", Vector3(3.2, 0, -2.0), 60.0)
	_person("kozak_camp", Vector3(0.1, 0, 0.0), Vector3(0.2, 0, 6), "walk", 0.1)
	_person("kozak_svyta", Vector3(-1.25, 0, -1.1), Vector3(-1.0, 0, 6), "walk", 0.55)
	_person("kozak", Vector3(1.3, 0, -0.9), Vector3(1.0, 0, 6), "walk", 0.8)
	_look(Vector3(0.2, 0.85, 5.6), Vector3(0.0, 1.5, -2.0), 40.0)


## 3. The regiment: a colonel on a rise before his army, the sun behind them.
func _e3() -> void:
	_sky(
		{
			"top": Color("394866"),
			"horizon": Color("eab274"),
			"glow": Color("f6c67a"),
			"glow_size": 0.5,
			"sun": Vector2(0.52, 0.52),
			"sun_size": 0.0,
			"clouds": 0.55,
			"cloud_dark": Color("4a4660"),
			"cloud_lit": Color("f8c890"),
			"seed": 7.0,
			"horizon_y": 0.64
		}
	)
	_light(Vector3(0.15, -0.45, 0.88), Color("ffd8a0"), 1.0, Color("8a8cac"), 0.55)
	_fog(Color("d8a878"), 10.0, 40.0)
	_ground(Rect2(-18, -24, 36, 30), [Vector3(-3, -6, 6.0), Vector3(6, -10, 6.0)])
	_person("polkovnyk", Vector3(0, 0, 1.1), Vector3(0.6, 0, 6), "cheer", 0.42)
	var kinds := [
		"serdiuk", "kozak", "kozak_camp", "zholner", "kozak_rival", "luchnyk", "kozak_svyta"
	]
	var i := 0
	for row in 4:
		for col in 8:
			var x := -6.3 + col * 1.8 + (row % 2) * 0.9 + randf_range(-0.2, 0.2)
			var z := -2.6 - row * 1.7
			_person(
				kinds[i % kinds.size()], Vector3(x, 0, z), Vector3(x * 0.6, 0, 8), "idle", randf()
			)
			i += 1
	_prop("banner", Vector3(-3.4, 0, -4.4), 20.0)
	_prop("banner", Vector3(2.9, 0, -5.4), -10.0)
	_prop("banner", Vector3(7.2, 0, -7.6), 15.0)
	_look(Vector3(0.6, 0.75, 7.2), Vector3(0.0, 2.0, -2.0), 44.0)


## 4. A road of his own: a lone Cossack walking away into the mist.
func _e4() -> void:
	_sky(
		{
			"top": Color("8790a6"),
			"horizon": Color("dcd6c8"),
			"glow": Color("fff6e0"),
			"glow_size": 0.55,
			"sun": Vector2(0.56, 0.42),
			"clouds": 0.3,
			"cloud_dark": Color("a7a8b4"),
			"cloud_lit": Color("f2eee4"),
			"seed": 11.0,
			"horizon_y": 0.56
		}
	)
	_light(Vector3(0.25, -0.6, -0.75), Color("f4ecdc"), 0.7, Color("b0b4c4"), 0.6)
	_fog(Color("d4d0c4"), 3.0, 24.0)
	overlay.set_shader_parameter("vignette", 0.35)
	_ground(
		Rect2(-14, -30, 28, 36),
		[Vector3(-4, -6, 4.0), Vector3(4, -12, 5.0)],
		[
			PackedVector2Array(
				[
					Vector2(0, 8),
					Vector2(0.4, 0),
					Vector2(1.6, -8),
					Vector2(-1.5, -18),
					Vector2(0, -28)
				]
			)
		]
	)
	_prop("yalyna", Vector3(-4.8, 0, -5.5))
	_prop("yalyna", Vector3(-6.5, 0, -9.0), 40.0, Vector3.ZERO, 1.2)
	_prop("yalyna", Vector3(4.6, 0, -9.5), 20.0, Vector3.ZERO, 1.1)
	_prop("yalyna", Vector3(-3.2, 0, -15.0))
	_prop("dub", Vector3(7.0, 0, -4.0), 10.0)
	_prop("kamin", Vector3(2.4, 0, -0.5), 100.0, Vector3.ZERO, 0.7)
	_prop("kushch", Vector3(-2.4, 0, 0.3))
	_person("kozak", Vector3(0.45, 0, -2.4), Vector3(1.4, 0, -10), "walk", 0.3)
	_look(Vector3(-0.2, 1.75, 5.2), Vector3(0.6, 1.0, -6.0), 40.0)


## 5. The grave of a fine man: a cross, a sabre in the ground, the sun going down.
func _e5() -> void:
	_sky(
		{
			"top": Color("3a2236"),
			"horizon": Color("f08a3a"),
			"glow": Color("ff9a40"),
			"glow_size": 0.5,
			"sun": Vector2(0.3, 0.5),
			"sun_size": 0.07,
			"sun_colour": Color("ffd46a"),
			"clouds": 0.45,
			"cloud_dark": Color("4a2530"),
			"cloud_lit": Color("ff9c56"),
			"seed": 13.0,
			"horizon_y": 0.62
		}
	)
	_light(Vector3(0.4, -0.3, 0.86), Color("ffb070"), 1.1, Color("6c4260"), 0.55)
	_fog(Color("e07a42"), 12.0, 40.0)
	_ground(
		Rect2(-14, -22, 28, 28),
		[Vector3(-3, -4, 4.0)],
		[],
		{"soil": Color("a87a52"), "grass_dry": Color("8a7048")}
	)
	_mound(Vector3(0.1, -0.2, -1.3), 1.4, 0.55, EARTH)
	_cross(Vector3(0.35, 0.25, -1.9), -5.0, 15.0, 1.6)
	_stuck("sabre", Vector3(0.95, 0.05, -0.55), -12.0, 20.0)
	_prop("kushch", Vector3(2.9, 0, -3.4))
	_prop("penok", Vector3(-2.4, 0, -2.6))
	_prop("topolia", Vector3(7.0, 0, -12.0))
	_look(Vector3(0.6, 0.8, 3.6), Vector3(0.1, 1.05, -1.6), 38.0)


## 6. Alone at sundown: where is the colonel I was born to serve?
func _e6() -> void:
	_sky(
		{
			"top": Color("2b2440"),
			"horizon": Color("ea6c4a"),
			"glow": Color("ec744c"),
			"glow_size": 0.45,
			"sun": Vector2(0.24, 0.6),
			"sun_size": 0.05,
			"sun_colour": Color("ffb878"),
			"clouds": 0.5,
			"cloud_dark": Color("3a2a44"),
			"cloud_lit": Color("f28c64"),
			"seed": 17.0,
			"horizon_y": 0.66
		}
	)
	_light(Vector3(0.62, -0.25, 0.75), Color("ffa070"), 1.0, Color("5c4262"), 0.5)
	_fog(Color("d26c52"), 12.0, 44.0)
	_ground(
		Rect2(-14, -22, 28, 28), [], [], {"soil": Color("9a6e50"), "grass_dry": Color("7c6448")}
	)
	_person("kharakternyk", Vector3(0.8, 0, -1.0), Vector3(-4, 0, -6), "idle", 0.5)
	_prop("penok", Vector3(-1.6, 0, 0.6))
	_look(Vector3(-0.6, 0.45, 5.0), Vector3(0.5, 1.6, -1.0), 36.0)


## 7. Marusia: the hero and the girl by her house in the evening.
func _e7() -> void:
	_sky(
		{
			"top": Color("34406a"),
			"horizon": Color("f2ba7a"),
			"glow": Color("ffcc8c"),
			"glow_size": 0.4,
			"sun": Vector2(0.12, 0.52),
			"clouds": 0.3,
			"cloud_dark": Color("6a5a78"),
			"cloud_lit": Color("ffd2a2"),
			"stars": 0.15,
			"seed": 19.0
		}
	)
	_light(Vector3(0.75, -0.35, -0.55), Color("ffc890"), 1.0, Color("7c84ac"), 0.45)
	_fog(Color("e2ae7c"), 12.0, 42.0)
	_ground(Rect2(-14, -20, 28, 28), [Vector3(-3, -3, 4.0), Vector3(4, -2, 3.0)])
	_prop("khata", Vector3(2.8, 0, -5.4), -22.0)
	_prop("tyn", Vector3(-1.8, 0, -2.8), 10.0)
	_prop("tyn", Vector3(-3.9, 0, -2.5), -6.0)
	_prop("dub", Vector3(-5.5, 0, -7.5), 30.0)
	_prop("stih", Vector3(-8.0, 0, -12.0))
	var hero := _person("kozak", Vector3(-0.42, 0, 0), Vector3(1, 0, 0.15), "idle", 0.3)
	hero.unequip_all()
	_person("divchyna", Vector3(0.42, 0, 0.05), Vector3(-1, 0, 0.2), "idle_unarmed", 0.5)
	_look(Vector3(0.1, 1.45, 4.0), Vector3(0.0, 1.2, 0.0), 38.0)


## 8. After the battle: a fallen banner, a gun on its side, the dead and the ravens' sky.
func _e8() -> void:
	_sky(
		{
			"top": Color("28283a"),
			"horizon": Color("b27250"),
			"glow": Color("c48462"),
			"glow_size": 0.4,
			"sun": Vector2(0.62, 0.6),
			"clouds": 0.66,
			"cloud_dark": Color("2c2834"),
			"cloud_lit": Color("b48c72"),
			"seed": 23.0,
			"horizon_y": 0.62
		}
	)
	_light(Vector3(-0.4, -0.45, 0.8), Color("e8b08a"), 0.85, Color("6a6478"), 0.5)
	_fog(Color("8c6a5e"), 8.0, 38.0)
	overlay.set_shader_parameter("vignette", 0.6)
	_ground(
		Rect2(-14, -22, 28, 28), [], [], {"soil": Color("8e7056"), "grass_dry": Color("6e6450")}
	)
	_prop("banner", Vector3(0.8, 0, -2.6), -30.0, Vector3(0, 0, 24.0))
	_prop("harmata", Vector3(-2.8, 0, -3.6), 70.0, Vector3(0, 0, 12.0))
	_prop("viz", Vector3(4.0, 0, -6.5), 30.0, Vector3(0, 0, 70.0))
	_prop("kamin", Vector3(-1.2, 0, 0.8), 30.0, Vector3.ZERO, 0.6)
	_person("kozak", Vector3(-0.8, 0, -0.6), Vector3(3, 0, 2), "death", 1.0)
	_person("zholner", Vector3(2.2, 0, -1.4), Vector3(-2, 0, 3), "death_back", 1.0)
	_stuck("spear", Vector3(-1.9, 0, -1.4), 24.0, 40.0)
	_look(Vector3(0.0, 1.15, 5.2), Vector3(0.2, 1.2, -2.0), 42.0)


## 9. A hero lies dead: his friend kneels by him.
func _e9() -> void:
	_sky(
		{
			"top": Color("5a6070"),
			"horizon": Color("bcb6aa"),
			"glow": Color("dcd4c4"),
			"glow_size": 0.45,
			"sun": Vector2(0.45, 0.38),
			"clouds": 0.62,
			"cloud_dark": Color("666a78"),
			"cloud_lit": Color("dcd8cc"),
			"seed": 29.0
		}
	)
	_light(Vector3(0.45, -0.65, -0.6), Color("eae4d8"), 0.8, Color("9098aa"), 0.55)
	_fog(Color("aaa69c"), 8.0, 36.0)
	_ground(Rect2(-14, -22, 28, 28), [Vector3(1, -2, 3.0)])
	_person("kozak_camp", Vector3(0.45, 0, 0.05), Vector3(-1, 0, 0.1), "pick_up", 0.42)
	_person("serdiuk", Vector3(-0.85, 0, 0.0), Vector3(-1, 0, 2), "death", 1.0)
	_stuck("sabre", Vector3(-1.75, 0, -0.75), 8.0, 30.0)
	_prop("penok", Vector3(2.4, 0, -1.6))
	_prop("yalyna", Vector3(-5.0, 0, -9.0))
	_prop("yalyna", Vector3(4.5, 0, -12.0), 20.0)
	_look(Vector3(0.5, 1.15, 4.0), Vector3(-0.2, 0.65, 0.0), 40.0)


## 10. A cup of wine by the fire at night, a murderer fewer in the land.
func _e10() -> void:
	_sky(
		{
			"top": Color("0b0f1e"),
			"horizon": Color("2c2c4a"),
			"glow": Color("48507a"),
			"glow_size": 0.2,
			"sun": Vector2(0.8, 0.18),
			"sun_size": 0.03,
			"sun_colour": Color("f2ecd2"),
			"clouds": 0.25,
			"cloud_dark": Color("141a2c"),
			"cloud_lit": Color("3c4462"),
			"stars": 1.0,
			"seed": 31.0
		}
	)
	_light(Vector3(-0.5, -0.6, -0.6), Color("8a9ad2"), 0.35, Color("2a3050"), 0.5)
	_fog(Color("1c2032"), 8.0, 32.0)
	overlay.set_shader_parameter("vignette", 0.6)
	_ground(Rect2(-14, -20, 28, 26))
	_fire(Vector3(0, 0, -0.6))
	var drinker := _person("kozak", Vector3(-1.25, 0, -0.1), Vector3(0.4, 0, 2), "use_item", 0.45)
	drinker.unequip_all()
	_cup(drinker)
	_stuck("sabre", Vector3(-2.1, 0, -0.9), 10.0, 60.0)
	_person("kozak_svyta", Vector3(1.05, 0, -1.3), Vector3(0, 0, -0.6), "sit", 0.8)
	_prop("bochka", Vector3(1.9, 0, 0.3))
	_prop("skrynia", Vector3(-2.3, 0, -1.6), 30.0)
	_prop("stih", Vector3(-2.6, 0, -5.4))
	_prop("viz", Vector3(3.6, 0, -4.6), -60.0)
	_look(Vector3(0.3, 1.35, 4.2), Vector3(0.0, 0.75, -0.6), 42.0)


## 11. His men never believed in him: the colonel alone, his osauls walking away.
func _e11() -> void:
	_sky(
		{
			"top": Color("2a3050"),
			"horizon": Color("ca9272"),
			"glow": Color("e8a272"),
			"glow_size": 0.4,
			"sun": Vector2(0.62, 0.55),
			"clouds": 0.45,
			"cloud_dark": Color("3c3a54"),
			"cloud_lit": Color("eaa880"),
			"seed": 37.0
		}
	)
	_light(Vector3(-0.3, -0.4, -0.85), Color("ffc89a"), 0.95, Color("6e7090"), 0.5)
	_fog(Color("b88a70"), 10.0, 40.0)
	_ground(
		Rect2(-14, -24, 28, 30),
		[],
		[PackedVector2Array([Vector2(-1, 6), Vector2(1, -4), Vector2(4, -16)])]
	)
	_prop("shatro", Vector3(-4.2, 0, -3.6), 20.0)
	_prop("banner", Vector3(-2.0, 0, -0.8), 10.0)
	_person("polkovnyk", Vector3(-1.2, 0, 1.3), Vector3(0.5, 0, 6), "idle", 0.6)
	_person("kozak_camp", Vector3(0.9, 0, -2.4), Vector3(2.5, 0, -10), "walk", 0.2)
	_person("kozak_rival", Vector3(2.2, 0, -3.6), Vector3(3.5, 0, -12), "walk", 0.5)
	_person("kozak_svyta", Vector3(3.3, 0, -5.2), Vector3(4.5, 0, -14), "walk", 0.8)
	_look(Vector3(0.6, 1.5, 6.4), Vector3(0.2, 1.2, -1.5), 42.0)


## 12. A regiment on the march over green fields under big clouds.
func _e12() -> void:
	_sky(
		{
			"top": Color("4a78b0"),
			"horizon": Color("dce2e2"),
			"glow": Color("fff8e2"),
			"glow_size": 0.4,
			"sun": Vector2(0.18, 0.28),
			"clouds": 0.5,
			"cloud_dark": Color("8a98b2"),
			"cloud_lit": Color("ffffff"),
			"seed": 41.0,
			"horizon_y": 0.56
		}
	)
	_light(Vector3(0.6, -0.6, -0.5), Color("fff0d8"), 1.05, Color("a0aac4"), 0.45)
	_fog(Color("ccd6d8"), 16.0, 52.0)
	_ground(
		Rect2(-18, -24, 36, 32),
		[Vector3(-6, -4, 7.0), Vector3(4, -8, 8.0), Vector3(8, 2, 5.0), Vector3(-2, 3, 5.0)],
		[PackedVector2Array([Vector2(-14, 4), Vector2(-2, 0), Vector2(14, -6)])]
	)
	var kinds := ["kozak", "serdiuk", "kozak_camp", "luchnyk", "kozak_rival", "zholner"]
	var dir := Vector3(1, 0, -0.42).normalized()
	var side := Vector3(0.42, 0, 1).normalized()
	var i := 0
	for rank in 5:
		for file in 3:
			var at := Vector3(-6.0, 0, 2.6) + dir * (rank * 2.0) + side * (file - 1) * 1.25
			_person(
				kinds[i % kinds.size()], at, at + dir, "walk", fmod(rank * 0.37 + file * 0.21, 1.0)
			)
			i += 1
	_prop("banner", Vector3(-5.5, 0, 2.4) + dir * 7.0 - side * 1.6, 0.0)
	_prop("topolia", Vector3(-8.0, 0, -12.0))
	_prop("topolia", Vector3(-5.5, 0, -14.0), 30.0, Vector3.ZERO, 0.9)
	_prop("dub", Vector3(9.0, 0, -10.0))
	_look(Vector3(-1.2, 1.9, 8.4), Vector3(0.6, 1.0, -1.0), 44.0)


## 13. Through the enemy's lines in the storm: an armoured man, sabre raised.
func _e13() -> void:
	_sky(
		{
			"top": Color("12161e"),
			"horizon": Color("4c5464"),
			"glow": Color("8494b4"),
			"glow_size": 0.3,
			"sun": Vector2(0.72, 0.3),
			"clouds": 0.82,
			"cloud_dark": Color("1c222e"),
			"cloud_lit": Color("7a849a"),
			"bolt": 0.74,
			"seed": 43.0,
			"horizon_y": 0.7
		}
	)
	_light(Vector3(-0.5, -0.45, 0.75), Color("c8d0e8"), 1.0, Color("4a5062"), 0.55)
	_fog(Color("3c4250"), 8.0, 32.0)
	overlay.set_shader_parameter("rain", 1.0)
	overlay.set_shader_parameter("vignette", 0.6)
	_ground(
		Rect2(-14, -22, 28, 28), [], [], {"soil": Color("6e665c"), "grass_dry": Color("5c5c50")}
	)
	_person("rotmistr", Vector3(0, 0, 0), Vector3(-2, 0, 3), "attack_slash", 0.32)
	_person("zholner", Vector3(-2.6, 0, -3.6), Vector3(1, 0, 2), "blocking", 0.3)
	_person("zholner", Vector3(2.8, 0, -4.4), Vector3(-1, 0, 2), "idle", 0.6)
	_look(Vector3(0.7, 0.55, 3.8), Vector3(0.0, 1.55, 0.0), 44.0)


## 14. A bitter old man alone by his house at dusk.
func _e14() -> void:
	_sky(
		{
			"top": Color("383a58"),
			"horizon": Color("da9a72"),
			"glow": Color("e2a272"),
			"glow_size": 0.35,
			"sun": Vector2(0.78, 0.6),
			"clouds": 0.4,
			"cloud_dark": Color("44405a"),
			"cloud_lit": Color("e6a684"),
			"stars": 0.15,
			"seed": 47.0
		}
	)
	_light(Vector3(-0.6, -0.35, -0.7), Color("ffbe8e"), 0.85, Color("6a6a88"), 0.5)
	_fog(Color("b8907a"), 12.0, 40.0)
	_ground(Rect2(-14, -22, 28, 28), [Vector3(3, -3, 3.0)])
	_prop("khata", Vector3(0.4, 0, -4.6), 0.0)
	_prop("drova", Vector3(2.8, 0, -2.3), -20.0)
	_prop("penok", Vector3(-2.8, 0, -1.2))
	_prop("tyn", Vector3(-4.6, 0, -2.0), 80.0)
	_prop("dub", Vector3(-7.5, 0, -7.0), 10.0)
	_person("kozak_svyta", Vector3(-1.3, 0, -1.9), Vector3(1.5, 0, 3), "sit", 0.2)
	_look(Vector3(0.8, 1.45, 5.0), Vector3(0.0, 1.35, -2.6), 42.0)


## 15. Graves on a hill under a red sky: a whole house wiped out.
func _e15() -> void:
	_sky(
		{
			"top": Color("1a0e18"),
			"horizon": Color("c4322a"),
			"glow": Color("d84a32"),
			"glow_size": 0.55,
			"sun": Vector2(0.46, 0.62),
			"sun_size": 0.09,
			"sun_colour": Color("f28a44"),
			"clouds": 0.5,
			"cloud_dark": Color("2a1018"),
			"cloud_lit": Color("e25e3c"),
			"seed": 53.0,
			"horizon_y": 0.66
		}
	)
	_light(Vector3(0.05, -0.2, 0.98), Color("ff7a50"), 0.9, Color("3c1c2a"), 0.6)
	_fog(Color("8c2a26"), 10.0, 40.0)
	overlay.set_shader_parameter("vignette", 0.7)
	_ground(
		Rect2(-14, -22, 28, 28), [], [], {"soil": Color("5a3a30"), "grass_dry": Color("4a3a30")}
	)
	_mound(Vector3(0, -2.6, -5.0), 7.0, 3.1, GRASS)
	_cross(Vector3(-2.4, 0.15, -4.4), 6.0, 10.0, 1.5)
	_cross(Vector3(-0.8, 0.45, -4.8), -4.0, -15.0, 1.7)
	_cross(Vector3(0.9, 0.42, -4.7), 10.0, 20.0, 1.4)
	_cross(Vector3(2.5, 0.1, -4.2), -12.0, 0.0, 1.55)
	_stuck("sabre", Vector3(0.1, 0.4, -4.1), -14.0, 0.0)
	_look(Vector3(0.0, 0.5, 5.0), Vector3(0.0, 1.5, -4.0), 38.0)
