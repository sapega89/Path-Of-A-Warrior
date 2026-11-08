extends "res://tests/test_case.gd"
## The 3D world under the screens (scripts/world/world_view.gd): drawn at the window's own
## pixels, shown scaled back to the layout, the camera's screen positions in layout units,
## 4x multisampling; the mission and the online battle draw their worlds in it.

const WorldView := preload("res://scripts/world/world_view.gd")


func test_the_world_is_drawn_at_the_windows_pixels() -> void:
	var screen := Control.new()
	screen.size = Vector2(1280, 720)
	root.add_child(screen)
	var view := WorldView.new()
	screen.add_child(view)
	var f: float = view.pixel_ratio()
	check(f >= 1.0, "never below the layout's size")
	eq(view.viewport.size, Vector2i((Vector2(1280, 720) * f).ceil()), "the world in window pixels")
	check(view.scale.is_equal_approx(Vector2.ONE / f), "shown scaled back down")
	check((view.size * view.scale).is_equal_approx((Vector2(1280, 720) * f).ceil() / f), "over the whole screen")
	eq(view.viewport.size_2d_override, Vector2i(1280, 720), "positions in layout units")
	eq(view.viewport.msaa_3d, Viewport.MSAA_4X, "smooth edges")
	# a camera's screen position is in layout units whatever the window's pixels
	var cam := Camera3D.new()
	view.viewport.add_child(cam)
	cam.look_at_from_position(Vector3(0, 0, 5), Vector3.ZERO, Vector3.UP)
	check(cam.unproject_position(Vector3.ZERO).is_equal_approx(Vector2(640, 360)), "the middle of the layout")
	# the screen grows: the world follows
	screen.size = Vector2(1560, 720)
	eq(view.viewport.size_2d_override, Vector2i(1560, 720), "after a resize")
	eq(view.viewport.size, Vector2i((Vector2(1560, 720) * f).ceil()), "after a resize, in window pixels")
	screen.free()


func test_the_screens_draw_their_worlds_in_it() -> void:
	for path in ["res://scripts/screens/mission_screen.gd", "res://scripts/screens/online_battle_screen.gd",
			"res://scripts/screens/map_viewer.gd"]:
		var code := FileAccess.get_file_as_string(path)
		check(code.contains("WorldView.new()"), path)
		check(not code.contains("SubViewportContainer.new()"), path + " has no plain container")
