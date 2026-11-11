extends Node
## Screenshots of the real game, for review (needs a display, not --headless):
##   godot --path godot/client --resolution 1280x720 res://tools/shots.tscn -- OUT_DIR
## Opens the main scene, walks through the screens and some maps, saves PNGs to OUT_DIR.

const MAPS: Array[int] = [1, 5, 10, 20, 30, 40]
const DIR_ACTIONS := {0: "move_down", 2: "move_left", 4: "move_up", 6: "move_right"}


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
	Router.current.ask.popup_centered()  # a new game over a saved one: the game's question, No first
	await _shot(out, "02_main_menu_delete_ask")
	Router.current.ask.hide()
	# A new game: the difficulty, the face, the name, the points.
	Router.push("new_game", {"profile_path": "user://shot_new.json"})
	var ng: Node = Router.current
	await _shot(out, "02a_new_difficulty")
	ng.choose_difficulty(1)
	ng.ask.hide()
	ng.show_step(ng.Step.HERO)
	await _frames(2)
	ng.body.get_child(0).get_child(2).grab_focus()
	await _shot(out, "02b_new_hero")
	ng.body.get_child(0).get_child(1).grab_focus()
	await _shot(out, "02b_new_hero_guardian")
	ng.choose_head(2)
	ng.name_edit.text = "Andrey"
	await _frames(1)
	ng.body.get_node("Keys").key("d").grab_focus()  # the keys under the name, as with a gamepad
	await _frames(2)
	await _shot(out, "02c_new_name")
	ng.submit_name()
	for i in 3:
		ng.spend(0)
	await _shot(out, "02d_new_points")
	for i in 2:  # the last points: the question to go on
		ng.spend(0)
	await _shot(out, "02e_new_ask")
	ng.ask.hide()
	Router.push("settings")
	await _shot(out, "03_settings")
	Router.current.open_controls()
	await _shot(out, "03b_controls")
	# Management and Attributes, with a hero who has put three points into HP.
	Router.go("main_menu")
	Router.push("management", {"profile_path": "user://shot_hero.json"})
	await _shot(out, "05_management")
	var hero: RefCounted = Profile.new()
	for i in 3:
		hero.spend_point(0)
	hero.gold = 300
	hero.save("user://shot_hero.json")
	Router.push("attributes", Router.params)
	await _shot(out, "06_attributes")
	Router.current.open_reset()
	await _shot(out, "06a_attributes_reset")
	Router.current.ask.hide()
	Router.current.finish_reset(false)
	await _shot(out, "06b_attributes_reset_done")
	Router.current.note.hide()
	# Skills: four learned skills, Storm Sabre on the third key, the cursor on the third key.
	Router.back()
	for i in [1, 5, 8]:
		hero.skill_levels[i] = 1
	hero.hotkeys = [12, 17, 13, 0, 0]
	hero.save("user://shot_hero.json")
	Router.push("skills", Router.params)
	await _frames(2)
	Router.current.slot = 2
	Router.current.refresh()
	Router.current.skills[20].grab_focus()
	await _shot(out, "07_skills")
	# Gear and Inventory: a helmet and armour worn, a few things and some gold in the backpack.
	Router.back()
	var items: GDScript = load("res://scripts/core/items.gd")
	for id in [131, 136]:
		hero.add_item(items.make(id))
		hero.use_item(0)
	for id in [126, 146, 102, 434, 503]:
		hero.add_item(items.make(id))
	hero.gold = 1250
	hero.save("user://shot_hero.json")
	Router.push("gear", Router.params)
	await _frames(2)
	Router.current.places[5].grab_focus()
	await _shot(out, "08_gear")
	Router.back()
	Router.push("inventory", Router.params)
	await _frames(2)
	Router.current.cells[1].grab_focus()
	await _shot(out, "09_inventory")
	Router.current.cells[42].grab_focus()
	await _frames(2)
	await _shot(out, "09a_inventory_last_rows")
	# Assign Items: three kinds of potion, the second key on the blue ones.
	Router.back()
	hero.quick_slots = [[1, 3], [4, 2], [7, 1], [0, 0], [0, 0]]
	hero.quick_keys = [0, 1]
	hero.save("user://shot_hero.json")
	Router.push("assign_items", Router.params)
	await _frames(2)
	Router.current.press_slot(2)
	Router.current.slots[2].grab_focus()
	await _shot(out, "10_assign_items")
	# The game menu, and its end: the list scrolls down to Help.
	Router.go("main_menu")
	Router.push("game_menu", {"profile_path": "user://shot_hero.json"})
	await _frames(2)
	await _shot(out, "11a_game_menu")
	Router.current.buttons[-1].grab_focus()  # Help, at the end: the list scrolls down
	await _frames(3)
	await _shot(out, "11a_game_menu_end")
	# The Blacksmith: buying from the shop, and enchanting the sword in hand.
	Router.go("main_menu")
	Router.push("blacksmith", {"profile_path": "user://shot_hero.json"})
	await _shot(out, "14_blacksmith")
	Router.current.open_page("buy")
	await _frames(2)
	Router.current.cells[9].grab_focus()
	await _shot(out, "15_shop_buy")
	Router.back()
	Router.current.open_page("enchant")
	await _frames(2)
	Router.current.cells[25].grab_focus()
	Router.current.press_cell(25)
	await _frames(2)
	await _shot(out, "16_enchant_ask")
	Router.current.ask.hide()
	Router.current.sparkle = 3  # the sparkle after Yes, without the outcome
	Router.current.sparkle_cells = [25] as Array[int]
	Router.current.redraw_sparkle()
	await _shot(out, "16_enchant_sparkle")
	Router.current.sparkle = -1
	Router.current.redraw_sparkle()
	Router.back()
	Router.current.open_page("combine")
	await _frames(2)
	Router.current.press_cell(0)
	Router.current.press_cell(2)
	Router.current.cells[2].grab_focus()
	await _shot(out, "17_combine")
	# Visiting: three friends after a won mission; Jan Gorski's greeting, the topics, the gift.
	hero = Profile.load_or_new("user://shot_hero.json")
	hero.friendship = {"4": 100, "13": 35, "29": 5}
	hero.can_visit = true
	hero.save("user://shot_hero.json")
	Router.go("main_menu")
	Router.push("visiting", {"profile_path": "user://shot_hero.json", "seed": 7})
	await _shot(out, "18_visiting_list")
	var visit: Node = Router.current
	visit.open(4)
	for i in 5:  # each line typed out at once, then the next
		visit.press()
	await _shot(out, "19_visiting_greeting")
	visit.press()
	await _shot(out, "20_visiting_topic")
	visit.choose(2)
	for i in 4:
		visit.press()
	visit.press()
	await _shot(out, "21_visiting_gift")
	# Endings: three reached, the cursor on one that is not.
	hero.endings = (1 << 0) | (1 << 2) | (1 << 3)
	hero.save("user://shot_hero.json")
	Router.go("main_menu")
	Router.push("endings", {"profile_path": "user://shot_hero.json"})
	await _frames(2)
	Router.current.list.get_child(1).grab_focus()
	Router.current.open(1)
	await _shot(out, "22_endings")
	# Help: the topics, then the second page of Blacksmith.
	Router.go("main_menu")
	Router.push("help")
	await _shot(out, "23_help")
	Router.current.open(2)
	Router.current.turn_page(1)
	await _shot(out, "24_help_page")
	Router.current.open(Router.current.CONTROL_TOPIC)  # Control: this version's keys
	await _shot(out, "24b_help_control")
	# A story: ending 2's talk, its first picture with its text floating up, its numbers and the
	# reward.
	Router.go("main_menu")
	Router.push(
		"story",
		{"story": 2, "reward_item": 502, "opened_lord": 8, "profile_path": "user://shot_hero.json"}
	)
	await _frames(2)
	var story: Node = Router.current
	for i in 5:
		story.next_page()
	story.press()
	await _shot(out, "11_story_talk")
	while story.pages[story.page].kind == "talk":
		story.next_page()
	for i in 50:
		story.tick()
	await _shot(out, "12_story_picture")
	story.page = story.pages.size() - 2
	story.next_page()
	for i in 120:
		story.tick()
	await _shot(out, "13_story_end")
	story.reward.hide()
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
	InputSetup.device = "pad"  # the top line names LB / RB and B
	viewer.show_info()
	await _shot(out, "map_%02d_pad" % MAPS.back())
	InputSetup.device = "keys"
	# The campaign: the mission list and the first mission, walking down into the next room.
	# The lords to fight for from chapter 5: Assassin and Brotherhood are not open yet.
	var walker: RefCounted = Profile.new()
	walker.place = 5
	walker.done["1:0"] = true
	walker.save("user://shot_walker.json")
	Router.go("campaign", {"profile_path": "user://shot_walker.json"})
	await _shot(out, "04_lords")
	Router.go("campaign", {"level": 2, "lord": 1, "profile_path": "user://shot_walker.json"})
	await _shot(out, "04_missions")
	# A mission's description, the question whether to accept it, the briefing typed out.
	Router.go(
		"campaign", {"level": 3, "lord": 1, "mission": 0, "profile_path": "user://shot_walker.json"}
	)
	await _shot(out, "04b_mission_description")
	Router.current.ask_accept()
	await _shot(out, "04c_mission_accept")
	Router.current.ask.hide()
	Router.go(
		"briefing", {"lord": 1, "mission": 0, "line": 0, "profile_path": "user://shot_walker.json"}
	)
	Router.current.process_mode = Node.PROCESS_MODE_DISABLED  # the briefing held still
	Router.current.press()
	Router.current.next_line()
	Router.current.press()
	await _shot(out, "04d_briefing")
	# The camps between missions: a stop with a way per mission (one place closed) and its
	# pause menu, six ways, the main camp at the start, its smithy and all of it from above, and
	# the town hall that every camp has.
	walker.place = 4
	walker.save("user://shot_walker.json")
	Router.go("camp", {"profile_path": "user://shot_walker.json"})
	await _shot(out, "04e_camp_fork")
	Router.current.toggle_menu()
	await _shot(out, "04k_camp_menu")
	walker.place = 27
	walker.save("user://shot_walker.json")
	Router.go("camp", {"profile_path": "user://shot_walker.json"})
	await _shot(out, "04f_camp_six_ways")
	walker.place = 0
	walker.save("user://shot_walker.json")
	Router.go("camp", {"profile_path": "user://shot_walker.json"})
	await _shot(out, "04g_camp_main")
	var camp: Node = Router.current  # the hero by the anvil, then the whole camp
	camp.hero.global_position = camp.spot_of("smith").at
	camp.camera.snap()
	await _shot(out, "04i_camp_smith")
	camp.camera.distance = 42.0
	camp.camera.snap()
	await _shot(out, "04j_camp_overview")
	# the town hall of the start camp: the flasks and the button that buys the next one
	Router.go("town_hall", {"profile_path": "user://shot_walker.json", "start": true})
	await _shot(out, "04h_town_hall")
	Router.go("run_end", {"profile_path": "user://shot_walker.json"})
	await _shot(out, "04k_run_end")
	Router.go("mission", {"lord": 1, "mission": 0, "seed": 1})
	var mission: Node = Router.current
	await _frames(20)
	await _shot(out, "mission_1_start")
	await _seconds(3.0)  # the banner, then the first soldiers come in through the exit
	await _shot(out, "mission_1_enemies")
	# The slots' labels name the device in use: an Xbox pad, then a PlayStation one.
	InputSetup.device = "pad"
	InputSetup.pad_brand = "xbox"
	await _shot(out, "mission_1_hud_xbox")
	InputSetup.pad_brand = "ps"
	await _shot(out, "mission_1_hud_ps")
	InputSetup.device = "keys"
	InputSetup.pad_brand = "generic"
	# The pause menu over the mission, then its Options.
	Router.current.pause()
	await _shot(out, "mission_1_pause")
	Router.current.pause_menu.open_options()
	await _shot(out, "mission_1_pause_options")
	Router.current.pause_menu.close_options()
	Router.current.pause_menu.open_help()
	await _shot(out, "mission_1_pause_help")
	Router.current.pause_menu.close_options()
	Router.current.pause_menu.open_items()
	await _shot(out, "mission_1_pause_items")
	Router.current.pause_menu.close_options()
	Router.current.pause_menu.buttons[4].pressed.emit()
	await _shot(out, "mission_1_pause_exit_ask")
	Router.current.pause_menu.ask.hide()
	Router.current.resume()
	# Fight: walk to the nearest soldier and strike, until the room is cleared.
	var shot_fight := false
	var t0 := Time.get_ticks_msec()
	while (
		Time.get_ticks_msec() - t0 < 60000
		and not mission.sim.exits_open()
		and not mission.sim.failed
	):
		await _fight_step(mission.sim)
		if not shot_fight and Time.get_ticks_msec() - t0 > 5000:
			shot_fight = true
			await _shot(out, "mission_1_fight")
	_release_all()
	print(
		"fight: kills ",
		mission.sim.kills,
		" hp ",
		mission.sim.hero.hp,
		" open ",
		mission.sim.exits_open(),
		" failed ",
		mission.sim.failed,
		" s ",
		(Time.get_ticks_msec() - t0) / 1000
	)
	await _shot(out, "mission_1_cleared")
	Router.current.toggle_auto()  # the AUTO corner lit (switched off again at once)
	await _shot(out, "mission_1_auto_on")
	Router.current.toggle_auto()
	# Save on the map once the room is clear (the shots' own hero file is put back after).
	var kept := FileAccess.get_file_as_string("user://hero.json")
	Router.current.pause()
	Router.current.pause_menu.save()
	await _shot(out, "mission_1_pause_saved")
	Router.current.pause_menu.note.hide()
	Router.current.resume()
	if kept.is_empty():
		DirAccess.remove_absolute(ProjectSettings.globalize_path("user://hero.json"))
	else:
		FileAccess.open("user://hero.json", FileAccess.WRITE).store_string(kept)
	_press("move_right")  # off the barrel's column
	await _seconds(0.3)
	_release("move_right")
	_press("move_down")
	await _seconds(6.0)
	_release("move_down")
	await _seconds(1.0)
	print("room after walking down: ", mission.sim.cell, " stage ", mission.sim.rooms_visited)
	await _shot(out, "mission_1_room_2")
	# Potions in the quick slots of the HUD, then one drunk.
	var msim: RefCounted = mission.sim
	msim.no_enemies = true
	while msim.banner != 0 or not msim.talk.is_empty():
		_press("attack")
		await _frames(2)
		_release("attack")
		await _seconds(0.2)
	msim.add_quick_item(4)
	msim.add_quick_item(4)
	msim.add_quick_item(1)
	msim.hero.hp = msim.hero.max_hp / 2
	msim.hero.mp = msim.hero.max_mp / 3
	await _seconds(0.3)
	await _shot(out, "mission_1_potions")
	while msim.banner != 0:
		_press("attack")
		await _frames(2)
		_release("attack")
		await _seconds(0.2)
	_press("potion_1")
	await _frames(2)
	_release("potion_1")
	await _seconds(0.13)
	print("potion: effect ", msim.effect_item, " mp ", msim.hero.mp)
	await _shot(out, "mission_1_potion_drunk")
	# Frames of effects held still: a buff skill, the dash, a fire scroll's blast.
	mission.set_process(false)
	for fx in [["buff", 17, 6], ["dash", 12, 4], ["heal", 15, 8]]:
		msim.hero.action = fx[1]
		msim.hero.frame = fx[2]
		mission._update_view(1.0)
		await _frames(3)
		await _shot(out, "mission_1_fx_%s" % fx[0])
	msim.hero.action = 0
	msim.hero.frame = 0
	msim.effect_item = -2
	msim.effect_step = 1
	msim.effect_pos = msim.hero.pos + Vector2i(0, 60)
	mission._update_view(1.0)
	await _frames(3)
	await _shot(out, "mission_1_fx_blast")
	msim.effect_item = 0
	# A hit spark held still on the hero.
	msim.hero.hit_fx_kind = 1
	msim.hero.hit_fx_frame = 0
	msim.hero.hit_fx_pos = msim.hero.pos
	mission._update_view(1.0)
	await _frames(3)
	await _shot(out, "mission_1_fx_spark")
	msim.hero.hit_fx_kind = 0
	# The fire held still on the soldier nearest the camera: a fire skill hit him.
	var burning = null
	for e in msim.enemies:
		if burning == null or e.pos.y > burning.pos.y:
			burning = e
	if burning != null:
		burning.on_fire = true
		burning.fire_frame = 3
		mission._update_view(1.0)
		await _frames(3)
		await _shot(out, "mission_1_fx_fire")
		burning.on_fire = false
	# A weapon trail held still: the whirling strike.
	msim.hero.action = 25
	msim.hero.frame = 3
	mission.trails = msim.trails(RandomNumberGenerator.new())
	mission._update_view(1.0)
	await _frames(3)
	await _shot(out, "mission_1_fx_trail")
	msim.hero.action = 0
	msim.hero.frame = 0
	mission.trails = []
	mission.set_process(true)
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
		_press("attack")
		await _frames(2)
		_release("attack")
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
				_press("attack")
				await _frames(2)
				_release("attack")
				await _seconds(0.15)
			sim.hero.mp = sim.hero.max_mp  # the first skill, a dash, against the general
			for i in 20:  # (it starts when the hero stands or walks)
				_press("skill_1")
				await _frames(2)
				_release("skill_1")
				await _seconds(0.1)
				if sim.hero.action == 12:
					break
			await _seconds(0.3)
			print("skill: action ", sim.hero.action, " mp ", sim.hero.mp)
			await _shot(out, "mission_1_skill")
	_release_all()
	print("general: hp ", sim.hero.hp, " won ", sim.won, " failed ", sim.failed)
	await _frames(10)
	await _shot(out, "mission_1_general_end")
	# The pages after the mission go on by themselves: the exp, the exp for time, then the
	# general's talk.
	for page in [
		[11, "mission_1_total_exp"], [12, "mission_1_time_exp"], [0, "mission_1_victory_talk"]
	]:
		while sim.banner != page[0] and not sim.finished:
			await _frames(1)
		await _seconds(1.0)
		await _shot(out, page[1])
	get_tree().quit()


func _release_all() -> void:
	for a in DIR_ACTIONS.values():
		_release(a)
	_release("attack")


## One step of a simple fighter: towards the nearest soldier that is in the room, strike when close.
func _fight_step(sim: RefCounted) -> void:
	var best: Variant = null
	var best_d := 1 << 30
	for e in sim.enemies:
		var d: int = MapGeometry.distance(e.pos, sim.hero.pos)
		if e.alerted != 0 and e.hp > 0 and d < best_d:
			best = e
			best_d = d
	_release_all()
	if best != null:
		if best_d <= 40:
			_press("attack")
		else:
			_press(DIR_ACTIONS[MapGeometry.dir4(sim.hero.pos, best.pos)])
	await _frames(4)
	_release("attack")
	await _frames(4)


## A key pressed as the player presses it: an input event, which the screens read too.
func _press(action: String) -> void:
	_send(action, true)


func _release(action: String) -> void:
	_send(action, false)


func _send(action: String, pressed: bool) -> void:
	var ev := InputEventAction.new()
	ev.action = action
	ev.pressed = pressed
	Input.parse_input_event(ev)


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
