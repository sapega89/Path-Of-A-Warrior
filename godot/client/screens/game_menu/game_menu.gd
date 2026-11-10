class_name GameMenu
extends BaseScreen
## Game menu, the hero's game (opened from the camp's pause menu), one column: the campaign
## (management, blacksmith, visiting), the Live pages on the server (trade, safe), multiplayer
## (scripts/ui/online_section.gd) and the help of the whole game, a small gap between the
## groups; it scrolls with the focus. The missions start from the ways out of the camp and the
## warehouse is the camp's stores, so neither is here. Back returns to the camp (to the main
## menu when there is nothing to go back to).
##
## The game is always online: here it starts (Cloud.game_started), and without an account the
## login opens (the main menu asks for it before, so only when the account was dropped), since
## the hero lives on the server. What Live kept for the player
## while away (notices, sales, gifts, Exp and Fame) is shown over the menu when it opens
## (scripts/ui/live_news.gd). The hero is in the online game (others can challenge him) only
## while this menu or a multiplayer page is open. Router.params: profile_path, live and online
## (tests and screenshots) go on to the pages.

var path: String = Profile.PATH
@onready var menu: VBoxContainer = %Column
@onready var list: VBoxContainer = %List
var buttons: Array[Button] = []  # the single-player pages and Help
var online: VBoxContainer  # the multiplayer pages
var news: Control  # what Live kept for the player; null when the game is not online


func _ready() -> void:
	path = profile_path()
	for b in list.get_children():
		if b is Button:
			buttons.append(b)
	online = OnlineSection.new(Router.params)
	list.get_node("Gap2").add_sibling(online)  # the multiplayer pages, between the groups
	if not Visits.can_visit(Profile.load_or_new(path)):
		list.get_node("Visiting").modulate = Color(1, 1, 1, 0.5)  # only says when one can visit
	buttons[0].grab_focus.call_deferred()
	if Cloud.enabled():
		Cloud.game_started()
		if not Cloud.has_account():
			Router.push.call_deferred("login", {"must": true})
			return
	_show_news()


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


## Back leaves the multiplayer pages and goes where the menu was opened from.
func go_back() -> void:
	online.leave()
	if not Router.back():
		Router.go("main_menu")
