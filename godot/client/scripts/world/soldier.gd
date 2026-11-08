extends Node3D
## An enemy of the map: the original 2D sprite standing in the 3D world, like the hero.
## Swords and archers are one sprite; a squad (kind 203) is three swordsmen drawn around
## the one actor of the simulation, at the original offsets for its direction. A general
## (kind < 200) is drawn from his look and side, with one sheet for his walk and strikes
## and one for his skills. The sheets are assets/original/enemy_<n>_<tint>.png and
## general_<look>_<side>_<base|sk>.png (godot/tools/import_original.py).

const SHEET_PATH := "res://assets/original/enemy_%d_%d.png"
const GENERAL_PATH := "res://assets/original/general_%d_%d_%s.png"
const COLUMNS := 16
const PX := 1.0 / 27.0
const FOOT_PX := 6

var kind := 201
var sprites: Array[Sprite3D] = []
var cell := Vector2(96, 96)
var hidden_from := 100  # frames from here on are not drawn (the dying blink)
var _offsets: Array = []
var _base: Texture2D
var _skill: Texture2D


func setup(enemy_kind: int, tint: int, squad_offsets: Array, general: Dictionary = {}) -> void:
	kind = enemy_kind
	_offsets = squad_offsets
	var origin := Vector2(48, 72)
	if kind < 200:
		var look := clampi(int(general.get("look", 1)), 1, 6)
		var side := int(general.get("side", 0)) & 1
		_base = load(GENERAL_PATH % [look, side, "base"])
		_skill = load(GENERAL_PATH % [look, side, "sk"])
		cell = Vector2(96, 112)
		origin = Vector2(48, 88)
		hidden_from = 180
	else:
		_base = load(SHEET_PATH % [1 if kind == 202 else 0, clampi(tint, 0, 3)])
	for i in (3 if kind == 203 else 1):
		var s := Sprite3D.new()
		s.name = "Sprite%d" % i
		s.texture = _base
		s.region_enabled = true
		s.pixel_size = PX
		s.billboard = BaseMaterial3D.BILLBOARD_FIXED_Y
		s.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
		s.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
		s.shaded = true
		s.position.y = (origin.y - cell.y / 2.0 + FOOT_PX) * PX
		add_child(s)
		sprites.append(s)


## Shows a frame; dir4 places the three men of a squad; skill: a general's skill frame.
func set_frame(frame: int, dir4: int, skill: bool = false) -> void:
	visible = frame < hidden_from
	if not visible:
		return
	var r := Rect2((frame % COLUMNS) * cell.x, (frame / COLUMNS) * cell.y, cell.x, cell.y)
	for i in sprites.size():
		var s := sprites[i]
		s.region_rect = r
		if kind < 200:
			s.texture = _skill if skill else _base
		elif kind == 203 and dir4 < _offsets.size():
			var o: Array = _offsets[dir4][i]
			s.position.x = float(o[0]) * PX
			s.position.z = float(o[1]) * PX
