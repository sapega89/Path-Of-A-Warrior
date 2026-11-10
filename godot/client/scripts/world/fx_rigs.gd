class_name FxRigs
extends Node3D
## The effects drawn in code are made of rigs: a Node3D for each effect shown, built once by
## _build_<kind>(rig) and kept in a pool by its kind. A rig's parts are quads (or an open
## cylinder) of light (fx_light.gdshader) or of dust and smoke (fx_puff.gdshader); the
## functions here make them, place them on the map and set how they look.

const LIGHT := preload("res://assets/art/shaders/fx_light.gdshader")
const PUFF := preload("res://assets/art/shaders/fx_puff.gdshader")
const PX := 1.0 / 27.0

## The shapes of fx_light.gdshader.
enum Shape { GLOW, RING, STAR, FLAME, BOLT, STREAK, RIBBON, SPIRAL, COLUMN, MOTES, SPLASH, SWEEP }
## How a part turns to the camera (fx_common.gdshaderinc).
enum Turn { PLACED, FACING, UPRIGHT, AXIS }

## Colours (sRGB): [core, edge].
const WARM := [Color(1.0, 0.95, 0.8), Color(0.83, 0.65, 0.27)]
const HOT := [Color(1.0, 0.92, 0.66), Color(0.91, 0.4, 0.14)]
const HEAL := [Color(0.88, 1.0, 0.82), Color(0.36, 0.74, 0.44)]
const STORM := [Color(0.93, 0.96, 1.0), Color(0.42, 0.5, 0.98)]
const WATER := [Color(0.9, 0.96, 1.0), Color(0.27, 0.5, 0.84)]
const STEEL := [Color(1.0, 1.0, 0.97), Color(0.7, 0.76, 0.86)]
const DUST := [Color(0.94, 0.89, 0.79), Color(0.73, 0.65, 0.55)]
const SMOKE := [Color(0.48, 0.44, 0.41), Color(0.3, 0.27, 0.25)]

var _pools := {}  # kind -> Array of rigs (Node3D)
var _used := {}  # kind -> rigs used by the last call
static var _tube_mesh: ArrayMesh


func _rig(kind: String) -> Node3D:
	var pool: Array = _pools.get(kind, [])
	_pools[kind] = pool
	var i := int(_used.get(kind, 0))
	_used[kind] = i + 1
	if i < pool.size():
		return pool[i]
	var rig := Node3D.new()
	rig.name = "%s%d" % [kind.capitalize(), i]
	add_child(rig)
	call("_build_" + kind, rig)
	pool.append(rig)
	return rig


## A part of light: a quad (or an open cylinder) with fx_light in a shape.
func _light(
	rig: Node3D,
	part: String,
	shape: Shape,
	turn: Turn,
	colours: Array,
	body := 0.0,
	cylinder := false
) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	mi.name = part
	if cylinder:
		mi.mesh = _tube()
	else:
		var q := QuadMesh.new()
		q.size = Vector2.ONE
		mi.mesh = q
	var m := ShaderMaterial.new()
	m.shader = LIGHT
	m.set_shader_parameter("shape", shape)
	m.set_shader_parameter("billboard", turn)
	m.set_shader_parameter("body", body)
	_colours(m, colours)
	mi.material_override = m
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mi.extra_cull_margin = 4.0
	rig.add_child(mi)
	return mi


## An open cylinder 1 across and 1 high, its middle at the origin: UV.x goes round it, UV.y
## from the top (0) to the bottom (1).
static func _tube() -> ArrayMesh:
	if _tube_mesh != null:
		return _tube_mesh
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var n := 24
	for i in n:
		var u0 := float(i) / n
		var u1 := float(i + 1) / n
		var a := Vector3(cos(u0 * TAU), 0.0, sin(u0 * TAU))
		var b := Vector3(cos(u1 * TAU), 0.0, sin(u1 * TAU))
		var top := Vector3(0.0, 0.5, 0.0)
		for v in [
			[a + top, Vector2(u0, 0.0)],
			[b + top, Vector2(u1, 0.0)],
			[b - top, Vector2(u1, 1.0)],
			[a + top, Vector2(u0, 0.0)],
			[b - top, Vector2(u1, 1.0)],
			[a - top, Vector2(u0, 1.0)]
		]:
			st.set_uv(v[1])
			st.add_vertex(v[0])
	_tube_mesh = st.commit()
	return _tube_mesh


## A part of dust or smoke.
func _puff(rig: Node3D, part: String, turn: Turn, colours: Array) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	mi.name = part
	var q := QuadMesh.new()
	q.size = Vector2.ONE
	mi.mesh = q
	var m := ShaderMaterial.new()
	m.shader = PUFF
	m.set_shader_parameter("billboard", turn)
	m.set_shader_parameter("color", _rgb(colours[0]))
	m.set_shader_parameter("shade", _rgb(colours[1]))
	mi.material_override = m
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mi.extra_cull_margin = 4.0
	rig.add_child(mi)
	return mi


static func _rgb(c: Color) -> Vector3:
	return Vector3(c.r, c.g, c.b)


static func _colours(m: ShaderMaterial, colours: Array) -> void:
	m.set_shader_parameter("core", _rgb(colours[0]))
	m.set_shader_parameter("edge", _rgb(colours[1]))


## Sets a part's shader values and shows it (strength 0 hides it).
static func _tune(part: MeshInstance3D, values: Dictionary) -> void:
	var m := part.material_override as ShaderMaterial
	for k in values:
		m.set_shader_parameter(k, values[k])
	part.visible = float(values.get("strength", 1.0)) > 0.001


## A quad lying on the ground, `size` across, at `at`.
static func _flat(part: Node3D, at: Vector3, size: float) -> void:
	part.transform = Transform3D(
		Basis(Vector3.RIGHT, -PI / 2.0) * Basis.from_scale(Vector3(size, size, 1.0)),
		at + Vector3(0.0, 0.03, 0.0)
	)


## A quad facing the camera (or upright), w by h, its middle at `at`.
static func _quad(part: Node3D, at: Vector3, w: float, h := -1.0) -> void:
	part.transform = Transform3D(Basis.from_scale(Vector3(w, h if h > 0.0 else w, 1.0)), at)


## A quad from `a` to `b` (turned to the camera about that line), w wide.
static func _span(part: Node3D, a: Vector3, b: Vector3, w: float) -> void:
	var x := b - a
	if x.length() < 0.001:
		x = Vector3(0.001, 0.0, 0.0)
	var y := (
		x.cross(Vector3.FORWARD if absf(x.normalized().y) > 0.9 else Vector3.UP).normalized() * w
	)
	part.transform = Transform3D(Basis(x, y, x.cross(y).normalized()), (a + b) / 2.0)


## An open cylinder standing on `at`, r around and h high.
static func _pillar(part: Node3D, at: Vector3, r: float, h: float) -> void:
	part.transform = Transform3D(
		Basis.from_scale(Vector3(r, h, r)), at + Vector3(0.0, h / 2.0, 0.0)
	)


static func _at(p: Vector2) -> Vector3:
	return MapPeople.to_world(p)


## The way an 8-direction faces on the ground.
static func _ahead(dir8: int) -> Vector3:
	var yaw := Motion.yaw_of(dir8)
	return Vector3(sin(yaw), 0.0, cos(yaw))


## A place around the middle of the room (px) for a strike of a room-wide skill, the same
## for the same frame.
static func scatter(kind: String, frame: int, rx: float, ry: float) -> Vector2:
	var rng := RandomNumberGenerator.new()
	rng.seed = hash([kind, frame])
	return Vector2(rng.randf_range(-rx, rx), rng.randf_range(-ry, ry))


static func _seed(p: Vector2, n := 0) -> float:
	return fposmod(p.x * 0.137 + p.y * 0.291 + n * 1.618, 10.0)


## How far through a run of frames, rising smoothly across the ticks: from a little after 0
## on its first frame to a little before 1 on its last, so that every frame the simulation
## shows has something to see.
static func _run(frame: int, t: float, frames: int) -> float:
	return clampf((float(frame) + 0.1 + 0.8 * clampf(t, 0.0, 1.0)) / float(frames), 0.0, 1.0)


## Fades in at the start and out at the end of a run.
static func _swell(x: float, rise := 0.15, fall := 0.25) -> float:
	return smoothstep(0.0, rise, x) * (1.0 - smoothstep(1.0 - fall, 1.0, x))
