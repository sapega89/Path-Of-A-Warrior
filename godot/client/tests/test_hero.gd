extends "res://tests/test_case.gd"

const Hero := preload("res://scripts/world/hero.gd")
const TouchControls := preload("res://scripts/ui/touch_controls.gd")


func test_directions() -> void:
	eq(Hero.dir8_of(Vector2.DOWN), 0, "down")
	eq(Hero.dir8_of(Vector2.LEFT), 2, "left")
	eq(Hero.dir8_of(Vector2.UP), 4, "up")
	eq(Hero.dir8_of(Vector2.RIGHT), 6, "right")
	eq(Hero.dir8_of(Vector2(1, 1)), 7, "down-right")


func test_walk_uses_original_tables() -> void:
	var h: CharacterBody3D = Hero.new()
	root.add_child(h)
	eq(int(h.info.frames), 53, "frames in the sheet")
	eq(h.current_frame(), 1, "idle facing down")
	h.step(Vector2.RIGHT, 0.016)
	check(h.walking, "walking")
	eq(h.dir8, 6, "facing right")
	eq(h.velocity.x, Hero.SPEED, "speed")
	eq(h.current_table(), h.info.walk[3], "walk table right")
	h.step(Vector2.ZERO, 0.016)
	eq(h.current_frame(), 10, "idle facing right")
	h.free()


func test_touch_stick() -> void:
	eq(TouchControls.stick_value(Vector2.ZERO, Vector2(45, 0), 90.0), Vector2(0.5, 0), "half right")
	eq(TouchControls.stick_value(Vector2.ZERO, Vector2(0, 500), 90.0), Vector2(0, 1), "clamped")
