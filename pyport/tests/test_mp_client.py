"""The generated MP client (pow_mp/_gen) driven headless through tools/mp_shot.py scenarios
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
                                  "mp_duel"])
def test_scenario_runs(name, tmp_path):
    mp_shot = _mp_shot()
    saved, frames = mp_shot.run(mp_shot.parse(SCEN / (name + ".keys")), tmp_path / "out",
                                save_dir=str(tmp_path / "rms"))
    assert saved and frames > 30


def test_login_registers_on_local_server(tmp_path):
    mp_shot = _mp_shot()
    mp_shot.run(mp_shot.parse(SCEN / "mp_menu.keys"), tmp_path / "out", save_dir=str(tmp_path / "rms"))
    from pow_mp.net.transport import LocalTransport
    srv = LocalTransport._server
    assert srv.storage.has_account("TEST")
    assert "TEST" in srv.online


def test_duel_reaches_the_result_and_is_recorded(tmp_path):
    mp_shot = _mp_shot()
    saved, _ = mp_shot.run(mp_shot.parse(SCEN / "mp_duel.keys"), tmp_path / "out",
                           save_dir=str(tmp_path / "rms"))
    assert "08_result.png" in saved and saved[-1].endswith("back_to_duel_menu.png")
    from pow_mp.net.transport import LocalTransport
    ch = LocalTransport._server.storage.load("TEST")
    assert ch.wins + ch.losses == 1
