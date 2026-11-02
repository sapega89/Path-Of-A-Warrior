"""m.java - the drawing of Gamevil Live (PHASE_7) and its registration record. Literal port.

as.a = m(); ag.L() calls as.aK() -> m.a() every frame while bV == 11. as.ho picks the screen.
"""
from pow.game.game_canvas import GameCanvas
from pow.game.live import Live, B5
from pow.game.gfx import Gfx
from pow.midp.rms import RecordStore


class LiveScreen(Live):

    def a_v(self):  # m.java:4-56
        if Live.screen_redraw:
            GameCanvas.menus.e_v()
            if Live.title is not None:
                Gfx.a_Lg(GameCanvas.font_white)
                GameCanvas.b_IIT(GameCanvas.screen_w // 2, 2, Live.title)
            Live.screen_redraw = False
        h = {1: self.bj_v, 2: self.bk_v, 3: self.bu_v, 4: self.bv_v, 5: self.bq_v, 6: self.br_v,
             7: self.bs_v, 8: self.bt_v, 9: self.bl_v, 10: self.bm_v, 11: self.bn_v, 12: LiveScreen.bo_v,
             13: self.bp_v}.get(Live.live_screen)
        if h is not None:
            h()
        if GameCanvas.popups.kind != 0:
            GameCanvas.popups.c_v()

    def bj_v(self):  # m.java:58-61  (list menu)
        self.aD_v()
        GameCanvas.h_II(-1, 2)

    def bk_v(self):  # m.java:63-77  (Safe: Local <-> Server)
        self.c_TI("Local", 85)
        self.c_II(GameCanvas.hero.gold, 108)
        GameCanvas.a_IIIIMII(85, 138, 70, 21, GameCanvas.images[7], 45, 138)
        if Live.flags[15] == 0:
            GameCanvas.a_IIIIMII(85, 138, 30, 21, Live.arrow_image, 0, 0)
            GameCanvas.a_IIIIMII(126, 139, 28, 19, Live.arrow_image, 30, 18)
        else:
            GameCanvas.a_IIIIMII(86, 139, 28, 19, Live.arrow_image, 30, 0)
            GameCanvas.a_IIIIMII(125, 138, 30, 21, Live.arrow_image, 0, 20)
        self.c_TI("Server", 167)
        self.c_II(Live.safe_gold, 190)
        GameCanvas.h_II(-1, 2)

    def bl_v(self):  # m.java:79-101  (Sell: the price)
        from pow.game.menus import Menus
        arrayOfString = ["Enter your selling", "price. " + str(Live.flags[4]) + "% of total", "will go to taxes."]
        str1 = "EnchantLv"
        b1 = 101
        Gfx.a_Lg(GameCanvas.font_white)
        for b2 in range(3):
            Live.a_TIII(arrayOfString[b2], 0, b1, 240)
            b1 += 13
        Live.a_IIIZ(Live.shown_item, 39, 180, False)
        self.c_IIII(71, 183, 130, 17)
        Gfx.a_Lg(GameCanvas.font_white)
        Menus.c_I(Live.shown_item)
        Live.a_TIII(str1 + str(Live.enchant), 141, 180, 0)
        self.a_IIII(45, 210, 150, 22)
        Gfx.a_Lg(GameCanvas.font_black)
        Live.a_TIII(GameCanvas.n_I(Live.values[14]), 0, 212, 240)
        GameCanvas.a_LzZI(GameCanvas.hero.backpack[GameCanvas.cursor[18]], True, -1)
        GameCanvas.info_box.rect.y = 155 - GameCanvas.view_y
        GameCanvas.menus.k_v()
        GameCanvas.h_II(7, 2)

    def bm_v(self):  # m.java:103-120  (Cancel Sell: my 5 lots)
        from pow.game.menus import Menus
        GameCanvas.h_II(-1, 2)
        self.i_I(83)
        i = 42
        for b in range(5):
            Live.a_IIIZ(Live.lots[b].id, i, 115, b == Live.selected_slot)
            i += 32
        i = self.b_III(160, 200, 48)
        if Live.lots[Live.selected_slot].id > 0:
            Gfx.a_Lg(GameCanvas.font_white)
            Live.a_TIII(Menus.c_I(Live.lots[Live.selected_slot].id), i, 164, 200)
            Live.a_TIII("Price " + GameCanvas.n_I(Live.prices[Live.selected_slot]), i, 178, 200)
            GameCanvas.a_LzZI(Live.lots[Live.selected_slot], False, -1)

    def bn_v(self):  # m.java:122-148  (Sale List / Gift List)
        from pow.game.menus import Menus
        arrayOfString1 = ["Listed Items", "has been sold."]
        arrayOfString2 = ["Listed Items", "has been recieved."]
        s = arrayOfString1[0] if Live.list_kind == 0 else arrayOfString2[0]
        Gfx.a_Lg(GameCanvas.font_white)
        Live.a_TIII(s, 0, 100, 240)
        s = arrayOfString1[1] if Live.list_kind == 0 else arrayOfString2[1]
        Live.a_TIII(s, 0, 113, 240)
        i = 42
        for b in range(5):
            Live.a_IIIZ(Live.lots[b].id, i, 130, b == Live.selected_slot)
            i += 32
        i = self.b_III(166, 150, 45) + 25
        if Live.lots[Live.selected_slot].id > 0:
            Gfx.a_Lg(GameCanvas.font_white)
            if Live.list_kind == 0:
                Live.a_TIII(Menus.c_I(Live.lots[Live.selected_slot].id), i, 170, 100)
                Live.a_TIII("Price " + GameCanvas.n_I(Live.prices[Live.selected_slot]), i, 183, 100)
                Live.a_TIII("EnchantLv " + str(Live.lots[Live.selected_slot].enchant), i, 196, 100)
                return
            Live.a_TIII(Live.gift_from[Live.selected_slot], i, 170, 100)
            Live.a_TIII(Menus.c_I(Live.lots[Live.selected_slot].id), i, 183, 100)
            GameCanvas.a_LzZI(Live.lots[Live.selected_slot], False, -1)
            GameCanvas.menus.k_v()

    @staticmethod
    def bo_v():  # m.java:150-156  (waiting: no answer for ~10 frames after the request -> "failed")
        if GameCanvas.popups.kind == 0 and not Live.busy:
            Live.anim_ticks += 1
            if Live.anim_ticks - 1 > 10:
                Live.close_target = 3
                GameCanvas.popups.d_I(29)
                Live.anim_ticks = 0

    def bp_v(self):  # m.java:158-208  (registration: UserID, then the password)
        i = GameCanvas.screen_h // 2 - 45
        if Live.reg_step == 0:
            Gfx.a_Lg(GameCanvas.font_white)
            Gfx.a_TIII("Please enter", GameCanvas.screen_w // 2, i, 1)
            Gfx.a_TIII("your password.", GameCanvas.screen_w // 2, i + 15, 1)
            Gfx.a_TIII("(4-12 numbers)", GameCanvas.screen_w // 2, i + 30, 1)
            Gfx.b_IIIII(GameCanvas.screen_w // 2 - 65, i + 65, 130, 20, 13421772)
            Gfx.a_Lg(GameCanvas.font_black)
            Gfx.a_TIII(Live.password, GameCanvas.screen_w // 2, i + 67, 1)
            if Live.blink and not (B5 and Live.busy):     # ORIG-BUG B5: not while the 530 is on its way
                Live.blink_count += 1
                if Live.blink_count - 1 > 2:
                    Live.reg_step = 1
                    GameCanvas.popups.d_I(29)
                    Live.blink_count = 0
                    Live.blink = False
            self.a_MIIIIII(GameCanvas.images[7], 0, GameCanvas.screen_h - 20, GameCanvas.screen_w, 20, 0, GameCanvas.screen_h - 20)
            b1 = 2
            if len(Live.password) > 0:
                b1 = 10
            if len(Live.password) >= 4:
                GameCanvas.h_II(8, b1)
                return
            GameCanvas.h_II(-1, b1)
        elif Live.reg_step == 1:
            if GameCanvas.popups.kind == 0:
                Live.blink = False
                Gfx.a_Lg(GameCanvas.font_white)
                Gfx.a_TIII("In order to access", GameCanvas.screen_w // 2, i - 30, 1)
                Gfx.a_TIII("Gamevil Live", GameCanvas.screen_w // 2, i - 10, 1)
                Gfx.a_TIII("you must register first.", GameCanvas.screen_w // 2, i + 10, 1)
                Gfx.a_TIII("Please enter a UserID.", GameCanvas.screen_w // 2, i + 30, 1)
                Gfx.a_TIII("(4-12 characters)", GameCanvas.screen_w // 2, i + 50, 1)
                Gfx.b_IIIII(GameCanvas.screen_w // 2 - 60, i + 70, 120, 20, 13421772)
                Gfx.a_Lg(GameCanvas.font_black)
                Gfx.a_TIII(GameCanvas.name_buf.a_v(), GameCanvas.screen_w // 2, i + 72, 1)
                GameCanvas.f_II(GameCanvas.letter_cursor, i + 90)
            self.a_MIIIIII(GameCanvas.images[7], 0, GameCanvas.screen_h - 20, GameCanvas.screen_w, 20, 0, GameCanvas.screen_h - 20)
            j = GameCanvas.name_buf.b_v()
            bool_ = 1                        # sic: (j >= 4 && j <= 12) ? true : true
            b2 = 2 if j == 0 else 10
            GameCanvas.h_II(bool_, b2)

    def bq_v(self):  # m.java:210-213  (Buy: categories)
        self.i_I(Live.values[15])
        self.bj_v()

    def br_v(self):  # m.java:215-224  (Buy: kinds)
        i = 20 + (255 - 64 + GameCanvas.cursor[6] >> 1)
        self.i_I(i)
        i += 32
        self.c_TI(Live.category_names[Live.category], i)
        i += 32
        GameCanvas.menus.a_IAzAI(i, None, Live.kind_items[Live.category])
        GameCanvas.h_II(-1, 2)

    def bs_v(self):  # m.java:226-254  (Buy: how many lots at each enchant level)
        i_ = 0
        self.i_I(47)
        i = self.b_III(89, 200, 32)
        Gfx.a_Lg(GameCanvas.font_white)
        Live.a_TIII(Live.category_names[Live.category], i, 99, 167)
        Live.a_IIIZ(Live.kind_items[Live.category][Live.kind], i + 167, 91, False)
        j = 131
        b2 = 0
        for b1 in range(2):
            i = 32
            for b in range(5):
                Live.a_IIIZ(0, i, j, b2 == Live.enchant)
                Gfx.a_MIII(Live.level_image, i + 1, j + 8, 0)
                self.h_III(b2, i + 27, j + 6)
                Live.a_IIIZ(0, i, j + 28 + 1, b2 == Live.enchant)
                self.h_III(Live.counts[15 - b2] // 10, i + 13, j + 28 + 8)
                self.h_III(Live.counts[15 - b2] % 10, i + 22, j + 28 + 8)
                i += 37
                b2 += 1
            j += 60
        del i_
        GameCanvas.h_II(-1, 2)

    def bt_v(self):  # m.java:256-276  (Buy: the lots of a page)
        j = 20 + (255 - 84 + GameCanvas.cursor[6] + 10 + 32 >> 1)
        self.i_I(j)
        j += 42
        i = self.b_III(j, 200, 32)
        Gfx.a_Lg(GameCanvas.font_white)
        Live.a_TIII(Live.category_names[Live.category], i, j + 10, 157)
        i += 157
        Live.a_IIIZ(Live.shown_item, i - 15, j + 9 - 7, False)
        if Live.category != 2:
            Gfx.a_MIII(Live.level_image, i + 28 - 14, j + 11, 0)
            self.h_III(Live.enchant, i + 28 + 14, j + 9)
        j += 42
        GameCanvas.menus.a_IAzAI(j, Live.lots, None)
        GameCanvas.cursor[14] = 1
        GameCanvas.a_LzZI(Live.lots[GameCanvas.cursor[18]], True, Live.prices[GameCanvas.cursor[18]])
        GameCanvas.menus.k_v()
        GameCanvas.h_II(-1, 2)

    @staticmethod
    def b_v():  # m.java:278-285  (registered already?)
        try:
            rs = RecordStore.openRecordStore("gamevil_pow_regist", True)
            return not (rs.getNumRecords() == 0)
        except Exception:
            return False

    @staticmethod
    def c_v():  # m.java:287-305  (keep UserID [0..12) and password [12..28))
        arrayOfByte1 = bytearray(28)
        arrayOfByte2 = Live.password.encode("latin-1")
        for b in range(len(arrayOfByte2)):
            arrayOfByte1[b] = arrayOfByte2[b]
        arrayOfByte2 = Live.user_id.encode("latin-1")
        for b in range(len(arrayOfByte2)):
            arrayOfByte1[12 + b] = arrayOfByte2[b]
        try:
            rs = RecordStore.openRecordStore("gamevil_pow_regist", True)
            if rs.getNumRecords() == 0:
                rs.addRecord(bytes(arrayOfByte1), 0, len(arrayOfByte1))
            rs.setRecord(1, bytes(arrayOfByte1), 0, len(arrayOfByte1))
        except Exception:
            return

    def d_v(self):  # m.java:307-320  (read it back: l = [0..12), m = [12..26))
        arrayOfByte = bytes(26)
        try:
            rs = RecordStore.openRecordStore("gamevil_pow_regist", False)
            if rs is None or rs.getNumRecords() < 1:
                Live.password = ""
                Live.user_id = ""
                return
            arrayOfByte = rs.getRecord(1)
        except Exception:
            pass
        Live.password = GameCanvas.f_T(GameCanvas.a_ABII(arrayOfByte, 0, 12))
        Live.user_id = GameCanvas.f_T(GameCanvas.a_ABII(arrayOfByte, 12, 26))

    def bu_v(self):  # m.java:322-341  (Safe: the amount)
        if GameCanvas.images[22] is None:
            GameCanvas.images[22] = self.d_T(GameCanvas.scr_ui.a_I(18))
        if GameCanvas.images[24] is None:
            GameCanvas.images[24] = self.d_T(GameCanvas.scr_ui.a_I(20))
        if Live.flags[15] == 0:
            Gfx.a_MII(GameCanvas.images[22], 107, 111)
        else:
            Gfx.a_MII(GameCanvas.images[24], 107, 111)
        Gfx.a_Lg(GameCanvas.font_white)
        Gfx.a_TIII("Local", GameCanvas.screen_w // 2 - 44, 111, 1)
        Gfx.a_TIII("Server", GameCanvas.screen_w // 2 + 50, 111, 1)
        Gfx.a_TIII("How much do", GameCanvas.screen_w // 2, 131, 1)
        Gfx.a_TIII("you want to move?", GameCanvas.screen_w // 2, 143, 1)
        self.a_IIII(70, 163, 100, 20)
        Gfx.a_Lg(GameCanvas.font_black)
        Gfx.a_TIII(GameCanvas.n_I(Live.values[14]), GameCanvas.screen_w // 2, 165, 1)
        GameCanvas.h_II(-1, 2)
        GameCanvas.popups.c_I(200)

    def a_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # m.java:343-356  (input box)
        GameCanvas.input_box.w = paramInt3 + 1
        GameCanvas.input_box.x = paramInt1 - 1
        GameCanvas.input_box.h = paramInt4 + 1
        GameCanvas.input_box.y = paramInt2 - 1
        GameCanvas.b_LacI(GameCanvas.input_box, 0)
        GameCanvas.input_box.x += 1
        GameCanvas.input_box.y += 1
        GameCanvas.b_LacI(GameCanvas.input_box, 16777215)
        GameCanvas.input_box.w -= 1
        GameCanvas.input_box.h -= 1
        GameCanvas.a_LacI(GameCanvas.input_box, GameCanvas.k_III(192, 192, 192))

    def bv_v(self):  # m.java:358-380  (Backpack / Warehouse grid)
        if Live.flags[7] == 0:
            s = "Backpack"
            arrayOfZ = GameCanvas.hero.backpack
        else:
            s = "Warehouse"
            arrayOfZ = Live.warehouse
        i = 20 + (255 - 38 + GameCanvas.cursor[6] + 16 + 22 >> 1)
        self.c_TI(s, i)
        i += 38
        GameCanvas.menus.a_IAzAI(i, arrayOfZ, None)
        GameCanvas.cursor[14] = 0
        GameCanvas.a_LzZI(arrayOfZ[GameCanvas.cursor[18]], True, -1)
        GameCanvas.menus.k_v()
        if Live.flags[7] == 0:
            GameCanvas.h_II(4, 2)
            return
        GameCanvas.h_II(3, 2)
