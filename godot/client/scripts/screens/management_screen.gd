extends Control
## Management: the hero's pages between missions. Attributes and Skills are open; Gear,
## Inventory and Assign Items are shown greyed until they have their pages.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
## Page button name, text key, screen (empty: not open yet).
const PAGES := [
	["Attributes", "management.attributes", "attributes"],
	["Skills", "management.skills", "skills"],
	["Gear", "management.gear", ""],
	["Inventory", "management.inventory", ""],
	["AssignItems", "management.assign_items", ""],
]

var buttons: Array[Button] = []


func _ready() -> void:
	var col := UiTheme.menu_column(self)
	col.add_child(UiTheme.heading("management.title", 44))
	for page in PAGES:
		var b := Button.new()
		b.name = page[0]
		b.text = page[1]
		var screen: String = page[2]
		b.disabled = screen.is_empty()
		if not b.disabled:
			b.pressed.connect(func(): Router.push(screen, Router.params))
		col.add_child(b)
		buttons.append(b)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	buttons[0].grab_focus.call_deferred()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
