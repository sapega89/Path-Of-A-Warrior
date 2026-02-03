extends Node
## Соответствует глобальным константам и состоянию из ag.java (J2ME).
## VIEW_W/H, TILE, типы экранов (bV), меню (cM[0]).
## Регистрирует действия ввода, если их ещё нет (мобилка → джойстик → клава).

# Разрешение оригинала (QVGA)
const VIEW_W := 240
const VIEW_H := 320
const TILE_SIZE := 27

# Сетка тайлов: в оригинале cb.a x cb.b, видимо 9x9 + запас
const MAP_VISIBLE_COLS := 9
const MAP_VISIBLE_ROWS := 9

# Типы экранов (bV в ag.java): 0=игра, 1=?, 2=меню/карта, 3=бой/диалог
enum ScreenType { GAME, MENU_MAP, BATTLE_DIALOG }
var screen_type: int = ScreenType.GAME

# Индекс меню (cM[0] в e.java): 0=главное, 4=инвентарь, 5=навыки, и т.д.
var menu_index: int = 0

# Текущий уровень (cq)
var current_level: int = 1

# --- Нова гра: герой, складність, ім'я, стати (cz.aB, ag.ep, cz.k, cz.m/n/o/q/F, cz.J) ---
var hero_index: int = 0
var difficulty_index: int = 1  # 0=Hard, 1=Normal (ag.ep, ae.aX, ae.aY)
var player_name: String = ""
var stat_atk: int = 1
var stat_def: int = 1
var stat_hp: int = 5
var stat_mp: int = 3
var stat_fame: int = 0
var stat_points_left: int = 0  # cz.J — очки на розподіл при новій грі

# Позиция камеры в тайлах (cd, ce в ag — смещение тайловой сетки)
var camera_tile_x: int = 0
var camera_tile_y: int = 0

# Смещение камеры в пикселях для плавного скролла (cc.a, cc.b)
var camera_offset_x: int = 0
var camera_offset_y: int = 0

# Имя ресурса тайлов уровня: "1" -> res://1_01.png .. 1_16.png
func get_level_tile_path(level: int, tile_index: int) -> String:
	return "res://%d_%02d.png" % [level, tile_index + 1]

# --- Ввод: гейм-менеджер выбирает источник по устройству ---
# Режим ввода: тач (виртуальный джойстик), геймпад или клавиатура
enum InputMode { TOUCH, GAMEPAD, KEYBOARD }
var input_mode: InputMode = InputMode.KEYBOARD
signal input_mode_changed

# Виртуальный джойстик пишет сюда при input_mode == TOUCH
var touch_move_direction: Vector2 = Vector2.ZERO

func is_mobile_device() -> bool:
	return OS.has_feature("mobile") or OS.has_feature("Android") or OS.has_feature("iOS")

func _ready() -> void:
	_ensure_input_actions()
	detect_input_mode()

func _input(event: InputEvent) -> void:
	# По любому вводу обновляем источник (подключили геймпад / тачнули экран / нажали клавишу)
	update_input_source(event)

func get_input_mode() -> InputMode:
	return input_mode

func detect_input_mode() -> void:
	if is_mobile_device():
		_set_input_mode(InputMode.TOUCH)
		return
	if Input.get_connected_joypads().size() > 0:
		_set_input_mode(InputMode.GAMEPAD)
		return
	_set_input_mode(InputMode.KEYBOARD)

func update_input_source(event: InputEvent) -> void:
	if event is InputEventScreenTouch or event is InputEventScreenDrag:
		_set_input_mode(InputMode.TOUCH)
	elif event is InputEventJoypadMotion or event is InputEventJoypadButton:
		_set_input_mode(InputMode.GAMEPAD)
	elif event is InputEventKey:
		_set_input_mode(InputMode.KEYBOARD)

func _set_input_mode(mode: InputMode) -> void:
	if input_mode == mode:
		return
	if input_mode == InputMode.TOUCH:
		touch_move_direction = Vector2.ZERO
	input_mode = mode
	input_mode_changed.emit()

func _ensure_input_actions() -> void:
	# Если в Project → Input Map уже заданы действия — не трогаем. Иначе добавляем клавиши (джойстик — в редакторе).
	var actions := [
		["move_left", [KEY_A, KEY_LEFT]],
		["move_right", [KEY_D, KEY_RIGHT]],
		["move_up", [KEY_W, KEY_UP]],
		["move_down", [KEY_S, KEY_DOWN]],
		["menu_prev", [KEY_LEFT]],
		["menu_next", [KEY_RIGHT]],
		["menu_confirm", [KEY_ENTER, KEY_KP_ENTER, KEY_SPACE]]
	]
	for a in actions:
		var name_act: String = a[0]
		var keys: Array = a[1]
		if not InputMap.has_action(name_act):
			InputMap.add_action(name_act)
			for k in keys:
				var ev := InputEventKey.new()
				ev.keycode = k
				InputMap.action_add_event(name_act, ev)
			if name_act.begins_with("move_"):
				InputMap.action_set_deadzone(name_act, 0.5)
