extends Control
## Екран вибору героя. Shell налаштований у сцені; карусель додана в LinksVBox.
## Великі портрети bB.a(38..41) = ju_1..ju_4.

signal hero_selected(hero_index: int)
signal back_requested

const HERO_COUNT := 4
const PORTRAIT_PATHS := [
	"res://ju_1.png", "res://ju_2.png",
	"res://ju_3.png", "res://ju_4.png"
]

var _hero_index: int = 0

@onready var _shell: Control = $SubmenuShell
@onready var _portrait_left: TextureButton = $SubmenuShell/MainLayer/MenuFrame/LinksVBox/PortraitRow/PortraitLeft
@onready var _portrait_center: TextureButton = $SubmenuShell/MainLayer/MenuFrame/LinksVBox/PortraitRow/PortraitCenter
@onready var _portrait_right: TextureButton = $SubmenuShell/MainLayer/MenuFrame/LinksVBox/PortraitRow/PortraitRight
@onready var _btn_left: TextureButton = $SubmenuShell/MainLayer/MenuFrame/LinksVBox/PortraitRow/BtnLeft
@onready var _btn_right: TextureButton = $SubmenuShell/MainLayer/MenuFrame/LinksVBox/PortraitRow/BtnRight


func _ready() -> void:
	_shell.set_title("CHARACTER")
	_shell.back_pressed.connect(func() -> void: back_requested.emit())
	_hero_index = GameState.hero_index if GameState.hero_index < HERO_COUNT else 0
	_update_portraits()
	_portrait_left.pressed.connect(_on_left)
	_portrait_center.pressed.connect(_on_confirm)
	_portrait_right.pressed.connect(_on_right)
	_btn_left.pressed.connect(_on_left)
	_btn_right.pressed.connect(_on_right)


func _input(event: InputEvent) -> void:
	if event.is_action_pressed(&"menu_prev"):
		_on_left()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"menu_next"):
		_on_right()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"menu_confirm"):
		_on_confirm()
		get_viewport().set_input_as_handled()


func _update_portraits() -> void:
	var prev := (_hero_index - 1 + HERO_COUNT) % HERO_COUNT
	var next := (_hero_index + 1) % HERO_COUNT
	_set_portrait(_portrait_left, prev)
	_set_portrait(_portrait_center, _hero_index)
	_set_portrait(_portrait_right, next)


func _set_portrait(rect: TextureButton, index: int) -> void:
	rect.texture_normal = load(PORTRAIT_PATHS[index]) as Texture2D


func _on_left() -> void:
	_hero_index = (_hero_index - 1 + HERO_COUNT) % HERO_COUNT
	_update_portraits()


func _on_right() -> void:
	_hero_index = (_hero_index + 1) % HERO_COUNT
	_update_portraits()


func _on_confirm() -> void:
	GameState.hero_index = _hero_index
	hero_selected.emit(_hero_index)
