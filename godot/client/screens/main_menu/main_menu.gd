class_name MainMenu
extends BaseScreen
## Main menu: continue (or play), new game, endings, settings, quit (no quit button on phones
## and the web). Continue opens the hero's camp (screens/camp/camp_screen.gd), where his
## game goes on; a new game starts its first mission at once after the opening. The hero is
## saved on this computer (Profile.PATH).

var buttons: Array[Button] = []
var ask: AskDialog  # "Starting a new game will cause your saved game to be deleted.", No first


func _ready() -> void:
	var col: VBoxContainer = %Column
	if Profile.exists():
		col.get_node("Play").text = "menu.continue"
	if not show_quit():
		col.get_node("Quit").free()
	for b in col.get_children():
		if b is Button:
			buttons.append(b)
	ask = AskDialog.new()
	ask.safe_default = true
	ask.dialog_text = tr("newgame.ask_delete")
	ask.confirmed.connect(func(): Router.push("new_game", {}))
	add_child(ask)
	_focus_first.call_deferred()


## The first button takes the focus once the menu is shown.
func _focus_first() -> void:
	if is_inside_tree():
		buttons[0].grab_focus()


## The saved hero goes on in his camp (back into the mission saved on its map, if any);
## without one a new game starts.
func play() -> void:
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


func open_endings() -> void:
	Router.push("endings", {})


func open_settings() -> void:
	Router.push("settings")


func quit() -> void:
	get_tree().quit()


## A new hero (difficulty, face, name, points); over a saved one only when that is confirmed.
func new_game() -> void:
	if Profile.exists():
		ask.popup_centered()
		return
	Router.push("new_game", {})


static func show_quit() -> bool:
	return not (OS.has_feature("mobile") or OS.has_feature("web"))


func go_back() -> void:
	Router.go("title")
