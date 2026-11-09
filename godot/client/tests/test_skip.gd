extends "res://tests/test_case.gd"
## SKIP, as pyport's left soft key: Q, F1 or the pad's Back, or a click on SKIP. It skips the
## talk on the map, the briefing and the story.

const MissionScreen := preload("res://scripts/screens/mission_screen.gd")
const Story := preload("res://scripts/screens/story_screen.gd")
const Briefing := preload("res://scripts/screens/briefing_screen.gd")


func _click(at: Vector2, device := 0) -> InputEventMouseButton:
	var ev := InputEventMouseButton.new()
	ev.button_index = MOUSE_BUTTON_LEFT
	ev.pressed = true
	ev.position = at
	ev.device = device
	return ev


func _skip_key() -> InputEventAction:
	var ev := InputEventAction.new()
	ev.action = "skip"
	ev.pressed = true
	return ev


## Hard has no auto-hunt: no AUTO corner, and Tab / F / the pad's Back do nothing.
func test_no_auto_on_hard() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = MissionScreen.new()
	root.add_child(screen)
	var view: Vector2 = screen.hud.get_viewport_rect().size
	var corner := Vector2(4, view.y - 4)
	screen.sim.difficulty = 1
	check(screen.auto_allowed(), "normal: AUTO")
	screen.toggle_auto()
	check(screen.autopilot.on, "normal: it turns on")
	screen.toggle_auto()
	screen.sim.difficulty = 0
	screen.hud.auto_allowed = screen.auto_allowed()
	check(not screen.auto_allowed(), "hard: no AUTO")
	check(not screen.hud.auto_at(corner), "hard: no AUTO corner")
	screen.toggle_auto()
	check(not screen.autopilot.on, "hard: it stays off")
	screen.queue_free()
	Router.params = old


func test_skip_corner_on_the_map() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = MissionScreen.new()
	root.add_child(screen)
	var view: Vector2 = screen.hud.get_viewport_rect().size
	var corner := Vector2(4, view.y - 4)
	check(not screen.hud.talking(), "nobody talks")
	check(screen.hud.auto_at(corner) and not screen.hud.skip_at(corner), "the corner is AUTO")
	screen.sim._start_general_talk(5, 0)
	check(screen.hud.talking(), "a general talks")
	check(screen.hud.skip_at(corner) and not screen.hud.auto_at(corner), "the corner is SKIP")
	var auto_was: bool = screen.autopilot.on
	screen._gui_input(_click(corner, InputEvent.DEVICE_ID_EMULATION))
	eq(screen.autopilot.on, auto_was, "a tap on it does not toggle the auto-hunt")
	check(screen._skip, "it skips, a touch too")
	screen._process(screen.tick)
	check(screen.sim.talk.is_empty(), "on the next tick the talk is over")
	check(not screen._skip, "once")

	screen.sim._start_general_talk(5, 0)
	Input.action_press("skip")
	screen._process(screen.tick)
	Input.action_release("skip")
	screen._process(0.0)
	check(screen.sim.talk.is_empty(), "the skip key")
	screen.free()
	Router.params = old


func _pad_back(pressed: bool) -> void:
	var ev := InputEventJoypadButton.new()
	ev.button_index = JOY_BUTTON_BACK
	ev.pressed = pressed
	Input.parse_input_event(ev)
	Input.flush_buffered_events()


## The pad's Back is SKIP and AUTO, as the corner: while someone talks it skips and leaves the
## auto-hunt as it was; when nobody talks it turns the auto-hunt on or off.
func test_pad_back_skips_or_toggles_auto() -> void:
	var old: Dictionary = Router.params
	var was: String = InputSetup.device
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = MissionScreen.new()
	root.add_child(screen)
	screen.sim.difficulty = 1
	var auto_was: bool = screen.autopilot.on
	screen.sim._start_general_talk(5, 0)
	_pad_back(true)
	screen._process(screen.tick)
	_pad_back(false)
	screen._process(0.0)
	check(screen.sim.talk.is_empty(), "a talk: Back skips it")
	eq(screen.autopilot.on, auto_was, "and the auto-hunt stays as it was")
	_pad_back(true)
	screen._process(0.0)
	_pad_back(false)
	screen._process(0.0)
	eq(screen.autopilot.on, not auto_was, "nobody talks: Back turns the auto-hunt on or off")
	screen.free()
	InputSetup.device = was
	Router.params = old


## As pyport's: on a talk of an ending SKIP goes to its pictures, on a picture to the next
## page; on a talk of the opening it ends the story.
func test_skip_the_story() -> void:
	var old: Dictionary = Router.params
	Router.params = {
		"story": 2, "reward_item": 502, "opened_lord": 8, "profile_path": "user://no_such_hero.json"
	}
	var screen: Control = Story.new()
	root.add_child(screen)
	screen._unhandled_input(_skip_key())
	eq(
		[screen.page, screen.pages[screen.page].kind],
		[14, "picture"],
		"an ending: on to its pictures"
	)
	screen.skip_button.pressed.emit()
	eq(screen.pages[screen.page].kind, "stats", "on a picture: the next page (the Skip button too)")
	screen.free()
	var host := Control.new()
	root.add_child(host)
	Router.attach(host)
	Router.go("title")
	Router.push("story", {"profile_path": "user://no_such_hero.json"})
	screen = Router.current
	screen.skip()
	eq(screen.page, 1, "the opening: a picture, the next one")
	screen.skip()
	eq(screen.pages[screen.page].kind, "talk", "then the talk")
	screen.skip()
	eq(Router.current_name(), "title", "on a talk: the end")
	Router.attach(null)
	host.free()
	Router.params = old


func test_skip_the_briefing() -> void:
	var old: Dictionary = Router.params
	var host := Control.new()
	root.add_child(host)
	Router.attach(host)
	Router.go(
		"briefing", {"lord": 1, "mission": 1, "line": 2, "profile_path": "user://no_such_hero.json"}
	)
	Router.current._unhandled_input(_skip_key())
	eq(
		[Router.current_name(), Router.params],
		["mission", {"lord": 1, "mission": 1}],
		"the skip key: the map"
	)
	Router.attach(null)
	host.free()
	Router.params = old
