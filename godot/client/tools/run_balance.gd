extends Node
## The balance of the runs: one new hero plays runs of the campaign on the autopilot
## (Autopilot), headless, as a player would. Before each run he spends his stat points and buys
## in the start camp what his fame pays for (the flasks, then the perks); in each camp he wears
## the better gear, uses the stat things and buys HP potions with half his gold; he takes a
## random card of each gift and goes on by a random open way. Prints a line per mission and per
## run, and when each thing of the start camp was bought:
##   godot --headless --path godot/client res://tools/run_balance.tscn -- <runs> <seed> [vows]
## vows: "hp" (the enemies' HP three steps up and the short time, from run VOWS_FROM) or "all"
## (every vow). Lines that start with RUN and BUY are for scripts:
##   RUN <run> <level> <fame of the run> <missions> <won> <lost>
##   BUY <thing> <after run> <level>

const TICK_CAP := 30000  # a mission not over by then is lost (the autopilot is stuck)
const MAX_MISSIONS := 60  # missions in one run at most
const VOWS_FROM := 10
## The order the stat points go in, round and round.
const POINTS := [Profile.Stat.ATTACK, Profile.Stat.HP, Profile.Stat.DEFENSE, Profile.Stat.HP]
const HP_POTIONS := [3, 2, 1]  # the shop's HP potions, the biggest first
const PERKS := ["reroll", "card", "second_skill"]

var campaign := Campaign.new()
var world := WorldMap.new(campaign)
var rng := RandomNumberGenerator.new()
var vows := ""
var runs_done := 0


func _ready() -> void:
	var args := OS.get_cmdline_user_args()
	var runs := int(args[0]) if args.size() > 0 else 3
	rng.seed = int(args[1]) if args.size() > 1 else 1
	vows = args[2] if args.size() > 2 else ""
	var hero := Profile.new()
	for r in runs:
		_run(hero, r + 1)
	get_tree().quit()


func _run(p: Profile, r: int) -> void:
	_before_run(p, r)
	var fame_before := p.fame
	var counts := {"missions": 0, "won": 0, "lost": 0}
	print(
		"run %d: level %d, fame %d, gold %d, flasks %d" % [r, p.level, p.fame, p.gold, p.run.flasks]
	)
	while counts.missions < MAX_MISSIONS:
		var next := _next_mission(p)
		if next.is_empty():
			print("  no way on from place %d" % p.place)
			p.run.end(p)
			break
		counts.missions += 1
		_gear_up(p)
		var result := _mission(p, int(next[0]), int(next[1]))
		counts["won" if result.won else "lost"] += 1
		if result.over:
			break
	runs_done = r
	var fame := p.fame - fame_before
	print("RUN %d %d %d %d %d %d" % [r, p.level, fame, counts.missions, counts.won, counts.lost])


## The start camp: the vows (from run VOWS_FROM), the stat points, the flasks and the perks.
func _before_run(p: Profile, r: int) -> void:
	if r == VOWS_FROM and vows != "":
		for i in Vows.MAX_HP_STEPS:
			p.run.vows.next_hp_step()
		p.run.vows.switch("short_time")
		if vows == "all":
			p.run.vows.switch("no_shop_potions")
			p.run.vows.switch("no_flasks")
	var i := 0
	while p.stat_points > 0:
		p.spend_point(POINTS[i % POINTS.size()])
		i += 1
	while p.run.flask_price() > 0 and p.fame >= p.run.flask_price():
		p.run.buy_flask(p)
		print("BUY flask%d %d %d" % [p.run.flasks, runs_done, p.level])
	for perk: String in PERKS:
		if p.run.buy_perk(p, perk):
			print("BUY %s %d %d" % [perk, runs_done, p.level])


## A camp: the better gear worn, the stat things used, HP potions bought with half the gold.
func _gear_up(p: Profile) -> void:
	for i in p.backpack.size():
		var id := int(p.backpack[i].id)
		if id == 0 or id >= 500 or Items.level_needed(id) > p.level or id in Items.NOT_WORN:
			continue
		var worn: Dictionary = p.equipped[Items.place(id)] if id < 300 else {}
		if Items.STAT_ITEMS.has(id) or int(worn.id) == 0 or _worth(p.backpack[i]) > _worth(worn):
			p.use_item(i)
	var budget := p.gold / 2
	for id: int in HP_POTIONS:
		var at := p.shop.find_custom(func(it: Dictionary) -> bool: return int(it.id) == id)
		while at >= 0 and budget >= int(Items.POTION_PRICES[id - 1]):
			var gold := p.gold
			if Blacksmith.buy(p, at) != "bought":
				break
			budget -= gold - p.gold


static func _worth(it: Dictionary) -> int:
	return int(it.attack) * 3 + int(it.defense) * 2 + int(it.hp) / 3 + int(it.mp) / 5


## The mission the camp offers, as the camp does (CampScreen.choices): [lord, mission], or [].
func _next_mission(p: Profile) -> Array:
	var to := p.heading
	if to > 0 and to in world.next_places(p.place) and p.is_lord_open(to):
		var n := campaign.lord_missions(to).size()
		var left: Array = range(n).filter(func(m: int) -> bool: return not p.is_done(to, m))
		if left.is_empty():
			left = range(n)
		return [to, int(left[rng.randi_range(0, left.size() - 1)])]
	var open: Array = world.next_places(p.place).filter(
		func(id: int) -> bool: return p.is_lord_open(id)
	)
	if open.is_empty():
		return []
	var lord := int(open[rng.randi_range(0, open.size() - 1)])
	for m in campaign.lord_missions(lord).size():
		if not p.is_done(lord, m):
			return [lord, m]
	return [lord, 0]


## Plays a mission and takes what it left, as MissionScreen does. Returns {won, over}.
func _mission(p: Profile, lord: int, mission: int) -> Dictionary:
	var info: Dictionary = campaign.lord_missions(lord)[mission]
	var fame := p.fame
	var sim := _play(p, lord, info, mission)
	var over := false
	if not sim.won:
		var story_ends := int(info.get("reward", 0)) > Profile.ENDING_BASE
		over = p.run.lose_mission(p, story_ends, sim.rng).over
	p.take_from(sim, lord, mission, int(info.get("id", 0)), rng)
	var ending := p.advance(sim, lord, info, rng)
	if not p.run.gift.is_empty():
		p.run.take_gift(p, rng.randi_range(0, p.run.gift.size() - 1), rng)
	if ending < 0 and sim.won:
		var ways: Array = world.next_places(lord).filter(
			func(id: int) -> bool: return p.is_lord_open(id)
		)
		p.heading = int(ways[rng.randi_range(0, ways.size() - 1)]) if not ways.is_empty() else 0
	print(
		(
			"  place %2d mission %d %s, level %d, fame +%d, %d ticks%s"
			% [
				lord,
				mission,
				"won" if sim.won else "lost",
				p.level,
				p.fame - fame,
				sim.ticks,
				" ending %d" % ending if ending >= 0 else ""
			]
		)
	)
	return {"won": sim.won, "over": over or (ending >= 0 and p.place == 0)}


func _play(p: Profile, lord: int, info: Dictionary, mission: int) -> MapSim:
	var s: Array = info.get("start", [4, 4])
	var map := MapBuilder.load_map(Campaign.lord_map(lord))
	var sim := MapSim.new(map, mission, Vector2i(int(s[0]), int(s[1])))
	sim.rng = JavaRandom.new(rng.randi())
	sim.boss_type = int(info.get("boss_type", 0))
	sim.mission_gold = int(info.get("gold", 0))
	sim.mission_general = int(info.get("general", 0))
	sim.time_limit = int(info.get("time_limit", 0))
	p.apply_to(sim)
	var pilot := Autopilot.new()
	pilot.toggle()
	for t in TICK_CAP:
		if not sim.talk.is_empty():
			sim.skip_talk()
		var d: Dictionary = pilot.decide(sim)
		sim.tick(int(d.held), -1, bool(d.fire) or sim.banner != 0, int(d.hotkey), -1, int(d.belt))
		if sim.finished or sim.failed:
			break
	return sim
