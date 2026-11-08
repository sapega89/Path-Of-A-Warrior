extends Node3D
## The people of a mission in the new art: the hero and the enemies of MapSim as 3D figures
## (scripts/art/art_figure.gd) on their places, turned their way and playing the clip of
## their action (scripts/world/motion.gd) in time with the ticks. A hit flashes them and
## knocks them off their place as CombatFeel says; a hit that holds the picture holds their
## clips too. The hero's look follows his class and his blade; an enemy's follows the side
## of the mission's general (assets/art/people.json): the Crown, the horde or Cossacks of a
## rival colonel, swordsmen, archers and squads of three.

const MapSim := preload("res://scripts/sim/map_sim.gd")
const Motion := preload("res://scripts/world/motion.gd")
const ArtFigure := preload("res://scripts/art/art_figure.gd")
const PEOPLE_PATH := "res://assets/art/people.json"
const PX := 1.0 / 27.0  # world units per map pixel (a tile is 27 px)
const FOOT_PX := 6  # the original's body box reaches this far below the position

## The hero's model by his class (Profile.HERO_CLASSES) and his blade by its kind.
const HEROES := ["kozak", "serdiuk", "kharakternyk", "haidamaka"]
const BLADES := ["sabre", "palash"]
## Swordsmen and archers of each side, and its generals.
const SOLDIERS := {
	"crown": ["zholner", "luchnyk"],
	"horde": ["tatar", "tatar_luk"],
	"cossack": ["kozak_rival", "kozak_rival_luk"],
}
const GENERALS := {"crown": "rotmistr", "horde": "murza", "cossack": "polkovnyk"}
## How quickly a figure turns to its new direction (1/s).
const TURN := 16.0

static var _sides: Dictionary = {}

var sim: RefCounted
var hero: Node3D  # an ArtFigure
var side := "crown"  # whose soldiers the mission's are
var enemies := {}  # sim actor -> Node3D holding 1 figure (3 for a squad)
var _state := {}  # sim actor -> [action, frame] of the last tick drawn
var _hero_look := Vector2i(-1, -1)


## The side of a general by his id ("crown", "horde" or "cossack").
static func side_of(general_id: int) -> String:
	if _sides.is_empty():
		var f := FileAccess.open(PEOPLE_PATH, FileAccess.READ)
		if f != null:
			var data: Variant = JSON.parse_string(f.get_as_text())
			if typeof(data) == TYPE_DICTIONARY:
				_sides = data.get("generals", {})
	return String(_sides.get(str(general_id), "crown"))


## The side of the general the sim met last (it keeps his data, not his id).
static func side_of_general(general: Dictionary) -> String:
	var name := String(general.get("name", ""))
	for gid in range(1, 400):
		var g := MapSim.general_data(gid)
		if g.is_empty():
			break
		if String(g.get("name", "")) == name:
			return side_of(gid)
	return "crown"


## The original pixel position to the world (the feet: FOOT_PX below the position).
static func to_world(p: Vector2) -> Vector3:
	return Vector3(p.x * PX, 0.0, (p.y + FOOT_PX) * PX)


func setup(map_sim: RefCounted, hero_class: int) -> void:
	sim = map_sim
	side = side_of(int(sim.mission_general)) if int(sim.mission_general) > 0 else "crown"
	set_hero_look(hero_class, int(sim.hero.weapon_kind))


## The hero's class (0..3) and blade kind (0 sabre, 1 palash).
func set_hero_look(hero_class: int, weapon_kind: int) -> void:
	var look := Vector2i(clampi(hero_class, 0, 3), clampi(weapon_kind, 0, 1))
	if look == _hero_look:
		return
	_hero_look = look
	var at := Vector3.ZERO
	var yaw := 0.0
	if hero != null:
		at = hero.position
		yaw = hero.rotation.y
		hero.free()
	hero = _figure(HEROES[look.x], [BLADES[look.y]])
	hero.name = "Hero"
	hero.position = at
	hero.rotation.y = yaw
	_state.erase(sim.hero)


func _figure(kind: String, weapons: Array) -> Node3D:
	var f: Node3D = ArtFigure.new()
	add_child(f)
	f.setup(kind)
	f.drive_manually()
	if not weapons.is_empty():
		f.unequip_all()
		for w in weapons:
			f.equip(w)
	return f


## Draws the state between the last two ticks: t 0..1 of the way, dt seconds the clips
## move on (0 while a hit holds the picture), tick seconds per tick, feel: CombatFeel.
func update(t: float, dt: float, tick: float, feel: RefCounted) -> void:
	var h: RefCounted = sim.hero
	hero.position = to_world(_smooth(h.prev_pos, h.pos, t))
	var speed := _ground_speed(h, tick)
	_drive(hero, h, Motion.hero(h.action, speed), MapSim.hero_anim(h.action, h.shown_dir), t, dt, tick)
	_turn(hero, Motion.yaw_of(h.shown_dir), dt)
	_flash(hero, h, feel)
	_place_enemies(t, dt, tick, feel)


func _place_enemies(t: float, dt: float, tick: float, feel: RefCounted) -> void:
	for e in enemies.keys():
		if not sim.enemies.has(e):
			enemies[e].queue_free()
			enemies.erase(e)
			_state.erase(e)
	var map4: Array = MapSim.table("dir8_to_dir4")
	for e in sim.enemies:
		var node: Node3D = enemies.get(e)
		if node == null:
			node = _enemy_node(e)
			enemies[e] = node
		# a knock-back (a long step while hit) goes out fast and slows down
		var knocked: bool = e.action == 2 and (e.pos - e.prev_pos).length() > 8
		var o: Vector3 = feel.offset_of(e) if feel != null else Vector3.ZERO
		var k: float = feel.knock_t(t) if knocked and feel != null else t
		node.position = to_world(_smooth(e.prev_pos, e.pos, k) + Vector2(o.x, o.y)) + Vector3(0.0, o.z * PX, 0.0)
		var frame: int = sim.enemy_sprite_frame(e)
		node.visible = frame < (180 if e.type < 200 else 100)
		var motion := Motion.enemy(e.type, e.action, _ground_speed(e, tick), knocked)
		var anim: Array = sim.enemy_anim(e, e.action)
		var restart := _restarted(e)
		var dir4 := int(map4[e.dir])
		for i in node.get_child_count():
			var fig := node.get_child(i) as Node3D
			_act(fig, e, motion, anim, t, tick, restart)
			fig.advance(dt)
			_turn(fig, Motion.yaw_of(e.dir), dt)
			_flash(fig, e, feel)
			if e.type == MapSim.KIND_SQUAD:
				var offsets: Array = MapSim.table("squad_offsets")
				if dir4 < offsets.size():
					var so: Array = offsets[dir4][i]
					fig.position = Vector3(float(so[0]) * PX, 0.0, float(so[1]) * PX)
		_state[e] = [e.action, e.frame]


func _enemy_node(e: RefCounted) -> Node3D:
	var node := Node3D.new()
	node.name = "Enemy"
	add_child(node)
	var kind: String
	if e.type < 200:
		kind = GENERALS[side_of_general(sim.general)]
	else:
		kind = SOLDIERS[side][1 if e.type == MapSim.KIND_ARCHERS else 0]
	for i in (3 if e.type == MapSim.KIND_SQUAD else 1):
		var f: Node3D = ArtFigure.new()
		node.add_child(f)
		f.setup(kind)
		f.drive_manually()
		f.rotation.y = Motion.yaw_of(e.dir)
	return node


func _drive(fig: Node3D, a: RefCounted, motion: Array, anim: Array, t: float, dt: float, tick: float) -> void:
	_act(fig, a, motion, anim, t, tick, _restarted(a))
	_state[a] = [a.action, a.frame]
	fig.advance(dt)


func _act(fig: Node3D, a: RefCounted, motion: Array, anim: Array, t: float, tick: float, restart: bool) -> void:
	var n := Motion.ticks(anim)
	var progress := clampf((float(a.frame) + t) / float(n), 0.0, 1.0) if restart else 0.0
	fig.act(motion, n * tick, restart, progress)


## The action began (again) since the last tick drawn.
func _restarted(a: RefCounted) -> bool:
	var last: Array = _state.get(a, [-1, 0])
	return int(last[0]) != a.action or a.frame < int(last[1])


## Turns smoothly while the clips move; a still picture shows the direction at once.
func _turn(fig: Node3D, yaw: float, dt: float) -> void:
	if dt <= 0.0:
		fig.rotation.y = yaw
	else:
		fig.rotation.y = lerp_angle(fig.rotation.y, yaw, 1.0 - exp(-TURN * dt))


func _flash(fig: Node3D, a: RefCounted, feel: RefCounted) -> void:
	var f: Array = feel.flash_of(a) if feel != null else [0.0, Color.WHITE]
	fig.flash(float(f[0]), f[1])


## m/s the actor moved over the last tick.
func _ground_speed(a: RefCounted, tick: float) -> float:
	var d: Vector2i = a.pos - a.prev_pos
	if d.length() > 40:
		return 0.0
	return d.length() * PX / maxf(tick, 0.001)


## The position between the last two ticks (a jump, such as a new room, is not smoothed).
static func _smooth(prev: Vector2i, now: Vector2i, t: float) -> Vector2:
	if (now - prev).length() > 40:
		return Vector2(now)
	return Vector2(prev).lerp(Vector2(now), clampf(t, 0.0, 1.0))
