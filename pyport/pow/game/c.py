"""c.java - map, combat and the story player (bd). Literal port, partial:
only c(int) (one page of a prologue / epilogue) is ported so far; the map and combat
(phases 3-4) are not."""
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
