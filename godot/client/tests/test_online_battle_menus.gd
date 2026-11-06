extends "res://tests/test_case.gd"
## Multiplayer > Duel and Mission (scripts/screens/online_battles_screen.gd), the Challenge and
## Invite An Ally lines, the Order's members, invitations, and the rewards of a battle going to
## the hero, against the server's online game (server/online.gd) in this process.

const OnlineBattle := preload("res://scripts/net/online_battle.gd")
const OnlineClient := preload("res://scripts/net/online_client.gd")
const Profile := preload("res://scripts/core/profile.gd")
const ClientTests := preload("res://tests/test_online_client.gd")
const OnlineTests := preload("res://tests/test_online_server.gd")
const ServerTests := preload("res://tests/test_server.gd")
const BattlesScreen := preload("res://scripts/screens/online_battles_screen.gd")
const TextScreen := preload("res://scripts/screens/online_text_screen.gd")
const OrderScreen := preload("res://scripts/screens/online_order_screen.gd")
const BattleScreen := preload("res://scripts/screens/online_battle_screen.gd")


func _dir() -> String:
	var d := "user://test_server_online_menus_%d" % randi()
	DirAccess.make_dir_recursive_absolute(d)
	return d


func _screen(script: GDScript, params: Dictionary) -> Control:
	Router.params = params
	var screen: Control = script.new()
	root.add_child(screen)
	return screen


## A player online whose battles are counted as they start.
func _player(net: RefCounted, uid: String, started: Array) -> RefCounted:
	var c: RefCounted = net.client(uid, OnlineTests.HERO)
	c.enter(func(_e): pass)
	c.on_battle = func() -> void: started.append(uid)
	return c


func test_duel_waits_for_an_opponent() -> void:
	var d := _dir()
	var net = ClientTests.Net.new(d)
	var started: Array = []
	var a: RefCounted = _player(net, "ANDREY", started)
	var m: RefCounted = _player(net, "MARIA", started)
	var old: Dictionary = Router.params
	var menu := _screen(BattlesScreen, {"online": a, "kind": "duel"})
	eq(menu.buttons.map(func(b): return b.text), ["online.duel_1on1", "online.duel_2on2",
		"online.challenge_1", "online.challenge_2", "online.duel_order"])
	menu.buttons[0].pressed.emit()
	check(a.waiting and menu.cancel.visible and menu.buttons[1].disabled, "searching")
	eq(menu.status.text, tr("online.searching"))
	menu.cancel.pressed.emit()
	check(not a.waiting and not menu.cancel.visible and not net.o.queue.has(net.session(a)), "cancelled")
	menu.buttons[0].pressed.emit()
	m.find_battle(0, func(_e): pass)
	eq(started, ["ANDREY", "MARIA"], "matched: both battles start")
	eq([a.battle.mode, a.battle.fighters[1].name, m.battle.fighters[1].name, a.waiting], [0, "MARIA", "ANDREY", false])
	menu.free()
	menu = _screen(BattlesScreen, {"online": a, "kind": "mission"})
	eq(menu.buttons.map(func(b): return str(b.name)), ["Solo", "Ally", "Order"])
	Router.params = old
	menu.free()
	ServerTests._rm(d)


func test_a_duel_waited_long_gets_the_cpu() -> void:
	var d := _dir()
	var net = ClientTests.Net.new(d)
	var started: Array = []
	var a: RefCounted = _player(net, "ANDREY", started)
	a.find_battle(1, func(_e): pass)
	check(a.waiting and started.is_empty())
	net.now += net.o.match_wait
	net.o.tick()
	net.flush()
	eq([started, a.battle.mode, a.battle.allies_alive, a.battle.enemies_alive], [["ANDREY"], 1, 2, 2])
	ServerTests._rm(d)


func test_challenges_and_invitations() -> void:
	var d := _dir()
	var net = ClientTests.Net.new(d)
	net.o.match_wait = 0
	var started: Array = []
	var a: RefCounted = _player(net, "ANDREY", started)
	var m: RefCounted = _player(net, "MARIA", started)
	var old: Dictionary = Router.params
	var text := _screen(TextScreen, {"online": a, "kind": "challenge1"})
	text.fields[0].text = "andrey"
	text._keep(text.fields[0], text.fields[0].text)
	text.submit()
	eq(text.info.text, tr("online.err_self_invite"))
	text.fields[0].text = "NOBODY"
	text.submit()
	eq(text.info.text, tr("online.err_no_player"))
	text.fields[0].text = "BLADE"
	text.submit()
	eq([started, a.battle.mode, a.battle.via, a.battle.fighters[1].name], [["ANDREY"], 0, "invite", "Blade"],
		"a bot takes the challenge")
	text.free()
	a.battle_request({"t": "mp_exit"})  # Exit Battle
	a.battle_over()
	net.o.online_part("MARIA").invitation = 0
	text = _screen(TextScreen, {"online": a, "kind": "ally"})
	text.fields[0].text = "MARIA"
	text.submit()
	eq(text.info.text, tr("online.err_denied"), "Maria denies invitations")
	net.o.online_part("MARIA").invitation = 1
	text.submit()
	eq(started, ["ANDREY", "ANDREY", "MARIA"], "Maria is taken into the mission")
	eq([m.battle.mode, m.battle.my_slot, m.battle.fighters[0].name, a.battle.fighters[1].name],
		[2, 2, "MARIA", "MARIA"], "her own battle: her place first")
	text.free()
	Router.params = old
	ServerTests._rm(d)


func test_order_members_into_a_battle() -> void:
	var d := _dir()
	var net = ClientTests.Net.new(d)
	var started: Array = []
	var a: RefCounted = _player(net, "ANDREY", started)
	var m: RefCounted = _player(net, "MARIA", started)
	a.order_create("WOLVES", func(_e): pass)
	m.order_join("WOLVES", func(_e): pass)
	var old: Dictionary = Router.params
	var order := _screen(OrderScreen, {"online": a, "pick": OnlineClient.TOGETHER})
	eq(order.info.text, tr("online.pick_together"))
	var buttons: Array = order.list.get_children()
	eq(buttons.map(func(b): return b.disabled), [true, false], "not me")
	buttons[1].pressed.emit()
	eq(started, ["ANDREY", "MARIA"], "2-on-2 Together")
	eq([a.battle.mode, a.battle.fighters[1].slot, m.battle.my_slot, a.battle.allies_alive], [1, 2, 2, 2],
		"side by side")
	order.free()
	Router.params = old
	ServerTests._rm(d)


func test_the_rewards_go_to_the_hero() -> void:
	var d := _dir()
	var net = ClientTests.Net.new(d)
	var started: Array = []
	var a: RefCounted = _player(net, "ANDREY", started)
	a.find_battle(2, func(_e): pass)
	var hero := d.path_join("hero.json")
	var p: RefCounted = Profile.new()
	p.gold = 100
	p.save(hero)
	var old: Dictionary = Router.params
	var screen := _screen(BattleScreen, {"online": a, "profile_path": hero})
	var b: RefCounted = a.battle
	b.on_push({"t": "battle_end", "win": 1, "gold": 450, "grade": 5, "fame": 30, "exp": 400, "rank": 2,
		"loot": {"id": 3, "attack": 0, "defense": 0, "hp": 0, "mp": 0, "enchant": 0, "name": "Potion"}})
	screen._process(OnlineBattle.TICK_MS / 1000.0)
	p = Profile.load_or_new(hero)
	eq([p.gold, p.fame, p.level > 1, p.quick_slots[0]], [550, 30, true, [3, 1]], "gold, fame, exp, the potion")
	check(screen.result_text().contains(tr("online.battle_level_up") % screen.levels_gained), screen.result_text())
	screen._process(OnlineBattle.TICK_MS / 1000.0)
	eq(Profile.load_or_new(hero).gold, 550, "once")
	screen.free()
	ServerTests._rm(d)
	d = _dir()
	net = ClientTests.Net.new(d)
	a = _player(net, "ANDREY", started)
	a.find_battle(2, func(_e): pass)
	hero = d.path_join("hero.json")
	p = Profile.new()
	for i in p.backpack.size():
		p.backpack[i] = {"id": 105, "attack": 0, "defense": 0, "hp": 0, "mp": 0, "enchant": 0}
	p.save(hero)
	screen = _screen(BattleScreen, {"online": a, "profile_path": hero})
	a.battle.on_push({"t": "battle_end", "win": 1, "gold": 0, "grade": 0, "fame": 0, "exp": 0, "rank": 1,
		"loot": {"id": 120, "attack": 9, "defense": 0, "hp": 0, "mp": 0, "enchant": 0, "name": "Blade"}})
	screen._process(OnlineBattle.TICK_MS / 1000.0)
	check(screen.loot_lost and screen.result_text().contains(tr("online.battle_bag_full")), "no room")
	screen.free()
	Router.params = old
	ServerTests._rm(d)
