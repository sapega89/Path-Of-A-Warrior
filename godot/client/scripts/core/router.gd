extends Node
## Screen router: shows one screen at a time inside a host Control and keeps
## a back stack. Screens are listed in SCREENS: a scene (.tscn) whose root is a BaseScreen,
## or, for a screen not moved to a scene yet, its script (.gd).

signal screen_changed(screen_name: String)

const SCREENS := {
	"title": "res://screens/title/title_screen.tscn",
	"main_menu": "res://screens/main_menu/main_menu.tscn",
	"game_menu": "res://screens/game_menu/game_menu.tscn",
	"settings": "res://screens/settings/settings_screen.tscn",
	"controls": "res://screens/controls/controls_screen.tscn",
	"map_viewer": "res://screens/map_viewer/map_viewer_screen.tscn",
	"campaign": "res://screens/campaign/campaign_screen.tscn",
	"camp": "res://screens/camp/camp_screen.tscn",
	"town_hall": "res://screens/town_hall/town_hall_screen.tscn",
	"mission": "res://screens/mission/mission_screen.tscn",
	"briefing": "res://screens/briefing/briefing_screen.tscn",
	"management": "res://screens/management/management_screen.tscn",
	"attributes": "res://screens/attributes/attributes_screen.tscn",
	"skills": "res://screens/skills/skills_screen.tscn",
	"gear": "res://screens/gear/gear_screen.tscn",
	"inventory": "res://screens/inventory/inventory_screen.tscn",
	"assign_items": "res://screens/assign_items/assign_items_screen.tscn",
	"story": "res://screens/story/story_screen.tscn",
	"blacksmith": "res://screens/blacksmith/blacksmith_screen.tscn",
	"shop": "res://screens/shop/shop_screen.tscn",
	"visiting": "res://screens/visiting/visiting_screen.tscn",
	"new_game": "res://screens/new_game/new_game_screen.tscn",
	"endings": "res://screens/endings/endings_screen.tscn",
	"help": "res://screens/help/help_screen.tscn",
	"offline": "res://screens/offline/offline_screen.tscn",
	"login": "res://screens/login/login_screen.tscn",
	"live_warehouse": "res://screens/live_warehouse/live_warehouse_screen.tscn",
	"live_safe": "res://screens/live_safe/live_safe_screen.tscn",
	"live_trade": "res://screens/live_trade/live_trade_screen.tscn",
	"live_buy": "res://screens/live_buy/live_buy_screen.tscn",
	"live_sell": "res://screens/live_sell/live_sell_screen.tscn",
	"live_cancel": "res://screens/live_cancel/live_cancel_screen.tscn",
	"live_gifts": "res://screens/live_gifts/live_gifts_screen.tscn",
	"live_give": "res://screens/live_give/live_give_screen.tscn",
	"online_character": "res://screens/online_character/online_character_screen.tscn",
	"online_skills": "res://screens/online_skills/online_skills_screen.tscn",
	"online_text": "res://screens/online_text/online_text_screen.tscn",
	"online_ranking": "res://screens/online_ranking/online_ranking_screen.tscn",
	"online_order": "res://screens/online_order/online_order_screen.tscn",
	"online_chat": "res://screens/online_chat/online_chat_screen.tscn",
	"online_options": "res://screens/online_options/online_options_screen.tscn",
	"online_battle": "res://screens/online_battle/online_battle_screen.tscn",
	"online_battles": "res://screens/online_battles/online_battles_screen.tscn",
}

var current: Control
## Parameters of the screen being shown (e.g. which mission), read by the screen in _ready.
var params: Dictionary = {}
var _host: Node
var _stack: Array[String] = []
var _params_stack: Array[Dictionary] = []


func attach(host: Node) -> void:
	_host = host
	_stack.clear()
	_params_stack.clear()
	current = null


## Shows a screen and forgets the history (e.g. title -> main menu).
func go(screen_name: String, screen_params: Dictionary = {}) -> bool:
	if not _show(screen_name, screen_params):
		return false
	_stack = [screen_name]
	_params_stack = [screen_params]
	return true


## Shows a screen on top of the current one; back() returns to it.
func push(screen_name: String, screen_params: Dictionary = {}) -> bool:
	if not _show(screen_name, screen_params):
		return false
	_stack.append(screen_name)
	_params_stack.append(screen_params)
	return true


## Shows a screen in place of the current one: back() then goes where the current one would
## have gone (e.g. briefing -> mission, and after the mission back to the campaign).
func replace(screen_name: String, screen_params: Dictionary = {}) -> bool:
	if _stack.is_empty():
		return go(screen_name, screen_params)
	if not _show(screen_name, screen_params):
		return false
	_stack[-1] = screen_name
	_params_stack[-1] = screen_params
	return true


## Returns to the previous screen. False when there is nowhere to go back.
func back() -> bool:
	if _stack.size() < 2:
		return false
	_stack.pop_back()
	_params_stack.pop_back()
	return _show(_stack.back(), _params_stack.back())


func current_name() -> String:
	return "" if _stack.is_empty() else _stack.back()


func depth() -> int:
	return _stack.size()


func _show(screen_name: String, screen_params: Dictionary = {}) -> bool:
	if _host == null or not SCREENS.has(screen_name):
		push_error("router: cannot show %s" % screen_name)
		return false
	params = screen_params
	var screen := make(SCREENS[screen_name])
	screen.name = screen_name
	screen.set_anchors_preset(Control.PRESET_FULL_RECT)
	if current != null:
		_host.remove_child(current)
		current.queue_free()
	current = screen
	_host.add_child(screen)
	screen_changed.emit(screen_name)
	return true


## A new screen from its scene or, for one not moved to a scene yet, its script.
static func make(path: String) -> Control:
	if path.ends_with(".tscn"):
		return (load(path) as PackedScene).instantiate()
	return (load(path) as Script).new()
