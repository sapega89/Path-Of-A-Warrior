"""c.java - map, combat and the story player (bd). Literal port, partial:
c(int) (one page of a prologue / epilogue) and d(int) / g() (end of a mission) are ported;
the map and combat (phases 3-4) are not."""
from pow.game.ag import ag
from pow.game import ae
from pow.game.j import j
from pow.game.x import x
import config
from pow.midp.jint import i8, i16, i32, idiv

F14 = config.DECOMP_FIX["F14"]


# direction key -> cz.c, as c.i_v reads ag.cj (used by the PORT-EXTRA HOLD_TO_MOVE)
_HELD_DIR = {-1: 4, 50: 4, -3: 2, 52: 2, -4: 6, 54: 6, -2: 0, 56: 0}


class c(ag):
    def __init__(self):  # c.java:4-6
        super().__init__(ag.bs)

    def c_I(self, paramInt):  # c.java:1393-1514  (load story page paramInt)
        arrayOfChar = ['\0'] * 10
        c1 = 0
        str_ = ag.bI.a_I(ag.eb[0] + paramInt)
        if (ag.ec == 0 and paramInt < ag.eb[1] - ag.eb[0]) or (ag.ec != 0 and paramInt >= ag.eb[1] - ag.eb[0]):
            # dialogue page: "[Name] text" typed into one of the two speech boxes
            self.a__I(0)
            str1 = ""
            if '/' < str_[0] < ':':
                ag.gf[0] = ""
                if 0 == ag.ee and paramInt == 2:
                    ag.fE = 0
                    str1 = ag.M_I(1)
                else:
                    b = 0
                    while b < 10:
                        if str_[b] == '|':
                            arrayOfChar[b] = '\0'
                            break
                        arrayOfChar[b] = str_[b]
                        b += 1
                    ag.fE = ag.a_AC(arrayOfChar)
                    ag.dD = len(str_) - b
                    str1 = str_[b + 1:]
                ag.fw[0] = str1
                ag.fG = 0
                ag.fA[0] = 0
            else:
                if ag.ec != 0 and 0 == (paramInt & 0x1):
                    ag.fG = 0
                else:
                    ag.fG = 1
                ag.gf[ag.fG] = str1
                if ag.ec != 0 and 0 == (paramInt & 0x1):
                    str1 = "[Master] " + str_
                else:
                    str1 = "[" + ag.cz.k + "] " + str_
                ag.fw[ag.fG] = str1
                ag.fA[ag.fG] = 0
                return
        else:
            if paramInt == ag.eb[2] - ag.eb[0]:
                # last page of an epilogue: completion statistics
                i = j_ = k = m = 0
                for b1 in range(225):
                    if (ag.dy[b1 >> 5] & i32(1 << (b1 & 0x1F))) != 0:
                        i += 1
                for b in range(45):
                    if b < 24 and (ag.ed & 1 << b) != 0:
                        k += 1
                    if 0 == (0x1FEF64FF7E6F & 1 << b):
                        for b1 in range(5):
                            n = b * 5 + b1
                            if (ag.dy[n >> 5] & i32(1 << (n & 0x1F))) != 0:
                                j_ += 1
                i = i * 100 // 102
                j_ = j_ * 100 // 18
                k = k * 100 // 24
                m = ag.fo * 100 // 44
                dp = ag.dp[0]
                dp[0] = "Mission"
                dp[1] = "Accomplished"
                dp[2] = "" + str(i) + " %"
                dp[3] = "Hidden Mission"
                dp[4] = "Accomplished"
                dp[5] = "" + str(j_) + " %"
                dp[6] = "Ending Collected"
                dp[7] = "" + str(k) + " %"
                dp[8] = "Warrior Collected"
                dp[9] = "" + str(m) + " %"
                dp[10] = "Total Accomplished"
                dp[11] = "" + str(i + j_ + k + m >> 2) + " %"
                ag.dq[0] = 11
                ag.fG = 1
                ag.fA[0] = ag.bY.b
                ag.fC[0] = 0
                return
            # picture page: image + text scrolling up
            self.a__I(2)
            ag.gf[1] = ""
            ag.gf[0] = ""
            if ag.ec != 0:
                b = -1
                if paramInt != 0:
                    c1 = 10
                else:
                    c1 = 1
            elif 0 == ag.ee and paramInt == 5:
                c1 = 0
                b = -1
                str_ = ag.M_I(0)
            else:
                b = 0
                while b < 10:
                    if str_[b] == '|':
                        arrayOfChar[b] = '\0'
                        break
                    arrayOfChar[b] = str_[b]
                    b += 1
                c1 = (ag.a_AC(arrayOfChar) - 1) & 0xFFFF
            str1 = str_[b + 1:]
            self.b_ABII(str1.encode("latin-1"), 200, 0)
            ag.ct[35] = self.d_T(ag.bA.a_I(2 + c1))
            ag.fA[0] = ag.bY.b
            ag.fA[0] = 230
            ag.fC[0] = 0
            ag.fG = 0
            ag.eh = 0

    # ---- end of a mission (called by the combat when the mission is won / lost) -----------

    def d_I(self, paramInt):  # c.java:1516-1607  (mission result: rewards, next chapter cq, ending)
        from pow.game import ae
        from pow.midp.jint import i8, i16, idiv
        arrayOfInt = [0, 0, 0, 0, 0, 0, 11, 8, 0, 15,
                      15, 20, 17, 19, 19, 0, 30, 22, 35, 38,
                      39, 33, 33, 44]
        cz = ag.cz
        dz = ag.dz[ag.dm]
        if paramInt != 0:
            cz.g[dz.a - 1] = i16(cz.g[dz.a - 1] + 5)
            if cz.g[dz.a - 1] > 100:
                cz.g[dz.a - 1] = 100
            ag.dx |= 1 << ag.ds[ag.dk] - 1
            i = (ag.ds[ag.dk] - 1) * 5 + ag.dm
            ag.dy[i >> 5] = ag.dy[i >> 5] | i32(1 << (i & 0x1F))
        ag.cq = i8(ag.ds[ag.dk])
        if dz.f < 200 and paramInt != 0:
            self.g_v()
        else:
            if paramInt != 0:
                i = dz.f - 200
            else:
                i = dz.g - 200
            ag.ck = 1
            self.ac_v()
            self.w_I(2)
            ag.dE = ag.fU
            ag.cO = 0
            if i != 3 or 0 != ag.L_I(502):
                ag.ed |= 1 << i
            if 0 == i:
                b = 0
                j_ = cz.g[1]
                if cz.g[0] + cz.g[15] > j_:
                    j_ = cz.g[0] + cz.g[15]
                    b = 1
                if cz.g[2] + cz.g[10] + cz.g[14] > j_:
                    j_ = cz.g[2] + cz.g[10] + cz.g[14]
                    b = 2
                j_ = idiv(j_ - 20, 10)
                if j_ > 8:
                    j_ = 8
                elif j_ < 0:
                    j_ = 0
                cz.h = i16(b)
                cz.i = i16(j_)
            ag.cq = i8(arrayOfInt[i])
            if 0 == ag.cq:
                for b in range(22):
                    cz.g[b] = 0
            if i == 2:
                ag.ef = 502
            elif self.C_I(10) != 0:
                ag.ef = 0
            else:
                ag.ef = i16(101 + ((4 + 5 * self.C_I(20)) if cz.l // 20 > 4 else (cz.l // 20 + 5 * self.C_I(20))))
            b2 = 0
            ag.eg = 0
            for b1 in range(45):
                if 0 == (ag.dw & 1 << b1):
                    b2 += 1
            if b2 != 0:
                j_ = self.C_I(b2)
                b = 0
                for b1 in range(45):
                    if 0 == (ag.dw & 1 << b1):
                        if j_ == b:
                            ag.dw |= 1 << b1
                            ag.eg = i16(b1 + 1)
                            break
                        b += 1
            if ag.ef != 0 and 0 == self.k_II(ag.ef, 1):
                ag.ef = 0
            self.l_II(i, 1)
        if ag.fo != 0:
            cz.S = 1
        cz.E += dz.h * 150 * (1 + (ag.ep ^ 0x1))
        self.ay()
        ag.dj = 0
        self.ar()

    def g_v(self):  # c.java:1609-1614  (after a won mission: talk with general dz.f, on the map)
        ag.dG = 2
        ag.bV = 5
        self.am()
        ag.ck = 1

    # =========================================================================================
    # The mission map (bV = 3) and its combat. With config.NO_ENEMIES (PORT-EXTRA, off by
    # default) no enemy is created: ez == 0 and every enemy loop below runs zero times.
    # =========================================================================================

    def a_v(self):  # c.java:8-18  (HP / MP balls of the HUD: black cover from the top)
        arrayOfInt = [idiv(35 * ag.cz.p, ag.cz.y), idiv(35 * ag.cz.r, ag.cz.z)]
        arrayOfInt1 = [[4, ag.bZ.b - 61], [201, ag.bZ.b - 61]]
        if ag.gk is None:
            ag.gk = self.d_T("ball_black")
        for b in range(2):
            if arrayOfInt[b] != 0:
                arrayOfInt[b] = 3 if arrayOfInt[b] < 3 else arrayOfInt[b]
            ag.a_IIIIMII(arrayOfInt1[b][0], arrayOfInt1[b][1], ag.gk.getWidth(), ag.gk.getHeight() - arrayOfInt[b],
                         ag.gk, 0, 0)

    @staticmethod
    def a_IIII(paramInt1, paramInt2, paramInt3, paramInt4):  # c.java:20-37  (mark map cells dirty)
        j_ = idiv(paramInt1, 27) - ag.cd
        k = idiv(paramInt2, 27) - ag.ce
        m = idiv(paramInt1 + paramInt3 - 1, 27) - ag.cd
        n = idiv(paramInt2 + paramInt4 - 1, 27) - ag.ce
        if j_ < 0:
            j_ = 0
        if k < 0:
            k = 0
        if m > ag.cb.a - 1:
            m = ag.cb.a - 1
        if n > ag.cb.b - 1:
            n = ag.cb.b - 1
        for i in range(j_, m + 1):
            for i1 in range(k, n + 1):
                ag.eE[i1][i] = 1

    def b_v(self):  # c.java:39-46  (HUD frame)
        cx = ag.cx
        ag.a_IIIIMII(0, 0, cx[1].getWidth(), cx[1].getHeight(), cx[1], 0, 0)
        ag.a_IIIIMII(ag.bZ.a - cx[1].getWidth(), 0, cx[1].getWidth(), cx[1].getHeight(), cx[1], 0, 0)
        ag.a_IIIIMII(0, 2, 120, 25, cx[3], 0, 0)
        ag.a_IIIIMII(ag.bZ.a - 120, 2, 120, 25, cx[4], 1, 0)
        ag.a_IIIIMII(ag.bZ.a // 2 - 120, ag.bZ.b - 61, 120, 61, cx[0], 0, 0)
        ag.a_IIIIMII(ag.bZ.a // 2, ag.bZ.b - 61, 120, 61, cx[2], 0, 0)

    def c_v(self):  # c.java:48-64  (draw one map frame)
        if 0 == ag.cl:
            ag.bc.l_v()
        for b in range(81):
            ag.eE[b // 9][b % 9] = 0
        if 0 == ag.cl:
            ag.bc.m_v()
        self.e_v()
        self.m_v()
        if 0 == ag.cl:
            self.l_v()
        self.k_v()
        self.b_v()
        ag.bc.n_v()
        if ag.co == 1:
            self.j_v()

    def j_v(self):  # c.java:66-79  (blinking exit arrows of the room)
        arrayOfInt1 = [ag.dd - 9, 5, ag.dd - 9, ag.bY.a - 31]
        arrayOfInt2 = [ag.bY.b - 31, ag.de - 13, 5, ag.de - 13]
        if ag.cn < 1:
            ag.cm = i16(ag.cm + 1)
            if (ag.cm & 0x2) != 0:
                for b in range(4):
                    if ag.eO[ag.eP].a[b] != 0 and ag.ct[21 + b] is not None:
                        img = ag.ct[21 + b]
                        self.b_MIIIIII(img, arrayOfInt1[b], arrayOfInt2[b], img.getWidth(), img.getHeight(), 0, 0)
                        c.a_IIII(ag.ca.a + arrayOfInt1[b], ag.ca.b + arrayOfInt2[b], img.getWidth(), img.getHeight())

    def k_v(self):  # c.java:81-122  (arrows flying: eC; only enemies shoot them)
        from pow.game.structs import ac
        ac_ = ac(0, 0, 0, 0)
        for b in range(3):
            eC = ag.eC[b]
            if eC.a != 0:
                ac_.a = i16(eC.b[0].a - ag.ca.a + ag.db)
                ac_.b = i16(eC.b[0].b - ag.ca.b + ag.dc) - 8
                ac_.c = eC.c
                ac_.d = eC.d
                ag.a_LacI(ac_, ag.k_III(245, 206, 116))
                ac_.c -= 1
                ac_.d -= 1
                ag.a_LacI(ac_, ag.k_III(240, 142, 53))
                ac_.c += 1
                ac_.d += 1
                c.a_IIII(eC.b[0].a, eC.b[0].b, eC.c, eC.d)
                bool_ = False
                if ac_.a < ag.db:
                    ac_.c = ag.db - ac_.a
                    if ac_.c > 0:
                        bool_ = True
                if ac_.b < ag.dc:
                    ac_.d = ag.dc - ac_.b
                    if ac_.d > 0:
                        bool_ = True
                if ac_.a + ac_.c >= ag.bY.a + ag.db:
                    ac_.a = ag.bY.a + ag.db
                    ac_.c = ag.db
                    bool_ = True
                if ac_.b + ac_.d >= ag.bY.b + ag.dc:
                    ac_.b = ag.bY.b + ag.dc
                    ac_.d = ag.dc
                    bool_ = True
                if bool_:
                    ag.a_LacI(ac_, 0)
                    c.a_IIII(eC.b[0].a, eC.b[0].b, eC.c, eC.d)

    def d_v(self):  # c.java:124-141  (erase the arrows)
        for b in range(3):
            eC = ag.eC[b]
            if eC.a != 0:
                i = eC.b[1].a - ag.ca.a
                j_ = eC.b[1].b - ag.ca.b - 8
                if (eC.e & 0x1) != 0:
                    b1 = 11
                    b2 = 3
                else:
                    b1 = 3
                    b2 = 11
                self.b_MIIIIII(ag.ct[7], i, j_, b1, b2, i + ag.cc.a, j_ + ag.cc.b)

    def l_v(self):  # c.java:143-156  (upper tile layer over dirty cells)
        cE = ag.cE
        for b in range(ag.cb.a):
            for b1 in range(ag.cb.b):
                if ag.eE[b1][b] != 0:
                    i = (ag.ce + b1) * cE.b.a + ag.cd + b
                    if (cE.a[cE.f + i] & 0x2) != 0 and cE.a[cE.d + i] - 1 >= 0:
                        j_ = ag.cJ[cE.a[cE.d + i] - 1] - 1
                        self.b_MIIIIII(ag.bT[j_], (ag.cd + b) * 27 - ag.ca.a, (ag.ce + b1) * 27 - ag.ca.b, 27, 27, 0, 0)

    def m_v(self):  # c.java:158-226  (skill effects fh == 3 and potion / scroll effect dU)
        arrayOfByte1 = [3, -10, 10]
        arrayOfByte2 = [-6, 0, 5]
        cz = ag.cz
        if ag.fh == 3:
            i = cz.a[0].a - ag.ca.a
            j_ = cz.a[0].b - ag.ca.b
            v = cz.e[0]
            if v == 27:
                if cz.f[0] == 9:
                    i += ae.aA[cz.d[1] >> 1]
                    j_ += ae.aB[cz.d[1] >> 1]
            elif v in (28, 29, 30):
                i = ag.dd
                j_ = ag.de + 11
            arrayOfByte = list(ag.eX[ag.eZ:ag.eZ + ag.fg])
            if len(arrayOfByte) < ag.fg:
                raise IndexError("System.arraycopy")
            self.a_ALyABIII(ag.fj, arrayOfByte, ag.fg, i, j_)
            for b in range(ag.fg):
                c.a_IIII(cz.a[0].a - ag.fj[b].e, cz.a[0].b - ag.fj[b].f, ag.fj[b].c, ag.fj[b].d)
            ag.fg = 1
        dU = ag.dU
        if dU.a != 0:
            b1 = 2
            v = dU.a
            if v == -2:
                arrayOfByte = ae.ar
                b2 = 63
                dU.f = dU.b
            elif v == -1:
                arrayOfByte = ae.ao
                b2 = 60
                dU.f = dU.b
                b1 = 0
            elif v in (10, 11):
                arrayOfByte = ae.av
                b2 = 67
                if dU.b > 0:
                    dU.f = i16(dU.b - 1 + (dU.d << 2))
                else:
                    return
            else:
                arrayOfByte = ae.am
                b2 = 58
                dU.f = i16(dU.b + 4)
            if dU.g is None:
                dU.g = arrayOfByte
                dU.h = self.K_I(b2)
            while b1 < 3:
                i = dU.c.a - ag.ca.a
                j_ = dU.c.b - ag.ca.b
                if dU.a == -1:
                    i += arrayOfByte1[b1]
                    j_ += arrayOfByte2[b1]
                self.a_LyBII(dU.h[dU.f], dU.g[dU.f], i, j_)
                c.a_IIII(dU.c.a - dU.h[dU.f].e, dU.c.b - dU.h[dU.f].f, dU.h[dU.f].c, dU.h[dU.f].d)
                b1 += 1

    def a_LyBII(self, paramy, paramByte, paramInt1, paramInt2):  # c.java:228-234
        self.a_ALyABIII([paramy], [paramByte], 1, paramInt1, paramInt2)

    def a_ALyABIII(self, paramArrayOfy, paramArrayOfbyte, paramInt1, paramInt2, paramInt3):  # c.java:236-245
        b1 = 0
        image = None
        for b in range(paramInt1):
            if paramArrayOfbyte[b] != b1:
                b1 = paramArrayOfbyte[b]
                if b1 != 0:
                    image = self.d_T(ag.bC.a_I(b1 - 27))
            if b1 != 0:
                self.b_MIIIIII(image, paramInt2 - paramArrayOfy[b].e, paramInt3 - paramArrayOfy[b].f,
                               image.getWidth(), image.getHeight(), 0, 0)

    def e_v(self):  # c.java:247-260  (hero and enemies, sorted by y)
        bool_ = True
        cz = ag.cz
        cz.L = cz.ab[cz.e[0]][cz.d[0]][cz.f[0]]
        for b in range(ag.ez):
            s = ag.ey[b]
            if bool_ and cz.a[0].b < ag.ex[s].a[0].b:
                self.o_v()
                bool_ = False
            self.e_I(s)
        if bool_:
            self.o_v()
        self.n_v()

    def n_v(self):  # c.java:262-279  (breaking-object animation)
        for b in range(ag.cB):
            cA = ag.cA[b]
            if cA.a != 0 and cA.h != 0:
                i = cA.b.a - ag.ca.a
                j_ = cA.b.b - ag.ca.b
                k = 2 - cA.h
                if k <= 3 and k >= 0:
                    if ag.ct[43] is None:
                        return
                    ag.bc.a_III(k, i, j_)
                    c.a_IIII(cA.b.a - ag.eV[k].e, cA.b.b - ag.eV[k].f, ag.eV[k].c, ag.eV[k].d)
                else:
                    break

    def _fm_from(self, src, n):  # `fm = new y[src.length - n]; fm[b] = src[n + b]`
        if n > len(src):
            raise ValueError("NegativeArraySizeException")
        ag.fm = src[n:]

    def e_I(self, paramInt):  # c.java:287-566  (draw an enemy: soldier 201-203 or general)
        ex = ag.ex[paramInt]
        ex.f[0] = min(ex.f[0], len(ex.B[ex.e[0]]) - 1)
        i = ex.a[0].a - ag.ca.a
        j_ = ex.a[0].b - ag.ca.b
        s = ex.B[ex.e[0]][ex.f[0]][ex.g[0]]
        if ex.h > 200:
            if s < 100:
                if ex.h == 203:
                    ay = ae.ay[ae.aT[ex.e[0]]]
                    D = ex.D[s]
                    for b in range(3):
                        self.b_MIIIIII(ex.C, i - D.e + ay[b][0], j_ - D.f + ay[b][1], D.c, D.d, D.a, D.b)
                    az = ae.az[ae.aT[ex.e[1]]]
                    c.a_IIII(ex.a[0].a - D.e + az[0], ex.a[0].b - D.f + az[1], D.c + az[2], D.d + az[3])
                else:
                    if ex.h == 202:
                        ex.C = ag.es[1]
                        ex.D = ag.et[1]
                    D = ex.D[s]
                    self.b_MIIIIII(ex.C, i - D.e, j_ - D.f, D.c, D.d, D.a, D.b)
                    c.a_IIII(ex.a[0].a - D.e, ex.a[0].b - D.f, D.c, D.d)
        else:
            if ex.f[0] < 6:
                i1 = 1310732 if ag.dC.c != 0 else 1053711
                n = i1 >> s & 0x1
                arrayOfY1 = ag.et[4]
                arrayOfY2 = ag.et[3]
                arrayOfY3 = ag.et[5]
            else:
                b = 2 if ag.dC.c != 0 else 3
                n = ae.aJ[(s >> 5 << 2) + b] >> (s & 0x1F) & 0x1
                arrayOfY1 = ag.et[7]
                arrayOfY2 = ag.et[6]
                arrayOfY3 = ag.et[8]
            f0 = ex.f[0]
            g0 = ex.g[0]
            if f0 == 6:
                if 2 < g0 < 6:
                    ag.fk = 1
                    ag.fl = ag.ct[44]
                    self._fm_from(ag.eW, ex.e[0] + (g0 & 0x1))
            elif f0 == 7:
                if 4 < g0 < 8:
                    ag.fk = 1
                    ag.fl = ag.ct[44]
                    self._fm_from(ag.eW, ex.e[0] + (g0 & 0x1))
            elif f0 == 8:
                if 0 < g0 < 9:
                    ag.fk = 1
                    ag.fl = ag.ct[44]
                    self._fm_from(ag.eW, ex.e[0] + (g0 & 0x1))
            elif f0 in (9, 10):
                if g0 > 3:
                    if g0 == 4:
                        ag.fb = self.K_I(57)
                        ag.fa = ae.al
                    ag.fk = 2
                    ag.fl = None
                    ag.fc = i16(g0 - 4)
                    self._fm_from(ag.fb, ag.fc)
            elif f0 in (11, 12, 13):
                if 3 < g0 < 10:
                    if g0 == 4:
                        ag.fb = self.K_I(58)
                        ag.fa = ae.am
                    ag.fk = 2
                    ag.fl = None
                    ag.fc = i16(g0 - 4)
                    self._fm_from(ag.fb, ag.fc)
            elif f0 == 15:
                if g0 == 5 or g0 == 6:
                    if g0 == 5:
                        ag.fb = self.K_I(59)
                        ag.fa = ae.an
                    ag.fk = 1
                    ag.fl = None
                    ag.fc = i16(g0 - 5)
                    self._fm_from(ag.fb, ag.fc)
            elif f0 == 16:
                if 1 < g0 < 6:
                    ag.fk = 1
                    ag.fl = ag.ct[44]
                    self._fm_from(ag.eW, g0 & 0x1)
            elif f0 == 17:
                if g0 == 5 or g0 == 6:
                    ag.fk = 1
                    ag.fl = ag.ct[44]
                    self._fm_from(ag.eW, g0 - 5)
            elif f0 == 18:
                if g0 == 5 or g0 == 6:
                    if g0 == 5:
                        ag.fb = self.K_I(61)
                        ag.fa = ae.ap
                    ag.fk = 1
                    ag.fl = None
                    ag.fc = i16(g0 - 5)
                    self._fm_from(ag.fb, ag.fc)
            elif f0 in (20, 21):
                if f0 == 21 and g0 == 9:        # case 21 falls through into case 20
                    ag.fb = self.K_I(63)
                    ag.fa = ae.ar
                    ag.fc = 2
                    ag.fk = 2
                    self._fm_from(ag.fb, 1)
                if 1 < g0 < 9:
                    if g0 == 2:
                        ag.fb = self.K_I(62)
                        ag.fa = ae.aq
                    ag.fk = 2
                    ag.fl = None
                    ag.fc = i16(g0 - 2 + (ex.e[0] >> 1) * 7)
                    self._fm_from(ag.fb, ag.fc)
            if s < 180:
                y2 = arrayOfY2[s]
                self.b_MIIIIII(ag.eq, i - y2.e + idiv(y2.c, 2) - 13, j_ - y2.f + y2.d - 5, ag.eq.getWidth(), ag.eq.getHeight(), 0, 0)
            if ag.fk == 1:
                fm0 = ag.fm[0]
                if ag.fl is not None:
                    self.b_MIIIIII(ag.fl, i - fm0.e, j_ - fm0.f, fm0.c, fm0.d, fm0.a, fm0.b)
                else:
                    self.a_ALyABIII(ag.fm, [ag.fa[ag.fc]], 1, i, j_)
                c.a_IIII(ex.a[0].a - fm0.e, ex.a[0].b - fm0.f, fm0.c, fm0.d)
            ag.em = 0
            ag.en = 0
            if s < 180:
                if ex.q > 0 or ex.p > 0:
                    ag.em = 1
                if ag.em == 1:
                    i1 = ag.bN % 3
                    q = ag.eQ[i1]
                    self.b_MIIIIII(ag.eR, i - q.e, j_ - q.f + 3, q.c, q.d, q.a, q.b)
                    ag.en = 1
                if n != 0:
                    self.a_IILyI(i, j_, arrayOfY3[s], paramInt)
                y2 = arrayOfY2[s]
                y1 = arrayOfY1[s]
                self.b_MIIIIII(ag.cz.aH, i - y2.e, j_ - y2.f, y2.c, y2.d, y2.a, y2.b)
                self.b_MIIIIII(ag.er[1], i - y1.e, j_ - y1.f, y1.c, y1.d, y1.a, y1.b)
                c.a_IIII(ex.a[0].a - y2.e, ex.a[0].b - y2.f, y2.c, y2.d)
                if 0 == n:
                    self.a_IILyI(i, j_, arrayOfY3[s], paramInt)
                if ag.em == 1:
                    i1 = 3 + ag.bN % 3
                    q = ag.eQ[i1]
                    self.b_MIIIIII(ag.eR, i - q.e, j_ - q.f + 3, q.c, q.d, q.a, q.b)
                    ag.en = 1
            ex.y = -1
            if ex.f[0] < 6:
                if 8 < s < 16 and (s & 0x1) != 0:
                    ex.y = i8(self.C_I(3))
                    ag.bc.a_II(paramInt, ex.y)
            else:
                f0 = ex.f[0]
                g0 = ex.g[0]
                if f0 == 6:
                    if 2 < g0 < 6:
                        ex.y = 1
                elif f0 == 7:
                    if 4 < g0 < 8:
                        ex.y = 1
                elif f0 == 8:
                    if g0 in (2, 4, 6, 8):
                        ex.y = 1
                elif f0 == 14:
                    if (g0 & 0x1) == 0:
                        ex.y = i8(self.C_I(3))
                elif f0 == 15:
                    if g0 == 5:
                        ex.y = 2
                elif f0 == 16:
                    if g0 == 6:
                        ex.y = 2
                elif f0 == 19:
                    if (g0 & 0x1) != 0:
                        ex.y = 2
                if -1 < ex.y < 100:
                    ag.bc.a_II(paramInt, ex.y)
            if ag.fk == 2:
                if ex.f[0] == 21 and ex.g[0] == 9:
                    i += ae.aA[ex.e[1] >> 1]
                    j_ += ae.aB[ex.e[1] >> 1]
                self.a_ALyABIII(ag.fm, [ag.fa[ag.fc]], 1, i, j_)
                c.a_IIII(ex.a[0].a - ag.fm[0].e, ex.a[0].b - ag.fm[0].f, ag.fm[0].c, ag.fm[0].d)
        if ex.w != 0:
            fe = ag.fe[ex.x]
            self.a_LyBII(fe, ag.fd[ex.x], i, j_)
            c.a_IIII(ex.a[0].a - fe.e, ex.a[0].b - fe.f, fe.c, fe.d)
        if ex.t != 0:
            ex.u = i8(ex.u + 1)
            if ex.u > 1:
                ex.t = 0
                return
            i = ex.v.a - ag.ca.a
            j_ = ex.v.b - ag.ca.b
            n = ex.u + (ex.t - 1 << 1)
            ag.bc.a_III(n, i, j_)
            v_ = ag.eV[n]
            c.a_IIII(ex.v.a - v_.e, ex.v.b - v_.f, v_.c, v_.d)

    def a_IILyI(self, paramInt1, paramInt2, paramy, paramInt3):  # c.java:568-571  (a general's weapon)
        self.b_MIIIIII(ag.ct[40 + ag.dC.c], paramInt1 - paramy.e, paramInt2 - paramy.f, paramy.c, paramy.d, paramy.a, paramy.b)
        c.a_IIII(ag.ex[paramInt3].a[0].a - paramy.e, ag.ex[paramInt3].a[0].b - paramy.f, paramy.c, paramy.d)

    def _fj_from(self, src, n):  # `fj = new y[src.length - n]; fj[b] = src[n + b]`
        if n > len(src):
            raise ValueError("NegativeArraySizeException")
        ag.fj = src[n:]

    def o_v(self):  # c.java:575-892  (draw the hero: shadow, body, weapon, effects)
        cz = ag.cz
        m = -1
        arrayOfByte = None
        if cz.e[0] < 12:
            l_ = 5789684072952 if cz.K != 0 else 8263870709823
            k = l_ >> cz.L & 0x1
            if 11 < cz.L < 36 and (cz.L & 0x1) != 0:
                m = ((cz.L - 12) & 0xFFFE) % 6 >> 1
            arrayOfY1 = cz.aC
            arrayOfY2 = cz.aE
            arrayOfY3 = ag.eS[cz.K]
        else:
            b1 = 0 if cz.K != 0 else 1
            k = ae.aJ[(cz.L >> 5 << 2) + b1] >> (cz.L & 0x1F) & 0x1
            arrayOfY1 = cz.aD
            arrayOfY2 = cz.aF
            arrayOfY3 = ag.eT[cz.K]
        e0 = cz.e[0]
        f0 = cz.f[0]
        # switch (cz.e[0]) - case 27 falls through into case 26 (no break in the original)
        if e0 == 2:
            ag.fh = 1
            ag.fi = ag.ct[44]
            self._fj_from(ag.eW, cz.d[0] + (f0 & 0x1))
            if f0 == 1:
                self.a__I(7)
        elif e0 == 12:
            if 2 < f0 < 6:
                m = 1
                ag.fh = 1
                ag.fi = ag.ct[44]
                self._fj_from(ag.eW, cz.d[0] + (f0 & 0x1))
        elif e0 == 13:
            if 4 < f0 < 8:
                m = 1
                ag.fh = 1
                ag.fi = ag.ct[44]
                self._fj_from(ag.eW, cz.d[0] + (f0 & 0x1))
        elif e0 == 14:
            if 0 < f0 < 9:
                if 0 == (f0 & 0x1):
                    m = 1
                ag.fh = 1
                ag.fi = ag.ct[44]
                self._fj_from(ag.eW, cz.d[0] + (f0 & 0x1))
        elif e0 in (15, 16):
            if f0 > 3:
                if ag.eX is None:
                    ag.eY = self.K_I(57)
                    ag.eX = ae.al
                ag.fh = 2
                ag.fi = None
                ag.eZ = i16(f0 - 4)
                self._fj_from(ag.eY, ag.eZ)
        elif e0 in (17, 18, 19):
            if 3 < f0 < 10:
                if ag.eX is None:
                    ag.eY = self.K_I(58)
                    ag.eX = ae.am
                ag.fh = 3
                ag.fi = None
                ag.eZ = i16(f0 - 4)
                self._fj_from(ag.eY, ag.eZ)
        elif e0 == 20:
            if (f0 & 0x1) != 0:
                m = cz.M
        elif e0 == 21:
            if f0 == 5 or f0 == 6:
                if f0 == 5:
                    m = 2
                    ag.eY = self.K_I(59)
                    ag.eX = ae.an
                ag.fh = 1
                ag.fi = None
                ag.eZ = i16(f0 - 5)
                self._fj_from(ag.eY, ag.eZ)
        elif e0 == 22:
            if 1 < f0 < 6:
                ag.fh = 1
                ag.fi = ag.ct[44]
                self._fj_from(ag.eW, f0 & 0x1)
            elif f0 == 6:
                m = 2
        elif e0 == 23:
            if f0 == 5 or f0 == 6:
                ag.fh = 1
                ag.fi = ag.ct[44]
                self._fj_from(ag.eW, f0 - 5)
        elif e0 == 24:
            if f0 == 5 or f0 == 6:
                if ag.eX is None:
                    ag.eY = self.K_I(61)
                    ag.eX = ae.ap
                ag.fh = 1
                ag.fi = None
                ag.eZ = i16(f0 - 5)
                self._fj_from(ag.eY, 1)
        elif e0 == 25:
            if (f0 & 0x1) != 0:
                m = 2
        elif e0 in (26, 27):
            if e0 == 27 and f0 == 9:
                ag.eY = self.K_I(63)
                ag.eX = ae.ar
                ag.fh = 3
                ag.eZ = 1
                self._fj_from(ag.eY, 1)
            if 1 < f0 < 9:
                if ag.eX is None:
                    ag.eY = self.K_I(62)
                    ag.eX = ae.aq
                ag.fh = 3
                ag.fi = None
                ag.eZ = i16(f0 - 2 + (cz.d[0] >> 1) * 7)
                self._fj_from(ag.eY, ag.eZ)
        elif e0 == 28:
            if 3 < f0 < 22:
                if ag.eX is None:
                    ag.eY = self.K_I(64)
                    ag.eX = ae.as_
                ag.fh = 3
                ag.fi = None
                if f0 > 9:
                    ag.eZ = i16((f0 - 10) * 3 + 6)
                    ag.fg = 3
                else:
                    ag.eZ = i16(f0 - 4)
                self._fj_from(ag.eY, ag.eZ)
        elif e0 == 29:
            if 6 < f0 < 22:
                if ag.eX is None:
                    ag.eY = self.K_I(65)
                    ag.eX = ae.at
                ag.fh = 3
                ag.fi = None
                ag.eZ = i16(f0 - 7)
                self._fj_from(ag.eY, ag.eZ)
        elif e0 == 30:
            if 3 < f0 < 9:
                if ag.eX is None:
                    ag.eY = self.K_I(66)
                    ag.eX = ae.au
                ag.fh = 3
                ag.fi = None
                ag.eZ = i16((f0 - 4) * 5)
                self._fj_from(ag.eY, ag.eZ)
                ag.fg = 5
            elif 12 < f0 < 15:
                if f0 == 13:
                    ag.eY = self.K_I(63)
                    ag.eX = ae.ar
                ag.fh = 3
                ag.fi = None
                ag.eZ = i16((f0 - 13) * 5 + 2)
                self._fj_from(ag.eY, ag.eZ)
                ag.fg = 3
        i = cz.a[0].a - ag.ca.a
        j_ = cz.a[0].b - ag.ca.b
        y2 = arrayOfY2[cz.L]
        self.b_MIIIIII(ag.eq, i - y2.e + idiv(y2.c, 2) - 13, j_ - y2.f + y2.d - 5, ag.eq.getWidth(), ag.eq.getHeight(), 0, 0)
        if ag.fh == 1:
            fj0 = ag.fj[0]
            if ag.fi is not None:
                self.b_MIIIIII(ag.fi, i - fj0.e, j_ - fj0.f, fj0.c, fj0.d, fj0.a, fj0.b)
            else:
                arrayOfByte = list(ag.eX[ag.eZ:])
                self.a_ALyABIII(ag.fj, arrayOfByte, 1, i, j_)
            c.a_IIII(cz.a[0].a - fj0.e, cz.a[0].b - fj0.f, fj0.c, fj0.d)
        if ag.ek == 1:
            i2 = ag.bN % 3
            q = ag.eQ[i2]
            self.b_MIIIIII(ag.eR, i - q.e, j_ - q.f + 3, q.c, q.d, q.a, q.b)
            ag.el = 1
        if m > -1:
            if 18 == (cz.d[0] >> 1) * 6 + (m << 1):
                ag.bc.a_II(-1, m)
            elif cz.d[0] == 4 and cz.e[0] != 25:
                ag.bc.a_II(-1, m)
        if k != 0:
            ag.bc.a_IILy(i, j_, arrayOfY3[cz.L])
        y1 = arrayOfY1[cz.L]
        self.b_MIIIIII(cz.aH, i - y2.e, j_ - y2.f, y2.c, y2.d, y2.a, y2.b)
        self.b_MIIIIII(cz.aG, i - y1.e, j_ - y1.f, y1.c, y1.d, y1.a, y1.b)
        c.a_IIII(cz.a[0].a - y1.e, cz.a[0].b - y1.f, y1.c, y1.d)
        c.a_IIII(cz.a[0].a - y2.e, cz.a[0].b - y2.f, y2.c, y2.d)
        if 0 == k:
            ag.bc.a_IILy(i, j_, arrayOfY3[cz.L])
        if m > -1:
            if cz.e[0] == 25:
                ag.bc.a_II(-1, m)
            elif 18 != (cz.d[0] >> 1) * 6 + (m << 1) and cz.d[0] != 4:
                ag.bc.a_II(-1, m)
        if ag.ek == 1:
            i2 = 3 + ag.bN % 3
            q = ag.eQ[i2]
            self.b_MIIIIII(ag.eR, i - q.e, j_ - q.f + 3, q.c, q.d, q.a, q.b)
        if ag.fh == 2:
            arrayOfByte = list(ag.eX[ag.eZ:])
            self.a_ALyABIII(ag.fj, arrayOfByte, 1, i, j_)
            c.a_IIII(cz.a[0].a - ag.fj[0].e, cz.a[0].b - ag.fj[0].f, ag.fj[0].c, ag.fj[0].d)
        elif cz.T != 0:
            arrayOfByte = list(ag.eX[ag.eZ:])
            arrayOfY = ag.eY[cz.U:]
            self.a_ALyABIII(arrayOfY, arrayOfByte, 1, i, j_)
            u = ag.eY[cz.U]
            c.a_IIII(cz.a[0].a - u.e, cz.a[0].b - u.f, u.c, u.d)
        if cz.O != 0:
            cz.P += 1
            if cz.P > 1:
                cz.O = 0
                return
            i2 = cz.P
            i = cz.Q.a - ag.ca.a
            j_ = cz.Q.b - ag.ca.b
            ag.bc.a_III(i2, i, j_)
            v_ = ag.eV[i2]
            c.a_IIII(cz.Q.a - v_.e, cz.Q.b - v_.f, v_.c, v_.d)

    def g_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # c.java:894-915  (run the scripts of cells)
        for b in range(paramInt4):
            for b1 in range(paramInt3):
                i = paramInt1 + b1 + paramInt2 + b & 0x7
                while ag.cH[i].c != 0:
                    j_ = ag.cE.a[ag.cH[i].a] & 0xFF
                    k = ag.cE.a[ag.cH[i].a + 1] & 0xFF
                    if j_ == paramInt1 + b1 and k == paramInt2 + b:
                        m = ag.cH[i].a
                        s = i16(i16(ag.cE.a[m + 2] & 0xFF | (ag.cE.a[m + 3] & 0xFF) << 8) + 4)
                        n = 4
                        while True:
                            n += self.c_IIIII(ag.cE.a[m + n], ag.cE.a[m + n + 1], ag.cE.a[m + n + 2], j_, k)
                            if not n < s:
                                break
                        break
                    i = ag.cH[i].b
                    if 0 == i:
                        break

    def c_IIIII(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # c.java:917-926
        if paramInt1 == 0:
            if ag.dm == paramInt2 - 1:
                self.b_IIII(paramInt3 + 200, paramInt4, paramInt5, 4)
            return 3
        return 0

    def b_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # c.java:928-1015  (create an enemy)
        import config
        if config.NO_ENEMIES:
            # PORT-EXTRA (POW_NO_ENEMIES=1): the map without the combat - nobody is created
            return
        arrayOfByte1 = [0, -56, 0, 56, 0]
        arrayOfByte2 = [56, 0, -56, 0, 0]
        b = 0
        while b < ag.ez and 0 != ag.ex[b].c:
            b += 1
        ex = ag.ex[b]
        ex.c = 1
        if config.DECOMP_FIX["F16"] and ex.a[1] is not ex.a[0]:
            # DECOMP-FIX F16: the start position is written into ex.a[1], but the enemy AI
            # (ar.java:1340-1600) moves ex.a[0]. Both are the same object once ar.aC()
            # (ex.a[1] = ex.a[0], ar.java:1831) has run for this slot; a slot used for the
            # first time keeps a[0] at (0, 0), the enemy is pushed into the top-left corner
            # of the room and can stay stuck there behind a tent or a wall.
            ex.a[1] = ex.a[0]
        ex.a[1].a = i16(paramInt2 * 27 + 12 + arrayOfByte1[paramInt4])
        ex.a[1].b = i16(paramInt3 * 27 + 20 + arrayOfByte2[paramInt4])
        ex.b.a = ex.b.b = 0
        ex.e[1] = ex.d = i8((paramInt4 << 1) + 4 & 0x7)
        ex.e[0] = ex.d = i8((paramInt4 << 1) + 4 & 0x7)
        ex.f[1] = 0
        ex.f[0] = 0
        ex.g[1] = 0
        ex.g[0] = 0
        if paramInt1 == 201 and ag.g_II(0, 2) != 0:
            paramInt1 = 203
        ex.h = i16(paramInt1)
        ex.s = 14
        ex.r = 0
        ex.t = 0
        ex.A = 0
        ex.z = 0
        ex.w = 0
        ex.y = 0
        ex.n = 0
        ex.o = 0
        ex.p = 0
        ex.q = 0
        if paramInt1 in (201, 202, 203):
            if paramInt1 == 202:            # case 202 falls through into case 201
                ex.r = 1
                ex.s = 15
            i = 0 if paramInt1 == 203 else paramInt1 - 201
            ex.B = ag.eL[i]
            ex.C = ag.es[i]
            ex.D = ag.et[i]
            self.a_II(paramInt1 - 201, b)
        else:
            if ag.dz[ag.dm].e == paramInt1:
                ag.cr = 1
            ag.eB = 1
            ag.dG = 1
            ag.dJ = i16(paramInt1)
            self.B_I(paramInt1)
            self.am()
            ag.ck = 1
            ag.bV = 5
            self.a_II(4, b)
            ex.B = ag.eK
            if ag.ct[40 + ag.dC.c] is None:
                ag.ct[40 + ag.dC.c] = self.d_T(ag.bB.a_I(42 + ag.dC.c))
            if ag.er[1] is None:
                ag.er[1] = self.d_T(ag.bB.a_I(50 + ag.dC.b - 1))
            ag.et[3] = self.K_I(68)
            ag.et[4] = self.K_I(70 + ag.dC.b - 1)
            ag.et[5] = self.K_I(88 + (ag.dC.c << 2))
            ag.et[6] = self.K_I(69)
            ag.et[7] = self.K_I(76 + ag.dC.b - 1)
            ag.et[8] = self.K_I(90 + (ag.dC.c << 2))
            ex.C = ag.cz.aH
            ex.D = ag.et[2]
            ag.eD[1] = 1
        ag.ey[ag.ez] = i16(b)
        ag.ez = i16(ag.ez + 1)
        if paramInt1 != 202:
            ag.eA = i16(ag.eA + 1)

    def a_II(self, paramInt1, paramInt2):  # c.java:1017-1041  (level, attack, defence, HP of a new enemy)
        arrayOfInt1 = [100, 100, 150]
        arrayOfInt2 = [3, 2, 3]
        arrayOfInt3 = [7, 5, 7]
        ex = ag.ex[paramInt2]
        if paramInt1 == 4:
            ex.i = i16(ag.cz.l + ag.eD[1])
            ex.j = i16(idiv((ag.dC.g + ex.i - 1) * 6, 5))
            ex.k = i16(idiv((ag.dC.h + ex.i - 1) * 6, 5))
            ex.m = ex.l = i16(ag.dC.i + (ex.i - 1) * 3)
            return
        if ag.cz.l < 21:
            i = ag.cz.l + ag.g_II(0, 5) - 2
            ex.i = i16(i) if i > 0 else 1
        elif ag.cz.l < 41:
            ex.i = i16(ag.cz.l + self.C_I(9) - 3)
        else:
            ex.i = i16(ag.cz.l + self.C_I(16) - 5)
        ex.j = i16(idiv((arrayOfInt2[paramInt1] + ex.i) * arrayOfInt1[paramInt1], 100))
        ex.k = i16(ex.i - 1)
        ex.m = ex.l = i16(arrayOfInt3[paramInt1] + 3 * ex.i)

    @staticmethod
    def p_v():  # c.java:1043-1050
        ag.ez = 0
        ag.eA = 0
        from pow.game.structs import ap
        for b in range(7):
            if ag.ex[b] is None:
                ag.ex[b] = ap()
            ag.ex[b].c = 0

    def h_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # c.java:1052-1075  (reachable cells of the room)
        i = idiv(paramInt3, 27)
        j_ = idiv(paramInt4, 27)
        if i < paramInt1:
            i = paramInt1
        elif i > paramInt1 + 6:
            i = paramInt1 + 6
        if j_ < paramInt2:
            j_ = paramInt2
        elif j_ > paramInt2 + 6:
            j_ = paramInt2 + 6
        for b in range(7):
            for b1 in range(7):
                ag.ew[b][b1] = 0
        for b in range(7):
            for b1 in range(7):
                k = paramInt1 + b + (paramInt2 + b1) * ag.cE.b.a
                if (ag.cE.a[ag.cE.f + k] & 0x1) != 0:
                    ag.ew[b][b1] = -1
        self.b_II(i - paramInt1, j_ - paramInt2)

    def b_II(self, paramInt1, paramInt2):  # c.java:1077-1086  (flood fill)
        arrayOfByte1 = [0, -1, 0, 1]
        arrayOfByte2 = [1, 0, -1, 0]
        ag.ew[paramInt1][paramInt2] = 1
        for b in range(4):
            x_ = paramInt1 + arrayOfByte1[b]
            y_ = paramInt2 + arrayOfByte2[b]
            if -1 < x_ < 7 and -1 < y_ < 7 and 0 == ag.ew[x_][y_]:
                self.b_II(x_, y_)

    def a_I(self, paramInt):  # c.java:1089-1115  (rooms of the map: exits, enemy waves)
        from pow.game.structs import au
        if config.DECOMP_FIX["F17"]:
            # DECOMP-FIX F17 (also here): `cE.b.a / 7 * cE.b.b / 7` is (width / 7) * (height / 7);
            # every N.arr holds exactly a whole number of missions of that many rooms. Literal,
            # maps 30 / 37 wide (Vengeance, ...) read past the end of the room data.
            j0 = idiv(ag.cE.b.a, 7) * idiv(ag.cE.b.b, 7)
        else:
            j0 = idiv(idiv(ag.cE.b.a, 7) * ag.cE.b.b, 7)
        arrayOfByte = ag.v_I(paramInt - 1)
        i = 20 + j0 * ag.dm * 19
        B = ag.b_B
        for b in range(j0):
            if ag.eO[b] is None:
                ag.eO[b] = au()
            eO = ag.eO[b]
            eO.a[0] = B(arrayOfByte[i])
            eO.a[1] = B(arrayOfByte[i + 1])
            eO.a[2] = B(arrayOfByte[i + 2])
            eO.a[3] = B(arrayOfByte[i + 3])
            eO.b = B(arrayOfByte[i + 4])
            eO.c = B(arrayOfByte[i + 5])
            eO.d = B(arrayOfByte[i + 6])
            eO.e = B(arrayOfByte[i + 7])
            eO.f = B(arrayOfByte[i + 8])
            eO.g = B(arrayOfByte[i + 9])
            eO.h = B(arrayOfByte[i + 10])
            eO.i = B(arrayOfByte[i + 11])
            eO.j = B(arrayOfByte[i + 12])
            eO.k = B(arrayOfByte[i + 13])
            eO.l = B(arrayOfByte[i + 14])
            eO.m = B(arrayOfByte[i + 15])
            eO.n = B(arrayOfByte[i + 16])
            eO.o = B(arrayOfByte[i + 18])
            i += 19

    @staticmethod
    def f_v():  # c.java:1117-1120  (hero pixel position -> cell)
        ag.cz.b[0].a = i16(idiv(ag.cz.a[0].a, 27))
        ag.cz.b[0].b = i16(idiv(ag.cz.a[0].b - 6, 27))

    @staticmethod
    def aB():  # c.java:1122-1125
        if ag.cE is not None:
            ag.cE.a_v()

    def b_I(self, paramInt):  # c.java:1127-1162  (load map file #paramInt of mdat)
        from pow.game.structs import o, aj
        o_ = o()
        c.aB()
        arrayOfByte = j.a("/" + ag.bF.a_I(paramInt - 1))
        k = len(arrayOfByte)
        o_.a = [b & 0xFF for b in arrayOfByte]
        if o_.b is None:
            o_.b = aj()
        o_.b.a = o_.a[0]
        o_.b.b = o_.a[1]
        o_.b.c = o_.a[2]
        i = 3 + o_.b.c
        o_.c = i
        j_ = o_.b.b * o_.b.a
        i += j_
        o_.d = i
        i += j_
        o_.e = i
        i += j_
        o_.f = i
        c.aC()
        i += j_
        if k > i:
            s = o_.a[i]
            i += 1
            i += 2
            for b in range(s):
                s1 = o_.a[i]
                s2 = o_.a[i + 1]
                m = o_.a[i + 2] & 0xFF | o_.a[i + 3] << 8 & 0xFF00
                c.a_III(i, s1, s2)
                i = i + 4 + m
        return o_

    @staticmethod
    def aC():  # c.java:1164-1171
        from pow.game.structs import ah
        ag.cI = 8
        for b in range(50):
            if ag.cH[b] is None:
                ag.cH[b] = ah()
            ag.cH[b].c = 0
            # PORT-EXTRA (hang fix): the original clears only .c and keeps the links .b of the
            # previous map. a_III() walks .b without looking at .c, so on a later map it can follow
            # an old link and set a node's .b to a lower index (even to itself): a cycle, and the
            # next a_III() into that bucket loops forever (the game freezes on a map load after
            # some missions; the Java code has the same bug). A cleared link ends every walk at a
            # node of this map, so a link always points to a higher index and cannot cycle.
            ag.cH[b].b = 0

    @staticmethod
    def a_III(paramInt1, paramInt2, paramInt3):  # c.java:1173-1190  (hash of cell scripts by (x + y) & 7)
        from pow.game.structs import ah
        i = paramInt2 + paramInt3 & 0x7
        if ag.cH[i] is None:
            ag.cH[i] = ah()
        if ag.cH[i].c != 0:
            while ag.cH[i].b != 0:
                i = ag.cH[i].b
            ag.cH[ag.cI].c = 1
            ag.cH[ag.cI].a = paramInt1
            ag.cH[ag.cI].b = 0
            ag.cI = i16(ag.cI + 1)
            ag.cH[i].b = ag.cI
            return
        ag.cH[i].c = 1
        ag.cH[i].a = paramInt1
        ag.cH[i].b = 0
    # NOTE: in a_III the decompiled order sets cH[i].b = cI *after* cI++, so it points one past
    # the entry just filled and the second script of a bucket is never found by g_IIII (that
    # script's cell enemies are not spawned). Kept literal: it is the order of the bytecode.

    def a_IIIII(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # c.java:1197-1391
        # (draw the visible tiles into ct[7], load the tile images, set up the room the hero is in)
        from pow.game.structs import r, f, a, i as i_
        cE = ag.cE
        x.a_G(ag.cu)
        ag.cB = 0
        for b1 in range(len(ag.cA)):
            if ag.cA[b1] is None:
                ag.cA[b1] = r()
            ag.cA[b1].a = 0
        for b1 in range(3):
            if ag.eC[b1] is None:
                ag.eC[b1] = f()
            ag.eC[b1].a = 0
        ag.cD = 0
        for b1 in range(10):
            if ag.cC[b1] is None:
                ag.cC[b1] = a()
            ag.cC[b1].a = 0
        ag.ca.a = i16(ag.cd * 27 + ag.cc.a)
        ag.ca.b = i16(ag.ce * 27 + ag.cc.b)
        ag.cf.a = i16(idiv(ag.cd, 7))
        ag.cf.b = i16(idiv(ag.ce, 7))
        b1 = 0
        for b2 in range(2):
            k = 0
            for b in range(240):
                ag.cJ[b] = 0
            ag.ct[4] = None
            if ag.bT is not None:
                for b1 in range(len(ag.bT)):
                    ag.bT[b1] = None
                ag.bT = None
                ag.R_v()
            for b1 in range(paramInt2):
                m = (paramInt4 + b1) * cE.b.a + paramInt3
                for b3 in range(paramInt1):
                    if b2 != 0:
                        if (cE.a[cE.f + m + b3] & 0x2) != 0 and cE.a[cE.d + m + b3] != 0 and 0 == ag.cJ[cE.a[cE.d + m + b3] - 1]:
                            k += 1
                            ag.cJ[cE.a[cE.d + m + b3] - 1] = k
                        if cE.a[cE.e + m + b3] != 0:
                            if 0 == ag.cJ[cE.a[cE.e + m + b3] - 1]:
                                k += 1
                                ag.cJ[cE.a[cE.e + m + b3] - 1] = k
                                k += 1
                                ag.cJ[cE.a[cE.e + m + b3]] = k
                            if paramInt5 != 0:
                                cE.a[cE.e + m + b3] = 0
                            else:
                                if len(ag.cA) <= ag.cB:
                                    ag.cA = ag.cA + [None] * len(ag.cA)
                                if ag.cA[ag.cB] is None:
                                    ag.cA[ag.cB] = r()
                                cA = ag.cA[ag.cB]
                                cA.a = 1
                                cA.c.a = i16(paramInt3 + b3)
                                cA.c.b = i16(paramInt4 + b1)
                                cA.b.a = i16(cA.c.a * 27 + 12)
                                cA.b.b = i16(cA.c.b * 27 + 20)
                                cA.g = cE.a[cE.e + m + b3]
                                if cA.g in (101, 113):
                                    cA.d = 41
                                else:
                                    cA.d = 21
                                cA.e = 0
                                cA.f = ag.cJ[cE.a[cE.e + m + b3] - 1]
                                cA.h = 0
                                ag.cB = i16(ag.cB + 1)
                    else:
                        if cE.a[cE.c + m + b3] != 0 and 0 == ag.cJ[cE.a[cE.c + m + b3] - 1]:
                            k += 1
                            ag.cJ[cE.a[cE.c + m + b3] - 1] = k
                        if cE.a[cE.d + m + b3] != 0 and 0 == ag.cJ[cE.a[cE.d + m + b3] - 1]:
                            k += 1
                            ag.cJ[cE.a[cE.d + m + b3] - 1] = k
            b1 = paramInt2 if paramInt2 > 0 else 0
            if ag.bT is not None:
                m = len(ag.bT)
                while b1 < m:
                    ag.bT[0] = None
                    b1 += 1
                ag.bT = None
            ag.R_v()
            ag.bT = [None] * k
            for b1 in range(15):
                m = b1 << 4
                for b3 in range(16):
                    if ag.cJ[m + b3] != 0:
                        ag.bT[ag.cJ[m + b3] - 1] = self.d_T(ag.bD.a_I(0 + b1) + "_" + ("" if b3 >= 9 else "0") + str(b3 + 1))
            x.a_G(ag.cu)
            if 0 == b2:
                for b1 in range(paramInt2):
                    for b3 in range(paramInt1):
                        k = (paramInt4 + b1) * cE.b.a + paramInt3 + b3
                        if cE.a[cE.c + k] != 0:
                            m = ag.cJ[cE.a[cE.c + k] - 1] - 1
                            if m >= 0:
                                ag.c_MIIIIII(ag.bT[m], 0, 0, b3 * 27, b1 * 27, 27, 27)
                        if cE.a[cE.d + k] != 0:
                            m = ag.cJ[cE.a[cE.d + k] - 1] - 1
                            if m >= 0:
                                ag.c_MIIIIII(ag.bT[m], 0, 0, b3 * 27, b1 * 27, 27, 27)
        ag.ct[4] = None
        if ag.bV == 4 and ag.cm < 7:
            x.a_G(ag.br)
            return
        arrayOfByte1 = [0, 0, 0, 6]
        arrayOfByte2 = [6, 0, 0, 0]
        arrayOfByte3 = [1, -1, -1, 1]
        if config.DECOMP_FIX["F17"]:
            # DECOMP-FIX F17: lost parentheses, `(ce + 4) / 7 * cE.b.a / 7` is row * (width / 7),
            # as ar.X() steps the rows (eP +- width / 7). Literal, the 5th room row of a map
            # 9 wide gives eP 6 instead of 5: a room that does not exist (crash) or a stale
            # room of an earlier map.
            ag.eP = i16(idiv(ag.ce + 4, 7) * idiv(cE.b.a, 7) + idiv(ag.cd + 4, 7))
        else:
            ag.eP = i16(idiv(idiv(ag.ce + 4, 7) * cE.b.a, 7) + idiv(ag.cd + 4, 7))
        c.p_v()
        for b1 in range(14):
            ag.eD[b1] = 0
        eO = ag.eO[ag.eP]
        if 0 == paramInt5:
            ag.eD[0] = eO.c
            ag.eD[1] = eO.d
            ag.eD[2] = eO.e
            ag.eD[3] = eO.f
            ag.eD[4] = eO.g
            ag.eD[5] = eO.h
            ag.eD[6] = eO.i
            ag.eD[7] = eO.j
            ag.eD[8] = eO.k
            ag.eD[9] = eO.l
            ag.eD[10] = eO.m
            ag.eD[11] = eO.n
        ag.ev = 0
        i = idiv(ag.cd + 2, 7) * 7 + 1
        j_ = idiv(ag.ce + 2, 7) * 7 + 1
        ag.bd.h_IIII(i, j_, ag.cz.a[0].a, ag.cz.a[0].b)
        for b1 in range(4):
            if eO.a[b1] != 0:
                k = i + arrayOfByte1[b1]
                m = j_ + arrayOfByte2[b1]
                for b in range(7):
                    if (b1 & 0x1) != 0:
                        if ag.ew[k - i][b] == 1:
                            n = k + (m + b) * cE.b.a
                            if 0 == cE.a[cE.e + n]:
                                n += arrayOfByte3[b1]
                                if (cE.a[cE.f + n] & 0x1) == 0 and cE.a[cE.e + n] == 0:
                                    if ag.eu[ag.ev] is None:
                                        ag.eu[ag.ev] = i_()
                                    ag.eu[ag.ev].a = k & 0xFFFF
                                    ag.eu[ag.ev].b = (m + b) & 0xFFFF
                                    ag.eu[ag.ev].c = b1
                                    ag.ev = i16(ag.ev + 1)
                    elif ag.ew[b][m - j_] == 1:
                        n = k + b + m * cE.b.a
                        if 0 == cE.a[cE.e + n]:
                            n += arrayOfByte3[b1] * cE.b.a
                            if (cE.a[cE.f + n] & 0x1) == 0 and cE.a[cE.e + n] == 0:
                                if ag.eu[ag.ev] is None:
                                    ag.eu[ag.ev] = i_()
                                ag.eu[ag.ev].a = (k + b) & 0xFFFF
                                ag.eu[ag.ev].b = m & 0xFFFF
                                ag.eu[ag.ev].c = b1
                                ag.ev = i16(ag.ev + 1)
        if paramInt5 != 0:
            ag.co = 1
            ag.cn = 5
        else:
            ag.bd.g_IIII(idiv(ag.cd, 7) * 7 + 1, idiv(ag.ce, 7) * 7 + 1, 7, 7)
        for b1 in range(9):
            for b in range(9):
                ag.eE[b1][b] = 1
        x.a_G(ag.br)

    @staticmethod
    def h_v():  # c.java:1616-1641  (mission experience -> dZ bars)
        arrayOfInt = ag.bb.p_v()
        cz = ag.cz
        dz = ag.dz[ag.dm]
        cz.F += ag.dY
        ag.dZ[0] = i16(cz.G * 100 // arrayOfInt[0])
        for b in range(2):
            if b != 0 and ag.dX < dz.i:
                ag.dY += idiv((idiv(idiv(dz.i - ag.dX, dz.i), 10) + 1) * ag.dY, 20)
            i = ag.dY << 1 + (ag.ep ^ 0x1)
            j_ = 0
            for b1 in range(10):
                j_ += arrayOfInt[b1]
                if cz.G + i < j_:
                    k = arrayOfInt[b1] - j_ + cz.G + i
                    ag.dZ[b + 1] = i16(idiv(k * 100, arrayOfInt[b1]) + b1 * 100)
                    if ag.dZ[b + 1] < b1 * 100 + 1:
                        ag.dZ[b + 1] = i16(b1 * 100 + 1)
                    if b == 1:
                        cz.G = k
                    break
        ag.ea = 0

    def i_v(self):  # c.java:1643-2136  (one map tick: erase, input, hero movement / actions)
        import config
        from pow.game.ar import ar
        arrayOfByte1 = [20, 20, 25]
        arrayOfByte2 = [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 6, 5, 5]
        i = -1
        j_ = 0
        bool_ = True
        k = 0
        m = 0
        cz = ag.cz
        self.aD()
        self.aF()
        self.aG()
        self.aH()
        self.aI()
        self.aK()
        self.aL()
        if ag.co == 1:
            self.aE()
        v = ag.cj
        if v in (-1, 50):
            i = 4
        elif v in (-3, 52):
            i = 2
        elif v in (-4, 54):
            i = 6
        elif v in (-2, 56):
            i = 0
        v = ag.ch
        if config.NO_COMBAT and v in (49, 51, 55, 57, 48, -5, 53, 35, 42):
            # PORT-EXTRA (POW_NO_COMBAT=1): attack, skill and potion keys do nothing
            v = None
        if v == 49:
            j_ = cz.V[0]
        elif v == 51:
            j_ = cz.V[1]
        elif v == 55:
            j_ = cz.V[2]
        elif v == 57:
            j_ = cz.V[3]
        elif v == 48:
            j_ = cz.V[4]
        elif v in (-5, 53):
            j_ = 3
        elif v in (35, 42):
            if 0 == ag.dU.a and cz.e[0] < 10:
                sel = cz.aa[0 if ag.ch == 42 else 1]
                ag.dU.a = cz.Z[sel].a
                brk = False
                if ag.dU.a > 9:
                    if cz.e[0] > 1:
                        ag.dU.a = 0
                        brk = True
                    else:
                        cz.e[0] = 11
                elif ag.dU.a != 0:
                    self.a__I(8)
                if not brk:
                    ag.dU.e = i16(sel)
                    ag.dU.b = 0
                    ag.dU.c.a = cz.a[0].a
                    ag.dU.c.b = cz.a[0].b
                    ag.dU.d = i16(ae.aT[cz.d[0]])
        elif v == -7:
            if ag.bg is not None:
                self.a__I(-1)
                ag.ai()
            ag.af_v()
            ag.cR.a = 1
            ag.cR.b = 0
            ag.cM[0] = 10
            ag.cM[2] = 0
            ag.cM[1] = 0
            ag.cN = 7
            ag.dE = ag.fZ
            ag.ck = 1
            ag.ct[10] = self.d_T(ag.bA.a_I(59))
            ag.ct[17] = self.d_T(ag.bA.a_I(27))
        if ag.dU.a > 0:
            if ag.dU.a > 9:
                cz.f[0] = ag.dU.b
                return
            return
        ag.bc.d_v()
        cz.f[0] = i16(cz.f[0] + 1)
        ag.cs[0] = i
        if cz.ab[cz.e[0]][cz.d[0]][cz.f[0]] > 200:
            if cz.e[0] == 2:
                ag.cs[4] = ag.cs[3] = ag.cs[2] = ag.cs[1] = ag.cs[0] = -1
                i = -1
            elif cz.e[0] == 10:
                from pow.game.e import e
                cz.f[0] = 10
                if ag.fq != 0:
                    e.b_II(ag.fq, -5)
                ag.cS.e_I(22)
                ag.dj = 0
                self.ar()
                return
            cz.f[0] = 0
            ag.eY = None
            ag.eX = None
            if cz.e[0] != 1:
                cz.e[0] = 0
        if config.HOLD_TO_MOVE and i == -1 and cz.e[0] < 2:
            # PORT-EXTRA (config.HOLD_TO_MOVE): the hero walks only while a direction key or the
            # mouse button is held; released = stand, still held after an attack = walk again
            from pow.game.Main import Main
            held = Main.b.held_direction() if Main.b is not None else None
            if held is None:
                if cz.e[0] == 1:
                    cz.e[0] = 0
                    cz.f[0] = 0
            else:
                hi = _HELD_DIR[held]
                if cz.e[0] == 0 or cz.c != hi:
                    cz.d[0] = cz.c = hi
                    cz.e[0] = 1
                    cz.f[0] = 0
        if cz.e[0] < 2:
            if i > -1:
                if ar.e_v() != 0:
                    cz.e[0] = 2
                    cz.f[0] = 0
                    cz.d[0] = cz.c = i
                    if ag.bg is not None:
                        ag.ai()
                elif cz.c == i:
                    cz.e[0] = cz.e[0] + 1 & 0x1
                    cz.f[0] = 0
                else:
                    cz.d[0] = cz.c = i
                    cz.e[0] = 1
                    cz.f[0] = 0
            if j_ == 3:
                if cz.N < 7:
                    cz.M = (cz.M + 1) % 3
                else:
                    cz.M = 0
                cz.N = 0
                cz.e[0] = 3 + cz.M + (cz.K ^ 0x1) * 3
                cz.f[0] = 0
                cz.d[0] = cz.c = ae.aT[cz.c] << 1
            elif j_ > 0 and ar.e_I(j_) != 0:
                cz.d[0] = cz.c = ae.aT[cz.c] << 1
                cz.e[0] = j_
                cz.f[0] = 0
                if cz.e[0] in (15, 16, 21, 22, 23, 24, 25):
                    self.a__I(11)
        n = cz.c
        e0 = cz.e[0]
        f0 = cz.f[0]
        if e0 == 1:
            k = ae.aw[n]
            m = ae.ax[n]
        elif e0 == 2:
            k = ae.aw[n] << 2
            m = ae.ax[n] << 2
        elif 3 <= e0 <= 8:
            k = idiv(ae.aw[n], 3)
            m = idiv(ae.ax[n], 3)
        elif e0 == 12:
            if 2 < f0 < 6:
                k = ae.aw[n] << 2
                m = ae.ax[n] << 2
        elif e0 in (13, 14):
            fall14 = e0 == 14
            if e0 == 13:
                if 4 < f0 < 8:
                    k = ae.aw[n] << 2
                    m = ae.ax[n] << 2
                    if k > 0:
                        k = ag.bc.a_LhII(cz.a[0], k, 6)
                    elif k < 0:
                        k = ag.bc.a_LhII(cz.a[0], k, 2)
                    if m > 0:
                        m = ag.bc.a_LhII(cz.a[0], m, 0)
                    elif m < 0:
                        m = ag.bc.a_LhII(cz.a[0], m, 4)
                    arrayOfInt = ag.bc.b_LhII(cz.a[0], k, m)
                    k = arrayOfInt[0]
                    m = arrayOfInt[1]
                    cz.a[0].a = i16(cz.a[0].a + k)
                    cz.a[0].b = i16(cz.a[0].b + m)
                    fall14 = True       # no break: falls into case 14
            if fall14:
                if 0 < f0 < 9:
                    k = ae.aw[n]
                    m = ae.ax[n]
        elif e0 == 10:
            if f0 < 10:
                cz.a[0].a = i16(cz.a[0].a + (-1 if (f0 & 0x1) != 0 else 1))
        elif e0 == 20:
            if 0 == (f0 & 0x1):
                k = ae.aw[n]
                m = ae.ax[n]
        elif e0 == 9 and cz.R > 0:
            cz.R -= 1
            n = cz.c + 4 & 0x7
            k = ae.aw[n] << 2
            m = ae.ax[n] << 2
        elif e0 == 9 and f0 == 1:
            n = cz.c + 4 & 0x7
            k = idiv(ae.aw[n] * 3, 4)
            m = idiv(ae.ax[n] * 3, 4)
        else:
            k = m = 0
        if k != 0 or m != 0:
            i = ag.bc.a_LhIIII(cz.a[0], k, m, n, -1)
            if cz.e[0] == 1:
                if cz.c in (0, 2, 4, 6):
                    if F14:
                        # DECOMP-FIX F14: decompiled as `k = aw[i]; m = ax[i]; if (i == -1 &&
                        # (i = ar.c(..)) != -1 && (i = bc.a(.., k, m, i, -1)) > -1 && i < 8)`:
                        # aw[-1] when the hero walks into a wall. The step must use the new
                        # direction returned by ar.c() (slide around the corner).
                        if i == -1:
                            i = ar.c_LhII(cz.a[0], cz.d[0], -1)
                            if i != -1:
                                k = ae.aw[i]
                                m = ae.ax[i]
                                i = ag.bc.a_LhIIII(cz.a[0], k, m, i, -1)
                                if -1 < i < 8:
                                    cz.d[0] = i
                    else:
                        if i < 0:
                            raise IndexError("ArrayIndexOutOfBoundsException: aw[%d]" % i)
                        k = ae.aw[i]
                        m = ae.ax[i]
                        if i == -1:
                            i = ar.c_LhII(cz.a[0], cz.d[0], -1)
                            if i != -1:
                                i = ag.bc.a_LhIIII(cz.a[0], k, m, i, -1)
                                if -1 < i < 8:
                                    cz.d[0] = i
                elif cz.c in (1, 3, 5, 7):
                    if i != -1 and i != 9:
                        cz.d[0] = i
        e0 = cz.e[0]
        f0 = cz.f[0]
        if 3 <= e0 <= 8 or 21 <= e0 <= 24:
            if 3 <= e0 <= 8 and f0 == arrayOfByte2[e0]:
                ag.bc.f_v()
            if f0 == arrayOfByte2[e0]:
                if e0 in (3, 4, 6, 7):
                    self.a__I(15)
                elif e0 in (5, 8, 21, 22):
                    self.a__I(16)
                elif e0 in (23, 24):
                    self.a__I(9)
                ag.bc.d_I(0)
                ag.bc.c_v()
        elif e0 == 12:
            if 2 < f0 < 6:
                if f0 == 3:
                    self.a__I(7)
                ag.bc.d_I(0)
                ag.bc.c_v()
        elif e0 == 13:
            if 4 < f0 < 8:
                if f0 == 5:
                    self.a__I(7)
                ag.bc.d_I(0)
                ag.bc.c_v()
        elif e0 == 14:
            if f0 in (2, 4, 6, 8):
                self.a__I(15)
                ag.bc.d_I(0)
                ag.bc.c_v()
        elif e0 in (15, 16):
            if f0 == 11:
                self.a__I(8)
                if e0 == 15:
                    cz.p += idiv(cz.y * (4 + cz.W[3]), 25)
                else:
                    cz.p += idiv(cz.y * (9 + cz.W[4]), 20)
                ar.b_v()
        elif e0 in (17, 18, 19):
            if f0 == 11:
                if e0 != 18:
                    cz.A = idiv(cz.w * cz.W[e0 - 12], arrayOfByte1[e0 - 17])
                    if cz.A < 1:
                        cz.A = 1
                    if cz.W[e0 - 12] < 4:
                        cz.C = 50
                    elif cz.W[e0 - 12] < 8:
                        cz.C = 100
                    else:
                        cz.C = 150
                if e0 != 17:
                    cz.B = idiv(cz.x * cz.W[e0 - 12], arrayOfByte1[e0 - 17])
                    if cz.B < 1:
                        cz.B = 1
                    if cz.W[e0 - 12] < 4:
                        cz.D = 50
                    elif cz.W[e0 - 12] < 8:
                        cz.D = 100
                    else:
                        cz.D = 150
            elif f0 == 4:
                self.a__I(12)
        elif e0 == 20:
            if (f0 & 0x1) != 0:
                self.a__I(15)
                if f0 in (1, 5, 9):
                    cz.M = 0
                else:
                    cz.M = 2
                ag.bc.d_I(0)
                ag.bc.c_v()
        elif e0 == 25:
            if (f0 & 0x1) != 0:
                self.a__I(9)
                ag.bc.d_I(0)
                ag.bc.c_v()
        elif e0 in (26, 27):
            if f0 == 8:
                if e0 == 27:
                    self.a__I(9)
                ag.bc.d_I(0)
                ag.bc.c_v()
            if 1 < f0 < 9:
                if f0 == 2:
                    self.a__I(13)
                bool_ = False
        elif e0 == 28:
            if f0 == 22:
                ag.bc.d_I(0)
                ag.bc.c_v()
                ag.ck = 1
            elif f0 > 3:
                bool_ = False
                ag.ck = 1
                ag.cl = 1
                if f0 == 6:
                    self.a__I(13)
        elif e0 == 29:
            if f0 == 22:
                ag.bc.d_I(0)
                ag.bc.c_v()
                ag.ck = 1
            elif f0 > 6:
                if f0 == 7:
                    self.a__I(14)
                bool_ = False
                ag.ck = 1
                if f0 == 12 or f0 == 16:
                    ag.cl = 2
                else:
                    ag.cl = 1
        elif e0 == 30:
            if f0 > 3:
                if f0 == 4:
                    self.a__I(11)
                elif f0 == 13:
                    self.a__I(9)
                if f0 < 15:
                    bool_ = False
                    ag.cl = 1
                ag.ck = 1
                if f0 == 9 or f0 == 11:
                    ag.cl = 2
                elif f0 == 15:
                    ag.bc.d_I(0)
                    ag.bc.c_v()
        if bool_:
            ag.bc.j_v()
            ag.bd.d_v()
            ag.bc.i_v()
            ag.bc.g_v()
            ar.h_v()
        c.f_v()

    def aD(self):  # c.java:2138-2148  (erase the breaking-object animation)
        for b in range(ag.cB):
            cA = ag.cA[b]
            if cA.a != 0 and cA.h != 0:
                i = cA.b.a - ag.ca.a
                j_ = cA.b.b - ag.ca.b
                k = 2 - cA.h
                cA.h = i16(cA.h - 1)
                self.m_III(k, i, j_)

    def m_III(self, paramInt1, paramInt2, paramInt3):  # c.java:2150-2152  (erase an eV frame from ct[7])
        v_ = ag.eV[paramInt1]
        self.b_MIIIIII(ag.ct[7], paramInt2 - v_.e, paramInt3 - v_.f, v_.c, v_.d,
                       paramInt2 - v_.e + ag.cc.a, paramInt3 - v_.f + ag.cc.b)

    def aE(self):  # c.java:2154-2162  (erase the exit arrows)
        arrayOfInt1 = [ag.dd - 9, 5, ag.dd - 9, ag.bY.a - 31]
        arrayOfInt2 = [ag.bY.b - 31, ag.de - 13, 5, ag.de - 13]
        if ag.cn < 1 and (ag.cm & 0x2) != 0:
            for b in range(4):
                if ag.eO[ag.eP].a[b] != 0 and ag.ct[21 + b] is not None:
                    self.b_MIIIIII(ag.ct[7], arrayOfInt1[b], arrayOfInt2[b], ag.ct[21 + b].getWidth(),
                                   ag.ct[21 + b].getHeight(), arrayOfInt1[b] + ag.cc.a, arrayOfInt2[b] + ag.cc.b)

    def aF(self):  # c.java:2164-2253  (erase the hero at its previous position)
        cz = ag.cz
        if cz.e[1] < 12:
            arrayOfY1 = cz.aC
            arrayOfY2 = cz.aE
            arrayOfY3 = ag.eS[cz.K]
        else:
            arrayOfY1 = cz.aD
            arrayOfY2 = cz.aF
            arrayOfY3 = ag.eT[cz.K]
        i = cz.a[1].a - ag.ca.a
        j_ = cz.a[1].b - ag.ca.b
        ct7 = ag.ct[7]
        ccx = ag.cc.a
        ccy = ag.cc.b
        y1 = arrayOfY1[cz.L]
        y2 = arrayOfY2[cz.L]
        y3 = arrayOfY3[cz.L]
        self.b_MIIIIII(ct7, i - y1.e, j_ - y1.f, y1.c, y1.d, i - y1.e + ccx, j_ - y1.f + ccy)
        self.b_MIIIIII(ct7, i - y2.e, j_ - y2.f, y2.c, y2.d, i - y2.e + ccx, j_ - y2.f + ccy)
        self.b_MIIIIII(ct7, i - y2.e + idiv(y2.c, 2) - 13, j_ - y2.f + y2.d - 5, 27, 11,
                       i - y2.e + ccx + idiv(y2.c, 2) - 13, j_ - y2.f + ccy + y2.d - 5)
        self.b_MIIIIII(ct7, i - y3.e, j_ - y3.f, y3.c, y3.d, i - y3.e + ccx, j_ - y3.f + ccy)
        if ag.ek == 1 or ag.el == 1:
            k = (ag.bN - 1) % 3
            q = ag.eQ[k]
            self.b_MIIIIII(ct7, i - q.e, j_ - q.f - 18, 40, 50, i - q.e + ccx, j_ - q.f + ccy - 18)
            ag.el = 0
        if cz.e[1] < 12:
            if 11 < cz.L < 36:
                k = cz.L - 12
                if (k & 0x1) != 0:
                    k &= 0xFFFE
                    self.m_II(-1, k % 6 >> 1)
        else:
            k = -1
            e1 = cz.e[1]
            f1 = cz.f[1]
            if e1 == 12:
                if 2 < f1 < 6:
                    k = 1
            elif e1 == 13:
                if 4 < f1 < 8:
                    k = 1
            elif e1 == 14:
                if f1 in (2, 4, 6, 8):
                    k = 1
            elif e1 == 20:
                if (f1 & 0x1) != 0:
                    k = cz.M
            elif e1 == 21:
                if f1 == 5:
                    k = 2
            elif e1 == 22:
                if f1 == 6:
                    k = 2
            elif e1 == 25:
                if (f1 & 0x1) != 0:
                    k = 2
            if k > -1:
                self.m_II(-1, k)
        if cz.T != 0:
            u = ag.eY[cz.U]
            self.b_MIIIIII(ct7, i - u.e, j_ - u.f, u.c, u.d, i - u.e + ccx, j_ - u.f + ccy)
            cz.U += 1
            if cz.U > 5:
                cz.T = 0
        if cz.O != 0 and cz.P > -1:
            i = cz.Q.a - ag.ca.a
            j_ = cz.Q.b - ag.ca.b
            k = cz.P
            self.m_III(k, i, j_)

    def m_II(self, paramInt1, paramInt2):  # c.java:2255-2281  (erase a weapon trail)
        if paramInt1 > -1:
            h_ = ag.ex[paramInt1].a[1]
            if ag.ex[paramInt1].f[1] == 19:
                i = ag.ex[paramInt1].e[1] + (ag.ex[paramInt1].g[1] >> 1 << 1) & 0x7
            else:
                i = ag.ex[paramInt1].e[1]
        else:
            h_ = ag.cz.a[1]
            if ag.cz.e[1] == 25:
                i = ag.cz.d[1] + (ag.cz.f[1] >> 1 << 1) & 0x7
            else:
                i = ag.cz.d[1]
        j_ = (i >> 1) * 6 + (paramInt2 << 1)
        k = h_.a - ag.ca.a
        m = h_.b - ag.ca.b
        for b in range(2):
            u = ag.eU[j_]
            self.b_MIIIIII(ag.ct[7], k - u.e, m - u.f, u.c, u.d, k - u.e + ag.cc.a, m - u.f + ag.cc.b)
            j_ += 1

    def aG(self):  # c.java:2283-2340  (erase the enemies)
        cc_a = ag.cc.a
        cc_b = ag.cc.b
        ct7 = ag.ct[7]
        for b in range(ag.ez):
            s1 = ag.ey[b]
            ex = ag.ex[s1]
            ex.f[0] = min(ex.f[0], len(ex.B[ex.e[0]]) - 1)
            s2 = ex.B[ex.e[1]][ex.f[1]][ex.g[1]]
            i = ex.a[1].a - ag.ca.a
            j_ = ex.a[1].b - ag.ca.b
            if ex.h > 200:
                if s2 < 180:
                    D = ex.D[s2]
                    if ex.h == 203:
                        az = ae.az[ae.aT[ex.e[1]]]
                        self.b_MIIIIII(ct7, i - D.e + az[0], j_ - D.f + az[1], D.c + az[2], D.d + az[3],
                                       i - D.e + cc_a + az[0], j_ - D.f + cc_b + az[1])
                    else:
                        self.b_MIIIIII(ct7, i - D.e, j_ - D.f, D.c, D.d, i - D.e + cc_a, j_ - D.f + cc_b)
            else:
                if ex.f[1] < 6:
                    arrayOfY2 = ag.et[3]
                    arrayOfY1 = ag.et[4]
                    arrayOfY3 = ag.et[5]
                else:
                    arrayOfY2 = ag.et[6]
                    arrayOfY1 = ag.et[7]
                    arrayOfY3 = ag.et[8]
                if s2 < 180:
                    y2 = arrayOfY2[s2]
                    self.b_MIIIIII(ct7, i - y2.e + idiv(y2.c, 2) - 13, j_ - y2.f + y2.d - 4, 27, 11,
                                   i - y2.e + cc_a + idiv(y2.c, 2) - 13, j_ - y2.f + cc_b + y2.d - 5)
                    if ag.em == 1 or ag.en == 1:
                        k = (ag.bN - 1) % 3
                        q = ag.eQ[k]
                        self.b_MIIIIII(ct7, i - q.e, j_ - q.f - 18, 40, 50, i - q.e + cc_a, j_ - q.f + cc_b - 18)
                        ag.en = 0
                else:
                    y2 = arrayOfY2[20]
                    self.b_MIIIIII(ct7, i - y2.e + idiv(y2.c, 2) - 9, j_ - y2.f + y2.d - 4, 18, 7,
                                   i - y2.e + cc_a + idiv(y2.c, 2) - 9, j_ - y2.f + cc_b + y2.d - 4)
                if s2 < 180:
                    for Y in (arrayOfY1[s2], arrayOfY2[s2], arrayOfY3[s2]):
                        self.b_MIIIIII(ct7, i - Y.e, j_ - Y.f, Y.c, Y.d, i - Y.e + cc_a, j_ - Y.f + cc_b)
                self.O_I(s1)
                if -1 < ex.y < 100:
                    self.m_II(s1, ex.y)
            if ex.w != 0:
                fe = ag.fe[ex.x]
                self.b_MIIIIII(ct7, i - fe.e, j_ - fe.f, fe.c, fe.d, i - fe.e + cc_a, j_ - fe.f + cc_b)
                ex.x = i8(ex.x + 1)
                if ex.x > 5:
                    ex.w = 0
            if ex.t != 0 and ex.u > -1:
                i = ex.v.a - ag.ca.a
                j_ = ex.v.b - ag.ca.b
                k = ex.u + (ex.t - 1 << 1)
                self.m_III(k, i, j_)

    def O_I(self, paramInt):  # c.java:2350-2421  (erase a general's weapon effect)
        ex = ag.ex[paramInt]
        h_ = ex.a[1]          # (the same object: case 21 moves it, as in the original)
        ag.fk = 0
        A = c.a_ALyI
        f1 = ex.f[1]
        g1 = ex.g[1]
        if f1 == 6:
            if 2 < g1 < 6:
                ag.fk = 1
                ag.fj = A(ag.eW, ex.e[1] + (g1 & 0x1))
        elif f1 == 7:
            if 4 < g1 < 8:
                ag.fk = 1
                ag.fj = A(ag.eW, ex.e[1] + (g1 & 0x1))
        elif f1 == 8:
            if 0 < g1 < 9:
                ag.fk = 1
                ag.fj = A(ag.eW, ex.e[1] + (g1 & 0x1))
        elif f1 in (9, 10):
            if g1 > 3:
                ag.fk = 1
                ag.fj = A(ag.fb, g1 - 4)
        elif f1 in (11, 12, 13):
            if 3 < g1 < 10:
                ag.fk = 3
                ag.fj = A(ag.fb, g1 - 4)
        elif f1 in (15, 18):
            if g1 == 5 or g1 == 6:
                ag.fk = 1
                ag.fj = A(ag.fb, g1 - 5)
        elif f1 == 16:
            if 1 < g1 < 6:
                ag.fk = 1
                ag.fj = A(ag.eW, g1 & 0x1)
        elif f1 == 17:
            if g1 == 5 or g1 == 6:
                ag.fk = 1
                ag.fj = A(ag.eW, g1 - 5)
        elif f1 in (20, 21):
            if f1 == 21 and g1 == 9:        # case 21 falls through into case 20
                ag.fk = 3
                ag.fj = A(ag.fb, 1)
                h_.a = i16(h_.a + ae.aA[ex.e[1] >> 1])
                h_.b = i16(h_.b + ae.aB[ex.e[1] >> 1])
            if 1 < g1 < 9:
                ag.fk = 3
                ag.fj = A(ag.fb, g1 - 2 + (ex.e[1] >> 1) * 7)
        if ag.fk != 0:
            i = h_.a - ag.ca.a
            j_ = h_.b - ag.ca.b
            ag.fk = 0
            fj = ag.fj[0]
            self.b_MIIIIII(ag.ct[7], i - fj.e - 8, j_ - fj.f - 8, fj.c + 16, fj.d + 16,
                           i - fj.e - 8 + ag.cc.a, j_ - fj.f - 8 + ag.cc.b)

    @staticmethod
    def a_ALyI(paramArrayOfy, paramInt):  # c.java:2342-2348
        return paramArrayOfy[paramInt:]

    def aH(self):  # c.java:2423-2428  (erase the dropped items)
        for b in range(ag.cD):
            cC = ag.cC[b]
            if cC.a != 0:
                x0 = cC.b.a - ag.ca.a - (cC.e >> 1)
                y0 = cC.b.b - ag.ca.b - (cC.f >> 1)
                self.b_MIIIIII(ag.ct[7], x0, y0, cC.e, cC.f, x0 + ag.cc.a, y0 + ag.cc.b)

    def aI(self):  # c.java:2430-2514  (erase the hero's weapon effects)
        from pow.game.structs import h
        cz = ag.cz
        h_ = h()
        h_.a = cz.a[1].a
        h_.b = cz.a[1].b
        ag.fh = 0
        e1 = cz.e[1]
        f1 = cz.f[1]
        A = c.a_ALyI
        if e1 == 2:
            ag.fh = 1
            ag.fj = A(ag.eW, cz.d[1] + (f1 & 0x1))
        elif e1 == 12:
            if 2 < f1 < 6:
                ag.fh = 1
                ag.fj = A(ag.eW, cz.d[1] + (f1 & 0x1))
        elif e1 == 13:
            if 4 < f1 < 8:
                ag.fh = 1
                ag.fj = A(ag.eW, cz.d[1] + (f1 & 0x1))
        elif e1 == 14:
            if 0 < f1 < 9:
                ag.fh = 1
                ag.fj = A(ag.eW, cz.d[1] + (f1 & 0x1))
        elif e1 in (15, 16):
            if f1 > 3:
                ag.fh = 1
                ag.fj = A(ag.eY, f1 - 4)
        elif e1 in (17, 18, 19):
            if 3 < f1 < 10:
                ag.fh = 3
                ag.fj = A(ag.eY, f1 - 4)
        elif e1 in (21, 24):
            if f1 == 5 or f1 == 6:
                ag.fh = 1
                ag.fj = A(ag.eY, f1 - 5)
        elif e1 == 22:
            if 1 < f1 < 6:
                ag.fh = 1
                ag.fj = A(ag.eW, f1 & 0x1)
        elif e1 == 23:
            if f1 == 5 or f1 == 6:
                ag.fh = 1
                ag.fj = A(ag.eW, f1 - 5)
        elif e1 in (26, 27):
            if e1 == 27 and f1 == 9:        # case 27 falls through into case 26
                ag.fh = 3
                ag.fj = A(ag.eY, 1)
                h_.a = i16(h_.a + ae.aA[cz.d[1] >> 1])
                h_.b = i16(h_.b + ae.aB[cz.d[1] >> 1])
            if 1 < f1 < 9:
                ag.fh = 3
                ag.fj = A(ag.eY, f1 - 2 + (cz.d[1] >> 1) * 7)
        if ag.fh != 0:
            i = h_.a - ag.ca.a
            j_ = h_.b - ag.ca.b
            for b in range(ag.fg):
                fj = ag.fj[b]
                self.b_MIIIIII(ag.ct[7], i - fj.e - 8, j_ - fj.f - 8, fj.c + 16, fj.d + 16,
                               i - fj.e + ag.cc.a - 8, j_ - fj.f + ag.cc.b - 8)
            ag.fh = 0
            ag.fg = 1

    def aJ(self):  # c.java:2516-2523  (erase the message box dT)
        from pow.game.g import g
        i = (g.b_v() + g.c_v()) * len(ag.dT.c) + 3
        self.b_MIIIIII(ag.ct[7], ag.bY.a - i - 7, 0, i + 7, 40, ag.bY.a - i + ag.cc.a - 7, ag.cc.b)
        c.a_IIII(ag.ca.a + ag.bY.a - i - 7, ag.ca.b, i + 7, 40)
        ag.dT.b = i16(ag.dT.b - 1)
        if ag.dT.b < 1:
            ag.dT.a = 0

    def aK(self):  # c.java:2525-2537  (erase the gold counter and the clock)
        if ag.dT.a != 0:
            self.aJ()
        else:
            i = ag.D_I(ag.cz.I) * 10 + 1
            self.b_MIIIIII(ag.ct[7], ag.bY.a - 3 - i - 7, 1, i + 7, 29, ag.bY.a - 3 - i + ag.cc.a - 7, 1 + ag.cc.b)
            c.a_IIII(ag.ca.a + ag.bY.a - 3 - i - 7, ag.ca.b + 1, i + 7, 29)
            if ag.cz.H > ag.cz.I:
                ag.cz.I += 1
        self.b_MIIIIII(ag.ct[7], 0, 0, 60, 20, ag.cc.a, ag.cc.b)
        c.a_IIII(ag.ca.a, ag.ca.b, 60, 20)

    def aL(self):  # c.java:2539-2590  (potion / scroll effect dU)
        arrayOfByte1 = [2, 10, 100, 2, 2, 2, 2, 2, 2, 2, 2, 2, 100, 100]
        arrayOfShort = [63, 60]
        arrayOfByte2 = [1, 1, 1, 2, 2, 2, 3, 3, 3]
        arrayOfByte3 = [30, 60, 100, 30, 60, 100, 30, 60, 100]
        dU = ag.dU
        if dU.a != 0:
            if dU.a <= 9 or dU.b != 0:
                hf = dU.h[dU.f]
                i = dU.c.a - hf.e - ag.ca.a
                j_ = dU.c.b - hf.f - ag.ca.b
                s1 = hf.c
                s2 = hf.d
                if dU.a < 0:
                    if dU.a == -1:
                        i -= 10
                        j_ -= 6
                        s1 = i16(s1 + 20)
                        s2 = i16(s2 + 11)
                        if dU.b in (1, 4, 7):
                            ag.bc.d_I(dU.a)
                    elif dU.b == 1:
                        ag.bc.d_I(dU.a)
                self.b_MIIIIII(ag.ct[7], i, j_, s1, s2, i + ag.cc.a, j_ + ag.cc.b)
            dU.b = i16(dU.b + 1)
            if dU.a > 9 and dU.b > 4:
                self.a__I(9)
                dU.g = None
                dU.h = self.K_I(arrayOfShort[dU.a - 10])
                dU.c.a = i16(dU.c.a + ae.aA[dU.d])
                dU.c.b = i16(dU.c.b + ae.aB[dU.d])
                dU.a = i16(dU.a - 12)
                dU.b = 0
            if dU.b >= arrayOfByte1[dU.a + 2]:
                if dU.a > 0:
                    if (arrayOfByte2[dU.a - 1] & 0x1) != 0:
                        ag.cz.p += idiv(ag.cz.y * arrayOfByte3[dU.a - 1], 100)
                    if (arrayOfByte2[dU.a - 1] & 0x2) != 0:
                        ag.cz.r += idiv(ag.cz.z * arrayOfByte3[dU.a - 1], 100)
                    from pow.game.ar import ar
                    ar.b_v()
                self.k_II(0, 0)
                dU.a = 0
                dU.g = None
                dU.h = None
