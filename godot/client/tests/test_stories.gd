extends "res://tests/test_case.gd"

const Stories := preload("res://scripts/core/stories.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Story := preload("res://scripts/screens/story_screen.gd")


func test_opening_pages() -> void:
	var pages: Array = Stories.pages(Stories.OPENING, "Leo")
	eq(pages.size(), 13, "13 pages")
	eq(pages[0].kind, "picture", "a picture first")
	eq(int(pages[0].picture), 1, "the second story picture")
	eq(int(pages[1].picture), 10, "then the eleventh")
	eq(pages[2].text, "[Master] Welcome to Crimson Temple.", "the master talks")
	eq(int(pages[2].speaker), Stories.NOFACE, "no face")
	eq(pages[3].text, "[Leo] ...", "the hero answers")
	eq(int(pages[3].speaker), Stories.HERO, "the hero")


func test_ending_pages() -> void:
	var pages: Array = Stories.pages(0, "Leo")
	eq(pages.size(), 10, "5 talk, 4 pictures, the numbers")
	eq(int(pages[0].speaker), 0, "the messenger")
	check(str(pages[0].text).begins_with("[Messenger] Sir,"), "his line")
	check(str(pages[1].text).begins_with("[Leo] Nay."), "the hero's line")
	eq(pages[2].text, "[Messenger] The country will need you..", "the line of the game's strings")
	eq(int(pages[5].picture), 0, "the first picture")
	check(str(pages[5].text).begins_with("I could get out"), "its text")
	eq(int(pages[6].picture), 1, "picture 2 (e2)")
	check(str(pages[6].text).begins_with("Alas,"), "its text")
	eq(pages[9].kind, "stats", "the numbers last")


func test_stats() -> void:
	var p := Profile.new()
	p.done["1:0"] = true
	p.done["5:0"] = true  # lord 5: a hidden mission
	p.endings = 0b111
	p.friendship["3"] = 10
	var lines: Array = Stories.stats_lines(p)
	eq(lines[2], "1 %", "2 of 102 missions")
	eq(lines[5], "5 %", "1 of 18 hidden")
	eq(lines[7], "12 %", "3 of 24 endings")
	eq(lines[9], "2 %", "1 of 44 generals")
	eq(lines[11], "5 %", "the average")


func test_story_screen() -> void:
	var old: Dictionary = Router.params
	Router.params = {"story": 2, "reward_item": 502, "opened_lord": 8, "profile_path": "user://no_such_hero.json"}
	var screen: Control = Story.new()
	root.add_child(screen)
	eq(screen.page, 0, "the first page")
	check(screen.portrait.visible, "a talk page shows a portrait")
	eq(screen.text.visible_characters, 0, "typing")
	screen.press()
	eq(screen.text.visible_characters, -1, "the whole line at once")
	screen.press()
	eq(screen.page, 1, "the next page")
	screen.page = screen.pages.size() - 2
	screen.next_page()
	check(screen.text.text.contains("Catherine's scarf\nreceived!"), "the reward")
	check(screen.text.text.begins_with("Mission Accomplished  0 %"), "the numbers a row each")
	check(screen.text.text.contains("Hidden Mission!"), "the lord opened")
	screen.free()
	Router.params = old
