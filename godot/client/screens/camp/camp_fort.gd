class_name CampFort
extends Node3D
## The camp between missions in the new art, «Плавні», built from its CampPlan: a ring of
## palisade on dry ground among water channels and reeds, at dusk. Each way on is a gate in
## the ring (the main gate with its icon in the south, side gates elsewhere) with a road to the
## yard and a dry causeway across the water; past it lies the land of that place (LAND). A
## closed way's gate is barred. In the middle the yard with two fires, the town hall's big
## tent, gone grey with smoke, north-west of it; round them the smithy (an anvil by its forge),
## smoke-dark tents, torches, guards inside the gates. Reeds, bushes and trees round the marsh
## are placed by the camp's own seed, so each place looks its own and the same each time.
## The water and the mist are the scene's (camp_fort.tscn); dusk() turns the world's light
## into the dusk. What stands is a round in the plan (CampPlan.add_solid) and a cylinder in
## `body`; the palisade and the barred gates are boxes in `body`, and the ground is one too.

const TORCH_FLAME := preload("res://screens/camp/torch_flame.tscn")
const DUSK := preload("res://screens/camp/camp_dusk.tres")
## The weak cold moon behind the clouds: colour, energy, the way its light goes.
const MOON_COLOR := Color("a3b0d2")
const MOON_ENERGY := 0.5
const MOON_LIGHT := Vector3(0.45, -0.55, -0.7)
const MOON_SHADOW := 60.0  # metres its shadows reach
## A campfire's warm light at dusk: colour, energy, reach (metres); it casts shadows.
const FIRE_LIGHT := [Color("ff9443"), 2.1, 9.0]
const LIGHT_FALLOFF := 1.6
## The Compatibility renderer lights one mesh (the ground) with this many lights at most:
## the fires first, then the torches while they last.
const LIGHTS := 8
const FLICKER := 9.0  # how fast the flames flicker
const TORCH_HEIGHT := 2.12  # the flame over the foot of the pole
## The town hall's tent, gone grey with smoke and rain (the painted shader's tint).
const SMOKED := Color(0.62, 0.6, 0.56)
const HALL_SCALE := 1.6
const PALISADE_HEIGHT := 3.0
const PALISADE_DEPTH := 0.5
const BAR_INSIDE := 1.2  # a barred gate's palisade stands this far inside the ring
const PERSON := 0.4  # metres round a person standing
const MOAT_STEP := 6.0  # degrees of one piece of a water channel
## The ground: its size, how fine its grid, the flat middle, the colours of the marsh.
const GROUND_SIZE := 130.0
const GROUND_STEP := 0.6
const PLAY := Rect2(-34, -34, 68, 60)
const SOIL := Color("6c5a3e")
const GRASS_DRY := Color("5c6440")
const GRASS_GREEN := Color("3f5530")
const TUFTS := 900
const ROAD_WIDTH := 1.2
const YARD_SIZE := Vector2(5.4, 4.6)  # the trodden yard's half width and half depth
## Green patches round the marsh and in the camp: Vector3(x, z, radius).
const GREENS := [
	Vector3(-22, -12, 8),
	Vector3(22, -13, 8),
	Vector3(-23, 12, 8),
	Vector3(23, 13, 8),
	Vector3(0, -26, 9),
	Vector3(-9, -4, 3.5),
	Vector3(9, -7, 3.5),
	Vector3(-4, 11, 3),
]
## Two creeks running off the moat to the east and the west.
const CREEKS := [
	[Vector2(19.6, -3.0), Vector2(25.0, -6.5), Vector2(30.0, -5.0), Vector2(36.0, -9.0)],
	[Vector2(-19.6, -3.0), Vector2(-24.5, -7.0), Vector2(-30.0, -6.0), Vector2(-36.0, -10.0)],
]
## Tents round the yard: [x, z, yaw, scale].
const TENTS := [
	[-11.5, -3.2, 75.0, 1.5],
	[-11.0, 4.2, 105.0, 1.4],
	[11.8, -4.6, -70.0, 1.5],
	[12.4, 6.4, -100.0, 1.35],
	[-3.2, -12.6, 10.0, 1.3],
	[6.2, -12.2, -15.0, 1.35],
]
## Things that stand about the camp: [prop, x, z, yaw, how much of its width blocks].
const ABOUT := [["harmata", -11.2, -6.4, 230.0, 0.8], ["stoiak", 3.0, -10.0, 30.0, 0.8]]
## The land past a gate, by the land of its place: pieces [kind, ahead, aside, scale], ahead
## of the causeway's end and aside of the way on (metres). Only LOW pieces stand in the
## south, where a tall one would stand before the camera.
const LAND := {
	"mountains": [["skelia", 2.5, -4.0, 1.3], ["skelia", 4.5, 4.2, 1.6], ["kamin", 1.5, -2.4, 1.4]],
	"forest":
	[
		["yalyna", 2.0, -3.6, 1.2],
		["yalyna", 2.6, 3.8, 1.3],
		["yalyna", 5.0, -5.0, 1.4],
		["dub", 5.4, 4.6, 1.2],
		["kushch", 1.2, -2.2, 1.0],
	],
	"town":
	[
		["tyn", 1.4, -3.0, 1.0],
		["tyn", 1.4, 3.0, 1.0],
		["khata", 4.6, -4.6, 0.9],
		["zhuravel", 3.6, 4.0, 1.0],
	],
	"steppe":
	[
		["stih", 2.2, -3.2, 0.9],
		["kushch", 2.6, 3.4, 1.1],
		["kamin", 3.4, -1.8, 0.9],
		["stih", 4.6, 4.0, 0.8],
	],
	"lake":
	[
		["kushch", 1.6, -2.8, 0.9],
		["kamin", 2.0, 2.8, 1.0],
		["ochert", 3.0, -1.6, 1.2],
		["ochert", 3.2, 1.8, 1.2],
	],
}
const LOW := ["kushch", "kamin", "stih", "ochert", "tyn"]
const LAND_PAST := 2.5  # the land begins this far past the moat
const SOUTH_SIDE := 45.0  # degrees each side of the south where only low land stands
## The marsh round the camp: reeds by the water, bushes past it, trees behind the camp.
const REED_GAP := 1.2  # metres along the water between two places for reeds
const REED_SKIP := 0.45  # how many of those stay bare
const BUSHES := 12
const TREES := ["topolia", "dub", "yalyna", "topolia"]
const TREE_COUNT := 10

var plan: CampPlan
var ground: ArtGround
var figures: Array[ArtFigure] = []
var hall: Node3D
var body: StaticBody3D
## The flickering lights of the fires and torches: [light, its energy, a phase].
var _flames: Array = []
var _lights_left := LIGHTS
var _time := 0.0
var _rng := RandomNumberGenerator.new()


## Builds the camp of `camp_plan`. lands: the land past each way ("lake", "mountains",
## "forest", "town" or "steppe", CampScreen.terrain()); seed_value: the camp's own.
func build(camp_plan: CampPlan, lands: Array, seed_value: int) -> void:
	plan = camp_plan
	_rng.seed = seed_value
	body = StaticBody3D.new()  # standards: allow nodes_in_code (the solids of the plan)
	body.name = "Solid"
	add_child(body)
	_box(Vector3(0.0, -0.5, 0.0), Vector3(GROUND_SIZE, 1.0, GROUND_SIZE), 0.0)
	_ground()
	_palisade()
	_hall_and_yard()
	_smithy()
	_tents()
	_torches()
	_guards()
	_reeds()
	_bushes_and_trees()
	for i in plan.exits.size():
		_land(plan.exits[i], str(lands[i]) if i < lands.size() else "steppe")


## Turns the world's light into the dusk over the marsh: the painted sky, the deep blue
## shade and the mist of camp_dusk.tres, and the sun into a weak cold moon.
static func dusk(world_light: WorldEnvironment, sun: DirectionalLight3D) -> void:
	world_light.environment = DUSK
	sun.light_color = MOON_COLOR
	sun.light_energy = MOON_ENERGY
	sun.directional_shadow_max_distance = MOON_SHADOW
	sun.transform = Transform3D(Basis.looking_at(MOON_LIGHT.normalized(), Vector3.UP), Vector3())


## The fires and torches flicker.
func _process(delta: float) -> void:
	_time += delta
	for f in _flames:
		var t: float = _time * FLICKER + f[2]
		(f[0] as OmniLight3D).light_energy = (
			f[1] * (0.86 + 0.08 * sin(t) + 0.06 * sin(t * 2.3 + 1.7))
		)


# -- the ground ------------------------------------------------------------------------------


## The ground: roads from the gates and the spots to the yard, the water channels round the
## ring (a causeway at each gate) and two creeks, green patches. It casts no shadows: inside the
## palisade it is flat, and the fires' shadows would draw it in every face of their cube maps.
func _ground() -> void:
	var g := ArtGround.new()
	g.name = "Ground"
	g.paths = _roads()
	g.path_width = ROAD_WIDTH
	g.hollows = _channels()
	g.greens = GREENS
	g.play = PLAY
	g.size = GROUND_SIZE
	g.step = GROUND_STEP
	g.tufts = TUFTS
	g.seed_value = _rng.randi()
	g.casts_shadow = false
	add_child(g)
	g.build()
	ground = g
	var m := g.material
	m.set_shader_parameter("soil", SOIL)
	m.set_shader_parameter("grass_dry", GRASS_DRY)
	m.set_shader_parameter("grass_green", GRASS_GREEN)


func _roads() -> Array:
	var roads: Array = []
	var yard := CampPlan.YARD
	for e in plan.exits:
		var far := CampPlan.on_ring(e.angle, CampPlan.RADIUS + 12.0)
		var mid := CampPlan.on_ring(e.angle, CampPlan.RADIUS * 0.55) + yard * 0.5
		var near := CampPlan.on_ring(e.angle, YARD_SIZE.x) + yard
		roads.append(
			PackedVector2Array(
				[Vector2(far.x, far.z), Vector2(mid.x, mid.z), Vector2(near.x, near.z)]
			)
		)
	var ring := PackedVector2Array()
	for i in 17:
		var a := TAU * i / 16.0
		ring.append(Vector2(yard.x + sin(a) * YARD_SIZE.x, yard.z + cos(a) * YARD_SIZE.y))
	roads.append(ring)
	var smith: Vector3 = CampPlan.SPOTS.smith[0]  # a path from the yard to the smithy
	var toward := yard + (smith - yard).normalized() * YARD_SIZE.x
	roads.append(PackedVector2Array([Vector2(toward.x, toward.z), Vector2(smith.x, smith.z)]))
	return roads


## The moat in arcs between the causeways (all round without gates), then the creeks.
func _channels() -> Array:
	var bare: Array[float] = []
	for e in plan.exits:
		bare.append(e.angle)
	bare.sort()
	var channels: Array = []
	if bare.is_empty():
		channels.append(_arc(0.0, 360.0))
	for i in bare.size():
		var after := bare[(i + 1) % bare.size()] + (360.0 if i == bare.size() - 1 else 0.0)
		channels.append(_arc(bare[i] + CampPlan.CAUSEWAY, after - CampPlan.CAUSEWAY))
	for creek in CREEKS:
		channels.append(PackedVector2Array(creek))
	return channels


func _arc(from: float, to: float) -> PackedVector2Array:
	var arc := PackedVector2Array()
	var steps := maxi(ceili((to - from) / MOAT_STEP), 1)
	for k in steps + 1:
		var p := CampPlan.on_ring(lerpf(from, to, float(k) / steps), CampPlan.MOAT)
		arc.append(Vector2(p.x, p.z))
	return arc


# -- the palisade and the gates --------------------------------------------------------------


## The ring piece by piece, a gate in each way out; a closed way's gate is barred.
func _palisade() -> void:
	var step := plan.step
	var r := CampPlan.RADIUS * cos(deg_to_rad(step / 2.0))
	var pieces := PropField.new("palisade")
	for i in roundi(360.0 / step):
		var a := (i + 0.5) * step
		if plan.exits.any(
			func(e: Dictionary) -> bool:
				return CampPlan.apart(a, e.angle) < plan.gate_half_width(e.angle) + 0.1
		):
			continue
		pieces.add(_placed(CampPlan.on_ring(a, r), a))
		_wall(a, r)
	for e in plan.exits:
		var main := CampPlan.gate_pieces(e.angle) == CampPlan.MAIN_GATE_PIECES
		_prop("brama" if main else "vorota", CampPlan.on_ring(e.angle, r), e.angle)
		if e.open:
			continue
		var bars := CampPlan.gate_pieces(e.angle)
		for k in bars:
			var a: float = e.angle + (k - (bars - 1) / 2.0) * step
			pieces.add(_placed(CampPlan.on_ring(a, r - BAR_INSIDE), a))
			_wall(a, r - BAR_INSIDE)
	pieces.build(self)


## A piece of palisade one cannot walk through, at `deg` round the ring, `r` from the middle.
func _wall(deg: float, r: float) -> void:
	var size := Vector3(CampPlan.PIECE, PALISADE_HEIGHT, PALISADE_DEPTH)
	_box(CampPlan.on_ring(deg, r) + Vector3(0.0, PALISADE_HEIGHT / 2.0, 0.0), size, deg)


# -- the middle of the camp ------------------------------------------------------------------


## The town hall's big tent and its banner, the yard's two fires with men round them, and a
## colonel by the hall.
func _hall_and_yard() -> void:
	var at := CampPlan.HALL_AT
	hall = _prop("shatro", at, 0.0, HALL_SCALE)
	var smoked := ArtKit.painted(false)
	smoked.set_shader_parameter("tint", SMOKED)
	ArtKit.dress(hall, smoked)
	_solid(hall, 0.82)
	_solid(_prop("banner", at + Vector3(-3.6, 0.0, 3.0), 15.0), 0.6)
	for f in CampPlan.FIRES:
		_solid(_prop("vohnyshche", f), 0.9)
		var fire := ArtEffects.campfire(self, f)
		_warm(fire, FIRE_LIGHT, true)
	var one: Vector3 = CampPlan.FIRES[0]
	var two: Vector3 = CampPlan.FIRES[1]
	_figure("kozak_svyta", one + Vector3(0.1, 0, -1.25), "sit", one + Vector3(0.6, 0, 2.0), 1.0)
	_figure("kozak_camp", one + Vector3(-1.2, 0, 0.2), "interact", one, 0.45)
	_figure("kozak_camp", two + Vector3(-0.9, 0, -0.9), "cheer", two, 0.55)
	_figure("kozak_svyta", two + Vector3(1.1, 0, -0.5), "sit", two, 1.0)
	_figure("polkovnyk", at + Vector3(-2.4, 0, 3.4), "idle", at + Vector3(-1.0, 0, 8.0), 0.4)


## The smithy: the anvil on its stump, the forge's fire, a rack of weapons, a chest and the
## smith at work.
func _smithy() -> void:
	var at := CampPlan.SMITH_AT
	_solid(_prop("kovadlo", at, 20.0, 1.0, true), 0.9)
	_solid(_prop("kuznya", at + Vector3(1.6, 0.0, -1.6), -90.0), 0.8)
	_solid(_prop("stoiak", at + Vector3(-1.4, 0.0, -0.9), 30.0), 0.8)
	_solid(_prop("skrynia", at + Vector3(1.5, 0.0, 0.6), -12.0, 1.0, true), 0.9)
	_figure("kozak_camp", at + Vector3(0.9, 0.0, -0.5), "attack_chop", at, 0.55)


## Smoke-dark tents round the yard, a cannon, a rack and firewood about.
func _tents() -> void:
	for t in TENTS:
		_solid(_prop("namet_dark", Vector3(t[0], 0.0, t[1]), t[2], t[3]), 0.85)
	for a in ABOUT:
		_solid(_prop(a[0], Vector3(a[1], 0.0, a[2]), a[3]), a[4])
	_solid(_prop("drova", Vector3(9.4, 0.0, -9.2), 40.0), 0.8)


## Torches at the hall's door and on both sides inside every open gate; those past the
## lights the renderer has (LIGHTS) burn without light.
func _torches() -> void:
	var door := CampPlan.HALL_AT + Vector3(0.0, 0.0, 3.4)
	var torches: Array[Vector3] = [door + Vector3(-1.9, 0, 0), door + Vector3(1.9, 0, 0)]
	for e in plan.exits:
		if e.open:
			var half := plan.gate_half_width(e.angle) + 2.5
			torches.append(CampPlan.on_ring(e.angle - half, CampPlan.RADIUS - 1.0))
			torches.append(CampPlan.on_ring(e.angle + half, CampPlan.RADIUS - 1.0))
	for t in torches:
		_solid(_prop("smoloskyp", t, _rng.randf() * 360.0), 0.5)
		var flame: Node3D = TORCH_FLAME.instantiate()
		flame.position = t + Vector3(0.02, TORCH_HEIGHT, 0.0)
		var light: OmniLight3D = flame.get_node("Light")
		if _lights_left > 0:
			_flames.append([light, light.light_energy, _rng.randf() * TAU])
			_lights_left -= 1
		else:
			light.free()
		add_child(flame)


## A guard with a spear inside each gate, by its side, looking into the camp.
func _guards() -> void:
	for e in plan.exits:
		var aside := plan.gate_half_width(e.angle) + 4.5
		var at := CampPlan.on_ring(e.angle + aside, CampPlan.RADIUS - 2.0)
		_figure("kozak_svyta", at, "idle", at - e.out * 3.0, 0.3).equip("spear")


# -- round the marsh -------------------------------------------------------------------------


## Reeds on both banks of the water, but not on the ways out.
func _reeds() -> void:
	var reeds := PropField.new("ochert")
	for line in ground.hollows:
		var pl: PackedVector2Array = line
		for k in pl.size() - 1:
			var across := (pl[k + 1] - pl[k]).normalized().orthogonal()
			var n := ceili(pl[k].distance_to(pl[k + 1]) / REED_GAP)
			for j in n:
				for side in [-1.0, 1.0]:
					if _rng.randf() < REED_SKIP:
						continue
					var p: Vector2 = pl[k].lerp(pl[k + 1], (j + _rng.randf()) / n)
					p += across * side * _rng.randf_range(1.2, 2.1)
					if not _on_way_out(Vector3(p.x, 0.0, p.y), 3.0):
						reeds.add(_standing(p, _rng.randf_range(0.75, 1.25), -0.05))
	reeds.build(self)


## Bushes past the water all round, trees in the north half behind the camp.
func _bushes_and_trees() -> void:
	for k in BUSHES:
		var a := 15.0 + 360.0 / BUSHES * k + _rng.randf_range(-8.0, 8.0)
		var p := CampPlan.on_ring(a, _rng.randf_range(24.0, 28.0))
		if not _on_way_out(p, 6.0):
			_stand("kushch", Vector2(p.x, p.z), _rng.randf_range(1.0, 1.4))
	for k in TREE_COUNT:
		var a := 100.0 + 16.0 * k + _rng.randf_range(-5.0, 5.0)
		var p := CampPlan.on_ring(a, _rng.randf_range(30.0, 36.0))
		if not _on_way_out(p, 8.0):
			_stand(TREES[k % TREES.size()], Vector2(p.x, p.z), _rng.randf_range(1.1, 1.35))


## Whether p lies on the way out of a gate (within `width` metres of its road past the ring).
func _on_way_out(p: Vector3, width: float) -> bool:
	for e in plan.exits:
		var ahead := p.dot(e.out)
		if ahead > CampPlan.RADIUS - 2.0 and (p - e.out * ahead).length() < width:
			return true
	return false


## The land of a way's place past its causeway: a few pieces beside the way on.
func _land(e: Dictionary, land: String) -> void:
	var out: Vector3 = e.out
	var across := Vector3(out.z, 0.0, -out.x)
	var south := CampPlan.apart(e.angle, CampPlan.SOUTH) < SOUTH_SIDE
	for piece in LAND.get(land, LAND["steppe"]):
		if south and not str(piece[0]) in LOW:
			continue
		var ahead := CampPlan.MOAT + LAND_PAST + float(piece[1])
		var p := out * ahead + across * float(piece[2])
		var node := _stand(str(piece[0]), Vector2(p.x, p.z), float(piece[3]))
		node.name = "Land%d" % get_child_count()


# -- pieces ----------------------------------------------------------------------------------


func _prop(what: String, at: Vector3, yaw := 0.0, scale_by := 1.0, outline := false) -> Node3D:
	var node := ArtKit.prop(what, outline)
	node.position = at
	node.rotation_degrees.y = yaw
	node.scale = Vector3.ONE * scale_by
	add_child(node)
	return node


## A prop standing on the ground at p (on its hills and banks), turned any way.
func _stand(what: String, p: Vector2, scale_by: float, sink := 0.0) -> Node3D:
	var node := ArtKit.prop(what)
	node.transform = _standing(p, scale_by, sink)
	add_child(node)
	return node


## Where a prop stands on the ground at p (on its hills and banks), turned any way.
func _standing(p: Vector2, scale_by: float, sink := 0.0) -> Transform3D:
	var at := Vector3(p.x, ground.height(p.x, p.y) + sink, p.y)
	return _placed(at, _rng.randf() * 360.0, scale_by)


## A prop's place: at `at`, turned `yaw` degrees about the vertical, `scale_by` its size.
static func _placed(at: Vector3, yaw: float, scale_by := 1.0) -> Transform3D:
	return Transform3D(Basis(Vector3.UP, deg_to_rad(yaw)).scaled(Vector3.ONE * scale_by), at)


## A person of the camp playing `clip` (at `at_time` seconds and still, or from a random
## moment), facing `face_to`; one cannot walk through him.
func _figure(
	kind: String, at: Vector3, clip: String, face_to: Vector3, at_time := -1.0
) -> ArtFigure:
	var f := ArtFigure.create(kind)
	add_child(f)
	f.position = at
	f.face(face_to - at)
	if at_time >= 0.0:
		f.pose(clip, at_time)
	else:
		f.play(clip, 0.0)
		f.player.seek(_rng.randf() * 0.8, true)
	figures.append(f)
	_round(Vector2(at.x, at.z), PERSON)
	return f


## The light of a fire made warmer and stronger for the dusk (colour, energy, reach), casting
## shadows if `shadows`; it flickers (_process()).
func _warm(flame: Node3D, how: Array, shadows: bool) -> void:
	for light in flame.find_children("*", "OmniLight3D", false, false):
		var l := light as OmniLight3D
		l.light_color = how[0]
		l.light_energy = how[1]
		l.omni_range = how[2]
		l.omni_attenuation = LIGHT_FALLOFF
		l.shadow_enabled = shadows
		_flames.append([l, float(how[1]), _rng.randf() * TAU])
		_lights_left -= 1


## A prop one cannot walk through: a round of `fill` of its widest half over its footprint.
func _solid(node: Node3D, fill := 1.0) -> Node3D:
	var box := _footprint(node)
	var centre := Vector2(box.get_center().x, box.get_center().z)
	_round(centre, maxf(box.size.x, box.size.z) / 2.0 * fill)
	return node


## A round one cannot walk through: in the plan and as a cylinder in the body.
func _round(centre: Vector2, radius: float) -> void:
	plan.add_solid(centre, radius)
	var shape := CollisionShape3D.new()  # standards: allow nodes_in_code (a solid of the plan)
	var c := CylinderShape3D.new()
	c.radius = radius
	c.height = 2.0
	shape.shape = c
	shape.position = Vector3(centre.x, 1.0, centre.y)
	body.add_child(shape)


## The box round a prop's meshes in the camp's space.
func _footprint(node: Node3D) -> AABB:
	var box := AABB()
	var first := true
	for mi in node.find_children("*", "MeshInstance3D", true, false):
		var m := mi as MeshInstance3D
		var to_camp := m.transform
		var up := m.get_parent()
		while up != self:
			to_camp = (up as Node3D).transform * to_camp
			up = up.get_parent()
		var b := to_camp * m.get_aabb()
		box = b if first else box.merge(b)
		first = false
	return box


func _box(at: Vector3, size: Vector3, yaw: float) -> void:
	var shape := CollisionShape3D.new()  # standards: allow nodes_in_code (a solid of the plan)
	var b := BoxShape3D.new()
	b.size = size
	shape.shape = b
	shape.position = at
	shape.rotation_degrees.y = yaw
	body.add_child(shape)
