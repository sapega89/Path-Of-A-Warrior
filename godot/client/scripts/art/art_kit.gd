extends RefCounted
## The new art: palette, materials and loaders for the models that
## godot/tools/art/build.py makes (people, weapons, shared clips, environment pieces).

const ROOT := "res://assets/art/"
const PAINTED := preload("res://assets/art/shaders/painted.gdshader")
const OUTLINE := preload("res://assets/art/shaders/outline.gdshader")

## The ten colours of the style guide.
const PALETTE := {
	"chernozem": Color("2B211C"),
	"ochre": Color("C9A15B"),
	"grass": Color("9E9A5C"),
	"oak": Color("4E6B3A"),
	"whitewash": Color("EDE6D6"),
	"cinnabar": Color("A8322D"),
	"blue": Color("2F4E7A"),
	"gold": Color("D4A645"),
	"steel": Color("6E7780"),
	"dusk": Color("1C2230"),
}

## Clips that repeat.
const LOOPING := ["idle", "idle_unarmed", "idle_2h", "walk", "walk_relaxed", "walk_back", "run",
	"run_relaxed", "blocking", "sit", "aim_bow"]

static var _scenes := {}
static var _clips: AnimationLibrary
static var _props_material: ShaderMaterial


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
