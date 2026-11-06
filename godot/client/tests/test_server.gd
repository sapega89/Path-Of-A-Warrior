extends "res://tests/test_case.gd"
## The game's server: protocol checks, accounts, limits, and a real ENet + DTLS connection.

const Protocol := preload("res://scripts/net/protocol.gd")
const NetClient := preload("res://scripts/net/net_client.gd")
const GameServer := preload("res://server/game_server.gd")
const Accounts := preload("res://server/accounts.gd")
const Guard := preload("res://server/guard.gd")
const ServerMain := preload("res://server/main.gd")
const PORT := 28399

static var _pairs: Array = []  # [key, cert] made once for all the tests


static func pair(i: int) -> Array:
	while _pairs.size() <= i:
		var c := Crypto.new()
		var key := c.generate_rsa(2048)
		_pairs.append([key, c.generate_self_signed_certificate(key, "CN=localhost,O=Test,C=UA")])
	return _pairs[i]


func _dir(tag: String) -> String:
	var d := "user://test_server_%s_%d" % [tag, randi()]
	DirAccess.make_dir_recursive_absolute(d)
	return d


## Removes a folder this test made (only user://test_server_*).
static func _rm(d: String) -> void:
	if not d.begins_with("user://test_server_"):
		return
	for sub in DirAccess.get_directories_at(d):
		_rm(d.path_join(sub))
	for f in DirAccess.get_files_at(d):
		DirAccess.remove_absolute(d.path_join(f))
	DirAccess.remove_absolute(d)


func _server(data: String) -> GameServer:
	var s := GameServer.new()
	var p := pair(0)
	eq(s.start(PORT, p[0], p[1], data, "127.0.0.1"), OK, "server listens")
	s.accounts.rounds = 50
	return s


## Polls both sides until done() is true or 5 s pass.
func _pump(s: GameServer, c: NetClient, done: Callable) -> bool:
	var t0 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < 5000:
		s.poll(1)
		c.poll(1)
		if done.call():
			return true
	return false


func test_pbkdf2_matches_rfc_vector() -> void:
	var a := Accounts.new(_dir("kdf"))
	# RFC 7914 section 11: PBKDF2-HMAC-SHA256 ("passwd", "salt", 1), first 32 bytes
	eq(a.pbkdf2("passwd".to_ascii_buffer(), "salt".to_ascii_buffer(), 1).hex_encode(),
		"55ac046e56e3089fec1691c22544b605f94185216dde0465e68b9d57c20dacbc")
	check(Accounts.same_bytes(PackedByteArray([1, 2]), PackedByteArray([1, 2])))
	check(not Accounts.same_bytes(PackedByteArray([1, 2]), PackedByteArray([1, 3])))
	_rm(a.dir)


func test_ids_and_packets() -> void:
	check(Protocol.valid_id("ANDREY"))
	check(not Protocol.valid_id("ABC"), "too short")
	check(not Protocol.valid_id("Andrey"), "lower case")
	check(not Protocol.valid_id(1234))
	check(Protocol.valid_password("1234"))
	check(not Protocol.valid_password("12a4"))
	eq(Protocol.decode(Protocol.encode({"t": "x"})), {"t": "x"})
	eq(Protocol.decode(var_to_bytes([1, 2])), {}, "not a dictionary")
	eq(Protocol.decode(var_to_bytes_with_objects(Node.new())), {}, "objects refused")
	eq(Protocol.decode(PackedByteArray([1, 2, 3])), {}, "garbage")


func test_wrong_passwords_block_the_login() -> void:
	var g := Guard.new()
	var now := [0.0]
	g.clock = func() -> float: return now[0]
	var wrong := func() -> bool: return false
	var right := func() -> bool: return true
	for i in Guard.LOGIN_FAILS:
		check(not g.check_password("ANDREY", "1.2.3.4", wrong))
	check(not g.check_password("ANDREY", "", right), "blocked looks like a wrong password")
	check(not g.check_password("OTHER", "1.2.3.4", right), "the address is blocked too")
	now[0] = Guard.LOGIN_BLOCK + 1.0
	check(g.check_password("ANDREY", "1.2.3.4", right), "free again after the block")


func test_new_accounts_connections_and_flood_limits() -> void:
	var g := Guard.new()
	var now := [0.0]
	g.clock = func() -> float: return now[0]
	for i in Guard.NEW_ACCOUNTS:
		check(g.may_create("1.2.3.4"))
	check(not g.may_create("1.2.3.4"), "6th account in an hour")
	check(g.may_create("5.6.7.8"), "another address")
	now[0] = Guard.NEW_ACCOUNTS_WINDOW + 1.0
	check(g.may_create("1.2.3.4"), "an hour later")
	for i in Guard.MAX_CONNECTIONS:
		check(g.open_connection("1.2.3.4"))
	check(not g.open_connection("1.2.3.4"), "11th connection")
	g.close_connection("1.2.3.4")
	check(g.open_connection("1.2.3.4"))
	var m := g.meter()
	for i in Guard.MAX_MESSAGES:
		check(m.allow())
	check(not m.allow(), "31st message in a second")


func test_accounts_keep_the_hero_on_disk() -> void:
	var d := _dir("acc")
	var a := Accounts.new(d)
	a.rounds = 20
	check(a.create_account("ANDREY", "1234"))
	check(not a.create_account("ANDREY", "9999"), "taken")
	check(a.check_password("ANDREY", "1234"))
	check(not a.check_password("ANDREY", "1235"))
	check(not a.check_password("NOBODY", "1234"))
	eq(a.hero_get("ANDREY"), {"rev": 0, "at": 0, "hero": null}, "no hero yet")
	var r: Array = a.hero_put("ANDREY", 0, 100, {"hero_name": "Andrey", "level": 3})
	check(r[0], "first save")
	eq(r[1].rev, 1)
	r = a.hero_put("ANDREY", 0, 200, {"hero_name": "Other"})
	check(not r[0], "a save from an old revision is a conflict")
	eq(r[1].hero.hero_name, "Andrey", "the conflict carries the server's hero")
	var again := Accounts.new(d)  # as after a restart
	check(again.check_password("ANDREY", "1234"), "password after a restart")
	eq(again.hero_get("ANDREY").rev, 1)
	eq(int(again.hero_get("ANDREY").hero.level), 3)
	check(not FileAccess.file_exists(d.path_join("ANDREY.json.tmp")), "no temporary file left")
	var text := FileAccess.get_file_as_string(d.path_join("ANDREY.json"))
	check(not text.contains("1234"), "the password is not in the file")
	_rm(d)


func test_requests_and_their_answers() -> void:
	var d := _dir("ans")
	var s := GameServer.new()
	s.accounts = Accounts.new(d)
	s.accounts.rounds = 20
	var a := GameServer.Session.new()
	eq(s.answer(a, {}).err, "bad message")
	eq(s.answer(a, {"t": "hero_get", "q": 7}), {"t": "hero_get", "ok": false, "err": "login first", "q": 7})
	eq(s.answer(a, {"t": "login", "id": "ANDREY", "pwd": "1234", "v": 0}).err, "update")
	eq(s.answer(a, {"t": "login", "id": "ANDREY", "pwd": "1234", "v": Protocol.VERSION}).err, "no account")
	eq(s.answer(a, {"t": "register", "id": "AN", "pwd": "1234", "v": Protocol.VERSION}).err, "bad id")
	check(s.answer(a, {"t": "register", "id": "ANDREY", "pwd": "1234", "v": Protocol.VERSION}).ok)
	eq(s.answer(a, {"t": "nope"}).err, "unknown")
	eq(s.answer(a, {"t": "hero_put", "base": "0", "at": 1, "hero": {}}).err, "bad message")
	eq(s.answer(a, {"t": "hero_put", "base": 0, "at": 1, "hero": {"x": "a".repeat(Protocol.MAX_HERO)}}).err,
		"too big")
	eq(s.answer(a, {"t": "hero_put", "base": 0, "at": 1, "hero": {"level": 2}}), {"t": "hero_put", "ok": true, "rev": 1})
	var b := GameServer.Session.new()
	eq(s.answer(b, {"t": "register", "id": "ANDREY", "pwd": "5555", "v": Protocol.VERSION}).err, "taken")
	eq(s.answer(b, {"t": "login", "id": "ANDREY", "pwd": "5555", "v": Protocol.VERSION}).err, "password")
	check(s.answer(b, {"t": "login", "id": "ANDREY", "pwd": "1234", "v": Protocol.VERSION}).ok)
	var c := s.answer(b, {"t": "hero_put", "base": 0, "at": 2, "hero": {"level": 9}})
	eq([c.err, c.rev, int(c.hero.level)], ["conflict", 1, 2], "the other device saved first")
	eq(s.answer(b, {"t": "hero_put", "base": 1, "at": 2, "hero": {"level": 9}}).rev, 2)
	eq(int(s.answer(a, {"t": "hero_get"}).hero.level), 9)
	_rm(d)


func test_register_and_save_over_enet_dtls() -> void:
	var d := _dir("net")
	var s := _server(d)
	var c := NetClient.new()
	eq(c.open("127.0.0.1", PORT, pair(0)[1]), OK, "client set up")
	var got := []
	c.request({"t": "register", "id": "ANDREY", "pwd": "1234", "v": Protocol.VERSION}, func(r): got.append(r))
	c.request({"t": "hero_put", "base": 0, "at": 5, "hero": {"hero_name": "Andrey"}}, func(r): got.append(r))
	c.request({"t": "hero_get"}, func(r): got.append(r))
	check(_pump(s, c, func(): return got.size() == 3), "three answers")
	if got.size() == 3:
		check(got[0].ok, "registered")
		eq(got[1].get("rev"), 1, "saved")
		eq(got[2].get("hero"), {"hero_name": "Andrey"}, "the hero back")
		eq(got[2].get("q"), 3, "answers carry their request's number")
	eq(c.state, NetClient.State.CONNECTED)
	eq(s.sessions.size(), 1)
	c.close()
	check(_pump(s, c, func(): return s.sessions.is_empty()), "the server sees the client leave")
	s.stop()
	_rm(d)


func test_a_server_with_another_certificate_is_refused() -> void:
	var d := _dir("cert")
	var s := _server(d)
	var c := NetClient.new()
	eq(c.open("127.0.0.1", PORT, pair(1)[1]), OK)
	var got := []
	c.request({"t": "login", "id": "ANDREY", "pwd": "1234", "v": Protocol.VERSION}, func(r): got.append(r))
	_pump(s, c, func(): return not got.is_empty() or c.state == NetClient.State.CLOSED)
	check(c.state != NetClient.State.CONNECTED, "not connected to an unknown server")
	if not got.is_empty():
		eq(got[0].err, "offline")
	c.close()
	s.stop()
	_rm(d)


func test_requests_when_offline() -> void:
	var c := NetClient.new()
	var got := []
	c.request({"t": "hero_get"}, func(r): got.append(r))
	eq(got, [{"t": "hero_get", "ok": false, "err": "offline", "q": 1}])


func test_server_args_and_certificate_files() -> void:
	eq(ServerMain.parse_args(PackedStringArray(["--port", "1234", "--data", "x", "loose"])),
		{"port": "1234", "data": "x"})
	var d := _dir("main")
	var first := ServerMain.load_or_make_cert(d, "", "")
	eq(first.size(), 2, "made a pair")
	check(FileAccess.file_exists(d.path_join("server.crt")))
	var second := ServerMain.load_or_make_cert(d, "", "")
	eq(second.size(), 2, "read it back")
	if second.size() == 2:
		eq(second[1].save_to_string(), first[1].save_to_string(), "the same certificate next time")
	_rm(d)
