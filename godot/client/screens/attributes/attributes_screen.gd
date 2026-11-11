class_name AttributesScreen
extends BaseScreen
## Attributes: the hero's name, level, fame and free stat points, and HP, MP, attack and
## defence, each with a "+" that spends a point on it (HP +5, MP +3, attack +1, defence +1).
## Attack and defence show the hero's own part and the gear's part ("4+1").
## Every point spent is saved at once. Reset gives the points back: the base stats go back to
## the hero's face, paid with 100 gold per level or an elixir (St John's Wort / Cornflower Tincture,
## Rapids / Forest Remedy). Points are spent and reset only in the start camp (HeroRun.at_start):
## elsewhere they wait, and a note says so.

## Stat row name, text key, Profile.Stat.
const STATS := [
	["HP", "attributes.hp", Profile.Stat.HP],
	["MP", "attributes.mp", Profile.Stat.MP],
	["ATK", "attributes.attack", Profile.Stat.ATTACK],
	["DEF", "attributes.defense", Profile.Stat.DEFENSE],
]

var profile: Profile
var path: String = Profile.PATH
var values := {}  # row name -> its value Label
var plus := {}  # stat row name -> its "+" Button
var pay_item: Button

@onready var reset: Button = %Reset
@onready var start_only: Label = %StartOnly  # the points wait for the start camp
@onready var ask: ConfirmationDialog = %Ask  # pay with gold (OK), an elixir ("item") or cancel
@onready var note: AcceptDialog = %Note


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	for row in ["Name", "Level", "Fame", "Points"] + STATS.map(func(s): return s[0]):
		values[row] = %Column.get_node(row + "/Value")
	for s in STATS:
		plus[s[0]] = %Column.get_node("%s/Plus%s" % [s[0], s[0]])
	pay_item = ask.add_button("", false, "item")
	refresh()
	%Back.grab_focus.call_deferred()
	for s in STATS:
		if not plus[s[0]].disabled:
			plus[s[0]].grab_focus.call_deferred()
			break


## Spends a point on the stat and saves the hero. False when no point is left.
func spend(stat: int) -> bool:
	if not HeroRun.at_start(profile) or not profile.spend_point(stat):
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
	var here := HeroRun.at_start(profile)
	for b in plus.values():
		b.disabled = profile.stat_points <= 0 or not here
	reset.disabled = not here
	start_only.visible = not here


func _on_pay_gold() -> void:
	finish_reset(false)


func _on_pay_item(_action: StringName) -> void:
	ask.hide()
	finish_reset(true)


## Asks how to pay for the reset; says so when there is nothing to reset.
func open_reset() -> void:
	if Attributes.spent_points(profile) == 0:
		_note(tr("attributes.reset_nothing"))
		return
	ask.dialog_text = tr("attributes.reset_ask") % Attributes.spent_points(profile)
	ask.ok_button_text = tr("attributes.pay_gold") % Attributes.reset_gold(profile)
	var slot: int = Attributes.reset_elixir_slot(profile)
	pay_item.disabled = slot < 0
	pay_item.text = (
		tr("attributes.no_elixir")
		if slot < 0
		else tr("attributes.use_item") % Items.name_of(int(profile.backpack[slot].id))
	)
	ask.popup_centered()


## Resets, paid with gold or an elixir, saves and says how it went. Returns the line said.
func finish_reset(by_item: bool) -> String:
	var free: int = Attributes.spent_points(profile)
	var why: String = Attributes.reset(profile, by_item)
	var said := (
		tr("attributes.reset_done") % free if why.is_empty() else tr("attributes.reset_" + why)
	)
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
