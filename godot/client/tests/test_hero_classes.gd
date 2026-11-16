extends "res://tests/test_case.gd"
## The four heroes' base stats and the reset of the attributes.

const TEST_PATH := "user://test_hero_classes.json"


func test_the_faces_are_worth_the_same() -> void:
	var worth := []
	for face in 4:
		var b: Array = Attributes.hero_base(face)
		worth.append(b[0] / 5.0 + b[1] / 3.0 + b[2] + b[3])
	eq(Attributes.hero_base(0), [30, 10, 5, 4], "the Cossack keeps the old numbers")
	for face in 4:
		check(absf(worth[face] - worth[0]) < 0.01, "face %d is worth as many points" % face)
	eq(Attributes.stats_line(1), "HP40 MP7 ATK3 DEF5", "the Serdiuk")


func test_a_new_hero_takes_his_face() -> void:
	var p := Profile.new()
	p.set_head(2)
	eq([p.base_hp, p.base_mp, p.base_attack, p.base_defense], [25, 16, 4, 4], "the Kharakternyk")
	eq(Attributes.spent_points(p), 0, "nothing spent")
	p.spend_point(Profile.Stat.MP)
	p.spend_point(Profile.Stat.ATTACK)
	eq(Attributes.spent_points(p), 2, "two points spent")


func test_reset_with_gold() -> void:
	var p := Profile.new()
	p.set_head(3)
	p.level = 4
	for i in 5:
		p.spend_point(Profile.Stat.HP)
	eq(p.stat_points, 0, "all spent")
	p.gold = 399
	eq(Attributes.reset(p, false), "gold", "400 gold at level 4")
	p.gold = 450
	eq(Attributes.reset(p, false), "", "reset")
	eq(p.gold, 50, "paid")
	eq(p.stat_points, 5, "the points are free again")
	eq(p.base_hp, 25, "the Haidamaka's HP")
	eq(Attributes.reset(p, false), "nothing", "nothing more to reset")


func test_reset_with_an_elixir() -> void:
	var p := Profile.new()
	p.spend_point(Profile.Stat.DEFENSE)
	eq(Attributes.reset(p, true), "item", "no elixir")
	p.backpack[7] = Items.make(435, RandomNumberGenerator.new())
	eq(Attributes.reset_elixir_slot(p), 7, "found")
	eq(Attributes.reset(p, true), "", "reset")
	eq(int(p.backpack[7].id), 0, "the elixir is gone")
	eq(p.stat_points, Profile.START_POINTS, "the point back")


func test_old_save_gets_its_points() -> void:
	# a Serdiuk saved when every face had 30/10/5/4 and 5 points on HP
	var p := Profile.new()
	p.head = 1
	p.base_hp = 55
	p.base_mp = 10
	p.base_attack = 5
	p.base_defense = 4
	p.stat_points = 0
	eq(Attributes.spent_points(p), 5, "worth the 5 points he spent")


func test_reset_on_the_attributes_screen() -> void:
	var p := Profile.new()
	p.gold = 1000
	p.spend_point(Profile.Stat.ATTACK)
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var screen: Control = Router.make(Router.SCREENS["attributes"])
	root.add_child(screen)
	screen.open_reset()
	check(screen.ask.visible, "asked how to pay")
	check(screen.pay_item.text.length() > 0, "the elixir button says there is none")
	screen.ask.hide()
	screen.finish_reset(false)
	var saved: RefCounted = Profile.load_or_new(TEST_PATH)
	eq(saved.gold, 900, "paid 100 at level 1")
	eq(saved.stat_points, Profile.START_POINTS, "saved with the points")
	screen.free()
	Router.params = old
