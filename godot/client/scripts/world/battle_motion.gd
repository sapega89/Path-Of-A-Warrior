class_name BattleMotion
extends RefCounted
## Who a fighter of the multiplayer battle is in the new art, and which clip of the shared
## library he plays for each animation of scripts/net/online_battle.gd: [clip, mode, speed]
## as in scripts/world/motion.gd ("loop", "fit" over the animation's ticks, "once").
## A player is the model of his class (the hero's four) with his blade; the server's fighters
## are a rival Cossack, a Crown soldier or a Tatar (the same one for the same name), each with
## his own weapons; the monsters of Solo Mission are the forest upyr with a club.

const RIVALS := ["kozak_rival", "zholner", "tatar"]
const MONSTER := "upyr"
## Portraits (assets/art/portraits): the hero's classes from 38, the rivals, the upyr.
const HERO_PORTRAIT := 38
const RIVAL_PORTRAITS := [42, 43, 44]
const MONSTER_PORTRAIT := 45

## The animations of the battle (their numbers there) and the clips that show them.
const ANIMS := {
	0: ["idle", "loop", 1.0],
	1: ["hit", "once", 1.0],  # hit
	2: ["run", "loop", 2.0],  # the run to the target
	3: ["attack_slash", "fit", 1.0],  # a blow
	4: ["block_hit", "fit", 1.0],  # the blow taken on the guard
	5: ["dodge_back", "fit", 1.0],  # evaded
	6: ["death", "once", 0.8],  # falls
	8: ["idle_2h", "loop", 1.0],  # the ready pose before a skill
	9: ["attack_spin", "fit", 1.0],  # Whirlwind Sabre: a series of 3
	10: ["attack_2h_slash", "fit", 1.0],  # Storm Sabre
	11: ["attack_stab", "loop", 2.6],  # Thunder Sabre: thrust after thrust
	12: ["cast_raise", "fit", 1.0],  # Healing Herbs, Living Water
	13: ["cheer", "fit", 1.0],  # a soul: Fury, Charm, Protection of the Virgin
	14: ["attack_sweep", "loop", 2.2],  # Dnipro Wave: a series of 6
	15: ["attack_2h_slash", "fit", 1.0],  # Rapids
	16: ["attack_2h_stab", "fit", 1.0],  # Flood: two at once
	17: ["run", "loop", 1.6],  # into place for Dnipro Wave or Rapids
	18: ["run", "loop", 1.6],
	19: ["run", "loop", 1.6],
	20: ["cast_raise", "fit", 1.0],  # Flood gathers
	28: ["run", "loop", 2.0],  # back to his place
}
## Animations where he moves along the ground (he faces the way he goes).
const MOVING := [2, 17, 18, 19, 28]


## The model of fighter f (characters/<kind>.glb).
static func kind_of(f: RefCounted) -> String:
	match int(f.kind):
		OnlineBattle.PLAYER:
			return MapPeople.HEROES[clampi(int(f.face), 0, 3)]
		OnlineBattle.MONSTER:
			return MONSTER
	return RIVALS[_rival(f)]


## The weapons a player carries (his blade); the others keep the model's own.
static func weapons_of(f: RefCounted) -> Array:
	if int(f.kind) == OnlineBattle.PLAYER:
		return [MapPeople.BLADES[clampi(int(f.weapon), 0, 1)]]
	return []


static func portrait_of(f: RefCounted) -> int:
	match int(f.kind):
		OnlineBattle.PLAYER:
			return HERO_PORTRAIT + clampi(int(f.face), 0, 3)
		OnlineBattle.MONSTER:
			return MONSTER_PORTRAIT
	return RIVAL_PORTRAITS[_rival(f)]


## Which of the rivals a server's fighter is: the same one for the same name.
static func _rival(f: RefCounted) -> int:
	return posmod(String(f.name).hash(), RIVALS.size())


## The animation of fighter i now: his own while a round plays back, else standing (the
## battle keeps the last one it played).
static func anim_of(battle: RefCounted, i: int) -> int:
	return int(battle.fighters[i].anim) if int(battle.state) == OnlineBattle.TURN else 0


## Fighter i lies fallen (not while he falls).
static func fallen(battle: RefCounted, i: int) -> bool:
	return int(battle.fighters[i].hp) <= 0 and anim_of(battle, i) != 6


## The clip of fighter i now: [clip, mode, speed]. The fallen lie as at the end of a fall.
static func motion(battle: RefCounted, i: int) -> Array:
	var f: RefCounted = battle.fighters[i]
	var anim := anim_of(battle, i)
	if fallen(battle, i):
		return ANIMS[6]
	if anim == 3 and int(f.kind) == OnlineBattle.MONSTER:
		return ["attack_chop", "fit", 1.0]  # the club comes down
	return ANIMS.get(anim, ANIMS[0])


## How far fighter i is into his animation: [ticks done, ticks it lasts].
static func progress(battle: RefCounted, i: int) -> Vector2i:
	var f: RefCounted = battle.fighters[i]
	var anim := anim_of(battle, i)
	if anim in [1, 4, 5] and i != int(battle.attacker):
		return Vector2i(int(f.anim_tick), maxi(1, int(f.anim_len)))
	if i == int(battle.attacker) and int(battle.state) == OnlineBattle.TURN:
		return Vector2i(int(battle.anim_frame), maxi(1, int(battle.anim_length)))
	return Vector2i(0, 1)
