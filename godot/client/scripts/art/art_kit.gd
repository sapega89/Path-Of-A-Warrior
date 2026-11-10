class_name ArtKit
extends RefCounted
## The new art: palette, materials and loaders for the models that
## godot/tools/art/build.py makes (people, weapons, shared clips, environment pieces).

const ROOT := "res://assets/art/"
const PAINTED := preload("res://assets/art/shaders/painted.gdshader")
const OUTLINE := preload("res://assets/art/shaders/outline.gdshader")

## The ten colours of the style guide.
const PALETTE := {
	"chernozem": Color("2B211C"),
	"ochre": Color("A88A57"),
	"grass": Color("85814F"),
	"oak": Color("435A33"),
	"whitewash": Color("CFC5B0"),
	"cinnabar": Color("8A2B25"),
	"blue": Color("2D3F57"),
	"gold": Color("AE8C48"),
	"steel": Color("6A7178"),
	"dusk": Color("1C2230"),
}

## Clips that repeat.
const LOOPING := [
	"idle",
	"idle_unarmed",
	"idle_2h",
	"walk",
	"walk_relaxed",
	"walk_back",
	"run",
	"run_relaxed",
	"blocking",
	"sit",
	"aim_bow"
]

## The light and air of the world: a warm sun through thin clouds, a cool shade that still
## shows the colours in it, the land fading far away into grey dust.
const SUN_COLOR := Color("f5e2c2")
const SUN_ENERGY := 0.95
const AMBIENT := Color("6e7a96")
const AMBIENT_ENERGY := 0.5
const AIR := Color("a7a393")
## The grade of the finished picture: brightness, contrast, saturation (a little muted).
const GRADE := Vector3(1.0, 1.1, 0.88)

static var _scenes := {}
static var _clips: AnimationLibrary
static var _props_material: ShaderMaterial
static var _tufts_material: ShaderMaterial


static func scene(path: String) -> PackedScene:
	if not _scenes.has(path):
		_scenes[path] = load(ROOT + path)
	return _scenes[path]


## Material for painted wood; with an ink outline for living figures and things to use.
static func painted(outline: bool) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	m.shader = PAINTED
	if outline:
		var ink := ShaderMaterial.new()
		ink.shader = OUTLINE
		m.next_pass = ink
	return m


## One shared material for the environment (no outline: it stays behind the figures).
static func props_material() -> ShaderMaterial:
	if _props_material == null:
		_props_material = painted(false)
	return _props_material


## The grass tufts: painted, without the mud that rises over the feet of things.
static func tufts_material() -> ShaderMaterial:
	if _tufts_material == null:
		_tufts_material = painted(false)
		_tufts_material.set_shader_parameter("dirt_height", 0.0)
	return _tufts_material


## The world's sun, shade and air (SUN_COLOR, AMBIENT, AIR) and its grading: the colours
## held down, the contrast up.
static func light(sun: DirectionalLight3D, env: Environment) -> void:
	sun.light_color = SUN_COLOR
	sun.light_energy = SUN_ENERGY
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = AMBIENT
	env.ambient_light_energy = AMBIENT_ENERGY
	grade(env)


static func grade(env: Environment) -> void:
	env.adjustment_enabled = true
	env.adjustment_saturation = GRADE.z
	env.adjustment_contrast = GRADE.y
	env.adjustment_brightness = GRADE.x


static func dress(node: Node, material: Material) -> void:
	if node is MeshInstance3D:
		(node as MeshInstance3D).material_override = material
	for child in node.get_children():
		dress(child, material)


## An environment piece from props/<name>.glb, standing at its origin.
static func prop(prop_name: String, outline := false) -> Node3D:
	var node: Node3D = scene("props/%s.glb" % prop_name).instantiate()
	dress(node, painted(true) if outline else props_material())
	return node


## The clips every person shares, from characters/humanoid_clips.glb.
static func clips() -> AnimationLibrary:
	if _clips == null:
		var holder: Node = scene("characters/humanoid_clips.glb").instantiate()
		var player := holder.find_child("AnimationPlayer", true, false) as AnimationPlayer
		_clips = player.get_animation_library(&"")
		for clip_name in LOOPING:
			if _clips.has_animation(clip_name):
				_clips.get_animation(clip_name).loop_mode = Animation.LOOP_LINEAR
		holder.free()
	return _clips


static func color(name: String) -> Color:
	return PALETTE.get(name, Color.MAGENTA)
