"""MpGame (m.java): the concrete canvas of the MP jar, plays the menu music.

Generated once from pyport/mp_java/m.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""
from pow_mp.rt import _js


from pow_mp.mp_canvas import MpCanvas

class MpGame(MpCanvas):
    players = None  # m.java:6 c
    requested_music = (-1)  # m.java:7 int
    music = (-1)  # m.java:8 int

    def __init__(self, main):  # m.java:10
        super().__init__(main)
        MpGame.players = PlayerPool(7, 1, True, True)

    @staticmethod
    def request_music(n2):  # m.java:15
        MpGame.requested_music = n2

    def tick_music(self):  # m.java:19
        MpGame.players.tick()
        bl = False
        bl2 = True
        n2 = MpGame.requested_music
        MpGame.requested_music = (-1)
        if (MpCanvas.volume != 0) and (n2 != (-1)):
            if n2 == 1:
                if MpGame.music == n2:
                    bl2 = False
                else:
                    self.stop_music()
                MpGame.music = n2
                bl = True
            else:
                MpGame.music = (-1)
                bl = False
            if bl2:
                self.play_music(n2, bl)

    def play_music(self, n2, bl):  # m.java:44
        MpGame.players.set_volume((MpCanvas.volume * 20))
        if MpCanvas.volume == 0:
            self.stop_music()
            return
        if n2 == 1:
            MpGame.players.load(_js(_js("/snd", n2), ".mid"), n2)
        else:
            MpGame.players.load(_js(_js("/snd", n2), ".wav"), n2)
        MpGame.players.play(n2, bl)

    def stop_music(self):  # m.java:58
        MpGame.requested_music = (-1)
        MpGame.music = (-1)
        MpGame.players.stop()


def _static_init():
    pass


def _late_imports():
    global PlayerPool, MpCanvas
    from pow_mp.player_pool import PlayerPool
    from pow_mp.mp_canvas import MpCanvas
