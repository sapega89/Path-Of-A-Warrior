"""Text input buffer for the hero name."""


class NameBuffer:
    def __init__(self, text, max_len, unused):
        self.chars = list(text)   # StringBuffer
        self.max_len = max_len           # max length
        self.changed = 0
        self.last_char = " "
        self.cursor = len(text)

    def move_cursor(self, step):
        if self.cursor + step >= 0 and self.cursor + step <= self.max_len - 1 and self.length() == self.cursor + step:
            self.cursor += step

    def get_text(self):
        return "".join(self.chars)

    def set_text(self, text):
        self.chars = list(text)

    def length(self):
        return 0 if len(self.chars) == 0 else len(self.chars)

    def handle_key(self, key):
        i = len(self.chars) - 1
        if key in (-7, -8):
            if i >= 0:
                del self.chars[i:]          # setLength(i)
                self.changed = 0
                self.move_cursor(-1)
            else:
                return 1
        elif 97 <= key <= 122 or 65 <= key <= 90 or 48 <= key <= 57:
            # 48..57 = the digits of the UserID keyboard (pow/game/key_grid.py);
            # the hero-name grid never sends them
            c = chr(key)
            if self.last_char != c:
                self.changed = 0
            self.last_char = c
            self.changed += 1
            if len(self.chars) == self.cursor:
                self.chars.append(c)
                self.changed = 1
            elif len(self.chars) < self.max_len:
                if len(self.chars) != 0:
                    self.move_cursor(1)
                self.chars.append(c)
        return 0
