extends Node3D
## Vertical slice of the new art: the Korsun camp, the camp on the marsh at dusk and one
## battle room, with the people, the environment kit, the effects and the HUD in the new style.
## It is a showcase only: the game's maps and battles still use their own scenes.
##   godot --path godot/client res://scenes/art_slice.tscn            (the camp)
##   godot --path godot/client res://scenes/art_slice.tscn -- fort 32  (the camp on the marsh)
##   godot --path godot/client res://scenes/art_slice.tscn -- battle 50
##   godot --path godot/client res://scenes/art_slice.tscn -- effects 35       (or effects_room)

const ArtKit := preload("res://scripts/art/art_kit.gd")
const ArtFigure := preload("res://scripts/art/art_figure.gd")
const ArtEffects := preload("res://scripts/art/art_effects.gd")
const ArtGround := preload("res://scripts/art/art_ground.gd")
const ArtHud := preload("res://scripts/art/art_hud.gd")
const MapEffects := preload("res://scripts/world/map_effects.gd")
const DUSK_SKY := preload("res://assets/art/shaders/dusk_sky.gdshader")
const WATER := preload("res://assets/art/shaders/water.gdshader")
const MIST := preload("res://assets/art/shaders/mist.gdshader")

## The effects of the map (scripts/world/map_effects.gd) in a grid, each on a kozak:
## [kind, frame, the kozak's clip, where he faces].
const EFFECT_GRID := [
	["slash", 6, "run", Vector3.RIGHT], ["trail", 0, "attack_slash", Vector3.BACK],
	["blood", 2, "hit", Vector3.BACK], ["heal", 4, "cast_raise", Vector3.BACK],
	["buff", 2, "cast_raise", Vector3.BACK], ["aura", 4, "idle", Vector3.BACK],
	["whirl", 0, "attack_2h_slash", Vector3.BACK], ["fire", 4, "hit", Vector3.BACK],
	["burst", 1, "attack_spin", Vector3.BACK], ["blast", 0, "", Vector3.ZERO],
	["wave", 24, "cast", Vector3.RIGHT], ["scroll", 14, "use_item", Vector3.RIGHT],
]

const FOV := 35.0
const DISTANCE := 13.0

## The camp on the marsh: the radius of its palisade ring, and its ways out: name ->
## [angle round the ring in degrees (0 = the front, +Z; growing towards +X), the gate, how many
## pieces of palisade it takes]. A1 is the main gate at the front, B2 and C3 the side gates
## at the back.
const FORT_RADIUS := 10.0
const FORT_EXITS := {"A1": [0.0, "brama", 2], "B2": [218.0, "vorota", 1], "C3": [142.0, "vorota", 1]}
## The water channels round the ring: how far out they run, and the dry causeway left on
## each side of a way out (degrees).
const FORT_MOAT := 13.6
const FORT_CAUSEWAY := 16.0
## Dusk over the marsh, grim and dark: a low violet-grey sky under heavy cloud
## (dusk_sky.gdshader), a weak cold moon behind it, a deep blue-black shade, mist over the
## water; the fires and torches give the only warm light, and the camp lies in pools of it.
const DUSK := {"top": Color("0b0d13"), "horizon": Color("36343f"), "glow": Color("55425b"),
	"glow_size": 0.3, "glow_dir": Vector3(0.55, 0.1, -0.8), "clouds": 0.7, "cloud_dark": Color("13151c"),
	"cloud_lit": Color("474c60"), "seed": 11.0}
const MOON_COLOR := Color("a3b0d2")
const MOON_ENERGY := 0.42
const DUSK_AMBIENT := Color("282d3c")
const DUSK_AMBIENT_ENERGY := 0.55
## The grade at dusk: brightness, contrast, saturation.
const DUSK_GRADE := Vector3(0.96, 1.18, 0.72)
## The warm light of a campfire and of a torch at dusk: colour, energy, reach (metres).
const FIRE_LIGHT := [Color("ff9443"), 2.1, 8.5]
const TORCH_LIGHT := [Color("ffa24c"), 1.5, 6.0]
## The mist over the marsh: sheets [height, density], its colour.
const MIST_SHEETS := [[0.25, 0.5], [0.6, 0.38], [1.0, 0.26], [1.6, 0.14]]
const MIST_COLOR := Vector3(0.37, 0.39, 0.47)
## The town hall's tent in the middle, gone grey with smoke and rain (the painted shader's tint).
const SMOKED := Color(0.62, 0.6, 0.56)

var place := "camp"
var pitch := 50.0
## Camera distance; the game's own camera keeps 13 m, a larger value shows the whole place.
var distance := DISTANCE
## The camera's field of view; a wider one over the whole place shows the sky above it.
var fov := FOV
var camera: Camera3D
var hero: Node3D
var hud: Control
var figures: Array[Node3D] = []
var effects: Array[Node] = []
## The ways out of the camp on the marsh: name -> the middle of its gate on the ground.
var exits := {}
var ground: Node3D  # the ArtGround of the place
## The flickering lights of the fires and torches: [light, its energy, a phase].
var _flames: Array = []
var _time := 0.0


func _ready() -> void:
	if get_parent() == get_tree().root:
		var args := OS.get_cmdline_user_args()
		if args.size() > 0:
			place = args[0]
		if args.size() > 1:
			pitch = float(args[1])
		build(place, pitch)


## The fires and torches flicker.
func _process(delta: float) -> void:
	if _flames.is_empty():
		return
	_time += delta
	for f in _flames:
		var t: float = _time * 9.0 + f[2]
		(f[0] as OmniLight3D).light_energy = f[1] * (0.86 + 0.08 * sin(t) + 0.06 * sin(t * 2.3 + 1.7))


func build(where: String, pitch_deg: float) -> void:
	place = where
	pitch = pitch_deg
	_world()
	if place == "battle":
		_battle()
	elif place == "lineup":
		_lineup()
	elif place == "people":
		_people()
	elif place == "effects":
		_effects()
	elif place == "effects_room":
		_effects_room()
	elif place == "fort":
		_fort()
	else:
		_camp()
	_camera()
	if not place in ["lineup", "people", "effects", "effects_room"]:
		hud = ArtHud.new()
		var layer := CanvasLayer.new()
		add_child(layer)
		layer.add_child(hud)
		hud.setup(hero, place)


func _world() -> void:
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = ArtKit.AIR
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	env.fog_enabled = true
	env.fog_mode = Environment.FOG_MODE_DEPTH
	env.fog_light_color = ArtKit.AIR
	env.fog_density = 1.0
	env.fog_depth_begin = distance + 8.0
	env.fog_depth_end = distance + 40.0
	env.fog_sky_affect = 0.0
	var we := WorldEnvironment.new()
	we.environment = env
	add_child(we)
	var sun := DirectionalLight3D.new()
	ArtKit.light(sun, env)
	sun.shadow_enabled = true
	sun.directional_shadow_mode = DirectionalLight3D.SHADOW_ORTHOGONAL
	sun.directional_shadow_max_distance = 40.0
	sun.shadow_blur = 1.5
	# from the upper left and a little from the viewer, so faces are in the light
	var dir := Vector3(0.5, -0.74, -0.45).normalized()
	sun.transform = Transform3D(Basis.looking_at(dir, Vector3.UP), Vector3.ZERO)
	add_child(sun)
	if place == "fort":
		_dusk(env, sun)


## Dusk instead of the day: the painted sky, the moon from behind the viewer, the deep shade,
## mist the colour of the horizon.
func _dusk(env: Environment, moon: DirectionalLight3D) -> void:
	var sm := ShaderMaterial.new()
	sm.shader = DUSK_SKY
	for key in DUSK:
		sm.set_shader_parameter(key, DUSK[key])
	var sky := Sky.new()
	sky.sky_material = sm
	env.background_mode = Environment.BG_SKY
	env.sky = sky
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = DUSK_AMBIENT
	env.ambient_light_energy = DUSK_AMBIENT_ENERGY
	env.fog_light_color = DUSK.horizon
	env.fog_depth_begin = distance + 4.0
	env.fog_depth_end = distance + 40.0
	env.fog_depth_curve = 0.7
	env.adjustment_brightness = DUSK_GRADE.x
	env.adjustment_contrast = DUSK_GRADE.y
	env.adjustment_saturation = DUSK_GRADE.z
	# the flames' brightest light rolls off into warm colour instead of white, and glows
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env.tonemap_exposure = 1.25
	env.tonemap_white = 3.0
	env.glow_enabled = true
	env.glow_intensity = 0.7
	env.glow_bloom = 0.0
	env.glow_hdr_threshold = 0.85
	env.glow_blend_mode = Environment.GLOW_BLEND_MODE_SCREEN
	moon.light_color = MOON_COLOR
	moon.light_energy = MOON_ENERGY
	moon.directional_shadow_max_distance = 60.0
	moon.transform = Transform3D(Basis.looking_at(Vector3(0.45, -0.55, -0.7).normalized(), Vector3.UP), Vector3.ZERO)


func _camera() -> void:
	camera = Camera3D.new()
	camera.fov = fov
	add_child(camera)
	var target := hero.global_position if hero != null else Vector3.ZERO
	if place == "lineup":
		camera.fov = 30.0
		camera.position = Vector3(0, 2.6, 11.5)
		camera.rotation_degrees = Vector3(-9.0, 0, 0)
		return
	if place == "people":
		camera.fov = 30.0
		camera.position = Vector3(0, 4.2, 15.5)
		camera.rotation_degrees = Vector3(-13.0, 0, 0)
		return
	var p := deg_to_rad(pitch)
	camera.position = target + Vector3(0.0, sin(p), cos(p)) * distance
	camera.rotation_degrees = Vector3(-pitch, 0.0, 0.0)


## Starts the one-shot effects again (sparks, dust), so a still picture catches them in flight.
func burst() -> void:
	for e in effects:
		if e is CPUParticles3D and (e as CPUParticles3D).one_shot:
			(e as CPUParticles3D).restart()


func _prop(prop_name: String, at: Vector3, yaw_deg := 0.0, scale_by := 1.0, outline := false) -> Node3D:
	var node := ArtKit.prop(prop_name, outline)
	node.position = at
	node.rotation_degrees.y = yaw_deg
	node.scale = Vector3.ONE * scale_by
	add_child(node)
	return node


func _figure(kind: String, at: Vector3, clip: String, face_to: Vector3, at_time := -1.0) -> Node3D:
	var f: Node3D = ArtFigure.new()
	add_child(f)
	f.setup(kind)
	f.position = at
	f.face(face_to - at)
	if at_time >= 0.0:
		f.pose(clip, at_time)
	else:
		f.play(clip, 0.0)
		f.player.seek(randf() * 0.8, true)
	figures.append(f)
	return f


func _ground(paths: Array, greens: Array, play: Rect2) -> void:
	var g: Node3D = ArtGround.new()
	g.paths = paths
	g.greens = greens
	g.play = play
	add_child(g)
	g.build()
	ground = g


# -- Korsun camp ----------------------------------------------------------------------
func _camp() -> void:
	var centre := Vector2(0.0, -0.4)
	_ground([
		PackedVector2Array([Vector2(-4.2, -4.4), Vector2(-2.0, -2.6), centre, Vector2(2.2, -1.6), Vector2(4.0, -3.6)]),
		PackedVector2Array([centre, Vector2(1.0, 2.0), Vector2(3.6, 2.6), Vector2(5.2, 1.0)]),
		PackedVector2Array([centre, Vector2(-3.5, 1.6), Vector2(-9.0, 3.0)]),
	], [Vector3(-8, -8, 4), Vector3(8, -7, 4), Vector3(-8, 5, 3), Vector3(6, 6, 4)], Rect2(-12, -11, 24, 20))
	# hut, fence and poplars at the back left
	_prop("khata", Vector3(-5.0, 0, -6.2), 8.0)
	_prop("tyn", Vector3(-7.2, 0, -3.5))
	_prop("tyn", Vector3(-9.25, 0, -3.5))
	_prop("tyn", Vector3(-1.9, 0, -3.9), -12.0)
	_prop("topolia", Vector3(-8.6, 0, -8.4))
	_prop("topolia", Vector3(-1.6, 0, -8.8))
	_prop("topolia", Vector3(8.8, 0, -7.8), 0.0, 0.9)
	_prop("zhuravel", Vector3(0.2, 0, -7.0), 200.0)
	_prop("stih", Vector3(-8.2, 0, -0.2))
	_prop("stih", Vector3(-7.4, 0, 2.0), 40.0, 0.75)
	# the colonel's tent and banner, the cannon
	_prop("shatro", Vector3(4.4, 0, -6.0), 10.0)
	_prop("banner", Vector3(6.8, 0, -3.6), -20.0)
	_prop("dub", Vector3(9.4, 0, -4.0))
	_prop("harmata", Vector3(-0.2, 0, -4.4), 170.0)
	# fire in the middle
	var fire := Vector3(-2.7, 0, -0.9)
	_prop("vohnyshche", fire)
	effects.append(ArtEffects.campfire(self, fire))
	# forge on the right, cart and barrels on the left
	_prop("kuznya", Vector3(8.0, 0, -0.6), -90.0)
	_prop("penok", Vector3(3.6, 0, 3.2))
	_prop("viz", Vector3(-6.6, 0, 1.6), 35.0)
	_prop("bochka", Vector3(-3.8, 0, 3.0))
	_prop("bochka", Vector3(-3.3, 0, 3.7), 30.0, 0.85)
	_prop("skrynia", Vector3(-4.6, 0, 3.9), 20.0)
	_prop("kushch", Vector3(-6.4, 0, -2.0))
	_prop("kushch", Vector3(2.6, 0, 4.6), 40.0)
	_prop("kushch", Vector3(-1.4, 0, 4.9), 90.0, 0.8)
	_prop("kamin", Vector3(7.6, 0, 3.6))
	_prop("namet", Vector3(9.4, 0, 3.2), 75.0)
	# people
	_figure("kozak_svyta", fire + Vector3(0.1, 0, -1.25), "sit", fire + Vector3(0.6, 0, 2.0), 1.0)
	_figure("kozak_camp", fire + Vector3(-1.25, 0, 0.1), "interact", fire, 0.45)
	_figure("kozak_camp", fire + Vector3(1.05, 0, 0.85), "cheer", fire, 0.55)
	_figure("polkovnyk", Vector3(2.8, 0, -2.7), "idle", Vector3(0.4, 0, 0.6), 0.4)
	_figure("kozak_svyta", Vector3(6.3, 0, -0.4), "attack_chop", Vector3(7.4, 0, -0.4), 0.55)
	_figure("luchnyk", Vector3(-3.6, 0, -3.1), "walk", Vector3(-4.4, 0, -4.4), 0.3)
	hero = _figure("kozak", Vector3(0.4, 0, 0.6), "idle", Vector3(1.4, 0, -1.6), 0.2)


# -- the camp on the marsh ------------------------------------------------------------
## A camp after Andrey's sketch: a ring of palisade on dry ground among water channels and
## reeds, with three ways out (FORT_EXITS: the main gate A1 at the front, the side gates B2 and
## C3 at the back, a road from each to the middle); the town hall's big tent in the middle,
## smoke-dark tents, two fires, torches, an anvil with the stores; at dusk (_dusk()).
func _fort() -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 41
	# roads from the ways out to the yard before the big tent, and round the yard
	var roads: Array = []
	for way in FORT_EXITS:
		var o := _on_ring(FORT_EXITS[way][0], FORT_RADIUS + 9.0)
		roads.append(PackedVector2Array([Vector2(o.x, o.z), Vector2(o.x * 0.45, o.z * 0.45), Vector2(0.0, 1.0)]))
	var yard := PackedVector2Array()
	for i in 13:
		var a := TAU * i / 12.0
		yard.append(Vector2(sin(a) * 4.4, -2.0 + cos(a) * 4.0))
	roads.append(yard)
	# the water channels: round the ring with a causeway at each way out, and two creeks away
	var channels: Array = []
	var bare := []
	for way in FORT_EXITS:
		bare.append(float(FORT_EXITS[way][0]))
	bare.sort()
	for i in bare.size():
		var from: float = bare[i] + FORT_CAUSEWAY
		var to: float = (bare[(i + 1) % bare.size()] + (360.0 if i == bare.size() - 1 else 0.0)) - FORT_CAUSEWAY
		var arc := PackedVector2Array()
		var steps := int(ceil((to - from) / 8.0))
		for k in steps + 1:
			var p := _on_ring(lerpf(from, to, float(k) / steps), FORT_MOAT)
			arc.append(Vector2(p.x, p.z))
		channels.append(arc)
	channels.append(PackedVector2Array([Vector2(FORT_MOAT, 0.0), Vector2(18.0, 2.5), Vector2(22.0, 1.0), Vector2(27.0, 4.0)]))
	channels.append(PackedVector2Array([Vector2(-FORT_MOAT, 0.0), Vector2(-17.5, -3.0), Vector2(-22.0, -2.0),
		Vector2(-27.0, -5.0)]))
	var g: Node3D = ArtGround.new()
	g.paths = roads
	g.path_width = 1.1
	g.hollows = channels
	g.greens = [Vector3(-16, -8, 6), Vector3(16, -9, 6), Vector3(-17, 9, 6), Vector3(17, 10, 6), Vector3(0, -19, 7),
		Vector3(-7, -2, 3), Vector3(7, 4, 3)]
	g.play = Rect2(-26, -26, 52, 44)
	g.size = 100.0
	g.tufts = 600
	g.seed_value = 41
	add_child(g)
	g.build()
	ground = g
	var m := (g.get_node("Ground") as MeshInstance3D).material_override as ShaderMaterial
	m.set_shader_parameter("soil", Color("6c5a3e"))
	m.set_shader_parameter("grass_dry", Color("5c6440"))
	m.set_shader_parameter("grass_green", Color("3f5530"))
	_water(Vector2(80.0, 80.0), -0.32)
	for i in MIST_SHEETS.size():
		_mist(MIST_SHEETS[i][0], MIST_SHEETS[i][1], float(i) * 5.3)
	# the palisade ring in two-metre pieces, a gate in each way out
	var step := rad_to_deg(2.0 * asin(1.0 / FORT_RADIUS))
	var pieces := int(floor(360.0 / step))
	step = 360.0 / pieces
	for i in pieces:
		var a := (i + 0.5) * step
		var gap := false
		for way in FORT_EXITS:
			var off := absf(fposmod(a - float(FORT_EXITS[way][0]) + 180.0, 360.0) - 180.0)
			gap = gap or off < step * float(FORT_EXITS[way][2]) / 2.0 + 0.1
		if not gap:
			_prop("palisade", _on_ring(a, FORT_RADIUS * cos(deg_to_rad(step / 2.0))), a)
	for way in FORT_EXITS:
		var at := _on_ring(FORT_EXITS[way][0], FORT_RADIUS * cos(deg_to_rad(step / 2.0)))
		_prop(FORT_EXITS[way][1], at, FORT_EXITS[way][0])
		exits[way] = at
	# the town hall's big tent in the middle, tents round it
	var hall := _prop("shatro", Vector3(0.0, 0, -3.2), 0.0, 1.35)
	var smoked := ArtKit.painted(false)
	smoked.set_shader_parameter("tint", SMOKED)
	ArtKit.dress(hall, smoked)
	_prop("namet_dark", Vector3(-6.3, 0, -1.4), 75.0, 1.5)
	_prop("namet_dark", Vector3(-5.6, 0, 3.0), 105.0, 1.4)
	_prop("namet_dark", Vector3(6.4, 0, 2.4), -70.0, 1.5)
	_prop("namet_dark", Vector3(6.0, 0, -3.8), -110.0, 1.35)
	_prop("namet_dark", Vector3(0.4, 0, -8.0), 5.0, 1.35)
	_prop("banner", Vector3(-3.0, 0, -1.2), 15.0)
	# two fires with men round them
	var fires := [Vector3(-3.4, 0, 1.2), Vector3(4.0, 0, -0.9)]
	for f in fires:
		_prop("vohnyshche", f)
		var fire_node := ArtEffects.campfire(self, f)
		effects.append(fire_node)
		_warm(fire_node, FIRE_LIGHT, true)
	_figure("kozak_svyta", fires[0] + Vector3(0.1, 0, -1.25), "sit", fires[0] + Vector3(0.6, 0, 2.0), 1.0)
	_figure("kozak_camp", fires[0] + Vector3(-1.2, 0, 0.2), "interact", fires[0], 0.45)
	_figure("kozak_camp", fires[1] + Vector3(-0.9, 0, 0.9), "cheer", fires[1], 0.55)
	_figure("kozak_svyta", fires[1] + Vector3(1.1, 0, -0.5), "sit", fires[1], 1.0)
	# the anvil and the stores, before the big tent
	_prop("kovadlo", Vector3(1.9, 0, 3.4), 20.0, 1.0, true)
	_prop("skrynia", Vector3(3.3, 0, 3.9), -12.0, 1.0, true)
	_prop("bochka", Vector3(4.3, 0, 3.1))
	_prop("bochka", Vector3(4.7, 0, 3.8), 30.0, 0.85)
	_prop("drova", Vector3(-1.6, 0, 4.6), 70.0)
	_prop("stoiak", Vector3(-2.2, 0, -6.6), 30.0)
	_prop("harmata", Vector3(-6.0, 0, -5.9), 210.0)
	# torches: by the main gate outside, inside the side gates, at the big tent's door
	var torches := [_on_ring(-14.0, FORT_RADIUS + 0.9), _on_ring(14.0, FORT_RADIUS + 0.9),
		_on_ring(FORT_EXITS.B2[0] + 9.0, FORT_RADIUS - 1.0), _on_ring(FORT_EXITS.C3[0] - 9.0, FORT_RADIUS - 1.0),
		Vector3(-1.5, 0, 0.2), Vector3(1.5, 0, 0.2)]
	for t in torches:
		_prop("smoloskyp", t, rng.randf() * 360.0)
		var torch := ArtEffects.torch(self, t)
		effects.append(torch)
		_warm(torch, TORCH_LIGHT, false)
	# guards: two outside the main gate, one inside each side gate
	for a in [-9.0, 9.0]:
		var at := _on_ring(a, FORT_RADIUS + 1.7)
		_figure("kozak_svyta", at, "idle", at * 2.0, 0.2 + absf(a) * 0.02).equip("spear")
	for way in ["B2", "C3"]:
		var a: float = FORT_EXITS[way][0] + (6.0 if way == "B2" else -6.0)
		var at := _on_ring(a, FORT_RADIUS - 1.5)
		_figure("kozak_svyta", at, "idle", at * 2.0, 0.4).equip("spear")
	_figure("polkovnyk", Vector3(0.9, 0, 0.9), "idle", Vector3(0.6, 0, 4.0), 0.4)
	hero = _figure("kozak", Vector3(0.1, 0, 2.6), "idle", Vector3(-0.3, 0, 6.0), 0.2)
	# reeds on both banks of the water, bushes and trees beyond
	for line in channels:
		var pl: PackedVector2Array = line
		for k in pl.size() - 1:
			var a2 := pl[k]
			var b2 := pl[k + 1]
			var across := (b2 - a2).normalized().orthogonal()
			var n := int(ceil(a2.distance_to(b2) / 1.1))
			for j in n:
				for side in [-1.0, 1.0]:
					if rng.randf() < 0.4:
						continue
					var p: Vector2 = a2.lerp(b2, (j + rng.randf()) / n) + across * side * rng.randf_range(1.2, 2.1)
					var at := Vector3(p.x, g.height(p.x, p.y) - 0.05, p.y)
					_prop("ochert", at, rng.randf() * 360.0, rng.randf_range(0.75, 1.25))
	for p in [Vector3(-18, 0, -8), Vector3(18.5, 0, -7), Vector3(-17, 0, 7), Vector3(18, 0, 9), Vector3(-7, 0, -18),
			Vector3(8, 0, -18.5), Vector3(-10, 0, 16), Vector3(11, 0, 16.5)]:
		_prop("kushch", Vector3(p.x, g.height(p.x, p.z), p.z), p.x * 17.0, rng.randf_range(1.0, 1.4))
	for t in [["topolia", -21.0, -17.0, 1.1], ["topolia", -16.0, -22.0, 1.2], ["dub", 22.0, -15.0, 1.15],
			["topolia", 19.0, -22.0, 1.15], ["yalyna", -25.0, -6.0, 1.3], ["yalyna", 26.0, -3.0, 1.25],
			["dub", -4.0, -25.0, 1.2], ["topolia", 6.0, -26.0, 1.1]]:
		_prop(t[0], Vector3(t[1], g.height(t[1], t[2]), t[2]), rng.randf() * 360.0, t[3])


## The still water of a marsh, a plane at `level` over the hollows of the ground: dark, with
## slow lighter ripples (water.gdshader).
func _water(size: Vector2, level: float) -> void:
	var plane := PlaneMesh.new()
	plane.size = size
	var mi := MeshInstance3D.new()
	mi.name = "Water"
	mi.mesh = plane
	mi.position.y = level
	var m := ShaderMaterial.new()
	m.shader = WATER
	m.set_shader_parameter("deep", Vector3(0.045, 0.055, 0.065))
	m.set_shader_parameter("shallow", Vector3(0.1, 0.115, 0.135))
	m.set_shader_parameter("glint", Vector3(0.42, 0.45, 0.52))
	mi.material_override = m
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mi)


## The light of a fire or a torch made warmer and stronger for the dusk (FIRE_LIGHT,
## TORCH_LIGHT), casting shadows if `shadows`; it flickers (_process()).
func _warm(flame: Node3D, how: Array, shadows: bool) -> void:
	for light in flame.find_children("*", "OmniLight3D", false, false):
		var l := light as OmniLight3D
		l.light_color = how[0]
		l.light_energy = how[1]
		l.omni_range = how[2]
		l.omni_attenuation = 1.6
		l.shadow_enabled = shadows
		_flames.append([l, float(how[1]), randf() * TAU])


## A sheet of the mist over the marsh at `height` (mist.gdshader), clear over the camp.
func _mist(height: float, density: float, seed_value: float) -> void:
	var plane := PlaneMesh.new()
	plane.size = Vector2(90.0, 90.0)
	var mi := MeshInstance3D.new()
	mi.name = "Mist"
	mi.mesh = plane
	mi.position.y = height
	var m := ShaderMaterial.new()
	m.shader = MIST
	m.set_shader_parameter("color", MIST_COLOR)
	m.set_shader_parameter("density", density)
	m.set_shader_parameter("clear_radius", FORT_RADIUS + 1.5)
	m.set_shader_parameter("seed", seed_value)
	mi.material_override = m
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mi)


## A point round the middle of the camp: `deg` degrees from the front (+Z) towards +X.
static func _on_ring(deg: float, radius: float) -> Vector3:
	var a := deg_to_rad(deg)
	return Vector3(sin(a) * radius, 0.0, cos(a) * radius)


# -- battle room ----------------------------------------------------------------------
func _battle() -> void:
	_ground([PackedVector2Array([Vector2(-1.0, 6.0), Vector2(0.0, 1.0), Vector2(0.4, -1.5)])],
		[Vector3(-5, 4, 3), Vector3(5, -5, 3), Vector3(5.5, 4.5, 3)], Rect2(-8, -8, 16, 16))
	for i in 4:
		_prop("palisade", Vector3(-3.0 + i * 2.0, 0, -4.4), 0.0)
	for i in 3:
		_prop("palisade", Vector3(-4.6, 0, -2.8 + i * 2.0), 90.0)
	_prop("banner_crown", Vector3(-3.6, 0, -3.6))
	_prop("namet", Vector3(4.6, 0, -6.0), 10.0)
	_prop("dub", Vector3(6.6, 0, -3.0))
	_prop("kushch", Vector3(4.6, 0, 1.6), 20.0)
	_prop("kushch", Vector3(4.2, 0, 3.4), 80.0, 0.8)
	_prop("kamin", Vector3(4.8, 0, -0.8), 0.0, 1.2)
	_prop("kamin", Vector3(-5.2, 0, 3.4), 40.0)
	_prop("bochka", Vector3(2.6, 0, -3.4), 0.0, 1.0, true)
	_prop("bochka", Vector3(3.3, 0, -3.0), 40.0, 0.85, true)
	_prop("skrynia", Vector3(-2.7, 0, -3.3), 10.0, 1.0, true)
	_prop("penok", Vector3(-3.4, 0, 2.6))
	_prop("trava", Vector3(1.6, 0, 2.4))
	_prop("trava", Vector3(-1.8, 0, 1.8), 50.0)
	# the fight: the hero cuts at a Crown soldier who takes it on his shield
	hero = _figure("kozak", Vector3(-0.2, 0, 0.9), "attack_slash", Vector3(0.9, 0, -0.4), 0.42)
	var guard := _figure("zholner", Vector3(0.9, 0, -0.45), "block_hit", hero.position, 0.18)
	_figure("zholner", Vector3(-2.1, 0, -1.4), "attack_chop", hero.position, 0.5)
	_figure("luchnyk", Vector3(2.4, 0, -2.0), "aim_bow", hero.position, 0.6)
	var to_guard := (guard.position - hero.position).normalized()
	var start := rad_to_deg(atan2(to_guard.x, to_guard.z)) - 110.0
	effects.append(ArtEffects.slash(self, hero.position, start, 150.0, 1.25, 1.0, 0.6, 0.55))
	effects.append(ArtEffects.sparks(self, hero.position + to_guard * 0.95 + Vector3(0, 1.15, 0)))
	effects.append(ArtEffects.dust(self, hero.position + Vector3(0, 0.05, 0.1), 8))
	guard.flash(0.08)


# -- everyone in a row, for the style sheet -------------------------------------------
func _lineup() -> void:
	_ground([], [Vector3(0, -3, 6)], Rect2(-10, -6, 20, 12))
	var kinds := ["kozak", "kozak_camp", "kozak_svyta", "zholner", "luchnyk", "polkovnyk"]
	for i in kinds.size():
		var x := (i - (kinds.size() - 1) / 2.0) * 1.6
		var clip := "idle"
		_figure(kinds[i], Vector3(x, 0, 0), clip, Vector3(x + 0.25, 0, 3.0), 0.3 + i * 0.13)
	_prop("topolia", Vector3(-6.5, 0, -5.0))
	_prop("shatro", Vector3(4.5, 0, -7.0), -20.0)
	_prop("khata", Vector3(-3.0, 0, -9.0), 10.0)
	hero = null


# -- the people of the map: the hero's four classes in front, the enemies behind --------
func _people() -> void:
	_ground([], [Vector3(0, -3, 6)], Rect2(-12, -8, 24, 16))
	var heroes := [["kozak", ""], ["serdiuk", "palash"], ["kharakternyk", "sabre"], ["haidamaka", "sabre"]]
	for i in heroes.size():
		var x := (i - (heroes.size() - 1) / 2.0) * 1.7
		var f := _figure(heroes[i][0], Vector3(x, 0, 2.2), "idle", Vector3(x + 0.3, 0, 6.0), 0.3 + i * 0.13)
		if heroes[i][1] != "":
			f.equip(heroes[i][1])
	var enemies := ["zholner", "luchnyk", "rotmistr", "kozak_rival", "kozak_rival_luk", "polkovnyk",
		"tatar", "tatar_luk", "murza"]
	for i in enemies.size():
		var x := (i - (enemies.size() - 1) / 2.0) * 1.45
		_figure(enemies[i], Vector3(x, 0, -0.6), "idle", Vector3(x - 0.2, 0, 4.0), 0.2 + i * 0.11)
	hero = null


# -- the effects of the map: one of each on a kozak, then the skills over a room ----------
func _effects() -> void:
	_ground([], [Vector3(0, -3, 6)], Rect2(-12, -8, 24, 16))
	var fx: Node3D = MapEffects.new()
	add_child(fx)
	var shown: Array = []
	for i in EFFECT_GRID.size():
		var e: Array = EFFECT_GRID[i]
		var at := Vector3((i % 4 - 1.5) * 3.3, 0.0, (i / 4 - 1.0) * 3.0)
		var p := _px(at)
		if e[2] != "":
			_figure("kozak", at, e[2], at + e[3], 0.35)
		shown.append([e[0], e[1], p])
		if e[0] == "aura":
			shown.append(["aura", 1, p + Vector2i(0, 3), true])
	fx.show_effects(shown, 0.5)
	hero = null


func _effects_room() -> void:
	_ground([], [Vector3(0, -3, 6)], Rect2(-12, -8, 24, 16))
	_figure("kozak", Vector3.ZERO, "cast_raise", Vector3(0, 0, 3), 0.5)
	for i in 6:
		var a := i * TAU / 6.0 + 0.4
		var at := Vector3(cos(a) * 3.2, 0.0, sin(a) * 2.4)
		_figure("tatar" if i % 2 == 0 else "tatar_luk", at, "hit", Vector3.ZERO, 0.2 + 0.1 * i)
	var fx: Node3D = MapEffects.new()
	add_child(fx)
	var p := _px(Vector3.ZERO)
	var shown: Array = [["storm", 3, p], ["storm", 6, p], ["storm", 7, p], ["storm", 8, p],
		["quake", 6, p]]
	for k in 5:
		shown.append(["rain", 5 + k, p])
	fx.show_effects(shown, 0.55)
	hero = null


## A place on the ground in the map's pixels (MapPeople.to_world turned back).
static func _px(at: Vector3) -> Vector2i:
	return Vector2i(roundi(at.x * 27.0), roundi(at.z * 27.0) - MapEffects.MapPeople.FOOT_PX)
