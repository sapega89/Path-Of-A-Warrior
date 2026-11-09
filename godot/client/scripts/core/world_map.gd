class_name WorldMap
extends RefCounted
## The campaign's world: 45 places, each one map with its missions, and the ways between them.
## A place is what campaign.json calls a lord: place N is map N, its missions are
## Campaign.lord_missions(N). From place p the hero can go to Campaign.chapter_lords(p)
## (place 0 is the start, before the first mission); winning a mission at place L puts him at L.
## The ways never lead back, so the places are laid out in columns: a place's column is the
## longest way to it from the start, and in a column the places sit near the places they
## come from.

enum State { HERE, NEXT, CLOSED, AWAY }

var campaign: RefCounted
## Place id -> Vector2(column, row); rows are centred on 0 and may be halves.
var cells := {}
var columns := 0
var rows := 0  # the most places in one column


func _init(c: RefCounted = null) -> void:
	campaign = c if c != null else Campaign.new()
	_layout()


func place_count() -> int:
	return campaign.lords.size()


## The places the hero can go to from `place`.
func next_places(place: int) -> Array:
	var out: Array = []
	for id in campaign.chapter_lords(place):
		out.append(int(id))
	return out


## Every way between two places: [from, to], from the first place on (the start is not a place).
func ways() -> Array:
	var out: Array = []
	for from in range(1, place_count() + 1):
		for to in next_places(from):
			out.append([from, to])
	return out


## The places a way leads from into `place`.
func comes_from(place: int) -> Array:
	var out: Array = []
	for w in ways():
		if w[1] == place:
			out.append(w[0])
	return out


## How the place looks to a hero at `here`: his own place, one he can go to now (and fight
## for), one he could go to but is closed, or one further away.
func state(place: int, here: int, profile: RefCounted) -> int:
	if place == here:
		return State.HERE
	if place in next_places(here):
		return State.NEXT if profile.is_lord_open(place) else State.CLOSED
	return State.AWAY


## Missions won at the place and how many it has.
func won(place: int, profile: RefCounted) -> Vector2i:
	var n: int = campaign.lord_missions(place).size()
	var w := 0
	for i in n:
		if profile.is_done(place, i):
			w += 1
	return Vector2i(w, n)


func _layout() -> void:
	var n := place_count()
	if n == 0:
		return
	# The longest way from the start: the places in an order where a way never goes back.
	var depth := {}
	var ins := {}
	for id in range(1, n + 1):
		ins[id] = 0
	for w in ways():
		ins[w[1]] += 1
	var ready: Array = next_places(0)
	for id in ready:
		depth[id] = 0
	var order: Array = []
	while not ready.is_empty():
		ready.sort()
		var id: int = ready.pop_front()
		order.append(id)
		for to in next_places(id):
			depth[to] = maxi(int(depth.get(to, 0)), int(depth[id]) + 1)
			ins[to] -= 1
			if ins[to] == 0:
				ready.append(to)
	for id in range(1, n + 1):
		if not depth.has(id):  # not reached from the start: after the last column
			order.append(id)
			depth[id] = 0
	var by_column := {}
	for id in order:
		var c: int = depth[id]
		if not by_column.has(c):
			by_column[c] = []
		by_column[c].append(id)
	columns = 0
	rows = 0
	for c in by_column:
		columns = maxi(columns, c + 1)
		rows = maxi(rows, by_column[c].size())
	# In a column, the places by the mean row of the places they come from.
	for c in range(columns):
		var ids: Array = by_column.get(c, [])
		var key := {}
		for id in ids:
			var from := comes_from(id).filter(func(f): return cells.has(f))
			var sum := 0.0
			for f in from:
				sum += cells[f].y
			key[id] = sum / from.size() if not from.is_empty() else 0.0
		ids.sort_custom(func(a, b): return key[a] < key[b] or (key[a] == key[b] and a < b))
		for i in ids.size():
			cells[ids[i]] = Vector2(c, i - (ids.size() - 1) / 2.0)
