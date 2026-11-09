class_name AssignItemsScreen
extends BaseScreen
## Assign Items: the hero's gold and the five potion slots of the belt, each with its key above
## it (Z X C V B, used in a mission) and "Keys Z X C V B" under them, as in pyport with the skill
## bar. The keypad's * and / still put the chosen slot on the old potion keys (no buttons or
## marks for them). Saved at once. Opened from a mission's pause menu (sim set) it changes that
## mission's slots and saves nothing; close goes back there.
const SLOTS := 5

var profile: RefCounted
var path: String = Profile.PATH
var slot := 0
var slots: Array[Button] = []
var marks: Array[Label] = []
@onready var gold: Label = %Gold.get_node("Value")
@onready var info: Label = %Info
var sim: RefCounted = null  # a mission's: its slots and keys are the ones changed
var close := Callable()  # set by the pause menu: what Back does instead of Router.back()


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	if sim != null:
		profile.quick_slots = sim.quick_slots
		profile.quick_keys = sim.quick_keys
		profile.gold += int(sim.gold)
	%Keys.text = tr("assign.keys")
	var row: HBoxContainer = %Slots
	for i in SLOTS:
		var box := VBoxContainer.new()
		var mark := Label.new()
		mark.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		mark.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		mark.custom_minimum_size = Vector2(0, 40)
		box.add_child(mark)
		marks.append(mark)
		var b := ItemSlot.button("Slot%d" % (i + 1))
		var at := i
		b.pressed.connect(func(): press_slot(at))
		b.focus_entered.connect(func(): _show_info(at))
		b.mouse_entered.connect(func(): _show_info(at))
		box.add_child(b)
		var count := Label.new()
		count.name = "Count"
		count.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		count.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		box.add_child(count)
		row.add_child(box)
		slots.append(b)
	refresh()
	_show_info(0)
	slots[0].grab_focus.call_deferred()


## The belt key of slot i ("Z" .. "B").
static func belt_key(i: int) -> String:
	return "ZXCVB"[i]


func press_slot(i: int) -> void:
	slot = i
	refresh()
	_show_info(i)


## Puts the chosen slot on potion key k. False when it cannot (empty, already there).
func press_key(k: int) -> bool:
	if not profile.assign_quick_key(k, slot):
		return false
	if sim == null:
		profile.save(path)
	refresh()
	return true


func go_back() -> void:
	if close.is_valid():
		close.call()
	else:
		Router.back()


func refresh() -> void:
	gold.text = str(profile.gold)
	for i in slots.size():
		var s: Array = profile.quick_slots[i]
		var id := int(s[0])
		slots[i].icon = ItemSlot.item_icon(id) if id != 0 else null
		slots[i].add_theme_stylebox_override("normal", ItemSlot.box(i == slot))
		slots[i].get_parent().get_node("Count").text = "x%d" % int(s[1]) if id != 0 else ""
		marks[i].text = belt_key(i)


func describe(i: int) -> String:
	return Items.describe_potion(int(profile.quick_slots[i][0]))


func _show_info(i: int) -> void:
	info.text = describe(i)


func _screen_input(event: InputEvent) -> void:
	for k in 2:
		if event.is_action_pressed("potion_%d" % (k + 1)):
			get_viewport().set_input_as_handled()
			press_key(k)


## The line of control hints under the screen (scripts/ui/hint_bar.gd): what picking a thing does.
func controls_hint() -> String:
	return InputSetup.hint("hint.grid_assign")
