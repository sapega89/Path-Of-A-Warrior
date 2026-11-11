extends "res://tests/test_case.gd"
## The maps of the campaign in the new art (scripts/world/map_art.gd): every tile is known,
## the ground rises where it is blocked and stays flat where people walk, the faces of cliffs
## climb, bridges and decks hold, what stands on a cell is a 3D piece, the breakable ones flash.


func _map(n: int) -> Node3D:
	var b: Node3D = MapArt.new()
	root.add_child(b)
	b.build(MapBuilder.load_map(n))
	return b


func _kind(b: Node3D, x: int, y: int) -> String:
	return b.kinds[int(b._part(x * MapArt.PARTS + 1, y * MapArt.PARTS + 1)[0])]


func test_every_tile_is_known() -> void:
	var t := MapArt.tiles()
	eq(int(t.get("parts")), MapArt.PARTS, "three parts to a tile")
	for k in t.kinds:
		check(MapArt.KIND_COLOUR.has(k), "a colour for %s" % k)
	for tile in t.props:
		var what: String = t.props[tile]
		check(
			MapArt.PROP.has(what) or MapArt.CLUSTERS.has(what) or what in MapArt.AS_GROUND,
			"tile %s: %s is drawn" % [tile, what]
		)
	var used := {}
	for n in range(1, MapBuilder.map_count() + 1):
		var m := MapBuilder.load_map(n)
		for layer in ["ground", "upper"]:
			for tile in m[layer]:
				used[int(tile)] = n
	for tile in used:
		if tile != 0:
			check(
				t.ground.has(str(tile)) or t.props.has(str(tile)),
				"tile %d (map %d)" % [tile, used[tile]]
			)


func test_people_walk_on_flat_ground() -> void:
	for n in [1, 2, 5, 9, 27, 33, 43]:
		var b := _map(n)
		var raised := 0
		for y in b.h:
			for x in b.w:
				if b.is_blocked(x, y):
					raised += 1 if b.height_of(x, y) > 0.0 else 0
				else:
					eq(b.height_of(x, y), 0.0, "map %d: (%d, %d) is free and flat" % [n, x, y])
		check(raised > 0, "map %d: some blocked cells rise" % n)
		b.free()


func test_the_ground_and_around() -> void:
	var b := _map(1)
	var ground: MeshInstance3D = b.get_node("Ground")
	var verts: PackedVector3Array = ground.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
	var m := MapArt.MARGIN
	eq(
		verts.size(),
		((b.w + 2 * m) * MapArt.PARTS + 1) * ((b.h + 2 * m) * MapArt.PARTS + 1),
		"a grid of parts"
	)
	var lo := Vector3(INF, INF, INF)
	var hi := -lo
	for v in verts:
		lo = lo.min(v)
		hi = hi.max(v)
	eq(
		[lo.x, lo.z, hi.x, hi.z],
		[-float(m), -float(m), float(b.w + m), float(b.h + m)],
		"the land goes on past the edges"
	)
	check(
		b.hills(-m, -m) > 0.5 and b.hills(b.w / 2.0, b.h / 2.0) == 0.0, "hills around, flat inside"
	)
	check(ground.material_override is ShaderMaterial, "painted by its shader")
	var blocked := 0
	for y in b.h:
		for x in b.w:
			blocked += 1 if b.is_blocked(x, y) else 0
	eq(b.get_node("Collision").get_child_count(), blocked + 5, "the same collision as before")
	b.free()


func test_a_cliff_climbs_to_its_top() -> void:
	var b := _map(5)
	eq(_kind(b, 9, 1), "stone", "the top of the cliff")
	eq(b.height_of(9, 1), MapArt.RAISE["stone"], "rises")
	eq(_kind(b, 9, 5), "rock", "its face")
	var pw: int = b.w * MapArt.PARTS
	var faces := 0
	for py in range(MapArt.PARTS * 4, MapArt.PARTS * 9):
		if b.part_face[py * pw + 9 * MapArt.PARTS] == 1:
			faces += 1
			var here: float = b.part_raise[py * pw + 9 * MapArt.PARTS]
			var above: float = b.part_raise[(py - 1) * pw + 9 * MapArt.PARTS]
			check(
				here > 0.0 and here < above,
				"the face climbs north: %.2f under %.2f" % [here, above]
			)
	check(faces >= 9, "the face of the cliff: %d parts" % faces)
	b.free()


func test_a_pit_in_the_cliff_is_filled() -> void:
	var b := _map(5)
	eq(MapArt.prop_of(b.cell("upper", 8, 1)), "pebbles", "pebbles on the cliff's top")
	check(b.is_blocked(8, 1), "blocked")
	eq(b.height_of(8, 1), b.height_of(9, 1), "the cell rises with the cliff")
	var on_top := false
	for p in b.props:
		if p.position.distance_to(Vector3(8.5, b.height_of(8, 1), 1.5)) < 0.01:
			on_top = true
	check(on_top, "the pebbles lie on its top")
	b.free()


func test_water_bridges_and_decks() -> void:
	var b := _map(43)
	check(b.has_node("Water"), "a river")
	eq(_kind(b, 11, 21), "wood", "a log bridge")
	eq(_kind(b, 11, 22), "wood", "over the water")
	eq(MapArt.prop_of(b.cell("upper", 10, 22)), "palisade", "a post at its side")
	eq(_kind(b, 10, 22), "wood", "stands on a deck, not in the water")
	eq(_kind(b, 7, 0), "water", "the river")
	b.free()


func test_what_stands_on_the_map() -> void:
	var b := _map(9)
	check(b.props.size() > 20, "props: %d" % b.props.size())
	var tents := 0
	for p in b.props:
		if p.scene_file_path.ends_with("shatro.glb"):
			tents += 1
	check(tents >= 2, "a tent over each group of its cells: %d" % tents)
	var grass := 0
	var wheat := 0
	for mmi in b.get_node("Grass").get_children():
		var n: int = (mmi as MultiMeshInstance3D).multimesh.instance_count
		if String(mmi.name).begins_with("wheat"):
			wheat += n
		else:
			grass += n
	check(grass > 300, "grass: %d" % grass)
	check(wheat > 100, "fields of wheat around: %d" % wheat)
	b.free()


## Grass and wheat sway (grass.gdshader), are lit as the ground, and only past the map's edge
## is wheat sown.
func test_grass_and_wheat() -> void:
	var b := _map(9)
	var chunk: MultiMeshInstance3D = b.get_node("Grass").get_child(0)
	eq(chunk.material_override, Grass.material(), "one material for all the grass")
	eq(chunk.cast_shadow, GeometryInstance3D.SHADOW_CASTING_SETTING_OFF, "no shadows of its own")
	check(chunk.multimesh.use_custom_data, "each clump its colour")
	# (the renderer multiplies the blades' vertex colour by the instance colour: without one the
	# grass neither sways nor shows its ears)
	for c in b.get_node("Grass").get_children():
		check((c as MultiMeshInstance3D).multimesh.use_colors, "%s: instance colours" % c.name)
	check(not b.in_field(b.w / 2.0, b.h / 2.0), "no wheat on the map")
	var sown := 0
	for x in range(-5, b.w + 5):
		if b.in_field(x + 0.5, -3.0):
			sown += 1
	check(sown > 0 and sown < b.w + 10, "fields along the top, not all of it: %d" % sown)
	var wheat := Grass.mesh("wheat")
	var grass := Grass.mesh("grass")
	check(wheat.get_aabb().size.y > grass.get_aabb().size.y * 1.5, "wheat stands taller")
	b.free()


func test_breakables_flash() -> void:
	var b := _map(1)
	eq(b.breakables.size(), 10, "breakable objects")
	var materials := {}
	for o in b.breakables:
		var at: PackedStringArray = String(o.name).split("_")
		eq(at[0], "Object", "named as before")
		var piece: Node3D = o.get_child(0)
		eq(
			Vector2(piece.position.x, piece.position.z),
			Vector2(int(at[1]) + 0.5, int(at[2]) + 0.5),
			"%s stands on its cell" % o.name
		)
		check(o.get_meta("material") is ShaderMaterial, "%s has a material" % o.name)
		materials[o.get_meta("material")] = true
	eq(materials.size(), b.breakables.size(), "each its own")
	var m: ShaderMaterial = b.breakables[0].get_meta("material")
	CombatFeel.flash_material(m, [0.7, Color(1, 0.5, 0.25)])
	eq(m.get_shader_parameter("flash"), 0.7, "a hit flashes it")
	b.free()


## A thing one can break wears two rings and warm edges that glow and dim; the other props do
## not.
func test_breakables_marked() -> void:
	var b := _map(1)
	for o in b.breakables:
		var m: ShaderMaterial = o.get_meta("material")
		var dark := m.next_pass as ShaderMaterial
		check(dark != null and dark.shader == ArtKit.BREAKABLE_OUTLINE, "%s: a dark ring" % o.name)
		var light := dark.next_pass as ShaderMaterial if dark != null else null
		check(
			light != null and light.shader == ArtKit.BREAKABLE_OUTLINE, "%s: a light ring" % o.name
		)
		var glow := light.next_pass as ShaderMaterial if light != null else null
		check(glow != null and glow.shader == ArtKit.BREAKABLE_GLOW, "%s: warm edges" % o.name)
	var others := 0
	for p in b.props:
		if p.get_parent() != null and p.get_parent().name == "Props":
			var m: Material = MapArt._material_of(p)
			check(m == null or m.next_pass == null, "%s is not" % p.name)
			others += 1
	check(others > 0, "props around")
	b.free()


## The rings read on any ground and in any wood: the light one stays light all through its
## pulse, the dark one stays dark, and the dark one lies out past the light one and behind it, in
## any window, so both show.
func test_breakable_rings() -> void:
	var dark := ArtKit.breakable_rings()
	var light := dark.next_pass as ShaderMaterial
	for key in ["color", "peak"]:
		check(dark.get_shader_parameter(key).get_luminance() < 0.2, "dark: %s" % key)
		check(light.get_shader_parameter(key).get_luminance() > 0.8, "light: %s" % key)
	for key in ["width_px", "min_pixels"]:
		check(
			dark.get_shader_parameter(key) >= light.get_shader_parameter(key) + 1.0,
			"the dark one a pixel further out: %s" % key
		)
	check(light.get_shader_parameter("min_pixels") >= 1.0, "light: a whole pixel of the world")
	check(dark.get_shader_parameter("behind") > 0.0, "the dark one behind the light one")
	eq(light.get_shader_parameter("behind"), 0.0, "the light one where the thing is")
	check(ArtKit.breakable_rings() == dark, "shared by all")


func test_the_mission_stands_on_the_new_maps() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 5, "mission": 0, "seed": 2}
	var screen: Control = Router.make(Router.SCREENS["mission"])
	root.add_child(screen)
	screen.set_process(false)
	check(screen.builder is MapArt, "the map in the new art")
	check(screen.world.find_child("Sun", true, false) is DirectionalLight3D, "the sun")
	var env: WorldEnvironment = screen.world.find_children("*", "WorldEnvironment", true, false)[0]
	check(env.environment.fog_enabled, "the air")
	for i in 20:
		screen._process(screen.tick)
	check(screen.sim.hero != null, "the hero plays on it")
	screen.queue_free()
	Router.params = old


func test_each_map_has_its_own_air() -> void:
	var scene := load(MapLight.SCENE) as PackedScene
	var a: MapLight = scene.instantiate()
	var b: MapLight = scene.instantiate()
	root.add_child(a)
	root.add_child(b)
	check(a.air.environment != b.air.environment, "a screen can change its air alone")
	eq(a.air.environment.background_color, ArtKit.AIR, "the land fades into grey dust")
	check(a.sun.shadow_enabled, "soft shadows")
	a.free()
	b.free()
