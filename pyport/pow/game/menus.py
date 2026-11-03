"""e.java - menu screens (bb). Literal port, Phase 0 subset:
Main Menu (cM[0] == 5) and the Game Menu carousel (cM[0] == 0), with the full key routing
(a(), aB/aC/aD/aE = up/down/left/right, b() = fire, aF() = back).
Screens of later phases raise NotPorted.
"""
import config
from pow.game import consts
from pow.game.game_canvas import GameCanvas
from pow.game.name_buffer import NameBuffer
from pow.game.res_reader import ResReader
from pow.game.structs import Item, MissionDef, Point, Rect
from pow.game.gfx import Gfx
from pow.midp.jint import i8, i16, i32, idiv, imod
from pow.game.font import Font
from pow.game.scr_table import ScrTable
from pow.game.arr_table import ArrTable
from pow.game import hero_classes
from pow.game.popups import RESPEC_POPUP, RESPEC_DONE_POPUP

F6 = config.DECOMP_FIX["F6"]
F10 = config.DECOMP_FIX["F10"]
F11 = config.DECOMP_FIX["F11"]


def _dec_cmp(v):
    """DECOMP-FIX F6: `cM[i] = cM[i] - 1; if (cM[i] - 1 < 0)` is a broken `if (--cM[i] < 0)`."""
    return v if F6 else v - 1


def _inc_cmp(v):
    """DECOMP-FIX F6: `cM[i] = cM[i] + 1; if (cM[i] + 1 >= n)` is a broken `if (++cM[i] >= n)`."""
    return v if F6 else v + 1


def ar_c(paramInt):  # ar.java:249-261  (Assign Items: put potion slot cM[1] on key * (0) or # (1))
    cz = GameCanvas.hero
    if cz.quick_slots[GameCanvas.menu[1]].item != 0 and cz.quick_keys[paramInt] != GameCanvas.menu[1]:
        if GameCanvas.menu[1] == cz.quick_keys[paramInt + 1 & 0x1]:
            i = cz.quick_keys[paramInt]
            cz.quick_keys[paramInt] = cz.quick_keys[paramInt + 1 & 0x1]
            cz.quick_keys[paramInt + 1 & 0x1] = i
        else:
            cz.quick_keys[paramInt] = i8(GameCanvas.menu[1])
        return 1
    return 0


class Menus(GameCanvas):
    mix_table = None  # public static byte[] a;   e.java:4

    def __init__(self):  # e.java:6-8
        super().__init__(GameCanvas.midlet)

    def draw_menu(self, paramInt):  # e.java:10-205  (draw the current menu; 1 = first frame, 2 = animation)
        cM = GameCanvas.menu
        if paramInt == 1:
            if cM[0] != 5:
                Gfx.set_font(GameCanvas.font_white)
                if GameCanvas.prev_state == 3:
                    Gfx.fill_rect(7, 19, 225, 242, 0)
                else:
                    self.draw_menu_frame()
                if cM[0] != 28:
                    if GameCanvas.prev_state == 3:
                        Gfx.set_font(GameCanvas.font_white)
                        self.draw_text_at(GameCanvas.menu_titles[cM[0]], 15, 0)
                    else:
                        self.draw_text_at(GameCanvas.menu_titles[cM[0]], 2 - GameCanvas.view_y, 0)
                else:
                    str_ = GameCanvas.split_field(GameCanvas.help_items[0], GameCanvas.help_topic)
                    if GameCanvas.prev_state == 3:
                        Gfx.set_font(GameCanvas.font_white)
                        self.draw_text_at(str_, 15, 0)
                    else:
                        self.draw_text_at(str_, 2 - GameCanvas.view_y, 0)
                if consts.u[cM[0]] != -1 or (consts.u[cM[0]] == -1 and cM[0] == 15):
                    if cM[0] == 3:
                        GameCanvas.draw_softkeys(11, 2)
                    elif cM[0] == 14:   # PORT-EXTRA: RESET the attributes (hero_classes)
                        GameCanvas.draw_softkeys(12, 2)
                    else:
                        GameCanvas.draw_softkeys(-1, 2)
            v = cM[0]
            if v == 0:
                GameCanvas.menu_scroll = 0
                GameCanvas.menu_anim = 0
                self.draw_game_menu()
            elif v == 5:
                self.draw_title()
                self.draw_main_menu()
            elif v in (1, 2, 10, 11, 12, 13, 25, 27):
                self.draw_list_menu()
            elif v == 9:
                self.draw_options()
            elif v == 28:
                self.draw_help_page()
            elif v == 6:
                self.draw_hero_choice()
            elif v == 7:
                self.draw_name_captions()
                self.draw_name_box()
            elif v in (8, 14):
                self.draw_stat_sheet(1)
            elif v == 29:
                self.draw_difficulty()
            elif v == 15:
                self.draw_skills(0)
                self.draw_description_strip()
            elif v == 16:
                self.draw_gear(cM[2], 0)
                self.draw_description_strip()
                GameCanvas.draw_softkeys(5, -1)
            elif v == 17:
                self.draw_inventory(0)
                self.draw_description_strip()
                GameCanvas.draw_softkeys(5, -1)
            elif v == 18:
                self.draw_assign_items(0)
                self.draw_description_strip()
            elif v in (21, 22, 23, 24):
                self.draw_blacksmith(True)
                self.draw_description_strip()
            elif v == 3:
                self.draw_mission_text()
            elif v == 4:
                self.draw_briefing()
            elif v == 19:
                self.draw_generals()
            elif v == 20:
                self.draw_story_portraits(GameCanvas.story_picture)
                if GameCanvas.speech_pos[0] > 0:
                    Menus.type_speech(GameCanvas.story_page + 1 & 0x1, 0, 1)
                if GameCanvas.speech_pos[1] > 0:
                    Menus.type_speech(GameCanvas.story_page & 0x1, 0, 1)
            if GameCanvas.popups.kind != 0:
                GameCanvas.popups.draw_popup()
                return
        else:
            if paramInt == 2:
                v = cM[0]
                if v == 0:
                    self.draw_game_menu()
                    return
                if v == 4:
                    Gfx.set_font(GameCanvas.font_white)
                    self.draw_menu_frame()
                    self.draw_briefing()
                    GameCanvas.key = -5
                    GameCanvas.wait_ticks = 0
                    self.tick_dialogue()
                    GameCanvas.redraw -= 1
                return
            if GameCanvas.popups.kind != 0:
                if GameCanvas.popups.popup_redraw != 0:
                    GameCanvas.popups.draw_popup()
                    return
            else:
                v = cM[0]
                if v == 0:
                    self.draw_game_menu()
                    return
                if v == 5:
                    self.draw_title()
                    self.draw_main_menu()
                    return
                if v == 7:
                    self.draw_name_box()
                    GameCanvas.draw_letter_grid(GameCanvas.letter_cursor, GameCanvas.view_cy + 32 + GameCanvas.view_y)
                    return
                if v in (8, 14):
                    if GameCanvas.menu_part != 0:
                        self.draw_stat_sheet(0)
                        return
                    return
                if v == 15:
                    if GameCanvas.menu_part != 0:
                        self.draw_skills(GameCanvas.menu_part)
                    self.draw_description_strip()
                    return
                if v == 16:
                    self.draw_description_strip()
                    return
                if v == 17:
                    if GameCanvas.menu_part != 0:
                        self.draw_inventory(1)
                    self.draw_description_strip()
                    return
                if v == 18:
                    if GameCanvas.menu_part != 0:
                        self.draw_assign_items(1)
                    self.draw_description_strip()
                    return
                if v in (21, 22, 23, 24):
                    self.draw_blacksmith(False)
                    self.draw_description_strip()
                    return
                if v == 4:
                    self.tick_dialogue()
                    return
                if v == 20:
                    self.tick_general_talk()
                    return

    def menu_keys(self):  # e.java:207-302  (keys of the menus)
        if GameCanvas.debug_keys:
            GameCanvas.score = -1
        v = GameCanvas.menu[0]
        if v == 4:
            return
        if v == 7:
            i = GameCanvas.move_letter_cursor(GameCanvas.key)
            if i == -7:
                if len(GameCanvas.name_buf.get_text()) == 0:
                    GameCanvas.menu[0] = 6
                    GameCanvas.redraw = 1
                    return
                GameCanvas.name_buf.handle_key(-8)
                return
            if i == -5 or i == 53:
                if GameCanvas.letter_cursor == 26:
                    if len(GameCanvas.name_buf.get_text()) != 0:
                        GameCanvas.hero.name = GameCanvas.name_buf.get_text()
                        GameCanvas.name_buf.set_text(GameCanvas.hero.name)
                        GameCanvas.menu[0] = 8
                        GameCanvas.update_hero_stats()
                        GameCanvas.menu_count = 4
                        GameCanvas.reset_base_stats()
                        return
                else:
                    if len(GameCanvas.name_buf.get_text()) == 0:
                        b = 65
                    else:
                        b = 97
                    GameCanvas.name_buf.handle_key(b + GameCanvas.letter_cursor)
                    return
            return
        if v == 20:
            if GameCanvas.key != -5:
                GameCanvas.key = -999
                return
            return
        if v in (21, 22, 23, 24):
            self.blacksmith_keys()
            return
        ch = GameCanvas.key
        if ch in (-1, 50):
            self.key_up()
            return
        if ch in (-2, 56):
            self.key_down_arrow()
            return
        if ch in (-3, 52):
            self.key_left()
            return
        if ch in (-4, 54):
            self.key_right()
            return
        if ch == 42:
            if GameCanvas.menu[0] == 18:
                GameCanvas.redraw = ar_c(0)
                return
        elif ch == 35:
            if GameCanvas.menu[0] == 18:
                GameCanvas.redraw = ar_c(1)
                return
        elif ch in (-5, 53):
            self.key_fire()
            return
        elif ch == -6:
            if GameCanvas.menu[0] == 14:    # PORT-EXTRA: attribute reset
                self.open_respec()
                return
            if GameCanvas.menu[0] == 16 or GameCanvas.menu[0] == 17 or GameCanvas.menu[0] == 3:
                self.key_fire()
                return
        elif ch == -7:
            self.key_back()

    @staticmethod
    def menu_link(paramInt1, paramInt2):  # e.java:304-307
        return consts.aW[paramInt1][paramInt2]

    def key_up(self):  # e.java:309-392  (UP)
        cM = GameCanvas.menu
        v = cM[0]
        if v == 0:
            if GameCanvas.menu_scroll == 0:
                GameCanvas.redraw = 2
                GameCanvas.menu_scroll = -1
            return
        if v in (3, 5, 6, 18, 20, 28):
            return
        if v in (8, 14):
            self.draw_stat_cursor(0)
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 0:
                cM[1] = GameCanvas.menu_count - 1
            self.draw_stat_cursor(1)
            return
        if v == 9:
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 1:
                cM[1] = GameCanvas.menu_count - 1
            if not GameCanvas.sound_on and cM[1] == 1:
                cM[1] = 0
            GameCanvas.clamp_menu_scroll()
            GameCanvas.redraw = 1
            return
        if v == 15:
            if cM[3] == 2:
                if cM[1] < 4:
                    cM[2] = cM[2] - 3
                    if cM[2] < 0:
                        cM[2] = cM[2] + 18
                    GameCanvas.menu_part = 3
                GameCanvas.menu_part = 3
                return
            return
        if v == 16:
            cM[2] = cM[2] + 1
            if _inc_cmp(cM[2]) >= GameCanvas.menu_count:
                cM[2] = 0
            GameCanvas.redraw = 1
            return
        if v == 17:
            cM[2] = cM[2] - 5
            if cM[2] < 0:
                cM[2] = cM[2] + 25
            GameCanvas.menu_part = 1
            return
        if v == 19:
            if cM[1] > 0:
                cM[1] = cM[1] - 1
                GameCanvas.redraw = 1
                return
            return
        if v == 29:
            cM[1] = 1 - cM[1]
            GameCanvas.redraw = 1
            return
        if v == 25:
            if cM[1] == 20:
                cM[1] = 23
            else:
                cM[1] = cM[1] - 1
            if cM[1] < cM[2]:
                cM[1] = cM[2] + 4
            GameCanvas.redraw = 1
            return
        cM[1] = cM[1] - 1
        if _dec_cmp(cM[1]) < 0:
            cM[1] = GameCanvas.menu_count - 1
        GameCanvas.clamp_menu_scroll()
        GameCanvas.redraw = 1

    def key_down_arrow(self):  # e.java:394-480  (DOWN)
        cM = GameCanvas.menu
        v = cM[0]
        if v == 0:
            if GameCanvas.menu_scroll == 0:
                GameCanvas.menu_scroll = 1
                GameCanvas.redraw = 2
            return
        if v in (3, 5, 6, 18, 20, 28):
            return
        if v in (8, 14):
            self.draw_stat_cursor(0)
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= GameCanvas.menu_count:
                cM[1] = 0
            self.draw_stat_cursor(1)
            return
        if v == 9:
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= GameCanvas.menu_count:
                cM[2] = 0
                cM[1] = 0
            if not GameCanvas.sound_on and cM[1] == 1:
                cM[1] = 2
            GameCanvas.clamp_menu_scroll()
            GameCanvas.redraw = 1
            return
        if v == 15:
            if cM[3] == 2:
                if cM[1] < 4:
                    cM[2] = cM[2] + 3
                    if cM[2] > 17:
                        cM[2] = cM[2] - 18
                GameCanvas.menu_part = 3
                return
            return
        if v == 16:
            cM[2] = cM[2] - 1
            if _dec_cmp(cM[2]) < 0:
                cM[2] = GameCanvas.menu_count - 1
            GameCanvas.redraw = 1
            return
        if v == 17:
            cM[2] = cM[2] + 5
            if cM[2] > 24:
                cM[2] = cM[2] - 25
            GameCanvas.menu_part = 1
            return
        if v == 19:
            if cM[1] < GameCanvas.menu_count - 1:
                cM[1] = cM[1] + 1
                GameCanvas.redraw = 1
                return
            return
        if v == 29:
            cM[1] = 1 - cM[1]
            GameCanvas.redraw = 1
            return
        if v == 25:
            if cM[1] == 23:
                cM[1] = 20
            else:
                cM[1] = cM[1] + 1
            if cM[1] > cM[2] + 4:
                cM[1] = cM[2]
            GameCanvas.redraw = 1
            return
        cM[1] = cM[1] + 1
        if _inc_cmp(cM[1]) >= GameCanvas.menu_count:
            cM[2] = 0
            cM[1] = 0
        GameCanvas.clamp_menu_scroll()
        GameCanvas.redraw = 1

    def key_left(self):  # e.java:482-584  (LEFT)
        cM = GameCanvas.menu
        v = cM[0]
        if v == 1:
            if GameCanvas.debug_keys and GameCanvas.chapter > 0:
                GameCanvas.chapter = i8(GameCanvas.chapter - 1)
                self.load_chapter_lords()
                GameCanvas.redraw = 1
            return
        if v == 3:
            if cM[2] > 0:
                cM[2] = cM[2] - 1
            else:
                cM[2] = GameCanvas.text_line_count[0] // 6
            GameCanvas.redraw = 1
            return
        if v == 28:
            if cM[1] <= 0 and GameCanvas.help_topic == 8:
                cM[1] = 1
                GameCanvas.redraw = 1
                return
            GameCanvas.redraw = 1
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 0:
                cM[1] = consts.z[GameCanvas.help_topic + 1] - consts.z[GameCanvas.help_topic] - 1
                return
            return
        if v == 5:
            GameCanvas.redraw = 1
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 0:
                cM[1] = 8
                return
            return
        if v == 18:
            GameCanvas.menu_part = 1
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 0:
                cM[1] = GameCanvas.menu_count - 1
                return
            return
        if v == 6:
            GameCanvas.hero.head = GameCanvas.hero.head - 1 & 0x3
            GameCanvas.redraw = 1
            return
        if v == 9:
            self.change_option(0)
            GameCanvas.redraw = 1
            return
        if v == 15:
            c3 = cM[3]
            cM[c3] = cM[c3] - 1
            if cM[3] == 1:
                if cM[c3] < 0:
                    cM[c3] = 4
                GameCanvas.menu_part = 2
                return
            if cM[1] < 4:
                if cM[c3] < 0:
                    cM[c3] = 17
            elif cM[c3] < 18:
                cM[c3] = 20
            GameCanvas.menu_part = 3
            return
        if v == 16:
            GameCanvas.redraw = 1
            cM[2] = cM[2] + 1
            if _inc_cmp(cM[2]) >= GameCanvas.menu_count:
                cM[2] = 0
                return
            return
        if v == 17:
            cM[2] = cM[2] - 1
            if _dec_cmp(cM[2]) < 0:
                cM[2] = GameCanvas.menu_count - 1
            GameCanvas.menu_part = 1
            return
        if v == 19:
            cM[1] = cM[1] - 4
            if cM[1] < 0:
                cM[1] = 0
            GameCanvas.redraw = 1
            return
        if v == 25:
            cM[2] = cM[2] - 5
            cM[1] = cM[1] - 5
            if cM[2] < 0:
                cM[2] = 20
                cM[1] = 20 + imod(cM[1] + 20, 5)
            GameCanvas.redraw = 1

    def key_right(self):  # e.java:586-686  (RIGHT)
        cM = GameCanvas.menu
        v = cM[0]
        if v == 1:
            if GameCanvas.debug_keys and GameCanvas.chapter < 44:
                GameCanvas.chapter = i8(GameCanvas.chapter + 1)
                self.load_chapter_lords()
                GameCanvas.redraw = 1
            return
        if v == 3:
            if (cM[2] + 1) * 6 - 1 < GameCanvas.text_line_count[0]:
                cM[2] = cM[2] + 1
            else:
                cM[2] = 0
            GameCanvas.redraw = 1
            return
        if v == 28:
            if cM[1] >= 1 and GameCanvas.help_topic == 8:
                GameCanvas.redraw = 1
                cM[1] = 0
                return
            GameCanvas.redraw = 1
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= consts.z[GameCanvas.help_topic + 1] - consts.z[GameCanvas.help_topic]:
                cM[1] = 0
                return
            return
        if v == 5:
            GameCanvas.redraw = 1
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= 9:
                cM[1] = 0
                return
            return
        if v == 18:
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= GameCanvas.menu_count:
                cM[1] = 0
            GameCanvas.menu_part = 1
            return
        if v == 6:
            GameCanvas.hero.head = GameCanvas.hero.head + 1 & 0x3
            GameCanvas.redraw = 1
            return
        if v == 9:
            self.change_option(1)
            GameCanvas.redraw = 1
            return
        if v == 15:
            c3 = cM[3]
            cM[c3] = cM[c3] + 1
            if cM[3] == 1:
                if cM[c3] > 4:
                    cM[c3] = 0
                GameCanvas.menu_part = 2
                return
            if cM[1] < 4:
                if cM[c3] > 17:
                    cM[c3] = 0
            elif cM[c3] > 20:
                cM[c3] = 18
            GameCanvas.menu_part = 3
            return
        if v == 16:
            GameCanvas.redraw = 1
            cM[2] = cM[2] - 1
            if _dec_cmp(cM[2]) < 0:
                cM[2] = GameCanvas.menu_count - 1
                return
            return
        if v == 17:
            cM[2] = cM[2] + 1
            if _inc_cmp(cM[2]) >= GameCanvas.menu_count:
                cM[2] = 0
            GameCanvas.menu_part = 1
            return
        if v == 19:
            cM[1] = cM[1] + 4
            if cM[1] >= GameCanvas.menu_count:
                cM[1] = GameCanvas.menu_count - 1
            GameCanvas.redraw = 1
            return
        if v == 25:
            cM[2] = cM[2] + 5
            cM[1] = cM[1] + 5
            if cM[2] > 20:
                cM[2] = 0
                cM[1] = imod(cM[1], 5)
            GameCanvas.redraw = 1

    def key_fire(self):  # e.java:688-1000  (FIRE)
        cM = GameCanvas.menu
        if cM[0] == 9:
            self.change_option(1)
            GameCanvas.redraw = 1
            return
        if cM[0] == 5:
            v = cM[1]
            if v == 4:
                GameCanvas.help_topic = 0
            elif v == 5:
                GameCanvas.redraw = 1
                GameCanvas.menu_return = cM[0]
                cM[0] = 28
                cM[1] = 0
                cM[2] = 0
                GameCanvas.menu_items = GameCanvas.help_items
                GameCanvas.menu_before_talk = i16(GameCanvas.menu_return)
                GameCanvas.help_topic = 8
                return
            elif v == 6:
                GameCanvas.popups.setup_popup(41)
                return
            elif v == 7:
                GameCanvas.popups.setup_popup(42)
                return
            elif v == 8:
                GameCanvas.popups.setup_popup(28)
                GameCanvas.redraw = 1
                return
            arrayOfInt = [0, 1, 3, 4, 5]
            cM[1] = arrayOfInt[cM[1]]
        if Menus.menu_link(cM[0], cM[1] % 7) > -1:
            self.enter_submenu()
            GameCanvas.menu_count = consts.v[cM[0]]
            c0 = cM[0]
            if c0 == 7:
                GameCanvas.hero.name = ""
            elif c0 == 9:
                GameCanvas.stop_sound()
            elif c0 == 10:
                GameCanvas.menu_items = GameCanvas.yes_no_items
            elif c0 == 12:
                GameCanvas.menu_items = GameCanvas.ok_items
            elif c0 == 13:
                GameCanvas.menu_items = GameCanvas.continue_items
            elif c0 == 27:
                GameCanvas.menu_items = GameCanvas.help_items
                GameCanvas.menu_before_talk = i16(GameCanvas.menu_return)
            elif c0 == 28:
                GameCanvas.help_topic = i16(cM[1])
                GameCanvas.menu_count = consts.z[GameCanvas.help_topic + 1] - consts.z[GameCanvas.help_topic]
            elif c0 == 14:
                GameCanvas.update_hero_stats()
            elif c0 == 15:
                cM[3] = 1
                GameCanvas.images[37] = self.load_image(GameCanvas.scr_ui.get(44))
                GameCanvas.images[38] = self.load_image(GameCanvas.scr_ui.get(45))
            elif c0 == 17:
                cz = GameCanvas.hero
                if GameCanvas.menu_return == 16 and cz.equipped[cM[2]].id != 0:
                    for b in range(25):
                        if 0 == cz.backpack[b].id:
                            self.swap_items(cz.equipped[cM[2]], cz.backpack[b])
                self.compact_backpack()
            elif c0 in (21, 22, 23, 24):
                self.enter_blacksmith()
            elif c0 == 1:
                Menus.free_carousel()
                self.load_chapter_lords()
            elif c0 == 3:
                GameCanvas.mission = i16(cM[1])
                self.load_mission_text()
            elif c0 == 20:
                self.open_general_talk()
            cM[2] = 0
            cM[1] = 0
            return
        v = cM[0]
        if v == 0:
            if cM[1] == 3:
                if GameCanvas.general_count == 0:
                    GameCanvas.popups.setup_popup(35)
                    return
                if GameCanvas.hero.live_registered != 0 and GameCanvas.general_count != 0:
                    self.enter_submenu()
                    cM[0] = 19
                    GameCanvas.seal = i16(GameCanvas.backpack_slot_of(504))
                    if GameCanvas.seal != 0 and config.ORIG_BUG["B3"]:
                        Menus.seal_list()
                    if GameCanvas.seal != 0:
                        GameCanvas.menu_count = 44
                    else:
                        GameCanvas.menu_count = GameCanvas.general_count
                    Menus.load_general_table()
                    cM[2] = 0
                    cM[1] = 0
                    return
                GameCanvas.popups.setup_popup(35)
                GameCanvas.redraw = 0
                GameCanvas.menu_scroll = 0
                GameCanvas.menu_anim = 0
                return
            if cM[1] == 2:
                GameCanvas.live.open_live()
                GameCanvas.redraw = 0
                GameCanvas.menu_scroll = 0
                GameCanvas.menu_anim = 0
                return
        elif v == 5:
            GameCanvas.redraw = 1
            if cM[1] == 0:
                if GameCanvas.has_save():
                    self.load_game()
                    if GameCanvas.live_saved != 0:
                        return
                    GameCanvas.stop_sound()
                    self.load_menu_frames()
                    self.enter_submenu()
                    GameCanvas.menu_anim = 0
                    GameCanvas.menu_scroll = 0
                    cM[0] = 0
                    GameCanvas.menu_count = consts.v[cM[0]]
                    GameCanvas.menu_items = GameCanvas.game_menu_items
                    cM[2] = 0
                    cM[1] = 0
                    self.load_hero_images()
                    if GameCanvas.save_flag != 0:  # e.java:856-866  (the save was made on the map: back into it)
                        self.load_chapter_lords()
                        self.load_lord_missions()
                        self.load_mission_text()
                        self.enter_map()
                        self.load_game()
                        GameCanvas.clock[1] = GameCanvas.now()
                        GameCanvas.clock[0] = GameCanvas.now()
                        GameCanvas.play_time = GameCanvas.clock[0] - GameCanvas.play_time
                        self.play_sound(-1)
                        return
                return
            if cM[1] == 1:
                GameCanvas.name_buf = None
                GameCanvas.name_buf = NameBuffer("", 8, 10)
                if GameCanvas.has_save():
                    GameCanvas.popups.setup_popup(3)
                    return
                self.start_new_game()
                return
        elif v in (8, 14):
            if GameCanvas.hero.stat_points > 0:
                GameCanvas.menu_part = 1
                GameCanvas.hero.stat_points -= 1
                if cM[1] == 0:
                    GameCanvas.hero.base_hp += 5
                elif cM[1] == 1:
                    GameCanvas.hero.base_mp += 3
                elif cM[1] == 2:
                    GameCanvas.hero.base_attack += 1
                elif cM[1] == 3:
                    GameCanvas.hero.base_defense += 1
                if cM[0] == 8 and GameCanvas.hero.stat_points == 0:
                    GameCanvas.popups.setup_popup(4)
                    GameCanvas.redraw = 1
                    return
        elif v == 29:
            GameCanvas.popups.setup_popup(36)
        elif v == 10:
            if cM[1] == 2:
                GameCanvas.popups.setup_popup(5)
                return
        elif v == 11:
            if cM[1] == 0:
                if self.save_game() != 0:
                    GameCanvas.popups.setup_popup(0)
            return
        elif v == 25:
            if (GameCanvas.score & 1 << cM[1]) != 0:
                self.enter_submenu()
                self.start_story(cM[1], 0)
                return
            GameCanvas.popups.show_text("3You must first complete|the missions needed|to view this ending.")
            return
        elif v == 15:
            cz = GameCanvas.hero
            if cM[3] == 1:
                if cz.hotkeys[cM[1]] != 0:
                    cM[2] = consts.aD[cz.hotkeys[cM[1]] - 12]
                    cz.hotkeys[cM[1]] = 0
                elif cM[1] < 4:
                    cM[2] = 0
                else:
                    cM[2] = 18
                cM[3] = 2
                if cM[2] < 18:
                    GameCanvas.menu_part = 6
                    return
                GameCanvas.redraw = 1
                return
            if consts.aC[cM[2]] != 0:
                if cz.skill_levels[consts.aC[cM[2]] - 12] != 0:
                    cz.hotkeys[cM[1]] = consts.aC[cM[2]]
                    cM[3] = 1
                GameCanvas.menu_part = 6
                return
        elif v == 17:
            cz = GameCanvas.hero
            it = cz.backpack[cM[2]]
            if it.id != 0:
                b = GameCanvas.item_slot_type(it.id)
                if GameCanvas.set_item_name(it.id) <= cz.level:
                    if it.id == 434:
                        it.id = 0
                        cz.base_hp += 5
                        GameCanvas.popups.setup_popup(23)
                    elif it.id == 435:
                        it.id = 0
                        cz.base_mp += 3
                        GameCanvas.popups.setup_popup(24)
                    elif it.id == 436:
                        it.id = 0
                        cz.base_defense += 1
                        GameCanvas.popups.setup_popup(25)
                    elif it.id == 437:
                        it.id = 0
                        cz.base_attack += 1
                        GameCanvas.popups.setup_popup(26)
                    elif it.id in (502, 504):
                        GameCanvas.popups.setup_popup(17)
                    else:
                        self.swap_items(it, cz.equipped[consts.aE[b]])
                else:
                    GameCanvas.popups.setup_popup(17)
            GameCanvas.menu_part = 1
            return
        elif v == 1:
            if (GameCanvas.missions_done & 1 << GameCanvas.lord_ids[cM[1]] - 1) != 0:
                self.enter_submenu()
                cM[0] = 2
                GameCanvas.menu_count = consts.v[cM[0]]
                GameCanvas.lord = i16(i8(cM[1]))
                self.load_lord_missions()
                cM[2] = 0
                cM[1] = 0
                return
        elif v == 3:
            GameCanvas.popups.setup_popup(6)
            return

    def key_back(self):  # e.java:1002-1109  (BACK)
        cM = GameCanvas.menu
        bool_ = False
        if consts.u[cM[0]] > -1:
            if cM[0] in (14, 15, 16, 17, 18):
                self.save_game()
            if consts.u[cM[0]] > 99:
                GameCanvas.help_topic = 0
                if cM[0] == 28 and GameCanvas.menu_return == 5:
                    GameCanvas.help_topic = 7
                    bool_ = True
                cM[0] = GameCanvas.menu_return
                if cM[0] == 0:
                    GameCanvas.menu_anim = 0
                    GameCanvas.menu_scroll = 0
                GameCanvas.restore_menu_cursor()
                GameCanvas.set_menu_items()
                if bool_:
                    cM[1] = 5
                    return
            else:
                if cM[0] == 1:
                    self.load_menu_frames()
                cM[0] = consts.u[cM[0]]
                if cM[0] == 0:
                    GameCanvas.menu_anim = 0
                    GameCanvas.menu_scroll = 0
                GameCanvas.restore_menu_cursor()
                GameCanvas.set_menu_items()
                if GameCanvas.menu_return == 5:
                    if cM[1] == 3:
                        cM[1] = 2
                    elif cM[1] == 4:
                        cM[1] = 3
                        if GameCanvas.prev_state == 3:  # e.java:1048-1056  (back to the map's pause menu)
                            GameCanvas.state = GameCanvas.prev_state
                            GameCanvas.prev_state = -1
                            cM[0] = 10
                            cM[1] = 4
                            GameCanvas.menu_count = 7
                            GameCanvas.menu_items = GameCanvas.pause_items
                            return
                    elif cM[1] == 5:
                        cM[1] = 4
                if GameCanvas.menu_return == 25:
                    cM[1] = 4
                if GameCanvas.menu_return == 27:
                    cM[1] = 3
                    if GameCanvas.prev_state == 3:  # e.java:1066-1074
                        GameCanvas.state = GameCanvas.prev_state
                        GameCanvas.prev_state = -1
                        cM[0] = 10
                        cM[1] = 4
                        GameCanvas.menu_count = 7
                        GameCanvas.menu_items = GameCanvas.pause_items
                        return
        else:
            v = cM[0]
            if v == 0:
                GameCanvas.free_hero_images()
                Menus.free_carousel()
                self.free_menu_images()
                cM[0] = 5
                GameCanvas.menu_count = 10
                cM[2] = 0
                cM[1] = 0
                GameCanvas.popups.kind = 0
                GameCanvas.redraw = 1
                return
            if v == 15:
                if cM[3] == 1:
                    cM[0] = 13
                    GameCanvas.restore_menu_cursor()
                    GameCanvas.images[37] = None
                    GameCanvas.images[38] = None
                    self.save_game()
                    return
                cM[3] = 1
                GameCanvas.menu_part = 6
                return
            if v == 27:
                cM[0] = GameCanvas.menu_before_talk
                GameCanvas.restore_menu_cursor()
                GameCanvas.set_menu_items()

    @staticmethod
    def free_carousel():  # e.java:1111-1118
        GameCanvas.anim_step = 0
        while GameCanvas.anim_step < 4:
            GameCanvas.images[26 + GameCanvas.anim_step] = None
            GameCanvas.anim_step += 1
        GameCanvas.carousel_image = None

    def enter_submenu(self):  # e.java:1120-1127  (remember cursor, go to the sub-menu)
        cM = GameCanvas.menu
        GameCanvas.menu_return = cM[0]
        GameCanvas.menu_cursors[cM[0]] = i16(cM[1])
        GameCanvas.menu_tops[cM[0]] = i16(cM[2])
        cM[0] = Menus.menu_link(cM[0], cM[1] % 7)
        GameCanvas.redraw = 1
        GameCanvas.menu_part = 0

    def free_shop_images(self):  # e.java:1129-1139
        GameCanvas.images[17] = None
        GameCanvas.images[10] = None
        GameCanvas.gear_data = None
        GameCanvas.rare_data = None
        GameCanvas.treasure_data = None
        for b in range(1, 4):
            GameCanvas.images[0 + b] = None
        GameCanvas.sparkle = None
        Menus.free_carousel()

    def draw_menu_frame(self):  # e.java:1141-1143  (menu background ct[7])
        self.draw_view_region(GameCanvas.images[7], 0, 0, GameCanvas.canvas_size.x, GameCanvas.canvas_size.y, 0, 0)

    def draw_list_menu(self):  # e.java:1145-1227  (vertical list menu: 1 2 10 11 12 13 25 27)
        cM = GameCanvas.menu
        i = GameCanvas.view_cx - 90
        arrayOfByte = [13, 34, 20, 0, 0, 0, 0, 0, 0, 0,
                       12, 18, 12, 13, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 13, 0, 0]
        b2 = 5 if GameCanvas.menu_count > 5 else GameCanvas.menu_count
        if cM[0] == 25 and cM[2] >= 20:
            b2 = 4
            if cM[1] >= 24:
                cM[1] = 23
        j_ = GameCanvas.view_cy - idiv(b2 * 30 - 10, 2)
        if GameCanvas.state == 3 or GameCanvas.prev_state == 3:
            j_ -= 30
        k = j_
        b = arrayOfByte[cM[0]]
        for b1 in range(b2):
            if cM[1] - cM[2] == b1:
                bool_ = True
                Gfx.set_font(GameCanvas.font_orange)
            else:
                bool_ = False
                Gfx.set_font(GameCanvas.font_white)
            m = i
            self.draw_box(m, j_ + GameCanvas.view_y, 180, 20, bool_)
            if GameCanvas.state == 2:
                if cM[0] == 0:
                    if cM[2] + b1 == 3 and (0 == GameCanvas.hero.live_registered or GameCanvas.general_count == 0):
                        Gfx.set_font(GameCanvas.font_gray)
                elif cM[0] == 1:
                    if GameCanvas.debug_keys:
                        GameCanvas.missions_done = -1
                    if 0 == (GameCanvas.missions_done & 1 << GameCanvas.lord_ids[cM[2] + b1] - 1):
                        Gfx.set_font(GameCanvas.font_gray)
                elif cM[0] == 25:
                    if 0 == (GameCanvas.score & 1 << cM[2] + b1):
                        Gfx.set_font(GameCanvas.font_gray)
            else:
                if GameCanvas.map_mode.mode == 1:
                    if cM[2] + b1 == 2 and (GameCanvas.actor_count > 0 or GameCanvas.boss_fight != 0 or GameCanvas.waves[0] != 0):
                        Gfx.set_font(GameCanvas.font_gray)
            if cM[0] == 25:
                if cM[2] + b1 < 24:
                    arrayOfByte1 = self.edat_bytes(54, 38 + cM[2] + b1)
                    str_ = GameCanvas.read_utf(arrayOfByte1, 0, len(arrayOfByte1))
                    self.draw_text_at(str_, j_ - 1, 18)
            elif cM[0] in (0, 10, 12, 13, 27):
                self.draw_text_at(GameCanvas.split_field(GameCanvas.menu_items[0], b1 + cM[2]), j_ - 1, 0)
            else:
                self.draw_text_at(GameCanvas.menu_items[b1 + cM[2]], j_ - 1, b)
            j_ += 30
        if cM[0] == 25:
            self.draw_page_number(cM[2] // 5 + 1, 5, GameCanvas.canvas_size.y - 35, True)
        elif cM[2] != 0 or cM[2] + 5 < GameCanvas.menu_count - 1:
            self.draw_arrow(2, GameCanvas.view_cx - 8 - GameCanvas.view_x, k - 10 - 5)
            self.draw_arrow(3, GameCanvas.view_cx - 8 - GameCanvas.view_x, j_ - 5)
        if cM[0] == 10:
            Gfx.draw_image_anchored(GameCanvas.softkey_bg, 120, GameCanvas.view_y + 15, 17)
            Gfx.set_font(GameCanvas.font_white)
            self.draw_text_at("PAUSE", 13, 0)
        if GameCanvas.debug_keys and cM[0] == 1:
            Gfx.set_font(GameCanvas.font_white)
            Gfx.fill_rect(GameCanvas.screen_w // 2 - 16, GameCanvas.screen_h - 17, 32, 17, 0)
            Gfx.draw_string("" + str(GameCanvas.chapter + 1), GameCanvas.screen_w // 2, GameCanvas.screen_h - 16, 1)

    def draw_options(self):  # e.java:1471-1521  (Options: Sound / Volume / Speed)
        i = GameCanvas.view_cy - 50
        if GameCanvas.menu[1] == 0:
            GameCanvas.menu[1] = 1
        for b in range(1, 3):
            if GameCanvas.menu[1] == b:
                bool_ = True
                Gfx.set_font(GameCanvas.font_orange)
            elif b == 3:
                bool_ = False
                Gfx.set_font(GameCanvas.font_gray)
            else:
                bool_ = False
                Gfx.set_font(GameCanvas.font_white)
            self.draw_box(GameCanvas.view_cx - 100, i + GameCanvas.view_y, 80, 20, bool_)
            self.draw_box(GameCanvas.view_cx - 10, i + GameCanvas.view_y, 110, 20, bool_)
            GameCanvas.draw_view_text_centred(GameCanvas.option_names[b], GameCanvas.view_cx - 100 + 40 - GameCanvas.view_x, i + 1)
            if bool_:
                self.draw_arrow(0, GameCanvas.view_cx - 10 - GameCanvas.view_x, i + 2)
                self.draw_arrow(1, GameCanvas.view_cx - 10 + 110 - 10 - 1 - GameCanvas.view_x, i + 2)
            if b == 0:
                str_ = GameCanvas.on_off[1 if GameCanvas.sound_on else 0]
            elif b == 1:
                str_ = ""
                for b1 in range(GameCanvas.volume // 25):
                    str_ = str_ + 'I'
                if str_ == "":
                    str_ = "OFF"
            elif b == 2:
                str_ = GameCanvas.speed_names[GameCanvas.speed]
            elif b == 3:
                str_ = consts.aX[GameCanvas.difficulty]
            else:
                return
            GameCanvas.draw_view_text_centred(str_, GameCanvas.view_cx + 156 - 111 - GameCanvas.view_x, i + 1)
            i += 10
            i += 20

    def draw_help_page(self):  # e.java:2311-2348  (Help / About page cM[1] of topic ej)
        if GameCanvas.state == 3 or GameCanvas.prev_state == 3:
            GameCanvas.view_cy -= 30
        i = GameCanvas.menu[1] + consts.z[GameCanvas.help_topic]
        arrayOfByte = self.edat_bytes(61, i)
        if GameCanvas.state == 2:
            self.word_wrap(arrayOfByte, 190, 0)
            self.draw_grey_frame(GameCanvas.view_cx - 100 + GameCanvas.view_x, GameCanvas.view_cy - 90 + GameCanvas.view_y, 200, 175)
        else:
            self.word_wrap(arrayOfByte, 190, 0)
            self.draw_grey_frame(GameCanvas.view_cx - 100, GameCanvas.view_cy - 70 + GameCanvas.view_y, 200, 120)
        Gfx.set_font(GameCanvas.font_white)
        for b in range(GameCanvas.text_line_count[0] + 1):
            if GameCanvas.state == 2:
                if GameCanvas.menu[0] == 28 and GameCanvas.help_topic == 8:
                    self.draw_text_at(GameCanvas.text_lines[0][b], GameCanvas.view_cy - 80 + b * 20 + 3, 30)
                    if GameCanvas.menu[1] == 1:
                        self.draw_text_at("v" + GameCanvas.app_version, GameCanvas.view_cy - 80 + 20 + 3, 30)
                else:
                    GameCanvas.draw_view_text(GameCanvas.text_lines[0][b], GameCanvas.view_cx - 95 - 1, GameCanvas.view_cy - 80 + b * 20 + 3)
            else:
                GameCanvas.draw_view_text(GameCanvas.text_lines[0][b], GameCanvas.view_cx - 90 - 1 - GameCanvas.view_x, GameCanvas.view_cy - 62 + b * 15)
        n = consts.z[GameCanvas.help_topic + 1] - consts.z[GameCanvas.help_topic]
        if GameCanvas.state == 2:
            if GameCanvas.prev_state == 3:
                self.draw_page_number(GameCanvas.menu[1] + 1, n, GameCanvas.canvas_size.y - 100, True)
            else:
                self.draw_page_number(GameCanvas.menu[1] + 1, n, GameCanvas.canvas_size.y - 35, True)
        else:
            self.draw_page_number(GameCanvas.menu[1] + 1, n, GameCanvas.view_cy + 65, True)
        if GameCanvas.state == 3 or GameCanvas.prev_state == 3:
            GameCanvas.view_cy += 30

    def draw_page_number(self, paramInt1, paramInt2, paramInt3, paramBoolean):  # e.java:2350-2372  (page "n / m" with arrows)
        if paramInt2 == 1:
            return
        i = GameCanvas.view_cx - 25 - 10
        if paramInt2 > 1:
            if paramInt1 != 1 or paramBoolean:
                self.draw_arrow(0, i, paramInt3)
            i += 60
            if paramInt1 != paramInt2 or paramBoolean:
                self.draw_arrow(1, i, paramInt3)
        paramInt3 += 2
        i = GameCanvas.view_cx - (8 + 9 * ((2 if paramInt2 > 9 else 1) + (2 if paramInt1 > 9 else 1)) + 2) // 2
        i = i + (18 if paramInt1 > 9 else 9)
        self.draw_small_number(paramInt1, i, paramInt3 + GameCanvas.view_y)
        i += 1
        if GameCanvas.prev_state == 3:
            GameCanvas.draw_region(i - GameCanvas.view_x, paramInt3 + 16, 8, 12, GameCanvas.images[20], 90, 0)
        else:
            GameCanvas.draw_region(i - GameCanvas.view_x, paramInt3, 8, 12, GameCanvas.images[20], 90, 0)
        i += 9 + (18 if paramInt2 > 9 else 9)
        self.draw_small_number(paramInt2, i, paramInt3 + GameCanvas.view_y)

    def draw_skills(self, paramInt):  # e.java:1523-1593  (Skills: 5 hot-key slots + skill tree pages)
        cz = GameCanvas.hero
        cM = GameCanvas.menu
        arrayOfByte = [1, 3, 7, 9, 0]
        if 0 == paramInt:
            for b in range(5):
                self.draw_empty_slot(40 + b * 30 + 4 * b, 60)
                self.draw_big_number(arrayOfByte[b], 40 + b * 30 + 18 + 4 * b, 70, 0)
        if paramInt % 2 == 0:
            for b in range(5):
                self.draw_empty_slot(40 + b * 30 + 4 * b, 90)
                if cz.hotkeys[b] != 0:
                    self.draw_map_region(GameCanvas.images[37], 40 + b * 30 + 4 * b + 1, 91, 28, 28, (cz.hotkeys[b] - 12) * 28, 0)
            self.draw_round_outline(40 + cM[1] * 30 + 4 * cM[1], 90, 30, 30, 255, 255, 255)
        arrayOfAc = [Rect(40, 140, 60, 20), Rect(40, 165, 60, 20)]
        if paramInt % 3 == 0:
            i = cM[2] // 6 << 1
            b2 = 2 if cM[2] < 18 else 1
            for b1 in range(b2):
                j_ = cM[2] // 6 * 6 + b1 * 3
                ac1 = arrayOfAc[b1]
                ac1.y = ac1.y + b1 * 10 + 5
                self.draw_round_outline(ac1.x - 1, ac1.y - 1, ac1.w + 2, ac1.h + 2, 152, 152, 152)
                GameCanvas.fill_rect(ac1, 0)
                Gfx.set_font(GameCanvas.font_white)
                GameCanvas.text_width = GameCanvas.measure_text(GameCanvas.skill_names[i + b1])
                GameCanvas.draw_view_text(GameCanvas.skill_names[i + b1], ac1.x + idiv(ac1.w - GameCanvas.text_width, 2), ac1.y + 1)
                for b in range(3):
                    self.draw_empty_slot(40 + (b + 2) * 34, 140 + 35 * b1)
                    if consts.aC[j_ + b] != 0:
                        if cz.skill_levels[consts.aC[j_ + b] - 12] != 0:
                            image = GameCanvas.images[37]
                        else:
                            image = GameCanvas.images[38]
                        self.draw_map_region(image, 40 + (b + 2) * 34 + 1, 140 + 35 * b1 + 1, 28, 28,
                                       (consts.aC[j_ + b] - 12) * 28, 0)
            if cM[3] == 2:
                # DECOMP-FIX F10: `35 * cM[2] % 6 / 3` -> `35 * (cM[2] % 6 / 3)`
                row = 35 * (cM[2] % 6 // 3) if F10 else 35 * cM[2] % 6 // 3
                self.draw_round_outline(40 + (cM[2] % 3 + 2) * 34, 140 + row, 30, 30, 255, 255, 255)
            ac_ = Rect(210, 0, 3, 20)
            self.draw_box(210, 150, 3, 50, False)
            if i == 6:
                ac_.x = 210
                ac_.y = 152
                ac_.w = 3
                ac_.h = 46
                GameCanvas.fill_rect(ac_, GameCanvas.rgb(231, 227, 198))
            else:
                ac_.y = 151 + (i >> 1) * 14 + GameCanvas.view_y
                GameCanvas.fill_rect(ac_, GameCanvas.rgb(231, 227, 198))
        # System.out.println("GameCanvas.DrawSkillSet(2)");
        if cM[3] == 1:
            self.draw_description(cz.hotkeys[cM[1]] + 2000, GameCanvas.view_cx - 100, GameCanvas.canvas_size.y - 70, 200, 22)
        else:
            self.draw_description(consts.aC[cM[2]] + 2000, GameCanvas.view_cx - 100, GameCanvas.canvas_size.y - 70, 200, 22)
        GameCanvas.menu_part = 0

    def draw_description_strip(self):  # e.java:1595-1630  (description strip; scrolls when longer than the box)
        dF = GameCanvas.info_box
        self.draw_box(dF.rect.x + GameCanvas.view_x, dF.rect.y + GameCanvas.view_y, dF.rect.w, dF.rect.h, False)
        Gfx.set_font(GameCanvas.font_white)
        if dF.shown != 0:
            GameCanvas.text_width = GameCanvas.measure_text(dF.text)
            dF.text_x = i16(dF.text_x - 5)
            if dF.rect.x - dF.text_x > GameCanvas.text_width + 3:
                dF.text_x = i16(dF.rect.x + dF.rect.w)
        GameCanvas.draw_view_text(dF.text, dF.text_x, dF.rect.y + (dF.rect.h - 11 >> 1) - 2)
        i = (GameCanvas.screen_w - dF.rect.w) // 2
        j_ = dF.rect.y + GameCanvas.view_y
        s1 = 0
        s2 = 0
        if GameCanvas.state == 3:
            s1 = GameCanvas.view_x
            s2 = GameCanvas.view_y
            Gfx.fill_rect(0, j_, i, dF.rect.h, 0)
            Gfx.fill_rect(GameCanvas.screen_w - i, j_, i, dF.rect.h, 0)
        self.draw_view_region(GameCanvas.images[7], 0, j_, i, dF.rect.h, -s1, j_ - s2)
        Gfx.draw_line(i - 1, j_, i - 1, j_ + dF.rect.h - 1, GameCanvas.rgb(80, 80, 80))
        self.draw_view_region(GameCanvas.images[7], GameCanvas.screen_w - i, j_, i - s1, dF.rect.h, GameCanvas.screen_w - i - s1, j_ - s2)
        Gfx.draw_line(GameCanvas.screen_w - i, j_, GameCanvas.screen_w - i, j_ + dF.rect.h - 1, GameCanvas.rgb(80, 80, 80))
        if GameCanvas.state == 3:
            Gfx.push_clip(0, j_, GameCanvas.screen_w, dF.rect.h)
            GameCanvas.scene.draw_hud_frame()
            Gfx.pop_clip()
            Gfx.push_clip(0, j_, i - 1, dF.rect.h)
            GameCanvas.popups.draw_popup_frame(170)
            Gfx.pop_clip()
            Gfx.push_clip(GameCanvas.screen_w - i + 1, j_, i - 1, dF.rect.h)
            GameCanvas.popups.draw_popup_frame(170)
            Gfx.pop_clip()

    def draw_gear(self, paramInt1, paramInt2):  # e.java:1632-1654  (Gear: hero sprite + 9 equipment slots)
        cz = GameCanvas.hero
        arrayOfByte1 = [-77, -77, -77, -33, 3, 47, 47, 47, -15]
        arrayOfByte2 = [21, -15, -51, -79, -79, -51, -15, 21, 49]
        GameCanvas.images[39] = self.load_image(GameCanvas.scr_ui.get(50))
        ct39 = GameCanvas.images[39]
        self.draw_map_region(ct39, GameCanvas.view_cx - ct39.getWidth() // 2, GameCanvas.view_cy - ct39.getHeight() // 2,
                       ct39.getWidth(), ct39.getHeight(), 0, 0)
        GameCanvas.images[39] = None
        for b in range(9):
            if cz.equipped[b].id != 0:
                self.load_item_def(cz.equipped[b].id)
                self.draw_item_icon(cz.equipped[b].id, GameCanvas.view_cx + arrayOfByte1[b], GameCanvas.view_cy + arrayOfByte2[b], 0)
        self.draw_round_outline(GameCanvas.view_cx + arrayOfByte1[paramInt1] - 1, GameCanvas.view_cy + arrayOfByte2[paramInt1] - 1, 30, 30, 255, 255, 255)
        GameCanvas.cursor[24] = GameCanvas.view_cx + arrayOfByte1[paramInt1] + GameCanvas.view_x + 7
        GameCanvas.cursor[25] = GameCanvas.view_cy + arrayOfByte2[paramInt1] + GameCanvas.view_y + 7
        f1 = cz.body_frames[1]
        self.draw_map_region(cz.body_image, GameCanvas.view_cx - f1.ox, GameCanvas.view_cy + 7 - f1.oy + 17, f1.w, f1.h, f1.src_x, f1.src_y)
        f2 = cz.head_frames[1]
        self.draw_map_region(cz.head_image, GameCanvas.view_cx - f2.ox, GameCanvas.view_cy + 7 - f2.oy + 17, f2.w, f2.h, f2.src_x, f2.src_y)
        if paramInt2 != 0:
            GameCanvas.describe_shop_item(self.item_under_cursor(-1), True, -1)
            return
        self.draw_description(paramInt1 + 1000, GameCanvas.view_cx - 79, GameCanvas.view_cy + 81 + 5, 158, 20)

    def draw_inventory(self, paramInt):  # e.java:1656-1692  (Inventory: 5x5 grid in 2 pages + gold)
        cz = GameCanvas.hero
        cM = GameCanvas.menu
        arrayOfInt1 = [GameCanvas.view_cx - 75, GameCanvas.view_cx - 45, GameCanvas.view_cx - 15, GameCanvas.view_cx + 15, GameCanvas.view_cx + 45]
        arrayOfInt2 = [GameCanvas.view_cy - 45, GameCanvas.view_cy - 15, GameCanvas.view_cy + 15]
        ac_ = Rect(GameCanvas.view_cx + 80, GameCanvas.view_cy - 40, 5, 80)
        if cM[2] < 15:
            b2 = 3
            b3 = 0
        else:
            b2 = 2
            b3 = 15
        if paramInt != 0:
            self.draw_map_region(GameCanvas.images[7], GameCanvas.view_cx - 75, GameCanvas.view_cy - 45, 150, 100, GameCanvas.view_cx - 75, GameCanvas.view_cy - 45)
        for b1 in range(b2):
            for b in range(5):
                self.draw_empty_slot(arrayOfInt1[b] + GameCanvas.view_x, arrayOfInt2[b1] + GameCanvas.view_y)
                self.load_item_def(cz.backpack[b3 + b1 * 5 + b].id)
                self.draw_item_icon(cz.backpack[b3 + b1 * 5 + b].id, arrayOfInt1[b] + 1, arrayOfInt2[b1] + 1, 0)
        GameCanvas.fill_rect(ac_, GameCanvas.rgb(148, 148, 148))
        ac_.x += 1
        ac_.y += 1
        ac_.w -= 2
        ac_.h -= 2
        GameCanvas.fill_rect(ac_, GameCanvas.rgb(33, 0, 0))
        ac_.y = GameCanvas.view_cy - 39 + (39 if b3 != 0 else 0) + GameCanvas.view_y
        ac_.h = 39
        GameCanvas.fill_rect(ac_, GameCanvas.rgb(231, 227, 198))
        self.draw_description(cM[2] + 1100, GameCanvas.view_cx - 75, GameCanvas.view_cy + 50, 150, 22)
        self.draw_round_outline(arrayOfInt1[cM[2] % 5], arrayOfInt2[(cM[2] - b3) // 5] + GameCanvas.view_y, 30, 30, 255, 255, 255)
        if 0 == paramInt:
            self.draw_gold_box()
        GameCanvas.menu_part = 0

    def draw_assign_items(self, paramInt):  # e.java:3022-3058  (Assign Items: 5 potion slots, * and # quick keys)
        cz = GameCanvas.hero
        if GameCanvas.state == 3:
            GameCanvas.view_cy -= 30
        if 0 == paramInt:
            self.draw_gold_box()
            Gfx.set_font(GameCanvas.font_white)
            for b1 in range(5):
                self.draw_box(GameCanvas.view_cx - 80 + 32 * b1, GameCanvas.view_cy - 40 + GameCanvas.view_y, 30, 22, False)
                if cz.quick_keys[0] == b1:
                    GameCanvas.draw_view_text(" * ", GameCanvas.view_cx - 80 + 32 * b1 - GameCanvas.view_x, GameCanvas.view_cy - 38)
                elif cz.quick_keys[1] == b1:
                    GameCanvas.draw_view_text(" # ", GameCanvas.view_cx - 80 + 32 * b1 - GameCanvas.view_x, GameCanvas.view_cy - 38)
        for b in range(5):
            if GameCanvas.state == 3:
                self.draw_box(GameCanvas.view_cx - 79 + 32 * b, GameCanvas.view_cy + 6, 28, 28, False)
                self.draw_item_icon(cz.quick_slots[b].item, GameCanvas.view_cx - 79 + 32 * b - GameCanvas.view_x, GameCanvas.view_cy + 6 - GameCanvas.view_y, b)
            else:
                self.draw_box(GameCanvas.view_cx - 79 + 32 * b, GameCanvas.view_cy - 10, 28, 28, False)
                self.draw_item_icon(cz.quick_slots[b].item, GameCanvas.view_cx - 79 + 32 * b - GameCanvas.view_x, GameCanvas.view_cy - 10 - GameCanvas.view_y, b)
        if GameCanvas.state == 3:
            self.draw_round_outline(GameCanvas.view_cx - 80 + 32 * GameCanvas.menu[1], GameCanvas.view_cy + 6, 30, 29, 255, 255, 255)
        else:
            self.draw_round_outline(GameCanvas.view_cx - 80 + 32 * GameCanvas.menu[1], GameCanvas.view_cy - 10, 30, 29, 255, 255, 255)
        GameCanvas.menu_part = 0
        self.draw_description(GameCanvas.menu[1] + 1200, GameCanvas.view_cx - 80 - GameCanvas.view_x, GameCanvas.view_cy + 30, 160, 22)
        self.draw_box(GameCanvas.view_cx - 80, GameCanvas.view_cy + 60 + GameCanvas.view_y, 160, 22, False)
        Gfx.set_font(GameCanvas.font_white)
        self.draw_text_at("*,# key Assign", GameCanvas.view_cy + 60, 15)
        if GameCanvas.state == 3:
            GameCanvas.view_cy += 30

    def draw_item_icon(self, paramInt1, paramInt2, paramInt3, paramInt4):  # e.java:3060-3081  (item icon)
        i = -1
        b = 0
        if paramInt1 > 500:
            i = paramInt1 - 501
            b = 3
        elif paramInt1 > 300:
            i = GameCanvas.treasure_def.icon
            b = 2
        elif paramInt1 > 100:
            i = GameCanvas.gear_def.icon
            b = 1
        elif paramInt1 > 0:
            i = paramInt1 - 1
            b = 0
        if i > -1:
            self.draw_map_region(GameCanvas.images[0 + b], paramInt2, paramInt3, 28, 28, i * 28, 0)
            if paramInt1 < 100:
                self.draw_small_digit(paramInt2, paramInt3 + 2, GameCanvas.hero.quick_slots[paramInt4].count)

    # ---- Blacksmith (screens 21 Buy, 22 Sell, 23 Enchant, 24 Combine) ----------------------
    # fK[0] = mode (cM[0]-21), fK[9]/fK[10] = cursor col/row, fK[18] = cell, fK[19] = item id,
    # fK[20] = message for aV(), fK[21] = price, fK[26] = sparkle frame (-1 idle), fK[27] = 1 on Gear

    def draw_item_grid(self, paramInt, paramArrayOfz, paramArrayOfint):  # e.java:1804-1861  (item grid)
        i = GameCanvas.cursor[8] * 5
        if GameCanvas.cursor[11] == 1:
            ac1 = Rect(0, 0, 0, 0)
            ac2 = Rect(0, 0, 0, 0)
            ac1.w = 4
            ac1.x = GameCanvas.cursor[12]
            ac1.h = GameCanvas.cursor[6]
            ac1.y = paramInt
            GameCanvas.draw_filled_rect(ac1, 16777215, 0)
            ac1.w -= 2
            ac1.x += 1
            ac1.h -= 2
            ac1.y += 1
            j_ = GameCanvas.cursor[8] * 32
            k = ac2.h
            j_ = idiv(j_ * k, GameCanvas.cursor[7])
            ac2.h = GameCanvas.cursor[13]
            ac2.y += j_
            GameCanvas.fill_rect(ac2, 16777215)
            GameCanvas.outline_rect(ac1, 10000536)
        paramInt += 1
        b1 = 0
        b2 = 0
        while b1 < GameCanvas.cursor[3]:
            j_ = GameCanvas.cursor[5]
            for b in range(5):
                if i == GameCanvas.cursor[18]:
                    bool_ = True
                    GameCanvas.cursor[24] = j_ + 13 + 1
                    GameCanvas.cursor[25] = paramInt + 13 + 1
                else:
                    bool_ = False
                for b3 in range(GameCanvas.combine_slots[3]):
                    if GameCanvas.combine_slots[b3] == i:
                        bool_ = True
                        GameCanvas.combine_pos[b2].x = i16(j_ + 13 + 1)
                        GameCanvas.combine_pos[b2].y = i16(paramInt + 13 + 1)
                        b2 += 1
                        break
                self.draw_grid_cell(j_, paramInt, bool_)
                if paramArrayOfint is not None:
                    self.draw_item_count_icon(paramArrayOfint[i], j_, paramInt, 0)
                else:
                    self.draw_grid_item(i, j_, paramInt, paramArrayOfz)
                j_ += 32
                i += 1
            paramInt += 32
            b1 += 1

    def draw_grid_item(self, paramInt1, paramInt2, paramInt3, paramArrayOfz):  # e.java:1863-1877
        if paramArrayOfz is not None:
            z1 = paramArrayOfz[paramInt1]
        else:
            z1 = self.item_under_cursor(paramInt1)
        if GameCanvas.cursor[0] == 1 and 0 < z1.id < 100:
            bool_ = z1.attack
        else:
            bool_ = 0
        self.draw_item_count_icon(z1.id, paramInt2, paramInt3, bool_)

    def draw_grid_cell(self, paramInt1, paramInt2, paramBoolean):  # e.java:1879-1881  (grid cell frame)
        GameCanvas.draw_frame_box(paramInt1 + 1, paramInt2 + 1, 26, 26, 0, 0, 16777215 if paramBoolean else 5263440, True)

    def draw_item_count_icon(self, paramInt1, paramInt2, paramInt3, paramInt4):  # e.java:1883-1902  (item icon by id + count)
        if paramInt1 > 500:
            image = GameCanvas.images[3]
            i = paramInt1 - 501
        elif paramInt1 > 300:
            image = GameCanvas.images[2]
            i = GameCanvas.item_tables[1].get_int(paramInt1 - 301, 7)
        elif paramInt1 > 100:
            image = GameCanvas.images[1]
            i = GameCanvas.item_tables[0].get_int(paramInt1 - 101, 7)
        else:
            image = GameCanvas.images[0]
            i = paramInt1 - 1
        GameCanvas.draw_region(paramInt2, paramInt3, 28, 28, image, i * 28, 0)
        if paramInt4 > 0:
            GameCanvas.draw_region(paramInt2, paramInt3, 9, 12, GameCanvas.images[20], paramInt4 * 9, 0)

    def draw_shop_grid(self):  # e.java:1904-1910  (gold + item grid + description)
        i = GameCanvas.cursor[1] + 1
        self.draw_hero_gold(i)
        i += 29
        self.draw_item_grid(i, None, None)
        GameCanvas.describe_shop_item(self.item_under_cursor(-1), True, -1)

    def draw_blacksmith(self, paramBoolean):  # e.java:1912-2111  (decompiler gave bytecode only; rebuilt from it)
        fK = GameCanvas.cursor
        if paramBoolean:
            if fK[27] == 0:
                self.draw_shop_grid()
            else:
                self.draw_gear(fK[18], 1)
            if fK[23] == -1 and GameCanvas.popups.kind == 0:
                # the Yes/No popup of Enchant / Combine has just closed
                fK[23] = 0
                if GameCanvas.key == -5 and GameCanvas.popups.button == 0:
                    if fK[21] > GameCanvas.hero.gold:
                        fK[20] = 4
                        Menus.blacksmith_message()
                        Menus.clear_combine()
                    else:
                        fK[26] = 0          # start the sparkle, the action follows below
                else:
                    Menus.clear_combine()
        if fK[26] == -1:
            return
        if fK[26] < 5:
            self.draw_sparkles()
            fK[26] += 1
            return
        fK[26] = -1
        GameCanvas.redraw = 1
        if fK[0] == 2:
            self.roll_enchant()
        elif fK[0] == 3:
            cz = GameCanvas.hero
            if fK[22] == 0:
                for b in range(3):
                    Item.clear(cz.backpack[GameCanvas.combine_slots[b]])
                dst = cz.backpack[GameCanvas.combine_slots[2]]
                dst.id = GameCanvas.combine_result.id
                dst.attack = GameCanvas.combine_result.attack
                dst.defense = GameCanvas.combine_result.defense
                dst.hp = GameCanvas.combine_result.hp
                dst.mp = GameCanvas.combine_result.mp
                dst.enchant = GameCanvas.combine_result.enchant
            elif fK[31] != -1:
                Item.clear(cz.backpack[fK[31]])
                fK[31] = -1
            Menus.clear_combine()
            fK[20] = 9
            cz.gold -= fK[21]
        self.save_game()
        Menus.blacksmith_message()

    def roll_enchant(self):  # e.java:2113-2135  (Enchant: roll success / fail / lost)
        arrayOfByte1 = [100, 90, 80, 70, 60, 45, 30, 10, 1]
        arrayOfByte2 = [0, 10, 20, 40, 50, 60, 70, 80, 90]
        z_ = self.item_under_cursor(-1)
        GameCanvas.cursor[20] = 2
        GameCanvas.hero.gold -= GameCanvas.cursor[21]
        if GameCanvas.cursor[22] == -1:
            GameCanvas.cursor[23] = 2
        else:
            i = self.rand(100) + 1
            if i > arrayOfByte1[z_.enchant]:
                i = self.rand(100)
                GameCanvas.cursor[23] = 2 if i <= arrayOfByte2[z_.enchant] else 1
            else:
                self.enchant_item(z_, 1)
                GameCanvas.cursor[23] = 0
        if GameCanvas.cursor[23] == 2:
            Item.clear(z_)
            GameCanvas.cursor[23] = 1

    def draw_sparkle(self, paramInt1, paramInt2):  # e.java:2137-2144  (sparkle frame)
        arrayOfByte1 = [0, 15, 30, 0, 20]
        arrayOfByte2 = [0, 0, 0, 16, 16]
        arrayOfByte3 = [16, 16, 16, 20, 24]
        n = arrayOfByte3[GameCanvas.cursor[26]]
        paramInt1 -= n >> 1
        paramInt2 -= n >> 1
        GameCanvas.draw_region(paramInt1, paramInt2, n, n, GameCanvas.sparkle, arrayOfByte1[GameCanvas.cursor[26]], arrayOfByte2[GameCanvas.cursor[26]])

    def draw_sparkles(self):  # e.java:2146-2156
        if GameCanvas.cursor[0] == 2:
            self.draw_sparkle(GameCanvas.cursor[24], GameCanvas.cursor[25])
            return
        if GameCanvas.cursor[0] == 3:
            for b in range(3):
                if GameCanvas.combine_pos[b].x > 0 and GameCanvas.combine_pos[b].y > 0:
                    self.draw_sparkle(GameCanvas.combine_pos[b].x, GameCanvas.combine_pos[b].y)

    @staticmethod
    def blacksmith_message():  # e.java:2396-2451  (Blacksmith message popup)
        from pow.game.popups import Popups
        arrayOfString = ["Success", "Fail"]
        str_ = ""
        GameCanvas.popups.reset()
        GameCanvas.redraw = 1
        fK = GameCanvas.cursor
        v = fK[20]
        if v == 0:
            if fK[19] < 1:
                return
            str_ = Popups.show_bought()
        elif v == 11:
            str_ = Popups.show_sold()
        elif v == 1:
            if fK[22] == 0:
                str_ = "1Not possible |to enchant."
            else:
                str_ = "2Price is " + str(fK[21]) + ".If |enchanting fails,|Items can be lost.|Continue?"
                GameCanvas.popups.timer = 200
        elif v == 2:
            if fK[23] != 0:
                fK[23] = 1
            str_ = "1Enchant|" + arrayOfString[fK[23]]
        elif v == 3:
            str_ = "1Fully enchanted.|Not possible|to enchant."
        elif v == 4:
            str_ = "1Not enough Gold"
        elif v == 5:
            str_ = "1You cannot|buy anymore."
        elif v == 6:
            str_ = "3Your backpack|is full. Please|empty some items|and try again."
        elif v == 7:
            str_ = "3Please select|3 items to|combine into one."
        elif v == 8:
            if fK[22] == 2:
                str_ = "1Not possible."
            else:
                str_ = ("2Compounding fee|is " + str(fK[21]) + ".|Selected items|could be lost|"
                        "when it fails.|Continue?")
                GameCanvas.popups.timer = 200
        elif v == 9:
            str_ = "1Compounding| " + arrayOfString[fK[22]]
        GameCanvas.popups.show_text(str_)

    def blacksmith_keys(self):  # e.java:2453-2566  (Blacksmith keys)
        fK = GameCanvas.cursor
        bool_ = True
        if fK[26] != -1:
            return
        ch = GameCanvas.key
        if ch in (-1, 50):
            if fK[27] == 0:
                fK[10] = fK[10] - 1
            else:
                fK[18] = fK[18] + 1
                if _inc_cmp(fK[18]) > 8:
                    fK[18] = 0
            GameCanvas.info_box.text = ""
        elif ch in (-2, 56):
            if fK[27] == 0:
                fK[10] = fK[10] + 1
            else:
                fK[18] = fK[18] - 1
                if _dec_cmp(fK[18]) < 0:
                    fK[18] = 8
            GameCanvas.info_box.text = ""
        elif ch in (-3, 52):
            if fK[27] == 0:
                fK[9] = fK[9] - 1
                if _dec_cmp(fK[9]) < 0:
                    fK[9] = 4
                    fK[10] = fK[10] - 1
            else:
                fK[18] = fK[18] + 1
                if _inc_cmp(fK[18]) > 8:
                    fK[18] = 0
            GameCanvas.info_box.text = ""
        elif ch in (-4, 54):
            if fK[27] == 0:
                fK[9] = fK[9] + 1
                if _inc_cmp(fK[9]) >= 5:
                    fK[9] = 0
                    fK[10] = fK[10] + 1
            else:
                fK[18] = fK[18] - 1
                if _dec_cmp(fK[18]) < 0:
                    fK[18] = 8
            GameCanvas.info_box.text = ""
        elif ch == -7:
            cM = GameCanvas.menu
            cM[0] = consts.u[cM[0]]
            GameCanvas.menu_count = consts.v[cM[0]]
            cM[1] = GameCanvas.menu_cursors[cM[0]]
            cM[2] = GameCanvas.menu_tops[cM[0]]
            GameCanvas.redraw = 1
            bool_ = False
            GameCanvas.images[39] = None
            GameCanvas.info_box.text = ""
            Menus.clear_combine()
        elif ch in (-5, 53):
            if fK[0] == 0:
                self.buy_item()
                bool_ = False
                Menus.blacksmith_message()
            elif fK[0] == 1:
                if fK[19] != 0:
                    self.sell_item()
                    Menus.blacksmith_message()
                else:
                    bool_ = False          # falls into `default`
            elif fK[0] == 2:
                self.enchant_price()
                Menus.blacksmith_message()
                bool_ = False              # falls into `default`
            else:
                if fK[0] == 3 and self.item_under_cursor(-1).id > 100:
                    b = 3
                    if GameCanvas.combine_slots[3] > 0:
                        b = 0
                        while b < GameCanvas.combine_slots[3] and GameCanvas.combine_slots[b] != fK[18]:
                            b += 1
                    if b < GameCanvas.combine_slots[3]:
                        while b < 2:
                            GameCanvas.combine_slots[b] = GameCanvas.combine_slots[b + 1]
                            b += 1
                        GameCanvas.combine_slots[3] = GameCanvas.combine_slots[3] - 1
                    else:
                        GameCanvas.combine_slots[GameCanvas.combine_slots[3]] = fK[18]
                        GameCanvas.combine_slots[3] = GameCanvas.combine_slots[3] + 1
                    if GameCanvas.combine_slots[3] == 3:
                        self.combine_result_of()
        else:
            bool_ = False
        if bool_:
            self.update_shop_cursor()
            GameCanvas.menus.draw_blacksmith(True)

    def combine_result_of(self):  # e.java:2568-2626  (Combine: work out the result of 3 items)
        arrayOfInt = [0, 0, 0]
        i = 0
        for b in range(3):
            z_ = self.item_under_cursor(GameCanvas.combine_slots[b])
            b1 = 0
            while b1 < b and arrayOfInt[b1] <= z_.id:
                b1 += 1
            for b2 in range(b, b1, -1):
                arrayOfInt[b2] = arrayOfInt[b2 - 1]
            arrayOfInt[b1] = z_.id
            i += z_.enchant
        Menus.mix_table = ResReader.read("/" + GameCanvas.scr_data.get(68))
        if Menus.mix_table is not None:
            arrayOfInt1 = [0, 149, 298]
            j_ = 0
            k = 149
            b = 0
            while b < 3:
                arrayOfInt2 = self.find_run(arrayOfInt1[b], arrayOfInt[b], j_, k)
                j_ = arrayOfInt2[0]
                k = arrayOfInt2[1]
                if 0 == arrayOfInt2[2]:
                    break
                b += 1
            if b < 3:
                GameCanvas.cursor[22] = 2
                Menus.clear_combine()
            else:
                j_ += self.rand(k)
                arrayOfInt[0] = Menus.mix_entry(447 + j_)
                GameCanvas.combine_result = self.make_item(arrayOfInt[0])
                GameCanvas.cursor[21] = idiv(Menus.item_price(GameCanvas.combine_result), 4)
                if arrayOfInt[0] < 500:
                    arrayOfInt[1] = GameCanvas.item_tables[1].get_int(arrayOfInt[0] - 301, 8)
                    arrayOfInt[2] = 15
                else:
                    arrayOfInt[1] = GameCanvas.item_tables[2].get_int(arrayOfInt[0] - 501, 7)
                    arrayOfInt[2] = 12
                arrayOfInt[1] = idiv(200 - arrayOfInt[1], 12)
                if arrayOfInt[1] >= self.rand(101):
                    GameCanvas.cursor[22] = 0
                    GameCanvas.combine_result = self.enchant_item(GameCanvas.combine_result, idiv(i, 3))
                else:
                    GameCanvas.cursor[22] = 1
                    arrayOfInt[1] = idiv((100 - arrayOfInt[1]) * 10, arrayOfInt[2])
                    GameCanvas.cursor[31] = GameCanvas.combine_slots[self.rand(3)] if arrayOfInt[1] >= self.rand(101) else -1
                GameCanvas.cursor[23] = -1
            GameCanvas.cursor[20] = 8
            Menus.blacksmith_message()
        Menus.mix_table = None

    def enchant_item(self, paramz, paramInt):  # e.java:2628-2668  (enchant paramInt times: raise stats)
        arrayOfByte = [30, 25, 20, 15, 9, 1]
        for b in range(paramInt):
            i = 0
            j_ = self.rand(101)
            b1 = 0
            while b1 < 5:
                i += arrayOfByte[b1]
                if j_ < i:
                    break
                b1 += 1
            j_ = (b1 + 5) * 10
            s = 0
            for b1 in range(4):
                s = (paramz.attack, paramz.defense, paramz.hp, paramz.mp)[b1]
                i = s
                if i > 0:
                    i = idiv(idiv(i * j_, 10) + 50, 100)
                    if i == 0:
                        i = 1
                    if b1 == 0:
                        paramz.attack = i16(paramz.attack + i)
                    elif b1 == 1:
                        paramz.defense = i16(paramz.defense + i)
                    elif b1 == 2:
                        paramz.hp = i16(paramz.hp + i)
                    elif b1 == 3:
                        paramz.mp = i16(paramz.mp + i)
            paramz.enchant = i8(paramz.enchant + 1)
        return paramz

    @staticmethod
    def mix_entry(paramInt):  # e.java:2670-2672
        return Menus.mix_table[paramInt * 2] & 0xFF | (Menus.mix_table[paramInt * 2 + 1] & 0xFF) << 8

    def find_run(self, paramInt1, paramInt2, paramInt3, paramInt4):  # e.java:2674-2692  (find run of paramInt2)
        arrayOfInt = [paramInt3, paramInt4, 0]
        b = 0
        while b < arrayOfInt[1]:
            i = Menus.mix_entry(paramInt1 + arrayOfInt[0])
            if i == paramInt2:
                break
            arrayOfInt[0] = arrayOfInt[0] + 1
            b += 1
        if b < arrayOfInt[1]:
            arrayOfInt[1] = arrayOfInt[1] - b
            b = 0
            i = Menus.mix_entry(paramInt1 + arrayOfInt[0])
            while b < arrayOfInt[1] and i == paramInt2:
                b += 1
                i = Menus.mix_entry(paramInt1 + arrayOfInt[0] + b)
            arrayOfInt[1] = b
            arrayOfInt[2] = 1
            return arrayOfInt
        arrayOfInt[2] = 0
        return arrayOfInt

    def enter_blacksmith(self):  # e.java:2694-2707  (enter a Blacksmith screen)
        if GameCanvas.menu[0] == 24:
            Menus.count_items()
            if GameCanvas.cursor[16] < 3:
                GameCanvas.popups.setup_popup(39)
                GameCanvas.redraw = 1
                GameCanvas.menu[1] = 3
                return True
        GameCanvas.load_item_tables()
        self.blacksmith_layout()
        return True

    def blacksmith_layout(self):  # e.java:2709-2754  (grid layout of the current Blacksmith mode)
        fK = GameCanvas.cursor
        fK[0] = GameCanvas.menu[0] - 21
        if fK[0] == 0 or fK[0] == 1:
            fK[14] = fK[0] + 1
        else:
            fK[14] = 0
        if fK[0] == 3:
            Menus.clear_combine()
            fK[20] = 7
            Menus.blacksmith_message()
        Menus.count_items()
        i = 0
        c = 173                     # '­'
        fK[4] = 5
        if fK[0] == 1:
            fK[4] = fK[4] + 1
        fK[3] = 5
        if fK[3] > 3:
            fK[3] = 3
        if fK[3] < fK[4]:
            fK[11] = 1
        else:
            fK[3] = fK[4]
            fK[11] = 0
        fK[6] = fK[3] * 32 - 2
        i = 72 + fK[6]
        fK[1] = 26 + (243 - i) // 2 + 1
        i = 158
        if fK[11] == 1:
            c = 32
            i = 164
            fK[7] = 32 * fK[4] - 2
            fK[13] = idiv(fK[6] * (fK[6] - 2), fK[7]) + 1
        fK[5] = (240 - i) // 2 + 1
        fK[12] = fK[5] + c
        fK[27] = 0
        fK[8] = 0
        fK[10] = 0
        fK[9] = 0
        self.update_shop_cursor()
        fK[26] = -1

    def update_shop_cursor(self):  # e.java:2756-2772  (clamp cursor, scroll, item under cursor -> fK[19])
        fK = GameCanvas.cursor
        if fK[27] == 0:
            if fK[10] < 0:
                fK[10] = fK[4] - 1
            elif fK[10] >= fK[4]:
                fK[10] = 0
            if fK[10] < fK[8]:
                fK[8] = fK[10]
            elif fK[10] >= fK[8] + fK[3]:
                fK[8] = fK[10] - fK[3] + 1
            fK[18] = fK[10] * 5 + fK[9]
        z_ = self.item_under_cursor(-1)
        fK[19] = z_.id if z_ is not None else 0

    @staticmethod
    def item_name(paramInt):  # e.java:2774-2786  (item name)
        if paramInt < 100:
            return consts.aN[paramInt - 1]
        if paramInt < 300:
            return GameCanvas.item_tables[0].get_string(paramInt - 101, 0)
        if paramInt < 500:
            return GameCanvas.item_tables[1].get_string(paramInt - 301, 0)
        return GameCanvas.item_tables[2].get_string(paramInt - 501, 0)

    @staticmethod
    def clear_combine():  # e.java:2788-2801  (clear the Combine selection)
        for b in range(len(GameCanvas.combine_slots)):
            GameCanvas.combine_slots[b] = 0
        for b in range(len(GameCanvas.combine_pos)):
            if GameCanvas.combine_pos[b] is None:
                GameCanvas.combine_pos[b] = Point()
            GameCanvas.combine_pos[b].x = 0
            GameCanvas.combine_pos[b].y = 0
        if GameCanvas.combine_result is None:
            GameCanvas.combine_result = Item()
        Item.clear(GameCanvas.combine_result)

    @staticmethod
    def count_items():  # e.java:2803-2815  (count items: fK[16] backpack, fK[17] potions)
        GameCanvas.cursor[16] = 0
        for b in range(25):
            if GameCanvas.hero.backpack[b].id > 0:
                GameCanvas.cursor[16] = GameCanvas.cursor[16] + 1
        GameCanvas.cursor[17] = 0
        for b in range(5):
            if GameCanvas.hero.quick_slots[b].item > 0:
                GameCanvas.cursor[17] = GameCanvas.cursor[17] + 1

    @staticmethod
    def item_price(paramz):  # e.java:2817-2830  (price of an item)
        if paramz.id < 100:
            i = consts.y[paramz.id - 1]
        elif paramz.id < 300:
            i = GameCanvas.item_tables[0].get_int(paramz.id - 101, 6)
            i = i + paramz.attack * 100
            i = i + paramz.defense * 100
            i = i + idiv(paramz.hp, 5) * 100
            i = i + idiv(paramz.mp, 3) * 100
        elif paramz.id < 500:
            j_ = 800 if GameCanvas.item_tables[1].get_int(paramz.id - 301, 6) == 0 else 400
            i = paramz.attack * j_
            i = i + paramz.defense * j_
            i = i + idiv(paramz.hp, 5) * j_
            i = i + idiv(paramz.mp, 3) * j_
        else:
            i = GameCanvas.item_tables[2].get_int(paramz.id - 501, 6)
        return i

    def buy_item(self):  # e.java:2832-2883  (Buy)
        cz = GameCanvas.hero
        fK = GameCanvas.cursor
        z_ = GameCanvas.shop[fK[18]]
        if z_.id == 0:
            fK[20] = -1
            return
        i = Menus.item_price(z_)
        if cz.gold >= i:
            if z_.id < 100:
                b = 0
                while b < 5 and cz.quick_slots[b].item != z_.id:
                    b += 1
                if b < 5:
                    if cz.quick_slots[b].count < 5:
                        cz.quick_slots[b].count = i16(cz.quick_slots[b].count + 1)
                        fK[20] = 0
                    else:
                        fK[20] = 5
                else:
                    b = 0
                    while b < 5 and cz.quick_slots[b].item != 0:
                        b += 1
                    if b < 5:
                        cz.quick_slots[b].item = z_.id
                        cz.quick_slots[b].count = 1
                        fK[17] = fK[17] + 1
                        fK[20] = 0
                    else:
                        fK[20] = 6
            elif fK[16] < 25:
                b = 0
                while b < 25 and cz.backpack[b].id != 0:
                    b += 1
                y_ = cz.backpack[b]
                y_.id = z_.id
                y_.attack = z_.attack
                y_.defense = z_.defense
                y_.hp = z_.hp
                y_.mp = z_.mp
                y_.enchant = z_.enchant
                Item.clear(z_)
                fK[16] = fK[16] + 1
                fK[20] = 0
            else:
                fK[20] = 6
        else:
            fK[20] = 4
        if fK[20] == 0:
            cz.gold -= i
            self.save_game()

    def sell_item(self):  # e.java:2885-2905  (Sell, half price)
        cz = GameCanvas.hero
        fK = GameCanvas.cursor
        z_ = self.item_under_cursor(-1)
        if z_ is None or z_.id == 0:
            return
        i = Menus.item_price(z_)
        if z_.id < 100:
            if cz.quick_slots[fK[18]].count > 1:
                cz.quick_slots[fK[18]].count = i16(cz.quick_slots[fK[18]].count - 1)
            else:
                cz.quick_slots[fK[18]].item = 0
                cz.quick_slots[fK[18]].count = 0
                fK[17] = fK[17] - 1
        else:
            Item.clear(z_)
            fK[16] = fK[16] - 1
        fK[20] = 11
        cz.gold += idiv(i, 2)
        self.save_game()

    def enchant_price(self):  # e.java:2907-2936  (Enchant: price and limit)
        fK = GameCanvas.cursor
        z_ = self.item_under_cursor(-1)
        if z_.id == 0:
            fK[20] = -1
            return
        fK[22] = 0
        fK[21] = 0
        if 100 < z_.id < 500:
            if z_.id < 300:
                fK[22] = GameCanvas.item_tables[0].get_int(z_.id - 101, 5)
            else:
                fK[22] = GameCanvas.item_tables[1].get_int(z_.id - 301, 6)
            if fK[22] > 0:
                fK[21] = z_.attack * 100
                fK[21] = fK[21] + z_.defense * 100
                fK[21] = fK[21] + idiv(z_.hp * 100, 5)
                fK[21] = fK[21] + idiv(z_.mp * 100, 3)
                if z_.enchant >= fK[22]:
                    fK[22] = 0
                    fK[20] = 3
                    return
        fK[20] = 1
        if fK[22] != 0:
            fK[23] = -1

    def draw_shop_description(self, paramz, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramBoolean):  # e.java:3083-3206  (shop description)
        dF = GameCanvas.info_box
        str1 = "/ Price: "
        str2 = "Price: "
        if paramz.id == 0:
            dF.shown = 0
            dF.rect.x = dF.rect.y = dF.rect.w = dF.rect.h = 0
            dF.text = ""
            dF.rect.x = (GameCanvas.screen_w - 202) // 2 - GameCanvas.view_x
            dF.rect.y = 200
            dF.rect.w = paramInt3 + 2
            dF.rect.h = paramInt4
            return
        if GameCanvas.cursor[14] > 0 and paramInt5 == -1:
            paramInt5 = Menus.item_price(paramz)
        if paramz.id < 100:
            i = paramz.id - 1
            dF.text = consts.aN[i]
            if GameCanvas.cursor[14] == 2:
                if len(dF.text) > 0:
                    dF.text += " / "
                dF.text += str2
                dF.text += GameCanvas.format_thousands(paramInt5 >> 1)
            dF.text += " / "
            if i < 9:
                str_ = "Recover " + str(consts.aP[i % 3]) + "% of total " + consts.aO[i // 3]
            else:
                str_ = "Ranged Atk"
            dF.text += str_
            if GameCanvas.cursor[14] == 1:
                dF.text += str1
                dF.text += GameCanvas.format_thousands(paramInt5)
        else:
            if paramz.id < 300:
                str_ = GameCanvas.item_tables[0].get_string(paramz.id - 101, 0)
                i = consts.w[(paramz.id - 101) % 5]
            elif paramz.id < 500:
                str_ = GameCanvas.item_tables[1].get_string(paramz.id - 301, 0)
                i = GameCanvas.item_tables[1].get_int(paramz.id - 301, 8)
            else:
                str_ = GameCanvas.item_tables[2].get_string(paramz.id - 501, 0)
                i = GameCanvas.item_tables[2].get_int(paramz.id - 501, 7)
            if paramBoolean:
                dF.text += str_
            if GameCanvas.cursor[14] == 2:
                if len(dF.text) > 0:
                    dF.text += " / "
                dF.text += str2
                dF.text += GameCanvas.format_thousands(paramInt5 >> 1)
            if len(dF.text) > 0:
                dF.text += " / "
            special = {434: " / Hp 5 Increased", 435: " / MP 3 Increased", 436: " / DEF 1 Increased",
                       437: " / ATK 1 Increased", 502: " / Catherine's scarf", 504: " / all General Visiting"}
            if paramz.id in special:
                dF.text += special[paramz.id][3:]
                if paramz.id == 504 and paramz.enchant > 0:
                    dF.text += " / Enchanted Lv" + str(paramz.enchant)
            else:
                if paramz.attack > 0:
                    dF.text += "Atk+" + str(paramz.attack) + " "
                if paramz.defense > 0:
                    dF.text += "Def+" + str(paramz.defense) + " "
                if paramz.hp > 0:
                    dF.text += "HP+" + str(paramz.hp) + " "
                if paramz.mp > 0:
                    dF.text += "MP+" + str(paramz.mp) + " "
                if paramz.enchant > 0:
                    dF.text += "/ Enchanted Lv" + str(paramz.enchant) + " "
                if i > 0:
                    dF.text += "/ Available at Lv" + str(i) + " "
            if GameCanvas.cursor[14] == 1:
                dF.text += str1
                dF.text += GameCanvas.format_thousands(paramInt5)
        dF.rect.x = (GameCanvas.screen_w - 202) // 2 - GameCanvas.view_x
        dF.rect.y = 200
        dF.rect.w = paramInt3 + 2
        dF.rect.h = paramInt4
        GameCanvas.text_width = GameCanvas.measure_text(dF.text)
        if GameCanvas.text_width > paramInt3 - 2:
            dF.shown = 1
            if GameCanvas.key != -999:
                dF.text_x = i16(dF.rect.x + dF.rect.w)
                return
        else:
            dF.shown = 0
            dF.text_x = i16(paramInt1 + 1)

    def load_title_images(self):  # e.java:1241-1244
        self.load_title_picture()
        GameCanvas.images[18] = self.load_image(GameCanvas.scr_ui.get(77))

    def draw_main_menu(self):  # e.java:1370-1383  (Main Menu: caption strip + blinking arrows)
        i = GameCanvas.menu[1]
        j_ = GameCanvas.view_cx - 52 + GameCanvas.view_x
        if 0 == i and not GameCanvas.has_save():
            i = 9
        GameCanvas.draw_region(j_, GameCanvas.canvas_size.y - 65, 116, 21, GameCanvas.images[18], 0, i * 21)
        GameCanvas.draw_region(j_ - 24 - GameCanvas.lord_count % 3 * 2, GameCanvas.canvas_size.y - 65 + 2, 10, 16, GameCanvas.images[17], 0, 0)
        GameCanvas.draw_region(j_ + 116 + 16 + GameCanvas.lord_count % 3 * 2, GameCanvas.canvas_size.y - 65 + 2, 10, 16, GameCanvas.images[17], 10, 0)
        if GameCanvas.lord_count > 100:
            GameCanvas.lord_count = 32
            return
        GameCanvas.lord_count += 1

    def draw_hero_choice(self):  # e.java:1385-1404  (screen 6: choose the hero, 3 heads, the middle one is chosen)
        image = None
        i = GameCanvas.hero.head - 1 & 0x3
        Gfx.set_font(GameCanvas.font_white)
        for b in range(3):
            str_ = GameCanvas.gamestr(65 + b)
            self.draw_text_at(str_, GameCanvas.view_cy - 90 - b * 20 + 10, 0)
        for b in range(3):
            image = self.load_image(GameCanvas.scr_char.get(38 + i))
            self.draw_round_outline(GameCanvas.view_cx - 94 + 69 * b + GameCanvas.view_x, GameCanvas.view_cy + 9 + GameCanvas.view_y, 50, 50, 148, 109, 82)
            self.draw_rect_outline(GameCanvas.view_cx - 93 + 69 * b + GameCanvas.view_x, GameCanvas.view_cy + 10 + GameCanvas.view_y, 48, 48, 33, 0, 0)
            self.draw_map_region(image, GameCanvas.view_cx - 92 + 69 * b, GameCanvas.view_cy + 11, 46, 46, 0, 0)
            i = i + 1 & 0x3
        self.draw_selection(GameCanvas.view_cx - 27 + GameCanvas.view_x + 1, GameCanvas.view_cy + 8 + GameCanvas.view_y, 52, 52, 255, 182, 82)
        self.draw_arrow(0, GameCanvas.view_cx - 40, GameCanvas.view_cy + 23)
        self.draw_arrow(1, GameCanvas.view_cx + 30, GameCanvas.view_cy + 23)
        # PORT-EXTRA: the heroes differ in base stats (hero_classes); show the chosen one's
        head = GameCanvas.hero.head
        self.draw_text_at(hero_classes.NAMES[head & 0x3], GameCanvas.view_cy + 72, 0)
        self.draw_text_at(hero_classes.stats_line(head), GameCanvas.view_cy + 92, 0)

    # --- PORT-EXTRA: attribute reset (pow/game/hero_classes.py) ---------------------------------
    def open_respec(self):
        """Attributes screen, left soft key: pay gold or an elixir to get the stat points back."""
        cz = GameCanvas.hero
        cs = GameCanvas.popups
        if hero_classes.spent_points(cz) == 0:
            cs.popup_id = RESPEC_DONE_POPUP
            cs.show_text("3Nothing to reset.")
            return
        slot = hero_classes.respec_item_slot(cz)
        if slot >= 0:
            item = "Use " + Menus.item_name(cz.backpack[slot].id)
        else:
            item = "No elixir"
        cs.setup_choice(RESPEC_POPUP, ["Reset attributes?", "Refund: %d points" % hero_classes.spent_points(cz)],
                        ["Pay " + GameCanvas.format_thousands(hero_classes.respec_gold(cz)) + " gold", item, "Cancel"])

    def finish_respec(self, choice):
        """The choice of open_respec(): 0 gold, 1 elixir, 2 cancel."""
        cz = GameCanvas.hero
        cs = GameCanvas.popups
        GameCanvas.redraw = 1
        if choice == 0:
            cost = hero_classes.respec_gold(cz)
            if cz.gold < cost:
                cs.popup_id = RESPEC_DONE_POPUP
                cs.show_text("3Not enough gold.")
                return
            cz.gold -= cost
        elif choice == 1:
            slot = hero_classes.respec_item_slot(cz)
            if slot < 0:
                cs.popup_id = RESPEC_DONE_POPUP
                cs.show_text("3You have no elixir.|Rise Potion, Azure|Potion, Falls or|Forest Medicine.")
                return
            Item.clear(cz.backpack[slot])
        else:
            return
        n = hero_classes.respec(cz)
        GameCanvas.update_hero_stats()
        GameCanvas.menu[1] = 0
        self.save_game()
        cs.popup_id = RESPEC_DONE_POPUP
        cs.show_text("3Attributes reset.|%d points are free." % n)

    def draw_name_captions(self):  # e.java:1406-1413  (screen 7: the two caption lines)
        Gfx.set_font(GameCanvas.font_white)
        GameCanvas.anim_step = 0
        while GameCanvas.anim_step < 2:
            self.draw_text_at(GameCanvas.gamestr(69 + GameCanvas.anim_step), GameCanvas.view_cy - 47 + GameCanvas.anim_step * 20, 0)
            GameCanvas.anim_step += 1

    def draw_name_box(self):  # e.java:1415-1427  (screen 7: the name box)
        i = GameCanvas.view_cx - 80 + GameCanvas.view_x
        j_ = GameCanvas.view_cy + 8 + GameCanvas.view_y
        Gfx.fill_rect(i, j_, 160, 20, 0)
        Gfx.draw_rect(i, j_, 160, 20, GameCanvas.rgb(173, 170, 173))
        Gfx.set_font(GameCanvas.font_white)
        Gfx.draw_string(GameCanvas.name_buf.get_text(), GameCanvas.screen_cx, j_ + 2, 1)
        if GameCanvas.name_buf.length() == 0:
            GameCanvas.draw_softkeys(-1, 2)
            return
        GameCanvas.draw_softkeys(-1, 10)

    def draw_stat_sheet(self, paramInt):  # e.java:1429-1469  (screen 8/14: stat sheet; 1 = whole, 0 = numbers only)
        cz = GameCanvas.hero
        arrayOfInt1 = [cz.base_hp, cz.base_mp, cz.base_attack, cz.base_defense]
        image = None
        if paramInt != 0:
            arrayOfInt = self.load_exp_table()
            GameCanvas.exp_bars[0] = i16(idiv(cz.exp * 100, arrayOfInt[0]))
            image = self.load_image(GameCanvas.scr_ui.get(26))
            i = image.getWidth()
            j_ = image.getHeight()
            GameCanvas.sheet_y = GameCanvas.view_cy - j_ // 2
            GameCanvas.sheet_x = GameCanvas.view_cx - i // 2
            self.draw_map_region(image, GameCanvas.sheet_x, GameCanvas.sheet_y, i, j_, 0, 0)
            GameCanvas.draw_view_text_centred(cz.name, GameCanvas.sheet_x + 110, GameCanvas.sheet_y + 6)
            self.draw_big_number(cz.level, GameCanvas.sheet_x + 152, GameCanvas.sheet_y + 34, 0)
            self.draw_big_number(cz.fame, GameCanvas.sheet_x + 152, GameCanvas.sheet_y + 61, 0)
        else:
            arrayOfInt = [GameCanvas.sheet_x + 88, GameCanvas.sheet_y + 83, 68, 20]
            Gfx.fill_rect(arrayOfInt[0], arrayOfInt[1], arrayOfInt[2], arrayOfInt[3], 0)
            arrayOfInt[0] = GameCanvas.sheet_x + 39
            arrayOfInt[1] = GameCanvas.sheet_y + 108
            arrayOfInt[2] = 104
            arrayOfInt[3] = 18
            for b1 in range(4):
                Gfx.fill_rect(arrayOfInt[0], arrayOfInt[1], arrayOfInt[2], arrayOfInt[3], 0)
                arrayOfInt[1] = arrayOfInt[1] + 20
        arrayOfInt2 = [cz.gear_hp, cz.gear_mp, cz.gear_attack, cz.gear_defense]
        self.draw_big_number(cz.stat_points, GameCanvas.sheet_x + 152, GameCanvas.sheet_y + 86, 0)
        for b in range(4):
            i = self.draw_big_number(arrayOfInt1[b], GameCanvas.sheet_x + 44, GameCanvas.sheet_y + 110 + b * 20, 1)
            if arrayOfInt2[b] > 0:
                self.draw_map_region(GameCanvas.images[19], i + 1, GameCanvas.sheet_y + 110 + b * 20, 10, 14, 105, 0)
                self.draw_big_number(arrayOfInt2[b], i + 9, GameCanvas.sheet_y + 110 + b * 20, 1)
        image = self.load_image(GameCanvas.scr_char.get(38 + cz.head))
        self.draw_map_region(image, GameCanvas.sheet_x + 2, GameCanvas.sheet_y + 3, 46, 46, 0, 0)
        if cz.stat_points > 0:
            self.draw_rect_outline(GameCanvas.sheet_x + 144, GameCanvas.sheet_y + 97 + 20 * GameCanvas.menu[1] + GameCanvas.view_y + 11, 14, 18, 255, 255, 255)
        GameCanvas.menu_part = 0

    def draw_story_portraits(self, paramInt):  # e.java:2158-2165  (story: speaker portrait top-left, hero bottom-right)
        self.draw_box(19 + GameCanvas.view_x + 2, GameCanvas.view_cy - 72 + 9 + GameCanvas.view_y, 46, 46, True)
        if paramInt > -1:
            self.draw_image_file(GameCanvas.scr_char.get(0 + paramInt), 19 + GameCanvas.view_x + 2, GameCanvas.view_cy - 73 + 10 + GameCanvas.view_y, 46, 46, 0, 0)
        self.draw_box(GameCanvas.canvas_size.x // 2 + 60 - GameCanvas.view_x, GameCanvas.view_cy - 72 + 109 + GameCanvas.view_y, 46, 46, True)
        self.draw_image_file(GameCanvas.scr_char.get(38 + GameCanvas.hero.head), GameCanvas.canvas_size.x // 2 + 60 - GameCanvas.view_x, GameCanvas.view_cy - 73 + 110 + GameCanvas.view_y, 46, 46, 0, 0)
        self.draw_speech_boxes(3)

    def draw_speech_boxes(self, paramInt):  # e.java:2167-2172  (empty speech boxes: 1 = top, 2 = bottom)
        if (paramInt & 0x1) != 0:
            self.draw_box(GameCanvas.view_cx - 60 + 15 + GameCanvas.view_x, GameCanvas.view_cy - 73 + 7 + GameCanvas.view_y, 150, 53, False)
        if (paramInt & 0x2) != 0:
            self.draw_box(GameCanvas.view_cx - 60 + -40 + GameCanvas.view_x, GameCanvas.view_cy - 73 + 107 + GameCanvas.view_y, 150, 53, False)

    @staticmethod
    def type_speech(paramInt1, paramInt2, paramInt3):  # e.java:2216-2309  (type speech text fw[p1], max 3 lines)
        # paramInt3 == 0: one tick of typing (state kept in fA/fx/fy/fz/fB/fC); 1: redraw all
        if paramInt1 == 0:
            i3 = GameCanvas.view_cx - 60 + 15 + 2 + GameCanvas.view_x
            i4 = GameCanvas.view_cy - 73 + 7 + 2 + GameCanvas.view_y
        elif paramInt1 == 1:
            i3 = GameCanvas.view_cx - 60 + -40 + 2 + GameCanvas.view_x
            i4 = GameCanvas.view_cy - 73 + 107 + 2 + GameCanvas.view_y
        else:
            return False
        if (GameCanvas.key == -6 or GameCanvas.key == -5) and 0 == paramInt3:
            i1 = 1000                    # a key shows the whole text at once
        else:
            i1 = GameCanvas.speech_pos[paramInt1]
        # decompiled `if (!(n = (p2 != i1) ? 0 : p2))`: n == 0 -> start over, else continue
        n = 0 if paramInt2 != i1 else paramInt2
        if n == 0:
            i = i3
            j_ = i4
            i2 = 0
            m = 0
            k = 0
        else:
            i = GameCanvas.speech_x[paramInt1]
            j_ = GameCanvas.speech_y[paramInt1]
            i2 = GameCanvas.speech_lines[paramInt1]
            m = GameCanvas.speech_done[paramInt1]
            k = GameCanvas.speech_w[paramInt1]
        Gfx.set_font(GameCanvas.font_white)
        while n <= i1 and n < len(GameCanvas.speech[paramInt1]):
            fw = GameCanvas.speech[paramInt1]
            i5 = Font.ascent() + Font.gap()
            p = (1 if n <= 0 else n) - 1
            if i == i3 or (p < len(fw) and fw[p] == ' ') or (n - 1 < len(fw) and fw[n - 1] == ']'):
                b = 0
                i6 = 0
                while n + b + 1 < len(fw) and fw[n + b] != ' ' and fw[n + b] != ']' and fw[n + b] != ',':
                    i6 += Font.ascent() + Font.gap()
                    b += 1
                    if i6 > 146:
                        i6 -= Font.ascent() + Font.gap()
                if fw[n + b] == ']':
                    k += Font.ascent()
                if i6 + k > 146:
                    k += i6
            k += i5
            if k > 146:
                if GameCanvas.key != -999 and m == 2:
                    break
                i = i3
                k = i5
                if m == 0:
                    i2 = n
                elif m != 1 and m == 2:
                    # 3 lines are full: drop the first line and start drawing again
                    str_ = fw[i2:]
                    GameCanvas.speech[paramInt1] = str_
                    i1 -= i2
                    m = n = 0
                    j_ = i4
                    k = 0
                    continue
                m += 1
                j_ += 16
            if n == 0:
                GameCanvas.menus.draw_speech_boxes(paramInt1 + 1)
            if i == i3 and fw[n] == ' ':
                n += 1
            if len(fw) >= n + 1:
                Gfx.draw_string(fw[n:n + 1], i, j_, 0)
            i += i5
            n += 1
        if 0 == paramInt3:
            GameCanvas.speech_pos[paramInt1] = n
            GameCanvas.speech_x[paramInt1] = i
            GameCanvas.speech_y[paramInt1] = j_
            GameCanvas.speech_w[paramInt1] = k
            GameCanvas.speech_lines[paramInt1] = i2
            GameCanvas.speech_done[paramInt1] = m
        return True

    def draw_difficulty(self):  # e.java:2374-2394  (screen 29: difficulty Hard / Normal)
        arrayOfInt = [GameCanvas.view_cx - 80 + GameCanvas.view_x, GameCanvas.view_cy - 60 + GameCanvas.view_y]
        GameCanvas.difficulty = i16(GameCanvas.menu[1])
        for b in range(2):
            if GameCanvas.menu[1] == b:
                Gfx.set_font(GameCanvas.font_orange)
                bool_ = True
            else:
                Gfx.set_font(GameCanvas.font_white)
                bool_ = False
            self.draw_box(arrayOfInt[0], arrayOfInt[1] + b * 25, 160, 20, bool_)
            self.draw_text_at(consts.aX[b], arrayOfInt[1] + 1 + b * 25 - 1, 15)
        Gfx.set_font(GameCanvas.font_white)
        self.draw_box(arrayOfInt[0], GameCanvas.view_cy + GameCanvas.view_y, 160, 80, False)
        for b in range(3):
            self.draw_text_at(consts.aY[GameCanvas.menu[1]][b], GameCanvas.view_cy + 10 + b * 20, 17)

    def load_item_def(self, paramInt):  # e.java:3465-3531  (item record -> cX / cY / cZ)
        arrayOfByte = bytearray(16)
        if paramInt < 100:
            return
        if paramInt < 300:
            if GameCanvas.gear_data is None:
                GameCanvas.gear_data = GameCanvas.load_data_file(47)
            cU = GameCanvas.gear_data
            i = 9 + (paramInt - 101) * 23
            b = 0
            while b < 15:
                arrayOfByte[b] = cU[i + b] & 0xFF
                if arrayOfByte[b] == 0:
                    break
                b += 1
            GameCanvas.gear_def.name = GameCanvas.read_utf(arrayOfByte, 0, b)
            GameCanvas.gear_def.slot = i8(cU[i + 15])
            GameCanvas.gear_def.bonus_stat = i8(cU[i + 15 + 1])
            GameCanvas.gear_def.bonus = i8(cU[i + 15 + 2])
            GameCanvas.gear_def.bonus_range = i8(cU[i + 15 + 3])
            GameCanvas.gear_def.icon = i8(cU[i + 22])
            if GameCanvas.state != 2:
                GameCanvas.gear_data = None
                return
        elif paramInt < 500:
            if GameCanvas.treasure_data is None:
                GameCanvas.treasure_data = GameCanvas.load_data_file(51)
            cV = GameCanvas.treasure_data
            i = 10 + (paramInt - 301) * 24
            b = 0
            while b < 15:
                arrayOfByte[b] = cV[i + b] & 0xFF
                if arrayOfByte[b] == 0:
                    break
                b += 1
            GameCanvas.treasure_def.name = GameCanvas.read_utf(arrayOfByte, 0, b)
            GameCanvas.treasure_def.slot = i8(cV[i + 15])
            GameCanvas.treasure_def.attack = GameCanvas.u16(cV[i + 16], cV[i + 17])
            GameCanvas.treasure_def.defense = i8(cV[i + 18])
            GameCanvas.treasure_def.hp = cV[i + 19] & 0xFF
            GameCanvas.treasure_def.mp = i8(cV[i + 20])
            GameCanvas.treasure_def.icon = i8(cV[i + 22])
            GameCanvas.treasure_def.level = cV[i + 23] & 0xFF
            if GameCanvas.state != 2:
                GameCanvas.treasure_data = None
                return
        else:
            if GameCanvas.rare_data is None:
                GameCanvas.rare_data = GameCanvas.load_data_file(49)
            cW = GameCanvas.rare_data
            i = 9 + (paramInt - 501) * 27
            b = 0
            while b < 15:
                arrayOfByte[b] = cW[i + b] & 0xFF
                if arrayOfByte[b] == 0:
                    break
                b += 1
            GameCanvas.rare_def.name = GameCanvas.read_utf(arrayOfByte, 0, b)
            GameCanvas.rare_def.slot = i8(cW[i + 15])
            GameCanvas.rare_def.attack = GameCanvas.u16(cW[i + 16], cW[i + 17])
            GameCanvas.rare_def.defense = i8(cW[i + 18])
            GameCanvas.rare_def.hp = GameCanvas.u16(cW[i + 19], cW[i + 20])
            GameCanvas.rare_def.mp = i8(cW[i + 21])
            GameCanvas.rare_def.level = cW[i + 26] & 0xFF
            if GameCanvas.state != 2:
                GameCanvas.rare_data = None

    def draw_stat_cursor(self, paramInt):  # e.java:3533-3545  (stat cursor: 0 = erase, 1 = draw)
        if GameCanvas.hero.stat_points > 0:
            if paramInt != 0:
                c = 255 if F11 else 1   # DECOMP-FIX F11: decompiled `true` (= 1) as a colour
            else:
                c = 0
            self.draw_rect_outline(GameCanvas.sheet_x + 144, GameCanvas.sheet_y + 97 + 20 * GameCanvas.menu[1] + 11, 14, 18, c, c, c)

    def load_exp_table(self):  # e.java:3547-3560  (exp table of the hero level from edat 45)
        arrayOfByte = GameCanvas.load_data_file(45)
        j_ = 40
        if GameCanvas.hero.level > 190:
            j_ = 200 - GameCanvas.hero.level << 2
        k = j_ // 4
        arrayOfInt = [0] * k
        i = 4 * (GameCanvas.hero.level - 1) + 2
        for b in range(k):
            o = i + b * 4
            arrayOfInt[b] = i32((arrayOfByte[o + 3] & 0xFF) << 24 | (arrayOfByte[o + 2] & 0xFF) << 16
                                | (arrayOfByte[o + 1] & 0xFF) << 8 | arrayOfByte[o] & 0xFF)
        return arrayOfInt

    def draw_game_menu(self):  # e.java:3283-3364  (Game Menu carousel, 4 animation frames per step)
        cM = GameCanvas.menu
        s = GameCanvas.menu_anim
        if GameCanvas.images[27] is None:
            self.load_menu_frames()
        dd = GameCanvas.view_cx
        arrayOfInt1 = [dd - 44 + 0] * 4
        arrayOfInt2 = [164, 180, 188, 166]
        arrayOfInt3 = [dd - 44 + 0] * 4
        arrayOfInt4 = [244, 230, 220, 244]
        arrayOfInt5 = [dd - 63 - 5 + 0] * 4
        arrayOfInt6 = [200, 232, 185, 204]
        i = dd - 60
        if GameCanvas.redraw == 2:
            if GameCanvas.menu_scroll == 1:
                for arr in (arrayOfInt1, arrayOfInt2, arrayOfInt3, arrayOfInt4, arrayOfInt5, arrayOfInt6):
                    arr[1], arr[2] = arr[2], arr[1]
                GameCanvas.menu_anim = i16(GameCanvas.menu_anim + 1)
                if GameCanvas.menu_anim == 3:
                    cM[1] = cM[1] + 1
                    if _inc_cmp(cM[1]) >= GameCanvas.menu_count - 1:
                        cM[2] = 0
                        cM[1] = 0
                    GameCanvas.clamp_menu_scroll()
                elif GameCanvas.menu_anim > 3:
                    GameCanvas.redraw = 0
                    GameCanvas.menu_scroll = 0
                    GameCanvas.menu_anim = 0
            elif GameCanvas.menu_scroll == -1:
                GameCanvas.menu_anim = i16(GameCanvas.menu_anim + 1)
                if GameCanvas.menu_anim == 3:
                    cM[1] = cM[1] - 1
                    if _dec_cmp(cM[1]) < 0:
                        cM[1] = GameCanvas.menu_count - 1 - 1
                    GameCanvas.clamp_menu_scroll()
                elif GameCanvas.menu_anim > 3:
                    GameCanvas.redraw = 0
                    GameCanvas.menu_scroll = 0
                    GameCanvas.menu_anim = 0
        self.draw_view_region(GameCanvas.images[7], 0, 0, GameCanvas.canvas_size.x, GameCanvas.canvas_size.y, 0, 0)
        self.draw_text_at(GameCanvas.menu_titles[cM[0]], 2 - GameCanvas.view_y, 0)
        if GameCanvas.carousel_image is None or GameCanvas.carousel_row != cM[1]:
            GameCanvas.carousel_image = self.load_image(GameCanvas.scr_ui.get(66 + cM[1]))
            GameCanvas.carousel_row = cM[1]
        if GameCanvas.carousel_image is not None:
            GameCanvas.draw_region(i, 60, 117, 90, GameCanvas.carousel_image, 0, 0)
        GameCanvas.draw_region(arrayOfInt1[s], arrayOfInt2[s], 89, 20, GameCanvas.images[27], 0, 0)
        GameCanvas.draw_region(arrayOfInt1[s] + 22, arrayOfInt2[s] + 5, 62, 11, GameCanvas.images[29], 0,
                     11 * (4 if cM[1] == 0 else (cM[1] - 1)))
        GameCanvas.draw_region(arrayOfInt3[s], arrayOfInt4[s], 89, 20, GameCanvas.images[27], 0, 0)
        GameCanvas.draw_region(arrayOfInt3[s] + 22, arrayOfInt4[s] + 5, 62, 11, GameCanvas.images[29], 0,
                     11 * (0 if cM[1] == 4 else (cM[1] + 1)))
        GameCanvas.draw_region(arrayOfInt5[s], arrayOfInt6[s], 127, 29, GameCanvas.images[26], 0, 0)
        GameCanvas.draw_region(arrayOfInt5[s] + 22 + 2, arrayOfInt6[s] + 5 + 1, 94, 18, GameCanvas.images[28], 0, 18 * cM[1])
        if GameCanvas.redraw != 2 and GameCanvas.menu_anim == 0:
            GameCanvas.draw_region(dd - 5 + GameCanvas.view_x, arrayOfInt6[s] - 6 - 5 - GameCanvas.lord_count % 3 * 2, 16, 10, GameCanvas.images[17], 20, 0)
            GameCanvas.draw_region(dd - 5 + GameCanvas.view_x, arrayOfInt6[s] + 29 + GameCanvas.lord_count % 3 * 2, 16, 10, GameCanvas.images[17], 20, 10)
        if GameCanvas.lord_count > 100:
            GameCanvas.lord_count = 32
        else:
            GameCanvas.lord_count += 1
        GameCanvas.draw_softkeys(-1, 2)

    # ---- Missions: lords (1), missions (2), description (3), briefing (4) ------------------

    def draw_mission_text(self):  # e.java:1229-1238  (mission description, 6 lines per page)
        self.draw_box(GameCanvas.view_cx - 100 + GameCanvas.view_x, GameCanvas.view_cy - 80, 200, 40, False)
        self.draw_text_at(GameCanvas.lord_name, GameCanvas.view_cy - 80, 30)
        self.draw_text_at(GameCanvas.mission_name, GameCanvas.view_cy - 60, 30)
        self.draw_box(GameCanvas.view_cx - 110, GameCanvas.view_cy - 30, 220, 119, False)
        for b in range(6):
            if GameCanvas.text_line_count[0] >= GameCanvas.menu[2] * 6 + b:
                GameCanvas.draw_text_left(GameCanvas.view_cx - 100 + GameCanvas.view_x, GameCanvas.view_cy - 28 + b * 20 + GameCanvas.view_y, GameCanvas.text_lines[0][GameCanvas.menu[2] * 6 + b])
        self.draw_page_number(GameCanvas.menu[2] + 1, idiv(GameCanvas.text_line_count[0], 6) + 1, GameCanvas.view_cy + 110, True)

    def draw_briefing(self):  # e.java:1246-1250  (briefing: portraits + empty speech boxes)
        self.draw_story_portraits(GameCanvas.mission_portraits[GameCanvas.mission])
        self.draw_skip_key(1)
        self.draw_speech_boxes(3)

    def draw_map_talk(self):  # e.java:1252-1264  (talk in the map: portrait bottom-left)
        if (GameCanvas.talk_box & 0x1) != 0:
            i = 0 + GameCanvas.general.portrait
        else:
            i = 38 + GameCanvas.hero.head
        j_ = GameCanvas.view_size.y - 46 - 4
        self.draw_box(2 + GameCanvas.view_x, j_ + GameCanvas.view_y, 48, 48, True)
        j_ += 1
        self.draw_image_file(GameCanvas.scr_char.get(i), 3 + GameCanvas.view_x, j_ + GameCanvas.view_y, 46, 46, 0, 0)
        self.draw_map_talk_box()
        self.draw_skip_key(1)

    def tick_dialogue(self):  # e.java:1266-1361  (dialogue typewriter: dG 0 briefing, 1 map talk, 2 general)
        arrayOfByte1 = [2, 3, 5]
        arrayOfByte2 = [2, 1, 1]
        if GameCanvas.state == 5 and GameCanvas.key != -6:
            GameCanvas.key = -999
        Gfx.set_font(GameCanvas.font_white)
        if GameCanvas.key == -6:
            GameCanvas.wait_ticks = 1
            GameCanvas.talk_rows = i16(GameCanvas.text_line_count[GameCanvas.talk_side])
            GameCanvas.talk_box = i16(arrayOfByte1[GameCanvas.talk_kind])
        if GameCanvas.wait_ticks > 0:
            GameCanvas.wait_ticks = i16(GameCanvas.wait_ticks - 1)
            if GameCanvas.key != -999:
                GameCanvas.wait_ticks = 0
            if GameCanvas.wait_ticks < 1:
                if GameCanvas.talk_rows >= GameCanvas.text_line_count[GameCanvas.talk_side]:
                    if GameCanvas.talk_box >= arrayOfByte1[GameCanvas.talk_kind]:
                        GameCanvas.redraw = 1
                        if GameCanvas.talk_kind != 0:
                            if GameCanvas.talk_kind == 1:
                                GameCanvas.state = 3
                                return
                            if GameCanvas.boss_fight != 0:
                                self.open_menu(2)
                                self.load_menu_frames()
                                GameCanvas.menu[0] = 0
                                GameCanvas.menu_count = consts.v[GameCanvas.menu[0]]
                                GameCanvas.menu_items = GameCanvas.game_menu_items
                                GameCanvas.state = 2
                                GameCanvas.menu_scroll = 0
                                GameCanvas.menu_anim = 0
                                GameCanvas.redraw = 1
                                self.paint_state()
                                return
                            GameCanvas.room_phase = 1
                            GameCanvas.room_phase_timer = 5
                            GameCanvas.state = 3
                            return
                        self.enter_map()
                        return
                    GameCanvas.talk_row = 0
                    GameCanvas.talk_rows = 0
                    if 0 == GameCanvas.talk_kind:
                        GameCanvas.talk_side = i16(GameCanvas.talk_side + 1 & 0x1)
                    GameCanvas.next_speech_pos()
                    self.load_dialogue_line(GameCanvas.talk_line + GameCanvas.talk_box - 1)
                    if GameCanvas.talk_kind != 0:
                        self.draw_map_talk()
                        return
                    self.draw_briefing_boxes()
                    return
                GameCanvas.talk_row = i16(GameCanvas.talk_row + 1)
                GameCanvas.talk_rows = i16(GameCanvas.talk_rows + 1)
                GameCanvas.talk_chars = 0
                GameCanvas.talk_cursor_x = GameCanvas.talk_x[GameCanvas.talk_side]
                if GameCanvas.talk_row > arrayOfByte2[GameCanvas.talk_kind]:
                    GameCanvas.talk_row = i16(arrayOfByte2[GameCanvas.talk_kind])
                    for b in range(20):
                        if b < GameCanvas.text_line_count[GameCanvas.talk_side]:
                            GameCanvas.text_lines[GameCanvas.talk_side][b] = GameCanvas.text_lines[GameCanvas.talk_side][b + 1]
                    if GameCanvas.talk_kind != 0:
                        self.draw_map_talk_box()
                        return
                    self.draw_briefing_boxes()
                    return
        else:
            if GameCanvas.key == -5:
                GameCanvas.talk_rows = i16(GameCanvas.talk_rows + arrayOfByte2[GameCanvas.talk_kind] - GameCanvas.talk_row)
                GameCanvas.talk_row = i16(arrayOfByte2[GameCanvas.talk_kind])
                GameCanvas.talk_chars = 29
                if GameCanvas.talk_kind != 0:
                    self.draw_map_talk_box()
                else:
                    self.draw_briefing_boxes()
                GameCanvas.wait_ticks = 3
                return
            line = GameCanvas.text_lines[GameCanvas.talk_side][GameCanvas.talk_row]
            str_ = line[GameCanvas.talk_chars:]
            if len(str_) != 0 and ord(str_[0]) > 0:
                GameCanvas.talk_chars = i16(GameCanvas.talk_chars + 1)
                Gfx.draw_string(str_[0:1], GameCanvas.talk_cursor_x + GameCanvas.view_x, GameCanvas.talk_y[GameCanvas.talk_side] + 16 * GameCanvas.talk_row + GameCanvas.view_y, 0)
                GameCanvas.talk_cursor_x = i16(GameCanvas.talk_cursor_x + 9)
                return
            if GameCanvas.talk_rows >= GameCanvas.text_line_count[GameCanvas.talk_side]:
                GameCanvas.wait_ticks = 15
                return
            GameCanvas.wait_ticks = 1

    def draw_briefing_boxes(self):  # e.java:2174-2205  (briefing: both speech boxes)
        Gfx.set_font(GameCanvas.font_white)
        self.draw_speech_boxes(2 if GameCanvas.talk_side != 0 else 1)
        dp, dL, dM = GameCanvas.text_lines, GameCanvas.talk_x, GameCanvas.talk_y
        if GameCanvas.talk_side != 0:
            for b in range(3):
                GameCanvas.draw_text(dL[0] + GameCanvas.view_x, dM[0] + 16 * b + GameCanvas.view_y, dp[0][b])
        else:
            for b in range(GameCanvas.talk_row):
                if dp[0][b] is not None:
                    GameCanvas.draw_text(dL[0] + GameCanvas.view_x, dM[0] + 16 * b + GameCanvas.view_y, dp[0][b])
            if dp[0][GameCanvas.talk_row] is not None:
                str_ = dp[0][GameCanvas.talk_row][0:min(GameCanvas.talk_chars, len(dp[0][GameCanvas.talk_row]))]
                GameCanvas.draw_text(dL[0] + GameCanvas.view_x, dM[0] + 16 * GameCanvas.talk_row + GameCanvas.view_y, str_)
        if GameCanvas.talk_box > 1:
            if GameCanvas.talk_side != 0:
                for b in range(GameCanvas.talk_row):
                    if dp[1][b] is not None:
                        GameCanvas.draw_text(dL[1] + GameCanvas.view_x, dM[1] + 16 * b + GameCanvas.view_y, dp[1][b])
                if dp[1][GameCanvas.talk_row] is not None:
                    str_ = dp[1][GameCanvas.talk_row][0:min(GameCanvas.talk_chars, len(dp[1][GameCanvas.talk_row]))]
                    GameCanvas.draw_text(dL[1] + GameCanvas.view_x, dM[1] + 16 * GameCanvas.talk_row + GameCanvas.view_y, str_)
                    return
            else:
                for b in range(3):
                    GameCanvas.draw_text(dL[1] + GameCanvas.view_x, dM[1] + 16 * b + GameCanvas.view_y, dp[1][b])

    def draw_map_talk_box(self):  # e.java:2207-2214  (map talk: one speech box at the bottom)
        self.draw_box(54 + GameCanvas.view_x, GameCanvas.view_size.y - 40 + GameCanvas.view_y, GameCanvas.view_size.x - 56, 38, True)
        Gfx.set_font(GameCanvas.font_white)
        for b in range(GameCanvas.talk_row):
            GameCanvas.draw_text(GameCanvas.talk_x[0] + GameCanvas.view_x, GameCanvas.talk_y[0] + 16 * b + GameCanvas.view_y, GameCanvas.text_lines[0][b])
        str_ = GameCanvas.text_lines[0][GameCanvas.talk_row][0:GameCanvas.talk_chars]
        GameCanvas.draw_text(GameCanvas.talk_x[0] + GameCanvas.view_x, GameCanvas.talk_y[0] + 16 * GameCanvas.talk_row + GameCanvas.view_y, str_)

    def load_lord_missions(self):  # e.java:3569-3603  (missions of lord dk -> dz / dA / dB, list dE = dA)
        i = 0
        GameCanvas.map_id = GameCanvas.lord_ids[GameCanvas.lord]
        GameCanvas.lord_name = GameCanvas.lord_names[GameCanvas.lord]
        arrayOfByte1 = GameCanvas.load_data_file(50)
        GameCanvas.menu_count = GameCanvas.lord_mission_counts[GameCanvas.lord]
        i = 11 * GameCanvas.lord_missions[GameCanvas.lord] + 11
        arrayOfByte2 = GameCanvas.load_data_file(55)
        for b in range(GameCanvas.menu_count):
            if GameCanvas.lords[b] is None:
                GameCanvas.lords[b] = MissionDef()
            dz = GameCanvas.lords[b]
            dz.id = GameCanvas.u8(arrayOfByte1[i])
            dz.start_x = GameCanvas.u8(arrayOfByte1[i + 1])
            dz.start_y = GameCanvas.u8(arrayOfByte1[i + 2])
            dz.tint = GameCanvas.u8(arrayOfByte1[i + 3])
            dz.boss_type = GameCanvas.u8(arrayOfByte1[i + 4])
            dz.general = GameCanvas.u8(arrayOfByte1[i + 5])
            dz.reward = GameCanvas.u8(arrayOfByte1[i + 6])
            dz.gold = GameCanvas.u8(arrayOfByte1[i + 7])
            dz.time_limit = i16(arrayOfByte1[i + 8] & 0xFF | i8(arrayOfByte1[i + 9]) & 0xFF00)
            dz.level_bonus = GameCanvas.u8(arrayOfByte1[i + 10])
            i += 11
            j_ = 3 + (dz.id - 1) * 15
            b1 = 14
            for b2 in range(14):
                if arrayOfByte2[j_ + b2] == 0:
                    b1 = b2
                    break
            GameCanvas.mission_names[b] = GameCanvas.read_utf(arrayOfByte2, j_, j_ + b1)
            GameCanvas.mission_portraits[b] = i8(arrayOfByte2[17 + (dz.id - 1) * 15])
        GameCanvas.menu_items = GameCanvas.mission_names

    # ---- Visiting: generals (19 list, 20 talk) ---------------------------------------------

    def draw_generals(self):  # e.java:1694-1748  (generals: Name / Points, 4 per page)
        arrayOfString = ["Name", "Points"]
        i = idiv(GameCanvas.canvas_size.x - 208, 2) + 2
        j_ = i + 134 + 10
        k = GameCanvas.view_size.y - 20 - 20 + 10
        m = 20 + idiv(k - 177, 2) + 2
        n = m
        i1 = GameCanvas.menu[1] % 4
        i2 = GameCanvas.menu[1] // 4
        GameCanvas.general_pages[1] = i16(i2 + 1)
        i2 *= 4
        self.draw_box(i, n, 130, 22, False)
        self.draw_box(j_, n, 60, 22, False)
        Gfx.set_font(GameCanvas.font_white)
        GameCanvas.draw_text_centred(i + 65, n + 1, arrayOfString[0])
        GameCanvas.draw_text_centred(j_ + 30, n + 1, arrayOfString[1])
        n += 31
        for b in range(4):
            if b == i1:
                bool_ = True
                Gfx.set_font(GameCanvas.font_orange)
            else:
                bool_ = False
                Gfx.set_font(GameCanvas.font_white)
            self.draw_box(i, n, 130, 22, bool_)
            self.draw_box(j_, n, 60, 22, bool_)
            if i2 < GameCanvas.menu_count:
                if GameCanvas.seal != 0:
                    str_ = GameCanvas.general_table.get_string(GameCanvas.generals[2][i2] - 1, 0)
                else:
                    str_ = GameCanvas.general_table.get_string(GameCanvas.generals[0][i2] - 1, 0)
                GameCanvas.draw_text_centred(i + 65, n + 1, str_)
                if GameCanvas.seal != 0:
                    b1 = 0
                    while b1 < GameCanvas.general_count and GameCanvas.generals[2][i2] != GameCanvas.generals[0][b1]:
                        b1 += 1
                    if b1 < GameCanvas.general_count:
                        str_ = "" + str(GameCanvas.generals[1][b1])
                    else:
                        str_ = "0"
                else:
                    str_ = "" + str(GameCanvas.generals[1][i2])
                GameCanvas.draw_text_centred(j_ + 30, n + 1, str_)
            i2 += 1
            n += 31
        n += 6
        self.draw_page_number(GameCanvas.general_pages[1], GameCanvas.general_pages[0], n, True)

    def tick_general_talk(self):  # e.java:1750-1802  (general talk: type the lines gf[], then popups 14 / 16)
        if GameCanvas.wait_ticks > 0:
            GameCanvas.wait_ticks = i16(GameCanvas.wait_ticks - 1)
            if GameCanvas.key != 0 and GameCanvas.wait_ticks > 3:
                GameCanvas.wait_ticks = 3
            if 0 == GameCanvas.wait_ticks:
                GameCanvas.story_page += 1
                if GameCanvas.story_page <= 3:
                    GameCanvas.speech[GameCanvas.story_page & 0x1] = GameCanvas.talk_lines[GameCanvas.story_page - 1]
                    GameCanvas.speech_pos[GameCanvas.story_page & 0x1] = 0
                    return
                if GameCanvas.story_page == 4:
                    GameCanvas.popups.setup_popup(14)
                    GameCanvas.speech_pos[1] = 0
                    return
                if GameCanvas.story_page < 7:
                    GameCanvas.speech[GameCanvas.story_page & 0x1] = GameCanvas.talk_lines[GameCanvas.story_page - 2]
                    GameCanvas.speech_pos[GameCanvas.story_page & 0x1] = 0
                    return
                GameCanvas.visit_text.free()
                GameCanvas.visit_text = None
                GameCanvas.general_table.free()
                GameCanvas.general_table = None
                GameCanvas.popups.setup_popup(16)
                return
        else:
            if GameCanvas.story_page >= 10:
                GameCanvas.story_page -= 10
                i = GameCanvas.story_page & 0x1
                GameCanvas.speech_pos[i] = len(GameCanvas.speech[i])
                j_ = 0
            else:
                i = GameCanvas.story_page & 0x1
                j_ = GameCanvas.speech_pos[i]
            if GameCanvas.story_page != 4:
                Menus.type_speech(i, j_, 0)
                if len(GameCanvas.speech[i]) <= GameCanvas.speech_pos[i] + 1:
                    if GameCanvas.key != 0:
                        GameCanvas.wait_ticks = 5
                        return
                    GameCanvas.wait_ticks = 15

    def open_general_talk(self):  # e.java:3366-3393  (open the talk with general cM[1])
        # the decompiler shows `j = 2;` as a field write; it is the local j declared below
        if GameCanvas.seal != 0:
            j_ = 2
            b = 0
            while b < GameCanvas.general_count and GameCanvas.generals[0][b] != GameCanvas.generals[2][GameCanvas.menu[1]]:
                b += 1
            GameCanvas.visit_general = i16(b)
            GameCanvas.visit_row = i16(GameCanvas.menu[1])
        else:
            j_ = 0
            GameCanvas.visit_general = i16(GameCanvas.menu[1])
        i = GameCanvas.generals[j_][GameCanvas.menu[1]] - 1
        self.set_general(GameCanvas.generals[j_][GameCanvas.menu[1]])
        GameCanvas.general_name = GameCanvas.general_table.get_string(i, 0)
        j_ = GameCanvas.general_table.get_int(i, 9)
        k = GameCanvas.general_table.get_int(i, 8)
        i = GameCanvas.generals[1][GameCanvas.visit_general]
        GameCanvas.story_picture = k
        GameCanvas.visit_topic = j_
        if Menus.load_greeting(i, j_):
            GameCanvas.speech[0] = ""
            GameCanvas.speech[1] = GameCanvas.talk_lines[0]
            GameCanvas.speech_pos[1] = 0
            GameCanvas.speech_pos[0] = 0
            GameCanvas.story_page = 1
            return True
        return False

    @staticmethod
    def load_greeting(paramInt1, paramInt2):  # e.java:3395-3430  (greeting lines of the general -> gf[])
        if GameCanvas.visit_text is not None:
            GameCanvas.visit_text.free()
            GameCanvas.visit_text = None
        GameCanvas.visit_text = ScrTable("/" + GameCanvas.scr_data.get(62))
        if 0 <= paramInt1 <= 100 and GameCanvas.visit_text is not None:
            if paramInt2 < 2:
                if paramInt1 > 99:
                    paramInt1 = 99
                paramInt1 = paramInt1 // 10 * 3
                if paramInt2 == 1:
                    paramInt1 += 30
                b1 = 3
                b2 = 0
            else:
                paramInt1 = 60 + (paramInt2 - 2 << 1)
                b1 = 2
                b2 = 3
            for b3 in range(b1):
                if len(GameCanvas.visit_text.get(paramInt1)) > 0:
                    str_ = GameCanvas.general_name if (b3 & 0x1) != 0 else GameCanvas.hero.name
                    GameCanvas.talk_lines[b3 + b2] = "[" + str_ + "] " + GameCanvas.visit_text.get(paramInt1) + " "
                    paramInt1 += 1
                else:
                    return False
            return True
        return False

    @staticmethod
    def add_friendship(paramInt1, paramInt2):  # e.java:3432-3463  (add paramInt2 friendship to general paramInt1)
        b = 0
        while b < GameCanvas.general_count and GameCanvas.generals[0][b] != paramInt1:
            b += 1
        if b == GameCanvas.general_count:
            if paramInt2 > 0:
                d_ = ArrTable("/" + GameCanvas.scr_data.get(52))
                for b1 in range(44):
                    i = d_.get_int(b1, 0)
                    if i == paramInt1:
                        GameCanvas.generals[0][b] = i16(paramInt1)
                        GameCanvas.general_count = i16(GameCanvas.general_count + 1)
                        GameCanvas.generals[1][b] = i16(GameCanvas.generals[1][b] + paramInt2)
                        break
        else:
            GameCanvas.generals[1][b] = i16(GameCanvas.generals[1][b] + paramInt2)
            if GameCanvas.generals[1][b] > 200 or 0 == GameCanvas.generals[1][b]:
                while b < GameCanvas.general_count:
                    GameCanvas.generals[0][b] = GameCanvas.generals[0][b + 1]
                    GameCanvas.generals[1][b] = GameCanvas.generals[1][b + 1]
                    b += 1
                GameCanvas.general_count = i16(GameCanvas.general_count - 1)
            elif GameCanvas.generals[1][b] >= 100:
                GameCanvas.generals[1][b] = 100
                return 1
        return 0

    def general_gift(self):  # e.java:3208-3281  (gift of the general after the talk -> fJ, cT[0])
        arrayOfShort = [[[500, 800, 900, 960, 990, 995, 998], [60, 61, 91, 92, 392, 892, 992],
                         [100, 600, 900, 930, 990, 995, 996], [1, 2, 5, 305, 310, 410, 910]],
                        [[1, 101, 106, 606, 609, 610, 910], [30, 31, 91, 92, 592, 892, 992],
                         [300, 360, 860, 960, 961, 991, 996], [1, 2, 5, 10, 40, 100, 200]]]
        cz = GameCanvas.hero
        if self.rand(100) < GameCanvas.generals[1][GameCanvas.visit_general]:
            i = self.rand(1000)
            GameCanvas.gift_level = 0
            while GameCanvas.gift_level < 7 and i >= arrayOfShort[GameCanvas.general.gift_table][GameCanvas.gift_kind][GameCanvas.gift_level]:
                GameCanvas.gift_level = i16(GameCanvas.gift_level + 1)
            GameCanvas.popups.lines[4] = ""
            v = GameCanvas.gift_level
            if v == 0:
                i = self.random_general_skill(0)
                if cz.skill_levels[i - 1] < 10:
                    str_ = GameCanvas.edat_string(54, i - 1)
                    cz.skill_levels[i - 1] = cz.skill_levels[i - 1] + 1
                    if cz.skill_levels[i - 1] == 1:
                        GameCanvas.popups.lines[4] = "Skill :"
                        GameCanvas.popup_lines[0] = str_
                        return
                    GameCanvas.popups.lines[4] = "Skill up :"
                    GameCanvas.popup_lines[0] = str_
                    return
            elif v == 1:
                if cz.base_attack < 10000:
                    cz.base_attack += 1
                    GameCanvas.popup_lines[0] = consts.aR[0]
                    return
            elif v == 2:
                if cz.base_defense < 10000:
                    cz.base_defense += 1
                    GameCanvas.popup_lines[0] = consts.aR[1]
                    return
            elif v == 3:
                if cz.base_hp < 25000:
                    cz.base_hp += 5
                    GameCanvas.popup_lines[0] = consts.aR[2]
                    return
            elif v == 4:
                if cz.base_mp < 20000:
                    cz.base_mp += 3
                    GameCanvas.popup_lines[0] = consts.aR[3]
                    return
            elif v == 5:
                cz.fame += 10
                GameCanvas.popup_lines[0] = consts.aR[4]
                return
            elif v == 6:
                if self.give_item(GameCanvas.engine.random_drop(4), 1) != 0:
                    GameCanvas.popup_lines[0] = GameCanvas.gear_def.name
                    GameCanvas.popups.lines[4] = "Item Acquired!"
                    return
            else:
                i = self.rand(11)
                if self.give_item(i + 1, 1) != 0:
                    GameCanvas.popup_lines[0] = consts.aN[i]
                    GameCanvas.popups.lines[4] = "Item Acquired!"
                    return
        GameCanvas.gift_level = 8

    @staticmethod
    def seal_list():
        """ORIG-BUG B3: the list of "all General Visiting" of 504 Emperor's Seal (fn[2], drawn
        by e.java:1725 and visited by bg() 3366-3378) is never filled in the original, so the
        Visiting screen showed 44 empty rows; the 44 generals one can visit are visitgen.arr."""
        vg = ArrTable("/visitgen.arr")
        for b in range(44):
            GameCanvas.generals[2][b] = i16(vg.get_int(b, 0))

    @staticmethod
    def load_general_table():  # e.java:3562-3567
        GameCanvas.general_pages[0] = i16(idiv(GameCanvas.menu_count - 1, 4) + 1)
        if GameCanvas.general_table is None:
            GameCanvas.general_table = ArrTable("/" + GameCanvas.scr_data.get(46))
        return False

    def draw_popup_extras(self):  # e.java:2938-2972  (popup extras on the map: experience bars of popups 11 / 12)
        i = 0
        if GameCanvas.popups.popup_id == 11:
            i = self.draw_exp_bar(GameCanvas.exp_bar_step, 0)
            if 0 == i and 0 == GameCanvas.popups.extra:
                GameCanvas.exp_bar_step = i16(GameCanvas.exp_bar_step + 1)
        elif GameCanvas.popups.popup_id == 12:
            i = self.draw_exp_bar(GameCanvas.exp_bar_step, 1)
            if 0 == i and 0 == GameCanvas.popups.extra:
                GameCanvas.exp_bar_step = i16(GameCanvas.exp_bar_step + 1)
        if i != 0 and 0 == GameCanvas.popups.extra:
            if i == 1:  # the bar is full: level up
                GameCanvas.exp_bars[0] = 0
                GameCanvas.exp_bars[1] = i16(GameCanvas.exp_bars[1] - 100)
                if GameCanvas.exp_bars[1] < 0:
                    GameCanvas.exp_bars[1] = 0
                GameCanvas.exp_bars[2] = i16(GameCanvas.exp_bars[2] - 100)
                GameCanvas.exp_bar_step = 0
                GameCanvas.popups.extra = 1
                GameCanvas.popups.extra_w = 20
                GameCanvas.popups.extra_h = 12
                GameCanvas.hero.level += 1
                GameCanvas.hero.stat_points += 3
                GameCanvas.popup_lines[0] = "Level Up : Lv " + str(GameCanvas.hero.level)
                GameCanvas.popups.lines[5] = GameCanvas.popup_lines[0]
                GameCanvas.popups.popup_redraw = 1
                return
            if GameCanvas.popups.timer > 100:
                GameCanvas.popups.timer = 16

    def draw_exp_bar(self, paramInt1, paramInt2):  # e.java:2974-3017  (experience bar; 1 = full, 2 = done)
        arrayOfInt = [[GameCanvas.rgb(115, 142, 140), GameCanvas.rgb(181, 178, 181), 16777215],
                      [GameCanvas.rgb(99, 0, 0), GameCanvas.rgb(181, 0, 0), GameCanvas.rgb(247, 73, 0)],
                      [GameCanvas.rgb(0, 65, 255), GameCanvas.rgb(0, 146, 255), GameCanvas.rgb(0, 255, 173)],
                      [GameCanvas.rgb(247, 73, 0), GameCanvas.rgb(255, 162, 0), GameCanvas.rgb(255, 223, 0)]]
        if GameCanvas.state == 3:
            GameCanvas.view_y = i16(GameCanvas.view_y - 30)
        y = GameCanvas.view_cy + 37 + GameCanvas.view_y + 20
        arrayOfAc = [Rect(GameCanvas.view_cx - 51, y, 102, 7),
                     Rect(GameCanvas.view_cx - 50, y, GameCanvas.exp_bars[0], 7),
                     Rect(GameCanvas.view_cx - 50 + GameCanvas.exp_bars[0], y, GameCanvas.exp_bars[1] - GameCanvas.exp_bars[0], 7),
                     Rect(GameCanvas.view_cx - 50 + GameCanvas.exp_bars[1], y, 0, 7)]
        if GameCanvas.state == 3:
            GameCanvas.view_y = i16(GameCanvas.view_y + 30)
        b3 = 0
        b2 = 4 if paramInt2 != 0 else 3
        if GameCanvas.exp_bars[paramInt2] + paramInt1 * 4 > GameCanvas.exp_bars[paramInt2 + 1]:
            i = GameCanvas.exp_bars[paramInt2 + 1] - GameCanvas.exp_bars[paramInt2]
            b3 = 2
        else:
            i = paramInt1 * 4
        if GameCanvas.exp_bars[paramInt2] + i > 100:
            arrayOfAc[paramInt2 + 2].w = 100 - GameCanvas.exp_bars[paramInt2]
            b3 = 1
        else:
            arrayOfAc[paramInt2 + 2].w = i
        GameCanvas.fill_rect(arrayOfAc[0], 0)
        arrayOfAc[0].x += 1
        arrayOfAc[0].w = 100
        for b1 in range(b2):
            if arrayOfAc[b1].w > 0:
                for b in range(3):
                    arrayOfAc[b1].y += 1
                    arrayOfAc[b1].h -= 2
                    GameCanvas.fill_rect(arrayOfAc[b1], arrayOfInt[b1][b])
        return b3
