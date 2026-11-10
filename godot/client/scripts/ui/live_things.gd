class_name LiveThings
extends VBoxContainer
## The hero's backpack or his Warehouse on the server, switched by the two buttons above the
## grid (scenes/ui/live_things.tscn): where a Live page picks a thing.

## The place i was pressed: of the backpack, or of the Warehouse when in_warehouse.
signal picked(i: int)
## The place i got the focus or the pointer.
signal pointed(i: int)

var live: RefCounted
var profile: RefCounted
var in_warehouse := false
var cells: Array[Button] = []


## Shows the things of this hero and Live client (the backpack first).
func show_hero(live_client: RefCounted, hero: RefCounted) -> void:
	live = live_client
	profile = hero
	if cells.is_empty():
		cells = (%Grid as ItemGrid).fill(LiveClient.WAREHOUSE, picked.emit, pointed.emit)
	refresh()


func show_side(warehouse: bool) -> void:
	in_warehouse = warehouse
	refresh()
	focus(0)
	pointed.emit(0)


## The focus on place i, and the side shown pressed.
func focus(i: int) -> void:
	(%Sides as GridSides).tabs()[1 if in_warehouse else 0].button_pressed = true
	cells[i].grab_focus()


func item_at(i: int) -> Dictionary:
	if in_warehouse:
		return live.warehouse[i].item if i >= 0 and i < live.warehouse.size() else Items.empty()
	return profile.backpack[i] if i >= 0 and i < profile.backpack.size() else Items.empty()


func refresh() -> void:
	var places: int = LiveClient.WAREHOUSE if in_warehouse else profile.backpack.size()
	for i in cells.size():
		cells[i].visible = i < places
		cells[i].icon = ItemSlot.item_icon(int(item_at(i).id)) if i < places else null
