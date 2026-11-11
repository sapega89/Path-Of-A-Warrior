extends "res://tests/test_case.gd"
## Many copies of a prop in batches (scripts/art/prop_field.gd): one MultiMesh for each mesh of
## the prop in each chunk, every copy in the props' material, each mesh where it sits in a node
## of the prop. (Headless, a MultiMesh keeps no transforms to read back: the place of a mesh in
## the prop is checked on its own.)

const COPIES := 30


func test_copies_in_batches() -> void:
	var parent := Node3D.new()
	root.add_child(parent)
	var field := PropField.new("ochert")
	for i in COPIES:
		field.add(
			Transform3D(
				Basis(Vector3.UP, i * 0.7).scaled(Vector3.ONE * (0.8 + i * 0.01)),
				Vector3(i * 0.8 - 12.0, 0.1 * i, sin(i) * 6.0)
			)
		)
	eq(field.count(), COPIES, "every copy")
	var holder := field.build(parent)
	eq(holder.name, &"Ochert", "named after the prop")
	var prop := ArtKit.prop("ochert")
	var meshes := prop.find_children("*", "MeshInstance3D", true, false).size()
	var drawn := 0
	for batch: MultiMeshInstance3D in holder.get_children():
		check(
			batch.material_override == ArtKit.props_material(),
			"%s: the props' material" % batch.name
		)
		drawn += batch.multimesh.instance_count
	eq(drawn, COPIES * meshes, "each mesh of each copy once")
	# 24 × 12 m: four chunks at most
	check(holder.get_child_count() <= meshes * 4, "%d batches" % holder.get_child_count())
	prop.free()
	parent.free()


func test_a_mesh_sits_as_in_the_prop() -> void:
	var parent := Node3D.new()
	root.add_child(parent)
	for prop_name in ["ochert", "palisade"]:
		var prop := ArtKit.prop(prop_name)
		var place := Transform3D(Basis(Vector3.UP, 0.7).scaled(Vector3.ONE * 0.9), Vector3(3, 1, 2))
		prop.transform = place
		parent.add_child(prop)
		for node in prop.find_children("*", "MeshInstance3D", true, false):
			var mi := node as MeshInstance3D
			check(
				(place * PropField._in_prop(mi, prop)).is_equal_approx(mi.global_transform),
				"%s: %s where the prop has it" % [prop_name, mi.name]
			)
		prop.free()
	parent.free()
