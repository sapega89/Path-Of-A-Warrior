"""ar.java - the map / combat engine (bc). Literal port, partial (phase 3 = the map):
the frame loop, the hero's walls and room exits, room scrolling, the HUD of the map and the
pause menu are ported. Everything that only runs with enemies on the map (ez > 0) or for an
attack (config.NO_COMBAT) raises NotPorted: it is the combat of phase 4."""
from pow.game import ae
from pow.game.ag import ag, not_ported
from pow.game.c import c
from pow.game.structs import h
from pow.game.x import x
import config
from pow.midp.jint import i16, idiv

F6 = config.DECOMP_FIX["F6"]


class ar(ag):
    def __init__(self):  # ar.java:2-4
        super().__init__(ag.bs)

    def a_v(self):  # ar.java:6-23  (one tick of the map)
        if ag.cS.b != 0:
            ag.cS.b_v()
            self.L_v()
        elif ag.cR.a != 0:
            self.o_v()
            self.L_v()
        else:
            ag.bd.i_v()
            self.L_v()
            self.aC()
            if not self.gj:
                self.O_I(1)
                return
        self.O_I(0)

    def b_I(self, paramInt):  # ar.java:25-93  (draw the map, its pause menu and popups)
        if paramInt == 1:
            self.K_v()
            for b in range(9):
                for b1 in range(9):
                    ag.eE[b][b1] = 1
            ag.bd.c_v()
            if ag.cR.a != 0:
                ag.cS.b_I(170)
                v = ag.cR.a
                if v == 1:
                    ag.bb.f_v()
                elif v == 2:
                    ag.bb.d_I(0)
                    ag.bb.k_v()
                elif v == 3:
                    ag.bb.j_v()
                elif v == 4:
                    ag.bb.l_v()
            if ag.cS.b != 0:
                ag.cS.c_v()
                ag.bb.n_v()
            return
        if paramInt == 2:
            return
        if ag.cS.b != 0:
            if ag.cS.j != 0:
                ag.cS.c_v()
            ag.bb.n_v()
            return
        if ag.cR.a != 0:
            if ag.cR.b != 0:
                v = ag.cR.a
                if v == 1:
                    ag.cS.b_I(170)
                    ag.bb.f_v()
                elif v == 2:
                    ag.bb.d_I(1)
                elif v == 3:
                    ag.cS.b_I(170)
                    ag.bb.j_v()
                elif v == 4:
                    ag.cS.b_I(170)
                    ag.bb.l_v()
                ag.cR.b = 0
            if ag.cR.a == 2:
                ag.bb.k_v()
                return
        else:
            ag.bd.c_v()

    def o_v(self):  # ar.java:95-247  (keys of the pause menu cR.a: 1 menu, 2 items, 3 options, 4 help)
        arrayOfByte1 = [0, 3, 0, 2, 4, 0, 0]
        arrayOfByte2 = [0, 3, 0, 5, 3, 0, 0]
        v = ag.ch
        blocked = ag.ez > 0 or ag.cr != 0 or ag.eD[0] != 0
        if v in (-1, 50):
            if ag.cR.a in (1, 3):
                ag.cM[1] = ag.cM[1] - 1
                if (ag.cM[1] < 0) if F6 else (ag.cM[1] - 1 < 0):   # DECOMP-FIX F6
                    ag.cM[1] = ag.cN - 1
                if ag.cM[1] == 1 and ag.cR.a == 3 and not ag.df:
                    ag.cM[1] = 0
                if ag.cM[1] == 2 and ag.cR.a == 1 and blocked:
                    ag.cM[1] = ag.cM[1] - 1
                ag.I_v()
                ag.cR.b = 1
            return
        if v in (-2, 56):
            if ag.cR.a in (1, 3):
                ag.cM[1] = ag.cM[1] + 1
                if (ag.cM[1] >= ag.cN) if F6 else (ag.cM[1] + 1 >= ag.cN):   # DECOMP-FIX F6
                    ag.cM[1] = 0
                if ag.cM[1] == 1 and ag.cR.a == 3 and not ag.df:
                    ag.cM[1] = 2
                if ag.cM[1] == 2 and ag.cR.a == 1 and blocked:
                    ag.cM[1] = ag.cM[1] + 1
                ag.I_v()
                ag.cR.b = 1
            return
        if v in (-3, 52):
            if ag.cR.a in (2, 4):
                ag.cM[1] = ag.cM[1] - 1
                if (ag.cM[1] < 0) if F6 else (ag.cM[1] - 1 < 0):   # DECOMP-FIX F6
                    ag.cM[1] = ag.cN - 1
                ag.cR.b = 1
            elif ag.cR.a == 3:
                self.y_I(0)
                ag.cR.b = 1
            return
        if v in (-4, 54):
            if ag.cR.a in (2, 4):
                ag.cM[1] = ag.cM[1] + 1
                if (ag.cM[1] >= ag.cN) if F6 else (ag.cM[1] + 1 >= ag.cN):   # DECOMP-FIX F6
                    ag.cM[1] = 0
                ag.cR.b = 1
            elif ag.cR.a == 3:
                self.y_I(1)
                ag.cR.b = 1
            return
        if v == 42:
            if ag.cR.a == 2:
                ag.ck = ar.c_I(0)
            return
        if v == 35:
            if ag.cR.a == 2:
                ag.ck = ar.c_I(1)
            return
        if v in (-5, 53):
            if ag.cM[0] == 10 and ag.cM[1] == 4:
                ag.cM[0] = 5
                ag.cM[1] = 3
                ag.bW = ag.bV
                ag.bV = 2
                ag.bb.b_v()
                return
            if ag.cR.a == 1:
                if arrayOfByte1[ag.cM[1]] != 0:
                    ag.cR.a = arrayOfByte1[ag.cM[1]]
                    ag.cN = arrayOfByte2[ag.cM[1]]
                    ag.ck = 1
                    ag.cP[0] = i16(ag.cM[1])
                    ag.cQ[0] = i16(ag.cM[2])
                    ag.cM[1] = 0
                    ag.ej = 3
                    return
                w = ag.cM[1]
                if w == 2:
                    if blocked:
                        ag.cS.e_I(7)
                    elif self.ar() != 0:
                        ag.cS.e_I(0)
                elif w == 0:
                    ag.ck = 1
                    ag.ct[10] = None
                    ag.ct[17] = None
                    ag.cR.a = 0
                    self.a__I(-1)
                elif w == 5:
                    ag.cS.e_I(5)
                elif w == 6:
                    ag.cS.e_I(28)
                    ag.ck = 1
                return
            if ag.cR.a == 3:
                self.y_I(1)
                ag.cR.b = 1
                return
            return
        if v == -7:
            ag.ck = 1
            if ag.cR.a == 1:
                ag.ct[10] = None
                ag.ct[17] = None
                ag.cR.a = 0
                self.a__I(-1)
                return
            ag.cR.a = 1
            ag.cM[1] = ag.cP[0]
            ag.cM[2] = ag.cQ[0]
            ag.cN = 7

    @staticmethod
    def c_I(paramInt):  # ar.java:249-261  (assign the potion under the cursor to * / #)
        cz = ag.cz
        if cz.Z[ag.cM[1]].a != 0 and cz.aa[paramInt] != ag.cM[1]:
            if ag.cM[1] == cz.aa[paramInt + 1 & 0x1]:
                i = cz.aa[paramInt]
                cz.aa[paramInt] = cz.aa[paramInt + 1 & 0x1]
                cz.aa[paramInt + 1 & 0x1] = i
            else:
                cz.aa[paramInt] = ag.cM[1]
            return 1
        return 0

    @staticmethod
    def b_v():  # ar.java:263-268
        if ag.cz.p > ag.cz.y:
            ag.cz.p = ag.cz.y
        if ag.cz.r > ag.cz.z:
            ag.cz.r = ag.cz.z

    @staticmethod
    def Q_I(paramInt):  # ar.java:270-272
        return -paramInt if paramInt < 0 else paramInt

    def a_IIIIIIII(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7, paramInt8):  # ar.java:274-282
        i = idiv(paramInt3 + paramInt7, 2)
        j_ = idiv(paramInt4 + paramInt8, 2)
        k = paramInt1 + idiv(paramInt3, 2) - paramInt5 + idiv(paramInt7, 2)
        m = paramInt2 + idiv(paramInt4, 2) - paramInt6 + idiv(paramInt8, 2)
        n = ar.Q_I(k)
        i1 = ar.Q_I(m)
        return n < i and i1 < j_

    # ---- the hero's attacks (phase 4) --------------------------------------------------------

    def c_v(self):  # ar.java:370-408  (hero attack vs. breakable objects)
        not_ported("ar.c() (attack objects)")

    def d_I(self, paramInt):  # ar.java:674-724  (hero attack vs. enemies)
        not_ported("ar.d(int) (attack enemies)")

    def f_v(self):  # ar.java:1196-1200  (turn to the nearest enemy, Hard only)
        not_ported("ar.f() (aim at an enemy)")

    def U_I(self, paramInt):  # ar.java:580-638  (the hero is hit)
        not_ported("ar.U(int) (hero hit)")

    @staticmethod
    def c_LhLh(paramh1, paramh2):  # ar.java:457-468  (distance, rounded)
        j_ = paramh1.a - paramh2.a
        k = paramh1.b - paramh2.b
        m = j_ * j_ + k * k
        j_ = -j_ if j_ < 0 else j_
        k = -k if k < 0 else k
        i = j_ if j_ > k else k
        while i * i < m:
            i += 2
        i -= 1
        if i * i < m:
            i += 1
        return i

    # ---- enemy waves of the room -------------------------------------------------------------

    def d_v(self):  # ar.java:726-741  (spawn the next enemy of the room's wave list eD)
        import config
        if config.NO_ENEMIES:
            # PORT-EXTRA (map without combat): the whole wave list of the room counts as
            # defeated at once, and the room is cleared exactly as when its last enemy dies
            # (ar.java:1326-1332): popup "Stage N Complete", then the exits open.
            # A room whose list holds a general (id < 200, c.java:986-1010: talk + duel) stays
            # closed: the mission is won only by defeating him, which is the combat.
            if any(0 < ag.eD[k] < 200 for k in range(0, 14, 2)):
                return
            if ag.co == 0 and ag.eD[0] != 0:
                for b in range(14):
                    ag.eD[b] = 0
                if ag.cr != 0:
                    ag.co = 4
                    ag.cn = 22
                else:
                    ag.co = 3
                    ag.cn = 5
            return
        if ag.eA < ag.eO[ag.eP].b:
            if ag.eD[0] == 0:
                return
            if (ag.eD[0] >= 200 or ag.eB == 0) and ag.ev != 0:
                i = self.C_I(ag.ev)
                ag.bd.b_IIII(ag.eD[0], ag.eu[i].a, ag.eu[i].b, ag.eu[i].c)
                ag.eD[1] = i16(ag.eD[1] - 1)
                if ag.eD[1] < 1:
                    for b in range(12):
                        ag.eD[b] = ag.eD[b + 2]

    @staticmethod
    def e_I(paramInt):  # ar.java:743-757  (MP cost of skill paramInt; 0 = not enough MP)
        arrayOfByte1 = [5, 6, 7, 10, 15, 7, 10, 10, 8, 9, 10, 5, 6, 7, 9, 12, 20, 20, 20]
        arrayOfByte2 = [3, 4, 5, 3, 4, 3, 3, 5, 3, 4, 5, 3, 4, 5, 5, 6, 5, 5, 5]
        i = 0
        if 12 <= paramInt <= 30:
            i = arrayOfByte1[paramInt - 12] + (ag.cz.W[paramInt - 12] - 1) * arrayOfByte2[paramInt - 12]
        if i > ag.cz.r:
            return 0
        ag.cz.r -= i
        return i

    @staticmethod
    def e_v():  # ar.java:759-767  (direction pressed twice quickly -> run)
        if ag.cs[0] > -1:
            if ag.dh >= 3:
                return 1 if (ag.cs[0] == ag.cs[1] or ag.cs[0] == ag.cs[2] or ag.cs[0] == ag.cs[3]) else 0
            if ag.cs[0] == ag.cs[1] or ag.cs[0] == ag.cs[2]:
                return 1
        return 0

    # ---- walls -------------------------------------------------------------------------------

    def a_LhII(self, paramh, paramInt1, paramInt2):  # ar.java:769-815  (step paramInt1 towards paramInt2 until no wall)
        arrayOfInt1 = [0, 0]
        arrayOfInt2 = [0, 0]
        arrayOfInt3 = [0, 0]
        cE = ag.cE
        n = len(cE.a) - 1
        while True:
            b2 = 0
            if paramInt2 == 2:
                arrayOfInt2[0] = idiv(paramh.b - 20, 27)
                arrayOfInt2[1] = idiv(paramh.b + 6, 27)
                arrayOfInt1[1] = arrayOfInt1[0] = idiv(paramh.a + paramInt1 - 12, 27)
            elif paramInt2 == 6:
                arrayOfInt2[0] = idiv(paramh.b - 20, 27)
                arrayOfInt2[1] = idiv(paramh.b + 6, 27)
                arrayOfInt1[1] = arrayOfInt1[0] = idiv(paramh.a + paramInt1 + 12, 27)
            elif paramInt2 == 4:
                arrayOfInt1[0] = idiv(paramh.a - 12, 27)
                arrayOfInt1[1] = idiv(paramh.a + 12, 27)
                arrayOfInt2[1] = arrayOfInt2[0] = idiv(paramh.b + paramInt1 - 20, 27)
            elif paramInt2 == 0:
                arrayOfInt1[0] = idiv(paramh.a - 12, 27)
                arrayOfInt1[1] = idiv(paramh.a + 12, 27)
                arrayOfInt2[1] = arrayOfInt2[0] = idiv(paramh.b + paramInt1 + 6, 27)
            for b1 in range(2):
                arrayOfInt3[b1] = arrayOfInt2[b1] * cE.b.a + arrayOfInt1[b1]
                if (cE.a[min(cE.f + arrayOfInt3[b1], n)] & 0x1) != 0 or cE.a[min(cE.e + arrayOfInt3[b1], n)] != 0:
                    b2 += 1
            if b2 != 0:
                paramInt1 = ar.t_II(b2, paramInt1)[1]
                if 0 == paramInt1:
                    return 0
                continue
            return paramInt1

    @staticmethod
    def t_II(paramInt1, paramInt2):  # ar.java:817-832  (both one step closer to 0)
        if paramInt1 > 0:
            paramInt1 -= 1
        elif paramInt1 < 0:
            paramInt1 += 1
        if paramInt2 > 0:
            paramInt2 -= 1
        elif paramInt2 < 0:
            paramInt2 += 1
        return [paramInt1, paramInt2]

    def b_LhII(self, paramh, paramInt1, paramInt2):  # ar.java:834-865  (keep inside the room; touching an edge = exit)
        arrayOfShort = [18, 144, 270, 396, 522, 648, 774, 900, 1026, 1152, 1278]
        for b in range(11):
            arrayOfShort[b] = i16(idiv(arrayOfShort[b] * 3, 2))
        h1 = h()
        h1.a = i16(paramh.a + paramInt1)
        h1.b = i16(paramh.b + paramInt2)
        if h1.a < arrayOfShort[ag.cf.a] + 12:
            paramInt1 = arrayOfShort[ag.cf.a] + 12 - paramh.a
            if ag.co == 1:
                ar.X_I(2)
        elif h1.a > arrayOfShort[ag.cf.a + 1] - 12:
            paramInt1 = arrayOfShort[ag.cf.a + 1] - 12 - paramh.a
            if ag.co == 1:
                ar.X_I(4)
        if h1.b < arrayOfShort[ag.cf.b] + 10:
            paramInt2 = arrayOfShort[ag.cf.b] + 10 - paramh.b
            if ag.co == 1:
                ar.X_I(3)
        elif h1.b > arrayOfShort[ag.cf.b + 1] + 10:
            paramInt2 = arrayOfShort[ag.cf.b + 1] + 10 - paramh.b
            if ag.co == 1:
                ar.X_I(1)
        return [paramInt1, paramInt2]

    @staticmethod
    def X_I(paramInt):  # ar.java:867-888  (leave the room through exit paramInt: 1 down 2 left 3 up 4 right)
        if ag.cn < 0 and ag.eO[ag.eP].a[paramInt - 1] != 0:
            ag.cp = i16(paramInt)
            if paramInt == 1:
                ag.eP = i16(ag.eP + idiv(ag.cE.b.a, 7))
            elif paramInt == 2:
                ag.eP = i16(ag.eP - 1)
            elif paramInt == 3:
                ag.eP = i16(ag.eP - idiv(ag.cE.b.a, 7))
            elif paramInt == 4:
                ag.eP = i16(ag.eP + 1)
            for b in range(4):
                ag.ct[21 + b] = None
            ag.cm = 0

    @staticmethod
    def c_LhII(paramh, paramInt1, paramInt2):  # ar.java:890-1014  (slide around a corner: new direction or -1)
        cE = ag.cE
        b1 = 0
        j_ = idiv(paramh.a, 27)
        k = idiv(paramh.b, 27)
        m = j_ + k * cE.b.a
        arrayOfInt1 = [0, 0]
        arrayOfInt2 = [1, 1]
        if paramInt2 == -1:
            h1 = ag.cz.j
        else:
            h1 = ag.ex[paramInt2].b
        if paramInt1 in (0, 6):
            b1 = 1
        elif paramInt1 in (2, 4):
            b1 = -1
        free = lambda q: 0 == (cE.a[cE.f + q] & 0x1) and 0 == cE.a[cE.e + q]
        if paramInt1 in (0, 4):
            i = m + cE.b.a * b1
            if free(i):
                h1.b = 0
                n = j_ * 27 + 8
                if paramh.a > n:
                    if paramh.a - n > 3:
                        h1.a = -3
                    else:
                        h1.a = i16(n - paramh.a)
                elif n - paramh.a > 3:
                    h1.a = 3
                else:
                    h1.a = i16(n - paramh.a)
                return 8
            for b in range(1, 6):
                if j_ + b < cE.b.a:
                    i = m + b
                    if free(i) and arrayOfInt2[0] != 0:
                        i = m + b + cE.b.a * b1
                        if free(i):
                            arrayOfInt1[0] = 1
                    else:
                        arrayOfInt2[0] = 0
                if j_ - b > -1:
                    i = m - b
                    if free(i) and arrayOfInt2[1] != 0:
                        i = m - b + cE.b.a * b1
                        if free(i):
                            arrayOfInt1[1] = 1
                    else:
                        arrayOfInt2[1] = 0
                if arrayOfInt1[0] != 0 and arrayOfInt1[1] != 0:
                    return 6 if paramh.a - j_ * 27 > 8 else 2
                if arrayOfInt1[0] != 0:
                    return 6
                if arrayOfInt1[1] != 0:
                    return 2
        elif paramInt1 in (2, 6):
            i = m + b1
            if free(i):
                h1.a = 0
                n = k * 27 + 20
                if paramh.b > n:
                    if paramh.b - n > 4:
                        h1.b = -4
                    else:
                        h1.b = i16(n - paramh.b)
                elif n - paramh.b > 4:
                    h1.b = 4
                else:
                    h1.b = i16(n - paramh.b)
                return 8
            for b in range(1, 6):
                if k + b < cE.b.b:
                    i = m + b * cE.b.a
                    if free(i) and arrayOfInt2[0] != 0:
                        i = m + b * cE.b.a + b1
                        if free(i):
                            arrayOfInt1[0] = 1
                    else:
                        arrayOfInt2[0] = 0
                if k - b > -1:
                    i = m - b * cE.b.a
                    if free(i) and arrayOfInt2[1] != 0:
                        i = m - b * cE.b.a + b1
                        if free(i):
                            arrayOfInt1[1] = 1
                    else:
                        arrayOfInt2[1] = 0
                if arrayOfInt1[0] != 0 and arrayOfInt1[1] != 0:
                    return 0 if paramh.b - k * 27 > 8 else 4
                if arrayOfInt1[0] != 0:
                    return 0
                if arrayOfInt1[1] != 0:
                    return 4
        return -1

    @staticmethod
    def u_II(paramInt1, paramInt2):  # ar.java:1016-1023  (diagonal step -> straight step)
        arrayOfByte = [[0, 1, 1, 2, 3, 4, 4, 5, 6, 7, 7, 8, 8, 9, 10, 10, 11],
                       [0, 2, 3, 4, 6, 7, 8, 9, 11, 13, 14, 16, 17, 18, 20, 21, 23]]
        if paramInt1 < 0:
            return -arrayOfByte[paramInt2][min(16, -paramInt1)]
        return arrayOfByte[paramInt2][min(16, paramInt1)]

    def a_LhIIII(self, paramh, paramInt1, paramInt2, paramInt3, paramInt4):  # ar.java:1025-1153  (move; returns the direction, -1 blocked, 9 stopped)
        i = 0
        j_ = 0
        if paramInt3 == 8:
            if paramInt4 < 0:
                paramInt1 = ag.cz.j.a
                paramInt2 = ag.cz.j.b
            else:
                paramInt1 = ag.ex[paramInt4].b.a
                paramInt2 = ag.ex[paramInt4].b.b
        else:
            if paramInt1 > 0:
                i = self.a_LhII(paramh, paramInt1, 6)
            elif paramInt1 < 0:
                i = self.a_LhII(paramh, paramInt1, 2)
            if paramInt2 > 0:
                j_ = self.a_LhII(paramh, paramInt2, 0)
            elif paramInt2 < 0:
                j_ = self.a_LhII(paramh, paramInt2, 4)
        u = ar.u_II
        if paramInt3 in (2, 6):
            if 0 == i:
                return -1
        elif paramInt3 in (0, 4):
            if 0 == j_:
                return -1
        elif paramInt3 in (1, 3, 5, 7):
            # diagonal: if one axis is blocked, go straight along the other one
            hx, vy = {1: (2, 0), 3: (2, 4), 5: (6, 4), 7: (6, 0)}[paramInt3]
            if not (i != 0 and j_ != 0):
                if i != 0:
                    paramInt3 = hx
                    i = self.a_LhII(paramh, u(paramInt1, 1), hx)
                elif j_ != 0:
                    paramInt3 = vy
                    j_ = self.a_LhII(paramh, u(paramInt2, 1), vy)
                else:
                    return -1
        elif paramInt3 == 8:
            if paramInt4 == -1:
                h1 = ag.cz.j
            else:
                h1 = ag.ex[paramInt4].b
            i = h1.a
            j_ = h1.b
            if h1.a > 0:
                paramInt3 = 6
            elif h1.a < 0:
                paramInt3 = 2
            elif h1.b > 0:
                paramInt3 = 0
            elif h1.b < 0:
                paramInt3 = 4
        arrayOfInt = self.b_LhII(paramh, i, j_)
        i = arrayOfInt[0]
        j_ = arrayOfInt[1]
        if i != 0 or j_ != 0:
            arrayOfInt = self.a_LhIII(paramh, i, j_, paramInt4)
            i = arrayOfInt[0]
            j_ = arrayOfInt[1]
            if i == 0 and j_ == 0:
                return 9
        paramh.a = i16(paramh.a + i)
        paramh.b = i16(paramh.b + j_)
        return paramInt3

    def a_LhIII(self, paramh, paramInt1, paramInt2, paramInt3):  # ar.java:1155-1194  (do not walk into the hero / enemies)
        b = 0
        h1 = h()
        h1.a = i16(paramh.a + paramInt1)
        h1.b = i16(paramh.b + paramInt2)
        if paramInt3 > -1:
            i = ar.c_LhLh(h1, ag.cz.a[0])
            j_ = ar.c_LhLh(paramh, ag.cz.a[0])
            if i < j_ and i < 20:
                while ar.Q_I(h1.a - ag.cz.a[0].a) <= 27 and ar.Q_I(h1.b - ag.cz.a[0].b) <= 27:
                    ar.t_II(paramInt1, paramInt2)       # (result unused in the original)
                    h1.a = i16(paramh.a + paramInt1)
                    h1.b = i16(paramh.b + paramInt2)
                    b += 1
                    if b > 16:
                        break
        else:
            for b1 in range(ag.ez):
                s = ag.ey[b1]
                if ag.ex[s].f[0] != 3:
                    i = ar.c_LhLh(h1, ag.ex[s].a[0])
                    j_ = ar.c_LhLh(paramh, ag.ex[s].a[0])
                    if i < j_ and i < 20:
                        b = 0
                        while ar.Q_I(h1.a - ag.ex[s].a[0].a) <= 27 and ar.Q_I(h1.b - ag.ex[s].a[0].b) <= 27:
                            ar.t_II(paramInt1, paramInt2)
                            h1.a = i16(paramh.a + paramInt1)
                            h1.b = i16(paramh.b + paramInt2)
                            b += 1
                            if b > 16:
                                break
        return [paramInt1, paramInt2]

    # ---- per-tick updates --------------------------------------------------------------------

    def g_v(self):  # ar.java:1310-1604  (enemy AI)
        if ag.ez > 0:
            not_ported("ar.g() (enemy AI)")

    @staticmethod
    def h_v():  # ar.java:1700-1711  (sort enemies by y)
        if ag.ez != 0:
            for b in range(ag.ez - 1):
                for i in range(b + 1, ag.ez):
                    if ag.ex[ag.ey[b]].a[0].b > ag.ex[ag.ey[i]].a[0].b:
                        s = ag.ey[b]
                        ag.ey[b] = ag.ey[i]
                        ag.ey[i] = s

    def i_v(self):  # ar.java:1713-1729  (pick up dropped items)
        for b in range(ag.cD):
            cC = ag.cC[b]
            if cC.a != 0:
                if ar.c_LhLh(ag.cz.a[0], cC.b) < 20 and self.k_II(cC.a, 1) != 0:
                    ag.ek = 1
                    if 100 < cC.a < 10000:
                        ag.bb.e_I(cC.a)
                        ag.cS.e_I(13)
                    cC.a = 0
                cC.c = i16(cC.c - 1)
                if cC.c < 1:
                    cC.a = 0

    def j_v(self):  # ar.java:1731-1749  (arrows: hit the hero or fly on)
        for b in range(3):
            eC = ag.eC[b]
            if eC.a != 0:
                eC.b[1].a = eC.b[0].a
                eC.b[1].b = eC.b[0].b
                if self.a_IIIIIIII(eC.b[0].a, eC.b[0].b + 8, eC.c, eC.d, ag.cz.a[0].a - 12, ag.cz.a[0].b - 20, 17, 18):
                    if ag.cz.e[0] < 12:
                        ag.bd.d_v()
                        eC.a = 0
                        self.U_I(b - 3)
                    else:
                        self.ac_I(b)
                else:
                    self.ac_I(b)

    def ac_I(self, paramInt):  # ar.java:1751-1772
        e1 = ag.cz.e[1]
        f1 = ag.cz.f[1]
        if e1 in (26, 27):
            if 1 < f1 < 9:
                return
        elif e1 == 28:
            if f1 > 3:
                return
        elif e1 == 29:
            if f1 > 6:
                return
        elif e1 == 30:
            if 3 < f1 < 15:
                return
        ar.ad_I(paramInt)

    @staticmethod
    def ad_I(paramInt):  # ar.java:1774-1793  (move an arrow)
        eC = ag.eC[paramInt]
        eC.g = eC.g + 1
        if eC.g > 22:
            eC.a = 0
            return
        if eC.e == 0:
            eC.b[0].b = i16(eC.b[0].b + 12)
        elif eC.e == 1:
            eC.b[0].a = i16(eC.b[0].a - 12)
        elif eC.e == 2:
            eC.b[0].b = i16(eC.b[0].b - 12)
        elif eC.e == 3:
            eC.b[0].a = i16(eC.b[0].a + 12)

    def aC(self):  # ar.java:1795-1879  (end of tick: previous state, room-change timers)
        cz = ag.cz
        cz.a[1] = cz.a[0]
        cz.b[1] = cz.b[0]
        cz.d[1] = cz.d[0]
        cz.d[0] = cz.c
        cz.e[1] = cz.e[0]
        cz.f[1] = cz.f[0]
        cz.N += 1
        ag.ek = 0
        if cz.C > 0:
            cz.C -= 1
            if cz.C < 1:
                cz.A = 0
            ag.ek = 1
        if cz.D > 0:
            cz.D -= 1
            if cz.D < 1:
                cz.B = 0
            ag.ek = 1
        ag.cs[4] = ag.cs[3]
        ag.cs[3] = ag.cs[2]
        ag.cs[2] = ag.cs[1]
        ag.cs[1] = ag.cs[0]
        ag.cs[0] = -1
        ag.cl = 0
        ag.fh = 0
        if ag.fd is not None:
            ag.ff = i16(ag.ff - 1)
            if ag.ff < 0:
                ag.fe = None
                ag.fd = None
        for b in range(ag.ez):
            s = ag.ey[b]
            ag.ex[s].a[1] = ag.ex[s].a[0]
            ag.ex[s].e[1] = ag.ex[s].e[0]
            ag.ex[s].f[1] = ag.ex[s].f[0]
            ag.ex[s].g[1] = ag.ex[s].g[0]
        if cz.e[0] in (28, 29, 30):
            if ag.co != 0:
                ag.cn = 0
            return
        if ag.co != 0:
            if ag.cn < 1:
                v = ag.co
                if v == 1:
                    if ag.cp != 0:
                        ag.bV = 4
                        ag.co = 0
                        ag.cm = 1
                    if 0 == ag.cn:
                        ag.cm = 2
                        for b in range(4):
                            if ag.eO[ag.eP].a[b] != 0:
                                ag.ct[21 + b] = self.d_T(ag.bA.a_I(17 + b))
                        ag.cn = i16(ag.cn - 1)
                        return
                elif v == 2:
                    ag.cS.e_I(8)
                    ag.co = 0
                    return
                elif v == 3:
                    ag.cS.e_I(9)
                    ag.co = 0
                    return
                elif v == 4:
                    ag.cS.e_I(10)
                    ag.co = 0
                return
            ag.cn = i16(ag.cn - 1)
            if ag.co == 3 and ag.cn == 0 and ag.bg is not None:
                ag.ai()

    def O_I(self, paramInt):  # ar.java:1881-1890  (mission clock dX, paused while a popup / menu is open)
        ag.dW[0] = ag.B_v()
        if paramInt == 0 or ag.dW[0] - ag.dW[1] > 1000:
            ag.dV += ag.dW[0] - ag.dW[1]
        else:
            l_ = ag.dW[0] - ag.dV
            ag.dX = int(l_ // 1000)
        ag.dW[1] = ag.dW[0]

    def k_v(self):  # ar.java:1892-1932  (bV = 4: scroll to the next room, 6 steps)
        v = ag.cp
        if v == 1:
            ag.ce += 7
        elif v == 2:
            ag.cd -= 7
        elif v == 3:
            ag.ce -= 7
        elif v == 4:
            ag.cd += 7
        if v in (1, 2, 3, 4):
            ag.cm = i16(ag.cm + 6)
            ag.bd.a_IIIII(ag.cb.a, ag.cb.b, ag.cd, ag.ce, 0)
        self.a_MIIIIII(ag.ct[7], ag.db, ag.dc, ag.bY.a, ag.bY.b, ag.cc.a, ag.cc.b)
        arrayOfInt = self.b_LhII(ag.cz.a[0], 0, 0)
        ag.cz.a[0].a = i16(ag.cz.a[0].a + arrayOfInt[0])
        ag.cz.a[0].b = i16(ag.cz.a[0].b + arrayOfInt[1])
        ag.bd.e_v()
        if ag.cm > 1:
            self.a__I(-1)
        if ag.cm > 6:
            ag.bV = 3
            ag.ck = 1
            ag.cp = 0
            ag.do = i16(ag.do + 1)
            ag.co = 2
            ag.cn = 1
            self.A_v()
        ag.cm = i16(ag.cm + 1)

    # ---- drawing helpers ---------------------------------------------------------------------

    def a_III(self, paramInt1, paramInt2, paramInt3):  # ar.java:1934-1936  (hit spark eV)
        v_ = ag.eV[paramInt1]
        self.b_MIIIIII(ag.ct[43], paramInt2 - v_.e, paramInt3 - v_.f, v_.c, v_.d, v_.a, v_.b)

    def a_IILy(self, paramInt1, paramInt2, paramy):  # ar.java:1938-1941  (the hero's weapon)
        self.b_MIIIIII(ag.ct[40 + ag.cz.K], paramInt1 - paramy.e, paramInt2 - paramy.f, paramy.c, paramy.d, paramy.a, paramy.b)
        c.a_IIII(ag.cz.a[0].a - paramy.e, ag.cz.a[0].b - paramy.f, paramy.c, paramy.d)

    def a_II(self, paramInt1, paramInt2):  # ar.java:1943-1969  (weapon trail of the hero (-1) or an enemy)
        if paramInt1 > -1:
            h_ = ag.ex[paramInt1].a[0]
            if ag.ex[paramInt1].f[0] == 19:
                i = ag.ex[paramInt1].e[0] + (ag.ex[paramInt1].g[0] >> 1 << 1) & 0x7
            else:
                i = ag.ex[paramInt1].e[0]
        else:
            h_ = ag.cz.a[0]
            if ag.cz.e[0] == 25:
                i = ag.cz.d[0] + (ag.cz.f[0] >> 1 << 1) & 0x7
            else:
                i = ag.cz.d[0]
        j_ = (i >> 1) * 6 + (paramInt2 << 1)
        k = h_.a - ag.ca.a
        m = h_.b - ag.ca.b
        for b in range(2):
            u = ag.eU[j_]
            self.b_MIIIIII(ag.ct[42], k - u.e, m - u.f, u.c, u.d, u.a, u.b)
            c.a_IIII(h_.a - u.e, h_.b - u.f, u.c, u.d)
            j_ += 1

    def l_v(self):  # ar.java:1971-1983  (object layer over dirty cells)
        cE = ag.cE
        for b in range(ag.cb.a):
            for b1 in range(ag.cb.b):
                if ag.eE[b1][b] != 0:
                    i = (ag.ce + b1) * cE.b.a + ag.cd + b
                    if cE.a[cE.e + i] != 0:
                        j_ = ag.cJ[cE.a[cE.e + i] - 1] - 1
                        self.b_MIIIIII(ag.bT[j_], (ag.cd + b) * 27 - ag.ca.a, (ag.ce + b1) * 27 - ag.ca.b, 27, 27, 0, 0)

    def m_v(self):  # ar.java:1985-2015  (dropped items; objects being broken)
        for b in range(ag.cD):
            cC = ag.cC[b]
            if cC.a != 0:
                self.b_MIIIIII(cC.g, cC.b.a - ag.ca.a - (cC.e >> 1), cC.b.b - ag.ca.b - (cC.f >> 1), cC.e, cC.f, cC.e * cC.d, 0)
                c.a_IIII(cC.b.a - (cC.e >> 1), cC.b.b - (cC.f >> 1), cC.e, cC.f)
        for b in range(ag.cB):
            cA = ag.cA[b]
            if cA.a != 0 and cA.e != 0:
                cA.e = i16(cA.e - 1)
                if (cA.e & 0x2) != 0:
                    self.b_MIIIIII(ag.bT[cA.f], cA.c.a * 27 - ag.ca.a, cA.c.b * 27 - ag.ca.b, 27, 27, 0, 0)
                else:
                    i = cA.c.a * 27 - ag.ca.a
                    j_ = cA.c.b * 27 - ag.ca.b
                    if ag.ct[7] is not None and i + ag.cc.a >= 0:
                        if i + ag.cc.a > ag.ct[7].getWidth():
                            return
                        self.b_MIIIIII(ag.ct[7], i, j_, 27, 27, i + ag.cc.a, j_ + ag.cc.b)
                    else:
                        break
                if 0 == cA.e:
                    self.a_ILh(3, cA.b)
                    cA.a = 0

    def a_ILh(self, paramInt, paramh):  # ar.java:2017-2053  (drop an item at paramh)
        from pow.game.structs import h as h_
        s1 = paramh.a
        s2 = paramh.b
        if s2 <= ag.ca.b + 27 or s2 >= ag.ca.b + 162 or s1 <= ag.ca.a + 27 or s1 >= ag.ca.a + 162:
            return
        s3 = self.P_I(paramInt)
        if s3 != 0:
            i = idiv(s2, 27) * ag.cE.b.a + idiv(s1, 27)
            if 0 == (ag.cE.a[ag.cE.f + i] & 0x1):
                b = 0
                while b < 10 and ag.cC[b].a != 0:
                    b += 1
                if b > 9:
                    return
                cC = ag.cC[b]
                cC.a = s3
                if cC.b is None:
                    cC.b = h_()
                cC.b.a = s1
                cC.b.b = s2
                cC.c = 75
                cC.e = cC.f = 28
                if s3 > 10000:
                    cC.g = ag.ct[32]
                    cC.d = 0
                    cC.e = i16(ag.ct[32].getWidth())
                    cC.f = i16(ag.ct[32].getHeight())
                elif s3 > 100:
                    cC.g = ag.ct[0]
                    cC.d = 11
                else:
                    cC.g = ag.ct[0]
                    cC.d = i16(s3 - 1)
                if b >= ag.cD:
                    ag.cD = i16(ag.cD + 1)

    def P_I(self, paramInt):  # ar.java:2055-2078  (random drop: item id, potion, or gold 10020/10040)
        C = self.C_I
        arrayOfByte1 = [5, 10, 20, 5, 100]
        arrayOfByte2 = [10, 30, 60, 1, 100]
        arrayOfByte3 = [69, 44, 24, 9, 0]
        arrayOfByte = [[0, 0, 33, 77, 100], [5, 30, 55, 80, 100], [30, 60, 90, 100, 100],
                       [40, 80, 100, 100, 100], [80, 100, 100, 100, 100]]
        if C(100) < arrayOfByte1[paramInt]:
            i = C(100)
            if i < arrayOfByte2[paramInt]:
                for b in range(5):
                    if ag.cz.l > arrayOfByte3[b]:
                        i = C(100)
                        for b1 in range(5):
                            if i < arrayOfByte[b][b1]:
                                return i16(101 + b1 + 5 * C(20))
            else:
                return i16(C(11) + 1)
        elif C(100) < 25:
            return i16(10020 + (ag.ep ^ 0x1) * 20)
        return 0

    def aD(self):  # ar.java:2081-2089  (the two quick potions * and # of the HUD)
        cz = ag.cz
        for b in range(2):
            z = cz.Z[cz.aa[b]]
            if z.a != 0:
                ag.a_IIIIMII(ag.dd + (2 * b - 1) * (44 + 28 * (1 - b) + 0), ag.bZ.b - 33 - 0 - 17, 28, 28, ag.ct[0], (z.a - 1) * 28, 0)
                ag.a_IIIIMII(ag.dd + (2 * b - 1) * (38 + 11 * (1 - b) + 0), ag.bZ.b - 16 - 0 - 17, 11, 12, ag.ct[20], 98, 0)
                self.h_III(z.b, ag.dd + (2 * b - 1) * (28 + 10 * b + 0), ag.bZ.b - 18 - 0 - 17)

    def n_v(self):  # ar.java:2091-2107  (HUD of the map: balls, gold, potions, clock, soft keys)
        ag.bd.a_v()
        if ag.dT.a != 0:
            self.aE()
        else:
            self.h_III(ag.cz.I, ag.bY.a - 4 - 7, 20)
        self.aD()
        self.j_III(0, 5, ag.dX)
        if ag.bV == 3 and ag.cS.b == 0:
            if ag.cR.a != 0:
                ag.h_II(-1, 9)
                return
            ag.h_II(-1, 1)

    def aE(self):  # ar.java:2109-2141  (message box dT: item picked up)
        not_ported("ar.aE() (message box on the map)")
