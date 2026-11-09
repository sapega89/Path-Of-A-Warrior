extends Control
## Game menu > Trade > Sell Item: a thing of the backpack or of the Warehouse (the two buttons above
## the grid), then its price, typed in; a share of it (the tax) goes to the server when it sells.
## Price Info shows the cheapest lots of the same kind. OK puts the thing on sale (five at most);
## the money comes into the Safe when another player buys it. Elixirs cannot be sold.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Items := preload("res://scripts/core/items.gd")
const ItemSlot := preload("res://scripts/ui/item_slot.gd")
const ItemGrid := preload("res://scripts/ui/item_grid.gd")
const LiveClient := preload("res://scripts/net/live_client.gd")

enum Step { PICK, PRICE, PRICES }

var live: RefCounted
var profile: RefCounted
var path: String = Profile.PATH
var step := Step.PICK
var in_warehouse := false
var chosen := -1  # the place (or Warehouse index) of the thing to sell
var body: VBoxContainer
var tabs: Array[Button] = []
var cells: Array[Button] = []
var price: LineEdit
var typed := ""  # the price typed before Price Info
var info: Label


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	profile = Profile.load_or_new(path)
	live = LiveClient.of(Router.params)
	var col := UiTheme.menu_column(self, 640)
	col.add_child(UiTheme.heading("live.sell", 44))
	body = VBoxContainer.new()
	body.name = "Body"
	body.custom_minimum_size = Vector2(0, 360)
	body.add_theme_constant_override("separation", 8)
	col.add_child(body)
	info = UiTheme.note("Info", 72)
	col.add_child(info)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(go_back)
	col.add_child(back)
	back.grab_focus.call_deferred()
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


func show_step(s: Step) -> void:
	step = s
	for c in body.get_children():
		body.remove_child(c)
		c.queue_free()
	cells.clear()
	price = null
	match step:
		Step.PICK:
			tabs = ItemGrid.sides(body, show_side)
			tabs[1 if in_warehouse else 0].button_pressed = true
			cells = ItemGrid.add(
				body, LiveClient.WAREHOUSE, 290, pick, func(i): info.text = describe(i)
			)
			refresh()
			cells[maxi(chosen, 0)].grab_focus.call_deferred()
		Step.PRICE:
			var it := item_at(chosen)
			var row := HBoxContainer.new()
			row.name = "Thing"
			row.alignment = BoxContainer.ALIGNMENT_CENTER
			row.add_theme_constant_override("separation", 16)
			var cell := ItemSlot.button("Cell")
			cell.icon = ItemSlot.item_icon(int(it.id))
			cell.focus_mode = Control.FOCUS_NONE
			cell.size_flags_vertical = Control.SIZE_SHRINK_CENTER
			row.add_child(cell)
			var name_line := Label.new()
			name_line.name = "Name"
			name_line.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
			name_line.text = (
				"%s\n%s" % [Items.name_of(int(it.id)), tr("live.enchant_lv") % int(it.enchant)]
			)
			row.add_child(name_line)
			body.add_child(row)
			var hint := UiTheme.note("Hint")
			hint.text = tr("live.sell_price") % live.tax
			body.add_child(hint)
			price = LineEdit.new()
			price.name = "Price"
			price.alignment = HORIZONTAL_ALIGNMENT_CENTER
			price.max_length = 9
			price.text_changed.connect(_typed)
			price.text_submitted.connect(func(_t: String) -> void: put_on_sale())
			body.add_child(price)
			var ok := Button.new()
			ok.name = "Ok"
			ok.text = "live.ok"
			ok.pressed.connect(put_on_sale)
			body.add_child(ok)
			var prices := Button.new()
			prices.name = "PriceInfo"
			prices.text = "live.price_info"
			prices.pressed.connect(price_info)
			body.add_child(prices)
			info.text = Items.describe(it)
			price.grab_focus.call_deferred()
		Step.PRICES:
			var title := UiTheme.note("Caption")
			title.text = tr("live.price_info")
			body.add_child(title)
			cells = ItemGrid.add(body, live.lots.size(), 300, func(_i): pass, show_price)
			for i in live.lots.size():
				cells[i].icon = ItemSlot.item_icon(int(live.lots[i].item.id))
			if not cells.is_empty():
				cells[0].grab_focus.call_deferred()
				show_price(0)


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
	if live.busy or price == null or int(price.text) <= 0:
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


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		go_back()
