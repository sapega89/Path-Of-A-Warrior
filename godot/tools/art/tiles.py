"""What each tile of the campaign's maps is, for the maps in the new art.

    python godot/tools/art/tiles.py     # writes godot/client/assets/art/tiles.json

A map (godot/client/data/maps/N.json) is a grid of tile numbers in layers. The new art
(scripts/world/map_art.gd) paints the ground and stands 3D props on it, so for every tile
number it needs:
  ground: what the ground is in each of the tile's 3 x 3 parts, as an index into KINDS, or -1
          where the tile is see-through (so the edge of a road keeps its shape);
  prop:   what stands on a blocked cell drawn with that tile (PROPS below, by looking at the
          tiles): a fir, a bush, a rock, a fence, a wall, a tent, a hut, a cliff...
The kind of a tile's ground comes from GROUND below; a tile not listed there takes the kind
whose reference tiles are nearest in colour.
"""

import json
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TILES = os.path.join(ROOT, "client", "assets", "original", "tiles.png")
OUT = os.path.join(ROOT, "client", "assets", "art", "tiles.json")
TILE = 27
COLS = 16
COUNT = 240
PARTS = 3

KINDS = ["meadow", "grass", "dirt", "sand", "gravel", "stone", "rock", "water", "wood", "cobble"]


def ids(*spans):
    out = []
    for s in spans:
        out += list(range(s[0], s[1] + 1)) if isinstance(s, tuple) else [s]
    return out


# the ground of the tiles, by kind (the first ones of each list are its colour reference)
GROUND = {
    "meadow": ids(4, (28, 35)),
    "grass": ids(192, (50, 57)),
    "dirt": ids(2, (20, 27), 239, 240),
    "sand": ids((89, 96), 189),
    "gravel": ids(1, 3, (6, 10), 12, 237, 238),
    "stone": ids(5, (36, 40), 42),
    "rock": ids(14, 15, 16, 11, 13, (17, 19), 41, 43, (44, 49)),
    "water": ids(77, 145, (73, 76), (78, 81), 149),
    "wood": ids(147, 146, 148, 144, 61, 84, 99, 100, (150, 158), 161, 162, (166, 170), 173, 174),
    "cobble": ids(128, 127, 133, 134, (226, 236)),
}

# what stands on a blocked cell drawn with the tile
PROPS = {
    "fir": ids((65, 68)),
    "bush": ids(117, 118, 136),
    "boulder": ids((69, 72)),
    "rock": ids(101, 102),
    "pebbles": ids(137),
    "stump": ids(115, 116, 129, 130, 142),
    "barrel": ids(97, 98),
    "bucket": ids(131, 132),
    "hay": ids(111, 112),
    "well": ids(113, 114),
    "fire": ids(124, 139, 140),
    "fence": ids(59, 62, (119, 123), (161, 164), (177, 188)),
    "palisade": ids(58, 60, (82, 83), (85, 88), 109, 110),
    "chest": ids(105, 108),
    "woodpile": ids(103, 104, 106),
    "rack": ids(125, 126),
    "tuft": ids(141),
    "grave": ids(190),
    "tent": ids((193, 204), (217, 225)),
    "hut": ids(99, 100, 143, (150, 160), (165, 176), (205, 216)),
    "wall": ids(107, 127, (133, 135), (226, 236)),
    "cliff": ids(5, 11, (13, 19), (36, 49)),
}


def pixels(im, t):
    i = t - 1
    x0, y0 = (i % COLS) * TILE, (i // COLS) * TILE
    return [[im.getpixel((x0 + x, y0 + y)) for x in range(TILE)] for y in range(TILE)]


def average(px):
    op = [p for row in px for p in row if p[3] > 128]
    if not op:
        return None
    return tuple(sum(p[c] for p in op) / len(op) for c in range(3))


def main():
    im = Image.open(TILES).convert("RGBA")
    kind_of = {}
    for k, tiles in GROUND.items():
        for t in tiles:
            kind_of.setdefault(t, KINDS.index(k))
    refs = {KINDS.index(k): average(pixels(im, tiles[0])) for k, tiles in GROUND.items()}
    ground = {}
    for t in range(1, COUNT + 1):
        px = pixels(im, t)
        avg = average(px)
        if avg is None:
            continue
        kind = kind_of.get(t)
        if kind is None:
            kind = min(refs, key=lambda k: sum((avg[c] - refs[k][c]) ** 2 for c in range(3)))
        parts = []
        step = TILE / PARTS
        for py in range(PARTS):
            for pxi in range(PARTS):
                block = [px[y][x] for y in range(int(py * step), int((py + 1) * step))
                         for x in range(int(pxi * step), int((pxi + 1) * step))]
                solid = sum(1 for p in block if p[3] > 128) / len(block)
                parts.append(kind if solid >= 0.5 else -1)
        ground[str(t)] = parts
    props = {str(t): name for name, tiles in PROPS.items() for t in tiles}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"kinds": KINDS, "parts": PARTS, "ground": ground, "props": props}, f, indent=0, sort_keys=True)
        f.write("\n")
    print(f"{OUT}: {len(ground)} tiles with ground, {len(props)} with props")


if __name__ == "__main__":
    main()
