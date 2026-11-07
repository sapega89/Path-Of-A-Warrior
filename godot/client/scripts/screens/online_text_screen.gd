extends Control
## A line to type for the online game (Router.params.kind):
##   quote         Change Quote: the battle's first words and the victory quote (1-20 characters)
##   order_create  Create Order / order_join  Join Order: 4-12 letters A-Z
##   peer          Chat > New Message: the UserID of the player (4-12 letters A-Z)
##   challenge1    Duel > Challenge 1:1 / challenge2 Challenge 2:2 / ally Mission > Invite An
##                 Ally: the UserID of the player taken into the battle
## OK sends it; the server's "not acceptable" or "name exists" are shown under it. Done, the
## screen goes back (peer: on to the conversation; a battle opens its screen by itself).

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const OnlineClient := preload("res://scripts/net/online_client.gd")
const Protocol := preload("res://scripts/net/protocol.gd")
const INVITES := {"challenge1": OnlineClient.CHALLENGE_1, "challenge2": OnlineClient.CHALLENGE_2,
	"ally": OnlineClient.ALLY}

var online: RefCounted
var kind := "quote"
var fields: Array[LineEdit] = []
var info: Label


func _ready() -> void:
	online = OnlineClient.of(Router.params)
	kind = str(Router.params.get("kind", "quote"))
	var col := UiTheme.menu_column(self, 560)
	col.add_child(UiTheme.heading("online.title_" + kind, 40))
	var hint := UiTheme.note("Hint")
	hint.text = tr("online.hint_" + kind)
	col.add_child(hint)
	var me: Dictionary = online.me if online != null else {}
	match kind:
		"quote":
			_field(col, "Start", 20, str(me.get("quote_start", "")))
			_field(col, "Win", 20, str(me.get("quote_win", "")))
		_:
			_field(col, "Text", 12, "")
	var ok := Button.new()
	ok.name = "Ok"
	ok.text = "live.ok"
	ok.pressed.connect(submit)
	col.add_child(ok)
	info = UiTheme.note("Info", 60)
	col.add_child(info)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	fields[0].grab_focus.call_deferred()


func _field(col: VBoxContainer, node_name: String, max_len: int, text: String) -> void:
	var e := LineEdit.new()
	e.name = node_name
	e.max_length = max_len
	e.alignment = HORIZONTAL_ALIGNMENT_CENTER
	e.text = text
	e.text_changed.connect(func(t: String) -> void: _keep(e, t))
	e.text_submitted.connect(func(_t: String) -> void: submit())
	col.add_child(e)
	fields.append(e)


## Only what the kind allows: A-Z (typed in any case) for a UserID or an order,
## printable ASCII for a quote.
func _keep(e: LineEdit, t: String) -> void:
	var clean := ""
	for c in t:
		match kind:
			"quote":
				if c >= " " and c <= "~":
					clean += c
			_:
				var u := c.to_upper()
				if u >= "A" and u <= "Z":
					clean += u
	if clean != t:
		var at := e.caret_column
		e.text = clean
		e.caret_column = mini(at, clean.length())


## What is wrong with the typed text, "" when it may be sent.
func problem() -> String:
	var t := fields[0].text
	match kind:
		"quote":
			return "" if not t.strip_edges().is_empty() and not fields[1].text.strip_edges().is_empty() \
				else tr("online.err_not_acceptable")
	return "" if Protocol.valid_id(t) else tr("online.err_not_acceptable")


func submit() -> void:
	if online == null or online.busy:
		return
	var p := problem()
	if not p.is_empty():
		info.text = p
		return
	send()


func send() -> void:
	if online == null or online.busy:
		return
	info.text = tr("live.connecting")
	var t := fields[0].text
	match kind:
		"quote":
			online.set_quote("start", t.strip_edges(), OnlineClient.later(self, &"quoted"))
		"order_create":
			online.order_create(t, OnlineClient.later(self, &"done"))
		"order_join":
			online.order_join(t, OnlineClient.later(self, &"done"))
		"challenge1", "challenge2", "ally":
			if t == str(online.me.get("id", "")):
				info.text = tr("online.err_self_invite")
				return
			online.invite(int(INVITES[kind]), t, OnlineClient.later(self, &"done"))
		"peer":
			if t == str(online.me.get("id", "")):
				info.text = tr("online.err_self")
				return
			var params := Router.params.duplicate()
			params.channel = OnlineClient.PRIVATE
			params.peer = t
			Router.back()
			Router.push("online_chat", params)


## The first quote went through: now the victory quote.
func quoted(err: String) -> void:
	if not err.is_empty():
		done(err)
		return
	online.set_quote("win", fields[1].text.strip_edges(), OnlineClient.later(self, &"done"))


func done(err: String) -> void:
	if err.is_empty():
		Router.back()
		return
	var k := "online.err_" + err.replace(" ", "_")
	info.text = tr(k) if tr(k) != k else tr("live.failed")


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
