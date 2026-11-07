extends "res://tests/test_case.gd"
## Before a mission, as pyport: its description, "Do you want to accept this mission?", the
## briefing (the advice and the hero's answer), then the map.

const Profile := preload("res://scripts/core/profile.gd")
const RouterScript := preload("res://scripts/core/router.gd")
const Briefing := preload("res://scripts/screens/briefing_screen.gd")
const PATH := "user://test_briefing.json"


func _cancel() -> InputEventAction:
	var ev := InputEventAction.new()
	ev.action = "ui_cancel"
	ev.pressed = true
	return ev


func test_replace_takes_the_place_of_the_top() -> void:
	var host := Control.new()
	root.add_child(host)
	var r: Node = RouterScript.new()
	r.attach(host)
	check(r.replace("title"), "on an empty stack it shows the screen")
	eq(r.depth(), 1, "as go")
	r.push("settings")
	check(r.replace("help", {"a": 1}), "replace")
	eq([r.current_name(), r.depth(), r.params], ["help", 2, {"a": 1}], "help in the place of settings")
	r.back()
	eq(r.current_name(), "title", "back goes where settings would have")
	check(not r.replace("nope"), "unknown screen")
	eq(r.current_name(), "title", "and nothing changed")
	r.free()
	host.free()


func test_briefing_lines_in_turn_then_random() -> void:
	var p: RefCounted = Profile.new()
	var rng := RandomNumberGenerator.new()
	rng.seed = 3
	for i in 10:
		eq(p.next_briefing(rng), i * 2, "mission %d accepted: advice %d" % [i + 1, i])
	var seen := {}
	for i in 300:
		var line: int = p.next_briefing(rng)
		check(line >= 20 and line <= 54 and line % 2 == 0, "then a random one of the rest: %d" % line)
		seen[line] = true
	eq(p.briefings, 11, "the count stops at 11")
	eq(seen.size(), 18, "each of the 18 others comes")
	var q: RefCounted = Profile.new()
	q.from_dict(p.to_dict())
	eq(q.briefings, 11, "saved with the hero")
	eq(Profile.new().briefings, 0, "a new hero: from the first")
	p.on_map = {"lord": 1, "mission": 0}
	p.save_keeping_map(PATH)
	eq(int(Profile.load_or_new(PATH).on_map.get("lord", 0)), 1, "counting it keeps a mission saved on its map")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(PATH))


func test_briefing_talk() -> void:
	var lines := Briefing.talk(0, "Colonel Bairak", "Ann")
	eq(lines[0], "[Colonel Bairak] You look like you're new here. If you have not visited the Blacksmith already, you ought to.", "the advice")
	eq(lines[1], "[Ann] I hear you.", "the answer")


func test_description_accept_briefing_mission() -> void:
	var old: Dictionary = Router.params
	var host := Control.new()
	root.add_child(host)
	Router.attach(host)
	var p: RefCounted = Profile.new()
	p.level = 3
	p.difficulty = 0
	p.hero_name = "Ann"
	p.on_map = {"lord": 2, "mission": 1}
	p.save_keeping_map(PATH)
	Router.go("campaign", {"level": 2, "lord": 1, "profile_path": PATH})
	var c: Control = Router.current
	(c.list.get_child(0) as Button).pressed.emit()
	eq(c.level, 3, "a mission: its description first")
	eq(c.heading.text, "Uprising", "the lord")
	eq((c.list.get_node("Mission") as Label).text, "Colonel Bairak", "the mission")
	check((c.list.get_node("Description") as Label).text.begins_with("\"The Rise of Darkness\" has roused"),
		"its text")
	c._unhandled_input(_cancel())
	eq(c.level, 2, "back: the missions")
	check(not c.ok.visible, "no OK on the list")
	(c.list.get_child(0) as Button).pressed.emit()
	check(c.ok.visible, "OK under it")
	(c.ok as Button).pressed.emit()
	check(c.ask.visible, "OK asks")
	eq(c.ask.dialog_text, "Zdzislaw Krzeminski\n%s\n\n%s" % [tr("campaign.level_gold") % [4, 900], tr("campaign.accept")],
		"the general, Lv hero + 1 and the gold, twice on hard")
	p.difficulty = 1
	p.save_keeping_map(PATH)
	c.profile = Profile.load_or_new(PATH)
	check(c.accept_text().contains(tr("campaign.level_gold") % [4, 450]), "on normal: the gold once")
	c.ask.hide()
	c.ask.confirmed.emit()
	eq([Router.current_name(), Router.depth()], ["briefing", 2], "Yes: the briefing")
	var saved: RefCounted = Profile.load_or_new(PATH)
	eq(saved.briefings, 1, "counted and saved")
	eq(int(saved.on_map.get("lord", 0)), 2, "the mission saved on its map stays")

	var b: Control = Router.current
	eq(b.lord_says.text, "[Colonel Bairak] You look like you're new here. If you have not visited the Blacksmith already, you ought to.",
		"the advice of the mission's lord")
	eq(b.lord_says.visible_characters, 0, "typed out")
	b._process(0.1)
	eq(b.lord_says.visible_characters, 4, "40 a second")
	b.press()
	eq(b.lord_says.visible_characters, -1, "a press: the whole line")
	b._process(0.1)
	eq(b.typing, b.lord_says, "it stays a moment")
	b._process(1.0)
	eq(b.typing, b.hero_says, "then the hero answers")
	eq(b.hero_says.text, "[Ann] I hear you.", "his answer")
	check(not b.lord_says.text.is_empty(), "the advice stays in its box")
	b._process(10.0)
	eq(b.hero_says.visible_characters, -1, "typed")
	b._process(10.0)
	eq([Router.current_name(), Router.depth()], ["mission", 2], "after the answer: the map, in the briefing's place")
	eq(Router.params, {"lord": 1, "mission": 0}, "of that mission")
	Router.back()
	eq(Router.current_name(), "campaign", "back from the mission: the campaign")

	Router.go("briefing", {"lord": 1, "mission": 2, "line": 4, "profile_path": PATH})
	Router.current._unhandled_input(_cancel())
	eq([Router.current_name(), Router.params], ["mission", {"lord": 1, "mission": 2}], "back skips to the map")
	Router.go("briefing", {"lord": 1, "mission": 0, "line": 4, "profile_path": PATH})
	Router.current.skip.pressed.emit()
	eq(Router.current_name(), "mission", "so does Skip")
	Router.attach(null)
	host.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(PATH))
