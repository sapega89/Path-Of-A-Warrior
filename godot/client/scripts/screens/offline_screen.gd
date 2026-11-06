extends Control
## "No connection": the game starts only online (scripts/net/cloud.gd). Shown by the main
## menu while the server is not there, or refused the stored login. OK (or a click) tries
## again, and so does the screen itself every AUTO_RETRY_MS; on a refused login BACK forgets
## the stored account (the game asks for one again). Once online, the main menu comes back.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const AUTO_RETRY_MS := 10000

var text: Label
var shown_at := 0


func _ready() -> void:
	var col := UiTheme.menu_column(self, 640)
	text = Label.new()
	text.name = "Text"
	text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	text.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	col.add_child(text)
	shown_at = Time.get_ticks_msec()
	refresh()


func lines() -> String:
	if Cloud.refused():
		return "%s\n\n%s\n%s" % [tr("offline.refused"), tr("offline.try_again"), tr("offline.other_account")]
	return "%s\n\n%s\n\n%s" % [tr("offline.no_connection"), tr("offline.only_online"), tr("offline.try_again")]


func refresh() -> void:
	text.text = lines()


func try_again() -> void:
	shown_at = Time.get_ticks_msec()
	Cloud.retry_now()
	text.text = tr("offline.connecting")


func _process(_delta: float) -> void:
	if Cloud.online() or not Cloud.enabled():
		Router.go("main_menu")
		return
	if not Cloud.refused() and Time.get_ticks_msec() - shown_at >= AUTO_RETRY_MS:
		try_again()
	elif Cloud.refused() and text.text == tr("offline.connecting"):
		refresh()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel") and Cloud.refused():
		get_viewport().set_input_as_handled()
		Cloud.forget_account()
		try_again()
	elif event.is_action_pressed("ui_accept") or (event is InputEventMouseButton and event.pressed):
		get_viewport().set_input_as_handled()
		try_again()
