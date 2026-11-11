class_name GearScreen
extends BaseScreen
## Gear: the hero as a 3D figure of the new art (his class, his blade) standing on a round
## stage in the middle of a panel, and the nine places around him (weapon, head, body, ...),
## each with what is worn there; an empty place shows a faint picture of what goes there.
## Picking a place takes off what is worn there into the backpack and opens the Inventory to
## choose what to wear instead. The line at the bottom says what the thing under the cursor is.

const SCALE := 2
const BOARD := Vector2(158, 162)  # the panel, in grid pixels
## The places around the middle of the panel, in grid pixels (top-left of the 28 px icon).
const PLACE_DX := [-77, -77, -77, -33, 3, 47, 47, 47, -15]
const PLACE_DY := [21, -15, -51, -79, -79, -51, -15, 21, 49]

var profile: Profile
var path: String = Profile.PATH
var places: Array[Button] = []
var ghosts: Array[TextureRect] = []  # the faint pictures of the empty places
@onready var figure: Node3D = %Figure  # the hero (an ArtFigure)
@onready var info: Label = %Info


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	var board: Control = %Board
	var mid := BOARD * SCALE / 2.0
	_light_the_hero()
	for i in Items.EQUIPPED:
		var b := ItemSlot.button("Place%d" % i)
		b.position = mid + Vector2(PLACE_DX[i] - 1, PLACE_DY[i] - 1) * SCALE - Vector2(3, 3)
		b.size = b.custom_minimum_size
		var ghost := TextureRect.new()
		ghost.name = "Ghost"
		ghost.texture = ItemSlot.item_icon(_sample(i))
		ghost.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		ghost.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		ghost.modulate = Color(0.55, 0.6, 0.72, 0.28)
		ghost.mouse_filter = Control.MOUSE_FILTER_IGNORE
		ghost.set_anchors_preset(Control.PRESET_FULL_RECT)
		ghost.set_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 8)
		b.add_child(ghost)
		ghosts.append(ghost)
		var at := i
		b.pressed.connect(func(): press_place(at))
		b.focus_entered.connect(func(): _show_info(at))
		b.mouse_entered.connect(func(): _show_info(at))
		board.add_child(b)
		places.append(b)

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
		ghosts[i].visible = places[i].icon == null


func describe(i: int) -> String:
	return Items.describe(profile.equipped[i])


func _show_info(i: int) -> void:
	info.text = describe(i)


## A thing worn in place i (the first gear that goes there), for the picture of an empty place.
static func _sample(i: int) -> int:
	for id in range(101, 601):
		if not Items.info(id).is_empty() and Items.place(id) == i:
			return id
	return 0


## The hero standing in his own small world (a light, the air), turned a little to the side,
## breathing in his idle clip; his picture fills the middle of the panel.
func _light_the_hero() -> void:
	var sun: DirectionalLight3D = %Sun
	sun.transform = Transform3D(
		Basis.looking_at(Vector3(-0.4, -0.6, -0.7).normalized(), Vector3.UP), Vector3.ZERO
	)
	var env := Environment.new()
	ArtKit.light(sun, env)
	sun.light_energy = 1.0  # a figure on a stand, not a field: more light on it
	env.ambient_light_energy = 0.45
	env.background_mode = Environment.BG_CLEAR_COLOR
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	(%World as WorldEnvironment).environment = env
	figure.setup(MapPeople.HEROES[clampi(int(profile.head), 0, 3)])
	figure.unequip_all()
	figure.equip(MapPeople.BLADES[clampi(profile.weapon_kind(), 0, 1)])
	figure.play(Motion.idle(profile.weapon_kind()), 0.0)


## The line of control hints under the screen (scripts/ui/hint_bar.gd): what picking a thing does.
func controls_hint() -> String:
	return InputSetup.hint("hint.grid_gear")
