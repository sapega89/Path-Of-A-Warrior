extends Control
## Рядок меню для титулу: спрайти з M_text, без підложки, тільки стрілки л/п.

signal item_selected(index: int)

const M_TEXT_PATH := "res://M_text.png"
const ARROW_BOUNCE_PIXELS := 3
const ARROW_BOUNCE_HZ := 2.0
const TRANSITION_DURATION := 0.12

var _anim_t: float = 0.0

const MENU_SPRITE_REGIONS := [
	Rect2(0, 21, 116, 21),    # 0: New Game
	Rect2(0, 0, 116, 21),     # 1: Continue (active)
	Rect2(0, 42, 116, 21),    # 2: Options
	Rect2(0, 63, 116, 21),    # 3: Help
	Rect2(0, 84, 116, 21),    # 4: Endings
	Rect2(0, 105, 116, 21),   # 5: About
	Rect2(0, 126, 116, 21),   # 6: More Games
	Rect2(0, 147, 116, 21),   # 7: Multiplayer
	Rect2(0, 168, 116, 21),   # 8: Exit
	Rect2(0, 189, 116, 21)    # 9: Continue (disabled)
]

var _items: Array[String] = []
var _current_index: int = 0
var _m_text_texture: Texture2D

@onready var _btn_left: TextureButton = $Row/LeftWrap/BtnLeft
@onready var _btn_right: TextureButton = $Row/RightWrap/BtnRight
@onready var _sprite_center: TextureRect = $Row/SpriteCenter


func _ready() -> void:
	_m_text_texture = load(M_TEXT_PATH) as Texture2D
	_btn_left.pressed.connect(_on_left)
	_btn_right.pressed.connect(_on_right)
	_update_sprite()


func setup_menu_items(items: Array[String]) -> void:
	_items = items
	_current_index = 0
	_update_sprite()


func process_menu_input(event: InputEvent) -> void:
	if event.is_action_pressed(&"menu_prev"):
		_on_left()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"menu_next"):
		_on_right()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"menu_confirm"):
		item_selected.emit(_current_index)
		get_viewport().set_input_as_handled()


func _on_left() -> void:
	_current_index = (_current_index - 1 + _items.size()) % _items.size()
	_play_transition()
	_update_sprite()


func _on_right() -> void:
	_current_index = (_current_index + 1) % _items.size()
	_play_transition()
	_update_sprite()


func _play_transition() -> void:
	if _sprite_center == null:
		return
	var tween := create_tween()
	tween.set_ease(Tween.EASE_OUT)
	tween.set_trans(Tween.TRANS_QUAD)
	_sprite_center.modulate.a = 0.4
	tween.tween_property(_sprite_center, "modulate:a", 1.0, TRANSITION_DURATION)


func _update_sprite() -> void:
	if _m_text_texture == null or _items.is_empty():
		return
	var region_index: int = _map_item_to_sprite(_current_index)
	if region_index >= 0 and region_index < MENU_SPRITE_REGIONS.size():
		var atlas := AtlasTexture.new()
		atlas.atlas = _m_text_texture
		atlas.region = MENU_SPRITE_REGIONS[region_index]
		_sprite_center.texture = atlas


func _process(delta: float) -> void:
	_anim_t += delta
	var offset_x := sin(_anim_t * ARROW_BOUNCE_HZ * TAU) * ARROW_BOUNCE_PIXELS
	if _btn_left != null:
		_btn_left.position.x = int(-offset_x)
	if _btn_right != null:
		_btn_right.position.x = int(offset_x)


func _map_item_to_sprite(item_index: int) -> int:
	match item_index:
		0: return 0  # Играть -> New Game
		1: return 1  # Продолжить -> Continue (або 9 якщо немає сейву)
		2: return 3  # Help
		3: return 2  # Options
		4: return 4  # Endings
		5: return 5  # Лицензия -> About
		6: return 8  # Выход -> Exit
	return 0
