extends Node
## Screenshots of the 3D world's look (the camp, a mission, a fight), for comparing the picture
## before and after a change to how the world is drawn. Needs a display:
##   godot --path godot/client --resolution 1920x1080 res://tools/look_shots.tscn -- OUT_DIR [PREFIX]

const DIR_ACTIONS := ["move_up", "move_right", "move_down", "move_left"]


func _ready() -> void:
	var args := OS.get_cmdline_user_args()
	var out := args[0] if args.size() > 0 else "user://look_shots"
	var prefix := args[1] if args.size() > 1 else ""
	DirAccess.make_dir_recursive_absolute(out)
	var main: Node = load("res://scenes/main.tscn").instantiate()
	add_child(main)
	await _frames(10)
	var walker: RefCounted = load("res://scripts/core/profile.gd").new()
	walker.place = 0
	walker.save("user://look_walker.json")
	Router.go("camp", {"profile_path": "user://look_walker.json"})
	await _seconds(1.0)
	await _shot(out, prefix + "camp_main")
	walker.place = 27
	walker.save("user://look_walker.json")
	Router.go("camp", {"profile_path": "user://look_walker.json"})
	await _seconds(1.0)
	await _shot(out, prefix + "camp_six_ways")
	Router.go("mission", {"lord": 1, "mission": 0, "seed": 1})
	var mission: Node = Router.current
	await _seconds(3.5)
	await _shot(out, prefix + "mission_1_enemies")
	var t0 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < 5000 and not mission.sim.exits_open() and not mission.sim.failed:
		await _fight_step(mission.sim)
	await _shot(out, prefix + "mission_1_fight")
	_release_all()
	Router.go("mission", {"lord": 3, "mission": 2, "seed": 3})
	await _seconds(3.0)
	await _shot(out, prefix + "mission_lord3")
	get_tree().quit()


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


func _release_all() -> void:
	for a in DIR_ACTIONS + ["attack"]:
		Input.action_release(a)


func _seconds(s: float) -> void:
	await get_tree().create_timer(s).timeout


func _frames(n: int) -> void:
	for i in n:
		await get_tree().process_frame


func _shot(out: String, shot_name: String) -> void:
	await _frames(5)
	await RenderingServer.frame_post_draw
	var img := get_viewport().get_texture().get_image()
	img.save_png(out.path_join(shot_name + ".png"))
	print("shot ", shot_name)
