extends "res://tests/test_case.gd"
## Always online: the hero kept on the server (scripts/net/cloud_sync.gd, cloud.gd) against a
## real server in this process.

const CloudSync := preload("res://scripts/net/cloud_sync.gd")
const GameServer := preload("res://server/game_server.gd")
const Online := preload("res://server/online.gd")
const Profile := preload("res://scripts/core/profile.gd")
const ServerTests := preload("res://tests/test_server.gd")
const PORT := 28398


func _dir() -> String:
	var d := "user://test_server_cloud_%d" % randi()
	DirAccess.make_dir_recursive_absolute(d)
	return d


func _server(data: String) -> GameServer:
	var s := GameServer.new()
	var p := ServerTests.pair(0)
	eq(s.start(PORT, p[0], p[1], data, "127.0.0.1"), OK, "server listens")
	s.accounts.rounds = 20
	return s


func _sync(account: Array = []) -> CloudSync:
	var c := CloudSync.new()
	c.setup("127.0.0.1", PORT, ServerTests.pair(0)[1])
	c.account = account
	return c


## Steps the server and the devices until done() or 5 s.
func _run(s: GameServer, devices: Array, done: Callable) -> bool:
	var t0 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < 5000:
		if s != null:
			s.poll(1)
		for d in devices:
			d.step()
		OS.delay_msec(1)
		if done.call():
			return true
	return false


func _end(s: GameServer, devices: Array, d: String) -> void:
	for c in devices:
		c.client.close()
	s.stop()
	ServerTests._rm(d)


func test_without_an_account_the_server_being_there_is_enough() -> void:
	var d := _dir()
	var s := _server(d)
	var a := _sync()
	check(not a.online(), "not before the server answered")
	check(_run(s, [a], a.online), "online once the server answers")
	_end(s, [a], d)


func test_register_sends_the_hero_made_before() -> void:
	var d := _dir()
	var s := _server(d)
	var a := _sync()
	a.save({"name": "Andrey", "level": 1})  # New Game before the registration
	var got := []
	a.register("ANDREY", "1234", func(r): got.append(r))
	check(_run(s, [a], func(): return not got.is_empty() and a.online() and a.idle()), "registered and sent")
	check(got[0].ok if not got.is_empty() else false, "the server took the account")
	eq(a.account, ["ANDREY", "1234"])
	eq(s.accounts.hero_get("ANDREY").hero, {"name": "Andrey", "level": 1}, "the hero is on the server")
	eq(a.rev, 1)
	_end(s, [a], d)


func test_another_device_takes_the_servers_hero() -> void:
	var d := _dir()
	var s := _server(d)
	s.accounts.create_account("ANDREY", "1234")
	s.accounts.hero_put("ANDREY", 0, 5, {"name": "Andrey", "level": 7})
	var b := _sync(["ANDREY", "1234"])
	check(_run(s, [b], b.online), "logged in")
	eq(int(b.hero.level), 7, "the server's hero")
	check(b.idle(), "nothing to send back")
	_end(s, [b], d)


func test_while_playing_this_devices_save_wins_a_conflict() -> void:
	var d := _dir()
	var s := _server(d)
	s.accounts.create_account("ANDREY", "1234")
	var a := _sync(["ANDREY", "1234"])
	check(_run(s, [a], a.online))
	s.accounts.hero_put("ANDREY", 0, 1, {"level": 2})  # another device saved meanwhile
	a.save({"level": 3})
	check(_run(s, [a], a.idle), "sent after the conflict")
	eq(int(s.accounts.hero_get("ANDREY").hero.level), 3, "this device's copy on top")
	eq(s.accounts.hero_get("ANDREY").rev, 2)
	_end(s, [a], d)


func test_a_wrong_password_is_refused_and_can_be_forgotten() -> void:
	var d := _dir()
	var s := _server(d)
	s.accounts.create_account("ANDREY", "1234")
	var a := _sync(["ANDREY", "9999"])
	check(_run(s, [a], a.refused), "refused")
	eq(a.err, "password")
	check(not a.online())
	a.forget_account()
	check(_run(s, [a], a.online), "without an account the game may start again")
	_end(s, [a], d)


func test_the_old_save_file_goes_to_the_server_once() -> void:
	var d := _dir()
	var s := _server(d)
	s.accounts.create_account("ANDREY", "1234")
	var a := _sync(["ANDREY", "1234"])
	a.legacy = {"name": "Old", "level": 9}
	check(_run(s, [a], func(): return a.online() and a.idle() and a.purge_legacy), "sent, file may go")
	eq(s.accounts.hero_get("ANDREY").hero, {"name": "Old", "level": 9})
	var b := _sync(["ANDREY", "1234"])
	b.legacy = {"name": "Older", "level": 1}
	check(_run(s, [b], b.online))
	eq(int(b.hero.level), 9, "the server already has a hero: the old file is not used")
	check(b.purge_legacy, "but it goes")
	_end(s, [b, a], d)


func test_no_server_waits_longer_each_time() -> void:
	var a := _sync(["ANDREY", "1234"])
	var now := [0]
	a.clock = func() -> int: return now[0]
	a.step()
	a.client.close()  # as if the connection failed
	check(not a.online())
	eq(a.retry_at, CloudSync.RETRY_MS, "next try in 30 s")
	now[0] = a.retry_at
	a.step()
	a.client.close()
	eq(a.retry_at, CloudSync.RETRY_MS * 3, "then after 60 s more")
	a.retry_now()
	eq(a.retry_at, 0, "OK on the offline screen tries now")


func test_profile_lives_on_the_server_when_online() -> void:
	var cloud: Node = root.get_node("/root/Cloud")
	var d := _dir()
	var s := _server(d)
	cloud.account_path = d.path_join("account.cfg")
	cloud.start("127.0.0.1", PORT, ServerTests.pair(0)[1])
	cloud.sync.legacy = null
	check(not Profile.exists(), "no hero yet")
	var p := Profile.new()
	p.hero_name = "Andrey"
	check(p.save(), "saved")
	check(Profile.exists(), "a hero now")
	eq(Profile.load_or_new().hero_name, "Andrey", "read back from memory")
	var got := []
	cloud.register("ANDREY", "1234", func(r): got.append(r))
	check(_run(s, [cloud.sync], func(): return cloud.online() and cloud.sync.idle()), "registered, sent")
	eq(str(s.accounts.hero_get("ANDREY").hero.name), "Andrey", "on the server")
	eq(cloud.load_account(), ["ANDREY", "1234"], "the account stays on this device")
	cloud.forget_account()
	eq(cloud.load_account(), [], "forgotten")
	cloud.stop()
	check(not cloud.enabled(), "off again: the hero file as before")
	s.stop()
	ServerTests._rm(d)


func test_live_goes_over_the_same_connection() -> void:
	var cloud: Node = root.get_node("/root/Cloud")
	var d := _dir()
	var s := _server(d)
	s.accounts.create_account("ANDREY", "1234")
	cloud.account_path = d.path_join("account.cfg")
	cloud.save_account("ANDREY", "1234")
	cloud.start("127.0.0.1", PORT, ServerTests.pair(0)[1])
	cloud.sync.legacy = null
	var got := []
	cloud.request({"t": "live_status"}, func(r): got.append(r))
	eq(got[0].err if not got.is_empty() else "", "offline", "not before the login")
	check(_run(s, [cloud.sync], cloud.online), "logged in")
	var p := Profile.new()
	p.gold = 300
	p.add_item(load("res://scripts/core/items.gd").make(101))
	var err := []
	cloud.live.sync(p, func(e): err.append(e))
	check(_run(s, [cloud.sync], func(): return not err.is_empty()), "answered")
	eq(err, [""], "synced")
	cloud.live.move_gold(p, true, 100, func(e): err.append(e))
	check(_run(s, [cloud.sync], func(): return err.size() > 1), "answered")
	eq([err[-1], int(p.gold), cloud.live.safe], ["", 200, 100], "gold into the Safe on the server")
	eq(int(s.live.user("ANDREY").safe), 100)
	cloud.stop()
	check(cloud.live == null, "no Live without the server")
	s.stop()
	ServerTests._rm(d)


func test_the_online_game_goes_over_the_same_connection() -> void:
	var cloud: Node = root.get_node("/root/Cloud")
	var d := _dir()
	var s := _server(d)
	s.accounts.create_account("ANDREY", "1234")
	s.accounts.create_account("MARIA", "1234")
	cloud.account_path = d.path_join("account.cfg")
	cloud.save_account("ANDREY", "1234")
	cloud.start("127.0.0.1", PORT, ServerTests.pair(0)[1])
	cloud.sync.legacy = null
	check(_run(s, [cloud.sync], cloud.online), "logged in")
	var mp: RefCounted = cloud.mp
	var err := []
	mp.enter(func(e): err.append(e))
	check(_run(s, [cloud.sync], func(): return not err.is_empty()), "answered")
	eq([err, mp.entered, s.online.is_online("ANDREY")], [[""], true, true], "online")
	var maria := Online.Session.new()  # another player, on the server
	maria.send = func(_m: Dictionary) -> void: pass
	s.online.enter(maria, "MARIA")
	eq(s.online.answer(maria, "chat_send", {"channel": Online.PRIVATE, "peer": "ANDREY", "text": "hi"}).ok, true)
	check(_run(s, [cloud.sync], func(): return int(mp.unread[1]) == 1), "her message pushed here, waiting")
	eq(mp.chat["pm:MARIA"].map(func(r): return r.text), ["hi"])
	cloud.stop()
	check(cloud.mp == null, "no online game without the server")
	s.stop()
	ServerTests._rm(d)
