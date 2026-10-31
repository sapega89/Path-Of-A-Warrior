"""Stand-ins for classes that later phases port (NOT-PORTED). They only do what the
Phase 0 screens need from them: nothing, without crashing."""


class as_stub:  # as.java (Gamevil Live) - phase 7
    a = None
    d = False   # static boolean d: set when a new game is created (l.java:144)
    gu = False

    def i(self):  # as.i(): network tick, called every frame from ag.run
        pass

    def g(self):
        from pow.game.ag import not_ported
        not_ported("as.g (Gamevil Live menu)")


class m_stub:  # m.java - phase 7
    pass


class ar_stub:  # ar.java - phase 3 (only ar.P, used by the generals' gifts e.o())
    def P_I(self, paramInt):  # ar.java:2055-2078  (random drop: item id, potion, or gold 10020/10040)
        from pow.game.ag import ag
        C = lambda n: ag.g_II(0, n)       # ag.C(int)
        arrayOfByte1 = [5, 10, 20, 5, 100]
        arrayOfByte2 = [10, 30, 60, 1, 100]
        arrayOfByte3 = [69, 44, 24, 9, 0]
        arrayOfByte = [[0, 0, 33, 77, 100], [5, 30, 55, 80, 100], [30, 60, 90, 100, 100],
                       [40, 80, 100, 100, 100], [80, 100, 100, 100, 100]]
        if C(100) < arrayOfByte1[paramInt]:
            i = C(100)
            if i < arrayOfByte2[paramInt]:
                for b in range(5):
                    if ag.cz.l > arrayOfByte3[b]:
                        i = C(100)
                        for b1 in range(5):
                            if i < arrayOfByte[b][b1]:
                                return 101 + b1 + 5 * C(20)
            else:
                return C(11) + 1
        elif C(100) < 25:
            return 10020 + (ag.ep ^ 0x1) * 20
        return 0


class c_stub:  # c.java - phase 3/4
    pass
