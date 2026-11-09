extends Control
## Multiplayer > Character > Skills: the skills the hero has learned (from the single player),
## each with its level and its cost on the battle's MP gauge, and the four skill slots of the
## battles. Pick a skill, then a slot to put it there (from another slot it moves); a slot
## picked with no skill in hand is emptied. Every change is saved on the server.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const OnlineClient := preload("res://scripts/net/online_client.gd")

var online: RefCounted
var list: VBoxContainer
var skill_buttons: Array[Button] = []
var slot_buttons: Array[Button] = []
var info: Label
var held := -1  # the skill picked, waiting for a slot
var slots: Array = []


func _ready() -> void:
	online = OnlineClient.of(Router.params)
	var col := UiTheme.menu_column(self, 640)
	col.add_child(UiTheme.heading("online.skills", 44))
	list = VBoxContainer.new()
	list.name = "List"
	list.add_theme_constant_override("separation", 4)
	col.add_child(list)
	var row := GridContainer.new()  # the four slots, two by two
	row.name = "Slots"
	row.columns = 2
	for i in 4:
		var b := Button.new()
		b.name = "Slot%d" % (i + 1)
		b.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		b.pressed.connect(press_slot.bind(i))
		row.add_child(b)
		slot_buttons.append(b)
	col.add_child(row)
	info = UiTheme.note("Info", 60)
	col.add_child(info)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	back.grab_focus.call_deferred()
	if online == null:
		info.text = tr("live.failed")
		return
	slots = (online.me.get("slots", []) as Array).duplicate()
	info.text = tr("live.connecting")
	online.ask_skills(OnlineClient.later(self, &"listed"))


func listed(err: String) -> void:
	if not err.is_empty():
		info.text = tr("live.failed")
		return
	info.text = tr("online.skills_hint") if not online.skills.is_empty() else tr("online.no_skills")
	for s in online.skills:
		var b := Button.new()
		var id := int(s.id)
		b.name = "Skill%d" % id
		b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		b.text = "%s  Lv%d  MP %d" % [OnlineClient.skill_name(id), int(s.level), cost(id)]
		b.pressed.connect(press_skill.bind(id))
		b.focus_entered.connect(
			func(): info.text = OnlineClient.SKILL_INFO[OnlineClient.SKILL_IDS.find(id)]
		)
		list.add_child(b)
		skill_buttons.append(b)
	refresh()
	if not skill_buttons.is_empty():
		skill_buttons[0].grab_focus.call_deferred()


## The skill's share of the battle's MP gauge (the server's skill_cost).
func cost(id: int) -> int:
	var costs: Array = online.me.get("skill_cost", [])
	var i := OnlineClient.SKILL_IDS.find(id)
	return int(costs[i]) if i >= 0 and i < costs.size() else 0


func refresh() -> void:
	for i in 4:
		var id := int(slots[i]) if i < slots.size() else OnlineClient.EMPTY_SKILL
		slot_buttons[i].text = (
			"%d: %s"
			% [i + 1, OnlineClient.skill_name(id) if id != OnlineClient.EMPTY_SKILL else "-"]
		)
	for b in skill_buttons:
		var id := int(b.name.trim_prefix("Skill"))
		b.modulate = Color(1, 0.85, 0.4) if id == held else Color.WHITE


func press_skill(id: int) -> void:
	held = id if held != id else -1
	info.text = tr("online.pick_slot") if held >= 0 else ""
	refresh()
	if held >= 0:
		slot_buttons[0].grab_focus()


## Puts the skill in hand into slot i (moving it from another), or empties the slot.
func press_slot(i: int) -> void:
	if online == null or online.busy:
		return
	var new_slots := slots.duplicate()
	while new_slots.size() < 4:
		new_slots.append(OnlineClient.EMPTY_SKILL)
	if held >= 0:
		var was := new_slots.find(held)
		if was >= 0:
			new_slots[was] = new_slots[i]
		new_slots[i] = held
	else:
		new_slots[i] = OnlineClient.EMPTY_SKILL
	held = -1
	info.text = tr("live.connecting")
	online.set_slots(new_slots, OnlineClient.later(self, &"saved"))


func saved(err: String) -> void:
	if not err.is_empty():
		info.text = tr("live.failed")
		return
	slots = (online.me.slots as Array).duplicate()
	info.text = tr("online.saved")
	refresh()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		if held >= 0:
			held = -1
			info.text = ""
			refresh()
			return
		Router.back()
