class_name BriefingScreen
extends BaseScreen
## The briefing of an accepted mission: the one who gives it (the mission's portrait, at the
## top) advises the hero and the hero (at the bottom) answers. Each line is typed out into its
## box and stays there; a line typed out goes on by itself after a moment. Attack / accept or a
## click shows the whole line, or goes on at once; back or SKIP (Q, F1, the pad's Back, the
## Skip button) goes straight to the map. The mission then takes the briefing's place, so back
## from the mission goes to the campaign.
## Params: lord, mission, line (the advice's line of talk.json "briefing", the hero answers
## with the next one), profile_path.

const CHARS_PER_SECOND := 40.0
## Ticks a typed line stays before the next one, and after a press that showed it whole.
const WAIT_TICKS := 15
const WAIT_AFTER_PRESS := 3

var lord_id := 0
var mission := 0
var lines: Array = []  # the advice and the hero's answer, "[Speaker] text"
var line_at := 0
@onready var lord_portrait: TextureRect = %Dialogue.speaker_portrait
@onready var hero_portrait: TextureRect = %Dialogue.hero_portrait
@onready var lord_says: Label = %Dialogue.speaker_says
@onready var hero_says: Label = %Dialogue.hero_says
var typing: Label  # the box being typed
@onready var skip: Button = %Skip
var _typed := 0.0
var _wait := -1.0  # seconds before the next line once this one is shown, -1 while typing
var _done := false


func _ready() -> void:
	var p: Dictionary = Router.params
	lord_id = int(p.get("lord", 0))
	mission = int(p.get("mission", 0))
	var profile := Profile.load_or_new(str(p.get("profile_path", Profile.PATH)))
	var ms := Campaign.new().lord_missions(lord_id)
	var m: Dictionary = ms[mission] if mission >= 0 and mission < ms.size() else {}
	lines = talk(int(p.get("line", 0)), tr(str(m.get("name", ""))), profile.hero_name)

	lord_portrait.texture = Pictures.portrait(int(m.get("portrait", 0)))
	hero_portrait.texture = Pictures.portrait(Stories.HERO_PORTRAIT + int(profile.head))

	_show_line()


## The two lines of the briefing from `line` of talk.json "briefing": the advice of `speaker`
## and the answer of `hero`, each "[Name] text".
static func talk(line: int, speaker: String, hero: String) -> Array:
	var all := MapSim.talk_lines("briefing")
	var out: Array = []
	for k in 2:
		var who := speaker if k == 0 else hero
		var i := line + k
		var text := I18n.text(all[i]) if i >= 0 and i < all.size() else ""
		out.append("[%s] %s" % [who, text.replace("&", who)])
	return out


## Types lines[line_at] into its box: the advice at the top, the answer at the bottom.
func _show_line() -> void:
	typing = lord_says if line_at == 0 else hero_says
	typing.text = str(lines[line_at])
	typing.visible_characters = 0
	_typed = 0.0
	_wait = -1.0


## Attack / accept / a click: the whole line, or the next one at once.
func press() -> void:
	if _done:
		return
	if _wait < 0.0:
		typing.visible_characters = -1
		_wait = WAIT_AFTER_PRESS * Settings.tick_seconds()
	else:
		next_line()


func next_line() -> void:
	line_at += 1
	if line_at < lines.size():
		_show_line()
	else:
		finish()


## The briefing is over (or skipped): the mission, in its place.
func finish() -> void:
	if _done:
		return
	_done = true
	set_process(false)
	Router.replace("mission", {"lord": lord_id, "mission": mission})


func _process(delta: float) -> void:
	if _done:
		return
	if _wait >= 0.0:
		_wait -= delta
		if _wait < 0.0:
			next_line()
		return
	_typed += delta * CHARS_PER_SECOND
	typing.visible_characters = mini(int(_typed), typing.text.length())
	if typing.visible_characters >= typing.text.length():
		typing.visible_characters = -1
		_wait = WAIT_TICKS * Settings.tick_seconds()


func go_back() -> void:
	finish()


func _screen_input(event: InputEvent) -> void:
	if event.is_action_pressed("skip"):
		get_viewport().set_input_as_handled()
		finish()
	elif event.is_action_pressed("attack") or event.is_action_pressed("ui_accept"):
		get_viewport().set_input_as_handled()
		press()


## A click beside Skip, as attack (in a window the screen itself takes the click).
func _gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		accept_event()
		press()


## The line of control hints under the screen (scripts/ui/hint_bar.gd).
func controls_hint() -> String:
	return InputSetup.hint("hint.skip")
