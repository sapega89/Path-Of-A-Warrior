#!/usr/bin/env python3
"""Reference parser for Path of a Warrior *.SP3 sprite-frame tables.

Format (reversed from ag.K(int), ag.java 3467-3482):
    u8   n                      number of frames
    n x  6 x int16 little-endian (ag.a(byte,byte), ag.java 1275-1277)
         a = src_x, b = src_y   (top-left of region inside the PNG atlas)
         c = w,     d = h       (region size)
         e = anchor_x, f = anchor_y  (pivot; dest_top_left = entity_pos - (e, f))
Draw call (c.java 306, 485-486, ar.java 1939):
    b(img, X - e, Y - f, c, d, a, b)   -> blit img[a:a+c, b:b+d] at (X-e, Y-f)
"Whole-image" effects (c.java 242-251): PNG chosen per frame through a byte table
    (value v -> imgeff.scr[v-27], 0 = draw nothing), whole PNG drawn at (X-e, Y-f);
    a,b are ignored, c,d are only used for the dirty-rect.

Usage: python3 -I pow_sp3.py /path/to/pow
"""
import os
import struct
import sys

END, BLANK = 222, 180          # animation terminator / invisible frame (ae.java)


def parse_sp3(path):
    data = open(path, 'rb').read()
    n = data[0]
    if len(data) != 1 + 12 * n:
        raise ValueError('%s: size %d != 1+12*%d' % (path, len(data), n))
    frames = []
    for i in range(n):
        a, b, c, d, e, f = struct.unpack_from('<6h', data, 1 + 12 * i)
        frames.append(dict(src=(a, b, c, d), anchor=(e, f)))
    return frames


def load_scr(path):
    """al.java: u16 count, u16 offsets[count+1] (LE), UTF-8 slices."""
    d = open(path, 'rb').read()
    cnt = d[0] | d[1] << 8
    out = []
    for i in range(cnt):
        j = d[2 + 2 * i] | d[3 + 2 * i] << 8
        k = d[4 + 2 * i] | d[5 + 2 * i] << 8
        out.append(d[j:k].decode('utf-8', 'replace'))
    return out


# --- animation tables copied verbatim from ae.java (lines 31-147) -------------
B = [[1], [4], [7], [10]]
C = [[0, 1, 2, 1], [3, 4, 5, 4], [6, 7, 8, 7], [9, 10, 11, 10]]
D = [[41] * 3, [42] * 3, [43] * 3, [44] * 3]
E = [[36] * 6 + [1], [37] * 6 + [4], [38] * 6 + [7], [39] * 6 + [10]]
F = [[12, 13], [18, 19], [24, 25], [30, 31]]
G = [[14, 15], [20, 21], [26, 27], [32, 33]]
H = [[16, 17], [22, 23], [28, 29], [34, 35]]
I = [[12, 13, 13], [18, 19, 19], [24, 25, 25], [30, 31, 31]]
J = [[14, 15, 15], [20, 21, 21], [26, 27, 27], [32, 33, 33]]
K = [[16, 17, 17], [22, 23, 23], [28, 29, 29], [34, 35, 35]]
L = [36] * 10 + [40] * 4
M = [[45] + [46] * 4, [47] + [48] * 4, [49] + [50] * 4, [51] + [52] * 4]
N = [[0, 1, 2, 3, 3, 3, 4], [5, 6, 7, 8, 8, 8, 9], [10, 11, 12, 13, 13, 13, 14], [15, 16, 17, 18, 18, 18, 19]]
O = [[20, 21, 22, 23, 24, 25, 25, 25, 26], [27, 28, 29, 30, 31, 32, 32, 32, 33],
     [34, 35, 36, 37, 38, 39, 39, 39, 40], [41, 42, 43, 44, 45, 46, 46, 46, 47]]
P = [[48, 49, 50, 49, 50, 49, 50, 49, 50, 51], [52, 53, 54, 53, 54, 53, 54, 53, 54, 55],
     [56, 57, 58, 57, 58, 57, 58, 57, 58, 59], [60, 61, 62, 61, 62, 61, 62, 61, 62, 63]]
Q = [64, 65, 66] + [67] * 10
R = [[68, 69, 70, 71] * 3, [72, 73, 74, 75] * 3, [76, 77, 78, 79] * 3, [80, 81, 82, 83] * 3]
S = [[84, 85, 86, 87, 88, 89, 89, 89], [90, 91, 92, 93, 94, 95, 95, 95],
     [96, 97, 98, 99, 100, 101, 101, 101], [102, 103, 104, 105, 106, 107, 107, 107]]
T = [[108, 109, 110, 111, 112, 113, 114, 115, 115, 115], [116, 117, 118, 119, 120, 121, 122, 123, 123, 123],
     [124, 125, 126, 127, 128, 129, 130, 131, 131, 131], [132, 133, 134, 135, 136, 137, 138, 139, 139, 139]]
U = [140, 141, 142, 143, 144, 145, 146, 145, 146, 145, 146]
V = [[147, 148, 149, 150, 151, 152, 153, 154], [149, 150, 151, 152, 153, 154, 147, 148],
     [151, 152, 153, 154, 147, 148, 149, 150], [153, 154, 147, 148, 149, 150, 151, 152]]
W = [[48, 49] + [50] * 7 + [51], [52, 53] + [54] * 7 + [55], [56, 57] + [58] * 7 + [59],
     [60, 61] + [62] * 6 + [59, 63]]
X = [64, 65, 66] + [67] * 20
Y = [155, 156, 157, 158, 159, 160] + [161] * 17
Z = [64, 65, 66] + [67] * 13
aa = [[0, 0, 1, 1], [2, 2, 3, 3], [4, 4, 5, 5], [6, 6, 7, 7]]
ab = [[8], [9], [10], [11]]
ac = [[12] * 7, [13] * 7, [14] * 7, [15] * 7]
ad = [[12, 12, 180, 12, 12, 180, 12], [13, 13, 180, 13, 13, 180, 13], [14, 14, 180, 14, 14, 180, 14], [15, 15, 180, 15, 15, 180, 15]]
ae_ = [[0], [2], [4], [6]]
af = [[1], [3], [5], [7]]
ag = [[8] * 7, [9] * 7, [10] * 7, [11] * 7]
ah = [[8, 8, 180, 8, 8, 180, 8], [9, 9, 180, 9, 9, 180, 9], [10, 10, 180, 10, 10, 180, 10], [11, 11, 180, 11, 11, 180, 11]]
ai = [[8, 9], [10, 11], [12, 13], [14, 15]]
aj = [[16] * 7, [17] * 7, [18] * 7, [19] * 7]
ak = [20, 20, 180, 180, 20, 20, 180, 180, 20, 20]
aT = [0, 1, 1, 1, 2, 3, 3, 3]          # 8 move dirs -> 4 sprite dirs (down,left,up,right)


def per_dir(t):
    """table either [4][...] (per sprite dir) or flat (same for all dirs)."""
    return t if isinstance(t[0], list) else [t] * 4


# player: cz.ab[anim] (ag.java 2069-2099); anims 0..11 -> normal SP3, 12..30 -> *_sk.SP3
PLAYER_ANIMS = [B, C, D, F, G, H, I, J, K, E, L, M,           # 0..11
                N, O, P, Q, Q, Q, Q, Q, R, S, T, U, U, V, W, W, X, Y, Z]  # 12..30
# generals: eH[f] (ag.java 2041-2062); f 0..5 -> 21-frame g_*.SP3, f 6..21 -> *_sk.SP3
GENERAL_ANIMS = [aa, ai, aj, ak, ai, ai, N, O, P, Q, Q, Q, Q, Q, R, S, T, U, U, V, W, W]
SOLDIER_ANIMS = [aa, ab, ac, ad]      # eF: mon1 (types 201/203)
ARCHER_ANIMS = [ae_, af, ag, ah]      # eG: mon2 (type 202)

# SP3 -> PNG atlas (from ag.y() 945-959, ag.aA() 3459-3465, c.b() 996-1005, ag.A() 973-988)
ATLAS = {
    'char_body': 'char_body', 'char_body_sk': 'char_body',
    'g_body': 'char_body', 'g_body_sk': 'char_body',          # generals reuse the hero body PNG
    'wep_long': 'wep_long', 'wep_long_sk': 'wep_long', 'wep_long_g': 'wep_long', 'wep_long_g_sk': 'wep_long',
    'wep_short': 'wep_short', 'wep_short_sk': 'wep_short', 'wep_short_g': 'wep_short', 'wep_short_g_sk': 'wep_short',
    'mon1': 'mon1', 'mon2': 'mon2', 'sword': 'sword',
    'effect0': 'effect0', 'effect1': 'effect1', 'effect_light': 'effect_light',
}
for i in range(1, 5):
    ATLAS['char_head%d' % i] = ATLAS['char_head%d_sk' % i] = 'char_head%d' % i
for i in range(1, 7):
    ATLAS['g_head%d' % i] = ATLAS['g_head%d_sk' % i] = 'g_head%d' % i

# whole-image effects: SP3 -> per-frame image byte table (ae.java 151-186); v-27 -> imgeff.scr index
FX_TABLES = {
    'effect2': [31, 32, 30, 31, 32, 30, 31, 32, 30],
    'effect3': [33, 34, 35, 36, 37, 38],
    'effect4': [40, 39],
    'effect6': [41, 42, 43, 44, 43, 44, 43, 44, 45, 41],
    'effect7': [46, 47],
    'effect8': [48, 49, 52, 0, 52, 0, 52, 50, 51, 52, 0, 52, 0, 52, 48, 49, 52, 0, 52, 0, 52, 50, 50, 52, 0, 52, 0, 52],
    'effect9': [53, 54, 54, 54, 54, 54, 53, 53, 53, 53],
    'effect10': [55, 56, 55, 56, 55, 56, 55, 55, 55, 56, 56, 56, 56, 56, 56, 56, 57, 0, 56, 57, 0, 57, 56, 0, 57, 56,
                 57, 56, 57, 56, 57, 56, 57, 56, 57, 56, 57, 56, 57, 56, 57, 56],
    'effect11': [0, 58, 59, 60, 0, 0, 61, 69, 62, 0, 61, 69, 62, 69, 70],
    'effect12': [65] * 15 + [63] * 5 + [64] * 5,
    'effect13': [66, 68, 67, 66] * 4,
}


def check_anims(name, anims, nframes):
    bad = []
    for ai_, t in enumerate(anims):
        for d, seq in enumerate(per_dir(t)):
            for fr in seq:
                if fr in (BLANK, END):
                    continue
                if not 0 <= fr < nframes:
                    bad.append((ai_, d, fr))
    print('  %-34s frames=%3d  referenced max=%3d  out-of-range=%s' % (
        name, nframes, max(fr for t in anims for s in per_dir(t) for fr in s if fr not in (BLANK, END)), bad or 'none'))
    return not bad


def main(root):
    sp3 = {os.path.basename(p)[:-4]: parse_sp3(os.path.join(root, p))
           for p in sorted(os.listdir(root)) if p.endswith('.SP3')}
    print('Parsed %d SP3 files (all sizes == 1 + 12*n)' % len(sp3))
    for name, fr in sp3.items():
        w = max(f['src'][0] + f['src'][2] for f in fr)
        h = max(f['src'][1] + f['src'][3] for f in fr)
        print('  %-16s n=%3d  atlas>=%3dx%-3d  png=%s' % (name, len(fr), w, h, ATLAS.get(name, '<per-frame table>')))

    print('\nCross-check: every frame referenced by ae.java animation tables exists in its SP3')
    ok = True
    ok &= check_anims('player anims 0..11  vs char_body', PLAYER_ANIMS[:12], len(sp3['char_body']))
    ok &= check_anims('player anims 12..30 vs char_body_sk', PLAYER_ANIMS[12:], len(sp3['char_body_sk']))
    ok &= check_anims('general f 0..5  vs g_body', GENERAL_ANIMS[:6], len(sp3['g_body']))
    ok &= check_anims('general f 6..21 vs g_body_sk', GENERAL_ANIMS[6:], len(sp3['g_body_sk']))
    ok &= check_anims('soldier eF vs mon1', SOLDIER_ANIMS, len(sp3['mon1']))
    ok &= check_anims('archer eG vs mon2', ARCHER_ANIMS, len(sp3['mon2']))
    # parallel layers must have identical frame counts
    for grp in (['char_body', 'char_head1', 'char_head2', 'char_head3', 'char_head4', 'wep_long', 'wep_short'],
                ['char_body_sk'] + ['char_head%d_sk' % i for i in range(1, 5)] + ['wep_long_sk', 'wep_short_sk'],
                ['g_body'] + ['g_head%d' % i for i in range(1, 7)] + ['wep_long_g', 'wep_short_g'],
                ['g_body_sk'] + ['g_head%d_sk' % i for i in range(1, 7)] + ['wep_long_g_sk', 'wep_short_g_sk']):
        counts = {g: len(sp3[g]) for g in grp}
        same = len(set(counts.values())) == 1
        ok &= same
        print('  layer group %-14s counts=%s  %s' % (grp[0], sorted(set(counts.values())), 'OK' if same else 'MISMATCH'))

    imgeff = load_scr(os.path.join(root, 'imgeff.scr'))
    print('\nWhole-image effects: SP3 frame count vs byte-table length, PNGs used')
    for name, tbl in FX_TABLES.items():
        pngs = sorted({imgeff[v - 27] for v in tbl if v})
        print('  %-9s frames=%3d table=%3d  pngs=%s' % (name, len(sp3[name]), len(tbl), pngs))
    print('\nRESULT:', 'ALL CHECKS PASSED' if ok else 'FAILURES')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
