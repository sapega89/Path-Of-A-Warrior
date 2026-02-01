extends Node2D
## Game scene: level tiles + player.
## Original: 240x320, tile 27x27, grid ~9x9 visible.

const TILE_SIZE := 27
const VIEW_WIDTH := 240
const VIEW_HEIGHT := 320

var _level_num := 1
var _tile_textures: Array[Texture2D] = []
var _tile_layer: Node2D
var _map_data: Array = []  # [row][col] = tile index 0..15
var _map_cols := 0
var _map_rows := 0

func _ready() -> void:
	_tile_layer = $TileLayer
	_load_level_tiles(_level_num)
	_build_demo_map()
	_draw_tiles()

func _load_level_tiles(level: int) -> void:
	_tile_textures.clear()
	for i in range(1, 17):
		var path := "res://%d_%02d.png" % [level, i]
		if ResourceLoader.exists(path):
			var tex: Texture2D = load(path) as Texture2D
			_tile_textures.append(tex)
		else:
			_tile_textures.append(null)
	if _tile_textures.is_empty():
		push_warning("No tiles found for level %d (e.g. res://1_01.png)" % level)

func _build_demo_map() -> void:
	# Demo: simple grid 12x12, border = tile 0, floor = tile 1
	_map_cols = 12
	_map_rows = 12
	_map_data.clear()
	for row in _map_rows:
		var r: Array = []
		for col in _map_cols:
			if row == 0 or row == _map_rows - 1 or col == 0 or col == _map_cols - 1:
				r.append(0)
			else:
				r.append(1)
		_map_data.append(r)

func _draw_tiles() -> void:
	for c in _tile_layer.get_children():
		c.queue_free()
	if _tile_textures.is_empty():
		return
	for row in _map_data.size():
		for col in _map_data[row].size():
			var idx: int = _map_data[row][col]
			if idx < 0 or idx >= _tile_textures.size() or _tile_textures[idx] == null:
				continue
			var spr := Sprite2D.new()
			spr.texture = _tile_textures[idx]
			spr.position = Vector2(col * TILE_SIZE + TILE_SIZE / 2.0, row * TILE_SIZE + TILE_SIZE / 2.0)
			_tile_layer.add_child(spr)
