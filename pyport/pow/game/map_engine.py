"""ar.java - the map / combat engine (bc). Literal port: the frame loop, the hero's walls and
room exits, room scrolling, the HUD of the map, the pause menu, the enemy AI, hits, skills,
potions and scrolls, deaths and drops. config.NO_ENEMIES / NO_COMBAT (PORT-EXTRA, off by
default) give the map without enemies / without the attack keys."""
from pow.game import consts
from pow.game.game_canvas import GameCanvas
from pow.game.map_scene import MapScene
from pow.game.structs import Point, Rect
from pow.game.gfx import Gfx
import config
from pow.midp.jint import i8, i16, idiv

F6 = config.DECOMP_FIX["F6"]


class MapEngine(GameCanvas):
    def __init__(self):  # ar.java:2-4
        super().__init__(GameCanvas.bs)

    def a_v(self):  # ar.java:6-23  (one tick of the map)
        if GameCanvas.cS.b != 0:
            GameCanvas.cS.b_v()
            self.L_v()
        elif GameCanvas.cR.a != 0:
            self.o_v()
            self.L_v()
        else:
            GameCanvas.bd.i_v()
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
                    GameCanvas.eE[b][b1] = 1
            GameCanvas.bd.c_v()
            if GameCanvas.cR.a != 0:
                GameCanvas.cS.b_I(170)
                v = GameCanvas.cR.a
                if v == 1:
                    GameCanvas.bb.f_v()
                elif v == 2:
                    GameCanvas.bb.d_I(0)
                    GameCanvas.bb.k_v()
                elif v == 3:
                    GameCanvas.bb.j_v()
                elif v == 4:
                    GameCanvas.bb.l_v()
            if GameCanvas.cS.b != 0:
                GameCanvas.cS.c_v()
                GameCanvas.bb.n_v()
            return
        if paramInt == 2:
            return
        if GameCanvas.cS.b != 0:
            if GameCanvas.cS.j != 0:
                GameCanvas.cS.c_v()
            GameCanvas.bb.n_v()
            return
        if GameCanvas.cR.a != 0:
            if GameCanvas.cR.b != 0:
                v = GameCanvas.cR.a
                if v == 1:
                    GameCanvas.cS.b_I(170)
                    GameCanvas.bb.f_v()
                elif v == 2:
                    GameCanvas.bb.d_I(1)
                elif v == 3:
                    GameCanvas.cS.b_I(170)
                    GameCanvas.bb.j_v()
                elif v == 4:
                    GameCanvas.cS.b_I(170)
                    GameCanvas.bb.l_v()
                GameCanvas.cR.b = 0
            if GameCanvas.cR.a == 2:
                GameCanvas.bb.k_v()
                return
        else:
            GameCanvas.bd.c_v()

    def o_v(self):  # ar.java:95-247  (keys of the pause menu cR.a: 1 menu, 2 items, 3 options, 4 help)
        arrayOfByte1 = [0, 3, 0, 2, 4, 0, 0]
        arrayOfByte2 = [0, 3, 0, 5, 3, 0, 0]
        v = GameCanvas.ch
        blocked = GameCanvas.ez > 0 or GameCanvas.cr != 0 or GameCanvas.eD[0] != 0
        if v in (-1, 50):
            if GameCanvas.cR.a in (1, 3):
                GameCanvas.cM[1] = GameCanvas.cM[1] - 1
                if (GameCanvas.cM[1] < 0) if F6 else (GameCanvas.cM[1] - 1 < 0):   # DECOMP-FIX F6
                    GameCanvas.cM[1] = GameCanvas.cN - 1
                if GameCanvas.cM[1] == 1 and GameCanvas.cR.a == 3 and not GameCanvas.df:
                    GameCanvas.cM[1] = 0
                if GameCanvas.cM[1] == 2 and GameCanvas.cR.a == 1 and blocked:
                    GameCanvas.cM[1] = GameCanvas.cM[1] - 1
                GameCanvas.I_v()
                GameCanvas.cR.b = 1
            return
        if v in (-2, 56):
            if GameCanvas.cR.a in (1, 3):
                GameCanvas.cM[1] = GameCanvas.cM[1] + 1
                if (GameCanvas.cM[1] >= GameCanvas.cN) if F6 else (GameCanvas.cM[1] + 1 >= GameCanvas.cN):   # DECOMP-FIX F6
                    GameCanvas.cM[1] = 0
                if GameCanvas.cM[1] == 1 and GameCanvas.cR.a == 3 and not GameCanvas.df:
                    GameCanvas.cM[1] = 2
                if GameCanvas.cM[1] == 2 and GameCanvas.cR.a == 1 and blocked:
                    GameCanvas.cM[1] = GameCanvas.cM[1] + 1
                GameCanvas.I_v()
                GameCanvas.cR.b = 1
            return
        if v in (-3, 52):
            if GameCanvas.cR.a in (2, 4):
                GameCanvas.cM[1] = GameCanvas.cM[1] - 1
                if (GameCanvas.cM[1] < 0) if F6 else (GameCanvas.cM[1] - 1 < 0):   # DECOMP-FIX F6
                    GameCanvas.cM[1] = GameCanvas.cN - 1
                GameCanvas.cR.b = 1
            elif GameCanvas.cR.a == 3:
                self.y_I(0)
                GameCanvas.cR.b = 1
            return
        if v in (-4, 54):
            if GameCanvas.cR.a in (2, 4):
                GameCanvas.cM[1] = GameCanvas.cM[1] + 1
                if (GameCanvas.cM[1] >= GameCanvas.cN) if F6 else (GameCanvas.cM[1] + 1 >= GameCanvas.cN):   # DECOMP-FIX F6
                    GameCanvas.cM[1] = 0
                GameCanvas.cR.b = 1
            elif GameCanvas.cR.a == 3:
                self.y_I(1)
                GameCanvas.cR.b = 1
            return
        if v == 42:
            if GameCanvas.cR.a == 2:
                GameCanvas.ck = MapEngine.c_I(0)
            return
        if v == 35:
            if GameCanvas.cR.a == 2:
                GameCanvas.ck = MapEngine.c_I(1)
            return
        if v in (-5, 53):
            if GameCanvas.cM[0] == 10 and GameCanvas.cM[1] == 4:
                GameCanvas.cM[0] = 5
                GameCanvas.cM[1] = 3
                GameCanvas.bW = GameCanvas.bV
                GameCanvas.bV = 2
                GameCanvas.bb.b_v()
                return
            if GameCanvas.cR.a == 1:
                if arrayOfByte1[GameCanvas.cM[1]] != 0:
                    GameCanvas.cR.a = arrayOfByte1[GameCanvas.cM[1]]
                    GameCanvas.cN = arrayOfByte2[GameCanvas.cM[1]]
                    GameCanvas.ck = 1
                    GameCanvas.cP[0] = i16(GameCanvas.cM[1])
                    GameCanvas.cQ[0] = i16(GameCanvas.cM[2])
                    GameCanvas.cM[1] = 0
                    GameCanvas.ej = 3
                    return
                w = GameCanvas.cM[1]
                if w == 2:
                    if blocked:
                        GameCanvas.cS.e_I(7)
                    elif self.ar() != 0:
                        GameCanvas.cS.e_I(0)
                elif w == 0:
                    GameCanvas.ck = 1
                    GameCanvas.ct[10] = None
                    GameCanvas.ct[17] = None
                    GameCanvas.cR.a = 0
                    self.a__I(-1)
                elif w == 5:
                    GameCanvas.cS.e_I(5)
                elif w == 6:
                    GameCanvas.cS.e_I(28)
                    GameCanvas.ck = 1
                return
            if GameCanvas.cR.a == 3:
                self.y_I(1)
                GameCanvas.cR.b = 1
                return
            return
        if v == -7:
            GameCanvas.ck = 1
            if GameCanvas.cR.a == 1:
                GameCanvas.ct[10] = None
                GameCanvas.ct[17] = None
                GameCanvas.cR.a = 0
                self.a__I(-1)
                return
            GameCanvas.cR.a = 1
            GameCanvas.cM[1] = GameCanvas.cP[0]
            GameCanvas.cM[2] = GameCanvas.cQ[0]
            GameCanvas.cN = 7

    @staticmethod
    def c_I(paramInt):  # ar.java:249-261  (assign the potion under the cursor to * / #)
        cz = GameCanvas.cz
        if cz.Z[GameCanvas.cM[1]].a != 0 and cz.aa[paramInt] != GameCanvas.cM[1]:
            if GameCanvas.cM[1] == cz.aa[paramInt + 1 & 0x1]:
                i = cz.aa[paramInt]
                cz.aa[paramInt] = cz.aa[paramInt + 1 & 0x1]
                cz.aa[paramInt + 1 & 0x1] = i
            else:
                cz.aa[paramInt] = GameCanvas.cM[1]
            return 1
        return 0

    @staticmethod
    def b_v():  # ar.java:263-268
        if GameCanvas.cz.p > GameCanvas.cz.y:
            GameCanvas.cz.p = GameCanvas.cz.y
        if GameCanvas.cz.r > GameCanvas.cz.z:
            GameCanvas.cz.r = GameCanvas.cz.z

    @staticmethod
    def Q_I(paramInt):  # ar.java:270-272
        return -paramInt if paramInt < 0 else paramInt

    def a_IIIIIIII(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7, paramInt8):  # ar.java:274-282
        i = idiv(paramInt3 + paramInt7, 2)
        j_ = idiv(paramInt4 + paramInt8, 2)
        k = paramInt1 + idiv(paramInt3, 2) - paramInt5 + idiv(paramInt7, 2)
        m = paramInt2 + idiv(paramInt4, 2) - paramInt6 + idiv(paramInt8, 2)
        n = MapEngine.Q_I(k)
        i1 = MapEngine.Q_I(m)
        return n < i and i1 < j_

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
        if config.NO_ENEMIES:
            # PORT-EXTRA (map without combat): the whole wave list of the room counts as
            # defeated at once, and the room is cleared exactly as when its last enemy dies
            # (ar.java:1326-1332): popup "Stage N Complete", then the exits open.
            # A room whose list holds a general (id < 200, c.java:986-1010: talk + duel) stays
            # closed: the mission is won only by defeating him, which is the combat.
            if any(0 < GameCanvas.eD[k] < 200 for k in range(0, 14, 2)):
                return
            if GameCanvas.co == 0 and GameCanvas.eD[0] != 0:
                for b in range(14):
                    GameCanvas.eD[b] = 0
                if GameCanvas.cr != 0:
                    GameCanvas.co = 4
                    GameCanvas.cn = 22
                else:
                    GameCanvas.co = 3
                    GameCanvas.cn = 5
            return
        if GameCanvas.eA < GameCanvas.eO[GameCanvas.eP].b:
            if GameCanvas.eD[0] == 0:
                return
            if (GameCanvas.eD[0] >= 200 or GameCanvas.eB == 0) and GameCanvas.ev != 0:
                i = self.C_I(GameCanvas.ev)
                GameCanvas.bd.b_IIII(GameCanvas.eD[0], GameCanvas.eu[i].a, GameCanvas.eu[i].b, GameCanvas.eu[i].c)
                GameCanvas.eD[1] = i16(GameCanvas.eD[1] - 1)
                if GameCanvas.eD[1] < 1:
                    for b in range(12):
                        GameCanvas.eD[b] = GameCanvas.eD[b + 2]

    @staticmethod
    def e_I(paramInt):  # ar.java:743-757  (MP cost of skill paramInt; 0 = not enough MP)
        arrayOfByte1 = [5, 6, 7, 10, 15, 7, 10, 10, 8, 9, 10, 5, 6, 7, 9, 12, 20, 20, 20]
        arrayOfByte2 = [3, 4, 5, 3, 4, 3, 3, 5, 3, 4, 5, 3, 4, 5, 5, 6, 5, 5, 5]
        i = 0
        if 12 <= paramInt <= 30:
            i = arrayOfByte1[paramInt - 12] + (GameCanvas.cz.W[paramInt - 12] - 1) * arrayOfByte2[paramInt - 12]
        if i > GameCanvas.cz.r:
            return 0
        GameCanvas.cz.r -= i
        return i

    @staticmethod
    def e_v():  # ar.java:759-767  (direction pressed twice quickly -> run)
        if GameCanvas.cs[0] > -1:
            if GameCanvas.dh >= 3:
                return 1 if (GameCanvas.cs[0] == GameCanvas.cs[1] or GameCanvas.cs[0] == GameCanvas.cs[2] or GameCanvas.cs[0] == GameCanvas.cs[3]) else 0
            if GameCanvas.cs[0] == GameCanvas.cs[1] or GameCanvas.cs[0] == GameCanvas.cs[2]:
                return 1
        return 0

    # ---- walls -------------------------------------------------------------------------------

    def a_LhII(self, paramh, paramInt1, paramInt2):  # ar.java:769-815  (step paramInt1 towards paramInt2 until no wall)
        arrayOfInt1 = [0, 0]
        arrayOfInt2 = [0, 0]
        arrayOfInt3 = [0, 0]
        cE = GameCanvas.cE
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
                paramInt1 = MapEngine.t_II(b2, paramInt1)[1]
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
        h1 = Point()
        h1.a = i16(paramh.a + paramInt1)
        h1.b = i16(paramh.b + paramInt2)
        if h1.a < arrayOfShort[GameCanvas.cf.a] + 12:
            paramInt1 = arrayOfShort[GameCanvas.cf.a] + 12 - paramh.a
            if GameCanvas.co == 1:
                MapEngine.X_I(2)
        elif h1.a > arrayOfShort[GameCanvas.cf.a + 1] - 12:
            paramInt1 = arrayOfShort[GameCanvas.cf.a + 1] - 12 - paramh.a
            if GameCanvas.co == 1:
                MapEngine.X_I(4)
        if h1.b < arrayOfShort[GameCanvas.cf.b] + 10:
            paramInt2 = arrayOfShort[GameCanvas.cf.b] + 10 - paramh.b
            if GameCanvas.co == 1:
                MapEngine.X_I(3)
        elif h1.b > arrayOfShort[GameCanvas.cf.b + 1] + 10:
            paramInt2 = arrayOfShort[GameCanvas.cf.b + 1] + 10 - paramh.b
            if GameCanvas.co == 1:
                MapEngine.X_I(1)
        return [paramInt1, paramInt2]

    @staticmethod
    def X_I(paramInt):  # ar.java:867-888  (leave the room through exit paramInt: 1 down 2 left 3 up 4 right)
        if GameCanvas.cn < 0 and GameCanvas.eO[GameCanvas.eP].a[paramInt - 1] != 0:
            GameCanvas.cp = i16(paramInt)
            if paramInt == 1:
                GameCanvas.eP = i16(GameCanvas.eP + idiv(GameCanvas.cE.b.a, 7))
            elif paramInt == 2:
                GameCanvas.eP = i16(GameCanvas.eP - 1)
            elif paramInt == 3:
                GameCanvas.eP = i16(GameCanvas.eP - idiv(GameCanvas.cE.b.a, 7))
            elif paramInt == 4:
                GameCanvas.eP = i16(GameCanvas.eP + 1)
            for b in range(4):
                GameCanvas.ct[21 + b] = None
            GameCanvas.cm = 0

    @staticmethod
    def c_LhII(paramh, paramInt1, paramInt2):  # ar.java:890-1014  (slide around a corner: new direction or -1)
        cE = GameCanvas.cE
        b1 = 0
        j_ = idiv(paramh.a, 27)
        k = idiv(paramh.b, 27)
        m = j_ + k * cE.b.a
        arrayOfInt1 = [0, 0]
        arrayOfInt2 = [1, 1]
        if paramInt2 == -1:
            h1 = GameCanvas.cz.j
        else:
            h1 = GameCanvas.ex[paramInt2].b
        if paramInt1 in (0, 6):
            b1 = 1
        elif paramInt1 in (2, 4):
            b1 = -1
        def free(q):
            return 0 == (cE.a[cE.f + q] & 0x1) and 0 == cE.a[cE.e + q]

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
                paramInt1 = GameCanvas.cz.j.a
                paramInt2 = GameCanvas.cz.j.b
            else:
                paramInt1 = GameCanvas.ex[paramInt4].b.a
                paramInt2 = GameCanvas.ex[paramInt4].b.b
        else:
            if paramInt1 > 0:
                i = self.a_LhII(paramh, paramInt1, 6)
            elif paramInt1 < 0:
                i = self.a_LhII(paramh, paramInt1, 2)
            if paramInt2 > 0:
                j_ = self.a_LhII(paramh, paramInt2, 0)
            elif paramInt2 < 0:
                j_ = self.a_LhII(paramh, paramInt2, 4)
        u = MapEngine.u_II
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
                h1 = GameCanvas.cz.j
            else:
                h1 = GameCanvas.ex[paramInt4].b
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
        h1 = Point()
        h1.a = i16(paramh.a + paramInt1)
        h1.b = i16(paramh.b + paramInt2)
        if paramInt3 > -1:
            i = MapEngine.c_LhLh(h1, GameCanvas.cz.a[0])
            j_ = MapEngine.c_LhLh(paramh, GameCanvas.cz.a[0])
            if i < j_ and i < 20:
                while MapEngine.Q_I(h1.a - GameCanvas.cz.a[0].a) <= 27 and MapEngine.Q_I(h1.b - GameCanvas.cz.a[0].b) <= 27:
                    MapEngine.t_II(paramInt1, paramInt2)       # (result unused in the original)
                    h1.a = i16(paramh.a + paramInt1)
                    h1.b = i16(paramh.b + paramInt2)
                    b += 1
                    if b > 16:
                        break
        else:
            for b1 in range(GameCanvas.ez):
                s = GameCanvas.ey[b1]
                if GameCanvas.ex[s].f[0] != 3:
                    i = MapEngine.c_LhLh(h1, GameCanvas.ex[s].a[0])
                    j_ = MapEngine.c_LhLh(paramh, GameCanvas.ex[s].a[0])
                    if i < j_ and i < 20:
                        b = 0
                        while MapEngine.Q_I(h1.a - GameCanvas.ex[s].a[0].a) <= 27 and MapEngine.Q_I(h1.b - GameCanvas.ex[s].a[0].b) <= 27:
                            MapEngine.t_II(paramInt1, paramInt2)
                            h1.a = i16(paramh.a + paramInt1)
                            h1.b = i16(paramh.b + paramInt2)
                            b += 1
                            if b > 16:
                                break
        return [paramInt1, paramInt2]

    # ---- the combat: hits ---------------------------------------------------------------------

    def b_II(self, paramInt1, paramInt2):  # ar.java:284-339  (the hero's action paramInt2 hits enemy paramInt1)
        ex = GameCanvas.ex[paramInt1]
        cz = GameCanvas.cz
        ex.t = 1
        if paramInt2 > -1:
            ex.e[0] = ex.d = MapEngine.b_LhLh(ex.a[0], cz.a[0])
        else:
            ex.e[0] = ex.d = MapEngine.b_LhLh(ex.a[0], GameCanvas.dU.c)
        if 3 <= paramInt2 <= 8:
            i = cz.w + cz.A - ex.k - ex.o
            ex.m = i16(ex.m - (i if i > 0 else 1))
        elif paramInt2 in (12, 13, 14) or 20 <= paramInt2 <= 30:
            i = cz.w + cz.A + idiv(cz.w * cz.W[paramInt2 - 12], consts.aU[paramInt2 - 12]) - ex.k - ex.o
            ex.m = i16(ex.m - (i if i > 0 else 1))
        elif paramInt2 == -2:
            ex.A = 2
            ex.m = i16(ex.m - (50 if cz.l << 1 > 50 else cz.l << 1))
            self.a__I(4)
        elif paramInt2 == -1:
            ex.m = i16(ex.m - (30 if cz.l > 30 else cz.l))
            self.a__I(3)
        if ex.m < 1:
            ex.m = 0
            ex.g[0] = 3
        else:
            ex.g[0] = 0
        MapEngine.R_I(paramInt1)
        ex.v = ex.a[0]
        ex.u = -1
        ex.f[0] = 2
        if ex.h < 200 and self.C_I(1000) < 150 and ex.m > 0:
            self.m_II(paramInt1, 1)

    def m_II(self, paramInt1, paramInt2):  # ar.java:341-368  (a general picks a skill)
        ex = GameCanvas.ex[paramInt1]
        ex.f[0] = i8(6 + GameCanvas.dC.d[self.C_I(4)] - 1)
        if ex.f[0] < 6 and ex.f[0] > 21:
            ex.f[0] = 1
        else:
            if ex.f[0] in (9, 10):
                if ex.z > 3:
                    ex.f[0] = 1
                elif ex.l >> 1 > ex.m:
                    ex.z = i8(ex.z + 1)
                else:
                    ex.f[0] = 1
            elif ex.f[0] in (11, 12, 13):
                if paramInt2 != 0:
                    ex.f[0] = 1
        ex.e[0] = ex.d = MapEngine.a_LhLh(ex.a[0], GameCanvas.cz.a[0])

    def c_v(self):  # ar.java:370-408  (the hero's attack vs. breakable objects cA)
        cz = GameCanvas.cz
        h_ = Point()
        for b in range(GameCanvas.cB):
            cA = GameCanvas.cA[b]
            if cA.a != 0 and cA.d > 0:
                e0 = cz.e[0]
                if e0 == 13:
                    q = cz.d[0] >> 1
                    if self.a_IIIIIIII(cz.a[0].a + consts.aF[q], cz.a[0].b + consts.aG[q], consts.aH[q], consts.aI[q], cA.b.a - 8, cA.b.b - 8, 18, 18):
                        self.W_I(b)
                elif e0 == 22:
                    if MapEngine.a_LhLhI(cz.a[0], cA.b, cz.d[0]) != 0:
                        self.s_II(b, consts.aK[cz.K])
                elif e0 in (23, 24):
                    self.s_II(b, 45)
                elif e0 == 25:
                    if (cz.d[0] + (cz.f[0] >> 1 << 1) & 0x7) == MapEngine.a_LhLh(cz.a[0], cA.b):
                        self.s_II(b, consts.aK[cz.K])
                elif e0 in (26, 27):
                    h_.a = i16(cz.a[0].a + consts.aA[cz.d[0] >> 1])
                    h_.b = i16(cz.a[0].b + consts.aB[cz.d[0] >> 1])
                    if MapEngine.c_LhLh(h_, cA.b) <= 35:
                        self.W_I(b)
                elif e0 in (28, 29, 30):
                    self.W_I(b)
                else:
                    self.p_II(b, consts.aK[cz.K])

    @staticmethod
    def R_I(paramInt):  # ar.java:410-421  (message box: enemy name and HP bar)
        ex = GameCanvas.ex[paramInt]
        GameCanvas.dT.a = 1
        GameCanvas.dT.b = 10
        GameCanvas.dT.d = ex.i
        GameCanvas.dT.e = i16(idiv(ex.m * 60, ex.l))
        if ex.h < 200:
            GameCanvas.dT.c = GameCanvas.dC.a
            return
        GameCanvas.dT.e = i16(GameCanvas.dT.e >> 1)
        GameCanvas.dT.c = consts.aS[ex.h - 201]

    @staticmethod
    def a_LhLhI(paramh1, paramh2, paramInt):  # ar.java:423-443  (is paramh2 in front of paramh1?)
        if paramInt == 2:
            if paramh1.a > paramh2.a:
                return 1
        elif paramInt == 6:
            if paramh1.a < paramh2.a:
                return 1
        elif paramInt == 0:
            if paramh1.b < paramh2.b:
                return 1
        elif paramInt == 4:
            if paramh1.b > paramh2.b:
                return 1
        return 0

    @staticmethod
    def a_LhLh(paramh1, paramh2):  # ar.java:445-449  (direction 0/2/4/6 from paramh1 to paramh2)
        i = paramh2.a - paramh1.a
        j_ = paramh2.b - paramh1.b
        if j_ > i:
            return 0 if j_ > -i else 2
        return 6 if j_ > -i else 4

    @staticmethod
    def b_LhLh(paramh1, paramh2):  # ar.java:451-455  (direction 0..7 from paramh1 to paramh2)
        i = paramh2.a - paramh1.a
        j_ = paramh2.b - paramh1.b
        if i + i < j_:
            if i + i > -j_:
                return 0
            if -i < j_ + j_:
                return 1
            if i < j_ + j_:
                return 2
            return 3
        if i + i < -j_:
            return 4
        if -i > j_ + j_:
            return 5
        if i > j_ + j_:
            return 6
        return 7

    def n_II(self, paramInt1, paramInt2):  # ar.java:470-473
        if GameCanvas.cz.d[0] == MapEngine.a_LhLh(GameCanvas.cz.a[0], GameCanvas.ex[paramInt1].a[0]):
            self.q_II(paramInt1, paramInt2)

    def o_II(self, paramInt1, paramInt2):  # ar.java:475-478
        if GameCanvas.ex[paramInt1].e[0] == MapEngine.a_LhLh(GameCanvas.ex[paramInt1].a[0], GameCanvas.cz.a[0]):
            self.r_II(paramInt1, paramInt2)

    def p_II(self, paramInt1, paramInt2):  # ar.java:480-483
        if GameCanvas.cz.d[0] == MapEngine.a_LhLh(GameCanvas.cz.a[0], GameCanvas.cA[paramInt1].b):
            self.s_II(paramInt1, paramInt2)

    def q_II(self, paramInt1, paramInt2):  # ar.java:485-488
        if MapEngine.c_LhLh(GameCanvas.cz.a[0], GameCanvas.ex[paramInt1].a[0]) <= paramInt2:
            self.S_I(paramInt1)

    def r_II(self, paramInt1, paramInt2):  # ar.java:490-493
        if MapEngine.c_LhLh(GameCanvas.cz.a[0], GameCanvas.ex[paramInt1].a[0]) <= paramInt2:
            self.T_I(paramInt1)

    def s_II(self, paramInt1, paramInt2):  # ar.java:495-498
        if MapEngine.c_LhLh(GameCanvas.cz.a[0], GameCanvas.cA[paramInt1].b) <= paramInt2:
            self.W_I(paramInt1)

    def S_I(self, paramInt):  # ar.java:500-544  (the hero hits enemy paramInt: knock-back A, effects)
        cz = GameCanvas.cz
        ex = GameCanvas.ex[paramInt]
        h_ = Point()
        if ex.f[0] > 5:
            return
        self.b_II(paramInt, cz.e[0])
        if cz.M > 1 and cz.e[0] < 12:
            ex.A = 1
        e0 = cz.e[0]
        if e0 == 12:
            cz.f[0] = 5
            ex.A = 2
        elif e0 in (14, 22):
            ex.A = 2
        elif e0 == 20:
            ex.t = i8(self.C_I(2) + 1)
            ex.A = 0
        elif e0 == 21:
            ex.A = 5
        elif e0 in (23, 24):
            if e0 == 24:                    # case 24 falls through into case 23
                ex.A = 5
            self.V_I(paramInt)
        elif e0 in (25, 26, 27):
            if e0 == 25:                    # 25 -> 27 -> 26 fall through
                ex.A = 2
            if e0 in (25, 27):
                ex.A = 5
            ex.t = 2
            h_.a = i16(cz.a[0].a + consts.aA[cz.d[0] >> 1])
            h_.b = i16(cz.a[0].b + consts.aB[cz.d[0] >> 1])
            ex.e[0] = ex.d = MapEngine.b_LhLh(ex.a[0], h_)
        elif e0 == 29:
            self.V_I(paramInt)
        self.a__I(16)                       # (`if (A != 0);` - the sound plays always)

    def T_I(self, paramInt):  # ar.java:546-578  (a general's skill hits the hero)
        cz = GameCanvas.cz
        f0 = GameCanvas.ex[paramInt].f[0]
        if f0 == 6:
            GameCanvas.ex[paramInt].g[0] = 5
            cz.R = 2
        elif f0 in (8, 16):
            cz.R = 2
        elif f0 == 14:
            cz.O = self.C_I(2) + 1
        elif f0 == 15:
            cz.R = 5
        elif f0 in (17, 18):
            if f0 == 18:                    # case 18 falls through into case 17
                cz.R = 5
            self.p_v()
        elif f0 == 19:
            cz.R = 2
            self.p_v()
        elif f0 in (20, 21):
            if f0 == 21:                    # case 21 falls through into case 20
                cz.R = 5
            cz.O = 2
        self.U_I(paramInt)

    def U_I(self, paramInt):  # ar.java:580-638  (the hero is hit by enemy paramInt, or by arrow paramInt + 3)
        cz = GameCanvas.cz
        if paramInt > -1:
            ex = GameCanvas.ex[paramInt]
            cz.d[0] = cz.c = MapEngine.b_LhLh(cz.a[0], ex.a[0])
            if ex.f[0] in (6, 7, 8, 14, 15, 16, 17, 18, 19, 20, 21):
                i = ex.j + ex.n + idiv(ex.j, consts.aU[ex.f[0] - 6]) - cz.x - cz.B
            else:
                i = ex.j + ex.n - cz.x - cz.B
            i = i if i > 0 else 1
            if cz.p > i:
                cz.p -= i
            else:
                cz.p = 0
        else:
            eC = GameCanvas.eC[paramInt + 3]
            cz.d[0] = cz.c = (eC.e << 1) + 4 & 0x7
            i = eC.f - cz.x - cz.B
            b = i8(i if i > 0 else 1)
            if cz.p > b:
                cz.p -= b
            else:
                cz.p = 0
        if paramInt > -1:
            MapEngine.R_I(paramInt)
        cz.Q = cz.a[0]
        cz.O = 1
        cz.P = -1
        cz.f[0] = 0
        cz.e[0] = 9
        if cz.R != 0:
            self.a__I(4)
        else:
            self.a__I(16)
        if cz.p < 1:
            cz.p = 0
            cz.e[0] = 10

    def V_I(self, paramInt):  # ar.java:640-651  (fire effect on an enemy)
        GameCanvas.ex[paramInt].w = 1
        GameCanvas.ex[paramInt].x = 0
        GameCanvas.ff = 7
        self.a__I(13)
        if GameCanvas.fd is None:
            GameCanvas.fe = self.K_I(60)
            GameCanvas.fd = list(consts.ao)

    def p_v(self):  # ar.java:653-661  (fire effect on the hero)
        GameCanvas.cz.T = 1
        GameCanvas.cz.U = 0
        self.a__I(13)
        if GameCanvas.eX is None:
            GameCanvas.eY = self.K_I(60)
            GameCanvas.eX = consts.ao

    def W_I(self, paramInt):  # ar.java:663-672  (hit a breakable object)
        cA = GameCanvas.cA[paramInt]
        cA.d = i16(cA.d - GameCanvas.cz.w + GameCanvas.cz.A)
        self.a__I(3)
        cA.h = 2
        if cA.d < 1:
            cA.e = 12
            i = cA.c.b * GameCanvas.cE.b.a + cA.c.a
            GameCanvas.cE.a[GameCanvas.cE.e + i] = 0

    def d_I(self, paramInt):  # ar.java:674-724  (the hero's attack (0) or a scroll (-1/-2) vs. enemies)
        cz = GameCanvas.cz
        h_ = Point()
        for b in range(GameCanvas.ez):
            s = GameCanvas.ey[b]
            ex = GameCanvas.ex[s]
            if ex.m > 0 and ex.r != 0 and ex.f[0] < 6:
                if paramInt == 0:
                    e0 = cz.e[0]
                    if e0 == 13:
                        q = cz.d[0] >> 1
                        if self.a_IIIIIIII(cz.a[0].a + consts.aF[q], cz.a[0].b + consts.aG[q], consts.aH[q], consts.aI[q], ex.a[0].a - 8, ex.a[0].b - 8, 17, 17):
                            self.b_II(s, cz.e[0])
                            self.a__I(3)
                    elif e0 == 22:
                        if MapEngine.a_LhLhI(cz.a[0], ex.a[0], cz.d[0]) != 0:
                            self.q_II(s, consts.aK[cz.K])
                    elif e0 in (23, 24):
                        self.q_II(s, 45)
                    elif e0 == 25:
                        if (cz.d[0] + (cz.f[0] >> 1 << 1) & 0x7) == MapEngine.a_LhLh(cz.a[0], ex.a[0]):
                            self.q_II(s, consts.aK[cz.K])
                    elif e0 in (26, 27):
                        h_.a = i16(cz.a[0].a + consts.aA[cz.d[0] >> 1])
                        h_.b = i16(cz.a[0].b + consts.aB[cz.d[0] >> 1])
                        if MapEngine.c_LhLh(h_, ex.a[0]) <= 35:
                            self.S_I(s)
                    elif e0 in (28, 29, 30):
                        self.S_I(s)
                    self.n_II(s, consts.aK[cz.K])
                elif paramInt in (-2, -1):
                    if MapEngine.c_LhLh(GameCanvas.dU.c, ex.a[0]) <= 35:
                        self.b_II(s, GameCanvas.dU.a)
                        self.a__I(4)

    def f_v(self):  # ar.java:1196-1200  (Normal difficulty, ep = 1: turn to the nearest enemy before the attack)
        if GameCanvas.ep != 0 or config.AUTO_AIM_HARD:   # PORT-EXTRA config.AUTO_AIM_HARD: also on Hard
            i = self.aB()
            if i > -1:
                GameCanvas.cz.d[0] = GameCanvas.cz.c = MapEngine.a_LhLh(GameCanvas.cz.a[0], GameCanvas.ex[i].a[0])

    def aB(self):  # ar.java:1202-1214  (nearest living enemy closer than 50)
        s = -1
        j_ = 50
        for b in range(GameCanvas.ez):
            s1 = GameCanvas.ey[b]
            i = MapEngine.c_LhLh(GameCanvas.ex[s1].a[0], GameCanvas.cz.a[0])
            if j_ > i and GameCanvas.ex[s1].m > 0:
                j_ = i
                s = s1
        return s

    # ---- the combat: enemy AI ----------------------------------------------------------------

    def Y_I(self, paramInt):  # ar.java:1216-1278  (choose the next action of enemy paramInt)
        arrayOfByte = [-2, -1, 0, 0, 0, 0, 1, 2]
        cz = GameCanvas.cz
        ex = GameCanvas.ex[paramInt]
        i = MapEngine.c_LhLh(cz.a[0], ex.a[0])
        b = 1 if i < 90 else 0
        ex.g[0] = 0
        j_ = self.C_I(1000)
        b1 = MapEngine.a_Lh(ex.a[0])
        if ex.h in (201, 203):
            if j_ < 150 + b * 300:
                ex.f[0] = 0
                ex.e[0] = ex.d = i8(b1 + arrayOfByte[j_ & 0x7] & 0x7)
                return
            if j_ < 850 - b * 100:
                if b != 0:
                    if i <= 45 and cz.e[0] != 9 and cz.e[0] != 10 and cz.e[0] < 12:
                        ex.f[0] = 1
                        ex.e[0] = ex.d = MapEngine.a_LhLh(ex.a[0], cz.a[0])
                        self.U_I(paramInt)
                        return
                    ex.f[0] = 0
                    ex.e[0] = ex.d = i8(b1 + arrayOfByte[j_ & 0x7] & 0x7)
                    return
                ex.f[0] = 0
                ex.e[0] = ex.d = i8(ex.e[0] + arrayOfByte[j_ & 0x7] & 0x7)
                return
            ex.f[0] = 0
            if b != 0:
                ex.e[0] = ex.d = i8(j_ & 0x7)
                return
            ex.e[0] = ex.d = i8(ex.e[0] + arrayOfByte[j_ & 0x7] & 0x7)
            return
        if ex.h == 202:
            ex.f[0] = 1
            ex.s = 15
            MapEngine.Z_I(paramInt)
            return
        if j_ < 150:
            self.m_II(paramInt, 0)
            return
        if j_ < 350:
            if i <= 60 and (cz.e[0] != 9 or cz.f[0] >= 6) and cz.e[0] != 10 and cz.e[0] < 12:
                ex.f[0] = 1
                ex.e[0] = ex.d = MapEngine.a_LhLh(ex.a[0], cz.a[0])
                return
        else:
            ex.e[0] = ex.d = b1

    @staticmethod
    def a_Lh(paramh):  # ar.java:1280-1284  (direction 0..7 from paramh to the hero, 27 px dead zone)
        i = GameCanvas.cz.a[0].a - paramh.a
        j_ = GameCanvas.cz.a[0].b - paramh.b
        if i > 27:
            return 7 if j_ > 27 else (5 if j_ < -27 else 6)
        if i < -27:
            return 1 if j_ > 27 else (3 if j_ < -27 else 2)
        return 0 if j_ > 0 else 4

    @staticmethod
    def Z_I(paramInt):  # ar.java:1286-1308  (an archer shoots an arrow eC)
        arrayOfByte1 = [-1, -15, -1, 5]
        arrayOfByte2 = [-5, -13, -30, -13]
        ex = GameCanvas.ex[paramInt]
        i = ex.e[0] >> 1
        for b in range(3):
            eC = GameCanvas.eC[b]
            if eC.a == 0:
                eC.a = 1
                eC.b[1].a = i16(ex.a[0].a + arrayOfByte1[i])
                eC.b[1].b = i16(ex.a[0].b + arrayOfByte2[i])
                if config.DECOMP_FIX["F18"]:
                    # DECOMP-FIX F18: the start goes into eC.b[1] (the "previous" position used
                    # only for erasing, c.java:124-141), but ar.j() (ar.java:1734-1735) first
                    # copies b[0] -> b[1] and then hits / moves b[0] (ar.ad). b[0] is a separate
                    # h (f.java), so literally every arrow flies from (0, 0) or from where the
                    # previous arrow of this slot vanished: never from the archer, never into
                    # the hero. With F18 the arrow starts at the archer's bow.
                    eC.b[0].a = eC.b[1].a
                    eC.b[0].b = eC.b[1].b
                eC.e = i8(i)
                eC.g = 0
                eC.f = ex.j
                if (i & 0x1) != 0:
                    eC.c = 11
                    eC.d = 2
                    return
                eC.c = 2
                eC.d = 11
                return

    _SHIFT203 = {3: (-10, 0), 1: (-10, 10), 2: (-10, 0), 0: (0, 10), 5: (10, 0), 7: (10, 10), 6: (10, 0)}

    def g_v(self):  # ar.java:1310-1604  (enemy AI: one tick of every enemy)
        arrayOfByte = [20, 20, 25]
        i = 0
        cz = GameCanvas.cz
        # Java `for (b = 0; b < ag.ez; b++)` reads ez every time: ab() below removes the dead
        # enemy from ey and decrements ez inside the loop (and the next enemy is skipped this tick)
        b = -1
        while True:
            b += 1
            if b >= GameCanvas.ez:
                break
            s1 = GameCanvas.ey[b]
            ex = GameCanvas.ex[s1]
            ex.f[0] = min(ex.f[0], len(ex.B[ex.e[0]]) - 1)
            ex.g[0] = i8(ex.g[0] + 1)
            ex.s = i8(ex.s - 1)
            s2 = ex.B[ex.e[0]][ex.f[0]][ex.g[0]]
            if ex.p > 0:
                ex.p = i16(ex.p - 1)
                if ex.p < 1:
                    ex.n = 0
            if ex.q > 0:
                ex.q = i16(ex.q - 1)
                if ex.q < 1:
                    ex.o = 0
            if ex.f[0] == 3:
                if s2 > 200:
                    self.ab_I(s1)
                    if GameCanvas.eA < 1 and 0 == GameCanvas.eD[0] and ex.h != 202:
                        if GameCanvas.cr != 0:
                            GameCanvas.co = 4
                            GameCanvas.cn = 22
                        else:
                            GameCanvas.co = 3
                            GameCanvas.cn = 5
                continue
            if s2 > 200:
                if ex.m < 1:
                    ex.f[0] = 3
                else:
                    ex.f[0] = 0
                ex.g[0] = 0
                if ex.h < 200:
                    GameCanvas.fb = None
                    GameCanvas.fa = None
            if ex.s < 1:
                ex.r = 1
                ex.s = 6
                if ex.f[0] == 0:
                    self.Y_I(s1)
            if ex.h == 202:
                ex.e[0] = ex.d = MapEngine.a_LhLh(ex.a[0], cz.a[0])
                continue
            j_ = ex.d
            if ex.r == 0:
                ex.a[0].a = i16(ex.a[0].a + consts.aw[j_])
                ex.a[0].b = i16(ex.a[0].b + consts.ax[j_])
                continue
            k = m = 0
            f0 = ex.f[0]
            g0 = ex.g[0]
            e0 = ex.e[0]
            if f0 == 0:
                k = consts.aw[j_]
                m = consts.ax[j_]
            elif f0 in (1, 4, 5):
                k = idiv(consts.aw[e0], 3)
                m = idiv(consts.ax[e0], 3)
            elif f0 == 6:
                if 2 < g0 < 6:
                    k = consts.aw[e0] << 2
                    m = consts.ax[e0] << 2
            elif f0 in (7, 8):
                fall8 = f0 == 8
                if f0 == 7 and 4 < g0 < 8:
                    k = consts.aw[e0] << 2
                    m = consts.ax[e0] << 2
                    if k > 0:
                        k = self.a_LhII(ex.a[0], k, 6)
                    elif k < 0:
                        k = self.a_LhII(ex.a[0], k, 2)
                    if m > 0:
                        m = self.a_LhII(ex.a[0], m, 0)
                    elif m < 0:
                        m = self.a_LhII(ex.a[0], m, 4)
                    arrayOfInt = self.b_LhII(ex.a[0], k, m)
                    k = arrayOfInt[0]
                    m = arrayOfInt[1]
                    ex.a[0].a = i16(ex.a[0].a + k)
                    ex.a[0].b = i16(ex.a[0].b + m)
                    fall8 = True            # no break: falls into case 8
                if fall8 and 0 < g0 < 9:
                    k = consts.aw[e0]
                    m = consts.ax[e0]
            elif f0 == 14:
                if 0 == (g0 & 0x1):
                    k = consts.aw[e0]
                    m = consts.ax[e0]
            elif f0 == 2 and ex.A > 0:
                ex.A = i8(ex.A - 1)
                j_ = j_ + 4 & 0x7
                k = consts.aw[j_] << 2
                m = consts.ax[j_] << 2
            elif f0 == 2 and g0 == 1:
                j_ = ex.d + 4 & 0x7
                k = idiv(consts.aw[j_] * 3, 4)
                m = idiv(consts.ax[j_] * 3, 4)
            if k != 0 or m != 0:
                if ex.h == 203:
                    arrayOfH = ex.a
                    dx, dy = MapEngine._SHIFT203.get(j_, (0, 0))
                    arrayOfH[0].a = i16(arrayOfH[0].a + dx)
                    arrayOfH[1].a = i16(arrayOfH[1].a + dx)
                    arrayOfH[0].b = i16(arrayOfH[0].b + dy)
                    arrayOfH[1].b = i16(arrayOfH[1].b + dy)
                    i = self.a_LhIIII(arrayOfH[0], k, m, j_, s1)
                    arrayOfH[0].a = i16(arrayOfH[0].a - dx)
                    arrayOfH[1].a = i16(arrayOfH[1].a - dx)
                    arrayOfH[0].b = i16(arrayOfH[0].b - dy)
                    arrayOfH[1].b = i16(arrayOfH[1].b - dy)
                else:
                    i = self.a_LhIIII(ex.a[0], k, m, j_, s1)
                if ex.f[0] == 0 and j_ in (0, 2, 4, 6):
                    if i == -1:
                        i = MapEngine.c_LhII(ex.a[0], ex.d, s1)
                        if i != -1:
                            self.a_LhIIII(ex.a[0], consts.aw[i], consts.ax[i], i, s1)
            f0 = ex.f[0]
            g0 = ex.g[0]
            if f0 in (1, 4, 5):
                if g0 == 1:
                    self.aa_I(s1)
            elif f0 == 6:
                if 2 < g0 < 6:
                    self.aa_I(s1)
            elif f0 == 7:
                if 4 < g0 < 8:
                    self.aa_I(s1)
            elif f0 == 8:
                if g0 in (2, 4, 6, 8):
                    self.aa_I(s1)
            elif f0 in (9, 10):
                if g0 == 11:
                    ex.m = i16(ex.m + idiv(ex.l * (20 if f0 == 9 else 50), 100))
                    if ex.m > ex.l:
                        ex.m = ex.l
            elif f0 in (11, 12, 13):
                if g0 == 11:
                    if f0 != 12:
                        ex.n = i16(idiv(ex.j, arrayOfByte[f0 - 11]))
                        if ex.n < 1:
                            ex.n = 1
                        ex.p = 50
                    if f0 != 11:
                        ex.o = i16(idiv(ex.k, arrayOfByte[f0 - 11]))
                        if ex.o < 1:
                            ex.o = 1
                        ex.q = 50
            elif f0 == 14:
                if (g0 & 0x1) != 0:
                    self.aa_I(s1)
            elif f0 == 15:
                if g0 == 5:
                    self.aa_I(s1)
            elif f0 == 16:
                if g0 == 6:
                    self.aa_I(s1)
            elif f0 in (17, 18):
                if g0 == 5:
                    self.aa_I(s1)
            elif f0 == 19:
                if (g0 & 0x1) != 0:
                    self.aa_I(s1)
            elif f0 in (20, 21):
                if g0 == 8:
                    self.aa_I(s1)

    def aa_I(self, paramInt):  # ar.java:1606-1661  (enemy paramInt strikes the hero)
        cz = GameCanvas.cz
        ex = GameCanvas.ex[paramInt]
        h_ = Point()
        if cz.e[0] != 9 and cz.e[0] != 10:
            if cz.e[0] < 12:
                f0 = ex.f[0]
                if f0 == 7:
                    q = ex.e[0] >> 1
                    if self.a_IIIIIIII(ex.a[0].a + consts.aF[q], ex.a[0].b + consts.aG[q], consts.aH[q], consts.aI[q], cz.a[0].a - 8, cz.a[0].b - 8, 17, 17):
                        self.U_I(paramInt)
                    return
                if f0 == 16:
                    if MapEngine.a_LhLhI(ex.a[0], cz.a[0], ex.e[0]) != 0:
                        self.r_II(paramInt, consts.aL[GameCanvas.dC.c])
                    return
                if f0 in (17, 18):
                    self.r_II(paramInt, 45)
                    return
                if f0 == 19:
                    if (ex.e[0] + (ex.g[0] >> 1 << 1) & 0x7) == MapEngine.a_LhLh(ex.a[0], cz.a[0]):
                        self.r_II(paramInt, consts.aL[GameCanvas.dC.c])
                    return
                if f0 in (20, 21):
                    h_.a = i16(ex.a[0].a + consts.aA[ex.e[0] >> 1])
                    h_.b = i16(ex.a[0].b + consts.aB[ex.e[0] >> 1])
                    if MapEngine.c_LhLh(h_, cz.a[0]) <= 35:
                        self.T_I(paramInt)
                    return
                self.o_II(paramInt, consts.aL[GameCanvas.dC.c])
                return
        elif cz.e[0] == 9:
            f0 = ex.f[0]
            if f0 in (8, 14):
                self.o_II(paramInt, consts.aL[GameCanvas.dC.c])
                return
            if f0 in (20, 21):
                h_.a = i16(ex.a[0].a + consts.aA[cz.d[0] >> 1])
                h_.b = i16(ex.a[0].b + consts.aB[cz.d[0] >> 1])
                if MapEngine.c_LhLh(h_, cz.a[0]) <= 35:
                    self.T_I(paramInt)

    def ab_I(self, paramInt):  # ar.java:1663-1698  (enemy paramInt is dead: exp, drop, remove)
        ex = GameCanvas.ex[paramInt]
        for b in range(GameCanvas.ez):
            if GameCanvas.ey[b] == paramInt:
                if ex.h < 200:
                    b1 = 2 if GameCanvas.cr != 0 else 1
                    GameCanvas.dY += ex.i << 1
                    if GameCanvas.dC.c != GameCanvas.cz.K:
                        GameCanvas.ct[40 + GameCanvas.dC.c] = None
                    GameCanvas.er[1] = None
                    for b2 in range(3, 9):
                        GameCanvas.et[b2] = None
                    GameCanvas.eB = 0
                else:
                    b1 = 0
                    GameCanvas.dY += ex.i
                self.a_ILh(b1, ex.a[0])
                if ex.h == 203:
                    GameCanvas.cz.H += 3
                else:
                    GameCanvas.cz.H += 1
                for b1 in range(b, 6):
                    GameCanvas.ey[b1] = GameCanvas.ey[b1 + 1]
                ex.c = 0
                GameCanvas.ez = i16(GameCanvas.ez - 1)
                if ex.h != 202:
                    GameCanvas.eA = i16(GameCanvas.eA - 1)
                return

    # ---- per-tick updates --------------------------------------------------------------------

    @staticmethod
    def h_v():  # ar.java:1700-1711  (sort enemies by y)
        if GameCanvas.ez != 0:
            for b in range(GameCanvas.ez - 1):
                for i in range(b + 1, GameCanvas.ez):
                    if GameCanvas.ex[GameCanvas.ey[b]].a[0].b > GameCanvas.ex[GameCanvas.ey[i]].a[0].b:
                        s = GameCanvas.ey[b]
                        GameCanvas.ey[b] = GameCanvas.ey[i]
                        GameCanvas.ey[i] = s

    def i_v(self):  # ar.java:1713-1729  (pick up dropped items)
        for b in range(GameCanvas.cD):
            cC = GameCanvas.cC[b]
            if cC.a != 0:
                if MapEngine.c_LhLh(GameCanvas.cz.a[0], cC.b) < 20 and self.k_II(cC.a, 1) != 0:
                    GameCanvas.ek = 1
                    if 100 < cC.a < 10000:
                        GameCanvas.bb.e_I(cC.a)
                        GameCanvas.cS.e_I(13)
                    cC.a = 0
                cC.c = i16(cC.c - 1)
                if cC.c < 1:
                    cC.a = 0

    def j_v(self):  # ar.java:1731-1749  (arrows: hit the hero or fly on)
        for b in range(3):
            eC = GameCanvas.eC[b]
            if eC.a != 0:
                eC.b[1].a = eC.b[0].a
                eC.b[1].b = eC.b[0].b
                if self.a_IIIIIIII(eC.b[0].a, eC.b[0].b + 8, eC.c, eC.d, GameCanvas.cz.a[0].a - 12, GameCanvas.cz.a[0].b - 20, 17, 18):
                    if GameCanvas.cz.e[0] < 12:
                        GameCanvas.bd.d_v()
                        eC.a = 0
                        self.U_I(b - 3)
                    else:
                        self.ac_I(b)
                else:
                    self.ac_I(b)

    def ac_I(self, paramInt):  # ar.java:1751-1772
        e1 = GameCanvas.cz.e[1]
        f1 = GameCanvas.cz.f[1]
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
        MapEngine.ad_I(paramInt)

    @staticmethod
    def ad_I(paramInt):  # ar.java:1774-1793  (move an arrow)
        eC = GameCanvas.eC[paramInt]
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
        cz = GameCanvas.cz
        cz.a[1] = cz.a[0]
        cz.b[1] = cz.b[0]
        cz.d[1] = cz.d[0]
        cz.d[0] = cz.c
        cz.e[1] = cz.e[0]
        cz.f[1] = cz.f[0]
        cz.N += 1
        GameCanvas.ek = 0
        if cz.C > 0:
            cz.C -= 1
            if cz.C < 1:
                cz.A = 0
            GameCanvas.ek = 1
        if cz.D > 0:
            cz.D -= 1
            if cz.D < 1:
                cz.B = 0
            GameCanvas.ek = 1
        GameCanvas.cs[4] = GameCanvas.cs[3]
        GameCanvas.cs[3] = GameCanvas.cs[2]
        GameCanvas.cs[2] = GameCanvas.cs[1]
        GameCanvas.cs[1] = GameCanvas.cs[0]
        GameCanvas.cs[0] = -1
        GameCanvas.cl = 0
        GameCanvas.fh = 0
        if GameCanvas.fd is not None:
            GameCanvas.ff = i16(GameCanvas.ff - 1)
            if GameCanvas.ff < 0:
                GameCanvas.fe = None
                GameCanvas.fd = None
        for b in range(GameCanvas.ez):
            s = GameCanvas.ey[b]
            GameCanvas.ex[s].a[1] = GameCanvas.ex[s].a[0]
            GameCanvas.ex[s].e[1] = GameCanvas.ex[s].e[0]
            GameCanvas.ex[s].f[1] = GameCanvas.ex[s].f[0]
            GameCanvas.ex[s].g[1] = GameCanvas.ex[s].g[0]
        if cz.e[0] in (28, 29, 30):
            if GameCanvas.co != 0:
                GameCanvas.cn = 0
            return
        if GameCanvas.co != 0:
            if GameCanvas.cn < 1:
                v = GameCanvas.co
                if v == 1:
                    if GameCanvas.cp != 0:
                        GameCanvas.bV = 4
                        GameCanvas.co = 0
                        GameCanvas.cm = 1
                    if 0 == GameCanvas.cn:
                        GameCanvas.cm = 2
                        for b in range(4):
                            if GameCanvas.eO[GameCanvas.eP].a[b] != 0:
                                GameCanvas.ct[21 + b] = self.d_T(GameCanvas.bA.a_I(17 + b))
                        GameCanvas.cn = i16(GameCanvas.cn - 1)
                        return
                elif v == 2:
                    GameCanvas.cS.e_I(8)
                    GameCanvas.co = 0
                    return
                elif v == 3:
                    GameCanvas.cS.e_I(9)
                    GameCanvas.co = 0
                    return
                elif v == 4:
                    GameCanvas.cS.e_I(10)
                    GameCanvas.co = 0
                return
            GameCanvas.cn = i16(GameCanvas.cn - 1)
            if GameCanvas.co == 3 and GameCanvas.cn == 0 and GameCanvas.bg is not None:
                GameCanvas.ai()

    def O_I(self, paramInt):  # ar.java:1881-1890  (mission clock dX, paused while a popup / menu is open)
        GameCanvas.dW[0] = GameCanvas.B_v()
        if paramInt == 0 or GameCanvas.dW[0] - GameCanvas.dW[1] > 1000:
            GameCanvas.dV += GameCanvas.dW[0] - GameCanvas.dW[1]
        else:
            l_ = GameCanvas.dW[0] - GameCanvas.dV
            GameCanvas.dX = int(l_ // 1000)
        GameCanvas.dW[1] = GameCanvas.dW[0]

    def k_v(self):  # ar.java:1892-1932  (bV = 4: scroll to the next room, 6 steps)
        v = GameCanvas.cp
        if v == 1:
            GameCanvas.ce += 7
        elif v == 2:
            GameCanvas.cd -= 7
        elif v == 3:
            GameCanvas.ce -= 7
        elif v == 4:
            GameCanvas.cd += 7
        if v in (1, 2, 3, 4):
            GameCanvas.cm = i16(GameCanvas.cm + 6)
            GameCanvas.bd.a_IIIII(GameCanvas.cb.a, GameCanvas.cb.b, GameCanvas.cd, GameCanvas.ce, 0)
        self.a_MIIIIII(GameCanvas.ct[7], GameCanvas.db, GameCanvas.dc, GameCanvas.bY.a, GameCanvas.bY.b, GameCanvas.cc.a, GameCanvas.cc.b)
        arrayOfInt = self.b_LhII(GameCanvas.cz.a[0], 0, 0)
        GameCanvas.cz.a[0].a = i16(GameCanvas.cz.a[0].a + arrayOfInt[0])
        GameCanvas.cz.a[0].b = i16(GameCanvas.cz.a[0].b + arrayOfInt[1])
        GameCanvas.bd.e_v()
        if GameCanvas.cm > 1:
            self.a__I(-1)
        if GameCanvas.cm > 6:
            GameCanvas.bV = 3
            GameCanvas.ck = 1
            GameCanvas.cp = 0
            GameCanvas.do = i16(GameCanvas.do + 1)
            GameCanvas.co = 2
            GameCanvas.cn = 1
            self.A_v()
        GameCanvas.cm = i16(GameCanvas.cm + 1)

    # ---- drawing helpers ---------------------------------------------------------------------

    def a_III(self, paramInt1, paramInt2, paramInt3):  # ar.java:1934-1936  (hit spark eV)
        v_ = GameCanvas.eV[paramInt1]
        self.b_MIIIIII(GameCanvas.ct[43], paramInt2 - v_.e, paramInt3 - v_.f, v_.c, v_.d, v_.a, v_.b)

    def a_IILy(self, paramInt1, paramInt2, paramy):  # ar.java:1938-1941  (the hero's weapon)
        self.b_MIIIIII(GameCanvas.ct[40 + GameCanvas.cz.K], paramInt1 - paramy.e, paramInt2 - paramy.f, paramy.c, paramy.d, paramy.a, paramy.b)
        MapScene.a_IIII(GameCanvas.cz.a[0].a - paramy.e, GameCanvas.cz.a[0].b - paramy.f, paramy.c, paramy.d)

    def a_II(self, paramInt1, paramInt2):  # ar.java:1943-1969  (weapon trail of the hero (-1) or an enemy)
        if paramInt1 > -1:
            h_ = GameCanvas.ex[paramInt1].a[0]
            if GameCanvas.ex[paramInt1].f[0] == 19:
                i = GameCanvas.ex[paramInt1].e[0] + (GameCanvas.ex[paramInt1].g[0] >> 1 << 1) & 0x7
            else:
                i = GameCanvas.ex[paramInt1].e[0]
        else:
            h_ = GameCanvas.cz.a[0]
            if GameCanvas.cz.e[0] == 25:
                i = GameCanvas.cz.d[0] + (GameCanvas.cz.f[0] >> 1 << 1) & 0x7
            else:
                i = GameCanvas.cz.d[0]
        j_ = (i >> 1) * 6 + (paramInt2 << 1)
        k = h_.a - GameCanvas.ca.a
        m = h_.b - GameCanvas.ca.b
        for b in range(2):
            u = GameCanvas.eU[j_]
            self.b_MIIIIII(GameCanvas.ct[42], k - u.e, m - u.f, u.c, u.d, u.a, u.b)
            MapScene.a_IIII(h_.a - u.e, h_.b - u.f, u.c, u.d)
            j_ += 1

    def l_v(self):  # ar.java:1971-1983  (object layer over dirty cells)
        cE = GameCanvas.cE
        for b in range(GameCanvas.cb.a):
            for b1 in range(GameCanvas.cb.b):
                if GameCanvas.eE[b1][b] != 0:
                    i = (GameCanvas.ce + b1) * cE.b.a + GameCanvas.cd + b
                    if cE.a[cE.e + i] != 0:
                        j_ = GameCanvas.cJ[cE.a[cE.e + i] - 1] - 1
                        self.b_MIIIIII(GameCanvas.bT[j_], (GameCanvas.cd + b) * 27 - GameCanvas.ca.a, (GameCanvas.ce + b1) * 27 - GameCanvas.ca.b, 27, 27, 0, 0)

    def m_v(self):  # ar.java:1985-2015  (dropped items; objects being broken)
        for b in range(GameCanvas.cD):
            cC = GameCanvas.cC[b]
            if cC.a != 0:
                self.b_MIIIIII(cC.g, cC.b.a - GameCanvas.ca.a - (cC.e >> 1), cC.b.b - GameCanvas.ca.b - (cC.f >> 1), cC.e, cC.f, cC.e * cC.d, 0)
                MapScene.a_IIII(cC.b.a - (cC.e >> 1), cC.b.b - (cC.f >> 1), cC.e, cC.f)
        for b in range(GameCanvas.cB):
            cA = GameCanvas.cA[b]
            if cA.a != 0 and cA.e != 0:
                cA.e = i16(cA.e - 1)
                if (cA.e & 0x2) != 0:
                    self.b_MIIIIII(GameCanvas.bT[cA.f], cA.c.a * 27 - GameCanvas.ca.a, cA.c.b * 27 - GameCanvas.ca.b, 27, 27, 0, 0)
                else:
                    i = cA.c.a * 27 - GameCanvas.ca.a
                    j_ = cA.c.b * 27 - GameCanvas.ca.b
                    if GameCanvas.ct[7] is not None and i + GameCanvas.cc.a >= 0:
                        if i + GameCanvas.cc.a > GameCanvas.ct[7].getWidth():
                            return
                        self.b_MIIIIII(GameCanvas.ct[7], i, j_, 27, 27, i + GameCanvas.cc.a, j_ + GameCanvas.cc.b)
                    else:
                        break
                if 0 == cA.e:
                    self.a_ILh(3, cA.b)
                    cA.a = 0

    def a_ILh(self, paramInt, paramh):  # ar.java:2017-2053  (drop an item at paramh)
        s1 = paramh.a
        s2 = paramh.b
        if s2 <= GameCanvas.ca.b + 27 or s2 >= GameCanvas.ca.b + 162 or s1 <= GameCanvas.ca.a + 27 or s1 >= GameCanvas.ca.a + 162:
            return
        s3 = self.P_I(paramInt)
        if s3 != 0:
            i = idiv(s2, 27) * GameCanvas.cE.b.a + idiv(s1, 27)
            if 0 == (GameCanvas.cE.a[GameCanvas.cE.f + i] & 0x1):
                b = 0
                while b < 10 and GameCanvas.cC[b].a != 0:
                    b += 1
                if b > 9:
                    return
                cC = GameCanvas.cC[b]
                cC.a = s3
                if cC.b is None:
                    cC.b = Point()
                cC.b.a = s1
                cC.b.b = s2
                cC.c = 75
                cC.e = cC.f = 28
                if s3 > 10000:
                    cC.g = GameCanvas.ct[32]
                    cC.d = 0
                    cC.e = i16(GameCanvas.ct[32].getWidth())
                    cC.f = i16(GameCanvas.ct[32].getHeight())
                elif s3 > 100:
                    cC.g = GameCanvas.ct[0]
                    cC.d = 11
                else:
                    cC.g = GameCanvas.ct[0]
                    cC.d = i16(s3 - 1)
                if b >= GameCanvas.cD:
                    GameCanvas.cD = i16(GameCanvas.cD + 1)

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
                    if GameCanvas.cz.l > arrayOfByte3[b]:
                        i = C(100)
                        for b1 in range(5):
                            if i < arrayOfByte[b][b1]:
                                return i16(101 + b1 + 5 * C(20))
            else:
                return i16(C(11) + 1)
        elif C(100) < 25:
            return i16(10020 + (GameCanvas.ep ^ 0x1) * 20)
        return 0

    def aD(self):  # ar.java:2081-2089  (the two quick potions * and # of the HUD)
        cz = GameCanvas.cz
        for b in range(2):
            z = cz.Z[cz.aa[b]]
            if z.a != 0:
                GameCanvas.a_IIIIMII(GameCanvas.dd + (2 * b - 1) * (44 + 28 * (1 - b) + 0), GameCanvas.bZ.b - 33 - 0 - 17, 28, 28, GameCanvas.ct[0], (z.a - 1) * 28, 0)
                GameCanvas.a_IIIIMII(GameCanvas.dd + (2 * b - 1) * (38 + 11 * (1 - b) + 0), GameCanvas.bZ.b - 16 - 0 - 17, 11, 12, GameCanvas.ct[20], 98, 0)
                self.h_III(z.b, GameCanvas.dd + (2 * b - 1) * (28 + 10 * b + 0), GameCanvas.bZ.b - 18 - 0 - 17)

    def n_v(self):  # ar.java:2091-2107  (HUD of the map: balls, gold, potions, clock, soft keys)
        GameCanvas.bd.a_v()
        if GameCanvas.dT.a != 0:
            self.aE()
        else:
            self.h_III(GameCanvas.cz.I, GameCanvas.bY.a - 4 - 7, 20)
        self.aD()
        self.j_III(0, 5, GameCanvas.dX)
        if GameCanvas.bV == 3 and GameCanvas.cS.b == 0:
            if GameCanvas.cR.a != 0:
                GameCanvas.h_II(-1, 9)
                return
            GameCanvas.h_II(-1, 1)

    def aE(self):  # ar.java:2109-2141  (message box dT: item picked up)
        GameCanvas.dD = GameCanvas.c_T(GameCanvas.dT.c)
        i = GameCanvas.bY.a - GameCanvas.bu.a_ACII(list(GameCanvas.dT.c), 0, len(GameCanvas.dT.c)) - 8
        Gfx.a_Lg(GameCanvas.bv)
        GameCanvas.d_TII(GameCanvas.dT.c, i, 3)
        GameCanvas.d_TII(GameCanvas.dT.c, i - 1, 2)
        GameCanvas.d_TII(GameCanvas.dT.c, i + 1, 2)
        GameCanvas.d_TII(GameCanvas.dT.c, i, 1)
        Gfx.a_Lg(GameCanvas.bu)
        GameCanvas.d_TII(GameCanvas.dT.c, i, 2)
        GameCanvas.dD = GameCanvas.s_I(GameCanvas.dT.d)
        ct31 = GameCanvas.ct[31]
        self.b_MIIIIII(ct31, GameCanvas.bY.a - ct31.getWidth() - 27 - 5 - 7, 2 + GameCanvas.bu.a_v(), ct31.getWidth(), ct31.getHeight(), 0, 0)
        self.a_IIIIIMIII(GameCanvas.dT.d, GameCanvas.bY.a - 15, 1 + GameCanvas.bu.a_v() + 17, 9, 12, GameCanvas.ct[20], 0, 0, -1)
        if GameCanvas.dT.e > 0:
            ac_ = Rect(GameCanvas.bY.a - 62 + GameCanvas.db - 7, 2 + GameCanvas.bu.a_v() + 12 + GameCanvas.dc, 62 if GameCanvas.dT.e > 62 else GameCanvas.dT.e, 7)
            GameCanvas.a_LacI(ac_, GameCanvas.k_III(0, 0, 0))
            ac_.b += 1
            ac_.d = 5
            ac_.a += 1
            ac_.c -= 2
            GameCanvas.a_LacI(ac_, GameCanvas.k_III(107, 0, 0))
            ac_.b += 1
            ac_.d = 3
            GameCanvas.a_LacI(ac_, GameCanvas.k_III(181, 0, 0))
            ac_.b += 1
            ac_.d = 1
            GameCanvas.a_LacI(ac_, GameCanvas.k_III(255, 73, 0))
        MapScene.a_IIII(GameCanvas.ca.a + 170, GameCanvas.ca.b, 68, 40)
