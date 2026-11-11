extends BaseScreen
## The town hall of a main camp: every colonel who gives missions, with how far the hero has
## come with him (Profile.progress, 5 per mission won; only his name while it is nothing yet),
## and the generals the hero knows, with their friendship (Visits.generals). Visiting opens the
## visits from here. Over them, the hero's flasks of living water (HeroRun) and his fame; in the
## town hall of the start camp (Router.params.start) the next flask is sold for fame.

var path: String = Profile.PATH
var profile: RefCounted
var campaign := Campaign.new()
var at_start := false  # the start camp's town hall: it sells the flasks
@onready var list: VBoxContainer = %List
@onready var visit: Button = %Visit
@onready var flasks: Label = %Flasks
@onready var buy: Button = %BuyFlask


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	at_start = bool(Router.params.get("start", false))
	_show_flasks()
	_section("hall.colonels")
	var grid := _grid("Colonels")
	for r in colonels():
		_cell(grid, colonel_line(r))
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


## How many flasks are bought and full, and the fame; at the start the next flask's price.
func _show_flasks() -> void:
	var run: HeroRun = profile.run
	flasks.text = (
		tr("hall.flasks") % [run.flasks, HeroRun.MAX_FLASKS, run.flasks_left, profile.fame]
	)
	var price := run.flask_price()
	buy.visible = at_start and price > 0
	buy.text = tr("hall.buy_flask") % price
	buy.disabled = profile.fame < price


func buy_flask() -> void:
	if profile.run.buy_flask(profile):
		profile.save(path)
	_show_flasks()


func open_visits() -> void:
	Router.push("visiting", {"profile_path": path})


## A colonel's line: his name, and how far the hero has come with him once it is something.
func colonel_line(colonel: Array) -> String:
	var name_text := tr(str(colonel[1]))
	var done := int(profile.progress.get(str(colonel[0]), 0))
	return name_text if done <= 0 else tr("hall.progress") % [name_text, done]


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
