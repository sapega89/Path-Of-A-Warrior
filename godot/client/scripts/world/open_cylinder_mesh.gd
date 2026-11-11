@tool
class_name OpenCylinderMesh
extends PrimitiveMesh
## An open cylinder of radius 1 and 1 high, its middle at the origin, for the effects that stand
## round someone (FxRigs): UV.x goes round it, UV.y from the top (0) to the bottom (1).

## Quads round it.
const SIDES := 24


func _create_mesh_array() -> Array:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in SIDES:
		var u0 := float(i) / SIDES
		var u1 := float(i + 1) / SIDES
		var a := Vector3(cos(u0 * TAU), 0.0, sin(u0 * TAU))
		var b := Vector3(cos(u1 * TAU), 0.0, sin(u1 * TAU))
		var top := Vector3(0.0, 0.5, 0.0)
		for v in [
			[a + top, Vector2(u0, 0.0)],
			[b + top, Vector2(u1, 0.0)],
			[b - top, Vector2(u1, 1.0)],
			[a + top, Vector2(u0, 0.0)],
			[b - top, Vector2(u1, 1.0)],
			[a - top, Vector2(u0, 1.0)]
		]:
			st.set_uv(v[1])
			st.add_vertex(v[0])
	return st.commit_to_arrays()
