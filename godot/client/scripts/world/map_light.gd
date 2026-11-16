class_name MapLight
extends Node3D
## The light and air of a map in the new art (scenes/world/map_light.tscn): a dull sun from the
## upper left with soft shadows, a deep cool shade (ArtKit.light), and the land fading into grey
## dust far away. Each instance has its own Environment, so a screen can change its air.

const SCENE := "res://scenes/world/map_light.tscn"

@onready var sun: DirectionalLight3D = $Sun
@onready var air: WorldEnvironment = $WorldEnvironment


func _ready() -> void:
	ArtKit.light(sun, air.environment)
	air.environment.background_color = ArtKit.AIR
	air.environment.fog_light_color = ArtKit.AIR
