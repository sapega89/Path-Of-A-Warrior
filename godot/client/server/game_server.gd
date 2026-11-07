extends RefCounted
## The game's server: accounts and the hero kept on the server (scripts/net/protocol.gd), Live
## (server/live.gd) and the online game (server/online.gd).
## start() binds the UDP port with DTLS, then poll() is called every frame (server/main.gd)
## or in a loop (tests).

const Protocol := preload("res://scripts/net/protocol.gd")
const Accounts := preload("res://server/accounts.gd")
const Guard := preload("res://server/guard.gd")
const Live := preload("res://server/live.gd")
const Online := preload("res://server/online.gd")

var host := ENetConnection.new()
var accounts: Accounts
var live: Live
var online: Online
var guard := Guard.new()
var running := false
## ENetPacketPeer -> Session.
var sessions := {}
## [peer, message] pushed by the online game (chat, battles), sent after the answer of the
## request that made them.
var _outbox: Array = []
## Lines of the log go here (main.gd prints them).
var log_line: Callable = func(_s: String) -> void: pass


class Session:
	var peer: ENetPacketPeer
	var address := ""
	var user := ""
	var meter: RefCounted
	var live := Live.Session.new()
	var online := Online.Session.new()


## Error code of the bind / DTLS setup, OK when the server is listening.
func start(port: int, key: CryptoKey, cert: X509Certificate, data_dir: String,
		bind_address := "*", max_peers := 256) -> int:
	accounts = Accounts.new(data_dir.path_join("accounts"))
	live = Live.new(data_dir)
	online = Online.new(data_dir, accounts)
	online.add_bots()
	var err := host.create_host_bound(bind_address, port, max_peers, Protocol.CHANNELS)
	if err != OK:
		return err
	err = host.dtls_server_setup(TLSOptions.server(key, cert))
	if err != OK:
		host.destroy()
		return err
	running = true
	return OK


func stop() -> void:
	if not running:
		return
	for p: ENetPacketPeer in sessions.keys():
		p.peer_disconnect_now()
	sessions.clear()
	if online != null:
		online.shutdown()
	_outbox.clear()
	host.destroy()
	running = false


## Handles every event waiting on the socket.
func poll(wait_ms := 0) -> void:
	if not running:
		return
	var ev: Array = host.service(wait_ms)
	while ev[0] != ENetConnection.EVENT_NONE:
		_event(ev)
		_flush()
		if ev[0] == ENetConnection.EVENT_ERROR:
			return
		ev = host.service(0)
	if online != null:
		online.tick()  # a duel that waited long enough gets the CPU
		_flush()


## Sends the pushes: the chat on channel 1, the rest (battles) on channel 0 in order with the
## answers.
func _flush() -> void:
	var out := _outbox.duplicate()
	_outbox.clear()
	for x in out:
		var peer: ENetPacketPeer = x[0]
		var m: Dictionary = x[1]
		peer.send(1 if m.get("t") == "chat_push" else 0, Protocol.encode(m), ENetPacketPeer.FLAG_RELIABLE)


func _event(ev: Array) -> void:
	var peer: ENetPacketPeer = ev[1]
	match ev[0]:
		ENetConnection.EVENT_CONNECT:
			var s := Session.new()
			s.peer = peer
			s.address = peer.get_remote_address()
			if not guard.open_connection(s.address):
				log_line.call("too many connections from %s" % s.address)
				peer.peer_disconnect_now()
				return
			s.meter = guard.meter()
			var outbox := _outbox
			s.online.send = func(m: Dictionary) -> void:  # a push, no request waits for it
				outbox.append([peer, m])
			sessions[peer] = s
		ENetConnection.EVENT_DISCONNECT:
			var s: Session = sessions.get(peer)
			if s != null:
				log_line.call("%s left (%s)" % [s.user if not s.user.is_empty() else "a guest", s.address])
				guard.close_connection(s.address)
				_leave_online(s)
				sessions.erase(peer)
		ENetConnection.EVENT_RECEIVE:
			var data := peer.get_packet()
			var s: Session = sessions.get(peer)
			if s == null:
				return
			if not s.meter.allow():
				log_line.call("flood from %s, closed" % s.address)
				_drop(s)
				return
			if data.size() > Protocol.MAX_PACKET:
				_send(s, {"t": "?", "ok": false, "err": "too big"})
				return
			_send(s, answer(s, Protocol.decode(data)))


func _drop(s: Session) -> void:
	guard.close_connection(s.address)
	_leave_online(s)
	sessions.erase(s.peer)
	s.peer.peer_disconnect_later()


func _leave_online(s: Session) -> void:
	if online != null:
		online.leave(s.online)


func _send(s: Session, msg: Dictionary) -> void:
	s.peer.send(0, Protocol.encode(msg), ENetPacketPeer.FLAG_RELIABLE)


## The answer to one request of a session.
func answer(s: Session, msg: Dictionary) -> Dictionary:
	var t: Variant = msg.get("t")
	var reply: Dictionary
	if not t is String:
		reply = {"t": "?", "ok": false, "err": "bad message"}
	elif t != "register" and t != "login" and s.user.is_empty():
		reply = _fail(t, "login first")
	else:
		match t:
			"register": reply = _register(s, msg)
			"login": reply = _login(s, msg)
			"hero_get": reply = _hero_get(s)
			"hero_put": reply = _hero_put(s, msg)
			"options_get": reply = _options_get(s)
			"options_put": reply = _options_put(s, msg)
			"name_check": reply = _name_check(s, msg)
			_:
				if t.begins_with("live_") and live != null:
					reply = live.answer(s.live, t, msg)
				elif t == "mp_enter" and online != null:
					reply = online.enter(s.online, s.user)
				elif online != null and (t.begins_with("mp_") or t.begins_with("order_")
						or t.begins_with("chat_")):
					reply = online.answer(s.online, t, msg)
				else:
					reply = _fail(t, "unknown")
	if msg.get("q") is int:
		reply["q"] = msg["q"]
	return reply


static func _fail(t: String, err: String) -> Dictionary:
	return {"t": t, "ok": false, "err": err}


func _register(s: Session, msg: Dictionary) -> Dictionary:
	if msg.get("v") != Protocol.VERSION:
		return _fail("register", "update")
	var uid: Variant = msg.get("id")
	var pwd: Variant = msg.get("pwd")
	if not (Protocol.valid_id(uid) and Protocol.valid_password(pwd)):
		return _fail("register", "bad id")
	if accounts.has_account(uid):
		return _fail("register", "taken")
	if not guard.may_create(s.address):
		return _fail("register", "limit")
	if not accounts.create_account(uid, pwd):
		return _fail("register", "taken")
	_leave_online(s)
	s.user = uid
	s.live.user = uid
	log_line.call("new account %s from %s" % [uid, s.address])
	return {"t": "register", "ok": true}


func _login(s: Session, msg: Dictionary) -> Dictionary:
	if msg.get("v") != Protocol.VERSION:
		return _fail("login", "update")
	var uid: Variant = msg.get("id")
	var pwd: Variant = msg.get("pwd")
	if not (Protocol.valid_id(uid) and Protocol.valid_password(pwd)):
		return _fail("login", "bad id")
	if not accounts.has_account(uid):
		return _fail("login", "no account")
	if not guard.check_password(uid, s.address, accounts.check_password.bind(uid, pwd)):
		return _fail("login", "password")
	_leave_online(s)
	s.user = uid
	s.live.user = uid
	log_line.call("%s logged in from %s" % [uid, s.address])
	return {"t": "login", "ok": true}


## Whether the new game may call the hero so: no other player's hero (nor a bot) has the name.
func _name_check(s: Session, msg: Dictionary) -> Dictionary:
	var name: Variant = msg.get("name")
	if not name is String or online == null:
		return _fail("name_check", "bad message")
	var err := online.check_name(name, s.user)
	return {"t": "name_check", "ok": true} if err.is_empty() else _fail("name_check", err)


func _hero_get(s: Session) -> Dictionary:
	var h := accounts.hero_get(s.user)
	return {"t": "hero_get", "ok": true, "rev": h.rev, "at": h.at, "hero": h.hero}


func _hero_put(s: Session, msg: Dictionary) -> Dictionary:
	var base: Variant = msg.get("base")
	var at: Variant = msg.get("at")
	var hero: Variant = msg.get("hero")
	if not (base is int and at is int and hero is Dictionary):
		return _fail("hero_put", "bad message")
	if JSON.stringify(hero).length() > Protocol.MAX_HERO:
		return _fail("hero_put", "too big")
	var r: Array = accounts.hero_put(s.user, base, at, hero)
	var entry: Dictionary = r[1]
	if r[0]:
		return {"t": "hero_put", "ok": true, "rev": entry.rev}
	return {"t": "hero_put", "ok": false, "err": "conflict",
		"rev": entry.rev, "at": entry.at, "hero": entry.hero}


func _options_get(s: Session) -> Dictionary:
	var e := accounts.store_get(s.user, "options")
	return {"t": "options_get", "ok": true, "rev": e.rev, "at": e.at, "options": e.data}


func _options_put(s: Session, msg: Dictionary) -> Dictionary:
	var base: Variant = msg.get("base")
	var at: Variant = msg.get("at")
	var options: Variant = msg.get("options")
	if not (base is int and at is int and options is Dictionary):
		return _fail("options_put", "bad message")
	if JSON.stringify(options).length() > Protocol.MAX_OPTIONS:
		return _fail("options_put", "too big")
	var r: Array = accounts.store_put(s.user, "options", base, at, options)
	var entry: Dictionary = r[1]
	if r[0]:
		return {"t": "options_put", "ok": true, "rev": entry.rev}
	return {"t": "options_put", "ok": false, "err": "conflict",
		"rev": entry.rev, "at": entry.at, "options": entry.data}
