"""The single drawing gateway of the game.

Every drawing call of the game goes through these static methods.
One drawing gateway for the whole game.
"""
from pow.midp.jint import i32, ushr32


class Gfx:
    g = None
    saved_clip_x = 0      # saved clip x
    saved_clip_y = 0
    saved_clip_w = 0
    saved_clip_h = 0
    clip_x = 0      # current clip x
    clip_y = 0
    clip_w = 0
    clip_h = 0
    font = None   # current font
    crc_table = None   # CRC table

    @staticmethod
    def set_graphics(graphics):
        Gfx.g = graphics
        Gfx.clip_x = Gfx.g.getClipX()
        Gfx.clip_y = Gfx.g.getClipY()
        Gfx.clip_w = Gfx.g.getClipWidth()
        Gfx.clip_h = Gfx.g.getClipHeight()

    @staticmethod
    def push_clip(x, y, w, h):
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
    def pop_clip():
        Gfx.clip_x = Gfx.saved_clip_x
        Gfx.clip_y = Gfx.saved_clip_y
        Gfx.clip_w = Gfx.saved_clip_w
        Gfx.clip_h = Gfx.saved_clip_h
        Gfx.g.setClip(Gfx.saved_clip_x, Gfx.saved_clip_y, Gfx.saved_clip_w, Gfx.saved_clip_h)

    @staticmethod
    def draw_image(image, x, y):
        Gfx.g.drawImage(image, x, y, 20)

    @staticmethod
    def draw_image_anchored(image, x, y, anchor):
        Gfx.g.drawImage(image, x, y, anchor)

    @staticmethod
    def draw_image_part(image, x, y, w, h, src_x, src_y):
        Gfx.g.clipRect(x, y, w, h)
        Gfx.g.drawImage(image, x - src_x, y - src_y, 20)
        Gfx.g.setClip(Gfx.clip_x, Gfx.clip_y, Gfx.clip_w, Gfx.clip_h)

    @staticmethod
    def draw_rect(x, y, w, h, color):
        Gfx.g.setColor(color)
        Gfx.g.drawRect(x, y, w - 1, h - 1)

    @staticmethod
    def fill_rect(x, y, w, h, color):
        Gfx.g.setColor(color)
        Gfx.g.fillRect(x, y, w, h)

    @staticmethod
    def draw_line(x1, y1, x2, y2, color):
        Gfx.g.setColor(color)
        Gfx.g.drawLine(x1, y1, x2, y2)

    @staticmethod
    def set_font(font):
        Gfx.font = font

    @staticmethod
    def draw_chars(chars, start, count, x, y, anchor):
        if (anchor & 0x1) != 0:
            x -= Gfx.font.chars_width(chars, start, count) // 2  # width >= 0: integer division
        elif (anchor & 0x8) != 0:
            x -= Gfx.font.chars_width(chars, start, count)
        i = start + count
        j = x
        for pos in range(start, i):
            ch = chars[pos]
            ch_w = Gfx.font.char_width(ch)
            Gfx.font.draw_char(ch, j, y)
            j += ch_w

    @staticmethod
    def draw_string(text, x, y, anchor):
        Gfx.draw_chars(list(text), 0, len(text), x, y, anchor)

    @staticmethod
    def make_crc_table():  # CRC-32 table, polynomial 0xEDB88320
        Gfx.crc_table = [0] * 256
        for b in range(256):
            i = b
            bits = 8
            while True:
                bits -= 1
                if bits < 0:
                    break
                if (i & 0x1) != 0:
                    i = i32(0xEDB88320 ^ ushr32(i, 1))
                    continue
                i = ushr32(i, 1)
            Gfx.crc_table[b] = i

    @staticmethod
    def crc32(data, pos, count):  # CRC-32
        if Gfx.crc_table is None:
            Gfx.make_crc_table()
        i = -1
        while True:
            count -= 1
            if count < 0:
                break
            # the original: a[(i ^ bytes[p++]) & 0xFF] ^ i >>> 8 ; the byte is signed but only & 0xFF matters
            i = i32(Gfx.crc_table[(i ^ data[pos]) & 0xFF] ^ ushr32(i, 8))
            pos += 1
        return (i ^ 0xFFFFFFFF) & 0xFFFFFFFF

    # static initializer builds two byte arrays and throws them away (dead code).
