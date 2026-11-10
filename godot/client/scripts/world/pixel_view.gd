class_name PixelView
extends SubViewportContainer
## A 3D world on the screen (a map's MapView), drawn by its child Viewport. It places and sizes
## itself over its parent (no anchors), stretching its viewport.
##
## Pixel art (the setting "pixel_art", on by default): the world is drawn small, about ROWS rows
## of pixels high, and blown up without smoothing, so each of its pixels is a crisp square of
## `pixel` screen pixels, the same whole number across the screen. Its colours are then held to
## a few steps of lightness and colour with an ordered dither between them (pixel_post.gdshader).
## Off: the world is drawn at the window's own pixels with smoothed edges (as the graphics
## quality says: Settings.GRAPHICS msaa), and the lamps' and fires' shadows are as good as it says.
## The setting "brightness" lifts or deepens the shade of the world (Settings.world_gamma): in
## pixel art before its steps, smooth by the shader world_light.gdshader, which is left off at
## the middle brightness, so the colours stay as they are.
##
## The screens are laid out at 1280×720 and stretched to the window (canvas_items). The viewport
## still reports the layout size (size_2d_override), so positions the screens take from the
## camera (Camera3D.unproject_position) stay in layout units.
##
## A FollowCamera moves in whole pixels of the world (its pixel_snap), so the land does not
## shimmer as it goes. What it moved between two of them (its pixel_rest) is made up here by
## shifting the picture, so the move stays smooth. For that the world is drawn MARGIN pixels
## larger on each side.

const POST := preload("res://assets/art/shaders/pixel_post.gdshader")
const LIGHT := preload("res://assets/art/shaders/world_light.gdshader")
## About how many rows of pixels the world has in pixel art, whatever the window.
const ROWS := 360.0
const MARGIN := 1
## After the camera has moved in the frame, so the picture is shifted by where it is now.
const AFTER_THE_CAMERA := 100

## Whether the world is drawn as pixel art now (the setting).
var pixel_art := true
## Screen pixels to one pixel of the world (1 when smooth).
var pixel := 1
## Pixels of the world drawn past each edge.
var margin := 0
## Screen pixels to one layout unit.
var ratio := 1.0
var post := ShaderMaterial.new()
var light := ShaderMaterial.new()  # the smooth world's brightness

@onready var viewport: SubViewport = $Viewport


## Screen pixels to one pixel of the world for an area this many screen pixels high.
static func pixel_for(screen_rows: float, on: bool) -> int:
	return maxi(1, roundi(screen_rows / ROWS)) if on else 1


func _ready() -> void:
	process_priority = AFTER_THE_CAMERA
	post.shader = POST
	light.shader = LIGHT
	viewport.size_2d_override_stretch = true
	get_tree().root.size_changed.connect(fit)
	var parent := get_parent() as Control
	if parent != null:
		parent.resized.connect(fit)
	Settings.changed.connect(_on_setting)
	fit()


## Screen pixels to one layout unit (1 when the window is the layout's size).
func pixel_ratio() -> float:
	var root := get_tree().root
	var layout := root.get_visible_rect().size
	if layout.x <= 0.0 or layout.y <= 0.0:
		return 1.0
	return maxf(0.01, minf(root.size.x / layout.x, root.size.y / layout.y))


## Covers the parent (or the whole screen) again after the window, the parent or the setting
## changed.
func fit() -> void:
	if not is_inside_tree():
		return
	var parent := get_parent() as Control
	var area: Vector2 = parent.size if parent != null else get_tree().root.get_visible_rect().size
	if area.x <= 0.0 or area.y <= 0.0:
		return
	ratio = pixel_ratio()
	pixel_art = bool(Settings.get_value("pixel_art"))
	pixel = pixel_for(area.y * ratio, pixel_art)
	margin = MARGIN if pixel_art else 0
	var cells := (area * ratio / pixel).ceil() + Vector2.ONE * margin * 2
	scale = Vector2.ONE * (pixel / ratio)
	size = cells
	viewport.size_2d_override = Vector2i((cells * pixel / ratio).round())
	var graphics: Dictionary = Settings.graphics()
	viewport.msaa_3d = Viewport.MSAA_DISABLED if pixel_art else graphics.msaa
	viewport.positional_shadow_atlas_size = graphics.lamps
	material = post if pixel_art else _smooth_material()
	texture_filter = (
		CanvasItem.TEXTURE_FILTER_NEAREST if pixel_art else CanvasItem.TEXTURE_FILTER_LINEAR
	)
	_place(Vector2.ZERO)


## The world's camera, told to move in whole pixels in pixel art; the picture shifted by what it
## has left over.
func _process(_delta: float) -> void:
	var camera := viewport.get_camera_3d() as FollowCamera
	var rest := Vector2.ZERO
	if camera != null:
		camera.pixel_snap = pixel_art
		rest = camera.pixel_rest
	_place(rest)


func _on_setting(key: String) -> void:
	if key in ["pixel_art", "brightness", "graphics"]:
		fit()


func _smooth_material() -> Material:
	var middle: bool = is_equal_approx(
		float(Settings.get_value("brightness")), float(Settings.DEFAULTS.brightness)
	)
	return null if middle else light


func _place(rest: Vector2) -> void:
	position = -(Vector2.ONE * margin + rest) * pixel / ratio
