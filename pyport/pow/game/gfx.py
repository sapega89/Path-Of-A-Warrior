"""x.java - the single drawing gateway of the game. Literal port.

Every drawing call of the game goes through these static methods.
Overloaded Java names get a signature suffix (see pyport/NAMES.md).
"""
from pow.midp.jint import i32, ushr32


class Gfx:
    g = None   # private static Graphics b;          x.java:5
    saved_clip_x = 0      # saved clip x                        x.java:7
    saved_clip_y = 0
    saved_clip_w = 0
    saved_clip_h = 0
    clip_x = 0      # current clip x                      x.java:15
    clip_y = 0
    clip_w = 0
    clip_h = 0
    font = None   # private static g k;  (current font)  x.java:23
    crc_table = None   # static int[] a;      (CRC table)    x.java:25

    @staticmethod
    def set_graphics(graphics):  # x.java:27-33
        Gfx.g = graphics
        Gfx.clip_x = Gfx.g.getClipX()
        Gfx.clip_y = Gfx.g.getClipY()
        Gfx.clip_w = Gfx.g.getClipWidth()
        Gfx.clip_h = Gfx.g.getClipHeight()

    @staticmethod
    def push_clip(x, y, w, h):  # x.java:35-45
        Gfx.saved_clip_x = Gfx.clip_x
        Gfx.saved_clip_y = Gfx.clip_y
        Gfx.saved_clip_w = Gfx.clip_w
        Gfx.saved_clip_h = Gfx.clip_h
        Gfx.clip_x = x
        Gfx.clip_y = y
        Gfx.clip_w = w
        Gfx.clip_h = h
        Gfx.g.clipRect(x, y, w, h)

    @staticmethod
    def pop_clip():  # x.java:47-53
        Gfx.clip_x = Gfx.saved_clip_x
        Gfx.clip_y = Gfx.saved_clip_y
        Gfx.clip_w = Gfx.saved_clip_w
        Gfx.clip_h = Gfx.saved_clip_h
        Gfx.g.setClip(Gfx.saved_clip_x, Gfx.saved_clip_y, Gfx.saved_clip_w, Gfx.saved_clip_h)

    @staticmethod
    def draw_image(image, x, y):  # x.java:55-57
        Gfx.g.drawImage(image, x, y, 20)

    @staticmethod
    def draw_image_anchored(image, x, y, anchor):  # x.java:59-61
        Gfx.g.drawImage(image, x, y, anchor)

    @staticmethod
    def draw_image_part(image, x, y, w, h, src_x, src_y):  # x.java:63-67
        Gfx.g.clipRect(x, y, w, h)
        Gfx.g.drawImage(image, x - src_x, y - src_y, 20)
        Gfx.g.setClip(Gfx.clip_x, Gfx.clip_y, Gfx.clip_w, Gfx.clip_h)

    @staticmethod
    def draw_rect(x, y, w, h, color):  # x.java:69-72
        Gfx.g.setColor(color)
        Gfx.g.drawRect(x, y, w - 1, h - 1)

    @staticmethod
    def fill_rect(x, y, w, h, color):  # x.java:74-77
        Gfx.g.setColor(color)
        Gfx.g.fillRect(x, y, w, h)

    @staticmethod
    def draw_line(x1, y1, x2, y2, color):  # x.java:79-82
        Gfx.g.setColor(color)
        Gfx.g.drawLine(x1, y1, x2, y2)

    @staticmethod
    def set_font(font):  # x.java:84-86
        Gfx.font = font

    @staticmethod
    def draw_chars(chars, start, count, x, y, anchor):  # x.java:88-102
        if (anchor & 0x1) != 0:
            x -= Gfx.font.chars_width(chars, start, count) // 2  # width >= 0: // == Java /
        elif (anchor & 0x8) != 0:
            x -= Gfx.font.chars_width(chars, start, count)
        i = start + count
        j = x
        for k in range(start, i):
            c = chars[k]
            m = Gfx.font.char_width(c)
            Gfx.font.draw_char(c, j, y)
            j += m

    @staticmethod
    def draw_string(text, x, y, anchor):  # x.java:104-106
        Gfx.draw_chars(list(text), 0, len(text), x, y, anchor)

    @staticmethod
    def make_crc_table():  # x.java:108-122  (CRC-32 table, polynomial 0xEDB88320)
        Gfx.crc_table = [0] * 256
        for b in range(256):
            i = b
            b1 = 8
            while True:
                b1 -= 1
                if b1 < 0:
                    break
                if (i & 0x1) != 0:
                    i = i32(0xEDB88320 ^ ushr32(i, 1))
                    continue
                i = ushr32(i, 1)
            Gfx.crc_table[b] = i

    @staticmethod
    def crc32(data, pos, count):  # x.java:124-129  (CRC-32)
        if Gfx.crc_table is None:
            Gfx.make_crc_table()
        i = -1
        while True:
            count -= 1
            if count < 0:
                break
            # Java: a[(i ^ bytes[p++]) & 0xFF] ^ i >>> 8 ; the byte is signed but only & 0xFF matters
            i = i32(Gfx.crc_table[(i ^ data[pos]) & 0xFF] ^ ushr32(i, 8))
            pos += 1
        return (i ^ 0xFFFFFFFF) & 0xFFFFFFFF

    # x.java:131-173: static initializer builds two byte arrays and throws them away (dead code).
