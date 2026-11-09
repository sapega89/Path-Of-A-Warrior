extends "res://tests/test_case.gd"
## A battle on this device (scripts/net/online_battle.gd) played to its end against the
## server's online game (server/online.gd) in this process.

const ClientTests := preload("res://tests/test_online_client.gd")
const OnlineTests := preload("res://tests/test_online_server.gd")
const ServerTests := preload("res://tests/test_server.gd")


func _dir() -> String:
	var d := "user://test_server_online_battle_%d" % randi()
	DirAccess.make_dir_recursive_absolute(d)
	return d


## Plays as a player would: Attack, the bar stopped near the mark, the first foe; OK at the
## end. Returns the states the battle went through, in order, each once.
func _play(c: RefCounted, limit := 30000) -> Array:
	var seen: Array = []
	var bar_at := 0
	for i in limit:
		var b: RefCounted = c.battle
		if b == null:
			break
		b.tick()
		if seen.is_empty() or seen[-1] != b.state:
			seen.append(b.state)
		match b.state:
			OnlineBattle.CHOOSE:
				if not b.exit_prompt and b.state_ticks == 3:
					b.key("right")
			OnlineBattle.TARGET:
				b.key("fire")
			OnlineBattle.BAR:
				bar_at += 1
				if b.state_ticks == 6:
					b.key("fire")
			OnlineBattle.RESULT:
				if b.result_shown():
					b.key("fire")
					if b.left:
						break
	return seen


func test_a_duel_played_to_the_result() -> void:
	var d := _dir()
	var net = ClientTests.Net.new(d)
	net.o.match_wait = 0  # the CPU at once
	var c: RefCounted = net.client("ANDREY", OnlineTests.HERO)
	c.enter(func(_e): pass)
	var got := []
	c.find_battle(0, func(e): got.append(e))
	eq(got, [""])
	check(c.battle != null, "the room message made the battle")
	var b: RefCounted = c.battle
	var room: RefCounted = net.session(c).room
	eq(
		[b.mode, b.my_slot, b.fighters[0].name, b.fighters[0].slot, b.fighters[1].slot],
		[0, 0, "ANDREY", 0, 1],
		"mine first"
	)
	eq([b.allies_alive, b.enemies_alive, b.fighters[0].x, b.fighters[0].y], [1, 1, 42, 225])
	eq(b.state, OnlineBattle.QUOTES, "all ready: the quotes")
	var seen := _play(c)
	for s in [
		OnlineBattle.ROUND,
		OnlineBattle.CHOOSE,
		OnlineBattle.BAR,
		OnlineBattle.SENT,
		OnlineBattle.REVEAL,
		OnlineBattle.TURN,
		OnlineBattle.OVER,
		OnlineBattle.RESULT
	]:
		check(seen.has(s), "went through %d: %s" % [s, seen])
	eq(b.state, OnlineBattle.RESULT)
	check(b.left, "OK on the result")
	var won: bool = room.battle.winner() == 0
	eq(b.battle_won, int(won), "the server's verdict")
	for i in 2:
		var f: RefCounted = b.fighters[i]
		eq(f.hp, room.battle.fighters[f.slot].hp, "HP as the server's, fighter %d" % i)
	eq([b.wins, b.losses], [1, 0] if won else [0, 1])
	check(net.session(c).room == null, "out of the room")
	ServerTests._rm(d)


func test_a_two_on_two_targets_and_a_mission_stage() -> void:
	var d := _dir()
	var net = ClientTests.Net.new(d)
	net.o.match_wait = 0
	var c: RefCounted = net.client("ANDREY", OnlineTests.HERO)
	c.enter(func(_e): pass)
	c.find_battle(1, func(_e): pass)
	var b: RefCounted = c.battle
	eq([b.mode, b.allies_alive, b.enemies_alive], [1, 2, 2])
	eq([b.fighters[0].y, b.fighters[1].y], [202, 202], "row 0 a little up")
	var room: RefCounted = net.session(c).room
	var seen := _play(c)
	check(seen.has(OnlineBattle.RESULT), "2-on-2 to the end: %s" % [seen])
	eq(b.fighters[0].hp, room.battle.fighters[0].hp, "my HP as the server's")
	if b.fighters[0].hp > 0:  # once I fall, the others fight it out on the server alone
		for i in 4:
			var f: RefCounted = b.fighters[i]
			eq(f.hp, room.battle.fighters[f.slot].hp, "HP as the server's, fighter %d" % i)
	c.battle_over()
	c.find_battle(2, func(_e): pass)
	b = c.battle
	eq(
		[b.mode, b.state, b.stage, b.stage_count >= 2],
		[2, OnlineBattle.STAGE_INTRO, 1, true],
		"a mission: its first stage"
	)
	room = net.session(c).room
	room.battle.fighters[1].hp = 1  # the stage's foes fall at the first blow
	if room.battle.fighters.has(3):
		room.battle.fighters[3].hp = 1
	seen = _play(c, 3000)
	check(seen.has(OnlineBattle.STAGE_END), "stage 1 cleared: %s" % [seen])
	check(b.stage >= 2 or b.state == OnlineBattle.RESULT, "the next stage came")
	ServerTests._rm(d)


func test_choosing_skills_targets_and_the_time_out() -> void:
	var b := OnlineBattle.new(
		func(_m): pass,
		{"slots": [11, 99, 3, 99], "skill_cost": [25, 30, 35, 40, 45, 50, 31, 40, 40, 45, 50]}
	)
	var sent: Array = []
	b.send = func(m): sent.append(m)
	b.on_push(
		{
			"t": "room",
			"via": "match",
			"bg": 0,
			"slot": 0,
			"mode": 1,
			"fighters":
			[
				{"slot": 1, "name": "A", "hp": 50},
				{"slot": 0, "name": "ME", "hp": 60},
				{"slot": 2, "name": "B", "hp": 40, "cpu": true},
				{"slot": 3, "name": "C", "hp": 45, "cpu": true}
			]
		}
	)
	eq([b.fighters[0].name, b.fighters[1].name, b.allies_alive, b.enemies_alive], ["ME", "A", 2, 2])
	b.on_push({"t": "round_start", "bar_speed": 0})
	eq(b.skill_slots, [11, 3])
	b.key("down")
	eq(b.state, OnlineBattle.CHOOSE, "no MP for a skill")
	b.fighters[0].mp = 30
	check(b.skill_ready(3) and not b.skill_ready(11))
	b.key("down")
	eq(b.state, OnlineBattle.SKILLS)
	b.key("fire")
	eq(b.state, OnlineBattle.SKILLS, "Fury needs 40")
	b.key("down")
	b.key("fire")
	eq([b.state, b.chosen_action], [OnlineBattle.TARGET, 3], "Whirlwind Sabre")
	b.tick()
	eq(b.target_cursor, 1, "the first foe")
	b.key("down")
	eq(b.target_cursor, 3, "the other foe")
	b.key("fire")
	b.tick()
	eq([b.state, b.hit_score], [OnlineBattle.SENT, 0], "a skill skips the bar")
	for i in 4:
		b.tick()
	eq(sent[-1], {"t": "mp_turn", "target": 3, "action": 3, "hit": 0})
	b.on_push({"t": "round_start", "bar_speed": 0})
	for i in 10 * 9 + 1:
		b.tick()
	eq([b.chosen_action, b.state], [1, OnlineBattle.SENT], "time out: Defend")
	b.on_push({"t": "round_start", "bar_speed": 0})
	b.key("auto")
	eq(b.choose_secs, 1, "auto-battle: this round too")
	for i in 10:
		b.tick()
	eq(b.chosen_action, OnlineBattle.AUTO, "the bot chooses")
	b.on_push({"t": "round_start", "bar_speed": 0})
	b.key("back")
	check(b.exit_prompt, "Exit Battle?")
	b.key("left")
	b.key("fire")
	check(b.left and sent[-1].t == "mp_exit", "left the battle")


func test_the_battle_screen_shows_a_duel() -> void:
	var d := _dir()
	var net = ClientTests.Net.new(d)
	net.o.match_wait = 0
	var c: RefCounted = net.client("ANDREY", OnlineTests.HERO)
	c.enter(func(_e): pass)
	c.find_battle(0, func(_e): pass)
	var old: Dictionary = Router.params
	Router.params = {"online": c, "profile_path": d.path_join("hero.json")}
	var screen: Control = OnlineBattleScreen.new()
	root.add_child(screen)
	var b: RefCounted = c.battle
	eq(screen.battle, b, "the client's battle")
	check(screen.arena.ground != null and screen.arena.scenery == b.bg & 3, "the field built")
	check(screen.bodies[0].position.x < 0 and screen.bodies[1].position.x > 0, "mine on the left")
	eq([screen.bodies[2].visible, screen.bodies[3].visible], [false, false], "a duel: two fighters")
	eq(screen.figures[0].kind, BattleMotion.kind_of(b.fighters[0]), "me: the model of my class")
	check(
		screen.figures[1].kind in BattleMotion.RIVALS, "the CPU: a rival " + screen.figures[1].kind
	)
	check(is_equal_approx(screen.bodies[1].rotation.y, -PI / 2.0), "facing left")
	var seen := {}
	for i in 30000:
		if screen.battle == null:
			break
		screen._process(OnlineBattle.TICK_MS / 1000.0)
		if screen.battle == null:
			break
		var st: int = b.state
		var now := [
			screen.pad.visible,
			screen.bar.visible,
			screen.center_text.text if screen.center.visible else ""
		]
		if not seen.has(st):
			seen[st] = now
		seen[st] = [seen[st][0] or now[0], seen[st][1] or now[1], seen[st][2]]
		match st:
			OnlineBattle.CHOOSE:
				if b.state_ticks == 3:
					screen.press("right")
			OnlineBattle.TARGET:
				screen.press("fire")
			OnlineBattle.BAR:
				if b.state_ticks == 6:
					screen.press("fire")
			OnlineBattle.RESULT:
				if b.result_shown():
					check(
						screen.center_text.text.contains(
							(
								tr("online.battle_win")
								if b.battle_won == 1
								else tr("online.battle_lose")
							)
						),
						"the result: " + screen.center_text.text
					)
					screen.press("fire")
	eq(seen.get(OnlineBattle.CHOOSE, [])[0], true, "the pad to choose")
	eq(seen.get(OnlineBattle.BAR, [])[1], true, "the timing bar")
	eq(
		seen.get(OnlineBattle.QUOTES, [false, false, "?"]),
		[false, false, ""],
		"the quotes over the fighters"
	)
	check(screen.battle == null and c.battle == null, "OK: the battle is over")
	screen.free()
	Router.params = old
	ServerTests._rm(d)


func test_the_battle_screen_leaves_when_kicked() -> void:
	var d := _dir()
	var net = ClientTests.Net.new(d)
	net.o.match_wait = 0
	var c: RefCounted = net.client("ANDREY", OnlineTests.HERO)
	c.enter(func(_e): pass)
	c.find_battle(0, func(_e): pass)
	var old: Dictionary = Router.params
	Router.params = {"online": c, "profile_path": d.path_join("hero.json")}
	var screen: Control = OnlineBattleScreen.new()
	root.add_child(screen)
	c.on_push({"t": "kicked"})
	screen._process(0.2)
	check(screen.battle == null and c.kicked, "another device took the account: out of the battle")
	screen.free()
	Router.params = old
	ServerTests._rm(d)


func _key(code: Key) -> InputEventKey:
	var ev := InputEventKey.new()
	ev.physical_keycode = code
	ev.keycode = code
	ev.pressed = true
	return ev


func test_auto_battle_by_tab_f_or_back() -> void:
	var d := _dir()
	var net = ClientTests.Net.new(d)
	net.o.match_wait = 0
	var c: RefCounted = net.client("ANDREY", OnlineTests.HERO)
	c.enter(func(_e): pass)
	c.find_battle(0, func(_e): pass)
	var old: Dictionary = Router.params
	Router.params = {"online": c, "profile_path": d.path_join("hero.json")}
	var screen: Control = OnlineBattleScreen.new()
	root.add_child(screen)
	var back := InputEventJoypadButton.new()
	back.button_index = JOY_BUTTON_BACK
	back.pressed = true
	var seen := []
	for ev in [_key(KEY_TAB), _key(KEY_F), back]:
		screen._unhandled_input(ev)
		seen.append(c.battle.auto_battle)
	eq(
		seen,
		[true, false, true],
		"Tab, F and the pad's Back each turn it over, as auto-hunt on the map"
	)
	screen.free()
	Router.params = old
	ServerTests._rm(d)


func test_battle_hints_name_the_pad_after_the_pad() -> void:
	var d := _dir()
	var net = ClientTests.Net.new(d)
	net.o.match_wait = 0
	var c: RefCounted = net.client("ANDREY", OnlineTests.HERO)
	c.enter(func(_e): pass)
	c.find_battle(0, func(_e): pass)
	var old: Dictionary = Router.params
	Router.params = {"online": c, "profile_path": d.path_join("hero.json")}
	var screen: Control = OnlineBattleScreen.new()
	root.add_child(screen)
	var was: String = InputSetup.device
	var states := {
		OnlineBattle.CHOOSE: "choose",
		OnlineBattle.SKILLS: "skills",
		OnlineBattle.TARGET: "target",
		OnlineBattle.BAR: "bar"
	}
	c.battle.auto_battle = false
	c.battle.exit_prompt = false
	for device in ["keys", "pad"]:
		InputSetup.device = device
		for st in states:
			c.battle.state = st
			var key: String = "online.battle_hint_" + states[st]
			eq(screen.hint_text(), InputSetup.hint(key), "%s: %s" % [device, key])
	InputSetup.device = "keys"
	eq(
		InputSetup.hint("online.battle_hint_choose"),
		"Arrows: choose the action   Esc: exit the battle   Tab / F: auto-battle",
		"the keyboard's line"
	)
	c.battle.state = OnlineBattle.BAR
	InputSetup.device = "pad"
	eq(screen.hint_text(), "A: stop the bar at the mark", "the pad's A")
	c.battle.state = OnlineBattle.CHOOSE
	eq(
		screen.hint_text(),
		"D-pad: choose the action   B: exit the battle   Back: auto-battle",
		"the pad's B and Back"
	)
	InputSetup.device = was
	screen.free()
	Router.params = old
	ServerTests._rm(d)


func test_auto_corner() -> void:
	var d := _dir()
	var net = ClientTests.Net.new(d)
	net.o.match_wait = 0
	var c: RefCounted = net.client("ANDREY", OnlineTests.HERO)
	c.enter(func(_e): pass)
	c.find_battle(0, func(_e): pass)
	var old: Dictionary = Router.params
	Router.params = {"online": c, "profile_path": d.path_join("hero.json")}
	var screen: Control = OnlineBattleScreen.new()
	root.add_child(screen)
	var was: String = InputSetup.device
	InputSetup.device = "keys"
	c.battle.auto_battle = false
	c.battle.state = OnlineBattle.QUOTES
	screen._refresh()
	check(not screen.auto_button.visible, "not over the quotes")
	c.battle.state = OnlineBattle.CHOOSE
	screen._refresh()
	check(screen.auto_button.visible, "while the actions are chosen")
	eq(screen.auto_button.text, "AUTO: Tab/F", "off: white, with its keys")
	eq(screen.auto_button.get_theme_color("font_color"), Color.WHITE, "white")
	InputSetup.device = "pad"
	screen._refresh()
	eq(screen.auto_button.text, "AUTO: Back", "the pad's key after the pad")
	screen.auto_button.pressed.emit()
	check(c.battle.auto_battle, "a click turns it on")
	eq(screen.auto_button.text, "AUTO", "on")
	eq(screen.auto_button.get_theme_color("font_color"), OnlineBattleScreen.AUTO_ON, "gold")
	InputSetup.device = was
	screen.free()
	Router.params = old
	ServerTests._rm(d)
