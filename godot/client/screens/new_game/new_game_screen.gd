class_name NewGameScreen
extends BaseScreen
## A new game, step by step as in the original: the difficulty (Normal first: x1 gold and exp,
## the hero turns to the nearest enemy as he strikes and AUTO hunts; Hard: x2, neither; it
## cannot change later), the
## hero's face (each face a hero with his own base stats), his name (up to 8 letters, typed or
## on the keys under the field, scripts/ui/key_grid.gd), and his
## 5 first stat points ("+" beside a stat puts a point in it; Reset gives them back, Done
## asks to go on once all are spent). Every step has Back. Then the hero is saved over
## any old one and the opening story starts, then the game menu.
## Params: profile_path (optional), then (the screen after the opening, default game_menu).

enum Step { DIFFICULTY, HERO, NAME, POINTS }

const HEADS := 4
const NAME_MAX := 8
const SCALE := 3
const STAT_KEYS := ["hp", "mp", "attack", "defense"]

var path: String = Profile.PATH
var profile := Profile.new()
var step := Step.DIFFICULTY
var ask: AskDialog
var stat_buttons: Array[Button] = []  # the "+" of each stat
var stat_values: Array[Label] = []

@onready var heading: Label = %Heading
@onready var body: VBoxContainer = %DifficultyPage  # the page of this step
@onready var info: Label = %Info
@onready var name_edit: LineEdit = %Name
@onready var points_label: Label = %Points
@onready var points_hint: Label = %PointsHint
@onready var reset_button: Button = %Reset
@onready var done_button: Button = %Done
## Each step's page and heading.
@onready var pages := {
	Step.DIFFICULTY: [%DifficultyPage, "newgame.difficulty"],
	Step.HERO: [%HeroPage, "newgame.hero"],
	Step.NAME: [%NamePage, "newgame.name"],
	Step.POINTS: [%PointsPage, "newgame.points"],
}


func _ready() -> void:
	path = profile_path()
	for h in HEADS:
		%Heads.add_child(_head_button(h))
	name_edit.add_sibling(KeyGrid.create(KeyGrid.LETTERS, name_edit))
	for i in STAT_KEYS.size():
		stat_buttons.append(%PointsPage.get_node("Row%d/Stat%d" % [i, i]))
		stat_values.append(%PointsPage.get_node("Row%d/Value" % i))
	ask = AskDialog.new()
	ask.confirmed.connect(_confirmed)
	add_child(ask)
	show_step(Step.DIFFICULTY)


## The button of face h: the hero's portrait in its frame.
func _head_button(h: int) -> Button:
	var b := Button.new()
	b.name = "Head%d" % h
	b.custom_minimum_size = Vector2(46, 46) * SCALE + Vector2(12, 12)
	var face := Pictures.framed("Portrait", Vector2(46, 46) * SCALE)
	face.texture = Pictures.portrait(Stories.HERO_PORTRAIT + h)
	face.mouse_filter = Control.MOUSE_FILTER_IGNORE
	face.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 6)
	b.add_child(face)
	b.pressed.connect(choose_head.bind(h))
	b.focus_entered.connect(show_class.bind(h))
	b.mouse_entered.connect(show_class.bind(h))
	return b


## The line of control hints under the screen (scripts/ui/hint_bar.gd), for this step.
func controls_hint() -> String:
	match step:
		Step.NAME:
			return InputSetup.hint("hint.new_name")
		Step.POINTS:
			return InputSetup.hint("hint.new_points")
	return InputSetup.hint("hint.menu")


## Back, as BACK (Esc, B, the right button): the step before, or out of a new game.
func go_back() -> void:
	match step:
		Step.DIFFICULTY:
			Router.back()
		Step.POINTS:  # the points back, then the name again
			reset_points()
			show_step(Step.NAME)
		_:
			show_step(step - 1)


## Shows the page of step s, as it is at its start.
func show_step(s: int) -> void:
	step = s
	for p in pages.values():
		p[0].visible = false
	body = pages[step][0]
	body.visible = true
	heading.text = pages[step][1]
	info.text = ""
	match step:
		Step.DIFFICULTY:
			(body.get_child(0) as Button).grab_focus.call_deferred()
			info.text = tr("newgame.mode_1")
		Step.HERO:
			show_class(profile.head)
			(%Heads.get_child(profile.head) as Button).grab_focus.call_deferred()
		Step.NAME:
			name_edit.text = ""
			name_edit.grab_focus.call_deferred()
		Step.POINTS:
			_refresh_points()
			stat_buttons[0].grab_focus.call_deferred()


## Under a difficulty: what it means.
func _show_mode(d: int) -> void:
	info.text = tr("newgame.mode_%d" % d)


func choose_difficulty(d: int) -> void:
	profile.difficulty = d
	_ask("newgame.ask_difficulty")


## Under the faces: the hint, and the hero of face h with his base stats.
func show_class(h: int) -> void:
	info.text = (
		"%s\n%s\n\n%s\n%s"
		% [
			tr("newgame.select_1"),
			tr("newgame.select_2"),
			tr(Profile.HERO_CLASSES[h]),
			Attributes.stats_line(h)
		]
	)


func choose_head(h: int) -> void:
	profile.set_head(h)
	show_step(Step.NAME)


## Only letters, as many as fit.
func _name_changed(t: String) -> void:
	var clean := ""
	for c in t:
		if (c >= "A" and c <= "Z") or (c >= "a" and c <= "z"):
			clean += c
	if clean != t:
		var at := name_edit.caret_column
		name_edit.text = clean
		name_edit.caret_column = mini(at, clean.length())


func _name_submitted(_t: String) -> void:
	submit_name()


func submit_name() -> bool:
	var n := name_edit.text.strip_edges()
	if n.is_empty():
		info.text = tr("newgame.name_empty")
		return false
	profile.hero_name = n
	show_step(Step.POINTS)
	return true


func spend(stat: int) -> void:
	if profile.spend_point(stat):
		_refresh_points()
		if profile.stat_points == 0:
			done_button.grab_focus()
			ask_done()


## Gives the points back: the hero of the chosen face again, with his name.
func reset_points() -> void:
	var fresh := Profile.new()
	fresh.difficulty = profile.difficulty
	fresh.set_head(profile.head)
	fresh.hero_name = profile.hero_name
	profile = fresh
	if step == Step.POINTS:
		_refresh_points()
		stat_buttons[0].grab_focus()


## Done: asks to go on with the hero (only once every point is spent).
func ask_done() -> void:
	if profile.stat_points == 0:
		_ask("newgame.ask_done")


func _refresh_points() -> void:
	points_label.text = tr("newgame.points_left") % profile.stat_points
	var values := [profile.base_hp, profile.base_mp, profile.base_attack, profile.base_defense]
	for i in stat_buttons.size():
		stat_values[i].text = str(values[i])
		stat_buttons[i].disabled = profile.stat_points == 0
	var left: int = profile.stat_points
	points_hint.text = tr("newgame.points_spent") if left == 0 else tr("newgame.points_hint")
	done_button.disabled = left > 0
	reset_button.disabled = left == Profile.START_POINTS


func _ask(key: String) -> void:
	ask.dialog_text = tr(key)
	ask.popup_centered()


func _confirmed() -> void:
	match step:
		Step.DIFFICULTY:
			show_step(Step.HERO)
		Step.POINTS:
			finish()


## Saves the new hero over the old one and starts the opening story, then `then`: the camp,
## which starts the first mission at once.
func finish() -> void:
	profile.save(path)
	var then := str(Router.params.get("then", "camp"))
	Router.back()
	Router.push(
		"story",
		{
			"story": Stories.OPENING,
			"then": then,
			"then_params": {"first": true, "profile_path": path},
			"profile_path": path
		}
	)
