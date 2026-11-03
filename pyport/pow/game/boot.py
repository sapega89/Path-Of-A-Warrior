"""af.java - boot screens: logo -> "sound enabled?" -> title. Literal port."""
from pow.game.game_canvas import GameCanvas
from pow.game.gfx import Gfx
from pow.midp import system


class Boot(GameCanvas):
    b = 0   # public static int b = 0;   af.java:4  (0 logo, 1 sound question, 2 title)
    c = 0   # public static long c;      af.java:6

    def __init__(self):  # af.java:2, 8-11
        super().__init__(GameCanvas.bs)
        self.a = self.d_T("logo1")    # Image a = d("logo1");   (instance initializer)
        Boot.c = system.currentTimeMillis()

    def a_v(self):  # af.java:15-36  (paint)
        from pow.game.midlet import Midlet
        if Boot.b == 0:
            GameCanvas.u_I(16777215)
            if self.a is not None:
                Gfx.a_MIII(self.a, GameCanvas.bL, GameCanvas.bM, 3)
            if system.currentTimeMillis() - Boot.c > 2500:
                self.a = None
                Boot.b = 1
                GameCanvas.cS.e_I(40)
                return
        else:
            if Boot.b == 1:
                GameCanvas.u_I(0)
                Gfx.a_Lg(GameCanvas.bu)
                GameCanvas.cS.c_v()
                return
            if Boot.b == 2:
                Midlet.b.S_v()

    def b_v(self):  # af.java:38-64  (keys)
        if Boot.b == 0:
            return
        if Boot.b == 1:
            i = GameCanvas.cS.b_v()
            if i != -1:
                GameCanvas.df = (i == 0)
                if i == 0:
                    if GameCanvas.dg == 0:
                        GameCanvas.dg = 75
                else:
                    GameCanvas.dg = 0
                self.a__I(0)
                Boot.b = 2
                self.E_v()
            return
        if Boot.b == 2 and Boot.b_I(GameCanvas.ch):
            GameCanvas.ck = 1
            GameCanvas.cv = None
            GameCanvas.cw = None
            GameCanvas.bb.g_v()
            self.T_v()

    @staticmethod
    def b_I(paramInt):  # af.java:66-92  ("press any key": which keys count)
        return paramInt in (-10, -8, -7, -6, -5, -4, -3, -2, -1, 35, 42, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57)
