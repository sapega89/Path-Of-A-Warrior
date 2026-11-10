class_name LiveClient
extends RefCounted
## Live on this device, the client of server/live.gd: what the Live screens know of the
## server's side (the Safe, the Warehouse) and the serials the server knows the backpack's
## things by.
##
## As in pyport the hero's gold and backpack are the client's word: sync() sends them
## whenever a Live screen opens, each thing with the serial of its place (place + 1). A place
## that gets a thing from the server keeps the serial the server gave it.
##
## Every call ends in done(err): "" when it went through, else the server's error ("gold",
## "full", "gone", ...) or "offline" when there was no answer. While a request is on its way
## busy is true and the screens take no presses.

const WAREHOUSE := 200
const MAX_SALES := 5
const TAX_PERCENT := 10
const ELIXIRS := [434, 435, 436, 437]
## The kinds of the Buy menu by category (Normal, Special, Rare): the thing shown for each.
const KINDS := [
	[116, 121, 126, 101, 106, 111, 131, 136, 156, 161, 181, 146, 151],
	[331, 324, 322, 301, 308, 302, 341, 350, 357, 363, 370, 380, 415],
	[501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518],
]

## request(msg, done): one request to the server, done(answer) (Cloud.request, or a test's).
var request: Callable
var safe := 0
var warehouse: Array = []  # [{serial, item}], in the server's order
var serials: Array = []  # backpack place -> the serial of its thing, 0 for an empty place
var synced := false
var busy := false
var tax := TAX_PERCENT  # the share of a sale the server keeps
var counts: Array = []  # Buy: lots of a kind at enchant 0..9
var lots: Array = []  # Buy: the lots of a page, Price Info, my lots: [{lot, item, price}]
var pages := 0  # Buy: pages of the kind and enchant asked for
## What the server has for this player when Live opens (ask_status), and what was read of it.
var has_notice := false
var has_sold := false
var has_gifts := false
var notices_seen := false  # the notices are shown once a game
var gifts_told := false  # the game menu says once a game that gifts came
var notice: Array = []  # the lines of a page of notices
var more_notices := false
var sold: Array = []  # Sale List: [{item, price}] (what others bought from me)
var gifts: Array = []  # Gift List: [{from, item}] (already in the Warehouse)
var more_gifts := false
var fame := 0  # Exp / Fame kept on the server for the hero
var exp_points := 0


func _init(send: Callable) -> void:
	request = send


## The Live client of the screen's params ("live", for tests and screenshots), else the one of
## the Cloud autoload; null when the game is not online.
static func of(params: Dictionary) -> RefCounted:
	if params.has("live"):
		return params.live
	var tree := Engine.get_main_loop() as SceneTree
	var cloud: Node = null if tree == null else tree.root.get_node_or_null("Cloud")
	return null if cloud == null else cloud.live


## done(err) for a screen's method, dropped when the screen is gone before the answer came.
static func later(screen: Object, method: StringName) -> Callable:
	var ref: WeakRef = weakref(screen)
	return func(err: String) -> void:
		var s: Object = ref.get_ref()
		if s != null and not (s is Node and (s as Node).is_queued_for_deletion()):
			s.call(method, err)


## A thing as the profile keeps it (the server's numbers can come back as floats).
static func thing(v: Variant) -> Dictionary:
	var it := Items.empty()
	if v is Dictionary:
		for k in it:
			it[k] = int(v.get(k, 0))
	return it


func _send(msg: Dictionary, done: Callable, on_ok: Callable) -> void:
	busy = true
	request.call(
		msg,
		func(r: Dictionary) -> void:
			busy = false
			if r.get("ok", false):
				on_ok.call(r)
				done.call("")
			else:
				done.call(str(r.get("err", "offline")))
	)


## Sends the hero's gold and backpack; the answer brings the Safe and the Warehouse.
func sync(profile: RefCounted, done: Callable) -> void:
	var places: Array = []
	var bp: Array = []
	for i in profile.backpack.size():
		var it: Dictionary = profile.backpack[i]
		places.append(i + 1 if int(it.id) != 0 else 0)
		if int(it.id) != 0:
			bp.append({"serial": i + 1, "item": thing(it)})
	_send(
		{"t": "live_sync", "gold": int(profile.gold), "backpack": bp},
		done,
		func(r: Dictionary) -> void:
			serials = places
			safe = int(r.get("safe", 0))
			warehouse = []
			for w in r.get("warehouse", []):
				warehouse.append({"serial": int(w.get("serial", 0)), "item": thing(w.get("item"))})
			synced = true
	)


## Gold from the hero into the Safe (to_safe) or back.
func move_gold(profile: RefCounted, to_safe: bool, amount: int, done: Callable) -> void:
	_send(
		{"t": "live_safe", "to_safe": to_safe, "amount": amount},
		done,
		func(r: Dictionary) -> void:
			profile.gold = int(r.gold)
			safe = int(r.safe)
	)


## The thing of a backpack place into the Warehouse.
func store(profile: RefCounted, place: int, done: Callable) -> void:
	if (
		serials.size() != profile.backpack.size()
		or place < 0
		or place >= serials.size()
		or int(serials[place]) == 0
		or int(profile.backpack[place].id) == 0
	):
		done.call("gone")
		return
	if warehouse.size() >= WAREHOUSE:
		done.call("full")
		return
	var it := thing(profile.backpack[place])
	var msg := {"t": "live_store", "to_warehouse": true, "serial": int(serials[place])}
	_send(
		msg,
		done,
		func(r: Dictionary) -> void:
			warehouse.append({"serial": int(r.serial), "item": it})
			profile.backpack[place] = Items.empty()
			serials[place] = 0
	)


## A thing of the Warehouse into the first free place of the backpack.
func take(profile: RefCounted, index: int, done: Callable) -> void:
	if serials.size() != profile.backpack.size() or index < 0 or index >= warehouse.size():
		done.call("gone")
		return
	var place := free_place(profile)
	if place < 0:
		done.call("full")
		return
	var entry: Dictionary = warehouse[index]
	var msg := {"t": "live_store", "to_warehouse": false, "serial": int(entry.serial)}
	_send(
		msg,
		done,
		func(r: Dictionary) -> void:
			profile.backpack[place] = thing(entry.item)
			serials[place] = int(r.serial)
			warehouse.erase(entry)
	)


## The Buy menu's category of a thing (0 Normal, 1 Special, 2 Rare) and its kind there.
static func category(id: int) -> int:
	return 2 if id > 500 else (1 if id > 300 else 0)


static func kind(id: int) -> int:
	return id - 501 if id > 500 else int(Items.info(id).get("icon", 0))


static func for_sale(id: int) -> bool:
	return id >= 100 and not ELIXIRS.has(id)


static func _lots_of(r: Dictionary) -> Array:
	var out: Array = []
	for x in r.get("lots", []):
		out.append(
			{
				"lot": int(x.get("lot", 0)),
				"item": thing(x.get("item")),
				"price": int(x.get("price", 0))
			}
		)
	return out


## What is new on the server for this player: notices, things sold, gifts; and the tax.
func ask_status(done: Callable) -> void:
	_send(
		{"t": "live_status"},
		done,
		func(r: Dictionary) -> void:
			has_notice = bool(r.get("notice", false))
			has_sold = bool(r.get("sold", false))
			has_gifts = bool(r.get("gifts", false))
			tax = int(r.get("tax", TAX_PERCENT))
	)


## The next page of the notices.
func ask_notices(done: Callable) -> void:
	_send(
		{"t": "live_notices"},
		done,
		func(r: Dictionary) -> void:
			notice = []
			for line in r.get("lines", []):
				notice.append(str(line))
			more_notices = bool(r.get("more", false))
			if not more_notices:
				notices_seen = true
	)


## The Sale List; the server forgets what it gave.
func ask_sold(done: Callable) -> void:
	_send(
		{"t": "live_sold"},
		done,
		func(r: Dictionary) -> void:
			sold = []
			for x in r.get("sold", []):
				sold.append({"item": thing(x.get("item")), "price": int(x.get("price", 0))})
			has_sold = false
	)


## The next five of the Gift List.
func ask_gifts(done: Callable) -> void:
	_send(
		{"t": "live_gifts"},
		done,
		func(r: Dictionary) -> void:
			gifts = []
			for x in r.get("gifts", []):
				gifts.append({"from": str(x.get("from", "")), "item": thing(x.get("item"))})
			more_gifts = bool(r.get("more", false))
			has_gifts = more_gifts
	)


## The Exp and Fame kept on the server; it keeps them no more.
func ask_fame(done: Callable) -> void:
	_send(
		{"t": "live_fame"},
		done,
		func(r: Dictionary) -> void:
			fame = int(r.get("fame", 0))
			exp_points = int(r.get("exp", 0))
	)


## Buy: how many lots of a kind there are at each enchant level.
func ask_counts(cat: int, k: int, done: Callable) -> void:
	_send(
		{"t": "live_counts", "cat": cat, "kind": k},
		done,
		func(r: Dictionary) -> void:
			counts = []
			for n in r.get("counts", []):
				counts.append(int(n))
	)


## Buy: a page of the lots of a kind (cheapest first); err "none" past the last one.
func ask_page(cat: int, k: int, enchant: int, page: int, done: Callable) -> void:
	var msg := {"t": "live_page", "cat": cat, "kind": k, "enchant": enchant, "page": page}
	_send(
		msg,
		done,
		func(r: Dictionary) -> void:
			lots = _lots_of(r)
			pages = int(r.get("pages", 0))
	)


## Sell > Price Info: the cheapest lots of a kind; err "none" when there are none.
func ask_prices(cat: int, k: int, done: Callable) -> void:
	_send(
		{"t": "live_prices", "cat": cat, "kind": k},
		done,
		func(r: Dictionary) -> void: lots = _lots_of(r)
	)


## Cancel Sale: this player's lots on sale; err "none" when there are none.
func ask_mine(done: Callable) -> void:
	_send({"t": "live_mine"}, done, func(r: Dictionary) -> void: lots = _lots_of(r))


## Buys a lot into the first free place of the backpack, or into the Warehouse.
func buy(profile: RefCounted, lot: Dictionary, to_warehouse: bool, done: Callable) -> void:
	var place := -1 if to_warehouse else free_place(profile)
	if not to_warehouse and place < 0:
		done.call("full")
		return
	if int(lot.price) > int(profile.gold):
		done.call("gold")
		return
	var msg := {"t": "live_buy", "lot": int(lot.lot), "to_warehouse": to_warehouse}
	_send(
		msg,
		done,
		func(r: Dictionary) -> void:
			_receive(profile, place, thing(lot.item), int(r.serial))
			profile.gold = int(r.gold)
			safe = int(r.safe)
			lots.erase(lot)
	)


## Puts a thing of a backpack place (or of the Warehouse) on sale for a price.
func sell(profile: RefCounted, from_warehouse: bool, at: int, price: int, done: Callable) -> void:
	var it := _at(profile, from_warehouse, at)
	if it.is_empty():
		done.call("gone")
		return
	if not for_sale(int(it.id)):
		done.call("not for sale")
		return
	var msg := {
		"t": "live_sell",
		"from_warehouse": from_warehouse,
		"serial": _serial_at(from_warehouse, at),
		"price": price
	}
	_send(msg, done, func(_r: Dictionary) -> void: _forget(profile, from_warehouse, at))


## Gives a thing of a backpack place (or of the Warehouse) to the player with UserID `to`: it
## goes into his Warehouse, with a line in his Gift List.
func give(profile: RefCounted, from_warehouse: bool, at: int, to: String, done: Callable) -> void:
	var it := _at(profile, from_warehouse, at)
	if it.is_empty():
		done.call("gone")
		return
	if not for_sale(int(it.id)):
		done.call("not for sale")
		return
	var msg := {
		"t": "live_give",
		"to": to,
		"from_warehouse": from_warehouse,
		"serial": _serial_at(from_warehouse, at)
	}
	_send(msg, done, func(_r: Dictionary) -> void: _forget(profile, from_warehouse, at))


## Takes one of my lots off the market: into the backpack, or the Warehouse when it is full.
func cancel(profile: RefCounted, lot: Dictionary, done: Callable) -> void:
	var place := free_place(profile)
	if place < 0 and warehouse.size() >= WAREHOUSE:
		done.call("full")
		return
	var msg := {"t": "live_cancel", "lot": int(lot.lot), "to_warehouse": place < 0}
	_send(
		msg,
		done,
		func(r: Dictionary) -> void:
			_receive(profile, place, thing(lot.item), int(r.serial))
			lots.erase(lot)
	)


## A thing of the backpack place `at` (or of the Warehouse), {} when there is none.
func _at(profile: RefCounted, from_warehouse: bool, at: int) -> Dictionary:
	if from_warehouse:
		return warehouse[at].item if at >= 0 and at < warehouse.size() else {}
	if (
		serials.size() != profile.backpack.size()
		or at < 0
		or at >= serials.size()
		or int(serials[at]) == 0
	):
		return {}
	return profile.backpack[at] if int(profile.backpack[at].id) != 0 else {}


func _serial_at(from_warehouse: bool, at: int) -> int:
	return int(warehouse[at].serial) if from_warehouse else int(serials[at])


## The thing of a backpack place (or of the Warehouse) is gone to the server.
func _forget(profile: RefCounted, from_warehouse: bool, at: int) -> void:
	if from_warehouse:
		warehouse.remove_at(at)
	else:
		profile.backpack[at] = Items.empty()
		serials[at] = 0


## A thing from the server into a backpack place with its serial, or (place -1) the Warehouse.
func _receive(profile: RefCounted, place: int, it: Dictionary, serial: int) -> void:
	if place < 0:
		warehouse.append({"serial": serial, "item": it})
	else:
		profile.backpack[place] = it
		serials[place] = serial


static func free_place(profile: RefCounted) -> int:
	for i in profile.backpack.size():
		if int(profile.backpack[i].id) == 0:
			return i
	return -1
