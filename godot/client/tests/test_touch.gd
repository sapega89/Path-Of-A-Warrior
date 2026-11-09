extends "res://tests/test_case.gd"
## The touch controls' buttons send their actions as input events, as keys do.


func test_touch_buttons_press_their_actions() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = MissionScreen.new()
	root.add_child(screen)
	var touch: Control = screen.get_node("Touch")
	touch._touch(0, touch.button_center("attack"), true)
	Input.flush_buffered_events()
	check(Input.is_action_pressed("attack"), "attack held while the finger is on it")
	touch._touch(0, touch.button_center("attack"), false)
	Input.flush_buffered_events()
	check(not Input.is_action_pressed("attack"), "and let go")
	check(screen.pause_menu == null, "not paused yet")
	touch._touch(1, touch.button_center("pause"), true)
	Input.flush_buffered_events()
	check(screen.pause_menu != null, "PAUSE pauses the mission, as Esc or Start")
	touch._touch(1, touch.button_center("pause"), false)
	Input.flush_buffered_events()
	check(not Input.is_action_pressed("pause"), "PAUSE let go")
	screen.free()
	Router.params = old
