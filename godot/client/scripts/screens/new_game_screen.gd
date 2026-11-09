extends Control
## A new game, step by step as in the original: the difficulty (Normal first: x1 gold and exp,
## the hero turns to the nearest enemy as he strikes and AUTO hunts; Hard: x2, neither; it
## cannot change later), the
## hero's face (each face a hero with his own base stats), his name (up to 8 letters, typed or
## on the keys under the field, scripts/ui/key_grid.gd), and his
## 5 first stat points ("+" beside a stat puts a point in it; Reset gives them back, Done
## asks to go on once all are spent). Every step has Back. Then the hero is saved over
## any old one and the opening story starts, then the game menu.
## Params: profile_path (optional), then (the screen after the opening, default game_menu).

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Stories := preload("res://scripts/core/stories.gd")
const KeyGrid := preload("res://scripts/ui/key_grid.gd")
const AskDialog := preload("res://scripts/ui/ask_dialog.gd")
const Pictures := preload("res://scripts/ui/pictures.gd")
const HEADS := 4
const NAME_MAX := 8
const SCALE := 3
const STAT_KEYS := ["hp", "mp", "attack", "defense"]
enum Step { DIFFICULTY, HERO, NAME, POINTS }

var path: String = Profile.PATH
var profile: RefCounted = Profile.new()
var step := Step.DIFFICULTY
var heading: Label
var body: VBoxContainer
var info: Label
var ask: AskDialog
var name_edit: LineEdit
var stat_buttons: Array[Button] = []  # the "+" of each stat
var stat_values: Array[Label] = []
var points_label: Label
var points_hint: Label
var reset_button: Button
var done_button: Button


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	var col := UiTheme.menu_column(self, 640)
	heading = UiTheme.heading("newgame.difficulty", 40)
	col.add_child(heading)
	body = VBoxContainer.new()
	body.name = "Body"
	body.add_theme_constant_override("separation", 10)
	col.add_child(body)
	info = Label.new()
	info.name = "Info"
	info.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	info.custom_minimum_size = Vector2(0, 80)
	col.add_child(info)
	ask = AskDialog.new()
	ask.confirmed.connect(_confirmed)
	add_child(ask)
	show_step(Step.DIFFICULTY)


func _clear() -> void:
	for c in body.get_children():
		body.remove_child(c)
		c.queue_free()
	stat_buttons.clear()
	stat_values.clear()
	info.text = ""
	points_hint = null
	reset_button = null
	done_button = null


func _button(
	node_name: String, text: String, on_press: Callable, translate := true, parent: Node = null
) -> Button:
	var b := Button.new()
	b.name = node_name
	b.text = text
	if not translate:
		b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	b.pressed.connect(on_press)
	(body if parent == null else parent).add_child(b)
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


func show_step(s: int) -> void:
	step = s
	_clear()
	match step:
		Step.DIFFICULTY:
			heading.text = "newgame.difficulty"
			for d in [1, 0]:  # Normal first, as most will play it
				var b := _button(
					"Difficulty%d" % d, "newgame.difficulty_%d" % d, choose_difficulty.bind(d)
				)
				b.focus_entered.connect(func(): info.text = tr("newgame.mode_%d" % d))
				b.mouse_entered.connect(func(): info.text = tr("newgame.mode_%d" % d))
			_button("Back", "common.back", go_back)
			(body.get_child(0) as Button).grab_focus.call_deferred()
			info.text = tr("newgame.mode_1")
		Step.HERO:
			heading.text = "newgame.hero"
			var row := HBoxContainer.new()
			row.name = "Heads"
			row.alignment = BoxContainer.ALIGNMENT_CENTER
			row.add_theme_constant_override("separation", 24)
			for h in HEADS:
				var b := Button.new()
				b.name = "Head%d" % h
				b.custom_minimum_size = Vector2(46, 46) * SCALE + Vector2(12, 12)
				var face := Pictures.framed("Portrait", Vector2(46, 46) * SCALE)
				face.texture = Pictures.portrait(Stories.HERO_PORTRAIT + h)
				face.mouse_filter = Control.MOUSE_FILTER_IGNORE
				face.set_anchors_and_offsets_preset(
					Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 6
				)
				b.add_child(face)
				b.pressed.connect(choose_head.bind(h))
				b.focus_entered.connect(show_class.bind(h))
				b.mouse_entered.connect(show_class.bind(h))
				row.add_child(b)
			body.add_child(row)
			_button("Back", "common.back", go_back)
			show_class(profile.head)
			(row.get_child(profile.head) as Button).grab_focus.call_deferred()
		Step.NAME:
			heading.text = "newgame.name"
			name_edit = LineEdit.new()
			name_edit.name = "Name"
			name_edit.max_length = NAME_MAX
			name_edit.alignment = HORIZONTAL_ALIGNMENT_CENTER
			name_edit.placeholder_text = tr("newgame.name_hint")
			name_edit.keep_editing_on_text_submit = true  # an empty name refused: it still types
			name_edit.text_submitted.connect(func(_t): submit_name())
			name_edit.text_changed.connect(_name_changed)
			body.add_child(name_edit)
			body.add_child(KeyGrid.create(KeyGrid.LETTERS, name_edit))
			_button("Ok", "newgame.ok", submit_name)
			_button("Back", "common.back", go_back)
			name_edit.grab_focus.call_deferred()
		Step.POINTS:
			heading.text = "newgame.points"
			points_label = Label.new()
			points_label.name = "Points"
			points_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			points_label.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
			body.add_child(points_label)
			for i in 4:
				# as on the Attributes screen: the stat, its value and "+" that puts a point in it
				var row := HBoxContainer.new()
				var l := Label.new()
				l.text = "attributes." + STAT_KEYS[i]
				l.size_flags_horizontal = Control.SIZE_EXPAND_FILL
				row.add_child(l)
				var v := Label.new()
				v.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
				v.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
				v.custom_minimum_size = Vector2(120, 0)
				row.add_child(v)
				stat_values.append(v)
				var b := Button.new()
				b.name = "Stat%d" % i
				b.text = "+"
				b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
				b.custom_minimum_size = Vector2(56, 0)
				b.pressed.connect(spend.bind(i))
				row.add_child(b)
				stat_buttons.append(b)
				body.add_child(row)
			points_hint = UiTheme.note("PointsHint")
			points_hint.add_theme_color_override("font_color", UiTheme.TEXT_DIM)
			body.add_child(points_hint)
			var actions := HBoxContainer.new()
			actions.name = "Actions"
			actions.alignment = BoxContainer.ALIGNMENT_CENTER
			actions.add_theme_constant_override("separation", 12)
			body.add_child(actions)
			reset_button = _button("Reset", "newgame.reset", reset_points, true, actions)
			done_button = _button("Done", "newgame.done", ask_done, true, actions)
			_button("Back", "common.back", go_back, true, actions)
			for b in actions.get_children():
				b.custom_minimum_size = Vector2(180, 0)
			_refresh_points()
			stat_buttons[0].grab_focus.call_deferred()


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
			Profile.stats_line(h)
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
	var fresh: RefCounted = Profile.new()
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


## Saves the new hero over the old one and starts the opening story, then the training
## (training_screen.gd), then `then` (the game menu).
func finish() -> void:
	profile.save(path)
	var then := str(Router.params.get("then", "camp"))
	Router.back()
	Router.push(
		"story",
		{
			"story": Stories.OPENING,
			"then": "training",
			"then_params":
			{
				"then": then,
				"then_params": {"first": true, "profile_path": path},
				"profile_path": path
			},
			"profile_path": path
		}
	)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		go_back()
