extends Control
## Attributes: the hero's name, level, fame and free stat points, and HP, MP, attack and
## defence, each with a "+" that spends a point on it (HP +5, MP +3, attack +1, defence +1).
## Attack and defence show the hero's own part and the gear's part ("4+1").
## Every point spent is saved at once. Reset gives the points back: the base stats go back to
## the hero's face, paid with 100 gold per level or an elixir (St John's Wort / Cornflower Tincture,
## Rapids / Forest Remedy).

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Items := preload("res://scripts/core/items.gd")
## Stat row name, text key, Profile.Stat.
const STATS := [
	["HP", "attributes.hp", Profile.Stat.HP],
	["MP", "attributes.mp", Profile.Stat.MP],
	["ATK", "attributes.attack", Profile.Stat.ATTACK],
	["DEF", "attributes.defense", Profile.Stat.DEFENSE],
]

var profile: RefCounted
var path: String = Profile.PATH
var values := {}  # row name -> its value Label
var plus := {}  # stat row name -> its "+" Button
var reset: Button
var ask: ConfirmationDialog  # pay with gold (OK), an elixir ("item") or cancel
var pay_item: Button
var note: AcceptDialog


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	profile = Profile.load_or_new(path)
	var col := UiTheme.menu_column(self, 520)
	col.add_child(UiTheme.heading("attributes.title", 44))
	_row(col, "Name", "attributes.name")
	_row(col, "Level", "attributes.level")
	_row(col, "Fame", "attributes.fame")
	_row(col, "Points", "attributes.points")
	for s in STATS:
		var b := Button.new()
		b.name = "Plus" + s[0]
		b.text = "+"
		var stat: int = s[2]
		b.pressed.connect(func(): spend(stat))
		_row(col, s[0], s[1], b)
		plus[s[0]] = b
	reset = Button.new()
	reset.name = "Reset"
	reset.text = "attributes.reset"
	reset.pressed.connect(open_reset)
	col.add_child(reset)
	ask = ConfirmationDialog.new()
	ask.name = "Ask"
	ask.confirmed.connect(func(): finish_reset(false))
	ask.custom_action.connect(func(_a): ask.hide(); finish_reset(true))
	pay_item = ask.add_button("", false, "item")
	add_child(ask)
	note = AcceptDialog.new()
	note.name = "Note"
	add_child(note)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	refresh()
	back.grab_focus.call_deferred()
	for s in STATS:
		if not plus[s[0]].disabled:
			plus[s[0]].grab_focus.call_deferred()
			break


## Spends a point on the stat and saves the hero. False when no point is left.
func spend(stat: int) -> bool:
	if not profile.spend_point(stat):
		return false
	profile.save(path)
	refresh()
	return true


func refresh() -> void:
	values["Name"].text = profile.hero_name
	values["Level"].text = str(profile.level)
	values["Fame"].text = str(profile.fame)
	values["Points"].text = str(profile.stat_points)
	values["HP"].text = str(profile.max_hp())
	values["MP"].text = str(profile.max_mp())
	values["ATK"].text = _with_gear(profile.base_attack, profile.attack())
	values["DEF"].text = _with_gear(profile.base_defense, profile.defense())
	for b in plus.values():
		b.disabled = profile.stat_points <= 0


## Asks how to pay for the reset; says so when there is nothing to reset.
func open_reset() -> void:
	if profile.spent_points() == 0:
		_note(tr("attributes.reset_nothing"))
		return
	ask.dialog_text = tr("attributes.reset_ask") % profile.spent_points()
	ask.ok_button_text = tr("attributes.pay_gold") % profile.respec_gold()
	var slot: int = profile.respec_item_slot()
	pay_item.disabled = slot < 0
	pay_item.text = tr("attributes.no_elixir") if slot < 0 else tr("attributes.use_item") % Items.name_of(int(profile.backpack[slot].id))
	ask.popup_centered()


## Resets, paid with gold or an elixir, saves and says how it went. Returns the line said.
func finish_reset(by_item: bool) -> String:
	var free: int = profile.spent_points()
	var why: String = profile.respec(by_item)
	var said := tr("attributes.reset_done") % free if why.is_empty() else tr("attributes.reset_" + why)
	if why.is_empty():
		profile.save(path)
		refresh()
	_note(said)
	return said


func _note(text: String) -> void:
	note.dialog_text = text
	note.popup_centered()


## "4+1" when the gear adds to the hero's own number, else just the number.
static func _with_gear(own: int, total: int) -> String:
	return str(own) if total == own else "%d+%d" % [own, total - own]


func _row(col: VBoxContainer, row_name: String, label_key: String, button: Button = null) -> void:
	var row := HBoxContainer.new()
	row.name = row_name
	var l := Label.new()
	l.text = label_key
	l.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(l)
	var v := Label.new()
	v.name = "Value"
	v.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	v.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	v.custom_minimum_size = Vector2(120, 0)
	row.add_child(v)
	values[row_name] = v
	if button != null:
		button.custom_minimum_size = Vector2(56, 0)
		row.add_child(button)
	col.add_child(row)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
