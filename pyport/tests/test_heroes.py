"""PORT-EXTRA: 10 heroes (pow/game/heroes.py) - frame tables, portraits, select screen, MP faces."""
import io
import struct

from conftest import ROOT  # noqa: F401  (sets sys.path and the dummy video driver)

RES = ROOT.parent


def _names(scr_strings):
    return {int(a): b.strip() for a, b in (l.split("\t") for l in (RES / scr_strings).read_text().splitlines() if l)}


def _k_i():
    """ag.K_I over the files named in mdat_QVGA.scr (ag.bF)."""
    from pow.game.al import al
    from pow.game.structs import y
    bF = al("/mdat_QVGA.scr")

    def K_I(i):
        data = (RES / bF.a_I(i)).read_bytes()
        out = []
        for k in range(data[0]):
            r = y()
            r.a, r.b, r.c, r.d, r.e, r.f = struct.unpack("<6h", data[1 + 12 * k:13 + 12 * k])
            out.append(r)
        return out
    return K_I


def test_roster_pictures():
    from pow.game import heroes
    imgchar = _names("imgchar_strings.txt")
    assert heroes.HERO_COUNT == 10
    assert [imgchar[heroes.portrait_index(b)] for b in range(10)] == [
        "ju_1", "ju_2", "ju_3", "ju_4", "jang_1", "jang_2", "jang_17", "jang_4", "jang_3", "jang_6"]
    assert [imgchar[heroes.head_image_index(b)] for b in range(10)] == [
        "char_head1", "char_head2", "char_head3", "char_head4",
        "g_head1", "g_head2", "g_head3", "g_head4", "g_head5", "g_head6"]


def test_portraits_are_the_generals_own():
    """general.arr: name, head (byte 11), face (byte 18) - the hero wears the general's head and face."""
    from pow.game import heroes
    data = (RES / "general.arr").read_bytes()
    gens = {}
    for k in range(1, 140):
        j = 23 * (k - 1) + 14
        if j + 23 > len(data):
            break
        name = data[j:j + 11].split(b"\0")[0].decode("latin-1")
        gens[name] = (data[j + 11], data[j + 18])
    for head, face, name in heroes.GENERAL_HEROES:
        assert gens[name] == (head, face), name


def test_frame_tables_cover_every_hero_frame():
    from pow.game import heroes
    K_I = _k_i()
    assert heroes.unmapped(K_I, 0) == [] and heroes.unmapped(K_I, 1) == []
    for n in range(1, 7):
        w, h = __import__("PIL.Image", fromlist=["Image"]).open(RES / ("g_head%d.png" % n)).size
        for sk, count in ((0, 53), (1, 162)):
            table = heroes.build_head_frames(K_I, n, sk)
            assert len(table) == count == len(K_I(45 + sk))
            for r in table:                                   # every rectangle is inside g_headN.png
                assert 0 <= r.a and 0 <= r.b and r.a + r.c <= w and r.b + r.d <= h and r.c > 0


def test_same_legs_keep_the_generals_pose():
    """A hero frame on legs the general also has shows the general's frame, placed the same way
    relative to the legs."""
    from pow.game import heroes
    K_I = _k_i()
    table = heroes.build_head_frames(K_I, 1, 0)
    cb, gb, gh = K_I(45), K_I(68), K_I(70)
    for L, g in ((0, 0), (3, 2), (12, 8), (40, 20)):        # stand, walk right, attack, lying
        assert (table[L].a, table[L].b) == (gh[g].a, gh[g].b)
        assert table[L].e - cb[L].e == gh[g].e - gb[g].e and table[L].f - cb[L].f == gh[g].f - gb[g].f


def test_hero_select_cycles_through_10(monkeypatch):
    from pow.game import heroes
    from pow.game.ag import ag
    from pow.game.structs import n
    monkeypatch.setattr(ag, "cz", n())
    seen = []
    for _ in range(10):
        ag.cz.aB = (ag.cz.aB + 1) % heroes.HERO_COUNT        # e.java case 6 (RIGHT)
        seen.append(ag.cz.aB)
    assert sorted(seen) == list(range(10))


def test_hero_select_clicks(monkeypatch):
    """e.aK: 5 heads at x = dd-118 + 47*b; the middle one = OK, the others turn the row."""
    from pow.game import pointer
    from pow.game.ag import ag
    monkeypatch.setattr(ag, "cM", [6, 0, 0, 0, 0])
    dd, de = ag.dd, ag.de
    L, R, F = pointer.LEFT, pointer.RIGHT, pointer.FIRE
    row = [pointer._new_game_keys(6, dd - 118 + 47 * b + 20, de + 30, "click") for b in range(5)]
    assert row == [[L, L], [L], [F], [R], [R, R]]
    assert pointer._new_game_keys(6, dd - 40, de + 70, "click") == [L]
    assert pointer._new_game_keys(6, dd + 32, de + 70, "click") == [R]


def test_mp_faces_from_portraits():
    import pygame
    from pow_mp import faces
    for f in range(4, 10):
        strip = pygame.image.load(io.BytesIO(faces.read("/face%d.png" % f)), "x.png")
        assert strip.get_size() == (41, 12)
        for k in (faces.ACT_BASE + f, faces.ACT_BASE + 6 + f):
            panel = pygame.image.load(io.BytesIO(faces.read("/act%d.png" % k)), "x.png")
            assert panel.get_size() == (86, 19)
        assert faces.read("/sprhead%d.png" % (f + 1)) is not None
    assert faces.read("/face3.png") is None and faces.read("/act12.png") is None


def test_mp_server_keeps_faces_0_to_9():
    from pow_server import model
    assert model.HERO_COUNT == 10


def test_mp_client_has_room_for_10_faces():
    from pow_mp import faces, game
    mods = game.load()
    g, l = mods["g"].g, mods["l"].l
    assert len(g.de) == 10                                    # face0..9 strips
    assert len(g.dg) == len(l.es) == len(l.et) == faces.ACT_BASE + 16
    assert len(g.dw) == len(g.dx) == 10                       # sprhead1..10 (as in the jar)


def test_mp_sp_face_kept():
    """262: the single-player hero's face 0..9 reaches the MP character (was & 3)."""
    from pow_server import model
    msg = {"sp": 1, "sp_level": 5, "sp_hp": 100, "sp_mp": 20, "sp_atk": 9, "sp_def": 4,
           "sp_hp_bonus": 0, "sp_mp_bonus": 0, "sp_atk_bonus": 0, "sp_def_bonus": 0,
           "sp_weapon": 1, "sp_skills": [0] * 11, "sp_slots": [99] * 4, "sp_progress": 0}
    for face, want in ((2, 2), (7, 7), (9, 9), (10, 0), (200, 0)):
        ch = model.Character(user_id="u")
        assert model.apply_sp_hero(ch, dict(msg, sp_face=face))
        assert ch.face == want
