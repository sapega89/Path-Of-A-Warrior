class_name LiveNews
extends Control
## What Live kept for the player while away, shown over the main menu: the notices (once a
## game, page by page), the Sale List (what other players bought from him; the money is in the
## Safe), the Gift List (five at a time; the gifts are in the Warehouse), and the Exp and Fame
## kept on the server, which the hero gets now (and maybe a level or more).
##
## It first sends the hero's gold and backpack to Live (scripts/net/live_client.gd sync), then
## asks what is new. A notice or the Exp and Fame is a popup; a list is shown in place of the
## menu (showing_list) until OK. finished comes when everything is read, or at once when the
## server does not answer: Trade, Warehouse and Safe say that themselves.

signal showing_list(on: bool)
signal finished

const LIST_PLACES := 20

var live: RefCounted
var path: String
var list: VBoxContainer  # the Sale List / Gift List
var list_kind := ""  # "sold" or "gifts"
var list_title: Label
var list_text: Label
var list_cells: Array[Button] = []
var list_info: Label
var list_ok: Button
var note: AcceptDialog  # a page of the notices, the Exp / Fame applied
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
	list_title = UiTheme.heading("live.sale_list", 44)
	list.add_child(list_title)
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
		list_kind = "sold"
		live.ask_sold(LiveClient.later(self, &"_listed"))
	else:
		_read_gifts()


## The gifts come five at a time, until there are no more.
func _read_gifts() -> void:
	if live.has_gifts:
		list_kind = "gifts"
		live.ask_gifts(LiveClient.later(self, &"_listed"))
	else:
		_read_fame()


func _read_fame() -> void:
	live.ask_fame(LiveClient.later(self, &"_famed"))


## The Sale List or a page of the Gift List came: shown until OK.
func _listed(err: String) -> void:
	var entries := entries_shown()
	if not err.is_empty() or entries.is_empty():
		if list_kind == "sold":
			_read_gifts()
		else:
			_read_fame()
		return
	list_title.text = "live.sale_list" if list_kind == "sold" else "live.gift_list"
	list_text.text = tr("live.sold_lines" if list_kind == "sold" else "live.gift_lines")
	for i in list_cells.size():
		list_cells[i].visible = i < maxi(entries.size(), 5)
		list_cells[i].icon = (
			ItemSlot.item_icon(int(entries[i].item.id)) if i < entries.size() else null
		)
	_set_list_shown(true)
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
		list_info.text = (
			"%s\n%s\n%s"
			% [
				Items.name_of(int(it.id)),
				tr("live.price") % int(e.price),
				tr("live.enchant_lv") % int(it.enchant)
			]
		)
	else:
		list_info.text = "%s\n%s\n%s" % [str(e.from), Items.name_of(int(it.id)), Items.describe(it)]


## OK under a list: after the Sale List the gifts, after a page of gifts the next one.
func list_done() -> void:
	if live.busy:
		return
	_set_list_shown(false)
	_read_gifts()


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
