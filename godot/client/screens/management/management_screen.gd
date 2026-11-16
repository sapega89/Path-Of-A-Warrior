extends BaseScreen
## Management: the hero's pages between missions: Attributes, Skills and the Inventory (his
## gear, backpack and belt in one window).

@onready var buttons: Array[Button] = [
	%Column.get_node("Attributes"),
	%Column.get_node("Skills"),
	%Column.get_node("Inventory"),
]


func _ready() -> void:
	buttons[0].grab_focus.call_deferred()


## One of the hero's pages, with the params of this one (which hero).
func open_page(screen: String) -> void:
	Router.push(screen, Router.params)
