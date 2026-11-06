"""The MP client (pow.game.online) driven headless through tools/mp_shot.py scenarios
against the in-game server: login, main menu, Character, Ranking, Options and a Duel vs CPU must not raise."""
import importlib.util
import pathlib

import pytest

HERE = pathlib.Path(__file__).resolve().parent.parent
SCEN = HERE / "tools" / "scenarios"


def _mp_shot():
    spec = importlib.util.spec_from_file_location("mp_shot", HERE / "tools" / "mp_shot.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize("name", ["mp_login", "mp_menu", "mp_character", "mp_ranking", "mp_options",
                                  "mp_duel", "mp_duel2", "mp_mission",
                                  "mp_challenge", "mp_invited", "mp_order_mission",
                                  "mp_order_menus"])
def test_scenario_runs(name, tmp_path):
    mp_shot = _mp_shot()
    saved, frames = mp_shot.run(mp_shot.parse(SCEN / (name + ".keys")), tmp_path / "out",
                                save_dir=str(tmp_path / "rms"))
    assert saved and frames > 30


def test_single_player_account_logs_in_without_the_login_screen(tmp_path):
    """PORT-EXTRA use_sp_account: the Live registration of the single player is the
    Multiplayer account: the title logs in at once, no Login screen (state 2) on the way."""
    mp_shot = _mp_shot()
    states = set()
    from pow.midp import display

    def seen(_screen):
        from pow.game.online.mp_canvas import MpCanvas
        states.add(MpCanvas.state)
    display.frame_hooks.append(seen)
    try:
        saved, _ = mp_shot.run(mp_shot.parse(SCEN / "mp_sp_account.keys"), tmp_path / "out",
                               save_dir=str(tmp_path / "rms"))
    finally:
        display.frame_hooks.remove(seen)
    from pow.midp.transport import LocalTransport
    assert "ANDREY" in LocalTransport._server.online
    assert 2 not in states and 10 in states
    assert saved[-1].endswith("main_menu_no_login.png")


def test_login_registers_on_local_server(tmp_path):
    mp_shot = _mp_shot()
    mp_shot.run(mp_shot.parse(SCEN / "mp_menu.keys"), tmp_path / "out", save_dir=str(tmp_path / "rms"))
    from pow.midp.transport import LocalTransport
    srv = LocalTransport._server
    assert srv.storage.has_account("TEST")
    assert "TEST" in srv.online


def test_duel_reaches_the_result_and_is_recorded(tmp_path):
    mp_shot = _mp_shot()
    saved, _ = mp_shot.run(mp_shot.parse(SCEN / "mp_duel.keys"), tmp_path / "out",
                           save_dir=str(tmp_path / "rms"))
    assert "08_result.png" in saved and saved[-1].endswith("back_to_duel_menu.png")
    from pow.midp.transport import LocalTransport
    ch = LocalTransport._server.storage.load("TEST")
    assert ch.wins + ch.losses == 1


def test_single_player_hero_plays_the_duel_and_gets_the_rewards(tmp_path, monkeypatch):
    """9.10: with a single-player save next to it, the client logs in with that hero and the
    duel's gold / fame / exp end up in the save."""
    import struct

    from test_mp_sp_bridge import make_save, store

    import config
    from pow.game.online import sp_bridge as S
    rms = tmp_path / "rms"
    monkeypatch.setattr(config, "SAVE_DIR", str(rms))
    store(make_save(gold=1000, fame=50, exp=7))
    mp_shot = _mp_shot()
    saved, _ = mp_shot.run(mp_shot.parse(SCEN / "mp_duel.keys"), tmp_path / "out", save_dir=str(rms))
    assert "08_result.png" in saved
    from pow.midp.transport import LocalTransport
    ch = LocalTransport._server.storage.load("TEST")
    assert ch.sp_linked and ch.level == 12 and ch.max_hp() == 260 and ch.skills == {3: 3, 9: 2}
    monkeypatch.setattr(config, "SAVE_DIR", str(rms))
    gold, fame, exp = struct.unpack_from("<iii", S.read_save(), S.OFF_GOLD)
    assert gold == 1000 + ch.gold and exp == 7 + ch.mp_exp and fame == 50 + ch.mp_fame


def test_auto_battle_plays_the_duel_alone(tmp_path):
    """PORT-EXTRA auto-battle: after Tab the client sends AUTO (255) in every 1027 and the
    server's bot plays the hero; the duel ends without an action key."""
    mp_shot = _mp_shot()
    try:
        saved, _ = mp_shot.run(mp_shot.parse(SCEN / "mp_autobattle.keys"), tmp_path / "out",
                               save_dir=str(tmp_path / "rms"))
    finally:
        from pow.game.online.mp_canvas import MpCanvas
        auto, MpCanvas.auto_battle = MpCanvas.auto_battle, False
    assert auto and saved[-1].endswith("auto_end.png")
    from pow.midp.transport import LocalTransport
    ch = LocalTransport._server.storage.load("TEST")
    assert ch.wins + ch.losses == 1


def test_order_window_team_duel_and_leave(tmp_path):
    """PORT-EXTRA: join RIVAL's order in the Order window, a 2-on-2 duel together, back to the
    window, leave the order."""
    mp_shot = _mp_shot()
    saved, _ = mp_shot.run(mp_shot.parse(SCEN / "mp_order.keys"), tmp_path / "out",
                           save_dir=str(tmp_path / "rms"))
    assert any(n.endswith("_result.png") for n in saved)
    assert any(n.endswith("_back_to_order.png") for n in saved) and saved[-1].endswith("after_leave.png")
    from pow.midp.transport import LocalTransport
    from pow_server import orders
    st = LocalTransport._server.storage
    test, rival = st.load("TEST"), st.load("RIVAL")
    assert test.order == "" and rival.order == "WOLF"
    assert orders.get(st, "WOLF")["members"] == ["RIVAL"]
    assert test.wins + test.losses == 1 and test.wins == rival.wins and test.losses == rival.losses


def test_chat_private_answer_and_lobby(tmp_path):
    """PORT-EXTRA: the Chat window: RIVAL's private message waits (badge, Private tab), TEST
    answers on the keyboard grid and the PC keyboard, RIVAL answers back, then TEST writes in
    the Lobby (40 characters at most)."""
    mp_shot = _mp_shot()
    saved, _ = mp_shot.run(mp_shot.parse(SCEN / "mp_chat.keys"), tmp_path / "out",
                           save_dir=str(tmp_path / "rms"))
    assert saved[-1].endswith("no_order.png")
    from pow.game.online.mp_canvas import MpCanvas
    from pow.midp.transport import LocalTransport
    from pow_server import chat
    st = LocalTransport._server.storage
    pm = chat.history(st, chat.pm_key("TEST", "RIVAL"))["rows"]
    assert [r[0] for r in pm] == ["RIVAL", "TEST", "RIVAL"]
    assert pm[1][2] == "Hi! Ready when you are." and pm[2][2] in chat.BOT_LINES
    lobby = chat.history(st, "chat:lobby")["rows"]
    assert lobby[-1] == ["TEST", "TEST", "Hello everyone, I am new here and ready"]
    assert MpCanvas.chat_unread == [0, 0, 0] and MpCanvas.chat_no_order
