"""Menu screens (bb): every menu screen and its key routing
(a(), aB/aC/aD/aE = up/down/left/right, b() = fire, aF() = back).
"""
import re

import config
from pow.game import consts, hero_classes
from pow.game.arr_table import ArrTable
from pow.game.font import Font
from pow.game.game_canvas import GameCanvas
from pow.game.gfx import Gfx
from pow.game.name_buffer import NameBuffer
from pow.game.popups import RESPEC_DONE_POPUP, RESPEC_POPUP
from pow.game.res_reader import ResReader
from pow.game.scr_table import ScrTable
from pow.game.structs import Item, MissionDef, Point, Rect
from pow.midp import display
from pow.midp.jint import i8, i16, i32, idiv, imod



def ar_c(paramInt):  # (Assign Items: put potion slot cM[1] on key * (0) or # (1))
    hero = GameCanvas.hero
    if hero.quick_slots[GameCanvas.menu[1]].item != 0 and hero.quick_keys[paramInt] != GameCanvas.menu[1]:
        if GameCanvas.menu[1] == hero.quick_keys[paramInt + 1 & 0x1]:
            i = hero.quick_keys[paramInt]
            hero.quick_keys[paramInt] = hero.quick_keys[paramInt + 1 & 0x1]
            hero.quick_keys[paramInt + 1 & 0x1] = i
        else:
            hero.quick_keys[paramInt] = i8(GameCanvas.menu[1])
        return 1
    return 0


class Menus(GameCanvas):
    mix_table = None

    def __init__(self):
        super().__init__(GameCanvas.midlet)

    def draw_menu(self, mode):  # draw the current menu; 1 = first frame, 2 = animation
        menu = GameCanvas.menu
        if mode == 1:
            if menu[0] != 5:
                Gfx.set_font(GameCanvas.font_white)
                if GameCanvas.prev_state == 3:
                    Gfx.fill_rect(7, 19, 225, 242, 0)
                else:
                    self.draw_menu_frame()
                if menu[0] != 28:
                    if GameCanvas.prev_state == 3:
                        Gfx.set_font(GameCanvas.font_white)
                        self.draw_text_at(GameCanvas.menu_titles[menu[0]], 15, 0)
                    else:
                        self.draw_text_at(GameCanvas.menu_titles[menu[0]], 2 - GameCanvas.view_y, 0)
                else:
                    str_ = GameCanvas.split_field(GameCanvas.help_items[0], GameCanvas.help_topic)
                    if GameCanvas.prev_state == 3:
                        Gfx.set_font(GameCanvas.font_white)
                        self.draw_text_at(str_, 15, 0)
                    else:
                        self.draw_text_at(str_, 2 - GameCanvas.view_y, 0)
                if consts.menu_parent[menu[0]] != -1 or (consts.menu_parent[menu[0]] == -1 and menu[0] == 15):
                    if menu[0] == 3:
                        GameCanvas.draw_softkeys(11, 2)
                    elif menu[0] == 14:   # RESET the attributes (hero_classes)
                        GameCanvas.draw_softkeys(12, 2)
                    else:
                        GameCanvas.draw_softkeys(-1, 2)
            screen = menu[0]
            if screen == 0:
                GameCanvas.menu_scroll = 0
                GameCanvas.menu_anim = 0
                self.draw_game_menu()
            elif screen == 5:
                self.draw_title()
                self.draw_main_menu()
            elif screen in (1, 2, 10, 11, 12, 13, 25, 27):
                self.draw_list_menu()
            elif screen == 9:
                self.draw_options()
            elif screen == 28:
                self.draw_help_page()
            elif screen == 6:
                self.draw_hero_choice()
            elif screen == 7:
                self.draw_name_captions()
                self.draw_name_box()
            elif screen in (8, 14):
                self.draw_stat_sheet(1)
            elif screen == 29:
                self.draw_difficulty()
            elif screen == 15:
                self.draw_skills(0)
                self.draw_skill_info()
            elif screen == 16:
                self.draw_gear(menu[2], 0)
                self.draw_description_strip()
                GameCanvas.draw_softkeys(5, -1)
            elif screen == 17:
                self.draw_inventory(0)
                self.draw_description_strip()
                GameCanvas.draw_softkeys(5, -1)
            elif screen == 18:
                self.draw_assign_items(0)
                self.draw_description_strip()
            elif screen in (21, 22, 23, 24):
                self.draw_blacksmith(True)
                self.draw_description_strip()
            elif screen == 3:
                self.draw_mission_text()
            elif screen == 4:
                self.draw_briefing()
            elif screen == 19:
                self.draw_generals()
            elif screen == 20:
                self.draw_story_portraits(GameCanvas.story_picture)
                if GameCanvas.speech_pos[0] > 0:
                    Menus.type_speech(GameCanvas.story_page + 1 & 0x1, 0, 1)
                if GameCanvas.speech_pos[1] > 0:
                    Menus.type_speech(GameCanvas.story_page & 0x1, 0, 1)
            if GameCanvas.popups.kind != 0:
                GameCanvas.popups.draw_popup()
                return
        else:
            if mode == 2:
                screen = menu[0]
                if screen == 0:
                    self.draw_game_menu()
                    return
                if screen == 4:
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
                screen = menu[0]
                if screen == 0:
                    self.draw_game_menu()
                    return
                if screen == 5:
                    self.draw_title()
                    self.draw_main_menu()
                    return
                if screen == 7:
                    self.draw_name_box()
                    GameCanvas.draw_letter_grid(GameCanvas.letter_cursor, GameCanvas.view_cy + 32 + GameCanvas.view_y)
                    return
                if screen in (8, 14):
                    if GameCanvas.menu_part != 0:
                        self.draw_stat_sheet(0)
                        return
                    return
                if screen == 15:
                    if GameCanvas.menu_part != 0:
                        self.draw_skills(GameCanvas.menu_part)
                    self.draw_skill_info()
                    return
                if screen == 16:
                    self.draw_description_strip()
                    return
                if screen == 17:
                    if GameCanvas.menu_part != 0:
                        self.draw_inventory(1)
                    self.draw_description_strip()
                    return
                if screen == 18:
                    if GameCanvas.menu_part != 0:
                        self.draw_assign_items(1)
                    self.draw_description_strip()
                    return
                if screen in (21, 22, 23, 24):
                    self.draw_blacksmith(False)
                    self.draw_description_strip()
                    return
                if screen == 4:
                    self.tick_dialogue()
                    return
                if screen == 20:
                    self.tick_general_talk()
                    return

    def menu_keys(self):  # keys of the menus
        if GameCanvas.debug_keys:
            GameCanvas.score = -1
        screen = GameCanvas.menu[0]
        if screen == 4:
            return
        if screen == 7:
            i = GameCanvas.move_letter_cursor(GameCanvas.key)
            if i == -7:
                if len(GameCanvas.name_buf.get_text()) == 0:
                    GameCanvas.menu[0] = 6
                    GameCanvas.redraw = 1
                    return
                GameCanvas.name_buf.handle_key(-8)
                return
            if i in (-5, 53):
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
        if screen == 20:
            if GameCanvas.key != -5:
                GameCanvas.key = -999
                return
            return
        if screen in (21, 22, 23, 24):
            self.blacksmith_keys()
            return
        key = GameCanvas.key
        if key in (-1, 50):
            self.key_up()
            return
        if key in (-2, 56):
            self.key_down_arrow()
            return
        if key in (-3, 52):
            self.key_left()
            return
        if key in (-4, 54):
            self.key_right()
            return
        if key == 42:
            if GameCanvas.menu[0] == 18:
                GameCanvas.redraw = ar_c(0)
                return
        elif key == 35:
            if GameCanvas.menu[0] == 18:
                GameCanvas.redraw = ar_c(1)
                return
        elif key in (-5, 53):
            self.key_fire()
            return
        elif key == -6:
            if GameCanvas.menu[0] == 14:    # attribute reset
                self.open_respec()
                return
            if GameCanvas.menu[0] == 16 or GameCanvas.menu[0] == 17 or GameCanvas.menu[0] == 3:
                self.key_fire()
                return
        elif key == -7:
            self.key_back()

    @staticmethod
    def menu_link(menu, item):
        return consts.menu_links[menu][item]

    def key_up(self):  # UP
        menu = GameCanvas.menu
        screen = menu[0]
        if screen == 0:
            if GameCanvas.menu_scroll == 0:
                GameCanvas.redraw = 2
                GameCanvas.menu_scroll = -1
            return
        if screen in (3, 5, 6, 18, 20, 28):
            return
        if screen in (8, 14):
            self.draw_stat_cursor(0)
            menu[1] = menu[1] - 1
            if menu[1] < 0:
                menu[1] = GameCanvas.menu_count - 1
            self.draw_stat_cursor(1)
            return
        if screen == 9:
            menu[1] = menu[1] - 1
            if menu[1] < 1:
                menu[1] = GameCanvas.menu_count - 1
            if not GameCanvas.sound_on and menu[1] == 1:
                menu[1] = 0
            GameCanvas.clamp_menu_scroll()
            GameCanvas.redraw = 1
            return
        if screen == 15:
            if menu[3] == 2:
                if menu[1] < 4:
                    menu[2] = menu[2] - 3
                    if menu[2] < 0:
                        menu[2] = menu[2] + 18
                    GameCanvas.menu_part = 3
                GameCanvas.menu_part = 3
                return
            return
        if screen == 16:
            menu[2] = menu[2] + 1
            if menu[2] >= GameCanvas.menu_count:
                menu[2] = 0
            GameCanvas.redraw = 1
            return
        if screen == 17:
            menu[2] = menu[2] - 5
            if menu[2] < 0:
                menu[2] = menu[2] + config.BACKPACK_SIZE
            GameCanvas.menu_part = 1
            return
        if screen == 19:
            if menu[1] > 0:
                menu[1] = menu[1] - 1
                GameCanvas.redraw = 1
                return
            return
        if screen == 29:
            menu[1] = 1 - menu[1]
            GameCanvas.redraw = 1
            return
        if screen == 25:
            if menu[1] == 20:
                menu[1] = 23
            else:
                menu[1] = menu[1] - 1
            if menu[1] < menu[2]:
                menu[1] = menu[2] + 4
            GameCanvas.redraw = 1
            return
        menu[1] = menu[1] - 1
        if menu[1] < 0:
            menu[1] = GameCanvas.menu_count - 1
        GameCanvas.clamp_menu_scroll()
        GameCanvas.redraw = 1

    def key_down_arrow(self):  # DOWN
        menu = GameCanvas.menu
        screen = menu[0]
        if screen == 0:
            if GameCanvas.menu_scroll == 0:
                GameCanvas.menu_scroll = 1
                GameCanvas.redraw = 2
            return
        if screen in (3, 5, 6, 18, 20, 28):
            return
        if screen in (8, 14):
            self.draw_stat_cursor(0)
            menu[1] = menu[1] + 1
            if menu[1] >= GameCanvas.menu_count:
                menu[1] = 0
            self.draw_stat_cursor(1)
            return
        if screen == 9:
            menu[1] = menu[1] + 1
            if menu[1] >= GameCanvas.menu_count:
                menu[2] = 0
                menu[1] = 0
            if not GameCanvas.sound_on and menu[1] == 1:
                menu[1] = 2
            GameCanvas.clamp_menu_scroll()
            GameCanvas.redraw = 1
            return
        if screen == 15:
            if menu[3] == 2:
                if menu[1] < 4:
                    menu[2] = menu[2] + 3
                    if menu[2] > 17:
                        menu[2] = menu[2] - 18
                GameCanvas.menu_part = 3
                return
            return
        if screen == 16:
            menu[2] = menu[2] - 1
            if menu[2] < 0:
                menu[2] = GameCanvas.menu_count - 1
            GameCanvas.redraw = 1
            return
        if screen == 17:
            menu[2] = menu[2] + 5
            if menu[2] > config.BACKPACK_SIZE - 1:
                menu[2] = menu[2] - config.BACKPACK_SIZE
            GameCanvas.menu_part = 1
            return
        if screen == 19:
            if menu[1] < GameCanvas.menu_count - 1:
                menu[1] = menu[1] + 1
                GameCanvas.redraw = 1
                return
            return
        if screen == 29:
            menu[1] = 1 - menu[1]
            GameCanvas.redraw = 1
            return
        if screen == 25:
            if menu[1] == 23:
                menu[1] = 20
            else:
                menu[1] = menu[1] + 1
            if menu[1] > menu[2] + 4:
                menu[1] = menu[2]
            GameCanvas.redraw = 1
            return
        menu[1] = menu[1] + 1
        if menu[1] >= GameCanvas.menu_count:
            menu[2] = 0
            menu[1] = 0
        GameCanvas.clamp_menu_scroll()
        GameCanvas.redraw = 1

    def key_left(self):  # LEFT
        menu = GameCanvas.menu
        screen = menu[0]
        if screen == 1:
            if GameCanvas.debug_keys and GameCanvas.chapter > 0:
                GameCanvas.chapter = i8(GameCanvas.chapter - 1)
                self.load_chapter_lords()
                GameCanvas.redraw = 1
            return
        if screen == 3:
            if menu[2] > 0:
                menu[2] = menu[2] - 1
            else:
                menu[2] = GameCanvas.text_line_count[0] // 6
            GameCanvas.redraw = 1
            return
        if screen == 28:
            if menu[1] <= 0 and GameCanvas.help_topic == 8:
                menu[1] = 1
                GameCanvas.redraw = 1
                return
            GameCanvas.redraw = 1
            menu[1] = menu[1] - 1
            if menu[1] < 0:
                menu[1] = consts.help_topic_start[GameCanvas.help_topic + 1] - consts.help_topic_start[GameCanvas.help_topic] - 1
                return
            return
        if screen == 5:
            GameCanvas.redraw = 1
            menu[1] = menu[1] - 1
            if menu[1] < 0:
                menu[1] = 8
                return
            return
        if screen == 18:
            GameCanvas.menu_part = 1
            menu[1] = menu[1] - 1
            if menu[1] < 0:
                menu[1] = GameCanvas.menu_count - 1
                return
            return
        if screen == 6:
            GameCanvas.hero.head = GameCanvas.hero.head - 1 & 0x3
            GameCanvas.redraw = 1
            return
        if screen == 9:
            self.change_option(0)
            GameCanvas.redraw = 1
            return
        if screen == 15:
            slot = menu[3]
            menu[slot] = menu[slot] - 1
            if menu[3] == 1:
                if menu[slot] < 0:
                    menu[slot] = 4
                GameCanvas.menu_part = 2
                return
            if menu[1] < 4:
                if menu[slot] < 0:
                    menu[slot] = 17
            elif menu[slot] < 18:
                menu[slot] = 20
            GameCanvas.menu_part = 3
            return
        if screen == 16:
            GameCanvas.redraw = 1
            menu[2] = menu[2] + 1
            if menu[2] >= GameCanvas.menu_count:
                menu[2] = 0
                return
            return
        if screen == 17:
            menu[2] = menu[2] - 1
            if menu[2] < 0:
                menu[2] = GameCanvas.menu_count - 1
            GameCanvas.menu_part = 1
            return
        if screen == 19:
            menu[1] = menu[1] - 4
            menu[1] = max(menu[1], 0)
            GameCanvas.redraw = 1
            return
        if screen == 25:
            menu[2] = menu[2] - 5
            menu[1] = menu[1] - 5
            if menu[2] < 0:
                menu[2] = 20
                menu[1] = 20 + imod(menu[1] + 20, 5)
            GameCanvas.redraw = 1

    def key_right(self):  # RIGHT
        menu = GameCanvas.menu
        screen = menu[0]
        if screen == 1:
            if GameCanvas.debug_keys and GameCanvas.chapter < 44:
                GameCanvas.chapter = i8(GameCanvas.chapter + 1)
                self.load_chapter_lords()
                GameCanvas.redraw = 1
            return
        if screen == 3:
            if (menu[2] + 1) * 6 - 1 < GameCanvas.text_line_count[0]:
                menu[2] = menu[2] + 1
            else:
                menu[2] = 0
            GameCanvas.redraw = 1
            return
        if screen == 28:
            if menu[1] >= 1 and GameCanvas.help_topic == 8:
                GameCanvas.redraw = 1
                menu[1] = 0
                return
            GameCanvas.redraw = 1
            menu[1] = menu[1] + 1
            if menu[1] >= consts.help_topic_start[GameCanvas.help_topic + 1] - consts.help_topic_start[GameCanvas.help_topic]:
                menu[1] = 0
                return
            return
        if screen == 5:
            GameCanvas.redraw = 1
            menu[1] = menu[1] + 1
            if menu[1] >= 9:
                menu[1] = 0
                return
            return
        if screen == 18:
            menu[1] = menu[1] + 1
            if menu[1] >= GameCanvas.menu_count:
                menu[1] = 0
            GameCanvas.menu_part = 1
            return
        if screen == 6:
            GameCanvas.hero.head = GameCanvas.hero.head + 1 & 0x3
            GameCanvas.redraw = 1
            return
        if screen == 9:
            self.change_option(1)
            GameCanvas.redraw = 1
            return
        if screen == 15:
            slot = menu[3]
            menu[slot] = menu[slot] + 1
            if menu[3] == 1:
                if menu[slot] > 4:
                    menu[slot] = 0
                GameCanvas.menu_part = 2
                return
            if menu[1] < 4:
                if menu[slot] > 17:
                    menu[slot] = 0
            elif menu[slot] > 20:
                menu[slot] = 18
            GameCanvas.menu_part = 3
            return
        if screen == 16:
            GameCanvas.redraw = 1
            menu[2] = menu[2] - 1
            if menu[2] < 0:
                menu[2] = GameCanvas.menu_count - 1
                return
            return
        if screen == 17:
            menu[2] = menu[2] + 1
            if menu[2] >= GameCanvas.menu_count:
                menu[2] = 0
            GameCanvas.menu_part = 1
            return
        if screen == 19:
            menu[1] = menu[1] + 4
            if menu[1] >= GameCanvas.menu_count:
                menu[1] = GameCanvas.menu_count - 1
            GameCanvas.redraw = 1
            return
        if screen == 25:
            menu[2] = menu[2] + 5
            menu[1] = menu[1] + 5
            if menu[2] > 20:
                menu[2] = 0
                menu[1] = imod(menu[1], 5)
            GameCanvas.redraw = 1

    def key_fire(self):  # FIRE
        menu = GameCanvas.menu
        if menu[0] == 9:
            self.change_option(1)
            GameCanvas.redraw = 1
            return
        if menu[0] == 5:
            sel = menu[1]
            if sel == 4:
                GameCanvas.help_topic = 0
            elif sel == 5:
                GameCanvas.redraw = 1
                GameCanvas.menu_return = menu[0]
                menu[0] = 28
                menu[1] = 0
                menu[2] = 0
                GameCanvas.menu_items = GameCanvas.help_items
                GameCanvas.menu_before_talk = i16(GameCanvas.menu_return)
                GameCanvas.help_topic = 8
                return
            elif sel == 6:
                GameCanvas.popups.setup_popup(41)
                return
            elif sel == 7:
                GameCanvas.popups.setup_popup(42)
                return
            elif sel == 8:
                GameCanvas.popups.setup_popup(28)
                GameCanvas.redraw = 1
                return
            screen_of = [0, 1, 3, 4, 5]
            menu[1] = screen_of[menu[1]]
        if Menus.menu_link(menu[0], menu[1] % 7) > -1:
            self.enter_submenu()
            GameCanvas.menu_count = consts.menu_sizes[menu[0]]
            menu_id = menu[0]
            if menu_id == 7:
                GameCanvas.hero.name = ""
            elif menu_id == 9:
                GameCanvas.stop_sound()
            elif menu_id == 10:
                GameCanvas.menu_items = GameCanvas.yes_no_items
            elif menu_id == 12:
                GameCanvas.menu_items = GameCanvas.ok_items
            elif menu_id == 13:
                GameCanvas.menu_items = GameCanvas.continue_items
            elif menu_id == 27:
                GameCanvas.menu_items = GameCanvas.help_items
                GameCanvas.menu_before_talk = i16(GameCanvas.menu_return)
            elif menu_id == 28:
                GameCanvas.help_topic = i16(menu[1])
                GameCanvas.menu_count = consts.help_topic_start[GameCanvas.help_topic + 1] - consts.help_topic_start[GameCanvas.help_topic]
            elif menu_id == 14:
                GameCanvas.update_hero_stats()
            elif menu_id == 15:
                menu[3] = 1
                GameCanvas.images[37] = self.load_image(GameCanvas.scr_ui.get(44))
                GameCanvas.images[38] = self.load_image(GameCanvas.scr_ui.get(45))
            elif menu_id == 17:
                hero = GameCanvas.hero
                if GameCanvas.menu_return == 16 and hero.equipped[menu[2]].id != 0:
                    for b in range(config.BACKPACK_SIZE):
                        if hero.backpack[b].id == 0:
                            self.swap_items(hero.equipped[menu[2]], hero.backpack[b])
                self.compact_backpack()
            elif menu_id in (21, 22, 23, 24):
                self.enter_blacksmith()
            elif menu_id == 1:
                Menus.free_carousel()
                self.load_chapter_lords()
            elif menu_id == 3:
                GameCanvas.mission = i16(menu[1])
                self.load_mission_text()
            elif menu_id == 20:
                self.open_general_talk()
            menu[2] = 0
            menu[1] = 0
            return
        sel = menu[0]
        handler = self._FIRE_BY_MENU.get(sel)
        if handler is not None:
            handler(self, menu)

    def _fire_game_menu(self, menu):  # menu 0
        if menu[1] == 3:
            if GameCanvas.general_count == 0:
                GameCanvas.popups.setup_popup(35)
                return
            if GameCanvas.hero.live_registered != 0 and GameCanvas.general_count != 0:
                self.enter_submenu()
                menu[0] = 19
                GameCanvas.seal = i16(GameCanvas.backpack_slot_of(504))
                if GameCanvas.seal != 0:
                    Menus.seal_list()
                if GameCanvas.seal != 0:
                    GameCanvas.menu_count = 44
                else:
                    GameCanvas.menu_count = GameCanvas.general_count
                Menus.load_general_table()
                menu[2] = 0
                menu[1] = 0
                return
            GameCanvas.popups.setup_popup(35)
            GameCanvas.redraw = 0
            GameCanvas.menu_scroll = 0
            GameCanvas.menu_anim = 0
            return
        if menu[1] == 2:
            GameCanvas.live.open_live()
            GameCanvas.redraw = 0
            GameCanvas.menu_scroll = 0
            GameCanvas.menu_anim = 0
            return

    def _fire_title_menu(self, menu):  # menu 5
        GameCanvas.redraw = 1
        if menu[1] == 0:
            if GameCanvas.has_save():
                self.load_game()
                if GameCanvas.live_saved != 0:
                    return
                from pow.game.live_online import Online
                Online.on_game_start()       # log in to Live in the background
                GameCanvas.stop_sound()
                self.load_menu_frames()
                self.enter_submenu()
                GameCanvas.menu_anim = 0
                GameCanvas.menu_scroll = 0
                menu[0] = 0
                GameCanvas.menu_count = consts.menu_sizes[menu[0]]
                GameCanvas.menu_items = GameCanvas.game_menu_items
                menu[2] = 0
                menu[1] = 0
                self.load_hero_images()
                if GameCanvas.save_flag != 0:  # the save was made on the map: back into it
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
        if menu[1] == 1:
            GameCanvas.name_buf = None
            GameCanvas.name_buf = NameBuffer("", 8, 10)
            if GameCanvas.has_save():
                GameCanvas.popups.setup_popup(3)
                return
            self.start_new_game()
            return

    def _fire_stat_points(self, menu):  # menu 8/14
        if GameCanvas.hero.stat_points > 0:
            GameCanvas.menu_part = 1
            GameCanvas.hero.stat_points -= 1
            if menu[1] == 0:
                GameCanvas.hero.base_hp += 5
            elif menu[1] == 1:
                GameCanvas.hero.base_mp += 3
            elif menu[1] == 2:
                GameCanvas.hero.base_attack += 1
            elif menu[1] == 3:
                GameCanvas.hero.base_defense += 1
            if menu[0] == 8 and GameCanvas.hero.stat_points == 0:
                GameCanvas.popups.setup_popup(4)
                GameCanvas.redraw = 1
                return

    def _fire_difficulty(self, menu):  # menu 29
        GameCanvas.popups.setup_popup(36)

    def _fire_confirm(self, menu):  # menu 10
        if menu[1] == 2:
            GameCanvas.popups.setup_popup(5)
            return

    def _fire_save_menu(self, menu):  # menu 11
        if menu[1] == 0 and self.save_game() != 0:
            GameCanvas.popups.setup_popup(0)

    def _fire_endings(self, menu):  # menu 25
        if (GameCanvas.score & 1 << menu[1]) != 0:
            self.enter_submenu()
            self.start_story(menu[1], 0)
            return
        GameCanvas.popups.show_text("3You must first complete|the missions needed|to view this ending.")
        return

    def _fire_hotkeys(self, menu):  # menu 15
        hero = GameCanvas.hero
        if menu[3] == 1:
            if hero.hotkeys[menu[1]] != 0:
                menu[2] = consts.skill_menu_index[hero.hotkeys[menu[1]] - 12]
                hero.hotkeys[menu[1]] = 0
            elif menu[1] < 4:
                menu[2] = 0
            else:
                menu[2] = 18
            menu[3] = 2
            if menu[2] < 18:
                GameCanvas.menu_part = 6
                return
            GameCanvas.redraw = 1
            return
        if consts.skill_menu_ids[menu[2]] != 0:
            if hero.skill_levels[consts.skill_menu_ids[menu[2]] - 12] != 0:
                hero.hotkeys[menu[1]] = consts.skill_menu_ids[menu[2]]
                menu[3] = 1
            GameCanvas.menu_part = 6
            return

    def _fire_backpack(self, menu):  # menu 17
        hero = GameCanvas.hero
        it = hero.backpack[menu[2]]
        if it.id != 0:
            b = GameCanvas.item_slot_type(it.id)
            if GameCanvas.set_item_name(it.id) <= hero.level:
                if it.id == 434:
                    it.id = 0
                    hero.base_hp += 5
                    GameCanvas.popups.setup_popup(23)
                elif it.id == 435:
                    it.id = 0
                    hero.base_mp += 3
                    GameCanvas.popups.setup_popup(24)
                elif it.id == 436:
                    it.id = 0
                    hero.base_defense += 1
                    GameCanvas.popups.setup_popup(25)
                elif it.id == 437:
                    it.id = 0
                    hero.base_attack += 1
                    GameCanvas.popups.setup_popup(26)
                elif it.id in (502, 504):
                    GameCanvas.popups.setup_popup(17)
                else:
                    self.swap_items(it, hero.equipped[consts.equip_slot_order[b]])
            else:
                GameCanvas.popups.setup_popup(17)
        GameCanvas.menu_part = 1

    def _fire_lords(self, menu):  # menu 1
        if (GameCanvas.missions_done & 1 << GameCanvas.lord_ids[menu[1]] - 1) != 0:
            self.enter_submenu()
            menu[0] = 2
            GameCanvas.menu_count = consts.menu_sizes[menu[0]]
            GameCanvas.lord = i16(i8(menu[1]))
            self.load_lord_missions()
            menu[2] = 0
            menu[1] = 0
            return

    def _fire_missions(self, menu):  # menu 3
        GameCanvas.popups.setup_popup(6)

    _FIRE_BY_MENU = {  # menu -> handler, the branches of key_fire
        0: _fire_game_menu,
        5: _fire_title_menu,
        8: _fire_stat_points,
        14: _fire_stat_points,
        29: _fire_difficulty,
        10: _fire_confirm,
        11: _fire_save_menu,
        25: _fire_endings,
        15: _fire_hotkeys,
        17: _fire_backpack,
        1: _fire_lords,
        3: _fire_missions,
    }

    def key_back(self):  # BACK
        menu = GameCanvas.menu
        bool_ = False
        if consts.menu_parent[menu[0]] > -1:
            if menu[0] in (14, 15, 16, 17, 18):
                self.save_game()
            if consts.menu_parent[menu[0]] > 99:
                GameCanvas.help_topic = 0
                if menu[0] == 28 and GameCanvas.menu_return == 5:
                    GameCanvas.help_topic = 7
                    bool_ = True
                menu[0] = GameCanvas.menu_return
                if menu[0] == 0:
                    GameCanvas.menu_anim = 0
                    GameCanvas.menu_scroll = 0
                GameCanvas.restore_menu_cursor()
                GameCanvas.set_menu_items()
                if bool_:
                    menu[1] = 5
                    return
            else:
                if menu[0] == 1:
                    self.load_menu_frames()
                menu[0] = consts.menu_parent[menu[0]]
                if menu[0] == 0:
                    GameCanvas.menu_anim = 0
                    GameCanvas.menu_scroll = 0
                GameCanvas.restore_menu_cursor()
                GameCanvas.set_menu_items()
                if GameCanvas.menu_return == 5:
                    if menu[1] == 3:
                        menu[1] = 2
                    elif menu[1] == 4:
                        menu[1] = 3
                        if GameCanvas.prev_state == 3:  # back to the map's pause menu
                            GameCanvas.state = GameCanvas.prev_state
                            GameCanvas.prev_state = -1
                            menu[0] = 10
                            menu[1] = 4
                            GameCanvas.menu_count = 7
                            GameCanvas.menu_items = GameCanvas.pause_items
                            return
                    elif menu[1] == 5:
                        menu[1] = 4
                if GameCanvas.menu_return == 25:
                    menu[1] = 4
                if GameCanvas.menu_return == 27:
                    menu[1] = 3
                    if GameCanvas.prev_state == 3:
                        GameCanvas.state = GameCanvas.prev_state
                        GameCanvas.prev_state = -1
                        menu[0] = 10
                        menu[1] = 4
                        GameCanvas.menu_count = 7
                        GameCanvas.menu_items = GameCanvas.pause_items
                        return
        else:
            screen = menu[0]
            if screen == 0:
                GameCanvas.free_hero_images()
                Menus.free_carousel()
                self.free_menu_images()
                menu[0] = 5
                GameCanvas.menu_count = 10
                menu[2] = 0
                menu[1] = 0
                GameCanvas.popups.kind = 0
                GameCanvas.redraw = 1
                return
            if screen == 15:
                if menu[3] == 1:
                    menu[0] = 13
                    GameCanvas.restore_menu_cursor()
                    GameCanvas.images[37] = None
                    GameCanvas.images[38] = None
                    self.save_game()
                    return
                menu[3] = 1
                GameCanvas.menu_part = 6
                return
            if screen == 27:
                menu[0] = GameCanvas.menu_before_talk
                GameCanvas.restore_menu_cursor()
                GameCanvas.set_menu_items()

    @staticmethod
    def free_carousel():
        GameCanvas.anim_step = 0
        while GameCanvas.anim_step < 4:
            GameCanvas.images[26 + GameCanvas.anim_step] = None
            GameCanvas.anim_step += 1
        GameCanvas.carousel_image = None

    def enter_submenu(self):  # remember cursor, go to the sub-menu
        menu = GameCanvas.menu
        GameCanvas.menu_return = menu[0]
        GameCanvas.menu_cursors[menu[0]] = i16(menu[1])
        GameCanvas.menu_tops[menu[0]] = i16(menu[2])
        menu[0] = Menus.menu_link(menu[0], menu[1] % 7)
        GameCanvas.redraw = 1
        GameCanvas.menu_part = 0

    def free_shop_images(self):
        GameCanvas.images[17] = None
        GameCanvas.images[10] = None
        GameCanvas.gear_data = None
        GameCanvas.rare_data = None
        GameCanvas.treasure_data = None
        for b in range(1, 4):
            GameCanvas.images[0 + b] = None
        GameCanvas.sparkle = None
        Menus.free_carousel()

    def draw_menu_frame(self):  # menu background ct[7]
        self.draw_view_region(GameCanvas.images[7], 0, 0, GameCanvas.canvas_size.x, GameCanvas.canvas_size.y, 0, 0)

    def draw_list_menu(self):  # vertical list menu: 1 2 10 11 12 13 25 27
        menu = GameCanvas.menu
        i = GameCanvas.view_cx - 90
        text_dx = [13, 34, 20, 0, 0, 0, 0, 0, 0, 0,
                       12, 18, 12, 13, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 13, 0, 0]
        rows = min(GameCanvas.menu_count, 5)
        if menu[0] == 25 and menu[2] >= 20:
            rows = 4
            if menu[1] >= 24:
                menu[1] = 23
        row_y = GameCanvas.view_cy - idiv(rows * 30 - 10, 2)
        if GameCanvas.state == 3 or GameCanvas.prev_state == 3:
            row_y -= 30
        first_y = row_y
        b = text_dx[menu[0]]
        for row in range(rows):
            if menu[1] - menu[2] == row:
                bool_ = True
                Gfx.set_font(GameCanvas.font_orange)
            else:
                bool_ = False
                Gfx.set_font(GameCanvas.font_white)
            box_x = i
            self.draw_box(box_x, row_y + GameCanvas.view_y, 180, 20, bool_)
            if GameCanvas.state == 2:
                if menu[0] == 0:
                    if menu[2] + row == 3 and (GameCanvas.hero.live_registered == 0 or GameCanvas.general_count == 0):
                        Gfx.set_font(GameCanvas.font_gray)
                elif menu[0] == 1:
                    if GameCanvas.debug_keys:
                        GameCanvas.missions_done = -1
                    if (GameCanvas.missions_done & 1 << GameCanvas.lord_ids[menu[2] + row] - 1) == 0:
                        Gfx.set_font(GameCanvas.font_gray)
                elif menu[0] == 25 and (GameCanvas.score & 1 << menu[2] + row) == 0:
                    Gfx.set_font(GameCanvas.font_gray)
            elif GameCanvas.map_mode.mode == 1 and menu[2] + row == 2 and (GameCanvas.actor_count > 0 or GameCanvas.boss_fight != 0 or GameCanvas.waves[0] != 0):
                Gfx.set_font(GameCanvas.font_gray)
            if menu[0] == 25:
                if menu[2] + row < 24:
                    utf = self.edat_bytes(54, 38 + menu[2] + row)
                    str_ = GameCanvas.read_utf(utf, 0, len(utf))
                    self.draw_text_at(str_, row_y - 1, 18)
            elif menu[0] in (0, 10, 12, 13, 27):
                self.draw_text_at(GameCanvas.split_field(GameCanvas.menu_items[0], row + menu[2]), row_y - 1, 0)
            else:
                self.draw_text_at(GameCanvas.menu_items[row + menu[2]], row_y - 1, b)
            row_y += 30
        if menu[0] == 25:
            self.draw_page_number(menu[2] // 5 + 1, 5, GameCanvas.canvas_size.y - 35, True)
        elif menu[2] != 0 or menu[2] + 5 < GameCanvas.menu_count - 1:
            self.draw_arrow(2, GameCanvas.view_cx - 8 - GameCanvas.view_x, first_y - 10 - 5)
            self.draw_arrow(3, GameCanvas.view_cx - 8 - GameCanvas.view_x, row_y - 5)
        if menu[0] == 10:
            Gfx.draw_image_anchored(GameCanvas.softkey_bg, 120, GameCanvas.view_y + 15, 17)
            Gfx.set_font(GameCanvas.font_white)
            self.draw_text_at("PAUSE", 13, 0)
        if GameCanvas.debug_keys and menu[0] == 1:
            Gfx.set_font(GameCanvas.font_white)
            Gfx.fill_rect(GameCanvas.screen_w // 2 - 16, GameCanvas.screen_h - 17, 32, 17, 0)
            Gfx.draw_string("" + str(GameCanvas.chapter + 1), GameCanvas.screen_w // 2, GameCanvas.screen_h - 16, 1)

    def draw_options(self):  # Options: Sound / Volume / Speed
        i = GameCanvas.view_cy - 50
        if GameCanvas.menu[1] == 0:
            GameCanvas.menu[1] = 1
        for b in range(1, consts.menu_sizes[9]):         # config.SCREEN_OPTION: + row 3 Screen
            if GameCanvas.menu[1] == b:
                bool_ = True
                Gfx.set_font(GameCanvas.font_orange)
            elif b == 3 and not config.SCREEN_OPTION:
                bool_ = False
                Gfx.set_font(GameCanvas.font_gray)
            else:
                bool_ = False
                Gfx.set_font(GameCanvas.font_white)
            self.draw_box(GameCanvas.view_cx - 100, i + GameCanvas.view_y, 80, 20, bool_)
            self.draw_box(GameCanvas.view_cx - 10, i + GameCanvas.view_y, 110, 20, bool_)
            name = "Screen" if b == 3 and config.SCREEN_OPTION else GameCanvas.option_names[b]
            GameCanvas.draw_view_text_centred(name, GameCanvas.view_cx - 100 + 40 - GameCanvas.view_x, i + 1)
            if bool_:
                self.draw_arrow(0, GameCanvas.view_cx - 10 - GameCanvas.view_x, i + 2)
                self.draw_arrow(1, GameCanvas.view_cx - 10 + 110 - 10 - 1 - GameCanvas.view_x, i + 2)
            if b == 0:
                str_ = GameCanvas.on_off[1 if GameCanvas.sound_on else 0]
            elif b == 1:
                str_ = ""
                for bar in range(GameCanvas.volume // 25):
                    str_ = str_ + "I"
                if str_ == "":
                    str_ = "OFF"
            elif b == 2:
                str_ = GameCanvas.speed_names[GameCanvas.speed]
            elif b == 3 and config.SCREEN_OPTION:
                str_ = "Full" if display.is_fullscreen() else "Window"
            elif b == 3:
                str_ = consts.difficulty_names[GameCanvas.difficulty]
            else:
                return
            GameCanvas.draw_view_text_centred(str_, GameCanvas.view_cx + 156 - 111 - GameCanvas.view_x, i + 1)
            i += 10
            i += 20

    def draw_help_page(self):  # Help / About page cM[1] of topic ej
        if GameCanvas.state == 3 or GameCanvas.prev_state == 3:
            GameCanvas.view_cy -= 30
        i = GameCanvas.menu[1] + consts.help_topic_start[GameCanvas.help_topic]
        text = self.edat_bytes(61, i)
        if GameCanvas.state == 2:
            self.word_wrap(text, 190, 0)
            self.draw_grey_frame(GameCanvas.view_cx - 100 + GameCanvas.view_x, GameCanvas.view_cy - 90 + GameCanvas.view_y, 200, 175)
        else:
            self.word_wrap(text, 190, 0)
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
        pages = consts.help_topic_start[GameCanvas.help_topic + 1] - consts.help_topic_start[GameCanvas.help_topic]
        if GameCanvas.state == 2:
            if GameCanvas.prev_state == 3:
                self.draw_page_number(GameCanvas.menu[1] + 1, pages, GameCanvas.canvas_size.y - 100, True)
            else:
                self.draw_page_number(GameCanvas.menu[1] + 1, pages, GameCanvas.canvas_size.y - 35, True)
        else:
            self.draw_page_number(GameCanvas.menu[1] + 1, pages, GameCanvas.view_cy + 65, True)
        if GameCanvas.state == 3 or GameCanvas.prev_state == 3:
            GameCanvas.view_cy += 30

    def draw_page_number(self, page, pages, y, wrap):  # page "n / m" with arrows
        if pages == 1:
            return
        i = GameCanvas.view_cx - 25 - 10
        if pages > 1:
            if page != 1 or wrap:
                self.draw_arrow(0, i, y)
            i += 60
            if page != pages or wrap:
                self.draw_arrow(1, i, y)
        y += 2
        i = GameCanvas.view_cx - (8 + 9 * ((2 if pages > 9 else 1) + (2 if page > 9 else 1)) + 2) // 2
        i = i + (18 if page > 9 else 9)
        self.draw_small_number(page, i, y + GameCanvas.view_y)
        i += 1
        if GameCanvas.prev_state == 3:
            GameCanvas.draw_region(i - GameCanvas.view_x, y + 16, 8, 12, GameCanvas.images[20], 90, 0)
        else:
            GameCanvas.draw_region(i - GameCanvas.view_x, y, 8, 12, GameCanvas.images[20], 90, 0)
        i += 9 + (18 if pages > 9 else 9)
        self.draw_small_number(pages, i, y + GameCanvas.view_y)

    def draw_skills(self, mode):  # Skills: 5 hot-key slots + skill tree pages
        hero = GameCanvas.hero
        menu = GameCanvas.menu
        slot_keys = [1, 3, 7, 9, 0]
        if config.SKILL_BAR or config.SKILL_CARD:
            # the PC keys of the 5 slots are 1-5 (the phone's were 1 3 7 9 0)
            slot_keys = [1, 2, 3, 4, 5]
        if mode == 0:
            for b in range(5):
                self.draw_empty_slot(40 + b * 30 + 4 * b, 60)
                self.draw_big_number(slot_keys[b], 40 + b * 30 + 18 + 4 * b, 70, 0)
        if mode % 2 == 0:
            for b in range(5):
                self.draw_empty_slot(40 + b * 30 + 4 * b, 90)
                if hero.hotkeys[b] != 0:
                    self.draw_map_region(GameCanvas.images[37], 40 + b * 30 + 4 * b + 1, 91, 28, 28, (hero.hotkeys[b] - 12) * 28, 0)
            self.draw_round_outline(40 + menu[1] * 30 + 4 * menu[1], 90, 30, 30, 255, 255, 255)
        boxes = [Rect(40, 140, 60, 20), Rect(40, 165, 60, 20)]
        if mode % 3 == 0:
            i = menu[2] // 6 << 1
            lines = 2 if menu[2] < 18 else 1
            for line in range(lines):
                base = menu[2] // 6 * 6 + line * 3
                box = boxes[line]
                box.y = box.y + line * 10 + 5
                self.draw_round_outline(box.x - 1, box.y - 1, box.w + 2, box.h + 2, 152, 152, 152)
                GameCanvas.fill_rect(box, 0)
                Gfx.set_font(GameCanvas.font_white)
                GameCanvas.text_width = GameCanvas.measure_text(GameCanvas.skill_names[i + line])
                GameCanvas.draw_view_text(GameCanvas.skill_names[i + line], box.x + idiv(box.w - GameCanvas.text_width, 2), box.y + 1)
                for b in range(3):
                    self.draw_empty_slot(40 + (b + 2) * 34, 140 + 35 * line)
                    if consts.skill_menu_ids[base + b] != 0:
                        if hero.skill_levels[consts.skill_menu_ids[base + b] - 12] != 0:
                            image = GameCanvas.images[37]
                        else:
                            image = GameCanvas.images[38]
                        self.draw_map_region(image, 40 + (b + 2) * 34 + 1, 140 + 35 * line + 1, 28, 28,
                                       (consts.skill_menu_ids[base + b] - 12) * 28, 0)
            if menu[3] == 2:
                row = 35 * (menu[2] % 6 // 3)
                self.draw_round_outline(40 + (menu[2] % 3 + 2) * 34, 140 + row, 30, 30, 255, 255, 255)
            bar = Rect(210, 0, 3, 20)
            self.draw_box(210, 150, 3, 50, False)
            if i == 6:
                bar.x = 210
                bar.y = 152
                bar.w = 3
                bar.h = 46
                GameCanvas.fill_rect(bar, GameCanvas.rgb(231, 227, 198))
            else:
                bar.y = 151 + (i >> 1) * 14 + GameCanvas.view_y
                GameCanvas.fill_rect(bar, GameCanvas.rgb(231, 227, 198))
        # System.out.println("GameCanvas.DrawSkillSet(2)");
        if menu[3] == 1:
            self.draw_description(hero.hotkeys[menu[1]] + 2000, GameCanvas.view_cx - 100, GameCanvas.canvas_size.y - 70, 200, 22)
        else:
            self.draw_description(consts.skill_menu_ids[menu[2]] + 2000, GameCanvas.view_cx - 100, GameCanvas.canvas_size.y - 70, 200, 22)
        GameCanvas.menu_part = 0

    def draw_skill_info(self):
        """Skills menu (cM[0] == 15): the description strip, or (config.SKILL_CARD)
        the skill card of pow/game/skill_bar.py for the slot / tree skill under the cursor."""
        if not config.SKILL_CARD:
            self.draw_description_strip()
            return
        from pow.game import skill_bar
        menu = GameCanvas.menu
        skill = GameCanvas.hero.hotkeys[menu[1]] if menu[3] == 1 else consts.skill_menu_ids[menu[2]]
        skill_bar.draw_card(skill)

    def draw_description_strip(self):  # description strip; scrolls when longer than the box
        info = GameCanvas.info_box
        if config.WIDE_DESC:
            self.draw_wide_description()
            return
        self.draw_box(info.rect.x + GameCanvas.view_x, info.rect.y + GameCanvas.view_y, info.rect.w, info.rect.h, False)
        Gfx.set_font(GameCanvas.font_white)
        if info.shown != 0:
            GameCanvas.text_width = GameCanvas.measure_text(info.text)
            info.text_x = i16(info.text_x - 5)
            if info.rect.x - info.text_x > GameCanvas.text_width + 3:
                info.text_x = i16(info.rect.x + info.rect.w)
        GameCanvas.draw_view_text(info.text, info.text_x, info.rect.y + (info.rect.h - 11 >> 1) - 2)
        i = (GameCanvas.screen_w - info.rect.w) // 2
        strip_y = info.rect.y + GameCanvas.view_y
        view_x = 0
        view_y = 0
        if GameCanvas.state == 3:
            view_x = GameCanvas.view_x
            view_y = GameCanvas.view_y
            Gfx.fill_rect(0, strip_y, i, info.rect.h, 0)
            Gfx.fill_rect(GameCanvas.screen_w - i, strip_y, i, info.rect.h, 0)
        self.draw_view_region(GameCanvas.images[7], 0, strip_y, i, info.rect.h, -view_x, strip_y - view_y)
        Gfx.draw_line(i - 1, strip_y, i - 1, strip_y + info.rect.h - 1, GameCanvas.rgb(80, 80, 80))
        self.draw_view_region(GameCanvas.images[7], GameCanvas.screen_w - i, strip_y, i - view_x, info.rect.h, GameCanvas.screen_w - i - view_x, strip_y - view_y)
        Gfx.draw_line(GameCanvas.screen_w - i, strip_y, GameCanvas.screen_w - i, strip_y + info.rect.h - 1, GameCanvas.rgb(80, 80, 80))
        if GameCanvas.state == 3:
            Gfx.push_clip(0, strip_y, GameCanvas.screen_w, info.rect.h)
            GameCanvas.scene.draw_hud_frame()
            Gfx.pop_clip()
            Gfx.push_clip(0, strip_y, i - 1, info.rect.h)
            GameCanvas.popups.draw_popup_frame(170)
            Gfx.pop_clip()
            Gfx.push_clip(GameCanvas.screen_w - i + 1, strip_y, i - 1, info.rect.h)
            GameCanvas.popups.draw_popup_frame(170)
            Gfx.pop_clip()

    # (config.WIDE_DESC): the description of an item / skill / potion in a box as wide
    # as the screen, in up to WIDE_DESC_LINES lines, instead of the narrow strip whose one line
    # runs by. The box always has the same size, so a shorter text leaves nothing behind.
    WIDE_DESC_X = 4
    WIDE_DESC_LINE = 14

    @staticmethod
    def wide_description_lines(text, width):
        """The parts of the description (" / " between them) packed into lines of `width` px;
        a part longer than a line is broken between words."""
        measure = GameCanvas.measure_text
        lines = []
        for raw in re.split(r"\s*/\s+", text):
            part = raw.strip()
            if not part:
                continue
            if lines and measure(lines[-1] + " / " + part) <= width:
                lines[-1] += " / " + part
                continue
            line = ""
            for word in part.split(" "):
                if line and measure(line + " " + word) > width:
                    lines.append(line)
                    line = word
                else:
                    line = (line + " " + word) if line else word
            if line:
                lines.append(line)
        return lines

    def draw_wide_description(self):
        info = GameCanvas.info_box
        if info.rect.w == 0 and info.rect.h == 0:
            return
        x = Menus.WIDE_DESC_X
        w = GameCanvas.screen_w - 2 * x
        Gfx.set_font(GameCanvas.font_white)
        lines = Menus.wide_description_lines(info.text, w - 8)
        # a longer text grows the box (up to WIDE_DESC_MAX_LINES rows): nothing runs by
        rows = min(config.WIDE_DESC_MAX_LINES, max(config.WIDE_DESC_LINES, len(lines)))
        lines = lines[:rows]
        h = rows * Menus.WIDE_DESC_LINE + 6
        y = info.rect.y + GameCanvas.view_y
        bottom = GameCanvas.screen_h - 20           # above the soft-key bar (BACK)
        if y + h > bottom:
            y = bottom - h
        self.draw_box(x, y, w, h, False)
        if GameCanvas.popups.kind != 0:            # a popup covers the top of the box only
            return
        for idx, line in enumerate(lines):
            Gfx.draw_string(line, x + 4, y + 3 + idx * Menus.WIDE_DESC_LINE, 0)

    def draw_gear(self, slot, describe):  # Gear: hero sprite + 9 equipment slots
        hero = GameCanvas.hero
        slot_dx = [-77, -77, -77, -33, 3, 47, 47, 47, -15]
        slot_dy = [21, -15, -51, -79, -79, -51, -15, 21, 49]
        GameCanvas.images[39] = self.load_image(GameCanvas.scr_ui.get(50))
        back = GameCanvas.images[39]
        self.draw_map_region(back, GameCanvas.view_cx - back.getWidth() // 2, GameCanvas.view_cy - back.getHeight() // 2,
                       back.getWidth(), back.getHeight(), 0, 0)
        GameCanvas.images[39] = None
        for b in range(9):
            if hero.equipped[b].id != 0:
                self.load_item_def(hero.equipped[b].id)
                self.draw_item_icon(hero.equipped[b].id, GameCanvas.view_cx + slot_dx[b], GameCanvas.view_cy + slot_dy[b], 0)
        self.draw_round_outline(GameCanvas.view_cx + slot_dx[slot] - 1, GameCanvas.view_cy + slot_dy[slot] - 1, 30, 30, 255, 255, 255)
        GameCanvas.cursor[24] = GameCanvas.view_cx + slot_dx[slot] + GameCanvas.view_x + 7
        GameCanvas.cursor[25] = GameCanvas.view_cy + slot_dy[slot] + GameCanvas.view_y + 7
        body = hero.body_frames[1]
        self.draw_map_region(hero.body_image, GameCanvas.view_cx - body.ox, GameCanvas.view_cy + 7 - body.oy + 17, body.w, body.h, body.src_x, body.src_y)
        head = hero.head_frames[1]
        self.draw_map_region(hero.head_image, GameCanvas.view_cx - head.ox, GameCanvas.view_cy + 7 - head.oy + 17, head.w, head.h, head.src_x, head.src_y)
        if describe != 0:
            GameCanvas.describe_shop_item(self.item_under_cursor(-1), True, -1)
            return
        self.draw_description(slot + 1000, GameCanvas.view_cx - 79, GameCanvas.view_cy + 81 + 5, 158, 20)

    def draw_inventory(self, mode):  # Inventory: 5x5 grid in 2 pages + gold
        hero = GameCanvas.hero
        menu = GameCanvas.menu
        col_x = [GameCanvas.view_cx - 75, GameCanvas.view_cx - 45, GameCanvas.view_cx - 15, GameCanvas.view_cx + 15, GameCanvas.view_cx + 45]
        row_y = [GameCanvas.view_cy - 45, GameCanvas.view_cy - 15, GameCanvas.view_cy + 15]
        bar = Rect(GameCanvas.view_cx + 80, GameCanvas.view_cy - 40, 5, 80)
        # config.BACKPACK_SIZE: pages of 3 rows (15 cells), the last one may be shorter;
        # with 25 cells this is the original's 3 + 2 rows
        pages = (config.BACKPACK_SIZE + 14) // 15
        page = menu[2] // 15
        first = page * 15
        rows = min(3, (config.BACKPACK_SIZE - first) // 5)
        if mode != 0:
            self.draw_map_region(GameCanvas.images[7], GameCanvas.view_cx - 75, GameCanvas.view_cy - 45, 150, 100, GameCanvas.view_cx - 75, GameCanvas.view_cy - 45)
        for row in range(rows):
            for b in range(5):
                self.draw_empty_slot(col_x[b] + GameCanvas.view_x, row_y[row] + GameCanvas.view_y)
                self.load_item_def(hero.backpack[first + row * 5 + b].id)
                self.draw_item_icon(hero.backpack[first + row * 5 + b].id, col_x[b] + 1, row_y[row] + 1, 0)
        GameCanvas.fill_rect(bar, GameCanvas.rgb(148, 148, 148))
        bar.x += 1
        bar.y += 1
        bar.w -= 2
        bar.h -= 2
        GameCanvas.fill_rect(bar, GameCanvas.rgb(33, 0, 0))
        bar.h = 78 // pages
        bar.y = GameCanvas.view_cy - 39 + page * 78 // pages + GameCanvas.view_y
        GameCanvas.fill_rect(bar, GameCanvas.rgb(231, 227, 198))
        self.draw_description(menu[2] + 1100, GameCanvas.view_cx - 75, GameCanvas.view_cy + 50, 150, 22)
        self.draw_round_outline(col_x[menu[2] % 5], row_y[(menu[2] - first) // 5] + GameCanvas.view_y, 30, 30, 255, 255, 255)
        if mode == 0:
            self.draw_gold_box()
        GameCanvas.menu_part = 0

    def draw_assign_items(self, mode):  # Assign Items: 5 potion slots, * and # quick keys
        hero = GameCanvas.hero
        if GameCanvas.state == 3:
            GameCanvas.view_cy -= 30
        if mode == 0:
            self.draw_gold_box()
            Gfx.set_font(GameCanvas.font_white)
            for slot in range(5):
                self.draw_box(GameCanvas.view_cx - 80 + 32 * slot, GameCanvas.view_cy - 40 + GameCanvas.view_y, 30, 22, False)
                if config.SKILL_BAR:
                    # config.SKILL_BAR: every belt slot has its own key Z X C V B
                    GameCanvas.draw_view_text(" " + "ZXCVB"[slot] + " ", GameCanvas.view_cx - 80 + 32 * slot - GameCanvas.view_x, GameCanvas.view_cy - 38)
                elif hero.quick_keys[0] == slot:
                    GameCanvas.draw_view_text(" * ", GameCanvas.view_cx - 80 + 32 * slot - GameCanvas.view_x, GameCanvas.view_cy - 38)
                elif hero.quick_keys[1] == slot:
                    GameCanvas.draw_view_text(" # ", GameCanvas.view_cx - 80 + 32 * slot - GameCanvas.view_x, GameCanvas.view_cy - 38)
        for b in range(5):
            if GameCanvas.state == 3:
                self.draw_box(GameCanvas.view_cx - 79 + 32 * b, GameCanvas.view_cy + 6, 28, 28, False)
                self.draw_item_icon(hero.quick_slots[b].item, GameCanvas.view_cx - 79 + 32 * b - GameCanvas.view_x, GameCanvas.view_cy + 6 - GameCanvas.view_y, b)
            else:
                self.draw_box(GameCanvas.view_cx - 79 + 32 * b, GameCanvas.view_cy - 10, 28, 28, False)
                self.draw_item_icon(hero.quick_slots[b].item, GameCanvas.view_cx - 79 + 32 * b - GameCanvas.view_x, GameCanvas.view_cy - 10 - GameCanvas.view_y, b)
        if GameCanvas.state == 3:
            self.draw_round_outline(GameCanvas.view_cx - 80 + 32 * GameCanvas.menu[1], GameCanvas.view_cy + 6, 30, 29, 255, 255, 255)
        else:
            self.draw_round_outline(GameCanvas.view_cx - 80 + 32 * GameCanvas.menu[1], GameCanvas.view_cy - 10, 30, 29, 255, 255, 255)
        GameCanvas.menu_part = 0
        # config.WIDE_DESC: the taller box goes under "*,# key Assign", not over it
        self.draw_description(GameCanvas.menu[1] + 1200, GameCanvas.view_cx - 80 - GameCanvas.view_x,
                              GameCanvas.view_cy + (88 if config.WIDE_DESC else 30), 160, 22)
        self.draw_box(GameCanvas.view_cx - 80, GameCanvas.view_cy + 60 + GameCanvas.view_y, 160, 22, False)
        Gfx.set_font(GameCanvas.font_white)
        self.draw_text_at("Keys Z X C V B" if config.SKILL_BAR else "*,# key Assign", GameCanvas.view_cy + 60, 15)
        if GameCanvas.state == 3:
            GameCanvas.view_cy += 30

    def draw_item_icon(self, item_id, x, y, slot):  # item icon
        i = -1
        b = 0
        if item_id > 500:
            i = item_id - 501
            b = 3
        elif item_id > 300:
            i = GameCanvas.treasure_def.icon
            b = 2
        elif item_id > 100:
            i = GameCanvas.gear_def.icon
            b = 1
        elif item_id > 0:
            i = item_id - 1
            b = 0
        if i > -1:
            self.draw_map_region(GameCanvas.images[0 + b], x, y, 28, 28, i * 28, 0)
            if item_id < 100:
                self.draw_small_digit(x, y + 2, GameCanvas.hero.quick_slots[slot].count)

    # ---- Blacksmith (screens 21 Buy, 22 Sell, 23 Enchant, 24 Combine) ----------------------
    # fK[0] = mode (cM[0]-21), fK[9]/fK[10] = cursor col/row, fK[18] = cell, fK[19] = item id,
    # fK[20] = message for aV(), fK[21] = price, fK[26] = sparkle frame (-1 idle), fK[27] = 1 on Gear

    def draw_item_grid(self, y, items, marks):  # item grid
        i = GameCanvas.cursor[8] * 5
        if GameCanvas.cursor[11] == 1:
            frame = Rect(0, 0, 0, 0)
            bar = Rect(0, 0, 0, 0)
            frame.w = 4
            frame.x = GameCanvas.cursor[12]
            frame.h = GameCanvas.cursor[6]
            frame.y = y
            GameCanvas.draw_filled_rect(frame, 16777215, 0)
            frame.w -= 2
            frame.x += 1
            frame.h -= 2
            frame.y += 1
            cell_x = GameCanvas.cursor[8] * 32
            bar_h = bar.h
            cell_x = idiv(cell_x * bar_h, GameCanvas.cursor[7])
            bar.h = GameCanvas.cursor[13]
            bar.y += cell_x
            GameCanvas.fill_rect(bar, 16777215)
            GameCanvas.outline_rect(frame, 10000536)
        y += 1
        cell = 0
        marked = 0
        while cell < GameCanvas.cursor[3]:
            cell_x = GameCanvas.cursor[5]
            for b in range(5):
                if i == GameCanvas.cursor[18]:
                    bool_ = True
                    GameCanvas.cursor[24] = cell_x + 13 + 1
                    GameCanvas.cursor[25] = y + 13 + 1
                else:
                    bool_ = False
                for j in range(GameCanvas.combine_slots[3]):
                    if GameCanvas.combine_slots[j] == i:
                        bool_ = True
                        GameCanvas.combine_pos[marked].x = i16(cell_x + 13 + 1)
                        GameCanvas.combine_pos[marked].y = i16(y + 13 + 1)
                        marked += 1
                        break
                self.draw_grid_cell(cell_x, y, bool_)
                if marks is not None:
                    self.draw_item_count_icon(marks[i], cell_x, y, 0)
                else:
                    self.draw_grid_item(i, cell_x, y, items)
                cell_x += 32
                i += 1
            y += 32
            cell += 1

    def draw_grid_item(self, index, x, y, items):
        if items is not None:
            item = items[index]
        else:
            item = self.item_under_cursor(index)
        if GameCanvas.cursor[0] == 1 and 0 < item.id < 100:
            bool_ = item.attack
        else:
            bool_ = 0
        self.draw_item_count_icon(item.id, x, y, bool_)

    def draw_grid_cell(self, x, y, selected):  # grid cell frame
        GameCanvas.draw_frame_box(x + 1, y + 1, 26, 26, 0, 0, 16777215 if selected else 5263440, True)

    def draw_item_count_icon(self, item_id, x, y, count):  # item icon by id + count
        if item_id > 500:
            image = GameCanvas.images[3]
            i = item_id - 501
        elif item_id > 300:
            image = GameCanvas.images[2]
            i = GameCanvas.item_tables[1].get_int(item_id - 301, 7)
        elif item_id > 100:
            image = GameCanvas.images[1]
            i = GameCanvas.item_tables[0].get_int(item_id - 101, 7)
        else:
            image = GameCanvas.images[0]
            i = item_id - 1
        GameCanvas.draw_region(x, y, 28, 28, image, i * 28, 0)
        if count > 0:
            GameCanvas.draw_region(x, y, 9, 12, GameCanvas.images[20], count * 9, 0)

    def draw_shop_grid(self):  # gold + item grid + description
        i = GameCanvas.cursor[1] + 1
        self.draw_hero_gold(i)
        i += 29
        self.draw_item_grid(i, None, None)
        GameCanvas.describe_shop_item(self.item_under_cursor(-1), True, -1)

    def draw_blacksmith(self, full):
        cursor = GameCanvas.cursor
        if full:
            if cursor[27] == 0:
                self.draw_shop_grid()
            else:
                self.draw_gear(cursor[18], 1)
            if cursor[23] == -1 and GameCanvas.popups.kind == 0:
                # the Yes/No popup of Enchant / Combine has just closed
                cursor[23] = 0
                if GameCanvas.key == -5 and GameCanvas.popups.button == 0:
                    if cursor[21] > GameCanvas.hero.gold:
                        cursor[20] = 4
                        Menus.blacksmith_message()
                        Menus.clear_combine()
                    else:
                        cursor[26] = 0          # start the sparkle, the action follows below
                else:
                    Menus.clear_combine()
        if cursor[26] == -1:
            return
        if cursor[26] < 5:
            self.draw_sparkles()
            cursor[26] += 1
            return
        cursor[26] = -1
        GameCanvas.redraw = 1
        if cursor[0] == 2:
            self.roll_enchant()
        elif cursor[0] == 3:
            hero = GameCanvas.hero
            if cursor[22] == 0:
                for b in range(3):
                    Item.clear(hero.backpack[GameCanvas.combine_slots[b]])
                dst = hero.backpack[GameCanvas.combine_slots[2]]
                dst.id = GameCanvas.combine_result.id
                dst.attack = GameCanvas.combine_result.attack
                dst.defense = GameCanvas.combine_result.defense
                dst.hp = GameCanvas.combine_result.hp
                dst.mp = GameCanvas.combine_result.mp
                dst.enchant = GameCanvas.combine_result.enchant
            elif cursor[31] != -1:
                Item.clear(hero.backpack[cursor[31]])
                cursor[31] = -1
            Menus.clear_combine()
            cursor[20] = 9
            hero.gold -= cursor[21]
        self.save_game()
        Menus.blacksmith_message()

    def roll_enchant(self):  # Enchant: roll success / fail / lost
        success_pct = [100, 90, 80, 70, 60, 45, 30, 10, 1]
        lost_pct = [0, 10, 20, 40, 50, 60, 70, 80, 90]
        item = self.item_under_cursor(-1)
        GameCanvas.cursor[20] = 2
        GameCanvas.hero.gold -= GameCanvas.cursor[21]
        if GameCanvas.cursor[22] == -1:
            GameCanvas.cursor[23] = 2
        else:
            i = self.rand(100) + 1
            if i > success_pct[item.enchant]:
                i = self.rand(100)
                GameCanvas.cursor[23] = 2 if i <= lost_pct[item.enchant] else 1
            else:
                self.enchant_item(item, 1)
                GameCanvas.cursor[23] = 0
        if GameCanvas.cursor[23] == 2:
            Item.clear(item)
            GameCanvas.cursor[23] = 1

    def draw_sparkle(self, x, y):  # sparkle frame
        src_x = [0, 15, 30, 0, 20]
        src_y = [0, 0, 0, 16, 16]
        size = [16, 16, 16, 20, 24]
        side = size[GameCanvas.cursor[26]]
        x -= side >> 1
        y -= side >> 1
        GameCanvas.draw_region(x, y, side, side, GameCanvas.sparkle, src_x[GameCanvas.cursor[26]], src_y[GameCanvas.cursor[26]])

    def draw_sparkles(self):
        if GameCanvas.cursor[0] == 2:
            self.draw_sparkle(GameCanvas.cursor[24], GameCanvas.cursor[25])
            return
        if GameCanvas.cursor[0] == 3:
            for b in range(3):
                if GameCanvas.combine_pos[b].x > 0 and GameCanvas.combine_pos[b].y > 0:
                    self.draw_sparkle(GameCanvas.combine_pos[b].x, GameCanvas.combine_pos[b].y)

    @staticmethod
    def blacksmith_message():  # Blacksmith message popup
        from pow.game.popups import Popups
        outcome = ["Success", "Fail"]
        str_ = ""
        GameCanvas.popups.reset()
        GameCanvas.redraw = 1
        cursor = GameCanvas.cursor
        msg = cursor[20]
        if msg == 0:
            if cursor[19] < 1:
                return
            str_ = Popups.show_bought()
        elif msg == 11:
            str_ = Popups.show_sold()
        elif msg == 1:
            if cursor[22] == 0:
                str_ = "1Not possible |to enchant."
            else:
                str_ = "2Price is " + str(cursor[21]) + ".If |enchanting fails,|Items can be lost.|Continue?"
                GameCanvas.popups.timer = 200
        elif msg == 2:
            if cursor[23] != 0:
                cursor[23] = 1
            str_ = "1Enchant|" + outcome[cursor[23]]
        elif msg == 3:
            str_ = "1Fully enchanted.|Not possible|to enchant."
        elif msg == 4:
            str_ = "1Not enough Gold"
        elif msg == 5:
            str_ = "1You cannot|buy anymore."
        elif msg == 6:
            str_ = "3Your backpack|is full. Please|empty some items|and try again."
        elif msg == 7:
            str_ = "3Please select|3 items to|combine into one."
        elif msg == 8:
            if cursor[22] == 2:
                str_ = "1Not possible."
            else:
                str_ = ("2Compounding fee|is " + str(cursor[21]) + ".|Selected items|could be lost|"
                        "when it fails.|Continue?")
                GameCanvas.popups.timer = 200
        elif msg == 9:
            str_ = "1Compounding| " + outcome[cursor[22]]
        GameCanvas.popups.show_text(str_)

    def blacksmith_keys(self):  # Blacksmith keys
        cursor = GameCanvas.cursor
        bool_ = True
        if cursor[26] != -1:
            return
        key = GameCanvas.key
        if key in (-1, 50):
            if cursor[27] == 0:
                cursor[10] = cursor[10] - 1
            else:
                cursor[18] = cursor[18] + 1
                if cursor[18] > 8:
                    cursor[18] = 0
            GameCanvas.info_box.text = ""
        elif key in (-2, 56):
            if cursor[27] == 0:
                cursor[10] = cursor[10] + 1
            else:
                cursor[18] = cursor[18] - 1
                if cursor[18] < 0:
                    cursor[18] = 8
            GameCanvas.info_box.text = ""
        elif key in (-3, 52):
            if cursor[27] == 0:
                cursor[9] = cursor[9] - 1
                if cursor[9] < 0:
                    cursor[9] = 4
                    cursor[10] = cursor[10] - 1
            else:
                cursor[18] = cursor[18] + 1
                if cursor[18] > 8:
                    cursor[18] = 0
            GameCanvas.info_box.text = ""
        elif key in (-4, 54):
            if cursor[27] == 0:
                cursor[9] = cursor[9] + 1
                if cursor[9] >= 5:
                    cursor[9] = 0
                    cursor[10] = cursor[10] + 1
            else:
                cursor[18] = cursor[18] - 1
                if cursor[18] < 0:
                    cursor[18] = 8
            GameCanvas.info_box.text = ""
        elif key == -7:
            menu = GameCanvas.menu
            menu[0] = consts.menu_parent[menu[0]]
            GameCanvas.menu_count = consts.menu_sizes[menu[0]]
            menu[1] = GameCanvas.menu_cursors[menu[0]]
            menu[2] = GameCanvas.menu_tops[menu[0]]
            GameCanvas.redraw = 1
            bool_ = False
            GameCanvas.images[39] = None
            GameCanvas.info_box.text = ""
            Menus.clear_combine()
        elif key in (-5, 53):
            if cursor[0] == 0:
                self.buy_item()
                bool_ = False
                Menus.blacksmith_message()
            elif cursor[0] == 1:
                if cursor[19] != 0:
                    self.sell_item()
                    Menus.blacksmith_message()
                else:
                    bool_ = False          # falls into `default`
            elif cursor[0] == 2:
                self.enchant_price()
                Menus.blacksmith_message()
                bool_ = False              # falls into `default`
            elif cursor[0] == 3 and self.item_under_cursor(-1).id > 100:
                b = 3
                if GameCanvas.combine_slots[3] > 0:
                    b = 0
                    while b < GameCanvas.combine_slots[3] and GameCanvas.combine_slots[b] != cursor[18]:
                        b += 1
                if b < GameCanvas.combine_slots[3]:
                    while b < 2:
                        GameCanvas.combine_slots[b] = GameCanvas.combine_slots[b + 1]
                        b += 1
                    GameCanvas.combine_slots[3] = GameCanvas.combine_slots[3] - 1
                else:
                    GameCanvas.combine_slots[GameCanvas.combine_slots[3]] = cursor[18]
                    GameCanvas.combine_slots[3] = GameCanvas.combine_slots[3] + 1
                if GameCanvas.combine_slots[3] == 3:
                    self.combine_result_of()
        else:
            bool_ = False
        if bool_:
            self.update_shop_cursor()
            GameCanvas.menus.draw_blacksmith(True)

    def combine_result_of(self):  # Combine: work out the result of 3 items
        ids = [0, 0, 0]
        i = 0
        for b in range(3):
            item = self.item_under_cursor(GameCanvas.combine_slots[b])
            pos = 0
            while pos < b and ids[pos] <= item.id:
                pos += 1
            for j in range(b, pos, -1):
                ids[j] = ids[j - 1]
            ids[pos] = item.id
            i += item.enchant
        Menus.mix_table = ResReader.read("/" + GameCanvas.scr_data.get(68))
        if Menus.mix_table is not None:
            table_base = [0, 149, 298]
            lo = 0
            hi = 149
            b = 0
            while b < 3:
                run = self.find_run(table_base[b], ids[b], lo, hi)
                lo = run[0]
                hi = run[1]
                if run[2] == 0:
                    break
                b += 1
            if b < 3:
                GameCanvas.cursor[22] = 2
                Menus.clear_combine()
            else:
                lo += self.rand(hi)
                ids[0] = Menus.mix_entry(447 + lo)
                GameCanvas.combine_result = self.make_item(ids[0])
                GameCanvas.cursor[21] = idiv(Menus.item_price(GameCanvas.combine_result), 4)
                if ids[0] < 500:
                    ids[1] = GameCanvas.item_tables[1].get_int(ids[0] - 301, 8)
                    ids[2] = 15
                else:
                    ids[1] = GameCanvas.item_tables[2].get_int(ids[0] - 501, 7)
                    ids[2] = 12
                ids[1] = idiv(200 - ids[1], 12)
                if ids[1] >= self.rand(101):
                    GameCanvas.cursor[22] = 0
                    GameCanvas.combine_result = self.enchant_item(GameCanvas.combine_result, idiv(i, 3))
                else:
                    GameCanvas.cursor[22] = 1
                    ids[1] = idiv((100 - ids[1]) * 10, ids[2])
                    GameCanvas.cursor[31] = GameCanvas.combine_slots[self.rand(3)] if ids[1] >= self.rand(101) else -1
                GameCanvas.cursor[23] = -1
            GameCanvas.cursor[20] = 8
            Menus.blacksmith_message()
        Menus.mix_table = None

    def enchant_item(self, item, times):  # enchant paramInt times: raise stats
        odds = [30, 25, 20, 15, 9, 1]
        for b in range(times):
            i = 0
            roll = self.rand(101)
            step = 0
            while step < 5:
                i += odds[step]
                if roll < i:
                    break
                step += 1
            roll = (step + 5) * 10
            stat = 0
            for step in range(4):
                stat = (item.attack, item.defense, item.hp, item.mp)[step]
                i = stat
                if i > 0:
                    i = idiv(idiv(i * roll, 10) + 50, 100)
                    if i == 0:
                        i = 1
                    if step == 0:
                        item.attack = i16(item.attack + i)
                    elif step == 1:
                        item.defense = i16(item.defense + i)
                    elif step == 2:
                        item.hp = i16(item.hp + i)
                    elif step == 3:
                        item.mp = i16(item.mp + i)
            item.enchant = i8(item.enchant + 1)
        return item

    @staticmethod
    def mix_entry(index):
        return Menus.mix_table[index * 2] & 0xFF | (Menus.mix_table[index * 2 + 1] & 0xFF) << 8

    def find_run(self, base, value, start, count):  # find run of paramInt2
        run = [start, count, 0]
        b = 0
        while b < run[1]:
            i = Menus.mix_entry(base + run[0])
            if i == value:
                break
            run[0] = run[0] + 1
            b += 1
        if b < run[1]:
            run[1] = run[1] - b
            b = 0
            i = Menus.mix_entry(base + run[0])
            while b < run[1] and i == value:
                b += 1
                i = Menus.mix_entry(base + run[0] + b)
            run[1] = b
            run[2] = 1
            return run
        run[2] = 0
        return run

    def enter_blacksmith(self):  # enter a Blacksmith screen
        if GameCanvas.menu[0] == 24:
            Menus.count_items()
            if GameCanvas.cursor[16] < 3:
                GameCanvas.popups.setup_popup(39)
                GameCanvas.redraw = 1
                GameCanvas.menu[1] = 3
                GameCanvas.cursor[8] = 0           # the grid behind the popup: its own scroll / cursor,
                GameCanvas.cursor[18] = 0          # not the last grid screen's (the 9-row Warehouse)
                return True
        GameCanvas.load_item_tables()
        self.blacksmith_layout()
        return True

    def blacksmith_layout(self):  # grid layout of the current Blacksmith mode
        cursor = GameCanvas.cursor
        cursor[0] = GameCanvas.menu[0] - 21
        if cursor[0] == 0 or cursor[0] == 1:
            cursor[14] = cursor[0] + 1
        else:
            cursor[14] = 0
        if cursor[0] == 3:
            Menus.clear_combine()
            cursor[20] = 7
            Menus.blacksmith_message()
        Menus.count_items()
        i = 0
        gap = 173                     # '­'
        cursor[4] = 5
        if cursor[0] != 0:
            cursor[4] = config.BACKPACK_SIZE // 5   # config.BACKPACK_SIZE (the shop of mode 0 keeps 25)
        if cursor[0] == 1:
            cursor[4] = cursor[4] + 1
        cursor[3] = 5
        cursor[3] = min(cursor[3], 3)
        if cursor[3] < cursor[4]:
            cursor[11] = 1
        else:
            cursor[3] = cursor[4]
            cursor[11] = 0
        cursor[6] = cursor[3] * 32 - 2
        i = 72 + cursor[6]
        cursor[1] = 26 + (243 - i) // 2 + 1
        i = 158
        if cursor[11] == 1:
            gap = 32
            i = 164
            cursor[7] = 32 * cursor[4] - 2
            cursor[13] = idiv(cursor[6] * (cursor[6] - 2), cursor[7]) + 1
        cursor[5] = (240 - i) // 2 + 1
        cursor[12] = cursor[5] + gap
        cursor[27] = 0
        cursor[8] = 0
        cursor[10] = 0
        cursor[9] = 0
        self.update_shop_cursor()
        cursor[26] = -1

    def update_shop_cursor(self):  # clamp cursor, scroll, item under cursor -> fK[19]
        cursor = GameCanvas.cursor
        if cursor[27] == 0:
            if cursor[10] < 0:
                cursor[10] = cursor[4] - 1
            elif cursor[10] >= cursor[4]:
                cursor[10] = 0
            if cursor[10] < cursor[8]:
                cursor[8] = cursor[10]
            elif cursor[10] >= cursor[8] + cursor[3]:
                cursor[8] = cursor[10] - cursor[3] + 1
            cursor[18] = cursor[10] * 5 + cursor[9]
        item = self.item_under_cursor(-1)
        cursor[19] = item.id if item is not None else 0

    @staticmethod
    def item_name(item_id):  # item name
        if item_id < 100:
            return consts.potion_names[item_id - 1]
        if item_id < 300:
            return GameCanvas.item_tables[0].get_string(item_id - 101, 0)
        if item_id < 500:
            return GameCanvas.item_tables[1].get_string(item_id - 301, 0)
        return GameCanvas.item_tables[2].get_string(item_id - 501, 0)

    @staticmethod
    def clear_combine():  # clear the Combine selection
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
    def count_items():  # count items: fK[16] backpack, fK[17] potions
        GameCanvas.cursor[16] = 0
        for b in range(config.BACKPACK_SIZE):
            if GameCanvas.hero.backpack[b].id > 0:
                GameCanvas.cursor[16] = GameCanvas.cursor[16] + 1
        GameCanvas.cursor[17] = 0
        for b in range(5):
            if GameCanvas.hero.quick_slots[b].item > 0:
                GameCanvas.cursor[17] = GameCanvas.cursor[17] + 1

    @staticmethod
    def item_price(item):  # price of an item
        if item.id < 100:
            i = consts.item_prices[item.id - 1]
        elif item.id < 300:
            i = GameCanvas.item_tables[0].get_int(item.id - 101, 6)
            i = i + item.attack * 100
            i = i + item.defense * 100
            i = i + idiv(item.hp, 5) * 100
            i = i + idiv(item.mp, 3) * 100
        elif item.id < 500:
            unit = 800 if GameCanvas.item_tables[1].get_int(item.id - 301, 6) == 0 else 400
            i = item.attack * unit
            i = i + item.defense * unit
            i = i + idiv(item.hp, 5) * unit
            i = i + idiv(item.mp, 3) * unit
        else:
            i = GameCanvas.item_tables[2].get_int(item.id - 501, 6)
        return i

    def buy_item(self):  # Buy
        hero = GameCanvas.hero
        cursor = GameCanvas.cursor
        item = GameCanvas.shop[cursor[18]]
        if item.id == 0:
            cursor[20] = -1
            return
        i = Menus.item_price(item)
        if hero.gold >= i:
            if item.id < 100:
                b = 0
                while b < 5 and hero.quick_slots[b].item != item.id:
                    b += 1
                if b < 5:
                    if hero.quick_slots[b].count < 5:
                        hero.quick_slots[b].count = i16(hero.quick_slots[b].count + 1)
                        cursor[20] = 0
                    else:
                        cursor[20] = 5
                else:
                    b = 0
                    while b < 5 and hero.quick_slots[b].item != 0:
                        b += 1
                    if b < 5:
                        hero.quick_slots[b].item = item.id
                        hero.quick_slots[b].count = 1
                        cursor[17] = cursor[17] + 1
                        cursor[20] = 0
                    else:
                        cursor[20] = 6
            elif cursor[16] < config.BACKPACK_SIZE:
                b = 0
                while b < config.BACKPACK_SIZE and hero.backpack[b].id != 0:
                    b += 1
                slot = hero.backpack[b]
                slot.id = item.id
                slot.attack = item.attack
                slot.defense = item.defense
                slot.hp = item.hp
                slot.mp = item.mp
                slot.enchant = item.enchant
                Item.clear(item)
                cursor[16] = cursor[16] + 1
                cursor[20] = 0
            else:
                cursor[20] = 6
        else:
            cursor[20] = 4
        if cursor[20] == 0:
            hero.gold -= i
            self.save_game()

    def sell_item(self):  # Sell, half price
        hero = GameCanvas.hero
        cursor = GameCanvas.cursor
        item = self.item_under_cursor(-1)
        if item is None or item.id == 0:
            return
        i = Menus.item_price(item)
        if item.id < 100:
            if hero.quick_slots[cursor[18]].count > 1:
                hero.quick_slots[cursor[18]].count = i16(hero.quick_slots[cursor[18]].count - 1)
            else:
                hero.quick_slots[cursor[18]].item = 0
                hero.quick_slots[cursor[18]].count = 0
                cursor[17] = cursor[17] - 1
        else:
            Item.clear(item)
            cursor[16] = cursor[16] - 1
        cursor[20] = 11
        hero.gold += idiv(i, 2)
        self.save_game()

    def enchant_price(self):  # Enchant: price and limit
        cursor = GameCanvas.cursor
        item = self.item_under_cursor(-1)
        if item.id == 0:
            cursor[20] = -1
            return
        cursor[22] = 0
        cursor[21] = 0
        if 100 < item.id < 500:
            if item.id < 300:
                cursor[22] = GameCanvas.item_tables[0].get_int(item.id - 101, 5)
            else:
                cursor[22] = GameCanvas.item_tables[1].get_int(item.id - 301, 6)
            if cursor[22] > 0:
                cursor[21] = item.attack * 100
                cursor[21] = cursor[21] + item.defense * 100
                cursor[21] = cursor[21] + idiv(item.hp * 100, 5)
                cursor[21] = cursor[21] + idiv(item.mp * 100, 3)
                if item.enchant >= cursor[22]:
                    cursor[22] = 0
                    cursor[20] = 3
                    return
        cursor[20] = 1
        if cursor[22] != 0:
            cursor[23] = -1

    def draw_shop_description(self, item, x, y, w, h, price, with_name):  # shop description
        info = GameCanvas.info_box
        price_sep = "/ Price: "
        price_label = "Price: "
        if item.id == 0:
            info.shown = 0
            info.rect.x = info.rect.y = info.rect.w = info.rect.h = 0
            info.text = ""
            info.rect.x = (GameCanvas.screen_w - 202) // 2 - GameCanvas.view_x
            info.rect.y = 200
            info.rect.w = w + 2
            info.rect.h = h
            return
        if GameCanvas.cursor[14] > 0 and price == -1:
            price = Menus.item_price(item)
        if item.id < 100:
            i = item.id - 1
            info.text = consts.potion_names[i]
            if GameCanvas.cursor[14] == 2:
                if len(info.text) > 0:
                    info.text += " / "
                info.text += price_label
                info.text += GameCanvas.format_thousands(price >> 1)
            info.text += " / "
            if i < 9:
                str_ = "Recover " + str(consts.potion_percents[i % 3]) + "% of total " + consts.potion_kinds[i // 3]
            else:
                str_ = "Ranged Atk"
            info.text += str_
            if GameCanvas.cursor[14] == 1:
                info.text += price_sep
                info.text += GameCanvas.format_thousands(price)
        else:
            if item.id < 300:
                str_ = GameCanvas.item_tables[0].get_string(item.id - 101, 0)
                i = consts.tier_levels[(item.id - 101) % 5]
            elif item.id < 500:
                str_ = GameCanvas.item_tables[1].get_string(item.id - 301, 0)
                i = GameCanvas.item_tables[1].get_int(item.id - 301, 8)
            else:
                str_ = GameCanvas.item_tables[2].get_string(item.id - 501, 0)
                i = GameCanvas.item_tables[2].get_int(item.id - 501, 7)
            if with_name:
                info.text += str_
            if GameCanvas.cursor[14] == 2:
                if len(info.text) > 0:
                    info.text += " / "
                info.text += price_label
                info.text += GameCanvas.format_thousands(price >> 1)
            if len(info.text) > 0:
                info.text += " / "
            special = {434: " / Hp 5 Increased", 435: " / MP 3 Increased", 436: " / DEF 1 Increased",
                       437: " / ATK 1 Increased", 502: " / Catherine's scarf", 504: " / all General Visiting"}
            if item.id in special:
                info.text += special[item.id][3:]
                if item.id == 504 and item.enchant > 0:
                    info.text += " / Enchanted Lv" + str(item.enchant)
            else:
                if item.attack > 0:
                    info.text += "Atk+" + str(item.attack) + " "
                if item.defense > 0:
                    info.text += "Def+" + str(item.defense) + " "
                if item.hp > 0:
                    info.text += "HP+" + str(item.hp) + " "
                if item.mp > 0:
                    info.text += "MP+" + str(item.mp) + " "
                if item.enchant > 0:
                    info.text += "/ Enchanted Lv" + str(item.enchant) + " "
                if i > 0:
                    info.text += "/ Available at Lv" + str(i) + " "
            if GameCanvas.cursor[14] == 1:
                info.text += price_sep
                info.text += GameCanvas.format_thousands(price)
        info.rect.x = (GameCanvas.screen_w - 202) // 2 - GameCanvas.view_x
        info.rect.y = 200
        info.rect.w = w + 2
        info.rect.h = h
        GameCanvas.text_width = GameCanvas.measure_text(info.text)
        if GameCanvas.text_width > w - 2:
            info.shown = 1
            if GameCanvas.key != -999:
                info.text_x = i16(info.rect.x + info.rect.w)
                return
        else:
            info.shown = 0
            info.text_x = i16(x + 1)

    def load_title_images(self):
        self.load_title_picture()
        GameCanvas.images[18] = self.load_image(GameCanvas.scr_ui.get(77))

    def draw_main_menu(self):  # Main Menu: caption strip + blinking arrows
        i = GameCanvas.menu[1]
        strip_x = GameCanvas.view_cx - 52 + GameCanvas.view_x
        if i == 0 and not GameCanvas.has_save():
            i = 9
        GameCanvas.draw_region(strip_x, GameCanvas.canvas_size.y - 65, 116, 21, GameCanvas.images[18], 0, i * 21)
        GameCanvas.draw_region(strip_x - 24 - GameCanvas.lord_count % 3 * 2, GameCanvas.canvas_size.y - 65 + 2, 10, 16, GameCanvas.images[17], 0, 0)
        GameCanvas.draw_region(strip_x + 116 + 16 + GameCanvas.lord_count % 3 * 2, GameCanvas.canvas_size.y - 65 + 2, 10, 16, GameCanvas.images[17], 10, 0)
        if GameCanvas.lord_count > 100:
            GameCanvas.lord_count = 32
            return
        GameCanvas.lord_count += 1

    def draw_hero_choice(self):  # screen 6: choose the hero, 3 heads, the middle one is chosen
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
        # the heroes differ in base stats (hero_classes); show the chosen one's
        head = GameCanvas.hero.head
        self.draw_text_at(hero_classes.NAMES[head & 0x3], GameCanvas.view_cy + 72, 0)
        self.draw_text_at(hero_classes.stats_line(head), GameCanvas.view_cy + 92, 0)

    # --- attribute reset (pow/game/hero_classes.py) ---------------------------------
    def open_respec(self):
        """Attributes screen, left soft key: pay gold or an elixir to get the stat points back."""
        hero = GameCanvas.hero
        popups = GameCanvas.popups
        if hero_classes.spent_points(hero) == 0:
            popups.popup_id = RESPEC_DONE_POPUP
            popups.show_text("3Nothing to reset.")
            return
        slot = hero_classes.respec_item_slot(hero)
        if slot >= 0:
            item = "Use " + Menus.item_name(hero.backpack[slot].id)
        else:
            item = "No elixir"
        popups.setup_choice(RESPEC_POPUP, ["Reset attributes?", "Refund: %d points" % hero_classes.spent_points(hero)],
                        ["Pay " + GameCanvas.format_thousands(hero_classes.respec_gold(hero)) + " gold", item, "Cancel"])

    def finish_respec(self, choice):
        """The choice of open_respec(): 0 gold, 1 elixir, 2 cancel."""
        hero = GameCanvas.hero
        popups = GameCanvas.popups
        GameCanvas.redraw = 1
        if choice == 0:
            cost = hero_classes.respec_gold(hero)
            if hero.gold < cost:
                popups.popup_id = RESPEC_DONE_POPUP
                popups.show_text("3Not enough gold.")
                return
            hero.gold -= cost
        elif choice == 1:
            slot = hero_classes.respec_item_slot(hero)
            if slot < 0:
                popups.popup_id = RESPEC_DONE_POPUP
                popups.show_text("3You have no elixir.|Rise Potion, Azure|Potion, Falls or|Forest Medicine.")
                return
            Item.clear(hero.backpack[slot])
        else:
            return
        free = hero_classes.respec(hero)
        GameCanvas.update_hero_stats()
        GameCanvas.menu[1] = 0
        self.save_game()
        popups.popup_id = RESPEC_DONE_POPUP
        popups.show_text("3Attributes reset.|%d points are free." % free)

    def draw_name_captions(self):  # screen 7: the two caption lines
        Gfx.set_font(GameCanvas.font_white)
        GameCanvas.anim_step = 0
        while GameCanvas.anim_step < 2:
            self.draw_text_at(GameCanvas.gamestr(69 + GameCanvas.anim_step), GameCanvas.view_cy - 47 + GameCanvas.anim_step * 20, 0)
            GameCanvas.anim_step += 1

    def draw_name_box(self):  # screen 7: the name box
        i = GameCanvas.view_cx - 80 + GameCanvas.view_x
        box_y = GameCanvas.view_cy + 8 + GameCanvas.view_y
        Gfx.fill_rect(i, box_y, 160, 20, 0)
        Gfx.draw_rect(i, box_y, 160, 20, GameCanvas.rgb(173, 170, 173))
        Gfx.set_font(GameCanvas.font_white)
        Gfx.draw_string(GameCanvas.name_buf.get_text(), GameCanvas.screen_cx, box_y + 2, 1)
        if GameCanvas.name_buf.length() == 0:
            GameCanvas.draw_softkeys(-1, 2)
            return
        GameCanvas.draw_softkeys(-1, 10)

    def draw_stat_sheet(self, whole):  # screen 8/14: stat sheet; 1 = whole, 0 = numbers only
        hero = GameCanvas.hero
        base = [hero.base_hp, hero.base_mp, hero.base_attack, hero.base_defense]
        image = None
        if whole != 0:
            rect = self.load_exp_table()
            GameCanvas.exp_bars[0] = i16(idiv(hero.exp * 100, rect[0]))
            image = self.load_image(GameCanvas.scr_ui.get(26))
            i = image.getWidth()
            sheet_h = image.getHeight()
            GameCanvas.sheet_y = GameCanvas.view_cy - sheet_h // 2
            GameCanvas.sheet_x = GameCanvas.view_cx - i // 2
            self.draw_map_region(image, GameCanvas.sheet_x, GameCanvas.sheet_y, i, sheet_h, 0, 0)
            GameCanvas.draw_view_text_centred(hero.name, GameCanvas.sheet_x + 110, GameCanvas.sheet_y + 6)
            self.draw_big_number(hero.level, GameCanvas.sheet_x + 152, GameCanvas.sheet_y + 34, 0)
            self.draw_big_number(hero.fame, GameCanvas.sheet_x + 152, GameCanvas.sheet_y + 61, 0)
        else:
            rect = [GameCanvas.sheet_x + 88, GameCanvas.sheet_y + 83, 68, 20]
            Gfx.fill_rect(rect[0], rect[1], rect[2], rect[3], 0)
            rect[0] = GameCanvas.sheet_x + 39
            rect[1] = GameCanvas.sheet_y + 108
            rect[2] = 104
            rect[3] = 18
            for row in range(4):
                Gfx.fill_rect(rect[0], rect[1], rect[2], rect[3], 0)
                rect[1] = rect[1] + 20
        gear = [hero.gear_hp, hero.gear_mp, hero.gear_attack, hero.gear_defense]
        self.draw_big_number(hero.stat_points, GameCanvas.sheet_x + 152, GameCanvas.sheet_y + 86, 0)
        for b in range(4):
            i = self.draw_big_number(base[b], GameCanvas.sheet_x + 44, GameCanvas.sheet_y + 110 + b * 20, 1)
            if gear[b] > 0:
                self.draw_map_region(GameCanvas.images[19], i + 1, GameCanvas.sheet_y + 110 + b * 20, 10, 14, 105, 0)
                self.draw_big_number(gear[b], i + 9, GameCanvas.sheet_y + 110 + b * 20, 1)
        image = self.load_image(GameCanvas.scr_char.get(38 + hero.head))
        self.draw_map_region(image, GameCanvas.sheet_x + 2, GameCanvas.sheet_y + 3, 46, 46, 0, 0)
        if hero.stat_points > 0:
            self.draw_rect_outline(GameCanvas.sheet_x + 144, GameCanvas.sheet_y + 97 + 20 * GameCanvas.menu[1] + GameCanvas.view_y + 11, 14, 18, 255, 255, 255)
        GameCanvas.menu_part = 0

    def draw_story_portraits(self, speaker):  # story: speaker portrait top-left, hero bottom-right
        self.draw_box(19 + GameCanvas.view_x + 2, GameCanvas.view_cy - 72 + 9 + GameCanvas.view_y, 46, 46, True)
        if speaker > -1:
            self.draw_image_file(GameCanvas.scr_char.get(0 + speaker), 19 + GameCanvas.view_x + 2, GameCanvas.view_cy - 73 + 10 + GameCanvas.view_y, 46, 46, 0, 0)
        self.draw_box(GameCanvas.canvas_size.x // 2 + 60 - GameCanvas.view_x, GameCanvas.view_cy - 72 + 109 + GameCanvas.view_y, 46, 46, True)
        self.draw_image_file(GameCanvas.scr_char.get(38 + GameCanvas.hero.head), GameCanvas.canvas_size.x // 2 + 60 - GameCanvas.view_x, GameCanvas.view_cy - 73 + 110 + GameCanvas.view_y, 46, 46, 0, 0)
        self.draw_speech_boxes(3)

    def draw_speech_boxes(self, boxes):  # empty speech boxes: 1 = top, 2 = bottom
        if (boxes & 0x1) != 0:
            self.draw_box(GameCanvas.view_cx - 60 + 15 + GameCanvas.view_x, GameCanvas.view_cy - 73 + 7 + GameCanvas.view_y, 150, 53, False)
        if (boxes & 0x2) != 0:
            self.draw_box(GameCanvas.view_cx - 60 + -40 + GameCanvas.view_x, GameCanvas.view_cy - 73 + 107 + GameCanvas.view_y, 150, 53, False)

    @staticmethod
    def type_speech(slot, pos, redraw):  # type speech text fw[p1], max 3 lines
        # paramInt3 == 0: one tick of typing (state kept in fA/fx/fy/fz/fB/fC); 1: redraw all
        if slot == 0:
            left = GameCanvas.view_cx - 60 + 15 + 2 + GameCanvas.view_x
            top = GameCanvas.view_cy - 73 + 7 + 2 + GameCanvas.view_y
        elif slot == 1:
            left = GameCanvas.view_cx - 60 + -40 + 2 + GameCanvas.view_x
            top = GameCanvas.view_cy - 73 + 107 + 2 + GameCanvas.view_y
        else:
            return False
        if (GameCanvas.key in (-6, -5)) and redraw == 0:
            limit = 1000                    # a key shows the whole text at once
        else:
            limit = GameCanvas.speech_pos[slot]
        # n == 0 -> start over, else continue
        cur = 0 if pos != limit else pos
        if cur == 0:
            i = left
            y = top
            line_start = 0
            lines_done = 0
            extent = 0
        else:
            i = GameCanvas.speech_x[slot]
            y = GameCanvas.speech_y[slot]
            line_start = GameCanvas.speech_lines[slot]
            lines_done = GameCanvas.speech_done[slot]
            extent = GameCanvas.speech_w[slot]
        Gfx.set_font(GameCanvas.font_white)
        while cur <= limit and cur < len(GameCanvas.speech[slot]):
            text = GameCanvas.speech[slot]
            line_h = Font.ascent() + Font.gap()
            prev = (1 if cur <= 0 else cur) - 1
            if i == left or (prev < len(text) and text[prev] == " ") or (cur - 1 < len(text) and text[cur - 1] == "]"):
                b = 0
                used_h = 0
                while cur + b + 1 < len(text) and text[cur + b] != " " and text[cur + b] != "]" and text[cur + b] != ",":
                    used_h += Font.ascent() + Font.gap()
                    b += 1
                    if used_h > 146:
                        used_h -= Font.ascent() + Font.gap()
                if text[cur + b] == "]":
                    extent += Font.ascent()
                if used_h + extent > 146:
                    extent += used_h
            extent += line_h
            if extent > 146:
                if GameCanvas.key != -999 and lines_done == 2:
                    break
                i = left
                extent = line_h
                if lines_done == 0:
                    line_start = cur
                elif lines_done != 1 and lines_done == 2:
                    # 3 lines are full: drop the first line and start drawing again
                    str_ = text[line_start:]
                    GameCanvas.speech[slot] = str_
                    limit -= line_start
                    lines_done = cur = 0
                    y = top
                    extent = 0
                    continue
                lines_done += 1
                y += 16
            if cur == 0:
                GameCanvas.menus.draw_speech_boxes(slot + 1)
            if i == left and text[cur] == " ":
                cur += 1
            if len(text) >= cur + 1:
                Gfx.draw_string(text[cur:cur + 1], i, y, 0)
            i += line_h
            cur += 1
        if redraw == 0:
            GameCanvas.speech_pos[slot] = cur
            GameCanvas.speech_x[slot] = i
            GameCanvas.speech_y[slot] = y
            GameCanvas.speech_w[slot] = extent
            GameCanvas.speech_lines[slot] = line_start
            GameCanvas.speech_done[slot] = lines_done
        return True

    def draw_difficulty(self):  # screen 29: difficulty Hard / Normal
        box_pos = [GameCanvas.view_cx - 80 + GameCanvas.view_x, GameCanvas.view_cy - 60 + GameCanvas.view_y]
        GameCanvas.difficulty = i16(GameCanvas.menu[1])
        for b in range(2):
            if GameCanvas.menu[1] == b:
                Gfx.set_font(GameCanvas.font_orange)
                bool_ = True
            else:
                Gfx.set_font(GameCanvas.font_white)
                bool_ = False
            self.draw_box(box_pos[0], box_pos[1] + b * 25, 160, 20, bool_)
            self.draw_text_at(consts.difficulty_names[b], box_pos[1] + 1 + b * 25 - 1, 15)
        Gfx.set_font(GameCanvas.font_white)
        self.draw_box(box_pos[0], GameCanvas.view_cy + GameCanvas.view_y, 160, 80, False)
        for b in range(3):
            self.draw_text_at(consts.mode_texts[GameCanvas.menu[1]][b], GameCanvas.view_cy + 10 + b * 20, 17)

    def load_item_def(self, item_id):  # item record -> cX / cY / cZ
        name_utf = bytearray(16)
        if item_id < 100:
            return
        if item_id < 300:
            if GameCanvas.gear_data is None:
                GameCanvas.gear_data = GameCanvas.load_data_file(47)
            gear_table = GameCanvas.gear_data
            i = 9 + (item_id - 101) * 23
            b = 0
            while b < 15:
                name_utf[b] = gear_table[i + b] & 0xFF
                if name_utf[b] == 0:
                    break
                b += 1
            GameCanvas.gear_def.name = GameCanvas.read_utf(name_utf, 0, b)
            GameCanvas.gear_def.slot = i8(gear_table[i + 15])
            GameCanvas.gear_def.bonus_stat = i8(gear_table[i + 15 + 1])
            GameCanvas.gear_def.bonus = i8(gear_table[i + 15 + 2])
            GameCanvas.gear_def.bonus_range = i8(gear_table[i + 15 + 3])
            GameCanvas.gear_def.icon = i8(gear_table[i + 22])
            if GameCanvas.state != 2:
                GameCanvas.gear_data = None
                return
        elif item_id < 500:
            if GameCanvas.treasure_data is None:
                GameCanvas.treasure_data = GameCanvas.load_data_file(51)
            treasure_table = GameCanvas.treasure_data
            i = 10 + (item_id - 301) * 24
            b = 0
            while b < 15:
                name_utf[b] = treasure_table[i + b] & 0xFF
                if name_utf[b] == 0:
                    break
                b += 1
            GameCanvas.treasure_def.name = GameCanvas.read_utf(name_utf, 0, b)
            GameCanvas.treasure_def.slot = i8(treasure_table[i + 15])
            GameCanvas.treasure_def.attack = GameCanvas.u16(treasure_table[i + 16], treasure_table[i + 17])
            GameCanvas.treasure_def.defense = i8(treasure_table[i + 18])
            GameCanvas.treasure_def.hp = treasure_table[i + 19] & 0xFF
            GameCanvas.treasure_def.mp = i8(treasure_table[i + 20])
            GameCanvas.treasure_def.icon = i8(treasure_table[i + 22])
            GameCanvas.treasure_def.level = treasure_table[i + 23] & 0xFF
            if GameCanvas.state != 2:
                GameCanvas.treasure_data = None
                return
        else:
            if GameCanvas.rare_data is None:
                GameCanvas.rare_data = GameCanvas.load_data_file(49)
            rare_table = GameCanvas.rare_data
            i = 9 + (item_id - 501) * 27
            b = 0
            while b < 15:
                name_utf[b] = rare_table[i + b] & 0xFF
                if name_utf[b] == 0:
                    break
                b += 1
            GameCanvas.rare_def.name = GameCanvas.read_utf(name_utf, 0, b)
            GameCanvas.rare_def.slot = i8(rare_table[i + 15])
            GameCanvas.rare_def.attack = GameCanvas.u16(rare_table[i + 16], rare_table[i + 17])
            GameCanvas.rare_def.defense = i8(rare_table[i + 18])
            GameCanvas.rare_def.hp = GameCanvas.u16(rare_table[i + 19], rare_table[i + 20])
            GameCanvas.rare_def.mp = i8(rare_table[i + 21])
            GameCanvas.rare_def.level = rare_table[i + 26] & 0xFF
            if GameCanvas.state != 2:
                GameCanvas.rare_data = None

    def draw_stat_cursor(self, draw):  # stat cursor: 0 = erase, 1 = draw
        if GameCanvas.hero.stat_points > 0:
            if draw != 0:
                color = 255
            else:
                color = 0
            self.draw_rect_outline(GameCanvas.sheet_x + 144, GameCanvas.sheet_y + 97 + 20 * GameCanvas.menu[1] + 11, 14, 18, color, color, color)

    def load_exp_table(self):  # exp table of the hero level from edat 45
        data = GameCanvas.load_data_file(45)
        size = 40
        if GameCanvas.hero.level > 190:
            size = 200 - GameCanvas.hero.level << 2
        count = size // 4
        table = [0] * count
        i = 4 * (GameCanvas.hero.level - 1) + 2
        for b in range(count):
            pos = i + b * 4
            table[b] = i32((data[pos + 3] & 0xFF) << 24 | (data[pos + 2] & 0xFF) << 16
                                | (data[pos + 1] & 0xFF) << 8 | data[pos] & 0xFF)
        return table

    def draw_game_menu(self):  # Game Menu carousel, 4 animation frames per step
        menu = GameCanvas.menu
        anim = GameCanvas.menu_anim
        if GameCanvas.images[27] is None:
            self.load_menu_frames()
        cx = GameCanvas.view_cx
        top_x = [cx - 44 + 0] * 4
        top_y = [164, 180, 188, 166]
        bottom_x = [cx - 44 + 0] * 4
        bottom_y = [244, 230, 220, 244]
        mid_x = [cx - 63 - 5 + 0] * 4
        mid_y = [200, 232, 185, 204]
        i = cx - 60
        if GameCanvas.redraw == 2:
            if GameCanvas.menu_scroll == 1:
                for arr in (top_x, top_y, bottom_x, bottom_y, mid_x, mid_y):
                    arr[1], arr[2] = arr[2], arr[1]
                GameCanvas.menu_anim = i16(GameCanvas.menu_anim + 1)
                if GameCanvas.menu_anim == 3:
                    menu[1] = menu[1] + 1
                    if menu[1] >= GameCanvas.menu_count - 1:
                        menu[2] = 0
                        menu[1] = 0
                    GameCanvas.clamp_menu_scroll()
                elif GameCanvas.menu_anim > 3:
                    GameCanvas.redraw = 0
                    GameCanvas.menu_scroll = 0
                    GameCanvas.menu_anim = 0
            elif GameCanvas.menu_scroll == -1:
                GameCanvas.menu_anim = i16(GameCanvas.menu_anim + 1)
                if GameCanvas.menu_anim == 3:
                    menu[1] = menu[1] - 1
                    if menu[1] < 0:
                        menu[1] = GameCanvas.menu_count - 1 - 1
                    GameCanvas.clamp_menu_scroll()
                elif GameCanvas.menu_anim > 3:
                    GameCanvas.redraw = 0
                    GameCanvas.menu_scroll = 0
                    GameCanvas.menu_anim = 0
        self.draw_view_region(GameCanvas.images[7], 0, 0, GameCanvas.canvas_size.x, GameCanvas.canvas_size.y, 0, 0)
        self.draw_text_at(GameCanvas.menu_titles[menu[0]], 2 - GameCanvas.view_y, 0)
        if GameCanvas.carousel_image is None or GameCanvas.carousel_row != menu[1]:
            GameCanvas.carousel_image = self.load_image(GameCanvas.scr_ui.get(66 + menu[1]))
            GameCanvas.carousel_row = menu[1]
        if GameCanvas.carousel_image is not None:
            GameCanvas.draw_region(i, 60, 117, 90, GameCanvas.carousel_image, 0, 0)
        GameCanvas.draw_region(top_x[anim], top_y[anim], 89, 20, GameCanvas.images[27], 0, 0)
        GameCanvas.draw_region(top_x[anim] + 22, top_y[anim] + 5, 62, 11, GameCanvas.images[29], 0,
                     11 * (4 if menu[1] == 0 else (menu[1] - 1)))
        GameCanvas.draw_region(bottom_x[anim], bottom_y[anim], 89, 20, GameCanvas.images[27], 0, 0)
        GameCanvas.draw_region(bottom_x[anim] + 22, bottom_y[anim] + 5, 62, 11, GameCanvas.images[29], 0,
                     11 * (0 if menu[1] == 4 else (menu[1] + 1)))
        GameCanvas.draw_region(mid_x[anim], mid_y[anim], 127, 29, GameCanvas.images[26], 0, 0)
        GameCanvas.draw_region(mid_x[anim] + 22 + 2, mid_y[anim] + 5 + 1, 94, 18, GameCanvas.images[28], 0, 18 * menu[1])
        if GameCanvas.redraw != 2 and GameCanvas.menu_anim == 0:
            GameCanvas.draw_region(cx - 5 + GameCanvas.view_x, mid_y[anim] - 6 - 5 - GameCanvas.lord_count % 3 * 2, 16, 10, GameCanvas.images[17], 20, 0)
            GameCanvas.draw_region(cx - 5 + GameCanvas.view_x, mid_y[anim] + 29 + GameCanvas.lord_count % 3 * 2, 16, 10, GameCanvas.images[17], 20, 10)
        if GameCanvas.lord_count > 100:
            GameCanvas.lord_count = 32
        else:
            GameCanvas.lord_count += 1
        GameCanvas.draw_softkeys(-1, 2)

    # ---- Missions: lords (1), missions (2), description (3), briefing (4) ------------------

    def draw_mission_text(self):  # mission description, 6 lines per page
        self.draw_box(GameCanvas.view_cx - 100 + GameCanvas.view_x, GameCanvas.view_cy - 80, 200, 40, False)
        self.draw_text_at(GameCanvas.lord_name, GameCanvas.view_cy - 80, 30)
        self.draw_text_at(GameCanvas.mission_name, GameCanvas.view_cy - 60, 30)
        self.draw_box(GameCanvas.view_cx - 110, GameCanvas.view_cy - 30, 220, 119, False)
        for b in range(6):
            if GameCanvas.text_line_count[0] >= GameCanvas.menu[2] * 6 + b:
                GameCanvas.draw_text_left(GameCanvas.view_cx - 100 + GameCanvas.view_x, GameCanvas.view_cy - 28 + b * 20 + GameCanvas.view_y, GameCanvas.text_lines[0][GameCanvas.menu[2] * 6 + b])
        self.draw_page_number(GameCanvas.menu[2] + 1, idiv(GameCanvas.text_line_count[0], 6) + 1, GameCanvas.view_cy + 110, True)

    def draw_briefing(self):  # briefing: portraits + empty speech boxes
        self.draw_story_portraits(GameCanvas.mission_portraits[GameCanvas.mission])
        self.draw_skip_key(1)
        self.draw_speech_boxes(3)

    def draw_map_talk(self):  # talk in the map: portrait bottom-left
        if (GameCanvas.talk_box & 0x1) != 0:
            i = 0 + GameCanvas.general.portrait
        else:
            i = 38 + GameCanvas.hero.head
        box_y = GameCanvas.view_size.y - 46 - 4
        self.draw_box(2 + GameCanvas.view_x, box_y + GameCanvas.view_y, 48, 48, True)
        box_y += 1
        self.draw_image_file(GameCanvas.scr_char.get(i), 3 + GameCanvas.view_x, box_y + GameCanvas.view_y, 46, 46, 0, 0)
        self.draw_map_talk_box()
        self.draw_skip_key(1)

    def tick_dialogue(self):  # dialogue typewriter: dG 0 briefing, 1 map talk, 2 general
        box_steps = [2, 3, 5]
        rows_of = [2, 1, 1]
        if GameCanvas.state == 5 and GameCanvas.key != -6:
            GameCanvas.key = -999
        Gfx.set_font(GameCanvas.font_white)
        if GameCanvas.key == -6:
            GameCanvas.wait_ticks = 1
            GameCanvas.talk_rows = i16(GameCanvas.text_line_count[GameCanvas.talk_side])
            GameCanvas.talk_box = i16(box_steps[GameCanvas.talk_kind])
        if GameCanvas.wait_ticks > 0:
            GameCanvas.wait_ticks = i16(GameCanvas.wait_ticks - 1)
            if GameCanvas.key != -999:
                GameCanvas.wait_ticks = 0
            if GameCanvas.wait_ticks < 1:
                if GameCanvas.talk_rows >= GameCanvas.text_line_count[GameCanvas.talk_side]:
                    if GameCanvas.talk_box >= box_steps[GameCanvas.talk_kind]:
                        GameCanvas.redraw = 1
                        if GameCanvas.talk_kind != 0:
                            if GameCanvas.talk_kind == 1:
                                GameCanvas.state = 3
                                return
                            if GameCanvas.boss_fight != 0:
                                self.open_menu(2)
                                self.load_menu_frames()
                                GameCanvas.menu[0] = 0
                                GameCanvas.menu_count = consts.menu_sizes[GameCanvas.menu[0]]
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
                    if GameCanvas.talk_kind == 0:
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
                if GameCanvas.talk_row > rows_of[GameCanvas.talk_kind]:
                    GameCanvas.talk_row = i16(rows_of[GameCanvas.talk_kind])
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
                GameCanvas.talk_rows = i16(GameCanvas.talk_rows + rows_of[GameCanvas.talk_kind] - GameCanvas.talk_row)
                GameCanvas.talk_row = i16(rows_of[GameCanvas.talk_kind])
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

    def draw_briefing_boxes(self):  # briefing: both speech boxes
        Gfx.set_font(GameCanvas.font_white)
        self.draw_speech_boxes(2 if GameCanvas.talk_side != 0 else 1)
        lines, talk_x, talk_y = GameCanvas.text_lines, GameCanvas.talk_x, GameCanvas.talk_y
        if GameCanvas.talk_side != 0:
            for b in range(3):
                GameCanvas.draw_text(talk_x[0] + GameCanvas.view_x, talk_y[0] + 16 * b + GameCanvas.view_y, lines[0][b])
        else:
            for b in range(GameCanvas.talk_row):
                if lines[0][b] is not None:
                    GameCanvas.draw_text(talk_x[0] + GameCanvas.view_x, talk_y[0] + 16 * b + GameCanvas.view_y, lines[0][b])
            if lines[0][GameCanvas.talk_row] is not None:
                str_ = lines[0][GameCanvas.talk_row][0:min(GameCanvas.talk_chars, len(lines[0][GameCanvas.talk_row]))]
                GameCanvas.draw_text(talk_x[0] + GameCanvas.view_x, talk_y[0] + 16 * GameCanvas.talk_row + GameCanvas.view_y, str_)
        if GameCanvas.talk_box > 1:
            if GameCanvas.talk_side != 0:
                for b in range(GameCanvas.talk_row):
                    if lines[1][b] is not None:
                        GameCanvas.draw_text(talk_x[1] + GameCanvas.view_x, talk_y[1] + 16 * b + GameCanvas.view_y, lines[1][b])
                if lines[1][GameCanvas.talk_row] is not None:
                    str_ = lines[1][GameCanvas.talk_row][0:min(GameCanvas.talk_chars, len(lines[1][GameCanvas.talk_row]))]
                    GameCanvas.draw_text(talk_x[1] + GameCanvas.view_x, talk_y[1] + 16 * GameCanvas.talk_row + GameCanvas.view_y, str_)
                    return
            else:
                for b in range(3):
                    GameCanvas.draw_text(talk_x[1] + GameCanvas.view_x, talk_y[1] + 16 * b + GameCanvas.view_y, lines[1][b])

    def draw_map_talk_box(self):  # map talk: one speech box at the bottom
        self.draw_box(54 + GameCanvas.view_x, GameCanvas.view_size.y - 40 + GameCanvas.view_y, GameCanvas.view_size.x - 56, 38, True)
        Gfx.set_font(GameCanvas.font_white)
        for b in range(GameCanvas.talk_row):
            GameCanvas.draw_text(GameCanvas.talk_x[0] + GameCanvas.view_x, GameCanvas.talk_y[0] + 16 * b + GameCanvas.view_y, GameCanvas.text_lines[0][b])
        str_ = GameCanvas.text_lines[0][GameCanvas.talk_row][0:GameCanvas.talk_chars]
        GameCanvas.draw_text(GameCanvas.talk_x[0] + GameCanvas.view_x, GameCanvas.talk_y[0] + 16 * GameCanvas.talk_row + GameCanvas.view_y, str_)

    def load_lord_missions(self):  # missions of lord dk -> dz / dA / dB, list dE = dA
        i = 0
        GameCanvas.map_id = GameCanvas.lord_ids[GameCanvas.lord]
        GameCanvas.lord_name = GameCanvas.lord_names[GameCanvas.lord]
        missions = GameCanvas.load_data_file(50)
        GameCanvas.menu_count = GameCanvas.lord_mission_counts[GameCanvas.lord]
        i = 11 * GameCanvas.lord_missions[GameCanvas.lord] + 11
        names = GameCanvas.load_data_file(55)
        for b in range(GameCanvas.menu_count):
            if GameCanvas.lords[b] is None:
                GameCanvas.lords[b] = MissionDef()
            lord = GameCanvas.lords[b]
            lord.id = GameCanvas.u8(missions[i])
            lord.start_x = GameCanvas.u8(missions[i + 1])
            lord.start_y = GameCanvas.u8(missions[i + 2])
            lord.tint = GameCanvas.u8(missions[i + 3])
            lord.boss_type = GameCanvas.u8(missions[i + 4])
            lord.general = GameCanvas.u8(missions[i + 5])
            lord.reward = GameCanvas.u8(missions[i + 6])
            lord.gold = GameCanvas.u8(missions[i + 7])
            lord.time_limit = i16(missions[i + 8] & 0xFF | i8(missions[i + 9]) & 0xFF00)
            lord.level_bonus = GameCanvas.u8(missions[i + 10])
            i += 11
            offset = 3 + (lord.id - 1) * 15
            name_len = 14
            for j in range(14):
                if names[offset + j] == 0:
                    name_len = j
                    break
            GameCanvas.mission_names[b] = GameCanvas.read_utf(names, offset, offset + name_len)
            GameCanvas.mission_portraits[b] = i8(names[17 + (lord.id - 1) * 15])
        GameCanvas.menu_items = GameCanvas.mission_names

    # ---- Visiting: generals (19 list, 20 talk) ---------------------------------------------

    def draw_generals(self):  # generals: Name / Points, 4 per page
        header = ["Name", "Points"]
        i = idiv(GameCanvas.canvas_size.x - 208, 2) + 2
        points_x = i + 134 + 10
        avail_h = GameCanvas.view_size.y - 20 - 20 + 10
        top = 20 + idiv(avail_h - 177, 2) + 2
        row_y = top
        row_sel = GameCanvas.menu[1] % 4
        nth = GameCanvas.menu[1] // 4
        GameCanvas.general_pages[1] = i16(nth + 1)
        nth *= 4
        self.draw_box(i, row_y, 130, 22, False)
        self.draw_box(points_x, row_y, 60, 22, False)
        Gfx.set_font(GameCanvas.font_white)
        GameCanvas.draw_text_centred(i + 65, row_y + 1, header[0])
        GameCanvas.draw_text_centred(points_x + 30, row_y + 1, header[1])
        row_y += 31
        for b in range(4):
            if b == row_sel:
                bool_ = True
                Gfx.set_font(GameCanvas.font_orange)
            else:
                bool_ = False
                Gfx.set_font(GameCanvas.font_white)
            self.draw_box(i, row_y, 130, 22, bool_)
            self.draw_box(points_x, row_y, 60, 22, bool_)
            if nth < GameCanvas.menu_count:
                if GameCanvas.seal != 0:
                    str_ = GameCanvas.general_table.get_string(GameCanvas.generals[2][nth] - 1, 0)
                else:
                    str_ = GameCanvas.general_table.get_string(GameCanvas.generals[0][nth] - 1, 0)
                GameCanvas.draw_text_centred(i + 65, row_y + 1, str_)
                if GameCanvas.seal != 0:
                    j = 0
                    while j < GameCanvas.general_count and GameCanvas.generals[2][nth] != GameCanvas.generals[0][j]:
                        j += 1
                    if j < GameCanvas.general_count:
                        str_ = "" + str(GameCanvas.generals[1][j])
                    else:
                        str_ = "0"
                else:
                    str_ = "" + str(GameCanvas.generals[1][nth])
                GameCanvas.draw_text_centred(points_x + 30, row_y + 1, str_)
            nth += 1
            row_y += 31
        row_y += 6
        self.draw_page_number(GameCanvas.general_pages[1], GameCanvas.general_pages[0], row_y, True)

    def tick_general_talk(self):  # general talk: type the lines gf[], then popups 14 / 16
        if GameCanvas.wait_ticks > 0:
            GameCanvas.wait_ticks = i16(GameCanvas.wait_ticks - 1)
            if GameCanvas.key != 0 and GameCanvas.wait_ticks > 3:
                GameCanvas.wait_ticks = 3
            if GameCanvas.wait_ticks == 0:
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
                pos = 0
            else:
                i = GameCanvas.story_page & 0x1
                pos = GameCanvas.speech_pos[i]
            if GameCanvas.story_page != 4:
                Menus.type_speech(i, pos, 0)
                if len(GameCanvas.speech[i]) <= GameCanvas.speech_pos[i] + 1:
                    if GameCanvas.key != 0:
                        GameCanvas.wait_ticks = 5
                        return
                    GameCanvas.wait_ticks = 15

    def open_general_talk(self):  # open the talk with general cM[1]
        if GameCanvas.seal != 0:
            idx = 2
            b = 0
            while b < GameCanvas.general_count and GameCanvas.generals[0][b] != GameCanvas.generals[2][GameCanvas.menu[1]]:
                b += 1
            GameCanvas.visit_general = i16(b)
            GameCanvas.visit_row = i16(GameCanvas.menu[1])
        else:
            idx = 0
            GameCanvas.visit_general = i16(GameCanvas.menu[1])
        i = GameCanvas.generals[idx][GameCanvas.menu[1]] - 1
        self.set_general(GameCanvas.generals[idx][GameCanvas.menu[1]])
        GameCanvas.general_name = GameCanvas.general_table.get_string(i, 0)
        idx = GameCanvas.general_table.get_int(i, 9)
        picture = GameCanvas.general_table.get_int(i, 8)
        i = GameCanvas.generals[1][GameCanvas.visit_general]
        GameCanvas.story_picture = picture
        GameCanvas.visit_topic = idx
        if Menus.load_greeting(i, idx):
            GameCanvas.speech[0] = ""
            GameCanvas.speech[1] = GameCanvas.talk_lines[0]
            GameCanvas.speech_pos[1] = 0
            GameCanvas.speech_pos[0] = 0
            GameCanvas.story_page = 1
            return True
        return False

    @staticmethod
    def load_greeting(friendship, kind):  # greeting lines of the general -> gf[]
        if GameCanvas.visit_text is not None:
            GameCanvas.visit_text.free()
            GameCanvas.visit_text = None
        GameCanvas.visit_text = ScrTable("/" + GameCanvas.scr_data.get(62))
        if 0 <= friendship <= 100 and GameCanvas.visit_text is not None:
            if kind < 2:
                friendship = min(friendship, 99)
                friendship = friendship // 10 * 3
                if kind == 1:
                    friendship += 30
                lines = 3
                first = 0
            else:
                friendship = 60 + (kind - 2 << 1)
                lines = 2
                first = 3
            for line in range(lines):
                if len(GameCanvas.visit_text.get(friendship)) > 0:
                    str_ = GameCanvas.general_name if (line & 0x1) != 0 else GameCanvas.hero.name
                    GameCanvas.talk_lines[line + first] = "[" + str_ + "] " + GameCanvas.visit_text.get(friendship) + " "
                    friendship += 1
                else:
                    return False
            return True
        return False

    @staticmethod
    def add_friendship(general, amount):  # add paramInt2 friendship to general paramInt1
        b = 0
        while b < GameCanvas.general_count and GameCanvas.generals[0][b] != general:
            b += 1
        if b == GameCanvas.general_count:
            if amount > 0:
                table = ArrTable("/" + GameCanvas.scr_data.get(52))
                for row in range(44):
                    i = table.get_int(row, 0)
                    if i == general:
                        GameCanvas.generals[0][b] = i16(general)
                        GameCanvas.general_count = i16(GameCanvas.general_count + 1)
                        GameCanvas.generals[1][b] = i16(GameCanvas.generals[1][b] + amount)
                        break
        else:
            GameCanvas.generals[1][b] = i16(GameCanvas.generals[1][b] + amount)
            if GameCanvas.generals[1][b] > 200 or GameCanvas.generals[1][b] == 0:
                while b < GameCanvas.general_count:
                    GameCanvas.generals[0][b] = GameCanvas.generals[0][b + 1]
                    GameCanvas.generals[1][b] = GameCanvas.generals[1][b + 1]
                    b += 1
                GameCanvas.general_count = i16(GameCanvas.general_count - 1)
            elif GameCanvas.generals[1][b] >= 100:
                GameCanvas.generals[1][b] = 100
                return 1
        return 0

    def general_gift(self):  # gift of the general after the talk -> fJ, cT[0]
        gift_odds = [[[500, 800, 900, 960, 990, 995, 998], [60, 61, 91, 92, 392, 892, 992],
                         [100, 600, 900, 930, 990, 995, 996], [1, 2, 5, 305, 310, 410, 910]],
                        [[1, 101, 106, 606, 609, 610, 910], [30, 31, 91, 92, 592, 892, 992],
                         [300, 360, 860, 960, 961, 991, 996], [1, 2, 5, 10, 40, 100, 200]]]
        hero = GameCanvas.hero
        if self.rand(100) < GameCanvas.generals[1][GameCanvas.visit_general]:
            i = self.rand(1000)
            GameCanvas.gift_level = 0
            while GameCanvas.gift_level < 7 and i >= gift_odds[GameCanvas.general.gift_table][GameCanvas.gift_kind][GameCanvas.gift_level]:
                GameCanvas.gift_level = i16(GameCanvas.gift_level + 1)
            GameCanvas.popups.lines[4] = ""
            level = GameCanvas.gift_level
            if level == 0:
                i = self.random_general_skill(0)
                if hero.skill_levels[i - 1] < 10:
                    str_ = GameCanvas.edat_string(54, i - 1)
                    hero.skill_levels[i - 1] = hero.skill_levels[i - 1] + 1
                    if hero.skill_levels[i - 1] == 1:
                        GameCanvas.popups.lines[4] = "Skill :"
                        GameCanvas.popup_lines[0] = str_
                        return
                    GameCanvas.popups.lines[4] = "Skill up :"
                    GameCanvas.popup_lines[0] = str_
                    return
            elif level == 1:
                if hero.base_attack < 10000:
                    hero.base_attack += 1
                    GameCanvas.popup_lines[0] = consts.stat_up_texts[0]
                    return
            elif level == 2:
                if hero.base_defense < 10000:
                    hero.base_defense += 1
                    GameCanvas.popup_lines[0] = consts.stat_up_texts[1]
                    return
            elif level == 3:
                if hero.base_hp < 25000:
                    hero.base_hp += 5
                    GameCanvas.popup_lines[0] = consts.stat_up_texts[2]
                    return
            elif level == 4:
                if hero.base_mp < 20000:
                    hero.base_mp += 3
                    GameCanvas.popup_lines[0] = consts.stat_up_texts[3]
                    return
            elif level == 5:
                hero.fame += 10
                GameCanvas.popup_lines[0] = consts.stat_up_texts[4]
                return
            elif level == 6:
                if self.give_item(GameCanvas.engine.random_drop(4), 1) != 0:
                    GameCanvas.popup_lines[0] = GameCanvas.gear_def.name
                    GameCanvas.popups.lines[4] = "Item Acquired!"
                    return
            else:
                i = self.rand(11)
                if self.give_item(i + 1, 1) != 0:
                    GameCanvas.popup_lines[0] = consts.potion_names[i]
                    GameCanvas.popups.lines[4] = "Item Acquired!"
                    return
        GameCanvas.gift_level = 8

    @staticmethod
    def seal_list():
        """the list of "all General Visiting" of 504 Emperor's Seal (fn[2], drawn
        by and visited by bg 3366-3378) is never filled in the original, so the
        Visiting screen showed 44 empty rows; the 44 generals one can visit are visitgen.arr."""
        vg = ArrTable("/visitgen.arr")
        for b in range(44):
            GameCanvas.generals[2][b] = i16(vg.get_int(b, 0))

    @staticmethod
    def load_general_table():
        GameCanvas.general_pages[0] = i16(idiv(GameCanvas.menu_count - 1, 4) + 1)
        if GameCanvas.general_table is None:
            GameCanvas.general_table = ArrTable("/" + GameCanvas.scr_data.get(46))
        return False

    def draw_popup_extras(self):  # popup extras on the map: experience bars of popups 11 / 12
        i = 0
        if GameCanvas.popups.popup_id == 11:
            i = self.draw_exp_bar(GameCanvas.exp_bar_step, 0)
            if i == 0 and GameCanvas.popups.extra == 0:
                GameCanvas.exp_bar_step = i16(GameCanvas.exp_bar_step + 1)
        elif GameCanvas.popups.popup_id == 12:
            i = self.draw_exp_bar(GameCanvas.exp_bar_step, 1)
            if i == 0 and GameCanvas.popups.extra == 0:
                GameCanvas.exp_bar_step = i16(GameCanvas.exp_bar_step + 1)
        if i != 0 and GameCanvas.popups.extra == 0:
            if i == 1:  # the bar is full: level up
                GameCanvas.exp_bars[0] = 0
                GameCanvas.exp_bars[1] = i16(GameCanvas.exp_bars[1] - 100)
                GameCanvas.exp_bars[1] = max(GameCanvas.exp_bars[1], 0)
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

    def draw_exp_bar(self, step, bar):  # experience bar; 1 = full, 2 = done
        colors = [[GameCanvas.rgb(115, 142, 140), GameCanvas.rgb(181, 178, 181), 16777215],
                      [GameCanvas.rgb(99, 0, 0), GameCanvas.rgb(181, 0, 0), GameCanvas.rgb(247, 73, 0)],
                      [GameCanvas.rgb(0, 65, 255), GameCanvas.rgb(0, 146, 255), GameCanvas.rgb(0, 255, 173)],
                      [GameCanvas.rgb(247, 73, 0), GameCanvas.rgb(255, 162, 0), GameCanvas.rgb(255, 223, 0)]]
        if GameCanvas.state == 3:
            GameCanvas.view_y = i16(GameCanvas.view_y - 30)
        y = GameCanvas.view_cy + 37 + GameCanvas.view_y + 20
        rects = [Rect(GameCanvas.view_cx - 51, y, 102, 7),
                     Rect(GameCanvas.view_cx - 50, y, GameCanvas.exp_bars[0], 7),
                     Rect(GameCanvas.view_cx - 50 + GameCanvas.exp_bars[0], y, GameCanvas.exp_bars[1] - GameCanvas.exp_bars[0], 7),
                     Rect(GameCanvas.view_cx - 50 + GameCanvas.exp_bars[1], y, 0, 7)]
        if GameCanvas.state == 3:
            GameCanvas.view_y = i16(GameCanvas.view_y + 30)
        result = 0
        parts = 4 if bar != 0 else 3
        if GameCanvas.exp_bars[bar] + step * 4 > GameCanvas.exp_bars[bar + 1]:
            i = GameCanvas.exp_bars[bar + 1] - GameCanvas.exp_bars[bar]
            result = 2
        else:
            i = step * 4
        if GameCanvas.exp_bars[bar] + i > 100:
            rects[bar + 2].w = 100 - GameCanvas.exp_bars[bar]
            result = 1
        else:
            rects[bar + 2].w = i
        GameCanvas.fill_rect(rects[0], 0)
        rects[0].x += 1
        rects[0].w = 100
        for part in range(parts):
            if rects[part].w > 0:
                for b in range(3):
                    rects[part].y += 1
                    rects[part].h -= 2
                    GameCanvas.fill_rect(rects[part], colors[part][b])
        return result
