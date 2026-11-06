"""PHASE_9 task 9.9: loot of the multiplayer battles, by the single-player drop rules."""
import random
import struct

import pytest
from test_mp_sp_bridge import make_save, store

import config
from pow.game.online import sp_bridge as S
from pow_server import loot


def test_tables_from_the_single_player():
    t = loot.tables()
    assert len(t["normal"]) == 100 and len(t["special"]) == 137 and len(t["rare"]) == 17
    assert all(len(it.name) <= 15 for v in t.values() for it in v)      # 1032 char[15]
    claymore = next(it for it in t["normal"] if it.id == 118)
    assert (claymore.name, claymore.atk, claymore.spread, claymore.level) == ("War Claymore", 6, 4, 25)
    valor = next(it for it in t["rare"] if it.id == 501)
    assert (valor.name, valor.hp, valor.mp, valor.level) == ("Book of Valor", 150, 150, 130)
    assert 502 not in {it.id for it in t["rare"]}                       # story only


@pytest.mark.parametrize(("kind", "drop", "equip"), [(0, 5, 10), (1, 10, 30), (2, 20, 60)])
def test_drop_rates_are_the_single_players(kind, drop, equip):
    rng = random.Random(3)
    n = 40000
    got = [loot.sp_drop(rng, 30, kind) for _ in range(n)]
    drops = [g for g in got if g]
    assert abs(len(drops) / n * 100 - drop) < 1
    assert abs(sum(g > 100 for g in drops) / len(drops) * 100 - equip) < 4
    assert all(1 <= g <= 11 or 101 <= g <= 200 for g in drops)


def test_normal_tier_follows_the_hero_level():
    rng = random.Random(5)
    def tiers(lv):
        return [(g - 101) % 5 for g in (loot.sp_drop(rng, lv, 2) for _ in range(6000)) if g > 100]

    assert set(tiers(5)) == {0, 1}                       # level <= 9: {80, 100} -> tiers 0-1
    assert set(tiers(80)) == set(tiers(50)) == {0, 1, 2, 3, 4}   # DROPS_AFTER_69
    import config
    old, config.DROPS_AFTER_69 = config.DROPS_AFTER_69, False
    try:
        assert min(tiers(80)) == 2                       # the original above Lv69: {0, 0, 33, 77, 100}
    finally:
        config.DROPS_AFTER_69 = old


def test_roll_keeps_the_best_and_can_give_special_or_rare():
    rng = random.Random(9)
    assert loot.roll(rng, 30, []) is None
    seen = set()
    for _ in range(3000):
        it = loot.roll(rng, 90, [2, 2, 2])
        if it:
            seen.add(it["id"] // 100)
            assert it["name"] and (it["id"] < 100 or it["atk"] + it["def"] + it["hp"] + it["mp"] >= 0)
    assert {0, 1, 3, 5} <= seen


@pytest.fixture
def save_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "SAVE_DIR", str(tmp_path))
    return tmp_path


def _cell(d, i):
    return struct.unpack_from("<hhhhhB", d, S.OFF_BACKPACK + 11 * i)


def test_item_goes_into_the_backpack_and_potions_onto_the_belt(save_dir):
    store(make_save())
    assert S.add_item(118, 9, 0, 0, 0) == 0
    assert S.add_item(3) == 0 and S.add_item(3) == 0
    d = S.read_save()
    assert _cell(d, 0) == (118, 9, 0, 0, 0, 0)
    assert struct.unpack_from("<hB", d, S.OFF_BELT) == (3, 2)


def test_full_backpack_keeps_the_loot_waiting(save_dir):
    data = bytearray(make_save())
    for o in S._backpack_offsets(data):                  # the 25 cells and the extra block
        struct.pack_into("<h", data, o, 101)
    store(data)
    assert S.add_item(504) == 1                          # waiting
    d = bytearray(S.read_save())
    struct.pack_into("<h", d, S.OFF_BACKPACK + 11 * 7, 0)   # the player sold something
    from pow.midp.rms import RecordStore
    RecordStore.openRecordStore(S.SAVE_STORE, False).setRecord(1, d, 0, len(d))
    assert S.add_item() == 0                             # the next login delivers it
    assert _cell(S.read_save(), 7)[0] == 504


def test_no_save_no_loot(save_dir):
    assert S.add_item(118) is None


def test_client_takes_the_item_from_1032(save_dir):
    from pow.game.online.net_thread import NetThread
    from pow_server import codec_bin
    from pow_server import messages as M
    store(make_save(gold=0, fame=0, exp=0))
    frame = codec_bin.encode(M.BATTLE_END, {"st": 1, "win": 1, "gold": 50, "fame": 3, "exp": 9,
                                            "loot": "Black Barb", "item_id": 379, "item_def": 4,
                                            "item_hp": 75, "item_mp": 36}, to_client=True)
    NetThread._port_extra_in(codec_bin.unframe(frame)[0][0])
    d = S.read_save()
    assert _cell(d, 0) == (379, 0, 4, 75, 36, 0)
    assert struct.unpack_from("<iii", d, S.OFF_GOLD) == (50, 3, 9)
