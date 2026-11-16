class_name MapBuilder
extends Node3D
## A map of the campaign (data/maps/<n>.json): its cells, their collision and the cells shown.
## MapArt (map_art.gd) builds on it and draws the map.
##
## One tile = 1 world unit; tile (x, y) covers x..x+1 on X and y..y+1 on Z
## (screen "down" is +Z, the camera looks along -Z).
## Collision is per cell: a blocked cell or an object is a solid box, and the edges of the map
## are walls.

const FLAG_BLOCKED := 1
const FLAG_OVER := 2
const WALL_HEIGHT := 1.5  # collision height of a blocked cell

var map: Dictionary
var w := 0
var h := 0
var breakables: Array[Node3D] = []
## The cells drawn (show_only); empty: all.
var _shown := {}


static func map_path(number: int) -> String:
	return "res://data/maps/%d.json" % number


static func load_map(number: int) -> Dictionary:
	var f := FileAccess.open(map_path(number), FileAccess.READ)
	if f == null:
		return {}
	var data: Variant = JSON.parse_string(f.get_as_text())
	return data if typeof(data) == TYPE_DICTIONARY else {}


static func map_count() -> int:
	var n := 0
	while FileAccess.file_exists(map_path(n + 1)):
		n += 1
	return n


func cell(layer: String, x: int, y: int) -> int:
	if x < 0 or y < 0 or x >= w or y >= h:
		return 0
	return int(map[layer][y * w + x])


func is_blocked(x: int, y: int) -> bool:
	return (cell("flags", x, y) & FLAG_BLOCKED) != 0 or cell("objects", x, y) != 0


func is_shown(x: int, y: int) -> bool:
	return _shown.is_empty() or _shown.has(Vector2i(x, y))


func _build_collision() -> void:
	var body := StaticBody3D.new()  # standards: allow nodes_in_code (the walls of the map)
	body.name = "Collision"
	add_child(body)
	for y in h:
		for x in w:
			if is_blocked(x, y):
				_box(body, Vector3(x + 0.5, WALL_HEIGHT / 2.0, y + 0.5), Vector3(1, WALL_HEIGHT, 1))
	# The edges of the map keep the actors inside it.
	_box(body, Vector3(w / 2.0, WALL_HEIGHT / 2.0, -0.5), Vector3(w + 2, WALL_HEIGHT, 1))
	_box(body, Vector3(w / 2.0, WALL_HEIGHT / 2.0, h + 0.5), Vector3(w + 2, WALL_HEIGHT, 1))
	_box(body, Vector3(-0.5, WALL_HEIGHT / 2.0, h / 2.0), Vector3(1, WALL_HEIGHT, h + 2))
	_box(body, Vector3(w + 0.5, WALL_HEIGHT / 2.0, h / 2.0), Vector3(1, WALL_HEIGHT, h + 2))
	var ground := CollisionShape3D.new()  # standards: allow nodes_in_code (the floor of the map)
	var plane := BoxShape3D.new()
	plane.size = Vector3(w + 2, 0.2, h + 2)
	ground.shape = plane
	ground.position = Vector3(w / 2.0, -0.1, h / 2.0)
	body.add_child(ground)


func _box(body: StaticBody3D, pos: Vector3, size: Vector3) -> void:
	var shape := CollisionShape3D.new()  # standards: allow nodes_in_code (a wall of the map)
	var box := BoxShape3D.new()
	box.size = size
	shape.shape = box
	shape.position = pos
	body.add_child(shape)


## A free cell near the centre of room `room` (index in the rooms grid), for the hero.
func start_cell(room: int = 0) -> Vector2i:
	var rooms_x: int = maxi(int(map.get("rooms", {}).get("rooms_x", 1)), 1)
	var centre := Vector2i((room % rooms_x) * 7 + 4, (room / rooms_x) * 7 + 4)
	for r in range(0, maxi(w, h)):
		for dy in range(-r, r + 1):
			for dx in range(-r, r + 1):
				var p := centre + Vector2i(dx, dy)
				if p.x >= 0 and p.y >= 0 and p.x < w and p.y < h and not is_blocked(p.x, p.y):
					return p
	return centre


static func cell_to_world(c: Vector2i) -> Vector3:
	return Vector3(c.x + 0.5, 0.0, c.y + 0.5)
