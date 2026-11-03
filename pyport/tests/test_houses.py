"""PORT-EXTRA proposal 22: clans as the houses of the lords (pow/house_data.py, pow/game/house.py,
pow_server/houses.py)."""
import pathlib
import struct

import pytest

from conftest import ROOT  # noqa: F401  (sets sys.path and the dummy video driver)
import config
from pow import house_data as HD


def _res(name):
    return (pathlib.Path(config.RES_ROOT) / name).read_bytes()


def _houses():
    return HD.build_houses(_res("mission.arr"), _res("sideinfo.arr"), _res("ruler.arr"))


# --- the data --------------------------------------------------------------------------------
def test_houses_come_from_the_missions():
    hs = _houses()
    names = HD.general_names(_res("general.arr"))
    by = {h.name: h for h in hs}
    assert [h.lord for h in hs] == [1, 2, 3, 6, 7, 11, 14, 15, 16]
    # The Rise: for Lord Gabriel the hero duels Reeve (general 5), for Frederick Kirkland (4)
    assert by["Lord Gabriel"].foes[0] == 5 and names[5 - 1] == "Reeve"
    assert by["Lord Frederick"].foes[0] == 4 and names[4 - 1] == "Kirkland"
    assert by["Lord Gabriel"].portrait == 33
    # story missions (general 0 or >= 200) make no house: Lord Edison, Lord Edgar ...
    assert "Lord Edison" not in by and "Lord Edgar" not in by
    assert all(1 <= g < 200 for h in hs for g in h.foes)


def test_bonus_and_oath_break():
    assert HD.foe_bonus_percent(0) == 5 and HD.foe_bonus_percent(45) == 9
    assert HD.foe_bonus_percent(100) == 15 and HD.foe_bonus_percent(250) == 15
    assert HD.oath_break(41) == 20 and HD.oath_break(0) == 0


# --- the single player ------------------------------------------------------------------------
@pytest.fixture
def game(tmp_path, monkeypatch):
    from pow.game.game_canvas import GameCanvas
    from pow.game.menus import Menus
    from pow.game.scr_table import ScrTable
    from pow.game.structs import Hero
    from pow.midp.jrandom import Random
    monkeypatch.setattr(config, "SAVE_DIR", str(tmp_path))
    g = Menus.__new__(Menus)
    monkeypatch.setattr(GameCanvas, "menus", g)
    monkeypatch.setattr(GameCanvas, "scr_data", ScrTable("/edat.scr"))
    monkeypatch.setattr(GameCanvas, "rng", Random(42))
    monkeypatch.setattr(GameCanvas, "hero", Hero())
    monkeypatch.setattr(GameCanvas, "save_buf", [0] * 2000)
    monkeypatch.setattr(GameCanvas, "state", 2)
    monkeypatch.setattr(GameCanvas, "difficulty", 1)
    monkeypatch.setattr(GameCanvas, "save_pos", 0)
    monkeypatch.setattr(GameCanvas, "item_tables", [None] * 3)
    monkeypatch.setattr(GameCanvas, "tables_loaded", [False] * 16)
    monkeypatch.setattr(GameCanvas, "shop", [None] * 25)
    monkeypatch.setattr(GameCanvas, "house", 0)
    GameCanvas.hero.reset_inventory()
    g.new_hero()
    GameCanvas.hero.name = "Leo"
    GameCanvas.reset_quick_items()
    g.fill_shop()
    return g


def test_oath_needs_the_lord_to_know_the_hero(game):
    from pow.game import house
    from pow.game.game_canvas import GameCanvas
    cz = GameCanvas.hero
    assert not house.swear(1)                      # loyalty 0: Lord Gabriel does not know him
    cz.mission_progress[0] = 15                    # three missions won for Gabriel
    cz.mission_progress[1] = 40
    assert house.swear(1) and GameCanvas.house == 1 and house.sworn().name == "Lord Gabriel"
    assert not house.swear(1)                      # already his
    assert not house.swear(4)                      # Lord Edison: no house
    assert house.swear(2) and GameCanvas.house == 2
    assert cz.mission_progress[0] == 7             # leaving Gabriel halves his loyalty
    assert cz.mission_progress[1] == 40


def test_house_bonus_hits_only_the_foes(game, monkeypatch):
    from pow.game import house
    from pow.game.game_canvas import GameCanvas
    from pow.game.structs import MissionDef
    GameCanvas.hero.mission_progress[0] = 50       # Gabriel, +10%
    assert house.extra_damage(5, 100) == 0         # no oath, no bonus
    house.swear(1)
    assert house.is_foe(5) and house.extra_damage(5, 100) == 10     # Reeve fights Gabriel's war
    assert house.extra_damage(5, 3) == 1           # at least 1
    assert not house.is_foe(4) and house.extra_damage(4, 100) == 0  # Kirkland: not his foe
    assert not house.is_foe(201)                   # a monster
    # on a mission for Gabriel every general is a foe
    dz = MissionDef()
    dz.id = 1
    monkeypatch.setattr(GameCanvas, "lords", [dz, None, None, None, None])
    monkeypatch.setattr(GameCanvas, "mission", 0)
    monkeypatch.setattr(GameCanvas, "state", 3)
    assert house.is_foe(4)


def test_oath_is_in_the_save_and_old_saves_have_none(game):
    from pow.game import house
    from pow.game.game_canvas import GameCanvas
    from pow.midp.rms import RecordStore
    GameCanvas.hero.mission_progress[10] = 20      # Lord Jacob
    assert house.swear(11)
    assert game.save_game()
    size = GameCanvas.save_pos
    rec = RecordStore.openRecordStore("gamevil_pow_data", False).getRecord(1)
    from pow_mp import sp_bridge
    assert size == sp_bridge.SAVE_LEN                       # the save keeps its size
    assert struct.unpack_from("<i", bytes(rec), sp_bridge.OFF_HOUSE)[0] == 11
    assert rec[sp_bridge.OFF_PROGRESS + 10] == 20
    assert sp_bridge.house(bytes(rec)) == (11, 20)
    GameCanvas.house = 0
    game.load_game()
    assert GameCanvas.house == 11 and GameCanvas.save_pos == size
    # a save of before the houses: those 4 ints were 0
    data = bytearray(rec)
    struct.pack_into("<i", data, sp_bridge.OFF_HOUSE, 0)
    RecordStore.openRecordStore("gamevil_pow_data", False).setRecord(1, data, 0, len(data))
    game.load_game()
    assert GameCanvas.house == 0 and house.sworn() is None
    game.new_hero()
    assert GameCanvas.house == 0


def test_house_screen_lines(game):
    from pow.game import house
    from pow.game.game_canvas import GameCanvas
    h = house.house_of(1)
    lines = house.info_lines(h)
    assert lines[0] == "Loyalty 0/100" and lines[1] == "Serve him in a mission"
    assert lines[2].startswith("Foes: Reeve, Augustine,") and len(lines) == house.INFO_LINES
    assert all(len(s) <= 24 for s in lines) and lines[-1].endswith("...")
    GameCanvas.hero.mission_progress[0] = 30
    house.swear(1)
    assert house.info_lines(h)[:2] == ["Loyalty 30/100 Sworn", "Foes take +8% damage"]
    assert house.info_lines(house.house_of(3))[-1] == "Foes: Barclay, Melbourne"


# --- the server -------------------------------------------------------------------------------
def test_hall_bands():
    from pow_server import houses as H
    from pow_server.storage import open_storage
    hall = H.HouseHall(open_storage())
    hall.set_oath("ANNA", 1, 40, "Anna")
    hall.set_oath("BORIS", 1, 70, "Boris")
    hall.set_oath("CYRIL", 2, 10, "Cyril")
    hall.set_oath("DORA", 4, 10, "Dora")             # Lord Edison: no house
    assert hall.member("DORA") is None
    assert [r[1] for r in hall.roster(1)] == ["Boris", "Anna"]
    summary = dict((lord, (n, total)) for lord, n, total in hall.summary())
    assert summary[1] == (2, 110) and summary[2] == (1, 10) and summary[3] == (0, 0)
    bid = hall.create_band("ANNA")
    with pytest.raises(H.HouseError) as ex:
        hall.join_band("CYRIL", bid)                 # Frederick's man in Gabriel's band
    assert ex.value.code == H.OTHER_HOUSE
    hall.join_band("BORIS", bid)
    assert hall.band_of("BORIS") == (bid, "ANNA", ["ANNA", "BORIS"])
    for n in range(H.BAND_MAX - 2):
        hall.set_oath("X%d" % n, 1, 5)
        hall.join_band("X%d" % n, bid)
    hall.set_oath("LATE", 1, 5)
    with pytest.raises(H.HouseError) as ex:
        hall.join_band("LATE", bid)
    assert ex.value.code == H.BAND_FULL
    hall.leave_band("ANNA")                          # the most loyal left leads
    assert hall.band_of("BORIS")[1] == "BORIS"
    hall.set_oath("BORIS", 2, 30)                    # a new oath leaves the band
    assert hall.member("BORIS")["band"] == 0 and hall.band_of("X0")[2] == ["X0", "X1"]
    hall.set_oath("X0", 0, 0)                        # no oath any more
    assert hall.member("X0") is None and hall.band_of("X1")[2] == ["X1"]
    hall.leave_band("X1")
    assert hall.bands(1) == []
    with pytest.raises(H.HouseError):
        hall.leave_band("X1")


def _session(server, uid, extra=b""):
    from pow_server import codec_bin, messages as M
    from pow_mp import sp_bridge as S
    from test_mp_sp_bridge import make_save
    out = []

    def recv(f):
        out.extend(codec_bin.decode(p, from_client=False) for p in codec_bin.unframe(f)[0])

    sess = server.connect(recv)
    sess.receive(codec_bin.unframe(codec_bin.encode(M.LOGIN_FIRST, {"id": uid, "pwd": "1234",
                                                                     "ver": M.GAME_VER}, to_client=False))[0][0])
    tok = out[-1]["token"]
    hero = S.hero(make_save())
    msg = dict({"id": uid, "ver": M.GAME_VER, "token": tok, "sp": 1},
               **{"sp_" + k: v for k, v in hero.items()})
    msg["_extra"] = extra
    sess.receive(codec_bin.unframe(codec_bin.encode(M.LOGIN, msg, to_client=False))[0][0])
    out.clear()

    def ask(op, **fields):
        sess.receive(codec_bin.unframe(codec_bin.encode(op, fields, to_client=False))[0][0])
        return out[-1]
    return sess, ask


def test_server_protocol():
    from pow_server import codec_bin, houses as H, messages as M
    from pow_server.server import GameServer
    from pow_server.storage import MemoryStorage
    server = GameServer(MemoryStorage())

    def oath(lord, lv):
        buf = bytearray()
        codec_bin._encode_fields(buf, M.SP_HOUSE, {"sp_house": lord, "sp_loyalty": lv})
        return bytes(buf)

    _, anna = _session(server, "ANNA", oath(1, 45))
    _, boris = _session(server, "BORIS", oath(1, 60))
    _, cyril = _session(server, "CYRIL", oath(2, 20))
    _, dora = _session(server, "DORA")                     # an old client: no oath sent
    info = anna(M.HOUSE_INFO)
    assert info["st"] == 1 and (info["house"], info["loyalty"], info["band"]) == (1, 45, 0)
    rows = {r["lord"]: r for r in info["houses"]}
    assert rows[1]["name"] == "Lord Gabriel" and rows[1]["members"] == 2 and rows[1]["loyalty"] == 105
    assert rows[2]["members"] == 1 and len(rows) == len(H.houses())
    roster = anna(M.HOUSE_ROSTER, lord=1)
    assert [r["loyalty"] for r in roster["rows"]] == [60, 45]
    band = anna(M.BAND_CREATE)
    assert band["st"] == 1
    assert boris(M.BAND_JOIN, band=band["band"])["st"] == 1
    assert cyril(M.BAND_JOIN, band=band["band"])["st"] == H.OTHER_HOUSE
    assert dora(M.BAND_CREATE)["st"] == H.NO_HOUSE
    assert dora(M.HOUSE_INFO)["house"] == 0
    lst = boris(M.BAND_LIST)
    assert lst["n"] == 1 and lst["rows"][0]["members"] == 2
    assert boris(M.BAND_LEAVE)["st"] == 1 and boris(M.BAND_LEAVE)["st"] == H.NO_BAND
    # the next login with another oath moves the player
    _, anna = _session(server, "ANNA", oath(2, 30))
    assert anna(M.HOUSE_INFO)["house"] == 2 and server.houses.bands(1) == []


def test_house_rows_take_the_mouse(game, monkeypatch):
    from pow.game import house, pointer
    from pow.game.game_canvas import GameCanvas
    monkeypatch.setattr(GameCanvas, "menu", [house.MENU, 0, 0, 0, 0, 0, 0, 0])
    monkeypatch.setattr(GameCanvas, "view_cx", 120)
    monkeypatch.setattr(GameCanvas, "view_cy", 160)
    monkeypatch.setattr(GameCanvas, "view_y", 0)
    house.enter()
    assert GameCanvas.menu_count == len(house.houses())
    top = house.list_top()
    assert pointer._menu_keys(house.MENU, 120, top + 2 * 30 + 5, "click") == [pointer.DOWN] * 2 + [pointer.FIRE]
    assert pointer._menu_keys(house.MENU, 120, top + 25, "click") == []        # between two rows
    assert pointer._menu_keys(house.MENU, 120, top + 5, "click") == [pointer.FIRE]
