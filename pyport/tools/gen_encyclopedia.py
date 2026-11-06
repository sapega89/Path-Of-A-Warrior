"""Builds the players' encyclopedia (pyport/web/encyclopedia.html) from the original game data.

    python pyport/tools/gen_encyclopedia.py          # -> pyport/web/encyclopedia.html

Everything on the page is read from the resource files in the repository root (kibo / sungbo /
shinki / general / mission / sideinfo / ruler / N.arr / *.scr / item-mixing-table.bin and the
PNG sheets), so after a data change it is enough to run the script again. The few numbers the
game keeps as constants (consumables, skill MP, the drop table, soldier stats) are taken
from pow.game.consts or copied here with a note where they come from.

Needs Pillow (icons are cut from the sheets and embedded as data: URIs, the page is one file).
build_web.py copies the page next to the game, like guide.html.
"""
import base64
import io
import json
import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
PY = ROOT / "pyport"
sys.path.insert(0, str(PY))
from pow.game import consts as ae  # noqa: E402

OUT = PY / "web" / "encyclopedia.html"


# ---- readers -------------------------------------------------------------------------------

def raw(name):
    return (ROOT / name).read_bytes()


def strings(name):
    """.scr string table: u16 count, (count+1) u16 offsets, UTF-8 bodies."""
    a = raw(name)
    n = a[0] | a[1] << 8
    off = [a[2 + i * 2] | a[3 + i * 2] << 8 for i in range(n + 1)]
    # a few texts keep EUC-KR curly quotes (\xa1\xae / \xa1\xaf) from the Korean original
    return [a[off[i]:off[i + 1]].replace(b"\xa1\xae", "\u2018".encode()).replace(b"\xa1\xaf", "\u2019".encode())
            .decode("utf-8", "replace") for i in range(n)]


class Table:
    """Fixed-width.arr table: u8 columns, u8 widths, rows of LE cells."""

    def __init__(self, name):
        b = raw(name)
        n = b[0]
        self.w = list(b[1:1 + n])
        self.o = [sum(self.w[:i]) for i in range(n)]
        self.size = sum(self.w)
        self.data = b[1 + n:]
        self.rows = len(self.data) // self.size

    def int(self, r, c):
        base = r * self.size + self.o[c]
        return int.from_bytes(self.data[base:base + self.w[c]], "little")

    def str(self, r, c):
        base = r * self.size + self.o[c]
        return self.data[base:base + self.w[c]].split(b"\0")[0].decode("latin-1").strip()


def s8(v):
    return v - 256 if v > 127 else v


# ---- images --------------------------------------------------------------------------------

IMG = {}          # key -> data URI (each picture is stored once, entries refer to it by key)


def _uri(im):
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def sheet(name):
    return Image.open(ROOT / name).convert("RGBA")


_SHEETS = {}


def cell(name, idx, w=28, h=28):
    key = "%s:%d" % (name, idx)
    if key not in IMG:
        sh = _SHEETS.setdefault(name, sheet(name))
        IMG[key] = _uri(sh.crop((idx * w, 0, idx * w + w, h)))
    return key


def portrait(n):
    """imgchar index: 0 = noface, N = jang_N (ruler.arr byte 14, general.arr column 8)."""
    name = "jang_%d.png" % n if n else "noface.png"
    if name not in IMG:
        IMG[name] = _uri(sheet(name))
    return name


def sp3(name):
    b = raw(name)
    return [tuple(int.from_bytes(b[1 + 12 * i + 2 * k:3 + 12 * i + 2 * k], "little", signed=True)
                  for k in range(6)) for i in range(b[0])]


def head(b):
    """Head sprite of a general (g_head{b}.png, first frame = facing the player)."""
    key = "g_head%d" % b
    if key not in IMG:
        x, y, w, h, _, _ = sp3("g_head%d.SP3" % b)[0]
        IMG[key] = _uri(sheet("g_head%d.png" % b).crop((x, y, x + w, y + h)))
    return key


# soldiers of a mission are recoloured by sideinfo byte 3 (palette 1..3)
PAL = [[(236, 211, 197), (205, 143, 128), (129, 81, 69), (104, 60, 49), (79, 39, 29)],
       [(226, 205, 178), (196, 179, 152), (180, 142, 122), (135, 111, 47), (93, 73, 49)],
       [(174, 225, 242), (101, 156, 195), (61, 102, 139), (43, 78, 115), (45, 45, 84)],
       [(162, 199, 159), (135, 156, 119), (86, 123, 98), (33, 98, 63), (51, 51, 51)]]


def soldier(mon, pal, frame=0):
    key = "%s:%d" % (mon, pal)
    if key not in IMG:
        im = Image.open(ROOT / (mon + ".png"))
        if pal:
            p = im.getpalette()
            for k in range(0, len(p), 3):
                c = tuple(p[k:k + 3])
                if c in PAL[0]:
                    p[k:k + 3] = PAL[pal][PAL[0].index(c)]
            im.putpalette(p)
        im = im.convert("RGBA")
        x, y, w, h, _, _ = sp3(mon + ".SP3")[frame]
        IMG[key] = _uri(im.crop((x, y, x + w, y + h)))
    return key


# ---- items ---------------------------------------------------------------------------------

TYPE = ["Зброя (довга)", "Зброя (коротка)", "Шолом", "Броня", "Рукавиці", "Чоботи", "Пояс",
        "Наруч", "Амулет", "Особливе"]
STAT = ["ATK", "DEF", "HP", "MP"]
TIER_LV = ae.tier_levels                    # reqLevel of the 5 tiers of Normal items

# drop class 0 soldier / 1 general / 2 mission target
DROP_CHANCE = [5, 10, 20]         # % that the enemy drops anything but gold
DROP_ITEM = [10, 30, 60]          # % of those drops that are a Normal item (else a consumable)
DROP_LV = [69, 44, 24, 9, 0]      # hero level > value -> row of DROP_TIER
DROP_TIER = [[0, 0, 33, 77, 100], [5, 30, 55, 80, 100], [30, 60, 90, 100, 100],
             [40, 80, 100, 100, 100], [80, 100, 100, 100, 100]]
DROP_LV_RANGE = ["70+", "45–69", "25–44", "10–24", "1–9"]

SPECIAL_NOTE = {
    434: "Використати в Inventory: назавжди HP +5.",
    435: "Використати в Inventory: назавжди MP +3.",
    436: "Використати в Inventory: назавжди DEF +1.",
    437: "Використати в Inventory: назавжди ATK +1.",
    502: "Сюжетний предмет: видається за кінцівку «Bloody Scarp». Потрібен для кінцівки «Love Of "
         "Warrior». Не вдягається.",
    504: "Відкриває у Visiting усіх 44 генералів. У звичайній грі не видається.",
}


def load_items():
    items = {}
    kibo, sungbo, shinki = Table("kibo.arr"), Table("sungbo.arr"), Table("shinki.arr")
    for r in range(kibo.rows):                                  # Normal 101..200
        iid = 101 + r
        st, base, spr = kibo.int(r, 2), kibo.int(r, 3), kibo.int(r, 4)
        items[iid] = {"id": iid, "n": kibo.str(r, 0), "cat": "n", "t": kibo.int(r, 1),
                          "ic": cell("kibo.png", kibo.int(r, 7)), "lv": TIER_LV[r % 5],
                          "s": {STAT[st]: "%d–%d" % (base, base + spr)}, "me": kibo.int(r, 5),
                          "p": kibo.int(r, 6), "tier": r % 5}
    for r in range(sungbo.rows):                                # Special 301..437
        iid = 301 + r
        s = {STAT[k]: sungbo.int(r, 2 + k) for k in range(4) if sungbo.int(r, 2 + k)}
        items[iid] = {"id": iid, "n": sungbo.str(r, 0), "cat": "s", "t": sungbo.int(r, 1),
                          "ic": cell("sungbo.png", sungbo.int(r, 7)), "lv": sungbo.int(r, 8), "s": s,
                          "me": sungbo.int(r, 6)}
    for r in range(shinki.rows):                                # Rare 501..518
        iid = 501 + r
        s = {STAT[k]: shinki.int(r, 2 + k) for k in range(4) if shinki.int(r, 2 + k)}
        items[iid] = {"id": iid, "n": shinki.str(r, 0), "cat": "r", "t": shinki.int(r, 1),
                          "ic": cell("shinki.png", r), "lv": shinki.int(r, 7), "s": s, "me": 0,
                          "p": shinki.int(r, 6)}   # shinki.png holds the 18 icons in id order
    for iid, it in items.items():
        if iid in SPECIAL_NOTE:
            it["note"] = SPECIAL_NOTE[iid]
    return items


def load_consumables():
    out = []
    for k, name in enumerate(ae.potion_names):
        cid = k + 1
        if cid <= 9:
            e = "%s +%d%%" % (ae.potion_kinds[k // 3], ae.potion_percents[k % 3])
        elif cid == 10:
            e = "Кидок на 60 px, вибух r=35: шкода min(50, 2·рівень героя), відкидає"
        else:
            e = "Кидок на 60 px, вибух r=35: 3 удари по min(30, рівень героя)"
        out.append({"id": cid, "n": name.strip(), "e": e, "p": ae.item_prices[k], "shop": cid in (1, 2, 3, 4, 5, 6, 10, 11),
                        "ic": cell("tool.png", k)})
    return out


def load_recipes():
    b = raw("item-mixing-table.bin")
    n = len(b) // 8
    u = lambda i: b[2 * i] | b[2 * i + 1] << 8                  # noqa: E731
    return [{"a": [u(r), u(n + r), u(2 * n + r)], "r": u(3 * n + r)} for r in range(n)]


# ---- skills --------------------------------------------------------------------------------

# MP = base + (level - 1) * inc;  ae.skill_attack_div: damage bonus ATK*lvl/aU
SKILL_MP = [(5, 3), (6, 4), (7, 5), (10, 3), (15, 4), (7, 3), (10, 3), (10, 5), (8, 3), (9, 4),
            (10, 5), (5, 3), (6, 4), (7, 5), (9, 5), (12, 6), (20, 5), (20, 5), (20, 5)]
SKILL_CAT = ["MOVE", "MOVE", "MOVE", "HEAL", "HEAL", "PASV", "PASV", "PASV", "FWD", "FWD", "FWD",
             "NEAR", "NEAR", "NEAR", "RANGE", "RANGE", "WHOLE", "WHOLE", "WHOLE"]
CAT_UA = {"MOVE": "Ривок", "HEAL": "Лікування", "PASV": "Посилення", "FWD": "Удар уперед",
          "NEAR": "Навколо себе", "RANGE": "Дальній", "WHOLE": "Увесь екран"}
SKILL_EFFECT = [
    "Ривок уперед з ударом, відкидає ціль.",
    "Ривок крізь ворогів, б'є всіх на шляху.",
    "Серія з 4 уколів з кроком уперед, відкидає.",
    "Лікує HP на maxHP·(4+рівень)/25.",
    "Лікує HP на maxHP·(9+рівень)/20.",
    "ATK +ATK·рівень/20 на 50/100/150 тіків (рівні 1–3 / 4–7 / 8–10).",
    "DEF +DEF·рівень/20 на 50/100/150 тіків.",
    "ATK і DEF +рівень/25 від поточних.",
    "Серія ближніх ударів з кроком уперед.",
    "Сильний удар, далеко відкидає ворога.",
    "Удар по всій півплощині попереду в радіусі зброї.",
    "Вогонь навколо себе (r=45), підпалює.",
    "Вогонь навколо себе з відкиданням, підпалює.",
    "Обертовий шквал ударів на 360°.",
    "Блискавка в точку за 60 px попереду (r=35). Зупиняє час.",
    "Ланцюгова блискавка з відкиданням. Зупиняє час.",
    "Ультимейт: б'є всіх ворогів на екрані, зупиняє час.",
    "Ультимейт: вогонь по всьому екрану, підпалює.",
    "Ультимейт: метеоритний дощ по всьому екрану.",
]


def load_skills(text):
    out = []
    for i in range(19):
        base, inc = SKILL_MP[i]
        cat = SKILL_CAT[i]
        bonus = ae.skill_attack_div[i]
        out.append({"id": i + 1, "n": text[i], "d": text[19 + i], "cat": cat, "catn": CAT_UA[cat],
                        "mp1": base, "mp10": base + 9 * inc, "bonus": ("ATK·рівень/%d" % bonus) if bonus else "",
                        "e": SKILL_EFFECT[i], "ic": cell("skill.png", i), "icg": cell("skillgray.png", i)})
    return out


# ---- generals, missions --------------------------------------------------------------------

def load_generals():
    g = Table("general.arr")
    out = {}
    for r in range(g.rows):
        gid = r + 1
        out[gid] = {"id": gid, "n": g.str(r, 0), "head": g.int(r, 1),
                        "wep": "коротка" if (g.int(r, 3) + 1) & 1 else "довга",
                        "sk": [g.int(r, 4 + k) for k in range(4) if g.int(r, 4 + k)],
                        "por": g.int(r, 8), "ty": g.int(r, 9), "atk": g.int(r, 10), "df": g.int(r, 11),
                        "hp": g.int(r, 12)}
    vg = Table("visitgen.arr")
    visit = [vg.int(r, 0) for r in range(vg.rows)]
    for gid in visit:
        if gid in out:
            out[gid]["visit"] = True
    for gen in out.values():
        gen["img"] = portrait(gen["por"]) if gen["por"] else head(gen["head"])
        gen["hd"] = head(gen["head"])
    return out


def brief_text(table, i):
    """brief.scr record i: "N|v1|v2" fills the (..) of record N in order."""
    s = table[i]
    parts = s.split("|")
    if parts[0].isdigit():
        base, vals = table[int(parts[0])], parts[1:]
        out, k, pos = [], 0, 0
        while True:
            a = base.find("(", pos)
            if a < 0:
                out.append(base[pos:])
                break
            b = base.find(")", a)
            out.append(base[pos:a])
            out.append(vals[k] if k < len(vals) else "")
            k += 1
            pos = b + 1
        s = "".join(out)
    else:
        s = s.replace("(", "").replace(")", "")
    return " ".join(s.replace("|", " ").split())


def load_missions(gens, text):
    m = raw("mission.arr")
    side = raw("sideinfo.arr")
    ruler = raw("ruler.arr")
    mdat = strings("mdat_QVGA.scr")
    briefs = strings("brief.scr")
    rulers = {}
    for a in range(1, (len(ruler) - 3) // 15 + 1):
        rec = ruler[3 + (a - 1) * 15:3 + a * 15]
        rulers[a] = {"n": rec[:14].split(b"\0")[0].decode("latin-1").strip(), "por": portrait(rec[14])}
    # - scenarios closed at a new game ("Hidden Mission", opened by an ending)
    hidden = {5, 8, 9, 16, 25, 26, 28, 29, 32, 37}
    scen, missions = [], []
    count = (len(m) - 10) // 38 - 1
    for sid in range(1, count + 1):
        e = 38 * sid + 10
        name = m[e:e + 30].split(b"\0")[0].decode("latin-1").strip()
        nxt = [x for x in m[38 * sid + 40:38 * sid + 46] if x]
        du, dv = s8(m[e + 36]), s8(m[e + 37])
        mp = raw(mdat[sid - 1])
        rooms = (mp[0] // 7) * (mp[1] // 7)
        level = raw("%d.arr" % sid)
        scen.append({"id": sid, "n": name, "next": nxt, "hidden": sid in hidden, "rooms": rooms,
                         "ms": list(range(du, du + dv))})
        for k in range(dv):
            gi = du + k
            r = side[11 * gi + 11:11 * gi + 22]
            soldiers = {201: 0, 202: 0, 203: 0}
            foes = []                                           # (general, level bonus)
            friends = []
            for room in range(rooms):
                q = 20 + 19 * (rooms * k + room)
                for p in range(6):
                    t, c = level[q + 5 + 2 * p], level[q + 6 + 2 * p]
                    if t in soldiers:
                        soldiers[t] += c
                    elif 0 < t < 200 and (t, c) not in foes:
                        foes.append((t, c))
                if level[q + 18] and level[q + 18] not in friends:
                    friends.append(level[q + 18])
            succ, fail = r[5], r[6]
            mis = {"id": gi, "no": gi + 1, "sc": sid, "scn": name, "k": k, "ru": r[0], "rn": rulers[r[0]]["n"],
                       "rp": rulers[r[0]]["por"], "pal": r[3], "boss": r[4], "bl": r[10],
                       "gold": r[7] * 150, "time": r[8],         # only the low byte is read
                       "succ": succ, "fail": fail, "sold": soldiers, "foes": foes, "fr": friends,
                       "brief": brief_text(briefs, gi), "hidden": sid in hidden}
            if succ >= 200:
                mis["end"] = text[38 + succ - 200]
            elif succ:
                mis["talk"] = succ
            if fail >= 200:
                mis["fend"] = text[38 + fail - 200]
            missions.append(mis)
    return scen, missions, rulers


# ---- cross references ----------------------------------------------------------------------

def link_up(items, recipes, gens, missions, skills):
    for it in items.values():
        it["from"], it["use"] = [], []
    for i, rc in enumerate(recipes):
        res = items[rc["r"]]
        lv = res["lv"]
        rc["lv"] = lv
        rc["p"] = round(((200 - lv) // 12 + 1) / 101 * 100, 1)    # aX(): success chance
        res["from"].append(i)
        for a in sorted(set(rc["a"])):
            items[a]["use"].append(i)
    for it in items.values():
        if it["cat"] == "n":
            t = it["tier"]
            rows = []
            for row, lvr in enumerate(DROP_LV_RANGE):
                lo = DROP_TIER[row][t - 1] if t else 0
                pct = DROP_TIER[row][t] - lo
                if pct:
                    rows.append([lvr, pct])
            it["drop"] = rows
    for gen in gens.values():
        gen["boss"], gen["in"], gen["talk"] = [], [], []
    for mis in missions:
        gens[mis["boss"]]["boss"].append(mis["id"])
        for g, lv in mis["foes"]:
            if mis["id"] not in [x[0] for x in gens[g]["in"]]:
                gens[g]["in"].append([mis["id"], lv])
        if "talk" in mis:
            gens[mis["talk"]]["talk"].append(mis["id"])
        for f in mis["fr"]:
            if mis["id"] not in gens[f]["talk"]:
                gens[f]["talk"].append(mis["id"])
    for s in skills:
        s["by"] = [g["id"] for g in gens.values() if s["id"] in g["sk"] and g.get("visit")]
        s["foe"] = [g["id"] for g in gens.values() if s["id"] in g["sk"] and (g["boss"] or g["in"])]


def soldier_table():
    """1038: soldier level L around the hero level Lp, ATK/DEF/HP."""
    base, mult, hpb = [3, 2, 3], [100, 100, 150], [7, 5, 7]

    def lv_range(lp):
        if lp < 21:
            return max(1, lp - 2), lp + 2
        if lp < 41:
            return lp - 3, lp + 5
        return lp - 5, lp + 10

    rows = []
    for lp in (1, 10, 20, 30, 50, 70, 100, 150):
        lo, hi = lv_range(lp)
        row = {"lp": lp, "lv": "%d–%d" % (lo, hi), "u": []}
        for t in range(3):
            f = lambda L, t=t: ((base[t] + L) * mult[t] // 100, L - 1, hpb[t] + 3 * L)   # noqa: E731
            a, b = f(lo), f(hi)
            row["u"].append(["%d–%d" % (a[k], b[k]) for k in range(3)])
        rows.append(row)
    return rows


# ---- page ----------------------------------------------------------------------------------

def main():
    text = strings("text.scr")
    items = load_items()
    cons = load_consumables()
    recipes = load_recipes()
    skills = load_skills(text)
    gens = load_generals()
    scen, missions, rulers = load_missions(gens, text)
    link_up(items, recipes, gens, missions, skills)
    enemies = [
        {"id": 201, "n": "Мечник", "en": "Swords", "ic": soldier("mon1", 0), "mult": 100, "note": "Ходить кімнатою і б'є впритул. З імовірністю 50% замість нього з'являється загін (203)."},
        {"id": 202, "n": "Лучник", "en": "Archers", "ic": soldier("mon2", 0), "mult": 100, "note": "Стоїть на місці (його ставить скрипт карти), стріляє. Не рахується для зачистки кімнати."},
        {"id": 203, "n": "Загін мечників", "en": "Swords", "ic": soldier("mon1", 0), "mult": 150, "note": "Троє мечників як один юніт, ATK ×1.5. За вбивство рахується 3 вороги."},
    ]
    pals = [[soldier("mon1", p), soldier("mon2", p)] for p in range(4)]
    data = {"items": list(items.values()), "cons": cons, "rec": recipes, "skills": skills,
                "gens": list(gens.values()), "scen": scen, "mis": missions, "enemies": enemies, "pals": pals,
                "stable": soldier_table(), "types": TYPE, "img": IMG,
                "rulers": dict(rulers.items())}
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = (PY / "tools" / "encyclopedia_template.html").read_text(encoding="utf-8")
    page = page.replace("/*DATA*/null", blob)
    OUT.write_text(page, encoding="utf-8")
    print("encyclopedia -> %s (%d KB): %d items, %d consumables, %d recipes, %d skills, "
          "%d generals, %d missions" % (OUT, OUT.stat().st_size // 1024, len(items), len(cons),
                                        len(recipes), len(skills), len(gens), len(missions)))


if __name__ == "__main__":
    main()
