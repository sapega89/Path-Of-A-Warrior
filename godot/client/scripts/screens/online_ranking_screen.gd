class_name OnlineRankingScreen
extends Control
## Multiplayer > Ranking (pyport's Ranking menu): Fame, Duel or Mission, the Top Rankers or the
## Ranks Near Me, three rows each, and my own rank under them. Duel and Mission rank by grade.

const CATEGORIES := [
	["Fame", "online.rank_fame"], ["Duel", "online.rank_duel"], ["Mission", "online.rank_mission"]
]
const VIEWS := [["Top", "online.rank_top"], ["Near", "online.rank_near"]]

var online: RefCounted
var cat := 1
var near := false
var cat_buttons: Array[Button] = []
var view_buttons: Array[Button] = []
var rows: Array[Label] = []
var mine: Label


func _ready() -> void:
	online = OnlineClient.of(Router.params)
	var col := UiTheme.menu_column(self, 640)
	col.add_child(UiTheme.heading("online.ranking", 44))
	cat_buttons = _row(col, "Categories", CATEGORIES, func(i): choose(i + 1, near))
	view_buttons = _row(col, "Views", VIEWS, func(i): choose(cat, i == 1))
	for i in 3:
		var l := UiTheme.note("Row%d" % (i + 1))
		l.add_theme_font_size_override("font_size", 28)
		col.add_child(l)
		rows.append(l)
	mine = UiTheme.note("Mine", 40)
	col.add_child(mine)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	cat_buttons[0].grab_focus.call_deferred()
	choose(1, false)


func _row(col: VBoxContainer, node_name: String, items: Array, press: Callable) -> Array[Button]:
	var row := HBoxContainer.new()
	row.name = node_name
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	var out: Array[Button] = []
	for i in items.size():
		var b := Button.new()
		b.name = items[i][0]
		b.text = items[i][1]
		b.custom_minimum_size = Vector2(190, 0)
		b.pressed.connect(press.bind(i))
		row.add_child(b)
		out.append(b)
	col.add_child(row)
	return out


func choose(category: int, near_me: bool) -> void:
	if online == null:
		mine.text = tr("live.failed")
		return
	if online.busy:
		return
	cat = category
	near = near_me
	for i in cat_buttons.size():
		cat_buttons[i].modulate = Color(1, 0.85, 0.4) if i + 1 == cat else Color.WHITE
	for i in view_buttons.size():
		view_buttons[i].modulate = Color(1, 0.85, 0.4) if (i == 1) == near else Color.WHITE
	mine.text = tr("live.connecting")
	online.ask_rank(cat, near, OnlineClient.later(self, &"ranked"))


func value_text(v: int) -> String:
	return str(v) if cat == 1 else OnlineClient.grade(v)


func ranked(err: String) -> void:
	if not err.is_empty():
		mine.text = tr("live.failed")
		return
	for i in 3:
		var r: Dictionary = online.rank_rows[i] if i < online.rank_rows.size() else {}
		var at := int(r.get("rank", 0))
		rows[i].text = "%d.  %s  %s" % [at, str(r.id), value_text(int(r.value))] if at > 0 else "-"
		rows[i].add_theme_color_override(
			"font_color",
			UiTheme.ACCENT if at > 0 and str(r.id) == str(online.me.get("id", "")) else Color.WHITE
		)
	mine.text = (
		tr("online.my_rank") % [int(online.rank.rank), value_text(int(online.rank.value))]
		if not online.rank.is_empty()
		else tr("online.no_rank")
	)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
