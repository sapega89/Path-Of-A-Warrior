class_name Hero
extends CharacterBody3D
## The hero: the original 2D sprite standing in the 3D world (decisions 06.11:
## "3D world, 2D hero", "move the game over as it is first").
##
## The frames come from assets/original/hero_<head>_<weapon>.png, made by
## godot/tools/import_original.py from the original body, head and weapon parts.
## The sprite turns to the camera around the vertical axis (Y billboard), so it
## stays flat to the screen but is sorted, lit and shadowed in 3D.
## Directions and the idle / walk tables are the original ones (hero.json).

signal attacked

const SHEET_PATH := "res://assets/original/hero_%d_%d.png"
const SKILL_SHEET_PATH := "res://assets/original/hero_%d_%d_sk.png"
const INFO_PATH := "res://assets/original/hero.json"
const SPEED := 4.0  # tiles per second
const GRAVITY := 20.0
## World units per sprite pixel: one original 27 px tile is one world unit.
const PIXEL_SIZE := 1.0 / 27.0
const FRAME_TIME := 0.1
const LOOP := 222  # end-of-table marker of the original animation tables
const FLASH_TIME := 0.15
const FLASH_COLOR := Color(1.6, 1.5, 1.2)

## Pixels of the sprite below the actor's position that still stand on the ground
## (the original's body box reaches 6 px below the position).
const FOOT_PX := 6

## Original 8-direction: 0 down, 2 left, 4 up, 6 right (clockwise on screen).
var dir8 := 0
## Driven by the map simulation (set_frame / world position) instead of reading the input.
var external := false
var walking := false
var sprite: Sprite3D
var info := {}
var _anim_pos := 0
var _anim_time := 0.0
var _flash := 0.0
var _base: Texture2D
var _skill: Texture2D
var _showing_skill := false


func _ready() -> void:
	var shape := CollisionShape3D.new()
	var capsule := CapsuleShape3D.new()
	capsule.radius = 0.3
	capsule.height = 1.2
	shape.shape = capsule
	shape.position.y = 0.6
	add_child(shape)

	info = load_info()
	sprite = Sprite3D.new()
	sprite.name = "Sprite"
	_base = load(SHEET_PATH % [0, 0])
	_skill = load(SKILL_SHEET_PATH % [0, 0])
	sprite.texture = _base
	sprite.region_enabled = true
	sprite.pixel_size = PIXEL_SIZE
	sprite.billboard = BaseMaterial3D.BILLBOARD_FIXED_Y
	sprite.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
	sprite.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD  # sharp edges, correct depth, casts a shadow
	sprite.shaded = true
	# The sprite is centred on its cell; the feet are (origin - cell / 2) px below the middle.
	var cell: Array = info.get("cell", [96, 96])
	var origin: Array = info.get("origin", [48, 72])
	sprite.position.y = (float(origin[1]) - float(cell[1]) / 2.0 + FOOT_PX) * PIXEL_SIZE
	add_child(sprite)
	_show_frame(current_frame())


static func load_info() -> Dictionary:
	var f := FileAccess.open(INFO_PATH, FileAccess.READ)
	if f == null:
		return {}
	var data: Variant = JSON.parse_string(f.get_as_text())
	return data if typeof(data) == TYPE_DICTIONARY else {}


## Uses another head (0..3) and weapon (sword type 0 or 1, the weapon's slot type) sheet.
func set_look(head: int, weapon: int) -> void:
	var tex: Texture2D = load(SHEET_PATH % [head, weapon])
	if tex != null:
		_base = tex
		_skill = load(SKILL_SHEET_PATH % [head, weapon])
		sprite.texture = _skill if _showing_skill else _base


## Input as a 2D vector (x = right, y = down on screen), length 0..1.
static func read_move() -> Vector2:
	return Input.get_vector("move_left", "move_right", "move_up", "move_down")


## Screen-space input to a direction on the floor. The camera looks along -Z,
## so "up" on screen is -Z in the world.
static func to_world(move: Vector2) -> Vector3:
	return Vector3(move.x, 0.0, move.y)


## Screen direction to the original 8-direction (0 down, 2 left, 4 up, 6 right).
static func dir8_of(move: Vector2) -> int:
	var a := atan2(-move.x, move.y)
	return posmod(roundi(a / (PI / 4.0)), 8)


## Original pixel position to the world (the feet: 6 px below the position).
static func px_to_world(p: Vector2) -> Vector3:
	return Vector3(p.x / 27.0, 0.0, (p.y + FOOT_PX) / 27.0)


## Shows a frame of the sheet (used when the simulation drives the hero); skill: a frame
## of the skill sheet (actions 12 and up).
func set_frame(frame: int, skill: bool = false) -> void:
	if skill != _showing_skill:
		_showing_skill = skill
		sprite.texture = _skill if skill else _base
		var cell: Array = info.get("skill_cell" if skill else "cell", [96, 96])
		var origin: Array = info.get("skill_origin" if skill else "origin", [48, 72])
		sprite.position.y = (float(origin[1]) - float(cell[1]) / 2.0 + FOOT_PX) * PIXEL_SIZE
	_show_frame(frame)


func _physics_process(delta: float) -> void:
	if external:
		return
	step(read_move(), delta)
	if Input.is_action_just_pressed("attack"):
		attack()
	_animate(delta)
	if _flash > 0.0:
		_flash = maxf(_flash - delta, 0.0)
		sprite.modulate = Color.WHITE.lerp(FLASH_COLOR, _flash / FLASH_TIME)


## One movement step; split out so tests can drive it without real input.
func step(move: Vector2, delta: float) -> void:
	var dir := to_world(move)
	velocity.x = dir.x * SPEED
	velocity.z = dir.z * SPEED
	velocity.y = 0.0 if is_on_floor() else velocity.y - GRAVITY * delta
	var was_walking := walking
	walking = move.length() > 0.1
	if walking:
		var d := dir8_of(move)
		if d != dir8 or not was_walking:
			_anim_pos = 0
			_anim_time = 0.0
		dir8 = d
	elif was_walking:
		_anim_pos = 0
	move_and_slide()


## The original table (idle or walk) for the current direction.
func current_table() -> Array:
	var map4: Array = info.get("dir8_to_dir4", [0, 1, 1, 1, 2, 3, 3, 3])
	var dir4: int = int(map4[dir8])
	var tables: Array = info.get("walk" if walking else "idle", [])
	return tables[dir4] if dir4 < tables.size() else [0, LOOP]


func current_frame() -> int:
	var table := current_table()
	if _anim_pos >= table.size() or int(table[_anim_pos]) == LOOP:
		_anim_pos = 0
	return int(table[_anim_pos])


func _animate(delta: float) -> void:
	_anim_time += delta
	while _anim_time >= FRAME_TIME:
		_anim_time -= FRAME_TIME
		_anim_pos += 1
	_show_frame(current_frame())


func _show_frame(frame: int) -> void:
	var cell: Array = info.get("skill_cell" if _showing_skill else "cell", [96, 96])
	var cols: int = int(info.get("columns", 16))
	var cw := float(cell[0])
	var ch := float(cell[1])
	sprite.region_rect = Rect2((frame % cols) * cw, (frame / cols) * ch, cw, ch)


func attack() -> void:
	_flash = FLASH_TIME
	attacked.emit()
