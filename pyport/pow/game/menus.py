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

    def a_I(self, paramInt):  # e.java:10-205  (draw the current menu; 1 = first frame, 2 = animation)
        cM = GameCanvas.menu
        if paramInt == 1:
            if cM[0] != 5:
                Gfx.a_Lg(GameCanvas.font_white)
                if GameCanvas.prev_state == 3:
                    Gfx.b_IIIII(7, 19, 225, 242, 0)
                else:
                    self.e_v()
                if cM[0] != 28:
                    if GameCanvas.prev_state == 3:
                        Gfx.a_Lg(GameCanvas.font_white)
                        self.b_TII(GameCanvas.menu_titles[cM[0]], 15, 0)
                    else:
                        self.b_TII(GameCanvas.menu_titles[cM[0]], 2 - GameCanvas.view_y, 0)
                else:
                    str_ = GameCanvas.b_TI(GameCanvas.help_items[0], GameCanvas.help_topic)
                    if GameCanvas.prev_state == 3:
                        Gfx.a_Lg(GameCanvas.font_white)
                        self.b_TII(str_, 15, 0)
                    else:
                        self.b_TII(str_, 2 - GameCanvas.view_y, 0)
                if consts.u[cM[0]] != -1 or (consts.u[cM[0]] == -1 and cM[0] == 15):
                    if cM[0] == 3:
                        GameCanvas.h_II(11, 2)
                    else:
                        GameCanvas.h_II(-1, 2)
            v = cM[0]
            if v == 0:
                GameCanvas.menu_scroll = 0
                GameCanvas.menu_anim = 0
                self.bf_v()
            elif v == 5:
                self.S_v()
                self.aJ()
            elif v in (1, 2, 10, 11, 12, 13, 25, 27):
                self.f_v()
            elif v == 9:
                self.j_v()
            elif v == 28:
                self.l_v()
            elif v == 6:
                self.aK()
            elif v == 7:
                self.aL()
                self.aM()
            elif v in (8, 14):
                self.O_I(1)
            elif v == 29:
                self.aU()
            elif v == 15:
                self.P_I(0)
                self.k_v()
            elif v == 16:
                self.n_II(cM[2], 0)
                self.k_v()
                GameCanvas.h_II(5, -1)
            elif v == 17:
                self.Q_I(0)
                self.k_v()
                GameCanvas.h_II(5, -1)
            elif v == 18:
                self.d_I(0)
                self.k_v()
            elif v in (21, 22, 23, 24):
                self.c_Z(True)
                self.k_v()
            elif v == 3:
                self.aH()
            elif v == 4:
                self.aI()
            elif v == 19:
                self.aN()
            elif v == 20:
                self.b_I(GameCanvas.story_picture)
                if GameCanvas.speech_pos[0] > 0:
                    Menus.a_III(GameCanvas.story_page + 1 & 0x1, 0, 1)
                if GameCanvas.speech_pos[1] > 0:
                    Menus.a_III(GameCanvas.story_page & 0x1, 0, 1)
            if GameCanvas.popups.kind != 0:
                GameCanvas.popups.c_v()
                return
        else:
            if paramInt == 2:
                v = cM[0]
                if v == 0:
                    self.bf_v()
                    return
                if v == 4:
                    Gfx.a_Lg(GameCanvas.font_white)
                    self.e_v()
                    self.aI()
                    GameCanvas.key = -5
                    GameCanvas.wait_ticks = 0
                    self.i_v()
                    GameCanvas.redraw -= 1
                return
            if GameCanvas.popups.kind != 0:
                if GameCanvas.popups.popup_redraw != 0:
                    GameCanvas.popups.c_v()
                    return
            else:
                v = cM[0]
                if v == 0:
                    self.bf_v()
                    return
                if v == 5:
                    self.S_v()
                    self.aJ()
                    return
                if v == 7:
                    self.aM()
                    GameCanvas.f_II(GameCanvas.letter_cursor, GameCanvas.view_cy + 32 + GameCanvas.view_y)
                    return
                if v in (8, 14):
                    if GameCanvas.menu_part != 0:
                        self.O_I(0)
                        return
                    return
                if v == 15:
                    if GameCanvas.menu_part != 0:
                        self.P_I(GameCanvas.menu_part)
                    self.k_v()
                    return
                if v == 16:
                    self.k_v()
                    return
                if v == 17:
                    if GameCanvas.menu_part != 0:
                        self.Q_I(1)
                    self.k_v()
                    return
                if v == 18:
                    if GameCanvas.menu_part != 0:
                        self.d_I(1)
                    self.k_v()
                    return
                if v in (21, 22, 23, 24):
                    self.c_Z(False)
                    self.k_v()
                    return
                if v == 4:
                    self.i_v()
                    return
                if v == 20:
                    self.aO()
                    return

    def a_v(self):  # e.java:207-302  (keys of the menus)
        if GameCanvas.debug_keys:
            GameCanvas.score = -1
        v = GameCanvas.menu[0]
        if v == 4:
            return
        if v == 7:
            i = GameCanvas.r_I(GameCanvas.key)
            if i == -7:
                if len(GameCanvas.name_buf.a_v()) == 0:
                    GameCanvas.menu[0] = 6
                    GameCanvas.redraw = 1
                    return
                GameCanvas.name_buf.a_I(-8)
                return
            if i == -5 or i == 53:
                if GameCanvas.letter_cursor == 26:
                    if len(GameCanvas.name_buf.a_v()) != 0:
                        GameCanvas.hero.name = GameCanvas.name_buf.a_v()
                        GameCanvas.name_buf.a_T(GameCanvas.hero.name)
                        GameCanvas.menu[0] = 8
                        GameCanvas.O_v()
                        GameCanvas.menu_count = 4
                        GameCanvas.aw()
                        return
                else:
                    if len(GameCanvas.name_buf.a_v()) == 0:
                        b = 65
                    else:
                        b = 97
                    GameCanvas.name_buf.a_I(b + GameCanvas.letter_cursor)
                    return
            return
        if v == 20:
            if GameCanvas.key != -5:
                GameCanvas.key = -999
                return
            return
        if v in (21, 22, 23, 24):
            self.aW()
            return
        ch = GameCanvas.key
        if ch in (-1, 50):
            self.aB()
            return
        if ch in (-2, 56):
            self.aC()
            return
        if ch in (-3, 52):
            self.aD()
            return
        if ch in (-4, 54):
            self.aE()
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
            self.b_v()
            return
        elif ch == -6:
            if GameCanvas.menu[0] == 16 or GameCanvas.menu[0] == 17 or GameCanvas.menu[0] == 3:
                self.b_v()
                return
        elif ch == -7:
            self.aF()

    @staticmethod
    def m_II(paramInt1, paramInt2):  # e.java:304-307
        return consts.aW[paramInt1][paramInt2]

    def aB(self):  # e.java:309-392  (UP)
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
            self.T_I(0)
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 0:
                cM[1] = GameCanvas.menu_count - 1
            self.T_I(1)
            return
        if v == 9:
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 1:
                cM[1] = GameCanvas.menu_count - 1
            if not GameCanvas.sound_on and cM[1] == 1:
                cM[1] = 0
            GameCanvas.I_v()
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
        GameCanvas.I_v()
        GameCanvas.redraw = 1

    def aC(self):  # e.java:394-480  (DOWN)
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
            self.T_I(0)
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= GameCanvas.menu_count:
                cM[1] = 0
            self.T_I(1)
            return
        if v == 9:
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= GameCanvas.menu_count:
                cM[2] = 0
                cM[1] = 0
            if not GameCanvas.sound_on and cM[1] == 1:
                cM[1] = 2
            GameCanvas.I_v()
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
        GameCanvas.I_v()
        GameCanvas.redraw = 1

    def aD(self):  # e.java:482-584  (LEFT)
        cM = GameCanvas.menu
        v = cM[0]
        if v == 1:
            if GameCanvas.debug_keys and GameCanvas.chapter > 0:
                GameCanvas.chapter = i8(GameCanvas.chapter - 1)
                self.C_v()
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
            self.y_I(0)
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

    def aE(self):  # e.java:586-686  (RIGHT)
        cM = GameCanvas.menu
        v = cM[0]
        if v == 1:
            if GameCanvas.debug_keys and GameCanvas.chapter < 44:
                GameCanvas.chapter = i8(GameCanvas.chapter + 1)
                self.C_v()
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
            self.y_I(1)
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

    def b_v(self):  # e.java:688-1000  (FIRE)
        cM = GameCanvas.menu
        if cM[0] == 9:
            self.y_I(1)
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
                GameCanvas.popups.e_I(41)
                return
            elif v == 7:
                GameCanvas.popups.e_I(42)
                return
            elif v == 8:
                GameCanvas.popups.e_I(28)
                GameCanvas.redraw = 1
                return
            arrayOfInt = [0, 1, 3, 4, 5]
            cM[1] = arrayOfInt[cM[1]]
        if Menus.m_II(cM[0], cM[1] % 7) > -1:
            self.c_v()
            GameCanvas.menu_count = consts.v[cM[0]]
            c0 = cM[0]
            if c0 == 7:
                GameCanvas.hero.name = ""
            elif c0 == 9:
                GameCanvas.ai()
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
                GameCanvas.O_v()
            elif c0 == 15:
                cM[3] = 1
                GameCanvas.images[37] = self.d_T(GameCanvas.scr_ui.a_I(44))
                GameCanvas.images[38] = self.d_T(GameCanvas.scr_ui.a_I(45))
            elif c0 == 17:
                cz = GameCanvas.hero
                if GameCanvas.menu_return == 16 and cz.equipped[cM[2]].id != 0:
                    for b in range(25):
                        if 0 == cz.backpack[b].id:
                            self.a_LzLz(cz.equipped[cM[2]], cz.backpack[b])
                self.ag()
            elif c0 in (21, 22, 23, 24):
                self.aY()
            elif c0 == 1:
                Menus.aG()
                self.C_v()
            elif c0 == 3:
                GameCanvas.mission = i16(cM[1])
                self.D_v()
            elif c0 == 20:
                self.bg_v()
            cM[2] = 0
            cM[1] = 0
            return
        v = cM[0]
        if v == 0:
            if cM[1] == 3:
                if GameCanvas.general_count == 0:
                    GameCanvas.popups.e_I(35)
                    return
                if GameCanvas.hero.live_registered != 0 and GameCanvas.general_count != 0:
                    self.c_v()
                    cM[0] = 19
                    GameCanvas.seal = i16(GameCanvas.L_I(504))
                    if GameCanvas.seal != 0 and config.ORIG_BUG["B3"]:
                        Menus.seal_list()
                    if GameCanvas.seal != 0:
                        GameCanvas.menu_count = 44
                    else:
                        GameCanvas.menu_count = GameCanvas.general_count
                    Menus.bh_v()
                    cM[2] = 0
                    cM[1] = 0
                    return
                GameCanvas.popups.e_I(35)
                GameCanvas.redraw = 0
                GameCanvas.menu_scroll = 0
                GameCanvas.menu_anim = 0
                return
            if cM[1] == 2:
                GameCanvas.live.g_v()
                GameCanvas.redraw = 0
                GameCanvas.menu_scroll = 0
                GameCanvas.menu_anim = 0
                return
        elif v == 5:
            GameCanvas.redraw = 1
            if cM[1] == 0:
                if GameCanvas.aq():
                    self.U_v()
                    if GameCanvas.live_saved != 0:
                        return
                    GameCanvas.ai()
                    self.F_v()
                    self.c_v()
                    GameCanvas.menu_anim = 0
                    GameCanvas.menu_scroll = 0
                    cM[0] = 0
                    GameCanvas.menu_count = consts.v[cM[0]]
                    GameCanvas.menu_items = GameCanvas.game_menu_items
                    cM[2] = 0
                    cM[1] = 0
                    self.aA()
                    if GameCanvas.save_flag != 0:  # e.java:856-866  (the save was made on the map: back into it)
                        self.C_v()
                        self.bi_v()
                        self.D_v()
                        self.y_v()
                        self.U_v()
                        GameCanvas.clock[1] = GameCanvas.B_v()
                        GameCanvas.clock[0] = GameCanvas.B_v()
                        GameCanvas.play_time = GameCanvas.clock[0] - GameCanvas.play_time
                        self.a__I(-1)
                        return
                return
            if cM[1] == 1:
                GameCanvas.name_buf = None
                GameCanvas.name_buf = NameBuffer("", 8, 10)
                if GameCanvas.aq():
                    GameCanvas.popups.e_I(3)
                    return
                self.au()
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
                    GameCanvas.popups.e_I(4)
                    GameCanvas.redraw = 1
                    return
        elif v == 29:
            GameCanvas.popups.e_I(36)
        elif v == 10:
            if cM[1] == 2:
                GameCanvas.popups.e_I(5)
                return
        elif v == 11:
            if cM[1] == 0:
                if self.ar() != 0:
                    GameCanvas.popups.e_I(0)
            return
        elif v == 25:
            if (GameCanvas.score & 1 << cM[1]) != 0:
                self.c_v()
                self.l_II(cM[1], 0)
                return
            GameCanvas.popups.a_T("3You must first complete|the missions needed|to view this ending.")
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
                b = GameCanvas.g_I(it.id)
                if GameCanvas.m_I(it.id) <= cz.level:
                    if it.id == 434:
                        it.id = 0
                        cz.base_hp += 5
                        GameCanvas.popups.e_I(23)
                    elif it.id == 435:
                        it.id = 0
                        cz.base_mp += 3
                        GameCanvas.popups.e_I(24)
                    elif it.id == 436:
                        it.id = 0
                        cz.base_defense += 1
                        GameCanvas.popups.e_I(25)
                    elif it.id == 437:
                        it.id = 0
                        cz.base_attack += 1
                        GameCanvas.popups.e_I(26)
                    elif it.id in (502, 504):
                        GameCanvas.popups.e_I(17)
                    else:
                        self.a_LzLz(it, cz.equipped[consts.aE[b]])
                else:
                    GameCanvas.popups.e_I(17)
            GameCanvas.menu_part = 1
            return
        elif v == 1:
            if (GameCanvas.missions_done & 1 << GameCanvas.lord_ids[cM[1]] - 1) != 0:
                self.c_v()
                cM[0] = 2
                GameCanvas.menu_count = consts.v[cM[0]]
                GameCanvas.lord = i16(i8(cM[1]))
                self.bi_v()
                cM[2] = 0
                cM[1] = 0
                return
        elif v == 3:
            GameCanvas.popups.e_I(6)
            return

    def aF(self):  # e.java:1002-1109  (BACK)
        cM = GameCanvas.menu
        bool_ = False
        if consts.u[cM[0]] > -1:
            if cM[0] in (14, 15, 16, 17, 18):
                self.ar()
            if consts.u[cM[0]] > 99:
                GameCanvas.help_topic = 0
                if cM[0] == 28 and GameCanvas.menu_return == 5:
                    GameCanvas.help_topic = 7
                    bool_ = True
                cM[0] = GameCanvas.menu_return
                if cM[0] == 0:
                    GameCanvas.menu_anim = 0
                    GameCanvas.menu_scroll = 0
                GameCanvas.ap()
                GameCanvas.ak()
                if bool_:
                    cM[1] = 5
                    return
            else:
                if cM[0] == 1:
                    self.F_v()
                cM[0] = consts.u[cM[0]]
                if cM[0] == 0:
                    GameCanvas.menu_anim = 0
                    GameCanvas.menu_scroll = 0
                GameCanvas.ap()
                GameCanvas.ak()
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
                GameCanvas.aj()
                Menus.aG()
                self.ae_v()
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
                    GameCanvas.ap()
                    GameCanvas.images[37] = None
                    GameCanvas.images[38] = None
                    self.ar()
                    return
                cM[3] = 1
                GameCanvas.menu_part = 6
                return
            if v == 27:
                cM[0] = GameCanvas.menu_before_talk
                GameCanvas.ap()
                GameCanvas.ak()

    @staticmethod
    def aG():  # e.java:1111-1118
        GameCanvas.anim_step = 0
        while GameCanvas.anim_step < 4:
            GameCanvas.images[26 + GameCanvas.anim_step] = None
            GameCanvas.anim_step += 1
        GameCanvas.carousel_image = None

    def c_v(self):  # e.java:1120-1127  (remember cursor, go to the sub-menu)
        cM = GameCanvas.menu
        GameCanvas.menu_return = cM[0]
        GameCanvas.menu_cursors[cM[0]] = i16(cM[1])
        GameCanvas.menu_tops[cM[0]] = i16(cM[2])
        cM[0] = Menus.m_II(cM[0], cM[1] % 7)
        GameCanvas.redraw = 1
        GameCanvas.menu_part = 0

    def d_v(self):  # e.java:1129-1139
        GameCanvas.images[17] = None
        GameCanvas.images[10] = None
        GameCanvas.gear_data = None
        GameCanvas.rare_data = None
        GameCanvas.treasure_data = None
        for b in range(1, 4):
            GameCanvas.images[0 + b] = None
        GameCanvas.sparkle = None
        Menus.aG()

    def e_v(self):  # e.java:1141-1143  (menu background ct[7])
        self.a_MIIIIII(GameCanvas.images[7], 0, 0, GameCanvas.canvas_size.x, GameCanvas.canvas_size.y, 0, 0)

    def f_v(self):  # e.java:1145-1227  (vertical list menu: 1 2 10 11 12 13 25 27)
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
                Gfx.a_Lg(GameCanvas.font_orange)
            else:
                bool_ = False
                Gfx.a_Lg(GameCanvas.font_white)
            m = i
            self.a_IIIIZ(m, j_ + GameCanvas.view_y, 180, 20, bool_)
            if GameCanvas.state == 2:
                if cM[0] == 0:
                    if cM[2] + b1 == 3 and (0 == GameCanvas.hero.live_registered or GameCanvas.general_count == 0):
                        Gfx.a_Lg(GameCanvas.font_gray)
                elif cM[0] == 1:
                    if GameCanvas.debug_keys:
                        GameCanvas.missions_done = -1
                    if 0 == (GameCanvas.missions_done & 1 << GameCanvas.lord_ids[cM[2] + b1] - 1):
                        Gfx.a_Lg(GameCanvas.font_gray)
                elif cM[0] == 25:
                    if 0 == (GameCanvas.score & 1 << cM[2] + b1):
                        Gfx.a_Lg(GameCanvas.font_gray)
            else:
                if GameCanvas.map_mode.mode == 1:
                    if cM[2] + b1 == 2 and (GameCanvas.actor_count > 0 or GameCanvas.boss_fight != 0 or GameCanvas.waves[0] != 0):
                        Gfx.a_Lg(GameCanvas.font_gray)
            if cM[0] == 25:
                if cM[2] + b1 < 24:
                    arrayOfByte1 = self.d_II(54, 38 + cM[2] + b1)
                    str_ = GameCanvas.a_ABII(arrayOfByte1, 0, len(arrayOfByte1))
                    self.b_TII(str_, j_ - 1, 18)
            elif cM[0] in (0, 10, 12, 13, 27):
                self.b_TII(GameCanvas.b_TI(GameCanvas.menu_items[0], b1 + cM[2]), j_ - 1, 0)
            else:
                self.b_TII(GameCanvas.menu_items[b1 + cM[2]], j_ - 1, b)
            j_ += 30
        if cM[0] == 25:
            self.a_IIIZ(cM[2] // 5 + 1, 5, GameCanvas.canvas_size.y - 35, True)
        elif cM[2] != 0 or cM[2] + 5 < GameCanvas.menu_count - 1:
            self.f_III(2, GameCanvas.view_cx - 8 - GameCanvas.view_x, k - 10 - 5)
            self.f_III(3, GameCanvas.view_cx - 8 - GameCanvas.view_x, j_ - 5)
        if cM[0] == 10:
            Gfx.a_MIII(GameCanvas.softkey_bg, 120, GameCanvas.view_y + 15, 17)
            Gfx.a_Lg(GameCanvas.font_white)
            self.b_TII("PAUSE", 13, 0)
        if GameCanvas.debug_keys and cM[0] == 1:
            Gfx.a_Lg(GameCanvas.font_white)
            Gfx.b_IIIII(GameCanvas.screen_w // 2 - 16, GameCanvas.screen_h - 17, 32, 17, 0)
            Gfx.a_TIII("" + str(GameCanvas.chapter + 1), GameCanvas.screen_w // 2, GameCanvas.screen_h - 16, 1)

    def j_v(self):  # e.java:1471-1521  (Options: Sound / Volume / Speed)
        i = GameCanvas.view_cy - 50
        if GameCanvas.menu[1] == 0:
            GameCanvas.menu[1] = 1
        for b in range(1, 3):
            if GameCanvas.menu[1] == b:
                bool_ = True
                Gfx.a_Lg(GameCanvas.font_orange)
            elif b == 3:
                bool_ = False
                Gfx.a_Lg(GameCanvas.font_gray)
            else:
                bool_ = False
                Gfx.a_Lg(GameCanvas.font_white)
            self.a_IIIIZ(GameCanvas.view_cx - 100, i + GameCanvas.view_y, 80, 20, bool_)
            self.a_IIIIZ(GameCanvas.view_cx - 10, i + GameCanvas.view_y, 110, 20, bool_)
            GameCanvas.c_TII(GameCanvas.option_names[b], GameCanvas.view_cx - 100 + 40 - GameCanvas.view_x, i + 1)
            if bool_:
                self.f_III(0, GameCanvas.view_cx - 10 - GameCanvas.view_x, i + 2)
                self.f_III(1, GameCanvas.view_cx - 10 + 110 - 10 - 1 - GameCanvas.view_x, i + 2)
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
            GameCanvas.c_TII(str_, GameCanvas.view_cx + 156 - 111 - GameCanvas.view_x, i + 1)
            i += 10
            i += 20

    def l_v(self):  # e.java:2311-2348  (Help / About page cM[1] of topic ej)
        if GameCanvas.state == 3 or GameCanvas.prev_state == 3:
            GameCanvas.view_cy -= 30
        i = GameCanvas.menu[1] + consts.z[GameCanvas.help_topic]
        arrayOfByte = self.d_II(61, i)
        if GameCanvas.state == 2:
            self.b_ABII(arrayOfByte, 190, 0)
            self.e_IIII(GameCanvas.view_cx - 100 + GameCanvas.view_x, GameCanvas.view_cy - 90 + GameCanvas.view_y, 200, 175)
        else:
            self.b_ABII(arrayOfByte, 190, 0)
            self.e_IIII(GameCanvas.view_cx - 100, GameCanvas.view_cy - 70 + GameCanvas.view_y, 200, 120)
        Gfx.a_Lg(GameCanvas.font_white)
        for b in range(GameCanvas.text_line_count[0] + 1):
            if GameCanvas.state == 2:
                if GameCanvas.menu[0] == 28 and GameCanvas.help_topic == 8:
                    self.b_TII(GameCanvas.text_lines[0][b], GameCanvas.view_cy - 80 + b * 20 + 3, 30)
                    if GameCanvas.menu[1] == 1:
                        self.b_TII("v" + GameCanvas.app_version, GameCanvas.view_cy - 80 + 20 + 3, 30)
                else:
                    GameCanvas.d_TII(GameCanvas.text_lines[0][b], GameCanvas.view_cx - 95 - 1, GameCanvas.view_cy - 80 + b * 20 + 3)
            else:
                GameCanvas.d_TII(GameCanvas.text_lines[0][b], GameCanvas.view_cx - 90 - 1 - GameCanvas.view_x, GameCanvas.view_cy - 62 + b * 15)
        n = consts.z[GameCanvas.help_topic + 1] - consts.z[GameCanvas.help_topic]
        if GameCanvas.state == 2:
            if GameCanvas.prev_state == 3:
                self.a_IIIZ(GameCanvas.menu[1] + 1, n, GameCanvas.canvas_size.y - 100, True)
            else:
                self.a_IIIZ(GameCanvas.menu[1] + 1, n, GameCanvas.canvas_size.y - 35, True)
        else:
            self.a_IIIZ(GameCanvas.menu[1] + 1, n, GameCanvas.view_cy + 65, True)
        if GameCanvas.state == 3 or GameCanvas.prev_state == 3:
            GameCanvas.view_cy += 30

    def a_IIIZ(self, paramInt1, paramInt2, paramInt3, paramBoolean):  # e.java:2350-2372  (page "n / m" with arrows)
        if paramInt2 == 1:
            return
        i = GameCanvas.view_cx - 25 - 10
        if paramInt2 > 1:
            if paramInt1 != 1 or paramBoolean:
                self.f_III(0, i, paramInt3)
            i += 60
            if paramInt1 != paramInt2 or paramBoolean:
                self.f_III(1, i, paramInt3)
        paramInt3 += 2
        i = GameCanvas.view_cx - (8 + 9 * ((2 if paramInt2 > 9 else 1) + (2 if paramInt1 > 9 else 1)) + 2) // 2
        i = i + (18 if paramInt1 > 9 else 9)
        self.e_III(paramInt1, i, paramInt3 + GameCanvas.view_y)
        i += 1
        if GameCanvas.prev_state == 3:
            GameCanvas.a_IIIIMII(i - GameCanvas.view_x, paramInt3 + 16, 8, 12, GameCanvas.images[20], 90, 0)
        else:
            GameCanvas.a_IIIIMII(i - GameCanvas.view_x, paramInt3, 8, 12, GameCanvas.images[20], 90, 0)
        i += 9 + (18 if paramInt2 > 9 else 9)
        self.e_III(paramInt2, i, paramInt3 + GameCanvas.view_y)

    def P_I(self, paramInt):  # e.java:1523-1593  (Skills: 5 hot-key slots + skill tree pages)
        cz = GameCanvas.hero
        cM = GameCanvas.menu
        arrayOfByte = [1, 3, 7, 9, 0]
        if 0 == paramInt:
            for b in range(5):
                self.i_II(40 + b * 30 + 4 * b, 60)
                self.d_IIII(arrayOfByte[b], 40 + b * 30 + 18 + 4 * b, 70, 0)
        if paramInt % 2 == 0:
            for b in range(5):
                self.i_II(40 + b * 30 + 4 * b, 90)
                if cz.hotkeys[b] != 0:
                    self.b_MIIIIII(GameCanvas.images[37], 40 + b * 30 + 4 * b + 1, 91, 28, 28, (cz.hotkeys[b] - 12) * 28, 0)
            self.b_IIIIIII(40 + cM[1] * 30 + 4 * cM[1], 90, 30, 30, 255, 255, 255)
        arrayOfAc = [Rect(40, 140, 60, 20), Rect(40, 165, 60, 20)]
        if paramInt % 3 == 0:
            i = cM[2] // 6 << 1
            b2 = 2 if cM[2] < 18 else 1
            for b1 in range(b2):
                j_ = cM[2] // 6 * 6 + b1 * 3
                ac1 = arrayOfAc[b1]
                ac1.y = ac1.y + b1 * 10 + 5
                self.b_IIIIIII(ac1.x - 1, ac1.y - 1, ac1.w + 2, ac1.h + 2, 152, 152, 152)
                GameCanvas.a_LacI(ac1, 0)
                Gfx.a_Lg(GameCanvas.font_white)
                GameCanvas.text_width = GameCanvas.c_T(GameCanvas.skill_names[i + b1])
                GameCanvas.d_TII(GameCanvas.skill_names[i + b1], ac1.x + idiv(ac1.w - GameCanvas.text_width, 2), ac1.y + 1)
                for b in range(3):
                    self.i_II(40 + (b + 2) * 34, 140 + 35 * b1)
                    if consts.aC[j_ + b] != 0:
                        if cz.skill_levels[consts.aC[j_ + b] - 12] != 0:
                            image = GameCanvas.images[37]
                        else:
                            image = GameCanvas.images[38]
                        self.b_MIIIIII(image, 40 + (b + 2) * 34 + 1, 140 + 35 * b1 + 1, 28, 28,
                                       (consts.aC[j_ + b] - 12) * 28, 0)
            if cM[3] == 2:
                # DECOMP-FIX F10: `35 * cM[2] % 6 / 3` -> `35 * (cM[2] % 6 / 3)`
                row = 35 * (cM[2] % 6 // 3) if F10 else 35 * cM[2] % 6 // 3
                self.b_IIIIIII(40 + (cM[2] % 3 + 2) * 34, 140 + row, 30, 30, 255, 255, 255)
            ac_ = Rect(210, 0, 3, 20)
            self.a_IIIIZ(210, 150, 3, 50, False)
            if i == 6:
                ac_.x = 210
                ac_.y = 152
                ac_.w = 3
                ac_.h = 46
                GameCanvas.a_LacI(ac_, GameCanvas.k_III(231, 227, 198))
            else:
                ac_.y = 151 + (i >> 1) * 14 + GameCanvas.view_y
                GameCanvas.a_LacI(ac_, GameCanvas.k_III(231, 227, 198))
        # System.out.println("GameCanvas.DrawSkillSet(2)");
        if cM[3] == 1:
            self.b_IIIII(cz.hotkeys[cM[1]] + 2000, GameCanvas.view_cx - 100, GameCanvas.canvas_size.y - 70, 200, 22)
        else:
            self.b_IIIII(consts.aC[cM[2]] + 2000, GameCanvas.view_cx - 100, GameCanvas.canvas_size.y - 70, 200, 22)
        GameCanvas.menu_part = 0

    def k_v(self):  # e.java:1595-1630  (description strip; scrolls when longer than the box)
        dF = GameCanvas.info_box
        self.a_IIIIZ(dF.rect.x + GameCanvas.view_x, dF.rect.y + GameCanvas.view_y, dF.rect.w, dF.rect.h, False)
        Gfx.a_Lg(GameCanvas.font_white)
        if dF.shown != 0:
            GameCanvas.text_width = GameCanvas.c_T(dF.text)
            dF.text_x = i16(dF.text_x - 5)
            if dF.rect.x - dF.text_x > GameCanvas.text_width + 3:
                dF.text_x = i16(dF.rect.x + dF.rect.w)
        GameCanvas.d_TII(dF.text, dF.text_x, dF.rect.y + (dF.rect.h - 11 >> 1) - 2)
        i = (GameCanvas.screen_w - dF.rect.w) // 2
        j_ = dF.rect.y + GameCanvas.view_y
        s1 = 0
        s2 = 0
        if GameCanvas.state == 3:
            s1 = GameCanvas.view_x
            s2 = GameCanvas.view_y
            Gfx.b_IIIII(0, j_, i, dF.rect.h, 0)
            Gfx.b_IIIII(GameCanvas.screen_w - i, j_, i, dF.rect.h, 0)
        self.a_MIIIIII(GameCanvas.images[7], 0, j_, i, dF.rect.h, -s1, j_ - s2)
        Gfx.c_IIIII(i - 1, j_, i - 1, j_ + dF.rect.h - 1, GameCanvas.k_III(80, 80, 80))
        self.a_MIIIIII(GameCanvas.images[7], GameCanvas.screen_w - i, j_, i - s1, dF.rect.h, GameCanvas.screen_w - i - s1, j_ - s2)
        Gfx.c_IIIII(GameCanvas.screen_w - i, j_, GameCanvas.screen_w - i, j_ + dF.rect.h - 1, GameCanvas.k_III(80, 80, 80))
        if GameCanvas.state == 3:
            Gfx.a_IIII(0, j_, GameCanvas.screen_w, dF.rect.h)
            GameCanvas.scene.b_v()
            Gfx.a_v()
            Gfx.a_IIII(0, j_, i - 1, dF.rect.h)
            GameCanvas.popups.b_I(170)
            Gfx.a_v()
            Gfx.a_IIII(GameCanvas.screen_w - i + 1, j_, i - 1, dF.rect.h)
            GameCanvas.popups.b_I(170)
            Gfx.a_v()

    def n_II(self, paramInt1, paramInt2):  # e.java:1632-1654  (Gear: hero sprite + 9 equipment slots)
        cz = GameCanvas.hero
        arrayOfByte1 = [-77, -77, -77, -33, 3, 47, 47, 47, -15]
        arrayOfByte2 = [21, -15, -51, -79, -79, -51, -15, 21, 49]
        GameCanvas.images[39] = self.d_T(GameCanvas.scr_ui.a_I(50))
        ct39 = GameCanvas.images[39]
        self.b_MIIIIII(ct39, GameCanvas.view_cx - ct39.getWidth() // 2, GameCanvas.view_cy - ct39.getHeight() // 2,
                       ct39.getWidth(), ct39.getHeight(), 0, 0)
        GameCanvas.images[39] = None
        for b in range(9):
            if cz.equipped[b].id != 0:
                self.e_I(cz.equipped[b].id)
                self.g_IIII(cz.equipped[b].id, GameCanvas.view_cx + arrayOfByte1[b], GameCanvas.view_cy + arrayOfByte2[b], 0)
        self.b_IIIIIII(GameCanvas.view_cx + arrayOfByte1[paramInt1] - 1, GameCanvas.view_cy + arrayOfByte2[paramInt1] - 1, 30, 30, 255, 255, 255)
        GameCanvas.cursor[24] = GameCanvas.view_cx + arrayOfByte1[paramInt1] + GameCanvas.view_x + 7
        GameCanvas.cursor[25] = GameCanvas.view_cy + arrayOfByte2[paramInt1] + GameCanvas.view_y + 7
        f1 = cz.body_frames[1]
        self.b_MIIIIII(cz.body_image, GameCanvas.view_cx - f1.ox, GameCanvas.view_cy + 7 - f1.oy + 17, f1.w, f1.h, f1.src_x, f1.src_y)
        f2 = cz.head_frames[1]
        self.b_MIIIIII(cz.head_image, GameCanvas.view_cx - f2.ox, GameCanvas.view_cy + 7 - f2.oy + 17, f2.w, f2.h, f2.src_x, f2.src_y)
        if paramInt2 != 0:
            GameCanvas.a_LzZI(self.o_I(-1), True, -1)
            return
        self.b_IIIII(paramInt1 + 1000, GameCanvas.view_cx - 79, GameCanvas.view_cy + 81 + 5, 158, 20)

    def Q_I(self, paramInt):  # e.java:1656-1692  (Inventory: 5x5 grid in 2 pages + gold)
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
            self.b_MIIIIII(GameCanvas.images[7], GameCanvas.view_cx - 75, GameCanvas.view_cy - 45, 150, 100, GameCanvas.view_cx - 75, GameCanvas.view_cy - 45)
        for b1 in range(b2):
            for b in range(5):
                self.i_II(arrayOfInt1[b] + GameCanvas.view_x, arrayOfInt2[b1] + GameCanvas.view_y)
                self.e_I(cz.backpack[b3 + b1 * 5 + b].id)
                self.g_IIII(cz.backpack[b3 + b1 * 5 + b].id, arrayOfInt1[b] + 1, arrayOfInt2[b1] + 1, 0)
        GameCanvas.a_LacI(ac_, GameCanvas.k_III(148, 148, 148))
        ac_.x += 1
        ac_.y += 1
        ac_.w -= 2
        ac_.h -= 2
        GameCanvas.a_LacI(ac_, GameCanvas.k_III(33, 0, 0))
        ac_.y = GameCanvas.view_cy - 39 + (39 if b3 != 0 else 0) + GameCanvas.view_y
        ac_.h = 39
        GameCanvas.a_LacI(ac_, GameCanvas.k_III(231, 227, 198))
        self.b_IIIII(cM[2] + 1100, GameCanvas.view_cx - 75, GameCanvas.view_cy + 50, 150, 22)
        self.b_IIIIIII(arrayOfInt1[cM[2] % 5], arrayOfInt2[(cM[2] - b3) // 5] + GameCanvas.view_y, 30, 30, 255, 255, 255)
        if 0 == paramInt:
            self.J_v()
        GameCanvas.menu_part = 0

    def d_I(self, paramInt):  # e.java:3022-3058  (Assign Items: 5 potion slots, * and # quick keys)
        cz = GameCanvas.hero
        if GameCanvas.state == 3:
            GameCanvas.view_cy -= 30
        if 0 == paramInt:
            self.J_v()
            Gfx.a_Lg(GameCanvas.font_white)
            for b1 in range(5):
                self.a_IIIIZ(GameCanvas.view_cx - 80 + 32 * b1, GameCanvas.view_cy - 40 + GameCanvas.view_y, 30, 22, False)
                if cz.quick_keys[0] == b1:
                    GameCanvas.d_TII(" * ", GameCanvas.view_cx - 80 + 32 * b1 - GameCanvas.view_x, GameCanvas.view_cy - 38)
                elif cz.quick_keys[1] == b1:
                    GameCanvas.d_TII(" # ", GameCanvas.view_cx - 80 + 32 * b1 - GameCanvas.view_x, GameCanvas.view_cy - 38)
        for b in range(5):
            if GameCanvas.state == 3:
                self.a_IIIIZ(GameCanvas.view_cx - 79 + 32 * b, GameCanvas.view_cy + 6, 28, 28, False)
                self.g_IIII(cz.quick_slots[b].item, GameCanvas.view_cx - 79 + 32 * b - GameCanvas.view_x, GameCanvas.view_cy + 6 - GameCanvas.view_y, b)
            else:
                self.a_IIIIZ(GameCanvas.view_cx - 79 + 32 * b, GameCanvas.view_cy - 10, 28, 28, False)
                self.g_IIII(cz.quick_slots[b].item, GameCanvas.view_cx - 79 + 32 * b - GameCanvas.view_x, GameCanvas.view_cy - 10 - GameCanvas.view_y, b)
        if GameCanvas.state == 3:
            self.b_IIIIIII(GameCanvas.view_cx - 80 + 32 * GameCanvas.menu[1], GameCanvas.view_cy + 6, 30, 29, 255, 255, 255)
        else:
            self.b_IIIIIII(GameCanvas.view_cx - 80 + 32 * GameCanvas.menu[1], GameCanvas.view_cy - 10, 30, 29, 255, 255, 255)
        GameCanvas.menu_part = 0
        self.b_IIIII(GameCanvas.menu[1] + 1200, GameCanvas.view_cx - 80 - GameCanvas.view_x, GameCanvas.view_cy + 30, 160, 22)
        self.a_IIIIZ(GameCanvas.view_cx - 80, GameCanvas.view_cy + 60 + GameCanvas.view_y, 160, 22, False)
        Gfx.a_Lg(GameCanvas.font_white)
        self.b_TII("*,# key Assign", GameCanvas.view_cy + 60, 15)
        if GameCanvas.state == 3:
            GameCanvas.view_cy += 30

    def g_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # e.java:3060-3081  (item icon)
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
            self.b_MIIIIII(GameCanvas.images[0 + b], paramInt2, paramInt3, 28, 28, i * 28, 0)
            if paramInt1 < 100:
                self.i_III(paramInt2, paramInt3 + 2, GameCanvas.hero.quick_slots[paramInt4].count)

    # ---- Blacksmith (screens 21 Buy, 22 Sell, 23 Enchant, 24 Combine) ----------------------
    # fK[0] = mode (cM[0]-21), fK[9]/fK[10] = cursor col/row, fK[18] = cell, fK[19] = item id,
    # fK[20] = message for aV(), fK[21] = price, fK[26] = sparkle frame (-1 idle), fK[27] = 1 on Gear

    def a_IAzAI(self, paramInt, paramArrayOfz, paramArrayOfint):  # e.java:1804-1861  (item grid)
        i = GameCanvas.cursor[8] * 5
        if GameCanvas.cursor[11] == 1:
            ac1 = Rect(0, 0, 0, 0)
            ac2 = Rect(0, 0, 0, 0)
            ac1.w = 4
            ac1.x = GameCanvas.cursor[12]
            ac1.h = GameCanvas.cursor[6]
            ac1.y = paramInt
            GameCanvas.a_LacII(ac1, 16777215, 0)
            ac1.w -= 2
            ac1.x += 1
            ac1.h -= 2
            ac1.y += 1
            j_ = GameCanvas.cursor[8] * 32
            k = ac2.h
            j_ = idiv(j_ * k, GameCanvas.cursor[7])
            ac2.h = GameCanvas.cursor[13]
            ac2.y += j_
            GameCanvas.a_LacI(ac2, 16777215)
            GameCanvas.b_LacI(ac1, 10000536)
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
                self.a_IIZ(j_, paramInt, bool_)
                if paramArrayOfint is not None:
                    self.a_IIII(paramArrayOfint[i], j_, paramInt, 0)
                else:
                    self.a_IIIAz(i, j_, paramInt, paramArrayOfz)
                j_ += 32
                i += 1
            paramInt += 32
            b1 += 1

    def a_IIIAz(self, paramInt1, paramInt2, paramInt3, paramArrayOfz):  # e.java:1863-1877
        if paramArrayOfz is not None:
            z1 = paramArrayOfz[paramInt1]
        else:
            z1 = self.o_I(paramInt1)
        if GameCanvas.cursor[0] == 1 and 0 < z1.id < 100:
            bool_ = z1.attack
        else:
            bool_ = 0
        self.a_IIII(z1.id, paramInt2, paramInt3, bool_)

    def a_IIZ(self, paramInt1, paramInt2, paramBoolean):  # e.java:1879-1881  (grid cell frame)
        GameCanvas.a_IIIIIIIZ(paramInt1 + 1, paramInt2 + 1, 26, 26, 0, 0, 16777215 if paramBoolean else 5263440, True)

    def a_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # e.java:1883-1902  (item icon by id + count)
        if paramInt1 > 500:
            image = GameCanvas.images[3]
            i = paramInt1 - 501
        elif paramInt1 > 300:
            image = GameCanvas.images[2]
            i = GameCanvas.item_tables[1].a_II(paramInt1 - 301, 7)
        elif paramInt1 > 100:
            image = GameCanvas.images[1]
            i = GameCanvas.item_tables[0].a_II(paramInt1 - 101, 7)
        else:
            image = GameCanvas.images[0]
            i = paramInt1 - 1
        GameCanvas.a_IIIIMII(paramInt2, paramInt3, 28, 28, image, i * 28, 0)
        if paramInt4 > 0:
            GameCanvas.a_IIIIMII(paramInt2, paramInt3, 9, 12, GameCanvas.images[20], paramInt4 * 9, 0)

    def aP(self):  # e.java:1904-1910  (gold + item grid + description)
        i = GameCanvas.cursor[1] + 1
        self.i_I(i)
        i += 29
        self.a_IAzAI(i, None, None)
        GameCanvas.a_LzZI(self.o_I(-1), True, -1)

    def c_Z(self, paramBoolean):  # e.java:1912-2111  (decompiler gave bytecode only; rebuilt from it)
        fK = GameCanvas.cursor
        if paramBoolean:
            if fK[27] == 0:
                self.aP()
            else:
                self.n_II(fK[18], 1)
            if fK[23] == -1 and GameCanvas.popups.kind == 0:
                # the Yes/No popup of Enchant / Combine has just closed
                fK[23] = 0
                if GameCanvas.key == -5 and GameCanvas.popups.button == 0:
                    if fK[21] > GameCanvas.hero.gold:
                        fK[20] = 4
                        Menus.aV()
                        Menus.bb()
                    else:
                        fK[26] = 0          # start the sparkle, the action follows below
                else:
                    Menus.bb()
        if fK[26] == -1:
            return
        if fK[26] < 5:
            self.aR()
            fK[26] += 1
            return
        fK[26] = -1
        GameCanvas.redraw = 1
        if fK[0] == 2:
            self.aQ()
        elif fK[0] == 3:
            cz = GameCanvas.hero
            if fK[22] == 0:
                for b in range(3):
                    Item.a(cz.backpack[GameCanvas.combine_slots[b]])
                dst = cz.backpack[GameCanvas.combine_slots[2]]
                dst.id = GameCanvas.combine_result.id
                dst.attack = GameCanvas.combine_result.attack
                dst.defense = GameCanvas.combine_result.defense
                dst.hp = GameCanvas.combine_result.hp
                dst.mp = GameCanvas.combine_result.mp
                dst.enchant = GameCanvas.combine_result.enchant
            elif fK[31] != -1:
                Item.a(cz.backpack[fK[31]])
                fK[31] = -1
            Menus.bb()
            fK[20] = 9
            cz.gold -= fK[21]
        self.ar()
        Menus.aV()

    def aQ(self):  # e.java:2113-2135  (Enchant: roll success / fail / lost)
        arrayOfByte1 = [100, 90, 80, 70, 60, 45, 30, 10, 1]
        arrayOfByte2 = [0, 10, 20, 40, 50, 60, 70, 80, 90]
        z_ = self.o_I(-1)
        GameCanvas.cursor[20] = 2
        GameCanvas.hero.gold -= GameCanvas.cursor[21]
        if GameCanvas.cursor[22] == -1:
            GameCanvas.cursor[23] = 2
        else:
            i = self.C_I(100) + 1
            if i > arrayOfByte1[z_.enchant]:
                i = self.C_I(100)
                GameCanvas.cursor[23] = 2 if i <= arrayOfByte2[z_.enchant] else 1
            else:
                self.a_LzI(z_, 1)
                GameCanvas.cursor[23] = 0
        if GameCanvas.cursor[23] == 2:
            Item.a(z_)
            GameCanvas.cursor[23] = 1

    def o_II(self, paramInt1, paramInt2):  # e.java:2137-2144  (sparkle frame)
        arrayOfByte1 = [0, 15, 30, 0, 20]
        arrayOfByte2 = [0, 0, 0, 16, 16]
        arrayOfByte3 = [16, 16, 16, 20, 24]
        n = arrayOfByte3[GameCanvas.cursor[26]]
        paramInt1 -= n >> 1
        paramInt2 -= n >> 1
        GameCanvas.a_IIIIMII(paramInt1, paramInt2, n, n, GameCanvas.sparkle, arrayOfByte1[GameCanvas.cursor[26]], arrayOfByte2[GameCanvas.cursor[26]])

    def aR(self):  # e.java:2146-2156
        if GameCanvas.cursor[0] == 2:
            self.o_II(GameCanvas.cursor[24], GameCanvas.cursor[25])
            return
        if GameCanvas.cursor[0] == 3:
            for b in range(3):
                if GameCanvas.combine_pos[b].x > 0 and GameCanvas.combine_pos[b].y > 0:
                    self.o_II(GameCanvas.combine_pos[b].x, GameCanvas.combine_pos[b].y)

    @staticmethod
    def aV():  # e.java:2396-2451  (Blacksmith message popup)
        from pow.game.popups import Popups
        arrayOfString = ["Success", "Fail"]
        str_ = ""
        GameCanvas.popups.a_v()
        GameCanvas.redraw = 1
        fK = GameCanvas.cursor
        v = fK[20]
        if v == 0:
            if fK[19] < 1:
                return
            str_ = Popups.d_v()
        elif v == 11:
            str_ = Popups.e_v()
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
        GameCanvas.popups.a_T(str_)

    def aW(self):  # e.java:2453-2566  (Blacksmith keys)
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
            Menus.bb()
        elif ch in (-5, 53):
            if fK[0] == 0:
                self.bc()
                bool_ = False
                Menus.aV()
            elif fK[0] == 1:
                if fK[19] != 0:
                    self.bd()
                    Menus.aV()
                else:
                    bool_ = False          # falls into `default`
            elif fK[0] == 2:
                self.be()
                Menus.aV()
                bool_ = False              # falls into `default`
            else:
                if fK[0] == 3 and self.o_I(-1).id > 100:
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
                        self.aX()
        else:
            bool_ = False
        if bool_:
            self.ba()
            GameCanvas.menus.c_Z(True)

    def aX(self):  # e.java:2568-2626  (Combine: work out the result of 3 items)
        arrayOfInt = [0, 0, 0]
        i = 0
        for b in range(3):
            z_ = self.o_I(GameCanvas.combine_slots[b])
            b1 = 0
            while b1 < b and arrayOfInt[b1] <= z_.id:
                b1 += 1
            for b2 in range(b, b1, -1):
                arrayOfInt[b2] = arrayOfInt[b2 - 1]
            arrayOfInt[b1] = z_.id
            i += z_.enchant
        Menus.mix_table = ResReader.a("/" + GameCanvas.scr_data.a_I(68))
        if Menus.mix_table is not None:
            arrayOfInt1 = [0, 149, 298]
            j_ = 0
            k = 149
            b = 0
            while b < 3:
                arrayOfInt2 = self.b_IIII(arrayOfInt1[b], arrayOfInt[b], j_, k)
                j_ = arrayOfInt2[0]
                k = arrayOfInt2[1]
                if 0 == arrayOfInt2[2]:
                    break
                b += 1
            if b < 3:
                GameCanvas.cursor[22] = 2
                Menus.bb()
            else:
                j_ += self.C_I(k)
                arrayOfInt[0] = Menus.S_I(447 + j_)
                GameCanvas.combine_result = self.J_I(arrayOfInt[0])
                GameCanvas.cursor[21] = idiv(Menus.b_Lz(GameCanvas.combine_result), 4)
                if arrayOfInt[0] < 500:
                    arrayOfInt[1] = GameCanvas.item_tables[1].a_II(arrayOfInt[0] - 301, 8)
                    arrayOfInt[2] = 15
                else:
                    arrayOfInt[1] = GameCanvas.item_tables[2].a_II(arrayOfInt[0] - 501, 7)
                    arrayOfInt[2] = 12
                arrayOfInt[1] = idiv(200 - arrayOfInt[1], 12)
                if arrayOfInt[1] >= self.C_I(101):
                    GameCanvas.cursor[22] = 0
                    GameCanvas.combine_result = self.a_LzI(GameCanvas.combine_result, idiv(i, 3))
                else:
                    GameCanvas.cursor[22] = 1
                    arrayOfInt[1] = idiv((100 - arrayOfInt[1]) * 10, arrayOfInt[2])
                    GameCanvas.cursor[31] = GameCanvas.combine_slots[self.C_I(3)] if arrayOfInt[1] >= self.C_I(101) else -1
                GameCanvas.cursor[23] = -1
            GameCanvas.cursor[20] = 8
            Menus.aV()
        Menus.mix_table = None

    def a_LzI(self, paramz, paramInt):  # e.java:2628-2668  (enchant paramInt times: raise stats)
        arrayOfByte = [30, 25, 20, 15, 9, 1]
        for b in range(paramInt):
            i = 0
            j_ = self.C_I(101)
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
    def S_I(paramInt):  # e.java:2670-2672
        return Menus.mix_table[paramInt * 2] & 0xFF | (Menus.mix_table[paramInt * 2 + 1] & 0xFF) << 8

    def b_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # e.java:2674-2692  (find run of paramInt2)
        arrayOfInt = [paramInt3, paramInt4, 0]
        b = 0
        while b < arrayOfInt[1]:
            i = Menus.S_I(paramInt1 + arrayOfInt[0])
            if i == paramInt2:
                break
            arrayOfInt[0] = arrayOfInt[0] + 1
            b += 1
        if b < arrayOfInt[1]:
            arrayOfInt[1] = arrayOfInt[1] - b
            b = 0
            i = Menus.S_I(paramInt1 + arrayOfInt[0])
            while b < arrayOfInt[1] and i == paramInt2:
                b += 1
                i = Menus.S_I(paramInt1 + arrayOfInt[0] + b)
            arrayOfInt[1] = b
            arrayOfInt[2] = 1
            return arrayOfInt
        arrayOfInt[2] = 0
        return arrayOfInt

    def aY(self):  # e.java:2694-2707  (enter a Blacksmith screen)
        if GameCanvas.menu[0] == 24:
            Menus.m_v()
            if GameCanvas.cursor[16] < 3:
                GameCanvas.popups.e_I(39)
                GameCanvas.redraw = 1
                GameCanvas.menu[1] = 3
                return True
        GameCanvas.az()
        self.aZ()
        return True

    def aZ(self):  # e.java:2709-2754  (grid layout of the current Blacksmith mode)
        fK = GameCanvas.cursor
        fK[0] = GameCanvas.menu[0] - 21
        if fK[0] == 0 or fK[0] == 1:
            fK[14] = fK[0] + 1
        else:
            fK[14] = 0
        if fK[0] == 3:
            Menus.bb()
            fK[20] = 7
            Menus.aV()
        Menus.m_v()
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
        self.ba()
        fK[26] = -1

    def ba(self):  # e.java:2756-2772  (clamp cursor, scroll, item under cursor -> fK[19])
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
        z_ = self.o_I(-1)
        fK[19] = z_.id if z_ is not None else 0

    @staticmethod
    def c_I(paramInt):  # e.java:2774-2786  (item name)
        if paramInt < 100:
            return consts.aN[paramInt - 1]
        if paramInt < 300:
            return GameCanvas.item_tables[0].b_II(paramInt - 101, 0)
        if paramInt < 500:
            return GameCanvas.item_tables[1].b_II(paramInt - 301, 0)
        return GameCanvas.item_tables[2].b_II(paramInt - 501, 0)

    @staticmethod
    def bb():  # e.java:2788-2801  (clear the Combine selection)
        for b in range(len(GameCanvas.combine_slots)):
            GameCanvas.combine_slots[b] = 0
        for b in range(len(GameCanvas.combine_pos)):
            if GameCanvas.combine_pos[b] is None:
                GameCanvas.combine_pos[b] = Point()
            GameCanvas.combine_pos[b].x = 0
            GameCanvas.combine_pos[b].y = 0
        if GameCanvas.combine_result is None:
            GameCanvas.combine_result = Item()
        Item.a(GameCanvas.combine_result)

    @staticmethod
    def m_v():  # e.java:2803-2815  (count items: fK[16] backpack, fK[17] potions)
        GameCanvas.cursor[16] = 0
        for b in range(25):
            if GameCanvas.hero.backpack[b].id > 0:
                GameCanvas.cursor[16] = GameCanvas.cursor[16] + 1
        GameCanvas.cursor[17] = 0
        for b in range(5):
            if GameCanvas.hero.quick_slots[b].item > 0:
                GameCanvas.cursor[17] = GameCanvas.cursor[17] + 1

    @staticmethod
    def b_Lz(paramz):  # e.java:2817-2830  (price of an item)
        if paramz.id < 100:
            i = consts.y[paramz.id - 1]
        elif paramz.id < 300:
            i = GameCanvas.item_tables[0].a_II(paramz.id - 101, 6)
            i = i + paramz.attack * 100
            i = i + paramz.defense * 100
            i = i + idiv(paramz.hp, 5) * 100
            i = i + idiv(paramz.mp, 3) * 100
        elif paramz.id < 500:
            j_ = 800 if GameCanvas.item_tables[1].a_II(paramz.id - 301, 6) == 0 else 400
            i = paramz.attack * j_
            i = i + paramz.defense * j_
            i = i + idiv(paramz.hp, 5) * j_
            i = i + idiv(paramz.mp, 3) * j_
        else:
            i = GameCanvas.item_tables[2].a_II(paramz.id - 501, 6)
        return i

    def bc(self):  # e.java:2832-2883  (Buy)
        cz = GameCanvas.hero
        fK = GameCanvas.cursor
        z_ = GameCanvas.shop[fK[18]]
        if z_.id == 0:
            fK[20] = -1
            return
        i = Menus.b_Lz(z_)
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
                Item.a(z_)
                fK[16] = fK[16] + 1
                fK[20] = 0
            else:
                fK[20] = 6
        else:
            fK[20] = 4
        if fK[20] == 0:
            cz.gold -= i
            self.ar()

    def bd(self):  # e.java:2885-2905  (Sell, half price)
        cz = GameCanvas.hero
        fK = GameCanvas.cursor
        z_ = self.o_I(-1)
        if z_ is None or z_.id == 0:
            return
        i = Menus.b_Lz(z_)
        if z_.id < 100:
            if cz.quick_slots[fK[18]].count > 1:
                cz.quick_slots[fK[18]].count = i16(cz.quick_slots[fK[18]].count - 1)
            else:
                cz.quick_slots[fK[18]].item = 0
                cz.quick_slots[fK[18]].count = 0
                fK[17] = fK[17] - 1
        else:
            Item.a(z_)
            fK[16] = fK[16] - 1
        fK[20] = 11
        cz.gold += idiv(i, 2)
        self.ar()

    def be(self):  # e.java:2907-2936  (Enchant: price and limit)
        fK = GameCanvas.cursor
        z_ = self.o_I(-1)
        if z_.id == 0:
            fK[20] = -1
            return
        fK[22] = 0
        fK[21] = 0
        if 100 < z_.id < 500:
            if z_.id < 300:
                fK[22] = GameCanvas.item_tables[0].a_II(z_.id - 101, 5)
            else:
                fK[22] = GameCanvas.item_tables[1].a_II(z_.id - 301, 6)
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

    def a_LzIIIIIZ(self, paramz, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramBoolean):  # e.java:3083-3206  (shop description)
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
            paramInt5 = Menus.b_Lz(paramz)
        if paramz.id < 100:
            i = paramz.id - 1
            dF.text = consts.aN[i]
            if GameCanvas.cursor[14] == 2:
                if len(dF.text) > 0:
                    dF.text += " / "
                dF.text += str2
                dF.text += GameCanvas.n_I(paramInt5 >> 1)
            dF.text += " / "
            if i < 9:
                str_ = "Recover " + str(consts.aP[i % 3]) + "% of total " + consts.aO[i // 3]
            else:
                str_ = "Ranged Atk"
            dF.text += str_
            if GameCanvas.cursor[14] == 1:
                dF.text += str1
                dF.text += GameCanvas.n_I(paramInt5)
        else:
            if paramz.id < 300:
                str_ = GameCanvas.item_tables[0].b_II(paramz.id - 101, 0)
                i = consts.w[(paramz.id - 101) % 5]
            elif paramz.id < 500:
                str_ = GameCanvas.item_tables[1].b_II(paramz.id - 301, 0)
                i = GameCanvas.item_tables[1].a_II(paramz.id - 301, 8)
            else:
                str_ = GameCanvas.item_tables[2].b_II(paramz.id - 501, 0)
                i = GameCanvas.item_tables[2].a_II(paramz.id - 501, 7)
            if paramBoolean:
                dF.text += str_
            if GameCanvas.cursor[14] == 2:
                if len(dF.text) > 0:
                    dF.text += " / "
                dF.text += str2
                dF.text += GameCanvas.n_I(paramInt5 >> 1)
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
                dF.text += GameCanvas.n_I(paramInt5)
        dF.rect.x = (GameCanvas.screen_w - 202) // 2 - GameCanvas.view_x
        dF.rect.y = 200
        dF.rect.w = paramInt3 + 2
        dF.rect.h = paramInt4
        GameCanvas.text_width = GameCanvas.c_T(dF.text)
        if GameCanvas.text_width > paramInt3 - 2:
            dF.shown = 1
            if GameCanvas.key != -999:
                dF.text_x = i16(dF.rect.x + dF.rect.w)
                return
        else:
            dF.shown = 0
            dF.text_x = i16(paramInt1 + 1)

    def g_v(self):  # e.java:1241-1244
        self.E_v()
        GameCanvas.images[18] = self.d_T(GameCanvas.scr_ui.a_I(77))

    def aJ(self):  # e.java:1370-1383  (Main Menu: caption strip + blinking arrows)
        i = GameCanvas.menu[1]
        j_ = GameCanvas.view_cx - 52 + GameCanvas.view_x
        if 0 == i and not GameCanvas.aq():
            i = 9
        GameCanvas.a_IIIIMII(j_, GameCanvas.canvas_size.y - 65, 116, 21, GameCanvas.images[18], 0, i * 21)
        GameCanvas.a_IIIIMII(j_ - 24 - GameCanvas.lord_count % 3 * 2, GameCanvas.canvas_size.y - 65 + 2, 10, 16, GameCanvas.images[17], 0, 0)
        GameCanvas.a_IIIIMII(j_ + 116 + 16 + GameCanvas.lord_count % 3 * 2, GameCanvas.canvas_size.y - 65 + 2, 10, 16, GameCanvas.images[17], 10, 0)
        if GameCanvas.lord_count > 100:
            GameCanvas.lord_count = 32
            return
        GameCanvas.lord_count += 1

    def aK(self):  # e.java:1385-1404  (screen 6: choose the hero, 3 heads, the middle one is chosen)
        image = None
        i = GameCanvas.hero.head - 1 & 0x3
        Gfx.a_Lg(GameCanvas.font_white)
        for b in range(3):
            str_ = GameCanvas.M_I(65 + b)
            self.b_TII(str_, GameCanvas.view_cy - 90 - b * 20 + 10, 0)
        for b in range(3):
            image = self.d_T(GameCanvas.scr_char.a_I(38 + i))
            self.b_IIIIIII(GameCanvas.view_cx - 94 + 69 * b + GameCanvas.view_x, GameCanvas.view_cy + 9 + GameCanvas.view_y, 50, 50, 148, 109, 82)
            self.a_IIIIIII(GameCanvas.view_cx - 93 + 69 * b + GameCanvas.view_x, GameCanvas.view_cy + 10 + GameCanvas.view_y, 48, 48, 33, 0, 0)
            self.b_MIIIIII(image, GameCanvas.view_cx - 92 + 69 * b, GameCanvas.view_cy + 11, 46, 46, 0, 0)
            i = i + 1 & 0x3
        self.c_IIIIIII(GameCanvas.view_cx - 27 + GameCanvas.view_x + 1, GameCanvas.view_cy + 8 + GameCanvas.view_y, 52, 52, 255, 182, 82)
        self.f_III(0, GameCanvas.view_cx - 40, GameCanvas.view_cy + 23)
        self.f_III(1, GameCanvas.view_cx + 30, GameCanvas.view_cy + 23)

    def aL(self):  # e.java:1406-1413  (screen 7: the two caption lines)
        Gfx.a_Lg(GameCanvas.font_white)
        GameCanvas.anim_step = 0
        while GameCanvas.anim_step < 2:
            self.b_TII(GameCanvas.M_I(69 + GameCanvas.anim_step), GameCanvas.view_cy - 47 + GameCanvas.anim_step * 20, 0)
            GameCanvas.anim_step += 1

    def aM(self):  # e.java:1415-1427  (screen 7: the name box)
        i = GameCanvas.view_cx - 80 + GameCanvas.view_x
        j_ = GameCanvas.view_cy + 8 + GameCanvas.view_y
        Gfx.b_IIIII(i, j_, 160, 20, 0)
        Gfx.a_IIIII(i, j_, 160, 20, GameCanvas.k_III(173, 170, 173))
        Gfx.a_Lg(GameCanvas.font_white)
        Gfx.a_TIII(GameCanvas.name_buf.a_v(), GameCanvas.screen_cx, j_ + 2, 1)
        if GameCanvas.name_buf.b_v() == 0:
            GameCanvas.h_II(-1, 2)
            return
        GameCanvas.h_II(-1, 10)

    def O_I(self, paramInt):  # e.java:1429-1469  (screen 8/14: stat sheet; 1 = whole, 0 = numbers only)
        cz = GameCanvas.hero
        arrayOfInt1 = [cz.base_hp, cz.base_mp, cz.base_attack, cz.base_defense]
        image = None
        if paramInt != 0:
            arrayOfInt = self.p_v()
            GameCanvas.exp_bars[0] = i16(idiv(cz.exp * 100, arrayOfInt[0]))
            image = self.d_T(GameCanvas.scr_ui.a_I(26))
            i = image.getWidth()
            j_ = image.getHeight()
            GameCanvas.sheet_y = GameCanvas.view_cy - j_ // 2
            GameCanvas.sheet_x = GameCanvas.view_cx - i // 2
            self.b_MIIIIII(image, GameCanvas.sheet_x, GameCanvas.sheet_y, i, j_, 0, 0)
            GameCanvas.c_TII(cz.name, GameCanvas.sheet_x + 110, GameCanvas.sheet_y + 6)
            self.d_IIII(cz.level, GameCanvas.sheet_x + 152, GameCanvas.sheet_y + 34, 0)
            self.d_IIII(cz.fame, GameCanvas.sheet_x + 152, GameCanvas.sheet_y + 61, 0)
        else:
            arrayOfInt = [GameCanvas.sheet_x + 88, GameCanvas.sheet_y + 83, 68, 20]
            Gfx.b_IIIII(arrayOfInt[0], arrayOfInt[1], arrayOfInt[2], arrayOfInt[3], 0)
            arrayOfInt[0] = GameCanvas.sheet_x + 39
            arrayOfInt[1] = GameCanvas.sheet_y + 108
            arrayOfInt[2] = 104
            arrayOfInt[3] = 18
            for b1 in range(4):
                Gfx.b_IIIII(arrayOfInt[0], arrayOfInt[1], arrayOfInt[2], arrayOfInt[3], 0)
                arrayOfInt[1] = arrayOfInt[1] + 20
        arrayOfInt2 = [cz.gear_hp, cz.gear_mp, cz.gear_attack, cz.gear_defense]
        self.d_IIII(cz.stat_points, GameCanvas.sheet_x + 152, GameCanvas.sheet_y + 86, 0)
        for b in range(4):
            i = self.d_IIII(arrayOfInt1[b], GameCanvas.sheet_x + 44, GameCanvas.sheet_y + 110 + b * 20, 1)
            if arrayOfInt2[b] > 0:
                self.b_MIIIIII(GameCanvas.images[19], i + 1, GameCanvas.sheet_y + 110 + b * 20, 10, 14, 105, 0)
                self.d_IIII(arrayOfInt2[b], i + 9, GameCanvas.sheet_y + 110 + b * 20, 1)
        image = self.d_T(GameCanvas.scr_char.a_I(38 + cz.head))
        self.b_MIIIIII(image, GameCanvas.sheet_x + 2, GameCanvas.sheet_y + 3, 46, 46, 0, 0)
        if cz.stat_points > 0:
            self.a_IIIIIII(GameCanvas.sheet_x + 144, GameCanvas.sheet_y + 97 + 20 * GameCanvas.menu[1] + GameCanvas.view_y + 11, 14, 18, 255, 255, 255)
        GameCanvas.menu_part = 0

    def b_I(self, paramInt):  # e.java:2158-2165  (story: speaker portrait top-left, hero bottom-right)
        self.a_IIIIZ(19 + GameCanvas.view_x + 2, GameCanvas.view_cy - 72 + 9 + GameCanvas.view_y, 46, 46, True)
        if paramInt > -1:
            self.a_TIIIIII(GameCanvas.scr_char.a_I(0 + paramInt), 19 + GameCanvas.view_x + 2, GameCanvas.view_cy - 73 + 10 + GameCanvas.view_y, 46, 46, 0, 0)
        self.a_IIIIZ(GameCanvas.canvas_size.x // 2 + 60 - GameCanvas.view_x, GameCanvas.view_cy - 72 + 109 + GameCanvas.view_y, 46, 46, True)
        self.a_TIIIIII(GameCanvas.scr_char.a_I(38 + GameCanvas.hero.head), GameCanvas.canvas_size.x // 2 + 60 - GameCanvas.view_x, GameCanvas.view_cy - 73 + 110 + GameCanvas.view_y, 46, 46, 0, 0)
        self.R_I(3)

    def R_I(self, paramInt):  # e.java:2167-2172  (empty speech boxes: 1 = top, 2 = bottom)
        if (paramInt & 0x1) != 0:
            self.a_IIIIZ(GameCanvas.view_cx - 60 + 15 + GameCanvas.view_x, GameCanvas.view_cy - 73 + 7 + GameCanvas.view_y, 150, 53, False)
        if (paramInt & 0x2) != 0:
            self.a_IIIIZ(GameCanvas.view_cx - 60 + -40 + GameCanvas.view_x, GameCanvas.view_cy - 73 + 107 + GameCanvas.view_y, 150, 53, False)

    @staticmethod
    def a_III(paramInt1, paramInt2, paramInt3):  # e.java:2216-2309  (type speech text fw[p1], max 3 lines)
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
        Gfx.a_Lg(GameCanvas.font_white)
        while n <= i1 and n < len(GameCanvas.speech[paramInt1]):
            fw = GameCanvas.speech[paramInt1]
            i5 = Font.b_v() + Font.c_v()
            p = (1 if n <= 0 else n) - 1
            if i == i3 or (p < len(fw) and fw[p] == ' ') or (n - 1 < len(fw) and fw[n - 1] == ']'):
                b = 0
                i6 = 0
                while n + b + 1 < len(fw) and fw[n + b] != ' ' and fw[n + b] != ']' and fw[n + b] != ',':
                    i6 += Font.b_v() + Font.c_v()
                    b += 1
                    if i6 > 146:
                        i6 -= Font.b_v() + Font.c_v()
                if fw[n + b] == ']':
                    k += Font.b_v()
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
                GameCanvas.menus.R_I(paramInt1 + 1)
            if i == i3 and fw[n] == ' ':
                n += 1
            if len(fw) >= n + 1:
                Gfx.a_TIII(fw[n:n + 1], i, j_, 0)
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

    def aU(self):  # e.java:2374-2394  (screen 29: difficulty Hard / Normal)
        arrayOfInt = [GameCanvas.view_cx - 80 + GameCanvas.view_x, GameCanvas.view_cy - 60 + GameCanvas.view_y]
        GameCanvas.difficulty = i16(GameCanvas.menu[1])
        for b in range(2):
            if GameCanvas.menu[1] == b:
                Gfx.a_Lg(GameCanvas.font_orange)
                bool_ = True
            else:
                Gfx.a_Lg(GameCanvas.font_white)
                bool_ = False
            self.a_IIIIZ(arrayOfInt[0], arrayOfInt[1] + b * 25, 160, 20, bool_)
            self.b_TII(consts.aX[b], arrayOfInt[1] + 1 + b * 25 - 1, 15)
        Gfx.a_Lg(GameCanvas.font_white)
        self.a_IIIIZ(arrayOfInt[0], GameCanvas.view_cy + GameCanvas.view_y, 160, 80, False)
        for b in range(3):
            self.b_TII(consts.aY[GameCanvas.menu[1]][b], GameCanvas.view_cy + 10 + b * 20, 17)

    def e_I(self, paramInt):  # e.java:3465-3531  (item record -> cX / cY / cZ)
        arrayOfByte = bytearray(16)
        if paramInt < 100:
            return
        if paramInt < 300:
            if GameCanvas.gear_data is None:
                GameCanvas.gear_data = GameCanvas.v_I(47)
            cU = GameCanvas.gear_data
            i = 9 + (paramInt - 101) * 23
            b = 0
            while b < 15:
                arrayOfByte[b] = cU[i + b] & 0xFF
                if arrayOfByte[b] == 0:
                    break
                b += 1
            GameCanvas.gear_def.name = GameCanvas.a_ABII(arrayOfByte, 0, b)
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
                GameCanvas.treasure_data = GameCanvas.v_I(51)
            cV = GameCanvas.treasure_data
            i = 10 + (paramInt - 301) * 24
            b = 0
            while b < 15:
                arrayOfByte[b] = cV[i + b] & 0xFF
                if arrayOfByte[b] == 0:
                    break
                b += 1
            GameCanvas.treasure_def.name = GameCanvas.a_ABII(arrayOfByte, 0, b)
            GameCanvas.treasure_def.slot = i8(cV[i + 15])
            GameCanvas.treasure_def.attack = GameCanvas.a_BB(cV[i + 16], cV[i + 17])
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
                GameCanvas.rare_data = GameCanvas.v_I(49)
            cW = GameCanvas.rare_data
            i = 9 + (paramInt - 501) * 27
            b = 0
            while b < 15:
                arrayOfByte[b] = cW[i + b] & 0xFF
                if arrayOfByte[b] == 0:
                    break
                b += 1
            GameCanvas.rare_def.name = GameCanvas.a_ABII(arrayOfByte, 0, b)
            GameCanvas.rare_def.slot = i8(cW[i + 15])
            GameCanvas.rare_def.attack = GameCanvas.a_BB(cW[i + 16], cW[i + 17])
            GameCanvas.rare_def.defense = i8(cW[i + 18])
            GameCanvas.rare_def.hp = GameCanvas.a_BB(cW[i + 19], cW[i + 20])
            GameCanvas.rare_def.mp = i8(cW[i + 21])
            GameCanvas.rare_def.level = cW[i + 26] & 0xFF
            if GameCanvas.state != 2:
                GameCanvas.rare_data = None

    def T_I(self, paramInt):  # e.java:3533-3545  (stat cursor: 0 = erase, 1 = draw)
        if GameCanvas.hero.stat_points > 0:
            if paramInt != 0:
                c = 255 if F11 else 1   # DECOMP-FIX F11: decompiled `true` (= 1) as a colour
            else:
                c = 0
            self.a_IIIIIII(GameCanvas.sheet_x + 144, GameCanvas.sheet_y + 97 + 20 * GameCanvas.menu[1] + 11, 14, 18, c, c, c)

    def p_v(self):  # e.java:3547-3560  (exp table of the hero level from edat 45)
        arrayOfByte = GameCanvas.v_I(45)
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

    def bf_v(self):  # e.java:3283-3364  (Game Menu carousel, 4 animation frames per step)
        cM = GameCanvas.menu
        s = GameCanvas.menu_anim
        if GameCanvas.images[27] is None:
            self.F_v()
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
                    GameCanvas.I_v()
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
                    GameCanvas.I_v()
                elif GameCanvas.menu_anim > 3:
                    GameCanvas.redraw = 0
                    GameCanvas.menu_scroll = 0
                    GameCanvas.menu_anim = 0
        self.a_MIIIIII(GameCanvas.images[7], 0, 0, GameCanvas.canvas_size.x, GameCanvas.canvas_size.y, 0, 0)
        self.b_TII(GameCanvas.menu_titles[cM[0]], 2 - GameCanvas.view_y, 0)
        if GameCanvas.carousel_image is None or GameCanvas.carousel_row != cM[1]:
            GameCanvas.carousel_image = self.d_T(GameCanvas.scr_ui.a_I(66 + cM[1]))
            GameCanvas.carousel_row = cM[1]
        if GameCanvas.carousel_image is not None:
            GameCanvas.a_IIIIMII(i, 60, 117, 90, GameCanvas.carousel_image, 0, 0)
        GameCanvas.a_IIIIMII(arrayOfInt1[s], arrayOfInt2[s], 89, 20, GameCanvas.images[27], 0, 0)
        GameCanvas.a_IIIIMII(arrayOfInt1[s] + 22, arrayOfInt2[s] + 5, 62, 11, GameCanvas.images[29], 0,
                     11 * (4 if cM[1] == 0 else (cM[1] - 1)))
        GameCanvas.a_IIIIMII(arrayOfInt3[s], arrayOfInt4[s], 89, 20, GameCanvas.images[27], 0, 0)
        GameCanvas.a_IIIIMII(arrayOfInt3[s] + 22, arrayOfInt4[s] + 5, 62, 11, GameCanvas.images[29], 0,
                     11 * (0 if cM[1] == 4 else (cM[1] + 1)))
        GameCanvas.a_IIIIMII(arrayOfInt5[s], arrayOfInt6[s], 127, 29, GameCanvas.images[26], 0, 0)
        GameCanvas.a_IIIIMII(arrayOfInt5[s] + 22 + 2, arrayOfInt6[s] + 5 + 1, 94, 18, GameCanvas.images[28], 0, 18 * cM[1])
        if GameCanvas.redraw != 2 and GameCanvas.menu_anim == 0:
            GameCanvas.a_IIIIMII(dd - 5 + GameCanvas.view_x, arrayOfInt6[s] - 6 - 5 - GameCanvas.lord_count % 3 * 2, 16, 10, GameCanvas.images[17], 20, 0)
            GameCanvas.a_IIIIMII(dd - 5 + GameCanvas.view_x, arrayOfInt6[s] + 29 + GameCanvas.lord_count % 3 * 2, 16, 10, GameCanvas.images[17], 20, 10)
        if GameCanvas.lord_count > 100:
            GameCanvas.lord_count = 32
        else:
            GameCanvas.lord_count += 1
        GameCanvas.h_II(-1, 2)

    # ---- Missions: lords (1), missions (2), description (3), briefing (4) ------------------

    def aH(self):  # e.java:1229-1238  (mission description, 6 lines per page)
        self.a_IIIIZ(GameCanvas.view_cx - 100 + GameCanvas.view_x, GameCanvas.view_cy - 80, 200, 40, False)
        self.b_TII(GameCanvas.lord_name, GameCanvas.view_cy - 80, 30)
        self.b_TII(GameCanvas.mission_name, GameCanvas.view_cy - 60, 30)
        self.a_IIIIZ(GameCanvas.view_cx - 110, GameCanvas.view_cy - 30, 220, 119, False)
        for b in range(6):
            if GameCanvas.text_line_count[0] >= GameCanvas.menu[2] * 6 + b:
                GameCanvas.a_IIT(GameCanvas.view_cx - 100 + GameCanvas.view_x, GameCanvas.view_cy - 28 + b * 20 + GameCanvas.view_y, GameCanvas.text_lines[0][GameCanvas.menu[2] * 6 + b])
        self.a_IIIZ(GameCanvas.menu[2] + 1, idiv(GameCanvas.text_line_count[0], 6) + 1, GameCanvas.view_cy + 110, True)

    def aI(self):  # e.java:1246-1250  (briefing: portraits + empty speech boxes)
        self.b_I(GameCanvas.mission_portraits[GameCanvas.mission])
        self.q_I(1)
        self.R_I(3)

    def h_v(self):  # e.java:1252-1264  (talk in the map: portrait bottom-left)
        if (GameCanvas.talk_box & 0x1) != 0:
            i = 0 + GameCanvas.general.portrait
        else:
            i = 38 + GameCanvas.hero.head
        j_ = GameCanvas.view_size.y - 46 - 4
        self.a_IIIIZ(2 + GameCanvas.view_x, j_ + GameCanvas.view_y, 48, 48, True)
        j_ += 1
        self.a_TIIIIII(GameCanvas.scr_char.a_I(i), 3 + GameCanvas.view_x, j_ + GameCanvas.view_y, 46, 46, 0, 0)
        self.aT()
        self.q_I(1)

    def i_v(self):  # e.java:1266-1361  (dialogue typewriter: dG 0 briefing, 1 map talk, 2 general)
        arrayOfByte1 = [2, 3, 5]
        arrayOfByte2 = [2, 1, 1]
        if GameCanvas.state == 5 and GameCanvas.key != -6:
            GameCanvas.key = -999
        Gfx.a_Lg(GameCanvas.font_white)
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
                                self.w_I(2)
                                self.F_v()
                                GameCanvas.menu[0] = 0
                                GameCanvas.menu_count = consts.v[GameCanvas.menu[0]]
                                GameCanvas.menu_items = GameCanvas.game_menu_items
                                GameCanvas.state = 2
                                GameCanvas.menu_scroll = 0
                                GameCanvas.menu_anim = 0
                                GameCanvas.redraw = 1
                                self.L_v()
                                return
                            GameCanvas.room_phase = 1
                            GameCanvas.room_phase_timer = 5
                            GameCanvas.state = 3
                            return
                        self.y_v()
                        return
                    GameCanvas.talk_row = 0
                    GameCanvas.talk_rows = 0
                    if 0 == GameCanvas.talk_kind:
                        GameCanvas.talk_side = i16(GameCanvas.talk_side + 1 & 0x1)
                    GameCanvas.ao()
                    self.z_I(GameCanvas.talk_line + GameCanvas.talk_box - 1)
                    if GameCanvas.talk_kind != 0:
                        self.h_v()
                        return
                    self.aS()
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
                        self.aT()
                        return
                    self.aS()
                    return
        else:
            if GameCanvas.key == -5:
                GameCanvas.talk_rows = i16(GameCanvas.talk_rows + arrayOfByte2[GameCanvas.talk_kind] - GameCanvas.talk_row)
                GameCanvas.talk_row = i16(arrayOfByte2[GameCanvas.talk_kind])
                GameCanvas.talk_chars = 29
                if GameCanvas.talk_kind != 0:
                    self.aT()
                else:
                    self.aS()
                GameCanvas.wait_ticks = 3
                return
            line = GameCanvas.text_lines[GameCanvas.talk_side][GameCanvas.talk_row]
            str_ = line[GameCanvas.talk_chars:]
            if len(str_) != 0 and ord(str_[0]) > 0:
                GameCanvas.talk_chars = i16(GameCanvas.talk_chars + 1)
                Gfx.a_TIII(str_[0:1], GameCanvas.talk_cursor_x + GameCanvas.view_x, GameCanvas.talk_y[GameCanvas.talk_side] + 16 * GameCanvas.talk_row + GameCanvas.view_y, 0)
                GameCanvas.talk_cursor_x = i16(GameCanvas.talk_cursor_x + 9)
                return
            if GameCanvas.talk_rows >= GameCanvas.text_line_count[GameCanvas.talk_side]:
                GameCanvas.wait_ticks = 15
                return
            GameCanvas.wait_ticks = 1

    def aS(self):  # e.java:2174-2205  (briefing: both speech boxes)
        Gfx.a_Lg(GameCanvas.font_white)
        self.R_I(2 if GameCanvas.talk_side != 0 else 1)
        dp, dL, dM = GameCanvas.text_lines, GameCanvas.talk_x, GameCanvas.talk_y
        if GameCanvas.talk_side != 0:
            for b in range(3):
                GameCanvas.c_IIT(dL[0] + GameCanvas.view_x, dM[0] + 16 * b + GameCanvas.view_y, dp[0][b])
        else:
            for b in range(GameCanvas.talk_row):
                if dp[0][b] is not None:
                    GameCanvas.c_IIT(dL[0] + GameCanvas.view_x, dM[0] + 16 * b + GameCanvas.view_y, dp[0][b])
            if dp[0][GameCanvas.talk_row] is not None:
                str_ = dp[0][GameCanvas.talk_row][0:min(GameCanvas.talk_chars, len(dp[0][GameCanvas.talk_row]))]
                GameCanvas.c_IIT(dL[0] + GameCanvas.view_x, dM[0] + 16 * GameCanvas.talk_row + GameCanvas.view_y, str_)
        if GameCanvas.talk_box > 1:
            if GameCanvas.talk_side != 0:
                for b in range(GameCanvas.talk_row):
                    if dp[1][b] is not None:
                        GameCanvas.c_IIT(dL[1] + GameCanvas.view_x, dM[1] + 16 * b + GameCanvas.view_y, dp[1][b])
                if dp[1][GameCanvas.talk_row] is not None:
                    str_ = dp[1][GameCanvas.talk_row][0:min(GameCanvas.talk_chars, len(dp[1][GameCanvas.talk_row]))]
                    GameCanvas.c_IIT(dL[1] + GameCanvas.view_x, dM[1] + 16 * GameCanvas.talk_row + GameCanvas.view_y, str_)
                    return
            else:
                for b in range(3):
                    GameCanvas.c_IIT(dL[1] + GameCanvas.view_x, dM[1] + 16 * b + GameCanvas.view_y, dp[1][b])

    def aT(self):  # e.java:2207-2214  (map talk: one speech box at the bottom)
        self.a_IIIIZ(54 + GameCanvas.view_x, GameCanvas.view_size.y - 40 + GameCanvas.view_y, GameCanvas.view_size.x - 56, 38, True)
        Gfx.a_Lg(GameCanvas.font_white)
        for b in range(GameCanvas.talk_row):
            GameCanvas.c_IIT(GameCanvas.talk_x[0] + GameCanvas.view_x, GameCanvas.talk_y[0] + 16 * b + GameCanvas.view_y, GameCanvas.text_lines[0][b])
        str_ = GameCanvas.text_lines[0][GameCanvas.talk_row][0:GameCanvas.talk_chars]
        GameCanvas.c_IIT(GameCanvas.talk_x[0] + GameCanvas.view_x, GameCanvas.talk_y[0] + 16 * GameCanvas.talk_row + GameCanvas.view_y, str_)

    def bi_v(self):  # e.java:3569-3603  (missions of lord dk -> dz / dA / dB, list dE = dA)
        i = 0
        GameCanvas.map_id = GameCanvas.lord_ids[GameCanvas.lord]
        GameCanvas.lord_name = GameCanvas.lord_names[GameCanvas.lord]
        arrayOfByte1 = GameCanvas.v_I(50)
        GameCanvas.menu_count = GameCanvas.lord_mission_counts[GameCanvas.lord]
        i = 11 * GameCanvas.lord_missions[GameCanvas.lord] + 11
        arrayOfByte2 = GameCanvas.v_I(55)
        for b in range(GameCanvas.menu_count):
            if GameCanvas.lords[b] is None:
                GameCanvas.lords[b] = MissionDef()
            dz = GameCanvas.lords[b]
            dz.id = GameCanvas.b_B(arrayOfByte1[i])
            dz.start_x = GameCanvas.b_B(arrayOfByte1[i + 1])
            dz.start_y = GameCanvas.b_B(arrayOfByte1[i + 2])
            dz.tint = GameCanvas.b_B(arrayOfByte1[i + 3])
            dz.boss_type = GameCanvas.b_B(arrayOfByte1[i + 4])
            dz.general = GameCanvas.b_B(arrayOfByte1[i + 5])
            dz.reward = GameCanvas.b_B(arrayOfByte1[i + 6])
            dz.gold = GameCanvas.b_B(arrayOfByte1[i + 7])
            dz.time_limit = i16(arrayOfByte1[i + 8] & 0xFF | i8(arrayOfByte1[i + 9]) & 0xFF00)
            dz.level_bonus = GameCanvas.b_B(arrayOfByte1[i + 10])
            i += 11
            j_ = 3 + (dz.id - 1) * 15
            b1 = 14
            for b2 in range(14):
                if arrayOfByte2[j_ + b2] == 0:
                    b1 = b2
                    break
            GameCanvas.mission_names[b] = GameCanvas.a_ABII(arrayOfByte2, j_, j_ + b1)
            GameCanvas.mission_portraits[b] = i8(arrayOfByte2[17 + (dz.id - 1) * 15])
        GameCanvas.menu_items = GameCanvas.mission_names

    # ---- Visiting: generals (19 list, 20 talk) ---------------------------------------------

    def aN(self):  # e.java:1694-1748  (generals: Name / Points, 4 per page)
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
        self.a_IIIIZ(i, n, 130, 22, False)
        self.a_IIIIZ(j_, n, 60, 22, False)
        Gfx.a_Lg(GameCanvas.font_white)
        GameCanvas.b_IIT(i + 65, n + 1, arrayOfString[0])
        GameCanvas.b_IIT(j_ + 30, n + 1, arrayOfString[1])
        n += 31
        for b in range(4):
            if b == i1:
                bool_ = True
                Gfx.a_Lg(GameCanvas.font_orange)
            else:
                bool_ = False
                Gfx.a_Lg(GameCanvas.font_white)
            self.a_IIIIZ(i, n, 130, 22, bool_)
            self.a_IIIIZ(j_, n, 60, 22, bool_)
            if i2 < GameCanvas.menu_count:
                if GameCanvas.seal != 0:
                    str_ = GameCanvas.general_table.b_II(GameCanvas.generals[2][i2] - 1, 0)
                else:
                    str_ = GameCanvas.general_table.b_II(GameCanvas.generals[0][i2] - 1, 0)
                GameCanvas.b_IIT(i + 65, n + 1, str_)
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
                GameCanvas.b_IIT(j_ + 30, n + 1, str_)
            i2 += 1
            n += 31
        n += 6
        self.a_IIIZ(GameCanvas.general_pages[1], GameCanvas.general_pages[0], n, True)

    def aO(self):  # e.java:1750-1802  (general talk: type the lines gf[], then popups 14 / 16)
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
                    GameCanvas.popups.e_I(14)
                    GameCanvas.speech_pos[1] = 0
                    return
                if GameCanvas.story_page < 7:
                    GameCanvas.speech[GameCanvas.story_page & 0x1] = GameCanvas.talk_lines[GameCanvas.story_page - 2]
                    GameCanvas.speech_pos[GameCanvas.story_page & 0x1] = 0
                    return
                GameCanvas.visit_text.a_v()
                GameCanvas.visit_text = None
                GameCanvas.general_table.a_v()
                GameCanvas.general_table = None
                GameCanvas.popups.e_I(16)
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
                Menus.a_III(i, j_, 0)
                if len(GameCanvas.speech[i]) <= GameCanvas.speech_pos[i] + 1:
                    if GameCanvas.key != 0:
                        GameCanvas.wait_ticks = 5
                        return
                    GameCanvas.wait_ticks = 15

    def bg_v(self):  # e.java:3366-3393  (open the talk with general cM[1])
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
        self.B_I(GameCanvas.generals[j_][GameCanvas.menu[1]])
        GameCanvas.general_name = GameCanvas.general_table.b_II(i, 0)
        j_ = GameCanvas.general_table.a_II(i, 9)
        k = GameCanvas.general_table.a_II(i, 8)
        i = GameCanvas.generals[1][GameCanvas.visit_general]
        GameCanvas.story_picture = k
        GameCanvas.visit_topic = j_
        if Menus.a_II(i, j_):
            GameCanvas.speech[0] = ""
            GameCanvas.speech[1] = GameCanvas.talk_lines[0]
            GameCanvas.speech_pos[1] = 0
            GameCanvas.speech_pos[0] = 0
            GameCanvas.story_page = 1
            return True
        return False

    @staticmethod
    def a_II(paramInt1, paramInt2):  # e.java:3395-3430  (greeting lines of the general -> gf[])
        if GameCanvas.visit_text is not None:
            GameCanvas.visit_text.a_v()
            GameCanvas.visit_text = None
        GameCanvas.visit_text = ScrTable("/" + GameCanvas.scr_data.a_I(62))
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
                if len(GameCanvas.visit_text.a_I(paramInt1)) > 0:
                    str_ = GameCanvas.general_name if (b3 & 0x1) != 0 else GameCanvas.hero.name
                    GameCanvas.talk_lines[b3 + b2] = "[" + str_ + "] " + GameCanvas.visit_text.a_I(paramInt1) + " "
                    paramInt1 += 1
                else:
                    return False
            return True
        return False

    @staticmethod
    def b_II(paramInt1, paramInt2):  # e.java:3432-3463  (add paramInt2 friendship to general paramInt1)
        b = 0
        while b < GameCanvas.general_count and GameCanvas.generals[0][b] != paramInt1:
            b += 1
        if b == GameCanvas.general_count:
            if paramInt2 > 0:
                d_ = ArrTable("/" + GameCanvas.scr_data.a_I(52))
                for b1 in range(44):
                    i = d_.a_II(b1, 0)
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

    def o_v(self):  # e.java:3208-3281  (gift of the general after the talk -> fJ, cT[0])
        arrayOfShort = [[[500, 800, 900, 960, 990, 995, 998], [60, 61, 91, 92, 392, 892, 992],
                         [100, 600, 900, 930, 990, 995, 996], [1, 2, 5, 305, 310, 410, 910]],
                        [[1, 101, 106, 606, 609, 610, 910], [30, 31, 91, 92, 592, 892, 992],
                         [300, 360, 860, 960, 961, 991, 996], [1, 2, 5, 10, 40, 100, 200]]]
        cz = GameCanvas.hero
        if self.C_I(100) < GameCanvas.generals[1][GameCanvas.visit_general]:
            i = self.C_I(1000)
            GameCanvas.gift_level = 0
            while GameCanvas.gift_level < 7 and i >= arrayOfShort[GameCanvas.general.gift_table][GameCanvas.gift_kind][GameCanvas.gift_level]:
                GameCanvas.gift_level = i16(GameCanvas.gift_level + 1)
            GameCanvas.popups.lines[4] = ""
            v = GameCanvas.gift_level
            if v == 0:
                i = self.p_I(0)
                if cz.skill_levels[i - 1] < 10:
                    str_ = GameCanvas.e_II(54, i - 1)
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
                if self.k_II(GameCanvas.engine.P_I(4), 1) != 0:
                    GameCanvas.popup_lines[0] = GameCanvas.gear_def.name
                    GameCanvas.popups.lines[4] = "Item Acquired!"
                    return
            else:
                i = self.C_I(11)
                if self.k_II(i + 1, 1) != 0:
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
            GameCanvas.generals[2][b] = i16(vg.a_II(b, 0))

    @staticmethod
    def bh_v():  # e.java:3562-3567
        GameCanvas.general_pages[0] = i16(idiv(GameCanvas.menu_count - 1, 4) + 1)
        if GameCanvas.general_table is None:
            GameCanvas.general_table = ArrTable("/" + GameCanvas.scr_data.a_I(46))
        return False

    def n_v(self):  # e.java:2938-2972  (popup extras on the map: experience bars of popups 11 / 12)
        i = 0
        if GameCanvas.popups.popup_id == 11:
            i = self.p_II(GameCanvas.exp_bar_step, 0)
            if 0 == i and 0 == GameCanvas.popups.extra:
                GameCanvas.exp_bar_step = i16(GameCanvas.exp_bar_step + 1)
        elif GameCanvas.popups.popup_id == 12:
            i = self.p_II(GameCanvas.exp_bar_step, 1)
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

    def p_II(self, paramInt1, paramInt2):  # e.java:2974-3017  (experience bar; 1 = full, 2 = done)
        arrayOfInt = [[GameCanvas.k_III(115, 142, 140), GameCanvas.k_III(181, 178, 181), 16777215],
                      [GameCanvas.k_III(99, 0, 0), GameCanvas.k_III(181, 0, 0), GameCanvas.k_III(247, 73, 0)],
                      [GameCanvas.k_III(0, 65, 255), GameCanvas.k_III(0, 146, 255), GameCanvas.k_III(0, 255, 173)],
                      [GameCanvas.k_III(247, 73, 0), GameCanvas.k_III(255, 162, 0), GameCanvas.k_III(255, 223, 0)]]
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
        GameCanvas.a_LacI(arrayOfAc[0], 0)
        arrayOfAc[0].x += 1
        arrayOfAc[0].w = 100
        for b1 in range(b2):
            if arrayOfAc[b1].w > 0:
                for b in range(3):
                    arrayOfAc[b1].y += 1
                    arrayOfAc[b1].h -= 2
                    GameCanvas.a_LacI(arrayOfAc[b1], arrayOfInt[b1][b])
        return b3
