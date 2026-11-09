class_name InventoryScreen
extends BaseScreen
## Inventory: the hero's gold and the 45 places of the backpack (it scrolls).
## Picking gear wears it (what was worn in its place comes into the backpack instead); a stat
## item (HP, MP, ATK, DEF up) is used up. Gear above the hero's level cannot be taken. Every change
## is saved at once.

const COLUMNS := 5

var profile: RefCounted
var path: String = Profile.PATH
var cells: Array[Button] = []
var gold: Label
var info: Label


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	profile.compact_backpack()
	var col := UiTheme.menu_column(self, 640)
	col.add_child(UiTheme.heading("inventory.title", 44))

	var gold_row := HBoxContainer.new()
	gold_row.name = "Gold"
	gold_row.alignment = BoxContainer.ALIGNMENT_CENTER
	gold_row.add_child(UiTheme.coin_rect())
	gold = Label.new()
	gold.name = "Value"
	gold.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	gold.custom_minimum_size = Vector2(160, 0)
	gold.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	gold_row.add_child(gold)
	col.add_child(gold_row)

	var grid := GridContainer.new()
	grid.name = "Backpack"
	grid.columns = COLUMNS
	grid.add_theme_constant_override("h_separation", 6)
	grid.add_theme_constant_override("v_separation", 6)
	for i in Items.BACKPACK:
		var b := ItemSlot.button("Cell%d" % i)
		var at := i
		b.pressed.connect(func(): press_cell(at))
		b.focus_entered.connect(func(): _show_info(at))
		b.mouse_entered.connect(func(): _show_info(at))
		grid.add_child(b)
		cells.append(b)
	var scroll := ScrollContainer.new()
	scroll.name = "Scroll"
	scroll.custom_minimum_size = Vector2(0, 340)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.follow_focus = true
	var center := CenterContainer.new()
	center.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	center.add_child(grid)
	scroll.add_child(center)
	col.add_child(scroll)

	info = Label.new()
	info.name = "Info"
	info.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	info.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	info.custom_minimum_size = Vector2(0, 72)
	col.add_child(info)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	refresh()
	_show_info(0)
	cells[0].grab_focus.call_deferred()


## Wears or uses the thing in the cell. Returns the line shown ("" when worn).
func press_cell(i: int) -> String:
	var said: String = profile.use_item(i)
	if said == "cannot":
		info.text = tr("inventory.cannot_take")
		return said
	profile.save(path)
	refresh()
	info.text = said if not said.is_empty() else describe(i)
	return said


func refresh() -> void:
	gold.text = str(profile.gold)
	for i in cells.size():
		cells[i].icon = ItemSlot.item_icon(int(profile.backpack[i].id))


func describe(i: int) -> String:
	return Items.describe(profile.backpack[i])


func _show_info(i: int) -> void:
	info.text = describe(i)


## The line of control hints under the screen (scripts/ui/hint_bar.gd): what picking a thing does.
func controls_hint() -> String:
	return InputSetup.hint("hint.grid_inventory")
