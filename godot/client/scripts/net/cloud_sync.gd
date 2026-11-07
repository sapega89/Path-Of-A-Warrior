extends RefCounted
## The hero kept on the server, as in pyport's "save only on the server": the hero lives in
## memory, every save goes to the server, and the game starts only online.
##
## step() is called every frame (scripts/net/cloud.gd). With an account it logs in, takes the
## server's hero (at the start the server's copy always wins) and sends every save, with the
## revision it was based on: when another device saved meanwhile, this device's copy wins and
## goes again on top of that revision. Without an account it only checks that the server is
## there (the game may start; the hero waits in memory until the registration). A lost
## connection is tried again after RETRY_MS, then twice as long each time, up to RETRY_MAX_MS.
## A hero saved in a file before (legacy) goes to the server when the account has none there
## yet; either way the file is then removed (purge_legacy).
##
## The Options (options_store: the Settings autoload) are kept on the device and on the server,
## as pyport keeps them: after each login the newer copy wins (the server's on a device the
## account is new to), and every change goes to the server; a conflict while playing is won
## by this device.

const NetClient := preload("res://scripts/net/net_client.gd")
const Protocol := preload("res://scripts/net/protocol.gd")

const RETRY_MS := 30000
const RETRY_MAX_MS := 300000

var address := "127.0.0.1"
var port := Protocol.PORT
var cert: X509Certificate
## Read into `cert` on the next try while `cert` is null (the local server makes it on its first
## start, maybe after the game).
var cert_path := ""
var clock: Callable = func() -> int: return Time.get_ticks_msec()

## [UserID, password], or [] without an account.
var account: Array = []
## idle, connecting (login sent), get, ready, off (the server refused the login), probe
var state := "idle"
var err := ""  # the last refusal: "password", "no account", "update"
var reachable := false  # no account: the server answered
var client := NetClient.new()

var hero: Variant = null  # the hero's dictionary, null: none yet
var rev := 0
var at := 0  # ms of the last save
var dirty := false  # saved here, not on the server yet
var in_flight := -1  # `at` of the save on its way, -1: none
var legacy: Variant = null  # a hero from the old save file
var purge_legacy := false  # the old file may go now
var started := false  # the game runs: a hero taken from the server now needs a restart
var restart_requested := false
var retry_at := 0
var retry_ms := RETRY_MS
var _first := true  # the first hero_get of this account
## The Options: cloud_values(), take_cloud(values), save_cloud() and `cloud`
## {user, rev, at, dirty}; null: only the hero.
var options_store: Object = null
var options_in_flight := -1  # `at` of the options on their way, -1: none
var _options_known := false  # the server's options were read since this login
var _losing := false  # _lost() is closing the connection


func setup(server_address: String, server_port: int, server_cert: X509Certificate) -> void:
	address = server_address
	port = server_port
	cert = server_cert


## The game may start: the hero came from the server, or there is no account yet and the
## server is there.
func online() -> bool:
	return reachable if account.is_empty() else state == "ready"


func refused() -> bool:
	return state == "off"


## A save of the game: sent when online, kept until then.
func save(d: Dictionary) -> void:
	hero = d.duplicate(true)
	at = maxi(int(clock.call()), at + 1)
	dirty = true


## Try now, not after the wait.
func retry_now() -> void:
	retry_at = 0
	retry_ms = RETRY_MS
	if state == "off":
		state = "idle"
	if client.state == NetClient.State.CLOSED:
		reachable = false


func use_account(id: String, pwd: String) -> void:
	if account == [id, pwd]:
		return
	account = [id, pwd]
	_first = true
	_drop()


func forget_account() -> void:
	account = []
	_drop()


func _drop(next := "idle") -> void:
	client.close()  # waiting requests get "offline"
	state = next
	in_flight = -1
	options_in_flight = -1
	_options_known = false


func _lost() -> void:
	if state == "off" or _losing or (state == "idle" and int(clock.call()) < retry_at):
		return  # lost already: another answer said "offline" too
	_losing = true
	_drop()
	_losing = false
	retry_at = int(clock.call()) + retry_ms
	retry_ms = mini(RETRY_MAX_MS, retry_ms * 2)


func _open() -> bool:
	if client.state != NetClient.State.CLOSED:
		return true
	if int(clock.call()) < retry_at:
		return false
	if _connect() != OK:
		_lost()
		return false
	return true


## Opens the connection; an error while the server's certificate cannot be read yet.
func _connect() -> int:
	if cert == null and not cert_path.is_empty() and FileAccess.file_exists(cert_path):
		var c := X509Certificate.new()
		if c.load(cert_path) == OK:
			cert = c
	if cert == null:
		return ERR_FILE_NOT_FOUND
	return client.open(address, port, cert)


func step() -> void:
	if account.is_empty():
		if not reachable and _open():
			if state != "probe":
				state = "probe"
				client.request({"t": "hello"}, _probe_answer)
			client.poll()
		return
	if state == "off":
		return
	if state == "idle" or state == "probe":
		if not _open():
			return
		state = "connecting"
		client.request({"t": "login", "id": account[0], "pwd": account[1], "v": Protocol.VERSION},
			_login_answer)
	client.poll()
	if state == "ready":
		_push()
		_push_options()


func _probe_answer(r: Dictionary) -> void:
	if r.get("err") == "offline":
		_lost()
		return
	reachable = true  # any answer: the server is there
	retry_ms = RETRY_MS


func _login_answer(r: Dictionary) -> void:
	if r.get("ok", false):
		_logged_in()
	elif r.get("err") == "offline":
		_lost()
	else:
		err = str(r.get("err", ""))
		_drop("off")


func _logged_in() -> void:
	retry_ms = RETRY_MS
	state = "get"
	client.request({"t": "hero_get"}, _get_answer)
	if options_store != null:
		client.request({"t": "options_get"}, _options_get_answer)


## Registers a new account on the server; done(answer) once it is known. On "ok" the account is
## this device's and its session is logged in.
func register(id: String, pwd: String, done: Callable) -> void:
	if client.state == NetClient.State.CLOSED and _connect() != OK:
		done.call({"t": "register", "ok": false, "err": "offline"})
		return
	state = "connecting"
	client.request({"t": "register", "id": id, "pwd": pwd, "v": Protocol.VERSION},
		func(r: Dictionary) -> void:
			if r.get("ok", false):
				account = [id, pwd]
				_first = true
				_logged_in()
			elif r.get("err") == "offline":
				_lost()
			else:
				state = "idle" if account.is_empty() else state
			done.call(r))


func _get_answer(r: Dictionary) -> void:
	if not r.get("ok", false):
		_lost()
		return
	var s_rev := int(r.get("rev", 0))
	var s_hero: Variant = r.get("hero")
	if s_hero is Dictionary:
		purge_legacy = legacy != null
		if (_first and not dirty) or (s_rev > rev and not (dirty and at > int(r.get("at", 0)))):
			_take(s_hero, s_rev)
		else:
			rev = s_rev  # ours is newer (or made before the registration): ours goes on top
	else:
		rev = 0
		if hero == null and legacy != null:
			hero = legacy
			at = maxi(int(clock.call()), 1)
			dirty = true
		elif hero != null:
			dirty = true  # a new account, or the server lost it: send ours
	_first = false
	state = "ready"


func _take(d: Dictionary, s_rev: int) -> void:
	hero = d
	rev = s_rev
	dirty = false
	if started:
		restart_requested = true


func _push() -> void:
	if not dirty or in_flight >= 0 or hero == null:
		return
	in_flight = at
	client.request({"t": "hero_put", "base": rev, "at": at, "hero": hero}, _put_answer)


func _put_answer(r: Dictionary) -> void:
	var sent := in_flight
	in_flight = -1
	if r.get("ok", false):
		rev = int(r.rev)
		if at == sent:
			dirty = false
		if legacy != null:
			purge_legacy = true
	elif r.get("err") == "conflict":
		rev = int(r.get("rev", rev))  # another device saved: this one's copy goes on top
	elif r.get("err") == "offline":
		_lost()
	else:
		push_warning("cloud: hero not saved (%s)" % r.get("err"))
		dirty = false


## Nothing waits to be sent.
func idle() -> bool:
	return not dirty and in_flight < 0 and (options_store == null
		or not options_store.cloud.dirty and options_in_flight < 0)


func _options_get_answer(r: Dictionary) -> void:
	if not r.get("ok", false):
		if r.get("err") == "offline":
			_lost()
		return
	var m: Dictionary = options_store.cloud
	var s_rev := int(r.get("rev", 0))
	var s_at := int(r.get("at", 0))
	var theirs: Variant = r.get("options")
	if not theirs is Dictionary:
		m.rev = 0
		m.dirty = true  # nothing on the server yet: ours go
	elif str(m.user) != str(account[0]) or (s_rev > int(m.rev)
			and not (m.dirty and int(m.at) > s_at)):
		options_store.take_cloud(theirs)
		m.rev = s_rev
		m.at = s_at
		m.dirty = false
	elif s_rev != int(m.rev):
		m.rev = s_rev  # ours are newer, or the server lost them: ours go on top
		m.dirty = true
	m.user = str(account[0])
	options_store.save_cloud()
	_options_known = true


func _push_options() -> void:
	if options_store == null or not _options_known or options_in_flight >= 0:
		return
	var m: Dictionary = options_store.cloud
	if not m.dirty:
		return
	options_in_flight = int(m.at)
	client.request({"t": "options_put", "base": int(m.rev), "at": int(m.at),
		"options": options_store.cloud_values()}, _options_put_answer)


func _options_put_answer(r: Dictionary) -> void:
	var sent := options_in_flight
	options_in_flight = -1
	var m: Dictionary = options_store.cloud
	if r.get("ok", false):
		m.rev = int(r.rev)
		if int(m.at) == sent:
			m.dirty = false
	elif r.get("err") == "conflict":
		m.rev = int(r.get("rev", m.rev))  # another device changed them: ours go on top
	elif r.get("err") == "offline":
		_lost()
		return
	else:
		push_warning("cloud: options not saved (%s)" % r.get("err"))
		m.dirty = false
	options_store.save_cloud()


## A save still has to reach the server and the connection is up or coming up: worth
## waiting for when the game quits.
func flushing() -> bool:
	return not account.is_empty() and state != "off" and client.state != NetClient.State.CLOSED \
		and not idle()
