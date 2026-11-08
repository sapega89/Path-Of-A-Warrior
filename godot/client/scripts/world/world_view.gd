extends SubViewportContainer
## The 3D world under a screen, drawn at the window's own pixels.
##
## The screens are laid out at 1280×720 and stretched to the window (canvas_items). A plain
## stretched container would draw its world at that layout size, and the window would then
## scale the picture up, blurring it on a phone's sharper screen. This one is as many times
## larger as the window is than the layout and is shown scaled down by as much, so each pixel
## of the world falls on one pixel of the screen. Its viewport still reports the layout size
## (size_2d_override), so positions the screens take from the camera
## (Camera3D.unproject_position) stay in layout units. The edges are smoothed by 4x
## multisampling.

var viewport: SubViewport


func _init() -> void:
	stretch = true
	viewport = SubViewport.new()
	viewport.msaa_3d = Viewport.MSAA_4X
	viewport.size_2d_override_stretch = true
	add_child(viewport)


func _ready() -> void:
	get_tree().root.size_changed.connect(fit)
	var parent := get_parent() as Control
	if parent != null:
		parent.resized.connect(fit)
	fit()


## How many window pixels one layout unit is (1 when the window is the layout's size).
func pixel_ratio() -> float:
	var root := get_tree().root
	var layout := root.get_visible_rect().size
	if layout.x <= 0.0 or layout.y <= 0.0:
		return 1.0
	return maxf(1.0, minf(root.size.x / layout.x, root.size.y / layout.y))


## Covers the parent (or the whole screen) again after the window or the parent changed size.
func fit() -> void:
	var parent := get_parent() as Control
	var area: Vector2 = parent.size if parent != null else get_tree().root.get_visible_rect().size
	if area.x <= 0.0 or area.y <= 0.0:
		return
	var f := pixel_ratio()
	position = Vector2.ZERO
	scale = Vector2.ONE / f
	size = (area * f).ceil()
	viewport.size_2d_override = Vector2i(area.round())
