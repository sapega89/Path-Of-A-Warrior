extends Control
## Строка меню зі стрілками. Анімація переходу між пунктами; меню в рамці (як у Java ag.e()).

signal item_selected(index: int)

const TRANSITION_DURATION := 0.12

var items: Array[String] = []
var current_index: int = 0

@onready var _btn_left: TextureButton = $Row/LeftWrap/BtnLeft
@onready var _btn_right: TextureButton = $Row/RightWrap/BtnRight
@onready var _btn_select: Button = $Row/BtnSelect
@onready var _left_wrap: Control = $Row/LeftWrap
@onready var _right_wrap: Control = $Row/RightWrap
@onready var _focus_bg: TextureRect = $FocusBg

const ARROW_BOUNCE_PIXELS := 3
const ARROW_BOUNCE_HZ := 2.0

var _anim_t: float = 0.0

func _ready() -> void:
	_btn_left.pressed.connect(_on_left)
	_btn_right.pressed.connect(_on_right)
	_btn_select.pressed.connect(_on_confirm)
	_update_label()

func setup_menu_items(item_list: Array) -> void:
	items.assign(item_list)
	current_index = 0
	_update_label()

func get_current_index() -> int:
	return current_index

func _on_left() -> void:
	if items.is_empty():
		return
	current_index = (current_index - 1 + items.size()) % items.size()
	_play_transition(-1)
	_update_label()

func _on_right() -> void:
	if items.is_empty():
		return
	current_index = (current_index + 1) % items.size()
	_play_transition(1)
	_update_label()

func _play_transition(_direction: int) -> void:
	if _btn_select == null:
		return
	var tween := create_tween()
	tween.set_ease(Tween.EASE_OUT)
	tween.set_trans(Tween.TRANS_QUAD)
	_btn_select.modulate.a = 0.4
	tween.tween_property(_btn_select, "modulate:a", 1.0, TRANSITION_DURATION)

func _on_confirm() -> void:
	item_selected.emit(current_index)

func _update_label() -> void:
	if _btn_select == null or items.is_empty():
		return
	_btn_select.text = items[current_index]

func _process(delta: float) -> void:
	# Плавна анімація стрілок (як у Java ag.dr % 3 * 2, але з sine для плавності)
	if _left_wrap == null or _right_wrap == null:
		return
	_anim_t += delta
	var offset_y := sin(_anim_t * ARROW_BOUNCE_HZ * TAU) * ARROW_BOUNCE_PIXELS
	_left_wrap.position.y = int(offset_y)
	_right_wrap.position.y = int(offset_y)
	# Стиль кнопки: box_01 при фокусі (як у Java)
	if _focus_bg != null and _btn_select != null:
		_focus_bg.visible = _btn_select.has_focus()

## Вызов из Main при клаве/геймпаде на ПК
func process_menu_input(event: InputEvent) -> void:
	if event.is_action_pressed(&"menu_prev"):
		_on_left()
		get_viewport().set_input_as_handled()
	if event.is_action_pressed(&"menu_next"):
		_on_right()
		get_viewport().set_input_as_handled()
	if event.is_action_pressed(&"menu_confirm"):
		_on_confirm()
		get_viewport().set_input_as_handled()
