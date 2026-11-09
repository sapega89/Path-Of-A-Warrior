class_name LiveSafeScreen
extends Control
## Game menu > Safe: gold between the hero (Local) and the Safe on the server. The arrow between
## the two says which way it goes, out of the Safe at first; it turns when pressed. The amount
## is typed in (no more than there is on that side) and OK moves it; the hero is saved then.

const ARROWS := ["res://assets/original/ui/arrow1.png", "res://assets/original/ui/arrow3.png"]

var live: RefCounted
var profile: RefCounted
var path: String = Profile.PATH
var to_safe := false  # the arrow points at the Safe (else at the hero)
var local: Label
var server: Label
var arrow: Button
var amount: LineEdit
var ok: Button
var info: Label


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	profile = Profile.load_or_new(path)
	live = LiveClient.of(Router.params)
	var col := UiTheme.menu_column(self, 640)
	col.add_child(UiTheme.heading("live.safe", 44))
	var row := HBoxContainer.new()
	row.name = "Sides"
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	row.add_theme_constant_override("separation", 24)
	local = _side(row, "Local", "live.local")
	arrow = Button.new()
	arrow.name = "Arrow"
	arrow.custom_minimum_size = Vector2(96, 64)
	arrow.expand_icon = true
	arrow.icon_alignment = HORIZONTAL_ALIGNMENT_CENTER
	arrow.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	arrow.pressed.connect(turn)
	row.add_child(arrow)
	server = _side(row, "Server", "live.server")
	col.add_child(row)
	var ask := Label.new()
	ask.text = "live.how_much"
	ask.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	col.add_child(ask)
	amount = LineEdit.new()
	amount.name = "Amount"
	amount.alignment = HORIZONTAL_ALIGNMENT_CENTER
	amount.max_length = 9
	amount.text_changed.connect(_typed)
	amount.text_submitted.connect(func(_t: String) -> void: submit())
	col.add_child(amount)
	ok = Button.new()
	ok.name = "Ok"
	ok.text = "live.ok"
	ok.pressed.connect(submit)
	col.add_child(ok)
	info = UiTheme.note("Info", 60)
	col.add_child(info)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	refresh()
	amount.grab_focus.call_deferred()
	if live == null:
		info.text = tr("live.failed")
		return
	info.text = tr("live.connecting")
	live.sync(profile, LiveClient.later(self, &"synced"))


func _side(row: HBoxContainer, node_name: String, caption_key: String) -> Label:
	var box := VBoxContainer.new()
	box.name = node_name
	box.custom_minimum_size = Vector2(200, 0)
	var caption := Label.new()
	caption.text = caption_key
	caption.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	box.add_child(caption)
	var gold := UiTheme.gold_row("Gold")
	box.add_child(gold)
	row.add_child(box)
	return gold.get_node("Value")


func synced(err: String) -> void:
	refresh()
	info.text = "" if err.is_empty() else tr("live.failed")


## The gold on the side the arrow comes from.
func source() -> int:
	if to_safe:
		return int(profile.gold)
	return 0 if live == null else int(live.safe)


func turn() -> void:
	to_safe = not to_safe
	_typed(amount.text)
	refresh()


## Only digits, and no more than there is.
func _typed(t: String) -> void:
	var digits := ""
	for c in t:
		if c >= "0" and c <= "9":
			digits += c
	if not digits.is_empty():
		digits = str(mini(int(digits), source()))
	if digits != t:
		amount.text = digits
		amount.caret_column = digits.length()


## Moves the amount typed. Returns false when nothing was asked of the server.
func submit() -> bool:
	if live == null or live.busy or not live.synced:
		return false
	if source() == 0:
		info.text = tr("live.no_gold" if to_safe else "live.no_safe_gold")
		return false
	var n := int(amount.text)
	if n <= 0:
		return false
	live.move_gold(profile, to_safe, n, LiveClient.later(self, &"moved"))
	return true


func moved(err: String) -> void:
	if err.is_empty():
		profile.save(path)
		amount.text = ""
		info.text = ""
	else:
		info.text = tr("live.out_of_range" if err == "gold" else "live.failed")
	refresh()


func refresh() -> void:
	local.text = str(profile.gold)
	server.text = "-" if live == null or not live.synced else str(live.safe)
	arrow.icon = load(ARROWS[1 if to_safe else 0])


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
