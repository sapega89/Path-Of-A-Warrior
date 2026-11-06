extends Camera3D
## The 2.5D camera: fixed angle from above and behind, follows the target smoothly.
## Narrow field of view so the picture looks almost flat (less perspective distortion).

const PITCH_DEG := 35.0  # low enough that the flat sprites are not squashed
const DISTANCE := 13.0  # about one 7x7 room fills the screen, as in the original
const FOLLOW_SPEED := 6.0

var target: Node3D


func _ready() -> void:
	fov = 35.0
	rotation_degrees = Vector3(-PITCH_DEG, 0.0, 0.0)
	snap()


static func offset() -> Vector3:
	var pitch := deg_to_rad(PITCH_DEG)
	return Vector3(0.0, sin(pitch), cos(pitch)) * DISTANCE


func snap() -> void:
	if target != null:
		global_position = target.global_position + offset()


func _process(delta: float) -> void:
	if target == null:
		return
	var goal := target.global_position + offset()
	global_position = global_position.lerp(goal, minf(FOLLOW_SPEED * delta, 1.0))
