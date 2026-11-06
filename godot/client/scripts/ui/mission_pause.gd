extends Control
## The pause menu of a mission, over the stopped game: Resume, Options (the settings, shown
## over it), Exit to Menu (the mission is lost, back to the campaign) and Exit Game (not on
## phones and the web). Back resumes.

signal resumed

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const MainMenu := preload("res://scripts/screens/main_menu.gd")
const SettingsScreen := preload("res://scripts/screens/settings_screen.gd")

var buttons: Array[Button] = []
var menu: Control
var settings: Control


func _ready() -> void:
	top_level = true  # the whole window, over the HUD and the touch controls
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.6)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(dim)
	menu = Control.new()
	menu.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(menu)
	var col := UiTheme.menu_column(menu)
	col.add_child(UiTheme.heading("pause.title", 44))
	_add(col, "Resume", "pause.resume", func(): resumed.emit())
	_add(col, "Options", "pause.options", open_options)
	_add(col, "Exit", "pause.exit", func(): Router.back())
	if MainMenu.show_quit():
		_add(col, "Quit", "pause.quit", func(): get_tree().quit())
	buttons[0].grab_focus.call_deferred()


func _add(col: VBoxContainer, node_name: String, text_key: String, on_press: Callable) -> void:
	var b := Button.new()
	b.name = node_name
	b.text = text_key
	b.pressed.connect(on_press)
	col.add_child(b)
	buttons.append(b)


## The settings over the pause menu; their Back comes back here.
func open_options() -> void:
	menu.visible = false
	settings = SettingsScreen.new()
	settings.name = "Settings"
	settings.set_anchors_preset(Control.PRESET_FULL_RECT)
	settings.close = close_options
	add_child(settings)


func close_options() -> void:
	if settings != null:
		settings.queue_free()
		settings = null
	menu.visible = true
	buttons[1].grab_focus.call_deferred()


func _unhandled_input(event: InputEvent) -> void:
	if settings == null and (event.is_action_pressed("ui_cancel") or event.is_action_pressed("pause")):
		get_viewport().set_input_as_handled()
		resumed.emit()
