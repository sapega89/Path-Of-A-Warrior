"""Icons of things and skills in the new art, drawn in code as SVG.

    python godot/tools/art/icons.py     # writes godot/client/assets/art/icons/<sheet>.svg

The game shows a thing or a skill by a sheet and an index (scripts/core/items.gd `icon`,
scripts/ui/item_slot.gd): tool (potions, bomb, dynamite, a box for gear found on the ground,
then a heap of gold), kibo (gear), sungbo (treasures), shinki (rare things), skill and skillgray
(skills 12..30, learned and not yet). Each sheet here is one strip of 128 x 128 icons in the
order of the original sheets, so only the picture changes.

The style is the one of the figures: flat colours of the palette (palette.py), a dark ink
outline, a light stroke for the shine. Common gear is iron and leather, treasures have gold
and stones, rare things are gold and azure; a skill is a sign on a medallion in the colour of
its group.
"""

import math
import os
import re

from palette import COLORS

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "client", "assets", "art", "icons")
SIZE = 128
INK = "#2B211C"
W = 4  # the ink outline


def c(name):
    """#rrggbb of a palette colour, or a hex given as is."""
    return "#" + COLORS[name] if name in COLORS else name


# working colours of the icons, beyond the palette
C = {
    "blade": "#D9DEE2", "blade_mid": "#A7AEB4", "blade_dark": "#6E7780", "iron": "#4B5157",
    "gold": c("gold"), "gold_light": "#F0D58A", "gold_dark": c("gold_dark"),
    "wood": c("wood"), "wood_dark": c("wood_dark"), "wood_light": c("wood_light"),
    "leather": c("leather_light"), "leather_dark": c("leather"), "red": c("cinnabar"),
    "red_dark": c("cinnabar_dark"), "red_light": "#D2503F", "blue": c("blue"),
    "blue_light": "#5F8BC4", "azure": "#7FB2E0", "azure_light": "#CFE6F7", "white": c("whitewash"),
    "parchment": "#E3CF9E", "green": c("oak_light"), "green_dark": c("oak"), "fur": c("fur"),
    "fur_light": "#5A4A40", "glass": "#E8F1F2", "amethyst": "#8E5BB0", "ember": c("ember"),
    "fire": c("fire"), "flame": "#FBE29A", "dusk": c("dusk"), "violet": "#5B4A8A",
    "teal": "#3E9C9A", "yellow": "#E8C547", "skin": c("skin"),
}


class Icon:
    """One icon: SVG elements in a 128 x 128 box."""

    def __init__(self):
        self.parts = []

    def raw(self, text):
        self.parts.append(text)

    def path(self, d, fill="none", stroke=INK, w=W, extra=""):
        s = f'<path d="{d}" fill="{fill}"'
        if stroke:
            s += f' stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'
        self.raw(s + f" {extra}/>")

    def shine(self, d, colour="#FFFFFF", w=3, opacity=0.7):
        """A light stroke without ink: the shine on steel, glass, cloth."""
        self.raw(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{w}" stroke-linecap="round" '
                 f'stroke-linejoin="round" opacity="{opacity}"/>')

    def bar(self, x1, y1, x2, y2, colour, w):
        """A thick rod with an ink edge (a grip, a haft, a strap)."""
        self.raw(f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{INK}" stroke-width="{w + 2 * W - 2}" '
                 f'stroke-linecap="round"/>')
        self.raw(f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{colour}" stroke-width="{w}" '
                 f'stroke-linecap="round"/>')

    def curve_bar(self, d, colour, w):
        self.raw(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 2 * W - 2}" stroke-linecap="round"/>')
        self.raw(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{w}" stroke-linecap="round"/>')

    def circle(self, cx, cy, r, fill, w=W, stroke=INK):
        st = f' stroke="{stroke}" stroke-width="{w}"' if stroke else ""
        self.raw(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"{st}/>')

    def ellipse(self, cx, cy, rx, ry, fill, w=W, stroke=INK, extra=""):
        st = f' stroke="{stroke}" stroke-width="{w}"' if stroke else ""
        self.raw(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}"{st} {extra}/>')

    def poly(self, pts, fill, w=W, stroke=INK):
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
        self.path(d, fill, stroke, w)

    def star(self, cx, cy, r, colour, points=4, inner=0.35):
        pts = []
        for i in range(points * 2):
            a = math.pi * i / points - math.pi / 2
            rr = r if i % 2 == 0 else r * inner
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        self.poly(pts, colour, 2)

    def group(self, transform, draw):
        self.raw(f'<g transform="{transform}">')
        draw()
        self.raw("</g>")

    def svg(self):
        return "\n".join(self.parts)


# ---- weapons: drawn along X from the pommel (0) to the tip (~140), then laid on the diagonal ----

def diagonal(icon, draw, origin=(12, 116), angle=-45):
    icon.group(f"translate({origin[0]} {origin[1]}) rotate({angle})", draw)


def hilt(k, grip, guard, pommel, length=28, cross=14, knuckle=False):
    """Grip from 4 to `length`, a guard across at `length`, a pommel at 0."""
    k.bar(4, 0, length - 2, 0, grip, 11)
    for x in range(8, length - 4, 6):
        k.shine(f"M{x} -4 L{x + 2} 4", INK, 1.5, 0.5)
    if knuckle:
        k.curve_bar(f"M{length} 7 Q{length - 6} 17 {length / 2} 15 Q 6 13 2 4", guard, 4)
    k.bar(length, -cross, length, cross, guard, 7)
    k.circle(length, -cross, 4.5, guard, 2.5)
    k.circle(length, cross, 4.5, guard, 2.5)
    k.circle(1, 0, 8, pommel, 3)


def sabre_blade(k, steel, shine, x0=31, tip=128, rise=16, width=15):
    k.path(f"M{x0} -6 Q{(x0 + tip) / 2 + 10} -6 {tip} {-rise} Q{(x0 + tip) / 2 + 6} {width} {x0} {width - 6} Z", steel)
    k.shine(f"M{x0 + 4} -2 Q{(x0 + tip) / 2 + 8} -2 {tip - 14} {-rise + 6}", shine, 3)


def straight_blade(k, steel, shine, x0=31, tip=138, width=16, single=True):
    h = width / 2
    if single:
        k.poly([(x0, -h), (tip - 14, -h), (tip, -1), (tip - 10, h), (x0, h)], steel)
    else:
        k.poly([(x0, -h), (tip - 18, -h + 1), (tip, 0), (tip - 18, h - 1), (x0, h)], steel)
    k.shine(f"M{x0 + 4} -2 L{tip - 18} -2", shine, 3)


def thin_blade(k, steel, shine, x0=33, tip=140, width=12):
    h = width / 2
    k.poly([(x0, -h), (tip, 0), (x0, h)], steel)
    k.shine(f"M{x0 + 4} -1 L{tip - 24} -1", shine, 2.5)


def yatagan_blade(k, steel, shine, x0=31, tip=136):
    k.path(f"M{x0} -5 Q{x0 + 50} 10 {tip} -6 Q{x0 + 52} 22 {x0} 6 Z", steel)
    k.shine(f"M{x0 + 5} -1 Q{x0 + 48} 11 {tip - 18} -2", shine, 2.5)


def haft(k, x0, x1, colour, w=9):
    k.bar(x0, 0, x1, 0, colour, w)


def leaf_head(k, x0, tip, width, steel, shine):
    h = width / 2
    k.path(f"M{x0} 0 Q{x0 + (tip - x0) * 0.35} {-h * 2} {tip} 0 Q{x0 + (tip - x0) * 0.35} {h * 2} {x0} 0 Z", steel)
    k.shine(f"M{x0 + 4} 0 L{tip - 6} 0", shine, 2)


def berdysh_head(k, x0, x1, steel, shine, edge=None):
    k.path(f"M{x0} 4 C{x0 - 2} 34 {x1 + 4} 40 {x1 + 12} 20 L{x1} 4 Z", steel)
    k.shine(f"M{x0 + 6} 22 C{x0 + 14} 32 {x1} 32 {x1 + 6} 20", edge or shine, 2.5)
    k.bar(x0, 2, x0, 6, c("iron"), 3)
    k.bar(x1 - 4, 2, x1 - 4, 6, c("iron"), 3)


# ---- tool: potions, the bomb, the dynamite, a box --------------------------------------------

POTION = {"red": ("#D2463A", "#8E2620"), "blue": ("#3D7CC9", "#22457A"), "gold": ("#E9A93A", "#A8662A")}


def vial(k, liquid):
    light, dark = POTION[liquid]
    k.group("rotate(-30 64 64)", lambda: (
        k.path("M52 20 H76 V96 Q76 116 64 116 Q52 116 52 96 Z", C["glass"]),
        k.path("M54 58 H74 V96 Q74 113 64 113 Q54 113 54 96 Z", light, None),
        k.path("M54 58 H74", "none", dark, 2),
        k.path("M52 20 H76 V96 Q76 116 64 116 Q52 116 52 96 Z", "none"),
        k.raw(f'<rect x="50" y="10" width="28" height="14" rx="4" fill="{C["wood"]}" stroke="{INK}" stroke-width="{W}"/>'),
        k.shine("M57 30 V92", "#FFFFFF", 3, 0.8)))


def bottle(k, liquid):
    light, dark = POTION[liquid]
    body = "M54 18 H74 V40 C 92 46 96 58 96 74 V104 Q96 116 84 116 H44 Q32 116 32 104 V74 C32 58 36 46 54 40 Z"
    k.path(body, C["glass"])
    k.path("M35 70 H93 V104 Q93 113 84 113 H44 Q35 113 35 104 Z", light, None)
    k.path("M35 70 H93", "none", dark, 2)
    k.path(body, "none")
    k.raw(f'<rect x="50" y="8" width="28" height="14" rx="4" fill="{C["wood"]}" stroke="{INK}" stroke-width="{W}"/>')
    k.shine("M42 76 V104", "#FFFFFF", 4, 0.8)
    k.shine("M58 26 V38", "#FFFFFF", 3, 0.7)


def flask(k, liquid):
    light, dark = POTION[liquid]
    k.path("M54 14 H74 V40 A40 40 0 1 1 54 40 Z", C["glass"])
    k.path("M28 72 H100 A36 36 0 0 1 28 72 Z", light, None)
    k.raw(f'<path d="M28 72 Q 64 64 100 72" fill="none" stroke="{dark}" stroke-width="2"/>')
    k.path("M54 14 H74 V40 A40 40 0 1 1 54 40 Z", "none")
    k.path("M48 40 H80", "none", INK, 3)
    k.raw(f'<rect x="50" y="4" width="28" height="13" rx="4" fill="{C["wood"]}" stroke="{INK}" stroke-width="{W}"/>')
    k.shine("M38 62 Q34 80 42 96", "#FFFFFF", 4, 0.8)
    k.circle(80, 92, 3, "#FFFFFF", 0, None)


def bomb(k):
    k.circle(58, 72, 40, "#3A3D44")
    k.shine("M34 60 Q38 44 52 38", "#9AA3AD", 5, 0.8)
    k.raw(f'<rect x="64" y="22" width="22" height="16" rx="3" fill="{C["iron"]}" stroke="{INK}" stroke-width="{W}" '
          f'transform="rotate(35 75 30)"/>')
    k.curve_bar("M80 24 Q90 10 100 14", C["parchment"], 3)
    k.star(104, 14, 14, C["fire"], 8, 0.4)
    k.star(104, 14, 6, C["flame"], 4, 0.4)


def dynamite(k):
    for i, x in enumerate((38, 58, 78)):
        k.raw(f'<rect x="{x - 10}" y="{40 + (i % 2) * 4}" width="22" height="74" rx="5" fill="{C["red"]}" '
              f'stroke="{INK}" stroke-width="{W}"/>')
        k.shine(f"M{x - 4} {48 + (i % 2) * 4} V{104 + (i % 2) * 4}", "#F08A78", 3, 0.7)
    for y in (62, 92):
        k.bar(26, y, 90, y + 2, C["parchment"], 4)
    k.curve_bar("M58 42 Q58 22 76 16", C["parchment"], 3)
    k.star(80, 14, 14, C["fire"], 8, 0.4)
    k.star(80, 14, 6, C["flame"], 4, 0.4)


def crate(k):
    k.raw(f'<rect x="22" y="30" width="84" height="80" rx="4" fill="{C["wood"]}" stroke="{INK}" stroke-width="{W}"/>')
    for y in (52, 74, 96):
        k.path(f"M24 {y} H104", "none", C["wood_dark"], 2)
    k.raw(f'<rect x="22" y="30" width="84" height="80" rx="4" fill="none" stroke="{INK}" stroke-width="{W}"/>')
    k.bar(28, 36, 100, 104, C["wood_light"], 6)
    k.curve_bar("M50 56 Q50 42 64 42 Q78 42 78 56 Q78 66 64 70 V80", C["gold"], 9)
    k.circle(64, 96, 6, C["gold"], 3)


def gold_heap(k):
    k.circle(66, 58, 26, C["gold"])
    k.circle(66, 58, 18, "none", 3, C["gold_dark"])
    k.path("M66 44 V72 M56 54 H76", "none", C["gold_dark"], 5)
    for x, ys in ((40, (104, 94, 84)), (90, (106, 96))):
        for y in ys:
            k.ellipse(x, y + 5, 22, 9, C["gold_dark"])
            k.ellipse(x, y, 22, 9, C["gold"])
            k.ellipse(x, y, 13, 4.5, "none", 2, C["gold_dark"])
    k.shine("M48 44 Q56 34 68 34", C["gold_light"], 4, 0.9)


TOOL = [lambda k: vial(k, "red"), lambda k: bottle(k, "red"), lambda k: flask(k, "red"),
        lambda k: vial(k, "blue"), lambda k: bottle(k, "blue"), lambda k: flask(k, "blue"),
        lambda k: vial(k, "gold"), lambda k: bottle(k, "gold"), lambda k: flask(k, "gold"),
        bomb, dynamite, crate, gold_heap]


# ---- gear (kibo): iron and leather; treasures (sungbo): gold and stones; rare (shinki) ------

class Look:
    """The materials of a thing by its rank."""

    def __init__(self, rank, grip=None, gem=None, glow="azure"):
        self.rank = rank
        self.glow = glow
        if rank == "rare":
            self.steel, self.shine, self.metal, self.trim = C["azure_light"], "#FFFFFF", C["gold"], C["gold_light"]
            self.grip, self.cloth, self.gem = C["blue"], C["azure"], C["azure"]
        elif rank == "treasure":
            self.steel, self.shine, self.metal, self.trim = C["blade"], "#FFFFFF", C["gold"], C["gold_light"]
            self.grip, self.cloth, self.gem = C["red_dark"], C["red"], C["amethyst"]
        else:
            self.steel, self.shine, self.metal, self.trim = C["blade_mid"], "#FFFFFF", C["iron"], C["blade_mid"]
            self.grip, self.cloth, self.gem = C["leather_dark"], C["leather"], C["red"]
        self.grip = grip or self.grip
        self.gem = gem or self.gem


GLOWS = {"azure": "#9FD0F5", "gold": "#F5D987", "white": "#F2F6FA"}


def glow(k, colour="azure"):
    """The light around a rare thing (a gradient of the sheet's <defs>)."""
    k.raw(f'<circle cx="64" cy="64" r="62" fill="url(#glow_{colour})"/>')


def broadsword(look, steel=None):
    def draw(k):
        if look.rank == "rare":
            glow(k, look.glow)
        diagonal(k, lambda: (straight_blade(k, steel or look.steel, look.shine, 32, 140, 17),
                             hilt(k, look.grip, look.metal, look.metal if look.rank != "gear" else c("iron"),
                                  knuckle=True)))
    return draw


def konchar(look, steel=None):
    def draw(k):
        if look.rank == "rare":
            glow(k, look.glow)
        diagonal(k, lambda: (thin_blade(k, steel or look.steel, look.shine, 36, 142, 13),
                             hilt(k, look.grip, look.metal, look.gem if look.rank != "gear" else look.metal,
                                  length=32, cross=16)), origin=(10, 118))
    return draw


def sabre(look, steel=None):
    def draw(k):
        if look.rank == "rare":
            glow(k, look.glow)
        diagonal(k, lambda: (sabre_blade(k, steel or look.steel, look.shine),
                             hilt(k, look.grip, look.metal, look.gem if look.rank != "gear" else look.metal, cross=12)),
                 origin=(18, 112))
    return draw


def yatagan(look):
    def draw(k):
        glow(k)
        diagonal(k, lambda: (yatagan_blade(k, look.steel, look.shine),
                             hilt(k, C["white"], look.metal, C["white"], cross=6)), origin=(14, 110))
    return draw


def kindjal(look):
    def draw(k):
        diagonal(k, lambda: (straight_blade(k, look.steel, look.shine, 30, 110, 22, single=False),
                             k.shine("M34 0 L84 0", C["blade_dark"], 2, 0.8),
                             hilt(k, look.grip, look.metal, look.metal, length=27, cross=9)), origin=(22, 106))
    return draw


def berdysh(look):
    def draw(k):
        diagonal(k, lambda: (haft(k, 0, 132, C["wood"] if look.rank == "gear" else C["wood_dark"]),
                             k.bar(124, 0, 136, 0, look.metal, 5),
                             berdysh_head(k, 76, 120, look.steel, look.shine,
                                          look.trim if look.rank != "gear" else None),
                             k.circle(4, 0, 5, look.metal, 3)), origin=(16, 114))
    return draw


def spear(look, width=14, long=False, pennant=None, moon=False):
    def draw(k):
        if look.rank == "rare":
            glow(k)
        head = 104 if not long else 112

        def parts():
            haft(k, 0, head, C["wood"], 8)
            if pennant:
                k.path(f"M{head - 26} -3 L{head - 4} -3 L{head - 12} -16 L{head - 4} -30 L{head - 26} -30 Z", pennant)
                k.path(f"M{head - 26} -16 H{head - 8}", "none", C["white"], 4)
            if moon:
                k.path(f"M{head - 2} -16 Q{head + 12} 0 {head - 2} 16 Q{head + 6} 0 {head - 2} -16 Z", look.steel)
            k.bar(head - 6, 0, head + 4, 0, look.metal, 9)
            if look.rank != "gear":
                k.bar(head - 10, 0, head - 8, 0, C["red"], 10)
            leaf_head(k, head + 2, 142, width * 1.4, look.steel, look.shine)
        diagonal(k, parts, origin=(8, 120))
    return draw


def bow(look, colour=None, string=None):
    def draw(k):
        if look.rank == "rare":
            glow(k, "white")
        body = colour or (C["wood_dark"] if look.rank == "gear" else C["red_dark"])
        k.path("M30 112 L112 30", "none", string or C["parchment"], 2)
        k.curve_bar("M30 112 Q22 100 26 86 Q34 50 62 40 Q86 30 100 22 Q112 18 112 30", body, 6)
        k.curve_bar("M30 112 Q22 100 26 86", look.metal, 4)
        k.curve_bar("M100 22 Q112 18 112 30", look.metal, 4)
        k.curve_bar("M40 64 Q46 52 56 46", look.trim if look.rank != "gear" else C["parchment"], 7)
        k.shine("M30 82 Q38 56 60 46", "#FFFFFF", 2, 0.4)
    return draw


def helmet(look):
    def draw(k):
        mail = C["blade_dark"] if look.rank == "gear" else C["blade_mid"]
        k.path("M26 66 Q26 108 40 112 H88 Q102 108 102 66 Z", mail)
        for y in range(76, 108, 8):
            for x in range(34 + (y % 16) // 2, 96, 8):
                k.raw(f'<circle cx="{x}" cy="{y}" r="2.6" fill="none" stroke="{INK}" stroke-width="1.4" opacity="0.6"/>')
        k.path("M26 70 Q24 26 64 20 Q104 26 102 70 Z", look.steel)
        k.shine("M38 56 Q40 34 60 28", "#FFFFFF", 4, 0.7)
        k.bar(26, 68, 102, 68, look.metal if look.rank != "gear" else C["leather"], 7)
        for x in range(34, 100, 12):
            k.circle(x, 68, 2.4, C["gold"] if look.rank != "gear" else C["blade"], 1.2)
        k.bar(64, 10, 64, 22, look.metal, 5)
        k.circle(64, 9, 4, look.metal, 2.5)
        k.bar(64, 70, 64, 92, look.steel, 5)
    return draw


def kuchma(look):
    def draw(k):
        if look.rank == "rare":
            glow(k, "gold")
        top = look.cloth if look.rank != "rare" else C["blue"]
        k.path("M34 62 Q30 26 64 22 Q96 20 106 40 Q112 54 100 62 Z", top)
        k.curve_bar("M104 42 Q114 58 108 76", top, 8)
        k.circle(108, 82, 7, C["gold"], 3)
        fur = C["fur"] if look.rank != "rare" else "#6A5444"
        k.path("M18 70 Q16 60 28 58 Q64 50 100 58 Q112 60 110 70 L108 96 Q64 110 20 96 Z", fur)
        for x in range(26, 106, 8):
            k.shine(f"M{x} 64 Q{x + 3} 78 {x - 1} 96", C["fur_light"] if look.rank != "rare" else "#9A8270",
                    3, 0.7)
        if look.rank == "rare":
            k.curve_bar("M64 46 Q60 22 76 8", C["white"], 6)
            k.circle(64, 50, 7, C["azure"], 3)
    return draw


def armour(look, kind="mail"):
    def draw(k):
        if look.rank == "rare":
            glow(k)
        body = "M44 18 L28 24 L12 52 L26 62 L34 50 L34 112 H94 V50 L102 62 L116 52 L100 24 L84 18 Q64 32 44 18 Z"
        if kind == "mail":
            k.path(body, C["blade_mid"])
            for y in range(32, 110, 7):
                for x in range(20 + (y % 14) // 2, 110, 7):
                    k.raw(f'<path d="M{x - 3} {y} Q{x} {y + 4} {x + 3} {y}" fill="none" stroke="{INK}" '
                          f'stroke-width="1.3" opacity="0.55"/>')
            k.path(body, "none")
            k.path("M44 18 Q64 32 84 18", "none", C["leather"], 6)
            k.bar(36, 84, 92, 84, C["leather_dark"], 7)
            k.circle(64, 84, 5, C["blade"], 2.5)
        else:
            k.path(body, C["blade_mid"] if look.rank != "rare" else C["azure"])
            k.path("M64 30 V110", "none", INK, 2.5)
            k.shine("M44 40 Q42 70 48 100", "#FFFFFF", 5, 0.6)
            for y in (60, 78, 96):
                k.path(f"M36 {y} Q64 {y + 8} 92 {y}", "none", INK, 2.5)
            k.path(body, "none", look.metal, 4)
            k.path(body, "none", INK, 1.5)
            k.circle(64, 46, 8, look.gem, 3)
    return draw


def belt(look, sash=False):
    def draw(k):
        if look.rank == "rare":
            glow(k, "gold")
        strap = look.cloth if sash else (C["leather"] if look.rank == "gear" else C["red_dark"])
        k.path("M14 58 Q64 40 114 58 L114 80 Q64 62 14 80 Z", strap)
        if sash:
            for y in (62, 68):
                k.shine(f"M18 {y + 4} Q64 {y - 14} 110 {y + 4}", C["gold_light"], 2, 0.8)
            k.curve_bar("M70 76 Q72 98 66 116", strap, 9)
            k.curve_bar("M84 74 Q90 94 88 112", strap, 9)
            for x in (66, 88):
                k.path(f"M{x - 6} 112 L{x - 8} 124 M{x} 114 V124 M{x + 6} 112 L{x + 8} 124", "none", C["gold"], 3)
        for x in range(24, 108, 14):
            if look.rank != "rare":
                k.circle(x, 66 + abs(x - 64) * 0.18 - 9, 3, look.trim, 1.5)
            else:
                k.raw(f'<rect x="{x - 5}" y="{58 + abs(x - 64) * 0.18 - 8}" width="10" height="14" rx="2" '
                      f'fill="{C["gold"]}" stroke="{INK}" stroke-width="2"/>')
        k.raw(f'<rect x="50" y="46" width="28" height="32" rx="6" fill="{look.metal if look.rank != "gear" else C["blade_mid"]}" '
              f'stroke="{INK}" stroke-width="{W}"/>')
        k.raw(f'<rect x="57" y="53" width="14" height="18" rx="3" fill="none" stroke="{INK}" stroke-width="3"/>')
        if look.rank != "gear":
            k.circle(64, 62, 4, look.gem, 2)
    return draw


def bracer(look):
    def draw(k):
        metal = C["gold"] if look.rank != "gear" else C["blade_mid"]
        stud = C["red"] if look.rank == "gear" else C["azure"]

        def parts():
            k.path("M-4 -22 Q46 -30 96 -18 L96 18 Q46 30 -4 22 Q-12 0 -4 -22 Z", metal)
            k.path("M96 -18 Q104 0 96 18 Q88 0 96 -18 Z", C["leather_dark"])
            k.shine("M6 -16 Q46 -22 86 -12", "#FFFFFF", 4, 0.6)
            k.path("M10 -24 Q8 0 10 24 M40 -27 Q38 0 40 27 M70 -25 Q68 0 70 25", "none", INK, 2)
            for x in (25, 55, 83):
                k.circle(x, 0, 5, stud, 2.5)
            for x in (18, 62):
                k.bar(x, -27, x, 27, C["leather"], 5)
        k.group("translate(24 100) rotate(-40)", parts)
    return draw


def locket(look):
    def draw(k):
        for i in range(9):
            t = i / 8
            x = 34 + 60 * t
            y = 18 + 50 * (1 - (2 * t - 1) ** 2) * 0.9
            k.ellipse(x, y, 4, 3, "none", 2, C["gold_dark"])
        k.path("M64 64 L60 72 H68 Z", C["gold"], INK, 2)
        k.ellipse(64, 92, 22, 26, C["gold"])
        k.ellipse(64, 92, 13, 16, C["red"], 3)
        k.shine("M58 84 Q60 80 64 79", "#FFFFFF", 3, 0.8)
        k.ellipse(64, 92, 22, 26, "none", 2, C["gold_dark"], 'stroke-dasharray="3 4"')
    return draw


def gauntlet(look):
    def draw(k):
        hide = C["leather"] if look.rank == "gear" else C["red_dark"]
        k.path("M30 120 L36 74 Q36 64 44 60 L44 28 Q44 20 51 20 Q57 20 57 28 L57 50 L58 20 Q58 12 65 12 Q72 12 72 20 "
               "L71 50 L73 24 Q74 16 80 16 Q87 16 86 25 L84 56 L88 38 Q90 31 96 33 Q101 35 100 42 L94 82 "
               "Q90 96 84 102 L84 120 Z", hide)
        k.path("M30 120 L84 120 L86 100 L32 98 Z", look.steel if look.rank != "gear" else C["blade_mid"])
        k.path("M44 60 Q60 66 84 58", "none", INK, 2)
        k.raw(f'<path d="M40 74 Q62 82 90 72 L88 88 Q62 96 38 88 Z" fill="{C["blade_mid"]}" stroke="{INK}" stroke-width="3"/>')
        for x in (48, 62, 76):
            k.circle(x, 82, 3, C["blade"], 1.5)
        k.shine("M47 30 V54", "#FFFFFF", 2.5, 0.5)
    return draw


def boots(look, colour=None, toe=False, wings=False):
    def draw(k):
        if wings:
            glow(k)
        hide = colour or C["leather"]
        k.path("M36 14 H76 L78 84 Q84 92 102 96 Q118 100 116 112 L114 116 H34 Z" if not toe else
               "M36 14 H76 L78 84 Q86 92 100 94 Q116 94 120 86 Q122 104 112 116 H34 Z", hide)
        k.path("M32 12 H80 V30 Q56 36 32 30 Z", C["fur"] if look.rank != "rare" else C["white"])
        k.path("M34 108 H116", "none", INK, 2)
        k.raw(f'<rect x="32" y="108" width="20" height="12" rx="2" fill="{C["wood_dark"]}" stroke="{INK}" stroke-width="3"/>')
        k.shine("M44 36 V96", "#FFFFFF", 4, 0.4)
        if look.rank != "gear":
            k.path("M40 58 Q56 66 72 58 M40 70 Q56 78 72 70", "none", C["gold"], 3)
        if wings:
            k.path("M78 40 Q100 22 122 26 Q108 34 116 40 Q100 42 106 50 Q90 50 80 58 Z", C["white"])
            k.shine("M84 46 Q100 34 116 30", C["azure"], 2, 0.9)
    return draw


def horse(colour, mane, look):
    def draw(k):
        if look.rank == "rare":
            glow(k, "gold")
        k.path("M96 116 Q102 86 92 66 Q84 46 70 36 L74 18 L62 30 L56 18 L52 34 Q36 42 26 62 Q16 78 22 90 "
               "Q30 98 40 92 Q48 86 56 78 Q62 92 58 116 Z", colour)
        k.path("M70 36 Q84 34 96 56 Q108 76 104 116 L96 116 Q102 86 92 66 Q84 46 70 36 Z", mane)
        k.ellipse(24, 84, 4, 3, INK, 0)
        k.circle(46, 56, 4.5, INK, 0, None)
        k.circle(47, 55, 1.5, "#FFFFFF", 0, None)
        strap = look.metal if look.rank != "gear" else C["red"]
        k.path("M30 74 Q46 70 56 76 M50 44 Q56 62 56 76 M56 76 L62 94", "none", strap, 4)
        k.circle(56, 76, 4, C["gold"], 2)
        if look.rank == "rare":
            k.curve_bar("M64 30 Q68 10 86 6", C["red"], 6)
    return draw


def scroll(k):
    k.path("M30 24 H98 V96 Q98 106 88 106 H30 Z", C["parchment"])
    for y in (40, 52, 64, 76):
        k.path(f"M40 {y} H{86 - (y % 3) * 6}", "none", C["wood_dark"], 2.5)
    k.raw(f'<rect x="22" y="14" width="84" height="16" rx="8" fill="{C["parchment"]}" stroke="{INK}" stroke-width="{W}"/>')
    k.raw(f'<rect x="22" y="98" width="70" height="16" rx="8" fill="{C["parchment"]}" stroke="{INK}" stroke-width="{W}"/>')
    k.curve_bar("M76 98 Q74 112 70 122", C["red"], 4)
    k.curve_bar("M80 98 Q86 112 90 120", C["red"], 4)
    k.circle(78, 98, 11, C["red_dark"])
    k.star(78, 98, 5, C["red_light"], 6, 0.5)


def tincture(liquid, flower, petals):
    def draw(k):
        k.path("M50 30 H78 V44 Q98 50 98 70 V104 Q98 116 86 116 H42 Q30 116 30 104 V70 Q30 50 50 44 Z", C["glass"])
        k.path("M33 72 H95 V104 Q95 113 86 113 H42 Q33 113 33 104 Z", liquid, None)
        k.path("M50 30 H78 V44 Q98 50 98 70 V104 Q98 116 86 116 H42 Q30 116 30 104 V70 Q30 50 50 44 Z", "none")
        k.raw(f'<rect x="46" y="18" width="36" height="14" rx="4" fill="{C["wood"]}" stroke="{INK}" stroke-width="{W}"/>')
        k.curve_bar("M70 20 Q76 8 92 4", C["green_dark"], 3)
        for i in range(petals):
            a = 2 * math.pi * i / petals
            k.ellipse(94 + math.cos(a) * 7, 8 + math.sin(a) * 7, 6, 4, flower, 2, INK,
                      f'transform="rotate({math.degrees(a):.0f} {94 + math.cos(a) * 7:.1f} {8 + math.sin(a) * 7:.1f})"')
        k.circle(94, 8, 4, C["yellow"], 2)
        k.raw(f'<rect x="40" y="78" width="48" height="24" rx="3" fill="{C["parchment"]}" stroke="{INK}" stroke-width="2"/>')
        k.path("M46 90 H82", "none", C["red"], 3)
        k.shine("M38 56 Q34 70 36 84", "#FFFFFF", 4, 0.7)
    return draw


def gourd(colour, band, berries=None):
    def draw(k):
        k.path("M56 12 H72 V26 Q90 30 90 46 Q90 56 82 60 Q106 70 106 92 Q106 118 64 118 Q22 118 22 92 Q22 70 46 60 "
               "Q38 56 38 46 Q38 30 56 26 Z", colour)
        k.bar(40, 62, 88, 62, band, 6)
        k.curve_bar("M86 46 Q112 54 100 82", C["leather"], 4)
        k.raw(f'<rect x="52" y="4" width="24" height="12" rx="4" fill="{C["wood"]}" stroke="{INK}" stroke-width="3"/>')
        k.shine("M34 84 Q34 100 46 108", "#FFFFFF", 4, 0.5)
        if berries:
            for x, y in ((60, 88), (70, 84), (66, 96), (76, 94)):
                k.circle(x, y, 5, berries, 2)
            k.path("M60 80 Q66 70 80 72", "none", C["green_dark"], 3)
    return draw


def book(k):
    k.path("M22 30 L84 18 L106 30 L106 108 L44 120 L22 108 Z", C["parchment"])
    k.path("M22 30 L84 18 L84 96 L22 108 Z", C["red_dark"])
    k.path("M84 18 L106 30 L106 108 L84 96 Z", C["parchment"])
    for y in (40, 52, 64, 76, 88):
        k.path(f"M86 {y - 6} L104 {y + 4}", "none", C["wood_light"], 1.5)
    k.path("M22 108 L44 120 L106 108", "none")
    for x, y in ((26, 34), (78, 24), (26, 98), (78, 88)):
        k.raw(f'<path d="M{x} {y} l6 -1 l0 8 l-6 1 Z" fill="{C["gold"]}" stroke="{INK}" stroke-width="1.5"/>')
    k.path("M53 34 L53 92 M38 62 L68 58", "none", C["gold"], 6)
    k.path("M53 34 L53 92 M38 62 L68 58", "none", INK, 1.5)
    k.bar(80, 50, 96, 54, C["gold"], 6)


def rushnyk(k):
    cloth = C["white"]
    k.path("M14 18 Q64 30 114 18 L114 108 L92 108 L92 44 Q64 74 36 44 L36 108 L14 108 Z", cloth)
    k.path("M14 18 Q64 30 114 18 Q96 26 92 44 Q64 74 36 44 Q32 26 14 18 Z", "#D8D0BE", INK, 3)
    k.bar(8, 18, 120, 18, C["wood"], 6)
    for x0 in (14, 92):
        for y in (78, 92):
            k.path(f"M{x0 + 2} {y} l4 -5 l4 5 l4 -5 l4 5", "none", C["red"], 3)
        k.path(f"M{x0} 70 H{x0 + 22} M{x0} 100 H{x0 + 22}", "none", C["red_dark"], 2)
    k.path("M42 52 l6 4 l-6 4 l-6 -4 Z M86 52 l6 4 l-6 4 l-6 -4 Z M64 62 l6 4 l-6 4 l-6 -4 Z", C["red"], INK, 1.5)
    for x in range(16, 36, 5):
        k.path(f"M{x} 108 V120", "none", C["red"], 2.5)
    for x in range(94, 114, 5):
        k.path(f"M{x} 108 V120", "none", C["red"], 2.5)


def seal(k):
    glow(k, "gold")
    k.raw(f'<rect x="20" y="70" width="88" height="44" rx="4" fill="{C["parchment"]}" stroke="{INK}" stroke-width="{W}" '
          f'transform="rotate(-6 64 92)"/>')
    k.circle(88, 96, 14, C["red_dark"])
    k.star(88, 96, 7, C["red_light"], 6, 0.5)
    k.path("M38 66 L58 66 L62 80 L34 80 Z", C["gold"])
    k.path("M44 66 Q38 40 48 26 Q52 18 58 26 Q66 40 52 66 Z", C["wood_dark"])
    k.circle(51, 20, 7, C["gold"])
    k.ellipse(48, 82, 18, 5, C["gold_dark"])
    k.shine("M46 30 Q42 44 46 60", C["wood_light"], 3, 0.8)


KIBO_LOOK = Look("gear")
SUNGBO_LOOK = Look("treasure")
SHINKI_LOOK = Look("rare")

KIBO = [broadsword(KIBO_LOOK), konchar(KIBO_LOOK), berdysh(KIBO_LOOK), sabre(KIBO_LOOK), spear(KIBO_LOOK),
        kindjal(KIBO_LOOK), helmet(KIBO_LOOK), armour(KIBO_LOOK, "mail"), belt(KIBO_LOOK), bracer(KIBO_LOOK),
        locket(KIBO_LOOK), gauntlet(KIBO_LOOK), boots(KIBO_LOOK)]

SUNGBO = [broadsword(SUNGBO_LOOK), konchar(SUNGBO_LOOK), berdysh(SUNGBO_LOOK), spear(SUNGBO_LOOK),
          spear(SUNGBO_LOOK, 10, True, C["red"]), spear(SUNGBO_LOOK, 10, True, moon=True), bow(SUNGBO_LOOK),
          kuchma(SUNGBO_LOOK), armour(SUNGBO_LOOK, "plate"), boots(SUNGBO_LOOK, C["red"], toe=True),
          belt(SUNGBO_LOOK, sash=True), horse("#8A5A36", C["fur"], SUNGBO_LOOK), scroll,
          tincture("#D9A23A", C["yellow"], 5), tincture("#3D6FB8", "#5C8FE0", 7),
          gourd(C["teal"], C["white"]), gourd(C["green"], C["red"], C["red"])]

SHINKI = [book, rushnyk, spear(SHINKI_LOOK, 12, True), seal, armour(SHINKI_LOOK, "plate"),
          horse("#E8DCC4", C["gold"], SHINKI_LOOK), boots(SHINKI_LOOK, C["blue_light"], toe=True, wings=True),
          konchar(SHINKI_LOOK), broadsword(Look("rare", grip=C["red_dark"], gem=C["red"]), C["blade"]),
          yatagan(SHINKI_LOOK), sabre(Look("rare", grip=C["dusk"], gem=C["amethyst"], glow="white"), "#7C8494"),
          broadsword(Look("rare", grip=C["red"], gem=C["gold"], glow="gold"), C["blade_mid"]), sabre(SHINKI_LOOK),
          broadsword(Look("rare", grip=C["white"], gem=C["azure_light"], glow="white"), C["azure_light"]),
          bow(SHINKI_LOOK, C["white"], C["azure"]),
          konchar(Look("rare", grip=C["red_dark"], gem=C["red"], glow="gold"), C["gold_light"]), kuchma(SHINKI_LOOK),
          belt(SHINKI_LOOK)]


# ---- skills: a sign on a medallion in the colour of the skill's group -------------------------

# the groups of skills 12..30 (data/skills.json "rows"): dash, heal, passive, forward, near,
# ranged, the whole room
GROUP = {"move": "#4D6E9C", "heal": "#4E7A3A", "pasv": "#9C7A30", "fwd": "#2F6E8A", "near": "#8E2E24",
         "range": "#4F3F7A", "whole": "#3A2A44"}


def medallion(k, group):
    k.circle(64, 64, 58, C["gold"], W)
    k.circle(64, 64, 49, GROUP[group], 3)
    for i in range(16):
        a = 2 * math.pi * i / 16
        k.circle(64 + math.cos(a) * 53.5, 64 + math.sin(a) * 53.5, 2, C["gold_dark"], 0, None)


def flame(k, x, y, s, rot=0, outer=None, inner=None):
    k.group(f"translate({x} {y}) rotate({rot}) scale({s})", lambda: (
        k.path("M0 20 Q-16 18 -14 2 Q-12 -8 -4 -14 Q-6 -4 0 -2 Q2 -14 10 -24 Q8 -8 14 0 Q18 18 0 20 Z",
               outer or C["ember"], INK, 3 / s),
        k.path("M0 16 Q-8 14 -7 6 Q-6 0 -1 -4 Q0 4 4 4 Q8 -2 8 -6 Q12 4 8 12 Q6 16 0 16 Z",
               inner or C["fire"], None)))


def wave(k, x, y, s, colour="#5F9FD0"):
    k.group(f"translate({x} {y}) scale({s})", lambda: (
        k.path("M-30 10 Q-24 -16 0 -18 Q22 -18 26 0 Q16 -10 6 -4 Q14 4 4 10 Z", colour, INK, 3 / s),
        k.shine("M-24 4 Q-18 -12 0 -14", "#FFFFFF", 2.5 / s, 0.8)))


def bolt(k, x, y, s, colour=None):
    k.group(f"translate({x} {y}) scale({s})", lambda: k.poly(
        [(4, -30), (-12, 2), (-1, 2), (-8, 30), (14, -6), (2, -6), (10, -30)], colour or C["flame"], 3 / s))


def sabre_sign(k, x, y, angle, s=1.0):
    k.group(f"translate({x} {y}) rotate({angle}) scale({s})", lambda: (
        sabre_blade(k, C["blade"], "#FFFFFF", 31, 100, 14, 9),
        hilt(k, C["red_dark"], C["gold"], C["gold"], cross=10)))


def skill_whirl(k):
    medallion(k, "move")
    k.curve_bar("M30 74 Q28 34 64 28 Q96 26 104 54", "#9FC0E8", 4)
    k.curve_bar("M98 58 Q100 96 62 102 Q34 104 26 80", "#9FC0E8", 4)
    sabre_sign(k, 34, 92, -45, 0.9)


def skill_storm(k):
    medallion(k, "move")
    for y, x in ((44, 20), (62, 14), (80, 22)):
        k.path(f"M{x} {y} H{x + 30}", "none", "#9FC0E8", 4)
    sabre_sign(k, 40, 76, -20, 0.9)


def skill_thunder(k):
    medallion(k, "move")
    for dy in (-20, 0, 20):
        k.group(f"translate(22 {64 + dy})", lambda: thin_blade(k, C["blade"], "#FFFFFF", 0, 70, 9))
    bolt(k, 96, 62, 0.8)


def skill_herbs(k):
    medallion(k, "heal")
    k.curve_bar("M64 106 Q60 70 66 30", C["green_dark"], 4)
    for (x, y, a) in ((64, 86, -40), (64, 70, 40), (64, 54, -40), (65, 40, 40)):
        k.ellipse(x + (14 if a > 0 else -14), y, 14, 7, C["green"], 2.5, INK,
                  f'transform="rotate({a} {x + (14 if a > 0 else -14)} {y})"')
    for i in range(5):
        a = 2 * math.pi * i / 5
        k.circle(66 + math.cos(a) * 6, 28 + math.sin(a) * 6, 4.5, C["white"], 2)
    k.circle(66, 28, 3.5, C["yellow"], 1.5)


def skill_water(k):
    medallion(k, "heal")
    k.path("M64 18 Q90 56 90 76 Q90 102 64 102 Q38 102 38 76 Q38 56 64 18 Z", "#6FB0E0")
    k.shine("M50 70 Q50 86 62 92", "#FFFFFF", 4, 0.8)
    k.star(94, 36, 10, C["white"], 4)
    k.star(34, 44, 7, C["white"], 4)


def skill_fury(k):
    medallion(k, "pasv")
    flame(k, 64, 70, 2.1, 0, C["red_light"], C["fire"])
    k.poly([(64, 26), (84, 50), (72, 50), (72, 90), (56, 90), (56, 50), (44, 50)], C["white"], 3)


def skill_charm(k):
    medallion(k, "pasv")
    k.path("M64 22 L96 34 Q96 80 64 104 Q32 80 32 34 Z", C["blue_light"])
    k.path("M64 30 L88 40 Q88 76 64 94 Q40 76 40 40 Z", "none", C["gold_light"], 3)
    k.star(64, 58, 16, C["gold"], 8, 0.45)


def skill_pokrova(k):
    medallion(k, "pasv")
    for i in range(9):
        a = math.pi + math.pi * i / 8
        k.path(f"M{64 + math.cos(a) * 26:.1f} {82 + math.sin(a) * 26:.1f} L{64 + math.cos(a) * 44:.1f} "
               f"{82 + math.sin(a) * 44:.1f}", "none", C["gold_light"], 3)
    k.path("M22 92 Q24 54 64 46 Q104 54 106 92 Q96 84 86 92 Q76 84 64 92 Q52 84 42 92 Q32 84 22 92 Z", C["blue_light"])
    for x in (40, 64, 88):
        k.star(x, 70, 5, C["gold_light"], 4)


def skill_wave(k):
    medallion(k, "fwd")
    wave(k, 64, 70, 1.5)
    wave(k, 52, 92, 0.8, "#3F7FB0")


def skill_rapids(k):
    medallion(k, "fwd")
    k.path("M24 100 L36 76 L52 80 L60 100 Z", C["blade_dark"])
    k.path("M66 100 L78 70 L98 78 L104 100 Z", C["blade_dark"])
    for x, y in ((40, 56), (64, 44), (88, 52)):
        k.path(f"M{x - 10} {y + 14} Q{x} {y - 18} {x + 10} {y + 14}", "#9FD0F0", INK, 3)
    k.path("M20 100 Q64 88 108 100", "none", "#9FD0F0", 5)


def skill_flood(k):
    medallion(k, "fwd")
    for i, y in enumerate((50, 70, 90)):
        wave(k, 64 - (i - 1) * 10, y, 1.1 - i * 0.1, ("#7FBFEA", "#5F9FD0", "#3F7FB0")[i])


def skill_ring_of_fire(k):
    medallion(k, "near")
    for i in range(8):
        a = 2 * math.pi * i / 8
        flame(k, 64 + math.cos(a) * 30, 64 + math.sin(a) * 30, 0.75, math.degrees(a) + 90)
    k.circle(64, 64, 10, C["flame"], 2)


def skill_fire_whirl(k):
    medallion(k, "near")
    k.curve_bar("M64 64 Q80 60 78 46 Q72 30 54 34 Q34 42 36 64 Q40 92 70 94 Q100 92 104 62", C["ember"], 8)
    k.curve_bar("M64 64 Q80 60 78 46 Q72 30 54 34 Q34 42 36 64 Q40 92 70 94 Q100 92 104 62", C["fire"], 3)
    flame(k, 102, 54, 0.8, 30)


def skill_blaze(k):
    medallion(k, "near")
    for i, x in enumerate((34, 56, 78, 98)):
        flame(k, x, 66 + (i % 2) * 6, 1.0 + (i % 2) * 0.3)
    for x in range(22, 108, 7):
        k.path(f"M{x} 104 Q{x + 2} 90 {x + 5} 82", "none", c("grass"), 3)


def skill_lightning(k):
    medallion(k, "range")
    bolt(k, 64, 64, 1.5)


def skill_perun(k):
    medallion(k, "range")
    k.group("translate(62 66) rotate(-45)", lambda: (
        k.curve_bar("M-40 0 L-28 -8 L-14 8 L0 -8 L14 6", C["flame"], 5),
        k.poly([(12, -14), (46, 0), (12, 14), (18, 0)], C["blade"], 3),
        k.poly([(-40, 0), (-54, -14), (-48, 0), (-54, 14)], C["red"], 2.5)))
    k.star(98, 30, 12, C["flame"], 4)


def skill_storm_cloud(k):
    medallion(k, "whole")
    k.path("M28 62 Q22 44 40 42 Q44 24 64 28 Q80 18 90 36 Q108 36 104 56 Q102 64 92 64 H36 Q30 64 28 62 Z", "#8C93A8")
    bolt(k, 52, 86, 0.6)
    bolt(k, 82, 88, 0.55)
    for x in (36, 66, 96):
        k.path(f"M{x} 70 L{x - 4} 80", "none", "#9FC0E8", 3)


def skill_serpent(k):
    medallion(k, "whole")
    k.curve_bar("M30 100 Q20 76 44 72 Q70 70 60 50 Q52 34 70 30", C["green"], 9)
    k.path("M64 22 Q80 16 88 28 Q84 36 70 36 Q60 34 64 22 Z", C["green"])
    k.circle(76, 25, 2.5, C["flame"], 0, None)
    flame(k, 98, 36, 1.0, 70)


def skill_rain(k):
    medallion(k, "whole")
    for x, y, s in ((44, 50, 1.0), (78, 38, 0.8), (92, 74, 1.1), (54, 90, 0.9)):
        k.curve_bar(f"M{x - 26 * s:.1f} {y - 26 * s:.1f} L{x - 6 * s:.1f} {y - 6 * s:.1f}", C["ember"], 6 * s)
        k.circle(x, y, 11 * s, C["fire"], 3)
        k.circle(x - 2 * s, y - 2 * s, 5 * s, C["flame"], 0, None)


SKILL = [skill_whirl, skill_storm, skill_thunder, skill_herbs, skill_water, skill_fury, skill_charm,
         skill_pokrova, skill_wave, skill_rapids, skill_flood, skill_ring_of_fire, skill_fire_whirl,
         skill_blaze, skill_lightning, skill_perun, skill_storm_cloud, skill_serpent, skill_rain]

SHEETS = {"tool": TOOL, "kibo": KIBO, "sungbo": SUNGBO, "shinki": SHINKI, "skill": SKILL}


def strip(recipes):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE * len(recipes)}" height="{SIZE}" '
           f'viewBox="0 0 {SIZE * len(recipes)} {SIZE}">', "<defs>"]
    for name, colour in GLOWS.items():
        out.append(f'<radialGradient id="glow_{name}"><stop offset="0" stop-color="{colour}" stop-opacity="0.75"/>'
                   f'<stop offset="0.55" stop-color="{colour}" stop-opacity="0.3"/>'
                   f'<stop offset="1" stop-color="{colour}" stop-opacity="0"/></radialGradient>')
    out.append("</defs>")
    for i, draw in enumerate(recipes):
        k = Icon()
        draw(k)
        out.append(f'<g transform="translate({i * SIZE} 0)">')
        out.append(k.svg())
        out.append("</g>")
    out.append("</svg>")
    return "\n".join(out) + "\n"


def grey(svg):
    """A skill not learned yet: every colour to a dim grey."""
    def to_grey(m):
        h = m.group(1)
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        v = int((0.3 * r + 0.59 * g + 0.11 * b) * 0.7)
        return "#%02X%02X%02X" % (v, v, v)
    return re.sub(r"#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b", to_grey, svg)


def main():
    os.makedirs(OUT, exist_ok=True)
    counts = {}
    for name, recipes in SHEETS.items():
        svg = strip(recipes)
        with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as f:
            f.write(svg)
        if name == "skill":
            with open(os.path.join(OUT, "skillgray.svg"), "w", encoding="utf-8") as f:
                f.write(grey(svg))
        counts[name] = len(recipes)
    print(OUT, counts)


if __name__ == "__main__":
    main()
