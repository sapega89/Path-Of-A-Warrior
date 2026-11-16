class_name MapDraft
extends RefCounted
## A map while the generator makes it (MapGenerator): its cells as the steps leave them, before
## they are written in the format of the campaign's maps. RoomFill puts what stands on the cells
## and keeps the ways through the rooms free, GroundPaint paints the ground under them. Cells
## are x + y * w, as in the map's layers.

var w := 0
var h := 0
var layout: RoomLayout
## Per cell: the kind of ground the fill gave it (a letter of MapArt.KIND_LETTERS: the water of a
## pond, the stone of a cliff, a wall...), "" where the ground is painted.
var kinds: Array[String] = []
## Per cell: what stands on it (MapArt.PROP or MapArt.CLUSTERS), "" nothing.
var props: Array[String] = []
## Per cell: 1 blocked (no one walks on it).
var blocked := PackedByteArray()
## Per cell: 1 kept free, a way through a room (no obstacle goes there).
var keep := PackedByteArray()
## Per cell: 1 on the path the hero walks, from door to door through the rooms.
var path := PackedByteArray()
## Per cell: the kind of each of its parts, nine letters (GroundPaint).
var parts: Array[String] = []


func _init(room_layout: RoomLayout) -> void:
	layout = room_layout
	w = layout.rooms_x * RoomLayout.ROOM + 2
	h = layout.rooms_y * RoomLayout.ROOM + 2
	kinds.resize(w * h)
	kinds.fill("")
	props.resize(w * h)
	props.fill("")
	parts.resize(w * h)
	parts.fill("")
	blocked.resize(w * h)
	keep.resize(w * h)
	path.resize(w * h)


func inside(c: Vector2i) -> bool:
	return c.x >= 0 and c.y >= 0 and c.x < w and c.y < h


func at(c: Vector2i) -> int:
	return c.y * w + c.x


## The cell in the top left corner of a room.
func corner(room: int) -> Vector2i:
	return layout.room_xy(room) * RoomLayout.ROOM + Vector2i.ONE


## The room a cell is in, -1 for the ring around the rooms and outside the map.
func room_of(c: Vector2i) -> int:
	if c.x < 1 or c.y < 1 or c.x > w - 2 or c.y > h - 2:
		return -1
	var room := (c - Vector2i.ONE) / RoomLayout.ROOM
	return room.y * layout.rooms_x + room.x


## Whether a cell is in the ring of cells around the rooms.
func in_ring(c: Vector2i) -> bool:
	return c.x == 0 or c.y == 0 or c.x == w - 1 or c.y == h - 1


## Puts an obstacle on a cell: blocked, with its kind of ground and what stands on it.
func put(c: Vector2i, kind: String, prop: String) -> void:
	var i := at(c)
	blocked[i] = 1
	kinds[i] = kind
	props[i] = prop


## Whether an obstacle may go on a cell: inside the map, free and not kept.
func open(c: Vector2i) -> bool:
	return inside(c) and blocked[at(c)] == 0 and keep[at(c)] == 0
