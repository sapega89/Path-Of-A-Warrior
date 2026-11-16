extends "res://tests/test_case.gd"
## The ground in chunks (scripts/art/ground_mesh.gd): every cell of the grid is drawn once, the
## chunks are small enough to be left out when off the screen, and the light falls on them as on
## one mesh of the whole grid (the same normals, so no seam where two chunks meet).

const COLUMNS := 41
const ROWS := 30
const STEP := 1.0


## A grid of hills and a ditch, with colours and the two channels of a map.
func _grid() -> GroundMesh:
	var grid := GroundMesh.new(COLUMNS, ROWS, STEP)
	for z in ROWS:
		for x in COLUMNS:
			var y := sin(x * 0.4) * cos(z * 0.3) * 1.5 - (0.7 if absi(x - 20) < 2 else 0.0)
			grid.add(Vector3(x * STEP, y, z * STEP), Color(x / 40.0, z / 30.0, 0.5))
			grid.add_uv(Vector2(x, z), Vector2(z, x))
	return grid


func test_every_cell_once_in_small_chunks() -> void:
	var grid := _grid()
	var ground := grid.build(StandardMaterial3D.new())
	check(ground.get_child_count() > 4, "in chunks: %d" % ground.get_child_count())
	var triangles := 0
	var cells := {}
	for chunk: MeshInstance3D in ground.get_children():
		var arrays := chunk.mesh.surface_get_arrays(0)
		var verts: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
		var index: PackedInt32Array = arrays[Mesh.ARRAY_INDEX]
		triangles += index.size() / 3
		for i in range(0, index.size(), 3):
			var middle := (verts[index[i]] + verts[index[i + 1]] + verts[index[i + 2]]) / 3.0
			var cell := Vector2i(floori(middle.x / STEP), floori(middle.z / STEP))
			cells[cell] = int(cells.get(cell, 0)) + 1
		var box := chunk.get_aabb()
		check(
			box.size.x <= GroundMesh.CHUNK + STEP and box.size.z <= GroundMesh.CHUNK + STEP,
			"%s is %.1f × %.1f m" % [chunk.name, box.size.x, box.size.z]
		)
		check(arrays[Mesh.ARRAY_TEX_UV2] != null, "%s keeps the second channel" % chunk.name)
	eq(triangles, (COLUMNS - 1) * (ROWS - 1) * 2, "two triangles a cell")
	eq(cells.size(), (COLUMNS - 1) * (ROWS - 1), "every cell")
	for cell: Vector2i in cells:
		eq(cells[cell], 2, "cell %s drawn once" % cell)
	ground.free()


func test_lit_as_one_mesh() -> void:
	var grid := _grid()
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in grid.vertices.size():
		st.set_color(grid.colors[i])
		st.add_vertex(grid.vertices[i])
	for z in ROWS - 1:
		for x in COLUMNS - 1:
			var a := grid.at(x, z)
			var b := a + COLUMNS
			for k: int in [a, a + 1, b, b, a + 1, b + 1]:
				st.add_index(k)
	st.generate_normals()
	var whole := st.commit().surface_get_arrays(0)
	var expected := {}
	for i in (whole[Mesh.ARRAY_VERTEX] as PackedVector3Array).size():
		expected[whole[Mesh.ARRAY_VERTEX][i]] = whole[Mesh.ARRAY_NORMAL][i]
	var ground := grid.build(StandardMaterial3D.new())
	var worst := 0.0
	var seen := 0
	for chunk: MeshInstance3D in ground.get_children():
		var arrays := chunk.mesh.surface_get_arrays(0)
		for i in (arrays[Mesh.ARRAY_VERTEX] as PackedVector3Array).size():
			var n: Vector3 = arrays[Mesh.ARRAY_NORMAL][i]
			worst = maxf(worst, n.distance_to(expected[arrays[Mesh.ARRAY_VERTEX][i]]))
			seen += 1
	check(seen > grid.vertices.size(), "the chunks share their edges")
	check(worst < 0.001, "the normals of one mesh: off by %.4f" % worst)
	ground.free()
