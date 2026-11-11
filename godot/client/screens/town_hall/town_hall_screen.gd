extends BaseScreen
## The town hall of the start camp (the only camp that has one, CampPlan.has_hall): what comes
## before a run (Prepare: the run setup screen, the starting skill, the flasks, the perks and the
## vows), over it the hero's flasks of living water (HeroRun) and his fame, and the generals the
## hero knows, with their friendship (Profile.friendship, in the order he met them).

const CELL_SCENE := preload("res://screens/town_hall/hall_cell.tscn")

var path: String = Profile.PATH
var profile: Profile
@onready var list: VBoxContainer = %List
@onready var flasks: Label = %Flasks
@onready var prepare: Button = %Prepare


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	_show_flasks()
	%Nobody.visible = profile.friendship.is_empty()
	%Generals.visible = not profile.friendship.is_empty()
	for id in profile.friendship:
		var name_key := str(MapSim.general_data(int(id)).get("name", "?"))
		_line(tr("hall.friend") % [tr(name_key), int(profile.friendship[id])])
	%Back.grab_focus.call_deferred()


## How many flasks are bought and full, and the fame.
func _show_flasks() -> void:
	var run: HeroRun = profile.run
	flasks.text = (
		tr("hall.flasks") % [run.flasks, HeroRun.MAX_FLASKS, run.flasks_left, profile.fame]
	)


func open_run_setup() -> void:
	Router.push("run_setup", {"profile_path": path})


## A line of the list of generals (hall_cell.tscn).
func _line(text: String) -> void:
	var l: Label = CELL_SCENE.instantiate()
	l.text = text
	%Generals.add_child(l)
