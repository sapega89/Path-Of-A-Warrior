class_name InventoryScreen
extends BaseScreen
## Inventory: all the hero has, in one window. On the left the hero on his stage with the nine
## places of his gear around him (gear_board.tscn) and under him the belt, five potion slots with
## their keys Z X C V B (belt.tscn); on the right his gold, the 45 places of the backpack and the
## line that says what the thing under the cursor is.
## Picking a worn thing takes it off into the backpack, and the cursor follows it there. Picking a
## thing in the backpack wears it (what was worn in its place comes into the backpack instead) or,
## a stat item (HP, MP, ATK, DEF up), uses it up; gear above the hero's level cannot be taken.
## Picking a belt slot chooses it for the keypad's * and / (the old potion keys, no marks for
## them). Every change is saved at once.
## Opened from a mission's pause menu (sim set) it shows only the belt and the gold, as gear is
## not changed in a fight: the keys change that mission's slots, nothing is saved, and close goes
## back to the pause menu.

var profile: Profile
var path: String = Profile.PATH
var cells: Array[Button] = []  # the backpack's places
var slot := -1  # the belt slot chosen for the potion keys (none until one is picked)
var sim: MapSim = null  # a mission's: its slots and keys are the ones changed
var close := Callable()  # set by the pause menu: what Back does instead of Router.back()

@onready var gear: GearBoard = %Gear
@onready var belt: Belt = %Belt
@onready var gold: Label = %Gold.get_node("Value")
@onready var info: Label = %Info


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	gear.place_pressed.connect(press_place)
	gear.place_pointed.connect(_show_place)
	belt.slot_pressed.connect(press_slot)
	belt.slot_pointed.connect(_show_slot)
	if sim != null:
		_take_the_mission()
	else:
		profile.compact_backpack()
		gear.show_hero(profile)
		_add_cells()
	refresh()
	if cells.is_empty():
		_show_slot(0)
		belt.slots[0].grab_focus.call_deferred()
	else:
		_show_cell(0)
		cells[0].grab_focus.call_deferred()


## In a mission: its belt and keys, the gold picked up in it; no gear and no backpack, and the
## belt above the gold.
func _take_the_mission() -> void:
	profile.quick_slots = sim.quick_slots
	profile.quick_keys = sim.quick_keys
	profile.gold += int(sim.gold)
	gear.visible = false
	%Backpack.visible = false
	(%Body as BoxContainer).vertical = true


## The backpack's places: how many is known only here (Items.BACKPACK).
func _add_cells() -> void:
	var grid: GridContainer = %Backpack
	for i in Items.BACKPACK:
		var b := ItemSlot.button("Cell%d" % i)
		b.pressed.connect(press_cell.bind(i))
		b.focus_entered.connect(_show_cell.bind(i))
		b.mouse_entered.connect(_show_cell.bind(i))
		grid.add_child(b)
		cells.append(b)


## Wears or uses the thing in the cell. Returns the line shown ("" when worn).
func press_cell(i: int) -> String:
	var said: String = profile.use_item(i)
	if said == "cannot":
		info.text = tr("inventory.cannot_take")
		return said
	profile.save(path)
	refresh()
	info.text = said if not said.is_empty() else describe(i)
	return said


## Takes off what is worn in place i into the backpack; the cursor follows it there. False when
## nothing is worn there or the backpack is full (the line says so).
func press_place(i: int) -> bool:
	var to := profile.backpack.find_custom(func(it: Dictionary) -> bool: return int(it.id) == 0)
	if not profile.unequip(i):
		if int(profile.equipped[i].id) != 0:
			info.text = tr("shop.full")
		return false
	profile.save(path)
	refresh()
	cells[to].grab_focus()
	return true


## Chooses belt slot i for the potion keys.
func press_slot(i: int) -> void:
	slot = i
	refresh()
	_show_slot(i)


## Puts the chosen belt slot on potion key k. False when it cannot (empty, already there).
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
	belt.show_slots(profile.quick_slots, slot)
	if sim == null:
		gear.show_gear(profile)
	for i in cells.size():
		cells[i].icon = ItemSlot.item_icon(int(profile.backpack[i].id))


## What the thing in the backpack's place i is.
func describe(i: int) -> String:
	return Items.describe(profile.backpack[i])


func _show_cell(i: int) -> void:
	info.text = describe(i)


func _show_place(i: int) -> void:
	info.text = Items.describe(profile.equipped[i])


func _show_slot(i: int) -> void:
	info.text = Items.describe_potion(int(profile.quick_slots[i][0]))


func _screen_input(event: InputEvent) -> void:
	for k in 2:
		if event.is_action_pressed("potion_%d" % (k + 1)):
			get_viewport().set_input_as_handled()
			press_key(k)


## The line of control hints under the screen (scripts/ui/hint_bar.gd): what picking the thing
## under the cursor does, in the gear, the belt or the backpack.
func controls_hint() -> String:
	var at := get_viewport().gui_get_focus_owner()
	if at != null and gear.is_ancestor_of(at):
		return InputSetup.hint("hint.grid_gear")
	if at != null and belt.is_ancestor_of(at):
		return InputSetup.hint("hint.grid_assign")
	return InputSetup.hint("hint.grid_inventory")
