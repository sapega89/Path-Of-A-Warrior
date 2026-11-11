@tool
class_name SweepMesh
extends PrimitiveMesh
## A curved ribbon round a middle, like the trail of a blade: `arc_deg` degrees round from
## `start_deg` (0 in front, +Z), from 0.55 of `radius` out to all of it, `height` up and rising
## by `tilt` along the way. UV.x runs along the arc (0..1), UV.y across it (0 inside, 1 outside).

## Quads along the arc.
const STEPS := 24
## Where the ribbon starts, a part of the radius.
const INNER := 0.55

@export var start_deg := 0.0:
	set(value):
		start_deg = value
		request_update()
@export var arc_deg := 150.0:
	set(value):
		arc_deg = value
		request_update()
@export var radius := 1.15:
	set(value):
		radius = value
		request_update()
@export var height := 1.1:
	set(value):
		height = value
		request_update()
@export var tilt := 0.35:
	set(value):
		tilt = value
		request_update()


func _create_mesh_array() -> Array:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in STEPS + 1:
		var t := float(i) / STEPS
		var a := deg_to_rad(start_deg + arc_deg * t)
		var dir := Vector3(sin(a), 0.0, cos(a))
		var lift := tilt * (t - 0.5)
		for j in 2:
			var r := radius * (INNER if j == 0 else 1.0)
			st.set_uv(Vector2(t, float(j)))
			st.add_vertex(dir * r + Vector3(0.0, height + lift * r, 0.0))
	for i in STEPS:
		var a := i * 2
		st.add_index(a)
		st.add_index(a + 1)
		st.add_index(a + 2)
		st.add_index(a + 1)
		st.add_index(a + 3)
		st.add_index(a + 2)
	return st.commit_to_arrays()
