extends Node
## The connection to the game server (godot/server): JSON requests over WebSocket, each
## answered by the message with its id (godot/server/game_server/protocol.py). Logs in as a
## guest of this device: a random device key made once and the server's token, both kept in
## user://account.cfg. Add it to the tree (it polls in _process) and `await ask(...)`; or
## call ask_now(...) where nothing may wait for frames (tests).

signal answered(msg: Dictionary)

const VERSION := 1
const ACCOUNT_PATH := "user://account.cfg"
const TIMEOUT_MS := 8000

var url := ""
var account_path := ACCOUNT_PATH
var account := ""
var peer := WebSocketPeer.new()
var _next_id := 1


## Opens the connection. False when the address is wrong.
func open(server_url: String) -> bool:
	url = server_url
	peer = WebSocketPeer.new()
	return peer.connect_to_url(url) == OK


func is_open() -> bool:
	return peer.get_ready_state() == WebSocketPeer.STATE_OPEN


func close() -> void:
	peer.close()


func _process(_delta: float) -> void:
	poll()


## Reads what came; every answer is emitted with `answered`.
func poll() -> Array:
	peer.poll()
	var got: Array = []
	while peer.get_ready_state() == WebSocketPeer.STATE_OPEN and peer.get_available_packet_count() > 0:
		var msg: Variant = JSON.parse_string(peer.get_packet().get_string_from_utf8())
		if typeof(msg) == TYPE_DICTIONARY:
			got.append(msg)
			answered.emit(msg)
	return got


func _send(type: String, fields: Dictionary) -> int:
	var id := _next_id
	_next_id += 1
	var msg := fields.duplicate()
	msg["type"] = type
	msg["id"] = id
	msg["v"] = VERSION
	peer.send_text(JSON.stringify(msg))
	return id


## The answer to a request, or {type: "error", code: "offline" | "timeout"}.
func ask(type: String, fields: Dictionary = {}) -> Dictionary:
	if not await _wait_open():
		return {"type": "error", "code": "offline"}
	var id := _send(type, fields)
	var start := Time.get_ticks_msec()
	while Time.get_ticks_msec() - start < TIMEOUT_MS:
		var msg: Dictionary = await answered
		if int(msg.get("id", -1)) == id:
			return msg
	return {"type": "error", "code": "timeout"}


func _wait_open() -> bool:
	var start := Time.get_ticks_msec()
	while peer.get_ready_state() == WebSocketPeer.STATE_CONNECTING and Time.get_ticks_msec() - start < TIMEOUT_MS:
		await get_tree().process_frame
	return is_open()


## ask() without the scene tree: polls and sleeps until the answer comes.
func ask_now(type: String, fields: Dictionary = {}) -> Dictionary:
	var start := Time.get_ticks_msec()
	while peer.get_ready_state() == WebSocketPeer.STATE_CONNECTING and Time.get_ticks_msec() - start < TIMEOUT_MS:
		peer.poll()
		OS.delay_msec(5)
	if not is_open():
		return {"type": "error", "code": "offline"}
	var id := _send(type, fields)
	while Time.get_ticks_msec() - start < TIMEOUT_MS:
		for msg in poll():
			if int(msg.get("id", -1)) == id:
				return msg
		OS.delay_msec(5)
	return {"type": "error", "code": "timeout"}


## The login request of this device: with the saved token, or as a guest the first time.
func login_request() -> Array:
	var cfg := ConfigFile.new()
	cfg.load(account_path)
	var token := str(cfg.get_value("account", "token", ""))
	account = str(cfg.get_value("account", "id", ""))
	if not token.is_empty() and not account.is_empty():
		return ["login", {"account": account, "token": token}]
	return ["guest_login", {"device": device_key()}]


## Keeps what a login answered (a guest login gives the account and a new token).
func login_answered(msg: Dictionary) -> bool:
	if str(msg.get("type", "")) == "guest_login_ok":
		var cfg := ConfigFile.new()
		cfg.load(account_path)
		cfg.set_value("account", "id", str(msg.account))
		cfg.set_value("account", "token", str(msg.token))
		cfg.save(account_path)
	if str(msg.get("type", "")) in ["login_ok", "guest_login_ok"]:
		account = str(msg.account)
		return true
	return false


## Logs in (await). On a stale token logs in again as the guest of this device.
func login() -> bool:
	var r: Array = login_request()
	var msg: Dictionary = await ask(r[0], r[1])
	if str(msg.get("code", "")) == "login":
		msg = await ask("guest_login", {"device": device_key()})
	return login_answered(msg)


func login_now() -> bool:
	var r: Array = login_request()
	var msg: Dictionary = ask_now(r[0], r[1])
	if str(msg.get("code", "")) == "login":
		msg = ask_now("guest_login", {"device": device_key()})
	return login_answered(msg)


## This device's key: random, made once.
func device_key() -> String:
	var cfg := ConfigFile.new()
	cfg.load(account_path)
	var key := str(cfg.get_value("account", "device", ""))
	if key.length() < 16:
		var rng := RandomNumberGenerator.new()
		rng.randomize()
		key = ""
		for i in 32:
			key += "%x" % rng.randi_range(0, 15)
		cfg.set_value("account", "device", key)
		cfg.save(account_path)
	return key
