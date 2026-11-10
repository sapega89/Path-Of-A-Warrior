class_name LiveGiftsScreen
extends BaseScreen
## Trade > Gift List (at the auctioneer in the camp): what other players gave this one, five at
## a time, and who gave each. The gifts are in the Warehouse already. The server shows each gift
## once, so the page shows the gifts that came since the last visit; Next asks for five more.

const PLACES := 5

var live: RefCounted
var gifts: Array = []  # the page shown: [{from, item}]
@onready var text: Label = %Text
var cells: Array[Button] = []
@onready var info: Label = %Info
@onready var next: Button = %Next


func _ready() -> void:
	live = LiveClient.of(Router.params)
	cells = (%Grid as ItemGrid).fill(PLACES, func(_i: int) -> void: pass, show_gift)
	(%Back as Button).grab_focus()
	if live == null:
		info.text = tr("live.failed")
		return
	info.text = tr("live.connecting")
	live.sync(Profile.load_or_new(profile_path()), LiveClient.later(self, &"synced"))


func synced(err: String) -> void:
	if err.is_empty():
		ask_next()
	else:
		info.text = tr("live.failed")


## Asks for the next five gifts. Returns false when nothing was asked.
func ask_next() -> bool:
	if live == null or live.busy:
		return false
	info.text = tr("live.connecting")
	live.ask_gifts(LiveClient.later(self, &"listed"))
	return true


func listed(err: String) -> void:
	if not err.is_empty():
		info.text = tr("live.failed")
		return
	gifts = live.gifts
	text.text = tr("live.no_gifts" if gifts.is_empty() else "live.gift_lines")
	for i in cells.size():
		cells[i].icon = ItemSlot.item_icon(int(gifts[i].item.id)) if i < gifts.size() else null
	next.visible = live.more_gifts
	show_gift(0)
	if next.visible:
		next.grab_focus()
	elif not gifts.is_empty():
		cells[0].grab_focus()


func show_gift(i: int) -> void:
	if i >= gifts.size():
		info.text = ""
		return
	var g: Dictionary = gifts[i]
	info.text = "%s\n%s" % [tr("live.gift_from") % str(g.from), Items.describe(g.item)]
