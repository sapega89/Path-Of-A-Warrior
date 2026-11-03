"""l.java - popups (cS). Literal port, Phase 0 subset.

Ported: drawing (c, b(int), a(4 ints), O, c(int)), text popups a(String) and e(int) with all
plain-text messages, and the key/timer logic b() for the branches the menus reach.
Branches that need map/combat/campaign code raise NotPorted.
"""
import config
from pow.game import consts
from pow.game.game_canvas import GameCanvas
from pow.game.gfx import Gfx
from pow.midp.jint import i16


class Popups(GameCanvas):
    image = None  # public static Image r = null;  l.java:38  (ui_popup)

    def __init__(self):  # l.java:42-44
        super().__init__(GameCanvas.midlet)
        self.from_gamestr = 0       # 1 = popup from d() (gamestr), 0 = from e()
        self.kind = 0       # popup kind: 0 none, 1 text, 2 yes/no, 3 4-choice, 4 result, 10 ok
        self.popup_id = 0      # popup id
        self.timer = 0       # timer (200 = wait for key)
        self.extra = 0
        self.extra_w = 0
        self.extra_h = 0
        self.height = 0       # height
        self.line_count = 0       # number of lines
        self.popup_redraw = 0       # redraw flag
        self.button = 0       # selected button
        self.lines = [None] * 10
        self.arg1 = None
        self.arg2 = None
        self.arg3 = None
        self.arg4 = None
        self.answered = False
        self.drawn = False

    def reset(self):  # l.java:46-60
        self.kind = 0
        self.popup_id = 0
        self.timer = 0
        self.extra = 0
        self.extra_w = 0
        self.extra_h = 0
        self.height = 0
        self.line_count = 0
        self.popup_redraw = 0
        self.button = 0
        self.answered = False
        for b in range(len(self.lines)):
            self.lines[b] = ""

    def popup_keys(self):  # l.java:62-324  (keys + timer; returns the chosen button or -1)
        if GameCanvas.key != 0:
            self.popup_redraw = 1
            if self.extra != 0:
                if (GameCanvas.key == -5 or GameCanvas.key == 53) and self.extra_w > 2:
                    self.extra_w = 2
            else:
                if self.kind == 1:
                    if GameCanvas.key == -5 or GameCanvas.key == 53:
                        if self.from_gamestr == 1:
                            if self.timer > 2 and self.popup_id != 20:
                                self.timer = 2
                            return -1
                        if GameCanvas.state != 1:
                            if self.timer > 2 and self.popup_id != 20:
                                self.timer = 2
                        elif self.popup_id == 37:
                            self.start_exit()
                elif self.kind == 2:
                    ch = GameCanvas.key
                    if ch in (-4, -3, 52, 54):
                        self.button = i16(self.button + 1 & 0x1)
                    elif ch in (-5, 53):
                        self.timer = 1
                        if self.button == 0:
                            if self.from_gamestr == 1:
                                self.kind = 0
                                self.answered = True
                                return -1
                            if self.popup_id == 28:
                                self.start_exit()
                                return -1
                            if GameCanvas.state == 2:
                                c0 = GameCanvas.menu[0]
                                if c0 == 3:
                                    GameCanvas.menu[0] = 4
                                    GameCanvas.talk_kind = 0
                                    GameCanvas.talk_count = i16(GameCanvas.talk_count + 1)
                                    self.start_dialogue()
                                elif c0 == 5:
                                    if self.popup_id == 28:
                                        self.start_exit()
                                        return -1
                                    if self.popup_id == 41 or self.popup_id == 42:
                                        # platformRequest(ag.bm / ag.bn): the browser is not opened in the port
                                        if self.popup_id == 41:
                                            print("platformRequest:", GameCanvas.more_games_url)
                                        else:
                                            # PORT-EXTRA: the Multiplayer jar is part of the port, so
                                            # main.py starts it after the game exits (no download)
                                            GameCanvas.midlet.to_multiplayer = True
                                        GameCanvas.midlet.destroyApp(True)
                                        GameCanvas.midlet.notifyDestroyed()
                                        return -1
                                    if GameCanvas.menu[1] == 1:
                                        self.start_new_game()
                                elif c0 == 8:
                                    GameCanvas.reset_quick_items()
                                    self.fill_shop()
                                    GameCanvas.live_time = GameCanvas.now()
                                    if GameCanvas.live is not None:
                                        type(GameCanvas.live).first_login = True     # as.d = true (static)
                                    if self.save_game() != 0:
                                        GameCanvas.menus.enter_submenu()
                                        GameCanvas.menu_items = GameCanvas.game_menu_items
                                        GameCanvas.menu[0] = 0
                                        GameCanvas.menu_count = consts.v[GameCanvas.menu[0]]
                                        GameCanvas.menu[2] = 0
                                        GameCanvas.menu[1] = 0
                                        self.load_hero_images()
                                        self.start_story(100, 0)
                                    else:
                                        GameCanvas.reset_base_stats()
                                        self.setup_popup(1)
                                elif c0 == 10:
                                    GameCanvas.free_hero_images()
                                    GameCanvas.menu[0] = 5
                                    GameCanvas.menu_count = 10
                                    GameCanvas.menu[2] = 0
                                    GameCanvas.menu[1] = 0
                                elif c0 == 29:
                                    GameCanvas.menus.enter_submenu()
                                    GameCanvas.menu[0] = 6
                                # break -> leaves both switches, continues with the timer below
                            elif GameCanvas.map_mode.mode == 1:  # l.java:172-182  (pause menu: Exit -> Game Menu)
                                if GameCanvas.menu[1] == 5:
                                    self.free_map_images()
                                    self.open_menu(2)
                                    GameCanvas.menu[0] = 5
                                    GameCanvas.menu_count = 10
                                    GameCanvas.state = 2
                                    GameCanvas.menu_scroll = 0
                                    GameCanvas.menu_anim = 0
                            elif GameCanvas.state == 0:
                                return 0
                        else:
                            if self.from_gamestr == 1:
                                self.kind = 0
                                return -1
                            if GameCanvas.menu[0] == 8:
                                GameCanvas.reset_base_stats()
                            return 1
                    elif ch == -7:
                        if GameCanvas.menu[0] == 8:
                            self.timer = 1
                            GameCanvas.reset_base_stats()
                            return 1
                elif self.kind == 3:
                    if self.timer > 5:
                        ch = GameCanvas.key
                        if ch in (-1, 50):
                            self.button = i16(self.button - 1)
                            self.button = i16(self.button & 0x3)
                        elif ch in (-2, 56):
                            self.button = i16(self.button + 1)
                            self.button = i16(self.button & 0x3)
                        elif ch in (-5, 53):
                            self.timer = 4
                elif self.kind == 10:
                    if GameCanvas.key == -5 or GameCanvas.key == 53:
                        self.timer = 2
                        GameCanvas.popups.kind = 0
                        self.answered = True
                        GameCanvas.redraw = 1
        return self._tick_timer()

    def _tick_timer(self):  # l.java:229-323  (the part of b() after the key switch)
        if self.extra != 0:
            self.extra_w = i16(self.extra_w - 1)
            if self.extra_w < 1:
                self.extra = 0
                GameCanvas.redraw = 1
        else:
            if self.timer < 200:
                self.timer = i16(self.timer - 1)
            if self.timer == 0:
                self.kind = 0
                GameCanvas.redraw = 1
                v = self.popup_id
                if v in (1, 18):
                    self.start_exit()
                elif v == 15:
                    GameCanvas.menu[0] = 0
                    for b in range(5):
                        GameCanvas.talk_lines[b] = ""
                    GameCanvas.restore_menu_cursor()
                    GameCanvas.menu_items = GameCanvas.game_menu_items
                elif v == 39:
                    GameCanvas.menu[0] = 12
                    GameCanvas.menu_count = consts.v[GameCanvas.menu[0]]
                    GameCanvas.menu[1] = 3
                elif v == 14:
                    from pow.game.menus import Menus
                    GameCanvas.story_page += 1
                    GameCanvas.gift_kind = self.button
                    Menus.load_greeting(0, (GameCanvas.visit_topic << 2) + 2 + self.button)
                    GameCanvas.speech[GameCanvas.story_page & 0x1] = GameCanvas.talk_lines[3]
                elif v == 16:
                    from pow.game.menus import Menus
                    GameCanvas.hero.live_registered = 0
                    GameCanvas.menus.general_gift()
                    if GameCanvas.seal != 0:
                        GameCanvas.seal = i16(Menus.add_friendship(GameCanvas.generals[2][GameCanvas.visit_row], 5))
                    else:
                        GameCanvas.seal = i16(Menus.add_friendship(GameCanvas.generals[0][GameCanvas.visit_general], 5))
                    self.save_game()
                    self.setup_popup(15)
                elif v == 9:  # room cleared: the exits open, or the mission's general talks
                    if GameCanvas.cells[GameCanvas.cell].general != 0:
                        GameCanvas.scene.start_victory_talk()
                    else:
                        GameCanvas.room_phase = 1
                        GameCanvas.room_phase_timer = 5
                elif v == 10:  # l.java:257-260  (Mission Success -> Total Exp)
                    from pow.game.map_scene import MapScene
                    self.setup_popup(11)
                    MapScene.make_exp_bars()
                elif v == 11:  # l.java:261-268  (Total Exp -> Time Exp, if in time)
                    if GameCanvas.mission_seconds < GameCanvas.lords[GameCanvas.mission].time_limit:
                        self.setup_popup(12)
                        GameCanvas.exp_bar_step = 0
                    else:
                        GameCanvas.scene.finish_mission(1)
                elif v == 12:  # l.java:269-271
                    GameCanvas.scene.finish_mission(1)
                elif v == 22:  # l.java:300-315  (Mission fail -> Game Menu)
                    if GameCanvas.lords[GameCanvas.mission].reward > 200:
                        GameCanvas.scene.finish_mission(0)
                    else:
                        self.open_menu(2)
                        self.load_menu_frames()
                        GameCanvas.menu[0] = 0
                        GameCanvas.menu_count = consts.v[GameCanvas.menu[0]]
                        GameCanvas.menu_items = GameCanvas.game_menu_items
                        GameCanvas.state = 2
                        GameCanvas.redraw = 1
                        GameCanvas.menu_scroll = 0
                        GameCanvas.menu_anim = 0
        return -1

    def draw_popup(self):  # l.java:326-397  (draw)
        i = -(self.height >> 1)
        if self.kind == 4:
            i += 20
        if GameCanvas.state == 3 or GameCanvas.prev_state == 3:
            i -= 30
        self.draw_popup_frame(self.height)
        Gfx.set_font(GameCanvas.font_white)
        for b in range(self.line_count):
            self.draw_text_at(self.lines[b], GameCanvas.view_cy + i, 0)
            i += 20
        if self.kind == 10:
            self.draw_ok(GameCanvas.view_cy + self.height // 2 - 18)
        elif self.kind == 2:
            self.draw_yes_no(GameCanvas.view_cy + i + 5)
        elif self.kind == 3:
            i += 5
            for b in range(4):
                if self.button == b:
                    Gfx.set_font(GameCanvas.font_orange)
                else:
                    Gfx.set_font(GameCanvas.font_white)
                self.draw_text_at(self.lines[b + 2], GameCanvas.view_cy + i, 0)
                i += 16
        elif self.kind == 4:  # l.java:357-381  (mission result: gold / total exp / time exp)
            if GameCanvas.state == 3:
                GameCanvas.view_cy -= 30
            self.draw_text_at(GameCanvas.lord_name, GameCanvas.view_cy - 75, len(GameCanvas.lord_name) + 1)
            if self.popup_id == 10:
                j_ = GameCanvas.lords[GameCanvas.mission].gold * 150 * (1 + (GameCanvas.difficulty ^ 0x1))
                self.draw_text_at("Gold Acquired!", GameCanvas.view_cy + 10, len("Gold Acquired!") + 1)
                self.draw_big_number(j_, GameCanvas.view_cx + (GameCanvas.decimal_digits(j_) * 9 >> 1) - GameCanvas.view_x, GameCanvas.view_cy + 30, 0)
            elif self.popup_id == 11:
                self.draw_text_at("Total Exp", GameCanvas.view_cy, len("Total Exp") + 1)
            elif self.popup_id == 12:
                self.draw_text_at("Time Exp", GameCanvas.view_cy - 7, len("Time Exp") + 1)
                GameCanvas.draw_view_text("Time Limit:", GameCanvas.view_cx - 78 - GameCanvas.view_x, GameCanvas.view_cy - 7 + 20)
                self.draw_clock(GameCanvas.view_cx + 34 - GameCanvas.view_x, GameCanvas.view_cy - 7 + 21, GameCanvas.lords[GameCanvas.mission].time_limit)
                GameCanvas.draw_view_text("Ested Time:", GameCanvas.view_cx - 78 - GameCanvas.view_x, GameCanvas.view_cy - 7 + 40)
                self.draw_clock(GameCanvas.view_cx + 34 - GameCanvas.view_x, GameCanvas.view_cy - 7 + 41, GameCanvas.mission_seconds)
            if GameCanvas.state == 3:
                GameCanvas.view_cy += 30
        if self.extra != 0:
            self.draw_popup_frame(self.extra_h)
            if GameCanvas.state == 3:
                GameCanvas.view_cy -= 30
            self.draw_text_at(self.lines[5], GameCanvas.view_cy - (self.extra_h >> 1) - 3, 0)
            if GameCanvas.state == 3:
                GameCanvas.view_cy += 30
        if self.drawn:
            self.draw_ok(GameCanvas.view_cy + i - 10)
        self.popup_redraw = 0

    def draw_popup_frame(self, paramInt):  # l.java:399-423  (popup frame)
        i = GameCanvas.view_cy - (paramInt >> 1) - 10
        if Popups.image is None:
            Popups.image = self.load_image(GameCanvas.scr_ui.get(33))
        r = Popups.image
        if (GameCanvas.state == 3 or GameCanvas.prev_state == 3) and not GameCanvas.paused:
            i -= 30
        for b in range(26):
            self.draw_map_region(r, GameCanvas.view_cx - 103 + b * 8 - GameCanvas.view_x, i, 8, 3, 10, 0)
        self.draw_tiled_back(GameCanvas.view_cx - 102 - GameCanvas.view_x, i + 3, 210, paramInt + 14)
        self.draw_map_region(r, GameCanvas.view_cx - 105 - GameCanvas.view_x, i, 3, 10, 0, 0)
        self.draw_map_region(r, GameCanvas.view_cx + 104 - GameCanvas.view_x, i, 3, 10, 2, 0)
        i += 10
        arrayOfInt = [[GameCanvas.view_cx - 105 - GameCanvas.view_x, 162, 162, 162, GameCanvas.view_cx + 106 - GameCanvas.view_x],
                      [GameCanvas.view_cx - 104 - GameCanvas.view_x, 67, 67, 67, GameCanvas.view_cx + 105 - GameCanvas.view_x],
                      [GameCanvas.view_cx - 103 - GameCanvas.view_x, 33, 33, 33, GameCanvas.view_cx + 104 - GameCanvas.view_x]]
        for b in range(3):
            col = GameCanvas.rgb(arrayOfInt[b][1], arrayOfInt[b][2], arrayOfInt[b][3])
            Gfx.draw_line(arrayOfInt[b][0] + GameCanvas.view_x, i + GameCanvas.view_y, arrayOfInt[b][0] + GameCanvas.view_x, i + paramInt - 1 + GameCanvas.view_y, col)
            Gfx.draw_line(arrayOfInt[b][4] + GameCanvas.view_x, i + GameCanvas.view_y, arrayOfInt[b][4] + GameCanvas.view_x, i + paramInt - 1 + GameCanvas.view_y, col)
        i += paramInt
        self.draw_map_region(r, GameCanvas.view_cx - 105 - GameCanvas.view_x, i, 3, 10, 5, 0)
        self.draw_map_region(r, GameCanvas.view_cx + 104 - GameCanvas.view_x, i, 3, 10, 7, 0)
        i += 7
        for b in range(26):
            self.draw_map_region(r, GameCanvas.view_cx - 103 + b * 8 - GameCanvas.view_x, i, 8, 3, 10, 3)

    def draw_tiled_back(self, paramInt1, paramInt2, paramInt3, paramInt4):  # l.java:425-446  (tiled ui_back)
        if GameCanvas.images[10] is None:
            GameCanvas.images[10] = self.load_image(GameCanvas.scr_ui.get(59))
        b = 0
        while b * 24 < paramInt4:
            if paramInt4 >= (b + 1) * 24:
                i = 24
            else:
                i = paramInt4 - b * 24
            b1 = 0
            while b1 * 52 < paramInt3:
                if paramInt3 >= (b1 + 1) * 52:
                    j_ = 52
                else:
                    j_ = paramInt3 - b1 * 52
                if GameCanvas.images[10] is not None:
                    self.draw_map_region(GameCanvas.images[10], paramInt1 + b1 * 52, paramInt2 + b * 24, j_, i, 0, 0)
                b1 += 1
            b += 1

    def draw_yes_no(self, paramInt):  # l.java:448-461  (Yes / No buttons)
        for b in range(2):
            if self.button == b:
                Gfx.set_font(GameCanvas.font_white)
                bool_ = True
            else:
                Gfx.set_font(GameCanvas.font_gray)
                bool_ = False
            self.draw_box(GameCanvas.view_cx - 60 + b * 80, paramInt + GameCanvas.view_y, 40, 17, bool_)
            GameCanvas.draw_view_text_centred(consts.aZ[b], GameCanvas.view_cx - 40 + b * 80, paramInt + 1)

    def draw_ok(self, paramInt):  # l.java:463-467  (Ok button)
        Gfx.set_font(GameCanvas.font_white)
        self.draw_box(GameCanvas.view_cx - 60 + 40 + GameCanvas.view_x, paramInt + GameCanvas.view_y, 40, 17, True)
        GameCanvas.draw_view_text_centred(consts.aZ[2], GameCanvas.view_cx, paramInt)

    def show_text(self, paramString):  # l.java:469-496  ("<kind>line|line|...")
        self.drawn = False
        i = 1
        if paramString != "":
            self.kind = i16(ord(paramString[0]) - 48)
            if self.kind == 3:
                self.kind = 10
                self.timer = 200
            s = 0
            for b in range(len(paramString)):
                if paramString[b] == '|':
                    # DECOMP-FIX F9 (proposed): decompiled `s = s + 1; l[s] = ...` is `l[s++] = ...`;
                    # literally, line 0 keeps stale text and the last line is never drawn.
                    if config.DECOMP_FIX["F9"]:
                        self.lines[s] = paramString[i:b]
                        s = i16(s + 1)
                    else:
                        s = i16(s + 1)
                        self.lines[s] = paramString[i:b]
                    i = b + 1
            if config.DECOMP_FIX["F9"]:
                self.lines[s] = paramString[i:]
                s = i16(s + 1)
            else:
                s = i16(s + 1)
                self.lines[s] = paramString[i:]
            self.line_count = s
            self.height = i16(20 * s + (s - 1) * 2)
            if self.kind == 2 or self.kind == 10:
                self.height = i16(self.height + 20)
            if self.timer == 0:
                self.timer = 10
            self.popup_redraw = 1

    def show(self, paramInt):  # l.java:506-598  (gamestr popup N: text gamestr[N+15], kind from its first digit)
        from pow.game.menus import Menus
        self.from_gamestr = 1
        self.drawn = False
        if GameCanvas.state == 3:
            GameCanvas.redraw = 1
        else:
            GameCanvas.popups.popup_redraw = 1
        self.button = 0
        self.popup_id = i16(paramInt)
        str1 = GameCanvas.gamestr(paramInt + 15)
        c = str1[0]
        if '0' <= c <= '9':
            self.kind = i16(ord(c) - 48)
            if self.kind != 2:
                self.kind = 10
            str2 = str1[1:]
        else:
            self.kind = 10
            str2 = str1
        self.timer = 200
        i = len(str2)
        b2 = 0
        j = 0
        for b1 in range(i + 1):
            if b1 == i or str2[b1] == '\\':
                if j == b1:
                    self.lines[b2] = " "
                else:
                    self.lines[b2] = str2[j:b1]
                b2 += 1
                j = b1 + 1
        self.line_count = i16(b2)
        if paramInt == 53:
            self.line_count = 4
            self.lines[0] = self.arg1
            self.lines[1] = self.arg2
            self.lines[2] = self.arg3
            self.lines[3] = self.arg4
        elif paramInt == 34:
            self.lines[0] = Menus.item_name(GameCanvas.cursor[19])
            self.lines[1] = self.lines[1] + self.arg1
        elif paramInt == 35:
            self.lines[1] = self.lines[1] + " " + Menus.item_name(GameCanvas.cursor[19])
        elif paramInt == 39:
            self.lines[3] = self.arg1 + "?"
        elif paramInt == 40:
            self.lines[0] = self.arg1
        elif paramInt == 41:
            self.lines[0] = self.arg1 + " " + self.lines[0]
            self.lines[1] = self.arg2 + " " + self.lines[1]
            self.lines[4] = self.arg3 + " Level up"
        elif paramInt == 49:
            self.lines[1] = self.arg2
            self.lines[2] = self.arg1
            self.line_count = 3
        elif paramInt == 54:
            self.lines[0] = "You can't use the ID."
            self.line_count = 1
        self.height = i16(20 * self.line_count + (self.line_count - 1 << 1))
        if self.kind == 2:
            self.height = i16(self.height + 25)
        elif self.kind == 3:
            self.height = 140
        elif self.kind == 4:
            self.height = 150
        elif self.kind == 10:
            self.height = i16(self.height + 30)
        GameCanvas.redraw = 1
        if GameCanvas.live is not None:
            from pow.game.live import Live
            Live.request_redraw()

    @staticmethod
    def show_bought():  # l.java:498-500  (Blacksmith: bought)
        from pow.game.menus import Menus
        return " You bought|1 " + Menus.item_name(GameCanvas.cursor[19]) + '.'

    @staticmethod
    def show_sold():  # l.java:502-504  (Blacksmith: sold)
        from pow.game.menus import Menus
        return " You sold|" + Menus.item_name(GameCanvas.cursor[19]) + '.'

    def setup_popup(self, paramInt):  # l.java:600-891
        self.from_gamestr = 0
        self.drawn = False
        arrayOfByte1 = [2, 2, 2, 4, 3, 3, 5, 3, 3, 3, 2, 2, 2, 2, 2, 5, 3, 2, 2, 3,
                        2, 4, 3, 2, 2, 2, 2, 0, 2, 3, 1, 1, 1, 1, 4, 4, 4, 1, 5, 5, 2, 5, 6]
        arrayOfByte2 = [1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 4, 4, 4, 1, 3, 1, 1, 1, 1, 2,
                        1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 10, 2, 1, 1, 1, 2, 2, 2]
        arrayOfShort = [20, 20, 20, 200, 200, 200, 200, 20, 20, 20, 20, 200, 200, 20, 200, 200, 20, 20, 200, 200,
                        200, 20, 20, 20, 20, 20, 20, 20, 200, 200, 20, 20, 20, 200, 200, 200, 200, 20, 200, 200,
                        200, 200, 200]
        if paramInt == 39:
            self.drawn = True
        self.kind = arrayOfByte2[paramInt]
        if GameCanvas.state == 3:
            GameCanvas.redraw = 1
        else:
            self.popup_redraw = 1
        self.timer = arrayOfShort[paramInt]
        self.line_count = arrayOfByte1[paramInt]
        self.button = 0
        self.popup_id = paramInt
        L = self.lines
        p = paramInt
        if p in _E_TEXT:
            for n, s in enumerate(_E_TEXT[p]):
                L[n] = s
            if p in (5, 28):
                self.button = 1
        elif p == 14:
            L[0] = "What do you want"
            L[1] = "to talk about?"
            for i in range(4):
                L[i + 2] = consts.ba[i]
        elif p in (23, 24, 25, 26):
            L[0] = {23: " / Hp 5 Increased", 24: " / MP 3 Increased",
                    25: " / DEF 1 Increased", 26: " / ATK 1 Increased"}[p][3:]
            L[1] = ""
        elif p == 6:
            dz = GameCanvas.lords[GameCanvas.mission]
            self.set_general(dz.boss_type)
            GameCanvas.popup_lines[0] = GameCanvas.general.name
            GameCanvas.popup_lines[1] = "Lv" + str(GameCanvas.hero.level + dz.level_bonus) + " / Gold: " + str(dz.gold * 150 * (1 + (GameCanvas.difficulty ^ 0x1)))
            L[0] = GameCanvas.popup_lines[0]
            L[1] = GameCanvas.popup_lines[1]
            L[2] = "Do you want to"
            L[3] = "accept this"
            L[4] = "mission?"
        elif p == 15:
            GameCanvas.popup_lines[1] = GameCanvas.general.name
            L[0] = "You visited"
            L[1] = GameCanvas.popup_lines[1] + '.'
            if GameCanvas.seal != 0:
                L[2] = "Friendship:100%"
            else:
                L[2] = "Friendship "
                L[3] = "increased by 5."
            if GameCanvas.gift_level < 8:
                L[5] = GameCanvas.popup_lines[0]
                self.line_count = i16(self.line_count + 1)
            else:
                L[4] = ""
                L[5] = "Press OK"
                self.line_count = i16(self.line_count + 1)
            self.play_sound(10)
        elif p == 16:
            L[0] = "You discussed"
            GameCanvas.popup_lines[0] = consts.ba[GameCanvas.gift_kind] + " with"
            L[1] = GameCanvas.popup_lines[0]
            GameCanvas.popup_lines[1] = GameCanvas.general.name + '.'
            L[2] = GameCanvas.popup_lines[1]
        elif p in (8, 9):  # l.java:679-689  (room / stage banner on the map)
            GameCanvas.popup_lines[0] = "Stage " + str(GameCanvas.rooms_visited)
            if p == 9:
                GameCanvas.popup_lines[0] = GameCanvas.popup_lines[0] + " Complete."
                self.play_sound(5)
            L[0] = GameCanvas.lord_name
            L[1] = GameCanvas.mission_name
            L[2] = GameCanvas.popup_lines[0]
        elif p == 10:  # l.java:690-693
            L[0] = GameCanvas.mission_name
            L[1] = "Mission Success"
        elif p == 13:  # l.java:694-698  (item picked up)
            GameCanvas.popup_lines[0] = GameCanvas.gear_def.name
            L[0] = GameCanvas.popup_lines[0]
            L[1] = "Acquired!!"
        elif p == 22:  # l.java:740-762  (mission failed: maybe an item is lost)
            L[0] = GameCanvas.lord_name
            L[1] = GameCanvas.mission_name
            L[2] = "Mission fail!"
            if GameCanvas.hero.level > 9 and self.rand(100) < GameCanvas.hero.level >> 2:
                i = self.rand(9)
                if GameCanvas.hero.equipped[i].id != 0:
                    GameCanvas.menus.load_item_def(GameCanvas.hero.equipped[i].id)
                    if GameCanvas.hero.equipped[i].id < 300:
                        GameCanvas.popup_lines[0] = GameCanvas.gear_def.name
                    elif GameCanvas.hero.equipped[i].id < 500:
                        GameCanvas.popup_lines[0] = GameCanvas.treasure_def.name
                    else:
                        GameCanvas.popup_lines[0] = GameCanvas.rare_def.name
                    GameCanvas.hero.equipped[i] = None
                    L[3] = "Lost!!"
                    L[4] = GameCanvas.popup_lines[0]
                    self.line_count = i16(self.line_count + 2)
            self.play_sound(6)
        elif p == 27:  # l.java:779-809  (reward item / hidden mission after the ending)
            if GameCanvas.reward_item != 0:
                if GameCanvas.reward_item == 502:
                    GameCanvas.popup_lines[0] = " / Catherine's scarf"[3:]
                else:
                    GameCanvas.menus.load_item_def(GameCanvas.reward_item)
                    GameCanvas.popup_lines[0] = GameCanvas.gear_def.name
                L[0] = GameCanvas.popup_lines[0]
                self.line_count = i16(self.line_count + 1)
                L[1] = "received!"
                self.line_count = i16(self.line_count + 1)
            if GameCanvas.reward_skill != 0:
                # DECOMP-FIX F19: decompiled `i = i + 1; l[i] = ...` is `l[i++] = ...` (as in F9 and in
                # the ef lines just above). Literally l[0] (eg only) or l[2] (ef and eg) is never
                # written and stays None -> the popup's draw fails and the screen after the ending
                # lore stays dark with only SKIP; the hidden mission's name is never drawn.
                f19 = config.DECOMP_FIX["F19"]
                if GameCanvas.reward_item != 0:
                    if f19:
                        L[self.line_count] = ""
                        self.line_count = i16(self.line_count + 1)
                    else:
                        self.line_count = i16(self.line_count + 1)
                        L[self.line_count] = ""
                arrayOfByte = GameCanvas.load_data_file(48)
                j_ = 38 * GameCanvas.reward_skill + 10
                b = 0
                while b < 30 and arrayOfByte[j_ + b] != 0:
                    b += 1
                GameCanvas.lord_names[0] = GameCanvas.read_utf(arrayOfByte, j_, j_ + b)
                if f19:
                    L[self.line_count] = "Hidden Mission!"
                    self.line_count = i16(self.line_count + 1)
                else:
                    self.line_count = i16(self.line_count + 1)
                    L[self.line_count] = "Hidden Mission!"
                GameCanvas.popup_lines[1] = GameCanvas.lord_names[0]
                if f19:
                    L[self.line_count] = GameCanvas.popup_lines[1]
                    self.line_count = i16(self.line_count + 1)
                else:
                    self.line_count = i16(self.line_count + 1)
                    L[self.line_count] = GameCanvas.popup_lines[1]
        self.height = i16(20 * self.line_count + (self.line_count - 1 << 1))
        if self.kind == 2:
            self.height = i16(self.height + 25)
        elif self.kind == 3:
            self.height = 140
        elif self.kind == 4:
            self.height = 150
        elif self.kind == 10:
            self.height = i16(self.height + 25)
        GameCanvas.redraw = 1


# l.java:640-868 - the plain-text cases of e(int), copied 1:1
_E_TEXT = {
    0: ["Saving", "Success!"],
    1: ["Not enough", "FreeSpace."],
    2: ["Not athorized", "Letter."],
    3: ["Starting a new game", "will cause your saved", "game to be deleted.", "Continue?"],
    4: ["Character settings", "are complete.", "Continue?"],
    5: ["Exit Game", "and go to", "main menu?"],
    7: ["Can't Save!", "it Needs all", "enemy dead."],
    17: ["You can't take", "this equipment."],
    18: ["Data is crashed", "Shutting down.."],
    28: ["Exit Game?", ""],
    30: ["Wait.."],
    31: ["Wait..."],
    32: ["Wait...."],
    35: ["Generals can not be", "visited at this time.", "Try again after", "completing a mission."],
    36: ["Difficulty will", "not change", "after starting.", "Continue?"],
    38: ["Not enough", "FreeSpace.", "Please delete", "some files", "before starting."],
    39: ["You must have", "at least 3 items", "in order to have", "them combined.", ""],
    40: ["Would you like", "sound enabled?"],
    41: ["Accessing 'More Games'", "will exit the game", "and open the browser.", "Would you like", "to continue?"],
    # PORT-EXTRA: the original text was "exit the game and open the browser to allow downloading of
    # the Multiplayer version"; in the port YES starts the Multiplayer game itself (main.py)
    42: ["Selecting YES will", "exit the game and", "start the online", "game: Path of a",
         "Warrior Multiplayer.", "Continue?"],
}
