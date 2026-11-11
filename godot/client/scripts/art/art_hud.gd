class_name ArtHud
extends Control
## HUD in the new art: a round portrait drawn live from the hero's model, health and
## spirit bars, the skill keys with folk-print icons, the purse and the place name.
## Its layout is scenes/art/art_hud.tscn (a skill's slot art_skill.tscn), its plates and
## letters the theme art_hud_theme.tres; icons are SVG (assets/art/ui).

const UI := "res://assets/art/ui/%s.svg"
const SCENE := "res://scenes/art/art_hud.tscn"
## The HUD's plates, bars and letters (its fonts made ready by UiTheme.theme()).
const THEME := "res://assets/art/ui/art_hud_theme.tres"
const SKILL_SCENE := preload("res://scenes/art/art_skill.tscn")
const SKILLS := ["sabre", "shield", "fire", "wind", "potion"]
const COOLING := 2  # the skill shown cooling down
const PLACE_NAMES := {"camp": "Корсунь", "battle": "Крута балка"}

const GOLD := Color("B08D4A")  # tarnished brass
const PAPER := Color("DCD3C2")
const DUSK := Color("1D1B1A")

var hero: Node3D
var screen := Vector2(1280, 720)

@onready var portrait_view: SubViewport = %PortraitView
@onready var portrait_camera: Camera3D = %Camera


static func icon(icon_name: String, px: int) -> Texture2D:
	var f := FileAccess.open(UI % icon_name, FileAccess.READ)
	if f == null:
		return null
	var svg := f.get_as_text()
	var img := Image.new()
	var probe := Image.new()
	probe.load_svg_from_string(svg, 1.0)
	var scale_by := float(px) / float(maxi(probe.get_width(), 1))
	img.load_svg_from_string(svg, scale_by)
	return ImageTexture.create_from_image(img)


## Shows the HUD over `place` (camp, battle), the portrait following `hero_node`.
func setup(hero_node: Node3D, place: String) -> void:
	hero = hero_node
	screen = get_viewport_rect().size
	theme = UiTheme.theme(THEME)
	(%Face as TextureRect).texture = portrait_view.get_texture()
	(%Ornament as TextureRect).texture = icon("ornament", 300)
	(%Coin as TextureRect).texture = icon("coin", 64)
	(%Place as Label).text = PLACE_NAMES.get(place, place)
	for i in SKILLS.size():
		_add_skill(i, i == 0 and place == "battle")


## A skill's slot (art_skill.tscn): its icon, its key, the first lit in a battle.
func _add_skill(i: int, active: bool) -> void:
	var slot: Panel = SKILL_SCENE.instantiate()
	if active:
		slot.theme_type_variation = &"ArtSkillActive"
	(slot.get_node("Icon") as TextureRect).texture = icon(SKILLS[i], 128)
	(slot.get_node("Key") as Label).text = str(i + 1)
	slot.get_node("Cooldown").visible = i == COOLING
	slot.get_node("Turns").visible = i == COOLING
	%Skills.add_child(slot)


func _process(_delta: float) -> void:
	if hero == null or not is_instance_valid(hero):
		return
	var forward := Vector3(sin(hero.rotation.y), 0.0, cos(hero.rotation.y))
	var head := hero.global_position + Vector3(0, 1.66, 0)
	portrait_camera.global_position = (
		head + forward * 1.25 + Vector3(0.25, 0.12, 0).rotated(Vector3.UP, hero.rotation.y)
	)
	portrait_camera.look_at(head + Vector3(0, 0.02, 0), Vector3.UP)


func _draw() -> void:
	# touch stick, as on a phone
	var c := Vector2(130, screen.y - 130)
	draw_circle(c, 86, Color(DUSK, 0.28))
	draw_arc(c, 86, 0, TAU, 64, Color(PAPER, 0.45), 3.0, true)
	draw_circle(c + Vector2(18, -10), 34, Color(PAPER, 0.35))
	draw_arc(c + Vector2(18, -10), 34, 0, TAU, 48, Color(GOLD, 0.8), 3.0, true)
