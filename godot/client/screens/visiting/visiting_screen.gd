class_name VisitingScreen
extends BaseScreen
## Visiting: the generals the hero is friends with and their friendship points; one of them
## comes to visit. He greets the hero (portraits and the lines typed out), the hero picks a
## thing to talk about, they talk, and the visit ends with the friendship gained and the
## general's gift. Saved at once. Without a mission won since the last visit (or without a
## friend) only a notice is shown.
## A line typed out goes on by itself after 15 ticks, as pyport's; attack / accept shows the
## whole line, or goes on at once; back leaves the list.

const CHARS_PER_SECOND := 40.0
## Ticks a line shown whole stays before the talk goes on by itself.
const WAIT_TICKS := 15
enum Step { LIST, GREETING, TOPIC, TALK, DISCUSSED, VISITED, CLOSED }

var profile: RefCounted
var path: String = Profile.PATH
var step := Step.LIST
@onready var heading: Label = %Heading
@onready var list: VBoxContainer = %List
@onready var talk_box: VBoxContainer = %Talk
@onready var general_portrait: TextureRect = %Dialogue.speaker_portrait
@onready var hero_portrait: TextureRect = %Dialogue.hero_portrait
@onready var general_says: Label = %Dialogue.speaker_says
@onready var hero_says: Label = %Dialogue.hero_says
## A notice in the middle: the question, what was discussed, the visit's end.
@onready var text: Label = %Text
var typing: Label  # the speech being typed
@onready var topics: VBoxContainer = %Topics
@onready var ok: Button = %Ok
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
	path = profile_path()
	profile = Profile.load_or_new(path)
	if Router.params.has("seed"):
		rng.seed = int(Router.params.seed)
	hero_portrait.texture = Pictures.portrait(Stories.HERO_PORTRAIT + int(profile.head))
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
			var b := _row(tr(str(MapSim.general_data(int(g[0])).get("name", "?"))), str(g[1]))
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
	general_portrait.texture = Pictures.portrait(int(general.get("portrait", 0)))
	general_says.text = ""
	hero_says.text = ""
	_show_line()


func _name() -> String:
	return tr(str(general.get("name", "?")))


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


## "You visited Jan Gorski. Friendship increased by 5." and the gift, if any.
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


## Back leaves the visits from the list of friends; in a talk it does nothing.
func go_back() -> void:
	if step == Step.LIST:
		Router.back()


func _screen_input(event: InputEvent) -> void:
	if (
		step in [Step.GREETING, Step.TALK]
		and (event.is_action_pressed("attack") or event.is_action_pressed("ui_accept"))
	):
		get_viewport().set_input_as_handled()
		press()


## A click beside the buttons while the general talks, as OK (in a window the screen itself
## takes the click).
func _gui_input(event: InputEvent) -> void:
	if step in [Step.GREETING, Step.TALK] and event is InputEventMouseButton and event.pressed:
		accept_event()
		press()
