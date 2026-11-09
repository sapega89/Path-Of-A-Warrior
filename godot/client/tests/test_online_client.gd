extends "res://tests/test_case.gd"
## The online game on this device (scripts/net/online_client.gd) and the Multiplayer screens,
## against the server's online game (server/online.gd) in this process.

const OnlineClient := preload("res://scripts/net/online_client.gd")
const Online := preload("res://server/online.gd")
const Accounts := preload("res://server/accounts.gd")
const ServerTests := preload("res://tests/test_server.gd")
const OnlineTests := preload("res://tests/test_online_server.gd")
const OnlineSection := preload("res://scripts/ui/online_section.gd")
const CharacterScreen := preload("res://scripts/screens/online_character_screen.gd")
const TextScreen := preload("res://scripts/screens/online_text_screen.gd")
const SkillsScreen := preload("res://scripts/screens/online_skills_screen.gd")
const RankingScreen := preload("res://scripts/screens/online_ranking_screen.gd")
const OrderScreen := preload("res://scripts/screens/online_order_screen.gd")
const ChatScreen := preload("res://scripts/screens/online_chat_screen.gd")
const OptionsScreen := preload("res://scripts/screens/online_options_screen.gd")


## The server's online game and its players' clients, answered at once: every request and
## push goes through var_to_bytes as over the wire, the pushes after the answer. Each request
## comes 2 s after the last (the chat lets one message through in 1.5 s).
class Net:
	var o: Online
	var players: Array = []  # [session, client, pushes waiting]
	var now := 100.0

	func _init(dir: String) -> void:
		var a := Accounts.new(dir.path_join("accounts"))
		a.rounds = 20
		o = Online.new(dir, a)
		o.rng.seed = 3
		o.clock = func() -> float: return now
		o.add_bots()

	func client(uid: String, hero := {}) -> OnlineClient:
		if not o.accounts.has_account(uid):
			o.accounts.create_account(uid, "1234")
		if not hero.is_empty():
			o.accounts.hero_put(uid, int(o.accounts.hero_get(uid).rev), 1, hero)
		var s := Online.Session.new()
		var box: Array = []
		s.send = func(m: Dictionary) -> void: box.append(bytes_to_var(var_to_bytes(m)))
		var entry: Array = [s, null, box]
		var c := OnlineClient.new(
			func(msg: Dictionary, done: Callable) -> void:
				var m: Dictionary = bytes_to_var(var_to_bytes(msg))
				now += 2.0
				var r: Dictionary = (
					o.enter(s, uid) if m.t == "mp_enter" else o.answer(s, str(m.t), m)
				)
				done.call(bytes_to_var(var_to_bytes(r)))
				flush()
		)
		entry[1] = c
		players.append(entry)
		return c

	func flush() -> void:
		for e in players:
			while not e[2].is_empty():
				e[1].on_push(e[2].pop_front())

	func session(c: OnlineClient) -> Online.Session:
		for e in players:
			if e[1] == c:
				return e[0]
		return null


func _dir() -> String:
	var d := "user://test_server_online_client_%d" % randi()
	DirAccess.make_dir_recursive_absolute(d)
	return d


func _screen(script: GDScript, params: Dictionary) -> Control:
	Router.params = params
	var screen: Control = script.new()
	root.add_child(screen)
	return screen


func test_enter_the_character_and_leave() -> void:
	var d := _dir()
	var net := Net.new(d)
	var c := net.client("ANDREY", OnlineTests.HERO)
	var got := []
	c.enter(func(e): got.append(e))
	eq(got, [""])
	check(c.entered and net.o.is_online("ANDREY"), "online")
	eq([c.me.id, c.me.name, int(c.me.level), c.unread], ["ANDREY", "ANDREY", 12, [0, 0]])
	c.ask_records(func(e): got.append(e))
	eq([got[-1], int(c.records.fame)], ["", 0])
	net.o.leave(net.session(c))  # the server forgot him (the connection came back)
	c.ask_attributes(func(e): got.append(e))
	eq([got[-1], int(c.attributes.atk_bonus)], ["", 6], "entered again and asked once more")
	check(net.o.is_online("ANDREY"))
	c.leave()
	check(not c.entered and not net.o.is_online("ANDREY"), "off the online game")
	ServerTests._rm(d)


func test_pushed_chat_counts_as_waiting() -> void:
	var d := _dir()
	var net := Net.new(d)
	var a := net.client("ANDREY")
	var b := net.client("MARIA")
	a.enter(func(_e): pass)
	b.enter(func(_e): pass)
	b.reading = OnlineClient.key(OnlineClient.LOBBY)
	var got := []
	a.send_chat(OnlineClient.LOBBY, "", "Hello all", func(e): got.append(e))
	eq(got, [""])
	eq(
		b.chat.get("lobby", []).map(func(r): return r.text),
		["Hello all"],
		"pushed to the lobby's readers"
	)
	eq(a.chat.get("lobby", []).size(), 1, "and back to me")
	a.send_chat(OnlineClient.PRIVATE, "MARIA", "psst", func(e): got.append(e))
	eq(got[-1], "")
	eq(b.unread, [0, 1], "a private message waits")
	eq(a.unread, [0, 0], "my own does not")
	b.ask_peers(func(e): got.append(e))
	eq(b.peers, [{"id": "ANDREY", "name": "ANDREY", "unread": 1, "online": 1}])
	b.read_chat(OnlineClient.PRIVATE, "ANDREY", func(e): got.append(e))
	eq([b.unread, b.peer_name, b.chat["pm:ANDREY"][0].text], [[0, 0], "ANDREY", "psst"])
	var kicked := []
	var other := net.client("MARIA")
	b.listen(self, &"_note")
	_notes = kicked
	other.enter(func(_e): pass)
	check(b.kicked and not b.entered, "another device took MARIA online")
	eq(kicked.map(func(m): return m.t), ["kicked"], "the listeners hear it")
	ServerTests._rm(d)


var _notes: Array = []


func _note(m: Dictionary) -> void:
	_notes.append(m)


func test_menu_and_character_pages() -> void:
	var d := _dir()
	var net := Net.new(d)
	var c := net.client("ANDREY", OnlineTests.HERO)
	var old: Dictionary = Router.params
	var menu := OnlineSection.new({"online": c})
	root.add_child(menu)
	eq(menu.status.text, "", "online")
	eq(menu.who.text, tr("online.who") % ["ANDREY", 12, 0, 0])
	check(menu.buttons.all(func(b): return not b.disabled), "all open")
	menu.free()
	menu = OnlineSection.new({})
	root.add_child(menu)
	check(menu.buttons.all(func(b): return b.disabled), "no server: all closed")
	menu.free()
	var page := _screen(CharacterScreen, {"online": c})
	page.open("records")
	check(page.info.text.contains(tr("online.duel_grade") % "D+"), "Records: " + page.info.text)
	page.open("attributes")
	eq(page.info.text.split("\n")[2], "ATK 9 + 6")
	page.open("purse")
	eq(page.info.text.split("\n")[2], tr("online.mp_gold") % 0)
	page.free()
	var text := _screen(TextScreen, {"online": c, "kind": "name"})
	text.fields[0].text = "Andrey"
	text.send()
	eq(
		[str(c.me.name), str(net.o.online_part("ANDREY").name)],
		["Andrey", "Andrey"],
		"the display name"
	)
	text.free()
	text = _screen(TextScreen, {"online": c, "kind": "name"})
	text.fields[0].text = "Blade"
	text.send()
	eq(text.info.text, tr("online.err_name_exists"), "a bot has it")
	text.free()
	text = _screen(TextScreen, {"online": c, "kind": "quote"})
	text.fields[0].text = "Come on!"
	text.fields[1].text = "Next!"
	text.send()
	eq(
		[str(net.o.online_part("ANDREY").quote_start), str(net.o.online_part("ANDREY").quote_win)],
		["Come on!", "Next!"]
	)
	text.free()
	var skills := _screen(SkillsScreen, {"online": c})
	eq(skills.skill_buttons.size(), 3, "Whirlwind Sabre, Healing Herbs, Fury")
	eq(
		skills.slot_buttons.map(func(b): return b.text),
		["1: Fury", "2: Healing Herbs", "3: Whirlwind Sabre", "4: -"]
	)
	skills.press_skill(9)
	skills.press_slot(3)
	eq(c.me.slots, [11, 3, 9, 99], "moved from slot 2 to 4: learned ones first")
	skills.press_slot(0)
	eq(net.o.character("ANDREY").slots, [3, 9, 99, 99], "a slot emptied")
	skills.free()
	Router.params = old
	ServerTests._rm(d)


func test_ranking_order_options() -> void:
	var d := _dir()
	var net := Net.new(d)
	var c := net.client("ANDREY")
	c.enter(func(_e): pass)
	var old: Dictionary = Router.params
	var rank := _screen(RankingScreen, {"online": c})
	eq(
		rank.rows.map(func(l): return l.text),
		["1.  BLADE  900", "2.  RAVEN  600", "3.  TIGER  400"]
	)
	eq(rank.mine.text, tr("online.my_rank") % [6, "0"])
	rank.choose(2, true)
	eq(
		rank.rows.map(func(l): return l.text),
		["4.  SHADOW  C", "5.  IRONFIST  C-", "6.  ANDREY  D+"],
		"my Duel grade, near me"
	)
	rank.free()
	var order := _screen(OrderScreen, {"online": c})
	eq(
		[order.info.text, order.create.visible, order.leave.visible],
		[tr("online.no_order"), true, false]
	)
	order.free()
	var text := _screen(TextScreen, {"online": c, "kind": "order_create"})
	text.fields[0].text = "WO"
	text.submit()
	eq(text.info.text, tr("online.err_not_acceptable"), "4 to 12 letters")
	text.fields[0].text = "WOLVES"
	text.submit()
	text.free()
	order = _screen(OrderScreen, {"online": c})
	eq([order.title.text, order.list.get_child_count(), order.leave.visible], ["WOLVES", 1, true])
	eq(order.list.get_child(0).text, "* ANDREY  Lv1  " + tr("online.online"))
	order.online.order_leave(order.shown)
	eq(net.o.order("WOLVES"), {}, "left: the order is gone")
	order.free()
	var opts := _screen(OptionsScreen, {"online": c})
	eq(opts.info.text, tr("online.invitation_accept"))
	opts.choose(0)
	eq(
		[opts.info.text, int(net.o.online_part("ANDREY").invitation)],
		[tr("online.invitation_deny"), 0]
	)
	opts.free()
	Router.params = old
	ServerTests._rm(d)


func test_chat_screen() -> void:
	var d := _dir()
	var net := Net.new(d)
	var a := net.client("ANDREY")
	var b := net.client("MARIA")
	a.enter(func(_e): pass)
	b.enter(func(_e): pass)
	var old: Dictionary = Router.params
	var chat := _screen(ChatScreen, {"online": a})
	eq([chat.info.text, chat.write.visible], [tr("online.no_messages"), true], "the Lobby")
	chat.line.text = "Hi there"
	chat.submit()
	eq([chat.line.text, chat.lines.get_child_count()], ["", 1], "sent, and pushed back")
	b.send_chat(OnlineClient.PRIVATE, "ANDREY", "hello you", func(_e): pass)
	eq(chat.tabs[2].text, tr("online.private") + " (1)", "a private message waits")
	chat.open(OnlineClient.ORDER, "")
	eq([chat.info.text, chat.write.visible], [tr("online.no_order"), false])
	chat.open(OnlineClient.PRIVATE, "")
	eq(
		chat.lines.get_child(0).text,
		"MARIA (1)  " + tr("online.online"),
		"a conversation with a message waiting"
	)
	chat.free()
	chat = _screen(ChatScreen, {"online": a, "channel": OnlineClient.PRIVATE, "peer": "MARIA"})
	eq(
		[chat.title.text, chat.lines.get_child(0).text],
		[tr("online.with") % "MARIA", "MARIA: hello you"]
	)
	eq(a.unread, [0, 0], "read")
	b.send_chat(OnlineClient.PRIVATE, "ANDREY", "and again", func(_e): pass)
	eq([chat.lines.get_child_count(), a.unread], [2, [0, 0]], "shown at once: not waiting")
	chat.line.text = "ok\\bye"
	chat._keep(chat.line.text)
	eq(chat.line.text, "okbye", "no backslash")
	chat.free()
	Router.params = old
	ServerTests._rm(d)
