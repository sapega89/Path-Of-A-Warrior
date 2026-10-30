extends CanvasLayer
## Виртуальный джойстик. Показывается только когда гейм-менеджер выбрал режим TOUCH.
## Пишет в GameState.touch_move_direction; игрок читает оттуда.

const PAD_MARGIN := 24
const BUTTON_SIZE := 48

var _pressed_left := false
var _pressed_right := false
var _pressed_up := false
var _pressed_down := false

@onready var _btn_left: TextureButton = $PadLeft
@onready var _btn_right: TextureButton = $PadRight
@onready var _btn_up: Button = $PadUp
@onready var _btn_down: Button = $PadDown

func _ready() -> void:
	_place_buttons()
	_connect_buttons()
	_update_visibility()
	GameState.input_mode_changed.connect(_update_visibility)

func _update_visibility() -> void:
	visible = GameState.get_input_mode() == GameState.InputMode.TOUCH

func _place_buttons() -> void:
	var h := get_viewport().get_visible_rect().size.y
	# Левая половина экрана — D-pad: 4 кнопки в сетке 2x2
	var cx := PAD_MARGIN + BUTTON_SIZE
	var cy := h - PAD_MARGIN - BUTTON_SIZE * 1.5
	_btn_left.position = Vector2(cx - BUTTON_SIZE - 4, cy)
	_btn_right.position = Vector2(cx + 4, cy)
	_btn_up.position = Vector2(cx - BUTTON_SIZE / 2.0 - 2, cy - BUTTON_SIZE - 4)
	_btn_down.position = Vector2(cx - BUTTON_SIZE / 2.0 - 2, cy + 4)
	_btn_left.size = Vector2(BUTTON_SIZE, BUTTON_SIZE)
	_btn_right.size = Vector2(BUTTON_SIZE, BUTTON_SIZE)
	_btn_up.size = Vector2(BUTTON_SIZE, BUTTON_SIZE)
	_btn_down.size = Vector2(BUTTON_SIZE, BUTTON_SIZE)

func _connect_buttons() -> void:
	_btn_left.button_down.connect(_on_left_down)
	_btn_left.button_up.connect(_on_left_up)
	_btn_right.button_down.connect(_on_right_down)
	_btn_right.button_up.connect(_on_right_up)
	_btn_up.button_down.connect(_on_up_down)
	_btn_up.button_up.connect(_on_up_up)
	_btn_down.button_down.connect(_on_down_down)
	_btn_down.button_up.connect(_on_down_up)

func _on_left_down() -> void:  _pressed_left = true
func _on_left_up() -> void:    _pressed_left = false
func _on_right_down() -> void: _pressed_right = true
func _on_right_up() -> void:  _pressed_right = false
func _on_up_down() -> void:   _pressed_up = true
func _on_up_up() -> void:     _pressed_up = false
func _on_down_down() -> void: _pressed_down = true
func _on_down_up() -> void:   _pressed_down = false

func _process(_delta: float) -> void:
	if not visible:
		return
	var v := Vector2.ZERO
	if _pressed_left:  v.x -= 1.0
	if _pressed_right: v.x += 1.0
	if _pressed_up:    v.y -= 1.0
	if _pressed_down:  v.y += 1.0
	GameState.touch_move_direction = v.normalized() if v != Vector2.ZERO else Vector2.ZERO

func _exit_tree() -> void:
	GameState.touch_move_direction = Vector2.ZERO
