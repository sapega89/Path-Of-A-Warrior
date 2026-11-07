extends Control
## The rooms of a mission on its place's map (scripts/world/rooms.gd), drawn small before the
## mission is accepted: the grid of rooms, the passages this mission opens between them, the
## room the hero starts in and the rooms with a general. Rooms the mission never reaches are
## dim, since the missions of a place walk the same map by different ways.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Rooms := preload("res://scripts/world/rooms.gd")
const MAX_SIZE := Vector2(600, 220)
const GENERAL := Color("c0504d")

var rooms: RefCounted
var start := 0
var reach := {}  # room -> true
var cell := 40.0


func _init(map: Dictionary, mission: int, start_tile: Vector2i) -> void:
	name = "Rooms"
	rooms = Rooms.new(map, mission)
	start = rooms.start_room(start_tile)
	for r in rooms.reachable_from(start):
		reach[r] = true
	cell = minf(48.0, minf(MAX_SIZE.x / rooms.rooms_x, MAX_SIZE.y / rooms.rooms_y))
	custom_minimum_size = Vector2(0, cell * rooms.rooms_y + 8)
	size_flags_horizontal = Control.SIZE_EXPAND_FILL


func reached() -> int:
	return reach.size()


func generals() -> Array:
	var out: Array = []
	for r in reach:
		if rooms.has_general(r):
			out.append(r)
	out.sort()
	return out


func _origin() -> Vector2:
	return Vector2((size.x - cell * rooms.rooms_x) / 2, 4)


func _rect(r: int) -> Rect2:
	var p: Vector2i = rooms.room_xy(r)
	return Rect2(_origin() + Vector2(p.x, p.y) * cell, Vector2(cell, cell)).grow(-cell * 0.12)


func _draw() -> void:
	var gens := generals()
	for r in rooms.count():
		draw_rect(_rect(r), UiTheme.BUTTON if reach.has(r) else UiTheme.PANEL)
	for r in reach:
		for exit_no in range(Rooms.EXIT_DOWN, Rooms.EXIT_RIGHT + 1):
			var n: int = rooms.neighbour(r, exit_no)
			if rooms.has_exit(r, exit_no) and n >= 0 and n < rooms.count():
				draw_line(_rect(r).get_center(), _rect(n).get_center(), UiTheme.ACCENT, maxf(2.0, cell / 10), true)
	for r in reach:
		var box := _rect(r).grow(-cell * 0.18)
		draw_rect(box, UiTheme.BUTTON)
	draw_rect(_rect(start).grow(-cell * 0.18), UiTheme.ACCENT)
	for r in gens:
		draw_circle(_rect(r).get_center(), cell * 0.16, GENERAL)
