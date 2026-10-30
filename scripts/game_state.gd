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

# --- Visiting: тільки генерали, які вже запросили гравця (логіка з Java, DESIGN §6.4.1) ---
const GENERALS_COUNT := 37
var general_invited: Array[bool] = []
var general_relationship: Array[int] = []
var general_names: Array[String] = []

# Чи дозволено візити зараз (напр. false до завершення місії — Punct 9)
var can_visit_generals: bool = true

# Mission: обрана місія та лорд (Java: dm = mission index, dk = lord index).
# «За якого лорда йду» = selected_lord_id (індекс) + player_lord_id (id для карти); карта й спавн залежать від лорда — див. JAVA_REFERENCE.md §7e.
var selected_mission_id: int = -1
var selected_lord_id: int = -1
var selected_battle_general_id: int = -1
## Id лорда для завантаження карти (Java ds[dk]): одна карта на лорда, bF.a(ds[dk]-1). При вході в місію ставити = selected_lord_id + 1 або з таблиці lord_index → map_id.
var player_lord_id: int = 1

# Лорди для місій — це НЕ генерали (Java: C() завантажує з v(48)=mission.arr; dt[] — імена, ds[] — id, до 6 на главу).
# Генерали = Visiting (37, jang_*); лорди/правителі = mission.arr, окремі особистості.
# Зв'язок «лорд → його генерали» у Java явно не знайдено (ймовірно колонка в general.arr або окремий дата-файл); див. JAVA_REFERENCE.md §7d.
# На полі бою з'являються лише генерали НЕ поточного лорда (вороги/союзники — це генерали інших лордів).
const LORDS_MAX := 6
var lord_unlocked: Array[bool] = []
var lord_names: Array[String] = []  # dt[] з mission.arr; для першої глави 4 лорди
## Для кожного індексу лорда (0..lords_count_in_chapter-1) — масив id генералів, які належать цьому лорду.
## Заповнюється в _init_lord_generals(); на полі бою використовувати лише генералів з get_general_ids_allowed_on_battlefield().
var lord_generals: Array[Array] = []  # Array[Array] — кожен елемент Array[int] (general id 0..GENERALS_COUNT-1)

# Глава/регіон (Java cq): j = 38*cq+40 у v(48); для cq=0 — перша глава: 1 місія, 4 лорди
var mission_chapter: int = 0
var missions_count_in_chapter: int = 1  # для cq=0 у першій місії одна доступна місія
var lords_count_in_chapter: int = 4     # для cq=0 — чотири лорди

# Назви місій (Java: dA[] з v(55)=ruler.arr, 3+((dz[b]).a-1)*15). Індекс = mission_index у межах глави.
var mission_names: Array[String] = []

# Яка місія за якою доступна (Java: dy[] — біти (ds[dk]-1)*5+dm). Місія 0 завжди доступна; місія i — після завершення i-1 для цього лорда.
var mission_completed: Array[Array] = []  # mission_completed[lord_index][mission_index] == true

# Позиция камеры в тайлах (cd, ce в ag — смещение тайловой сетки). Спавн гравця на карті залежить від лорда (Java: cz.a[0], cz.b[0] → cd, ce).
var camera_tile_x: int = 0
var camera_tile_y: int = 0
## Точка спавну на карті по лордах (тайлові координати). Індекс = індекс лорда; при вході на карту встановити camera_tile_* з цих значень.
var spawn_tile_per_lord: Array[Vector2i] = []  # [Vector2i(4, 4), ...] — placeholder по одному на лорда

# Смещение камеры в пикселях для плавного скролла (cc.a, cc.b)
var camera_offset_x: int = 0
var camera_offset_y: int = 0

# Имя ресурса тайлов уровня: "1" -> res://1_01.png .. 1_16.png
func get_level_tile_path(level: int, tile_index: int) -> String:
	return "res://%d_%02d.png" % [level, tile_index + 1]

# --- Поле бою: лише генерали НЕ поточного лорда ---

## Повертає true, якщо генерал з id [general_id] належить лорду [lord_index].
func is_general_of_lord(general_id: int, lord_index: int) -> bool:
	if lord_index < 0 or lord_index >= lord_generals.size():
		return false
	var ids: Array = lord_generals[lord_index]
	for i in range(ids.size()):
		if ids[i] == general_id:
			return true
	return false

## Генерали, які можуть з'явитися на полі бою: усі, крім генералів обраного лорда (selected_lord_id).
## Якщо лорд не обраний (-1), повертаються усі id (0..GENERALS_COUNT-1).
func get_general_ids_allowed_on_battlefield() -> Array[int]:
	var allowed: Array[int] = []
	for gid in range(GENERALS_COUNT):
		if selected_lord_id < 0:
			allowed.append(gid)
		elif not is_general_of_lord(gid, selected_lord_id):
			allowed.append(gid)
	return allowed

# --- Назви місій і флоу доступності (Java: dA[], dy[]) ---

## Повертає назву місії за індексом у межах глави. Якщо нема в списку — "Mission N".
func get_mission_name(mission_index: int) -> String:
	if mission_index >= 0 and mission_index < mission_names.size() and mission_names[mission_index] != "":
		return mission_names[mission_index]
	return "Mission %d" % (mission_index + 1)

## Чи доступна місія [mission_index] для лорда [lord_index]. Місія 0 завжди так; далі — після завершення попередньої.
func is_mission_available(lord_index: int, mission_index: int) -> bool:
	if mission_index <= 0:
		return true
	if lord_index < 0 or lord_index >= mission_completed.size():
		return true
	var completed: Array = mission_completed[lord_index]
	if mission_index - 1 >= completed.size():
		return true
	return completed[mission_index - 1] == true

## Позначити місію як завершену для лорда (викликати після успішного завершення місії на карті).
func set_mission_completed(lord_index: int, mission_index: int) -> void:
	if lord_index < 0:
		return
	while mission_completed.size() <= lord_index:
		mission_completed.append([])
	var arr: Array = mission_completed[lord_index]
	while arr.size() <= mission_index:
		arr.append(false)
	arr[mission_index] = true

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
	_init_generals_if_needed()

func _init_generals_if_needed() -> void:
	if general_invited.size() != GENERALS_COUNT:
		general_invited.resize(GENERALS_COUNT)
		general_relationship.resize(GENERALS_COUNT)
		general_names.resize(GENERALS_COUNT)
		for i in range(GENERALS_COUNT):
			general_invited[i] = false
			general_relationship[i] = 0
			general_names[i] = "General %d" % (i + 1)
		general_names[0] = "Reeve"
		general_names[1] = "Gabriel"
		# Демо: кілька запрошених для тесту Visiting
		general_invited[0] = true
		general_invited[1] = true
		general_relationship[0] = 25
		general_relationship[1] = 10
	_init_lord_generals()
	if lord_unlocked.size() != LORDS_MAX:
		lord_unlocked.resize(LORDS_MAX)
		for i in range(LORDS_MAX):
			lord_unlocked[i] = true
	if lord_names.size() < lords_count_in_chapter:
		lord_names.resize(lords_count_in_chapter)
		for i in range(lords_count_in_chapter):
			if i >= lord_names.size() or lord_names[i] == "":
				lord_names[i] = _default_lord_name(i)
	_init_mission_data()

func _init_mission_data() -> void:
	# Назви місій для глави (Java: ruler.arr v(55)). Поки placeholder; можна підставити з даних.
	if mission_names.is_empty():
		mission_names = ["First Strike", "The Front Line", "Hold the Pass", "Enemy Supply", "Final Push"]
		mission_names.resize(maxi(mission_names.size(), missions_count_in_chapter))
	# Слот для відстеження завершених місій по лордах (Java: dy[]).
	while mission_completed.size() < lords_count_in_chapter:
		var arr: Array = []
		for _i in range(8):
			arr.append(false)
		mission_completed.append(arr)

func _init_lord_generals() -> void:
	## Розподіл генералів по лордах (placeholder: рівномірно). На полі бою — тільки генерали інших лордів.
	if lord_generals.size() >= lords_count_in_chapter:
		return
	lord_generals.clear()
	var n: int = lords_count_in_chapter
	if n <= 0:
		n = 1
	var per_lord: int = GENERALS_COUNT / n
	var remainder: int = GENERALS_COUNT % n
	var start: int = 0
	for lord_i in range(n):
		var count: int = per_lord + (1 if lord_i < remainder else 0)
		var arr: Array[int] = []
		for k in range(count):
			if start + k < GENERALS_COUNT:
				arr.append(start + k)
		start += count
		lord_generals.append(arr)
	# Місце спавну на карті по лордах (Java: cd, ce з cz.b[0]); порядок карт = по лордах (map id = lord id).
	while spawn_tile_per_lord.size() < n:
		spawn_tile_per_lord.append(Vector2i(4, 4))

func _default_lord_name(index: int) -> String:
	# Java: dt[b] з v(48) mission.arr; поки placeholder (не плутати з генералами)
	var defaults: Array[String] = ["Lord North", "Lord South", "Lord East", "Lord West"]
	if index < defaults.size():
		return defaults[index]
	return "Lord %d" % (index + 1)

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

const SAVE_PATH := "user://save.json"

## Зберігає hero_index, difficulty_index, player_name у user://save.json.
## Повертає true при успіху.
func save_game() -> bool:
	var data := {
		"hero_index": hero_index,
		"difficulty_index": difficulty_index,
		"player_name": player_name,
	}
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file == null:
		return false
	file.store_string(JSON.stringify(data))
	file.close()
	return true

## Завантажує hero_index, difficulty_index, player_name з user://save.json.
## Повертає true при успіху, false якщо файл відсутній або пошкоджений.
func load_game() -> bool:
	if not FileAccess.file_exists(SAVE_PATH):
		return false
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file == null:
		return false
	var text := file.get_as_text()
	file.close()
	var parsed = JSON.parse_string(text)
	if not parsed is Dictionary:
		return false
	if parsed.has("hero_index"):
		hero_index = int(parsed["hero_index"])
	if parsed.has("difficulty_index"):
		difficulty_index = int(parsed["difficulty_index"])
	if parsed.has("player_name"):
		player_name = str(parsed["player_name"])
	return true

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
