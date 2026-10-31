"""e.java - menu screens (bb). Literal port, Phase 0 subset:
Main Menu (cM[0] == 5) and the Game Menu carousel (cM[0] == 0), with the full key routing
(a(), aB/aC/aD/aE = up/down/left/right, b() = fire, aF() = back).
Screens of later phases raise NotPorted.
"""
import config
from pow.game import ae
from pow.game.ag import ag, not_ported
from pow.game.at import at
from pow.game.x import x
from pow.midp.jint import i8, i16, i32, idiv

F6 = config.DECOMP_FIX["F6"]
F11 = config.DECOMP_FIX["F11"]


def _dec_cmp(v):
    """DECOMP-FIX F6: `cM[i] = cM[i] - 1; if (cM[i] - 1 < 0)` is a broken `if (--cM[i] < 0)`."""
    return v if F6 else v - 1


def _inc_cmp(v):
    """DECOMP-FIX F6: `cM[i] = cM[i] + 1; if (cM[i] + 1 >= n)` is a broken `if (++cM[i] >= n)`."""
    return v if F6 else v + 1


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
            elif v == 6:
                self.aK()
            elif v == 7:
                self.aL()
                self.aM()
            elif v in (8, 14):
                self.O_I(1)
            elif v == 29:
                self.aU()
            else:
                not_ported("e.a(1) screen cM[0]=%d" % v)
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
                    not_ported("e.a(2) cM[0]=4 (briefing)")
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
                if v in (4, 15, 16, 17, 18, 20, 21, 22, 23, 24):
                    not_ported("e.a(0) screen cM[0]=%d" % v)

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
            not_ported("e.aW() (blacksmith)")
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
                not_ported("ar.c(0) (quick slot)")
        elif ch == 35:
            if ag.cM[0] == 18:
                not_ported("ar.c(1) (quick slot)")
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

    def aD(self):  # e.java:482-584  (LEFT) - Phase 0: Main Menu; other screens later
        cM = ag.cM
        v = cM[0]
        if v == 5:
            ag.ck = 1
            cM[1] = cM[1] - 1
            if _dec_cmp(cM[1]) < 0:
                cM[1] = 8
                return
            return
        if v == 6:
            ag.cz.aB = ag.cz.aB - 1 & 0x3
            ag.ck = 1
            return
        if v in (1, 3, 9, 15, 16, 17, 18, 19, 25, 28):
            not_ported("e.aD() cM[0]=%d" % v)

    def aE(self):  # e.java:586-686  (RIGHT) - Phase 0: Main Menu; other screens later
        cM = ag.cM
        v = cM[0]
        if v == 5:
            ag.ck = 1
            cM[1] = cM[1] + 1
            if _inc_cmp(cM[1]) >= 9:
                cM[1] = 0
                return
            return
        if v == 6:
            ag.cz.aB = ag.cz.aB + 1 & 0x3
            ag.ck = 1
            return
        if v in (1, 3, 9, 15, 16, 17, 18, 19, 25, 28):
            not_ported("e.aE() cM[0]=%d" % v)

    def b_v(self):  # e.java:688-1000  (FIRE)
        cM = ag.cM
        if cM[0] == 9:
            not_ported("e.y(1) (options)")
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
            if cM[0] == 7:
                ag.cz.k = ""
            else:   # 1 3 9 10 12 13 14 15 17 20-24 27 28: later phases
                not_ported("e.b() -> screen cM[0]=%d" % cM[0])
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
                    not_ported("e.b() general visits (cM[0]=19)")
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
                    if ag.dj != 0:
                        not_ported("e.b() continue inside a mission (dj != 0)")
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
        elif v in (1, 3, 10, 11, 15, 17, 25):
            not_ported("e.b() cM[0]=%d" % v)

    def aF(self):  # e.java:1002-1109  (BACK)
        cM = ag.cM
        bool_ = False
        if ae.u[cM[0]] > -1:
            if cM[0] in (14, 15, 16, 17, 18):
                not_ported("e.ar() (save) on back")
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
                        if ag.bW == 3:
                            not_ported("e.aF() back into the map")
                    elif cM[1] == 5:
                        cM[1] = 4
                if ag.cO == 25:
                    cM[1] = 4
                if ag.cO == 27:
                    cM[1] = 3
                    if ag.bW == 3:
                        not_ported("e.aF() back into the map")
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
                not_ported("e.aF() cM[0]=15 (skills)")
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
