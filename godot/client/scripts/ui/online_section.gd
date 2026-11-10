class_name OnlineSection
extends VBoxContainer
## The multiplayer part of the game menu, under the line of the character: Character, Ranking,
## Order and Chat, open once the player is online. Duel and Online Missions, and Invitations
## (whether another player's challenge takes me into a battle), are hidden while the online
## battles are being redone (BATTLES). Showing it puts the player online
## (scripts/net/online_client.gd enter); until the server answers it says "Connecting...",
## without an answer "Network connection has failed".
## The line under the heading is the character: display name, level, wins and losses; Chat
## shows the messages waiting (order and private). Another device taking the player online
## ("kicked") closes them. leave() takes the player off the online game.

## Whether the online battles are shown: Duel, Online Missions and Invitations here, their
## topics and keys in Help. Off while they are being redone.
const BATTLES := false
## Button name, text key, screen and the kind for that screen.
const PAGES := [
	["Duel", "online.duel", "online_battles", "duel"],
	["OnlineMissions", "menu.online_missions", "online_battles", "mission"],
	["Character", "online.character", "online_character", ""],
	["Ranking", "online.ranking", "online_ranking", ""],
	["Order", "online.order", "online_order", ""],
	["Chat", "online.chat", "online_chat", ""],
	["Invitations", "menu.invitations", "online_options", ""],
]
## The pages of the online battles, hidden while BATTLES is off.
const BATTLE_PAGES := ["Duel", "OnlineMissions", "Invitations"]

var online: RefCounted
var who: Label
var status: Label
var buttons: Array[Button] = []
var chat: Button


## params go on to the pages (online, for tests and screenshots).
func _init(params: Dictionary) -> void:
	name = "Multiplayer"
	online = OnlineClient.of(params)
	add_theme_constant_override("separation", 6)
	who = UiTheme.note("Who")
	who.add_theme_font_size_override("font_size", 22)
	add_child(who)
	status = UiTheme.note("Status")
	add_child(status)
	for page in shown_pages():
		var b := Button.new()
		b.name = page[0]
		b.text = page[1]
		b.disabled = true
		var screen: String = page[2]
		var page_params: Dictionary = params.duplicate()
		if not str(page[3]).is_empty():
			page_params.kind = page[3]
		b.pressed.connect(func(): Router.push(screen, page_params))
		add_child(b)
		buttons.append(b)
	chat = get_node("Chat")


## The pages of PAGES shown: without the battles' pages while BATTLES is off.
static func shown_pages() -> Array:
	if BATTLES:
		return PAGES
	return PAGES.filter(func(p: Array) -> bool: return not p[0] in BATTLE_PAGES)


func _ready() -> void:
	if online == null:
		_say(tr("live.failed"))
		return
	online.listen(self, &"pushed")
	_say(tr("live.connecting"))
	if online.entered:
		online.ask_profile(OnlineClient.later(self, &"entered"))
	else:
		online.enter(OnlineClient.later(self, &"entered"))


func entered(err: String) -> void:
	if not err.is_empty():
		_say(tr("live.failed"))
		return
	_say("")
	show_me()
	for b in buttons:
		b.disabled = false


func show_me() -> void:
	var m: Dictionary = online.me
	who.text = (
		tr("online.who")
		% [
			str(m.get("name", "")),
			int(m.get("level", 1)),
			int(m.get("wins", 0)),
			int(m.get("losses", 0))
		]
	)
	var waiting := int(online.unread[0]) + int(online.unread[1])
	chat.text = tr("online.chat") + (" (%d)" % waiting if waiting > 0 else "")


## A message from the server: a chat message counts as waiting; "kicked", another device took
## the player online.
func pushed(m: Dictionary) -> void:
	if m.t == "kicked":
		_say(tr("online.kicked"))
		for b in buttons:
			b.disabled = true
	elif m.t == "chat_push" and not online.me.is_empty():
		show_me()


## The state of the connection under the character; no empty line when there is nothing to say.
func _say(text: String) -> void:
	status.text = text
	status.visible = not text.is_empty()


## Off the online game: nobody can challenge the hero while he is away from this menu.
func leave() -> void:
	if online != null:
		online.leave()
