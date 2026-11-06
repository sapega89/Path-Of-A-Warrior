extends Control
## A page of the Blacksmith (Router.params "mode"): the hero's gold over a grid of things.
## Buy: the shop's potions, scrolls and gears. Sell: the quick slots' potions, then the
## backpack, for half the price. Enchant: the backpack, then what the hero wears; enchanting
## costs gold, asks first, and can fail or lose the thing. Every change is saved at once.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Items := preload("res://scripts/core/items.gd")
const ItemSlot := preload("res://scripts/ui/item_slot.gd")
const COLUMNS := 5
const QUICK := 5

var profile: RefCounted
var path: String = Profile.PATH
var mode := "buy"
var cells: Array[Button] = []
var gold: Label
var info: Label
var ask: ConfirmationDialog
var asked := -1  # the cell waiting for the answer to "Continue?"
var rng := RandomNumberGenerator.new()


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	mode = str(Router.params.get("mode", "buy"))
	profile = Profile.load_or_new(path)
	profile.compact_backpack()
	var col := UiTheme.menu_column(self, 640)
	col.add_child(UiTheme.heading("blacksmith." + mode, 44))

	var gold_row := HBoxContainer.new()
	gold_row.name = "Gold"
	gold_row.alignment = BoxContainer.ALIGNMENT_CENTER
	var coin := TextureRect.new()
	coin.texture = load("res://assets/original/ui/gold.png")
	coin.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	coin.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	coin.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	coin.custom_minimum_size = Vector2(56, 40)
	gold_row.add_child(coin)
	gold = Label.new()
	gold.name = "Value"
	gold.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	gold.custom_minimum_size = Vector2(160, 0)
	gold.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	gold_row.add_child(gold)
	col.add_child(gold_row)

	var grid := GridContainer.new()
	grid.name = "Things"
	grid.columns = COLUMNS
	grid.add_theme_constant_override("h_separation", 6)
	grid.add_theme_constant_override("v_separation", 6)
	for i in cell_count():
		var b := ItemSlot.button("Cell%d" % i)
		var at := i
		b.pressed.connect(func(): press_cell(at))
		b.focus_entered.connect(func(): _show_info(at))
		b.mouse_entered.connect(func(): _show_info(at))
		grid.add_child(b)
		cells.append(b)
	var scroll := ScrollContainer.new()
	scroll.name = "Scroll"
	scroll.custom_minimum_size = Vector2(0, 340)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.follow_focus = true
	var center := CenterContainer.new()
	center.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	center.add_child(grid)
	scroll.add_child(center)
	col.add_child(scroll)

	info = Label.new()
	info.name = "Info"
	info.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	info.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	info.custom_minimum_size = Vector2(0, 72)
	col.add_child(info)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)

	ask = ConfirmationDialog.new()
	ask.name = "Ask"
	ask.confirmed.connect(confirm)
	ask.canceled.connect(func(): asked = -1)
	add_child(ask)
	refresh()
	_show_info(0)
	cells[0].grab_focus.call_deferred()


func cell_count() -> int:
	match mode:
		"sell":
			return QUICK + Items.BACKPACK
		"enchant":
			return Items.BACKPACK + Items.EQUIPPED
	return profile.shop.size()


## The thing in a cell (a potion of a quick slot as {id}).
func item_at(i: int) -> Dictionary:
	match mode:
		"sell":
			if i < QUICK:
				var it := Items.empty()
				it.id = int(profile.quick_slots[i][0])
				return it
			return profile.backpack[i - QUICK]
		"enchant":
			if i < Items.BACKPACK:
				return profile.backpack[i]
			return profile.equipped[i - Items.BACKPACK]
	return profile.shop[i]


## Buys, sells, or asks to enchant the thing of the cell. Returns the line shown.
func press_cell(i: int) -> String:
	var item := item_at(i)
	var id := int(item.id)
	if id == 0:
		return ""
	var said := ""
	match mode:
		"buy":
			var r: String = profile.buy(i)
			said = tr("shop." + r).replace("%s", _name(id))
			if r == "bought":
				profile.save(path)
		"sell":
			var where := "quick" if i < QUICK else "backpack"
			var thing := _name(id)
			if profile.sell(where, i if i < QUICK else i - QUICK):
				profile.save(path)
				said = tr("shop.sold").replace("%s", thing)
		"enchant":
			var can: String = profile.can_enchant(item)
			if can != "ok":
				said = tr("enchant." + can)
			else:
				asked = i
				ask.dialog_text = tr("enchant.ask").replace("%d", str(Items.enchant_price(item)))
				ask.popup_centered()
				said = ask.dialog_text
	refresh()
	info.text = said
	return said


## The answer Yes to "Continue?": the thing is enchanted (or not). Returns the line shown.
func confirm() -> String:
	if asked < 0:
		return ""
	var r: String = profile.enchant(item_at(asked), rng)
	asked = -1
	if r != "no_gold":
		profile.save(path)
	var said := tr("shop.no_gold") if r == "no_gold" else tr("enchant.success" if r == "success" else "enchant.fail")
	refresh()
	info.text = said
	return said


func refresh() -> void:
	gold.text = str(profile.gold)
	for i in cells.size():
		var item := item_at(i)
		cells[i].icon = ItemSlot.item_icon(int(item.id))
		if mode == "sell" and i < QUICK and int(item.id) != 0:
			cells[i].text = str(int(profile.quick_slots[i][1]))
		else:
			cells[i].text = ""


func describe(i: int) -> String:
	var item := item_at(i)
	if mode == "enchant":
		return Items.describe(item)
	return Items.describe_for_sale(item, mode == "sell")


func _name(id: int) -> String:
	if id < 100:
		return str(Items.POTION_NAMES[id - 1]).strip_edges() if id <= Items.POTION_NAMES.size() else ""
	return Items.name_of(id)


func _show_info(i: int) -> void:
	info.text = describe(i)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
