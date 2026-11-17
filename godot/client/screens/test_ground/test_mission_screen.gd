class_name TestMissionScreen
extends MissionScreen
## A mission on the test ground (TestGroundScreen): the mission of a map of the campaign as it
## plays, with its enemies, rooms and talks, but the hero cannot die (MapSim.immortal), AUTO is
## there on hard too and nothing is saved: no exp, gold or loot taken, no place won. PageUp or
## [ goes to the first mission of the previous map, PageDown or ] of the next (after the last
## map the first); a mission won goes on to the next one of its map, after its last to the
## next map. The line at the top says which map and mission, and the keys.
## Params: {lord (the map), mission}, as a mission's.

@onready var where: Label = %Where


func _ready() -> void:
	super()
	sim.immortal = true
	var missions := Campaign.new().lord_missions(lord_id).size()
	where.text = (
		tr("test_ground.where")
		% [lord_id, MapBuilder.map_count(), lord_name, mission + 1, missions]
	)


## The map `step` maps on from `place`, round the campaign (after the last, the first).
static func map_after(place: int, step: int) -> int:
	return wrapi(place + step, 1, MapBuilder.map_count() + 1)


## The mission after mission `mission_no` of map `place`: the next one of the map, or the first
## of the next map. Vector2i(map, mission).
static func mission_after(place: int, mission_no: int) -> Vector2i:
	if mission_no + 1 < Campaign.new().lord_missions(place).size():
		return Vector2i(place, mission_no + 1)
	return Vector2i(map_after(place, 1), 0)


## Shows mission `mission_no` of map `place` in place of this one.
func go_to(place: int, mission_no: int) -> void:
	set_process(false)
	Router.replace("test_mission", {"lord": place, "mission": mission_no})


## A mission won goes on to the next one; nothing is taken or saved.
func _finish() -> void:
	var next := mission_after(lord_id, mission)
	go_to(next.x, next.y)


## AUTO on any difficulty.
func auto_allowed() -> bool:
	return sim != null


func _screen_input(event: InputEvent) -> void:
	if pause_menu == null and is_processing():
		for step: int in [-1, 1]:
			if event.is_action_pressed("map_prev" if step < 0 else "map_next"):
				get_viewport().set_input_as_handled()
				go_to(map_after(lord_id, step), 0)
				return
	super(event)
