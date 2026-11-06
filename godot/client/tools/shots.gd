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
	Input.action_press("move_down")
	await _seconds(6.0)
	Input.action_release("move_down")
	await _seconds(1.0)
	print("room after walking down: ", mission.sim.cell, " stage ", mission.sim.rooms_visited)
	await _shot(out, "mission_1_room_2")
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
