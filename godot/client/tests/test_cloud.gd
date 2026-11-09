extends "res://tests/test_case.gd"
## Always online: the hero kept on the server (scripts/net/cloud_sync.gd, cloud.gd) against a
## real server in this process.

const ServerTests := preload("res://tests/test_server.gd")
const SettingsScript := preload("res://scripts/core/settings.gd")
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
	check(
		_run(s, [a], func(): return not got.is_empty() and a.online() and a.idle()),
		"registered and sent"
	)
	check(got[0].ok if not got.is_empty() else false, "the server took the account")
	eq(a.account, ["ANDREY", "1234"])
	eq(
		s.accounts.hero_get("ANDREY").hero,
		{"name": "Andrey", "level": 1},
		"the hero is on the server"
	)
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
	check(
		_run(s, [a], func(): return a.online() and a.idle() and a.purge_legacy), "sent, file may go"
	)
	eq(s.accounts.hero_get("ANDREY").hero, {"name": "Old", "level": 9})
	var b := _sync(["ANDREY", "1234"])
	b.legacy = {"name": "Older", "level": 1}
	check(_run(s, [b], b.online))
	eq(int(b.hero.level), 9, "the server already has a hero: the old file is not used")
	check(b.purge_legacy, "but it goes")
	_end(s, [b, a], d)


func test_the_game_is_always_online_with_the_internet_server_by_default() -> void:
	var Cloud := preload("res://scripts/net/cloud.gd")
	var cfg: Dictionary = Cloud.server_config(PackedStringArray())
	eq(cfg.address, "140.238.73.129", "the game's server (project setting pow/net/server)")
	eq(cfg.port, 28310)
	eq(cfg.cert_path, "res://net/server.crt", "its certificate, shipped with the game")
	check(FileAccess.file_exists(cfg.cert_path), "the certificate is in the project")
	cfg = Cloud.server_config(
		PackedStringArray(["--server", "127.0.0.1", "--cert", "user://server/server.crt"])
	)
	eq(
		[cfg.address, cfg.port, cfg.cert_path],
		["127.0.0.1", 28310, "user://server/server.crt"],
		"the local server"
	)
	cfg = Cloud.server_config(
		PackedStringArray(["--server", "pow.example:28311", "--cert", "/x/s.crt"])
	)
	eq([cfg.address, cfg.port, cfg.cert_path], ["pow.example", 28311, "/x/s.crt"], "another server")
	eq(Cloud.server_config(PackedStringArray(["--offline"])), {}, "--offline: without a server")
	var d := _dir()
	eq(
		Cloud.server_config(PackedStringArray(), d).cert_path,
		"res://net/server.crt",
		"no files next to the game: the project's server"
	)
	var f := FileAccess.open(d.path_join("server.txt"), FileAccess.WRITE)
	f.store_string("# the server of our group\n\n  friends.example:28312  \n")
	f.close()
	FileAccess.open(d.path_join("server.crt"), FileAccess.WRITE).close()
	cfg = Cloud.server_config(PackedStringArray(), d)
	eq(
		[cfg.address, cfg.port, cfg.cert_path],
		["friends.example", 28312, d.path_join("server.crt")],
		"server.txt and server.crt next to the game"
	)
	cfg = Cloud.server_config(PackedStringArray(["--server", "pow.example"]), d)
	eq([cfg.address, cfg.port], ["pow.example", 28310], "the command line wins")
	check(Cloud.runs_the_game(PackedStringArray(["--path", "godot/client"])), "the game")
	check(Cloud.runs_the_game(PackedStringArray(["res://scenes/main.tscn"])), "its main scene")
	check(
		not Cloud.runs_the_game(PackedStringArray(["--headless", "res://tests/runner.tscn"])),
		"not the tests"
	)
	check(not Cloud.runs_the_game(PackedStringArray(["res://server/main.tscn"])), "not the server")
	check(
		not Cloud.runs_the_game(PackedStringArray(["-s", "res://tools/net_check.gd"])), "not a tool"
	)


func test_the_certificate_is_read_once_the_local_server_made_it() -> void:
	var d := _dir()
	var a := CloudSync.new()
	a.setup("127.0.0.1", PORT, null)
	a.cert_path = d.path_join("server.crt")
	a.step()
	check(not a.online(), "no certificate yet: no connection")
	check(a.retry_at > 0, "tries again later")
	var s := _server(d)
	ServerTests.pair(0)[1].save(a.cert_path)
	a.retry_now()
	check(_run(s, [a], a.online), "online once the certificate is there")
	_end(s, [a], d)


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
	check(cloud.sync.options_store == root.get_node("/root/Settings"), "the Options go along")
	cloud.sync.options_store = null  # this device's own Options stay out of the tests
	check(not Profile.exists(), "no hero yet")
	var p := Profile.new()
	p.hero_name = "Andrey"
	check(p.save(), "saved")
	check(Profile.exists(), "a hero now")
	eq(Profile.load_or_new().hero_name, "Andrey", "read back from memory")
	var got := []
	cloud.register("ANDREY", "1234", func(r): got.append(r))
	check(
		_run(s, [cloud.sync], func(): return cloud.online() and cloud.sync.idle()),
		"registered, sent"
	)
	eq(str(s.accounts.hero_get("ANDREY").hero.name), "Andrey", "on the server")
	eq(cloud.sync.account, ["ANDREY", "1234"], "the account kept while the game runs")
	check(not FileAccess.file_exists(cloud.account_path), "and not on the device")
	cloud.forget_account()
	check(not cloud.has_account(), "forgotten")
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
	cloud.start("127.0.0.1", PORT, ServerTests.pair(0)[1])
	cloud.sync.legacy = null
	cloud.sync.options_store = null  # this device's own Options stay out of the tests
	cloud.login("ANDREY", "1234", func(_r: Dictionary) -> void: pass)
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
	cloud.start("127.0.0.1", PORT, ServerTests.pair(0)[1])
	cloud.sync.legacy = null
	cloud.sync.options_store = null  # this device's own Options stay out of the tests
	cloud.login("ANDREY", "1234", func(_r: Dictionary) -> void: pass)
	check(_run(s, [cloud.sync], cloud.online), "logged in")
	var mp: RefCounted = cloud.mp
	var err := []
	mp.enter(func(e): err.append(e))
	check(_run(s, [cloud.sync], func(): return not err.is_empty()), "answered")
	eq([err, mp.entered, s.online.is_online("ANDREY")], [[""], true, true], "online")
	var maria := OnlineServer.Session.new()  # another player, on the server
	maria.send = func(_m: Dictionary) -> void: pass
	s.online.enter(maria, "MARIA")
	eq(
		(
			s
			. online
			. answer(
				maria,
				"chat_send",
				{"channel": OnlineServer.PRIVATE, "peer": "ANDREY", "text": "hi"}
			)
			. ok
		),
		true
	)
	check(
		_run(s, [cloud.sync], func(): return int(mp.unread[1]) == 1),
		"her message pushed here, waiting"
	)
	eq(mp.chat["pm:MARIA"].map(func(r): return r.text), ["hi"])
	cloud.stop()
	check(cloud.mp == null, "no online game without the server")
	s.stop()
	ServerTests._rm(d)


## The Options of one device, in their own file.
func _options(d: String, tag: String) -> Node:
	var o: Node = SettingsScript.new()
	o.path = d.path_join("settings_%s.cfg" % tag)
	o.load_from_disk()
	return o


func test_the_options_follow_the_account() -> void:
	var d := _dir()
	var s := _server(d)
	s.accounts.create_account("ANDREY", "1234")
	var a := _sync(["ANDREY", "1234"])
	a.options_store = _options(d, "a")
	a.options_store.set_value("game_speed", 4)
	check(_run(s, [a], func(): return a.online() and a.idle()), "logged in, sent")
	eq(
		s.accounts.store_get("ANDREY", "options").data,
		{"music_volume": 0.8, "sfx_volume": 0.8, "game_speed": 4},
		"the volumes and the speed"
	)
	var b := _sync(["ANDREY", "1234"])
	b.options_store = _options(d, "b")
	b.options_store.set_value("game_speed", 0)  # before this account was used here
	check(_run(s, [b], func(): return b.online() and b.idle()), "the other device logged in")
	eq(b.options_store.get_value("game_speed"), 4, "a device new to the account takes the server's")
	eq(b.options_store.cloud.user, "ANDREY")
	b.options_store.set_value("sfx_volume", 0.3)
	check(_run(s, [b], b.idle), "sent")
	a.client.close()
	a.options_store.free()
	a = _sync(["ANDREY", "1234"])  # the first device starts the game again
	a.options_store = _options(d, "a")
	eq(
		[a.options_store.get_value("game_speed"), a.options_store.cloud.rev],
		[4, 1],
		"its own, from its file"
	)
	check(_run(s, [a], func(): return a.online() and a.idle()), "logged in")
	eq(a.options_store.get_value("sfx_volume"), 0.3, "the newer copy wins")
	var again := _options(d, "a")
	eq(
		[again.get_value("sfx_volume"), again.cloud.rev, again.cloud.dirty],
		[0.3, 2, false],
		"kept on the device"
	)
	again.free()
	a.options_store.set_value("music_volume", 0.5)  # changed on both while both play
	check(a.flushing(), "Quit waits for the options too")
	b.options_store.set_value("music_volume", 0.1)
	check(_run(s, [a, b], func(): return a.idle() and b.idle()), "both sent")
	eq(s.accounts.store_get("ANDREY", "options").rev, 4, "the second one went on top of the first")
	b.client.close()
	b.options_store.set_value("game_speed", 1)  # changed while the connection is lost
	b.step()
	check(not b.online(), "offline")
	a.options_store.set_value("game_speed", 2)
	check(_run(s, [a], a.idle), "the other device sent its own meanwhile")
	b.options_store.cloud.at = a.options_store.cloud.at + 1  # but this change came later
	b.retry_now()
	check(_run(s, [b], func(): return b.online() and b.idle()), "back online")
	eq(
		[
			b.options_store.get_value("game_speed"),
			int(s.accounts.store_get("ANDREY", "options").data.game_speed)
		],
		[1, 1],
		"the later change wins"
	)
	_end(s, [a, b], d)
	a.options_store.free()
	b.options_store.free()


func test_quitting_lets_the_last_save_reach_the_server() -> void:
	var cloud: Node = root.get_node("/root/Cloud")
	var d := _dir()
	var s := _server(d)
	s.accounts.create_account("ANDREY", "1234")
	cloud.account_path = d.path_join("account.cfg")
	cloud.start("127.0.0.1", PORT, ServerTests.pair(0)[1])
	cloud.sync.legacy = null
	cloud.sync.options_store = null  # this device's own Options stay out of the tests
	cloud.login("ANDREY", "1234", func(_r: Dictionary) -> void: pass)
	var quits := []
	cloud.quit_now = func() -> void: quits.append(true)
	check(_run(s, [cloud.sync], cloud.online), "logged in")
	cloud.quit_game()
	eq(quits.size(), 1, "nothing waits: at once")
	cloud.save_hero({"name": "Andrey", "level": 7})
	cloud.quit_game()
	cloud._process(0.0)
	eq(quits.size(), 1, "not before the last save is on the server")
	var t0 := Time.get_ticks_msec()
	while quits.size() < 2 and Time.get_ticks_msec() - t0 < 5000:
		s.poll(1)
		cloud._process(0.0)
		OS.delay_msec(1)
	eq(quits.size(), 2, "then the game ends")
	eq(int(s.accounts.hero_get("ANDREY").hero.level), 7, "with the save on the server")
	cloud.save_hero({"name": "Andrey", "level": 8})
	cloud.quit_game()
	cloud._process(0.0)  # the server does not answer
	eq(quits.size(), 2, "waiting")
	cloud.quit_at = Time.get_ticks_msec()  # FLUSH_MS later
	cloud._process(0.0)
	eq(quits.size(), 3, "no longer than FLUSH_MS")
	cloud.save_hero({"name": "Andrey", "level": 9})
	cloud.sync.client.close()
	cloud.quit_game()
	eq(quits.size(), 4, "no connection: at once")
	cloud.stop()
	cloud.quit_game()
	eq(quits.size(), 5, "without the server: at once")
	cloud.quit_now = Callable()
	s.stop()
	ServerTests._rm(d)


func test_the_login_lasts_only_while_the_game_runs() -> void:
	var cloud: Node = root.get_node("/root/Cloud")
	var d := _dir()
	var s := _server(d)
	s.accounts.create_account("ANDREY", "1234")
	cloud.account_path = d.path_join("account.cfg")
	var old := ConfigFile.new()  # an older version kept the account here
	old.set_value("account", "id", "ANDREY")
	old.set_value("account", "pwd", "1234")
	old.save(cloud.account_path)
	cloud.start("127.0.0.1", PORT, ServerTests.pair(0)[1])
	cloud.sync.legacy = null
	cloud.sync.options_store = null  # this device's own Options stay out of the tests
	check(not cloud.has_account(), "a new start asks for the account")
	check(not FileAccess.file_exists(cloud.account_path), "the old file is gone")
	check(_run(s, [cloud.sync], cloud.online), "the server is there")
	var got := []
	cloud.login("ANDREY", "9999", func(r): got.append(r))
	check(_run(s, [cloud.sync], func(): return not got.is_empty()), "answered")
	eq([got[0].get("err"), cloud.has_account()], ["password", false], "a wrong password")
	cloud.login("MARIA", "1234", func(r): got.append(r))
	check(_run(s, [cloud.sync], func(): return got.size() > 1), "answered")
	eq(got[1].get("err"), "no account", "nobody by that UserID")
	cloud.login("ANDREY", "1234", func(r): got.append(r))
	check(_run(s, [cloud.sync], func(): return got.size() > 2 and cloud.online()), "logged in")
	eq(
		[got[2].get("ok"), cloud.has_account(), cloud.hero()],
		[true, true, null],
		"no hero there yet"
	)
	check(not FileAccess.file_exists(cloud.account_path), "nothing kept on the device")
	cloud.stop()
	s.stop()
	ServerTests._rm(d)


func test_a_login_after_the_server_answered_gets_its_answer() -> void:
	var d := _dir()
	var s := _server(d)
	s.accounts.create_account("ANDREY", "1234")
	var a := _sync()
	check(_run(s, [a], a.online), "the server is there: the menu opens")
	for i in 50:  # the menu stays open a while before the player logs in
		s.poll(1)
		a.step()
	var got := []
	a.login("ANDREY", "1234", func(r): got.append(r))
	check(
		_run(s, [a], func(): return not got.is_empty() and a.online()),
		"answered, not Connecting... for ever"
	)
	eq(got[0].get("ok") if not got.is_empty() else null, true, "logged in")
	_end(s, [a], d)
