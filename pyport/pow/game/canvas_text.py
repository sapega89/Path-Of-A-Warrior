""", part of GameCanvas: text: tables, word wrap, numbers to text, byte strings.

A mixin of GameCanvas (pow/game/game_canvas.py); the methods keep their `# :FROM-TO`
comments. `GameCanvas` below is the real class, set by game_canvas.py once it exists.
"""

import config
from pow.game.jutil import _arraycopy
from pow.game.scr_table import ScrTable, _read_utf
from pow.midp.jint import i8, i16, idiv, imod

GameCanvas = None   # set by pow/game/game_canvas.py


class TextMixin:
    @staticmethod
    def split_field(text, index):  # field #paramInt of "a|b|c"
        if text is None:
            return None
        bool_ = False
        start = 0
        end = 0
        field = 0
        text = text + "|"
        for pos in range(len(text)):
            if text[pos] == "|":
                field += 1
            if not bool_ and field == index:
                if field == 0:
                    start = pos
                else:
                    start = pos + 1
                bool_ = True
            elif bool_ and field == index + 1:
                end = pos
                break
        return text[start:end]

    @staticmethod
    def u16(lo, hi):
        return i16(lo & 0xFF | (hi & 0xFF) << 8)

    @staticmethod
    def load_menu_texts():  # menu captions from uimenu.scr = edat[69]
        table = ScrTable("/" + GameCanvas.scr_data.get(69))
        for b in range(30):
            GameCanvas.menu_titles[b] = table.get(b)
            if b < 7:
                GameCanvas.skill_names[b] = table.get(b + 48)
            if b < 6:
                GameCanvas.main_menu_items[b] = table.get(b + 30)
            if b < 5:
                GameCanvas.speed_names[b] = table.get(b + 55)
            if b < 4:
                GameCanvas.option_names[b] = table.get(b + 42)
            if b < 2:
                GameCanvas.on_off[b] = table.get(b + 46)
        GameCanvas.game_menu_items[0] = table.get(36)
        GameCanvas.yes_no_items[0] = table.get(37)
        GameCanvas.help_items[0] = table.get(38)
        GameCanvas.ok_items[0] = table.get(39)
        GameCanvas.continue_items[0] = table.get(40)
        GameCanvas.pause_items[0] = table.get(41)
        table.free()

    @staticmethod
    def read_utf(data, start, end):  # readUTF of bytes[from:to]
        begin = start
        stop = end
        str_ = None
        try:
            size = stop - begin
            utf = bytearray(size + 2)
            utf[0] = size >> 8 & 0xFF
            utf[1] = size & 0xFF
            utf[2:] = data[begin:begin + size]
            str_ = _read_utf(utf)
        except Exception:
            pass
        return str_

    @staticmethod
    def gamestr(index):
        return GameCanvas.scr_gamestr.get(index)

    @staticmethod
    def key_digit(key):  # key code '0'..'9' -> digit, else -1
        if 48 <= key <= 57:
            return key - 48
        return -1

    @staticmethod
    def trim_right(text):  # trim trailing spaces; sic: one char left -> ""
        last = len(text) - 1
        while last >= 0 and text[last] == " ":
            last -= 1
        return "" if last == 0 else text[:last + 1]

    @staticmethod
    def cut_at_control(text):  # up to the first control character
        b = 0
        while b < len(text) and text[b] >= " ":
            b += 1
        return "" if b == 0 else text[:b]

    @staticmethod
    def cut_at_space(text):  # up to the first space
        b = 0
        while b < len(text) and text[b] != " ":
            b += 1
        return "" if b == 0 else text[:b]

    @staticmethod
    def char_width(ch):  # width of a character
        return GameCanvas.font_white.char_width(chr(ch & 0xFFFF))

    def word_wrap(self, text, width, slot):  # word wrap into dp[paramInt2]
        line_start = 0
        break_at = 0
        line_w = 0
        b = 0
        GameCanvas.text_line_count[slot] = 0
        lines = GameCanvas.text_lines[slot] = [None] * 120
        size = len(text)
        pos = 0
        while pos <= size:
            if pos != size:
                ch = text[pos]
                line_w += GameCanvas.char_width(ch)
                if (ch in {32, 124}) and line_w - GameCanvas.char_width(ch) >= width:
                    if break_at < line_start:
                        break_at = pos
                    lines[b] = GameCanvas.read_utf(text, line_start, break_at)
                    b += 1
                    line_start = break_at + 1
                    pos = line_start - 1
                    line_w = 0
                elif ch == 32:
                    break_at = pos
                elif ch == 124:
                    lines[b] = GameCanvas.read_utf(text, line_start, pos)
                    b += 1
                    line_start = break_at = pos + 1
                    line_w = 0
            elif line_w > width:
                lines[b] = GameCanvas.read_utf(text, line_start, break_at)
                b += 1
                lines[b] = GameCanvas.read_utf(text, break_at + 1, pos)
                b += 1
            elif break_at != size - 1:
                lines[b] = GameCanvas.read_utf(text, line_start, pos)
                b += 1
            pos += 1
        if b >= 1:
            GameCanvas.text_line_count[slot] = i8(b - 1)
        return 1

    @staticmethod
    def parse_int(chars):  # Integer.parseInt of the leading digits
        str_ = ""
        b = 0
        while b < len(chars) and "0" <= chars[b] <= "9":
            str_ = str_ + chars[b]
            b += 1
        return int(str_)

    # ---- menus: Options / Help / Endings helpers -------------------------------------------

    def edat_bytes(self, file, index):
        return GameCanvas.edat_string(file, index).encode("latin-1")

    @staticmethod
    def edat_string(file, index):  # string paramInt2 of edat file paramInt1
        table = ScrTable("/" + GameCanvas.scr_data.get(file))
        str_ = table.get(index)
        table.free()
        return str_

    @staticmethod
    def digit_count(value):  # number of digits
        powers = [10, 100, 1000, 10000]
        b = 0
        while b < 4 and value >= powers[b]:
            b += 1
        return b + 1

    @staticmethod
    def measure_text(text):  # text width
        return GameCanvas.font_white.string_width(text)

    @staticmethod
    def format_thousands(value):  # 12345 -> "12,345"
        str_ = str(value)
        size = len(str_)
        digits = [0] * size
        for i in range(size):
            digits[size - i - 1] = imod(value, 10)
            value = idiv(value, 10)
        str_ = ""
        for j in range(size):
            str_ = str_ + str(digits[j])
            if size % 3 == (j + 1) % 3 and j != size - 1:
                str_ = str_ + ","
        return str_

    # ---- Missions: lords, mission list, briefing text, general data ------------------------

    @staticmethod
    def u8(value):
        return i16(value & 0xFF)

    def load_mission_text(self):  # mission description -> dp[0]
        GameCanvas.mission_name = GameCanvas.mission_names[GameCanvas.mission]
        table = GameCanvas.load_data_file(56)
        text = self.table_text(table, GameCanvas.lord_missions[GameCanvas.lord] + GameCanvas.mission)
        b = 0
        while b < len(text) and text[b] != 0:
            b += 1
        line = bytearray(text[:b])
        self.word_wrap(line, 190, 0)

    def table_text(self, table, index):  # (text paramInt of a table, "(..)" macros)
        offsets = [0] * 110
        src = bytearray(1500)
        macro = bytearray(1500)
        out = bytearray(1500)
        digits = ["\0"] * 3
        digit_count = 0
        copied = [0, 0]
        pos = [0, 0]
        count = table[0] & 0xFF | table[1] << 8 & 0xFF00
        for i in range(count + 1):
            offsets[i] = table[2 + i * 2] & 0xFF | table[2 + i * 2 + 1] << 8 & 0xFF00
        _arraycopy(table, offsets[index], src, 0,
                   offsets[index + 1] - offsets[index])
        i = 0
        while i < 3 and 48 <= src[i] <= 57:
            digits[i] = chr(src[i])
            digit_count += 1
            i += 1
        if digit_count != 0:
            pos[0] = digit_count + 1
            copied[0] = digit_count + 1
            macro_no = GameCanvas.parse_int(digits)
            _arraycopy(table, offsets[macro_no], macro, 0, offsets[macro_no + 1] - offsets[macro_no])
        else:
            _arraycopy(src, 0, macro, 0, 1500)
        while macro[pos[1]] != 0:
            if macro[pos[1]] == 40:
                out = GameCanvas.append_bytes(out, macro, copied[1], pos[1])
                copied[1] = pos[1] + 1
                if digit_count != 0:
                    pos[1] = GameCanvas.index_after(macro, pos[1], ")")
                    copied[1] = pos[1]
                    pos[0] = GameCanvas.index_after(src, pos[0], "|")
                    out = GameCanvas.append_bytes(out, src, copied[0], pos[0] - 1)
                    copied[0] = pos[0]
                    continue
                pos[1] = GameCanvas.index_after(macro, pos[1], ")")
                out = GameCanvas.append_bytes(out, macro, copied[1], pos[1] - 1)
                copied[1] = pos[1]
                continue
            pos[1] = pos[1] + 1
        return GameCanvas.append_bytes(out, macro, copied[1], pos[1])

    @staticmethod
    def append_bytes(dst, src, start, end):  # append at the first 0
        b = 0
        while b < len(dst) and dst[b] != 0:
            b += 1
        _arraycopy(src, start, dst, b, end - start)
        return dst

    @staticmethod
    def index_after(data, start, ch):  # index after the next paramChar
        code = ord(ch)
        b = 0
        while data[start + b] != code and data[start + b] != 0:
            if (data[start + b] & 0x80) != 0:
                b += 2
            b += 1
        return start + b + 1

    @staticmethod
    def decimal_digits(value):  # number of decimal digits
        b = 1
        limit = 10
        while value >= limit:
            b += 1
            limit *= 10
        return b
