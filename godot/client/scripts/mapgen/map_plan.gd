class_name MapPlan
extends RefCounted
## The plan of a place's map: what the map generator keeps of the campaign. From
## data/map_plans.json: the place's biome, its seed and, for each mission, its generals in the
## order the hero meets them; from campaign.json: how deep in the campaign the place is, the
## general whose fall wins each mission and how many places the campaign goes on to from here.

const PATH := "res://data/map_plans.json"

static var _data: Dictionary = {}

var place := 0
var biome := ""
## Where the map generator's random numbers start (MapGenerator).
var seed := 0
## How deep in the campaign the place is: the fewest places won on the way to it from the
## start, itself too (the places the hero can go to first are 1).
var depth := 0
## Per mission, the rooms with generals or a talk as the hero meets them, the room of the
## mission's own general last (stops_of): {generals: [[kind, level bonus], ...], talk: the one
## who talks when the room is cleared, 0 none}.
var missions: Array[Array] = []
## Per mission, the general whose fall wins it (campaign.json boss_type).
var bosses: Array[int] = []
## The places the campaign goes on to from here: the ways on shown after a mission won.
var ways_on := 0


static func of(place_id: int) -> MapPlan:
	if _data.is_empty():
		_data = JSON.parse_string(FileAccess.get_file_as_string(PATH))
	var plan := MapPlan.new()
	plan.place = place_id
	var data: Dictionary = _data.get(str(place_id), {})
	plan.biome = str(data.get("biome", ""))
	plan.seed = int(data.get("seed", 0))
	for stops: Array in data.get("missions", []):
		var mission: Array[Dictionary] = []
		for stop: Dictionary in stops:
			mission.append(_stop(stop.get("generals", []), int(stop.get("talk", 0))))
		plan.missions.append(mission)
	var campaign := Campaign.new()
	for info: Dictionary in campaign.lord_missions(place_id):
		plan.bosses.append(int(info.get("boss_type", 0)))
	var world := WorldMap.new(campaign)
	plan.ways_on = world.next_places(place_id).size()
	plan.depth = _depth(world, place_id)
	return plan


## The rooms with generals or a talk of mission `mission` of a map, in the order the hero meets
## them: rooms by how many rooms from the start room they are along the rooms' exits, then by
## number; the room of `boss` (the mission's own general) last, and none past it.
static func stops_of(map: Dictionary, mission: int, boss: int) -> Array[Dictionary]:
	var rooms := Rooms.new(map, mission)
	var start := MapBuilder.mission_start(map, mission)
	var first := rooms.room_at(Vector3(start.x + 0.5, 0.0, start.y + 0.5))
	var steps := {first: 0}
	var todo: Array[int] = [first]
	while not todo.is_empty():
		var room: int = todo.pop_front()
		if _has_general(rooms, room, boss):
			continue
		for exit_no in range(Rooms.EXIT_DOWN, Rooms.EXIT_RIGHT + 1):
			var next := rooms.beside(room, exit_no)
			if rooms.has_exit(room, exit_no) and next >= 0 and not steps.has(next):
				steps[next] = int(steps[room]) + 1
				todo.append(next)
	var met: Array = steps.keys()
	met.sort_custom(
		func(a: int, b: int) -> bool: return steps[a] < steps[b] or (steps[a] == steps[b] and a < b)
	)
	var out: Array[Dictionary] = []
	var last: Dictionary = {}
	for room: int in met:
		var generals: Array = rooms.waves(room).filter(
			func(wave: Array) -> bool: return wave[0] > 0 and wave[0] < 200
		)
		var talk := int(rooms.cells[room].get("general", 0)) if room < rooms.cells.size() else 0
		if generals.is_empty() and talk == 0:
			continue
		if _has_general(rooms, room, boss):
			last = _stop(generals, talk)
		else:
			out.append(_stop(generals, talk))
	if not last.is_empty():
		out.append(last)
	return out


## The fewest steps from the start (place 0) to the place along the ways of the campaign.
static func _depth(world: WorldMap, place_id: int) -> int:
	var steps := {0: 0}
	var todo: Array[int] = [0]
	while not todo.is_empty():
		var at: int = todo.pop_front()
		for next: int in world.next_places(at):
			if not steps.has(next):
				steps[next] = int(steps[at]) + 1
				todo.append(next)
	return int(steps.get(place_id, 0))


static func _has_general(rooms: Rooms, room: int, general: int) -> bool:
	return rooms.waves(room).any(func(wave: Array) -> bool: return wave[0] == general)


static func _stop(generals: Array, talk: int) -> Dictionary:
	var pairs: Array = generals.map(func(g: Array) -> Array: return [int(g[0]), int(g[1])])
	return {"generals": pairs, "talk": talk}
