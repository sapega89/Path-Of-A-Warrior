extends BaseScreen
## The town hall of a main camp: every colonel who gives missions, with how far the hero has
## come with him (Profile.progress, 5 per mission won; only his name while it is nothing yet),
## and the generals the hero knows, with their friendship (Profile.friendship, in the order he
## met them). Over them, the hero's flasks of living water (HeroRun) and his fame; the town hall
## of the start camp (Router.params.start) opens what comes before a run (the run setup screen:
## the starting skill, the flasks and the perks bought with fame).

const CELL_SCENE := preload("res://screens/town_hall/hall_cell.tscn")

var path: String = Profile.PATH
var profile: Profile
var campaign := Campaign.new()
var at_start := false  # the start camp's town hall: it opens the run setup
@onready var list: VBoxContainer = %List
@onready var flasks: Label = %Flasks
@onready var prepare: Button = %Prepare


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	at_start = bool(Router.params.get("start", false))
	_show_flasks()
	for r in colonels():
		_cell(%Colonels, colonel_line(r))
	%Nobody.visible = profile.friendship.is_empty()
	%Generals.visible = not profile.friendship.is_empty()
	for id in profile.friendship:
		var name_key := str(MapSim.general_data(int(id)).get("name", "?"))
		_cell(%Generals, tr("hall.friend") % [tr(name_key), int(profile.friendship[id])])
	%Back.grab_focus.call_deferred()


## How many flasks are bought and full, and the fame.
func _show_flasks() -> void:
	var run: HeroRun = profile.run
	flasks.text = (
		tr("hall.flasks") % [run.flasks, HeroRun.MAX_FLASKS, run.flasks_left, profile.fame]
	)
	prepare.visible = at_start


func open_run_setup() -> void:
	Router.push("run_setup", {"profile_path": path})


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
