#!/usr/bin/env python3
"""Reference parser for Path of a Warrior map data (N.MAP, N.arr, *.scr string tables).
Usage: python3 -I powmap.py <data_dir> [map_id]
"""
import sys, os

TILE = 27          # px
ROOM = 7           # tiles per room side (interior)

# ---------- .scr string table (al.java) ----------
def read_scr(path):
    d = open(path, 'rb').read()
    out, idx = [], 0
    while True:
        i = 2 + idx * 2                        # al.a(): i = 2 + index*2 (entries overlap: end(i) == start(i+1))
        if i + 4 > len(d):
            break
        start = d[i] | d[i + 1] << 8           # little-endian u16
        end = d[i + 2] | d[i + 3] << 8
        if start >= end or end > len(d):
            break
        out.append(d[start:end].decode('utf-8', 'replace'))   # Java modified UTF-8 (ASCII here)
        idx += 1
    return out

# ---------- tile id -> PNG name (c.java 1293-1298) ----------
def tile_png(tile_id, imgtile):
    """tile_id is 1-based (0 = empty). group = (id-1)>>4 selects imgtile.scr entry, frame = (id-1)&15."""
    g, f = (tile_id - 1) >> 4, (tile_id - 1) & 15
    return f"{imgtile[g]}_{f + 1:02d}.png"

# ---------- N.MAP (c.b(int), c.java 1128-1167) ----------
def parse_map(path):
    d = open(path, 'rb').read()
    W, H, P = d[0], d[1], d[2]
    palette = list(d[3:3 + P])                 # sorted distinct tile ids used (incl. 0, and obj+1); not read by the game
    o = 3 + P
    n = W * H
    names = ('ground', 'overlay', 'object', 'attr')
    layers = {nm: d[o + k * n:o + (k + 1) * n] for k, nm in enumerate(names)}
    i = o + 4 * n
    events = []
    if len(d) > i:                             # optional event block
        count = d[i]
        total = d[i + 1] | d[i + 2] << 8       # skipped by the game ("i += 2"); == sum(4+len) of records
        i += 3
        for _ in range(count):
            x, y = d[i], d[i + 1]
            ln = d[i + 2] | d[i + 3] << 8
            body = d[i + 4:i + 4 + ln]
            cmds = [tuple(body[k:k + 3]) for k in range(0, ln, 3)]   # opcode 0 is the only one: (0, mission_no(1-based), npc_type-200)
            events.append(dict(x=x, y=y, cmds=cmds))
            i += 4 + ln
    assert i == len(d), (path, i, len(d))
    return dict(W=W, H=H, palette=palette, events=events, **layers)

# ---------- N.arr (c.a(int), c.java 1089-1116) ----------
ROOM_FIELDS = ('exit_down', 'exit_left', 'exit_up', 'exit_right', 'max_alive',
               'spawn')            # spawn = 6 (type,param) pairs at bytes 5..16; byte 17 unused; byte 18 = event general id
def parse_arr(path, W, H):
    d = open(path, 'rb').read()
    header = d[:20]                            # [19, 1 x 19]  (field count + field widths) - skipped by the game
    rooms_per_mission = (W // ROOM) * (H // ROOM)      # NOTE: decompiled "W/7*H/7" must be read as (W/7)*(H/7)
    rec = 19
    nmis = (len(d) - 20) // (rooms_per_mission * rec)
    assert 20 + nmis * rooms_per_mission * rec == len(d)
    missions = []
    for m in range(nmis):
        rooms = []
        for r in range(rooms_per_mission):
            b = d[20 + (m * rooms_per_mission + r) * rec:][:rec]
            pairs = [(b[5 + 2 * k], b[6 + 2 * k]) for k in range(6)]
            rooms.append(dict(exits=list(b[0:4]),   # [down,left,up,right]
                              max_alive=b[4],
                              spawns=[p for p in pairs if p[0]],   # type>=200: soldier type x count; type<200: general id, level bonus
                              unused17=b[17],
                              event_general=b[18]))
        missions.append(rooms)
    return dict(header=list(header), missions=missions, rooms_per_mission=rooms_per_mission)

# ---------- mission start tiles (sideinfo.arr via mission.arr; e.java bi() 3569-3603, ag.C() 1043-1062) ----------
def missions_for_area(data_dir, area_id):
    m = open(os.path.join(data_dir, 'mission.arr'), 'rb').read()
    s = open(os.path.join(data_dir, 'sideinfo.arr'), 'rb').read()
    o = 38 * area_id + 10
    name = m[o:o + 30].split(b'\0')[0].decode('latin1')
    du, dv = m[o + 36], m[o + 37]
    out = []
    for k in range(dv):
        r = s[11 * (du + k) + 11:][:11]
        out.append(dict(ruler=r[0], start=(r[1], r[2]), recolor=r[3], target_general=r[4],
                        on_success=r[5], on_fail=r[6], gold_mul=r[7], par_time=r[8], level_bonus=r[10]))
    return name, out

def ascii_map(mp, starts=(), events=()):
    W, H = mp['W'], mp['H']
    rows = []
    for y in range(H):
        line = []
        for x in range(W):
            k = y * W + x
            a, ob = mp['attr'][k], mp['object'][k]
            ch = '#' if a & 1 else ('^' if a & 2 else '.')
            if ob:
                ch = 'o'
            if (x, y) in events:
                ch = 'A'
            if (x, y) in starts:
                ch = 'S'
            line.append(ch)
        rows.append(''.join(line))
    return rows

if __name__ == '__main__':
    D = sys.argv[1]
    imgtile = read_scr(os.path.join(D, 'imgtile.scr'))
    mdat = read_scr(os.path.join(D, 'mdat_QVGA.scr'))
    edat = read_scr(os.path.join(D, 'edat.scr'))
    print('imgtile.scr:', imgtile)
    print('mdat_QVGA.scr[0..44] maps:', mdat[0], '...', mdat[44], '| [45..] =', mdat[45:48], '...')
    print('edat.scr[0..44] arr:', edat[0], '...', edat[44])
    allused = {}
    for mid in range(1, 46):
        mp = parse_map(os.path.join(D, mdat[mid - 1]))
        ar = parse_arr(os.path.join(D, edat[mid - 1]), mp['W'], mp['H'])
        name, mis = missions_for_area(D, mid)
        assert len(mis) == len(ar['missions'])
        for lay in ('ground', 'overlay', 'object'):
            for t in set(mp[lay]):
                if t:
                    allused.setdefault(lay, set()).add(t)
                    if lay == 'object':
                        allused[lay].add(t + 1)
        print(f"map {mid:2d} {name!r:18} {mp['W']:2d}x{mp['H']:<2d} rooms {mp['W']//7}x{mp['H']//7} "
              f"missions={len(ar['missions'])} events={len(mp['events'])}")
    for lay, s in allused.items():
        print(lay, 'tile ids:', len(s), 'range', min(s), '-', max(s), 'pngs e.g.', [tile_png(t, imgtile) for t in sorted(s)[:3]])
    sel = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    mp = parse_map(os.path.join(D, f'{sel}.MAP'))
    name, mis = missions_for_area(D, sel)
    starts = {m['start'] for m in mis}
    evs = {(e['x'], e['y']) for e in mp['events']}
    print(f'\n{sel}.MAP  {mp["W"]}x{mp["H"]}  legend: # solid(attr&1)  ^ foreground(attr&2)  o object  A archer-event  S mission start  . floor')
    for y, row in enumerate(ascii_map(mp, starts, evs)):
        sep = '-' if y % 7 == 0 else ' '
        print(f'{y:2d} {row}')
    print('events:', mp['events'])
    print('missions:', mis)
    ar = parse_arr(os.path.join(D, f'{sel}.arr'), mp['W'], mp['H'])
    for mi, rooms in enumerate(ar['missions']):
        print(f'mission {mi}:', [(r['exits'], r['spawns'], r['event_general']) for r in rooms])
