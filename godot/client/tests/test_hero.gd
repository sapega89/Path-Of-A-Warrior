extends "res://tests/test_case.gd"


## A hero in the tree.
func _hero() -> Hero:
	var h := (load("res://scenes/world/hero.tscn") as PackedScene).instantiate() as Hero
	root.add_child(h)
	return h


func test_directions() -> void:
	eq(Hero.dir8_of(Vector2.DOWN), 0, "down")
	eq(Hero.dir8_of(Vector2.LEFT), 2, "left")
	eq(Hero.dir8_of(Vector2.UP), 4, "up")
	eq(Hero.dir8_of(Vector2.RIGHT), 6, "right")
	eq(Hero.dir8_of(Vector2(1, 1)), 7, "down-right")


func test_walk() -> void:
	var h := _hero()
	check(h.find_children("*", "Sprite3D").is_empty(), "only the body: the figure is drawn")
	check(not h.walking, "standing")
	h.step(Vector2.RIGHT, 0.016)
	check(h.walking, "walking")
	eq(h.dir8, 6, "facing right")
	eq(h.velocity.x, Hero.SPEED, "speed")
	h.step(Vector2.ZERO, 0.016)
	check(not h.walking, "stopped")
	eq(h.dir8, 6, "still facing right")
	h.free()


func test_the_hero_steps_every_frame() -> void:
	var h := _hero()
	check(h.is_processing(), "a step each frame")
	check(not h.is_physics_processing(), "not each physics tick")
	h.free()


func test_touch_stick() -> void:
	eq(TouchControls.stick_value(Vector2.ZERO, Vector2(45, 0), 90.0), Vector2(0.5, 0), "half right")
	eq(TouchControls.stick_value(Vector2.ZERO, Vector2(0, 500), 90.0), Vector2(0, 1), "clamped")
