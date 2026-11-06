extends Node3D
## Builds a 3D map from an original map (data/maps/<n>.json, made by
## godot/tools/import_original.py) with the original tiles.
##
## One tile = 1 world unit; tile (x, y) covers x..x+1 on X and y..y+1 on Z
## (screen "down" is +Z, the camera looks along -Z).
##   ground layer      -> flat floor
##   upper layer       -> flat decals (roads, grass), except:
##   blocked / overlay -> stood up: a column of cells with flags bit 0 (blocked) or bit 1
##                        (drawn over the actors) is a front view of a wall, tree or house
##                        in the original art, so it is raised as a vertical picture at the
##                        front (largest y) cell of the run, stacking upward
##   objects layer     -> breakable things as sprites facing the camera
## Collision is per cell as in the original: a blocked cell or an object is a solid box.

const ATLAS_PATH := "res://assets/original/tiles.png"
const ATLAS_COLS := 16
const ATLAS_ROWS := 15
const TILE_PX := 27
const FLAG_BLOCKED := 1
const FLAG_OVER := 2
const WALL_HEIGHT := 1.5  # collision height of a blocked cell
const DECAL_LIFT := 0.002

var map: Dictionary
var w := 0
var h := 0
var atlas: Texture2D
var floor_mat: StandardMaterial3D
var stand_mat: StandardMaterial3D
var breakables: Array[Node3D] = []


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


## UV rectangle of tile id t (1..240) in the atlas.
static func tile_uv(t: int) -> Rect2:
	var i := t - 1
	var inset := Vector2(0.25 / (ATLAS_COLS * TILE_PX), 0.25 / (ATLAS_ROWS * TILE_PX))
	var pos := Vector2(float(i % ATLAS_COLS) / ATLAS_COLS, float(i / ATLAS_COLS) / ATLAS_ROWS)
	var size := Vector2(1.0 / ATLAS_COLS, 1.0 / ATLAS_ROWS)
	return Rect2(pos + inset, size - inset * 2.0)


func cell(layer: String, x: int, y: int) -> int:
	if x < 0 or y < 0 or x >= w or y >= h:
		return 0
	return int(map[layer][y * w + x])


func is_blocked(x: int, y: int) -> bool:
	return (cell("flags", x, y) & FLAG_BLOCKED) != 0 or cell("objects", x, y) != 0


## Cells that are shown standing up: blocked or overlay, with an upper tile.
func is_standing(x: int, y: int) -> bool:
	return cell("upper", x, y) != 0 and (cell("flags", x, y) & (FLAG_BLOCKED | FLAG_OVER)) != 0


## Runs of standing cells per column: [{x, top, bottom}], bottom = the front cell.
func standing_runs() -> Array[Dictionary]:
	var runs: Array[Dictionary] = []
	for x in w:
		var y := 0
		while y < h:
			if is_standing(x, y):
				var top := y
				while y + 1 < h and is_standing(x, y + 1):
					y += 1
				runs.append({"x": x, "top": top, "bottom": y})
			y += 1
	return runs


func build(data: Dictionary) -> void:
	map = data
	w = int(map.get("w", 0))
	h = int(map.get("h", 0))
	for child in get_children():
		child.queue_free()
	breakables.clear()
	atlas = load(ATLAS_PATH)
	floor_mat = _material(false)
	stand_mat = _material(true)
	_build_floor()
	_build_standing()
	_build_objects()
	_build_collision()


func _material(cutout: bool) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_texture = atlas
	m.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
	if cutout:
		m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
		m.alpha_scissor_threshold = 0.5
		m.cull_mode = BaseMaterial3D.CULL_DISABLED
	return m


func _build_floor() -> void:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for y in h:
		for x in w:
			var g := cell("ground", x, y)
			if g != 0:
				_flat_quad(st, x, y, 0.0, g)
			var u := cell("upper", x, y)
			if u != 0 and not is_standing(x, y):
				_flat_quad(st, x, y, DECAL_LIFT, u)
	_add_mesh("Floor", st, stand_mat)  # decals have transparent pixels


func _build_standing() -> void:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for run in standing_runs():
		var front_z := float(run.bottom) + 1.0
		var level := 0
		for y in range(run.bottom, run.top - 1, -1):
			_wall_quad(st, run.x, front_z, level, cell("upper", run.x, y))
			level += 1
	_add_mesh("Standing", st, stand_mat)


func _build_objects() -> void:
	for y in h:
		for x in w:
			var kind := cell("objects", x, y)
			if kind == 0:
				continue
			var s := Sprite3D.new()
			s.name = "Object_%d_%d" % [x, y]
			s.texture = atlas
			s.region_enabled = true
			var i := kind - 1
			s.region_rect = Rect2((i % ATLAS_COLS) * TILE_PX, (i / ATLAS_COLS) * TILE_PX, TILE_PX, TILE_PX)
			s.pixel_size = 1.0 / TILE_PX
			s.billboard = BaseMaterial3D.BILLBOARD_FIXED_Y
			s.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
			s.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
			s.shaded = true
			s.position = Vector3(x + 0.5, 0.5, y + 0.5)
			s.set_meta("kind", kind)
			s.set_meta("hp", 41 if kind in [101, 113] else 21)
			add_child(s)
			breakables.append(s)


func _build_collision() -> void:
	var body := StaticBody3D.new()
	body.name = "Collision"
	add_child(body)
	for y in h:
		for x in w:
			if is_blocked(x, y):
				_box(body, Vector3(x + 0.5, WALL_HEIGHT / 2.0, y + 0.5), Vector3(1, WALL_HEIGHT, 1))
	# The map edge: the original keeps the actors inside the map.
	_box(body, Vector3(w / 2.0, WALL_HEIGHT / 2.0, -0.5), Vector3(w + 2, WALL_HEIGHT, 1))
	_box(body, Vector3(w / 2.0, WALL_HEIGHT / 2.0, h + 0.5), Vector3(w + 2, WALL_HEIGHT, 1))
	_box(body, Vector3(-0.5, WALL_HEIGHT / 2.0, h / 2.0), Vector3(1, WALL_HEIGHT, h + 2))
	_box(body, Vector3(w + 0.5, WALL_HEIGHT / 2.0, h / 2.0), Vector3(1, WALL_HEIGHT, h + 2))
	var ground := CollisionShape3D.new()
	var plane := BoxShape3D.new()
	plane.size = Vector3(w + 2, 0.2, h + 2)
	ground.shape = plane
	ground.position = Vector3(w / 2.0, -0.1, h / 2.0)
	body.add_child(ground)


func _box(body: StaticBody3D, pos: Vector3, size: Vector3) -> void:
	var shape := CollisionShape3D.new()
	var box := BoxShape3D.new()
	box.size = size
	shape.shape = box
	shape.position = pos
	body.add_child(shape)


func _flat_quad(st: SurfaceTool, x: int, y: int, lift: float, t: int) -> void:
	var uv := tile_uv(t)
	var a := Vector3(x, lift, y)
	var b := Vector3(x + 1, lift, y)
	var c := Vector3(x + 1, lift, y + 1)
	var d := Vector3(x, lift, y + 1)
	_quad(st, a, b, c, d, uv, Vector3.UP)


func _wall_quad(st: SurfaceTool, x: int, z: float, level: int, t: int) -> void:
	var uv := tile_uv(t)
	var a := Vector3(x, level + 1, z)
	var b := Vector3(x + 1, level + 1, z)
	var c := Vector3(x + 1, level, z)
	var d := Vector3(x, level, z)
	_quad(st, a, b, c, d, uv, Vector3.BACK)


## a b / d c, a = top-left of the picture.
func _quad(st: SurfaceTool, a: Vector3, b: Vector3, c: Vector3, d: Vector3, uv: Rect2, normal: Vector3) -> void:
	var ua := uv.position
	var ub := Vector2(uv.end.x, uv.position.y)
	var uc := uv.end
	var ud := Vector2(uv.position.x, uv.end.y)
	for v in [[a, ua], [b, ub], [c, uc], [a, ua], [c, uc], [d, ud]]:
		st.set_normal(normal)
		st.set_uv(v[1])
		st.add_vertex(v[0])


func _add_mesh(node_name: String, st: SurfaceTool, mat: Material) -> void:
	var mi := MeshInstance3D.new()
	mi.name = node_name
	var mesh := st.commit()
	if mesh.get_surface_count() > 0:
		mesh.surface_set_material(0, mat)
	mi.mesh = mesh
	add_child(mi)


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
