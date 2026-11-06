extends "res://tests/test_case.gd"
## Save on the map (pause menu): once the room is cleared, the mission is saved with what was
## picked up, and Continue comes back to that room.

const MissionScreen := preload("res://scripts/screens/mission_screen.gd")
const MainMenu := preload("res://scripts/screens/main_menu.gd")
const Profile := preload("res://scripts/core/profile.gd")


func test_save_on_the_map_and_continue() -> void:
	var kept := FileAccess.get_file_as_string(Profile.PATH)  # the hero of this machine, put back after
	var p := Profile.new()
	p.gold = 100
	p.save()
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = MissionScreen.new()
	root.add_child(screen)
	var sim: RefCounted = screen.sim
	sim.waves = [201, 2]
	check(not screen.save_on_map(), "not while enemies are to come")
	sim.waves = [0]
	for e in sim.enemies:
		e.hp = 0
	sim.gold = 50
	sim.items.append(131)
	sim.hero.hp = 10
	sim.kills = 7
	check(screen.save_on_map(), "saved once the room is clear")
	eq(sim.gold, 0, "the gold picked up went to the hero")
	var saved: RefCounted = Profile.load_or_new()
	eq(saved.gold, 150, "with the gold picked up")
	eq(int(saved.backpack[0].id), 131, "and the helmet")
	eq(int(saved.on_map.get("lord", 0)), 1, "the mission on its map")
	eq(int(saved.on_map.get("hp", 0)), 10, "his HP")
	var room: int = sim.cell
	screen.free()

	Router.params = {"lord": 1, "mission": 0, "seed": 2, "resume": true}
	var again: Control = MissionScreen.new()
	root.add_child(again)
	eq(again.sim.hero.hp, 10, "Continue: the HP of the save")
	eq(again.sim.kills, 7, "and its kills")
	eq(again.sim.cell, room, "in the room saved")
	again.free()

	saved.save()
	check(Profile.load_or_new().on_map.is_empty(), "any other save forgets it")
	Router.params = old
	if kept.is_empty():
		DirAccess.remove_absolute(ProjectSettings.globalize_path(Profile.PATH))
	else:
		var f := FileAccess.open(Profile.PATH, FileAccess.WRITE)
		f.store_string(kept)
