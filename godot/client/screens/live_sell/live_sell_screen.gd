class_name LiveSellScreen
extends BaseScreen
## Game menu > Trade > Sell Item: a thing of the backpack or of the Warehouse (the two buttons above
## the grid), then its price, typed in; a share of it (the tax) goes to the server when it sells.
## Price Info shows the cheapest lots of the same kind. OK puts the thing on sale (five at most);
## the money comes into the Safe when another player buys it. Elixirs cannot be sold.

enum Step { PICK, PRICE, PRICES }

var live: RefCounted
var profile: RefCounted
var path: String = Profile.PATH
var step := Step.PICK
var in_warehouse := false
var chosen := -1  # the place (or Warehouse index) of the thing to sell
@onready var body: VBoxContainer = %Body
@onready var tabs: Array[Button] = (%Sides as GridSides).tabs()
var cells: Array[Button] = []  # the places of the page shown
var pick_cells: Array[Button] = []
var thing: Button  # on the Price page: the thing to sell
@onready var price: LineEdit = %Price
var typed := ""  # the price typed before Price Info
@onready var info: Label = %Info
## Each step's page.
@onready var pages := {Step.PICK: %PickPage, Step.PRICE: %PricePage, Step.PRICES: %PricesPage}


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	live = LiveClient.of(Router.params)
	pick_cells = (%PickGrid as ItemGrid).fill(LiveClient.WAREHOUSE, pick, _show_pick)
	thing = ItemSlot.button("Cell")
	thing.focus_mode = Control.FOCUS_NONE
	thing.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	%Thing.add_child(thing)
	%Thing.move_child(thing, 0)
	%Back.grab_focus.call_deferred()
	if live == null:
		info.text = tr("live.failed")
		return
	info.text = tr("live.connecting")
	live.sync(profile, LiveClient.later(self, &"synced"))


func synced(err: String) -> void:
	if err.is_empty():
		show_step(Step.PICK)
		info.text = describe(0)
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
			cells = pick_cells
			tabs[1 if in_warehouse else 0].button_pressed = true
			refresh()
			cells[maxi(chosen, 0)].grab_focus.call_deferred()
		Step.PRICE:
			var it := item_at(chosen)
			thing.icon = ItemSlot.item_icon(int(it.id))
			%Name.text = (
				"%s\n%s" % [Items.name_of(int(it.id)), tr("live.enchant_lv") % int(it.enchant)]
			)
			%Hint.text = tr("live.sell_price") % live.tax
			price.text = ""
			info.text = Items.describe(it)
			price.grab_focus.call_deferred()
		Step.PRICES:
			%Caption.text = tr("live.price_info")
			var prices: ItemGrid = %PricesGrid
			prices.clear()
			cells = prices.fill(live.lots.size(), func(_i): pass, show_price)
			for i in live.lots.size():
				cells[i].icon = ItemSlot.item_icon(int(live.lots[i].item.id))
			if not cells.is_empty():
				cells[0].grab_focus.call_deferred()
				show_price(0)


func _show_pick(i: int) -> void:
	info.text = describe(i)


func _on_price_submitted(_t: String) -> void:
	put_on_sale()


func show_side(warehouse: bool) -> void:
	in_warehouse = warehouse
	refresh()
	cells[0].grab_focus()
	info.text = describe(0)


func item_at(i: int) -> Dictionary:
	if in_warehouse:
		return live.warehouse[i].item if i >= 0 and i < live.warehouse.size() else Items.empty()
	return profile.backpack[i] if i >= 0 and i < profile.backpack.size() else Items.empty()


func describe(i: int) -> String:
	return Items.describe(item_at(i))


func refresh() -> void:
	var places: int = LiveClient.WAREHOUSE if in_warehouse else profile.backpack.size()
	for i in cells.size():
		cells[i].visible = i < places
		cells[i].icon = ItemSlot.item_icon(int(item_at(i).id)) if i < places else null


## Picks the thing of a place to sell. Returns false when it cannot be sold (or is none).
func pick(i: int) -> bool:
	var id := int(item_at(i).id)
	if id == 0 or live.busy:
		return false
	if not LiveClient.for_sale(id):
		info.text = tr("live.not_for_sale")
		return false
	chosen = i
	show_step(Step.PRICE)
	return true


## Only digits.
func _typed(t: String) -> void:
	var digits := ""
	for c in t:
		if c >= "0" and c <= "9":
			digits += c
	digits = digits.lstrip("0")
	if digits != t:
		price.text = digits
		price.caret_column = digits.length()


## OK: the thing goes on sale for the price typed. Returns false when nothing was asked.
func put_on_sale() -> bool:
	if live.busy or step != Step.PRICE or int(price.text) <= 0:
		return false
	live.sell(profile, in_warehouse, chosen, int(price.text), LiveClient.later(self, &"sold"))
	return true


func sold(err: String) -> void:
	match err:
		"":
			profile.save(path)
			chosen = -1
			show_step(Step.PICK)
			info.text = tr("live.on_sale")
		"limit":
			info.text = tr("live.limit")
		"price":
			info.text = tr("live.bad_price")
		"not for sale":
			info.text = tr("live.not_for_sale")
		_:
			info.text = tr("live.failed")


func price_info() -> void:
	if live.busy:
		return
	typed = price.text
	var id := int(item_at(chosen).id)
	live.ask_prices(LiveClient.category(id), LiveClient.kind(id), LiveClient.later(self, &"priced"))


func priced(err: String) -> void:
	match err:
		"":
			show_step(Step.PRICES)
		"none":
			info.text = tr("live.no_items")
		_:
			info.text = tr("live.failed")


func show_price(i: int) -> void:
	if i < live.lots.size():
		var lot: Dictionary = live.lots[i]
		info.text = "%s\n%s" % [Items.describe(lot.item), tr("live.price") % int(lot.price)]


func go_back() -> void:
	if live != null and live.busy:
		return
	match step:
		Step.PRICES:
			show_step(Step.PRICE)
			price.text = typed
		Step.PRICE:
			show_step(Step.PICK)
			info.text = describe(chosen)
		_:
			Router.back()
