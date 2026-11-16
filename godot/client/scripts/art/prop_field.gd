class_name PropField
extends RefCounted
## Many copies of one prop (the reeds along the water, the pieces of a palisade) drawn as
## MultiMeshes, one for each CHUNK × CHUNK metres, in place of a node for each copy: the renderer
## draws a chunk at one go, in the picture and in every shadow, where it drew each copy on its
## own. The copies look as ArtKit.prop() ones: the same meshes in the same material.

const CHUNK := 16.0

var prop_name := ""
## Where the copies stand, by chunk: Vector2i -> Array of Transform3D.
var _placed := {}


func _init(prop: String) -> void:
	prop_name = prop


## One more copy, placed in the space of the node that build() fills.
func add(place: Transform3D) -> void:
	var key := Vector2i(floori(place.origin.x / CHUNK), floori(place.origin.z / CHUNK))
	if not _placed.has(key):
		_placed[key] = []
	_placed[key].append(place)


## How many copies there are.
func count() -> int:
	var n := 0
	for key: Vector2i in _placed:
		n += (_placed[key] as Array).size()
	return n


## The copies under a new node of `parent` named after the prop: a MultiMeshInstance3D for each
## mesh of the prop in each chunk.
func build(parent: Node3D) -> Node3D:
	var holder := Node3D.new()  # standards: allow nodes_in_code (the copies of a prop)
	holder.name = prop_name.to_pascal_case()
	parent.add_child(holder)
	var source := ArtKit.prop(prop_name)
	for node in source.find_children("*", "MeshInstance3D", true, false):
		var mi := node as MeshInstance3D
		var local := _in_prop(mi, source)
		for key: Vector2i in _placed:
			var list: Array = _placed[key]
			var mm := MultiMesh.new()
			mm.transform_format = MultiMesh.TRANSFORM_3D
			mm.mesh = mi.mesh
			mm.instance_count = list.size()
			for i in list.size():
				mm.set_instance_transform(i, (list[i] as Transform3D) * local)
			var copies := MultiMeshInstance3D.new()  # standards: allow nodes_in_code (a chunk of copies)
			copies.name = "%s_%d_%d" % [mi.name, key.x, key.y]
			copies.multimesh = mm
			copies.material_override = mi.material_override
			copies.cast_shadow = mi.cast_shadow
			holder.add_child(copies)
	source.free()
	return holder


## Where a mesh of the prop is in the prop's own space.
static func _in_prop(mi: MeshInstance3D, source: Node3D) -> Transform3D:
	var place := mi.transform
	var up := mi.get_parent()
	while up != source:
		place = (up as Node3D).transform * place
		up = up.get_parent()
	return place
