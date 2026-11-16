class_name GroundPaint
extends RefCounted
## The ground of a map being made (MapDraft), in parts (MapArt.PARTS a cell each way) so that the
## kinds run into each other as the game draws them: the biome's ground, patches of the biome's
## other kinds where a noise of our random numbers says (each taking its share of the map), the
## path along the ways through the rooms (its edges wandering into the parts beside it), the
## kinds the fill gave its cells (water, the stone of a cliff, a wall) over all their parts, and
## sand on the banks of the water.
##
## A biome's ground in the rules: ground (its kind, a letter of MapArt.KIND_LETTERS), patches
## [[kind, share of the map], ...], path (the kind of the path).

## Parts between the points of the noise.
const NOISE_STEP := 5
## The share of the parts beside the path that it takes.
const PATH_EDGE := 0.35
const WATER := "w"
const BANK := "s"

var draft: MapDraft
var biome: Dictionary
var random: GameRandom
## The parts across and down the map.
var _pw := 0
var _ph := 0
## Per part (x + y * _pw): its kind.
var _kinds: Array[String] = []


func _init(map_draft: MapDraft, biome_rules: Dictionary, rng: GameRandom) -> void:
	draft = map_draft
	biome = biome_rules
	random = rng
	_pw = draft.w * MapArt.PARTS
	_ph = draft.h * MapArt.PARTS


## Paints the parts of every cell of the draft.
func paint() -> void:
	_kinds.resize(_pw * _ph)
	_kinds.fill(str(biome["ground"]))
	for patch: Array in biome["patches"]:
		_patch(str(patch[0]), float(patch[1]))
	_paint_path(str(biome["path"]))
	for i in draft.w * draft.h:
		if draft.kinds[i] != "":
			_paint_cell(i, draft.kinds[i])
	_paint_banks()
	for i in draft.w * draft.h:
		var letters := ""
		for p in _cell_parts(i):
			letters += _kinds[p]
		draft.parts[i] = letters


## The parts of a cell, row by row (as the map writes its nine letters).
func _cell_parts(cell: int) -> Array[int]:
	var x := (cell % draft.w) * MapArt.PARTS
	var y := (cell / draft.w) * MapArt.PARTS
	var out: Array[int] = []
	for dy in MapArt.PARTS:
		for dx in MapArt.PARTS:
			out.append((y + dy) * _pw + x + dx)
	return out


func _paint_cell(cell: int, kind: String) -> void:
	for p in _cell_parts(cell):
		_kinds[p] = kind


## A kind over the parts where the noise is lowest, `share` of them.
func _patch(kind: String, share: float) -> void:
	var noise := _noise()
	var sorted := noise.duplicate()
	sorted.sort()
	var below: float = sorted[clampi(roundi(share * sorted.size()), 0, sorted.size() - 1)]
	for p in noise.size():
		if noise[p] < below:
			_kinds[p] = kind


## A smooth noise over the parts, 0 to 1: random values on points NOISE_STEP parts apart, eased
## between them.
func _noise() -> PackedFloat32Array:
	const IN := 1000
	var across := _pw / NOISE_STEP + 2
	var down := _ph / NOISE_STEP + 2
	var points := PackedFloat32Array()
	for i in across * down:
		points.append(random.below(IN) / float(IN))
	var out := PackedFloat32Array()
	out.resize(_pw * _ph)
	for py in _ph:
		for px in _pw:
			var gx := px / NOISE_STEP
			var gy := py / NOISE_STEP
			var fx := smoothstep(0.0, 1.0, (px % NOISE_STEP) / float(NOISE_STEP))
			var fy := smoothstep(0.0, 1.0, (py % NOISE_STEP) / float(NOISE_STEP))
			var top := lerpf(points[gy * across + gx], points[gy * across + gx + 1], fx)
			var bottom := lerpf(
				points[(gy + 1) * across + gx], points[(gy + 1) * across + gx + 1], fx
			)
			out[py * _pw + px] = lerpf(top, bottom, fy)
	return out


## The path's cells, and the parts beside them now and then.
func _paint_path(kind: String) -> void:
	const IN := 1000
	for i in draft.w * draft.h:
		if draft.path[i] == 0:
			continue
		_paint_cell(i, kind)
		var c := Vector2i(i % draft.w, i / draft.w)
		for step in RoomLayout.STEP:
			var n := c + step
			if not draft.inside(n) or draft.path[draft.at(n)] == 1:
				continue
			for p in _edge_parts(draft.at(n), -step):
				if random.below(IN) < PATH_EDGE * IN:
					_kinds[p] = kind


## The parts of a cell along its side that faces the way `toward` goes.
func _edge_parts(cell: int, toward: Vector2i) -> Array[int]:
	var parts := _cell_parts(cell)
	var last := MapArt.PARTS - 1
	var out: Array[int] = []
	for i in parts.size():
		var at := Vector2i(i % MapArt.PARTS, i / MapArt.PARTS)
		if (
			(toward.x > 0 and at.x == last)
			or (toward.x < 0 and at.x == 0)
			or (toward.y > 0 and at.y == last)
			or (toward.y < 0 and at.y == 0)
		):
			out.append(parts[i])
	return out


## Sand on the parts of the dry cells off the path that touch a part of water.
func _paint_banks() -> void:
	var bank: Array[int] = []
	for py in _ph:
		for px in _pw:
			var cell := (py / MapArt.PARTS) * draft.w + px / MapArt.PARTS
			if draft.kinds[cell] != "" or draft.path[cell] == 1 or _kinds[py * _pw + px] == WATER:
				continue
			for step in RoomLayout.STEP:
				var n := Vector2i(px, py) + step
				if n.x < 0 or n.y < 0 or n.x >= _pw or n.y >= _ph:
					continue
				if _kinds[n.y * _pw + n.x] == WATER:
					bank.append(py * _pw + px)
					break
	for p in bank:
		_kinds[p] = BANK
