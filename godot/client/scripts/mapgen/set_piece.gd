class_name SetPiece
extends RefCounted
## A room made by hand (data/set_pieces.json): its 7x7 cells written as rows of characters, each
## one a cell of the key: free ({}), or blocked by a kind of ground (kind, a letter of
## MapArt.KIND_LETTERS) or a thing standing on it (prop). A piece has a role (general: the arena
## of a mission's own general; start: the room a mission starts in; crossing: a way over water;
## village; gate) and the biomes it fits. The generator lays a piece one of its WAYS ways, turned
## and mirrored, and opens it where the ways through the room go (RoomFill).

const PATH := "res://data/set_pieces.json"
## The ways a piece can lie: four quarter turns, each as drawn and mirrored.
const WAYS := 8
const SIDE := 7

static var _data: Dictionary = {}
static var _pieces: Array[SetPiece] = []

var name := ""
var role := ""
var biomes: Array[String] = []
var rows: Array[String] = []


## Every piece of the data, in its order.
static func all() -> Array[SetPiece]:
	if _pieces.is_empty():
		for entry: Dictionary in _data_of()["pieces"]:
			var piece := SetPiece.new()
			piece.name = str(entry["name"])
			piece.role = str(entry["role"])
			for biome: String in entry["biomes"]:
				piece.biomes.append(biome)
			for row: String in entry["rows"]:
				piece.rows.append(row)
			_pieces.append(piece)
	return _pieces


## The pieces of a role that fit a biome.
static func fitting(of_role: String, biome: String) -> Array[SetPiece]:
	var out: Array[SetPiece] = []
	for piece in all():
		if piece.role == of_role and biome in piece.biomes:
			out.append(piece)
	return out


## What a character of the rows stands for: {kind, prop}, {} a free cell.
static func key() -> Dictionary:
	return _data_of()["key"]


static func _data_of() -> Dictionary:
	if _data.is_empty():
		_data = JSON.parse_string(FileAccess.get_file_as_string(PATH))
	return _data


## What is on cell `at` of the room (0 to SIDE - 1 each way) with the piece laid the `way`-th way.
func cell(at: Vector2i, way: int) -> Dictionary:
	var from := at
	if way >= WAYS / 2:
		from.x = SIDE - 1 - from.x
	for i in way % (WAYS / 2):
		from = Vector2i(from.y, SIDE - 1 - from.x)
	return key()[rows[from.y][from.x]]
