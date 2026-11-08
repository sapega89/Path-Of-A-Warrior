"""Palette of the "steppe folk print" art style.

The ten base colours come from the style guide. Working colours are mixed from them
for things the base set does not cover (skin, wood, straw, canvas, leather).
Colours are sRGB hex; `linear()` converts them for vertex colours, which glTF stores
in linear space.
"""

BASE = {
    "chernozem": "2B211C",  # outlines, deep shadows, dark leather
    "ochre": "C9A15B",      # steppe soil, dry wood, parchment
    "grass": "9E9A5C",      # dry grass, fields
    "oak": "4E6B3A",        # forest, bushes, green cloth
    "whitewash": "EDE6D6",  # hut walls, shirts, UI text
    "cinnabar": "A8322D",   # coats, banners, health
    "blue": "2F4E7A",       # trousers, water, mana
    "gold": "D4A645",       # rare items, trims, rewards
    "steel": "6E7780",      # armour and weapons
    "dusk": "1C2230",       # night, fog, menu background
}

WORK = {
    "skin": "D29B74",
    "skin_dark": "B47A55",
    "hair": "2B211C",
    "hair_grey": "B9B2A6",
    "hair_brown": "4A3020",
    "hair_red": "8E3B1F",
    "hair_blond": "D2B06A",
    "hair_white": "E6E0D4",
    "fur": "3A2E28",
    "fur_grey": "6F655C",
    "leather": "5A3A26",
    "leather_light": "8A5A36",
    "wood": "8A5A36",
    "wood_dark": "5C3B26",
    "wood_light": "B48A5A",
    "thatch": "A98D5A",
    "straw": "D1B26A",
    "canvas": "D8CBB0",
    "canvas_dark": "A99C82",
    "clay": "B5764E",
    "stone": "8C8577",
    "stone_dark": "5F5A52",
    "iron": "4B5157",
    "steel_light": "A7AEB4",
    "cinnabar_dark": "7A2420",
    "blue_dark": "22385A",
    "blue_light": "4D6E9C",
    "oak_dark": "34492A",
    "oak_light": "6F8A4A",
    "grass_dark": "77754A",
    "gold_dark": "9C7A30",
    "ember": "E8742A",
    "fire": "F2B33D",
    "crimson": "8C1F3A",
}

COLORS = {**BASE, **WORK}


def srgb(name_or_hex):
    """(r, g, b) in 0..1, sRGB."""
    h = COLORS.get(name_or_hex, name_or_hex).lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def _to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def linear(name_or_hex, shade=1.0):
    """(r, g, b, 1) in linear space; `shade` multiplies the sRGB value first."""
    r, g, b = srgb(name_or_hex)
    return tuple(_to_linear(min(1.0, max(0.0, c * shade))) for c in (r, g, b)) + (1.0,)
