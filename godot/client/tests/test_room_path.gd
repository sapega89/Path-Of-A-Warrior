extends "res://tests/test_case.gd"
## The autopilot's ways through a room (scripts/sim/room_path.gd, RoomPath): the steps round
## the walls, the ways out of a side, and a step between two walls from the side of a cell.


## The three rooms with walls on some cells of the first room.
func _sim(walls: Array[Vector2i], start: Vector2i) -> MapSim:
	var map := own_map("three_rooms")
	for c in walls:
		map.flags[c.y * int(map.w) + c.x] = 1
	return MapSim.new(map, 0, start)


func test_the_steps_round_a_wall() -> void:
	var sim := _sim([Vector2i(4, 3), Vector2i(5, 3), Vector2i(6, 3)], Vector2i(5, 5))
	var steps := RoomPath.steps_from(sim, [Vector2i(5, 2)])
	eq(int(steps[Vector2i(5, 4)]), 6, "under the wall: round one of its ends")
	check(not steps.has(Vector2i(5, 3)), "no steps on a wall")
	check(not steps.has(Vector2i(5, 8)), "nor in the next room")
	eq(RoomPath.steps_to(steps, Vector2i(5, 3)), 1, "to a wall: to the cell next to it")
	eq(RoomPath.cell_of(sim, sim.hero.pos), Vector2i(5, 5), "the hero's cell")


func test_the_ways_out_on_a_side() -> void:
	var sim := _sim([], Vector2i(4, 4))
	var down := RoomPath.ways_out(sim, 0)
	eq(down.size(), 6, "the bottom row but its thing to break: %s" % [down])
	check(not Vector2i(7, 7) in down, "not the thing to break")


func test_up_between_two_walls_from_the_left_of_its_cell() -> void:
	# A gap at (4, 3) between two walls; the hero under it, near the left side of his cell: the
	# game's slide along the wall would stop him 8 px into the cell, still under the wall on the
	# left, so he steps right first, then up through the gap.
	var sim := _sim([Vector2i(3, 3), Vector2i(5, 3)], Vector2i(4, 4))
	sim.continue_in_clear_room()
	sim.hero.pos.x = 4 * RoomPath.CELL + 5
	eq(RoomPath.step_to(sim, Vector2i(4, 4), 4), 6, "right first")
	var steps := RoomPath.steps_from(sim, [Vector2i(4, 2)])
	for t in 20:
		var d := RoomPath.next_step(sim, steps, Vector2i(0, -1))
		var held := -1 if d < 0 else RoomPath.step_to(sim, RoomPath.cell_of(sim, sim.hero.pos), d)
		sim.tick(held, -1, sim.banner != 0, -1, -1, -1)
	eq(RoomPath.cell_of(sim, sim.hero.pos), Vector2i(4, 2), "through the gap")
