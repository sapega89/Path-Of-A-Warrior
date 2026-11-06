"""MpGame: the concrete canvas of the multiplayer, plays the menu music.
"""
from pow.game.online.mp_canvas import MpCanvas
from pow.game.online.rt import _js


class MpGame(MpCanvas):
    players = None  # c
    requested_music = (-1)  # int
    music = (-1)  # int

    def __init__(self, main):
        super().__init__(main)
        MpGame.players = PlayerPool(7, 1, True, True)

    @staticmethod
    def request_music(music):
        MpGame.requested_music = music

    def tick_music(self):
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

    def play_music(self, music, loop):
        MpGame.players.set_volume(MpCanvas.volume * 20)
        if MpCanvas.volume == 0:
            self.stop_music()
            return
        if music == 1:
            MpGame.players.load(_js(_js("/snd", music), ".mid"), music)
        else:
            MpGame.players.load(_js(_js("/snd", music), ".wav"), music)
        MpGame.players.play(music, loop)

    def stop_music(self):
        MpGame.requested_music = (-1)
        MpGame.music = (-1)
        MpGame.players.stop()


def _static_init():
    pass


def _late_imports():
    global PlayerPool, MpCanvas
    from pow.game.online.mp_canvas import MpCanvas
    from pow.game.online.player_pool import PlayerPool
