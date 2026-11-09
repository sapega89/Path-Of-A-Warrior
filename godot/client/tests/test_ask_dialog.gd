extends "res://tests/test_case.gd"
## The game's own question and notice (scripts/ui/ask_dialog.gd): in the game's theme, the focus
## on Yes or (when Yes loses something) on No, Back answers No, and the keys do not reach the
## screen under it.


func _cancel() -> InputEventAction:
	var ev := InputEventAction.new()
	ev.action = "ui_cancel"
	ev.pressed = true
	return ev


func test_question() -> void:
	var host := Control.new()
	host.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.add_child(host)
	var before := Button.new()
	host.add_child(before)
	before.grab_focus()
	var ask: Control = AskDialog.new()
	host.add_child(ask)
	var answers := []
	ask.confirmed.connect(func() -> void: answers.append("yes"))
	ask.canceled.connect(func() -> void: answers.append("no"))
	ask.dialog_text = "Continue?"
	eq(ask.label.text, "Continue?", "its text")
	eq([ask.ok.text, ask.cancel.text], ["ask.yes", "ask.no"], "Yes and No")
	check(not ask.visible, "hidden until asked")
	ask.popup_centered()
	check(ask.visible, "shown")
	check(ask.ok.has_focus(), "the focus on Yes")
	eq(host.get_child(-1), ask, "over the rest of the screen")
	ask.get_viewport().push_input(_cancel())
	check(not ask.visible, "Back closes it")
	eq(answers, ["no"], "Back answers No")
	check(before.has_focus(), "the focus back where it was")
	ask.safe_default = true
	ask.popup_centered()
	check(ask.cancel.has_focus(), "safe: the focus on No")
	before.grab_focus()  # the screen's own deferred focus, in the same frame
	ask._focus_first()  # the dialog's deferred call after it
	check(ask.cancel.has_focus(), "the focus taken back to No")
	ask.ok.grab_focus()
	ask._focus_first()
	check(ask.ok.has_focus(), "a button of its own keeps the focus")
	ask.cancel.grab_focus()
	ask.ok.pressed.emit()
	eq(answers, ["no", "yes"], "Yes answers Yes")
	check(not ask.visible, "and closes it")
	host.free()


func test_notice() -> void:
	var note: Control = AskDialog.new(true)
	root.add_child(note)
	check(not note.cancel.visible, "a notice has OK alone")
	eq(note.ok.text, "ask.ok", "OK")
	note.popup_centered()
	check(note.ok.has_focus(), "the focus on OK")
	note.free()


## Back on the question after the last point closes the question; the points stay (it does not
## go back to the name, as Back on the screen does).
func test_back_stays_with_the_question() -> void:
	var old: Dictionary = Router.params
	Router.params = {"profile_path": "user://test_ask.json"}
	var screen: Control = NewGameScreen.new()
	root.add_child(screen)
	check(screen.ask is AskDialog, "the game's own question")
	screen.choose_head(0)
	screen.name_edit.text = "Ivan"
	screen.submit_name()
	for i in Profile.START_POINTS:
		screen.spend(Profile.Stat.HP)
	check(screen.ask.visible, "asked to go on")
	screen.get_viewport().push_input(_cancel())
	check(not screen.ask.visible, "Back: the question goes")
	eq(screen.step, NewGameScreen.Step.POINTS, "the points stay")
	check(screen.done_button.has_focus(), "the focus on Done again")
	screen.free()
	Router.params = old


func test_main_menu_asks_with_no_first() -> void:
	var menu: Control = Router.make(Router.SCREENS["main_menu"])
	root.add_child(menu)
	check(menu.ask is AskDialog and menu.ask.safe_default, "deleting the save: No first")
	menu.free()
