extends Control
## Blacksmith: Buy, Sell, Enchant and Combine, each a page of things (the shop screen).

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
## Page button name, text key, shop mode (empty: not open yet).
const PAGES := [
	["Buy", "blacksmith.buy", "buy"],
	["Sell", "blacksmith.sell", "sell"],
	["Enchant", "blacksmith.enchant", "enchant"],
	["Combine", "blacksmith.combine", ""],
]

var buttons: Array[Button] = []


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
	buttons[0].grab_focus.call_deferred()


func open_page(mode: String) -> void:
	var p := Router.params.duplicate()
	p["mode"] = mode
	Router.push("shop", p)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
