extends "res://tests/test_case.gd"
## The game's keys on a mission's map come as input events: a press is taken once and kept
## until the next tick of the game, a held key does not press again, and while the game is
## stopped the keys are not taken.


func _action(action: String, pressed: bool) -> void:
	var ev := InputEventAction.new()
	ev.action = action
	ev.pressed = pressed
	Input.parse_input_event(ev)
	Input.flush_buffered_events()


func test_a_press_is_taken_once() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: MissionScreen = Router.make(Router.SCREENS["mission"])
	root.add_child(screen)
	_action("attack", true)
	check(screen._fire, "a press of attack: an attack on the next tick")
	screen._process(screen.tick)
	check(not screen._fire, "the tick took it")
	screen._process(screen.tick)
	check(not screen._fire, "held: no second attack")
	_action("attack", false)
	_action("skill_2", true)
	eq(screen._hotkey, 1, "a skill key")
	_action("skill_2", false)
	_action("potion_1", true)
	eq(screen._potion, 0, "a potion key")
	_action("potion_1", false)
	screen.set_process(false)
	_action("belt_3", true)
	eq(screen._belt, -1, "the game stopped: the keys are not taken")
	_action("belt_3", false)
	screen.free()
	Router.params = old
