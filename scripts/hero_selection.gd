extends Control
## Екран вибору героя (cM[0]==5). cz.aB 0..3; портрети bB.a(38..41) ju_1..ju_4 / char_head1..4.

signal hero_selected(hero_index: int)
signal back_requested

const HERO_COUNT := 4
const PORTRAIT_PATHS := ["res://char_head1.png", "res://char_head2.png", "res://char_head3.png", "res://char_head4.png"]

var _hero_index: int = 0

@onready var _portrait: TextureRect = $Margin/VBox/CenterRow/PortraitWrap/Portrait
@onready var _btn_left: TextureButton = $Margin/VBox/CenterRow/BtnLeft
@onready var _btn_right: TextureButton = $Margin/VBox/CenterRow/BtnRight
@onready var _btn_confirm: Button = $Margin/VBox/BottomRow/BtnConfirm
@onready var _btn_back: Button = $Margin/VBox/BottomRow/BtnBack


func _ready() -> void:
	_hero_index = GameState.hero_index if GameState.hero_index < HERO_COUNT else 0
	_update_portrait()
	_btn_left.pressed.connect(_on_left)
	_btn_right.pressed.connect(_on_right)
	_btn_confirm.pressed.connect(_on_confirm)
	_btn_back.pressed.connect(_on_back)
	_btn_confirm.grab_focus()


func _input(event: InputEvent) -> void:
	if event.is_action_pressed(&"menu_prev") or event.is_action_pressed(&"menu_next"):
		if event.is_action_pressed(&"menu_prev"):
			_on_left()
		else:
			_on_right()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"ui_cancel"):
		_on_back()
		get_viewport().set_input_as_handled()


func process_menu_input(event: InputEvent) -> void:
	if event.is_action_pressed(&"menu_prev"):
		_on_left()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"menu_next"):
		_on_right()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"ui_cancel"):
		_on_back()
		get_viewport().set_input_as_handled()


func _update_portrait() -> void:
	var path: String = PORTRAIT_PATHS[_hero_index] if _hero_index < PORTRAIT_PATHS.size() else PORTRAIT_PATHS[0]
	var tex: Texture2D = load(path) as Texture2D
	if tex != null:
		_portrait.texture = tex
		_portrait.visible = true
	else:
		_portrait.visible = false


func _on_left() -> void:
	_hero_index = (_hero_index - 1 + HERO_COUNT) % HERO_COUNT
	_update_portrait()


func _on_right() -> void:
	_hero_index = (_hero_index + 1) % HERO_COUNT
	_update_portrait()


func _on_confirm() -> void:
	GameState.hero_index = _hero_index
	hero_selected.emit(_hero_index)


func _on_back() -> void:
	back_requested.emit()
