extends BaseScreen
## Trade (in the game menu, and at the auctioneer in the camp): Buy Item, Sell Item, Cancel Sale,
## the Gift List and Give a Gift (the Live client in Router.params goes on to each page).

@onready var buttons: Array[Button] = [
	%Column.get_node("Buy"),
	%Column.get_node("Sell"),
	%Column.get_node("Cancel"),
	%Column.get_node("Gifts"),
	%Column.get_node("Give")
]


func _ready() -> void:
	buttons[0].grab_focus.call_deferred()


## A page of the trade, with the Live client of this one.
func open_page(screen: String) -> void:
	Router.push(screen, Router.params)
