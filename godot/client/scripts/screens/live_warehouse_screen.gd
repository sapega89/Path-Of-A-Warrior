class_name LiveWarehouseScreen
extends Control
## Game menu > Warehouse: the hero's backpack or the Warehouse on the server (200 places), switched
## by the two buttons above the grid. Picking a thing moves it to the other one (into the
## first free place of the backpack); the hero is saved after every move.

var live: RefCounted
var profile: RefCounted
var path: String = Profile.PATH
var in_warehouse := false  # the grid shows the Warehouse (else the backpack)
var tabs: Array[Button] = []
var count: Label
var cells: Array[Button] = []
var info: Label


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	profile = Profile.load_or_new(path)
	live = LiveClient.of(Router.params)
	var col := UiTheme.menu_column(self, 640)
	col.add_child(UiTheme.heading("live.warehouse", 44))
	tabs = ItemGrid.sides(col, show_side)
	count = UiTheme.note("Count")
	col.add_child(count)
	cells = ItemGrid.add(col, LiveClient.WAREHOUSE, 290, press_cell, _show_info)
	info = UiTheme.note("Info", 72)
	col.add_child(info)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	refresh()
	cells[0].grab_focus.call_deferred()
	if live == null:
		info.text = tr("live.failed")
		return
	info.text = tr("live.connecting")
	live.sync(profile, LiveClient.later(self, &"synced"))


func synced(err: String) -> void:
	refresh()
	info.text = describe(0) if err.is_empty() else tr("live.failed")


func show_side(warehouse: bool) -> void:
	in_warehouse = warehouse
	tabs[1 if warehouse else 0].button_pressed = true
	refresh()
	cells[0].grab_focus()
	_show_info(0)


func item_at(i: int) -> Dictionary:
	if in_warehouse:
		return (
			live.warehouse[i].item if live != null and i < live.warehouse.size() else Items.empty()
		)
	return profile.backpack[i] if i < profile.backpack.size() else Items.empty()


## Moves the thing of the cell to the other side. Returns false when nothing was asked.
func press_cell(i: int) -> bool:
	if live == null or live.busy or not live.synced or int(item_at(i).id) == 0:
		return false
	if in_warehouse:
		live.take(profile, i, LiveClient.later(self, &"moved"))
	else:
		live.store(profile, i, LiveClient.later(self, &"moved"))
	return true


func moved(err: String) -> void:
	if err.is_empty():
		profile.save(path)
		refresh()
		info.text = ""
		return
	match err:
		"full":
			info.text = tr("live.backpack_full" if in_warehouse else "live.warehouse_full")
		_:  # the server lost this device's backpack (a new connection): send it again
			info.text = tr("live.failed")
			live.sync(profile, LiveClient.later(self, &"resynced"))


func resynced(_err: String) -> void:
	refresh()


func refresh() -> void:
	var places: int = LiveClient.WAREHOUSE if in_warehouse else profile.backpack.size()
	for i in cells.size():
		cells[i].visible = i < places
		cells[i].icon = ItemSlot.item_icon(int(item_at(i).id)) if i < places else null
	var used := 0
	for i in places:
		if int(item_at(i).id) != 0:
			used += 1
	count.text = "%d / %d" % [used, places]


func describe(i: int) -> String:
	return Items.describe(item_at(i))


func _show_info(i: int) -> void:
	info.text = describe(i)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()


## The line of control hints under the screen (scripts/ui/hint_bar.gd): what picking a thing does.
func controls_hint() -> String:
	return InputSetup.hint("hint.grid_warehouse")
