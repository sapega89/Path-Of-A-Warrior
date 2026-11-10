class_name LiveServer
extends RefCounted
## Live on the server (pyport/pow_server/live.py): a market where players sell things to each
## other (Trade), a Warehouse of WAREHOUSE places, a Safe for gold, the Sale List (what others
## bought from me), gifts from player to player (into the Warehouse, with a line in the Gift
## List) and Exp / Fame kept on the server. As in pyport the gold and
## the backpack are the client's word (live_sync), the rest is the server's.
##
## The NPC stock is made up as in pyport: a few Normal / Special things of every kind at enchant
## 0..4 and two random Rare ones, renewed every NPC_REFRESH seconds, priced at the shop's price
## times 1.0..2.0; 502 Silk Rushnyk and 504 Hetman's Seal are always for sale (LIVE_PRICE). A
## sale pays the seller the price less TAX_PERCENT, into the Safe.
##
## Requests (scripts/net/protocol.gd), each answered {t, ok, err?}:
##   live_status            -> notice, sold, gifts (anything new), tax
##   live_notices           -> lines (the next page), more
##   live_sold              -> sold: [{item, price}] (up to PAGE, then they are gone)
##   live_gifts             -> gifts: [{from, item}], more
##   live_fame              -> fame, exp (kept for the hero, then zero)
##   live_sync {gold, backpack: [{serial, item}]} -> safe, warehouse: [{serial, item}]
##   live_safe {to_safe, amount}       -> gold, safe
##   live_store {to_warehouse, serial} -> serial (its new one)
##   live_counts {cat, kind}           -> counts: lots at enchant 0..9
##   live_page {cat, kind, enchant, page} -> lots: [{lot, item, price}], pages
##   live_buy {lot, to_warehouse}      -> serial, gold, safe
##   live_sell {from_warehouse, serial, price}
##   live_prices {cat, kind}           -> lots (cheapest first)
##   live_mine                         -> lots (my lots on sale)
##   live_cancel {lot, to_warehouse}   -> serial
##   live_give {to, from_warehouse, serial} (to: another player's UserID)
## Errors as in pyport: "gold" (not enough), "full", "gone" (sold meanwhile), "limit" (5 lots),
## "price", "not for sale", "own" (your own lot), "none" (empty list), "bad message"; and
## "nobody" (no player with that UserID), "self" (a gift to yourself).

const TAX_PERCENT := 10
const WAREHOUSE := 200
const BACKPACK := 45
const MAX_SALES := 5
const PAGE := 20
const NPC_REFRESH := 3600.0
const MAX_GOLD := 999999999
const ELIXIRS := [434, 435, 436, 437]
const LIVE_PRICE := {502: 3000, 504: 5000}
const NORMAL_KINDS := 13
const SPECIAL_KINDS := 13
const RARE_KINDS := 18

## The handler of each request type (answer()).
var _answers: Dictionary = {}
var dir: String
## The players a gift can go to (GameServer sets it); without it nobody gets a gift.
var accounts: Accounts
var notices: Array = []  # pages of up to 4 lines
var rng := RandomNumberGenerator.new()
var clock: Callable = func() -> float: return Time.get_unix_time_from_system()
## UserID -> {safe, warehouse, serial, sold, gifts, fame, exp}
var _users := {}
var _market := {}


func _init(data_dir: String) -> void:
	dir = data_dir.path_join("live")
	DirAccess.make_dir_recursive_absolute(dir)
	_answers = {
		"live_status": _on_live_status,
		"live_notices": _on_live_notices,
		"live_sold": _on_live_sold,
		"live_gifts": _on_live_gifts,
		"live_fame": _on_live_fame,
		"live_sync": _sync,
		"live_safe": _safe,
		"live_store": _store,
		"live_counts": _on_live_counts,
		"live_page": _on_live_page,
		"live_buy": _buy,
		"live_sell": _sell,
		"live_prices": _on_live_prices,
		"live_mine": _on_live_mine,
		"live_cancel": _cancel,
		"live_give": _give
	}


# --- what the server keeps --------------------------------------------------------------
static func _read(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var v: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	return v if v is Dictionary else {}


static func _write(path: String, d: Dictionary) -> void:
	var f := FileAccess.open(path + ".tmp", FileAccess.WRITE)
	if f == null:
		push_error("live: cannot write %s" % path)
		return
	f.store_string(JSON.stringify(d))
	f.close()
	if FileAccess.file_exists(path):
		DirAccess.remove_absolute(path)
	DirAccess.rename_absolute(path + ".tmp", path)


func user(uid: String) -> Dictionary:
	if not _users.has(uid):
		var u := _read(dir.path_join("user_%s.json" % uid))
		if u.is_empty():
			u = {
				"safe": 0,
				"warehouse": [],
				"serial": 0,
				"sold": [],
				"gifts": [],
				"fame": 0,
				"exp": 0
			}
		_users[uid] = u
	return _users[uid]


func save_user(uid: String) -> void:
	_write(dir.path_join("user_%s.json" % uid), user(uid))


func market() -> Dictionary:
	if _market.is_empty():
		_market = _read(dir.path_join("market.json"))
		if _market.is_empty():
			_market = {"next": 1, "lots": [], "npc_at": -1.0}
	if float(_market.npc_at) < 0 or float(clock.call()) - float(_market.npc_at) >= NPC_REFRESH:
		restock(_market)
		save_market()
	return _market


func save_market() -> void:
	_write(dir.path_join("market.json"), _market)


# --- things ---------------------------------------------------------------------------
static func category(id: int) -> int:
	return 2 if id > 500 else (1 if id > 300 else 0)


## The Buy menu's kind of a thing: its icon (Normal / Special), id - 501 for Rare.
static func kind(id: int) -> int:
	return id - 501 if id > 500 else int(Items.info(id).get("icon", 0))


static func for_sale(id: int) -> bool:
	return id >= 100 and not ELIXIRS.has(id)


## Clean copy of a client's thing: only the fields a thing has, as numbers.
static func clean(v: Variant) -> Dictionary:
	if not v is Dictionary:
		return {}
	var it := Items.empty()
	for k in it:
		it[k] = clampi(int(v.get(k, 0)), 0, 65535)
	return it if it.id > 0 else {}


## New NPC stock: a few things of every Normal / Special kind at enchant 0..4, two random Rare
## ones, and those of LIVE_PRICE that never run out. Players' lots stay.
func restock(m: Dictionary) -> void:
	var lots: Array = m.lots.filter(func(x): return not str(x.seller).is_empty())
	var by_kind := {}
	for table in ["gear", "treasures"]:
		for key in Items.data().get(table, {}):
			var id := int(key)
			if not for_sale(id):
				continue
			by_kind.get_or_add(Vector2i(category(id), kind(id)), []).append(id)
	var add := func(it: Dictionary, price: int, forever: bool) -> void:
		lots.append(
			{
				"id": int(m.next),
				"seller": "",
				"item": it,
				"price": mini(maxi(price, 1), MAX_GOLD),
				"forever": forever
			}
		)
		m.next = int(m.next) + 1
	for cat in [0, 1]:
		var lo := 1.2 if cat == 0 else 1.0
		var hi := 2.0 if cat == 0 else 1.6
		for k in NORMAL_KINDS if cat == 0 else SPECIAL_KINDS:
			var ids: Array = by_kind.get(Vector2i(cat, k), [])
			for i in 4 if cat == 0 else 2:
				if ids.is_empty():
					break
				var id: int = ids[rng.randi_range(0, ids.size() - 1)]
				var it := Items.make(id, rng)
				var times := mini(
					Items.enchant_max(id), [0, 0, 0, 1, 1, 2, 3, 4][rng.randi_range(0, 7)]
				)
				for t in times:
					Items.enchant(it, rng)
				add.call(it, int(Items.price(it) * rng.randf_range(lo, hi)), false)
	var rares: Array = range(501, 519).filter(func(i): return not LIVE_PRICE.has(i))
	for n in 2:
		var id: int = rares.pop_at(rng.randi_range(0, rares.size() - 1))
		var it := Items.make(id)
		add.call(it, int(Items.price(it) * rng.randf_range(1.0, 1.3)), false)
	for id in LIVE_PRICE:
		add.call(Items.make(id), int(LIVE_PRICE[id]), true)
	m.lots = lots
	m.npc_at = float(clock.call())


# --- a player's session -------------------------------------------------------------------
class Session:
	var user := ""
	var gold := 0
	var backpack := {}  # serial -> thing (what the client sent in live_sync)
	var notice_page := 0


func _fail(t: String, err: String) -> Dictionary:
	return {"t": t, "ok": false, "err": err}


static func _serial(u: Dictionary) -> int:
	u.serial = int(u.serial) % 60000 + 1
	return u.serial


static func _new_bp_serial(s: Session) -> int:
	var n := 1000
	while s.backpack.has(n):
		n += 1
	return n


func _lots(s: Session, cat: int, k: int, ench := -1) -> Array:
	return market().lots.filter(
		func(x):
			var id := int(x.item.id)
			return (
				category(id) == cat
				and kind(id) == k
				and str(x.seller) != s.user
				and (ench < 0 or cat == 2 or int(x.item.enchant) == ench)
			)
	)


static func _lot_out(x: Dictionary) -> Dictionary:
	return {"lot": int(x.id), "item": x.item, "price": int(x.price)}


func _find_lot(id: int) -> Dictionary:
	for x in market().lots:
		if int(x.id) == id:
			return x
	return {}


## The answer to one Live request of a logged-in session.
func answer(s: Session, t: String, msg: Dictionary) -> Dictionary:
	var u := user(s.user)
	var handler: Callable = _answers.get(t, Callable())
	if not handler.is_valid():
		return _fail(t, "unknown")
	return handler.call(s, u, msg)


func _on_live_status(_s: Session, u: Dictionary, _msg: Dictionary) -> Dictionary:
	return {
		"t": "live_status",
		"ok": true,
		"notice": not notices.is_empty(),
		"sold": not u.sold.is_empty(),
		"gifts": not u.gifts.is_empty(),
		"tax": TAX_PERCENT
	}


func _on_live_notices(s: Session, _u: Dictionary, _msg: Dictionary) -> Dictionary:
	if notices.is_empty():
		return _fail("live_notices", "none")
	var page: Array = notices[s.notice_page % notices.size()]
	s.notice_page += 1
	var more := s.notice_page < notices.size()
	if not more:
		s.notice_page = 0
	return {"t": "live_notices", "ok": true, "lines": page.slice(0, 4), "more": more}


func _on_live_sold(s: Session, u: Dictionary, _msg: Dictionary) -> Dictionary:
	var sold: Array = u.sold.slice(0, PAGE)
	u.sold = u.sold.slice(PAGE)
	save_user(s.user)
	return {"t": "live_sold", "ok": true, "sold": sold}


func _on_live_gifts(s: Session, u: Dictionary, _msg: Dictionary) -> Dictionary:
	var gifts: Array = u.gifts.slice(0, 5)
	u.gifts = u.gifts.slice(5)
	save_user(s.user)
	return {"t": "live_gifts", "ok": true, "gifts": gifts, "more": not u.gifts.is_empty()}


func _on_live_fame(s: Session, u: Dictionary, _msg: Dictionary) -> Dictionary:
	var r := {"t": "live_fame", "ok": true, "fame": int(u.fame), "exp": int(u.exp)}
	u.fame = 0
	u.exp = 0
	save_user(s.user)
	return r


func _on_live_counts(s: Session, _u: Dictionary, msg: Dictionary) -> Dictionary:
	var counts: Array = []
	counts.resize(10)
	counts.fill(0)
	for x in _lots(s, int(msg.get("cat", -1)), int(msg.get("kind", -1))):
		counts[mini(9, int(x.item.enchant))] += 1
	return {"t": "live_counts", "ok": true, "counts": counts}


func _on_live_page(s: Session, _u: Dictionary, msg: Dictionary) -> Dictionary:
	var lots := _lots(
		s, int(msg.get("cat", -1)), int(msg.get("kind", -1)), int(msg.get("enchant", 0))
	)
	lots.sort_custom(func(a, b): return [int(a.price), int(a.id)] < [int(b.price), int(b.id)])
	var page := int(msg.get("page", 0))
	if page < 0 or page * PAGE >= lots.size():
		return _fail("live_page", "none")
	return {
		"t": "live_page",
		"ok": true,
		"lots": lots.slice(page * PAGE, page * PAGE + PAGE).map(_lot_out),
		"pages": ceili(lots.size() / float(PAGE))
	}


func _on_live_prices(s: Session, _u: Dictionary, msg: Dictionary) -> Dictionary:
	var lots := _lots(s, int(msg.get("cat", -1)), int(msg.get("kind", -1)))
	if lots.is_empty():
		return _fail("live_prices", "none")
	lots.sort_custom(func(a, b): return int(a.price) < int(b.price))
	return {"t": "live_prices", "ok": true, "lots": lots.slice(0, PAGE).map(_lot_out)}


func _on_live_mine(s: Session, _u: Dictionary, _msg: Dictionary) -> Dictionary:
	var mine: Array = market().lots.filter(func(x): return str(x.seller) == s.user)
	if mine.is_empty():
		return _fail("live_mine", "none")
	return {"t": "live_mine", "ok": true, "lots": mine.slice(0, PAGE).map(_lot_out)}


func _sync(s: Session, u: Dictionary, msg: Dictionary) -> Dictionary:
	var bp: Variant = msg.get("backpack")
	if not (msg.get("gold") is int and bp is Array and bp.size() <= BACKPACK):
		return _fail("live_sync", "bad message")
	s.gold = clampi(msg.gold, 0, MAX_GOLD)  # the client's word, as in pyport
	s.backpack = {}
	for e in bp:
		var it := clean(e.get("item") if e is Dictionary else null)
		if not it.is_empty():
			s.backpack[int(e.get("serial", 0))] = it
	return {"t": "live_sync", "ok": true, "safe": int(u.safe), "warehouse": u.warehouse}


func _safe(s: Session, u: Dictionary, msg: Dictionary) -> Dictionary:
	var amount := int(msg.get("amount", 0))
	var to_safe := bool(msg.get("to_safe", true))
	if amount <= 0 or (to_safe and amount > s.gold) or (not to_safe and amount > int(u.safe)):
		return _fail("live_safe", "gold")
	if (
		(to_safe and int(u.safe) + amount > MAX_GOLD)
		or (not to_safe and s.gold + amount > MAX_GOLD)
	):
		return _fail("live_safe", "gold")
	var sign := 1 if to_safe else -1
	s.gold -= amount * sign
	u.safe = int(u.safe) + amount * sign
	save_user(s.user)
	return {"t": "live_safe", "ok": true, "gold": s.gold, "safe": int(u.safe)}


func _store(s: Session, u: Dictionary, msg: Dictionary) -> Dictionary:
	var serial := int(msg.get("serial", -1))
	var wh: Array = u.warehouse
	var n := 0
	if bool(msg.get("to_warehouse", true)):
		if not s.backpack.has(serial):
			return _fail("live_store", "gone")
		if wh.size() >= WAREHOUSE:
			return _fail("live_store", "full")
		n = _serial(u)
		wh.append({"serial": n, "item": s.backpack[serial]})
		s.backpack.erase(serial)
	else:
		var i := wh.find_custom(func(w): return int(w.serial) == serial)
		if i < 0:
			return _fail("live_store", "gone")
		if s.backpack.size() >= BACKPACK:
			return _fail("live_store", "full")
		n = _new_bp_serial(s)
		s.backpack[n] = wh[i].item
		wh.remove_at(i)
	save_user(s.user)
	return {"t": "live_store", "ok": true, "serial": n}


func _buy(s: Session, u: Dictionary, msg: Dictionary) -> Dictionary:
	var lot := _find_lot(int(msg.get("lot", -1)))
	var to_wh := bool(msg.get("to_warehouse", false))
	if lot.is_empty():
		return _fail("live_buy", "gone")
	if str(lot.seller) == s.user:
		return _fail("live_buy", "own")
	if int(lot.price) > s.gold:
		return _fail("live_buy", "gold")
	if (to_wh and u.warehouse.size() >= WAREHOUSE) or (not to_wh and s.backpack.size() >= BACKPACK):
		return _fail("live_buy", "full")
	var it: Dictionary = lot.item.duplicate()
	if not bool(lot.forever):
		market().lots.erase(lot)
	save_market()
	if not str(lot.seller).is_empty():
		var su := user(str(lot.seller))
		su.safe = mini(MAX_GOLD, int(su.safe) + int(lot.price) - int(lot.price) * TAX_PERCENT / 100)
		su.sold.append({"item": it, "price": int(lot.price)})
		save_user(str(lot.seller))
	s.gold -= int(lot.price)
	var n := 0
	if to_wh:
		n = _serial(u)
		u.warehouse.append({"serial": n, "item": it})
	else:
		n = _new_bp_serial(s)
		s.backpack[n] = it
	save_user(s.user)
	return {"t": "live_buy", "ok": true, "serial": n, "gold": s.gold, "safe": int(u.safe)}


func _sell(s: Session, u: Dictionary, msg: Dictionary) -> Dictionary:
	var m := market()
	if m.lots.filter(func(x): return str(x.seller) == s.user).size() >= MAX_SALES:
		return _fail("live_sell", "limit")
	var price: Variant = msg.get("price")
	if not price is int or price <= 0 or price > MAX_GOLD:
		return _fail("live_sell", "price")
	var serial := int(msg.get("serial", -1))
	var from_wh := bool(msg.get("from_warehouse", false))
	var it := _own_thing(s, u, from_wh, serial)
	if it.is_empty():
		return _fail("live_sell", "gone")
	if not for_sale(int(it.id)):
		return _fail("live_sell", "not for sale")
	_take_away(s, u, from_wh, serial)
	m.lots.append(
		{"id": int(m.next), "seller": s.user, "item": it, "price": price, "forever": false}
	)
	m.next = int(m.next) + 1
	save_market()
	return {"t": "live_sell", "ok": true}


func _cancel(s: Session, u: Dictionary, msg: Dictionary) -> Dictionary:
	var lot := _find_lot(int(msg.get("lot", -1)))
	if lot.is_empty() or str(lot.seller) != s.user:
		return _fail("live_cancel", "gone")
	var to_wh := bool(msg.get("to_warehouse", false))
	if to_wh and u.warehouse.size() >= WAREHOUSE:
		return _fail("live_cancel", "full")
	market().lots.erase(lot)
	save_market()
	var n := 0
	if to_wh:
		n = _serial(u)
		u.warehouse.append({"serial": n, "item": lot.item})
		save_user(s.user)
	else:
		n = _new_bp_serial(s)
		s.backpack[n] = lot.item
	return {"t": "live_cancel", "ok": true, "serial": n}


## A thing of this player's backpack (serial of live_sync) or Warehouse, {} when there is none.
static func _own_thing(s: Session, u: Dictionary, from_wh: bool, serial: int) -> Dictionary:
	if not from_wh:
		return s.backpack.get(serial, {})
	var i: int = u.warehouse.find_custom(func(w): return int(w.serial) == serial)
	return u.warehouse[i].item if i >= 0 else {}


func _take_away(s: Session, u: Dictionary, from_wh: bool, serial: int) -> void:
	if from_wh:
		u.warehouse.remove_at(u.warehouse.find_custom(func(w): return int(w.serial) == serial))
		save_user(s.user)
	else:
		s.backpack.erase(serial)


## A thing of the backpack or the Warehouse to another player, into his Warehouse.
func _give(s: Session, u: Dictionary, msg: Dictionary) -> Dictionary:
	var to: Variant = msg.get("to")
	if not Protocol.valid_id(to) or accounts == null or not accounts.has_account(to):
		return _fail("live_give", "nobody")
	if to == s.user:
		return _fail("live_give", "self")
	var serial := int(msg.get("serial", -1))
	var from_wh := bool(msg.get("from_warehouse", false))
	var it := _own_thing(s, u, from_wh, serial)
	if it.is_empty():
		return _fail("live_give", "gone")
	if not for_sale(int(it.id)):
		return _fail("live_give", "not for sale")
	if not give_gift(str(to), s.user, it):
		return _fail("live_give", "full")
	_take_away(s, u, from_wh, serial)
	return {"t": "live_give", "ok": true}


## Puts a thing in a player's Warehouse with a Gift List line (a gift of another player, or
## multiplayer loot).
func give_gift(uid: String, sender: String, item: Dictionary) -> bool:
	var u := user(uid)
	if u.warehouse.size() >= WAREHOUSE:
		return false
	u.warehouse.append({"serial": _serial(u), "item": item})
	u.gifts.append({"from": sender.left(8), "item": item})
	save_user(uid)
	return true
