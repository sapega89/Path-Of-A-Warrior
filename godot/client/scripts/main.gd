extends Control
## Root of the game: applies the UI theme and hands the screen area to the Router.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")


func _ready() -> void:
	theme = UiTheme.build()
	var bg := ColorRect.new()
	bg.color = UiTheme.BG
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(bg)
	var host := Control.new()
	host.name = "Screens"
	host.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(host)
	Router.attach(host)
	Router.go("title")
