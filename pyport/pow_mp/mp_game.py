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
    def request_music(music):  # m.java:15
        MpGame.requested_music = music

    def tick_music(self):  # m.java:19
        MpGame.players.tick()
        loop = False
        restart = True
        music = MpGame.requested_music
        MpGame.requested_music = (-1)
        if (MpCanvas.volume != 0) and (music != (-1)):
            if music == 1:
                if MpGame.music == music:
                    restart = False
                else:
                    self.stop_music()
                MpGame.music = music
                loop = True
            else:
                MpGame.music = (-1)
                loop = False
            if restart:
                self.play_music(music, loop)

    def play_music(self, music, loop):  # m.java:44
        MpGame.players.set_volume(MpCanvas.volume * 20)
        if MpCanvas.volume == 0:
            self.stop_music()
            return
        if music == 1:
            MpGame.players.load(_js(_js("/snd", music), ".mid"), music)
        else:
            MpGame.players.load(_js(_js("/snd", music), ".wav"), music)
        MpGame.players.play(music, loop)

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
