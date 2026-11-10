class_name BattleStage
extends Node3D
## The stage of the online battle (World/Viewport/Stage of the battle screen): the field
## (Arena), the fighters as the maps' people (Fighter0..3, scripts/world/battle_motion.gd: who
## is who, which clip shows each animation of the battle), the effects of the missions on them
## (Effects, scripts/world/map_effects.gd), the chevron over the target (Target) and the camera.
## show_fighters puts everyone where the battle's step has them; move_fighters walks and turns
## them smoothly between the steps. A blow that lands shakes the view.

## World units per pixel of the battle (online_battle.gd's 240×320 field): one 27 px map tile
## is one unit, as on the map.
const PX := 1.0 / 27.0
## The battle's ground line where the fighters of a 1-on-1 stand.
const GROUND_Y := 225
const TICK := OnlineBattle.TICK_MS / 1000.0
const CAMERA_AT := Vector3(0, 2.2, 10.2)
const CAMERA_TO := Vector3(0, 1.2, 0)
## The people stand a little taller than on the maps: the battle is seen closer.
const FIGURE_SCALE := 1.18
## How quickly a figure turns to its new direction (1/s).
const TURN := 14.0
const MARKER_UP := 2.6  # the target's chevron over the feet (world units)
const SHAKE := 0.07  # how far a blow that lands shakes the view (world units)
const HIT_FLASH := Color(0.8, 0.16, 0.12)  # the flash of one who is hit: blood-red
## The rows of a 2-on-2 stand apart in depth; seen from the camera the back one would hide
## behind the front one, so the farther a fighter stands the farther out from the middle it
## is drawn (by this part of its distance from the middle per pixel of depth).
const SPREAD := 0.016
## The chevron over the target: brass over blood-red, inked.
# gdlint:ignore = max-line-length
const MARKER_SVG := '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 72"><path d="M8 6 L32 26 L56 6 L56 20 L32 40 L8 20 Z" fill="#b89550" stroke="#0f0d0c" stroke-width="3.5" stroke-linejoin="round"/><path d="M14 34 L32 49 L50 34 L50 45 L32 62 L14 45 Z" fill="#8a2b25" stroke="#0f0d0c" stroke-width="3.5" stroke-linejoin="round"/></svg>'

var battle: RefCounted  # what is shown (scripts/net/online_battle.gd)
var bodies: Array[Node3D] = []  # Fighter0..3: where each fighter stands
var figures: Array = [null, null, null, null]  # the ArtFigure of each
var clock := 0.0  # seconds the battle has been shown (the screen moves it on)
var _looks := ["", "", "", ""]  # what each figure was made for
var _last: Array[Vector2i] = []  # [animation, ticks into it] of each fighter drawn last
var _from: Array[Vector3] = []  # where each stood at the step before and stands now
var _to: Array[Vector3] = []
var _yaw: Array[float] = []
var _fx: Array = []  # the effects of this step (MapEffects.show_effects)
var _fallen_at: Array[float] = [-1.0, -1.0, -1.0, -1.0]  # when each was first seen lying (clock)
var _shake := 0.0  # how hard the view shakes from a blow (world units), dying away

@onready var arena: BattleArena = $Arena
@onready var camera: Camera3D = $Camera
@onready var effects: MapEffects = $Effects
@onready var marker: Sprite3D = $Target


func _ready() -> void:
	camera.look_at_from_position(CAMERA_AT, CAMERA_TO, Vector3.UP)
	for i in 4:
		bodies.append(get_node("Fighter%d" % i) as Node3D)
		_last.append(Vector2i(-1, 0))
		_from.append(Vector3.ZERO)
		_to.append(Vector3.ZERO)
		_yaw.append(0.0)
	var img := Image.new()
	img.load_svg_from_string(MARKER_SVG, 1.5)
	marker.texture = ImageTexture.create_from_image(img)


## Where a fighter's feet are: the battle's (x, y), with a leap's height kept apart.
static func world_at(sx: float, gy: float, lift: float) -> Vector3:
	var out := 1.0 + (GROUND_Y - gy) * SPREAD
	return Vector3((sx - OnlineBattle.CX) * out * PX, lift * PX, (gy - GROUND_Y) * PX)


## The figure of fighter i, made again when someone else stands in his place.
func _figure(i: int, f: RefCounted) -> Node3D:
	var kind := BattleMotion.kind_of(f)
	var weapons := BattleMotion.weapons_of(f)
	var look := "%s %s" % [kind, weapons]
	if figures[i] != null and _looks[i] == look:
		return figures[i]
	if figures[i] != null:
		figures[i].free()
	var fig: Node3D = ArtFigure.new()
	fig.name = "Figure"
	bodies[i].add_child(fig)
	fig.setup(kind)
	fig.scale = Vector3.ONE * FIGURE_SCALE
	fig.drive_manually()
	if not weapons.is_empty():
		fig.unequip_all()
		for w in weapons:
			fig.equip(w)
	figures[i] = fig
	_looks[i] = look
	_last[i] = Vector2i(-1, 0)
	return fig


## The fighters at this step: each figure's place, the way it faces, its clip; the effects on
## them; the chevron over the target. Still (the screen does not move its clips on), each
## shows at once, without blending; part_of_step: how far the screen is to the next step.
func show_fighters(still: bool, part_of_step: float) -> void:
	_fx.clear()
	var places: Array[Vector3] = []
	for i in 4:
		var f: RefCounted = battle.fighters[i]
		var sx: float = (OnlineBattle.W - f.x) if f.mirrored() else f.x
		places.append(world_at(sx, f.y + f.lift, f.lift))
	for i in 4:
		var f: RefCounted = battle.fighters[i]
		bodies[i].visible = f.present
		if not f.present:
			continue
		var fig := _figure(i, f)
		var fresh := _last[i].x < 0  # just came: stands in his place at once
		var to := places[i]
		_from[i] = _to[i] if _to[i].distance_to(to) < 2.5 and not fresh else to
		_to[i] = to
		var anim := BattleMotion.anim_of(battle, i)
		_yaw[i] = _heading(i, f, anim, places)
		var motion: Array = BattleMotion.motion(battle, i)
		var p := BattleMotion.progress(battle, i)
		var restart := anim != _last[i].x or p.x < _last[i].y
		if restart and anim == 1 and not still:
			_shake = maxf(_shake, SHAKE)  # a blow that lands shakes the view
		_last[i] = Vector2i(anim, p.x)
		var part := float(p.x) / float(p.y)
		if BattleMotion.fallen(battle, i):
			# the fall plays on to its end; seen only now, he lies at once
			if fig.shown_clip != "death":
				fig.act(motion, 0.0, true, 1.0, 0.0)
		else:
			if f.hp > 0 and fig.shown_clip == "death":
				fig.shown_clip = ""  # up again: a new stage
			fig.act(motion, p.y * TICK, restart, part, 0.0 if still else ArtFigure.BLEND)
		fig.flash(0.4 * (1.0 - clampf(part, 0.0, 1.0)) if anim == 1 else 0.0, HIT_FLASH)
		if still or fresh:
			bodies[i].position = to
			bodies[i].rotation.y = _yaw[i]
		_effects_of(i, f, anim, to, p, still)
	marker.visible = false
	if battle.state == OnlineBattle.TARGET:
		var t: int = battle.target_cursor
		if battle.fighters[t].present:
			marker.visible = true
			marker.position = _to[t] + Vector3(0, MARKER_UP, 0)
	effects.show_effects(_fx, part_of_step)


## The way fighter i faces: towards the other side; running in, at his target; running back,
## to his place; moving into place for a skill, the way he goes.
func _heading(i: int, f: RefCounted, anim: int, places: Array[Vector3]) -> float:
	var way := Vector3(1.0 if f.team() == 0 else -1.0, 0.0, 0.0)
	match anim:
		2:
			var t: int = battle.target
			if t >= 0 and t != i:
				way = places[t] - places[i]
		28:
			var row_y: int = (
				OnlineBattle.CY + 65 + (0 if battle.mode == 0 else (-23 if f.row() == 0 else 23))
			)
			way = world_at(42.0 if f.team() == 0 else OnlineBattle.W - 42.0, row_y, 0.0) - places[i]
		17, 18, 19:
			if (places[i] - _from[i]).length() > 0.01:
				way = places[i] - _from[i]
	if Vector2(way.x, way.z).length() < 0.05:
		way = Vector3(1.0 if f.team() == 0 else -1.0, 0.0, 0.0)
	return atan2(way.x, way.z)


## The effects on fighter i (feet at `at`): the trail of his blade while he strikes, healing or
## a soul's light, sparks where a blow lands on him, dust when he dodges, his aura.
func _effects_of(i: int, f: RefCounted, anim: int, at: Vector3, p: Vector2i, still: bool) -> void:
	var px := Vector2(at.x / PX, at.z / PX - MapPeople.FOOT_PX)
	var ahead := 6 if f.team() == 0 else 2  # the way he faces, of the map's 8
	if i == battle.attacker and battle.state == OnlineBattle.TURN:
		match anim:
			3, 9, 10, 11, 14, 15, 16:
				var blow := 0
				match anim:
					3:
						blow = 2 if f.kind == OnlineBattle.MONSTER else 0
					10:
						blow = 2
					15:
						blow = 1
					16:
						blow = 0
					_:
						blow = (p.x / 2) % 3
				_fx.append(["trail", (ahead >> 1) * 3 + blow, px])
			12:
				_fx.append(["heal", mini(p.x * 9 / p.y, 8), px])
			13:
				_fx.append(["buff", mini(p.x * 6 / p.y, 5), px])
	match anim:
		1:
			# blood: the drops fly away from the blow, to his own side
			_fx.append(["blood", (4 if f.team() == 1 else 8) + 2 + mini(p.x, 1), px])
		4:
			_fx.append(["spark", mini(p.x, 1), px])  # steel on the guard
		5:
			_fx.append(["slash", ((ahead + 4) % 8) | mini(p.x, 1), px])
	if BattleMotion.fallen(battle, i):
		# blood spreads under the fallen (he lies on his back, his chest behind his feet) and stays;
		# a still screen shows it spread
		if _fallen_at[i] < 0.0:
			_fallen_at[i] = clock
		var spread := 7 if still else clampi(int((clock - _fallen_at[i]) / 0.25), 0, 7)
		var chest := px - Vector2(1.0 if f.team() == 0 else -1.0, 0.0) * 0.8 / PX
		_fx.append(["pool", spread, chest, true])
	else:
		_fallen_at[i] = -1.0
	if f.status in [11, 12, 13] and battle.state != OnlineBattle.RESULT:
		_fx.append(["aura", battle.state_ticks % 3, px, true])


## Between the steps: the figures walk on to where the next step puts them, turn, and play
## their clips; the effects run on; the chevron bobs.
func move_fighters(delta: float, part_of_step: float) -> void:
	for i in 4:
		if not bodies[i].visible or figures[i] == null:
			continue
		bodies[i].position = _from[i].lerp(_to[i], part_of_step)
		bodies[i].rotation.y = lerp_angle(bodies[i].rotation.y, _yaw[i], 1.0 - exp(-TURN * delta))
		figures[i].advance(delta)
	effects.show_effects(_fx, part_of_step)
	if marker.visible:
		marker.position.y = MARKER_UP + 0.08 * sin(clock * 6.0)
	camera.h_offset = _shake * sin(clock * 71.0)
	camera.v_offset = _shake * 0.6 * sin(clock * 53.0 + 1.3)
	_shake = move_toward(_shake, 0.0, delta * SHAKE * 4.0)
