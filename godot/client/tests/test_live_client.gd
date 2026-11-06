extends "res://tests/test_case.gd"
## Live on this device (scripts/net/live_client.gd) and its screens, against the server's Live
## (server/live.gd) in this process.

const LiveClient := preload("res://scripts/net/live_client.gd")
const Live := preload("res://server/live.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Items := preload("res://scripts/core/items.gd")
const ServerTests := preload("res://tests/test_server.gd")
const WarehouseScreen := preload("res://scripts/screens/live_warehouse_screen.gd")
const SafeScreen := preload("res://scripts/screens/live_safe_screen.gd")
const LiveScreen := preload("res://scripts/screens/live_screen.gd")
const TEST_PATH := "user://test_live_client_hero.json"


func _dir() -> String:
	var d := "user://test_server_live_client_%d" % randi()
	DirAccess.make_dir_recursive_absolute(d)
	return d


## A client whose requests the server's Live answers at once, for UserID ANDREY.
func _client(d: String) -> Array:
	var l := Live.new(d)
	l.rng.seed = 7
	l.clock = func() -> float: return 1000.0
	var s := Live.Session.new()
	s.user = "ANDREY"
	var c := LiveClient.new(func(msg: Dictionary, done: Callable) -> void:
		var r := l.answer(s, str(msg.t), bytes_to_var(var_to_bytes(msg)))  # as over the wire
		done.call(bytes_to_var(var_to_bytes(r))))
	return [c, l, s]


func _hero(gold := 500) -> RefCounted:
	var p := Profile.new()
	p.gold = gold
	p.add_item(Items.make(101))
	p.add_item(Items.make(131))
	return p


func test_sync_sends_the_backpack_with_a_serial_per_place() -> void:
	var d := _dir()
	var t := _client(d)
	var c: RefCounted = t[0]
	var p := _hero()
	var got := []
	c.sync(p, func(err): got.append(err))
	eq(got, [""], "synced")
	check(c.synced)
	eq(c.serials.slice(0, 3), [1, 2, 0], "a serial for each thing")
	eq(t[2].gold, 500, "the hero's gold on the server")
	eq(t[2].backpack.keys(), [1, 2])
	ServerTests._rm(d)


func test_into_the_warehouse_and_back() -> void:
	var d := _dir()
	var t := _client(d)
	var c: RefCounted = t[0]
	var p := _hero()
	c.sync(p, func(_e): pass)
	var got := []
	c.store(p, 0, func(err): got.append(err))
	eq(got, [""], "stored")
	eq(int(p.backpack[0].id), 0, "out of the backpack")
	eq(c.warehouse.size(), 1)
	eq(int(c.warehouse[0].item.id), 101, "in the Warehouse")
	eq(t[1].user("ANDREY").warehouse.size(), 1, "on the server")
	c.store(p, 0, func(err): got.append(err))
	eq(got[-1], "gone", "nothing there any more")
	c.take(p, 0, func(err): got.append(err))
	eq(got[-1], "", "taken back")
	eq(int(p.backpack[0].id), 101, "into the first free place")
	check(int(c.serials[0]) >= 1000, "with the serial the server gave it")
	eq(c.warehouse.size(), 0)
	c.store(p, 0, func(err): got.append(err))
	eq(got[-1], "", "that serial works")
	ServerTests._rm(d)


func test_a_full_backpack_takes_nothing() -> void:
	var d := _dir()
	var t := _client(d)
	var c: RefCounted = t[0]
	var p := _hero()
	c.sync(p, func(_e): pass)
	c.store(p, 0, func(_e): pass)
	for i in p.backpack.size():
		if int(p.backpack[i].id) == 0:
			p.backpack[i] = Items.make(106)
	c.sync(p, func(_e): pass)
	var got := []
	c.take(p, 0, func(err): got.append(err))
	eq(got, ["full"])
	eq(c.warehouse.size(), 1, "still in the Warehouse")
	ServerTests._rm(d)


func test_gold_into_the_safe_and_out() -> void:
	var d := _dir()
	var t := _client(d)
	var c: RefCounted = t[0]
	var p := _hero(500)
	c.sync(p, func(_e): pass)
	var got := []
	c.move_gold(p, true, 600, func(err): got.append(err))
	eq(got, ["gold"], "more than the hero has")
	c.move_gold(p, true, 200, func(err): got.append(err))
	eq([got[-1], int(p.gold), c.safe], ["", 300, 200], "into the Safe")
	c.move_gold(p, false, 50, func(err): got.append(err))
	eq([got[-1], int(p.gold), c.safe], ["", 350, 150], "and out")
	ServerTests._rm(d)


func test_offline_every_call_says_so() -> void:
	var c := LiveClient.new(func(msg: Dictionary, done: Callable) -> void:
		done.call({"t": msg.t, "ok": false, "err": "offline"}))
	var got := []
	c.sync(_hero(), func(err): got.append(err))
	eq(got, ["offline"])
	check(not c.synced)
	check(not c.busy, "not waiting any more")


func test_warehouse_screen() -> void:
	var d := _dir()
	var t := _client(d)
	_hero().save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH, "live": t[0]}
	var screen: Control = WarehouseScreen.new()
	root.add_child(screen)
	check(screen.cells[0].icon != null, "the backpack first")
	eq(screen.count.text, "2 / 45")
	check(screen.press_cell(0), "into the Warehouse")
	check(screen.cells[0].icon == null, "gone from the backpack")
	eq(int(Profile.load_or_new(TEST_PATH).backpack[0].id), 0, "the hero saved")
	screen.show_side(true)
	eq(screen.count.text, "1 / 200")
	eq(int(screen.item_at(0).id), 101)
	check(screen.press_cell(0), "back into the backpack")
	eq(int(Profile.load_or_new(TEST_PATH).backpack[0].id), 101, "saved again")
	check(not screen.press_cell(0), "an empty place does nothing")
	screen.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))
	ServerTests._rm(d)


func test_safe_screen() -> void:
	var d := _dir()
	var t := _client(d)
	_hero(500).save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH, "live": t[0]}
	var screen: Control = SafeScreen.new()
	root.add_child(screen)
	eq([screen.local.text, screen.server.text], ["500", "0"])
	check(not screen.submit(), "nothing in the Safe to take out")
	eq(screen.info.text, tr("live.no_safe_gold"))
	screen.turn()
	screen.amount.text = "9999"
	screen._typed(screen.amount.text)
	eq(screen.amount.text, "500", "no more than the hero has")
	screen.amount.text = "120"
	check(screen.submit(), "into the Safe")
	eq([screen.local.text, screen.server.text], ["380", "120"])
	eq(int(Profile.load_or_new(TEST_PATH).gold), 380, "the hero saved")
	screen.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))
	ServerTests._rm(d)


func test_live_menu_opens_its_pages_once_synced() -> void:
	var d := _dir()
	var t := _client(d)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH, "live": t[0]}
	var screen: Control = LiveScreen.new()
	root.add_child(screen)
	eq(screen.status.text, "", "connected")
	eq(screen.buttons.map(func(b): return b.disabled), [true, false, false, true],
		"Warehouse and Safe (Trade and Multiplayer not yet)")
	screen.free()
	Router.params = {"profile_path": TEST_PATH}
	screen = LiveScreen.new()
	root.add_child(screen)
	eq(screen.status.text, tr("live.failed"), "offline: no Live")
	check(screen.buttons.all(func(b): return b.disabled))
	screen.free()
	Router.params = old
	ServerTests._rm(d)
