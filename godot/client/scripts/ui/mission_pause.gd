extends Control
## The pause menu of a mission, over the stopped game, in pyport's order: Resume, Items (Assign
## Items for this mission's potion keys), Save (once the room is cleared; Continue comes back
## to it), Options (the settings), Help, Exit to Menu (asked
## first: the mission is lost, back to the campaign) and Exit Game (asked first; not on phones
## and the web). Items, Options and Help show over the menu. Back resumes.

signal resumed

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const MainMenu := preload("res://scripts/screens/main_menu.gd")
const SettingsScreen := preload("res://scripts/screens/settings_screen.gd")
const HelpScreen := preload("res://scripts/screens/help_screen.gd")
const AssignItems := preload("res://scripts/screens/assign_items_screen.gd")

var buttons: Array[Button] = []
var menu: Control
var settings: Control  # the items, the settings or the help shown over the menu
var sim: RefCounted  # the mission's (its potion keys)
var save_game := Callable()  # the mission's save on its map: true when saved
var note: AcceptDialog
var ask: ConfirmationDialog
var asked := ""  # "exit" or "quit"


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
	_add(col, "Items", "pause.items", open_items)
	_add(col, "Save", "pause.save", save)
	_add(col, "Options", "pause.options", open_options)
	_add(col, "Help", "pause.help", open_help)
	_add(col, "Exit", "pause.exit", func(): _ask("exit"))
	if MainMenu.show_quit():
		_add(col, "Quit", "pause.quit", func(): _ask("quit"))
	note = AcceptDialog.new()
	note.name = "Note"
	add_child(note)
	ask = ConfirmationDialog.new()
	ask.name = "Ask"
	ask.confirmed.connect(confirmed)
	add_child(ask)
	buttons[0].grab_focus.call_deferred()


## "Exit Game and go to main menu?" / "Exit Game?", No first.
func _ask(what: String) -> void:
	asked = what
	ask.dialog_text = tr("pause.ask_" + what)
	ask.popup_centered()
	ask.get_cancel_button().grab_focus.call_deferred()


func confirmed() -> void:
	if asked == "exit":
		Router.back()
	elif asked == "quit":
		get_tree().quit()


## Saves the mission on its map and says how it went ("Saving Success!" or "Can't Save!").
func save() -> bool:
	var ok: bool = save_game.is_valid() and save_game.call()
	note.dialog_text = tr("pause.saved" if ok else "pause.cannot_save")
	note.popup_centered()
	return ok


## Assign Items over the pause menu, for this mission's potion keys.
func open_items() -> void:
	var screen: Control = AssignItems.new()
	screen.sim = sim
	_open_over(screen, "Items")


func _add(col: VBoxContainer, node_name: String, text_key: String, on_press: Callable) -> void:
	var b := Button.new()
	b.name = node_name
	b.text = text_key
	b.pressed.connect(on_press)
	col.add_child(b)
	buttons.append(b)


## The settings over the pause menu; their Back comes back here.
func open_options() -> void:
	_open_over(SettingsScreen.new(), "Settings")


## The help over the pause menu; leaving it comes back here.
func open_help() -> void:
	_open_over(HelpScreen.new(), "Help")


func _open_over(screen: Control, node_name: String) -> void:
	menu.visible = false
	settings = screen
	settings.name = node_name
	settings.set_anchors_preset(Control.PRESET_FULL_RECT)
	settings.close = close_options
	add_child(settings)


func close_options() -> void:
	var was := "" if settings == null else str(settings.name)
	if settings != null:
		settings.queue_free()
		settings = null
	menu.visible = true
	for b in buttons:
		if str(b.name) == ("Options" if was == "Settings" else was):
			b.grab_focus.call_deferred()


func _unhandled_input(event: InputEvent) -> void:
	if settings == null and (event.is_action_pressed("ui_cancel") or event.is_action_pressed("pause")):
		get_viewport().set_input_as_handled()
		resumed.emit()
