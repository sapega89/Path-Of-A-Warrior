extends CharacterBody2D
## Player: movement (arrows / WASD), 27px grid-aligned like original.

const TILE_SIZE := 27
const MOVE_SPEED := 120.0

func _physics_process(delta: float) -> void:
	var dir := Vector2.ZERO
	dir.x = Input.get_axis(&"ui_left", &"ui_right")
	dir.y = Input.get_axis(&"ui_up", &"ui_down")
	if dir != Vector2.ZERO:
		dir = dir.normalized()
	velocity = dir * MOVE_SPEED
	move_and_slide()
