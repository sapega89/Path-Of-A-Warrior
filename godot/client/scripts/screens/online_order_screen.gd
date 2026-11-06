extends Control
## Multiplayer > Order (pyport's Order window): my order's name and its members (the leader
## first, then me, who is online, the others), with Leave Order ("Leave the order?"). Without
## an order: Create Order and Join Order, a name of 4-12 letters (scripts/screens/
## online_text_screen.gd).

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const OnlineClient := preload("res://scripts/net/online_client.gd")

var online: RefCounted
var title: Label
var info: Label
var list: VBoxContainer
var create: Button
var join: Button
var leave: Button
var ask: ConfirmationDialog


func _ready() -> void:
	online = OnlineClient.of(Router.params)
	var col := UiTheme.menu_column(self, 640)
	col.add_child(UiTheme.heading("online.order", 44))
	title = UiTheme.note("Name")
	title.add_theme_font_size_override("font_size", 32)
	title.add_theme_color_override("font_color", UiTheme.ACCENT)
	col.add_child(title)
	list = VBoxContainer.new()
	list.name = "Members"
	list.add_theme_constant_override("separation", 2)
	col.add_child(list)
	info = UiTheme.note("Info", 40)
	col.add_child(info)
	create = _button(col, "Create", "online.order_create", func(): _type("order_create"))
	join = _button(col, "Join", "online.order_join", func(): _type("order_join"))
	leave = _button(col, "Leave", "online.order_leave", func(): ask.popup_centered())
	var back := _button(col, "Back", "common.back", func(): Router.back())
	for b in [create, join, leave]:
		b.visible = false
	ask = ConfirmationDialog.new()
	ask.name = "Ask"
	ask.dialog_text = tr("online.order_leave_ask")
	ask.confirmed.connect(func(): online.order_leave(OnlineClient.later(self, &"shown")))
	add_child(ask)
	back.grab_focus.call_deferred()
	if online == null:
		info.text = tr("live.failed")
		return
	info.text = tr("live.connecting")
	online.ask_order(OnlineClient.later(self, &"shown"))


func _button(col: VBoxContainer, node_name: String, key: String, press: Callable) -> Button:
	var b := Button.new()
	b.name = node_name
	b.text = key
	b.pressed.connect(press)
	col.add_child(b)
	return b


func _type(kind: String) -> void:
	var p := Router.params.duplicate()
	p.kind = kind
	Router.push("online_text", p)


func shown(err: String) -> void:
	if not err.is_empty():
		info.text = tr("live.failed")
		return
	for c in list.get_children():
		c.queue_free()
	var inside := not str(online.order_name).is_empty()
	title.text = online.order_name
	info.text = "" if inside else tr("online.no_order")
	for m in online.members:
		var l := Label.new()
		l.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		l.text = "%s%s  Lv%d%s" % ["* " if int(m.leader) else "", str(m.name), int(m.level),
			"  " + tr("online.online") if int(m.online) else ""]
		l.add_theme_color_override("font_color", Color(0.5, 1, 0.5) if int(m.online) else Color(0.7, 0.7, 0.7))
		list.add_child(l)
	create.visible = not inside
	join.visible = not inside
	leave.visible = inside
	(leave if inside else create).grab_focus.call_deferred()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
