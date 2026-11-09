class_name FollowCamera
extends Camera3D
## The 2.5D camera: fixed angle from above and behind. It follows a target node, or,
## when there is none, looks at a fixed point (the middle of the current room, as the
## original screen shows one room at a time).
## Narrow field of view so the picture looks almost flat (less perspective distortion).

const PITCH_DEG := 35.0  # low enough that the flat sprites are not squashed
const DISTANCE := 13.0  # about one 7x7 room fills the screen, as in the original
const FOLLOW_SPEED := 6.0

var target: Node3D
## How far back the camera is: DISTANCE, farther where more than a room should show (a camp).
var distance := DISTANCE
## The point to look at when there is no target.
var focus := Vector3.ZERO


func _ready() -> void:
	fov = 35.0
	rotation_degrees = Vector3(-PITCH_DEG, 0.0, 0.0)
	snap()


func offset() -> Vector3:
	var pitch := deg_to_rad(PITCH_DEG)
	return Vector3(0.0, sin(pitch), cos(pitch)) * distance


func goal() -> Vector3:
	return (target.global_position if target != null else focus) + offset()


func snap() -> void:
	if is_inside_tree():
		global_position = goal()


func _process(delta: float) -> void:
	global_position = global_position.lerp(goal(), minf(FOLLOW_SPEED * delta, 1.0))
