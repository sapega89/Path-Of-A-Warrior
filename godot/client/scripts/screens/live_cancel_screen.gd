extends Control
## Game menu > Trade > Cancel Sale: this player's lots on sale (five at most). Picking one asks
## "Do you want to cancel sales of ...?"; Yes takes it off the market into the backpack, or into
## the Warehouse when the backpack is full. The hero is saved then.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Items := preload("res://scripts/core/items.gd")
const ItemSlot := preload("res://scripts/ui/item_slot.gd")
const ItemGrid := preload("res://scripts/ui/item_grid.gd")
const LiveClient := preload("res://scripts/net/live_client.gd")

var live: RefCounted
var profile: RefCounted
var path: String = Profile.PATH
var gold: Label
var cells: Array[Button] = []
var info: Label
var ask: ConfirmationDialog
var asked: Dictionary = {}  # the lot waiting for Yes


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	profile = Profile.load_or_new(path)
	live = LiveClient.of(Router.params)
	var col := UiTheme.menu_column(self, 640)
	col.add_child(UiTheme.heading("live.cancel", 44))
	var gold_row := UiTheme.gold_row("Gold")
	gold = gold_row.get_node("Value")
	gold.text = str(profile.gold)
	col.add_child(gold_row)
	cells = ItemGrid.add(col, LiveClient.MAX_SALES, 70, press_lot, show_lot)
	info = UiTheme.note("Info", 100)
	col.add_child(info)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	ask = ConfirmationDialog.new()
	ask.name = "Ask"
	ask.confirmed.connect(confirm)
	ask.canceled.connect(func(): asked = {})
	add_child(ask)
	cells[0].grab_focus.call_deferred()
	if live == null:
		info.text = tr("live.failed")
		return
	info.text = tr("live.connecting")
	live.sync(profile, LiveClient.later(self, &"synced"))


func synced(err: String) -> void:
	if not err.is_empty():
		info.text = tr("live.failed")
		return
	live.lots = []
	live.ask_mine(LiveClient.later(self, &"listed"))


func listed(err: String) -> void:
	if err == "none":
		live.lots = []
	refresh()
	match err:
		"":
			show_lot(0)
		"none":
			info.text = tr("live.no_items")
		_:
			info.text = tr("live.failed")


func refresh() -> void:
	gold.text = str(profile.gold)
	for i in cells.size():
		cells[i].icon = ItemSlot.item_icon(int(live.lots[i].item.id)) if i < live.lots.size() else null


func show_lot(i: int) -> void:
	if live != null and i < live.lots.size():
		var lot: Dictionary = live.lots[i]
		info.text = "%s\n%s\n%s" % [Items.name_of(int(lot.item.id)), tr("live.price") % int(lot.price),
			Items.describe(lot.item)]


## Asks before taking the lot of a place off the market. Returns the question.
func press_lot(i: int) -> String:
	if live == null or live.busy or i >= live.lots.size():
		return ""
	asked = live.lots[i]
	ask.dialog_text = tr("live.cancel_ask") % Items.name_of(int(asked.item.id))
	ask.popup_centered()
	return ask.dialog_text


func confirm() -> void:
	if asked.is_empty() or live.busy:
		return
	live.cancel(profile, asked, LiveClient.later(self, &"canceled"))


func canceled(err: String) -> void:
	var lot := asked
	asked = {}
	match err:
		"":
			profile.save(path)
			refresh()
			info.text = tr("live.canceled") % Items.name_of(int(lot.item.id))
		"full":
			info.text = tr("live.warehouse_full")
		"gone":  # bought meanwhile
			info.text = tr("live.sold_out")
			live.ask_mine(LiveClient.later(self, &"relisted"))
		_:
			info.text = tr("live.failed")


## The list again after a lot was gone, keeping the line that said so.
func relisted(err: String) -> void:
	if err == "none":
		live.lots = []
	refresh()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
