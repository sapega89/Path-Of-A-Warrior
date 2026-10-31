"""Stand-ins for classes that later phases port (NOT-PORTED). They only do what the
Phase 0 screens need from them: nothing, without crashing."""


class as_stub:  # as.java (Gamevil Live) - phase 7
    a = None
    gu = False

    def i(self):  # as.i(): network tick, called every frame from ag.run
        pass

    def g(self):
        from pow.game.ag import not_ported
        not_ported("as.g (Gamevil Live menu)")


class m_stub:  # m.java - phase 7
    pass


class ar_stub:  # ar.java - phase 3
    pass


class c_stub:  # c.java - phase 3/4
    pass
