"""Converts the original game's maps and tiles into files the Godot client reads.

Step 1 of the Godot plan is to move the game over as it is, so the client uses the
original data and art for now. Run from the repo root:

    python godot/tools/import_original.py

Writes
  godot/client/data/maps/<n>.json        one per map (1..45), see MAP FORMAT below
  godot/client/assets/original/tiles.png the 240 map tiles in one atlas, 16 x 15 tiles of 27 px
  godot/client/assets/original/hero_<head>_<weapon>[_sk].png + hero.json
                                         the hero's frames, body + head + weapon put together as
                                         pyport draw_hero does, one cell per
                                         sprite frame; hero.json has the walk / idle tables
  godot/client/assets/original/enemy_<n>_<tint>.png
                                         the soldiers' frames (n 0 swords, 1 archers) in cells
                                         like the hero's, one sheet per mission tint (0..3), the
                                         palette swapped as load_recoloured does
  godot/client/assets/original/general_<look>_<side>_<base|sk>.png
                                         a general (body, head of his look, weapon of his side,
                                         the mark under him) as draw_enemy puts him together:
                                         base = walk / strike frames, sk = skill frames
  godot/client/assets/original/ui/*.png  UI pictures used as they are (exit arrows, ...)
  godot/client/data/tables.json          the game's constant tables the map code uses (animation
                                         frame lists, direction steps, ...), copied from
                                         pyport/pow/game/consts.py by name
  godot/client/data/talk.json            the dialogue lines (briefing, a general on the map,
                                         after a victory), see TALK_FILES
  godot/client/data/help.json            the Help topics and their pages (export_help)
  godot/client/data/visit.json           visiting a general: the greetings and talks, and
                                         the 44 generals one can visit (export_visit)
  godot/client/i18n/names.json           our names (own_names.json) in both languages, English
                                         name -> {"en", "uk"}, for the game to translate them
  godot/client/i18n/story.json           our story texts (own_story.json: the mission briefings,
                                         the opening and endings, the talks, the visits, the help)
                                         in both languages, English text -> {"en", "uk"}; the
                                         English goes into the data files in place of the
                                         imported texts (export_story_i18n)
  godot/client/data/campaign.json        chapters, lords (one map each) and missions, as the
                                         campaign screens read them (load_chapter_lords,
                                         load_lord_missions):
    mission.arr  rows of 38 bytes from 10: row r = 30-byte name of lord r (r >= 1),
                 6 lord ids of chapter r (r >= 0), first mission and mission count of lord r
    sideinfo.arr missions of 11 bytes from 11: id, start x, start y (tiles), tint, boss type,
                 general, reward, gold, time limit (u16), level bonus
    ruler.arr    mission names, 15 bytes per id from 3: 14-byte name, portrait
    brief.scr    (edat 56) the description of mission k, with the "(..)" macros put in
                 (expand_text, as pyport table_text)
    general.arr  the generals (read_generals): name, look, side, skills, stats

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
import re
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
ORIGINAL = ROOT / "original"  # the original game's files
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
        path = ORIGINAL / (tile_name(tile_names, t) + ".png")
        if not path.exists():
            continue
        img = Image.open(path).convert("RGBA")
        atlas.paste(img, (((t - 1) % 16) * TILE, ((t - 1) // 16) * TILE))
        found += 1
    return atlas, found


# SP3 frame tables (as load_frames reads them): u8 count, per frame 6 x s16 LE
# src_x, src_y, w, h, ox, oy; the part is drawn at (x - ox, y - oy) (ox / oy can be < 0).
def read_frames(path):
    d = path.read_bytes()

    def s16(p):
        v = d[p] | d[p + 1] << 8
        return v - 0x10000 if v >= 0x8000 else v
    return [tuple(s16(1 + i * 12 + k * 2) for k in range(6)) for i in range(d[0])]


HERO_CELL = (96, 96)
HERO_ORIGIN = (48, 72)  # the hero's position (feet) inside a cell: centred across, 24 px under the middle
# weapon drawn behind the body when bit `sprite_frame` is set (as draw_hero does)
WEAPON_BEHIND_BITS = {0: 8263870709823, 1: 5789684072952}
HEADS = 4
WEAPONS = 2  # 0 long sword, 1 short sword


def build_hero(mdat, chars, head, weapon):
    body_img = Image.open(ORIGINAL / (chars[44] + ".png")).convert("RGBA")
    head_img = Image.open(ORIGINAL / (chars[46 + head] + ".png")).convert("RGBA")
    wep_img = Image.open(ORIGINAL / (chars[42 + weapon] + ".png")).convert("RGBA")
    body = read_frames(ORIGINAL / mdat[45])
    heads = read_frames(ORIGINAL / mdat[47 + head])
    weps = read_frames(ORIGINAL / mdat[87 + (weapon << 2)])
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


HERO_SKILL_CELL = (128, 112)
HERO_SKILL_ORIGIN = (64, 88)  # the skill swings reach 55 px aside and 76 px up


def build_hero_skills(mdat, chars, head, weapon, flags):
    """The hero's skill frames (actions 12 and up), as draw_hero puts them together."""
    body_img = Image.open(ORIGINAL / (chars[44] + ".png")).convert("RGBA")
    head_img = Image.open(ORIGINAL / (chars[46 + head] + ".png")).convert("RGBA")
    wep_img = Image.open(ORIGINAL / (chars[42 + weapon] + ".png")).convert("RGBA")
    body = read_frames(ORIGINAL / mdat[46])
    heads = read_frames(ORIGINAL / mdat[51 + head])
    weps = read_frames(ORIGINAL / mdat[89 + (weapon << 2)])
    cw, ch = HERO_SKILL_CELL
    ox0, oy0 = HERO_SKILL_ORIGIN
    sheet = Image.new("RGBA", (cw * 16, ch * ((len(body) + 15) // 16)), (0, 0, 0, 0))

    def paste(cell, img, f):
        sx, sy, w, h, ox, oy = f
        if w > 0 and h > 0:
            sheet.alpha_composite(img.crop((sx, sy, sx + w, sy + h)),
                                  ((cell % 16) * cw + ox0 - ox, (cell // 16) * ch + oy0 - oy))

    for i in range(len(body)):
        behind = flags[(i >> 5 << 2) + (0 if weapon else 1)] >> (i & 31) & 1
        if behind and i < len(weps):
            paste(i, wep_img, weps[i])
        paste(i, body_img, body[i])
        if i < len(heads):
            paste(i, head_img, heads[i])
        if not behind and i < len(weps):
            paste(i, wep_img, weps[i])
    return sheet


def export_hero(out):
    mdat = scr.load(ORIGINAL / "mdat_QVGA.scr")
    chars = scr.load(ORIGINAL / "imgchar.scr")
    count = 0
    for head in range(HEADS):
        for weapon in range(WEAPONS):
            sheet, count = build_hero(mdat, chars, head, weapon)
            sheet.save(out / ("hero_%d_%d.png" % (head, weapon)))
    sys.path.insert(0, str(ROOT / "pyport"))
    from pow.game import consts
    for head in range(HEADS):
        for weapon in range(WEAPONS):
            build_hero_skills(mdat, chars, head, weapon, consts.general_frame_flags).save(
                out / ("hero_%d_%d_sk.png" % (head, weapon)))
    info = {
        "cell": list(HERO_CELL), "origin": list(HERO_ORIGIN), "frames": count, "columns": 16,
        "skill_cell": list(HERO_SKILL_CELL), "skill_origin": list(HERO_SKILL_ORIGIN),
        # tables per dir4 (consts.dir8_to_dir4), frame lists end with 222 (loop)
        "dir8_to_dir4": consts.dir8_to_dir4,
        "idle": consts.hero_anim_0, "walk": consts.hero_anim_1,
    }
    (out / "hero.json").write_text(json.dumps(info))


ENEMY_SPRITES = [(56, 82), (57, 83)]  # (imgchar image, mdat frame table): swords, archers
# Mission tint t replaces the 5 colours of palette 0 with those of palette t.
ENEMY_PALETTES = [
    [(236, 211, 197), (205, 143, 128), (129, 81, 69), (104, 60, 49), (79, 39, 29)],
    [(226, 205, 178), (196, 179, 152), (180, 142, 122), (135, 111, 47), (93, 73, 49)],
    [(174, 225, 242), (101, 156, 195), (61, 102, 139), (43, 78, 115), (45, 45, 84)],
    [(162, 199, 159), (135, 156, 119), (86, 123, 98), (33, 98, 63), (51, 51, 51)],
]


def recolour(img, tint):
    if tint == 0:
        return img
    swap = {ENEMY_PALETTES[0][b]: ENEMY_PALETTES[tint][b] for b in range(5)}
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a and (r, g, b) in swap:
                px[x, y] = swap[(r, g, b)] + (a,)
    return img


def export_enemies(out):
    mdat = scr.load(ORIGINAL / "mdat_QVGA.scr")
    chars = scr.load(ORIGINAL / "imgchar.scr")
    cw, ch = HERO_CELL
    for n, (image, table) in enumerate(ENEMY_SPRITES):
        frames = read_frames(ORIGINAL / mdat[table])
        for tint in range(len(ENEMY_PALETTES)):
            img = recolour(Image.open(ORIGINAL / (chars[image] + ".png")).convert("RGBA"), tint)
            sheet = Image.new("RGBA", (cw * 16, ch * ((len(frames) + 15) // 16)), (0, 0, 0, 0))
            for i, (sx, sy, w, h, ox, oy) in enumerate(frames):
                if w and h:
                    part = img.crop((sx, sy, sx + w, sy + h))
                    sheet.alpha_composite(part, ((i % 16) * cw + HERO_ORIGIN[0] - ox,
                                                 (i // 16) * ch + HERO_ORIGIN[1] - oy))
            sheet.save(out / ("enemy_%d_%d.png" % (n, tint)))


GENERAL_CELL = (96, 112)
GENERAL_ORIGIN = (48, 88)  # the skill frames reach 75 px above the feet
GENERAL_LOOKS = 6
# weapon behind the body (drawn first): base frames by bit (side 1, side 0); skill frames by
# general_frame_flags[(f >> 5 << 2) + (2 if side else 3)] bit (f & 31), as draw_enemy does
GENERAL_WEAPON_BEHIND = {1: 1310732, 0: 1053711}


def build_general(mdat, chars, look, side, skill, flags):
    body_img = Image.open(ORIGINAL / (chars[44] + ".png")).convert("RGBA")
    head_img = Image.open(ORIGINAL / (chars[50 + look - 1] + ".png")).convert("RGBA")
    wep_img = Image.open(ORIGINAL / (chars[42 + side] + ".png")).convert("RGBA")
    mark = Image.open(ORIGINAL / (chars[45] + ".png")).convert("RGBA")
    body = read_frames(ORIGINAL / mdat[69 if skill else 68])
    heads = read_frames(ORIGINAL / mdat[(76 if skill else 70) + look - 1])
    weps = read_frames(ORIGINAL / mdat[(90 if skill else 88) + (side << 2)])
    cw, ch = GENERAL_CELL
    ox0, oy0 = GENERAL_ORIGIN
    sheet = Image.new("RGBA", (cw * 16, ch * ((len(body) + 15) // 16)), (0, 0, 0, 0))

    def paste(cell, img, f):
        sx, sy, w, h, ox, oy = f
        if w > 0 and h > 0:
            sheet.alpha_composite(img.crop((sx, sy, sx + w, sy + h)),
                                  ((cell % 16) * cw + ox0 - ox, (cell // 16) * ch + oy0 - oy))

    for i in range(len(body)):
        if i >= 180:
            break
        x0, y0 = (i % 16) * cw, (i // 16) * ch
        bx, by, bw, bh, box, boy = body[i]
        # the general's mark under his feet
        mx, my = x0 + ox0 - box + bw // 2 - 13, y0 + oy0 - boy + bh - 5
        if 0 <= mx and mx + mark.width <= sheet.width and 0 <= my and my + mark.height <= sheet.height:
            sheet.alpha_composite(mark, (mx, my))
        if skill:
            behind = flags[(i >> 5 << 2) + (2 if side else 3)] >> (i & 31) & 1
        else:
            behind = GENERAL_WEAPON_BEHIND[side] >> i & 1
        if behind and i < len(weps):
            paste(i, wep_img, weps[i])
        paste(i, body_img, body[i])
        if i < len(heads):
            paste(i, head_img, heads[i])
        if not behind and i < len(weps):
            paste(i, wep_img, weps[i])
    return sheet


def export_generals(out):
    from pow.game import consts
    mdat = scr.load(ORIGINAL / "mdat_QVGA.scr")
    chars = scr.load(ORIGINAL / "imgchar.scr")
    for look in range(1, GENERAL_LOOKS + 1):
        for side in range(2):
            for skill in range(2):
                build_general(mdat, chars, look, side, skill, consts.general_frame_flags).save(
                    out / ("general_%d_%d_%s.png" % (look, side, "sk" if skill else "base")))


# general.arr: 23 bytes per general from 14: 11-byte name, look, -, side (0 = short sword
# as stored, the game flips it), 4 skills, portrait, gift table, attack, defence, HP
def read_generals():
    d = (ORIGINAL / "general.arr").read_bytes()
    out = {}
    g = 1
    while 23 * (g - 1) + 14 + 23 <= len(d):
        o = 23 * (g - 1) + 14
        b = d[o + 11:o + 23]
        out[g] = {"name": OWN_NAMES["generals"].get(str(g), [cstr(d[o:o + 11])])[0], "look": b[0], "side": (b[2] + 1) & 1,
                  "skills": list(b[3:7]), "portrait": b[7], "gift_table": b[8],
                  "attack": b[9], "defense": b[10], "hp": b[11]}
        g += 1
    return out


# Dialogue files (edat 57 + kind): u16 count, count + 1 u16 offsets, UTF-8 lines.
# Kind 0 the mission briefing, 1 a general met on the map, 2 the talk after a victory.
TALK_FILES = {"briefing": 57, "map": 58, "general": 59}


def export_talk(out):
    edat = scr.load(ORIGINAL / "edat.scr")
    talk = {}
    for name, index in TALK_FILES.items():
        d = (ORIGINAL / edat[index]).read_bytes()
        n = d[0] | d[1] << 8
        off = [d[2 + i * 2] | d[3 + i * 2] << 8 for i in range(n + 1)]
        talk[name] = [d[off[i]:off[i + 1]].decode("utf-8", "replace") for i in range(n)]
        talk[name] = own_story_lines(OWN_STORY["talk"][name], own_texts(talk[name]))
    (out / "talk.json").write_text(json.dumps(talk, ensure_ascii=False, indent=0))


# Visiting a general (edat 62 visit.scr, 52 visitgen.arr): the greetings, ten points of
# friendship to three lines (0..29 a general of topic 0, 30..59 of topic 1), then per topic
# the four things to talk about, two lines each (60.. topic 0, 68.. topic 1); and the 44
# generals one can visit (the Emperor's Seal lists them all).
def export_visit(out):
    edat = scr.load(ORIGINAL / "edat.scr")
    d = (ORIGINAL / edat[52]).read_bytes()
    n = d[0]
    width = d[1]
    generals = [int.from_bytes(d[1 + n + width * i:1 + n + width * (i + 1)], "little")
                for i in range((len(d) - 1 - n) // width)]
    lines = own_story_lines(OWN_STORY["visit"], own_texts(read_table(ORIGINAL / edat[62])))
    visit = {"lines": lines, "generals": generals}
    (out / "visit.json").write_text(json.dumps(visit, ensure_ascii=False, indent=0))


# Help (edat 61 help.scr): the topic names (uimenu.scr 38, "Missions|Visiting|...") and where
# each topic's pages start (the last two pages are the About box, not a topic); the pages shown are
# ours (own_story.json), as many as each topic needs.
HELP_TOPIC_START = [0, 5, 8, 14, 17, 22, 28, 35, 37]


def export_help(out):
    edat = scr.load(ORIGINAL / "edat.scr")
    pages = read_table(ORIGINAL / edat[61])
    names = read_table(ORIGINAL / "uimenu.scr")[38].split("|")
    topics = [{"name": names[i], "pages": pages[HELP_TOPIC_START[i]:HELP_TOPIC_START[i + 1]]}
              for i in range(len(HELP_TOPIC_START) - 1)]
    for topic, own in zip(topics, OWN_STORY["help"]):
        topic["name"] = own_story_text(own["name"], topic["name"])
        topic["pages"] = [own_story_text(page) for page in own["pages"]]  # ours, as many as we wrote
    (out / "help.json").write_text(json.dumps({"topics": topics}, ensure_ascii=False, indent=0))


def read_table(path):
    """A text table: u16 count, count + 1 u16 offsets, UTF-8 strings."""
    d = path.read_bytes()
    n = d[0] | d[1] << 8
    off = [d[2 + i * 2] | d[3 + i * 2] << 8 for i in range(n + 1)]
    return [d[off[i]:off[i + 1]].decode("utf-8", "replace") for i in range(n)]


# The Skills page: the 19 skills (12..30) with what each does, the seven groups it shows
# one row each, and the row's three places (0: an empty place).
SKILL_ROWS = [[12, 13, 14], [15, 16, 0], [17, 18, 19], [20, 21, 22], [23, 24, 25], [26, 27, 0],
              [28, 29, 30]]


# Our names for the game's things (own_names.json): section -> imported name -> [en, uk].
OWN_NAMES = json.loads((pathlib.Path(__file__).with_name("own_names.json")).read_text(encoding="utf-8"))


def own_name(section, name):
    """Our English name for an imported one (the name itself when the table has none)."""
    return OWN_NAMES.get(section, {}).get(name, [name])[0]


TITLES = ("Lord", "Lady", "General", "Emperor", "Empress")


def own_title(name):
    """"Lord Gabriel" -> our person with his rank ("Colonel Bairak"); else the name as it is."""
    title, _, base = name.partition(" ")
    person = OWN_NAMES["people"].get(base)
    return person[2] if title in TITLES and person else name


def _own_text_rules():
    rules = [(re.compile(re.escape(a)), b) for a, b in OWN_NAMES["phrases"].items()]
    for a in sorted(OWN_NAMES["places"], key=len, reverse=True):
        rules.append((re.compile(r"\b%s\b" % re.escape(a)), OWN_NAMES["places"][a][0]))
    names = "|".join(sorted(map(re.escape, OWN_NAMES["people"]), key=len, reverse=True))
    people = OWN_NAMES["people"]
    rules.append((re.compile(r"\b(?:%s) (%s)\b" % ("|".join(TITLES), names)), lambda m: people[m.group(1)][2]))
    rules.append((re.compile(r"\b(%s)\b" % names), lambda m: people[m.group(1)][4]))
    return rules


OWN_TEXT_RULES = _own_text_rules()


def own_text(text):
    """The text with our names of people and places (own_names.json people, places, phrases)."""
    for pattern, new in OWN_TEXT_RULES:
        text = pattern.sub(new, text)
    return text


def own_texts(data):
    """own_text on every string in a JSON value."""
    if isinstance(data, str):
        return own_text(data)
    if isinstance(data, list):
        return [own_texts(x) for x in data]
    if isinstance(data, dict):
        return {k: own_texts(v) for k, v in data.items()}
    return data


OWN_STORY = json.loads((pathlib.Path(__file__).with_name("own_story.json")).read_text(encoding="utf-8"))
STORY_I18N = {}


def own_story_text(own, imported=""):
    """Our English text for an imported one ({"en", "uk"} of own_story.json), noting both languages
    for i18n/story.json; the imported text itself when ours is None (a line the game fills in)."""
    if own is None:
        return imported
    en, uk = own["en"], own["uk"]
    # a line of an ending: "<number>|text"; the game translates the text after the bar
    head = re.match(r"\d+\|", en)
    key = en[head.end():] if head else en
    STORY_I18N[key] = {"en": key, "uk": uk[head.end():] if head and re.match(r"\d+\|", uk) else uk}
    return en


def own_story_lines(own, imported):
    """Our texts in place of a table of imported ones; they must be as many."""
    if len(own) != len(imported):
        raise ValueError("own_story.json: %d texts for %d imported" % (len(own), len(imported)))
    return [own_story_text(a, b) for a, b in zip(own, imported)]


def export_story_i18n(out):
    """i18n/story.json: every English text of own_story.json -> its text in each language."""
    (out / "story.json").write_text(json.dumps(STORY_I18N, ensure_ascii=False, indent=0, sort_keys=True),
                                    encoding="utf-8")


def export_names(out):
    """i18n/names.json: every English name of own_names.json -> its text in each language
    (a person also with his rank)."""
    names = {}
    for section, table in OWN_NAMES.items():
        if not isinstance(table, dict) or section == "phrases":
            continue
        for value in table.values():
            for en, uk in zip(value[0:4:2], value[1:4:2]):
                names[en] = {"en": en, "uk": uk}
    (out / "names.json").write_text(json.dumps(names, ensure_ascii=False, indent=0, sort_keys=True),
                                    encoding="utf-8")


def export_skills(out):
    edat = scr.load(ORIGINAL / "edat.scr")
    text = read_table(ORIGINAL / edat[54])
    menu = read_table(ORIGINAL / edat[69])
    skills = {"names": [own_name("skills", n) for n in text[0:19]], "effects": text[19:38], "groups": menu[48:55], "rows": SKILL_ROWS}
    (out / "skills.json").write_text(json.dumps(skills, ensure_ascii=False, indent=0))


# The things the hero can carry (edat 47 / 51 / 49). Gear 101..300 (23 bytes each from 9):
# name, slot, the stat its bonus goes to (0 ATK, 1 DEF, 2 HP, 3 MP), bonus, the random extra
# a found one may get, icon. Treasures 301..500 (24 bytes from 10) and rare things 501..
# (27 bytes from 9): name, slot, ATK (u16), DEF, HP (u8 / u16), MP, icon, the level needed.
# A gear's level needed comes from its tier (id % 5). A rare thing's icon is id - 501.
GEAR_LEVELS = [70, 1, 10, 25, 45]


def s8(v):
    return v - 256 if v > 127 else v


def export_items(out):
    edat = scr.load(ORIGINAL / "edat.scr")
    gear, treasures, rare = {}, {}, {}
    d = (ORIGINAL / edat[47]).read_bytes()
    k = 0
    while 9 + 23 * (k + 1) <= len(d):
        i = 9 + 23 * k
        gear[101 + k] = {"name": own_name("items", cstr(d[i:i + 15])), "slot": s8(d[i + 15]), "stat": s8(d[i + 16]),
                         "bonus": s8(d[i + 17]), "range": s8(d[i + 18]), "enchant_max": d[i + 19],
                         "price": d[i + 20] | d[i + 21] << 8, "icon": s8(d[i + 22]),
                         "level": GEAR_LEVELS[(101 + k) % 5]}
        k += 1
    d = (ORIGINAL / edat[51]).read_bytes()
    k = 0
    while 10 + 24 * (k + 1) <= len(d):
        i = 10 + 24 * k
        treasures[301 + k] = {"name": own_name("items", cstr(d[i:i + 15])), "slot": s8(d[i + 15]),
                              "attack": d[i + 16] | d[i + 17] << 8, "defense": s8(d[i + 18]),
                              "hp": d[i + 19], "mp": s8(d[i + 20]), "enchant_max": d[i + 21],
                              "icon": s8(d[i + 22]), "level": d[i + 23]}
        k += 1
    d = (ORIGINAL / edat[49]).read_bytes()
    k = 0
    while 9 + 27 * (k + 1) <= len(d):
        i = 9 + 27 * k
        rare[501 + k] = {"name": own_name("items", cstr(d[i:i + 15])), "slot": s8(d[i + 15]),
                         "attack": d[i + 16] | d[i + 17] << 8, "defense": s8(d[i + 18]),
                         "hp": d[i + 19] | d[i + 20] << 8, "mp": s8(d[i + 21]),
                         "price": int.from_bytes(d[i + 22:i + 26], "little"), "icon": k,
                         "level": d[i + 26]}
        k += 1
    (out / "items.json").write_text(json.dumps({"gear": gear, "treasures": treasures, "rare": rare},
                                               ensure_ascii=False, indent=0))
    return len(gear) + len(treasures) + len(rare)


# The stories (edat 63 the opening, 64.. the endings, six to a file). Ending s: its lines
# from story_offsets[2s] - the file's first, talk pages up to story_offsets[2s + 1], picture
# pages up to story_offsets[2s + 2]. Story pictures are imgui e1..e15, portraits imgchar
# 0..41 (noface, the generals jang_1..37, the hero's heads ju_1..4).
STORY_PICTURES = ["e%d" % i for i in range(1, 16)]


def zip_same(own, imported):
    if len(own) != len(imported):
        raise ValueError("own_story.json: %d texts for %d imported" % (len(own), len(imported)))
    return zip(own, imported)


def _story_line(own, key):
    """A talk line of an ending ("<portrait>|text", the hero's without a portrait) or a picture
    ("<picture>|text") of own_story.json as the data has it; None stays None."""
    if own is None:
        return None
    number = int(own[key])
    if key == "who" and number < 0:
        return own
    return {"en": "%d|%s" % (number, own["en"]), "uk": "%d|%s" % (number, own["uk"])}


def export_stories(out, assets):
    sys.path.insert(0, str(ROOT / "pyport"))
    from pow.game import consts
    edat = scr.load(ORIGINAL / "edat.scr")
    offsets = consts.story_offsets
    endings = []
    for s in range(24):
        lines = read_table(ORIGINAL / edat[64 + s // 6])
        base = offsets[s // 6 * 12]
        p0, p1, p2 = (offsets[2 * s + i] - base for i in range(3))
        own = OWN_STORY["stories"]["endings"][s]
        talk = [own_story_text(_story_line(t, "who"), line)
                for t, line in zip_same(own["talk"], own_texts(lines[p0:p1]))]
        pictures = [own_story_text(_story_line(t, "pic"), line)
                    for t, line in zip_same(own["pictures"], own_texts(lines[p1:p2]))]
        endings.append({"talk": talk, "pictures": pictures})
    own = OWN_STORY["stories"]
    stories = {"opening": own_story_lines(own["opening"], own_texts(read_table(ORIGINAL / edat[63]))),
               "endings": endings,
               "gamestr": own_story_lines(own["gamestr"], own_texts(read_table(ORIGINAL / "gamestr.scr")[:2])),
               "titles": own_story_lines(own["titles"], own_texts(read_table(ORIGINAL / edat[54])[38:62]))}
    (out / "stories.json").write_text(json.dumps(stories, ensure_ascii=False, indent=0))
    (assets / "story").mkdir(parents=True, exist_ok=True)
    for name in STORY_PICTURES:
        Image.open(ORIGINAL / (name + ".png")).convert("RGBA").save(assets / "story" / (name + ".png"))
    chars = scr.load(ORIGINAL / "imgchar.scr")
    (assets / "portraits").mkdir(parents=True, exist_ok=True)
    for i in range(42):
        Image.open(ORIGINAL / (chars[i] + ".png")).convert("RGBA").save(assets / "portraits" / ("%d.png" % i))


def cstr(b):
    return bytes(b).split(b"\0")[0].decode("utf-8", "replace")


def read_exp_table():
    """The exp the hero needs to go from level n + 1 to n + 2 (exp.arr: u16 count, s32 each)."""
    d = (ORIGINAL / "exp.arr").read_bytes()
    return [int.from_bytes(d[2 + 4 * k:6 + 4 * k], "little", signed=True) for k in range((len(d) - 2) // 4)]


def expand_text(table, i):
    """Text i of a table with its macros put in, as pyport table_text does: a text that starts
    with a number and "|" is that text of the table with each "(..)" replaced by the next of
    its own "|" parts; any other text just loses the brackets of its "(..)"."""
    src = table[i]
    head = re.match(r"(\d{1,3})\|", src)
    if head is None:
        return re.sub(r"\(([^)]*)\)", r"\1", src)
    parts = src[head.end():].split("|")
    return re.sub(r"\([^)]*\)", lambda m: parts.pop(0) if parts else "", table[int(head.group(1))])


def export_campaign(out):
    rows = (ORIGINAL / "mission.arr").read_bytes()
    side = (ORIGINAL / "sideinfo.arr").read_bytes()
    names = (ORIGINAL / "ruler.arr").read_bytes()
    chapters, lords = [], {}
    r = 0
    while 38 * r + 10 + 38 <= len(rows):
        o = 38 * r + 10
        chapters.append([b for b in rows[o + 30:o + 36] if b > 0])  # chapter r
        if r > 0:
            name = own_name("chapters", str(r)) if str(r) in OWN_NAMES["chapters"] else cstr(rows[o:o + 30])
            lords[r] = {"name": name, "first_mission": rows[o + 36], "missions": rows[o + 37]}
        r += 1
    while chapters and not chapters[-1]:
        chapters.pop()
    edat = scr.load(ORIGINAL / "edat.scr")
    descriptions = read_table(ORIGINAL / edat[56])
    missions = []
    i = 11
    while i + 11 <= len(side):
        m = side[i:i + 11]
        mid = m[0]
        n = 3 + (mid - 1) * 15
        missions.append({
            "id": mid, "start": [m[1], m[2]], "tint": m[3], "boss_type": m[4], "general": m[5],
            "reward": m[6], "gold": m[7], "time_limit": m[8] | m[9] << 8, "level_bonus": m[10],
            "name": own_title(cstr(names[n:n + 14])) if mid > 0 else "",
            "portrait": int.from_bytes(names[n + 14:n + 15], "little", signed=True) if mid > 0 else 0,
            "description": own_story_text(OWN_STORY["missions"][len(missions)],
                                          own_text(expand_text(descriptions, len(missions))) if len(missions) < len(descriptions) else ""),
        })
        i += 11
    (out / "campaign.json").write_text(json.dumps(
        {"chapters": chapters, "lords": lords, "missions": missions, "generals": read_generals(),
         "exp_table": read_exp_table()},
        ensure_ascii=False, indent=0))
    return len(chapters), len(missions)


UI_IMAGES = ["arrow0", "arrow1", "arrow2", "arrow3",  # exit arrows: down, left, up, right
             "tool", "gold",  # things on the floor: potions and gear (28 px frames), gold
             # the map's HUD: top bars, bottom panel with the HP / MP balls, the cover
             # that empties a ball, digits (0-9 , + :) and small digits (0-9 / x)
             "box_01", "box_01_R", "box_02", "box_02R", "ball_black", "number1", "number2",
             # the skills' icons (28 px, skill 12 first), learned and not yet learned
             "skill", "skillgray",
             # the icons of gear, treasures and rare things (28 px), the Gear page's frame
             "kibo", "sungbo", "shinki", "ui_equipbox",
             # the Blacksmith's sparkle over what is enchanted or combined (5 frames)
             "itemReinforce"]


def export_ui(out):
    out.mkdir(parents=True, exist_ok=True)
    for name in UI_IMAGES:
        Image.open(ORIGINAL / (name + ".png")).convert("RGBA").save(out / (name + ".png"))


TABLES = [
    "dir8_to_dir4", "dir_dx8", "dir_dy8", "speed_frame_ms",
    "hero_anim_0", "hero_anim_1", "hero_anim_2", "hero_anim_3", "hero_anim_4", "hero_anim_5",
    "hero_anim_6", "hero_anim_7", "hero_anim_8", "hero_anim_9", "hero_anim_10", "hero_anim_11",
    "hero_anim_12", "hero_anim_13", "hero_anim_14", "hero_anim_15_19", "hero_anim_20",
    "hero_anim_21", "hero_anim_22", "hero_anim_23_24", "hero_anim_25", "hero_anim_26_27",
    "hero_anim_28", "hero_anim_29", "hero_anim_30",
    "head_anim_0", "head_anim_1", "head_anim_2", "head_anim_3",
    "body_anim_0", "body_anim_1", "body_anim_2", "body_anim_3",
    "weapon_anim_1", "weapon_anim_2", "weapon_anim_3", "general_frame_flags",
    "squad_offsets", "hit_box_x", "hit_box_y", "hit_box_w", "hit_box_h", "front_dx", "front_dy",
    "weapon_reach", "skill_attack_div", "troop_names",
]


def export_tables(out):
    from pow.game import consts
    tables = {name: getattr(consts, name) for name in TABLES}
    (out / "tables.json").write_text(json.dumps(tables, separators=(",", ":")))


# The effects of the hero's skills, potions and scrolls: (sheet, frames file of mdat, table
# of pictures in consts or None, the [part, picture] pairs if not part i with picture i).
# A frame shows its picture (imgeff entry picture - 27) with its part's offset; the slash
# frames (sheet "slash") are regions of the picture effect1 instead.
EFFECTS = [
    ("slash", 56, None, None),
    ("heal", 57, "fx_anim_15_16", None),
    ("buff", 58, "fx_anim_17_19", None),
    ("whirl", 59, "fx_anim_21", None),
    ("fire", 60, "fx_fire", None),
    ("burst", 61, "fx_anim_24", [[1, 0], [1, 1]]),
    ("wave", 62, "fx_anim_26_27", None),
    ("blast", 63, "fx_anim_27_end", None),
    ("storm", 64, "fx_anim_28", None),
    ("quake", 65, "fx_anim_29", None),
    ("rain", 66, "fx_anim_30", None),
    ("scroll", 67, "fx_item_10_11", None),
    ("spark", 55, None, None),
    ("trail", 86, None, None),
    ("aura", 98, None, None),
]
## The sheets cut as regions of one picture: imgeff entry 1, or the entry named here (the
## aura of a buff: 3 glowing rings on the ground, then 3 pictures of the light rising).
EFFECT_IMAGE = {"spark": 0, "trail": 2, "aura": 44}
## Sheets whose pictures are made of several parts drawn together: the weapon trail is two
## parts a picture (4 directions x 3 steps).
EFFECT_GROUP = {"trail": 2}
EFFECT_COLUMNS = 8


def _merge_cells(parts):
    """One picture of parts (image, x, y) drawn over each other, with its own x, y."""
    x0 = min(p[1] for p in parts)
    y0 = min(p[2] for p in parts)
    x1 = max(p[1] + p[0].width for p in parts)
    y1 = max(p[2] + p[0].height for p in parts)
    img = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
    for p in parts:
        img.alpha_composite(p[0], (p[1] - x0, p[2] - y0))
    return img, x0, y0


def export_effects(out):
    from pow.game import consts
    mdat = scr.load(ORIGINAL / "mdat_QVGA.scr")
    eff = scr.load(ORIGINAL / "imgeff.scr")
    info = {}
    for name, frames_file, table, pairs in EFFECTS:
        parts = read_frames(ORIGINAL / mdat[frames_file])
        pics = getattr(consts, table) if table else None
        if pairs is None:
            n = len(pics) if pics else len(parts)
            pairs = [[i, i] for i in range(min(n, len(parts)))]
        cells = []  # (image or None, x, y) with the point of the effect at 0, 0
        for part, pic in pairs:
            sx, sy, w, h, ox, oy = parts[part]
            if pics is None:
                src = Image.open(ORIGINAL / (eff[EFFECT_IMAGE.get(name, 1)] + ".png")).convert("RGBA")
                cells.append((src.crop((sx, sy, sx + w, sy + h)), -ox, -oy))
            elif pics[pic] != 0:
                cells.append((Image.open(ORIGINAL / (eff[pics[pic] - 27] + ".png")).convert("RGBA"), -ox, -oy))
            else:
                cells.append((None, 0, 0))
        group = EFFECT_GROUP.get(name, 1)
        if group > 1:
            cells = [_merge_cells(cells[i:i + group]) for i in range(0, len(cells), group)]
        drawn = [c for c in cells if c[0] is not None]
        x0 = min(c[1] for c in drawn)
        y0 = min(c[2] for c in drawn)
        x1 = max(c[1] + c[0].width for c in drawn)
        y1 = max(c[2] + c[0].height for c in drawn)
        cw, ch = x1 - x0, y1 - y0
        cols = min(EFFECT_COLUMNS, len(cells))
        rows = (len(cells) + cols - 1) // cols
        sheet = Image.new("RGBA", (cw * cols, ch * rows), (0, 0, 0, 0))
        for i, (img, x, y) in enumerate(cells):
            if img is not None:
                sheet.alpha_composite(img, ((i % cols) * cw + x - x0, (i // cols) * ch + y - y0))
        sheet.save(out / ("fx_%s.png" % name))
        info[name] = {"cell": [cw, ch], "origin": [-x0, -y0], "frames": len(cells), "columns": cols}
    (out / "effects.json").write_text(json.dumps(info, separators=(",", ":")))


MIX_ROWS = 149


def export_mixing(out):
    """The Blacksmith's Combine: item-mixing-table.bin is four columns of 149 numbers (16 bit):
    three things (their ids, smallest first) and what they make. Rows for the same three are
    next to each other; one of them is chosen at random."""
    d = (ORIGINAL / "item-mixing-table.bin").read_bytes()
    e = [d[i] | d[i + 1] << 8 for i in range(0, len(d), 2)]
    rows = [[e[i], e[MIX_ROWS + i], e[2 * MIX_ROWS + i], e[3 * MIX_ROWS + i]] for i in range(MIX_ROWS)]
    (out / "mixing.json").write_text(json.dumps(rows, separators=(",", ":")))


SOUND_FONTS = ["/usr/share/sounds/sf2/FluidR3_GM.sf2", "/usr/share/sounds/sf2/default-GM.sf2"]


def export_sounds(out):
    """The effects snd3..16 as they are (sfx_N.wav); the three MIDI tunes snd0..2 played
    through a General MIDI sound font into music_N.ogg (needs fluidsynth and ffmpeg). A tune
    already made is kept: delete it to make it again."""
    import shutil
    import subprocess
    import tempfile
    out.mkdir(parents=True, exist_ok=True)
    for n in range(3, 17):
        shutil.copyfile(ORIGINAL / ("snd%d.wav" % n), out / ("sfx_%d.wav" % n))
    font = next((f for f in SOUND_FONTS if pathlib.Path(f).exists()), None)
    if font is None or not shutil.which("fluidsynth") or not shutil.which("ffmpeg"):
        print("music: fluidsynth, ffmpeg or a sound font missing, the tunes are kept")
        return
    with tempfile.TemporaryDirectory() as tmp:
        for n in range(3):
            if (out / ("music_%d.ogg" % n)).exists():
                continue
            wav = pathlib.Path(tmp) / ("music_%d.wav" % n)
            subprocess.run(["fluidsynth", "-ni", "-F", str(wav), "-r", "44100", font,
                            str(ORIGINAL / ("snd%d.mid" % n))], check=True, capture_output=True)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-c:a", "libvorbis",
                            "-q:a", "3", str(out / ("music_%d.ogg" % n))], check=True)


def main():
    tile_names = scr.load(ORIGINAL / "imgtile.scr")
    map_files = [n for n in scr.load(ORIGINAL / "mdat_QVGA.scr") if n.endswith(".MAP")]
    room_files = scr.load(ORIGINAL / "edat.scr")
    out_maps = CLIENT / "data" / "maps"
    out_maps.mkdir(parents=True, exist_ok=True)
    for index, name in enumerate(map_files):
        m = parse_map((ORIGINAL / name).read_bytes())
        m["number"] = index + 1
        m["rooms"] = parse_rooms((ORIGINAL / room_files[index]).read_bytes(), m["w"], m["h"])
        (out_maps / ("%d.json" % (index + 1))).write_text(json.dumps(m, separators=(",", ":")))
    chapters, missions = export_campaign(CLIENT / "data")
    export_tables(CLIENT / "data")
    export_talk(CLIENT / "data")
    export_visit(CLIENT / "data")
    export_help(CLIENT / "data")
    export_names(CLIENT / "i18n")
    export_skills(CLIENT / "data")
    export_items(CLIENT / "data")
    export_mixing(CLIENT / "data")
    export_stories(CLIENT / "data", CLIENT / "assets" / "original")
    export_story_i18n(CLIENT / "i18n")
    atlas, found = build_atlas(tile_names)
    out_tiles = CLIENT / "assets" / "original"
    out_tiles.mkdir(parents=True, exist_ok=True)
    atlas.save(out_tiles / "tiles.png")
    export_hero(out_tiles)
    export_enemies(out_tiles)
    export_generals(out_tiles)
    export_ui(out_tiles / "ui")
    export_effects(out_tiles)
    export_sounds(out_tiles / "sound")
    print("maps: %d, tiles: %d, chapters: %d, missions: %d" % (len(map_files), found, chapters, missions))


if __name__ == "__main__":
    main()
