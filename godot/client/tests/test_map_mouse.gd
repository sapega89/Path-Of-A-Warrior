extends "res://tests/test_case.gd"
## The mouse on a mission's map, as pyport's pointer: beside the hero walks, on him attacks.

const MissionScreen := preload("res://scripts/screens/mission_screen.gd")


func _click(at: Vector2, button := MOUSE_BUTTON_LEFT, pressed := true) -> InputEventMouseButton:
	var ev := InputEventMouseButton.new()
	ev.button_index = button
	ev.pressed = pressed
	ev.position = at
	return ev


func _hero_middle(screen: Control) -> Vector2:
	var middle: Vector3 = screen.hero.global_position + Vector3(0, 26.0 / 27.0, 0)
	return screen.camera.unproject_position(middle)


func _screen() -> Control:
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = MissionScreen.new()
	root.add_child(screen)
	return screen


func test_click_beside_the_hero_walks_that_way() -> void:
	var old: Dictionary = Router.params
	var screen := _screen()
	var c := _hero_middle(screen)
	eq(screen.pointer_dir(c), -1, "on the hero")
	eq(screen.pointer_dir(c + Vector2(200, 30)), 6, "right")
	eq(screen.pointer_dir(c + Vector2(-200, 30)), 2, "left")
	eq(screen.pointer_dir(c + Vector2(30, -200)), 4, "up")
	eq(screen.pointer_dir(c + Vector2(30, 200)), 0, "down")
	var start: Vector2i = screen.sim.hero.pos
	screen._unhandled_input(_click(c + Vector2(200, 0)))
	eq(screen._mouse_dir, 6, "the button holds right")
	eq(screen._pressed, 6, "a press of right")
	for i in 6:
		screen._process(screen.tick)
	check(screen.sim.hero.pos.x > start.x, "the hero walked right while the button was held")
	var drag := InputEventMouseMotion.new()
	drag.position = c + Vector2(0, -200)
	screen._unhandled_input(drag)
	eq(screen._mouse_dir, 4, "dragging turns him")
	screen._unhandled_input(_click(c + Vector2(0, -200), MOUSE_BUTTON_LEFT, false))
	eq(screen._mouse_dir, -1, "the button let go: he stops")
	screen.free()
	Router.params = old


func test_click_on_the_hero_or_right_button_attacks() -> void:
	var old: Dictionary = Router.params
	var screen := _screen()
	var c := _hero_middle(screen)
	screen._unhandled_input(_click(c))
	check(screen._fire, "a click on the hero")
	eq(screen._mouse_dir, -1, "and no walking")
	screen._fire = false
	screen._unhandled_input(_click(c + Vector2(300, -100), MOUSE_BUTTON_RIGHT))
	check(screen._fire, "the right button: where he faces")
	eq(screen._mouse_dir, -1, "the right button does not walk")
	screen._fire = false
	var touch := _click(c + Vector2(200, 0))
	touch.device = InputEvent.DEVICE_ID_EMULATION
	screen._unhandled_input(touch)
	eq(screen._mouse_dir, -1, "a touch: the touch controls walk, not the tap")
	check(not screen._fire, "nor attack")
	screen.free()
	Router.params = old


func test_pause_corner() -> void:
	var old: Dictionary = Router.params
	var screen := _screen()
	var view: Vector2 = screen.hud.get_viewport_rect().size
	check(not screen.hud.pause_at(view - Vector2(200, 2)), "not left of the corner")
	check(screen.hud.pause_at(view - Vector2(4, 4)), "the bottom-right corner")
	screen._unhandled_input(_click(view - Vector2(4, 4)))
	check(screen.pause_menu != null, "PAUSE pauses")
	screen.free()
	Router.params = old
