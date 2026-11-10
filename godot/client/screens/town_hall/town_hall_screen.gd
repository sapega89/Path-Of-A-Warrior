extends BaseScreen
## The town hall of a main camp: every colonel who gives missions, with how far the hero has
## come with him (Profile.progress, 5 per mission won), and the generals the hero knows, with
## their friendship (Visits.generals). Visiting opens the visits from here.

var path: String = Profile.PATH
var profile: RefCounted
var campaign := Campaign.new()
@onready var list: VBoxContainer = %List
@onready var visit: Button = %Visit


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	_section("hall.colonels")
	var grid := _grid("Colonels")
	for r in colonels():
		_cell(grid, tr("hall.progress") % [tr(str(r[1])), int(profile.progress.get(str(r[0]), 0))])
	_section("hall.generals")
	var gens: Array = Visits.generals(profile)
	if gens.is_empty():
		var none := UiTheme.note("Nobody")
		none.text = tr("hall.nobody")
		list.add_child(none)
	else:
		grid = _grid("Generals")
		for g in gens:
			var name_key := str(MapSim.general_data(int(g[0])).get("name", "?"))
			_cell(grid, tr("hall.friend") % [tr(name_key), int(g[1])])
	visit.disabled = not Visits.can_visit(profile)
	(%Back if visit.disabled else visit).grab_focus.call_deferred()


func open_visits() -> void:
	Router.push("visiting", {"profile_path": path})


## Every colonel who gives missions: [[ruler id, name], ...] by id.
func colonels() -> Array:
	var seen := {}
	for m in campaign.missions:
		var id := int(m.get("id", 0))
		if not seen.has(id):
			seen[id] = str(m.get("name", ""))
	var ids := seen.keys()
	ids.sort()
	return ids.map(func(id): return [id, seen[id]])


func _section(key: String) -> void:
	var l := Label.new()
	l.text = key
	l.add_theme_color_override("font_color", UiTheme.ACCENT)
	list.add_child(l)


func _grid(node_name: String) -> GridContainer:
	var g := GridContainer.new()
	g.name = node_name
	g.columns = 2
	g.add_theme_constant_override("h_separation", 24)
	list.add_child(g)
	return g


func _cell(grid: GridContainer, text: String) -> void:
	var l := Label.new()
	l.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	l.text = text
	l.custom_minimum_size = Vector2(360, 0)
	l.add_theme_font_size_override("font_size", 22)
	l.clip_text = true
	grid.add_child(l)
