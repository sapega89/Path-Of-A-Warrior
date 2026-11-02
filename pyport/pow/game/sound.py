"""k.java - sound manager (music snd0-2, SFX snd3-16). Literal port."""
from pow.game.game_canvas import GameCanvas
from pow.midp import system
from pow.game.player_pool import PlayerPool


class Sound(GameCanvas):
    a = None     # public static aq a = null;     k.java:2
    b = -1       # requested sound                k.java:4
    a_ = -1      # current music                  k.java:6
    d = -1
    e = 0
    f = [0] * 17

    def __init__(self, paramMain):  # k.java:14-20
        super().__init__(paramMain)
        for b in range(17):
            Sound.f[b] = 0
        Sound.f[9] = 500
        Sound.a = PlayerPool(17, 1, True, True)

    def a__I(self, paramInt):  # k.java:22-33
        if Sound.a is None or not GameCanvas.df:
            return
        l = system.currentTimeMillis() - Sound.e
        if Sound.d != -1 and Sound.f[Sound.d] != 0 and l < Sound.f[Sound.d]:
            return
        if paramInt > 2 and paramInt != 15 and paramInt != 16 and paramInt != 3 and paramInt != 4:
            Sound.b_v()
        Sound.b = paramInt
        Sound.d = paramInt
        Sound.e = system.currentTimeMillis()

    def a_v(self):  # k.java:35-59  (called once per tick from ag.run)
        if Sound.a is None or not GameCanvas.df:
            return
        Sound.a.e_v()
        bool1 = False
        bool2 = True
        i = Sound.b
        Sound.b = -1
        if GameCanvas.df and i != -1:
            if i <= 2:
                if Sound.a_ == i:
                    bool2 = False
                else:
                    Sound.b_v()
                Sound.a_ = i
                bool1 = True
            else:
                Sound.a_ = -1
                bool1 = False
            if bool2:
                self.a_IZ(i, bool1)

    def a_IZ(self, paramInt, paramBoolean):  # k.java:61-73
        Sound.a.a_I(GameCanvas.dg)
        if GameCanvas.dg == 0:
            Sound.b_v()
            return
        if paramInt <= 2:
            Sound.a.a_TI("/snd" + str(paramInt) + ".mid", paramInt)
        else:
            Sound.a.a_TI("/snd" + str(paramInt) + ".wav", paramInt)
        Sound.a.a_IZ(paramInt, paramBoolean)

    @staticmethod
    def b_v():  # k.java:75-79
        Sound.b = -1
        Sound.a_ = -1
        Sound.a.b_v()
