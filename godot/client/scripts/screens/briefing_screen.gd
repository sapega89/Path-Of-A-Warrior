extends Control
## The briefing of an accepted mission: the one who gives it (the mission's portrait, at the
## top) advises the hero and the hero (at the bottom) answers. Each line is typed out into its
## box and stays there; a line typed out goes on by itself after a moment. Attack / accept or a
## click shows the whole line, or goes on at once; back or SKIP (Q, F1, the pad's Back, the
## Skip button) goes straight to the map. The mission then takes the briefing's place, so back
## from the mission goes to the campaign.
## Params: lord, mission, line (the advice's line of talk.json "briefing", the hero answers
## with the next one), profile_path.

const Profile := preload("res://scripts/core/profile.gd")
const Campaign := preload("res://scripts/core/campaign.gd")
const Stories := preload("res://scripts/core/stories.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")
const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const PORTRAITS := "res://assets/original/portraits/%d.png"
const SCALE := 3
const CHARS_PER_SECOND := 40.0
## Ticks a typed line stays before the next one, and after a press that showed it whole.
const WAIT_TICKS := 15
const WAIT_AFTER_PRESS := 3

var lord_id := 0
var mission := 0
var lines: Array = []  # the advice and the hero's answer, "[Speaker] text"
var line_at := 0
var lord_portrait: TextureRect
var hero_portrait: TextureRect
var lord_says: Label
var hero_says: Label
var typing: Label  # the box being typed
var skip: Button
var _typed := 0.0
var _wait := -1.0  # seconds before the next line once this one is shown, -1 while typing
var _done := false


func _ready() -> void:
	var p: Dictionary = Router.params
	lord_id = int(p.get("lord", 0))
	mission = int(p.get("mission", 0))
	var profile: RefCounted = Profile.load_or_new(str(p.get("profile_path", Profile.PATH)))
	var ms := Campaign.new().lord_missions(lord_id)
	var m: Dictionary = ms[mission] if mission >= 0 and mission < ms.size() else {}
	lines = talk(int(p.get("line", 0)), tr(str(m.get("name", ""))), profile.hero_name)

	var col := UiTheme.menu_column(self, 760)
	col.add_theme_constant_override("separation", 12)
	var top := HBoxContainer.new()
	top.add_theme_constant_override("separation", 16)
	lord_portrait = _portrait("LordPortrait")
	lord_says = _speech("LordSays")
	top.add_child(lord_portrait)
	top.add_child(lord_says)
	col.add_child(top)
	var bottom := HBoxContainer.new()
	bottom.add_theme_constant_override("separation", 16)
	hero_says = _speech("HeroSays")
	hero_portrait = _portrait("HeroPortrait")
	bottom.add_child(hero_says)
	bottom.add_child(hero_portrait)
	col.add_child(bottom)
	lord_portrait.texture = load(PORTRAITS % int(m.get("portrait", 0)))
	hero_portrait.texture = load(PORTRAITS % (Stories.HERO_PORTRAIT + int(profile.head)))

	skip = Button.new()
	skip.name = "Skip"
	skip.text = "common.skip"
	skip.flat = true
	skip.focus_mode = Control.FOCUS_NONE
	skip.set_anchors_preset(Control.PRESET_BOTTOM_LEFT)
	skip.position = Vector2(12, -60)
	skip.pressed.connect(finish)
	add_child(skip)
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


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel") or event.is_action_pressed("skip"):
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
