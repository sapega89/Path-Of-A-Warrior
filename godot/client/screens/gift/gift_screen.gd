class_name GiftScreen
extends BaseScreen
## The gift of the mission just won (Gifts, kept in HeroRun until taken): the general's portrait
## and name over his cards (gift_card.tscn), each with what kind it is, what it gives and its
## icon. The card pressed is the hero's, saved at once, and the screen goes back to the camp.
## A gift is always taken, so Back stays here while there is one.

const CARD := "res://screens/gift/gift_card.tscn"

var path: String = Profile.PATH
var profile: Profile
var cards: Array[Button] = []
var rng := RandomNumberGenerator.new()

@onready var title: Label = %Title
@onready var portrait: TextureRect = %Portrait
@onready var row: HBoxContainer = %Cards


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	var general := MapSim.general_data(profile.run.gift_from)
	portrait.visible = not general.is_empty()
	if general.is_empty():
		title.text = tr("gift.title_none")
	else:
		title.text = tr("gift.title") % tr(str(general.get("name", "")))
		portrait.texture = Pictures.portrait(int(general.get("portrait", 0)))
	var scene := load(CARD) as PackedScene
	for i in profile.run.gift.size():
		var gift: Dictionary = profile.run.gift[i]
		var card: Button = scene.instantiate()
		card.name = "Card%d" % i
		card.text = "%s\n%s" % [tr(Gifts.kind_key(gift)), Gifts.text(profile, gift)]
		card.icon = icon(gift)
		card.pressed.connect(take.bind(i))
		row.add_child(card)
		cards.append(card)
	if not cards.is_empty():
		cards[0].grab_focus.call_deferred()


## The picture of a card: the skill's, the gear's or the potion's icon; none for a stat.
static func icon(gift: Dictionary) -> Texture2D:
	var id := int(gift.get("id", 0))
	match int(gift.get("kind", -1)):
		Gifts.Kind.SKILL:
			return ItemSlot.icon("skill", id)
		Gifts.Kind.GEAR:
			return ItemSlot.item_icon(id)
		Gifts.Kind.POTION:
			return ItemSlot.icon("tool", id - 1)
	return null


## The hero takes card i: saved, and back to the camp.
func take(i: int) -> void:
	profile.run.take_gift(profile, i, rng)
	profile.save(path)
	Router.back()


## Back leaves only when there is no gift to take.
func go_back() -> void:
	if profile.run.gift.is_empty():
		super.go_back()
