extends Node
## Screen router: shows one screen at a time inside a host Control and keeps
## a back stack. Screens are Control scripts listed in SCREENS.

signal screen_changed(screen_name: String)

const SCREENS := {
	"title": "res://scripts/screens/title_screen.gd",
	"main_menu": "res://scripts/screens/main_menu.gd",
	"settings": "res://scripts/screens/settings_screen.gd",
	"map_viewer": "res://scripts/screens/map_viewer.gd",
}

var current: Control
var _host: Node
var _stack: Array[String] = []


func attach(host: Node) -> void:
	_host = host
	_stack.clear()
	current = null


## Shows a screen and forgets the history (e.g. title -> main menu).
func go(screen_name: String) -> bool:
	if not _show(screen_name):
		return false
	_stack = [screen_name]
	return true


## Shows a screen on top of the current one; back() returns to it.
func push(screen_name: String) -> bool:
	if not _show(screen_name):
		return false
	_stack.append(screen_name)
	return true


## Returns to the previous screen. False when there is nowhere to go back.
func back() -> bool:
	if _stack.size() < 2:
		return false
	_stack.pop_back()
	return _show(_stack.back())


func current_name() -> String:
	return "" if _stack.is_empty() else _stack.back()


func depth() -> int:
	return _stack.size()


func _show(screen_name: String) -> bool:
	if _host == null or not SCREENS.has(screen_name):
		push_error("router: cannot show %s" % screen_name)
		return false
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
