extends RefCounted
## The online game on this device, the client of server/online.gd: what the Multiplayer
## screens know of the player's online character, the Ranking, the order and the chat.
##
## enter() puts the player online (the Multiplayer menu opens), leave() takes him off. A
## request the server answers "enter first" (the connection came back, the server forgot him)
## enters again and is sent once more. Messages the server sends on its own (a chat message,
## "kicked", the battles) come in on_push(); the screens that listen() get them too.
##
## Every call ends in done(err): "" when it went through, else the server's error ("name
## exists", "too fast", ...) or "offline". While a request is on its way busy is true.
##
## A battle (scripts/net/online_battle.gd) starts with the server's "room" message, after
## find_battle() or invite(), or when another player's invitation takes me in: it is `battle`
## until the screen is done with it, and the battle's messages go to it. on_battle() is
## called when one starts, to show it (the Cloud pushes the battle screen).

const OnlineBattle := preload("res://scripts/net/online_battle.gd")
const BATTLE_PUSHES := ["room", "stage_info", "all_ready", "round_start", "turn_result",
	"stage_end", "room_join", "battle_end"]

## invite() modes: Challenge 1:1, Challenge 2:2, Invite An Ally (a mission), 2-on-2 side by
## side with a member of my order against two CPU fighters.
const CHALLENGE_1 := 0
const CHALLENGE_2 := 1
const ALLY := 2
const TOGETHER := 3

const SKILL_IDS := [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
const EMPTY_SKILL := 99
const GRADES := ["D+", "C-", "C", "C+", "B-", "B", "B+", "A-", "A", "A+"]
const SKILL_NAMES := ["Whirlwind Sabre", "Storm Sabre", "Thunder Sabre", "Dnipro Wave",
	"Rapids", "Flood", "Healing Herbs", "Living Water", "Fury", "Charm",
	"Protection of the Virgin"]
const SKILL_INFO := ["Series of 3 Atk", "Ignore opponent Def.", "Ignore opponent Evd.",
	"Series of 6 Atk", "Opponent Atk Decrease", "Atk 2 enemies at the same time", "Heal HP",
	"Heal HP and MP Increase", "Atk Increase for 3 turns", "Def Increase for 3 turns",
	"Atk/Def Increase for 3 turns"]
const LOBBY := 0
const ORDER := 1
const PRIVATE := 2
const MAX_TEXT := 40
const HISTORY := 30

## request(msg, done): one request to the server, done(answer) (Cloud.request, or a test's).
var request: Callable
var busy := false
var entered := false
var kicked := false  # the same UserID went online on another device
var me := {}  # the character: name, face, level, wins, losses, hp, weapon, slots, quotes, skill_cost
var unread := [0, 0]  # chat messages waiting: [order, private]
var invitation := 1  # Options > Invitation: 0 Deny, 1 Accept
var attributes := {}  # hp, hp_bonus, mp, mp_bonus, atk, atk_bonus, def, def_bonus
var skills: Array = []  # [{id, level}] of the learned skills
var records := {}  # fame, duel_grade, mission_grade, order
var purse := {}  # exp, fame, gold earned online
var rank := {}  # my rank: {rank, value}, {} when none
var rank_rows: Array = []  # [{rank, id, value}] x 3
var order_name := ""
var members: Array = []  # [{id, name, level, online, leader}]
var chat := {}  # conversation key -> [{id, name, text}]
var peer_name := ""  # the display name of the private conversation read last
var peers: Array = []  # [{id, name, unread, online}]
var reading := ""  # the conversation a screen shows (its pushes are not unread)
var battle: RefCounted = null  # the battle on, from its "room" message
var waiting := false  # a duel waits for an opponent
var on_battle := Callable()  # a battle started: show it
var _listeners: Array = []  # [WeakRef, method]


func _init(send: Callable) -> void:
	request = send


## The online client of the screen's params ("online", for tests and screenshots), else the
## one of the Cloud autoload; null when the game is not online.
static func of(params: Dictionary) -> RefCounted:
	if params.has("online"):
		return params.online
	var tree := Engine.get_main_loop() as SceneTree
	var cloud: Node = null if tree == null else tree.root.get_node_or_null("Cloud")
	return null if cloud == null else cloud.mp


## done(err) for a screen's method, dropped when the screen is gone before the answer came.
static func later(screen: Object, method: StringName) -> Callable:
	var ref: WeakRef = weakref(screen)
	return func(err: String) -> void:
		var s: Object = ref.get_ref()
		if s != null and not (s is Node and (s as Node).is_queued_for_deletion()):
			s.call(method, err)


static func key(channel: int, peer := "") -> String:
	return ["lobby", "order", "pm:" + peer][clampi(channel, 0, 2)]


static func skill_name(id: int) -> String:
	var i := SKILL_IDS.find(id)
	return String(TranslationServer.translate(SKILL_NAMES[i])) if i >= 0 else ""


static func grade(v: int) -> String:
	return GRADES[clampi(v, 0, GRADES.size() - 1)]


## The text as the chat sends it: printable ASCII without the backslash, at most 40 characters.
static func clean_text(t: String) -> String:
	var out := ""
	for c in t:
		if c >= " " and c <= "~" and c != "\\":
			out += c
	return out.left(MAX_TEXT)


## Pushes from the server go to screen.method(message) while the screen lives.
func listen(screen: Object, method: StringName) -> void:
	_listeners.append([weakref(screen), method])


func on_push(m: Dictionary) -> void:
	match str(m.get("t", "")):
		"chat_push":
			var k := key(int(m.get("channel", 0)), str(m.get("peer", "")))
			var rows: Array = chat.get(k, [])
			rows.append({"id": str(m.get("id", "")), "name": str(m.get("name", "")), "text": str(m.get("text", ""))})
			chat[k] = rows.slice(-HISTORY)
			var channel := int(m.get("channel", 0))
			if k != reading and str(m.get("id", "")) != str(me.get("id", "")) and channel != LOBBY:
				unread[channel - 1] = mini(99, int(unread[channel - 1]) + 1)
		"kicked":
			kicked = true
			entered = false
			battle = null
		var t when BATTLE_PUSHES.has(t):
			var started: bool = t == "room"
			if started:
				waiting = false
				battle = OnlineBattle.new(battle_request, me)
			if battle != null:
				battle.on_push(m)
			if started and on_battle.is_valid():
				on_battle.call()
	var alive: Array = []
	for l in _listeners:
		var s: Object = l[0].get_ref()
		if s != null and not (s is Node and (s as Node).is_queued_for_deletion()):
			alive.append(l)
			s.call(l[1], m)
	_listeners = alive


func _send(msg: Dictionary, done: Callable, on_ok: Callable, again := true) -> void:
	busy = true
	request.call(msg, _answered.bind(msg, done, on_ok, again))


func _answered(r: Dictionary, msg: Dictionary, done: Callable, on_ok: Callable, again: bool) -> void:
	busy = false
	if r.get("ok", false):
		on_ok.call(r)
		done.call("")
	elif str(r.get("err", "")) == "enter first" and again and str(msg.t) != "mp_enter":
		entered = false
		enter(_entered_again.bind(msg, done, on_ok))
	else:
		done.call(str(r.get("err", "offline")))


func _entered_again(err: String, msg: Dictionary, done: Callable, on_ok: Callable) -> void:
	if err.is_empty():
		_send(msg, done, on_ok, false)
	else:
		done.call(err)


func _take_me(r: Dictionary) -> void:
	me = r.duplicate()
	me.erase("q")
	var u: Array = r.get("unread", [0, 0])
	unread = [int(u[0]), int(u[1])] if u.size() == 2 else [0, 0]


## Online from now on; the answer is the character.
func enter(done: Callable) -> void:
	_send({"t": "mp_enter"}, done, func(r: Dictionary) -> void:
		_take_me(r)
		entered = true
		kicked = false)


func leave() -> void:
	if entered:
		entered = false
		request.call({"t": "mp_leave"}, func(_r: Dictionary) -> void: pass)


func ask_profile(done: Callable) -> void:
	_send({"t": "mp_profile"}, done, _take_me)


func ask_options(done: Callable) -> void:
	_send({"t": "mp_options"}, done, func(r: Dictionary) -> void: invitation = int(r.get("invitation", 1)))


func set_invitation(v: int, done: Callable) -> void:
	_send({"t": "mp_options_set", "invitation": v}, done, func(_r: Dictionary) -> void: invitation = v)


func set_name(name: String, done: Callable) -> void:
	_send({"t": "mp_name", "name": name}, done, func(_r: Dictionary) -> void: me.name = name)


## which: "start" (the battle's first words) or "win" (the victory quote).
func set_quote(which: String, quote: String, done: Callable) -> void:
	_send({"t": "mp_quote", "which": which, "quote": quote}, done, func(_r: Dictionary) -> void:
		me["quote_" + which] = quote)


func ask_attributes(done: Callable) -> void:
	_send({"t": "mp_attributes"}, done, func(r: Dictionary) -> void:
		attributes = r.duplicate()
		attributes.erase("q"))


func ask_skills(done: Callable) -> void:
	_send({"t": "mp_skills"}, done, func(r: Dictionary) -> void:
		skills = []
		for s in r.get("skills", []):
			skills.append({"id": int(s.id), "level": int(s.level)}))


## The four skill slots (EMPTY_SKILL for none), learned skills only.
func set_slots(slots: Array, done: Callable) -> void:
	_send({"t": "mp_slots", "slots": slots}, done, func(_r: Dictionary) -> void:
		var kept: Array = slots.filter(func(s): return s != EMPTY_SKILL)
		while kept.size() < 4:
			kept.append(EMPTY_SKILL)
		me.slots = kept)


func ask_records(done: Callable) -> void:
	_send({"t": "mp_records"}, done, func(r: Dictionary) -> void:
		records = r.duplicate()
		records.erase("q"))


func ask_purse(done: Callable) -> void:
	_send({"t": "mp_purse"}, done, func(r: Dictionary) -> void:
		purse = r.duplicate()
		purse.erase("q"))


## The Ranking of a category (1 Fame, 2 Duel, 3 Mission): my rank, then three rows (the top
## three, or around me when near).
func ask_rank(cat: int, near: bool, done: Callable) -> void:
	_send({"t": "mp_rank_mine", "cat": cat}, _ranked.bind(cat, near, done), func(r: Dictionary) -> void:
		rank = {"rank": int(r.rank), "value": int(r.value)})


func _ranked(err: String, cat: int, near: bool, done: Callable) -> void:
	if not err.is_empty() and err != "none":
		done.call(err)
		return
	if err == "none":
		rank = {}
	_send({"t": "mp_rank_list", "cat": cat, "near": near}, done, func(r: Dictionary) -> void:
		rank_rows = r.get("rows", []))


func ask_order(done: Callable) -> void:
	_send({"t": "order_info"}, done, func(r: Dictionary) -> void:
		order_name = str(r.get("name", ""))
		members = r.get("rows", []))


func order_create(name: String, done: Callable) -> void:
	_send({"t": "order_create", "name": name}, done, func(_r: Dictionary) -> void: order_name = name.to_upper())


func order_join(name: String, done: Callable) -> void:
	_send({"t": "order_join", "name": name}, done, func(_r: Dictionary) -> void: order_name = name.to_upper())


func order_leave(done: Callable) -> void:
	_send({"t": "order_leave"}, done, func(_r: Dictionary) -> void:
		order_name = ""
		members = [])


## Reads a conversation (and the server counts it read).
func read_chat(channel: int, peer: String, done: Callable) -> void:
	_send({"t": "chat_read", "channel": channel, "peer": peer}, done, func(r: Dictionary) -> void:
		var rows: Array = []
		for x in r.get("rows", []):
			rows.append({"id": str(x.id), "name": str(x.name), "text": str(x.text)})
		chat[key(channel, str(r.get("peer", peer)))] = rows
		if channel == PRIVATE:
			peer_name = str(r.get("peer_name", peer))
		if channel != LOBBY:
			unread[channel - 1] = 0 if channel == ORDER else maxi(0, int(unread[1]) - _peer_unread(peer)))


func _peer_unread(peer: String) -> int:
	for p in peers:
		if p.id == peer:
			var n := int(p.unread)
			p.unread = 0
			return n
	return 0


## Writes to a conversation; the server pushes the message back to every reader, me too.
func send_chat(channel: int, peer: String, text: String, done: Callable) -> void:
	_send({"t": "chat_send", "channel": channel, "peer": peer, "text": text}, done, func(_r: Dictionary) -> void: pass)


func ask_peers(done: Callable) -> void:
	_send({"t": "chat_peers"}, done, func(r: Dictionary) -> void:
		peers = []
		for p in r.get("rows", []):
			peers.append({"id": str(p.id), "name": str(p.name), "unread": int(p.unread), "online": int(p.online)}))


# --- battles --------------------------------------------------------------------------------
## Duel 1-on-1 (mode 0), 2-on-2 (1) or a Solo Mission (2): the battle comes as a push, now or
## when an opponent is found (waiting).
func find_battle(mode: int, done: Callable) -> void:
	_send({"t": "mp_match", "mode": mode}, done, func(r: Dictionary) -> void:
		waiting = bool(r.get("waiting", false)))


## No more waiting for an opponent.
func cancel_battle(done: Callable) -> void:
	_send({"t": "mp_cancel"}, done, func(_r: Dictionary) -> void: waiting = false)


## Challenge 1-on-1 (mode 0) or 2-on-2 (1), Invite An Ally (2), side by side with a member of
## my order (3); errors "no player", "self", "not online", "playing", "denied", "not member".
func invite(mode: int, uid: String, done: Callable) -> void:
	_send({"t": "mp_invite", "mode": mode, "id": uid}, done, func(_r: Dictionary) -> void: pass)


## A message of the battle (mp_ready, mp_turn, ...): its answer says nothing the battle needs.
func battle_request(msg: Dictionary) -> void:
	request.call(msg, func(_r: Dictionary) -> void: pass)


## The battle screen is done with the battle.
func battle_over() -> void:
	battle = null
