class_name Belt
extends HBoxContainer
## The belt in the Inventory (belt.tscn): its five potion slots, each with its key above it
## (Z X C V B, used in a mission) and how many potions are in it under it; the chosen slot (the
## one the keypad's * and / take) has a brass border. It only shows: a slot picked or pointed at
## is said up to the screen with a signal.

signal slot_pressed(slot: int)
signal slot_pointed(slot: int)

const SLOTS := 5

var slots: Array[Button] = []
var marks: Array[Label] = []  # the key above each slot
var counts: Array[Label] = []  # how many are in it, under it


func _ready() -> void:
	for i in SLOTS:
		var cell: Control = get_node("Belt%d" % (i + 1))
		var b: Button = cell.get_node("Slot")
		b.pressed.connect(slot_pressed.emit.bind(i))
		b.focus_entered.connect(slot_pointed.emit.bind(i))
		b.mouse_entered.connect(slot_pointed.emit.bind(i))
		slots.append(b)
		marks.append(cell.get_node("Mark"))
		counts.append(cell.get_node("Count"))


## The potions in the slots ([id, count] each) and which slot is chosen.
func show_slots(quick_slots: Array, chosen: int) -> void:
	for i in slots.size():
		var id := int(quick_slots[i][0])
		slots[i].icon = ItemSlot.item_icon(id) if id != 0 else null
		ItemSlot.choose(slots[i], i == chosen)
		counts[i].text = "x%d" % int(quick_slots[i][1]) if id != 0 else ""
