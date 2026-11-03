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
from pow.game.structs import Item, Lord, Point, Rect
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
    cz = GameCanvas.cz
    if cz.Z[GameCanvas.cM[1]].a != 0 and cz.aa[paramInt] != GameCanvas.cM[1]:
        if GameCanvas.cM[1] == cz.aa[paramInt + 1 & 0x1]:
            i = cz.aa[paramInt]
            cz.aa[paramInt] = cz.aa[paramInt + 1 & 0x1]
            cz.aa[paramInt + 1 & 0x1] = i
        else:
            cz.aa[paramInt] = i8(GameCanvas.cM[1])
        return 1
    return 0


class Menus(GameCanvas):
    a = None  # public static byte[] a;   e.java:4

    def __init__(self):  # e.java:6-8
        super().__init__(GameCanvas.bs)

    def a_I(self, paramInt):  # e.java:10-205  (draw the current menu; 1 = first frame, 2 = animation)
        cM = GameCanvas.cM
        if paramInt == 1:
            if cM[0] != 5:
                Gfx.a_Lg(GameCanvas.bu)
                if GameCanvas.bW == 3:
                    Gfx.b_IIIII(7, 19, 225, 242, 0)
                else:
                    self.e_v()
                if cM[0] != 28:
                    if GameCanvas.bW == 3:
                        Gfx.a_Lg(GameCanvas.bu)
                        self.b_TII(GameCanvas.fT[cM[0]], 15, 0)
                    else:
                        self.b_TII(GameCanvas.fT[cM[0]], 2 - GameCanvas.dc, 0)
                else:
                    str_ = GameCanvas.b_TI(GameCanvas.ga[0], GameCanvas.ej)
                    if GameCanvas.bW == 3:
                        Gfx.a_Lg(GameCanvas.bu)
                        self.b_TII(str_, 15, 0)
                    else:
                        self.b_TII(str_, 2 - GameCanvas.dc, 0)
                if consts.u[cM[0]] != -1 or (consts.u[cM[0]] == -1 and cM[0] == 15):
                    if cM[0] == 3:
                        GameCanvas.h_II(11, 2)
                    else:
                        GameCanvas.h_II(-1, 2)
            v = cM[0]
            if v == 0:
                GameCanvas.cL = 0
                GameCanvas.cK = 0
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
                self.b_I(GameCanvas.fE)
                if GameCanvas.fA[0] > 0:
                    Menus.a_III(GameCanvas.fD + 1 & 0x1, 0, 1)
                if GameCanvas.fA[1] > 0:
                    Menus.a_III(GameCanvas.fD & 0x1, 0, 1)
            if GameCanvas.cS.b != 0:
                GameCanvas.cS.c_v()
                return
        else:
            if paramInt == 2:
                v = cM[0]
                if v == 0:
                    self.bf_v()
                    return
                if v == 4:
                    Gfx.a_Lg(GameCanvas.bu)
                    self.e_v()
                    self.aI()
                    GameCanvas.ch = -5
                    GameCanvas.dS = 0
                    self.i_v()
                    GameCanvas.ck -= 1
                return
            if GameCanvas.cS.b != 0:
                if GameCanvas.cS.j != 0:
                    GameCanvas.cS.c_v()
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
                    GameCanvas.f_II(GameCanvas.bP, GameCanvas.de + 32 + GameCanvas.dc)
                    return
                if v in (8, 14):
                    if GameCanvas.da != 0:
                        self.O_I(0)
                        return
                    return
                if v == 15:
                    if GameCanvas.da != 0:
                        self.P_I(GameCanvas.da)
                    self.k_v()
                    return
                if v == 16:
                    self.k_v()
                    return
                if v == 17:
                    if GameCanvas.da != 0:
                        self.Q_I(1)
                    self.k_v()
                    return
                if v == 18:
                    if GameCanvas.da != 0:
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
        if GameCanvas.bj:
            GameCanvas.ed = -1
        v = GameCanvas.cM[0]
        if v == 4:
            return
        if v == 7:
            i = GameCanvas.r_I(GameCanvas.ch)
            if i == -7:
                if len(GameCanvas.bz.a_v()) == 0:
                    GameCanvas.cM[0] = 6
                    GameCanvas.ck = 1
                    return
                GameCanvas.bz.a_I(-8)
                return
            if i == -5 or i == 53:
                if GameCanvas.bP == 26:
                    if len(GameCanvas.bz.a_v()) != 0:
                        GameCanvas.cz.k = GameCanvas.bz.a_v()
                        GameCanvas.bz.a_T(GameCanvas.cz.k)
                        GameCanvas.cM[0] = 8
                        GameCanvas.O_v()
                        GameCanvas.cN = 4
                        GameCanvas.aw()
                        return
                else:
                    if len(GameCanvas.bz.a_v()) == 0:
                        b = 65
                    else:
                        b = 97
                    GameCanvas.bz.a_I(b + GameCanvas.bP)
                    return
            return
        if v == 20:
            if GameCanvas.ch != -5:
                GameCanvas.ch = -999
                return
            return
        if v in (21, 22, 23, 24):
            self.aW()
            return
        ch = GameCanvas.ch
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
            if GameCanvas.cM[0] == 18:
                GameCanvas.ck = ar_c(0)
                return
        elif ch == 35:
            if GameCanvas.cM[0] == 18:
                GameCanvas.ck = ar_c(1)
                return
        elif ch in (-5, 53):
            self.b_v()
            return
        elif ch == -6:
            if GameCanvas.cM[0] == 16 or GameCanvas.cM[0] == 17 or GameCanvas.cM[0] == 3:
                self.b_v()
                return
        elif ch == -7:
            self.aF()

    @staticmethod
    def m_II(paramInt1, paramInt2):  # e.java:304-307
        return consts.aW[paramInt1][paramInt2]

    def aB(self):  # e.java:309-392  (UP)
        cM = GameCanvas.cM
        v = cM[0]
        if v == 0:
            if GameCanvas.cL == 0:
                GameCanvas.ck = 2
                GameCanvas.cL = -1
            return
        if v in (3, 5, 6, 18, 20, 28):
            return
        if v in (8, 14):
            self.T_I(0)
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 0:
                cM[1] = GameCanvas.cN - 1
            self.T_I(1)
            return
        if v == 9:
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 1:
                cM[1] = GameCanvas.cN - 1
            if not GameCanvas.df and cM[1] == 1:
                cM[1] = 0
            GameCanvas.I_v()
            GameCanvas.ck = 1
            return
        if v == 15:
            if cM[3] == 2:
                if cM[1] < 4:
                    cM[2] = cM[2] - 3
                    if cM[2] < 0:
                        cM[2] = cM[2] + 18
                    GameCanvas.da = 3
                GameCanvas.da = 3
                return
            return
        if v == 16:
            cM[2] = cM[2] + 1
            if _inc_cmp(cM[2]) >= GameCanvas.cN:
                cM[2] = 0
            GameCanvas.ck = 1
            return
        if v == 17:
            cM[2] = cM[2] - 5
            if cM[2] < 0:
                cM[2] = cM[2] + 25
            GameCanvas.da = 1
            return
        if v == 19:
            if cM[1] > 0:
                cM[1] = cM[1] - 1
                GameCanvas.ck = 1
                return
            return
        if v == 29:
            cM[1] = 1 - cM[1]
            GameCanvas.ck = 1
            return
        if v == 25:
            if cM[1] == 20:
                cM[1] = 23
            else:
                cM[1] = cM[1] - 1
            if cM[1] < cM[2]:
                cM[1] = cM[2] + 4
            GameCanvas.ck = 1
            return
        cM[1] = cM[1] - 1
        if _dec_cmp(cM[1]) < 0:
            cM[1] = GameCanvas.cN - 1
        GameCanvas.I_v()
        GameCanvas.ck = 1

    def aC(self):  # e.java:394-480  (DOWN)
        cM = GameCanvas.cM
        v = cM[0]
        if v == 0:
            if GameCanvas.cL == 0:
                GameCanvas.cL = 1
                GameCanvas.ck = 2
            return
        if v in (3, 5, 6, 18, 20, 28):
            return
        if v in (8, 14):
            self.T_I(0)
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= GameCanvas.cN:
                cM[1] = 0
            self.T_I(1)
            return
        if v == 9:
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= GameCanvas.cN:
                cM[2] = 0
                cM[1] = 0
            if not GameCanvas.df and cM[1] == 1:
                cM[1] = 2
            GameCanvas.I_v()
            GameCanvas.ck = 1
            return
        if v == 15:
            if cM[3] == 2:
                if cM[1] < 4:
                    cM[2] = cM[2] + 3
                    if cM[2] > 17:
                        cM[2] = cM[2] - 18
                GameCanvas.da = 3
                return
            return
        if v == 16:
            cM[2] = cM[2] - 1
            if _dec_cmp(cM[2]) < 0:
                cM[2] = GameCanvas.cN - 1
            GameCanvas.ck = 1
            return
        if v == 17:
            cM[2] = cM[2] + 5
            if cM[2] > 24:
                cM[2] = cM[2] - 25
            GameCanvas.da = 1
            return
        if v == 19:
            if cM[1] < GameCanvas.cN - 1:
                cM[1] = cM[1] + 1
                GameCanvas.ck = 1
                return
            return
        if v == 29:
            cM[1] = 1 - cM[1]
            GameCanvas.ck = 1
            return
        if v == 25:
            if cM[1] == 23:
                cM[1] = 20
            else:
                cM[1] = cM[1] + 1
            if cM[1] > cM[2] + 4:
                cM[1] = cM[2]
            GameCanvas.ck = 1
            return
        cM[1] = cM[1] + 1
        if _inc_cmp(cM[1]) >= GameCanvas.cN:
            cM[2] = 0
            cM[1] = 0
        GameCanvas.I_v()
        GameCanvas.ck = 1

    def aD(self):  # e.java:482-584  (LEFT)
        cM = GameCanvas.cM
        v = cM[0]
        if v == 1:
            if GameCanvas.bj and GameCanvas.cq > 0:
                GameCanvas.cq = i8(GameCanvas.cq - 1)
                self.C_v()
                GameCanvas.ck = 1
            return
        if v == 3:
            if cM[2] > 0:
                cM[2] = cM[2] - 1
            else:
                cM[2] = GameCanvas.dq[0] // 6
            GameCanvas.ck = 1
            return
        if v == 28:
            if cM[1] <= 0 and GameCanvas.ej == 8:
                cM[1] = 1
                GameCanvas.ck = 1
                return
            GameCanvas.ck = 1
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 0:
                cM[1] = consts.z[GameCanvas.ej + 1] - consts.z[GameCanvas.ej] - 1
                return
            return
        if v == 5:
            GameCanvas.ck = 1
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 0:
                cM[1] = 8
                return
            return
        if v == 18:
            GameCanvas.da = 1
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 0:
                cM[1] = GameCanvas.cN - 1
                return
            return
        if v == 6:
            GameCanvas.cz.aB = GameCanvas.cz.aB - 1 & 0x3
            GameCanvas.ck = 1
            return
        if v == 9:
            self.y_I(0)
            GameCanvas.ck = 1
            return
        if v == 15:
            c3 = cM[3]
            cM[c3] = cM[c3] - 1
            if cM[3] == 1:
                if cM[c3] < 0:
                    cM[c3] = 4
                GameCanvas.da = 2
                return
            if cM[1] < 4:
                if cM[c3] < 0:
                    cM[c3] = 17
            elif cM[c3] < 18:
                cM[c3] = 20
            GameCanvas.da = 3
            return
        if v == 16:
            GameCanvas.ck = 1
            cM[2] = cM[2] + 1
            if _inc_cmp(cM[2]) >= GameCanvas.cN:
                cM[2] = 0
                return
            return
        if v == 17:
            cM[2] = cM[2] - 1
            if _dec_cmp(cM[2]) < 0:
                cM[2] = GameCanvas.cN - 1
            GameCanvas.da = 1
            return
        if v == 19:
            cM[1] = cM[1] - 4
            if cM[1] < 0:
                cM[1] = 0
            GameCanvas.ck = 1
            return
        if v == 25:
            cM[2] = cM[2] - 5
            cM[1] = cM[1] - 5
            if cM[2] < 0:
                cM[2] = 20
                cM[1] = 20 + imod(cM[1] + 20, 5)
            GameCanvas.ck = 1

    def aE(self):  # e.java:586-686  (RIGHT)
        cM = GameCanvas.cM
        v = cM[0]
        if v == 1:
            if GameCanvas.bj and GameCanvas.cq < 44:
                GameCanvas.cq = i8(GameCanvas.cq + 1)
                self.C_v()
                GameCanvas.ck = 1
            return
        if v == 3:
            if (cM[2] + 1) * 6 - 1 < GameCanvas.dq[0]:
                cM[2] = cM[2] + 1
            else:
                cM[2] = 0
            GameCanvas.ck = 1
            return
        if v == 28:
            if cM[1] >= 1 and GameCanvas.ej == 8:
                GameCanvas.ck = 1
                cM[1] = 0
                return
            GameCanvas.ck = 1
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= consts.z[GameCanvas.ej + 1] - consts.z[GameCanvas.ej]:
                cM[1] = 0
                return
            return
        if v == 5:
            GameCanvas.ck = 1
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= 9:
                cM[1] = 0
                return
            return
        if v == 18:
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= GameCanvas.cN:
                cM[1] = 0
            GameCanvas.da = 1
            return
        if v == 6:
            GameCanvas.cz.aB = GameCanvas.cz.aB + 1 & 0x3
            GameCanvas.ck = 1
            return
        if v == 9:
            self.y_I(1)
            GameCanvas.ck = 1
            return
        if v == 15:
            c3 = cM[3]
            cM[c3] = cM[c3] + 1
            if cM[3] == 1:
                if cM[c3] > 4:
                    cM[c3] = 0
                GameCanvas.da = 2
                return
            if cM[1] < 4:
                if cM[c3] > 17:
                    cM[c3] = 0
            elif cM[c3] > 20:
                cM[c3] = 18
            GameCanvas.da = 3
            return
        if v == 16:
            GameCanvas.ck = 1
            cM[2] = cM[2] - 1
            if _dec_cmp(cM[2]) < 0:
                cM[2] = GameCanvas.cN - 1
                return
            return
        if v == 17:
            cM[2] = cM[2] + 1
            if _inc_cmp(cM[2]) >= GameCanvas.cN:
                cM[2] = 0
            GameCanvas.da = 1
            return
        if v == 19:
            cM[1] = cM[1] + 4
            if cM[1] >= GameCanvas.cN:
                cM[1] = GameCanvas.cN - 1
            GameCanvas.ck = 1
            return
        if v == 25:
            cM[2] = cM[2] + 5
            cM[1] = cM[1] + 5
            if cM[2] > 20:
                cM[2] = 0
                cM[1] = imod(cM[1], 5)
            GameCanvas.ck = 1

    def b_v(self):  # e.java:688-1000  (FIRE)
        cM = GameCanvas.cM
        if cM[0] == 9:
            self.y_I(1)
            GameCanvas.ck = 1
            return
        if cM[0] == 5:
            v = cM[1]
            if v == 4:
                GameCanvas.ej = 0
            elif v == 5:
                GameCanvas.ck = 1
                GameCanvas.cO = cM[0]
                cM[0] = 28
                cM[1] = 0
                cM[2] = 0
                GameCanvas.dE = GameCanvas.ga
                GameCanvas.ei = i16(GameCanvas.cO)
                GameCanvas.ej = 8
                return
            elif v == 6:
                GameCanvas.cS.e_I(41)
                return
            elif v == 7:
                GameCanvas.cS.e_I(42)
                return
            elif v == 8:
                GameCanvas.cS.e_I(28)
                GameCanvas.ck = 1
                return
            arrayOfInt = [0, 1, 3, 4, 5]
            cM[1] = arrayOfInt[cM[1]]
        if Menus.m_II(cM[0], cM[1] % 7) > -1:
            self.c_v()
            GameCanvas.cN = consts.v[cM[0]]
            c0 = cM[0]
            if c0 == 7:
                GameCanvas.cz.k = ""
            elif c0 == 9:
                GameCanvas.ai()
            elif c0 == 10:
                GameCanvas.dE = GameCanvas.fW
            elif c0 == 12:
                GameCanvas.dE = GameCanvas.fX
            elif c0 == 13:
                GameCanvas.dE = GameCanvas.fY
            elif c0 == 27:
                GameCanvas.dE = GameCanvas.ga
                GameCanvas.ei = i16(GameCanvas.cO)
            elif c0 == 28:
                GameCanvas.ej = i16(cM[1])
                GameCanvas.cN = consts.z[GameCanvas.ej + 1] - consts.z[GameCanvas.ej]
            elif c0 == 14:
                GameCanvas.O_v()
            elif c0 == 15:
                cM[3] = 1
                GameCanvas.ct[37] = self.d_T(GameCanvas.bA.a_I(44))
                GameCanvas.ct[38] = self.d_T(GameCanvas.bA.a_I(45))
            elif c0 == 17:
                cz = GameCanvas.cz
                if GameCanvas.cO == 16 and cz.X[cM[2]].a != 0:
                    for b in range(25):
                        if 0 == cz.Y[b].a:
                            self.a_LzLz(cz.X[cM[2]], cz.Y[b])
                self.ag()
            elif c0 in (21, 22, 23, 24):
                self.aY()
            elif c0 == 1:
                Menus.aG()
                self.C_v()
            elif c0 == 3:
                GameCanvas.dm = i16(cM[1])
                self.D_v()
            elif c0 == 20:
                self.bg_v()
            cM[2] = 0
            cM[1] = 0
            return
        v = cM[0]
        if v == 0:
            if cM[1] == 3:
                if GameCanvas.fo == 0:
                    GameCanvas.cS.e_I(35)
                    return
                if GameCanvas.cz.S != 0 and GameCanvas.fo != 0:
                    self.c_v()
                    cM[0] = 19
                    GameCanvas.fu = i16(GameCanvas.L_I(504))
                    if GameCanvas.fu != 0 and config.ORIG_BUG["B3"]:
                        Menus.seal_list()
                    if GameCanvas.fu != 0:
                        GameCanvas.cN = 44
                    else:
                        GameCanvas.cN = GameCanvas.fo
                    Menus.bh_v()
                    cM[2] = 0
                    cM[1] = 0
                    return
                GameCanvas.cS.e_I(35)
                GameCanvas.ck = 0
                GameCanvas.cL = 0
                GameCanvas.cK = 0
                return
            if cM[1] == 2:
                GameCanvas.be.g_v()
                GameCanvas.ck = 0
                GameCanvas.cL = 0
                GameCanvas.cK = 0
                return
        elif v == 5:
            GameCanvas.ck = 1
            if cM[1] == 0:
                if GameCanvas.aq():
                    self.U_v()
                    if GameCanvas.fS != 0:
                        return
                    GameCanvas.ai()
                    self.F_v()
                    self.c_v()
                    GameCanvas.cK = 0
                    GameCanvas.cL = 0
                    cM[0] = 0
                    GameCanvas.cN = consts.v[cM[0]]
                    GameCanvas.dE = GameCanvas.fU
                    cM[2] = 0
                    cM[1] = 0
                    self.aA()
                    if GameCanvas.dj != 0:  # e.java:856-866  (the save was made on the map: back into it)
                        self.C_v()
                        self.bi_v()
                        self.D_v()
                        self.y_v()
                        self.U_v()
                        GameCanvas.dW[1] = GameCanvas.B_v()
                        GameCanvas.dW[0] = GameCanvas.B_v()
                        GameCanvas.dV = GameCanvas.dW[0] - GameCanvas.dV
                        self.a__I(-1)
                        return
                return
            if cM[1] == 1:
                GameCanvas.bz = None
                GameCanvas.bz = NameBuffer("", 8, 10)
                if GameCanvas.aq():
                    GameCanvas.cS.e_I(3)
                    return
                self.au()
                return
        elif v in (8, 14):
            if GameCanvas.cz.J > 0:
                GameCanvas.da = 1
                GameCanvas.cz.J -= 1
                if cM[1] == 0:
                    GameCanvas.cz.o += 5
                elif cM[1] == 1:
                    GameCanvas.cz.q += 3
                elif cM[1] == 2:
                    GameCanvas.cz.m += 1
                elif cM[1] == 3:
                    GameCanvas.cz.n += 1
                if cM[0] == 8 and GameCanvas.cz.J == 0:
                    GameCanvas.cS.e_I(4)
                    GameCanvas.ck = 1
                    return
        elif v == 29:
            GameCanvas.cS.e_I(36)
        elif v == 10:
            if cM[1] == 2:
                GameCanvas.cS.e_I(5)
                return
        elif v == 11:
            if cM[1] == 0:
                if self.ar() != 0:
                    GameCanvas.cS.e_I(0)
            return
        elif v == 25:
            if (GameCanvas.ed & 1 << cM[1]) != 0:
                self.c_v()
                self.l_II(cM[1], 0)
                return
            GameCanvas.cS.a_T("3You must first complete|the missions needed|to view this ending.")
            return
        elif v == 15:
            cz = GameCanvas.cz
            if cM[3] == 1:
                if cz.V[cM[1]] != 0:
                    cM[2] = consts.aD[cz.V[cM[1]] - 12]
                    cz.V[cM[1]] = 0
                elif cM[1] < 4:
                    cM[2] = 0
                else:
                    cM[2] = 18
                cM[3] = 2
                if cM[2] < 18:
                    GameCanvas.da = 6
                    return
                GameCanvas.ck = 1
                return
            if consts.aC[cM[2]] != 0:
                if cz.W[consts.aC[cM[2]] - 12] != 0:
                    cz.V[cM[1]] = consts.aC[cM[2]]
                    cM[3] = 1
                GameCanvas.da = 6
                return
        elif v == 17:
            cz = GameCanvas.cz
            it = cz.Y[cM[2]]
            if it.a != 0:
                b = GameCanvas.g_I(it.a)
                if GameCanvas.m_I(it.a) <= cz.l:
                    if it.a == 434:
                        it.a = 0
                        cz.o += 5
                        GameCanvas.cS.e_I(23)
                    elif it.a == 435:
                        it.a = 0
                        cz.q += 3
                        GameCanvas.cS.e_I(24)
                    elif it.a == 436:
                        it.a = 0
                        cz.n += 1
                        GameCanvas.cS.e_I(25)
                    elif it.a == 437:
                        it.a = 0
                        cz.m += 1
                        GameCanvas.cS.e_I(26)
                    elif it.a in (502, 504):
                        GameCanvas.cS.e_I(17)
                    else:
                        self.a_LzLz(it, cz.X[consts.aE[b]])
                else:
                    GameCanvas.cS.e_I(17)
            GameCanvas.da = 1
            return
        elif v == 1:
            if (GameCanvas.dw & 1 << GameCanvas.ds[cM[1]] - 1) != 0:
                self.c_v()
                cM[0] = 2
                GameCanvas.cN = consts.v[cM[0]]
                GameCanvas.dk = i16(i8(cM[1]))
                self.bi_v()
                cM[2] = 0
                cM[1] = 0
                return
        elif v == 3:
            GameCanvas.cS.e_I(6)
            return

    def aF(self):  # e.java:1002-1109  (BACK)
        cM = GameCanvas.cM
        bool_ = False
        if consts.u[cM[0]] > -1:
            if cM[0] in (14, 15, 16, 17, 18):
                self.ar()
            if consts.u[cM[0]] > 99:
                GameCanvas.ej = 0
                if cM[0] == 28 and GameCanvas.cO == 5:
                    GameCanvas.ej = 7
                    bool_ = True
                cM[0] = GameCanvas.cO
                if cM[0] == 0:
                    GameCanvas.cK = 0
                    GameCanvas.cL = 0
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
                    GameCanvas.cK = 0
                    GameCanvas.cL = 0
                GameCanvas.ap()
                GameCanvas.ak()
                if GameCanvas.cO == 5:
                    if cM[1] == 3:
                        cM[1] = 2
                    elif cM[1] == 4:
                        cM[1] = 3
                        if GameCanvas.bW == 3:  # e.java:1048-1056  (back to the map's pause menu)
                            GameCanvas.bV = GameCanvas.bW
                            GameCanvas.bW = -1
                            cM[0] = 10
                            cM[1] = 4
                            GameCanvas.cN = 7
                            GameCanvas.dE = GameCanvas.fZ
                            return
                    elif cM[1] == 5:
                        cM[1] = 4
                if GameCanvas.cO == 25:
                    cM[1] = 4
                if GameCanvas.cO == 27:
                    cM[1] = 3
                    if GameCanvas.bW == 3:  # e.java:1066-1074
                        GameCanvas.bV = GameCanvas.bW
                        GameCanvas.bW = -1
                        cM[0] = 10
                        cM[1] = 4
                        GameCanvas.cN = 7
                        GameCanvas.dE = GameCanvas.fZ
                        return
        else:
            v = cM[0]
            if v == 0:
                GameCanvas.aj()
                Menus.aG()
                self.ae_v()
                cM[0] = 5
                GameCanvas.cN = 10
                cM[2] = 0
                cM[1] = 0
                GameCanvas.cS.b = 0
                GameCanvas.ck = 1
                return
            if v == 15:
                if cM[3] == 1:
                    cM[0] = 13
                    GameCanvas.ap()
                    GameCanvas.ct[37] = None
                    GameCanvas.ct[38] = None
                    self.ar()
                    return
                cM[3] = 1
                GameCanvas.da = 6
                return
            if v == 27:
                cM[0] = GameCanvas.ei
                GameCanvas.ap()
                GameCanvas.ak()

    @staticmethod
    def aG():  # e.java:1111-1118
        GameCanvas.cy = 0
        while GameCanvas.cy < 4:
            GameCanvas.ct[26 + GameCanvas.cy] = None
            GameCanvas.cy += 1
        GameCanvas.gl = None

    def c_v(self):  # e.java:1120-1127  (remember cursor, go to the sub-menu)
        cM = GameCanvas.cM
        GameCanvas.cO = cM[0]
        GameCanvas.cP[cM[0]] = i16(cM[1])
        GameCanvas.cQ[cM[0]] = i16(cM[2])
        cM[0] = Menus.m_II(cM[0], cM[1] % 7)
        GameCanvas.ck = 1
        GameCanvas.da = 0

    def d_v(self):  # e.java:1129-1139
        GameCanvas.ct[17] = None
        GameCanvas.ct[10] = None
        GameCanvas.cU = None
        GameCanvas.cW = None
        GameCanvas.cV = None
        for b in range(1, 4):
            GameCanvas.ct[0 + b] = None
        GameCanvas.fN = None
        Menus.aG()

    def e_v(self):  # e.java:1141-1143  (menu background ct[7])
        self.a_MIIIIII(GameCanvas.ct[7], 0, 0, GameCanvas.bZ.a, GameCanvas.bZ.b, 0, 0)

    def f_v(self):  # e.java:1145-1227  (vertical list menu: 1 2 10 11 12 13 25 27)
        cM = GameCanvas.cM
        i = GameCanvas.dd - 90
        arrayOfByte = [13, 34, 20, 0, 0, 0, 0, 0, 0, 0,
                       12, 18, 12, 13, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 13, 0, 0]
        b2 = 5 if GameCanvas.cN > 5 else GameCanvas.cN
        if cM[0] == 25 and cM[2] >= 20:
            b2 = 4
            if cM[1] >= 24:
                cM[1] = 23
        j_ = GameCanvas.de - idiv(b2 * 30 - 10, 2)
        if GameCanvas.bV == 3 or GameCanvas.bW == 3:
            j_ -= 30
        k = j_
        b = arrayOfByte[cM[0]]
        for b1 in range(b2):
            if cM[1] - cM[2] == b1:
                bool_ = True
                Gfx.a_Lg(GameCanvas.bw)
            else:
                bool_ = False
                Gfx.a_Lg(GameCanvas.bu)
            m = i
            self.a_IIIIZ(m, j_ + GameCanvas.dc, 180, 20, bool_)
            if GameCanvas.bV == 2:
                if cM[0] == 0:
                    if cM[2] + b1 == 3 and (0 == GameCanvas.cz.S or GameCanvas.fo == 0):
                        Gfx.a_Lg(GameCanvas.bx)
                elif cM[0] == 1:
                    if GameCanvas.bj:
                        GameCanvas.dw = -1
                    if 0 == (GameCanvas.dw & 1 << GameCanvas.ds[cM[2] + b1] - 1):
                        Gfx.a_Lg(GameCanvas.bx)
                elif cM[0] == 25:
                    if 0 == (GameCanvas.ed & 1 << cM[2] + b1):
                        Gfx.a_Lg(GameCanvas.bx)
            else:
                if GameCanvas.cR.a == 1:
                    if cM[2] + b1 == 2 and (GameCanvas.ez > 0 or GameCanvas.cr != 0 or GameCanvas.eD[0] != 0):
                        Gfx.a_Lg(GameCanvas.bx)
            if cM[0] == 25:
                if cM[2] + b1 < 24:
                    arrayOfByte1 = self.d_II(54, 38 + cM[2] + b1)
                    str_ = GameCanvas.a_ABII(arrayOfByte1, 0, len(arrayOfByte1))
                    self.b_TII(str_, j_ - 1, 18)
            elif cM[0] in (0, 10, 12, 13, 27):
                self.b_TII(GameCanvas.b_TI(GameCanvas.dE[0], b1 + cM[2]), j_ - 1, 0)
            else:
                self.b_TII(GameCanvas.dE[b1 + cM[2]], j_ - 1, b)
            j_ += 30
        if cM[0] == 25:
            self.a_IIIZ(cM[2] // 5 + 1, 5, GameCanvas.bZ.b - 35, True)
        elif cM[2] != 0 or cM[2] + 5 < GameCanvas.cN - 1:
            self.f_III(2, GameCanvas.dd - 8 - GameCanvas.db, k - 10 - 5)
            self.f_III(3, GameCanvas.dd - 8 - GameCanvas.db, j_ - 5)
        if cM[0] == 10:
            Gfx.a_MIII(GameCanvas.bU, 120, GameCanvas.dc + 15, 17)
            Gfx.a_Lg(GameCanvas.bu)
            self.b_TII("PAUSE", 13, 0)
        if GameCanvas.bj and cM[0] == 1:
            Gfx.a_Lg(GameCanvas.bu)
            Gfx.b_IIIII(GameCanvas.bJ // 2 - 16, GameCanvas.bK - 17, 32, 17, 0)
            Gfx.a_TIII("" + str(GameCanvas.cq + 1), GameCanvas.bJ // 2, GameCanvas.bK - 16, 1)

    def j_v(self):  # e.java:1471-1521  (Options: Sound / Volume / Speed)
        i = GameCanvas.de - 50
        if GameCanvas.cM[1] == 0:
            GameCanvas.cM[1] = 1
        for b in range(1, 3):
            if GameCanvas.cM[1] == b:
                bool_ = True
                Gfx.a_Lg(GameCanvas.bw)
            elif b == 3:
                bool_ = False
                Gfx.a_Lg(GameCanvas.bx)
            else:
                bool_ = False
                Gfx.a_Lg(GameCanvas.bu)
            self.a_IIIIZ(GameCanvas.dd - 100, i + GameCanvas.dc, 80, 20, bool_)
            self.a_IIIIZ(GameCanvas.dd - 10, i + GameCanvas.dc, 110, 20, bool_)
            GameCanvas.c_TII(GameCanvas.gb[b], GameCanvas.dd - 100 + 40 - GameCanvas.db, i + 1)
            if bool_:
                self.f_III(0, GameCanvas.dd - 10 - GameCanvas.db, i + 2)
                self.f_III(1, GameCanvas.dd - 10 + 110 - 10 - 1 - GameCanvas.db, i + 2)
            if b == 0:
                str_ = GameCanvas.gc[1 if GameCanvas.df else 0]
            elif b == 1:
                str_ = ""
                for b1 in range(GameCanvas.dg // 25):
                    str_ = str_ + 'I'
                if str_ == "":
                    str_ = "OFF"
            elif b == 2:
                str_ = GameCanvas.ge[GameCanvas.dh]
            elif b == 3:
                str_ = consts.aX[GameCanvas.ep]
            else:
                return
            GameCanvas.c_TII(str_, GameCanvas.dd + 156 - 111 - GameCanvas.db, i + 1)
            i += 10
            i += 20

    def l_v(self):  # e.java:2311-2348  (Help / About page cM[1] of topic ej)
        if GameCanvas.bV == 3 or GameCanvas.bW == 3:
            GameCanvas.de -= 30
        i = GameCanvas.cM[1] + consts.z[GameCanvas.ej]
        arrayOfByte = self.d_II(61, i)
        if GameCanvas.bV == 2:
            self.b_ABII(arrayOfByte, 190, 0)
            self.e_IIII(GameCanvas.dd - 100 + GameCanvas.db, GameCanvas.de - 90 + GameCanvas.dc, 200, 175)
        else:
            self.b_ABII(arrayOfByte, 190, 0)
            self.e_IIII(GameCanvas.dd - 100, GameCanvas.de - 70 + GameCanvas.dc, 200, 120)
        Gfx.a_Lg(GameCanvas.bu)
        for b in range(GameCanvas.dq[0] + 1):
            if GameCanvas.bV == 2:
                if GameCanvas.cM[0] == 28 and GameCanvas.ej == 8:
                    self.b_TII(GameCanvas.dp[0][b], GameCanvas.de - 80 + b * 20 + 3, 30)
                    if GameCanvas.cM[1] == 1:
                        self.b_TII("v" + GameCanvas.bh, GameCanvas.de - 80 + 20 + 3, 30)
                else:
                    GameCanvas.d_TII(GameCanvas.dp[0][b], GameCanvas.dd - 95 - 1, GameCanvas.de - 80 + b * 20 + 3)
            else:
                GameCanvas.d_TII(GameCanvas.dp[0][b], GameCanvas.dd - 90 - 1 - GameCanvas.db, GameCanvas.de - 62 + b * 15)
        n = consts.z[GameCanvas.ej + 1] - consts.z[GameCanvas.ej]
        if GameCanvas.bV == 2:
            if GameCanvas.bW == 3:
                self.a_IIIZ(GameCanvas.cM[1] + 1, n, GameCanvas.bZ.b - 100, True)
            else:
                self.a_IIIZ(GameCanvas.cM[1] + 1, n, GameCanvas.bZ.b - 35, True)
        else:
            self.a_IIIZ(GameCanvas.cM[1] + 1, n, GameCanvas.de + 65, True)
        if GameCanvas.bV == 3 or GameCanvas.bW == 3:
            GameCanvas.de += 30

    def a_IIIZ(self, paramInt1, paramInt2, paramInt3, paramBoolean):  # e.java:2350-2372  (page "n / m" with arrows)
        if paramInt2 == 1:
            return
        i = GameCanvas.dd - 25 - 10
        if paramInt2 > 1:
            if paramInt1 != 1 or paramBoolean:
                self.f_III(0, i, paramInt3)
            i += 60
            if paramInt1 != paramInt2 or paramBoolean:
                self.f_III(1, i, paramInt3)
        paramInt3 += 2
        i = GameCanvas.dd - (8 + 9 * ((2 if paramInt2 > 9 else 1) + (2 if paramInt1 > 9 else 1)) + 2) // 2
        i = i + (18 if paramInt1 > 9 else 9)
        self.e_III(paramInt1, i, paramInt3 + GameCanvas.dc)
        i += 1
        if GameCanvas.bW == 3:
            GameCanvas.a_IIIIMII(i - GameCanvas.db, paramInt3 + 16, 8, 12, GameCanvas.ct[20], 90, 0)
        else:
            GameCanvas.a_IIIIMII(i - GameCanvas.db, paramInt3, 8, 12, GameCanvas.ct[20], 90, 0)
        i += 9 + (18 if paramInt2 > 9 else 9)
        self.e_III(paramInt2, i, paramInt3 + GameCanvas.dc)

    def P_I(self, paramInt):  # e.java:1523-1593  (Skills: 5 hot-key slots + skill tree pages)
        cz = GameCanvas.cz
        cM = GameCanvas.cM
        arrayOfByte = [1, 3, 7, 9, 0]
        if 0 == paramInt:
            for b in range(5):
                self.i_II(40 + b * 30 + 4 * b, 60)
                self.d_IIII(arrayOfByte[b], 40 + b * 30 + 18 + 4 * b, 70, 0)
        if paramInt % 2 == 0:
            for b in range(5):
                self.i_II(40 + b * 30 + 4 * b, 90)
                if cz.V[b] != 0:
                    self.b_MIIIIII(GameCanvas.ct[37], 40 + b * 30 + 4 * b + 1, 91, 28, 28, (cz.V[b] - 12) * 28, 0)
            self.b_IIIIIII(40 + cM[1] * 30 + 4 * cM[1], 90, 30, 30, 255, 255, 255)
        arrayOfAc = [Rect(40, 140, 60, 20), Rect(40, 165, 60, 20)]
        if paramInt % 3 == 0:
            i = cM[2] // 6 << 1
            b2 = 2 if cM[2] < 18 else 1
            for b1 in range(b2):
                j_ = cM[2] // 6 * 6 + b1 * 3
                ac1 = arrayOfAc[b1]
                ac1.b = ac1.b + b1 * 10 + 5
                self.b_IIIIIII(ac1.a - 1, ac1.b - 1, ac1.c + 2, ac1.d + 2, 152, 152, 152)
                GameCanvas.a_LacI(ac1, 0)
                Gfx.a_Lg(GameCanvas.bu)
                GameCanvas.dD = GameCanvas.c_T(GameCanvas.gd[i + b1])
                GameCanvas.d_TII(GameCanvas.gd[i + b1], ac1.a + idiv(ac1.c - GameCanvas.dD, 2), ac1.b + 1)
                for b in range(3):
                    self.i_II(40 + (b + 2) * 34, 140 + 35 * b1)
                    if consts.aC[j_ + b] != 0:
                        if cz.W[consts.aC[j_ + b] - 12] != 0:
                            image = GameCanvas.ct[37]
                        else:
                            image = GameCanvas.ct[38]
                        self.b_MIIIIII(image, 40 + (b + 2) * 34 + 1, 140 + 35 * b1 + 1, 28, 28,
                                       (consts.aC[j_ + b] - 12) * 28, 0)
            if cM[3] == 2:
                # DECOMP-FIX F10: `35 * cM[2] % 6 / 3` -> `35 * (cM[2] % 6 / 3)`
                row = 35 * (cM[2] % 6 // 3) if F10 else 35 * cM[2] % 6 // 3
                self.b_IIIIIII(40 + (cM[2] % 3 + 2) * 34, 140 + row, 30, 30, 255, 255, 255)
            ac_ = Rect(210, 0, 3, 20)
            self.a_IIIIZ(210, 150, 3, 50, False)
            if i == 6:
                ac_.a = 210
                ac_.b = 152
                ac_.c = 3
                ac_.d = 46
                GameCanvas.a_LacI(ac_, GameCanvas.k_III(231, 227, 198))
            else:
                ac_.b = 151 + (i >> 1) * 14 + GameCanvas.dc
                GameCanvas.a_LacI(ac_, GameCanvas.k_III(231, 227, 198))
        # System.out.println("GameCanvas.DrawSkillSet(2)");
        if cM[3] == 1:
            self.b_IIIII(cz.V[cM[1]] + 2000, GameCanvas.dd - 100, GameCanvas.bZ.b - 70, 200, 22)
        else:
            self.b_IIIII(consts.aC[cM[2]] + 2000, GameCanvas.dd - 100, GameCanvas.bZ.b - 70, 200, 22)
        GameCanvas.da = 0

    def k_v(self):  # e.java:1595-1630  (description strip; scrolls when longer than the box)
        dF = GameCanvas.dF
        self.a_IIIIZ(dF.b.a + GameCanvas.db, dF.b.b + GameCanvas.dc, dF.b.c, dF.b.d, False)
        Gfx.a_Lg(GameCanvas.bu)
        if dF.a != 0:
            GameCanvas.dD = GameCanvas.c_T(dF.c)
            dF.d = i16(dF.d - 5)
            if dF.b.a - dF.d > GameCanvas.dD + 3:
                dF.d = i16(dF.b.a + dF.b.c)
        GameCanvas.d_TII(dF.c, dF.d, dF.b.b + (dF.b.d - 11 >> 1) - 2)
        i = (GameCanvas.bJ - dF.b.c) // 2
        j_ = dF.b.b + GameCanvas.dc
        s1 = 0
        s2 = 0
        if GameCanvas.bV == 3:
            s1 = GameCanvas.db
            s2 = GameCanvas.dc
            Gfx.b_IIIII(0, j_, i, dF.b.d, 0)
            Gfx.b_IIIII(GameCanvas.bJ - i, j_, i, dF.b.d, 0)
        self.a_MIIIIII(GameCanvas.ct[7], 0, j_, i, dF.b.d, -s1, j_ - s2)
        Gfx.c_IIIII(i - 1, j_, i - 1, j_ + dF.b.d - 1, GameCanvas.k_III(80, 80, 80))
        self.a_MIIIIII(GameCanvas.ct[7], GameCanvas.bJ - i, j_, i - s1, dF.b.d, GameCanvas.bJ - i - s1, j_ - s2)
        Gfx.c_IIIII(GameCanvas.bJ - i, j_, GameCanvas.bJ - i, j_ + dF.b.d - 1, GameCanvas.k_III(80, 80, 80))
        if GameCanvas.bV == 3:
            Gfx.a_IIII(0, j_, GameCanvas.bJ, dF.b.d)
            GameCanvas.bd.b_v()
            Gfx.a_v()
            Gfx.a_IIII(0, j_, i - 1, dF.b.d)
            GameCanvas.cS.b_I(170)
            Gfx.a_v()
            Gfx.a_IIII(GameCanvas.bJ - i + 1, j_, i - 1, dF.b.d)
            GameCanvas.cS.b_I(170)
            Gfx.a_v()

    def n_II(self, paramInt1, paramInt2):  # e.java:1632-1654  (Gear: hero sprite + 9 equipment slots)
        cz = GameCanvas.cz
        arrayOfByte1 = [-77, -77, -77, -33, 3, 47, 47, 47, -15]
        arrayOfByte2 = [21, -15, -51, -79, -79, -51, -15, 21, 49]
        GameCanvas.ct[39] = self.d_T(GameCanvas.bA.a_I(50))
        ct39 = GameCanvas.ct[39]
        self.b_MIIIIII(ct39, GameCanvas.dd - ct39.getWidth() // 2, GameCanvas.de - ct39.getHeight() // 2,
                       ct39.getWidth(), ct39.getHeight(), 0, 0)
        GameCanvas.ct[39] = None
        for b in range(9):
            if cz.X[b].a != 0:
                self.e_I(cz.X[b].a)
                self.g_IIII(cz.X[b].a, GameCanvas.dd + arrayOfByte1[b], GameCanvas.de + arrayOfByte2[b], 0)
        self.b_IIIIIII(GameCanvas.dd + arrayOfByte1[paramInt1] - 1, GameCanvas.de + arrayOfByte2[paramInt1] - 1, 30, 30, 255, 255, 255)
        GameCanvas.fK[24] = GameCanvas.dd + arrayOfByte1[paramInt1] + GameCanvas.db + 7
        GameCanvas.fK[25] = GameCanvas.de + arrayOfByte2[paramInt1] + GameCanvas.dc + 7
        f1 = cz.aE[1]
        self.b_MIIIIII(cz.aH, GameCanvas.dd - f1.e, GameCanvas.de + 7 - f1.f + 17, f1.c, f1.d, f1.a, f1.b)
        f2 = cz.aC[1]
        self.b_MIIIIII(cz.aG, GameCanvas.dd - f2.e, GameCanvas.de + 7 - f2.f + 17, f2.c, f2.d, f2.a, f2.b)
        if paramInt2 != 0:
            GameCanvas.a_LzZI(self.o_I(-1), True, -1)
            return
        self.b_IIIII(paramInt1 + 1000, GameCanvas.dd - 79, GameCanvas.de + 81 + 5, 158, 20)

    def Q_I(self, paramInt):  # e.java:1656-1692  (Inventory: 5x5 grid in 2 pages + gold)
        cz = GameCanvas.cz
        cM = GameCanvas.cM
        arrayOfInt1 = [GameCanvas.dd - 75, GameCanvas.dd - 45, GameCanvas.dd - 15, GameCanvas.dd + 15, GameCanvas.dd + 45]
        arrayOfInt2 = [GameCanvas.de - 45, GameCanvas.de - 15, GameCanvas.de + 15]
        ac_ = Rect(GameCanvas.dd + 80, GameCanvas.de - 40, 5, 80)
        if cM[2] < 15:
            b2 = 3
            b3 = 0
        else:
            b2 = 2
            b3 = 15
        if paramInt != 0:
            self.b_MIIIIII(GameCanvas.ct[7], GameCanvas.dd - 75, GameCanvas.de - 45, 150, 100, GameCanvas.dd - 75, GameCanvas.de - 45)
        for b1 in range(b2):
            for b in range(5):
                self.i_II(arrayOfInt1[b] + GameCanvas.db, arrayOfInt2[b1] + GameCanvas.dc)
                self.e_I(cz.Y[b3 + b1 * 5 + b].a)
                self.g_IIII(cz.Y[b3 + b1 * 5 + b].a, arrayOfInt1[b] + 1, arrayOfInt2[b1] + 1, 0)
        GameCanvas.a_LacI(ac_, GameCanvas.k_III(148, 148, 148))
        ac_.a += 1
        ac_.b += 1
        ac_.c -= 2
        ac_.d -= 2
        GameCanvas.a_LacI(ac_, GameCanvas.k_III(33, 0, 0))
        ac_.b = GameCanvas.de - 39 + (39 if b3 != 0 else 0) + GameCanvas.dc
        ac_.d = 39
        GameCanvas.a_LacI(ac_, GameCanvas.k_III(231, 227, 198))
        self.b_IIIII(cM[2] + 1100, GameCanvas.dd - 75, GameCanvas.de + 50, 150, 22)
        self.b_IIIIIII(arrayOfInt1[cM[2] % 5], arrayOfInt2[(cM[2] - b3) // 5] + GameCanvas.dc, 30, 30, 255, 255, 255)
        if 0 == paramInt:
            self.J_v()
        GameCanvas.da = 0

    def d_I(self, paramInt):  # e.java:3022-3058  (Assign Items: 5 potion slots, * and # quick keys)
        cz = GameCanvas.cz
        if GameCanvas.bV == 3:
            GameCanvas.de -= 30
        if 0 == paramInt:
            self.J_v()
            Gfx.a_Lg(GameCanvas.bu)
            for b1 in range(5):
                self.a_IIIIZ(GameCanvas.dd - 80 + 32 * b1, GameCanvas.de - 40 + GameCanvas.dc, 30, 22, False)
                if cz.aa[0] == b1:
                    GameCanvas.d_TII(" * ", GameCanvas.dd - 80 + 32 * b1 - GameCanvas.db, GameCanvas.de - 38)
                elif cz.aa[1] == b1:
                    GameCanvas.d_TII(" # ", GameCanvas.dd - 80 + 32 * b1 - GameCanvas.db, GameCanvas.de - 38)
        for b in range(5):
            if GameCanvas.bV == 3:
                self.a_IIIIZ(GameCanvas.dd - 79 + 32 * b, GameCanvas.de + 6, 28, 28, False)
                self.g_IIII(cz.Z[b].a, GameCanvas.dd - 79 + 32 * b - GameCanvas.db, GameCanvas.de + 6 - GameCanvas.dc, b)
            else:
                self.a_IIIIZ(GameCanvas.dd - 79 + 32 * b, GameCanvas.de - 10, 28, 28, False)
                self.g_IIII(cz.Z[b].a, GameCanvas.dd - 79 + 32 * b - GameCanvas.db, GameCanvas.de - 10 - GameCanvas.dc, b)
        if GameCanvas.bV == 3:
            self.b_IIIIIII(GameCanvas.dd - 80 + 32 * GameCanvas.cM[1], GameCanvas.de + 6, 30, 29, 255, 255, 255)
        else:
            self.b_IIIIIII(GameCanvas.dd - 80 + 32 * GameCanvas.cM[1], GameCanvas.de - 10, 30, 29, 255, 255, 255)
        GameCanvas.da = 0
        self.b_IIIII(GameCanvas.cM[1] + 1200, GameCanvas.dd - 80 - GameCanvas.db, GameCanvas.de + 30, 160, 22)
        self.a_IIIIZ(GameCanvas.dd - 80, GameCanvas.de + 60 + GameCanvas.dc, 160, 22, False)
        Gfx.a_Lg(GameCanvas.bu)
        self.b_TII("*,# key Assign", GameCanvas.de + 60, 15)
        if GameCanvas.bV == 3:
            GameCanvas.de += 30

    def g_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # e.java:3060-3081  (item icon)
        i = -1
        b = 0
        if paramInt1 > 500:
            i = paramInt1 - 501
            b = 3
        elif paramInt1 > 300:
            i = GameCanvas.cY.g
            b = 2
        elif paramInt1 > 100:
            i = GameCanvas.cX.f
            b = 1
        elif paramInt1 > 0:
            i = paramInt1 - 1
            b = 0
        if i > -1:
            self.b_MIIIIII(GameCanvas.ct[0 + b], paramInt2, paramInt3, 28, 28, i * 28, 0)
            if paramInt1 < 100:
                self.i_III(paramInt2, paramInt3 + 2, GameCanvas.cz.Z[paramInt4].b)

    # ---- Blacksmith (screens 21 Buy, 22 Sell, 23 Enchant, 24 Combine) ----------------------
    # fK[0] = mode (cM[0]-21), fK[9]/fK[10] = cursor col/row, fK[18] = cell, fK[19] = item id,
    # fK[20] = message for aV(), fK[21] = price, fK[26] = sparkle frame (-1 idle), fK[27] = 1 on Gear

    def a_IAzAI(self, paramInt, paramArrayOfz, paramArrayOfint):  # e.java:1804-1861  (item grid)
        i = GameCanvas.fK[8] * 5
        if GameCanvas.fK[11] == 1:
            ac1 = Rect(0, 0, 0, 0)
            ac2 = Rect(0, 0, 0, 0)
            ac1.c = 4
            ac1.a = GameCanvas.fK[12]
            ac1.d = GameCanvas.fK[6]
            ac1.b = paramInt
            GameCanvas.a_LacII(ac1, 16777215, 0)
            ac1.c -= 2
            ac1.a += 1
            ac1.d -= 2
            ac1.b += 1
            j_ = GameCanvas.fK[8] * 32
            k = ac2.d
            j_ = idiv(j_ * k, GameCanvas.fK[7])
            ac2.d = GameCanvas.fK[13]
            ac2.b += j_
            GameCanvas.a_LacI(ac2, 16777215)
            GameCanvas.b_LacI(ac1, 10000536)
        paramInt += 1
        b1 = 0
        b2 = 0
        while b1 < GameCanvas.fK[3]:
            j_ = GameCanvas.fK[5]
            for b in range(5):
                if i == GameCanvas.fK[18]:
                    bool_ = True
                    GameCanvas.fK[24] = j_ + 13 + 1
                    GameCanvas.fK[25] = paramInt + 13 + 1
                else:
                    bool_ = False
                for b3 in range(GameCanvas.fO[3]):
                    if GameCanvas.fO[b3] == i:
                        bool_ = True
                        GameCanvas.fP[b2].a = i16(j_ + 13 + 1)
                        GameCanvas.fP[b2].b = i16(paramInt + 13 + 1)
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
        if GameCanvas.fK[0] == 1 and 0 < z1.a < 100:
            bool_ = z1.b
        else:
            bool_ = 0
        self.a_IIII(z1.a, paramInt2, paramInt3, bool_)

    def a_IIZ(self, paramInt1, paramInt2, paramBoolean):  # e.java:1879-1881  (grid cell frame)
        GameCanvas.a_IIIIIIIZ(paramInt1 + 1, paramInt2 + 1, 26, 26, 0, 0, 16777215 if paramBoolean else 5263440, True)

    def a_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # e.java:1883-1902  (item icon by id + count)
        if paramInt1 > 500:
            image = GameCanvas.ct[3]
            i = paramInt1 - 501
        elif paramInt1 > 300:
            image = GameCanvas.ct[2]
            i = GameCanvas.bH[1].a_II(paramInt1 - 301, 7)
        elif paramInt1 > 100:
            image = GameCanvas.ct[1]
            i = GameCanvas.bH[0].a_II(paramInt1 - 101, 7)
        else:
            image = GameCanvas.ct[0]
            i = paramInt1 - 1
        GameCanvas.a_IIIIMII(paramInt2, paramInt3, 28, 28, image, i * 28, 0)
        if paramInt4 > 0:
            GameCanvas.a_IIIIMII(paramInt2, paramInt3, 9, 12, GameCanvas.ct[20], paramInt4 * 9, 0)

    def aP(self):  # e.java:1904-1910  (gold + item grid + description)
        i = GameCanvas.fK[1] + 1
        self.i_I(i)
        i += 29
        self.a_IAzAI(i, None, None)
        GameCanvas.a_LzZI(self.o_I(-1), True, -1)

    def c_Z(self, paramBoolean):  # e.java:1912-2111  (decompiler gave bytecode only; rebuilt from it)
        fK = GameCanvas.fK
        if paramBoolean:
            if fK[27] == 0:
                self.aP()
            else:
                self.n_II(fK[18], 1)
            if fK[23] == -1 and GameCanvas.cS.b == 0:
                # the Yes/No popup of Enchant / Combine has just closed
                fK[23] = 0
                if GameCanvas.ch == -5 and GameCanvas.cS.k == 0:
                    if fK[21] > GameCanvas.cz.E:
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
        GameCanvas.ck = 1
        if fK[0] == 2:
            self.aQ()
        elif fK[0] == 3:
            cz = GameCanvas.cz
            if fK[22] == 0:
                for b in range(3):
                    Item.a(cz.Y[GameCanvas.fO[b]])
                dst = cz.Y[GameCanvas.fO[2]]
                dst.a = GameCanvas.fQ.a
                dst.b = GameCanvas.fQ.b
                dst.c = GameCanvas.fQ.c
                dst.d = GameCanvas.fQ.d
                dst.e = GameCanvas.fQ.e
                dst.f = GameCanvas.fQ.f
            elif fK[31] != -1:
                Item.a(cz.Y[fK[31]])
                fK[31] = -1
            Menus.bb()
            fK[20] = 9
            cz.E -= fK[21]
        self.ar()
        Menus.aV()

    def aQ(self):  # e.java:2113-2135  (Enchant: roll success / fail / lost)
        arrayOfByte1 = [100, 90, 80, 70, 60, 45, 30, 10, 1]
        arrayOfByte2 = [0, 10, 20, 40, 50, 60, 70, 80, 90]
        z_ = self.o_I(-1)
        GameCanvas.fK[20] = 2
        GameCanvas.cz.E -= GameCanvas.fK[21]
        if GameCanvas.fK[22] == -1:
            GameCanvas.fK[23] = 2
        else:
            i = self.C_I(100) + 1
            if i > arrayOfByte1[z_.f]:
                i = self.C_I(100)
                GameCanvas.fK[23] = 2 if i <= arrayOfByte2[z_.f] else 1
            else:
                self.a_LzI(z_, 1)
                GameCanvas.fK[23] = 0
        if GameCanvas.fK[23] == 2:
            Item.a(z_)
            GameCanvas.fK[23] = 1

    def o_II(self, paramInt1, paramInt2):  # e.java:2137-2144  (sparkle frame)
        arrayOfByte1 = [0, 15, 30, 0, 20]
        arrayOfByte2 = [0, 0, 0, 16, 16]
        arrayOfByte3 = [16, 16, 16, 20, 24]
        n = arrayOfByte3[GameCanvas.fK[26]]
        paramInt1 -= n >> 1
        paramInt2 -= n >> 1
        GameCanvas.a_IIIIMII(paramInt1, paramInt2, n, n, GameCanvas.fN, arrayOfByte1[GameCanvas.fK[26]], arrayOfByte2[GameCanvas.fK[26]])

    def aR(self):  # e.java:2146-2156
        if GameCanvas.fK[0] == 2:
            self.o_II(GameCanvas.fK[24], GameCanvas.fK[25])
            return
        if GameCanvas.fK[0] == 3:
            for b in range(3):
                if GameCanvas.fP[b].a > 0 and GameCanvas.fP[b].b > 0:
                    self.o_II(GameCanvas.fP[b].a, GameCanvas.fP[b].b)

    @staticmethod
    def aV():  # e.java:2396-2451  (Blacksmith message popup)
        from pow.game.popups import Popups
        arrayOfString = ["Success", "Fail"]
        str_ = ""
        GameCanvas.cS.a_v()
        GameCanvas.ck = 1
        fK = GameCanvas.fK
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
                GameCanvas.cS.d = 200
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
                GameCanvas.cS.d = 200
        elif v == 9:
            str_ = "1Compounding| " + arrayOfString[fK[22]]
        GameCanvas.cS.a_T(str_)

    def aW(self):  # e.java:2453-2566  (Blacksmith keys)
        fK = GameCanvas.fK
        bool_ = True
        if fK[26] != -1:
            return
        ch = GameCanvas.ch
        if ch in (-1, 50):
            if fK[27] == 0:
                fK[10] = fK[10] - 1
            else:
                fK[18] = fK[18] + 1
                if _inc_cmp(fK[18]) > 8:
                    fK[18] = 0
            GameCanvas.dF.c = ""
        elif ch in (-2, 56):
            if fK[27] == 0:
                fK[10] = fK[10] + 1
            else:
                fK[18] = fK[18] - 1
                if _dec_cmp(fK[18]) < 0:
                    fK[18] = 8
            GameCanvas.dF.c = ""
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
            GameCanvas.dF.c = ""
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
            GameCanvas.dF.c = ""
        elif ch == -7:
            cM = GameCanvas.cM
            cM[0] = consts.u[cM[0]]
            GameCanvas.cN = consts.v[cM[0]]
            cM[1] = GameCanvas.cP[cM[0]]
            cM[2] = GameCanvas.cQ[cM[0]]
            GameCanvas.ck = 1
            bool_ = False
            GameCanvas.ct[39] = None
            GameCanvas.dF.c = ""
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
                if fK[0] == 3 and self.o_I(-1).a > 100:
                    b = 3
                    if GameCanvas.fO[3] > 0:
                        b = 0
                        while b < GameCanvas.fO[3] and GameCanvas.fO[b] != fK[18]:
                            b += 1
                    if b < GameCanvas.fO[3]:
                        while b < 2:
                            GameCanvas.fO[b] = GameCanvas.fO[b + 1]
                            b += 1
                        GameCanvas.fO[3] = GameCanvas.fO[3] - 1
                    else:
                        GameCanvas.fO[GameCanvas.fO[3]] = fK[18]
                        GameCanvas.fO[3] = GameCanvas.fO[3] + 1
                    if GameCanvas.fO[3] == 3:
                        self.aX()
        else:
            bool_ = False
        if bool_:
            self.ba()
            GameCanvas.bb.c_Z(True)

    def aX(self):  # e.java:2568-2626  (Combine: work out the result of 3 items)
        arrayOfInt = [0, 0, 0]
        i = 0
        for b in range(3):
            z_ = self.o_I(GameCanvas.fO[b])
            b1 = 0
            while b1 < b and arrayOfInt[b1] <= z_.a:
                b1 += 1
            for b2 in range(b, b1, -1):
                arrayOfInt[b2] = arrayOfInt[b2 - 1]
            arrayOfInt[b1] = z_.a
            i += z_.f
        Menus.a = ResReader.a("/" + GameCanvas.bE.a_I(68))
        if Menus.a is not None:
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
                GameCanvas.fK[22] = 2
                Menus.bb()
            else:
                j_ += self.C_I(k)
                arrayOfInt[0] = Menus.S_I(447 + j_)
                GameCanvas.fQ = self.J_I(arrayOfInt[0])
                GameCanvas.fK[21] = idiv(Menus.b_Lz(GameCanvas.fQ), 4)
                if arrayOfInt[0] < 500:
                    arrayOfInt[1] = GameCanvas.bH[1].a_II(arrayOfInt[0] - 301, 8)
                    arrayOfInt[2] = 15
                else:
                    arrayOfInt[1] = GameCanvas.bH[2].a_II(arrayOfInt[0] - 501, 7)
                    arrayOfInt[2] = 12
                arrayOfInt[1] = idiv(200 - arrayOfInt[1], 12)
                if arrayOfInt[1] >= self.C_I(101):
                    GameCanvas.fK[22] = 0
                    GameCanvas.fQ = self.a_LzI(GameCanvas.fQ, idiv(i, 3))
                else:
                    GameCanvas.fK[22] = 1
                    arrayOfInt[1] = idiv((100 - arrayOfInt[1]) * 10, arrayOfInt[2])
                    GameCanvas.fK[31] = GameCanvas.fO[self.C_I(3)] if arrayOfInt[1] >= self.C_I(101) else -1
                GameCanvas.fK[23] = -1
            GameCanvas.fK[20] = 8
            Menus.aV()
        Menus.a = None

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
                s = (paramz.b, paramz.c, paramz.d, paramz.e)[b1]
                i = s
                if i > 0:
                    i = idiv(idiv(i * j_, 10) + 50, 100)
                    if i == 0:
                        i = 1
                    if b1 == 0:
                        paramz.b = i16(paramz.b + i)
                    elif b1 == 1:
                        paramz.c = i16(paramz.c + i)
                    elif b1 == 2:
                        paramz.d = i16(paramz.d + i)
                    elif b1 == 3:
                        paramz.e = i16(paramz.e + i)
            paramz.f = i8(paramz.f + 1)
        return paramz

    @staticmethod
    def S_I(paramInt):  # e.java:2670-2672
        return Menus.a[paramInt * 2] & 0xFF | (Menus.a[paramInt * 2 + 1] & 0xFF) << 8

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
        if GameCanvas.cM[0] == 24:
            Menus.m_v()
            if GameCanvas.fK[16] < 3:
                GameCanvas.cS.e_I(39)
                GameCanvas.ck = 1
                GameCanvas.cM[1] = 3
                return True
        GameCanvas.az()
        self.aZ()
        return True

    def aZ(self):  # e.java:2709-2754  (grid layout of the current Blacksmith mode)
        fK = GameCanvas.fK
        fK[0] = GameCanvas.cM[0] - 21
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
        fK = GameCanvas.fK
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
        fK[19] = z_.a if z_ is not None else 0

    @staticmethod
    def c_I(paramInt):  # e.java:2774-2786  (item name)
        if paramInt < 100:
            return consts.aN[paramInt - 1]
        if paramInt < 300:
            return GameCanvas.bH[0].b_II(paramInt - 101, 0)
        if paramInt < 500:
            return GameCanvas.bH[1].b_II(paramInt - 301, 0)
        return GameCanvas.bH[2].b_II(paramInt - 501, 0)

    @staticmethod
    def bb():  # e.java:2788-2801  (clear the Combine selection)
        for b in range(len(GameCanvas.fO)):
            GameCanvas.fO[b] = 0
        for b in range(len(GameCanvas.fP)):
            if GameCanvas.fP[b] is None:
                GameCanvas.fP[b] = Point()
            GameCanvas.fP[b].a = 0
            GameCanvas.fP[b].b = 0
        if GameCanvas.fQ is None:
            GameCanvas.fQ = Item()
        Item.a(GameCanvas.fQ)

    @staticmethod
    def m_v():  # e.java:2803-2815  (count items: fK[16] backpack, fK[17] potions)
        GameCanvas.fK[16] = 0
        for b in range(25):
            if GameCanvas.cz.Y[b].a > 0:
                GameCanvas.fK[16] = GameCanvas.fK[16] + 1
        GameCanvas.fK[17] = 0
        for b in range(5):
            if GameCanvas.cz.Z[b].a > 0:
                GameCanvas.fK[17] = GameCanvas.fK[17] + 1

    @staticmethod
    def b_Lz(paramz):  # e.java:2817-2830  (price of an item)
        if paramz.a < 100:
            i = consts.y[paramz.a - 1]
        elif paramz.a < 300:
            i = GameCanvas.bH[0].a_II(paramz.a - 101, 6)
            i = i + paramz.b * 100
            i = i + paramz.c * 100
            i = i + idiv(paramz.d, 5) * 100
            i = i + idiv(paramz.e, 3) * 100
        elif paramz.a < 500:
            j_ = 800 if GameCanvas.bH[1].a_II(paramz.a - 301, 6) == 0 else 400
            i = paramz.b * j_
            i = i + paramz.c * j_
            i = i + idiv(paramz.d, 5) * j_
            i = i + idiv(paramz.e, 3) * j_
        else:
            i = GameCanvas.bH[2].a_II(paramz.a - 501, 6)
        return i

    def bc(self):  # e.java:2832-2883  (Buy)
        cz = GameCanvas.cz
        fK = GameCanvas.fK
        z_ = GameCanvas.fL[fK[18]]
        if z_.a == 0:
            fK[20] = -1
            return
        i = Menus.b_Lz(z_)
        if cz.E >= i:
            if z_.a < 100:
                b = 0
                while b < 5 and cz.Z[b].a != z_.a:
                    b += 1
                if b < 5:
                    if cz.Z[b].b < 5:
                        cz.Z[b].b = i16(cz.Z[b].b + 1)
                        fK[20] = 0
                    else:
                        fK[20] = 5
                else:
                    b = 0
                    while b < 5 and cz.Z[b].a != 0:
                        b += 1
                    if b < 5:
                        cz.Z[b].a = z_.a
                        cz.Z[b].b = 1
                        fK[17] = fK[17] + 1
                        fK[20] = 0
                    else:
                        fK[20] = 6
            elif fK[16] < 25:
                b = 0
                while b < 25 and cz.Y[b].a != 0:
                    b += 1
                y_ = cz.Y[b]
                y_.a = z_.a
                y_.b = z_.b
                y_.c = z_.c
                y_.d = z_.d
                y_.e = z_.e
                y_.f = z_.f
                Item.a(z_)
                fK[16] = fK[16] + 1
                fK[20] = 0
            else:
                fK[20] = 6
        else:
            fK[20] = 4
        if fK[20] == 0:
            cz.E -= i
            self.ar()

    def bd(self):  # e.java:2885-2905  (Sell, half price)
        cz = GameCanvas.cz
        fK = GameCanvas.fK
        z_ = self.o_I(-1)
        if z_ is None or z_.a == 0:
            return
        i = Menus.b_Lz(z_)
        if z_.a < 100:
            if cz.Z[fK[18]].b > 1:
                cz.Z[fK[18]].b = i16(cz.Z[fK[18]].b - 1)
            else:
                cz.Z[fK[18]].a = 0
                cz.Z[fK[18]].b = 0
                fK[17] = fK[17] - 1
        else:
            Item.a(z_)
            fK[16] = fK[16] - 1
        fK[20] = 11
        cz.E += idiv(i, 2)
        self.ar()

    def be(self):  # e.java:2907-2936  (Enchant: price and limit)
        fK = GameCanvas.fK
        z_ = self.o_I(-1)
        if z_.a == 0:
            fK[20] = -1
            return
        fK[22] = 0
        fK[21] = 0
        if 100 < z_.a < 500:
            if z_.a < 300:
                fK[22] = GameCanvas.bH[0].a_II(z_.a - 101, 5)
            else:
                fK[22] = GameCanvas.bH[1].a_II(z_.a - 301, 6)
            if fK[22] > 0:
                fK[21] = z_.b * 100
                fK[21] = fK[21] + z_.c * 100
                fK[21] = fK[21] + idiv(z_.d * 100, 5)
                fK[21] = fK[21] + idiv(z_.e * 100, 3)
                if z_.f >= fK[22]:
                    fK[22] = 0
                    fK[20] = 3
                    return
        fK[20] = 1
        if fK[22] != 0:
            fK[23] = -1

    def a_LzIIIIIZ(self, paramz, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramBoolean):  # e.java:3083-3206  (shop description)
        dF = GameCanvas.dF
        str1 = "/ Price: "
        str2 = "Price: "
        if paramz.a == 0:
            dF.a = 0
            dF.b.a = dF.b.b = dF.b.c = dF.b.d = 0
            dF.c = ""
            dF.b.a = (GameCanvas.bJ - 202) // 2 - GameCanvas.db
            dF.b.b = 200
            dF.b.c = paramInt3 + 2
            dF.b.d = paramInt4
            return
        if GameCanvas.fK[14] > 0 and paramInt5 == -1:
            paramInt5 = Menus.b_Lz(paramz)
        if paramz.a < 100:
            i = paramz.a - 1
            dF.c = consts.aN[i]
            if GameCanvas.fK[14] == 2:
                if len(dF.c) > 0:
                    dF.c += " / "
                dF.c += str2
                dF.c += GameCanvas.n_I(paramInt5 >> 1)
            dF.c += " / "
            if i < 9:
                str_ = "Recover " + str(consts.aP[i % 3]) + "% of total " + consts.aO[i // 3]
            else:
                str_ = "Ranged Atk"
            dF.c += str_
            if GameCanvas.fK[14] == 1:
                dF.c += str1
                dF.c += GameCanvas.n_I(paramInt5)
        else:
            if paramz.a < 300:
                str_ = GameCanvas.bH[0].b_II(paramz.a - 101, 0)
                i = consts.w[(paramz.a - 101) % 5]
            elif paramz.a < 500:
                str_ = GameCanvas.bH[1].b_II(paramz.a - 301, 0)
                i = GameCanvas.bH[1].a_II(paramz.a - 301, 8)
            else:
                str_ = GameCanvas.bH[2].b_II(paramz.a - 501, 0)
                i = GameCanvas.bH[2].a_II(paramz.a - 501, 7)
            if paramBoolean:
                dF.c += str_
            if GameCanvas.fK[14] == 2:
                if len(dF.c) > 0:
                    dF.c += " / "
                dF.c += str2
                dF.c += GameCanvas.n_I(paramInt5 >> 1)
            if len(dF.c) > 0:
                dF.c += " / "
            special = {434: " / Hp 5 Increased", 435: " / MP 3 Increased", 436: " / DEF 1 Increased",
                       437: " / ATK 1 Increased", 502: " / Catherine's scarf", 504: " / all General Visiting"}
            if paramz.a in special:
                dF.c += special[paramz.a][3:]
                if paramz.a == 504 and paramz.f > 0:
                    dF.c += " / Enchanted Lv" + str(paramz.f)
            else:
                if paramz.b > 0:
                    dF.c += "Atk+" + str(paramz.b) + " "
                if paramz.c > 0:
                    dF.c += "Def+" + str(paramz.c) + " "
                if paramz.d > 0:
                    dF.c += "HP+" + str(paramz.d) + " "
                if paramz.e > 0:
                    dF.c += "MP+" + str(paramz.e) + " "
                if paramz.f > 0:
                    dF.c += "/ Enchanted Lv" + str(paramz.f) + " "
                if i > 0:
                    dF.c += "/ Available at Lv" + str(i) + " "
            if GameCanvas.fK[14] == 1:
                dF.c += str1
                dF.c += GameCanvas.n_I(paramInt5)
        dF.b.a = (GameCanvas.bJ - 202) // 2 - GameCanvas.db
        dF.b.b = 200
        dF.b.c = paramInt3 + 2
        dF.b.d = paramInt4
        GameCanvas.dD = GameCanvas.c_T(dF.c)
        if GameCanvas.dD > paramInt3 - 2:
            dF.a = 1
            if GameCanvas.ch != -999:
                dF.d = i16(dF.b.a + dF.b.c)
                return
        else:
            dF.a = 0
            dF.d = i16(paramInt1 + 1)

    def g_v(self):  # e.java:1241-1244
        self.E_v()
        GameCanvas.ct[18] = self.d_T(GameCanvas.bA.a_I(77))

    def aJ(self):  # e.java:1370-1383  (Main Menu: caption strip + blinking arrows)
        i = GameCanvas.cM[1]
        j_ = GameCanvas.dd - 52 + GameCanvas.db
        if 0 == i and not GameCanvas.aq():
            i = 9
        GameCanvas.a_IIIIMII(j_, GameCanvas.bZ.b - 65, 116, 21, GameCanvas.ct[18], 0, i * 21)
        GameCanvas.a_IIIIMII(j_ - 24 - GameCanvas.dr % 3 * 2, GameCanvas.bZ.b - 65 + 2, 10, 16, GameCanvas.ct[17], 0, 0)
        GameCanvas.a_IIIIMII(j_ + 116 + 16 + GameCanvas.dr % 3 * 2, GameCanvas.bZ.b - 65 + 2, 10, 16, GameCanvas.ct[17], 10, 0)
        if GameCanvas.dr > 100:
            GameCanvas.dr = 32
            return
        GameCanvas.dr += 1

    def aK(self):  # e.java:1385-1404  (screen 6: choose the hero, 3 heads, the middle one is chosen)
        image = None
        i = GameCanvas.cz.aB - 1 & 0x3
        Gfx.a_Lg(GameCanvas.bu)
        for b in range(3):
            str_ = GameCanvas.M_I(65 + b)
            self.b_TII(str_, GameCanvas.de - 90 - b * 20 + 10, 0)
        for b in range(3):
            image = self.d_T(GameCanvas.bB.a_I(38 + i))
            self.b_IIIIIII(GameCanvas.dd - 94 + 69 * b + GameCanvas.db, GameCanvas.de + 9 + GameCanvas.dc, 50, 50, 148, 109, 82)
            self.a_IIIIIII(GameCanvas.dd - 93 + 69 * b + GameCanvas.db, GameCanvas.de + 10 + GameCanvas.dc, 48, 48, 33, 0, 0)
            self.b_MIIIIII(image, GameCanvas.dd - 92 + 69 * b, GameCanvas.de + 11, 46, 46, 0, 0)
            i = i + 1 & 0x3
        self.c_IIIIIII(GameCanvas.dd - 27 + GameCanvas.db + 1, GameCanvas.de + 8 + GameCanvas.dc, 52, 52, 255, 182, 82)
        self.f_III(0, GameCanvas.dd - 40, GameCanvas.de + 23)
        self.f_III(1, GameCanvas.dd + 30, GameCanvas.de + 23)

    def aL(self):  # e.java:1406-1413  (screen 7: the two caption lines)
        Gfx.a_Lg(GameCanvas.bu)
        GameCanvas.cy = 0
        while GameCanvas.cy < 2:
            self.b_TII(GameCanvas.M_I(69 + GameCanvas.cy), GameCanvas.de - 47 + GameCanvas.cy * 20, 0)
            GameCanvas.cy += 1

    def aM(self):  # e.java:1415-1427  (screen 7: the name box)
        i = GameCanvas.dd - 80 + GameCanvas.db
        j_ = GameCanvas.de + 8 + GameCanvas.dc
        Gfx.b_IIIII(i, j_, 160, 20, 0)
        Gfx.a_IIIII(i, j_, 160, 20, GameCanvas.k_III(173, 170, 173))
        Gfx.a_Lg(GameCanvas.bu)
        Gfx.a_TIII(GameCanvas.bz.a_v(), GameCanvas.bL, j_ + 2, 1)
        if GameCanvas.bz.b_v() == 0:
            GameCanvas.h_II(-1, 2)
            return
        GameCanvas.h_II(-1, 10)

    def O_I(self, paramInt):  # e.java:1429-1469  (screen 8/14: stat sheet; 1 = whole, 0 = numbers only)
        cz = GameCanvas.cz
        arrayOfInt1 = [cz.o, cz.q, cz.m, cz.n]
        image = None
        if paramInt != 0:
            arrayOfInt = self.p_v()
            GameCanvas.dZ[0] = i16(idiv(cz.G * 100, arrayOfInt[0]))
            image = self.d_T(GameCanvas.bA.a_I(26))
            i = image.getWidth()
            j_ = image.getHeight()
            GameCanvas.eN = GameCanvas.de - j_ // 2
            GameCanvas.eM = GameCanvas.dd - i // 2
            self.b_MIIIIII(image, GameCanvas.eM, GameCanvas.eN, i, j_, 0, 0)
            GameCanvas.c_TII(cz.k, GameCanvas.eM + 110, GameCanvas.eN + 6)
            self.d_IIII(cz.l, GameCanvas.eM + 152, GameCanvas.eN + 34, 0)
            self.d_IIII(cz.F, GameCanvas.eM + 152, GameCanvas.eN + 61, 0)
        else:
            arrayOfInt = [GameCanvas.eM + 88, GameCanvas.eN + 83, 68, 20]
            Gfx.b_IIIII(arrayOfInt[0], arrayOfInt[1], arrayOfInt[2], arrayOfInt[3], 0)
            arrayOfInt[0] = GameCanvas.eM + 39
            arrayOfInt[1] = GameCanvas.eN + 108
            arrayOfInt[2] = 104
            arrayOfInt[3] = 18
            for b1 in range(4):
                Gfx.b_IIIII(arrayOfInt[0], arrayOfInt[1], arrayOfInt[2], arrayOfInt[3], 0)
                arrayOfInt[1] = arrayOfInt[1] + 20
        arrayOfInt2 = [cz.u, cz.v, cz.s, cz.t]
        self.d_IIII(cz.J, GameCanvas.eM + 152, GameCanvas.eN + 86, 0)
        for b in range(4):
            i = self.d_IIII(arrayOfInt1[b], GameCanvas.eM + 44, GameCanvas.eN + 110 + b * 20, 1)
            if arrayOfInt2[b] > 0:
                self.b_MIIIIII(GameCanvas.ct[19], i + 1, GameCanvas.eN + 110 + b * 20, 10, 14, 105, 0)
                self.d_IIII(arrayOfInt2[b], i + 9, GameCanvas.eN + 110 + b * 20, 1)
        image = self.d_T(GameCanvas.bB.a_I(38 + cz.aB))
        self.b_MIIIIII(image, GameCanvas.eM + 2, GameCanvas.eN + 3, 46, 46, 0, 0)
        if cz.J > 0:
            self.a_IIIIIII(GameCanvas.eM + 144, GameCanvas.eN + 97 + 20 * GameCanvas.cM[1] + GameCanvas.dc + 11, 14, 18, 255, 255, 255)
        GameCanvas.da = 0

    def b_I(self, paramInt):  # e.java:2158-2165  (story: speaker portrait top-left, hero bottom-right)
        self.a_IIIIZ(19 + GameCanvas.db + 2, GameCanvas.de - 72 + 9 + GameCanvas.dc, 46, 46, True)
        if paramInt > -1:
            self.a_TIIIIII(GameCanvas.bB.a_I(0 + paramInt), 19 + GameCanvas.db + 2, GameCanvas.de - 73 + 10 + GameCanvas.dc, 46, 46, 0, 0)
        self.a_IIIIZ(GameCanvas.bZ.a // 2 + 60 - GameCanvas.db, GameCanvas.de - 72 + 109 + GameCanvas.dc, 46, 46, True)
        self.a_TIIIIII(GameCanvas.bB.a_I(38 + GameCanvas.cz.aB), GameCanvas.bZ.a // 2 + 60 - GameCanvas.db, GameCanvas.de - 73 + 110 + GameCanvas.dc, 46, 46, 0, 0)
        self.R_I(3)

    def R_I(self, paramInt):  # e.java:2167-2172  (empty speech boxes: 1 = top, 2 = bottom)
        if (paramInt & 0x1) != 0:
            self.a_IIIIZ(GameCanvas.dd - 60 + 15 + GameCanvas.db, GameCanvas.de - 73 + 7 + GameCanvas.dc, 150, 53, False)
        if (paramInt & 0x2) != 0:
            self.a_IIIIZ(GameCanvas.dd - 60 + -40 + GameCanvas.db, GameCanvas.de - 73 + 107 + GameCanvas.dc, 150, 53, False)

    @staticmethod
    def a_III(paramInt1, paramInt2, paramInt3):  # e.java:2216-2309  (type speech text fw[p1], max 3 lines)
        # paramInt3 == 0: one tick of typing (state kept in fA/fx/fy/fz/fB/fC); 1: redraw all
        if paramInt1 == 0:
            i3 = GameCanvas.dd - 60 + 15 + 2 + GameCanvas.db
            i4 = GameCanvas.de - 73 + 7 + 2 + GameCanvas.dc
        elif paramInt1 == 1:
            i3 = GameCanvas.dd - 60 + -40 + 2 + GameCanvas.db
            i4 = GameCanvas.de - 73 + 107 + 2 + GameCanvas.dc
        else:
            return False
        if (GameCanvas.ch == -6 or GameCanvas.ch == -5) and 0 == paramInt3:
            i1 = 1000                    # a key shows the whole text at once
        else:
            i1 = GameCanvas.fA[paramInt1]
        # decompiled `if (!(n = (p2 != i1) ? 0 : p2))`: n == 0 -> start over, else continue
        n = 0 if paramInt2 != i1 else paramInt2
        if n == 0:
            i = i3
            j_ = i4
            i2 = 0
            m = 0
            k = 0
        else:
            i = GameCanvas.fx[paramInt1]
            j_ = GameCanvas.fy[paramInt1]
            i2 = GameCanvas.fB[paramInt1]
            m = GameCanvas.fC[paramInt1]
            k = GameCanvas.fz[paramInt1]
        Gfx.a_Lg(GameCanvas.bu)
        while n <= i1 and n < len(GameCanvas.fw[paramInt1]):
            fw = GameCanvas.fw[paramInt1]
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
                if GameCanvas.ch != -999 and m == 2:
                    break
                i = i3
                k = i5
                if m == 0:
                    i2 = n
                elif m != 1 and m == 2:
                    # 3 lines are full: drop the first line and start drawing again
                    str_ = fw[i2:]
                    GameCanvas.fw[paramInt1] = str_
                    i1 -= i2
                    m = n = 0
                    j_ = i4
                    k = 0
                    continue
                m += 1
                j_ += 16
            if n == 0:
                GameCanvas.bb.R_I(paramInt1 + 1)
            if i == i3 and fw[n] == ' ':
                n += 1
            if len(fw) >= n + 1:
                Gfx.a_TIII(fw[n:n + 1], i, j_, 0)
            i += i5
            n += 1
        if 0 == paramInt3:
            GameCanvas.fA[paramInt1] = n
            GameCanvas.fx[paramInt1] = i
            GameCanvas.fy[paramInt1] = j_
            GameCanvas.fz[paramInt1] = k
            GameCanvas.fB[paramInt1] = i2
            GameCanvas.fC[paramInt1] = m
        return True

    def aU(self):  # e.java:2374-2394  (screen 29: difficulty Hard / Normal)
        arrayOfInt = [GameCanvas.dd - 80 + GameCanvas.db, GameCanvas.de - 60 + GameCanvas.dc]
        GameCanvas.ep = i16(GameCanvas.cM[1])
        for b in range(2):
            if GameCanvas.cM[1] == b:
                Gfx.a_Lg(GameCanvas.bw)
                bool_ = True
            else:
                Gfx.a_Lg(GameCanvas.bu)
                bool_ = False
            self.a_IIIIZ(arrayOfInt[0], arrayOfInt[1] + b * 25, 160, 20, bool_)
            self.b_TII(consts.aX[b], arrayOfInt[1] + 1 + b * 25 - 1, 15)
        Gfx.a_Lg(GameCanvas.bu)
        self.a_IIIIZ(arrayOfInt[0], GameCanvas.de + GameCanvas.dc, 160, 80, False)
        for b in range(3):
            self.b_TII(consts.aY[GameCanvas.cM[1]][b], GameCanvas.de + 10 + b * 20, 17)

    def e_I(self, paramInt):  # e.java:3465-3531  (item record -> cX / cY / cZ)
        arrayOfByte = bytearray(16)
        if paramInt < 100:
            return
        if paramInt < 300:
            if GameCanvas.cU is None:
                GameCanvas.cU = GameCanvas.v_I(47)
            cU = GameCanvas.cU
            i = 9 + (paramInt - 101) * 23
            b = 0
            while b < 15:
                arrayOfByte[b] = cU[i + b] & 0xFF
                if arrayOfByte[b] == 0:
                    break
                b += 1
            GameCanvas.cX.a = GameCanvas.a_ABII(arrayOfByte, 0, b)
            GameCanvas.cX.b = i8(cU[i + 15])
            GameCanvas.cX.c = i8(cU[i + 15 + 1])
            GameCanvas.cX.d = i8(cU[i + 15 + 2])
            GameCanvas.cX.e = i8(cU[i + 15 + 3])
            GameCanvas.cX.f = i8(cU[i + 22])
            if GameCanvas.bV != 2:
                GameCanvas.cU = None
                return
        elif paramInt < 500:
            if GameCanvas.cV is None:
                GameCanvas.cV = GameCanvas.v_I(51)
            cV = GameCanvas.cV
            i = 10 + (paramInt - 301) * 24
            b = 0
            while b < 15:
                arrayOfByte[b] = cV[i + b] & 0xFF
                if arrayOfByte[b] == 0:
                    break
                b += 1
            GameCanvas.cY.a = GameCanvas.a_ABII(arrayOfByte, 0, b)
            GameCanvas.cY.b = i8(cV[i + 15])
            GameCanvas.cY.c = GameCanvas.a_BB(cV[i + 16], cV[i + 17])
            GameCanvas.cY.d = i8(cV[i + 18])
            GameCanvas.cY.e = cV[i + 19] & 0xFF
            GameCanvas.cY.f = i8(cV[i + 20])
            GameCanvas.cY.g = i8(cV[i + 22])
            GameCanvas.cY.h = cV[i + 23] & 0xFF
            if GameCanvas.bV != 2:
                GameCanvas.cV = None
                return
        else:
            if GameCanvas.cW is None:
                GameCanvas.cW = GameCanvas.v_I(49)
            cW = GameCanvas.cW
            i = 9 + (paramInt - 501) * 27
            b = 0
            while b < 15:
                arrayOfByte[b] = cW[i + b] & 0xFF
                if arrayOfByte[b] == 0:
                    break
                b += 1
            GameCanvas.cZ.a = GameCanvas.a_ABII(arrayOfByte, 0, b)
            GameCanvas.cZ.b = i8(cW[i + 15])
            GameCanvas.cZ.c = GameCanvas.a_BB(cW[i + 16], cW[i + 17])
            GameCanvas.cZ.d = i8(cW[i + 18])
            GameCanvas.cZ.e = GameCanvas.a_BB(cW[i + 19], cW[i + 20])
            GameCanvas.cZ.f = i8(cW[i + 21])
            GameCanvas.cZ.g = cW[i + 26] & 0xFF
            if GameCanvas.bV != 2:
                GameCanvas.cW = None

    def T_I(self, paramInt):  # e.java:3533-3545  (stat cursor: 0 = erase, 1 = draw)
        if GameCanvas.cz.J > 0:
            if paramInt != 0:
                c = 255 if F11 else 1   # DECOMP-FIX F11: decompiled `true` (= 1) as a colour
            else:
                c = 0
            self.a_IIIIIII(GameCanvas.eM + 144, GameCanvas.eN + 97 + 20 * GameCanvas.cM[1] + 11, 14, 18, c, c, c)

    def p_v(self):  # e.java:3547-3560  (exp table of the hero level from edat 45)
        arrayOfByte = GameCanvas.v_I(45)
        j_ = 40
        if GameCanvas.cz.l > 190:
            j_ = 200 - GameCanvas.cz.l << 2
        k = j_ // 4
        arrayOfInt = [0] * k
        i = 4 * (GameCanvas.cz.l - 1) + 2
        for b in range(k):
            o = i + b * 4
            arrayOfInt[b] = i32((arrayOfByte[o + 3] & 0xFF) << 24 | (arrayOfByte[o + 2] & 0xFF) << 16
                                | (arrayOfByte[o + 1] & 0xFF) << 8 | arrayOfByte[o] & 0xFF)
        return arrayOfInt

    def bf_v(self):  # e.java:3283-3364  (Game Menu carousel, 4 animation frames per step)
        cM = GameCanvas.cM
        s = GameCanvas.cK
        if GameCanvas.ct[27] is None:
            self.F_v()
        dd = GameCanvas.dd
        arrayOfInt1 = [dd - 44 + 0] * 4
        arrayOfInt2 = [164, 180, 188, 166]
        arrayOfInt3 = [dd - 44 + 0] * 4
        arrayOfInt4 = [244, 230, 220, 244]
        arrayOfInt5 = [dd - 63 - 5 + 0] * 4
        arrayOfInt6 = [200, 232, 185, 204]
        i = dd - 60
        if GameCanvas.ck == 2:
            if GameCanvas.cL == 1:
                for arr in (arrayOfInt1, arrayOfInt2, arrayOfInt3, arrayOfInt4, arrayOfInt5, arrayOfInt6):
                    arr[1], arr[2] = arr[2], arr[1]
                GameCanvas.cK = i16(GameCanvas.cK + 1)
                if GameCanvas.cK == 3:
                    cM[1] = cM[1] + 1
                    if _inc_cmp(cM[1]) >= GameCanvas.cN - 1:
                        cM[2] = 0
                        cM[1] = 0
                    GameCanvas.I_v()
                elif GameCanvas.cK > 3:
                    GameCanvas.ck = 0
                    GameCanvas.cL = 0
                    GameCanvas.cK = 0
            elif GameCanvas.cL == -1:
                GameCanvas.cK = i16(GameCanvas.cK + 1)
                if GameCanvas.cK == 3:
                    cM[1] = cM[1] - 1
                    if _dec_cmp(cM[1]) < 0:
                        cM[1] = GameCanvas.cN - 1 - 1
                    GameCanvas.I_v()
                elif GameCanvas.cK > 3:
                    GameCanvas.ck = 0
                    GameCanvas.cL = 0
                    GameCanvas.cK = 0
        self.a_MIIIIII(GameCanvas.ct[7], 0, 0, GameCanvas.bZ.a, GameCanvas.bZ.b, 0, 0)
        self.b_TII(GameCanvas.fT[cM[0]], 2 - GameCanvas.dc, 0)
        if GameCanvas.gl is None or GameCanvas.gm != cM[1]:
            GameCanvas.gl = self.d_T(GameCanvas.bA.a_I(66 + cM[1]))
            GameCanvas.gm = cM[1]
        if GameCanvas.gl is not None:
            GameCanvas.a_IIIIMII(i, 60, 117, 90, GameCanvas.gl, 0, 0)
        GameCanvas.a_IIIIMII(arrayOfInt1[s], arrayOfInt2[s], 89, 20, GameCanvas.ct[27], 0, 0)
        GameCanvas.a_IIIIMII(arrayOfInt1[s] + 22, arrayOfInt2[s] + 5, 62, 11, GameCanvas.ct[29], 0,
                     11 * (4 if cM[1] == 0 else (cM[1] - 1)))
        GameCanvas.a_IIIIMII(arrayOfInt3[s], arrayOfInt4[s], 89, 20, GameCanvas.ct[27], 0, 0)
        GameCanvas.a_IIIIMII(arrayOfInt3[s] + 22, arrayOfInt4[s] + 5, 62, 11, GameCanvas.ct[29], 0,
                     11 * (0 if cM[1] == 4 else (cM[1] + 1)))
        GameCanvas.a_IIIIMII(arrayOfInt5[s], arrayOfInt6[s], 127, 29, GameCanvas.ct[26], 0, 0)
        GameCanvas.a_IIIIMII(arrayOfInt5[s] + 22 + 2, arrayOfInt6[s] + 5 + 1, 94, 18, GameCanvas.ct[28], 0, 18 * cM[1])
        if GameCanvas.ck != 2 and GameCanvas.cK == 0:
            GameCanvas.a_IIIIMII(dd - 5 + GameCanvas.db, arrayOfInt6[s] - 6 - 5 - GameCanvas.dr % 3 * 2, 16, 10, GameCanvas.ct[17], 20, 0)
            GameCanvas.a_IIIIMII(dd - 5 + GameCanvas.db, arrayOfInt6[s] + 29 + GameCanvas.dr % 3 * 2, 16, 10, GameCanvas.ct[17], 20, 10)
        if GameCanvas.dr > 100:
            GameCanvas.dr = 32
        else:
            GameCanvas.dr += 1
        GameCanvas.h_II(-1, 2)

    # ---- Missions: lords (1), missions (2), description (3), briefing (4) ------------------

    def aH(self):  # e.java:1229-1238  (mission description, 6 lines per page)
        self.a_IIIIZ(GameCanvas.dd - 100 + GameCanvas.db, GameCanvas.de - 80, 200, 40, False)
        self.b_TII(GameCanvas.dl, GameCanvas.de - 80, 30)
        self.b_TII(GameCanvas.dn, GameCanvas.de - 60, 30)
        self.a_IIIIZ(GameCanvas.dd - 110, GameCanvas.de - 30, 220, 119, False)
        for b in range(6):
            if GameCanvas.dq[0] >= GameCanvas.cM[2] * 6 + b:
                GameCanvas.a_IIT(GameCanvas.dd - 100 + GameCanvas.db, GameCanvas.de - 28 + b * 20 + GameCanvas.dc, GameCanvas.dp[0][GameCanvas.cM[2] * 6 + b])
        self.a_IIIZ(GameCanvas.cM[2] + 1, idiv(GameCanvas.dq[0], 6) + 1, GameCanvas.de + 110, True)

    def aI(self):  # e.java:1246-1250  (briefing: portraits + empty speech boxes)
        self.b_I(GameCanvas.dB[GameCanvas.dm])
        self.q_I(1)
        self.R_I(3)

    def h_v(self):  # e.java:1252-1264  (talk in the map: portrait bottom-left)
        if (GameCanvas.dK & 0x1) != 0:
            i = 0 + GameCanvas.dC.e
        else:
            i = 38 + GameCanvas.cz.aB
        j_ = GameCanvas.bY.b - 46 - 4
        self.a_IIIIZ(2 + GameCanvas.db, j_ + GameCanvas.dc, 48, 48, True)
        j_ += 1
        self.a_TIIIIII(GameCanvas.bB.a_I(i), 3 + GameCanvas.db, j_ + GameCanvas.dc, 46, 46, 0, 0)
        self.aT()
        self.q_I(1)

    def i_v(self):  # e.java:1266-1361  (dialogue typewriter: dG 0 briefing, 1 map talk, 2 general)
        arrayOfByte1 = [2, 3, 5]
        arrayOfByte2 = [2, 1, 1]
        if GameCanvas.bV == 5 and GameCanvas.ch != -6:
            GameCanvas.ch = -999
        Gfx.a_Lg(GameCanvas.bu)
        if GameCanvas.ch == -6:
            GameCanvas.dS = 1
            GameCanvas.dQ = i16(GameCanvas.dq[GameCanvas.dR])
            GameCanvas.dK = i16(arrayOfByte1[GameCanvas.dG])
        if GameCanvas.dS > 0:
            GameCanvas.dS = i16(GameCanvas.dS - 1)
            if GameCanvas.ch != -999:
                GameCanvas.dS = 0
            if GameCanvas.dS < 1:
                if GameCanvas.dQ >= GameCanvas.dq[GameCanvas.dR]:
                    if GameCanvas.dK >= arrayOfByte1[GameCanvas.dG]:
                        GameCanvas.ck = 1
                        if GameCanvas.dG != 0:
                            if GameCanvas.dG == 1:
                                GameCanvas.bV = 3
                                return
                            if GameCanvas.cr != 0:
                                self.w_I(2)
                                self.F_v()
                                GameCanvas.cM[0] = 0
                                GameCanvas.cN = consts.v[GameCanvas.cM[0]]
                                GameCanvas.dE = GameCanvas.fU
                                GameCanvas.bV = 2
                                GameCanvas.cL = 0
                                GameCanvas.cK = 0
                                GameCanvas.ck = 1
                                self.L_v()
                                return
                            GameCanvas.co = 1
                            GameCanvas.cn = 5
                            GameCanvas.bV = 3
                            return
                        self.y_v()
                        return
                    GameCanvas.dP = 0
                    GameCanvas.dQ = 0
                    if 0 == GameCanvas.dG:
                        GameCanvas.dR = i16(GameCanvas.dR + 1 & 0x1)
                    GameCanvas.ao()
                    self.z_I(GameCanvas.dI + GameCanvas.dK - 1)
                    if GameCanvas.dG != 0:
                        self.h_v()
                        return
                    self.aS()
                    return
                GameCanvas.dP = i16(GameCanvas.dP + 1)
                GameCanvas.dQ = i16(GameCanvas.dQ + 1)
                GameCanvas.dO = 0
                GameCanvas.dN = GameCanvas.dL[GameCanvas.dR]
                if GameCanvas.dP > arrayOfByte2[GameCanvas.dG]:
                    GameCanvas.dP = i16(arrayOfByte2[GameCanvas.dG])
                    for b in range(20):
                        if b < GameCanvas.dq[GameCanvas.dR]:
                            GameCanvas.dp[GameCanvas.dR][b] = GameCanvas.dp[GameCanvas.dR][b + 1]
                    if GameCanvas.dG != 0:
                        self.aT()
                        return
                    self.aS()
                    return
        else:
            if GameCanvas.ch == -5:
                GameCanvas.dQ = i16(GameCanvas.dQ + arrayOfByte2[GameCanvas.dG] - GameCanvas.dP)
                GameCanvas.dP = i16(arrayOfByte2[GameCanvas.dG])
                GameCanvas.dO = 29
                if GameCanvas.dG != 0:
                    self.aT()
                else:
                    self.aS()
                GameCanvas.dS = 3
                return
            line = GameCanvas.dp[GameCanvas.dR][GameCanvas.dP]
            str_ = line[GameCanvas.dO:]
            if len(str_) != 0 and ord(str_[0]) > 0:
                GameCanvas.dO = i16(GameCanvas.dO + 1)
                Gfx.a_TIII(str_[0:1], GameCanvas.dN + GameCanvas.db, GameCanvas.dM[GameCanvas.dR] + 16 * GameCanvas.dP + GameCanvas.dc, 0)
                GameCanvas.dN = i16(GameCanvas.dN + 9)
                return
            if GameCanvas.dQ >= GameCanvas.dq[GameCanvas.dR]:
                GameCanvas.dS = 15
                return
            GameCanvas.dS = 1

    def aS(self):  # e.java:2174-2205  (briefing: both speech boxes)
        Gfx.a_Lg(GameCanvas.bu)
        self.R_I(2 if GameCanvas.dR != 0 else 1)
        dp, dL, dM = GameCanvas.dp, GameCanvas.dL, GameCanvas.dM
        if GameCanvas.dR != 0:
            for b in range(3):
                GameCanvas.c_IIT(dL[0] + GameCanvas.db, dM[0] + 16 * b + GameCanvas.dc, dp[0][b])
        else:
            for b in range(GameCanvas.dP):
                if dp[0][b] is not None:
                    GameCanvas.c_IIT(dL[0] + GameCanvas.db, dM[0] + 16 * b + GameCanvas.dc, dp[0][b])
            if dp[0][GameCanvas.dP] is not None:
                str_ = dp[0][GameCanvas.dP][0:min(GameCanvas.dO, len(dp[0][GameCanvas.dP]))]
                GameCanvas.c_IIT(dL[0] + GameCanvas.db, dM[0] + 16 * GameCanvas.dP + GameCanvas.dc, str_)
        if GameCanvas.dK > 1:
            if GameCanvas.dR != 0:
                for b in range(GameCanvas.dP):
                    if dp[1][b] is not None:
                        GameCanvas.c_IIT(dL[1] + GameCanvas.db, dM[1] + 16 * b + GameCanvas.dc, dp[1][b])
                if dp[1][GameCanvas.dP] is not None:
                    str_ = dp[1][GameCanvas.dP][0:min(GameCanvas.dO, len(dp[1][GameCanvas.dP]))]
                    GameCanvas.c_IIT(dL[1] + GameCanvas.db, dM[1] + 16 * GameCanvas.dP + GameCanvas.dc, str_)
                    return
            else:
                for b in range(3):
                    GameCanvas.c_IIT(dL[1] + GameCanvas.db, dM[1] + 16 * b + GameCanvas.dc, dp[1][b])

    def aT(self):  # e.java:2207-2214  (map talk: one speech box at the bottom)
        self.a_IIIIZ(54 + GameCanvas.db, GameCanvas.bY.b - 40 + GameCanvas.dc, GameCanvas.bY.a - 56, 38, True)
        Gfx.a_Lg(GameCanvas.bu)
        for b in range(GameCanvas.dP):
            GameCanvas.c_IIT(GameCanvas.dL[0] + GameCanvas.db, GameCanvas.dM[0] + 16 * b + GameCanvas.dc, GameCanvas.dp[0][b])
        str_ = GameCanvas.dp[0][GameCanvas.dP][0:GameCanvas.dO]
        GameCanvas.c_IIT(GameCanvas.dL[0] + GameCanvas.db, GameCanvas.dM[0] + 16 * GameCanvas.dP + GameCanvas.dc, str_)

    def bi_v(self):  # e.java:3569-3603  (missions of lord dk -> dz / dA / dB, list dE = dA)
        i = 0
        GameCanvas.cg = GameCanvas.ds[GameCanvas.dk]
        GameCanvas.dl = GameCanvas.dt[GameCanvas.dk]
        arrayOfByte1 = GameCanvas.v_I(50)
        GameCanvas.cN = GameCanvas.dv[GameCanvas.dk]
        i = 11 * GameCanvas.du[GameCanvas.dk] + 11
        arrayOfByte2 = GameCanvas.v_I(55)
        for b in range(GameCanvas.cN):
            if GameCanvas.dz[b] is None:
                GameCanvas.dz[b] = Lord()
            dz = GameCanvas.dz[b]
            dz.a = GameCanvas.b_B(arrayOfByte1[i])
            dz.b = GameCanvas.b_B(arrayOfByte1[i + 1])
            dz.c = GameCanvas.b_B(arrayOfByte1[i + 2])
            dz.d = GameCanvas.b_B(arrayOfByte1[i + 3])
            dz.e = GameCanvas.b_B(arrayOfByte1[i + 4])
            dz.f = GameCanvas.b_B(arrayOfByte1[i + 5])
            dz.g = GameCanvas.b_B(arrayOfByte1[i + 6])
            dz.h = GameCanvas.b_B(arrayOfByte1[i + 7])
            dz.i = i16(arrayOfByte1[i + 8] & 0xFF | i8(arrayOfByte1[i + 9]) & 0xFF00)
            dz.j = GameCanvas.b_B(arrayOfByte1[i + 10])
            i += 11
            j_ = 3 + (dz.a - 1) * 15
            b1 = 14
            for b2 in range(14):
                if arrayOfByte2[j_ + b2] == 0:
                    b1 = b2
                    break
            GameCanvas.dA[b] = GameCanvas.a_ABII(arrayOfByte2, j_, j_ + b1)
            GameCanvas.dB[b] = i8(arrayOfByte2[17 + (dz.a - 1) * 15])
        GameCanvas.dE = GameCanvas.dA

    # ---- Visiting: generals (19 list, 20 talk) ---------------------------------------------

    def aN(self):  # e.java:1694-1748  (generals: Name / Points, 4 per page)
        arrayOfString = ["Name", "Points"]
        i = idiv(GameCanvas.bZ.a - 208, 2) + 2
        j_ = i + 134 + 10
        k = GameCanvas.bY.b - 20 - 20 + 10
        m = 20 + idiv(k - 177, 2) + 2
        n = m
        i1 = GameCanvas.cM[1] % 4
        i2 = GameCanvas.cM[1] // 4
        GameCanvas.fp[1] = i16(i2 + 1)
        i2 *= 4
        self.a_IIIIZ(i, n, 130, 22, False)
        self.a_IIIIZ(j_, n, 60, 22, False)
        Gfx.a_Lg(GameCanvas.bu)
        GameCanvas.b_IIT(i + 65, n + 1, arrayOfString[0])
        GameCanvas.b_IIT(j_ + 30, n + 1, arrayOfString[1])
        n += 31
        for b in range(4):
            if b == i1:
                bool_ = True
                Gfx.a_Lg(GameCanvas.bw)
            else:
                bool_ = False
                Gfx.a_Lg(GameCanvas.bu)
            self.a_IIIIZ(i, n, 130, 22, bool_)
            self.a_IIIIZ(j_, n, 60, 22, bool_)
            if i2 < GameCanvas.cN:
                if GameCanvas.fu != 0:
                    str_ = GameCanvas.fr.b_II(GameCanvas.fn[2][i2] - 1, 0)
                else:
                    str_ = GameCanvas.fr.b_II(GameCanvas.fn[0][i2] - 1, 0)
                GameCanvas.b_IIT(i + 65, n + 1, str_)
                if GameCanvas.fu != 0:
                    b1 = 0
                    while b1 < GameCanvas.fo and GameCanvas.fn[2][i2] != GameCanvas.fn[0][b1]:
                        b1 += 1
                    if b1 < GameCanvas.fo:
                        str_ = "" + str(GameCanvas.fn[1][b1])
                    else:
                        str_ = "0"
                else:
                    str_ = "" + str(GameCanvas.fn[1][i2])
                GameCanvas.b_IIT(j_ + 30, n + 1, str_)
            i2 += 1
            n += 31
        n += 6
        self.a_IIIZ(GameCanvas.fp[1], GameCanvas.fp[0], n, True)

    def aO(self):  # e.java:1750-1802  (general talk: type the lines gf[], then popups 14 / 16)
        if GameCanvas.dS > 0:
            GameCanvas.dS = i16(GameCanvas.dS - 1)
            if GameCanvas.ch != 0 and GameCanvas.dS > 3:
                GameCanvas.dS = 3
            if 0 == GameCanvas.dS:
                GameCanvas.fD += 1
                if GameCanvas.fD <= 3:
                    GameCanvas.fw[GameCanvas.fD & 0x1] = GameCanvas.gf[GameCanvas.fD - 1]
                    GameCanvas.fA[GameCanvas.fD & 0x1] = 0
                    return
                if GameCanvas.fD == 4:
                    GameCanvas.cS.e_I(14)
                    GameCanvas.fA[1] = 0
                    return
                if GameCanvas.fD < 7:
                    GameCanvas.fw[GameCanvas.fD & 0x1] = GameCanvas.gf[GameCanvas.fD - 2]
                    GameCanvas.fA[GameCanvas.fD & 0x1] = 0
                    return
                GameCanvas.fs.a_v()
                GameCanvas.fs = None
                GameCanvas.fr.a_v()
                GameCanvas.fr = None
                GameCanvas.cS.e_I(16)
                return
        else:
            if GameCanvas.fD >= 10:
                GameCanvas.fD -= 10
                i = GameCanvas.fD & 0x1
                GameCanvas.fA[i] = len(GameCanvas.fw[i])
                j_ = 0
            else:
                i = GameCanvas.fD & 0x1
                j_ = GameCanvas.fA[i]
            if GameCanvas.fD != 4:
                Menus.a_III(i, j_, 0)
                if len(GameCanvas.fw[i]) <= GameCanvas.fA[i] + 1:
                    if GameCanvas.ch != 0:
                        GameCanvas.dS = 5
                        return
                    GameCanvas.dS = 15

    def bg_v(self):  # e.java:3366-3393  (open the talk with general cM[1])
        # the decompiler shows `j = 2;` as a field write; it is the local j declared below
        if GameCanvas.fu != 0:
            j_ = 2
            b = 0
            while b < GameCanvas.fo and GameCanvas.fn[0][b] != GameCanvas.fn[2][GameCanvas.cM[1]]:
                b += 1
            GameCanvas.fH = i16(b)
            GameCanvas.fv = i16(GameCanvas.cM[1])
        else:
            j_ = 0
            GameCanvas.fH = i16(GameCanvas.cM[1])
        i = GameCanvas.fn[j_][GameCanvas.cM[1]] - 1
        self.B_I(GameCanvas.fn[j_][GameCanvas.cM[1]])
        GameCanvas.ft = GameCanvas.fr.b_II(i, 0)
        j_ = GameCanvas.fr.a_II(i, 9)
        k = GameCanvas.fr.a_II(i, 8)
        i = GameCanvas.fn[1][GameCanvas.fH]
        GameCanvas.fE = k
        GameCanvas.fF = j_
        if Menus.a_II(i, j_):
            GameCanvas.fw[0] = ""
            GameCanvas.fw[1] = GameCanvas.gf[0]
            GameCanvas.fA[1] = 0
            GameCanvas.fA[0] = 0
            GameCanvas.fD = 1
            return True
        return False

    @staticmethod
    def a_II(paramInt1, paramInt2):  # e.java:3395-3430  (greeting lines of the general -> gf[])
        if GameCanvas.fs is not None:
            GameCanvas.fs.a_v()
            GameCanvas.fs = None
        GameCanvas.fs = ScrTable("/" + GameCanvas.bE.a_I(62))
        if 0 <= paramInt1 <= 100 and GameCanvas.fs is not None:
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
                if len(GameCanvas.fs.a_I(paramInt1)) > 0:
                    str_ = GameCanvas.ft if (b3 & 0x1) != 0 else GameCanvas.cz.k
                    GameCanvas.gf[b3 + b2] = "[" + str_ + "] " + GameCanvas.fs.a_I(paramInt1) + " "
                    paramInt1 += 1
                else:
                    return False
            return True
        return False

    @staticmethod
    def b_II(paramInt1, paramInt2):  # e.java:3432-3463  (add paramInt2 friendship to general paramInt1)
        b = 0
        while b < GameCanvas.fo and GameCanvas.fn[0][b] != paramInt1:
            b += 1
        if b == GameCanvas.fo:
            if paramInt2 > 0:
                d_ = ArrTable("/" + GameCanvas.bE.a_I(52))
                for b1 in range(44):
                    i = d_.a_II(b1, 0)
                    if i == paramInt1:
                        GameCanvas.fn[0][b] = i16(paramInt1)
                        GameCanvas.fo = i16(GameCanvas.fo + 1)
                        GameCanvas.fn[1][b] = i16(GameCanvas.fn[1][b] + paramInt2)
                        break
        else:
            GameCanvas.fn[1][b] = i16(GameCanvas.fn[1][b] + paramInt2)
            if GameCanvas.fn[1][b] > 200 or 0 == GameCanvas.fn[1][b]:
                while b < GameCanvas.fo:
                    GameCanvas.fn[0][b] = GameCanvas.fn[0][b + 1]
                    GameCanvas.fn[1][b] = GameCanvas.fn[1][b + 1]
                    b += 1
                GameCanvas.fo = i16(GameCanvas.fo - 1)
            elif GameCanvas.fn[1][b] >= 100:
                GameCanvas.fn[1][b] = 100
                return 1
        return 0

    def o_v(self):  # e.java:3208-3281  (gift of the general after the talk -> fJ, cT[0])
        arrayOfShort = [[[500, 800, 900, 960, 990, 995, 998], [60, 61, 91, 92, 392, 892, 992],
                         [100, 600, 900, 930, 990, 995, 996], [1, 2, 5, 305, 310, 410, 910]],
                        [[1, 101, 106, 606, 609, 610, 910], [30, 31, 91, 92, 592, 892, 992],
                         [300, 360, 860, 960, 961, 991, 996], [1, 2, 5, 10, 40, 100, 200]]]
        cz = GameCanvas.cz
        if self.C_I(100) < GameCanvas.fn[1][GameCanvas.fH]:
            i = self.C_I(1000)
            GameCanvas.fJ = 0
            while GameCanvas.fJ < 7 and i >= arrayOfShort[GameCanvas.dC.f][GameCanvas.fI][GameCanvas.fJ]:
                GameCanvas.fJ = i16(GameCanvas.fJ + 1)
            GameCanvas.cS.l[4] = ""
            v = GameCanvas.fJ
            if v == 0:
                i = self.p_I(0)
                if cz.W[i - 1] < 10:
                    str_ = GameCanvas.e_II(54, i - 1)
                    cz.W[i - 1] = cz.W[i - 1] + 1
                    if cz.W[i - 1] == 1:
                        GameCanvas.cS.l[4] = "Skill :"
                        GameCanvas.cT[0] = str_
                        return
                    GameCanvas.cS.l[4] = "Skill up :"
                    GameCanvas.cT[0] = str_
                    return
            elif v == 1:
                if cz.m < 10000:
                    cz.m += 1
                    GameCanvas.cT[0] = consts.aR[0]
                    return
            elif v == 2:
                if cz.n < 10000:
                    cz.n += 1
                    GameCanvas.cT[0] = consts.aR[1]
                    return
            elif v == 3:
                if cz.o < 25000:
                    cz.o += 5
                    GameCanvas.cT[0] = consts.aR[2]
                    return
            elif v == 4:
                if cz.q < 20000:
                    cz.q += 3
                    GameCanvas.cT[0] = consts.aR[3]
                    return
            elif v == 5:
                cz.F += 10
                GameCanvas.cT[0] = consts.aR[4]
                return
            elif v == 6:
                if self.k_II(GameCanvas.bc.P_I(4), 1) != 0:
                    GameCanvas.cT[0] = GameCanvas.cX.a
                    GameCanvas.cS.l[4] = "Item Acquired!"
                    return
            else:
                i = self.C_I(11)
                if self.k_II(i + 1, 1) != 0:
                    GameCanvas.cT[0] = consts.aN[i]
                    GameCanvas.cS.l[4] = "Item Acquired!"
                    return
        GameCanvas.fJ = 8

    @staticmethod
    def seal_list():
        """ORIG-BUG B3: the list of "all General Visiting" of 504 Emperor's Seal (fn[2], drawn
        by e.java:1725 and visited by bg() 3366-3378) is never filled in the original, so the
        Visiting screen showed 44 empty rows; the 44 generals one can visit are visitgen.arr."""
        vg = ArrTable("/visitgen.arr")
        for b in range(44):
            GameCanvas.fn[2][b] = i16(vg.a_II(b, 0))

    @staticmethod
    def bh_v():  # e.java:3562-3567
        GameCanvas.fp[0] = i16(idiv(GameCanvas.cN - 1, 4) + 1)
        if GameCanvas.fr is None:
            GameCanvas.fr = ArrTable("/" + GameCanvas.bE.a_I(46))
        return False

    def n_v(self):  # e.java:2938-2972  (popup extras on the map: experience bars of popups 11 / 12)
        i = 0
        if GameCanvas.cS.b_ == 11:
            i = self.p_II(GameCanvas.ea, 0)
            if 0 == i and 0 == GameCanvas.cS.e:
                GameCanvas.ea = i16(GameCanvas.ea + 1)
        elif GameCanvas.cS.b_ == 12:
            i = self.p_II(GameCanvas.ea, 1)
            if 0 == i and 0 == GameCanvas.cS.e:
                GameCanvas.ea = i16(GameCanvas.ea + 1)
        if i != 0 and 0 == GameCanvas.cS.e:
            if i == 1:  # the bar is full: level up
                GameCanvas.dZ[0] = 0
                GameCanvas.dZ[1] = i16(GameCanvas.dZ[1] - 100)
                if GameCanvas.dZ[1] < 0:
                    GameCanvas.dZ[1] = 0
                GameCanvas.dZ[2] = i16(GameCanvas.dZ[2] - 100)
                GameCanvas.ea = 0
                GameCanvas.cS.e = 1
                GameCanvas.cS.f = 20
                GameCanvas.cS.g = 12
                GameCanvas.cz.l += 1
                GameCanvas.cz.J += 3
                GameCanvas.cT[0] = "Level Up : Lv " + str(GameCanvas.cz.l)
                GameCanvas.cS.l[5] = GameCanvas.cT[0]
                GameCanvas.cS.j = 1
                return
            if GameCanvas.cS.d > 100:
                GameCanvas.cS.d = 16

    def p_II(self, paramInt1, paramInt2):  # e.java:2974-3017  (experience bar; 1 = full, 2 = done)
        arrayOfInt = [[GameCanvas.k_III(115, 142, 140), GameCanvas.k_III(181, 178, 181), 16777215],
                      [GameCanvas.k_III(99, 0, 0), GameCanvas.k_III(181, 0, 0), GameCanvas.k_III(247, 73, 0)],
                      [GameCanvas.k_III(0, 65, 255), GameCanvas.k_III(0, 146, 255), GameCanvas.k_III(0, 255, 173)],
                      [GameCanvas.k_III(247, 73, 0), GameCanvas.k_III(255, 162, 0), GameCanvas.k_III(255, 223, 0)]]
        if GameCanvas.bV == 3:
            GameCanvas.dc = i16(GameCanvas.dc - 30)
        y = GameCanvas.de + 37 + GameCanvas.dc + 20
        arrayOfAc = [Rect(GameCanvas.dd - 51, y, 102, 7),
                     Rect(GameCanvas.dd - 50, y, GameCanvas.dZ[0], 7),
                     Rect(GameCanvas.dd - 50 + GameCanvas.dZ[0], y, GameCanvas.dZ[1] - GameCanvas.dZ[0], 7),
                     Rect(GameCanvas.dd - 50 + GameCanvas.dZ[1], y, 0, 7)]
        if GameCanvas.bV == 3:
            GameCanvas.dc = i16(GameCanvas.dc + 30)
        b3 = 0
        b2 = 4 if paramInt2 != 0 else 3
        if GameCanvas.dZ[paramInt2] + paramInt1 * 4 > GameCanvas.dZ[paramInt2 + 1]:
            i = GameCanvas.dZ[paramInt2 + 1] - GameCanvas.dZ[paramInt2]
            b3 = 2
        else:
            i = paramInt1 * 4
        if GameCanvas.dZ[paramInt2] + i > 100:
            arrayOfAc[paramInt2 + 2].c = 100 - GameCanvas.dZ[paramInt2]
            b3 = 1
        else:
            arrayOfAc[paramInt2 + 2].c = i
        GameCanvas.a_LacI(arrayOfAc[0], 0)
        arrayOfAc[0].a += 1
        arrayOfAc[0].c = 100
        for b1 in range(b2):
            if arrayOfAc[b1].c > 0:
                for b in range(3):
                    arrayOfAc[b1].b += 1
                    arrayOfAc[b1].d -= 2
                    GameCanvas.a_LacI(arrayOfAc[b1], arrayOfInt[b1][b])
        return b3
