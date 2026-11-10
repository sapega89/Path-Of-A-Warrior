class_name MapEffects
extends SkillEffects
## The effects of a mission in the new art, made in code: the blows, skills, potions and
## scrolls MapSim shows, the fire on whoever burns, the auras of buffs, the blood of hits (and
## the blots it leaves on the ground for a while), the weapon trails and the archers' arrows.
## show_effects() takes what MapSim gives each tick: [kind, frame, point in map pixels], with an
## optional true for the ring of an aura (on the ground behind the one who glows) or for a trail
## whose swing is done (it fades). The frame says how far the effect has gone (and for some,
## which way it goes); t, 0..1 of the way to the next tick, carries it on smoothly.
## Room-wide skills (Thunderstorm, Rain of Fire) strike at places that follow from the frame,
## the same each time.

const BLOOD := preload("res://assets/art/shaders/fx_blood.gdshader")

## The kinds of effects and how many frames each has (the skills' own: SKILL_FRAMES).
##   slash:  dust kicked up by a dash (frame: direction << 1 | step)
##   trail:  the trail of a blade (direction * 3 + which blow)
##   spark:  where a blow lands on steel (two steps; 0-1 a light hit, 2-3 a hard one)
##   blood:  where a blow lands on a man: drops thrown out and the blood they leave on the
##           ground (two steps; 0-1 a light hit, 2-3 a hard one; +4 they fly to the right,
##           +8 to the left)
##   pool:   blood spreading under one who lies fallen (it stays at the last frame)
##   heal, buff, aura: herbs and water healing, a buff or a potion, the glow of a buff
##   whirl:  the crown of water that knocks back
##   fire, burst, blast: fire on someone, a fire burst, an explosion
##   wave:   lightning running ahead (direction * 7 + step)
##   storm, rain, quake: Thunderstorm, Rain of Fire, Serpent's Breath over the room
##   scroll: the orb of a scroll flying ahead (direction * 4 + step)
const FRAMES := {
	"slash": 8,
	"trail": 12,
	"spark": 4,
	"blood": 12,
	"pool": 8,
	"heal": 9,
	"buff": 6,
	"aura": 6,
	"whirl": 2,
	"fire": 10,
	"burst": 2,
	"blast": 10,
	"wave": 28,
	"storm": 42,
	"rain": 25,
	"quake": 15,
	"scroll": 16
}

## Height of the flames of someone burning, by frame.
const FIRE_H := [0.6, 1.0, 1.4, 1.75, 1.95, 2.0, 1.95, 1.75, 0.9, 0.5]
## How far (px) the arrows fly each tick.
const ARROW_STEP := 12

var _arrows: Array[Node3D] = []
var _arrow_mesh: ArrayMesh
## What the last show_effects() drew: [kind, frame, rig].
var drawn: Array = []
## The blood hits leave on the ground: [blot, when it was left (ms)]; the oldest goes first.
const STAINS := 24
const STAIN_MS := 9000.0
var _stains: Array = []
var _stain_holder: Node3D
## The hits that bled last time and this time (by place and blow), so that each leaves one stain.
var _bled := {}
var _bleeding := {}


## Draws the effects of the tick; t: 0..1 of the way to the next tick.
func show_effects(list: Array, t := 0.0) -> void:
	_used.clear()
	drawn.clear()
	_bleeding = {}
	for e in list:
		var kind := str(e[0])
		var frame := int(e[1])
		if frame < 0 or frame >= int(FRAMES.get(kind, SKILL_FRAMES.get(kind, 0))):
			continue
		var rig := _rig(kind)
		rig.visible = true
		var p := Vector2(e[2])
		var behind: bool = e.size() > 3 and bool(e[3])
		call("_draw_" + kind, rig, frame, p, clampf(t, 0.0, 1.0), behind)
		drawn.append([kind, frame, rig])
	for kind in _pools:
		var pool: Array = _pools[kind]
		for i in range(int(_used.get(kind, 0)), pool.size()):
			pool[i].visible = false
	_bled = _bleeding
	_age_stains()


## How many effects the last call drew.
func shown() -> int:
	return drawn.size()


## The archers' arrows in flight (MapSim.arrows); moving: they fly on this tick (they stand
## while a big skill holds the room), so they are drawn on their way to the next place.
func show_shots(arrows: Array, t := 0.0, moving := true) -> void:
	while _arrows.size() < arrows.size():
		var a := MeshInstance3D.new()
		a.name = "Arrow%d" % _arrows.size()
		a.mesh = _arrow()
		a.material_override = ArtKit.props_material()
		a.visible = false
		add_child(a)
		_arrows.append(a)
	for i in _arrows.size():
		var node := _arrows[i]
		var a = arrows[i] if i < arrows.size() else null
		node.visible = a != null and a.active
		if not node.visible:
			continue
		var d := int(a.dir)
		var step := (
			Vector2(int(MapSim.table("front_dx")[d]), int(MapSim.table("front_dy")[d])).normalized()
			* ARROW_STEP
		)
		var p := Vector2(a.pos) + Vector2(a.w, a.h) / 2.0 + Vector2(0.0, 8.0)
		if moving and int(a.ticks) > 0:
			p -= step * (1.0 - clampf(t, 0.0, 1.0))
		node.position = MapPeople.to_world(p) + Vector3(0.0, 0.95, 0.0)
		node.rotation = Vector3(0.0, Motion.yaw_of(d << 1), 0.0)


# ---- a dash: dust ------------------------------------------------------------------------


func _build_slash(rig: Node3D) -> void:
	_light(rig, "Ring", Shape.RING, Turn.PLACED, DUST, 0.4)
	for i in 3:
		_puff(rig, "Dust%d" % i, Turn.FACING, DUST)


func _draw_slash(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var dir8 := (frame >> 1) << 1
	var ph := _run(frame & 1, t, 2)
	var ahead := _ahead(dir8)
	var side := ahead.cross(Vector3.UP)
	var at := _at(p)
	var ring := rig.get_node("Ring") as MeshInstance3D
	_flat(ring, at, lerpf(0.9, 2.2, ph))
	_tune(ring, {"radius": 0.75, "width": 0.14, "count": 0.0, "strength": 0.7 * (1.0 - ph)})
	for i in 3:
		var puff := rig.get_node("Dust%d" % i) as MeshInstance3D
		var back := 0.25 + 0.3 * i * (0.6 + ph)
		_quad(
			puff,
			(
				at
				- ahead * back
				+ side * (i - 1) * 0.28
				+ Vector3(0.0, 0.3 + 0.12 * i + 0.3 * ph, 0.0)
			),
			0.7 + 0.55 * ph
		)
		_tune(puff, {"strength": 0.9 * (1.0 - ph * ph), "seed": _seed(p, i)})


# ---- the trail of a blade ----------------------------------------------------------------


func _build_trail(rig: Node3D) -> void:
	# a sweep to the left, one back to the right, and a chop from above
	var sweeps := [[-80.0, 160.0, 0.35], [80.0, -160.0, -0.35]]
	for i in 2:
		var r := ArtEffects.slash(
			rig, Vector3.ZERO, sweeps[i][0], sweeps[i][1], 1.05, 0.95, sweeps[i][2]
		)
		r.name = "Blow%d" % i
	var chop := ArtEffects.slash(rig, Vector3.ZERO, 120.0, -170.0, 1.0, 0.0, 0.0)
	chop.name = "Blow2"
	chop.rotation = Vector3(0.0, 0.0, PI / 2.0)
	chop.position = Vector3(0.0, 0.95, 0.0)
	for i in 3:
		var m := ShaderMaterial.new()
		m.shader = LIGHT
		m.set_shader_parameter("shape", Shape.SWEEP)
		m.set_shader_parameter("body", 0.55)
		_colours(m, STEEL)
		(rig.get_node("Blow%d" % i) as MeshInstance3D).material_override = m


func _draw_trail(rig: Node3D, frame: int, p: Vector2, t: float, fading: bool) -> void:
	var blow := frame % 3
	rig.position = _at(p)
	rig.rotation = Vector3(0.0, Motion.yaw_of((frame / 3) << 1), 0.0)
	for i in 3:
		var r := rig.get_node("Blow%d" % i) as MeshInstance3D
		r.visible = i == blow
		if r.visible:
			var swing := {"progress": 0.25 + 0.7 * t, "strength": 1.0}
			_tune(r, {"progress": 0.8, "strength": 1.0 - t} if fading else swing)


# ---- a hit -------------------------------------------------------------------------------


func _build_spark(rig: Node3D) -> void:
	_light(rig, "Glow", Shape.GLOW, Turn.FACING, WARM)
	_light(rig, "Star", Shape.STAR, Turn.FACING, WARM, 0.35)


func _draw_spark(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var hard := frame >= 2
	var ph := _run(frame & 1, t, 2)
	var at := _at(p) + Vector3(0.0, 0.95, 0.0)
	var colours: Array = HOT if hard else WARM
	var star := rig.get_node("Star") as MeshInstance3D
	var glow := rig.get_node("Glow") as MeshInstance3D
	_colours(star.material_override, colours)
	_colours(glow.material_override, colours)
	var size := 1.25 if hard else 0.95
	_quad(star, at, size * lerpf(0.85, 1.35, ph))
	_tune(
		star,
		{
			"count": 7.0 if hard else 9.0,
			"seed": _seed(p, frame),
			"strength": 1.0 - ph * ph,
			"toward": 0.8
		}
	)
	_quad(glow, at, size * lerpf(1.0, 0.5, ph))
	_tune(glow, {"strength": 0.9 * (1.0 - ph), "toward": 0.75})


# ---- blood -------------------------------------------------------------------------------


## A part of blood: a quad with fx_blood in a shape (0 the spray, 1 a blot on the ground).
func _blood_part(rig: Node3D, part: String, shape: int, turn: Turn) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	mi.name = part
	var q := QuadMesh.new()
	q.size = Vector2.ONE
	mi.mesh = q
	var m := ShaderMaterial.new()
	m.shader = BLOOD
	m.set_shader_parameter("shape", shape)
	m.set_shader_parameter("billboard", turn)
	mi.material_override = m
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mi.extra_cull_margin = 4.0
	if rig != null:
		rig.add_child(mi)
	return mi


func _build_blood(rig: Node3D) -> void:
	_blood_part(rig, "Spray", 0, Turn.FACING)
	_light(rig, "Glint", Shape.GLOW, Turn.FACING, STEEL)


func _draw_blood(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var hard := (frame & 3) >= 2
	var side: float = [0.0, 1.0, -1.0][clampi(frame >> 2, 0, 2)]
	var ph := _run(frame & 1, t, 2)
	var at := _at(p) + Vector3(0.0, 1.0, 0.0)
	var size := 2.0 if hard else 1.45
	var spray := rig.get_node("Spray") as MeshInstance3D
	_quad(spray, at, size)
	_tune(
		spray,
		{
			"progress": ph,
			"count": 18.0 if hard else 11.0,
			"seed": _seed(p, frame & 3),
			"side": side,
			"strength": 1.0 - smoothstep(0.8, 1.0, ph),
			"toward": 0.8
		}
	)
	var glint := rig.get_node("Glint") as MeshInstance3D
	_quad(glint, at, size * 0.6 * (1.0 - ph))
	_tune(glint, {"strength": 0.5 * (1.0 - ph) * (1.0 - ph), "toward": 0.85})
	# one blot on the ground for each blow, a little to the side the drops fly
	var key := "%d,%d,%d" % [int(p.x), int(p.y), frame >> 1]
	_bleeding[key] = true
	if not _bled.has(key):
		_stain(_at(p) + Vector3(side * 0.35, 0.0, 0.0), size * 0.8, _seed(p, frame))


## Leaves a blot of blood on the ground, the oldest going when there are too many.
func _stain(at: Vector3, size: float, seed_value: float) -> void:
	if _stain_holder == null:
		_stain_holder = Node3D.new()
		_stain_holder.name = "Stains"
		add_child(_stain_holder)
	var blot: MeshInstance3D
	if _stains.size() >= STAINS:
		blot = _stains.pop_front()[0]
	else:
		blot = _blood_part(_stain_holder, "Stain%d" % _stains.size(), 1, Turn.PLACED)
	_flat(blot, at, size)
	_tune(blot, {"seed": seed_value, "progress": 0.0, "strength": 0.85})
	_stains.append([blot, Time.get_ticks_msec()])


## The blots spread for a moment, lie, and fade away.
func _age_stains() -> void:
	var now := Time.get_ticks_msec()
	for s in _stains:
		var age := float(now - int(s[1]))
		_tune(
			s[0],
			{
				"progress": clampf(age / 400.0, 0.0, 1.0),
				"strength": 0.85 * (1.0 - smoothstep(STAIN_MS * 0.6, STAIN_MS, age))
			}
		)


func _build_pool(rig: Node3D) -> void:
	_blood_part(rig, "Pool", 1, Turn.PLACED)


func _draw_pool(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var ph := _run(frame, t, 8)
	var pool := rig.get_node("Pool") as MeshInstance3D
	_flat(pool, _at(p), lerpf(0.9, 2.0, ph))
	_tune(pool, {"progress": 0.3 + 0.7 * ph, "seed": _seed(p), "strength": 0.9})


# ---- healing, buffs, auras ---------------------------------------------------------------


func _build_heal(rig: Node3D) -> void:
	_light(rig, "Spiral", Shape.SPIRAL, Turn.PLACED, HEAL, 0.35, true)
	_light(rig, "Motes", Shape.MOTES, Turn.PLACED, HEAL, 0.6, true)
	_light(rig, "Ground", Shape.GLOW, Turn.PLACED, HEAL)


func _draw_heal(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var ph := _run(frame, t, 9)
	var swell := _swell(ph)
	var at := _at(p)
	_pillar(rig.get_node("Spiral"), at, 0.6, 2.1)
	_tune(rig.get_node("Spiral"), {"count": 2.0, "progress": ph, "strength": swell})
	_pillar(rig.get_node("Motes"), at, 0.75, 2.5)
	_tune(rig.get_node("Motes"), {"count": 10.0, "strength": swell})
	_flat(rig.get_node("Ground"), at, 1.9)
	_tune(rig.get_node("Ground"), {"strength": 0.6 * swell})


func _build_buff(rig: Node3D) -> void:
	_light(rig, "Column", Shape.COLUMN, Turn.PLACED, WARM, 0.15, true)
	_light(rig, "Ring", Shape.RING, Turn.PLACED, WARM, 0.4)
	_light(rig, "Ground", Shape.GLOW, Turn.PLACED, WARM)


## A pillar of light comes down on him (frames 0-3) and spreads in a ring on the ground (3-5;
## a potion shows only the ring).
func _draw_buff(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var ph := _run(frame, t, 6)
	var at := _at(p)
	var column := smoothstep(0.0, 0.12, ph) * (1.0 - smoothstep(0.5, 0.72, ph))
	_pillar(rig.get_node("Column"), at, 0.55, lerpf(3.4, 2.4, ph))
	_tune(rig.get_node("Column"), {"count": 6.0, "seed": _seed(p), "strength": column})
	var spread := clampf((ph - 0.45) / 0.55, 0.0, 1.0)
	_flat(rig.get_node("Ring"), at, 1.2 + 1.8 * spread)
	_tune(
		rig.get_node("Ring"),
		{
			"radius": 0.7,
			"width": 0.1,
			"count": 0.0,
			"strength": (1.0 - spread) if ph > 0.45 else 0.0
		}
	)
	_flat(rig.get_node("Ground"), at, 1.6)
	_tune(rig.get_node("Ground"), {"strength": 0.5 * maxf(column, 1.0 - spread)})


func _build_aura(rig: Node3D) -> void:
	_light(rig, "Ring", Shape.RING, Turn.PLACED, WARM, 0.4)
	_light(rig, "Light", Shape.MOTES, Turn.PLACED, WARM, 0.6, true)


## The ring on the ground behind him (frames 0-2) or the light rising around him (3-5).
func _draw_aura(rig: Node3D, frame: int, p: Vector2, t: float, behind: bool) -> void:
	var at := _at(p - Vector2(0, 3))
	var ring := behind or frame < 3
	var pulse := _run(frame % 3, t, 3)
	_flat(rig.get_node("Ring"), at, 1.35 + 0.12 * sin(pulse * TAU))
	_tune(
		rig.get_node("Ring"),
		{"radius": 0.72, "width": 0.09, "count": 0.0, "strength": 0.6 if ring else 0.0}
	)
	_pillar(rig.get_node("Light"), at, 0.5, 2.1)
	_tune(rig.get_node("Light"), {"count": 7.0, "seed": 1.3, "strength": 0.0 if ring else 1.0})


# ---- water, fire, explosions -------------------------------------------------------------


func _build_whirl(rig: Node3D) -> void:
	_light(rig, "Ring", Shape.RING, Turn.PLACED, WATER, 0.5)
	_light(rig, "Wall", Shape.SPLASH, Turn.PLACED, WATER, 0.5, true)
	_light(rig, "Ground", Shape.GLOW, Turn.PLACED, WATER)


func _draw_whirl(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var ph := _run(frame, t, 2)
	var at := _at(p)
	_flat(rig.get_node("Ring"), at, 1.6 + 2.8 * ph)
	_tune(
		rig.get_node("Ring"),
		{"radius": 0.7, "width": 0.1, "count": 16.0, "seed": _seed(p), "strength": 1.0 - 0.7 * ph}
	)
	_pillar(rig.get_node("Wall"), at, 0.7 + 1.3 * ph, 1.0 - 0.45 * ph)
	_tune(rig.get_node("Wall"), {"count": 22.0, "seed": _seed(p), "strength": 0.9 * (1.0 - ph)})
	_flat(rig.get_node("Ground"), at, 2.4 + 2.0 * ph)
	_tune(rig.get_node("Ground"), {"strength": 0.45 * (1.0 - ph)})


func _build_fire(rig: Node3D) -> void:
	_light(rig, "Flame0", Shape.FLAME, Turn.UPRIGHT, HOT, 0.55)
	_light(rig, "Flame1", Shape.FLAME, Turn.UPRIGHT, HOT, 0.55)
	_light(rig, "Ground", Shape.GLOW, Turn.PLACED, HOT)


func _draw_fire(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var h := lerpf(FIRE_H[frame], FIRE_H[mini(frame + 1, FIRE_H.size() - 1)], t)
	var at := _at(p)
	var s := _seed(p)
	_quad(rig.get_node("Flame0"), at + Vector3(0.1, h / 2.0, 0.0), 0.9 * maxf(h, 0.6), h)
	_tune(rig.get_node("Flame0"), {"seed": s, "toward": 0.45})
	_quad(rig.get_node("Flame1"), at + Vector3(-0.22, h * 0.38, 0.05), 0.7 * maxf(h, 0.6), h * 0.76)
	_tune(rig.get_node("Flame1"), {"seed": s + 3.0, "toward": 0.5})
	_flat(rig.get_node("Ground"), at, 1.0 + 0.7 * h)
	_tune(rig.get_node("Ground"), {"strength": 0.55})


func _build_burst(rig: Node3D) -> void:
	_light(rig, "Glow", Shape.GLOW, Turn.FACING, HOT)
	_light(rig, "Star", Shape.STAR, Turn.FACING, HOT, 0.35)
	_light(rig, "Ring", Shape.RING, Turn.PLACED, HOT, 0.4)


func _draw_burst(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var ph := _run(frame, t, 2)
	var at := _at(p)
	_quad(rig.get_node("Glow"), at + Vector3(0.0, 0.8, 0.0), 2.2 * (0.6 + 0.6 * ph))
	_tune(rig.get_node("Glow"), {"strength": 1.0 - ph, "toward": 0.5})
	_quad(rig.get_node("Star"), at + Vector3(0.0, 0.8, 0.0), 1.5 + 1.8 * ph)
	_tune(
		rig.get_node("Star"),
		{"count": 11.0, "seed": _seed(p), "strength": 1.0 - pow(ph, 1.5), "toward": 0.6}
	)
	_flat(rig.get_node("Ring"), at, 1.2 + 3.2 * ph)
	_tune(rig.get_node("Ring"), {"radius": 0.75, "width": 0.08, "count": 0.0, "strength": 1.0 - ph})


func _build_blast(rig: Node3D) -> void:
	_light(rig, "Glow", Shape.GLOW, Turn.FACING, HOT)
	_light(rig, "Star", Shape.STAR, Turn.FACING, HOT, 0.35)
	_light(rig, "Scorch", Shape.RING, Turn.PLACED, HOT, 0.4)
	for i in 2:
		_puff(rig, "Smoke%d" % i, Turn.FACING, SMOKE)


## An explosion: a scroll's (frames 0-1, where it lands) or one of those that end Rain of
## Fire (2-9, each one tick, at its own place in the room).
func _draw_blast(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var ph := _run(frame, t, 2) if frame < 2 else _run(0, t, 1)
	var size := 1.0 if frame < 2 else 0.8
	var at := _at(p + (Vector2.ZERO if frame < 2 else scatter("blast", frame, 95.0, 75.0)))
	var mid := at + Vector3(0.0, 0.8 * size, 0.0)
	_quad(rig.get_node("Glow"), mid, 2.6 * size * (0.5 + 0.5 * ph))
	_tune(rig.get_node("Glow"), {"strength": 1.0 - ph, "toward": 0.4})
	_quad(rig.get_node("Star"), mid, 3.0 * size * (0.4 + 0.6 * ph))
	_tune(
		rig.get_node("Star"),
		{"count": 13.0, "seed": _seed(p, frame), "strength": pow(1.0 - ph, 1.2), "toward": 0.5}
	)
	_flat(rig.get_node("Scorch"), at, 2.8 * size * (0.3 + 0.7 * ph))
	_tune(
		rig.get_node("Scorch"),
		{"radius": 0.7, "width": 0.12, "count": 9.0, "seed": _seed(p), "strength": 1.0 - ph}
	)
	for i in 2:
		var smoke := rig.get_node("Smoke%d" % i) as MeshInstance3D
		_quad(
			smoke,
			mid + Vector3((i - 0.5) * 0.5 * size, (0.3 + ph * 1.1) * size, 0.0),
			1.3 * size * (0.5 + ph)
		)
		_tune(smoke, {"strength": 0.6 * sin(ph * PI), "seed": _seed(p, i)})


# ---- lightning ---------------------------------------------------------------------------


func _build_wave(rig: Node3D) -> void:
	for i in 3:
		_light(rig, "Bolt%d" % i, Shape.BOLT, Turn.AXIS, STORM, 0.3)
	_light(rig, "Ball", Shape.GLOW, Turn.FACING, STORM)
	_light(rig, "Ground", Shape.GLOW, Turn.PLACED, STORM)


## Lightning runs ahead of the caster: a ball crackling on its way, a bolt from his hand to it.
func _draw_wave(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var step := frame % 7
	var ahead := _ahead((frame / 7) << 1)
	var reach := (20.0 + (step + t) * 17.0) * PX
	var hand := _at(p) + Vector3(0.0, 1.05, 0.0) + ahead * 0.35
	var ball := _at(p) + ahead * reach + Vector3(0.0, 0.8, 0.0)
	var s := _seed(p, frame)
	_span(rig.get_node("Bolt0"), hand, ball, 0.7)
	_tune(rig.get_node("Bolt0"), {"seed": s, "strength": 1.0})
	for i in 2:
		var a := s * 2.3 + i * 2.2 + t * 3.0
		var tip := ball + Vector3(cos(a), 0.6 * sin(a * 1.7), sin(a)) * 0.9
		_span(rig.get_node("Bolt%d" % (i + 1)), ball, tip, 0.5)
		_tune(rig.get_node("Bolt%d" % (i + 1)), {"seed": s + i + 1.0, "strength": 0.9})
	_quad(rig.get_node("Ball"), ball, 1.3)
	_tune(rig.get_node("Ball"), {"strength": 1.0, "toward": 0.3})
	_flat(rig.get_node("Ground"), Vector3(ball.x, 0.0, ball.z), 1.8)
	_tune(rig.get_node("Ground"), {"strength": 0.5})


func _build_storm(rig: Node3D) -> void:
	_light(rig, "Bolt", Shape.BOLT, Turn.AXIS, STORM, 0.3)
	_light(rig, "Ground", Shape.GLOW, Turn.PLACED, STORM)
	_light(rig, "Ring", Shape.RING, Turn.PLACED, STORM, 0.3)


## Thunderstorm: strikes from the sky, first over the middle of the room (frames 0-5, the
## storm gathering), then three each tick all over it.
func _draw_storm(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var gathering := frame < 6
	var at := _at(p + (Vector2.ZERO if gathering else scatter("storm", frame, 100.0, 80.0)))
	var s := _seed(p, frame)
	var lean := Vector3(sin(s) * 0.8, 0.0, cos(s * 1.3) * 0.4)
	_span(rig.get_node("Bolt"), at, at + Vector3(0.0, 7.5, 0.0) + lean, 0.55 if gathering else 1.0)
	_tune(
		rig.get_node("Bolt"),
		{"seed": s, "strength": (0.55 if gathering else 1.0) * (1.0 - 0.6 * t)}
	)
	_flat(rig.get_node("Ground"), at, 2.4)
	_tune(rig.get_node("Ground"), {"strength": 0.9 * (1.0 - t)})
	_flat(rig.get_node("Ring"), at, 1.0 + 2.2 * t)
	_tune(
		rig.get_node("Ring"),
		{"radius": 0.7, "width": 0.1, "count": 0.0, "strength": 0.8 * (1.0 - t)}
	)


# ---- fire from above, the fire serpent ---------------------------------------------------


func _build_rain(rig: Node3D) -> void:
	_light(rig, "Tail", Shape.STREAK, Turn.AXIS, HOT, 0.35)
	_light(rig, "Head", Shape.GLOW, Turn.FACING, HOT, 0.3)
	_light(rig, "Ground", Shape.GLOW, Turn.PLACED, HOT)


## Rain of Fire: five fireballs a tick fall from the sky on places all over the room.
func _draw_rain(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var ground := _at(p + scatter("rain", frame, 105.0, 85.0))
	var sky := ground + Vector3(-2.4, 7.5, -1.4)
	var fall := pow(t, 1.3)
	var head := sky.lerp(ground, fall) + Vector3(0.0, 0.25, 0.0)
	var tail := head + (sky - ground).normalized() * 2.4
	_span(rig.get_node("Tail"), tail, head, 0.9)
	_tune(rig.get_node("Tail"), {"seed": _seed(p, frame), "strength": 1.0})
	_quad(rig.get_node("Head"), head, 1.0)
	_tune(rig.get_node("Head"), {"strength": 1.0})
	_flat(rig.get_node("Ground"), ground, 0.8 + 1.6 * fall)
	_tune(rig.get_node("Ground"), {"strength": 0.25 + 0.6 * fall})


func _build_quake(rig: Node3D) -> void:
	var body := MeshInstance3D.new()
	body.name = "Body"
	body.mesh = ImmediateMesh.new()
	var m := ShaderMaterial.new()
	m.shader = LIGHT
	m.set_shader_parameter("shape", Shape.RIBBON)
	m.set_shader_parameter("billboard", Turn.PLACED)
	m.set_shader_parameter("body", 0.5)
	_colours(m, HOT)
	body.material_override = m
	body.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	body.extra_cull_margin = 8.0
	rig.add_child(body)
	_light(rig, "Head", Shape.GLOW, Turn.FACING, HOT, 0.3)
	_light(rig, "Ground", Shape.GLOW, Turn.PLACED, HOT)


## Serpent's Breath: a serpent of fire winds round the room.
func _draw_quake(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var ph := _run(frame, t, 15)
	var swell := _swell(ph, 0.1, 0.15)
	var middle := _at(p)
	var radius := 85.0 * PX
	var head_a := -PI / 2.0 + ph * TAU * 1.3
	var cam := get_viewport().get_camera_3d() if is_inside_tree() else null
	var mesh := (rig.get_node("Body") as MeshInstance3D).mesh as ImmediateMesh
	mesh.clear_surfaces()
	var n := 40
	var points: Array[Vector3] = []
	for i in n:
		var a := head_a - (1.0 - float(i) / (n - 1)) * 2.8
		points.append(
			(
				middle
				+ Vector3(
					cos(a) * radius, 0.75 + 0.35 * sin(a * 3.0 + ph * 9.0), sin(a) * radius * 0.8
				)
			)
		)
	mesh.surface_begin(Mesh.PRIMITIVE_TRIANGLE_STRIP)
	for i in n:
		var along := points[mini(i + 1, n - 1)] - points[maxi(i - 1, 0)]
		var to_cam := (cam.global_position - points[i]) if cam != null else Vector3(0.0, 0.57, 0.82)
		var side := along.cross(to_cam).normalized() * 0.65 * swell
		var u := float(i) / (n - 1)
		mesh.surface_set_uv(Vector2(u, 0.0))
		mesh.surface_add_vertex(points[i] + side)
		mesh.surface_set_uv(Vector2(u, 1.0))
		mesh.surface_add_vertex(points[i] - side)
	mesh.surface_end()
	_tune(rig.get_node("Body"), {"strength": swell, "seed": 2.0})
	_quad(rig.get_node("Head"), points[n - 1], 1.5 * swell + 0.01)
	_tune(rig.get_node("Head"), {"strength": swell})
	_flat(rig.get_node("Ground"), Vector3(points[n - 1].x, 0.0, points[n - 1].z), 2.0)
	_tune(rig.get_node("Ground"), {"strength": 0.5 * swell})


# ---- a scroll ----------------------------------------------------------------------------


func _build_scroll(rig: Node3D) -> void:
	_light(rig, "Orb", Shape.GLOW, Turn.FACING, WARM, 0.3)
	_light(rig, "Star", Shape.STAR, Turn.FACING, WARM, 0.3)
	_light(rig, "Tail", Shape.STREAK, Turn.AXIS, WARM, 0.2)
	_puff(rig, "Shadow", Turn.PLACED, SMOKE)


## The orb of a scroll flies up and ahead to where its blast falls.
func _draw_scroll(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var d := frame >> 2
	var s := _run(frame & 3, t, 4)
	var front := Vector2(int(MapSim.table("front_dx")[d]), int(MapSim.table("front_dy")[d]))
	var ground := _at(p + front * s)
	var at := ground + Vector3(0.0, 1.0 + sin(PI * s) * 1.3, 0.0)
	var before := (
		_at(p + front * maxf(s - 0.15, 0.0))
		+ Vector3(0.0, 1.0 + sin(PI * maxf(s - 0.15, 0.0)) * 1.3, 0.0)
	)
	_quad(rig.get_node("Orb"), at, 0.9)
	_tune(rig.get_node("Orb"), {"strength": 1.0})
	_quad(rig.get_node("Star"), at, 0.8)
	_tune(rig.get_node("Star"), {"count": 6.0, "seed": s * 6.0, "strength": 0.8})
	_span(rig.get_node("Tail"), at + (before - at) * 3.0, at, 0.45)
	_tune(rig.get_node("Tail"), {"strength": 0.8 if s > 0.02 else 0.0})
	_flat(rig.get_node("Shadow"), ground, 0.6)
	_tune(rig.get_node("Shadow"), {"strength": 0.35})


# ---- an arrow ----------------------------------------------------------------------------


## An arrow along +Z: a shaft of oak, a steel head, white and red fletching.
func _arrow() -> ArrayMesh:
	if _arrow_mesh != null:
		return _arrow_mesh
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	_box(
		st, Vector3(0.0, 0.0, 0.0), Vector3(0.03, 0.03, 0.72), ArtKit.color("ochre").darkened(0.25)
	)
	# the head: a pyramid
	var steel := ArtKit.color("steel").lightened(0.2)
	var tip := Vector3(0.0, 0.0, 0.48)
	var base := [
		Vector3(-0.045, 0.0, 0.34),
		Vector3(0.0, 0.045, 0.34),
		Vector3(0.045, 0.0, 0.34),
		Vector3(0.0, -0.045, 0.34)
	]
	for i in 4:
		_tri(st, base[i], base[(i + 1) % 4], tip, steel)
	# the fletching: two crossed vanes
	for v in [Vector3(0.07, 0.0, 0.0), Vector3(0.0, 0.07, 0.0)]:
		var col := ArtKit.color("whitewash") if v.x > 0.0 else ArtKit.color("cinnabar")
		var a := Vector3(0.0, 0.0, -0.36)
		var b := Vector3(0.0, 0.0, -0.2)
		_tri(st, a - v, b, a + v, col)
		_tri(st, a + v, b, a - v, col)
	st.generate_normals()
	_arrow_mesh = st.commit()
	return _arrow_mesh


static func _tri(st: SurfaceTool, a: Vector3, b: Vector3, c: Vector3, col: Color) -> void:
	st.set_color(col.srgb_to_linear())
	st.add_vertex(a)
	st.add_vertex(b)
	st.add_vertex(c)


static func _box(st: SurfaceTool, at: Vector3, size: Vector3, col: Color) -> void:
	var h := size / 2.0
	var c := [
		Vector3(-h.x, -h.y, -h.z),
		Vector3(h.x, -h.y, -h.z),
		Vector3(h.x, h.y, -h.z),
		Vector3(-h.x, h.y, -h.z),
		Vector3(-h.x, -h.y, h.z),
		Vector3(h.x, -h.y, h.z),
		Vector3(h.x, h.y, h.z),
		Vector3(-h.x, h.y, h.z)
	]
	for f in [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [3, 7, 6, 2], [0, 4, 7, 3], [1, 2, 6, 5]]:
		_tri(st, at + c[f[0]], at + c[f[1]], at + c[f[2]], col)
		_tri(st, at + c[f[0]], at + c[f[2]], at + c[f[3]], col)
