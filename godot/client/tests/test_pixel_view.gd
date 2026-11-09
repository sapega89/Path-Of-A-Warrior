extends "res://tests/test_case.gd"
## The 3D world as pixel art (scripts/world/pixel_view.gd): drawn small and blown up in whole
## screen pixels, its colours held to steps; smooth when the setting is off; the camera moving in
## whole pixels of the world with what is left over made up by shifting the picture.

const PixelView := preload("res://scripts/world/pixel_view.gd")
const FollowCamera := preload("res://scripts/world/follow_camera.gd")
const MissionScreen := preload("res://scripts/screens/mission_screen.gd")
const TEST_PATH := "user://test_pixel_settings.cfg"


func _area(size: Vector2) -> Control:
	var c := Control.new()
	c.size = size
	root.add_child(c)
	return c


func _set_pixel_art(on: bool) -> void:
	var old_path: String = Settings.path
	Settings.path = TEST_PATH
	Settings.set_value("pixel_art", on)
	Settings.path = old_path
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))


func test_a_pixel_is_a_whole_number_of_screen_pixels() -> void:
	eq(PixelView.pixel_for(720.0, true), 2, "720 rows")
	eq(PixelView.pixel_for(1080.0, true), 3, "1080 rows")
	eq(PixelView.pixel_for(1440.0, true), 4, "1440 rows")
	eq(PixelView.pixel_for(2160.0, true), 6, "4K")
	eq(PixelView.pixel_for(240.0, true), 1, "never less than one")
	eq(PixelView.pixel_for(1080.0, false), 1, "smooth: the window's own pixels")


func test_the_world_is_drawn_small_and_blown_up() -> void:
	_set_pixel_art(true)
	var area := _area(Vector2(1280, 720))
	var view: Control = PixelView.new()
	area.add_child(view)
	var r: float = view.ratio
	var px: int = view.pixel
	check(px >= 1, "a pixel: %d" % px)
	var rows: int = view.viewport.size.y - 2 * view.margin
	check(absf(rows * px - 720.0 * r) < px, "the rows cover the area: %d × %d" % [rows, px])
	eq(view.margin, PixelView.MARGIN, "a pixel more on each side")
	check(view.scale.is_equal_approx(Vector2.ONE * px / r), "blown up by a whole pixel")
	check((view.size * view.scale).y >= 720.0, "covers the area")
	eq(view.viewport.msaa_3d, Viewport.MSAA_DISABLED, "no smoothing of the edges")
	check(view.material != null and (view.material as ShaderMaterial).shader == PixelView.POST,
		"the colours held to steps")
	eq(view.texture_filter, CanvasItem.TEXTURE_FILTER_NEAREST, "no smoothing when blown up")
	check(view.position.is_equal_approx(-Vector2.ONE * view.margin * px / r), "the margin off the screen")
	check(view.viewport.own_world_3d, "a world of its own")
	area.free()


func test_smooth_when_the_setting_is_off() -> void:
	_set_pixel_art(false)
	var area := _area(Vector2(1280, 720))
	var view: Control = PixelView.new()
	area.add_child(view)
	eq(view.pixel, 1, "the window's own pixels")
	eq(view.margin, 0, "no margin")
	check(view.material == null, "the colours as they are")
	check(view.viewport.msaa_3d != Viewport.MSAA_DISABLED, "smoothed edges")
	eq(view.viewport.size_2d_override, Vector2i(1280, 720), "positions in layout units")
	# and back on while it is shown
	_set_pixel_art(true)
	check(view.material != null and view.margin == PixelView.MARGIN, "pixel art again")
	area.free()


func test_the_camera_moves_in_whole_pixels() -> void:
	var holder := SubViewport.new()
	holder.size = Vector2i(642, 362)
	root.add_child(holder)
	var camera: Camera3D = FollowCamera.new()
	camera.focus = Vector3(3.37, 0.0, 5.123)
	holder.add_child(camera)
	camera.snap()
	check(camera.global_position.is_equal_approx(camera.goal()), "not snapped unless asked")
	eq(camera.pixel_rest, Vector2.ZERO, "nothing left over")
	camera.pixel_snap = true
	camera.snap()
	var s: float = camera.pixel_world_size()
	check(s > 0.0, "a pixel's size where it looks: %f" % s)
	var right: Vector3 = camera.global_basis.x
	var up: Vector3 = camera.global_basis.y
	var across: float = camera.global_position.dot(right) / s
	var along: float = camera.global_position.dot(up) / s
	check(absf(across - roundf(across)) < 0.001 and absf(along - roundf(along)) < 0.001,
		"on the grid of pixels: %f, %f" % [across, along])
	var rest: Vector2 = camera.pixel_rest
	check(absf(rest.x) <= 0.5 and absf(rest.y) <= 0.5, "less than half a pixel left over: %s" % rest)
	var smooth: Vector3 = camera.global_position + right * rest.x * s - up * rest.y * s
	check(smooth.is_equal_approx(camera.goal()), "the snapped place and what is left over make the goal")
	# a slow move still gets there: the snapping does not hold the camera back
	camera.focus += Vector3(0.5, 0.0, 0.0)
	var start: Vector3 = camera.global_position
	for i in 200:
		camera._process(1.0 / 60.0)
	check(camera.global_position.distance_to(start) > 0.45, "it followed the focus")
	holder.free()


func test_the_mission_draws_its_world_in_a_pixel_view() -> void:
	_set_pixel_art(true)
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = MissionScreen.new()
	root.add_child(screen)
	var view: Node = screen.get_node("World")
	check(view.get_script() == PixelView, "the world is a pixel view")
	check(screen.viewport == view.viewport, "the screen's viewport is the view's")
	view._process(0.0)
	check(screen.camera.pixel_snap, "its camera moves in whole pixels")
	screen.free()
	Router.params = old
