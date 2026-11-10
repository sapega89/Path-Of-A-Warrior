class_name OnlineBattle
extends RefCounted
# gdlint: disable=max-file-lines
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
## REVEAL (everyone's card) -> TURN (each record played back) -> ROUND ... -> OVER (mp_ready)
## -> STAGE_END (mp_stage_next) or RESULT.

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


class Fighter:
	var present := false
	var slot := 0
	var name := ""
	var alt_name := ""
	var level := 1
	var wins := 0
	var losses := 0
	var hp := 0
	var max_hp := 1
	var mp := 0
	var weapon := 0
	var face := 0
	var kind := PLAYER
	var quote_start := ""
	var quote_win := ""
	var x := 0
	var y := 0
	var frame := 0
	var anim := 0
	var anim_tick := 0
	var anim_len := 0
	var hp_target := 0
	var mp_target := 0
	var hp_step := 0
	var mp_step := 0
	var hp_delta := 0
	var blink := 0
	var status := 99  # 11..13: a soul's aura (its action), 99 none
	var status_ticks := 0
	## How high over the ground the fighter is now, in pixels: the part of an animation's
	## up-and-down that is a leap, not a step along the ground (the 2.5D screen shows it as
	## height; y stays as on the original screen).
	var lift := 0
	var leap_from := 0

	func team() -> int:
		return slot % 2

	func row() -> int:
		return slot / 2

	func mirrored() -> bool:
		return slot % 2 != 0


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
var fighters: Array[Fighter] = []
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
		fighters.append(Fighter.new())
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
	var f := Fighter.new()
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


func place(f: Fighter) -> void:
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
			_idle_all()
		STAGE_INTRO:
			_idle_all()
			if state_ticks == 1500 / TIME_MS:
				send.call({"t": "mp_intro_done"})
		QUOTES:
			state_ticks = maxi(state_ticks, 2)
			_idle_all()
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
				_idle_all()
		SKILLS:
			if state_ticks < 2:
				state_ticks = 2
				skill_cursor = 0
			_idle_all()
		TARGET:
			if state_ticks < 2:
				state_ticks = 2
				_first_target()
			_idle_all()
		BAR:
			_idle_all()
			if state_ticks < 2:
				state_ticks = 2
				if chosen_action > 2:
					stop_timing()
				else:
					_start_bar()
		SENT:
			_idle_all()
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
			_idle_all()
			if state_ticks >= 4:
				turn_rec = 0
				_next_record()
		NO_BATTLE:
			_idle_all()
			if state_ticks < 2:
				state_ticks = 2
			elif state_ticks == 1000 / TIME_MS:
				set_state(ROUND)
		TURN_START:
			_idle_all()
			_reset_turn()
			set_state(TURN)
		TURN:
			_turn_fighters()
			_damage()
			anim_frame += 1
			_step_turn()
		OVER:
			_idle_all()
			if state_ticks < 2:
				state_ticks = 2
				send.call({"t": "mp_ready"})
		STAGE_END:
			_stage_end()
		RESULT:
			if state_ticks < 5:
				state_ticks = 5
				sounds.append(5 if battle_won == 1 else 4)
			_idle_all()
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
	_idle_all()


func _tick_statuses() -> void:
	for f in fighters:
		if f.present and f.status in [11, 12, 13]:
			f.status_ticks -= 1
			if f.status_ticks <= 0:
				f.status = 99


func _stage_end() -> void:
	if state_ticks < 2:
		state_ticks = 2
	_idle_all()
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


# --- playing a round back -------------------------------------------------------------------
func _next_record() -> void:
	if records.is_empty():
		set_state(NO_BATTLE)
	elif turn_rec < records.size():
		set_state(TURN_START)
	else:
		set_state(ROUND)


func _r(field: String) -> int:
	return int(rec.get(field, 0))


func _update_bars(f: Fighter) -> void:
	f.hp_delta = f.hp_target - f.hp
	f.hp_step = f.hp_delta / 5
	if f.hp_step == 0:
		f.hp_step = signi(f.hp_target - f.hp)
	f.mp_step = (f.mp_target - f.mp) / 5
	if f.mp_step == 0:
		f.mp_step = signi(f.mp_target - f.mp)


func _reset_turn() -> void:
	rec = records[turn_rec]
	anim_frame = 0
	target2 = -1
	damage_tick = -1
	for i in 4:
		var f := fighters[i]
		if not f.present:
			continue
		f.anim = 0
		f.anim_tick = 0
		f.anim_len = 0
		f.hp_delta = 0
		if f.slot == _r("actor"):
			attacker = i
			f.hp_target = _r("actor_hp")
			f.mp_target = _r("actor_mp")
			_update_bars(f)
		if f.slot == _r("target"):
			target = i
			f.hp_target = _r("target_hp")
			f.mp_target = _r("target_mp")
			_update_bars(f)
			if _r("result") == RES_HIT:
				target_reaction = REACT_DEFENDED if turn_actions[i] == 1 else REACT_HIT
			elif _r("result") == RES_EVADED:
				target_reaction = REACT_EVADE
		if _r("has2nd") > 0 and f.slot == _r("target2"):
			target2 = i
			f.hp_target = _r("target2_hp")
			f.mp_target = _r("target2_mp")
			_update_bars(f)
			if _r("result2") == RES_HIT:
				target2_reaction = REACT_DEFENDED if turn_actions[i] == 1 else REACT_HIT
			elif _r("result2") == RES_EVADED:
				target2_reaction = REACT_EVADE
	var a := fighters[attacker]
	var action := _r("action")
	if action in [3, 4, 5, 6, 7, 8]:
		a.anim = 8  # the ready pose
	elif action in [2, 9, 10]:
		a.anim = 12  # a heal
	elif action in [11, 12, 13]:
		a.anim = 13  # a soul
	elif action == 0:
		a.anim = 2  # the run to the target
		_run_to_target(a)
	anim_length = int(anim_lengths[a.anim])


func _run_to_target(a: Fighter) -> void:
	run_dx = (W - 67 - 42) / int(anim_lengths[a.anim])
	run_dy = 0
	if mode != 0 and a.row() != _r("target") / 2:
		run_dy = (46 if a.row() == 0 else -46) / int(anim_lengths[a.anim])


## The fighters during a record: the others first, then the one acting.
func _turn_fighters() -> void:
	for i in 4:
		var f := fighters[i]
		if not f.present or i == attacker:
			continue
		match f.anim:
			0:
				_idle(i)
			1, 4:
				var id := f.anim + (21 if f.kind == MONSTER else 0)
				f.frame = int(first_frame[id])
				f.x -= 2
			5:
				f.frame = int(first_frame[26 if f.kind == MONSTER else 5])
				if f.anim_tick == 0:
					f.x -= 6
					sounds.append(3)
				elif f.anim_tick == 1:
					f.x -= 2
			6:
				_dying(f)
			_:
				_anim(f)
	var a := fighters[attacker]
	if a.anim == 2 or a.anim == 28:
		a.frame = int(first_frame[23 if a.kind == MONSTER else 2])
		a.x += run_dx
		a.y += run_dy
	elif a.anim == 6:
		_dying(a)
	else:
		_anim(a)


func _dying(f: Fighter) -> void:
	f.frame = int(first_frame[27 if f.kind == MONSTER else 6]) + anim_frame


func _anim(f: Fighter) -> void:
	var id := f.anim
	if f.kind == MONSTER and id == 3:
		id = 24
	var at := anim_frame
	if id == 12 and at >= 4:
		at = 4
	f.frame = int(first_frame[id]) + at
	if id < steps.size():
		var st: Array = steps[id]
		if at == 0:
			f.leap_from = f.y
		if 3 * at + 2 < st.size():
			f.x += _signed(int(st[3 * at + 1]))
			f.y += _signed(int(st[3 * at + 2]))
		# the ground under the fighter moves evenly from where the animation began to where
		# it ends; the rest of the way up and down is height
		var n := st.size() / 3
		var total := 0
		for k in n:
			total += _signed(int(st[3 * k + 2]))
		if n > 0:
			f.lift = f.leap_from + total * mini(at + 1, n) / n - f.y


static func _signed(v: int) -> int:
	return -(v & 0x7F) if v & 0x80 else v & 0x7F


## The pose of a fighter standing (blinking), or lying when fallen.
func _idle(i: int) -> void:
	var f := fighters[i]
	if f.hp > 0:
		if state_ticks % 4 == f.blink:
			f.frame = (state_ticks / 4) % 2
		if f.frame != 0 and f.frame != 1:
			f.frame = 0
	else:
		f.frame = int(first_frame[6]) + 1


func _idle_all() -> void:
	for i in 4:
		if fighters[i].present:
			_idle(i)


## The HP and MP of those in the record move to what the record says, the
## change shown over them.
func _damage() -> void:
	if damage_tick < 0:
		return
	for i in _involved():
		var f := fighters[i]
		if f.hp != f.hp_target:
			f.hp = maxi(0, f.hp + f.hp_step)
		if f.mp != f.mp_target:
			f.mp = maxi(0, f.mp + f.mp_step)
		if f.hp_delta != 0:
			var sx := (W - f.x) if f.mirrored() else f.x
			damage_shown.append([sx, f.y, 40 + 2 * damage_tick, f.hp_delta])
	for i in _involved():
		if fighters[i].hp == 0:
			fighters[i].hp = 1  # still standing until the record's end
	damage_tick += 1


## The fighters in the record played back: the one acting and its targets, each once.
func _involved() -> Array:
	var out: Array = []
	for i in [attacker, target, target2]:
		if i >= 0 and fighters[i].present and not out.has(i):
			out.append(i)
	return out


func _step_turn() -> void:
	if damage_tick >= 5:
		damage_tick = -1
		for i in _involved():
			fighters[i].hp = fighters[i].hp_target
			fighters[i].mp = fighters[i].mp_target
	var a := fighters[attacker]
	if anim_frame >= anim_length:
		anim_frame = 0
		match a.anim:
			2, 17, 18, 19:
				_after_run_in()
			8:
				_after_ready()
			20:
				if _r("action") == 8:
					fighters[attacker].anim = 16
			3, 9, 10, 11, 14, 15, 16:
				_after_strike()
			12, 13, 28:
				_after_run_back()
			6:
				turn_rec += 1
				_next_record()
		if state != TURN:
			return
		anim_length = int(anim_lengths[fighters[attacker].anim])
	if fighters[attacker].anim != 6:
		_reactions()


func _after_run_in() -> void:
	var a := fighters[attacker]
	a.x = W - 67
	a.y = CY + 65
	if mode != 0:
		a.y += (-1 if _r("target") / 2 == 0 else 1) * 23
	match _r("action"):
		3:
			a.anim = 9
		4:
			a.anim = 10
		5:
			a.anim = 11
		6:
			a.anim = 14
		7:
			a.anim = 15
		0:
			a.anim = 3


func _after_ready() -> void:
	var a := fighters[attacker]
	var action := _r("action")
	if action in [3, 4, 5]:
		a.anim = 2
		_run_to_target(a)
	elif action in [6, 7]:
		if mode == 0 or _r("target") / 2 == _r("actor") / 2:
			a.anim = 17
		elif _r("target") / 2 == 1:
			a.anim = 18
		else:
			a.anim = 19
	elif action == 8:
		a.anim = 20


func _after_strike() -> void:
	if _r("flags") == 3 and fighters[attacker].slot == _r("actor"):  # the target strikes back
		var t := attacker
		attacker = target
		target = t
		fighters[attacker].anim = 3
		target_reaction = REACT_HIT
		return
	damage_tick = 0
	if _r("flags") == 3:
		var t := attacker
		attacker = target
		target = t
		fighters[target].anim = 0
		place(fighters[target])
	var a := fighters[attacker]
	a.anim = 28  # the run back
	var length := int(anim_lengths[28])
	run_dx = (42 - a.x) / length
	run_dy = 0
	if mode != 0 and a.row() != _r("target") / 2:
		run_dy = (-46 if a.row() == 0 else 46) / length


func _after_run_back() -> void:
	var a := fighters[attacker]
	place(a)
	var fallen := -1
	for i in 4:
		var f := fighters[i]
		if not f.present:
			continue
		if a.anim == 13 and f.team() == a.team():  # the soul's aura on the team
			f.status = _r("action")
			f.status_ticks = 3
		if f.hp == 0 and f.hp_delta != 0:
			fallen = i
			f.anim = 6
			if f.team() == fighters[0].team():
				allies_alive -= 1
			else:
				enemies_alive -= 1
	if fallen > 0:
		if a.anim != 6:
			a.anim = 0
		attacker = fallen
		return
	turn_rec += 1
	_next_record()


## When the target flinches, dodges or falls back, and the sounds.
func _reactions() -> void:
	var a := fighters[attacker]
	if a.anim != 12 and a.anim != 13 and _r("flags") != 3:
		for i in [target, target2]:
			if i >= 0 and fighters[i].anim != 0:
				var f := fighters[i]
				f.anim_tick += 1
				if f.anim_tick >= f.anim_len:
					f.anim = 0
					place(f)
	match a.anim:
		3, 9, 10, 11, 14:
			if target_reaction in [REACT_HIT, REACT_DEFENDED]:
				if a.anim == 11 and anim_frame == 17:
					_start_reaction()
					fighters[target].anim_len = 3
					return
				if anim_frame % 2 != 1 or (a.anim == 11 and anim_frame > 10):
					return
				_start_reaction()
				fighters[target].anim_len = 2
			elif target_reaction == REACT_EVADE:
				if _r("flags") == 3:
					if anim_frame != 0:
						return
					var t := fighters[target]
					t.anim = 5
					t.anim_tick = 0
					t.anim_len = anim_length
				else:
					if anim_frame % 2 != 1:
						return
					_start_reaction()
					fighters[target].anim_len = 2
		15:
			if target_reaction in [REACT_HIT, REACT_DEFENDED] and anim_frame == 2:
				_start_reaction()
				fighters[target].anim_len = 4
		16:
			if target_reaction in [REACT_HIT, REACT_DEFENDED] and anim_frame == 8:
				_start_reaction()
				fighters[target].anim_len = 3
				if target2 != -1:
					var t2 := fighters[target2]
					t2.anim = target2_reaction
					t2.anim_tick = 0
					t2.anim_len = 3
		12:
			if anim_frame == 4:
				damage_tick = 0
				sounds.append(6)
		13:
			if (anim_frame == 4 and _r("action") == 13) or anim_frame == 7:
				sounds.append(5)
			elif anim_frame == 5:
				damage_tick = 0


func _start_reaction() -> void:
	var t := fighters[target]
	t.anim = target_reaction
	t.anim_tick = 0
	var a := fighters[attacker]
	sounds.append(2 if a.anim == 16 or a.anim == 15 else 0)


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
		return _r("action")
	if i == target:
		return _r("result")
	if i == target2:
		return _r("result2")
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
