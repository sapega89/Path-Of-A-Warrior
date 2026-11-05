"""m.java - the drawing of Gamevil Live (PHASE_7) and its registration record. Literal port.

as.a = m(); ag.L() calls as.aK() -> m.a() every frame while bV == 11. as.ho picks the screen.
"""
import config
from pow.game.game_canvas import GameCanvas
from pow.game.gfx import Gfx
from pow.game.live import B5, Live
from pow.midp.rms import RecordStore


class LiveScreen(Live):

    def draw_live_screen(self):  # m.java:4-56
        if Live.screen_redraw:
            GameCanvas.menus.draw_menu_frame()
            if Live.title is not None:
                Gfx.set_font(GameCanvas.font_white)
                GameCanvas.draw_text_centred(GameCanvas.screen_w // 2, 2, Live.title)
            Live.screen_redraw = False
        h = {1: self.draw_list_screen, 2: self.draw_safe, 3: self.draw_safe_amount, 4: self.draw_grid, 5: self.draw_buy_categories, 6: self.draw_buy_kinds,
             7: self.draw_buy_enchants, 8: self.draw_buy_lots, 9: self.draw_sell_price, 10: self.draw_cancel_sell, 11: self.draw_sale_list, 12: LiveScreen.draw_waiting,
             13: self.draw_registration}.get(Live.live_screen)
        if h is not None:
            h()
        if GameCanvas.popups.kind != 0:
            GameCanvas.popups.draw_popup()

    def draw_list_screen(self):  # m.java:58-61  (list menu)
        self.draw_list()
        GameCanvas.draw_softkeys(-1, 2)

    def draw_safe(self):  # m.java:63-77  (Safe: Local <-> Server)
        self.draw_caption_box("Local", 85)
        self.draw_gold_amount(GameCanvas.hero.gold, 108)
        GameCanvas.draw_region(85, 138, 70, 21, GameCanvas.images[7], 45, 138)
        if Live.flags[15] == 0:
            GameCanvas.draw_region(85, 138, 30, 21, Live.arrow_image, 0, 0)
            GameCanvas.draw_region(126, 139, 28, 19, Live.arrow_image, 30, 18)
        else:
            GameCanvas.draw_region(86, 139, 28, 19, Live.arrow_image, 30, 0)
            GameCanvas.draw_region(125, 138, 30, 21, Live.arrow_image, 0, 20)
        self.draw_caption_box("Server", 167)
        self.draw_gold_amount(Live.safe_gold, 190)
        GameCanvas.draw_softkeys(-1, 2)

    def draw_sell_price(self):  # m.java:79-101  (Sell: the price)
        from pow.game.menus import Menus
        lines = ["Enter your selling", "price. " + str(Live.flags[4]) + "% of total", "will go to taxes."]
        label = "EnchantLv"
        line_y = 101
        Gfx.set_font(GameCanvas.font_white)
        for i in range(3):
            Live.draw_text_centred_in(lines[i], 0, line_y, 240)
            line_y += 13
        Live.draw_item_cell(Live.shown_item, 39, 180, False)
        self.draw_panel(71, 183, 130, 17)
        Gfx.set_font(GameCanvas.font_white)
        Menus.item_name(Live.shown_item)
        Live.draw_text_centred_in(label + str(Live.enchant), 141, 180, 0)
        self.draw_input_box(45, 210, 150, 22)
        Gfx.set_font(GameCanvas.font_black)
        Live.draw_text_centred_in(GameCanvas.format_thousands(Live.values[14]), 0, 212, 240)
        items = GameCanvas.hero.backpack
        if config.ORIG_BUG["B11"] and Live.flags[7] == 1:   # ORIG-BUG B11: sold from the warehouse
            items = Live.warehouse
        GameCanvas.describe_shop_item(items[GameCanvas.cursor[18]], True, -1)
        GameCanvas.info_box.rect.y = 155 - GameCanvas.view_y
        if config.WIDE_DESC:            # PORT-EXTRA: the tall box under the price box, not over the item
            GameCanvas.info_box.rect.y = 238 - GameCanvas.view_y
        GameCanvas.menus.draw_description_strip()
        GameCanvas.draw_softkeys(7, 2)

    def draw_cancel_sell(self):  # m.java:103-120  (Cancel Sell: my 5 lots)
        from pow.game.menus import Menus
        GameCanvas.draw_softkeys(-1, 2)
        self.draw_hero_gold(83)
        i = 42
        for b in range(5):
            Live.draw_item_cell(Live.lots[b].id, i, 115, b == Live.selected_slot)
            i += 32
        i = self.draw_centred_box(160, 200, 48)
        if Live.lots[Live.selected_slot].id > 0:
            Gfx.set_font(GameCanvas.font_white)
            Live.draw_text_centred_in(Menus.item_name(Live.lots[Live.selected_slot].id), i, 164, 200)
            Live.draw_text_centred_in("Price " + GameCanvas.format_thousands(Live.prices[Live.selected_slot]), i, 178, 200)
            GameCanvas.describe_shop_item(Live.lots[Live.selected_slot], False, -1)

    def draw_sale_list(self):  # m.java:122-148  (Sale List / Gift List)
        from pow.game.menus import Menus
        sold_lines = ["Listed Items", "has been sold."]
        gift_lines = ["Listed Items", "has been recieved."]
        line = sold_lines[0] if Live.list_kind == 0 else gift_lines[0]
        Gfx.set_font(GameCanvas.font_white)
        Live.draw_text_centred_in(line, 0, 100, 240)
        line = sold_lines[1] if Live.list_kind == 0 else gift_lines[1]
        Live.draw_text_centred_in(line, 0, 113, 240)
        i = 42
        for b in range(5):
            Live.draw_item_cell(Live.lots[b].id, i, 130, b == Live.selected_slot)
            i += 32
        i = self.draw_centred_box(166, 150, 45) + 25
        if Live.lots[Live.selected_slot].id > 0:
            Gfx.set_font(GameCanvas.font_white)
            if Live.list_kind == 0:
                Live.draw_text_centred_in(Menus.item_name(Live.lots[Live.selected_slot].id), i, 170, 100)
                Live.draw_text_centred_in("Price " + GameCanvas.format_thousands(Live.prices[Live.selected_slot]), i, 183, 100)
                Live.draw_text_centred_in("EnchantLv " + str(Live.lots[Live.selected_slot].enchant), i, 196, 100)
                return
            Live.draw_text_centred_in(Live.gift_from[Live.selected_slot], i, 170, 100)
            Live.draw_text_centred_in(Menus.item_name(Live.lots[Live.selected_slot].id), i, 183, 100)
            GameCanvas.describe_shop_item(Live.lots[Live.selected_slot], False, -1)
            if config.WIDE_DESC:        # PORT-EXTRA: the tall box under the gift box (y 166..211)
                GameCanvas.info_box.rect.y = 216 - GameCanvas.view_y
            GameCanvas.menus.draw_description_strip()

    @staticmethod
    def draw_waiting():  # m.java:150-156  (waiting: no answer for ~10 frames after the request -> "failed")
        if GameCanvas.popups.kind == 0 and not Live.busy:
            Live.anim_ticks += 1
            if Live.anim_ticks - 1 > 10:
                Live.close_target = 3
                GameCanvas.popups.show(29)
                Live.anim_ticks = 0

    def draw_registration(self):  # m.java:158-208  (registration: UserID, then the password)
        i = GameCanvas.screen_h // 2 - 45
        if Live.reg_step == 0:
            Gfx.set_font(GameCanvas.font_white)
            Gfx.draw_string("Please enter", GameCanvas.screen_w // 2, i, 1)
            Gfx.draw_string("your password.", GameCanvas.screen_w // 2, i + 15, 1)
            Gfx.draw_string("(4-12 numbers)", GameCanvas.screen_w // 2, i + 30, 1)
            Gfx.fill_rect(GameCanvas.screen_w // 2 - 65, i + 65, 130, 20, 13421772)
            Gfx.set_font(GameCanvas.font_black)
            Gfx.draw_string(Live.password, GameCanvas.screen_w // 2, i + 67, 1)
            if config.REG_KEYBOARD:          # PORT-EXTRA: 0..9 + OK under the box (key_grid.py)
                Live.pwd_grid.draw(i + 90)
            if Live.blink and not (B5 and Live.busy):     # ORIG-BUG B5: not while the 530 is on its way
                Live.blink_count += 1
                if Live.blink_count - 1 > 2:
                    Live.reg_step = 1
                    GameCanvas.popups.show(29)
                    Live.blink_count = 0
                    Live.blink = False
            self.draw_view_region(GameCanvas.images[7], 0, GameCanvas.screen_h - 20, GameCanvas.screen_w, 20, 0, GameCanvas.screen_h - 20)
            right_key = 2
            if len(Live.password) > 0:
                right_key = 10
            if len(Live.password) >= 4:
                GameCanvas.draw_softkeys(8, right_key)
                return
            GameCanvas.draw_softkeys(-1, right_key)
        elif Live.reg_step == 1:
            if GameCanvas.popups.kind == 0:
                Live.blink = False
                Gfx.set_font(GameCanvas.font_white)
                Gfx.draw_string("In order to access", GameCanvas.screen_w // 2, i - 30, 1)
                Gfx.draw_string("Gamevil Live", GameCanvas.screen_w // 2, i - 10, 1)
                Gfx.draw_string("you must register first.", GameCanvas.screen_w // 2, i + 10, 1)
                Gfx.draw_string("Please enter a UserID.", GameCanvas.screen_w // 2, i + 30, 1)
                Gfx.draw_string("(4-12 characters)", GameCanvas.screen_w // 2, i + 50, 1)
                Gfx.fill_rect(GameCanvas.screen_w // 2 - 60, i + 70, 120, 20, 13421772)
                Gfx.set_font(GameCanvas.font_black)
                Gfx.draw_string(GameCanvas.name_buf.get_text(), GameCanvas.screen_w // 2, i + 72, 1)
                if config.REG_KEYBOARD:      # PORT-EXTRA: the letters + a row of digits (key_grid.py)
                    Live.id_grid.draw(i + 90)
                else:
                    GameCanvas.draw_letter_grid(GameCanvas.letter_cursor, i + 90)
            self.draw_view_region(GameCanvas.images[7], 0, GameCanvas.screen_h - 20, GameCanvas.screen_w, 20, 0, GameCanvas.screen_h - 20)
            j = GameCanvas.name_buf.length()
            bool_ = 1                        # sic: (j >= 4 && j <= 12) ? true : true
            right_key2 = 2 if j == 0 else 10
            GameCanvas.draw_softkeys(bool_, right_key2)

    def draw_buy_categories(self):  # m.java:210-213  (Buy: categories)
        self.draw_hero_gold(Live.values[15])
        self.draw_list_screen()

    def draw_buy_kinds(self):  # m.java:215-224  (Buy: kinds)
        i = 20 + (255 - 64 + GameCanvas.cursor[6] >> 1)
        self.draw_hero_gold(i)
        i += 32
        self.draw_caption_box(Live.category_names[Live.category], i)
        i += 32
        GameCanvas.menus.draw_item_grid(i, None, Live.kind_items[Live.category])
        GameCanvas.draw_softkeys(-1, 2)

    def draw_buy_enchants(self):  # m.java:226-254  (Buy: how many lots at each enchant level)
        i_ = 0
        self.draw_hero_gold(47)
        i = self.draw_centred_box(89, 200, 32)
        Gfx.set_font(GameCanvas.font_white)
        Live.draw_text_centred_in(Live.category_names[Live.category], i, 99, 167)
        Live.draw_item_cell(Live.kind_items[Live.category][Live.kind], i + 167, 91, False)
        j = 131
        enchant = 0
        for row in range(2):
            i = 32
            for b in range(5):
                Live.draw_item_cell(0, i, j, enchant == Live.enchant)
                Gfx.draw_image_anchored(Live.level_image, i + 1, j + 8, 0)
                self.draw_number_commas(enchant, i + 27, j + 6)
                Live.draw_item_cell(0, i, j + 28 + 1, enchant == Live.enchant)
                self.draw_number_commas(Live.counts[15 - enchant] // 10, i + 13, j + 28 + 8)
                self.draw_number_commas(Live.counts[15 - enchant] % 10, i + 22, j + 28 + 8)
                i += 37
                enchant += 1
            j += 60
        del i_
        GameCanvas.draw_softkeys(-1, 2)

    def draw_buy_lots(self):  # m.java:256-276  (Buy: the lots of a page)
        if config.ORIG_BUG["B10"]:     # ORIG-BUG B10: centre gold + box + grid + strip, grid above the strip
            j = 20 + (255 - (84 + GameCanvas.cursor[6] + 10 + 32) >> 1)
        else:
            j = 20 + (255 - 84 + GameCanvas.cursor[6] + 10 + 32 >> 1)
        self.draw_hero_gold(j)
        j += 42
        i = self.draw_centred_box(j, 200, 32)
        Gfx.set_font(GameCanvas.font_white)
        Live.draw_text_centred_in(Live.category_names[Live.category], i, j + 10, 157)
        i += 157
        Live.draw_item_cell(Live.shown_item, i - 15, j + 9 - 7, False)
        if Live.category != 2:
            Gfx.draw_image_anchored(Live.level_image, i + 28 - 14, j + 11, 0)
            self.draw_number_commas(Live.enchant, i + 28 + 14, j + 9)
        j += 42
        GameCanvas.menus.draw_item_grid(j, Live.lots, None)
        GameCanvas.cursor[14] = 1
        GameCanvas.describe_shop_item(Live.lots[GameCanvas.cursor[18]], True, Live.prices[GameCanvas.cursor[18]])
        GameCanvas.menus.draw_description_strip()
        GameCanvas.draw_softkeys(-1, 2)

    @staticmethod
    def is_registered():  # m.java:278-285  (registered already?)
        try:
            rs = RecordStore.openRecordStore("gamevil_pow_regist", True)
            return rs.getNumRecords() != 0
        except Exception:
            return False

    @staticmethod
    def save_login():  # m.java:287-305  (keep UserID [0..12) and password [12..28))
        record = bytearray(28)
        chars = Live.password.encode("latin-1")
        for b in range(len(chars)):
            record[b] = chars[b]
        chars = Live.user_id.encode("latin-1")
        for b in range(len(chars)):
            record[12 + b] = chars[b]
        try:
            rs = RecordStore.openRecordStore("gamevil_pow_regist", True)
            if rs.getNumRecords() == 0:
                rs.addRecord(bytes(record), 0, len(record))
            rs.setRecord(1, bytes(record), 0, len(record))
        except Exception:
            return

    def load_login(self):  # m.java:307-320  (read it back: l = [0..12), m = [12..26))
        record = bytes(26)
        try:
            rs = RecordStore.openRecordStore("gamevil_pow_regist", False)
            if rs is None or rs.getNumRecords() < 1:
                Live.password = ""
                Live.user_id = ""
                return
            record = rs.getRecord(1)
        except Exception:
            pass
        Live.password = GameCanvas.cut_at_control(GameCanvas.read_utf(record, 0, 12))
        Live.user_id = GameCanvas.cut_at_control(GameCanvas.read_utf(record, 12, 26))

    def draw_safe_amount(self):  # m.java:322-341  (Safe: the amount)
        if GameCanvas.images[22] is None:
            GameCanvas.images[22] = self.load_image(GameCanvas.scr_ui.get(18))
        if GameCanvas.images[24] is None:
            GameCanvas.images[24] = self.load_image(GameCanvas.scr_ui.get(20))
        if Live.flags[15] == 0:
            Gfx.draw_image(GameCanvas.images[22], 107, 111)
        else:
            Gfx.draw_image(GameCanvas.images[24], 107, 111)
        Gfx.set_font(GameCanvas.font_white)
        Gfx.draw_string("Local", GameCanvas.screen_w // 2 - 44, 111, 1)
        Gfx.draw_string("Server", GameCanvas.screen_w // 2 + 50, 111, 1)
        Gfx.draw_string("How much do", GameCanvas.screen_w // 2, 131, 1)
        Gfx.draw_string("you want to move?", GameCanvas.screen_w // 2, 143, 1)
        self.draw_input_box(70, 163, 100, 20)
        Gfx.set_font(GameCanvas.font_black)
        Gfx.draw_string(GameCanvas.format_thousands(Live.values[14]), GameCanvas.screen_w // 2, 165, 1)
        GameCanvas.draw_softkeys(-1, 2)
        GameCanvas.popups.draw_ok(200)

    def draw_input_box(self, x, y, w, h):  # m.java:343-356  (input box)
        GameCanvas.input_box.w = w + 1
        GameCanvas.input_box.x = x - 1
        GameCanvas.input_box.h = h + 1
        GameCanvas.input_box.y = y - 1
        GameCanvas.outline_rect(GameCanvas.input_box, 0)
        GameCanvas.input_box.x += 1
        GameCanvas.input_box.y += 1
        GameCanvas.outline_rect(GameCanvas.input_box, 16777215)
        GameCanvas.input_box.w -= 1
        GameCanvas.input_box.h -= 1
        GameCanvas.fill_rect(GameCanvas.input_box, GameCanvas.rgb(192, 192, 192))

    def draw_grid(self):  # m.java:358-380  (Backpack / Warehouse grid)
        if Live.flags[7] == 0:
            caption = "Backpack"
            items = GameCanvas.hero.backpack
        else:
            caption = "Warehouse"
            items = Live.warehouse
        if config.ORIG_BUG["B9"]:      # ORIG-BUG B9: centre caption + grid + strip, grid above the strip
            i = 20 + (255 - (38 + GameCanvas.cursor[6] + 16 + 22) >> 1)
        else:
            i = 20 + (255 - 38 + GameCanvas.cursor[6] + 16 + 22 >> 1)
        self.draw_caption_box(caption, i)
        i += 38
        GameCanvas.menus.draw_item_grid(i, items, None)
        GameCanvas.cursor[14] = 0
        GameCanvas.describe_shop_item(items[GameCanvas.cursor[18]], True, -1)
        GameCanvas.menus.draw_description_strip()
        if Live.flags[7] == 0:
            GameCanvas.draw_softkeys(4, 2)
            return
        GameCanvas.draw_softkeys(3, 2)
