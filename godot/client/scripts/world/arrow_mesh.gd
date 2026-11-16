@tool
class_name ArrowMesh
extends PrimitiveMesh
## An archer's arrow along +Z (scenes/world/effects/arrow.tscn): a shaft of oak, a steel head,
## white and red fletching, in vertex colours of the palette (ArtKit.color()).


func _create_mesh_array() -> Array:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	_box(
		st, Vector3(0.0, 0.0, 0.0), Vector3(0.03, 0.03, 0.72), ArtKit.color("ochre").darkened(0.25)
	)
	# the head: a pyramid
	var steel := ArtKit.color("steel").lightened(0.2)
	var tip := Vector3(0.0, 0.0, 0.48)
	var base := [
		Vector3(-0.045, 0.0, 0.34),
		Vector3(0.0, 0.045, 0.34),
		Vector3(0.045, 0.0, 0.34),
		Vector3(0.0, -0.045, 0.34)
	]
	for i in 4:
		_tri(st, base[i], base[(i + 1) % 4], tip, steel)
	# the fletching: two crossed vanes
	for v in [Vector3(0.07, 0.0, 0.0), Vector3(0.0, 0.07, 0.0)]:
		var col := ArtKit.color("whitewash") if v.x > 0.0 else ArtKit.color("cinnabar")
		var a := Vector3(0.0, 0.0, -0.36)
		var b := Vector3(0.0, 0.0, -0.2)
		_tri(st, a - v, b, a + v, col)
		_tri(st, a + v, b, a - v, col)
	st.generate_normals()
	return st.commit_to_arrays()


static func _tri(st: SurfaceTool, a: Vector3, b: Vector3, c: Vector3, col: Color) -> void:
	st.set_color(col.srgb_to_linear())
	st.add_vertex(a)
	st.add_vertex(b)
	st.add_vertex(c)


static func _box(st: SurfaceTool, at: Vector3, size: Vector3, col: Color) -> void:
	var h := size / 2.0
	var c := [
		Vector3(-h.x, -h.y, -h.z),
		Vector3(h.x, -h.y, -h.z),
		Vector3(h.x, h.y, -h.z),
		Vector3(-h.x, h.y, -h.z),
		Vector3(-h.x, -h.y, h.z),
		Vector3(h.x, -h.y, h.z),
		Vector3(h.x, h.y, h.z),
		Vector3(-h.x, h.y, h.z)
	]
	for f in [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [3, 7, 6, 2], [0, 4, 7, 3], [1, 2, 6, 5]]:
		_tri(st, at + c[f[0]], at + c[f[1]], at + c[f[2]], col)
		_tri(st, at + c[f[0]], at + c[f[2]], at + c[f[3]], col)
