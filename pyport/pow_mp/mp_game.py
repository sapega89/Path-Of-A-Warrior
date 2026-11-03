"""MpGame (m.java): the concrete canvas of the MP jar, plays the menu music.

Generated once from pyport/mp_java/m.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""
from pow_mp.rt import _js


from pow_mp.mp_canvas import MpCanvas

class MpGame(MpCanvas):
    fb = None  # m.java:6 c
    fc = (-1)  # m.java:7 int
    fd = (-1)  # m.java:8 int

    def __init__(self, main):  # m.java:10
        super().__init__(main)
        MpGame.fb = PlayerPool(7, 1, True, True)

    @staticmethod
    def v_I(n2):  # m.java:15
        MpGame.fc = n2

    def ak_v(self):  # m.java:19
        MpGame.fb.b()
        bl = False
        bl2 = True
        n2 = MpGame.fc
        MpGame.fc = (-1)
        if (MpCanvas.am != 0) and (n2 != (-1)):
            if n2 == 1:
                if MpGame.fd == n2:
                    bl2 = False
                else:
                    self.ag_v()
                MpGame.fd = n2
                bl = True
            else:
                MpGame.fd = (-1)
                bl = False
            if bl2:
                self.b_IZ(n2, bl)

    def b_IZ(self, n2, bl):  # m.java:44
        MpGame.fb.a_I((MpCanvas.am * 20))
        if MpCanvas.am == 0:
            self.ag_v()
            return
        if n2 == 1:
            MpGame.fb.a_TI(_js(_js("/snd", n2), ".mid"), n2)
        else:
            MpGame.fb.a_TI(_js(_js("/snd", n2), ".wav"), n2)
        MpGame.fb.a_IZ(n2, bl)

    def ag_v(self):  # m.java:58
        MpGame.fc = (-1)
        MpGame.fd = (-1)
        MpGame.fb.a_v()


def _static_init():
    pass


def _late_imports():
    global PlayerPool, MpCanvas
    from pow_mp.player_pool import PlayerPool
    from pow_mp.mp_canvas import MpCanvas
