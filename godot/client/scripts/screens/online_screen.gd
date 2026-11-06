extends Control
## Live > Multiplayer: the online game's main menu (pyport pow/game/online: Duel, Mission,
## Character, Options, Help, Ranking, and the Order and Chat windows). Help is open even
## without the server; the rest once the player is online. Opening it puts the player
## online (scripts/net/online_client.gd enter); until the server answers it says
## "Connecting...", without an answer "Network connection has failed" with only Back. The line
## under the title is the character: display name, level, wins and losses. Chat shows the
## messages waiting (order and private). Back takes the player off the online game.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const OnlineClient := preload("res://scripts/net/online_client.gd")
const MainMenu := preload("res://scripts/screens/main_menu.gd")
## Page button name, text key, screen (empty: not open yet), and its kind for the screen.
const PAGES := [
	["Duel", "online.duel", "online_battles", "duel"],
	["Mission", "online.mission", "online_battles", "mission"],
	["Character", "online.character", "online_character"],
	["Ranking", "online.ranking", "online_ranking"],
	["Order", "online.order", "online_order"],
	["Chat", "online.chat", "online_chat"],
	["Options", "online.options", "online_options"],
	["Help", "online.help", "help", "mp"],
]

var online: RefCounted
var status: Label
var who: Label
var buttons: Array[Button] = []
var chat: Button


func _ready() -> void:
	online = OnlineClient.of(Router.params)
	var col := UiTheme.menu_column(self, 560)
	col.theme = MainMenu.compact_theme()  # nine buttons in a 720 px high screen
	col.add_theme_constant_override("separation", 4)
	col.add_child(UiTheme.heading("online.title", 44))
	who = UiTheme.note("Who")
	col.add_child(who)
	status = UiTheme.note("Status")
	col.add_child(status)
	for page in PAGES:
		var b := Button.new()
		b.name = page[0]
		b.text = page[1]
		b.disabled = page[0] != "Help"
		var screen: String = page[2]
		var params: Dictionary = Router.params.duplicate()
		if page.size() > 3:
			params.kind = page[3]
		if not screen.is_empty():
			b.pressed.connect(func(): Router.push(screen, params))
		col.add_child(b)
		buttons.append(b)
	chat = buttons[5]
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(close)
	col.add_child(back)
	back.grab_focus.call_deferred()
	if online == null:
		status.text = tr("live.failed")
		return
	online.listen(self, &"pushed")
	status.text = tr("live.connecting")
	if online.entered:
		online.ask_profile(OnlineClient.later(self, &"entered"))
	else:
		online.enter(OnlineClient.later(self, &"entered"))


func entered(err: String) -> void:
	if not err.is_empty():
		status.text = tr("live.failed")
		return
	status.text = ""
	show_me()
	for i in buttons.size():
		buttons[i].disabled = str(PAGES[i][2]).is_empty()
	buttons[2].grab_focus.call_deferred()  # after Back's, asked for in _ready


func show_me() -> void:
	var m: Dictionary = online.me
	who.text = tr("online.who") % [str(m.get("name", "")), int(m.get("level", 1)), int(m.get("wins", 0)),
		int(m.get("losses", 0))]
	var waiting := int(online.unread[0]) + int(online.unread[1])
	chat.text = tr("online.chat") + (" (%d)" % waiting if waiting > 0 else "")


## A message from the server: a chat message counts as waiting; "kicked", another device took
## the player online.
func pushed(m: Dictionary) -> void:
	if m.t == "kicked":
		status.text = tr("online.kicked")
		for b in buttons:
			b.disabled = str(b.name) != "Help"
	elif m.t == "chat_push" and not online.me.is_empty():
		show_me()


func close() -> void:
	if online != null:
		online.leave()
	Router.back()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		close()
