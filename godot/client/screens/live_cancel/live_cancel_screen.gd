class_name LiveCancelScreen
extends BaseScreen
## Game menu > Trade > Cancel Sale: this player's lots on sale (five at most). Picking one asks
## "Do you want to cancel sales of ...?"; Yes takes it off the market into the backpack, or into
## the Warehouse when the backpack is full. The hero is saved then.

var live: RefCounted
var profile: RefCounted
var path: String = Profile.PATH
@onready var gold: Label = %Gold.get_node("Value")
var cells: Array[Button] = []
@onready var info: Label = %Info
@onready var ask: ConfirmationDialog = %Ask
var asked: Dictionary = {}  # the lot waiting for Yes


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	live = LiveClient.of(Router.params)
	gold.text = str(profile.gold)
	cells = (%Grid as ItemGrid).fill(LiveClient.MAX_SALES, press_lot, show_lot)
	cells[0].grab_focus.call_deferred()
	if live == null:
		info.text = tr("live.failed")
		return
	info.text = tr("live.connecting")
	live.sync(profile, LiveClient.later(self, &"synced"))


func _on_cancel() -> void:
	asked = {}


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
		cells[i].icon = (
			ItemSlot.item_icon(int(live.lots[i].item.id)) if i < live.lots.size() else null
		)


func show_lot(i: int) -> void:
	if live != null and i < live.lots.size():
		var lot: Dictionary = live.lots[i]
		info.text = (
			"%s\n%s\n%s"
			% [
				Items.name_of(int(lot.item.id)),
				tr("live.price") % int(lot.price),
				Items.describe(lot.item)
			]
		)


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
