"""at.java - text input buffer for the hero name. Literal port."""


class NameBuffer:
    def __init__(self, paramString, paramInt1, paramInt2):  # at.java:12-18
        self.chars = list(paramString)   # StringBuffer
        self.max_len = paramInt1           # max length
        self.changed = 0
        self.last_char = ' '
        self.cursor = len(paramString)

    def move_cursor(self, paramInt):  # at.java:20-23
        if self.cursor + paramInt >= 0 and self.cursor + paramInt <= self.max_len - 1 and self.length() == self.cursor + paramInt:
            self.cursor += paramInt

    def get_text(self):  # at.java:25-28
        return "".join(self.chars)

    def set_text(self, paramString):  # at.java:30-32
        self.chars = list(paramString)

    def length(self):  # at.java:34-42
        return 0 if len(self.chars) == 0 else len(self.chars)

    def handle_key(self, paramInt):  # at.java:44-70
        i = len(self.chars) - 1
        if paramInt == -7 or paramInt == -8:
            if i >= 0:
                del self.chars[i:]          # setLength(i)
                self.changed = 0
                self.move_cursor(-1)
            else:
                return 1
        elif 97 <= paramInt <= 122 or 65 <= paramInt <= 90:
            c = chr(paramInt)
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
