extends "res://tests/test_case.gd"
## The online game on the server (server/online.gd), as pyport's pow_server: the character
## made from the hero, Options, the Character pages, the Ranking, the orders, the chat and the
## bots.

const Online := preload("res://server/online.gd")
const Rules := preload("res://server/rules.gd")
const Accounts := preload("res://server/accounts.gd")
const GameServer := preload("res://server/game_server.gd")
const NetClient := preload("res://scripts/net/net_client.gd")
const Protocol := preload("res://scripts/net/protocol.gd")
const ServerTests := preload("res://tests/test_server.gd")

## A level-12 Kharakternyk with a short blade, three skills and all three on his keys.
const HERO := {"level": 12, "head": 2, "base": [60, 31, 9, 8],
	"equipped": [{"id": 105, "attack": 6, "defense": 0, "hp": 0, "mp": 0, "enchant": 0},
		{"id": 201, "attack": 0, "defense": 3, "hp": 5, "mp": 2, "enchant": 0}],
	"skill_levels": [2, 0, 0, 1, 0, 3], "hotkeys": [17, 15, 12, 0, 0],
	"done": {"1:1": true, "1:2": true}}


func _dir() -> String:
	var d := "user://test_server_online_%d" % randi()
	DirAccess.make_dir_recursive_absolute(d)
	return d


func _accounts(d: String) -> Accounts:
	var a := Accounts.new(d.path_join("accounts"))
	a.rounds = 20
	return a


func _online(d: String, a: Accounts) -> Online:
	var o := Online.new(d, a)
	o.rng.seed = 3
	o.clock = func() -> float: return 100.0
	o.add_bots()
	return o


## A session that keeps what is pushed to it.
func _session(pushes: Array) -> Online.Session:
	var s := Online.Session.new()
	s.send = func(m: Dictionary) -> void: pushes.append(m)
	return s


## A player with an account, online.
func _player(o: Online, uid: String, pushes: Array = []) -> Online.Session:
	if not o.accounts.has_account(uid):
		o.accounts.create_account(uid, "1234")
	var s := _session(pushes)
	check(o.enter(s, uid).ok, "%s online" % uid)
	return s


func test_skill_costs_follow_the_single_player_mp() -> void:
	eq(Rules.skill_cost(3, 1, 10), 50, "Whirlwind Sabre Lv1: 5 MP of a new hero's 10")
	eq(Rules.skill_mp(11, 3), 13, "Fury Lv3")
	eq(Rules.skill_cost(11, 3, 33), 40, "13 of 33, rounded up")
	eq(Rules.skill_cost(10, 9, 5), 100, "more than the hero has: a full gauge")
	eq(Rules.skill_cost(3, 1, 0), 100)
	eq(Rules.HERO_BASES[1], [40, 7, 3, 5], "[HP, MP, ATK, DEF] of the Serdiuk")


func test_character_comes_from_the_hero_on_the_server() -> void:
	var d := _dir()
	var a := _accounts(d)
	var o := _online(d, a)
	a.create_account("ANDREY", "1234")
	var p: Dictionary = o.enter(_session([]), "ANDREY")
	eq([p.level, p.face, p.hp, p.weapon, p.slots], [1, 0, 40, 0, [3, 11, 99, 99]],
		"no hero yet: a new Cossack with 5 points and the Iron Broadsword")
	eq(p.skill_cost[0], 50, "Whirlwind Sabre of 10 MP")
	eq(p.unread, [0, 0])
	var c := o.character("ANDREY")
	eq([c.atk, c.atk_bonus, c.def, c.mp, c.skills], [7, 1, 5, 10, {3: 1, 11: 1}])
	a.hero_put("ANDREY", 0, 1, HERO)
	for acc in [a, _accounts(d)]:  # in memory, then read back from the file
		var o2 := Online.new(d, acc)
		c = o2.character("ANDREY")
		eq([c.level, c.face, c.hp, c.hp_bonus, c.mp, c.mp_bonus, c.atk, c.atk_bonus, c.def, c.def_bonus],
			[12, 2, 60, 5, 31, 2, 9, 6, 8, 3], "the hero's stats and his gear's bonuses")
		eq([c.weapon, c.skills, c.slots, c.progress], [1, {3: 2, 9: 1, 11: 3}, [11, 9, 3, 99], 2],
			"a blade, the learned skills, the ones on his keys, two missions won")
		var costs: Array = o2.profile("ANDREY").skill_cost
		eq([costs.size(), costs[0], costs[1], costs[8]], [11, 25, 19, 40], "MP 33: Wind Lv2 8, Storm 6, Soul Lv3 13")
	ServerTests._rm(d)


func test_requests_need_the_multiplayer_menu_open() -> void:
	var d := _dir()
	var srv := GameServer.new()
	srv.accounts = _accounts(d)
	srv.online = _online(d, srv.accounts)
	var s := GameServer.Session.new()
	eq(srv.answer(s, {"t": "mp_enter"}).err, "login first")
	check(srv.answer(s, {"t": "register", "id": "ANDREY", "pwd": "1234", "v": Protocol.VERSION}).ok)
	eq(srv.answer(s, {"t": "mp_profile", "q": 4}), {"t": "mp_profile", "ok": false, "err": "enter first", "q": 4})
	var r := srv.answer(s, {"t": "mp_enter", "q": 5})
	eq([r.ok, r.name, r.q], [true, "ANDREY", 5], "the profile; no display name yet: the UserID")
	check(srv.online.is_online("ANDREY"))
	eq(srv.answer(s, {"t": "mp_nope"}).err, "unknown")
	check(srv.answer(s, {"t": "mp_leave"}).ok)
	check(not srv.online.is_online("ANDREY"), "left the menu")
	eq(srv.answer(s, {"t": "chat_peers"}).err, "enter first")
	ServerTests._rm(d)


func test_another_device_takes_the_player_online() -> void:
	var d := _dir()
	var o := _online(d, _accounts(d))
	var first: Array = []
	var a := _player(o, "ANDREY", first)
	var b := _player(o, "ANDREY")
	eq(first, [{"t": "kicked"}], "the first device is told")
	eq(o.answer(a, "mp_profile", {}).err, "enter first")
	check(o.answer(b, "mp_profile", {}).ok)
	o.leave(a)  # its connection closes later
	check(o.is_online("ANDREY"), "the second one stays")
	ServerTests._rm(d)


func test_options_name_quotes_and_slots() -> void:
	var d := _dir()
	var a := _accounts(d)
	var o := _online(d, a)
	var s := _player(o, "ANDREY")
	a.hero_put("ANDREY", 0, 1, HERO)
	eq(o.answer(s, "mp_options", {}).invitation, 1, "Accept")
	check(o.answer(s, "mp_options_set", {"invitation": 0}).ok)
	eq(o.answer(s, "mp_options_set", {"invitation": 2}).err, "bad message")
	eq(o.answer(s, "mp_name", {"name": "An drey"}).err, "not acceptable")
	eq(o.answer(s, "mp_name", {"name": "Andrey123"}).err, "not acceptable", "8 characters at most")
	eq(o.answer(s, "mp_name", {"name": "bLaDe"}).err, "name exists", "a bot's name, any case")
	check(o.answer(s, "mp_name", {"name": "Andrey"}).ok)
	check(o.answer(s, "mp_quote", {"which": "win", "quote": "Next!"}).ok)
	eq(o.answer(s, "mp_quote", {"which": "start", "quote": "x".repeat(21)}).err, "not acceptable")
	eq(o.answer(s, "mp_slots", {"slots": [9, 4, 99, 99]}).err, "bad message", "Storm is not learned")
	eq(o.answer(s, "mp_slots", {"slots": [9, 9, 99, 99]}).err, "bad message", "twice")
	check(o.answer(s, "mp_slots", {"slots": [99, 9, 99, 3]}).ok)
	eq(o.answer(s, "mp_skills", {}).skills, [{"id": 3, "level": 2}, {"id": 9, "level": 1}, {"id": 11, "level": 3}])
	var at := o.answer(s, "mp_attributes", {})
	eq([at.hp, at.hp_bonus, at.atk, at.atk_bonus], [60, 5, 9, 6])
	var again := Online.new(d, a)  # as after a restart
	var p := again.profile("ANDREY")
	eq([p.name, p.quote_win, p.quote_start, p.slots], ["Andrey", "Next!", "Prepare yourself!", [9, 3, 99, 99]],
		"kept on the server; the slots chosen here, learned ones first")
	eq(int(again.online_part("ANDREY").invitation), 0)
	ServerTests._rm(d)


func test_ranking_records_and_purse() -> void:
	var d := _dir()
	var o := _online(d, _accounts(d))
	var s := _player(o, "ANDREY")
	_player(o, "MARIA")
	var top := o.answer(s, "mp_rank_list", {"cat": 1})
	eq(top.rows.map(func(r): return [r.rank, r.id, r.value]),
		[[1, "BLADE", 900], [2, "RAVEN", 600], [3, "TIGER", 400]], "the bots lead the Fame ranking")
	var near := o.answer(s, "mp_rank_list", {"cat": 1, "near": true})
	eq(near.rows.map(func(r): return r.id), ["IRONFIST", "ANDREY", "MARIA"], "me in the middle")
	var mine := o.answer(s, "mp_rank_mine", {"cat": 2})
	eq([mine.rank, mine.value], [6, 0])
	eq(o.answer(s, "mp_rank_mine", {"cat": 4}).err, "bad message")
	eq(o.answer(s, "mp_records", {}), {"t": "mp_records", "ok": true, "fame": 0, "duel_grade": 0,
		"mission_grade": 0, "order": ""})
	eq(o.answer(s, "mp_purse", {}), {"t": "mp_purse", "ok": true, "exp": 0, "fame": 0, "gold": 0})
	eq(o.table(2)[0].value, 9, "Blade's Duel grade A+")
	check(o.is_online("BLADE"), "bots are always online")
	ServerTests._rm(d)


func test_orders() -> void:
	var d := _dir()
	var o := _online(d, _accounts(d))
	var a := _player(o, "ANDREY")
	var b := _player(o, "MARIA")
	eq(o.answer(a, "order_create", {"name": "WO"}).err, "not acceptable", "4 to 12 letters")
	check(o.answer(a, "order_create", {"name": "wolves"}).ok, "typed in any case")
	eq(o.answer(a, "order_create", {"name": "BEARS"}).err, "in order")
	eq(o.answer(b, "order_create", {"name": "WOLVES"}).err, "name exists")
	eq(o.answer(b, "order_join", {"name": "BEARS"}).err, "none")
	check(o.answer(b, "order_join", {"name": "WOLVES"}).ok)
	o.leave(b)
	var info := o.answer(a, "order_info", {})
	eq(info.name, "WOLVES")
	eq(info.rows.map(func(r): return [r.id, r.leader, r.online]), [["ANDREY", 1, 1], ["MARIA", 0, 0]])
	eq(o.answer(a, "mp_records", {}).order, "WOLVES")
	check(o.same_order("ANDREY", "MARIA"))
	check(o.answer(a, "order_leave", {}).ok)
	eq(o.answer(a, "order_info", {}).name, "", "out of it")
	eq(Online.new(d, o.accounts).order("WOLVES").members, ["MARIA"], "the next member leads")
	b = _player(o, "MARIA")
	o.answer(b, "order_leave", {})
	check(o.order("WOLVES").is_empty(), "the last one out: the order is gone")
	check(o.answer(a, "order_create", {"name": "WOLVES"}).ok, "and its name is free")
	ServerTests._rm(d)


func test_lobby_order_and_private_chat() -> void:
	var d := _dir()
	var o := _online(d, _accounts(d))
	var got_a: Array = []
	var got_b: Array = []
	var a := _player(o, "ANDREY", got_a)
	var b := _player(o, "MARIA", got_b)
	o.answer(b, "mp_name", {"name": "Maria"})
	eq(o.answer(a, "chat_send", {"channel": 0, "text": "  "}).err, "not acceptable")
	eq(o.answer(a, "chat_send", {"channel": 0, "text": "back\\slash"}).err, "not acceptable")
	check(o.answer(a, "chat_send", {"channel": 0, "text": "Hi, SHITty day"}).ok)
	var push := {"t": "chat_push", "channel": 0, "peer": "", "id": "ANDREY", "name": "ANDREY",
		"text": "Hi, ****ty day"}
	eq([got_a, got_b], [[push], [push]], "every reader gets it, the writer too; rude words starred")
	eq(o.answer(a, "chat_send", {"channel": 0, "text": "again"}).err, "too fast", "1 in 1.5 s")
	var now := [100.0]
	o.clock = func() -> float: return now[0]
	for i in 5:
		now[0] += 2.0
		check(o.answer(a, "chat_send", {"channel": 0, "text": "line %d" % i}).ok)
	now[0] += 2.0
	eq(o.answer(a, "chat_send", {"channel": 0, "text": "one more"}).err, "too fast", "6 in 20 s")
	now[0] += 20.0
	var rows: Array = o.answer(b, "chat_read", {"channel": 0}).rows
	eq([rows.size(), rows[0].text, rows[-1].text], [6, "Hi, ****ty day", "line 4"])
	eq(o.answer(a, "chat_send", {"channel": 1, "text": "x"}).err, "no order")
	eq(o.answer(a, "chat_send", {"channel": 2, "peer": "ANDREY", "text": "x"}).err, "self")
	eq(o.answer(a, "chat_send", {"channel": 2, "peer": "NOBODY", "text": "x"}).err, "no player")
	o.leave(b)
	got_a.clear()
	got_b.clear()
	check(o.answer(a, "chat_send", {"channel": 2, "peer": "maria", "text": "where are you?"}).ok)
	eq(got_a.map(func(m): return [m.peer, m.text]), [["MARIA", "where are you?"]], "only me: Maria is away")
	eq(got_b, [])
	b = _player(o, "MARIA", got_b)
	eq(o.enter(b, "MARIA").unread, [0, 1], "a private message waits")
	eq(o.answer(b, "chat_peers", {}).rows, [{"id": "ANDREY", "name": "ANDREY", "unread": 1, "online": 1}])
	var pm := o.answer(b, "chat_read", {"channel": 2, "peer": "ANDREY"})
	eq([pm.peer_name, pm.rows.map(func(r): return r.text)], ["ANDREY", ["where are you?"]])
	eq(o.unread("MARIA"), [0, 0], "read")
	eq(o.answer(a, "chat_read", {"channel": 2, "peer": "MARIA"}).peer_name, "Maria")
	o.answer(a, "order_create", {"name": "WOLVES"})
	o.answer(b, "order_join", {"name": "WOLVES"})
	now[0] += 5.0
	o.answer(a, "chat_send", {"channel": 1, "text": "to the order"})
	eq(o.unread("MARIA"), [1, 0])
	eq(o.unread("ANDREY"), [0, 0], "my own message is read")
	o.answer(b, "chat_read", {"channel": 1})
	eq(o.unread("MARIA"), [0, 0])
	ServerTests._rm(d)


func test_a_bot_answers_a_private_message() -> void:
	var d := _dir()
	var o := _online(d, _accounts(d))
	var got: Array = []
	var a := _player(o, "ANDREY", got)
	check(o.answer(a, "chat_send", {"channel": 2, "peer": "BLADE", "text": "hello"}).ok)
	eq(got.size(), 2, "my message and the answer")
	eq([got[1].id, got[1].name, Online.BOT_LINES.has(got[1].text)], ["BLADE", "Blade", true])
	eq(o.unread("ANDREY"), [0, 1], "the answer waits in Blade's conversation")
	eq(o.accounts.check_password("BLADE", ""), false, "nobody logs in as a bot")
	ServerTests._rm(d)


func test_chat_pushes_over_enet() -> void:
	var d := "user://test_server_online_net_%d" % randi()
	DirAccess.make_dir_recursive_absolute(d)
	var srv := GameServer.new()
	var p := ServerTests.pair(0)
	eq(srv.start(ServerTests.PORT, p[0], p[1], d, "127.0.0.1"), OK)
	srv.accounts.rounds = 20
	var clients: Array[NetClient] = [NetClient.new(), NetClient.new()]
	var got: Array = []
	var pushed: Array = []
	for i in 2:
		var c := clients[i]
		c.on_push = func(m: Dictionary) -> void: pushed.append([i, m])
		eq(c.open("127.0.0.1", ServerTests.PORT, p[1]), OK)
		c.request({"t": "register", "id": ["ANDREY", "MARIA"][i], "pwd": "1234", "v": Protocol.VERSION},
			func(r): got.append(r))
		c.request({"t": "mp_enter"}, func(r): got.append(r))
	var t0 := Time.get_ticks_msec()
	while got.size() < 4 and Time.get_ticks_msec() - t0 < 5000:
		srv.poll(1)
		for c in clients:
			c.poll(1)
	eq(got.map(func(r): return r.ok), [true, true, true, true], "registered and online")
	clients[0].request({"t": "chat_send", "channel": 0, "text": "hello"}, func(r): got.append(r))
	t0 = Time.get_ticks_msec()
	while (got.size() < 5 or pushed.size() < 2) and Time.get_ticks_msec() - t0 < 5000:
		srv.poll(1)
		for c in clients:
			c.poll(1)
	eq(got.size(), 5, "the answer")
	pushed.sort_custom(func(x, y): return x[0] < y[0])
	eq(pushed.map(func(x): return [x[0], x[1].t, x[1].text]), [[0, "chat_push", "hello"], [1, "chat_push", "hello"]],
		"both clients get the message")
	clients[1].close()
	t0 = Time.get_ticks_msec()
	while srv.online.is_online("MARIA") and Time.get_ticks_msec() - t0 < 5000:
		srv.poll(1)
	check(not srv.online.is_online("MARIA"), "offline when the connection closes")
	clients[0].close()
	srv.stop()
	ServerTests._rm(d)
