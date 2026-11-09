class_name MainMenu
extends BaseScreen
## Main menu: continue (or play), new game, endings, settings, quit (no quit button on phones
## and the web). Continue opens the hero's camp (scripts/screens/camp_screen.gd), where his
## game goes on; a new game starts its first mission at once after the opening. While the game is
## always online and this run has no account yet, Play
## and New game open the login (scripts/screens/login_screen.gd) first; it comes back here and
## goes on with play() or new_game() once the hero (or none) has come from the server.

var buttons: Array[Button] = []
var ask: AskDialog  # "Starting a new game will cause your saved game to be deleted.", No first


func _ready() -> void:
	if Cloud.enabled() and not Cloud.online():
		Router.go.call_deferred("offline")  # the game starts only online
	var col := UiTheme.menu_column(self)
	col.add_child(UiTheme.heading("game.title", 44))
	var saved := Profile.exists()
	_add(col, "Play", "menu.continue" if saved else "menu.play", play)
	_add(col, "NewGame", "menu.new_game", new_game)
	_add(col, "Endings", "menu.endings", func(): Router.push("endings", {}))
	_add(col, "Settings", "menu.settings", func(): Router.push("settings"))
	if show_quit():
		_add(col, "Quit", "menu.quit", func(): Cloud.quit_game())
	ask = AskDialog.new()
	ask.safe_default = true
	ask.dialog_text = tr("newgame.ask_delete")
	ask.confirmed.connect(func(): Router.push("new_game", {}))
	add_child(ask)
	_focus_first.call_deferred()


## The first button takes the focus, unless the login sent this menu on at once.
func _focus_first() -> void:
	if is_inside_tree():
		buttons[0].grab_focus()


## The saved hero goes on in his camp (back into the mission saved on its map, if any);
## without one a new game starts.
func play() -> void:
	if needs_login():
		Router.push("login", {"next": "play"})
		return
	if not Profile.exists():
		Router.push("new_game", {})
		return
	Router.push("camp")
	var on_map: Dictionary = Profile.load_or_new().on_map
	if not on_map.is_empty():
		Router.push(
			"mission",
			{
				"lord": int(on_map.get("lord", 1)),
				"mission": int(on_map.get("mission", 0)),
				"resume": true
			}
		)


## A new hero (difficulty, face, name, points); over a saved one only when that is confirmed.
func new_game() -> void:
	if needs_login():
		Router.push("login", {"next": "new_game"})
		return
	if Profile.exists():
		ask.popup_centered()
		return
	Router.push("new_game", {})


## The hero is on the server and nobody has logged in since the game started.
static func needs_login() -> bool:
	return Cloud.enabled() and not Cloud.has_account()


static func show_quit() -> bool:
	return not (OS.has_feature("mobile") or OS.has_feature("web"))


func _add(col: VBoxContainer, node_name: String, text_key: String, on_press: Callable) -> void:
	var b := Button.new()
	b.name = node_name
	b.text = text_key
	b.pressed.connect(on_press)
	col.add_child(b)
	buttons.append(b)


func go_back() -> void:
	Router.go("title")
