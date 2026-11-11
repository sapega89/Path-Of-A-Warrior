class_name GameMenu
extends BaseScreen
## Game menu, the hero's game (opened from the camp's pause menu), one column: the campaign
## (management, visiting), then after a small gap the help of the whole game; it scrolls with
## the focus. The missions start from the ways out of the camp and the blacksmith stands in the
## camp, so neither is here. Back returns to the camp (to the main menu when there is nothing to
## go back to).
## Router.params: profile_path (tests and screenshots) goes on to the pages.

var path: String = Profile.PATH
var buttons: Array[Button] = []

@onready var list: VBoxContainer = %List


func _ready() -> void:
	path = profile_path()
	for b in list.get_children():
		if b is Button:
			buttons.append(b)
	if not Visits.can_visit(Profile.load_or_new(path)):
		list.get_node("Visiting").modulate = Color(1, 1, 1, 0.5)  # only says when one can visit
	buttons[0].grab_focus.call_deferred()


func _open(screen: String) -> void:
	Router.push(screen, Router.params)


## Back goes where the menu was opened from.
func go_back() -> void:
	if not Router.back():
		Router.go("main_menu")
