class_name SkillsScreen
extends BaseScreen
## Skills: the five skill keys and the skills by group (MOVE, HEAL, PASV, FWD, NEAR, RANGE,
## WHOLE). A learned skill has its coloured icon, one not yet learned its grey icon.
## Pick a key, then a learned skill to put it on that key; picking a key that holds a skill
## takes the skill off. Beside the groups, the card of the skill under the cursor: name and
## level, what it is, MP and what it does now and at the next level.
## Every change is saved at once.

const SKILLS_PATH := "res://data/skills.json"
const KEY_COUNT := 5
const KEY_SCENE := preload("res://screens/skills/skill_key.tscn")
const ROW_SCENE := preload("res://screens/skills/skill_row.tscn")
const LINE_SCENE := preload("res://screens/skills/card_line.tscn")

var profile: Profile
var path: String = Profile.PATH
var data: Dictionary = {}
var slot := 0  # the skill key being set
var keys: Array[Button] = []
var skills := {}  # skill id -> its Button
var info: Label  # the card's heading line (name and level)
@onready var card: VBoxContainer = %Lines


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	data = load_data()
	for i in KEY_COUNT:
		_add_key(i)
	var groups: Array = data.get("groups", [])
	var rows: Array = data.get("rows", [])
	for r in rows.size():
		_add_row(str(groups[r]) if r < groups.size() else "", rows[r])
	refresh()
	_show_info(int(profile.hotkeys[0]))
	keys[0].grab_focus.call_deferred()


## Skill key i (skill_key.tscn): its keyboard key above its place.
func _add_key(i: int) -> void:
	var cell: Control = KEY_SCENE.instantiate()
	(cell.get_node("Key") as Label).text = key_name(i)
	var b: Button = cell.get_node("Slot")
	b.name = "Key%d" % (i + 1)
	b.pressed.connect(press_key.bind(i))
	b.focus_entered.connect(func(): _show_info(int(profile.hotkeys[i])))
	b.mouse_entered.connect(func(): _show_info(int(profile.hotkeys[i])))
	%Keys.add_child(cell)
	keys.append(b)


## A group's row (skill_row.tscn): its name, then its skills (0: an empty place).
func _add_row(group: String, ids: Array) -> void:
	var row: Control = ROW_SCENE.instantiate()
	(row.get_node("Group") as Label).text = group
	for id in ids:
		var skill := int(id)
		var b := ItemSlot.button("Skill%d" % skill)
		if skill == 0:
			b.disabled = true
			b.focus_mode = Control.FOCUS_NONE
		else:
			b.pressed.connect(press_skill.bind(skill))
			b.focus_entered.connect(_show_info.bind(skill))
			b.mouse_entered.connect(_show_info.bind(skill))
			skills[skill] = b
		row.add_child(b)
	%Groups.add_child(row)


static func load_data() -> Dictionary:
	var f := FileAccess.open(SKILLS_PATH, FileAccess.READ)
	if f == null:
		return {}
	var d: Variant = JSON.parse_string(f.get_as_text())
	return d if typeof(d) == TYPE_DICTIONARY else {}


## The first keyboard key of skill key i ("1", "2", ... ), as the player presses it.
static func key_name(i: int) -> String:
	var action := "skill_%d" % (i + 1)
	if InputMap.has_action(action):
		for ev in InputMap.action_get_events(action):
			if ev is InputEventKey:
				return OS.get_keycode_string(ev.physical_keycode)
	return str(i + 1)


## A key holding a skill gives it back; the key becomes the one to set.
func press_key(i: int) -> void:
	slot = i
	if int(profile.hotkeys[i]) != 0:
		profile.hotkeys[i] = 0
		profile.save(path)
	refresh()
	_show_info(0)


## A learned skill goes onto the key being set. False when it is not learned.
func press_skill(skill: int) -> bool:
	if not profile.assign_hotkey(slot, skill):
		_show_info(skill)
		return false
	profile.save(path)
	refresh()
	_show_info(skill)
	return true


func refresh() -> void:
	for i in keys.size():
		var skill := int(profile.hotkeys[i])
		keys[i].icon = _icon(skill, true) if skill != 0 else null
		ItemSlot.choose(keys[i], i == slot)
	for skill in skills:
		skills[skill].icon = _icon(skill, profile.skill_level(skill) > 0)


## "Whirlwind Sabre / Lv1 Dash & Slash", or "... / (Not Available)" for a skill not learned.
func describe(skill: int) -> String:
	var i := skill - 12
	var names: Array = data.get("names", [])
	var effects: Array = data.get("effects", [])
	if i < 0 or i >= names.size():
		return ""
	var level: int = profile.skill_level(skill)
	if level == 0:
		return "%s / %s" % [tr(names[i]), tr("skills.not_available")]
	return "%s / Lv%d %s" % [tr(names[i]), level, effects[i] if i < effects.size() else ""]


## The card's lines of a skill ([text, heading?]).
func card_lines(skill: int) -> Array:
	return SkillCard.lines(
		skill,
		profile.skill_level(skill),
		data.get("names", []),
		data.get("effects", []),
		profile.attack(),
		profile.defense(),
		profile.max_hp(),
		Settings.tick_seconds()
	)


func _show_info(skill: int) -> void:
	for c in card.get_children():
		card.remove_child(c)
		c.queue_free()
	info = null
	for line in card_lines(skill):
		var l: Label = LINE_SCENE.instantiate()
		l.text = str(line[0])
		if line[1]:
			l.theme_type_variation = &"SmallAccentLabel"
			info = l
		card.add_child(l)


func _icon(skill: int, learned: bool) -> Texture2D:
	return ItemSlot.icon("skill" if learned else "skillgray", skill - 12)
