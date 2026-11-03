"""l.java - popups (cS): drawing, text popups, choices and the key / timer logic."""
import config
from pow.game import consts
from pow.game.game_canvas import GameCanvas
from pow.game.gfx import Gfx
from pow.midp.jint import i16

# PORT-EXTRA popup ids past the original 0..42: the attribute reset (Menus.open_respec)
RESPEC_POPUP = 90           # 3 choices: gold / elixir / cancel
RESPEC_DONE_POPUP = 91      # its result (Ok); no action when it closes


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
        self.choices = 4        # PORT-EXTRA: rows of a kind-3 popup (the original always has 4)

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
                if (GameCanvas.key in (-5, 53)) and self.extra_w > 2:
                    self.extra_w = 2
            elif self.kind == 1:
                if GameCanvas.key in (-5, 53):
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
                key = GameCanvas.key
                if key in (-4, -3, 52, 54):
                    self.button = i16(self.button + 1 & 0x1)
                elif key in (-5, 53):
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
                            menu_id = GameCanvas.menu[0]
                            if menu_id == 3:
                                GameCanvas.menu[0] = 4
                                GameCanvas.talk_kind = 0
                                GameCanvas.talk_count = i16(GameCanvas.talk_count + 1)
                                self.start_dialogue()
                            elif menu_id == 5:
                                if self.popup_id == 28:
                                    self.start_exit()
                                    return -1
                                if self.popup_id in {41, 42}:
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
                            elif menu_id == 8:
                                GameCanvas.reset_quick_items()
                                self.fill_shop()
                                GameCanvas.live_time = GameCanvas.now()
                                if GameCanvas.live is not None:
                                    type(GameCanvas.live).first_login = True     # as.d = true (static)
                                if self.save_game() != 0:
                                    GameCanvas.menus.enter_submenu()
                                    GameCanvas.menu_items = GameCanvas.game_menu_items
                                    GameCanvas.menu[0] = 0
                                    GameCanvas.menu_count = consts.menu_sizes[GameCanvas.menu[0]]
                                    GameCanvas.menu[2] = 0
                                    GameCanvas.menu[1] = 0
                                    self.load_hero_images()
                                    self.start_story(100, 0)
                                else:
                                    GameCanvas.reset_base_stats()
                                    self.setup_popup(1)
                            elif menu_id == 10:
                                GameCanvas.free_hero_images()
                                GameCanvas.menu[0] = 5
                                GameCanvas.menu_count = 10
                                GameCanvas.menu[2] = 0
                                GameCanvas.menu[1] = 0
                            elif menu_id == 29:
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
                elif key == -7 and GameCanvas.menu[0] == 8:
                    self.timer = 1
                    GameCanvas.reset_base_stats()
                    return 1
            elif self.kind == 3:
                if self.timer > 5:
                    key = GameCanvas.key
                    if key in (-1, 50):
                        self.button = i16(self.button - 1)
                        self.button = i16(self.button % self.choices)    # & 0x3 with 4 rows
                    elif key in (-2, 56):
                        self.button = i16(self.button + 1)
                        self.button = i16(self.button % self.choices)
                    elif key in (-5, 53):
                        self.timer = 4
            elif self.kind == 10 and GameCanvas.key in (-5, 53):
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
                popup = self.popup_id
                if popup in (1, 18):
                    self.start_exit()
                elif popup == 15:
                    GameCanvas.menu[0] = 0
                    for b in range(5):
                        GameCanvas.talk_lines[b] = ""
                    GameCanvas.restore_menu_cursor()
                    GameCanvas.menu_items = GameCanvas.game_menu_items
                elif popup == RESPEC_POPUP:     # PORT-EXTRA: attribute reset chosen
                    self.choices = 4
                    GameCanvas.menus.finish_respec(self.button)
                elif popup == 39:
                    GameCanvas.menu[0] = 12
                    GameCanvas.menu_count = consts.menu_sizes[GameCanvas.menu[0]]
                    GameCanvas.menu[1] = 3
                elif popup == 14:
                    from pow.game.menus import Menus
                    GameCanvas.story_page += 1
                    GameCanvas.gift_kind = self.button
                    Menus.load_greeting(0, (GameCanvas.visit_topic << 2) + 2 + self.button)
                    GameCanvas.speech[GameCanvas.story_page & 0x1] = GameCanvas.talk_lines[3]
                elif popup == 16:
                    from pow.game.menus import Menus
                    GameCanvas.hero.live_registered = 0
                    GameCanvas.menus.general_gift()
                    if GameCanvas.seal != 0:
                        GameCanvas.seal = i16(Menus.add_friendship(GameCanvas.generals[2][GameCanvas.visit_row], 5))
                    else:
                        GameCanvas.seal = i16(Menus.add_friendship(GameCanvas.generals[0][GameCanvas.visit_general], 5))
                    self.save_game()
                    self.setup_popup(15)
                elif popup == 9:  # room cleared: the exits open, or the mission's general talks
                    if GameCanvas.cells[GameCanvas.cell].general != 0:
                        GameCanvas.scene.start_victory_talk()
                    else:
                        GameCanvas.room_phase = 1
                        GameCanvas.room_phase_timer = 5
                elif popup == 10:  # l.java:257-260  (Mission Success -> Total Exp)
                    from pow.game.map_scene import MapScene
                    self.setup_popup(11)
                    MapScene.make_exp_bars()
                elif popup == 11:  # l.java:261-268  (Total Exp -> Time Exp, if in time)
                    if GameCanvas.mission_seconds < GameCanvas.lords[GameCanvas.mission].time_limit:
                        self.setup_popup(12)
                        GameCanvas.exp_bar_step = 0
                    else:
                        GameCanvas.scene.finish_mission(1)
                elif popup == 12:  # l.java:269-271
                    GameCanvas.scene.finish_mission(1)
                elif popup == 22:  # l.java:300-315  (Mission fail -> Game Menu)
                    if GameCanvas.lords[GameCanvas.mission].reward > 200:
                        GameCanvas.scene.finish_mission(0)
                    else:
                        self.open_menu(2)
                        self.load_menu_frames()
                        GameCanvas.menu[0] = 0
                        GameCanvas.menu_count = consts.menu_sizes[GameCanvas.menu[0]]
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
            for b in range(self.choices):
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
                gold = GameCanvas.lords[GameCanvas.mission].gold * 150 * (1 + (GameCanvas.difficulty ^ 0x1))
                self.draw_text_at("Gold Acquired!", GameCanvas.view_cy + 10, len("Gold Acquired!") + 1)
                self.draw_big_number(gold, GameCanvas.view_cx + (GameCanvas.decimal_digits(gold) * 9 >> 1) - GameCanvas.view_x, GameCanvas.view_cy + 30, 0)
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

    def draw_popup_frame(self, height):  # l.java:399-423  (popup frame)
        i = GameCanvas.view_cy - (height >> 1) - 10
        if Popups.image is None:
            Popups.image = self.load_image(GameCanvas.scr_ui.get(33))
        frame = Popups.image
        if (GameCanvas.state == 3 or GameCanvas.prev_state == 3) and not GameCanvas.paused:
            i -= 30
        for b in range(26):
            self.draw_map_region(frame, GameCanvas.view_cx - 103 + b * 8 - GameCanvas.view_x, i, 8, 3, 10, 0)
        self.draw_tiled_back(GameCanvas.view_cx - 102 - GameCanvas.view_x, i + 3, 210, height + 14)
        self.draw_map_region(frame, GameCanvas.view_cx - 105 - GameCanvas.view_x, i, 3, 10, 0, 0)
        self.draw_map_region(frame, GameCanvas.view_cx + 104 - GameCanvas.view_x, i, 3, 10, 2, 0)
        i += 10
        frame_lines = [[GameCanvas.view_cx - 105 - GameCanvas.view_x, 162, 162, 162, GameCanvas.view_cx + 106 - GameCanvas.view_x],
                      [GameCanvas.view_cx - 104 - GameCanvas.view_x, 67, 67, 67, GameCanvas.view_cx + 105 - GameCanvas.view_x],
                      [GameCanvas.view_cx - 103 - GameCanvas.view_x, 33, 33, 33, GameCanvas.view_cx + 104 - GameCanvas.view_x]]
        for b in range(3):
            col = GameCanvas.rgb(frame_lines[b][1], frame_lines[b][2], frame_lines[b][3])
            Gfx.draw_line(frame_lines[b][0] + GameCanvas.view_x, i + GameCanvas.view_y, frame_lines[b][0] + GameCanvas.view_x, i + height - 1 + GameCanvas.view_y, col)
            Gfx.draw_line(frame_lines[b][4] + GameCanvas.view_x, i + GameCanvas.view_y, frame_lines[b][4] + GameCanvas.view_x, i + height - 1 + GameCanvas.view_y, col)
        i += height
        self.draw_map_region(frame, GameCanvas.view_cx - 105 - GameCanvas.view_x, i, 3, 10, 5, 0)
        self.draw_map_region(frame, GameCanvas.view_cx + 104 - GameCanvas.view_x, i, 3, 10, 7, 0)
        i += 7
        for b in range(26):
            self.draw_map_region(frame, GameCanvas.view_cx - 103 + b * 8 - GameCanvas.view_x, i, 8, 3, 10, 3)

    def draw_tiled_back(self, x, y, w, h):  # l.java:425-446  (tiled ui_back)
        if GameCanvas.images[10] is None:
            GameCanvas.images[10] = self.load_image(GameCanvas.scr_ui.get(59))
        b = 0
        while b * 24 < h:
            if h >= (b + 1) * 24:
                i = 24
            else:
                i = h - b * 24
            col = 0
            while col * 52 < w:
                if w >= (col + 1) * 52:
                    tile_w = 52
                else:
                    tile_w = w - col * 52
                if GameCanvas.images[10] is not None:
                    self.draw_map_region(GameCanvas.images[10], x + col * 52, y + b * 24, tile_w, i, 0, 0)
                col += 1
            b += 1

    def draw_yes_no(self, y):  # l.java:448-461  (Yes / No buttons)
        for b in range(2):
            if self.button == b:
                Gfx.set_font(GameCanvas.font_white)
                bool_ = True
            else:
                Gfx.set_font(GameCanvas.font_gray)
                bool_ = False
            self.draw_box(GameCanvas.view_cx - 60 + b * 80, y + GameCanvas.view_y, 40, 17, bool_)
            GameCanvas.draw_view_text_centred(consts.yes_no_ok[b], GameCanvas.view_cx - 40 + b * 80, y + 1)

    def draw_ok(self, y):  # l.java:463-467  (Ok button)
        Gfx.set_font(GameCanvas.font_white)
        self.draw_box(GameCanvas.view_cx - 60 + 40 + GameCanvas.view_x, y + GameCanvas.view_y, 40, 17, True)
        GameCanvas.draw_view_text_centred(consts.yes_no_ok[2], GameCanvas.view_cx, y)

    def show_text(self, text):  # l.java:469-496  ("<kind>line|line|...")
        self.drawn = False
        i = 1
        if text != "":
            self.kind = i16(ord(text[0]) - 48)
            if self.kind == 3:
                self.kind = 10
                self.timer = 200
            line = 0
            for b in range(len(text)):
                if text[b] == "|":
                    # DECOMP-FIX F9 (proposed): decompiled `s = s + 1; l[s] = ...` is `l[s++] = ...`;
                    # literally, line 0 keeps stale text and the last line is never drawn.
                    if config.DECOMP_FIX["F9"]:
                        self.lines[line] = text[i:b]
                        line = i16(line + 1)
                    else:
                        line = i16(line + 1)
                        self.lines[line] = text[i:b]
                    i = b + 1
            if config.DECOMP_FIX["F9"]:
                self.lines[line] = text[i:]
                line = i16(line + 1)
            else:
                line = i16(line + 1)
                self.lines[line] = text[i:]
            self.line_count = line
            self.height = i16(20 * line + (line - 1) * 2)
            if self.kind in {2, 10}:
                self.height = i16(self.height + 20)
            if self.timer == 0:
                self.timer = 10
            self.popup_redraw = 1

    def show(self, popup):  # l.java:506-598  (gamestr popup N: text gamestr[N+15], kind from its first digit)
        from pow.game.menus import Menus
        self.from_gamestr = 1
        self.drawn = False
        if GameCanvas.state == 3:
            GameCanvas.redraw = 1
        else:
            GameCanvas.popups.popup_redraw = 1
        self.button = 0
        self.popup_id = i16(popup)
        raw = GameCanvas.gamestr(popup + 15)
        first = raw[0]
        if "0" <= first <= "9":
            self.kind = i16(ord(first) - 48)
            if self.kind != 2:
                self.kind = 10
            text = raw[1:]
        else:
            self.kind = 10
            text = raw
        self.timer = 200
        i = len(text)
        line = 0
        j = 0
        for pos in range(i + 1):
            if pos == i or text[pos] == "\\":
                if j == pos:
                    self.lines[line] = " "
                else:
                    self.lines[line] = text[j:pos]
                line += 1
                j = pos + 1
        self.line_count = i16(line)
        if popup == 53:
            self.line_count = 4
            self.lines[0] = self.arg1
            self.lines[1] = self.arg2
            self.lines[2] = self.arg3
            self.lines[3] = self.arg4
        elif popup == 34:
            self.lines[0] = Menus.item_name(GameCanvas.cursor[19])
            self.lines[1] = self.lines[1] + self.arg1
        elif popup == 35:
            self.lines[1] = self.lines[1] + " " + Menus.item_name(GameCanvas.cursor[19])
        elif popup == 39:
            self.lines[3] = self.arg1 + "?"
        elif popup == 40:
            self.lines[0] = self.arg1
        elif popup == 41:
            self.lines[0] = self.arg1 + " " + self.lines[0]
            self.lines[1] = self.arg2 + " " + self.lines[1]
            self.lines[4] = self.arg3 + " Level up"
        elif popup == 49:
            self.lines[1] = self.arg2
            self.lines[2] = self.arg1
            self.line_count = 3
        elif popup == 54:
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
        return " You bought|1 " + Menus.item_name(GameCanvas.cursor[19]) + "."

    @staticmethod
    def show_sold():  # l.java:502-504  (Blacksmith: sold)
        from pow.game.menus import Menus
        return " You sold|" + Menus.item_name(GameCanvas.cursor[19]) + "."

    def setup_choice(self, popup_id, text, choices):
        """PORT-EXTRA: a kind-3 popup (like e(14)) with its own text and 2..4 choice rows; the
        chosen row comes to _tick_timer() under popup_id as self.button."""
        self.from_gamestr = 0
        self.drawn = False
        self.kind = 3
        self.timer = 200
        self.button = 0
        self.popup_id = popup_id
        if len(text) != 2:          # draw_popup() takes the rows from lines[2..]
            raise ValueError("setup_choice: the text has %d lines, 2 expected" % len(text))
        self.line_count = len(text)
        self.choices = len(choices)
        for n, s in enumerate(list(text) + list(choices)):
            self.lines[n] = s
        self.height = 140 - 16 * (4 - self.choices)     # e(int) gives kind 3 a height of 140
        self.popup_redraw = 1
        GameCanvas.redraw = 1

    def setup_popup(self, popup):  # l.java:600-891
        self.from_gamestr = 0
        self.choices = 4
        self.drawn = False
        line_counts = [2, 2, 2, 4, 3, 3, 5, 3, 3, 3, 2, 2, 2, 2, 2, 5, 3, 2, 2, 3,
                        2, 4, 3, 2, 2, 2, 2, 0, 2, 3, 1, 1, 1, 1, 4, 4, 4, 1, 5, 5, 2, 5, 6]
        kinds = [1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 4, 4, 4, 1, 3, 1, 1, 1, 1, 2,
                        1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 10, 2, 1, 1, 1, 2, 2, 2]
        timers = [20, 20, 20, 200, 200, 200, 200, 20, 20, 20, 20, 200, 200, 20, 200, 200, 20, 20, 200, 200,
                        200, 20, 20, 20, 20, 20, 20, 20, 200, 200, 20, 20, 20, 200, 200, 200, 200, 20, 200, 200,
                        200, 200, 200]
        if popup == 39:
            self.drawn = True
        self.kind = kinds[popup]
        if GameCanvas.state == 3:
            GameCanvas.redraw = 1
        else:
            self.popup_redraw = 1
        self.timer = timers[popup]
        self.line_count = line_counts[popup]
        self.button = 0
        self.popup_id = popup
        lines = self.lines
        p = popup
        if p in _E_TEXT:
            for n, s in enumerate(_E_TEXT[p]):
                lines[n] = s
            if p in (5, 28):
                self.button = 1
        elif p == 14:
            lines[0] = "What do you want"
            lines[1] = "to talk about?"
            for i in range(4):
                lines[i + 2] = consts.gift_kinds[i]
        elif p in (23, 24, 25, 26):
            lines[0] = {23: " / Hp 5 Increased", 24: " / MP 3 Increased",
                    25: " / DEF 1 Increased", 26: " / ATK 1 Increased"}[p][3:]
            lines[1] = ""
        elif p == 6:
            lord = GameCanvas.lords[GameCanvas.mission]
            self.set_general(lord.boss_type)
            GameCanvas.popup_lines[0] = GameCanvas.general.name
            GameCanvas.popup_lines[1] = "Lv" + str(GameCanvas.hero.level + lord.level_bonus) + " / Gold: " + str(lord.gold * 150 * (1 + (GameCanvas.difficulty ^ 0x1)))
            lines[0] = GameCanvas.popup_lines[0]
            lines[1] = GameCanvas.popup_lines[1]
            lines[2] = "Do you want to"
            lines[3] = "accept this"
            lines[4] = "mission?"
        elif p == 15:
            GameCanvas.popup_lines[1] = GameCanvas.general.name
            lines[0] = "You visited"
            lines[1] = GameCanvas.popup_lines[1] + "."
            if GameCanvas.seal != 0:
                lines[2] = "Friendship:100%"
            else:
                lines[2] = "Friendship "
                lines[3] = "increased by 5."
            if GameCanvas.gift_level < 8:
                lines[5] = GameCanvas.popup_lines[0]
                self.line_count = i16(self.line_count + 1)
            else:
                lines[4] = ""
                lines[5] = "Press OK"
                self.line_count = i16(self.line_count + 1)
            self.play_sound(10)
        elif p == 16:
            lines[0] = "You discussed"
            GameCanvas.popup_lines[0] = consts.gift_kinds[GameCanvas.gift_kind] + " with"
            lines[1] = GameCanvas.popup_lines[0]
            GameCanvas.popup_lines[1] = GameCanvas.general.name + "."
            lines[2] = GameCanvas.popup_lines[1]
        elif p in (8, 9):  # l.java:679-689  (room / stage banner on the map)
            GameCanvas.popup_lines[0] = "Stage " + str(GameCanvas.rooms_visited)
            if p == 9:
                GameCanvas.popup_lines[0] = GameCanvas.popup_lines[0] + " Complete."
                self.play_sound(5)
            lines[0] = GameCanvas.lord_name
            lines[1] = GameCanvas.mission_name
            lines[2] = GameCanvas.popup_lines[0]
        elif p == 10:  # l.java:690-693
            lines[0] = GameCanvas.mission_name
            lines[1] = "Mission Success"
        elif p == 13:  # l.java:694-698  (item picked up)
            GameCanvas.popup_lines[0] = GameCanvas.gear_def.name
            lines[0] = GameCanvas.popup_lines[0]
            lines[1] = "Acquired!!"
        elif p == 22:  # l.java:740-762  (mission failed: maybe an item is lost)
            lines[0] = GameCanvas.lord_name
            lines[1] = GameCanvas.mission_name
            lines[2] = "Mission fail!"
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
                    lines[3] = "Lost!!"
                    lines[4] = GameCanvas.popup_lines[0]
                    self.line_count = i16(self.line_count + 2)
            self.play_sound(6)
        elif p == 27:  # l.java:779-809  (reward item / hidden mission after the ending)
            if GameCanvas.reward_item != 0:
                if GameCanvas.reward_item == 502:
                    GameCanvas.popup_lines[0] = " / Catherine's scarf"[3:]
                else:
                    GameCanvas.menus.load_item_def(GameCanvas.reward_item)
                    GameCanvas.popup_lines[0] = GameCanvas.gear_def.name
                lines[0] = GameCanvas.popup_lines[0]
                self.line_count = i16(self.line_count + 1)
                lines[1] = "received!"
                self.line_count = i16(self.line_count + 1)
            if GameCanvas.reward_skill != 0:
                # DECOMP-FIX F19: decompiled `i = i + 1; l[i] = ...` is `l[i++] = ...` (as in F9 and in
                # the ef lines just above). Literally l[0] (eg only) or l[2] (ef and eg) is never
                # written and stays None -> the popup's draw fails and the screen after the ending
                # lore stays dark with only SKIP; the hidden mission's name is never drawn.
                fix_f19 = config.DECOMP_FIX["F19"]
                if GameCanvas.reward_item != 0:
                    if fix_f19:
                        lines[self.line_count] = ""
                        self.line_count = i16(self.line_count + 1)
                    else:
                        self.line_count = i16(self.line_count + 1)
                        lines[self.line_count] = ""
                data = GameCanvas.load_data_file(48)
                pos = 38 * GameCanvas.reward_skill + 10
                b = 0
                while b < 30 and data[pos + b] != 0:
                    b += 1
                GameCanvas.lord_names[0] = GameCanvas.read_utf(data, pos, pos + b)
                if fix_f19:
                    lines[self.line_count] = "Hidden Mission!"
                    self.line_count = i16(self.line_count + 1)
                else:
                    self.line_count = i16(self.line_count + 1)
                    lines[self.line_count] = "Hidden Mission!"
                GameCanvas.popup_lines[1] = GameCanvas.lord_names[0]
                if fix_f19:
                    lines[self.line_count] = GameCanvas.popup_lines[1]
                    self.line_count = i16(self.line_count + 1)
                else:
                    self.line_count = i16(self.line_count + 1)
                    lines[self.line_count] = GameCanvas.popup_lines[1]
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
