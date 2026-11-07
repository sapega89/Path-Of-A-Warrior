extends Control
## Registration: the account the hero is kept under on the server (UserID 4-12 letters A-Z,
## password 4-12 digits), the same account for Live and multiplayer. Opened by the game menu
## when the game is always online and this device has no account yet; it cannot be skipped
## (no hero without an account), so Back does nothing. OK registers on the server, then the
## game goes on. The keys under the fields (scripts/ui/key_grid.gd) type with a gamepad too.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Protocol := preload("res://scripts/net/protocol.gd")
const KeyGrid := preload("res://scripts/ui/key_grid.gd")

var user_id: LineEdit
var password: LineEdit
var info: Label
var keys: VBoxContainer
var busy := false


func _ready() -> void:
	var col := UiTheme.menu_column(self, 520)
	col.add_child(UiTheme.heading("register.title", 40))
	var hint := Label.new()
	hint.text = "register.hint"
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hint.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	col.add_child(hint)
	user_id = _field(col, "UserId", "register.user_id", 12)
	user_id.text_changed.connect(func(t: String) -> void: _keep(user_id, t, "A", "Z", true))
	password = _field(col, "Password", "register.password", 12)
	password.secret = true
	password.text_changed.connect(func(t: String) -> void: _keep(password, t, "0", "9", false))
	user_id.text_submitted.connect(func(_t: String) -> void: password.grab_focus())
	password.text_submitted.connect(func(_t: String) -> void: submit())
	keys = KeyGrid.create(KeyGrid.ACCOUNT, user_id)
	keys.follow(user_id)
	keys.follow(password)
	col.add_child(keys)
	var ok := Button.new()
	ok.name = "Ok"
	ok.text = "register.ok"
	ok.pressed.connect(submit)
	col.add_child(ok)
	info = Label.new()
	info.name = "Info"
	info.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	info.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	info.custom_minimum_size = Vector2(0, 60)
	col.add_child(info)
	user_id.grab_focus.call_deferred()


func _field(col: VBoxContainer, node_name: String, hint_key: String, max_len: int) -> LineEdit:
	var e := LineEdit.new()
	e.name = node_name
	e.max_length = max_len
	e.alignment = HORIZONTAL_ALIGNMENT_CENTER
	e.placeholder_text = tr(hint_key)
	col.add_child(e)
	return e


## Only the characters a UserID (A-Z, typed in any case) or a password (0-9) may have.
func _keep(e: LineEdit, t: String, first: String, last: String, upper: bool) -> void:
	var clean := ""
	for c in (t.to_upper() if upper else t):
		if c >= first and c <= last:
			clean += c
	if clean != t:
		var at := e.caret_column
		e.text = clean
		e.caret_column = mini(at, clean.length())


## What is wrong with the typed account, "" when it may be sent.
func problem() -> String:
	if not Protocol.valid_id(user_id.text):
		return tr("register.bad_id")
	if not Protocol.valid_password(password.text):
		return tr("register.bad_password")
	return ""


func submit() -> void:
	if busy:
		return
	var p := problem()
	if not p.is_empty():
		info.text = p
		return
	busy = true
	info.text = tr("offline.connecting")
	Cloud.register(user_id.text, password.text, answered)


func answered(r: Dictionary) -> void:
	busy = false
	if r.get("ok", false):
		Router.back()
		return
	var key := "register.err_" + str(r.get("err", "offline")).replace(" ", "_")
	info.text = tr(key) if tr(key) != key else tr("register.err_offline")


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()  # no hero without an account
		info.text = tr("register.must")
