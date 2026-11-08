extends Node
## The server's entry, run without graphics:
##   godot --headless --path godot/client res://server/main.tscn -- [--port 28310]
##       [--bind *] [--data user://server] [--key server.key --cert server.crt]
## Without --key / --cert it makes a self-signed pair in the data folder on the first start
## (server.key, server.crt); the game trusts the certificate it is given (pow/net/cert).

const Protocol := preload("res://scripts/net/protocol.gd")
const GameServer := preload("res://server/game_server.gd")

var server := GameServer.new()


func _ready() -> void:
	var args := parse_args(OS.get_cmdline_user_args())
	var data := str(args.get("data", "user://server"))
	DirAccess.make_dir_recursive_absolute(data)
	var pair := load_or_make_cert(data, str(args.get("key", "")), str(args.get("cert", "")))
	if pair.is_empty():
		get_tree().quit(1)
		return
	server.log_line = func(s: String) -> void: print(s)
	var port := int(args.get("port", Protocol.PORT))
	var err := server.start(port, pair[0], pair[1], data, str(args.get("bind", "*")))
	if err != OK:
		printerr("cannot listen on UDP port %d: %s" % [port, error_string(err)])
		get_tree().quit(1)
		return
	print("listening on UDP %d (DTLS), data in %s" % [port, ProjectSettings.globalize_path(data)])


func _process(_delta: float) -> void:
	server.poll()


func _exit_tree() -> void:
	server.stop()


## --name value pairs after `--`.
static func parse_args(argv: PackedStringArray) -> Dictionary:
	var out := {}
	var i := 0
	while i < argv.size():
		var a := argv[i]
		if a.begins_with("--") and i + 1 < argv.size():
			out[a.substr(2)] = argv[i + 1]
			i += 2
		else:
			i += 1
	return out


## [key, cert] from the given files, or from / into the data folder.
static func load_or_make_cert(data: String, key_path: String, cert_path: String) -> Array:
	if key_path.is_empty() != cert_path.is_empty():
		printerr("give both --key and --cert")
		return []
	var key := CryptoKey.new()
	var cert := X509Certificate.new()
	if key_path.is_empty():
		key_path = data.path_join("server.key")
		cert_path = data.path_join("server.crt")
		if not FileAccess.file_exists(key_path):
			var crypto := Crypto.new()
			key = crypto.generate_rsa(2048)
			cert = crypto.generate_self_signed_certificate(key, "CN=localhost,O=Path of a Warrior,C=UA",
				"20250101000000", "20450101000000")
			key.save(key_path)
			cert.save(cert_path)
			print("made a self-signed certificate: %s" % ProjectSettings.globalize_path(cert_path))
			return [key, cert]
	if key.load(key_path) != OK or cert.load(cert_path) != OK:
		printerr("cannot read %s / %s" % [key_path, cert_path])
		return []
	return [key, cert]
