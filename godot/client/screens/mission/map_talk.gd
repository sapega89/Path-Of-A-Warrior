class_name MapTalk
extends Control
## A talk over the map, in map pixels over the HUD's width: the portrait of who speaks in a
## 48 px box at the left and the line beside it from x 54, 38 high, both just above the HUD
## (and its skill bar).

@onready var face: PanelContainer = $Face
@onready var portrait: TextureRect = $Face/Portrait
@onready var box: PanelContainer = $Box
@onready var line: Label = $Box/Line


## Shows `text` beside the portrait `who`.
func show_line(who: Texture2D, text: String) -> void:
	var view := get_viewport_rect().size
	var k := MapHud.scale_of(view)
	var top := MapHud.top_of(view)
	var left := view.x / 2.0 - 120.0 * k
	portrait.texture = who
	portrait.custom_minimum_size = Vector2(46, 46) * k
	face.position = Vector2(left + 2 * k, top - 50 * k)
	face.size = Vector2(48, 48) * k
	line.text = text
	var px := int(11 * k)  # the line's size follows the HUD's scale
	line.add_theme_font_size_override("font_size", px)  # standards: allow theme_in_code (HUD scale)
	box.custom_minimum_size = Vector2(184, 38) * k
	box.size = box.custom_minimum_size
	box.reset_size()
	box.position = Vector2(left + 54 * k, top - 2 * k - box.size.y)
