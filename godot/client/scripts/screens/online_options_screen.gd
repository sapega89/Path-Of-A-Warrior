extends Control
## Multiplayer > Options: Invitation, Accept or Deny (pyport's Options > Invitation): whether
## another player's Challenge or Invite An Ally takes me into the battle. It is kept on the
## server.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const OnlineClient := preload("res://scripts/net/online_client.gd")

var online: RefCounted
var accept: Button
var deny: Button
var info: Label


func _ready() -> void:
	online = OnlineClient.of(Router.params)
	var col := UiTheme.menu_column(self, 560)
	col.add_child(UiTheme.heading("online.options", 44))
	var label := Label.new()
	label.text = "online.invitation"
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	col.add_child(label)
	var row := HBoxContainer.new()
	row.name = "Invitation"
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	accept = Button.new()
	accept.name = "Accept"
	accept.text = "online.accept"
	accept.custom_minimum_size = Vector2(200, 0)
	accept.pressed.connect(choose.bind(1))
	row.add_child(accept)
	deny = Button.new()
	deny.name = "Deny"
	deny.text = "online.deny"
	deny.custom_minimum_size = Vector2(200, 0)
	deny.pressed.connect(choose.bind(0))
	row.add_child(deny)
	col.add_child(row)
	info = UiTheme.note("Info", 80)
	col.add_child(info)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	accept.grab_focus.call_deferred()
	if online == null:
		info.text = tr("live.failed")
		return
	info.text = tr("live.connecting")
	online.ask_options(OnlineClient.later(self, &"shown"))


func shown(err: String) -> void:
	if not err.is_empty():
		info.text = tr("live.failed")
		return
	info.text = tr("online.invitation_" + ("accept" if online.invitation == 1 else "deny"))
	accept.modulate = Color(1, 0.85, 0.4) if online.invitation == 1 else Color.WHITE
	deny.modulate = Color(1, 0.85, 0.4) if online.invitation == 0 else Color.WHITE


func choose(v: int) -> void:
	if online == null or online.busy:
		return
	info.text = tr("live.connecting")
	online.set_invitation(v, OnlineClient.later(self, &"shown"))


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
