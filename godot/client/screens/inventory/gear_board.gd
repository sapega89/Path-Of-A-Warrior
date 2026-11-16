class_name GearBoard
extends Control
## The hero's gear in the Inventory (gear_board.tscn): the hero as a 3D figure of the new art
## (his class, his blade) standing on a round stage in the middle of a panel, and the nine places
## around him (weapon, head, body, ...), each with what is worn there; an empty place shows a
## faint picture of what goes there. It only shows: a place picked or pointed at is said up to
## the screen with a signal.

signal place_pressed(place: int)
signal place_pointed(place: int)

var places: Array[Button] = []
var ghosts: Array[TextureRect] = []  # the faint pictures of the empty places
var blade := -1  # the weapon kind the figure holds

@onready var figure: ArtFigure = %Figure  # the hero


func _ready() -> void:
	for i in Items.EQUIPPED:
		var place: Button = get_node("Place%d" % i)
		var ghost: TextureRect = place.get_node("Ghost")
		ghost.texture = ItemSlot.item_icon(_sample(i))
		place.pressed.connect(place_pressed.emit.bind(i))
		place.focus_entered.connect(place_pointed.emit.bind(i))
		place.mouse_entered.connect(place_pointed.emit.bind(i))
		places.append(place)
		ghosts.append(ghost)


## The hero standing in his own small world (a light, the air), turned a little to the side; his
## picture fills the middle of the panel.
func show_hero(hero: Profile) -> void:
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
	figure.setup(MapPeople.HEROES[clampi(hero.head, 0, 3)])
	show_gear(hero)


## What the hero wears: the icon in each place and, when the kind of his weapon changed, the
## blade in his hand, breathing in its idle clip.
func show_gear(hero: Profile) -> void:
	for i in places.size():
		places[i].icon = ItemSlot.item_icon(int(hero.equipped[i].id))
		ghosts[i].visible = places[i].icon == null
	var weapon := hero.weapon_kind()
	if weapon == blade:
		return
	blade = weapon
	figure.unequip_all()
	figure.equip(MapPeople.BLADES[clampi(weapon, 0, 1)])
	figure.play(Motion.idle(weapon), 0.0)


## A thing worn in place i (the first gear that goes there), for the picture of an empty place.
static func _sample(i: int) -> int:
	for id in range(101, 601):
		if not Items.info(id).is_empty() and Items.place(id) == i:
			return id
	return 0
