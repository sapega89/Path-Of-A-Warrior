class_name MapAnims
extends RefCounted
## The animation tables of the hero and the enemies: the frames of each action, the picture shown
## now.
## Static functions over the state of a MapSim (MapSim.tick() runs them).


## The hero's frame list for an action and 8-direction (as the original builds hero.anims).
static func hero_anim(action: int, dir8: int) -> Array:
	var dir4: int = int(MapSim.table("dir8_to_dir4")[dir8])
	var names := {
		0: "hero_anim_0",
		1: "hero_anim_1",
		2: "hero_anim_2",
		9: "hero_anim_9",
		3: "hero_anim_3",
		4: "hero_anim_4",
		5: "hero_anim_5",
		6: "hero_anim_6",
		7: "hero_anim_7",
		8: "hero_anim_8",
		11: "hero_anim_11",
		12: "hero_anim_12",
		13: "hero_anim_13",
		14: "hero_anim_14",
		20: "hero_anim_20",
		21: "hero_anim_21",
		22: "hero_anim_22",
		25: "hero_anim_25",
		26: "hero_anim_26_27",
		27: "hero_anim_26_27"
	}
	var flat := {
		10: "hero_anim_10",
		15: "hero_anim_15_19",
		16: "hero_anim_15_19",
		17: "hero_anim_15_19",
		18: "hero_anim_15_19",
		19: "hero_anim_15_19",
		23: "hero_anim_23_24",
		24: "hero_anim_23_24",
		28: "hero_anim_28",
		29: "hero_anim_29",
		30: "hero_anim_30"
	}
	if names.has(action):
		return MapSim.table(names[action])[dir4]
	if flat.has(action):
		return MapSim.table(flat[action])
	return [0, 222]


## How many actions an enemy has (its animation table's size).
static func enemy_actions(e: MapActor) -> int:
	return 22 if e.type < 200 else 4


## An enemy's frame list for its action. Soldiers: 0 walk, 1 attack, 2 hurt, 3 dying;
## generals: the same, 4 and 5 strikes, 6..21 skills (the hero's skill animations).
static func enemy_anim(e: MapActor, action: int) -> Array:
	var dir4 := int(MapSim.table("dir8_to_dir4")[e.dir])
	if e.type > 200:
		var prefix := "body_anim_" if e.type == MapSim.KIND_ARCHERS else "head_anim_"
		return MapSim.table(prefix + str(clampi(action, 0, 3)))[dir4]
	match clampi(action, 0, 21):
		0:
			return MapSim.table("head_anim_0")[dir4]
		1, 4, 5:
			return MapSim.table("weapon_anim_1")[dir4]
		2:
			return MapSim.table("weapon_anim_2")[dir4]
		3:
			return MapSim.table("weapon_anim_3")
		6:
			return MapSim.table("hero_anim_12")[dir4]
		7:
			return MapSim.table("hero_anim_13")[dir4]
		8:
			return MapSim.table("hero_anim_14")[dir4]
		9, 10, 11, 12, 13:
			return MapSim.table("hero_anim_15_19")
		14:
			return MapSim.table("hero_anim_20")[dir4]
		15:
			return MapSim.table("hero_anim_21")[dir4]
		16:
			return MapSim.table("hero_anim_22")[dir4]
		17, 18:
			return MapSim.table("hero_anim_23_24")
		19:
			return MapSim.table("hero_anim_25")[dir4]
	return MapSim.table("hero_anim_26_27")[dir4]


## The sprite frame an enemy shows now; 100 and more is not drawn (the dying blink).
static func enemy_sprite_frame(e: MapActor) -> int:
	var anim := enemy_anim(e, e.action)
	return int(anim[clampi(e.frame, 0, anim.size() - 1)])


## The sprite frame the hero shows now.
static func hero_sprite_frame(sim: MapSim) -> int:
	var anim := hero_anim(sim.hero.action, sim.hero.shown_dir)
	var f := clampi(sim.hero.frame, 0, anim.size() - 1)
	var v := int(anim[f])
	return v if v <= MapSim.END else int(anim[0])
