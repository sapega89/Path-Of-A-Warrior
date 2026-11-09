class_name OnlineOrderScreen
extends BaseScreen
## Multiplayer > Order (pyport's Order window): my order's name and its members (the leader
## first, then me, who is online, the others), with Leave Order ("Leave the order?"). Without
## an order: Create Order and Join Order, a name of 4-12 letters (scripts/screens/
## online_text_screen.gd). A member online takes me into a battle with him: Mission Together
## or 2-on-2 Together (side by side against two CPU fighters); Duel > 2-on-2 Order and Mission
## > Order Ally open the list for one of them (Router.params.pick, the OnlineClient invite
## mode). The battle opens its screen by itself and comes back here.

var online: RefCounted
var title: Label
var info: Label
var list: VBoxContainer
var create: Button
var join: Button
var leave: Button
var ask: ConfirmationDialog
var together: ConfirmationDialog  # a member chosen: 2-on-2 Together (OK) or Mission Together
var pick := -1  # the invite mode a member is chosen for, -1 either
var chosen := ""  # the member's UserID


func _ready() -> void:
	online = OnlineClient.of(Router.params)
	pick = int(Router.params.get("pick", -1))
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
	together = ConfirmationDialog.new()
	together.name = "Together"
	together.ok_button_text = tr("online.together_2on2")
	together.add_button(tr("online.together_mission"), false, "mission")
	together.confirmed.connect(func(): invite(OnlineClient.TOGETHER))
	together.custom_action.connect(
		func(_a: StringName):
			together.hide()
			invite(OnlineClient.ALLY)
	)
	add_child(together)
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
	if inside and pick >= 0:
		info.text = tr(
			"online.pick_together" if pick == OnlineClient.TOGETHER else "online.pick_ally"
		)
	var me_id := str(online.me.get("id", ""))
	for m in online.members:
		var l := Button.new()
		l.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		l.text = (
			"%s%s  Lv%d%s"
			% [
				"* " if int(m.leader) else "",
				str(m.name),
				int(m.level),
				"  " + tr("online.online") if int(m.online) else ""
			]
		)
		var color := Color(0.5, 1, 0.5) if int(m.online) else Color(0.7, 0.7, 0.7)
		for state in ["font_color", "font_disabled_color", "font_hover_color", "font_focus_color"]:
			l.add_theme_color_override(state, color)
		l.disabled = not int(m.online) or str(m.id) == me_id
		var uid := str(m.id)
		l.pressed.connect(func(): choose(uid))
		list.add_child(l)
	create.visible = not inside
	join.visible = not inside
	leave.visible = inside and pick < 0  # the list opened for a battle: only the members
	var first: Control = leave if inside else create
	if pick >= 0:
		for b: Button in list.get_children():
			if not b.disabled and not b.is_queued_for_deletion():
				first = b
				break
	first.grab_focus.call_deferred()


## A member pressed: into the battle the list was opened for, else the choice of two.
func choose(uid: String) -> void:
	if online == null or online.busy:
		return
	chosen = uid
	if pick >= 0:
		invite(pick)
		return
	together.dialog_text = tr("online.together_ask") % uid
	together.popup_centered()


func invite(mode: int) -> void:
	info.text = tr("live.connecting")
	online.invite(mode, chosen, OnlineClient.later(self, &"invited"))


func invited(err: String) -> void:
	if err.is_empty():
		info.text = ""
		return
	var k := "online.err_" + err.replace(" ", "_")
	info.text = tr(k) if tr(k) != k else tr("live.failed")
