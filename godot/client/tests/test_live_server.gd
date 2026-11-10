extends "res://tests/test_case.gd"
## Live on the server (server/live.gd): Safe, Warehouse, Trade, as pyport's pow_server/live.py.

const ServerTests := preload("res://tests/test_server.gd")


func _dir() -> String:
	var d := "user://test_server_live_%d" % randi()
	DirAccess.make_dir_recursive_absolute(d)
	return d


func _live(d: String) -> LiveServer:
	var l := LiveServer.new(d)
	l.rng.seed = 7
	l.clock = func() -> float: return 1000.0
	return l


func _session(uid: String, gold := 0, backpack: Array = []) -> LiveServer.Session:
	var s := LiveServer.Session.new()
	s.user = uid
	s.gold = gold
	for i in backpack.size():
		s.backpack[i + 1] = backpack[i]
	return s


func test_npc_stock_has_every_kind_and_the_two_that_never_run_out() -> void:
	var d := _dir()
	var l := _live(d)
	var lots: Array = l.market().lots
	check(lots.size() > 50, "a full stock (%d lots)" % lots.size())
	var towel := lots.filter(func(x): return int(x.item.id) == 502)
	eq(towel.size(), 1, "Silk Rushnyk for sale")
	eq(int(towel[0].price), 3000)
	check(towel[0].forever, "it never runs out")
	check(lots.all(func(x): return LiveServer.for_sale(int(x.item.id))), "no elixirs or potions")
	check(lots.all(func(x): return str(x.seller).is_empty()), "all NPC lots")
	ServerTests._rm(d)


func test_safe_and_warehouse() -> void:
	var d := _dir()
	var l := _live(d)
	var s := _session("ANDREY", 500, [Items.make(101)])
	var r := l.answer(
		s, "live_sync", {"gold": 500, "backpack": [{"serial": 1, "item": Items.make(101)}]}
	)
	eq([r.ok, r.safe, r.warehouse], [true, 0, []])
	eq(
		l.answer(s, "live_safe", {"to_safe": true, "amount": 600}).err,
		"gold",
		"more than the hero has"
	)
	r = l.answer(s, "live_safe", {"to_safe": true, "amount": 200})
	eq([r.gold, r.safe], [300, 200], "into the Safe")
	r = l.answer(s, "live_store", {"to_warehouse": true, "serial": 1})
	check(r.ok, "into the Warehouse")
	eq(s.backpack.size(), 0)
	var again := _live(d)  # as after a restart
	eq(int(again.user("ANDREY").safe), 200, "the Safe is kept")
	eq(again.user("ANDREY").warehouse.size(), 1, "the Warehouse too")
	r = l.answer(s, "live_store", {"to_warehouse": false, "serial": r.serial})
	check(r.ok and s.backpack.has(r.serial), "back into the backpack")
	ServerTests._rm(d)


func test_sell_buy_tax_and_the_sale_list() -> void:
	var d := _dir()
	var l := _live(d)
	var seller := _session("SELLER", 0, [Items.make(101)])
	eq(l.answer(seller, "live_sell", {"serial": 1, "price": 0}).err, "price")
	check(l.answer(seller, "live_sell", {"serial": 1, "price": 1000}).ok, "on sale")
	var mine: Dictionary = l.answer(seller, "live_mine", {})
	eq(mine.lots.size(), 1)
	var lot: int = mine.lots[0].lot
	eq(l.answer(seller, "live_buy", {"lot": lot}).err, "own", "not one's own")
	var buyer := _session("BUYER", 900)
	eq(l.answer(buyer, "live_buy", {"lot": lot}).err, "gold", "too dear")
	buyer.gold = 1500
	var r := l.answer(buyer, "live_buy", {"lot": lot})
	check(r.ok, "bought")
	eq(r.gold, 500)
	eq(int(buyer.backpack[r.serial].id), 101, "in the buyer's backpack")
	eq(int(l.user("SELLER").safe), 900, "the price less 10% tax in the seller's Safe")
	check(l.answer(seller, "live_status", {}).sold, "something was sold")
	var sold: Dictionary = l.answer(seller, "live_sold", {})
	eq([int(sold.sold[0].item.id), int(sold.sold[0].price)], [101, 1000], "the Sale List")
	eq(l.answer(seller, "live_sold", {}).sold, [], "read once")
	eq(l.answer(buyer, "live_buy", {"lot": lot}).err, "gone", "sold already")
	ServerTests._rm(d)


func test_five_lots_at_most_and_cancel() -> void:
	var d := _dir()
	var l := _live(d)
	var things := []
	for i in 6:
		things.append(Items.make(101))
	var s := _session("ANDREY", 0, things)
	for i in 5:
		check(l.answer(s, "live_sell", {"serial": i + 1, "price": 10}).ok)
	eq(l.answer(s, "live_sell", {"serial": 6, "price": 10}).err, "limit", "5 per player")
	var lot: int = l.answer(s, "live_mine", {}).lots[0].lot
	var r := l.answer(s, "live_cancel", {"lot": lot, "to_warehouse": true})
	check(r.ok, "taken back")
	eq(l.user("ANDREY").warehouse.size(), 1, "into the Warehouse")
	eq(l.answer(s, "live_cancel", {"lot": lot}).err, "gone")
	ServerTests._rm(d)


func test_elixirs_cannot_be_sold() -> void:
	var d := _dir()
	var l := _live(d)
	var s := _session("ANDREY", 0, [Items.make(434)])
	eq(l.answer(s, "live_sell", {"serial": 1, "price": 10}).err, "not for sale")
	ServerTests._rm(d)


func test_buy_menu_counts_and_pages() -> void:
	var d := _dir()
	var l := _live(d)
	var s := _session("ANDREY", 10)
	var counts: Array = l.answer(s, "live_counts", {"cat": 2, "kind": 1}).counts
	eq(counts[0], 1, "one Silk Rushnyk (rare kind 1)")
	var page := l.answer(s, "live_page", {"cat": 2, "kind": 1, "enchant": 0, "page": 0})
	eq(int(page.lots[0].item.id), 502)
	eq(
		l.answer(s, "live_page", {"cat": 2, "kind": 1, "enchant": 0, "page": 1}).err,
		"none",
		"no second page"
	)
	check(l.answer(s, "live_prices", {"cat": 0, "kind": 0}).ok, "price info")
	ServerTests._rm(d)


func test_live_needs_a_login_on_the_server() -> void:
	var d := _dir()
	var srv := GameServer.new()
	srv.accounts = Accounts.new(d.path_join("accounts"))
	srv.accounts.rounds = 20
	srv.live = _live(d)
	var a := GameServer.Session.new()
	eq(srv.answer(a, {"t": "live_status"}).err, "login first")
	check(srv.answer(a, {"t": "register", "id": "ANDREY", "pwd": "1234", "v": Protocol.VERSION}).ok)
	eq(srv.answer(a, {"t": "live_status", "q": 3}).q, 3, "answered")
	check(srv.answer(a, {"t": "live_sync", "gold": 5, "backpack": []}).ok)
	eq(srv.answer(a, {"t": "live_sync", "gold": "5", "backpack": []}).err, "bad message")
	ServerTests._rm(d)
