class_name FxRigs
extends Node3D
## The effects are made of rigs: a scene for each kind (scenes/world/effects/<kind>.tscn),
## instanced once for each effect shown at a time and kept in a pool by its kind. A rig's parts
## are quads (or open cylinders, OpenCylinderMesh) of light (fx_light.gdshader), of blood
## (fx_blood.gdshader) or of dust and smoke (fx_puff.gdshader); the functions here place them on
## the map and set how they look.

const RIG_PATH := "res://scenes/world/effects/%s.tscn"
const PX := 1.0 / 27.0

var _pools := {}  # kind -> Array of rigs (Node3D)
var _used := {}  # kind -> rigs used by the last call


func _rig(kind: String) -> Node3D:
	var pool: Array = _pools.get(kind, [])
	_pools[kind] = pool
	var i := int(_used.get(kind, 0))
	_used[kind] = i + 1
	if i < pool.size():
		return pool[i]
	var rig := (load(RIG_PATH % kind) as PackedScene).instantiate() as Node3D
	rig.name = "%s%d" % [kind.capitalize(), i]
	add_child(rig)
	pool.append(rig)
	return rig


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
