extends "res://tests/test_case.gd"
## The map viewer (screens/map_viewer): the hero shown as the missions show a new one, the
## Cossack's 3D figure with the first kind of weapon, walking and turning with the body under it.


func test_the_hero_is_the_cossack_figure() -> void:
	var viewer: MapViewer = Router.make(Router.SCREENS["map_viewer"])
	root.add_child(viewer)
	eq(viewer.figure.kind, MapPeople.HEROES.front(), "the Cossack's figure")
	check(
		viewer.figure.skeleton.find_child(MapPeople.BLADES.front(), true, false) != null,
		"his weapon"
	)
	check(not viewer.hero.sprite.visible, "not the flat picture")
	eq(viewer.figure.player.current_animation, "idle_2h", "standing, the spear ready in both hands")
	for i in 10:
		viewer.hero.step(Vector2.RIGHT, 1.0 / 60.0)
	viewer._process(1.0)
	eq(viewer.figure.player.current_animation, "walk", "walking")
	for i in 30:
		viewer.hero.step(Vector2.ZERO, 1.0 / 60.0)
	viewer._process(1.0)
	eq(viewer.figure.player.current_animation, "idle_2h", "and stopped again")
	check(
		is_equal_approx(viewer.figure.rotation.y, Motion.yaw_of(viewer.hero.dir8)),
		"turned the way he goes"
	)
	viewer.free()
