"""l.java - popups (cS). Literal port, Phase 0 subset.

Ported: drawing (c, b(int), a(4 ints), O, c(int)), text popups a(String) and e(int) with all
plain-text messages, and the key/timer logic b() for the branches the menus reach.
Branches that need map/combat/campaign code raise NotPorted.
"""
import config
from pow.game import ae
from pow.game.ag import ag, not_ported
from pow.game.x import x
from pow.midp.jint import i16


class l(ag):
    r = None  # public static Image r = null;  l.java:38  (ui_popup)

    def __init__(self):  # l.java:42-44
        super().__init__(ag.bs)
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
        if ag.ch != 0:
            self.j = 1
            if self.e != 0:
                if (ag.ch == -5 or ag.ch == 53) and self.f > 2:
                    self.f = 2
            else:
                if self.b == 1:
                    if ag.ch == -5 or ag.ch == 53:
                        if self.a == 1:
                            if self.d > 2 and self.b_ != 20:
                                self.d = 2
                            return -1
                        if ag.bV != 1:
                            if self.d > 2 and self.b_ != 20:
                                self.d = 2
                        elif self.b_ == 37:
                            self.as_()
                elif self.b == 2:
                    ch = ag.ch
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
                            if ag.bV == 2:
                                c0 = ag.cM[0]
                                if c0 == 3:
                                    ag.cM[0] = 4
                                    ag.dG = 0
                                    ag.dH = i16(ag.dH + 1)
                                    self.am()
                                elif c0 == 5:
                                    if self.b_ == 28:
                                        self.as_()
                                        return -1
                                    if self.b_ == 41 or self.b_ == 42:
                                        # platformRequest(ag.bm / ag.bn): the browser is not opened in the port
                                        print("platformRequest:", ag.bm if self.b_ == 41 else ag.bn)
                                        ag.bs.destroyApp(True)
                                        ag.bs.notifyDestroyed()
                                        return -1
                                    if ag.cM[1] == 1:
                                        self.au()
                                elif c0 == 8:
                                    ag.ax()
                                    self.ay()
                                    ag.eo = ag.B_v()
                                    if ag.be is not None:
                                        type(ag.be).d = True     # as.d = true (static)
                                    if self.ar() != 0:
                                        ag.bb.c_v()
                                        ag.dE = ag.fU
                                        ag.cM[0] = 0
                                        ag.cN = ae.v[ag.cM[0]]
                                        ag.cM[2] = 0
                                        ag.cM[1] = 0
                                        self.aA()
                                        self.l_II(100, 0)
                                    else:
                                        ag.aw()
                                        self.e_I(1)
                                elif c0 == 10:
                                    ag.aj()
                                    ag.cM[0] = 5
                                    ag.cN = 10
                                    ag.cM[2] = 0
                                    ag.cM[1] = 0
                                elif c0 == 29:
                                    ag.bb.c_v()
                                    ag.cM[0] = 6
                                # break -> leaves both switches, continues with the timer below
                            elif ag.cR.a == 1:  # l.java:172-182  (pause menu: Exit -> Game Menu)
                                if ag.cM[1] == 5:
                                    self.al_()
                                    self.w_I(2)
                                    ag.cM[0] = 5
                                    ag.cN = 10
                                    ag.bV = 2
                                    ag.cL = 0
                                    ag.cK = 0
                            elif ag.bV == 0:
                                return 0
                        else:
                            if self.a == 1:
                                self.b = 0
                                return -1
                            if ag.cM[0] == 8:
                                ag.aw()
                            return 1
                    elif ch == -7:
                        if ag.cM[0] == 8:
                            self.d = 1
                            ag.aw()
                            return 1
                elif self.b == 3:
                    if self.d > 5:
                        ch = ag.ch
                        if ch in (-1, 50):
                            self.k = i16(self.k - 1)
                            self.k = i16(self.k & 0x3)
                        elif ch in (-2, 56):
                            self.k = i16(self.k + 1)
                            self.k = i16(self.k & 0x3)
                        elif ch in (-5, 53):
                            self.d = 4
                elif self.b == 10:
                    if ag.ch == -5 or ag.ch == 53:
                        self.d = 2
                        ag.cS.b = 0
                        self.q = True
                        ag.ck = 1
        return self._timer()

    def _timer(self):  # l.java:229-323  (the part of b() after the key switch)
        if self.e != 0:
            self.f = i16(self.f - 1)
            if self.f < 1:
                self.e = 0
                ag.ck = 1
        else:
            if self.d < 200:
                self.d = i16(self.d - 1)
            if self.d == 0:
                self.b = 0
                ag.ck = 1
                v = self.b_
                if v in (1, 18):
                    self.as_()
                elif v == 15:
                    ag.cM[0] = 0
                    for b in range(5):
                        ag.gf[b] = ""
                    ag.ap()
                    ag.dE = ag.fU
                elif v == 39:
                    ag.cM[0] = 12
                    ag.cN = ae.v[ag.cM[0]]
                    ag.cM[1] = 3
                elif v == 14:
                    from pow.game.e import e
                    ag.fD += 1
                    ag.fI = self.k
                    e.a_II(0, (ag.fF << 2) + 2 + self.k)
                    ag.fw[ag.fD & 0x1] = ag.gf[3]
                elif v == 16:
                    from pow.game.e import e
                    ag.cz.S = 0
                    ag.bb.o_v()
                    if ag.fu != 0:
                        ag.fu = i16(e.b_II(ag.fn[2][ag.fv], 5))
                    else:
                        ag.fu = i16(e.b_II(ag.fn[0][ag.fH], 5))
                    self.ar()
                    self.e_I(15)
                elif v == 9:  # room cleared: the exits open, or the mission's general talks
                    if ag.eO[ag.eP].o != 0:
                        ag.bd.g_v()
                    else:
                        ag.co = 1
                        ag.cn = 5
                elif v in (10, 11, 12, 22):
                    not_ported("l.b timer b_=%d (map/combat)" % v)
        return -1

    def c_v(self):  # l.java:326-397  (draw)
        i = -(self.h >> 1)
        if self.b == 4:
            i += 20
        if ag.bV == 3 or ag.bW == 3:
            i -= 30
        self.b_I(self.h)
        x.a_Lg(ag.bu)
        for b in range(self.i):
            self.b_TII(self.l[b], ag.de + i, 0)
            i += 20
        if self.b == 10:
            self.c_I(ag.de + self.h // 2 - 18)
        elif self.b == 2:
            self.O_I(ag.de + i + 5)
        elif self.b == 3:
            i += 5
            for b in range(4):
                if self.k == b:
                    x.a_Lg(ag.bw)
                else:
                    x.a_Lg(ag.bu)
                self.b_TII(self.l[b + 2], ag.de + i, 0)
                i += 16
        elif self.b == 4:
            not_ported("l.c kind 4 (mission result)")
        if self.e != 0:
            self.b_I(self.g)
            if ag.bV == 3:
                ag.de -= 30
            self.b_TII(self.l[5], ag.de - (self.g >> 1) - 3, 0)
            if ag.bV == 3:
                ag.de += 30
        if self.s:
            self.c_I(ag.de + i - 10)
        self.j = 0

    def b_I(self, paramInt):  # l.java:399-423  (popup frame)
        i = ag.de - (paramInt >> 1) - 10
        if l.r is None:
            l.r = self.d_T(ag.bA.a_I(33))
        r = l.r
        if (ag.bV == 3 or ag.bW == 3) and not ag.bS:
            i -= 30
        for b in range(26):
            self.b_MIIIIII(r, ag.dd - 103 + b * 8 - ag.db, i, 8, 3, 10, 0)
        self.a_IIII(ag.dd - 102 - ag.db, i + 3, 210, paramInt + 14)
        self.b_MIIIIII(r, ag.dd - 105 - ag.db, i, 3, 10, 0, 0)
        self.b_MIIIIII(r, ag.dd + 104 - ag.db, i, 3, 10, 2, 0)
        i += 10
        arrayOfInt = [[ag.dd - 105 - ag.db, 162, 162, 162, ag.dd + 106 - ag.db],
                      [ag.dd - 104 - ag.db, 67, 67, 67, ag.dd + 105 - ag.db],
                      [ag.dd - 103 - ag.db, 33, 33, 33, ag.dd + 104 - ag.db]]
        for b in range(3):
            col = ag.k_III(arrayOfInt[b][1], arrayOfInt[b][2], arrayOfInt[b][3])
            x.c_IIIII(arrayOfInt[b][0] + ag.db, i + ag.dc, arrayOfInt[b][0] + ag.db, i + paramInt - 1 + ag.dc, col)
            x.c_IIIII(arrayOfInt[b][4] + ag.db, i + ag.dc, arrayOfInt[b][4] + ag.db, i + paramInt - 1 + ag.dc, col)
        i += paramInt
        self.b_MIIIIII(r, ag.dd - 105 - ag.db, i, 3, 10, 5, 0)
        self.b_MIIIIII(r, ag.dd + 104 - ag.db, i, 3, 10, 7, 0)
        i += 7
        for b in range(26):
            self.b_MIIIIII(r, ag.dd - 103 + b * 8 - ag.db, i, 8, 3, 10, 3)

    def a_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # l.java:425-446  (tiled ui_back)
        if ag.ct[10] is None:
            ag.ct[10] = self.d_T(ag.bA.a_I(59))
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
                if ag.ct[10] is not None:
                    self.b_MIIIIII(ag.ct[10], paramInt1 + b1 * 52, paramInt2 + b * 24, j_, i, 0, 0)
                b1 += 1
            b += 1

    def O_I(self, paramInt):  # l.java:448-461  (Yes / No buttons)
        for b in range(2):
            if self.k == b:
                x.a_Lg(ag.bu)
                bool_ = True
            else:
                x.a_Lg(ag.bx)
                bool_ = False
            self.a_IIIIZ(ag.dd - 60 + b * 80, paramInt + ag.dc, 40, 17, bool_)
            ag.c_TII(ae.aZ[b], ag.dd - 40 + b * 80, paramInt + 1)

    def c_I(self, paramInt):  # l.java:463-467  (Ok button)
        x.a_Lg(ag.bu)
        self.a_IIIIZ(ag.dd - 60 + 40 + ag.db, paramInt + ag.dc, 40, 17, True)
        ag.c_TII(ae.aZ[2], ag.dd, paramInt)

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

    def d_I(self, paramInt):  # l.java:506-598
        not_ported("l.d(int) (gamestr popups)")

    @staticmethod
    def d_v():  # l.java:498-500  (Blacksmith: bought)
        from pow.game.e import e
        return " You bought|1 " + e.c_I(ag.fK[19]) + '.'

    @staticmethod
    def e_v():  # l.java:502-504  (Blacksmith: sold)
        from pow.game.e import e
        return " You sold|" + e.c_I(ag.fK[19]) + '.'

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
        if ag.bV == 3:
            ag.ck = 1
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
                L[i + 2] = ae.ba[i]
        elif p in (23, 24, 25, 26):
            L[0] = {23: " / Hp 5 Increased", 24: " / MP 3 Increased",
                    25: " / DEF 1 Increased", 26: " / ATK 1 Increased"}[p][3:]
            L[1] = ""
        elif p == 6:
            dz = ag.dz[ag.dm]
            self.B_I(dz.e)
            ag.cT[0] = ag.dC.a
            ag.cT[1] = "Lv" + str(ag.cz.l + dz.j) + " / Gold: " + str(dz.h * 150 * (1 + (ag.ep ^ 0x1)))
            L[0] = ag.cT[0]
            L[1] = ag.cT[1]
            L[2] = "Do you want to"
            L[3] = "accept this"
            L[4] = "mission?"
        elif p == 15:
            ag.cT[1] = ag.dC.a
            L[0] = "You visited"
            L[1] = ag.cT[1] + '.'
            if ag.fu != 0:
                L[2] = "Friendship:100%"
            else:
                L[2] = "Friendship "
                L[3] = "increased by 5."
            if ag.fJ < 8:
                L[5] = ag.cT[0]
                self.i = i16(self.i + 1)
            else:
                L[4] = ""
                L[5] = "Press OK"
                self.i = i16(self.i + 1)
            self.a__I(10)
        elif p == 16:
            L[0] = "You discussed"
            ag.cT[0] = ae.ba[ag.fI] + " with"
            L[1] = ag.cT[0]
            ag.cT[1] = ag.dC.a + '.'
            L[2] = ag.cT[1]
        elif p in (8, 9):  # l.java:679-689  (room / stage banner on the map)
            ag.cT[0] = "Stage " + str(ag.do)
            if p == 9:
                ag.cT[0] = ag.cT[0] + " Complete."
                self.a__I(5)
            L[0] = ag.dl
            L[1] = ag.dn
            L[2] = ag.cT[0]
        elif p == 10:  # l.java:690-693
            L[0] = ag.dn
            L[1] = "Mission Success"
        elif p == 13:  # l.java:694-698  (item picked up)
            ag.cT[0] = ag.cX.a
            L[0] = ag.cT[0]
            L[1] = "Acquired!!"
        elif p in (22, 27):
            not_ported("l.e(%d) (mission failed / ending reward)" % p)
        self.h = i16(20 * self.i + (self.i - 1 << 1))
        if self.b == 2:
            self.h = i16(self.h + 25)
        elif self.b == 3:
            self.h = 140
        elif self.b == 4:
            self.h = 150
        elif self.b == 10:
            self.h = i16(self.h + 25)
        ag.ck = 1


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
    42: ["Selecting YES will", "exit the game and open", "the browser to allow", "downloading of the",
         "Multiplayer version.", "Continue?"],
}
