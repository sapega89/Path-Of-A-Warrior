"""Environment kit for the steppe camp and battle rooms.

Every piece stands on the ground at its origin; 1 unit = 1 tile = 1 m. Shapes are kept
simple and rounded like carved and painted wood. Each builder takes a MeshKit and
returns nothing; `build_all()` exports one .glb per piece.
"""

import math
import random

from mathutils import Matrix, Vector

from mesh_kit import MeshKit, triangles

TAU = math.tau


def jitter(rng, lo=0.92, hi=1.06):
    return rng.uniform(lo, hi)


def poly(k, verts, faces, color, smooth=False, shade=1.0):
    k.add((verts, faces), color, None, None, smooth, shade)


# -- buildings ----------------------------------------------------------------------
def hip_roof(k, w, d, h0, h1, over, thick, color, shade=1.0):
    W, D = w / 2 + over, d / 2 + over
    r = max(0.05, w / 2 - d / 2)
    lo, hi = h0, h0 + thick
    v = [(-W, -D, lo), (W, -D, lo), (W, D, lo), (-W, D, lo),
         (-W, -D, hi), (W, -D, hi), (W, D, hi), (-W, D, hi),
         (-r, 0, h1), (r, 0, h1)]
    f = [(0, 3, 2, 1),
         (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
         (4, 5, 9, 8), (6, 7, 8, 9), (5, 6, 9), (7, 4, 8)]
    poly(k, v, f, color, shade=shade)


def window(k, center, facing, w=0.55, h=0.6):
    """Small window with blue frame and shutters on a wall facing `facing` (+-X or +-Y)."""
    fx, fy = facing
    side = Vector((abs(fy), abs(fx), 0))
    c = Vector(center)
    out = Vector((fx, fy, 0))
    rot = Matrix.Rotation(math.atan2(fx, -fy), 4, "Z")
    k.box(c + out * 0.02, (w + 0.12, 0.06, h + 0.12), "blue", rot=rot)
    k.box(c + out * 0.04, (w, 0.05, h), "dusk", rot=rot)
    k.box(c + out * 0.06, (w, 0.03, 0.04), "blue_light", rot=rot)
    k.box(c + out * 0.06, (0.04, 0.03, h), "blue_light", rot=rot)
    for s in (1, -1):
        k.box(c + out * 0.05 + side * s * (w / 2 + 0.17), (0.26, 0.04, h + 0.06), "blue", rot=rot)
    k.box(c + out * 0.09 - Vector((0, 0, h / 2 + 0.08)), (w + 0.2, 0.12, 0.05), "wood", rot=rot)


def khata(k, rng):
    w, d, hw = 5.0, 3.4, 2.1
    k.box((0, 0, 0.2), (w + 0.25, d + 0.25, 0.4), "clay")
    k.box((0, 0, 0.4 + (hw - 0.4) / 2), (w, d, hw - 0.4), "whitewash", taper=0.985)
    k.box((0, 0, 0.42), (w + 0.04, d + 0.04, 0.06), "cinnabar")
    hip_roof(k, w, d, hw - 0.05, 4.4, 0.45, 0.32, "thatch")
    k.box((0, 0, 4.4), (w - d + 0.3, 0.3, 0.16), "thatch", shade=0.88)
    k.box((-1.2, 0.4, 4.0), (0.45, 0.45, 1.2), "whitewash", shade=0.95)
    k.box((-1.2, 0.4, 4.62), (0.55, 0.55, 0.08), "clay")
    # door and windows on the front (-Y)
    k.box((0.85, -d / 2 - 0.03, 1.05), (0.9, 0.08, 1.7), "wood_dark")
    k.box((0.85, -d / 2 - 0.06, 1.05), (0.06, 0.04, 1.6), "wood", shade=0.85)
    k.box((0.85, -d / 2 - 0.05, 1.95), (1.1, 0.08, 0.1), "blue")
    window(k, (-1.0, -d / 2, 1.3), (0, -1))
    window(k, (2.4 - 0.0, -d / 2, 1.3), (0, -1), w=0.45)
    window(k, (w / 2, 0.3, 1.3), (1, 0))
    window(k, (-w / 2, 0.0, 1.3), (-1, 0))
    k.box((0.85, -d / 2 - 0.45, 0.08), (1.2, 0.7, 0.16), "stone")


def tyn(k, rng, length=2.0):
    """Wattle fence segment along X with a clay pot on one post."""
    n = 3
    for i in range(n):
        x = -length / 2 + length * i / (n - 1)
        k.tube((x, 0, 0), (x + rng.uniform(-0.03, 0.03), 0, 1.25), 0.05, 0.04, "wood_dark", segs=6)
    for row in range(5):
        z = 0.25 + row * 0.2
        pts, radii = [], []
        for j in range(9):
            t = j / 8
            x = -length / 2 + length * t
            y = 0.045 * math.sin(t * math.pi * 4 + row * math.pi)
            pts.append((x, y, z + rng.uniform(-0.01, 0.01)))
            radii.append(0.045)
        k.sweep(pts, radii, "wood_light", segs=5, flat=0.8, shade=jitter(rng, 0.85, 1.05))
    x = -length / 2
    k.lathe((x, 0, 1.25), [(0.0, 0.04), (0.04, 0.09), (0.16, 0.12), (0.26, 0.08), (0.3, 0.05, "hard"), (0.33, 0.06), (0.34, 0.0)],
            "clay", segs=10, rot=Matrix.Rotation(math.pi, 4, "X") @ Matrix.Translation((0, 0, -0.34)))


def palisade(k, rng, length=2.0):
    n = 9
    for i in range(n):
        x = -length / 2 + length * (i + 0.5) / n
        h = rng.uniform(2.1, 2.45)
        r = rng.uniform(0.095, 0.115)
        k.lathe((x, rng.uniform(-0.02, 0.02), 0), [(0.0, r), (h - 0.3, r, "hard"), (h, 0.0)],
                "wood", segs=7, shade=jitter(rng, 0.85, 1.08))
    for z in (0.6, 1.6):
        k.beam((-length / 2, 0.13, z), (length / 2, 0.13, z), 0.08, 0.1, "wood_dark")


def kuznya(k, rng):
    """Open forge: four posts, a lean-to thatch roof, a clay hearth, an anvil on a stump."""
    for x, y in ((-1.5, -1.1), (1.5, -1.1), (-1.5, 1.1), (1.5, 1.1)):
        h = 2.2 if y < 0 else 2.8
        k.tube((x, y, 0), (x, y, h), 0.09, 0.08, "wood_dark", segs=6)
    v = [(-1.9, -1.6, 2.15), (1.9, -1.6, 2.15), (1.9, 1.5, 2.95), (-1.9, 1.5, 2.95)]
    v2 = [(x, y, z + 0.22) for x, y, z in v]
    poly(k, v + v2, [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)], "thatch")
    k.box((0.6, 0.6, 0.45), (1.3, 1.0, 0.9), "clay")
    k.box((0.6, 0.6, 0.92), (1.0, 0.7, 0.06), "ember")
    k.box((0.6, 0.6, 0.93), (0.6, 0.4, 0.06), "fire")
    k.lathe((0.9, 0.85, 0.9), [(0.0, 0.2), (0.9, 0.12), (1.6, 0.1)], "clay", segs=8, shade=0.9)
    k.lathe((-0.6, -0.3, 0), [(0.0, 0.26), (0.45, 0.24, "hard"), (0.46, 0.0)], "wood", segs=9)
    k.box((-0.6, -0.3, 0.55), (0.18, 0.4, 0.16), "iron")
    k.box((-0.6, -0.3, 0.66), (0.24, 0.62, 0.08), "iron", taper=1.0)
    k.lathe((-0.6, -0.62, 0.66), [(-0.04, 0.04), (0.04, 0.0)], "iron", segs=6,
            rot=Matrix.Rotation(math.pi / 2, 4, "X"))
    k.box((-1.1, 0.7, 0.35), (0.6, 0.9, 0.12), "leather", rot=Matrix.Rotation(0.2, 4, "X"))
    k.beam((-1.2, -0.2, 0.75), (-0.4, -0.25, 0.72), 0.04, 0.04, "wood_light")


# -- tents and camp -------------------------------------------------------------------
def shatro(k, rng, radius=2.2, wall=1.6, top=3.6, stripes=("canvas", "whitewash"), banner=True):
    """Round pavilion tent with striped walls, a scalloped valance and a banner pole."""
    n = 16
    for i in range(n):
        a0, a1 = TAU * i / n, TAU * (i + 1) / n
        mid = (a0 + a1) / 2
        if abs(((mid + math.pi) % TAU) - math.pi) < 0.25:
            continue  # doorway at the front
        col = stripes[i % 2]
        k.lathe((0, 0, 0), [(0.0, radius), (wall, radius * 0.98)], col, segs=1, a0=a0, a1=a1, thickness=0.03,
                cap0=False, cap1=False, smooth=False)
        k.lathe((0, 0, 0), [(wall - 0.02, radius * 1.06, "hard"), (wall + 0.05, radius * 1.03), (top, 0.06)],
                stripes[(i + 1) % 2], segs=1, a0=a0, a1=a1, thickness=0.03, cap0=False, cap1=False, smooth=False)
        # valance tooth
        ca, sa = math.sin(mid), -math.cos(mid)
        p = Vector((ca * radius * 1.07, sa * radius * 1.07, wall - 0.12))
        k.box(p, (0.42, 0.04, 0.3), "cinnabar", rot=Matrix.Rotation(mid, 4, "Z"), taper=0.4)
        k.box(p + Vector((0, 0, 0.17)), (0.44, 0.05, 0.06), "gold", rot=Matrix.Rotation(mid, 4, "Z"))
    k.lathe((0, 0, 0), [(0.0, 0.0), (0.0, radius * 0.97)], "canvas_dark", segs=n, cap0=False, cap1=False)
    k.tube((0, 0, 0), (0, 0, top + 1.6), 0.06, 0.05, "wood_dark", segs=6)
    k.ball((0, 0, top + 1.62), 0.1, "gold", segs=8, rings=5)
    # door flaps folded aside
    for s in (1, -1):
        k.box((s * 0.42, -radius * 1.0, wall / 2), (0.32, 0.08, wall), "cinnabar", rot=Matrix.Rotation(s * 0.5, 4, "Z"))
    if banner:
        flag(k, rng, (0, 0, top + 1.45), 1.0, 0.6, "cinnabar", "gold")


def flag(k, rng, top, w, h, color, trim):
    """Waving flag hanging from a pole at `top`, flying towards +X."""
    tx, ty, tz = top
    cols, rows = 8, 3
    verts = []
    for r in range(rows + 1):
        for c in range(cols + 1):
            u, v = c / cols, r / rows
            x = tx + 0.05 + u * w
            y = ty + 0.08 * math.sin(u * math.pi * 2.0) * u
            z = tz - v * h - 0.06 * u * u
            if c == cols and r in (0, rows):
                pass
            verts.append((x, y, z))
    faces = []
    for r in range(rows):
        for c in range(cols):
            a = r * (cols + 1) + c
            faces.append((a, a + 1, a + cols + 2, a + cols + 1))
    made = k.add((verts, faces), color, None, None, True)
    k.solidify(made, 0.02, color)
    k.box((tx + 0.05 + w * 0.45, ty + 0.04, tz - h * 0.5), (0.14, 0.06, 0.14), trim, rot=Matrix.Rotation(math.pi / 4, 4, "Y"))


def banner(k, rng, color="cinnabar"):
    k.tube((0, 0, 0), (0, 0, 3.6), 0.05, 0.04, "wood_dark", segs=6)
    k.lathe((0, 0, 3.6), [(0.0, 0.05), (0.1, 0.06), (0.32, 0.0)], "gold", segs=6)
    flag(k, rng, (0, 0, 3.5), 1.3, 0.85, color, "gold")
    k.lathe((0, 0, 0), [(0.0, 0.25), (0.12, 0.22), (0.2, 0.0)], "stone", segs=7, smooth=False)


def namet(k, rng):
    """Small A-frame canvas tent along X."""
    L, W, H = 2.4, 1.9, 1.6
    v = [(-L / 2, -W / 2, 0), (L / 2, -W / 2, 0), (L / 2, W / 2, 0), (-L / 2, W / 2, 0), (-L / 2, 0, H), (L / 2, 0, H)]
    made = k.add((v, [(0, 1, 5, 4), (2, 3, 4, 5), (1, 2, 5), (3, 0, 4)]), "canvas", None, None, False)
    k.box((-L / 2 - 0.02, -0.0, 0.5), (0.04, 0.6, 1.0), "dusk", taper=0.2)
    for x in (-L / 2 - 0.05, L / 2 + 0.05):
        k.tube((x, 0, 0), (x, 0, H + 0.25), 0.035, 0.03, "wood_dark", segs=5)
    k.beam((-L / 2 - 0.05, 0, H + 0.02), (L / 2 + 0.05, 0, H + 0.02), 0.06, 0.06, "wood")


def vohnyshche(k, rng):
    """Campfire: stone ring, logs and a cauldron on a tripod (the flame is an effect)."""
    for i in range(9):
        a = TAU * i / 9 + rng.uniform(-0.1, 0.1)
        k.ball((math.sin(a) * 0.55, -math.cos(a) * 0.55, 0.06), (0.14, 0.12, 0.1), "stone",
               rot=Matrix.Rotation(a, 4, "Z"), segs=6, rings=4, smooth=False, shade=jitter(rng, 0.8, 1.05))
    for i in range(4):
        a = TAU * i / 4 + 0.4
        d = Vector((math.sin(a), -math.cos(a), 0))
        k.tube(d * 0.42 + Vector((0, 0, 0.05)), d * 0.05 + Vector((0, 0, 0.22)), 0.06, 0.05, "wood_dark", segs=6)
    k.ball((0, 0, 0.08), (0.28, 0.28, 0.06), "chernozem", segs=8, rings=3)
    k.ball((0, 0, 0.12), (0.18, 0.18, 0.05), "ember", segs=8, rings=3)
    for i in range(3):
        a = TAU * i / 3
        k.tube((math.sin(a) * 0.75, -math.cos(a) * 0.75, 0), (0, 0, 1.45), 0.03, 0.025, "wood_dark", segs=5)
    k.tube((0, 0, 1.45), (0, 0, 0.95), 0.006, 0.006, "iron", segs=4)
    k.lathe((0, 0, 0.6), [(0.0, 0.0), (0.0, 0.12), (0.12, 0.24), (0.3, 0.26, "hard"), (0.33, 0.24), (0.32, 0.0)],
            "iron", segs=12)


def viz(k, rng):
    """Wooden cart with two barrels; shafts towards -Y."""
    k.box((0, 0, 0.8), (1.3, 2.4, 0.12), "wood")
    for s in (1, -1):
        k.box((s * 0.67, 0, 1.05), (0.07, 2.4, 0.42), "wood", shade=0.92)
    for y in (1.2, -1.2):
        k.box((0, y, 1.05), (1.3, 0.07, 0.42), "wood", shade=0.92)
    for s in (1, -1):
        for y in (0.75, -0.75):
            wheel(k, (s * 0.8, y, 0.55), 0.55)
        k.beam((s * 0.35, -1.2, 0.85), (s * 0.45, -2.9, 0.55), 0.07, 0.07, "wood_dark")
    k.beam((-0.9, 0.75, 0.55), (0.9, 0.75, 0.55), 0.08, 0.08, "wood_dark")
    k.beam((-0.9, -0.75, 0.55), (0.9, -0.75, 0.55), 0.08, 0.08, "wood_dark")
    bochka(k, rng, (0.0, 0.5, 0.86), lying=True)
    bochka(k, rng, (0.0, -0.45, 0.86), lying=False, scale=0.8)
    k.box((0.35, -0.75, 1.0), (0.35, 0.45, 0.3), "canvas", rot=Matrix.Rotation(0.3, 4, "Z"))


def wheel(k, center, r, spokes=8):
    c = Vector(center)
    rot = Matrix.Rotation(math.pi / 2, 4, "Y")
    k.lathe(c + Vector((-0.04, 0, 0)), [(0.0, r - 0.07, "hard"), (0.0, r), (0.08, r, "hard"), (0.08, r - 0.07)],
            "wood_dark", segs=14, rot=rot, cap0=False, cap1=False, smooth=False)
    k.lathe(c + Vector((-0.04, 0, 0)), [(0.0, r - 0.07, "hard"), (0.08, r - 0.07)],
            "wood_dark", segs=14, rot=rot @ Matrix.Rotation(math.pi, 4, "X") @ Matrix.Translation((0, 0, -0.08)),
            cap0=False, cap1=False, smooth=False)
    k.lathe(c + Vector((-0.09, 0, 0)), [(0.0, 0.1), (0.18, 0.1)], "wood", segs=8, rot=rot)
    for i in range(spokes):
        a = TAU * i / spokes
        d = Vector((0, math.cos(a), math.sin(a)))
        k.beam(c + d * 0.08, c + d * (r - 0.05), 0.04, 0.04, "wood")


def bochka(k, rng, pos=(0, 0, 0), lying=False, scale=1.0):
    r, h = 0.3 * scale, 0.75 * scale
    prof = [(0.0, r * 0.82, "hard"), (h * 0.5, r), (h, r * 0.82, "hard")]
    rot = None
    p = Vector(pos)
    if lying:
        rot = Matrix.Rotation(math.pi / 2, 4, "Y")
        p = p + Vector((-h / 2, 0, r * 0.95))
    k.lathe(p, prof, "wood", segs=12, rot=rot, shade=jitter(rng))
    for z in (0.12, 0.5, 0.88):
        rr = r * (0.82 + 0.18 * math.sin(math.pi * z)) + 0.01
        k.lathe(p if rot is None else p, [(h * z - 0.025, rr), (h * z + 0.025, rr)], "iron", segs=12, rot=rot,
                cap0=False, cap1=False)


def bochka_piece(k, rng):
    bochka(k, rng)


def skrynia(k, rng):
    k.box((0, 0, 0.3), (1.0, 0.6, 0.6), "wood", shade=jitter(rng))
    k.box((0, 0, 0.62), (1.04, 0.64, 0.06), "wood_dark")
    for x in (-0.35, 0.35):
        k.box((x, 0, 0.32), (0.06, 0.64, 0.64), "iron")
    k.box((0, -0.31, 0.45), (0.1, 0.03, 0.12), "gold")


def harmata(k, rng):
    """Field cannon on a two-wheeled carriage, barrel towards -Y."""
    k.box((0, 0.6, 0.45), (0.5, 1.9, 0.22), "wood", rot=Matrix.Rotation(-0.25, 4, "X"))
    for s in (1, -1):
        wheel(k, (s * 0.42, -0.1, 0.62), 0.62, spokes=10)
    k.beam((-0.5, -0.1, 0.62), (0.5, -0.1, 0.62), 0.09, 0.09, "wood_dark")
    rot = Matrix.Rotation(math.pi / 2 - 0.08, 4, "X")
    k.lathe((0, 0.45, 0.85), [(0.0, 0.0), (0.0, 0.16), (0.12, 0.17, "hard"), (0.16, 0.15), (1.2, 0.12), (1.4, 0.13, "hard"),
                              (1.5, 0.13), (1.5, 0.07, "hard"), (1.3, 0.0)], "gold_dark", segs=12, rot=rot)
    k.ball((0, 0.52, 0.86), 0.08, "gold_dark", segs=8, rings=5)
    k.box((0, 0.35, 0.86), (0.3, 0.2, 0.08), "iron")
    for i in range(3):
        k.ball((0.6 + i * 0.13, 0.9, 0.06), 0.06, "iron", segs=6, rings=4)


def stih(k, rng):
    """Haystack with a pole."""
    k.lathe((0, 0, 0), [(0.0, 1.05), (0.5, 1.15), (1.3, 0.95), (2.1, 0.45), (2.5, 0.0)], "straw", segs=11,
            shade=jitter(rng), smooth=True)
    k.lathe((0, 0, 0), [(0.0, 1.07), (0.25, 1.12, "hard"), (0.26, 0.0)], "thatch", segs=11)
    k.tube((0, 0, 2.3), (0.05, 0, 3.1), 0.04, 0.03, "wood_dark", segs=5)


def zhuravel(k, rng):
    """Well with a sweep crane."""
    k.box((0, 0, 0.45), (1.1, 1.1, 0.9), "wood", shade=0.95)
    k.box((0, 0, 0.92), (1.2, 1.2, 0.08), "wood_dark")
    k.box((0, 0, 0.93), (0.9, 0.9, 0.04), "dusk")
    k.tube((1.4, 0.0, 0), (1.4, 0.0, 2.8), 0.12, 0.09, "wood_dark", segs=7)
    k.box((1.4, 0, 2.86), (0.14, 0.3, 0.2), "wood_dark", taper=1.2)
    a, b = Vector((0.0, 0.0, 4.4)), Vector((3.0, 0.0, 1.7))
    k.tube(b, a, 0.07, 0.04, "wood", segs=6)
    k.box(b + Vector((0.15, 0, -0.1)), (0.35, 0.3, 0.3), "stone", shade=0.9)
    k.tube(a, (0.0, 0.0, 1.3), 0.012, 0.012, "wood_dark", segs=4)
    k.lathe((0.0, 0.0, 1.0), [(0.0, 0.12), (0.28, 0.16, "hard"), (0.29, 0.0)], "wood_light", segs=8)


# -- nature ---------------------------------------------------------------------------
def topolia(k, rng):
    h = rng.uniform(6.0, 7.2)
    k.tube((0, 0, 0), (0, 0, h * 0.45), 0.2, 0.12, "wood_dark", segs=7)
    prof = [(h * 0.18, 0.0), (h * 0.22, 0.55), (h * 0.45, 0.85), (h * 0.75, 0.6), (h * 0.95, 0.18), (h, 0.0)]
    k.lathe((0, 0, 0), prof, "oak_dark", segs=9, shade=jitter(rng))
    for i in range(3):
        a = rng.uniform(0, TAU)
        z = rng.uniform(0.35, 0.7) * h
        k.ball((math.sin(a) * 0.55, -math.cos(a) * 0.55, z), (0.42, 0.42, 0.9), "oak", segs=8, rings=5,
               shade=jitter(rng, 0.9, 1.1))


def dub(k, rng):
    h = rng.uniform(3.6, 4.4)
    k.lathe((0, 0, 0), [(0.0, 0.42), (0.2, 0.3), (h * 0.6, 0.24), (h * 0.62, 0.0)], "wood_dark", segs=8)
    for i in range(3):
        a = TAU * i / 3 + rng.uniform(-0.3, 0.3)
        k.beam((0, 0, h * 0.5), (math.sin(a) * 1.0, -math.cos(a) * 1.0, h * 0.8), 0.14, 0.14, "wood_dark")
    blobs = [((0, 0, h + 0.4), 1.7), ((1.1, 0.3, h - 0.1), 1.2), ((-1.1, -0.2, h), 1.25), ((0.2, -1.0, h - 0.2), 1.1),
             ((-0.2, 1.0, h + 0.1), 1.15)]
    for (x, y, z), r in blobs:
        k.ball((x, y, z), (r, r, r * 0.75), "oak", segs=10, rings=6, shade=jitter(rng, 0.82, 1.08))


def kushch(k, rng):
    """A ragged bush: rough clumps of leaves, dark inside, a few bare twigs sticking out."""
    for i in range(6):
        a = TAU * i / 6 + rng.uniform(0, 0.8)
        d = rng.uniform(0.2, 0.42)
        r = rng.uniform(0.32, 0.5)
        rot = Matrix.Rotation(rng.uniform(0, TAU), 4, "Z") @ Matrix.Rotation(rng.uniform(-0.4, 0.4), 4, "X")
        k.ball((math.sin(a) * d, -math.cos(a) * d, r * 0.75 + rng.uniform(0, 0.2)), (r, r * 0.9, r * 0.75),
               "oak" if i % 2 else "oak_dark", segs=7, rings=4, rot=rot, smooth=False, shade=jitter(rng, 0.75, 1.05))
    for i in range(3):
        a = rng.uniform(0, TAU)
        base = Vector((math.sin(a) * 0.25, -math.cos(a) * 0.25, 0.5))
        tip = base + Vector((math.sin(a) * 0.45, -math.cos(a) * 0.45, rng.uniform(0.35, 0.6)))
        k.tube(base, tip, 0.02, 0.006, "wood_dark", segs=4)


def kamin(k, rng):
    for i in range(rng.randint(2, 3)):
        r = rng.uniform(0.55, 0.95)
        a = rng.uniform(0, TAU)
        rot = Matrix.Rotation(rng.uniform(0, TAU), 4, "Z") @ Matrix.Rotation(rng.uniform(-0.3, 0.3), 4, "X")
        k.ball((math.sin(a) * 0.4 * i, -math.cos(a) * 0.4 * i, r * 0.45), (r, r * 0.8, r * 0.65), "stone", segs=6, rings=4,
               rot=rot, smooth=False, shade=jitter(rng, 0.85, 1.08))


def trava(k, rng):
    """Tuft of dry grass, now and then a dry seed head."""
    for i in range(9):
        a = rng.uniform(0, TAU)
        d = rng.uniform(0.0, 0.18)
        base = Vector((math.sin(a) * d, -math.cos(a) * d, 0))
        tip = base + Vector((rng.uniform(-0.15, 0.15), rng.uniform(-0.15, 0.15), rng.uniform(0.35, 0.6)))
        k.lathe(base, [(0.0, 0.03), ((tip - base).length, 0.0)], "grass", segs=3, smooth=False,
                rot=Vector((0, 0, 1)).rotation_difference(tip - base).to_matrix().to_4x4(), shade=jitter(rng, 0.85, 1.15))
    for i in range(1 if rng.random() < 0.35 else 0):
        p = Vector((rng.uniform(-0.2, 0.2), rng.uniform(-0.2, 0.2), rng.uniform(0.4, 0.55)))
        k.tube((p.x, p.y, 0), p, 0.008, 0.008, "grass_dark", segs=3)
        k.ball(p, (0.025, 0.025, 0.05), "straw", segs=5, rings=3)


def penok(k, rng):
    """Stump with an axe stuck in it."""
    k.lathe((0, 0, 0), [(0.0, 0.38), (0.12, 0.3), (0.5, 0.28, "hard"), (0.51, 0.0)], "wood", segs=9)
    k.lathe((0, 0, 0.505), [(0.0, 0.24), (0.005, 0.0)], "wood_light", segs=9)
    k.beam((0.05, 0, 0.55), (0.5, -0.3, 0.95), 0.04, 0.04, "wood_light")
    k.box((0.02, 0.02, 0.52), (0.22, 0.03, 0.14), "steel", rot=Matrix.Rotation(-0.6, 4, "Z"))


# -- the maps of the campaign: firs, a woodpile, a weapon rack, crags on the cliffs --------
def yalyna(k, rng):
    """Fir: a straight trunk and four tiers of dark needles."""
    h = rng.uniform(3.8, 4.4)
    k.tube((0, 0, 0), (0, 0, h * 0.3), 0.16, 0.12, "wood_dark", segs=7)
    tiers = 4
    for i in range(tiers):
        z0 = h * (0.16 + 0.19 * i)
        r = 1.1 * (1.0 - i / (tiers + 0.8))
        k.lathe((0, 0, z0), [(0.0, r * 0.35), (0.02, r, "hard"), (0.14, r * 0.9, "hard"), (h * 0.36, 0.0)],
                "oak_dark", segs=9, shade=jitter(rng, 0.85, 1.05))


def drova(k, rng):
    """Woodpile: split logs stacked between two stakes."""
    for row in range(3):
        n = 4 - row
        for i in range(n):
            x = (i - (n - 1) / 2) * 0.24
            z = 0.11 + row * 0.2
            k.tube((x, -0.45, z), (x + rng.uniform(-0.02, 0.02), 0.45, z), 0.1, 0.1,
                   "wood" if (i + row) % 2 else "wood_light", segs=6, shade=jitter(rng))
    for x in (-0.55, 0.55):
        k.tube((x, 0, 0), (x, 0, 0.8), 0.04, 0.035, "wood_dark", segs=5)


def stoiak(k, rng):
    """Weapon rack: two posts, a bar, spears leaning on it."""
    for x in (-0.6, 0.6):
        k.tube((x, 0, 0), (x, 0, 1.2), 0.05, 0.045, "wood_dark", segs=6)
    k.beam((-0.65, 0, 1.05), (0.65, 0, 1.05), 0.06, 0.06, "wood")
    for i in range(4):
        x = -0.45 + i * 0.3
        k.tube((x, 0.25, 0), (x + 0.02, -0.03, 1.6), 0.02, 0.02, "wood_light", segs=4)
        k.lathe((x + 0.02, -0.03, 1.6), [(0.0, 0.035), (0.18, 0.0)], "steel", segs=4)


def skelia(k, rng):
    """Crags on the face of a cliff: angular rocks heaped up to two metres."""
    for i in range(5):
        r = rng.uniform(0.42, 0.62)
        x, y = rng.uniform(-0.28, 0.28), rng.uniform(-0.28, 0.28)
        hgt = rng.uniform(1.1, 2.0) if i < 3 else rng.uniform(0.5, 0.9)
        rot = Matrix.Rotation(rng.uniform(0, TAU), 4, "Z") @ Matrix.Rotation(rng.uniform(-0.15, 0.15), 4, "X")
        k.ball((x, y, hgt * 0.5), (r, r * 0.9, hgt * 0.6), "stone" if i % 2 else "stone_dark", segs=6, rings=4,
               rot=rot, smooth=False, shade=jitter(rng, 0.85, 1.1))


PROPS = {
    "khata": khata,
    "tyn": tyn,
    "palisade": palisade,
    "kuznya": kuznya,
    "shatro": shatro,
    "namet": namet,
    "banner": banner,
    "banner_crown": lambda k, rng: banner(k, rng, "whitewash"),
    "vohnyshche": vohnyshche,
    "viz": viz,
    "bochka": bochka_piece,
    "skrynia": skrynia,
    "harmata": harmata,
    "stih": stih,
    "zhuravel": zhuravel,
    "topolia": topolia,
    "dub": dub,
    "kushch": kushch,
    "kamin": kamin,
    "trava": trava,
    "penok": penok,
    "yalyna": yalyna,
    "drova": drova,
    "stoiak": stoiak,
    "skelia": skelia,
}


def build_one(name, seed=7):
    rng = random.Random(f"{name}:{seed}")
    k = MeshKit()
    PROPS[name](k, rng)
    return k.to_object(name)


def build_all(out, export):
    import bpy
    report = []
    for name in PROPS:
        obj = build_one(name)
        export(f"{out}/props/{name}.glb", [obj])
        report.append((name, triangles(obj)))
        bpy.data.objects.remove(obj, do_unlink=True)
    return report


def preview_set():
    return []
