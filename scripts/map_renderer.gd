extends Node2D
## Рендер карты по сетке 27x27. Соответствует c.java: l() — отрисовка тайлов,
## eE — «грязные» клетки, cE — данные слоя, cJ — индексы тайлов, ca — камера.

const TILE := GameState.TILE_SIZE
const VIEW_W := GameState.VIEW_W
const VIEW_H := GameState.VIEW_H
const COLS := GameState.MAP_VISIBLE_COLS
const ROWS := GameState.MAP_VISIBLE_ROWS

var _tile_textures: Array[Texture2D] = []
var _map_data: Array[Array] = []  # [row][col] = tile index 0..15
var _map_cols: int = 0
var _map_rows: int = 0
var _level: int = 1
var _tile_nodes: Array[Array] = []  # [row][col] = Sprite2D

func _ready() -> void:
	_load_level_tiles(GameState.current_level)
	_build_demo_map()
	_create_tile_sprites()
	_update_tile_positions()

func set_level(level: int) -> void:
	if _level == level:
		return
	_level = level
	_load_level_tiles(level)
	_refresh_all_tiles()

func set_camera_offset(tile_x: int, tile_y: int, pixel_off_x: int, pixel_off_y: int) -> void:
	var world_px := Vector2(tile_x * TILE + pixel_off_x, tile_y * TILE + pixel_off_y)
	position = Vector2(VIEW_W / 2.0, VIEW_H / 2.0) - world_px
	_update_visible_tiles(tile_x, tile_y)

func _load_level_tiles(level: int) -> void:
	_tile_textures.clear()
	for i in range(16):
		var path := GameState.get_level_tile_path(level, i)
		if ResourceLoader.exists(path):
			var tex: Texture2D = load(path) as Texture2D
			_tile_textures.append(tex)
		else:
			_tile_textures.append(null)
	if _tile_textures.is_empty():
		push_warning("MapRenderer: no tiles for level %d" % level)

func _build_demo_map() -> void:
	# Демо: сетка как в оригинале, бордюр + пол. Можно позже загружать из .MAP
	_map_cols = 20
	_map_rows = 20
	_map_data.clear()
	for row in _map_rows:
		var r: Array = []
		for col in _map_cols:
			if row == 0 or row == _map_rows - 1 or col == 0 or col == _map_cols - 1:
				r.append(0)
			else:
				# Чередуем пол для разнообразия
				r.append(1 + (row + col) % 2)
		_map_data.append(r)

func _create_tile_sprites() -> void:
	for child in get_children():
		child.queue_free()
	_tile_nodes.clear()
	for row in _map_rows:
		var row_nodes: Array = []
		for col in _map_cols:
			var spr := Sprite2D.new()
			add_child(spr)
			row_nodes.append(spr)
		_tile_nodes.append(row_nodes)
	_refresh_all_tiles()

func _refresh_all_tiles() -> void:
	for row in _map_data.size():
		for col in _map_data[row].size():
			_set_tile_sprite(row, col, _map_data[row][col])

func _set_tile_sprite(row: int, col: int, tile_index: int) -> void:
	if row >= _tile_nodes.size() or col >= _tile_nodes[row].size():
		return
	var spr: Sprite2D = _tile_nodes[row][col]
	if tile_index >= 0 and tile_index < _tile_textures.size() and _tile_textures[tile_index]:
		spr.texture = _tile_textures[tile_index]
		spr.visible = true
	else:
		spr.visible = false
	spr.position = Vector2(col * TILE + TILE / 2.0, row * TILE + TILE / 2.0)

func _update_tile_positions() -> void:
	for row in _map_data.size():
		for col in _map_data[row].size():
			var spr: Sprite2D = _tile_nodes[row][col]
			spr.position = Vector2(col * TILE + TILE / 2.0, row * TILE + TILE / 2.0)

func _update_visible_tiles(tile_x: int, tile_y: int) -> void:
	# Опционально: скрывать тайлы далеко от камеры для производительности
	pass

func get_tile_at_pixel(px: float, py: float) -> Vector2i:
	var col := int(px / TILE)
	var row := int(py / TILE)
	return Vector2i(clampi(col, 0, _map_cols - 1), clampi(row, 0, _map_rows - 1))

func is_walkable(tile_col: int, tile_row: int) -> bool:
	if tile_row < 0 or tile_row >= _map_rows or tile_col < 0 or tile_col >= _map_cols:
		return false
	var idx: int = _map_data[tile_row][tile_col]
	return idx != 0
