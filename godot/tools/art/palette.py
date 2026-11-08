"""Palette of the art style: worn, dusty colours of a hard steppe life (dull cloth, tarnished
brass, dark blood-red, weathered skin).

The ten base colours come from the style guide. Working colours are mixed from them
for things the base set does not cover (skin, wood, straw, canvas, leather).
Colours are sRGB hex; `linear()` converts them for vertex colours, which glTF stores
in linear space.
"""

BASE = {
    "chernozem": "2B211C",  # outlines, deep shadows, dark leather
    "ochre": "A88A57",      # steppe soil, dry wood, parchment
    "grass": "85814F",      # dry grass, fields
    "oak": "435A33",        # forest, bushes, green cloth
    "whitewash": "CFC5B0",  # hut walls, shirts, UI text
    "cinnabar": "8A2B25",   # coats, banners, health
    "blue": "2D3F57",       # trousers, water, mana
    "gold": "AE8C48",       # rare items, trims, rewards
    "steel": "6A7178",      # armour and weapons
    "dusk": "1C2230",       # night, fog, menu background
}

WORK = {
    "skin": "BE896A",
    "skin_dark": "9C6A4E",
    "hair": "2B211C",
    "hair_grey": "B9B2A6",
    "hair_brown": "4A3020",
    "hair_red": "8E3B1F",
    "hair_blond": "B0955E",
    "hair_white": "E6E0D4",
    "fur": "3A2E28",
    "fur_grey": "6F655C",
    "leather": "5A3A26",
    "leather_light": "765034",
    "wood": "8A5A36",
    "wood_dark": "5C3B26",
    "wood_light": "9A7650",
    "thatch": "8E7A52",
    "straw": "B09A62",
    "canvas": "BEB298",
    "canvas_dark": "948770",
    "clay": "9A6646",
    "stone": "8C8577",
    "stone_dark": "5F5A52",
    "iron": "4B5157",
    "steel_light": "9DA3A8",
    "cinnabar_dark": "64221E",
    "blue_dark": "222F42",
    "blue_light": "4A5F7A",
    "oak_dark": "34492A",
    "oak_light": "5E7442",
    "grass_dark": "77754A",
    "gold_dark": "7E6430",
    "ember": "E8742A",
    "fire": "F2B33D",
    "crimson": "74202F",
    "stubble": "7E6252",  # an unshaven jaw
    "skin_upyr": "8F9B7C",  # the grey-green skin of the forest upyr (the battles' monsters)
    "skin_upyr_dark": "6B7759",
    "bone": "DCCFB4",
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
