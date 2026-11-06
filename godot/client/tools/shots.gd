extends Node
## Screenshots of the real game, for review (needs a display, not --headless):
##   godot --path godot/client --resolution 1280x720 res://tools/shots.tscn -- OUT_DIR
## Opens the main scene, walks through the screens and some maps, saves PNGs to OUT_DIR.

const MAPS: Array[int] = [1, 5, 10, 20, 30, 40]


func _ready() -> void:
	var args := OS.get_cmdline_user_args()
	var out := args[0] if args.size() > 0 else "user://shots"
	DirAccess.make_dir_recursive_absolute(out)
	var main: Node = load("res://scenes/main.tscn").instantiate()
	add_child(main)
	await _frames(10)
	await _shot(out, "01_title")
	Router.go("main_menu")
	await _shot(out, "02_main_menu")
	Router.push("settings")
	await _shot(out, "03_settings")
	Router.go("map_viewer")
	var viewer: Node = Router.current
	for n in MAPS:
		viewer.show_map(n)
		await _frames(30)
		await _shot(out, "map_%02d" % n)
	# A few steps to the right, to see the walk frame and the camera follow.
	for i in 20:
		viewer.hero.step(Vector2.RIGHT, 1.0 / 60.0)
		await get_tree().physics_frame
	await _shot(out, "map_%02d_walk" % MAPS.back())
	# The campaign: the mission list and the first mission, walking down into the next room.
	Router.go("campaign", {"level": 2, "chapter": 0, "lord": 1})
	await _shot(out, "04_missions")
	Router.go("mission", {"lord": 1, "mission": 0, "seed": 1})
	var mission: Node = Router.current
	await _frames(20)
	await _shot(out, "mission_1_start")
	await _seconds(3.0)  # the banner, then the first soldiers come in through the exit
	await _shot(out, "mission_1_enemies")
	# Fight: walk to the nearest soldier and strike, until the room is cleared.
	var shot_fight := false
	var t0 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < 60000 and not mission.sim.exits_open() and not mission.sim.failed:
		await _fight_step(mission.sim)
		if not shot_fight and Time.get_ticks_msec() - t0 > 5000:
			shot_fight = true
			await _shot(out, "mission_1_fight")
	_release_all()
	print("fight: kills ", mission.sim.kills, " hp ", mission.sim.hero.hp, " open ", mission.sim.exits_open(),
		" failed ", mission.sim.failed, " s ", (Time.get_ticks_msec() - t0) / 1000)
	await _shot(out, "mission_1_cleared")
	Input.action_press("move_right")  # off the barrel's column
	await _seconds(0.3)
	Input.action_release("move_right")
	Input.action_press("move_down")
	await _seconds(6.0)
	Input.action_release("move_down")
	await _seconds(1.0)
	print("room after walking down: ", mission.sim.cell, " stage ", mission.sim.rooms_visited)
	await _shot(out, "mission_1_room_2")
	# Potions in the quick slots of the HUD, then one drunk.
	var msim: RefCounted = mission.sim
	msim.no_enemies = true
	while msim.banner != 0 or not msim.talk.is_empty():
		Input.action_press("attack")
		await _frames(2)
		Input.action_release("attack")
		await _seconds(0.2)
	msim.add_quick_item(4)
	msim.add_quick_item(4)
	msim.add_quick_item(1)
	msim.hero.hp = msim.hero.max_hp / 2
	msim.hero.mp = msim.hero.max_mp / 3
	await _seconds(0.3)
	await _shot(out, "mission_1_potions")
	while msim.banner != 0:
		Input.action_press("attack")
		await _frames(2)
		Input.action_release("attack")
		await _seconds(0.2)
	Input.action_press("potion_1")
	await _frames(2)
	Input.action_release("potion_1")
	await _seconds(0.1)
	print("potion: effect ", msim.effect_item, " step ", msim.effect_step, " hp ", msim.hero.hp)
	await _shot(out, "mission_1_potion_drunk")
	# A general: he comes in with his talk, then the fight.
	Router.go("mission", {"lord": 1, "mission": 0, "seed": 2})
	mission = Router.current
	var sim: RefCounted = mission.sim
	sim.no_enemies = true
	await _seconds(3.0)
	_release_all()
	sim.no_enemies = false
	sim.waves[0] = 1
	sim.waves[1] = 1
	var spot: Vector3i = sim.spawn_spots[0]
	sim.create_enemy(1, spot.x, spot.y, spot.z)
	sim.waves[0] = 0  # he is the room's last enemy
	sim.waves[1] = 0
	sim.room_phase = 0
	await _seconds(1.5)
	await _shot(out, "mission_1_general_talk")
	for i in 8:
		Input.action_press("attack")
		await _frames(2)
		Input.action_release("attack")
		await _seconds(0.15)
	t0 = Time.get_ticks_msec()
	var shot_general := false
	while Time.get_ticks_msec() - t0 < 30000 and not sim.won and not sim.failed:
		await _fight_step(sim)
		if not shot_general and Time.get_ticks_msec() - t0 > 3000:
			shot_general = true
			await _shot(out, "mission_1_general_fight")
			_release_all()
			while not sim.talk.is_empty():  # (a skill waits for the end of his words)
				Input.action_press("attack")
				await _frames(2)
				Input.action_release("attack")
				await _seconds(0.15)
			sim.hero.mp = sim.hero.max_mp  # the first skill, a dash, against the general
			for i in 20:  # (it starts when the hero stands or walks)
				Input.action_press("skill_1")
				await _frames(2)
				Input.action_release("skill_1")
				await _seconds(0.1)
				print("skill try: action ", sim.hero.action, " mp ", sim.hero.mp, " banner ", sim.banner,
					" talk ", sim.talk.size(), " effect ", sim.effect_item)
				if sim.hero.action == 12:
					break
			await _seconds(0.3)
			await _shot(out, "mission_1_skill")
	_release_all()
	print("general: hp ", sim.hero.hp, " won ", sim.won, " failed ", sim.failed)
	await _frames(10)
	await _shot(out, "mission_1_general_end")
	get_tree().quit()


const DIR_ACTIONS := {0: "move_down", 2: "move_left", 4: "move_up", 6: "move_right"}


func _release_all() -> void:
	for a in DIR_ACTIONS.values():
		Input.action_release(a)
	Input.action_release("attack")


## One step of a simple fighter: towards the nearest soldier that is in the room, strike when close.
func _fight_step(sim: RefCounted) -> void:
	var best: Variant = null
	var best_d := 1 << 30
	for e in sim.enemies:
		var d: int = sim.distance(e.pos, sim.hero.pos)
		if e.alerted != 0 and e.hp > 0 and d < best_d:
			best = e
			best_d = d
	_release_all()
	if best != null:
		if best_d <= 40:
			Input.action_press("attack")
		else:
			Input.action_press(DIR_ACTIONS[sim.dir4(sim.hero.pos, best.pos)])
	await _frames(4)
	Input.action_release("attack")
	await _frames(4)


func _seconds(t: float) -> void:
	await get_tree().create_timer(t).timeout


func _frames(n: int) -> void:
	for i in n:
		await get_tree().process_frame


func _shot(out: String, shot_name: String) -> void:
	await _frames(5)
	await RenderingServer.frame_post_draw
	var img := get_viewport().get_texture().get_image()
	img.save_png(out.path_join(shot_name + ".png"))
	print("shot ", shot_name)
