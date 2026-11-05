"""Asked by the player: on-screen keyboards of the Gamevil Live registration
(config.REG_KEYBOARD), so that a gamepad can type the UserID and the password too.

The original typed the UserID on the hero-name grid ag.f(int,int) (2 x 14
letters + OK) and the password from the number keys only. Here:

    UserID     A..N / O..Z + OK / 0..9    the original grid plus a row of digits
    password   0..9 + OK                  one row under the password box

Arrows move the cursor (up / down keep the column, clamped to the row's end; left / right wrap
in the row), OK types the cell, OK on the OK cell = the left soft key (CONFIRM). The cells are
drawn: 10 x 17 px, the OK cell 19 px wide, the cursor blinks red every 2 frames.
The hero-name grid itself stays the original's (pow/game/menus.py, pointer.py).
"""
from pow.game.game_canvas import GameCanvas
from pow.game.gfx import Gfx

UP, DOWN, LEFT, RIGHT, FIRE = -1, -2, -3, -4, -5
CELL_W, CELL_H, OK_W = 10, 17, 19
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
RED, BLUE, BLACK = 0xFF0000, 0x0000FF, 0


class KeyGrid:
    def __init__(self, rows):
        self.rows = [list(r) for r in rows]      # "OK" = the confirm cell
        self.row = 0
        self.col = 0

    @classmethod
    def user_id(cls):
        return cls([LETTERS[:14], [*LETTERS[14:], "OK"], "0123456789"])

    @classmethod
    def password(cls):
        return cls([[*"0123456789", "OK"]])

    @property
    def label(self):
        return self.rows[self.row][self.col]

    @property
    def is_ok(self):
        return self.label == "OK"

    def move(self, key):
        """An arrow key moves the cursor: True. Any other key: False, nothing changes."""
        if key == UP:
            self.row = (self.row - 1) % len(self.rows)
        elif key == DOWN:
            self.row = (self.row + 1) % len(self.rows)
        elif key == LEFT:
            self.col = (self.col - 1) % len(self.rows[self.row])
            return True
        elif key == RIGHT:
            self.col = (self.col + 1) % len(self.rows[self.row])
            return True
        else:
            return False
        self.col = min(self.col, len(self.rows[self.row]) - 1)
        return True

    # --- drawing ---
    @staticmethod
    def _row_width(row):
        return 2 + sum(OK_W if label == "OK" else CELL_W for label in row)

    @property
    def width(self):
        return max(self._row_width(row) for row in self.rows)

    def draw(self, y):
        """The grid with its top-left corner at (centre - width / 2, y)."""
        w = self.width
        left = GameCanvas.screen_cx - w // 2
        Gfx.fill_rect(left, y, w, CELL_H * len(self.rows), BLACK)
        blink = GameCanvas.frame % 4 < 2
        Gfx.set_font(GameCanvas.font_white)
        for r, row in enumerate(self.rows):
            top = y + 1 + CELL_H * r
            for c, label in enumerate(row):
                x = left + 2 + CELL_W * c
                wide = label == "OK"
                if wide:
                    Gfx.fill_rect(x + 1, top, OK_W, 15, BLUE)
                if blink and (r, c) == (self.row, self.col):
                    Gfx.fill_rect(x + (1 if wide else 0), top, OK_W if wide else CELL_W, 15, RED)
                dx = 1 if label in ("I", "OK") else 0
                Gfx.draw_string(label, x + 1 + dx, top - 1, 0)
