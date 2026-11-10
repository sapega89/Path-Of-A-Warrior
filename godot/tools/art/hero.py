"""The hero's Cossack class, finer than the wooden figures of characters.py: tall, a shaved head
with an oseledets braided down behind the ear, a long Cossack moustache, narrow steel-grey eyes
under straight brows; a long black zhupan open on the chest over a linen shirt, wine-red
embroidery with silver lozenges down every edge, a standing collar, a wine-red sash, black
sharovary and tall boots.

Cloth is built from open shells through horizontal rings, so a coat can open in a V, turn its
lapels back and part over the legs; hair and the moustache are tapering locks.
"""

import math

from mathutils import Matrix, Vector

from characters import Figure

TAU = math.pi * 2.0
HEAD = 0.86  # the head is drawn this much smaller than the others': a tall man's proportions

RECIPES = {
    "kozak_hero": {
        "hair": "hair_black", "iris": "iris_steel", "shirt": "whitewash", "coat": "noir", "lining": "wine_dark",
        "coat_trim": "wine", "sash": "wine", "trousers": "noir_light", "boots": "chernozem", "boot_band": "wine_dark",
    },
}


class HeroFigure(Figure):
    SEGS = 24

    # -- helpers ------------------------------------------------------------------------
    def shell(self, rings, color, bone, segs=None, thickness=0.0, inner=None, folds=0):
        """An open surface through horizontal rings (z, rx, ry, a0, a1[, fold depth]): each ring
        runs from the angle a0 to a1 (0 is the front, growing towards the left side), so an
        opening can widen or narrow from ring to ring; `folds` waves the cloth around, as deep
        as each ring says. `inner` colours the inside when it has a thickness."""
        segs = segs or self.SEGS
        verts, faces = [], []
        for ring in rings:
            z, rx, ry, a0, a1 = ring[:5]
            depth = ring[5] if len(ring) > 5 else 0.0
            for j in range(segs + 1):
                a = a0 + (a1 - a0) * j / segs
                w = 1.0 + depth * math.sin(folds * (a - a0)) if folds else 1.0
                verts.append((rx * w * math.sin(a), -ry * w * math.cos(a), z))
        n = segs + 1
        for i in range(len(rings) - 1):
            for j in range(segs):
                a, b = i * n + j, (i + 1) * n + j
                faces.append((a, a + 1, b + 1, b))
        made = self.k.add((verts, faces), color, bone, None, True)
        if thickness > 0:
            self.k.solidify(made, thickness, inner or color, bone)
        return made

    def lock(self, points, widths, color, around, flat=0.5, segs=8):
        """A lock of hair: a tapering tube flattened so that it lies on the head (towards
        `around`)."""
        pts = [Vector(p) for p in points]
        verts, faces = [], []
        for i, p in enumerate(pts):
            t = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
            out = p - around
            out = (out - t * out.dot(t)).normalized()
            side = out.cross(t).normalized()
            for j in range(segs):
                a = TAU * j / segs
                verts.append(tuple(p + side * (math.cos(a) * widths[i]) + out * (math.sin(a) * widths[i] * flat)))
        for i in range(len(pts) - 1):
            for j in range(segs):
                j2 = (j + 1) % segs
                a, b = i * segs, (i + 1) * segs
                faces.append((a + j, a + j2, b + j2, b + j))
        faces.append(tuple(reversed(range(segs))))
        last = (len(pts) - 1) * segs
        faces.append(tuple(range(last, last + segs)))
        return self.k.add((verts, faces), color, "head", None, True)

    # -- head ---------------------------------------------------------------------------
    def head(self, r):
        k = self.k
        c = self.h("head") + Vector((0, 0, 0.125))
        self.head_center = c
        # the skull, and a lean lower face narrowing to a pointed chin
        k.ball(c + Vector((0, 0.012, 0.022)), (0.096, 0.104, 0.11), "skin", "head", segs=self.SEGS, rings=14)
        jaw = [(-0.13, 0.0), (-0.127, 0.016), (-0.112, 0.036), (-0.08, 0.062), (-0.04, 0.082), (0.0, 0.09),
               (0.03, 0.09)]
        k.lathe(c + Vector((0, -0.01, 0.004)), jaw, "skin", "head", segs=self.SEGS, sx=0.88, sy=0.98,
                rot=Matrix.Rotation(-0.32, 4, "X"))
        k.tube(self.h("head") + Vector((0, 0.014, -0.09)), c + Vector((0, 0.016, -0.04)), 0.06, 0.051, "skin",
               "head", segs=16)
        for sx in (1, -1):
            k.ball(c + Vector((0.09 * sx, 0.016, -0.014)), (0.011, 0.018, 0.026), "skin", "head", segs=10, rings=6,
                   rot=Matrix.Rotation(0.2 * sx, 4, "Z"))
        # a small straight nose, a firm mouth
        k.box(c + Vector((0, -0.093, -0.026)), (0.012, 0.018, 0.05), "skin", "head", taper=0.5,
              rot=Matrix.Rotation(-0.3, 4, "X"))
        k.ball(c + Vector((0, -0.1015, -0.049)), (0.0075, 0.0075, 0.006), "skin", "head", segs=8, rings=5)
        k.box(c + Vector((0, -0.0915, -0.079)), (0.022, 0.005, 0.0028), "skin_dark", "head")
        # a long Cossack moustache: from under the nose over the lip, its ends hanging down past
        # the corners of the mouth below the jaw
        for sx in (1, -1):
            pts = [(0.003, -0.1015, -0.057), (0.017, -0.1005, -0.063), (0.031, -0.0945, -0.073),
                   (0.041, -0.0875, -0.089), (0.0465, -0.083, -0.11), (0.049, -0.081, -0.134), (0.0485, -0.081, -0.156)]
            self.lock([c + Vector((x * sx, y, z)) for x, y, z in pts],
                      [0.0075, 0.0105, 0.0108, 0.0092, 0.0072, 0.0045, 0.0012], r["hair"],
                      c + Vector((0, 0.02, -0.06)), flat=0.55, segs=10)
        self.eyes(r)

    def eyes(self, r):
        """Narrow eyes under low straight brows that dip towards the nose, a heavy dark upper lid,
        a small spark of light: a grown man's stern look."""
        k, c = self.k, self.head_center
        for sx in (1, -1):
            yaw = Matrix.Rotation(0.42 * sx, 4, "Z") @ Matrix.Rotation(-0.12 * sx, 4, "Y")
            k.ball(c + Vector((0.038 * sx, -0.08, 0.001)), (0.0235, 0.008, 0.0096), "whitewash", "head",
                   segs=14, rings=7, rot=yaw)
            k.ball(c + Vector((0.0382 * sx, -0.0858, 0.0005)), (0.0106, 0.005, 0.0104), r["iris"], "head",
                   segs=14, rings=7, rot=yaw)
            k.ball(c + Vector((0.0388 * sx, -0.0895, 0.0)), (0.0052, 0.003, 0.006), "chernozem", "head",
                   segs=10, rings=5, rot=yaw)
            k.ball(c + Vector((0.0352 * sx, -0.0918, 0.0042)), 0.0024, "hair_white", "head", segs=8, rings=4)
            lid = [c + Vector((0.013 * sx, -0.0892, 0.003)), c + Vector((0.036 * sx, -0.092, 0.0108)),
                   c + Vector((0.064 * sx, -0.0705, 0.0118))]
            k.sweep(lid, [0.0034, 0.0048, 0.0056], "chernozem", "head", segs=6, flat=0.6)
            low = [c + Vector((0.026 * sx, -0.0905, -0.0098)), c + Vector((0.057 * sx, -0.0765, -0.0055))]
            k.sweep(low, [0.0012, 0.002], "skin_dark", "head", segs=5, flat=0.6)
            brow = [c + Vector((0.01 * sx, -0.1005, 0.019)), c + Vector((0.04 * sx, -0.0975, 0.0275)),
                    c + Vector((0.07 * sx, -0.0715, 0.03))]
            k.sweep(brow, [0.0048, 0.0046, 0.0018], r["hair"], "head", segs=6, flat=0.5)

    def oseledets(self, r):
        """A shaved head with the Cossack oseledets: a thick lock from the top of the brow back
        over the crown, then down behind the left ear in a braid to the collar, tied at the end."""
        k, c, hair = self.k, self.head_center, r["hair"]
        whorl = c + Vector((0, 0.02, 0.035))
        k.ball(whorl, (0.0965, 0.103, 0.104), "scalp", "head", segs=self.SEGS, rings=12)

        def on_skull(deg, e, out):
            ph = math.radians(deg)
            return whorl + Vector((math.sin(ph) * math.cos(e) * 0.0965 * out, -math.cos(ph) * math.cos(e) * 0.103 * out,
                                   math.sin(e) * 0.104 * out))

        top = [on_skull(0, 0.62, 1.02), on_skull(0, 0.95, 1.08), on_skull(4, 1.3, 1.12), on_skull(60, 1.42, 1.12),
               on_skull(118, 1.05, 1.1), on_skull(112, 0.62, 1.1), on_skull(106, 0.2, 1.12)]
        self.lock(top, [0.012, 0.026, 0.03, 0.03, 0.026, 0.022, 0.018], hair, whorl, flat=0.45, segs=10)
        # the braid: knots in turn either side of its line, hanging from behind the ear
        start = top[-1]
        end = start + Vector((0.012, 0.02, -0.2))
        knots = 9
        for i in range(knots):
            t = i / (knots - 1)
            at = start.lerp(end, t) + Vector((0.0, 0.006 if i % 2 else -0.006, 0.0))
            w = 0.017 * (1.0 - 0.45 * t)
            k.ball(at, (w, w * 0.8, w * 1.45), hair, "head", segs=8, rings=5,
                   rot=Matrix.Rotation(0.4 if i % 2 else -0.4, 4, "X"))
        k.ball(end + Vector((0, 0, -0.012)), (0.009, 0.009, 0.008), r["sash"], "head", segs=8, rings=5)
        self.lock([end + Vector((0, 0, -0.016)), end + Vector((0.002, 0.003, -0.045))], [0.009, 0.002], hair,
                  end + Vector((0, -0.05, 0)), flat=0.6, segs=8)

    # -- body ---------------------------------------------------------------------------
    def zhupan(self, r):
        """A long black zhupan worn open at the chest: lapels turned back on the wine-red
        lining, a standing collar open in front, the skirt parting below the sash down to the
        calves, embroidery down every edge and round the hem; under it a linen shirt open to the
        middle of the chest on bare skin, a silver cross on a cord."""
        k = self.k
        coat, lining, trim = r["coat"], r["lining"], r["coat_trim"]
        # the chest, bare where the shirt opens
        skin = [(1.32, 0.162, 0.108), (1.37, 0.17, 0.116), (1.42, 0.176, 0.12), (1.48, 0.17, 0.114),
                (1.53, 0.148, 0.098), (1.57, 0.096, 0.074)]
        self.shell([(z, rx, ry, -0.9, 0.9) for z, rx, ry in skin], "skin", "chest", segs=16)
        # the shirt, open in a V to the middle of the chest
        shirt = [(1.1, 0.15, 0.108, 0.0), (1.2, 0.154, 0.11, 0.0), (1.3, 0.166, 0.112, 0.0), (1.35, 0.172, 0.118, 0.03),
                 (1.42, 0.182, 0.125, 0.25), (1.48, 0.176, 0.12, 0.42), (1.53, 0.154, 0.104, 0.56),
                 (1.575, 0.104, 0.08, 0.7)]
        self.shell([(z, rx, ry, a, TAU - a) for z, rx, ry, a in shirt], r["shirt"], "chest", thickness=0.005)
        for sx in (1, -1):
            k.beam(Vector((0.046 * sx, -0.1, 1.545)), Vector((0.0, -0.127, 1.425)), 0.0035, 0.003, "chernozem", "chest")
        k.box(Vector((0.0, -0.13, 1.405)), (0.008, 0.005, 0.034), "steel_light", "chest")
        k.box(Vector((0.0, -0.13, 1.41)), (0.024, 0.005, 0.007), "steel_light", "chest")
        # the coat over the chest and the waist, open in a V that narrows to the sash
        chest = [(1.3, 0.178, 0.12, 0.2), (1.38, 0.194, 0.13, 0.3), (1.46, 0.198, 0.134, 0.46),
                 (1.52, 0.18, 0.124, 0.64), (1.56, 0.132, 0.1, 0.84)]
        waist = [(1.0, 0.158, 0.116, 0.05), (1.1, 0.154, 0.112, 0.08), (1.2, 0.162, 0.114, 0.13), (1.3, 0.178, 0.12, 0.2)]
        for part, bone in ((chest, "chest"), (waist, "spine")):
            self.shell([(z, rx, ry, a, TAU - a) for z, rx, ry, a in part], coat, bone, thickness=0.01, inner=lining)
        # the lapels: the fronts turned back over the chest, wide at the collar and narrowing to
        # nothing at the waist, the lining outwards, embroidered round their edge
        lapel = [(1.3, 0.181, 0.122, 0.2, 0.0), (1.38, 0.197, 0.133, 0.3, 0.08), (1.46, 0.201, 0.137, 0.46, 0.2),
                 (1.52, 0.183, 0.127, 0.64, 0.26), (1.556, 0.138, 0.104, 0.82, 0.22)]
        for side in (1, -1):
            ring = [(z, rx, ry, a, a + w + 0.02) if side > 0 else (z, rx, ry, TAU - a - w - 0.02, TAU - a)
                    for z, rx, ry, a, w in lapel]
            self.shell(ring, lining, "chest", segs=4, thickness=0.004)
            self.edges([(z, rx * 1.004, ry * 1.004, a + w, TAU - a - w) for z, rx, ry, a, w in lapel], trim, "chest",
                       only=side)
        self.edges([(z, rx, ry, a, TAU - a) for z, rx, ry, a in waist], trim, "spine")
        self.lozenges([(z, rx, ry, a) for z, rx, ry, a in waist if z < 1.25], "spine")
        # the standing collar: round the back and the sides of the neck, flaring, open in front
        collar = [(1.548, 0.118, 0.094, 0.92), (1.6, 0.124, 0.106, 1.1), (1.655, 0.142, 0.126, 1.4)]
        self.shell([(z, rx, ry, a, TAU - a) for z, rx, ry, a in collar], coat, "chest", thickness=0.008, inner=lining)
        self.shell([(z, rx * 1.012, ry * 1.012, a - 0.02, TAU - a + 0.02) for z, rx, ry, a in
                    [(1.638, 0.138, 0.122, 1.36), (1.657, 0.143, 0.127, 1.4)]], trim, "chest", thickness=0.005)
        self.skirt(r)
        self.sash(r)

    def skirt(self, r):
        """The zhupan's skirt in two halves that follow the thighs down to the calves, parting at
        the front, a vent at the back, embroidered down the front edges and round the hem."""
        coat, lining, trim = r["coat"], r["lining"], r["coat_trim"]
        hem = 0.3
        rings = [(hem, 0.29, 0.25, 0.5, 0.06), (0.45, 0.262, 0.222, 0.4, 0.045), (0.62, 0.228, 0.192, 0.28, 0.03),
                 (0.78, 0.196, 0.162, 0.18, 0.015), (0.92, 0.17, 0.134, 0.1, 0.0), (1.02, 0.162, 0.12, 0.06, 0.0)]
        for side, bone in ((1, "upperleg.l"), (-1, "upperleg.r")):
            ring = [(z, rx, ry, a, math.pi - 0.035, f) if side > 0 else (z, rx, ry, math.pi + 0.035, TAU - a, f)
                    for z, rx, ry, a, f in rings]
            self.shell(ring, coat, bone, thickness=0.01, inner=lining, folds=5)
            self.edges([(z, rx, ry, a, TAU - a) for z, rx, ry, a, f in rings], trim, bone, only=side)
            self.lozenges([(z, rx, ry, a) for z, rx, ry, a, f in rings[1:]], bone, only=side)
            bottom = [ring[0], (hem + 0.06,) + tuple(ring[0][1:])]
            self.shell([(z, rx * 1.008, ry * 1.008, a0, a1, f) for z, rx, ry, a0, a1, f in bottom], trim, bone,
                       thickness=0.005, folds=5)

    def sash(self, r):
        """A wide sash, its knot and long ends on the left hip; a belt over it with a silver
        buckle, a pouch on the right, wide sharovary under the coat."""
        k, sash = self.k, r["sash"]
        k.lathe((0, 0, 0), [(0.98, 0.172, "hard"), (1.0, 0.178), (1.11, 0.176), (1.13, 0.17, "hard")],
                sash, "spine", segs=self.SEGS, sx=1.0, sy=0.72)
        k.lathe((0, 0, 0), [(1.035, 0.182, "hard"), (1.075, 0.182, "hard")], "leather", "spine", segs=self.SEGS,
                sx=1.0, sy=0.72)
        k.box(Vector((0, -0.134, 1.055)), (0.05, 0.012, 0.046), "steel_light", "spine")
        k.box(Vector((0, -0.139, 1.055)), (0.03, 0.006, 0.026), r["coat"], "spine")
        knot = Vector((0.155, -0.07, 1.04))
        k.ball(knot, (0.034, 0.032, 0.038), sash, "hips", segs=12, rings=6)
        for dx, length in ((0.0, 0.4), (0.03, 0.32)):
            top = knot + Vector((0.008 + dx * 0.5, -0.004 + dx * 0.3, -0.02))
            k.box(top + Vector((0, 0, -length / 2)), (0.024, 0.064, length), sash, "hips", taper=0.85)
            k.box(top + Vector((0, 0, -length - 0.015)), (0.022, 0.056, 0.03), r["coat_trim"], "hips")
        k.box(Vector((-0.17, -0.04, 0.98)), (0.04, 0.07, 0.08), "leather", "hips")
        k.lathe((0, 0, 0), [(0.84, 0.136), (0.93, 0.15), (1.0, 0.144), (1.04, 0.134)], r["trousers"], "hips",
                segs=self.SEGS, sx=1.16, sy=0.88)

    def lozenges(self, rings, bone, only=0, step=0.07):
        """Silver lozenges down the embroidery of an opening's edges (rings (z, rx, ry, a) of the
        right half's edge at the angle a), one every `step` metres."""
        for side in (1, -1):
            if only and side != only:
                continue
            for (z0, rx0, ry0, a0), (z1, rx1, ry1, a1) in zip(rings, rings[1:]):
                n = max(1, int(abs(z1 - z0) / step))
                for i in range(n):
                    t = (i + 0.5) / n
                    z, rx, ry = z0 + (z1 - z0) * t, rx0 + (rx1 - rx0) * t, ry0 + (ry1 - ry0) * t
                    a = (a0 + (a1 - a0) * t + 0.035) * side
                    at = Vector((rx * 1.02 * math.sin(a), -ry * 1.02 * math.cos(a), z))
                    turn = Matrix.Rotation(math.atan2(rx * math.sin(a), ry * math.cos(a)), 4, "Z")
                    self.k.box(at, (0.011, 0.003, 0.016), "steel_light", bone,
                               rot=turn @ Matrix.Rotation(math.pi / 4, 4, "Y"))

    def edges(self, rings, trim, bone, only=0):
        """Embroidery down both edges of an opening (rings of shell()): a band with a silver
        thread inside it; `only` 1 or -1 for just the left or the right edge."""
        for side in (1, -1):
            if only and side != only:
                continue
            band = [(z, rx * 1.01, ry * 1.01, a0, a0 + 0.1) if side > 0 else (z, rx * 1.01, ry * 1.01, a1 - 0.1, a1)
                    for z, rx, ry, a0, a1 in rings]
            self.shell(band, trim, bone, segs=2, thickness=0.004)
            line = [(z, rx * 1.014, ry * 1.014, a0 + 0.07, a0 + 0.082) if side > 0 else
                    (z, rx * 1.014, ry * 1.014, a1 - 0.082, a1 - 0.07) for z, rx, ry, a0, a1 in rings]
            self.shell(line, "steel_light", bone, segs=1, thickness=0.002)

    def sleeve(self, r, side):
        """The zhupan's sleeve over a lean strong arm, a wide cuff with a silver thread, a dark
        leather guard at the wrist, a bare hand."""
        k, s = self.k, 1 if side == "l" else -1
        ua, la, hd = "upperarm." + side, "lowerarm." + side, "hand." + side
        sh, el, wr = self.h(ua), self.h(la), self.h("wrist." + side)
        coat, trim = r["coat"], r["coat_trim"]
        k.ball(sh + Vector((0.008 * s, 0, 0.004)), (0.074, 0.07, 0.072), coat, ua, segs=16, rings=8)
        k.along(sh, el, [(-0.04, 0.058), (0.0, 0.068), (0.35, 0.068), (0.6, 0.061), (0.9, 0.054), (1.05, 0.052)],
                coat, ua, segs=16, sy=1.04)
        k.ball(el, 0.052, coat, la, segs=12, rings=6)
        k.along(el, wr, [(0.0, 0.052), (0.3, 0.054), (0.6, 0.049), (0.62, 0.0)], coat, la, segs=14)
        k.along(el, wr, [(0.56, 0.0), (0.56, 0.056, "hard"), (0.9, 0.06), (0.96, 0.062), (0.97, 0.0)], trim, la,
                segs=14)
        k.along(el, wr, [(0.72, 0.0), (0.72, 0.0612, "hard"), (0.74, 0.0618), (0.741, 0.0)], "steel_light", la,
                segs=14)
        k.along(el, wr, [(0.9, 0.0), (0.9, 0.04, "hard"), (1.06, 0.038), (1.07, 0.0)], "chernozem", la, segs=12)
        k.along(wr - Vector((0.02 * s, 0, 0)), self.h(hd) + Vector((0.02 * s, 0, 0)), [(0.0, 0.034), (1.0, 0.036)],
                "skin", "wrist." + side, segs=12)
        hc = self.h(hd) + Vector((0.026 * s, -0.004, -0.01))
        k.ball(hc, (0.045, 0.034, 0.042), "skin", hd, segs=12, rings=7)
        k.ball(hc + Vector((-0.015 * s, -0.03, 0.007)), (0.016, 0.014, 0.013), "skin", hd, segs=8, rings=5)

    def leg(self, r, side):
        """Sharovary bloused over the tops of tall slim boots, a band round each top."""
        k = self.k
        ul, ll, ft, to = ("upperleg." + side, "lowerleg." + side, "foot." + side, "toes." + side)
        hip, knee, ankle, ball = self.h(ul), self.h(ll), self.h(ft), self.h(to)
        trousers, boots, x = r["trousers"], r["boots"], hip.x
        k.along(hip, knee, [(-0.05, 0.1), (0.25, 0.116), (0.62, 0.11), (0.92, 0.094), (1.08, 0.088)], trousers, ul,
                segs=16)
        k.along(knee, ankle, [(-0.06, 0.084), (0.08, 0.09), (0.2, 0.082), (0.26, 0.0)], trousers, ll, segs=16)
        k.along(knee, ankle, [(0.16, 0.0), (0.16, 0.064, "hard"), (0.3, 0.06), (0.62, 0.05), (1.0, 0.044),
                              (1.12, 0.043)], boots, ll, segs=16)
        k.along(knee, ankle, [(0.17, 0.0), (0.17, 0.0665, "hard"), (0.23, 0.065), (0.231, 0.0)], r["boot_band"], ll,
                segs=16)
        k.ball(Vector((x, -0.004, 0.066)), (0.047, 0.088, 0.058), boots, ft, segs=14, rings=7)
        k.box(Vector((x, 0.042, 0.018)), (0.058, 0.052, 0.036), r["coat"], ft)
        k.ball(Vector((x, ball.y - 0.036, 0.032)), (0.043, 0.075, 0.031), boots, to, segs=14, rings=6)
        k.ball(Vector((x, ball.y - 0.098, 0.036)), (0.02, 0.03, 0.018), boots, to, segs=8, rings=5)

    def build(self, r):
        neck = self.h("head")
        self.k.pre = Matrix.Translation(neck) @ Matrix.Scale(HEAD, 4) @ Matrix.Translation(-neck)
        self.head(r)
        self.oseledets(r)
        self.k.pre = None
        self.zhupan(r)
        for side in ("l", "r"):
            self.sleeve(r, side)
            self.leg(r, side)
        return self.k


def build(name, bones, deform, armature):
    return HeroFigure(bones, deform).build(RECIPES[name]).to_object(name, armature)
