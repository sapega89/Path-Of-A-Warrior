class_name BattlePlayback
extends RefCounted
## A round of the online battle played back, one record after another: each fighter's turn (running
## in, the strike, the target's reaction, running back), the animations, the changes of HP and MP
## and the fallen.
## Static functions over the state of an OnlineBattle (OnlineBattle.tick() runs them).


static func _signed(v: int) -> int:
	return -(v & 0x7F) if v & 0x80 else v & 0x7F


static func next_record(battle: OnlineBattle) -> void:
	if battle.records.is_empty():
		battle.set_state(OnlineBattle.NO_BATTLE)
	elif battle.turn_rec < battle.records.size():
		battle.set_state(OnlineBattle.TURN_START)
	else:
		battle.set_state(OnlineBattle.ROUND)


## A field of the record played back.
static func field(battle: OnlineBattle, key: String) -> int:
	return int(battle.rec.get(key, 0))


static func _update_bars(f: OnlineFighter) -> void:
	f.hp_delta = f.hp_target - f.hp
	f.hp_step = f.hp_delta / 5
	if f.hp_step == 0:
		f.hp_step = signi(f.hp_target - f.hp)
	f.mp_step = (f.mp_target - f.mp) / 5
	if f.mp_step == 0:
		f.mp_step = signi(f.mp_target - f.mp)


static func reset_turn(battle: OnlineBattle) -> void:
	battle.rec = battle.records[battle.turn_rec]
	battle.anim_frame = 0
	battle.target2 = -1
	battle.damage_tick = -1
	for i in 4:
		var f := battle.fighters[i]
		if not f.present:
			continue
		f.anim = 0
		f.anim_tick = 0
		f.anim_len = 0
		f.hp_delta = 0
		if f.slot == field(battle, "actor"):
			battle.attacker = i
			f.hp_target = field(battle, "actor_hp")
			f.mp_target = field(battle, "actor_mp")
			_update_bars(f)
		if f.slot == field(battle, "target"):
			battle.target = i
			f.hp_target = field(battle, "target_hp")
			f.mp_target = field(battle, "target_mp")
			_update_bars(f)
			if field(battle, "result") == OnlineBattle.RES_HIT:
				battle.target_reaction = (
					OnlineBattle.REACT_DEFENDED
					if battle.turn_actions[i] == 1
					else OnlineBattle.REACT_HIT
				)
			elif field(battle, "result") == OnlineBattle.RES_EVADED:
				battle.target_reaction = OnlineBattle.REACT_EVADE
		if field(battle, "has2nd") > 0 and f.slot == field(battle, "target2"):
			battle.target2 = i
			f.hp_target = field(battle, "target2_hp")
			f.mp_target = field(battle, "target2_mp")
			_update_bars(f)
			if field(battle, "result2") == OnlineBattle.RES_HIT:
				battle.target2_reaction = (
					OnlineBattle.REACT_DEFENDED
					if battle.turn_actions[i] == 1
					else OnlineBattle.REACT_HIT
				)
			elif field(battle, "result2") == OnlineBattle.RES_EVADED:
				battle.target2_reaction = OnlineBattle.REACT_EVADE
	var a := battle.fighters[battle.attacker]
	var action := field(battle, "action")
	if action in [3, 4, 5, 6, 7, 8]:
		a.anim = 8  # the ready pose
	elif action in [2, 9, 10]:
		a.anim = 12  # a heal
	elif action in [11, 12, 13]:
		a.anim = 13  # a soul
	elif action == 0:
		a.anim = 2  # the run to the target
		_run_to_target(battle, a)
	battle.anim_length = int(battle.anim_lengths[a.anim])


static func _run_to_target(battle: OnlineBattle, a: OnlineFighter) -> void:
	battle.run_dx = (OnlineBattle.W - 67 - 42) / int(battle.anim_lengths[a.anim])
	battle.run_dy = 0
	if battle.mode != 0 and a.row() != field(battle, "target") / 2:
		battle.run_dy = (46 if a.row() == 0 else -46) / int(battle.anim_lengths[a.anim])


## The fighters during a record: the others first, then the one acting.
static func turn_fighters(battle: OnlineBattle) -> void:
	for i in 4:
		var f := battle.fighters[i]
		if not f.present or i == battle.attacker:
			continue
		match f.anim:
			0:
				_idle(battle, i)
			1, 4:
				var id := f.anim + (21 if f.kind == OnlineBattle.MONSTER else 0)
				f.frame = int(battle.first_frame[id])
				f.x -= 2
			5:
				f.frame = int(battle.first_frame[26 if f.kind == OnlineBattle.MONSTER else 5])
				if f.anim_tick == 0:
					f.x -= 6
					battle.sounds.append(3)
				elif f.anim_tick == 1:
					f.x -= 2
			6:
				_dying(battle, f)
			_:
				_anim(battle, f)
	var a := battle.fighters[battle.attacker]
	if a.anim == 2 or a.anim == 28:
		a.frame = int(battle.first_frame[23 if a.kind == OnlineBattle.MONSTER else 2])
		a.x += battle.run_dx
		a.y += battle.run_dy
	elif a.anim == 6:
		_dying(battle, a)
	else:
		_anim(battle, a)


static func _dying(battle: OnlineBattle, f: OnlineFighter) -> void:
	f.frame = (
		int(battle.first_frame[27 if f.kind == OnlineBattle.MONSTER else 6]) + battle.anim_frame
	)


static func _anim(battle: OnlineBattle, f: OnlineFighter) -> void:
	var id := f.anim
	if f.kind == OnlineBattle.MONSTER and id == 3:
		id = 24
	var at := battle.anim_frame
	if id == 12 and at >= 4:
		at = 4
	f.frame = int(battle.first_frame[id]) + at
	if id < battle.steps.size():
		var st: Array = battle.steps[id]
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


## The pose of a fighter standing (blinking), or lying when fallen.
static func _idle(battle: OnlineBattle, i: int) -> void:
	var f := battle.fighters[i]
	if f.hp > 0:
		if battle.state_ticks % 4 == f.blink:
			f.frame = (battle.state_ticks / 4) % 2
		if f.frame != 0 and f.frame != 1:
			f.frame = 0
	else:
		f.frame = int(battle.first_frame[6]) + 1


static func idle_all(battle: OnlineBattle) -> void:
	for i in 4:
		if battle.fighters[i].present:
			_idle(battle, i)


## The HP and MP of those in the record move to what the record says, the
## change shown over them.
static func damage(battle: OnlineBattle) -> void:
	if battle.damage_tick < 0:
		return
	for i in _involved(battle):
		var f := battle.fighters[i]
		if f.hp != f.hp_target:
			f.hp = maxi(0, f.hp + f.hp_step)
		if f.mp != f.mp_target:
			f.mp = maxi(0, f.mp + f.mp_step)
		if f.hp_delta != 0:
			var sx := (OnlineBattle.W - f.x) if f.mirrored() else f.x
			battle.damage_shown.append([sx, f.y, 40 + 2 * battle.damage_tick, f.hp_delta])
	for i in _involved(battle):
		if battle.fighters[i].hp == 0:
			battle.fighters[i].hp = 1  # still standing until the record's end
	battle.damage_tick += 1


## The fighters in the record played back: the one acting and its targets, each once.
static func _involved(battle: OnlineBattle) -> Array:
	var out: Array = []
	for i in [battle.attacker, battle.target, battle.target2]:
		if i >= 0 and battle.fighters[i].present and not out.has(i):
			out.append(i)
	return out


static func step_turn(battle: OnlineBattle) -> void:
	if battle.damage_tick >= 5:
		battle.damage_tick = -1
		for i in _involved(battle):
			battle.fighters[i].hp = battle.fighters[i].hp_target
			battle.fighters[i].mp = battle.fighters[i].mp_target
	var a := battle.fighters[battle.attacker]
	if battle.anim_frame >= battle.anim_length:
		battle.anim_frame = 0
		match a.anim:
			2, 17, 18, 19:
				_after_run_in(battle)
			8:
				_after_ready(battle)
			20:
				if field(battle, "action") == 8:
					battle.fighters[battle.attacker].anim = 16
			3, 9, 10, 11, 14, 15, 16:
				_after_strike(battle)
			12, 13, 28:
				_after_run_back(battle)
			6:
				battle.turn_rec += 1
				next_record(battle)
		if battle.state != OnlineBattle.TURN:
			return
		battle.anim_length = int(battle.anim_lengths[battle.fighters[battle.attacker].anim])
	if battle.fighters[battle.attacker].anim != 6:
		_reactions(battle)


static func _after_run_in(battle: OnlineBattle) -> void:
	var a := battle.fighters[battle.attacker]
	a.x = OnlineBattle.W - 67
	a.y = OnlineBattle.CY + 65
	if battle.mode != 0:
		a.y += (-1 if field(battle, "target") / 2 == 0 else 1) * 23
	match field(battle, "action"):
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


static func _after_ready(battle: OnlineBattle) -> void:
	var a := battle.fighters[battle.attacker]
	var action := field(battle, "action")
	if action in [3, 4, 5]:
		a.anim = 2
		_run_to_target(battle, a)
	elif action in [6, 7]:
		if battle.mode == 0 or field(battle, "target") / 2 == field(battle, "actor") / 2:
			a.anim = 17
		elif field(battle, "target") / 2 == 1:
			a.anim = 18
		else:
			a.anim = 19
	elif action == 8:
		a.anim = 20


static func _after_strike(battle: OnlineBattle) -> void:
	if (
		field(battle, "flags") == 3
		and battle.fighters[battle.attacker].slot == field(battle, "actor")
	):  # the target strikes back
		var t := battle.attacker
		battle.attacker = battle.target
		battle.target = t
		battle.fighters[battle.attacker].anim = 3
		battle.target_reaction = OnlineBattle.REACT_HIT
		return
	battle.damage_tick = 0
	if field(battle, "flags") == 3:
		var t := battle.attacker
		battle.attacker = battle.target
		battle.target = t
		battle.fighters[battle.target].anim = 0
		battle.place(battle.fighters[battle.target])
	var a := battle.fighters[battle.attacker]
	a.anim = 28  # the run back
	var length := int(battle.anim_lengths[28])
	battle.run_dx = (42 - a.x) / length
	battle.run_dy = 0
	if battle.mode != 0 and a.row() != field(battle, "target") / 2:
		battle.run_dy = (-46 if a.row() == 0 else 46) / length


static func _after_run_back(battle: OnlineBattle) -> void:
	var a := battle.fighters[battle.attacker]
	battle.place(a)
	var fallen := -1
	for i in 4:
		var f := battle.fighters[i]
		if not f.present:
			continue
		if a.anim == 13 and f.team() == a.team():  # the soul's aura on the team
			f.status = field(battle, "action")
			f.status_ticks = 3
		if f.hp == 0 and f.hp_delta != 0:
			fallen = i
			f.anim = 6
			if f.team() == battle.fighters[0].team():
				battle.allies_alive -= 1
			else:
				battle.enemies_alive -= 1
	if fallen > 0:
		if a.anim != 6:
			a.anim = 0
		battle.attacker = fallen
		return
	battle.turn_rec += 1
	next_record(battle)


## When the target flinches, dodges or falls back, and the sounds.
static func _reactions(battle: OnlineBattle) -> void:
	var a := battle.fighters[battle.attacker]
	if a.anim != 12 and a.anim != 13 and field(battle, "flags") != 3:
		for i in [battle.target, battle.target2]:
			if i >= 0 and battle.fighters[i].anim != 0:
				var f := battle.fighters[i]
				f.anim_tick += 1
				if f.anim_tick >= f.anim_len:
					f.anim = 0
					battle.place(f)
	match a.anim:
		3, 9, 10, 11, 14:
			if battle.target_reaction in [OnlineBattle.REACT_HIT, OnlineBattle.REACT_DEFENDED]:
				if a.anim == 11 and battle.anim_frame == 17:
					_start_reaction(battle)
					battle.fighters[battle.target].anim_len = 3
					return
				if battle.anim_frame % 2 != 1 or (a.anim == 11 and battle.anim_frame > 10):
					return
				_start_reaction(battle)
				battle.fighters[battle.target].anim_len = 2
			elif battle.target_reaction == OnlineBattle.REACT_EVADE:
				if field(battle, "flags") == 3:
					if battle.anim_frame != 0:
						return
					var t := battle.fighters[battle.target]
					t.anim = 5
					t.anim_tick = 0
					t.anim_len = battle.anim_length
				else:
					if battle.anim_frame % 2 != 1:
						return
					_start_reaction(battle)
					battle.fighters[battle.target].anim_len = 2
		15:
			if (
				battle.target_reaction in [OnlineBattle.REACT_HIT, OnlineBattle.REACT_DEFENDED]
				and battle.anim_frame == 2
			):
				_start_reaction(battle)
				battle.fighters[battle.target].anim_len = 4
		16:
			if (
				battle.target_reaction in [OnlineBattle.REACT_HIT, OnlineBattle.REACT_DEFENDED]
				and battle.anim_frame == 8
			):
				_start_reaction(battle)
				battle.fighters[battle.target].anim_len = 3
				if battle.target2 != -1:
					var t2 := battle.fighters[battle.target2]
					t2.anim = battle.target2_reaction
					t2.anim_tick = 0
					t2.anim_len = 3
		12:
			if battle.anim_frame == 4:
				battle.damage_tick = 0
				battle.sounds.append(6)
		13:
			if (battle.anim_frame == 4 and field(battle, "action") == 13) or battle.anim_frame == 7:
				battle.sounds.append(5)
			elif battle.anim_frame == 5:
				battle.damage_tick = 0


static func _start_reaction(battle: OnlineBattle) -> void:
	var t := battle.fighters[battle.target]
	t.anim = battle.target_reaction
	t.anim_tick = 0
	var a := battle.fighters[battle.attacker]
	battle.sounds.append(2 if a.anim == 16 or a.anim == 15 else 0)
