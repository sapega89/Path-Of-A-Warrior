extends Control
## Main menu: play, settings, quit (no quit button on phones and the web).

const UiTheme := preload("res://scripts/ui/ui_theme.gd")

var buttons: Array[Button] = []


func _ready() -> void:
	var col := UiTheme.menu_column(self)
	col.add_child(UiTheme.heading("game.title", 44))
	_add(col, "Play", "menu.play", func(): Router.push("map_viewer"))
	_add(col, "Settings", "menu.settings", func(): Router.push("settings"))
	if show_quit():
		_add(col, "Quit", "menu.quit", func(): get_tree().quit())
	buttons[0].grab_focus.call_deferred()


static func show_quit() -> bool:
	return not (OS.has_feature("mobile") or OS.has_feature("web"))


func _add(col: VBoxContainer, node_name: String, text_key: String, on_press: Callable) -> void:
	var b := Button.new()
	b.name = node_name
	b.text = text_key
	b.pressed.connect(on_press)
	col.add_child(b)
	buttons.append(b)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.go("title")
