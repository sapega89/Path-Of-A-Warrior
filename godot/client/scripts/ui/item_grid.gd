class_name ItemGrid
extends ScrollContainer
## A grid of item places (ItemSlot buttons), five a row, centred in a box that scrolls when it is
## higher than its custom_minimum_size (scenes/ui/item_grid.tscn). Placed in a scene, or added
## by code with add().

const SCENE := "res://scenes/ui/item_grid.tscn"


## Makes n places; pressing place i calls press(i), focusing or pointing at it calls show(i).
## Returns the places' buttons.
func fill(n: int, press: Callable, show: Callable) -> Array[Button]:
	var things: GridContainer = $Center/Things
	var cells: Array[Button] = []
	for i in n:
		var b := ItemSlot.button("Cell%d" % i)
		var at := i
		b.pressed.connect(func(): press.call(at))
		b.focus_entered.connect(func(): show.call(at))
		b.mouse_entered.connect(func(): show.call(at))
		things.add_child(b)
		cells.append(b)
	return cells


## Takes every place away (for fill() again).
func clear() -> void:
	var things: GridContainer = $Center/Things
	for c in things.get_children():
		things.remove_child(c)
		c.queue_free()


## Adds a grid of n places, `height` high, to `col` (see fill()). Returns the places' buttons.
static func add(
	col: Container, n: int, height: int, press: Callable, show: Callable
) -> Array[Button]:
	var grid: ItemGrid = (load(SCENE) as PackedScene).instantiate()
	grid.custom_minimum_size = Vector2(0, height)
	col.add_child(grid)
	return grid.fill(n, press, show)


## The Backpack / Warehouse buttons (scenes/ui/grid_sides.tscn) in a row under `col`;
## side(true) is called for the Warehouse, side(false) for the backpack.
static func sides(col: Container, side: Callable) -> Array[Button]:
	var row: GridSides = (load(GridSides.SCENE) as PackedScene).instantiate()
	row.chosen.connect(side)
	col.add_child(row)
	return row.tabs()
