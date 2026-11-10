class_name OnlineBattle
extends RefCounted
## One online battle on this device: what the server's pushes say (server/room.gd), played
## back step by step as the game's battle screen does it in pyport (pow/game/online), one step
## every TICK_MS. The screen (screens/online_battle/online_battle_screen.gd) draws what is here and
## passes the keys on.
##
## Places are on the original's 240 x 320 screen: a fighter of the left team (slot % 2 == 0)
## stands at (x, y), one of the right team at (W - x, y), drawn turned; every fighter's x grows
## towards the other side. Fighter 0 is mine.
##
## The steps: ROOM (the fighters come), STAGE_INTRO (a mission's stage, then mp_intro_done),
## QUOTES, then each round ROUND (mp_ready) -> CHOOSE (10 s: Left Defend, Right Attack, Up
## Evade, Down a skill) -> SKILLS -> TARGET -> BAR (the timing bar) -> SENT (mp_turn) ->
## REVEAL (everyone's card) -> TURN (each record played back: scripts/net/battle_playback.gd)
## -> ROUND ... -> OVER (mp_ready) -> STAGE_END (mp_stage_next) or RESULT. The fighters are
## OnlineFighter (scripts/net/online_fighter.gd).

const W := 240
const H := 320
const CX := 120
const CY := 160
const HP_BAR_W := 89  # W / 2 - 28 - 3
const TICK_MS := 110  # one step (the game speed Normal)
const TIME_MS := 100  # a time of N ms lasts N / TIME_MS steps
const BAR_LEFT := CX - 44
const MARK := BAR_LEFT + 72  # the timing bar's mark (100 %)
const CHOOSE_SECS := 10
const AUTO := 255  # the server's bot chooses (auto-battle)
const NO_ACTION := 99
const CHOOSING_SKILL := 20
const EMPTY_SKILL := 99
const DATA := "res://data/mp.json"

const ROOM := 90
const STAGE_INTRO := 91
const QUOTES := 92
const ROUND := 93
const CHOOSE := 94
const SKILLS := 95
const TARGET := 96
const BAR := 97
const SENT := 98
const REVEAL := 99
const NO_BATTLE := 100
const TURN_START := 101
const TURN := 102
const OVER := 103
const STAGE_END := 104
const RESULT := 105

const PLAYER := 0
const CPU := 1
const MONSTER := 2

const RES_HIT := 1
const RES_EVADED := 2
## the reactions of a target: hit, hit while defending, evaded
const REACT_HIT := 1
const REACT_DEFENDED := 4
const REACT_EVADE := 5

## send(msg): a request of the battle to the server (mp_ready, mp_turn, ...), no answer needed.
var send: Callable
var rng := RandomNumberGenerator.new()
var tables: Dictionary = {}
var first_frame: Array = []
var anim_lengths: Array = []
var steps: Array = []

var state := ROOM
var prev_state := -1
var state_ticks := 0
var timer_ticks := 0
var via := ""
var bg := 0
var mode := 0  # 0 1-on-1, 1 2-on-2, 2 Solo Mission
var my_slot := 0
var fighters: Array[OnlineFighter] = []
var allies_alive := 0
var enemies_alive := 0
var round_no := 0
var stage_title := ""
var stage := 0
var stage_count := 0

var skill_slots: Array = []  # my skills in the slots (3..13)
var skill_costs: Array = []  # what each skill (3..13) takes of the MP gauge
var chosen_action := NO_ACTION
var choose_secs := 0
var skill_cursor := 0
var target_cursor := 0
var exit_asked := false
var exit_prompt := false
var exit_cursor := 1
var exit_ticks := 0
var auto_battle := false
var bar_speed := 0
var bar_x := BAR_LEFT
var bar_shown := false
var hit_score := 0

var turn_actions: Array = [0, 0, 0, 0]  # by fighter
var records: Array = []
var rec := {}  # the record played back
var turn_rec := 0
var attacker := 0
var target := -1
var target2 := -1
var target_reaction := 0
var target2_reaction := 0
var anim_frame := 0
var anim_length := 0
var run_dx := 0
var run_dy := 0
var damage_tick := -1
var damage_shown: Array = []  # [screen x, y of the feet, pixels over them, hp change] this step

var battle_won := 0
var result := {}  # battle_end: win, gold, grade, fame, exp, loot, rank
var wins := 0
var losses := 0
var left := false  # the player chose Exit Battle, or OK on the result: back to the menu
var sounds: Array = []  # sounds started this step (mp/snd<n>.ogg)


func _init(request: Callable, me: Dictionary = {}) -> void:
	send = request
	var f := FileAccess.open(DATA, FileAccess.READ)
	if f != null:
		tables = JSON.parse_string(f.get_as_text())
	first_frame = tables.get("anim_first_frame", [])
	anim_lengths = tables.get("anim_length", [])
	steps = tables.get("anim_steps", [])
	for i in 4:
		fighters.append(OnlineFighter.new())
	wins = int(me.get("wins", 0))
	losses = int(me.get("losses", 0))
	for s in me.get("slots", []):
		if int(s) != EMPTY_SKILL:
			skill_slots.append(int(s))
	skill_costs = me.get("skill_cost", [])
	rng.randomize()


# --- the server's pushes --------------------------------------------------------------------
func on_push(m: Dictionary) -> void:
	match str(m.get("t", "")):
		"room":
			via = str(m.get("via", ""))
			bg = int(m.get("bg", 0))
			my_slot = int(m.get("slot", 0))
			mode = int(m.get("mode", 0))
			for f in fighters:
				f.present = false
			allies_alive = 0
			enemies_alive = 0
			var list: Array = m.get("fighters", [])
			for w in list:  # mine first: fighter 0
				if int(w.get("slot", -1)) == my_slot:
					_join(w)
			for w in list:
				if int(w.get("slot", -1)) != my_slot:
					_join(w)
			set_state(ROOM)
		"room_join":
			_join(m.get("fighter", {}))
		"stage_info":
			stage_title = str(m.get("title", ""))
			stage_count = int(m.get("stages", 1))
			stage = int(m.get("stage", 1))
			set_state(STAGE_INTRO)
		"all_ready":
			set_state(QUOTES)
		"round_start":
			chosen_action = NO_ACTION
			set_timer(9)
			choose_secs = 1 if auto_battle else CHOOSE_SECS
			exit_asked = false
			set_state(CHOOSE)
		"turn_result":
			var actions: Array = m.get("actions", [0, 0, 0, 0])
			for i in 4:
				var f := fighters[i]
				if f.present and f.slot < actions.size():
					turn_actions[i] = int(actions[f.slot])
			records = m.get("records", [])
			set_state(REVEAL)
		"stage_end":
			bg = int(m.get("bg", bg))
			set_state(STAGE_END)
		"battle_end":
			result = m.duplicate()
			battle_won = int(m.get("win", 0))
			if mode != 2:
				if battle_won == 1:
					wins += 1
				else:
					losses += 1
			set_state(RESULT)


## A fighter of the room message (server/battle.gd Fighter.wire) in the first free place.
func _join(w: Dictionary) -> void:
	var i := 0
	while i < 4 and fighters[i].present:
		i += 1
	if i >= 4:
		return
	var f := OnlineFighter.new()
	f.present = true
	f.slot = int(w.get("slot", 0))
	f.name = str(w.get("name", ""))
	f.level = int(w.get("level", 1))
	f.wins = int(w.get("wins", 0))
	f.losses = int(w.get("losses", 0))
	f.hp = int(w.get("hp", 1))
	f.max_hp = maxi(1, f.hp)
	f.weapon = clampi(int(w.get("weapon", 0)), 0, 1)
	f.face = clampi(int(w.get("face", 0)), 0, 3)
	f.kind = (
		MONSTER if bool(w.get("monster", false)) else (CPU if bool(w.get("cpu", false)) else PLAYER)
	)
	f.quote_start = str(w.get("quote_start", ""))
	f.quote_win = str(w.get("quote_win", ""))
	f.mp = 0
	f.blink = rng.randi_range(0, 3)
	fighters[i] = f
	place(f)
	if f.team() == my_slot % 2:
		allies_alive += 1
	else:
		enemies_alive += 1


func place(f: OnlineFighter) -> void:
	f.x = 42
	f.y = CY + 65
	if mode != 0:
		f.y += (-1 if f.row() == 0 else 1) * 23


# --- steps ----------------------------------------------------------------------------------
func set_state(s: int) -> void:
	state = s
	state_ticks = 0


func set_timer(ticks: int) -> void:
	timer_ticks = ticks


## One step: the timer, then what the state does, then the step count.
func tick() -> void:
	sounds.clear()
	damage_shown.clear()
	for f in fighters:
		f.lift = 0
	if not exit_prompt:
		_timer()
	prev_state = state
	match state:
		ROOM:
			state_ticks = maxi(state_ticks, 2)
			BattlePlayback.idle_all(self)
		STAGE_INTRO:
			BattlePlayback.idle_all(self)
			if state_ticks == 1500 / TIME_MS:
				send.call({"t": "mp_intro_done"})
		QUOTES:
			state_ticks = maxi(state_ticks, 2)
			BattlePlayback.idle_all(self)
			if state_ticks == 2500 / TIME_MS:
				round_no = 0
				set_state(ROUND)
		ROUND:
			_round()
		CHOOSE:
			if state_ticks < 2:
				state_ticks = 2
				bar_shown = false
			if exit_prompt:
				exit_ticks += 1
				if exit_ticks >= 15000 / TIME_MS:
					exit_prompt = false
			else:
				BattlePlayback.idle_all(self)
		SKILLS:
			if state_ticks < 2:
				state_ticks = 2
				skill_cursor = 0
			BattlePlayback.idle_all(self)
		TARGET:
			if state_ticks < 2:
				state_ticks = 2
				_first_target()
			BattlePlayback.idle_all(self)
		BAR:
			BattlePlayback.idle_all(self)
			if state_ticks < 2:
				state_ticks = 2
				if chosen_action > 2:
					stop_timing()
				else:
					_start_bar()
		SENT:
			BattlePlayback.idle_all(self)
			if state_ticks < 2:
				state_ticks = 2
				if chosen_action <= 2 and bar_shown and hit_score != 20:
					sounds.append(0)  # a hit on the bar
			elif state_ticks == 4:
				send.call(
					{
						"t": "mp_turn",
						"target": fighters[target_cursor].slot,
						"action": chosen_action,
						"hit": hit_score
					}
				)
		REVEAL:
			state_ticks = maxi(state_ticks, 2)
			BattlePlayback.idle_all(self)
			if state_ticks >= 4:
				turn_rec = 0
				BattlePlayback.next_record(self)
		NO_BATTLE:
			BattlePlayback.idle_all(self)
			if state_ticks < 2:
				state_ticks = 2
			elif state_ticks == 1000 / TIME_MS:
				set_state(ROUND)
		TURN_START:
			BattlePlayback.idle_all(self)
			BattlePlayback.reset_turn(self)
			set_state(TURN)
		TURN:
			BattlePlayback.turn_fighters(self)
			BattlePlayback.damage(self)
			anim_frame += 1
			BattlePlayback.step_turn(self)
		OVER:
			BattlePlayback.idle_all(self)
			if state_ticks < 2:
				state_ticks = 2
				send.call({"t": "mp_ready"})
		STAGE_END:
			_stage_end()
		RESULT:
			if state_ticks < 5:
				state_ticks = 5
				sounds.append(5 if battle_won == 1 else 4)
			BattlePlayback.idle_all(self)
	if prev_state == state and state_ticks < 25000:
		state_ticks += 1


## The timer of the round: the timing bar moves a step each tick; else the seconds to choose
## run out (Defend, or the bot on auto-battle).
func _timer() -> void:
	if timer_ticks == 1:
		timer_ticks = 0
		if state == BAR:
			bar_x += bar_speed
			if bar_x > MARK + bar_speed:
				bar_x = MARK + bar_speed
			else:
				set_timer(1)
		else:
			choose_secs -= 1
			if choose_secs == 0:
				chosen_action = AUTO if auto_battle else 1
				bar_x = MARK + bar_speed
				stop_timing()
			set_timer(9)
	elif timer_ticks > 0:
		timer_ticks -= 1


func _round() -> void:
	if state_ticks < 2:
		state_ticks = 2
		round_no += 1
		if allies_alive == 0 or enemies_alive == 0 or fighters[0].hp == 0:
			set_state(OVER)
			return
		_tick_statuses()
	elif state_ticks == 1000 / TIME_MS:
		send.call({"t": "mp_ready"})
	BattlePlayback.idle_all(self)


func _tick_statuses() -> void:
	for f in fighters:
		if f.present and f.status in [11, 12, 13]:
			f.status_ticks -= 1
			if f.status_ticks <= 0:
				f.status = 99


func _stage_end() -> void:
	if state_ticks < 2:
		state_ticks = 2
	BattlePlayback.idle_all(self)
	if state_ticks == 1000 / TIME_MS:
		for i in range(1, 4):
			var f := fighters[i]
			if f.present and f.team() != fighters[0].team():
				f.present = false
		enemies_alive = 0
		send.call({"t": "mp_stage_next"})
		for f in fighters:
			f.status = 99
			f.status_ticks = 0
		set_state(ROOM)


# --- choosing -------------------------------------------------------------------------------
## A skill in a slot can be used: the MP gauge holds its cost.
func skill_ready(skill: int) -> bool:
	var i := skill - 3
	return i >= 0 and i < skill_costs.size() and fighters[0].mp >= int(skill_costs[i])


func any_skill_ready() -> bool:
	return skill_slots.any(func(s): return skill_ready(int(s)))


func _first_target() -> void:
	var me := fighters[0]
	if chosen_action in [9, 10]:  # a heal: me, or pick an ally
		target_cursor = 0
		if allies_alive > 1:
			return
		start_timing()
		return
	if chosen_action in [0, 3, 4, 5, 6, 7]:
		for i in range(1, 4):
			var f := fighters[i]
			if f.present and f.team() != me.team():
				target_cursor = i
				break
		if enemies_alive > 1:
			return
	start_timing()


func start_timing() -> void:
	timer_ticks = 0
	set_state(BAR)


func _start_bar() -> void:
	bar_speed = [4, 8, 5][rng.randi_range(0, 2)]
	set_timer(1)
	bar_x = BAR_LEFT
	bar_shown = true


func stop_timing() -> void:
	timer_ticks = 0
	if chosen_action > 2:
		hit_score = 0
	else:
		if bar_speed in [6, 7] and absi(MARK - bar_x) <= bar_speed / 2:
			bar_x = MARK
		if bar_x < MARK:
			hit_score = 20 + bar_x - BAR_LEFT
		elif bar_x == MARK:
			hit_score = 100
		else:
			hit_score = 20
	set_state(SENT)


## A key: "up", "down", "left", "right", "fire", "back"; "auto" turns auto-battle on and off.
func key(k: String) -> void:
	if k == "auto":
		auto_battle = not auto_battle
		if auto_battle and state == CHOOSE and choose_secs > 1:
			choose_secs = 1
		return
	match state:
		CHOOSE:
			_key_choose(k)
		SKILLS:
			_key_skills(k)
		TARGET:
			_key_target(k)
		BAR:
			if state_ticks > 0 and k == "fire":
				stop_timing()
		RESULT:
			if state_ticks > 1000 / TIME_MS and k == "fire":
				left = true


func _key_choose(k: String) -> void:
	if exit_prompt:
		if k == "left" or k == "right":
			exit_cursor = (exit_cursor + 1) % 2
		elif k == "fire":
			exit_prompt = false
			if exit_cursor == 0:  # Yes: the battle is lost, back to the menu
				send.call({"t": "mp_exit"})
				left = true
		return
	chosen_action = NO_ACTION
	match k:
		"up":
			chosen_action = 2
		"left":
			chosen_action = 1
		"right":
			chosen_action = 0
		"down":
			if any_skill_ready():
				chosen_action = CHOOSING_SKILL
		"back":
			if not exit_asked:
				exit_asked = true
				exit_prompt = true
				exit_cursor = 1
				exit_ticks = 0
	if chosen_action == CHOOSING_SKILL:
		set_state(SKILLS)
	elif chosen_action != NO_ACTION:
		set_state(TARGET)


func _key_skills(k: String) -> void:
	var n := skill_slots.size()
	if n == 0:
		chosen_action = NO_ACTION
		set_state(CHOOSE)
		return
	match k:
		"up":
			skill_cursor = skill_cursor - 1 if skill_cursor > 0 else n - 1
		"down":
			skill_cursor = skill_cursor + 1 if skill_cursor < n - 1 else 0
		"fire":
			var s := int(skill_slots[skill_cursor])
			if skill_ready(s):
				chosen_action = s
				set_state(TARGET)
		"back":
			chosen_action = NO_ACTION
			set_state(CHOOSE)


func _key_target(k: String) -> void:
	if k == "up" or k == "down":
		var cur := fighters[target_cursor]
		var from := (
			0 if chosen_action in [9, 10] else (1 if chosen_action in [0, 3, 4, 5, 6, 7] else 4)
		)
		for i in range(from, 4):
			var f := fighters[i]
			if f.present and f.team() == cur.team() and f.slot != cur.slot:
				target_cursor = i
				return
		return
	if k == "fire":
		start_timing()
	elif k == "back":
		if chosen_action in [3, 4, 5, 6, 7, 9, 10]:
			set_state(SKILLS)
		else:
			set_state(CHOOSE)


# --- what the screen shows ------------------------------------------------------------------
## The card of fighter i this step: the action it shows, or -1.
func card_action(i: int) -> int:
	var f := fighters[i]
	if not f.present or f.hp <= 0:
		return -1
	if state == REVEAL:
		return int(turn_actions[i])
	if state != TURN:
		return -1
	if i == attacker:
		return BattlePlayback.field(self, "action")
	if i == target:
		return BattlePlayback.field(self, "result")
	if i == target2:
		return BattlePlayback.field(self, "result2")
	return -1


## Whose quotes show: 0 or 1 a side at the start, 2 the winners at the end, -1 none.
func quote_side_shown() -> int:
	if state == QUOTES:
		if state_ticks >= 1500 / TIME_MS:
			return 1
		if state_ticks >= 500 / TIME_MS:
			return 0
		return -1
	if state == RESULT and state_ticks < 1500 / TIME_MS:
		return 2
	return -1


## Fighter i says its quote now (side as quote_side_shown).
func says_quote(i: int, side: int) -> bool:
	var f := fighters[i]
	if not f.present:
		return false
	if side == 2:
		return (f.team() == fighters[0].slot % 2) == (battle_won == 1)
	return f.team() == side


func result_shown() -> bool:
	return state == RESULT and state_ticks >= 1500 / TIME_MS
