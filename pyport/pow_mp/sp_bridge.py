"""Bridge to the single-player save (PHASE_9 task 9.10), on the client side.

The original: POW single, Gamevil Live > Management > Save User Data, sent the hero to the
server (as.java:475-528, opcode 256), and the multiplayer server played with that hero.
Gamevil Live of the single-player port is not there yet (phase 7), so the multiplayer client
reads the hero itself from the single-player save on the same computer / in the same browser
(RMS "gamevil_pow_data", one 965-byte record written by ag.java) and sends it with every login
(262, PORT-EXTRA). The gold, fame and experience of a won or lost battle (1032) go back into
that save at once.

Offsets follow ag.U() (ag.java:2126-2215): little-endian, after the 2-byte record length,
char[16] name, u8 at 18, then the fields in reading order.
"""
import struct

import config

SAVE_STORE = "gamevil_pow_data"
SAVE_LEN = 965

# offsets in the record (see the module docstring)
OFF_LEVEL = 471          # cz.l   u8
OFF_ATK = 472            # cz.m   s16 base ATK
OFF_DEF = 474            # cz.n   s16 base DEF
OFF_HP = 476             # cz.o   s16 max HP
OFF_MP = 480             # cz.q   s16 max MP
OFF_GOLD = 484           # cz.E   s32
OFF_FAME = 488           # cz.F   s32
OFF_EXP = 492            # cz.G   s32 (exp into the current level; ag.H levels up from it)
OFF_SLOTS = 501          # cz.V[5] u8: assigned skills, index + 12 (as.java:500-505)
OFF_SKILLS = 506         # cz.W[19] u8: skill levels by index
OFF_ITEMS = 525          # cz.X[9]: z {s16 id, s16 atk, s16 def, s16 hp, s16 mp, u8}
OFF_DY = 38              # ag.dy[8] s32: mission progress bits
OFF_FACE = 916           # cz.aB  u8: hero 0..3
OFF_BACKPACK = 624       # cz.Y[25]: z like X[] (analysis/03 §4.2)
OFF_BELT = 899           # cz.Z[5]: {u16 id, u8 count <= 5}, consumables 1..11
# PORT-EXTRA config.BACKPACK_SIZE: the cells past 25 follow the record as {u8 'B', u8 n, n x z}
# (GameCanvas.write_backpack_extra)
BACKPACK_EXTRA_MARK = 0x42
PENDING_STORE = "pow_mp_loot"   # loot that found the backpack full, delivered later

# PORT-EXTRA: a part of the single player (main.py): the rewards of 1032 are not written into
# the save (the hero is in memory there) but kept here for Live.after_multiplayer
embedded = False
pending = []                    # [{"gold", "fame", "exp", "loot": [(id, atk, def, hp, mp)]}]


def keep_rewards(gold, fame, exp, item=None):
    pending.append({"gold": gold, "fame": fame, "exp": exp, "loot": [item] if item else []})


def take_rewards():
    """What the battles earned since the last call (main.py, after the screens)."""
    out, pending[:] = list(pending), []
    return out

# as.gG (as.java:84-86): SP skill index -> skill code; MP knows codes 3..13
SKILL_CODES = (3, 4, 5, 9, 10, 11, 12, 13, 6, 7, 8, 14, 15, 16, 17, 18, 19, 20, 21)
MP_SKILLS = tuple(range(3, 14))


def read_save():
    """The raw single-player save, or None when there is none."""
    try:
        from pow.midp.rms import RecordStore
        rs = RecordStore.openRecordStore(SAVE_STORE, False)
        if rs is None or rs.getNumRecords() < 1:
            return None
        data = bytes(b & 0xFF for b in rs.getRecord(1))
    except Exception:
        return None
    if len(data) < SAVE_LEN or (data[0] | data[1] << 8) == 0:
        return None
    return data


def _s16(d, off):
    return struct.unpack_from("<h", d, off)[0]


def weapon_type(item_id):
    """ag.g(id) ^ 1 (as.java:479): 0 long, 1 short. ag.g = 1 below 100 (the starting sword),
    else the item's class byte (e.java:3465-3480; kibo.arr: 0 for ids 101-115 Blades/Pikes,
    1 for 116-130 Claymores/Swords/Axes)."""
    return 1 if 101 <= item_id <= 115 else 0


def hero(data):
    """The fields of 256 the multiplayer server uses, from a raw save (None -> None)."""
    if data is None:
        return None
    items = []
    for i in range(9):
        o = OFF_ITEMS + 11 * i
        items.append(struct.unpack_from("<hhhhhB", data, o))
    bonus = [sum(it[k] for it in items if it[0] != 0) for k in (1, 2, 3, 4)]   # ag.O()
    skills = [0] * len(MP_SKILLS)
    for idx in range(19):
        lvl = data[OFF_SKILLS + idx]
        code = SKILL_CODES[idx]
        if lvl > 0 and code in MP_SKILLS:
            skills[code - 3] = lvl
    slots = []
    for i in range(5):
        v = data[OFF_SLOTS + i]
        if v >= 12 and SKILL_CODES[v - 12] in MP_SKILLS and len(slots) < 4:
            slots.append(SKILL_CODES[v - 12])
    progress = sum(struct.unpack_from("<I", data, OFF_DY + 4 * i)[0].bit_count() for i in range(8))
    return {
        "level": data[OFF_LEVEL], "hp": _s16(data, OFF_HP), "mp": _s16(data, OFF_MP),
        "atk": _s16(data, OFF_ATK), "def": _s16(data, OFF_DEF),
        "atk_bonus": bonus[0], "def_bonus": bonus[1], "hp_bonus": bonus[2], "mp_bonus": bonus[3],
        "face": data[OFF_FACE] & 3, "weapon": weapon_type(items[0][0]), "skills": skills,
        "slots": slots + [99] * (4 - len(slots)), "progress": min(255, progress),
    }


def add_rewards(gold, fame, exp):
    """1032: put what the battle earned into the single-player save (gold -> cz.E, fame -> cz.F,
    exp -> cz.G; the single player levels up from cz.G the next time it gains exp, ag.H)."""
    try:
        from pow.midp.rms import RecordStore
        rs = RecordStore.openRecordStore(SAVE_STORE, False)
        if rs is None or rs.getNumRecords() < 1:
            return False
        data = bytearray(b & 0xFF for b in rs.getRecord(1))
        if len(data) < SAVE_LEN:
            return False
        for off, add in ((OFF_GOLD, gold), (OFF_FAME, fame), (OFF_EXP, exp)):
            v = struct.unpack_from("<i", data, off)[0]
            struct.pack_into("<i", data, off, max(0, min(0x7FFFFFFF, v + add)))
        rs.setRecord(1, data, 0, len(data))
        return True
    except Exception:
        return False


def _put_item(data, item):
    """ag.k(id, ...) (ag.java:3286-3360): a consumable stacks on the belt (5 at most), the rest
    takes the first free backpack cell. False when there is no room."""
    iid = item[0]
    if iid < 100:
        free = None
        for i in range(5):
            o = OFF_BELT + 3 * i
            sid, cnt = struct.unpack_from("<hB", data, o)
            if sid == iid and cnt < 5:
                struct.pack_into("<hB", data, o, iid, cnt + 1)
                return True
            if sid == 0 and free is None:
                free = o
        if free is None:
            return False
        struct.pack_into("<hB", data, free, iid, 1)
        return True
    for o in _backpack_offsets(data):
        if struct.unpack_from("<h", data, o)[0] == 0:
            struct.pack_into("<hhhhhB", data, o, *item[:5], 0)
            return True
    return False


def _backpack_offsets(data):
    """Offsets of every backpack cell in the record: the original 25, then the extra block. A
    record without the block (an old save) gets an empty one, so loot can use those cells too."""
    offs = [OFF_BACKPACK + 11 * i for i in range(25)]
    extra = config.BACKPACK_SIZE - 25
    if extra <= 0:
        return offs
    end = data[0] | data[1] << 8
    if end == SAVE_LEN:
        need = SAVE_LEN + 2 + 11 * extra
        if len(data) < need:
            data.extend(bytes(need - len(data)))
        data[SAVE_LEN], data[SAVE_LEN + 1] = BACKPACK_EXTRA_MARK, extra
        data[SAVE_LEN + 2:need] = bytes(11 * extra)
        data[0], data[1] = need & 0xFF, need >> 8 & 0xFF
        end = need
    if end >= SAVE_LEN + 2 and data[SAVE_LEN] == BACKPACK_EXTRA_MARK:
        for i in range(min(data[SAVE_LEN + 1], extra)):
            o = SAVE_LEN + 2 + 11 * i
            if o + 11 <= end:
                offs.append(o)
    return offs


def _pending():
    from pow.midp.rms import RecordStore
    rs = RecordStore.openRecordStore(PENDING_STORE, True)
    if rs.getNumRecords() < 1:
        rs.addRecord(bytearray(), 0, 0)
    raw = bytes(b & 0xFF for b in (rs.getRecord(1) or b""))
    return rs, [struct.unpack_from("<Hhhhh", raw, o) for o in range(0, len(raw) - 9, 10)]


def add_item(item_id=0, atk=0, def_=0, hp=0, mp=0):
    """1032 loot: into the single-player backpack (or belt); a full backpack keeps it waiting
    in our own store until there is room (the next battle or login tries again). Returns the
    number of items still waiting, or None without a single-player save."""
    try:
        from pow.midp.rms import RecordStore
        rs = RecordStore.openRecordStore(SAVE_STORE, False)
        if rs is None or rs.getNumRecords() < 1:
            return None
        data = bytearray(b & 0xFF for b in rs.getRecord(1))
        if len(data) < SAVE_LEN:
            return None
        prs, waiting = _pending()
        if item_id:
            waiting.append((item_id, atk, def_, hp, mp))
        left = [it for it in waiting if not _put_item(data, it)]
        if len(left) != len(waiting):
            rs.setRecord(1, data, 0, len(data))
        raw = bytearray(b"".join(struct.pack("<Hhhhh", *it) for it in left))
        prs.setRecord(1, raw, 0, len(raw))
        return len(left)
    except Exception:
        return None
