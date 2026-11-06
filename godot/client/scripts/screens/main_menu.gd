extends Control
## Main menu: continue (or play), new game, blacksmith, management, visiting, endings, maps, settings, help, quit (no quit button on phones and the web).

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Visits := preload("res://scripts/core/visits.gd")

var buttons: Array[Button] = []
var ask: ConfirmationDialog  # "Starting a new game will cause your saved game to be deleted."


func _ready() -> void:
	var col := UiTheme.menu_column(self)
	col.add_child(UiTheme.heading("game.title", 44))
	var saved := FileAccess.file_exists(Profile.PATH)
	_add(col, "Play", "menu.continue" if saved else "menu.play", play)
	_add(col, "NewGame", "menu.new_game", new_game)
	_add(col, "Blacksmith", "menu.blacksmith", func(): Router.push("blacksmith"))
	_add(col, "Management", "menu.management", func(): Router.push("management"))
	_add(col, "Visiting", "menu.visiting", func(): Router.push("visiting"))
	if not Visits.can_visit(Profile.load_or_new()):
		buttons[-1].modulate = Color(1, 1, 1, 0.5)  # greyed: it only says when one can visit
	_add(col, "Endings", "menu.endings", func(): Router.push("endings", {}))
	_add(col, "Maps", "menu.maps", func(): Router.push("map_viewer"))
	_add(col, "Settings", "menu.settings", func(): Router.push("settings"))
	_add(col, "Help", "menu.help", func(): Router.push("help"))
	if show_quit():
		_add(col, "Quit", "menu.quit", func(): get_tree().quit())
	ask = ConfirmationDialog.new()
	ask.name = "Ask"
	ask.dialog_text = tr("newgame.ask_delete")
	ask.confirmed.connect(func(): Router.push("new_game", {}))
	add_child(ask)
	buttons[0].grab_focus.call_deferred()


## The saved hero goes on with the campaign; without one a new game starts.
func play() -> void:
	if FileAccess.file_exists(Profile.PATH):
		Router.push("campaign")
		return
	Router.push("new_game", {})


## A new hero (difficulty, face, name, points); over a saved one only when that is confirmed.
func new_game() -> void:
	if FileAccess.file_exists(Profile.PATH):
		ask.popup_centered()
		return
	Router.push("new_game", {})


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
