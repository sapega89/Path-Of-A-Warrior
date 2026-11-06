extends "res://tests/test_case.gd"

const Items := preload("res://scripts/core/items.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Gear := preload("res://scripts/screens/gear_screen.gd")
const Inventory := preload("res://scripts/screens/inventory_screen.gd")
const TEST_PATH := "user://test_items.json"


func test_item_data() -> void:
	eq(Items.name_of(116), "Iron Claymore", "the first weapon")
	eq(Items.slot_type(116), 1, "a sword of type 1")
	eq(Items.place(131), 3, "a helmet's place")
	eq(Items.describe(Items.make(116)), "Iron Claymore / ATK+1 / Available at Lv1", "as the Gear page says")
	eq(Items.level_needed(102), 10, "a tier 2 gear")
	eq(Items.icon(116), ["kibo", 0], "gear icon")
	eq(Items.icon(503), ["shinki", 2], "rare icon")
	eq(Items.icon(3), ["tool", 2], "potion icon")
	var rng := RandomNumberGenerator.new()
	rng.seed = 7
	for i in 20:
		var a := int(Items.make(141, rng).hp)
		check(a >= 15 and a <= 30, "a found Lord Armour: HP 15 and up to 15 more, got %d" % a)


func test_new_hero_gear() -> void:
	var p := Profile.new()
	eq(int(p.equipped[0].id), 116, "the claymore in hand")
	eq(p.weapon_kind(), 1, "its sword type")
	eq(p.attack(), 6, "5 + 1")
	eq(p.backpack.size(), 45, "45 places")


func test_wear_and_take_off() -> void:
	var p := Profile.new()
	check(p.add_item(Items.make(126)), "a Half-Axe in the backpack")
	check(p.add_item(Items.make(131)), "a helmet")
	eq(p.use_item(0), "", "the axe is worn")
	eq(int(p.equipped[0].id), 126, "in hand")
	eq(int(p.backpack[0].id), 116, "the claymore went into the backpack")
	eq(p.attack(), 8, "5 + 3")
	eq(p.use_item(1), "", "the helmet is worn")
	eq(int(p.equipped[3].id), 131, "on the head")
	eq(p.defense(), 5, "4 + 1")
	check(p.unequip(3), "taken off")
	eq(p.defense(), 4, "no helmet")
	eq(int(p.backpack[1].id), 131, "back in the backpack")
	p.add_item(Items.make(102))
	eq(p.use_item(2), "cannot", "level 10 gear on a level 1 hero")
	p.add_item(Items.make(434))
	eq(p.use_item(3), "HP Up : 5", "a stat item")
	eq(p.max_hp(), 35, "HP +5")
	eq(int(p.backpack[3].id), 0, "used up")
	p.backpack[0] = Items.empty()
	p.compact_backpack()
	eq(int(p.backpack[0].id), 131, "no holes")
	eq(int(p.backpack[1].id), 102, "in order")


func test_gear_saved() -> void:
	var p := Profile.new()
	p.add_item(Items.make(136))
	p.use_item(0)
	p.save(TEST_PATH)
	var q: RefCounted = Profile.load_or_new(TEST_PATH)
	eq(int(q.equipped[5].id), 136, "the armour worn")
	eq(q.defense(), 7, "4 + 3")
	eq(int(q.equipped[0].id), 116, "the claymore")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))


func test_gear_and_inventory_pages() -> void:
	var p := Profile.new()
	p.add_item(Items.make(131))
	p.add_item(Items.make(102))
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var gear: Control = Gear.new()
	root.add_child(gear)
	eq(gear.places.size(), 9, "nine places")
	check(gear.places[0].icon != null, "the claymore's icon")
	check(gear.places[3].icon == null, "no helmet")
	eq(gear.describe(0), "Iron Claymore / ATK+1 / Available at Lv1", "the weapon")
	gear.free()
	var inv: Control = Inventory.new()
	root.add_child(inv)
	eq(inv.gold.text, "0", "gold")
	eq(inv.press_cell(1), "cannot", "too high a level")
	eq(inv.info.text, "You can't take this equipment.", "said so")
	eq(inv.press_cell(0), "", "the helmet is worn")
	check(inv.cells[0].icon == null, "its place is empty")
	inv.free()
	var saved: RefCounted = Profile.load_or_new(TEST_PATH)
	eq(int(saved.equipped[3].id), 131, "saved")
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))


## A save from when the backpack had 25 places: the 20 new ones are empty.
func test_old_backpack_of_25() -> void:
	var p := Profile.new()
	var d: Dictionary = p.to_dict()
	var old: Array = d.backpack.slice(0, 25)
	old[24] = Items.make(131, RandomNumberGenerator.new())
	d.backpack = old
	var q := Profile.new()
	q.from_dict(d)
	eq(q.backpack.size(), Items.BACKPACK, "45 places")
	eq(int(q.backpack[24].id), 131, "the old last place kept")
	eq(int(q.backpack[44].id), 0, "the new ones empty")
	check(q.add_item(Items.make(102, RandomNumberGenerator.new())), "room for more")
