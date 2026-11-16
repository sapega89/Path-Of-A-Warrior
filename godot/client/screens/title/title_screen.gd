extends BaseScreen
## Title: the game name and "press any key"; any key, button or tap opens the main menu.

@onready var _prompt: Label = %Prompt


func _ready() -> void:
	var tw := create_tween().set_loops()
	tw.tween_property(_prompt, "modulate:a", 0.3, 0.8)
	tw.tween_property(_prompt, "modulate:a", 1.0, 0.8)


## Any key (back too) starts: it goes to the main menu.
func handles_back() -> bool:
	return false


func _screen_input(event: InputEvent) -> void:
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
