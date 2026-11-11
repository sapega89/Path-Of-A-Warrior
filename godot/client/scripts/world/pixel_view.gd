class_name PixelView
extends SubViewportContainer
## A 3D world on the screen (a map's MapView), drawn by its child Viewport as pixel art. It places
## and sizes itself over its parent (no anchors), stretching its viewport.
##
## The world is drawn small, about ROWS rows of pixels high, with no smoothing of its edges, and
## blown up without smoothing, so each of its pixels is a crisp square of `pixel` screen pixels,
## the same whole number across the screen. Its colours are then held to a few steps of lightness
## and colour with an ordered dither between them (pixel_post.gdshader). The setting "brightness"
## lifts or deepens the shade of the world (Settings.world_gamma) before those steps, in the same
## shader. The graphics quality (Settings.GRAPHICS) sets how good the lamps' and fires' shadows
## are.
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
## About how many rows of pixels the world has, whatever the window.
const ROWS := 360.0
## Pixels of the world drawn past each edge.
const MARGIN := 1
## After the camera has moved in the frame, so the picture is shifted by where it is now.
const AFTER_THE_CAMERA := 100

## Screen pixels to one pixel of the world.
var pixel := 1
## Screen pixels to one layout unit.
var ratio := 1.0
var post := ShaderMaterial.new()

@onready var viewport: SubViewport = $Viewport


## Screen pixels to one pixel of the world for an area this many screen pixels high.
static func pixel_for(screen_rows: float) -> int:
	return maxi(1, roundi(screen_rows / ROWS))


func _ready() -> void:
	process_priority = AFTER_THE_CAMERA
	post.shader = POST
	material = post
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	viewport.msaa_3d = Viewport.MSAA_DISABLED
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


## Covers the parent (or the whole screen) again after the window, the parent or the graphics
## quality changed.
func fit() -> void:
	if not is_inside_tree():
		return
	var parent := get_parent() as Control
	var area: Vector2 = parent.size if parent != null else get_tree().root.get_visible_rect().size
	if area.x <= 0.0 or area.y <= 0.0:
		return
	ratio = pixel_ratio()
	pixel = pixel_for(area.y * ratio)
	var cells := (area * ratio / pixel).ceil() + Vector2.ONE * MARGIN * 2
	scale = Vector2.ONE * (pixel / ratio)
	size = cells
	viewport.size_2d_override = Vector2i((cells * pixel / ratio).round())
	viewport.positional_shadow_atlas_size = Settings.graphics().lamps
	_place(Vector2.ZERO)


## The world's camera, told to move in whole pixels; the picture shifted by what it has left over.
func _process(_delta: float) -> void:
	var camera := viewport.get_camera_3d() as FollowCamera
	var rest := Vector2.ZERO
	if camera != null:
		camera.pixel_snap = true
		rest = camera.pixel_rest
	_place(rest)


func _on_setting(key: String) -> void:
	if key == "graphics":
		fit()


func _place(rest: Vector2) -> void:
	position = -(Vector2.ONE * MARGIN + rest) * pixel / ratio
