extends Node3D
## A person in the new art: the body from characters/<kind>.glb with its weapons, the
## shared clips, the painted material and the ink outline. The model faces +Z.

const ArtKit := preload("res://scripts/art/art_kit.gd")

var kind := ""
var body: Node3D
var skeleton: Skeleton3D
var player: AnimationPlayer
var material: ShaderMaterial
## The clip and play mode shown now (act()).
var shown_clip := ""
var shown_mode := ""
var _hold_until := 0.0
var _speed := 1.0

## A change of clip blends over this many seconds.
const BLEND := 0.08


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


## Hit flash: 1 is the flash colour (white unless given), 0 is the normal colour.
func flash(amount: float, color := Color(1.0, 0.95, 0.85)) -> void:
	material.set_shader_parameter("flash", amount)
	material.set_shader_parameter("flash_color", Vector3(color.r, color.g, color.b))


## The clips move only when advance() is called (the map: a hit holds the picture, the
## pause stops it).
func drive_manually() -> void:
	player.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL


func advance(delta: float) -> void:
	if delta > 0.0:
		player.advance(delta)


## Shows a motion [clip, mode, speed] (scripts/world/motion.gd). duration: the action's length
## in seconds (mode "fit"); restart: the action began (again) now; progress: how far into it
## (0..1) it already is. Walking or standing does not cut off most of a blow, and the fallen
## stay down.
func act(motion: Array, duration := 0.0, restart := false, progress := 0.0) -> void:
	var c: String = motion[0]
	var m: String = motion[1]
	var speed: float = motion[2]
	if player == null or not player.has_animation(c):
		return
	var length := player.get_animation(c).length
	if m == "fit":
		speed = length / maxf(duration, 0.42)
	if m == "loop":
		if c == shown_clip and shown_mode == "loop":
			if absf(speed - _speed) > 0.05:
				_speed = speed
				player.play(c, BLEND, speed)
			return
		if shown_mode != "loop" and player.is_playing() and player.current_animation_position < _hold_until:
			return
		if shown_clip == "death":
			return
	elif not restart and c == shown_clip:
		return
	player.play(c, BLEND, speed)
	player.seek(clampf(progress, 0.0, 1.0) * length if m != "loop" else 0.0, true)
	shown_clip = c
	shown_mode = m
	_speed = speed
	_hold_until = length * 0.8


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
