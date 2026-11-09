class_name ItemGrid
extends RefCounted
## A grid of item places (ItemSlot buttons), five a row, centred in a box that scrolls when it is
## higher than `height`; and the two buttons that switch Live's grids between the backpack and
## the Warehouse.

const COLUMNS := 5


## Adds a grid of n places to `col`; pressing place i calls press(i), focusing or pointing at
## it calls show(i). Returns the places' buttons.
static func add(
	col: Container, n: int, height: int, press: Callable, show: Callable
) -> Array[Button]:
	var grid := GridContainer.new()
	grid.name = "Things"
	grid.columns = COLUMNS
	grid.add_theme_constant_override("h_separation", 6)
	grid.add_theme_constant_override("v_separation", 6)
	var cells: Array[Button] = []
	for i in n:
		var b := ItemSlot.button("Cell%d" % i)
		var at := i
		b.pressed.connect(func(): press.call(at))
		b.focus_entered.connect(func(): show.call(at))
		b.mouse_entered.connect(func(): show.call(at))
		grid.add_child(b)
		cells.append(b)
	var scroll := ScrollContainer.new()
	scroll.name = "Scroll"
	scroll.custom_minimum_size = Vector2(0, height)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.follow_focus = true
	var center := CenterContainer.new()
	center.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	center.add_child(grid)
	scroll.add_child(center)
	col.add_child(scroll)
	return cells


## The Backpack / Warehouse buttons in a row under `col` (the backpack chosen);
## side(true) is called for the Warehouse, side(false) for the backpack.
static func sides(col: Container, side: Callable) -> Array[Button]:
	var row := HBoxContainer.new()
	row.name = "Sides"
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	var group := ButtonGroup.new()
	var tabs: Array[Button] = []
	for t in [["Backpack", "live.backpack"], ["Warehouse", "live.warehouse"]]:
		var b := Button.new()
		b.name = t[0]
		b.text = t[1]
		b.toggle_mode = true
		b.button_group = group
		b.custom_minimum_size = Vector2(220, 0)
		var wh: bool = t[0] == "Warehouse"
		b.pressed.connect(func(): side.call(wh))
		row.add_child(b)
		tabs.append(b)
	tabs[0].button_pressed = true
	col.add_child(row)
	return tabs
