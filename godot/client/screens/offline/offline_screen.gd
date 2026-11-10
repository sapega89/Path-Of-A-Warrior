class_name OfflineScreen
extends BaseScreen
## "No connection": the game starts only online (scripts/net/cloud.gd). Shown by the main
## menu while the server is not there, or refused the stored login. OK (or a click) tries
## again, and so does the screen itself every AUTO_RETRY_MS; on a refused login BACK forgets
## the stored account (the game asks for one again). Once online, the main menu comes back.
## OK and BACK are named for the device just used, as pyport's: Enter / Esc, A / B, or OK / Back
## on a phone, in the line of hints under the screen. The buttons under the text do the same: Try
## again, and Another account on a
## refused login.

const AUTO_RETRY_MS := 10000

@onready var text: Label = %Text
@onready var retry: Button = %Retry
@onready var other: Button = %Other  # on a refused login: forget it and log in with another account
var shown_at := 0


func _ready() -> void:
	retry.grab_focus.call_deferred()
	shown_at = Time.get_ticks_msec()
	refresh()
	InputSetup.device_changed.connect(_on_device)


func lines() -> String:
	if Cloud.refused():
		return tr("offline.refused")
	return "%s\n\n%s" % [tr("offline.no_connection"), tr("offline.only_online")]


func refresh() -> void:
	text.text = lines()
	other.visible = Cloud.refused()


## Forgets the stored login (the game asks for one again) and tries again.
func other_account() -> void:
	Cloud.forget_account()
	try_again()


## The keys are named for the device just used (Enter / Esc or A / B).
func _on_device(_device: String) -> void:
	if text.text != tr("offline.connecting"):
		refresh()


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


## Back is another account, and only once the server refused this one.
func handles_back() -> bool:
	return Cloud.refused()


func go_back() -> void:
	other_account()


func _screen_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_accept") and get_viewport().gui_get_focus_owner() == null:
		get_viewport().set_input_as_handled()
		try_again()


## A click anywhere tries again (in a window the screen itself takes the click).
func _gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed:
		accept_event()
		try_again()


## The keys of the buttons, in the line of control hints under the screen (scripts/ui/hint_bar.gd).
func controls_hint() -> String:
	if Cloud.refused():
		return (
			"%s · %s"
			% [InputSetup.hint("offline.try_again"), InputSetup.hint("offline.other_account")]
		)
	return InputSetup.hint("offline.try_again")
