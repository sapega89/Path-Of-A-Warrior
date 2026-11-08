"""Humanoid skeleton for every person in the game.

The skeleton and its animation clips come from the KayKit Adventurers pack (CC0,
Kay Lousberg). Its figures are chibi, so the bones are moved to adult proportions
(about 1.8 m): each bone keeps its direction and roll, only its head and length change,
so the joint rotations of every clip still fit. Hip translations are scaled with the leg
length. The IK helper bones are dropped; the clips already hold the baked result.
"""

import math

import bpy
from mathutils import Matrix, Vector

KNIGHT = "addons/kaykit_character_pack_adventures/Characters/gltf/Knight.glb"

# clip in the pack -> clip name in the game
CLIPS = {
    "Idle": "idle",
    "Unarmed_Idle": "idle_unarmed",
    "2H_Melee_Idle": "idle_2h",
    "Walking_A": "walk",
    "Walking_B": "walk_relaxed",
    "Walking_Backwards": "walk_back",
    "Running_A": "run",
    "Running_B": "run_relaxed",
    "1H_Melee_Attack_Chop": "attack_chop",
    "1H_Melee_Attack_Slice_Diagonal": "attack_slash",
    "1H_Melee_Attack_Slice_Horizontal": "attack_sweep",
    "1H_Melee_Attack_Stab": "attack_stab",
    "2H_Melee_Attack_Slice": "attack_2h_slash",
    "2H_Melee_Attack_Spin": "attack_spin",
    "2H_Melee_Attack_Stab": "attack_2h_stab",
    "2H_Ranged_Aiming": "aim_bow",
    "2H_Ranged_Shoot": "shoot_bow",
    "Block": "block",
    "Block_Hit": "block_hit",
    "Blocking": "blocking",
    "Hit_A": "hit",
    "Hit_B": "hit_heavy",
    "Death_A": "death",
    "Death_B": "death_back",
    "Dodge_Forward": "dodge",
    "Dodge_Backward": "dodge_back",
    "Cheer": "cheer",
    "Interact": "interact",
    "PickUp": "pick_up",
    "Sit_Floor_Idle": "sit",
    "Spellcast_Shoot": "cast",
    "Spellcast_Raise": "cast_raise",
    "Throw": "throw",
    "Use_Item": "use_item",
}

LOOPING = {"idle", "idle_unarmed", "idle_2h", "walk", "walk_relaxed", "walk_back", "run",
           "run_relaxed", "blocking", "sit", "aim_bow"}

DEFORM = [
    "root", "hips", "spine", "chest", "head",
    "upperarm.l", "lowerarm.l", "wrist.l", "hand.l", "handslot.l",
    "upperarm.r", "lowerarm.r", "wrist.r", "hand.r", "handslot.r",
    "upperleg.l", "lowerleg.l", "foot.l", "toes.l",
    "upperleg.r", "lowerleg.r", "foot.r", "toes.r",
]

# New placement. "head": explicit head position (left side; right mirrors x);
# "len": length multiplier. Bones without a head follow their parent's tail
# (or keep their offset from the parent's head when they did not start at its tail).
ADULT = {
    "hips": {"head": (0.0, 0.0, 0.87), "len": 1.0},
    "spine": {"len": 0.64},
    "chest": {"len": 0.956},
    "head": {"head": (0.0, 0.0, 1.56), "len": 1.0},
    "upperarm": {"head": (0.19, 0.0, 1.45), "len": 1.1},
    "lowerarm": {"len": 1.1},
    "wrist": {"len": 1.0},
    "hand": {"len": 0.9},
    "upperleg": {"head": (0.105, 0.0, 0.95), "len": 1.894},
    "lowerleg": {"len": 2.41},
    "foot": {"len": 1.148},
    "toes": {"len": 0.6},
}

# old hip-joint height 0.519 -> new 0.95
HIP_SCALE = 0.95 / 0.519

# The pack's clips hold the arms out wide to clear a chibi body. Turning the arm chains
# down by this angle at rest (an A-pose) lowers them in every clip by the same amount.
ARM_DROP_DEG = 22.0
ARM_CHAIN = ("upperarm", "lowerarm", "wrist", "hand", "handslot")


def arm_drop(side):
    """Rotation (about the front-back axis) that lowers the arm of `side` ("l" or "r")."""
    sign = 1.0 if side == "l" else -1.0
    return Matrix.Rotation(math.radians(ARM_DROP_DEG) * sign, 4, "Y")


def _spec(name):
    base = name.split(".")[0]
    spec = dict(ADULT.get(base, {}))
    if "head" in spec and name.endswith(".r"):
        x, y, z = spec["head"]
        spec["head"] = (-x, y, z)
    return spec


def _channelbags(action):
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                yield bag


def load(kaykit_root):
    """Import the pack's skeleton and clips, re-proportioned. Returns the armature."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=f"{kaykit_root}/{KNIGHT}")
    arm = bpy.data.objects["Rig"]
    for obj in list(bpy.data.objects):
        if obj is not arm:
            bpy.data.objects.remove(obj, do_unlink=True)
    for me in list(bpy.data.meshes):
        bpy.data.meshes.remove(me)
    if arm.animation_data:
        for track in list(arm.animation_data.nla_tracks):
            arm.animation_data.nla_tracks.remove(track)
        arm.animation_data.action = None

    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    ebs = arm.data.edit_bones
    for eb in list(ebs):
        if eb.name not in DEFORM:
            ebs.remove(eb)
    old = {eb.name: (eb.head.copy(), eb.tail.copy(), eb.matrix.copy(), eb.length) for eb in ebs}
    new_head, new_tail = {}, {}
    for name in DEFORM:
        eb = ebs[name]
        h0, t0, m0, l0 = old[name]
        spec = _spec(name)
        if "head" in spec:
            head = Vector(spec["head"])
        elif eb.parent is None:
            head = h0.copy()
        else:
            p = eb.parent.name
            ph0, pt0 = old[p][0], old[p][1]
            if (h0 - pt0).length < 1e-3:
                head = new_tail[p].copy()
            else:
                head = new_head[p] + (h0 - ph0)
        length = l0 * spec.get("len", 1.0)
        m = m0.copy()
        m.translation = head
        eb.matrix = m
        eb.length = length
        new_head[name] = eb.head.copy()
        new_tail[name] = eb.tail.copy()
    for side in ("l", "r"):
        pivot = ebs["upperarm." + side].head.copy()
        turn = Matrix.Translation(pivot) @ arm_drop(side) @ Matrix.Translation(-pivot)
        for part in ARM_CHAIN:
            eb = ebs[f"{part}.{side}"]
            length = eb.length
            eb.matrix = turn @ eb.matrix
            eb.length = length
    bpy.ops.object.mode_set(mode="OBJECT")

    keep = set(CLIPS)
    for action in list(bpy.data.actions):
        if action.name not in keep:
            bpy.data.actions.remove(action)
            continue
        for bag in _channelbags(action):
            for fc in list(bag.fcurves):
                bone = fc.data_path.split('"')[1] if '"' in fc.data_path else ""
                if bone and bone not in DEFORM:
                    bag.fcurves.remove(fc)
                    continue
                if bone == "hips" and fc.data_path.endswith("location"):
                    for k in fc.keyframe_points:
                        k.co[1] *= HIP_SCALE
                        k.handle_left[1] *= HIP_SCALE
                        k.handle_right[1] *= HIP_SCALE
        action.name = CLIPS[action.name]
        action.use_fake_user = True
    return arm


def bones(arm):
    """name -> (head, tail) in world space at rest."""
    mw = arm.matrix_world
    return {b.name: (mw @ b.head_local, mw @ b.tail_local) for b in arm.data.bones}


def strip_for_export(arm, with_clips):
    """Leave the clips on the armature's NLA (one track each) or drop them."""
    if not with_clips:
        if arm.animation_data:
            arm.animation_data.action = None
            for t in list(arm.animation_data.nla_tracks):
                arm.animation_data.nla_tracks.remove(t)
        return
    ad = arm.animation_data or arm.animation_data_create()
    for t in list(ad.nla_tracks):
        ad.nla_tracks.remove(t)
    for action in bpy.data.actions:
        track = ad.nla_tracks.new()
        track.name = action.name
        strip = track.strips.new(action.name, int(action.frame_range[0]), action)
        if action.slots:
            strip.action_slot = action.slots[0]
        track.mute = False
