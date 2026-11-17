class_name TestGroundScreen
extends BaseScreen
## The test ground (main menu -> Test Ground): a button for each map of the campaign. One opens
## the first mission of its map as the test ground plays it (TestMissionScreen: the hero cannot
## die, nothing is saved); coming back, the map opened last has the focus. Back leaves.

const ROW_SCENE := preload("res://screens/test_ground/map_button.tscn")

@onready var maps: GridContainer = %Maps


func _ready() -> void:
	var campaign := Campaign.new()
	for n in range(1, MapBuilder.map_count() + 1):
		var b: Button = ROW_SCENE.instantiate()
		b.name = "Map%d" % n
		b.text = "%d. %s" % [n, campaign.lord_name(n)]
		b.pressed.connect(open.bind(n))
		maps.add_child(b)
	_focus_last.call_deferred()


## The map opened last (the first at the start) takes the focus once the screen is shown.
func _focus_last() -> void:
	if is_inside_tree():
		var last := clampi(int(Router.params.get("map", 1)), 1, maps.get_child_count())
		(maps.get_child(last - 1) as Button).grab_focus()


## The first mission of map `place` on the test ground.
func open(place: int) -> void:
	Router.params["map"] = place
	Router.push("test_mission", {"lord": place, "mission": 0})
