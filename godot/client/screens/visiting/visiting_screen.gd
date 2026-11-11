class_name VisitingScreen
extends BaseScreen
## Visiting: the generals the hero is friends with and their friendship points; one of them
## comes to visit. The talk opens in a popup over the list: he greets the hero (portraits and
## the lines typed out, the hero's by his portrait on the right), the hero picks a thing to talk
## about in place of his line, they talk, and a small notice in the talk's place tells what was
## discussed, then the friendship gained and the general's gift. Saved at once. Without a
## mission won since the last visit (or without a friend) only a notice is shown.
## A line typed out goes on by itself after 15 ticks; attack / accept shows the
## whole line, or goes on at once; back leaves the list.

enum Step { LIST, GREETING, TOPIC, TALK, DISCUSSED, VISITED, CLOSED }

## Ticks a line shown whole stays before the talk goes on by itself.
const WAIT_TICKS := 15

var profile: Profile
var path: String = Profile.PATH
var step := Step.LIST
var typing: Label:  # the speech being typed
	get:
		return dialogue.typing
var general_id := 0
var general := {}
var chosen := 0
var lines: Array = []
var line_at := 0
var gift := {}
var rng := RandomNumberGenerator.new()

@onready var column: VBoxContainer = %Column
@onready var list: VBoxContainer = %List
@onready var notice: Label = %Notice
@onready var header: VisitRow = %Header
@onready var friends: VBoxContainer = %Friends
@onready var back: Button = %Back
## The talk's popup over the list: its shade, the talk, then the notice in its place.
@onready var popup: Control = %Popup
@onready var talk: PanelContainer = %Talk
@onready var general_name: Label = %GeneralName
@onready var dialogue: Dialogue = %Dialogue
@onready var general_portrait: TextureRect = %Dialogue.speaker_portrait
@onready var hero_portrait: TextureRect = %Dialogue.hero_portrait
@onready var general_says: Label = %Dialogue.speaker_says
@onready var hero_says: Label = %Dialogue.hero_says
## The question and the four things to talk about, in place of the hero's line.
@onready var topics: VBoxContainer = %Topics
@onready var first_topic: Button = %Topic0
## The notice after the talk: what was discussed, the visit's end; and its OK.
@onready var note: Control = %Note
@onready var text: Label = %Text
@onready var ok: Button = %Ok


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	if Router.params.has("seed"):
		rng.seed = int(Router.params.seed)
	hero_portrait.texture = Pictures.portrait(Stories.HERO_PORTRAIT + int(profile.head))
	header.show_general("visit.name", "visit.points")
	dialogue.line_done.connect(next_line)
	show_list()


func show_list() -> void:
	step = Step.LIST
	popup.visible = false
	for c in friends.get_children():
		friends.remove_child(c)
		c.queue_free()
	var can := Visits.can_visit(profile)
	notice.visible = not can
	header.visible = can
	if can:
		for g in Visits.generals(profile):
			var name_key := str(MapSim.general_data(int(g[0])).get("name", "?"))
			VisitRow.add(friends, name_key, str(g[1])).pressed.connect(open.bind(int(g[0])))
	var first: Button = friends.get_child(0) if friends.get_child_count() > 0 else back
	first.grab_focus.call_deferred()


## The general comes: the popup with his greeting. The list behind it takes no focus.
func open(id: int) -> void:
	general_id = id
	general = MapSim.general_data(id)
	var points := int(profile.friendship.get(str(id), 0))
	lines = Visits.greeting(points, int(general.get("gift_table", 0)), profile.hero_name, _name())
	line_at = 0
	step = Step.GREETING
	column.focus_behavior_recursive = Control.FOCUS_BEHAVIOR_DISABLED
	get_viewport().gui_release_focus()
	popup.visible = true
	talk.visible = true
	note.visible = false
	general_name.text = _name()
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
	hero_says.visible = true
	var box := hero_says if line_at % 2 == 0 else general_says
	dialogue.say(box, str(lines[line_at]), WAIT_TICKS * Settings.tick_seconds())


## The notice in the talk's place: its text and OK.
func _show_note(body: String) -> void:
	dialogue.stop()
	text.text = body
	talk.visible = false
	note.visible = true
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
	match step:
		Step.GREETING, Step.TALK:
			dialogue.press(WAIT_TICKS * Settings.tick_seconds())
		Step.DISCUSSED:
			step = Step.VISITED
			gift = Visits.finish(profile, general_id, general, chosen, rng)
			profile.save(path)
			Audio.play_sound(10)
			_show_note(visited_text())
		Step.VISITED:
			step = Step.CLOSED
			Router.back()


## The talk's next line; after the greeting the things to talk about, after the talk what
## was discussed.
func next_line() -> void:
	line_at += 1
	if line_at < lines.size():
		_show_line()
	elif step == Step.GREETING:
		step = Step.TOPIC
		hero_says.visible = false
		topics.visible = true
		first_topic.grab_focus.call_deferred()
	else:
		step = Step.DISCUSSED
		_show_note(tr("visit.discussed") % [tr("visit.topic_%d" % chosen), _name()])


## "You visited Jan Gorski. Friendship increased by 5." and the gift, if any.
func visited_text() -> String:
	var out: Array = [tr("visit.visited") % _name()]
	out.append(tr("visit.full") if bool(gift.get("full", false)) else tr("visit.more"))
	if int(gift.get("kind", Visits.Gift.NONE)) != Visits.Gift.NONE:
		out.append("")
		if not str(gift.title).is_empty():
			out.append(tr(str(gift.title)))
		out.append(tr(str(gift.text)))
	return "\n".join(PackedStringArray(out))


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


## A click beside the buttons while the general talks, as OK (the popup's shade and panel pass
## the click on to the screen; in a window the screen itself takes the click).
func _gui_input(event: InputEvent) -> void:
	if step in [Step.GREETING, Step.TALK] and event is InputEventMouseButton and event.pressed:
		accept_event()
		press()
