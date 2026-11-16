extends Control
## Root of the game: applies the UI theme and hands the screen area to the Router. Its scene
## lays the menus' backdrop (assets/art/shaders/ui_backdrop.gdshader), the screen area and the
## line of control hints under it (scenes/ui/hint_bar.tscn).

@onready var screens: Control = %Screens
@onready var hints: HintBar = %HintBar


func _ready() -> void:
	theme = UiTheme.theme(UiTheme.THEME)
	hints.host = screens
	Router.attach(screens)
	Router.go("title")
