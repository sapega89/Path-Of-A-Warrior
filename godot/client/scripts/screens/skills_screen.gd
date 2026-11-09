class_name SkillsScreen
extends BaseScreen
## Skills: the five skill keys and the skills by group (MOVE, HEAL, PASV, FWD, NEAR, RANGE,
## WHOLE). A learned skill has its coloured icon, one not yet learned its grey icon.
## Pick a key, then a learned skill to put it on that key; picking a key that holds a skill
## takes the skill off. Beside the groups, the card of the skill under the cursor (as in
## pyport): name and level, what it is, MP and what it does now and at the next level.
## Every change is saved at once.

const SKILLS_PATH := "res://data/skills.json"
const KEY_COUNT := 5

var profile: RefCounted
var path: String = Profile.PATH
var data: Dictionary = {}
var slot := 0  # the skill key being set
var keys: Array[Button] = []
var skills := {}  # skill id -> its Button
var info: Label  # the card's heading line (name and level)
var card: VBoxContainer


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	data = load_data()
	var col := UiTheme.menu_column(self, 900)
	col.add_child(UiTheme.heading("skills.title", 44))

	var key_row := HBoxContainer.new()
	key_row.name = "Keys"
	key_row.alignment = BoxContainer.ALIGNMENT_CENTER
	key_row.add_theme_constant_override("separation", 16)
	for i in KEY_COUNT:
		var box := VBoxContainer.new()
		var l := Label.new()
		l.text = key_name(i)
		l.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		box.add_child(l)
		var b := _icon_button("Key%d" % (i + 1))
		var at := i
		b.pressed.connect(func(): press_key(at))
		b.focus_entered.connect(func(): _show_info(int(profile.hotkeys[at])))
		b.mouse_entered.connect(func(): _show_info(int(profile.hotkeys[at])))
		box.add_child(b)
		key_row.add_child(box)
		keys.append(b)
	col.add_child(key_row)

	var grid := GridContainer.new()
	grid.name = "Groups"
	grid.columns = 2
	grid.add_theme_constant_override("h_separation", 40)
	grid.add_theme_constant_override("v_separation", 6)
	var groups: Array = data.get("groups", [])
	var rows: Array = data.get("rows", [])
	for r in rows.size():
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation", 8)
		var l := Label.new()
		l.text = str(groups[r]) if r < groups.size() else ""
		l.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		l.custom_minimum_size = Vector2(110, 0)
		l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		row.add_child(l)
		for id in rows[r]:
			var skill := int(id)
			var b := _icon_button("Skill%d" % skill)
			if skill == 0:
				b.disabled = true
				b.focus_mode = Control.FOCUS_NONE
			else:
				b.pressed.connect(func(): press_skill(skill))
				b.focus_entered.connect(func(): _show_info(skill))
				b.mouse_entered.connect(func(): _show_info(skill))
				skills[skill] = b
			row.add_child(b)
		grid.add_child(row)
	var middle := HBoxContainer.new()
	middle.add_theme_constant_override("separation", 24)
	middle.add_child(grid)
	var panel := PanelContainer.new()
	panel.name = "Card"
	panel.custom_minimum_size = Vector2(330, 0)
	panel.add_theme_stylebox_override("panel", UiTheme.box(UiTheme.PANEL, UiTheme.ACCENT, 2))
	card = VBoxContainer.new()
	panel.add_child(card)
	middle.add_child(panel)
	var center := CenterContainer.new()
	center.add_child(middle)
	col.add_child(center)

	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	refresh()
	_show_info(int(profile.hotkeys[0]))
	keys[0].grab_focus.call_deferred()


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
		keys[i].add_theme_stylebox_override("normal", ItemSlot.box(i == slot))
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
		var l := Label.new()
		l.text = str(line[0])
		l.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		l.custom_minimum_size = Vector2(310, 0)
		l.add_theme_font_size_override("font_size", 22)
		if line[1]:
			l.add_theme_color_override("font_color", UiTheme.ACCENT)
			info = l
		card.add_child(l)


func _icon(skill: int, learned: bool) -> Texture2D:
	return ItemSlot.icon("skill" if learned else "skillgray", skill - 12)


func _icon_button(node_name: String) -> Button:
	return ItemSlot.button(node_name)
