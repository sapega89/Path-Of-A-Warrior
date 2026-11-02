"""l.java - popups (cS). Literal port, Phase 0 subset.

Ported: drawing (c, b(int), a(4 ints), O, c(int)), text popups a(String) and e(int) with all
plain-text messages, and the key/timer logic b() for the branches the menus reach.
Branches that need map/combat/campaign code raise NotPorted.
"""
import config
from pow.game import consts
from pow.game.game_canvas import GameCanvas
from pow.game.gfx import Gfx
from pow.midp.jint import i16


class Popups(GameCanvas):
    r = None  # public static Image r = null;  l.java:38  (ui_popup)

    def __init__(self):  # l.java:42-44
        super().__init__(GameCanvas.bs)
        self.a = 0       # 1 = popup from d() (gamestr), 0 = from e()
        self.b = 0       # popup kind: 0 none, 1 text, 2 yes/no, 3 4-choice, 4 result, 10 ok
        self.b_ = 0      # popup id
        self.d = 0       # timer (200 = wait for key)
        self.e = 0
        self.f = 0
        self.g = 0
        self.h = 0       # height
        self.i = 0       # number of lines
        self.j = 0       # redraw flag
        self.k = 0       # selected button
        self.l = [None] * 10
        self.m = None
        self.n = None
        self.o = None
        self.p = None
        self.q = False
        self.s = False

    def a_v(self):  # l.java:46-60
        self.b = 0
        self.b_ = 0
        self.d = 0
        self.e = 0
        self.f = 0
        self.g = 0
        self.h = 0
        self.i = 0
        self.j = 0
        self.k = 0
        self.q = False
        for b in range(len(self.l)):
            self.l[b] = ""

    def b_v(self):  # l.java:62-324  (keys + timer; returns the chosen button or -1)
        if GameCanvas.ch != 0:
            self.j = 1
            if self.e != 0:
                if (GameCanvas.ch == -5 or GameCanvas.ch == 53) and self.f > 2:
                    self.f = 2
            else:
                if self.b == 1:
                    if GameCanvas.ch == -5 or GameCanvas.ch == 53:
                        if self.a == 1:
                            if self.d > 2 and self.b_ != 20:
                                self.d = 2
                            return -1
                        if GameCanvas.bV != 1:
                            if self.d > 2 and self.b_ != 20:
                                self.d = 2
                        elif self.b_ == 37:
                            self.as_()
                elif self.b == 2:
                    ch = GameCanvas.ch
                    if ch in (-4, -3, 52, 54):
                        self.k = i16(self.k + 1 & 0x1)
                    elif ch in (-5, 53):
                        self.d = 1
                        if self.k == 0:
                            if self.a == 1:
                                self.b = 0
                                self.q = True
                                return -1
                            if self.b_ == 28:
                                self.as_()
                                return -1
                            if GameCanvas.bV == 2:
                                c0 = GameCanvas.cM[0]
                                if c0 == 3:
                                    GameCanvas.cM[0] = 4
                                    GameCanvas.dG = 0
                                    GameCanvas.dH = i16(GameCanvas.dH + 1)
                                    self.am()
                                elif c0 == 5:
                                    if self.b_ == 28:
                                        self.as_()
                                        return -1
                                    if self.b_ == 41 or self.b_ == 42:
                                        # platformRequest(ag.bm / ag.bn): the browser is not opened in the port
                                        if self.b_ == 41:
                                            print("platformRequest:", GameCanvas.bm)
                                        else:
                                            # PORT-EXTRA: the Multiplayer jar is part of the port, so
                                            # main.py starts it after the game exits (no download)
                                            GameCanvas.bs.to_multiplayer = True
                                        GameCanvas.bs.destroyApp(True)
                                        GameCanvas.bs.notifyDestroyed()
                                        return -1
                                    if GameCanvas.cM[1] == 1:
                                        self.au()
                                elif c0 == 8:
                                    GameCanvas.ax()
                                    self.ay()
                                    GameCanvas.eo = GameCanvas.B_v()
                                    if GameCanvas.be is not None:
                                        type(GameCanvas.be).d = True     # as.d = true (static)
                                    if self.ar() != 0:
                                        GameCanvas.bb.c_v()
                                        GameCanvas.dE = GameCanvas.fU
                                        GameCanvas.cM[0] = 0
                                        GameCanvas.cN = consts.v[GameCanvas.cM[0]]
                                        GameCanvas.cM[2] = 0
                                        GameCanvas.cM[1] = 0
                                        self.aA()
                                        self.l_II(100, 0)
                                    else:
                                        GameCanvas.aw()
                                        self.e_I(1)
                                elif c0 == 10:
                                    GameCanvas.aj()
                                    GameCanvas.cM[0] = 5
                                    GameCanvas.cN = 10
                                    GameCanvas.cM[2] = 0
                                    GameCanvas.cM[1] = 0
                                elif c0 == 29:
                                    GameCanvas.bb.c_v()
                                    GameCanvas.cM[0] = 6
                                # break -> leaves both switches, continues with the timer below
                            elif GameCanvas.cR.a == 1:  # l.java:172-182  (pause menu: Exit -> Game Menu)
                                if GameCanvas.cM[1] == 5:
                                    self.al_()
                                    self.w_I(2)
                                    GameCanvas.cM[0] = 5
                                    GameCanvas.cN = 10
                                    GameCanvas.bV = 2
                                    GameCanvas.cL = 0
                                    GameCanvas.cK = 0
                            elif GameCanvas.bV == 0:
                                return 0
                        else:
                            if self.a == 1:
                                self.b = 0
                                return -1
                            if GameCanvas.cM[0] == 8:
                                GameCanvas.aw()
                            return 1
                    elif ch == -7:
                        if GameCanvas.cM[0] == 8:
                            self.d = 1
                            GameCanvas.aw()
                            return 1
                elif self.b == 3:
                    if self.d > 5:
                        ch = GameCanvas.ch
                        if ch in (-1, 50):
                            self.k = i16(self.k - 1)
                            self.k = i16(self.k & 0x3)
                        elif ch in (-2, 56):
                            self.k = i16(self.k + 1)
                            self.k = i16(self.k & 0x3)
                        elif ch in (-5, 53):
                            self.d = 4
                elif self.b == 10:
                    if GameCanvas.ch == -5 or GameCanvas.ch == 53:
                        self.d = 2
                        GameCanvas.cS.b = 0
                        self.q = True
                        GameCanvas.ck = 1
        return self._timer()

    def _timer(self):  # l.java:229-323  (the part of b() after the key switch)
        if self.e != 0:
            self.f = i16(self.f - 1)
            if self.f < 1:
                self.e = 0
                GameCanvas.ck = 1
        else:
            if self.d < 200:
                self.d = i16(self.d - 1)
            if self.d == 0:
                self.b = 0
                GameCanvas.ck = 1
                v = self.b_
                if v in (1, 18):
                    self.as_()
                elif v == 15:
                    GameCanvas.cM[0] = 0
                    for b in range(5):
                        GameCanvas.gf[b] = ""
                    GameCanvas.ap()
                    GameCanvas.dE = GameCanvas.fU
                elif v == 39:
                    GameCanvas.cM[0] = 12
                    GameCanvas.cN = consts.v[GameCanvas.cM[0]]
                    GameCanvas.cM[1] = 3
                elif v == 14:
                    from pow.game.menus import Menus
                    GameCanvas.fD += 1
                    GameCanvas.fI = self.k
                    Menus.a_II(0, (GameCanvas.fF << 2) + 2 + self.k)
                    GameCanvas.fw[GameCanvas.fD & 0x1] = GameCanvas.gf[3]
                elif v == 16:
                    from pow.game.menus import Menus
                    GameCanvas.cz.S = 0
                    GameCanvas.bb.o_v()
                    if GameCanvas.fu != 0:
                        GameCanvas.fu = i16(Menus.b_II(GameCanvas.fn[2][GameCanvas.fv], 5))
                    else:
                        GameCanvas.fu = i16(Menus.b_II(GameCanvas.fn[0][GameCanvas.fH], 5))
                    self.ar()
                    self.e_I(15)
                elif v == 9:  # room cleared: the exits open, or the mission's general talks
                    if GameCanvas.eO[GameCanvas.eP].o != 0:
                        GameCanvas.bd.g_v()
                    else:
                        GameCanvas.co = 1
                        GameCanvas.cn = 5
                elif v == 10:  # l.java:257-260  (Mission Success -> Total Exp)
                    from pow.game.map_scene import MapScene
                    self.e_I(11)
                    MapScene.h_v()
                elif v == 11:  # l.java:261-268  (Total Exp -> Time Exp, if in time)
                    if GameCanvas.dX < GameCanvas.dz[GameCanvas.dm].i:
                        self.e_I(12)
                        GameCanvas.ea = 0
                    else:
                        GameCanvas.bd.d_I(1)
                elif v == 12:  # l.java:269-271
                    GameCanvas.bd.d_I(1)
                elif v == 22:  # l.java:300-315  (Mission fail -> Game Menu)
                    if GameCanvas.dz[GameCanvas.dm].g > 200:
                        GameCanvas.bd.d_I(0)
                    else:
                        self.w_I(2)
                        self.F_v()
                        GameCanvas.cM[0] = 0
                        GameCanvas.cN = consts.v[GameCanvas.cM[0]]
                        GameCanvas.dE = GameCanvas.fU
                        GameCanvas.bV = 2
                        GameCanvas.ck = 1
                        GameCanvas.cL = 0
                        GameCanvas.cK = 0
        return -1

    def c_v(self):  # l.java:326-397  (draw)
        i = -(self.h >> 1)
        if self.b == 4:
            i += 20
        if GameCanvas.bV == 3 or GameCanvas.bW == 3:
            i -= 30
        self.b_I(self.h)
        Gfx.a_Lg(GameCanvas.bu)
        for b in range(self.i):
            self.b_TII(self.l[b], GameCanvas.de + i, 0)
            i += 20
        if self.b == 10:
            self.c_I(GameCanvas.de + self.h // 2 - 18)
        elif self.b == 2:
            self.O_I(GameCanvas.de + i + 5)
        elif self.b == 3:
            i += 5
            for b in range(4):
                if self.k == b:
                    Gfx.a_Lg(GameCanvas.bw)
                else:
                    Gfx.a_Lg(GameCanvas.bu)
                self.b_TII(self.l[b + 2], GameCanvas.de + i, 0)
                i += 16
        elif self.b == 4:  # l.java:357-381  (mission result: gold / total exp / time exp)
            if GameCanvas.bV == 3:
                GameCanvas.de -= 30
            self.b_TII(GameCanvas.dl, GameCanvas.de - 75, len(GameCanvas.dl) + 1)
            if self.b_ == 10:
                j_ = GameCanvas.dz[GameCanvas.dm].h * 150 * (1 + (GameCanvas.ep ^ 0x1))
                self.b_TII("Gold Acquired!", GameCanvas.de + 10, len("Gold Acquired!") + 1)
                self.d_IIII(j_, GameCanvas.dd + (GameCanvas.D_I(j_) * 9 >> 1) - GameCanvas.db, GameCanvas.de + 30, 0)
            elif self.b_ == 11:
                self.b_TII("Total Exp", GameCanvas.de, len("Total Exp") + 1)
            elif self.b_ == 12:
                self.b_TII("Time Exp", GameCanvas.de - 7, len("Time Exp") + 1)
                GameCanvas.d_TII("Time Limit:", GameCanvas.dd - 78 - GameCanvas.db, GameCanvas.de - 7 + 20)
                self.j_III(GameCanvas.dd + 34 - GameCanvas.db, GameCanvas.de - 7 + 21, GameCanvas.dz[GameCanvas.dm].i)
                GameCanvas.d_TII("Ested Time:", GameCanvas.dd - 78 - GameCanvas.db, GameCanvas.de - 7 + 40)
                self.j_III(GameCanvas.dd + 34 - GameCanvas.db, GameCanvas.de - 7 + 41, GameCanvas.dX)
            if GameCanvas.bV == 3:
                GameCanvas.de += 30
        if self.e != 0:
            self.b_I(self.g)
            if GameCanvas.bV == 3:
                GameCanvas.de -= 30
            self.b_TII(self.l[5], GameCanvas.de - (self.g >> 1) - 3, 0)
            if GameCanvas.bV == 3:
                GameCanvas.de += 30
        if self.s:
            self.c_I(GameCanvas.de + i - 10)
        self.j = 0

    def b_I(self, paramInt):  # l.java:399-423  (popup frame)
        i = GameCanvas.de - (paramInt >> 1) - 10
        if Popups.r is None:
            Popups.r = self.d_T(GameCanvas.bA.a_I(33))
        r = Popups.r
        if (GameCanvas.bV == 3 or GameCanvas.bW == 3) and not GameCanvas.bS:
            i -= 30
        for b in range(26):
            self.b_MIIIIII(r, GameCanvas.dd - 103 + b * 8 - GameCanvas.db, i, 8, 3, 10, 0)
        self.a_IIII(GameCanvas.dd - 102 - GameCanvas.db, i + 3, 210, paramInt + 14)
        self.b_MIIIIII(r, GameCanvas.dd - 105 - GameCanvas.db, i, 3, 10, 0, 0)
        self.b_MIIIIII(r, GameCanvas.dd + 104 - GameCanvas.db, i, 3, 10, 2, 0)
        i += 10
        arrayOfInt = [[GameCanvas.dd - 105 - GameCanvas.db, 162, 162, 162, GameCanvas.dd + 106 - GameCanvas.db],
                      [GameCanvas.dd - 104 - GameCanvas.db, 67, 67, 67, GameCanvas.dd + 105 - GameCanvas.db],
                      [GameCanvas.dd - 103 - GameCanvas.db, 33, 33, 33, GameCanvas.dd + 104 - GameCanvas.db]]
        for b in range(3):
            col = GameCanvas.k_III(arrayOfInt[b][1], arrayOfInt[b][2], arrayOfInt[b][3])
            Gfx.c_IIIII(arrayOfInt[b][0] + GameCanvas.db, i + GameCanvas.dc, arrayOfInt[b][0] + GameCanvas.db, i + paramInt - 1 + GameCanvas.dc, col)
            Gfx.c_IIIII(arrayOfInt[b][4] + GameCanvas.db, i + GameCanvas.dc, arrayOfInt[b][4] + GameCanvas.db, i + paramInt - 1 + GameCanvas.dc, col)
        i += paramInt
        self.b_MIIIIII(r, GameCanvas.dd - 105 - GameCanvas.db, i, 3, 10, 5, 0)
        self.b_MIIIIII(r, GameCanvas.dd + 104 - GameCanvas.db, i, 3, 10, 7, 0)
        i += 7
        for b in range(26):
            self.b_MIIIIII(r, GameCanvas.dd - 103 + b * 8 - GameCanvas.db, i, 8, 3, 10, 3)

    def a_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # l.java:425-446  (tiled ui_back)
        if GameCanvas.ct[10] is None:
            GameCanvas.ct[10] = self.d_T(GameCanvas.bA.a_I(59))
        b = 0
        while b * 24 < paramInt4:
            if paramInt4 >= (b + 1) * 24:
                i = 24
            else:
                i = paramInt4 - b * 24
            b1 = 0
            while b1 * 52 < paramInt3:
                if paramInt3 >= (b1 + 1) * 52:
                    j_ = 52
                else:
                    j_ = paramInt3 - b1 * 52
                if GameCanvas.ct[10] is not None:
                    self.b_MIIIIII(GameCanvas.ct[10], paramInt1 + b1 * 52, paramInt2 + b * 24, j_, i, 0, 0)
                b1 += 1
            b += 1

    def O_I(self, paramInt):  # l.java:448-461  (Yes / No buttons)
        for b in range(2):
            if self.k == b:
                Gfx.a_Lg(GameCanvas.bu)
                bool_ = True
            else:
                Gfx.a_Lg(GameCanvas.bx)
                bool_ = False
            self.a_IIIIZ(GameCanvas.dd - 60 + b * 80, paramInt + GameCanvas.dc, 40, 17, bool_)
            GameCanvas.c_TII(consts.aZ[b], GameCanvas.dd - 40 + b * 80, paramInt + 1)

    def c_I(self, paramInt):  # l.java:463-467  (Ok button)
        Gfx.a_Lg(GameCanvas.bu)
        self.a_IIIIZ(GameCanvas.dd - 60 + 40 + GameCanvas.db, paramInt + GameCanvas.dc, 40, 17, True)
        GameCanvas.c_TII(consts.aZ[2], GameCanvas.dd, paramInt)

    def a_T(self, paramString):  # l.java:469-496  ("<kind>line|line|...")
        self.s = False
        i = 1
        if paramString != "":
            self.b = i16(ord(paramString[0]) - 48)
            if self.b == 3:
                self.b = 10
                self.d = 200
            s = 0
            for b in range(len(paramString)):
                if paramString[b] == '|':
                    # DECOMP-FIX F9 (proposed): decompiled `s = s + 1; l[s] = ...` is `l[s++] = ...`;
                    # literally, line 0 keeps stale text and the last line is never drawn.
                    if config.DECOMP_FIX["F9"]:
                        self.l[s] = paramString[i:b]
                        s = i16(s + 1)
                    else:
                        s = i16(s + 1)
                        self.l[s] = paramString[i:b]
                    i = b + 1
            if config.DECOMP_FIX["F9"]:
                self.l[s] = paramString[i:]
                s = i16(s + 1)
            else:
                s = i16(s + 1)
                self.l[s] = paramString[i:]
            self.i = s
            self.h = i16(20 * s + (s - 1) * 2)
            if self.b == 2 or self.b == 10:
                self.h = i16(self.h + 20)
            if self.d == 0:
                self.d = 10
            self.j = 1

    def d_I(self, paramInt):  # l.java:506-598  (gamestr popup N: text gamestr[N+15], kind from its first digit)
        from pow.game.menus import Menus
        self.a = 1
        self.s = False
        if GameCanvas.bV == 3:
            GameCanvas.ck = 1
        else:
            GameCanvas.cS.j = 1
        self.k = 0
        self.b_ = i16(paramInt)
        str1 = GameCanvas.M_I(paramInt + 15)
        c = str1[0]
        if '0' <= c <= '9':
            self.b = i16(ord(c) - 48)
            if self.b != 2:
                self.b = 10
            str2 = str1[1:]
        else:
            self.b = 10
            str2 = str1
        self.d = 200
        i = len(str2)
        b2 = 0
        j = 0
        for b1 in range(i + 1):
            if b1 == i or str2[b1] == '\\':
                if j == b1:
                    self.l[b2] = " "
                else:
                    self.l[b2] = str2[j:b1]
                b2 += 1
                j = b1 + 1
        self.i = i16(b2)
        if paramInt == 53:
            self.i = 4
            self.l[0] = self.m
            self.l[1] = self.n
            self.l[2] = self.o
            self.l[3] = self.p
        elif paramInt == 34:
            self.l[0] = Menus.c_I(GameCanvas.fK[19])
            self.l[1] = self.l[1] + self.m
        elif paramInt == 35:
            self.l[1] = self.l[1] + " " + Menus.c_I(GameCanvas.fK[19])
        elif paramInt == 39:
            self.l[3] = self.m + "?"
        elif paramInt == 40:
            self.l[0] = self.m
        elif paramInt == 41:
            self.l[0] = self.m + " " + self.l[0]
            self.l[1] = self.n + " " + self.l[1]
            self.l[4] = self.o + " Level up"
        elif paramInt == 49:
            self.l[1] = self.n
            self.l[2] = self.m
            self.i = 3
        elif paramInt == 54:
            self.l[0] = "You can't use the ID."
            self.i = 1
        self.h = i16(20 * self.i + (self.i - 1 << 1))
        if self.b == 2:
            self.h = i16(self.h + 25)
        elif self.b == 3:
            self.h = 140
        elif self.b == 4:
            self.h = 150
        elif self.b == 10:
            self.h = i16(self.h + 30)
        GameCanvas.ck = 1
        if GameCanvas.be is not None:
            from pow.game.live import Live
            Live.aJ()

    @staticmethod
    def d_v():  # l.java:498-500  (Blacksmith: bought)
        from pow.game.menus import Menus
        return " You bought|1 " + Menus.c_I(GameCanvas.fK[19]) + '.'

    @staticmethod
    def e_v():  # l.java:502-504  (Blacksmith: sold)
        from pow.game.menus import Menus
        return " You sold|" + Menus.c_I(GameCanvas.fK[19]) + '.'

    def e_I(self, paramInt):  # l.java:600-891
        self.a = 0
        self.s = False
        arrayOfByte1 = [2, 2, 2, 4, 3, 3, 5, 3, 3, 3, 2, 2, 2, 2, 2, 5, 3, 2, 2, 3,
                        2, 4, 3, 2, 2, 2, 2, 0, 2, 3, 1, 1, 1, 1, 4, 4, 4, 1, 5, 5, 2, 5, 6]
        arrayOfByte2 = [1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 4, 4, 4, 1, 3, 1, 1, 1, 1, 2,
                        1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 10, 2, 1, 1, 1, 2, 2, 2]
        arrayOfShort = [20, 20, 20, 200, 200, 200, 200, 20, 20, 20, 20, 200, 200, 20, 200, 200, 20, 20, 200, 200,
                        200, 20, 20, 20, 20, 20, 20, 20, 200, 200, 20, 20, 20, 200, 200, 200, 200, 20, 200, 200,
                        200, 200, 200]
        if paramInt == 39:
            self.s = True
        self.b = arrayOfByte2[paramInt]
        if GameCanvas.bV == 3:
            GameCanvas.ck = 1
        else:
            self.j = 1
        self.d = arrayOfShort[paramInt]
        self.i = arrayOfByte1[paramInt]
        self.k = 0
        self.b_ = paramInt
        L = self.l
        p = paramInt
        if p in _E_TEXT:
            for n, s in enumerate(_E_TEXT[p]):
                L[n] = s
            if p in (5, 28):
                self.k = 1
        elif p == 14:
            L[0] = "What do you want"
            L[1] = "to talk about?"
            for i in range(4):
                L[i + 2] = consts.ba[i]
        elif p in (23, 24, 25, 26):
            L[0] = {23: " / Hp 5 Increased", 24: " / MP 3 Increased",
                    25: " / DEF 1 Increased", 26: " / ATK 1 Increased"}[p][3:]
            L[1] = ""
        elif p == 6:
            dz = GameCanvas.dz[GameCanvas.dm]
            self.B_I(dz.e)
            GameCanvas.cT[0] = GameCanvas.dC.a
            GameCanvas.cT[1] = "Lv" + str(GameCanvas.cz.l + dz.j) + " / Gold: " + str(dz.h * 150 * (1 + (GameCanvas.ep ^ 0x1)))
            L[0] = GameCanvas.cT[0]
            L[1] = GameCanvas.cT[1]
            L[2] = "Do you want to"
            L[3] = "accept this"
            L[4] = "mission?"
        elif p == 15:
            GameCanvas.cT[1] = GameCanvas.dC.a
            L[0] = "You visited"
            L[1] = GameCanvas.cT[1] + '.'
            if GameCanvas.fu != 0:
                L[2] = "Friendship:100%"
            else:
                L[2] = "Friendship "
                L[3] = "increased by 5."
            if GameCanvas.fJ < 8:
                L[5] = GameCanvas.cT[0]
                self.i = i16(self.i + 1)
            else:
                L[4] = ""
                L[5] = "Press OK"
                self.i = i16(self.i + 1)
            self.a__I(10)
        elif p == 16:
            L[0] = "You discussed"
            GameCanvas.cT[0] = consts.ba[GameCanvas.fI] + " with"
            L[1] = GameCanvas.cT[0]
            GameCanvas.cT[1] = GameCanvas.dC.a + '.'
            L[2] = GameCanvas.cT[1]
        elif p in (8, 9):  # l.java:679-689  (room / stage banner on the map)
            GameCanvas.cT[0] = "Stage " + str(GameCanvas.do)
            if p == 9:
                GameCanvas.cT[0] = GameCanvas.cT[0] + " Complete."
                self.a__I(5)
            L[0] = GameCanvas.dl
            L[1] = GameCanvas.dn
            L[2] = GameCanvas.cT[0]
        elif p == 10:  # l.java:690-693
            L[0] = GameCanvas.dn
            L[1] = "Mission Success"
        elif p == 13:  # l.java:694-698  (item picked up)
            GameCanvas.cT[0] = GameCanvas.cX.a
            L[0] = GameCanvas.cT[0]
            L[1] = "Acquired!!"
        elif p == 22:  # l.java:740-762  (mission failed: maybe an item is lost)
            L[0] = GameCanvas.dl
            L[1] = GameCanvas.dn
            L[2] = "Mission fail!"
            if GameCanvas.cz.l > 9 and self.C_I(100) < GameCanvas.cz.l >> 2:
                i = self.C_I(9)
                if GameCanvas.cz.X[i].a != 0:
                    GameCanvas.bb.e_I(GameCanvas.cz.X[i].a)
                    if GameCanvas.cz.X[i].a < 300:
                        GameCanvas.cT[0] = GameCanvas.cX.a
                    elif GameCanvas.cz.X[i].a < 500:
                        GameCanvas.cT[0] = GameCanvas.cY.a
                    else:
                        GameCanvas.cT[0] = GameCanvas.cZ.a
                    GameCanvas.cz.X[i] = None
                    L[3] = "Lost!!"
                    L[4] = GameCanvas.cT[0]
                    self.i = i16(self.i + 2)
            self.a__I(6)
        elif p == 27:  # l.java:779-809  (reward item / hidden mission after the ending)
            if GameCanvas.ef != 0:
                if GameCanvas.ef == 502:
                    GameCanvas.cT[0] = " / Catherine's scarf"[3:]
                else:
                    GameCanvas.bb.e_I(GameCanvas.ef)
                    GameCanvas.cT[0] = GameCanvas.cX.a
                L[0] = GameCanvas.cT[0]
                self.i = i16(self.i + 1)
                L[1] = "received!"
                self.i = i16(self.i + 1)
            if GameCanvas.eg != 0:
                # DECOMP-FIX F19: decompiled `i = i + 1; l[i] = ...` is `l[i++] = ...` (as in F9 and in
                # the ef lines just above). Literally l[0] (eg only) or l[2] (ef and eg) is never
                # written and stays None -> the popup's draw fails and the screen after the ending
                # lore stays dark with only SKIP; the hidden mission's name is never drawn.
                f19 = config.DECOMP_FIX["F19"]
                if GameCanvas.ef != 0:
                    if f19:
                        L[self.i] = ""
                        self.i = i16(self.i + 1)
                    else:
                        self.i = i16(self.i + 1)
                        L[self.i] = ""
                arrayOfByte = GameCanvas.v_I(48)
                j_ = 38 * GameCanvas.eg + 10
                b = 0
                while b < 30 and arrayOfByte[j_ + b] != 0:
                    b += 1
                GameCanvas.dt[0] = GameCanvas.a_ABII(arrayOfByte, j_, j_ + b)
                if f19:
                    L[self.i] = "Hidden Mission!"
                    self.i = i16(self.i + 1)
                else:
                    self.i = i16(self.i + 1)
                    L[self.i] = "Hidden Mission!"
                GameCanvas.cT[1] = GameCanvas.dt[0]
                if f19:
                    L[self.i] = GameCanvas.cT[1]
                    self.i = i16(self.i + 1)
                else:
                    self.i = i16(self.i + 1)
                    L[self.i] = GameCanvas.cT[1]
        self.h = i16(20 * self.i + (self.i - 1 << 1))
        if self.b == 2:
            self.h = i16(self.h + 25)
        elif self.b == 3:
            self.h = 140
        elif self.b == 4:
            self.h = 150
        elif self.b == 10:
            self.h = i16(self.h + 25)
        GameCanvas.ck = 1


# l.java:640-868 - the plain-text cases of e(int), copied 1:1
_E_TEXT = {
    0: ["Saving", "Success!"],
    1: ["Not enough", "FreeSpace."],
    2: ["Not athorized", "Letter."],
    3: ["Starting a new game", "will cause your saved", "game to be deleted.", "Continue?"],
    4: ["Character settings", "are complete.", "Continue?"],
    5: ["Exit Game", "and go to", "main menu?"],
    7: ["Can't Save!", "it Needs all", "enemy dead."],
    17: ["You can't take", "this equipment."],
    18: ["Data is crashed", "Shutting down.."],
    28: ["Exit Game?", ""],
    30: ["Wait.."],
    31: ["Wait..."],
    32: ["Wait...."],
    35: ["Generals can not be", "visited at this time.", "Try again after", "completing a mission."],
    36: ["Difficulty will", "not change", "after starting.", "Continue?"],
    38: ["Not enough", "FreeSpace.", "Please delete", "some files", "before starting."],
    39: ["You must have", "at least 3 items", "in order to have", "them combined.", ""],
    40: ["Would you like", "sound enabled?"],
    41: ["Accessing 'More Games'", "will exit the game", "and open the browser.", "Would you like", "to continue?"],
    # PORT-EXTRA: the original text was "exit the game and open the browser to allow downloading of
    # the Multiplayer version"; in the port YES starts the Multiplayer game itself (main.py)
    42: ["Selecting YES will", "exit the game and", "start the online", "game: Path of a",
         "Warrior Multiplayer.", "Continue?"],
}
