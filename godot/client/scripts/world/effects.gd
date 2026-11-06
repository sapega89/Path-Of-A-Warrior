extends Node3D
## The pictures of the effects (skills, potions, scrolls) standing in the 3D world like the
## other sprites, drawn over them. show_effects() takes MapSim.effects(): [sheet, frame,
## point in map pixels], and an optional true for a picture behind the one at that point (the
## ring of a buff's aura): it stands a little further back, hidden where he stands in front. The sheets are assets/original/fx_<name>.png with their cells
## and origins in effects.json (godot/tools/import_original.py).

const Hero := preload("res://scripts/world/hero.gd")
const INFO_PATH := "res://assets/original/effects.json"
const SHEET_PATH := "res://assets/original/fx_%s.png"
const PX := 1.0 / 27.0
const BEHIND := 0.08  # how far back (world units) a picture behind someone stands

var info := {}
var _sheets := {}
var _sprites: Array[Sprite3D] = []


func _ready() -> void:
	var f := FileAccess.open(INFO_PATH, FileAccess.READ)
	if f != null:
		var data: Variant = JSON.parse_string(f.get_as_text())
		if typeof(data) == TYPE_DICTIONARY:
			info = data


func show_effects(list: Array) -> void:
	var used := 0
	for e in list:
		var sheet := str(e[0])
		var frame := int(e[1])
		var meta: Dictionary = info.get(sheet, {})
		if meta.is_empty() or frame < 0 or frame >= int(meta.frames):
			continue
		var s := _sprite(used)
		used += 1
		var cell: Array = meta.cell
		var origin: Array = meta.origin
		var cols := int(meta.columns)
		s.texture = _sheet(sheet)
		s.region_rect = Rect2((frame % cols) * float(cell[0]), (frame / cols) * float(cell[1]),
			float(cell[0]), float(cell[1]))
		s.offset = Vector2(float(cell[0]) / 2.0 - float(origin[0]), float(origin[1]) - float(cell[1]) / 2.0)
		var p: Vector2i = e[2]
		var behind: bool = e.size() > 3 and bool(e[3])
		s.position = Hero.px_to_world(Vector2(p)) - Vector3(0.0, 0.0, BEHIND if behind else 0.0)
		s.no_depth_test = not behind
		s.render_priority = 0 if behind else 1
		s.visible = true
	for i in range(used, _sprites.size()):
		_sprites[i].visible = false


func shown() -> int:
	var n := 0
	for s in _sprites:
		if s.visible:
			n += 1
	return n


func _sheet(sheet_name: String) -> Texture2D:
	if not _sheets.has(sheet_name):
		_sheets[sheet_name] = load(SHEET_PATH % sheet_name)
	return _sheets[sheet_name]


func _sprite(i: int) -> Sprite3D:
	while _sprites.size() <= i:
		var s := Sprite3D.new()
		s.name = "Effect%d" % _sprites.size()
		s.region_enabled = true
		s.pixel_size = PX
		s.billboard = BaseMaterial3D.BILLBOARD_FIXED_Y
		s.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
		s.no_depth_test = true
		s.render_priority = 1
		add_child(s)
		_sprites.append(s)
	return _sprites[i]
