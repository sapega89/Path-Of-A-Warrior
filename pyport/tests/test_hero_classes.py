"""PORT-EXTRA: own base stats for the four heroes and the attribute reset (pow/game/hero_classes.py)."""
import types

import pytest

from pow.game import hero_classes as H
from pow.game.structs import Item
from pow_server import battle as B
from pow_server import sp_rules as R


def _hero(head, hp, mp, atk, df, level=1, points=0, items=()):
    backpack = [Item() for _ in range(25)]
    for b, i in enumerate(items):
        backpack[b].id = i
    return types.SimpleNamespace(head=head, base_hp=hp, base_mp=mp, base_attack=atk, base_defense=df,
                                 hp=hp, mp=mp, level=level, stat_points=points, backpack=backpack)


def test_every_hero_is_worth_the_original_points():
    orig = H.BASE_STATS[0]
    assert orig == (30, 10, 5, 4)                       # ag.aw: head 0 keeps the original hero
    assert len(set(H.BASE_STATS)) == 4
    for stats in H.BASE_STATS:
        diffs = [(s - o) / g for s, o, g in zip(stats, orig, H.POINT_GAIN, strict=True)]
        assert all(d == int(d) for d in diffs) and sum(diffs) == 0


def test_server_has_the_same_table():
    for head, (hp, mp, atk, df) in enumerate(H.BASE_STATS):
        assert R.hero_base(head) == {"hp": hp, "mp": mp, "atk": atk, "def": df}
    assert dict(zip(("hp", "mp", "atk", "def"), H.POINT_GAIN, strict=True)) == R.POINT_GAIN


@pytest.mark.parametrize("head", range(4))
def test_respec_returns_all_points(head):
    hp, mp, atk, df = H.BASE_STATS[head]
    h = _hero(head, hp + 10, mp + 3, atk + 4, df + 2, level=3, points=1)   # 2+1+4+2 = 9 points
    assert H.spent_points(h) == 9
    assert H.respec(h) == 9
    assert (h.base_hp, h.base_mp, h.base_attack, h.base_defense) == (hp, mp, atk, df)
    assert h.stat_points == 10 and H.spent_points(h) == 0


@pytest.mark.parametrize("head", range(4))
def test_old_save_made_with_the_original_stats(head):
    """A hero saved before the heads differed (30/10/5/4 + points) gets exactly its points back."""
    h = _hero(head, 30 + 15, 10 + 6, 5 + 4, 4 + 1)     # 3 + 2 + 4 + 1 = 10 points
    assert H.spent_points(h) == 10
    H.respec(h)
    assert (h.base_hp, h.base_mp, h.base_attack, h.base_defense) == H.BASE_STATS[head]


def test_price():
    h = _hero(0, 30, 10, 5, 4, level=25, items=(101, 436))
    assert H.respec_gold(h) == 2500
    assert H.respec_item_slot(h) == 1
    assert H.respec_item_slot(_hero(0, 30, 10, 5, 4, items=(101, 502))) == -1


def test_hero_build_uses_the_face():
    ch = types.SimpleNamespace(face=1, atk=3 + 2, def_=5 + 1, hp=40 + 10, mp=7)
    assert B.hero_build(ch) == {"atk": 2, "def": 1, "hp": 2, "mp": 0}
    assert R.hero_stats(1, {"atk": 1}, face=3) == {"atk": 12, "def": 3, "hp": 25, "mp": 10}


def _game(monkeypatch, gold, items=()):
    from pow.game import popups as P
    from pow.game.game_canvas import GameCanvas
    from pow.game.menus import Menus
    hp, mp, atk, df = H.BASE_STATS[2]
    hero = _hero(2, hp + 5, mp, atk + 2, df, level=4, items=items)
    hero.gold = gold
    shown = []
    pop = types.SimpleNamespace(popup_id=0, show_text=shown.append, setup_choice=lambda *a: shown.append(a))
    monkeypatch.setattr(GameCanvas, "hero", hero)
    monkeypatch.setattr(GameCanvas, "popups", pop)
    monkeypatch.setattr(GameCanvas, "update_hero_stats", staticmethod(lambda: None))
    monkeypatch.setattr(GameCanvas, "menu", [14, 2, 0, 0, 0])
    m = Menus.__new__(Menus)
    monkeypatch.setattr(Menus, "save_game", lambda self: 1, raising=False)
    monkeypatch.setattr(Menus, "item_name", staticmethod(lambda i: "Falls Medicine"))
    return m, hero, shown, P


def test_pay_gold(monkeypatch):
    m, hero, shown, P = _game(monkeypatch, 1000)
    m.open_respec()
    assert shown[-1][0] == P.RESPEC_POPUP and shown[-1][1][1] == "Refund: 3 points"
    assert shown[-1][2] == ["Pay 400 gold", "No elixir", "Cancel"]
    m.finish_respec(0)
    assert hero.gold == 600 and hero.stat_points == 3 and hero.base_attack == H.BASE_STATS[2][2]


def test_not_enough_gold_and_cancel(monkeypatch):
    m, hero, shown, _P = _game(monkeypatch, 399)
    m.finish_respec(0)
    assert "Not enough gold" in shown[-1] and hero.stat_points == 0 and hero.gold == 399
    m.finish_respec(2)
    assert hero.stat_points == 0 and len(shown) == 1


def test_pay_with_an_elixir(monkeypatch):
    m, hero, shown, _P = _game(monkeypatch, 0, items=(101, 436))
    m.open_respec()
    assert shown[-1][2][1] == "Use Falls Medicine"
    m.finish_respec(1)
    assert hero.backpack[1].id == 0 and hero.backpack[0].id == 101 and hero.stat_points == 3
    m.finish_respec(1)                                  # nothing to pay with any more
    assert "no elixir" in shown[-1]
