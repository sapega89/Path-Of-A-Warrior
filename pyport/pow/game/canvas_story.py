"""ag.java, part of GameCanvas: story player, dialogues, generals and lords.

A mixin of GameCanvas (pow/game/game_canvas.py); the methods keep their `# ag.java:FROM-TO`
comments. `GameCanvas` below is the real class, set by game_canvas.py once it exists.
"""

from pow.game import consts
from pow.game.gfx import Gfx
from pow.game.jutil import _jchar
from pow.game.scr_table import ScrTable
from pow.midp.jint import i8, i16

GameCanvas = None   # set by pow/game/game_canvas.py


class StoryMixin:
    def start_story(self, story, ending):  # ag.java:3488-3528  (start the story player, bV = 10)
        GameCanvas.story_id = i16(story)
        if story < 100:
            GameCanvas.story_ending = 0
            b = 64 + story // 6
            for i in range(3):
                GameCanvas.story_pages[i] = consts.story_offsets[(story << 1) + i] - consts.story_offsets[story // 6 * 12]
            if story == 3 and ending != 0 and GameCanvas.backpack_slot_of(502) == 0:
                GameCanvas.story_pages[2] = 0
                GameCanvas.story_pages[1] = 0
                GameCanvas.story_pages[0] = 0
                GameCanvas.chapter = 4
            GameCanvas.story_picture = -1
        else:
            GameCanvas.story_ending = 1
            b = 63
            GameCanvas.story_pages[0] = 0
            GameCanvas.story_pages[1] = 2
            GameCanvas.story_pages[2] = 13
            GameCanvas.story_picture = 0
            GameCanvas.menu_items = GameCanvas.game_menu_items
            GameCanvas.menu_return = 0
        if GameCanvas.scr_story is None:
            GameCanvas.scr_story = ScrTable("/" + GameCanvas.scr_data.get(b))
        GameCanvas.talk_lines[1] = ""
        GameCanvas.talk_lines[0] = ""
        GameCanvas.speech_pos[1] = 0
        GameCanvas.speech_pos[0] = 0
        GameCanvas.story_page = 0
        GameCanvas.wait_ticks = 0
        GameCanvas.speech_line = 0
        GameCanvas.scene.load_story_page(GameCanvas.story_page)
        if GameCanvas.story_ending == 0:
            self.draw_menu_background(1)
        GameCanvas.state = 10
        self.play_sound(2)
        GameCanvas.redraw = 1

    # ---- story player (bV == 10): prologue / epilogue -------------------------------------

    def tick_story(self):  # ag.java:1612-1692  (one tick of the story player)
        if GameCanvas.wait_ticks > 0:
            GameCanvas.wait_ticks = i16(GameCanvas.wait_ticks - 1)
            if GameCanvas.key != -999 and GameCanvas.wait_ticks > 3:
                GameCanvas.wait_ticks = 3
            if GameCanvas.wait_ticks == 0:
                GameCanvas.story_page += 1
                if GameCanvas.story_page < GameCanvas.story_pages[2] - GameCanvas.story_pages[0]:
                    GameCanvas.scene.load_story_page(GameCanvas.story_page)
                elif GameCanvas.story_ending == 0 and GameCanvas.menu_return == 0 and GameCanvas.story_page == GameCanvas.story_pages[2] - GameCanvas.story_pages[0]:
                    if GameCanvas.reward_item != 0 or GameCanvas.reward_skill != 0:
                        GameCanvas.popups.setup_popup(27)
                    GameCanvas.scene.load_story_page(GameCanvas.story_page)
                else:
                    GameCanvas.scr_story.free()
                    GameCanvas.scr_story = None
                    GameCanvas.talk_lines[1] = ""
                    GameCanvas.talk_lines[0] = ""
                    self.load_menu_frames()
                    GameCanvas.menu[0] = GameCanvas.menu_return
                    GameCanvas.images[35] = None
                    GameCanvas.images[35] = None
                    GameCanvas.restore_menu_cursor()
                    if GameCanvas.menu[0] == 0:
                        GameCanvas.menu[1] = 0
                    GameCanvas.state = 2
                    GameCanvas.menu_scroll = 0
                    GameCanvas.menu_anim = 0
                GameCanvas.redraw = 1
        elif (GameCanvas.story_ending == 0 and GameCanvas.story_page < GameCanvas.story_pages[1] - GameCanvas.story_pages[0]) or (GameCanvas.story_ending != 0 and GameCanvas.story_page >= GameCanvas.story_pages[1] - GameCanvas.story_pages[0]):
            from pow.game.menus import Menus
            Menus.type_speech(GameCanvas.speech_line, GameCanvas.speech_pos[GameCanvas.speech_line], 0)
            if len(GameCanvas.speech[GameCanvas.speech_line]) <= GameCanvas.speech_pos[GameCanvas.speech_line]:
                if GameCanvas.key != -999:
                    GameCanvas.wait_ticks = 0
                else:
                    GameCanvas.wait_ticks = 15
        else:
            self.draw_story()
            GameCanvas.story_fade = i16(GameCanvas.story_fade + 1)
            if GameCanvas.speech_line == 0:
                if GameCanvas.story_fade > 3:
                    GameCanvas.speech_line = i16(GameCanvas.speech_line + 1)
                    GameCanvas.story_fade = 0
            elif GameCanvas.speech_line == 2:
                if GameCanvas.story_fade > 4:
                    GameCanvas.wait_ticks = 3
            elif GameCanvas.speech_line == 1:
                GameCanvas.speech_pos[0] = GameCanvas.speech_pos[0] - 2
                if GameCanvas.speech_pos[0] < -28:
                    GameCanvas.speech_pos[0] = GameCanvas.speech_pos[0] + 22
                    GameCanvas.speech_done[0] = GameCanvas.speech_done[0] + 1
                    if GameCanvas.text_line_count[0] < GameCanvas.speech_done[0]:
                        if GameCanvas.story_page == GameCanvas.story_pages[2] - GameCanvas.story_pages[0]:
                            GameCanvas.wait_ticks = 3
                        else:
                            GameCanvas.speech_line = i16(GameCanvas.speech_line + 1)
                    GameCanvas.story_fade = 1
        if GameCanvas.key == -6:
            GameCanvas.wait_ticks = 1
            if GameCanvas.story_ending != 0:
                if GameCanvas.story_page >= GameCanvas.story_pages[1] - GameCanvas.story_pages[0]:
                    GameCanvas.story_page = 100
                    return
            elif GameCanvas.story_page < GameCanvas.story_pages[1] - GameCanvas.story_pages[0]:
                GameCanvas.story_page = GameCanvas.story_pages[1] - GameCanvas.story_pages[0] - 1

    def draw_story(self):  # ag.java:1698-1737  (story picture + scrolling text)
        self.fill_screen_rgb(0, 0, 0)
        picture = GameCanvas.images[35]
        if GameCanvas.speech_line in (0, 2):
            if 0 < GameCanvas.story_fade < 4:
                self.draw_map_region(picture, GameCanvas.view_cx - (picture.getWidth() >> 1), GameCanvas.view_cy - (picture.getHeight() >> 1),
                               picture.getWidth(), picture.getHeight(), 0, 0)
        elif GameCanvas.speech_line == 1:
            line_y = GameCanvas.speech_pos[0]
            if GameCanvas.story_page != GameCanvas.story_pages[2] - GameCanvas.story_pages[0]:
                self.draw_map_region(picture, GameCanvas.view_cx - (picture.getWidth() >> 1), GameCanvas.view_cy - (picture.getHeight() >> 1),
                               picture.getWidth(), picture.getHeight(), 0, 0)
            line = GameCanvas.speech_done[0]
            while line <= GameCanvas.text_line_count[0] and line_y <= 230:
                # char arithmetic, as decompiled: `255 - (m - de + 72 << 4)` (only ==255 / ==0 matter)
                if line_y > GameCanvas.view_cy + 72:
                    alpha = 255 - (line_y - GameCanvas.view_cy + 72 << 4) & 0xFFFF
                elif line_y < GameCanvas.view_cy - 72:
                    alpha = 255 - (GameCanvas.view_cy - 72 - line_y << 4) & 0xFFFF
                else:
                    alpha = 255
                Gfx.set_font(GameCanvas.font_black)
                self.draw_text_at(GameCanvas.text_lines[0][line], line_y + 1, 30)
                GameCanvas.draw_text_centred_at(GameCanvas.text_lines[0][line], line_y - 1, 1)
                if alpha == 255:
                    Gfx.set_font(GameCanvas.font_white)
                elif alpha == 0:
                    Gfx.set_font(GameCanvas.font_black)
                else:
                    Gfx.set_font(GameCanvas.font_gray)
                self.draw_text_at(GameCanvas.text_lines[0][line], line_y, 30)
                line_y += 22
                line += 1
        self.draw_skip_key(2)

    def load_chapter_lords(self):  # ag.java:1043-1062  (lords of chapter cq -> ds/dt/du/dv, list dE = dt)
        offset = 0
        data = GameCanvas.load_data_file(48)
        offset = 38 * GameCanvas.chapter + 40
        GameCanvas.lord_count = 0
        for b in range(6):
            GameCanvas.lord_ids[b] = i8(data[offset + b])
            if GameCanvas.lord_ids[b] > 0:
                lord_pos = 38 * GameCanvas.lord_ids[b] + 10
                name_len = 0
                while name_len < 30 and data[lord_pos + name_len] != 0:
                    name_len += 1
                GameCanvas.lord_names[b] = GameCanvas.read_utf(data, lord_pos, lord_pos + name_len)
                GameCanvas.lord_missions[b] = i8(data[lord_pos + 36])
                GameCanvas.lord_mission_counts[b] = i8(data[lord_pos + 37])
                GameCanvas.lord_count += 1
        GameCanvas.menu_count = GameCanvas.lord_count
        GameCanvas.menu_items = GameCanvas.lord_names

    def start_dialogue(self):  # ag.java:2572-2582  (start a dialogue: briefing dG 0, map talk 1, general 2)
        GameCanvas.talk_box = 0
        GameCanvas.talk_row = 0
        GameCanvas.talk_rows = 0
        GameCanvas.talk_side = 0
        GameCanvas.wait_ticks = 0
        GameCanvas.next_speech_pos()
        self.start_dialogue_text()
        if GameCanvas.talk_line < 200:
            self.load_dialogue_line(GameCanvas.talk_line)

    def load_dialogue_line(self, line):  # ag.java:2584-2637  (line paramInt of dialogue file 57+dG -> dp[dR])
        speaker = ""
        offsets = [0] * 60
        parts = [None, None]
        side = GameCanvas.talk_side
        if (GameCanvas.talk_box & 0x1) != 0:
            if GameCanvas.talk_kind == 0:
                speaker = GameCanvas.mission_names[GameCanvas.mission]
            elif GameCanvas.talk_kind in (2, 1):
                if GameCanvas.talk_kind == 2:          # case 2 falls through into case 1
                    if GameCanvas.boss_fight != 0:
                        self.set_general(GameCanvas.lords[GameCanvas.mission].general)
                    else:
                        self.set_general(GameCanvas.cells[GameCanvas.cell].general)
                speaker = GameCanvas.general.name
        else:
            speaker = GameCanvas.hero.name
        data = GameCanvas.load_data_file(57 + GameCanvas.talk_kind)
        count = data[0] & 0xFF | data[1] << 8 & 0xFF00
        for i in range(count + 1):
            offsets[i] = data[2 + i * 2] & 0xFF | data[2 + i * 2 + 1] << 8 & 0xFF00
        parts[0] = GameCanvas.read_utf(data, offsets[line], offsets[line + 1])
        parts[1] = "[" + speaker + "] "
        GameCanvas.text_width = len(parts[0])
        text_start = 0
        for i in range(GameCanvas.text_width):
            if parts[0][i] == "&":
                if text_start != i:
                    # System.arraycopy(String[], m, String, ...) would throw in Java; the game
                    # only prints this marker, so the texts never have '&' after other text
                    GameCanvas.log("=========================check this 96430jfds")
                parts[1] = parts[1] + speaker
                text_start = i + 1
        clean = ""
        for j in range(len(parts[0])):
            if parts[0][j] != "&":
                clean = clean + parts[0][j]
        parts[0] = clean
        if text_start < GameCanvas.text_width:
            parts[1] = parts[1] + parts[0]
        self.word_wrap(bytearray(parts[1].encode("utf-8")), 150, side)

    def start_dialogue_text(self):  # ag.java:2639-2681  (first line dI of the dialogue)
        from pow.game.menus import Menus
        kind = GameCanvas.talk_kind
        if kind == 0:
            if GameCanvas.talk_count > 10:
                GameCanvas.talk_count = 11
                GameCanvas.talk_line = i16(GameCanvas.rand_range(0, 18) + 10 << 1)
                return
            GameCanvas.talk_line = i16(GameCanvas.talk_count - 1 << 1)
            return
        if kind == 1:
            general = 0
            Menus.add_friendship(GameCanvas.talk_general, -5)
            GameCanvas.talk_line = 21
            return
        if kind == 2:
            if GameCanvas.boss_fight != 0:
                general = GameCanvas.lords[GameCanvas.mission].general
            else:
                general = GameCanvas.cells[GameCanvas.cell].general
            if general == 0:
                GameCanvas.redraw = 1
                self.open_menu(2)
                self.load_menu_frames()
                GameCanvas.menu[0] = 0
                GameCanvas.menu_count = consts.menu_sizes[GameCanvas.menu[0]]
                GameCanvas.menu_items = GameCanvas.game_menu_items
                GameCanvas.talk_line = 200
                GameCanvas.state = 2
                GameCanvas.menu_scroll = 0
                GameCanvas.menu_anim = 0
                return
            Menus.add_friendship(general, 5)
            GameCanvas.talk_points = general
            general = GameCanvas.friendship(general)
            if general >= 100:
                general = 95
            GameCanvas.talk_line = i16(general // 10 * 5)

    @staticmethod
    def friendship(general):  # ag.java:2683-2687  (friendship points of general paramInt)
        b = 0
        while b < GameCanvas.general_count and GameCanvas.generals[0][b] != general:
            b += 1
        return 0 if b == GameCanvas.general_count else GameCanvas.generals[1][b]

    @staticmethod
    def next_speech_pos():  # ag.java:2689-2703  (position of the next speech box)
        GameCanvas.talk_box = i16(GameCanvas.talk_box + 1)
        if GameCanvas.talk_kind != 0:
            GameCanvas.talk_x[GameCanvas.talk_side] = 60
            GameCanvas.talk_y[GameCanvas.talk_side] = i16(GameCanvas.view_size.y - 39)
        elif (GameCanvas.talk_box & 0x1) != 0:
            GameCanvas.talk_x[GameCanvas.talk_side] = i16(GameCanvas.view_cx - 60 + 15 + 2)
            GameCanvas.talk_y[GameCanvas.talk_side] = i16(GameCanvas.view_cy - 64)
        else:
            GameCanvas.talk_x[GameCanvas.talk_side] = i16(GameCanvas.view_cx - 60 + -40 + 2)
            GameCanvas.talk_y[GameCanvas.talk_side] = i16(GameCanvas.view_cy - 73 + 107 + 2)
        GameCanvas.talk_chars = 0
        GameCanvas.talk_cursor_x = GameCanvas.talk_x[GameCanvas.talk_side]

    def set_general(self, general):  # ag.java:2705-2726  (general paramInt -> dC)
        data = None
        offset = 0
        data = GameCanvas.load_data_file(46)
        offset = 23 * (general - 1) + 14
        gen = GameCanvas.general
        gen.name = ""
        b = 0
        while b < 11 and data[offset + b] != 0:
            b += 1
        gen.name = GameCanvas.read_utf(data, offset, offset + b)
        gen.look = _jchar(data[offset + 11])
        gen.side = _jchar(data[offset + 11 + 2])
        gen.skills[0] = _jchar(data[offset + 11 + 3])
        gen.skills[1] = _jchar(data[offset + 11 + 4])
        gen.skills[2] = _jchar(data[offset + 11 + 5])
        gen.skills[3] = _jchar(data[offset + 11 + 6])
        gen.portrait = _jchar(data[offset + 11 + 7])
        gen.gift_table = _jchar(data[offset + 11 + 8])
        gen.attack = _jchar(data[offset + 11 + 9])
        gen.defense = _jchar(data[offset + 11 + 10])
        gen.hp = _jchar(data[offset + 11 + 11])
        gen.side = gen.side + 1 & 0x1

    def random_general_skill(self, force):  # ag.java:1494-1505  (random skill of general dC)
        b = 0
        while b < 4 and GameCanvas.general.skills[b] != 0:
            b += 1
        if force != 0:
            while True:
                skill = GameCanvas.general.skills[self.rand(b)]
                if not skill > 0o20:
                    return skill
        return GameCanvas.general.skills[self.rand(b)]
