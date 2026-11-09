extends Control
## Blacksmith: Buy, Sell, Enchant and Combine, each a page of things (the shop screen).
## Combine with fewer than 3 things in the Inventory only says so, as pyport's popup 39.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
## Things the Inventory needs for Combine to open.
const COMBINE_AT_LEAST := 3
## Page button name, text key, shop mode (empty: not open yet).
const PAGES := [
	["Buy", "blacksmith.buy", "buy"],
	["Sell", "blacksmith.sell", "sell"],
	["Enchant", "blacksmith.enchant", "enchant"],
	["Combine", "blacksmith.combine", "combine"],
]

var buttons: Array[Button] = []
var notice: AcceptDialog


func _ready() -> void:
	var col := UiTheme.menu_column(self)
	col.add_child(UiTheme.heading("blacksmith.title", 44))
	for page in PAGES:
		var b := Button.new()
		b.name = page[0]
		b.text = page[1]
		var mode: String = page[2]
		b.disabled = mode.is_empty()
		if not b.disabled:
			b.pressed.connect(open_page.bind(mode))
		col.add_child(b)
		buttons.append(b)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	notice = AcceptDialog.new()
	notice.name = "Notice"
	notice.title = ""
	notice.dialog_text = "combine.too_few"
	add_child(notice)
	buttons[0].grab_focus.call_deferred()


## The page of `mode`; Combine only with 3 things or more in the Inventory. False when it does
## not open.
func open_page(mode: String) -> bool:
	if mode == "combine" and things() < COMBINE_AT_LEAST:
		notice.popup_centered()
		return false
	var p := Router.params.duplicate()
	p["mode"] = mode
	Router.push("shop", p)
	return true


## The things in the hero's Inventory.
func things() -> int:
	var profile: RefCounted = Profile.load_or_new(
		str(Router.params.get("profile_path", Profile.PATH))
	)
	return profile.backpack.filter(func(it): return int(it.get("id", 0)) > 0).size()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
