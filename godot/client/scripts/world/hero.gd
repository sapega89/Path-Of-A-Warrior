class_name Hero
extends CharacterBody3D
## The hero's body in the 3D world (scenes/world/hero.tscn): it walks with the input (or is
## moved by the screen when `external`), collides with the walls and turns to where it goes.
## What the player sees is the figure of the new art under it (ArtFigure), which the screen
## plays and turns by `walking` and `dir8`.

signal attacked

const SPEED := 4.0  # tiles per second
const GRAVITY := 20.0
## World units per map pixel: one 27 px tile is one world unit.
const PIXEL_SIZE := 1.0 / 27.0
## Pixels below an actor's position that still stand on the ground (its body box reaches this
## far below the position).
const FOOT_PX := 6

## The 8-direction: 0 down, 2 left, 4 up, 6 right (clockwise on screen).
var dir8 := 0
## Driven by the screen (world position) instead of reading the input.
var external := false
var walking := false


## Input as a 2D vector (x = right, y = down on screen), length 0..1.
static func read_move() -> Vector2:
	return Input.get_vector("move_left", "move_right", "move_up", "move_down")


## Screen-space input to a direction on the floor. The camera looks along -Z,
## so "up" on screen is -Z in the world.
static func to_world(move: Vector2) -> Vector3:
	return Vector3(move.x, 0.0, move.y)


## Screen direction to the 8-direction (0 down, 2 left, 4 up, 6 right).
static func dir8_of(move: Vector2) -> int:
	var a := atan2(-move.x, move.y)
	return posmod(roundi(a / (PI / 4.0)), 8)


## A map pixel position to the world (the feet: FOOT_PX below the position).
static func px_to_world(p: Vector2) -> Vector3:
	return Vector3(p.x / 27.0, 0.0, (p.y + FOOT_PX) / 27.0)


## A step every frame, not every physics tick, so the walk is smooth at any refresh rate (60
## steps a second on a 144 Hz screen would move him in jerks); move_and_slide() takes the
## frame's delta here.
func _process(delta: float) -> void:
	if external:
		return
	step(read_move(), delta)
	if Input.is_action_just_pressed("attack"):
		attack()


## One movement step; split out so tests can drive it without real input.
func step(move: Vector2, delta: float) -> void:
	var dir := to_world(move)
	velocity.x = dir.x * SPEED
	velocity.z = dir.z * SPEED
	velocity.y = 0.0 if is_on_floor() else velocity.y - GRAVITY * delta
	walking = move.length() > 0.1
	if walking:
		dir8 = dir8_of(move)
	move_and_slide()


func attack() -> void:
	attacked.emit()
