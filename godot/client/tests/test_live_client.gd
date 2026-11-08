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
const MainMenu := preload("res://scripts/screens/main_menu.gd")
const GameMenu := preload("res://scripts/screens/game_menu.gd")
const BuyScreen := preload("res://scripts/screens/live_buy_screen.gd")
const SellScreen := preload("res://scripts/screens/live_sell_screen.gd")
const CancelScreen := preload("res://scripts/screens/live_cancel_screen.gd")
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
	return _player(l, "ANDREY")


## Another player's client on the same server.
func _player(l: Live, uid: String) -> Array:
	var s := Live.Session.new()
	s.user = uid
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


func test_game_menu_has_the_game_and_the_main_menu_the_rest() -> void:
	var d := _dir()
	var t := _client(d)
	_hero().save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH, "live": t[0]}
	var screen: Control = GameMenu.new()
	root.add_child(screen)
	eq(screen.buttons.map(func(b): return str(b.name)), ["Missions", "Management", "Blacksmith",
		"Visiting", "Trade", "Warehouse", "Safe", "Help"])
	eq(screen.online.buttons.map(func(b): return str(b.name)), ["Duel", "OnlineMissions", "Character",
		"Ranking", "Order", "Chat", "Invitations"], "the multiplayer pages in the same menu")
	check(t[0].synced and screen.news.done, "Live synced, nothing new")
	check(screen.menu.visible)
	screen.free()
	Router.params = {"profile_path": TEST_PATH}
	screen = GameMenu.new()
	root.add_child(screen)
	check(screen.news == null, "offline: nothing asked")
	screen.free()
	screen = MainMenu.new()
	root.add_child(screen)
	var names: Array = screen.buttons.map(func(b): return str(b.name))
	eq(names.slice(0, 4), ["Play", "NewGame", "Endings", "Settings"])
	screen.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))
	ServerTests._rm(d)


func test_sell_buy_and_cancel() -> void:
	var d := _dir()
	var t := _client(d)
	var seller: RefCounted = t[0]
	var b := _player(t[1], "BUYER")
	var buyer: RefCounted = b[0]
	var p := _hero(0)
	seller.sync(p, func(_e): pass)
	var got := []
	seller.sell(p, false, 1, 0, func(e): got.append(e))
	eq(got[-1], "price", "no price")
	seller.sell(p, false, 1, 10, func(e): got.append(e))
	eq(got[-1], "", "on sale")
	eq(int(p.backpack[1].id), 0, "out of the backpack")
	seller.ask_mine(func(e): got.append(e))
	eq(seller.lots.size(), 1, "my lot")
	var q := _hero(1000)
	buyer.sync(q, func(_e): pass)
	buyer.ask_counts(LiveClient.category(131), LiveClient.kind(131), func(e): got.append(e))
	check(int(buyer.counts[0]) >= 1, "counted at enchant 0")
	buyer.ask_page(LiveClient.category(131), LiveClient.kind(131), 0, 0, func(e): got.append(e))
	var mine: Array = buyer.lots.filter(func(x): return int(x.price) == 10)
	eq(mine.size(), 1, "the seller's lot on the page")
	buyer.buy(q, mine[0], false, func(e): got.append(e))
	eq(got[-1], "", "bought")
	eq(int(q.gold), 990)
	eq(int(q.backpack[2].id), 131, "into the first free place")
	eq(int(t[1].user("ANDREY").safe), 9, "the price less 10% in the seller's Safe")
	seller.ask_mine(func(e): got.append(e))
	eq(got[-1], "none", "nothing on sale any more")
	seller.sell(p, false, 0, 50, func(e): got.append(e))
	seller.ask_mine(func(e): got.append(e))
	seller.cancel(p, seller.lots[0], func(e): got.append(e))
	eq(got[-1], "", "taken back")
	eq(int(p.backpack[0].id), 101, "into the backpack")
	ServerTests._rm(d)


func test_elixirs_and_the_warehouse_on_sale() -> void:
	var d := _dir()
	var t := _client(d)
	var c: RefCounted = t[0]
	var p := _hero()
	p.backpack[2] = Items.make(434)
	c.sync(p, func(_e): pass)
	var got := []
	c.sell(p, false, 2, 10, func(e): got.append(e))
	eq(got, ["not for sale"], "an elixir")
	c.store(p, 0, func(_e): pass)
	c.sell(p, true, 0, 10, func(e): got.append(e))
	eq(got[-1], "", "from the Warehouse")
	eq(c.warehouse.size(), 0)
	c.ask_prices(0, LiveClient.kind(101), func(e): got.append(e))
	eq(got[-1], "", "price info")
	check(c.lots.size() > 0)
	check(c.lots.all(func(x): return LiveClient.kind(int(x.item.id)) == LiveClient.kind(101)), "of that kind")
	ServerTests._rm(d)


func test_buy_screen() -> void:
	var d := _dir()
	var t := _client(d)
	var p := _hero(10000)
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH, "live": t[0]}
	var screen: Control = BuyScreen.new()
	root.add_child(screen)
	eq(screen.step, BuyScreen.Step.CATEGORY)
	screen.choose_category(2)
	eq(screen.step, BuyScreen.Step.KIND)
	eq(screen.cells.size(), 18, "the Rare kinds")
	screen.choose_kind(1)  # 502 Silk Rushnyk: always for sale
	eq(screen.step, BuyScreen.Step.LOTS, "Rare: straight to the lots")
	eq(int(screen.live.lots[0].item.id), 502)
	check(screen.press_lot(0).contains("3000"), "asks: %s" % screen.ask.dialog_text)
	screen.ask.hide()
	screen.confirm()
	eq(int(screen.profile.gold), 7000, "bought")
	eq(int(Profile.load_or_new(TEST_PATH).gold), 7000, "the hero saved")
	check(Profile.load_or_new(TEST_PATH).has_item(502), "with the towel")
	eq(screen.step, BuyScreen.Step.LOTS, "the towel is still there")
	screen.go_back()
	screen.go_back()
	screen.choose_category(0)
	screen.choose_kind(0)
	eq(screen.step, BuyScreen.Step.ENCHANT, "Normal: the enchant levels")
	eq(screen.cells.size(), 10)
	screen.choose_enchant(9)
	eq(screen.info.text, tr("live.no_items"), "none at +9")
	screen.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))
	ServerTests._rm(d)


func test_sell_and_cancel_screens() -> void:
	var d := _dir()
	var t := _client(d)
	_hero().save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH, "live": t[0]}
	var screen: Control = SellScreen.new()
	root.add_child(screen)
	check(screen.pick(0), "the sword picked")
	eq(screen.step, SellScreen.Step.PRICE)
	screen.price.text = "x12a"
	screen._typed(screen.price.text)
	eq(screen.price.text, "12", "digits only")
	screen.price_info()
	eq(screen.step, SellScreen.Step.PRICES, "the cheapest of its kind")
	screen.go_back()
	eq(screen.price.text, "12", "the price typed is kept")
	check(screen.put_on_sale(), "on sale")
	eq(screen.step, SellScreen.Step.PICK)
	eq(screen.info.text, tr("live.on_sale"))
	eq(int(Profile.load_or_new(TEST_PATH).backpack[0].id), 0, "the hero saved")
	screen.free()
	screen = CancelScreen.new()
	root.add_child(screen)
	check(screen.cells[0].icon != null, "my lot")
	check(screen.press_lot(0).contains(Items.name_of(101)), "asks")
	screen.ask.hide()
	screen.confirm()
	eq(screen.info.text, tr("live.canceled") % Items.name_of(101))
	check(screen.cells[0].icon == null, "nothing on sale")
	eq(int(Profile.load_or_new(TEST_PATH).backpack[0].id), 101, "back in the backpack, saved")
	screen.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))
	ServerTests._rm(d)


func test_game_menu_shows_notices_sale_list_gifts_and_fame() -> void:
	var d := _dir()
	var t := _client(d)
	var l: Live = t[1]
	l.notices = [["Welcome", "to Live"], ["Second", "page"]]
	var u := l.user("ANDREY")
	u.sold.append({"item": Items.make(101), "price": 700})
	l.give_gift("ANDREY", "FRIEND", Items.make(131))
	u.fame = 7
	u.exp = 5
	_hero(0).save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH, "live": t[0]}
	var screen: Control = GameMenu.new()
	root.add_child(screen)
	var news: Control = screen.news
	check(news.note.visible, "a page of notices")
	check(news.note.dialog_text.begins_with("Welcome\nto Live"), news.note.dialog_text)
	news.note.confirmed.emit()
	check(news.note.dialog_text.begins_with("Second"), "the next page")
	news.note.confirmed.emit()
	check(news.list.visible and not screen.menu.visible, "then the Sale List, in place of the menu")
	eq(news.list_kind, "sold")
	check(news.list_info.text.contains("700"), news.list_info.text)
	news.list_done()
	eq(news.list_kind, "gifts", "then the Gift List")
	check(news.list_info.text.begins_with("FRIEND"), news.list_info.text)
	eq(t[0].warehouse.size(), 1, "the gift is in the Warehouse")
	news.list_done()
	eq(news.note.dialog_text, tr("live.fame_applied") % [5, 7], "then the Exp and Fame")
	news.note.confirmed.emit()
	check(news.done and screen.menu.visible, "done, the menu again")
	var hero: RefCounted = Profile.load_or_new(TEST_PATH)
	eq([int(hero.fame), int(hero.experience)], [7, 5], "the hero got them, saved")
	screen.free()
	screen = GameMenu.new()
	root.add_child(screen)
	news = screen.news
	check(not news.note.visible and not news.list.visible, "nothing new the second time")
	check(news.done and screen.menu.visible, "the menu at once")
	screen.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))
	ServerTests._rm(d)
