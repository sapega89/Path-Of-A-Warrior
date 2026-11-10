# gdlint: disable=max-public-methods
class_name OnlineServer
extends RefCounted
# gdlint: disable=max-file-lines
## The online game on the server (pyport/pow_server/server.py, model.py, chat.py, orders.py):
## each account's online character, Options, the Character pages, the Ranking, the orders and
## the chat; and the server's bots, accounts nobody logs in to that are always online.
##
## The character is the account's hero (the single-player save the server keeps,
## server/accounts.gd: level, HP / MP / ATK / DEF and the gear's bonuses, the face and the
## weapon, the skills and the keys they are on, the missions won) plus what only the online
## game has: the display name, the two quotes, wins and losses, the Exp / Fame / Gold earned
## online, the Duel and Mission grades, Invitation, the skill slots chosen online and the order.
## That part is kept in <data>/online/char_<ID>.json; orders in order_<NAME>.json; the chat in
## chat_*.json (the last HISTORY messages of each conversation) and me_<ID>.json (what a player
## has read).
##
## The Multiplayer menu of a client sends mp_enter first (the player is online from then on,
## until mp_leave or the connection closes); every other request needs it. Each is answered
## {t, ok, err?}:
##   mp_enter / mp_profile            -> the character (id, name, face, level, wins, losses, hp,
##                                       weapon, slots, quotes, skill_cost), unread: [order,
##                                       private]
##   mp_options / mp_options_set {invitation: 0 Deny, 1 Accept}
##   mp_name {name}                   -> err "not acceptable", "name exists"
##   mp_quote {which: "start" | "win", quote}
##   mp_attributes                    -> hp, hp_bonus, mp, mp_bonus, atk, atk_bonus, def, def_bonus
##   mp_skills                        -> skills: [{id, level}]
##   mp_slots {slots: 4 ids, 99 empty}
##   mp_records                       -> fame, duel_grade, mission_grade, order
##   mp_purse                         -> exp, fame, gold (earned online)
##   mp_rank_mine {cat: 1 Fame, 2 Duel, 3 Mission} -> rank, value
##   mp_rank_list {cat, near}         -> rows: 3 x {rank, id, value} (the top three, or around me)
##   order_info                       -> name, rows: [{id, name, level, online, leader}]
##   order_create {name} / order_join {name} / order_leave
##                                    -> err "not acceptable", "name exists", "none", "full", "in
##                                    order"
##   chat_read {channel: 0 lobby, 1 order, 2 private, peer} -> peer_name, rows: [{id, name, text}]
##   chat_send {channel, peer, text}  -> err "no order", "no player", "self", "not acceptable",
##                                       "too fast"; every online reader gets
##                                       {t: "chat_push", channel, peer, id, name, text}
##   chat_peers                       -> rows: [{id, name, unread, online}]
##
## Battles (server/room.gd, server/battle.gd); the battle itself comes as pushes (room.gd):
##   mp_match {mode: 0 Duel 1-on-1, 1 Duel 2-on-2, 2 Solo Mission} -> waiting: a duel waits up
##                                       to MATCH_WAIT s for a player near my level, then gets
##                                       the CPU; a mission starts at once with a CPU ally
##   mp_cancel                        -> no more waiting (err "none")
##   mp_invite {mode: 0 Challenge 1:1, 1 Challenge 2:2, 2 Invite An Ally, 3 with an order member
##             against two CPU fighters, id} -> err "busy", "self", "no player", "not member",
##                                       "not online", "playing", "denied"; no question to the
##                                       other player: his Options > Invitation decides; a bot
##                                       always accepts and fights as a CPU fighter of my level
##   mp_ready / mp_turn {target, action, hit} / mp_stage_next / mp_intro_done / mp_exit
##                                    -> err "no battle"; mp_exit leaves (a duel left is lost)
##   battle_end carries the rewards (also added to the character's purse here) and the loot,
##   which the client gives the hero.

const EMPTY_SKILL := 99
const SKILL_IDS := [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
## single-player skill index -> its code; the online game knows the codes 3..13
const SKILL_CODES := [3, 4, 5, 9, 10, 11, 12, 13, 6, 7, 8, 14, 15, 16, 17, 18, 19, 20, 21]
## what only the online game has, with the values of a new character
const ONLINE_FIELDS := {
	"name": "",
	"wins": 0,
	"losses": 0,
	"quote_start": "Prepare yourself!",
	"quote_win": "Too easy.",
	"mp_exp": 0,
	"mp_fame": 0,
	"gold": 0,
	"duel_grade": 0,
	"mission_grade": 0,
	"invitation": 1,
	"slots": [],
	"order": "",
	"bot": false
}
## the server's bots: UserID, display name, Fame
const BOTS := [
	["BLADE", "Blade", 900],
	["RAVEN", "Raven", 600],
	["TIGER", "Tiger", 400],
	["SHADOW", "Shadow", 250],
	["IRONFIST", "Ironfist", 100]
]
const BOT_LINES := [
	"Ha! Fight me first.",
	"Not now, I am sharpening my sword.",
	"Challenge me and we will talk.",
	"Good luck out there!",
	"See you in the arena.",
	"Who sent you?",
	"I only speak with my blade."
]

const LOBBY := 0
const ORDER := 1
const PRIVATE := 2
const MAX_TEXT := 40
const HISTORY := 30
const MAX_PEERS := 20
const RATE := [[1.5, 1], [20.0, 6]]  # at most 1 message in 1.5 s and 6 in 20 s
const MAX_MEMBERS := 30
const MATCH_WAIT := 60.0  # seconds a Duel waits for a live opponent, then a CPU
const MATCH_LEVELS := [10, 20]  # level reach at first / after half the wait
const INVITE_TEAM := 3
## starred whole or inside words, any case
# gdlint:ignore = max-line-length
const RUDE := "fuck|shit|bitch|cunt|dick|asshole|bastard|whore|slut|nigg|fagg|blya|blia|suka|pizd|khuy|xuy|huy|hui|ebat|yeba|mudak|pidor|pidar|gandon"

## The handler of each request type (answer()).
var _answers: Dictionary = {}
var dir: String
var accounts: Accounts
var rng := RandomNumberGenerator.new()
var clock: Callable = func() -> float: return Time.get_ticks_msec() / 1000.0
## UserID -> Session of the players online
var online := {}
var queue: Array = []  # sessions waiting for a Duel, oldest first
var rooms: Array = []  # the battles going on
var match_wait := MATCH_WAIT
var _chars := {}  # UserID -> the online part of the character
var _docs := {}  # file name -> a document (orders, chat)
var _rude := RegEx.create_from_string("(?i)" + RUDE)
var _name_re := RegEx.create_from_string("^[A-Za-z0-9]{1,8}$")
var _quote_re := RegEx.create_from_string("^[ -~]{1,20}$")
var _id_re := RegEx.create_from_string("^[A-Z]{4,12}$")
var _text_re := RegEx.create_from_string("^[ -\\[\\]-~]+$")


## A player's connection as the online game sees it. send(msg) pushes a message to the client.
class Session:
	var user := ""
	var send: Callable = func(_m: Dictionary) -> void: pass
	var chat_times: Array = []
	var room: RefCounted = null  # server/room.gd while in a battle
	var slot := 0  # my slot in it
	var queued_mode := -1  # mp_match mode while waiting for an opponent
	var queued_at := 0.0


func _init(data_dir: String, account_store: Accounts) -> void:
	dir = data_dir.path_join("online")
	accounts = account_store
	DirAccess.make_dir_recursive_absolute(dir)
	for f in DirAccess.get_files_at(dir):
		if f.begins_with("char_") and f.ends_with(".json"):
			var uid := f.trim_prefix("char_").trim_suffix(".json")
			_chars[uid] = _read(dir.path_join(f))
	_answers = {
		"mp_profile": _on_mp_profile,
		"mp_options": _on_mp_options,
		"mp_options_set": _on_mp_options_set,
		"mp_name": _on_mp_name,
		"mp_quote": _on_mp_quote,
		"mp_attributes": _on_mp_attributes,
		"mp_skills": _on_mp_skills,
		"mp_slots": _on_mp_slots,
		"mp_records": _on_mp_records,
		"mp_purse": _on_mp_purse,
		"mp_rank_mine": _on_mp_rank_mine,
		"mp_rank_list": _on_mp_rank_list,
		"order_info": _on_order_info,
		"order_create": _on_order_create,
		"order_join": _on_order_create,
		"order_leave": _on_order_leave,
		"chat_read": _on_chat_read,
		"chat_send": _chat_send,
		"mp_match": _match,
		"mp_cancel": _on_mp_cancel,
		"mp_invite": _invite,
		"mp_ready": _in_battle,
		"mp_turn": _in_battle,
		"mp_stage_next": _in_battle,
		"mp_intro_done": _in_battle,
		"mp_exit": _in_battle,
		"chat_peers": _on_chat_peers
	}


# --- what the server keeps ----------------------------------------------------------------
static func _read(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var v: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	return v if v is Dictionary else {}


static func _write(path: String, d: Dictionary) -> void:
	var f := FileAccess.open(path + ".tmp", FileAccess.WRITE)
	if f == null:
		push_error("online: cannot write %s" % path)
		return
	f.store_string(JSON.stringify(d))
	f.close()
	if FileAccess.file_exists(path):
		DirAccess.remove_absolute(path)
	DirAccess.rename_absolute(path + ".tmp", path)


func _doc(file: String, empty: Dictionary) -> Dictionary:
	if not _docs.has(file):
		var d := _read(dir.path_join(file))
		_docs[file] = d if not d.is_empty() else empty
	return _docs[file]


func _put_doc(file: String, d: Dictionary) -> void:
	_docs[file] = d
	_write(dir.path_join(file), d)


## The online part of a character; one never kept yet is made (and kept unless `keep` is
## false: another player looked at only).
func online_part(uid: String, keep := true) -> Dictionary:
	if not _chars.has(uid):
		var fresh: Dictionary = ONLINE_FIELDS.duplicate(true)
		if not keep:
			return fresh
		_chars[uid] = fresh
	var c: Dictionary = _chars[uid]
	for k in ONLINE_FIELDS:
		if not c.has(k):
			c[k] = ONLINE_FIELDS[k]
	return c


func save_char(uid: String) -> void:
	_write(dir.path_join("char_%s.json" % uid), online_part(uid))


## The whole character: the account's hero and the online part.
func character(uid: String) -> Dictionary:
	var c := online_part(uid, false).duplicate(true)
	c.id = uid
	var hero: Variant = accounts.hero_get(uid).get("hero") if accounts.has_account(uid) else null
	var h: Dictionary = hero if hero is Dictionary else {}
	c.level = clampi(int(h.get("level", 1)), 1, 255)
	var base: Array = h.get("base", [])
	var face := int(h.get("head", 0)) & 3
	var start: Array = Rules.HERO_BASES[face]
	c.face = face
	c.hp = int(base[0]) if base.size() == 4 else start[0] + 10
	c.mp = int(base[1]) if base.size() == 4 else start[1]
	c.atk = int(base[2]) if base.size() == 4 else start[2] + 2
	c.def = int(base[3]) if base.size() == 4 else start[3] + 1
	var bonus := {"attack": 0, "defense": 0, "hp": 0, "mp": 0}
	var worn: Array = h.get("equipped", [])
	for it in worn:
		if it is Dictionary and int(it.get("id", 0)) != 0:
			for k in bonus:
				bonus[k] += int(it.get(k, 0))
	if h.is_empty():
		bonus.attack = 1  # the Iron Broadsword of a new hero
	c.atk_bonus = bonus.attack
	c.def_bonus = bonus.defense
	c.hp_bonus = bonus.hp
	c.mp_bonus = bonus.mp
	var weapon := int(worn[0].get("id", 0)) if not worn.is_empty() and worn[0] is Dictionary else 0
	c.weapon = 1 if weapon >= 101 and weapon <= 115 else 0
	var skills := {}
	var levels: Array = h.get("skill_levels", [])
	for i in mini(levels.size(), SKILL_CODES.size()):
		if int(levels[i]) > 0 and SKILL_IDS.has(SKILL_CODES[i]):
			skills[SKILL_CODES[i]] = int(levels[i])
	if h.is_empty():
		skills = {3: 1, 11: 1}  # Whirlwind Sabre, Fury
	c.skills = skills
	var chosen: Array = c.slots
	if chosen.is_empty():  # none chosen online: the skills on the hero's keys
		for v in h.get("hotkeys", [12, 17] if h.is_empty() else []):
			var i := int(v) - 12
			if i >= 0 and i < SKILL_CODES.size():
				chosen.append(SKILL_CODES[i])
	var slots: Array = []  # the learned ones, each once, then EMPTY_SKILL
	for v in chosen:
		if skills.has(int(v)) and not slots.has(int(v)) and slots.size() < 4:
			slots.append(int(v))
	while slots.size() < 4:
		slots.append(EMPTY_SKILL)
	c.slots = slots
	c.progress = (h.get("done", {}) as Dictionary).size()
	return c


static func max_hp(c: Dictionary) -> int:
	return int(c.hp) + int(c.hp_bonus)


static func max_mp(c: Dictionary) -> int:
	return int(c.mp) + int(c.mp_bonus)


static func display_name(c: Dictionary) -> String:
	return str(c.name) if not str(c.name).is_empty() else str(c.id).left(8)


## Four slots: learned skills first, then EMPTY_SKILL; [] when one is not learned or twice.
static func _valid_slots(skills: Dictionary, slots: Array) -> Array:
	var out: Array = []
	for s in slots:
		var v := int(s)
		if v == EMPTY_SKILL:
			continue
		if not skills.has(v) or out.has(v):
			return []
		out.append(v)
	if out.size() > 4:
		return []
	while out.size() < 4:
		out.append(EMPTY_SKILL)
	return out


func profile(uid: String) -> Dictionary:
	var c := character(uid)
	var costs: Array = []
	for id in SKILL_IDS:
		costs.append(Rules.skill_cost(id, int(c.skills.get(id, 1)), max_mp(c)))
	return {
		"id": uid,
		"name": display_name(c),
		"face": c.face,
		"level": c.level,
		"wins": int(c.wins),
		"losses": int(c.losses),
		"hp": max_hp(c),
		"weapon": c.weapon,
		"slots": c.slots,
		"quote_start": c.quote_start,
		"quote_win": c.quote_win,
		"skill_cost": costs
	}


# --- the server's bots ----------------------------------------------------------------------
## Makes the bot accounts on the first start (accounts without a password: nobody logs in
## to them); a UserID that is already taken, by a bot of an earlier start or a player, is left
## alone.
func add_bots() -> void:
	for b in BOTS:
		var uid: String = b[0]
		if accounts.has_account(uid) or not accounts.create_account(uid, ""):
			continue
		var c := online_part(uid)
		c.bot = true
		c.name = "" if name_taken(b[1], uid) else b[1]
		var fame: int = b[2]
		c.mp_fame = fame
		c.duel_grade = mini(9, fame / 100)
		c.mission_grade = c.duel_grade
		c.wins = fame / 10
		c.losses = fame / 25
		c.quote_start = "Nobody else? Fight me!"
		c.quote_win = "Come back stronger."
		save_char(uid)


func is_bot(uid: String) -> bool:
	return _chars.has(uid) and bool(_chars[uid].get("bot", false))


func is_online(uid: String) -> bool:
	return online.has(uid) or is_bot(uid)


# --- sessions --------------------------------------------------------------------------------
## A player opened the Multiplayer menu: online from now on, his character kept (so that the
## Ranking counts him). Another connection of the same UserID that was online is told
## {t: "kicked"} and is not online any more. Returns the answer to mp_enter.
func enter(s: Session, uid: String) -> Dictionary:
	if uid.is_empty():
		return _fail("mp_enter", "login first")
	var old: Session = online.get(uid)
	if old != null and old != s:
		old.send.call({"t": "kicked"})
		leave(old)
	leave(s)
	s.user = uid
	online[uid] = s
	if not FileAccess.file_exists(dir.path_join("char_%s.json" % uid)):
		save_char(uid)
	var p := profile(uid)
	p.unread = unread(uid)
	return _ok("mp_enter", p)


## Out of the online game: not waiting any more, out of a battle (a duel left is lost).
func leave(s: Session) -> void:
	queue.erase(s)
	if s.room != null:
		var r: Room = s.room
		s.room = null
		r.leave(s)
		if r.players.is_empty():
			rooms.erase(r)
	if not s.user.is_empty() and online.get(s.user) == s:
		online.erase(s.user)
	s.user = ""


## The server stops: every battle and wait ends without rewards.
func shutdown() -> void:
	for r in rooms:
		for s in r.players.values():
			s.room = null
		r.players.clear()
	rooms.clear()
	queue.clear()
	online.clear()


func _fail(t: String, err: String) -> Dictionary:
	return {"t": t, "ok": false, "err": err}


func _ok(t: String, d := {}) -> Dictionary:
	d.t = t
	d.ok = true
	return d


## The answer to one request of a logged-in player.
func answer(s: Session, t: String, msg: Dictionary) -> Dictionary:
	var uid := s.user
	if t == "mp_leave":
		leave(s)
		return _ok(t)
	if uid.is_empty():
		return _fail(t, "enter first")
	online_part(uid)  # the player's part of the game is made on his first request
	var handler: Callable = _answers.get(t, Callable())
	if not handler.is_valid():
		return _fail(t, "unknown")
	return handler.call(s, t, msg)


func _on_mp_profile(s: Session, t: String, _msg: Dictionary) -> Dictionary:
	var uid := s.user
	var p := profile(uid)
	p.unread = unread(uid)
	return _ok(t, p)


func _on_mp_options(s: Session, t: String, _msg: Dictionary) -> Dictionary:
	var uid := s.user
	var c := online_part(uid)
	return _ok(t, {"invitation": int(c.invitation)})


func _on_mp_options_set(s: Session, t: String, msg: Dictionary) -> Dictionary:
	var uid := s.user
	var c := online_part(uid)
	var v: Variant = msg.get("invitation")
	if not (v is int and (v == 0 or v == 1)):
		return _fail(t, "bad message")
	c.invitation = v
	save_char(uid)
	return _ok(t)


func _on_mp_name(s: Session, t: String, msg: Dictionary) -> Dictionary:
	var uid := s.user
	var c := online_part(uid)
	var name := str(msg.get("name", ""))
	if _name_re.search(name) == null:
		return _fail(t, "not acceptable")
	if name_taken(name, uid):
		return _fail(t, "name exists")
	c.name = name
	save_char(uid)
	return _ok(t)


func _on_mp_quote(s: Session, t: String, msg: Dictionary) -> Dictionary:
	var uid := s.user
	var c := online_part(uid)
	var q := str(msg.get("quote", ""))
	var which := str(msg.get("which", ""))
	if _quote_re.search(q) == null or not which in ["start", "win"]:
		return _fail(t, "not acceptable")
	c["quote_" + which] = q
	save_char(uid)
	return _ok(t)


func _on_mp_attributes(s: Session, t: String, _msg: Dictionary) -> Dictionary:
	var uid := s.user
	var ch := character(uid)
	return _ok(
		t,
		{
			"hp": ch.hp,
			"hp_bonus": ch.hp_bonus,
			"mp": ch.mp,
			"mp_bonus": ch.mp_bonus,
			"atk": ch.atk,
			"atk_bonus": ch.atk_bonus,
			"def": ch.def,
			"def_bonus": ch.def_bonus
		}
	)


func _on_mp_skills(s: Session, t: String, _msg: Dictionary) -> Dictionary:
	var uid := s.user
	var ch := character(uid)
	var rows: Array = []
	for id in SKILL_IDS:
		if ch.skills.has(id):
			rows.append({"id": id, "level": ch.skills[id]})
	return _ok(t, {"skills": rows})


func _on_mp_slots(s: Session, t: String, msg: Dictionary) -> Dictionary:
	var uid := s.user
	var c := online_part(uid)
	var slots: Variant = msg.get("slots")
	var ok: Array = (
		_valid_slots(character(uid).skills, slots) if slots is Array and slots.size() == 4 else []
	)
	if ok.is_empty():
		return _fail(t, "bad message")
	c.slots = ok
	save_char(uid)
	return _ok(t)


func _on_mp_records(s: Session, t: String, _msg: Dictionary) -> Dictionary:
	var uid := s.user
	var c := online_part(uid)
	var doc := my_order(uid)
	return _ok(
		t,
		{
			"fame": int(c.mp_fame),
			"duel_grade": int(c.duel_grade),
			"mission_grade": int(c.mission_grade),
			"order": str(doc.get("name", ""))
		}
	)


func _on_mp_purse(s: Session, t: String, _msg: Dictionary) -> Dictionary:
	var uid := s.user
	var c := online_part(uid)
	return _ok(t, {"exp": int(c.mp_exp), "fame": int(c.mp_fame), "gold": int(c.gold)})


func _on_mp_rank_mine(s: Session, t: String, msg: Dictionary) -> Dictionary:
	var uid := s.user
	var cat := int(msg.get("cat", 0))
	if cat < 1 or cat > 3:
		return _fail(t, "bad message")
	for r in table(cat):
		if r.id == uid:
			return _ok(t, {"rank": r.rank, "value": r.value})
	return _fail(t, "none")


func _on_mp_rank_list(s: Session, t: String, msg: Dictionary) -> Dictionary:
	var uid := s.user
	var cat := int(msg.get("cat", 0))
	if cat < 1 or cat > 3:
		return _fail(t, "bad message")
	var rows := table(cat)
	var start := 0
	if bool(msg.get("near", false)):  # me in the middle when possible
		var me := rows.find_custom(func(r): return r.id == uid)
		start = maxi(0, mini(me - 1, rows.size() - 3))
	rows = rows.slice(start, start + 3)
	while rows.size() < 3:
		rows.append({"rank": 0, "id": "", "value": 0})
	return _ok(t, {"rows": rows})


func _on_order_info(s: Session, _t: String, _msg: Dictionary) -> Dictionary:
	var uid := s.user
	return _order_info(uid)


func _on_order_create(s: Session, t: String, msg: Dictionary) -> Dictionary:
	var uid := s.user
	return _order_enter(t, uid, str(msg.get("name", "")).to_upper())


func _on_order_leave(s: Session, t: String, _msg: Dictionary) -> Dictionary:
	var uid := s.user
	_order_leave(uid)
	return _ok(t)


func _on_chat_read(s: Session, _t: String, msg: Dictionary) -> Dictionary:
	var uid := s.user
	return _chat_read(uid, msg)


func _on_mp_cancel(s: Session, t: String, _msg: Dictionary) -> Dictionary:
	if not queue.has(s):
		return _fail(t, "none")
	queue.erase(s)
	return _ok(t)


func _on_chat_peers(s: Session, t: String, _msg: Dictionary) -> Dictionary:
	var uid := s.user
	var rows: Array = []
	for p in _me(uid).peers:
		rows.append(
			{
				"id": p[0],
				"name": display_name(character(p[0])),
				"unread": int(p[1]),
				"online": int(is_online(p[0]))
			}
		)
	return _ok(t, {"rows": rows})


func name_taken(name: String, uid: String) -> bool:
	for other in _chars:
		if other != uid and str(_chars[other].get("name", "")).to_upper() == name.to_upper():
			return true
	return false


## Every character by a value (1 Fame, 2 Duel grade, 3 Mission grade), best first.
func table(cat: int) -> Array:
	var key: String = ["", "mp_fame", "duel_grade", "mission_grade"][cat]
	var ids: Array = _chars.keys()
	ids.sort_custom(
		func(a, b):
			var va := int(_chars[a].get(key, 0))
			var vb := int(_chars[b].get(key, 0))
			return va > vb or (va == vb and str(a) < str(b))
	)
	var out: Array = []
	for i in ids.size():
		out.append({"rank": i + 1, "id": ids[i], "value": int(_chars[ids[i]].get(key, 0))})
	return out


# --- orders ----------------------------------------------------------------------------------
func order(name: String) -> Dictionary:
	if name.is_empty():
		return {}
	var d := _doc("order_%s.json" % name, {})
	return d if not (d.get("members", []) as Array).is_empty() else {}


## My order; a stale one (gone, or I am not in it) is forgotten.
func my_order(uid: String) -> Dictionary:
	var c := online_part(uid)
	var d := order(str(c.order))
	if d.is_empty() or not uid in d.members:
		if not str(c.order).is_empty():
			c.order = ""
			save_char(uid)
		return {}
	return d


func same_order(a: String, b: String) -> bool:
	var d := my_order(a)
	return not d.is_empty() and b in d.members


func _order_info(uid: String) -> Dictionary:
	var d := my_order(uid)
	if d.is_empty():
		return _ok("order_info", {"name": "", "rows": []})
	var rows: Array = []
	for m in d.members:
		var ch := character(m)
		rows.append(
			{
				"id": m,
				"name": display_name(ch),
				"level": ch.level,
				"online": int(online.has(m)),
				"leader": int(m == d.members[0])
			}
		)
	rows.sort_custom(
		func(a, b):  # the leader, me, who is online, the others
			var ka := [1 - a.leader, int(a.id != uid), 1 - a.online]
			var kb := [1 - b.leader, int(b.id != uid), 1 - b.online]
			return ka < kb
	)
	return _ok("order_info", {"name": d.name, "rows": rows.slice(0, MAX_MEMBERS)})


func _order_enter(t: String, uid: String, name: String) -> Dictionary:
	if not my_order(uid).is_empty():
		return _fail(t, "in order")
	var file := "order_%s.json" % name
	if t == "order_create":
		if _id_re.search(name) == null:
			return _fail(t, "not acceptable")
		if not order(name).is_empty():
			return _fail(t, "name exists")
		_put_doc(file, {"name": name, "members": [uid]})
		_put_doc("chat_order_%s.json" % name, {"seq": 0, "rows": []})  # a new order, a new chat
	else:
		var d := order(name)
		if d.is_empty():
			return _fail(t, "none")
		if not uid in d.members:
			if d.members.size() >= MAX_MEMBERS:
				return _fail(t, "full")
			d.members.append(uid)
			_put_doc(file, d)
	var c := online_part(uid)
	c.order = name
	save_char(uid)
	var me := _me(uid)
	me.order_seen = int(_chat("chat_order_%s.json" % name).seq)  # earlier messages count as read
	_put_doc("me_%s.json" % uid, me)
	return _ok(t)


func _order_leave(uid: String) -> void:
	var c := online_part(uid)
	var d := order(str(c.order))
	if not d.is_empty() and uid in d.members:
		d.members.erase(uid)
		_put_doc("order_%s.json" % d.name, d)
	if not str(c.order).is_empty():
		c.order = ""
		save_char(uid)


# --- the chat --------------------------------------------------------------------------------
func _chat(file: String) -> Dictionary:
	return _doc(file, {"seq": 0, "rows": []})


func _me(uid: String) -> Dictionary:
	return _doc("me_%s.json" % uid, {"order_seen": 0, "peers": []})


static func _pm_file(a: String, b: String) -> String:
	return "chat_pm_%s_%s.json" % ([a, b] if a < b else [b, a])


## The text as it will be shown, or "" when it is not acceptable.
func clean(text: Variant) -> String:
	var s := str(text).strip_edges() if text is String else ""
	if s.is_empty() or s.length() > MAX_TEXT or _text_re.search(s) == null:
		return ""
	for m in _rude.search_all(s):
		s = (
			s.substr(0, m.get_start())
			+ "*".repeat(m.get_end() - m.get_start())
			+ s.substr(m.get_end())
		)
	return s


## [order, private]: chat messages waiting for a player.
func unread(uid: String) -> Array:
	var me := _me(uid)
	var in_order := 0
	var c := online_part(uid)
	if not str(c.order).is_empty():
		in_order = maxi(0, int(_chat("chat_order_%s.json" % c.order).seq) - int(me.order_seen))
	var private := 0
	for p in me.peers:
		private += int(p[1])
	return [mini(in_order, 99), mini(private, 99)]


## [file, ""] of a conversation, or ["", error].
func _target(uid: String, channel: int, peer: String) -> Array:
	match channel:
		LOBBY:
			return ["chat_lobby.json", ""]
		ORDER:
			var d := my_order(uid)
			return ["chat_order_%s.json" % d.name, ""] if not d.is_empty() else ["", "no order"]
		PRIVATE:
			if peer == uid:
				return ["", "self"]
			if _id_re.search(peer) == null or not accounts.has_account(peer):
				return ["", "no player"]
			return [_pm_file(uid, peer), ""]
	return ["", "bad message"]


func _touch_peer(uid: String, peer: String, add_unread: bool) -> void:
	var me := _me(uid)
	var old: Array = []
	for p in me.peers:
		if p[0] == peer:
			old = p
	var count := 0 if not add_unread else (int(old[1]) if not old.is_empty() else 0) + 1
	var peers: Array = [[peer, mini(count, 99)]]
	for p in me.peers:
		if p[0] != peer:
			peers.append(p)
	me.peers = peers.slice(0, MAX_PEERS)
	_put_doc("me_%s.json" % uid, me)


func _chat_read(uid: String, msg: Dictionary) -> Dictionary:
	var channel := int(msg.get("channel", -1))
	var peer := str(msg.get("peer", "")).to_upper()
	var target := _target(uid, channel, peer)
	if target[0].is_empty():
		return _fail("chat_read", target[1])
	var doc := _chat(target[0])
	var me := _me(uid)
	if channel == ORDER:
		me.order_seen = int(doc.seq)
		_put_doc("me_%s.json" % uid, me)
	elif channel == PRIVATE:
		for p in me.peers:
			if p[0] == peer:
				p[1] = 0
		_put_doc("me_%s.json" % uid, me)
	else:
		peer = ""
	var rows: Array = []
	for r in doc.rows:
		rows.append({"id": r[0], "name": r[1], "text": r[2]})
	return _ok(
		"chat_read",
		{
			"channel": channel,
			"peer": peer,
			"peer_name": display_name(character(peer)) if not peer.is_empty() else "",
			"rows": rows
		}
	)


## Whether a player may write one more message now.
func _rate_ok(s: Session) -> bool:
	var now: float = clock.call()
	s.chat_times = s.chat_times.filter(func(x): return now - float(x) < 20.0)
	for r in RATE:
		if s.chat_times.filter(func(x): return now - float(x) < float(r[0])).size() >= int(r[1]):
			return false
	s.chat_times.append(now)
	return true


func _chat_send(s: Session, _t: String, msg: Dictionary) -> Dictionary:
	var uid := s.user
	var channel := int(msg.get("channel", -1))
	var peer := str(msg.get("peer", "")).to_upper()
	var target := _target(uid, channel, peer)
	if target[0].is_empty():
		return _fail("chat_send", target[1])
	var text := clean(msg.get("text"))
	if text.is_empty():
		return _fail("chat_send", "not acceptable")
	if not _rate_ok(s):
		return _fail("chat_send", "too fast")
	var name := display_name(character(uid))
	var doc := _append(target[0], uid, name, text)
	var readers: Array = []  # [UserID, the peer as that reader sees it]
	match channel:
		LOBBY:
			for other in online:
				readers.append([other, ""])
		ORDER:
			for m in my_order(uid).members:
				readers.append([m, ""])
			var me := _me(uid)
			me.order_seen = int(doc.seq)  # my own message is read
			_put_doc("me_%s.json" % uid, me)
		PRIVATE:
			readers = [[uid, peer], [peer, uid]]
			_touch_peer(uid, peer, false)
			_touch_peer(peer, uid, true)
	for r in readers:
		var other: Session = online.get(r[0])
		if other != null:
			other.send.call(
				{
					"t": "chat_push",
					"channel": channel,
					"peer": r[1],
					"id": uid,
					"name": name,
					"text": text
				}
			)
	if channel == PRIVATE and is_bot(peer):  # a bot answers with one of its lines
		var line: String = BOT_LINES[rng.randi_range(0, BOT_LINES.size() - 1)]
		var bot_name := display_name(character(peer))
		_append(target[0], peer, bot_name, line)
		_touch_peer(uid, peer, true)
		s.send.call(
			{
				"t": "chat_push",
				"channel": PRIVATE,
				"peer": peer,
				"id": peer,
				"name": bot_name,
				"text": line
			}
		)
	return _ok("chat_send")


func _append(file: String, uid: String, name: String, text: String) -> Dictionary:
	var doc := _chat(file)
	doc.seq = int(doc.seq) + 1
	var rows: Array = doc.rows
	rows.append([uid, name, text])
	doc.rows = rows.slice(-HISTORY)
	_put_doc(file, doc)
	return doc


# --- battles ---------------------------------------------------------------------------------
static func _int(v: Variant, default: int) -> int:
	return v if v is int else default


func _open_room(
	mode: int, fighters: Array, players: Dictionary, progress: int, via: String
) -> void:
	var r := Room.new(self, mode, fighters, players, progress, via)
	rooms.append(r)
	r.start()


func _fighter(uid: String, slot: int) -> Battle.Fighter:
	return Battle.from_character(character(uid), slot)


func _match(s: Session, _t: String, msg: Dictionary) -> Dictionary:
	var t := "mp_match"
	var mode := _int(msg.get("mode"), -1)
	if mode < 0 or mode > 2:
		return _fail(t, "bad message")
	if s.room != null or queue.has(s):
		return _fail(t, "busy")
	if mode == 2 or match_wait <= 0:
		start_vs_cpu(s, mode)
		return _ok(t, {"waiting": false})
	var other := find_opponent(s, mode)
	if other == null:
		s.queued_mode = mode
		s.queued_at = clock.call()
		queue.append(s)
		return _ok(t, {"waiting": true})
	queue.erase(other)
	var first := _fighter(other.user, 0)  # the one who waited takes the left side
	var second := _fighter(s.user, 1)
	var fighters: Array = [first, second]
	if mode == 1:
		fighters += [
			Battle.cpu_fighter(rng, first, 2, true), Battle.cpu_fighter(rng, second, 3, true)
		]
	_open_room(mode, fighters, {0: other, 1: s}, 0, "match")
	return _ok(t, {"waiting": false})


## A player waiting for the same kind of duel near my level: within MATCH_LEVELS, the reach
## opening once they have waited half the time.
func find_opponent(s: Session, mode: int) -> Session:
	var now: float = clock.call()
	var level := int(character(s.user).level)
	for other: Session in queue:
		if other == s or other.queued_mode != mode:
			continue
		var reach: int = (
			MATCH_LEVELS[1] if now - other.queued_at >= match_wait / 2 else MATCH_LEVELS[0]
		)
		if absi(int(character(other.user).level) - level) <= reach:
			return other
	return null


## Called often (server/game_server.gd poll): a duel that waited match_wait gets the CPU.
func tick() -> void:
	if queue.is_empty():
		return
	var now: float = clock.call()
	for s: Session in queue.duplicate():
		if now - s.queued_at >= match_wait:
			queue.erase(s)
			start_vs_cpu(s, s.queued_mode)


## A battle against the CPU: 1v1 at slots 0 / 1; 2v2 adds an ally at 2 and a foe at 3; a
## mission an ally at 2 (the foes come with the stages).
func start_vs_cpu(s: Session, mode: int) -> void:
	var me := _fighter(s.user, 0)
	var others: Array = []
	if mode == 2:
		others = [Battle.cpu_fighter(rng, me, 2, true)]
	else:
		others = [Battle.cpu_fighter(rng, me, 1)]
		if mode == 1:
			others += [Battle.cpu_fighter(rng, me, 2, true), Battle.cpu_fighter(rng, me, 3)]
	_open_room(mode, [me] + others, {0: s}, int(character(s.user).progress), "match")


func _invite(s: Session, _t: String, msg: Dictionary) -> Dictionary:
	var t := "mp_invite"
	var mode := _int(msg.get("mode"), -1)
	var uid := str(msg.get("id", "")).to_upper()
	if mode < 0 or mode > INVITE_TEAM:
		return _fail(t, "bad message")
	if s.room != null or queue.has(s):
		return _fail(t, "busy")
	if uid == s.user:
		return _fail(t, "self")
	if _id_re.search(uid) == null or not accounts.has_account(uid):
		return _fail(t, "no player")
	if mode == INVITE_TEAM and not same_order(s.user, uid):
		return _fail(t, "not member")
	if is_bot(uid) and not online.has(uid):
		_invite_bot(s, mode, uid)
		return _ok(t)
	var other: Session = online.get(uid)
	if other == null:
		return _fail(t, "not online")
	if other.room != null or queue.has(other):
		return _fail(t, "playing")
	if int(online_part(uid).invitation) == 0:
		return _fail(t, "denied")
	var me := _fighter(s.user, 0)
	if mode == INVITE_TEAM:  # side by side against two CPU fighters, a 2-on-2 duel
		var mate := _fighter(uid, 2)
		_open_room(
			1,
			[me, mate, Battle.cpu_fighter(rng, me, 1), Battle.cpu_fighter(rng, mate, 3)],
			{0: s, 2: other},
			0,
			""
		)
		return _ok(t)
	var them := _fighter(uid, 2 if mode == 2 else 1)
	var fighters: Array = [me, them]
	if mode == 1:  # each player gets a CPU ally
		fighters += [Battle.cpu_fighter(rng, me, 2, true), Battle.cpu_fighter(rng, them, 3, true)]
	var progress := maxi(int(character(s.user).progress), int(character(uid).progress))
	_open_room(mode, fighters, {0: s, them.slot: other}, progress, "")
	return _ok(t)


## A bot challenged or invited: the room as against the CPU, the bot in the invited player's
## place.
func _invite_bot(s: Session, mode: int, uid: String) -> void:
	var me := _fighter(s.user, 0)
	var fighters: Array = [me, bot_fighter(uid, me, 2 if mode == 2 else 1, mode == 2)]
	if mode == 1:
		fighters += [Battle.cpu_fighter(rng, me, 2, true), Battle.cpu_fighter(rng, me, 3)]
	_open_room(mode, fighters, {0: s}, int(character(s.user).progress), "invite")


## A bot in a battle: a CPU fighter of about my level, with the bot's name and record.
func bot_fighter(uid: String, me: Battle.Fighter, slot: int, ally: bool) -> Battle.Fighter:
	var c := character(uid)
	var f := Battle.cpu_fighter(rng, me, slot, ally)
	f.name = display_name(c)
	f.keep_name = true
	f.wins = int(c.wins)
	f.losses = int(c.losses)
	f.quote_start = str(c.quote_start)
	f.quote_win = str(c.quote_win)
	return f


func _in_battle(s: Session, t: String, msg: Dictionary) -> Dictionary:
	var r: Room = s.room
	if r == null:
		return _fail(t, "no battle")
	match t:
		"mp_ready":
			r.round_ready(s)
		"mp_turn":
			r.turn(
				s,
				[
					_int(msg.get("target"), 1),
					_int(msg.get("action"), Battle.DEFEND),
					_int(msg.get("hit"), 20)
				]
			)
		"mp_stage_next":
			r.stage_next(s)
		"mp_intro_done":
			r.intro_done(s)
		"mp_exit":  # "Exit Battle"
			s.room = null
			r.leave(s)
			if r.players.is_empty():
				rooms.erase(r)
	return _ok(t)


## The end of the battle for a player: the rewards (a mission's for the stages cleared), one
## drop roll per foe beaten (mission monsters are soldiers, the last stage's fighter a boss,
## a duel's fighters generals), his rank, and out of the room.
func battle_end(s: Session, r: Room) -> void:
	var b: Battle = r.battle
	var m: Dictionary = r.mission
	var c := online_part(s.user)
	var res: Dictionary
	var cat := 2
	var kills: Array = []
	if not m.is_empty():
		var stood: bool = r.human_slots.any(func(k): return b.fighters[k].alive())
		var cleared: int = int(m.stage) - (0 if stood and not b.team_alive(1) else 1)
		res = b.mission_rewards(c, s.slot, cleared, int(m.stages))
		cat = 3
		for i in mini(cleared, int(m.stages) - 1):
			kills.append_array([0, 0])
		if cleared == int(m.stages):
			kills.append_array([2, 0])
	else:
		res = b.duel_rewards(c, s.slot)
		if res.win:
			for f in b.fighters.values():
				if f.team() != s.slot % 2:
					kills.append(1)
	res.loot = Loot.roll(rng, int(character(s.user).level), kills)
	r.players.erase(s.slot)
	s.room = null
	if r.players.is_empty():
		rooms.erase(r)
	save_char(s.user)
	res.rank = 0
	for row in table(cat):
		if row.id == s.user:
			res.rank = row.rank
	res.t = "battle_end"
	s.send.call(res)


## A player left a duel (it counts, a loss when not won); no battle_end for him.
func duel_left(s: Session, r: Room) -> void:
	if s.user.is_empty():
		return
	r.battle.duel_rewards(online_part(s.user), s.slot)
	save_char(s.user)
