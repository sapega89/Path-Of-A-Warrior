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


## Ticks with no key until the page changes or the mission is over; the ticks it took
## (-1: not within n).
func _next_page(sim: RefCounted, n: int = 400) -> int:
	var b: int = sim.banner
	for t in n:
		sim.tick(-1, -1)
		if sim.banner != b or sim.finished:
			return t + 1
	return -1


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


func test_archers_stand_on_their_cells() -> void:
	# Map 1 puts an archer on cell (3, 1) of its first room in its fourth mission.
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 3, Vector2i(4, 2))
	var archers: Array = sim.enemies.filter(func(e): return e.type == MapSim.KIND_ARCHERS)
	eq(archers.size(), 1, "the archer of the room's script")
	if archers.size() == 1:
		eq(archers[0].pos, Vector2i(3 * 27 + 12, 1 * 27 + 20), "on his cell")
		eq(archers[0].alerted, 1, "on guard at once")
	eq(sim.enemies_alive, 0, "archers do not count for clearing the room")
	sim = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	eq(sim.enemies.size(), 0, "another mission: nobody there")
	sim = MapSim.new(MapBuilder.load_map(1), 3, Vector2i(4, 2))
	sim.no_enemies = true
	sim.enemies.clear()
	sim.enter_room()
	eq(sim.enemies.size(), 0, "the map without enemies: no archers either")


func test_arrows_wait_while_a_big_skill_holds_the_room() -> void:
	var sim := _sim(false)
	var a = sim.arrows[0]
	# [the hero's action and frame of the last tick, the arrow flies on]
	for c in [[0, 0, true], [12, 5, true], [26, 1, true], [26, 2, false], [27, 8, false],
			[26, 9, true], [28, 3, true], [28, 4, false], [28, 30, false], [29, 6, true],
			[29, 7, false], [30, 3, true], [30, 4, false], [30, 14, false], [30, 15, true]]:
		a.active = true
		a.pos = sim.hero.pos + Vector2i(0, 120)
		a.dir = 2  # up, toward the hero
		a.ticks = 0
		sim.hero.last_action = c[0]
		sim.hero.last_frame = c[1]
		sim._tick_arrows()
		eq(a.pos.y, sim.hero.pos.y + (108 if c[2] else 120), "skill %d, frame %d" % [c[0], c[1]])
		eq(a.ticks, 1 if c[2] else 0, "its time goes on only while it flies")
	sim.hero.action = 28
	sim.hero.frame = 6
	sim._end_tick()
	eq([sim.hero.last_action, sim.hero.last_frame], [28, 6], "the end of a tick keeps them")


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



## The sword hits ahead within a band one cell wide to each side, not only in the quarter faced.
func test_strike_band() -> void:
	var o := Vector2i(100, 100)
	check(MapSim.in_strike_reach(o, o + Vector2i(15, -20), 6, 63), "right: a little above, close up")
	check(MapSim.in_strike_reach(o, o + Vector2i(15, 25), 6, 63), "right: a little below")
	check(MapSim.in_strike_reach(o, o + Vector2i(-25, -10), 4, 63), "up: a little to the left")
	check(MapSim.in_strike_reach(o, o + Vector2i(45, 35), 6, 63), "right: the quarter as before")
	check(not MapSim.in_strike_reach(o, o + Vector2i(10, -30), 6, 63), "right: more than a cell above")
	check(not MapSim.in_strike_reach(o, o + Vector2i(-10, 5), 6, 63), "right: behind him")
	check(not MapSim.in_strike_reach(o, o + Vector2i(60, 25), 6, 63), "right: out of reach")
	# on hard (no turning to the enemy) a soldier a little above, in front of him, is hit
	var d := _duel()
	var sim: RefCounted = d[0]
	var e = d[1]
	sim.difficulty = 0
	e.pos = sim.hero.pos + Vector2i(15, -20)  # in the quarter above him
	sim.hero.facing = 6
	sim.hero.dir = 6
	var hp: int = e.hp
	sim.tick(-1, -1, true)
	sim.tick(-1, -1)
	eq(sim.hero.facing, 6, "he did not turn")
	check(e.hp < hp, "the strike took HP: %d -> %d" % [hp, e.hp])


## The hero turns to the enemy beside him as he strikes on normal; on hard he aims by hand.
func test_auto_aim_only_on_normal() -> void:
	for hard in [false, true]:
		var d := _duel()
		var sim: RefCounted = d[0]
		var e = d[1]
		sim.difficulty = 0 if hard else 1
		e.pos = sim.hero.pos + Vector2i(30, 0)
		sim.tick(-1, -1, true)
		sim.tick(-1, -1)
		eq(sim.hero.facing, 0 if hard else 6, "turned to the enemy only on normal (hard: %s)" % hard)


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


func test_weapon_trail_of_a_swing() -> void:
	var sim := _sim(false)
	var pick := RandomNumberGenerator.new()
	eq(sim.trails(pick).size(), 0, "no trail standing")
	sim.hero.dir = 4
	sim.hero.action = 12
	sim.hero.frame = 3
	var t: Array = sim.trails(pick)
	eq(t.size(), 1, "a skill swing leaves a trail")
	if t.size() == 1:
		eq(str(t[0][0]), "trail", "the trail sheet")
		eq(int(t[0][1]), 2 * 3 + 1, "facing down, the middle step")
		eq(t[0][2], sim.hero.pos, "at the hero")
	sim.hero.action = 25
	sim.hero.frame = 3
	t = sim.trails(pick)
	if t.size() == 1:
		eq(int(t[0][1]), 3 * 3 + 2, "a whirl turns its trail (down + 2 = left)")
	else:
		check(false, "the whirl leaves a trail: %d" % t.size())
	var seen := false
	sim.hero.action = 0
	sim.hero.frame = 0
	sim.tick(-1, -1, true)
	for i in 8:
		if sim.trails(pick).size() > 0:
			seen = true
		sim.tick(-1, -1)
	check(seen, "a sword strike leaves a trail")


func test_strikes_and_hits_have_their_sounds() -> void:
	var d := _duel()
	var sim: RefCounted = d[0]
	var heard: Array[int] = []
	sim.tick(-1, -1, true)
	heard.append_array(sim.sounds)
	for i in 3:
		sim.tick(-1, -1)
		heard.append_array(sim.sounds)
	check(15 in heard, "the swing: %s" % [heard])
	check(16 in heard, "the strike lands: %s" % [heard])
	sim.hero.hurt_ticks = 0
	sim.hero_is_hit(d[1])
	eq(sim.sounds.back(), 16, "the hero is hit")

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
	var heard := false
	for t in 30:
		sim.tick(-1, -1)
		heard = heard or (sim.banner == MapSim.BANNER_FAILED and 6 in sim.sounds)
		if sim.banner == MapSim.BANNER_FAILED:
			break
	eq(sim.banner, MapSim.BANNER_FAILED, "Mission fail!")
	check(heard, "with its sound (6)")
	eq(_next_page(sim), MapSim.BANNER_TICKS, "20 ticks, then the mission is over")
	check(sim.finished, "over")
	sim = _duel()[0]
	sim.hero.hp = 0
	sim.failed = true
	sim._show_banner(MapSim.BANNER_FAILED)
	sim.tick(-1, -1, true)
	check(not sim.finished, "a key: two more ticks")
	sim.tick(-1, -1)
	check(sim.finished, "then it is over")


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


## As pyport's popup 13: a gear picked up shows "<its name> Acquired!!" for 20 ticks while the
## map waits (a key: 2); with no place left in the Inventory it stays on the floor.
func test_a_gear_picked_up_is_acquired() -> void:
	var sim := _sim(false)
	for t in 60:
		if sim.banner == 0 and sim.room_phase == 0:
			break
		sim.tick(-1, -1)
	sim.free_places = 1
	for k in 2:
		var d = MapSim.Drop.new()
		d.item = 131 + k
		d.pos = sim.hero.pos
		sim.drops.append(d)
	sim.tick(-1, -1)
	eq([sim.items.size(), sim.banner, sim.acquired], [1, MapSim.BANNER_ACQUIRED, 131], "Acquired!!")
	eq(sim.free_places, 0, "the last place taken")
	eq(sim.drops.size(), 1, "the other stays on the floor")
	var ticks: int = sim.play_ticks
	for t in 19:
		sim.tick(-1, -1)
	eq([sim.banner, sim.play_ticks], [MapSim.BANNER_ACQUIRED, ticks], "the map waits")
	sim.tick(-1, -1)
	eq(sim.banner, 0, "gone after 20 ticks")
	sim.tick(-1, -1)
	eq(sim.items.size(), 1, "still no place")
	sim.free_places = 1
	sim.tick(-1, -1)
	eq([sim.items.size(), sim.acquired], [2, 132], "a place: picked up")
	sim.tick(-1, -1, true)
	sim.tick(-1, -1)
	eq(sim.banner, 0, "a key closes it sooner")


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
	eq(sim.general.get("name", ""), "Zdzislaw Krzeminski", "general 1")
	check(sim.boss_fight, "the mission's own general")
	eq(g.level, 2, "the hero's level and the list's count")
	eq(g.hp, 23, "20 HP and 3 a level")
	eq(sim.talk.size(), 3, "three lines")
	eq(sim.talk[0], "[Zdzislaw Krzeminski] Zdzislaw Krzeminski is here!", "his name for &")
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
	for t in 5:
		sim.tick(-1, -1, true)
	eq(sim.banner, MapSim.BANNER_SUCCESS, "a key does not end it")
	eq(_next_page(sim), MapSim.BANNER_TICKS - 5, "it shows 20 ticks")
	eq(sim.banner, MapSim.BANNER_TOTAL_EXP, "then the exp")
	var ticks := _next_page(sim)
	check(sim.finished, "no time limit, no general to talk: the mission is over")
	check(ticks > MapSim.EXP_PAGE_TICKS, "after the bar and 16 ticks (%d)" % ticks)


func test_rewards_and_the_talk_after_the_mission() -> void:
	var sim := _sim(false)
	sim.mission_gold = 3
	sim.mission_exp = 40
	sim.time_limit = 192
	sim.mission_general = 5
	sim._show_banner(MapSim.BANNER_SUCCESS)
	eq(sim.gold_reward(), 450, "gold: 3 x 150 on normal")
	_next_page(sim)
	eq(sim.banner, MapSim.BANNER_TOTAL_EXP, "the exp")
	eq(sim.exp_reward(), 80, "exp: twice on normal")
	sim.hero_exp = 0
	# 80 exp from 0: the bar's 100 px in 26 ticks, the level up, "Level Up" 20 ticks, the
	# 28 px of the 30 / 104 left in 8, then the page stays 16
	eq(_next_page(sim), 26 + 1 + 20 + 8 + MapSim.EXP_PAGE_TICKS, "the exp page goes on by itself")
	eq(sim.banner, MapSim.BANNER_TIME_EXP, "in time: the exp for time")
	eq(sim.mission_exp, 42, "a twentieth more")
	_next_page(sim)
	eq(sim.banner, 0, "the pages are over")
	eq(sim.talk.size(), 5, "the general talks")
	check(sim.talk[0].begins_with("[Andrii Nedolia] You handle yourself well, warrior."), "his first words: %s" % sim.talk[0])
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
	sim.set_general(4)  # Jan Gorski: skills 2, 3, 4, 6 (a heal only when hurt: else a strike)
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


func test_a_buff_shows_its_aura() -> void:
	var sim: RefCounted = _duel()[0]
	sim.enemies.clear()
	sim.tick(-1, -1)
	eq(sim.auras().size(), 0, "no aura without a buff")
	sim.hero.attack_buff = 3
	sim.hero.attack_buff_ticks = 2
	sim.tick(-1, -1)
	eq(sim.auras().size(), 0, "the buff shows from the next tick")
	var seen: Array = []
	for t in 3:
		sim.tick(-1, -1)
		var a: Array = sim.auras()
		if a.size() == 2:
			eq([a[0][0], a[0][2], a[0][3], a[1][2]], ["aura", sim.hero.pos + Vector2i(0, 3), true,
				sim.hero.pos + Vector2i(0, 3)], "a ring behind him and the light in front, at his feet")
			eq(int(a[1][1]), int(a[0][1]) + 3, "the same step of both")
		seen.append(a.size())
	eq(seen, [2, 2, 0], "while it lasts, and the tick it ends")
	var d = MapSim.Drop.new()
	d.item = 10020
	d.pos = sim.hero.pos
	sim.drops.append(d)
	sim.tick(-1, -1)
	eq(sim.auras().size(), 2, "he glows as he picks something up")
	sim.tick(-1, -1)
	eq(sim.auras().size(), 0, "for that tick")
	var sim2: RefCounted = _general_duel()[0]
	var g = sim2.enemies[0]
	g.defense_buff_ticks = 5
	eq(sim2.auras().size(), 2, "a general's buff too")
	eq(sim2.auras()[0][2], g.pos + Vector2i(0, 3), "on him")
	var node := Effects.new()
	node._ready()
	node.show_effects(sim2.auras())
	eq(node.shown(), 2, "both pictures are drawn")
	check(not node.get_child(0).no_depth_test and node.get_child(1).no_depth_test,
		"the ring stands behind him, the light over him")
	node.free()


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


## A belt key uses its own slot, whatever slots the * and # keys drink from.
func test_belt_slot_by_its_key() -> void:
	var sim: RefCounted = _duel()[0]
	sim.quick_slots[3] = [1, 2]
	sim.hero.hp = 10
	sim.tick(-1, -1, false, -1, -1, 3)
	for t in 3:
		sim.tick(-1, -1)
	eq(sim.hero.hp, 19, "the potion of the fourth slot (V)")
	eq(int(sim.quick_slots[3][1]), 1, "one left there")
	eq(sim.skill_mp_need(12, 1), 5, "a skill's MP at level 1")


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


func test_effects_of_a_generals_skills() -> void:
	var d := _general_duel()
	var sim: RefCounted = d[0]
	var g = d[1]
	g.dir = 2
	# action, frame -> the picture shown on him (or in front of him, the blast)
	var cases := [
		[6, 3, ["slash", 3, g.pos]], [8, 2, ["slash", 2, g.pos]], [10, 5, ["heal", 1, g.pos]],
		[12, 4, ["buff", 0, g.pos]], [15, 6, ["whirl", 1, g.pos]], [16, 3, ["slash", 1, g.pos]],
		[17, 5, ["slash", 0, g.pos]], [18, 6, ["burst", 1, g.pos]],
		[18, 5, ["burst", 0, g.pos + MapSim.BURST_FIRST_SHIFT]],
		[20, 3, ["wave", 8, g.pos]], [21, 9, ["blast", 1, sim._front_of(g.pos, 2)]]]
	for c in cases:
		g.action = c[0]
		g.frame = c[1]
		eq(sim.effects(), [c[2]], "general action %d frame %d" % [c[0], c[1]])
	for c in [[6, 2], [7, 8], [14, 3], [19, 3], [1, 0]]:
		g.action = c[0]
		g.frame = c[1]
		eq(sim.effects().size(), 0, "nothing at action %d frame %d" % [c[0], c[1]])
	var e = sim.create_enemy(MapSim.KIND_SWORDS, 4, 7, 0)
	e.action = 6
	e.frame = 3
	g.action = 0
	eq(sim.effects().size(), 0, "a soldier's actions are not skills")


func test_fire_skills_set_on_fire() -> void:
	for skill in [23, 24, 29]:
		var d := _duel()
		var sim: RefCounted = d[0]
		var e = d[1]
		sim.hero.action = skill
		sim._strike_enemy(e)
		check(sim.sounds.has(13), "%d: the fire's sound" % skill)
		eq(sim.fires().size(), 0, "%d: it shows from the end of the tick" % skill)
		sim.hero.action = 0
		var shown: Array = []
		for t in 7:
			sim.tick(-1, -1)
			for f in sim.fires():
				shown.append(int(f[1]))
				eq(f[0], "fire", "from the fire sheet")
				eq(f[2], e.pos, "on the soldier")
		eq(shown, [0, 1, 2, 3, 4, 5], "%d: six pictures, then it is out" % skill)
	var d := _duel()
	var sim: RefCounted = d[0]
	sim.hero.action = 22
	sim._strike_enemy(d[1])
	sim.tick(-1, -1)
	eq(sim.fires().size(), 0, "other skills do not burn")


func test_a_general_sets_the_hero_on_fire() -> void:
	for skill in [17, 18, 19]:
		var d := _general_duel()
		var sim: RefCounted = d[0]
		var g = d[1]
		g.action = skill
		sim._general_skill_hits_hero(g)
		check(sim.sounds.has(13), "%d: the fire's sound" % skill)
		sim._end_tick()
		var f: Array = sim.fires()
		eq(f.size(), 1, "%d: the hero burns" % skill)
		if f.size() == 1:
			eq([f[0][1], f[0][2]], [0, sim.hero.pos], "its first picture on him")
		eq(sim.hero.hurt_ticks, 2 if skill == 19 else (5 if skill == 18 else 0), "%d: he reels" % skill)
	var d := _general_duel()
	var sim: RefCounted = d[0]
	d[1].action = 16
	sim._general_skill_hits_hero(d[1])
	sim._end_tick()
	eq(sim.fires().size(), 0, "other skills do not burn")


func test_skip_ends_a_talk_and_what_follows_comes() -> void:
	var d := _general_duel()
	var sim: RefCounted = d[0]
	eq(sim.talk.size(), 3, "the general who comes talks")
	sim.skip_talk()
	check(sim.talk.is_empty(), "SKIP: the talk is over")
	var x: int = sim.hero.pos.x
	sim.tick(1, 1)
	check(sim.hero.pos.x != x, "and the hero plays at once")
	sim.skip_talk()
	check(sim.talk.is_empty(), "with no talk it does nothing")

	sim = _sim(false)
	sim.mission_general = 5
	sim.banner = MapSim.BANNER_TIME_EXP
	_next_page(sim)
	eq(sim.talk.size(), 5, "the general's words after the mission")
	sim.skip_talk()
	check(sim.finished, "skipped: the mission is over")

	sim = _sim(false)
	for t in 200:
		if sim.exits_open():
			break
		sim.tick(-1, -1, sim.banner != 0)
	sim.rooms.cells = sim.rooms.cells.duplicate(true)
	sim.rooms.cells[sim.cell]["general"] = 5
	sim.room_phase = 0
	sim.banner = MapSim.BANNER_STAGE_CLEAR
	sim.banner_timer = 1
	sim.tick(-1, -1)
	eq(sim.talk.size(), 5, "the general of the room talks")
	sim.skip_talk()
	for t in 20:
		sim.tick(-1, -1)
	check(sim.exits_open(), "skipped: the exits open")
