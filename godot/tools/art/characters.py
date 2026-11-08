"""People of the game, built as jointed wooden figures on the shared skeleton.

Each recipe below names a hat, a face, a coat, trousers, boots and colours; `build()`
turns it into one skinned mesh. Silhouette says who the figure is (hat, coat cut,
armour, weapon); the sash colour says whose side it is on (FACTIONS).
"""

import math

from mathutils import Matrix, Vector

from mesh_kit import MeshKit

FACTIONS = {
    "hetman": "gold",       # the hero's regiment
    "crown": "whitewash",   # Crown army
    "rival": "oak",         # Cossacks of a rival colonel
    "horde": "crimson",     # the Crimean horde
}

RECIPES = {
    "kozak": {
        "hat": "shlyk", "hat_cloth": "cinnabar", "hair": "hair", "face": "mustache",
        "coat": "cinnabar", "coat_trim": "cinnabar_dark", "coat_len": "knee", "buttons": "gold",
        "sash": FACTIONS["hetman"], "trousers": "blue", "boots": "leather",
    },
    "kozak_camp": {
        "hat": "oseledets", "hair": "hair", "face": "mustache",
        "coat": "whitewash", "coat_trim": "canvas_dark", "coat_len": "shirt",
        "sash": "cinnabar", "trousers": "blue", "boots": "leather",
    },
    "kozak_svyta": {
        "hat": "kuchma", "hair": "hair_grey", "face": "mustache",
        "coat": "wood_dark", "coat_trim": "fur", "coat_len": "knee",
        "sash": FACTIONS["hetman"], "trousers": "cinnabar_dark", "boots": "leather",
    },
    "zholner": {
        "hat": "shyshak", "hair": "hair", "face": "short_mustache",
        "coat": "blue_dark", "coat_trim": "dusk", "coat_len": "thigh", "armour": "cuirass",
        "sash": FACTIONS["crown"], "trousers": "stone_dark", "boots": "chernozem",
    },
    "luchnyk": {
        "hat": "kolpak", "hat_cloth": "oak_dark", "hair": "hair", "face": "short_mustache",
        "coat": "oak", "coat_trim": "oak_dark", "coat_len": "thigh",
        "sash": FACTIONS["crown"], "trousers": "grass_dark", "boots": "leather", "quiver": True,
    },
    "polkovnyk": {
        "hat": "plume", "hat_cloth": "cinnabar", "hair": "hair_grey", "face": "long_mustache",
        "coat": "blue", "coat_trim": "gold", "coat_len": "long", "buttons": "gold",
        "undercoat": "cinnabar", "sash": "gold", "trousers": "cinnabar_dark", "boots": "gold_dark",
        "belly": 1.12, "hanging_sleeves": True,
    },
    # the hero's four classes (Profile.HERO_CLASSES): Cossack is "kozak" above
    "serdiuk": {
        "hat": "misiurka", "hair": "hair", "face": "mustache",
        "coat": "blue", "coat_trim": "blue_dark", "coat_len": "knee", "armour": "mail",
        "sash": FACTIONS["hetman"], "trousers": "cinnabar_dark", "boots": "chernozem",
    },
    "kharakternyk": {
        "hat": "kuchma", "hat_fur": "fur", "hair": "hair_grey", "face": "long_mustache",
        "coat": "dusk", "coat_trim": "oak_dark", "coat_len": "long", "amulet": True,
        "sash": FACTIONS["hetman"], "trousers": "blue_dark", "boots": "leather",
    },
    "haidamaka": {
        "hat": "kolpak_tall", "hat_cloth": "cinnabar", "hair": "hair", "face": "mustache",
        "coat": "whitewash", "coat_trim": "canvas_dark", "coat_len": "shirt", "vest": "fur_grey",
        "sash": FACTIONS["hetman"], "trousers": "blue", "boots": "leather",
    },
    # Cossacks of a rival colonel
    "kozak_rival": {
        "hat": "kuchma", "hair": "hair", "face": "mustache",
        "coat": "stone", "coat_trim": "fur", "coat_len": "knee",
        "sash": FACTIONS["rival"], "trousers": "oak_dark", "boots": "leather",
    },
    "kozak_rival_luk": {
        "hat": "kolpak", "hat_cloth": "oak_dark", "hair": "hair", "face": "mustache",
        "coat": "grass_dark", "coat_trim": "wood_dark", "coat_len": "thigh",
        "sash": FACTIONS["rival"], "trousers": "stone_dark", "boots": "leather", "quiver": True,
    },
    # the horde
    "tatar": {
        "hat": "tatar", "hat_cloth": "cinnabar_dark", "hair": "hair", "face": "short_mustache", "beard": True,
        "coat": "blue_light", "coat_trim": "fur", "coat_len": "knee",
        "sash": FACTIONS["horde"], "trousers": "cinnabar_dark", "boots": "leather_light",
    },
    "tatar_luk": {
        "hat": "tatar", "hat_cloth": "oak_dark", "hair": "hair", "face": "short_mustache", "beard": True,
        "coat": "canvas", "coat_trim": "fur", "coat_len": "thigh",
        "sash": FACTIONS["horde"], "trousers": "cinnabar_dark", "boots": "leather_light", "quiver": True,
    },
    # generals of the Crown and of the horde (the Cossack one is "polkovnyk")
    "rotmistr": {
        "hat": "kolpak_noble", "hat_cloth": "crimson", "hair": "hair", "face": "long_mustache",
        "coat": "crimson", "coat_trim": "gold", "coat_len": "long", "buttons": "gold",
        "undercoat": "gold", "sash": FACTIONS["crown"], "trousers": "blue_dark", "boots": "gold_dark",
        "belly": 1.08, "hanging_sleeves": True,
    },
    "murza": {
        "hat": "murza", "hair": "hair", "face": "long_mustache", "beard": True,
        "coat": "blue_dark", "coat_trim": "gold", "coat_len": "long", "buttons": "gold",
        "undercoat": "ochre", "sash": FACTIONS["horde"], "trousers": "cinnabar_dark", "boots": "gold_dark",
        "belly": 1.1,
    },
}


class Figure:
    def __init__(self, bones, deform):
        self.b = bones
        self.k = MeshKit(deform)

    def h(self, name):
        return Vector(self.b[name][0])

    def t(self, name):
        return Vector(self.b[name][1])

    # -- head -----------------------------------------------------------------
    def head(self, r):
        k = self.k
        c = self.h("head") + Vector((0, 0, 0.125))
        self.head_center = c
        k.ball(c, (0.108, 0.112, 0.128), "skin", "head", segs=14, rings=8)
        k.tube(self.h("head") + Vector((0, 0.01, -0.07)), c, 0.052, 0.05, "skin_dark", "head", segs=8)
        k.ball(c + Vector((0, -0.112, -0.012)), (0.022, 0.03, 0.032), "skin_dark", "head", segs=8, rings=5)
        for sx in (1, -1):
            k.ball(c + Vector((0.042 * sx, -0.098, 0.022)), (0.016, 0.01, 0.016), "chernozem", "head", segs=6, rings=4)
            k.box(c + Vector((0.045 * sx, -0.1, 0.048)), (0.04, 0.012, 0.012), r["hair"], "head",
                  rot=Matrix.Rotation(-0.12 * sx, 4, "Y"))
            k.ball(c + Vector((0.108 * sx, 0.0, -0.005)), (0.018, 0.028, 0.034), "skin_dark", "head", segs=6, rings=4)
        face = r.get("face", "mustache")
        if face in ("mustache", "long_mustache", "short_mustache"):
            droop = {"mustache": 0.11, "long_mustache": 0.17, "short_mustache": 0.04}[face]
            reach = {"mustache": 0.085, "long_mustache": 0.1, "short_mustache": 0.07}[face]
            for sx in (1, -1):
                pts = [c + Vector((0.008 * sx, -0.122, -0.04)),
                       c + Vector((0.045 * sx, -0.118, -0.05)),
                       c + Vector((reach * sx, -0.095, -0.05 - droop * 0.5)),
                       c + Vector((reach * 1.05 * sx, -0.075, -0.05 - droop))]
                k.sweep(pts, [0.017, 0.02, 0.013, 0.005], r["hair"], "head", segs=6, flat=0.7)
        if r.get("beard"):
            k.ball(c + Vector((0, -0.088, -0.118)), (0.05, 0.045, 0.06), r["hair"], "head", segs=8, rings=5)

    def hat(self, r):
        k, c = self.k, self.head_center
        kind = r.get("hat")
        if kind == "kuchma":
            k.lathe(c + Vector((0, 0, 0.03)),
                    [(0.0, 0.118, "hard"), (0.04, 0.138), (0.12, 0.136), (0.18, 0.1), (0.205, 0.0)],
                    r.get("hat_fur", "fur_grey"), "head", segs=14, sx=1.0, sy=1.04)
        if kind in ("shlyk", "plume"):
            k.lathe(c + Vector((0, 0, 0.035)),
                    [(0.0, 0.118, "hard"), (0.03, 0.128), (0.12, 0.132), (0.155, 0.12, "hard"), (0.16, 0.0)],
                    "fur", "head", segs=14, sx=1.0, sy=1.04)
            if kind in ("shlyk", "plume"):
                cloth = r.get("hat_cloth", "cinnabar")
                top = c + Vector((0, 0.0, 0.19))
                pts = [top, top + Vector((0.0, 0.04, 0.07)), top + Vector((-0.04, 0.11, 0.06)),
                       top + Vector((-0.08, 0.15, -0.02)), top + Vector((-0.1, 0.15, -0.1))]
                k.sweep(pts, [0.1, 0.085, 0.06, 0.04, 0.025], cloth, "head", segs=10)
                k.ball(pts[-1] + Vector((0, 0, -0.025)), 0.028, "gold", "head", segs=8, rings=5)
            if kind == "plume":
                front = c + Vector((0.0, -0.12, 0.13))
                k.ball(front, (0.03, 0.015, 0.035), "gold", "head", segs=8, rings=5)
                k.ball(front + Vector((0, -0.012, 0)), 0.012, "cinnabar", "head", segs=6, rings=4)
                pts = [front + Vector((0, 0.0, 0.02)), front + Vector((0.0, 0.02, 0.16)),
                       front + Vector((0.0, 0.08, 0.28)), front + Vector((0.0, 0.17, 0.33))]
                k.sweep(pts, [0.02, 0.035, 0.03, 0.006], "whitewash", "head", segs=6, flat=0.45)
        elif kind == "oseledets":
            k.ball(c + Vector((0, 0.005, 0.01)), (0.111, 0.116, 0.126), "skin", "head", segs=14, rings=8)
            pts = [c + Vector((0.0, -0.03, 0.128)), c + Vector((0.04, -0.01, 0.135)),
                   c + Vector((0.09, 0.01, 0.1)), c + Vector((0.118, 0.0, 0.03)),
                   c + Vector((0.12, -0.02, -0.06))]
            k.sweep(pts, [0.03, 0.03, 0.024, 0.016, 0.006], r["hair"], "head", segs=6, flat=0.6)
        elif kind == "shyshak":
            k.lathe(c + Vector((0, 0, 0.0)),
                    [(0.0, 0.122, "hard"), (0.06, 0.125), (0.12, 0.105), (0.17, 0.06), (0.195, 0.02, "hard"),
                     (0.23, 0.008), (0.235, 0.0)],
                    "steel", "head", segs=14)
            k.lathe(c + Vector((0, 0.0, -0.002)),
                    [(-0.12, 0.17, "hard"), (-0.06, 0.15), (0.005, 0.124)], "steel", "head",
                    segs=14, a0=math.radians(100), a1=math.radians(260), thickness=0.01)
            k.box(c + Vector((0, -0.118, 0.0)), (0.12, 0.05, 0.016), "steel", "head",
                  rot=Matrix.Rotation(0.35, 4, "X"))
            k.beam(c + Vector((0, -0.128, 0.03)), c + Vector((0, -0.128, -0.07)), 0.014, 0.01, "steel_light", "head")
            for sx in (1, -1):
                k.box(c + Vector((0.11 * sx, -0.03, -0.05)), (0.012, 0.07, 0.1), "steel", "head",
                      rot=Matrix.Rotation(0.12 * sx, 4, "Y"))
        elif kind == "kolpak":
            cloth = r.get("hat_cloth", "oak_dark")
            k.lathe(c + Vector((0, 0, 0.04)),
                    [(0.0, 0.124, "hard"), (0.05, 0.132), (0.07, 0.13, "hard"), (0.072, 0.0)],
                    "fur", "head", segs=14)
            k.lathe(c + Vector((0, 0.01, 0.1)),
                    [(0.0, 0.112, "hard"), (0.08, 0.1), (0.17, 0.07), (0.2, 0.0)],
                    cloth, "head", segs=12, rot=Matrix.Rotation(-0.25, 4, "X"))
            k.ball(c + Vector((0.0, -0.02, 0.125)), (0.012, 0.03, 0.08), "whitewash", "head",
                   rot=Matrix.Rotation(-0.2, 4, "X"), segs=6, rings=4)

        elif kind == "misiurka":
            # a low steel cap with a spike and a mail curtain over the neck
            k.lathe(c + Vector((0, 0, 0.02)),
                    [(0.0, 0.126, "hard"), (0.05, 0.126), (0.1, 0.102), (0.14, 0.05), (0.155, 0.0)],
                    "steel", "head", segs=14)
            k.tube(c + Vector((0, 0, 0.16)), c + Vector((0, 0, 0.24)), 0.012, 0.003, "steel_light", "head", segs=6)
            k.lathe(c + Vector((0, 0, 0.0)), [(-0.2, 0.175, "hard"), (-0.1, 0.152), (0.025, 0.128)], "iron", "head",
                    segs=14, a0=math.radians(65), a1=math.radians(295), thickness=0.012)
        elif kind == "tatar":
            # a cloth cone on a rolled fur brim
            cloth = r.get("hat_cloth", "cinnabar_dark")
            k.lathe(c + Vector((0, 0, 0.03)),
                    [(0.0, 0.124, "hard"), (0.02, 0.142), (0.06, 0.144), (0.08, 0.12, "hard"), (0.081, 0.0)],
                    "fur", "head", segs=14)
            k.lathe(c + Vector((0, 0, 0.1)), [(0.0, 0.118, "hard"), (0.07, 0.1), (0.15, 0.06), (0.22, 0.0)],
                    cloth, "head", segs=12)
            k.ball(c + Vector((0, 0, 0.32)), 0.02, "gold", "head", segs=6, rings=4)
        elif kind == "murza":
            # a tall grey fur cap with a gold top and a jewel
            k.lathe(c + Vector((0, 0, 0.03)),
                    [(0.0, 0.126, "hard"), (0.05, 0.145), (0.16, 0.14), (0.21, 0.1), (0.235, 0.0)],
                    "fur_grey", "head", segs=14)
            k.ball(c + Vector((0, 0, 0.27)), 0.032, "gold", "head", segs=8, rings=5)
            front = c + Vector((0, -0.142, 0.1))
            k.ball(front, (0.03, 0.014, 0.034), "gold", "head", segs=8, rings=5)
            k.ball(front + Vector((0, -0.01, 0)), 0.014, "blue", "head", segs=6, rings=4)
        elif kind == "kolpak_noble":
            # a nobleman's cap: a fur band, a cloth crown, a jewel and a heron feather
            cloth = r.get("hat_cloth", "crimson")
            k.lathe(c + Vector((0, 0, 0.035)),
                    [(0.0, 0.124, "hard"), (0.03, 0.136), (0.09, 0.136), (0.1, 0.1, "hard"), (0.101, 0.0)],
                    "fur_grey", "head", segs=14)
            k.lathe(c + Vector((0, 0, 0.11)), [(0.0, 0.112, "hard"), (0.05, 0.106), (0.09, 0.06), (0.11, 0.0)],
                    cloth, "head", segs=12)
            front = c + Vector((0, -0.138, 0.09))
            k.ball(front, (0.03, 0.014, 0.034), "gold", "head", segs=8, rings=5)
            k.ball(front + Vector((0, -0.012, 0)), 0.012, "cinnabar", "head", segs=6, rings=4)
            pts = [front + Vector((0, 0.0, 0.02)), front + Vector((0.0, 0.03, 0.18)),
                   front + Vector((0.0, 0.08, 0.3)), front + Vector((0.0, 0.15, 0.36))]
            k.sweep(pts, [0.012, 0.03, 0.025, 0.004], "whitewash", "head", segs=6, flat=0.45)
        elif kind == "kolpak_tall":
            # the haidamaka's tall cloth cap, its top falling back
            cloth = r.get("hat_cloth", "cinnabar")
            k.lathe(c + Vector((0, 0, 0.035)),
                    [(0.0, 0.124, "hard"), (0.04, 0.138), (0.1, 0.136), (0.11, 0.1, "hard"), (0.111, 0.0)],
                    "fur", "head", segs=14)
            pts = [c + Vector((0, 0, 0.12)), c + Vector((0, 0.02, 0.24)), c + Vector((0, 0.06, 0.33)),
                   c + Vector((0, 0.13, 0.37)), c + Vector((0, 0.19, 0.31))]
            k.sweep(pts, [0.112, 0.1, 0.08, 0.05, 0.028], cloth, "head", segs=10)
            k.ball(pts[-1] + Vector((0, 0.01, -0.03)), 0.026, "gold", "head", segs=8, rings=5)

    # -- body -----------------------------------------------------------------
    def torso(self, r):
        k = self.k
        belly = r.get("belly", 1.0)
        coat, trim = r["coat"], r.get("coat_trim", r["coat"])
        chest_top = self.t("chest").z
        k.lathe((0, 0, 0), [(1.29, 0.15 * belly), (1.39, 0.158), (1.46, 0.152), (1.51, 0.118), (chest_top + 0.005, 0.07)],
                coat, "chest", segs=14, sx=1.18, sy=0.82)
        k.lathe((0, 0, 0), [(1.045, 0.136 * belly), (1.17, 0.146 * belly), (1.31, 0.15 * belly)],
                coat, "spine", segs=14, sx=1.15, sy=0.84)
        k.lathe((0, 0, 0), [(chest_top - 0.02, 0.072), (chest_top + 0.03, 0.06)],
                "whitewash", "chest", segs=10, sx=1.0, sy=0.95)
        if r.get("undercoat"):
            # the inner coat shows in the open front of the outer one
            k.box((0, -0.122, 1.19), (0.1, 0.03, 0.24), r["undercoat"], "spine", taper=1.2)
            k.box((0, -0.124, 1.41), (0.12, 0.03, 0.2), r["undercoat"], "chest", taper=0.8)
        if r.get("armour") == "cuirass":
            k.lathe((0, 0, 0), [(1.06, 0.15, "hard"), (1.2, 0.163), (1.36, 0.17), (1.47, 0.16), (1.52, 0.12, "hard")],
                    "steel", "chest", segs=14, sx=1.17, sy=0.86)
            k.lathe((0, 0, 0), [(1.0, 0.152, "hard"), (1.08, 0.158, "hard")], "steel_light", "spine",
                    segs=14, sx=1.16, sy=0.86)
            for sx in (1, -1):
                k.ball(self.h("upperarm.l" if sx > 0 else "upperarm.r") + Vector((0.01 * sx, 0, 0.02)),
                       (0.095, 0.09, 0.07), "steel", "upperarm.l" if sx > 0 else "upperarm.r", segs=10, rings=5)
        if r.get("armour") == "mail":
            # mail from the shoulders to the sash
            k.lathe((0, 0, 0), [(1.29, 0.164 * belly), (1.39, 0.17), (1.46, 0.164), (1.52, 0.124, "hard")],
                    "iron", "chest", segs=14, sx=1.18, sy=0.84)
            k.lathe((0, 0, 0), [(1.13, 0.156 * belly, "hard"), (1.2, 0.158 * belly), (1.31, 0.164 * belly)],
                    "iron", "spine", segs=14, sx=1.16, sy=0.85)
            for sx in (1, -1):
                k.ball(self.h("upperarm.l" if sx > 0 else "upperarm.r") + Vector((0.01 * sx, 0, 0.0)),
                       (0.095, 0.09, 0.08), "iron", "upperarm.l" if sx > 0 else "upperarm.r", segs=10, rings=5)
        if r.get("vest"):
            # a sheepskin vest, open in front
            a0, a1 = math.radians(30), math.radians(330)
            k.lathe((0, 0, 0), [(1.29, 0.162 * belly), (1.39, 0.17), (1.46, 0.164), (1.52, 0.124, "hard")],
                    r["vest"], "chest", segs=14, sx=1.18, sy=0.84, a0=a0, a1=a1, thickness=0.02)
            k.lathe((0, 0, 0), [(0.96, 0.17 * belly, "hard"), (1.17, 0.158 * belly), (1.31, 0.162 * belly)],
                    r["vest"], "spine", segs=14, sx=1.16, sy=0.85, a0=a0, a1=a1, thickness=0.02)
        if r.get("amulet"):
            k.beam(Vector((0.06, -0.1, 1.5)), Vector((0.0, -0.135, 1.36)), 0.008, 0.006, "leather", "chest")
            k.beam(Vector((-0.06, -0.1, 1.5)), Vector((0.0, -0.135, 1.36)), 0.008, 0.006, "leather", "chest")
            k.ball(Vector((0.0, -0.14, 1.34)), (0.036, 0.012, 0.036), "gold", "chest", segs=10, rings=5)
            k.ball(Vector((0.0, -0.152, 1.34)), 0.012, "cinnabar", "chest", segs=6, rings=4)
        # sash
        sash = r["sash"]
        k.lathe((0, 0, 0), [(1.02, 0.142 * belly, "hard"), (1.045, 0.152 * belly), (1.105, 0.152 * belly), (1.13, 0.142 * belly, "hard")],
                sash, "spine", segs=14, sx=1.15, sy=0.86)
        knot = Vector((0.16 * belly, -0.06, 1.06))
        k.ball(knot, (0.03, 0.035, 0.035), sash, "hips", segs=8, rings=5)
        for dx, dz in ((0.0, 0.0), (0.03, -0.01)):
            k.box(knot + Vector((0.005 + dx * 0.5, -0.005 + dx, -0.12 + dz)), (0.018, 0.05, 0.2), sash, "hips", taper=0.9)
        buttons = r.get("buttons")
        if buttons and r.get("armour") != "cuirass":
            for z, bone in ((1.17, "spine"), (1.25, "spine"), (1.34, "chest"), (1.42, "chest")):
                y = -0.15 * 0.84 * (belly if z < 1.3 else 1.0) - 0.006
                k.ball((0, y, z), 0.014, buttons, bone, segs=6, rings=4)
        # skirt panels follow the thighs so the legs never cut through them
        length = r.get("coat_len", "knee")
        if length != "shirt":
            bottom = {"thigh": 0.74, "knee": 0.6, "long": 0.42}[length]
            flare = {"thigh": 0.205, "knee": 0.24, "long": 0.27}[length] * belly
            prof = [(bottom, flare, "hard"), ((bottom + 0.9) / 2, (flare + 0.16) / 2), (0.92, 0.158 * belly), (1.04, 0.142 * belly)]
            hem = [(bottom - 0.005, flare + 0.008, "hard"), (bottom + 0.045, flare - 0.004)]
            for side, (a0, a1) in (("l", (15, 170)), ("r", (190, 345))):
                bone = "upperleg." + side
                k.lathe((0, 0, 0), prof, coat, bone, segs=8, sx=1.12, sy=0.92,
                        a0=math.radians(a0), a1=math.radians(a1), thickness=0.012)
                k.lathe((0, 0, 0), hem, trim, bone, segs=8, sx=1.12, sy=0.92,
                        a0=math.radians(a0), a1=math.radians(a1), thickness=0.014)
        else:
            k.lathe((0, 0, 0), [(0.9, 0.165, "hard"), (0.97, 0.15), (1.04, 0.14)], coat, "hips", segs=12, sx=1.12, sy=0.9)
        k.lathe((0, 0, 0), [(0.84, 0.13), (0.95, 0.15), (1.05, 0.136)], r["trousers"], "hips", segs=12, sx=1.15, sy=0.86)
        if r.get("quiver"):
            base = Vector((-0.07, 0.15, 1.12))
            top = Vector((0.1, 0.17, 1.55))
            k.tube(base, top, 0.05, 0.06, "leather", "chest", segs=8)
            for i, dx in enumerate((-0.02, 0.0, 0.02)):
                tip = top + Vector((dx, 0.0, 0.0)) + (top - base).normalized() * 0.1
                k.tube(top, tip, 0.006, 0.006, "wood_light", "chest", segs=4)
                k.box(tip, (0.03, 0.006, 0.05), "whitewash", "chest")
            k.beam(Vector((0.16, -0.12, 1.47)), Vector((-0.12, 0.13, 1.08)), 0.03, 0.012, "leather_light", "chest")

    def arm(self, r, side):
        k, s = self.k, 1 if side == "l" else -1
        coat, trim = r["coat"], r.get("coat_trim", r["coat"])
        ua, la, hd = "upperarm." + side, "lowerarm." + side, "hand." + side
        sh, el, wr = self.h(ua), self.h(la), self.h("wrist." + side)
        if not r.get("armour"):
            k.ball(sh + Vector((0.01 * s, 0, 0)), (0.085, 0.08, 0.08), coat, ua, segs=10, rings=6)
        k.along(sh, el, [(-0.05, 0.06), (0.0, 0.075), (0.5, 0.07), (1.0, 0.06), (1.06, 0.056)], coat, ua, segs=10)
        k.ball(el, 0.058, coat, la, segs=8, rings=5)
        k.along(el, wr, [(0.0, 0.058), (0.72, 0.05)], coat, la, segs=10)
        k.along(el, wr, [(0.7, 0.056, "hard"), (0.75, 0.064), (1.0, 0.066), (1.02, 0.0)], trim, la, segs=10)
        if r.get("hanging_sleeves"):
            k.along(sh + Vector((0.02 * s, 0.08, -0.02)), sh + Vector((0.08 * s, 0.14, -0.62)),
                    [(0.0, 0.045), (0.7, 0.06), (1.0, 0.04), (1.01, 0.0)], coat, "chest", segs=8, sx=1.0, sy=0.5)
        k.along(self.h("wrist." + side) - Vector((0.02 * s, 0, 0)), self.h(hd) + Vector((0.02 * s, 0, 0)),
                [(0.0, 0.04), (1.0, 0.042)], "skin", "wrist." + side, segs=8)
        hc = self.h(hd) + Vector((0.03 * s, -0.005, -0.012))
        k.ball(hc, (0.062, 0.046, 0.056), "skin", hd, segs=10, rings=6)
        k.ball(hc + Vector((-0.02 * s, -0.04, 0.008)), (0.022, 0.02, 0.018), "skin", hd, segs=6, rings=4)

    def leg(self, r, side):
        k = self.k
        ul, ll, ft, to = ("upperleg." + side, "lowerleg." + side, "foot." + side, "toes." + side)
        hip, knee, ankle, ball = self.h(ul), self.h(ll), self.h(ft), self.h(to)
        trousers, boots = r["trousers"], r["boots"]
        k.along(hip, knee, [(-0.05, 0.1), (0.3, 0.128), (0.7, 0.122), (1.0, 0.085), (1.12, 0.078)],
                trousers, ul, segs=10)
        k.ball(knee + Vector((0, -0.005, -0.02)), (0.082, 0.085, 0.07), trousers, ll, segs=10, rings=5)
        k.along(knee, ankle, [(0.1, 0.0), (0.1, 0.083, "hard"), (0.16, 0.08), (0.6, 0.066), (1.0, 0.058), (1.12, 0.055)],
                boots, ll, segs=10)
        x = hip.x
        k.ball(Vector((x, -0.0, 0.07)), (0.056, 0.095, 0.072), boots, ft, segs=10, rings=6)
        k.box(Vector((x, 0.045, 0.018)), (0.07, 0.06, 0.036), "chernozem", ft)
        k.ball(Vector((x, ball.y - 0.04, 0.034)), (0.05, 0.075, 0.034), boots, to, segs=10, rings=5)
        k.ball(Vector((x, ball.y - 0.1, 0.045)), (0.022, 0.03, 0.02), boots, to, segs=6, rings=4)

    def build(self, r):
        self.head(r)
        self.hat(r)
        self.torso(r)
        for side in ("l", "r"):
            self.arm(r, side)
            self.leg(r, side)
        return self.k


def build(name, bones, deform, armature):
    fig = Figure(bones, deform)
    kit = fig.build(RECIPES[name])
    return kit.to_object(name, armature)
