class_name MapGenerator
extends RefCounted
## Makes the map of a place from its plan (MapPlan) and the rules of data/map_rules.json, in the
## format of the campaign's maps (MapBuilder), step by step on a MapDraft: the grid of rooms and
## each mission's route (RoomLayout), what stands in the rooms (RoomFill, with the rooms made by
## hand: SetPiece), the fights of each mission, its things to break and its time (WavePlan), the
## ground (GroundPaint). Each step draws from its own random numbers, started from the seed and
## the step's name, so that new rules for one step do not move what the others make. A map the
## game cannot play (MapCheck) is made again from the next seed, up to TRIES seeds.
##
## map_rules.json: curve: per band of depths in the campaign (MapPlan.depth: [first, last]),
## route_rooms ([fewest, most] rooms on a mission's route), crowding (the least and the most of a
## room on a route its obstacles take), soldiers and archers (WavePlan); breakables and time
## (WavePlan); biomes: per biome of the plan, its ground (GroundPaint), barrier, low_barrier,
## obstacles, land and loose things (RoomFill), breakables (WavePlan).

const RULES_PATH := "res://data/map_rules.json"
const FORMAT := 2
## Seeds tried for a place, from its own on.
const TRIES := 50
## Enemies alive at once in a room: a rule of the fight, the same in every room.
const MAX_ENEMIES := 3

static var _rules: Dictionary = {}

## Why the last seed tried gave no map the game can play (make).
var problems: Array[String] = []


## The map of the place from the first of TRIES seeds, its own on, that gives one the game can
## play; {} when none does (problems tells why).
func make(plan: MapPlan) -> Dictionary:
	for i in TRIES:
		var map := build(plan, plan.seed + i)
		problems = MapCheck.problems(map, plan.bosses, plan.ways_on)
		if problems.is_empty():
			return map
	return {}


## The map of the place from `map_seed`, whether the game can play it or not.
static func build(plan: MapPlan, map_seed: int) -> Dictionary:
	var layout := layout_of(plan, map_seed)
	var draft := MapDraft.new(layout)
	var biome: Dictionary = _rules_of()["biomes"][plan.biome]
	var crowding: Array = curve(plan.depth)["crowding"]
	RoomFill.new(draft, biome, stream(map_seed, "fill")).fill(
		plan, Vector2(crowding[0], crowding[1])
	)
	var fights := WavePlan.new(draft, plan, _rules_of(), stream(map_seed, "waves"))
	fights.make()
	GroundPaint.new(draft, biome, stream(map_seed, "ground")).paint()
	var map := {"format": FORMAT, "seed": map_seed, "w": draft.w, "h": draft.h}
	map["biome"] = plan.biome
	map["parts"] = Array(draft.parts)
	map["props"] = Array(draft.props)
	map["objects"] = Array(fights.objects)
	map["flags"] = Array(draft.blocked)
	map["scripts"] = Array(fights.scripts)
	var missions: Array = []
	var starts: Array = []
	for mission in plan.missions.size():
		missions.append(_mission_rooms(plan, layout, fights.waves[mission], mission))
		var start := layout.start(mission)
		starts.append([start.x, start.y])
	map["rooms"] = {"rooms_x": layout.rooms_x, "rooms_y": layout.rooms_y, "missions": missions}
	map["starts"] = starts
	map["time_limits"] = Array(fights.time_limits)
	return map


## The rooms and routes of the place's map from `map_seed`, as long as the curve says for its
## depth.
static func layout_of(plan: MapPlan, map_seed: int) -> RoomLayout:
	return RoomLayout.new(plan, route_rooms(plan.depth), stream(map_seed, "layout"))


## The fewest and the most rooms on the route of a mission `depth` steps into the campaign.
static func route_rooms(depth: int) -> Vector2i:
	var rooms: Array = curve(depth)["route_rooms"]
	return Vector2i(rooms[0], rooms[1])


## The band of the curve (map_rules.json) for a place `depth` steps into the campaign.
static func curve(depth: int) -> Dictionary:
	var bands: Array = _rules_of()["curve"]
	for band: Dictionary in bands:
		if depth <= int(band["depths"][1]):
			return band
	return bands[-1]


static func _rules_of() -> Dictionary:
	if _rules.is_empty():
		_rules = JSON.parse_string(FileAccess.get_file_as_string(RULES_PATH))
	return _rules


## Random numbers for one step of making the map: started from the seed and the step's name
## (the FNV-1a hash of "seed:step", our own so that no new Godot moves the maps).
static func stream(map_seed: int, step: String) -> GameRandom:
	const FNV_OFFSET := 0x811C9DC5
	const FNV_PRIME := 0x01000193
	var hash_of := FNV_OFFSET
	for byte in ("%d:%s" % [map_seed, step]).to_utf8_buffer():
		hash_of = ((hash_of ^ byte) * FNV_PRIME) & 0xFFFFFFFF
	return GameRandom.new(hash_of)


## The rooms of a mission (Rooms.cells): the exits of its route, its waves (WavePlan) and in the
## room of each stop of its plan who talks.
static func _mission_rooms(plan: MapPlan, layout: RoomLayout, waves: Array, mission: int) -> Array:
	var talks := {}
	for i in plan.missions[mission].size():
		talks[layout.routes[mission][layout.stops[mission][i]]] = plan.missions[mission][i]["talk"]
	var rooms: Array = []
	for room in layout.rooms_x * layout.rooms_y:
		(
			rooms
			. append(
				{
					"exits": layout.exits(mission, room),
					"max_enemies": MAX_ENEMIES,
					"waves": waves[room],
					"general": talks.get(room, 0),
				}
			)
		)
	return rooms
