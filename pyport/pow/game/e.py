"""e.java - menu screens (bb). Literal port, Phase 0 subset:
Main Menu (cM[0] == 5) and the Game Menu carousel (cM[0] == 0), with the full key routing
(a(), aB/aC/aD/aE = up/down/left/right, b() = fire, aF() = back).
Screens of later phases raise NotPorted.
"""
import config
from pow.game import ae
from pow.game.ag import ag, not_ported
from pow.game.at import at
from pow.game.j import j
from pow.game.structs import ac, z
from pow.game.x import x
from pow.midp.jint import i8, i16, i32, idiv, imod

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
    cz = ag.cz
    if cz.Z[ag.cM[1]].a != 0 and cz.aa[paramInt] != ag.cM[1]:
        if ag.cM[1] == cz.aa[paramInt + 1 & 0x1]:
            i = cz.aa[paramInt]
            cz.aa[paramInt] = cz.aa[paramInt + 1 & 0x1]
            cz.aa[paramInt + 1 & 0x1] = i
        else:
            cz.aa[paramInt] = i8(ag.cM[1])
        return 1
    return 0


class e(ag):
    a = None  # public static byte[] a;   e.java:4

    def __init__(self):  # e.java:6-8
        super().__init__(ag.bs)

    def a_I(self, paramInt):  # e.java:10-205  (draw the current menu; 1 = first frame, 2 = animation)
        cM = ag.cM
        if paramInt == 1:
            if cM[0] != 5:
                x.a_Lg(ag.bu)
                if ag.bW == 3:
                    x.b_IIIII(7, 19, 225, 242, 0)
                else:
                    self.e_v()
                if cM[0] != 28:
                    if ag.bW == 3:
                        x.a_Lg(ag.bu)
                        self.b_TII(ag.fT[cM[0]], 15, 0)
                    else:
                        self.b_TII(ag.fT[cM[0]], 2 - ag.dc, 0)
                else:
                    str_ = ag.b_TI(ag.ga[0], ag.ej)
                    if ag.bW == 3:
                        x.a_Lg(ag.bu)
                        self.b_TII(str_, 15, 0)
                    else:
                        self.b_TII(str_, 2 - ag.dc, 0)
                if ae.u[cM[0]] != -1 or (ae.u[cM[0]] == -1 and cM[0] == 15):
                    if cM[0] == 3:
                        ag.h_II(11, 2)
                    else:
                        ag.h_II(-1, 2)
            v = cM[0]
            if v == 0:
                ag.cL = 0
                ag.cK = 0
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
                ag.h_II(5, -1)
            elif v == 17:
                self.Q_I(0)
                self.k_v()
                ag.h_II(5, -1)
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
                self.b_I(ag.fE)
                if ag.fA[0] > 0:
                    e.a_III(ag.fD + 1 & 0x1, 0, 1)
                if ag.fA[1] > 0:
                    e.a_III(ag.fD & 0x1, 0, 1)
            if ag.cS.b != 0:
                ag.cS.c_v()
                return
        else:
            if paramInt == 2:
                v = cM[0]
                if v == 0:
                    self.bf_v()
                    return
                if v == 4:
                    x.a_Lg(ag.bu)
                    self.e_v()
                    self.aI()
                    ag.ch = -5
                    ag.dS = 0
                    self.i_v()
                    ag.ck -= 1
                return
            if ag.cS.b != 0:
                if ag.cS.j != 0:
                    ag.cS.c_v()
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
                    ag.f_II(ag.bP, ag.de + 32 + ag.dc)
                    return
                if v in (8, 14):
                    if ag.da != 0:
                        self.O_I(0)
                        return
                    return
                if v == 15:
                    if ag.da != 0:
                        self.P_I(ag.da)
                    self.k_v()
                    return
                if v == 16:
                    self.k_v()
                    return
                if v == 17:
                    if ag.da != 0:
                        self.Q_I(1)
                    self.k_v()
                    return
                if v == 18:
                    if ag.da != 0:
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
        if ag.bj:
            ag.ed = -1
        v = ag.cM[0]
        if v == 4:
            return
        if v == 7:
            i = ag.r_I(ag.ch)
            if i == -7:
                if len(ag.bz.a_v()) == 0:
                    ag.cM[0] = 6
                    ag.ck = 1
                    return
                ag.bz.a_I(-8)
                return
            if i == -5 or i == 53:
                if ag.bP == 26:
                    if len(ag.bz.a_v()) != 0:
                        ag.cz.k = ag.bz.a_v()
                        ag.bz.a_T(ag.cz.k)
                        ag.cM[0] = 8
                        ag.O_v()
                        ag.cN = 4
                        ag.aw()
                        return
                else:
                    if len(ag.bz.a_v()) == 0:
                        b = 65
                    else:
                        b = 97
                    ag.bz.a_I(b + ag.bP)
                    return
            return
        if v == 20:
            if ag.ch != -5:
                ag.ch = -999
                return
            return
        if v in (21, 22, 23, 24):
            self.aW()
            return
        ch = ag.ch
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
            if ag.cM[0] == 18:
                ag.ck = ar_c(0)
                return
        elif ch == 35:
            if ag.cM[0] == 18:
                ag.ck = ar_c(1)
                return
        elif ch in (-5, 53):
            self.b_v()
            return
        elif ch == -6:
            if ag.cM[0] == 16 or ag.cM[0] == 17 or ag.cM[0] == 3:
                self.b_v()
                return
        elif ch == -7:
            self.aF()

    @staticmethod
    def m_II(paramInt1, paramInt2):  # e.java:304-307
        return ae.aW[paramInt1][paramInt2]

    def aB(self):  # e.java:309-392  (UP)
        cM = ag.cM
        v = cM[0]
        if v == 0:
            if ag.cL == 0:
                ag.ck = 2
                ag.cL = -1
            return
        if v in (3, 5, 6, 18, 20, 28):
            return
        if v in (8, 14):
            self.T_I(0)
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 0:
                cM[1] = ag.cN - 1
            self.T_I(1)
            return
        if v == 9:
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 1:
                cM[1] = ag.cN - 1
            if not ag.df and cM[1] == 1:
                cM[1] = 0
            ag.I_v()
            ag.ck = 1
            return
        if v == 15:
            if cM[3] == 2:
                if cM[1] < 4:
                    cM[2] = cM[2] - 3
                    if cM[2] < 0:
                        cM[2] = cM[2] + 18
                    ag.da = 3
                ag.da = 3
                return
            return
        if v == 16:
            cM[2] = cM[2] + 1
            if _inc_cmp(cM[2]) >= ag.cN:
                cM[2] = 0
            ag.ck = 1
            return
        if v == 17:
            cM[2] = cM[2] - 5
            if cM[2] < 0:
                cM[2] = cM[2] + 25
            ag.da = 1
            return
        if v == 19:
            if cM[1] > 0:
                cM[1] = cM[1] - 1
                ag.ck = 1
                return
            return
        if v == 29:
            cM[1] = 1 - cM[1]
            ag.ck = 1
            return
        if v == 25:
            if cM[1] == 20:
                cM[1] = 23
            else:
                cM[1] = cM[1] - 1
            if cM[1] < cM[2]:
                cM[1] = cM[2] + 4
            ag.ck = 1
            return
        cM[1] = cM[1] - 1
        if _dec_cmp(cM[1]) < 0:
            cM[1] = ag.cN - 1
        ag.I_v()
        ag.ck = 1

    def aC(self):  # e.java:394-480  (DOWN)
        cM = ag.cM
        v = cM[0]
        if v == 0:
            if ag.cL == 0:
                ag.cL = 1
                ag.ck = 2
            return
        if v in (3, 5, 6, 18, 20, 28):
            return
        if v in (8, 14):
            self.T_I(0)
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= ag.cN:
                cM[1] = 0
            self.T_I(1)
            return
        if v == 9:
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= ag.cN:
                cM[2] = 0
                cM[1] = 0
            if not ag.df and cM[1] == 1:
                cM[1] = 2
            ag.I_v()
            ag.ck = 1
            return
        if v == 15:
            if cM[3] == 2:
                if cM[1] < 4:
                    cM[2] = cM[2] + 3
                    if cM[2] > 17:
                        cM[2] = cM[2] - 18
                ag.da = 3
                return
            return
        if v == 16:
            cM[2] = cM[2] - 1
            if _dec_cmp(cM[2]) < 0:
                cM[2] = ag.cN - 1
            ag.ck = 1
            return
        if v == 17:
            cM[2] = cM[2] + 5
            if cM[2] > 24:
                cM[2] = cM[2] - 25
            ag.da = 1
            return
        if v == 19:
            if cM[1] < ag.cN - 1:
                cM[1] = cM[1] + 1
                ag.ck = 1
                return
            return
        if v == 29:
            cM[1] = 1 - cM[1]
            ag.ck = 1
            return
        if v == 25:
            if cM[1] == 23:
                cM[1] = 20
            else:
                cM[1] = cM[1] + 1
            if cM[1] > cM[2] + 4:
                cM[1] = cM[2]
            ag.ck = 1
            return
        cM[1] = cM[1] + 1
        if _inc_cmp(cM[1]) >= ag.cN:
            cM[2] = 0
            cM[1] = 0
        ag.I_v()
        ag.ck = 1

    def aD(self):  # e.java:482-584  (LEFT)
        cM = ag.cM
        v = cM[0]
        if v == 1:
            if ag.bj and ag.cq > 0:
                ag.cq = i8(ag.cq - 1)
                self.C_v()
                ag.ck = 1
            return
        if v == 3:
            if cM[2] > 0:
                cM[2] = cM[2] - 1
            else:
                cM[2] = ag.dq[0] // 6
            ag.ck = 1
            return
        if v == 28:
            if cM[1] <= 0 and ag.ej == 8:
                cM[1] = 1
                ag.ck = 1
                return
            ag.ck = 1
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 0:
                cM[1] = ae.z[ag.ej + 1] - ae.z[ag.ej] - 1
                return
            return
        if v == 5:
            ag.ck = 1
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 0:
                cM[1] = 8
                return
            return
        if v == 18:
            ag.da = 1
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 0:
                cM[1] = ag.cN - 1
                return
            return
        if v == 6:
            ag.cz.aB = ag.cz.aB - 1 & 0x3
            ag.ck = 1
            return
        if v == 9:
            self.y_I(0)
            ag.ck = 1
            return
        if v == 15:
            c3 = cM[3]
            cM[c3] = cM[c3] - 1
            if cM[3] == 1:
                if cM[c3] < 0:
                    cM[c3] = 4
                ag.da = 2
                return
            if cM[1] < 4:
                if cM[c3] < 0:
                    cM[c3] = 17
            elif cM[c3] < 18:
                cM[c3] = 20
            ag.da = 3
            return
        if v == 16:
            ag.ck = 1
            cM[2] = cM[2] + 1
            if _inc_cmp(cM[2]) >= ag.cN:
                cM[2] = 0
                return
            return
        if v == 17:
            cM[2] = cM[2] - 1
            if _dec_cmp(cM[2]) < 0:
                cM[2] = ag.cN - 1
            ag.da = 1
            return
        if v == 19:
            cM[1] = cM[1] - 4
            if cM[1] < 0:
                cM[1] = 0
            ag.ck = 1
            return
        if v == 25:
            cM[2] = cM[2] - 5
            cM[1] = cM[1] - 5
            if cM[2] < 0:
                cM[2] = 20
                cM[1] = 20 + imod(cM[1] + 20, 5)
            ag.ck = 1

    def aE(self):  # e.java:586-686  (RIGHT)
        cM = ag.cM
        v = cM[0]
        if v == 1:
            if ag.bj and ag.cq < 44:
                ag.cq = i8(ag.cq + 1)
                self.C_v()
                ag.ck = 1
            return
        if v == 3:
            if (cM[2] + 1) * 6 - 1 < ag.dq[0]:
                cM[2] = cM[2] + 1
            else:
                cM[2] = 0
            ag.ck = 1
            return
        if v == 28:
            if cM[1] >= 1 and ag.ej == 8:
                ag.ck = 1
                cM[1] = 0
                return
            ag.ck = 1
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= ae.z[ag.ej + 1] - ae.z[ag.ej]:
                cM[1] = 0
                return
            return
        if v == 5:
            ag.ck = 1
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= 9:
                cM[1] = 0
                return
            return
        if v == 18:
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= ag.cN:
                cM[1] = 0
            ag.da = 1
            return
        if v == 6:
            ag.cz.aB = ag.cz.aB + 1 & 0x3
            ag.ck = 1
            return
        if v == 9:
            self.y_I(1)
            ag.ck = 1
            return
        if v == 15:
            c3 = cM[3]
            cM[c3] = cM[c3] + 1
            if cM[3] == 1:
                if cM[c3] > 4:
                    cM[c3] = 0
                ag.da = 2
                return
            if cM[1] < 4:
                if cM[c3] > 17:
                    cM[c3] = 0
            elif cM[c3] > 20:
                cM[c3] = 18
            ag.da = 3
            return
        if v == 16:
            ag.ck = 1
            cM[2] = cM[2] - 1
            if _dec_cmp(cM[2]) < 0:
                cM[2] = ag.cN - 1
                return
            return
        if v == 17:
            cM[2] = cM[2] + 1
            if _inc_cmp(cM[2]) >= ag.cN:
                cM[2] = 0
            ag.da = 1
            return
        if v == 19:
            cM[1] = cM[1] + 4
            if cM[1] >= ag.cN:
                cM[1] = ag.cN - 1
            ag.ck = 1
            return
        if v == 25:
            cM[2] = cM[2] + 5
            cM[1] = cM[1] + 5
            if cM[2] > 20:
                cM[2] = 0
                cM[1] = imod(cM[1], 5)
            ag.ck = 1

    def b_v(self):  # e.java:688-1000  (FIRE)
        cM = ag.cM
        if cM[0] == 9:
            self.y_I(1)
            ag.ck = 1
            return
        if cM[0] == 5:
            v = cM[1]
            if v == 4:
                ag.ej = 0
            elif v == 5:
                ag.ck = 1
                ag.cO = cM[0]
                cM[0] = 28
                cM[1] = 0
                cM[2] = 0
                ag.dE = ag.ga
                ag.ei = i16(ag.cO)
                ag.ej = 8
                return
            elif v == 6:
                ag.cS.e_I(41)
                return
            elif v == 7:
                ag.cS.e_I(42)
                return
            elif v == 8:
                ag.cS.e_I(28)
                ag.ck = 1
                return
            arrayOfInt = [0, 1, 3, 4, 5]
            cM[1] = arrayOfInt[cM[1]]
        if e.m_II(cM[0], cM[1] % 7) > -1:
            self.c_v()
            ag.cN = ae.v[cM[0]]
            c0 = cM[0]
            if c0 == 7:
                ag.cz.k = ""
            elif c0 == 9:
                ag.ai()
            elif c0 == 10:
                ag.dE = ag.fW
            elif c0 == 12:
                ag.dE = ag.fX
            elif c0 == 13:
                ag.dE = ag.fY
            elif c0 == 27:
                ag.dE = ag.ga
                ag.ei = i16(ag.cO)
            elif c0 == 28:
                ag.ej = i16(cM[1])
                ag.cN = ae.z[ag.ej + 1] - ae.z[ag.ej]
            elif c0 == 14:
                ag.O_v()
            elif c0 == 15:
                cM[3] = 1
                ag.ct[37] = self.d_T(ag.bA.a_I(44))
                ag.ct[38] = self.d_T(ag.bA.a_I(45))
            elif c0 == 17:
                cz = ag.cz
                if ag.cO == 16 and cz.X[cM[2]].a != 0:
                    for b in range(25):
                        if 0 == cz.Y[b].a:
                            self.a_LzLz(cz.X[cM[2]], cz.Y[b])
                self.ag()
            elif c0 in (21, 22, 23, 24):
                self.aY()
            elif c0 == 1:
                e.aG()
                self.C_v()
            elif c0 == 3:
                ag.dm = i16(cM[1])
                self.D_v()
            elif c0 == 20:
                self.bg_v()
            cM[2] = 0
            cM[1] = 0
            return
        v = cM[0]
        if v == 0:
            if cM[1] == 3:
                if ag.fo == 0:
                    ag.cS.e_I(35)
                    return
                if ag.cz.S != 0 and ag.fo != 0:
                    self.c_v()
                    cM[0] = 19
                    ag.fu = i16(ag.L_I(504))
                    if ag.fu != 0:
                        ag.cN = 44
                    else:
                        ag.cN = ag.fo
                    e.bh_v()
                    cM[2] = 0
                    cM[1] = 0
                    return
                ag.cS.e_I(35)
                ag.ck = 0
                ag.cL = 0
                ag.cK = 0
                return
            if cM[1] == 2:
                ag.be.g()
                ag.ck = 0
                ag.cL = 0
                ag.cK = 0
                return
        elif v == 5:
            ag.ck = 1
            if cM[1] == 0:
                if ag.aq():
                    self.U_v()
                    if ag.fS != 0:
                        return
                    ag.ai()
                    self.F_v()
                    self.c_v()
                    ag.cK = 0
                    ag.cL = 0
                    cM[0] = 0
                    ag.cN = ae.v[cM[0]]
                    ag.dE = ag.fU
                    cM[2] = 0
                    cM[1] = 0
                    self.aA()
                    if ag.dj != 0:  # e.java:856-866  (the save was made on the map: back into it)
                        self.C_v()
                        self.bi_v()
                        self.D_v()
                        self.y_v()
                        self.U_v()
                        ag.dW[1] = ag.B_v()
                        ag.dW[0] = ag.B_v()
                        ag.dV = ag.dW[0] - ag.dV
                        self.a__I(-1)
                        return
                return
            if cM[1] == 1:
                ag.bz = None
                ag.bz = at("", 8, 10)
                if ag.aq():
                    ag.cS.e_I(3)
                    return
                self.au()
                return
        elif v in (8, 14):
            if ag.cz.J > 0:
                ag.da = 1
                ag.cz.J -= 1
                if cM[1] == 0:
                    ag.cz.o += 5
                elif cM[1] == 1:
                    ag.cz.q += 3
                elif cM[1] == 2:
                    ag.cz.m += 1
                elif cM[1] == 3:
                    ag.cz.n += 1
                if cM[0] == 8 and ag.cz.J == 0:
                    ag.cS.e_I(4)
                    ag.ck = 1
                    return
        elif v == 29:
            ag.cS.e_I(36)
        elif v == 10:
            if cM[1] == 2:
                ag.cS.e_I(5)
                return
        elif v == 11:
            if cM[1] == 0:
                if self.ar() != 0:
                    ag.cS.e_I(0)
            return
        elif v == 25:
            if (ag.ed & 1 << cM[1]) != 0:
                self.c_v()
                self.l_II(cM[1], 0)
                return
            ag.cS.a_T("3You must first complete|the missions needed|to view this ending.")
            return
        elif v == 15:
            cz = ag.cz
            if cM[3] == 1:
                if cz.V[cM[1]] != 0:
                    cM[2] = ae.aD[cz.V[cM[1]] - 12]
                    cz.V[cM[1]] = 0
                elif cM[1] < 4:
                    cM[2] = 0
                else:
                    cM[2] = 18
                cM[3] = 2
                if cM[2] < 18:
                    ag.da = 6
                    return
                ag.ck = 1
                return
            if ae.aC[cM[2]] != 0:
                if cz.W[ae.aC[cM[2]] - 12] != 0:
                    cz.V[cM[1]] = ae.aC[cM[2]]
                    cM[3] = 1
                ag.da = 6
                return
        elif v == 17:
            cz = ag.cz
            it = cz.Y[cM[2]]
            if it.a != 0:
                b = ag.g_I(it.a)
                if ag.m_I(it.a) <= cz.l:
                    if it.a == 434:
                        it.a = 0
                        cz.o += 5
                        ag.cS.e_I(23)
                    elif it.a == 435:
                        it.a = 0
                        cz.q += 3
                        ag.cS.e_I(24)
                    elif it.a == 436:
                        it.a = 0
                        cz.n += 1
                        ag.cS.e_I(25)
                    elif it.a == 437:
                        it.a = 0
                        cz.m += 1
                        ag.cS.e_I(26)
                    elif it.a in (502, 504):
                        ag.cS.e_I(17)
                    else:
                        self.a_LzLz(it, cz.X[ae.aE[b]])
                else:
                    ag.cS.e_I(17)
            ag.da = 1
            return
        elif v == 1:
            if (ag.dw & 1 << ag.ds[cM[1]] - 1) != 0:
                self.c_v()
                cM[0] = 2
                ag.cN = ae.v[cM[0]]
                ag.dk = i16(i8(cM[1]))
                self.bi_v()
                cM[2] = 0
                cM[1] = 0
                return
        elif v == 3:
            ag.cS.e_I(6)
            return

    def aF(self):  # e.java:1002-1109  (BACK)
        cM = ag.cM
        bool_ = False
        if ae.u[cM[0]] > -1:
            if cM[0] in (14, 15, 16, 17, 18):
                self.ar()
            if ae.u[cM[0]] > 99:
                ag.ej = 0
                if cM[0] == 28 and ag.cO == 5:
                    ag.ej = 7
                    bool_ = True
                cM[0] = ag.cO
                if cM[0] == 0:
                    ag.cK = 0
                    ag.cL = 0
                ag.ap()
                ag.ak()
                if bool_:
                    cM[1] = 5
                    return
            else:
                if cM[0] == 1:
                    self.F_v()
                cM[0] = ae.u[cM[0]]
                if cM[0] == 0:
                    ag.cK = 0
                    ag.cL = 0
                ag.ap()
                ag.ak()
                if ag.cO == 5:
                    if cM[1] == 3:
                        cM[1] = 2
                    elif cM[1] == 4:
                        cM[1] = 3
                        if ag.bW == 3:  # e.java:1048-1056  (back to the map's pause menu)
                            ag.bV = ag.bW
                            ag.bW = -1
                            cM[0] = 10
                            cM[1] = 4
                            ag.cN = 7
                            ag.dE = ag.fZ
                            return
                    elif cM[1] == 5:
                        cM[1] = 4
                if ag.cO == 25:
                    cM[1] = 4
                if ag.cO == 27:
                    cM[1] = 3
                    if ag.bW == 3:  # e.java:1066-1074
                        ag.bV = ag.bW
                        ag.bW = -1
                        cM[0] = 10
                        cM[1] = 4
                        ag.cN = 7
                        ag.dE = ag.fZ
                        return
        else:
            v = cM[0]
            if v == 0:
                ag.aj()
                e.aG()
                self.ae_v()
                cM[0] = 5
                ag.cN = 10
                cM[2] = 0
                cM[1] = 0
                ag.cS.b = 0
                ag.ck = 1
                return
            if v == 15:
                if cM[3] == 1:
                    cM[0] = 13
                    ag.ap()
                    ag.ct[37] = None
                    ag.ct[38] = None
                    self.ar()
                    return
                cM[3] = 1
                ag.da = 6
                return
            if v == 27:
                cM[0] = ag.ei
                ag.ap()
                ag.ak()

    @staticmethod
    def aG():  # e.java:1111-1118
        ag.cy = 0
        while ag.cy < 4:
            ag.ct[26 + ag.cy] = None
            ag.cy += 1
        ag.gl = None

    def c_v(self):  # e.java:1120-1127  (remember cursor, go to the sub-menu)
        cM = ag.cM
        ag.cO = cM[0]
        ag.cP[cM[0]] = i16(cM[1])
        ag.cQ[cM[0]] = i16(cM[2])
        cM[0] = e.m_II(cM[0], cM[1] % 7)
        ag.ck = 1
        ag.da = 0

    def d_v(self):  # e.java:1129-1139
        ag.ct[17] = None
        ag.ct[10] = None
        ag.cU = None
        ag.cW = None
        ag.cV = None
        for b in range(1, 4):
            ag.ct[0 + b] = None
        ag.fN = None
        e.aG()

    def e_v(self):  # e.java:1141-1143  (menu background ct[7])
        self.a_MIIIIII(ag.ct[7], 0, 0, ag.bZ.a, ag.bZ.b, 0, 0)

    def f_v(self):  # e.java:1145-1227  (vertical list menu: 1 2 10 11 12 13 25 27)
        cM = ag.cM
        i = ag.dd - 90
        arrayOfByte = [13, 34, 20, 0, 0, 0, 0, 0, 0, 0,
                       12, 18, 12, 13, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 13, 0, 0]
        b2 = 5 if ag.cN > 5 else ag.cN
        if cM[0] == 25 and cM[2] >= 20:
            b2 = 4
            if cM[1] >= 24:
                cM[1] = 23
        j_ = ag.de - idiv(b2 * 30 - 10, 2)
        if ag.bV == 3 or ag.bW == 3:
            j_ -= 30
        k = j_
        b = arrayOfByte[cM[0]]
        for b1 in range(b2):
            if cM[1] - cM[2] == b1:
                bool_ = True
                x.a_Lg(ag.bw)
            else:
                bool_ = False
                x.a_Lg(ag.bu)
            m = i
            self.a_IIIIZ(m, j_ + ag.dc, 180, 20, bool_)
            if ag.bV == 2:
                if cM[0] == 0:
                    if cM[2] + b1 == 3 and (0 == ag.cz.S or ag.fo == 0):
                        x.a_Lg(ag.bx)
                elif cM[0] == 1:
                    if ag.bj:
                        ag.dw = -1
                    if 0 == (ag.dw & 1 << ag.ds[cM[2] + b1] - 1):
                        x.a_Lg(ag.bx)
                elif cM[0] == 25:
                    if 0 == (ag.ed & 1 << cM[2] + b1):
                        x.a_Lg(ag.bx)
            else:
                if ag.cR.a == 1:
                    if cM[2] + b1 == 2 and (ag.ez > 0 or ag.cr != 0 or ag.eD[0] != 0):
                        x.a_Lg(ag.bx)
            if cM[0] == 25:
                if cM[2] + b1 < 24:
                    arrayOfByte1 = self.d_II(54, 38 + cM[2] + b1)
                    str_ = ag.a_ABII(arrayOfByte1, 0, len(arrayOfByte1))
                    self.b_TII(str_, j_ - 1, 18)
            elif cM[0] in (0, 10, 12, 13, 27):
                self.b_TII(ag.b_TI(ag.dE[0], b1 + cM[2]), j_ - 1, 0)
            else:
                self.b_TII(ag.dE[b1 + cM[2]], j_ - 1, b)
            j_ += 30
        if cM[0] == 25:
            self.a_IIIZ(cM[2] // 5 + 1, 5, ag.bZ.b - 35, True)
        elif cM[2] != 0 or cM[2] + 5 < ag.cN - 1:
            self.f_III(2, ag.dd - 8 - ag.db, k - 10 - 5)
            self.f_III(3, ag.dd - 8 - ag.db, j_ - 5)
        if cM[0] == 10:
            x.a_MIII(ag.bU, 120, ag.dc + 15, 17)
            x.a_Lg(ag.bu)
            self.b_TII("PAUSE", 13, 0)
        if ag.bj and cM[0] == 1:
            x.a_Lg(ag.bu)
            x.b_IIIII(ag.bJ // 2 - 16, ag.bK - 17, 32, 17, 0)
            x.a_TIII("" + str(ag.cq + 1), ag.bJ // 2, ag.bK - 16, 1)

    def j_v(self):  # e.java:1471-1521  (Options: Sound / Volume / Speed)
        i = ag.de - 50
        if ag.cM[1] == 0:
            ag.cM[1] = 1
        for b in range(1, 3):
            if ag.cM[1] == b:
                bool_ = True
                x.a_Lg(ag.bw)
            elif b == 3:
                bool_ = False
                x.a_Lg(ag.bx)
            else:
                bool_ = False
                x.a_Lg(ag.bu)
            self.a_IIIIZ(ag.dd - 100, i + ag.dc, 80, 20, bool_)
            self.a_IIIIZ(ag.dd - 10, i + ag.dc, 110, 20, bool_)
            ag.c_TII(ag.gb[b], ag.dd - 100 + 40 - ag.db, i + 1)
            if bool_:
                self.f_III(0, ag.dd - 10 - ag.db, i + 2)
                self.f_III(1, ag.dd - 10 + 110 - 10 - 1 - ag.db, i + 2)
            if b == 0:
                str_ = ag.gc[1 if ag.df else 0]
            elif b == 1:
                str_ = ""
                for b1 in range(ag.dg // 25):
                    str_ = str_ + 'I'
                if str_ == "":
                    str_ = "OFF"
            elif b == 2:
                str_ = ag.ge[ag.dh]
            elif b == 3:
                str_ = ae.aX[ag.ep]
            else:
                return
            ag.c_TII(str_, ag.dd + 156 - 111 - ag.db, i + 1)
            i += 10
            i += 20

    def l_v(self):  # e.java:2311-2348  (Help / About page cM[1] of topic ej)
        if ag.bV == 3 or ag.bW == 3:
            ag.de -= 30
        i = ag.cM[1] + ae.z[ag.ej]
        arrayOfByte = self.d_II(61, i)
        if ag.bV == 2:
            self.b_ABII(arrayOfByte, 190, 0)
            self.e_IIII(ag.dd - 100 + ag.db, ag.de - 90 + ag.dc, 200, 175)
        else:
            self.b_ABII(arrayOfByte, 190, 0)
            self.e_IIII(ag.dd - 100, ag.de - 70 + ag.dc, 200, 120)
        x.a_Lg(ag.bu)
        for b in range(ag.dq[0] + 1):
            if ag.bV == 2:
                if ag.cM[0] == 28 and ag.ej == 8:
                    self.b_TII(ag.dp[0][b], ag.de - 80 + b * 20 + 3, 30)
                    if ag.cM[1] == 1:
                        self.b_TII("v" + ag.bh, ag.de - 80 + 20 + 3, 30)
                else:
                    ag.d_TII(ag.dp[0][b], ag.dd - 95 - 1, ag.de - 80 + b * 20 + 3)
            else:
                ag.d_TII(ag.dp[0][b], ag.dd - 90 - 1 - ag.db, ag.de - 62 + b * 15)
        n = ae.z[ag.ej + 1] - ae.z[ag.ej]
        if ag.bV == 2:
            if ag.bW == 3:
                self.a_IIIZ(ag.cM[1] + 1, n, ag.bZ.b - 100, True)
            else:
                self.a_IIIZ(ag.cM[1] + 1, n, ag.bZ.b - 35, True)
        else:
            self.a_IIIZ(ag.cM[1] + 1, n, ag.de + 65, True)
        if ag.bV == 3 or ag.bW == 3:
            ag.de += 30

    def a_IIIZ(self, paramInt1, paramInt2, paramInt3, paramBoolean):  # e.java:2350-2372  (page "n / m" with arrows)
        if paramInt2 == 1:
            return
        i = ag.dd - 25 - 10
        if paramInt2 > 1:
            if paramInt1 != 1 or paramBoolean:
                self.f_III(0, i, paramInt3)
            i += 60
            if paramInt1 != paramInt2 or paramBoolean:
                self.f_III(1, i, paramInt3)
        paramInt3 += 2
        i = ag.dd - (8 + 9 * ((2 if paramInt2 > 9 else 1) + (2 if paramInt1 > 9 else 1)) + 2) // 2
        i = i + (18 if paramInt1 > 9 else 9)
        self.e_III(paramInt1, i, paramInt3 + ag.dc)
        i += 1
        if ag.bW == 3:
            ag.a_IIIIMII(i - ag.db, paramInt3 + 16, 8, 12, ag.ct[20], 90, 0)
        else:
            ag.a_IIIIMII(i - ag.db, paramInt3, 8, 12, ag.ct[20], 90, 0)
        i += 9 + (18 if paramInt2 > 9 else 9)
        self.e_III(paramInt2, i, paramInt3 + ag.dc)

    def P_I(self, paramInt):  # e.java:1523-1593  (Skills: 5 hot-key slots + skill tree pages)
        cz = ag.cz
        cM = ag.cM
        arrayOfByte = [1, 3, 7, 9, 0]
        if 0 == paramInt:
            for b in range(5):
                self.i_II(40 + b * 30 + 4 * b, 60)
                self.d_IIII(arrayOfByte[b], 40 + b * 30 + 18 + 4 * b, 70, 0)
        if paramInt % 2 == 0:
            for b in range(5):
                self.i_II(40 + b * 30 + 4 * b, 90)
                if cz.V[b] != 0:
                    self.b_MIIIIII(ag.ct[37], 40 + b * 30 + 4 * b + 1, 91, 28, 28, (cz.V[b] - 12) * 28, 0)
            self.b_IIIIIII(40 + cM[1] * 30 + 4 * cM[1], 90, 30, 30, 255, 255, 255)
        arrayOfAc = [ac(40, 140, 60, 20), ac(40, 165, 60, 20)]
        if paramInt % 3 == 0:
            i = cM[2] // 6 << 1
            b2 = 2 if cM[2] < 18 else 1
            for b1 in range(b2):
                j_ = cM[2] // 6 * 6 + b1 * 3
                ac1 = arrayOfAc[b1]
                ac1.b = ac1.b + b1 * 10 + 5
                self.b_IIIIIII(ac1.a - 1, ac1.b - 1, ac1.c + 2, ac1.d + 2, 152, 152, 152)
                ag.a_LacI(ac1, 0)
                x.a_Lg(ag.bu)
                ag.dD = ag.c_T(ag.gd[i + b1])
                ag.d_TII(ag.gd[i + b1], ac1.a + idiv(ac1.c - ag.dD, 2), ac1.b + 1)
                for b in range(3):
                    self.i_II(40 + (b + 2) * 34, 140 + 35 * b1)
                    if ae.aC[j_ + b] != 0:
                        if cz.W[ae.aC[j_ + b] - 12] != 0:
                            image = ag.ct[37]
                        else:
                            image = ag.ct[38]
                        self.b_MIIIIII(image, 40 + (b + 2) * 34 + 1, 140 + 35 * b1 + 1, 28, 28,
                                       (ae.aC[j_ + b] - 12) * 28, 0)
            if cM[3] == 2:
                # DECOMP-FIX F10: `35 * cM[2] % 6 / 3` -> `35 * (cM[2] % 6 / 3)`
                row = 35 * (cM[2] % 6 // 3) if F10 else 35 * cM[2] % 6 // 3
                self.b_IIIIIII(40 + (cM[2] % 3 + 2) * 34, 140 + row, 30, 30, 255, 255, 255)
            ac_ = ac(210, 0, 3, 20)
            self.a_IIIIZ(210, 150, 3, 50, False)
            if i == 6:
                ac_.a = 210
                ac_.b = 152
                ac_.c = 3
                ac_.d = 46
                ag.a_LacI(ac_, ag.k_III(231, 227, 198))
            else:
                ac_.b = 151 + (i >> 1) * 14 + ag.dc
                ag.a_LacI(ac_, ag.k_III(231, 227, 198))
        # System.out.println("GameCanvas.DrawSkillSet(2)");
        if cM[3] == 1:
            self.b_IIIII(cz.V[cM[1]] + 2000, ag.dd - 100, ag.bZ.b - 70, 200, 22)
        else:
            self.b_IIIII(ae.aC[cM[2]] + 2000, ag.dd - 100, ag.bZ.b - 70, 200, 22)
        ag.da = 0

    def k_v(self):  # e.java:1595-1630  (description strip; scrolls when longer than the box)
        dF = ag.dF
        self.a_IIIIZ(dF.b.a + ag.db, dF.b.b + ag.dc, dF.b.c, dF.b.d, False)
        x.a_Lg(ag.bu)
        if dF.a != 0:
            ag.dD = ag.c_T(dF.c)
            dF.d = i16(dF.d - 5)
            if dF.b.a - dF.d > ag.dD + 3:
                dF.d = i16(dF.b.a + dF.b.c)
        ag.d_TII(dF.c, dF.d, dF.b.b + (dF.b.d - 11 >> 1) - 2)
        i = (ag.bJ - dF.b.c) // 2
        j_ = dF.b.b + ag.dc
        s1 = 0
        s2 = 0
        if ag.bV == 3:
            s1 = ag.db
            s2 = ag.dc
            x.b_IIIII(0, j_, i, dF.b.d, 0)
            x.b_IIIII(ag.bJ - i, j_, i, dF.b.d, 0)
        self.a_MIIIIII(ag.ct[7], 0, j_, i, dF.b.d, -s1, j_ - s2)
        x.c_IIIII(i - 1, j_, i - 1, j_ + dF.b.d - 1, ag.k_III(80, 80, 80))
        self.a_MIIIIII(ag.ct[7], ag.bJ - i, j_, i - s1, dF.b.d, ag.bJ - i - s1, j_ - s2)
        x.c_IIIII(ag.bJ - i, j_, ag.bJ - i, j_ + dF.b.d - 1, ag.k_III(80, 80, 80))
        if ag.bV == 3:
            x.a_IIII(0, j_, ag.bJ, dF.b.d)
            ag.bd.b_v()
            x.a_v()
            x.a_IIII(0, j_, i - 1, dF.b.d)
            ag.cS.b_I(170)
            x.a_v()
            x.a_IIII(ag.bJ - i + 1, j_, i - 1, dF.b.d)
            ag.cS.b_I(170)
            x.a_v()

    def n_II(self, paramInt1, paramInt2):  # e.java:1632-1654  (Gear: hero sprite + 9 equipment slots)
        cz = ag.cz
        arrayOfByte1 = [-77, -77, -77, -33, 3, 47, 47, 47, -15]
        arrayOfByte2 = [21, -15, -51, -79, -79, -51, -15, 21, 49]
        ag.ct[39] = self.d_T(ag.bA.a_I(50))
        ct39 = ag.ct[39]
        self.b_MIIIIII(ct39, ag.dd - ct39.getWidth() // 2, ag.de - ct39.getHeight() // 2,
                       ct39.getWidth(), ct39.getHeight(), 0, 0)
        ag.ct[39] = None
        for b in range(9):
            if cz.X[b].a != 0:
                self.e_I(cz.X[b].a)
                self.g_IIII(cz.X[b].a, ag.dd + arrayOfByte1[b], ag.de + arrayOfByte2[b], 0)
        self.b_IIIIIII(ag.dd + arrayOfByte1[paramInt1] - 1, ag.de + arrayOfByte2[paramInt1] - 1, 30, 30, 255, 255, 255)
        ag.fK[24] = ag.dd + arrayOfByte1[paramInt1] + ag.db + 7
        ag.fK[25] = ag.de + arrayOfByte2[paramInt1] + ag.dc + 7
        f1 = cz.aE[1]
        self.b_MIIIIII(cz.aH, ag.dd - f1.e, ag.de + 7 - f1.f + 17, f1.c, f1.d, f1.a, f1.b)
        f2 = cz.aC[1]
        self.b_MIIIIII(cz.aG, ag.dd - f2.e, ag.de + 7 - f2.f + 17, f2.c, f2.d, f2.a, f2.b)
        if paramInt2 != 0:
            ag.a_LzZI(self.o_I(-1), True, -1)
            return
        self.b_IIIII(paramInt1 + 1000, ag.dd - 79, ag.de + 81 + 5, 158, 20)

    def Q_I(self, paramInt):  # e.java:1656-1692  (Inventory: 5x5 grid in 2 pages + gold)
        cz = ag.cz
        cM = ag.cM
        arrayOfInt1 = [ag.dd - 75, ag.dd - 45, ag.dd - 15, ag.dd + 15, ag.dd + 45]
        arrayOfInt2 = [ag.de - 45, ag.de - 15, ag.de + 15]
        ac_ = ac(ag.dd + 80, ag.de - 40, 5, 80)
        if cM[2] < 15:
            b2 = 3
            b3 = 0
        else:
            b2 = 2
            b3 = 15
        if paramInt != 0:
            self.b_MIIIIII(ag.ct[7], ag.dd - 75, ag.de - 45, 150, 100, ag.dd - 75, ag.de - 45)
        for b1 in range(b2):
            for b in range(5):
                self.i_II(arrayOfInt1[b] + ag.db, arrayOfInt2[b1] + ag.dc)
                self.e_I(cz.Y[b3 + b1 * 5 + b].a)
                self.g_IIII(cz.Y[b3 + b1 * 5 + b].a, arrayOfInt1[b] + 1, arrayOfInt2[b1] + 1, 0)
        ag.a_LacI(ac_, ag.k_III(148, 148, 148))
        ac_.a += 1
        ac_.b += 1
        ac_.c -= 2
        ac_.d -= 2
        ag.a_LacI(ac_, ag.k_III(33, 0, 0))
        ac_.b = ag.de - 39 + (39 if b3 != 0 else 0) + ag.dc
        ac_.d = 39
        ag.a_LacI(ac_, ag.k_III(231, 227, 198))
        self.b_IIIII(cM[2] + 1100, ag.dd - 75, ag.de + 50, 150, 22)
        self.b_IIIIIII(arrayOfInt1[cM[2] % 5], arrayOfInt2[(cM[2] - b3) // 5] + ag.dc, 30, 30, 255, 255, 255)
        if 0 == paramInt:
            self.J_v()
        ag.da = 0

    def d_I(self, paramInt):  # e.java:3022-3058  (Assign Items: 5 potion slots, * and # quick keys)
        cz = ag.cz
        if ag.bV == 3:
            ag.de -= 30
        if 0 == paramInt:
            self.J_v()
            x.a_Lg(ag.bu)
            for b1 in range(5):
                self.a_IIIIZ(ag.dd - 80 + 32 * b1, ag.de - 40 + ag.dc, 30, 22, False)
                if cz.aa[0] == b1:
                    ag.d_TII(" * ", ag.dd - 80 + 32 * b1 - ag.db, ag.de - 38)
                elif cz.aa[1] == b1:
                    ag.d_TII(" # ", ag.dd - 80 + 32 * b1 - ag.db, ag.de - 38)
        for b in range(5):
            if ag.bV == 3:
                self.a_IIIIZ(ag.dd - 79 + 32 * b, ag.de + 6, 28, 28, False)
                self.g_IIII(cz.Z[b].a, ag.dd - 79 + 32 * b - ag.db, ag.de + 6 - ag.dc, b)
            else:
                self.a_IIIIZ(ag.dd - 79 + 32 * b, ag.de - 10, 28, 28, False)
                self.g_IIII(cz.Z[b].a, ag.dd - 79 + 32 * b - ag.db, ag.de - 10 - ag.dc, b)
        if ag.bV == 3:
            self.b_IIIIIII(ag.dd - 80 + 32 * ag.cM[1], ag.de + 6, 30, 29, 255, 255, 255)
        else:
            self.b_IIIIIII(ag.dd - 80 + 32 * ag.cM[1], ag.de - 10, 30, 29, 255, 255, 255)
        ag.da = 0
        self.b_IIIII(ag.cM[1] + 1200, ag.dd - 80 - ag.db, ag.de + 30, 160, 22)
        self.a_IIIIZ(ag.dd - 80, ag.de + 60 + ag.dc, 160, 22, False)
        x.a_Lg(ag.bu)
        self.b_TII("*,# key Assign", ag.de + 60, 15)
        if ag.bV == 3:
            ag.de += 30

    def g_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # e.java:3060-3081  (item icon)
        i = -1
        b = 0
        if paramInt1 > 500:
            i = paramInt1 - 501
            b = 3
        elif paramInt1 > 300:
            i = ag.cY.g
            b = 2
        elif paramInt1 > 100:
            i = ag.cX.f
            b = 1
        elif paramInt1 > 0:
            i = paramInt1 - 1
            b = 0
        if i > -1:
            self.b_MIIIIII(ag.ct[0 + b], paramInt2, paramInt3, 28, 28, i * 28, 0)
            if paramInt1 < 100:
                self.i_III(paramInt2, paramInt3 + 2, ag.cz.Z[paramInt4].b)

    # ---- Blacksmith (screens 21 Buy, 22 Sell, 23 Enchant, 24 Combine) ----------------------
    # fK[0] = mode (cM[0]-21), fK[9]/fK[10] = cursor col/row, fK[18] = cell, fK[19] = item id,
    # fK[20] = message for aV(), fK[21] = price, fK[26] = sparkle frame (-1 idle), fK[27] = 1 on Gear

    def a_IAzAI(self, paramInt, paramArrayOfz, paramArrayOfint):  # e.java:1804-1861  (item grid)
        i = ag.fK[8] * 5
        if ag.fK[11] == 1:
            ac1 = ac(0, 0, 0, 0)
            ac2 = ac(0, 0, 0, 0)
            ac1.c = 4
            ac1.a = ag.fK[12]
            ac1.d = ag.fK[6]
            ac1.b = paramInt
            ag.a_LacII(ac1, 16777215, 0)
            ac1.c -= 2
            ac1.a += 1
            ac1.d -= 2
            ac1.b += 1
            j_ = ag.fK[8] * 32
            k = ac2.d
            j_ = idiv(j_ * k, ag.fK[7])
            ac2.d = ag.fK[13]
            ac2.b += j_
            ag.a_LacI(ac2, 16777215)
            ag.b_LacI(ac1, 10000536)
        paramInt += 1
        b1 = 0
        b2 = 0
        while b1 < ag.fK[3]:
            j_ = ag.fK[5]
            for b in range(5):
                if i == ag.fK[18]:
                    bool_ = True
                    ag.fK[24] = j_ + 13 + 1
                    ag.fK[25] = paramInt + 13 + 1
                else:
                    bool_ = False
                for b3 in range(ag.fO[3]):
                    if ag.fO[b3] == i:
                        bool_ = True
                        ag.fP[b2].a = i16(j_ + 13 + 1)
                        ag.fP[b2].b = i16(paramInt + 13 + 1)
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
        if ag.fK[0] == 1 and 0 < z1.a < 100:
            bool_ = z1.b
        else:
            bool_ = 0
        self.a_IIII(z1.a, paramInt2, paramInt3, bool_)

    def a_IIZ(self, paramInt1, paramInt2, paramBoolean):  # e.java:1879-1881  (grid cell frame)
        ag.a_IIIIIIIZ(paramInt1 + 1, paramInt2 + 1, 26, 26, 0, 0, 16777215 if paramBoolean else 5263440, True)

    def a_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # e.java:1883-1902  (item icon by id + count)
        if paramInt1 > 500:
            image = ag.ct[3]
            i = paramInt1 - 501
        elif paramInt1 > 300:
            image = ag.ct[2]
            i = ag.bH[1].a_II(paramInt1 - 301, 7)
        elif paramInt1 > 100:
            image = ag.ct[1]
            i = ag.bH[0].a_II(paramInt1 - 101, 7)
        else:
            image = ag.ct[0]
            i = paramInt1 - 1
        ag.a_IIIIMII(paramInt2, paramInt3, 28, 28, image, i * 28, 0)
        if paramInt4 > 0:
            ag.a_IIIIMII(paramInt2, paramInt3, 9, 12, ag.ct[20], paramInt4 * 9, 0)

    def aP(self):  # e.java:1904-1910  (gold + item grid + description)
        i = ag.fK[1] + 1
        self.i_I(i)
        i += 29
        self.a_IAzAI(i, None, None)
        ag.a_LzZI(self.o_I(-1), True, -1)

    def c_Z(self, paramBoolean):  # e.java:1912-2111  (decompiler gave bytecode only; rebuilt from it)
        fK = ag.fK
        if paramBoolean:
            if fK[27] == 0:
                self.aP()
            else:
                self.n_II(fK[18], 1)
            if fK[23] == -1 and ag.cS.b == 0:
                # the Yes/No popup of Enchant / Combine has just closed
                fK[23] = 0
                if ag.ch == -5 and ag.cS.k == 0:
                    if fK[21] > ag.cz.E:
                        fK[20] = 4
                        e.aV()
                        e.bb()
                    else:
                        fK[26] = 0          # start the sparkle, the action follows below
                else:
                    e.bb()
        if fK[26] == -1:
            return
        if fK[26] < 5:
            self.aR()
            fK[26] += 1
            return
        fK[26] = -1
        ag.ck = 1
        if fK[0] == 2:
            self.aQ()
        elif fK[0] == 3:
            cz = ag.cz
            if fK[22] == 0:
                for b in range(3):
                    z.a(cz.Y[ag.fO[b]])
                dst = cz.Y[ag.fO[2]]
                dst.a = ag.fQ.a
                dst.b = ag.fQ.b
                dst.c = ag.fQ.c
                dst.d = ag.fQ.d
                dst.e = ag.fQ.e
                dst.f = ag.fQ.f
            elif fK[31] != -1:
                z.a(cz.Y[fK[31]])
                fK[31] = -1
            e.bb()
            fK[20] = 9
            cz.E -= fK[21]
        self.ar()
        e.aV()

    def aQ(self):  # e.java:2113-2135  (Enchant: roll success / fail / lost)
        arrayOfByte1 = [100, 90, 80, 70, 60, 45, 30, 10, 1]
        arrayOfByte2 = [0, 10, 20, 40, 50, 60, 70, 80, 90]
        z_ = self.o_I(-1)
        ag.fK[20] = 2
        ag.cz.E -= ag.fK[21]
        if ag.fK[22] == -1:
            ag.fK[23] = 2
        else:
            i = self.C_I(100) + 1
            if i > arrayOfByte1[z_.f]:
                i = self.C_I(100)
                ag.fK[23] = 2 if i <= arrayOfByte2[z_.f] else 1
            else:
                self.a_LzI(z_, 1)
                ag.fK[23] = 0
        if ag.fK[23] == 2:
            z.a(z_)
            ag.fK[23] = 1

    def o_II(self, paramInt1, paramInt2):  # e.java:2137-2144  (sparkle frame)
        arrayOfByte1 = [0, 15, 30, 0, 20]
        arrayOfByte2 = [0, 0, 0, 16, 16]
        arrayOfByte3 = [16, 16, 16, 20, 24]
        n = arrayOfByte3[ag.fK[26]]
        paramInt1 -= n >> 1
        paramInt2 -= n >> 1
        ag.a_IIIIMII(paramInt1, paramInt2, n, n, ag.fN, arrayOfByte1[ag.fK[26]], arrayOfByte2[ag.fK[26]])

    def aR(self):  # e.java:2146-2156
        if ag.fK[0] == 2:
            self.o_II(ag.fK[24], ag.fK[25])
            return
        if ag.fK[0] == 3:
            for b in range(3):
                if ag.fP[b].a > 0 and ag.fP[b].b > 0:
                    self.o_II(ag.fP[b].a, ag.fP[b].b)

    @staticmethod
    def aV():  # e.java:2396-2451  (Blacksmith message popup)
        from pow.game.l import l
        arrayOfString = ["Success", "Fail"]
        str_ = ""
        ag.cS.a_v()
        ag.ck = 1
        fK = ag.fK
        v = fK[20]
        if v == 0:
            if fK[19] < 1:
                return
            str_ = l.d_v()
        elif v == 11:
            str_ = l.e_v()
        elif v == 1:
            if fK[22] == 0:
                str_ = "1Not possible |to enchant."
            else:
                str_ = "2Price is " + str(fK[21]) + ".If |enchanting fails,|Items can be lost.|Continue?"
                ag.cS.d = 200
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
                ag.cS.d = 200
        elif v == 9:
            str_ = "1Compounding| " + arrayOfString[fK[22]]
        ag.cS.a_T(str_)

    def aW(self):  # e.java:2453-2566  (Blacksmith keys)
        fK = ag.fK
        bool_ = True
        if fK[26] != -1:
            return
        ch = ag.ch
        if ch in (-1, 50):
            if fK[27] == 0:
                fK[10] = fK[10] - 1
            else:
                fK[18] = fK[18] + 1
                if _inc_cmp(fK[18]) > 8:
                    fK[18] = 0
            ag.dF.c = ""
        elif ch in (-2, 56):
            if fK[27] == 0:
                fK[10] = fK[10] + 1
            else:
                fK[18] = fK[18] - 1
                if _dec_cmp(fK[18]) < 0:
                    fK[18] = 8
            ag.dF.c = ""
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
            ag.dF.c = ""
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
            ag.dF.c = ""
        elif ch == -7:
            cM = ag.cM
            cM[0] = ae.u[cM[0]]
            ag.cN = ae.v[cM[0]]
            cM[1] = ag.cP[cM[0]]
            cM[2] = ag.cQ[cM[0]]
            ag.ck = 1
            bool_ = False
            ag.ct[39] = None
            ag.dF.c = ""
            e.bb()
        elif ch in (-5, 53):
            if fK[0] == 0:
                self.bc()
                bool_ = False
                e.aV()
            elif fK[0] == 1:
                if fK[19] != 0:
                    self.bd()
                    e.aV()
                else:
                    bool_ = False          # falls into `default`
            elif fK[0] == 2:
                self.be()
                e.aV()
                bool_ = False              # falls into `default`
            else:
                if fK[0] == 3 and self.o_I(-1).a > 100:
                    b = 3
                    if ag.fO[3] > 0:
                        b = 0
                        while b < ag.fO[3] and ag.fO[b] != fK[18]:
                            b += 1
                    if b < ag.fO[3]:
                        while b < 2:
                            ag.fO[b] = ag.fO[b + 1]
                            b += 1
                        ag.fO[3] = ag.fO[3] - 1
                    else:
                        ag.fO[ag.fO[3]] = fK[18]
                        ag.fO[3] = ag.fO[3] + 1
                    if ag.fO[3] == 3:
                        self.aX()
        else:
            bool_ = False
        if bool_:
            self.ba()
            ag.bb.c_Z(True)

    def aX(self):  # e.java:2568-2626  (Combine: work out the result of 3 items)
        arrayOfInt = [0, 0, 0]
        i = 0
        for b in range(3):
            z_ = self.o_I(ag.fO[b])
            b1 = 0
            while b1 < b and arrayOfInt[b1] <= z_.a:
                b1 += 1
            for b2 in range(b, b1, -1):
                arrayOfInt[b2] = arrayOfInt[b2 - 1]
            arrayOfInt[b1] = z_.a
            i += z_.f
        e.a = j.a("/" + ag.bE.a_I(68))
        if e.a is not None:
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
                ag.fK[22] = 2
                e.bb()
            else:
                j_ += self.C_I(k)
                arrayOfInt[0] = e.S_I(447 + j_)
                ag.fQ = self.J_I(arrayOfInt[0])
                ag.fK[21] = idiv(e.b_Lz(ag.fQ), 4)
                if arrayOfInt[0] < 500:
                    arrayOfInt[1] = ag.bH[1].a_II(arrayOfInt[0] - 301, 8)
                    arrayOfInt[2] = 15
                else:
                    arrayOfInt[1] = ag.bH[2].a_II(arrayOfInt[0] - 501, 7)
                    arrayOfInt[2] = 12
                arrayOfInt[1] = idiv(200 - arrayOfInt[1], 12)
                if arrayOfInt[1] >= self.C_I(101):
                    ag.fK[22] = 0
                    ag.fQ = self.a_LzI(ag.fQ, idiv(i, 3))
                else:
                    ag.fK[22] = 1
                    arrayOfInt[1] = idiv((100 - arrayOfInt[1]) * 10, arrayOfInt[2])
                    ag.fK[31] = ag.fO[self.C_I(3)] if arrayOfInt[1] >= self.C_I(101) else -1
                ag.fK[23] = -1
            ag.fK[20] = 8
            e.aV()
        e.a = None

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
        return e.a[paramInt * 2] & 0xFF | (e.a[paramInt * 2 + 1] & 0xFF) << 8

    def b_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # e.java:2674-2692  (find run of paramInt2)
        arrayOfInt = [paramInt3, paramInt4, 0]
        b = 0
        while b < arrayOfInt[1]:
            i = e.S_I(paramInt1 + arrayOfInt[0])
            if i == paramInt2:
                break
            arrayOfInt[0] = arrayOfInt[0] + 1
            b += 1
        if b < arrayOfInt[1]:
            arrayOfInt[1] = arrayOfInt[1] - b
            b = 0
            i = e.S_I(paramInt1 + arrayOfInt[0])
            while b < arrayOfInt[1] and i == paramInt2:
                b += 1
                i = e.S_I(paramInt1 + arrayOfInt[0] + b)
            arrayOfInt[1] = b
            arrayOfInt[2] = 1
            return arrayOfInt
        arrayOfInt[2] = 0
        return arrayOfInt

    def aY(self):  # e.java:2694-2707  (enter a Blacksmith screen)
        if ag.cM[0] == 24:
            e.m_v()
            if ag.fK[16] < 3:
                ag.cS.e_I(39)
                ag.ck = 1
                ag.cM[1] = 3
                return True
        ag.az()
        self.aZ()
        return True

    def aZ(self):  # e.java:2709-2754  (grid layout of the current Blacksmith mode)
        fK = ag.fK
        fK[0] = ag.cM[0] - 21
        if fK[0] == 0 or fK[0] == 1:
            fK[14] = fK[0] + 1
        else:
            fK[14] = 0
        if fK[0] == 3:
            e.bb()
            fK[20] = 7
            e.aV()
        e.m_v()
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
        fK = ag.fK
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
            return ae.aN[paramInt - 1]
        if paramInt < 300:
            return ag.bH[0].b_II(paramInt - 101, 0)
        if paramInt < 500:
            return ag.bH[1].b_II(paramInt - 301, 0)
        return ag.bH[2].b_II(paramInt - 501, 0)

    @staticmethod
    def bb():  # e.java:2788-2801  (clear the Combine selection)
        from pow.game.structs import h
        for b in range(len(ag.fO)):
            ag.fO[b] = 0
        for b in range(len(ag.fP)):
            if ag.fP[b] is None:
                ag.fP[b] = h()
            ag.fP[b].a = 0
            ag.fP[b].b = 0
        if ag.fQ is None:
            ag.fQ = z()
        z.a(ag.fQ)

    @staticmethod
    def m_v():  # e.java:2803-2815  (count items: fK[16] backpack, fK[17] potions)
        ag.fK[16] = 0
        for b in range(25):
            if ag.cz.Y[b].a > 0:
                ag.fK[16] = ag.fK[16] + 1
        ag.fK[17] = 0
        for b in range(5):
            if ag.cz.Z[b].a > 0:
                ag.fK[17] = ag.fK[17] + 1

    @staticmethod
    def b_Lz(paramz):  # e.java:2817-2830  (price of an item)
        if paramz.a < 100:
            i = ae.y[paramz.a - 1]
        elif paramz.a < 300:
            i = ag.bH[0].a_II(paramz.a - 101, 6)
            i = i + paramz.b * 100
            i = i + paramz.c * 100
            i = i + idiv(paramz.d, 5) * 100
            i = i + idiv(paramz.e, 3) * 100
        elif paramz.a < 500:
            j_ = 800 if ag.bH[1].a_II(paramz.a - 301, 6) == 0 else 400
            i = paramz.b * j_
            i = i + paramz.c * j_
            i = i + idiv(paramz.d, 5) * j_
            i = i + idiv(paramz.e, 3) * j_
        else:
            i = ag.bH[2].a_II(paramz.a - 501, 6)
        return i

    def bc(self):  # e.java:2832-2883  (Buy)
        cz = ag.cz
        fK = ag.fK
        z_ = ag.fL[fK[18]]
        if z_.a == 0:
            fK[20] = -1
            return
        i = e.b_Lz(z_)
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
                z.a(z_)
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
        cz = ag.cz
        fK = ag.fK
        z_ = self.o_I(-1)
        if z_ is None or z_.a == 0:
            return
        i = e.b_Lz(z_)
        if z_.a < 100:
            if cz.Z[fK[18]].b > 1:
                cz.Z[fK[18]].b = i16(cz.Z[fK[18]].b - 1)
            else:
                cz.Z[fK[18]].a = 0
                cz.Z[fK[18]].b = 0
                fK[17] = fK[17] - 1
        else:
            z.a(z_)
            fK[16] = fK[16] - 1
        fK[20] = 11
        cz.E += idiv(i, 2)
        self.ar()

    def be(self):  # e.java:2907-2936  (Enchant: price and limit)
        fK = ag.fK
        z_ = self.o_I(-1)
        if z_.a == 0:
            fK[20] = -1
            return
        fK[22] = 0
        fK[21] = 0
        if 100 < z_.a < 500:
            if z_.a < 300:
                fK[22] = ag.bH[0].a_II(z_.a - 101, 5)
            else:
                fK[22] = ag.bH[1].a_II(z_.a - 301, 6)
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
        dF = ag.dF
        str1 = "/ Price: "
        str2 = "Price: "
        if paramz.a == 0:
            dF.a = 0
            dF.b.a = dF.b.b = dF.b.c = dF.b.d = 0
            dF.c = ""
            dF.b.a = (ag.bJ - 202) // 2 - ag.db
            dF.b.b = 200
            dF.b.c = paramInt3 + 2
            dF.b.d = paramInt4
            return
        if ag.fK[14] > 0 and paramInt5 == -1:
            paramInt5 = e.b_Lz(paramz)
        if paramz.a < 100:
            i = paramz.a - 1
            dF.c = ae.aN[i]
            if ag.fK[14] == 2:
                if len(dF.c) > 0:
                    dF.c += " / "
                dF.c += str2
                dF.c += ag.n_I(paramInt5 >> 1)
            dF.c += " / "
            if i < 9:
                str_ = "Recover " + str(ae.aP[i % 3]) + "% of total " + ae.aO[i // 3]
            else:
                str_ = "Ranged Atk"
            dF.c += str_
            if ag.fK[14] == 1:
                dF.c += str1
                dF.c += ag.n_I(paramInt5)
        else:
            if paramz.a < 300:
                str_ = ag.bH[0].b_II(paramz.a - 101, 0)
                i = ae.w[(paramz.a - 101) % 5]
            elif paramz.a < 500:
                str_ = ag.bH[1].b_II(paramz.a - 301, 0)
                i = ag.bH[1].a_II(paramz.a - 301, 8)
            else:
                str_ = ag.bH[2].b_II(paramz.a - 501, 0)
                i = ag.bH[2].a_II(paramz.a - 501, 7)
            if paramBoolean:
                dF.c += str_
            if ag.fK[14] == 2:
                if len(dF.c) > 0:
                    dF.c += " / "
                dF.c += str2
                dF.c += ag.n_I(paramInt5 >> 1)
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
            if ag.fK[14] == 1:
                dF.c += str1
                dF.c += ag.n_I(paramInt5)
        dF.b.a = (ag.bJ - 202) // 2 - ag.db
        dF.b.b = 200
        dF.b.c = paramInt3 + 2
        dF.b.d = paramInt4
        ag.dD = ag.c_T(dF.c)
        if ag.dD > paramInt3 - 2:
            dF.a = 1
            if ag.ch != -999:
                dF.d = i16(dF.b.a + dF.b.c)
                return
        else:
            dF.a = 0
            dF.d = i16(paramInt1 + 1)

    def g_v(self):  # e.java:1241-1244
        self.E_v()
        ag.ct[18] = self.d_T(ag.bA.a_I(77))

    def aJ(self):  # e.java:1370-1383  (Main Menu: caption strip + blinking arrows)
        i = ag.cM[1]
        j_ = ag.dd - 52 + ag.db
        if 0 == i and not ag.aq():
            i = 9
        ag.a_IIIIMII(j_, ag.bZ.b - 65, 116, 21, ag.ct[18], 0, i * 21)
        ag.a_IIIIMII(j_ - 24 - ag.dr % 3 * 2, ag.bZ.b - 65 + 2, 10, 16, ag.ct[17], 0, 0)
        ag.a_IIIIMII(j_ + 116 + 16 + ag.dr % 3 * 2, ag.bZ.b - 65 + 2, 10, 16, ag.ct[17], 10, 0)
        if ag.dr > 100:
            ag.dr = 32
            return
        ag.dr += 1

    def aK(self):  # e.java:1385-1404  (screen 6: choose the hero, 3 heads, the middle one is chosen)
        image = None
        i = ag.cz.aB - 1 & 0x3
        x.a_Lg(ag.bu)
        for b in range(3):
            str_ = ag.M_I(65 + b)
            self.b_TII(str_, ag.de - 90 - b * 20 + 10, 0)
        for b in range(3):
            image = self.d_T(ag.bB.a_I(38 + i))
            self.b_IIIIIII(ag.dd - 94 + 69 * b + ag.db, ag.de + 9 + ag.dc, 50, 50, 148, 109, 82)
            self.a_IIIIIII(ag.dd - 93 + 69 * b + ag.db, ag.de + 10 + ag.dc, 48, 48, 33, 0, 0)
            self.b_MIIIIII(image, ag.dd - 92 + 69 * b, ag.de + 11, 46, 46, 0, 0)
            i = i + 1 & 0x3
        self.c_IIIIIII(ag.dd - 27 + ag.db + 1, ag.de + 8 + ag.dc, 52, 52, 255, 182, 82)
        self.f_III(0, ag.dd - 40, ag.de + 23)
        self.f_III(1, ag.dd + 30, ag.de + 23)

    def aL(self):  # e.java:1406-1413  (screen 7: the two caption lines)
        x.a_Lg(ag.bu)
        ag.cy = 0
        while ag.cy < 2:
            self.b_TII(ag.M_I(69 + ag.cy), ag.de - 47 + ag.cy * 20, 0)
            ag.cy += 1

    def aM(self):  # e.java:1415-1427  (screen 7: the name box)
        i = ag.dd - 80 + ag.db
        j_ = ag.de + 8 + ag.dc
        x.b_IIIII(i, j_, 160, 20, 0)
        x.a_IIIII(i, j_, 160, 20, ag.k_III(173, 170, 173))
        x.a_Lg(ag.bu)
        x.a_TIII(ag.bz.a_v(), ag.bL, j_ + 2, 1)
        if ag.bz.b_v() == 0:
            ag.h_II(-1, 2)
            return
        ag.h_II(-1, 10)

    def O_I(self, paramInt):  # e.java:1429-1469  (screen 8/14: stat sheet; 1 = whole, 0 = numbers only)
        cz = ag.cz
        arrayOfInt1 = [cz.o, cz.q, cz.m, cz.n]
        image = None
        if paramInt != 0:
            arrayOfInt = self.p_v()
            ag.dZ[0] = i16(idiv(cz.G * 100, arrayOfInt[0]))
            image = self.d_T(ag.bA.a_I(26))
            i = image.getWidth()
            j_ = image.getHeight()
            ag.eN = ag.de - j_ // 2
            ag.eM = ag.dd - i // 2
            self.b_MIIIIII(image, ag.eM, ag.eN, i, j_, 0, 0)
            ag.c_TII(cz.k, ag.eM + 110, ag.eN + 6)
            self.d_IIII(cz.l, ag.eM + 152, ag.eN + 34, 0)
            self.d_IIII(cz.F, ag.eM + 152, ag.eN + 61, 0)
        else:
            arrayOfInt = [ag.eM + 88, ag.eN + 83, 68, 20]
            x.b_IIIII(arrayOfInt[0], arrayOfInt[1], arrayOfInt[2], arrayOfInt[3], 0)
            arrayOfInt[0] = ag.eM + 39
            arrayOfInt[1] = ag.eN + 108
            arrayOfInt[2] = 104
            arrayOfInt[3] = 18
            for b1 in range(4):
                x.b_IIIII(arrayOfInt[0], arrayOfInt[1], arrayOfInt[2], arrayOfInt[3], 0)
                arrayOfInt[1] = arrayOfInt[1] + 20
        arrayOfInt2 = [cz.u, cz.v, cz.s, cz.t]
        self.d_IIII(cz.J, ag.eM + 152, ag.eN + 86, 0)
        for b in range(4):
            i = self.d_IIII(arrayOfInt1[b], ag.eM + 44, ag.eN + 110 + b * 20, 1)
            if arrayOfInt2[b] > 0:
                self.b_MIIIIII(ag.ct[19], i + 1, ag.eN + 110 + b * 20, 10, 14, 105, 0)
                self.d_IIII(arrayOfInt2[b], i + 9, ag.eN + 110 + b * 20, 1)
        image = self.d_T(ag.bB.a_I(38 + cz.aB))
        self.b_MIIIIII(image, ag.eM + 2, ag.eN + 3, 46, 46, 0, 0)
        if cz.J > 0:
            self.a_IIIIIII(ag.eM + 144, ag.eN + 97 + 20 * ag.cM[1] + ag.dc + 11, 14, 18, 255, 255, 255)
        ag.da = 0

    def b_I(self, paramInt):  # e.java:2158-2165  (story: speaker portrait top-left, hero bottom-right)
        self.a_IIIIZ(19 + ag.db + 2, ag.de - 72 + 9 + ag.dc, 46, 46, True)
        if paramInt > -1:
            self.a_TIIIIII(ag.bB.a_I(0 + paramInt), 19 + ag.db + 2, ag.de - 73 + 10 + ag.dc, 46, 46, 0, 0)
        self.a_IIIIZ(ag.bZ.a // 2 + 60 - ag.db, ag.de - 72 + 109 + ag.dc, 46, 46, True)
        self.a_TIIIIII(ag.bB.a_I(38 + ag.cz.aB), ag.bZ.a // 2 + 60 - ag.db, ag.de - 73 + 110 + ag.dc, 46, 46, 0, 0)
        self.R_I(3)

    def R_I(self, paramInt):  # e.java:2167-2172  (empty speech boxes: 1 = top, 2 = bottom)
        if (paramInt & 0x1) != 0:
            self.a_IIIIZ(ag.dd - 60 + 15 + ag.db, ag.de - 73 + 7 + ag.dc, 150, 53, False)
        if (paramInt & 0x2) != 0:
            self.a_IIIIZ(ag.dd - 60 + -40 + ag.db, ag.de - 73 + 107 + ag.dc, 150, 53, False)

    @staticmethod
    def a_III(paramInt1, paramInt2, paramInt3):  # e.java:2216-2309  (type speech text fw[p1], max 3 lines)
        # paramInt3 == 0: one tick of typing (state kept in fA/fx/fy/fz/fB/fC); 1: redraw all
        from pow.game.g import g
        if paramInt1 == 0:
            i3 = ag.dd - 60 + 15 + 2 + ag.db
            i4 = ag.de - 73 + 7 + 2 + ag.dc
        elif paramInt1 == 1:
            i3 = ag.dd - 60 + -40 + 2 + ag.db
            i4 = ag.de - 73 + 107 + 2 + ag.dc
        else:
            return False
        if (ag.ch == -6 or ag.ch == -5) and 0 == paramInt3:
            i1 = 1000                    # a key shows the whole text at once
        else:
            i1 = ag.fA[paramInt1]
        # decompiled `if (!(n = (p2 != i1) ? 0 : p2))`: n == 0 -> start over, else continue
        n = 0 if paramInt2 != i1 else paramInt2
        if n == 0:
            i = i3
            j_ = i4
            i2 = 0
            m = 0
            k = 0
        else:
            i = ag.fx[paramInt1]
            j_ = ag.fy[paramInt1]
            i2 = ag.fB[paramInt1]
            m = ag.fC[paramInt1]
            k = ag.fz[paramInt1]
        x.a_Lg(ag.bu)
        while n <= i1 and n < len(ag.fw[paramInt1]):
            fw = ag.fw[paramInt1]
            i5 = g.b_v() + g.c_v()
            p = (1 if n <= 0 else n) - 1
            if i == i3 or (p < len(fw) and fw[p] == ' ') or (n - 1 < len(fw) and fw[n - 1] == ']'):
                b = 0
                i6 = 0
                while n + b + 1 < len(fw) and fw[n + b] != ' ' and fw[n + b] != ']' and fw[n + b] != ',':
                    i6 += g.b_v() + g.c_v()
                    b += 1
                    if i6 > 146:
                        i6 -= g.b_v() + g.c_v()
                if fw[n + b] == ']':
                    k += g.b_v()
                if i6 + k > 146:
                    k += i6
            k += i5
            if k > 146:
                if ag.ch != -999 and m == 2:
                    break
                i = i3
                k = i5
                if m == 0:
                    i2 = n
                elif m != 1 and m == 2:
                    # 3 lines are full: drop the first line and start drawing again
                    str_ = fw[i2:]
                    ag.fw[paramInt1] = str_
                    i1 -= i2
                    m = n = 0
                    j_ = i4
                    k = 0
                    continue
                m += 1
                j_ += 16
            if n == 0:
                ag.bb.R_I(paramInt1 + 1)
            if i == i3 and fw[n] == ' ':
                n += 1
            if len(fw) >= n + 1:
                x.a_TIII(fw[n:n + 1], i, j_, 0)
            i += i5
            n += 1
        if 0 == paramInt3:
            ag.fA[paramInt1] = n
            ag.fx[paramInt1] = i
            ag.fy[paramInt1] = j_
            ag.fz[paramInt1] = k
            ag.fB[paramInt1] = i2
            ag.fC[paramInt1] = m
        return True

    def aU(self):  # e.java:2374-2394  (screen 29: difficulty Hard / Normal)
        arrayOfInt = [ag.dd - 80 + ag.db, ag.de - 60 + ag.dc]
        ag.ep = i16(ag.cM[1])
        for b in range(2):
            if ag.cM[1] == b:
                x.a_Lg(ag.bw)
                bool_ = True
            else:
                x.a_Lg(ag.bu)
                bool_ = False
            self.a_IIIIZ(arrayOfInt[0], arrayOfInt[1] + b * 25, 160, 20, bool_)
            self.b_TII(ae.aX[b], arrayOfInt[1] + 1 + b * 25 - 1, 15)
        x.a_Lg(ag.bu)
        self.a_IIIIZ(arrayOfInt[0], ag.de + ag.dc, 160, 80, False)
        for b in range(3):
            self.b_TII(ae.aY[ag.cM[1]][b], ag.de + 10 + b * 20, 17)

    def e_I(self, paramInt):  # e.java:3465-3531  (item record -> cX / cY / cZ)
        arrayOfByte = bytearray(16)
        if paramInt < 100:
            return
        if paramInt < 300:
            if ag.cU is None:
                ag.cU = ag.v_I(47)
            cU = ag.cU
            i = 9 + (paramInt - 101) * 23
            b = 0
            while b < 15:
                arrayOfByte[b] = cU[i + b] & 0xFF
                if arrayOfByte[b] == 0:
                    break
                b += 1
            ag.cX.a = ag.a_ABII(arrayOfByte, 0, b)
            ag.cX.b = i8(cU[i + 15])
            ag.cX.c = i8(cU[i + 15 + 1])
            ag.cX.d = i8(cU[i + 15 + 2])
            ag.cX.e = i8(cU[i + 15 + 3])
            ag.cX.f = i8(cU[i + 22])
            if ag.bV != 2:
                ag.cU = None
                return
        elif paramInt < 500:
            if ag.cV is None:
                ag.cV = ag.v_I(51)
            cV = ag.cV
            i = 10 + (paramInt - 301) * 24
            b = 0
            while b < 15:
                arrayOfByte[b] = cV[i + b] & 0xFF
                if arrayOfByte[b] == 0:
                    break
                b += 1
            ag.cY.a = ag.a_ABII(arrayOfByte, 0, b)
            ag.cY.b = i8(cV[i + 15])
            ag.cY.c = ag.a_BB(cV[i + 16], cV[i + 17])
            ag.cY.d = i8(cV[i + 18])
            ag.cY.e = cV[i + 19] & 0xFF
            ag.cY.f = i8(cV[i + 20])
            ag.cY.g = i8(cV[i + 22])
            ag.cY.h = cV[i + 23] & 0xFF
            if ag.bV != 2:
                ag.cV = None
                return
        else:
            if ag.cW is None:
                ag.cW = ag.v_I(49)
            cW = ag.cW
            i = 9 + (paramInt - 501) * 27
            b = 0
            while b < 15:
                arrayOfByte[b] = cW[i + b] & 0xFF
                if arrayOfByte[b] == 0:
                    break
                b += 1
            ag.cZ.a = ag.a_ABII(arrayOfByte, 0, b)
            ag.cZ.b = i8(cW[i + 15])
            ag.cZ.c = ag.a_BB(cW[i + 16], cW[i + 17])
            ag.cZ.d = i8(cW[i + 18])
            ag.cZ.e = ag.a_BB(cW[i + 19], cW[i + 20])
            ag.cZ.f = i8(cW[i + 21])
            ag.cZ.g = cW[i + 26] & 0xFF
            if ag.bV != 2:
                ag.cW = None

    def T_I(self, paramInt):  # e.java:3533-3545  (stat cursor: 0 = erase, 1 = draw)
        if ag.cz.J > 0:
            if paramInt != 0:
                c = 255 if F11 else 1   # DECOMP-FIX F11: decompiled `true` (= 1) as a colour
            else:
                c = 0
            self.a_IIIIIII(ag.eM + 144, ag.eN + 97 + 20 * ag.cM[1] + 11, 14, 18, c, c, c)

    def p_v(self):  # e.java:3547-3560  (exp table of the hero level from edat 45)
        arrayOfByte = ag.v_I(45)
        j_ = 40
        if ag.cz.l > 190:
            j_ = 200 - ag.cz.l << 2
        k = j_ // 4
        arrayOfInt = [0] * k
        i = 4 * (ag.cz.l - 1) + 2
        for b in range(k):
            o = i + b * 4
            arrayOfInt[b] = i32((arrayOfByte[o + 3] & 0xFF) << 24 | (arrayOfByte[o + 2] & 0xFF) << 16
                                | (arrayOfByte[o + 1] & 0xFF) << 8 | arrayOfByte[o] & 0xFF)
        return arrayOfInt

    def bf_v(self):  # e.java:3283-3364  (Game Menu carousel, 4 animation frames per step)
        cM = ag.cM
        s = ag.cK
        if ag.ct[27] is None:
            self.F_v()
        dd = ag.dd
        arrayOfInt1 = [dd - 44 + 0] * 4
        arrayOfInt2 = [164, 180, 188, 166]
        arrayOfInt3 = [dd - 44 + 0] * 4
        arrayOfInt4 = [244, 230, 220, 244]
        arrayOfInt5 = [dd - 63 - 5 + 0] * 4
        arrayOfInt6 = [200, 232, 185, 204]
        i = dd - 60
        if ag.ck == 2:
            if ag.cL == 1:
                for arr in (arrayOfInt1, arrayOfInt2, arrayOfInt3, arrayOfInt4, arrayOfInt5, arrayOfInt6):
                    arr[1], arr[2] = arr[2], arr[1]
                ag.cK = i16(ag.cK + 1)
                if ag.cK == 3:
                    cM[1] = cM[1] + 1
                    if _inc_cmp(cM[1]) >= ag.cN - 1:
                        cM[2] = 0
                        cM[1] = 0
                    ag.I_v()
                elif ag.cK > 3:
                    ag.ck = 0
                    ag.cL = 0
                    ag.cK = 0
            elif ag.cL == -1:
                ag.cK = i16(ag.cK + 1)
                if ag.cK == 3:
                    cM[1] = cM[1] - 1
                    if _dec_cmp(cM[1]) < 0:
                        cM[1] = ag.cN - 1 - 1
                    ag.I_v()
                elif ag.cK > 3:
                    ag.ck = 0
                    ag.cL = 0
                    ag.cK = 0
        self.a_MIIIIII(ag.ct[7], 0, 0, ag.bZ.a, ag.bZ.b, 0, 0)
        self.b_TII(ag.fT[cM[0]], 2 - ag.dc, 0)
        if ag.gl is None or ag.gm != cM[1]:
            ag.gl = self.d_T(ag.bA.a_I(66 + cM[1]))
            ag.gm = cM[1]
        if ag.gl is not None:
            ag.a_IIIIMII(i, 60, 117, 90, ag.gl, 0, 0)
        ag.a_IIIIMII(arrayOfInt1[s], arrayOfInt2[s], 89, 20, ag.ct[27], 0, 0)
        ag.a_IIIIMII(arrayOfInt1[s] + 22, arrayOfInt2[s] + 5, 62, 11, ag.ct[29], 0,
                     11 * (4 if cM[1] == 0 else (cM[1] - 1)))
        ag.a_IIIIMII(arrayOfInt3[s], arrayOfInt4[s], 89, 20, ag.ct[27], 0, 0)
        ag.a_IIIIMII(arrayOfInt3[s] + 22, arrayOfInt4[s] + 5, 62, 11, ag.ct[29], 0,
                     11 * (0 if cM[1] == 4 else (cM[1] + 1)))
        ag.a_IIIIMII(arrayOfInt5[s], arrayOfInt6[s], 127, 29, ag.ct[26], 0, 0)
        ag.a_IIIIMII(arrayOfInt5[s] + 22 + 2, arrayOfInt6[s] + 5 + 1, 94, 18, ag.ct[28], 0, 18 * cM[1])
        if ag.ck != 2 and ag.cK == 0:
            ag.a_IIIIMII(dd - 5 + ag.db, arrayOfInt6[s] - 6 - 5 - ag.dr % 3 * 2, 16, 10, ag.ct[17], 20, 0)
            ag.a_IIIIMII(dd - 5 + ag.db, arrayOfInt6[s] + 29 + ag.dr % 3 * 2, 16, 10, ag.ct[17], 20, 10)
        if ag.dr > 100:
            ag.dr = 32
        else:
            ag.dr += 1
        ag.h_II(-1, 2)

    # ---- Missions: lords (1), missions (2), description (3), briefing (4) ------------------

    def aH(self):  # e.java:1229-1238  (mission description, 6 lines per page)
        self.a_IIIIZ(ag.dd - 100 + ag.db, ag.de - 80, 200, 40, False)
        self.b_TII(ag.dl, ag.de - 80, 30)
        self.b_TII(ag.dn, ag.de - 60, 30)
        self.a_IIIIZ(ag.dd - 110, ag.de - 30, 220, 119, False)
        for b in range(6):
            if ag.dq[0] >= ag.cM[2] * 6 + b:
                ag.a_IIT(ag.dd - 100 + ag.db, ag.de - 28 + b * 20 + ag.dc, ag.dp[0][ag.cM[2] * 6 + b])
        self.a_IIIZ(ag.cM[2] + 1, idiv(ag.dq[0], 6) + 1, ag.de + 110, True)

    def aI(self):  # e.java:1246-1250  (briefing: portraits + empty speech boxes)
        self.b_I(ag.dB[ag.dm])
        self.q_I(1)
        self.R_I(3)

    def h_v(self):  # e.java:1252-1264  (talk in the map: portrait bottom-left)
        if (ag.dK & 0x1) != 0:
            i = 0 + ag.dC.e
        else:
            i = 38 + ag.cz.aB
        j_ = ag.bY.b - 46 - 4
        self.a_IIIIZ(2 + ag.db, j_ + ag.dc, 48, 48, True)
        j_ += 1
        self.a_TIIIIII(ag.bB.a_I(i), 3 + ag.db, j_ + ag.dc, 46, 46, 0, 0)
        self.aT()
        self.q_I(1)

    def i_v(self):  # e.java:1266-1361  (dialogue typewriter: dG 0 briefing, 1 map talk, 2 general)
        arrayOfByte1 = [2, 3, 5]
        arrayOfByte2 = [2, 1, 1]
        if ag.bV == 5 and ag.ch != -6:
            ag.ch = -999
        x.a_Lg(ag.bu)
        if ag.ch == -6:
            ag.dS = 1
            ag.dQ = i16(ag.dq[ag.dR])
            ag.dK = i16(arrayOfByte1[ag.dG])
        if ag.dS > 0:
            ag.dS = i16(ag.dS - 1)
            if ag.ch != -999:
                ag.dS = 0
            if ag.dS < 1:
                if ag.dQ >= ag.dq[ag.dR]:
                    if ag.dK >= arrayOfByte1[ag.dG]:
                        ag.ck = 1
                        if ag.dG != 0:
                            if ag.dG == 1:
                                ag.bV = 3
                                return
                            if ag.cr != 0:
                                self.w_I(2)
                                self.F_v()
                                ag.cM[0] = 0
                                ag.cN = ae.v[ag.cM[0]]
                                ag.dE = ag.fU
                                ag.bV = 2
                                ag.cL = 0
                                ag.cK = 0
                                ag.ck = 1
                                self.L_v()
                                return
                            ag.co = 1
                            ag.cn = 5
                            ag.bV = 3
                            return
                        self.y_v()
                        return
                    ag.dP = 0
                    ag.dQ = 0
                    if 0 == ag.dG:
                        ag.dR = i16(ag.dR + 1 & 0x1)
                    ag.ao()
                    self.z_I(ag.dI + ag.dK - 1)
                    if ag.dG != 0:
                        self.h_v()
                        return
                    self.aS()
                    return
                ag.dP = i16(ag.dP + 1)
                ag.dQ = i16(ag.dQ + 1)
                ag.dO = 0
                ag.dN = ag.dL[ag.dR]
                if ag.dP > arrayOfByte2[ag.dG]:
                    ag.dP = i16(arrayOfByte2[ag.dG])
                    for b in range(20):
                        if b < ag.dq[ag.dR]:
                            ag.dp[ag.dR][b] = ag.dp[ag.dR][b + 1]
                    if ag.dG != 0:
                        self.aT()
                        return
                    self.aS()
                    return
        else:
            if ag.ch == -5:
                ag.dQ = i16(ag.dQ + arrayOfByte2[ag.dG] - ag.dP)
                ag.dP = i16(arrayOfByte2[ag.dG])
                ag.dO = 29
                if ag.dG != 0:
                    self.aT()
                else:
                    self.aS()
                ag.dS = 3
                return
            line = ag.dp[ag.dR][ag.dP]
            str_ = line[ag.dO:]
            if len(str_) != 0 and ord(str_[0]) > 0:
                ag.dO = i16(ag.dO + 1)
                x.a_TIII(str_[0:1], ag.dN + ag.db, ag.dM[ag.dR] + 16 * ag.dP + ag.dc, 0)
                ag.dN = i16(ag.dN + 9)
                return
            if ag.dQ >= ag.dq[ag.dR]:
                ag.dS = 15
                return
            ag.dS = 1

    def aS(self):  # e.java:2174-2205  (briefing: both speech boxes)
        x.a_Lg(ag.bu)
        self.R_I(2 if ag.dR != 0 else 1)
        dp, dL, dM = ag.dp, ag.dL, ag.dM
        if ag.dR != 0:
            for b in range(3):
                ag.c_IIT(dL[0] + ag.db, dM[0] + 16 * b + ag.dc, dp[0][b])
        else:
            for b in range(ag.dP):
                if dp[0][b] is not None:
                    ag.c_IIT(dL[0] + ag.db, dM[0] + 16 * b + ag.dc, dp[0][b])
            if dp[0][ag.dP] is not None:
                str_ = dp[0][ag.dP][0:min(ag.dO, len(dp[0][ag.dP]))]
                ag.c_IIT(dL[0] + ag.db, dM[0] + 16 * ag.dP + ag.dc, str_)
        if ag.dK > 1:
            if ag.dR != 0:
                for b in range(ag.dP):
                    if dp[1][b] is not None:
                        ag.c_IIT(dL[1] + ag.db, dM[1] + 16 * b + ag.dc, dp[1][b])
                if dp[1][ag.dP] is not None:
                    str_ = dp[1][ag.dP][0:min(ag.dO, len(dp[1][ag.dP]))]
                    ag.c_IIT(dL[1] + ag.db, dM[1] + 16 * ag.dP + ag.dc, str_)
                    return
            else:
                for b in range(3):
                    ag.c_IIT(dL[1] + ag.db, dM[1] + 16 * b + ag.dc, dp[1][b])

    def aT(self):  # e.java:2207-2214  (map talk: one speech box at the bottom)
        self.a_IIIIZ(54 + ag.db, ag.bY.b - 40 + ag.dc, ag.bY.a - 56, 38, True)
        x.a_Lg(ag.bu)
        for b in range(ag.dP):
            ag.c_IIT(ag.dL[0] + ag.db, ag.dM[0] + 16 * b + ag.dc, ag.dp[0][b])
        str_ = ag.dp[0][ag.dP][0:ag.dO]
        ag.c_IIT(ag.dL[0] + ag.db, ag.dM[0] + 16 * ag.dP + ag.dc, str_)

    def bi_v(self):  # e.java:3569-3603  (missions of lord dk -> dz / dA / dB, list dE = dA)
        from pow.game.structs import an
        i = 0
        ag.cg = ag.ds[ag.dk]
        ag.dl = ag.dt[ag.dk]
        arrayOfByte1 = ag.v_I(50)
        ag.cN = ag.dv[ag.dk]
        i = 11 * ag.du[ag.dk] + 11
        arrayOfByte2 = ag.v_I(55)
        for b in range(ag.cN):
            if ag.dz[b] is None:
                ag.dz[b] = an()
            dz = ag.dz[b]
            dz.a = ag.b_B(arrayOfByte1[i])
            dz.b = ag.b_B(arrayOfByte1[i + 1])
            dz.c = ag.b_B(arrayOfByte1[i + 2])
            dz.d = ag.b_B(arrayOfByte1[i + 3])
            dz.e = ag.b_B(arrayOfByte1[i + 4])
            dz.f = ag.b_B(arrayOfByte1[i + 5])
            dz.g = ag.b_B(arrayOfByte1[i + 6])
            dz.h = ag.b_B(arrayOfByte1[i + 7])
            dz.i = i16(arrayOfByte1[i + 8] & 0xFF | i8(arrayOfByte1[i + 9]) & 0xFF00)
            dz.j = ag.b_B(arrayOfByte1[i + 10])
            i += 11
            j_ = 3 + (dz.a - 1) * 15
            b1 = 14
            for b2 in range(14):
                if arrayOfByte2[j_ + b2] == 0:
                    b1 = b2
                    break
            ag.dA[b] = ag.a_ABII(arrayOfByte2, j_, j_ + b1)
            ag.dB[b] = i8(arrayOfByte2[17 + (dz.a - 1) * 15])
        ag.dE = ag.dA

    # ---- Visiting: generals (19 list, 20 talk) ---------------------------------------------

    def aN(self):  # e.java:1694-1748  (generals: Name / Points, 4 per page)
        arrayOfString = ["Name", "Points"]
        i = idiv(ag.bZ.a - 208, 2) + 2
        j_ = i + 134 + 10
        k = ag.bY.b - 20 - 20 + 10
        m = 20 + idiv(k - 177, 2) + 2
        n = m
        i1 = ag.cM[1] % 4
        i2 = ag.cM[1] // 4
        ag.fp[1] = i16(i2 + 1)
        i2 *= 4
        self.a_IIIIZ(i, n, 130, 22, False)
        self.a_IIIIZ(j_, n, 60, 22, False)
        x.a_Lg(ag.bu)
        ag.b_IIT(i + 65, n + 1, arrayOfString[0])
        ag.b_IIT(j_ + 30, n + 1, arrayOfString[1])
        n += 31
        for b in range(4):
            if b == i1:
                bool_ = True
                x.a_Lg(ag.bw)
            else:
                bool_ = False
                x.a_Lg(ag.bu)
            self.a_IIIIZ(i, n, 130, 22, bool_)
            self.a_IIIIZ(j_, n, 60, 22, bool_)
            if i2 < ag.cN:
                if ag.fu != 0:
                    str_ = ag.fr.b_II(ag.fn[2][i2] - 1, 0)
                else:
                    str_ = ag.fr.b_II(ag.fn[0][i2] - 1, 0)
                ag.b_IIT(i + 65, n + 1, str_)
                if ag.fu != 0:
                    b1 = 0
                    while b1 < ag.fo and ag.fn[2][i2] != ag.fn[0][b1]:
                        b1 += 1
                    if b1 < ag.fo:
                        str_ = "" + str(ag.fn[1][b1])
                    else:
                        str_ = "0"
                else:
                    str_ = "" + str(ag.fn[1][i2])
                ag.b_IIT(j_ + 30, n + 1, str_)
            i2 += 1
            n += 31
        n += 6
        self.a_IIIZ(ag.fp[1], ag.fp[0], n, True)

    def aO(self):  # e.java:1750-1802  (general talk: type the lines gf[], then popups 14 / 16)
        if ag.dS > 0:
            ag.dS = i16(ag.dS - 1)
            if ag.ch != 0 and ag.dS > 3:
                ag.dS = 3
            if 0 == ag.dS:
                ag.fD += 1
                if ag.fD <= 3:
                    ag.fw[ag.fD & 0x1] = ag.gf[ag.fD - 1]
                    ag.fA[ag.fD & 0x1] = 0
                    return
                if ag.fD == 4:
                    ag.cS.e_I(14)
                    ag.fA[1] = 0
                    return
                if ag.fD < 7:
                    ag.fw[ag.fD & 0x1] = ag.gf[ag.fD - 2]
                    ag.fA[ag.fD & 0x1] = 0
                    return
                ag.fs.a_v()
                ag.fs = None
                ag.fr.a_v()
                ag.fr = None
                ag.cS.e_I(16)
                return
        else:
            if ag.fD >= 10:
                ag.fD -= 10
                i = ag.fD & 0x1
                ag.fA[i] = len(ag.fw[i])
                j_ = 0
            else:
                i = ag.fD & 0x1
                j_ = ag.fA[i]
            if ag.fD != 4:
                e.a_III(i, j_, 0)
                if len(ag.fw[i]) <= ag.fA[i] + 1:
                    if ag.ch != 0:
                        ag.dS = 5
                        return
                    ag.dS = 15

    def bg_v(self):  # e.java:3366-3393  (open the talk with general cM[1])
        # the decompiler shows `j = 2;` as a field write; it is the local j declared below
        if ag.fu != 0:
            j_ = 2
            b = 0
            while b < ag.fo and ag.fn[0][b] != ag.fn[2][ag.cM[1]]:
                b += 1
            ag.fH = i16(b)
            ag.fv = i16(ag.cM[1])
        else:
            j_ = 0
            ag.fH = i16(ag.cM[1])
        i = ag.fn[j_][ag.cM[1]] - 1
        self.B_I(ag.fn[j_][ag.cM[1]])
        ag.ft = ag.fr.b_II(i, 0)
        j_ = ag.fr.a_II(i, 9)
        k = ag.fr.a_II(i, 8)
        i = ag.fn[1][ag.fH]
        ag.fE = k
        ag.fF = j_
        if e.a_II(i, j_):
            ag.fw[0] = ""
            ag.fw[1] = ag.gf[0]
            ag.fA[1] = 0
            ag.fA[0] = 0
            ag.fD = 1
            return True
        return False

    @staticmethod
    def a_II(paramInt1, paramInt2):  # e.java:3395-3430  (greeting lines of the general -> gf[])
        from pow.game.al import al
        if ag.fs is not None:
            ag.fs.a_v()
            ag.fs = None
        ag.fs = al("/" + ag.bE.a_I(62))
        if 0 <= paramInt1 <= 100 and ag.fs is not None:
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
                if len(ag.fs.a_I(paramInt1)) > 0:
                    str_ = ag.ft if (b3 & 0x1) != 0 else ag.cz.k
                    ag.gf[b3 + b2] = "[" + str_ + "] " + ag.fs.a_I(paramInt1) + " "
                    paramInt1 += 1
                else:
                    return False
            return True
        return False

    @staticmethod
    def b_II(paramInt1, paramInt2):  # e.java:3432-3463  (add paramInt2 friendship to general paramInt1)
        from pow.game.d import d
        b = 0
        while b < ag.fo and ag.fn[0][b] != paramInt1:
            b += 1
        if b == ag.fo:
            if paramInt2 > 0:
                d_ = d("/" + ag.bE.a_I(52))
                for b1 in range(44):
                    i = d_.a_II(b1, 0)
                    if i == paramInt1:
                        ag.fn[0][b] = i16(paramInt1)
                        ag.fo = i16(ag.fo + 1)
                        ag.fn[1][b] = i16(ag.fn[1][b] + paramInt2)
                        break
        else:
            ag.fn[1][b] = i16(ag.fn[1][b] + paramInt2)
            if ag.fn[1][b] > 200 or 0 == ag.fn[1][b]:
                while b < ag.fo:
                    ag.fn[0][b] = ag.fn[0][b + 1]
                    ag.fn[1][b] = ag.fn[1][b + 1]
                    b += 1
                ag.fo = i16(ag.fo - 1)
            elif ag.fn[1][b] >= 100:
                ag.fn[1][b] = 100
                return 1
        return 0

    def o_v(self):  # e.java:3208-3281  (gift of the general after the talk -> fJ, cT[0])
        arrayOfShort = [[[500, 800, 900, 960, 990, 995, 998], [60, 61, 91, 92, 392, 892, 992],
                         [100, 600, 900, 930, 990, 995, 996], [1, 2, 5, 305, 310, 410, 910]],
                        [[1, 101, 106, 606, 609, 610, 910], [30, 31, 91, 92, 592, 892, 992],
                         [300, 360, 860, 960, 961, 991, 996], [1, 2, 5, 10, 40, 100, 200]]]
        cz = ag.cz
        if self.C_I(100) < ag.fn[1][ag.fH]:
            i = self.C_I(1000)
            ag.fJ = 0
            while ag.fJ < 7 and i >= arrayOfShort[ag.dC.f][ag.fI][ag.fJ]:
                ag.fJ = i16(ag.fJ + 1)
            ag.cS.l[4] = ""
            v = ag.fJ
            if v == 0:
                i = self.p_I(0)
                if cz.W[i - 1] < 10:
                    str_ = ag.e_II(54, i - 1)
                    cz.W[i - 1] = cz.W[i - 1] + 1
                    if cz.W[i - 1] == 1:
                        ag.cS.l[4] = "Skill :"
                        ag.cT[0] = str_
                        return
                    ag.cS.l[4] = "Skill up :"
                    ag.cT[0] = str_
                    return
            elif v == 1:
                if cz.m < 10000:
                    cz.m += 1
                    ag.cT[0] = ae.aR[0]
                    return
            elif v == 2:
                if cz.n < 10000:
                    cz.n += 1
                    ag.cT[0] = ae.aR[1]
                    return
            elif v == 3:
                if cz.o < 25000:
                    cz.o += 5
                    ag.cT[0] = ae.aR[2]
                    return
            elif v == 4:
                if cz.q < 20000:
                    cz.q += 3
                    ag.cT[0] = ae.aR[3]
                    return
            elif v == 5:
                cz.F += 10
                ag.cT[0] = ae.aR[4]
                return
            elif v == 6:
                if self.k_II(ag.bc.P_I(4), 1) != 0:
                    ag.cT[0] = ag.cX.a
                    ag.cS.l[4] = "Item Acquired!"
                    return
            else:
                i = self.C_I(11)
                if self.k_II(i + 1, 1) != 0:
                    ag.cT[0] = ae.aN[i]
                    ag.cS.l[4] = "Item Acquired!"
                    return
        ag.fJ = 8

    @staticmethod
    def bh_v():  # e.java:3562-3567
        from pow.game.d import d
        ag.fp[0] = i16(idiv(ag.cN - 1, 4) + 1)
        if ag.fr is None:
            ag.fr = d("/" + ag.bE.a_I(46))
        return False

    def n_v(self):  # e.java:2938-2972  (popup extras on the map: experience bars of popups 11 / 12)
        i = 0
        if ag.cS.b_ == 11:
            i = self.p_II(ag.ea, 0)
            if 0 == i and 0 == ag.cS.e:
                ag.ea = i16(ag.ea + 1)
        elif ag.cS.b_ == 12:
            i = self.p_II(ag.ea, 1)
            if 0 == i and 0 == ag.cS.e:
                ag.ea = i16(ag.ea + 1)
        if i != 0 and 0 == ag.cS.e:
            if i == 1:  # the bar is full: level up
                ag.dZ[0] = 0
                ag.dZ[1] = i16(ag.dZ[1] - 100)
                if ag.dZ[1] < 0:
                    ag.dZ[1] = 0
                ag.dZ[2] = i16(ag.dZ[2] - 100)
                ag.ea = 0
                ag.cS.e = 1
                ag.cS.f = 20
                ag.cS.g = 12
                ag.cz.l += 1
                ag.cz.J += 3
                ag.cT[0] = "Level Up : Lv " + str(ag.cz.l)
                ag.cS.l[5] = ag.cT[0]
                ag.cS.j = 1
                return
            if ag.cS.d > 100:
                ag.cS.d = 16

    def p_II(self, paramInt1, paramInt2):  # e.java:2974-3017  (experience bar; 1 = full, 2 = done)
        arrayOfInt = [[ag.k_III(115, 142, 140), ag.k_III(181, 178, 181), 16777215],
                      [ag.k_III(99, 0, 0), ag.k_III(181, 0, 0), ag.k_III(247, 73, 0)],
                      [ag.k_III(0, 65, 255), ag.k_III(0, 146, 255), ag.k_III(0, 255, 173)],
                      [ag.k_III(247, 73, 0), ag.k_III(255, 162, 0), ag.k_III(255, 223, 0)]]
        if ag.bV == 3:
            ag.dc = i16(ag.dc - 30)
        y = ag.de + 37 + ag.dc + 20
        arrayOfAc = [ac(ag.dd - 51, y, 102, 7),
                     ac(ag.dd - 50, y, ag.dZ[0], 7),
                     ac(ag.dd - 50 + ag.dZ[0], y, ag.dZ[1] - ag.dZ[0], 7),
                     ac(ag.dd - 50 + ag.dZ[1], y, 0, 7)]
        if ag.bV == 3:
            ag.dc = i16(ag.dc + 30)
        b3 = 0
        b2 = 4 if paramInt2 != 0 else 3
        if ag.dZ[paramInt2] + paramInt1 * 4 > ag.dZ[paramInt2 + 1]:
            i = ag.dZ[paramInt2 + 1] - ag.dZ[paramInt2]
            b3 = 2
        else:
            i = paramInt1 * 4
        if ag.dZ[paramInt2] + i > 100:
            arrayOfAc[paramInt2 + 2].c = 100 - ag.dZ[paramInt2]
            b3 = 1
        else:
            arrayOfAc[paramInt2 + 2].c = i
        ag.a_LacI(arrayOfAc[0], 0)
        arrayOfAc[0].a += 1
        arrayOfAc[0].c = 100
        for b1 in range(b2):
            if arrayOfAc[b1].c > 0:
                for b in range(3):
                    arrayOfAc[b1].b += 1
                    arrayOfAc[b1].d -= 2
                    ag.a_LacI(arrayOfAc[b1], arrayOfInt[b1][b])
        return b3
