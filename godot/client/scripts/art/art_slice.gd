class_name ArtSlice
extends Node3D
## Vertical slice of the new art: the Korsun camp and one battle room, with the people,
## the environment kit, the effects and the HUD in the new style. It is a showcase only:
## the game's maps and battles still use their own scenes.
##   godot --path godot/client res://scenes/art_slice.tscn            (the camp)
##   godot --path godot/client res://scenes/art_slice.tscn -- battle 50
##   godot --path godot/client res://scenes/art_slice.tscn -- effects 35       (or effects_room)

## The effects of the map (scripts/world/map_effects.gd) in a grid, each on a kozak:
## [kind, frame, the kozak's clip, where he faces].
const EFFECT_GRID := [
	["slash", 6, "run", Vector3.RIGHT],
	["trail", 0, "attack_slash", Vector3.BACK],
	["blood", 2, "hit", Vector3.BACK],
	["heal", 4, "cast_raise", Vector3.BACK],
	["buff", 2, "cast_raise", Vector3.BACK],
	["aura", 4, "idle", Vector3.BACK],
	["whirl", 0, "attack_2h_slash", Vector3.BACK],
	["fire", 4, "hit", Vector3.BACK],
	["burst", 1, "attack_spin", Vector3.BACK],
	["blast", 0, "", Vector3.ZERO],
	["wave", 24, "cast", Vector3.RIGHT],
	["scroll", 14, "use_item", Vector3.RIGHT],
]

const FOV := 35.0
const DISTANCE := 13.0

var place := "camp"
var pitch := 50.0
## Camera distance; the game's own camera keeps 13 m, a larger value shows the whole place.
var distance := DISTANCE
var camera: Camera3D
var hero: Node3D
var hud: Control
var figures: Array[Node3D] = []
var effects: Array[Node] = []


func _ready() -> void:
	if get_parent() == get_tree().root:
		var args := OS.get_cmdline_user_args()
		if args.size() > 0:
			place = args[0]
		if args.size() > 1:
			pitch = float(args[1])
		build(place, pitch)


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


func _camera() -> void:
	camera = Camera3D.new()
	camera.fov = FOV
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


func _prop(
	prop_name: String, at: Vector3, yaw_deg := 0.0, scale_by := 1.0, outline := false
) -> Node3D:
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


# -- Korsun camp ----------------------------------------------------------------------
func _camp() -> void:
	var centre := Vector2(0.0, -0.4)
	_ground(
		[
			PackedVector2Array(
				[
					Vector2(-4.2, -4.4),
					Vector2(-2.0, -2.6),
					centre,
					Vector2(2.2, -1.6),
					Vector2(4.0, -3.6)
				]
			),
			PackedVector2Array([centre, Vector2(1.0, 2.0), Vector2(3.6, 2.6), Vector2(5.2, 1.0)]),
			PackedVector2Array([centre, Vector2(-3.5, 1.6), Vector2(-9.0, 3.0)]),
		],
		[Vector3(-8, -8, 4), Vector3(8, -7, 4), Vector3(-8, 5, 3), Vector3(6, 6, 4)],
		Rect2(-12, -11, 24, 20)
	)
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
	hero = _figure("kozak_hero", Vector3(0.4, 0, 0.6), "idle", Vector3(1.4, 0, -1.6), 0.2)


# -- battle room ----------------------------------------------------------------------
func _battle() -> void:
	_ground(
		[PackedVector2Array([Vector2(-1.0, 6.0), Vector2(0.0, 1.0), Vector2(0.4, -1.5)])],
		[Vector3(-5, 4, 3), Vector3(5, -5, 3), Vector3(5.5, 4.5, 3)],
		Rect2(-8, -8, 16, 16)
	)
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
	hero = _figure("kozak_hero", Vector3(-0.2, 0, 0.9), "attack_slash", Vector3(0.9, 0, -0.4), 0.42)
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
	var heroes := [
		["kozak_hero", ""], ["serdiuk", "palash"], ["kharakternyk", "sabre"], ["haidamaka", "sabre"]
	]
	for i in heroes.size():
		var x := (i - (heroes.size() - 1) / 2.0) * 1.7
		var f := _figure(
			heroes[i][0], Vector3(x, 0, 2.2), "idle", Vector3(x + 0.3, 0, 6.0), 0.3 + i * 0.13
		)
		if heroes[i][1] != "":
			f.equip(heroes[i][1])
	var enemies := [
		"zholner",
		"luchnyk",
		"rotmistr",
		"kozak_rival",
		"kozak_rival_luk",
		"polkovnyk",
		"tatar",
		"tatar_luk",
		"murza"
	]
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
	var shown: Array = [
		["storm", 3, p], ["storm", 6, p], ["storm", 7, p], ["storm", 8, p], ["quake", 6, p]
	]
	for k in 5:
		shown.append(["rain", 5 + k, p])
	fx.show_effects(shown, 0.55)
	hero = null


## A place on the ground in the map's pixels (MapPeople.to_world turned back).
static func _px(at: Vector3) -> Vector2i:
	return Vector2i(roundi(at.x * 27.0), roundi(at.z * 27.0) - MapPeople.FOOT_PX)
