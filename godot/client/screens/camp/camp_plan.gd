class_name CampPlan
extends RefCounted
## The ground plan of the camp between missions, «Плавні» (no nodes; CampFort builds it): a
## ring of palisade RADIUS metres round with a gate for each way on (a mission, see
## camp_screen.gd) on a side of the world (GATES: north, east, west, south, then north-east and
## north-west), the yard with its fires in the middle, in the start camp the town hall
## north-west of it (off the north road, so it never hides the hero there), east of the yard the
## smithy. A closed way's gate is barred. What stands in the camp is added as a round
## (add_solid), so blocked() and reachable() know the ground without physics. The spots are
## where the hero uses something (SPOTS): a way's road inside its gate, the smithy, the town
## hall's door (from farther off than the smithy's).
## Coordinates: metres on the XZ plane, the middle of the ring at (0, 0); +Z is south (towards
## the camera), +X east.

## The palisade ring's radius; the water channels run round it at MOAT, with a dry causeway
## CAUSEWAY degrees to each side of a gate.
const RADIUS := 16.0
const MOAT := 19.6
const CAUSEWAY := 11.0
const PIECE := 2.0  # metres of one piece of palisade
## Where the gates go for 1..6 ways: degrees round the ring from the south (+Z) towards the
## east (+X).
const SOUTH := 0.0
const EAST := 90.0
const NORTH := 180.0
const WEST := 270.0
const GATES := [
	[],
	[NORTH],
	[NORTH, EAST],
	[NORTH, EAST, WEST],
	[NORTH, EAST, WEST, SOUTH],
	[NORTH, EAST, WEST, SOUTH, 135.0],
	[NORTH, EAST, WEST, SOUTH, 135.0, 225.0],
]
## Pieces of palisade a gate takes: the main gate in the south is two wide, the others one.
const MAIN_GATE_PIECES := 2
const SIDE_GATE_PIECES := 1
const OUT := 1.0  # a gate counts as walked out of this far past the ring
const ROAD_IN := 2.2  # a way's spot: its road this far inside the gate
const ROAD_OUT := 6.0  # how far past the ring one can walk out of an open gate
const GATE_ROOM := 6.0  # degrees past a gate's side that still count as walking out of it
## Where things stand.
const HALL_AT := Vector3(-4.5, 0.0, -7.0)  # off the north road, so it hides nothing there
const YARD := Vector3(0.0, 0.0, 1.0)  # the middle of the trodden yard before the hall
const FIRES := [Vector3(-3.6, 0.0, 2.2), Vector3(3.8, 0.0, 0.4)]
const SMITH_AT := Vector3(9.0, 0.0, 2.6)  # the anvil
const START := Vector3(0.0, 0.0, 5.2)
## Where the hero stands to use each, and how near he must come (metres): the town hall's
## door from farther off, so he need not walk right up to it.
const SPOTS := {
	"hall": [HALL_AT + Vector3(0.0, 0.0, 3.9), 3.0],
	"smith": [SMITH_AT + Vector3(-0.2, 0.0, 1.6), 2.0],
}
const WAY_RANGE := 2.0
const BODY := 0.3  # the hero's radius
const GRID := 0.5  # metres of a cell of reachable()
## The places the endings take the hero to (Profile.NEXT_PLACE) and the start: main camps.
const MAIN := [0, 8, 11, 15, 17, 19, 20, 22, 30, 33, 35, 38, 39, 44]

## One per way: {place, mission, open, angle, out: the way on (a unit vector), gate: the
## middle of the gate, inside: its road just within it}.
var exits: Array[Dictionary] = []
var main := false
var has_hall := true  # the town hall stands only in the start camp (CampScreen)
## What stands: [centre (Vector2 on XZ), radius]; the palisade ring is not in it (blocked()).
var solids: Array = []
var step := 0.0  # degrees of one piece of palisade


## ways: [[place id, open], ...] or [[place id, open, mission], ...], at most six. with_hall:
## the town hall stands in the camp.
func _init(ways: Array = [], is_main_camp := false, with_hall := true) -> void:
	main = is_main_camp
	has_hall = with_hall
	var pieces := floori(360.0 / rad_to_deg(2.0 * asin(PIECE / 2.0 / RADIUS)))
	step = 360.0 / pieces
	var gates: Array = GATES[clampi(ways.size(), 0, GATES.size() - 1)]
	for i in mini(ways.size(), gates.size()):
		var angle: float = gates[i]
		var way: Array = ways[i]
		(
			exits
			. append(
				{
					"place": int(way[0]),
					"open": bool(way[1]),
					"mission": int(way[2]) if way.size() > 2 else -1,
					"angle": angle,
					"out": on_ring(angle, 1.0),
					"gate": on_ring(angle, RADIUS),
					"inside": on_ring(angle, RADIUS - ROAD_IN),
				}
			)
		)


static func is_main(place: int) -> bool:
	return place in MAIN


## A point round the middle of the camp: `deg` degrees from the south (+Z) towards the east.
static func on_ring(deg: float, radius: float) -> Vector3:
	var a := deg_to_rad(deg)
	return Vector3(sin(a) * radius, 0.0, cos(a) * radius)


## The angle of a point round the middle, as on_ring() counts it (0..360).
static func angle_of(p: Vector3) -> float:
	return fposmod(rad_to_deg(atan2(p.x, p.z)), 360.0)


## Degrees between two angles round the ring (0..180).
static func apart(a: float, b: float) -> float:
	return absf(fposmod(a - b + 180.0, 360.0) - 180.0)


## Pieces of palisade the gate at `angle` takes.
static func gate_pieces(angle: float) -> int:
	return MAIN_GATE_PIECES if is_equal_approx(angle, SOUTH) else SIDE_GATE_PIECES


## How many degrees a gate takes to each side of its middle.
func gate_half_width(angle: float) -> float:
	return step * gate_pieces(angle) / 2.0


## The open way whose gate the position has walked out of, as its index, or -1.
func exit_crossed(pos: Vector3) -> int:
	if Vector2(pos.x, pos.z).length() < RADIUS + OUT:
		return -1
	var a := angle_of(pos)
	for i in exits.size():
		var e := exits[i]
		if e.open and apart(a, e.angle) <= gate_half_width(e.angle) + GATE_ROOM:
			return i
	return -1


## Something one cannot walk through, as a round on the ground.
func add_solid(centre: Vector2, radius: float) -> void:
	solids.append([centre, radius])


## Whether a body of `radius` cannot stand at p: in something standing, in the palisade or a
## barred gate, or outside the ring but not in an open gate's way.
func blocked(p: Vector3, radius := BODY) -> bool:
	var q := Vector2(p.x, p.z)
	for s in solids:
		if q.distance_to(s[0]) < float(s[1]) + radius:
			return true
	var r := q.length()
	if r < RADIUS - 0.5 - radius:
		return false
	var a := angle_of(p)
	for e in exits:
		var room := gate_half_width(e.angle) - rad_to_deg(radius / RADIUS) - 0.5
		if e.open and apart(a, e.angle) < room:
			return r > RADIUS + ROAD_OUT
	return true


## The cells of GRID metres one can walk to from `from`: a set of Vector2i.
func reachable(from: Vector3) -> Dictionary:
	var first := cell_of(from)
	var seen := {first: true}
	var todo: Array[Vector2i] = [first]
	while not todo.is_empty():
		var c: Vector2i = todo.pop_back()
		for d in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
			var n: Vector2i = c + d
			var at := Vector3(n.x * GRID, 0.0, n.y * GRID)
			if seen.has(n) or Vector2(n).length() * GRID > RADIUS + OUT + 2.0 or blocked(at):
				continue
			seen[n] = true
			todo.append(n)
	return seen


## The cell of reachable() a position is in.
static func cell_of(p: Vector3) -> Vector2i:
	return Vector2i(roundi(p.x / GRID), roundi(p.z / GRID))


## Where the hero uses things: a way's road inside its gate (with its place, mission and
## whether it is open), then the smithy and the town hall (if it stands); each {kind, at, range}.
func spots() -> Array[Dictionary]:
	var out: Array[Dictionary] = []
	for e in exits:
		(
			out
			. append(
				{
					"kind": "way",
					"place": e.place,
					"mission": e.mission,
					"open": e.open,
					"at": e.inside,
					"range": WAY_RANGE,
				}
			)
		)
	for kind in ["smith", "hall"] if has_hall else ["smith"]:
		out.append({"kind": kind, "at": SPOTS[kind][0], "range": SPOTS[kind][1]})
	return out


## The nearest of `spots` whose range reaches `pos`, or empty.
static func spot_near(spots_list: Array[Dictionary], pos: Vector3) -> Dictionary:
	var best := {}
	var best_d := INF
	for s in spots_list:
		var d := Vector2(pos.x - s.at.x, pos.z - s.at.z).length()
		if d <= float(s.range) and d < best_d:
			best = s
			best_d = d
	return best
