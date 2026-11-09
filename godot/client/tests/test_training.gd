extends "res://tests/test_case.gd"
## The training before the first mission (scripts/screens/training_screen.gd and its steps,
## scripts/ui/tutorial.gd): the steps one after another, a step that has nothing to teach left
## out, no losing, the hints for the device in use, Skip Training on the pause menu, and the way
## from New Game's opening story through the training to the game menu.

const Training := preload("res://scripts/screens/training_screen.gd")
const Tutorial := preload("res://scripts/ui/tutorial.gd")
const Profile := preload("res://scripts/core/profile.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")
const NewGame := preload("res://scripts/screens/new_game_screen.gd")
const PATH := "user://test_training.json"


func _training(difficulty := 1) -> Control:
	var p: RefCounted = Profile.new()
	p.difficulty = difficulty
	p.save(PATH)
	Router.params = {"profile_path": PATH}
	var screen: Control = Training.new()
	root.add_child(screen)
	return screen


func test_the_steps() -> void:
	var old: Dictionary = Router.params
	var was: String = InputSetup.device
	InputSetup.device = "keys"
	var screen := _training()
	var sim: RefCounted = screen.sim
	var t: Tutorial = screen.tutorial
	eq(sim.time_limit, 0, "no time limit")
	check(sim.enemies.is_empty() and int(sim.waves[0]) == 0, "nobody in the room")
	eq(t.step, Tutorial.Step.MOVE, "first: walk")
	eq(t.label.text, "Walk: WASD / arrows", "its hint")
	t.check()
	eq(t.step, Tutorial.Step.MOVE, "not yet")
	sim.hero.pos += Vector2i(Tutorial.WALK_PX, 0)
	t.check()
	eq(t.step, Tutorial.Step.ATTACK, "walked: a soldier")
	eq([int(sim.waves[0]), int(sim.waves[1]), sim.max_enemies()], [MapSim.KIND_SWORDS, 1, 1], "one comes in")
	eq(t.label.text, "A soldier! Walk up to him and strike: J", "strike")
	sim.waves[0] = 0  # he came in and fell
	t.check()
	eq(t.step, Tutorial.Step.SKILL, "nothing dropped: no loot step")
	eq(sim.hero.mp, sim.hero.max_mp, "MP full")
	eq(int(sim.waves[1]), 2, "two more")
	sim.waves[0] = 0
	t.check()
	eq(t.step, Tutorial.Step.SKILL, "beaten without the skill: still the skill")
	eq(int(sim.waves[1]), 1, "one more for it")
	sim.hero.mp -= 5
	t.check()
	sim.waves[0] = 0
	t.check()
	eq(t.step, Tutorial.Step.POTION, "the skill used: the potion")
	eq(sim.quick_slots[0], [Tutorial.POTION, 1], "a red potion on the belt")
	eq(sim.hero.hp, sim.hero.max_hp / 3, "HP at a third")
	eq(t.label.text, "The red ball is your health. Drink a potion from the belt: Z", "drink")
	sim.quick_slots[0] = [0, 0]
	t.check()
	eq(t.step, Tutorial.Step.AUTO, "drunk: the auto-hunt")
	eq(t.label.text, "Three more. Auto-hunt: Tab. The hero fights by himself; any key takes over", "AUTO")
	screen.toggle_auto()
	t.check()
	sim.waves[0] = 0
	t.check()
	eq(t.step, Tutorial.Step.EXIT, "fought with AUTO: out of the room")
	check(not screen.autopilot.on, "the player walks out himself")
	check(not sim.hold_room and sim.no_enemies, "the room lets go, the next ones are empty")
	eq(sim.room_phase, 3, "the room is cleared")
	sim.cell += 1
	t.check()
	eq(t.step, Tutorial.Step.PAUSE, "in the next room: pause")
	eq(t.label.text, "Pause: Esc. When a room is clear, you can save there", "pause")
	screen.pause()
	t._process(0.1)
	eq(t.step, Tutorial.Step.DONE, "paused: done")
	eq(t.label.text, "Training complete! Enter: to the game", "the end")
	screen.free()
	InputSetup.device = was
	Router.params = old


func test_hard_has_no_auto_step_and_nobody_loses() -> void:
	var old: Dictionary = Router.params
	var screen := _training(0)
	var t: Tutorial = screen.tutorial
	t.begin(Tutorial.Step.AUTO)
	eq(t.step, Tutorial.Step.EXIT, "hard: no AUTO, out of the room")
	var hero = screen.sim.hero
	hero.hp = 1
	t._process(0.1)
	eq(hero.hp, hero.max_hp / 2, "below a quarter: healed to half")
	screen.free()
	Router.params = old


func test_the_hint_follows_the_device() -> void:
	var old: Dictionary = Router.params
	var was: Array = [InputSetup.device, InputSetup.pad_brand]
	InputSetup.device = "keys"
	var screen := _training()
	var t: Tutorial = screen.tutorial
	InputSetup.device = "pad"
	InputSetup.pad_brand = "ps"
	InputSetup.device_changed.emit("pad")
	eq(t.label.text, "Walk: Left stick", "a pad: the left stick")
	t.begin(Tutorial.Step.ATTACK)
	eq(t.label.text, "A soldier! Walk up to him and strike: Cross", "PlayStation: Cross")
	InputSetup.device = "touch"
	InputSetup.device_changed.emit("touch")
	eq(t.label.text, tr("training.attack_touch"), "a phone: its own words")
	screen.free()
	InputSetup.device = was[0]
	InputSetup.pad_brand = was[1]
	Router.params = old


## The soldiers a step sends come in through the exits, and the last one's death leaves the
## room as it was (the training clears it when it says).
func test_the_room_waits_for_the_training() -> void:
	var old: Dictionary = Router.params
	var screen := _training()
	screen.set_process(false)
	var sim: RefCounted = screen.sim
	sim.send_soldiers(1)
	for i in 80:
		if not sim.enemies.is_empty():
			break
		sim.tick(-1)
	eq(sim.enemies.size(), 1, "a soldier came in")
	var e = sim.enemies[0]
	e.hp = 0
	e.action = 3
	e.frame = 0
	for i in 40:
		sim.tick(-1)
	eq(sim.enemies_alive, 0, "he fell")
	eq(sim.room_phase, 0, "the room is not cleared by itself")
	check(not sim.exits_open(), "the exits stay shut")
	sim.clear_room()
	for i in 40:
		sim.tick(-1)
	check(sim.exits_open(), "cleared when the training says: the exits open")
	screen.free()
	Router.params = old


## The training says "walk out by the blinking arrow": the arrow down is above the HUD, not
## under it.
func test_the_arrow_down_shows_above_the_hud() -> void:
	var old: Dictionary = Router.params
	var screen := _training()
	screen._place_arrows()
	var view: Vector2 = screen.get_viewport_rect().size
	var a: TextureRect = screen.arrows[0]
	check(a.position.y + a.size.y <= screen.hud.top_of(view), "above the HUD: %s + %s <= %s" % [
		a.position.y, a.size.y, screen.hud.top_of(view)])
	screen.free()
	Router.params = old


func test_skip_training_on_the_pause_menu() -> void:
	var old: Dictionary = Router.params
	var screen := _training()
	screen.pause()
	var menu: Control = screen.pause_menu
	var names := []
	for b in menu.buttons:
		names.append(str(b.name))
	check(not names.has("Save"), "nothing to save")
	var exit: Button = menu.buttons[names.find("Exit")]
	eq(exit.text, "pause.skip_training", "Exit is Skip Training")
	exit.pressed.emit()
	eq(menu.ask.dialog_text, tr("pause.ask_skip_training"), "asked first")
	check(menu.ask.cancel.has_focus(), "No first")
	check(menu.leave.is_valid(), "Yes leaves the training")
	screen.free()
	Router.params = old


## New Game: the opening story, then the training, then the game menu; Settings: the training
## and back to them.
func test_the_way_through_the_training() -> void:
	var old: Dictionary = Router.params
	var host := Control.new()
	root.add_child(host)
	Router.attach(host)
	Router.go("settings")
	Router.push("new_game", {"profile_path": PATH})
	var ng: Control = Router.current
	ng.finish()
	eq(Router.current_name(), "story", "the opening story")
	eq([Router.params.get("then"), Router.params.get("then_params")],
		["training", {"then": "game_menu", "profile_path": PATH}], "then the training, then the menu")
	Router.current._end()
	eq(Router.current_name(), "training", "the training")
	eq(Router.params, {"then": "game_menu", "profile_path": PATH}, "with where to go after it")
	Router.current.tutorial.finish()
	eq(Router.current_name(), "game_menu", "after it: the game menu")
	Router.go("settings")
	var training: Button = Router.current.find_child("Training", true, false)
	check(training != null, "Settings: Training")
	training.pressed.emit()
	eq(Router.current_name(), "training", "the training again")
	Router.current.leave()
	eq(Router.current_name(), "settings", "and back to the Settings")
	Router.attach(null)
	host.free()
	Router.params = old
