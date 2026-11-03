"""as.java - Gamevil Live of the single player (PHASE_7): its menus, the input and the
requests / answers. Literal port; the drawing is m.java (pow/game/m.py).

as is static state (every field is static in Java) plus an ag subclass instance (ag.be) whose
methods ag.run / ag.t / ag.L call. The server it talks to is pow_server/live.py, through
pow/game/v.py. Screens (ho, drawn by m.a()): 1 list, 2 Safe, 3 amount, 4 Backpack/Warehouse,
5 categories, 6 kinds, 7 enchant levels, 8 lots, 9 price, 10 Cancel, 11 Sale/Gift List,
12 waiting, 13 registration. Input handlers (hp): see t(int).

Fixes (config):
- DECOMP_FIX F20: as.a(ab) reads the status byte into a local and never sets gr, but m()
  waits for gr == 1 after the login 530 to send the request that needed it, and the error
  path passes gr as the error code: the status is gr (analysis/03 §5.1).
- ORIG_BUG B4: Buy with a full backpack asks "save it in Warehouse?" and then sends the item
  to the warehouse (ht[7] = 1), but 789 always puts it into the backpack: the search for a
  free slot runs past cz.Y[24] (ArrayIndexOutOfBounds in the network thread). Fixed: it goes
  into the warehouse list.
- ORIG_BUG B5: after CONFIRM on the password screen m.bp() counts frames (gE) and after 3 shows
  "Network connection has failed" and goes back to the UserID, even when the 531 has already
  answered (its popup is replaced) or is still on its way. Fixed: no count while the request
  is in flight (gu), and the 531 answer stops it.
"""
import config
from pow.game.ag import ag
from pow.game import heroes
from pow.game.structs import z
from pow.game.v import v
from pow.game.x import x
from pow.midp import system
from pow.midp.graphics import Image
from pow.midp.jint import i8, i16, idiv
from pow.midp.rms import RecordStore

F20 = config.DECOMP_FIX["F20"]
B4 = config.ORIG_BUG["B4"]
B5 = config.ORIG_BUG["B5"]


class as_(ag):
    a = None            # m (the drawing)
    b = None            # v (the network)
    d = True            # first Gamevil Live since the game started / a new game
    e = False           # waiting for an answer
    f = 0               # time of the request
    g = -1              # request to send on the next i()
    h = 0               # opcode of the last answer
    i = 0
    j = 0
    k = 0               # registration step: 1 UserID, 0 password
    l = ""              # password
    m = ""              # UserID
    n = False           # the 530 is a registration from the screen (popups 48 / 44)
    o = False
    p = None            # netLoading0.png
    q = None            # netLoading1.png
    r = None            # ui_arrow2.png
    s = None            # ui_level.png
    gn = system.currentTimeMillis() // 10000
    go = 0
    gp = 0              # request that waits for the login
    gq = 0              # request in flight
    gr = 0              # status of the last answer (F20)
    gs = False          # an answer (or an error) came
    gt = -1             # what the closing popup leads to (i())
    gu = False          # busy: "Connecting..." over the screen, keys ignored
    gv = None           # short[25] backpack serials
    gw = [None] * 100   # z[100] warehouse
    gx = None           # short[100] warehouse serials
    gy = 0              # gold in the Safe
    gz = [None] * 20    # z[20] lots of the page / Sale List / Gift List / my lots
    gA = [0] * 20       # lot ids
    gB = [0] * 20       # prices
    gC = [""] * 5       # Gift List: from whom
    gD = 0              # 0 Sale List, 1 Gift List
    gE = False
    gF = [[116, 121, 126, 101, 106, 111, 131, 136, 156, 161, 181, 146, 151, 0, 0, 0, 0, 0, 0, 0],
          [331, 324, 322, 301, 308, 302, 341, 350, 357, 363, 370, 380, 415, 0, 0, 0, 0, 0, 0, 0],
          [501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 0, 0]]
    gG = [3, 4, 5, 9, 10, 11, 12, 13, 6, 7, 8, 14, 15, 16, 17, 18, 19, 20, 21]
    gH = False          # inside a(ab)
    gI = [None] * 8     # list menu items
    gJ = 0              # list: count
    gK = 0              # list: visible rows / a slot count
    gL = 0              # list: cursor
    gM = 0              # list: first visible
    gN = 0              # list: y
    gO = 0
    gP = 0              # category 0 Normal 1 Special 2 Rare
    gQ = 0              # kind
    gR = 0              # enchant level
    gS = 0              # page
    gT = 0              # page step
    gU = gV = gW = gX = gY = gZ = 0
    ha = hb = hc = hd = he = hf = hg = hh = 0
    hi = 0              # item id shown
    hj = 0              # serial of the selected item
    hk = 0              # selected slot of a 5-slot list
    hl = [None] * 12    # gamestr 2..13 titles
    hm = [None] * 50    # gamestr 15..64
    hn = ""             # title
    ho = 0              # screen
    hp = 0              # input handler
    hq = False          # redraw
    hr = 0
    hs = 0
    ht = [0] * 16
    hu = [0] * 16
    hv = [0] * 16
    hw = ["Normal Items", "Special Items", "Rare Items"]

    def __init__(self):  # as.java:172-178
        super().__init__(ag.bs)
        if as_.gv is None:
            as_.gv = [0] * 25
        if as_.gx is None:
            as_.gx = [0] * 100

    def g_v(self):  # as.java:180-190  (Game Menu > Gamevil Live)
        from pow.game.m import m
        as_.o = True
        if m.b_v():
            as_.n = False
            as_.a.d_v()
            ag.cS.d_I(2)
            as_.gt = 2
            return
        self.h_v()

    def h_v(self):  # as.java:192-208  (registration screen)
        from pow.game.at import at
        ag.bp = True
        ag.ai()
        as_.hn = "Registration"
        as_.ho = 13
        as_.hp = 18
        as_.k = 1
        ag.bP = 0
        as_.aJ()
        ag.bV = 11
        as_.l = ""
        as_.m = ""
        ag.bz = None
        ag.bz = at("", 12, 10)
        self.k_v()
        as_.aJ()

    def i_v(self):  # as.java:210-299  (every frame from ag.run)
        if as_.b is not None:
            as_.b.pump()
        if as_.g != -1:
            self.d_I(as_.g)
        if ag.cS.q:
            ag.cS.q = False
            i = as_.gt
            as_.gt = -1
            s1 = ag.cS.k
            if i == 3:
                self.ba_v()
                as_.aJ()
            elif i == 2:
                if s1 == 0:
                    ag.bp = True
                    ag.ai()
                    self.k_v()
                    self.aE_v()
                    self.aI_v()
                    self.c_I(512)
                else:
                    self.ba_v()
                    as_.aJ()
            elif i == 7:
                if as_.ht[15] > 0:
                    self.c_I(516)
                else:
                    self.aS_v()
            elif i == 8:
                self.aX_v()
            elif i == 9:
                if s1 == 0:
                    bool_ = False
                    if as_.ht[14] == 1:
                        for b in range(9):
                            if ag.cz.X[b].a > 0:
                                bool_ = True
                                break
                        if bool_:
                            ag.cS.d_I(33)
                            return self._i_end()
                    as_.hr = 0
                    if as_.ht[14] == 0:
                        self.c_I(256)
                    else:
                        self.c_I(262)
            elif i == 10:
                if s1 == 0:
                    if ag.fK[16] < 25:
                        as_.ht[7] = 0
                        as_.hr = 0
                        self.c_I(788)
                    else:
                        ag.cS.d_I(12)
                        as_.gt = 11
            elif i == 11:
                if s1 == 0:
                    as_.ht[7] = 1
                    as_.hr = 0
                    self.c_I(788)
            elif i == 14:
                if s1 == 0:
                    as_.hr = 0
                    self.c_I(866)
                    as_.hq = True
        self._i_end()

    def _i_end(self):
        if as_.e:
            self.m_v()

    @staticmethod
    def b_I(paramInt):  # as.java:301-353  (error code -> gamestr popup)
        b = {-1: 21, -2: 22, -4: 23, -12: 24, -13: 25, -15: 26, -16: 27, -18: 28, -20: 29,
             -22: 30, -23: 31, -26: 7, -49: 54}.get(paramInt, -1)
        if paramInt == -26:
            as_.gt = 3
        elif paramInt == -11:
            b = 10 if as_.gS > 0 else 8
        if b != -1:
            ag.cS.d_I(b)

    def j_v(self):  # as.java:355-364  ("Connecting..." over the screen)
        ag.cS.b_I(96)
        i = ag.de - 20 - 10
        j = as_.p.getWidth()
        k = as_.p.getHeight()
        ag.a_IIIIMII((ag.bJ - j) // 2, i, j, k, as_.p, 0, 0)
        ag.a_IIIIMII((ag.bJ - j) // 2, i, j * (ag.bN % 6) // 5, k, as_.q, 0, 0)
        x.a_Lg(ag.bu)
        x.a_TIII("Connecting...", ag.bJ // 2, i + 50, 1)

    def k_v(self):  # as.java:366-378
        try:
            if as_.p is None:
                as_.p = Image.createImage("/netLoading0.png")
            if as_.q is None:
                as_.q = Image.createImage("/netLoading1.png")
            if as_.r is None:
                as_.r = Image.createImage("/ui_arrow2.png")
            if as_.s is None:
                as_.s = Image.createImage("/ui_level.png")
        except Exception:
            pass
        as_.l_v()

    @staticmethod
    def l_v():  # as.java:380-386
        if as_.b is None:
            as_.b = v()
            as_.b.setPriority(5)
            as_.b.start()

    def f_v(self):  # as.java:388-390  (s.f(): connected)
        self.n_v()

    def c_I(self, paramInt):  # as.java:392-397  (ask for a request on the next i())
        as_.gr = 0
        ag.v_v()
        as_.gu = True
        as_.g = paramInt

    def d_I(self, paramInt):  # as.java:399-413
        as_.g = -1
        as_.gp = 0
        if not v.h:
            as_.gp = paramInt
            as_.gq = 530
        else:
            as_.gq = paramInt
        as_.f = system.currentTimeMillis()
        as_.e = False
        self.e_I(as_.gq)
        as_.aJ()
        as_.e = True

    def m_v(self):  # as.java:415-438  (answer came / timeout)
        if as_.gs:
            if not as_.gH:
                ag.w_v()
                as_.e = False
                as_.gu = False
                as_.aJ()
        elif v.m and not as_.gH and (ag.ch == -7 or system.currentTimeMillis() > as_.f + 30000):
            as_.gr = -1
            if as_.b is not None:
                as_.b.a_v()
                as_.bi_v()
                ag.R_v()
            as_.gu = False
            self.a_IILab(as_.gq + 1, as_.gr, None)
            as_.aJ()
        if as_.gr == 1 and as_.gq == 530 and as_.gp != 530:
            as_.gq = as_.gp
            self.c_I(as_.gq)

    def e_I(self, paramInt):  # as.java:440-451
        as_.gq = paramInt
        if not v.h:
            if as_.b is None:
                as_.l_v()
            v.a_Ls(self)
            as_.b.a_TI(ag.bk, ag.bl)
        else:
            self.n_v()
        as_.gs = False

    def n_v(self):  # as.java:453-576  (write the request gq)
        cz = ag.cz
        as_.gr = 0
        as_.b.a_I(as_.gq)
        q = as_.gq
        if q == 530:
            v.b_TI(as_.m, 12)
            v.b_TI(as_.l, 16)
            v.b_TI("1501", 4)
            v.b_I(as_.gn)
            as_.go = system.currentTimeMillis() // 10000
            v.b_I(as_.go)
        elif q in (516, 256):
            v.b_I(cz.F)
            v.b_I(cz.G)
            v.a_S(cz.l)
            v.a_B(cz.aB)
            v.a_B(ag.g_I(cz.X[0].a) ^ 0x1)
            v.a_S(cz.m)
            v.a_S(cz.n)
            v.a_S(cz.o)
            v.a_S(cz.q)
            v.a_S(cz.J)
            ag.O_v()
            v.a_S(cz.s)
            v.a_S(cz.t)
            v.a_S(cz.u)
            v.a_S(cz.v)
            for b1 in range(8):
                v.b_I(ag.dy[b1])
            b = 0
            for b2 in range(len(cz.W)):
                if cz.W[b2] > 0:
                    b += 1
            v.a_B(b)
            for b3 in range(len(cz.W)):
                if cz.W[b3] > 0:
                    v.a_B(as_.gG[b3])
                    v.a_B(cz.W[b3])
                    bool_ = False
                    for b8 in range(4):
                        if cz.V[b8] - 12 == b3:
                            bool_ = True
                            break
                    v.a_Z(bool_)
            v.b_TI(cz.k, 8)
            v.a_Z(not (cz.S == 0))
            v.a_B(ag.fo & 0xFF)
            for b4 in range(ag.fo):
                v.a_B(ag.fn[0][b4] & 0xFF)
                v.a_B(ag.fn[1][b4] & 0xFF)
            v.b_I(ag.dw & 0xFFFFFFFF)
            v.b_I(ag.dw >> 32 & 0xFFFFFFFF)
            v.a_B(ag.cq)
            for b5 in range(22):
                v.a_B(cz.g[b5] & 0xFF)
            v.a_B(cz.h & 0xFF)
            v.a_B(cz.i & 0xFF)
            v.b_I(ag.ed)
        elif q == 768:
            from pow.game.e import e
            v.b_I(cz.E)
            e.m_v()
            b6 = i8(ag.fK[16])
            v.a_B(b6)
            for b7 in range(25):
                if cz.Y[b7].a > 0:
                    v.a_S(cz.Y[b7].a)
                    as_.gv[b7] = i16(b7 + 1)
                    v.a_S(as_.gv[b7])
                    v.a_B(cz.Y[b7].f)
                    v.a_S(cz.Y[b7].b)
                    v.a_S(cz.Y[b7].c)
                    v.a_S(cz.Y[b7].d)
                    v.a_S(cz.Y[b7].e)
        elif q == 832:
            v.a_B(as_.ht[15] ^ 0x1)
            v.b_I(as_.hv[14])
        elif q == 816:
            v.a_B(as_.ht[7])
            v.a_S(as_.hj)
        elif q in (784, 786, 788, 800):     # case 784 / 786 / 788 / 800 fall through
            if q == 784:
                v.a_B(as_.gP + 1)
            if q in (784, 786):
                v.a_B(as_.gP + 1)
                v.a_B(as_.gQ + 1)
                v.a_B(as_.gR)
            if q in (784, 786, 788):
                v.b_I(as_.gA[ag.fK[18]])
            v.a_B(as_.ht[7])
            v.a_S(as_.hj)
            v.b_I(as_.hv[14])
        elif q in (802, 866):               # case 802 falls through into 866
            if q == 802:
                v.a_B(as_.gP + 1)
                v.a_B(as_.gQ + 1)
            v.b_I(as_.gA[as_.hk])
            v.a_B(0 if ag.fK[16] < 25 else 1)
        as_.b.b_v()

    def o_v(self):  # as.java:578-591
        v.h = False
        if as_.b is not None:
            as_.b.a_v()
            as_.bi_v()
        if ag.bV == 11:
            as_.gt = 3
            ag.cS.d_I(29)
        as_.gu = False
        as_.e = False
        ag.f_I(300)

    def e_v(self):  # as.java:593-599  (s.e(): the connection failed / broke)
        if as_.b is not None:
            as_.b.a_v()
            as_.bi_v()
        as_.gs = True

    @staticmethod
    def _copy(dst, src):
        dst.a, dst.b, dst.c, dst.d, dst.e, dst.f = src.a, src.b, src.c, src.d, src.e, src.f

    def a_Lab(self, paramab):  # as.java:601-990  (s.a(ab): one answer)
        cz = ag.cz
        fK = ag.fK
        as_.gH = True
        v.m = False
        s1 = paramab.b_v()
        b = paramab.a_v()
        if F20:
            as_.gr = b                      # DECOMP_FIX F20
        as_.h = s1
        if B5 and s1 == 531:
            as_.gE = False                  # ORIG-BUG B5
        if b == 1:
            if s1 == 531:
                as_.gn = as_.go
                self.ar()
                paramab.a_v()
                paramab.a_v()
                b6 = paramab.a_v()
                if (b6 == 0 or b6 == 2) and as_.n:
                    from pow.game.m import m
                    m.c_v()
                    if b6 == 0:
                        ag.cS.d_I(48)
                    elif b6 == 2:
                        ag.cS.d_I(44)
                    as_.gt = 2
                    as_.n = False
            elif s1 == 513:
                as_.ht[15] = paramab.a_v()
                as_.ht[14] = paramab.a_v()
                as_.ht[13] = paramab.a_v()
                paramab.a_v()
                for _ in range(5):
                    paramab.c_v()
                as_.ht[4] = paramab.a_v()
                as_.ht[5] = paramab.a_v()
                self.aR_v()
                as_.aJ()
            elif s1 == 517:
                ag.cS.m = ag.e_T(ag.f_T(paramab.a_I(16)))
                ag.cS.n = ag.e_T(ag.f_T(paramab.a_I(16)))
                ag.cS.o = ag.e_T(ag.f_T(paramab.a_I(16)))
                ag.cS.p = ag.e_T(ag.f_T(paramab.a_I(16)))
                ag.cS.d_I(53)
                as_.gt = 7
                if paramab.a_v() == 1:
                    as_.ht[15] = i16(as_.ht[15] + 1)
                else:
                    as_.ht[15] = 0
            elif s1 == 519:
                for b1 in range(20):
                    if as_.gz[b1] is None:
                        as_.gz[b1] = z()
                    z.a(as_.gz[b1])
                    as_.gB[b1] = 0
                b5 = paramab.a_v()
                for b1 in range(b5):
                    as_.gz[b1].a = paramab.b_v()
                    as_.gz[b1].f = paramab.a_v()
                    as_.gB[b1] = paramab.c_v()
                as_.gD = 0
                self.aT_v()
            elif s1 == 261:
                ag.fR = i16(ag.fR - 1)
                if ag.fR == 0:
                    self.ar()
                    if as_.hv[15] == 0 and as_.hv[14] == 0:
                        if as_.d:
                            ag.cS.d_I(20)
                        else:
                            ag.cS.q = True
                    else:
                        ag.cS.m = str(as_.hv[14])
                        ag.cS.n = str(as_.hv[15])
                        ag.cS.o = str(as_.hv[13])
                        ag.cS.d_I(41)
                    as_.gt = 8
                else:
                    ag.fR = 0
                    self.aV_v()
            elif s1 == 263:
                cz.F = paramab.c_v()
                cz.G = paramab.c_v()
                cz.l = paramab.b_v() & 0xFF
                cz.aB = paramab.a_v()
                if not 0 <= cz.aB < heroes.HERO_COUNT:   # PORT-EXTRA: 10 heroes, a broken byte -> hero 1
                    cz.aB = 0
                cz.K = paramab.a_v()
                cz.m = paramab.b_v()
                cz.n = paramab.b_v()
                cz.o = paramab.b_v()
                cz.q = paramab.b_v()
                cz.J = paramab.b_v()
                for b1 in range(len(cz.W)):
                    cz.W[b1] = 0
                for b1 in range(len(cz.V)):
                    cz.V[b1] = 0
                b4 = paramab.a_v()
                b1 = 0
                b2 = 0
                while b1 < b4:
                    b8 = paramab.a_v()
                    b7 = 0
                    while b7 < 19 and as_.gG[b7] != b8:
                        b7 += 1
                    cz.W[b7] = paramab.a_v()
                    b8 = paramab.a_v()
                    if b8 == 1:
                        cz.V[b2] = b7 + 12
                        b2 += 1
                    b1 += 1
                for b1 in range(8):
                    ag.dy[b1] = paramab.c_v()
                cz.k = ag.g_T(ag.f_T(paramab.a_I(8)))
                cz.S = paramab.a_v()
                for b1 in range(45):
                    ag.fn[0][b1] = 0
                    ag.fn[1][b1] = 0
                ag.fo = i16(paramab.a_v())
                for b1 in range(ag.fo):
                    ag.fn[0][b1] = i16(paramab.a_v())
                    ag.fn[1][b1] = i16(paramab.a_v())
                i = paramab.c_v()
                ag.dw = paramab.c_v()
                ag.dw <<= 32
                ag.dw |= i                  # sic: a negative low word fills the high one (Java long |)
                ag.cq = paramab.a_v()
                for b1 in range(22):
                    cz.g[b1] = i16(paramab.a_v())
                cz.h = i16(paramab.a_v())
                cz.i = i16(paramab.a_v())
                ag.ed = paramab.c_v()
                self.ar()
                ag.cS.d_I(19)
            elif s1 == 257:
                ag.cS.d_I(18)
            elif s1 == 769:
                as_.gy = paramab.c_v()
                for b1 in range(100):
                    if as_.gw[b1] is None:
                        as_.gw[b1] = z()
                    z.a(as_.gw[b1])
                as_.ht[6] = i16(paramab.a_v() & 0xFF)
                for b1 in range(len(as_.gw)):
                    z.a(as_.gw[b1])
                for b1 in range(as_.ht[6]):
                    as_.gw[b1].a = paramab.b_v()
                    as_.gx[b1] = paramab.b_v()
                    as_.gw[b1].f = paramab.a_v()
                    as_.gw[b1].b = paramab.b_v()
                    as_.gw[b1].c = paramab.b_v()
                    as_.gw[b1].d = paramab.b_v()
                    as_.gw[b1].e = paramab.b_v()
                self.aH_v()
            elif s1 == 833:
                cz.E = paramab.c_v()
                as_.gy = paramab.c_v()
            elif s1 == 817:
                if as_.ht[7] == 0:
                    as_.gK = 100
                    fK[16] = fK[16] - 1
                    as_.ht[6] = i16(as_.ht[6] + 1)
                    b1 = 0
                    while b1 < as_.gK and as_.gw[b1].a != 0:
                        b1 += 1
                    as_._copy(as_.gw[b1], cz.Y[fK[18]])
                    z.a(cz.Y[fK[18]])
                    as_.gx[b1] = paramab.b_v()
                    as_.gv[fK[18]] = 0
                else:
                    as_.gK = 25
                    as_.ht[6] = i16(as_.ht[6] - 1)
                    fK[16] = fK[16] + 1
                    b1 = 0
                    while b1 < as_.gK and cz.Y[b1].a != 0:
                        b1 += 1
                    as_._copy(cz.Y[b1], as_.gw[fK[18]])
                    z.a(as_.gw[fK[18]])
                    as_.gv[b1] = paramab.b_v()
                    as_.gx[fK[18]] = 0
                self.O_I(0)
                as_.aJ()
            elif s1 == 785:
                b1 = 0
                b3 = 15
                while b1 < 10:
                    as_.hu[b3] = paramab.a_v()
                    b1 += 1
                    b3 -= 1
                self.aM_v()
            elif s1 == 521:
                for b1 in range(5):
                    if as_.gz[b1] is None:
                        as_.gz[b1] = z()
                    z.a(as_.gz[b1])
                    as_.gC[b1] = ""
                b5 = paramab.a_v()
                for b1 in range(b5):
                    as_.gC[b1] = ag.f_T(paramab.a_I(8))
                    as_.gz[b1].a = paramab.b_v()
                    as_.gz[b1].f = paramab.a_v()
                    as_.gz[b1].b = paramab.b_v()
                    as_.gz[b1].c = paramab.b_v()
                    as_.gz[b1].d = paramab.b_v()
                    as_.gz[b1].e = paramab.b_v()
                as_.ht[13] = paramab.a_v()
                as_.gD = 1
                self.aT_v()
            elif s1 == 787:
                for b1 in range(20):
                    if as_.gz[b1] is None:
                        as_.gz[b1] = z()
                    z.a(as_.gz[b1])
                    as_.gA[b1] = 0
                    as_.gB[b1] = 0
                b4 = paramab.a_v()
                for b1 in range(b4):
                    as_.gA[b1] = paramab.c_v()
                    as_.gz[b1].a = paramab.b_v()
                    as_.gB[b1] = paramab.c_v()
                    as_.gz[b1].f = paramab.a_v()
                    as_.gz[b1].b = paramab.b_v()
                    as_.gz[b1].c = paramab.b_v()
                    as_.gz[b1].d = paramab.b_v()
                    as_.gz[b1].e = paramab.b_v()
                as_.gS = i8(as_.gS + as_.gT)
                self.aN_v()
            elif s1 == 789:
                if B4 and as_.ht[7] == 1:     # ORIG-BUG B4: bought into the warehouse
                    as_.ht[6] = i16(as_.ht[6] + 1)
                    b1 = 0
                    while b1 < 100 and as_.gw[b1].a != 0:
                        b1 += 1
                    as_._copy(as_.gw[b1], as_.gz[fK[18]])
                    as_.p_v()
                    as_.gx[b1] = paramab.b_v()
                else:
                    as_.gK = 25
                    fK[16] = fK[16] + 1
                    b1 = 0
                    while b1 < as_.gK and cz.Y[b1].a != 0:
                        b1 += 1
                    as_._copy(cz.Y[b1], as_.gz[fK[18]])
                    as_.p_v()
                    as_.gv[b1] = paramab.b_v()
                cz.E = paramab.c_v()
                as_.gy = paramab.c_v()
                self.O_I(0)
                ag.cS.d_I(35)
            elif s1 == 801:
                if as_.ht[7] == 0:
                    z.a(cz.Y[as_.hk])
                    as_.gv[as_.hk] = 0
                    fK[16] = fK[16] - 1
                else:
                    z.a(as_.gw[as_.hk])
                    as_.gx[as_.hk] = 0
                    as_.ht[6] = i16(as_.ht[6] - 1)
                self.O_I(0)
                ag.cS.d_I(36)
                self.aP_v()
            elif s1 in (803, 865):
                for b1 in range(20):
                    if as_.gz[b1] is None:
                        as_.gz[b1] = z()
                    z.a(as_.gz[b1])
                    as_.gA[b1] = 0
                    as_.gB[b1] = 0
                b4 = paramab.a_v()
                if b4 > 20:
                    b4 = 20
                for b1 in range(b4):
                    if s1 == 865:
                        as_.gA[b1] = paramab.c_v()
                    as_.gz[b1].a = paramab.b_v()
                    as_.gB[b1] = paramab.c_v()
                    as_.gz[b1].f = paramab.a_v()
                    as_.gz[b1].b = paramab.b_v()
                    as_.gz[b1].c = paramab.b_v()
                    as_.gz[b1].d = paramab.b_v()
                    as_.gz[b1].e = paramab.b_v()
                if s1 == 803:
                    self.aO_v()
                    as_.ho = 8
                    as_.hp = 10
                    as_.hn = as_.hl[6]
                    as_.aJ()
                else:
                    self.d_Z(False)
            elif s1 == 867:
                if as_.ht[7] == 0:
                    as_.gK = 25
                    as_.ht[6] = i16(as_.ht[6] - 1)
                    fK[16] = fK[16] + 1
                    b1 = 0
                    while b1 < as_.gK and cz.Y[b1].a != 0:
                        b1 += 1
                    as_._copy(cz.Y[b1], as_.gz[as_.hk])
                    z.a(as_.gz[as_.hk])
                    as_.p_v()
                    as_.gv[b1] = paramab.b_v()
                else:
                    as_.gK = 100
                    fK[16] = fK[16] - 1
                    as_.ht[6] = i16(as_.ht[6] + 1)
                    b1 = 0
                    while b1 < as_.gK and as_.gw[b1].a != 0:
                        b1 += 1
                    as_._copy(as_.gw[b1], as_.gz[as_.hk])
                    z.a(as_.gz[as_.hk])
                    as_.p_v()
                    as_.gx[b1] = paramab.b_v()
                self.O_I(0)
                ag.cS.d_I(40)
            elif s1 == 259:
                as_.hv[15] = paramab.c_v()
                as_.hv[14] = paramab.c_v()
                as_.hv[13] = ag.H_I(as_.hv[14])
                cz.F += as_.hv[15]
                ag.fR = 1
                self.ar()
                self.aW_v()
        else:
            self.a_IILab(as_.h, as_.gr if F20 else 0, paramab)
        as_.gH = False
        v.m = True
        as_.gs = True

    def a_IILab(self, paramInt1, paramInt2, paramab):  # as.java:992-1056  (error answers)
        if paramInt1 == 531:
            if paramab is None:
                as_.b_I(paramInt2)
                as_.gt = 3
                return
            paramab.a_v()
            paramab.a_v()
            b = paramab.a_v()
            if b == 1:
                ag.cS.d_I(43)
                return
            if b == 3 and paramInt2 != -49:
                ag.cS.d_I(47)
                return
            as_.b_I(paramInt2)
            as_.gt = 3
            return
        if paramInt1 == 513:
            as_.b_I(paramInt2)
            as_.gt = 3
            return
        if paramInt1 == 517:
            self.aS_v()
            return
        if paramInt1 == 519:
            self.aU_v()
            return
        if paramInt1 == 521:
            self.aV_v()
            return
        if paramInt1 in (259, 261):
            self.aX_v()
            return
        if paramInt1 == 769:
            as_.b_I(paramInt2)
            as_.gt = 3
            return
        if paramInt1 == 789:
            as_.b_I(paramInt2)
            return
        if paramInt1 == 867 and paramInt2 == -12:
            as_.p_v()
        if paramInt1 in (867, 801, 817, 833, 849):
            self.O_I(0)
        as_.b_I(paramInt2)

    @staticmethod
    def p_v():  # as.java:1058-1062
        z.a(as_.gz[as_.hk])
        as_.gB[as_.hk] = 0
        as_.gA[as_.hk] = 0

    def O_I(self, paramInt):  # as.java:1064-1067  (save the game)
        ag.fS = i16(paramInt)
        self.ar()

    @staticmethod
    def aB_v():  # as.java:1069-1071
        return 32 * as_.gK - 12

    @staticmethod
    def e_TII(paramString, paramInt1, paramInt2):  # as.java:1073-1092  ("a|b|c|" -> list menu)
        i = 0
        j = 0
        for b in range(len(paramString)):
            if paramString[b] == '|':
                as_.gI[i] = paramString[j:b]
                j = b + 1
                i += 1
        if i == 0:
            return
        as_.gJ = i16(i)
        i = idiv(paramInt2 + 12, 32)
        as_.gK = i16(i)
        if as_.gK > as_.gJ:
            as_.gK = as_.gJ
        as_.gN = i16(paramInt1 + (paramInt2 - 32 * as_.gK - 12 >> 1))
        as_.gM = as_.gL = 0

    def P_I(self, paramInt):  # as.java:1094-1109  (list keys: -2 moved, index chosen, -1)
        i = -1
        if paramInt in (-1, -2, 50, 56):
            if paramInt in (-1, 50):
                as_.gL -= 1
                if as_.gL < 0:
                    as_.gL = i16(as_.gJ - 1)
            else:
                as_.gL += 1
                if as_.gL >= as_.gJ:
                    as_.gL = 0
            as_.aC_v()
            i = -2
        elif paramInt in (-5, 53):
            i = as_.gL
        return i

    @staticmethod
    def aC_v():  # as.java:1111-1118
        if as_.gM > as_.gL:
            as_.gM = as_.gL
            return
        if as_.gL - as_.gM >= as_.gK:
            as_.gM = as_.gL - as_.gK + 1

    def aD_v(self):  # as.java:1120-1135  (draw the list menu)
        i = as_.gN
        b = 0
        j = as_.gM
        while b < as_.gK:
            if j == as_.gL:
                ag.a_IIIIIIIZ(45, i, 150, 20, ag.k_III(0, 0, 0), ag.k_III(255, 255, 255), ag.k_III(0, 0, 0), True)
                x.a_Lg(ag.bw)
            else:
                ag.a_IIIIIIIZ(46, i + 1, 148, 18, ag.k_III(0, 0, 0), ag.k_III(80, 80, 80), ag.k_III(0, 0, 0), True)
                x.a_Lg(ag.bu)
            ag.b_IIT(120, i + 1, as_.gI[j])
            i += 32
            b += 1
            j += 1

    def aE_v(self):  # as.java:1137-1143
        self.aF_v()
        self.aG_v()
        ag.az()
        ag.bV = 11
        as_.gO = ag.bY.a

    def aF_v(self):  # as.java:1145-1149
        for b in range(12):
            as_.hl[b] = ag.M_I(2 + b)
        return True

    def aG_v(self):  # as.java:1151-1155
        for b in range(50):
            as_.hm[b] = ag.M_I(15 + b)
        return True

    def aH_v(self):  # as.java:1157-1176  (GAMEVIL LIVE menu)
        as_.e_TII("Trade|Warehouse|Safe|Management|", 20, 255)
        as_.gL = as_.gU
        as_.gM = as_.gV
        as_.aC_v()
        as_.hp = 2
        as_.ho = 1
        as_.hn = as_.hl[2]
        as_.hr = 0
        as_.hs = 10
        if as_.o and as_.d:
            as_.o = False
            ag.cS.m = as_.l
            ag.cS.n = as_.m
            ag.cS.d_I(49)
        as_.aJ()
        as_.d = False

    def aI_v(self):  # as.java:1178-1184  (waiting screen)
        as_.hp = 17
        as_.ho = 12
        as_.hn = as_.hl[2]
        as_.j = 0
        as_.aJ()

    @staticmethod
    def aJ():  # as.java:1186-1188
        as_.hq = True

    @staticmethod
    def a_IIIZ(paramInt1, paramInt2, paramInt3, paramBoolean):  # as.java:1190-1194  (item cell)
        ag.bb.a_IIZ(paramInt2, paramInt3, paramBoolean)
        if paramInt1 > 0:
            ag.bb.a_IIII(paramInt1, paramInt2, paramInt3, 0)

    @staticmethod
    def a_TIII(paramString, paramInt1, paramInt2, paramInt3):  # as.java:1196-1198
        x.a_TIII(paramString, paramInt1 + idiv(paramInt3, 2), paramInt2, 1)

    @staticmethod
    def aK():  # as.java:1200-1202
        as_.a.a_v()

    def c_TI(self, paramString, paramInt):  # as.java:1204-1209  (caption box)
        x.a_Lg(ag.bu)
        self.b_III(paramInt, 200, 22)
        if paramString != "":
            self.b_TII(paramString, paramInt + 1 - ag.dc, 0)

    def t_I(self, paramInt):  # as.java:1211-1269  (keys)
        i = paramInt
        if ag.cS.b != 0:
            ag.cS.b_v()
            ag.ch = -999
            as_.aJ()
            return
        ag.ch = -999
        h = {1: self.R_I, 2: self.ae_I, 3: self.aa_I, 4: self.Z_I, 5: self.W_I, 6: self.X_I, 7: self.Y_I,
             8: self.U_I, 9: self.V_I, 10: self.T_I, 13: self.S_I, 14: self.ab_I, 15: self.ad_I,
             16: self.af_I, 18: self.Q_I}.get(as_.hp)
        if h is not None:
            h(i)

    def Q_I(self, paramInt):  # as.java:1271-1328  (registration: UserID, then password)
        if as_.k == 0:
            i = len(as_.l)
            if paramInt == -7:
                if i > 0:
                    as_.l = as_.l[:i - 1]
                else:
                    as_.k = 1
                    as_.aJ()
                if i == 10:
                    as_.aJ()
                    return
            elif paramInt == -6:
                if i >= 4:
                    as_.gE = True
                    as_.n = True
                    self.c_I(530)
                    return
            else:
                j = ag.N_I(paramInt)
                if j != -1 and i < 12:
                    as_.l += str(j)
                return
        elif as_.k == 1:
            if len(ag.bz.a_v()) == 0 and paramInt == -7:
                self.ba_v()
                return
            i = ag.r_I(paramInt)
            if i == -7:
                ag.bz.a_I(-8)
                return
            if i == -5 or i == 53:
                if ag.bP == 26 and len(ag.bz.a_v()) >= 4:
                    if len(ag.bz.a_v()) != 0:
                        as_.m = ag.bz.a_v()
                        ag.bz.a_T(as_.m)
                        as_.k = 0
                        as_.aJ()
                        return
                else:
                    ag.bz.a_I(65 + ag.bP)
                    return
            elif i == -6 and len(ag.bz.a_v()) >= 4 and len(ag.bz.a_v()) != 0:
                as_.m = ag.bz.a_v()
                ag.bz.a_T(as_.m)
                as_.k = 0
                as_.aJ()

    def R_I(self, paramInt):  # as.java:1330-1357  (Sale / Gift List)
        if paramInt == -3:
            as_.hk = as_.hk - 1 if as_.hk > 0 else 4
            as_.aJ()
        elif paramInt == -4:
            as_.hk = as_.hk + 1 if as_.hk < 4 else 0
            as_.aJ()
        elif paramInt in (-8, -5):
            if as_.gD == 0:
                self.aU_v()
            else:
                self.aV_v()

    def S_I(self, paramInt):  # as.java:1359-1394  (Cancel Sell: my 5 lots)
        from pow.game.e import e
        if paramInt == -7:
            self.bf_v()
        elif paramInt in (-5, 53):
            if as_.gz[as_.hk].a > 0:
                as_.hi = as_.gz[as_.hk].a
                as_.ht[7] = 0 if ag.fK[16] < 25 else 1
                ag.cS.m = e.c_I(as_.gz[as_.hk].a)
                ag.cS.d_I(39)
                as_.gt = 14
        elif paramInt in (-3, 52):
            as_.hk = as_.hk - 1 if as_.hk > 0 else 4
            as_.aJ()
        elif paramInt in (-4, 54):
            as_.hk = as_.hk + 1 if as_.hk < 4 else 0
            as_.aJ()

    def T_I(self, paramInt):  # as.java:1396-1403  (Price Info list)
        if paramInt == -7:
            self.aQ_v()
            return
        self.a_IZ(paramInt, False)

    def U_I(self, paramInt):  # as.java:1405-1440  (Sell: pick an item)
        if paramInt == -7:
            self.bf_v()
            return
        if paramInt in (-5, 53):
            z1 = as_.be_v()
            if z1.a > 0:
                if 434 <= z1.a <= 437:
                    ag.cS.d_I(13)
                    return
                as_.hi = z1.a
                as_.gR = i16(z1.f)
                as_.hk = ag.fK[18]
                if z1.a > 500:
                    as_.gP = 2
                    as_.gQ = i16(z1.a - 501)
                elif z1.a > 300:
                    as_.gP = 1
                    as_.gQ = i16(ag.bH[1].a_II(z1.a - 301, 7))
                else:
                    as_.gP = 0
                    as_.gQ = i16(ag.bH[0].a_II(z1.a - 101, 7))
                as_.hv[13] = 0
                as_.hv[14] = 0
                as_.e_Z(True)
                self.aQ_v()
            return
        self.ac_I(paramInt)

    def V_I(self, paramInt):  # as.java:1442-1489  (Sell: the price)
        bool_ = True
        if 48 <= paramInt <= 57:
            i = ag.N_I(paramInt)
            if 0 <= i <= 9 and as_.hv[13] < 9:
                as_.hv[14] = as_.hv[14] * 10
                as_.hv[14] = as_.hv[14] + i
                if as_.hv[14] > 0:
                    as_.hv[13] = as_.hv[13] + 1
        elif paramInt == -7:
            if as_.hv[13] > 0:
                as_.hv[14] = idiv(as_.hv[14], 10)
                as_.hv[13] = as_.hv[13] - 1
            else:
                self.aP_v()
        elif paramInt == -5:
            if as_.hv[14] > 0:
                self.c_I(800)
                as_.hr = 0
            else:
                bool_ = False
        elif paramInt == -6:
            self.c_I(802)
            as_.hr = 0
        else:
            bool_ = False
        if bool_:
            as_.aJ()

    def W_I(self, paramInt):  # as.java:1491-1518  (Buy: kind)
        if paramInt == -7:
            self.aY_v()
            return
        if paramInt in (-5, 53):
            if as_.gF[as_.gP][ag.fK[18]] != 0:
                as_.e_Z(False)
                as_.hi = as_.gF[as_.gP][ag.fK[18]]
                as_.gQ = i16(ag.fK[18])
                if as_.gP == 2:
                    as_.gR = 0
                    as_.gS = 0
                    as_.gT = 1
                    self.c_I(786)
                else:
                    as_.gR = 0
                    self.c_I(784)
                as_.hr = 0
                as_.aJ()
            return
        self.a_IZ(paramInt, False)

    def X_I(self, paramInt):  # as.java:1520-1556  (Buy: enchant level)
        bool_ = True
        if paramInt == -7:
            self.aL_v()                      # falls through into case -3
            as_.gR = i16(as_.gR - 1 if as_.gR > 0 else 9)
        elif paramInt in (-3, 52):
            as_.gR = i16(as_.gR - 1 if as_.gR > 0 else 9)
        elif paramInt in (-4, 54):
            as_.gR = i16(as_.gR + 1 if as_.gR < 9 else 0)
        elif paramInt in (-2, -1, 50, 56):
            as_.gR = i16(as_.gR + (-5 if as_.gR > 4 else 5))
        elif paramInt in (-5, 53):
            if as_.hu[15 - as_.gR] > 0:
                as_.gS = 0
                as_.gT = 1
                self.c_I(786)
                as_.hr = 0
            else:
                ag.cS.d_I(8)
        else:
            bool_ = False
        if bool_:
            as_.aJ()

    def Y_I(self, paramInt):  # as.java:1558-1608  (Buy: the lots)
        if paramInt == -7:
            if as_.gP == 2:
                self.aL_v()
                return
            as_.hr = 0
            self.c_I(784)
        elif paramInt in (-5, 53):
            ag.fK[19] = as_.gz[ag.fK[18]].a
            if as_.gz[ag.fK[18]].a != 0:
                if as_.gB[ag.fK[18]] > ag.cz.E:
                    ag.cS.d_I(11)
                    return
                if ag.fK[16] >= 25:
                    ag.cS.d_I(12)
                    return
                as_.hk = ag.fK[18]
                ag.cS.m = str(as_.gB[ag.fK[18]])
                ag.cS.d_I(34)
                as_.gt = 10
            return
        else:
            i = self.a_IZ(paramInt, False)
            if i != 0:
                if i < 0:
                    if as_.gS > 1:
                        as_.gT = -1
                        as_.hr = 0
                        self.c_I(786)
                    else:
                        ag.cS.d_I(9)
                else:
                    as_.gT = 1
                    as_.hr = 0
                    self.c_I(786)
            else:
                return
        as_.aJ()

    def Z_I(self, paramInt):  # as.java:1610-1626  (Buy: category)
        if paramInt == -7:
            self.bf_v()
            return
        i = self.P_I(paramInt)
        if 0 <= i <= 2:
            as_.gW = i16(as_.gL)
            as_.gX = i16(as_.gM)
            as_.gP = i16(i)
            as_.e_Z(True)
            self.aL_v()
            return
        if i == -2:
            as_.aJ()

    def aL_v(self):  # as.java:1628-1633
        self.c_Z(False)
        as_.ho = 6
        as_.hp = 5
        as_.aJ()

    def aM_v(self):  # as.java:1635-1639
        as_.ho = 7
        as_.hp = 6
        as_.aJ()

    def aN_v(self):  # as.java:1641-1646
        self.aO_v()
        as_.ho = 8
        as_.hp = 7
        as_.aJ()

    def aO_v(self):  # as.java:1648-1650
        self.a_IIZ(4, 2, True)

    def c_Z(self, paramBoolean):  # as.java:1652-1666  (restore the grid cursor)
        as_.ht[7] = as_.hf
        as_.gP = as_.ha
        if paramBoolean:
            self.a_IIZ(5 if as_.ht[7] == 0 else 20, 3, False)
        else:
            self.a_IIZ(4 if as_.gP == 2 else 3, 3, False)
        ag.fK[10] = as_.hb
        ag.fK[9] = as_.hc
        ag.fK[18] = as_.hd
        ag.fK[8] = as_.he
        as_.hv[5] = as_.hg
        as_.hv[6] = as_.hh

    def aP_v(self):  # as.java:1668-1674  (Sell: Backpack / Warehouse grid)
        self.c_Z(True)
        as_.hp = 8
        as_.ho = 4
        as_.hn = as_.hl[5]
        as_.aJ()

    def aQ_v(self):  # as.java:1676-1681
        as_.ho = 9
        as_.hp = 9
        as_.hn = as_.hl[5]
        as_.aJ()

    def d_Z(self, paramBoolean):  # as.java:1683-1695
        if paramBoolean:
            as_.hr = 0
            as_.gS = 0
            self.c_I(864)
        else:
            as_.hk = 0
            as_.hp = 13
            as_.ho = 10
            as_.hn = as_.hl[8]
        as_.aJ()

    def aR_v(self):  # as.java:1697-1705  (after 513: notices, Sale List, Gift List, Exp/Fame, sync)
        as_.hr = i16(as_.hr + as_.hs)
        if as_.ht[15] == 1 and as_.d:
            self.c_I(516)
            as_.aJ()
            return
        self.aS_v()

    def aS_v(self):  # as.java:1707-1715
        as_.hr = i16(as_.hr + as_.hs)
        if as_.ht[14] == 1:
            self.c_I(518)
            as_.aJ()
            return
        self.aU_v()

    def aT_v(self):  # as.java:1717-1723
        as_.hk = 0
        as_.hp = 1
        as_.ho = 11
        as_.hn = as_.hl[0] if as_.gD == 0 else as_.hl[1]
        as_.aJ()

    def aU_v(self):  # as.java:1725-1733
        as_.hr = i16(as_.hr + as_.hs)
        if as_.ht[13] == 1:
            self.c_I(520)
            as_.aJ()
            return
        self.aV_v()

    def aV_v(self):  # as.java:1735-1744
        as_.hr = i16(as_.hr + as_.hs)
        if ag.fR == 0:
            self.c_I(258)
            as_.aJ()
            return
        ag.fR = 2
        self.aW_v()

    def aW_v(self):  # as.java:1746-1750
        as_.hr = i16(as_.hr + as_.hs)
        self.c_I(260)
        as_.aJ()

    def aX_v(self):  # as.java:1752-1756
        as_.hr = i16(as_.hr + as_.hs)
        self.c_I(768)
        as_.aJ()

    def aa_I(self, paramInt):  # as.java:1758-1785  (Trade: Buy / Sell / Cancel)
        if paramInt == -7:
            self.aH_v()
            return
        i = self.P_I(paramInt)
        if i >= 0:
            as_.gW = i16(as_.gL)
            as_.gX = i16(as_.gM)
            if i == 0:
                as_.gY = as_.gZ = 0
                self.aY_v()
            elif i == 1:
                as_.e_Z(True)
                self.aP_v()
            elif i == 2:
                as_.e_Z(True)
                self.d_Z(True)
            return
        if i == -2:
            as_.aJ()

    def ab_I(self, paramInt):  # as.java:1787-1804  (Warehouse grid: move an item)
        if paramInt == -7:
            self.aH_v()
            return
        if paramInt in (-5, 53):
            z1 = as_.be_v()
            if z1.a > 0:
                self.c_I(816)
                as_.hr = 0
                as_.aJ()
            return
        self.ac_I(paramInt)

    def aY_v(self):  # as.java:1806-1812
        self.aZ_v()
        as_.hp = 4
        as_.ho = 5
        as_.hn = as_.hl[4]
        as_.aJ()

    def aZ_v(self):  # as.java:1814-1824
        as_.e_TII("Normal Items|Special Items|Rare Items|", 20, 255)
        as_.gL = as_.gY
        as_.gM = as_.gZ
        as_.aC_v()
        i = 32 + as_.aB_v()
        i = 20 + (255 - i >> 1)
        as_.hv[15] = i
        as_.gN = i + 22 + 10

    def ac_I(self, paramInt):  # as.java:1826-1841  (grid keys, -6 switches Backpack / Warehouse)
        if paramInt == -6:
            if as_.ht[7] == 1:
                self.bc_v()
                as_.aJ()
                return
            if as_.ht[7] == 0:
                self.bd_v()
                as_.aJ()
                return
        else:
            self.a_IZ(paramInt, True)

    def a_IZ(self, paramInt, paramBoolean):  # as.java:1843-1877  (grid cursor)
        fK = ag.fK
        i = 1
        if paramInt in (-1, 50):
            fK[10] = fK[10] - 1
        elif paramInt in (-2, 56):
            fK[10] = fK[10] + 1
        elif paramInt in (-3, 52):
            fK[9] = fK[9] - 1
            if fK[9] - 1 < 0:
                fK[9] = 4
                fK[10] = fK[10] - 1
        elif paramInt in (-4, 54):
            fK[9] = fK[9] + 1
            if fK[9] + 1 >= 5:
                fK[9] = 0
                fK[10] = fK[10] + 1
        else:
            i = 0
        if i:
            i = as_.f_Z(paramBoolean)
            if i == 0:
                as_.aJ()
        return i

    def ad_I(self, paramInt):  # as.java:1879-1968  (Safe)
        bool_ = True
        if as_.ht[14] == 0:
            if paramInt in (-4, -3):
                as_.ht[15] = i16(as_.ht[15] ^ 0x1)
            elif paramInt in (-1, 50):
                as_.ht[15] = 0
            elif paramInt in (-2, 56):
                as_.ht[15] = 1
            elif paramInt == -7:
                self.aH_v()
                ag.ct[22] = None
                ag.ct[24] = None
            elif paramInt in (-5, 53):
                if as_.ht[15] == 0:
                    as_.hv[15] = as_.gy
                    if as_.gy == 0:
                        ag.cS.d_I(14)
                else:
                    as_.hv[15] = ag.cz.E
                    if ag.cz.E == 0:
                        ag.cS.d_I(15)
                if as_.hv[15] > 0:
                    as_.ht[14] = 1
                    as_.hv[14] = 0
                    as_.ho = 3
                    as_.aJ()
            else:
                bool_ = False
        else:
            if 48 <= paramInt <= 57:
                i = ag.N_I(paramInt)
                if i != -1:
                    as_.hv[14] = as_.hv[14] * 10
                    as_.hv[14] = as_.hv[14] + i
                    if as_.hv[14] > as_.hv[15]:
                        as_.hv[14] = as_.hv[15]
            elif paramInt == -7:
                if as_.hv[14] > 0:
                    as_.hv[14] = idiv(as_.hv[14], 10)
                else:
                    as_.ht[14] = 0
                    as_.ho = 2
                    as_.aJ()
            elif paramInt == -5:
                if as_.hv[14] > 0:
                    self.c_I(832)
                    as_.ht[14] = 0
                    as_.ho = 2
                    as_.aJ()
                else:
                    bool_ = False
            else:
                bool_ = False
        if bool_:
            as_.aJ()

    def ba_v(self):  # as.java:1970-1978  (leave Gamevil Live -> Game Menu)
        ag.bV = 2
        self.o_v()
        ag.ck = 1
        ag.cM[0] = 0
        ag.cM[1] = 2
        ag.cS.a = 0
        ag.bp = False

    @staticmethod
    def e_Z(paramBoolean):  # as.java:1980-1999  (remember / reset the grid cursor)
        as_.ha = as_.gP
        if paramBoolean:
            as_.hb = as_.hc = as_.hd = as_.he = as_.hf = as_.hg = as_.hh = 0
            return
        as_.hf = as_.ht[7]
        as_.hb = i16(ag.fK[10])
        as_.hc = i16(ag.fK[9])
        as_.hd = i16(ag.fK[18])
        as_.he = i16(ag.fK[8])
        as_.hg = i16(as_.hv[5])
        as_.hh = i16(as_.hv[6])

    def bb_v(self):  # as.java:2001-2007  (Warehouse screen)
        self.bc_v()
        as_.hp = 14
        as_.ho = 4
        as_.hn = as_.hl[9]
        as_.aJ()

    def bc_v(self):  # as.java:2009-2012
        as_.ht[7] = 0
        self.a_IIZ(5, 3, True)

    def bd_v(self):  # as.java:2014-2017
        as_.ht[7] = 1
        self.a_IIZ(20, 3, True)

    def a_IIZ(self, paramInt1, paramInt2, paramBoolean):  # as.java:2019-2043  (grid geometry)
        fK = ag.fK
        fK[3] = paramInt2
        fK[6] = 32 * paramInt2 - 4 + 2
        fK[4] = paramInt1
        fK[7] = 32 * paramInt1 - 4 + 2
        c = 156                              # char c = '\u009c'
        if paramInt2 < paramInt1:
            c += 8
            fK[11] = 1
            fK[13] = fK[6] * (fK[6] - 2) * 10
            fK[13] = idiv(idiv(fK[13], fK[7]) + 9, 10)
        else:
            fK[11] = 0
        fK[5] = 240 - c >> 1
        fK[12] = fK[5] + 156 + 4
        fK[26] = -1
        fK[27] = 0
        if paramBoolean:
            fK[8] = 0
            fK[10] = 0
            fK[9] = 0
            as_.f_Z(True)

    @staticmethod
    def f_Z(paramBoolean):  # as.java:2045-2072  (clamp the grid cursor; -1 / 1 = left the grid)
        fK = ag.fK
        if fK[10] < 0:
            if paramBoolean:
                fK[10] = fK[4] - 1
            else:
                fK[10] = as_.hv[5]
                fK[9] = as_.hv[6]
                return -1
        elif fK[10] >= fK[4]:
            if paramBoolean:
                fK[10] = 0
            else:
                fK[10] = as_.hv[5]
                fK[9] = as_.hv[6]
                return 1
        as_.hv[5] = fK[10]
        as_.hv[6] = fK[9]
        if fK[10] < fK[8]:
            fK[8] = fK[10]
        elif fK[10] >= fK[8] + fK[3]:
            fK[8] = fK[10] - fK[3] + 1
        fK[18] = fK[10] * 5 + fK[9]
        return 0

    @staticmethod
    def be_v():  # as.java:2074-2081  (the selected item of the Backpack / Warehouse grid)
        if as_.ht[7] == 0:
            as_.hj = as_.gv[ag.fK[18]]
            return ag.cz.Y[ag.fK[18]]
        as_.hj = as_.gx[ag.fK[18]]
        return as_.gw[ag.fK[18]]

    def bf_v(self):  # as.java:2083-2093  (Trade menu)
        as_.e_TII("Buy Item|Sell Item|Cancel Sell|", 26, 243)
        as_.gL = as_.gW
        as_.gM = as_.gX
        as_.aC_v()
        as_.hp = 3
        as_.ho = 1
        as_.hn = as_.hl[3]
        as_.aJ()

    def ae_I(self, paramInt):  # as.java:2095-2126  (GAMEVIL LIVE menu)
        if paramInt == -7:
            self.ba_v()
            if ag.fS == 0:
                return
        else:
            i = self.P_I(paramInt)
            if i >= 0:
                as_.gU = i16(as_.gL)
                as_.gV = i16(as_.gM)
                if i == 0:
                    as_.gW = as_.gX = 0
                    self.bf_v()
                elif i == 1:
                    as_.e_Z(True)
                    self.bb_v()
                elif i == 2:
                    self.bg_v()
                elif i == 3:
                    self.bh_v()
                return
            if i == -2:
                as_.aJ()

    def bg_v(self):  # as.java:2128-2135  (Safe)
        as_.ht[15] = 0
        as_.ht[14] = 0
        as_.hp = 15
        as_.ho = 2
        as_.hn = as_.hl[10]
        as_.aJ()

    def bh_v(self):  # as.java:2137-2143  (Management)
        as_.e_TII("Save User Data|Load User Data|", 26, 243)
        as_.hp = 16
        as_.hn = as_.hl[11]
        as_.aJ()

    def af_I(self, paramInt):  # as.java:2145-2159  (Management keys)
        if paramInt == -7:
            self.aH_v()
            return
        i = self.P_I(paramInt)
        if 0 <= i <= 1:
            as_.ht[14] = i16(i)
            ag.cS.d_I(16 if i == 0 else 17)
            as_.gt = 9
            return
        if i == -2:
            as_.aJ()

    @staticmethod
    def bi_v():  # as.java:2161-2164
        v.i = False
        as_.b = None
