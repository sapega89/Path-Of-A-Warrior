extends "res://tests/test_case.gd"

const MapBuilder := preload("res://scripts/world/map_builder.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")
const JavaRandom := preload("res://scripts/sim/java_random.gd")
const Effects := preload("res://scripts/world/effects.gd")


## Mission 1 of lord 1 on map 1, the same random numbers every run.
func _sim(enemies: bool = true) -> RefCounted:
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	sim.rng = JavaRandom.new(1)
	sim.no_enemies = not enemies
	return sim


## An empty, open room with one swordsman standing below the hero.
func _duel() -> Array:
	var sim := _sim(false)
	for t in 200:
		if sim.exits_open():
			break
		sim.tick(-1, -1, sim.banner != 0)  # the key closes a banner (in the room it strikes)
	var e = sim.create_enemy(MapSim.KIND_SWORDS, 4, 7, 0)
	e.type = MapSim.KIND_SWORDS
	e.pos = sim.hero.pos + Vector2i(0, 30)
	e.alerted = 1
	e.think_ticks = 100  # does not choose an action during the test
	sim.hero.facing = 0
	sim.hero.dir = 0
	return [sim, e]


func test_random_numbers() -> void:
	var r := JavaRandom.new(42)
	eq(r.next_int(), -1170105035, "first number of seed 42")
	eq(r.next_int(), 234785527, "second number")
	for i in 100:
		var v := r.below(7)
		if v < 0 or v > 6:
			check(false, "below(7) out of range: %d" % v)
			break


func test_directions_and_distance() -> void:
	eq(MapSim.distance(Vector2i(0, 0), Vector2i(30, 40)), 50, "3-4-5")
	eq(MapSim.dir4(Vector2i(0, 0), Vector2i(0, 30)), 0, "down")
	eq(MapSim.dir4(Vector2i(0, 0), Vector2i(-30, 5)), 2, "left")
	eq(MapSim.dir8(Vector2i(0, 0), Vector2i(10, 30)), 0, "almost down")
	eq(MapSim.dir8(Vector2i(0, 0), Vector2i(30, 30)), 7, "down right")


func test_spawn_spots_on_the_open_exit() -> void:
	var sim := _sim()
	check(sim.spawn_spots.size() > 0, "room 1 has places to come in")
	for s in sim.spawn_spots:
		eq(s.z, 0, "room 1 opens down only")
		eq(s.y, 7, "the bottom row of the room")


func test_soldiers_come_in() -> void:
	var sim := _sim()
	var most := 0
	var first_y := -1
	for t in 80:
		sim.tick(-1, -1, true)
		if first_y == -1 and sim.enemies.size() > 0:
			first_y = sim.enemies[0].pos.y
		most = maxi(most, sim.enemies.size())
	check(first_y > MapSim.edge(1), "the first one starts outside, below the room: %d" % first_y)
	check(most > 0 and most <= sim.max_enemies(), "at most the room's maximum at once: %d" % most)
	for e in sim.enemies:
		check(e.type == MapSim.KIND_SWORDS or e.type == MapSim.KIND_SQUAD, "room 1 sends swords")
	check(not sim.exits_open(), "the room stays closed while they live")


func test_sword_hits() -> void:
	var d := _duel()
	var sim: RefCounted = d[0]
	var e = d[1]
	var hp: int = e.hp
	sim.tick(-1, -1, true)
	check(sim.hero.action >= 3 and sim.hero.action <= 8, "a sword action: %d" % sim.hero.action)
	sim.tick(-1, -1)
	check(e.hp < hp, "the strike took HP: %d -> %d" % [hp, e.hp])
	eq(e.action, 2, "the soldier reels")
	eq(sim.target_info.get("name", ""), "Swords", "the target's name is shown")



func test_hit_spark_shows_two_ticks() -> void:
	var d := _duel()
	var sim: RefCounted = d[0]
	var e = d[1]
	eq(sim.sparks().size(), 0, "no spark before the strike")
	sim.tick(-1, -1, true)
	sim.tick(-1, -1)
	var sp: Array = sim.sparks()
	eq(sp.size(), 1, "the strike shows a spark")
	var at := Vector2i.ZERO
	if sp.size() == 1:
		eq(int(sp[0][0]), 0, "its first picture")
		at = sp[0][1]
		check(MapSim.distance(at, e.pos) <= 8, "where the soldier was hit: %s, %s" % [at, e.pos])
	sim.tick(-1, -1)
	sp = sim.sparks()
	if sp.size() == 1:
		eq(int(sp[0][0]), 1, "then its second picture")
		eq(sp[0][1], at, "in the same place, as the soldier reels back")
	else:
		check(false, "the spark shows a second tick: %d" % sp.size())
	sim.tick(-1, -1)
	sim.tick(-1, -1)
	check(sim.sparks().filter(func(x): return x[1] == e.pos and int(x[0]) < 2).size() <= 1, "the spark ends")

func test_last_enemy_clears_the_room() -> void:
	var d := _duel()
	var sim: RefCounted = d[0]
	var e = d[1]
	sim.room_phase = 0
	e.hp = 1
	sim.tick(-1, -1, true)
	sim.tick(-1, -1)
	eq(e.hp, 0, "struck down")
	var cleared := false
	for t in 40:
		sim.tick(-1, -1)
		if sim.banner == MapSim.BANNER_STAGE_CLEAR:
			cleared = true
			break
	check(sim.enemies.is_empty(), "the body is gone")
	eq(sim.kills, 1, "one kill")
	check(cleared, "Stage Complete")


func test_hero_falls() -> void:
	var d := _duel()
	var sim: RefCounted = d[0]
	sim.hero.hp = 1
	sim.hero_is_hit(d[1])
	eq(sim.hero.hp, 0, "no HP left")
	eq(sim.hero.action, 10, "falls")
	for t in 30:
		sim.tick(-1, -1)
	eq(sim.banner, MapSim.BANNER_FAILED, "Mission fail!")
	check(not sim.finished, "waits for a key")
	sim.tick(-1, -1, true)
	check(sim.finished, "a key ends the mission")


func test_barrel_breaks() -> void:
	var sim := _sim(false)
	for t in 200:
		if sim.exits_open():
			break
		sim.tick(-1, -1, sim.banner != 0)
	var barrel = null
	for b in sim.breakables:
		if b.tile == Vector2i(4, 6):
			barrel = b
	check(barrel != null, "the barrel at (4, 6) is in the room")
	if barrel == null:
		return
	eq(barrel.hp, 41, "a barrel takes 41")
	sim.hero.pos = Vector2i(120, 150)
	sim.hero.facing = 0
	sim.hero.dir = 0
	for t in 120:
		sim.tick(-1, -1, t % 4 == 0)
		if barrel.hp < 1:
			break
	check(barrel.hp < 1, "broken by the sword: %d" % barrel.hp)
	eq(int(sim.objects[6 * sim.w + 4]), 0, "the cell is free")
	for t in 13:
		sim.tick(-1, -1)
	check(not barrel.active, "gone after blinking")


func test_gold_is_picked_up() -> void:
	var sim := _sim(false)
	var d = MapSim.Drop.new()
	d.item = 10020
	d.pos = sim.hero.pos
	sim.drops.append(d)
	sim.tick(-1, -1)
	sim.tick(-1, -1)
	eq(sim.gold, 20, "20 gold")
	check(sim.drops.is_empty(), "nothing left on the floor")


## A general met in an open room, with the hero next to him.
func _general_duel() -> Array:
	var d := _duel()
	var sim: RefCounted = d[0]
	sim.enemies.clear()
	sim.enemies_alive = 0
	sim.boss_type = 1
	sim.waves[0] = 1
	sim.waves[1] = 1
	var g = sim.create_enemy(1, 4, 7, 0)
	g.pos = sim.hero.pos + Vector2i(0, 30)
	g.alerted = 1
	g.think_ticks = 100
	return [sim, g]


func test_general_comes_with_his_talk() -> void:
	var d := _general_duel()
	var sim: RefCounted = d[0]
	var g = d[1]
	eq(sim.general.get("name", ""), "Wallace", "general 1")
	check(sim.boss_fight, "the mission's own general")
	eq(g.level, 2, "the hero's level and the list's count")
	eq(g.hp, 23, "20 HP and 3 a level")
	eq(sim.talk.size(), 3, "three lines")
	eq(sim.talk[0], "[Wallace] Wallace is here!!!", "his name for &")
	sim.tick(-1, -1)
	eq(sim.talk_text(), "[", "typed a letter a tick")
	var x: int = sim.hero.pos.x
	for t in 10:
		sim.tick(-1, -1, true)
		if sim.talk.is_empty():
			break
	check(sim.talk.is_empty(), "the key goes through the talk")
	eq(sim.hero.pos.x, x, "the world waited")


func test_mission_won_when_his_general_falls() -> void:
	var d := _general_duel()
	var sim: RefCounted = d[0]
	var g = d[1]
	sim.talk.clear()
	sim.room_phase = 0
	sim.waves[0] = 0
	sim.waves[1] = 0
	g.hp = 1
	sim.tick(-1, -1, true)
	sim.tick(-1, -1)
	eq(g.hp, 0, "struck down")
	for t in 80:
		sim.tick(-1, -1)
		if sim.banner == MapSim.BANNER_SUCCESS:
			break
	eq(sim.banner, MapSim.BANNER_SUCCESS, "Mission Success!")
	check(sim.won, "won")
	sim.tick(-1, -1, true)
	eq(sim.banner, MapSim.BANNER_TOTAL_EXP, "then the exp")
	sim.tick(-1, -1, true)
	check(sim.finished, "no time limit, no general to talk: the mission is over")


func test_rewards_and_the_talk_after_the_mission() -> void:
	var sim := _sim(false)
	sim.mission_gold = 3
	sim.mission_exp = 40
	sim.time_limit = 192
	sim.mission_general = 5
	sim.banner = MapSim.BANNER_SUCCESS
	eq(sim.gold_reward(), 450, "gold: 3 x 150 on normal")
	sim.tick(-1, -1, true)
	eq(sim.banner, MapSim.BANNER_TOTAL_EXP, "the exp")
	eq(sim.exp_reward(), 80, "exp: twice on normal")
	sim.tick(-1, -1, true)
	eq(sim.banner, MapSim.BANNER_TIME_EXP, "in time: the exp for time")
	eq(sim.mission_exp, 42, "a twentieth more")
	sim.tick(-1, -1, true)
	eq(sim.banner, 0, "the pages are over")
	eq(sim.talk.size(), 5, "the general talks")
	check(sim.talk[0].begins_with("[Reeve] Not bad, warrior."), "his first words: %s" % sim.talk[0])
	check(sim.talk[1].begins_with("[Hero]"), "then the hero")
	eq(sim.friendship.get(5, 0), 5, "friendship grows")
	for t in 400:
		if sim.finished:
			break
		sim.tick(-1, -1, true)
	check(sim.finished, "after the talk the mission is over")


func test_room_general_talks_when_his_room_is_cleared() -> void:
	var sim := _sim(false)
	for t in 200:
		if sim.exits_open():
			break
		sim.tick(-1, -1, sim.banner != 0)
	sim.rooms.cells = sim.rooms.cells.duplicate(true)  # (the map's data stays as it is)
	sim.rooms.cells[sim.cell]["general"] = 5
	sim.room_phase = 0
	sim.banner = MapSim.BANNER_STAGE_CLEAR
	sim.banner_timer = 1
	sim.tick(-1, -1)
	eq(sim.talk.size(), 5, "he talks")
	check(not sim.exits_open(), "the exits wait for the talk")
	for t in 400:
		if sim.exits_open():
			break
		sim.tick(-1, -1, true)
	check(sim.exits_open(), "then they open")


func test_general_skills_are_actions() -> void:
	var d := _general_duel()
	var sim: RefCounted = d[0]
	var g = d[1]
	sim.set_general(4)  # Kirkland: skills 2, 3, 4, 6 (a heal only when hurt: else a strike)
	for t in 20:
		sim.general_pick_skill(g, false)
		check(g.action == 1 or (g.action >= 5 and g.action <= 21), "a skill action: %d" % g.action)
		check(sim.enemy_anim(g, g.action).size() > 1, "with frames")


func test_skill_costs_mp_and_hits() -> void:
	var d := _duel()
	var sim: RefCounted = d[0]
	var e = d[1]
	var hp: int = e.hp
	sim.tick(-1, -1, false, 0)  # the first skill key: skill 12
	eq(sim.hero.action, 12, "the skill starts")
	eq(sim.hero.mp, 5, "it took 5 MP")
	# The dash goes 24 px a frame through anyone: he stands 40 px ahead, where the first
	# dashing frame ends in front of him (an idle soldier walks on; here he waits).
	var spot: Vector2i = sim.hero.pos + Vector2i(0, 40)
	for t in 6:
		e.pos = spot
		sim.tick(-1, -1)
	check(e.hp < hp, "the skill took HP: %d -> %d" % [hp, e.hp])
	sim.hero.mp = 4
	sim.hero.action = 0
	sim.tick(-1, -1, false, 0)
	check(sim.hero.action != 12, "no skill without MP")
	eq(sim.hero.mp, 4, "nothing is taken")


func test_attack_buff_skill() -> void:
	var sim: RefCounted = _duel()[0]
	sim.tick(-1, -1, false, 1)  # the second skill key: skill 17
	eq(sim.hero.action, 17, "the buff starts")
	eq(sim.hero.mp, 3, "it took 7 MP")
	for t in 14:
		sim.tick(-1, -1)
	check(sim.hero.attack_buff > 0, "attack is raised")
	check(sim.hero.attack_buff_ticks > 0, "for a while")


func test_potion_restores_hp() -> void:
	var sim: RefCounted = _duel()[0]
	check(sim.add_quick_item(1), "a small HP potion goes to a quick slot")
	sim.hero.hp = 10
	sim.tick(-1, -1, false, -1, 0)
	for t in 3:
		sim.tick(-1, -1)
	eq(sim.hero.hp, 19, "30 % of 30 HP")
	eq(int(sim.quick_slots[0][0]), 0, "the slot is empty again")
	eq(sim.effect_item, 0, "nothing in use")


func test_scroll_blast_hits() -> void:
	var d := _duel()
	var sim: RefCounted = d[0]
	var e = d[1]
	var hp: int = e.hp
	check(sim.add_quick_item(10), "a fire scroll goes to a quick slot")
	sim.tick(-1, -1, false, -1, 0)
	eq(sim.hero.action, 11, "the hero holds the scroll up")
	var spot: Vector2i = e.pos
	for t in 10:
		e.pos = spot  # (an idle soldier walks on; here he waits for the blast)
		sim.tick(-1, -1)
	check(e.hp < hp, "the blast took HP: %d -> %d" % [hp, e.hp])
	eq(sim.effect_item, 0, "the scroll is used up")


func test_effects_of_skills_and_potions() -> void:
	var d := _duel()
	var sim: RefCounted = d[0]
	eq(sim.effects().size(), 0, "nothing while standing")
	sim.tick(-1, -1, false, 0)  # skill 12: the dash
	for t in 3:
		sim.tick(-1, -1)
	var fx: Array = sim.effects()
	eq(fx.size(), 1, "the dash shows its effect")
	eq(fx[0][0], "slash", "from the slash sheet")
	var sim2: RefCounted = _duel()[0]
	sim2.add_quick_item(4)
	sim2.tick(-1, -1, false, -1, 0)
	fx = sim2.effects()
	eq(fx.size(), 1, "a potion in use shows")
	eq(fx[0][1], 4, "its first frame")
	var node := Effects.new()
	node._ready()
	node.show_effects(fx + [["storm", 99, Vector2i.ZERO], ["nothing", 0, Vector2i.ZERO]])
	eq(node.shown(), 1, "only frames the sheets have are drawn")
	node.free()
