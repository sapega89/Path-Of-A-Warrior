extends BaseScreen
## Game menu > Trade: Buy Item, Sell Item and Cancel Sale (the Live client in Router.params goes on
## to each page).

## Page button name, text key, screen.
const PAGES := [
	["Buy", "live.buy", "live_buy"],
	["Sell", "live.sell", "live_sell"],
	["Cancel", "live.cancel", "live_cancel"],
]

var buttons: Array[Button] = []


func _ready() -> void:
	var col := UiTheme.menu_column(self)
	col.add_child(UiTheme.heading("live.trade", 44))
	for page in PAGES:
		var b := Button.new()
		b.name = page[0]
		b.text = page[1]
		var screen: String = page[2]
		b.pressed.connect(func(): Router.push(screen, Router.params))
		col.add_child(b)
		buttons.append(b)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	buttons[0].grab_focus.call_deferred()
