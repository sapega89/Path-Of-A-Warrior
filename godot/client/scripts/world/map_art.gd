class_name MapArt
extends "res://scripts/world/map_builder.gd"
## A map of the campaign in the new art, from the same data as MapBuilder (data/maps/N.json),
## with the same cells, collision and breakable objects:
##   the ground   one painted surface (in chunks, GroundMesh, so that only what is in view is
##                drawn), three parts to a tile, each part the kind of ground its tile shows
##                there (assets/art/tiles.json, made by godot/tools/art/tiles.py): meadow,
##                grass, dirt, sand, gravel, stone, rock, water, wood or cobble, with the
##                detail of its kind (pebbles, planks, paving);
##   raised       a blocked cell of rock, stone, gravel, cobble or wood rises as a cliff or a wall
##                (its faces drawn as strata, stone courses or logs); a blocked cell of grass as
##                a bank; the slope stays inside the blocked cell, so the free cells stay flat;
##                the rows of rock under a cliff's top are its face, climbing to the top, with
##                crags; a rock or a bush in the middle of a cliff lies on its top;
##   water        sinks under a water surface; a bridge of logs, or a deck under a fence over
##                the water, is boards;
##   props        what stands on a cell (a fir, a bush, a rock, a fence, a palisade, a barrel,
##                a haystack, a well, a campfire...) is a 3D piece of the new art; a tent or a
##                hut drawn over several cells is one tent or hut over their middle;
##   objects      the breakable ones too: a hit flashes each, a glowing brass outline marks it;
##   around       the land goes on past the edges and rises into low hills, with fields of
##                wheat; grass on the meadows in and around the map; both sway in the wind.
## The simulation does not see any of this: it keeps the original cells.

const GROUND_SHADER := preload("res://assets/art/shaders/map_ground.gdshader")
const WATER_SHADER := preload("res://assets/art/shaders/water.gdshader")
const TILES_PATH := "res://assets/art/tiles.json"
const PARTS := 3  # parts to a tile, each way
const MARGIN := 10  # tiles of land around the map

## The colour of each kind of ground (sRGB, near the palette): worn, dusty, held down.
const KIND_COLOUR := {
	"meadow": Color("74714a"),
	"grass": Color("5a6a3e"),
	"dirt": Color("7f6546"),
	"sand": Color("9c8964"),
	"gravel": Color("716659"),
	"stone": Color("6c7177"),
	"rock": Color("58565b"),
	"water": Color("34475a"),
	"wood": Color("6e4c33"),
	"cobble": Color("7c766c"),
}
## How high a blocked cell of each kind rises (none: it does not). Low enough that a wall
## hides little of the cells behind it from the game's camera.
const RAISE := {
	"gravel": 1.0,
	"stone": 1.0,
	"rock": 1.0,
	"cobble": 0.9,
	"wood": 0.9,
	"meadow": 0.45,
	"grass": 0.45,
	"dirt": 0.45,
	"sand": 0.45
}
## How the face of a raised kind looks (map_ground.gdshader): 0 rock in strata, 0.25 an earth
## bank, 0.5 stone in courses, 1 logs.
const FACE := {
	"meadow": 0.25, "grass": 0.25, "dirt": 0.25, "sand": 0.25, "cobble": 0.5, "wood": 1.0
}
## The detail painted on a kind (map_ground.gdshader): pebbles and cracks, planks, paving.
const DETAIL := {"gravel": 0, "stone": 0, "rock": 0, "wood": 1, "cobble": 2}
const WATER_DEPTH := 0.45
const WATER_LEVEL := -0.08
## The props by what a tile shows: [piece in assets/art/props, scale, turned at random].
const PROP := {
	"fir": ["yalyna", Vector3(0.72, 0.72, 0.72), true],
	"bush": ["kushch", Vector3(0.75, 0.75, 0.75), true],
	"boulder": ["kamin", Vector3(1.1, 1.1, 1.1), true],
	"rock": ["kamin", Vector3(0.8, 0.8, 0.8), true],
	"pebbles": ["kamin", Vector3(0.35, 0.35, 0.35), true],
	"stump": ["penok", Vector3.ONE, true],
	"barrel": ["bochka", Vector3.ONE, true],
	"bucket": ["bochka", Vector3(0.6, 0.6, 0.6), true],
	"hay": ["stih", Vector3(0.5, 0.5, 0.5), true],
	"well": ["zhuravel", Vector3(0.5, 0.5, 0.5), false],
	"fire": ["vohnyshche", Vector3(0.8, 0.8, 0.8), true],
	"fence": ["tyn", Vector3(0.5, 1.0, 1.0), false],
	"palisade": ["palisade", Vector3(0.5, 0.8, 0.8), false],
	"chest": ["skrynia", Vector3(0.8, 0.8, 0.8), false],
	"woodpile": ["drova", Vector3(0.9, 0.9, 0.9), false],
	"rack": ["stoiak", Vector3(0.8, 0.8, 0.8), false],
	"tuft": ["trava", Vector3.ONE, true],
	"grave": ["kamin", Vector3(0.35, 0.5, 0.35), true],
	"crag": ["skelia", Vector3(0.4, 0.4, 0.4), true],
}
## What grows or lies on a cell: in the middle of a raised place it rises with it.
const NATURAL := ["fir", "bush", "boulder", "rock", "pebbles", "stump", "tuft", "grave"]
## Drawn by the ground itself (raised when blocked), not by a prop.
const AS_GROUND := ["cliff", "wall"]
## One piece over all the blocked cells it covers.
const CLUSTERS := {"tent": "shatro", "hut": "khata"}

static var _tiles := {}

var kinds: Array = []
## Per part of the map (x + y * w * PARTS): the kind (index into kinds) and how high it rises.
var part_kind := PackedInt32Array()
var part_raise := PackedFloat32Array()
## Per part: 1 where it is the face of a cliff (its slope painted as rock).
var part_face := PackedByteArray()
## Per cell (x + y * w): the main kind and how high it rises.
var cell_kind := PackedInt32Array()
var cell_raise := PackedFloat32Array()
var props: Array[Node3D] = []
## What paints the ground (map_ground.gdshader), shared by its chunks (GroundMesh), and the
## water (none on a map without it).
var ground_material: ShaderMaterial
var water_material: ShaderMaterial


static func tiles() -> Dictionary:
	if _tiles.is_empty():
		var f := FileAccess.open(TILES_PATH, FileAccess.READ)
		if f != null:
			var data: Variant = JSON.parse_string(f.get_as_text())
			if typeof(data) == TYPE_DICTIONARY:
				_tiles = data
	return _tiles


## What the tile shows standing on a cell ("" for plain ground).
static func prop_of(tile: int) -> String:
	return String(tiles().get("props", {}).get(str(tile), ""))


func build(data: Dictionary) -> void:
	map = data
	w = int(map.get("w", 0))
	h = int(map.get("h", 0))
	for child in get_children():
		child.queue_free()
	breakables.clear()
	props.clear()
	_standing.clear()
	kinds = tiles().get("kinds", [])
	_layout()
	_build_ground()
	_build_water()
	_build_props()
	_build_objects()
	_build_grass()
	_build_collision()


# ---- what each part of the map is ----------------------------------------------------------


func _layout() -> void:
	var pw := w * PARTS
	part_kind.resize(pw * h * PARTS)
	part_raise.resize(pw * h * PARTS)
	part_face.resize(pw * h * PARTS)
	part_face.fill(0)
	cell_kind.resize(w * h)
	cell_raise.resize(w * h)
	var ground: Dictionary = tiles().get("ground", {})
	var water := kinds.find("water")
	var wood := kinds.find("wood")
	for y in h:
		for x in w:
			var g := cell("ground", x, y)
			var u := cell("upper", x, y)
			var gparts: Array = ground.get(str(g), [])
			var uparts: Array = []
			if u != 0 and (prop_of(u) == "" or prop_of(u) in AS_GROUND):
				uparts = ground.get(str(u), [])
			var main := _main_kind(gparts)
			# a fence or a palisade does not stand in water: a deck of boards under it
			var decked := prop_of(u) in ["fence", "palisade"]
			var cell_kinds: Array[int] = []
			for i in PARTS * PARTS:
				var k := main
				if i < uparts.size() and int(uparts[i]) >= 0:
					k = int(uparts[i])
				elif i < gparts.size() and int(gparts[i]) >= 0:
					k = int(gparts[i])
				if decked and k == water:
					k = wood
				cell_kinds.append(k)
			cell_kind[y * w + x] = _main_kind(cell_kinds)
			cell_raise[y * w + x] = _raise_of(x, y, cell_kinds)
			for i in PARTS * PARTS:
				part_kind[(y * PARTS + i / PARTS) * pw + x * PARTS + i % PARTS] = cell_kinds[i]
	_fill_pits()
	for y in h:
		for x in w:
			for i in PARTS * PARTS:
				part_raise[(y * PARTS + i / PARTS) * pw + x * PARTS + i % PARTS] = cell_raise[
					y * w + x
				]
	_slope_cliffs()


## A blocked cell with something standing on it (pebbles, a bush, a fir) in the middle of a
## raised place rises with it, the thing on its top.
func _fill_pits() -> void:
	var lifted := {}
	for y in h:
		for x in w:
			var what := prop_of(cell("upper", x, y))
			if (
				cell_raise[y * w + x] > 0.0
				or (cell("flags", x, y) & FLAG_BLOCKED) == 0
				or cell("objects", x, y) != 0
				or not what in NATURAL
			):
				continue
			var around: Array[float] = []
			for d in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
				var n: Vector2i = Vector2i(x, y) + d
				if (
					n.x >= 0
					and n.y >= 0
					and n.x < w
					and n.y < h
					and cell_raise[n.y * w + n.x] > 0.0
				):
					around.append(cell_raise[n.y * w + n.x])
			if around.size() >= 3:
				lifted[y * w + x] = around.min()
	for at in lifted:
		cell_raise[at] = lifted[at]


## The cells of rock under the top of a cliff (the rows of its face in the tiles) are its face:
## the ground climbs across them from the foot to the top, painted as rock.
func _slope_cliffs() -> void:
	var rock := kinds.find("rock")
	var pw := w * PARTS
	for x in w:
		var y := 0
		while y < h:
			if not _is_face(x, y, rock):
				y += 1
				continue
			var top := y - 1
			while y < h and _is_face(x, y, rock):
				y += 1
			var rows := (y - 1 - top) * PARTS  # the part rows of the face, from the top down
			var height := cell_raise[top * w + x] if top >= 0 else float(RAISE["rock"])
			if top >= 0 and cell_raise[top * w + x] <= 0.0:
				continue  # a rock standing alone: as it is
			for r in rows:
				var py := (top + 1) * PARTS + r
				for i in PARTS:
					var at := py * pw + x * PARTS + i
					part_raise[at] = height * float(rows - r) / float(rows + 1)
					part_face[at] = 1


func _is_face(x: int, y: int, rock: int) -> bool:
	return cell_raise[y * w + x] > 0.0 and cell_kind[y * w + x] == rock


func _main_kind(parts: Array) -> int:
	var count := {}
	for k in parts:
		if int(k) >= 0:
			count[int(k)] = int(count.get(int(k), 0)) + 1
	var best := maxi(kinds.find("meadow"), 0)
	var n := 0
	for k in count:
		if count[k] > n:
			best = k
			n = count[k]
	return best


## How high a cell rises: a blocked cell of ground (or of a cliff or wall tile) by its kind.
func _raise_of(x: int, y: int, cell_kinds: Array[int]) -> float:
	if (cell("flags", x, y) & FLAG_BLOCKED) == 0 or cell("objects", x, y) != 0:
		return 0.0
	var u := cell("upper", x, y)
	if u != 0 and prop_of(u) != "" and not prop_of(u) in AS_GROUND:
		return 0.0
	var main := _main_kind(cell_kinds)
	return float(RAISE.get(_kind_name(main), 0.0))


func _kind_name(k: int) -> String:
	return String(kinds[k]) if k >= 0 and k < kinds.size() else "meadow"


## The kind and height of a part and whether it is a cliff's face (px, py in parts; outside
## the map: the nearest edge part).
func _part(px: int, py: int) -> Array:
	var cx := clampi(px, 0, w * PARTS - 1)
	var cy := clampi(py, 0, h * PARTS - 1)
	var at := cy * w * PARTS + cx
	return [part_kind[at], part_raise[at], part_face[at]]


## How high the ground is in the middle of cell (x, y).
func height_of(x: int, y: int) -> float:
	return float(_part(x * PARTS + PARTS / 2, y * PARTS + PARTS / 2)[1])


## The height of the land around the map: low hills rising away from the edge.
func hills(x: float, z: float) -> float:
	var out := maxf(maxf(-x, x - w), maxf(-z, z - h))
	if out <= 0.0:
		return 0.0
	var wave := 0.6 + 0.4 * sin(x * 0.31 + cos(z * 0.23) * 2.0) * cos(z * 0.27 - x * 0.11)
	return smoothstep(0.5, 8.0, out) * 2.6 * wave


# ---- the ground ----------------------------------------------------------------------------


func _build_ground() -> void:
	var lo := -MARGIN * PARTS
	var nx := (w + 2 * MARGIN) * PARTS + 1
	var nz := (h + 2 * MARGIN) * PARTS + 1
	var grid := GroundMesh.new(nx, nz, 1.0 / PARTS)
	for j in nz:
		for i in nx:
			_ground_vertex(grid, lo + i, lo + j)
	ground_material = ShaderMaterial.new()
	ground_material.shader = GROUND_SHADER
	add_child(grid.build(ground_material))


## The ground's vertex at the corner (vx, vz) of four parts: their colours mixed, its height
## (raised when all four are, sunk under water when all four are wet), the detail of their
## kinds (pebbles, planks, paving) and of a cliff's face.
func _ground_vertex(grid: GroundMesh, vx: int, vz: int) -> void:
	var colour := Color(0, 0, 0, 0)
	var detail := [0.0, 0.0, 0.0]
	var raised := 0
	var lowest := 99.0
	var wet := 0
	var face := 0.0
	var cliff := 0.0
	for d in [Vector2i(-1, -1), Vector2i(0, -1), Vector2i(-1, 0), Vector2i(0, 0)]:
		var p: Array = _part(vx + d.x, vz + d.y)
		var name := _kind_name(p[0])
		var c: Color = KIND_COLOUR.get(name, KIND_COLOUR["meadow"])
		colour += Color(c.r, c.g, c.b, 0.0) * 0.25
		if DETAIL.has(name):
			detail[DETAIL[name]] += 0.25
		if float(p[1]) > 0.0:
			raised += 1
			lowest = minf(lowest, float(p[1]))
			face += float(FACE.get(name, 0.0))
		if name == "water":
			wet += 1
		cliff += 0.25 * int(p[2])
	var x := float(vx) / PARTS
	var z := float(vz) / PARTS
	var y := hills(x, z)
	if raised == 4:
		y += lowest + (_wobble(x, z) * 0.08 if face / raised < 0.4 else 0.0)
	elif wet == 4:
		y -= WATER_DEPTH
	colour.a = face / raised if raised > 0 else 0.0
	grid.add(Vector3(x, y, z), colour)
	grid.add_uv(Vector2(detail[0], detail[1]), Vector2(detail[2], cliff))


static func _wobble(x: float, z: float) -> float:
	return sin(x * 2.3 + z * 1.1) * cos(z * 1.9 - x * 0.7)


func _build_water() -> void:
	var any := false
	var water := kinds.find("water")
	for k in part_kind:
		if k == water:
			any = true
			break
	if not any:
		return
	var q := PlaneMesh.new()
	q.size = Vector2(w + 2.0, h + 2.0)
	var mi := MeshInstance3D.new()  # standards: allow nodes_in_code (the map's water)
	mi.name = "Water"
	mi.mesh = q
	mi.position = Vector3(w / 2.0, WATER_LEVEL, h / 2.0)
	water_material = ShaderMaterial.new()
	water_material.shader = WATER_SHADER
	mi.material_override = water_material
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mi)


# ---- what stands on the map ----------------------------------------------------------------


func _build_props() -> void:
	var holder := Node3D.new()  # standards: allow nodes_in_code (the map's props)
	holder.name = "Props"
	add_child(holder)
	var clustered := {}  # Vector2i -> class, the blocked cells of tents and huts
	for y in h:
		for x in w:
			var flags := cell("flags", x, y)
			var what := prop_of(cell("upper", x, y))
			if what == "" or what in AS_GROUND or cell("objects", x, y) != 0:
				continue
			var blocked := (flags & FLAG_BLOCKED) != 0
			if CLUSTERS.has(what):
				if blocked:
					clustered[Vector2i(x, y)] = what
				continue
			if not blocked and (flags & FLAG_OVER) != 0:
				continue  # the top of something drawn over the people: its foot stands below
			if what == "fir" and prop_of(cell("upper", x, y + 1)) == "fir":
				continue  # one fir for the cells of one tree: at its foot
			_stand(holder, what, x, y, false)
	_build_clusters(holder, clustered)
	# crags here and there on the faces of the cliffs
	for y in h:
		for x in w:
			if (
				int(_part(x * PARTS + 1, y * PARTS + 1)[2]) == 1
				and hash(Vector2i(x, y) * 31) % 100 < 30
			):
				_stand(holder, "crag", x, y, false).position.y -= 0.1


## A prop of `what` on cell (x, y); breakable: marked as one (ArtKit.breakable_prop).
func _stand(parent: Node3D, what: String, x: int, y: int, breakable: bool) -> Node3D:
	var spec: Array = PROP.get(what, [])
	if spec.is_empty():
		return null
	var node := ArtKit.breakable_prop(spec[0]) if breakable else ArtKit.prop(spec[0])
	var rng := RandomNumberGenerator.new()
	rng.seed = hash(Vector2i(x, y))
	var scale_by: Vector3 = spec[1] * rng.randf_range(0.9, 1.1)
	if what in ["fence", "palisade"]:
		scale_by = spec[1]
	node.scale = scale_by
	node.position = Vector3(x + 0.5, height_of(x, y), y + 0.5)
	if spec[2]:
		node.rotation.y = rng.randf() * TAU
	elif what in ["fence", "palisade"] and not _along_x(x, y):
		node.rotation.y = PI / 2.0
	parent.add_child(node)
	props.append(node)
	if what == "fire":
		ArtEffects.campfire(node, Vector3(0.0, 0.1, 0.0))
	return node


## A fence runs along X unless its neighbours run along Z.
func _along_x(x: int, y: int) -> bool:
	var fences := ["fence", "palisade"]
	if prop_of(cell("upper", x - 1, y)) in fences or prop_of(cell("upper", x + 1, y)) in fences:
		return true
	return not (
		prop_of(cell("upper", x, y - 1)) in fences or prop_of(cell("upper", x, y + 1)) in fences
	)


## Each group of touching blocked cells of a tent (or a hut) is one tent over its middle.
func _build_clusters(parent: Node3D, clustered: Dictionary) -> void:
	var seen := {}
	for start in clustered:
		if seen.has(start):
			continue
		var what: String = clustered[start]
		var lo: Vector2i = start
		var hi: Vector2i = start
		var todo: Array[Vector2i] = [start]
		seen[start] = true
		while not todo.is_empty():
			var c: Vector2i = todo.pop_back()
			lo = Vector2i(mini(lo.x, c.x), mini(lo.y, c.y))
			hi = Vector2i(maxi(hi.x, c.x), maxi(hi.y, c.y))
			for d in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
				var n: Vector2i = c + d
				if clustered.get(n, "") == what and not seen.has(n):
					seen[n] = true
					todo.append(n)
		var size := Vector2(hi - lo) + Vector2.ONE
		var node := ArtKit.prop(CLUSTERS[what])
		var s := clampf(size.x / (4.6 if what == "tent" else 5.4), 0.4, 1.2)
		node.scale = Vector3.ONE * s
		node.position = Vector3(lo.x + size.x / 2.0, 0.0, lo.y + size.y / 2.0)
		parent.add_child(node)
		props.append(node)


## Draws only these cells (as MapBuilder.show_only; empty: all): the ground and the water of
## the others darker (a mask the shaders read), the props on them hidden. The breakables'
## nodes stay (the mission screen hides them by is_shown); collision stays.
func show_only(cells: Dictionary) -> void:
	_shown = cells
	var img := Image.create(maxi(w, 1), maxi(h, 1), false, Image.FORMAT_L8)
	for y in h:
		for x in w:
			img.set_pixel(x, y, Color.WHITE if is_shown(x, y) else Color.BLACK)
	var tex := ImageTexture.create_from_image(img)
	for m: ShaderMaterial in [ground_material, water_material]:
		if m != null:
			m.set_shader_parameter("view_mask", tex)
			m.set_shader_parameter(
				"view_rect", Vector4(0, 0, w, h) if not cells.is_empty() else Vector4.ZERO
			)
	for node in props:
		if (
			is_instance_valid(node)
			and node.get_parent() != null
			and node.get_parent().name == "Props"
		):
			node.visible = is_shown(floori(node.position.x), floori(node.position.z))


## The breakable objects (MapSim.breakables) as props, named Object_x_y like MapBuilder's.
func _build_objects() -> void:
	for y in h:
		for x in w:
			var kind := cell("objects", x, y)
			if kind == 0:
				continue
			var node := Node3D.new()  # standards: allow nodes_in_code (an object of the map)
			node.name = "Object_%d_%d" % [x, y]
			add_child(node)
			var piece := _stand(
				node, prop_of(kind) if PROP.has(prop_of(kind)) else "barrel", x, y, true
			)
			node.set_meta("kind", kind)
			node.set_meta("hp", 41 if kind in [101, 113] else 21)
			node.set_meta("material", _material_of(piece))
			breakables.append(node)


static func _material_of(node: Node) -> Material:
	if node is MeshInstance3D and (node as MeshInstance3D).material_override != null:
		return (node as MeshInstance3D).material_override
	for c in node.get_children():
		var m := _material_of(c)
		if m != null:
			return m
	return null


## Grass on the meadows, in and around the map, and fields of wheat on the land around it,
## swaying in the wind (Grass). Grass grows thick on lush grass, thinner on a meadow, in the
## colour of its ground leaning to green; a field is a block of land past the edge (FIELD).
func _build_grass() -> void:
	var grass := Grass.new()
	var rng := RandomNumberGenerator.new()
	rng.seed = w * 7919 + h
	var meadow := kinds.find("meadow")
	var lush := kinds.find("grass")
	for py in range(-MARGIN * PARTS / 2, (h + MARGIN / 2) * PARTS):
		for px in range(-MARGIN * PARTS / 2, (w + MARGIN / 2) * PARTS):
			var p: Array = _part(px, py)
			var kind := int(p[0])
			if not kind in [meadow, lush] or float(p[1]) > 0.0:
				continue
			var x := (px + rng.randf()) / PARTS
			var z := (py + rng.randf()) / PARTS
			if in_field(x, z):
				if rng.randf() < Grass.WHEAT_DENSITY:
					grass.add("wheat", Vector3(x, hills(x, z), z), Grass.WHEAT, rng)
				continue
			var ground := "grass" if kind == lush else "meadow"
			if rng.randf() > float(Grass.DENSITY[ground]):
				continue
			var colour: Color = KIND_COLOUR[ground].lerp(Grass.GREEN, Grass.GREENER)
			grass.add("grass", Vector3(x, hills(x, z), z), colour, rng)
	grass.build(self)


## Whether (x, z) is in a field of wheat: blocks of Grass.FIELD metres on the land past the map's
## edge, about half of them sown.
func in_field(x: float, z: float) -> bool:
	if x > -1.0 and x < w + 1.0 and z > -1.0 and z < h + 1.0:
		return false
	var block := Vector2i(floori(x / Grass.FIELD.x), floori(z / Grass.FIELD.y))
	return (hash([block, w, h]) & 0xff) < Grass.SOWN
