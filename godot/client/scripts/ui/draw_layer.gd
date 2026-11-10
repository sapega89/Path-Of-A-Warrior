class_name DrawLayer
extends Control
## A layer drawn by its screen: each time it draws, `drawing` asks the screen to draw on it
## (the screen connects it to its draw_<what>(layer)).

signal drawing(layer: Control)


func _draw() -> void:
	drawing.emit(self)
