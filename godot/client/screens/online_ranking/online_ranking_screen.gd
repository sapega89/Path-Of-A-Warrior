class_name OnlineRankingScreen
extends BaseScreen
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
@onready var rows: Array[Label] = [%Row1, %Row2, %Row3]
@onready var mine: Label = %Mine


func _ready() -> void:
	online = OnlineClient.of(Router.params)
	cat_buttons.assign(%Categories.get_children())
	view_buttons.assign(%Views.get_children())
	cat_buttons[0].grab_focus.call_deferred()
	choose(1, false)


func _on_category(i: int) -> void:
	choose(i + 1, near)


func _on_view(i: int) -> void:
	choose(cat, i == 1)


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
