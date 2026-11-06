"""The multiplayer screens driven headless through tools/shot.py scenarios (Live > Multiplayer
on the in-game server): the menus, Character, Ranking, Options, a Duel vs CPU, a mission, the
Challenge, the orders and the chat must run to their end without raising."""
import os
import subprocess
import sys

import pytest
from conftest import ROOT

SCEN = ROOT / "tools" / "scenarios"


def _run(name, out):
    env = dict(os.environ, POW_DEBUG="1")   # an exception in the game loop fails the run
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "shot.py"), str(SCEN / (name + ".keys")),
                        "--out", str(out)], capture_output=True, text=True, check=False, timeout=600, env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    return r.stdout


@pytest.mark.parametrize("name", ["mp_menu", "mp_character", "mp_ranking", "mp_options",
                                  "mp_duel", "mp_duel2", "mp_mission", "mp_autobattle",
                                  "mp_challenge", "mp_invited", "mp_order_mission",
                                  "mp_order_menus", "mp_order", "mp_chat"])
def test_scenario_runs(name, tmp_path):
    out = tmp_path / name
    stdout = _run(name, out)
    assert list(out.glob("*.png")), stdout
