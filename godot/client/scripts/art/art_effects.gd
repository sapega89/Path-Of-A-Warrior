class_name ArtEffects
extends RefCounted
## Effects in the new art, made in code: the sabre trail, sparks where steel meets steel,
## dust under feet, the campfire.

const SLASH := preload("res://assets/art/shaders/slash.gdshader")


static func _unshaded(color: Color, additive := false) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.vertex_color_use_as_albedo = true
	m.albedo_color = color
	m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	if additive:
		m.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	m.billboard_mode = BaseMaterial3D.BILLBOARD_PARTICLES
	m.cull_mode = BaseMaterial3D.CULL_DISABLED
	return m


static func _ramp(colors: Array) -> Gradient:
	var offsets := PackedFloat32Array()
	var list := PackedColorArray()
	for i in colors.size():
		offsets.append(float(i) / float(colors.size() - 1))
		list.append(colors[i])
	var g := Gradient.new()
	g.offsets = offsets
	g.colors = list
	return g


## A curved ribbon of light that follows the blade: `arc` degrees around the attacker,
## from `start` degrees (0 = in front, +Z). `life` 0..1 runs the sweep.
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
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var steps := 24
	for i in steps + 1:
		var t := float(i) / steps
		var a := deg_to_rad(start_deg + arc_deg * t)
		var dir := Vector3(sin(a), 0.0, cos(a))
		var lift := tilt * (t - 0.5)
		for j in 2:
			var r := radius * (0.55 if j == 0 else 1.0)
			st.set_uv(Vector2(t, float(j)))
			st.add_vertex(dir * r + Vector3(0.0, height + lift * r, 0.0))
	for i in steps:
		var a := i * 2
		st.add_index(a)
		st.add_index(a + 1)
		st.add_index(a + 2)
		st.add_index(a + 1)
		st.add_index(a + 3)
		st.add_index(a + 2)
	var mi := MeshInstance3D.new()
	mi.mesh = st.commit()
	var m := ShaderMaterial.new()
	m.shader = SLASH
	m.set_shader_parameter("life", life)
	mi.material_override = m
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mi.position = center
	parent.add_child(mi)
	return mi


static func sparks(parent: Node3D, at: Vector3, amount := 26) -> CPUParticles3D:
	var p := CPUParticles3D.new()
	p.amount = amount
	p.lifetime = 0.45
	p.one_shot = true
	p.explosiveness = 0.95
	p.mesh = _spark_mesh()
	p.direction = Vector3(0, 0.6, 1)
	p.spread = 70.0
	p.initial_velocity_min = 1.8
	p.initial_velocity_max = 4.0
	p.gravity = Vector3(0, -9.0, 0)
	p.scale_amount_min = 0.6
	p.scale_amount_max = 1.2
	p.color_ramp = _ramp(
		[Color("FFE08A"), ArtKit.color("gold"), Color("E8742A"), Color(0.66, 0.2, 0.18, 0.0)]
	)
	p.position = at
	parent.add_child(p)
	p.emitting = true
	return p


static func _spark_mesh() -> Mesh:
	var q := QuadMesh.new()
	q.size = Vector2(0.045, 0.12)
	q.material = _unshaded(Color.WHITE, true)
	return q


static func dust(parent: Node3D, at: Vector3, amount := 10) -> CPUParticles3D:
	var p := CPUParticles3D.new()
	p.amount = amount
	p.lifetime = 0.9
	p.one_shot = true
	p.explosiveness = 0.8
	var s := SphereMesh.new()
	s.radius = 0.16
	s.height = 0.26
	s.radial_segments = 8
	s.rings = 4
	s.material = _unshaded(Color.WHITE)
	(s.material as StandardMaterial3D).billboard_mode = BaseMaterial3D.BILLBOARD_DISABLED
	p.mesh = s
	p.direction = Vector3(0, 0.3, 0)
	p.spread = 180.0
	p.initial_velocity_min = 0.4
	p.initial_velocity_max = 1.2
	p.gravity = Vector3(0, 0.3, 0)
	p.scale_amount_min = 0.6
	p.scale_amount_max = 1.4
	var curve := Curve.new()
	curve.add_point(Vector2(0, 0.5))
	curve.add_point(Vector2(1, 1.6))
	p.scale_amount_curve = curve
	p.color_ramp = _ramp([Color(0.85, 0.75, 0.55, 0.75), Color(0.85, 0.75, 0.55, 0.0)])
	p.position = at
	parent.add_child(p)
	p.emitting = true
	return p


## Fire, sparks and smoke over a campfire, with a flickering warm light.
static func campfire(parent: Node3D, at: Vector3) -> Node3D:
	var root := Node3D.new()
	root.position = at
	parent.add_child(root)
	var flame := CPUParticles3D.new()
	flame.amount = 26
	flame.lifetime = 0.7
	var q := QuadMesh.new()
	q.size = Vector2(0.32, 0.42)
	q.material = _unshaded(Color.WHITE, true)
	flame.mesh = q
	flame.emission_shape = CPUParticles3D.EMISSION_SHAPE_SPHERE
	flame.emission_sphere_radius = 0.18
	flame.direction = Vector3.UP
	flame.spread = 12.0
	flame.gravity = Vector3(0, 1.2, 0)
	flame.initial_velocity_min = 0.4
	flame.initial_velocity_max = 0.9
	var shrink := Curve.new()
	shrink.add_point(Vector2(0, 1.0))
	shrink.add_point(Vector2(1, 0.15))
	flame.scale_amount_curve = shrink
	flame.color_ramp = _ramp([Color("F2B33D"), Color("E8742A"), Color(0.66, 0.2, 0.18, 0.0)])
	flame.position = Vector3(0, 0.25, 0)
	root.add_child(flame)
	var smoke := CPUParticles3D.new()
	smoke.amount = 14
	smoke.lifetime = 2.6
	var s := SphereMesh.new()
	s.radius = 0.22
	s.height = 0.36
	s.radial_segments = 8
	s.rings = 4
	s.material = _unshaded(Color.WHITE)
	(s.material as StandardMaterial3D).billboard_mode = BaseMaterial3D.BILLBOARD_DISABLED
	smoke.mesh = s
	smoke.direction = Vector3.UP
	smoke.spread = 10.0
	smoke.initial_velocity_min = 0.5
	smoke.initial_velocity_max = 0.8
	smoke.gravity = Vector3(0.25, 0.15, 0)
	var grow := Curve.new()
	grow.add_point(Vector2(0, 0.6))
	grow.add_point(Vector2(1, 2.2))
	smoke.scale_amount_curve = grow
	smoke.color_ramp = _ramp(
		[Color(0.42, 0.4, 0.4, 0.0), Color(0.5, 0.48, 0.46, 0.45), Color(0.6, 0.58, 0.56, 0.0)]
	)
	smoke.position = Vector3(0, 1.6, 0)
	root.add_child(smoke)
	var light := OmniLight3D.new()
	light.light_color = Color("F2B33D")
	light.light_energy = 0.9
	light.omni_range = 4.5
	light.position = Vector3(0, 0.8, 0)
	root.add_child(light)
	return root
