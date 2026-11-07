extends Control
## Game menu, the hero's game (Main menu > Continue, and after the opening of a new game):
## missions, management, blacksmith, the Live pages on the server (trade, warehouse, safe),
## multiplayer and visiting. Back returns to the main menu.
##
## The game is always online: here it starts (Cloud.game_started), and without an account the
## registration opens once, since the hero lives on the server. What Live kept for the player
## while away (notices, sales, gifts, Exp and Fame) is shown over the menu when it opens
## (scripts/ui/live_news.gd). Router.params: profile_path, live and online (tests and
## screenshots) go on to the pages.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Visits := preload("res://scripts/core/visits.gd")
const LiveClient := preload("res://scripts/net/live_client.gd")
const LiveNews := preload("res://scripts/ui/live_news.gd")
## Button name, text key and screen of each page.
const PAGES := [
	["Missions", "menu.missions", "campaign"],
	["Management", "menu.management", "management"],
	["Blacksmith", "menu.blacksmith", "blacksmith"],
	["Trade", "live.trade", "live_trade"],
	["Warehouse", "live.warehouse", "live_warehouse"],
	["Safe", "live.safe", "live_safe"],
	["Multiplayer", "menu.multiplayer", "online"],
	["Visiting", "menu.visiting", "visiting"],
]

var path: String = Profile.PATH
var menu: VBoxContainer
var buttons: Array[Button] = []
var news: Control  # what Live kept for the player; null when the game is not online


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	menu = UiTheme.menu_column(self)
	menu.add_child(UiTheme.heading("menu.game", 44))
	for page in PAGES:
		var b := Button.new()
		b.name = page[0]
		b.text = page[1]
		var screen: String = page[2]
		b.pressed.connect(func(): Router.push(screen, Router.params))
		menu.add_child(b)
		buttons.append(b)
	if not Visits.can_visit(Profile.load_or_new(path)):
		buttons[-1].modulate = Color(1, 1, 1, 0.5)  # greyed: it only says when one can visit
	buttons[0].grab_focus.call_deferred()
	if Cloud.enabled():
		Cloud.game_started()
		if not Cloud.has_account():
			Router.push.call_deferred("register")
			return
	_show_news()


func _show_news() -> void:
	var live := LiveClient.of(Router.params)
	if live == null:
		return
	news = LiveNews.new(live, path)
	news.showing_list.connect(func(on: bool) -> void:
		menu.visible = not on
		if not on:
			buttons[0].grab_focus.call_deferred())
	add_child(news)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		if not Router.back():
			Router.go("main_menu")
