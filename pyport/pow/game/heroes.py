"""PORT-EXTRA: the hero roster, 4 heroes of the original + 6 heroes made of the generals' art.

The original has 4 heroes (cz.aB = 0..3): portrait ju_1..ju_4 (imgchar 38..41), upper body
char_head1..4 (imgchar 46..49) with the frame tables char_headN.SP3 (mdat 47..50, 53 frames
for the map: walk, attack, dash, throw...) and char_headN_sk.SP3 (mdat 51..54, 162 frames for
the skills). The legs (char_body, the same picture as g_body) are common to all of them.

Heroes 4..9 use the upper bodies of the generals, g_head1..6 (imgchar 50..55), and the
portraits of generals that wear them (jang_N, the same 46x46 as ju_N). No new picture is
added. The generals' tables are shorter: g_headN.SP3 has 21 map frames (no dash, no throw,
two frames per walk instead of three); g_headN_sk.SP3 has the full 162 skill frames, but some
of the generals' skill poses stand on other legs than the hero's. So the hero's frame tables
are built here (head_frames), frame by frame:

1. the general's frame with the same legs (same rectangle of char_body / g_body) and its
   upper body, moved by the difference of the legs' offsets - exactly as the general looks;
2. otherwise (the hero's own poses: the walk's middle step, the third attack frame, dash,
   throw, some skill poses) the general's upper body from FALLBACK, a hand-made table "hero's
   upper body picture -> general's frame with the closest pose"; it is put where the hero's
   own upper body was, aligned by the bottom middle (the waist on the legs).

The 4 heroes of the original use their own pictures and tables unchanged.
"""

HERO_COUNT = 10        # cz.aB = 0..9 (the original: 0..3)
ORIG_HEROES = 4

# heroes 4..9: (g_headN, portrait jang_N, name of the general who wears it in general.arr)
# The portraits are the generals' own (general.arr: head byte 11, face byte 18).
GENERAL_HEROES = [
    (1, 1, "Augustine"),
    (2, 2, "Reeve"),
    (3, 17, "Melbourne"),
    (4, 4, "Lord Aldred"),
    (5, 3, "Kirkland"),
    (6, 6, "Charlton"),
]

# mdat_QVGA.scr (ag.bF) indices of the frame tables
_MDAT_CHAR_BODY = 45, 46          # char_body.SP3, char_body_sk.SP3
_MDAT_CHAR_HEAD = 47, 51          # + aB: char_headN.SP3, char_headN_sk.SP3 (hero 1)
_MDAT_G_BODY = 68, 69             # g_body.SP3, g_body_sk.SP3
_MDAT_G_HEAD = 70, 76             # + N - 1: g_headN.SP3, g_headN_sk.SP3

# Frame mapping table for the poses the generals do not have. Key: the rectangle of the
# hero's upper body picture in char_head1..4.png (x, y, w, h), the same in all 4 heroes.
# Value: (table, frame) of the general whose upper body is taken: table 0 = g_headN.SP3
# (map frames 0..20), 1 = g_headN_sk.SP3 (skill frames 0..161).
# General's map frames: 0-1 walk down, 2-3 walk right, 4-5 walk up, 6-7 walk left,
# 8-9 attack down, 10-11 attack right, 12-13 attack up, 14-15 attack left, 16-19 hit, 20 down.
FALLBACK = {
    (102, 0, 24, 27): (0, 0),     # walk down, middle step          -> walk down
    (168, 0, 18, 27): (0, 2),     # walk right, middle step         -> walk right
    (28, 0, 26, 27): (0, 4),      # walk up, middle step            -> walk up
    (226, 0, 18, 27): (0, 6),     # walk left, middle step          -> walk left
    (82, 27, 31, 26): (0, 9),     # attack down, 3rd frame / throw  -> attack down
    (218, 57, 25, 23): (0, 11),   # attack right, 3rd frame / dash  -> attack right
    (243, 57, 21, 27): (0, 10),   # attack right, recoil / throw    -> attack right, swing
    (179, 27, 23, 24): (0, 13),   # attack up, 3rd frame / dash     -> attack up
    (202, 27, 34, 26): (0, 13),   # attack up, recoil / throw       -> attack up
    (86, 57, 27, 27): (0, 15),    # attack left, 3rd frame / dash   -> attack left
    (113, 57, 26, 23): (0, 15),   # attack left, recoil / throw     -> attack left
    (28, 57, 23, 24): (0, 15),    # attack left (skill legs)        -> attack left
    (320, 27, 22, 39): (1, 143),  # both arms up (skill)            -> the same frame of the general
}

_cache = {}


def is_general(aB):
    return aB >= ORIG_HEROES


def head_number(aB):
    """1..6 = g_headN of a general hero."""
    return GENERAL_HEROES[aB - ORIG_HEROES][0]


def portrait_index(aB):
    """imgchar.scr (ag.bB) index of the 46x46 portrait: ju_1..4 (38..41) or jang_N (N)."""
    if is_general(aB):
        return GENERAL_HEROES[aB - ORIG_HEROES][1]
    return 38 + aB


def head_image_index(aB):
    """imgchar.scr index of the upper body picture: char_head1..4 (46..49) or g_head1..6 (50..55)."""
    if is_general(aB):
        return 50 + head_number(aB) - 1
    return 46 + aB


def _rect(r):
    return r.a, r.b, r.c, r.d


def _copy(src, e, f):
    from pow.game.structs import y
    r = y()
    r.a, r.b, r.c, r.d, r.e, r.f = src.a, src.b, src.c, src.d, e, f
    return r


def build_head_frames(K_I, n, sk):
    """Frame table of the upper body g_head<n> for the hero's legs (char_body).
    K_I(index) reads an mdat_QVGA frame table (ag.K_I). sk: 0 = map table, 1 = skill table."""
    cb = K_I(_MDAT_CHAR_BODY[sk])          # the hero's legs, frame by frame
    ch = K_I(_MDAT_CHAR_HEAD[sk])          # the hero's upper body (hero 1; all 4 share it)
    gB = [K_I(_MDAT_G_BODY[0]), K_I(_MDAT_G_BODY[1])]
    gH = [K_I(_MDAT_G_HEAD[0] + n - 1), K_I(_MDAT_G_HEAD[1] + n - 1)]
    out = []
    for L, legs in enumerate(cb):
        g = None
        if L < len(gB[sk]) and _rect(gB[sk][L]) == _rect(legs):
            g = L
        else:
            for k, r in enumerate(gB[sk]):
                if _rect(r) == _rect(legs):
                    g = k
                    break
        if g is not None:                  # 1. same legs: the general's own pose
            src = gH[sk][g]
            out.append(_copy(src, src.e - gB[sk][g].e + legs.e, src.f - gB[sk][g].f + legs.f))
            continue
        own = ch[L]                        # 2. the hero's own pose: FALLBACK
        t, k = FALLBACK.get(_rect(own), (sk, 0))
        src = gH[t][k]
        # bottom middle of the general's picture on the bottom middle of the hero's
        e = own.e - own.c // 2 + src.c // 2
        f = own.f - own.d + src.d
        out.append(_copy(src, e, f))
    return out


def head_frames(ag_inst, aB, sk):
    """cz.aC (sk = 0) or cz.aD (sk = 1) for hero aB."""
    if not is_general(aB):
        return ag_inst.K_I(_MDAT_CHAR_HEAD[sk] + aB)
    key = (head_number(aB), sk)
    if key not in _cache:
        _cache[key] = build_head_frames(ag_inst.K_I, key[0], sk)
    return _cache[key]


def unmapped(K_I, sk):
    """Hero upper-body pictures used by frames that have no general frame with the same legs
    and no FALLBACK entry (tests: must be empty)."""
    cb = K_I(_MDAT_CHAR_BODY[sk])
    ch = K_I(_MDAT_CHAR_HEAD[sk])
    gb = {_rect(r) for r in K_I(_MDAT_G_BODY[sk])}
    return sorted({_rect(ch[L]) for L, legs in enumerate(cb)
                   if _rect(legs) not in gb and _rect(ch[L]) not in FALLBACK})
