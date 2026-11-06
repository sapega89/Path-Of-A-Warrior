extends Node
## Screen router: shows one screen at a time inside a host Control and keeps
## a back stack. Screens are Control scripts listed in SCREENS.

signal screen_changed(screen_name: String)

const SCREENS := {
	"title": "res://scripts/screens/title_screen.gd",
	"main_menu": "res://scripts/screens/main_menu.gd",
	"settings": "res://scripts/screens/settings_screen.gd",
	"map_viewer": "res://scripts/screens/map_viewer.gd",
	"campaign": "res://scripts/screens/campaign_screen.gd",
	"mission": "res://scripts/screens/mission_screen.gd",
	"management": "res://scripts/screens/management_screen.gd",
	"attributes": "res://scripts/screens/attributes_screen.gd",
	"skills": "res://scripts/screens/skills_screen.gd",
	"gear": "res://scripts/screens/gear_screen.gd",
	"inventory": "res://scripts/screens/inventory_screen.gd",
	"assign_items": "res://scripts/screens/assign_items_screen.gd",
	"story": "res://scripts/screens/story_screen.gd",
	"blacksmith": "res://scripts/screens/blacksmith_screen.gd",
	"shop": "res://scripts/screens/shop_screen.gd",
	"visiting": "res://scripts/screens/visiting_screen.gd",
	"new_game": "res://scripts/screens/new_game_screen.gd",
	"endings": "res://scripts/screens/endings_screen.gd",
	"help": "res://scripts/screens/help_screen.gd",
	"offline": "res://scripts/screens/offline_screen.gd",
	"register": "res://scripts/screens/register_screen.gd",
	"live": "res://scripts/screens/live_screen.gd",
	"live_warehouse": "res://scripts/screens/live_warehouse_screen.gd",
	"live_safe": "res://scripts/screens/live_safe_screen.gd",
	"live_trade": "res://scripts/screens/live_trade_screen.gd",
	"live_buy": "res://scripts/screens/live_buy_screen.gd",
	"live_sell": "res://scripts/screens/live_sell_screen.gd",
	"live_cancel": "res://scripts/screens/live_cancel_screen.gd",
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
	var script: Script = load(SCREENS[screen_name])
	var screen: Control = script.new()
	screen.name = screen_name
	screen.set_anchors_preset(Control.PRESET_FULL_RECT)
	if current != null:
		_host.remove_child(current)
		current.queue_free()
	current = screen
	_host.add_child(screen)
	screen_changed.emit(screen_name)
	return true
