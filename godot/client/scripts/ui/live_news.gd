class_name LiveNews
extends Control
## What Live kept for the player while away, shown over the main menu: the notices (once a
## game, page by page), the Sale List (what other players bought from him; the money is in the
## Safe), a note that gifts came (once a game; they are in the Warehouse, and the Gift List is at
## the auctioneer: screens/live_gifts), and the Exp and Fame kept on the server, which the hero
## gets now (and maybe a level or more).
##
## It first sends the hero's gold and backpack to Live (scripts/net/live_client.gd sync), then
## asks what is new. A notice, the gifts or the Exp and Fame is a popup; the Sale List is shown
## in place of the menu (showing_list) until OK. finished comes when everything is read, or at
## once when the server does not answer: Trade, Warehouse and Safe say that themselves.

signal showing_list(on: bool)
signal finished

const LIST_PLACES := 20

var live: RefCounted
var path: String
var list: VBoxContainer  # the Sale List
var list_cells: Array[Button] = []
var list_info: Label
var list_ok: Button
var note: AcceptDialog  # a page of the notices, the gifts came, the Exp / Fame applied
var after_note: Callable
var done := false


func _init(live_client: RefCounted, profile_path: String = Profile.PATH) -> void:
	live = live_client
	path = profile_path
	name = "LiveNews"
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE  # the menu under it takes the clicks


func _ready() -> void:
	_build_list()
	note = AcceptDialog.new()
	note.name = "Note"
	note.title = tr("live.title")
	note.confirmed.connect(_note_closed)
	note.canceled.connect(_note_closed)
	add_child(note)
	live.sync(Profile.load_or_new(path), LiveClient.later(self, &"_synced"))


func _build_list() -> void:
	var col := UiTheme.menu_column(self, 640)
	list = VBoxContainer.new()
	list.name = "List"
	list.visible = false
	list.add_theme_constant_override("separation", 8)
	list.add_child(UiTheme.heading("live.sale_list", 44))
	var text := UiTheme.note("Text")
	text.text = tr("live.sold_lines")
	list.add_child(text)
	list_cells = ItemGrid.add(list, LIST_PLACES, 140, func(_i): pass, show_entry)
	list_info = UiTheme.note("Info", 100)
	list.add_child(list_info)
	list_ok = Button.new()
	list_ok.name = "Ok"
	list_ok.text = "live.ok"
	list_ok.pressed.connect(list_done)
	list.add_child(list_ok)
	col.add_child(list)


func _synced(err: String) -> void:
	if not err.is_empty():
		_finish()
		return
	live.ask_status(LiveClient.later(self, &"_statused"))


func _statused(err: String) -> void:
	if not err.is_empty():
		_finish()
		return
	_read_notices()


func _read_notices() -> void:
	if live.has_notice and not live.notices_seen:
		live.ask_notices(LiveClient.later(self, &"_noticed"))
	else:
		_read_sold()


func _noticed(err: String) -> void:
	if not err.is_empty():
		_read_sold()
		return
	_show_note(
		"\n".join(live.notice),
		func() -> void:
			if live.more_notices:
				live.ask_notices(LiveClient.later(self, &"_noticed"))
			else:
				_read_sold()
	)


func _read_sold() -> void:
	if live.has_sold:
		live.ask_sold(LiveClient.later(self, &"_listed"))
	else:
		_tell_gifts()


## The gifts are not read here (that is the auctioneer's Gift List): only told of, once a game.
func _tell_gifts() -> void:
	if live.has_gifts and not live.gifts_told:
		live.gifts_told = true
		_show_note(tr("live.gifts_waiting"), _read_fame)
	else:
		_read_fame()


func _read_fame() -> void:
	live.ask_fame(LiveClient.later(self, &"_famed"))


## The Sale List came: shown until OK.
func _listed(err: String) -> void:
	var entries: Array = live.sold
	if not err.is_empty() or entries.is_empty():
		_tell_gifts()
		return
	for i in list_cells.size():
		list_cells[i].visible = i < maxi(entries.size(), 5)
		list_cells[i].icon = (
			ItemSlot.item_icon(int(entries[i].item.id)) if i < entries.size() else null
		)
	_set_list_shown(true)
	show_entry(0)
	list_ok.grab_focus.call_deferred()


func show_entry(i: int) -> void:
	if i >= live.sold.size():
		list_info.text = ""
		return
	var e: Dictionary = live.sold[i]
	var it: Dictionary = e.item
	list_info.text = (
		"%s\n%s\n%s"
		% [
			Items.name_of(int(it.id)),
			tr("live.price") % int(e.price),
			tr("live.enchant_lv") % int(it.enchant)
		]
	)


## OK under the Sale List: then the gifts.
func list_done() -> void:
	if live.busy:
		return
	_set_list_shown(false)
	_tell_gifts()


## The Exp and Fame kept on the server go to the hero (and maybe a level or more).
func _famed(err: String) -> void:
	if not err.is_empty() or (live.fame == 0 and live.exp_points == 0):
		_finish()
		return
	var profile: RefCounted = Profile.load_or_new(path)
	profile.fame = mini(int(profile.fame) + live.fame, 0x7FFFFFFF)
	var levels: int = profile.gain_exp(live.exp_points)
	profile.save(path)
	var text := tr("live.fame_applied") % [live.exp_points, live.fame]
	if levels > 0:
		text += "\n" + tr("live.level_up") % levels
	_show_note(text, _finish)


func _show_note(text: String, then: Callable) -> void:
	note.dialog_text = text
	after_note = then
	note.popup_centered()


func _note_closed() -> void:
	var then := after_note
	after_note = Callable()
	if then.is_valid():
		then.call()


func _set_list_shown(on: bool) -> void:
	list.visible = on
	mouse_filter = Control.MOUSE_FILTER_STOP if on else Control.MOUSE_FILTER_IGNORE
	showing_list.emit(on)


func _finish() -> void:
	done = true
	finished.emit()
