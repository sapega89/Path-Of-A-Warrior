extends "res://tests/test_case.gd"
## The multiplayer battle in the new art: who each fighter is (scripts/world/battle_motion.gd),
## the clips of the battle's animations, the field of each background
## (scripts/world/battle_arena.gd), and the screen of a Solo Mission played step by step: the
## upyr, the portraits on the plates, the chevron over the target, the blade's trail and the
## blood of a hit.

const OnlineBattle := preload("res://scripts/net/online_battle.gd")
const ClientTests := preload("res://tests/test_online_client.gd")
const OnlineTests := preload("res://tests/test_online_server.gd")
const ServerTests := preload("res://tests/test_server.gd")
const BattleScreen := preload("res://scripts/screens/online_battle_screen.gd")
const BattleMotion := preload("res://scripts/world/battle_motion.gd")
const BattleArena := preload("res://scripts/world/battle_arena.gd")
const MapPeople := preload("res://scripts/world/map_people.gd")
const Pictures := preload("res://scripts/ui/pictures.gd")
const ArtKit := preload("res://scripts/art/art_kit.gd")


func _dir() -> String:
	var d := "user://test_battle_art_%d" % randi()
	DirAccess.make_dir_recursive_absolute(d)
	return d


## A battle of the server's online game in this process: [client, its dir].
func _battle(mode: int) -> Array:
	var d := _dir()
	var net = ClientTests.Net.new(d)
	net.o.match_wait = 0
	var c: RefCounted = net.client("ANDREY", OnlineTests.HERO)
	c.enter(func(_e): pass)
	c.find_battle(mode, func(_e): pass)
	return [c, d]


func test_who_is_who() -> void:
	var f := OnlineBattle.Fighter.new()
	f.kind = OnlineBattle.PLAYER
	for face in 4:
		f.face = face
		eq(BattleMotion.kind_of(f), MapPeople.HEROES[face], "a player: the model of his class")
		eq(BattleMotion.portrait_of(f), 38 + face, "and its portrait")
	f.weapon = 1
	eq(BattleMotion.weapons_of(f), ["palash"], "his blade")
	f.kind = OnlineBattle.CPU
	var kinds := {}
	for name in ["Brakka", "Kaida", "Ulric", "Ysolde", "Dorn", "Borin", "Thane", "Selene"]:
		f.name = name
		var kind := BattleMotion.kind_of(f)
		check(kind in BattleMotion.RIVALS, "%s: a rival" % name)
		eq(BattleMotion.kind_of(f), kind, "the same one for the same name")
		eq(
			BattleMotion.portrait_of(f),
			BattleMotion.RIVAL_PORTRAITS[BattleMotion.RIVALS.find(kind)],
			"his portrait"
		)
		kinds[kind] = true
	eq(kinds.size(), 3, "all three rivals among them")
	eq(BattleMotion.weapons_of(f), [], "the server's fighters keep their own weapons")
	f.kind = OnlineBattle.MONSTER
	eq([BattleMotion.kind_of(f), BattleMotion.portrait_of(f)], ["upyr", 45], "a monster: the upyr")
	var upyr: Node = ArtKit.scene("characters/upyr.glb").instantiate()
	check(upyr.find_child("Skeleton3D", true, false) != null, "the upyr is rigged as the others")
	check(upyr.find_child("bulava", true, false) != null, "with his club")
	upyr.free()


func test_every_animation_has_its_clip() -> void:
	var clips := ArtKit.clips()
	for anim in BattleMotion.ANIMS:
		check(
			clips.has_animation(BattleMotion.ANIMS[anim][0]),
			"animation %d: %s" % [anim, BattleMotion.ANIMS[anim]]
		)
	var got: Array = _battle(0)
	var b: RefCounted = got[0].battle
	var f: RefCounted = b.fighters[1]
	b.state = OnlineBattle.TURN
	b.attacker = 1
	f.anim = 3
	eq(BattleMotion.motion(b, 1)[0], "attack_slash", "a blow")
	f.kind = OnlineBattle.MONSTER
	eq(BattleMotion.motion(b, 1)[0], "attack_chop", "the club comes down")
	b.state = OnlineBattle.CHOOSE
	eq(
		[BattleMotion.anim_of(b, 1), BattleMotion.motion(b, 1)[0]],
		[0, "idle"],
		"between the rounds: standing"
	)
	f.hp = 0
	check(BattleMotion.fallen(b, 1), "fallen")
	eq(BattleMotion.motion(b, 1), BattleMotion.ANIMS[6], "lies as at the end of a fall")
	b.state = OnlineBattle.TURN
	f.anim = 6
	check(not BattleMotion.fallen(b, 1) and BattleMotion.motion(b, 1)[0] == "death", "falls")
	b.anim_frame = 1
	b.anim_length = 2
	eq(BattleMotion.progress(b, 1), Vector2i(1, 2), "half of it")
	ServerTests._rm(got[1])


func test_the_fields() -> void:
	var stage := Node3D.new()
	root.add_child(stage)
	var seen := {}
	for scenery in 4:
		var a: Node3D = BattleArena.new()
		stage.add_child(a)
		a.build((2 << 4) | scenery)
		var field: Node = a.get_node("Field")
		var things: Array = []
		for c in field.get_children():
			if c != a.ground:
				things.append(String(c.name).rstrip("0123456789"))
		things.sort()
		check(things.size() >= 12, "scenery %d: %d things" % [scenery, things.size()])
		seen[str(things)] = true
		var ground := a.ground.get_node("Ground") as MeshInstance3D
		eq(
			(ground.material_override as ShaderMaterial).get_shader_parameter("grass_green"),
			BattleArena.GROUNDS[2][2],
			"dry steppe"
		)
		eq(a.sky_settings(), BattleArena.DAY, "by day")
		var old: Node = a.get_node("Field")
		a.build((2 << 4) | scenery)
		check(a.get_node("Field") == old, "the same background: built once")
		a.build((1 << 6) | scenery)
		eq([a.sky_settings().stars, a.ground_kind], [1.0, 0], "at night, on a green meadow")
	eq(seen.size(), 4, "four sceneries, each its own")
	stage.free()


func test_a_mission_on_the_screen() -> void:
	var got: Array = _battle(2)
	var c: RefCounted = got[0]
	var old: Dictionary = Router.params
	Router.params = {"online": c, "profile_path": String(got[1]).path_join("hero.json")}
	var screen: Control = BattleScreen.new()
	root.add_child(screen)
	screen.size = Vector2(1280, 720)
	screen.set_process(false)
	var b: RefCounted = c.battle
	eq(b.mode, 2, "a Solo Mission")
	check(screen.arena.scenery == b.bg & 3, "the field of its background")
	var text := FileAccess.get_file_as_string("res://scripts/screens/online_battle_screen.gd")
	for old_art in ["fighter_", "gamebg", '"ui%d"', "act%d", "face%d", "monster_r"]:
		check(not text.contains(old_art), "no sprite of the old screen: " + old_art)
	var seen := {}
	for i in 6000:
		b.tick()
		screen._refresh()
		if b.state == OnlineBattle.RESULT or b.left:
			break
		if not seen.has("people") and b.state == OnlineBattle.CHOOSE:
			seen["people"] = true
			var monsters := 0
			for k in 4:
				var f: RefCounted = b.fighters[k]
				eq(screen.figures[k].kind, BattleMotion.kind_of(f), "fighter %d as who he is" % k)
				var face := BattleMotion.portrait_of(f)
				eq(screen.portraits[k].texture, Pictures.portrait(face), "his portrait")
				# the hero's portraits look to the left, the others to the right: each looks across
				eq(
					screen.portraits[k].flip_h,
					(face >= 38 and face < 42) != f.mirrored(),
					"fighter %d looks across" % k
				)
				eq(
					screen.portraits[k].position.x > screen.size.x / 2.0,
					f.mirrored(),
					"fighter %d on his side" % k
				)
				if f.kind == OnlineBattle.MONSTER:
					monsters += 1
					eq(screen.figures[k].kind, "upyr", "a monster")
			eq(monsters, 2, "two monsters")
		match b.state:
			OnlineBattle.CHOOSE:
				if not b.exit_prompt and b.state_ticks >= 3:
					b.key("right")
			OnlineBattle.TARGET:
				if b.state_ticks >= 3:
					var t: int = b.target_cursor
					check(
						(
							screen.marker.visible
							and (
								screen.marker.position.distance_to(
									(
										screen.bodies[t].position
										+ Vector3(0, BattleScreen.MARKER_UP, 0)
									)
								)
								< 0.01
							)
						),
						"the chevron over the target"
					)
					seen["target"] = true
					b.key("fire")
			OnlineBattle.BAR:
				if b.state_ticks == 6:
					b.key("fire")
		for e in screen.effects.drawn:
			seen[e[0]] = true
	for what in ["people", "target", "trail", "blood"]:
		check(seen.has(what), "seen: " + what)
	screen.free()
	Router.params = old
	ServerTests._rm(got[1])
