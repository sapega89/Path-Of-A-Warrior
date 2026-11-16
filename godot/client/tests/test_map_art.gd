extends "res://tests/test_case.gd"
## The maps in the new art (scripts/world/map_art.gd): every part and prop of the campaign's
## maps is known; on the tests' own maps the ground rises where it is blocked and stays flat
## where people walk, the faces of cliffs climb, bridges and decks hold, what stands on a cell is
## a 3D piece, the breakable ones flash.


## One of the tests' own maps (three_rooms, terrain) in the new art.
func _map(name: String) -> Node3D:
	var b: Node3D = MapArt.new()
	root.add_child(b)
	b.build(own_map(name))
	return b


func _kind(b: Node3D, x: int, y: int) -> String:
	return b.kinds[int(b._part(x * MapArt.PARTS + 1, y * MapArt.PARTS + 1)[0])]


func test_every_part_and_prop_is_known() -> void:
	eq(MapArt.KIND_LETTERS.length(), MapArt.KINDS.size(), "a letter for each kind of ground")
	for k in MapArt.KINDS:
		check(MapArt.KIND_COLOUR.has(k), "a colour for %s" % k)
	var breakable: Array = MapSim.table("breakable_prop")
	eq(MapSim.table("breakable_hp").size(), breakable.size(), "a strength for each breakable")
	for code in range(1, breakable.size()):
		check(
			MapArt.PROP.has(breakable[code]), "breakable %d: %s is drawn" % [code, breakable[code]]
		)
	for n in range(1, MapBuilder.map_count() + 1):
		var m := MapBuilder.load_map(n)
		var unknown := {}
		for letters: String in m.parts:
			for letter in letters:
				if not letter in MapArt.KIND_LETTERS:
					unknown[letter] = true
			if letters.length() != MapArt.PARTS * MapArt.PARTS:
				unknown[letters] = true
		for what: String in m.props:
			if what != "" and not (MapArt.PROP.has(what) or MapArt.CLUSTERS.has(what)):
				unknown[what] = true
		for code in m.objects:
			if int(code) < 0 or int(code) >= breakable.size():
				unknown[code] = true
		eq(unknown.keys(), [], "map %d: every part, prop and object is known" % n)


func test_people_walk_on_flat_ground() -> void:
	for name in ["three_rooms", "terrain"]:
		var b := _map(name)
		var raised := 0
		for y in b.h:
			for x in b.w:
				if b.is_blocked(x, y):
					raised += 1 if b.height_of(x, y) > 0.0 else 0
				else:
					eq(b.height_of(x, y), 0.0, "%s: (%d, %d) is free and flat" % [name, x, y])
		check(raised > 0, "%s: some blocked cells rise" % name)
		b.free()


func test_the_ground_and_around() -> void:
	var b := _map("three_rooms")
	var ground: Node3D = b.get_node("Ground")
	check(ground.get_child_count() > 1, "in chunks")
	var corners := {}
	var lo := Vector3(INF, INF, INF)
	var hi := -lo
	for chunk: MeshInstance3D in ground.get_children():
		check(chunk.material_override == b.ground_material, "%s: painted as one" % chunk.name)
		for v: Vector3 in chunk.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]:
			corners[Vector2(v.x, v.z)] = true
			lo = lo.min(v)
			hi = hi.max(v)
	var m := MapArt.MARGIN
	eq(
		corners.size(),
		((b.w + 2 * m) * MapArt.PARTS + 1) * ((b.h + 2 * m) * MapArt.PARTS + 1),
		"a grid of parts"
	)
	eq(
		[lo.x, lo.z, hi.x, hi.z],
		[-float(m), -float(m), float(b.w + m), float(b.h + m)],
		"the land goes on past the edges"
	)
	check(
		b.hills(-m, -m) > 0.5 and b.hills(b.w / 2.0, b.h / 2.0) == 0.0, "hills around, flat inside"
	)
	check(b.ground_material.shader == MapArt.GROUND_SHADER, "painted by its shader")
	var blocked := 0
	for y in b.h:
		for x in b.w:
			blocked += 1 if b.is_blocked(x, y) else 0
	eq(b.get_node("Collision").get_child_count(), blocked + 5, "the same collision as before")
	b.free()


## The cliff of the terrain map: its stone top in rows 0 and 1, its face of rock in rows 2..4.
func test_a_cliff_climbs_to_its_top() -> void:
	var b := _map("terrain")
	eq(_kind(b, 2, 1), "stone", "the top of the cliff")
	eq(b.height_of(2, 1), MapArt.RAISE["stone"], "rises")
	eq(_kind(b, 2, 3), "rock", "its face")
	var pw: int = b.w * MapArt.PARTS
	var faces := 0
	for py in range(MapArt.PARTS * 2, MapArt.PARTS * 5):
		if b.part_face[py * pw + 2 * MapArt.PARTS] == 1:
			faces += 1
			var here: float = b.part_raise[py * pw + 2 * MapArt.PARTS]
			var above: float = b.part_raise[(py - 1) * pw + 2 * MapArt.PARTS]
			check(
				here > 0.0 and here < above,
				"the face climbs north: %.2f under %.2f" % [here, above]
			)
	check(faces >= 9, "the face of the cliff: %d parts" % faces)
	b.free()


func test_a_pit_in_the_cliff_is_filled() -> void:
	var b := _map("terrain")
	eq(b.prop_at(3, 1), "pebbles", "pebbles on the cliff's top")
	check(b.is_blocked(3, 1), "blocked")
	eq(b.height_of(3, 1), b.height_of(2, 1), "the cell rises with the cliff")
	var on_top := false
	for p in b.props:
		if p.position.distance_to(Vector3(3.5, b.height_of(3, 1), 1.5)) < 0.01:
			on_top = true
	check(on_top, "the pebbles lie on its top")
	b.free()


## The river of the terrain map runs down columns 9 and 10, the log bridge across it in row 4.
func test_water_bridges_and_decks() -> void:
	var b := _map("terrain")
	check(b.has_node("Water"), "a river")
	eq(_kind(b, 9, 4), "wood", "a log bridge")
	eq(_kind(b, 10, 4), "wood", "over the water")
	check(not b.is_blocked(10, 4), "people cross it")
	eq(b.prop_at(9, 3), "palisade", "a post at its side")
	eq(_kind(b, 9, 3), "wood", "stands on a deck, not in the water")
	eq(_kind(b, 9, 0), "water", "the river")
	b.free()


func test_what_stands_on_the_map() -> void:
	var b := _map("terrain")
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
	var b := _map("terrain")
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
	var b := _map("three_rooms")
	eq(b.breakables.size(), 6, "breakable objects")
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
	var b := _map("three_rooms")
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
	Router.params = {"lord": 5, "mission": 0, "seed": 2, "map_path": own_map_path("terrain")}
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
