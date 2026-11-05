""", part of GameCanvas: drawing primitives: text, boxes, frames, numbers, soft keys, descriptions.

A mixin of GameCanvas (pow/game/game_canvas.py); the methods keep their `# :FROM-TO`
comments. `GameCanvas` below is the real class, set by game_canvas.py once it exists.
"""

import config
from pow.game import consts
from pow.game.gfx import Gfx
from pow.game.structs import Rect
from pow.midp import canvas
from pow.midp.jint import i16, idiv, imod



GameCanvas = None   # set by pow/game/game_canvas.py


class DrawMixin:
    @staticmethod
    def draw_text_left(x, y, text):
        if text is not None:
            Gfx.draw_string(text, x, y, 0)

    @staticmethod
    def draw_text_centred(x, y, text):
        if text is not None:
            Gfx.draw_string(text, x, y, 1)

    def draw_view_region(self, image, x, y, w, h, src_x, src_y):
        GameCanvas.draw_region(x, y, w, h, image, src_x, src_y)

    @staticmethod
    def draw_text(x, y, text):
        Gfx.draw_string(text, x, y, 0)

    def draw_view_background(self):
        if GameCanvas.screen_fill == 0:
            self.fill_view(0, 0, 0)
            self.draw_view_region(GameCanvas.images[7], GameCanvas.view_x, GameCanvas.view_y, GameCanvas.view_size.x, GameCanvas.view_size.y, GameCanvas.view_offset.x, GameCanvas.view_offset.y)
            return
        if GameCanvas.screen_fill == 1:
            self.fill_view(0, 0, 0)
            return
        if GameCanvas.screen_fill == 2:
            self.fill_view(255, 255, 255)

    def fill_view(self, r, g, b):
        Gfx.fill_rect(GameCanvas.view_x, GameCanvas.view_y, GameCanvas.view_size.x, GameCanvas.view_size.y, GameCanvas.rgb(r, g, b))

    @staticmethod
    def fill_screen(color):
        Gfx.fill_rect(0, 0, GameCanvas.screen_w, GameCanvas.screen_h, color)

    def draw_title(self):  # title screen
        if GameCanvas.images[30] is None:
            return
        GameCanvas.draw_region(0, 0, GameCanvas.canvas_size.x, GameCanvas.canvas_size.y, GameCanvas.images[30], 0, 0)
        # : no copyright line of the original publisher under the
        # title
        if GameCanvas.title_logo is None:
            GameCanvas.title_logo = self.load_image(GameCanvas.scr_ui.get(42))
        if GameCanvas.frame % 6 < 3 and GameCanvas.state == 0:
            GameCanvas.draw_region(GameCanvas.view_cx - 55 + GameCanvas.view_x, GameCanvas.canvas_size.y - 60, 110, 14, GameCanvas.title_logo, 0, 0)

    def draw_image_file(self, name, x, y, w, h, src_x, src_y):
        image = self.load_image(name)
        if image is not None:
            GameCanvas.draw_region(x, y, w, h, image, src_x, src_y)

    def draw_menu_background(self, mode):  # menu background into ct[7]
        if mode == 1:
            return
        Gfx.set_graphics(GameCanvas.buffer_g)
        GameCanvas.images[11] = self.load_image(GameCanvas.scr_ui.get(60))
        GameCanvas.images[12] = self.load_image(GameCanvas.scr_ui.get(61))
        GameCanvas.images[16] = self.load_image(GameCanvas.scr_ui.get(63))
        GameCanvas.images[9] = self.load_image(GameCanvas.scr_ui.get(59))
        tile_w = GameCanvas.images[9].getWidth()
        tile_h = GameCanvas.images[9].getHeight()
        b = 0
        while b * tile_h < GameCanvas.canvas_size.y + tile_h:
            for col in range(4):
                GameCanvas.draw_region_at(GameCanvas.images[9], 0, 0, (b & 0x1) * -31 + col * tile_w, b * tile_h, tile_w, tile_h)
            b += 1
        # the original: (W - w) * b / 2 and H / 2 * b % 2 - all operands >= 0, so integer division
        for b in range(4):
            GameCanvas.draw_region_at(GameCanvas.images[12], 0, 0, (GameCanvas.canvas_size.x - GameCanvas.images[12].getWidth()) * b // 2, GameCanvas.canvas_size.y // 2 * b % 2,
                         GameCanvas.images[12].getWidth(), GameCanvas.images[12].getHeight())
        for b in range(4):
            GameCanvas.draw_region_at(GameCanvas.images[11], 0, 0, GameCanvas.canvas_size.x // 2 * b % 2, (GameCanvas.canvas_size.y - GameCanvas.images[11].getHeight()) * b // 2,
                         GameCanvas.images[11].getWidth(), GameCanvas.images[11].getHeight())
        GameCanvas.draw_region_at(GameCanvas.images[16], 0, 0, (GameCanvas.canvas_size.x >> 1) - GameCanvas.images[16].getWidth() // 2, 0,
                     GameCanvas.images[16].getWidth(), GameCanvas.images[16].getHeight())
        GameCanvas.images[11] = None
        GameCanvas.images[12] = None
        GameCanvas.images[16] = None
        GameCanvas.images[9] = None
        Gfx.set_graphics(GameCanvas.screen_g)

    @staticmethod
    def draw_region(x, y, w, h, image, src_x, src_y):
        Gfx.draw_image_part(image, x, y, w, h, src_x, src_y)

    def draw_map_region(self, image, x, y, w, h, src_x, src_y):
        clip_top = y
        clip_top = min(clip_top, 0)
        clip_bottom = GameCanvas.view_size.y - y - h
        clip_bottom = min(clip_bottom, 0)
        clip_left = x
        clip_left = min(clip_left, 0)
        clip_right = GameCanvas.view_size.x - x - w
        clip_right = min(clip_right, 0)
        if h + clip_top + clip_bottom > 0 and w + clip_left + clip_right > 0:
            GameCanvas.draw_region(x + GameCanvas.view_x - clip_left, y - clip_top + GameCanvas.view_y, w + clip_left + clip_right, h + clip_top + clip_bottom,
                         image, src_x - clip_left, src_y - clip_top)

    @staticmethod
    def draw_region_at(image, src_x, src_y, x, y, w, h):
        Gfx.draw_image_part(image, x, y, w, h, src_x, src_y)

    @staticmethod
    def draw_text_centred_at(text, y, view_x):  # centred text
        y += 2
        Gfx.draw_string(text, GameCanvas.view_cx + GameCanvas.view_x + view_x, y + GameCanvas.view_y, 1)

    def draw_text_at(self, text, y, unused):
        GameCanvas.draw_text_centred_at(text, y, 0)

    @staticmethod
    def draw_view_text_centred(text, x, y):
        Gfx.draw_string(text, x + GameCanvas.view_x, y + GameCanvas.view_y, 1)

    @staticmethod
    def draw_view_text(text, x, y):
        Gfx.draw_string(text, x + GameCanvas.view_x, y + GameCanvas.view_y, 0)

    def draw_box(self, x, y, w, h, selected):
        GameCanvas.draw_frame_box(x, y, w, h, 0, 5263440, 16777215, selected)

    @staticmethod
    def draw_frame_box(x, y, w, h, fill, outer, inner, framed):
        rect = Rect(0, 0, 0, 0)
        if framed:
            rect.x = x - 2
            rect.w = w + 4
            rect.y = y - 1
            rect.h = h + 2
            Gfx.draw_rect(rect.x, rect.y, rect.w, rect.h, inner)
            rect.x += 1
            rect.w -= 2
            rect.y -= 1
            rect.h += 2
            Gfx.draw_rect(rect.x, rect.y, rect.w, rect.h, inner)
        rect.x = x - 1
        rect.w = w + 2
        rect.y = y
        rect.h = h
        Gfx.draw_rect(rect.x, rect.y, rect.w, rect.h, outer)
        rect.x += 1
        rect.w -= 2
        rect.y -= 1
        rect.h += 2
        Gfx.draw_rect(rect.x, rect.y, rect.w, rect.h, outer)
        rect.y += 1
        rect.h -= 2
        Gfx.fill_rect(rect.x, rect.y, rect.w, rect.h, fill)

    @staticmethod
    def rgb(r, g, b):
        return (r & 0xFF) << 16 | (g & 0xFF) << 8 | b & 0xFF

    @staticmethod
    def draw_auto_badge():
        """(pow/game/autopilot.py): the AUTO button in the bottom-left corner of the map
        (the corner is empty on the map; a click on it, Tab or F toggles): white while the
        auto-hunt is on, grey while it is off (config.AUTO_BUTTON: only while it is on)."""
        from pow.game.autopilot import Autopilot
        if GameCanvas.state != 3 or GameCanvas.popups.kind != 0:
            return
        if not (Autopilot.on or config.AUTO_BUTTON):
            return
        Gfx.fill_rect(0, GameCanvas.screen_h - 17, 48, 17, 0)
        Gfx.set_font(GameCanvas.font_white if Autopilot.on else GameCanvas.font_gray)
        Gfx.draw_string("AUTO", 24, GameCanvas.screen_h - 17, 1)

    @staticmethod
    def draw_softkeys(left, right):  # soft-key captions
        if GameCanvas.popups.kind != 0:
            return
        key_w = GameCanvas.softkey_bg.getWidth()
        key_h = GameCanvas.softkey_bg.getHeight()
        str_ = ""
        left_hint, right_hint = canvas.key_hints()   # config.KEY_HINTS
        if left != -1:
            Gfx.set_font(GameCanvas.font_white)
            Gfx.draw_image(GameCanvas.softkey_bg, 0, GameCanvas.screen_h - key_h)
            text_w = len(str_ + left_hint + consts.softkey_labels[left]) * 10
            extra = text_w + 4 - GameCanvas.softkey_bg.getWidth()
            if extra > 0:
                Gfx.fill_rect(key_w - 8, GameCanvas.screen_h - key_h + 2, 8, 13, 0)
                Gfx.draw_image(GameCanvas.softkey_bg, extra, GameCanvas.screen_h - key_h)
                Gfx.fill_rect(extra, GameCanvas.screen_h - key_h + 2, 8, 13, 0)
                Gfx.draw_string(str_ + left_hint + consts.softkey_labels[left], (key_w + extra) // 2, GameCanvas.screen_h - key_h, 1)
            else:
                Gfx.draw_string(str_ + left_hint + consts.softkey_labels[left], key_w // 2, GameCanvas.screen_h - key_h, 1)
        if right != -1:
            Gfx.set_font(GameCanvas.font_white)
            Gfx.draw_image(GameCanvas.softkey_bg, GameCanvas.screen_w - key_w - 0, GameCanvas.screen_h - key_h)
            text_w = len(str_ + right_hint + consts.softkey_labels[right]) * 10
            extra = text_w + 15 - GameCanvas.softkey_bg.getWidth()
            if extra > 0:
                Gfx.fill_rect(GameCanvas.screen_w - key_w - 0, GameCanvas.screen_h - key_h + 2, 8, 13, 0)
                Gfx.draw_image(GameCanvas.softkey_bg, GameCanvas.screen_w - key_w - extra - 0, GameCanvas.screen_h - key_h)
                Gfx.fill_rect(GameCanvas.screen_w - extra - 0 - 8, GameCanvas.screen_h - key_h + 2, 8, 13, 0)
                Gfx.draw_string(str_ + right_hint + consts.softkey_labels[right], GameCanvas.screen_w - (key_w + extra) // 2 - 0, GameCanvas.screen_h - key_h, 1)
                return
            Gfx.draw_string(str_ + right_hint + consts.softkey_labels[right], GameCanvas.screen_w - key_w // 2 - 0, GameCanvas.screen_h - key_h, 1)

    def set_color(self, r, g, b):
        GameCanvas.fill_color = GameCanvas.rgb(r, g, b)

    @staticmethod
    def draw_line(x1, y1, x2, y2):
        Gfx.draw_line(x1, y1, x2, y2, GameCanvas.fill_color)

    _F_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                  "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                  "U", "V", "W", "X", "Y", "Z", "OK"]

    @staticmethod
    def draw_letter_grid(cursor, y):  # letter grid A..Z + OK
        left = GameCanvas.screen_cx - 71
        letters = GameCanvas._F_LETTERS
        Gfx.fill_rect(left, y, 142, 34, 0)
        Gfx.fill_rect(left + 123, y + 18, 19, 15, 255)
        if GameCanvas.frame % 4 < 2:
            if cursor == 26:
                Gfx.fill_rect(left + 123, y + 18, 19, 15, 16711680)
            else:
                Gfx.fill_rect(left + 2 + 10 * (cursor % 14), y + 1 + 17 * (cursor // 14), 10, 15, 16711680)
        Gfx.set_font(GameCanvas.font_white)
        for b in range(len(letters)):
            if b in {8, 26}:
                dx = 1
            else:
                dx = 0
            row = 17 * (b // 14)
            Gfx.draw_string(letters[b], left + 3 + b % 14 * 10 + dx, y + row, 0)

    def draw_arrow(self, direction, x, y):  # arrow from ct[17]
        if direction == 0:
            src_x = src_y = 0
            w, h = 10, 16
        elif direction == 1:
            src_x, src_y = 9, 0
            w, h = 10, 16
        elif direction == 2:
            src_x, src_y = 20, 0
            w, h = 16, 10
        elif direction == 3:
            src_x, src_y = 20, 9
            w, h = 16, 10
        else:
            return
        GameCanvas.draw_region(x + GameCanvas.view_x, y + GameCanvas.view_y, w, h, GameCanvas.images[17], src_x, src_y)

    def draw_big_number(self, value, x, y, with_commas):  # number from ct[19]
        if with_commas != 0:
            digits = 0
            rest = idiv(value, 10)
            x += 9
            while rest > 0:
                rest = idiv(rest, 10)
                digits += 1
                x += 9
                if digits % 3 == 0:
                    x += 4
        end_x = x
        b = 0
        while True:
            if b % 3 == 0 and b != 0:
                x -= 4
                self.draw_map_region(GameCanvas.images[19], x, y, 5, 14, 100, 0)
            x -= 9
            self.draw_map_region(GameCanvas.images[19], x, y, 10, 14, imod(value, 10) * 10, 0)
            b += 1
            value = idiv(value, 10)
            if value <= 0:
                return end_x

    def draw_rect_outline(self, x, y, w, h, r, g, b):  # rectangle outline
        self.set_color(r, g, b)
        GameCanvas.draw_line(x, y, x + w - 1, y)
        GameCanvas.draw_line(x, y + 1, x, y + h - 1)
        GameCanvas.draw_line(x + w - 1, y, x + w - 1, y + h - 1)
        GameCanvas.draw_line(x + 1, y + h - 1, x + w - 2, y + h - 1)

    def draw_round_outline(self, x, y, w, h, r, g, b):  # outline, round corners
        self.set_color(r, g, b)
        GameCanvas.draw_line(x + 1, y, x + w - 2, y)
        GameCanvas.draw_line(x, y + 1, x, y + h - 2)
        GameCanvas.draw_line(x + w - 1, y + 1, x + w - 1, y + h - 2)
        GameCanvas.draw_line(x + 1, y + h - 1, x + w - 2, y + h - 1)

    def draw_selection(self, x, y, w, h, r, g, b):  # selection frame
        self.draw_round_outline(x, y, w, h, r, g, b)
        self.draw_dot(x + 1, y + 1)
        self.draw_dot(x + w - 2, y + 1)
        self.draw_dot(x + 1, y + h - 2)
        self.draw_dot(x + w - 2, y + h - 2)

    def draw_dot(self, x, y):
        GameCanvas.draw_line(x, y, x + 1, y + 1)

    def fill_screen_rgb(self, r, g, b):  # fill the screen
        Gfx.fill_rect(0, 0, GameCanvas.canvas_size.x, GameCanvas.canvas_size.y, GameCanvas.rgb(r, g, b))

    def draw_skip_key(self, unused):  # soft key "Skip"
        GameCanvas.draw_softkeys(0, -1)

    def draw_small_number(self, value, x, y):  # small number, ct[20]
        self.draw_image_part(value, x, y, 9, 12, GameCanvas.images[20], 0, 0, 0)

    def draw_image_part(self, value, x, y, w, h, image,
                    src_x, src_y, gap):  # number from a digit strip
        if value < 0 or image is None:
            return
        x -= w
        if value > 0:
            while value > 0:
                sx = src_x + w * (value % 10)
                GameCanvas.draw_region(x, y, w, h, image, sx, src_y)
                value //= 10
                x -= w + gap
            return
        GameCanvas.draw_region(x, y, w, h, image, src_x, src_y)

    def draw_empty_slot(self, x, y):  # empty 30x30 item slot
        rect = Rect(x + 1, y + 1, 28, 28)
        self.draw_round_outline(x, y, 30, 30, 80, 80, 80)
        Gfx.fill_rect(rect.x, rect.y, rect.w, rect.h, 0)

    def draw_grey_frame(self, x, y, w, h):  # grey frame, black inside
        rect = Rect(x + 1, y + 1, w - 2, h - 2)
        self.draw_round_outline(x, y, w, h, 152, 152, 152)
        Gfx.fill_rect(rect.x, rect.y, rect.w, rect.h, 0)

    @staticmethod
    def fill_rect(rect, color):  # fill rect
        if rect is not None:
            Gfx.fill_rect(rect.x, rect.y, rect.w, rect.h, color)

    @staticmethod
    def outline_rect(rect, color):  # outline rect
        if rect is not None:
            Gfx.draw_rect(rect.x, rect.y, rect.w, rect.h, color)

    @staticmethod
    def draw_filled_rect(rect, outline, fill):
        Gfx.fill_rect(rect.x, rect.y, rect.w, rect.h, fill)
        Gfx.draw_rect(rect.x, rect.y, rect.w, rect.h, outline)

    def draw_small_digit(self, x, y, digit):  # small digit from ct[20]
        self.draw_map_region(GameCanvas.images[20], x, y, 9, 12, digit * 9, 0)

    def draw_gold_box(self):  # gold box
        widths = [7, 14, 21, 32, 39, 46, 57, 64, 71, 82]
        rest = GameCanvas.hero.gold
        self.draw_box(GameCanvas.view_cx - 70, GameCanvas.view_cy - 80 + GameCanvas.view_y, 140, 22, False)
        b = 0
        while b < 9:
            rest = idiv(rest, 10)
            if rest == 0:
                break
            b += 1
        self.draw_big_number(GameCanvas.hero.gold, GameCanvas.view_cx + (widths[b] >> 1) + 16 - GameCanvas.view_x, GameCanvas.view_cy - 76, 0)
        self.draw_map_region(GameCanvas.images[32], GameCanvas.view_cx - 69 - GameCanvas.view_x, GameCanvas.view_cy - 80, GameCanvas.images[32].getWidth(), GameCanvas.images[32].getHeight(), 0, 0)

    def draw_description(self, what, x, y, w, h):  # description of item / skill
        hero = GameCanvas.hero
        info = GameCanvas.info_box
        attack = defense = hp = mp = enchant = min_level = 0
        str_ = ""
        info.rect.x = x
        info.rect.y = y
        info.rect.w = w
        info.rect.h = h
        info.text = ""
        if what > 999:
            if what < 1100:
                it = hero.equipped[what - 1000]
            elif what < 1200:
                it = hero.backpack[what - 1100]
            else:
                it = None
            if it is not None:
                min_level = GameCanvas.set_item_name(it.id)
                attack = it.attack
                defense = it.defense
                hp = it.hp
                mp = it.mp
                enchant = i16(it.enchant)
                str_ = GameCanvas.special_suffix(it.id)
            elif what < 2000:
                info.text = GameCanvas.describe_potion(hero.quick_slots[what - 1200].item)
            else:
                info.text = self.describe_skill(what - 2000)
        if info.text != "":
            if str_ != "":
                info.text += str_
            if attack != 0:
                info.text += " / ATK+" + str(attack)
            if defense != 0:
                info.text += " / DEF+" + str(defense)
            if hp != 0:
                info.text += " / HP+" + str(hp)
            if mp != 0:
                info.text += " / MP+" + str(mp)
            if enchant != 0:
                info.text += " / Enchanted Lv" + str(enchant)
            if min_level != 0:
                info.text += " / Available at Lv" + str(min_level)
            GameCanvas.text_width = GameCanvas.measure_text(info.text)
            if GameCanvas.text_width > w - 2:
                info.shown = 1
                info.text_x = i16(x + 20)
                return
            info.shown = 0
            info.text_x = i16(x + 1)

    def describe_skill(self, skill):  # skill description
        text = ""
        skill -= 12
        if skill < 0 or skill > 18:
            return text
        utf = self.edat_bytes(54, skill)
        name = GameCanvas.read_utf(utf, 0, len(utf))
        if GameCanvas.hero.skill_levels[skill] != 0:
            utf = self.edat_bytes(54, skill + 19)
            text = name + " / Lv" + str(GameCanvas.hero.skill_levels[skill]) + " " + GameCanvas.read_utf(utf, 0, len(utf))
        else:
            text = name + " / (Not Available)"
        return text

    # ---- Blacksmith helpers ----------------------------------------------------------------

    def draw_panel(self, x, y, w, h):
        GameCanvas.draw_frame_box(x + 1, y + 1, w - 2, h - 2, 0, 0, 10000536, True)

    def draw_centred_box(self, y, w, h):  # centred box, returns its x
        box_x = 240 - w >> 1
        self.draw_panel(box_x, y, w, h)
        return box_x

    def draw_gold_amount(self, gold, y):  # gold box with amount paramInt1
        text_x = self.draw_centred_box(y, 200, 22)
        b = 0
        rest = gold
        while True:
            b += 1
            rest = idiv(rest, 10)
            if not rest > 0:
                break
        text_x += 100
        text_w = b * 7 + (b - 1) // 3 * 4 + 12 + 3
        text_x -= text_w >> 1
        y += 6
        self.draw_number_commas(gold, text_x + text_w + 10, y)
        self.draw_map_region(GameCanvas.images[32], GameCanvas.view_cx - 69, y - 5, GameCanvas.images[32].getWidth(), GameCanvas.images[32].getHeight(), 0, 0)

    def draw_hero_gold(self, y):
        self.draw_gold_amount(GameCanvas.hero.gold, y)

    def draw_number_commas(self, value, x, y):  # number with thousands commas
        b = 0
        while True:                         # a comma before every 3rd digit
            if b != 0 and b % 3 == 0:
                x -= 4
                GameCanvas.draw_region(x, y, 5, 14, GameCanvas.images[19], 100, 0)
            x -= 10
            GameCanvas.draw_region(x, y, 10, 14, GameCanvas.images[19], imod(value, 10) * 10, 0)
            b += 1
            value = idiv(value, 10)
            if not value > 0:
                break

    def draw_digit(self, digit, x, y):  # one digit of ct[19]
        self.draw_map_region(GameCanvas.images[19], x, y, 10, 14, 10 * digit, 0)

    def draw_clock(self, x, y, secs):  # mission clock mm:ss
        digit_x = [0, 9, 25, 34]
        digits = [idiv(secs, 600) % 10, idiv(secs, 60) % 10, secs % 60 // 10, secs % 10]
        for b in range(4):
            self.draw_digit(digits[b], x + digit_x[b] + 10, y)
        self.draw_map_region(GameCanvas.images[19], x + 20 + 10, y, 4, 14, 115, 0)
