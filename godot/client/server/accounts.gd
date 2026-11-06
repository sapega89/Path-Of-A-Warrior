extends RefCounted
## The server's accounts, one JSON file each (<dir>/<UserID>.json), written whole to a .tmp
## file first and then renamed over the old one, so a crash never leaves half a file.
##   {"id", "salt", "hash", "rounds", "created", "hero": {"rev", "at", "data"}}
## The password is kept only as PBKDF2-HMAC-SHA256 of a random salt.

const ROUNDS := 10000

var dir: String
## PBKDF2 rounds of new accounts (tests use fewer).
var rounds := ROUNDS
var _cache := {}  # UserID -> its dictionary
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


## {"rev", "at", "hero"} of the account (rev 0, hero null: none yet).
func hero_get(uid: String) -> Dictionary:
	var h: Dictionary = _account(uid).get("hero", {})
	return {"rev": int(h.get("rev", 0)), "at": int(h.get("at", 0)), "hero": h.get("data")}


## Writes the hero when `base` is its current revision. Returns [true, the new entry] or
## [false, the current entry] when another device saved first.
func hero_put(uid: String, base: int, at: int, hero: Dictionary) -> Array:
	var acc := _account(uid)
	var cur := hero_get(uid)
	if acc.is_empty() or base != int(cur.rev):
		return [false, cur]
	var old: Variant = acc.hero
	acc.hero = {"rev": int(cur.rev) + 1, "at": at, "data": hero}
	if not _write(acc):
		acc.hero = old
		return [false, cur]
	return [true, hero_get(uid)]


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
