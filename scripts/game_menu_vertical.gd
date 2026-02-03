extends Control
## Ігрове меню вертикальне (Java: e.java aJ, bA.a(66+cM[1])=m_illu, txt_m/txt_b, ui_arrow_menu vertical).

signal item_selected(index: int)
signal back_requested

const MENU_LABELS := ["Mission", "Blacksmith", "Gamevil Live", "Visiting", "Management", "ETC"]
const TXT_M_PATH := "res://txt_m.png"
const TXT_B_PATH := "res://txt_b.png"
const ILLU_PATHS := [
	"res://m_illu1.png", "res://m_illu2.png", "res://m_illu3.png",
	"res://m_illu4.png", "res://m_illu5.png", "res://m_illu6.png"
]
## txt_m: 94x18 per row (selected), txt_b: 62x11 per row (prev/next)
const TXT_M_W := 94
const TXT_M_H := 18
const TXT_B_W := 62
const TXT_B_H := 11

var _current_index: int = 0
var _txt_m_texture: Texture2D
var _txt_b_texture: Texture2D

@onready var _illustration: TextureRect = $MainLayer/MenuFrame/Illustration
@onready var _item0: TextureRect = $MainLayer/MenuFrame/ItemsVBox/Row0/Item0Wrap/Item0
@onready var _item1: TextureRect = $MainLayer/MenuFrame/ItemsVBox/Row1/Item1Wrap/Item1
@onready var _item2: TextureRect = $MainLayer/MenuFrame/ItemsVBox/Row2/Item2Wrap/Item2
@onready var _arrow_up: TextureRect = $MainLayer/MenuFrame/ItemsVBox/ArrowUpWrap/ArrowUp
@onready var _arrow_down: TextureRect = $MainLayer/MenuFrame/ItemsVBox/ArrowDownWrap/ArrowDown
@onready var _arrow_down1: TextureRect = $MainLayer/MenuFrame/ItemsVBox/Row1/ArrowDown1Wrap/ArrowDown1
@onready var _back_btn: Button = $MainLayer/BackBtnWrap/BackBtn
@onready var _arrow_up_wrap: Control = $MainLayer/MenuFrame/ItemsVBox/ArrowUpWrap
@onready var _arrow_down_wrap: Control = $MainLayer/MenuFrame/ItemsVBox/ArrowDownWrap
@onready var _arrow_down1_wrap: Control = $MainLayer/MenuFrame/ItemsVBox/Row1/ArrowDown1Wrap
@onready var _row0: Control = $MainLayer/MenuFrame/ItemsVBox/Row0
@onready var _row1: Control = $MainLayer/MenuFrame/ItemsVBox/Row1
@onready var _row2: Control = $MainLayer/MenuFrame/ItemsVBox/Row2
@onready var _items_vbox: Control = $MainLayer/MenuFrame/ItemsVBox

const ARROW_BOUNCE_PIXELS := 2
const ARROW_BOUNCE_HZ := 2.0
## Java bf(): вниз — swap Y рядків 1 і 2 (середній опускається, нижній піднімається); вгору — рядки піднімаються
const ROW0_BASE_Y := 0
const ROW1_BASE_Y := 49
const ROW2_BASE_Y := 108
## Плавна анімація ковзання
const CAROUSEL_SLIDE_DURATION := 0.22
var _anim_t: float = 0.0

## Карусель як у Java (e.java bf): Tween замість _process
var _carousel_direction: int = 0  # 1=вниз, -1=вгору
var _carousel_step: int = 0

func _ready() -> void:
	_txt_m_texture = load(TXT_M_PATH) as Texture2D
	_txt_b_texture = load(TXT_B_PATH) as Texture2D
	_back_btn.pressed.connect(_on_back)
	## Java e.java: UP (-1) → aB(), DOWN (-2) → aC(); + клік по стрілках
	_setup_arrow_click(_arrow_up_wrap, -1)
	_setup_arrow_click(_arrow_down_wrap, 1)
	_setup_arrow_click(_arrow_down1_wrap, 1)
	_update_display()

func _setup_arrow_click(ctrl: Control, dir: int) -> void:
	if ctrl == null:
		return
	ctrl.mouse_filter = Control.MOUSE_FILTER_STOP
	ctrl.gui_input.connect(_on_arrow_gui_input.bind(dir))

func _on_arrow_gui_input(event: InputEvent, dir: int) -> void:
	if event is InputEventMouseButton:
		var mb := event as InputEventMouseButton
		if mb.button_index == MOUSE_BUTTON_LEFT and mb.pressed:
			_start_carousel(dir)
			get_viewport().set_input_as_handled()

func setup_menu_items(_items: Array) -> void:
	pass

func get_current_index() -> int:
	return _current_index

func process_menu_input(event: InputEvent) -> void:
	if _carousel_direction != 0:
		return
	## Java e.java 259-266: ag.ch -1/50 → aB() (вгору), -2/56 → aC() (вниз)
	var prev := event.is_action_pressed(&"menu_prev") or event.is_action_pressed(&"ui_up")
	var next := event.is_action_pressed(&"menu_next") or event.is_action_pressed(&"ui_down")
	if prev:
		_start_carousel(-1)
		get_viewport().set_input_as_handled()
	elif next:
		_start_carousel(1)
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"menu_confirm"):
		item_selected.emit(_current_index)
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"ui_cancel"):
		_on_back()
		get_viewport().set_input_as_handled()

func _start_carousel(dir: int) -> void:
	_carousel_direction = dir
	_carousel_step = 0
	## Стрілки ховаємо одразу в цьому ж кадрі — без анімації, щоб не було помітних кадрів
	_hide_arrows()
	_reset_row_positions()
	## Вниз: верхній (prev) не видно. Вгору: нижній (next) не видно — дзеркально до вниз
	if dir == 1 and _row0 != null:
		_row0.visible = false
	if dir == -1 and _row2 != null:
		_row2.visible = false
	_update_display()
	var tween := create_tween()
	tween.set_ease(Tween.EASE_IN_OUT)
	tween.set_trans(Tween.TRANS_SINE)
	## Java bf(): вниз — середній ряд опускається вниз, нижній піднімається (swap Y). Вгору — рядки піднімаються вгору.
	## Анімація вниз (dir == 1) — ідеальна, зафіксована: Row0 прихований, Row1/Row2 swap Y, не змінювати.
	if dir == 1:
		if _row1 != null:
			tween.tween_property(_row1, "position:y", float(ROW2_BASE_Y), CAROUSEL_SLIDE_DURATION)
		if _row2 != null:
			tween.parallel().tween_property(_row2, "position:y", float(ROW1_BASE_Y), CAROUSEL_SLIDE_DURATION)
	else:
		## Вгору: так само як вниз, тільки вгору — swap Row0 і Row1 (верхній їде вниз, середній вгору)
		if _row0 != null:
			tween.tween_property(_row0, "position:y", float(ROW1_BASE_Y), CAROUSEL_SLIDE_DURATION)
		if _row1 != null:
			tween.parallel().tween_property(_row1, "position:y", float(ROW0_BASE_Y), CAROUSEL_SLIDE_DURATION)
	tween.tween_callback(func():
		var n := MENU_LABELS.size()
		if _carousel_direction == 1:
			_current_index = (_current_index + 1) % n
		else:
			_current_index = (_current_index - 1 + n) % n
		_carousel_direction = 0
		_carousel_step = 0
		_reset_row_positions()
		if _row0 != null:
			_row0.visible = true
		if _row2 != null:
			_row2.visible = true
		_show_arrows()
		_update_display()
	)

func _hide_arrows() -> void:
	if _arrow_up_wrap != null:
		_arrow_up_wrap.visible = false
	if _arrow_down_wrap != null:
		_arrow_down_wrap.visible = false
	if _arrow_down1_wrap != null:
		_arrow_down1_wrap.visible = false

func _show_arrows() -> void:
	if _arrow_up_wrap != null:
		_arrow_up_wrap.visible = true
	if _arrow_down_wrap != null:
		_arrow_down_wrap.visible = true
	if _arrow_down1_wrap != null:
		_arrow_down1_wrap.visible = true

func _reset_row_positions() -> void:
	if _row0 != null:
		_row0.position.y = ROW0_BASE_Y
	if _row1 != null:
		_row1.position.y = ROW1_BASE_Y
	if _row2 != null:
		_row2.position.y = ROW2_BASE_Y

func _update_display() -> void:
	var n := MENU_LABELS.size()
	var i0 := (_current_index - 1 + n) % n
	var i1 := _current_index
	var i2 := (_current_index + 1) % n
	## Контент не міняється під час ковзання; після tween оновлюємо індекс і _update_display()
	_update_rows(i0, i1, i2, _carousel_step, _carousel_direction)
	if _illustration != null and _current_index < ILLU_PATHS.size():
		var tex := load(ILLU_PATHS[_current_index]) as Texture2D
		if tex != null:
			_illustration.texture = tex

func _update_rows(i0: int, i1: int, i2: int, _step: int, _dir: int) -> void:
	_update_region(_item0, i0, TXT_B_W, TXT_B_H, _txt_m_texture)
	_update_region(_item1, i1, TXT_M_W, TXT_M_H, _txt_b_texture)
	_update_region(_item2, i2, TXT_B_W, TXT_B_H, _txt_m_texture)

## Оновлює тільки ряд (idx) в атласі; зберігає position/size зі сцени якщо є
func _update_region(rect: TextureRect, idx: int, w: int, h: int, atlas_tex: Texture2D) -> void:
	if rect == null or atlas_tex == null:
		return
	var existing := rect.texture as AtlasTexture
	var region: Rect2
	if existing != null and existing.atlas == atlas_tex:
		var rh := int(existing.region.size.y)
		region = Rect2(existing.region.position.x, idx * rh, existing.region.size.x, existing.region.size.y)
	else:
		region = Rect2(0, idx * h, w, h)
	var atlas := AtlasTexture.new()
	atlas.atlas = atlas_tex
	atlas.region = region
	rect.texture = atlas

func _process(delta: float) -> void:
	_anim_t += delta
	var offset_y := sin(_anim_t * ARROW_BOUNCE_HZ * TAU) * ARROW_BOUNCE_PIXELS
	if _arrow_up != null:
		_arrow_up.position.y = int(-offset_y)
	if _arrow_down != null:
		_arrow_down.position.y = int(offset_y)
	if _arrow_down1 != null:
		_arrow_down1.position.y = int(offset_y)

func _on_back() -> void:
	back_requested.emit()
