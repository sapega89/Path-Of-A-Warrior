extends "res://tests/test_case.gd"

const Profile := preload("res://scripts/core/profile.gd")
const NewGame := preload("res://scripts/screens/new_game_screen.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")
const MapBuilder := preload("res://scripts/world/map_builder.gd")
const TEST_PATH := "user://test_new_game.json"


func test_head_and_difficulty_are_kept() -> void:
	var p := Profile.new()
	eq(p.difficulty, 1, "normal by default")
	p.head = 2
	p.difficulty = 0
	p.save(TEST_PATH)
	var q: RefCounted = Profile.load_or_new(TEST_PATH)
	eq(q.head, 2, "the face")
	eq(q.difficulty, 0, "hard")
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	q.apply_to(sim)
	eq(sim.difficulty, 0, "the mission is played hard")


func test_new_game_steps() -> void:
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var screen: Control = NewGame.new()
	root.add_child(screen)
	eq(screen.step, NewGame.Step.DIFFICULTY, "the difficulty first")
	screen.choose_difficulty(0)
	screen._confirmed()
	eq(screen.step, NewGame.Step.HERO, "then the face")
	screen.choose_head(3)
	eq(screen.step, NewGame.Step.NAME, "then the name")
	screen.name_edit.text = ""
	check(not screen.submit_name(), "a name is needed")
	screen.name_edit.text = "Ivan7!"
	screen._name_changed(screen.name_edit.text)
	eq(screen.name_edit.text, "Ivan", "only letters")
	check(screen.submit_name(), "taken")
	eq(screen.step, NewGame.Step.POINTS, "then the points")
	for i in 5:
		screen.spend(Profile.Stat.ATTACK)
	eq(screen.profile.stat_points, 0, "all five spent")
	screen.profile.save(TEST_PATH)  # (finish() also opens the story)
	var saved: RefCounted = Profile.load_or_new(TEST_PATH)
	eq(saved.hero_name, "Ivan", "the name")
	eq(saved.head, 3, "the face")
	eq(saved.difficulty, 0, "hard")
	eq(saved.base_attack, Profile.BASE_ATTACK + 5, "the points")
	screen.free()
	Router.params = old
