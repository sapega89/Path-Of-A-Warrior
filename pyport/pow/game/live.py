"""as.java - Gamevil Live of the single player (PHASE_7): its menus, the input and the
requests / answers. Literal port; the drawing is m.java (pow/game/m.py).

as is static state (every field is static in Java) plus an ag subclass instance (ag.be) whose
methods ag.run / ag.t / ag.L call. The server it talks to is pow_server/live.py, through
pow/game/v.py. Screens (ho, drawn by m.a()): 1 list, 2 Safe, 3 amount, 4 Backpack/Warehouse,
5 categories, 6 kinds, 7 enchant levels, 8 lots, 9 price, 10 Cancel, 11 Sale/Gift List,
12 waiting, 13 registration. Input handlers (hp): see t(int).

Fixes (config):
- DECOMP_FIX F20: as.a(ab) reads the status byte into a local and never sets gr, but m()
  waits for gr == 1 after the login 530 to send the request that needed it, and the error
  path passes gr as the error code: the status is gr (analysis/03 §5.1).
- ORIG_BUG B4: Buy with a full backpack asks "save it in Warehouse?" and then sends the item
  to the warehouse (ht[7] = 1), but 789 always puts it into the backpack: the search for a
  free slot runs past cz.Y[24] (ArrayIndexOutOfBounds in the network thread). Fixed: it goes
  into the warehouse list.
- ORIG_BUG B5: after CONFIRM on the password screen m.bp() counts frames (gE) and after 3 shows
  "Network connection has failed" and goes back to the UserID, even when the 531 has already
  answered (its popup is replaced) or is still on its way. Fixed: no count while the request
  is in flight (gu), and the 531 answer stops it.
"""
import config
from pow.game.game_canvas import GameCanvas
from pow.game.structs import Item
from pow.game.live_net import LiveNet
from pow.game.gfx import Gfx
from pow.midp import system
from pow.midp.graphics import Image
from pow.midp.jint import i8, i16, idiv

F20 = config.DECOMP_FIX["F20"]
B4 = config.ORIG_BUG["B4"]
B5 = config.ORIG_BUG["B5"]


class Live(GameCanvas):
    screen = None            # m (the drawing)
    net = None            # v (the network)
    first_login = True            # first Gamevil Live since the game started / a new game
    waiting = False           # waiting for an answer
    request_time = 0               # time of the request
    pending_request = -1              # request to send on the next i()
    answer_op = 0               # opcode of the last answer
    blink_count = 0
    anim_ticks = 0
    reg_step = 0               # registration step: 1 UserID, 0 password
    password = ""              # password
    user_id = ""              # UserID
    reg_from_popup = False           # the 530 is a registration from the screen (popups 48 / 44)
    inited = False
    loading0 = None            # netLoading0.png
    loading1 = None            # netLoading1.png
    arrow_image = None            # ui_arrow2.png
    level_image = None            # ui_level.png
    session_id = system.currentTimeMillis() // 10000
    session_new = 0
    login_request = 0              # request that waits for the login
    request_in_flight = 0              # request in flight
    answer_status = 0              # status of the last answer (F20)
    answered = False          # an answer (or an error) came
    close_target = -1             # what the closing popup leads to (i())
    busy = False          # busy: "Connecting..." over the screen, keys ignored
    backpack_serials = None           # short[25] backpack serials
    warehouse = [None] * 100   # z[100] warehouse
    warehouse_serials = None           # short[100] warehouse serials
    safe_gold = 0              # gold in the Safe
    lots = [None] * 20    # z[20] lots of the page / Sale List / Gift List / my lots
    lot_ids = [0] * 20       # lot ids
    prices = [0] * 20       # prices
    gift_from = [""] * 5       # Gift List: from whom
    list_kind = 0              # 0 Sale List, 1 Gift List
    blink = False
    kind_items = [[116, 121, 126, 101, 106, 111, 131, 136, 156, 161, 181, 146, 151, 0, 0, 0, 0, 0, 0, 0],
          [331, 324, 322, 301, 308, 302, 341, 350, 357, 363, 370, 380, 415, 0, 0, 0, 0, 0, 0, 0],
          [501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 0, 0]]
    category_codes = [3, 4, 5, 9, 10, 11, 12, 13, 6, 7, 8, 14, 15, 16, 17, 18, 19, 20, 21]
    in_answer = False          # inside a(ab)
    list_items = [None] * 8     # list menu items
    list_count = 0              # list: count
    list_rows = 0              # list: visible rows / a slot count
    list_cursor = 0              # list: cursor
    list_top = 0              # list: first visible
    list_y = 0              # list: y
    list_w = 0
    category = 0              # category 0 Normal 1 Special 2 Rare
    kind = 0              # kind
    enchant = 0              # enchant level
    page = 0              # page
    page_step = 0              # page step
    saved_0 = saved_1 = saved_2 = saved_3 = saved_4 = saved_5 = 0
    saved_6 = saved_7 = saved_8 = saved_9 = saved_10 = saved_11 = saved_12 = saved_13 = 0
    shown_item = 0              # item id shown
    selected_serial = 0              # serial of the selected item
    selected_slot = 0              # selected slot of a 5-slot list
    titles = [None] * 12    # gamestr 2..13 titles
    live_strings = [None] * 50    # gamestr 15..64
    title = ""             # title
    live_screen = 0              # screen
    input_handler = 0              # input handler
    screen_redraw = False          # redraw
    scroll = 0
    scroll_step = 0
    flags = [0] * 16
    counts = [0] * 16
    values = [0] * 16
    category_names = ["Normal Items", "Special Items", "Rare Items"]

    def __init__(self):  # as.java:172-178
        super().__init__(GameCanvas.midlet)
        if Live.backpack_serials is None:
            Live.backpack_serials = [0] * 25
        if Live.warehouse_serials is None:
            Live.warehouse_serials = [0] * 100

    def g_v(self):  # as.java:180-190  (Game Menu > Gamevil Live)
        from pow.game.live_screen import LiveScreen
        Live.inited = True
        if LiveScreen.b_v():
            Live.reg_from_popup = False
            Live.screen.d_v()
            GameCanvas.popups.d_I(2)
            Live.close_target = 2
            return
        self.h_v()

    def h_v(self):  # as.java:192-208  (registration screen)
        from pow.game.name_buffer import NameBuffer
        GameCanvas.in_live = True
        GameCanvas.ai()
        Live.title = "Registration"
        Live.live_screen = 13
        Live.input_handler = 18
        Live.reg_step = 1
        GameCanvas.letter_cursor = 0
        Live.aJ()
        GameCanvas.state = 11
        Live.password = ""
        Live.user_id = ""
        GameCanvas.name_buf = None
        GameCanvas.name_buf = NameBuffer("", 12, 10)
        self.k_v()
        Live.aJ()

    def i_v(self):  # as.java:210-299  (every frame from ag.run)
        if Live.net is not None:
            Live.net.pump()
        if Live.pending_request != -1:
            self.d_I(Live.pending_request)
        if GameCanvas.popups.answered:
            GameCanvas.popups.answered = False
            i = Live.close_target
            Live.close_target = -1
            s1 = GameCanvas.popups.button
            if i == 3:
                self.ba_v()
                Live.aJ()
            elif i == 2:
                if s1 == 0:
                    GameCanvas.in_live = True
                    GameCanvas.ai()
                    self.k_v()
                    self.aE_v()
                    self.aI_v()
                    self.c_I(512)
                else:
                    self.ba_v()
                    Live.aJ()
            elif i == 7:
                if Live.flags[15] > 0:
                    self.c_I(516)
                else:
                    self.aS_v()
            elif i == 8:
                self.aX_v()
            elif i == 9:
                if s1 == 0:
                    bool_ = False
                    if Live.flags[14] == 1:
                        for b in range(9):
                            if GameCanvas.hero.equipped[b].id > 0:
                                bool_ = True
                                break
                        if bool_:
                            GameCanvas.popups.d_I(33)
                            return self._i_end()
                    Live.scroll = 0
                    if Live.flags[14] == 0:
                        self.c_I(256)
                    else:
                        self.c_I(262)
            elif i == 10:
                if s1 == 0:
                    if GameCanvas.cursor[16] < 25:
                        Live.flags[7] = 0
                        Live.scroll = 0
                        self.c_I(788)
                    else:
                        GameCanvas.popups.d_I(12)
                        Live.close_target = 11
            elif i == 11:
                if s1 == 0:
                    Live.flags[7] = 1
                    Live.scroll = 0
                    self.c_I(788)
            elif i == 14:
                if s1 == 0:
                    Live.scroll = 0
                    self.c_I(866)
                    Live.screen_redraw = True
        self._i_end()

    def _i_end(self):
        if Live.waiting:
            self.m_v()

    @staticmethod
    def b_I(paramInt):  # as.java:301-353  (error code -> gamestr popup)
        b = {-1: 21, -2: 22, -4: 23, -12: 24, -13: 25, -15: 26, -16: 27, -18: 28, -20: 29,
             -22: 30, -23: 31, -26: 7, -49: 54}.get(paramInt, -1)
        if paramInt == -26:
            Live.close_target = 3
        elif paramInt == -11:
            b = 10 if Live.page > 0 else 8
        if b != -1:
            GameCanvas.popups.d_I(b)

    def j_v(self):  # as.java:355-364  ("Connecting..." over the screen)
        GameCanvas.popups.b_I(96)
        i = GameCanvas.view_cy - 20 - 10
        j = Live.loading0.getWidth()
        k = Live.loading0.getHeight()
        GameCanvas.a_IIIIMII((GameCanvas.screen_w - j) // 2, i, j, k, Live.loading0, 0, 0)
        GameCanvas.a_IIIIMII((GameCanvas.screen_w - j) // 2, i, j * (GameCanvas.frame % 6) // 5, k, Live.loading1, 0, 0)
        Gfx.a_Lg(GameCanvas.font_white)
        Gfx.a_TIII("Connecting...", GameCanvas.screen_w // 2, i + 50, 1)

    def k_v(self):  # as.java:366-378
        try:
            if Live.loading0 is None:
                Live.loading0 = Image.createImage("/netLoading0.png")
            if Live.loading1 is None:
                Live.loading1 = Image.createImage("/netLoading1.png")
            if Live.arrow_image is None:
                Live.arrow_image = Image.createImage("/ui_arrow2.png")
            if Live.level_image is None:
                Live.level_image = Image.createImage("/ui_level.png")
        except Exception:
            pass
        Live.l_v()

    @staticmethod
    def l_v():  # as.java:380-386
        if Live.net is None:
            Live.net = LiveNet()
            Live.net.setPriority(5)
            Live.net.start()

    def f_v(self):  # as.java:388-390  (s.f(): connected)
        self.n_v()

    def c_I(self, paramInt):  # as.java:392-397  (ask for a request on the next i())
        Live.answer_status = 0
        GameCanvas.v_v()
        Live.busy = True
        Live.pending_request = paramInt

    def d_I(self, paramInt):  # as.java:399-413
        Live.pending_request = -1
        Live.login_request = 0
        if not LiveNet.connected:
            Live.login_request = paramInt
            Live.request_in_flight = 530
        else:
            Live.request_in_flight = paramInt
        Live.request_time = system.currentTimeMillis()
        Live.waiting = False
        self.e_I(Live.request_in_flight)
        Live.aJ()
        Live.waiting = True

    def m_v(self):  # as.java:415-438  (answer came / timeout)
        if Live.answered:
            if not Live.in_answer:
                GameCanvas.w_v()
                Live.waiting = False
                Live.busy = False
                Live.aJ()
        elif LiveNet.waiting and not Live.in_answer and (GameCanvas.key == -7 or system.currentTimeMillis() > Live.request_time + 30000):
            Live.answer_status = -1
            if Live.net is not None:
                Live.net.a_v()
                Live.bi_v()
                GameCanvas.R_v()
            Live.busy = False
            self.a_IILab(Live.request_in_flight + 1, Live.answer_status, None)
            Live.aJ()
        if Live.answer_status == 1 and Live.request_in_flight == 530 and Live.login_request != 530:
            Live.request_in_flight = Live.login_request
            self.c_I(Live.request_in_flight)

    def e_I(self, paramInt):  # as.java:440-451
        Live.request_in_flight = paramInt
        if not LiveNet.connected:
            if Live.net is None:
                Live.l_v()
            LiveNet.a_Ls(self)
            Live.net.a_TI(GameCanvas.live_host, GameCanvas.live_port)
        else:
            self.n_v()
        Live.answered = False

    def n_v(self):  # as.java:453-576  (write the request gq)
        cz = GameCanvas.hero
        Live.answer_status = 0
        Live.net.a_I(Live.request_in_flight)
        q = Live.request_in_flight
        if q == 530:
            LiveNet.b_TI(Live.user_id, 12)
            LiveNet.b_TI(Live.password, 16)
            LiveNet.b_TI("1501", 4)
            LiveNet.b_I(Live.session_id)
            Live.session_new = system.currentTimeMillis() // 10000
            LiveNet.b_I(Live.session_new)
        elif q in (516, 256):
            LiveNet.b_I(cz.fame)
            LiveNet.b_I(cz.exp)
            LiveNet.a_S(cz.level)
            LiveNet.a_B(cz.head)
            LiveNet.a_B(GameCanvas.g_I(cz.equipped[0].id) ^ 0x1)
            LiveNet.a_S(cz.base_attack)
            LiveNet.a_S(cz.base_defense)
            LiveNet.a_S(cz.base_hp)
            LiveNet.a_S(cz.base_mp)
            LiveNet.a_S(cz.stat_points)
            GameCanvas.O_v()
            LiveNet.a_S(cz.gear_attack)
            LiveNet.a_S(cz.gear_defense)
            LiveNet.a_S(cz.gear_hp)
            LiveNet.a_S(cz.gear_mp)
            for b1 in range(8):
                LiveNet.b_I(GameCanvas.stats[b1])
            b = 0
            for b2 in range(len(cz.skill_levels)):
                if cz.skill_levels[b2] > 0:
                    b += 1
            LiveNet.a_B(b)
            for b3 in range(len(cz.skill_levels)):
                if cz.skill_levels[b3] > 0:
                    LiveNet.a_B(Live.category_codes[b3])
                    LiveNet.a_B(cz.skill_levels[b3])
                    bool_ = False
                    for b8 in range(4):
                        if cz.hotkeys[b8] - 12 == b3:
                            bool_ = True
                            break
                    LiveNet.a_Z(bool_)
            LiveNet.b_TI(cz.name, 8)
            LiveNet.a_Z(not (cz.live_registered == 0))
            LiveNet.a_B(GameCanvas.general_count & 0xFF)
            for b4 in range(GameCanvas.general_count):
                LiveNet.a_B(GameCanvas.generals[0][b4] & 0xFF)
                LiveNet.a_B(GameCanvas.generals[1][b4] & 0xFF)
            LiveNet.b_I(GameCanvas.missions_done & 0xFFFFFFFF)
            LiveNet.b_I(GameCanvas.missions_done >> 32 & 0xFFFFFFFF)
            LiveNet.a_B(GameCanvas.chapter)
            for b5 in range(22):
                LiveNet.a_B(cz.mission_progress[b5] & 0xFF)
            LiveNet.a_B(cz.live_stat1 & 0xFF)
            LiveNet.a_B(cz.live_stat2 & 0xFF)
            LiveNet.b_I(GameCanvas.score)
        elif q == 768:
            from pow.game.menus import Menus
            LiveNet.b_I(cz.gold)
            Menus.m_v()
            b6 = i8(GameCanvas.cursor[16])
            LiveNet.a_B(b6)
            for b7 in range(25):
                if cz.backpack[b7].id > 0:
                    LiveNet.a_S(cz.backpack[b7].id)
                    Live.backpack_serials[b7] = i16(b7 + 1)
                    LiveNet.a_S(Live.backpack_serials[b7])
                    LiveNet.a_B(cz.backpack[b7].enchant)
                    LiveNet.a_S(cz.backpack[b7].attack)
                    LiveNet.a_S(cz.backpack[b7].defense)
                    LiveNet.a_S(cz.backpack[b7].hp)
                    LiveNet.a_S(cz.backpack[b7].mp)
        elif q == 832:
            LiveNet.a_B(Live.flags[15] ^ 0x1)
            LiveNet.b_I(Live.values[14])
        elif q == 816:
            LiveNet.a_B(Live.flags[7])
            LiveNet.a_S(Live.selected_serial)
        elif q in (784, 786, 788, 800):     # case 784 / 786 / 788 / 800 fall through
            if q == 784:
                LiveNet.a_B(Live.category + 1)
            if q in (784, 786):
                LiveNet.a_B(Live.category + 1)
                LiveNet.a_B(Live.kind + 1)
                LiveNet.a_B(Live.enchant)
            if q in (784, 786, 788):
                LiveNet.b_I(Live.lot_ids[GameCanvas.cursor[18]])
            LiveNet.a_B(Live.flags[7])
            LiveNet.a_S(Live.selected_serial)
            LiveNet.b_I(Live.values[14])
        elif q in (802, 866):               # case 802 falls through into 866
            if q == 802:
                LiveNet.a_B(Live.category + 1)
                LiveNet.a_B(Live.kind + 1)
            LiveNet.b_I(Live.lot_ids[Live.selected_slot])
            LiveNet.a_B(0 if GameCanvas.cursor[16] < 25 else 1)
        Live.net.b_v()

    def o_v(self):  # as.java:578-591
        LiveNet.connected = False
        if Live.net is not None:
            Live.net.a_v()
            Live.bi_v()
        if GameCanvas.state == 11:
            Live.close_target = 3
            GameCanvas.popups.d_I(29)
        Live.busy = False
        Live.waiting = False
        GameCanvas.f_I(300)

    def e_v(self):  # as.java:593-599  (s.e(): the connection failed / broke)
        if Live.net is not None:
            Live.net.a_v()
            Live.bi_v()
        Live.answered = True

    @staticmethod
    def _copy(dst, src):
        dst.id, dst.attack, dst.defense, dst.hp, dst.mp, dst.enchant = src.id, src.attack, src.defense, src.hp, src.mp, src.enchant

    def a_Lab(self, paramab):  # as.java:601-990  (s.a(ab): one answer)
        cz = GameCanvas.hero
        fK = GameCanvas.cursor
        Live.in_answer = True
        LiveNet.waiting = False
        s1 = paramab.b_v()
        b = paramab.a_v()
        if F20:
            Live.answer_status = b                      # DECOMP_FIX F20
        Live.answer_op = s1
        if B5 and s1 == 531:
            Live.blink = False                  # ORIG-BUG B5
        if b == 1:
            if s1 == 531:
                Live.session_id = Live.session_new
                self.ar()
                paramab.a_v()
                paramab.a_v()
                b6 = paramab.a_v()
                if (b6 == 0 or b6 == 2) and Live.reg_from_popup:
                    from pow.game.live_screen import LiveScreen
                    LiveScreen.c_v()
                    if b6 == 0:
                        GameCanvas.popups.d_I(48)
                    elif b6 == 2:
                        GameCanvas.popups.d_I(44)
                    Live.close_target = 2
                    Live.reg_from_popup = False
            elif s1 == 513:
                Live.flags[15] = paramab.a_v()
                Live.flags[14] = paramab.a_v()
                Live.flags[13] = paramab.a_v()
                paramab.a_v()
                for _ in range(5):
                    paramab.c_v()
                Live.flags[4] = paramab.a_v()
                Live.flags[5] = paramab.a_v()
                self.aR_v()
                Live.aJ()
            elif s1 == 517:
                GameCanvas.popups.arg1 = GameCanvas.e_T(GameCanvas.f_T(paramab.a_I(16)))
                GameCanvas.popups.arg2 = GameCanvas.e_T(GameCanvas.f_T(paramab.a_I(16)))
                GameCanvas.popups.arg3 = GameCanvas.e_T(GameCanvas.f_T(paramab.a_I(16)))
                GameCanvas.popups.arg4 = GameCanvas.e_T(GameCanvas.f_T(paramab.a_I(16)))
                GameCanvas.popups.d_I(53)
                Live.close_target = 7
                if paramab.a_v() == 1:
                    Live.flags[15] = i16(Live.flags[15] + 1)
                else:
                    Live.flags[15] = 0
            elif s1 == 519:
                for b1 in range(20):
                    if Live.lots[b1] is None:
                        Live.lots[b1] = Item()
                    Item.a(Live.lots[b1])
                    Live.prices[b1] = 0
                b5 = paramab.a_v()
                for b1 in range(b5):
                    Live.lots[b1].id = paramab.b_v()
                    Live.lots[b1].enchant = paramab.a_v()
                    Live.prices[b1] = paramab.c_v()
                Live.list_kind = 0
                self.aT_v()
            elif s1 == 261:
                GameCanvas.live_gifts = i16(GameCanvas.live_gifts - 1)
                if GameCanvas.live_gifts == 0:
                    self.ar()
                    if Live.values[15] == 0 and Live.values[14] == 0:
                        if Live.first_login:
                            GameCanvas.popups.d_I(20)
                        else:
                            GameCanvas.popups.answered = True
                    else:
                        GameCanvas.popups.arg1 = str(Live.values[14])
                        GameCanvas.popups.arg2 = str(Live.values[15])
                        GameCanvas.popups.arg3 = str(Live.values[13])
                        GameCanvas.popups.d_I(41)
                    Live.close_target = 8
                else:
                    GameCanvas.live_gifts = 0
                    self.aV_v()
            elif s1 == 263:
                cz.fame = paramab.c_v()
                cz.exp = paramab.c_v()
                cz.level = paramab.b_v() & 0xFF
                cz.head = paramab.a_v()
                cz.weapon_kind = paramab.a_v()
                cz.base_attack = paramab.b_v()
                cz.base_defense = paramab.b_v()
                cz.base_hp = paramab.b_v()
                cz.base_mp = paramab.b_v()
                cz.stat_points = paramab.b_v()
                for b1 in range(len(cz.skill_levels)):
                    cz.skill_levels[b1] = 0
                for b1 in range(len(cz.hotkeys)):
                    cz.hotkeys[b1] = 0
                b4 = paramab.a_v()
                b1 = 0
                b2 = 0
                while b1 < b4:
                    b8 = paramab.a_v()
                    b7 = 0
                    while b7 < 19 and Live.category_codes[b7] != b8:
                        b7 += 1
                    cz.skill_levels[b7] = paramab.a_v()
                    b8 = paramab.a_v()
                    if b8 == 1:
                        cz.hotkeys[b2] = b7 + 12
                        b2 += 1
                    b1 += 1
                for b1 in range(8):
                    GameCanvas.stats[b1] = paramab.c_v()
                cz.name = GameCanvas.g_T(GameCanvas.f_T(paramab.a_I(8)))
                cz.live_registered = paramab.a_v()
                for b1 in range(45):
                    GameCanvas.generals[0][b1] = 0
                    GameCanvas.generals[1][b1] = 0
                GameCanvas.general_count = i16(paramab.a_v())
                for b1 in range(GameCanvas.general_count):
                    GameCanvas.generals[0][b1] = i16(paramab.a_v())
                    GameCanvas.generals[1][b1] = i16(paramab.a_v())
                i = paramab.c_v()
                GameCanvas.missions_done = paramab.c_v()
                GameCanvas.missions_done <<= 32
                GameCanvas.missions_done |= i                  # sic: a negative low word fills the high one (Java long |)
                GameCanvas.chapter = paramab.a_v()
                for b1 in range(22):
                    cz.mission_progress[b1] = i16(paramab.a_v())
                cz.live_stat1 = i16(paramab.a_v())
                cz.live_stat2 = i16(paramab.a_v())
                GameCanvas.score = paramab.c_v()
                self.ar()
                GameCanvas.popups.d_I(19)
            elif s1 == 257:
                GameCanvas.popups.d_I(18)
            elif s1 == 769:
                Live.safe_gold = paramab.c_v()
                for b1 in range(100):
                    if Live.warehouse[b1] is None:
                        Live.warehouse[b1] = Item()
                    Item.a(Live.warehouse[b1])
                Live.flags[6] = i16(paramab.a_v() & 0xFF)
                for b1 in range(len(Live.warehouse)):
                    Item.a(Live.warehouse[b1])
                for b1 in range(Live.flags[6]):
                    Live.warehouse[b1].id = paramab.b_v()
                    Live.warehouse_serials[b1] = paramab.b_v()
                    Live.warehouse[b1].enchant = paramab.a_v()
                    Live.warehouse[b1].attack = paramab.b_v()
                    Live.warehouse[b1].defense = paramab.b_v()
                    Live.warehouse[b1].hp = paramab.b_v()
                    Live.warehouse[b1].mp = paramab.b_v()
                self.aH_v()
            elif s1 == 833:
                cz.gold = paramab.c_v()
                Live.safe_gold = paramab.c_v()
            elif s1 == 817:
                if Live.flags[7] == 0:
                    Live.list_rows = 100
                    fK[16] = fK[16] - 1
                    Live.flags[6] = i16(Live.flags[6] + 1)
                    b1 = 0
                    while b1 < Live.list_rows and Live.warehouse[b1].id != 0:
                        b1 += 1
                    Live._copy(Live.warehouse[b1], cz.backpack[fK[18]])
                    Item.a(cz.backpack[fK[18]])
                    Live.warehouse_serials[b1] = paramab.b_v()
                    Live.backpack_serials[fK[18]] = 0
                else:
                    Live.list_rows = 25
                    Live.flags[6] = i16(Live.flags[6] - 1)
                    fK[16] = fK[16] + 1
                    b1 = 0
                    while b1 < Live.list_rows and cz.backpack[b1].id != 0:
                        b1 += 1
                    Live._copy(cz.backpack[b1], Live.warehouse[fK[18]])
                    Item.a(Live.warehouse[fK[18]])
                    Live.backpack_serials[b1] = paramab.b_v()
                    Live.warehouse_serials[fK[18]] = 0
                self.O_I(0)
                Live.aJ()
            elif s1 == 785:
                b1 = 0
                b3 = 15
                while b1 < 10:
                    Live.counts[b3] = paramab.a_v()
                    b1 += 1
                    b3 -= 1
                self.aM_v()
            elif s1 == 521:
                for b1 in range(5):
                    if Live.lots[b1] is None:
                        Live.lots[b1] = Item()
                    Item.a(Live.lots[b1])
                    Live.gift_from[b1] = ""
                b5 = paramab.a_v()
                for b1 in range(b5):
                    Live.gift_from[b1] = GameCanvas.f_T(paramab.a_I(8))
                    Live.lots[b1].id = paramab.b_v()
                    Live.lots[b1].enchant = paramab.a_v()
                    Live.lots[b1].attack = paramab.b_v()
                    Live.lots[b1].defense = paramab.b_v()
                    Live.lots[b1].hp = paramab.b_v()
                    Live.lots[b1].mp = paramab.b_v()
                Live.flags[13] = paramab.a_v()
                Live.list_kind = 1
                self.aT_v()
            elif s1 == 787:
                for b1 in range(20):
                    if Live.lots[b1] is None:
                        Live.lots[b1] = Item()
                    Item.a(Live.lots[b1])
                    Live.lot_ids[b1] = 0
                    Live.prices[b1] = 0
                b4 = paramab.a_v()
                for b1 in range(b4):
                    Live.lot_ids[b1] = paramab.c_v()
                    Live.lots[b1].id = paramab.b_v()
                    Live.prices[b1] = paramab.c_v()
                    Live.lots[b1].enchant = paramab.a_v()
                    Live.lots[b1].attack = paramab.b_v()
                    Live.lots[b1].defense = paramab.b_v()
                    Live.lots[b1].hp = paramab.b_v()
                    Live.lots[b1].mp = paramab.b_v()
                Live.page = i8(Live.page + Live.page_step)
                self.aN_v()
            elif s1 == 789:
                if B4 and Live.flags[7] == 1:     # ORIG-BUG B4: bought into the warehouse
                    Live.flags[6] = i16(Live.flags[6] + 1)
                    b1 = 0
                    while b1 < 100 and Live.warehouse[b1].id != 0:
                        b1 += 1
                    Live._copy(Live.warehouse[b1], Live.lots[fK[18]])
                    Live.p_v()
                    Live.warehouse_serials[b1] = paramab.b_v()
                else:
                    Live.list_rows = 25
                    fK[16] = fK[16] + 1
                    b1 = 0
                    while b1 < Live.list_rows and cz.backpack[b1].id != 0:
                        b1 += 1
                    Live._copy(cz.backpack[b1], Live.lots[fK[18]])
                    Live.p_v()
                    Live.backpack_serials[b1] = paramab.b_v()
                cz.gold = paramab.c_v()
                Live.safe_gold = paramab.c_v()
                self.O_I(0)
                GameCanvas.popups.d_I(35)
            elif s1 == 801:
                if Live.flags[7] == 0:
                    Item.a(cz.backpack[Live.selected_slot])
                    Live.backpack_serials[Live.selected_slot] = 0
                    fK[16] = fK[16] - 1
                else:
                    Item.a(Live.warehouse[Live.selected_slot])
                    Live.warehouse_serials[Live.selected_slot] = 0
                    Live.flags[6] = i16(Live.flags[6] - 1)
                self.O_I(0)
                GameCanvas.popups.d_I(36)
                self.aP_v()
            elif s1 in (803, 865):
                for b1 in range(20):
                    if Live.lots[b1] is None:
                        Live.lots[b1] = Item()
                    Item.a(Live.lots[b1])
                    Live.lot_ids[b1] = 0
                    Live.prices[b1] = 0
                b4 = paramab.a_v()
                if b4 > 20:
                    b4 = 20
                for b1 in range(b4):
                    if s1 == 865:
                        Live.lot_ids[b1] = paramab.c_v()
                    Live.lots[b1].id = paramab.b_v()
                    Live.prices[b1] = paramab.c_v()
                    Live.lots[b1].enchant = paramab.a_v()
                    Live.lots[b1].attack = paramab.b_v()
                    Live.lots[b1].defense = paramab.b_v()
                    Live.lots[b1].hp = paramab.b_v()
                    Live.lots[b1].mp = paramab.b_v()
                if s1 == 803:
                    self.aO_v()
                    Live.live_screen = 8
                    Live.input_handler = 10
                    Live.title = Live.titles[6]
                    Live.aJ()
                else:
                    self.d_Z(False)
            elif s1 == 867:
                if Live.flags[7] == 0:
                    Live.list_rows = 25
                    Live.flags[6] = i16(Live.flags[6] - 1)
                    fK[16] = fK[16] + 1
                    b1 = 0
                    while b1 < Live.list_rows and cz.backpack[b1].id != 0:
                        b1 += 1
                    Live._copy(cz.backpack[b1], Live.lots[Live.selected_slot])
                    Item.a(Live.lots[Live.selected_slot])
                    Live.p_v()
                    Live.backpack_serials[b1] = paramab.b_v()
                else:
                    Live.list_rows = 100
                    fK[16] = fK[16] - 1
                    Live.flags[6] = i16(Live.flags[6] + 1)
                    b1 = 0
                    while b1 < Live.list_rows and Live.warehouse[b1].id != 0:
                        b1 += 1
                    Live._copy(Live.warehouse[b1], Live.lots[Live.selected_slot])
                    Item.a(Live.lots[Live.selected_slot])
                    Live.p_v()
                    Live.warehouse_serials[b1] = paramab.b_v()
                self.O_I(0)
                GameCanvas.popups.d_I(40)
            elif s1 == 259:
                Live.values[15] = paramab.c_v()
                Live.values[14] = paramab.c_v()
                Live.values[13] = GameCanvas.H_I(Live.values[14])
                cz.fame += Live.values[15]
                GameCanvas.live_gifts = 1
                self.ar()
                self.aW_v()
        else:
            self.a_IILab(Live.answer_op, Live.answer_status if F20 else 0, paramab)
        Live.in_answer = False
        LiveNet.waiting = True
        Live.answered = True

    def a_IILab(self, paramInt1, paramInt2, paramab):  # as.java:992-1056  (error answers)
        if paramInt1 == 531:
            if paramab is None:
                Live.b_I(paramInt2)
                Live.close_target = 3
                return
            paramab.a_v()
            paramab.a_v()
            b = paramab.a_v()
            if b == 1:
                GameCanvas.popups.d_I(43)
                return
            if b == 3 and paramInt2 != -49:
                GameCanvas.popups.d_I(47)
                return
            Live.b_I(paramInt2)
            Live.close_target = 3
            return
        if paramInt1 == 513:
            Live.b_I(paramInt2)
            Live.close_target = 3
            return
        if paramInt1 == 517:
            self.aS_v()
            return
        if paramInt1 == 519:
            self.aU_v()
            return
        if paramInt1 == 521:
            self.aV_v()
            return
        if paramInt1 in (259, 261):
            self.aX_v()
            return
        if paramInt1 == 769:
            Live.b_I(paramInt2)
            Live.close_target = 3
            return
        if paramInt1 == 789:
            Live.b_I(paramInt2)
            return
        if paramInt1 == 867 and paramInt2 == -12:
            Live.p_v()
        if paramInt1 in (867, 801, 817, 833, 849):
            self.O_I(0)
        Live.b_I(paramInt2)

    @staticmethod
    def p_v():  # as.java:1058-1062
        Item.a(Live.lots[Live.selected_slot])
        Live.prices[Live.selected_slot] = 0
        Live.lot_ids[Live.selected_slot] = 0

    def O_I(self, paramInt):  # as.java:1064-1067  (save the game)
        GameCanvas.live_saved = i16(paramInt)
        self.ar()

    @staticmethod
    def aB_v():  # as.java:1069-1071
        return 32 * Live.list_rows - 12

    @staticmethod
    def e_TII(paramString, paramInt1, paramInt2):  # as.java:1073-1092  ("a|b|c|" -> list menu)
        i = 0
        j = 0
        for b in range(len(paramString)):
            if paramString[b] == '|':
                Live.list_items[i] = paramString[j:b]
                j = b + 1
                i += 1
        if i == 0:
            return
        Live.list_count = i16(i)
        i = idiv(paramInt2 + 12, 32)
        Live.list_rows = i16(i)
        if Live.list_rows > Live.list_count:
            Live.list_rows = Live.list_count
        Live.list_y = i16(paramInt1 + (paramInt2 - 32 * Live.list_rows - 12 >> 1))
        Live.list_top = Live.list_cursor = 0

    def P_I(self, paramInt):  # as.java:1094-1109  (list keys: -2 moved, index chosen, -1)
        i = -1
        if paramInt in (-1, -2, 50, 56):
            if paramInt in (-1, 50):
                Live.list_cursor -= 1
                if Live.list_cursor < 0:
                    Live.list_cursor = i16(Live.list_count - 1)
            else:
                Live.list_cursor += 1
                if Live.list_cursor >= Live.list_count:
                    Live.list_cursor = 0
            Live.aC_v()
            i = -2
        elif paramInt in (-5, 53):
            i = Live.list_cursor
        return i

    @staticmethod
    def aC_v():  # as.java:1111-1118
        if Live.list_top > Live.list_cursor:
            Live.list_top = Live.list_cursor
            return
        if Live.list_cursor - Live.list_top >= Live.list_rows:
            Live.list_top = Live.list_cursor - Live.list_rows + 1

    def aD_v(self):  # as.java:1120-1135  (draw the list menu)
        i = Live.list_y
        b = 0
        j = Live.list_top
        while b < Live.list_rows:
            if j == Live.list_cursor:
                GameCanvas.a_IIIIIIIZ(45, i, 150, 20, GameCanvas.k_III(0, 0, 0), GameCanvas.k_III(255, 255, 255), GameCanvas.k_III(0, 0, 0), True)
                Gfx.a_Lg(GameCanvas.font_orange)
            else:
                GameCanvas.a_IIIIIIIZ(46, i + 1, 148, 18, GameCanvas.k_III(0, 0, 0), GameCanvas.k_III(80, 80, 80), GameCanvas.k_III(0, 0, 0), True)
                Gfx.a_Lg(GameCanvas.font_white)
            GameCanvas.b_IIT(120, i + 1, Live.list_items[j])
            i += 32
            b += 1
            j += 1

    def aE_v(self):  # as.java:1137-1143
        self.aF_v()
        self.aG_v()
        GameCanvas.az()
        GameCanvas.state = 11
        Live.list_w = GameCanvas.view_size.x

    def aF_v(self):  # as.java:1145-1149
        for b in range(12):
            Live.titles[b] = GameCanvas.M_I(2 + b)
        return True

    def aG_v(self):  # as.java:1151-1155
        for b in range(50):
            Live.live_strings[b] = GameCanvas.M_I(15 + b)
        return True

    def aH_v(self):  # as.java:1157-1176  (GAMEVIL LIVE menu)
        Live.e_TII("Trade|Warehouse|Safe|Management|", 20, 255)
        Live.list_cursor = Live.saved_0
        Live.list_top = Live.saved_1
        Live.aC_v()
        Live.input_handler = 2
        Live.live_screen = 1
        Live.title = Live.titles[2]
        Live.scroll = 0
        Live.scroll_step = 10
        if Live.inited and Live.first_login:
            Live.inited = False
            GameCanvas.popups.arg1 = Live.password
            GameCanvas.popups.arg2 = Live.user_id
            GameCanvas.popups.d_I(49)
        Live.aJ()
        Live.first_login = False

    def aI_v(self):  # as.java:1178-1184  (waiting screen)
        Live.input_handler = 17
        Live.live_screen = 12
        Live.title = Live.titles[2]
        Live.anim_ticks = 0
        Live.aJ()

    @staticmethod
    def aJ():  # as.java:1186-1188
        Live.screen_redraw = True

    @staticmethod
    def a_IIIZ(paramInt1, paramInt2, paramInt3, paramBoolean):  # as.java:1190-1194  (item cell)
        GameCanvas.menus.a_IIZ(paramInt2, paramInt3, paramBoolean)
        if paramInt1 > 0:
            GameCanvas.menus.a_IIII(paramInt1, paramInt2, paramInt3, 0)

    @staticmethod
    def a_TIII(paramString, paramInt1, paramInt2, paramInt3):  # as.java:1196-1198
        Gfx.a_TIII(paramString, paramInt1 + idiv(paramInt3, 2), paramInt2, 1)

    @staticmethod
    def aK():  # as.java:1200-1202
        Live.screen.a_v()

    def c_TI(self, paramString, paramInt):  # as.java:1204-1209  (caption box)
        Gfx.a_Lg(GameCanvas.font_white)
        self.b_III(paramInt, 200, 22)
        if paramString != "":
            self.b_TII(paramString, paramInt + 1 - GameCanvas.view_y, 0)

    def t_I(self, paramInt):  # as.java:1211-1269  (keys)
        i = paramInt
        if GameCanvas.popups.kind != 0:
            GameCanvas.popups.b_v()
            GameCanvas.key = -999
            Live.aJ()
            return
        GameCanvas.key = -999
        h = {1: self.R_I, 2: self.ae_I, 3: self.aa_I, 4: self.Z_I, 5: self.W_I, 6: self.X_I, 7: self.Y_I,
             8: self.U_I, 9: self.V_I, 10: self.T_I, 13: self.S_I, 14: self.ab_I, 15: self.ad_I,
             16: self.af_I, 18: self.Q_I}.get(Live.input_handler)
        if h is not None:
            h(i)

    def Q_I(self, paramInt):  # as.java:1271-1328  (registration: UserID, then password)
        if Live.reg_step == 0:
            i = len(Live.password)
            if paramInt == -7:
                if i > 0:
                    Live.password = Live.password[:i - 1]
                else:
                    Live.reg_step = 1
                    Live.aJ()
                if i == 10:
                    Live.aJ()
                    return
            elif paramInt == -6:
                if i >= 4:
                    Live.blink = True
                    Live.reg_from_popup = True
                    self.c_I(530)
                    return
            else:
                j = GameCanvas.N_I(paramInt)
                if j != -1 and i < 12:
                    Live.password += str(j)
                return
        elif Live.reg_step == 1:
            if len(GameCanvas.name_buf.a_v()) == 0 and paramInt == -7:
                self.ba_v()
                return
            i = GameCanvas.r_I(paramInt)
            if i == -7:
                GameCanvas.name_buf.a_I(-8)
                return
            if i == -5 or i == 53:
                if GameCanvas.letter_cursor == 26 and len(GameCanvas.name_buf.a_v()) >= 4:
                    if len(GameCanvas.name_buf.a_v()) != 0:
                        Live.user_id = GameCanvas.name_buf.a_v()
                        GameCanvas.name_buf.a_T(Live.user_id)
                        Live.reg_step = 0
                        Live.aJ()
                        return
                else:
                    GameCanvas.name_buf.a_I(65 + GameCanvas.letter_cursor)
                    return
            elif i == -6 and len(GameCanvas.name_buf.a_v()) >= 4 and len(GameCanvas.name_buf.a_v()) != 0:
                Live.user_id = GameCanvas.name_buf.a_v()
                GameCanvas.name_buf.a_T(Live.user_id)
                Live.reg_step = 0
                Live.aJ()

    def R_I(self, paramInt):  # as.java:1330-1357  (Sale / Gift List)
        if paramInt == -3:
            Live.selected_slot = Live.selected_slot - 1 if Live.selected_slot > 0 else 4
            Live.aJ()
        elif paramInt == -4:
            Live.selected_slot = Live.selected_slot + 1 if Live.selected_slot < 4 else 0
            Live.aJ()
        elif paramInt in (-8, -5):
            if Live.list_kind == 0:
                self.aU_v()
            else:
                self.aV_v()

    def S_I(self, paramInt):  # as.java:1359-1394  (Cancel Sell: my 5 lots)
        from pow.game.menus import Menus
        if paramInt == -7:
            self.bf_v()
        elif paramInt in (-5, 53):
            if Live.lots[Live.selected_slot].id > 0:
                Live.shown_item = Live.lots[Live.selected_slot].id
                Live.flags[7] = 0 if GameCanvas.cursor[16] < 25 else 1
                GameCanvas.popups.arg1 = Menus.c_I(Live.lots[Live.selected_slot].id)
                GameCanvas.popups.d_I(39)
                Live.close_target = 14
        elif paramInt in (-3, 52):
            Live.selected_slot = Live.selected_slot - 1 if Live.selected_slot > 0 else 4
            Live.aJ()
        elif paramInt in (-4, 54):
            Live.selected_slot = Live.selected_slot + 1 if Live.selected_slot < 4 else 0
            Live.aJ()

    def T_I(self, paramInt):  # as.java:1396-1403  (Price Info list)
        if paramInt == -7:
            self.aQ_v()
            return
        self.a_IZ(paramInt, False)

    def U_I(self, paramInt):  # as.java:1405-1440  (Sell: pick an item)
        if paramInt == -7:
            self.bf_v()
            return
        if paramInt in (-5, 53):
            z1 = Live.be_v()
            if z1.id > 0:
                if 434 <= z1.id <= 437:
                    GameCanvas.popups.d_I(13)
                    return
                Live.shown_item = z1.id
                Live.enchant = i16(z1.enchant)
                Live.selected_slot = GameCanvas.cursor[18]
                if z1.id > 500:
                    Live.category = 2
                    Live.kind = i16(z1.id - 501)
                elif z1.id > 300:
                    Live.category = 1
                    Live.kind = i16(GameCanvas.item_tables[1].a_II(z1.id - 301, 7))
                else:
                    Live.category = 0
                    Live.kind = i16(GameCanvas.item_tables[0].a_II(z1.id - 101, 7))
                Live.values[13] = 0
                Live.values[14] = 0
                Live.e_Z(True)
                self.aQ_v()
            return
        self.ac_I(paramInt)

    def V_I(self, paramInt):  # as.java:1442-1489  (Sell: the price)
        bool_ = True
        if 48 <= paramInt <= 57:
            i = GameCanvas.N_I(paramInt)
            if 0 <= i <= 9 and Live.values[13] < 9:
                Live.values[14] = Live.values[14] * 10
                Live.values[14] = Live.values[14] + i
                if Live.values[14] > 0:
                    Live.values[13] = Live.values[13] + 1
        elif paramInt == -7:
            if Live.values[13] > 0:
                Live.values[14] = idiv(Live.values[14], 10)
                Live.values[13] = Live.values[13] - 1
            else:
                self.aP_v()
        elif paramInt == -5:
            if Live.values[14] > 0:
                self.c_I(800)
                Live.scroll = 0
            else:
                bool_ = False
        elif paramInt == -6:
            self.c_I(802)
            Live.scroll = 0
        else:
            bool_ = False
        if bool_:
            Live.aJ()

    def W_I(self, paramInt):  # as.java:1491-1518  (Buy: kind)
        if paramInt == -7:
            self.aY_v()
            return
        if paramInt in (-5, 53):
            if Live.kind_items[Live.category][GameCanvas.cursor[18]] != 0:
                Live.e_Z(False)
                Live.shown_item = Live.kind_items[Live.category][GameCanvas.cursor[18]]
                Live.kind = i16(GameCanvas.cursor[18])
                if Live.category == 2:
                    Live.enchant = 0
                    Live.page = 0
                    Live.page_step = 1
                    self.c_I(786)
                else:
                    Live.enchant = 0
                    self.c_I(784)
                Live.scroll = 0
                Live.aJ()
            return
        self.a_IZ(paramInt, False)

    def X_I(self, paramInt):  # as.java:1520-1556  (Buy: enchant level)
        bool_ = True
        if paramInt == -7:
            self.aL_v()                      # falls through into case -3
            Live.enchant = i16(Live.enchant - 1 if Live.enchant > 0 else 9)
        elif paramInt in (-3, 52):
            Live.enchant = i16(Live.enchant - 1 if Live.enchant > 0 else 9)
        elif paramInt in (-4, 54):
            Live.enchant = i16(Live.enchant + 1 if Live.enchant < 9 else 0)
        elif paramInt in (-2, -1, 50, 56):
            Live.enchant = i16(Live.enchant + (-5 if Live.enchant > 4 else 5))
        elif paramInt in (-5, 53):
            if Live.counts[15 - Live.enchant] > 0:
                Live.page = 0
                Live.page_step = 1
                self.c_I(786)
                Live.scroll = 0
            else:
                GameCanvas.popups.d_I(8)
        else:
            bool_ = False
        if bool_:
            Live.aJ()

    def Y_I(self, paramInt):  # as.java:1558-1608  (Buy: the lots)
        if paramInt == -7:
            if Live.category == 2:
                self.aL_v()
                return
            Live.scroll = 0
            self.c_I(784)
        elif paramInt in (-5, 53):
            GameCanvas.cursor[19] = Live.lots[GameCanvas.cursor[18]].id
            if Live.lots[GameCanvas.cursor[18]].id != 0:
                if Live.prices[GameCanvas.cursor[18]] > GameCanvas.hero.gold:
                    GameCanvas.popups.d_I(11)
                    return
                if GameCanvas.cursor[16] >= 25:
                    GameCanvas.popups.d_I(12)
                    return
                Live.selected_slot = GameCanvas.cursor[18]
                GameCanvas.popups.arg1 = str(Live.prices[GameCanvas.cursor[18]])
                GameCanvas.popups.d_I(34)
                Live.close_target = 10
            return
        else:
            i = self.a_IZ(paramInt, False)
            if i != 0:
                if i < 0:
                    if Live.page > 1:
                        Live.page_step = -1
                        Live.scroll = 0
                        self.c_I(786)
                    else:
                        GameCanvas.popups.d_I(9)
                else:
                    Live.page_step = 1
                    Live.scroll = 0
                    self.c_I(786)
            else:
                return
        Live.aJ()

    def Z_I(self, paramInt):  # as.java:1610-1626  (Buy: category)
        if paramInt == -7:
            self.bf_v()
            return
        i = self.P_I(paramInt)
        if 0 <= i <= 2:
            Live.saved_2 = i16(Live.list_cursor)
            Live.saved_3 = i16(Live.list_top)
            Live.category = i16(i)
            Live.e_Z(True)
            self.aL_v()
            return
        if i == -2:
            Live.aJ()

    def aL_v(self):  # as.java:1628-1633
        self.c_Z(False)
        Live.live_screen = 6
        Live.input_handler = 5
        Live.aJ()

    def aM_v(self):  # as.java:1635-1639
        Live.live_screen = 7
        Live.input_handler = 6
        Live.aJ()

    def aN_v(self):  # as.java:1641-1646
        self.aO_v()
        Live.live_screen = 8
        Live.input_handler = 7
        Live.aJ()

    def aO_v(self):  # as.java:1648-1650
        self.a_IIZ(4, 2, True)

    def c_Z(self, paramBoolean):  # as.java:1652-1666  (restore the grid cursor)
        Live.flags[7] = Live.saved_11
        Live.category = Live.saved_6
        if paramBoolean:
            self.a_IIZ(5 if Live.flags[7] == 0 else 20, 3, False)
        else:
            self.a_IIZ(4 if Live.category == 2 else 3, 3, False)
        GameCanvas.cursor[10] = Live.saved_7
        GameCanvas.cursor[9] = Live.saved_8
        GameCanvas.cursor[18] = Live.saved_9
        GameCanvas.cursor[8] = Live.saved_10
        Live.values[5] = Live.saved_12
        Live.values[6] = Live.saved_13

    def aP_v(self):  # as.java:1668-1674  (Sell: Backpack / Warehouse grid)
        self.c_Z(True)
        Live.input_handler = 8
        Live.live_screen = 4
        Live.title = Live.titles[5]
        Live.aJ()

    def aQ_v(self):  # as.java:1676-1681
        Live.live_screen = 9
        Live.input_handler = 9
        Live.title = Live.titles[5]
        Live.aJ()

    def d_Z(self, paramBoolean):  # as.java:1683-1695
        if paramBoolean:
            Live.scroll = 0
            Live.page = 0
            self.c_I(864)
        else:
            Live.selected_slot = 0
            Live.input_handler = 13
            Live.live_screen = 10
            Live.title = Live.titles[8]
        Live.aJ()

    def aR_v(self):  # as.java:1697-1705  (after 513: notices, Sale List, Gift List, Exp/Fame, sync)
        Live.scroll = i16(Live.scroll + Live.scroll_step)
        if Live.flags[15] == 1 and Live.first_login:
            self.c_I(516)
            Live.aJ()
            return
        self.aS_v()

    def aS_v(self):  # as.java:1707-1715
        Live.scroll = i16(Live.scroll + Live.scroll_step)
        if Live.flags[14] == 1:
            self.c_I(518)
            Live.aJ()
            return
        self.aU_v()

    def aT_v(self):  # as.java:1717-1723
        Live.selected_slot = 0
        Live.input_handler = 1
        Live.live_screen = 11
        Live.title = Live.titles[0] if Live.list_kind == 0 else Live.titles[1]
        Live.aJ()

    def aU_v(self):  # as.java:1725-1733
        Live.scroll = i16(Live.scroll + Live.scroll_step)
        if Live.flags[13] == 1:
            self.c_I(520)
            Live.aJ()
            return
        self.aV_v()

    def aV_v(self):  # as.java:1735-1744
        Live.scroll = i16(Live.scroll + Live.scroll_step)
        if GameCanvas.live_gifts == 0:
            self.c_I(258)
            Live.aJ()
            return
        GameCanvas.live_gifts = 2
        self.aW_v()

    def aW_v(self):  # as.java:1746-1750
        Live.scroll = i16(Live.scroll + Live.scroll_step)
        self.c_I(260)
        Live.aJ()

    def aX_v(self):  # as.java:1752-1756
        Live.scroll = i16(Live.scroll + Live.scroll_step)
        self.c_I(768)
        Live.aJ()

    def aa_I(self, paramInt):  # as.java:1758-1785  (Trade: Buy / Sell / Cancel)
        if paramInt == -7:
            self.aH_v()
            return
        i = self.P_I(paramInt)
        if i >= 0:
            Live.saved_2 = i16(Live.list_cursor)
            Live.saved_3 = i16(Live.list_top)
            if i == 0:
                Live.saved_4 = Live.saved_5 = 0
                self.aY_v()
            elif i == 1:
                Live.e_Z(True)
                self.aP_v()
            elif i == 2:
                Live.e_Z(True)
                self.d_Z(True)
            return
        if i == -2:
            Live.aJ()

    def ab_I(self, paramInt):  # as.java:1787-1804  (Warehouse grid: move an item)
        if paramInt == -7:
            self.aH_v()
            return
        if paramInt in (-5, 53):
            z1 = Live.be_v()
            if z1.id > 0:
                self.c_I(816)
                Live.scroll = 0
                Live.aJ()
            return
        self.ac_I(paramInt)

    def aY_v(self):  # as.java:1806-1812
        self.aZ_v()
        Live.input_handler = 4
        Live.live_screen = 5
        Live.title = Live.titles[4]
        Live.aJ()

    def aZ_v(self):  # as.java:1814-1824
        Live.e_TII("Normal Items|Special Items|Rare Items|", 20, 255)
        Live.list_cursor = Live.saved_4
        Live.list_top = Live.saved_5
        Live.aC_v()
        i = 32 + Live.aB_v()
        i = 20 + (255 - i >> 1)
        Live.values[15] = i
        Live.list_y = i + 22 + 10

    def ac_I(self, paramInt):  # as.java:1826-1841  (grid keys, -6 switches Backpack / Warehouse)
        if paramInt == -6:
            if Live.flags[7] == 1:
                self.bc_v()
                Live.aJ()
                return
            if Live.flags[7] == 0:
                self.bd_v()
                Live.aJ()
                return
        else:
            self.a_IZ(paramInt, True)

    def a_IZ(self, paramInt, paramBoolean):  # as.java:1843-1877  (grid cursor)
        fK = GameCanvas.cursor
        i = 1
        if paramInt in (-1, 50):
            fK[10] = fK[10] - 1
        elif paramInt in (-2, 56):
            fK[10] = fK[10] + 1
        elif paramInt in (-3, 52):
            fK[9] = fK[9] - 1
            if fK[9] - 1 < 0:
                fK[9] = 4
                fK[10] = fK[10] - 1
        elif paramInt in (-4, 54):
            fK[9] = fK[9] + 1
            if fK[9] + 1 >= 5:
                fK[9] = 0
                fK[10] = fK[10] + 1
        else:
            i = 0
        if i:
            i = Live.f_Z(paramBoolean)
            if i == 0:
                Live.aJ()
        return i

    def ad_I(self, paramInt):  # as.java:1879-1968  (Safe)
        bool_ = True
        if Live.flags[14] == 0:
            if paramInt in (-4, -3):
                Live.flags[15] = i16(Live.flags[15] ^ 0x1)
            elif paramInt in (-1, 50):
                Live.flags[15] = 0
            elif paramInt in (-2, 56):
                Live.flags[15] = 1
            elif paramInt == -7:
                self.aH_v()
                GameCanvas.images[22] = None
                GameCanvas.images[24] = None
            elif paramInt in (-5, 53):
                if Live.flags[15] == 0:
                    Live.values[15] = Live.safe_gold
                    if Live.safe_gold == 0:
                        GameCanvas.popups.d_I(14)
                else:
                    Live.values[15] = GameCanvas.hero.gold
                    if GameCanvas.hero.gold == 0:
                        GameCanvas.popups.d_I(15)
                if Live.values[15] > 0:
                    Live.flags[14] = 1
                    Live.values[14] = 0
                    Live.live_screen = 3
                    Live.aJ()
            else:
                bool_ = False
        else:
            if 48 <= paramInt <= 57:
                i = GameCanvas.N_I(paramInt)
                if i != -1:
                    Live.values[14] = Live.values[14] * 10
                    Live.values[14] = Live.values[14] + i
                    if Live.values[14] > Live.values[15]:
                        Live.values[14] = Live.values[15]
            elif paramInt == -7:
                if Live.values[14] > 0:
                    Live.values[14] = idiv(Live.values[14], 10)
                else:
                    Live.flags[14] = 0
                    Live.live_screen = 2
                    Live.aJ()
            elif paramInt == -5:
                if Live.values[14] > 0:
                    self.c_I(832)
                    Live.flags[14] = 0
                    Live.live_screen = 2
                    Live.aJ()
                else:
                    bool_ = False
            else:
                bool_ = False
        if bool_:
            Live.aJ()

    def ba_v(self):  # as.java:1970-1978  (leave Gamevil Live -> Game Menu)
        GameCanvas.state = 2
        self.o_v()
        GameCanvas.redraw = 1
        GameCanvas.menu[0] = 0
        GameCanvas.menu[1] = 2
        GameCanvas.popups.from_gamestr = 0
        GameCanvas.in_live = False

    @staticmethod
    def e_Z(paramBoolean):  # as.java:1980-1999  (remember / reset the grid cursor)
        Live.saved_6 = Live.category
        if paramBoolean:
            Live.saved_7 = Live.saved_8 = Live.saved_9 = Live.saved_10 = Live.saved_11 = Live.saved_12 = Live.saved_13 = 0
            return
        Live.saved_11 = Live.flags[7]
        Live.saved_7 = i16(GameCanvas.cursor[10])
        Live.saved_8 = i16(GameCanvas.cursor[9])
        Live.saved_9 = i16(GameCanvas.cursor[18])
        Live.saved_10 = i16(GameCanvas.cursor[8])
        Live.saved_12 = i16(Live.values[5])
        Live.saved_13 = i16(Live.values[6])

    def bb_v(self):  # as.java:2001-2007  (Warehouse screen)
        self.bc_v()
        Live.input_handler = 14
        Live.live_screen = 4
        Live.title = Live.titles[9]
        Live.aJ()

    def bc_v(self):  # as.java:2009-2012
        Live.flags[7] = 0
        self.a_IIZ(5, 3, True)

    def bd_v(self):  # as.java:2014-2017
        Live.flags[7] = 1
        self.a_IIZ(20, 3, True)

    def a_IIZ(self, paramInt1, paramInt2, paramBoolean):  # as.java:2019-2043  (grid geometry)
        fK = GameCanvas.cursor
        fK[3] = paramInt2
        fK[6] = 32 * paramInt2 - 4 + 2
        fK[4] = paramInt1
        fK[7] = 32 * paramInt1 - 4 + 2
        c = 156                              # char c = '\u009c'
        if paramInt2 < paramInt1:
            c += 8
            fK[11] = 1
            fK[13] = fK[6] * (fK[6] - 2) * 10
            fK[13] = idiv(idiv(fK[13], fK[7]) + 9, 10)
        else:
            fK[11] = 0
        fK[5] = 240 - c >> 1
        fK[12] = fK[5] + 156 + 4
        fK[26] = -1
        fK[27] = 0
        if paramBoolean:
            fK[8] = 0
            fK[10] = 0
            fK[9] = 0
            Live.f_Z(True)

    @staticmethod
    def f_Z(paramBoolean):  # as.java:2045-2072  (clamp the grid cursor; -1 / 1 = left the grid)
        fK = GameCanvas.cursor
        if fK[10] < 0:
            if paramBoolean:
                fK[10] = fK[4] - 1
            else:
                fK[10] = Live.values[5]
                fK[9] = Live.values[6]
                return -1
        elif fK[10] >= fK[4]:
            if paramBoolean:
                fK[10] = 0
            else:
                fK[10] = Live.values[5]
                fK[9] = Live.values[6]
                return 1
        Live.values[5] = fK[10]
        Live.values[6] = fK[9]
        if fK[10] < fK[8]:
            fK[8] = fK[10]
        elif fK[10] >= fK[8] + fK[3]:
            fK[8] = fK[10] - fK[3] + 1
        fK[18] = fK[10] * 5 + fK[9]
        return 0

    @staticmethod
    def be_v():  # as.java:2074-2081  (the selected item of the Backpack / Warehouse grid)
        if Live.flags[7] == 0:
            Live.selected_serial = Live.backpack_serials[GameCanvas.cursor[18]]
            return GameCanvas.hero.backpack[GameCanvas.cursor[18]]
        Live.selected_serial = Live.warehouse_serials[GameCanvas.cursor[18]]
        return Live.warehouse[GameCanvas.cursor[18]]

    def bf_v(self):  # as.java:2083-2093  (Trade menu)
        Live.e_TII("Buy Item|Sell Item|Cancel Sell|", 26, 243)
        Live.list_cursor = Live.saved_2
        Live.list_top = Live.saved_3
        Live.aC_v()
        Live.input_handler = 3
        Live.live_screen = 1
        Live.title = Live.titles[3]
        Live.aJ()

    def ae_I(self, paramInt):  # as.java:2095-2126  (GAMEVIL LIVE menu)
        if paramInt == -7:
            self.ba_v()
            if GameCanvas.live_saved == 0:
                return
        else:
            i = self.P_I(paramInt)
            if i >= 0:
                Live.saved_0 = i16(Live.list_cursor)
                Live.saved_1 = i16(Live.list_top)
                if i == 0:
                    Live.saved_2 = Live.saved_3 = 0
                    self.bf_v()
                elif i == 1:
                    Live.e_Z(True)
                    self.bb_v()
                elif i == 2:
                    self.bg_v()
                elif i == 3:
                    self.bh_v()
                return
            if i == -2:
                Live.aJ()

    def bg_v(self):  # as.java:2128-2135  (Safe)
        Live.flags[15] = 0
        Live.flags[14] = 0
        Live.input_handler = 15
        Live.live_screen = 2
        Live.title = Live.titles[10]
        Live.aJ()

    def bh_v(self):  # as.java:2137-2143  (Management)
        Live.e_TII("Save User Data|Load User Data|", 26, 243)
        Live.input_handler = 16
        Live.title = Live.titles[11]
        Live.aJ()

    def af_I(self, paramInt):  # as.java:2145-2159  (Management keys)
        if paramInt == -7:
            self.aH_v()
            return
        i = self.P_I(paramInt)
        if 0 <= i <= 1:
            Live.flags[14] = i16(i)
            GameCanvas.popups.d_I(16 if i == 0 else 17)
            Live.close_target = 9
            return
        if i == -2:
            Live.aJ()

    @staticmethod
    def bi_v():  # as.java:2161-2164
        LiveNet.running = False
        Live.net = None
