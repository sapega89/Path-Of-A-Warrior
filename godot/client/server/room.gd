extends RefCounted
## One battle of the online game and the players in it (pyport pow_server/server.py, Room):
## one player against the CPU, or two for a Challenge, Invite An Ally or a duel found by the
## matchmaking. The server waits for the choice of every player still fighting before it
## resolves a round, and sends the same result to all of them. A player who has fallen waits
## for battle_end while the others fight on. The client gives itself a time to choose, so only
## a dropped connection can stall a round, and then the round goes on without that player.
##
## What the players are sent (server/online.gd Session.send):
##   {t: "room", via: "match" | "invite" | "invited", bg, slot, mode, fighters: [Battle wire]}
##   {t: "stage_info", title, stages, stage}  (a mission; the client answers mp_intro_done)
##   {t: "all_ready"}                         (the battle or the stage starts)
##   {t: "round_start", bar_speed}            (after mp_ready: choose, mp_turn)
##   {t: "turn_result", actions: 4, records}  (once every player has chosen)
##   {t: "stage_end", bg}                     (a stage cleared; mp_stage_next for the next)
##   {t: "room_join", fighter}                (a foe of the next stage)
##   {t: "battle_end", win, gold, grade, fame, exp, loot, rank}

const Battle := preload("res://server/battle.gd")

var online: RefCounted  # server/online.gd: rewards, loot, the Ranking
var rng: RandomNumberGenerator
var via := ""  # what the room message says to everyone ("" by who they are)
var mode := 0
var players := {}  # slot -> the session of a player still connected
var human_slots: Array = []
var mission := {}  # {title, stages, stage} of a Solo Mission
var battle: Battle
var turns := {}  # slot -> [target, action, hit] of this round
var waiting_end: Array = []  # fallen players whose client waits for battle_end
var ready: Array = []  # players past a stage's end or its intro
var stage_bg := -1


func _init(server: RefCounted, battle_mode: int, fighters: Array, room_players: Dictionary,
		progress := 0, opening := "") -> void:
	online = server
	rng = server.rng
	via = opening
	mode = battle_mode
	players = room_players.duplicate()
	human_slots = players.keys()
	if mode == 2:
		var stages := Battle.mission_stages(progress)
		mission = {"title": Battle._pick(rng, Battle.MISSION_TITLES), "stages": stages, "stage": 1}
		fighters = fighters + Battle.mission_wave(rng, _strongest(fighters), 1, stages)
	_name_cpus(fighters)
	battle = Battle.new(rng, fighters, mode)


static func _strongest(fighters: Array) -> Battle.Fighter:
	var humans: Array = fighters.filter(func(f): return not f.cpu)
	if humans.is_empty():
		humans = fighters
	return Battle._max_by(humans, func(f): return [f.max_hp, f.atk])


## No two CPU fighters share a name, nor a player's (monsters keep theirs). `keep`: fighters
## already in the battle, whose names stay and are taken.
func _name_cpus(fighters: Array, keep: Array = []) -> void:
	var taken: Array = []
	for f in fighters:
		if not f.cpu or f.keep_name:
			taken.append(f.name)
	for f in keep:
		taken.append(f.name)
	var names: Array = Battle.CPU_NAMES.filter(func(n): return not taken.has(n))
	for i in range(names.size() - 1, 0, -1):  # shuffled
		var j := rng.randi_range(0, i)
		var x: Variant = names[i]
		names[i] = names[j]
		names[j] = x
	var k := 0
	for f in fighters:
		if f.cpu and not f.monster and not f.keep_name:
			f.name = names[k]
			k += 1


func start() -> void:
	var wires: Array = battle.fighters.values().map(func(f): return f.wire())
	for slot in players:
		var s: RefCounted = players[slot]
		s.room = self
		s.slot = slot
		var opening := via
		if opening.is_empty():
			opening = "match" if players.size() == 1 else ("invite" if slot == 0 else "invited")
		s.send.call({"t": "room", "via": opening, "bg": battle.bg, "slot": slot, "mode": mode,
			"fighters": wires})
		if not mission.is_empty():
			_stage_info(s)
		else:
			s.send.call({"t": "all_ready"})


# --- who is still playing -------------------------------------------------------------------
## Slots of the connected players whose fighter stands.
func fighting() -> Array:
	return players.keys().filter(func(slot): return battle.fighters[slot].alive())


static func _covers(have: Array, want: Array) -> bool:
	return want.all(func(x): return have.has(x))


func _stage_info(s: RefCounted) -> void:
	s.send.call({"t": "stage_info", "title": str(mission.title), "stages": mission.stages,
		"stage": mission.stage})


## Another stage follows the cleared one.
func _mission_left() -> bool:
	return not mission.is_empty() and battle.team_alive(0) and not battle.team_alive(1) \
		and int(mission.stage) < int(mission.stages)


# --- the players' messages ----------------------------------------------------------------
func intro_done(s: RefCounted) -> void:
	if mission.is_empty() or not s.slot in fighting():
		return
	if not ready.has(s.slot):
		ready.append(s.slot)
	_release_intro()


func _release_intro() -> void:
	if mission.is_empty() or ready.is_empty() or not _covers(ready, fighting()):
		return
	var now := fighting()
	var slots: Array = ready.filter(func(x): return now.has(x))
	slots.sort()
	for slot in slots:
		players[slot].send.call({"t": "all_ready"})
	ready.clear()


func stage_next(s: RefCounted) -> void:
	if not _mission_left() or not s.slot in fighting():
		return
	if not ready.has(s.slot):
		ready.append(s.slot)
	_release_stage()


## The new foes go out once every player has asked for the next stage (the client clears the
## old foes then).
func _release_stage() -> void:
	if not (_mission_left() and not ready.is_empty() and _covers(ready, fighting())):
		return
	ready.clear()
	mission.stage = int(mission.stage) + 1
	stage_bg = -1
	var mine: Array = battle.fighters.values().filter(func(f): return f.team() == 0)
	var foes := Battle.mission_wave(rng, _strongest(mine), mission.stage, mission.stages)
	_name_cpus(foes, mine)  # the clients know the names of mine: only the new ones change
	battle.new_wave(foes)
	var slots := fighting()
	slots.sort()
	for slot in slots:
		var s: RefCounted = players[slot]
		for f in foes:
			s.send.call({"t": "room_join", "fighter": f.wire()})
		_stage_info(s)


func turn(s: RefCounted, choice: Array) -> void:
	if not s.slot in fighting():
		return
	if battle.over():  # the other side hung up while I was choosing
		s.send.call({"t": "turn_result", "actions": [0, 0, 0, 0], "records": []})
		return
	turns[s.slot] = choice
	_resolve_if_ready()


func _resolve_if_ready() -> void:
	var playing := fighting()
	if turns.is_empty() or not (battle.over() or _covers(turns.keys(), playing)):
		return
	if battle.over():  # someone hung up: answer those who already chose
		var chose: Array = turns.keys()
		chose.sort()
		for slot in chose:
			players[slot].send.call({"t": "turn_result", "actions": [0, 0, 0, 0], "records": []})
		turns.clear()
		_flush_end()
		return
	var mine := {}
	for slot in turns:
		if playing.has(slot):
			mine[slot] = turns[slot]
	var result := battle.resolve(mine)
	turns.clear()
	playing.sort()
	for slot in playing:
		var msg := result.duplicate(true)
		msg.t = "turn_result"
		players[slot].send.call(msg)
	_flush_end()


func round_ready(s: RefCounted) -> void:
	var me: Battle.Fighter = battle.fighters[s.slot]
	if not battle.over() and me.alive():
		s.send.call({"t": "round_start", "bar_speed": 0})
		return
	if me.alive() and _mission_left():
		if stage_bg < 0:
			stage_bg = Battle.battle_background(rng)
			battle.bg = stage_bg
		s.send.call({"t": "stage_end", "bg": stage_bg})  # "Stage N Complete!", then mp_stage_next
		return
	if not waiting_end.has(s.slot):
		waiting_end.append(s.slot)
	_flush_end()


## battle_end to the fallen players once nobody is left to play on; the CPU fighters left
## fight it out here first.
func _flush_end() -> void:
	if waiting_end.is_empty() or not _covers(waiting_end, fighting()):
		return  # someone still plays on (a next stage too)
	battle.finish()
	var slots := waiting_end.duplicate()
	slots.sort()
	waiting_end.clear()
	for slot in slots:
		if players.has(slot):
			online.battle_end(players[slot], self)


## A player hung up or left the battle: a duel left is a loss; in a 2-on-2 or a mission the
## CPU takes the fighter over.
func leave(s: RefCounted) -> void:
	var slot: int = s.slot
	if players.get(slot) != s:
		return
	players.erase(slot)
	turns.erase(slot)
	ready.erase(slot)
	waiting_end.erase(slot)
	var f: Battle.Fighter = battle.fighters[slot]
	if mission.is_empty():
		if not battle.over():
			if not players.is_empty() and mode == 1:
				f.cpu = true  # the team plays on
			else:
				f.hp = 0
				if not battle.beaten.has(f):  # the one who stayed beat him: Fame / Exp / gold
					battle.beaten.append(f)
		online.duel_left(s, self)  # over or not, it counts (a loss when not won)
	else:
		f.cpu = true  # the ally fights on; the mission left earns nothing
	if not players.is_empty():
		_resolve_if_ready()
		_release_intro()
		_release_stage()
		_flush_end()
