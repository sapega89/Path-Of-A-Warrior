extends Node3D
## Ground for a scene in the new art: a grid painted by ground.gdshader. Vertex colours
## mark trodden paths (r) and green grass (g); outside the play area the land rises
## into low hills so the edge of the world is never seen. Grass tufts are one MultiMesh.

const ArtKit := preload("res://scripts/art/art_kit.gd")
const GROUND := preload("res://assets/art/shaders/ground.gdshader")

var size := 64.0
var step := 0.5
## Rectangle on the XZ plane that stays flat (x, z, width, depth).
var play := Rect2(-12, -12, 24, 24)
## Polylines on the XZ plane (Array of PackedVector2Array) and their half width.
var paths: Array = []
var path_width := 0.8
## Green patches: Vector3(x, z, radius).
var greens: Array = []
var tufts := 140
var seed_value := 3

var _rng := RandomNumberGenerator.new()


func build() -> void:
	_rng.seed = seed_value
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var n := int(size / step)
	var half := size / 2.0
	for i in n + 1:
		for j in n + 1:
			var x := -half + i * step
			var z := -half + j * step
			st.set_color(Color(_path_amount(x, z), _green_amount(x, z), 0.0))
			st.add_vertex(Vector3(x, height(x, z), z))
	for i in n:
		for j in n:
			var a := i * (n + 1) + j
			var b := a + n + 1
			# clockwise seen from above: Godot's front face
			st.add_index(a)
			st.add_index(b)
			st.add_index(a + 1)
			st.add_index(b)
			st.add_index(b + 1)
			st.add_index(a + 1)
	st.generate_normals()
	var mi := MeshInstance3D.new()
	mi.name = "Ground"
	mi.mesh = st.commit()
	var m := ShaderMaterial.new()
	m.shader = GROUND
	mi.material_override = m
	add_child(mi)
	_scatter_tufts()


func height(x: float, z: float) -> float:
	var dx := maxf(play.position.x - x, x - play.end.x)
	var dz := maxf(play.position.y - z, z - play.end.y)
	var out := maxf(maxf(dx, dz), 0.0)
	if out <= 0.0:
		return 0.0
	var rise := smoothstep(0.0, 9.0, out) * 3.2
	var wave := 0.6 + 0.4 * sin(x * 0.31 + cos(z * 0.23) * 2.0) * cos(z * 0.27 - x * 0.11)
	return rise * wave


func _path_amount(x: float, z: float) -> float:
	var p := Vector2(x, z)
	var best := 99.0
	for line in paths:
		var pl: PackedVector2Array = line
		for k in pl.size() - 1:
			var q := Geometry2D.get_closest_point_to_segment(p, pl[k], pl[k + 1])
			best = minf(best, p.distance_to(q))
	return 1.0 - smoothstep(path_width * 0.5, path_width * 1.3, best)


func _green_amount(x: float, z: float) -> float:
	var g := 0.0
	for patch in greens:
		var v: Vector3 = patch
		var d := Vector2(x, z).distance_to(Vector2(v.x, v.y))
		g = maxf(g, 1.0 - smoothstep(v.z * 0.4, v.z, d))
	return g


func _scatter_tufts() -> void:
	var source: Node = ArtKit.scene("props/trava.glb").instantiate()
	var mesh_node: MeshInstance3D = source.find_children("*", "MeshInstance3D", true, false)[0]
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.mesh = mesh_node.mesh
	var placed: Array[Transform3D] = []
	var tries := 0
	while placed.size() < tufts and tries < tufts * 10:
		tries += 1
		var x := _rng.randf_range(play.position.x - 6.0, play.end.x + 6.0)
		var z := _rng.randf_range(play.position.y - 6.0, play.end.y + 6.0)
		if _path_amount(x, z) > 0.2:
			continue
		var t := Transform3D(Basis(Vector3.UP, _rng.randf() * TAU).scaled(Vector3.ONE * _rng.randf_range(0.45, 0.8)),
			Vector3(x, height(x, z), z))
		placed.append(t)
	mm.instance_count = placed.size()
	for i in placed.size():
		mm.set_instance_transform(i, placed[i])
	var mmi := MultiMeshInstance3D.new()
	mmi.name = "Tufts"
	mmi.multimesh = mm
	mmi.material_override = ArtKit.props_material()
	mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mmi)
	source.free()
