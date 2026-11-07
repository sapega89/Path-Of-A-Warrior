extends Control
## Login: the account the hero is kept under on the server (UserID 4-12 letters A-Z, password
## 4-12 digits), the same account for Live and multiplayer. The main menu opens it on Play,
## Continue and New game while this run of the game has no account yet: Log in takes an account
## made before, New account registers this UserID and password. The account is kept only until
## the game is closed (scripts/net/cloud.gd). Once logged in and the hero (or none) has come
## from the server, the screen goes back and calls Router.params.next on the screen under it
## (the main menu's play or new_game). Back returns there without logging in (to the main menu
## when params.must: the game menu opened it, which needs an account). The keys under the
## fields (scripts/ui/key_grid.gd) type with a gamepad; they show only while it is in use.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Protocol := preload("res://scripts/net/protocol.gd")
const KeyGrid := preload("res://scripts/ui/key_grid.gd")

var user_id: LineEdit
var password: LineEdit
var info: Label
var keys: VBoxContainer
var login_button: Button
var register_button: Button
var busy := false
var waiting := false  # logged in, the hero not here yet
var next := ""
var must := false


func _ready() -> void:
	next = str(Router.params.get("next", ""))
	must = bool(Router.params.get("must", false))
	var col := UiTheme.menu_column(self, 520)
	col.add_child(UiTheme.heading("login.title", 40))
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
	login_button = _button(col, "Login", "login.ok", submit)
	register_button = _button(col, "Register", "login.new", submit.bind(true))
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


func _button(col: VBoxContainer, node_name: String, text_key: String, on_press: Callable) -> Button:
	var b := Button.new()
	b.name = node_name
	b.text = text_key
	b.pressed.connect(on_press)
	col.add_child(b)
	return b


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


## Log in (or, with new_account, register) with the typed account.
func submit(new_account := false) -> void:
	if busy or waiting:
		return
	var p := problem()
	if not p.is_empty():
		info.text = p
		return
	busy = true
	info.text = tr("offline.connecting")
	if new_account:
		Cloud.register(user_id.text, password.text, answered)
	else:
		Cloud.login(user_id.text, password.text, answered)


func answered(r: Dictionary) -> void:
	busy = false
	if r.get("ok", false):
		waiting = true
		_process(0.0)
		return
	info.text = error_text(str(r.get("err", "offline")))


static func error_text(err: String) -> String:
	var key := "register.err_" + err.replace(" ", "_")
	var text := TranslationServer.translate(key)
	return text if text != key else TranslationServer.translate("register.err_offline")


## Logged in: once the hero (or none) has come from the server, on to what was asked.
func _process(_delta: float) -> void:
	if waiting and (Cloud.online() or not Cloud.enabled()):
		waiting = false
		done()


func done() -> void:
	var then := next
	Router.back()
	if not then.is_empty() and Router.current != null and Router.current.has_method(then):
		Router.current.call(then)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		if busy or waiting:
			return
		if must or Router.depth() < 2:
			Router.go("main_menu")
		else:
			Router.back()
