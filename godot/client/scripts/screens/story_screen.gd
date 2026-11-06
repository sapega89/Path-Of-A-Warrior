extends Control
## The story player: the opening of a new game and the endings. Talk pages show the
## speaker's portrait and the line typed out; picture pages show the story picture with its
## text; an ending ends with how much of the game is done and what the ending gave.
## A talk or picture page shown whole goes on by itself after 15 ticks, as pyport's (the last
## page, with the numbers, waits for a key). Attack / accept shows the whole line, or goes on at
## once; back or SKIP (Q, F1, the pad's Back, the Skip button) skips to the end.
## Params: story (Stories.OPENING or an ending), reward_item, opened_lord, then (a screen to
## open when the story is over, instead of going back).

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Stories := preload("res://scripts/core/stories.gd")
const Items := preload("res://scripts/core/items.gd")
const Campaign := preload("res://scripts/core/campaign.gd")
const PORTRAITS := "res://assets/original/portraits/%d.png"
const PICTURES := "res://assets/original/story/e%d.png"
const SCALE := 3
const CHARS_PER_SECOND := 40.0
## Ticks a page shown whole stays before the story goes on by itself.
const WAIT_TICKS := 15

var profile: RefCounted
var story := Stories.OPENING
var pages: Array = []
var page := -1
var portrait: TextureRect
var picture: TextureRect
var text: Label
var skip_button: Button
var _typed := 0.0
var _wait := -1.0  # seconds before the next page comes by itself, -1: it waits for a key


func _ready() -> void:
	var p: Dictionary = Router.params
	profile = Profile.load_or_new(str(p.get("profile_path", Profile.PATH)))
	story = int(p.get("story", Stories.OPENING))
	pages = Stories.pages(story, profile.hero_name)
	var bg := ColorRect.new()
	bg.color = Color.BLACK
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE  # a click goes to the screen
	add_child(bg)
	var col := UiTheme.menu_column(self, 900)
	var row := HBoxContainer.new()
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	portrait = TextureRect.new()
	portrait.name = "Portrait"
	portrait.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	portrait.custom_minimum_size = Vector2(46, 46) * SCALE
	row.add_child(portrait)
	picture = TextureRect.new()
	picture.name = "Picture"
	picture.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.custom_minimum_size = Vector2(117, 90) * SCALE
	row.add_child(picture)
	col.add_child(row)
	text = Label.new()
	text.name = "Text"
	text.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	text.custom_minimum_size = Vector2(900, 200)
	col.add_child(text)
	skip_button = Button.new()
	skip_button.name = "Skip"
	skip_button.text = "common.skip"
	skip_button.flat = true
	skip_button.focus_mode = Control.FOCUS_NONE
	skip_button.set_anchors_preset(Control.PRESET_BOTTOM_LEFT)
	skip_button.position = Vector2(12, -60)
	skip_button.pressed.connect(skip)
	add_child(skip_button)
	next_page()


## Shows the next page, or ends the story. False when it is over.
func next_page() -> bool:
	page += 1
	_wait = -1.0
	if page >= pages.size():
		_end()
		return false
	var pg: Dictionary = pages[page]
	portrait.visible = false
	picture.visible = false
	match str(pg.kind):
		"talk":
			var who := int(pg.speaker)
			if who == Stories.HERO:
				who = Stories.HERO_PORTRAIT + int(profile.head)
			portrait.texture = load(PORTRAITS % who)
			Audio.play_music(0)
			portrait.visible = true
			text.horizontal_alignment = HORIZONTAL_ALIGNMENT_LEFT
			text.text = str(pg.text)
		"picture":
			picture.texture = load(PICTURES % (int(pg.picture) + 1))
			Audio.play_music(2)
			picture.visible = picture.texture != null
			text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			text.text = str(pg.text)
		"stats":
			text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			text.text = "\n".join(PackedStringArray(stats_rows() + reward_lines()))
	_typed = 0.0
	text.visible_characters = 0
	return true


## The numbers of the game done, a row each: "Mission Accomplished  50 %".
func stats_rows() -> Array:
	var l: Array = Stories.stats_lines(profile)
	return ["%s %s  %s" % [l[0], l[1], l[2]], "%s %s  %s" % [l[3], l[4], l[5]],
		"%s  %s" % [l[6], l[7]], "%s  %s" % [l[8], l[9]], "%s  %s" % [l[10], l[11]]]


## What the ending gave: the item received, the hidden mission (lord) opened.
func reward_lines() -> Array:
	var p: Dictionary = Router.params
	var out: Array = []
	var item := int(p.get("reward_item", 0))
	if item != 0:
		out.append_array(["", Items.name_of(item) if item != Profile.SCARF else "Catherine's scarf", "received!"])
	var lord := int(p.get("opened_lord", 0))
	if lord != 0:
		out.append_array(["", "Hidden Mission!", Campaign.new().lord_name(lord)])
	return out


## Shows the whole line at once, or goes on when it is all shown.
func press() -> void:
	if text.visible_characters >= 0 and text.visible_characters < text.text.length():
		text.visible_characters = -1
		_shown()
	else:
		next_page()


## The page is shown whole: a talk or a picture goes on by itself after a moment.
func _shown() -> void:
	if page < pages.size() and str(pages[page].kind) != "stats":
		_wait = WAIT_TICKS * Settings.tick_seconds()


func _process(delta: float) -> void:
	if _wait >= 0.0:
		_wait -= delta
		if _wait < 0.0:
			next_page()
		return
	if text.visible_characters < 0:
		return
	_typed += delta * CHARS_PER_SECOND
	text.visible_characters = mini(int(_typed), text.text.length())
	if text.visible_characters >= text.text.length():
		text.visible_characters = -1
		_shown()


func _end() -> void:
	set_process(false)
	var then := str(Router.params.get("then", ""))
	Router.back()
	if not then.is_empty():
		Router.push(then)


## Skips to the end: of an ending to its numbers, then out.
func skip() -> void:
	page = pages.size() - 2 if story != Stories.OPENING and page < pages.size() - 1 else pages.size()
	next_page()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel") or event.is_action_pressed("skip"):
		get_viewport().set_input_as_handled()
		skip()
	elif event.is_action_pressed("attack") or event.is_action_pressed("ui_accept"):
		get_viewport().set_input_as_handled()
		press()


## A click anywhere, as attack / accept (in a window the screen itself takes the click).
func _gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed:
		accept_event()
		press()
