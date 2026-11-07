extends Control
## Game menu, the hero's game (Main menu > Continue, and after the opening of a new game), in
## three columns: the campaign (missions, management, blacksmith, visiting, and the help of the
## whole game), the Live pages on the server (trade, warehouse, safe) and multiplayer
## (scripts/ui/online_section.gd). Back returns to the main menu.
##
## The game is always online: here it starts (Cloud.game_started), and without an account the
## registration opens once, since the hero lives on the server. What Live kept for the player
## while away (notices, sales, gifts, Exp and Fame) is shown over the menu when it opens
## (scripts/ui/live_news.gd). The hero is in the online game (others can challenge him) only
## while this menu or a multiplayer page is open. Router.params: profile_path, live and online
## (tests and screenshots) go on to the pages.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Visits := preload("res://scripts/core/visits.gd")
const LiveClient := preload("res://scripts/net/live_client.gd")
const LiveNews := preload("res://scripts/ui/live_news.gd")
const OnlineSection := preload("res://scripts/ui/online_section.gd")
const COLUMN_WIDTH := 360
## Each single-player column: its name, its heading, then its pages (button name, text key,
## screen).
const COLUMNS := [
	["Campaign", "menu.campaign", [
		["Missions", "menu.missions", "campaign"],
		["Management", "menu.management", "management"],
		["Blacksmith", "menu.blacksmith", "blacksmith"],
		["Visiting", "menu.visiting", "visiting"],
		["Help", "menu.help", "help"],  # of the whole game
	]],
	["Live", "menu.live", [
		["Trade", "live.trade", "live_trade"],
		["Warehouse", "live.warehouse", "live_warehouse"],
		["Safe", "live.safe", "live_safe"],
	]],
]

var path: String = Profile.PATH
var menu: VBoxContainer
var buttons: Array[Button] = []  # the single-player pages
var online: VBoxContainer  # the multiplayer column
var news: Control  # what Live kept for the player; null when the game is not online


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	menu = UiTheme.menu_column(self, COLUMN_WIDTH * 3)
	menu.theme = UiTheme.compact()
	menu.add_child(UiTheme.heading("menu.game", 44))
	var columns := HBoxContainer.new()
	columns.name = "Columns"
	columns.add_theme_constant_override("separation", 32)
	menu.add_child(columns)
	for c in COLUMNS:
		columns.add_child(_column(c[0], c[1], c[2]))
	online = OnlineSection.new(Router.params)
	online.custom_minimum_size = Vector2(COLUMN_WIDTH, 0)
	columns.add_child(online)
	if not Visits.can_visit(Profile.load_or_new(path)):
		menu.get_node("Columns/Campaign/Visiting").modulate = Color(1, 1, 1, 0.5)  # only says when one can visit
	buttons[0].grab_focus.call_deferred()
	if Cloud.enabled():
		Cloud.game_started()
		if not Cloud.has_account():
			Router.push.call_deferred("register")
			return
	_show_news()


func _column(node_name: String, heading_key: String, pages: Array) -> VBoxContainer:
	var col := VBoxContainer.new()
	col.name = node_name
	col.custom_minimum_size = Vector2(COLUMN_WIDTH, 0)
	col.add_theme_constant_override("separation", 6)
	col.add_child(UiTheme.heading(heading_key, 32))
	for page in pages:
		var b := Button.new()
		b.name = page[0]
		b.text = page[1]
		b.pressed.connect(_open.bind(str(page[2])))
		col.add_child(b)
		buttons.append(b)
	return col


## A page of the hero's own game: off the online game first.
func _open(screen: String) -> void:
	online.leave()
	Router.push(screen, Router.params)


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
		online.leave()
		if not Router.back():
			Router.go("main_menu")
