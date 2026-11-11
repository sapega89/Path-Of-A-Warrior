extends "res://tests/test_case.gd"
## A mission lost, as the original: from level 10 on the hero may lose a thing he wears.


## Gives the numbers it is told, as rng.below would.
class Rolls:
	extends JavaRandom
	var values: Array = []
	var asked: Array = []

	func _init(v: Array) -> void:
		values = v

	func below(hi: int) -> int:
		asked.append(hi)
		return int(values.pop_front())


func test_lose_gear_chance_and_place() -> void:
	var p: RefCounted = Profile.new()
	p.level = 9
	var r := Rolls.new([0, 0])
	eq(p.lose_gear(r), {}, "up to level 9 nothing is lost")
	eq(r.asked, [], "not even rolled")
	p.level = 40
	r = Rolls.new([10])
	eq(p.lose_gear(r), {}, "level 40: a roll of 10 of 100 keeps it (chance 40 / 4)")
	eq(r.asked, [100], "one roll")
	r = Rolls.new([9, 0])
	var lost: Dictionary = p.lose_gear(r)
	eq(int(lost.get("id", 0)), Profile.START_WEAPON, "a roll of 9: the weapon (place 0) is lost")
	eq(r.asked, [100, Items.EQUIPPED], "the place: one of the 9")
	eq(int(p.equipped[0].id), 0, "the place is empty")
	eq(p.lose_gear(Rolls.new([0, 0])), {}, "an empty place: nothing")
	p.equipped[4] = Items.make(Profile.START_WEAPON)
	eq(int(p.lose_gear(Rolls.new([0, 4])).get("id", 0)), Profile.START_WEAPON, "any of the places")


func test_lost_gear_on_the_fail_banner() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = Router.make(Router.SCREENS["mission"])
	root.add_child(screen)
	screen.profile.level = 40
	# a seed whose rolls lose the weapon: below 10 of 100, then place 0
	var s := 0
	while true:
		var t := JavaRandom.new(s)
		if t.below(100) < 10 and t.below(Items.EQUIPPED) == 0:
			break
		s += 1
	screen.sim.rng = JavaRandom.new(s)
	screen.sim.failed = true
	screen.sim.banner = MapSim.BANNER_FAILED
	screen._process(0.0)
	eq(int(screen.lost_gear.get("id", 0)), Profile.START_WEAPON, "the weapon is lost")
	eq(int(screen.profile.equipped[0].id), 0, "taken from the hero")
	var text: String = screen.banner_text.text
	# no flask was bought, so the lost mission also ends the run
	var lines: PackedStringArray = [
		tr("mission.failed"),
		tr("run.over"),
		tr("mission.lost"),
		Items.name_of(Profile.START_WEAPON)
	]
	check(text.ends_with("\n".join(lines)), "the banner names it: %s" % text)
	screen._process(0.0)
	eq(int(screen.profile.equipped[0].id), 0, "once")
	screen.free()
	Router.params = old


func test_a_flask_on_the_fail_banner() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = Router.make(Router.SCREENS["mission"])
	root.add_child(screen)
	screen.profile.run.flasks = 1
	screen.profile.run.flasks_left = 1
	screen.sim.failed = true
	screen.sim.banner = MapSim.BANNER_FAILED
	screen._process(0.0)
	var text: String = screen.banner_text.text
	check(text.contains(tr("run.flask_used") % 0), "a flask is spent: %s" % text)
	check(not screen.run_over, "the run goes on")
	screen.free()
	Router.params = old
