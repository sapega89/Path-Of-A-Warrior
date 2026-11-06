extends Control
## Live, the market on the server (scripts/net/live_client.gd): Trade, Warehouse, Safe and
## Multiplayer. Opening it sends the hero's gold and backpack to the server; until the answer
## comes it says "Connecting...", and without one (no server, the connection broke) "Network
## connection has failed" with only Back.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const LiveClient := preload("res://scripts/net/live_client.gd")
## Page button name, text key, screen (empty: not open yet).
const PAGES := [
	["Trade", "live.trade", ""],
	["Warehouse", "live.warehouse", "live_warehouse"],
	["Safe", "live.safe", "live_safe"],
	["Multiplayer", "live.multiplayer", ""],
]

var live: RefCounted
var profile: RefCounted
var status: Label
var buttons: Array[Button] = []
var back: Button


func _ready() -> void:
	profile = Profile.load_or_new(str(Router.params.get("profile_path", Profile.PATH)))
	live = LiveClient.of(Router.params)
	var col := UiTheme.menu_column(self)
	col.add_child(UiTheme.heading("live.title", 44))
	status = UiTheme.note("Status")
	col.add_child(status)
	for page in PAGES:
		var b := Button.new()
		b.name = page[0]
		b.text = page[1]
		b.disabled = true
		var screen: String = page[2]
		if not screen.is_empty():
			b.pressed.connect(func(): Router.push(screen, Router.params))
		col.add_child(b)
		buttons.append(b)
	back = Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	back.grab_focus.call_deferred()
	if live == null:
		status.text = tr("live.failed")
		return
	status.text = tr("live.connecting")
	live.sync(profile, LiveClient.later(self, &"synced"))


## The answer to the sync: the pages open, or the connection failed.
func synced(err: String) -> void:
	status.text = "" if err.is_empty() else tr("live.failed")
	for i in buttons.size():
		buttons[i].disabled = not err.is_empty() or str(PAGES[i][2]).is_empty()
	for b in buttons:
		if not b.disabled:
			b.grab_focus.call_deferred()  # after Back's, asked for in _ready
			break


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
