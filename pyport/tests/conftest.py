import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["POW_SCALE"] = "1"

import pytest  # noqa: E402


@pytest.fixture(scope="session")
def display():
    from pow.midp import display as d
    if d.screen is None:
        d.init(headless=True)
    return d
