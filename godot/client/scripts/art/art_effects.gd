class_name ArtEffects
extends RefCounted
## Effects in the new art (scenes/art/effects): the sabre trail, sparks where steel meets steel,
## dust under feet, the campfire.

const SLASH := preload("res://scenes/art/effects/slash.tscn")
const SPARKS := preload("res://scenes/art/effects/sparks.tscn")
const DUST := preload("res://scenes/art/effects/dust.tscn")
const CAMPFIRE := preload("res://scenes/art/effects/campfire.tscn")


## A curved ribbon of light that follows the blade (SweepMesh): `arc` degrees around the
## attacker, from `start` degrees (0 = in front, +Z). `life` 0..1 runs the sweep.
static func slash(
	parent: Node3D,
	center: Vector3,
	start_deg: float,
	arc_deg := 150.0,
	radius := 1.15,
	height := 1.1,
	tilt := 0.35,
	life := 0.5
) -> MeshInstance3D:
	var sweep := SweepMesh.new()
	sweep.start_deg = start_deg
	sweep.arc_deg = arc_deg
	sweep.radius = radius
	sweep.height = height
	sweep.tilt = tilt
	var mi := SLASH.instantiate() as MeshInstance3D
	mi.mesh = sweep
	(mi.material_override as ShaderMaterial).set_shader_parameter("life", life)
	mi.position = center
	parent.add_child(mi)
	return mi


## A burst of sparks, `amount` of them.
static func sparks(parent: Node3D, at: Vector3, amount := 26) -> CPUParticles3D:
	return _burst(SPARKS, parent, at, amount)


## A puff of dust, `amount` clouds.
static func dust(parent: Node3D, at: Vector3, amount := 10) -> CPUParticles3D:
	return _burst(DUST, parent, at, amount)


static func _burst(scene: PackedScene, parent: Node3D, at: Vector3, amount: int) -> CPUParticles3D:
	var p := scene.instantiate() as CPUParticles3D
	p.amount = amount
	p.position = at
	parent.add_child(p)
	p.emitting = true
	return p


## Fire, sparks and smoke over a campfire, with a flickering warm light.
static func campfire(parent: Node3D, at: Vector3) -> Node3D:
	var root := CAMPFIRE.instantiate() as Node3D
	root.position = at
	parent.add_child(root)
	return root
