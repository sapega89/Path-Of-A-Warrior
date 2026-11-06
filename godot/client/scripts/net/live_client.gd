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

const Items := preload("res://scripts/core/items.gd")
const WAREHOUSE := 200

## request(msg, done): one request to the server, done(answer) (Cloud.request, or a test's).
var request: Callable
var safe := 0
var warehouse: Array = []  # [{serial, item}], in the server's order
var serials: Array = []  # backpack place -> the serial of its thing, 0 for an empty place
var synced := false
var busy := false


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
	request.call(msg, func(r: Dictionary) -> void:
		busy = false
		if r.get("ok", false):
			on_ok.call(r)
			done.call("")
		else:
			done.call(str(r.get("err", "offline"))))


## Sends the hero's gold and backpack; the answer brings the Safe and the Warehouse.
func sync(profile: RefCounted, done: Callable) -> void:
	var places: Array = []
	var bp: Array = []
	for i in profile.backpack.size():
		var it: Dictionary = profile.backpack[i]
		places.append(i + 1 if int(it.id) != 0 else 0)
		if int(it.id) != 0:
			bp.append({"serial": i + 1, "item": thing(it)})
	_send({"t": "live_sync", "gold": int(profile.gold), "backpack": bp}, done, func(r: Dictionary) -> void:
		serials = places
		safe = int(r.get("safe", 0))
		warehouse = []
		for w in r.get("warehouse", []):
			warehouse.append({"serial": int(w.get("serial", 0)), "item": thing(w.get("item"))})
		synced = true)


## Gold from the hero into the Safe (to_safe) or back.
func move_gold(profile: RefCounted, to_safe: bool, amount: int, done: Callable) -> void:
	_send({"t": "live_safe", "to_safe": to_safe, "amount": amount}, done, func(r: Dictionary) -> void:
		profile.gold = int(r.gold)
		safe = int(r.safe))


## The thing of a backpack place into the Warehouse.
func store(profile: RefCounted, place: int, done: Callable) -> void:
	if serials.size() != profile.backpack.size() or place < 0 or place >= serials.size() \
			or int(serials[place]) == 0 or int(profile.backpack[place].id) == 0:
		done.call("gone")
		return
	if warehouse.size() >= WAREHOUSE:
		done.call("full")
		return
	var it := thing(profile.backpack[place])
	var msg := {"t": "live_store", "to_warehouse": true, "serial": int(serials[place])}
	_send(msg, done, func(r: Dictionary) -> void:
		warehouse.append({"serial": int(r.serial), "item": it})
		profile.backpack[place] = Items.empty()
		serials[place] = 0)


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
	_send(msg, done, func(r: Dictionary) -> void:
		profile.backpack[place] = thing(entry.item)
		serials[place] = int(r.serial)
		warehouse.erase(entry))


static func free_place(profile: RefCounted) -> int:
	for i in profile.backpack.size():
		if int(profile.backpack[i].id) == 0:
			return i
	return -1
