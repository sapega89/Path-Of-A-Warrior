extends Node
## Screenshots of the real game, for review (needs a display, not --headless):
##   godot --path godot/client --resolution 1280x720 res://tools/shots.tscn -- OUT_DIR
## Opens the main scene, walks through the screens and some maps, saves PNGs to OUT_DIR.

const MAPS: Array[int] = [1, 5, 10, 20, 30, 40]
## The multiplayer shots' hero, as the server keeps it (Profile.to_dict()).
const ONLINE_HERO := {
	"level": 12,
	"head": 2,
	"base": [60, 31, 9, 8],
	"equipped":
	[
		{"id": 105, "attack": 6, "defense": 0, "hp": 0, "mp": 0, "enchant": 0},
		{"id": 201, "attack": 0, "defense": 3, "hp": 5, "mp": 2, "enchant": 0}
	],
	"skill_levels": [2, 0, 0, 1, 0, 3],
	"hotkeys": [17, 15, 12, 0, 0]
}


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
	# Always online: no server there, then the login (scripts/net/cloud.gd).
	var cloud: Node = get_node("/root/Cloud")
	cloud.account_path = "user://shot_account.cfg"
	cloud.start("127.0.0.1", 28397, X509Certificate.new())
	Router.go("main_menu")
	await _frames(3)
	await _shot(out, "10b_no_connection")
	Router.go("login")
	await _frames(2)
	Router.current.user_id.grab_focus()  # the line of hints says what the field takes
	await _shot(out, "10c_login_typing")
	Router.current.user_id.text = "ANDREY"
	Router.current.password.text = "12"
	Router.current.submit()
	await _shot(out, "10c_register")
	cloud.stop()
	# The Live pages: the Warehouse (two things moved there), the Safe; the server's Live runs
	# in this process (server/live.gd), the hero is a copy.
	_rm_dir("user://shot_live")
	var market: RefCounted = LiveServer.new("user://shot_live")
	market.rng.seed = 7
	var session: RefCounted = LiveServer.Session.new()
	session.user = "ANDREY"
	var client: RefCounted = LiveClient.new(
		func(msg: Dictionary, done: Callable) -> void:
			done.call(bytes_to_var(var_to_bytes(market.answer(session, str(msg.t), msg))))
	)
	hero.gold = 5000
	hero.save("user://shot_live_hero.json")
	hero.gold = 1250
	var live_params := {"profile_path": "user://shot_live_hero.json", "live": client}
	Router.go("main_menu")
	Router.push("game_menu", live_params)
	Router.push("live_warehouse", live_params)
	await _frames(2)
	Router.current.cells[2].grab_focus()
	await _shot(out, "10e_live_backpack")
	Router.current.press_cell(0)
	Router.current.press_cell(1)
	Router.current.show_side(true)
	await _frames(2)
	Router.current.cells[1].grab_focus()
	await _shot(out, "10f_live_warehouse")
	Router.back()
	Router.push("live_safe", live_params)
	await _frames(2)
	Router.current.turn()
	Router.current.amount.text = "500"
	Router.current.submit()
	Router.current.amount.text = "250"
	await _shot(out, "10g_live_safe")
	# Trade: Buy (kinds of Normal Items, the enchant levels, a page of lots, "Buy for?"), Sell
	# (the price, Price Info), Cancel Sale with the lot just put on sale.
	Router.back()
	Router.push("live_trade", live_params)
	await _shot(out, "10h_live_trade")
	Router.push("live_buy", live_params)
	await _frames(2)
	Router.current.choose_category(0)
	await _frames(2)
	Router.current.cells[2].grab_focus()
	await _shot(out, "10i_live_buy_kinds")
	Router.current.choose_kind(2)
	await _shot(out, "10j_live_buy_enchant")
	Router.current.choose_enchant(0)
	await _frames(2)
	Router.current.cells[1].grab_focus()
	await _shot(out, "10k_live_buy_lots")
	Router.current.press_lot(1)
	await _shot(out, "10l_live_buy_ask")
	Router.current.ask.hide()
	Router.back()
	Router.push("live_sell", live_params)
	await _frames(2)
	Router.current.pick(2)  # the first two things are in the Warehouse now
	Router.current.price.text = "1500"
	await _shot(out, "10m_live_sell_price")
	Router.current.price_info()
	await _frames(2)
	await _shot(out, "10n_live_price_info")
	Router.current.go_back()
	Router.current.put_on_sale()
	Router.back()
	Router.push("live_cancel", live_params)
	await _frames(2)
	await _shot(out, "10o_live_cancel")
	# Opening the game menu with something new on Live: a notice, the Sale List, the note that
	# gifts came, the Exp and Fame kept there; then the Gift List in Trade.
	market.notices = [["Welcome to Live!", "Sell what you", "do not need."]]
	var on_server: Dictionary = market.user("ANDREY")
	on_server.sold.append({"item": items.make(146), "price": 1800})
	on_server.sold.append({"item": items.make(161), "price": 950})
	market.give_gift("ANDREY", "MARIA", items.make(503))
	on_server.fame = 12
	on_server.exp = 300
	client.notices_seen = false
	Router.go("main_menu")
	Router.push("game_menu", live_params)
	await _frames(2)
	var news: Control = Router.current.news
	await _shot(out, "10p_live_notice")
	news.note.hide()
	news.note.confirmed.emit()
	await _frames(2)
	await _shot(out, "10q_live_sale_list")
	news.list_done()
	await _frames(2)
	await _shot(out, "10r_live_gifts_came")
	news.note.hide()
	news.note.confirmed.emit()
	await _frames(2)
	await _shot(out, "10s_live_fame")
	news.note.hide()
	news.note.confirmed.emit()
	Router.push("live_gifts", live_params)
	await _frames(2)
	await _shot(out, "10t_live_gift_list")
	# Give a Gift: the first thing that can be given, MARIA typed in, then "Give ... to MARIA?".
	Router.back()
	Router.push("live_give", live_params)
	await _frames(2)
	for i in LiveClient.WAREHOUSE:
		if Router.current.pick(i):
			break
	Router.current.to.text = "MARIA"
	await _frames(2)
	await _shot(out, "10u_live_give")
	Router.current.ask_give()
	await _frames(2)
	await _shot(out, "10v_live_give_ask")
	Router.current.ask.hide()
	# Multiplayer: the menu, the Character pages, Skills, Ranking, the Order, the Chat and the
	# Options. The server's online game runs in this process (server/online.gd) with its bots;
	# Maria is in my order and wrote while I was away.
	_rm_dir("user://shot_online")
	var accounts: RefCounted = Accounts.new("user://shot_online/accounts")
	accounts.rounds = 20
	var game: RefCounted = OnlineServer.new("user://shot_online", accounts)
	game.rng.seed = 7
	var now := [100.0]
	game.clock = func() -> float: return now[0]
	game.add_bots()
	accounts.create_account("ANDREY", "1234")
	accounts.hero_put("ANDREY", 0, 1, ONLINE_HERO)
	accounts.create_account("MARIA", "1234")
	var me_part: Dictionary = game.online_part("ANDREY")
	me_part.merge(
		{
			"name": "Andrey",
			"wins": 7,
			"losses": 3,
			"mp_fame": 320,
			"duel_grade": 5,
			"mission_grade": 3,
			"gold": 1800,
			"mp_exp": 950
		},
		true
	)
	game.save_char("ANDREY")
	var mine: RefCounted = OnlineServer.Session.new()
	var pushes: Array = []
	mine.send = func(m: Dictionary) -> void: pushes.append(bytes_to_var(var_to_bytes(m)))
	var maria: RefCounted = OnlineServer.Session.new()
	maria.send = func(_m: Dictionary) -> void: pass
	game.enter(mine, "ANDREY")
	game.answer(mine, "order_create", {"name": "WOLVES"})
	game.leave(mine)
	game.enter(maria, "MARIA")
	game.answer(maria, "mp_name", {"name": "Maria"})
	game.answer(maria, "order_join", {"name": "WOLVES"})
	for m in [
		[OnlineServer.LOBBY, "", "Anyone up for a duel?"],
		[OnlineServer.ORDER, "", "Wolves, meet at the arena!"],
		[OnlineServer.PRIVATE, "ANDREY", "Want to do a mission together?"]
	]:
		now[0] += 2.0
		game.answer(maria, "chat_send", {"channel": m[0], "peer": m[1], "text": m[2]})
	pushes.clear()
	var holder: Array = []  # the client, for its own request's pushes
	var mp: RefCounted = OnlineClient.new(
		func(msg: Dictionary, done: Callable) -> void:
			now[0] += 2.0
			var r: Dictionary = (
				game.enter(mine, "ANDREY")
				if msg.t == "mp_enter"
				else game.answer(mine, str(msg.t), bytes_to_var(var_to_bytes(msg)))
			)
			done.call(bytes_to_var(var_to_bytes(r)))
			while not pushes.is_empty():
				holder[0].on_push(pushes.pop_front())
	)
	holder.append(mp)
	var mp_params := {"online": mp}
	Router.go("main_menu")
	Router.push("game_menu", live_params.merged(mp_params))
	await _frames(2)
	await _shot(out, "11a_game_menu")
	Router.current.buttons[-1].grab_focus()  # Help, at the end: the list scrolls down
	await _frames(3)
	await _shot(out, "11a_game_menu_end")
	Router.push("online_character", mp_params)
	await _frames(2)
	Router.current.open("records")
	await _frames(2)
	await _shot(out, "11b_online_records")
	Router.current.open("attributes")
	Router.current.buttons[1].grab_focus()
	await _frames(2)
	await _shot(out, "11c_online_attributes")
	Router.push("online_skills", mp_params)
	await _frames(2)
	await _shot(out, "11d_online_skills")
	Router.back()
	Router.back()
	Router.push("online_ranking", mp_params)
	await _frames(2)
	Router.current.choose(1, true)
	await _frames(2)
	await _shot(out, "11e_online_ranking")
	Router.back()
	Router.push("online_order", mp_params)
	await _frames(2)
	await _shot(out, "11f_online_order")
	Router.back()
	Router.push("online_chat", mp_params)
	await _frames(2)
	Router.current.line.text = "Me! Level 12 here."
	Router.current.submit()
	await _frames(2)
	await _shot(out, "11g_online_chat_lobby")
	mp.send_chat(OnlineClient.PRIVATE, "RAVEN", "Hello Raven!", func(_e: String) -> void: pass)
	Router.current.open(OnlineClient.PRIVATE, "")
	await _frames(2)
	await _shot(out, "11h_online_chat_private")
	Router.push("online_chat", {"online": mp, "channel": OnlineClient.PRIVATE, "peer": "MARIA"})
	await _frames(2)
	Router.current.line.text = "Sure, after my duel."
	await _shot(out, "11i_online_chat_with")
	Router.back()
	Router.back()
	Router.push("online_text", {"online": mp, "kind": "quote"})
	await _frames(2)
	await _shot(out, "11j_online_quote")
	Router.back()
	Router.push("online_options", mp_params)
	await _frames(2)
	await _shot(out, "11k_online_options")
	Router.back()
	# Duel and Mission: the menu, searching for an opponent, a Challenge, the order's members.
	var duel := {"online": mp, "kind": "duel"}
	Router.push("online_battles", duel)
	await _frames(2)
	await _shot(out, "11l_online_duel")
	Router.current.buttons[0].pressed.emit()
	await _frames(2)
	await _shot(out, "11m_online_searching")
	Router.current.cancel.pressed.emit()
	Router.push("online_text", {"online": mp, "kind": "challenge1"})
	await _frames(2)
	Router.current.fields[0].text = "RAVEN"
	await _shot(out, "11n_online_challenge")
	Router.back()
	Router.push("online_order", {"online": mp, "pick": OnlineClient.TOGETHER})
	await _frames(2)
	await _shot(out, "11o_online_order_pick")
	Router.back()
	Router.back()
	if OnlineSection.BATTLES:  # the Duel topic of the one help, while the battles are shown
		Router.push("help")
		await _frames(2)
		Router.current.open(Router.current.topics.size() - 2)
		await _shot(out, "11p_online_help")
		Router.back()
	await _battle_shots(out, game, mp)
	mp.leave()
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
	Router.current.set_process(false)
	Router.current.press()
	Router.current.next_line()
	Router.current.press()
	await _shot(out, "04d_briefing")
	# The camps between missions: a stop with a way per mission (one place closed) and its
	# pause menu, six ways, the main camp at the start, its auctioneer and all of it from above,
	# and the town hall that every camp has.
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
	var camp: Node = Router.current  # the hero by the auctioneer's stall, then the whole camp
	camp.hero.global_position = camp.spot_of("auction").at
	camp.camera.snap()
	await _shot(out, "04i_camp_auction")
	camp.camera.distance = 42.0
	camp.camera.snap()
	await _shot(out, "04j_camp_overview")
	Router.go("town_hall", {"profile_path": "user://shot_walker.json"})
	await _shot(out, "04h_town_hall")
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


const DIR_ACTIONS := {0: "move_down", 2: "move_left", 4: "move_up", 6: "move_right"}


## The multiplayer battles against the server's CPU fighters: a duel from the quotes to the
## result; a 2-on-2 (Exit Battle?, choosing the target, a blow); a Solo Mission (the stage, a
## blow at a monster).
func _battle_shots(out: String, game: RefCounted, mp: RefCounted) -> void:
	game.match_wait = 0
	var params := {"online": mp, "profile_path": "user://shot_online/hero.json"}
	mp.on_battle = func() -> void: Router.push("online_battle", params)
	Router.push("online_battles", {"online": mp, "kind": "duel"})
	Router.current.buttons[0].pressed.emit()  # 1-on-1 Duel
	var screen: Node = Router.current
	screen.set_process(false)
	await _battle_until(
		screen,
		func(b: RefCounted) -> bool: return b.state == OnlineBattle.QUOTES and b.state_ticks >= 8
	)
	await _shot(out, "12a_battle_quotes")
	await _battle_until(
		screen,
		func(b: RefCounted) -> bool: return b.state == OnlineBattle.CHOOSE and b.state_ticks == 3
	)
	await _shot(out, "12b_battle_choose")
	await _battle_until(
		screen,
		func(b: RefCounted) -> bool: return b.state == OnlineBattle.BAR and b.state_ticks == 5
	)
	await _shot(out, "12c_battle_bar")
	await _battle_until(screen, _blow_shown)
	await _shot(out, "12d_battle_blow")
	await _battle_until(screen, func(_b: RefCounted) -> bool: return false)
	await _shot(out, "12e_battle_result")
	await _battle_leave(screen)
	Router.current.buttons[1].pressed.emit()  # 2-on-2 Duel
	screen = Router.current
	screen.set_process(false)
	await _battle_until(
		screen,
		func(b: RefCounted) -> bool: return b.state == OnlineBattle.CHOOSE and b.state_ticks == 3
	)
	screen.press("back")
	await _shot(out, "12f_battle_exit")
	screen.press("fire")  # No
	await _battle_until(
		screen,
		func(b: RefCounted) -> bool:
			return b.state == OnlineBattle.TARGET and b.state_ticks >= 4 and b.state_ticks % 2 == 0
	)
	screen.press("down")
	await _shot(out, "12g_battle_2v2_target")
	InputSetup.device = "pad"  # the hint names the pad's buttons after a pad button
	screen._refresh()
	await _shot(out, "12g_battle_2v2_target_pad")
	InputSetup.device = "keys"
	screen._refresh()
	await _battle_until(screen, _blow_shown)
	await _shot(out, "12h_battle_2v2_blow")
	await _battle_leave(screen)
	Router.back()
	Router.push("online_battles", {"online": mp, "kind": "mission"})
	Router.current.buttons[0].pressed.emit()  # Solo Mission
	screen = Router.current
	screen.set_process(false)
	await _battle_until(
		screen,
		func(b: RefCounted) -> bool:
			return b.state == OnlineBattle.STAGE_INTRO and b.state_ticks >= 4
	)
	await _shot(out, "12i_mission_stage")
	await _battle_until(screen, _blow_shown)
	await _shot(out, "12j_mission_blow")
	await _battle_leave(screen)
	Router.back()
	mp.on_battle = Callable()


## A blow's change of HP shown over a fighter.
func _blow_shown(b: RefCounted) -> bool:
	return b.state == OnlineBattle.TURN and b.damage_shown.size() > 0 and b.damage_tick == 2


## Plays the battle shown on screen step by step as a player would (Attack, the bar stopped
## near the mark, the first foe) until done(battle) holds after a step, or the result shows.
func _battle_until(screen: Node, done: Callable, limit := 5000) -> void:
	var b: RefCounted = screen.battle
	for i in limit:
		b.tick()
		if done.call(b) or (b.state == OnlineBattle.RESULT and b.result_shown()):
			break
		match b.state:
			OnlineBattle.CHOOSE:
				if not b.exit_prompt and b.state_ticks >= 3:
					b.key("right")
			OnlineBattle.TARGET:
				if b.state_ticks >= 5:
					b.key("fire")
			OnlineBattle.BAR:
				if b.state_ticks == 6:
					b.key("fire")
	screen._refresh()
	await _frames(2)


## Out of the battle: OK on the result, or Exit Battle when it goes on.
func _battle_leave(screen: Node) -> void:
	await _battle_until(
		screen,
		func(b: RefCounted) -> bool:
			return b.state == OnlineBattle.CHOOSE and b.state_ticks == 3 and not b.exit_asked
	)
	if screen.battle.state == OnlineBattle.CHOOSE:
		screen.press("back")
		screen.press("left")
	screen.press("fire")
	await _frames(2)


func _release_all() -> void:
	for a in DIR_ACTIONS.values():
		Input.action_release(a)
	Input.action_release("attack")


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
			Input.action_press("attack")
		else:
			Input.action_press(DIR_ACTIONS[MapGeometry.dir4(sim.hero.pos, best.pos)])
	await _frames(4)
	Input.action_release("attack")
	await _frames(4)


## Empties a folder of the shots' own data and the folders in it (only user://shot_*).
func _rm_dir(d: String) -> void:
	if not d.begins_with("user://shot_") or not DirAccess.dir_exists_absolute(d):
		return
	for sub in DirAccess.get_directories_at(d):
		_rm_dir(d.path_join(sub))
	for f in DirAccess.get_files_at(d):
		DirAccess.remove_absolute(d.path_join(f))


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
