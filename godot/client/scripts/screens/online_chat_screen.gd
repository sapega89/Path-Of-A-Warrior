extends Control
## Multiplayer > Chat (pyport's Chat window): three tabs, Lobby (everyone online), Order (my
## order) and Private (my conversations, the newest first, with the messages waiting in each;
## New Message asks for a UserID). A conversation shows its last 30 messages and a line to
## write (up to 40 characters). The server sends every new message to whoever is online, so
## the page grows as they come; the tabs count what waits in the others.
## Router.params: channel (0 Lobby, 1 Order, 2 Private) and peer (a private conversation).

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const OnlineClient := preload("res://scripts/net/online_client.gd")
const TABS := [["Lobby", "online.lobby"], ["OrderTab", "online.order"], ["Private", "online.private"]]

var online: RefCounted
var channel := 0
var peer := ""
var title: Label
var tabs: Array[Button] = []
var scroll: ScrollContainer
var lines: VBoxContainer
var write: HBoxContainer
var line: LineEdit
var new_message: Button
var info: Label


func _ready() -> void:
	online = OnlineClient.of(Router.params)
	channel = clampi(int(Router.params.get("channel", 0)), 0, 2)
	peer = str(Router.params.get("peer", ""))
	var col := UiTheme.menu_column(self, 760)
	title = UiTheme.heading("online.chat", 40)
	title.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	col.add_child(title)
	var row := HBoxContainer.new()
	row.name = "Tabs"
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	for i in TABS.size():
		var b := Button.new()
		b.name = TABS[i][0]
		b.custom_minimum_size = Vector2(220, 0)
		b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		b.pressed.connect(func(): open(i, ""))
		row.add_child(b)
		tabs.append(b)
	col.add_child(row)
	row.visible = peer.is_empty()
	scroll = ScrollContainer.new()
	scroll.name = "Scroll"
	scroll.custom_minimum_size = Vector2(0, 330)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	lines = VBoxContainer.new()
	lines.name = "Lines"
	lines.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	lines.add_theme_constant_override("separation", 2)
	scroll.add_child(lines)
	col.add_child(scroll)
	new_message = Button.new()
	new_message.name = "NewMessage"
	new_message.text = "online.new_message"
	new_message.pressed.connect(func():
		var p := Router.params.duplicate()
		p.kind = "peer"
		Router.push("online_text", p))
	col.add_child(new_message)
	write = HBoxContainer.new()
	write.name = "Write"
	line = LineEdit.new()
	line.name = "Line"
	line.max_length = OnlineClient.MAX_TEXT
	line.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	line.placeholder_text = tr("online.write_hint")
	line.text_changed.connect(_keep)
	line.text_submitted.connect(func(_t: String) -> void: submit())
	write.add_child(line)
	var send := Button.new()
	send.name = "Send"
	send.text = "online.send"
	send.pressed.connect(submit)
	write.add_child(send)
	col.add_child(write)
	info = UiTheme.note("Info", 36)
	col.add_child(info)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	if online == null:
		info.text = tr("live.failed")
		write.visible = false
		new_message.visible = false
		return
	online.listen(self, &"pushed")
	open(channel, peer)


func _exit_tree() -> void:
	if online != null:
		online.reading = ""


func _keep(t: String) -> void:
	var clean := OnlineClient.clean_text(t)
	if clean != t:
		var at := line.caret_column
		line.text = clean
		line.caret_column = mini(at, clean.length())


func current() -> String:
	return OnlineClient.key(channel, peer)


func list_open() -> bool:
	return channel == OnlineClient.PRIVATE and peer.is_empty()


## A tab, or a private conversation (peer).
func open(ch: int, with: String) -> void:
	if online.busy:
		return
	channel = ch
	peer = with
	online.reading = "" if list_open() else current()
	title.text = tr("online.chat") if peer.is_empty() else tr("online.with") % peer
	new_message.visible = list_open()
	write.visible = false
	info.text = tr("live.connecting")
	_tab_texts()
	if list_open():
		online.ask_peers(OnlineClient.later(self, &"peers_shown"))
	else:
		online.read_chat(channel, peer, OnlineClient.later(self, &"read"))


func _tab_texts() -> void:
	var counts := [0, int(online.unread[0]), int(online.unread[1])]
	for i in tabs.size():
		tabs[i].text = tr(TABS[i][1]) + (" (%d)" % counts[i] if counts[i] > 0 and i != channel else "")
		tabs[i].modulate = Color(1, 0.85, 0.4) if i == channel else Color.WHITE


func _clear() -> void:
	for c in lines.get_children():
		lines.remove_child(c)
		c.queue_free()


func read(err: String) -> void:
	_clear()
	_tab_texts()
	if err == "no order":
		info.text = tr("online.no_order")
		return
	if not err.is_empty():
		info.text = tr("live.failed")
		return
	if not peer.is_empty():
		title.text = tr("online.with") % online.peer_name
	write.visible = true
	show_lines()
	line.grab_focus.call_deferred()


func show_lines() -> void:
	_clear()
	var rows: Array = online.chat.get(current(), [])
	info.text = "" if not rows.is_empty() else tr("online.no_messages")
	var my_id := str(online.me.get("id", ""))
	for r in rows:
		var l := Label.new()
		l.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		l.text = "%s: %s" % [r.name, r.text]
		if str(r.id) == my_id:
			l.add_theme_color_override("font_color", UiTheme.ACCENT)
		lines.add_child(l)
	_to_bottom.call_deferred()


func _to_bottom() -> void:
	if is_inside_tree():
		scroll.scroll_vertical = int(scroll.get_v_scroll_bar().max_value)


func peers_shown(err: String) -> void:
	_clear()
	_tab_texts()
	if not err.is_empty():
		info.text = tr("live.failed")
		return
	info.text = "" if not online.peers.is_empty() else tr("online.no_conversations")
	for p in online.peers:
		var b := Button.new()
		b.name = "Peer" + str(p.id)
		b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		b.text = "%s%s%s" % [p.name, " (%d)" % int(p.unread) if int(p.unread) > 0 else "",
			"  " + tr("online.online") if int(p.online) else ""]
		var id := str(p.id)
		b.pressed.connect(func():
			var params := Router.params.duplicate()
			params.channel = OnlineClient.PRIVATE
			params.peer = id
			Router.push("online_chat", params))
		lines.add_child(b)
	(lines.get_child(0) if lines.get_child_count() > 0 else new_message).grab_focus.call_deferred()


func submit() -> void:
	if online == null or online.busy or not write.visible:
		return
	var t := OnlineClient.clean_text(line.text.strip_edges())
	if t.is_empty():
		return
	online.send_chat(channel, peer, t, OnlineClient.later(self, &"sent"))


func sent(err: String) -> void:
	if err.is_empty():
		line.clear()
		info.text = ""
		return
	var k := "online.err_" + err.replace(" ", "_")
	info.text = tr(k) if tr(k) != k else tr("live.failed")


## A message came: shown here when it is this conversation's (and counted read), else the
## tabs count it.
func pushed(m: Dictionary) -> void:
	if m.t != "chat_push":
		return
	var k := OnlineClient.key(int(m.channel), str(m.peer))
	if k == current() and not list_open():
		show_lines()
		if channel != OnlineClient.LOBBY and not online.busy:
			online.read_chat(channel, peer, func(_e: String) -> void: pass)  # read: not waiting
	elif list_open() and int(m.channel) == OnlineClient.PRIVATE and not online.busy:
		online.ask_peers(OnlineClient.later(self, &"peers_shown"))
	_tab_texts()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
