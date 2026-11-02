"""af.java - boot screens: logo -> "sound enabled?" -> title. Literal port."""
from pow.game.game_canvas import GameCanvas
from pow.game.gfx import Gfx
from pow.midp import system


class Boot(GameCanvas):
    step = 0   # public static int b = 0;   af.java:4  (0 logo, 1 sound question, 2 title)
    start_time = 0   # public static long c;      af.java:6

    def __init__(self):  # af.java:2, 8-11
        super().__init__(GameCanvas.midlet)
        self.logo = self.d_T("logo1")    # Image a = d("logo1");   (instance initializer)
        Boot.start_time = system.currentTimeMillis()

    def a_v(self):  # af.java:15-36  (paint)
        from pow.game.midlet import Midlet
        if Boot.step == 0:
            GameCanvas.u_I(16777215)
            if self.logo is not None:
                Gfx.a_MIII(self.logo, GameCanvas.screen_cx, GameCanvas.screen_cy, 3)
            if system.currentTimeMillis() - Boot.start_time > 2500:
                self.logo = None
                Boot.step = 1
                GameCanvas.popups.e_I(40)
                return
        else:
            if Boot.step == 1:
                GameCanvas.u_I(0)
                Gfx.a_Lg(GameCanvas.font_white)
                GameCanvas.popups.c_v()
                return
            if Boot.step == 2:
                Midlet.canvas.S_v()

    def b_v(self):  # af.java:38-64  (keys)
        if Boot.step == 0:
            return
        if Boot.step == 1:
            i = GameCanvas.popups.b_v()
            if i != -1:
                GameCanvas.sound_on = (i == 0)
                if i == 0:
                    if GameCanvas.volume == 0:
                        GameCanvas.volume = 75
                else:
                    GameCanvas.volume = 0
                self.a__I(0)
                Boot.step = 2
                self.E_v()
            return
        if Boot.step == 2 and Boot.b_I(GameCanvas.key):
            GameCanvas.redraw = 1
            GameCanvas.title_press = None
            GameCanvas.title_logo = None
            GameCanvas.menus.g_v()
            self.T_v()

    @staticmethod
    def b_I(paramInt):  # af.java:66-92  ("press any key": which keys count)
        return paramInt in (-10, -8, -7, -6, -5, -4, -3, -2, -1, 35, 42, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57)
