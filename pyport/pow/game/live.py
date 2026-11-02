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
from pow.game.game_canvas import GameCanvas
from pow.game.structs import Item
from pow.game.live_net import LiveNet
from pow.game.gfx import Gfx
from pow.midp import system
from pow.midp.graphics import Image
from pow.midp.jint import i8, i16, idiv

F20 = config.DECOMP_FIX["F20"]
B4 = config.ORIG_BUG["B4"]
B5 = config.ORIG_BUG["B5"]


class Live(GameCanvas):
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
        super().__init__(GameCanvas.bs)
        if Live.gv is None:
            Live.gv = [0] * 25
        if Live.gx is None:
            Live.gx = [0] * 100

    def g_v(self):  # as.java:180-190  (Game Menu > Gamevil Live)
        from pow.game.live_screen import LiveScreen
        Live.o = True
        if LiveScreen.b_v():
            Live.n = False
            Live.a.d_v()
            GameCanvas.cS.d_I(2)
            Live.gt = 2
            return
        self.h_v()

    def h_v(self):  # as.java:192-208  (registration screen)
        from pow.game.name_buffer import NameBuffer
        GameCanvas.bp = True
        GameCanvas.ai()
        Live.hn = "Registration"
        Live.ho = 13
        Live.hp = 18
        Live.k = 1
        GameCanvas.bP = 0
        Live.aJ()
        GameCanvas.bV = 11
        Live.l = ""
        Live.m = ""
        GameCanvas.bz = None
        GameCanvas.bz = NameBuffer("", 12, 10)
        self.k_v()
        Live.aJ()

    def i_v(self):  # as.java:210-299  (every frame from ag.run)
        if Live.b is not None:
            Live.b.pump()
        if Live.g != -1:
            self.d_I(Live.g)
        if GameCanvas.cS.q:
            GameCanvas.cS.q = False
            i = Live.gt
            Live.gt = -1
            s1 = GameCanvas.cS.k
            if i == 3:
                self.ba_v()
                Live.aJ()
            elif i == 2:
                if s1 == 0:
                    GameCanvas.bp = True
                    GameCanvas.ai()
                    self.k_v()
                    self.aE_v()
                    self.aI_v()
                    self.c_I(512)
                else:
                    self.ba_v()
                    Live.aJ()
            elif i == 7:
                if Live.ht[15] > 0:
                    self.c_I(516)
                else:
                    self.aS_v()
            elif i == 8:
                self.aX_v()
            elif i == 9:
                if s1 == 0:
                    bool_ = False
                    if Live.ht[14] == 1:
                        for b in range(9):
                            if GameCanvas.cz.X[b].a > 0:
                                bool_ = True
                                break
                        if bool_:
                            GameCanvas.cS.d_I(33)
                            return self._i_end()
                    Live.hr = 0
                    if Live.ht[14] == 0:
                        self.c_I(256)
                    else:
                        self.c_I(262)
            elif i == 10:
                if s1 == 0:
                    if GameCanvas.fK[16] < 25:
                        Live.ht[7] = 0
                        Live.hr = 0
                        self.c_I(788)
                    else:
                        GameCanvas.cS.d_I(12)
                        Live.gt = 11
            elif i == 11:
                if s1 == 0:
                    Live.ht[7] = 1
                    Live.hr = 0
                    self.c_I(788)
            elif i == 14:
                if s1 == 0:
                    Live.hr = 0
                    self.c_I(866)
                    Live.hq = True
        self._i_end()

    def _i_end(self):
        if Live.e:
            self.m_v()

    @staticmethod
    def b_I(paramInt):  # as.java:301-353  (error code -> gamestr popup)
        b = {-1: 21, -2: 22, -4: 23, -12: 24, -13: 25, -15: 26, -16: 27, -18: 28, -20: 29,
             -22: 30, -23: 31, -26: 7, -49: 54}.get(paramInt, -1)
        if paramInt == -26:
            Live.gt = 3
        elif paramInt == -11:
            b = 10 if Live.gS > 0 else 8
        if b != -1:
            GameCanvas.cS.d_I(b)

    def j_v(self):  # as.java:355-364  ("Connecting..." over the screen)
        GameCanvas.cS.b_I(96)
        i = GameCanvas.de - 20 - 10
        j = Live.p.getWidth()
        k = Live.p.getHeight()
        GameCanvas.a_IIIIMII((GameCanvas.bJ - j) // 2, i, j, k, Live.p, 0, 0)
        GameCanvas.a_IIIIMII((GameCanvas.bJ - j) // 2, i, j * (GameCanvas.bN % 6) // 5, k, Live.q, 0, 0)
        Gfx.a_Lg(GameCanvas.bu)
        Gfx.a_TIII("Connecting...", GameCanvas.bJ // 2, i + 50, 1)

    def k_v(self):  # as.java:366-378
        try:
            if Live.p is None:
                Live.p = Image.createImage("/netLoading0.png")
            if Live.q is None:
                Live.q = Image.createImage("/netLoading1.png")
            if Live.r is None:
                Live.r = Image.createImage("/ui_arrow2.png")
            if Live.s is None:
                Live.s = Image.createImage("/ui_level.png")
        except Exception:
            pass
        Live.l_v()

    @staticmethod
    def l_v():  # as.java:380-386
        if Live.b is None:
            Live.b = LiveNet()
            Live.b.setPriority(5)
            Live.b.start()

    def f_v(self):  # as.java:388-390  (s.f(): connected)
        self.n_v()

    def c_I(self, paramInt):  # as.java:392-397  (ask for a request on the next i())
        Live.gr = 0
        GameCanvas.v_v()
        Live.gu = True
        Live.g = paramInt

    def d_I(self, paramInt):  # as.java:399-413
        Live.g = -1
        Live.gp = 0
        if not LiveNet.h:
            Live.gp = paramInt
            Live.gq = 530
        else:
            Live.gq = paramInt
        Live.f = system.currentTimeMillis()
        Live.e = False
        self.e_I(Live.gq)
        Live.aJ()
        Live.e = True

    def m_v(self):  # as.java:415-438  (answer came / timeout)
        if Live.gs:
            if not Live.gH:
                GameCanvas.w_v()
                Live.e = False
                Live.gu = False
                Live.aJ()
        elif LiveNet.m and not Live.gH and (GameCanvas.ch == -7 or system.currentTimeMillis() > Live.f + 30000):
            Live.gr = -1
            if Live.b is not None:
                Live.b.a_v()
                Live.bi_v()
                GameCanvas.R_v()
            Live.gu = False
            self.a_IILab(Live.gq + 1, Live.gr, None)
            Live.aJ()
        if Live.gr == 1 and Live.gq == 530 and Live.gp != 530:
            Live.gq = Live.gp
            self.c_I(Live.gq)

    def e_I(self, paramInt):  # as.java:440-451
        Live.gq = paramInt
        if not LiveNet.h:
            if Live.b is None:
                Live.l_v()
            LiveNet.a_Ls(self)
            Live.b.a_TI(GameCanvas.bk, GameCanvas.bl)
        else:
            self.n_v()
        Live.gs = False

    def n_v(self):  # as.java:453-576  (write the request gq)
        cz = GameCanvas.cz
        Live.gr = 0
        Live.b.a_I(Live.gq)
        q = Live.gq
        if q == 530:
            LiveNet.b_TI(Live.m, 12)
            LiveNet.b_TI(Live.l, 16)
            LiveNet.b_TI("1501", 4)
            LiveNet.b_I(Live.gn)
            Live.go = system.currentTimeMillis() // 10000
            LiveNet.b_I(Live.go)
        elif q in (516, 256):
            LiveNet.b_I(cz.F)
            LiveNet.b_I(cz.G)
            LiveNet.a_S(cz.l)
            LiveNet.a_B(cz.aB)
            LiveNet.a_B(GameCanvas.g_I(cz.X[0].a) ^ 0x1)
            LiveNet.a_S(cz.m)
            LiveNet.a_S(cz.n)
            LiveNet.a_S(cz.o)
            LiveNet.a_S(cz.q)
            LiveNet.a_S(cz.J)
            GameCanvas.O_v()
            LiveNet.a_S(cz.s)
            LiveNet.a_S(cz.t)
            LiveNet.a_S(cz.u)
            LiveNet.a_S(cz.v)
            for b1 in range(8):
                LiveNet.b_I(GameCanvas.dy[b1])
            b = 0
            for b2 in range(len(cz.W)):
                if cz.W[b2] > 0:
                    b += 1
            LiveNet.a_B(b)
            for b3 in range(len(cz.W)):
                if cz.W[b3] > 0:
                    LiveNet.a_B(Live.gG[b3])
                    LiveNet.a_B(cz.W[b3])
                    bool_ = False
                    for b8 in range(4):
                        if cz.V[b8] - 12 == b3:
                            bool_ = True
                            break
                    LiveNet.a_Z(bool_)
            LiveNet.b_TI(cz.k, 8)
            LiveNet.a_Z(not (cz.S == 0))
            LiveNet.a_B(GameCanvas.fo & 0xFF)
            for b4 in range(GameCanvas.fo):
                LiveNet.a_B(GameCanvas.fn[0][b4] & 0xFF)
                LiveNet.a_B(GameCanvas.fn[1][b4] & 0xFF)
            LiveNet.b_I(GameCanvas.dw & 0xFFFFFFFF)
            LiveNet.b_I(GameCanvas.dw >> 32 & 0xFFFFFFFF)
            LiveNet.a_B(GameCanvas.cq)
            for b5 in range(22):
                LiveNet.a_B(cz.g[b5] & 0xFF)
            LiveNet.a_B(cz.h & 0xFF)
            LiveNet.a_B(cz.i & 0xFF)
            LiveNet.b_I(GameCanvas.ed)
        elif q == 768:
            from pow.game.menus import Menus
            LiveNet.b_I(cz.E)
            Menus.m_v()
            b6 = i8(GameCanvas.fK[16])
            LiveNet.a_B(b6)
            for b7 in range(25):
                if cz.Y[b7].a > 0:
                    LiveNet.a_S(cz.Y[b7].a)
                    Live.gv[b7] = i16(b7 + 1)
                    LiveNet.a_S(Live.gv[b7])
                    LiveNet.a_B(cz.Y[b7].f)
                    LiveNet.a_S(cz.Y[b7].b)
                    LiveNet.a_S(cz.Y[b7].c)
                    LiveNet.a_S(cz.Y[b7].d)
                    LiveNet.a_S(cz.Y[b7].e)
        elif q == 832:
            LiveNet.a_B(Live.ht[15] ^ 0x1)
            LiveNet.b_I(Live.hv[14])
        elif q == 816:
            LiveNet.a_B(Live.ht[7])
            LiveNet.a_S(Live.hj)
        elif q in (784, 786, 788, 800):     # case 784 / 786 / 788 / 800 fall through
            if q == 784:
                LiveNet.a_B(Live.gP + 1)
            if q in (784, 786):
                LiveNet.a_B(Live.gP + 1)
                LiveNet.a_B(Live.gQ + 1)
                LiveNet.a_B(Live.gR)
            if q in (784, 786, 788):
                LiveNet.b_I(Live.gA[GameCanvas.fK[18]])
            LiveNet.a_B(Live.ht[7])
            LiveNet.a_S(Live.hj)
            LiveNet.b_I(Live.hv[14])
        elif q in (802, 866):               # case 802 falls through into 866
            if q == 802:
                LiveNet.a_B(Live.gP + 1)
                LiveNet.a_B(Live.gQ + 1)
            LiveNet.b_I(Live.gA[Live.hk])
            LiveNet.a_B(0 if GameCanvas.fK[16] < 25 else 1)
        Live.b.b_v()

    def o_v(self):  # as.java:578-591
        LiveNet.h = False
        if Live.b is not None:
            Live.b.a_v()
            Live.bi_v()
        if GameCanvas.bV == 11:
            Live.gt = 3
            GameCanvas.cS.d_I(29)
        Live.gu = False
        Live.e = False
        GameCanvas.f_I(300)

    def e_v(self):  # as.java:593-599  (s.e(): the connection failed / broke)
        if Live.b is not None:
            Live.b.a_v()
            Live.bi_v()
        Live.gs = True

    @staticmethod
    def _copy(dst, src):
        dst.a, dst.b, dst.c, dst.d, dst.e, dst.f = src.a, src.b, src.c, src.d, src.e, src.f

    def a_Lab(self, paramab):  # as.java:601-990  (s.a(ab): one answer)
        cz = GameCanvas.cz
        fK = GameCanvas.fK
        Live.gH = True
        LiveNet.m = False
        s1 = paramab.b_v()
        b = paramab.a_v()
        if F20:
            Live.gr = b                      # DECOMP_FIX F20
        Live.h = s1
        if B5 and s1 == 531:
            Live.gE = False                  # ORIG-BUG B5
        if b == 1:
            if s1 == 531:
                Live.gn = Live.go
                self.ar()
                paramab.a_v()
                paramab.a_v()
                b6 = paramab.a_v()
                if (b6 == 0 or b6 == 2) and Live.n:
                    from pow.game.live_screen import LiveScreen
                    LiveScreen.c_v()
                    if b6 == 0:
                        GameCanvas.cS.d_I(48)
                    elif b6 == 2:
                        GameCanvas.cS.d_I(44)
                    Live.gt = 2
                    Live.n = False
            elif s1 == 513:
                Live.ht[15] = paramab.a_v()
                Live.ht[14] = paramab.a_v()
                Live.ht[13] = paramab.a_v()
                paramab.a_v()
                for _ in range(5):
                    paramab.c_v()
                Live.ht[4] = paramab.a_v()
                Live.ht[5] = paramab.a_v()
                self.aR_v()
                Live.aJ()
            elif s1 == 517:
                GameCanvas.cS.m = GameCanvas.e_T(GameCanvas.f_T(paramab.a_I(16)))
                GameCanvas.cS.n = GameCanvas.e_T(GameCanvas.f_T(paramab.a_I(16)))
                GameCanvas.cS.o = GameCanvas.e_T(GameCanvas.f_T(paramab.a_I(16)))
                GameCanvas.cS.p = GameCanvas.e_T(GameCanvas.f_T(paramab.a_I(16)))
                GameCanvas.cS.d_I(53)
                Live.gt = 7
                if paramab.a_v() == 1:
                    Live.ht[15] = i16(Live.ht[15] + 1)
                else:
                    Live.ht[15] = 0
            elif s1 == 519:
                for b1 in range(20):
                    if Live.gz[b1] is None:
                        Live.gz[b1] = Item()
                    Item.a(Live.gz[b1])
                    Live.gB[b1] = 0
                b5 = paramab.a_v()
                for b1 in range(b5):
                    Live.gz[b1].a = paramab.b_v()
                    Live.gz[b1].f = paramab.a_v()
                    Live.gB[b1] = paramab.c_v()
                Live.gD = 0
                self.aT_v()
            elif s1 == 261:
                GameCanvas.fR = i16(GameCanvas.fR - 1)
                if GameCanvas.fR == 0:
                    self.ar()
                    if Live.hv[15] == 0 and Live.hv[14] == 0:
                        if Live.d:
                            GameCanvas.cS.d_I(20)
                        else:
                            GameCanvas.cS.q = True
                    else:
                        GameCanvas.cS.m = str(Live.hv[14])
                        GameCanvas.cS.n = str(Live.hv[15])
                        GameCanvas.cS.o = str(Live.hv[13])
                        GameCanvas.cS.d_I(41)
                    Live.gt = 8
                else:
                    GameCanvas.fR = 0
                    self.aV_v()
            elif s1 == 263:
                cz.F = paramab.c_v()
                cz.G = paramab.c_v()
                cz.l = paramab.b_v() & 0xFF
                cz.aB = paramab.a_v()
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
                    while b7 < 19 and Live.gG[b7] != b8:
                        b7 += 1
                    cz.W[b7] = paramab.a_v()
                    b8 = paramab.a_v()
                    if b8 == 1:
                        cz.V[b2] = b7 + 12
                        b2 += 1
                    b1 += 1
                for b1 in range(8):
                    GameCanvas.dy[b1] = paramab.c_v()
                cz.k = GameCanvas.g_T(GameCanvas.f_T(paramab.a_I(8)))
                cz.S = paramab.a_v()
                for b1 in range(45):
                    GameCanvas.fn[0][b1] = 0
                    GameCanvas.fn[1][b1] = 0
                GameCanvas.fo = i16(paramab.a_v())
                for b1 in range(GameCanvas.fo):
                    GameCanvas.fn[0][b1] = i16(paramab.a_v())
                    GameCanvas.fn[1][b1] = i16(paramab.a_v())
                i = paramab.c_v()
                GameCanvas.dw = paramab.c_v()
                GameCanvas.dw <<= 32
                GameCanvas.dw |= i                  # sic: a negative low word fills the high one (Java long |)
                GameCanvas.cq = paramab.a_v()
                for b1 in range(22):
                    cz.g[b1] = i16(paramab.a_v())
                cz.h = i16(paramab.a_v())
                cz.i = i16(paramab.a_v())
                GameCanvas.ed = paramab.c_v()
                self.ar()
                GameCanvas.cS.d_I(19)
            elif s1 == 257:
                GameCanvas.cS.d_I(18)
            elif s1 == 769:
                Live.gy = paramab.c_v()
                for b1 in range(100):
                    if Live.gw[b1] is None:
                        Live.gw[b1] = Item()
                    Item.a(Live.gw[b1])
                Live.ht[6] = i16(paramab.a_v() & 0xFF)
                for b1 in range(len(Live.gw)):
                    Item.a(Live.gw[b1])
                for b1 in range(Live.ht[6]):
                    Live.gw[b1].a = paramab.b_v()
                    Live.gx[b1] = paramab.b_v()
                    Live.gw[b1].f = paramab.a_v()
                    Live.gw[b1].b = paramab.b_v()
                    Live.gw[b1].c = paramab.b_v()
                    Live.gw[b1].d = paramab.b_v()
                    Live.gw[b1].e = paramab.b_v()
                self.aH_v()
            elif s1 == 833:
                cz.E = paramab.c_v()
                Live.gy = paramab.c_v()
            elif s1 == 817:
                if Live.ht[7] == 0:
                    Live.gK = 100
                    fK[16] = fK[16] - 1
                    Live.ht[6] = i16(Live.ht[6] + 1)
                    b1 = 0
                    while b1 < Live.gK and Live.gw[b1].a != 0:
                        b1 += 1
                    Live._copy(Live.gw[b1], cz.Y[fK[18]])
                    Item.a(cz.Y[fK[18]])
                    Live.gx[b1] = paramab.b_v()
                    Live.gv[fK[18]] = 0
                else:
                    Live.gK = 25
                    Live.ht[6] = i16(Live.ht[6] - 1)
                    fK[16] = fK[16] + 1
                    b1 = 0
                    while b1 < Live.gK and cz.Y[b1].a != 0:
                        b1 += 1
                    Live._copy(cz.Y[b1], Live.gw[fK[18]])
                    Item.a(Live.gw[fK[18]])
                    Live.gv[b1] = paramab.b_v()
                    Live.gx[fK[18]] = 0
                self.O_I(0)
                Live.aJ()
            elif s1 == 785:
                b1 = 0
                b3 = 15
                while b1 < 10:
                    Live.hu[b3] = paramab.a_v()
                    b1 += 1
                    b3 -= 1
                self.aM_v()
            elif s1 == 521:
                for b1 in range(5):
                    if Live.gz[b1] is None:
                        Live.gz[b1] = Item()
                    Item.a(Live.gz[b1])
                    Live.gC[b1] = ""
                b5 = paramab.a_v()
                for b1 in range(b5):
                    Live.gC[b1] = GameCanvas.f_T(paramab.a_I(8))
                    Live.gz[b1].a = paramab.b_v()
                    Live.gz[b1].f = paramab.a_v()
                    Live.gz[b1].b = paramab.b_v()
                    Live.gz[b1].c = paramab.b_v()
                    Live.gz[b1].d = paramab.b_v()
                    Live.gz[b1].e = paramab.b_v()
                Live.ht[13] = paramab.a_v()
                Live.gD = 1
                self.aT_v()
            elif s1 == 787:
                for b1 in range(20):
                    if Live.gz[b1] is None:
                        Live.gz[b1] = Item()
                    Item.a(Live.gz[b1])
                    Live.gA[b1] = 0
                    Live.gB[b1] = 0
                b4 = paramab.a_v()
                for b1 in range(b4):
                    Live.gA[b1] = paramab.c_v()
                    Live.gz[b1].a = paramab.b_v()
                    Live.gB[b1] = paramab.c_v()
                    Live.gz[b1].f = paramab.a_v()
                    Live.gz[b1].b = paramab.b_v()
                    Live.gz[b1].c = paramab.b_v()
                    Live.gz[b1].d = paramab.b_v()
                    Live.gz[b1].e = paramab.b_v()
                Live.gS = i8(Live.gS + Live.gT)
                self.aN_v()
            elif s1 == 789:
                if B4 and Live.ht[7] == 1:     # ORIG-BUG B4: bought into the warehouse
                    Live.ht[6] = i16(Live.ht[6] + 1)
                    b1 = 0
                    while b1 < 100 and Live.gw[b1].a != 0:
                        b1 += 1
                    Live._copy(Live.gw[b1], Live.gz[fK[18]])
                    Live.p_v()
                    Live.gx[b1] = paramab.b_v()
                else:
                    Live.gK = 25
                    fK[16] = fK[16] + 1
                    b1 = 0
                    while b1 < Live.gK and cz.Y[b1].a != 0:
                        b1 += 1
                    Live._copy(cz.Y[b1], Live.gz[fK[18]])
                    Live.p_v()
                    Live.gv[b1] = paramab.b_v()
                cz.E = paramab.c_v()
                Live.gy = paramab.c_v()
                self.O_I(0)
                GameCanvas.cS.d_I(35)
            elif s1 == 801:
                if Live.ht[7] == 0:
                    Item.a(cz.Y[Live.hk])
                    Live.gv[Live.hk] = 0
                    fK[16] = fK[16] - 1
                else:
                    Item.a(Live.gw[Live.hk])
                    Live.gx[Live.hk] = 0
                    Live.ht[6] = i16(Live.ht[6] - 1)
                self.O_I(0)
                GameCanvas.cS.d_I(36)
                self.aP_v()
            elif s1 in (803, 865):
                for b1 in range(20):
                    if Live.gz[b1] is None:
                        Live.gz[b1] = Item()
                    Item.a(Live.gz[b1])
                    Live.gA[b1] = 0
                    Live.gB[b1] = 0
                b4 = paramab.a_v()
                if b4 > 20:
                    b4 = 20
                for b1 in range(b4):
                    if s1 == 865:
                        Live.gA[b1] = paramab.c_v()
                    Live.gz[b1].a = paramab.b_v()
                    Live.gB[b1] = paramab.c_v()
                    Live.gz[b1].f = paramab.a_v()
                    Live.gz[b1].b = paramab.b_v()
                    Live.gz[b1].c = paramab.b_v()
                    Live.gz[b1].d = paramab.b_v()
                    Live.gz[b1].e = paramab.b_v()
                if s1 == 803:
                    self.aO_v()
                    Live.ho = 8
                    Live.hp = 10
                    Live.hn = Live.hl[6]
                    Live.aJ()
                else:
                    self.d_Z(False)
            elif s1 == 867:
                if Live.ht[7] == 0:
                    Live.gK = 25
                    Live.ht[6] = i16(Live.ht[6] - 1)
                    fK[16] = fK[16] + 1
                    b1 = 0
                    while b1 < Live.gK and cz.Y[b1].a != 0:
                        b1 += 1
                    Live._copy(cz.Y[b1], Live.gz[Live.hk])
                    Item.a(Live.gz[Live.hk])
                    Live.p_v()
                    Live.gv[b1] = paramab.b_v()
                else:
                    Live.gK = 100
                    fK[16] = fK[16] - 1
                    Live.ht[6] = i16(Live.ht[6] + 1)
                    b1 = 0
                    while b1 < Live.gK and Live.gw[b1].a != 0:
                        b1 += 1
                    Live._copy(Live.gw[b1], Live.gz[Live.hk])
                    Item.a(Live.gz[Live.hk])
                    Live.p_v()
                    Live.gx[b1] = paramab.b_v()
                self.O_I(0)
                GameCanvas.cS.d_I(40)
            elif s1 == 259:
                Live.hv[15] = paramab.c_v()
                Live.hv[14] = paramab.c_v()
                Live.hv[13] = GameCanvas.H_I(Live.hv[14])
                cz.F += Live.hv[15]
                GameCanvas.fR = 1
                self.ar()
                self.aW_v()
        else:
            self.a_IILab(Live.h, Live.gr if F20 else 0, paramab)
        Live.gH = False
        LiveNet.m = True
        Live.gs = True

    def a_IILab(self, paramInt1, paramInt2, paramab):  # as.java:992-1056  (error answers)
        if paramInt1 == 531:
            if paramab is None:
                Live.b_I(paramInt2)
                Live.gt = 3
                return
            paramab.a_v()
            paramab.a_v()
            b = paramab.a_v()
            if b == 1:
                GameCanvas.cS.d_I(43)
                return
            if b == 3 and paramInt2 != -49:
                GameCanvas.cS.d_I(47)
                return
            Live.b_I(paramInt2)
            Live.gt = 3
            return
        if paramInt1 == 513:
            Live.b_I(paramInt2)
            Live.gt = 3
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
            Live.b_I(paramInt2)
            Live.gt = 3
            return
        if paramInt1 == 789:
            Live.b_I(paramInt2)
            return
        if paramInt1 == 867 and paramInt2 == -12:
            Live.p_v()
        if paramInt1 in (867, 801, 817, 833, 849):
            self.O_I(0)
        Live.b_I(paramInt2)

    @staticmethod
    def p_v():  # as.java:1058-1062
        Item.a(Live.gz[Live.hk])
        Live.gB[Live.hk] = 0
        Live.gA[Live.hk] = 0

    def O_I(self, paramInt):  # as.java:1064-1067  (save the game)
        GameCanvas.fS = i16(paramInt)
        self.ar()

    @staticmethod
    def aB_v():  # as.java:1069-1071
        return 32 * Live.gK - 12

    @staticmethod
    def e_TII(paramString, paramInt1, paramInt2):  # as.java:1073-1092  ("a|b|c|" -> list menu)
        i = 0
        j = 0
        for b in range(len(paramString)):
            if paramString[b] == '|':
                Live.gI[i] = paramString[j:b]
                j = b + 1
                i += 1
        if i == 0:
            return
        Live.gJ = i16(i)
        i = idiv(paramInt2 + 12, 32)
        Live.gK = i16(i)
        if Live.gK > Live.gJ:
            Live.gK = Live.gJ
        Live.gN = i16(paramInt1 + (paramInt2 - 32 * Live.gK - 12 >> 1))
        Live.gM = Live.gL = 0

    def P_I(self, paramInt):  # as.java:1094-1109  (list keys: -2 moved, index chosen, -1)
        i = -1
        if paramInt in (-1, -2, 50, 56):
            if paramInt in (-1, 50):
                Live.gL -= 1
                if Live.gL < 0:
                    Live.gL = i16(Live.gJ - 1)
            else:
                Live.gL += 1
                if Live.gL >= Live.gJ:
                    Live.gL = 0
            Live.aC_v()
            i = -2
        elif paramInt in (-5, 53):
            i = Live.gL
        return i

    @staticmethod
    def aC_v():  # as.java:1111-1118
        if Live.gM > Live.gL:
            Live.gM = Live.gL
            return
        if Live.gL - Live.gM >= Live.gK:
            Live.gM = Live.gL - Live.gK + 1

    def aD_v(self):  # as.java:1120-1135  (draw the list menu)
        i = Live.gN
        b = 0
        j = Live.gM
        while b < Live.gK:
            if j == Live.gL:
                GameCanvas.a_IIIIIIIZ(45, i, 150, 20, GameCanvas.k_III(0, 0, 0), GameCanvas.k_III(255, 255, 255), GameCanvas.k_III(0, 0, 0), True)
                Gfx.a_Lg(GameCanvas.bw)
            else:
                GameCanvas.a_IIIIIIIZ(46, i + 1, 148, 18, GameCanvas.k_III(0, 0, 0), GameCanvas.k_III(80, 80, 80), GameCanvas.k_III(0, 0, 0), True)
                Gfx.a_Lg(GameCanvas.bu)
            GameCanvas.b_IIT(120, i + 1, Live.gI[j])
            i += 32
            b += 1
            j += 1

    def aE_v(self):  # as.java:1137-1143
        self.aF_v()
        self.aG_v()
        GameCanvas.az()
        GameCanvas.bV = 11
        Live.gO = GameCanvas.bY.a

    def aF_v(self):  # as.java:1145-1149
        for b in range(12):
            Live.hl[b] = GameCanvas.M_I(2 + b)
        return True

    def aG_v(self):  # as.java:1151-1155
        for b in range(50):
            Live.hm[b] = GameCanvas.M_I(15 + b)
        return True

    def aH_v(self):  # as.java:1157-1176  (GAMEVIL LIVE menu)
        Live.e_TII("Trade|Warehouse|Safe|Management|", 20, 255)
        Live.gL = Live.gU
        Live.gM = Live.gV
        Live.aC_v()
        Live.hp = 2
        Live.ho = 1
        Live.hn = Live.hl[2]
        Live.hr = 0
        Live.hs = 10
        if Live.o and Live.d:
            Live.o = False
            GameCanvas.cS.m = Live.l
            GameCanvas.cS.n = Live.m
            GameCanvas.cS.d_I(49)
        Live.aJ()
        Live.d = False

    def aI_v(self):  # as.java:1178-1184  (waiting screen)
        Live.hp = 17
        Live.ho = 12
        Live.hn = Live.hl[2]
        Live.j = 0
        Live.aJ()

    @staticmethod
    def aJ():  # as.java:1186-1188
        Live.hq = True

    @staticmethod
    def a_IIIZ(paramInt1, paramInt2, paramInt3, paramBoolean):  # as.java:1190-1194  (item cell)
        GameCanvas.bb.a_IIZ(paramInt2, paramInt3, paramBoolean)
        if paramInt1 > 0:
            GameCanvas.bb.a_IIII(paramInt1, paramInt2, paramInt3, 0)

    @staticmethod
    def a_TIII(paramString, paramInt1, paramInt2, paramInt3):  # as.java:1196-1198
        Gfx.a_TIII(paramString, paramInt1 + idiv(paramInt3, 2), paramInt2, 1)

    @staticmethod
    def aK():  # as.java:1200-1202
        Live.a.a_v()

    def c_TI(self, paramString, paramInt):  # as.java:1204-1209  (caption box)
        Gfx.a_Lg(GameCanvas.bu)
        self.b_III(paramInt, 200, 22)
        if paramString != "":
            self.b_TII(paramString, paramInt + 1 - GameCanvas.dc, 0)

    def t_I(self, paramInt):  # as.java:1211-1269  (keys)
        i = paramInt
        if GameCanvas.cS.b != 0:
            GameCanvas.cS.b_v()
            GameCanvas.ch = -999
            Live.aJ()
            return
        GameCanvas.ch = -999
        h = {1: self.R_I, 2: self.ae_I, 3: self.aa_I, 4: self.Z_I, 5: self.W_I, 6: self.X_I, 7: self.Y_I,
             8: self.U_I, 9: self.V_I, 10: self.T_I, 13: self.S_I, 14: self.ab_I, 15: self.ad_I,
             16: self.af_I, 18: self.Q_I}.get(Live.hp)
        if h is not None:
            h(i)

    def Q_I(self, paramInt):  # as.java:1271-1328  (registration: UserID, then password)
        if Live.k == 0:
            i = len(Live.l)
            if paramInt == -7:
                if i > 0:
                    Live.l = Live.l[:i - 1]
                else:
                    Live.k = 1
                    Live.aJ()
                if i == 10:
                    Live.aJ()
                    return
            elif paramInt == -6:
                if i >= 4:
                    Live.gE = True
                    Live.n = True
                    self.c_I(530)
                    return
            else:
                j = GameCanvas.N_I(paramInt)
                if j != -1 and i < 12:
                    Live.l += str(j)
                return
        elif Live.k == 1:
            if len(GameCanvas.bz.a_v()) == 0 and paramInt == -7:
                self.ba_v()
                return
            i = GameCanvas.r_I(paramInt)
            if i == -7:
                GameCanvas.bz.a_I(-8)
                return
            if i == -5 or i == 53:
                if GameCanvas.bP == 26 and len(GameCanvas.bz.a_v()) >= 4:
                    if len(GameCanvas.bz.a_v()) != 0:
                        Live.m = GameCanvas.bz.a_v()
                        GameCanvas.bz.a_T(Live.m)
                        Live.k = 0
                        Live.aJ()
                        return
                else:
                    GameCanvas.bz.a_I(65 + GameCanvas.bP)
                    return
            elif i == -6 and len(GameCanvas.bz.a_v()) >= 4 and len(GameCanvas.bz.a_v()) != 0:
                Live.m = GameCanvas.bz.a_v()
                GameCanvas.bz.a_T(Live.m)
                Live.k = 0
                Live.aJ()

    def R_I(self, paramInt):  # as.java:1330-1357  (Sale / Gift List)
        if paramInt == -3:
            Live.hk = Live.hk - 1 if Live.hk > 0 else 4
            Live.aJ()
        elif paramInt == -4:
            Live.hk = Live.hk + 1 if Live.hk < 4 else 0
            Live.aJ()
        elif paramInt in (-8, -5):
            if Live.gD == 0:
                self.aU_v()
            else:
                self.aV_v()

    def S_I(self, paramInt):  # as.java:1359-1394  (Cancel Sell: my 5 lots)
        from pow.game.menus import Menus
        if paramInt == -7:
            self.bf_v()
        elif paramInt in (-5, 53):
            if Live.gz[Live.hk].a > 0:
                Live.hi = Live.gz[Live.hk].a
                Live.ht[7] = 0 if GameCanvas.fK[16] < 25 else 1
                GameCanvas.cS.m = Menus.c_I(Live.gz[Live.hk].a)
                GameCanvas.cS.d_I(39)
                Live.gt = 14
        elif paramInt in (-3, 52):
            Live.hk = Live.hk - 1 if Live.hk > 0 else 4
            Live.aJ()
        elif paramInt in (-4, 54):
            Live.hk = Live.hk + 1 if Live.hk < 4 else 0
            Live.aJ()

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
            z1 = Live.be_v()
            if z1.a > 0:
                if 434 <= z1.a <= 437:
                    GameCanvas.cS.d_I(13)
                    return
                Live.hi = z1.a
                Live.gR = i16(z1.f)
                Live.hk = GameCanvas.fK[18]
                if z1.a > 500:
                    Live.gP = 2
                    Live.gQ = i16(z1.a - 501)
                elif z1.a > 300:
                    Live.gP = 1
                    Live.gQ = i16(GameCanvas.bH[1].a_II(z1.a - 301, 7))
                else:
                    Live.gP = 0
                    Live.gQ = i16(GameCanvas.bH[0].a_II(z1.a - 101, 7))
                Live.hv[13] = 0
                Live.hv[14] = 0
                Live.e_Z(True)
                self.aQ_v()
            return
        self.ac_I(paramInt)

    def V_I(self, paramInt):  # as.java:1442-1489  (Sell: the price)
        bool_ = True
        if 48 <= paramInt <= 57:
            i = GameCanvas.N_I(paramInt)
            if 0 <= i <= 9 and Live.hv[13] < 9:
                Live.hv[14] = Live.hv[14] * 10
                Live.hv[14] = Live.hv[14] + i
                if Live.hv[14] > 0:
                    Live.hv[13] = Live.hv[13] + 1
        elif paramInt == -7:
            if Live.hv[13] > 0:
                Live.hv[14] = idiv(Live.hv[14], 10)
                Live.hv[13] = Live.hv[13] - 1
            else:
                self.aP_v()
        elif paramInt == -5:
            if Live.hv[14] > 0:
                self.c_I(800)
                Live.hr = 0
            else:
                bool_ = False
        elif paramInt == -6:
            self.c_I(802)
            Live.hr = 0
        else:
            bool_ = False
        if bool_:
            Live.aJ()

    def W_I(self, paramInt):  # as.java:1491-1518  (Buy: kind)
        if paramInt == -7:
            self.aY_v()
            return
        if paramInt in (-5, 53):
            if Live.gF[Live.gP][GameCanvas.fK[18]] != 0:
                Live.e_Z(False)
                Live.hi = Live.gF[Live.gP][GameCanvas.fK[18]]
                Live.gQ = i16(GameCanvas.fK[18])
                if Live.gP == 2:
                    Live.gR = 0
                    Live.gS = 0
                    Live.gT = 1
                    self.c_I(786)
                else:
                    Live.gR = 0
                    self.c_I(784)
                Live.hr = 0
                Live.aJ()
            return
        self.a_IZ(paramInt, False)

    def X_I(self, paramInt):  # as.java:1520-1556  (Buy: enchant level)
        bool_ = True
        if paramInt == -7:
            self.aL_v()                      # falls through into case -3
            Live.gR = i16(Live.gR - 1 if Live.gR > 0 else 9)
        elif paramInt in (-3, 52):
            Live.gR = i16(Live.gR - 1 if Live.gR > 0 else 9)
        elif paramInt in (-4, 54):
            Live.gR = i16(Live.gR + 1 if Live.gR < 9 else 0)
        elif paramInt in (-2, -1, 50, 56):
            Live.gR = i16(Live.gR + (-5 if Live.gR > 4 else 5))
        elif paramInt in (-5, 53):
            if Live.hu[15 - Live.gR] > 0:
                Live.gS = 0
                Live.gT = 1
                self.c_I(786)
                Live.hr = 0
            else:
                GameCanvas.cS.d_I(8)
        else:
            bool_ = False
        if bool_:
            Live.aJ()

    def Y_I(self, paramInt):  # as.java:1558-1608  (Buy: the lots)
        if paramInt == -7:
            if Live.gP == 2:
                self.aL_v()
                return
            Live.hr = 0
            self.c_I(784)
        elif paramInt in (-5, 53):
            GameCanvas.fK[19] = Live.gz[GameCanvas.fK[18]].a
            if Live.gz[GameCanvas.fK[18]].a != 0:
                if Live.gB[GameCanvas.fK[18]] > GameCanvas.cz.E:
                    GameCanvas.cS.d_I(11)
                    return
                if GameCanvas.fK[16] >= 25:
                    GameCanvas.cS.d_I(12)
                    return
                Live.hk = GameCanvas.fK[18]
                GameCanvas.cS.m = str(Live.gB[GameCanvas.fK[18]])
                GameCanvas.cS.d_I(34)
                Live.gt = 10
            return
        else:
            i = self.a_IZ(paramInt, False)
            if i != 0:
                if i < 0:
                    if Live.gS > 1:
                        Live.gT = -1
                        Live.hr = 0
                        self.c_I(786)
                    else:
                        GameCanvas.cS.d_I(9)
                else:
                    Live.gT = 1
                    Live.hr = 0
                    self.c_I(786)
            else:
                return
        Live.aJ()

    def Z_I(self, paramInt):  # as.java:1610-1626  (Buy: category)
        if paramInt == -7:
            self.bf_v()
            return
        i = self.P_I(paramInt)
        if 0 <= i <= 2:
            Live.gW = i16(Live.gL)
            Live.gX = i16(Live.gM)
            Live.gP = i16(i)
            Live.e_Z(True)
            self.aL_v()
            return
        if i == -2:
            Live.aJ()

    def aL_v(self):  # as.java:1628-1633
        self.c_Z(False)
        Live.ho = 6
        Live.hp = 5
        Live.aJ()

    def aM_v(self):  # as.java:1635-1639
        Live.ho = 7
        Live.hp = 6
        Live.aJ()

    def aN_v(self):  # as.java:1641-1646
        self.aO_v()
        Live.ho = 8
        Live.hp = 7
        Live.aJ()

    def aO_v(self):  # as.java:1648-1650
        self.a_IIZ(4, 2, True)

    def c_Z(self, paramBoolean):  # as.java:1652-1666  (restore the grid cursor)
        Live.ht[7] = Live.hf
        Live.gP = Live.ha
        if paramBoolean:
            self.a_IIZ(5 if Live.ht[7] == 0 else 20, 3, False)
        else:
            self.a_IIZ(4 if Live.gP == 2 else 3, 3, False)
        GameCanvas.fK[10] = Live.hb
        GameCanvas.fK[9] = Live.hc
        GameCanvas.fK[18] = Live.hd
        GameCanvas.fK[8] = Live.he
        Live.hv[5] = Live.hg
        Live.hv[6] = Live.hh

    def aP_v(self):  # as.java:1668-1674  (Sell: Backpack / Warehouse grid)
        self.c_Z(True)
        Live.hp = 8
        Live.ho = 4
        Live.hn = Live.hl[5]
        Live.aJ()

    def aQ_v(self):  # as.java:1676-1681
        Live.ho = 9
        Live.hp = 9
        Live.hn = Live.hl[5]
        Live.aJ()

    def d_Z(self, paramBoolean):  # as.java:1683-1695
        if paramBoolean:
            Live.hr = 0
            Live.gS = 0
            self.c_I(864)
        else:
            Live.hk = 0
            Live.hp = 13
            Live.ho = 10
            Live.hn = Live.hl[8]
        Live.aJ()

    def aR_v(self):  # as.java:1697-1705  (after 513: notices, Sale List, Gift List, Exp/Fame, sync)
        Live.hr = i16(Live.hr + Live.hs)
        if Live.ht[15] == 1 and Live.d:
            self.c_I(516)
            Live.aJ()
            return
        self.aS_v()

    def aS_v(self):  # as.java:1707-1715
        Live.hr = i16(Live.hr + Live.hs)
        if Live.ht[14] == 1:
            self.c_I(518)
            Live.aJ()
            return
        self.aU_v()

    def aT_v(self):  # as.java:1717-1723
        Live.hk = 0
        Live.hp = 1
        Live.ho = 11
        Live.hn = Live.hl[0] if Live.gD == 0 else Live.hl[1]
        Live.aJ()

    def aU_v(self):  # as.java:1725-1733
        Live.hr = i16(Live.hr + Live.hs)
        if Live.ht[13] == 1:
            self.c_I(520)
            Live.aJ()
            return
        self.aV_v()

    def aV_v(self):  # as.java:1735-1744
        Live.hr = i16(Live.hr + Live.hs)
        if GameCanvas.fR == 0:
            self.c_I(258)
            Live.aJ()
            return
        GameCanvas.fR = 2
        self.aW_v()

    def aW_v(self):  # as.java:1746-1750
        Live.hr = i16(Live.hr + Live.hs)
        self.c_I(260)
        Live.aJ()

    def aX_v(self):  # as.java:1752-1756
        Live.hr = i16(Live.hr + Live.hs)
        self.c_I(768)
        Live.aJ()

    def aa_I(self, paramInt):  # as.java:1758-1785  (Trade: Buy / Sell / Cancel)
        if paramInt == -7:
            self.aH_v()
            return
        i = self.P_I(paramInt)
        if i >= 0:
            Live.gW = i16(Live.gL)
            Live.gX = i16(Live.gM)
            if i == 0:
                Live.gY = Live.gZ = 0
                self.aY_v()
            elif i == 1:
                Live.e_Z(True)
                self.aP_v()
            elif i == 2:
                Live.e_Z(True)
                self.d_Z(True)
            return
        if i == -2:
            Live.aJ()

    def ab_I(self, paramInt):  # as.java:1787-1804  (Warehouse grid: move an item)
        if paramInt == -7:
            self.aH_v()
            return
        if paramInt in (-5, 53):
            z1 = Live.be_v()
            if z1.a > 0:
                self.c_I(816)
                Live.hr = 0
                Live.aJ()
            return
        self.ac_I(paramInt)

    def aY_v(self):  # as.java:1806-1812
        self.aZ_v()
        Live.hp = 4
        Live.ho = 5
        Live.hn = Live.hl[4]
        Live.aJ()

    def aZ_v(self):  # as.java:1814-1824
        Live.e_TII("Normal Items|Special Items|Rare Items|", 20, 255)
        Live.gL = Live.gY
        Live.gM = Live.gZ
        Live.aC_v()
        i = 32 + Live.aB_v()
        i = 20 + (255 - i >> 1)
        Live.hv[15] = i
        Live.gN = i + 22 + 10

    def ac_I(self, paramInt):  # as.java:1826-1841  (grid keys, -6 switches Backpack / Warehouse)
        if paramInt == -6:
            if Live.ht[7] == 1:
                self.bc_v()
                Live.aJ()
                return
            if Live.ht[7] == 0:
                self.bd_v()
                Live.aJ()
                return
        else:
            self.a_IZ(paramInt, True)

    def a_IZ(self, paramInt, paramBoolean):  # as.java:1843-1877  (grid cursor)
        fK = GameCanvas.fK
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
            i = Live.f_Z(paramBoolean)
            if i == 0:
                Live.aJ()
        return i

    def ad_I(self, paramInt):  # as.java:1879-1968  (Safe)
        bool_ = True
        if Live.ht[14] == 0:
            if paramInt in (-4, -3):
                Live.ht[15] = i16(Live.ht[15] ^ 0x1)
            elif paramInt in (-1, 50):
                Live.ht[15] = 0
            elif paramInt in (-2, 56):
                Live.ht[15] = 1
            elif paramInt == -7:
                self.aH_v()
                GameCanvas.ct[22] = None
                GameCanvas.ct[24] = None
            elif paramInt in (-5, 53):
                if Live.ht[15] == 0:
                    Live.hv[15] = Live.gy
                    if Live.gy == 0:
                        GameCanvas.cS.d_I(14)
                else:
                    Live.hv[15] = GameCanvas.cz.E
                    if GameCanvas.cz.E == 0:
                        GameCanvas.cS.d_I(15)
                if Live.hv[15] > 0:
                    Live.ht[14] = 1
                    Live.hv[14] = 0
                    Live.ho = 3
                    Live.aJ()
            else:
                bool_ = False
        else:
            if 48 <= paramInt <= 57:
                i = GameCanvas.N_I(paramInt)
                if i != -1:
                    Live.hv[14] = Live.hv[14] * 10
                    Live.hv[14] = Live.hv[14] + i
                    if Live.hv[14] > Live.hv[15]:
                        Live.hv[14] = Live.hv[15]
            elif paramInt == -7:
                if Live.hv[14] > 0:
                    Live.hv[14] = idiv(Live.hv[14], 10)
                else:
                    Live.ht[14] = 0
                    Live.ho = 2
                    Live.aJ()
            elif paramInt == -5:
                if Live.hv[14] > 0:
                    self.c_I(832)
                    Live.ht[14] = 0
                    Live.ho = 2
                    Live.aJ()
                else:
                    bool_ = False
            else:
                bool_ = False
        if bool_:
            Live.aJ()

    def ba_v(self):  # as.java:1970-1978  (leave Gamevil Live -> Game Menu)
        GameCanvas.bV = 2
        self.o_v()
        GameCanvas.ck = 1
        GameCanvas.cM[0] = 0
        GameCanvas.cM[1] = 2
        GameCanvas.cS.a = 0
        GameCanvas.bp = False

    @staticmethod
    def e_Z(paramBoolean):  # as.java:1980-1999  (remember / reset the grid cursor)
        Live.ha = Live.gP
        if paramBoolean:
            Live.hb = Live.hc = Live.hd = Live.he = Live.hf = Live.hg = Live.hh = 0
            return
        Live.hf = Live.ht[7]
        Live.hb = i16(GameCanvas.fK[10])
        Live.hc = i16(GameCanvas.fK[9])
        Live.hd = i16(GameCanvas.fK[18])
        Live.he = i16(GameCanvas.fK[8])
        Live.hg = i16(Live.hv[5])
        Live.hh = i16(Live.hv[6])

    def bb_v(self):  # as.java:2001-2007  (Warehouse screen)
        self.bc_v()
        Live.hp = 14
        Live.ho = 4
        Live.hn = Live.hl[9]
        Live.aJ()

    def bc_v(self):  # as.java:2009-2012
        Live.ht[7] = 0
        self.a_IIZ(5, 3, True)

    def bd_v(self):  # as.java:2014-2017
        Live.ht[7] = 1
        self.a_IIZ(20, 3, True)

    def a_IIZ(self, paramInt1, paramInt2, paramBoolean):  # as.java:2019-2043  (grid geometry)
        fK = GameCanvas.fK
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
            Live.f_Z(True)

    @staticmethod
    def f_Z(paramBoolean):  # as.java:2045-2072  (clamp the grid cursor; -1 / 1 = left the grid)
        fK = GameCanvas.fK
        if fK[10] < 0:
            if paramBoolean:
                fK[10] = fK[4] - 1
            else:
                fK[10] = Live.hv[5]
                fK[9] = Live.hv[6]
                return -1
        elif fK[10] >= fK[4]:
            if paramBoolean:
                fK[10] = 0
            else:
                fK[10] = Live.hv[5]
                fK[9] = Live.hv[6]
                return 1
        Live.hv[5] = fK[10]
        Live.hv[6] = fK[9]
        if fK[10] < fK[8]:
            fK[8] = fK[10]
        elif fK[10] >= fK[8] + fK[3]:
            fK[8] = fK[10] - fK[3] + 1
        fK[18] = fK[10] * 5 + fK[9]
        return 0

    @staticmethod
    def be_v():  # as.java:2074-2081  (the selected item of the Backpack / Warehouse grid)
        if Live.ht[7] == 0:
            Live.hj = Live.gv[GameCanvas.fK[18]]
            return GameCanvas.cz.Y[GameCanvas.fK[18]]
        Live.hj = Live.gx[GameCanvas.fK[18]]
        return Live.gw[GameCanvas.fK[18]]

    def bf_v(self):  # as.java:2083-2093  (Trade menu)
        Live.e_TII("Buy Item|Sell Item|Cancel Sell|", 26, 243)
        Live.gL = Live.gW
        Live.gM = Live.gX
        Live.aC_v()
        Live.hp = 3
        Live.ho = 1
        Live.hn = Live.hl[3]
        Live.aJ()

    def ae_I(self, paramInt):  # as.java:2095-2126  (GAMEVIL LIVE menu)
        if paramInt == -7:
            self.ba_v()
            if GameCanvas.fS == 0:
                return
        else:
            i = self.P_I(paramInt)
            if i >= 0:
                Live.gU = i16(Live.gL)
                Live.gV = i16(Live.gM)
                if i == 0:
                    Live.gW = Live.gX = 0
                    self.bf_v()
                elif i == 1:
                    Live.e_Z(True)
                    self.bb_v()
                elif i == 2:
                    self.bg_v()
                elif i == 3:
                    self.bh_v()
                return
            if i == -2:
                Live.aJ()

    def bg_v(self):  # as.java:2128-2135  (Safe)
        Live.ht[15] = 0
        Live.ht[14] = 0
        Live.hp = 15
        Live.ho = 2
        Live.hn = Live.hl[10]
        Live.aJ()

    def bh_v(self):  # as.java:2137-2143  (Management)
        Live.e_TII("Save User Data|Load User Data|", 26, 243)
        Live.hp = 16
        Live.hn = Live.hl[11]
        Live.aJ()

    def af_I(self, paramInt):  # as.java:2145-2159  (Management keys)
        if paramInt == -7:
            self.aH_v()
            return
        i = self.P_I(paramInt)
        if 0 <= i <= 1:
            Live.ht[14] = i16(i)
            GameCanvas.cS.d_I(16 if i == 0 else 17)
            Live.gt = 9
            return
        if i == -2:
            Live.aJ()

    @staticmethod
    def bi_v():  # as.java:2161-2164
        LiveNet.i = False
        Live.b = None
