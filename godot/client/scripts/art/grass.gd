extends RefCounted
## Grass and wheat that sway in the wind (grass.gdshader): clumps of thin blades scattered by
## MultiMeshes, one for each CHUNK × CHUNK metres, so the ones off the screen are not drawn.
## Each clump's instance carries the colour it grows in (its custom data), so grass on a meadow
## and on lush grass, and the wheat of the fields, differ while sharing one mesh and material.

const SHADER := preload("res://assets/art/shaders/grass.gdshader")
const CHUNK := 8.0

## How a kind of clump is made: blades, their height and width (metres), ears of wheat on top.
const KINDS := {
	"grass": {"blades": 7, "height": 0.34, "width": 0.05, "ears": false},
	"wheat": {"blades": 5, "height": 0.62, "width": 0.03, "ears": true},
}

static var _meshes := {}
static var _material: ShaderMaterial

## Clumps to place: per kind, per chunk, [transform, colour] pairs.
var _clumps := {}


static func material() -> ShaderMaterial:
	if _material == null:
		_material = ShaderMaterial.new()
		_material.shader = SHADER
	return _material


static func mesh(kind: String) -> ArrayMesh:
	if not _meshes.has(kind):
		var k: Dictionary = KINDS[kind]
		_meshes[kind] = clump(int(k.blades), float(k.height), float(k.width), bool(k.ears), kind.hash())
	return _meshes[kind]


## A clump of `blades` thin blades about `height` tall, leaning out from its middle. The vertex
## colour: red how high up (0 at the root, 1 at the tip), alpha 1 on an ear of wheat.
static func clump(blades: int, height: float, width: float, ears: bool, seed: int) -> ArrayMesh:
	var rng := RandomNumberGenerator.new()
	rng.seed = seed
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in blades:
		var a := TAU * (i + rng.randf() * 0.7) / blades
		var out := Vector3(cos(a), 0.0, sin(a))
		var root := out * rng.randf_range(0.0, 0.06)
		var tall := height * rng.randf_range(0.7, 1.0)
		var top := out * tall * rng.randf_range(0.15, 0.4) + Vector3(0.0, tall, 0.0)
		# the blade turned to face a random way, so the camera sees most of them broadside
		var side := Vector3(1.0, 0.0, 0.0).rotated(Vector3.UP, rng.randf() * PI) * width * 0.5
		if ears:
			# a stalk, and an ear of wheat: a narrow diamond along its top
			var ear_at := root + top * 0.7
			_tri(st, [root - side * 0.6, root + side * 0.6, ear_at], [0.0, 0.0, 0.7], 0.0)
			var mid := root + top * 0.85
			_tri(st, [ear_at, mid + side * 1.8, root + top], [0.7, 0.85, 1.0], 1.0)
			_tri(st, [ear_at, root + top, mid - side * 1.8], [0.7, 1.0, 0.85], 1.0)
		else:
			_tri(st, [root - side, root + side, root + top], [0.0, 0.0, 1.0], 0.0)
	return st.commit()


static func _tri(st: SurfaceTool, points: Array, ups: Array, ear: float) -> void:
	for i in 3:
		st.set_color(Color(ups[i], 0.0, 0.0, ear))
		st.set_normal(Vector3.UP)
		st.add_vertex(points[i])


## One clump of `kind` at `at` (on the ground), turned and sized at random, in `colour`.
func add(kind: String, at: Vector3, colour: Color, rng: RandomNumberGenerator) -> void:
	var key := Vector2i(floori(at.x / CHUNK), floori(at.z / CHUNK))
	if not _clumps.has(kind):
		_clumps[kind] = {}
	if not _clumps[kind].has(key):
		_clumps[kind][key] = []
	var basis := Basis(Vector3.UP, rng.randf() * TAU).scaled(Vector3.ONE * rng.randf_range(0.75, 1.25))
	_clumps[kind][key].append([Transform3D(basis, at), Color(colour.r, colour.g, colour.b, rng.randf())])


## How many clumps of a kind are placed.
func count(kind: String) -> int:
	var n := 0
	for key in _clumps.get(kind, {}):
		n += _clumps[kind][key].size()
	return n


## The MultiMeshes of everything placed, under `parent` (a node named Grass, one child a chunk).
func build(parent: Node3D) -> Node3D:
	var holder := Node3D.new()
	holder.name = "Grass"
	parent.add_child(holder)
	for kind in _clumps:
		for key in _clumps[kind]:
			var list: Array = _clumps[kind][key]
			var mm := MultiMesh.new()
			mm.transform_format = MultiMesh.TRANSFORM_3D
			mm.use_custom_data = true
			mm.mesh = mesh(kind)
			mm.instance_count = list.size()
			for i in list.size():
				mm.set_instance_transform(i, list[i][0])
				mm.set_instance_custom_data(i, list[i][1])
			var mmi := MultiMeshInstance3D.new()
			mmi.name = "%s_%d_%d" % [kind, key.x, key.y]
			mmi.multimesh = mm
			mmi.material_override = material()
			mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
			holder.add_child(mmi)
	return holder
