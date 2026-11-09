class_name OnlineBattlesScreen
extends BaseScreen
## Multiplayer > Duel or Mission (Router.params.kind "duel" / "mission"): the ways into a
## battle. Duel: 1-on-1 Duel and 2-on-2 Duel (an opponent of about my level, else the CPU),
## Challenge 1:1 and Challenge 2:2 (a player by UserID), 2-on-2 Order (side by side with a
## member of my order). Mission: Solo Mission (with a CPU ally), Invite An Ally (by UserID),
## Order Ally (a member of my order). While a duel waits for an opponent it says "Searching
## for opponent..." with Cancel. The battle screen opens by itself when the battle starts
## (OnlineClient.on_battle) and comes back here after it.

## Button name, text key, what it does: ["find", mode] / ["type", text screen kind] /
## ["order", invite mode].
const CHOICES := {
	"duel":
	[
		["Duel1", "online.duel_1on1", ["find", 0]],
		["Duel2", "online.duel_2on2", ["find", 1]],
		["Challenge1", "online.challenge_1", ["type", "challenge1"]],
		["Challenge2", "online.challenge_2", ["type", "challenge2"]],
		["Order", "online.duel_order", ["order", OnlineClient.TOGETHER]],
	],
	"mission":
	[
		["Solo", "online.mission_solo", ["find", 2]],
		["Ally", "online.mission_ally", ["type", "ally"]],
		["Order", "online.mission_order", ["order", OnlineClient.ALLY]],
	],
}

var online: RefCounted
var kind := "duel"
var buttons: Array[Button] = []
var status: Label
var cancel: Button
var _ticks := 0.0


func _ready() -> void:
	online = OnlineClient.of(Router.params)
	kind = str(Router.params.get("kind", "duel"))
	if not CHOICES.has(kind):
		kind = "duel"
	var col := UiTheme.menu_column(self, 560)
	col.add_child(UiTheme.heading("online." + kind, 44))
	status = UiTheme.note("Status", 44)
	col.add_child(status)
	for c in CHOICES[kind]:
		var b := Button.new()
		b.name = c[0]
		b.text = c[1]
		var what: Array = c[2]
		b.pressed.connect(func(): choose(what))
		col.add_child(b)
		buttons.append(b)
	cancel = Button.new()
	cancel.name = "Cancel"
	cancel.text = "online.cancel_search"
	cancel.pressed.connect(stop_waiting)
	cancel.visible = false
	col.add_child(cancel)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(close)
	col.add_child(back)
	if online == null:
		status.text = tr("live.failed")
		for b in buttons:
			b.disabled = true
		back.grab_focus.call_deferred()
		return
	buttons[0].grab_focus.call_deferred()
	_show_waiting()


func choose(what: Array) -> void:
	if online == null or online.busy or online.waiting:
		return
	match str(what[0]):
		"find":
			status.text = tr("live.connecting")
			online.find_battle(int(what[1]), OnlineClient.later(self, &"found"))
		"type":
			var p := Router.params.duplicate()
			p.kind = what[1]
			Router.push("online_text", p)
		"order":
			var p := Router.params.duplicate()
			p.pick = int(what[1])
			Router.push("online_order", p)


## The answer to Duel / Solo Mission: waiting for an opponent, or the battle has started
## (its screen is on by now).
func found(err: String) -> void:
	if not err.is_empty():
		status.text = error_text(err)
		return
	status.text = ""
	_show_waiting()


func _show_waiting() -> void:
	var w: bool = online.waiting
	cancel.visible = w
	for b in buttons:
		b.disabled = w
	if w:
		status.text = tr("online.searching")
		cancel.grab_focus.call_deferred()


func _process(delta: float) -> void:
	if online == null or not online.waiting:
		return
	_ticks += delta
	status.text = tr("online.searching") + ".".repeat(int(_ticks * 2.0) % 4)


func stop_waiting() -> void:
	if online == null or not online.waiting:
		return
	online.cancel_battle(OnlineClient.later(self, &"stopped"))


func stopped(_err: String) -> void:
	status.text = ""
	_show_waiting()
	buttons[0].grab_focus.call_deferred()


## Back: no more waiting, then the game menu.
func close() -> void:
	if online != null and online.waiting:
		online.cancel_battle(func(_e: String) -> void: pass)
	Router.back()


func error_text(err: String) -> String:
	var k := "online.err_" + err.replace(" ", "_")
	return tr(k) if tr(k) != k else tr("live.failed")


func go_back() -> void:
	close()
