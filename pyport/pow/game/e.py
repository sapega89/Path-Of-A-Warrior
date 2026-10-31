"""e.java - menu screens (bb). Literal port, Phase 0 subset:
Main Menu (cM[0] == 5) and the Game Menu carousel (cM[0] == 0), with the full key routing
(a(), aB/aC/aD/aE = up/down/left/right, b() = fire, aF() = back).
Screens of later phases raise NotPorted.
"""
import config
from pow.game import ae
from pow.game.ag import ag, not_ported
from pow.game.x import x
from pow.midp.jint import i16

F6 = config.DECOMP_FIX["F6"]


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
                if v in (4, 7, 15, 16, 17, 18, 20, 21, 22, 23, 24) or (v in (8, 14) and ag.da != 0):
                    not_ported("e.a(0) screen cM[0]=%d" % v)

    def a_v(self):  # e.java:207-302  (keys of the menus)
        if ag.bj:
            ag.ed = -1
        v = ag.cM[0]
        if v == 4:
            return
        if v == 7:
            not_ported("e.a() name entry (cM[0]=7)")
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
            not_ported("e.T(int) (stat points)")
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
            not_ported("e.T(int) (stat points)")
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
            not_ported("e.b() -> screen cM[0]=%d" % cM[0])
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
                not_ported("e.b() New Game (at, au)")
        elif v in (1, 3, 8, 10, 11, 14, 15, 17, 25, 29):
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
