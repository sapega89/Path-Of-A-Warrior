extends "res://tests/test_case.gd"

const ENDING_2 := {
	"story": 2, "reward_item": 502, "opened_lord": 8, "profile_path": "user://no_such_hero.json"
}


func test_opening_pages() -> void:
	var pages: Array = Stories.pages(Stories.OPENING, "Leo")
	eq(pages.size(), 13, "13 pages")
	eq(pages[0].kind, "picture", "a picture first")
	eq(int(pages[0].picture), 1, "the second story picture")
	eq(int(pages[1].picture), 10, "then the eleventh")
	eq(
		pages[2].text,
		"[Prior] So you have found your way to the Motronyn Monastery.",
		"the prior talks"
	)
	eq(int(pages[2].speaker), Stories.NOFACE, "no face")
	eq(pages[3].text, "[Leo] ...", "the hero answers")
	eq(int(pages[3].speaker), Stories.HERO, "the hero")


func test_ending_pages() -> void:
	var pages: Array = Stories.pages(0, "Leo")
	eq(pages.size(), 10, "5 talk, 4 pictures, the numbers")
	eq(int(pages[0].speaker), 0, "the messenger")
	check(str(pages[0].text).begins_with("[Messenger] Sir,"), "his line")
	check(str(pages[1].text).begins_with("[Leo] No."), "the hero's line")
	eq(
		pages[2].text,
		"[Messenger] The country still needs men like you.",
		"the line of the game's strings"
	)
	eq(int(pages[5].picture), 0, "the first picture")
	check(str(pages[5].text).begins_with("That was how I walked away"), "its text")
	eq(int(pages[6].picture), 1, "picture 2 (e2)")
	check(str(pages[6].text).begins_with("But fate"), "its text")
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


func _story(params: Dictionary) -> Control:
	Router.params = params
	var screen: Control = Router.make(Router.SCREENS["story"])
	root.add_child(screen)
	return screen


## A talk, as pyport's: two boxes under "Epilogue", the one who speaks at the top, the hero at
## the bottom; each keeps its last line.
func test_story_talk() -> void:
	var old: Dictionary = Router.params
	var screen := _story(ENDING_2)
	eq(screen.title.text, "story.epilogue", "an ending: the epilogue")
	check(
		screen.talk_box.visible and not screen.background.visible,
		"the talk on the menu's background"
	)
	eq(screen.typing, screen.speaker_says, "Oksana speaks at the top")
	eq(
		screen.speaker_says.text,
		"[Oksana] It is cold... so cold. I cannot feel my hands...",
		"her line"
	)
	check(screen.speaker_portrait.texture.resource_path.ends_with("/37.png"), "beside her portrait")
	check(
		screen.hero_portrait.texture.resource_path.ends_with("/38.png"), "the hero's at the bottom"
	)
	eq(screen.typing.visible_characters, 0, "typed out")
	screen.press()
	eq(screen.typing.visible_characters, -1, "a press: the whole line")
	screen.press()
	eq(screen.page, 1, "another: the next page")
	check(
		screen.speaker_portrait.texture.resource_path.ends_with("/1.png"),
		"General Augustine's portrait"
	)
	for i in 4:
		screen.next_page()
	eq([screen.page, screen.typing], [5, screen.hero_says], "the hero answers at the bottom")
	eq(
		[screen.speaker_says.text, screen.speaker_says.visible_characters],
		["[Cossack] Run for it! Run!", -1],
		"the top box keeps its last line"
	)
	screen.free()
	screen = _story({"profile_path": "user://no_such_hero.json"})
	eq(screen.title.text, "story.prologue", "the opening: the prologue")
	screen.free()
	Router.params = old


## A picture, as pyport's: the picture comes, its text floats up over it 2 a tick (a line every
## 22, from y 230, white within 72 of the middle), the picture goes and the next page comes.
func test_story_picture_floats() -> void:
	var old: Dictionary = Router.params
	var screen := _story(ENDING_2)
	screen.page = 13
	screen.next_page()
	eq(screen.pages[screen.page].kind, "picture", "a picture")
	check(screen.background.visible and not screen.talk_box.visible, "on black")
	check(screen.lines.size() > 1, "its text in lines: %s" % [screen.lines])
	check(screen.lines[0].begins_with("Colonel Kozub gave up"), screen.lines[0])
	check(not screen.picture.visible, "the picture comes")
	screen.tick()
	check(screen.picture.visible, "it is there")
	eq(screen.line_y(0), -1000, "the text not yet")
	for i in 3:
		screen.tick()
	eq(
		[screen.phase, screen.line_y(0), screen.line_y(1)],
		[1, 230, -1000],
		"the first line at 230, the next below"
	)
	eq(screen.line_color(230), Color(UiTheme.TEXT), "white in the middle")
	screen.tick()
	eq(screen.line_y(0), 228, "up 2 a tick")
	for i in 10:
		screen.tick()
	eq([screen.line_y(0), screen.line_y(1)], [208, 230], "the next line 22 below")
	eq(screen.line_color(60), Color(UiTheme.TEXT_DIM), "grey above the middle")
	screen.press()
	eq(screen.page, 14, "a press does nothing there")
	var guard := 0
	while screen.phase == 1 and guard < 2000:
		screen.tick()
		guard += 1
	eq(
		[screen.phase, screen.line_y(screen.lines.size() - 1)],
		[2, -1000],
		"all gone up: the picture goes"
	)
	for i in 7:
		screen.tick()
	eq(screen.page, 15, "then the next page")
	screen.free()
	Router.params = old


## The numbers float up from below the screen, without a picture, and what the ending gave
## comes in a popup; the story ends after them, once the popup is closed.
func test_story_numbers_and_reward() -> void:
	var old: Dictionary = Router.params
	var host := Control.new()
	root.add_child(host)
	Router.attach(host)
	Router.go("title")
	Router.push("story", ENDING_2)
	var screen: Control = Router.current
	screen.page = screen.pages.size() - 2
	screen.next_page()
	eq(screen.pages[screen.page].kind, "stats", "the numbers")
	check(not screen.picture.visible, "no picture")
	eq(
		Array(screen.lines.slice(0, 3)),
		["Mission", "Accomplished", "0 %"],
		"a line each, as pyport's"
	)
	eq(screen.lines.size(), 12, "missions, hidden missions, endings, generals, the total")
	eq(screen.line_y(0), -1000, "below the screen")
	for i in 45:
		screen.tick()
	eq(screen.line_y(0), 230, "then up")
	check(screen.reward.visible, "the reward popup")
	eq(
		screen.reward.dialog_text,
		"Oksana's scarf\nreceived!\n\n%s\n%s" % [tr("story.new_road"), Campaign.new().lord_name(8)],
		"what the ending gave"
	)
	screen.skip()
	eq(Router.current, screen, "the story waits for the popup")
	screen.reward.hide()
	eq(Router.current_name(), "title", "then it is over")
	Router.attach(null)
	host.free()
	Router.params = old


## Played again from Endings: no numbers, no popup.
func test_story_replay() -> void:
	var old: Dictionary = Router.params
	var params := ENDING_2.duplicate()
	params["replay"] = true
	var screen := _story(params)
	eq(screen.pages[screen.pages.size() - 1].kind, "picture", "it ends with its last picture")
	screen.free()
	Router.params = old


## A click anywhere is attack / accept: the screen takes it in _gui_input (in a window a click
## never reaches _unhandled_input).
func test_story_screen_click() -> void:
	var old: Dictionary = Router.params
	var screen := _story(ENDING_2)
	eq(
		screen.get_child(0).mouse_filter,
		Control.MOUSE_FILTER_IGNORE,
		"the black background lets clicks through"
	)
	var click := InputEventMouseButton.new()
	click.button_index = MOUSE_BUTTON_LEFT
	click.pressed = true
	screen._gui_input(click)
	eq(screen.typing.visible_characters, -1, "a click: the whole line")
	screen._gui_input(click)
	eq(screen.page, 1, "another: the next page")
	click.pressed = false
	screen._gui_input(click)
	eq(screen.page, 1, "a release does nothing")
	screen.free()
	Router.params = old


## As pyport's: a talk typed out goes on by itself after 15 ticks; a picture goes on by itself
## in ticks of the game's speed.
func test_story_goes_on_by_itself() -> void:
	var old: Dictionary = Router.params
	var screen := _story(ENDING_2)
	var wait: float = StoryScreen.WAIT_TICKS * Settings.tick_seconds()
	step_dialogue(screen.dialogue, screen.typing.text.length() / Dialogue.CHARS_PER_SECOND + 0.01)
	eq(screen.typing.visible_characters, -1, "the line typed out")
	step_dialogue(screen.dialogue, wait * 0.5)
	eq(screen.page, 0, "it stays a moment")
	step_dialogue(screen.dialogue, wait)
	eq(screen.page, 1, "then the next page")
	screen.press()
	step_dialogue(screen.dialogue, wait * 0.5)
	eq(screen.page, 1, "shown whole by a press: it stays a moment too")
	step_dialogue(screen.dialogue, wait)
	eq(screen.page, 2, "then goes on")
	screen.page = 13
	screen.next_page()
	screen._process(Settings.tick_seconds() * 5.5)
	eq([screen.phase, screen.line_y(0)], [1, 228], "a picture: a tick at a time")
	screen.free()
	Router.params = old
