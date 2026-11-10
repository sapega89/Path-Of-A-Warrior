extends Node
## Paints the portraits of the new art (needs a display, not --headless):
##   godot --path godot/client --resolution 640x640 res://tools/portraits.tscn
## Each bust of assets/art/portraits/busts.glb (made by godot/tools/art/portraits.py) in the
## game's painted shader with its ink outline, lit as the figures on the maps, turned as
## busts.json says, before a backdrop in the colour of its side
## (assets/art/shaders/portrait_backdrop.gdshader), into assets/art/portraits/<number>.png.

const DIR := "res://assets/art/portraits/"
const SIZE := 512  # painted at, then made smaller
const OUT := 256
## The backdrop of each side: [light behind the head, dark at the corners].
const SIDES := {
	"cossack": [Color("9a7f52"), Color("2e2216")],
	"crown": [Color("6e7f95"), Color("161e2c")],
	"horde": [Color("8a4a42"), Color("2a1014")],
	"hero": [Color("a8884e"), Color("3a2810")],
	"plain": [Color("827868"), Color("26221c")],
}

var view: SubViewport  # the bust, on a clear background
var canvas: SubViewport  # the backdrop with the bust over it
var stand: Node3D
var backdrop: ShaderMaterial


func _ready() -> void:
	var only := OS.get_cmdline_user_args()
	_stage()
	var info: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(DIR + "busts.json"))
	var busts: Node = load(DIR + "busts.glb").instantiate()
	var meshes := {}
	for m in busts.find_children("bust_*", "MeshInstance3D", true, false):
		meshes[String(m.name).trim_prefix("bust_")] = m
	var ids := info.keys()
	ids.sort_custom(func(a, b): return int(a) < int(b))
	for id in ids:
		if not only.is_empty() and not (id in only):
			continue
		var m: MeshInstance3D = meshes.get(id)
		if m == null:
			push_error("no bust %s" % id)
			continue
		var bust := MeshInstance3D.new()
		bust.mesh = m.mesh
		bust.material_override = ArtKit.painted(true)
		bust.rotation.y = deg_to_rad(float(info[id].look))
		stand.add_child(bust)
		var side: Array = SIDES.get(String(info[id].side), SIDES.plain)
		backdrop.set_shader_parameter("light_colour", side[0])
		backdrop.set_shader_parameter("dark_colour", side[1])
		await _frames(4)
		await RenderingServer.frame_post_draw
		var img := canvas.get_texture().get_image()
		img.resize(OUT, OUT, Image.INTERPOLATE_LANCZOS)
		img.save_png(ProjectSettings.globalize_path(DIR + "%s.png" % id))
		print("portrait ", id)
		bust.free()
	busts.free()
	get_tree().quit()


## A small world of its own: the sun and the air of the maps, the camera on the head and
## shoulders; its picture is laid over the backdrop in a second, flat viewport.
func _stage() -> void:
	view = SubViewport.new()
	view.size = Vector2i(SIZE, SIZE)
	view.own_world_3d = true
	view.transparent_bg = true
	view.msaa_3d = Viewport.MSAA_8X
	view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	add_child(view)
	var env := Environment.new()
	env.background_mode = Environment.BG_CLEAR_COLOR
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	var we := WorldEnvironment.new()
	we.environment = env
	view.add_child(we)
	var sun := DirectionalLight3D.new()
	ArtKit.light(sun, env)
	# a hard light from the side: half of the face in the shade
	sun.light_energy = 1.05
	env.ambient_light_energy = 0.3
	sun.transform = Transform3D(
		Basis.looking_at(Vector3(0.8, -0.4, -0.45).normalized(), Vector3.UP), Vector3.ZERO
	)
	view.add_child(sun)
	stand = Node3D.new()
	view.add_child(stand)
	var camera := Camera3D.new()
	camera.fov = 24.0
	view.add_child(camera)
	camera.look_at_from_position(Vector3(0, 1.69, 1.9), Vector3(0, 1.63, 0), Vector3.UP)

	canvas = SubViewport.new()
	canvas.size = Vector2i(SIZE, SIZE)
	canvas.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	add_child(canvas)
	var rect := ColorRect.new()
	rect.size = Vector2(SIZE, SIZE)
	backdrop = ShaderMaterial.new()
	backdrop.shader = preload("res://assets/art/shaders/portrait_backdrop.gdshader")
	rect.material = backdrop
	canvas.add_child(rect)
	var bust := TextureRect.new()
	bust.texture = view.get_texture()
	bust.size = Vector2(SIZE, SIZE)
	canvas.add_child(bust)


func _frames(n: int) -> void:
	for i in n:
		await get_tree().process_frame
