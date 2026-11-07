extends Control
## The town hall of a main camp: every colonel who gives missions, with how far the hero has
## come with him (Profile.progress, 5 per mission won), and the generals the hero knows, with
## their friendship (Visits.generals). Visiting opens the visits from here.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Campaign := preload("res://scripts/core/campaign.gd")
const Visits := preload("res://scripts/core/visits.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")

var path: String = Profile.PATH
var profile: RefCounted
var campaign := Campaign.new()
var list: VBoxContainer
var visit: Button


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	profile = Profile.load_or_new(path)
	var col := UiTheme.menu_column(self, 760)
	col.add_child(UiTheme.heading("camp.hall", 40))
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size = Vector2(760, 500)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	col.add_child(scroll)
	list = VBoxContainer.new()
	list.name = "List"
	list.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(list)
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
	var row := HBoxContainer.new()
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	row.add_theme_constant_override("separation", 12)
	col.add_child(row)
	visit = Button.new()
	visit.name = "Visit"
	visit.text = "hall.visits"
	visit.disabled = not Visits.can_visit(profile)
	visit.pressed.connect(func(): Router.push("visiting", {"profile_path": path}))
	row.add_child(visit)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	row.add_child(back)
	(back if visit.disabled else visit).grab_focus.call_deferred()


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


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
