extends Control
## The story player, as pyport's: the opening of a new game and the endings.
## A talk page types its line into one of two boxes under "Prologue" / "Epilogue", as the
## briefing does: the one who speaks (the master, a general) at the top beside his portrait,
## the hero at the bottom beside his; each box keeps its last line. A line typed out goes on
## by itself after 15 ticks; attack / accept / a click shows the whole line, or goes on at once.
## A picture page shows the story picture, then its text floats up over it a line at a time
## (white in the middle of the screen, grey above and below it, each on a dark backing so it
## reads over the picture) and the picture goes; an
## ending played after its mission ends with the numbers of the game done floating up, and
## what the ending gave in a popup. These pages go on by themselves; a press does nothing there.
## SKIP (Q, F1, the pad's Back, the Skip button, back): on a talk of the opening, the end; on a
## talk of an ending, its pictures; on a picture or the numbers, the next page.
## Params: story (Stories.OPENING or an ending), reward_item, opened_lord, replay (played again
## from Endings: no numbers, no popup), then (a screen to open when the story is over, instead
## of going back).

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Stories := preload("res://scripts/core/stories.gd")
const Items := preload("res://scripts/core/items.gd")
const Campaign := preload("res://scripts/core/campaign.gd")
const PORTRAITS := "res://assets/original/portraits/%d.png"
const PICTURES := "res://assets/original/story/e%d.png"
const SCALE := 3
const CHARS_PER_SECOND := 40.0
## Ticks a typed line stays before the story goes on by itself.
const WAIT_TICKS := 15
## The floating text, in the original screen's pixels (240 x 320, the middle at y 160): it
## starts at y 230 (the numbers at 320, below the screen), goes up 2 a tick, a line every 22,
## wrapped at 200; a line is drawn from y 230 up, white within 72 of the middle, grey beyond,
## and is gone above -28.
const SCREEN_H := 320
const MIDDLE := 160
const TEXT_FROM := 230
const LINE_STEP := 22
const RISE := 2
const WRAP := 200
const BRIGHT := 72
const GONE := -28
const LINE_FONT := 32
## Ticks the picture comes and goes in, and the wait after it before the next page.
const PICTURE_TICKS := 3
const AFTER_TICKS := 3

var profile: RefCounted
var story := Stories.OPENING
var pages: Array = []
var page := -1
var background: ColorRect  # black under the pictures and the numbers
var talk_box: Control
var title: Label
var speaker_portrait: TextureRect
var hero_portrait: TextureRect
var speaker_says: Label
var hero_says: Label
var typing: Label  # the box being typed on a talk page
var picture: TextureRect
var float_box: Control  # the floating lines, a Label each
var lines: PackedStringArray = []  # the floating text of this page
var reward: AcceptDialog  # what the ending gave
var skip_button: Button
## Picture pages: 0 the picture comes, 1 its text floats up, 2 the picture goes.
var phase := 0
var first_line := 0  # the first floating line still on the screen
var first_y := 0  # its y
var _fade := 0
var _after := 0  # ticks left before the next page, 0: not yet
var _ticks := 0.0
var _typed := 0.0
var _wait := -1.0  # seconds before the next talk page comes by itself, -1: not yet
var _over := false


func _ready() -> void:
	var p: Dictionary = Router.params
	profile = Profile.load_or_new(str(p.get("profile_path", Profile.PATH)))
	story = int(p.get("story", Stories.OPENING))
	pages = Stories.pages(story, profile.hero_name)
	if bool(p.get("replay", false)):
		pages = pages.filter(func(pg): return str(pg.kind) != "stats")
	background = ColorRect.new()
	background.color = Color.BLACK
	background.set_anchors_preset(Control.PRESET_FULL_RECT)
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE  # a click goes to the screen
	add_child(background)

	var col := UiTheme.menu_column(self, 760)
	col.add_theme_constant_override("separation", 12)
	talk_box = col.get_parent()
	talk_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	title = UiTheme.heading("story.prologue" if story == Stories.OPENING else "story.epilogue", 40)
	title.name = "Title"
	col.add_child(title)
	var top := HBoxContainer.new()
	top.add_theme_constant_override("separation", 16)
	speaker_portrait = _portrait("SpeakerPortrait")
	speaker_says = _speech("SpeakerSays")
	top.add_child(speaker_portrait)
	top.add_child(speaker_says)
	col.add_child(top)
	var bottom := HBoxContainer.new()
	bottom.add_theme_constant_override("separation", 16)
	hero_says = _speech("HeroSays")
	hero_portrait = _portrait("HeroPortrait")
	bottom.add_child(hero_says)
	bottom.add_child(hero_portrait)
	col.add_child(bottom)
	hero_portrait.texture = load(PORTRAITS % (Stories.HERO_PORTRAIT + int(profile.head)))

	var center := CenterContainer.new()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)
	picture = TextureRect.new()
	picture.name = "Picture"
	picture.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.custom_minimum_size = Vector2(117, 90) * SCALE
	center.add_child(picture)
	float_box = Control.new()
	float_box.name = "Lines"
	float_box.set_anchors_preset(Control.PRESET_FULL_RECT)
	float_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(float_box)

	skip_button = Button.new()
	skip_button.name = "Skip"
	skip_button.text = "common.skip"
	skip_button.flat = true
	skip_button.focus_mode = Control.FOCUS_NONE
	skip_button.set_anchors_preset(Control.PRESET_BOTTOM_LEFT)
	skip_button.position = Vector2(12, -60)
	skip_button.pressed.connect(skip)
	add_child(skip_button)
	reward = AcceptDialog.new()
	reward.name = "Reward"
	reward.title = ""
	add_child(reward)
	next_page()


func _portrait(node_name: String) -> TextureRect:
	var t := TextureRect.new()
	t.name = node_name
	t.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	t.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	t.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	t.custom_minimum_size = Vector2(46, 46) * SCALE
	return t


func _speech(node_name: String) -> Label:
	var l := Label.new()
	l.name = node_name
	l.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	l.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	l.custom_minimum_size = Vector2(0, 46 * SCALE)
	l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	return l


## Shows the next page, or ends the story. False when it is over.
func next_page() -> bool:
	page += 1
	_wait = -1.0
	_after = 0
	_ticks = 0.0
	_set_lines([])
	if page >= pages.size():
		_end()
		return false
	var pg: Dictionary = pages[page]
	var talking := str(pg.kind) == "talk"
	background.visible = not talking
	talk_box.visible = talking
	picture.visible = false
	match str(pg.kind):
		"talk":
			Audio.play_music(0)
			if typing != null:
				typing.visible_characters = -1  # the other box keeps its line whole
			var who := int(pg.speaker)
			if who == Stories.HERO:
				typing = hero_says
			else:
				typing = speaker_says
				speaker_portrait.texture = load(PORTRAITS % who)
			typing.text = str(pg.text)
			typing.visible_characters = 0
			_typed = 0.0
		"picture":
			Audio.play_music(2)
			picture.texture = load(PICTURES % (int(pg.picture) + 1))
			_set_lines(wrap_lines(str(pg.text), _line_font(), LINE_FONT, WRAP * SCALE))
			phase = 0
			_fade = 0
			first_y = TEXT_FROM
		"stats":
			_set_lines(PackedStringArray(Stories.stats_lines(profile)))
			phase = 1
			first_y = SCREEN_H
			var got := reward_lines()
			if not got.is_empty():
				reward.dialog_text = "\n".join(PackedStringArray(got))
				reward.popup_centered()
	_place_lines()
	return true


## What the ending gave, as pyport's popup: "Oksana's scarf / received!", then "Hidden
## Mission!" and the lord opened.
func reward_lines() -> Array:
	var p: Dictionary = Router.params
	var out: Array = []
	var item := int(p.get("reward_item", 0))
	if item != 0:
		out.append_array([Items.name_of(item) if item != Profile.SCARF else "Oksana's scarf", "received!"])
	var lord := int(p.get("opened_lord", 0))
	if lord != 0:
		if not out.is_empty():
			out.append("")
		out.append_array(["Hidden Mission!", Campaign.new().lord_name(lord)])
	return out


## `text` in lines no wider than `width` (a word longer than that keeps a line of its own).
static func wrap_lines(text: String, font: Font, font_size: int, width: float) -> PackedStringArray:
	var out := PackedStringArray()
	var line := ""
	for word in text.split(" ", false):
		var longer := word if line.is_empty() else line + " " + word
		if line.is_empty() or font.get_string_size(longer, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x <= width:
			line = longer
		else:
			out.append(line)
			line = word
	if not line.is_empty():
		out.append(line)
	return out


func _line_font() -> Font:
	return get_theme_font("font", "Label")


func _set_lines(new_lines: PackedStringArray) -> void:
	lines = new_lines
	first_line = 0
	for c in float_box.get_children():
		float_box.remove_child(c)
		c.queue_free()
	for l in lines:
		var label := Label.new()
		label.text = l
		label.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		label.add_theme_font_size_override("font_size", LINE_FONT)
		label.add_theme_color_override("font_outline_color", Color.BLACK)
		label.add_theme_constant_override("outline_size", 6)
		label.add_theme_stylebox_override("normal", line_backing())
		label.set_anchors_preset(Control.PRESET_CENTER_TOP)  # as wide as its words
		label.grow_horizontal = Control.GROW_DIRECTION_BOTH
		label.visible = false
		float_box.add_child(label)


## The dark, half-clear box under a floating line.
static func line_backing() -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(0, 0, 0, 0.55)
	sb.content_margin_left = 16
	sb.content_margin_right = 16
	sb.set_corner_radius_all(6)
	return sb


## The y of floating line `i` on the original screen, or -1000 while it is not drawn (not up to
## y 230 yet, gone, or not floating now).
func line_y(i: int) -> int:
	if phase != 1 or i < first_line or i >= lines.size():
		return -1000
	var y := first_y + (i - first_line) * LINE_STEP
	return y if y <= TEXT_FROM else -1000


## White within 72 of the middle of the screen, grey beyond it.
static func line_color(y: int) -> Color:
	return UiTheme.TEXT if absi(y - MIDDLE) <= BRIGHT else UiTheme.TEXT_DIM


func _place_lines() -> void:
	var kids := float_box.get_children()
	for i in kids.size():
		var label: Label = kids[i]
		var y := line_y(i)
		label.visible = y > -1000
		if label.visible:
			label.offset_top = size.y / 2 + (y - MIDDLE) * SCALE
			label.offset_bottom = label.offset_top + LINE_STEP * SCALE
			label.add_theme_color_override("font_color", line_color(y))
	if page < pages.size() and str(pages[page].kind) == "picture":
		picture.visible = phase == 1 or (_fade > 0 and _fade <= PICTURE_TICKS)


## One tick of a picture page or of the numbers.
func tick() -> void:
	if _after > 0:
		_after -= 1
		if _after == 0:
			next_page()
		return
	match phase:
		0:  # the picture comes
			_fade += 1
			if _fade > PICTURE_TICKS:
				phase = 1
				_fade = 0
		1:  # the text floats up
			first_y -= RISE
			if first_y < GONE:
				first_y += LINE_STEP
				first_line += 1
				if first_line >= lines.size():
					if str(pages[page].kind) == "stats":
						_after = AFTER_TICKS
					else:
						phase = 2
						_fade = 1
		2:  # the picture goes
			_fade += 1
			if _fade > PICTURE_TICKS:
				_after = AFTER_TICKS
	_place_lines()


## Attack / accept / a click: on a talk, the whole line, or the next page at once.
func press() -> void:
	if _over or page >= pages.size() or str(pages[page].kind) != "talk":
		return
	if typing.visible_characters >= 0 and typing.visible_characters < typing.text.length():
		typing.visible_characters = -1
		_wait = WAIT_TICKS * Settings.tick_seconds()
	else:
		next_page()


func _process(delta: float) -> void:
	if _over or page >= pages.size():
		return
	if str(pages[page].kind) != "talk":
		_ticks += delta
		var t: float = Settings.tick_seconds()
		var at := page
		while _ticks >= t and page == at and not _over:
			_ticks -= t
			tick()
		return
	if _wait >= 0.0:
		_wait -= delta
		if _wait < 0.0:
			next_page()
		return
	if typing.visible_characters < 0:
		return
	_typed += delta * CHARS_PER_SECOND
	typing.visible_characters = mini(int(_typed), typing.text.length())
	if typing.visible_characters >= typing.text.length():
		typing.visible_characters = -1
		_wait = WAIT_TICKS * Settings.tick_seconds()


## The story is over: back (or on to `then`); while the popup of what the ending gave is up,
## once it is closed.
func _end() -> void:
	if _over:
		return
	if reward.visible:
		if not reward.visibility_changed.is_connected(_end):
			reward.visibility_changed.connect(_end, CONNECT_ONE_SHOT)
		return
	_over = true
	set_process(false)
	var then := str(Router.params.get("then", ""))
	Router.back()
	if not then.is_empty():
		Router.push(then)


## SKIP: from a talk of the opening to the end, from a talk of an ending to its pictures; on a
## picture or the numbers, the next page.
func skip() -> void:
	if _over or page >= pages.size():
		return
	if str(pages[page].kind) == "talk":
		if story == Stories.OPENING:
			page = pages.size() - 1
		else:
			var first := page
			while first < pages.size() and str(pages[first].kind) == "talk":
				first += 1
			page = first - 1
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


## The line of control hints under the screen (scripts/ui/hint_bar.gd).
func controls_hint() -> String:
	return InputSetup.hint("hint.skip")
