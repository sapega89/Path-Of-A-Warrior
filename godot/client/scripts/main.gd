extends Control
## Root of the game: applies the UI theme, lays the menus' backdrop and hands the screen area
## to the Router.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")


func _ready() -> void:
	theme = UiTheme.build()
	add_child(UiTheme.backdrop())
	var host := Control.new()
	host.name = "Screens"
	host.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(host)
	Router.attach(host)
	Router.go("title")
