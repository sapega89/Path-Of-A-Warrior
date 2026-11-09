class_name OnlineCharacterScreen
extends BaseScreen
## Multiplayer > Character (pyport's Character menu): Records, Attributes, Skills,
## Exp/Fame/Gold, Change Quote, Display Name. Records, Attributes and Exp/Fame/Gold are read
## from the server and shown beside the menu; the others open their page.

## Button name, text key, what it does: a page shown here or a screen and its params.
const ITEMS := [
	["Records", "online.records", "records"],
	["Attributes", "online.attributes", "attributes"],
	["Skills", "online.skills", "online_skills"],
	["Purse", "online.purse", "purse"],
	["Quote", "online.quote", "online_text:quote"],
	["Name", "online.name", "online_text:name"],
]

var online: RefCounted
var info: Label
var buttons: Array[Button] = []


func _ready() -> void:
	online = OnlineClient.of(Router.params)
	var col := UiTheme.menu_column(self, 900)
	col.add_child(UiTheme.heading("online.character", 44))
	var row := HBoxContainer.new()  # the menu, and what it shows beside it
	row.name = "Row"
	row.add_theme_constant_override("separation", 24)
	col.add_child(row)
	var menu := VBoxContainer.new()
	menu.name = "Menu"
	menu.custom_minimum_size = Vector2(440, 0)
	menu.add_theme_constant_override("separation", 8)
	row.add_child(menu)
	for item in ITEMS:
		var b := Button.new()
		b.name = item[0]
		b.text = item[1]
		var what: String = item[2]
		b.pressed.connect(func(): open(what))
		menu.add_child(b)
		buttons.append(b)
	info = UiTheme.note("Info")
	info.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	info.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	row.add_child(info)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	buttons[0].grab_focus.call_deferred()


func open(what: String) -> void:
	if online == null or online.busy:
		return
	if what.begins_with("online_text:"):
		var p := Router.params.duplicate()
		p.kind = what.trim_prefix("online_text:")
		Router.push("online_text", p)
	elif what.begins_with("online_"):
		Router.push(what, Router.params)
	else:
		info.text = tr("live.connecting")
		match what:
			"records":
				online.ask_records(OnlineClient.later(self, &"show_records"))
			"attributes":
				online.ask_attributes(OnlineClient.later(self, &"show_attributes"))
			"purse":
				online.ask_purse(OnlineClient.later(self, &"show_purse"))


func show_records(err: String) -> void:
	if not err.is_empty():
		info.text = tr("live.failed")
		return
	var m: Dictionary = online.me
	var r: Dictionary = online.records
	var order := str(r.get("order", ""))
	info.text = "\n".join(
		[
			tr("online.level") % int(m.get("level", 1)),
			tr("online.fame") % int(r.get("fame", 0)),
			tr("online.duel_grade") % OnlineClient.grade(int(r.get("duel_grade", 0))),
			tr("online.wins") % [int(m.get("wins", 0)), int(m.get("losses", 0))],
			tr("online.mission_grade") % OnlineClient.grade(int(r.get("mission_grade", 0))),
			tr("online.order_line") % (order if not order.is_empty() else "-")
		]
	)


func show_attributes(err: String) -> void:
	if not err.is_empty():
		info.text = tr("live.failed")
		return
	var a: Dictionary = online.attributes
	var lines: Array = []
	for k in [["hp", "HP"], ["mp", "MP"], ["atk", "ATK"], ["def", "DEF"]]:
		var bonus := int(a.get(k[0] + "_bonus", 0))
		lines.append(
			"%s %d%s" % [k[1], int(a.get(k[0], 0)), (" + %d" % bonus) if bonus != 0 else ""]
		)
	info.text = "\n".join(lines)


func show_purse(err: String) -> void:
	if not err.is_empty():
		info.text = tr("live.failed")
		return
	var p: Dictionary = online.purse
	info.text = "\n".join(
		[
			tr("online.mp_exp") % int(p.get("exp", 0)),
			tr("online.mp_fame") % int(p.get("fame", 0)),
			tr("online.mp_gold") % int(p.get("gold", 0))
		]
	)
