extends Control
## Live, the market on the server (scripts/net/live_client.gd): Trade, Warehouse, Safe and
## Multiplayer. Opening it sends the hero's gold and backpack to the server; until the answer
## comes it says "Connecting...", and without one (no server, the connection broke) "Network
## connection has failed" with only Back.
##
## Then, as in pyport, what the server kept for the player comes before the menu: the notices
## (once a game), the Sale List (what other players bought from him; the money is in the Safe),
## the Gift List (the gifts are in the Warehouse), and the Exp and Fame kept on the server, which
## the hero gets now.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Items := preload("res://scripts/core/items.gd")
const ItemSlot := preload("res://scripts/ui/item_slot.gd")
const ItemGrid := preload("res://scripts/ui/item_grid.gd")
const LiveClient := preload("res://scripts/net/live_client.gd")
## Page button name, text key, screen (empty: not open yet).
const PAGES := [
	["Trade", "live.trade", "live_trade"],
	["Warehouse", "live.warehouse", "live_warehouse"],
	["Safe", "live.safe", "live_safe"],
	["Multiplayer", "live.multiplayer", "online"],
]
const LIST_PLACES := 20

var live: RefCounted
var profile: RefCounted
var path: String = Profile.PATH
var status: Label
var menu: VBoxContainer
var buttons: Array[Button] = []
var back: Button
## The opening: "notices", "sold", "gifts", "fame", "menu", then "" (the menu is open).
var stage := ""
var list: VBoxContainer  # the Sale List / Gift List
var list_kind := ""  # "sold" or "gifts"
var list_text: Label
var list_cells: Array[Button] = []
var list_info: Label
var list_ok: Button
var note: AcceptDialog  # a page of the notices, the Exp / Fame applied
var after_note: Callable


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	profile = Profile.load_or_new(path)
	live = LiveClient.of(Router.params)
	var col := UiTheme.menu_column(self, 640)
	col.add_child(UiTheme.heading("live.title", 44))
	status = UiTheme.note("Status")
	col.add_child(status)
	menu = VBoxContainer.new()
	menu.name = "Menu"
	menu.add_theme_constant_override("separation", 8)
	for page in PAGES:
		var b := Button.new()
		b.name = page[0]
		b.text = page[1]
		b.disabled = true
		var screen: String = page[2]
		if not screen.is_empty():
			b.pressed.connect(func(): Router.push(screen, Router.params))
		menu.add_child(b)
		buttons.append(b)
	col.add_child(menu)
	_build_list(col)
	back = Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	note = AcceptDialog.new()
	note.name = "Note"
	note.title = tr("live.title")
	note.confirmed.connect(_note_closed)
	note.canceled.connect(_note_closed)
	add_child(note)
	back.grab_focus.call_deferred()
	if live == null:
		status.text = tr("live.failed")
		return
	status.text = tr("live.connecting")
	live.sync(profile, LiveClient.later(self, &"synced"))


func _build_list(col: VBoxContainer) -> void:
	list = VBoxContainer.new()
	list.name = "List"
	list.visible = false
	list.add_theme_constant_override("separation", 8)
	list_text = UiTheme.note("Text")
	list.add_child(list_text)
	list_cells = ItemGrid.add(list, LIST_PLACES, 140, func(_i): pass, show_entry)
	list_info = UiTheme.note("Info", 100)
	list.add_child(list_info)
	list_ok = Button.new()
	list_ok.name = "Ok"
	list_ok.text = "live.ok"
	list_ok.pressed.connect(list_done)
	list.add_child(list_ok)
	col.add_child(list)


func synced(err: String) -> void:
	if not err.is_empty():
		failed()
		return
	live.ask_status(LiveClient.later(self, &"statused"))


func statused(err: String) -> void:
	if not err.is_empty():
		failed()
		return
	status.text = ""
	stage = "notices"
	advance()


func failed() -> void:
	stage = ""
	status.text = tr("live.failed")
	for b in buttons:
		b.disabled = true


## The next thing of the opening: notices (once a game), Sale List, Gift List, Exp / Fame, then
## the menu.
func advance() -> void:
	match stage:
		"notices":
			stage = "sold"
			if live.has_notice and not live.notices_seen:
				live.ask_notices(LiveClient.later(self, &"noticed"))
				return
			advance()
		"sold":
			stage = "gifts"
			list_kind = "sold"
			if live.has_sold:
				live.ask_sold(LiveClient.later(self, &"listed"))
				return
			advance()
		"gifts":
			list_kind = "gifts"
			if live.has_gifts:  # five at a time, until there are no more
				live.ask_gifts(LiveClient.later(self, &"listed"))
				return
			stage = "fame"
			advance()
		"fame":
			stage = "menu"
			live.ask_fame(LiveClient.later(self, &"famed"))
		"menu":
			stage = ""
			open_menu()


func open_menu() -> void:
	status.text = ""
	list.visible = false
	menu.visible = true
	for i in buttons.size():
		buttons[i].disabled = str(PAGES[i][2]).is_empty()
	for b in buttons:
		if not b.disabled:
			b.grab_focus.call_deferred()  # after Back's, asked for in _ready
			break


func noticed(err: String) -> void:
	if not err.is_empty():
		advance()
		return
	_show_note("\n".join(live.notice), func() -> void:
		if live.more_notices:
			live.ask_notices(LiveClient.later(self, &"noticed"))
		else:
			advance())


func _show_note(text: String, then: Callable) -> void:
	note.dialog_text = text
	after_note = then
	note.popup_centered()


func _note_closed() -> void:
	var then := after_note
	after_note = Callable()
	if then.is_valid():
		then.call()


## The Sale List or a page of the Gift List came: shown until OK.
func listed(err: String) -> void:
	var entries := entries_shown()
	if not err.is_empty() or entries.is_empty():
		if list_kind == "gifts":
			stage = "fame"
		advance()
		return
	status.text = tr("live.sale_list" if list_kind == "sold" else "live.gift_list")
	list_text.text = tr("live.sold_lines" if list_kind == "sold" else "live.gift_lines")
	for i in list_cells.size():
		list_cells[i].visible = i < maxi(entries.size(), 5)
		list_cells[i].icon = ItemSlot.item_icon(int(entries[i].item.id)) if i < entries.size() else null
	menu.visible = false
	list.visible = true
	show_entry(0)
	list_ok.grab_focus.call_deferred()


func entries_shown() -> Array:
	return live.sold if list_kind == "sold" else live.gifts


func show_entry(i: int) -> void:
	var entries := entries_shown()
	if i >= entries.size():
		list_info.text = ""
		return
	var e: Dictionary = entries[i]
	var it: Dictionary = e.item
	if list_kind == "sold":
		list_info.text = "%s\n%s\n%s" % [Items.name_of(int(it.id)), tr("live.price") % int(e.price),
			tr("live.enchant_lv") % int(it.enchant)]
	else:
		list_info.text = "%s\n%s\n%s" % [str(e.from), Items.name_of(int(it.id)), Items.describe(it)]


func list_done() -> void:
	if live.busy:
		return
	list.visible = false
	menu.visible = true
	status.text = ""
	advance()


## The Exp and Fame kept on the server go to the hero (and maybe a level or more).
func famed(err: String) -> void:
	if not err.is_empty() or (live.fame == 0 and live.exp_points == 0):
		advance()
		return
	profile.fame = mini(int(profile.fame) + live.fame, 0x7FFFFFFF)
	var levels: int = profile.gain_exp(live.exp_points)
	profile.save(path)
	var text := tr("live.fame_applied") % [live.exp_points, live.fame]
	if levels > 0:
		text += "\n" + tr("live.level_up") % levels
	_show_note(text, advance)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
