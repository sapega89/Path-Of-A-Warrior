class_name SkillEffects
extends FxRigs
## The skills' own effects in the new art (rigs of scenes/world/effects): each skill that showed
## only dust, the same light as another skill or nothing at all gets its own. MapEffects draws them
## with the rest (show_effects()); MapPictures.skill_effects() says when. A frame of a kind that
## goes one way is its 8-direction * its steps + the step.
##   whirlwind:  Whirlwind Sabre, a ring of steel round him (4 steps, one way)
##   smash:      Storm Sabre, the blow from above and the shock where it lands (3, one way)
##   thrust:     Thunder Sabre, each thrust a crack of lightning ahead (8, one way)
##   spring:     Living Water, water rising round him (9)
##   fury:       Fury, flames of rage round him (6)
##   charm:      Charm, a ring of runes and a light winding round him (6)
##   surge:      Dnipro Wave, each blow throws a wave ahead (4, one way)
##   flood:      Flood, waves running ahead of him (6, one way)
##   fire_ring:  Ring of Fire, flames bursting out round him (6)
##   fire_whirl: Fire Whirl, fire winding up round him (6)
##   blaze:      Steppe Blaze, a ring of fire sweeping round him (8)
const SKILL_FRAMES := {
	"whirlwind": 32,
	"smash": 24,
	"thrust": 64,
	"spring": 9,
	"fury": 6,
	"charm": 6,
	"surge": 32,
	"flood": 48,
	"fire_ring": 6,
	"fire_whirl": 6,
	"blaze": 8,
}

## Flames round one in Fury and in Ring of Fire (as many as their scenes hold).
const FURY_FLAMES := 5
const RING_FLAMES := 8


## Vector2i(8-direction, step) of a frame of a kind that goes one way.
static func _way(frame: int, steps: int) -> Vector2i:
	return Vector2i(frame / steps, frame % steps)


## The rig stands where the skill is used, turned the way it goes.
static func _stand(rig: Node3D, p: Vector2, dir8: int, turn := 0.0) -> void:
	rig.position = _at(p)
	rig.rotation = Vector3(0.0, Motion.yaw_of(dir8) + turn, 0.0)


## Flames standing round the middle of the rig, r away, h high.
static func _flames(rig: Node3D, n: int, r: float, h: float, p: Vector2) -> void:
	for i in n:
		var a := i * TAU / n + 0.4
		var fh := h * (0.8 + 0.3 * sin(i * 2.3))
		var flame := rig.get_node("Flame%d" % i) as MeshInstance3D
		var at := Vector3(cos(a) * r, fh / 2.0, sin(a) * r * 0.8)
		_quad(flame, at, 0.75 * maxf(fh, 0.4), maxf(fh, 0.01))
		_tune(flame, {"seed": _seed(p, i), "toward": 0.45, "strength": 1.0 if fh > 0.05 else 0.0})


# ---- blades: Whirlwind Sabre, Storm Sabre, Thunder Sabre ---------------------------------


## The blade goes round him once, and the wind of it spreads on the ground.
func _draw_whirlwind(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var w := _way(frame, 4)
	var ph := _run(w.y, t, 4)
	_stand(rig, p, w.x)
	_tune(rig.get_node("Ring"), {"progress": ph, "strength": 1.0})
	_flat(rig.get_node("Gust"), Vector3.ZERO, 1.8 + 2.0 * ph)
	_tune(
		rig.get_node("Gust"),
		{"radius": 0.72, "width": 0.12, "count": 0.0, "strength": 0.7 - 0.6 * ph}
	)


## The blade comes down from above in front of him, and where it lands the ground cracks
## and a ring of shock and dust goes out.
func _draw_smash(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var w := _way(frame, 3)
	var ph := _run(w.y, t, 3)
	_stand(rig, p, w.x)
	_tune(rig.get_node("Arc"), {"progress": minf(0.2 + ph * 1.1, 1.0), "strength": 1.0})
	var hit := clampf((ph - 0.35) / 0.65, 0.0, 1.0)
	var front := Vector3(0.0, 0.0, 1.4)
	_flat(rig.get_node("Shock"), front, 0.8 + 3.2 * hit)
	_tune(
		rig.get_node("Shock"),
		{"radius": 0.72, "width": 0.1, "count": 0.0, "strength": (1.0 - hit) if hit > 0.0 else 0.0}
	)
	_flat(rig.get_node("Crack"), front, 2.4)
	_tune(rig.get_node("Crack"), {"count": 9.0, "seed": _seed(p), "strength": sin(PI * hit)})
	for i in 2:
		var dust := rig.get_node("Dust%d" % i) as MeshInstance3D
		_quad(dust, front + Vector3((i - 0.5) * 0.9, 0.3 + 0.6 * hit, 0.0), 0.8 + 0.9 * hit)
		_tune(dust, {"strength": 0.8 * sin(PI * hit), "seed": _seed(p, i)})


## Each thrust cracks off the point of the blade like thunder, left and right of him by turns.
func _draw_thrust(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var w := _way(frame, 8)
	var ahead := _ahead(w.x)
	var side := ahead.cross(Vector3.UP) * (0.15 if w.y % 2 == 0 else -0.15)
	var hand := _at(p) + Vector3(0.0, 1.0, 0.0) + ahead * 0.5 + side
	var tip := hand + ahead * (0.9 + 0.5 * t)
	var s := _seed(p, frame)
	var fade := 1.0 - 0.8 * t * t
	_span(rig.get_node("Bolt"), hand, tip, 0.6)
	_tune(rig.get_node("Bolt"), {"seed": s, "strength": fade})
	_span(rig.get_node("Fork"), tip, tip + ahead * 0.4 + side * 3.0 + Vector3(0.0, 0.4, 0.0), 0.4)
	_tune(rig.get_node("Fork"), {"seed": s + 1.0, "strength": 0.8 * fade})
	_quad(rig.get_node("Tip"), tip, 1.1)
	_tune(rig.get_node("Tip"), {"strength": fade, "toward": 0.3})
	_quad(rig.get_node("Crackle"), tip, 0.8 + 0.6 * t)
	_tune(rig.get_node("Crackle"), {"count": 7.0, "seed": s, "strength": fade, "toward": 0.35})


# ---- healing and blessings: Living Water, Fury, Charm ------------------------------------


## Water wells up round his feet and winds up round him.
func _draw_spring(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var ph := _run(frame, t, 9)
	var swell := _swell(ph)
	_stand(rig, p, 0)
	_pillar(rig.get_node("Spiral"), Vector3.ZERO, 0.65, 2.0)
	_tune(rig.get_node("Spiral"), {"count": 3.0, "progress": ph * 2.0, "strength": swell})
	_pillar(rig.get_node("Wall"), Vector3.ZERO, 0.8 + 0.25 * ph, 0.45 + 0.35 * sin(PI * ph))
	_tune(rig.get_node("Wall"), {"count": 18.0, "seed": _seed(p), "strength": 0.8 * swell})
	_pillar(rig.get_node("Drops"), Vector3.ZERO, 0.8, 2.4)
	_tune(rig.get_node("Drops"), {"count": 12.0, "strength": swell})
	_flat(rig.get_node("Ground"), Vector3.ZERO, 2.1)
	_tune(rig.get_node("Ground"), {"strength": 0.6 * swell})


## Flames of rage flare up round him and a red ring throbs on the ground.
func _draw_fury(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var ph := _run(frame, t, 6)
	var swell := _swell(ph, 0.2, 0.3)
	_stand(rig, p, 0)
	_flames(rig, FURY_FLAMES, 0.65, 1.6 * swell, p)
	_flat(rig.get_node("Ring"), Vector3.ZERO, 1.5 + 0.25 * sin(ph * TAU * 2.0))
	_tune(
		rig.get_node("Ring"),
		{"radius": 0.72, "width": 0.1, "count": 10.0, "seed": _seed(p), "strength": 0.8 * swell}
	)
	_flat(rig.get_node("Ground"), Vector3.ZERO, 2.3)
	_tune(rig.get_node("Ground"), {"strength": 0.6 * swell})


## A ring of runes turns on the ground and a violet light winds up round him.
func _draw_charm(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var ph := _run(frame, t, 6)
	var swell := _swell(ph)
	_stand(rig, p, 0, ph * PI)
	_flat(rig.get_node("Runes"), Vector3.ZERO, 2.1)
	_tune(
		rig.get_node("Runes"),
		{"radius": 0.7, "width": 0.07, "count": 14.0, "seed": 1.0, "strength": swell}
	)
	_pillar(rig.get_node("Spiral"), Vector3.ZERO, 0.55, 2.2)
	_tune(rig.get_node("Spiral"), {"count": 2.0, "progress": -ph * 2.0, "strength": 0.8 * swell})
	_pillar(rig.get_node("Motes"), Vector3.ZERO, 0.7, 2.3)
	_tune(rig.get_node("Motes"), {"count": 9.0, "strength": swell})
	_flat(rig.get_node("Ground"), Vector3.ZERO, 1.8)
	_tune(rig.get_node("Ground"), {"strength": 0.5 * swell})


# ---- water: Dnipro Wave, Flood -----------------------------------------------------------


## Each blow sweeps a wave of water before him that breaks in a splash.
func _draw_surge(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var w := _way(frame, 4)
	var ph := _run(w.y, t, 4)
	_stand(rig, p, w.x)
	_tune(rig.get_node("Wave"), {"progress": ph, "strength": 1.0})
	var front := Vector3(0.0, 0.0, 1.6)
	_pillar(rig.get_node("Splash"), front, 0.35 + 0.5 * ph, 0.2 + 0.8 * sin(PI * ph))
	_tune(rig.get_node("Splash"), {"count": 14.0, "seed": _seed(p, w.y), "strength": 1.0 - ph})
	_flat(rig.get_node("Ground"), front, 1.9)
	_tune(rig.get_node("Ground"), {"strength": 0.5 * (1.0 - ph)})


## Three waves, one after another, run ahead of him and break.
func _draw_flood(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var w := _way(frame, 6)
	var ph := _run(w.y, t, 6)
	_stand(rig, p, w.x)
	for i in 3:
		var d := clampf(ph * 1.4 - i * 0.2, 0.0, 1.0)
		var h := 1.1 * sin(PI * d) + 0.01
		var wave := rig.get_node("Wave%d" % i) as MeshInstance3D
		wave.transform = Transform3D(
			Basis.from_scale(Vector3(1.2, h, 0.35)), Vector3(0.0, h / 2.0, 0.8 + 3.5 * d)
		)
		_tune(wave, {"count": 16.0, "seed": _seed(p, i), "strength": sin(PI * d)})
	_flat(rig.get_node("Ground"), Vector3(0.0, 0.0, 0.8 + 2.0 * ph), 2.6)
	_tune(rig.get_node("Ground"), {"strength": 0.5 * _swell(ph)})


# ---- fire: Ring of Fire, Fire Whirl, Steppe Blaze ----------------------------------------


## Flames burst out of the ground round him and spread outwards in a ring.
func _draw_fire_ring(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var ph := _run(frame, t, 6)
	var r := 0.6 + 1.8 * smoothstep(0.0, 0.6, ph)
	var swell := _swell(ph, 0.1, 0.35)
	_stand(rig, p, 0)
	_flames(rig, RING_FLAMES, r, 1.3 * swell, p)
	_flat(rig.get_node("Ring"), Vector3.ZERO, 2.0 * r + 0.6)
	_tune(
		rig.get_node("Ring"),
		{"radius": 0.72, "width": 0.1, "count": 16.0, "seed": _seed(p), "strength": swell}
	)
	_flat(rig.get_node("Ground"), Vector3.ZERO, 2.0 * r + 1.0)
	_tune(rig.get_node("Ground"), {"strength": 0.5 * swell})


## Fire winds up round him in a whirl, faster and faster.
func _draw_fire_whirl(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var ph := _run(frame, t, 6)
	var swell := _swell(ph, 0.15, 0.2)
	_stand(rig, p, 0)
	_pillar(rig.get_node("Spiral"), Vector3.ZERO, 0.95, 2.6)
	_tune(rig.get_node("Spiral"), {"count": 3.0, "progress": ph * ph * 4.0, "strength": swell})
	_pillar(rig.get_node("Inner"), Vector3.ZERO, 0.6, 2.0)
	_tune(rig.get_node("Inner"), {"count": 2.0, "progress": -ph * 3.0, "strength": 0.8 * swell})
	_flat(rig.get_node("Ground"), Vector3.ZERO, 2.5)
	_tune(rig.get_node("Ground"), {"strength": 0.6 * swell})


## A ring of fire sweeps round him twice, scorching the ground, embers flying up.
func _draw_blaze(rig: Node3D, frame: int, p: Vector2, t: float, _behind: bool) -> void:
	var ph := _run(frame, t, 8)
	var swell := _swell(ph, 0.1, 0.2)
	_stand(rig, p, 0, -ph * TAU * 2.0)
	_tune(rig.get_node("Ring"), {"progress": 0.5, "strength": swell})
	_pillar(rig.get_node("Embers"), Vector3.ZERO, 1.3, 1.8)
	_tune(rig.get_node("Embers"), {"count": 14.0, "strength": swell})
	_flat(rig.get_node("Scorch"), Vector3.ZERO, 3.4)
	_tune(
		rig.get_node("Scorch"),
		{"radius": 0.72, "width": 0.12, "count": 12.0, "seed": _seed(p), "strength": 0.7 * swell}
	)
