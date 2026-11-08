"""Weapons and shields. Each one is a separate mesh held by a hand bone, so a
character can change weapons without a new body. Built at rest pose around the
hand slots: the right slot holds blades pointing forward (-Y), the left slot holds
shields and bows.
"""

import math

from mathutils import Matrix, Vector

import rig
from mesh_kit import MeshKit

# weapon -> bone that holds it
SLOTS = {
    "sabre": "handslot.r",
    "sabre_gold": "handslot.r",
    "palash": "handslot.r",
    "kalkan": "handslot.l",
    "bulava": "handslot.r",
    "spear": "handslot.r",
    "shield": "handslot.l",
    "bow": "handslot.l",
}


def sabre(k, s, gold=False):
    metal = "gold" if gold else "steel"
    k.ball(s + Vector((0, 0.1, 0.004)), (0.02, 0.026, 0.022), metal)
    k.tube(s + Vector((0, 0.095, 0)), s + Vector((0, -0.035, 0)), 0.017, 0.019, "chernozem" if not gold else "cinnabar_dark", segs=8)
    k.beam(s + Vector((0, -0.045, 0.055)), s + Vector((0, -0.045, -0.06)), 0.022, 0.018, metal)
    k.ball(s + Vector((0, -0.045, -0.065)), 0.014, metal, segs=6, rings=4)
    pts, widths = [], []
    n = 7
    for i in range(n + 1):
        t = i / n
        pts.append(s + Vector((0, -0.05 - 0.82 * t, 0.012 + 0.13 * t * t)))
        widths.append(0.046 * (1.0 - 0.25 * t) if i < n else 0.004)
    k.blade(pts, widths, 0.012, "steel_light")


def palash(k, s):
    # a straight broadsword with a knuckle guard
    k.ball(s + Vector((0, 0.1, 0.004)), (0.022, 0.028, 0.024), "steel")
    k.tube(s + Vector((0, 0.095, 0)), s + Vector((0, -0.035, 0)), 0.018, 0.02, "leather", segs=8)
    k.beam(s + Vector((0, -0.045, 0.07)), s + Vector((0, -0.045, -0.07)), 0.024, 0.02, "steel")
    k.beam(s + Vector((0, -0.045, 0.07)), s + Vector((0, 0.085, 0.035)), 0.012, 0.01, "steel")
    pts, widths = [], []
    n = 6
    for i in range(n + 1):
        t = i / n
        pts.append(s + Vector((0, -0.05 - 0.9 * t, 0.012)))
        widths.append(0.052 * (1.0 - 0.18 * t) if i < n else 0.004)
    k.blade(pts, widths, 0.014, "steel_light")


def kalkan(k, s):
    # the horde's small domed shield; at rest its face looks up (+Z) like the big one
    c = s + Vector((0.0, -0.01, 0.07))
    k.lathe(c, [(-0.02, 0.0), (-0.02, 0.21, "hard"), (0.0, 0.22), (0.03, 0.18), (0.05, 0.1), (0.06, 0.0)],
            "cinnabar_dark", segs=16)
    k.lathe(c, [(0.0, 0.232, "hard"), (0.022, 0.222, "hard"), (0.024, 0.2, "hard"), (0.0, 0.2)],
            "gold", segs=16, cap0=False, cap1=False)
    k.lathe(c + Vector((0, 0, 0.05)), [(0.0, 0.06, "hard"), (0.03, 0.04), (0.045, 0.0)], "gold", segs=12)


def bulava(k, s):
    k.tube(s + Vector((0, 0.12, 0)), s + Vector((0, -0.42, 0)), 0.016, 0.018, "wood_dark", segs=8)
    k.ball(s + Vector((0, 0.13, 0)), 0.022, "gold", segs=8, rings=5)
    head = s + Vector((0, -0.5, 0))
    k.ball(head, 0.075, "gold", segs=12, rings=7)
    for i in range(6):
        a = math.tau * i / 6
        k.ball(head + Vector((math.cos(a) * 0.07, 0, math.sin(a) * 0.07)), 0.022, "gold_dark", segs=6, rings=4)
    k.ball(head + Vector((0, -0.075, 0)), 0.02, "cinnabar", segs=6, rings=4)


def spear(k, s):
    k.tube(s + Vector((0, 0.9, 0)), s + Vector((0, -1.25, 0)), 0.018, 0.016, "wood", segs=6)
    k.blade([s + Vector((0, -1.25, 0)), s + Vector((0, -1.38, 0)), s + Vector((0, -1.55, 0))],
            [0.05, 0.06, 0.004], 0.014, "steel_light")
    k.box(s + Vector((0, -1.2, 0)), (0.035, 0.06, 0.035), "iron")


def shield(k, s):
    # round wooden shield; at rest its face looks up (+Z), in the guard pose it faces out
    c = s + Vector((0.0, -0.01, 0.07))
    k.lathe(c, [(-0.02, 0.0), (-0.02, 0.29, "hard"), (0.0, 0.3), (0.02, 0.29, "hard"), (0.03, 0.0)],
            "whitewash", segs=16)
    k.lathe(c, [(0.0, 0.31, "hard"), (0.032, 0.3, "hard"), (0.034, 0.27, "hard"), (0.0, 0.27)],
            "iron", segs=16, cap0=False, cap1=False)
    for a in (0.0, math.pi / 2):
        k.box(c + Vector((0, 0, 0.026)), (0.52, 0.07, 0.008), "cinnabar", rot=Matrix.Rotation(a, 4, "Z"))
    k.lathe(c + Vector((0, 0, 0.03)), [(0.0, 0.08, "hard"), (0.03, 0.06), (0.05, 0.0)], "steel", segs=12)


def bow(k, s):
    # recurve bow: limbs along Y at rest like a blade, string on the archer's side (-X)
    pts, radii = [], []
    for i in range(-6, 7):
        t = i / 6
        pts.append(s + Vector((-0.13 * t * t + 0.05 * t ** 6, -0.62 * t, 0.0)))
        radii.append(0.011 + 0.012 * (1 - abs(t)))
    k.sweep(pts, radii, "wood_dark", segs=6)
    k.tube(s + Vector((0, 0.07, 0)), s + Vector((0, -0.07, 0)), 0.021, 0.021, "leather_light", segs=6)
    k.tube(pts[0], pts[-1], 0.003, 0.003, "whitewash", segs=4)


BUILDERS = {
    "sabre": lambda k, s: sabre(k, s),
    "sabre_gold": lambda k, s: sabre(k, s, gold=True),
    "palash": palash,
    "kalkan": kalkan,
    "bulava": bulava,
    "spear": spear,
    "shield": shield,
    "bow": bow,
}


def build(name, bones, armature):
    slot = SLOTS[name]
    k = MeshKit()
    # modelled around the slot as it sits in a T-pose, then turned with the lowered arm
    BUILDERS[name](k, Vector((0.0, 0.0, 0.0)))
    k.transform(Matrix.Translation(Vector(bones[slot][0])) @ rig.arm_drop(slot[-1]))
    obj = k.to_object(name)
    obj.parent = armature
    obj.parent_type = "BONE"
    obj.parent_bone = slot
    b = armature.data.bones[slot]
    m = b.matrix_local.copy()
    m.translation = b.tail_local
    obj.matrix_parent_inverse = (armature.matrix_world @ m).inverted()
    return obj
