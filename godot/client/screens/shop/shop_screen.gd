class_name ShopScreen
extends BaseScreen
## A page of the Blacksmith (Router.params "mode"): the hero's gold over a grid of things.
## Buy: the shop's potions, scrolls and gears. Sell: the quick slots' potions, then the
## backpack, for half the price. Enchant: the backpack, then what the hero wears; enchanting
## costs gold, asks first, and can fail or lose the thing. Combine: three things of the
## backpack chosen (a gold border) make one new thing, for a fee, or fail and maybe lose
## one of them. Every change is saved at once. After Yes to Enchant or Combine a sparkle plays
## on the thing (on each of the three) for five steps of 120 ms, then comes the outcome; it is
## drawn in the new art by the Sparkle node (EnchantSparkle).

const QUICK := 5
const SPARKLE_STEPS := 5
const SPARKLE_FRAME := 0.12  # seconds a step lasts, as a frame of the menus

var profile: Profile
var path: String = Profile.PATH
var mode := "buy"
var cells: Array[Button] = []
var asked := -1  # the cell waiting for the answer to "Continue?"
var chosen: Array[int] = []  # Combine: the backpack places chosen
var plan := {}  # Combine: what the three chosen make (Profile.combine_plan)
var rng := RandomNumberGenerator.new()
var sparkle := -1  # the sparkle's step now, -1: none
var sparkle_cells: Array[int] = []  # the cells it plays on

var _sparkle_time := 0.0

@onready var gold: Label = %Gold.get_node("Value")
@onready var info: Label = %Info
@onready var ask: ConfirmationDialog = %Ask

@onready var _sparkle_view: EnchantSparkle = %Sparkle


func _ready() -> void:
	path = profile_path()
	mode = str(Router.params.get("mode", "buy"))
	profile = Profile.load_or_new(path)
	profile.compact_backpack()
	%Heading.text = "blacksmith." + mode
	var grid: GridContainer = %Things
	for i in cell_count():
		var b := ItemSlot.button("Cell%d" % i)
		var at := i
		b.pressed.connect(func(): press_cell(at))
		b.focus_entered.connect(func(): _show_info(at))
		b.mouse_entered.connect(func(): _show_info(at))
		grid.add_child(b)
		cells.append(b)
	set_process(false)
	refresh()
	_show_info(0)
	if mode == "combine":
		info.text = tr("combine.select")
	cells[0].grab_focus.call_deferred()


func cell_count() -> int:
	match mode:
		"sell":
			return QUICK + Items.BACKPACK
		"enchant":
			return Items.BACKPACK + Items.EQUIPPED
		"combine":
			return Items.BACKPACK
	return profile.shop.size()


## The thing in a cell (a potion of a quick slot as {id}).
func item_at(i: int) -> Dictionary:
	match mode:
		"sell":
			if i < QUICK:
				var it := Items.empty()
				it.id = int(profile.quick_slots[i][0])
				return it
			return profile.backpack[i - QUICK]
		"enchant":
			if i < Items.BACKPACK:
				return profile.backpack[i]
			return profile.equipped[i - Items.BACKPACK]
		"combine":
			return profile.backpack[i]
	return profile.shop[i]


## Buys, sells, or asks to enchant the thing of the cell. Returns the line shown.
func press_cell(i: int) -> String:
	if sparkle >= 0:
		return ""
	var item := item_at(i)
	var id := int(item.id)
	if id == 0:
		return ""
	var said := ""
	match mode:
		"buy":
			var r: String = Blacksmith.buy(profile, i)
			said = tr("shop." + r).replace("%s", _name(id))
			if r == "bought":
				profile.save(path)
		"sell":
			var where := "quick" if i < QUICK else "backpack"
			var thing := _name(id)
			if Blacksmith.sell(profile, where, i if i < QUICK else i - QUICK):
				profile.save(path)
				said = tr("shop.sold").replace("%s", thing)
		"enchant":
			var can: String = Blacksmith.can_enchant(item)
			if can != "ok":
				said = tr("enchant." + can)
			else:
				asked = i
				ask.dialog_text = tr("enchant.ask").replace("%d", str(Items.enchant_price(item)))
				ask.popup_centered()
				said = ask.dialog_text
		"combine":
			said = _choose(i)
	refresh()
	info.text = said
	return said


## Combine: a thing chosen, or chosen no more. With three, what they make is worked out
## and the fee asked.
func _choose(i: int) -> String:
	if int(profile.backpack[i].id) <= 100:
		return ""
	if i in chosen:
		chosen.erase(i)
		return Items.describe(profile.backpack[i])
	chosen.append(i)
	if chosen.size() < 3:
		return Items.describe(profile.backpack[i])
	plan = Blacksmith.combine_plan(profile, chosen, rng)
	if plan.is_empty():
		chosen.clear()
		return tr("combine.not_possible")
	asked = i
	ask.dialog_text = tr("combine.ask").replace("%d", str(int(plan.price)))
	ask.popup_centered()
	return ask.dialog_text


func _cancel() -> void:
	asked = -1
	chosen.clear()
	plan = {}
	refresh()


## The answer Yes to "Continue?": the sparkle starts on the thing, or on the three chosen.
func confirm() -> void:
	if asked < 0 or sparkle >= 0:
		return
	sparkle_cells.clear()
	if mode == "combine":
		sparkle_cells.append_array(chosen)
	else:
		sparkle_cells.append(asked)
	sparkle = 0
	_sparkle_time = 0.0
	set_process(true)
	redraw_sparkle()


func _process(delta: float) -> void:
	_sparkle_time += delta
	while sparkle >= 0 and _sparkle_time >= SPARKLE_FRAME:
		_sparkle_time -= SPARKLE_FRAME
		next_sparkle()
	if sparkle >= 0:
		redraw_sparkle()  # it moves on between the steps too


## The sparkle's next step; after the fifth the outcome. Returns the line shown then.
func next_sparkle() -> String:
	if sparkle < 0:
		return ""
	sparkle += 1
	if sparkle < SPARKLE_STEPS:
		redraw_sparkle()
		return ""
	sparkle = -1
	sparkle_cells.clear()
	redraw_sparkle()
	set_process(false)
	return finish()


## After the sparkle: the thing is enchanted, or the three combined (or not). Returns the
## line shown.
func finish() -> String:
	if asked < 0:
		return ""
	if mode == "combine":
		var c: String = Blacksmith.combine(profile, chosen, plan)
		asked = -1
		chosen.clear()
		plan = {}
		if c != "no_gold":
			profile.save(path)
		var line := tr("shop.no_gold") if c == "no_gold" else tr("combine." + c)
		refresh()
		info.text = line
		return line
	var r: String = Blacksmith.enchant(profile, item_at(asked), rng)
	asked = -1
	if r != "no_gold":
		profile.save(path)
	var said := (
		tr("shop.no_gold")
		if r == "no_gold"
		else tr("enchant.success" if r == "success" else "enchant.fail")
	)
	refresh()
	info.text = said
	return said


## How far the sparkle has played, 0..1 (between its steps too).
func sparkle_phase() -> float:
	if sparkle < 0:
		return 0.0
	var step := clampf(_sparkle_time / SPARKLE_FRAME, 0.0, 1.0)
	return clampf((sparkle + step) / SPARKLE_STEPS, 0.0, 1.0)


## Shows the sparkle over its cells as far as it has played; nothing while it does not play.
func redraw_sparkle() -> void:
	var rects: Array[Rect2] = []
	if sparkle >= 0:
		for i in sparkle_cells:
			rects.append(cells[i].get_global_rect())
	_sparkle_view.show_over(rects, sparkle_phase())


func refresh() -> void:
	gold.text = str(profile.gold)
	for i in cells.size():
		var item := item_at(i)
		cells[i].icon = ItemSlot.item_icon(int(item.id))
		if mode == "sell" and i < QUICK and int(item.id) != 0:
			cells[i].text = str(int(profile.quick_slots[i][1]))
		else:
			cells[i].text = ""
		cells[i].add_theme_stylebox_override("normal", ItemSlot.box(i in chosen))


func describe(i: int) -> String:
	var item := item_at(i)
	if mode == "enchant" or mode == "combine":
		return Items.describe(item)
	return Items.describe_for_sale(item, mode == "sell")


func _name(id: int) -> String:
	if id < 100:
		return (
			str(Items.POTION_NAMES[id - 1]).strip_edges() if id <= Items.POTION_NAMES.size() else ""
		)
	return Items.name_of(id)


func _show_info(i: int) -> void:
	info.text = describe(i)


## The line of control hints under the screen (scripts/ui/hint_bar.gd): what picking a thing does.
func controls_hint() -> String:
	return InputSetup.hint("hint.grid_" + mode)
