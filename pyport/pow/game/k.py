"""k.java - sound manager (music snd0-2, SFX snd3-16). Literal port."""
from pow.game.ag import ag
from pow.midp import system


class k(ag):
    a = None     # public static aq a = null;     k.java:2
    b = -1       # requested sound                k.java:4
    a_ = -1      # current music                  k.java:6
    d = -1
    e = 0
    f = [0] * 17

    def __init__(self, paramMain):  # k.java:14-20
        from pow.game.aq import aq
        super().__init__(paramMain)
        for b in range(17):
            k.f[b] = 0
        k.f[9] = 500
        k.a = aq(17, 1, True, True)

    def a__I(self, paramInt):  # k.java:22-33
        if k.a is None or not ag.df:
            return
        l = system.currentTimeMillis() - k.e
        if k.d != -1 and k.f[k.d] != 0 and l < k.f[k.d]:
            return
        if paramInt > 2 and paramInt != 15 and paramInt != 16 and paramInt != 3 and paramInt != 4:
            k.b_v()
        k.b = paramInt
        k.d = paramInt
        k.e = system.currentTimeMillis()

    def a_v(self):  # k.java:35-59  (called once per tick from ag.run)
        if k.a is None or not ag.df:
            return
        k.a.e_v()
        bool1 = False
        bool2 = True
        i = k.b
        k.b = -1
        if ag.df and i != -1:
            if i <= 2:
                if k.a_ == i:
                    bool2 = False
                else:
                    k.b_v()
                k.a_ = i
                bool1 = True
            else:
                k.a_ = -1
                bool1 = False
            if bool2:
                self.a_IZ(i, bool1)

    def a_IZ(self, paramInt, paramBoolean):  # k.java:61-73
        k.a.a_I(ag.dg)
        if ag.dg == 0:
            k.b_v()
            return
        if paramInt <= 2:
            k.a.a_TI("/snd" + str(paramInt) + ".mid", paramInt)
        else:
            k.a.a_TI("/snd" + str(paramInt) + ".wav", paramInt)
        k.a.a_IZ(paramInt, paramBoolean)

    @staticmethod
    def b_v():  # k.java:75-79
        k.b = -1
        k.a_ = -1
        k.a.b_v()
