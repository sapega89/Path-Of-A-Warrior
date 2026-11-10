class_name Protocol
extends RefCounted
## What the game and its server say to each other: ENet over UDP, encrypted with DTLS, one
## Godot Dictionary per packet (var_to_bytes, never objects), on channel 0, reliable and in order.
##
## Every request has "t" (its type) and may carry "q" (a number the answer repeats). Every
## answer has "t", "ok", and "err" when ok is false.
##
##   register {id, pwd, v}       -> {ok} / err "update" "bad id" "taken" "limit"
##   login    {id, pwd, v}       -> {ok} / err "update" "bad id" "no account" "password"
##   hero_get {}                 -> {ok, rev, at, hero}          (rev 0 and hero null: none yet)
##   hero_put {base, at, hero}   -> {ok, rev} / err "conflict" with the server's {rev, at, hero}
##   options_get {}              -> {ok, rev, at, options}       (the Options, kept like the hero)
##   options_put {base, at, options} -> {ok, rev} / err "conflict" with {rev, at, options}
##
## Any request before a login answers err "login first"; a wrong one "bad message", an unknown
## type "unknown", a packet over MAX_PACKET "too big". `base` is the revision of the hero the
## client last saw: a device that missed another device's save gets "conflict".
## UserID: 4 to 12 letters A-Z; password: 4 to 12 digits.

const VERSION := 1
const PORT := 28310
const CHANNELS := 3  # 0 requests, 1 chat and invitations, 2 arena battles (later)
const MAX_PACKET := 64 * 1024
const MAX_HERO := 48 * 1024  # bytes of the hero in the server's file
const MAX_OPTIONS := 1024  # bytes of the Options in the server's file


static func encode(msg: Dictionary) -> PackedByteArray:
	return var_to_bytes(msg)


## The dictionary of a packet, or {} when it is anything else.
static func decode(data: PackedByteArray) -> Dictionary:
	if data.is_empty() or data.size() > MAX_PACKET:
		return {}
	var v: Variant = bytes_to_var(data)  # objects are refused here
	return v if v is Dictionary else {}


static func valid_id(id: Variant) -> bool:
	return id is String and _match(id, 4, 12, "A", "Z")


static func valid_password(pwd: Variant) -> bool:
	return pwd is String and _match(pwd, 4, 12, "0", "9")


static func _match(s: String, lo: int, hi: int, first: String, last: String) -> bool:
	if s.length() < lo or s.length() > hi:
		return false
	for c in s:
		if c < first or c > last:
			return false
	return true
