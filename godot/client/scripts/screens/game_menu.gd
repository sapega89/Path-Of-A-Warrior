class_name GameMenu
extends Control
## Game menu, the hero's game (Main menu > Continue, and after the opening of a new game), one
## column: the campaign (missions, management, blacksmith, visiting), the Live pages on the
## server (trade, warehouse, safe), multiplayer (scripts/ui/online_section.gd) and the help of
## the whole game, a small gap between the groups; it scrolls with the focus. Back returns to
## the main menu.
##
## The game is always online: here it starts (Cloud.game_started), and without an account the
## login opens (the main menu asks for it before, so only when the account was dropped), since
## the hero lives on the server. What Live kept for the player
## while away (notices, sales, gifts, Exp and Fame) is shown over the menu when it opens
## (scripts/ui/live_news.gd). The hero is in the online game (others can challenge him) only
## while this menu or a multiplayer page is open. Router.params: profile_path, live and online
## (tests and screenshots) go on to the pages.

const WIDTH := 460
const LIST_HEIGHT := 600
const GAP := 14
## The pages of each single-player group: button name, text key, screen.
const CAMPAIGN := [
	["Missions", "menu.missions", "campaign"],
	["Management", "menu.management", "management"],
	["Blacksmith", "menu.blacksmith", "blacksmith"],
	["Visiting", "menu.visiting", "visiting"],
]
const LIVE := [
	["Trade", "live.trade", "live_trade"],
	["Warehouse", "live.warehouse", "live_warehouse"],
	["Safe", "live.safe", "live_safe"],
]

var path: String = Profile.PATH
var menu: VBoxContainer
var list: VBoxContainer
var buttons: Array[Button] = []  # the single-player pages and Help
var online: VBoxContainer  # the multiplayer pages
var news: Control  # what Live kept for the player; null when the game is not online


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	menu = UiTheme.menu_column(self, WIDTH)
	menu.theme = UiTheme.compact()
	menu.add_child(UiTheme.heading("menu.game", 44))
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size = Vector2(WIDTH, LIST_HEIGHT)
	scroll.follow_focus = true
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	menu.add_child(scroll)
	list = VBoxContainer.new()
	list.name = "List"
	list.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	list.add_theme_constant_override("separation", 6)
	scroll.add_child(list)
	for group in [CAMPAIGN, LIVE]:
		for page in group:
			_add(page[0], page[1], page[2])
		_gap()
	online = OnlineSection.new(Router.params)
	list.add_child(online)
	_gap()
	_add("Help", "menu.help", "help")  # of the whole game
	if not Visits.can_visit(Profile.load_or_new(path)):
		list.get_node("Visiting").modulate = Color(1, 1, 1, 0.5)  # only says when one can visit
	buttons[0].grab_focus.call_deferred()
	if Cloud.enabled():
		Cloud.game_started()
		if not Cloud.has_account():
			Router.push.call_deferred("login", {"must": true})
			return
	_show_news()


func _add(node_name: String, text_key: String, screen: String) -> void:
	var b := Button.new()
	b.name = node_name
	b.text = text_key
	b.pressed.connect(_open.bind(screen))
	list.add_child(b)
	buttons.append(b)


func _gap() -> void:
	var gap := Control.new()
	gap.custom_minimum_size = Vector2(0, GAP)
	list.add_child(gap)


## A page of the hero's own game: off the online game first.
func _open(screen: String) -> void:
	online.leave()
	Router.push(screen, Router.params)


func _show_news() -> void:
	var live := LiveClient.of(Router.params)
	if live == null:
		return
	news = LiveNews.new(live, path)
	news.showing_list.connect(
		func(on: bool) -> void:
			menu.visible = not on
			if not on:
				buttons[0].grab_focus.call_deferred()
	)
	add_child(news)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		online.leave()
		if not Router.back():
			Router.go("main_menu")
