extends SceneTree
## Checks a running server end to end (CI): registers a random account, saves a hero and reads
## it back. Exit code 0 when it all worked.
##   godot --headless --path godot/client -s res://tools/net_check.gd -- HOST PORT CERT.crt

const Protocol := preload("res://scripts/net/protocol.gd")
const NetClient := preload("res://scripts/net/net_client.gd")


func _init() -> void:
	var a := OS.get_cmdline_user_args()
	if a.size() < 3:
		printerr("usage: -- HOST PORT CERT")
		quit(2)
		return
	var cert := X509Certificate.new()
	if cert.load(a[2]) != OK:
		printerr("cannot read %s" % a[2])
		quit(2)
		return
	var c := NetClient.new()
	c.open(a[0], int(a[1]), cert)
	var uid := ""
	for i in 8:
		uid += char(65 + randi() % 26)
	var got := []
	var keep := func(r: Dictionary) -> void: got.append(r)
	c.request({"t": "register", "id": uid, "pwd": "1234", "v": Protocol.VERSION}, keep)
	c.request({"t": "hero_put", "base": 0, "at": 1, "hero": {"hero_name": "Check"}}, keep)
	c.request({"t": "hero_get"}, keep)
	var t0 := Time.get_ticks_msec()
	while got.size() < 3 and Time.get_ticks_msec() - t0 < 15000:
		c.poll(10)
	c.close()
	print(got)
	var ok: bool = got.size() == 3 and got[0].ok and got[1].ok and got[2].get("hero") == {"hero_name": "Check"}
	print("net check: ", "ok" if ok else "FAILED")
	quit(0 if ok else 1)
