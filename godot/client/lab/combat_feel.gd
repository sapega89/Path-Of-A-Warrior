extends RefCounted
## How a hit feels, for the combat feel lab (lab/combat_feel_lab.gd): the hitstop, the camera
## shake, the white flash, the recoil of the one hit, the flight of the one killed and the hit
## sound's pitch. It only watches the map simulation: hits() compares the HP before and after a
## tick, react() turns this tick's hits into what the screen shows, advance() lets it fade.
## The simulation, its positions and its ticks are never changed. Every effect can be switched
## off (`on`) and every number tuned (`p`), both from the lab's panel.

## The effects, each on or off.
var on := {
	"hitstop": true, "shake": true, "flash": true, "recoil": true, "knock_ease": true,
	"launch": true, "sound": true,
}
## The numbers: times in seconds, distances in the original's pixels (27 to a tile).
var p := {
	# hitstop: how long the picture stands still
	"stop_hit": 0.04, "stop_heavy": 0.07, "stop_kill": 0.09, "stop_boss": 0.16,
	"stop_hurt": 0.06, "stop_object": 0.03,
	"stop_budget": 0.2, "stop_window": 0.5,  # at most this much in any such window
	"stop_scale": 1.0,
	# shake: trauma 0..1 added by a hit; the offset is trauma² × shake_px
	"trauma_hit": 0.25, "trauma_heavy": 0.4, "trauma_kill": 0.5, "trauma_boss": 0.8,
	"trauma_hurt": 0.45, "trauma_object": 0.2,
	"shake_px": 10.0, "shake_roll": 0.8, "shake_decay": 2.5, "shake_freq": 25.0,
	"shake_kick_px": 2.0, "shake_scale": 1.0,
	# flash: how long the one hit shows white
	"flash_hit": 0.06, "flash_heavy": 0.08, "flash_kill": 0.10, "flash_boss": 0.2,
	"flash_hurt": 0.12, "flash_object": 0.06,
	# recoil of the one hit, and the flight of the one killed
	"recoil_px": 3.0, "recoil_heavy_px": 6.0, "recoil_time": 0.12,
	"launch_px": 24.0, "launch_boss_px": 32.0, "launch_hop_px": 8.0, "launch_time": 0.25,
	# sound
	"pitch_spread": 0.07, "kill_pitch": 0.8, "kill_delay": 0.03, "heavy_db": 2.0,
}

const WHITE := Color(1.0, 1.0, 1.0)
const HURT := Color(1.0, 0.35, 0.3)  # the hero's flash when he is hit

## The picture stands still while this is above 0 (seconds of real time).
var freeze := 0.0
var trauma := 0.0
## actor (a sim Actor or Breakable) -> {t, total, color}
var flashes := {}
## actor -> {t, total, dir: Vector2, px}
var recoils := {}
## actor -> {t, total, dir: Vector2, px, hop}
var launches := {}

var _budget := 0.2
var _time := 0.0
var _kick := Vector2.ZERO  # the first jolt of a strong hit, along the blow
var _noise := FastNoiseLite.new()


func _init() -> void:
	_noise.noise_type = FastNoiseLite.TYPE_SIMPLEX
	_noise.frequency = 1.0
	_noise.seed = 7
	_budget = float(p.stop_budget)


## What the hits are judged by: the HP of everyone (and of the breakable objects) now.
static func snapshot(sim: RefCounted) -> Dictionary:
	var hp := {}
	hp[sim.hero] = sim.hero.hp
	for e in sim.enemies:
		hp[e] = e.hp
	for b in sim.breakables:
		hp[b] = b.hp
	return hp


## This tick's hits: whoever has less HP than in `before` (snapshot()). Each one:
## {who: "enemy" | "hero" | "object", actor, pos (map px), dir (away from the blow, unit),
## killed, heavy (a combo's third strike or a skill: he is knocked back; the hero: a general's
## skill that pushes him), boss (a general)}.
static func hits(sim: RefCounted, before: Dictionary) -> Array:
	var out: Array = []
	var hero = sim.hero
	for e in sim.enemies:
		if not before.has(e) or e.hp >= int(before[e]):
			continue
		out.append({"who": "enemy", "actor": e, "pos": e.pos, "dir": _away(hero.pos, e.pos, e.facing),
			"killed": e.hp <= 0, "heavy": e.ai_mode > 0 or hero.action >= 12, "boss": e.type < 200})
	if before.has(hero) and hero.hp < int(before[hero]):
		var back: int = (hero.facing + 4) & 7
		out.append({"who": "hero", "actor": hero, "pos": hero.pos, "dir": _dir8_vec(back),
			"killed": hero.hp <= 0, "heavy": hero.hurt_ticks > 0, "boss": false})
	for b in sim.breakables:
		if before.has(b) and b.hp < int(before[b]):
			out.append({"who": "object", "actor": b, "pos": b.pos, "dir": _away(hero.pos, b.pos, 0),
				"killed": b.hp < 1, "heavy": false, "boss": false})
	return out


static func _away(from: Vector2i, to: Vector2i, facing: int) -> Vector2:
	var d := Vector2(to - from)
	if d.length() < 1.0:
		return _dir8_vec((facing + 4) & 7)
	return d.normalized()


## The original 8-direction (0 down, 2 left, 4 up, 6 right) as a unit vector on the map.
static func _dir8_vec(d8: int) -> Vector2:
	var a := float(d8) * PI / 4.0
	return Vector2(-sin(a), cos(a))


## The strength of a hit, for the tables of `p`: "kill" outranks "heavy" outranks "hit".
static func grade(h: Dictionary) -> String:
	if h.who == "hero":
		return "hurt"
	if h.who == "object":
		return "object"
	if h.killed:
		return "boss" if h.boss else "kill"
	return "heavy" if h.heavy else "hit"


## This tick's hits start their effects. The strongest hit sets the hitstop and the shake (a
## skill hitting five does not stop or shake five times as much); each one hit flashes.
func react(list: Array) -> void:
	var stop := 0.0
	var shake := 0.0
	var kick := Vector2.ZERO
	var seen := {}
	for h in list:
		var g := grade(h)
		if float(p["stop_" + g]) > stop:
			stop = float(p["stop_" + g])
		if float(p["trauma_" + g]) > shake:
			shake = float(p["trauma_" + g])
			kick = h.dir if g != "hit" and g != "object" else Vector2.ZERO
		var a = h.actor
		if seen.has(a):
			continue  # hit twice in a tick: one effect
		seen[a] = true
		if on.flash:
			var t := float(p["flash_" + g])
			flashes[a] = {"t": t, "total": t, "color": HURT if g == "hurt" else WHITE}
		if h.who != "enemy":
			continue
		if on.launch and h.killed:
			var t := float(p.launch_time)
			launches[a] = {"t": 0.0, "total": t, "dir": h.dir,
				"px": float(p.launch_boss_px if h.boss else p.launch_px), "hop": float(p.launch_hop_px)}
			recoils.erase(a)
		elif on.recoil:
			var t := float(p.recoil_time)
			recoils[a] = {"t": 0.0, "total": t, "dir": h.dir,
				"px": float(p.recoil_heavy_px if h.heavy else p.recoil_px)}
	if on.hitstop and stop > 0.0:
		var want := stop * float(p.stop_scale)
		var got := minf(want, _budget)
		_budget -= got
		freeze = maxf(freeze, got)
	if on.shake and shake > 0.0:
		trauma = minf(1.0, trauma + shake)
		_kick = kick * float(p.shake_kick_px)


## Real time goes on: the shake and the flashes fade even while the picture stands still; the
## recoil and the flight move only with the world (frozen: they wait).
func advance(delta: float) -> void:
	_time += delta
	var window := maxf(float(p.stop_window), 0.01)
	_budget = minf(float(p.stop_budget), _budget + delta * float(p.stop_budget) / window)
	var frozen := freeze > 0.0
	freeze = maxf(0.0, freeze - delta)
	trauma = maxf(0.0, trauma - float(p.shake_decay) * delta)
	_kick = _kick.lerp(Vector2.ZERO, minf(1.0, delta * 20.0))
	for a in flashes.keys():
		flashes[a].t -= delta
		if flashes[a].t <= 0.0:
			flashes.erase(a)
	if frozen:
		return
	for a in recoils.keys():
		recoils[a].t += delta
		if recoils[a].t >= recoils[a].total:
			recoils.erase(a)
	for a in launches.keys():
		launches[a].t = minf(launches[a].t + delta, launches[a].total)  # stays where it landed


## How white the actor shows (0..1) and in which colour.
func flash_of(actor) -> Array:
	if not flashes.has(actor):
		return [0.0, WHITE]
	var f: Dictionary = flashes[actor]
	return [clampf(f.t / maxf(f.total, 0.001), 0.0, 1.0), f.color]


## Where the actor is drawn off its place, in map pixels: x, y on the floor, z up (the hop).
func offset_of(actor) -> Vector3:
	var out := Vector3.ZERO
	if recoils.has(actor):
		var r: Dictionary = recoils[actor]
		var k := clampf(r.t / maxf(r.total, 0.001), 0.0, 1.0)
		# out fast, back slower
		var s := sin(PI * pow(k, 0.6))
		out += Vector3(r.dir.x, r.dir.y, 0.0) * r.px * s
	if launches.has(actor):
		var l: Dictionary = launches[actor]
		var k := clampf(l.t / maxf(l.total, 0.001), 0.0, 1.0)
		var flown := 1.0 - pow(1.0 - k, 3.0)
		out += Vector3(l.dir.x * l.px * flown, l.dir.y * l.px * flown, l.hop * sin(PI * k))
	return out


## The camera's offset now: [x px, y px, roll in degrees].
func camera_shake() -> Vector3:
	if trauma <= 0.0 and _kick.length() < 0.01:
		return Vector3.ZERO
	var s := trauma * trauma * float(p.shake_scale)
	var t := _time * float(p.shake_freq)
	var x := _noise.get_noise_2d(t, 0.0) * float(p.shake_px) * s + _kick.x * float(p.shake_scale)
	var y := _noise.get_noise_2d(0.0, t + 100.0) * float(p.shake_px) * s + _kick.y * float(p.shake_scale)
	var roll := _noise.get_noise_2d(t + 200.0, t) * float(p.shake_roll) * s
	return Vector3(x, y, roll)


## The pitch of a hit sound: a little higher or lower each time.
func pitch(rng: RandomNumberGenerator) -> float:
	var s := float(p.pitch_spread)
	return 1.0 + rng.randf_range(-s, s)


## Forgets the effects of actors gone from the map (no longer in `alive`).
func forget_except(alive: Dictionary) -> void:
	for d in [flashes, recoils, launches]:
		for a in d.keys():
			if not alive.has(a):
				d.erase(a)
