extends RefCounted
## A battle of the online game on the server (pyport pow_server/battle.py): Duel 1-on-1 and
## 2-on-2, Solo Mission. The client only shows what the server decides: it sends one choice a
## round {target, action, hit %} and plays the records back. The numbers are the single
## player's where it has them (server/rules.gd: hero stats, soldiers, damage ATK - DEF, skills,
## heals, souls, rewards); the rest (the timing bar, Defend / Evade, the MP gauge, grades, the
## CPU) is pyport's.
##
## Slots: slot % 2 is the team (0 left, 1 right), slot / 2 the row; 1-on-1 uses 0 and 1.
## Actions: 0 Attack, 1 Defend, 2 Evade, 3..13 skills. Defend and Evade are stances: they never
## make a record of their own.

const Rules := preload("res://server/rules.gd")

const ATTACK := 0
const DEFEND := 1
const EVADE := 2
const AUTO := 255  # a choice with this action lets the bot choose
const WIND := 3
const STORM := 4
const THUNDER := 5
const TIDE := 6
const WAVE := 7
const TIDAL := 8
const HEAL_MED := 9
const HEAL_MAX := 10
const SOUL_DEVIL := 11
const SOUL_GUARD := 12
const SOUL_ARCH := 13
const ENEMY_SKILLS := [WIND, STORM, THUNDER, TIDE, WAVE, TIDAL]
const HEALS := [HEAL_MED, HEAL_MAX]
const SOULS := [SOUL_DEVIL, SOUL_GUARD, SOUL_ARCH]

const RES_HIT := 1
const RES_EVADED := 2
const MP_MAX := 100
const MP_ATTACK := 20  # an Attack fills the gauge this much
const MP_HIT := 10  # a hit taken
const MP_STANCE := 15  # a round of Defend / Evade
const EVADE_CHANCE := 0.45
const DEFEND_FACTOR := 0.4
const SKILL_HIT := 70  # skills skip the timing bar
## Attack is the single player's 3-hit combo; where the timing bar stops decides how many land
const COMBO_HITS := [[88, 3], [52, 2], [0, 1]]

const CPU_NAMES := ["Garrick", "Selene", "Borin", "Kaida", "Ulric", "Mirena", "Dorn", "Ysolde",
	"Thane", "Rowan", "Brakka", "Liora"]
const CPU_QUOTES := [["En garde!", "Too slow."], ["Face me!", "As expected."],
	["Show me your blade", "Train harder."], ["Here I come!", "Victory is mine!"]]
## where a CPU fighter's points go when the hero it copies has none
const BUILDS := [{"atk": 2, "def": 1, "hp": 2}, {"atk": 3, "def": 1, "hp": 1},
	{"atk": 1, "def": 2, "hp": 2}, {"atk": 2, "def": 2, "hp": 1}]

## the bot: where it stops the timing bar, heals a battle at most, heals when HP lasts this many
## rounds or less
const BAR_CHOICES := [40, 52, 64, 76, 76, 88, 88, 100]
const HEAL_LIMIT := 3
const HEAL_ROUNDS := 2

const GRADE_TOP := 9  # D+ .. A+
const MISSION_TITLES := ["Dark Forest", "Old Ruins", "Bandit Pass", "Cursed Swamp", "Iron Keep",
	"Bone Valley", "Frozen Gate", "Lost Temple"]
const MONSTER_NAMES := ["Goblin", "Ghoul", "Orc", "Troll", "Imp", "Wraith", "Ogre", "Lizard"]
const SOLDIER_KINDS := [0, 0, 1, 2]  # swordsmen more often than archers and squads


class Fighter:
	var slot := 0
	var name := ""
	var level := 1
	var max_hp := 1
	var atk := 0
	var def := 0
	var skills := {}  # skill -> level
	var slots: Array = []  # the skills it can use
	var face := 0
	var weapon := 0  # 0 long, 1 short
	var cpu := false
	var monster := false  # attacks only
	var wins := 0
	var losses := 0
	var quote_start := ""
	var quote_win := ""
	var hp := 0
	var mp := 0
	var stance := ATTACK
	var buffs := {}  # "atk" / "def" -> [bonus, rounds]
	var general := false  # worth 2 L when beaten, a soldier L
	var build := {}  # where the hero's stat points went (CPU fighters copy it)
	var max_mp := 10  # the hero's MP in the single player (skill costs)
	var keep_name := false  # a server bot: its own name
	var auto := false  # auto-battle: the bot chooses for this player
	var last_action := ATTACK  # the bot does not take a stance twice in a row
	var heals := 0  # heals cast in this battle

	func team() -> int:
		return slot % 2

	func alive() -> bool:
		return hp > 0

	func bonus(stat: String) -> int:
		var b: Array = buffs.get(stat, [])
		return int(b[0]) if not b.is_empty() else 0

	## Gauge cost of a skill: its single-player MP share of this hero's MP.
	func cost(skill: int) -> int:
		return Rules.skill_cost(skill, int(skills.get(skill, 1)), max_mp)

	func can_use(skill: int) -> bool:
		return slots.has(skill) and skills.has(skill) and mp >= cost(skill)

	## What the clients are told of a fighter.
	func wire() -> Dictionary:
		return {"slot": slot, "name": name.left(8), "level": level, "wins": wins, "losses": losses,
			"hp": max_hp, "weapon": weapon, "face": face, "cpu": cpu, "monster": monster,
			"quote_start": quote_start, "quote_win": quote_win}


# --- helpers --------------------------------------------------------------------------------
static func _pick(rng: RandomNumberGenerator, a: Array) -> Variant:
	return a[rng.randi_range(0, a.size() - 1)]


## The first item with the smallest key (numbers or arrays of them).
static func _min_by(items: Array, key: Callable) -> Variant:
	var best: Variant = null
	var best_key: Variant = null
	for x in items:
		var k: Variant = key.call(x)
		if best == null or k < best_key:
			best = x
			best_key = k
	return best


static func _max_by(items: Array, key: Callable) -> Variant:
	var best: Variant = null
	var best_key: Variant = null
	for x in items:
		var k: Variant = key.call(x)
		if best == null or k > best_key:
			best = x
			best_key = k
	return best


static func _sum(values: Array) -> int:
	var n := 0
	for v in values:
		n += int(v)
	return n


# --- fighters -------------------------------------------------------------------------------
## A player's fighter from his character (server/online.gd character()).
static func from_character(c: Dictionary, slot: int) -> Fighter:
	var f := Fighter.new()
	f.slot = slot
	f.name = str(c.name) if not str(c.name).is_empty() else str(c.id).left(8)
	f.level = int(c.level)
	f.max_hp = int(c.hp) + int(c.hp_bonus)
	f.hp = f.max_hp
	f.atk = int(c.atk) + int(c.atk_bonus)
	f.def = int(c.def) + int(c.def_bonus)
	f.skills = (c.skills as Dictionary).duplicate()
	f.slots = (c.slots as Array).filter(func(s): return f.skills.has(int(s))).map(func(s): return int(s))
	f.face = int(c.face)
	f.weapon = int(c.weapon)
	f.wins = int(c.wins)
	f.losses = int(c.losses)
	f.quote_start = str(c.quote_start)
	f.quote_win = str(c.quote_win)
	f.build = hero_build(c)
	f.general = true  # a hero beaten counts like a general
	f.max_mp = int(c.mp) + int(c.mp_bonus)
	return f


## The stat points of a hero: its base stats over a new hero's of its face, per point gain.
static func hero_build(c: Dictionary) -> Dictionary:
	var b := Rules.hero_base(int(c.face))
	return {"atk": maxi(0, int(c.atk) - int(b.atk)), "def": maxi(0, int(c.def) - int(b.def)),
		"hp": maxi(0, (int(c.hp) - int(b.hp)) / int(Rules.POINT_GAIN.hp)),
		"mp": maxi(0, (int(c.mp) - int(b.mp)) / int(Rules.POINT_GAIN.mp))}


## A CPU fighter: a single-player hero of about my level, its points spent like mine, my
## skills, in the shop's gear of its level.
static func cpu_fighter(rng: RandomNumberGenerator, me: Fighter, slot: int, ally := false) -> Fighter:
	var f := Fighter.new()
	f.slot = slot
	f.level = maxi(1, me.level + rng.randi_range(-2, 1) - (1 if ally else 0))
	# the points go about where mine went: with damage ATK - DEF (at least 1) a random build can
	# out-DEF the other side's ATK and the duel never ends
	var build: Dictionary = me.build.duplicate() if _sum(me.build.values()) > 0 else (_pick(rng, BUILDS) as Dictionary).duplicate()
	var stat: String = _pick(rng, ["atk", "def", "hp"])
	build[stat] = int(build.get(stat, 0)) + maxi(1, _sum(build.values()) / 10)
	f.skills = me.skills.duplicate() if not me.skills.is_empty() else {WIND: 1, SOUL_DEVIL: 1}
	f.slots = me.slots.filter(func(s): return f.skills.has(s))
	if f.slots.is_empty():
		f.slots = f.skills.keys().slice(0, 4)
	var q: Array = _pick(rng, CPU_QUOTES)
	var kit := Rules.shop_kit(f.level)
	f.name = _pick(rng, CPU_NAMES)
	f.face = rng.randi_range(0, 3)
	var st := Rules.hero_stats(f.level, build, f.face)
	f.max_hp = int(st.hp) + int(kit.hp)
	f.hp = f.max_hp
	f.atk = int(st.atk) + int(kit.atk)
	f.def = int(st.def) + int(kit.def)
	f.weapon = rng.randi_range(0, 1)
	f.cpu = true
	f.wins = rng.randi_range(0, 5 * f.level)
	f.losses = rng.randi_range(0, 5 * f.level)
	f.quote_start = q[0]
	f.quote_win = q[1]
	f.general = true
	f.build = build
	f.max_mp = int(st.mp)
	return f


## A mission's monster: a single-player soldier of about my level.
static func monster(rng: RandomNumberGenerator, me: Fighter, slot: int) -> Fighter:
	var f := Fighter.new()
	f.slot = slot
	f.name = _pick(rng, MONSTER_NAMES)
	f.level = Rules.soldier_level(rng, me.level)
	var st := Rules.soldier_stats(_pick(rng, SOLDIER_KINDS), f.level)
	f.max_hp = int(st.hp)
	f.hp = f.max_hp
	f.atk = int(st.atk)
	f.def = int(st.def)
	f.cpu = true
	f.monster = true
	return f


## Stages of a Solo Mission: 2, and more with the single player's progress, up to 6.
static func mission_stages(progress: int) -> int:
	return 2 + mini(4, progress / 6)


## The foes of a stage at slots 1 and 3: soldiers; the last stage has a CPU fighter, the boss.
static func mission_wave(rng: RandomNumberGenerator, me: Fighter, stage: int, stages: int) -> Array:
	var foes: Array = [monster(rng, me, 1), monster(rng, me, 3)]
	if stage == stages:
		foes[0] = cpu_fighter(rng, me, 1)
	return foes


## h of the mission's gold (3..15) for 2..6 stages.
static func mission_gold_rate(stages: int) -> int:
	return 3 * (stages - 1)


## The battle's background: bits 4-5 the ground 0..3, 0-1 the foreground 0..3 (always day).
static func battle_background(rng: RandomNumberGenerator) -> int:
	return (rng.randi_range(0, 3) << 4) | rng.randi_range(0, 3)


# --- the bot --------------------------------------------------------------------------------
# One choice a round for a CPU fighter, and for a player on auto-battle. It looks one round
# ahead on the same numbers as the strike: finish a foe off with the cheapest action that kills,
# Defend or Evade when the hits coming are lethal, heal when HP is below them, else the action
# with the most damage, a skill only when it beats Attack by enough for its MP.

## The damage `action` of f would do to t (no Evade roll).
static func strike_damage(f: Fighter, t: Fighter, action: int, hit := 100, defended := false) -> int:
	var one := f.atk + f.bonus("atk") - t.def - t.bonus("def")
	var hits := 1
	if action == ATTACK:
		for c in COMBO_HITS:
			if hit >= c[0]:
				hits = c[1]
				break
	else:
		one += Rules.skill_bonus(action, f.atk, int(f.skills.get(action, 1)))
		hits = Rules.SKILL_HITS[action]
	var dmg := maxi(1, one) * hits
	return maxi(1, int(dmg * DEFEND_FACTOR)) if defended else dmg


## [action, hit %, MP cost] of everything f can strike with this round.
static func attack_options(f: Fighter, hit := 100) -> Array:
	var opts: Array = [[ATTACK, hit, 0]]
	for s in f.slots:
		if s in ENEMY_SKILLS and f.can_use(s):
			opts.append([s, SKILL_HIT, f.cost(s)])
	return opts


## The most damage foe g can do to me this round (a full combo or its best skill).
static func threat(g: Fighter, me: Fighter) -> int:
	var most := 0
	for o in attack_options(g):
		most = maxi(most, strike_damage(g, me, o[0], o[1]))
	return most


static func _acts_before(me: Fighter, g: Fighter) -> bool:
	return me.mp > g.mp


## [target slot, heal, 0] for the ally (or me) in the most need, or [].
static func _heal_choice(me: Fighter, allies: Array, incoming: Dictionary) -> Array:
	var heals: Array = HEALS.filter(func(s): return me.can_use(s))
	if heals.is_empty() or me.heals >= HEAL_LIMIT:
		return []
	var team: Array = [me]
	for a in allies:
		if a.alive() and a != me:
			team.append(a)
	var order: Array = []  # the lowest share of HP first, in team order on a tie
	for i in team.size():
		order.append([float(team[i].hp) / team[i].max_hp, i])
	order.sort()
	for o in order:
		var t: Fighter = team[o[1]]
		var coming := int(incoming.get(t.slot, 0))
		# a heal against small hits only drags the fight out (MP comes back faster than HP goes)
		if t.hp > HEAL_ROUNDS * coming or t.hp >= t.max_hp:
			continue
		# the smallest heal that lifts t out of reach, else the biggest one
		var gain := {}
		for s in heals:
			gain[s] = Rules.heal(s, t.max_hp, int(me.skills.get(s, 1)))
		var enough: Array = heals.filter(func(s): return t.hp + int(gain[s]) > coming)
		var heal: int = _min_by(enough, func(s): return me.cost(s)) if not enough.is_empty() \
			else _max_by(heals, func(s): return gain[s])
		return [t.slot, heal, 0]
	return []


## My hits take the foes down in fewer rounds than theirs take me: a heal would only drag the
## fight out (two bots that both heal it out never end).
static func _winning_race(me: Fighter, foes: Array, opts: Array) -> bool:
	var hit := 100
	for o in opts:
		if o[0] == ATTACK:
			hit = o[1]
			break
	var mine := 0.0
	var coming := 0
	for g in foes:
		mine += float(g.hp) / maxi(1, strike_damage(me, g, ATTACK, hit))
		coming += threat(g, me)
	return mine < float(me.hp) / maxi(1, coming)


## [target slot, action, hit %] for a CPU fighter or a player on auto-battle.
static func cpu_choice(rng: RandomNumberGenerator, me: Fighter, all_foes: Array, allies: Array = []) -> Array:
	var foes: Array = all_foes.filter(func(g): return g.alive())
	if foes.is_empty():
		return [me.slot, DEFEND, 0]
	var hit: int = _pick(rng, BAR_CHOICES)
	var incoming := {me.slot: _sum(foes.map(func(g): return threat(g, me)))}
	for a in allies:
		if a.alive() and a != me:
			incoming[a.slot] = _sum(foes.map(func(g): return threat(g, a)))
	var lethal: bool = me.hp <= int(incoming[me.slot])
	# do I act before every foe (higher MP first, a tie is a coin flip)
	var first: bool = foes.all(func(g): return _acts_before(me, g)) or (
		not foes.any(func(g): return _acts_before(g, me)) and rng.randf() < 0.5)
	var opts := attack_options(me, hit)

	# 1. finish a foe off with the cheapest action that kills (the most dangerous foe first);
	#    pointless when its hits land first and kill me
	if first or not lethal:
		var kills: Array = []
		for g in foes:
			for o in opts:
				if strike_damage(me, g, o[0], o[1]) >= g.hp:
					kills.append([o[2], -threat(g, me), g.slot, o[0], o[1]])
		if not kills.is_empty():
			var k: Array = _min_by(kills, func(x): return x)
			return [k[2], k[3], k[4]]

	# 2. heal when HP is below the damage of the next rounds; against a lethal round it helps
	#    only if I act first
	var heal := _heal_choice(me, allies, incoming)
	if not heal.is_empty() and (first or not lethal or heal[0] != me.slot) \
			and not _winning_race(me, foes, opts):
		return heal

	# 3. a lethal round: Defend if it saves me, else Evade (45 %; Thunder ignores it). Not twice
	#    in a row, so that two bots cannot hide behind their stances forever
	var weakest: Fighter = _min_by(foes, func(g): return g.hp)
	if lethal and not me.last_action in [DEFEND, EVADE]:
		var defended := _sum(foes.map(func(g): return maxi(1, int(threat(g, me) * DEFEND_FACTOR))))
		var thunder: bool = foes.any(func(g): return g.can_use(THUNDER))
		return [weakest.slot, DEFEND if me.hp > defended or thunder else EVADE, hit]

	# 4. a soul when no aura is up and it is worth more than the Attack it costs: its bonus on
	#    every hit of the rounds it lasts (the cast round is one of them)
	if not lethal and not (me.buffs.has("atk") or me.buffs.has("def")):
		var base := strike_damage(me, weakest, ATTACK, hit)
		var fight := minf(float(_sum(foes.map(func(g): return g.hp))) / maxi(1, base), 99.0)
		var best_soul := -1
		var best_value := float(base)
		for s in SOULS:
			if not me.can_use(s):
				continue
			var sd := Rules.soul(s, me.atk, me.def, int(me.skills.get(s, 1)))
			var rounds := minf(float(int(sd[2]) / 50), fight - 1.0)
			var value := rounds * (int(sd[0]) * 3 + int(sd[1]) * 3 * foes.size())
			if value > best_value:
				best_soul = s
				best_value = value
		if best_soul >= 0:
			return [me.slot, best_soul, 0]

	# 5. damage on the foe that falls soonest (the most dangerous on a tie). A skill only when it
	#    beats Attack this round, the one with the most extra damage per MP; with HP getting low
	#    it leaves the MP of a heal
	var target: Fighter = _min_by(foes, func(g):
		var most := 1
		for o in opts:
			most = maxi(most, strike_damage(me, g, o[0], o[1]))
		return [float(g.hp) / most, -threat(g, me)])
	var base := strike_damage(me, target, ATTACK, hit)
	var others: Array = foes.filter(func(g): return g != target)
	var reserve := 0
	if me.hp * 100 < me.max_hp * 60:
		var costs: Array = HEALS.filter(func(s): return me.slots.has(s) and me.skills.has(s)).map(
			func(s): return me.cost(s))
		reserve = costs.min() if not costs.is_empty() else 0
	var extra := func(o: Array) -> int:
		var dmg := strike_damage(me, target, o[0], o[1])
		if o[0] == TIDAL and not others.is_empty():  # its second target takes a strike too
			dmg += strike_damage(me, others[0], o[0], o[1])
		return dmg - base
	var better: Array = opts.filter(func(o): return o[0] != ATTACK and extra.call(o) > 0 and me.mp - o[2] >= reserve)
	if better.is_empty():
		return [target.slot, ATTACK, hit]
	var best: Array = _max_by(better, func(o): return [float(extra.call(o)) / o[2], extra.call(o)])
	return [target.slot, best[0], best[1]]


# --- the battle -----------------------------------------------------------------------------
## One battle: the fighters, the round, who has been beaten.
var rng: RandomNumberGenerator
var mode := 0
var fighters := {}  # slot -> Fighter
var round_no := 0  # rounds played
var bg := 0
var beaten: Array = []  # fighters knocked out, in order (rewards)

## Battle.new(rng, fighters, mode): mode 0 Duel 1-on-1, 1 Duel 2-on-2, 2 Solo Mission.
func _init(random: RandomNumberGenerator, list: Array, battle_mode := 0) -> void:
	rng = random
	mode = battle_mode
	for f in list:
		fighters[f.slot] = f
	bg = battle_background(rng)

func team_alive(team: int) -> bool:
	for f in fighters.values():
		if f.alive() and f.team() == team:
			return true
	return false

func over() -> bool:
	return not (team_alive(0) and team_alive(1))

## The team still standing, or -1 while both stand or none does.
func winner() -> int:
	var a := team_alive(0)
	var b := team_alive(1)
	return 0 if a and not b else (1 if b and not a else -1)

func foes(f: Fighter) -> Array:
	return fighters.values().filter(func(g): return g.alive() and g.team() != f.team())

func allies(f: Fighter) -> Array:
	return fighters.values().filter(func(g): return g.alive() and g.team() == f.team())

## Mission: the next stage's foes replace team 1; my team keeps its MP and buffs and gets
## back `rest` of its max HP (the living ones).
func new_wave(new_foes: Array, rest := 0.35) -> void:
	var mine := {}
	for s in fighters:
		if fighters[s].team() == 0:
			mine[s] = fighters[s]
	fighters = mine
	for f in fighters.values():
		if f.alive():
			f.hp = mini(f.max_hp, f.hp + int(f.max_hp * rest))
	for f in new_foes:
		fighters[f.slot] = f

## The CPU fighters play the rest (the players have no one left to choose).
func finish(max_rounds := 60) -> void:
	while not over() and max_rounds > 0:
		resolve({})
		max_rounds -= 1

## One round. choices: slot -> [target, action, hit %] of the players; the CPU, a fighter on
## auto-battle and a choice with action AUTO go to the bot. Returns {actions, records}.
func resolve(choices: Dictionary) -> Dictionary:
	round_no += 1
	var plan := {}
	for f in fighters.values():
		if not f.alive():
			continue
		var choice: Array = [] if f.cpu or f.auto else choices.get(f.slot, [f.slot, DEFEND, 20])
		if choice.is_empty() or choice[1] == AUTO:
			choice = cpu_choice(rng, f, foes(f), allies(f))
		plan[f.slot] = _validate(f, choice)
	for slot in plan:
		fighters[slot].stance = plan[slot][1]
		fighters[slot].last_action = plan[slot][1]
	var actions: Array = []
	for s in 4:
		actions.append(plan[s][1] if plan.has(s) else 0)
	# higher MP acts first; ties are random
	var order: Array = []
	for slot in plan:
		order.append([-fighters[slot].mp, rng.randf(), slot])
	order.sort()
	var records: Array = []
	for o in order:
		var f: Fighter = fighters[o[2]]
		var p: Array = plan[o[2]]
		if not f.alive() or over():
			continue
		if p[1] == DEFEND or p[1] == EVADE:
			f.mp = mini(MP_MAX, f.mp + MP_STANCE)
			continue
		var rec := _act(f, p[0], p[1], p[2])
		if not rec.is_empty():
			records.append(rec)
	for f in fighters.values():
		var left := {}
		for k in f.buffs:
			f.buffs[k][1] -= 1
			if f.buffs[k][1] > 0:
				left[k] = f.buffs[k]
		f.buffs = left
		f.stance = ATTACK
	return {"actions": actions, "records": records}

func _validate(f: Fighter, choice: Array) -> Array:
	var target: int = choice[0]
	var action: int = choice[1]
	var hit := clampi(choice[2], 0, 100)
	if action == DEFEND or action == EVADE or action == ATTACK:
		return [target, action, hit]
	if action < WIND or action > SOUL_ARCH or not f.can_use(action):
		return [target, ATTACK, 20]  # not learned, not in a slot or not enough MP
	return [target, action, SKILL_HIT]

func _target(f: Fighter, target: int, action: int) -> Fighter:
	var t: Fighter = fighters.get(target)
	if action in HEALS:
		return t if t != null and t.alive() and t.team() == f.team() else f
	if action in SOULS:
		return f
	if t != null and t.alive() and t.team() != f.team():
		return t
	return _min_by(foes(f), func(g): return g.hp)

func _act(f: Fighter, target: int, action: int, hit: int) -> Dictionary:
	var t := _target(f, target, action)
	if t == null:
		return {}
	var rec := {"actor": f.slot, "action": action, "target": t.slot, "result": RES_HIT,
		"has2nd": 0, "flags": 0}
	if action >= WIND:
		f.mp -= f.cost(action)
	if action in HEALS:
		f.heals += 1
		t.hp = mini(t.max_hp, t.hp + Rules.heal(action, t.max_hp, int(f.skills.get(action, 1))))
		if action == HEAL_MAX:
			f.mp = mini(MP_MAX, f.mp + 20)
	elif action in SOULS:
		var sd := Rules.soul(action, f.atk, f.def, int(f.skills.get(action, 1)))
		var turns: int = int(sd[2]) / 50 + 1  # 50 ticks are about a round
		for ally in fighters.values():  # the aura covers the team
			if ally.alive() and ally.team() == f.team():
				if int(sd[0]) > 0:
					ally.buffs["atk"] = [int(sd[0]), turns]
				if int(sd[1]) > 0:
					ally.buffs["def"] = [int(sd[1]), turns]
	else:
		rec.result = _strike(f, t, action, hit)
		f.mp = mini(MP_MAX, f.mp + (MP_ATTACK if action == ATTACK else 0))
		if action == TIDAL:
			var others: Array = foes(f).filter(func(g): return g != t)
			if not others.is_empty():
				var t2: Fighter = others[0]
				rec.result2 = _strike(f, t2, action, hit)
				rec.has2nd = 1
				rec.target2 = t2.slot
				rec.target2_hp = t2.hp
				rec.target2_mp = t2.mp
	rec.actor_hp = f.hp
	rec.actor_mp = f.mp
	rec.target_hp = t.hp
	rec.target_mp = t.mp
	return rec

## One action's damage, one number for all its hits; returns the result. A hit is
## ATK + A - DEF - B, at least 1; a skill adds ATK * lvl / AU to every hit.
func _strike(f: Fighter, t: Fighter, action: int, hit: int) -> int:
	if t.stance == EVADE and action != THUNDER and rng.randf() < EVADE_CHANCE:
		return RES_EVADED
	var dmg := strike_damage(f, t, action, hit, t.stance == DEFEND)
	t.hp = maxi(0, t.hp - dmg)
	t.mp = mini(MP_MAX, t.mp + MP_HIT)
	if not t.alive():
		beaten.append(t)
	return RES_HIT


# --- rewards --------------------------------------------------------------------------------
## dY of the foes `team` beat: L for a soldier, 2 L for a general.
func _dy(team: int) -> int:
	var n := 0
	for f in beaten:
		if f.team() != team:
			n += Rules.kill_value(f.level, f.general)
	return n


## Gold, Fame and Exp earned online (the character's purse; the client pays the hero).
static func _pay(c: Dictionary, gold: int, fame: int, exp_points: int) -> void:
	c.gold = int(c.gold) + gold
	c.mp_fame = int(c.mp_fame) + fame
	c.mp_exp = int(c.mp_exp) + exp_points


## The result of the duel (1-on-1 or 2-on-2) for my_slot, on the online part of his character c:
## {win, gold, grade, fame, exp}. A fighter beaten counts as a general killed in the single
## player: Fame dY, Exp 2 dY, and a gold bag of 20 at 25 % each. A loss pays nothing.
func duel_rewards(c: Dictionary, my_slot: int) -> Dictionary:
	var me: Fighter = fighters[my_slot]
	var win := winner() == me.team()
	var gold := 0
	var fame := 0
	var exp_points := 0
	var grade := 0
	if win:
		var dy := _dy(me.team())
		fame = dy
		exp_points = 2 * dy
		for f in beaten:
			if f.team() != me.team() and rng.randf() < 0.25:
				gold += 20
		# HP left and a quick win
		grade = mini(GRADE_TOP, me.hp * 10 / me.max_hp + (2 if round_no <= 5 else 0))
		c.wins = int(c.wins) + 1
		c.duel_grade = mini(GRADE_TOP, int(c.duel_grade) + 1)
	else:
		c.losses = int(c.losses) + 1
		c.duel_grade = maxi(0, int(c.duel_grade) - 1)
	_pay(c, gold, fame, exp_points)
	return {"win": int(win), "gold": gold, "grade": grade, "fame": fame, "exp": exp_points}


## A mission's result (no wins or losses): accomplished, the single player's mission end
## (Fame dY, Exp 2 (dY + dY / 20 in time), gold h * 150); failed, nothing.
func mission_rewards(c: Dictionary, my_slot: int, cleared: int, stages: int) -> Dictionary:
	var me: Fighter = fighters[my_slot]
	if cleared != stages:
		return {"win": 0, "gold": 0, "grade": 0, "fame": 0, "exp": 0}
	var got := Rules.mission_end(_dy(me.team()), round_no <= 6 * stages, mission_gold_rate(stages))
	var grade := mini(GRADE_TOP, 3 + stages / 2 + me.hp * 4 / maxi(1, me.max_hp))
	c.mission_grade = maxi(int(c.mission_grade), grade)
	_pay(c, got[2], got[0], got[1])
	return {"win": 1, "gold": got[2], "grade": grade, "fame": got[0], "exp": got[1]}
