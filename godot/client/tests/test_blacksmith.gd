extends "res://tests/test_case.gd"

const Profile := preload("res://scripts/core/profile.gd")
const Items := preload("res://scripts/core/items.gd")
const Shop := preload("res://scripts/screens/shop_screen.gd")
const TEST_PATH := "user://test_blacksmith.json"


func test_prices() -> void:
	eq(Items.price({"id": 1}), 60, "a Red Potion (S)")
	eq(Items.price({"id": 11}), 200, "a Handy Dynamite")
	var blade := Items.make(101)
	eq(int(blade.attack), 2, "an Iron Sabre: ATK+2")
	eq(Items.price(blade), 120 + 200, "its price and 100 a point")
	eq(Items.price(Items.make(501)), 150000, "a rare thing has its own price")
	eq(Items.enchant_price(blade), 200, "enchanting costs 100 a point")


func test_tiers_by_level() -> void:
	eq(Items.tier(1, 0), 0, "a new hero finds tier 0 gear mostly")
	eq(Items.tier(1, 79), 0, "80 % of it")
	eq(Items.tier(1, 80), 1, "and 20 % tier 1")
	eq(Items.tier(70, 0), 2, "at level 70 at least tier 2")
	eq(Items.tier(70, 99), 4, "and a third tier 4")


func test_the_shop_is_filled() -> void:
	var p := Profile.new()
	var rng := RandomNumberGenerator.new()
	rng.seed = 3
	p.fill_shop(rng)
	eq(p.shop.size(), 25, "25 things")
	for i in Items.SHOP_POTIONS.size():
		eq(int(p.shop[i].id), int(Items.SHOP_POTIONS[i]), "potions and scrolls first")
	var last := 0
	for i in range(8, 25):
		var id := int(p.shop[i].id)
		check(id > 100 and id <= 200, "a gear: %d" % id)
		check(id >= last, "the cheapest first")
		last = id


func test_buy_and_sell() -> void:
	var p := Profile.new()
	p.gold = 100
	eq(p.buy(0), "bought", "a Red Potion (S)")
	eq(p.quick_slots[0], [1, 1], "into a quick slot")
	eq(p.gold, 40, "for 60")
	eq(p.buy(0), "no_gold", "40 is not enough")
	p.gold = 1000
	p.quick_slots[0] = [1, 5]
	eq(p.buy(0), "no_more", "5 at most")
	p.gold = 100000
	var gear: Dictionary = p.shop[8].duplicate()
	eq(p.buy(8), "bought", "a gear")
	eq(int(p.backpack[0].id), int(gear.id), "into the backpack")
	eq(int(p.shop[8].id), 0, "and out of the shop")
	var before := p.gold
	check(p.sell("backpack", 0), "sold")
	eq(p.gold, before + Items.price(gear) / 2, "for half the price")
	eq(int(p.backpack[0].id), 0, "gone")
	check(p.sell("quick", 0), "a potion sold")
	eq(p.quick_slots[0], [1, 4], "one less")


func test_enchanting() -> void:
	var p := Profile.new()
	eq(p.can_enchant({"id": 1, "enchant": 0}), "not_possible", "a potion")
	var blade := Items.make(101)
	eq(p.can_enchant(blade), "ok", "a gear")
	p.gold = 150
	eq(p.enchant(blade), "no_gold", "it costs 200")
	p.gold = 1000
	eq(p.enchant(blade), "success", "the first enchanting always works")
	eq(int(blade.attack), 3, "ATK grows by at least 1")
	eq(int(blade.enchant), 1, "enchanted once")
	eq(p.gold, 800, "for 200")
	blade.enchant = 5
	eq(p.can_enchant(blade), "full", "5 times at most for an Iron Sabre")
	var rng := RandomNumberGenerator.new()
	rng.seed = 11
	var lost := false
	for i in 50:
		var spear := Items.make(301)
		spear.enchant = 8
		p.gold = 100000
		var r: String = p.enchant(spear, rng)
		if r == "lost":
			eq(int(spear.id), 0, "a lost thing is gone")
			lost = true
			break
	check(lost, "an enchanting at 8 loses the thing most often")


func test_shop_screen() -> void:
	var p := Profile.new()
	p.gold = 1000
	p.add_item(Items.make(101))
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH, "mode": "buy"}
	var screen: Control = Shop.new()
	root.add_child(screen)
	eq(screen.cells.size(), 25, "the shop's 25 things")
	check(screen.cells[0].icon != null, "a potion's icon")
	check(screen.describe(0).begins_with("Red Potion (S)"), "its line: %s" % screen.describe(0))
	screen.press_cell(0)
	eq(int(screen.profile.gold), 940, "bought for 60")
	screen.free()
	Router.params = {"profile_path": TEST_PATH, "mode": "enchant"}
	screen = Shop.new()
	root.add_child(screen)
	eq(screen.cells.size(), Items.BACKPACK + Items.EQUIPPED, "the backpack and the Gear page")
	screen.press_cell(0)
	eq(screen.asked, 0, "asks first")
	screen.confirm()
	eq(screen.sparkle, 0, "Yes: the sparkle starts")
	eq(screen.sparkle_cells, [0] as Array[int], "on the thing")
	eq(int(screen.profile.backpack[0].enchant), 0, "not enchanted yet")
	eq(screen.press_cell(1), "", "nothing is pressed while it plays")
	for f in 4:
		eq(screen.next_sparkle(), "", "frame %d" % (f + 2))
	eq(screen.next_sparkle(), screen.info.text, "after the fifth frame the outcome")
	eq(screen.sparkle, -1, "and the sparkle is gone")
	eq(int(screen.profile.backpack[0].enchant), 1, "enchanted")
	screen.free()
	var saved: RefCounted = Profile.load_or_new(TEST_PATH)
	eq(int(saved.backpack[0].enchant), 1, "saved")
	eq(int(saved.quick_slots[0][0]), 1, "the potion bought is kept")
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))


func test_combine() -> void:
	eq(Items.mixes([186, 101, 156]), [342], "an Iron Sabre and two more make a treasure")
	eq(Items.mixes([101, 101, 101]), [], "three blades make nothing")
	var p := Profile.new()
	for id in [101, 156, 186]:
		p.add_item(Items.make(id))
	var rng := RandomNumberGenerator.new()
	rng.seed = 5
	var plan: Dictionary = p.combine_plan([0, 1, 2], rng)
	eq(int(plan.result.id), 342, "what they make")
	eq(int(plan.price), Items.price(plan.result) / 4, "a quarter of its price")
	eq(p.combine_plan([0, 1, 3], rng), {}, "an empty place: nothing")
	p.gold = 0
	eq(p.combine([0, 1, 2], plan), "no_gold", "the fee first")
	p.gold = 100000
	plan.success = true
	eq(p.combine([0, 1, 2], plan), "success", "combined")
	eq(int(p.backpack[0].id), 0, "the first is used up")
	eq(int(p.backpack[1].id), 0, "the second too")
	eq(int(p.backpack[2].id), 342, "the new thing in the third's place")
	for id in [101, 156, 186]:
		p.add_item(Items.make(id))
	plan.success = false
	plan.lost = 1
	eq(p.combine([0, 1, 3], plan), "fail", "it failed")
	eq(int(p.backpack[1].id), 0, "and lost one")
	eq(int(p.backpack[0].id), 101, "the others stay")


func test_combine_screen() -> void:
	var p := Profile.new()
	p.gold = 100000
	for id in [101, 156, 186]:
		p.add_item(Items.make(id))
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH, "mode": "combine"}
	var screen: Control = Shop.new()
	root.add_child(screen)
	eq(screen.info.text, screen.tr("combine.select"), "choose three")
	screen.press_cell(0)
	screen.press_cell(1)
	eq(screen.chosen, [0, 1] as Array[int], "two chosen")
	screen.press_cell(1)
	eq(screen.chosen.size(), 1, "the second chosen no more")
	screen.press_cell(1)
	screen.press_cell(2)
	eq(screen.asked, 2, "three: the fee is asked")
	screen.plan.success = true
	screen.confirm()
	eq(screen.sparkle_cells, [0, 1, 2] as Array[int], "the sparkle on the three")
	screen._process(0.5)
	eq([screen.sparkle, int(screen.profile.backpack[2].id)], [4, 186], "its fifth frame, not yet combined")
	screen._process(0.1)
	eq(screen.sparkle, -1, "after 0.6 s the sparkle is gone")
	eq(int(screen.profile.backpack[2].id), 342, "combined")
	eq(screen.chosen.size(), 0, "nothing chosen now")
	screen.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))


## As pyport's popup 39: Combine with fewer than 3 things in the Inventory only says so.
func test_combine_needs_three_things() -> void:
	var p := Profile.new()
	for id in [101, 156]:
		p.add_item(Items.make(id))
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	var host := Control.new()
	root.add_child(host)
	Router.attach(host)
	Router.go("blacksmith", {"profile_path": TEST_PATH})
	var smith: Control = Router.current
	eq(smith.things(), 2, "two things")
	check(not smith.open_page("combine"), "Combine does not open")
	check(smith.notice.visible, "it says why")
	eq(smith.notice.dialog_text, "combine.too_few", "\"at least 3 items\"")
	eq(Router.current_name(), "blacksmith", "still the Blacksmith")
	smith.notice.hide()
	check(smith.open_page("sell"), "the other pages open")
	Router.back()
	p.add_item(Items.make(186))
	p.save(TEST_PATH)
	smith = Router.current
	check(smith.open_page("combine"), "three: Combine opens")
	eq(Router.current_name(), "shop", "the Combine page")
	Router.attach(null)
	host.free()
	Router.params = old
	DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH))
