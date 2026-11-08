extends Node3D
## A person in the new art: the body from characters/<kind>.glb with its weapons, the
## shared clips, the painted material and the ink outline. The model faces +Z.

const ArtKit := preload("res://scripts/art/art_kit.gd")

var kind := ""
var body: Node3D
var skeleton: Skeleton3D
var player: AnimationPlayer
var material: ShaderMaterial


func setup(figure_kind: String) -> Node3D:
	kind = figure_kind
	body = ArtKit.scene("characters/%s.glb" % kind).instantiate()
	add_child(body)
	skeleton = body.find_child("Skeleton3D", true, false) as Skeleton3D
	material = ArtKit.painted(true)
	ArtKit.dress(body, material)
	player = AnimationPlayer.new()
	player.name = "Clips"
	body.add_child(player)
	player.root_node = NodePath("..")
	player.add_animation_library(&"", ArtKit.clips())
	return self


func play(clip: String, blend := 0.15, speed := 1.0) -> void:
	if player != null and player.has_animation(clip):
		player.play(clip, blend, speed)


## Shows the clip at a given second, for still pictures.
func pose(clip: String, at: float) -> void:
	play(clip, 0.0)
	player.seek(at, true)
	player.pause()


func face(direction: Vector3) -> void:
	if direction.length_squared() > 0.0001:
		rotation.y = atan2(direction.x, direction.z)


func look_at_point(point: Vector3) -> void:
	face(point - global_position)


## Hit flash: 1 is white, 0 is the normal colour.
func flash(amount: float) -> void:
	material.set_shader_parameter("flash", amount)


## Puts a weapon from characters/weapons.glb into the hand it belongs to.
func equip(weapon: String) -> void:
	var source: Node = ArtKit.scene("characters/weapons.glb").instantiate()
	var mesh := source.find_child(weapon, true, false) as MeshInstance3D
	if mesh != null:
		var holder := mesh.get_parent() as BoneAttachment3D
		var attach := BoneAttachment3D.new()
		attach.bone_name = holder.bone_name
		skeleton.add_child(attach)
		var copy := MeshInstance3D.new()
		copy.name = weapon
		copy.mesh = mesh.mesh
		copy.transform = mesh.transform
		copy.material_override = material
		attach.add_child(copy)
	source.free()


## Hides the weapons the model came with (the ones under bone attachments).
func unequip_all() -> void:
	for attach in skeleton.find_children("*", "BoneAttachment3D", true, false):
		attach.queue_free()
