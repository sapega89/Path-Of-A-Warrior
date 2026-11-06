extends Node
## Autoload "Cloud": always online, the hero only on the server (scripts/net/cloud_sync.gd).
##
## On when the game knows its server: command line `-- --server HOST:PORT --cert FILE.crt`,
## or the project settings pow/net/server and pow/net/cert. Off (no server given, as in the
## tests and the screenshots) the hero stays in user://hero.json as before.
## The account (UserID + password) stays on this device in user://account.cfg.
## Live (scripts/net/live_client.gd) and the online game (scripts/net/online_client.gd) go
## over the same logged-in connection (request()); the server's pushes go to the online game.

const CloudSync := preload("res://scripts/net/cloud_sync.gd")
const LiveClient := preload("res://scripts/net/live_client.gd")
const OnlineClient := preload("res://scripts/net/online_client.gd")
const Protocol := preload("res://scripts/net/protocol.gd")
const ACCOUNT_PATH := "user://account.cfg"
const LEGACY_PATH := "user://hero.json"

var sync: CloudSync = null
var live: LiveClient = null
var mp: OnlineClient = null  # the online game, while connected
var account_path := ACCOUNT_PATH


func _ready() -> void:
	var cfg := server_config(OS.get_cmdline_user_args())
	if cfg.is_empty():
		return
	start(cfg.address, cfg.port, cfg.cert)


## {address, port, cert} of the server, or {} when the game has none.
static func server_config(argv: PackedStringArray) -> Dictionary:
	var server := str(ProjectSettings.get_setting("pow/net/server", ""))
	var cert_path := str(ProjectSettings.get_setting("pow/net/cert", ""))
	for i in argv.size() - 1:
		if argv[i] == "--server":
			server = argv[i + 1]
		elif argv[i] == "--cert":
			cert_path = argv[i + 1]
	if server.is_empty() or cert_path.is_empty():
		return {}
	var cert := X509Certificate.new()
	if cert.load(cert_path) != OK:
		push_error("cloud: cannot read the server's certificate %s" % cert_path)
		return {}
	var port := Protocol.PORT
	var address := server
	if server.contains(":"):
		address = server.get_slice(":", 0)
		port = int(server.get_slice(":", 1))
	return {"address": address, "port": port, "cert": cert}


func start(address: String, port: int, cert: X509Certificate) -> void:
	sync = CloudSync.new()
	sync.setup(address, port, cert)
	live = LiveClient.new(request)
	mp = OnlineClient.new(request)
	mp.on_battle = func() -> void: Router.push("online_battle")
	sync.client.on_push = _push
	sync.options_store = Settings
	var acc := load_account()
	if not acc.is_empty():
		sync.account = acc
	if FileAccess.file_exists(LEGACY_PATH):
		var v: Variant = JSON.parse_string(FileAccess.get_file_as_string(LEGACY_PATH))
		if v is Dictionary:
			sync.legacy = v


func stop() -> void:
	if sync != null:
		sync.client.close()
	sync = null
	live = null
	mp = null


func enabled() -> bool:
	return sync != null


func online() -> bool:
	return sync != null and sync.online()


func refused() -> bool:
	return sync != null and sync.refused()


func has_account() -> bool:
	return sync != null and not sync.account.is_empty()


## The hero's dictionary from the server (or saved since), null when there is none.
func hero() -> Variant:
	return null if sync == null else sync.hero


## One request over the logged-in connection, done(answer); offline: {ok: false, err: "offline"}.
func request(msg: Dictionary, done: Callable) -> void:
	if not online():
		done.call({"t": msg.get("t", "?"), "ok": false, "err": "offline"})
		return
	sync.client.request(msg, done)


func _push(m: Dictionary) -> void:
	if mp != null:
		mp.on_push(m)


func save_hero(d: Dictionary) -> void:
	if sync != null:
		sync.save(d)


## The game is past its start: a newer hero from the server now means a restart.
func game_started() -> void:
	if sync != null:
		sync.started = true


func retry_now() -> void:
	if sync != null:
		sync.retry_now()


## done(answer): ok, or err "taken", "bad id", "limit", "update", "offline".
func register(id: String, pwd: String, done: Callable) -> void:
	if sync == null:
		done.call({"ok": false, "err": "offline"})
		return
	sync.register(id, pwd, func(r: Dictionary) -> void:
		if r.get("ok", false):
			save_account(id, pwd)
		done.call(r))


## "Login refused" > BACK: the stored account goes; the game asks for one again.
func forget_account() -> void:
	DirAccess.remove_absolute(account_path)
	if sync != null:
		sync.forget_account()


func load_account() -> Array:
	var cf := ConfigFile.new()
	if cf.load(account_path) != OK:
		return []
	var id: Variant = cf.get_value("account", "id", "")
	var pwd: Variant = cf.get_value("account", "pwd", "")
	if Protocol.valid_id(id) and Protocol.valid_password(pwd):
		return [id, pwd]
	return []


func save_account(id: String, pwd: String) -> void:
	var cf := ConfigFile.new()
	cf.set_value("account", "id", id)
	cf.set_value("account", "pwd", pwd)
	cf.save(account_path)


func _process(_delta: float) -> void:
	if sync == null:
		return
	sync.step()
	if sync.purge_legacy:
		sync.purge_legacy = false
		sync.legacy = null
		DirAccess.remove_absolute(LEGACY_PATH)
	if sync.restart_requested:
		sync.restart_requested = false
		sync.started = false
		Router.go("main_menu")  # the hero in memory was the old one


func _exit_tree() -> void:
	stop()
