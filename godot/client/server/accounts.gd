extends RefCounted
## The server's accounts, one JSON file each (<dir>/<UserID>.json), written whole to a .tmp
## file first and then renamed over the old one, so a crash never leaves half a file.
##   {"id", "salt", "hash", "rounds", "created", "hero": {"rev", "at", "data"},
##    "options": {"rev", "at", "data"}}
## The hero and the Options (STORES) each keep a revision: a write based on an older one is
## refused, so a device that missed another device's save learns of it.
## The password is kept only as PBKDF2-HMAC-SHA256 of a random salt.
## The hero's name (hero.data.name) belongs to one account, in any case: the first account
## saved with it keeps it (name_owner()); the new game asks the server whether it is free.

const ROUNDS := 10000
const STORES := ["hero", "options"]

var dir: String
## PBKDF2 rounds of new accounts (tests use fewer).
var rounds := ROUNDS
var _cache := {}  # UserID -> its dictionary
var _names := {}  # the hero's name in upper case -> the UserID it belongs to
var _names_read := false  # _names was made from the files
var _crypto := Crypto.new()


func _init(accounts_dir: String) -> void:
	dir = accounts_dir
	DirAccess.make_dir_recursive_absolute(dir)


func _file(uid: String) -> String:
	return dir.path_join(uid + ".json")


func _account(uid: String) -> Dictionary:
	if _cache.has(uid):
		return _cache[uid]
	if not FileAccess.file_exists(_file(uid)):
		return {}
	var v: Variant = JSON.parse_string(FileAccess.get_file_as_string(_file(uid)))
	if not v is Dictionary:
		push_error("accounts: unreadable %s" % _file(uid))
		return {}
	_cache[uid] = v
	return v


func _write(acc: Dictionary) -> bool:
	var path := _file(str(acc.id))
	var f := FileAccess.open(path + ".tmp", FileAccess.WRITE)
	if f == null:
		push_error("accounts: cannot write %s" % path)
		return false
	f.store_string(JSON.stringify(acc))
	f.close()
	if FileAccess.file_exists(path):
		DirAccess.remove_absolute(path)  # rename does not replace a file everywhere
	return DirAccess.rename_absolute(path + ".tmp", path) == OK


func has_account(uid: String) -> bool:
	return not _account(uid).is_empty()


## A new account; with no password (pwd ""), one nobody can log in to (the server's bots).
func create_account(uid: String, pwd: String) -> bool:
	if has_account(uid):
		return false
	var salt := _crypto.generate_random_bytes(16)
	var acc := {"id": uid, "salt": salt.hex_encode(), "rounds": rounds,
		"hash": pbkdf2(pwd.to_ascii_buffer(), salt, rounds).hex_encode() if not pwd.is_empty() else "",
		"created": Time.get_unix_time_from_system(), "hero": {"rev": 0, "at": 0, "data": null}}
	if not _write(acc):
		return false
	_cache[uid] = acc
	return true


func check_password(uid: String, pwd: String) -> bool:
	var acc := _account(uid)
	if acc.is_empty() or str(acc.get("hash", "")).is_empty():
		return false
	var h := pbkdf2(pwd.to_ascii_buffer(), str(acc.salt).hex_decode(), int(acc.rounds))
	return same_bytes(h, str(acc.hash).hex_decode())


## {"rev", "at", "data"} of one of the account's STORES (rev 0, data null: none yet).
func store_get(uid: String, store: String) -> Dictionary:
	var h: Dictionary = _account(uid).get(store, {})
	return {"rev": int(h.get("rev", 0)), "at": int(h.get("at", 0)), "data": h.get("data")}


## Writes a store when `base` is its current revision. Returns [true, the new entry] or
## [false, the current entry] when another device saved first.
func store_put(uid: String, store: String, base: int, at: int, data: Dictionary) -> Array:
	var acc := _account(uid)
	var cur := store_get(uid, store)
	if acc.is_empty() or not store in STORES or base != int(cur.rev):
		return [false, cur]
	var old: Variant = acc.get(store)
	acc[store] = {"rev": int(cur.rev) + 1, "at": at, "data": data}
	if not _write(acc):
		if old == null:
			acc.erase(store)
		else:
			acc[store] = old
		return [false, cur]
	return [true, store_get(uid, store)]


## The UserID whose hero has this name (any case), "" when nobody's has it.
func name_owner(name: String) -> String:
	_read_names()
	return str(_names.get(name.to_upper(), ""))


## The hero's name of an account's hero dictionary, "" without one.
static func hero_name(hero: Variant) -> String:
	return str(hero.get("name", "")).strip_edges() if hero is Dictionary else ""


## Who has which name, from every account's file: of two heroes with one name, the older
## account has it.
func _read_names() -> void:
	if _names_read:
		return
	_names_read = true
	var accs: Array = []
	for f in DirAccess.get_files_at(dir):
		if f.ends_with(".json"):
			var acc := _account(f.trim_suffix(".json"))
			if not acc.is_empty():
				accs.append(acc)
	accs.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		var ca := float(a.get("created", 0))
		var cb := float(b.get("created", 0))
		return ca < cb or (ca == cb and str(a.id) < str(b.id)))
	for acc: Dictionary in accs:
		_claim_name(str(acc.id), hero_name((acc.get("hero", {}) as Dictionary).get("data")))


## The account's hero is called `name` now: its old name is free again, the new one is its
## own unless another account has it.
func _claim_name(uid: String, name: String) -> void:
	for k in _names.keys():
		if _names[k] == uid and k != name.to_upper():
			_names.erase(k)
	if not name.is_empty() and not _names.has(name.to_upper()):
		_names[name.to_upper()] = uid


## {"rev", "at", "hero"} of the account (rev 0, hero null: none yet).
func hero_get(uid: String) -> Dictionary:
	var e := store_get(uid, "hero")
	return {"rev": e.rev, "at": e.at, "hero": e.data}


## store_put() of the hero, the entries as hero_get() gives them.
func hero_put(uid: String, base: int, at: int, hero: Dictionary) -> Array:
	var r := store_put(uid, "hero", base, at, hero)
	if r[0]:
		_read_names()
		_claim_name(uid, hero_name(hero))
	return [r[0], hero_get(uid)]


## PBKDF2-HMAC-SHA256 with one 32-byte block (RFC 8018).
func pbkdf2(pwd: PackedByteArray, salt: PackedByteArray, count: int) -> PackedByteArray:
	var block := salt.duplicate()
	block.append_array(PackedByteArray([0, 0, 0, 1]))
	var u := _crypto.hmac_digest(HashingContext.HASH_SHA256, pwd, block)
	var out := u.duplicate()
	for i in count - 1:
		u = _crypto.hmac_digest(HashingContext.HASH_SHA256, pwd, u)
		for j in out.size():
			out[j] ^= u[j]
	return out


## Equal bytes, in a time that does not depend on where they differ.
static func same_bytes(a: PackedByteArray, b: PackedByteArray) -> bool:
	if a.size() != b.size():
		return false
	var diff := 0
	for i in a.size():
		diff |= a[i] ^ b[i]
	return diff == 0
