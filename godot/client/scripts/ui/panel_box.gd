class_name PanelBox
extends StyleBox
## The plate of a panel or a window: dark leather in an iron rim, a stitched seam inside it and
## an iron rivet in each corner. Its content margins are set where it is used (theme.tres): a
## script's _init runs after the loaded values, so it leaves them alone.

## How far it reaches out of its rect: left, top, right, bottom (a window's frame and title).
@export var outset: Array[float] = [0.0, 0.0, 0.0, 0.0]

var plate: StyleBoxFlat


func _init() -> void:
	plate = Ornament.flat(Color(UiTheme.PANEL, 0.97), UiTheme.IRON, 3, UiTheme.RADIUS)
	plate.shadow_color = Color(0, 0, 0, 0.55)
	plate.shadow_size = 10
	plate.shadow_offset = Vector2(0, 4)


func _get_draw_rect(rect: Rect2) -> Rect2:
	return rect.grow_individual(outset[0], outset[1], outset[2], outset[3])


func _draw(to: RID, rect: Rect2) -> void:
	rect = _get_draw_rect(rect)
	plate.draw(to, rect)
	if rect.size.x < 40 or rect.size.y < 40:
		return
	Ornament.grain(to, rect.grow(-3))
	Ornament.seam(to, rect.grow(-8), UiTheme.THREAD)
	for corner in [
		rect.position,
		Vector2(rect.end.x, rect.position.y),
		rect.end,
		Vector2(rect.position.x, rect.end.y)
	]:
		var c: Vector2 = corner + (rect.get_center() - corner).sign() * 8.0
		Ornament.rivet(to, c, 4.5)
