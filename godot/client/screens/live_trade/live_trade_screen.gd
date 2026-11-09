extends BaseScreen
## Game menu > Trade: Buy Item, Sell Item and Cancel Sale (the Live client in Router.params goes on
## to each page).

@onready var buttons: Array[Button] = [
	%Column.get_node("Buy"), %Column.get_node("Sell"), %Column.get_node("Cancel")
]


func _ready() -> void:
	buttons[0].grab_focus.call_deferred()


## A page of the trade, with the Live client of this one.
func open_page(screen: String) -> void:
	Router.push(screen, Router.params)
