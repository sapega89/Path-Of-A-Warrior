extends "res://tests/test_case.gd"
## SKIP, as pyport's left soft key: Q, F1 or the pad's Back, or a click on SKIP. It skips the
## talk on the map, the briefing and the story.


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
	var screen: Control = Router.make(Router.SCREENS["mission"])
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
	screen.hud.refresh()
	check(not screen.hud.get_node("%Auto").visible, "hard: no AUTO corner")
	screen.toggle_auto()
	check(not screen.autopilot.on, "hard: it stays off")
	screen.queue_free()
	Router.params = old


func test_skip_corner_on_the_map() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = Router.make(Router.SCREENS["mission"])
	root.add_child(screen)
	var view: Vector2 = screen.hud.get_viewport_rect().size
	var corner := Vector2(4, view.y - 4)
	var auto: Button = screen.hud.get_node("%Auto")
	var skip: Button = screen.hud.get_node("%Skip")
	check(not screen.hud.talking(), "nobody talks")
	check(auto.visible and not skip.visible, "the corner is AUTO")
	MapTalks.start_general_talk(screen.sim, 5, 0)
	screen.hud.refresh()
	check(screen.hud.talking(), "a general talks")
	check(skip.visible and not auto.visible, "the corner is SKIP")
	check(skip.get_global_rect().has_point(corner), "in AUTO's place")
	var auto_was: bool = screen.autopilot.on
	root.get_viewport().push_input(_click(corner, InputEvent.DEVICE_ID_EMULATION), true)
	var up := _click(corner, InputEvent.DEVICE_ID_EMULATION)
	up.pressed = false
	root.get_viewport().push_input(up, true)
	eq(screen.autopilot.on, auto_was, "a tap on it does not toggle the auto-hunt")
	check(screen._skip, "it skips, a touch too")
	screen._process(screen.tick)
	check(screen.sim.talk.is_empty(), "on the next tick the talk is over")
	check(not screen._skip, "once")

	MapTalks.start_general_talk(screen.sim, 5, 0)
	_action("skip", true)
	screen._process(screen.tick)
	_action("skip", false)
	screen._process(0.0)
	check(screen.sim.talk.is_empty(), "the skip key")
	screen.free()
	Router.params = old


func _action(action: String, pressed: bool) -> void:
	var ev := InputEventAction.new()
	ev.action = action
	ev.pressed = pressed
	Input.parse_input_event(ev)
	Input.flush_buffered_events()


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
	var screen: Control = Router.make(Router.SCREENS["mission"])
	root.add_child(screen)
	screen.sim.difficulty = 1
	var auto_was: bool = screen.autopilot.on
	MapTalks.start_general_talk(screen.sim, 5, 0)
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
	var screen: Control = Router.make(Router.SCREENS["story"])
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
