"""in the Gamevil Live Backpack / Warehouse grid (as.a(int, boolean)): LEFT / RIGHT
step one cell; only past the edge cell the cursor goes to the row before / after."""
import pytest
from conftest import ROOT  # noqa: F401  (sets sys.path and the dummy video driver)

LEFT, RIGHT = -3, -4


@pytest.fixture
def grid(monkeypatch):
    from pow.game.game_canvas import GameCanvas
    from pow.game.live import Live

    cursor = [0] * 40
    cursor[3] = 5        # visible rows
    cursor[4] = 9        # rows of the grid
    monkeypatch.setattr(GameCanvas, "cursor", cursor)
    monkeypatch.setattr(Live, "values", [0] * 32)
    monkeypatch.setattr(Live, "request_redraw", staticmethod(lambda: None))
    live = Live.__new__(Live)
    return live, cursor


def _walk(live, cursor, key, n):
    cells = []
    for _ in range(n):
        live.draw_grid_cursor(key, True)
        cells.append((cursor[10], cursor[9]))
    return cells


def test_right_visits_every_cell_of_the_row(grid):
    live, cursor = grid
    cursor[10], cursor[9] = 2, 0
    assert _walk(live, cursor, RIGHT, 5) == [(2, 1), (2, 2), (2, 3), (2, 4), (3, 0)]
    assert cursor[18] == 15


def test_left_visits_every_cell_of_the_row(grid):
    live, cursor = grid
    cursor[10], cursor[9] = 2, 4
    assert _walk(live, cursor, LEFT, 5) == [(2, 3), (2, 2), (2, 1), (2, 0), (1, 4)]
    assert cursor[18] == 9
