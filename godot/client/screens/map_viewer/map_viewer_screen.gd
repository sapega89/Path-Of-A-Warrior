class_name MapViewer
extends BaseScreen
## Walks the hero around the maps of the campaign in 3D, in the new art (MapArt). skill_3 /
## skill_4 (keys 3 / 4, gamepad LB / RB) switch to the previous / next map; the line at the top
## names the keys of the device in use. The hero is shown as the missions show a new one: the
## figure of the first class (the Cossack) with the first kind of weapon, a long one held ready
## in both hands (the body under it walks, the figure stands or walks and turns the way he goes).

## The hero's kind of weapon (MapPeople.BLADES): the first one.
const WEAPON_KIND := 0

var map_number := 1
var map_total := 0

@onready var view: MapView = $World
@onready var hero: Hero = $World/Viewport/WorldRoot/Hero
@onready var figure: ArtFigure = $World/Viewport/WorldRoot/Hero/Figure
@onready var info: Label = %Info


func _ready() -> void:
	view.camera.target = hero
	figure.setup(MapPeople.HEROES.front())
	figure.unequip_all()
	figure.equip(MapPeople.BLADES[WEAPON_KIND])
	figure.play(Motion.idle(WEAPON_KIND), 0.0)
	hero.sprite.visible = false
	InputSetup.device_changed.connect(show_info)
	map_total = MapBuilder.map_count()
	show_map(1)


func show_map(number: int) -> bool:
	var data := MapBuilder.load_map(number)
	if data.is_empty():
		return false
	map_number = number
	view.map.build(data)
	hero.global_position = MapBuilder.cell_to_world(view.map.start_cell(0)) + Vector3(0, 0.05, 0)
	hero.velocity = Vector3.ZERO
	figure.rotation.y = Motion.yaw_of(hero.dir8)
	view.camera.snap()
	show_info()
	return true


func _process(delta: float) -> void:
	figure.play("walk" if hero.walking else Motion.idle(WEAPON_KIND))
	figure.rotation.y = lerp_angle(
		figure.rotation.y, Motion.yaw_of(hero.dir8), 1.0 - exp(-MapPeople.TURN * delta)
	)


## "Map n / N" and the keys that change it, named for the device in use.
func show_info(_device := "") -> void:
	info.text = InputSetup.hint("viewer.info") % [map_number, map_total]


func _screen_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause"):
		get_viewport().set_input_as_handled()
		Router.back()
	elif event.is_action_pressed("skill_3"):
		show_map(wrapi(map_number - 1, 1, map_total + 1))
	elif event.is_action_pressed("skill_4"):
		show_map(wrapi(map_number + 1, 1, map_total + 1))


## No line of control hints under this screen: it shows its own (scripts/ui/hint_bar.gd).
func controls_hint() -> String:
	return ""
