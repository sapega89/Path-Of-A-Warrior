extends BaseScreen
## Management: the hero's pages between missions: Attributes, Skills, Gear, Inventory and
## Assign Items.

@onready var buttons: Array[Button] = [
	%Column.get_node("Attributes"),
	%Column.get_node("Skills"),
	%Column.get_node("Gear"),
	%Column.get_node("Inventory"),
	%Column.get_node("AssignItems"),
]


func _ready() -> void:
	buttons[0].grab_focus.call_deferred()


## One of the hero's pages, with the params of this one (which hero).
func open_page(screen: String) -> void:
	Router.push(screen, Router.params)
