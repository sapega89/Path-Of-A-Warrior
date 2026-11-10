class_name MapView
extends PixelView
## A map's 3D world on the screen: its own world in a viewport, the light and air of the new
## art (MapArt.add_environment), the map in the new art and the camera. The screens add the
## people to `world` and build the map with `map.build()`.

@onready var world: Node3D = $Viewport/WorldRoot
@onready var map: MapArt = $Viewport/WorldRoot/Map
@onready var camera: FollowCamera = $Viewport/WorldRoot/Camera


func _ready() -> void:
	super()
	MapArt.add_environment(world)
	camera.make_current()
