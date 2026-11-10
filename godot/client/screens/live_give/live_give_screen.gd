class_name LiveGiveScreen
extends BaseScreen
## Trade > Give a Gift (at the auctioneer in the camp): a thing of the backpack or of the
## Warehouse, then the UserID of the player it is for, typed in. OK asks once more; Yes sends
## the thing into that player's Warehouse, with a line in his Gift List (screens/live_gifts).
## The hero is saved then. What cannot be sold (elixirs) cannot be given either.

enum Step { PICK, WHO }

## The text for each answer of the server that is not "".
const ERRORS := {
	"nobody": "live.no_player",
	"self": "live.gift_self",
	"full": "live.their_warehouse_full",
	"not for sale": "live.not_giftable",
}

var live: RefCounted
var profile: RefCounted
var path: String = Profile.PATH
var step := Step.PICK
var chosen := -1  # the place (or Warehouse index) of the thing to give
var sent: Array = []  # the name of the thing on its way and who it is for
@onready var things: LiveThings = %Things
var thing: Button  # on the Who page: the thing to give
@onready var to: LineEdit = %To
@onready var info: Label = %Info
@onready var ask: ConfirmationDialog = %Ask
## Each step's page.
@onready var pages := {Step.PICK: %Things, Step.WHO: %WhoPage}


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	live = LiveClient.of(Router.params)
	thing = ItemSlot.button("Cell")
	thing.focus_mode = Control.FOCUS_NONE
	thing.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	%Thing.add_child(thing)
	%Thing.move_child(thing, 0)
	(%Back as Button).grab_focus()
	if live == null:
		info.text = tr("live.failed")
		return
	info.text = tr("live.connecting")
	live.sync(profile, LiveClient.later(self, &"synced"))


func synced(err: String) -> void:
	if err.is_empty():
		things.show_hero(live, profile)
		show_step(Step.PICK)
		_show_pick(0)
	else:
		info.text = tr("live.failed")


## Shows the page of step s, as it is at its start.
func show_step(s: Step) -> void:
	step = s
	for p in pages.values():
		p.visible = false
	pages[step].visible = true
	match step:
		Step.PICK:
			things.refresh()
			things.focus(maxi(chosen, 0))
		Step.WHO:
			var it := things.item_at(chosen)
			thing.icon = ItemSlot.item_icon(int(it.id))
			%Name.text = Items.name_of(int(it.id))
			info.text = Items.describe(it)
			to.grab_focus()


func _show_pick(i: int) -> void:
	info.text = Items.describe(things.item_at(i))


## Picks the thing of a place to give. Returns false when it cannot be given (or is none).
func pick(i: int) -> bool:
	var id := int(things.item_at(i).id)
	if id == 0 or live.busy:
		return false
	if not LiveClient.for_sale(id):
		info.text = tr("live.not_giftable")
		return false
	chosen = i
	show_step(Step.WHO)
	return true


## A UserID: capital letters only.
func _typed(t: String) -> void:
	var letters := ""
	for c in t.to_upper():
		if c >= "A" and c <= "Z":
			letters += c
	if letters != t:
		to.text = letters
		to.caret_column = letters.length()


func _on_to_submitted(_t: String) -> void:
	ask_give()


## OK: asks whether to give the thing to the player typed. Returns the question, "" when none.
func ask_give() -> String:
	if live.busy or step != Step.WHO:
		return ""
	if not Protocol.valid_id(to.text):
		info.text = tr("live.bad_user_id")
		return ""
	sent = [Items.name_of(int(things.item_at(chosen).id)), to.text]
	ask.dialog_text = tr("live.give_ask") % sent
	ask.popup_centered()
	return ask.dialog_text


## Yes: the thing goes to the player.
func confirm() -> void:
	if not live.busy and step == Step.WHO:
		live.give(profile, things.in_warehouse, chosen, sent[1], LiveClient.later(self, &"given"))


func given(err: String) -> void:
	if not err.is_empty():
		info.text = tr(ERRORS.get(err, "live.failed"))
		return
	profile.save(path)
	chosen = -1
	show_step(Step.PICK)
	info.text = tr("live.given") % sent


func go_back() -> void:
	if live != null and live.busy:
		return
	if step == Step.WHO:
		show_step(Step.PICK)
		_show_pick(chosen)
	else:
		Router.back()
