extends Control
## Gear: the hero in the middle of the original frame and the nine places around him (weapon,
## head, body, ...), each with what is worn there. Picking a place takes off what is worn
## there into the backpack and opens the Inventory to choose what to wear instead.
## The line at the bottom says what the thing under the cursor is.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Items := preload("res://scripts/core/items.gd")
const ItemSlot := preload("res://scripts/ui/item_slot.gd")
const HeroSprite := preload("res://scripts/world/hero.gd")
const SCALE := 2
## The places around the middle of the frame, in original pixels (top-left of the 28 px icon).
const PLACE_DX := [-77, -77, -77, -33, 3, 47, 47, 47, -15]
const PLACE_DY := [21, -15, -51, -79, -79, -51, -15, 21, 49]

var profile: RefCounted
var path: String = Profile.PATH
var places: Array[Button] = []
var info: Label

var _frame: Texture2D = preload("res://assets/original/ui/ui_equipbox.png")


func _ready() -> void:
	path = str(Router.params.get("profile_path", Profile.PATH))
	profile = Profile.load_or_new(path)
	var col := UiTheme.menu_column(self, 640)
	col.add_child(UiTheme.heading("gear.title", 44))

	var board := Control.new()
	board.name = "Board"
	var size_px := Vector2(_frame.get_size()) * SCALE
	board.custom_minimum_size = size_px + Vector2(0, 8)
	var center := CenterContainer.new()
	center.add_child(board)
	col.add_child(center)
	var mid := Vector2(size_px.x / 2.0, size_px.y / 2.0)
	var frame := TextureRect.new()
	frame.texture = _frame
	frame.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	frame.stretch_mode = TextureRect.STRETCH_SCALE
	frame.size = size_px
	board.add_child(frame)
	board.add_child(_hero_figure(mid))
	for i in Items.EQUIPPED:
		var b := ItemSlot.button("Place%d" % i)
		b.position = mid + Vector2(PLACE_DX[i] - 1, PLACE_DY[i] - 1) * SCALE - Vector2(3, 3)
		b.size = b.custom_minimum_size
		var at := i
		b.pressed.connect(func(): press_place(at))
		b.focus_entered.connect(func(): _show_info(at))
		b.mouse_entered.connect(func(): _show_info(at))
		board.add_child(b)
		places.append(b)

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
	places[0].grab_focus.call_deferred()


## Takes off what is worn in the place and opens the Inventory.
func press_place(i: int) -> void:
	if profile.unequip(i):
		profile.save(path)
	refresh()
	Router.push("inventory", Router.params)


func refresh() -> void:
	for i in places.size():
		places[i].icon = ItemSlot.item_icon(int(profile.equipped[i].id))
		# an empty place shows the frame's own picture of what goes there
		places[i].self_modulate = Color(1, 1, 1, 1) if places[i].icon != null else Color(1, 1, 1, 0.25)


func describe(i: int) -> String:
	return Items.describe(profile.equipped[i])


func _show_info(i: int) -> void:
	info.text = describe(i)


## The hero standing, from his sheet (the sword he holds), feet a little below the middle.
func _hero_figure(mid: Vector2) -> TextureRect:
	var data: Dictionary = HeroSprite.load_info()
	var cell: Array = data.get("cell", [96, 96])
	var origin: Array = data.get("origin", [48, 72])
	var columns := int(data.get("columns", 16))
	var idle: Array = data.get("idle", [[1]])
	var f := int(idle[0][0])
	var t := AtlasTexture.new()
	t.atlas = load(HeroSprite.SHEET_PATH % [0, profile.weapon_kind()])
	t.region = Rect2((f % columns) * int(cell[0]), (f / columns) * int(cell[1]), int(cell[0]), int(cell[1]))
	var r := TextureRect.new()
	r.name = "Hero"
	r.texture = t
	r.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	r.stretch_mode = TextureRect.STRETCH_SCALE
	r.size = Vector2(int(cell[0]), int(cell[1])) * SCALE
	r.position = mid + Vector2(-int(origin[0]), 24 - int(origin[1])) * SCALE
	r.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return r


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		Router.back()
