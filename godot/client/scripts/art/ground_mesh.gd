class_name GroundMesh
extends RefCounted
## The ground of a 3D view as a grid of vertices (`columns` × `rows`, row after row along x,
## `step` metres apart) cut into chunks of about CHUNK metres a side, each its own mesh. The
## renderer then draws only the chunks the camera sees, and a lamp's shadow only those in its
## reach; one mesh of the whole land was drawn whole in every pass, most of it off the screen.
## The normals are worked out over the whole grid, as one mesh would have them, so the chunks
## meet without a seam in the light.

const CHUNK := 16.0

var columns := 0
var rows := 0
var step := 1.0
var vertices := PackedVector3Array()
var colors := PackedColorArray()
## Two more channels for each vertex (map_ground.gdshader reads them), or none.
var uvs := PackedVector2Array()
var uv2s := PackedVector2Array()


func _init(grid_columns: int, grid_rows: int, grid_step: float) -> void:
	columns = grid_columns
	rows = grid_rows
	step = grid_step


## The next vertex of the grid (along x, then the next row).
func add(at: Vector3, colour: Color) -> void:
	vertices.append(at)
	colors.append(colour)


## The two channels of the vertex added last.
func add_uv(uv: Vector2, uv2: Vector2) -> void:
	uvs.append(uv)
	uv2s.append(uv2)


## The chunks under a new node (named Ground), all painted with `material`.
func build(material: Material) -> Node3D:
	var holder := Node3D.new()  # standards: allow nodes_in_code (the ground of the view)
	holder.name = "Ground"
	var normals := _normals()
	var cells := maxi(1, roundi(CHUNK / step))
	for z0 in range(0, rows - 1, cells):
		for x0 in range(0, columns - 1, cells):
			var mi := MeshInstance3D.new()  # standards: allow nodes_in_code (a chunk of the ground)
			mi.name = "Chunk_%d_%d" % [x0 / cells, z0 / cells]
			mi.mesh = _chunk(
				x0, z0, mini(x0 + cells, columns - 1), mini(z0 + cells, rows - 1), normals
			)
			mi.material_override = material
			holder.add_child(mi)
	return holder


## The vertex at column x, row z.
func at(x: int, z: int) -> int:
	return z * columns + x


## Each vertex's normal: the faces round it, each counted once (as SurfaceTool.generate_normals).
## A cell from vertex a (b the one a row on) is two triangles, clockwise seen from above
## (Godot's front face): a, a + 1, b and b, a + 1, b + 1.
func _normals() -> PackedVector3Array:
	var sums := PackedVector3Array()
	sums.resize(vertices.size())
	for z in rows - 1:
		for x in columns - 1:
			var a := at(x, z)
			var b := a + columns
			var first := Plane(vertices[a], vertices[a + 1], vertices[b]).normal
			var second := Plane(vertices[b], vertices[a + 1], vertices[b + 1]).normal
			sums[a] += first
			sums[a + 1] += first + second
			sums[b] += first + second
			sums[b + 1] += second
	for i in sums.size():
		sums[i] = sums[i].normalized()
	return sums


## The mesh of the cells from column x0, row z0 to column x1, row z1 (their far corners).
func _chunk(x0: int, z0: int, x1: int, z1: int, normals: PackedVector3Array) -> ArrayMesh:
	var width := x1 - x0 + 1
	var arrays: Array = []
	arrays.resize(Mesh.ARRAY_MAX)
	var verts := PackedVector3Array()
	var norms := PackedVector3Array()
	var cols := PackedColorArray()
	var uv := PackedVector2Array()
	var uv2 := PackedVector2Array()
	var with_uv := uvs.size() == vertices.size()
	for z in range(z0, z1 + 1):
		for x in range(x0, x1 + 1):
			var k := at(x, z)
			verts.append(vertices[k])
			norms.append(normals[k])
			cols.append(colors[k])
			if with_uv:
				uv.append(uvs[k])
				uv2.append(uv2s[k])
	var index := PackedInt32Array()
	for z in z1 - z0:
		for x in width - 1:
			var a := z * width + x
			var b := a + width
			index.append_array(PackedInt32Array([a, a + 1, b, b, a + 1, b + 1]))  # as in _normals()
	arrays[Mesh.ARRAY_VERTEX] = verts
	arrays[Mesh.ARRAY_NORMAL] = norms
	arrays[Mesh.ARRAY_COLOR] = cols
	if with_uv:
		arrays[Mesh.ARRAY_TEX_UV] = uv
		arrays[Mesh.ARRAY_TEX_UV2] = uv2
	arrays[Mesh.ARRAY_INDEX] = index
	var mesh := ArrayMesh.new()
	mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
	return mesh
