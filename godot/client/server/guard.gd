class_name Guard
extends RefCounted
## The server's limits against guessing and flooding:
## - LOGIN_FAILS wrong passwords for one UserID, or from one address, within LOGIN_WINDOW
##   seconds block that UserID / address for LOGIN_BLOCK seconds; a blocked login is answered
##   as a wrong password (no hint that the guess was right);
## - at most NEW_ACCOUNTS new accounts from one address in NEW_ACCOUNTS_WINDOW seconds;
## - at most MAX_CONNECTIONS connections at once from one address;
## - at most MAX_MESSAGES messages a second on one connection, then it is closed.
## An empty address (tests) counts only for the per-UserID limit.

const LOGIN_FAILS := 5
const LOGIN_WINDOW := 600.0
const LOGIN_BLOCK := 300.0
const NEW_ACCOUNTS := 5
const NEW_ACCOUNTS_WINDOW := 3600.0
const MAX_CONNECTIONS := 10
const MAX_MESSAGES := 30

var login_fails := LOGIN_FAILS
var login_window := LOGIN_WINDOW
var login_block := LOGIN_BLOCK
var new_accounts := NEW_ACCOUNTS
var new_accounts_window := NEW_ACCOUNTS_WINDOW
var max_connections := MAX_CONNECTIONS
var max_messages := MAX_MESSAGES
## Seconds now; tests put their own clock here.
var clock: Callable = func() -> float: return Time.get_ticks_msec() / 1000.0

var _fails := {}  # "id:X" / "ip:A" -> Array of times of wrong passwords
var _blocked := {}  # same keys -> blocked until
var _created := {}  # address -> Array of times of new accounts
var connections := {}  # address -> open connections


static func _keys(uid: String, peer: String) -> Array[String]:
	var keys: Array[String] = ["id:" + uid]
	if not peer.is_empty():
		keys.append("ip:" + peer)
	return keys


func _trim(times: Array, window: float) -> void:
	var now: float = clock.call()
	while not times.is_empty() and now - float(times[0]) > window:
		times.pop_front()


func login_blocked(uid: String, peer: String = "") -> bool:
	var now: float = clock.call()
	for k in _keys(uid, peer):
		if _blocked.has(k):
			if now < float(_blocked[k]):
				return true
			_blocked.erase(k)
	return false


## After a password check: a right one clears the UserID's count.
func login_result(uid: String, peer: String, ok: bool) -> void:
	if ok:
		_fails.erase("id:" + uid)
		return
	var now: float = clock.call()
	for k in _keys(uid, peer):
		var times: Array = _fails.get_or_add(k, [])
		times.append(now)
		_trim(times, login_window)
		if times.size() >= login_fails:
			_blocked[k] = now + login_block
			times.clear()


## The password check (check: Callable() -> bool) behind the limits.
func check_password(uid: String, peer: String, check: Callable) -> bool:
	if login_blocked(uid, peer):
		return false
	var ok: bool = check.call()
	login_result(uid, peer, ok)
	return ok


func may_create(peer: String) -> bool:
	if peer.is_empty():
		return true
	var times: Array = _created.get_or_add(peer, [])
	_trim(times, new_accounts_window)
	if times.size() >= new_accounts:
		return false
	times.append(clock.call())
	return true


## False: too many connections from this address already.
func open_connection(peer: String) -> bool:
	if peer.is_empty():
		return true
	if int(connections.get(peer, 0)) >= max_connections:
		return false
	connections[peer] = int(connections.get(peer, 0)) + 1
	return true


func close_connection(peer: String) -> void:
	if peer.is_empty() or int(connections.get(peer, 0)) <= 0:
		return
	connections[peer] = int(connections[peer]) - 1
	if connections[peer] == 0:
		connections.erase(peer)


## Times of one connection's messages: allow() is false once more than max_messages came in
## the last second.
class Meter:
	var per_second: int
	var clock: Callable
	var times: Array[float] = []

	func _init(limit: int, c: Callable) -> void:
		per_second = limit
		clock = c

	func allow() -> bool:
		var now: float = clock.call()
		times.append(now)
		while not times.is_empty() and now - times[0] > 1.0:
			times.pop_front()
		return times.size() <= per_second


func meter() -> Meter:
	return Meter.new(max_messages, clock)
