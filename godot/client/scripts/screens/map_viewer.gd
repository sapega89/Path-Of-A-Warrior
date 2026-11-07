extends Control
## Walks the hero around the original maps in 3D. skill_3 / skill_4 (keys 3 / 4,
## gamepad LB / RB) switch to the previous / next map; the line at the top names the keys of
## the device in use. Grows into the real map
## screen when the map logic (rooms, exits, enemies) is ported.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const MapBuilder := preload("res://scripts/world/map_builder.gd")
const Hero := preload("res://scripts/world/hero.gd")
const FollowCamera := preload("res://scripts/world/follow_camera.gd")
const TouchControls := preload("res://scripts/ui/touch_controls.gd")

var viewport: SubViewport
var world: Node3D
var builder: Node3D
var hero: CharacterBody3D
var camera: Camera3D
var touch: Control
var info: Label
var map_number := 1
var map_total := 0


func _ready() -> void:
	var container := SubViewportContainer.new()
	container.name = "World"
	container.stretch = true
	container.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(container)
	viewport = SubViewport.new()
	viewport.own_world_3d = true
	viewport.msaa_3d = Viewport.MSAA_2X
	container.add_child(viewport)

	world = Node3D.new()
	world.name = "WorldRoot"
	viewport.add_child(world)
	MapBuilder.add_environment(world)
	builder = MapBuilder.new()
	builder.name = "Map"
	world.add_child(builder)
	hero = Hero.new()
	hero.name = "Hero"
	world.add_child(hero)
	camera = FollowCamera.new()
	camera.name = "Camera"
	camera.target = hero
	world.add_child(camera)
	camera.make_current()

	info = Label.new()
	info.name = "Info"
	info.position = Vector2(24, 16)
	info.add_theme_font_size_override("font_size", 20)
	add_child(info)
	InputSetup.device_changed.connect(show_info)

	touch = TouchControls.new()
	touch.name = "Touch"
	add_child(touch)

	map_total = MapBuilder.map_count()
	show_map(1)


func show_map(number: int) -> bool:
	var data := MapBuilder.load_map(number)
	if data.is_empty():
		return false
	map_number = number
	builder.build(data)
	hero.global_position = MapBuilder.cell_to_world(builder.start_cell(0)) + Vector3(0, 0.05, 0)
	hero.velocity = Vector3.ZERO
	camera.snap()
	show_info()
	return true


## "Map n / N" and the keys that change it, named for the device in use.
func show_info(_device := "") -> void:
	info.text = InputSetup.hint("viewer.info") % [map_number, map_total]


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause") or event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
	elif event.is_action_pressed("skill_3"):
		show_map(wrapi(map_number - 1, 1, map_total + 1))
	elif event.is_action_pressed("skill_4"):
		show_map(wrapi(map_number + 1, 1, map_total + 1))


## No line of control hints under this screen: it shows its own (scripts/ui/hint_bar.gd).
func controls_hint() -> String:
	return ""
