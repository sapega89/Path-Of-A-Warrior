class_name BaseScreen
extends Control
## A screen the Router shows. It keeps in one place what every screen does the same way:
## the back key and where the hero the screen works on is kept.
##
## The back key (ui_cancel) calls go_back(), which goes to the previous screen; a screen whose
## back does more (closes a step first, asks) overrides go_back(), and one
## where the key is not "back" now returns false from handles_back(). Every other key goes to
## _screen_input(), which a screen overrides instead of _unhandled_input().


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel") and handles_back():
		get_viewport().set_input_as_handled()
		go_back()
		return
	_screen_input(event)


## What the back key does: the previous screen.
func go_back() -> void:
	Router.back()


## Whether the back key is "back" on this screen right now.
func handles_back() -> bool:
	return true


## The screen's other keys (the back key is already handled when it gets here).
func _screen_input(_event: InputEvent) -> void:
	pass


## Where the hero is kept: Profile.PATH (user://hero.json on this computer), or the file a test
## gives in Router.params.profile_path. This is the one place that reads that param (the
## standards check's profile_path_param marks the others).
static func profile_path() -> String:
	var params: Dictionary = Router.params
	return str(params.get("profile_path", Profile.PATH))  # standards: allow profile_path_param (owner)
