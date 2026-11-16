extends "res://tests/test_case.gd"
## The 3D world as pixel art (scripts/world/pixel_view.gd): drawn small and blown up in whole
## screen pixels, its colours held to steps, and never smooth; the camera moving in whole pixels
## of the world, with what is left over made up by shifting the picture.

const MAP_VIEW := preload("res://scenes/world/map_view.tscn")
const TEST_PATH := "user://test_pixel_settings.cfg"


func _area(size: Vector2) -> Control:
	var c := Control.new()
	c.size = size
	root.add_child(c)
	return c


func _set_setting(key: String, value: Variant) -> void:
	var old_path: String = Settings.path
	Settings.path = TEST_PATH
	Settings.set_value(key, value)
	Settings.path = old_path
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))


func _view_in(area: Control) -> MapView:
	var view: MapView = MAP_VIEW.instantiate()
	area.add_child(view)
	return view


func test_a_pixel_is_a_whole_number_of_screen_pixels() -> void:
	eq(PixelView.pixel_for(720.0), 2, "720 rows")
	eq(PixelView.pixel_for(1080.0), 3, "1080 rows")
	eq(PixelView.pixel_for(1440.0), 4, "1440 rows")
	eq(PixelView.pixel_for(2160.0), 6, "4K")
	eq(PixelView.pixel_for(240.0), 1, "never less than one")


func test_the_world_is_drawn_small_and_blown_up() -> void:
	var area := _area(Vector2(1280, 720))
	var view := _view_in(area)
	var r: float = view.ratio
	var px: int = view.pixel
	check(px >= 1, "a pixel: %d" % px)
	var rows: int = view.viewport.size.y - 2 * PixelView.MARGIN
	check(absf(rows * px - 720.0 * r) < px, "the rows cover the area: %d × %d" % [rows, px])
	eq(view.viewport.size_2d_override.y, roundi(view.viewport.size.y * px / r), "layout units")
	check(view.scale.is_equal_approx(Vector2.ONE * px / r), "blown up by a whole pixel")
	check((view.size * view.scale).y >= 720.0, "covers the area")
	eq(view.viewport.msaa_3d, Viewport.MSAA_DISABLED, "no smoothing of the edges")
	var post := view.material as ShaderMaterial
	check(post != null and post.shader == PixelView.POST, "the colours held to steps")
	eq(view.texture_filter, CanvasItem.TEXTURE_FILTER_NEAREST, "no smoothing when blown up")
	check(view.position.is_equal_approx(-Vector2.ONE * px / r), "the margin off the screen")
	area.free()


func test_the_brightness_goes_through_the_steps() -> void:
	var area := _area(Vector2(1280, 720))
	var view := _view_in(area)
	_set_setting("brightness", 0.8)
	eq(view.material, view.post, "brighter: the same shader takes the brightness")
	_set_setting("brightness", 0.2)
	eq(view.material, view.post, "darker: the same")
	_set_setting("brightness", 0.5)
	area.free()


func test_the_graphics_quality() -> void:
	var area := _area(Vector2(1280, 720))
	var view := _view_in(area)
	eq(view.viewport.positional_shadow_atlas_size, 2048, "Medium: the lamps' shadows the engine's")
	_set_setting("graphics", 0)
	eq(view.viewport.positional_shadow_atlas_size, 1024, "Low: coarser shadows of lamps")
	_set_setting("graphics", 2)
	eq(view.viewport.positional_shadow_atlas_size, 4096, "High: finer shadows of lamps")
	eq(view.viewport.msaa_3d, Viewport.MSAA_DISABLED, "never smoothed")
	_set_setting("graphics", 1)
	area.free()


func test_the_camera_moves_in_whole_pixels() -> void:
	var holder := SubViewport.new()
	holder.size = Vector2i(642, 362)
	root.add_child(holder)
	var camera := FollowCamera.new()
	camera.focus = Vector3(3.37, 0.0, 5.123)
	holder.add_child(camera)
	camera.snap()
	check(camera.global_position.is_equal_approx(camera.goal()), "not snapped unless asked")
	eq(camera.pixel_rest, Vector2.ZERO, "nothing left over")
	camera.pixel_snap = true
	camera.snap()
	var s := camera.pixel_world_size()
	check(s > 0.0, "a pixel's size where it looks: %f" % s)
	var right := camera.global_basis.x
	var up := camera.global_basis.y
	var across := camera.global_position.dot(right) / s
	var along := camera.global_position.dot(up) / s
	check(
		absf(across - roundf(across)) < 0.001 and absf(along - roundf(along)) < 0.001,
		"on the grid of pixels: %f, %f" % [across, along]
	)
	var rest := camera.pixel_rest
	check(absf(rest.x) <= 0.5 and absf(rest.y) <= 0.5, "less than half a pixel over: %s" % rest)
	var smooth := camera.global_position + right * rest.x * s - up * rest.y * s
	check(smooth.is_equal_approx(camera.goal()), "the snapped place and the rest make the goal")
	# a slow move still gets there: the snapping does not hold the camera back
	camera.focus += Vector3(0.5, 0.0, 0.0)
	var start := camera.global_position
	for i in 200:
		camera._process(1.0 / 60.0)
	check(camera.global_position.distance_to(start) > 0.45, "it followed the focus")
	holder.free()


func test_the_mission_draws_its_world_as_pixel_art() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = Router.make(Router.SCREENS["mission"])
	root.add_child(screen)
	var view := screen.get_node("World") as PixelView
	check(view != null, "the world is a pixel view")
	view._process(0.0)
	check(screen.camera.pixel_snap, "its camera moves in whole pixels")
	check(view.material != null, "its colours held to steps")
	screen.free()
	Router.params = old
