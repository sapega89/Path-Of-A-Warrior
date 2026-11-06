"""Converts the original game's maps and tiles into files the Godot client reads.

Step 1 of the Godot plan is to move the game over as it is, so the client uses the
original data and art for now. Run from the repo root:

    python godot/tools/import_original.py

Writes
  godot/client/data/maps/<n>.json        one per map (1..45), see MAP FORMAT below
  godot/client/assets/original/tiles.png the 240 map tiles in one atlas, 16 x 15 tiles of 27 px
  godot/client/assets/original/hero_<head>_<weapon>.png + hero.json
                                         the hero's frames, body + head + weapon put together as
                                         pyport draw_hero does, one cell per
                                         sprite frame; hero.json has the walk / idle tables

MAP FORMAT (N.MAP, as pyport/pow/game/map_scene.py load_map reads it):
  u8 w, u8 h, u8 n, n bytes (ids of the tiles the map uses),
  then 4 layers of w*h bytes: ground, upper, objects, flags,
  then optional cell scripts: u8 count, 2 bytes, per script u8 x, u8 y, u16 LE length, bytes.
  Tile id t (1..240) is image imgtile[(t-1) // 16] + "_" + "%02d" % ((t-1) % 16 + 1).
  flags bit 0 = blocked, bit 1 = the upper tile is drawn over the actors.
  objects = breakable things; kind k uses tile k (whole) and k+1 (broken), hp 41 for 101 / 113 else 21.
ROOMS (N.arr, as load_rooms reads it): the map is a grid of 7x7-tile rooms,
  (w // 7) * (h // 7) of them. Per mission m the rooms start at
  20 + rooms * m * 19; per room: 4 exits (down, left, up, right), max enemies,
  12 wave enemy kinds, 1 unused byte, general.
"""
import json
import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pyport"))
from pow.data import scr  # noqa: E402

CLIENT = ROOT / "godot" / "client"
TILE = 27
ROOM_BYTES = 19


def tile_name(tile_names, t):
    return "%s_%02d" % (tile_names[(t - 1) // 16], (t - 1) % 16 + 1)


def parse_map(data):
    w, h, n = data[0], data[1], data[2]
    i = 3 + n
    size = w * h
    layers = {}
    for name in ("ground", "upper", "objects", "flags"):
        layers[name] = list(data[i:i + size])
        i += size
    scripts = []
    if len(data) > i:
        count = data[i]
        i += 3
        for _ in range(count):
            x, y = data[i], data[i + 1]
            length = data[i + 2] | data[i + 3] << 8
            body = list(data[i + 4:i + 4 + length])
            scripts.append({"x": x, "y": y, "ops": [body[k:k + 3] for k in range(0, len(body), 3)]})
            i += 4 + length
    return {"w": w, "h": h, "tiles_used": list(data[3:3 + n]), **layers, "scripts": scripts}


def parse_rooms(data, w, h):
    rooms = (w // 7) * (h // 7)
    missions = []
    i = 20
    while rooms and i + rooms * ROOM_BYTES <= len(data):
        mission = []
        for _ in range(rooms):
            r = data[i:i + ROOM_BYTES]
            mission.append({"exits": list(r[0:4]), "max_enemies": r[4],
                            "waves": list(r[5:17]), "general": r[18]})
            i += ROOM_BYTES
        missions.append(mission)
    return {"rooms_x": w // 7, "rooms_y": h // 7, "header": list(data[:20]), "missions": missions}


def build_atlas(tile_names):
    atlas = Image.new("RGBA", (16 * TILE, 15 * TILE), (0, 0, 0, 0))
    found = 0
    for t in range(1, 241):
        path = ROOT / (tile_name(tile_names, t) + ".png")
        if not path.exists():
            continue
        img = Image.open(path).convert("RGBA")
        atlas.paste(img, (((t - 1) % 16) * TILE, ((t - 1) // 16) * TILE))
        found += 1
    return atlas, found


# SP3 frame tables (as load_frames reads them): u8 count, per frame 6 x u16 LE
# src_x, src_y, w, h, ox, oy; the part is drawn at (x - ox, y - oy).
def read_frames(path):
    d = path.read_bytes()
    u = lambda p: d[p] | d[p + 1] << 8
    return [tuple(u(1 + i * 12 + k * 2) for k in range(6)) for i in range(d[0])]


HERO_CELL = (96, 96)
HERO_ORIGIN = (48, 72)  # the hero's position (feet) inside a cell: centred across, 24 px under the middle
# weapon drawn behind the body when bit `sprite_frame` is set (as draw_hero does)
WEAPON_BEHIND_BITS = {0: 8263870709823, 1: 5789684072952}
HEADS = 4
WEAPONS = 2  # 0 long sword, 1 short sword


def build_hero(mdat, chars, head, weapon):
    body_img = Image.open(ROOT / (chars[44] + ".png")).convert("RGBA")
    head_img = Image.open(ROOT / (chars[46 + head] + ".png")).convert("RGBA")
    wep_img = Image.open(ROOT / (chars[42 + weapon] + ".png")).convert("RGBA")
    body = read_frames(ROOT / mdat[45])
    heads = read_frames(ROOT / mdat[47 + head])
    weps = read_frames(ROOT / mdat[87 + (weapon << 2)])
    count = len(body)
    cw, ch = HERO_CELL
    sheet = Image.new("RGBA", (cw * 16, ch * ((count + 15) // 16)), (0, 0, 0, 0))

    def paste(cell, img, f):
        sx, sy, w, h, ox, oy = f
        if w == 0 or h == 0:
            return
        part = img.crop((sx, sy, sx + w, sy + h))
        x = (cell % 16) * cw + HERO_ORIGIN[0] - ox
        y = (cell // 16) * ch + HERO_ORIGIN[1] - oy
        sheet.alpha_composite(part, (x, y))

    for i in range(count):
        behind = WEAPON_BEHIND_BITS[weapon] >> i & 1
        if behind and i < len(weps):
            paste(i, wep_img, weps[i])
        paste(i, body_img, body[i])
        if i < len(heads):
            paste(i, head_img, heads[i])
        if not behind and i < len(weps):
            paste(i, wep_img, weps[i])
    return sheet, count


def export_hero(out):
    mdat = scr.load(ROOT / "mdat_QVGA.scr")
    chars = scr.load(ROOT / "imgchar.scr")
    count = 0
    for head in range(HEADS):
        for weapon in range(WEAPONS):
            sheet, count = build_hero(mdat, chars, head, weapon)
            sheet.save(out / ("hero_%d_%d.png" % (head, weapon)))
    sys.path.insert(0, str(ROOT / "pyport"))
    from pow.game import consts
    info = {
        "cell": list(HERO_CELL), "origin": list(HERO_ORIGIN), "frames": count, "columns": 16,
        # tables per dir4 (consts.dir8_to_dir4), frame lists end with 222 (loop)
        "dir8_to_dir4": consts.dir8_to_dir4,
        "idle": consts.hero_anim_0, "walk": consts.hero_anim_1,
    }
    (out / "hero.json").write_text(json.dumps(info))


def main():
    tile_names = scr.load(ROOT / "imgtile.scr")
    map_files = [n for n in scr.load(ROOT / "mdat_QVGA.scr") if n.endswith(".MAP")]
    room_files = scr.load(ROOT / "edat.scr")
    out_maps = CLIENT / "data" / "maps"
    out_maps.mkdir(parents=True, exist_ok=True)
    for index, name in enumerate(map_files):
        m = parse_map((ROOT / name).read_bytes())
        m["number"] = index + 1
        m["rooms"] = parse_rooms((ROOT / room_files[index]).read_bytes(), m["w"], m["h"])
        (out_maps / ("%d.json" % (index + 1))).write_text(json.dumps(m, separators=(",", ":")))
    atlas, found = build_atlas(tile_names)
    out_tiles = CLIENT / "assets" / "original"
    out_tiles.mkdir(parents=True, exist_ok=True)
    atlas.save(out_tiles / "tiles.png")
    export_hero(out_tiles)
    print("maps: %d, tiles: %d" % (len(map_files), found))


if __name__ == "__main__":
    main()
