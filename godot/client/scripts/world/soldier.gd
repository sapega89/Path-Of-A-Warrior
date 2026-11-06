extends Node3D
## An enemy soldier of the map: the original 2D sprite standing in the 3D world, like the
## hero. Swords and archers are one sprite; a squad (kind 203) is three swordsmen drawn
## around the one actor of the simulation, at the original offsets for its direction.
## The sheets are assets/original/enemy_<n>_<tint>.png (godot/tools/import_original.py),
## cells laid out like the hero's.

const SHEET_PATH := "res://assets/original/enemy_%d_%d.png"
const CELL := Vector2(96, 96)
const ORIGIN := Vector2(48, 72)
const COLUMNS := 16
const PX := 1.0 / 27.0
const FOOT_PX := 6
const HIDDEN := 100  # frames from here on are not drawn (the dying blink)

var kind := 201
var sprites: Array[Sprite3D] = []
var _offsets: Array = []


func setup(enemy_kind: int, tint: int, squad_offsets: Array) -> void:
	kind = enemy_kind
	_offsets = squad_offsets
	var tex: Texture2D = load(SHEET_PATH % [1 if kind == 202 else 0, clampi(tint, 0, 3)])
	for i in (3 if kind == 203 else 1):
		var s := Sprite3D.new()
		s.name = "Sprite%d" % i
		s.texture = tex
		s.region_enabled = true
		s.pixel_size = PX
		s.billboard = BaseMaterial3D.BILLBOARD_FIXED_Y
		s.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
		s.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
		s.shaded = true
		s.position.y = (ORIGIN.y - CELL.y / 2.0 + FOOT_PX) * PX
		add_child(s)
		sprites.append(s)


## Shows a frame; dir4 places the three men of a squad.
func set_frame(frame: int, dir4: int) -> void:
	visible = frame < HIDDEN
	if not visible:
		return
	var r := Rect2((frame % COLUMNS) * CELL.x, (frame / COLUMNS) * CELL.y, CELL.x, CELL.y)
	for i in sprites.size():
		var s := sprites[i]
		s.region_rect = r
		if kind == 203 and dir4 < _offsets.size():
			var o: Array = _offsets[dir4][i]
			s.position.x = float(o[0]) * PX
			s.position.z = float(o[1]) * PX
