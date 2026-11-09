extends "res://tests/test_case.gd"
## The line of control hints under the screens, and the buttons that make a screen clear without
## knowing its keys: Done / Reset / Back on the new hero's points, Back in the campaign.

const TEST_PATH := "user://test_hints.json"


func test_menu_line_by_device() -> void:
	var was: String = InputSetup.device
	var menu := Control.new()  # a screen with no line of its own
	InputSetup.device = "keys"
	check(HintBar.text_for(menu).contains("Enter"), "the keyboard's keys")
	InputSetup.device = "pad"
	var pad := HintBar.text_for(menu)
	check(pad.contains("A") and pad.contains("B"), "the pad's buttons")
	InputSetup.device = was
	eq(HintBar.text_for(null), "", "no screen, no line")
	menu.free()


func test_screens_with_own_line() -> void:
	var screen: Control = Router.make(Router.SCREENS["title"])
	eq(HintBar.text_for(screen), "", "the title has its own line: no bar")
	screen.free()


func _new_game_at_points() -> Control:
	Router.params = {"profile_path": TEST_PATH}
	var screen: Control = NewGameScreen.new()
	root.add_child(screen)
	screen.choose_head(1)
	screen.name_edit.text = "Ivan"
	screen.submit_name()
	return screen


func test_points_have_done_reset_back() -> void:
	var old: Dictionary = Router.params
	var screen := _new_game_at_points()
	var was: String = InputSetup.device
	InputSetup.device = "keys"
	check(screen.controls_hint().contains("+1"), "the line says a press adds a point")
	InputSetup.device = was
	eq(screen.stat_buttons[0].text, "+", 'a "+" beside each stat')
	check(screen.done_button.disabled, "Done waits for every point")
	check(screen.reset_button.disabled, "nothing to reset yet")
	var hp: int = screen.profile.base_hp
	screen.spend(Profile.Stat.HP)
	check(not screen.reset_button.disabled, "Reset once a point is spent")
	screen.reset_points()
	eq(screen.profile.base_hp, hp, "Reset gives the point back")
	eq(screen.profile.stat_points, Profile.START_POINTS, "all five again")
	eq(screen.profile.hero_name, "Ivan", "the name stays")
	for i in Profile.START_POINTS:
		screen.spend(Profile.Stat.ATTACK)
	check(not screen.done_button.disabled, "Done once every point is spent")
	screen.ask.hide()  # the question cancelled: Done is still there to go on
	check(screen.done_button.visible and not screen.done_button.disabled, "Done stays")
	screen.go_back()
	eq(screen.step, NewGameScreen.Step.NAME, "Back: the name again")
	check(screen.body.get_node("Back") != null, "Back under the name too")
	screen.free()
	Router.params = old


func test_campaign_back_button() -> void:
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var screen: Control = CampaignScreen.new()
	root.add_child(screen)
	check(screen.find_child("Back", true, false) is Button, "a Back button")
	screen._open_lord(1)
	eq(screen.level, 2, "a lord's missions")
	screen.go_back()
	eq(screen.level, 1, "Back: the lords again")
	screen.free()
	Router.params = old
