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
## Pixel art (pixel_view.gd sets it): the camera moves in whole pixels of the world, as big as
## one is where it looks, so the land does not shimmer under it as it goes. pixel_rest is what
## is left over (in those pixels, x to the right, y down), for the view to shift the picture by.
var pixel_snap := false
var pixel_rest := Vector2.ZERO
## Where the camera is on its way, before the snapping.
var _smooth := Vector3.ZERO


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
		_smooth = goal()
		_place()


func _process(delta: float) -> void:
	_smooth = _smooth.lerp(goal(), minf(FOLLOW_SPEED * delta, 1.0))
	_place()


## How big a pixel of the world is where the camera looks (0: not pixel art).
func pixel_world_size() -> float:
	var view := get_viewport() as SubViewport
	if not pixel_snap or view == null or view.size.y <= 0:
		return 0.0
	return 2.0 * distance * tan(deg_to_rad(fov) * 0.5) / view.size.y


func _place() -> void:
	pixel_rest = Vector2.ZERO
	var s := pixel_world_size()
	if s <= 0.0:
		global_position = _smooth
		return
	var right := global_basis.x
	var up := global_basis.y
	var across := _smooth.dot(right) / s
	var along := _smooth.dot(up) / s
	global_position = _smooth + right * (roundf(across) - across) * s + up * (roundf(along) - along) * s
	pixel_rest = Vector2(across - roundf(across), roundf(along) - along)
