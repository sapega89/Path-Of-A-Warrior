class_name CombatFeel
extends RefCounted
## How a hit feels on the map (the mission screen, and the lab lab/combat_feel_lab.gd): the
## hitstop, the camera shake, the white flash, the recoil of the one hit, the flight of the one
## killed, the hit sound's pitch and the rumble of the pad (or the phone). It only watches the
## map simulation: hits() compares the HP before and after a tick, react() turns this tick's
## hits into what the screen shows, advance() lets it fade. The simulation, its positions and
## its ticks are never changed. Every effect can be switched off (`on`, use_settings()) and
## every number tuned (`p`, the lab's panel).

## The effects, each on or off.
var on := {
	"hitstop": true,
	"shake": true,
	"flash": true,
	"recoil": true,
	"knock_ease": true,
	"launch": true,
	"sound": true,
	"rumble": true,
}
## The numbers: times in seconds, distances in the original's pixels (27 to a tile).
var p := {
	# hitstop: how long the picture stands still
	"stop_hit": 0.04,
	"stop_heavy": 0.07,
	"stop_kill": 0.09,
	"stop_boss": 0.16,
	"stop_hurt": 0.06,
	"stop_object": 0.03,
	"stop_budget": 0.2,
	"stop_window": 0.5,  # at most this much in any such window
	"stop_scale": 1.0,
	# shake: trauma 0..1 added by a hit; the offset is trauma² × shake_px
	"trauma_hit": 0.25,
	"trauma_heavy": 0.4,
	"trauma_kill": 0.5,
	"trauma_boss": 0.8,
	"trauma_hurt": 0.45,
	"trauma_object": 0.2,
	"shake_px": 10.0,
	"shake_roll": 0.8,
	"shake_decay": 2.5,
	"shake_freq": 25.0,
	"shake_kick_px": 2.0,
	"shake_scale": 1.0,
	# flash: how long the one hit shows white
	"flash_hit": 0.06,
	"flash_heavy": 0.08,
	"flash_kill": 0.10,
	"flash_boss": 0.2,
	"flash_hurt": 0.12,
	"flash_object": 0.06,
	# recoil of the one hit, and the flight of the one killed
	"recoil_px": 3.0,
	"recoil_heavy_px": 6.0,
	"recoil_time": 0.12,
	"launch_px": 24.0,
	"launch_boss_px": 32.0,
	"launch_hop_px": 8.0,
	"launch_time": 0.25,
	# sound
	"pitch_spread": 0.07,
	"kill_pitch": 0.8,
	"kill_delay": 0.03,
	"heavy_db": 2.0,
	# rumble: [weak motor, strong motor, seconds]
	"rumble_hit": [0.25, 0.0, 0.06],
	"rumble_heavy": [0.4, 0.25, 0.1],
	"rumble_kill": [0.45, 0.5, 0.12],
	"rumble_boss": [0.7, 1.0, 0.35],
	"rumble_hurt": [0.5, 0.6, 0.15],
	"rumble_object": [0.2, 0.0, 0.05],
	"rumble_scale": 1.0,
}

const HIT_SOUNDS := [3, 4, 15, 16]
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

## The rumble this tick's strongest hit asks for, [weak, strong, seconds] (empty: none);
## rumble() plays it.
var rumble_wanted: Array = []
var _budget := 0.2
var _time := 0.0
var _sound_pick := RandomNumberGenerator.new()
var _kick := Vector2.ZERO  # the first jolt of a strong hit, along the blow
var _noise := FastNoiseLite.new()


func _init() -> void:
	_noise.noise_type = FastNoiseLite.TYPE_SIMPLEX
	_noise.frequency = 1.0
	_noise.seed = 7
	_budget = float(p.stop_budget)


## What the hits are judged by: the HP of everyone (and of the breakable objects) now.
static func snapshot(sim: MapSim) -> Dictionary:
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
static func hits(sim: MapSim, before: Dictionary) -> Array:
	var out: Array = []
	var hero := sim.hero
	for e in sim.enemies:
		if not before.has(e) or e.hp >= int(before[e]):
			continue
		out.append(
			{
				"who": "enemy",
				"actor": e,
				"pos": e.pos,
				"dir": _away(hero.pos, e.pos, e.facing),
				"killed": e.hp <= 0,
				"heavy": e.ai_mode > 0 or hero.action >= 12,
				"boss": e.type < 200
			}
		)
	if before.has(hero) and hero.hp < int(before[hero]):
		var back: int = (hero.facing + 4) & 7
		out.append(
			{
				"who": "hero",
				"actor": hero,
				"pos": hero.pos,
				"dir": _dir8_vec(back),
				"killed": hero.hp <= 0,
				"heavy": hero.hurt_ticks > 0,
				"boss": false
			}
		)
	for b in sim.breakables:
		if before.has(b) and b.hp < int(before[b]):
			out.append(
				{
					"who": "object",
					"actor": b,
					"pos": b.pos,
					"dir": _away(hero.pos, b.pos, 0),
					"killed": b.hp < 1,
					"heavy": false,
					"boss": false
				}
			)
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
	rumble_wanted = []
	for h in list:
		var g := grade(h)
		var r: Array = p["rumble_" + g]
		if (
			on.rumble
			and (
				rumble_wanted.is_empty()
				or float(r[1]) + float(r[0]) > float(rumble_wanted[1]) + float(rumble_wanted[0])
			)
		):
			rumble_wanted = r
		if float(p["stop_" + g]) > stop:
			stop = float(p["stop_" + g])
		if float(p["trauma_" + g]) > shake:
			shake = float(p["trauma_" + g])
			kick = h.dir if g != "hit" and g != "object" else Vector2.ZERO
		var a: RefCounted = h.actor  # standards: allow weak_type (actor or breakable)
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
			launches[a] = {
				"t": 0.0,
				"total": t,
				"dir": h.dir,
				"px": float(p.launch_boss_px if h.boss else p.launch_px),
				"hop": float(p.launch_hop_px)
			}
			recoils.erase(a)
		elif on.recoil:
			var t := float(p.recoil_time)
			recoils[a] = {
				"t": 0.0,
				"total": t,
				"dir": h.dir,
				"px": float(p.recoil_heavy_px if h.heavy else p.recoil_px)
			}
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
func flash_of(actor: RefCounted) -> Array:  # standards: allow weak_type (actor or breakable)
	if not flashes.has(actor):
		return [0.0, WHITE]
	var f: Dictionary = flashes[actor]
	return [clampf(f.t / maxf(f.total, 0.001), 0.0, 1.0), f.color]


## Where the actor is drawn off its place, in map pixels: x, y on the floor, z up (the hop).
func offset_of(actor: RefCounted) -> Vector3:  # standards: allow weak_type (actor or breakable)
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
	var y := (
		_noise.get_noise_2d(0.0, t + 100.0) * float(p.shake_px) * s + _kick.y * float(p.shake_scale)
	)
	var roll := _noise.get_noise_2d(t + 200.0, t) * float(p.shake_roll) * s
	return Vector3(x, y, roll)


## The pitch of a hit sound: a little higher or lower each time.
func pitch(rng: RandomNumberGenerator) -> float:
	var s := float(p.pitch_spread)
	return 1.0 + rng.randf_range(-s, s)


## The effects as the player set them (Settings): all of them with "hit_feel", the shake also
## with "screen_shake", the rumble also with "rumble".
func use_settings(settings: Node) -> void:
	var all := bool(settings.get_value("hit_feel"))
	for k in on:
		on[k] = all
	on.shake = all and bool(settings.get_value("screen_shake"))
	on.rumble = all and bool(settings.get_value("rumble"))


## The sounds of a tick (MapSim.sounds) through Audio: while the sound effect is on, the hits
## (3, 4, 15, 16) with their pitch a little off each time, louder on a strong hit, and on a kill
## a lower second layer just after; everything else as the game always plays it.
func play_sounds(sounds: Array, list: Array) -> void:
	var kill := false
	var heavy := false
	for h in list:
		kill = kill or (h.killed and h.who == "enemy")
		heavy = heavy or h.heavy
	for n in sounds:
		if not (on.sound and n in HIT_SOUNDS):
			Audio.play_sound(n)
			continue
		var db := float(p.heavy_db) if heavy or kill else 0.0
		Audio.play_sound(n, pitch(_sound_pick), db)
		if kill:
			kill = false
			var tree := Engine.get_main_loop() as SceneTree
			if tree != null:
				tree.create_timer(float(p.kill_delay)).timeout.connect(
					Audio.play_sound.bind(n, float(p.kill_pitch), db)
				)


## Plays the rumble react() asked for: on the pad's motors when a pad is what the player uses,
## a short buzz of the phone when it is the touch screen.
func rumble(device: String) -> void:
	if rumble_wanted.is_empty():
		return
	var k := float(p.rumble_scale)
	var weak := clampf(float(rumble_wanted[0]) * k, 0.0, 1.0)
	var strong := clampf(float(rumble_wanted[1]) * k, 0.0, 1.0)
	var secs := float(rumble_wanted[2])
	rumble_wanted = []
	if weak <= 0.0 and strong <= 0.0:
		return
	if device == "pad":
		for j in Input.get_connected_joypads():
			Input.start_joy_vibration(j, weak, strong, secs)
	elif device == "touch" and OS.has_feature("mobile"):
		Input.vibrate_handheld(int(secs * 1000.0), maxf(weak, strong))


## The camera's shake now, put on its offsets (they move the picture without moving the camera,
## so its following the room is not disturbed). PX: world units per map pixel.
func shake_camera(camera: Camera3D, px: float) -> void:
	var s := camera_shake()
	camera.h_offset = s.x * px
	camera.v_offset = -s.y * px
	camera.rotation.z = deg_to_rad(s.z)


## Where between two ticks a knocked-back actor is drawn: out fast, slowing down (while that
## effect is on), instead of at an even speed.
func knock_t(t: float) -> float:
	t = clampf(t, 0.0, 1.0)
	return 1.0 - pow(1.0 - t, 3.0) if on.knock_ease else t


## The flash of one hit on a sprite: drawn for that moment with a material that adds the colour
## as light, so it shows nearly white (on the hero red) even unlit, keeping the sprite's own
## picture, billboard and alpha edge. `mats` keeps a material per sprite.
## The hit flash on a piece of the new art: its painted material, f as flash_of() gives it.
static func flash_material(m: Material, f: Array) -> void:
	if m is ShaderMaterial:
		var c: Color = f[1]
		(m as ShaderMaterial).set_shader_parameter("flash", float(f[0]))
		(m as ShaderMaterial).set_shader_parameter("flash_color", Vector3(c.r, c.g, c.b))


static func flash_sprite(s: Sprite3D, f: Array, mats: Dictionary) -> void:
	var k: float = f[0]
	if k <= 0.0:
		if s.material_override != null:
			s.material_override = null
		return
	var m: StandardMaterial3D = mats.get(s)
	if m == null:
		m = StandardMaterial3D.new()
		m.billboard_mode = BaseMaterial3D.BILLBOARD_FIXED_Y
		m.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
		m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
		m.alpha_scissor_threshold = 0.5
		m.cull_mode = BaseMaterial3D.CULL_DISABLED
		m.vertex_color_use_as_albedo = true
		m.emission_enabled = true
		mats[s] = m
	m.albedo_texture = s.texture
	m.emission = f[1]
	m.emission_energy_multiplier = 1.2 * k
	m.no_depth_test = s.no_depth_test
	m.render_priority = s.render_priority
	s.material_override = m


## Forgets the effects of actors gone from the map (no longer in `alive`).
func forget_except(alive: Dictionary) -> void:
	for d in [flashes, recoils, launches]:
		for a in d.keys():
			if not alive.has(a):
				d.erase(a)
