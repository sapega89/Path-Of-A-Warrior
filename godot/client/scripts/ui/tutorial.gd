extends Control
## The training's steps (scripts/screens/training_screen.gd), one hint at a time at the top of
## the map, under the clock. A step waits for what it asks, then the next one starts by itself:
##   MOVE    walk a couple of cells
##   ATTACK  a soldier comes in: kill him
##   LOOT    he dropped something: walk over it (8 s at most; no step when nothing dropped)
##   SKILL   MP full, two more: use the skill on key 1 and kill them (no step without a skill)
##   POTION  HP at a third, a red potion on the first belt slot: drink it
##   AUTO    three more: turn on the auto-hunt and let it fight (not on hard, it has no AUTO)
##   EXIT    the room is cleared: walk out through the blinking arrow
##   PAUSE   in the next room: pause (8 s at most)
##   DONE    "Training complete!": OK, or 5 s, and `finished`
## The hints name the keys of the device in use (InputSetup.hint: "training.attack" says J after
## the keyboard, A after an Xbox pad, the big button on a phone) and change when it changes.
## The hero cannot lose here: below a quarter of his HP he is healed to half.

signal finished

const UiTheme := preload("res://scripts/ui/ui_theme.gd")

enum Step { MOVE, ATTACK, LOOT, SKILL, POTION, AUTO, EXIT, PAUSE, DONE }
const KEYS := ["training.move", "training.attack", "training.loot", "training.skill",
	"training.potion", "training.auto", "training.exit", "training.pause", "training.done"]
const WALK_PX := 54  # two cells
const LOOT_WAIT := 8.0
const PAUSE_WAIT := 8.0
const DONE_WAIT := 5.0
const POTION := 1  # the small red potion (30 % HP)
const TOP := 64  # px from the top: under the clock's box

var screen: Control  # the training screen: its sim, autopilot and pause menu
var step := Step.MOVE
var panel: PanelContainer  # the hint's box, in the middle of the top
var label: Label
var _t := 0.0  # seconds of play in this step
var _from := Vector2i.ZERO  # MOVE: where the hero stood
var _done_it := false  # SKILL: a skill used; AUTO: the auto-hunt turned on
var _cell := 0  # EXIT: the room to leave
var _over := false


func _ready() -> void:
	name = "Tutorial"
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	offset_top = TOP
	var center := CenterContainer.new()
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	center.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	add_child(center)
	panel = PanelContainer.new()
	panel.name = "Panel"
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var sb := UiTheme.box(Color(UiTheme.PANEL, 0.92), UiTheme.ACCENT, 2)
	sb.set_content_margin_all(12)
	sb.content_margin_left = 24
	sb.content_margin_right = 24
	panel.add_theme_stylebox_override("panel", sb)
	center.add_child(panel)
	label = Label.new()
	label.name = "Text"
	label.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED  # InputSetup.hint translates
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.add_theme_font_size_override("font_size", 24)
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.add_child(label)
	InputSetup.device_changed.connect(_on_device_changed)
	begin(Step.MOVE)


func _exit_tree() -> void:
	if InputSetup.device_changed.is_connected(_on_device_changed):
		InputSetup.device_changed.disconnect(_on_device_changed)


## The hint of the step, for the device in use.
func text() -> String:
	return InputSetup.hint(KEYS[step])


## Starts a step: what it needs on the map, and its hint. A step that has nothing to teach
## here (no loot, no skill on key 1, no AUTO on hard) goes on to the next one.
func begin(s: Step) -> void:
	step = s
	_t = 0.0
	_done_it = false
	var sim: RefCounted = screen.sim
	match s:
		Step.MOVE:
			_from = sim.hero.pos
		Step.ATTACK:
			_send(1)
		Step.LOOT:
			if sim.drops.is_empty():
				begin(Step.SKILL)
				return
		Step.SKILL:
			if int(sim.hotkeys[0]) == 0:
				begin(Step.POTION)
				return
			sim.hero.mp = sim.hero.max_mp
			_send(2)
		Step.POTION:
			sim.quick_slots[0] = [POTION, 1]
			sim.hero.hp = maxi(1, sim.hero.max_hp / 3)
		Step.AUTO:
			if not screen.auto_allowed():
				begin(Step.EXIT)
				return
			_send(3)
		Step.EXIT:
			if screen.autopilot.on:
				screen.toggle_auto()  # the player walks out himself
			sim.hold_room = false
			sim.no_enemies = true  # the next rooms are empty
			sim.clear_room()
			_cell = sim.cell
	label.text = text()


func _send(n: int) -> void:
	screen.sim.send_soldiers(n)


## All of this step's soldiers came in and are dead (a squad of three is one of them).
func _fought() -> bool:
	return int(screen.sim.waves[0]) == 0 and screen.sim.enemies_alive == 0


func _process(delta: float) -> void:
	if _over or screen == null or screen.sim == null:
		return
	if screen.pause_menu != null:
		if step == Step.PAUSE:
			begin(Step.DONE)
		return
	_t += delta
	_heal()
	check()


## The step's end: the next step when the player did what it asked.
func check() -> void:
	var sim: RefCounted = screen.sim
	match step:
		Step.MOVE:
			if Vector2(sim.hero.pos - _from).length() >= WALK_PX:
				begin(Step.ATTACK)
		Step.ATTACK:
			if _fought():
				begin(Step.LOOT)
		Step.LOOT:
			if sim.drops.is_empty() or _t >= LOOT_WAIT:
				begin(Step.SKILL)
		Step.SKILL:
			if sim.hero.mp < sim.hero.max_mp:
				_done_it = true
			if _fought():
				if _done_it:
					begin(Step.POTION)
				else:  # all beaten by the sword: one more, MP full again
					sim.hero.mp = sim.hero.max_mp
					_send(1)
		Step.POTION:
			if int(sim.quick_slots[0][1]) < 1:
				begin(Step.AUTO)
		Step.AUTO:
			if screen.autopilot.on:
				_done_it = true
			if _fought():
				if _done_it:
					begin(Step.EXIT)
				else:
					_send(1)
		Step.EXIT:
			if sim.cell != _cell and not sim.scrolling:
				begin(Step.PAUSE)
		Step.PAUSE:
			if _t >= PAUSE_WAIT:
				begin(Step.DONE)
		Step.DONE:
			if _t >= DONE_WAIT:
				finish()


## Nobody loses the training: below a quarter of his HP the hero is healed to half.
func _heal() -> void:
	var hero = screen.sim.hero
	if hero.hp > 0 and hero.hp < hero.max_hp / 4:
		hero.hp = hero.max_hp / 2


func finish() -> void:
	if _over:
		return
	_over = true
	finished.emit()


func _unhandled_input(event: InputEvent) -> void:
	if step == Step.DONE and not _over and screen.pause_menu == null \
			and (event.is_action_pressed("ui_accept") or event.is_action_pressed("attack")):
		get_viewport().set_input_as_handled()
		finish()


func _on_device_changed(_device: String) -> void:
	label.text = text()
