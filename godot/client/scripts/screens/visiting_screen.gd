extends Control
## Visiting: the generals the hero is friends with and their friendship points; one of them
## comes to visit. He greets the hero (portraits and the lines typed out), the hero picks a
## thing to talk about, they talk, and the visit ends with the friendship gained and the
## general's gift. Saved at once. Without a mission won since the last visit (or without a
## friend) only a notice is shown.
## A line typed out goes on by itself after 15 ticks, as pyport's; attack / accept shows the
## whole line, or goes on at once; back leaves the list.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Visits := preload("res://scripts/core/visits.gd")
const Stories := preload("res://scripts/core/stories.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")
const PORTRAITS := "res://assets/original/portraits/%d.png"
const SCALE := 3
const CHARS_PER_SECOND := 40.0
## Ticks a line shown whole stays before the talk goes on by itself.
const WAIT_TICKS := 15
enum Step { LIST, GREETING, TOPIC, TALK, DISCUSSED, VISITED, CLOSED }

var profile: RefCounted
var path: String = Profile.PATH
var step := Step.LIST
var heading: Label
var list: VBoxContainer
var talk_box: VBoxContainer
var general_portrait: TextureRect
var hero_portrait: TextureRect
var general_says: Label
var hero_says: Label
var text: Label  # a notice in the middle: the question, what was discussed, the visit's end
var typing: Label  # the speech being typed
var topics: VBoxContainer
var ok: Button
var general_id := 0
var general := {}
var chosen := 0
var lines: Array = []
var line_at := 0
var gift := {}
var rng := RandomNumberGenerator.new()
var _typed := 0.0
var _wait := -1.0  # seconds before the talk goes on by itself, -1: it waits for a key


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	profile = Profile.load_or_new(path)
	if Router.params.has("seed"):
		rng.seed = int(Router.params.seed)
	var col := UiTheme.menu_column(self, 760)
	heading = UiTheme.heading("visit.title", 40)
	col.add_child(heading)

	list = VBoxContainer.new()
	list.name = "List"
	list.add_theme_constant_override("separation", 6)
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size = Vector2(760, 470)
	scroll.follow_focus = true
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	list.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(list)
	col.add_child(scroll)

	talk_box = VBoxContainer.new()
	talk_box.name = "Talk"
	talk_box.add_theme_constant_override("separation", 12)
	var top := HBoxContainer.new()
	top.add_theme_constant_override("separation", 16)
	top.add_child(_portrait("GeneralPortrait"))
	top.add_child(_speech("GeneralSays"))
	talk_box.add_child(top)
	var bottom := HBoxContainer.new()
	bottom.add_theme_constant_override("separation", 16)
	bottom.add_child(_speech("HeroSays"))
	bottom.add_child(_portrait("HeroPortrait"))
	talk_box.add_child(bottom)
	general_portrait = top.get_child(0)
	general_says = top.get_child(1)
	hero_portrait = bottom.get_child(1)
	hero_says = bottom.get_child(0)
	hero_portrait.texture = load(PORTRAITS % (Stories.HERO_PORTRAIT + int(profile.head)))
	text = Label.new()
	text.name = "Text"
	text.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	text.custom_minimum_size = Vector2(760, 0)
	talk_box.add_child(text)
	topics = VBoxContainer.new()
	topics.name = "Topics"
	for i in Visits.TOPICS.size():
		var b := Button.new()
		b.name = "Topic%d" % i
		b.text = "visit.topic_%d" % i
		b.pressed.connect(choose.bind(i))
		topics.add_child(b)
	talk_box.add_child(topics)
	ok = Button.new()
	ok.name = "Ok"
	ok.text = "visit.ok"
	ok.pressed.connect(press)
	talk_box.add_child(ok)
	col.add_child(talk_box)
	show_list()


func show_list() -> void:
	step = Step.LIST
	talk_box.visible = false
	list.get_parent().visible = true
	heading.text = "visit.title"
	for c in list.get_children():
		list.remove_child(c)
		c.queue_free()
	if not Visits.can_visit(profile):
		var l := Label.new()
		l.name = "Notice"
		l.text = "visit.not_now"
		l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		list.add_child(l)
	else:
		var head := _row(tr("visit.name"), tr("visit.points"))
		head.disabled = true
		head.focus_mode = Control.FOCUS_NONE
		for g in Visits.generals(profile):
			var b := _row(str(MapSim.general_data(int(g[0])).get("name", "?")), str(g[1]))
			b.pressed.connect(open.bind(int(g[0])))
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	list.add_child(back)
	for c in list.get_children():
		if c is Button and not (c as Button).disabled:
			(c as Button).grab_focus.call_deferred()
			break


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


## A row of the list: the name on the left, the points on the right.
func _row(left: String, right: String) -> Button:
	var b := Button.new()
	b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	b.custom_minimum_size = Vector2(0, 44)
	var name_label := Label.new()
	name_label.text = left
	name_label.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	name_label.set_anchors_preset(Control.PRESET_LEFT_WIDE)
	name_label.offset_left = 24
	name_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	name_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	b.add_child(name_label)
	var points := Label.new()
	points.text = right
	points.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	points.set_anchors_preset(Control.PRESET_RIGHT_WIDE)
	points.offset_left = -140
	points.offset_right = -24
	points.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	points.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	points.mouse_filter = Control.MOUSE_FILTER_IGNORE
	b.add_child(points)
	list.add_child(b)
	return b


## The general comes: his greeting.
func open(id: int) -> void:
	general_id = id
	general = MapSim.general_data(id)
	var points := int(profile.friendship.get(str(id), 0))
	lines = Visits.greeting(points, int(general.get("gift_table", 0)), profile.hero_name, _name())
	line_at = 0
	step = Step.GREETING
	list.get_parent().visible = false
	talk_box.visible = true
	heading.text = _name()
	heading.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	general_portrait.texture = load(PORTRAITS % int(general.get("portrait", 0)))
	general_says.text = ""
	hero_says.text = ""
	_show_line()


func _name() -> String:
	return str(general.get("name", "?"))


## Types lines[line_at] into the box of who says it (the hero says the even lines); the
## other box keeps its last line.
func _show_line() -> void:
	topics.visible = false
	ok.visible = false
	text.text = ""
	typing = hero_says if line_at % 2 == 0 else general_says
	typing.text = str(lines[line_at])
	_typed = 0.0
	typing.visible_characters = 0


## A page of a popup: the text in the middle and its OK button.
func _show_popup(body: String) -> void:
	topics.visible = false
	typing = null
	text.text = body
	ok.visible = true
	ok.grab_focus.call_deferred()


## The hero picked what to talk about.
func choose(i: int) -> void:
	if step != Step.TOPIC:
		return
	chosen = i
	lines = Visits.talk(int(general.get("gift_table", 0)), i, profile.hero_name, _name())
	line_at = 0
	step = Step.TALK
	_show_line()


## Attack / accept / OK: the whole line, the next line, the next page.
func press() -> void:
	_wait = -1.0
	match step:
		Step.GREETING, Step.TALK:
			if typing != null and typing.visible_characters >= 0:
				typing.visible_characters = -1
				_wait = WAIT_TICKS * Settings.tick_seconds()
				return
			line_at += 1
			if line_at < lines.size():
				_show_line()
			elif step == Step.GREETING:
				step = Step.TOPIC
				typing = null
				text.text = tr("visit.which_topic")
				topics.visible = true
				(topics.get_child(0) as Button).grab_focus.call_deferred()
			else:
				step = Step.DISCUSSED
				_show_popup(tr("visit.discussed") % [tr("visit.topic_%d" % chosen), _name()])
		Step.DISCUSSED:
			step = Step.VISITED
			gift = Visits.finish(profile, general_id, general, chosen, rng)
			profile.save(path)
			Audio.play_sound(10)
			_show_popup(visited_text())
		Step.VISITED:
			step = Step.CLOSED
			Router.back()


## "You visited Kirkland. Friendship increased by 5." and the gift, if any.
func visited_text() -> String:
	var out: Array = [tr("visit.visited") % _name()]
	out.append(tr("visit.full") if bool(gift.get("full", false)) else tr("visit.more"))
	if int(gift.get("kind", Visits.Gift.NONE)) != Visits.Gift.NONE:
		out.append("")
		if not str(gift.title).is_empty():
			out.append(str(gift.title))
		out.append(str(gift.text))
	return "\n".join(PackedStringArray(out))


func _process(delta: float) -> void:
	if _wait >= 0.0:
		_wait -= delta
		if _wait < 0.0:
			press()
		return
	if typing == null or typing.visible_characters < 0:
		return
	_typed += delta * CHARS_PER_SECOND
	typing.visible_characters = mini(int(_typed), typing.text.length())
	if typing.visible_characters >= typing.text.length():
		typing.visible_characters = -1
		_wait = WAIT_TICKS * Settings.tick_seconds()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		if step == Step.LIST:
			Router.back()
	elif step in [Step.GREETING, Step.TALK] and (event.is_action_pressed("attack")
			or event.is_action_pressed("ui_accept")):
		get_viewport().set_input_as_handled()
		press()


## A click beside the buttons while the general talks, as OK (in a window the screen itself
## takes the click).
func _gui_input(event: InputEvent) -> void:
	if step in [Step.GREETING, Step.TALK] and event is InputEventMouseButton and event.pressed:
		accept_event()
		press()
