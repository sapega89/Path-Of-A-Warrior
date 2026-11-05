"""as.java - Gamevil Live of the single player (PHASE_7): its menus, the input and the
requests / answers. Literal port; the drawing is m.java (pow/game/m.py).

as is static state (every field is static in Java) plus an ag subclass instance (ag.be) whose
methods ag.run / ag.t / ag.L call. The server it talks to is pow_server/live.py, through
pow/game/v.py. Screens (ho, drawn by m.a()): 1 list, 2 Safe, 3 amount, 4 Backpack/Warehouse,
5 categories, 6 kinds, 7 enchant levels, 8 lots, 9 price, 10 Cancel, 11 Sale/Gift List,
12 waiting, 13 registration. Input handlers (hp): see t(int).

Fixes (config):
- DECOMP_FIX F6: the Backpack / Warehouse grid cursor (as.a(int, boolean)) has the same broken
  `--fK[9] < 0` / `++fK[9] >= 5`: LEFT from column 1 and RIGHT from column 3 jumped over the
  edge cell to the next row, so columns 0 and 4 could not be reached sideways.
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
from pow.game.gfx import Gfx
from pow.game.key_grid import KeyGrid
from pow.game.live_net import LiveNet
from pow.game.live_online import Online
from pow.game.structs import Item
from pow.midp import system
from pow.midp.graphics import Image
from pow.midp.jint import i8, i16, idiv

F20 = config.DECOMP_FIX["F20"]
F6 = config.DECOMP_FIX["F6"]
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
    auto_mp = False            # PORT-EXTRA: open Multiplayer as soon as the Live menu is reached
    id_grid = None             # PORT-EXTRA: KeyGrid of the UserID (config.REG_KEYBOARD)
    pwd_grid = None            # PORT-EXTRA: KeyGrid of the password
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
    backpack_serials = None           # short[25] backpack serials (PORT-EXTRA config.BACKPACK_SIZE)
    warehouse = [None] * config.WAREHOUSE_SIZE   # z[100] warehouse (PORT-EXTRA config.WAREHOUSE_SIZE)
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
            Live.backpack_serials = [0] * config.BACKPACK_SIZE
        if Live.warehouse_serials is None:
            Live.warehouse_serials = [0] * config.WAREHOUSE_SIZE

    def open_live(self):  # as.java:180-190  (Game Menu > Gamevil Live)
        from pow.game.live_screen import LiveScreen
        Live.inited = True
        if LiveScreen.is_registered():
            Live.reg_from_popup = False
            Live.screen.load_login()
            if Online.enabled():             # PORT-EXTRA: no "Connect to Gamevil Live?"
                self.connect_live()
                return
            GameCanvas.popups.show(2)
            Live.close_target = 2
            return
        self.open_registration()

    def open_registration(self):  # as.java:192-208  (registration screen)
        from pow.game.name_buffer import NameBuffer
        GameCanvas.in_live = True
        GameCanvas.stop_sound()
        Live.title = "Registration"
        Live.live_screen = 13
        Live.input_handler = 18
        Live.reg_step = 1
        GameCanvas.letter_cursor = 0
        if config.REG_KEYBOARD:        # PORT-EXTRA: the on-screen keyboards (pow/game/key_grid.py)
            Live.id_grid, Live.pwd_grid = KeyGrid.user_id(), KeyGrid.password()
        Live.request_redraw()
        GameCanvas.state = 11
        Live.password = ""
        Live.user_id = ""
        GameCanvas.name_buf = None
        GameCanvas.name_buf = NameBuffer("", 12, 10)
        self.load_live_images()
        Live.request_redraw()

    def tick_live(self):  # as.java:210-299  (every frame from ag.run)
        if Live.net is not None:
            Live.net.pump()
        Online.tick(self)                    # PORT-EXTRA: the background login (live_online.py)
        if Live.pending_request != -1 and not Online.background:
            self.queue_request(Live.pending_request)
        if GameCanvas.popups.answered:
            GameCanvas.popups.answered = False
            i = Live.close_target
            Live.close_target = -1
            button = GameCanvas.popups.button
            if i == 3:
                self.leave_live()
                Live.request_redraw()
            elif i == 2:
                if button == 0:
                    self.connect_live()
                else:
                    self.leave_live()
                    Live.request_redraw()
            elif i == 7:
                if Live.flags[15] > 0:
                    self.ask_request(516)
                else:
                    self.sync_sale_list()
            elif i == 8:
                self.sync_done()
            elif i == 9:
                if button == 0:
                    bool_ = False
                    if Live.flags[14] == 1:
                        for b in range(9):
                            if GameCanvas.hero.equipped[b].id > 0:
                                bool_ = True
                                break
                        if bool_:
                            GameCanvas.popups.show(33)
                            return self._end_tick()
                    Live.scroll = 0
                    if Live.flags[14] == 0:
                        self.ask_request(256)
                    else:
                        self.ask_request(262)
            elif i == 10:
                if button == 0:
                    if GameCanvas.cursor[16] < config.BACKPACK_SIZE:
                        Live.flags[7] = 0
                        Live.scroll = 0
                        self.ask_request(788)
                    else:
                        GameCanvas.popups.show(12)
                        Live.close_target = 11
            elif i == 11:
                if button == 0:
                    Live.flags[7] = 1
                    Live.scroll = 0
                    self.ask_request(788)
            elif i == 14:
                if button == 0:
                    Live.scroll = 0
                    self.ask_request(866)
                    Live.screen_redraw = True
        self._end_tick()

    def connect_live(self):  # as.java:226-232  (popup 2 YES: into Gamevil Live, request 512)
        GameCanvas.in_live = True
        GameCanvas.stop_sound()
        self.load_live_images()
        self.enter_live()
        self.open_waiting()
        self.ask_request(512)

    def _end_tick(self):
        if Live.waiting:
            self.check_answer()

    @staticmethod
    def show_error(code):  # as.java:301-353  (error code -> gamestr popup)
        b = {-1: 21, -2: 22, -4: 23, -12: 24, -13: 25, -15: 26, -16: 27, -18: 28, -20: 29,
             -22: 30, -23: 31, -26: 7, -49: 54}.get(code, -1)
        if code == -26:
            Live.close_target = 3
        elif code == -11:
            b = 10 if Live.page > 0 else 8
        if b != -1:
            GameCanvas.popups.show(b)

    @staticmethod
    def quiet_request():
        """PORT-EXTRA (config.ALWAYS_ONLINE): no "Connecting..." for a request over the connection
        that is already open, unless its answer takes longer than QUIET_MS."""
        return (Online.enabled() and LiveNet.connected
                and system.currentTimeMillis() - Live.request_time < Online.QUIET_MS)

    def draw_connecting(self):  # as.java:355-364  ("Connecting..." over the screen)
        GameCanvas.popups.draw_popup_frame(96)
        i = GameCanvas.view_cy - 20 - 10
        j = Live.loading0.getWidth()
        bar_h = Live.loading0.getHeight()
        GameCanvas.draw_region((GameCanvas.screen_w - j) // 2, i, j, bar_h, Live.loading0, 0, 0)
        GameCanvas.draw_region((GameCanvas.screen_w - j) // 2, i, j * (GameCanvas.frame % 6) // 5, bar_h, Live.loading1, 0, 0)
        Gfx.set_font(GameCanvas.font_white)
        Gfx.draw_string("Connecting...", GameCanvas.screen_w // 2, i + 50, 1)

    def load_live_images(self):  # as.java:366-378
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
        Live.start_net()

    @staticmethod
    def start_net():  # as.java:380-386
        if Live.net is None:
            Live.net = LiveNet()
            Live.net.setPriority(5)
            Live.net.start()

    def on_connected(self):  # as.java:388-390  (s.f(): connected)
        self.write_request()

    def ask_request(self, opcode):  # as.java:392-397  (ask for a request on the next i())
        Live.answer_status = 0
        GameCanvas.lock_keys()
        Live.busy = True
        Live.pending_request = opcode

    def queue_request(self, opcode):  # as.java:399-413
        Live.pending_request = -1
        Live.login_request = 0
        if not LiveNet.connected:
            Live.login_request = opcode
            Live.request_in_flight = 530
        else:
            Live.request_in_flight = opcode
        Live.request_time = system.currentTimeMillis()
        Live.waiting = False
        self.send_request(Live.request_in_flight)
        Live.request_redraw()
        Live.waiting = True

    def check_answer(self):  # as.java:415-438  (answer came / timeout)
        if Online.background:                # PORT-EXTRA: the background 530, no screen to update
            self.check_background_answer()
            return
        if Live.answered:
            if not Live.in_answer:
                GameCanvas.unlock_keys()
                Live.waiting = False
                Live.busy = False
                Live.request_redraw()
        elif LiveNet.waiting and not Live.in_answer and (GameCanvas.key == -7 or system.currentTimeMillis() > Live.request_time + 30000):
            Live.answer_status = -1
            if Live.net is not None:
                Live.net.close()
                Live.drop_net()
                GameCanvas.gc()
            Live.busy = False
            self.on_error_answer(Live.request_in_flight + 1, Live.answer_status, None)
            Live.request_redraw()
        if Live.answer_status == 1 and Live.request_in_flight == 530 and Live.login_request != 530:
            Live.request_in_flight = Live.login_request
            self.ask_request(Live.request_in_flight)

    def check_background_answer(self):
        """PORT-EXTRA: check_answer() for the background login: silent, keys never locked."""
        if Live.answered:
            if not Live.in_answer:
                Live.waiting = False
                Online.on_login_answer(Live.answer_op == 531 and Live.answer_status == 1 and LiveNet.connected)
        elif system.currentTimeMillis() > Live.request_time + 30000:
            if Live.net is not None:
                Live.net.close()
                Live.drop_net()
            Live.waiting = False
            Online.on_login_answer(False)

    def send_request(self, opcode):  # as.java:440-451
        Live.request_in_flight = opcode
        if not LiveNet.connected:
            if Live.net is None:
                Live.start_net()
            LiveNet.set_listener(self)
            Live.net.set_address(GameCanvas.live_host, GameCanvas.live_port)
        else:
            self.write_request()
        Live.answered = False

    def write_request(self):  # as.java:453-576  (write the request gq)
        hero = GameCanvas.hero
        Live.answer_status = 0
        Live.net.begin_request(Live.request_in_flight)
        op = Live.request_in_flight
        if op == 530:
            LiveNet.write_string(Live.user_id, 12)
            LiveNet.write_string(Live.password, 16)
            LiveNet.write_string("1501", 4)
            LiveNet.write_int(Live.session_id)
            Live.session_new = system.currentTimeMillis() // 10000
            LiveNet.write_int(Live.session_new)
        elif op in (516, 256):
            LiveNet.write_int(hero.fame)
            LiveNet.write_int(hero.exp)
            LiveNet.write_short(hero.level)
            LiveNet.write_byte(hero.head)
            LiveNet.write_byte(GameCanvas.item_slot_type(hero.equipped[0].id) ^ 0x1)
            LiveNet.write_short(hero.base_attack)
            LiveNet.write_short(hero.base_defense)
            LiveNet.write_short(hero.base_hp)
            LiveNet.write_short(hero.base_mp)
            LiveNet.write_short(hero.stat_points)
            GameCanvas.update_hero_stats()
            LiveNet.write_short(hero.gear_attack)
            LiveNet.write_short(hero.gear_defense)
            LiveNet.write_short(hero.gear_hp)
            LiveNet.write_short(hero.gear_mp)
            for i_stat in range(8):
                LiveNet.write_int(GameCanvas.stats[i_stat])
            b = 0
            for i_cat in range(len(hero.skill_levels)):
                if hero.skill_levels[i_cat] > 0:
                    b += 1
            LiveNet.write_byte(b)
            for i_skill in range(len(hero.skill_levels)):
                if hero.skill_levels[i_skill] > 0:
                    LiveNet.write_byte(Live.category_codes[i_skill])
                    LiveNet.write_byte(hero.skill_levels[i_skill])
                    bool_ = False
                    for i_key in range(4):
                        if hero.hotkeys[i_key] - 12 == i_skill:
                            bool_ = True
                            break
                    LiveNet.write_bool(bool_)
            LiveNet.write_string(hero.name, 8)
            LiveNet.write_bool(hero.live_registered != 0)
            LiveNet.write_byte(GameCanvas.general_count & 0xFF)
            for i_gen in range(GameCanvas.general_count):
                LiveNet.write_byte(GameCanvas.generals[0][i_gen] & 0xFF)
                LiveNet.write_byte(GameCanvas.generals[1][i_gen] & 0xFF)
            LiveNet.write_int(GameCanvas.missions_done & 0xFFFFFFFF)
            LiveNet.write_int(GameCanvas.missions_done >> 32 & 0xFFFFFFFF)
            LiveNet.write_byte(GameCanvas.chapter)
            for i_mis in range(22):
                LiveNet.write_byte(hero.mission_progress[i_mis] & 0xFF)
            LiveNet.write_byte(hero.live_stat1 & 0xFF)
            LiveNet.write_byte(hero.live_stat2 & 0xFF)
            LiveNet.write_int(GameCanvas.score)
        elif op == 768:
            from pow.game.menus import Menus
            LiveNet.write_int(hero.gold)
            Menus.count_items()
            slot_count = i8(GameCanvas.cursor[16])
            LiveNet.write_byte(slot_count)
            for i_item in range(config.BACKPACK_SIZE):
                if hero.backpack[i_item].id > 0:
                    LiveNet.write_short(hero.backpack[i_item].id)
                    Live.backpack_serials[i_item] = i16(i_item + 1)
                    LiveNet.write_short(Live.backpack_serials[i_item])
                    LiveNet.write_byte(hero.backpack[i_item].enchant)
                    LiveNet.write_short(hero.backpack[i_item].attack)
                    LiveNet.write_short(hero.backpack[i_item].defense)
                    LiveNet.write_short(hero.backpack[i_item].hp)
                    LiveNet.write_short(hero.backpack[i_item].mp)
        elif op == 832:
            LiveNet.write_byte(Live.flags[15] ^ 0x1)
            LiveNet.write_int(Live.values[14])
        elif op == 816:
            LiveNet.write_byte(Live.flags[7])
            LiveNet.write_short(Live.selected_serial)
        elif op in (784, 786, 788, 800):     # case 784 / 786 / 788 / 800 fall through
            if op == 784:
                LiveNet.write_byte(Live.category + 1)
            if op in (784, 786):
                LiveNet.write_byte(Live.category + 1)
                LiveNet.write_byte(Live.kind + 1)
                LiveNet.write_byte(Live.enchant)
            if op in (784, 786, 788):
                LiveNet.write_int(Live.lot_ids[GameCanvas.cursor[18]])
            LiveNet.write_byte(Live.flags[7])
            LiveNet.write_short(Live.selected_serial)
            LiveNet.write_int(Live.values[14])
        elif op in (802, 866):               # case 802 falls through into 866
            if op == 802:
                LiveNet.write_byte(Live.category + 1)
                LiveNet.write_byte(Live.kind + 1)
            LiveNet.write_int(Live.lot_ids[Live.selected_slot])
            LiveNet.write_byte(0 if GameCanvas.cursor[16] < config.BACKPACK_SIZE else 1)
        Live.net.send_request()

    def disconnect(self):  # as.java:578-591
        if not (Online.enabled() and Online.wanted):   # PORT-EXTRA: else the connection stays
            self.close_net()
        if GameCanvas.state == 11:
            Live.close_target = 3
            GameCanvas.popups.show(29)
        Live.busy = False
        Live.waiting = False
        GameCanvas.sleep(300)

    def close_net(self):
        LiveNet.connected = False
        if Live.net is not None:
            Live.net.close()
            Live.drop_net()

    def on_connection_failed(self):  # as.java:593-599  (s.e(): the connection failed / broke)
        if Live.net is not None:
            Live.net.close()
            Live.drop_net()
        Live.answered = True

    @staticmethod
    def _copy_item(dst, src):
        dst.id, dst.attack, dst.defense, dst.hp, dst.mp, dst.enchant = src.id, src.attack, src.defense, src.hp, src.mp, src.enchant

    def on_answer(self, answer):  # as.java:601-990  (s.a(ab): one answer)
        Live.in_answer = True
        LiveNet.waiting = False
        op = answer.read_s16()
        b = answer.read_s8()
        if F20:
            Live.answer_status = b                      # DECOMP_FIX F20
        Live.answer_op = op
        if B5 and op == 531:
            Live.blink = False                  # ORIG-BUG B5
        if b == 1:
            handler = self._ANSWER_BY_OPCODE.get(op)
            if handler is not None:
                handler(self, answer, op)
        else:
            self.on_error_answer(Live.answer_op, Live.answer_status if F20 else 0, answer)
        Live.in_answer = False
        LiveNet.waiting = True
        Live.answered = True

    def _on_login(self, answer, op):  # answer 531
        Live.session_id = Live.session_new
        if not Online.background:            # PORT-EXTRA: the background login saves nothing
            self.save_game()
        answer.read_s8()
        answer.read_s8()
        result = answer.read_s8()
        if (result in {0, 2}) and Live.reg_from_popup:
            from pow.game.live_screen import LiveScreen
            LiveScreen.save_login()
            if result == 0:
                GameCanvas.popups.show(48)
            elif result == 2:
                GameCanvas.popups.show(44)
            Live.close_target = 2
            Live.reg_from_popup = False
            if Online.offer_open:            # PORT-EXTRA: the offered registration: back to the game
                Online.on_registration_closed(True)
                Live.close_target = 3

    def _on_status(self, answer, op):  # answer 513
        Live.flags[15] = answer.read_s8()
        Live.flags[14] = answer.read_s8()
        Live.flags[13] = answer.read_s8()
        answer.read_s8()
        for _ in range(5):
            answer.read_s32()
        Live.flags[4] = answer.read_s8()
        Live.flags[5] = answer.read_s8()
        self.after_login()
        Live.request_redraw()

    def _on_notices(self, answer, op):  # answer 517
        GameCanvas.popups.arg1 = GameCanvas.trim_right(GameCanvas.cut_at_control(answer.read_string(16)))
        GameCanvas.popups.arg2 = GameCanvas.trim_right(GameCanvas.cut_at_control(answer.read_string(16)))
        GameCanvas.popups.arg3 = GameCanvas.trim_right(GameCanvas.cut_at_control(answer.read_string(16)))
        GameCanvas.popups.arg4 = GameCanvas.trim_right(GameCanvas.cut_at_control(answer.read_string(16)))
        GameCanvas.popups.show(53)
        Live.close_target = 7
        if answer.read_s8() == 1:
            Live.flags[15] = i16(Live.flags[15] + 1)
        else:
            Live.flags[15] = 0

    def _on_sale_list(self, answer, op):  # answer 519
        for idx in range(20):
            if Live.lots[idx] is None:
                Live.lots[idx] = Item()
            Item.clear(Live.lots[idx])
            Live.prices[idx] = 0
        lot_count = answer.read_s8()
        for idx in range(lot_count):
            Live.lots[idx].id = answer.read_s16()
            Live.lots[idx].enchant = answer.read_s8()
            Live.prices[idx] = answer.read_s32()
        Live.list_kind = 0
        self.open_trade_list()

    def _on_exp_fame_saved(self, answer, op):  # answer 261
        GameCanvas.live_gifts = i16(GameCanvas.live_gifts - 1)
        if GameCanvas.live_gifts == 0:
            self.save_game()
            if Live.values[15] == 0 and Live.values[14] == 0:
                if Live.first_login and not Online.enabled():
                    GameCanvas.popups.show(20)   # PORT-EXTRA: online, the Multiplayer screens
                else:                             # pay the hero at once (after_multiplayer)
                    GameCanvas.popups.answered = True
            else:
                GameCanvas.popups.arg1 = str(Live.values[14])
                GameCanvas.popups.arg2 = str(Live.values[15])
                GameCanvas.popups.arg3 = str(Live.values[13])
                GameCanvas.popups.show(41)
            Live.close_target = 8
        else:
            GameCanvas.live_gifts = 0
            self.sync_gifts()

    def _on_user_data_loaded(self, answer, op):  # answer 263
        hero = GameCanvas.hero
        hero.fame = answer.read_s32()
        hero.exp = answer.read_s32()
        hero.level = answer.read_s16() & 0xFF
        hero.head = answer.read_s8()
        hero.weapon_kind = answer.read_s8()
        hero.base_attack = answer.read_s16()
        hero.base_defense = answer.read_s16()
        hero.base_hp = answer.read_s16()
        hero.base_mp = answer.read_s16()
        hero.stat_points = answer.read_s16()
        for idx in range(len(hero.skill_levels)):
            hero.skill_levels[idx] = 0
        for idx in range(len(hero.hotkeys)):
            hero.hotkeys[idx] = 0
        count = answer.read_s8()
        idx = 0
        hotkey = 0
        while idx < count:
            code = answer.read_s8()
            cat = 0
            while cat < 19 and Live.category_codes[cat] != code:
                cat += 1
            hero.skill_levels[cat] = answer.read_s8()
            code = answer.read_s8()
            if code == 1:
                hero.hotkeys[hotkey] = cat + 12
                hotkey += 1
            idx += 1
        for idx in range(8):
            GameCanvas.stats[idx] = answer.read_s32()
        hero.name = GameCanvas.cut_at_space(GameCanvas.cut_at_control(answer.read_string(8)))
        hero.live_registered = answer.read_s8()
        for idx in range(45):
            GameCanvas.generals[0][idx] = 0
            GameCanvas.generals[1][idx] = 0
        GameCanvas.general_count = i16(answer.read_s8())
        for idx in range(GameCanvas.general_count):
            GameCanvas.generals[0][idx] = i16(answer.read_s8())
            GameCanvas.generals[1][idx] = i16(answer.read_s8())
        i = answer.read_s32()
        GameCanvas.missions_done = answer.read_s32()
        GameCanvas.missions_done <<= 32
        GameCanvas.missions_done |= i                  # sic: a negative low word fills the high one (Java long |)
        GameCanvas.chapter = answer.read_s8()
        for idx in range(22):
            hero.mission_progress[idx] = i16(answer.read_s8())
        hero.live_stat1 = i16(answer.read_s8())
        hero.live_stat2 = i16(answer.read_s8())
        GameCanvas.score = answer.read_s32()
        self.save_game()
        GameCanvas.popups.show(19)

    def _on_user_data_saved(self, answer, op):  # answer 257
        GameCanvas.popups.show(18)

    def _on_sync(self, answer, op):  # answer 769
        Live.safe_gold = answer.read_s32()
        for idx in range(config.WAREHOUSE_SIZE):
            if Live.warehouse[idx] is None:
                Live.warehouse[idx] = Item()
            Item.clear(Live.warehouse[idx])
        Live.flags[6] = i16(answer.read_s8() & 0xFF)
        for idx in range(len(Live.warehouse)):
            Item.clear(Live.warehouse[idx])
        for idx in range(Live.flags[6]):
            Live.warehouse[idx].id = answer.read_s16()
            Live.warehouse_serials[idx] = answer.read_s16()
            Live.warehouse[idx].enchant = answer.read_s8()
            Live.warehouse[idx].attack = answer.read_s16()
            Live.warehouse[idx].defense = answer.read_s16()
            Live.warehouse[idx].hp = answer.read_s16()
            Live.warehouse[idx].mp = answer.read_s16()
        self.open_live_menu()

    def _on_safe(self, answer, op):  # answer 833
        hero = GameCanvas.hero
        hero.gold = answer.read_s32()
        Live.safe_gold = answer.read_s32()

    def _on_warehouse(self, answer, op):  # answer 817
        hero = GameCanvas.hero
        cursor = GameCanvas.cursor
        if Live.flags[7] == 0:
            Live.list_rows = config.WAREHOUSE_SIZE
            cursor[16] = cursor[16] - 1
            Live.flags[6] = i16(Live.flags[6] + 1)
            idx = 0
            while idx < Live.list_rows and Live.warehouse[idx].id != 0:
                idx += 1
            Live._copy_item(Live.warehouse[idx], hero.backpack[cursor[18]])
            Item.clear(hero.backpack[cursor[18]])
            Live.warehouse_serials[idx] = answer.read_s16()
            Live.backpack_serials[cursor[18]] = 0
        else:
            Live.list_rows = config.BACKPACK_SIZE
            Live.flags[6] = i16(Live.flags[6] - 1)
            cursor[16] = cursor[16] + 1
            idx = 0
            while idx < Live.list_rows and hero.backpack[idx].id != 0:
                idx += 1
            Live._copy_item(hero.backpack[idx], Live.warehouse[cursor[18]])
            Item.clear(Live.warehouse[cursor[18]])
            Live.backpack_serials[idx] = answer.read_s16()
            Live.warehouse_serials[cursor[18]] = 0
        self.save_and_sync(0)
        Live.request_redraw()

    def _on_lot_counts(self, answer, op):  # answer 785
        idx = 0
        count_slot = 15
        while idx < 10:
            Live.counts[count_slot] = answer.read_s8()
            idx += 1
            count_slot -= 1
        self.open_cancel_sell()

    def _on_gift_list(self, answer, op):  # answer 521
        for idx in range(5):
            if Live.lots[idx] is None:
                Live.lots[idx] = Item()
            Item.clear(Live.lots[idx])
            Live.gift_from[idx] = ""
        lot_count = answer.read_s8()
        for idx in range(lot_count):
            Live.gift_from[idx] = GameCanvas.cut_at_control(answer.read_string(8))
            Live.lots[idx].id = answer.read_s16()
            Live.lots[idx].enchant = answer.read_s8()
            Live.lots[idx].attack = answer.read_s16()
            Live.lots[idx].defense = answer.read_s16()
            Live.lots[idx].hp = answer.read_s16()
            Live.lots[idx].mp = answer.read_s16()
        Live.flags[13] = answer.read_s8()
        Live.list_kind = 1
        self.open_trade_list()

    def _on_lots_page(self, answer, op):  # answer 787
        for idx in range(20):
            if Live.lots[idx] is None:
                Live.lots[idx] = Item()
            Item.clear(Live.lots[idx])
            Live.lot_ids[idx] = 0
            Live.prices[idx] = 0
        count = answer.read_s8()
        for idx in range(count):
            Live.lot_ids[idx] = answer.read_s32()
            Live.lots[idx].id = answer.read_s16()
            Live.prices[idx] = answer.read_s32()
            Live.lots[idx].enchant = answer.read_s8()
            Live.lots[idx].attack = answer.read_s16()
            Live.lots[idx].defense = answer.read_s16()
            Live.lots[idx].hp = answer.read_s16()
            Live.lots[idx].mp = answer.read_s16()
        Live.page = i8(Live.page + Live.page_step)
        self.open_sale_list()

    def _on_bought(self, answer, op):  # answer 789
        hero = GameCanvas.hero
        cursor = GameCanvas.cursor
        if B4 and Live.flags[7] == 1:     # ORIG-BUG B4: bought into the warehouse
            Live.flags[6] = i16(Live.flags[6] + 1)
            idx = 0
            while idx < config.WAREHOUSE_SIZE and Live.warehouse[idx].id != 0:
                idx += 1
            Live._copy_item(Live.warehouse[idx], Live.lots[cursor[18]])
            Live.clear_selected_lot()
            Live.warehouse_serials[idx] = answer.read_s16()
        else:
            Live.list_rows = config.BACKPACK_SIZE
            cursor[16] = cursor[16] + 1
            idx = 0
            while idx < Live.list_rows and hero.backpack[idx].id != 0:
                idx += 1
            Live._copy_item(hero.backpack[idx], Live.lots[cursor[18]])
            Live.clear_selected_lot()
            Live.backpack_serials[idx] = answer.read_s16()
        hero.gold = answer.read_s32()
        Live.safe_gold = answer.read_s32()
        self.save_and_sync(0)
        GameCanvas.popups.show(35)

    def _on_put_on_sale(self, answer, op):  # answer 801
        hero = GameCanvas.hero
        cursor = GameCanvas.cursor
        if Live.flags[7] == 0:
            Item.clear(hero.backpack[Live.selected_slot])
            Live.backpack_serials[Live.selected_slot] = 0
            cursor[16] = cursor[16] - 1
        else:
            Item.clear(Live.warehouse[Live.selected_slot])
            Live.warehouse_serials[Live.selected_slot] = 0
            Live.flags[6] = i16(Live.flags[6] - 1)
        self.save_and_sync(0)
        GameCanvas.popups.show(36)
        self.open_sell_grid()

    def _on_price_info(self, answer, op):  # answer 803/865
        for idx in range(20):
            if Live.lots[idx] is None:
                Live.lots[idx] = Item()
            Item.clear(Live.lots[idx])
            Live.lot_ids[idx] = 0
            Live.prices[idx] = 0
        count = answer.read_s8()
        count = min(count, 20)
        for idx in range(count):
            if op == 865:
                Live.lot_ids[idx] = answer.read_s32()
            Live.lots[idx].id = answer.read_s16()
            Live.prices[idx] = answer.read_s32()
            Live.lots[idx].enchant = answer.read_s8()
            Live.lots[idx].attack = answer.read_s16()
            Live.lots[idx].defense = answer.read_s16()
            Live.lots[idx].hp = answer.read_s16()
            Live.lots[idx].mp = answer.read_s16()
        if op == 803:
            self.set_cancel_sell_grid()
            Live.live_screen = 8
            Live.input_handler = 10
            Live.title = Live.titles[6]
            Live.request_redraw()
        else:
            self.open_buy_lots(False)

    def _on_lot_cancelled(self, answer, op):  # answer 867
        hero = GameCanvas.hero
        cursor = GameCanvas.cursor
        if Live.flags[7] == 0:
            Live.list_rows = config.BACKPACK_SIZE
            Live.flags[6] = i16(Live.flags[6] - 1)
            cursor[16] = cursor[16] + 1
            idx = 0
            while idx < Live.list_rows and hero.backpack[idx].id != 0:
                idx += 1
            Live._copy_item(hero.backpack[idx], Live.lots[Live.selected_slot])
            Item.clear(Live.lots[Live.selected_slot])
            Live.clear_selected_lot()
            Live.backpack_serials[idx] = answer.read_s16()
        else:
            Live.list_rows = config.WAREHOUSE_SIZE
            cursor[16] = cursor[16] - 1
            Live.flags[6] = i16(Live.flags[6] + 1)
            idx = 0
            while idx < Live.list_rows and Live.warehouse[idx].id != 0:
                idx += 1
            Live._copy_item(Live.warehouse[idx], Live.lots[Live.selected_slot])
            Item.clear(Live.lots[Live.selected_slot])
            Live.clear_selected_lot()
            Live.warehouse_serials[idx] = answer.read_s16()
        self.save_and_sync(0)
        GameCanvas.popups.show(40)

    def _on_exp_fame(self, answer, op):  # answer 259
        hero = GameCanvas.hero
        Live.values[15] = answer.read_s32()
        Live.values[14] = answer.read_s32()
        Live.values[13] = GameCanvas.add_exp(Live.values[14])
        hero.fame += Live.values[15]
        GameCanvas.live_gifts = 1
        self.save_game()
        self.sync_exp_fame()

    _ANSWER_BY_OPCODE = {  # answer -> handler, the branches of on_answer
        531: _on_login,
        513: _on_status,
        517: _on_notices,
        519: _on_sale_list,
        261: _on_exp_fame_saved,
        263: _on_user_data_loaded,
        257: _on_user_data_saved,
        769: _on_sync,
        833: _on_safe,
        817: _on_warehouse,
        785: _on_lot_counts,
        521: _on_gift_list,
        787: _on_lots_page,
        789: _on_bought,
        801: _on_put_on_sale,
        803: _on_price_info,
        865: _on_price_info,
        867: _on_lot_cancelled,
        259: _on_exp_fame,
    }

    def on_error_answer(self, opcode, code, answer):  # as.java:992-1056  (error answers)
        if Online.background:                # PORT-EXTRA: the background login fails silently
            return
        if opcode == 531:
            if answer is None:
                Live.show_error(code)
                Live.close_target = 3
                return
            answer.read_s8()
            answer.read_s8()
            b = answer.read_s8()
            if b == 1:
                GameCanvas.popups.show(43)
                return
            if b == 3 and code != -49:
                GameCanvas.popups.show(47)
                return
            Live.show_error(code)
            Live.close_target = 3
            return
        if opcode == 513:
            Live.show_error(code)
            Live.close_target = 3
            return
        if opcode == 517:
            self.sync_sale_list()
            return
        if opcode == 519:
            self.sync_gift_list()
            return
        if opcode == 521:
            self.sync_gifts()
            return
        if opcode in (259, 261):
            self.sync_done()
            return
        if opcode == 769:
            Live.show_error(code)
            Live.close_target = 3
            return
        if opcode == 789:
            Live.show_error(code)
            return
        if opcode == 867 and code == -12:
            Live.clear_selected_lot()
        if opcode in (867, 801, 817, 833, 849):
            self.save_and_sync(0)
        Live.show_error(code)

    @staticmethod
    def clear_selected_lot():  # as.java:1058-1062
        Item.clear(Live.lots[Live.selected_slot])
        Live.prices[Live.selected_slot] = 0
        Live.lot_ids[Live.selected_slot] = 0

    def save_and_sync(self, saved):  # as.java:1064-1067  (save the game)
        GameCanvas.live_saved = i16(saved)
        self.save_game()

    @staticmethod
    def list_height():  # as.java:1069-1071
        return 32 * Live.list_rows - 12

    @staticmethod
    def set_list_items(items, y, h):  # as.java:1073-1092  ("a|b|c|" -> list menu)
        i = 0
        j = 0
        for b in range(len(items)):
            if items[b] == "|":
                Live.list_items[i] = items[j:b]
                j = b + 1
                i += 1
        if i == 0:
            return
        Live.list_count = i16(i)
        i = idiv(h + 12, 32)
        Live.list_rows = i16(i)
        Live.list_rows = min(Live.list_rows, Live.list_count)
        Live.list_y = i16(y + (h - 32 * Live.list_rows - 12 >> 1))
        Live.list_top = Live.list_cursor = 0

    def list_keys(self, key):  # as.java:1094-1109  (list keys: -2 moved, index chosen, -1)
        i = -1
        if key in (-1, -2, 50, 56):
            if key in (-1, 50):
                Live.list_cursor -= 1
                if Live.list_cursor < 0:
                    Live.list_cursor = i16(Live.list_count - 1)
            else:
                Live.list_cursor += 1
                if Live.list_cursor >= Live.list_count:
                    Live.list_cursor = 0
            Live.clamp_list_scroll()
            i = -2
        elif key in (-5, 53):
            i = Live.list_cursor
        return i

    @staticmethod
    def clamp_list_scroll():  # as.java:1111-1118
        if Live.list_top > Live.list_cursor:
            Live.list_top = Live.list_cursor
            return
        if Live.list_cursor - Live.list_top >= Live.list_rows:
            Live.list_top = Live.list_cursor - Live.list_rows + 1

    def draw_list(self):  # as.java:1120-1135  (draw the list menu)
        i = Live.list_y
        b = 0
        j = Live.list_top
        while b < Live.list_rows:
            if j == Live.list_cursor:
                GameCanvas.draw_frame_box(45, i, 150, 20, GameCanvas.rgb(0, 0, 0), GameCanvas.rgb(255, 255, 255), GameCanvas.rgb(0, 0, 0), True)
                Gfx.set_font(GameCanvas.font_orange)
            else:
                GameCanvas.draw_frame_box(46, i + 1, 148, 18, GameCanvas.rgb(0, 0, 0), GameCanvas.rgb(80, 80, 80), GameCanvas.rgb(0, 0, 0), True)
                Gfx.set_font(GameCanvas.font_white)
            GameCanvas.draw_text_centred(120, i + 1, Live.list_items[j])
            i += 32
            b += 1
            j += 1

    def enter_live(self):  # as.java:1137-1143
        self.load_titles()
        self.load_live_strings()
        GameCanvas.load_item_tables()
        GameCanvas.state = 11
        Live.list_w = GameCanvas.view_size.x

    def load_titles(self):  # as.java:1145-1149
        for b in range(12):
            Live.titles[b] = GameCanvas.gamestr(2 + b)
        return True

    def load_live_strings(self):  # as.java:1151-1155
        for b in range(50):
            Live.live_strings[b] = GameCanvas.gamestr(15 + b)
        return True

    def open_live_menu(self):  # as.java:1157-1176  (GAMEVIL LIVE menu)
        # PORT-EXTRA: one hero kept on the server, so no Management (Save / Load User Data)
        # PORT-EXTRA: online, the Multiplayer screens are a part of this game (main.py)
        Live.set_list_items("Trade|Warehouse|Safe|Multiplayer|" if Online.enabled() else "Trade|Warehouse|Safe|Management|", 20, 255)
        Live.list_cursor = Live.saved_0
        Live.list_top = Live.saved_1
        Live.clamp_list_scroll()
        Live.input_handler = 2
        Live.live_screen = 1
        Live.title = Live.titles[2]
        Live.scroll = 0
        Live.scroll_step = 10
        if Live.inited and Live.first_login:
            Live.inited = False
            GameCanvas.popups.arg1 = Live.password
            GameCanvas.popups.arg2 = Live.user_id
            GameCanvas.popups.show(49)
        Live.request_redraw()
        Live.first_login = False
        if Live.auto_mp:                     # PORT-EXTRA: Main Menu > Multiplayer > YES
            Live.auto_mp = False
            self.open_multiplayer()

    # --- PORT-EXTRA: the Multiplayer screens (pow_mp) as a part of this game ---------------
    def open_multiplayer(self):
        """Gamevil Live > Multiplayer: the single player waits in memory while main.py runs the
        Multiplayer screens in the same window; its Exit comes back here (after_multiplayer)."""
        self.save_game()                     # the Multiplayer login (262) reads the hero from the save
        self.suspend()

    def after_multiplayer(self, rewards):
        """Back in the Live menu: what the battles earned (1032: gold, fame, exp, loot) goes to
        the hero in memory, as the Exp / Fame of Gamevil Live did (259 -> ag.H, popup 41)."""
        hero = GameCanvas.hero
        gold = fame = exp = 0
        for r in rewards:
            gold += r.get("gold", 0)
            fame += r.get("fame", 0)
            exp += r.get("exp", 0)
            for item in r.get("loot", ()):
                self.give_loot(item)
        hero.gold = max(0, min(0x7FFFFFFF, hero.gold + gold))
        hero.fame = max(0, min(0x7FFFFFFF, hero.fame + fame))
        levels = GameCanvas.add_exp(exp) if exp > 0 else 0
        self.save_game()
        Live.request_redraw()
        if gold or fame or exp:
            GameCanvas.popups.arg1 = str(exp)
            GameCanvas.popups.arg2 = str(fame)
            GameCanvas.popups.arg3 = str(levels)
            GameCanvas.popups.show(41)
            Live.close_target = -1

    def give_loot(self, item):
        """One 1032 loot item (id, atk, def, hp, mp) into the hero: a consumable stacks on the
        belt (ag.k), the rest takes the first free backpack cell with the stats the server
        rolled. False when there is no room (the item is lost, as a drop on a full backpack)."""
        item_id, atk, def_, hp, mp = item
        if item_id < 100:
            return self.give_item(item_id, 1) != 0
        hero = GameCanvas.hero
        for cell in hero.backpack:
            if cell.id == 0:
                cell.id, cell.attack, cell.defense, cell.hp, cell.mp, cell.enchant = item_id, atk, def_, hp, mp, 0
                return True
        return False

    def open_waiting(self):  # as.java:1178-1184  (waiting screen)
        Live.input_handler = 17
        Live.live_screen = 12
        Live.title = Live.titles[2]
        Live.anim_ticks = 0
        Live.request_redraw()

    @staticmethod
    def request_redraw():  # as.java:1186-1188
        Live.screen_redraw = True

    @staticmethod
    def draw_item_cell(item_id, x, y, selected):  # as.java:1190-1194  (item cell)
        GameCanvas.menus.draw_grid_cell(x, y, selected)
        if item_id > 0:
            GameCanvas.menus.draw_item_count_icon(item_id, x, y, 0)

    @staticmethod
    def draw_text_centred_in(text, x, y, w):  # as.java:1196-1198
        Gfx.draw_string(text, x + idiv(w, 2), y, 1)

    @staticmethod
    def draw_screen():  # as.java:1200-1202
        Live.screen.draw_live_screen()

    def draw_caption_box(self, text, y):  # as.java:1204-1209  (caption box)
        Gfx.set_font(GameCanvas.font_white)
        self.draw_centred_box(y, 200, 22)
        if text != "":
            self.draw_text_at(text, y + 1 - GameCanvas.view_y, 0)

    def key_down(self, key):  # as.java:1211-1269  (keys)
        i = key
        if GameCanvas.popups.kind != 0:
            GameCanvas.popups.popup_keys()
            GameCanvas.key = -999
            Live.request_redraw()
            return
        GameCanvas.key = -999
        h = {1: self.sale_list_keys, 2: self.live_menu_keys, 3: self.trade_keys, 4: self.buy_category_keys, 5: self.buy_kind_keys, 6: self.buy_enchant_keys, 7: self.buy_lots_keys,
             8: self.sell_pick_keys, 9: self.sell_price_keys, 10: self.price_info_keys, 13: self.cancel_sell_keys, 14: self.warehouse_keys, 15: self.safe_keys,
             16: self.management_keys, 18: self.registration_keys}.get(Live.input_handler)
        if h is not None:
            h(i)

    def keyboard_key(self, key):
        """PORT-EXTRA (config.REG_KEYBOARD): the on-screen keyboards of key_grid.py in front of
        registration_keys: arrows move (on the UserID step the phone's 2 4 6 8 too, as ag.r does),
        OK types the cell; -> the key for the original handler, None when taken here."""
        if Live.reg_step == 0:                   # the password: the number keys stay digits
            grid = Live.pwd_grid
            if grid.move(key):
                Live.request_redraw()
                return None
            if key == -5:
                return -6 if grid.is_ok else ord(grid.label)   # CONFIRM / the digit's key
            return key
        grid = Live.id_grid
        if grid.move({50: -1, 56: -2, 52: -3, 54: -4}.get(key, key)):
            Live.request_redraw()
            return None
        if key in (-5, 53):
            if grid.is_ok:
                return -6
            GameCanvas.name_buf.handle_key(ord(grid.label))    # A..Z, 0..9
            Live.request_redraw()
            return None
        return key

    def registration_keys(self, key):  # as.java:1271-1328  (registration: UserID, then password)
        if config.REG_KEYBOARD:
            key = self.keyboard_key(key)         # PORT-EXTRA
            if key is None:
                return
        if Live.reg_step == 0:
            i = len(Live.password)
            if key == -7:
                if i > 0:
                    Live.password = Live.password[:i - 1]
                else:
                    Live.reg_step = 1
                    Live.request_redraw()
                if i == 10:
                    Live.request_redraw()
                    return
            elif key == -6:
                if i >= 4:
                    Live.blink = True
                    Live.reg_from_popup = True
                    self.ask_request(530)
                    return
            else:
                j = GameCanvas.key_digit(key)
                if j != -1 and i < 12:
                    Live.password += str(j)
                return
        elif Live.reg_step == 1:
            if len(GameCanvas.name_buf.get_text()) == 0 and key == -7:
                self.leave_live()
                return
            i = GameCanvas.move_letter_cursor(key)
            if i == -7:
                GameCanvas.name_buf.handle_key(-8)
                return
            if i in (-5, 53):
                if GameCanvas.letter_cursor == 26 and len(GameCanvas.name_buf.get_text()) >= 4:
                    if len(GameCanvas.name_buf.get_text()) != 0:
                        Live.user_id = GameCanvas.name_buf.get_text()
                        GameCanvas.name_buf.set_text(Live.user_id)
                        Live.reg_step = 0
                        Live.request_redraw()
                        return
                else:
                    GameCanvas.name_buf.handle_key(65 + GameCanvas.letter_cursor)
                    return
            elif i == -6 and len(GameCanvas.name_buf.get_text()) >= 4 and len(GameCanvas.name_buf.get_text()) != 0:
                Live.user_id = GameCanvas.name_buf.get_text()
                GameCanvas.name_buf.set_text(Live.user_id)
                Live.reg_step = 0
                Live.request_redraw()

    def sale_list_keys(self, key):  # as.java:1330-1357  (Sale / Gift List)
        if key == -3:
            Live.selected_slot = Live.selected_slot - 1 if Live.selected_slot > 0 else 4
            Live.request_redraw()
        elif key == -4:
            Live.selected_slot = Live.selected_slot + 1 if Live.selected_slot < 4 else 0
            Live.request_redraw()
        elif key in (-8, -5):
            if Live.list_kind == 0:
                self.sync_gift_list()
            else:
                self.sync_gifts()

    def cancel_sell_keys(self, key):  # as.java:1359-1394  (Cancel Sell: my 5 lots)
        from pow.game.menus import Menus
        if key == -7:
            self.open_trade()
        elif key in (-5, 53):
            if Live.lots[Live.selected_slot].id > 0:
                Live.shown_item = Live.lots[Live.selected_slot].id
                Live.flags[7] = 0 if GameCanvas.cursor[16] < config.BACKPACK_SIZE else 1
                GameCanvas.popups.arg1 = Menus.item_name(Live.lots[Live.selected_slot].id)
                GameCanvas.popups.show(39)
                Live.close_target = 14
        elif key in (-3, 52):
            Live.selected_slot = Live.selected_slot - 1 if Live.selected_slot > 0 else 4
            Live.request_redraw()
        elif key in (-4, 54):
            Live.selected_slot = Live.selected_slot + 1 if Live.selected_slot < 4 else 0
            Live.request_redraw()

    def price_info_keys(self, key):  # as.java:1396-1403  (Price Info list)
        if key == -7:
            self.open_price_info()
            return
        self.draw_grid_cursor(key, False)

    def sell_pick_keys(self, key):  # as.java:1405-1440  (Sell: pick an item)
        if key == -7:
            self.open_trade()
            return
        if key in (-5, 53):
            item = Live.selected_grid_item()
            if item.id > 0:
                if 434 <= item.id <= 437:
                    GameCanvas.popups.show(13)
                    return
                Live.shown_item = item.id
                Live.enchant = i16(item.enchant)
                Live.selected_slot = GameCanvas.cursor[18]
                if item.id > 500:
                    Live.category = 2
                    Live.kind = i16(item.id - 501)
                elif item.id > 300:
                    Live.category = 1
                    Live.kind = i16(GameCanvas.item_tables[1].get_int(item.id - 301, 7))
                else:
                    Live.category = 0
                    Live.kind = i16(GameCanvas.item_tables[0].get_int(item.id - 101, 7))
                Live.values[13] = 0
                Live.values[14] = 0
                Live.save_grid_cursor(True)
                self.open_price_info()
            return
        self.grid_keys(key)

    def sell_price_keys(self, key):  # as.java:1442-1489  (Sell: the price)
        bool_ = True
        if 48 <= key <= 57:
            i = GameCanvas.key_digit(key)
            if 0 <= i <= 9 and Live.values[13] < 9:
                Live.values[14] = Live.values[14] * 10
                Live.values[14] = Live.values[14] + i
                if Live.values[14] > 0:
                    Live.values[13] = Live.values[13] + 1
        elif key == -7:
            if Live.values[13] > 0:
                Live.values[14] = idiv(Live.values[14], 10)
                Live.values[13] = Live.values[13] - 1
            else:
                self.open_sell_grid()
        elif key == -5:
            if Live.values[14] > 0:
                self.ask_request(800)
                Live.scroll = 0
            else:
                bool_ = False
        elif key == -6:
            self.ask_request(802)
            Live.scroll = 0
        else:
            bool_ = False
        if bool_:
            Live.request_redraw()

    def buy_kind_keys(self, key):  # as.java:1491-1518  (Buy: kind)
        if key == -7:
            self.open_buy_category()
            return
        if key in (-5, 53):
            if Live.kind_items[Live.category][GameCanvas.cursor[18]] != 0:
                Live.save_grid_cursor(False)
                Live.shown_item = Live.kind_items[Live.category][GameCanvas.cursor[18]]
                Live.kind = i16(GameCanvas.cursor[18])
                if Live.category == 2:
                    Live.enchant = 0
                    Live.page = 0
                    Live.page_step = 1
                    self.ask_request(786)
                else:
                    Live.enchant = 0
                    self.ask_request(784)
                Live.scroll = 0
                Live.request_redraw()
            return
        self.draw_grid_cursor(key, False)

    def buy_enchant_keys(self, key):  # as.java:1520-1556  (Buy: enchant level)
        bool_ = True
        if key == -7:
            self.open_sell_price()                      # falls through into case -3
            Live.enchant = i16(Live.enchant - 1 if Live.enchant > 0 else 9)
        elif key in (-3, 52):
            Live.enchant = i16(Live.enchant - 1 if Live.enchant > 0 else 9)
        elif key in (-4, 54):
            Live.enchant = i16(Live.enchant + 1 if Live.enchant < 9 else 0)
        elif key in (-2, -1, 50, 56):
            Live.enchant = i16(Live.enchant + (-5 if Live.enchant > 4 else 5))
        elif key in (-5, 53):
            if Live.counts[15 - Live.enchant] > 0:
                Live.page = 0
                Live.page_step = 1
                self.ask_request(786)
                Live.scroll = 0
            else:
                GameCanvas.popups.show(8)
        else:
            bool_ = False
        if bool_:
            Live.request_redraw()

    def buy_lots_keys(self, key):  # as.java:1558-1608  (Buy: the lots)
        if key == -7:
            if Live.category == 2:
                self.open_sell_price()
                return
            Live.scroll = 0
            self.ask_request(784)
        elif key in (-5, 53):
            GameCanvas.cursor[19] = Live.lots[GameCanvas.cursor[18]].id
            if Live.lots[GameCanvas.cursor[18]].id != 0:
                if Live.prices[GameCanvas.cursor[18]] > GameCanvas.hero.gold:
                    GameCanvas.popups.show(11)
                    return
                if GameCanvas.cursor[16] >= config.BACKPACK_SIZE:
                    GameCanvas.popups.show(12)
                    return
                Live.selected_slot = GameCanvas.cursor[18]
                GameCanvas.popups.arg1 = str(Live.prices[GameCanvas.cursor[18]])
                GameCanvas.popups.show(34)
                Live.close_target = 10
            return
        else:
            i = self.draw_grid_cursor(key, False)
            if i != 0:
                if i < 0:
                    if Live.page > 1:
                        Live.page_step = -1
                        Live.scroll = 0
                        self.ask_request(786)
                    else:
                        GameCanvas.popups.show(9)
                else:
                    Live.page_step = 1
                    Live.scroll = 0
                    self.ask_request(786)
            else:
                return
        Live.request_redraw()

    def buy_category_keys(self, key):  # as.java:1610-1626  (Buy: category)
        if key == -7:
            self.open_trade()
            return
        i = self.list_keys(key)
        if 0 <= i <= 2:
            Live.saved_2 = i16(Live.list_cursor)
            Live.saved_3 = i16(Live.list_top)
            Live.category = i16(i)
            Live.save_grid_cursor(True)
            self.open_sell_price()
            return
        if i == -2:
            Live.request_redraw()

    def open_sell_price(self):  # as.java:1628-1633
        self.restore_grid_cursor(False)
        Live.live_screen = 6
        Live.input_handler = 5
        Live.request_redraw()

    def open_cancel_sell(self):  # as.java:1635-1639
        Live.live_screen = 7
        Live.input_handler = 6
        Live.request_redraw()

    def open_sale_list(self):  # as.java:1641-1646
        self.set_cancel_sell_grid()
        Live.live_screen = 8
        Live.input_handler = 7
        Live.request_redraw()

    def set_cancel_sell_grid(self):  # as.java:1648-1650
        self.set_grid(4, 2, True)

    def restore_grid_cursor(self, items_grid):  # as.java:1652-1666  (restore the grid cursor)
        Live.flags[7] = Live.saved_11
        Live.category = Live.saved_6
        if items_grid:
            self.set_grid(config.BACKPACK_SIZE // 5 if Live.flags[7] == 0 else config.WAREHOUSE_SIZE // 5, 3, False)
        else:
            self.set_grid(4 if Live.category == 2 else 3, 3, False)
        GameCanvas.cursor[10] = Live.saved_7
        GameCanvas.cursor[9] = Live.saved_8
        GameCanvas.cursor[18] = Live.saved_9
        GameCanvas.cursor[8] = Live.saved_10
        Live.values[5] = Live.saved_12
        Live.values[6] = Live.saved_13

    def open_sell_grid(self):  # as.java:1668-1674  (Sell: Backpack / Warehouse grid)
        self.restore_grid_cursor(True)
        Live.input_handler = 8
        Live.live_screen = 4
        Live.title = Live.titles[5]
        Live.request_redraw()

    def open_price_info(self):  # as.java:1676-1681
        Live.live_screen = 9
        Live.input_handler = 9
        Live.title = Live.titles[5]
        Live.request_redraw()

    def open_buy_lots(self, request):  # as.java:1683-1695
        if request:
            Live.scroll = 0
            Live.page = 0
            self.ask_request(864)
        else:
            Live.selected_slot = 0
            Live.input_handler = 13
            Live.live_screen = 10
            Live.title = Live.titles[8]
        Live.request_redraw()

    def after_login(self):  # as.java:1697-1705  (after 513: notices, Sale List, Gift List, Exp/Fame, sync)
        Live.scroll = i16(Live.scroll + Live.scroll_step)
        if Live.flags[15] == 1 and Live.first_login:
            self.ask_request(516)
            Live.request_redraw()
            return
        self.sync_sale_list()

    def sync_sale_list(self):  # as.java:1707-1715
        Live.scroll = i16(Live.scroll + Live.scroll_step)
        if Live.flags[14] == 1:
            self.ask_request(518)
            Live.request_redraw()
            return
        self.sync_gift_list()

    def open_trade_list(self):  # as.java:1717-1723
        Live.selected_slot = 0
        Live.input_handler = 1
        Live.live_screen = 11
        Live.title = Live.titles[0] if Live.list_kind == 0 else Live.titles[1]
        Live.request_redraw()

    def sync_gift_list(self):  # as.java:1725-1733
        Live.scroll = i16(Live.scroll + Live.scroll_step)
        if Live.flags[13] == 1:
            self.ask_request(520)
            Live.request_redraw()
            return
        self.sync_gifts()

    def sync_gifts(self):  # as.java:1735-1744
        Live.scroll = i16(Live.scroll + Live.scroll_step)
        if GameCanvas.live_gifts == 0:
            self.ask_request(258)
            Live.request_redraw()
            return
        GameCanvas.live_gifts = 2
        self.sync_exp_fame()

    def sync_exp_fame(self):  # as.java:1746-1750
        Live.scroll = i16(Live.scroll + Live.scroll_step)
        self.ask_request(260)
        Live.request_redraw()

    def sync_done(self):  # as.java:1752-1756
        Live.scroll = i16(Live.scroll + Live.scroll_step)
        self.ask_request(768)
        Live.request_redraw()

    def trade_keys(self, key):  # as.java:1758-1785  (Trade: Buy / Sell / Cancel)
        if key == -7:
            self.open_live_menu()
            return
        i = self.list_keys(key)
        if i >= 0:
            Live.saved_2 = i16(Live.list_cursor)
            Live.saved_3 = i16(Live.list_top)
            if i == 0:
                Live.saved_4 = Live.saved_5 = 0
                self.open_buy_category()
            elif i == 1:
                Live.save_grid_cursor(True)
                self.open_sell_grid()
            elif i == 2:
                Live.save_grid_cursor(True)
                self.open_buy_lots(True)
            return
        if i == -2:
            Live.request_redraw()

    def warehouse_keys(self, key):  # as.java:1787-1804  (Warehouse grid: move an item)
        if key == -7:
            self.open_live_menu()
            return
        if key in (-5, 53):
            item = Live.selected_grid_item()
            if item.id > 0:
                self.ask_request(816)
                Live.scroll = 0
                Live.request_redraw()
            return
        self.grid_keys(key)

    def open_buy_category(self):  # as.java:1806-1812
        self.set_category_list()
        Live.input_handler = 4
        Live.live_screen = 5
        Live.title = Live.titles[4]
        Live.request_redraw()

    def set_category_list(self):  # as.java:1814-1824
        Live.set_list_items("Normal Items|Special Items|Rare Items|", 20, 255)
        Live.list_cursor = Live.saved_4
        Live.list_top = Live.saved_5
        Live.clamp_list_scroll()
        i = 32 + Live.list_height()
        i = 20 + (255 - i >> 1)
        Live.values[15] = i
        Live.list_y = i + 22 + 10

    def grid_keys(self, key):  # as.java:1826-1841  (grid keys, -6 switches Backpack / Warehouse)
        if key == -6:
            if Live.flags[7] == 1:
                self.set_backpack_grid()
                Live.request_redraw()
                return
            if Live.flags[7] == 0:
                self.set_warehouse_grid()
                Live.request_redraw()
                return
        else:
            self.draw_grid_cursor(key, True)

    def draw_grid_cursor(self, key, wrap):  # as.java:1843-1877  (grid cursor)
        cursor = GameCanvas.cursor
        i = 1
        if key in (-1, 50):
            cursor[10] = cursor[10] - 1
        elif key in (-2, 56):
            cursor[10] = cursor[10] + 1
        elif key in (-3, 52):
            cursor[9] = cursor[9] - 1
            if (cursor[9] < 0) if F6 else (cursor[9] - 1 < 0):     # DECOMP-FIX F6
                cursor[9] = 4
                cursor[10] = cursor[10] - 1
        elif key in (-4, 54):
            cursor[9] = cursor[9] + 1
            if (cursor[9] >= 5) if F6 else (cursor[9] + 1 >= 5):   # DECOMP-FIX F6
                cursor[9] = 0
                cursor[10] = cursor[10] + 1
        else:
            i = 0
        if i:
            i = Live.clamp_grid_cursor(wrap)
            if i == 0:
                Live.request_redraw()
        return i

    def safe_keys(self, key):  # as.java:1879-1968  (Safe)
        bool_ = True
        if Live.flags[14] == 0:
            if key in (-4, -3):
                Live.flags[15] = i16(Live.flags[15] ^ 0x1)
            elif key in (-1, 50):
                Live.flags[15] = 0
            elif key in (-2, 56):
                Live.flags[15] = 1
            elif key == -7:
                self.open_live_menu()
                GameCanvas.images[22] = None
                GameCanvas.images[24] = None
            elif key in (-5, 53):
                if Live.flags[15] == 0:
                    Live.values[15] = Live.safe_gold
                    if Live.safe_gold == 0:
                        GameCanvas.popups.show(14)
                else:
                    Live.values[15] = GameCanvas.hero.gold
                    if GameCanvas.hero.gold == 0:
                        GameCanvas.popups.show(15)
                if Live.values[15] > 0:
                    Live.flags[14] = 1
                    Live.values[14] = 0
                    Live.live_screen = 3
                    Live.request_redraw()
            else:
                bool_ = False
        elif 48 <= key <= 57:
            i = GameCanvas.key_digit(key)
            if i != -1:
                Live.values[14] = Live.values[14] * 10
                Live.values[14] = Live.values[14] + i
                Live.values[14] = min(Live.values[14], Live.values[15])
        elif key == -7:
            if Live.values[14] > 0:
                Live.values[14] = idiv(Live.values[14], 10)
            else:
                Live.flags[14] = 0
                Live.live_screen = 2
                Live.request_redraw()
        elif key == -5:
            if Live.values[14] > 0:
                self.ask_request(832)
                Live.flags[14] = 0
                Live.live_screen = 2
                Live.request_redraw()
            else:
                bool_ = False
        else:
            bool_ = False
        if bool_:
            Live.request_redraw()

    def leave_live(self):  # as.java:1970-1978  (leave Gamevil Live -> Game Menu)
        if Online.offer_open:                # PORT-EXTRA: BACK on the offered registration = skip
            Online.on_registration_closed(False)
        GameCanvas.state = 2
        self.disconnect()
        GameCanvas.redraw = 1
        GameCanvas.menu[0] = 0
        GameCanvas.menu[1] = 2
        GameCanvas.popups.from_gamestr = 0
        GameCanvas.in_live = False

    @staticmethod
    def save_grid_cursor(reset):  # as.java:1980-1999  (remember / reset the grid cursor)
        Live.saved_6 = Live.category
        if reset:
            Live.saved_7 = Live.saved_8 = Live.saved_9 = Live.saved_10 = Live.saved_11 = Live.saved_12 = Live.saved_13 = 0
            return
        Live.saved_11 = Live.flags[7]
        Live.saved_7 = i16(GameCanvas.cursor[10])
        Live.saved_8 = i16(GameCanvas.cursor[9])
        Live.saved_9 = i16(GameCanvas.cursor[18])
        Live.saved_10 = i16(GameCanvas.cursor[8])
        Live.saved_12 = i16(Live.values[5])
        Live.saved_13 = i16(Live.values[6])

    def open_warehouse(self):  # as.java:2001-2007  (Warehouse screen)
        self.set_backpack_grid()
        Live.input_handler = 14
        Live.live_screen = 4
        Live.title = Live.titles[9]
        Live.request_redraw()

    def set_backpack_grid(self):  # as.java:2009-2012
        Live.flags[7] = 0
        self.set_grid(config.BACKPACK_SIZE // 5, 3, True)

    def set_warehouse_grid(self):  # as.java:2014-2017
        Live.flags[7] = 1
        self.set_grid(config.WAREHOUSE_SIZE // 5, 3, True)

    def set_grid(self, rows, visible_rows, reset):  # as.java:2019-2043  (grid geometry)
        cursor = GameCanvas.cursor
        cursor[3] = visible_rows
        cursor[6] = 32 * visible_rows - 4 + 2
        cursor[4] = rows
        cursor[7] = 32 * rows - 4 + 2
        grid_w = 156                              # char c = '\u009c'
        if visible_rows < rows:
            grid_w += 8
            cursor[11] = 1
            cursor[13] = cursor[6] * (cursor[6] - 2) * 10
            cursor[13] = idiv(idiv(cursor[13], cursor[7]) + 9, 10)
        else:
            cursor[11] = 0
        cursor[5] = 240 - grid_w >> 1
        cursor[12] = cursor[5] + 156 + 4
        cursor[26] = -1
        cursor[27] = 0
        if reset:
            cursor[8] = 0
            cursor[10] = 0
            cursor[9] = 0
            Live.clamp_grid_cursor(True)

    @staticmethod
    def clamp_grid_cursor(wrap):  # as.java:2045-2072  (clamp the grid cursor; -1 / 1 = left the grid)
        cursor = GameCanvas.cursor
        if cursor[10] < 0:
            if wrap:
                cursor[10] = cursor[4] - 1
            else:
                cursor[10] = Live.values[5]
                cursor[9] = Live.values[6]
                return -1
        elif cursor[10] >= cursor[4]:
            if wrap:
                cursor[10] = 0
            else:
                cursor[10] = Live.values[5]
                cursor[9] = Live.values[6]
                return 1
        Live.values[5] = cursor[10]
        Live.values[6] = cursor[9]
        if cursor[10] < cursor[8]:
            cursor[8] = cursor[10]
        elif cursor[10] >= cursor[8] + cursor[3]:
            cursor[8] = cursor[10] - cursor[3] + 1
        cursor[18] = cursor[10] * 5 + cursor[9]
        return 0

    @staticmethod
    def selected_grid_item():  # as.java:2074-2081  (the selected item of the Backpack / Warehouse grid)
        if Live.flags[7] == 0:
            Live.selected_serial = Live.backpack_serials[GameCanvas.cursor[18]]
            return GameCanvas.hero.backpack[GameCanvas.cursor[18]]
        Live.selected_serial = Live.warehouse_serials[GameCanvas.cursor[18]]
        return Live.warehouse[GameCanvas.cursor[18]]

    def open_trade(self):  # as.java:2083-2093  (Trade menu)
        Live.set_list_items("Buy Item|Sell Item|Cancel Sell|", 26, 243)
        Live.list_cursor = Live.saved_2
        Live.list_top = Live.saved_3
        Live.clamp_list_scroll()
        Live.input_handler = 3
        Live.live_screen = 1
        Live.title = Live.titles[3]
        Live.request_redraw()

    def live_menu_keys(self, key):  # as.java:2095-2126  (GAMEVIL LIVE menu)
        if key == -7:
            self.leave_live()
            if GameCanvas.live_saved == 0:
                return
        else:
            i = self.list_keys(key)
            if i >= 0:
                Live.saved_0 = i16(Live.list_cursor)
                Live.saved_1 = i16(Live.list_top)
                if i == 0:
                    Live.saved_2 = Live.saved_3 = 0
                    self.open_trade()
                elif i == 1:
                    Live.save_grid_cursor(True)
                    self.open_warehouse()
                elif i == 2:
                    self.open_safe()
                elif i == 3:
                    if Online.enabled():         # PORT-EXTRA: Multiplayer instead of Management
                        self.open_multiplayer()
                    else:
                        self.open_management()
                return
            if i == -2:
                Live.request_redraw()

    def open_safe(self):  # as.java:2128-2135  (Safe)
        Live.flags[15] = 0
        Live.flags[14] = 0
        Live.input_handler = 15
        Live.live_screen = 2
        Live.title = Live.titles[10]
        Live.request_redraw()

    def open_management(self):  # as.java:2137-2143  (Management)
        Live.set_list_items("Save User Data|Load User Data|", 26, 243)
        Live.input_handler = 16
        Live.title = Live.titles[11]
        Live.request_redraw()

    def management_keys(self, key):  # as.java:2145-2159  (Management keys)
        if key == -7:
            self.open_live_menu()
            return
        i = self.list_keys(key)
        if 0 <= i <= 1:
            Live.flags[14] = i16(i)
            GameCanvas.popups.show(16 if i == 0 else 17)
            Live.close_target = 9
            return
        if i == -2:
            Live.request_redraw()

    @staticmethod
    def drop_net():  # as.java:2161-2164
        LiveNet.running = False
        Live.net = None
