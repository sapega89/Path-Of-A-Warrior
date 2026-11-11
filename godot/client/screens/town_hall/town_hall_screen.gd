extends BaseScreen
## The town hall of a main camp: every colonel who gives missions, with how far the hero has
## come with him (Profile.progress, 5 per mission won; only his name while it is nothing yet),
## and the generals the hero knows, with their friendship (Visits.generals). Visiting opens the
## visits from here.

const CELL_SCENE := preload("res://screens/town_hall/hall_cell.tscn")

var path: String = Profile.PATH
var profile: Profile
var campaign := Campaign.new()
@onready var list: VBoxContainer = %List
@onready var visit: Button = %Visit


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	for r in colonels():
		_cell(%Colonels, colonel_line(r))
	var gens: Array = Visits.generals(profile)
	%Nobody.visible = gens.is_empty()
	%Generals.visible = not gens.is_empty()
	for g in gens:
		var name_key := str(MapSim.general_data(int(g[0])).get("name", "?"))
		_cell(%Generals, tr("hall.friend") % [tr(name_key), int(g[1])])
	visit.disabled = not Visits.can_visit(profile)
	(%Back if visit.disabled else visit).grab_focus.call_deferred()


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


## A line of a list (hall_cell.tscn): a colonel or a general.
func _cell(grid: GridContainer, text: String) -> void:
	var l: Label = CELL_SCENE.instantiate()
	l.text = text
	grid.add_child(l)
