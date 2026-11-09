class_name LiveBuyScreen
extends Control
## Game menu > Trade > Buy Item, step by step: the category (Normal, Special, Rare Items), the kind
## (a grid of the things), the enchant level with the number of lots at each (Rare things have
## none), then the lots, 20 a page, cheapest first. Picking a lot asks "Buy for N Gold?"; with a
## full backpack it asks whether to put the thing in the Warehouse instead. The hero is saved
## after a buy. Back goes one step up.

const CATEGORIES := ["live.normal", "live.special", "live.rare"]
const LEVELS := 10

enum Step { CATEGORY, KIND, ENCHANT, LOTS }

var live: RefCounted
var profile: RefCounted
var path: String = Profile.PATH
var step := Step.CATEGORY
var cat := 0
var kind := 0
var enchant := 0
var page := 0
var gold: Label
var caption: Label
var body: VBoxContainer
var cells: Array[Button] = []  # the places of the step's grid (or its list)
var page_line: Label
var info: Label
var ask: ConfirmationDialog
var asked: Dictionary = {}  # the lot waiting for Yes
var into_warehouse := false  # ... and where it goes
var note := ""  # the line the next step shows (what happened before it)


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	profile = Profile.load_or_new(path)
	live = LiveClient.of(Router.params)
	var col := UiTheme.menu_column(self, 640)
	col.add_child(UiTheme.heading("live.buy", 44))
	var gold_row := UiTheme.gold_row("Gold")
	gold = gold_row.get_node("Value")
	col.add_child(gold_row)
	caption = UiTheme.note("Caption")
	col.add_child(caption)
	body = VBoxContainer.new()
	body.name = "Body"
	body.custom_minimum_size = Vector2(0, 300)
	body.add_theme_constant_override("separation", 8)
	col.add_child(body)
	info = UiTheme.note("Info", 72)
	col.add_child(info)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(go_back)
	col.add_child(back)
	ask = ConfirmationDialog.new()
	ask.name = "Ask"
	ask.confirmed.connect(confirm)
	ask.canceled.connect(func(): asked = {})
	add_child(ask)
	gold.text = str(profile.gold)
	back.grab_focus.call_deferred()
	if live == null:
		info.text = tr("live.failed")
		return
	info.text = tr("live.connecting")
	live.sync(profile, LiveClient.later(self, &"synced"))


func synced(err: String) -> void:
	if err.is_empty():
		show_step(Step.CATEGORY)
	else:
		info.text = tr("live.failed")


## Builds the page of a step from what the client has (counts, lots).
func show_step(s: Step) -> void:
	step = s
	for c in body.get_children():
		body.remove_child(c)
		c.queue_free()
	cells.clear()
	page_line = null
	info.text = note
	note = ""
	gold.text = str(profile.gold)
	match step:
		Step.CATEGORY:
			caption.text = ""
			for i in CATEGORIES.size():
				var b := Button.new()
				b.name = "Category%d" % i
				b.text = CATEGORIES[i]
				b.pressed.connect(choose_category.bind(i))
				body.add_child(b)
				cells.append(b)
			if cat < cells.size():
				cells[cat].grab_focus.call_deferred()
			return
		Step.KIND:
			caption.text = tr(CATEGORIES[cat])
			var ids: Array = LiveClient.KINDS[cat]
			cells = ItemGrid.add(
				body, ids.size(), 300, choose_kind, func(i): info.text = Items.name_of(ids[i])
			)
			for i in ids.size():
				cells[i].icon = ItemSlot.item_icon(ids[i])
			cells[mini(kind, cells.size() - 1)].grab_focus.call_deferred()
		Step.ENCHANT:
			caption.text = (
				"%s / %s" % [tr(CATEGORIES[cat]), Items.name_of(LiveClient.KINDS[cat][kind])]
			)
			var grid := GridContainer.new()
			grid.name = "Levels"
			grid.columns = 5
			grid.add_theme_constant_override("h_separation", 6)
			grid.add_theme_constant_override("v_separation", 6)
			for e in LEVELS:
				var b := Button.new()
				b.name = "Level%d" % e
				b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
				b.custom_minimum_size = Vector2(110, 90)
				b.text = "+%d\n%d" % [e, lot_count(e)]
				b.pressed.connect(choose_enchant.bind(e))
				grid.add_child(b)
				cells.append(b)
			var center := CenterContainer.new()
			center.add_child(grid)
			body.add_child(center)
			cells[enchant].grab_focus.call_deferred()
		Step.LOTS:
			var line := (
				"%s / %s" % [tr(CATEGORIES[cat]), Items.name_of(LiveClient.KINDS[cat][kind])]
			)
			caption.text = line if cat == 2 else "%s +%d" % [line, enchant]
			cells = ItemGrid.add(body, live.lots.size(), 220, press_lot, show_lot)
			for i in live.lots.size():
				cells[i].icon = ItemSlot.item_icon(int(live.lots[i].item.id))
			var row := HBoxContainer.new()
			row.name = "Pages"
			row.alignment = BoxContainer.ALIGNMENT_CENTER
			row.add_theme_constant_override("separation", 16)
			var prev := Button.new()
			prev.name = "Prev"
			prev.text = "live.prev"
			prev.pressed.connect(turn_page.bind(-1))
			row.add_child(prev)
			page_line = Label.new()
			page_line.name = "Page"
			page_line.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
			page_line.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			page_line.custom_minimum_size = Vector2(200, 0)
			page_line.text = tr("live.page") % [page + 1, maxi(1, live.pages)]
			row.add_child(page_line)
			var next := Button.new()
			next.name = "Next"
			next.text = "live.next"
			next.pressed.connect(turn_page.bind(1))
			row.add_child(next)
			body.add_child(row)
			if not cells.is_empty():
				cells[0].grab_focus.call_deferred()
				if info.text.is_empty():
					show_lot(0)


func lot_count(e: int) -> int:
	return int(live.counts[e]) if e < live.counts.size() else 0


func choose_category(i: int) -> void:
	if cat != i:
		kind = 0
	cat = i
	show_step(Step.KIND)


func choose_kind(k: int) -> void:
	if live.busy:
		return
	kind = k
	enchant = 0
	page = 0
	if cat == 2:
		live.ask_page(cat, kind, 0, 0, LiveClient.later(self, &"paged"))
	else:
		live.ask_counts(cat, kind, LiveClient.later(self, &"counted"))


func counted(err: String) -> void:
	if err.is_empty():
		show_step(Step.ENCHANT)
	else:
		info.text = tr("live.failed")


func choose_enchant(e: int) -> void:
	if live.busy:
		return
	enchant = e
	if lot_count(e) == 0:
		info.text = tr("live.no_items")
		return
	page = 0
	live.ask_page(cat, kind, enchant, page, LiveClient.later(self, &"paged"))


func paged(err: String) -> void:
	match err:
		"":
			show_step(Step.LOTS)
		"none":  # nothing (left) of this kind
			if page > 0:
				page -= 1
				live.ask_page(cat, kind, enchant, page, LiveClient.later(self, &"paged"))
			elif step == Step.LOTS:
				if note.is_empty():
					note = tr("live.no_items")
				go_back()
			else:
				info.text = tr("live.no_items")
		_:
			note = ""
			info.text = tr("live.failed")


func turn_page(by: int) -> void:
	if live.busy:
		return
	if page + by < 0:
		info.text = tr("live.top")
		return
	if page + by >= live.pages:
		info.text = tr("live.no_more")
		return
	page += by
	live.ask_page(cat, kind, enchant, page, LiveClient.later(self, &"paged"))


func show_lot(i: int) -> void:
	if i < live.lots.size():
		var lot: Dictionary = live.lots[i]
		info.text = "%s\n%s" % [Items.describe(lot.item), tr("live.price") % int(lot.price)]


## Asks before buying the lot of a place. Returns the question, or why not.
func press_lot(i: int) -> String:
	if live.busy or i >= live.lots.size():
		return ""
	var lot: Dictionary = live.lots[i]
	if int(lot.price) > int(profile.gold):
		info.text = tr("live.need_gold")
		return info.text
	into_warehouse = LiveClient.free_place(profile) < 0
	asked = lot
	if into_warehouse:
		ask.dialog_text = tr("live.to_warehouse_ask")
	else:
		ask.dialog_text = tr("live.buy_ask") % [Items.name_of(int(lot.item.id)), int(lot.price)]
	ask.popup_centered()
	return ask.dialog_text


## Yes: the lot asked about is bought.
func confirm() -> void:
	if asked.is_empty() or live.busy:
		return
	live.buy(profile, asked, into_warehouse, LiveClient.later(self, &"bought"))


func bought(err: String) -> void:
	var lot := asked
	asked = {}
	match err:
		"":
			profile.save(path)
			gold.text = str(profile.gold)
			note = tr("live.bought") % Items.name_of(int(lot.item.id))
			info.text = note
			live.ask_page(cat, kind, enchant, page, LiveClient.later(self, &"paged"))
		"gold":
			info.text = tr("live.need_gold")
		"full":
			info.text = tr("live.warehouse_full" if into_warehouse else "live.backpack_full")
		"gone":
			note = tr("live.sold_out")
			info.text = note
			live.ask_page(cat, kind, enchant, page, LiveClient.later(self, &"paged"))
		_:
			info.text = tr("live.failed")


## Back one step (the enchant levels are asked for again), or out of Buy.
func go_back() -> void:
	if live != null and live.busy:
		return
	match step:
		Step.LOTS:
			if cat == 2:
				show_step(Step.KIND)
			else:
				live.ask_counts(cat, kind, LiveClient.later(self, &"counted"))
		Step.ENCHANT:
			show_step(Step.KIND)
		Step.KIND:
			show_step(Step.CATEGORY)
		_:
			Router.back()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		go_back()
