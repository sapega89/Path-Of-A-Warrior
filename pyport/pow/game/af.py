"""af.java - boot screens: logo -> "sound enabled?" -> title. Literal port."""
from pow.game.ag import ag
from pow.game.x import x
from pow.midp import system


class af(ag):
    b = 0   # public static int b = 0;   af.java:4  (0 logo, 1 sound question, 2 title)
    c = 0   # public static long c;      af.java:6

    def __init__(self):  # af.java:2, 8-11
        super().__init__(ag.bs)
        self.a = self.d_T("logo1")    # Image a = d("logo1");   (instance initializer)
        af.c = system.currentTimeMillis()

    def a_v(self):  # af.java:15-36  (paint)
        from pow.game.Main import Main
        if af.b == 0:
            ag.u_I(16777215)
            if self.a is not None:
                x.a_MIII(self.a, ag.bL, ag.bM, 3)
            if system.currentTimeMillis() - af.c > 2500:
                self.a = None
                af.b = 1
                ag.cS.e_I(40)
                return
        else:
            if af.b == 1:
                ag.u_I(0)
                x.a_Lg(ag.bu)
                ag.cS.c_v()
                return
            if af.b == 2:
                Main.b.S_v()

    def b_v(self):  # af.java:38-64  (keys)
        if af.b == 0:
            return
        if af.b == 1:
            i = ag.cS.b_v()
            if i != -1:
                ag.df = (i == 0)
                if i == 0:
                    if ag.dg == 0:
                        ag.dg = 75
                else:
                    ag.dg = 0
                self.a__I(0)
                af.b = 2
                self.E_v()
            return
        if af.b == 2 and af.b_I(ag.ch):
            ag.ck = 1
            ag.cv = None
            ag.cw = None
            ag.bb.g_v()
            self.T_v()

    @staticmethod
    def b_I(paramInt):  # af.java:66-92  ("press any key": which keys count)
        return paramInt in (-10, -8, -7, -6, -5, -4, -3, -2, -1, 35, 42, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57)
