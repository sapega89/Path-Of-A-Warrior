extends "res://tests/test_case.gd"
## The game menu has the hero's own pages and Help: no Trade or Safe, nothing on a server, and
## no Blacksmith (he stands in the camp).

const TEST_PATH := "user://test_game_menu.json"


func test_the_hero_pages_and_help() -> void:
	Profile.new().save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var screen: Control = Router.make(Router.SCREENS["game_menu"])
	root.add_child(screen)
	eq(
		screen.buttons.map(func(b: Button) -> String: return str(b.name)),
		["Management", "Visiting", "Help"],
		"the campaign's pages, then Help"
	)
	check(screen.list.get_node_or_null("Blacksmith") == null, "no Blacksmith: he is in the camp")
	check(screen.list.get_node_or_null("Trade") == null, "no Trade")
	check(screen.list.get_node_or_null("Safe") == null, "no Safe")
	screen.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))
