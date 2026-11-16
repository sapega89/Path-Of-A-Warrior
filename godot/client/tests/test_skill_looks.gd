extends "res://tests/test_case.gd"
## How the skills look in a mission (scripts/world/motion.gd, skill_effects.gd,
## scripts/sim/map_pictures.gd): each skill has its own move and its own effect, the hero's
## and a general's alike.

const SKILL_IDS := [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
## The skills that got an effect of their own: skill -> its kind.
const OWN := {
	12: "whirlwind",
	13: "smash",
	14: "thrust",
	16: "spring",
	17: "fury",
	18: "charm",
	20: "surge",
	22: "flood",
	23: "fire_ring",
	24: "fire_whirl",
	25: "blaze",
}


func _kinds(list: Array) -> Array:
	var out: Array = []
	for e in list:
		out.append(str(e[0]))
	return out


func test_every_skill_moves_its_own_way() -> void:
	var lib := ArtKit.clips()
	var seen := {}
	for s in SKILL_IDS:
		var m := Motion.hero(s)
		check(lib.has_animation(m[0]), "skill %d: clip %s" % [s, m[0]])
		var move := "%s %s" % [m[0], m[3] if m.size() > 3 else m[1]]
		check(not seen.has(move), "skill %d moves as skill %s: %s" % [s, seen.get(move), move])
		seen[move] = s
	eq(Motion.body_pose(Motion.hero(3), 0.5), Vector3.ZERO, "a blow moves only the clip")
	eq(Motion.body_pose(Motion.hero(13), 0.0), Vector3.ZERO, "a leap starts on the ground")
	check(Motion.body_pose(Motion.hero(13), 0.3).x > 0.7, "Storm Sabre leaps high")
	check(is_zero_approx(Motion.body_pose(Motion.hero(13), 1.0).x), "and lands")
	check(Motion.body_pose(Motion.hero(28), 0.5).x > 0.3, "Thunderstorm lifts him up")
	check(Motion.body_pose(Motion.hero(12), 0.5).z > 0.15, "Whirlwind Sabre leans into it")
	check(
		is_equal_approx(Motion.body_pose(Motion.hero(24), 1.0).y, TAU),
		"Fire Whirl turns him round once more, ending as he began"
	)
	eq(
		Motion.body_pose(Motion.enemy(5, 7), 0.3),
		Motion.body_pose(Motion.hero(13), 0.3),
		"a general"
	)


func test_the_figure_carries_the_move() -> void:
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	var people := MapPeople.new()
	root.add_child(people)
	people.setup(sim, 0)
	var body: Node3D = people.hero.body
	sim.hero.action = 13
	sim.hero.frame = 2
	people.update(0.5, 0.05, 0.12, null)
	check(body.position.y > 0.5, "Storm Sabre: up in the air (%.2f)" % body.position.y)
	sim.hero.action = 0
	sim.hero.frame = 0
	people.update(0.5, 0.05, 0.12, null)
	eq(body.position, Vector3.ZERO, "standing: on the ground")
	eq(body.rotation, Vector3.ZERO, "and upright")
	people.free()


func test_every_frame_of_the_skills_own_effects_is_drawn() -> void:
	var fx: Node3D = MapEffects.new()
	root.add_child(fx)
	for kind in SkillEffects.SKILL_FRAMES:
		for frame in int(SkillEffects.SKILL_FRAMES[kind]):
			for t in [0.0, 0.5, 1.0]:
				fx.show_effects([[kind, frame, Vector2i(100, 100)]], t)
				eq(fx.shown(), 1, "%s %d at %.1f" % [kind, frame, t])
				var shown := 0
				for c in fx.drawn[0][2].get_children():
					shown += 1 if (c as Node3D).visible else 0
				check(shown > 0, "%s %d at %.1f shows something" % [kind, frame, t])
	fx.show_effects([["whirlwind", 32, Vector2i(100, 100)]])
	eq(fx.shown(), 0, "a frame past the end: nothing")
	fx.free()


func test_every_skill_shows_its_own_effect() -> void:
	for s in OWN:
		var seen := {}
		for f in Motion.ticks(MapAnims.hero_anim(s, 6)):
			var out: Array = []
			MapPictures.skill_effects(s, f, Vector2i(100, 100), 6, out)
			for e in out:
				seen[str(e[0])] = true
				check(
					int(e[1]) < int(SkillEffects.SKILL_FRAMES[e[0]]),
					"skill %d frame %d: %s in range" % [s, f, e]
				)
		eq(seen.keys(), [OWN[s]], "skill %d" % s)
	var out: Array = []
	MapPictures.skill_effects(12, 3, Vector2i(100, 100), 6, out)
	eq(out, [["whirlwind", 6 * 4 + 1, Vector2i(100, 100)]], "the way he faces is in the frame")


func test_the_hero_and_a_general_show_them() -> void:
	var sim: RefCounted = MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	sim.hero.action = 16
	sim.hero.frame = 6
	var kinds := _kinds(MapPictures.effects(sim))
	check("spring" in kinds and not "heal" in kinds, "Living Water is water: %s" % [kinds])
	sim.hero.action = 15
	check("heal" in _kinds(MapPictures.effects(sim)), "Healing Herbs keep the herbs")
	sim.hero.action = 17
	kinds = _kinds(MapPictures.effects(sim))
	check("fury" in kinds and not "buff" in kinds, "Fury burns: %s" % [kinds])
	sim.hero.action = 19
	check("buff" in _kinds(MapPictures.effects(sim)), "Protection keeps its light from above")
	sim.hero.action = 0
	var general := MapActor.new()
	general.type = 5
	general.pos = Vector2i(120, 90)
	general.dir = 2
	general.action = 14  # the hero's 20, Dnipro Wave
	general.frame = 1
	sim.enemies.append(general)
	eq(
		MapPictures.effects(sim).filter(func(e: Array) -> bool: return e[0] == "surge"),
		[["surge", 2 * 4 + 1, Vector2i(120, 90)]],
		"a general's Dnipro Wave"
	)
