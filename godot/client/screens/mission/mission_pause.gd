class_name MissionPause
extends Control
## The pause menu of a mission, over the stopped game (mission_pause.tscn): Resume, Items
## (Assign Items for this mission's potion keys), Options (the settings), Help, Exit to Menu
## (asked first: the mission is lost, back to the camp) and Exit Game (asked first; not on phones
## and the web). The game is saved in the camps between missions, so there is no Save here
## (save() is kept for a mission saved on its map by an older version). Items, Options and Help
## show over the menu. Back resumes.

signal resumed

const SCENE := "res://screens/mission/mission_pause.tscn"

var buttons: Array[Button] = []
var settings: Control  # the items, the settings or the help shown over the menu
var sim: MapSim  # the mission's (its potion keys)
var save_game := Callable()  # the mission's save on its map: true when saved
var asked := ""  # "exit" or "quit"

@onready var menu: Control = %Menu
@onready var note: AskDialog = %Note  # a notice: OK alone
@onready var ask: AskDialog = %Ask


func _ready() -> void:
	if not MainMenu.show_quit():
		%Column.get_node("Quit").free()
	for b in %Column.get_children():
		if b is Button:
			buttons.append(b)
	buttons[0].grab_focus.call_deferred()


func _unhandled_input(event: InputEvent) -> void:
	if (
		settings == null
		and (event.is_action_pressed("ui_cancel") or event.is_action_pressed("pause"))
	):
		get_viewport().set_input_as_handled()
		resumed.emit()


func resume() -> void:
	resumed.emit()


## "Exit Game and go to main menu?" / "Exit Game?", No first.
func _ask(what: String) -> void:
	asked = what
	ask.dialog_text = tr("pause.ask_" + what)
	ask.popup_centered()


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
	var screen: Control = Router.make(Router.SCREENS["assign_items"])
	screen.sim = sim
	_open_over(screen, "Items")


## The settings over the pause menu; their Back comes back here.
func open_options() -> void:
	_open_over(Router.make(Router.SCREENS["settings"]), "Settings")


## The help over the pause menu; leaving it comes back here.
func open_help() -> void:
	_open_over(Router.make(Router.SCREENS["help"]), "Help")


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
