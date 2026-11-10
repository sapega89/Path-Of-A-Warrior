class_name LoginScreen
extends BaseScreen
## Login: the account the hero is kept under on the server (UserID 4-12 letters A-Z, password
## 4-12 digits), the same account for Live. The main menu opens it on Play,
## Continue and New game while this run of the game has no account yet: Log in takes an account
## made before, New account registers this UserID and password. The account is kept only until
## the game is closed (scripts/net/cloud.gd). Once logged in and the hero (or none) has come
## from the server, the screen goes back and calls Router.params.next on the screen under it
## (the main menu's play or new_game). Back returns there without logging in (to the main menu
## when params.must: the game menu opened it, which needs an account). The keys under the
## fields (scripts/ui/key_grid.gd) type with a gamepad; they show only while it is in use.

@onready var user_id: LineEdit = %UserId
@onready var password: LineEdit = %Password
@onready var info: Label = %Info
@onready var login_button: Button = %Login
@onready var register_button: Button = %Register
var keys: VBoxContainer  # under the fields, made for them (KeyGrid)
var busy := false
var waiting := false  # logged in, the hero not here yet
var next := ""
var must := false


func _ready() -> void:
	next = str(Router.params.get("next", ""))
	must = bool(Router.params.get("must", false))
	keys = KeyGrid.create(KeyGrid.ACCOUNT, user_id)
	keys.follow(user_id)
	keys.follow(password)
	password.add_sibling(keys)
	_type_in.call_deferred(user_id)


func _on_user_id_changed(t: String) -> void:
	_keep(user_id, t, "A", "Z", true)


func _on_password_changed(t: String) -> void:
	_keep(password, t, "0", "9", false)


func _on_user_id_submitted(_t: String) -> void:
	_type_in(password)


func _on_password_submitted(_t: String) -> void:
	submit()


func register() -> void:
	submit(true)


## The line of control hints: while a field types on the keyboard, what it takes and what Enter
## does there (the menus' line, with its arrows, would say nothing of typing).
func controls_hint() -> String:
	var f := get_viewport().gui_get_focus_owner() if is_inside_tree() else null
	if InputSetup.device == "keys" and f == user_id:
		return InputSetup.hint("hint.login_user")
	if InputSetup.device == "keys" and f == password:
		return InputSetup.hint("hint.login_password")
	return InputSetup.hint("hint.menu")


## The field takes the focus and types at once (a field reached with Enter or the d-pad would
## otherwise wait for one more Enter or a click before it types).
func _type_in(e: LineEdit) -> void:
	e.grab_focus()
	e.edit()


## Only the characters a UserID (A-Z, typed in any case) or a password (0-9) may have.
func _keep(e: LineEdit, t: String, first: String, last: String, upper: bool) -> void:
	var clean := ""
	for c in t.to_upper() if upper else t:
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


## Back, unless a request is on its way: the main menu when the login must come first.
func go_back() -> void:
	if busy or waiting:
		return
	if must or Router.depth() < 2:
		Router.go("main_menu")
	else:
		Router.back()
