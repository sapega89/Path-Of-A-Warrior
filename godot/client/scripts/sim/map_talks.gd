class_name MapTalks
extends RefCounted
## The talks over the map and the pages after a room or the mission: the generals' talk, the
## friendship it brings, the exp pages and the rewards.
## Static functions over the state of a MapSim (MapSim.tick() runs them).

const EXP_PAGE_WAITS := 200  # the timer of an exp page while its bar grows
const TALK_STEPS := 3  # a general met on the map: he, the hero, he
const VICTORY_TALK_STEPS := 5  # a general after his room or mission: he, the hero, ...
const FRIENDSHIP_PER_TALK := 5
const FRIENDSHIP_PER_FIGHT := 5  # a general met as a foe on the map loses this much


## A general met on the map: "<name> is here!!!", the hero's "...", his "Come on!". The fight
## costs friendship with him (not below 0), and his talk after it brings none.
static func start_map_talk(sim: MapSim, id: int) -> void:
	sim.friendship[id] = maxi(int(sim.friendship.get(id, 0)) - FRIENDSHIP_PER_FIGHT, 0)
	sim.fought[id] = true

	var lines := MapSim.talk_lines("map")
	sim.talk.clear()
	var name := String(TranslationServer.translate(str(sim.general.get("name", ""))))
	for k in TALK_STEPS:
		var speaker := name if (k & 1) == 0 else sim.hero_name
		var text := I18n.text(lines[21 + k]) if 21 + k < lines.size() else ""
		sim.talk.append("[%s] %s" % [speaker, text.replace("&", speaker)])
	sim.talk_line = 0
	sim.talk_chars = 0
	sim.talk_wait = 0


## Who says the line shown now: true for the hero (the odd lines), false for the general.
static func hero_talks(sim: MapSim) -> bool:
	return (sim.talk_line & 1) == 1


## The line shown now, as far as it is typed.
static func talk_text(sim: MapSim) -> String:
	if sim.talk.is_empty():
		return ""
	return sim.talk[sim.talk_line].substr(0, sim.talk_chars)


## SKIP: the talk is over at once, and what follows it comes (the fight, the exits, the end
## of the mission).
static func skip_talk(sim: MapSim) -> void:
	if sim.talk.is_empty():
		return
	sim.talk.clear()
	sim.talk_line = 0
	sim.talk_chars = 0
	sim.talk_wait = 0
	_talk_done(sim)


## A letter a tick; the key shows the whole line, or goes on once it is shown. A shown
## line waits 15 ticks.
static func tick_talk(sim: MapSim, fire: bool) -> void:
	var line := sim.talk[sim.talk_line]
	if sim.talk_wait > 0:
		sim.talk_wait -= 1
		if fire:
			sim.talk_wait = 0
		if sim.talk_wait < 1:
			sim.talk_line += 1
			sim.talk_chars = 0
			if sim.talk_line >= sim.talk.size():
				sim.talk.clear()
				sim.talk_line = 0
				_talk_done(sim)
		return
	if fire:
		sim.talk_chars = line.length()
		sim.talk_wait = 3
		return
	sim.talk_chars += 1
	if sim.talk_chars >= line.length():
		sim.talk_wait = 15


## The general of the room (0 none), who talks once it is cleared.
static func room_general(sim: MapSim) -> int:
	return (
		int(sim.rooms.cells[sim.cell].get("general", 0)) if sim.cell < sim.rooms.cells.size() else 0
	)


## "Mission Success!" (with the gold) -> the exp -> the exp for time if in time -> the
## general's talk -> the mission is over.
static func next_result_page(sim: MapSim) -> void:
	match sim.banner:
		MapSim.BANNER_SUCCESS:
			sim.banner = MapSim.BANNER_TOTAL_EXP
			sim.banner_timer = EXP_PAGE_WAITS
			sim.exp_bars.begin(sim.hero.level, sim.hero_exp, exp_reward(sim))
		MapSim.BANNER_TOTAL_EXP:
			if sim.play_seconds() < sim.time_limit:
				sim.time_exp = (
					((sim.time_limit - sim.play_seconds()) / sim.time_limit / 10 + 1)
					* sim.mission_exp
					/ 20
				)
				sim.mission_exp += sim.time_exp
				sim.banner = MapSim.BANNER_TIME_EXP
				sim.banner_timer = EXP_PAGE_WAITS
				sim.exp_bars.begin_time(exp_reward(sim))
			else:
				_mission_over(sim)
		_:
			_mission_over(sim)


## An exp page: its bar grows; all shown, the page stays 16 ticks more and the next one
## comes. A key cuts a "Level Up" short.
static func tick_exp_page(sim: MapSim, fire: bool) -> void:
	if fire and sim.exp_bars.level_up_ticks > 2:
		sim.exp_bars.level_up_ticks = 2
	var all_shown := sim.exp_bars.done()
	sim.exp_bars.tick()
	if not all_shown:
		return
	if sim.banner_timer > MapSim.EXP_PAGE_TICKS:
		sim.banner_timer = MapSim.EXP_PAGE_TICKS
	sim.banner_timer -= 1
	if sim.banner_timer <= 0:
		next_result_page(sim)


static func _mission_over(sim: MapSim) -> void:
	sim.banner = 0
	if sim.mission_general > 0 and sim.mission_general < 200:
		start_general_talk(sim, sim.mission_general, 2)
	else:
		sim.finished = true


## The gold of the mission (twice on hard difficulty, 0).
static func gold_reward(sim: MapSim) -> int:
	return sim.mission_gold * 150 * (1 + (sim.difficulty ^ 1))


## The exp the mission gives (twice its kills' worth, four times on hard difficulty).
static func exp_reward(sim: MapSim) -> int:
	return sim.mission_exp << (1 + (sim.difficulty ^ 1))


## A general's words after his room or the mission; the more friendship, the warmer
## (five lines for every ten points). The talk adds friendship, unless the hero fought him in
## this mission. after: what follows (talk_after).
static func start_general_talk(sim: MapSim, id: int, after: int) -> void:
	MapEnemyPlay.set_general(sim, id)
	var gain := 0 if sim.fought.has(id) else FRIENDSHIP_PER_TALK
	var points := mini(int(sim.friendship.get(id, 0)) + gain, 100)
	sim.friendship[id] = points
	var first := mini(points, 95) / 10 * VICTORY_TALK_STEPS
	var lines := MapSim.talk_lines("general")
	var name := String(TranslationServer.translate(str(sim.general.get("name", ""))))
	sim.talk.clear()
	for k in VICTORY_TALK_STEPS:
		var speaker := name if (k & 1) == 0 else sim.hero_name
		var text := I18n.text(lines[first + k]) if first + k < lines.size() else ""
		sim.talk.append("[%s] %s" % [speaker, text.replace("&", speaker)])
	sim.talk_line = 0
	sim.talk_chars = 0
	sim.talk_wait = 0
	sim.talk_after = after


static func _talk_done(sim: MapSim) -> void:
	var after := sim.talk_after
	sim.talk_after = 0
	if after == 1:
		sim.room_phase = 1
		sim.room_phase_timer = 5
	elif after == 2:
		sim.finished = true
