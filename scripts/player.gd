extends CharacterBody2D
## Персонаж: движение по сетке 27px, 4 направления. Соответствует cz (n.java), позиция в пикселях.

const TILE := GameState.TILE_SIZE
const VIEW_W := GameState.VIEW_W
const VIEW_H := GameState.VIEW_H
const MOVE_SPEED := 90.0

@onready var sprite: Sprite2D = $Sprite2D

func _ready() -> void:
	# Ноги героя в позиції ноди (один спрайт — повне тіло, як у Java ct[40+cz.K] = wep_long)
	if sprite.texture != null:
		var sz := sprite.texture.get_size()
		sprite.position = Vector2(-sz.x * 0.5, -sz.y)
		sprite.centered = false
	# Старт в центре экрана в мировых координатах
	position = Vector2(VIEW_W / 2.0, VIEW_H / 2.0)

func _physics_process(_delta: float) -> void:
	# Источник ввода выбирает гейм-менеджер (TOUCH / GAMEPAD / KEYBOARD)
	var dir := Vector2.ZERO
	if GameState.get_input_mode() == GameState.InputMode.TOUCH:
		dir = GameState.touch_move_direction
	else:
		dir.x = Input.get_axis(&"move_left", &"move_right")
		dir.y = Input.get_axis(&"move_up", &"move_down")
	if dir != Vector2.ZERO:
		dir = dir.normalized()
		# Поворот спрайта по направлению (как в оригинале — 4 стороны)
		if abs(dir.x) >= abs(dir.y):
			sprite.flip_h = dir.x < 0
	velocity = dir * MOVE_SPEED
	move_and_slide()
