extends Control
## Live: the hero on the game server (Settings server_url). Logs in as the guest of this
## device, then saves the hero to the server or loads him from it over the one here, each
## after a question, as the original's Live did. Params: profile_path, server_url (optional).

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const NetClient := preload("res://scripts/core/net_client.gd")

var path: String = Profile.PATH
var net: NetClient
var status: Label
var info: Label
var buttons: Array[Button] = []
var ask_box: ConfirmationDialog
var asked := ""  # "save" or "load": what the open question is about
var busy := false


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	var col := UiTheme.menu_column(self, 560)
	col.add_child(UiTheme.heading("live.title", 44))
	status = Label.new()
	status.name = "Status"
	status.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	status.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	col.add_child(status)
	_add(col, "Save", "live.save", func(): _ask("save"))
	_add(col, "Load", "live.load", func(): _ask("load"))
	_add(col, "Back", "common.back", func(): Router.back())
	info = Label.new()
	info.name = "Info"
	info.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	info.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	info.custom_minimum_size = Vector2(0, 80)
	col.add_child(info)
	ask_box = ConfirmationDialog.new()
	ask_box.name = "Ask"
	ask_box.confirmed.connect(func(): run(asked))
	add_child(ask_box)
	net = NetClient.new()
	net.name = "Net"
	add_child(net)
	buttons[0].grab_focus.call_deferred()
	connect_server()


func _add(col: VBoxContainer, node_name: String, key: String, on_press: Callable) -> void:
	var b := Button.new()
	b.name = node_name
	b.text = key
	b.pressed.connect(on_press)
	col.add_child(b)
	buttons.append(b)


func server_url() -> String:
	return str(Router.params.get("server_url", Settings.get_value("server_url")))


## Connects and logs in. True when the hero can be saved or loaded.
func connect_server() -> bool:
	_set_busy(true)
	status.text = tr("live.connecting")
	var ok := net.open(server_url()) and await net.login()
	status.text = (tr("live.online") % net.account) if ok else tr("live.offline")
	_set_busy(not ok)
	buttons[2].disabled = false
	return ok


func _set_busy(on: bool) -> void:
	busy = on
	for b in buttons:
		b.disabled = on


func _ask(what: String) -> void:
	if busy:
		return
	asked = what
	ask_box.dialog_text = tr("live.ask_" + what)
	ask_box.popup_centered()


## Saves or loads. Returns the line shown.
func run(what: String) -> String:
	_set_busy(true)
	var said := ""
	var got: Dictionary = await net.ask("hero_get")
	if str(got.type) != "hero_get_ok":
		said = tr("live.error") % str(got.get("code", ""))
	elif what == "save":
		var put: Dictionary = await net.ask("hero_put",
			{"hero": Profile.load_or_new(path).to_dict(), "rev": int(got.rev)})
		said = tr("live.saved") if str(put.type) == "hero_put_ok" else tr("live.error") % str(put.get("code", ""))
	elif got.hero == null:
		said = tr("live.nothing")
	else:
		var p: RefCounted = Profile.new()
		p.from_dict(got.hero)
		p.save(path)
		said = tr("live.loaded")
	info.text = said
	_set_busy(false)
	return said


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
