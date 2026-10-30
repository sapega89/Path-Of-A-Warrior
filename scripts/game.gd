extends Node2D
## Игровая сцена: карта (c.java) + персонаж + камера. Обновляет позицию карты по персонажу.

const VIEW_W := GameState.VIEW_W
const VIEW_H := GameState.VIEW_H
const CENTER := Vector2(VIEW_W / 2.0, VIEW_H / 2.0)

var _map: Node2D
var _player: CharacterBody2D

func _ready() -> void:
	_map = $MapRenderer
	_player = $Player
	if _map.has_method("set_camera_offset"):
		_update_map_camera()

func _process(_delta: float) -> void:
	_update_map_camera()

func _update_map_camera() -> void:
	if not is_instance_valid(_player) or not is_instance_valid(_map):
		return
	var px: Vector2 = _player.global_position
	var tile_x := int(px.x / GameState.TILE_SIZE)
	var tile_y := int(px.y / GameState.TILE_SIZE)
	var pixel_off_x := int(px.x) % GameState.TILE_SIZE
	var pixel_off_y := int(px.y) % GameState.TILE_SIZE
	_map.set_camera_offset(tile_x, tile_y, pixel_off_x, pixel_off_y)
