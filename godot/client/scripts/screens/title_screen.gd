extends Control
## Title: the game name and "press any key"; any key, button or tap opens the main menu.

var _prompt: Label


func _ready() -> void:
	var col := UiTheme.menu_column(self, 800)
	col.add_child(UiTheme.heading("game.title", 72))
	var spacer := Control.new()
	spacer.custom_minimum_size = Vector2(0, 80)
	spacer.mouse_filter = Control.MOUSE_FILTER_IGNORE  # a click there reaches the screen too
	col.add_child(spacer)
	_prompt = Label.new()
	_prompt.name = "Prompt"
	_prompt.text = "title.press_any"
	_prompt.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_prompt.add_theme_color_override("font_color", UiTheme.TEXT_DIM)
	col.add_child(_prompt)
	var tw := create_tween().set_loops()
	tw.tween_property(_prompt, "modulate:a", 0.3, 0.8)
	tw.tween_property(_prompt, "modulate:a", 1.0, 0.8)


func _unhandled_input(event: InputEvent) -> void:
	if is_start_event(event):
		get_viewport().set_input_as_handled()
		Router.go("main_menu")


## A click or a tap anywhere: in a window the screen itself takes it (it never reaches
## _unhandled_input).
func _gui_input(event: InputEvent) -> void:
	if is_start_event(event):
		accept_event()
		Router.go("main_menu")


static func is_start_event(event: InputEvent) -> bool:
	if (
		event is InputEventKey
		or event is InputEventJoypadButton
		or event is InputEventMouseButton
		or event is InputEventScreenTouch
	):
		return event.is_pressed() and not event.is_echo()
	return false


## No line of control hints under this screen: it shows its own (scripts/ui/hint_bar.gd).
func controls_hint() -> String:
	return ""
