"""c.java - map, combat and the story player (bd). Literal port, partial:
c(int) (one page of a prologue / epilogue) and d(int) / g() (end of a mission) are ported;
the map and combat (phases 3-4) are not."""
from pow.game.ag import ag
from pow.midp.jint import i32


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
