extends "res://tests/test_case.gd"
## Battles of the online game on the server (server/battle.gd, room.gd, loot.gd and the
## battle requests of online.gd), as pyport's pow_server/battle.py, loot.py and Room.

const Online := preload("res://server/online.gd")
const Battle := preload("res://server/battle.gd")
const Rules := preload("res://server/rules.gd")
const Loot := preload("res://server/loot.gd")
const Accounts := preload("res://server/accounts.gd")
const ServerTests := preload("res://tests/test_server.gd")
const OnlineTests := preload("res://tests/test_online_server.gd")


func _dir() -> String:
	var d := "user://test_server_battle_%d" % randi()
	DirAccess.make_dir_recursive_absolute(d)
	return d


func _online(d: String) -> Online:
	var a := Accounts.new(d.path_join("accounts"))
	a.rounds = 20
	var o := Online.new(d, a)
	o.rng.seed = 11
	o.add_bots()
	return o


## A player online, with what the server pushed to him in .inbox.
class Player:
	var s: Online.Session
	var inbox: Array = []
	var seen: Array = []  # every push, in order


func _player(o: Online, uid: String, hero := {}) -> Player:
	var p := Player.new()
	if not o.accounts.has_account(uid):
		o.accounts.create_account(uid, "1234")
	if not hero.is_empty():
		o.accounts.hero_put(uid, int(o.accounts.hero_get(uid).rev), 1, hero)
	p.s = Online.Session.new()
	var inbox := p.inbox
	p.s.send = func(m: Dictionary) -> void: inbox.append(m)
	check(o.enter(p.s, uid).ok, "%s online" % uid)
	return p


## Plays the pushes as a client that never waits: ready after every result, the bot chooses
## its moves (action AUTO). Stops when nothing is left to answer.
func _play(o: Online, players: Array, limit := 5000) -> void:
	var busy := true
	while busy and limit > 0:
		busy = false
		for p: Player in players:
			if p.inbox.is_empty():
				continue
			busy = true
			limit -= 1
			var m: Dictionary = p.inbox.pop_front()
			p.seen.append(m)
			match m.t:
				"all_ready", "turn_result":
					o.answer(p.s, "mp_ready", {})
				"round_start":
					o.answer(p.s, "mp_turn", {"target": 1, "action": Battle.AUTO, "hit": 88})
				"stage_info":
					o.answer(p.s, "mp_intro_done", {})
				"stage_end":
					o.answer(p.s, "mp_stage_next", {})
	check(limit > 0, "the battle ends")


static func _of(p: Player, t: String) -> Array:
	return p.seen.filter(func(m): return m.t == t)


func _fighter(atk: int, def: int, hp := 100) -> Battle.Fighter:
	var f := Battle.Fighter.new()
	f.atk = atk
	f.def = def
	f.max_hp = hp
	f.hp = hp
	f.skills = {3: 1}
	f.slots = [3]
	return f


func test_single_player_numbers() -> void:
	eq(Rules.hero_stats(10, {"atk": 2, "def": 1, "hp": 2}, 0), {"hp": 100, "mp": 10, "atk": 17, "def": 10})
	eq(Rules.hero_stats(12, {"atk": 4, "def": 4, "hp": 5, "mp": 7}, 2), {"hp": 70, "mp": 61, "atk": 11, "def": 11})
	eq(Rules.soldier_stats(2, 7), {"atk": 15, "def": 6, "hp": 28}, "a squad of level 7")
	eq([Rules.skill_bonus(3, 20, 4), Rules.heal(9, 100, 3), Rules.heal(10, 100, 3)], [4, 28, 60])
	eq(Rules.soul(13, 30, 20, 5), [6, 4, 100], "Protection of the Virgin Lv5")
	eq(Rules.mission_end(45, true, 6), [45, 94, 900])
	eq(Rules.shop_kit(1), {"atk": 1, "def": 0, "hp": 0}, "a new hero's Iron Claymore")
	eq(Rules.shop_kit(10), {"atk": 6, "def": 11, "hp": 60})
	eq(Rules.shop_kit(25), {"atk": 12, "def": 20, "hp": 120})
	eq(Rules.shop_kit(99), {"atk": 27, "def": 44, "hp": 285})


func test_strikes_and_stances() -> void:
	var f := _fighter(20, 0)
	var t := _fighter(0, 5)
	eq([Battle.strike_damage(f, t, Battle.ATTACK, 100), Battle.strike_damage(f, t, Battle.ATTACK, 60),
		Battle.strike_damage(f, t, Battle.ATTACK, 10)], [45, 30, 15], "the bar decides 3, 2 or 1 hits")
	eq(Battle.strike_damage(f, t, Battle.ATTACK, 100, true), 18, "Defend takes 40 %")
	eq(Battle.strike_damage(f, t, Battle.WIND), 48, "Whirlwind Sabre: 3 hits of ATK - DEF + ATK / 20")
	eq(Battle.strike_damage(_fighter(1, 0), _fighter(0, 50), Battle.ATTACK, 0), 1, "at least 1")
	t.slot = 1
	var b := Battle.new(RandomNumberGenerator.new(), [f, t])
	var r := b.resolve({0: [1, Battle.ATTACK, 100], 1: [0, Battle.DEFEND, 0]})
	eq(r.actions, [Battle.ATTACK, Battle.DEFEND, 0, 0])
	eq(r.records.size(), 1, "a stance makes no record")
	var rec: Dictionary = r.records[0]
	eq([rec.actor, rec.target, rec.result, rec.target_hp, rec.actor_mp], [0, 1, Battle.RES_HIT, 82, 20],
		"18 through Defend; +20 MP an Attack")
	eq(t.mp, 25, "+15 a stance, +10 a hit")
	f.mp = 100
	r = b.resolve({0: [1, Battle.WIND, 100], 1: [0, Battle.ATTACK, 100]})
	eq(r.records[0].actor, 0, "more MP acts first")
	eq(r.records[0].actor_mp, 50, "Whirlwind Sabre costs 50 of a 10-MP hero's gauge")
	r = b.resolve({0: [1, Battle.STORM, 100]})
	eq(r.actions[0], Battle.ATTACK, "Storm is not learned: an Attack")
	eq(r.records.filter(func(x): return x.actor == 0)[0].action, Battle.ATTACK)


func test_a_duel_against_the_cpu() -> void:
	var d := _dir()
	var o := _online(d)
	o.match_wait = 0
	var a := _player(o, "ANDREY", OnlineTests.HERO)
	var r := o.answer(a.s, "mp_match", {"mode": 0})
	eq([r.ok, r.waiting], [true, false])
	eq(o.answer(a.s, "mp_match", {"mode": 0}).err, "busy")
	var room: Dictionary = a.inbox[0]
	eq([room.t, room.via, room.slot, room.mode, room.fighters.size()], ["room", "match", 0, 0, 2])
	var foe: Dictionary = room.fighters[1]
	check(foe.cpu and Battle.CPU_NAMES.has(foe.name), "a CPU fighter")
	check(absi(int(foe.level) - 12) <= 2, "of about my level (%d)" % foe.level)
	_play(o, [a])
	var end: Array = _of(a, "battle_end")
	eq(end.size(), 1)
	var c := o.online_part("ANDREY")
	if end.size() == 1:
		var e: Dictionary = end[0]
		eq(int(c.wins) + int(c.losses), 1, "a win or a loss")
		eq(int(c.wins), e.win)
		check(e.rank > 0, "my Duel rank")
		check(e.loot is Dictionary, "loot or {}")
		if e.win:
			eq(e.fame, 2 * int(foe.level), "a fighter beaten is a general: Fame 2 L")
			eq(e.exp, 2 * e.fame)
			eq(int(c.mp_fame), e.fame, "in the purse")
	eq(o.rooms.size(), 0)
	check(a.s.room == null, "out of the room")
	check(_of(a, "turn_result").all(func(m): return m.actions.size() == 4), "four actions a round")
	ServerTests._rm(d)


func test_two_players_meet_in_the_queue() -> void:
	var d := _dir()
	var o := _online(d)
	var now := [0.0]
	o.clock = func() -> float: return now[0]
	var a := _player(o, "ANDREY")
	var b := _player(o, "MARIA")
	eq(o.answer(a.s, "mp_match", {"mode": 0}).waiting, true, "nobody yet")
	eq(o.answer(a.s, "mp_cancel", {}).ok, true)
	eq(o.answer(a.s, "mp_cancel", {}).err, "none")
	o.answer(a.s, "mp_match", {"mode": 0})
	eq(o.answer(b.s, "mp_match", {"mode": 1}).waiting, true, "another kind of duel")
	o.answer(b.s, "mp_cancel", {})
	eq(o.answer(b.s, "mp_match", {"mode": 0}).waiting, false, "found")
	eq([a.inbox[0].via, a.inbox[0].slot, b.inbox[0].slot], ["match", 0, 1], "who waited is on the left")
	eq(a.inbox[0].fighters.map(func(f): return f.name), ["ANDREY", "MARIA"])
	_play(o, [a, b])
	var ends: Array = _of(a, "battle_end") + _of(b, "battle_end")
	eq(ends.size(), 2)
	eq(int(o.online_part("ANDREY").wins) + int(o.online_part("MARIA").wins), 1, "one of them wins")
	check(_of(a, "turn_result").size() == _of(b, "turn_result").size(), "the same rounds for both")
	var c := _player(o, "OLEG")
	o.answer(c.s, "mp_match", {"mode": 1})
	now[0] = 30.0
	o.tick()
	eq(c.inbox.size(), 0, "still waiting")
	now[0] = 60.0
	o.tick()
	eq([c.inbox[0].t, c.inbox[0].fighters.size()], ["room", 4], "a minute: a 2-on-2 against the CPU")
	ServerTests._rm(d)


func test_a_solo_mission() -> void:
	var d := _dir()
	var o := _online(d)
	var hero := OnlineTests.HERO.duplicate(true)
	var done := {}
	for i in 12:  # 12 missions won: 2 + 12 / 6 stages
		done["1:%d" % i] = true
	hero.done = done
	var a := _player(o, "ANDREY", hero)
	check(o.answer(a.s, "mp_match", {"mode": 2}).ok)
	var room: Dictionary = a.inbox[0]
	eq(room.fighters.map(func(f): return f.slot), [0, 2, 1, 3], "me, my CPU ally, two foes")
	check(room.fighters[2].monster, "a monster")
	eq([a.inbox[1].t, a.inbox[1].stages, a.inbox[1].stage], ["stage_info", 4, 1])
	_play(o, [a])
	var end: Array = _of(a, "battle_end")
	eq(end.size(), 1)
	var stages := _of(a, "stage_info").size()
	eq(_of(a, "room_join").size(), 2 * (stages - 1), "two new foes a stage")
	eq(_of(a, "stage_end").size(), stages - 1 if not end.is_empty() and end[0].win else _of(a, "stage_end").size())
	if not end.is_empty() and end[0].win:
		eq(stages, 4)
		check(int(o.online_part("ANDREY").mission_grade) > 0, "a Mission grade")
		eq(end[0].gold, 9 * 150, "h = 3 (stages - 1)")
	eq(int(o.online_part("ANDREY").wins) + int(o.online_part("ANDREY").losses), 0, "no wins or losses")
	ServerTests._rm(d)


func test_invitations() -> void:
	var d := _dir()
	var o := _online(d)
	var a := _player(o, "ANDREY")
	var b := _player(o, "MARIA")
	o.accounts.create_account("OLEG", "1234")
	eq(o.answer(a.s, "mp_invite", {"mode": 0, "id": "ANDREY"}).err, "self")
	eq(o.answer(a.s, "mp_invite", {"mode": 0, "id": "NOBODY"}).err, "no player")
	eq(o.answer(a.s, "mp_invite", {"mode": 0, "id": "OLEG"}).err, "not online")
	eq(o.answer(a.s, "mp_invite", {"mode": 7, "id": "MARIA"}).err, "bad message")
	eq(o.answer(a.s, "mp_invite", {"mode": 3, "id": "MARIA"}).err, "not member", "Invite a member: an order")
	o.answer(b.s, "mp_options_set", {"invitation": 0})
	eq(o.answer(a.s, "mp_invite", {"mode": 0, "id": "MARIA"}).err, "denied")
	o.answer(b.s, "mp_options_set", {"invitation": 1})
	check(o.answer(a.s, "mp_invite", {"mode": 2, "id": "maria"}).ok, "Invite An Ally")
	eq([a.inbox[0].via, b.inbox[0].via, b.inbox[0].slot], ["invite", "invited", 2], "no question: she is in")
	eq(o.answer(a.s, "mp_invite", {"mode": 0, "id": "BLADE"}).err, "busy", "I am in a battle")
	var c := _player(o, "OLEG")
	eq(o.answer(c.s, "mp_invite", {"mode": 0, "id": "MARIA"}).err, "playing")
	check(o.answer(c.s, "mp_invite", {"mode": 1, "id": "BLADE"}).ok, "a bot always accepts")
	var bot: Array = c.inbox[0].fighters.filter(func(f): return f.slot == 1)
	eq([bot[0].name, bot[0].cpu], ["Blade", true], "the bot fights under its name")
	eq(c.inbox[0].fighters.size(), 4)
	_play(o, [a, b, c])
	eq([_of(a, "battle_end").size(), _of(b, "battle_end").size(), _of(c, "battle_end").size()], [1, 1, 1])
	o.answer(a.s, "order_create", {"name": "WOLVES"})
	o.answer(b.s, "order_join", {"name": "WOLVES"})
	a.inbox.clear()
	b.inbox.clear()
	check(o.answer(a.s, "mp_invite", {"mode": 3, "id": "MARIA"}).ok)
	eq([a.inbox[0].mode, b.inbox[0].slot], [1, 2], "side by side in a 2-on-2")
	eq(b.inbox[0].fighters.filter(func(f): return f.cpu).map(func(f): return f.slot), [1, 3])
	ServerTests._rm(d)


func test_leaving_a_duel_loses_it() -> void:
	var d := _dir()
	var o := _online(d)
	var a := _player(o, "ANDREY")
	var b := _player(o, "MARIA")
	o.answer(a.s, "mp_invite", {"mode": 0, "id": "MARIA"})
	check(o.answer(a.s, "mp_exit", {}).ok)
	eq(o.answer(a.s, "mp_ready", {}).err, "no battle")
	eq([int(o.online_part("ANDREY").losses), int(o.online_part("MARIA").wins)], [1, 0])
	b.inbox.clear()
	o.answer(b.s, "mp_ready", {})
	eq(b.inbox.size(), 1)
	if b.inbox.size() == 1:
		eq([b.inbox[0].t, b.inbox[0].win, b.inbox[0].fame], ["battle_end", 1, 2], "won: a level-1 hero beaten")
	eq(int(o.online_part("MARIA").wins), 1)
	eq(o.rooms.size(), 0)
	o.match_wait = 0
	o.answer(a.s, "mp_match", {"mode": 0})
	var again := Online.Session.new()  # the same UserID from another device
	o.enter(again, "ANDREY")
	eq(int(o.online_part("ANDREY").losses), 2, "kicked out of a duel: lost")
	eq(o.rooms.size(), 0)
	o.leave(b.s)
	ServerTests._rm(d)


func test_loot() -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 5
	var got := {}
	for i in 3000:
		var it := Loot.roll(rng, 30, [2, 2])
		if not it.is_empty():
			got[int(it.id)] = it
	check(got.keys().any(func(id): return id <= 11), "potions and bombs")
	check(got.keys().any(func(id): return id > 100 and id <= 200), "Normal gear")
	check(got.keys().any(func(id): return id > 300 and id < 500), "Special things")
	check(not got.has(502), "never the Silk Towel")
	for id in got:
		var it: Dictionary = got[id]
		check(not str(it.name).is_empty(), "%d has a name" % id)
		if id > 100 and id <= 200:
			var rec := Loot.Items.info(id)
			var v: int = it[Loot.Items.GEAR_STATS[int(rec.stat)]]
			check(v >= int(rec.bonus) and v <= int(rec.bonus) + int(rec.range), "%d: base + 0..range" % id)
	eq(Loot.roll(rng, 30, []), {}, "nothing beaten, nothing found")
