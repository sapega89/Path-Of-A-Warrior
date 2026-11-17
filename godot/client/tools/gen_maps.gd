extends Node
## Writes the maps the map generator makes (MapGenerator.make) into data/maps/N.json, the maps of
## the campaign, and prints a line a place (the seed it took and how many seeds it tried) and a
## line a mission (its rooms, soldiers, archers and time). Headless:
##   godot --headless --path godot/client res://tools/gen_maps.tscn -- [places] [seeds N]
## places: numbers and ranges (1 5 9-13), or `depths A B` (the places A to B steps into the
## campaign, MapPlan.depth); none: every place. With `seeds N` it writes nothing: it makes the
## map of each place from N seeds, its own on, and prints those the game could not play
## (MapCheck), a line `BAD <place> <seed>: <problem>` each.

var places: Array[int] = []
var seeds := 0


func _ready() -> void:
	_read_args(OS.get_cmdline_user_args())
	if places.is_empty():
		places.assign(range(1, MapBuilder.map_count() + 1))
	for place in places:
		if seeds > 0:
			_try_seeds(place)
		else:
			_write(place)
	get_tree().quit()


func _read_args(args: PackedStringArray) -> void:
	var i := 0
	while i < args.size():
		if args[i] == "seeds":
			seeds = int(args[i + 1])
			i += 2
		elif args[i] == "depths":
			for place in range(1, MapBuilder.map_count() + 1):
				var depth := MapPlan.of(place).depth
				if depth >= int(args[i + 1]) and depth <= int(args[i + 2]):
					places.append(place)
			i += 3
		else:
			var ends := args[i].split("-")
			places.append_array(range(int(ends[0]), int(ends[-1]) + 1))
			i += 1


func _write(place: int) -> void:
	var plan := MapPlan.of(place)
	var generator := MapGenerator.new()
	var map := generator.make(plan)
	if map.is_empty():
		print("BAD %d: no map from %d seeds: %s" % [place, MapGenerator.TRIES, generator.problems])
		return
	var f := FileAccess.open(MapBuilder.map_path(place), FileAccess.WRITE)
	f.store_string(JSON.stringify(map, "", false))
	f.close()
	print(
		(
			"place %d (%s, depth %d): seed %d, try %d"
			% [place, plan.biome, plan.depth, map.seed, int(map.seed) - plan.seed + 1]
		)
	)
	for m in plan.missions.size():
		var fights := WavePlan.fights_of(map, m)
		print(
			(
				"  mission %d: %d rooms, %d soldiers, %d archers, %d s"
				% [m + 1, fights.rooms, fights.soldiers, fights.archers, fights.time]
			)
		)


func _try_seeds(place: int) -> void:
	var plan := MapPlan.of(place)
	var bad := 0
	for i in seeds:
		var map := MapGenerator.build(plan, plan.seed + i)
		var problems := MapCheck.problems(map, plan.bosses, plan.ways_on)
		if not problems.is_empty():
			bad += 1
			print("BAD %d %d: %s" % [place, plan.seed + i, problems[0]])
	print("place %d: %d of %d seeds the game can play" % [place, seeds - bad, seeds])
