"""MpCanvas (g.java): the canvas of the MP jar - screens, menus, battles.

Generated once from pyport/mp_java/g.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""
from pow_mp.rt import (
    ByteArrayInputStream,
    DataInputStream,
    Image,
    Random,
    RecordStore,
    _Canvas,
    _arraycopy,
    _inc,
    _js,
    _set,
    i32,
    i8,
    idiv,
    imod,
    system,
)



class _Brk_block0_1631(BaseException):
    pass


class _Brk_block0_2273(BaseException):
    pass


class _Brk_block0_2989(BaseException):
    pass


class _Brk_block1_457(BaseException):
    pass


class _Brk_block4_3348(BaseException):
    pass


class _Brk_block5_3348(BaseException):
    pass


class _Cont_block47_2359(BaseException):
    pass


class _Cont_block49_2378(BaseException):
    pass


class MpCanvas(_Canvas):
    a = None  # g.java:25 String
    b = None  # g.java:26 m
    c = None  # g.java:27 String
    d = 0  # g.java:28 int
    e = None  # g.java:29 Graphics
    f = None  # g.java:30 Image
    g = None  # g.java:31 Graphics
    h = None  # g.java:32 Random
    i = None  # g.java:33 String
    j = None  # g.java:34 String
    k = 0  # g.java:35 int
    l = None  # g.java:36 Main
    m = 0  # g.java:37 int
    n = None  # g.java:38 j
    o = None  # g.java:39 j
    p = None  # g.java:40 j
    q = None  # g.java:41 j
    r = None  # g.java:42 String
    s = 0  # g.java:43 int
    t = None  # g.java:44 String
    u = False  # g.java:45 boolean
    v = 0  # g.java:46 long
    w = False  # g.java:47 boolean
    x = False  # g.java:48 boolean
    y = 0  # g.java:49 int
    z = 0  # g.java:50 int
    A = False  # g.java:51 boolean
    B = 0  # g.java:52 int
    C = 0  # g.java:53 int
    D = False  # g.java:54 boolean
    E = 0  # g.java:55 int
    F = 0  # g.java:56 long
    G = False  # g.java:57 boolean
    H = 0  # g.java:58 int
    I = 0  # g.java:59 int
    J = False  # g.java:60 boolean
    K = False  # g.java:61 boolean
    L = False  # g.java:62 boolean
    M = 0  # g.java:63 long
    N = 0  # g.java:64 long
    O = False  # g.java:65 boolean
    P = False  # g.java:66 boolean
    Q = 0  # g.java:67 int
    R = 0  # g.java:68 int
    S = 0  # g.java:69 int
    T = 0  # g.java:70 int
    U = 0  # g.java:71 int
    V = 0  # g.java:72 int
    W = 0  # g.java:73 int
    X = 0  # g.java:74 int
    Y = None  # g.java:75 String[]
    Z = None  # g.java:76 int[]
    aa = None  # g.java:77 int[]
    ab = 0  # g.java:78 int
    ac = None  # g.java:79 int[]
    ad = 0  # g.java:80 int
    ae = 0  # g.java:81 byte
    af = 0  # g.java:82 int
    ag = None  # g.java:83 String
    ah = None  # g.java:84 String
    ai = None  # g.java:85 String
    aj = None  # g.java:86 String
    ak = None  # g.java:87 String
    al = 0  # g.java:88 int
    am = 0  # g.java:89 int
    an = 0  # g.java:90 int
    ao = 0  # g.java:91 int
    ap = 0  # g.java:92 int
    aq = False  # g.java:93 boolean
    ar = 0  # g.java:94 byte
    as_ = 0  # g.java:95 int
    at = 0  # g.java:96 int
    au = 0  # g.java:97 int
    av = 0  # g.java:98 int
    aw = 0  # g.java:99 int
    ax = 0  # g.java:100 int
    ay = 0  # g.java:101 int
    az = 0  # g.java:102 int
    aA = 0  # g.java:103 int
    aB = 0  # g.java:104 int
    aC = 0  # g.java:105 int
    aD = 0  # g.java:106 int
    aE = 0  # g.java:107 int
    aF = 0  # g.java:108 int
    aG = 0  # g.java:109 int
    aH = 0  # g.java:110 int
    aI = 0  # g.java:111 int
    aJ = 0  # g.java:112 int
    aK = 0  # g.java:113 int
    aL = 0  # g.java:114 int
    aM = 0  # g.java:115 int
    aN = 0  # g.java:116 byte
    aO = 0  # g.java:117 int
    aP = 0  # g.java:118 int
    aQ = 0  # g.java:119 int
    aR = 0  # g.java:120 int
    aS = 0  # g.java:121 int
    aT = 0  # g.java:122 int
    aU = 0  # g.java:123 int
    aV = 0  # g.java:124 int
    aW = 0  # g.java:125 byte
    aX = 0  # g.java:126 int
    aY = 0  # g.java:127 int
    aZ = 0  # g.java:128 int
    ba = 0  # g.java:129 int
    bb = 0  # g.java:130 int
    bc = 0  # g.java:131 int
    bd = 0  # g.java:132 int
    be = 0  # g.java:133 int
    bf = 0  # g.java:134 int
    bg = 0  # g.java:135 int
    bh = 0  # g.java:136 byte
    bi = False  # g.java:137 boolean
    bj = False  # g.java:138 boolean
    bk = False  # g.java:139 boolean
    bl = 0  # g.java:140 int
    bm = 0  # g.java:141 int
    bn = False  # g.java:142 boolean
    bo = 0  # g.java:143 int
    bp = 0  # g.java:144 int
    bq = False  # g.java:145 boolean
    br = False  # g.java:146 boolean
    bs = False  # g.java:147 boolean
    bt = False  # g.java:148 boolean
    bu = 0  # g.java:149 int
    bv = 0  # g.java:150 int
    bw = False  # g.java:151 boolean
    bx = False  # g.java:152 boolean
    by = 0  # g.java:153 int
    bz = 0  # g.java:154 byte
    bA = 0  # g.java:155 int
    bB = 0  # g.java:156 int
    bC = 0  # g.java:157 int
    bD = 0  # g.java:158 int
    bE = None  # g.java:159 byte[]
    bF = None  # g.java:160 String[]
    bG = None  # g.java:161 String
    bH = None  # g.java:162 String
    bI = None  # g.java:163 String
    bJ = 0  # g.java:164 int
    bK = 0  # g.java:165 int
    bL = None  # g.java:166 String
    bM = None  # g.java:167 String[]
    bN = None  # g.java:168 String[]
    bO = None  # g.java:169 String[]
    bP = None  # g.java:170 String[]
    bQ = None  # g.java:171 boolean[]
    bR = None  # g.java:172 int[]
    bS = None  # g.java:173 int[]
    bT = None  # g.java:174 int[]
    bU = None  # g.java:175 int[]
    bV = None  # g.java:176 int[]
    bW = None  # g.java:177 int[]
    bX = None  # g.java:178 int[]
    bY = None  # g.java:179 int[]
    bZ = None  # g.java:180 byte[]
    ca = None  # g.java:181 int[]
    cb = None  # g.java:182 int[]
    cc = None  # g.java:183 int[]
    cd = None  # g.java:184 int[]
    ce = None  # g.java:185 int[]
    cf = None  # g.java:186 int[]
    cg = None  # g.java:187 int[]
    ch = None  # g.java:188 int[]
    ci = None  # g.java:189 int[]
    cj = None  # g.java:190 int[]
    ck = None  # g.java:191 int[]
    cl = None  # g.java:192 int[]
    cm = None  # g.java:193 int[]
    cn = None  # g.java:194 int[]
    co = None  # g.java:195 int[]
    cp = None  # g.java:196 int[]
    cq = None  # g.java:197 int[]
    cr = None  # g.java:198 int[]
    cs = 0  # g.java:199 int
    ct = 0  # g.java:200 int
    cu = 0  # g.java:201 int
    cv = 0  # g.java:202 int
    cw = 0  # g.java:203 int
    cx = 0  # g.java:204 int
    cy = 0  # g.java:205 int
    cz = 0  # g.java:206 int
    cA = 0  # g.java:207 int
    cB = None  # g.java:208 byte[]
    cC = 0  # g.java:209 int
    cD = 0  # g.java:210 int
    cE = None  # g.java:211 String
    cF = None  # g.java:212 String
    cG = None  # g.java:213 String
    cH = None  # g.java:214 int[]
    cI = None  # g.java:215 int[]
    cJ = None  # g.java:216 int[]
    cK = None  # g.java:217 byte[]
    cL = 0  # g.java:218 int
    cM = 0  # g.java:219 int
    cN = 0  # g.java:220 int
    cO = 0  # g.java:221 int
    cP = 0  # g.java:222 int
    cQ = 0  # g.java:223 int
    cR = 0  # g.java:224 int
    cS = 0  # g.java:225 int
    cT = 0  # g.java:226 int
    cU = 0  # g.java:227 int
    cV = 0  # g.java:228 int
    cW = 0  # g.java:229 int
    cX = 0  # g.java:230 int
    cY = 0  # g.java:231 int
    cZ = 0  # g.java:232 int
    da = 0  # g.java:233 int
    db = 0  # g.java:234 int
    dc = 0  # g.java:235 int
    dd = None  # g.java:236 Image[]
    de = None  # g.java:237 Image[]
    df = None  # g.java:238 Image[]
    dg = None  # g.java:239 Image[]
    dh = None  # g.java:240 Image[]
    di = None  # g.java:241 Image[]
    dj = None  # g.java:242 Image[]
    dk = None  # g.java:243 Image
    dl = None  # g.java:244 Image
    dm = None  # g.java:245 Image
    dn = None  # g.java:246 Image
    do_ = None  # g.java:247 Image
    dp = None  # g.java:248 Image
    dq = None  # g.java:249 Image
    dr = None  # g.java:250 Image
    ds = None  # g.java:251 Image
    dt = None  # g.java:252 Image
    du = None  # g.java:253 Image[]
    dv = None  # g.java:254 a[]
    dw = None  # g.java:255 Image[][]
    dx = None  # g.java:256 a[][]
    dy = None  # g.java:257 Image[][]
    dz = None  # g.java:258 a[][]
    dA = None  # g.java:259 Image[][]
    dB = None  # g.java:260 a[][]
    dC = None  # g.java:261 Image[][]
    dD = None  # g.java:262 a[][]
    dE = None  # g.java:263 a[]
    dF = None  # g.java:264 Image[]
    dG = None  # g.java:265 a[]
    dH = None  # g.java:266 Image[]
    dI = None  # g.java:267 a[]
    dJ = None  # g.java:268 Image[]
    dK = None  # g.java:269 a[]
    dL = None  # g.java:270 Image[]
    dM = None  # g.java:271 a[]
    dN = None  # g.java:272 Image[]
    dO = None  # g.java:273 a[]
    dP = None  # g.java:274 h
    dQ = 0  # g.java:275 int
    dR = 0  # g.java:276 int
    dS = 0  # g.java:277 int
    dT = None  # g.java:278 Thread
    dU = None  # g.java:279 int[]
    dV = None  # g.java:280 int[]
    dW = 0  # g.java:281 int
    dX = False  # g.java:282 boolean
    dY = False  # g.java:283 boolean
    dZ = 0  # g.java:284 int
    ea = False  # g.java:285 boolean
    eb = False  # g.java:286 boolean
    ec = 0  # g.java:287 int
    ed = None  # g.java:288 String[]
    ee = 0  # g.java:289 long

    def __init__(self, main):  # g.java:295
        _Canvas.__init__(self)
        MpCanvas.l = main
        self.setFullScreenMode(True)

    @staticmethod
    def a_T(string):  # g.java:291
        print(_js(string))

    def a_v(self):  # g.java:300
        MpCanvas.dV[0] = 1
        _t1 = self.getWidth()
        MpCanvas.cQ = _t1
        MpCanvas.cS = _t1
        _t2 = self.getHeight()
        MpCanvas.cR = _t2
        MpCanvas.cT = _t2
        try:
            MpCanvas.a = MpCanvas.l.getAppProperty("MIDlet-Version")
            MpCanvas.r = MpCanvas.l.getAppProperty("GAMEVIL_SERVER")
            MpCanvas.s = int(MpCanvas.l.getAppProperty("GAMEVIL_PORT"))
            MpCanvas.t = MpCanvas.l.getAppProperty("GAMEVIL_GAME_VER")
        except Exception:
            MpCanvas.a = ""
            MpCanvas.r = "64.14.246.182"
            MpCanvas.s = 28200
            MpCanvas.t = "0111"
        MpCanvas.f = Image.createImage(MpCanvas.cQ, MpCanvas.cR)
        MpCanvas.g = MpCanvas.f.getGraphics()
        MpCanvas.cW = idiv(MpCanvas.cQ, 2)
        MpCanvas.cX = idiv(MpCanvas.cR, 2)
        MpCanvas.bK = ((idiv(MpCanvas.cQ, 2) - 28) - 3)
        n2 = 0
        while n2 < 4:
            MpCanvas.bP[n2] = ""
            n2 = n2 + 1
        MpCanvas.n = Font("/0_font.png", 5, 11, 6, 0xFFFFFF)
        MpCanvas.o = Font("/0_font.png", 5, 11, 6, 16400640)
        MpCanvas.p = Font("/0_font.png", 5, 11, 6, 0x646464)
        MpCanvas.q = Font("/0_font.png", 5, 11, 6, 0x41FF41)
        self.f_v()
        self.L_v()
        MpCanvas.b = MpGame(MpCanvas.l)
        MpCanvas.X_v()
        MpCanvas.i_I(0)

    def b_T(self, string):  # g.java:337
        image = None
        try:
            image = Image.createImage(string)
        except Exception as exception:
            MpCanvas.a_T(_js("--------createImage err:", exception))
        return image

    @staticmethod
    def a_G(graphics):  # g.java:348
        n2 = idiv(80, MpCanvas.k)
        if n2 > 30:
            n2 = 30
        elif n2 < 19:
            n2 = 19
        n3 = 0
        if ((MpCanvas.cY == 162) or (MpCanvas.cY == 163)) or (MpCanvas.cY == 164):
            n3 = 15
        elif MpCanvas.cY == 10:
            n3 = 40
        Draw.a_GMIIIIII(graphics, MpCanvas.do_, (idiv((((MpCanvas.cQ - (n2 * ((MpCanvas.k - 1)))) - 11)), 2) + (n2 * MpCanvas.dU[MpCanvas.dW])), ((MpCanvas.cX + 6) + n3), 12, 15, 0, 0)

    def paint(self, graphics):  # g.java:364
        MpCanvas.e = graphics
        Gfx.a_G(graphics)
        if MpCanvas.w:
            MpCanvas.dY = True
            return
        self.d_v()
        if graphics.getClipX() > 0:
            graphics.setClip(0, 0, MpCanvas.cQ, MpCanvas.cR)
        MpCanvas.dY = True

    @staticmethod
    def a_J(l2):  # g.java:378
        if l2 > 0:
            try:
                system.sleep(l2)
                return
            except Exception:
                pass

    @staticmethod
    def a_I(n2):  # g.java:388
        MpCanvas.H = n2

    def b_v(self):  # g.java:392
        if (not MpCanvas.K) or MpCanvas.L:
            MpCanvas.H = 0
            return
        if (MpCanvas.H != 0) and ((MpCanvas.H == 1) != MpCanvas.J):
            if MpCanvas.H == 1:
                MpCanvas.J = True
                if MpCanvas.b is not None:
                    MpCanvas.I = MpGame.fd
                    self.ag_v()
            elif MpCanvas.H == 2:
                MpCanvas.J = False
                if (MpCanvas.b is not None) and (MpCanvas.I != (-1)):
                    self.t_I(MpCanvas.I)
        MpCanvas.H = 0

    def run(self):  # g.java:414
        g2 = self
        self.a_v()
        self.c_v()
        MpCanvas.a_J(250)

    def c_v(self):  # g.java:423
        MpCanvas.ee = system.currentTimeMillis()
        while True:
            MpCanvas.ee = system.currentTimeMillis()
            if MpCanvas.J:
                if MpCanvas.m != (-999):
                    self.f_I(MpCanvas.m)
                    MpCanvas.m = (-999)
                MpCanvas.dY = False
                self.repaint()
                MpCanvas.a_J(250)
            else:
                l2 = 0
                n2 = 0
                if MpCanvas.m != (-999):
                    self.f_I(MpCanvas.m)
                    MpCanvas.m = (-999)
                MpCanvas.dY = False
                self.repaint()
                self.serviceRepaints()
                while not MpCanvas.dY:
                    MpCanvas.a_J(10)
                if MpCanvas.b is not None:
                    if ((((((MpCanvas.cY >= 10) and (MpCanvas.cY <= 89)) and (MpCanvas.cY != 88)) and (not MpCanvas.J)) or (MpCanvas.cY == 1)) or (MpCanvas.cY == 6)) or (MpCanvas.cY == 7):
                        self.s_I(1)
                    MpCanvas.b.ak_v()
                if (MpCanvas.cZ == MpCanvas.cY) and (MpCanvas.da < 25000):
                    MpCanvas.da = MpCanvas.da + 1
                if MpCanvas.da >= 25000:
                    MpCanvas.da = 100
                if ((n2 := (Consts.ef[MpCanvas.an] - i32(((((l2 := system.currentTimeMillis())) - MpCanvas.ee)))))) > 20:
                    MpCanvas.a_J(n2)
                else:
                    MpCanvas.a_J(20)
            self.b_v()
            MpCanvas.K = True

    def d_v(self):  # g.java:474
        if MpCanvas.dY:
            return
        if (MpCanvas.cY != 3) and (MpCanvas.cY != 10000):
            MpCanvas.L = False
        if MpCanvas.J:
            Draw.b_GIIIII(MpCanvas.e, 0, 0, MpCanvas.cS, MpCanvas.cT, 0)
            self.c_GIIIII(MpCanvas.e, MpCanvas.cW, MpCanvas.cX, 100, 29, 0)
            self.a_GTIIII(MpCanvas.e, Consts.eX[2], MpCanvas.cW, (MpCanvas.cX - 6), 1, 0xFFFFFF)
            return
        if NetThread.j and (not MpCanvas.eb):
            if NetThread.h > 100:
                NetThread.h = 0
                self.c_I(39327)
                if _inc(MpCanvas, 'dZ', 1) > 20:
                    MpCanvas.dZ = 0
                    MpCanvas.cw = 13
                    MpCanvas.x = False
                    self.o_v()
            else:
                NetThread.h = NetThread.h + 1
        if not MpCanvas.D:
            if MpCanvas.d == 1:
                MpCanvas.d = 0
                if MpCanvas.cY == 97:
                    if (_set(MpCanvas, 'cA', (MpCanvas.cA + MpCanvas.cz))) > (((MpCanvas.cW - 44) + 72) + MpCanvas.cz):
                        MpCanvas.cA = (((MpCanvas.cW - 44) + 72) + MpCanvas.cz)
                    else:
                        MpCanvas.b_I(1)
                else:
                    if _inc(MpCanvas, 'ba', -1) == 0:
                        MpCanvas.bB = 1
                        MpCanvas.cA = (((MpCanvas.cW - 44) + 72) + MpCanvas.cz)
                        self.C_v()
                    MpCanvas.b_I((10 - MpCanvas.an))
            elif MpCanvas.d > 0:
                MpCanvas.d = MpCanvas.d - 1
        MpCanvas.cZ = MpCanvas.cY
        _sw3 = MpCanvas.cY
        try:
            _m4 = False
            while True:
                if _m4 or _sw3 == 0:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        try:
                            MpCanvas.ds = self.b_T("/gamevillogo.png")
                            MpCanvas.dt = self.b_T("/softbg.png")
                            MpCanvas.dS = idiv(((MpCanvas.cR - ((MpCanvas.ds.getHeight() + 12)))), 2)
                            MpCanvas.ds.getHeight()
                            MpCanvas.ds.getWidth()
                        except Exception:
                            pass
                        MpCanvas.M = system.currentTimeMillis()
                        Draw.b_GIIIII(MpCanvas.g, 0, 0, MpCanvas.cQ, MpCanvas.cR, 0xFFFFFF)
                    self.e_v()
                    Draw.a_GMIII(MpCanvas.e, MpCanvas.ds, idiv(MpCanvas.cQ, 2), MpCanvas.dS, 17)
                    if (system.currentTimeMillis() - MpCanvas.M) <= 3000:
                        break
                    MpCanvas.ds = None
                    MpCanvas.cY = 5
                    return
                if _m4 or _sw3 == 161:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.c = Consts.eM[5]
                        MpCanvas.k = 3
                        self.U_v()
                    self.e_v()
                    self.a_GTIIIIZZ(MpCanvas.e, Consts.eR[MpCanvas.dU[MpCanvas.dW]], (MpCanvas.cW - 43), (MpCanvas.cX - 19), 86, 17, False, True)
                    MpCanvas.a_G(MpCanvas.e)
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 in (162, 163, 164):
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.c = Consts.eR[(MpCanvas.cY - 162)]
                        MpCanvas.k = 2
                        self.U_v()
                        MpCanvas.cO = ((MpCanvas.cQ - 96) >> 1)
                        MpCanvas.c_GIIII(MpCanvas.g, MpCanvas.cO, (MpCanvas.cX - 54), 96, 15)
                        self.a_GTIIII(MpCanvas.g, MpCanvas.i, (idiv(MpCanvas.cQ, 2) + 4), ((MpCanvas.cX + 2) - 54), 1, 0xFFFFFF)
                        MpCanvas.c_GIIII(MpCanvas.g, MpCanvas.cO, ((MpCanvas.cX + 14) - 54), 96, 15)
                        self.a_GTIIII(MpCanvas.g, Consts.eX[4], (MpCanvas.cO + 3), (((MpCanvas.cX + 14) + 2) - 54), 0, 0xFFFFFF)
                        MpCanvas.b_GIIII(MpCanvas.g, ((MpCanvas.cO + 96) - 7), (((MpCanvas.cX + 14) + 3) - 54), MpCanvas.ac[MpCanvas.ae], 0)
                        _sw5 = MpCanvas.cY
                        if _sw5 == 162:
                            var1_1 = Consts.eR[0]
                        else:
                            var1_1 = Consts.eX[3]
                        MpCanvas.c_GIIII(MpCanvas.g, MpCanvas.cO, ((MpCanvas.cX + 28) - 54), 96, 15)
                        self.a_GTIIII(MpCanvas.g, var1_1, (MpCanvas.cO + 3), (((MpCanvas.cX + 28) + 2) - 54), 0, 0xFFFFFF)
                        MpCanvas.b_GIIII(MpCanvas.g, ((MpCanvas.cO + 96) - 7), (((MpCanvas.cX + 28) + 3) - 54), MpCanvas.ad, 0)
                    self.e_v()
                    self.a_GTIIIIZZ(MpCanvas.e, Consts.eS[MpCanvas.dU[MpCanvas.dW]], (MpCanvas.cW - 43), ((MpCanvas.cX - 19) + 15), 86, 17, False, True)
                    MpCanvas.a_G(MpCanvas.e)
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 in (170, 171):
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.c = Consts.eS[(MpCanvas.cY - 170)]
                        self.l_G(MpCanvas.g)
                        var1_2 = ((MpCanvas.cQ - 110) >> 1)
                        var2_7 = (MpCanvas.cR >> 1)
                        _sw6 = MpCanvas.af
                        if _sw6 == 162:
                            var3_14 = Consts.eR[0]
                        elif _sw6 == 163:
                            var3_14 = Consts.eX[3]
                        else:
                            var3_14 = Consts.eX[3]
                        var4_16 = 0
                        while var4_16 < 3:
                            self.a_GTIIII(MpCanvas.g, MpCanvas.Y[var4_16], MpCanvas.cW, ((var2_7 - 65) + (45 * var4_16)), 1, 0xFFFFFF)
                            MpCanvas.c_GIIII(MpCanvas.g, var1_2, ((var2_7 - 52) + (45 * var4_16)), 110, 15)
                            MpCanvas.c_GIIII(MpCanvas.g, var1_2, ((var2_7 - 38) + (45 * var4_16)), 110, 15)
                            self.a_GTIIII(MpCanvas.g, Consts.eX[4], (var1_2 + 3), (((var2_7 - 52) + 2) + (45 * var4_16)), 0, 0xFFFFFF)
                            MpCanvas.b_GIIII(MpCanvas.g, ((var1_2 + 110) - 7), ((((var2_7 - 52) + 2) + 1) + (45 * var4_16)), MpCanvas.Z[var4_16], 0)
                            self.a_GTIIII(MpCanvas.g, var3_14, (var1_2 + 3), (((var2_7 - 38) + 2) + (45 * var4_16)), 0, 0xFFFFFF)
                            MpCanvas.b_GIIII(MpCanvas.g, ((var1_2 + 110) - 7), ((((var2_7 - 38) + 2) + 1) + (45 * var4_16)), MpCanvas.aa[var4_16], 0)
                            var4_16 = var4_16 + 1
                    self.e_v()
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 90:
                    _m4 = True
                    if MpCanvas.O:
                        self.W_v()
                        self.Y_v()
                        MpCanvas.O = False
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.bk = False
                    if MpCanvas.bj:
                        if MpCanvas.ca[MpCanvas.ct] == 0:
                            MpCanvas.bk = True
                        self.m_G(MpCanvas.g)
                        MpCanvas.bj = False
                    self.e_v()
                    self.c_G(MpCanvas.e)
                    if MpCanvas.bk:
                        self.y_v()
                        break
                    self.af_v()
                    return
                if _m4 or _sw3 == 91:
                    _m4 = True
                    self.e_v()
                    self.c_G(MpCanvas.e)
                    self.z_v()
                    if MpCanvas.da != idiv(1500, MpCanvas.dc):
                        break
                    self.c_I(1038)
                    return
                if _m4 or _sw3 == 92:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                    self.e_v()
                    self.c_G(MpCanvas.e)
                    if (MpCanvas.da >= idiv(500, MpCanvas.dc)) and (MpCanvas.da < idiv(1500, MpCanvas.dc)):
                        self.b_GI(MpCanvas.e, 0)
                    elif MpCanvas.da >= idiv(1500, MpCanvas.dc):
                        self.b_GI(MpCanvas.e, 1)
                    if MpCanvas.da != idiv(2500, MpCanvas.dc):
                        break
                    MpCanvas.aR = 0
                    MpCanvas.i_I(93)
                    return
                if _m4 or _sw3 == 93:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.X_v()
                        MpCanvas.da = 2
                        MpCanvas.aR = MpCanvas.aR + 1
                        if ((MpCanvas.bb == 0) or (MpCanvas.bc == 0)) or (MpCanvas.bW[0] == 0):
                            MpCanvas.i_I(103)
                        else:
                            MpCanvas.Q_v()
                    elif MpCanvas.da == idiv(1000, MpCanvas.dc):
                        self.c_I(1025)
                    self.e_v()
                    self.c_G(MpCanvas.e)
                    if ((((MpCanvas.aR > 0) and (MpCanvas.aR < 100)) and (MpCanvas.bb != 0)) and (MpCanvas.bc != 0)) and (MpCanvas.bW[0] != 0):
                        self.i_G(MpCanvas.e)
                        self.d_GI(MpCanvas.e, 2)
                        self.S_v()
                    return
                if _m4 or _sw3 == 94:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.bt = False
                    self.e_v()
                    if MpCanvas.D:
                        MpCanvas.dZ = 1
                        MpCanvas.da = MpCanvas.da - 1
                        self.c_GIIIII(MpCanvas.e, MpCanvas.cW, MpCanvas.cX, 120, 100, 0)
                        self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((MpCanvas.cX - 21) - 10), Consts.eX[60], 0xFFFFFF)
                        self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((MpCanvas.cX - 21) + 2), Consts.eX[61], 0xFFFFFF)
                        self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((MpCanvas.cX - 21) + 14), Consts.eX[62], 0xFFFFFF)
                        var1_3 = i32(((15 - idiv(((system.currentTimeMillis() - MpCanvas.F)), 1000))))
                        self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((MpCanvas.cX - 21) + 30), _js(Consts.eX[63], "   "), 0xFFFFFF)
                        self.a_GIITI(MpCanvas.e, (MpCanvas.cW + 35), ((MpCanvas.cX - 21) + 30), _js("", var1_3), 16400640)
                        var2_8 = 0
                        while var2_8 < 2:
                            if MpCanvas.E == var2_8:
                                self.a_GTIIII(MpCanvas.e, Consts.eX[(40 + var2_8)], ((MpCanvas.cW - 28) + (var2_8 * 55)), (MpCanvas.cX + 28), 1, 0xFFFFFF)
                                self.c_GIIIII(MpCanvas.e, ((MpCanvas.cW - 42) + (var2_8 * 55)), (MpCanvas.cX + 25), 29, 14, 3)
                            else:
                                self.c_GIIIII(MpCanvas.e, ((MpCanvas.cW - 42) + (var2_8 * 55)), (MpCanvas.cX + 25), 29, 14, 2)
                                self.a_GTIIII(MpCanvas.e, Consts.eX[(40 + var2_8)], ((MpCanvas.cW - 28) + (var2_8 * 55)), (MpCanvas.cX + 28), 1, 0x646464)
                            var2_8 = var2_8 + 1
                        if var1_3 > 0:
                            break
                        MpCanvas.D = False
                        break
                    self.c_G(MpCanvas.e)
                    MpCanvas.j_G(MpCanvas.e)
                    self.d_GI(MpCanvas.e, 0)
                    return
                if _m4 or _sw3 == 95:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.db = 0
                    self.e_v()
                    self.c_G(MpCanvas.e)
                    self.h_G(MpCanvas.e)
                    self.d_GI(MpCanvas.e, 1)
                    return
                if _m4 or _sw3 == 96:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        _sw7 = MpCanvas.bB
                        _m8 = False
                        while True:
                            if _m8 or _sw7 in (9, 10):
                                _m8 = True
                                MpCanvas.bA = 0
                                if MpCanvas.bb > 1:
                                    break
                                self.B_v()
                                return
                            if _m8 or _sw7 in (0, 3, 4, 5, 6, 7):
                                _m8 = True
                                MpCanvas.cL = 1
                                while MpCanvas.cL < 4:
                                    if MpCanvas.bQ[MpCanvas.cL] and (imod(MpCanvas.bR[MpCanvas.cL], 2) != imod(MpCanvas.bR[0], 2)):
                                        MpCanvas.bA = MpCanvas.cL
                                        break
                                    MpCanvas.cL = MpCanvas.cL + 1
                                if MpCanvas.bc > 1:
                                    break
                            if _m8 or _sw7 not in (9, 10, 0, 3, 4, 5, 6, 7):
                                _m8 = True
                                self.B_v()
                            break
                    self.e_v()
                    self.c_G(MpCanvas.e)
                    MpCanvas.j_G(MpCanvas.e)
                    self.d_G(MpCanvas.e)
                    self.d_GI(MpCanvas.e, 1)
                    return
                if _m4 or _sw3 == 97:
                    _m4 = True
                    self.e_v()
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        if MpCanvas.bB > 2:
                            self.c_G(MpCanvas.e)
                            MpCanvas.j_G(MpCanvas.e)
                            self.C_v()
                            return
                        self.c_G(MpCanvas.e)
                        MpCanvas.j_G(MpCanvas.e)
                        MpCanvas.A_v()
                        self.e_G(MpCanvas.e)
                        self.f_G(MpCanvas.e)
                        return
                    if MpCanvas.da > 0:
                        self.c_G(MpCanvas.e)
                        MpCanvas.j_G(MpCanvas.e)
                        self.e_G(MpCanvas.e)
                        self.f_G(MpCanvas.e)
                        return
                    self.c_G(MpCanvas.e)
                    MpCanvas.j_G(MpCanvas.e)
                    self.e_G(MpCanvas.e)
                    self.f_G(MpCanvas.e)
                    return
                if _m4 or _sw3 == 98:
                    _m4 = True
                    self.e_v()
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        self.c_G(MpCanvas.e)
                        MpCanvas.j_G(MpCanvas.e)
                        self.e_G(MpCanvas.e)
                        if (MpCanvas.bB <= 2) and MpCanvas.bt:
                            self.f_G(MpCanvas.e)
                    elif MpCanvas.da == 4:
                        self.c_G(MpCanvas.e)
                        MpCanvas.j_G(MpCanvas.e)
                        self.e_G(MpCanvas.e)
                        self.c_I(1027)
                    else:
                        self.c_G(MpCanvas.e)
                        MpCanvas.j_G(MpCanvas.e)
                        if MpCanvas.da < 4:
                            self.e_G(MpCanvas.e)
                    if MpCanvas.da < 4:
                        break
                    self.d_GI(MpCanvas.e, 2)
                    self.S_v()
                    return
                if _m4 or _sw3 == 99:
                    _m4 = True
                    self.e_v()
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                    self.c_G(MpCanvas.e)
                    self.R_v()
                    if MpCanvas.da < 4:
                        return
                    MpCanvas.bC = 0
                    self.E_v()
                    return
                if _m4 or _sw3 == 100:
                    _m4 = True
                    self.e_v()
                    self.c_G(MpCanvas.e)
                    self.c_GIIIII(MpCanvas.e, MpCanvas.cW, (MpCanvas.cX - 25), 80, 20, 0)
                    self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((MpCanvas.cX - 6) - 25), Consts.eX[8], 0xFFFFFF)
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        return
                    if MpCanvas.da != idiv(1000, MpCanvas.dc):
                        break
                    MpCanvas.i_I(93)
                    return
                if _m4 or _sw3 == 101:
                    _m4 = True
                    self.e_v()
                    self.c_G(MpCanvas.e)
                    self.k_v()
                    MpCanvas.i_I(102)
                    return
                if _m4 or _sw3 == 102:
                    _m4 = True
                    self.e_v()
                    self.s_v()
                    self.R_v()
                    self.I_v()
                    MpCanvas.Q = MpCanvas.Q + 1
                    self.D_v()
                    return
                if _m4 or _sw3 == 103:
                    _m4 = True
                    self.e_v()
                    self.c_G(MpCanvas.e)
                    if MpCanvas.da >= 2:
                        break
                    MpCanvas.da = 2
                    self.c_I(1025)
                    return
                if _m4 or _sw3 == 104:
                    _m4 = True
                    self.e_v()
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.du[0] = None
                        MpCanvas.du[1] = None
                        var1_4 = 0
                        while var1_4 < 3:
                            if MpCanvas.dv[var1_4] is not None:
                                MpCanvas.dv[var1_4].a_v()
                            MpCanvas.dv[var1_4] = None
                            var1_4 = var1_4 + 1
                        var1_4 = 0
                        while var1_4 < 10:
                            MpCanvas.dw[var1_4][0] = None
                            MpCanvas.dw[var1_4][1] = None
                            var2_9 = 0
                            while var2_9 < 3:
                                if MpCanvas.dx[var1_4][var2_9] is not None:
                                    MpCanvas.dx[var1_4][var2_9].a_v()
                                MpCanvas.dx[var1_4][var2_9] = None
                                var2_9 = var2_9 + 1
                            var1_4 = var1_4 + 1
                        var1_4 = 0
                        while var1_4 < 2:
                            MpCanvas.dy[var1_4][0] = None
                            MpCanvas.dy[var1_4][1] = None
                            var2_9 = 0
                            while var2_9 < 3:
                                if MpCanvas.dz[var1_4][var2_9] is not None:
                                    MpCanvas.dz[var1_4][var2_9].a_v()
                                MpCanvas.dz[var1_4][var2_9] = None
                                var2_9 = var2_9 + 1
                            var1_4 = var1_4 + 1
                        MpCanvas.X_v()
                    if MpCanvas.da < idiv(1000, MpCanvas.dc):
                        self.c_G(MpCanvas.e)
                        self.H_v()
                        return
                    if MpCanvas.da == idiv(1000, MpCanvas.dc):
                        self.c_G(MpCanvas.e)
                        MpCanvas.cL = 1
                        while MpCanvas.cL < 4:
                            if MpCanvas.bQ[MpCanvas.cL] and (imod(MpCanvas.bR[MpCanvas.cL], 2) != imod(MpCanvas.bR[0], 2)):
                                MpCanvas.bQ[MpCanvas.cL] = False
                            MpCanvas.cL = MpCanvas.cL + 1
                        MpCanvas.bc = 0
                        self.c_I(1036)
                        MpCanvas.cL = 0
                        while MpCanvas.cL < 4:
                            MpCanvas.cp[MpCanvas.cL] = 99
                            MpCanvas.cq[MpCanvas.cL] = 0
                            MpCanvas.cL = MpCanvas.cL + 1
                        MpCanvas.i_I(90)
                        MpCanvas.O = True
                        return
                    self.c_G(MpCanvas.e)
                    return
                if _m4 or _sw3 == 105:
                    _m4 = True
                    self.e_v()
                    if MpCanvas.da < 5:
                        MpCanvas.da = 5
                        self.i_v()
                        if MpCanvas.aU == 1:
                            self.t_I(5)
                        else:
                            self.t_I(4)
                    if MpCanvas.da < idiv(1500, MpCanvas.dc):
                        MpCanvas.g_G(MpCanvas.e)
                        self.c_G(MpCanvas.e)
                        self.b_GI(MpCanvas.e, 2)
                        return
                    if MpCanvas.da < idiv(1500, MpCanvas.dc):
                        break
                    MpCanvas.g_G(MpCanvas.e)
                    self.c_G(MpCanvas.e)
                    self.P_v()
                    return
                if _m4 or _sw3 == 10:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        var1_5 = 0
                        while var1_5 < len(MpCanvas.de):
                            MpCanvas.de[var1_5] = None
                            var1_5 = var1_5 + 1
                        self.i_v()
                        MpCanvas.c = Consts.eX[9]
                        MpCanvas.k = 6
                        self.U_v()
                    self.e_v()
                    Draw.a_GMIII(MpCanvas.e, MpCanvas.dd[MpCanvas.dU[MpCanvas.dW]], (MpCanvas.cW - 40), (MpCanvas.cX - 59), 0)
                    self.a_GTIIIIZZ(MpCanvas.e, Consts.eM[MpCanvas.dU[MpCanvas.dW]], (MpCanvas.cW - 39), (MpCanvas.cX + 21), 78, 17, False, True)
                    MpCanvas.a_G(MpCanvas.e)
                    if MpCanvas.x:
                        self.v_G(MpCanvas.e)
                        break
                    self.c_II(5, 2)
                    return
                if _m4 or _sw3 == 11:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.c = Consts.eM[0]
                        MpCanvas.k = 3
                        self.U_v()
                    Draw.a_GMIII(MpCanvas.e, MpCanvas.f, 0, 0, 0)
                    self.a_GTIIIIZZ(MpCanvas.e, Consts.eN[MpCanvas.dU[MpCanvas.dW]], (MpCanvas.cW - 39), (MpCanvas.cX - 19), 78, 17, False, True)
                    MpCanvas.a_G(MpCanvas.e)
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 12:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.c = Consts.eM[1]
                        MpCanvas.k = 2
                        self.U_v()
                    self.e_v()
                    self.a_GTIIIIZZ(MpCanvas.e, Consts.eO[MpCanvas.dU[MpCanvas.dW]], (MpCanvas.cW - 45), (MpCanvas.cX - 19), 90, 17, False, True)
                    MpCanvas.a_G(MpCanvas.e)
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 16:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.c = Consts.eM[2]
                        MpCanvas.k = 6
                        self.U_v()
                    self.e_v()
                    self.a_GTIIIIZZ(MpCanvas.e, Consts.eP[MpCanvas.dU[MpCanvas.dW]], (MpCanvas.cW - 45), (MpCanvas.cX - 19), 90, 17, False, True)
                    MpCanvas.a_G(MpCanvas.e)
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 20:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.k = 2
                        self.w_G(MpCanvas.g)
                    self.e_v()
                    MpCanvas.cL = 0
                    while MpCanvas.cL < 2:
                        if MpCanvas.dU[MpCanvas.dW] == MpCanvas.cL:
                            self.c_GIIIII(MpCanvas.e, (MpCanvas.cW - 56), ((MpCanvas.cX - 16) + (MpCanvas.cL * 20)), 111, 14, 3)
                            self.a_GTIIII(MpCanvas.e, Consts.eX[(38 + MpCanvas.cL)], idiv(MpCanvas.cS, 2), ((MpCanvas.cX - 15) + (MpCanvas.cL * 20)), 1, 0xFFFFFF)
                        MpCanvas.cL = MpCanvas.cL + 1
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 21:
                    _m4 = True
                    var1_6 = (MpCanvas.cX - 48)
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.C = 0
                        MpCanvas.bG = ""
                        self.f_GI(MpCanvas.g, var1_6)
                    self.e_v()
                    self.a_GIITI(MpCanvas.e, MpCanvas.cW, (var1_6 + 61), MpCanvas.bG, 0x41FF41)
                    MpCanvas.a_II(MpCanvas.C, (var1_6 + 75))
                    if imod(MpCanvas.da, 4) < 2:
                        var2_10 = MpCanvas.n.a_T(MpCanvas.bG)
                        if len(MpCanvas.bG) == 12:
                            var2_10 = (var2_10 - (MpCanvas.n.a_T("A") * 2))
                        MpCanvas.b_GIIIII(MpCanvas.e, (MpCanvas.cW + idiv(var2_10, 2)), (var1_6 + 71), ((MpCanvas.cW + idiv(var2_10, 2)) + 4), (var1_6 + 71), 0xFFFFFF)
                    if len(MpCanvas.bG) == 0:
                        self.c_II(4, 1)
                        break
                    self.c_II(4, 3)
                    return
                if _m4 or _sw3 == 80:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.c = Consts.eP[0]
                    self.Z_v()
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 81:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.c = Consts.eP[1]
                    self.aa_v()
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 82:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.c = Consts.eP[2]
                        self.p_G(MpCanvas.g)
                    self.e_v()
                    self.ab_v()
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 83:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.c = Consts.eP[3]
                    self.ac_v()
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 84:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.C = 0
                        MpCanvas.da = 2
                        MpCanvas.c = Consts.eP[4]
                        self.q_G(MpCanvas.g)
                    self.e_v()
                    self.r_G(MpCanvas.e)
                    if len(MpCanvas.bG) == 0:
                        self.c_II(4, 1)
                        break
                    self.c_II(4, 3)
                    return
                if _m4 or _sw3 == 88:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.c = Consts.eM[3]
                        MpCanvas.k = 3
                        self.o_G(MpCanvas.g)
                    self.e_v()
                    MpCanvas.cL = 0
                    while MpCanvas.cL < 3:
                        if MpCanvas.dU[MpCanvas.dW] == MpCanvas.cL:
                            self.a_GTIIII(MpCanvas.e, Consts.eW[MpCanvas.cL], (MpCanvas.cW - 28), ((MpCanvas.cX - 15) + (MpCanvas.cL * 19)), 1, 0xFFFFFF)
                            _sw9 = MpCanvas.cL
                            _m10 = False
                            while True:
                                if _m10 or _sw9 == 0:
                                    _m10 = True
                                    self.a_GTIIII(MpCanvas.e, Consts.eW[(3 + MpCanvas.an)], (MpCanvas.cW + 33), (MpCanvas.cX - 15), 1, 0xFFFFFF)
                                    break
                                if _m10 or _sw9 == 1:
                                    _m10 = True
                                    self.a_GTIIII(MpCanvas.e, Consts.eW[(8 + MpCanvas.ap)], (MpCanvas.cW + 33), ((MpCanvas.cX - 15) + (MpCanvas.cL * 19)), 1, 0xFFFFFF)
                                    break
                                if _m10 or _sw9 == 2:
                                    _m10 = True
                                    if MpCanvas.ah_v() > 0:
                                        var2_11 = 0
                                        while var2_11 < MpCanvas.ah_v():
                                            Draw.b_GIIIII(MpCanvas.e, ((MpCanvas.cW + 21) + (5 * var2_11)), ((MpCanvas.cX - 13) + (MpCanvas.cL * 19)), 3, 8, 0xFFFFFF)
                                            var2_11 = var2_11 + 1
                                        break
                                    self.a_GTIIII(MpCanvas.e, Consts.eW[(6 + ((0 if (MpCanvas.ah_v() > 0) else 1)))], (MpCanvas.cW + 33), ((MpCanvas.cX - 15) + (MpCanvas.cL * 19)), 1, 0xFFFFFF)
                                break
                            self.c_GIIIII(MpCanvas.e, (MpCanvas.cW - 58), ((MpCanvas.cX - 16) + (MpCanvas.cL * 19)), 61, 14, 3)
                            self.c_GIIIII(MpCanvas.e, (MpCanvas.cW + 13), ((MpCanvas.cX - 16) + (MpCanvas.cL * 19)), 39, 14, 3)
                            if imod(MpCanvas.da, 4) < 2:
                                MpCanvas.c_IIM((MpCanvas.cW + 6), ((MpCanvas.cX - 13) + (MpCanvas.cL * 19)), MpCanvas.di[1])
                                MpCanvas.b_IIM((MpCanvas.cW + 59), ((MpCanvas.cX - 13) + (MpCanvas.cL * 19)), MpCanvas.di[1])
                        else:
                            _sw11 = MpCanvas.cL
                            _m12 = False
                            while True:
                                if _m12 or _sw11 == 0:
                                    _m12 = True
                                    self.a_GTIIII(MpCanvas.e, Consts.eW[(3 + MpCanvas.an)], (MpCanvas.cW + 33), (MpCanvas.cX - 15), 1, 0x646464)
                                    break
                                if _m12 or _sw11 == 1:
                                    _m12 = True
                                    self.a_GTIIII(MpCanvas.e, Consts.eW[(8 + MpCanvas.ap)], (MpCanvas.cW + 33), ((MpCanvas.cX - 15) + (MpCanvas.cL * 19)), 1, 0x646464)
                                    break
                                if _m12 or _sw11 == 2:
                                    _m12 = True
                                    if MpCanvas.ah_v() > 0:
                                        var2_11 = 0
                                        while var2_11 < MpCanvas.ah_v():
                                            Draw.b_GIIIII(MpCanvas.e, ((MpCanvas.cW + 21) + (5 * var2_11)), ((MpCanvas.cX - 13) + (MpCanvas.cL * 19)), 3, 8, 0x646464)
                                            var2_11 = var2_11 + 1
                                        break
                                    self.a_GTIIII(MpCanvas.e, Consts.eW[(6 + ((0 if (MpCanvas.ah_v() > 0) else 1)))], (MpCanvas.cW + 33), ((MpCanvas.cX - 15) + (MpCanvas.cL * 19)), 1, 0x646464)
                                break
                        MpCanvas.cL = MpCanvas.cL + 1
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 7:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.c = Consts.eX[64]
                        self.k_G(MpCanvas.g)
                    self.e_v()
                    self.c_GIIIII(MpCanvas.e, MpCanvas.cW, MpCanvas.cX, 112, 48, 0)
                    self.a_GIITI(MpCanvas.e, MpCanvas.cW, (MpCanvas.cX - 18), _js(Consts.eX[64], "!"), 0xFFFFFF)
                    self.a_GIITI(MpCanvas.e, MpCanvas.cW, (MpCanvas.cX - 6), MpCanvas.i, 0xFFFFFF)
                    self.r_I((MpCanvas.cX + 9))
                    return
                if _m4 or _sw3 == 6:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.c = Consts.eX[18]
                        self.k_G(MpCanvas.g)
                    self.r_v()
                    return
                if _m4 or _sw3 == 3:
                    _m4 = True
                    self.e_v()
                    if MpCanvas.da > idiv(20000, MpCanvas.dc):
                        MpCanvas.cw = 7
                        self.o_v()
                        return
                    self.ae_v()
                    return
                if _m4 or _sw3 == 10000:
                    _m4 = True
                    self.e_v()
                    if MpCanvas.da == 1:
                        self.m_v()
                    if MpCanvas.da > idiv(20000, MpCanvas.dc):
                        MpCanvas.cw = 7
                        self.o_v()
                        return
                    self.ae_v()
                    return
                if _m4 or _sw3 == 4:
                    _m4 = True
                    self.e_v()
                    self.ad_v()
                    if MpCanvas.x:
                        self.v_G(MpCanvas.e)
                        break
                    if (MpCanvas.cw == 7) or (MpCanvas.cw == 1):
                        self.c_II(5, 2)
                    return
                if _m4 or _sw3 == 5:
                    _m4 = True
                    Draw.b_GIIIII(MpCanvas.e, 0, 0, MpCanvas.cQ, MpCanvas.cR, 0)
                    self.c_GIIIII(MpCanvas.e, MpCanvas.cW, MpCanvas.cX, 120, 100, 0)
                    self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((MpCanvas.cX - 21) - 10), Consts.eX[35], 0xFFFFFF)
                    self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((MpCanvas.cX - 21) + 5), Consts.eX[36], 0xFFFFFF)
                    MpCanvas.cL = 0
                    while MpCanvas.cL < 2:
                        if MpCanvas.dU[MpCanvas.dW] == MpCanvas.cL:
                            self.a_GTIIII(MpCanvas.e, Consts.eX[(40 + MpCanvas.cL)], ((MpCanvas.cW - 28) + (MpCanvas.cL * 55)), (MpCanvas.cX + 28), 1, 0xFFFFFF)
                            self.c_GIIIII(MpCanvas.e, ((MpCanvas.cW - 42) + (MpCanvas.cL * 55)), (MpCanvas.cX + 25), 29, 14, 3)
                        else:
                            self.c_GIIIII(MpCanvas.e, ((MpCanvas.cW - 42) + (MpCanvas.cL * 55)), (MpCanvas.cX + 25), 29, 14, 2)
                            self.a_GTIIII(MpCanvas.e, Consts.eX[(40 + MpCanvas.cL)], ((MpCanvas.cW - 28) + (MpCanvas.cL * 55)), (MpCanvas.cX + 28), 1, 0x646464)
                        MpCanvas.cL = MpCanvas.cL + 1
                    return
                if _m4 or _sw3 == 1:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        var2_12 = idiv(((MpCanvas.cT - 320)), 2)
                        var3_15 = 0
                        while var3_15 < 4:
                            MpCanvas.dp = self.b_T(_js(_js("/title_", ((var3_15 + 1))), ".png"))
                            Draw.a_GMIII(MpCanvas.g, MpCanvas.dp, (MpCanvas.cW - idiv(MpCanvas.dp.getWidth(), 2)), (var2_12 + (80 * var3_15)), 0)
                            MpCanvas.dp = None
                            var3_15 = var3_15 + 1
                        if MpCanvas.dr is None:
                            MpCanvas.dr = self.b_T("/gamevil.png")
                        Draw.a_GMIII(MpCanvas.g, MpCanvas.dr, idiv(MpCanvas.cQ, 2), (MpCanvas.cR - 1), 33)
                        if MpCanvas.dq is None:
                            MpCanvas.dq = self.b_T("/press.png")
                    self.e_v()
                    if imod(MpCanvas.da, 4) >= 2:
                        break
                    Draw.a_GMIII(MpCanvas.e, MpCanvas.dq, idiv(MpCanvas.cQ, 2), (MpCanvas.cR - 27), 33)
                    return
                if _m4 or _sw3 == 2:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.bG = ""
                        self.i_v()
                        MpCanvas.c = Consts.eV[0]
                        self.l_G(MpCanvas.g)
                    self.e_v()
                    self.M_v()
                    return
                if _m4 or _sw3 == 160:
                    _m4 = True
                    self.e_v()
                    _sw13 = MpCanvas.al
                    _m14 = False
                    while True:
                        if _m14 or _sw13 == 0:
                            _m14 = True
                            MpCanvas.bJ = len(MpCanvas.ag)
                            self.c_GIIIII(MpCanvas.e, MpCanvas.cW, MpCanvas.cX, ((MpCanvas.bJ * 7) + 6), 45, 0)
                            self.a_IITI(MpCanvas.cW, (MpCanvas.cX - 13), MpCanvas.ag, 16400640)
                            self.a_IITI(MpCanvas.cW, (MpCanvas.cX + 2), MpCanvas.ah, 16400640)
                            raise _Brk_block1_457()
                        if _m14 or _sw13 == 1:
                            _m14 = True
                            self.c_GIIIII(MpCanvas.e, MpCanvas.cW, MpCanvas.cX, 120, 100, 0)
                            self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((MpCanvas.cX - 21) - 10), MpCanvas.ag, 16400640)
                            self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((MpCanvas.cX - 21) + 5), MpCanvas.ah, 16400640)
                            self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((MpCanvas.cX - 21) + 20), Consts.eX[19], 16400640)
                            MpCanvas.cL = 0
                            while MpCanvas.cL < 2:
                                if MpCanvas.dU[MpCanvas.dW] == MpCanvas.cL:
                                    self.a_GTIIII(MpCanvas.e, Consts.eX[(40 + MpCanvas.cL)], ((MpCanvas.cW - 28) + (MpCanvas.cL * 55)), (MpCanvas.cX + 28), 1, 16400640)
                                    self.c_GIIIII(MpCanvas.e, ((MpCanvas.cW - 42) + (MpCanvas.cL * 55)), (MpCanvas.cX + 25), 29, 14, 3)
                                else:
                                    self.c_GIIIII(MpCanvas.e, ((MpCanvas.cW - 42) + (MpCanvas.cL * 55)), (MpCanvas.cX + 25), 29, 14, 2)
                                    self.a_GTIIII(MpCanvas.e, Consts.eX[(40 + MpCanvas.cL)], ((MpCanvas.cW - 28) + (MpCanvas.cL * 55)), (MpCanvas.cX + 28), 1, 0xFFFFFF)
                                MpCanvas.cL = MpCanvas.cL + 1
                            raise _Brk_block1_457()
                        if _m14 or _sw13 == 2:
                            _m14 = True
                            self.c_GIIIII(MpCanvas.e, MpCanvas.cW, MpCanvas.cX, 120, 100, 0)
                            self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((MpCanvas.cX - 26) - 10), MpCanvas.ag, 16400640)
                            self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((MpCanvas.cX - 26) + 5), MpCanvas.ah, 16400640)
                            self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((MpCanvas.cX - 26) + 20), MpCanvas.ai, 16400640)
                            self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((MpCanvas.cX - 26) + 35), MpCanvas.aj, 16400640)
                            self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((MpCanvas.cX - 26) + 50), MpCanvas.ak, 16400640)
                        if _m14 or _sw13 not in (0, 1, 2):
                            _m14 = True
                            return
                        break
                if _m4 or _sw3 == 300:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.n_v()
                        self.ag_v()
                        MpCanvas.ds = self.b_T("/outro.png")
                    Draw.b_GIIIII(MpCanvas.e, 0, 0, MpCanvas.cS, MpCanvas.cT, 0)
                    var2_13 = MpCanvas.ds.getWidth()
                    Gfx.a_MIIIIII(MpCanvas.ds, (MpCanvas.cW - idiv(var2_13, 2)), (MpCanvas.cX - 10), var2_13, 19, 0, 0)
                    Gfx.a_MIIIIII(MpCanvas.ds, (MpCanvas.cW - idiv(var2_13, 2)), (MpCanvas.cT - 26), var2_13, 23, 0, 19)
                    if MpCanvas.da <= 30:
                        break
                    MpCanvas.l.destroyApp(True)
                    MpCanvas.l.notifyDestroyed()
                    return
                if _m4 or _sw3 == 87:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.c = Consts.eM[4]
                        MpCanvas.k = 6
                        self.U_v()
                    self.e_v()
                    self.a_GTIIIIZZ(MpCanvas.e, Consts.eQ[MpCanvas.dU[MpCanvas.dW]], (MpCanvas.cW - 39), (MpCanvas.cX - 19), 78, 17, False, True)
                    MpCanvas.a_G(MpCanvas.e)
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 89:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.be = 0
                    self.T_v()
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 85:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        _sw15 = MpCanvas.cY
                        if _sw15 == 85:
                            MpCanvas.c = Consts.eP[5]
                        self.s_G(MpCanvas.g)
                    self.e_v()
                    self.t_G(MpCanvas.e)
                    if len(MpCanvas.bG) == 0:
                        self.c_II(4, 1)
                        break
                    self.c_II(4, 3)
                    return
                if _m4 or _sw3 == 86:
                    _m4 = True
                    if MpCanvas.da < 2:
                        MpCanvas.da = 2
                        MpCanvas.k = 2
                    self.e_v()
                    self.t_G(MpCanvas.e)
                    self.u_G(MpCanvas.e)
                break
        except _Brk_block1_457:
            pass

    @staticmethod
    def b_I(n2):  # g.java:1467
        MpCanvas.d = n2

    def a_GIITI(self, graphics, n2, n3, string, n4):  # g.java:1471
        self.a_GTIIII(graphics, string, n2, n3, 1, n4)

    def a_IITI(self, n2, n3, string, n4):  # g.java:1475
        self.a_GTIIII(MpCanvas.e, string, n2, n3, 1, n4)

    def b_GIITI(self, graphics, n2, n3, string, n4):  # g.java:1479
        self.a_GTIIII(graphics, string, n2, n3, 0, n4)

    def b_IITI(self, n2, n3, string, n4):  # g.java:1483
        self.a_GTIIII(MpCanvas.e, string, n2, n3, 0, n4)

    def a_GTIIII(self, graphics, string, n2, n3, n4, n5):  # g.java:1487
        _sw16 = n5
        if _sw16 == 0xFFFFFF:
            Gfx.a_Lj(MpCanvas.n)
        elif _sw16 == 16400640:
            Gfx.a_Lj(MpCanvas.o)
        elif _sw16 == 0x646464:
            Gfx.a_Lj(MpCanvas.p)
        elif _sw16 == 0x41FF41:
            Gfx.a_Lj(MpCanvas.q)
        else:
            MpCanvas.a_T(_js("=======================drawString: No Color:", n5))
        Gfx.a_GTIII(graphics, string, n2, n3, n4)

    @staticmethod
    def a_IIIII(n2, n3, n4, n5, n6):  # g.java:1512
        Draw.a_GIIIII(MpCanvas.e, n2, n3, n4, n5, n6)

    @staticmethod
    def b_IIIII(n2, n3, n4, n5, n6):  # g.java:1516
        Draw.b_GIIIII(MpCanvas.e, n2, n3, n4, n5, n6)

    @staticmethod
    def a_GIIIII(graphics, n2, n3, n4, n5, n6):  # g.java:1520
        Draw.b_GIIIII(graphics, n2, n3, n4, n5, n6)

    @staticmethod
    def a_GI(graphics, n2):  # g.java:1524
        graphics.setColor(n2)

    @staticmethod
    def b_GIIIII(graphics, n2, n3, n4, n5, n6):  # g.java:1528
        Draw.c_GIIIII(graphics, n2, n3, n4, n5, n6)

    @staticmethod
    def a_GIIII(graphics, n2, n3, n4, n5):  # g.java:1532
        Draw.c_GIIII(graphics, n2, n3, n4, n5)

    @staticmethod
    def a_GIII(graphics, n2, n3, n4):  # g.java:1536
        Draw.b_GIIIII(graphics, n2, n3, 1, 1, n4)

    @staticmethod
    def a_IIM(n2, n3, image):  # g.java:1540
        Draw.a_GMIII(MpCanvas.e, image, n2, n3, 0)

    @staticmethod
    def a_GIIM(graphics, n2, n3, image):  # g.java:1544
        Draw.a_GMIII(graphics, image, n2, n3, 0)

    @staticmethod
    def b_IIM(n2, n3, image):  # g.java:1548
        n4 = (idiv(image.getWidth(), 2) + 1)
        n5 = image.getHeight()
        Draw.a_GMIIIIII(MpCanvas.e, image, (n2 - n4), n3, n4, n5, (n4 - 1), 0)

    @staticmethod
    def b_GIIM(graphics, n2, n3, image):  # g.java:1554
        n4 = (idiv(image.getWidth(), 2) + 1)
        n5 = image.getHeight()
        Draw.a_GMIIIIII(graphics, image, (n2 - n4), n3, n4, n5, (n4 - 1), 0)

    @staticmethod
    def a_GIIIM(graphics, n2, n3, n4, image):  # g.java:1560
        n5 = (idiv(image.getWidth(), 2) + 1)
        Draw.a_GMIIIIII(graphics, image, (n2 - n5), n3, n5, n4, (n5 - 1), 0)

    @staticmethod
    def a_IIMZ(n2, n3, image, bl):  # g.java:1565
        if bl:
            n4 = (idiv(image.getWidth(), 2) + 1)
            n5 = image.getHeight()
            Draw.a_GMIIIIII(MpCanvas.e, image, (n2 - n4), n3, n4, n5, (n4 - 1), 0)
            return
        Draw.a_GMIII(MpCanvas.e, image, (n2 - image.getWidth()), n3, 0)

    @staticmethod
    def a_GIIMII(graphics, n2, n3, image, n4, n5):  # g.java:1575
        n6 = (idiv(image.getWidth(), 2) + 1)
        Draw.a_GMIIIIII(graphics, image, n2, n3, n6, n4, 0, (n4 * n5))

    @staticmethod
    def b_GIIIM(graphics, n2, n3, n4, image):  # g.java:1580
        n5 = (idiv(image.getWidth(), 2) + 1)
        Draw.a_GMIIIIII(graphics, image, (n2 - n5), n3, n5, n4, (n5 - 1), n4)

    @staticmethod
    def c_IIM(n2, n3, image):  # g.java:1585
        n4 = (idiv(image.getWidth(), 2) + 1)
        n5 = image.getHeight()
        Draw.a_GMIIIIII(MpCanvas.e, image, n2, n3, n4, n5, 0, 0)

    @staticmethod
    def c_GIIM(graphics, n2, n3, image):  # g.java:1591
        n4 = (idiv(image.getWidth(), 2) + 1)
        n5 = image.getHeight()
        Draw.a_GMIIIIII(graphics, image, n2, n3, n4, n5, 0, 0)

    @staticmethod
    def c_GIIIM(graphics, n2, n3, n4, image):  # g.java:1597
        n5 = (idiv(image.getWidth(), 2) + 1)
        Draw.a_GMIIIIII(graphics, image, n2, n3, n5, n4, 0, 0)

    def e_v(self):  # g.java:1602
        Draw.a_GMIII(MpCanvas.e, MpCanvas.f, 0, 0, 0)
        if (MpCanvas.cY >= 90) and (MpCanvas.cY <= 105):
            MpCanvas.g_G(MpCanvas.e)

    def c_I(self, n2):  # g.java:1609
        if (n2 == 262) or (n2 == 278):
            MpCanvas.N = system.currentTimeMillis()
        if NetThread.j and (idiv(((system.currentTimeMillis() - MpCanvas.N)), 1000) > 45):
            MpCanvas.dZ = 0
            MpCanvas.cw = 13
            MpCanvas.x = False
            self.o_v()
            MpCanvas.N = system.currentTimeMillis()
            return
        MpCanvas.N = system.currentTimeMillis()
        MpCanvas.dR = 0
        MpCanvas.dQ = n2
        MpCanvas.dP.a_I(MpCanvas.dQ)
        _sw17 = MpCanvas.dQ
        if _sw17 == 1300:
            NetThread.a_B(i8(((MpCanvas.ae + 1))))
        elif _sw17 == 1293:
            NetThread.a_B(i8(MpCanvas.ab))
            NetThread.b_I(1)
        elif _sw17 == 256:
            NetThread.b_TI(MpCanvas.i, 12)
            NetThread.b_TI(MpCanvas.t, 4)
        elif _sw17 == 262:
            NetThread.b_TI(MpCanvas.i, 12)
            NetThread.b_TI(MpCanvas.t, 4)
        elif _sw17 == 278:
            NetThread.b_TI(MpCanvas.i, 12)
            NetThread.b_TI(MpCanvas.j, 16)
            NetThread.b_TI(MpCanvas.t, 4)
        elif _sw17 == 512:
            NetThread.a_B(MpCanvas.bz)
        elif _sw17 == 1291:
            MpCanvas.cM = 0
            MpCanvas.cL = 0
            while MpCanvas.cL < 4:
                if MpCanvas.cH[(MpCanvas.cB[MpCanvas.cL] - 3)] != 99:
                    NetThread.a_B(MpCanvas.cB[MpCanvas.cL])
                    MpCanvas.cM = MpCanvas.cM + 1
                MpCanvas.cL = MpCanvas.cL + 1
            MpCanvas.cL = MpCanvas.cM
            while MpCanvas.cL < 4:
                NetThread.a_B(i8(99))
                MpCanvas.cL = MpCanvas.cL + 1
        elif _sw17 == 1280:
            NetThread.b_TI(MpCanvas.bG, 8)
        elif _sw17 == 258:
            NetThread.b_I(MpCanvas.aO)
        elif _sw17 == 1027:
            NetThread.a_B(i8(MpCanvas.bR[MpCanvas.bA]))
            NetThread.a_B(i8(MpCanvas.bB))
            NetThread.a_B(i8(MpCanvas.aS))
        elif _sw17 in (1282, 1284):
            NetThread.b_TI(MpCanvas.bG, 20)
        elif _sw17 == 768:
            NetThread.a_B(MpCanvas.bz)
            NetThread.b_TI(MpCanvas.bG, 12)
        elif _sw17 == 288:
            pass
        elif _sw17 == 290:
            NetThread.b_I(MpCanvas.ap)
        NetThread.b_v()

    def f_v(self):  # g.java:1706
        MpCanvas.df[2] = self.b_T("/ui2.png")
        MpCanvas.df[3] = self.b_T("/ui3.png")
        MpCanvas.df[15] = self.b_T("/ui15.png")
        MpCanvas.df[16] = self.b_T("/ui16.png")
        MpCanvas.df[17] = self.b_T("/ui17.png")
        MpCanvas.df[18] = self.b_T("/ui18.png")
        MpCanvas.df[19] = self.b_T("/ui19.png")
        n2 = 0
        while n2 < 6:
            MpCanvas.dg[n2] = self.b_T(_js(_js("/act", n2), ".png"))
            n2 = n2 + 1
        MpCanvas.di[1] = self.b_T("/menuarrow1.png")
        n3 = 0
        while n3 < 8:
            MpCanvas.dh[n3] = self.b_T(_js(_js("/gnum", n3), ".png"))
            n3 = n3 + 1
        self.h_v()

    def g_v(self):  # g.java:1728
        MpCanvas.df[34] = self.b_T("/ui34.png")
        MpCanvas.df[35] = self.b_T("/ui35.png")
        MpCanvas.df[36] = self.b_T("/ui36.png")
        MpCanvas.df[37] = self.b_T("/ui37.png")
        MpCanvas.df[38] = self.b_T("/ui38.png")
        MpCanvas.df[48] = self.b_T("/ui48.png")
        MpCanvas.df[49] = self.b_T("/ui49.png")
        MpCanvas.df[52] = self.b_T("/ui52.png")
        MpCanvas.df[53] = self.b_T("/ui53.png")

    def h_v(self):  # g.java:1740
        n2 = 0
        while n2 < 6:
            if MpCanvas.dd[n2] is None:
                MpCanvas.dd[n2] = self.b_T(_js(_js("/mpic", n2), ".png"))
            n2 = n2 + 1
        if MpCanvas.dm is None:
            MpCanvas.dm = self.b_T("/ui_borderh.png")
        if MpCanvas.dk is None:
            MpCanvas.dk = self.b_T("/ui_borderv.png")
        if MpCanvas.dn is None:
            MpCanvas.dn = self.b_T("/ui_titlebox.png")
        if MpCanvas.dl is None:
            MpCanvas.dl = self.b_T("/ui_back.png")
        if MpCanvas.do_ is None:
            MpCanvas.do_ = self.b_T("/ui_menuicon.png")

    def i_v(self):  # g.java:1765
        n2 = 0
        MpCanvas.du[0] = None
        MpCanvas.du[1] = None
        n3 = 0
        while n3 < 3:
            if MpCanvas.dv[n3] is not None:
                MpCanvas.dv[n3].a_v()
            MpCanvas.dv[n3] = None
            n3 = n3 + 1
        n3 = 0
        while n3 < 10:
            MpCanvas.dw[n3][0] = None
            MpCanvas.dw[n3][1] = None
            n2 = 0
            while n2 < 3:
                if MpCanvas.dx[n3][n2] is not None:
                    MpCanvas.dx[n3][n2].a_v()
                MpCanvas.dx[n3][n2] = None
                n2 = n2 + 1
            n3 = n3 + 1
        n3 = 0
        while n3 < 2:
            MpCanvas.dy[n3][0] = None
            MpCanvas.dy[n3][1] = None
            n2 = 0
            while n2 < 3:
                if MpCanvas.dz[n3][n2] is not None:
                    MpCanvas.dz[n3][n2].a_v()
                MpCanvas.dz[n3][n2] = None
                n2 = n2 + 1
            n3 = n3 + 1
        n3 = 0
        while n3 < 2:
            MpCanvas.dA[n3][0] = None
            MpCanvas.dA[n3][1] = None
            n2 = 0
            while n2 < 3:
                if MpCanvas.dB[n3][n2] is not None:
                    MpCanvas.dB[n3][n2].a_v()
                MpCanvas.dB[n3][n2] = None
                n2 = n2 + 1
            n3 = n3 + 1
        n3 = 0
        while n3 < 2:
            MpCanvas.dC[n3][0] = None
            MpCanvas.dC[n3][1] = None
            n2 = 0
            while n2 < 3:
                if MpCanvas.dD[n3][n2] is not None:
                    MpCanvas.dD[n3][n2].a_v()
                MpCanvas.dD[n3][n2] = None
                n2 = n2 + 1
            n3 = n3 + 1
        MpCanvas.dF[0] = None
        MpCanvas.dF[1] = None
        n3 = 0
        while n3 < 3:
            if MpCanvas.dG[n3] is not None:
                MpCanvas.dG[n3].a_v()
            MpCanvas.dG[n3] = None
            n3 = n3 + 1
        MpCanvas.dH[0] = None
        MpCanvas.dH[1] = None
        if MpCanvas.dI[0] is not None:
            MpCanvas.dI[0].a_v()
        MpCanvas.dI[0] = None
        MpCanvas.dJ[0] = None
        MpCanvas.dJ[1] = None
        if MpCanvas.dK[0] is not None:
            MpCanvas.dK[0].a_v()
        MpCanvas.dK[0] = None
        MpCanvas.dL[0] = None
        MpCanvas.dL[1] = None
        if MpCanvas.dM[0] is not None:
            MpCanvas.dM[0].a_v()
        MpCanvas.dM[0] = None
        MpCanvas.dN[0] = None
        MpCanvas.dN[0] = None
        if MpCanvas.dO[0] is not None:
            MpCanvas.dO[0].a_v()
        MpCanvas.dO[0] = None
        n3 = 2
        while n3 < len(MpCanvas.dg):
            MpCanvas.dg[n3] = None
            n3 = n3 + 1
        MpCanvas.df[34] = None
        MpCanvas.df[35] = None
        MpCanvas.df[36] = None
        MpCanvas.df[37] = None
        MpCanvas.df[38] = None
        MpCanvas.df[48] = None
        MpCanvas.df[49] = None
        MpCanvas.df[52] = None
        MpCanvas.df[53] = None
        MpCanvas.X_v()
        if MpCanvas.di[1] is None:
            MpCanvas.di[1] = self.b_T("/menuarrow1.png")
        self.h_v()

    def a_Lk(self, k2):  # g.java:1888
        MpCanvas.u = False
        if MpCanvas.J or (MpCanvas.H == 1):
            MpCanvas.cw = 7
            MpCanvas.x = False
            MpCanvas.n_v()
            MpCanvas.b_I((-1))
            self.k_I(4)
            return
        if NetThread.a == 280:
            MpCanvas.cw = 17
            MpCanvas.x = False
            MpCanvas.n_v()
            self.k_I(4)
            return
        if not NetThread.j:
            return
        s = k2.b_v()
        by = k2.a_v()
        MpCanvas.dR = by
        _sw18 = s
        try:
            _m19 = False
            while True:
                if _m19 or _sw18 == 279:
                    _m19 = True
                    if MpCanvas.dR == 1:
                        MpCanvas.K_v()
                        self.o_v()
                        MpCanvas.cv = 0
                        MpCanvas.A = False
                        MpCanvas.i_I(10000)
                        return
                    by2 = k2.a_v()
                    self.o_v()
                    if by2 == 0:
                        MpCanvas.z = 0
                        MpCanvas.cw = 14
                    elif by2 == 1:
                        MpCanvas.z = 1
                        MpCanvas.cw = 15
                    else:
                        MpCanvas.z = 0
                        MpCanvas.cw = 0
                    self.k_I(4)
                    return
                if _m19 or _sw18 == 263:
                    _m19 = True
                    _sw20 = MpCanvas.dR
                    if _sw20 == 1:
                        MpCanvas.cE = k2.a_I(8)
                        MpCanvas.ar = k2.a_v()
                        MpCanvas.as_ = k2.b_v()
                        MpCanvas.at = k2.c()
                        MpCanvas.au = k2.c()
                        MpCanvas.av = k2.b_v()
                        k2.b_v()
                        k2.b_v()
                        MpCanvas.aw = k2.a_v()
                        MpCanvas.bE[0] = k2.a_v()
                        MpCanvas.bE[1] = k2.a_v()
                        MpCanvas.bE[2] = k2.a_v()
                        MpCanvas.bE[3] = k2.a_v()
                        MpCanvas.bD = 0
                        MpCanvas.cL = 0
                        while MpCanvas.cL < 4:
                            if MpCanvas.bE[MpCanvas.cL] != 99:
                                MpCanvas.bD = MpCanvas.bD + 1
                            MpCanvas.cL = MpCanvas.cL + 1
                        MpCanvas.cF = MpCanvas.d_T(k2.a_I(20))
                        MpCanvas.cG = MpCanvas.d_T(k2.a_I(20))
                        MpCanvas.cL = 0
                        while MpCanvas.cL < 11:
                            MpCanvas.cI[MpCanvas.cL] = k2.a_v()
                            MpCanvas.cL = MpCanvas.cL + 1
                        MpCanvas.aK = k2.a_v()
                        MpCanvas.aL = k2.a_v()
                        MpCanvas.aM = k2.a_v()
                        if MpCanvas.aL < 0:
                            MpCanvas.aL = 0
                        if MpCanvas.aM < 0:
                            MpCanvas.aM = 0
                        MpCanvas.aN = k2.a_v()
                        k2.a_I(8)
                        k2.a_I(8)
                        k2.a_v()
                        k2.a_v()
                        k2.a_v()
                        MpCanvas.dp = None
                        MpCanvas.dq = None
                        MpCanvas.dr = None
                        MpCanvas.X_v()
                        if MpCanvas.dX:
                            if MpCanvas.P:
                                self.l_I(7)
                                return
                            self.l_I(10)
                            return
                        if MpCanvas.aN > 0:
                            MpCanvas.aO = 1
                            self.c_I(258)
                            return
                        MpCanvas.aN = 0
                        self.l_I(7)
                        return
                    elif _sw20 == (-2):
                        MpCanvas.cw = 1
                        self.o_v()
                        return
                    elif _sw20 == (-9):
                        MpCanvas.cw = 8
                        self.o_v()
                        return
                    MpCanvas.cw = 7
                    MpCanvas.x = False
                    MpCanvas.n_v()
                    self.k_I(4)
                    return
                if _m19 or _sw18 == 1286:
                    _m19 = True
                    _sw21 = MpCanvas.bz
                    _m22 = False
                    while True:
                        if _m22 or _sw21 in (0, 1):
                            _m22 = True
                            MpCanvas.i_I(11)
                            raise _Brk_block0_1631()
                        if _m22 or _sw21 == 2:
                            _m22 = True
                            MpCanvas.i_I(12)
                        break
                    return
                if _m19 or _sw18 == 1301:
                    _m19 = True
                    _sw23 = MpCanvas.dR
                    _m24 = False
                    while True:
                        if _m24 or _sw23 == 1:
                            _m24 = True
                            MpCanvas.ac[MpCanvas.ae] = k2.c()
                            MpCanvas.ad = k2.c()
                            self.k_I(((161 + MpCanvas.dU[MpCanvas.dW]) + 1))
                            raise _Brk_block0_1631()
                        if _m24 or _sw23 == (-1):
                            _m24 = True
                            MpCanvas.cw = 0
                            self.k_I(4)
                        break
                    return
                if _m19 or _sw18 == 1294:
                    _m19 = True
                    _sw25 = MpCanvas.dR
                    _m26 = False
                    while True:
                        if _m26 or _sw25 == 1:
                            _m26 = True
                            n2 = k2.a_v()
                            n3 = 0
                            while n3 < n2:
                                MpCanvas.Z[n3] = k2.c()
                                MpCanvas.Y[n3] = k2.a_I(12)
                                MpCanvas.aa[n3] = k2.c()
                                n3 = n3 + 1
                            self.k_I((170 + MpCanvas.dU[MpCanvas.dW]))
                            raise _Brk_block0_1631()
                        if _m26 or _sw25 == (-1):
                            _m26 = True
                            MpCanvas.cw = 0
                            self.k_I(4)
                        break
                    return
                if _m19 or _sw18 == 259:
                    _m19 = True
                    _sw27 = MpCanvas.dR
                    if _sw27 == 1:
                        n4 = 0
                        while n4 < 4:
                            MpCanvas.bF[n4] = k2.a_I(16)
                            n4 = n4 + 1
                        MpCanvas.aN = k2.a_v()
                        MpCanvas.bd = 1
                        MpCanvas.i_I(6)
                        return
                    MpCanvas.cw = 0
                    self.k_I(4)
                    return
                if _m19 or _sw18 == 513:
                    _m19 = True
                    _sw28 = MpCanvas.dR
                    if _sw28 == 1:
                        MpCanvas.by = k2.a_v()
                        MpCanvas.bh = k2.a_v()
                        MpCanvas.bz = k2.a_v()
                        k2.a_v()
                        MpCanvas.w = True
                        self.O_v()
                        MpCanvas.w = False
                        MpCanvas.O = True
                        return
                    MpCanvas.cw = 0
                    _sw29 = MpCanvas.dR
                    if _sw29 == (-11):
                        MpCanvas.cw = 8
                    self.k_I(4)
                    return
                if _m19 or _sw18 == 769:
                    _m19 = True
                    _sw30 = MpCanvas.dR
                    if _sw30 == 1:
                        MpCanvas.by = k2.a_v()
                        MpCanvas.bh = k2.a_v()
                        MpCanvas.bz = k2.a_v()
                        k2.a_v()
                        MpCanvas.w = True
                        self.O_v()
                        MpCanvas.w = False
                        MpCanvas.O = True
                        return
                    _sw31 = MpCanvas.dR
                    if _sw31 == (-3):
                        MpCanvas.cw = 2
                    elif _sw31 == (-4):
                        MpCanvas.cw = 3
                    elif _sw31 == (-5):
                        MpCanvas.cw = 4
                    elif _sw31 == (-12):
                        MpCanvas.cw = 9
                    elif _sw31 == (-16):
                        MpCanvas.cw = 18
                    else:
                        MpCanvas.cw = 0
                    self.k_I(4)
                    return
                if _m19 or _sw18 == 770:
                    _m19 = True
                    _sw32 = MpCanvas.dR
                    if _sw32 == 1:
                        MpCanvas.x = False
                        MpCanvas.by = k2.a_v()
                        MpCanvas.bh = k2.a_v()
                        MpCanvas.bz = k2.a_v()
                        k2.a_v()
                        MpCanvas.w = True
                        self.O_v()
                        MpCanvas.w = False
                        MpCanvas.O = True
                        return
                    MpCanvas.cw = 0
                    self.k_I(4)
                    return
                if _m19 or _sw18 == 514:
                    _m19 = True
                    _sw33 = MpCanvas.dR
                    if _sw33 == 1:
                        MpCanvas.cL = 0
                        while MpCanvas.cL < 4:
                            if not MpCanvas.bQ[MpCanvas.cL]:
                                MpCanvas.ct = MpCanvas.cL
                                break
                            MpCanvas.cL = MpCanvas.cL + 1
                        MpCanvas.bQ[MpCanvas.ct] = True
                        MpCanvas.bR[MpCanvas.ct] = k2.a_v()
                        if imod(MpCanvas.bR[MpCanvas.ct], 2) == imod(MpCanvas.bR[0], 2):
                            MpCanvas.bb = MpCanvas.bb + 1
                        else:
                            MpCanvas.bc = MpCanvas.bc + 1
                        MpCanvas.bM[MpCanvas.ct] = k2.a_I(8)
                        MpCanvas.bS[MpCanvas.ct] = k2.b_v()
                        MpCanvas.bT[MpCanvas.ct] = k2.c()
                        MpCanvas.bU[MpCanvas.ct] = k2.c()
                        MpCanvas.bW[MpCanvas.ct] = k2.b_v()
                        MpCanvas.bV[MpCanvas.ct] = MpCanvas.bW[MpCanvas.ct]
                        MpCanvas.bY[MpCanvas.ct] = k2.a_v()
                        MpCanvas.bZ[MpCanvas.ct] = k2.a_v()
                        if MpCanvas.bZ[MpCanvas.ct] == 10:
                            MpCanvas.bZ[MpCanvas.ct] = 0
                            MpCanvas.ca[MpCanvas.ct] = 2
                        elif MpCanvas.bZ[MpCanvas.ct] < 10:
                            MpCanvas.ca[MpCanvas.ct] = 0
                        else:
                            n5 = MpCanvas.ct
                            MpCanvas.bZ[n5] = i8(((MpCanvas.bZ[n5] - 30)))
                            MpCanvas.ca[MpCanvas.ct] = 1
                        MpCanvas.bN[MpCanvas.ct] = k2.a_I(20)
                        MpCanvas.bO[MpCanvas.ct] = k2.a_I(20)
                        MpCanvas.cr[MpCanvas.ct] = k2.a_v()
                        MpCanvas.bP[MpCanvas.ct] = k2.a_I(8)
                        MpCanvas.bX[MpCanvas.ct] = 0
                        MpCanvas.h_I(MpCanvas.ct)
                        MpCanvas.co[MpCanvas.ct] = imod(abs(MpCanvas.h.nextInt()), 4)
                        MpCanvas.cp[MpCanvas.ct] = 99
                        MpCanvas.cq[MpCanvas.ct] = 0
                        MpCanvas.bj = True
                        if MpCanvas.cY != 4:
                            break
                        MpCanvas.i_I(90)
                        MpCanvas.O = True
                        return
                    MpCanvas.cw = 0
                    self.k_I(4)
                    return
                if _m19 or _sw18 == 1024:
                    _m19 = True
                    _sw34 = MpCanvas.dR
                    if _sw34 == 1:
                        MpCanvas.i_I(92)
                    return
                if _m19 or _sw18 == 1026:
                    _m19 = True
                    _sw35 = MpCanvas.dR
                    if _sw35 == 1:
                        MpCanvas.bB = 99
                        MpCanvas.b_I((10 - MpCanvas.an))
                        MpCanvas.ba = 10
                        MpCanvas.G = False
                        MpCanvas.i_I(94)
                    return
                if _m19 or _sw18 == 1028:
                    _m19 = True
                    _sw36 = MpCanvas.dR
                    if _sw36 == 1:
                        MpCanvas.cL = 0
                        while MpCanvas.cL < 4:
                            MpCanvas.bi = False
                            MpCanvas.cM = 0
                            while MpCanvas.cM < 4:
                                if MpCanvas.bQ[MpCanvas.cM] and (MpCanvas.bR[MpCanvas.cM] == MpCanvas.cL):
                                    MpCanvas.ct = MpCanvas.cM
                                    MpCanvas.bi = True
                                    break
                                MpCanvas.cM = MpCanvas.cM + 1
                            if MpCanvas.bi:
                                MpCanvas.cb[MpCanvas.ct] = k2.a_v()
                            else:
                                MpCanvas.bJ = k2.a_v()
                            MpCanvas.cL = MpCanvas.cL + 1
                        MpCanvas.aT = k2.a_v()
                        MpCanvas.cL = 0
                        while MpCanvas.cL < MpCanvas.aT:
                            MpCanvas.cK[(0 + MpCanvas.cL)] = k2.a_v()
                            MpCanvas.cK[(4 + MpCanvas.cL)] = k2.a_v()
                            MpCanvas.cJ[(0 + MpCanvas.cL)] = k2.b_v()
                            MpCanvas.cK[(8 + MpCanvas.cL)] = k2.a_v()
                            MpCanvas.cK[(12 + MpCanvas.cL)] = k2.a_v()
                            MpCanvas.cK[(16 + MpCanvas.cL)] = k2.a_v()
                            MpCanvas.cJ[(4 + MpCanvas.cL)] = k2.b_v()
                            MpCanvas.cK[(20 + MpCanvas.cL)] = k2.a_v()
                            MpCanvas.cK[(24 + MpCanvas.cL)] = k2.a_v()
                            MpCanvas.cK[(28 + MpCanvas.cL)] = k2.a_v()
                            MpCanvas.cL = MpCanvas.cL + 1
                        k2.a_v()
                        MpCanvas.cL = 0
                        while MpCanvas.cL < MpCanvas.aT:
                            if MpCanvas.cK[(24 + MpCanvas.cL)] == 1:
                                MpCanvas.cK[(32 + MpCanvas.cL)] = k2.a_v()
                                MpCanvas.cK[(36 + MpCanvas.cL)] = k2.a_v()
                                MpCanvas.cJ[(8 + MpCanvas.cL)] = k2.b_v()
                                MpCanvas.cK[(40 + MpCanvas.cL)] = k2.a_v()
                            MpCanvas.cL = MpCanvas.cL + 1
                        MpCanvas.i_I(99)
                    return
                if _m19 or _sw18 == 1031:
                    _m19 = True
                    _sw37 = MpCanvas.dR
                    if _sw37 == 1:
                        MpCanvas.by = k2.a_v()
                        MpCanvas.i_I(104)
                    return
                if _m19 or _sw18 == 1032:
                    _m19 = True
                    _sw38 = MpCanvas.dR
                    if _sw38 == 1:
                        MpCanvas.aU = k2.a_v()
                        if MpCanvas.bz != 2:
                            if MpCanvas.aU == 1:
                                MpCanvas.at = MpCanvas.at + 1
                            else:
                                MpCanvas.au = MpCanvas.au + 1
                        MpCanvas.aV = k2.b_v()
                        MpCanvas.aW = k2.a_v()
                        MpCanvas.aX = k2.b_v()
                        MpCanvas.aY = k2.b_v()
                        MpCanvas.bI = k2.a_I(15)
                        MpCanvas.aZ = k2.c()
                        k2.a_v()
                        k2.c()
                        k2.a_v()
                        MpCanvas.i_I(105)
                    return
                if _m19 or _sw18 == 1037:
                    _m19 = True
                    _sw39 = MpCanvas.dR
                    if _sw39 == 1:
                        MpCanvas.bH = k2.a_I(14)
                        MpCanvas.aP = k2.a_v()
                        MpCanvas.aQ = k2.a_v()
                        MpCanvas.i_I(91)
                    return
                if _m19 or _sw18 == 1035:
                    _m19 = True
                    _sw40 = MpCanvas.dR
                    _m41 = False
                    while True:
                        if _m41 or _sw40 == 1:
                            _m41 = True
                            MpCanvas.bg = k2.a_v()
                            MpCanvas.cL = 0
                            while MpCanvas.cL < 4:
                                if MpCanvas.bQ[MpCanvas.cL] and (MpCanvas.bR[MpCanvas.cL] == MpCanvas.bg):
                                    MpCanvas.ct = MpCanvas.cL
                                    break
                                MpCanvas.cL = MpCanvas.cL + 1
                            MpCanvas.bQ[MpCanvas.ct] = False
                            if MpCanvas.bW[MpCanvas.ct] == 0:
                                break
                            if imod(MpCanvas.bR[MpCanvas.ct], 2) == imod(MpCanvas.bR[0], 2):
                                MpCanvas.bb = MpCanvas.bb - 1
                                raise _Brk_block0_1631()
                            MpCanvas.bc = MpCanvas.bc - 1
                        break
                    return
                if _m19 or _sw18 == 1281:
                    _m19 = True
                    _sw42 = MpCanvas.dR
                    if _sw42 == 1:
                        MpCanvas.cE = MpCanvas.bG
                        self.m_I(2)
                        return
                    elif _sw42 == (-6):
                        MpCanvas.cw = 6
                        self.k_I(4)
                        return
                    elif _sw42 == (-49):
                        MpCanvas.cw = 5
                        self.k_I(4)
                        return
                    elif _sw42 == (-15):
                        MpCanvas.cw = 5
                        self.k_I(4)
                        return
                    MpCanvas.cw = 0
                    self.k_I(4)
                    return
                if _m19 or _sw18 == 1283:
                    _m19 = True
                    self.k_I(84)
                    _sw43 = MpCanvas.dR
                    if _sw43 == 1:
                        MpCanvas.cF = MpCanvas.bG
                        MpCanvas.C = 0
                        MpCanvas.bG = MpCanvas.cG
                        MpCanvas.B = 1
                        return
                    elif _sw43 == (-49):
                        MpCanvas.cw = 5
                        self.k_I(4)
                        return
                    MpCanvas.cw = 0
                    self.k_I(4)
                    return
                if _m19 or _sw18 == 1285:
                    _m19 = True
                    _sw44 = MpCanvas.dR
                    if _sw44 == 1:
                        MpCanvas.cG = MpCanvas.bG
                        self.N_v()
                        return
                    elif _sw44 == (-49):
                        MpCanvas.cw = 5
                        self.k_I(4)
                        return
                    MpCanvas.cw = 0
                    self.k_I(4)
                    return
                if _m19 or _sw18 == 1288:
                    _m19 = True
                    _sw45 = MpCanvas.dR
                    if _sw45 == 1:
                        MpCanvas.aC = k2.b_v()
                        MpCanvas.aD = k2.b_v()
                        MpCanvas.aE = k2.b_v()
                        MpCanvas.aF = k2.b_v()
                        MpCanvas.aG = k2.b_v()
                        MpCanvas.aH = k2.b_v()
                        MpCanvas.aI = k2.b_v()
                        MpCanvas.aJ = k2.b_v()
                        self.k_I(81)
                        return
                    MpCanvas.cw = 0
                    self.k_I(4)
                    return
                if _m19 or _sw18 == 1290:
                    _m19 = True
                    _sw46 = MpCanvas.dR
                    if _sw46 == 1:
                        MpCanvas.cL = 0
                        while MpCanvas.cL < 11:
                            MpCanvas.cH[MpCanvas.cL] = 99
                            MpCanvas.cL = MpCanvas.cL + 1
                        MpCanvas.bf = k2.a_v()
                        MpCanvas.cL = 0
                        while MpCanvas.cL < MpCanvas.bf:
                            MpCanvas.bp = k2.a_v()
                            MpCanvas.cH[(MpCanvas.bp - 3)] = k2.a_v()
                            MpCanvas.cL = MpCanvas.cL + 1
                        MpCanvas.cL = 0
                        while MpCanvas.cL < MpCanvas.bD:
                            MpCanvas.cB[MpCanvas.cL] = MpCanvas.bE[MpCanvas.cL]
                            MpCanvas.cL = MpCanvas.cL + 1
                        while MpCanvas.cL < 4:
                            MpCanvas.cM = 0
                            while MpCanvas.cM < 11:
                                MpCanvas.bq = False
                                MpCanvas.cN = 0
                                while MpCanvas.cN < MpCanvas.cL:
                                    if MpCanvas.cB[MpCanvas.cN] == (3 + MpCanvas.cM):
                                        MpCanvas.bq = True
                                        break
                                    MpCanvas.cN = MpCanvas.cN + 1
                                if not MpCanvas.bq:
                                    MpCanvas.cB[MpCanvas.cL] = i8(((3 + MpCanvas.cM)))
                                    break
                                MpCanvas.cM = MpCanvas.cM + 1
                            MpCanvas.cL = MpCanvas.cL + 1
                        self.k_I(82)
                        return
                    MpCanvas.cw = 0
                    self.k_I(4)
                    return
                if _m19 or _sw18 == 1292:
                    _m19 = True
                    _sw47 = MpCanvas.dR
                    if _sw47 == 1:
                        MpCanvas.cM = 0
                        MpCanvas.cL = 0
                        while MpCanvas.cL < 4:
                            if MpCanvas.cH[(MpCanvas.cB[MpCanvas.cL] - 3)] != 99:
                                MpCanvas.bE[MpCanvas.cM] = MpCanvas.cB[MpCanvas.cL]
                                MpCanvas.cM = MpCanvas.cM + 1
                            MpCanvas.cL = MpCanvas.cL + 1
                        MpCanvas.bD = MpCanvas.cM
                        MpCanvas.cL = MpCanvas.cM
                        while MpCanvas.cL < 4:
                            MpCanvas.bE[MpCanvas.cM] = 99
                            MpCanvas.cL = MpCanvas.cL + 1
                        self.N_v()
                        return
                    MpCanvas.cw = 0
                    self.k_I(4)
                    return
                if _m19 or _sw18 == 1297:
                    _m19 = True
                    _sw48 = MpCanvas.dR
                    if _sw48 == 1:
                        MpCanvas.ax = k2.c()
                        MpCanvas.aA = k2.c()
                        MpCanvas.aB = k2.c()
                        self.k_I(80)
                        return
                    MpCanvas.cw = 0
                    self.k_I(4)
                    return
                if _m19 or _sw18 == 1299:
                    _m19 = True
                    _sw49 = MpCanvas.dR
                    if _sw49 == 1:
                        MpCanvas.ay = k2.c()
                        MpCanvas.ax = k2.c()
                        MpCanvas.az = k2.c()
                        self.k_I(83)
                        return
                    MpCanvas.cw = 0
                    self.k_I(4)
                    return
                if _m19 or _sw18 == 1536:
                    _m19 = True
                    _sw50 = MpCanvas.dR
                    if _sw50 == 1:
                        MpCanvas.bd = k2.a_v()
                        n6 = 0
                        while n6 < 4:
                            MpCanvas.bF[n6] = k2.a_I(16)
                            n6 = n6 + 1
                        MpCanvas.aN = 0
                        MpCanvas.i_I(6)
                    return
                if _m19 or _sw18 == 289:
                    _m19 = True
                    if MpCanvas.dR == 1:
                        _t51 = k2.c()
                        MpCanvas.ao = _t51
                        MpCanvas.ap = _t51
                        self.k_I(88)
                        return
                    MpCanvas.cw = 0
                    self.k_I(4)
                    return
                if _m19 or _sw18 == 291:
                    _m19 = True
                    if MpCanvas.dR == 1:
                        self.N_v()
                        return
                    MpCanvas.cw = 0
                    self.k_I(4)
                break
        except _Brk_block0_1631:
            pass

    def d_I(self, n2):  # g.java:2589
        if MpCanvas.da < 2:
            return
        if (n2 == (-3)) or (n2 == (-1)):
            if MpCanvas.dU[MpCanvas.dW] > 0:
                n3 = MpCanvas.dW
                MpCanvas.dU[n3] = (MpCanvas.dU[n3] - 1)
            else:
                MpCanvas.dU[MpCanvas.dW] = (MpCanvas.k - 1)
        elif (n2 == (-4)) or (n2 == (-2)):
            if MpCanvas.dU[MpCanvas.dW] < (MpCanvas.k - 1):
                n4 = MpCanvas.dW
                MpCanvas.dU[n4] = (MpCanvas.dU[n4] + 1)
            else:
                MpCanvas.dU[MpCanvas.dW] = 0
        if n2 == (-5):
            self.q_v()

    def e_I(self, n2):  # g.java:2613
        if MpCanvas.da < 2:
            return
        if (n2 == (-3)) or (n2 == (-1)):
            if MpCanvas.dU[MpCanvas.dW] > 0:
                n3 = MpCanvas.dW
                MpCanvas.dU[n3] = (MpCanvas.dU[n3] - 1)
            else:
                MpCanvas.dU[MpCanvas.dW] = 1
        elif (n2 == (-4)) or (n2 == (-2)):
            if MpCanvas.dU[MpCanvas.dW] < 1:
                n4 = MpCanvas.dW
                MpCanvas.dU[n4] = (MpCanvas.dU[n4] + 1)
            else:
                MpCanvas.dU[MpCanvas.dW] = 0
        if n2 == (-5):
            self.q_v()
            return
        if n2 == (-7):
            if (MpCanvas.cY == 160) and (MpCanvas.al != 1):
                return
            MpCanvas.dU[MpCanvas.dW] = 1
            self.q_v()

    def keyPressed(self, n2):  # g.java:2645
        if (n2 == (-32)) or (n2 == (-33)):
            return
        MpCanvas.m = n2
        if MpCanvas.J:
            if MpCanvas.m == (-5):
                MpCanvas.a_I(2)
            MpCanvas.m = (-999)

    def f_I(self, var1_1):  # g.java:2661
        MpCanvas.dZ = 0
        MpCanvas.cs = var1_1
        _sw52 = MpCanvas.cY
        try:
            _m53 = False
            while True:
                if _m53 or _sw52 == 161:
                    _m53 = True
                    if MpCanvas.cs == (-7):
                        self.N_v()
                        return
                if _m53 or _sw52 in (11, 12, 16, 87, 162, 163, 164):
                    _m53 = True
                    if MpCanvas.cs == (-7):
                        self.N_v()
                        return
                    self.d_I(MpCanvas.cs)
                    return
                if _m53 or _sw52 in (170, 171):
                    _m53 = True
                    if (MpCanvas.cs != (-7)) and (MpCanvas.cs != (-5)):
                        break
                    self.N_v()
                    return
                if _m53 or _sw52 == 6:
                    _m53 = True
                    if MpCanvas.aN > 0:
                        MpCanvas.aO = MpCanvas.aO + 1
                        self.c_I(258)
                        return
                    if MpCanvas.bd == 1:
                        self.l_I(7)
                        return
                    if MpCanvas.bd != 9:
                        break
                    MpCanvas.i_I(300)
                    return
                if _m53 or _sw52 == 7:
                    _m53 = True
                    MpCanvas.k = 2
                    MpCanvas.P = False
                    self.l_I(10)
                    return
                if _m53 or _sw52 == 10:
                    _m53 = True
                    if MpCanvas.x:
                        if (MpCanvas.cs == (-3)) or (MpCanvas.cs == (-4)):
                            MpCanvas.y = imod(((MpCanvas.y + 1)), 2)
                            return
                        if MpCanvas.cs != (-5):
                            break
                        if MpCanvas.y == 0:
                            MpCanvas.i_I(300)
                            return
                        MpCanvas.x = False
                        return
                    if MpCanvas.cs == (-6):
                        MpCanvas.n_v()
                        MpCanvas.z = 0
                        MpCanvas.P = True
                        MpCanvas.C = 0
                        self.k_I(2)
                        return
                    if MpCanvas.cs == (-7):
                        MpCanvas.x = True
                        MpCanvas.y = 1
                        return
                    self.d_I(MpCanvas.cs)
                    return
                if _m53 or _sw52 in (80, 81, 83):
                    _m53 = True
                    if (MpCanvas.cs != (-5)) and (MpCanvas.cs != (-7)):
                        break
                    self.N_v()
                    return
                if _m53 or _sw52 == 82:
                    _m53 = True
                    if MpCanvas.cs == (-1):
                        if MpCanvas.dU[MpCanvas.dW] > 0:
                            v0 = MpCanvas.dW
                            MpCanvas.dU[v0] = (MpCanvas.dU[v0] - 1)
                        else:
                            MpCanvas.dU[MpCanvas.dW] = 3
                    elif MpCanvas.cs == (-2):
                        if MpCanvas.dU[MpCanvas.dW] < 3:
                            v1 = MpCanvas.dW
                            MpCanvas.dU[v1] = (MpCanvas.dU[v1] + 1)
                        else:
                            MpCanvas.dU[MpCanvas.dW] = 0
                    elif MpCanvas.cs == (-3):
                        while True:
                            try:
                                if MpCanvas.cB[MpCanvas.dU[MpCanvas.dW]] > 3:
                                    v2 = MpCanvas.dU[MpCanvas.dW]
                                    MpCanvas.cB[v2] = i8(((MpCanvas.cB[v2] - 1)))
                                else:
                                    MpCanvas.cB[MpCanvas.dU[MpCanvas.dW]] = 13
                                MpCanvas.bq = False
                                MpCanvas.cL = 0
                                while MpCanvas.cL < 4:
                                    if (MpCanvas.cL != MpCanvas.dU[MpCanvas.dW]) and (MpCanvas.cB[MpCanvas.dU[MpCanvas.dW]] == MpCanvas.cB[MpCanvas.cL]):
                                        MpCanvas.bq = True
                                        raise _Cont_block47_2359()
                                    MpCanvas.cL = MpCanvas.cL + 1
                            except _Cont_block47_2359:
                                pass
                            if not (MpCanvas.bq):
                                break
                    elif MpCanvas.cs == (-4):
                        while True:
                            try:
                                if MpCanvas.cB[MpCanvas.dU[MpCanvas.dW]] < 13:
                                    v3 = MpCanvas.dU[MpCanvas.dW]
                                    MpCanvas.cB[v3] = i8(((MpCanvas.cB[v3] + 1)))
                                else:
                                    MpCanvas.cB[MpCanvas.dU[MpCanvas.dW]] = 3
                                MpCanvas.bq = False
                                MpCanvas.cL = 0
                                while MpCanvas.cL < 4:
                                    if (MpCanvas.cL != MpCanvas.dU[MpCanvas.dW]) and (MpCanvas.cB[MpCanvas.dU[MpCanvas.dW]] == MpCanvas.cB[MpCanvas.cL]):
                                        MpCanvas.bq = True
                                        raise _Cont_block49_2378()
                                    MpCanvas.cL = MpCanvas.cL + 1
                            except _Cont_block49_2378:
                                pass
                            if not (MpCanvas.bq):
                                break
                    if (MpCanvas.cs != (-5)) and (MpCanvas.cs != (-7)):
                        break
                    self.q_v()
                    return
                if _m53 or _sw52 == 84:
                    _m53 = True
                    if MpCanvas.cs == (-7):
                        if len(MpCanvas.bG) == 0:
                            if MpCanvas.B == 0:
                                self.N_v()
                                return
                            MpCanvas.B = MpCanvas.B - 1
                            return
                        MpCanvas.bG = MpCanvas.bG[0:(len(MpCanvas.bG) - 1)]
                        return
                    if (MpCanvas.cs == (-5)) or (MpCanvas.cs == (-6)):
                        if len(MpCanvas.bG) == 0:
                            if MpCanvas.C >= 26:
                                break
                            MpCanvas.bG = _js(MpCanvas.bG, chr(((((65 + MpCanvas.C))) & 0xFFFF)))
                            return
                        if len(MpCanvas.bG) > 20:
                            break
                        if MpCanvas.C < 26:
                            if len(MpCanvas.bG) >= 20:
                                break
                            MpCanvas.bG = _js(MpCanvas.bG, chr(((((97 + MpCanvas.C))) & 0xFFFF)))
                            return
                        if MpCanvas.C == 26:
                            if len(MpCanvas.bG) >= 20:
                                break
                            MpCanvas.bG = _js(MpCanvas.bG, chr(32))
                            return
                        if MpCanvas.C != 27:
                            break
                        MpCanvas.cv = 5
                        MpCanvas.bG = MpCanvas.d_T(MpCanvas.bG)
                        if MpCanvas.B == 0:
                            self.c_I(1282)
                        else:
                            self.c_I(1284)
                        MpCanvas.i_I(3)
                        return
                    MpCanvas.q_I(MpCanvas.cs)
                    return
                if _m53 or _sw52 == 85:
                    _m53 = True
                    if MpCanvas.cs == (-7):
                        if len(MpCanvas.bG) == 0:
                            self.N_v()
                            return
                        MpCanvas.bG = MpCanvas.bG[0:(len(MpCanvas.bG) - 1)]
                        return
                    if (MpCanvas.cs == (-5)) or (MpCanvas.cs == (-6)):
                        if len(MpCanvas.bG) == 0:
                            if MpCanvas.C >= 26:
                                break
                            MpCanvas.bG = _js(MpCanvas.bG, chr(((((65 + MpCanvas.C))) & 0xFFFF)))
                            return
                        if len(MpCanvas.bG) > 8:
                            break
                        if MpCanvas.C < 26:
                            if len(MpCanvas.bG) >= 8:
                                break
                            MpCanvas.bG = _js(MpCanvas.bG, chr(((((97 + MpCanvas.C))) & 0xFFFF)))
                            return
                        if MpCanvas.C != 26:
                            break
                        self.k_I(86)
                        return
                    MpCanvas.p_I(MpCanvas.cs)
                    return
                if _m53 or _sw52 == 88:
                    _m53 = True
                    if MpCanvas.cs == (-1):
                        if MpCanvas.dU[MpCanvas.dW] > 0:
                            v4 = MpCanvas.dW
                            MpCanvas.dU[v4] = (MpCanvas.dU[v4] - 1)
                            return
                        MpCanvas.dU[MpCanvas.dW] = 2
                        return
                    if MpCanvas.cs == (-2):
                        if MpCanvas.dU[MpCanvas.dW] < 2:
                            v5 = MpCanvas.dW
                            MpCanvas.dU[v5] = (MpCanvas.dU[v5] + 1)
                            return
                        MpCanvas.dU[MpCanvas.dW] = 0
                        return
                    if (MpCanvas.cs == (-3)) or (MpCanvas.cs == (-4)):
                        self.q_v()
                        return
                    if MpCanvas.cs == (-5):
                        MpCanvas.cs = (-4)
                        self.q_v()
                        return
                    if MpCanvas.cs != (-7):
                        break
                    MpCanvas.K_v()
                    if MpCanvas.ap != MpCanvas.ao:
                        MpCanvas.cv = 1
                        MpCanvas.i_I(3)
                        self.c_I(290)
                        return
                    self.N_v()
                    self.t_I(1)
                    return
                if _m53 or _sw52 == 89:
                    _m53 = True
                    if MpCanvas.cs == (-3):
                        if MpCanvas.be > 0:
                            MpCanvas.be = MpCanvas.be - 1
                            return
                        MpCanvas.be = (Consts.ew[MpCanvas.dU[(MpCanvas.dW - 1)]] - 1)
                        return
                    if (MpCanvas.cs == (-4)) or (MpCanvas.cs == (-5)):
                        if MpCanvas.be < (Consts.ew[MpCanvas.dU[(MpCanvas.dW - 1)]] - 1):
                            MpCanvas.be = MpCanvas.be + 1
                            return
                        MpCanvas.be = 0
                        return
                    if MpCanvas.cs != (-7):
                        break
                    self.N_v()
                    return
                if _m53 or _sw52 == 20:
                    _m53 = True
                    if MpCanvas.cs == (-7):
                        self.N_v()
                        return
                    self.d_I(MpCanvas.cs)
                    return
                if _m53 or _sw52 == 21:
                    _m53 = True
                    if (MpCanvas.cs == (-5)) or (MpCanvas.cs == (-6)):
                        if len(MpCanvas.bG) > 12:
                            break
                        if MpCanvas.C < 26:
                            if len(MpCanvas.bG) >= 12:
                                break
                            MpCanvas.bG = _js(MpCanvas.bG, chr(((((65 + MpCanvas.C))) & 0xFFFF)))
                            return
                        if (MpCanvas.C != 26) or (len(MpCanvas.bG) < 4):
                            break
                        _sw54 = MpCanvas.bz
                        if _sw54 == 0:
                            MpCanvas.cv = 2
                        elif _sw54 == 1:
                            MpCanvas.cv = 4
                        elif _sw54 == 2:
                            MpCanvas.cv = 4
                        MpCanvas.cv = 0
                        self.c_I(768)
                        MpCanvas.i_I(3)
                        return
                    if var1_1 == (-7):
                        if len(MpCanvas.bG) == 0:
                            self.N_v()
                            return
                        MpCanvas.bG = MpCanvas.bG[0:(len(MpCanvas.bG) - 1)]
                        return
                    MpCanvas.p_I(var1_1)
                    return
                if _m53 or _sw52 == 94:
                    _m53 = True
                    if MpCanvas.D:
                        if (MpCanvas.cs == (-3)) or (MpCanvas.cs == (-4)):
                            MpCanvas.E = imod(((MpCanvas.E + 1)), 2)
                            return
                        if MpCanvas.cs != (-5):
                            break
                        if MpCanvas.E == 0:
                            MpCanvas.P = False
                            MpCanvas.n_v()
                            MpCanvas.b_I((-1))
                            MpCanvas.cv = 0
                            MpCanvas.A = False
                            MpCanvas.i_I(10000)
                            return
                        MpCanvas.D = False
                        return
                    MpCanvas.bB = 99
                    if MpCanvas.cs == (-1):
                        MpCanvas.bB = 2
                    elif MpCanvas.cs == (-3):
                        MpCanvas.bB = 1
                    elif MpCanvas.cs == (-4):
                        MpCanvas.bB = 0
                    elif MpCanvas.cs == (-2):
                        if MpCanvas.bD > 0:
                            MpCanvas.cN = 0
                            while MpCanvas.cN < MpCanvas.bD:
                                if MpCanvas.bX[0] >= MpCanvas.cI[(MpCanvas.bE[MpCanvas.cN] - 3)]:
                                    MpCanvas.bB = 20
                                    break
                                MpCanvas.cN = MpCanvas.cN + 1
                    elif (MpCanvas.cs == (-7)) and (not MpCanvas.G):
                        MpCanvas.G = True
                        MpCanvas.D = True
                        MpCanvas.E = 1
                        MpCanvas.F = system.currentTimeMillis()
                    if MpCanvas.bB == 20:
                        MpCanvas.i_I(95)
                        return
                    if MpCanvas.bB == 99:
                        break
                    MpCanvas.i_I(96)
                    return
                if _m53 or _sw52 == 95:
                    _m53 = True
                    if MpCanvas.cs == (-1):
                        MpCanvas.db = (_inc(MpCanvas, 'db', -1) if (MpCanvas.db > 0) else (MpCanvas.bD - 1))
                    elif MpCanvas.cs == (-2):
                        MpCanvas.db = (_inc(MpCanvas, 'db', 1) if (MpCanvas.db < (MpCanvas.bD - 1)) else 0)
                    if MpCanvas.cs == (-5):
                        if MpCanvas.bX[0] < MpCanvas.cI[(MpCanvas.bE[MpCanvas.db] - 3)]:
                            break
                        MpCanvas.bB = MpCanvas.bE[MpCanvas.db]
                        MpCanvas.i_I(96)
                        return
                    if MpCanvas.cs != (-7):
                        break
                    MpCanvas.bB = 99
                    MpCanvas.i_I(94)
                    return
                if _m53 or _sw52 == 96:
                    _m53 = True
                    if (MpCanvas.cs == (-1)) or (MpCanvas.cs == (-2)):
                        _sw55 = MpCanvas.bB
                        _m56 = False
                        while True:
                            if _m56 or _sw55 in (9, 10):
                                _m56 = True
                                MpCanvas.cL = 0
                                while MpCanvas.cL < 4:
                                    if (MpCanvas.bQ[MpCanvas.cL] and (imod(MpCanvas.bR[MpCanvas.cL], 2) == imod(MpCanvas.bR[MpCanvas.bA], 2))) and (MpCanvas.bR[MpCanvas.cL] != MpCanvas.bR[MpCanvas.bA]):
                                        MpCanvas.bA = MpCanvas.cL
                                        raise _Brk_block0_2273()
                                    MpCanvas.cL = MpCanvas.cL + 1
                                raise _Brk_block0_2273()
                            if _m56 or _sw55 in (0, 3, 4, 5, 6, 7):
                                _m56 = True
                                MpCanvas.cL = 1
                                while MpCanvas.cL < 4:
                                    if (MpCanvas.bQ[MpCanvas.cL] and (imod(MpCanvas.bR[MpCanvas.cL], 2) == imod(MpCanvas.bR[MpCanvas.bA], 2))) and (MpCanvas.bR[MpCanvas.cL] != MpCanvas.bR[MpCanvas.bA]):
                                        MpCanvas.bA = MpCanvas.cL
                                        raise _Brk_block0_2273()
                                    MpCanvas.cL = MpCanvas.cL + 1
                            if _m56 or _sw55 not in (9, 10, 0, 3, 4, 5, 6, 7):
                                _m56 = True
                                return
                            break
                    if MpCanvas.cs == (-5):
                        self.B_v()
                        return
                    if MpCanvas.cs != (-7):
                        break
                    _sw57 = MpCanvas.bB
                    if _sw57 in (3, 4, 5, 6, 7, 9, 10):
                        MpCanvas.i_I(95)
                        return
                    MpCanvas.i_I(94)
                    return
                if _m53 or _sw52 == 97:
                    _m53 = True
                    if (MpCanvas.da <= 0) or (MpCanvas.cs != (-5)):
                        break
                    self.C_v()
                    return
                if _m53 or _sw52 == 105:
                    _m53 = True
                    if (MpCanvas.da <= idiv(1000, MpCanvas.dc)) or (MpCanvas.cs != (-5)):
                        break
                    self.l_I(10)
                    _sw58 = MpCanvas.bz
                    _m59 = False
                    while True:
                        if _m59 or _sw58 == 0:
                            _m59 = True
                            self.k_I(11)
                            raise _Brk_block0_2273()
                        if _m59 or _sw58 == 1:
                            _m59 = True
                            self.k_I(11)
                            MpCanvas.dU[MpCanvas.dW] = 1
                            raise _Brk_block0_2273()
                        if _m59 or _sw58 == 2:
                            _m59 = True
                            MpCanvas.dU[MpCanvas.dW] = 1
                            self.k_I(12)
                        break
                    return
                if _m53 or _sw52 == 4:
                    _m53 = True
                    if MpCanvas.x:
                        if (MpCanvas.cs == (-3)) or (MpCanvas.cs == (-4)):
                            MpCanvas.y = imod(((MpCanvas.y + 1)), 2)
                            return
                        if MpCanvas.cs != (-5):
                            break
                        if MpCanvas.y == 0:
                            MpCanvas.i_I(300)
                            return
                        MpCanvas.x = False
                        MpCanvas.y = 1
                        return
                    if MpCanvas.cs == (-6):
                        if (MpCanvas.cw != 7) and (MpCanvas.cw != 1):
                            break
                        MpCanvas.n_v()
                        MpCanvas.z = 0
                        MpCanvas.P = True
                        MpCanvas.i_I(2)
                        MpCanvas.x = False
                        return
                    if MpCanvas.cs == (-7):
                        if (MpCanvas.cw != 7) and (MpCanvas.cw != 1):
                            break
                        MpCanvas.x = True
                        MpCanvas.y = 1
                        return
                    if MpCanvas.cs != (-5):
                        break
                    if not NetThread.j:
                        if ((MpCanvas.cw == 14) or (MpCanvas.cw == 15)) or (MpCanvas.cw == 16):
                            self.N_v()
                            return
                        if MpCanvas.cw == 17:
                            MpCanvas.z = 0
                            MpCanvas.P = True
                            self.k_I(2)
                            return
                        if MpCanvas.cw != 1:
                            MpCanvas.cv = 0
                            MpCanvas.i_I(10000)
                            return
                        self.l_I(1)
                        return
                    if MpCanvas.ec > (-1):
                        self.k_I(MpCanvas.ec)
                        MpCanvas.ec = (-1)
                        return
                    _sw60 = MpCanvas.dV[(MpCanvas.dW - 1)]
                    if _sw60 == 105:
                        return
                    elif _sw60 == 86:
                        self.m_I(2)
                        return
                    self.N_v()
                    return
                if _m53 or _sw52 == 5:
                    _m53 = True
                    if (MpCanvas.cs == (-3)) or (MpCanvas.cs == (-4)):
                        MpCanvas.dU[MpCanvas.dW] = imod(((MpCanvas.dU[MpCanvas.dW] + 1)), 2)
                        return
                    if MpCanvas.cs != (-5):
                        break
                    if MpCanvas.dU[MpCanvas.dW] == 0:
                        if MpCanvas.am == 0:
                            MpCanvas.am = 4
                    else:
                        MpCanvas.am = 0
                    MpCanvas.K_v()
                    MpCanvas.i_I(1)
                    self.s_I(1)
                    return
                if _m53 or _sw52 == 1:
                    _m53 = True
                    if MpCanvas.da <= 3:
                        break
                    if MpCanvas.i == "":
                        MpCanvas.z = 0
                        self.k_I(2)
                        return
                    if MpCanvas.cw == 1:
                        MpCanvas.i_I(4)
                        return
                    MpCanvas.cv = 0
                    MpCanvas.A = False
                    MpCanvas.i_I(10000)
                    return
                if _m53 or _sw52 == 2:
                    _m53 = True
                    self.j_I(MpCanvas.cs)
                    return
                if _m53 or _sw52 in (86, 160):
                    _m53 = True
                    self.e_I(MpCanvas.cs)
                break
        except _Brk_block0_2273:
            pass

    @staticmethod
    def j_v():  # g.java:3263
        MpCanvas.cj[MpCanvas.cL] = (MpCanvas.cf[MpCanvas.cL] - MpCanvas.bW[MpCanvas.cL])
        MpCanvas.ch[MpCanvas.cL] = idiv(MpCanvas.cj[MpCanvas.cL], 5)
        if MpCanvas.ch[MpCanvas.cL] == 0:
            if MpCanvas.cf[MpCanvas.cL] > MpCanvas.bW[MpCanvas.cL]:
                MpCanvas.ch[MpCanvas.cL] = 1
            elif MpCanvas.cf[MpCanvas.cL] < MpCanvas.bW[MpCanvas.cL]:
                MpCanvas.ch[MpCanvas.cL] = (-1)
        MpCanvas.ci[MpCanvas.cL] = idiv(((MpCanvas.cg[MpCanvas.cL] - MpCanvas.bX[MpCanvas.cL])), 5)
        if MpCanvas.ci[MpCanvas.cL] == 0:
            if MpCanvas.cg[MpCanvas.cL] > MpCanvas.bX[MpCanvas.cL]:
                MpCanvas.ci[MpCanvas.cL] = 1
                return
            if MpCanvas.cg[MpCanvas.cL] < MpCanvas.bX[MpCanvas.cL]:
                MpCanvas.ci[MpCanvas.cL] = (-1)

    def k_v(self):  # g.java:3285
        MpCanvas.Q = 0
        MpCanvas.U = (-1)
        MpCanvas.X = (-1)
        MpCanvas.cL = 0
        while MpCanvas.cL < 4:
            if MpCanvas.bQ[MpCanvas.cL]:
                MpCanvas.cc[MpCanvas.cL] = 0
                MpCanvas.cd[MpCanvas.cL] = 0
                MpCanvas.ce[MpCanvas.cL] = 0
                MpCanvas.cj[MpCanvas.cL] = 0
                if MpCanvas.bR[MpCanvas.cL] == MpCanvas.cK[(0 + MpCanvas.bC)]:
                    MpCanvas.S = MpCanvas.cL
                    MpCanvas.cf[MpCanvas.cL] = MpCanvas.cJ[(0 + MpCanvas.bC)]
                    MpCanvas.cg[MpCanvas.cL] = MpCanvas.cK[(8 + MpCanvas.bC)]
                    MpCanvas.j_v()
                if MpCanvas.bR[MpCanvas.cL] == MpCanvas.cK[(12 + MpCanvas.bC)]:
                    MpCanvas.T = MpCanvas.cL
                    MpCanvas.cf[MpCanvas.cL] = MpCanvas.cJ[(4 + MpCanvas.bC)]
                    MpCanvas.cg[MpCanvas.cL] = MpCanvas.cK[(20 + MpCanvas.bC)]
                    MpCanvas.j_v()
                    _sw61 = MpCanvas.cK[(16 + MpCanvas.bC)]
                    _m62 = False
                    while True:
                        if _m62 or _sw61 == 1:
                            _m62 = True
                            if MpCanvas.cb[MpCanvas.T] == 1:
                                MpCanvas.V = 4
                                break
                            MpCanvas.V = 1
                            break
                        if _m62 or _sw61 == 2:
                            _m62 = True
                            MpCanvas.V = 5
                        break
                if (MpCanvas.cK[(24 + MpCanvas.bC)] > 0) and (MpCanvas.bR[MpCanvas.cL] == MpCanvas.cK[(32 + MpCanvas.bC)]):
                    MpCanvas.U = MpCanvas.cL
                    MpCanvas.cf[MpCanvas.cL] = MpCanvas.cJ[(8 + MpCanvas.bC)]
                    MpCanvas.cg[MpCanvas.cL] = MpCanvas.cK[(40 + MpCanvas.bC)]
                    MpCanvas.j_v()
                    _sw63 = MpCanvas.cK[(36 + MpCanvas.bC)]
                    _m64 = False
                    while True:
                        if _m64 or _sw63 == 1:
                            _m64 = True
                            if MpCanvas.cb[MpCanvas.U] == 1:
                                MpCanvas.W = 4
                                break
                            MpCanvas.W = 1
                            break
                        if _m64 or _sw63 == 2:
                            _m64 = True
                            MpCanvas.W = 5
                        break
            MpCanvas.cL = MpCanvas.cL + 1
        _sw65 = MpCanvas.cK[(4 + MpCanvas.bC)]
        if _sw65 in (3, 4, 5, 6, 7, 8):
            MpCanvas.cc[MpCanvas.S] = 8
        elif _sw65 in (2, 9, 10):
            MpCanvas.cc[MpCanvas.S] = 12
        elif _sw65 in (11, 12, 13):
            MpCanvas.cc[MpCanvas.S] = 13
        elif _sw65 == 0:
            MpCanvas.cc[MpCanvas.S] = 2
            MpCanvas.bl = idiv((((MpCanvas.cQ - 67) - 42)), Consts.eh[MpCanvas.cc[MpCanvas.S]])
            MpCanvas.bm = (0 if (MpCanvas.bz == 0) else ((0 if (idiv(MpCanvas.bR[MpCanvas.S], 2) == idiv(MpCanvas.cK[(12 + MpCanvas.bC)], 2)) else ((idiv(46, Consts.eh[MpCanvas.cc[MpCanvas.S]]) if (idiv(MpCanvas.bR[MpCanvas.S], 2) == 0) else idiv((-46), Consts.eh[MpCanvas.cc[MpCanvas.S]]))))))
        MpCanvas.R = Consts.eh[MpCanvas.cc[MpCanvas.S]]

    def l_v(self):  # g.java:3374
        if MpCanvas.A:
            self.c_I(278)
            return
        self.c_I(262)

    def m_v(self):  # g.java:3382
        MpCanvas.eb = False
        if not NetThread.j:
            if MpCanvas.dP is None:
                MpCanvas.dP = NetThread()
                MpCanvas.dP.setPriority(10)
                MpCanvas.dP.start()
            NetThread.a_Lg(self)
            MpCanvas.L = True
            MpCanvas.dP.a_TI(MpCanvas.r, MpCanvas.s)

    @staticmethod
    def n_v():  # g.java:3396
        MpCanvas.ea = True
        NetThread.j = False
        MpCanvas.h.k = False
        MpCanvas.a_J(400)
        if MpCanvas.dP is not None:
            NetThread.a_v()
        MpCanvas.dP = None
        MpCanvas.dX = True
        MpCanvas.b_I((-1))
        MpCanvas.a_J(100)

    def o_v(self):  # g.java:3410
        MpCanvas.n_v()
        if MpCanvas.cw > (-1):
            self.p_v()

    def p_v(self):  # g.java:3417
        if MpCanvas.aq:
            MpCanvas.aq = False
            return
        MpCanvas.i_I(4)

    def g_I(self, n2):  # g.java:3425
        if not MpCanvas.ea:
            MpCanvas.cw = (7 if (n2 < 10) else n2)
            self.o_v()
        MpCanvas.ea = False

    def hideNotify(self):  # g.java:3433
        self.ag_v()
        MpCanvas.a_I(1)

    def showNotify(self):  # g.java:3438
        MpCanvas.a_I(1)

    def c_GIIIII(self, graphics, n2, n3, n4, n5, n6):  # g.java:3442
        n7 = 0x525152
        n8 = 0xFFFFFF
        _sw66 = n6
        if _sw66 in (0, 7):
            if imod(n4, 2) == 1:
                n4 = n4 + 1
            if imod(n5, 2) == 1:
                n5 = n5 + 1
            MpCanvas.cx = (n2 - idiv(n4, 2))
            MpCanvas.cy = (n3 - idiv(n5, 2))
            if n6 == 0:
                Draw.b_GIIIII(graphics, MpCanvas.cx, MpCanvas.cy, n4, n5, 0)
            Draw.a_GIIIII(graphics, (MpCanvas.cx + 1), (MpCanvas.cy + 1), (n4 - 2), (n5 - 2), 0xADAAAD)
            MpCanvas.c_GIIM(graphics, (MpCanvas.cx + Consts.eq[2]), (MpCanvas.cy + Consts.er[2]), MpCanvas.df[2])
            MpCanvas.b_GIIM(graphics, ((MpCanvas.cx + n4) + Consts.eq[2]), (MpCanvas.cy + Consts.er[2]), MpCanvas.df[2])
            MpCanvas.c_GIIM(graphics, (MpCanvas.cx + Consts.eq[3]), ((((MpCanvas.cy + n5) - 2) - 5) + Consts.er[3]), MpCanvas.df[3])
            MpCanvas.b_GIIM(graphics, ((MpCanvas.cx + n4) + Consts.eq[3]), ((((MpCanvas.cy + n5) - 2) - 5) + Consts.er[3]), MpCanvas.df[3])
            return
        elif _sw66 == 1:
            MpCanvas.a_GIIIII(graphics, n2, n3, n4, n5, 0)
            MpCanvas.a_GI(graphics, 0xBDBABD)
            MpCanvas.a_GIIII(graphics, (n2 + 14), n3, (((n2 + n4) - 14) - 1), n3)
            MpCanvas.a_GIIII(graphics, (n2 + 14), ((n3 + n5) - 1), (((n2 + n4) - 14) - 1), ((n3 + n5) - 1))
            MpCanvas.a_GI(graphics, 0x949A94)
            MpCanvas.a_GIIII(graphics, (n2 + 1), n3, (n2 + 13), n3)
            MpCanvas.a_GIIII(graphics, ((n2 + n4) - 14), n3, ((n2 + n4) - 2), n3)
            MpCanvas.a_GIIII(graphics, (n2 + 1), ((n3 + n5) - 1), (n2 + 13), ((n3 + n5) - 1))
            MpCanvas.a_GIIII(graphics, ((n2 + n4) - 14), ((n3 + n5) - 1), ((n2 + n4) - 2), ((n3 + n5) - 1))
            MpCanvas.a_GI(graphics, 0xADAAAD)
            MpCanvas.a_GIIII(graphics, (n2 + 5), n3, (n2 + 8), n3)
            MpCanvas.a_GIIII(graphics, ((n2 + n4) - 9), n3, ((n2 + n4) - 6), n3)
            MpCanvas.a_GIIII(graphics, (n2 + 5), ((n3 + n5) - 1), (n2 + 8), ((n3 + n5) - 1))
            MpCanvas.a_GIIII(graphics, ((n2 + n4) - 9), ((n3 + n5) - 1), ((n2 + n4) - 6), ((n3 + n5) - 1))
            MpCanvas.a_GI(graphics, 0x949A94)
            MpCanvas.a_GIIII(graphics, n2, (n3 + 1), n2, ((n3 + n5) - 2))
            MpCanvas.a_GIIII(graphics, ((n2 + n4) - 1), (n3 + 1), ((n2 + n4) - 1), ((n3 + n5) - 2))
            MpCanvas.a_GI(graphics, 0xADAAAD)
            MpCanvas.a_GIIII(graphics, n2, (n3 + 4), n2, ((n3 + n5) - 5))
            MpCanvas.a_GIIII(graphics, ((n2 + n4) - 1), (n3 + 4), ((n2 + n4) - 1), ((n3 + n5) - 5))
            return
        elif _sw66 == 3:
            MpCanvas.a_GI(graphics, n8)
            MpCanvas.a_GIIII(graphics, n2, (n3 - 1), ((n2 + n4) - 1), (n3 - 1))
            MpCanvas.a_GIIII(graphics, n2, (n3 + n5), ((n2 + n4) - 1), (n3 + n5))
            MpCanvas.a_GIIII(graphics, (n2 - 1), n3, (n2 - 1), ((n3 + n5) - 1))
            MpCanvas.a_GIIII(graphics, (n2 + n4), n3, (n2 + n4), ((n3 + n5) - 1))
            MpCanvas.a_GIII(graphics, n2, n3, n8)
            MpCanvas.a_GIII(graphics, ((n2 + n4) - 1), n3, n8)
            MpCanvas.a_GIII(graphics, n2, ((n3 + n5) - 1), n8)
            MpCanvas.a_GIII(graphics, ((n2 + n4) - 1), ((n3 + n5) - 1), n8)
            return
        Draw.b_GIIIII(graphics, n2, (n3 + 1), 1, (n5 - 2), n7)
        Draw.b_GIIIII(graphics, ((n2 + n4) - 1), (n3 + 1), 1, (n5 - 2), n7)
        MpCanvas.cM = 1
        while MpCanvas.cM < (n4 - 1):
            Draw.b_GIIIII(graphics, (n2 + MpCanvas.cM), n3, 1, n5, n7)
            Draw.b_GIIIII(graphics, (n2 + MpCanvas.cM), (n3 + 1), 1, (n5 - 2), 0)
            MpCanvas.cM = MpCanvas.cM + 1

    def q_v(self):  # g.java:3512
        _sw67 = MpCanvas.cY
        try:
            _m68 = False
            while True:
                if _m68 or _sw67 == 160:
                    _m68 = True
                    _sw69 = MpCanvas.al
                    _m70 = False
                    while True:
                        if _m70 or _sw69 == 1:
                            _m70 = True
                            if MpCanvas.dU[MpCanvas.dW] == 0:
                                MpCanvas.cv = 5
                                MpCanvas.i_I(3)
                                raise _Brk_block0_2989()
                            self.o_v()
                            MpCanvas.i_I(1)
                            raise _Brk_block0_2989()
                        if _m70 or _sw69 in (0, 2):
                            _m70 = True
                            self.o_v()
                            MpCanvas.i_I(1)
                        break
                    return
                if _m68 or _sw67 == 161:
                    _m68 = True
                    MpCanvas.ae = i8(MpCanvas.dU[MpCanvas.dW])
                    MpCanvas.cv = 1
                    MpCanvas.i_I(3)
                    self.c_I(1300)
                    return
                if _m68 or _sw67 in (162, 163, 164):
                    _m68 = True
                    MpCanvas.af = MpCanvas.cY
                    MpCanvas.ab = ((((((MpCanvas.dV[MpCanvas.dW] - 162) + 1)) * 10) + MpCanvas.dU[MpCanvas.dW]) + 1)
                    MpCanvas.cv = 1
                    MpCanvas.i_I(3)
                    self.c_I(1293)
                    return
                if _m68 or _sw67 == 10:
                    _m68 = True
                    _sw71 = MpCanvas.dU[MpCanvas.dW]
                    _m72 = False
                    while True:
                        if _m72 or _sw71 == 0:
                            _m72 = True
                            self.k_I(11)
                            raise _Brk_block0_2989()
                        if _m72 or _sw71 == 1:
                            _m72 = True
                            self.k_I(12)
                            raise _Brk_block0_2989()
                        if _m72 or _sw71 == 2:
                            _m72 = True
                            self.k_I(16)
                            raise _Brk_block0_2989()
                        if _m72 or _sw71 == 3:
                            _m72 = True
                            MpCanvas.cv = 1
                            MpCanvas.i_I(3)
                            self.c_I(288)
                            raise _Brk_block0_2989()
                        if _m72 or _sw71 == 4:
                            _m72 = True
                            self.k_I(87)
                            raise _Brk_block0_2989()
                        if _m72 or _sw71 == 5:
                            _m72 = True
                            self.k_I(161)
                        break
                    return
                if _m68 or _sw67 == 11:
                    _m68 = True
                    _sw73 = MpCanvas.dU[MpCanvas.dW]
                    _m74 = False
                    while True:
                        if _m74 or _sw73 == 0:
                            _m74 = True
                            MpCanvas.bz = 0
                            MpCanvas.cv = 2
                            MpCanvas.i_I(3)
                            self.c_I(512)
                            raise _Brk_block0_2989()
                        if _m74 or _sw73 == 1:
                            _m74 = True
                            MpCanvas.bz = 1
                            MpCanvas.cv = 2
                            MpCanvas.i_I(3)
                            self.c_I(512)
                            raise _Brk_block0_2989()
                        if _m74 or _sw73 == 2:
                            _m74 = True
                            self.k_I(20)
                            raise _Brk_block0_2989()
                        if _m74 or _sw73 == 3:
                            _m74 = True
                            self.k_I(87)
                            raise _Brk_block0_2989()
                        if _m74 or _sw73 == 4:
                            _m74 = True
                            self.k_I(161)
                        break
                    return
                if _m68 or _sw67 == 12:
                    _m68 = True
                    _sw75 = MpCanvas.dU[MpCanvas.dW]
                    _m76 = False
                    while True:
                        if _m76 or _sw75 == 0:
                            _m76 = True
                            MpCanvas.bz = i8(2)
                            MpCanvas.cv = 3
                            MpCanvas.i_I(3)
                            self.c_I(512)
                            raise _Brk_block0_2989()
                        if _m76 or _sw75 == 1:
                            _m76 = True
                            MpCanvas.bz = i8(2)
                            self.k_I(21)
                            raise _Brk_block0_2989()
                        if _m76 or _sw75 == 2:
                            _m76 = True
                            self.k_I(87)
                            raise _Brk_block0_2989()
                        if _m76 or _sw75 == 3:
                            _m76 = True
                            self.k_I(161)
                        break
                    return
                if _m68 or _sw67 == 16:
                    _m68 = True
                    _sw77 = MpCanvas.dU[MpCanvas.dW]
                    _m78 = False
                    while True:
                        if _m78 or _sw77 == 0:
                            _m78 = True
                            MpCanvas.cv = 1
                            MpCanvas.i_I(3)
                            self.c_I(1296)
                            raise _Brk_block0_2989()
                        if _m78 or _sw77 == 1:
                            _m78 = True
                            MpCanvas.cv = 1
                            MpCanvas.i_I(3)
                            self.c_I(1287)
                            raise _Brk_block0_2989()
                        if _m78 or _sw77 == 2:
                            _m78 = True
                            MpCanvas.cv = 1
                            MpCanvas.i_I(3)
                            self.c_I(1289)
                            raise _Brk_block0_2989()
                        if _m78 or _sw77 == 3:
                            _m78 = True
                            MpCanvas.cv = 1
                            MpCanvas.i_I(3)
                            self.c_I(1298)
                            raise _Brk_block0_2989()
                        if _m78 or _sw77 == 4:
                            _m78 = True
                            MpCanvas.C = 0
                            MpCanvas.B = 0
                            MpCanvas.bG = MpCanvas.cF
                            self.k_I(84)
                            raise _Brk_block0_2989()
                        if _m78 or _sw77 == 5:
                            _m78 = True
                            MpCanvas.C = 0
                            MpCanvas.bG = MpCanvas.cE
                            self.k_I(85)
                        break
                    return
                if _m68 or _sw67 == 82:
                    _m68 = True
                    MpCanvas.cv = 5
                    MpCanvas.i_I(3)
                    self.c_I(1291)
                    return
                if _m68 or _sw67 == 84:
                    _m68 = True
                    return
                if _m68 or _sw67 == 86:
                    _m68 = True
                    _sw79 = MpCanvas.dU[MpCanvas.dW]
                    _m80 = False
                    while True:
                        if _m80 or _sw79 == 0:
                            _m80 = True
                            MpCanvas.cv = 5
                            MpCanvas.i_I(3)
                            self.c_I(1280)
                            raise _Brk_block0_2989()
                        if _m80 or _sw79 == 1:
                            _m80 = True
                            self.m_I(1)
                        break
                    return
                if _m68 or _sw67 == 88:
                    _m68 = True
                    _sw81 = MpCanvas.dU[MpCanvas.dW]
                    _m82 = False
                    while True:
                        if _m82 or _sw81 == 0:
                            _m82 = True
                            if MpCanvas.cs == (-4):
                                if _inc(MpCanvas, 'an', 1) <= 2:
                                    break
                                MpCanvas.an = 0
                                raise _Brk_block0_2989()
                            if (MpCanvas.cs != (-3)) or (_inc(MpCanvas, 'an', -1) >= 0):
                                break
                            MpCanvas.an = 2
                            raise _Brk_block0_2989()
                        if _m82 or _sw81 == 1:
                            _m82 = True
                            if (MpCanvas.cs != (-3)) and (MpCanvas.cs != (-4)):
                                break
                            MpCanvas.ap = imod(((MpCanvas.ap + 1)), 2)
                            raise _Brk_block0_2989()
                        if _m82 or _sw81 == 2:
                            _m82 = True
                            if MpCanvas.cs == (-3):
                                self.ai_v()
                                raise _Brk_block0_2989()
                            if MpCanvas.cs != (-4):
                                break
                            self.aj_v()
                        break
                    return
                if _m68 or _sw67 == 87:
                    _m68 = True
                    self.k_I(89)
                    return
                if _m68 or _sw67 == 20:
                    _m68 = True
                    _sw83 = MpCanvas.dU[MpCanvas.dW]
                    if _sw83 == 0:
                        MpCanvas.bz = 0
                    elif _sw83 == 1:
                        MpCanvas.bz = 1
                    self.k_I(21)
                break
        except _Brk_block0_2989:
            pass

    def r_v(self):  # g.java:3746
        self.e_v()
        self.c_GIIIII(MpCanvas.e, MpCanvas.cW, MpCanvas.cX, 116, 76, 0)
        n2 = 0
        while n2 < 4:
            self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((MpCanvas.cX - 31) + (12 * n2)), MpCanvas.bF[n2], 0xFFFFFF)
            n2 = n2 + 1
        self.r_I((MpCanvas.cX + 22))

    def s_v(self):  # g.java:3757
        MpCanvas.cL = 0
        while MpCanvas.cL < 4:
            if MpCanvas.bQ[MpCanvas.cL] and (MpCanvas.cL != MpCanvas.S):
                _sw84 = MpCanvas.cc[MpCanvas.cL]
                if _sw84 == 0:
                    self.b_G(MpCanvas.e)
                elif _sw84 in (1, 4):
                    self.t_v()
                elif _sw84 == 5:
                    self.u_v()
                elif _sw84 == 6:
                    self.v_v()
                else:
                    self.x_v()
            MpCanvas.cL = MpCanvas.cL + 1
        MpCanvas.cL = MpCanvas.S
        _sw85 = MpCanvas.cc[MpCanvas.S]
        if _sw85 in (2, 28):
            self.w_v()
            return
        elif _sw85 == 6:
            self.v_v()
            return
        self.x_v()

    def t_v(self):  # g.java:3801
        MpCanvas.cC = MpCanvas.cc[MpCanvas.cL]
        if MpCanvas.ca[MpCanvas.cL] == 2:
            MpCanvas.cC = (MpCanvas.cC + 21)
        MpCanvas.cn[MpCanvas.cL] = Consts.eg[MpCanvas.cC]
        n2 = MpCanvas.cL
        MpCanvas.ck[n2] = (MpCanvas.ck[n2] - 2)
        MpCanvas.cm[MpCanvas.cL] = (-1)
        self.c_GI(MpCanvas.e, MpCanvas.cL)

    def u_v(self):  # g.java:3813
        MpCanvas.cC = (26 if (MpCanvas.ca[MpCanvas.cL] == 2) else 5)
        MpCanvas.cn[MpCanvas.cL] = Consts.eg[MpCanvas.cC]
        if MpCanvas.cd[MpCanvas.cL] == 0:
            n2 = MpCanvas.cL
            MpCanvas.ck[n2] = (MpCanvas.ck[n2] - 6)
            self.t_I(3)
        elif MpCanvas.cd[MpCanvas.cL] == 1:
            n3 = MpCanvas.cL
            MpCanvas.ck[n3] = (MpCanvas.ck[n3] - 2)
        MpCanvas.cm[MpCanvas.cL] = (-1)
        self.c_GI(MpCanvas.e, MpCanvas.cL)

    def v_v(self):  # g.java:3828
        MpCanvas.cC = (27 if (MpCanvas.ca[MpCanvas.cL] == 2) else 6)
        MpCanvas.cn[MpCanvas.cL] = (Consts.eg[MpCanvas.cC] + MpCanvas.Q)
        MpCanvas.cm[MpCanvas.cL] = (-1)
        self.c_GI(MpCanvas.e, MpCanvas.cL)

    def w_v(self):  # g.java:3835
        MpCanvas.cn[MpCanvas.cL] = (Consts.eg[23] if (MpCanvas.ca[MpCanvas.cL] == 2) else Consts.eg[2])
        n2 = MpCanvas.cL
        MpCanvas.ck[n2] = (MpCanvas.ck[n2] + MpCanvas.bl)
        n3 = MpCanvas.cL
        MpCanvas.cl[n3] = (MpCanvas.cl[n3] + MpCanvas.bm)
        MpCanvas.cm[MpCanvas.cL] = (-1)
        self.c_GI(MpCanvas.e, MpCanvas.cL)

    def x_v(self):  # g.java:3845
        MpCanvas.cC = MpCanvas.cc[MpCanvas.cL]
        if (MpCanvas.ca[MpCanvas.cL] == 2) and (MpCanvas.cC == 3):
            MpCanvas.cC = 24
        if (MpCanvas.cC == 12) and (MpCanvas.Q >= 4):
            MpCanvas.bo = MpCanvas.Q
            MpCanvas.Q = 4
        MpCanvas.cn[MpCanvas.cL] = (Consts.eg[MpCanvas.cC] + MpCanvas.Q)
        MpCanvas.bJ = Consts.ep[MpCanvas.cC][((3 * MpCanvas.Q) + 1)]
        n2 = MpCanvas.cL
        MpCanvas.ck[n2] = (MpCanvas.ck[n2] + ((((-1) if (((MpCanvas.bJ & 0x80)) > 0) else 1)) * ((MpCanvas.bJ & 0x7F))))
        MpCanvas.bJ = Consts.ep[MpCanvas.cC][((3 * MpCanvas.Q) + 2)]
        n3 = MpCanvas.cL
        MpCanvas.cl[n3] = (MpCanvas.cl[n3] + ((((-1) if (((MpCanvas.bJ & 0x80)) > 0) else 1)) * ((MpCanvas.bJ & 0x7F))))
        self.c_GI(MpCanvas.e, MpCanvas.cL)
        if (MpCanvas.cC == 12) and (MpCanvas.Q >= 4):
            MpCanvas.Q = MpCanvas.bo

    def b_G(self, graphics):  # g.java:3867
        if MpCanvas.bW[MpCanvas.cL] > 0:
            if ((((MpCanvas.cY == 104) or (MpCanvas.cY == 105))) and (MpCanvas.ca[MpCanvas.cL] != 2)) and (MpCanvas.aU == 1):
                if MpCanvas.da < 3:
                    MpCanvas.cn[MpCanvas.cL] = (Consts.eg[MpCanvas.cC] + MpCanvas.da)
                    n2 = MpCanvas.cL
                    MpCanvas.ck[n2] = (MpCanvas.ck[n2] + ((((-1) if (((MpCanvas.bJ & 0x80)) > 0) else 1)) * ((MpCanvas.bJ & 0x7F))))
                    n3 = MpCanvas.cL
                    MpCanvas.cl[n3] = (MpCanvas.cl[n3] + ((((-1) if (((MpCanvas.bJ & 0x80)) > 0) else 1)) * ((MpCanvas.bJ & 0x7F))))
            else:
                if imod(MpCanvas.da, 4) == MpCanvas.co[MpCanvas.cL]:
                    MpCanvas.cn[MpCanvas.cL] = imod(idiv(MpCanvas.da, 4), 2)
                if (MpCanvas.cn[MpCanvas.cL] != 0) and (MpCanvas.cn[MpCanvas.cL] != 1):
                    MpCanvas.cn[MpCanvas.cL] = 0
        else:
            MpCanvas.cn[MpCanvas.cL] = (Consts.eg[6] + 1)
        MpCanvas.cm[MpCanvas.cL] = (-1)
        if ((MpCanvas.cc[MpCanvas.S] == 12) and (MpCanvas.cL == MpCanvas.T)) and (MpCanvas.Q >= 4):
            MpCanvas.cm[MpCanvas.cL] = ((10 + MpCanvas.Q) - 4)
        self.c_GI(graphics, MpCanvas.cL)

    def b_GI(self, graphics, n2):  # g.java:3895
        MpCanvas.cL = 0
        while MpCanvas.cL < 4:
            try:
                try:
                    if not MpCanvas.bQ[MpCanvas.cL]:
                        raise _Brk_block4_3348()
                    if imod(MpCanvas.bR[MpCanvas.cL], 2) == n2:
                        raise _Brk_block5_3348()
                    if n2 != 2:
                        raise _Brk_block4_3348()
                    bl = ((imod(MpCanvas.bR[MpCanvas.cL], 2) == MpCanvas.bR[0]) if (MpCanvas.aU == 1) else (imod(MpCanvas.bR[MpCanvas.cL], 2) != MpCanvas.bR[0]))
                    if not bl:
                        raise _Brk_block4_3348()
                except _Brk_block5_3348:
                    pass
                self.c_GIIIII(graphics, (0 if (imod(MpCanvas.bR[MpCanvas.cL], 2) == 0) else (MpCanvas.cQ - 60)), (12 if (idiv(MpCanvas.bR[MpCanvas.cL], 2) == 0) else ((MpCanvas.cR - 12) - 15)), 60, 15, 1)
                self.a_IITI((30 if (imod(MpCanvas.bR[MpCanvas.cL], 2) == 0) else (MpCanvas.cQ - 30)), (14 if (idiv(MpCanvas.bR[MpCanvas.cL], 2) == 0) else (((MpCanvas.cR - 12) - 15) + 2)), MpCanvas.bM[MpCanvas.cL], 16400640)
                MpCanvas.cO = MpCanvas.cW
                MpCanvas.cP = (38 if (idiv(MpCanvas.bR[MpCanvas.cL], 2) == 0) else (((MpCanvas.cR - 12) - 15) - 11))
                self.c_GIIIII(graphics, MpCanvas.cO, MpCanvas.cP, MpCanvas.cQ, 22, 0)
                self.a_IITI(MpCanvas.cO, (MpCanvas.cP - 5), (MpCanvas.bO[MpCanvas.cL] if (n2 == 2) else MpCanvas.bN[MpCanvas.cL]), 0xFFFFFF)
            except _Brk_block4_3348:
                pass
            MpCanvas.cL = MpCanvas.cL + 1

    def y_v(self):  # g.java:3917
        self.c_GIIIII(MpCanvas.e, MpCanvas.cW, MpCanvas.cX, 78, 86, 0)
        self.a_GIITI(MpCanvas.e, MpCanvas.cW, (MpCanvas.cX - 34), MpCanvas.bM[MpCanvas.ct], 0xFFFFFF)
        self.a_GIITI(MpCanvas.e, MpCanvas.cW, (MpCanvas.cX - 20), _js(_js(Consts.eX[27], "."), MpCanvas.bS[MpCanvas.ct]), 0xFFFFFF)
        self.f_GIII(MpCanvas.e, (MpCanvas.cW + 22), (MpCanvas.cX + 12), MpCanvas.bT[MpCanvas.ct])
        self.b_GIITI(MpCanvas.e, (MpCanvas.cW - 27), (MpCanvas.cX + 11), Consts.eX[49], 0xFFFFFF)
        self.f_GIII(MpCanvas.e, (MpCanvas.cW + 22), (MpCanvas.cX + 24), MpCanvas.bU[MpCanvas.ct])
        self.b_GIITI(MpCanvas.e, (MpCanvas.cW - 27), (MpCanvas.cX + 23), Consts.eX[50], 0xFFFFFF)

    def c_G(self, graphics):  # g.java:3927
        MpCanvas.cL = 0
        while MpCanvas.cL < 4:
            if MpCanvas.bQ[MpCanvas.cL]:
                self.b_G(graphics)
            MpCanvas.cL = MpCanvas.cL + 1

    def d_G(self, graphics):  # g.java:3937
        if imod(MpCanvas.bR[MpCanvas.bA], 2) == 0:
            self.a_GIITI(graphics, 30, (14 if (idiv(MpCanvas.bR[MpCanvas.bA], 2) == 0) else (((MpCanvas.cR - 12) - 15) + 2)), (MpCanvas.bM[MpCanvas.bA] if ((len(MpCanvas.bP[MpCanvas.bA]) == 0) or (imod(MpCanvas.aR, 2) == 0)) else MpCanvas.bP[MpCanvas.bA]), 16400640)
            if imod(MpCanvas.da, 2) == 0:
                MpCanvas.c_GIIIM(graphics, Consts.eq[48], (((19 if (idiv(MpCanvas.bR[MpCanvas.bA], 2) == 0) else (MpCanvas.cR - 19))) + Consts.er[48]), 12, MpCanvas.df[48])
                return
            MpCanvas.a_GIIMII(graphics, (Consts.eq[48] + 1), (((19 if (idiv(MpCanvas.bR[MpCanvas.bA], 2) == 0) else (MpCanvas.cR - 19))) + Consts.er[48]), MpCanvas.df[48], 12, 1)
            return
        self.a_GIITI(graphics, (MpCanvas.cQ - 30), (14 if (idiv(MpCanvas.bR[MpCanvas.bA], 2) == 0) else (((MpCanvas.cR - 12) - 15) + 2)), (MpCanvas.bM[MpCanvas.bA] if ((len(MpCanvas.bP[MpCanvas.bA]) == 0) or (imod(MpCanvas.aR, 2) == 0)) else MpCanvas.bP[MpCanvas.bA]), 16400640)
        if imod(MpCanvas.da, 2) == 0:
            MpCanvas.a_GIIIM(graphics, (MpCanvas.cQ - ((1 + Consts.eq[48]))), (((19 if (idiv(MpCanvas.bR[MpCanvas.bA], 2) == 0) else (MpCanvas.cR - 19))) + Consts.er[48]), 12, MpCanvas.df[48])
            return
        MpCanvas.b_GIIIM(graphics, (MpCanvas.cQ - ((2 + Consts.eq[48]))), (((19 if (idiv(MpCanvas.bR[MpCanvas.bA], 2) == 0) else (MpCanvas.cR - 19))) + Consts.er[48]), 12, MpCanvas.df[48])

    def z_v(self):  # g.java:3955
        self.c_GIIIII(MpCanvas.e, MpCanvas.cW, MpCanvas.cX, 102, 86, 0)
        self.a_IITI(MpCanvas.cW, (MpCanvas.cX - 30), MpCanvas.bH, 0xFFFFFF)
        self.a_IITI(MpCanvas.cW, (MpCanvas.cX - 15), _js(_js(_js(Consts.eX[26], MpCanvas.aQ), "/"), MpCanvas.aP), 0xFFFFFF)
        MpCanvas.cL = 1
        while MpCanvas.cL < 4:
            if MpCanvas.bQ[MpCanvas.cL]:
                if MpCanvas.bR[MpCanvas.cL] == 1:
                    self.a_IITI((MpCanvas.cW - 24), (MpCanvas.cX + 4), MpCanvas.bM[MpCanvas.cL], 0xFFFFFF)
                    self.b_IITI((MpCanvas.cW + 4), (MpCanvas.cX + 4), _js(_js(Consts.eX[27], ""), MpCanvas.bS[MpCanvas.cL]), 0xFFFFFF)
                elif MpCanvas.bR[MpCanvas.cL] == 3:
                    self.a_IITI((MpCanvas.cW - 24), (MpCanvas.cX + 20), MpCanvas.bM[MpCanvas.cL], 0xFFFFFF)
                    self.b_IITI((MpCanvas.cW + 4), (MpCanvas.cX + 20), _js(_js(Consts.eX[27], ""), MpCanvas.bS[MpCanvas.cL]), 0xFFFFFF)
            MpCanvas.cL = MpCanvas.cL + 1

    @staticmethod
    def A_v():  # g.java:3974
        MpCanvas.bJ = imod(abs(MpCanvas.h.nextInt()), 3)
        _sw86 = MpCanvas.bJ
        if _sw86 == 0:
            MpCanvas.cz = 4
        elif _sw86 == 1:
            MpCanvas.cz = 8
        else:
            MpCanvas.cz = 5
        MpCanvas.b_I(1)
        MpCanvas.cA = (MpCanvas.cW - 44)
        MpCanvas.bt = True

    def e_G(self, graphics):  # g.java:3994
        if MpCanvas.bt:
            n2 = MpCanvas.cX
            if MpCanvas.bz == 0:
                n2 = (MpCanvas.cT - 26)
            self.c_GIIIII(graphics, MpCanvas.cW, (n2 + 3), 110, 38, 0)
            Draw.a_GMIII(graphics, MpCanvas.df[35], ((MpCanvas.cW - 44) + Consts.eq[35]), (n2 + Consts.er[35]), 0)
            Draw.a_GMIII(graphics, MpCanvas.df[36], ((MpCanvas.cW - 44) + Consts.eq[36]), (n2 + Consts.er[36]), 0)
            Draw.a_GMIII(graphics, MpCanvas.df[37], ((MpCanvas.cW - 44) + Consts.eq[37]), (n2 + Consts.er[37]), 0)

    def f_G(self, graphics):  # g.java:4007
        n2 = MpCanvas.cX
        if MpCanvas.bz == 0:
            n2 = (MpCanvas.cT - 26)
        if MpCanvas.cY == 98:
            if MpCanvas.aS == 100:
                Draw.a_GMIII(graphics, MpCanvas.df[52], (((MpCanvas.cW - 44) + 72) + Consts.eq[52]), (n2 + Consts.er[52]), 0)
                self.t_I(0)
            elif MpCanvas.aS == 20:
                Draw.a_GMIII(graphics, MpCanvas.df[53], (((MpCanvas.cW - 44) + 72) + Consts.eq[53]), (n2 + Consts.er[53]), 0)
            else:
                Draw.a_GMIII(graphics, MpCanvas.df[49], ((MpCanvas.cA - 20) + Consts.eu[35]), ((n2 - 11) + Consts.ev[35]), 0)
                self.t_I(0)
        if imod(MpCanvas.da, 2) == 0:
            Draw.a_GMIII(graphics, MpCanvas.df[38], (((MpCanvas.cW - 44) + 72) + Consts.eq[38]), (n2 + Consts.er[38]), 0)
        Draw.a_GMIII(graphics, MpCanvas.df[34], (MpCanvas.cA + Consts.eq[34]), (n2 + Consts.er[34]), 0)
        if (MpCanvas.cY == 97) and (MpCanvas.cA > ((MpCanvas.cW - 44) + 72)):
            self.C_v()

    def B_v(self):  # g.java:4032
        MpCanvas.d = 0
        MpCanvas.i_I(97)

    def C_v(self):  # g.java:4037
        MpCanvas.d = 0
        if MpCanvas.bB > 2:
            MpCanvas.aS = 0
        else:
            if (((MpCanvas.cz == 6) or (MpCanvas.cz == 7))) and (abs((((MpCanvas.cW - 44) + 72) - MpCanvas.cA)) <= idiv(MpCanvas.cz, 2)):
                MpCanvas.cA = ((MpCanvas.cW - 44) + 72)
            MpCanvas.aS = ((((20 + MpCanvas.cA) - MpCanvas.cW) + 44) if (MpCanvas.cA < ((MpCanvas.cW - 44) + 72)) else ((100 if (MpCanvas.cA == ((MpCanvas.cW - 44) + 72)) else 20)))
        MpCanvas.i_I(98)

    @staticmethod
    def a_GAMALaI(graphics, imageArray, aArray, n2):  # g.java:4050
        a2 = aArray[0]
        n3 = 0
        if n2 >= 400:
            n3 = (n2 - 400)
        elif n2 >= 300:
            n3 = (n2 - 300)
        elif n2 >= 200:
            n3 = (n2 - 200)
            a2 = aArray[2]
        elif n2 >= 100:
            n3 = (n2 - 100)
            a2 = aArray[1]
        else:
            n3 = n2
        if MpCanvas.bn:
            Draw.a_GMIIIIII(graphics, imageArray[1], (MpCanvas.cQ - (((MpCanvas.cU - a2.g[n3]) + a2.e[n3]))), (MpCanvas.cV - a2.h[n3]), a2.e[n3], a2.f[n3], a2.c[n3], a2.d[n3])
            return
        Draw.a_GMIIIIII(graphics, imageArray[0], (MpCanvas.cU - a2.g[n3]), (MpCanvas.cV - a2.h[n3]), a2.e[n3], a2.f[n3], a2.c[n3], a2.d[n3])

    def c_GI(self, graphics, n2):  # g.java:4073
        n3 = 0
        MpCanvas.bn = (imod(MpCanvas.bR[n2], 2) != 0)
        MpCanvas.cU = MpCanvas.ck[n2]
        MpCanvas.cV = MpCanvas.cl[n2]
        self.a_IZ(n2, True)
        if MpCanvas.ca[n2] != 2:
            self.a_AMALaT(MpCanvas.dF, MpCanvas.dG, "sprshadow")
            MpCanvas.a_GAMALaI(graphics, MpCanvas.dF, MpCanvas.dG, MpCanvas.cn[n2])
        bl = False
        if MpCanvas.ca[n2] == 2:
            bl = Consts.eo[imod(MpCanvas.cn[n2], 100)]
            if bl:
                self.a_AMALaTI(MpCanvas.dJ, MpCanvas.dK, "spr_wp_mon", 0)
                MpCanvas.a_GAMALaI(graphics, MpCanvas.dJ, MpCanvas.dK, MpCanvas.cn[n2])
        else:
            n3 = idiv(MpCanvas.cn[n2], 100)
            if MpCanvas.bY[n2] == 0:
                if n3 == 2:
                    bl = Consts.ek[imod(MpCanvas.cn[n2], 100)]
            else:
                bl = (Consts.em[imod(MpCanvas.cn[n2], 100)] if (n3 == 1) else ((Consts.en[imod(MpCanvas.cn[n2], 100)] if (n3 == 2) else Consts.el[imod(MpCanvas.cn[n2], 100)])))
            if bl:
                self.a_AMALaT(MpCanvas.dy[MpCanvas.bY[n2]], MpCanvas.dz[MpCanvas.bY[n2]], _js("sprwp", ((MpCanvas.bY[n2] + 1))))
                MpCanvas.a_GAMALaI(graphics, MpCanvas.dy[MpCanvas.bY[n2]], MpCanvas.dz[MpCanvas.bY[n2]], MpCanvas.cn[n2])
        if MpCanvas.ca[n2] == 2:
            self.a_AMALaTI(MpCanvas.dH, MpCanvas.dI, "spr_mon", 0)
            MpCanvas.a_GAMALaI(graphics, MpCanvas.dH, MpCanvas.dI, MpCanvas.cn[n2])
        else:
            self.a_AMALaT(MpCanvas.dF, MpCanvas.dG, "sprshadow")
            MpCanvas.a_GAMALaI(graphics, MpCanvas.dF, MpCanvas.dG, MpCanvas.cn[n2])
            self.a_AMALaT(MpCanvas.du, MpCanvas.dv, "sprbody")
            MpCanvas.a_GAMALaI(graphics, MpCanvas.du, MpCanvas.dv, MpCanvas.cn[n2])
        n3 = 0
        if MpCanvas.ca[n2] != 2:
            if MpCanvas.ca[n2] == 0:
                n3 = MpCanvas.bZ[n2]
            self.a_AMALaT(MpCanvas.dw[n3], MpCanvas.dx[n3], _js("sprhead", ((n3 + 1))))
            MpCanvas.a_GAMALaI(graphics, MpCanvas.dw[n3], MpCanvas.dx[n3], MpCanvas.cn[n2])
        if MpCanvas.bQ[n2] and (MpCanvas.cY != 105):
            _sw87 = MpCanvas.cp[n2]
            if _sw87 == 11:
                self.V_v()
                MpCanvas.e_GI(graphics, 0)
            elif _sw87 == 12:
                self.V_v()
                MpCanvas.e_GI(graphics, 1)
            elif _sw87 == 13:
                self.V_v()
                MpCanvas.e_GI(graphics, 2)
        if not bl:
            if MpCanvas.ca[n2] == 2:
                self.a_AMALaTI(MpCanvas.dJ, MpCanvas.dK, "spr_wp_mon", 0)
                MpCanvas.a_GAMALaI(graphics, MpCanvas.dJ, MpCanvas.dK, MpCanvas.cn[n2])
            else:
                self.a_AMALaT(MpCanvas.dy[MpCanvas.bY[n2]], MpCanvas.dz[MpCanvas.bY[n2]], _js("sprwp", ((MpCanvas.bY[n2] + 1))))
                MpCanvas.a_GAMALaI(graphics, MpCanvas.dy[MpCanvas.bY[n2]], MpCanvas.dz[MpCanvas.bY[n2]], MpCanvas.cn[n2])
        self.a_IZ(n2, False)

    def a_IZ(self, n2, bl):  # g.java:4151
        if MpCanvas.ca[n2] == 2:
            if not bl:
                self.a_AMALaTI(MpCanvas.dN, MpCanvas.dO, "spr_sword_mon", 0)
                MpCanvas.a_GAMALaI(MpCanvas.e, MpCanvas.dN, MpCanvas.dO, MpCanvas.cn[n2])
                self.a_AMALaTI(MpCanvas.dL, MpCanvas.dM, "spr_eff_mon", 0)
                MpCanvas.a_GAMALaI(MpCanvas.e, MpCanvas.dL, MpCanvas.dM, MpCanvas.cn[n2])
                return
        else:
            n3 = 0
            bl2 = False
            if not bl:
                self.a_AMALaT(MpCanvas.dA[MpCanvas.bY[n2]], MpCanvas.dB[MpCanvas.bY[n2]], _js("sprsword", ((MpCanvas.bY[n2] + 1))))
                MpCanvas.a_GAMALaI(MpCanvas.e, MpCanvas.dA[MpCanvas.bY[n2]], MpCanvas.dB[MpCanvas.bY[n2]], MpCanvas.cn[n2])
                self.a_AMALaT(MpCanvas.dC[0], MpCanvas.dD[0], "spreff1")
                MpCanvas.a_GAMALaI(MpCanvas.e, MpCanvas.dC[0], MpCanvas.dD[0], MpCanvas.cn[n2])
            if bl == ((bl2 := (Consts.ei[imod(MpCanvas.cn[n2], 100)] if (((n3 := idiv(MpCanvas.cn[n2], 100))) == 1) else ((Consts.ej[imod(MpCanvas.cn[n2], 100)] if (n3 == 2) else False))))):
                self.a_AMALaT(MpCanvas.dC[1], MpCanvas.dD[1], "spreff2")
                MpCanvas.a_GAMALaI(MpCanvas.e, MpCanvas.dC[1], MpCanvas.dD[1], MpCanvas.cn[n2])

    def D_v(self):  # g.java:4176
        if MpCanvas.X >= 5:
            MpCanvas.X = (-1)
            MpCanvas.cL = 0
            while MpCanvas.cL < 4:
                if MpCanvas.bQ[MpCanvas.cL] and ((((MpCanvas.cL == MpCanvas.S) or (MpCanvas.cL == MpCanvas.T)) or (MpCanvas.cL == MpCanvas.U))):
                    if MpCanvas.bW[MpCanvas.cL] != MpCanvas.cf[MpCanvas.cL]:
                        MpCanvas.bW[MpCanvas.cL] = MpCanvas.cf[MpCanvas.cL]
                    if MpCanvas.bX[MpCanvas.cL] != MpCanvas.cg[MpCanvas.cL]:
                        MpCanvas.bX[MpCanvas.cL] = MpCanvas.cg[MpCanvas.cL]
                MpCanvas.cL = MpCanvas.cL + 1
        if MpCanvas.Q >= MpCanvas.R:
            MpCanvas.Q = 0
            _sw88 = MpCanvas.cc[MpCanvas.S]
            _m89 = False
            while True:
                if _m89 or _sw88 in (2, 17, 18, 19):
                    _m89 = True
                    MpCanvas.ck[MpCanvas.S] = (MpCanvas.cQ - 67)
                    MpCanvas.cl[MpCanvas.S] = (MpCanvas.cX + 65)
                    if MpCanvas.bz != 0:
                        n2 = MpCanvas.S
                        MpCanvas.cl[n2] = (MpCanvas.cl[n2] + ((((-1) if (idiv(MpCanvas.cK[(12 + MpCanvas.bC)], 2) == 0) else 1)) * 23))
                    _sw90 = MpCanvas.cK[(4 + MpCanvas.bC)]
                    if _sw90 == 3:
                        MpCanvas.cc[MpCanvas.S] = 9
                    elif _sw90 == 4:
                        MpCanvas.cc[MpCanvas.S] = 10
                    elif _sw90 == 5:
                        MpCanvas.cc[MpCanvas.S] = 11
                    elif _sw90 == 6:
                        MpCanvas.cc[MpCanvas.S] = 14
                    elif _sw90 == 7:
                        MpCanvas.cc[MpCanvas.S] = 15
                    elif _sw90 == 0:
                        MpCanvas.cc[MpCanvas.S] = 3
                    break
                if _m89 or _sw88 == 8:
                    _m89 = True
                    _sw91 = MpCanvas.cK[(4 + MpCanvas.bC)]
                    _m92 = False
                    while True:
                        if _m92 or _sw91 in (3, 4, 5):
                            _m92 = True
                            MpCanvas.cc[MpCanvas.S] = 2
                            MpCanvas.bl = idiv((((MpCanvas.cQ - 67) - 42)), Consts.eh[MpCanvas.cc[MpCanvas.S]])
                            if MpCanvas.bz == 0:
                                MpCanvas.bm = 0
                                break
                            if idiv(MpCanvas.bR[MpCanvas.S], 2) == idiv(MpCanvas.cK[(12 + MpCanvas.bC)], 2):
                                MpCanvas.bm = 0
                                break
                            if idiv(MpCanvas.bR[MpCanvas.S], 2) == 0:
                                MpCanvas.bm = idiv(46, Consts.eh[MpCanvas.cc[MpCanvas.S]])
                                break
                            MpCanvas.bm = idiv((-46), Consts.eh[MpCanvas.cc[MpCanvas.S]])
                            break
                        if _m92 or _sw91 in (6, 7):
                            _m92 = True
                            if MpCanvas.bz == 0:
                                MpCanvas.cc[MpCanvas.S] = 17
                                break
                            if idiv(MpCanvas.cK[(12 + MpCanvas.bC)], 2) == idiv(MpCanvas.cK[(0 + MpCanvas.bC)], 2):
                                MpCanvas.cc[MpCanvas.S] = 17
                                break
                            if idiv(MpCanvas.cK[(12 + MpCanvas.bC)], 2) == 1:
                                MpCanvas.cc[MpCanvas.S] = 18
                                break
                            MpCanvas.cc[MpCanvas.S] = 19
                            break
                        if _m92 or _sw91 == 8:
                            _m92 = True
                            MpCanvas.cc[MpCanvas.S] = 20
                        break
                    break
                if _m89 or _sw88 == 20:
                    _m89 = True
                    _sw93 = MpCanvas.cK[(4 + MpCanvas.bC)]
                    if _sw93 == 8:
                        MpCanvas.cc[MpCanvas.S] = 16
                    break
                if _m89 or _sw88 in (3, 9, 10, 11, 14, 15, 16):
                    _m89 = True
                    if (MpCanvas.cK[(28 + MpCanvas.bC)] == 3) and (MpCanvas.bR[MpCanvas.S] == MpCanvas.cK[(0 + MpCanvas.bC)]):
                        MpCanvas.bJ = MpCanvas.S
                        MpCanvas.S = MpCanvas.T
                        MpCanvas.T = MpCanvas.bJ
                        MpCanvas.cc[MpCanvas.S] = 3
                        MpCanvas.V = 1
                        break
                    MpCanvas.X = 0
                    if MpCanvas.cK[(28 + MpCanvas.bC)] == 3:
                        MpCanvas.bJ = MpCanvas.S
                        MpCanvas.S = MpCanvas.T
                        MpCanvas.T = MpCanvas.bJ
                        MpCanvas.cc[MpCanvas.T] = 0
                        MpCanvas.h_I(MpCanvas.T)
                    MpCanvas.cc[MpCanvas.S] = 28
                    MpCanvas.bl = idiv(((42 - MpCanvas.ck[MpCanvas.S])), Consts.eh[MpCanvas.cc[MpCanvas.S]])
                    if MpCanvas.bz == 0:
                        MpCanvas.bm = 0
                        break
                    if idiv(MpCanvas.bR[MpCanvas.S], 2) == idiv(MpCanvas.cK[(12 + MpCanvas.bC)], 2):
                        MpCanvas.bm = 0
                        break
                    if idiv(MpCanvas.bR[MpCanvas.S], 2) == 0:
                        MpCanvas.bm = idiv((-46), Consts.eh[MpCanvas.cc[MpCanvas.S]])
                        break
                    MpCanvas.bm = idiv(46, Consts.eh[MpCanvas.cc[MpCanvas.S]])
                    break
                if _m89 or _sw88 in (12, 13, 28):
                    _m89 = True
                    MpCanvas.h_I(MpCanvas.S)
                    MpCanvas.bJ = (-1)
                    MpCanvas.cL = 0
                    while MpCanvas.cL < 4:
                        if MpCanvas.bQ[MpCanvas.cL]:
                            if (MpCanvas.cc[MpCanvas.S] == 13) and (imod(MpCanvas.bR[MpCanvas.S], 2) == imod(MpCanvas.bR[MpCanvas.cL], 2)):
                                MpCanvas.cp[MpCanvas.cL] = MpCanvas.cK[(4 + MpCanvas.bC)]
                                MpCanvas.cq[MpCanvas.cL] = 3
                            if (MpCanvas.bW[MpCanvas.cL] == 0) and (MpCanvas.cj[MpCanvas.cL] != 0):
                                MpCanvas.bJ = MpCanvas.cL
                                MpCanvas.cc[MpCanvas.bJ] = 6
                                if imod(MpCanvas.bR[MpCanvas.cL], 2) == imod(MpCanvas.bR[0], 2):
                                    MpCanvas.bb = MpCanvas.bb - 1
                                else:
                                    MpCanvas.bc = MpCanvas.bc - 1
                        MpCanvas.cL = MpCanvas.cL + 1
                    if MpCanvas.bJ > 0:
                        if MpCanvas.cc[MpCanvas.S] != 6:
                            MpCanvas.cc[MpCanvas.S] = 0
                        MpCanvas.S = MpCanvas.bJ
                        break
                    MpCanvas.bC = MpCanvas.bC + 1
                    self.E_v()
                    break
                if _m89 or _sw88 == 6:
                    _m89 = True
                    MpCanvas.bC = MpCanvas.bC + 1
                    self.E_v()
                break
            MpCanvas.R = Consts.eh[MpCanvas.cc[MpCanvas.S]]
        if MpCanvas.cc[MpCanvas.S] != 6:
            self.F_v()

    def E_v(self):  # g.java:4372
        if MpCanvas.aT == 0:
            MpCanvas.i_I(100)
            return
        if MpCanvas.bC < MpCanvas.aT:
            MpCanvas.i_I(101)
            return
        MpCanvas.i_I(93)

    def F_v(self):  # g.java:4388
        if ((MpCanvas.cc[MpCanvas.S] != 12) and (MpCanvas.cc[MpCanvas.S] != 13)) and (MpCanvas.cK[(28 + MpCanvas.bC)] != 3):
            if (MpCanvas.T != (-1)) and (MpCanvas.cc[MpCanvas.T] != 0):
                n2 = MpCanvas.T
                MpCanvas.cd[n2] = (MpCanvas.cd[n2] + 1)
                if MpCanvas.cd[MpCanvas.T] >= MpCanvas.ce[MpCanvas.T]:
                    MpCanvas.cc[MpCanvas.T] = 0
                    MpCanvas.h_I(MpCanvas.T)
            if (MpCanvas.U != (-1)) and (MpCanvas.cc[MpCanvas.U] != 0):
                n3 = MpCanvas.U
                MpCanvas.cd[n3] = (MpCanvas.cd[n3] + 1)
                if MpCanvas.cd[MpCanvas.U] >= MpCanvas.ce[MpCanvas.U]:
                    MpCanvas.cc[MpCanvas.U] = 0
                    MpCanvas.h_I(MpCanvas.U)
        _sw94 = MpCanvas.cc[MpCanvas.S]
        _m95 = False
        while True:
            if _m95 or _sw94 in (3, 9, 10, 11, 14):
                _m95 = True
                _sw96 = MpCanvas.V
                _m97 = False
                while True:
                    if _m97 or _sw96 in (1, 4):
                        _m97 = True
                        if (MpCanvas.cc[MpCanvas.S] == 11) and (MpCanvas.Q == 17):
                            self.G_v()
                            MpCanvas.ce[MpCanvas.T] = 3
                            return
                        if imod(MpCanvas.Q, 2) != 1:
                            return
                        if (MpCanvas.cc[MpCanvas.S] == 11) and (MpCanvas.Q > 10):
                            return
                        self.G_v()
                        MpCanvas.ce[MpCanvas.T] = 2
                        return
                    if _m97 or _sw96 == 5:
                        _m97 = True
                        if MpCanvas.cK[(28 + MpCanvas.bC)] == 3:
                            if MpCanvas.Q != 0:
                                return
                            MpCanvas.cc[MpCanvas.T] = 5
                            MpCanvas.cd[MpCanvas.T] = 0
                            MpCanvas.ce[MpCanvas.T] = MpCanvas.R
                            return
                        else:
                            if imod(MpCanvas.Q, 2) != 1:
                                return
                            self.G_v()
                            MpCanvas.ce[MpCanvas.T] = 2
                    if _m97 or _sw96 not in (1, 4, 5):
                        _m97 = True
                        return
                    break
            if _m95 or _sw94 == 15:
                _m95 = True
                _sw98 = MpCanvas.V
                if _sw98 in (1, 4):
                    if MpCanvas.Q != 2:
                        return
                    self.G_v()
                    MpCanvas.ce[MpCanvas.T] = 4
                return
            if _m95 or _sw94 == 16:
                _m95 = True
                _sw99 = MpCanvas.V
                if _sw99 in (1, 4):
                    if MpCanvas.Q != 8:
                        return
                    self.G_v()
                    MpCanvas.ce[MpCanvas.T] = 3
                    if MpCanvas.U == (-1):
                        return
                    MpCanvas.cc[MpCanvas.U] = MpCanvas.W
                    MpCanvas.cd[MpCanvas.U] = 0
                    MpCanvas.ce[MpCanvas.U] = 3
                return
            if _m95 or _sw94 == 12:
                _m95 = True
                if MpCanvas.Q != 4:
                    return
                MpCanvas.X = 0
                self.t_I(6)
                if MpCanvas.cK[(4 + MpCanvas.bC)] == 2:
                    return
                return
            if _m95 or _sw94 == 13:
                _m95 = True
                if (MpCanvas.Q == 4) and (MpCanvas.cK[(4 + MpCanvas.bC)] == 13):
                    MpCanvas.cL = 0
                    while MpCanvas.cL < 4:
                        MpCanvas.cL = MpCanvas.cL + 1
                    self.t_I(5)
                    return
                if MpCanvas.Q == 7:
                    MpCanvas.cL = 0
                    while MpCanvas.cL < 4:
                        MpCanvas.cL = MpCanvas.cL + 1
                    self.t_I(5)
                    return
                if MpCanvas.Q != 5:
                    return
                MpCanvas.X = 0
            break

    def G_v(self):  # g.java:4501
        MpCanvas.cc[MpCanvas.T] = MpCanvas.V
        MpCanvas.cd[MpCanvas.T] = 0
        if (MpCanvas.cc[MpCanvas.S] == 16) or (MpCanvas.cc[MpCanvas.S] == 15):
            self.t_I(2)
            return
        self.t_I(0)

    def H_v(self):  # g.java:4511
        self.c_GIIIII(MpCanvas.e, MpCanvas.cW, MpCanvas.cX, 88, 72, 0)
        self.a_GIITI(MpCanvas.e, MpCanvas.cW, (MpCanvas.cX - 20), MpCanvas.bH, 0xFFFFFF)
        MpCanvas.bL = _js(_js(Consts.eX[26], " "), MpCanvas.aQ)
        self.a_GIITI(MpCanvas.e, MpCanvas.cW, (MpCanvas.cX - 4), MpCanvas.bL, 0xFFFFFF)
        self.a_GIITI(MpCanvas.e, MpCanvas.cW, (MpCanvas.cX + 12), Consts.eX[28], 0xFFFFFF)

    def I_v(self):  # g.java:4519
        if MpCanvas.X < 0:
            return
        MpCanvas.cL = 0
        while MpCanvas.cL < 4:
            if MpCanvas.bQ[MpCanvas.cL] and ((((MpCanvas.cL == MpCanvas.S) or (MpCanvas.cL == MpCanvas.T)) or (MpCanvas.cL == MpCanvas.U))):
                if MpCanvas.bW[MpCanvas.cL] != MpCanvas.cf[MpCanvas.cL]:
                    n2 = MpCanvas.cL
                    MpCanvas.bW[n2] = (MpCanvas.bW[n2] + MpCanvas.ch[MpCanvas.cL])
                    if MpCanvas.bW[MpCanvas.cL] < 0:
                        MpCanvas.bW[MpCanvas.cL] = 0
                if MpCanvas.bX[MpCanvas.cL] != MpCanvas.cg[MpCanvas.cL]:
                    n3 = MpCanvas.cL
                    MpCanvas.bX[n3] = (MpCanvas.bX[n3] + MpCanvas.ci[MpCanvas.cL])
                    if MpCanvas.bX[MpCanvas.cL] < 0:
                        MpCanvas.bX[MpCanvas.cL] = 0
                if MpCanvas.cj[MpCanvas.cL] != 0:
                    bl = _set(MpCanvas, 'bn', (imod(MpCanvas.bR[MpCanvas.cL], 2) != 0))
                    if not MpCanvas.bn:
                        self.e_GIII(MpCanvas.e, MpCanvas.ck[MpCanvas.cL], ((MpCanvas.cl[MpCanvas.cL] - 40) - (2 * MpCanvas.X)), MpCanvas.cj[MpCanvas.cL])
                    else:
                        self.e_GIII(MpCanvas.e, (MpCanvas.cQ - MpCanvas.ck[MpCanvas.cL]), ((MpCanvas.cl[MpCanvas.cL] - 40) - (2 * MpCanvas.X)), MpCanvas.cj[MpCanvas.cL])
            MpCanvas.cL = MpCanvas.cL + 1
        MpCanvas.g_G(MpCanvas.e)
        MpCanvas.cL = 0
        while MpCanvas.cL < 4:
            if (MpCanvas.bQ[MpCanvas.cL] and ((((MpCanvas.cL == MpCanvas.S) or (MpCanvas.cL == MpCanvas.T)) or (MpCanvas.cL == MpCanvas.U)))) and (MpCanvas.bW[MpCanvas.cL] == 0):
                MpCanvas.bW[MpCanvas.cL] = 1
            MpCanvas.cL = MpCanvas.cL + 1
        MpCanvas.X = MpCanvas.X + 1

    @staticmethod
    def g_G(graphics):  # g.java:4562
        MpCanvas.cL = 0
        while MpCanvas.cL < 4:
            if MpCanvas.bQ[MpCanvas.cL]:
                n2 = 0
                n3 = idiv((MpCanvas.bW[MpCanvas.cL] * MpCanvas.bK), MpCanvas.bV[MpCanvas.cL])
                if (n3 == 0) and (MpCanvas.bW[MpCanvas.cL] > 0):
                    n3 = 1
                n4 = (28 if (imod(MpCanvas.bR[MpCanvas.cL], 2) == 0) else ((MpCanvas.cQ - 28) - MpCanvas.bK))
                n5 = (0 if (idiv(MpCanvas.bR[MpCanvas.cL], 2) == 0) else ((MpCanvas.cR - 3) - 6))
                n3 = n3 - 1
                if MpCanvas.bW[MpCanvas.cL] > 0:
                    if imod(MpCanvas.bR[MpCanvas.cL], 2) == 0:
                        Draw.a_GIIII(graphics, n4, n5, n3, 0xB50000)
                        Draw.a_GIIII(graphics, n4, (n5 + 1), n3, 0xFF0000)
                        Draw.a_GIIII(graphics, n4, (n5 + 2), n3, 0xB50000)
                    else:
                        n2 = (MpCanvas.bK - n3)
                        Draw.a_GIIII(graphics, (n4 + n2), n5, n3, 0xB50000)
                        Draw.a_GIIII(graphics, (n4 + n2), (n5 + 1), n3, 0xFF0000)
                        Draw.a_GIIII(graphics, (n4 + n2), (n5 + 2), n3, 0xB50000)
                if (((n3 := idiv((MpCanvas.bX[MpCanvas.cL] * MpCanvas.bK), 100))) == 0) and (MpCanvas.bX[MpCanvas.cL] > 0):
                    n3 = 1
                n4 = (28 if (imod(MpCanvas.bR[MpCanvas.cL], 2) == 0) else ((MpCanvas.cQ - 28) - MpCanvas.bK))
                n5 = (6 if (idiv(MpCanvas.bR[MpCanvas.cL], 2) == 0) else (MpCanvas.cR - 3))
                n3 = n3 - 1
                if MpCanvas.bX[MpCanvas.cL] > 0:
                    if imod(MpCanvas.bR[MpCanvas.cL], 2) == 0:
                        Draw.a_GIIII(graphics, n4, n5, n3, 3223675)
                        Draw.a_GIIII(graphics, n4, (n5 + 1), n3, 9216734)
                        Draw.a_GIIII(graphics, n4, (n5 + 2), n3, 3223675)
                    else:
                        n2 = (MpCanvas.bK - n3)
                        Draw.a_GIIII(graphics, (n4 + n2), n5, n3, 3223675)
                        Draw.a_GIIII(graphics, (n4 + n2), (n5 + 1), n3, 9216734)
                        Draw.a_GIIII(graphics, (n4 + n2), (n5 + 2), n3, 3223675)
            MpCanvas.cL = MpCanvas.cL + 1

    @staticmethod
    def J_v():  # g.java:4609
        MpCanvas.cL = 0
        while MpCanvas.cL < 4:
            MpCanvas.bQ[MpCanvas.cL] = False
            MpCanvas.cL = MpCanvas.cL + 1
        MpCanvas.bb = 0
        MpCanvas.bc = 0

    def b_GIII(self, graphics, n2, n3, n4):  # g.java:4619
        MpCanvas.b_GIIII(graphics, n2, n3, n4, 1)

    def c_GIII(self, graphics, n2, n3, n4):  # g.java:4623
        MpCanvas.b_GIIII(graphics, n2, n3, n4, 2)

    def d_GIII(self, graphics, n2, n3, n4):  # g.java:4627
        MpCanvas.b_GIIII(graphics, n2, n3, n4, 3)

    def e_GIII(self, graphics, n2, n3, n4):  # g.java:4631
        MpCanvas.b_GIIII(graphics, n2, n3, n4, 4)

    def a_III(self, n2, n3, n4):  # g.java:4635
        MpCanvas.b_GIIII(MpCanvas.e, n2, n3, n4, 5)

    def f_GIII(self, graphics, n2, n3, n4):  # g.java:4639
        MpCanvas.b_GIIII(graphics, n2, n3, n4, 0)

    def b_III(self, n2, n3, n4):  # g.java:4643
        MpCanvas.b_GIIII(MpCanvas.e, n2, n3, n4, 0)

    def c_III(self, n2, n3, n4):  # g.java:4647
        MpCanvas.b_GIIII(MpCanvas.e, n2, n3, n4, 1)

    def d_III(self, n2, n3, n4):  # g.java:4651
        MpCanvas.b_GIIII(MpCanvas.e, n2, n3, n4, 0)

    def e_III(self, n2, n3, n4):  # g.java:4655
        MpCanvas.b_GIIII(MpCanvas.e, n2, n3, n4, 1)

    @staticmethod
    def b_GIIII(graphics, n2, n3, n4, n5):  # g.java:4659
        n6 = 1
        n7 = 0
        _sw100 = n5
        if _sw100 in (0, 1, 7):
            while (idiv(n4, n6) > 0) or (n6 == 1):
                n8 = idiv(imod(n4, ((n6 * 10))), n6)
                Draw.a_GMIIIIII(graphics, MpCanvas.dh[n5], n2, n3, 5, 8, (n8 * 5), 0)
                n2 = (n2 - 6)
                n6 = (n6 * 10)
                if (imod((n7 := i32(n7 + 1)), 3) != 0) or (idiv(n4, n6) <= 0):
                    continue
                Draw.a_GMIIIIII(graphics, MpCanvas.dh[n5], (n2 := (n2 + 2)), (n3 + 5), 2, 3, 50, 5)
                n2 = (n2 - 6)
            return
        elif _sw100 == 5:
            Draw.a_GMIIIIII(graphics, MpCanvas.dh[6], (n2 - 3), (n3 - 1), 3, 10, 7, 0)
            n2 = (n2 - 9)
            while (idiv(n4, n6) > 0) or (n6 == 1):
                n9 = idiv(imod(n4, ((n6 * 10))), n6)
                Draw.a_GMIIIIII(graphics, MpCanvas.dh[n5], n2, n3, 5, 8, (n9 * 5), 16)
                n2 = (n2 - 6)
                n6 = (n6 * 10)
                if (imod((n7 := i32(n7 + 1)), 3) != 0) or (idiv(n4, n6) <= 0):
                    continue
                Draw.b_GIIIII(graphics, (n2 := (n2 + 2)), (n3 + 6), 1, 3, 65280)
                n2 = (n2 - 6)
            Draw.a_GMIIIIII(graphics, MpCanvas.dh[6], (n2 - 2), (n3 - 1), 7, 10, 0, 0)
            return
        elif _sw100 == 2:
            while (idiv(n4, n6) > 0) or (n6 == 1):
                n10 = idiv(imod(n4, ((n6 * 10))), n6)
                Draw.a_GMIIIIII(graphics, MpCanvas.dh[n5], n2, n3, 7, 11, (n10 * 7), 0)
                n2 = (n2 - 8)
                n6 = (n6 * 10)
            return
        elif _sw100 == 3:
            while (idiv(n4, n6) > 0) or (n6 == 1):
                n11 = idiv(imod(n4, ((n6 * 10))), n6)
                Draw.a_GMIIIIII(graphics, MpCanvas.dh[n5], n2, n3, 12, 13, (n11 * 12), 0)
                n2 = (n2 - 12)
                n6 = (n6 * 10)
            return
        elif _sw100 == 4:
            if n4 < 0:
                n4 = (-n4)
                MpCanvas.br = True
            else:
                MpCanvas.br = False
            while (idiv(n4, n6) > 0) or (n6 == 1):
                n12 = idiv(imod(n4, ((n6 * 10))), n6)
                Draw.a_GMIIIIII(graphics, MpCanvas.dh[n5], n2, n3, 6, 10, (n12 * 6), (10 if MpCanvas.br else 0))
                n2 = (n2 - 7)
                n6 = (n6 * 10)

    @staticmethod
    def h_I(n2):  # g.java:4726
        MpCanvas.ck[n2] = 42
        MpCanvas.cl[n2] = (MpCanvas.cX + 65)
        if MpCanvas.bz != 0:
            n3 = n2
            MpCanvas.cl[n3] = (MpCanvas.cl[n3] + ((((-1) if (idiv(MpCanvas.bR[n2], 2) == 0) else 1)) * 23))

    @staticmethod
    def i_I(n2):  # g.java:4735
        MpCanvas.cY = n2
        MpCanvas.da = 0

    @staticmethod
    def K_v():  # g.java:4740
        byArray = [0] * (28)
        n2 = 0
        while n2 < len(byArray):
            byArray[n2] = 0
            n2 = n2 + 1
        byArray[0] = i8(MpCanvas.an)
        byArray[1] = i8(MpCanvas.am)
        byArray2 = bytearray(MpCanvas.i.encode('latin-1', 'replace'))
        n2 = 0
        while n2 < len(byArray2):
            byArray[(2 + n2)] = byArray2[n2]
            n2 = n2 + 1
        byArray2 = bytearray(MpCanvas.j.encode('latin-1', 'replace'))
        n2 = 0
        while n2 < len(byArray2):
            byArray[(14 + n2)] = byArray2[n2]
            n2 = n2 + 1
        try:
            recordStore = RecordStore.openRecordStore("pow_mp_save", True)
            if recordStore.getNumRecords() == 0:
                recordStore.addRecord(byArray, 0, len(byArray))
            recordStore.setRecord(1, byArray, 0, len(byArray))
            return
        except Exception:
            return

    def L_v(self):  # g.java:4774
        byArray = [0] * (28)
        MpCanvas.an = 0
        MpCanvas.am = 4
        MpCanvas.i = ""
        MpCanvas.j = ""
        try:
            recordStore = RecordStore.openRecordStore("pow_mp_save", False)
            if (recordStore is None) or (recordStore.getNumRecords() < 1):
                return False
            byArray = recordStore.getRecord(1)
        except Exception:
            pass
        if len(byArray) >= 28:
            MpCanvas.an = byArray[0]
            MpCanvas.am = byArray[1]
            MpCanvas.i = MpCanvas.c_T(MpCanvas.a_ABII(byArray, 2, 14))
            MpCanvas.j = MpCanvas.c_T(MpCanvas.a_ABII(byArray, 14, 28))
            return True
        return False

    @staticmethod
    def a_ABII(byArray, n2, n3):  # g.java:4798
        n4 = n2
        n5 = n3
        string = None
        try:
            n6 = (n5 - n4)
            byArray2 = [0] * ((n6 + 2))
            byArray3 = byArray2
            byArray2[0] = i8((((n6 >> 8) & 0xFF)))
            byArray3[1] = i8(((n6 & 0xFF)))
            _arraycopy(byArray, n4, byArray3, 2, n6)
            byteArrayInputStream = ByteArrayInputStream(byArray3, 0, len(byArray3))
            dataInputStream = DataInputStream(byteArrayInputStream)
            string = dataInputStream.readUTF()
            byteArrayInputStream.close()
            dataInputStream.close()
        except Exception:
            pass
        return string

    @staticmethod
    def c_T(string):  # g.java:4819
        n2 = 0
        n3 = len(string)
        n2 = 0
        while n2 < n3:
            if ord(string[n2]) < 32:
                break
            n2 = n2 + 1
        if n2 == 0:
            return ""
        return string[0:n2]

    def M_v(self):  # g.java:4833
        n2 = 0
        _sw101 = MpCanvas.z
        _m102 = False
        while True:
            if _m102 or _sw101 == 0:
                _m102 = True
                if MpCanvas.x:
                    self.v_G(MpCanvas.e)
                    return
                n2 = (MpCanvas.cX - 57)
                n3 = 0
                while n3 < 7:
                    self.a_GIITI(MpCanvas.e, MpCanvas.cW, (n2 + (12 * n3)), Consts.eV[(1 + n3)], 0xFFFFFF)
                    n3 = n3 + 1
                Draw.b_GIIIII(MpCanvas.e, (MpCanvas.cW - 40), (n2 + 86), 80, 13, 0)
                Draw.a_GIIIII(MpCanvas.e, (MpCanvas.cW - 40), (n2 + 86), 80, 13, 0x646464)
                self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((n2 + 52) + 35), MpCanvas.bG, 0x41FF41)
                MpCanvas.a_II(MpCanvas.C, ((n2 + 64) + 35))
                if imod(MpCanvas.da, 4) < 2:
                    n4 = MpCanvas.n.a_T(MpCanvas.bG)
                    if len(MpCanvas.bG) == 12:
                        n4 = (n4 - (MpCanvas.n.a_T("A") * 2))
                    MpCanvas.b_GIIIII(MpCanvas.e, (MpCanvas.cW + idiv(n4, 2)), ((n2 + 62) + 35), ((MpCanvas.cW + idiv(n4, 2)) + 4), ((n2 + 62) + 35), 0xFFFFFF)
                if len(MpCanvas.bG) == 0:
                    self.c_II(4, 2)
                    break
                self.c_II(4, 3)
                return
            if _m102 or _sw101 == 1:
                _m102 = True
                n2 = (MpCanvas.cX - 45)
                n5 = 0
                while n5 < 5:
                    self.a_GIITI(MpCanvas.e, MpCanvas.cW, (n2 + (12 * n5)), Consts.eV[(8 + n5)], 0xFFFFFF)
                    n5 = n5 + 1
                Draw.b_GIIIII(MpCanvas.e, (MpCanvas.cW - 40), (n2 + 63), 80, 13, 0)
                Draw.a_GIIIII(MpCanvas.e, (MpCanvas.cW - 40), (n2 + 63), 80, 13, 0x646464)
                self.a_GIITI(MpCanvas.e, MpCanvas.cW, (n2 + 64), MpCanvas.j, 0x41FF41)
                if len(MpCanvas.j) >= 4:
                    self.c_II(0, 3)
                    return
                if len(MpCanvas.j) > 0:
                    self.c_II((-1), 3)
                    return
                self.c_II((-1), 1)
            break

    def j_I(self, n2):  # g.java:4888
        _sw103 = MpCanvas.z
        _m104 = False
        while True:
            if _m104 or _sw103 == 0:
                _m104 = True
                if MpCanvas.x:
                    if (MpCanvas.cs == (-3)) or (MpCanvas.cs == (-4)):
                        MpCanvas.y = imod(((MpCanvas.y + 1)), 2)
                        return
                    if MpCanvas.cs != (-5):
                        break
                    if MpCanvas.y == 0:
                        MpCanvas.i_I(300)
                        return
                    MpCanvas.x = False
                    return
                len(MpCanvas.i)
                bl = False
                if n2 == (-7):
                    if len(MpCanvas.bG) == 0:
                        MpCanvas.x = True
                        return
                    MpCanvas.bG = MpCanvas.bG[0:(len(MpCanvas.bG) - 1)]
                    return
                if (MpCanvas.cs == (-5)) or (MpCanvas.cs == (-6)):
                    if len(MpCanvas.bG) > 12:
                        break
                    if MpCanvas.C < 26:
                        if len(MpCanvas.bG) >= 12:
                            break
                        MpCanvas.bG = _js(MpCanvas.bG, chr(((((65 + MpCanvas.C))) & 0xFFFF)))
                        return
                    if (MpCanvas.C != 26) or (len(MpCanvas.bG) < 4):
                        break
                    MpCanvas.i = MpCanvas.bG
                    MpCanvas.z = 1
                    MpCanvas.j = ""
                    return
                MpCanvas.p_I(MpCanvas.cs)
                return
            if _m104 or _sw103 == 1:
                _m104 = True
                n3 = len(MpCanvas.j)
                n4 = (-1)
                _sw105 = n2
                if _sw105 == 48:
                    n4 = 0
                elif _sw105 == 49:
                    n4 = 1
                elif _sw105 == 50:
                    n4 = 2
                elif _sw105 == 51:
                    n4 = 3
                elif _sw105 == 52:
                    n4 = 4
                elif _sw105 == 53:
                    n4 = 5
                elif _sw105 == 54:
                    n4 = 6
                elif _sw105 == 55:
                    n4 = 7
                elif _sw105 == 56:
                    n4 = 8
                elif _sw105 == 57:
                    n4 = 9
                if n2 == (-7):
                    if n3 > 0:
                        MpCanvas.j = MpCanvas.j[0:(n3 - 1)]
                        return
                    MpCanvas.z = 0
                    MpCanvas.C = 0
                    return
                if n4 != (-1):
                    if n3 >= 12:
                        break
                    MpCanvas.j = _js(_js(MpCanvas.j, ""), n4)
                    return
                if (n2 != (-6)) or (n3 < 4):
                    break
                MpCanvas.cv = 0
                MpCanvas.A = True
                MpCanvas.i_I(10000)
            break

    def k_I(self, n2):  # g.java:4996
        if n2 != MpCanvas.dV[MpCanvas.dW]:
            MpCanvas.dU[_inc(MpCanvas, 'dW', 1)] = 0
            MpCanvas.dV[MpCanvas.dW] = n2
        MpCanvas.i_I(n2)

    def l_I(self, n2):  # g.java:5004
        if n2 == 10:
            MpCanvas.dX = True
        MpCanvas.dW = 0
        MpCanvas.dU[0] = 0
        MpCanvas.dV[0] = n2
        MpCanvas.i_I(n2)

    def N_v(self):  # g.java:5014
        if MpCanvas.dW > 0:
            MpCanvas.i_I(MpCanvas.dV[_inc(MpCanvas, 'dW', -1)])

    def m_I(self, n2):  # g.java:5020
        if MpCanvas.dW >= n2:
            MpCanvas.i_I(MpCanvas.dV[_set(MpCanvas, 'dW', (MpCanvas.dW - n2))])

    def O_v(self):  # g.java:5026
        MpCanvas.dm = None
        MpCanvas.dk = None
        MpCanvas.dn = None
        MpCanvas.dl = None
        MpCanvas.do_ = None
        n2 = 0
        while n2 < 6:
            MpCanvas.dd[n2] = None
            n2 = n2 + 1
        MpCanvas.di[1] = None
        MpCanvas.X_v()
        self.g_v()
        MpCanvas.J_v()
        MpCanvas.bR[0] = MpCanvas.bh
        MpCanvas.bM[0] = MpCanvas.cE
        MpCanvas.bS[0] = MpCanvas.as_
        MpCanvas.bT[0] = MpCanvas.at
        MpCanvas.bU[0] = MpCanvas.au
        MpCanvas.bW[0] = MpCanvas.av
        MpCanvas.bV[0] = MpCanvas.bW[0]
        MpCanvas.bX[0] = 0
        MpCanvas.bY[0] = MpCanvas.aw
        MpCanvas.bZ[0] = MpCanvas.ar
        MpCanvas.bN[0] = MpCanvas.cF
        MpCanvas.bO[0] = MpCanvas.cG
        MpCanvas.cr[0] = MpCanvas.aK
        MpCanvas.bQ[0] = True
        MpCanvas.bb = MpCanvas.bb + 1
        MpCanvas.h_I(0)
        MpCanvas.co[0] = imod(abs(MpCanvas.h.nextInt()), 4)
        MpCanvas.cp[0] = 99
        MpCanvas.cq[0] = 0
        MpCanvas.bj = False
        MpCanvas.aR = 0
        MpCanvas.D = False
        self.k_I(90)
        self.ag_v()
        MpCanvas.O = True

    def h_G(self, graphics):  # g.java:5068
        self.c_GIIIII(graphics, MpCanvas.cW, (MpCanvas.cX - 26), 110, 60, 0)
        Draw.b_GIIIII(graphics, (MpCanvas.cW - 51), ((MpCanvas.cX - 51) + (MpCanvas.db * 12)), 102, 12, 12956683)
        MpCanvas.cL = 0
        while MpCanvas.cL < MpCanvas.bD:
            if MpCanvas.bX[0] < MpCanvas.cI[(MpCanvas.bE[MpCanvas.cL] - 3)]:
                self.a_GIITI(graphics, MpCanvas.cW, ((MpCanvas.cX - 51) + (MpCanvas.cL * 12)), Consts.eK[(MpCanvas.bE[MpCanvas.cL] - 3)], 0x646464)
                if (MpCanvas.bE[MpCanvas.cL] != 9) and (MpCanvas.bE[MpCanvas.cL] == 10):
                    pass
            else:
                self.a_GIITI(graphics, MpCanvas.cW, ((MpCanvas.cX - 51) + (MpCanvas.cL * 12)), Consts.eK[(MpCanvas.bE[MpCanvas.cL] - 3)], 0xFFFFFF)
            MpCanvas.cL = MpCanvas.cL + 1

    def P_v(self):  # g.java:5085
        _sw106 = MpCanvas.bz
        if _sw106 in (0, 1):
            n2 = (MpCanvas.cX - 62)
            self.c_GIIIII(MpCanvas.e, MpCanvas.cW, MpCanvas.cX, 102, 124, 0)
            self.a_GIITI(MpCanvas.e, MpCanvas.cW, (n2 + 5), MpCanvas.bM[0], 0xFFFFFF)
            string = (Consts.eX[5] if (MpCanvas.aU == 1) else Consts.eX[6])
            self.a_GTIIII(MpCanvas.e, string, MpCanvas.cW, (n2 + 19), 1, 16400640)
            self.a_GTIIII(MpCanvas.e, Consts.eX[49], (MpCanvas.cW - 42), (n2 + 35), 0, 0xFFFFFF)
            self.f_GIII(MpCanvas.e, (MpCanvas.cW + 36), (n2 + 36), MpCanvas.at)
            self.a_GTIIII(MpCanvas.e, Consts.eX[50], (MpCanvas.cW - 42), (n2 + 50), 0, 0xFFFFFF)
            self.f_GIII(MpCanvas.e, (MpCanvas.cW + 36), (n2 + 51), MpCanvas.au)
            self.a_GTIIII(MpCanvas.e, Consts.eX[29], (MpCanvas.cW - 42), (n2 + 70), 0, 0xFFFFFF)
            self.b_GIII(MpCanvas.e, (MpCanvas.cW + 36), (n2 + 71), MpCanvas.aV)
            self.a_GTIIII(MpCanvas.e, Consts.eR[0], (MpCanvas.cW - 42), (n2 + 83), 0, 0xFFFFFF)
            self.b_GIII(MpCanvas.e, (MpCanvas.cW + 36), (n2 + 84), MpCanvas.aX)
            self.a_GTIIII(MpCanvas.e, Consts.eX[4], (MpCanvas.cW - 42), (n2 + 96), 0, 0x41FF41)
            self.f_GIII(MpCanvas.e, (MpCanvas.cW + 36), (n2 + 97), MpCanvas.aZ)
            self.r_I((n2 + 109))
            return
        elif _sw106 == 2:
            n3 = (MpCanvas.cX - 62)
            self.c_GIIIII(MpCanvas.e, MpCanvas.cW, MpCanvas.cX, 102, 124, 0)
            self.a_GIITI(MpCanvas.e, MpCanvas.cW, (n3 + 3), MpCanvas.bM[0], 0xFFFFFF)
            if MpCanvas.aU == 1:
                self.a_GIITI(MpCanvas.e, MpCanvas.cW, (n3 + 15), Consts.eL[MpCanvas.aW], 16400640)
            else:
                self.a_GIITI(MpCanvas.e, MpCanvas.cW, (n3 + 15), Consts.eX[31], 16400640)
            self.a_GTIIII(MpCanvas.e, Consts.eX[29], (MpCanvas.cW - 34), (n3 + 30), 0, 0xFFFFFF)
            self.b_GIII(MpCanvas.e, (MpCanvas.cW + 30), (n3 + 31), MpCanvas.aV)
            self.a_GTIIII(MpCanvas.e, Consts.eX[32], (MpCanvas.cW - 34), (n3 + 42), 0, 0xFFFFFF)
            self.b_GIII(MpCanvas.e, (MpCanvas.cW + 30), (n3 + 43), MpCanvas.aY)
            self.a_GTIIII(MpCanvas.e, Consts.eR[0], (MpCanvas.cW - 34), (n3 + 54), 0, 0xFFFFFF)
            self.b_GIII(MpCanvas.e, (MpCanvas.cW + 30), (n3 + 55), MpCanvas.aX)
            if not (MpCanvas.bI == "NONE"):
                self.a_GIITI(MpCanvas.e, MpCanvas.cW, (n3 + 69), MpCanvas.bI, 0xFFFFFF)
                self.a_GIITI(MpCanvas.e, MpCanvas.cW, (n3 + 81), _js(Consts.eX[33], "!!!"), 0xFFFFFF)
            self.a_GTIIII(MpCanvas.e, Consts.eX[4], (MpCanvas.cW - 34), (n3 + 96), 0, 0x41FF41)
            self.b_GIII(MpCanvas.e, (MpCanvas.cW + 30), (n3 + 97), MpCanvas.aZ)
            self.r_I((n3 + 109))

    @staticmethod
    def Q_v():  # g.java:5133
        MpCanvas.cL = 0
        while MpCanvas.cL < 4:
            if MpCanvas.bQ[MpCanvas.cL]:
                _sw107 = MpCanvas.cp[MpCanvas.cL]
                _m108 = False
                while True:
                    if _m108 or _sw107 in (11, 12, 13):
                        _m108 = True
                        n2 = MpCanvas.cL
                        MpCanvas.cq[n2] = (MpCanvas.cq[n2] - 1)
                        if MpCanvas.cq[MpCanvas.cL] > 0:
                            break
                        MpCanvas.cp[MpCanvas.cL] = 99
                    break
            MpCanvas.cL = MpCanvas.cL + 1

    def R_v(self):  # g.java:5152
        MpCanvas.cO = 0
        if MpCanvas.da == 0:
            MpCanvas.cO = (-40)
        elif MpCanvas.da == 1:
            MpCanvas.cO = (-20)
        MpCanvas.cL = 0
        while MpCanvas.cL < 4:
            if (MpCanvas.bQ[MpCanvas.cL] and (MpCanvas.bW[MpCanvas.cL] > 0)) and (((((MpCanvas.cY == 99) or (MpCanvas.cL == MpCanvas.S)) or (MpCanvas.cL == MpCanvas.T)) or (MpCanvas.cL == MpCanvas.U))):
                MpCanvas.cP = (27 if (MpCanvas.bz == 0) else ((27 if (idiv(MpCanvas.bR[MpCanvas.cL], 2) == 0) else ((MpCanvas.cR - 27) - 23))))
                _sw109 = MpCanvas.ca[MpCanvas.cL]
                if _sw109 == 0:
                    MpCanvas.cD = MpCanvas.bZ[MpCanvas.cL]
                    MpCanvas.bx = True
                elif _sw109 == 1:
                    MpCanvas.cD = 4
                    MpCanvas.bx = False
                elif _sw109 == 2:
                    MpCanvas.cD = 5
                    MpCanvas.bx = False
                if MpCanvas.cY == 99:
                    MpCanvas.bJ = MpCanvas.cb[MpCanvas.cL]
                elif MpCanvas.cL == MpCanvas.S:
                    MpCanvas.bJ = MpCanvas.cK[(4 + MpCanvas.bC)]
                elif MpCanvas.cL == MpCanvas.T:
                    MpCanvas.bJ = MpCanvas.cK[(16 + MpCanvas.bC)]
                elif MpCanvas.cL == MpCanvas.U:
                    MpCanvas.bJ = MpCanvas.cK[(36 + MpCanvas.bC)]
                if imod(MpCanvas.bR[MpCanvas.cL], 2) == 0:
                    Draw.a_GIIIII(MpCanvas.e, MpCanvas.cO, MpCanvas.cP, 60, 23, 0)
                    Draw.a_GIIIII(MpCanvas.e, (MpCanvas.cO + 1), (MpCanvas.cP + 1), 58, 21, 16769990)
                    _sw110 = MpCanvas.bJ
                    if _sw110 in (0, 3, 4, 5, 6, 7, 8):
                        self.a_AMTI(MpCanvas.dg, "act", 0)
                        self.a_AMTI(MpCanvas.dg, "act", (6 + MpCanvas.cD))
                        MpCanvas.c_IIM((MpCanvas.cO + Consts.es[0]), (MpCanvas.cP + Consts.et[0]), MpCanvas.dg[0])
                        MpCanvas.c_IIM((MpCanvas.cO + Consts.es[(6 + MpCanvas.cD)]), (MpCanvas.cP + Consts.et[(6 + MpCanvas.cD)]), MpCanvas.dg[(6 + MpCanvas.cD)])
                    else:
                        self.a_AMTI(MpCanvas.dg, "act", 1)
                        self.a_AMTI(MpCanvas.dg, "act", (12 + MpCanvas.cD))
                        MpCanvas.c_IIM((MpCanvas.cO + Consts.es[1]), (MpCanvas.cP + Consts.et[1]), MpCanvas.dg[1])
                        MpCanvas.c_IIM((MpCanvas.cO + Consts.es[(12 + MpCanvas.cD)]), (MpCanvas.cP + Consts.et[(12 + MpCanvas.cD)]), MpCanvas.dg[(12 + MpCanvas.cD)])
                    MpCanvas.bJ = (3 if (MpCanvas.bJ > 2) else MpCanvas.bJ)
                    self.a_AMTI(MpCanvas.dg, "act", (2 + MpCanvas.bJ))
                    MpCanvas.a_IIM((((MpCanvas.cO + 60) - 19) + Consts.es[(2 + MpCanvas.bJ)]), ((0 + MpCanvas.cP) + Consts.et[(2 + MpCanvas.bJ)]), MpCanvas.dg[(2 + MpCanvas.bJ)])
                else:
                    MpCanvas.a_IIIII(((MpCanvas.cQ - MpCanvas.cO) - 60), MpCanvas.cP, 60, 23, 0)
                    MpCanvas.a_IIIII((((MpCanvas.cQ - MpCanvas.cO) - 60) + 1), (MpCanvas.cP + 1), 58, 21, 16769990)
                    _sw111 = MpCanvas.bJ
                    if _sw111 in (0, 3, 4, 5, 6, 7, 8):
                        self.a_AMTI(MpCanvas.dg, "act", (6 + MpCanvas.cD))
                        MpCanvas.b_IIM((MpCanvas.cQ - ((MpCanvas.cO + Consts.es[0]))), (MpCanvas.cP + Consts.et[0]), MpCanvas.dg[0])
                        MpCanvas.a_IIMZ((MpCanvas.cQ - ((MpCanvas.cO + Consts.es[(6 + MpCanvas.cD)]))), (MpCanvas.cP + Consts.et[(6 + MpCanvas.cD)]), MpCanvas.dg[(6 + MpCanvas.cD)], MpCanvas.bx)
                    else:
                        self.a_AMTI(MpCanvas.dg, "act", (12 + MpCanvas.cD))
                        MpCanvas.b_IIM((MpCanvas.cQ - ((MpCanvas.cO + Consts.es[1]))), (MpCanvas.cP + Consts.et[1]), MpCanvas.dg[1])
                        MpCanvas.a_IIMZ((MpCanvas.cQ - ((MpCanvas.cO + Consts.es[(12 + MpCanvas.cD)]))), (MpCanvas.cP + Consts.et[(12 + MpCanvas.cD)]), MpCanvas.dg[(12 + MpCanvas.cD)], MpCanvas.bx)
                    MpCanvas.bJ = (3 if (MpCanvas.bJ > 2) else MpCanvas.bJ)
                    self.a_AMTI(MpCanvas.dg, "act", (2 + MpCanvas.bJ))
                    MpCanvas.a_IIM(((((MpCanvas.cQ - MpCanvas.cO) - 60) + 10) + Consts.es[(2 + MpCanvas.bJ)]), ((0 + MpCanvas.cP) + Consts.et[(2 + MpCanvas.bJ)]), MpCanvas.dg[(2 + MpCanvas.bJ)])
            MpCanvas.cL = MpCanvas.cL + 1

    def i_G(self, graphics):  # g.java:5246
        if MpCanvas.aR < 10:
            Draw.a_GMIIIIII(graphics, MpCanvas.dh[3], (MpCanvas.cW - 33), (MpCanvas.cX - 31), 52, 13, 120, 0)
            self.d_GIII(graphics, (MpCanvas.cW + 21), (MpCanvas.cX - 31), MpCanvas.aR)
            return
        Draw.a_GMIIIIII(graphics, MpCanvas.dh[3], (MpCanvas.cW - 39), (MpCanvas.cX - 31), 52, 13, 120, 0)
        self.d_GIII(graphics, (MpCanvas.cW + 27), (MpCanvas.cX - 31), MpCanvas.aR)

    @staticmethod
    def j_G(graphics):  # g.java:5256
        MpCanvas.cO = MpCanvas.cW
        MpCanvas.cP = (MpCanvas.cX - 40)
        if MpCanvas.bz == 0:
            MpCanvas.cP = (MpCanvas.cP - 6)
        Draw.a_GMIII(graphics, MpCanvas.df[17], (MpCanvas.cO - 12), MpCanvas.cP, 0)
        Draw.a_GMIII(graphics, MpCanvas.df[16], ((MpCanvas.cO - 36) - 1), (MpCanvas.cP + 16), 0)
        Draw.a_GMIII(graphics, MpCanvas.df[15], ((MpCanvas.cO + 12) + 1), (MpCanvas.cP + 16), 0)
        MpCanvas.bs = False
        if MpCanvas.bD > 0:
            MpCanvas.cN = 0
            while MpCanvas.cN < MpCanvas.bD:
                if MpCanvas.bX[0] >= MpCanvas.cI[(MpCanvas.bE[MpCanvas.cN] - 3)]:
                    MpCanvas.bs = True
                MpCanvas.cN = MpCanvas.cN + 1
        Draw.a_GMIII(graphics, MpCanvas.df[(18 + ((0 if MpCanvas.bs else 1)))], (MpCanvas.cO - 12), (MpCanvas.cP + 30), 0)
        if MpCanvas.bB != 99:
            n2 = 0
            n3 = 0
            if MpCanvas.bB == 0:
                n3 = ((MpCanvas.cO + 12) + 1)
                n2 = (MpCanvas.cP + 16)
            elif MpCanvas.bB == 1:
                n3 = ((MpCanvas.cO - 36) - 1)
                n2 = (MpCanvas.cP + 16)
            elif MpCanvas.bB == 2:
                n3 = (MpCanvas.cO - 12)
                n2 = MpCanvas.cP
            else:
                n3 = (MpCanvas.cO - 12)
                n2 = (MpCanvas.cP + 30)
            Draw.a_GIIIII(graphics, (n3 - 1), (n2 - 1), 24, 24, 15721306)
            Draw.a_GIIIII(graphics, n3, n2, 23, 23, 15721306)

    def d_GI(self, graphics, n2):  # g.java:5297
        n3 = 0
        if MpCanvas.bz == 0:
            n3 = 25
        _sw112 = n2
        if _sw112 == 0:
            if MpCanvas.ba > 5:
                self.c_GIIIII(graphics, MpCanvas.cW, ((MpCanvas.cX + 28) + n3), 120, 27, 0)
                self.a_IITI(MpCanvas.cW, ((MpCanvas.cX + 17) + n3), Consts.eX[0], 0xFFFFFF)
                self.a_IITI(MpCanvas.cW, ((MpCanvas.cX + 28) + n3), Consts.eX[1], (0x646464 if MpCanvas.G else 0xFFFFFF))
                return
            self.c_GIIIII(graphics, MpCanvas.cW, ((MpCanvas.cX + 28) + n3), 26, 26, 0)
            self.c_GIII(graphics, (MpCanvas.cW - 4), ((MpCanvas.cX + 22) + n3), MpCanvas.ba)
            return
        elif _sw112 == 1:
            self.c_GIIIII(graphics, MpCanvas.cW, ((MpCanvas.cX + 28) + n3), 120, 27, 0)
            self.a_IITI(MpCanvas.cW, ((MpCanvas.cX + 23) + n3), Consts.eX[17], 0xFFFFFF)
            return
        elif _sw112 == 2:
            string = ""
            if imod(MpCanvas.da, 4) == 1:
                string = "."
            elif imod(MpCanvas.da, 4) == 2:
                string = ".."
            elif imod(MpCanvas.da, 4) == 3:
                string = "..."
            self.c_GIIIII(graphics, MpCanvas.cW, ((MpCanvas.cX + 28) + n3), 80, 24, 0)
            self.b_IITI((MpCanvas.cW - 30), ((MpCanvas.cX + 23) + n3), _js(Consts.eX[7], string), 0xFFFFFF)

    def S_v(self):  # g.java:5334
        if MpCanvas.u:
            if idiv(((MpCanvas.v - system.currentTimeMillis())), 1000) >= 80:
                MpCanvas.u = False
                MpCanvas.cw = 13
                MpCanvas.x = False
                MpCanvas.n_v()
                MpCanvas.b_I((-1))
                self.k_I(4)
                return
        else:
            MpCanvas.u = True
            MpCanvas.v = system.currentTimeMillis()

    def T_v(self):  # g.java:5351
        n2 = (MpCanvas.cX - 57)
        self.k_G(MpCanvas.e)
        MpCanvas.b_IIIII(((MpCanvas.cW - 52) - 7), (n2 - 2), 118, 123, 0)
        MpCanvas.a_IIIII(((MpCanvas.cW - 52) - 7), (n2 - 2), 118, 123, 0x949694)
        MpCanvas.b_IIIII(((MpCanvas.cW - 52) - 6), (n2 - 1), 116, 13, 0x313431)
        MpCanvas.bv = 0
        MpCanvas.cL = 0
        while MpCanvas.cL < MpCanvas.be:
            _sw113 = MpCanvas.dU[(MpCanvas.dW - 1)]
            if _sw113 == 0:
                MpCanvas.bv = (MpCanvas.bv + Consts.ey[MpCanvas.cL])
            elif _sw113 == 1:
                MpCanvas.bv = (MpCanvas.bv + Consts.eA[MpCanvas.cL])
            elif _sw113 == 2:
                MpCanvas.bv = (MpCanvas.bv + Consts.eC[MpCanvas.cL])
            elif _sw113 == 3:
                MpCanvas.bv = (MpCanvas.bv + Consts.eE[MpCanvas.cL])
            elif _sw113 == 4:
                MpCanvas.bv = (MpCanvas.bv + Consts.eG[MpCanvas.cL])
            elif _sw113 == 5:
                MpCanvas.bv = (MpCanvas.bv + Consts.eI[MpCanvas.cL])
            MpCanvas.cL = MpCanvas.cL + 1
        _sw114 = MpCanvas.dU[(MpCanvas.dW - 1)]
        if _sw114 == 0:
            self.a_IITI(MpCanvas.cW, n2, Consts.ex[MpCanvas.bv], 0xFFFFFF)
            MpCanvas.bJ = Consts.ey[MpCanvas.be]
        elif _sw114 == 1:
            self.a_IITI(MpCanvas.cW, n2, Consts.ez[MpCanvas.bv], 0xFFFFFF)
            MpCanvas.bJ = Consts.eA[MpCanvas.be]
        elif _sw114 == 2:
            self.a_IITI(MpCanvas.cW, n2, Consts.eB[MpCanvas.bv], 0xFFFFFF)
            MpCanvas.bJ = Consts.eC[MpCanvas.be]
        elif _sw114 == 3:
            self.a_IITI(MpCanvas.cW, n2, Consts.eD[MpCanvas.bv], 0xFFFFFF)
            MpCanvas.bJ = Consts.eE[MpCanvas.be]
        elif _sw114 == 4:
            self.a_IITI(MpCanvas.cW, n2, Consts.eF[MpCanvas.bv], 0xFFFFFF)
            MpCanvas.bJ = Consts.eG[MpCanvas.be]
        elif _sw114 == 5:
            self.a_IITI(MpCanvas.cW, n2, Consts.eH[MpCanvas.bv], 0xFFFFFF)
            MpCanvas.bJ = Consts.eI[MpCanvas.be]
        MpCanvas.cL = 1
        while MpCanvas.cL < MpCanvas.bJ:
            _sw115 = MpCanvas.dU[(MpCanvas.dW - 1)]
            _m116 = False
            while True:
                if _m116 or _sw115 == 0:
                    _m116 = True
                    self.b_IITI((MpCanvas.cW - 56), ((n2 + (MpCanvas.cL * 12)) + 1), Consts.ex[(MpCanvas.bv + MpCanvas.cL)], 0xFFFFFF)
                    break
                if _m116 or _sw115 == 1:
                    _m116 = True
                    self.b_IITI((MpCanvas.cW - 56), ((n2 + (MpCanvas.cL * 12)) + 1), Consts.ez[(MpCanvas.bv + MpCanvas.cL)], 0xFFFFFF)
                    break
                if _m116 or _sw115 == 2:
                    _m116 = True
                    self.b_IITI((MpCanvas.cW - 56), ((n2 + (MpCanvas.cL * 12)) + 1), Consts.eB[(MpCanvas.bv + MpCanvas.cL)], 0xFFFFFF)
                    break
                if _m116 or _sw115 == 3:
                    _m116 = True
                    self.b_IITI((MpCanvas.cW - 56), ((n2 + (MpCanvas.cL * 12)) + 1), Consts.eD[(MpCanvas.bv + MpCanvas.cL)], 0xFFFFFF)
                    break
                if _m116 or _sw115 == 4:
                    _m116 = True
                    self.a_IITI(MpCanvas.cW, ((n2 + (MpCanvas.cL * 17)) + 9), Consts.eF[(MpCanvas.bv + MpCanvas.cL)], 0xFFFFFF)
                    if MpCanvas.cL != 3:
                        break
                    self.a_IITI(MpCanvas.cW, ((n2 + (MpCanvas.cL * 17)) + 9), _js("v", MpCanvas.a), 0xFFFFFF)
                    break
                if _m116 or _sw115 == 5:
                    _m116 = True
                    self.b_IITI((MpCanvas.cW - 56), ((n2 + (MpCanvas.cL * 12)) + 1), Consts.eH[(MpCanvas.bv + MpCanvas.cL)], 0xFFFFFF)
                break
            MpCanvas.cL = MpCanvas.cL + 1
        if Consts.ew[MpCanvas.dU[(MpCanvas.dW - 1)]] > 1:
            self.a_IITI(MpCanvas.cW, ((n2 + 72) + 38), _js(_js((MpCanvas.be + 1), "/"), Consts.ew[MpCanvas.dU[(MpCanvas.dW - 1)]]), 0xFFFFFF)
            MpCanvas.c_IIM((MpCanvas.cW - 35), ((n2 + 72) + 39), MpCanvas.di[1])
            MpCanvas.b_IIM((MpCanvas.cW + 35), ((n2 + 72) + 39), MpCanvas.di[1])

    def U_v(self):  # g.java:5456
        self.l_G(MpCanvas.g)
        n2 = idiv(80, MpCanvas.k)
        if n2 > 30:
            n2 = 30
        elif n2 < 19:
            n2 = 19
        n3 = 0
        if ((MpCanvas.cY == 162) or (MpCanvas.cY == 163)) or (MpCanvas.cY == 164):
            n3 = 15
        elif MpCanvas.cY == 10:
            n3 = 40
        MpCanvas.cL = 0
        while MpCanvas.cL < MpCanvas.k:
            Draw.a_GMIIIIII(MpCanvas.g, MpCanvas.do_, (idiv((((MpCanvas.cQ - (n2 * ((MpCanvas.k - 1)))) - 11)), 2) + (n2 * MpCanvas.cL)), ((MpCanvas.cX + 6) + n3), 12, 15, 12, 0)
            MpCanvas.cL = MpCanvas.cL + 1

    def V_v(self):  # g.java:5477
        if MpCanvas.bn:
            self.b_AMTI(MpCanvas.dC[1], "spreff2_r", 1)
        else:
            self.b_AMTI(MpCanvas.dC[1], "spreff2", 0)
        if MpCanvas.dE[0] is None:
            MpCanvas.dE[0] = SpriteFrames("/spreff3.SP2")

    @staticmethod
    def e_GI(graphics, n2):  # g.java:5488
        n3 = ((n2 * 2) + imod(MpCanvas.da, 2))
        if MpCanvas.bn:
            Draw.a_GMIIIIII(graphics, MpCanvas.dC[1][1], (MpCanvas.cQ - (((MpCanvas.cU - MpCanvas.dE[0].g[n3]) + MpCanvas.dE[0].e[n3]))), (MpCanvas.cV - MpCanvas.dE[0].h[n3]), MpCanvas.dE[0].e[n3], MpCanvas.dE[0].f[n3], MpCanvas.dE[0].c[n3], MpCanvas.dE[0].d[n3])
            return
        Draw.a_GMIIIIII(graphics, MpCanvas.dC[1][0], (MpCanvas.cU - MpCanvas.dE[0].g[n3]), (MpCanvas.cV - MpCanvas.dE[0].h[n3]), MpCanvas.dE[0].e[n3], MpCanvas.dE[0].f[n3], MpCanvas.dE[0].c[n3], MpCanvas.dE[0].d[n3])

    def a_AMTI(self, imageArray, string, n2):  # g.java:5497
        if imageArray[n2] is None:
            imageArray[n2] = self.b_T(_js(_js(_js("/", string), n2), ".png"))

    def b_AMTI(self, imageArray, string, n2):  # g.java:5503
        if imageArray[n2] is None:
            imageArray[n2] = self.b_T(_js(_js("/", string), ".png"))

    def a_AMALaT(self, imageArray, aArray, string):  # g.java:5509
        self.a_AMALaTI(imageArray, aArray, string, 1)

    def a_AMALaTI(self, imageArray, aArray, string, n2):  # g.java:5513
        if MpCanvas.bn:
            if imageArray[1] is None:
                imageArray[1] = self.b_T(_js(_js("/", string), "_r.png"))
        elif imageArray[0] is None:
            imageArray[0] = self.b_T(_js(_js("/", string), ".png"))
        if aArray[0] is None:
            if n2 == 0:
                aArray[0] = SpriteFrames(_js(_js("/", string), ".SP2"))
                return
            if n2 == 1:
                aArray[0] = SpriteFrames(_js(_js("/", string), "_basic.SP2"))
                aArray[1] = SpriteFrames(_js(_js("/", string), "_skill1.SP2"))
                aArray[2] = SpriteFrames(_js(_js("/", string), "_skill2.SP2"))

    def W_v(self):  # g.java:5534
        n2 = 0
        n3 = 0
        Draw.b_GIIIII(MpCanvas.g, 0, 0, MpCanvas.cQ, MpCanvas.cR, 0)
        n3 = (idiv(MpCanvas.cT, 2) - 95)
        n4 = (idiv(MpCanvas.cS, 30) + 1)
        n5 = ((MpCanvas.by >> 6) & 3)
        _sw117 = n5
        if _sw117 == 0:
            self.n_I(4)
            self.n_I(5)
            self.n_I(6)
            self.n_I(7)
            self.n_I(8)
            Draw.b_GIIIII(MpCanvas.g, 0, 0, MpCanvas.cQ, (n3 + 1), 11257599)
            n2 = 0
            while n2 < n4:
                MpCanvas.a_GIIM(MpCanvas.g, (30 * n2), n3, MpCanvas.dj[4])
                MpCanvas.a_GIIM(MpCanvas.g, (30 * n2), (n3 + 30), MpCanvas.dj[5])
                n2 = n2 + 1
            MpCanvas.a_GIIM(MpCanvas.g, (MpCanvas.cS - MpCanvas.dj[6].getWidth()), ((n3 - 2) - MpCanvas.dj[6].getHeight()), MpCanvas.dj[6])
            MpCanvas.a_GIIM(MpCanvas.g, 18, (n3 - 30), MpCanvas.dj[7])
            MpCanvas.a_GIIM(MpCanvas.g, 52, (n3 - 15), MpCanvas.dj[8])
        elif _sw117 == 1:
            self.n_I(9)
            self.n_I(10)
            self.n_I(11)
            self.n_I(12)
            self.n_I(13)
            Draw.b_GIIIII(MpCanvas.g, 0, 0, MpCanvas.cQ, (n3 + 1), 1645890)
            n2 = 0
            while n2 < n4:
                MpCanvas.a_GIIM(MpCanvas.g, (30 * n2), n3, MpCanvas.dj[9])
                MpCanvas.a_GIIM(MpCanvas.g, (30 * n2), (n3 + 30), MpCanvas.dj[10])
                n2 = n2 + 1
            MpCanvas.a_GIIM(MpCanvas.g, (MpCanvas.cS - MpCanvas.dj[6].getWidth()), ((n3 - 2) - MpCanvas.dj[6].getHeight()), MpCanvas.dj[11])
            MpCanvas.a_GIIM(MpCanvas.g, 18, (n3 - 30), MpCanvas.dj[12])
            MpCanvas.a_GIIM(MpCanvas.g, 52, (n3 - 15), MpCanvas.dj[13])
        n6 = ((MpCanvas.by >> 4) & 3)
        self.n_I((14 + n6))
        n2 = 0
        while n2 < n4:
            MpCanvas.a_GIIM(MpCanvas.g, (30 * n2), (n3 + 83), MpCanvas.dj[(14 + n6)])
            n2 = n2 + 1
        n7 = (MpCanvas.by & 3)
        n8 = 0
        nArray = [3, 8, (-8), 16]
        self.n_I((0 + n7))
        n8 = (n3 + nArray[n7])
        MpCanvas.a_GIIM(MpCanvas.g, 0, n8, MpCanvas.dj[(0 + n7)])
        n2 = 0
        while n2 < len(MpCanvas.dj):
            MpCanvas.dj[n2] = None
            n2 = n2 + 1
        MpCanvas.X_v()

    @staticmethod
    def X_v():  # g.java:5599
        None

    def n_I(self, n2):  # g.java:5603
        if MpCanvas.dj[n2] is None:
            MpCanvas.dj[n2] = self.b_T(_js(_js("/gamebg", n2), ".png"))

    def Y_v(self):  # g.java:5609
        Draw.b_GIIIII(MpCanvas.g, 0, 0, MpCanvas.cQ, 12, 0)
        MpCanvas.o_I(0)
        n2 = 0
        Draw.a_GIIII(MpCanvas.g, 28, 4, (MpCanvas.bK - 1), 8429760)
        Draw.a_GIIII(MpCanvas.g, 28, 10, (MpCanvas.bK - 1), 8429760)
        Draw.a_GIIII(MpCanvas.g, 31, 4, ((MpCanvas.bK - 1) - 6), 0x808080)
        Draw.a_GIIII(MpCanvas.g, 31, 10, ((MpCanvas.bK - 1) - 6), 0x808080)
        n2 = (28 + MpCanvas.bK)
        Draw.b_GIIII(MpCanvas.g, n2, 0, 10, 0x808080)
        Draw.b_GIIII(MpCanvas.g, n2, 3, 1, 8429760)
        Draw.b_GIIII(MpCanvas.g, n2, 4, 1, 0)
        Draw.b_GIIII(MpCanvas.g, n2, 5, 1, 8429760)
        Draw.b_GIIII(MpCanvas.g, n2, 9, 1, 8429760)
        MpCanvas.o_I(1)
        n2 = (((MpCanvas.cQ - 28) - MpCanvas.bK) + 1)
        Draw.a_GIIII(MpCanvas.g, n2, 4, (MpCanvas.bK - 1), 8429760)
        Draw.a_GIIII(MpCanvas.g, n2, 10, (MpCanvas.bK - 1), 8429760)
        Draw.a_GIIII(MpCanvas.g, (n2 + 3), 4, ((MpCanvas.bK - 1) - 6), 0x808080)
        Draw.a_GIIII(MpCanvas.g, (n2 + 3), 10, ((MpCanvas.bK - 1) - 6), 0x808080)
        n2 = (((MpCanvas.cQ - 28) - 1) - MpCanvas.bK)
        Draw.b_GIIII(MpCanvas.g, n2, 0, 10, 0x808080)
        Draw.b_GIIII(MpCanvas.g, n2, 3, 1, 8429760)
        Draw.b_GIIII(MpCanvas.g, n2, 4, 1, 0)
        Draw.b_GIIII(MpCanvas.g, n2, 5, 1, 8429760)
        Draw.b_GIIII(MpCanvas.g, n2, 9, 1, 8429760)
        if MpCanvas.bz != 0:
            Draw.b_GIIIII(MpCanvas.g, 0, (MpCanvas.cR - 12), MpCanvas.cQ, 12, 0)
            MpCanvas.o_I(2)
            Draw.a_GIIII(MpCanvas.g, 28, (MpCanvas.cR - 5), (MpCanvas.bK - 1), 8429760)
            Draw.a_GIIII(MpCanvas.g, 28, (MpCanvas.cR - 11), (MpCanvas.bK - 1), 8429760)
            Draw.a_GIIII(MpCanvas.g, 31, (MpCanvas.cR - 5), (MpCanvas.bK - 6), 0x808080)
            Draw.a_GIIII(MpCanvas.g, 31, (MpCanvas.cR - 11), (MpCanvas.bK - 6), 0x808080)
            n2 = ((28 + MpCanvas.bK) + 1)
            Draw.b_GIIII(MpCanvas.g, (n2 - 1), (MpCanvas.cR - 9), 9, 0x808080)
            Draw.b_GIIII(MpCanvas.g, (n2 - 1), (MpCanvas.cR - 4), 1, 8429760)
            Draw.b_GIIII(MpCanvas.g, (n2 - 1), (MpCanvas.cR - 5), 1, 0)
            Draw.b_GIIII(MpCanvas.g, (n2 - 1), (MpCanvas.cR - 6), 1, 8429760)
            Draw.b_GIIII(MpCanvas.g, (n2 - 1), (MpCanvas.cR - 10), 1, 8429760)
            MpCanvas.o_I(3)
            n2 = (((MpCanvas.cQ - 28) - MpCanvas.bK) + 1)
            Draw.a_GIIII(MpCanvas.g, n2, (MpCanvas.cR - 5), (MpCanvas.bK - 1), 8429760)
            Draw.a_GIIII(MpCanvas.g, n2, (MpCanvas.cR - 11), (MpCanvas.bK - 1), 8429760)
            Draw.a_GIIII(MpCanvas.g, (n2 + 3), (MpCanvas.cR - 5), ((MpCanvas.bK - 1) - 6), 0x808080)
            Draw.a_GIIII(MpCanvas.g, (n2 + 3), (MpCanvas.cR - 11), ((MpCanvas.bK - 1) - 6), 0x808080)
            n2 = (((MpCanvas.cQ - 28) - 1) - MpCanvas.bK)
            Draw.b_GIIII(MpCanvas.g, n2, (MpCanvas.cR - 9), 10, 0x808080)
            Draw.b_GIIII(MpCanvas.g, n2, (MpCanvas.cR - 4), 1, 8429760)
            Draw.b_GIIII(MpCanvas.g, n2, (MpCanvas.cR - 5), 1, 0)
            Draw.b_GIIII(MpCanvas.g, n2, (MpCanvas.cR - 6), 1, 8429760)
            Draw.b_GIIII(MpCanvas.g, n2, (MpCanvas.cR - 10), 1, 8429760)

    @staticmethod
    def o_I(n2):  # g.java:5663
        n3 = (28 if (imod(n2, 2) == 0) else ((((MpCanvas.cQ - 28) - 1) - MpCanvas.bK) + 2))
        n4 = (0 if (idiv(n2, 2) == 0) else ((MpCanvas.cR - 3) - 6))
        n5 = 0
        while n5 < 2:
            if n5 == 1:
                n4 = (n4 + 6)
            Draw.a_GIIII(MpCanvas.g, n3, n4, (MpCanvas.bK - 1), 0x808080)
            Draw.a_GIIII(MpCanvas.g, n3, (n4 + 1), (MpCanvas.bK - 1), 0xFFFFFF)
            Draw.a_GIIII(MpCanvas.g, n3, (n4 + 2), (MpCanvas.bK - 1), 0xC0C0C0)
            n5 = n5 + 1

    def k_G(self, graphics):  # g.java:5678
        self.l_G(graphics)

    def l_G(self, graphics):  # g.java:5682
        n2 = 0
        n3 = 0
        n4 = 0
        MpCanvas.n_G(graphics)
        if MpCanvas.cR <= 144:
            n4 = (78 - idiv(((144 - MpCanvas.cR)), 2))
            n3 = ((MpCanvas.cR - 18) - n4)
            Draw.a_GMIIIIII(graphics, MpCanvas.dk, 0, 5, 5, 8, 0, 0)
            Draw.a_GMIIIIII(graphics, MpCanvas.dk, 0, 13, 5, n4, 0, (8 + ((78 - n4))))
            Draw.a_GMIIIIII(graphics, MpCanvas.dk, 0, (13 + n4), 5, n3, 0, (134 - n3))
            n2 = (MpCanvas.cQ - 5)
            Draw.a_GMIIIIII(graphics, MpCanvas.dk, n2, 5, 5, 8, 5, 0)
            Draw.a_GMIIIIII(graphics, MpCanvas.dk, n2, 13, 5, n4, 5, (8 + ((78 - n4))))
            Draw.a_GMIIIIII(graphics, MpCanvas.dk, n2, (13 + n4), 5, n3, 5, (134 - n3))
        else:
            n4 = idiv(((MpCanvas.cR - 144)), 2)
            n3 = ((MpCanvas.cR - 144) - n4)
            Draw.a_GMIIIIII(graphics, MpCanvas.dk, 0, 5, 5, 59, 0, 0)
            MpCanvas.d_GIIII(graphics, 0, 64, n4, 0)
            Draw.a_GMIIIIII(graphics, MpCanvas.dk, 0, (64 + n4), 5, 17, 0, 59)
            MpCanvas.d_GIIII(graphics, 0, ((64 + n4) + 17), n3, 0)
            Draw.a_GMIIIIII(graphics, MpCanvas.dk, 0, ((MpCanvas.cR - 5) - 58), 5, 58, 0, 76)
            n2 = (MpCanvas.cQ - 5)
            Draw.a_GMIIIIII(graphics, MpCanvas.dk, n2, 5, 5, 59, 5, 0)
            MpCanvas.d_GIIII(graphics, n2, 64, n4, 5)
            Draw.a_GMIIIIII(graphics, MpCanvas.dk, n2, (64 + n4), 5, 17, 5, 59)
            MpCanvas.d_GIIII(graphics, n2, ((64 + n4) + 17), n4, 5)
            Draw.a_GMIIIIII(graphics, MpCanvas.dk, n2, ((MpCanvas.cR - 5) - 58), 5, 58, 5, 76)
        n4 = idiv(((MpCanvas.cQ - 120)), 2)
        n3 = ((MpCanvas.cQ - 120) - n4)
        Draw.a_GMIIIIII(graphics, MpCanvas.dm, 0, 0, 21, 5, 0, 0)
        MpCanvas.e_GIIII(graphics, 21, 0, n4, 0)
        Draw.a_GMIIIIII(graphics, MpCanvas.dm, (21 + n4), 0, 77, 5, 21, 0)
        MpCanvas.e_GIIII(graphics, (98 + n4), 0, n3, 0)
        Draw.a_GMIIIIII(graphics, MpCanvas.dm, (MpCanvas.cQ - 21), 0, 21, 5, 98, 0)
        n2 = (MpCanvas.cR - 5)
        Draw.a_GMIIIIII(graphics, MpCanvas.dm, 0, n2, 37, 5, 0, 5)
        MpCanvas.e_GIIII(graphics, 37, n2, n4, 5)
        Draw.a_GMIIIIII(graphics, MpCanvas.dm, (37 + n4), n2, 45, 5, 37, 5)
        MpCanvas.e_GIIII(graphics, (82 + n4), n2, n3, 5)
        Draw.a_GMIIIIII(graphics, MpCanvas.dm, (MpCanvas.cQ - 37), n2, 37, 5, 82, 5)
        Draw.a_GMIIIIII(graphics, MpCanvas.dn, (MpCanvas.cW - 46), 0, 46, 15, 0, 0)
        Draw.a_GMIIIIII(graphics, MpCanvas.dn, MpCanvas.cW, 0, 46, 15, 17, 0)
        self.a_GTIIII(graphics, MpCanvas.c, idiv(MpCanvas.cQ, 2), 2, 1, 0xFFFFFF)

    def a_GTIIIIZZ(self, graphics, string, n2, n3, n4, n5, bl, bl2):  # g.java:5730
        if bl:
            Draw.a_GIIIIII(graphics, (n2 - 1), (n3 - 1), (n4 + 2), (n5 + 2), 1, 0xFFFFFF)
            Draw.a_GIIIII(graphics, n2, n3, n4, n5, 0xFFFFFF)
        MpCanvas.c_GIIII(graphics, n2, n3, n4, n5)
        if not bl2:
            self.a_IITI((n2 + idiv(n4, 2)), (n3 + idiv(((n5 - 11)), 2)), string, 0x646464)
            return
        self.a_IITI((n2 + idiv(n4, 2)), (n3 + idiv(((n5 - 11)), 2)), string, 0xFFFFFF)

    @staticmethod
    def c_GIIII(graphics, n2, n3, n4, n5):  # g.java:5743
        Draw.a_GIIIIII(graphics, n2, n3, n4, n5, 1, 0x949694)
        Draw.b_GIIIII(graphics, (n2 + 1), (n3 + 1), (n4 - 2), (n5 - 2), 0)

    def m_G(self, graphics):  # g.java:5748
        MpCanvas.cL = 0
        while MpCanvas.cL < 4:
            if MpCanvas.bQ[MpCanvas.cL]:
                if imod(MpCanvas.bR[MpCanvas.cL], 2) == 0:
                    if MpCanvas.ca[MpCanvas.cL] == 0:
                        self.a_AMTI(MpCanvas.de, "face", MpCanvas.bZ[MpCanvas.cL])
                        MpCanvas.c_GIIM(graphics, 0, (0 if (idiv(MpCanvas.bR[MpCanvas.cL], 2) == 0) else (MpCanvas.cR - 12)), MpCanvas.de[MpCanvas.bZ[MpCanvas.cL]])
                        MpCanvas.de[MpCanvas.bZ[MpCanvas.cL]] = None
                    self.c_GIIIII(graphics, 0, (12 if (idiv(MpCanvas.bR[MpCanvas.cL], 2) == 0) else ((MpCanvas.cR - 12) - 15)), 60, 15, 1)
                    if (len(MpCanvas.bP[MpCanvas.cL]) == 0) or (imod(MpCanvas.aR, 2) == 0):
                        self.a_GIITI(graphics, 30, (14 if (idiv(MpCanvas.bR[MpCanvas.cL], 2) == 0) else (((MpCanvas.cR - 12) - 15) + 2)), MpCanvas.bM[MpCanvas.cL], 0xFFFFFF)
                    else:
                        self.a_GIITI(graphics, 30, (14 if (idiv(MpCanvas.bR[MpCanvas.cL], 2) == 0) else (((MpCanvas.cR - 12) - 15) + 2)), MpCanvas.bP[MpCanvas.cL], 0xFFFFFF)
                else:
                    if MpCanvas.ca[MpCanvas.cL] == 0:
                        self.a_AMTI(MpCanvas.de, "face", MpCanvas.bZ[MpCanvas.cL])
                        MpCanvas.b_GIIM(graphics, MpCanvas.cQ, (0 if (idiv(MpCanvas.bR[MpCanvas.cL], 2) == 0) else (MpCanvas.cR - 12)), MpCanvas.de[MpCanvas.bZ[MpCanvas.cL]])
                        MpCanvas.de[MpCanvas.bZ[MpCanvas.cL]] = None
                    self.c_GIIIII(graphics, (MpCanvas.cQ - 60), (12 if (idiv(MpCanvas.bR[MpCanvas.cL], 2) == 0) else ((MpCanvas.cR - 12) - 15)), 60, 15, 1)
                    if (len(MpCanvas.bP[MpCanvas.cL]) == 0) or (imod(MpCanvas.aR, 2) == 0):
                        self.a_GIITI(graphics, (MpCanvas.cQ - 30), (14 if (idiv(MpCanvas.bR[MpCanvas.cL], 2) == 0) else (((MpCanvas.cR - 12) - 15) + 2)), MpCanvas.bM[MpCanvas.cL], 0xFFFFFF)
                    else:
                        self.a_GIITI(graphics, (MpCanvas.cQ - 30), (14 if (idiv(MpCanvas.bR[MpCanvas.cL], 2) == 0) else (((MpCanvas.cR - 12) - 15) + 2)), MpCanvas.bP[MpCanvas.cL], 0xFFFFFF)
            MpCanvas.cL = MpCanvas.cL + 1
        MpCanvas.X_v()

    @staticmethod
    def d_GIIII(graphics, n2, n3, n4, n5):  # g.java:5783
        n6 = (idiv(n4, 11) + 1)
        n7 = 0
        while n7 < n6:
            Draw.a_GMIIIIII(graphics, MpCanvas.dk, n2, (n3 + (11 * n7)), 5, 11, n5, 8)
            n7 = n7 + 1

    @staticmethod
    def n_G(graphics):  # g.java:5792
        n2 = (idiv(MpCanvas.cQ, MpCanvas.dl.getWidth()) + 1)
        n3 = (idiv(MpCanvas.cR, MpCanvas.dl.getHeight()) + 1)
        n4 = 0
        while n4 < n2:
            n5 = 0
            while n5 < n3:
                if imod(n5, 2) != 0:
                    Draw.a_GMIII(graphics, MpCanvas.dl, (MpCanvas.dl.getWidth() * n4), (MpCanvas.dl.getHeight() * n5), 0)
                else:
                    Draw.a_GMIIIIII(graphics, MpCanvas.dl, (MpCanvas.dl.getWidth() * n4), (MpCanvas.dl.getHeight() * n5), 21, 24, 31, 0)
                    Draw.a_GMIIIIII(graphics, MpCanvas.dl, ((MpCanvas.dl.getWidth() * n4) + 21), (MpCanvas.dl.getHeight() * n5), 31, 24, 0, 0)
                n5 = n5 + 1
            n4 = n4 + 1

    @staticmethod
    def e_GIIII(graphics, n2, n3, n4, n5):  # g.java:5811
        n6 = (idiv(n4, 11) + 1)
        n7 = 0
        while n7 < n6:
            Draw.a_GMIIIIII(graphics, MpCanvas.dm, (n2 + (11 * n7)), n3, 11, 5, 10, n5)
            n7 = n7 + 1

    def o_G(self, graphics):  # g.java:5820
        self.k_G(graphics)
        MpCanvas.cL = 0
        while MpCanvas.cL < 3:
            self.c_GIIIII(graphics, (MpCanvas.cW - 58), ((MpCanvas.cX - 16) + (MpCanvas.cL * 19)), 61, 14, 2)
            self.a_GTIIII(graphics, Consts.eW[MpCanvas.cL], (MpCanvas.cW - 28), ((MpCanvas.cX - 15) + (MpCanvas.cL * 19)), 1, 0x646464)
            self.c_GIIIII(graphics, (MpCanvas.cW + 13), ((MpCanvas.cX - 16) + (MpCanvas.cL * 19)), 39, 14, 2)
            MpCanvas.cL = MpCanvas.cL + 1

    def Z_v(self):  # g.java:5831
        self.k_G(MpCanvas.e)
        MpCanvas.cL = 0
        while MpCanvas.cL < 6:
            self.c_GIIIII(MpCanvas.e, (MpCanvas.cW - 60), ((MpCanvas.cX - 47) + (MpCanvas.cL * 17)), 81, 14, 2)
            self.c_GIIIII(MpCanvas.e, (MpCanvas.cW + 23), ((MpCanvas.cX - 47) + (MpCanvas.cL * 17)), 37, 14, 2)
            self.a_GTIIII(MpCanvas.e, Consts.eX[(46 + MpCanvas.cL)], (MpCanvas.cW - 19), ((MpCanvas.cX - 45) + (MpCanvas.cL * 17)), 1, 0xFFFFFF)
            _sw118 = MpCanvas.cL
            if _sw118 == 0:
                self.c_III((MpCanvas.cW + 52), ((MpCanvas.cX - 44) + (MpCanvas.cL * 17)), MpCanvas.as_)
            elif _sw118 == 1:
                self.e_III((MpCanvas.cW + 52), ((MpCanvas.cX - 44) + (MpCanvas.cL * 17)), MpCanvas.ax)
            elif _sw118 == 2:
                MpCanvas.cu = MpCanvas.aA
            elif _sw118 == 3:
                MpCanvas.cu = MpCanvas.at
            elif _sw118 == 4:
                MpCanvas.cu = MpCanvas.au
            elif _sw118 == 5:
                MpCanvas.cu = MpCanvas.aB
            if MpCanvas.cL > 1:
                self.d_III((MpCanvas.cW + 52), ((MpCanvas.cX - 44) + (MpCanvas.cL * 17)), MpCanvas.cu)
            MpCanvas.cL = MpCanvas.cL + 1

    def aa_v(self):  # g.java:5870
        self.k_G(MpCanvas.e)
        n2 = 0
        MpCanvas.cL = 0
        while MpCanvas.cL < 4:
            self.c_GIIIII(MpCanvas.e, (MpCanvas.cW - 54), ((MpCanvas.cX - 30) + (MpCanvas.cL * 17)), 39, 14, 2)
            self.c_GIIIII(MpCanvas.e, (MpCanvas.cW - 13), ((MpCanvas.cX - 30) + (MpCanvas.cL * 17)), 67, 14, 2)
            self.a_GTIIII(MpCanvas.e, Consts.eX[(42 + MpCanvas.cL)], (MpCanvas.cW - 35), ((MpCanvas.cX - 28) + (MpCanvas.cL * 17)), 1, 0xFFFFFF)
            _sw119 = MpCanvas.cL
            if _sw119 == 0:
                MpCanvas.cu = MpCanvas.aC
                n2 = MpCanvas.aD
            elif _sw119 == 1:
                MpCanvas.cu = MpCanvas.aE
                n2 = MpCanvas.aF
            elif _sw119 == 2:
                MpCanvas.cu = MpCanvas.aG
                n2 = MpCanvas.aH
            elif _sw119 == 3:
                MpCanvas.cu = MpCanvas.aI
                n2 = MpCanvas.aJ
            self.b_III((MpCanvas.cW + 9), ((MpCanvas.cX - 27) + (MpCanvas.cL * 17)), MpCanvas.cu)
            self.a_III((MpCanvas.cW + 52), ((MpCanvas.cX - 27) + (MpCanvas.cL * 17)), n2)
            MpCanvas.cL = MpCanvas.cL + 1

    def p_G(self, graphics):  # g.java:5905
        self.k_G(graphics)
        MpCanvas.cL = 0
        while MpCanvas.cL < 5:
            self.c_GIIIII(graphics, (MpCanvas.cW - 58), ((MpCanvas.cX - 51) + (MpCanvas.cL * 16)), 91, 14, 2)
            self.c_GIIIII(graphics, (MpCanvas.cW + 43), ((MpCanvas.cX - 51) + (MpCanvas.cL * 16)), 15, 14, 2)
            MpCanvas.cL = MpCanvas.cL + 1
        self.a_GIITI(graphics, (MpCanvas.cW - 13), (MpCanvas.cX - 49), "NAME", 0xFFFFFF)
        self.a_GIITI(graphics, (MpCanvas.cW + 51), (MpCanvas.cX - 49), "LV", 0xFFFFFF)
        MpCanvas.a_GIIIII(graphics, (MpCanvas.cW - 52), (MpCanvas.cX + 31), 104, 27, 0)
        MpCanvas.b_GIIIII(graphics, (MpCanvas.cW - 52), (MpCanvas.cX + 30), (MpCanvas.cW + 51), (MpCanvas.cX + 30), 0x804000)
        MpCanvas.b_GIIIII(graphics, (MpCanvas.cW - 52), (MpCanvas.cX + 58), (MpCanvas.cW + 51), (MpCanvas.cX + 58), 0x804000)
        MpCanvas.b_GIIIII(graphics, (MpCanvas.cW - 53), (MpCanvas.cX + 31), (MpCanvas.cW - 53), (MpCanvas.cX + 57), 0x804000)
        MpCanvas.b_GIIIII(graphics, (MpCanvas.cW + 52), (MpCanvas.cX + 31), (MpCanvas.cW + 52), (MpCanvas.cX + 57), 0x804000)

    def ab_v(self):  # g.java:5922
        MpCanvas.cL = 0
        while MpCanvas.cL < 4:
            if MpCanvas.dU[MpCanvas.dW] == MpCanvas.cL:
                if imod(MpCanvas.da, 4) < 2:
                    MpCanvas.c_IIM((MpCanvas.cW - 65), ((MpCanvas.cX - 32) + (MpCanvas.cL * 16)), MpCanvas.di[1])
                    MpCanvas.b_IIM((MpCanvas.cW + 40), ((MpCanvas.cX - 32) + (MpCanvas.cL * 16)), MpCanvas.di[1])
                self.c_GIIIII(MpCanvas.e, (MpCanvas.cW - 58), ((MpCanvas.cX - 35) + (MpCanvas.cL * 16)), 91, 14, 3)
                self.c_GIIIII(MpCanvas.e, (MpCanvas.cW + 43), ((MpCanvas.cX - 35) + (MpCanvas.cL * 16)), 15, 14, 3)
            if MpCanvas.cH[(MpCanvas.cB[MpCanvas.cL] - 3)] == 99:
                self.a_GIITI(MpCanvas.e, (MpCanvas.cW - 12), ((MpCanvas.cX - 33) + (MpCanvas.cL * 16)), Consts.eK[(MpCanvas.cB[MpCanvas.cL] - 3)], 0x646464)
                if MpCanvas.dU[MpCanvas.dW] == MpCanvas.cL:
                    self.b_IITI((MpCanvas.cW - 50), (MpCanvas.cX + 32), Consts.eX[34], 0x646464)
            else:
                self.a_GIITI(MpCanvas.e, (MpCanvas.cW - 12), ((MpCanvas.cX - 33) + (MpCanvas.cL * 16)), Consts.eK[(MpCanvas.cB[MpCanvas.cL] - 3)], 0xFFFFFF)
                self.c_III((MpCanvas.cW + 48), ((MpCanvas.cX - 32) + (MpCanvas.cL * 16)), MpCanvas.cH[(MpCanvas.cB[MpCanvas.cL] - 3)])
                if MpCanvas.dU[MpCanvas.dW] == MpCanvas.cL:
                    self.b_IITI((MpCanvas.cW - 50), (MpCanvas.cX + 32), Consts.eJ[(((MpCanvas.cB[MpCanvas.cL] - 3)) * 2)], 0xFFFFFF)
                    self.b_IITI((MpCanvas.cW - 50), (MpCanvas.cX + 45), Consts.eJ[((((MpCanvas.cB[MpCanvas.cL] - 3)) * 2) + 1)], 0xFFFFFF)
            MpCanvas.cL = MpCanvas.cL + 1

    def ac_v(self):  # g.java:5950
        self.k_G(MpCanvas.e)
        MpCanvas.cL = 0
        while MpCanvas.cL < 3:
            self.c_GIIIII(MpCanvas.e, (MpCanvas.cW - 50), ((MpCanvas.cX - 45) + (MpCanvas.cL * 34)), 100, 14, 2)
            self.c_GIIIII(MpCanvas.e, (MpCanvas.cW - 50), ((MpCanvas.cX - 32) + (MpCanvas.cL * 34)), 100, 14, 2)
            self.a_GTIIII(MpCanvas.e, Consts.eX[(52 + MpCanvas.cL)], MpCanvas.cW, ((MpCanvas.cX - 43) + (MpCanvas.cL * 34)), 1, 0xFFFFFF)
            _sw120 = MpCanvas.cL
            if _sw120 == 0:
                MpCanvas.cu = MpCanvas.ay
            elif _sw120 == 1:
                MpCanvas.cu = MpCanvas.ax
            elif _sw120 == 2:
                MpCanvas.cu = MpCanvas.az
            self.d_III((MpCanvas.cW + 24), ((MpCanvas.cX - 29) + (MpCanvas.cL * 34)), MpCanvas.cu)
            MpCanvas.cL = MpCanvas.cL + 1

    def q_G(self, graphics):  # g.java:5975
        self.k_G(graphics)
        self.c_GIIIII(graphics, (MpCanvas.cW - 62), (MpCanvas.cX + 7), 126, 16, 6)

    def r_G(self, graphics):  # g.java:5980
        string = MpCanvas.bG
        self.a_IITI(MpCanvas.cW, (MpCanvas.cX - 44), _js(_js(Consts.eX[58], "."), ((MpCanvas.B + 1))), 16400640)
        if MpCanvas.B == 0:
            self.a_IITI(MpCanvas.cW, (MpCanvas.cX - 32), Consts.eX[23], 0xFFFFFF)
            self.a_IITI(MpCanvas.cW, (MpCanvas.cX - 20), Consts.eX[24], 0xFFFFFF)
        else:
            self.a_IITI(MpCanvas.cW, (MpCanvas.cX - 32), Consts.eX[15], 0xFFFFFF)
            self.a_IITI(MpCanvas.cW, (MpCanvas.cX - 20), Consts.eX[16], 0xFFFFFF)
        self.a_IITI(MpCanvas.cW, (MpCanvas.cX - 8), Consts.eX[25], 0xFFFFFF)
        self.a_GIITI(graphics, MpCanvas.cW, (MpCanvas.cX + 9), string, 0x41FF41)
        if imod(MpCanvas.da, 4) < 2:
            n2 = MpCanvas.n.a_T(string)
            if len(string) == 20:
                n2 = (n2 - (MpCanvas.n.a_T("A") * 2))
            MpCanvas.b_GIIIII(graphics, (MpCanvas.cW + idiv(n2, 2)), (MpCanvas.cX + 20), ((MpCanvas.cW + idiv(n2, 2)) + 4), (MpCanvas.cX + 20), 0xFFFFFF)
        MpCanvas.b_II(MpCanvas.C, (MpCanvas.cX + 27))

    @staticmethod
    def a_II(n2, n3):  # g.java:6002
        n4 = (MpCanvas.cW - 57)
        stringArray = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "OK"]
        Gfx.a_IIIII(n4, n3, 115, 22, 0)
        Gfx.a_IIIII((n4 + 99), (n3 + 12), 13, 9, 255)
        if imod(MpCanvas.da, 4) < 2:
            if n2 == 26:
                Gfx.a_IIIII((n4 + 99), (n3 + 12), 13, 9, 0xFF0000)
            else:
                Gfx.a_IIIII(((n4 + 2) + (imod(n2, 14) * 8)), ((n3 + 1) + (11 * (idiv(n2, 14)))), 7, 9, 0xFF0000)
        Gfx.a_Lj(MpCanvas.n)
        n5 = 0
        while n5 < len(stringArray):
            n6 = (1 if (n5 == 8) else ((1 if (n5 == 26) else 0)))
            Gfx.a_TIII(stringArray[n5], (((n4 + 3) + (imod(n5, 14) * 8)) + n6), (n3 + (11 * (idiv(n5, 14)))), 0)
            n5 = n5 + 1

    @staticmethod
    def p_I(n2):  # g.java:6023
        n3 = n2
        if ((n2 != (-7)) and (n2 != (-5))) and (n2 != (-6)):
            if n2 == (-1):
                MpCanvas.C = imod((((MpCanvas.C + 28) - 14)), 28)
            elif n2 == (-2):
                MpCanvas.C = imod((((MpCanvas.C + 28) + 14)), 28)
            elif n2 == (-3):
                MpCanvas.C = imod((((MpCanvas.C + 28) - 1)), 28)
            elif (n2 == (-4)) and ((_set(MpCanvas, 'C', imod((((MpCanvas.C + 28) + 1)), 28))) == 27):
                MpCanvas.C = 0
        if MpCanvas.C == 27:
            MpCanvas.C = 26
        return n3

    @staticmethod
    def b_II(n2, n3):  # g.java:6042
        n4 = (MpCanvas.cW - 60)
        stringArray = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " ", "OK"]
        Gfx.a_IIIII(n4, n3, 120, 22, 0)
        Gfx.a_IIIII((n4 + 99), (n3 + 13), 5, 7, 0x666666)
        Gfx.a_IIIII((n4 + 106), (n3 + 12), 13, 9, 255)
        if imod(MpCanvas.da, 4) < 2:
            if n2 == 27:
                Gfx.a_IIIII((n4 + 106), (n3 + 12), 13, 9, 0xFF0000)
            else:
                Gfx.a_IIIII(((n4 + 2) + (imod(n2, 14) * 8)), ((n3 + 1) + (11 * (idiv(n2, 14)))), 7, 9, 0xFF0000)
        Gfx.a_Lj(MpCanvas.n)
        n5 = 0
        while n5 < len(stringArray):
            n6 = (1 if (n5 == 8) else ((1 if (n5 == 26) else 0)))
            Gfx.a_TIII(stringArray[n5], (((n4 + 3) + (imod(n5, 14) * 8)) + n6), (n3 + (11 * (idiv(n5, 14)))), 0)
            n5 = n5 + 1

    @staticmethod
    def q_I(n2):  # g.java:6064
        n3 = n2
        if ((n2 != (-7)) and (n2 != (-5))) and (n2 != (-6)):
            if n2 == (-1):
                MpCanvas.C = imod((((MpCanvas.C + 28) - 14)), 28)
            elif n2 == (-2):
                MpCanvas.C = imod((((MpCanvas.C + 28) + 14)), 28)
            elif n2 == (-3):
                MpCanvas.C = imod((((MpCanvas.C + 28) - 1)), 28)
            elif n2 == (-4):
                MpCanvas.C = imod((((MpCanvas.C + 28) + 1)), 28)
        return n3

    @staticmethod
    def d_T(string):  # g.java:6080
        n2 = len(string)
        n3 = (n2 - 1)
        while n3 >= 0:
            if ord(string[n3]) != 32:
                break
            n3 = n3 - 1
        if n3 == 0:
            return ""
        return string[0:(n3 + 1)]

    def s_G(self, graphics):  # g.java:6093
        self.k_G(graphics)
        self.c_GIIIII(graphics, (MpCanvas.cW - 62), (MpCanvas.cX + 7), 126, 16, 6)
        self.a_GIITI(graphics, MpCanvas.cW, (MpCanvas.cX - 32), Consts.eU[0], 0xFFFFFF)
        self.a_GIITI(graphics, MpCanvas.cW, (MpCanvas.cX - 20), Consts.eU[1], 0xFFFFFF)
        self.a_GIITI(graphics, MpCanvas.cW, (MpCanvas.cX - 8), Consts.eU[2], 0xFFFFFF)

    def t_G(self, graphics):  # g.java:6101
        self.a_GIITI(graphics, MpCanvas.cW, (MpCanvas.cX + 9), MpCanvas.bG, 0x41FF41)
        if imod(MpCanvas.da, 4) < 2:
            n2 = MpCanvas.n.a_T(MpCanvas.bG)
            if len(MpCanvas.bG) == 8:
                n2 = (n2 - (MpCanvas.n.a_T("A") * 2))
            MpCanvas.b_GIIIII(graphics, (MpCanvas.cW + idiv(n2, 2)), (MpCanvas.cX + 20), ((MpCanvas.cW + idiv(n2, 2)) + 4), (MpCanvas.cX + 20), 0xFFFFFF)
        MpCanvas.a_II(MpCanvas.C, (MpCanvas.cX + 27))

    def u_G(self, graphics):  # g.java:6113
        self.c_GIIIII(graphics, (MpCanvas.cW - 60), ((MpCanvas.cX - 35) - 5), 120, 94, 5)
        self.a_GIITI(graphics, MpCanvas.cW, (MpCanvas.cX - 32), Consts.eU[3], 0xFFFFFF)
        self.a_GIITI(graphics, MpCanvas.cW, (MpCanvas.cX - 20), Consts.eU[4], 0xFFFFFF)
        self.a_GIITI(graphics, MpCanvas.cW, (MpCanvas.cX - 8), Consts.eU[5], 0xFFFFFF)
        self.a_GIITI(graphics, MpCanvas.cW, (MpCanvas.cX + 8), MpCanvas.bG, 0x41FF41)
        MpCanvas.cL = 0
        while MpCanvas.cL < 2:
            self.c_GIIIII(graphics, ((MpCanvas.cW - 42) + (MpCanvas.cL * 55)), (MpCanvas.cX + 35), 29, 14, 2)
            self.a_GTIIII(graphics, Consts.eX[(40 + MpCanvas.cL)], ((MpCanvas.cW - 28) + (MpCanvas.cL * 55)), (MpCanvas.cX + 38), 1, 0x646464)
            if MpCanvas.dU[MpCanvas.dW] == MpCanvas.cL:
                self.a_GTIIII(graphics, Consts.eX[(40 + MpCanvas.cL)], ((MpCanvas.cW - 28) + (MpCanvas.cL * 55)), (MpCanvas.cX + 38), 1, 0xFFFFFF)
                self.c_GIIIII(graphics, ((MpCanvas.cW - 42) + (MpCanvas.cL * 55)), (MpCanvas.cX + 35), 29, 14, 3)
            MpCanvas.cL = MpCanvas.cL + 1

    def v_G(self, graphics):  # g.java:6131
        self.c_GIIIII(graphics, (MpCanvas.cW - 53), (MpCanvas.cX - 34), 106, 68, 5)
        self.a_GIITI(graphics, MpCanvas.cW, (MpCanvas.cX - 22), Consts.eX[56], 0xFFFFFF)
        self.a_GIITI(graphics, MpCanvas.cW, (MpCanvas.cX - 7), Consts.eX[57], 0xFFFFFF)
        n2 = 0
        while n2 < 2:
            self.c_GIIIII(graphics, ((MpCanvas.cW - 42) + (n2 * 55)), (MpCanvas.cX + 15), 29, 14, (3 if (MpCanvas.y == n2) else 2))
            self.a_GTIIII(graphics, Consts.eX[(40 + n2)], ((MpCanvas.cW - 27) + (n2 * 55)), (MpCanvas.cX + 17), 1, (0xFFFFFF if (MpCanvas.y == n2) else 0x646464))
            n2 = n2 + 1

    def ad_v(self):  # g.java:6143
        MpCanvas.bu = 0
        MpCanvas.cL = 0
        while MpCanvas.cL < MpCanvas.cw:
            MpCanvas.bu = (MpCanvas.bu + Consts.eZ[MpCanvas.cL])
            MpCanvas.cL = MpCanvas.cL + 1
        MpCanvas.bJ = 0
        MpCanvas.cL = 0
        while MpCanvas.cL < Consts.eZ[MpCanvas.cw]:
            MpCanvas.bw = True
            if MpCanvas.bw:
                MpCanvas.ed[MpCanvas.cL] = Consts.eY[(MpCanvas.bu + MpCanvas.cL)]
            if MpCanvas.bJ < len(MpCanvas.ed[MpCanvas.cL]):
                MpCanvas.bJ = len(MpCanvas.ed[MpCanvas.cL])
            MpCanvas.cL = MpCanvas.cL + 1
        MpCanvas.cM = 0
        self.c_GIIIII(MpCanvas.e, MpCanvas.cW, MpCanvas.cX, (MpCanvas.bJ * 7), (((((Consts.eZ[MpCanvas.cw] + 1)) * 15) + MpCanvas.cM) + 4), 0)
        MpCanvas.cL = 0
        while MpCanvas.cL < Consts.eZ[MpCanvas.cw]:
            self.a_GIITI(MpCanvas.e, MpCanvas.cW, ((((MpCanvas.cX - idiv((Consts.eZ[MpCanvas.cw] * 15), 2)) + (MpCanvas.cL * 15)) - 4) - idiv(MpCanvas.cM, 3)), MpCanvas.ed[MpCanvas.cL], 0xFFFFFF)
            MpCanvas.cL = MpCanvas.cL + 1
        self.r_I(((MpCanvas.cX + idiv((Consts.eZ[MpCanvas.cw] * 15), 2)) - 5))

    def w_G(self, graphics):  # g.java:6172
        self.k_G(graphics)
        MpCanvas.cL = 0
        while MpCanvas.cL < 2:
            self.c_GIIIII(graphics, (MpCanvas.cW - 56), ((MpCanvas.cX - 16) + (MpCanvas.cL * 20)), 111, 14, 2)
            self.a_GTIIII(graphics, Consts.eX[(38 + MpCanvas.cL)], idiv(MpCanvas.cS, 2), ((MpCanvas.cX - 15) + (MpCanvas.cL * 20)), 1, 0x646464)
            MpCanvas.cL = MpCanvas.cL + 1

    def f_GI(self, graphics, n2):  # g.java:6182
        self.k_G(graphics)
        n3 = 0
        while n3 < 5:
            self.a_GIITI(graphics, MpCanvas.cW, (n2 + (12 * n3)), Consts.eU[(((6 if (MpCanvas.bz == 0) else 12)) + n3)], 0xFFFFFF)
            n3 = n3 + 1
        self.c_GIIIII(graphics, (MpCanvas.cW - 40), (n2 + 59), 80, 15, 6)

    def ae_v(self):  # g.java:6192
        string = ""
        if imod(MpCanvas.da, 4) == 1:
            string = "."
        elif imod(MpCanvas.da, 4) == 2:
            string = ".."
        elif imod(MpCanvas.da, 4) == 3:
            string = "..."
        n2 = (MpCanvas.n.a_T(Consts.fa[MpCanvas.cv]) + 14)
        self.c_GIIIII(MpCanvas.e, MpCanvas.cW, MpCanvas.cX, (n2 + 22), 30, 0)
        self.b_GIITI(MpCanvas.e, (MpCanvas.cW - idiv(n2, 2)), ((MpCanvas.cX - 7) + 2), _js(Consts.fa[MpCanvas.cv], string), 0xFFFFFF)

    def af_v(self):  # g.java:6206
        string = ""
        if imod(MpCanvas.da, 4) == 1:
            string = "."
        elif imod(MpCanvas.da, 4) == 2:
            string = ".."
        elif imod(MpCanvas.da, 4) == 3:
            string = "..."
        n2 = (MpCanvas.n.a_T(Consts.eX[7]) + 14)
        self.c_GIIIII(MpCanvas.e, MpCanvas.cW, MpCanvas.cX, (n2 + 22), 30, 0)
        self.b_GIITI(MpCanvas.e, (MpCanvas.cW - idiv(n2, 2)), (MpCanvas.cX - 6), _js(Consts.eX[7], string), 0xFFFFFF)

    def c_II(self, n2, n3):  # g.java:6220
        if n2 != (-1):
            MpCanvas.a_GIIM(MpCanvas.e, 0, (MpCanvas.cT - 11), MpCanvas.dt)
            self.a_GIITI(MpCanvas.e, 28, (MpCanvas.cT - 11), Consts.eT[n2], 0xFFFFFF)
        if n3 != (-1):
            MpCanvas.a_GIIM(MpCanvas.e, (MpCanvas.cS - 57), (MpCanvas.cT - 11), MpCanvas.dt)
            self.a_GIITI(MpCanvas.e, (MpCanvas.cS - 28), (MpCanvas.cT - 11), Consts.eT[n3], 0xFFFFFF)

    def r_I(self, n2):  # g.java:6231
        self.c_GIIIII(MpCanvas.e, (MpCanvas.cW - 10), (n2 + 1), 18, 9, 3)
        self.a_GIITI(MpCanvas.e, MpCanvas.cW, n2, Consts.eT[0], 0xFFFFFF)

    def s_I(self, n2):  # g.java:6236
        MpCanvas.u_I(n2)

    def t_I(self, n2):  # g.java:6240
        MpCanvas.u_I(n2)

    @staticmethod
    def u_I(n2):  # g.java:6244
        if MpCanvas.b is not None:
            MpGame.v_I(n2)

    def ag_v(self):  # g.java:6250
        if MpCanvas.b is not None:
            MpCanvas.b.ag_v()

    @staticmethod
    def ah_v():  # g.java:6256
        return MpCanvas.am

    def ai_v(self):  # g.java:6260
        MpCanvas.am = imod((((MpCanvas.am + 6) - 1)), 6)
        self.ag_v()
        if MpCanvas.am != 0:
            self.t_I(3)

    def aj_v(self):  # g.java:6268
        MpCanvas.am = imod(((MpCanvas.am + 1)), 6)
        self.ag_v()
        if MpCanvas.am != 0:
            self.t_I(3)


def _static_init():
    MpCanvas.c = ""
    MpCanvas.d = 0
    MpCanvas.e = None
    MpCanvas.h = Random()
    MpCanvas.k = 7
    MpCanvas.m = (-999)
    MpCanvas.n = None
    MpCanvas.o = None
    MpCanvas.p = None
    MpCanvas.q = None
    MpCanvas.u = False
    MpCanvas.w = False
    MpCanvas.x = False
    MpCanvas.D = False
    MpCanvas.H = 0
    MpCanvas.I = (-1)
    MpCanvas.J = False
    MpCanvas.K = False
    MpCanvas.L = False
    MpCanvas.O = True
    MpCanvas.P = True
    MpCanvas.Y = [None] * (3)
    MpCanvas.Z = [0] * (3)
    MpCanvas.aa = [0] * (3)
    MpCanvas.ac = [0, 0, 0, 0]
    MpCanvas.am = 4
    MpCanvas.an = 1
    MpCanvas.ao = 1
    MpCanvas.bx = True
    MpCanvas.bE = [0] * (4)
    MpCanvas.bF = [None] * (4)
    MpCanvas.bM = [None] * (4)
    MpCanvas.bN = [None] * (4)
    MpCanvas.bO = [None] * (4)
    MpCanvas.bP = [None] * (4)
    MpCanvas.bQ = [False] * (4)
    MpCanvas.bR = [0] * (4)
    MpCanvas.bS = [0] * (4)
    MpCanvas.bT = [0] * (4)
    MpCanvas.bU = [0] * (4)
    MpCanvas.bV = [0] * (4)
    MpCanvas.bW = [0] * (4)
    MpCanvas.bX = [0] * (4)
    MpCanvas.bY = [0] * (4)
    MpCanvas.bZ = [0] * (4)
    MpCanvas.ca = [0] * (4)
    MpCanvas.cb = [0] * (4)
    MpCanvas.cc = [0] * (4)
    MpCanvas.cd = [0] * (4)
    MpCanvas.ce = [0] * (4)
    MpCanvas.cf = [0] * (4)
    MpCanvas.cg = [0] * (4)
    MpCanvas.ch = [0] * (4)
    MpCanvas.ci = [0] * (4)
    MpCanvas.cj = [0] * (4)
    MpCanvas.ck = [0] * (4)
    MpCanvas.cl = [0] * (4)
    MpCanvas.cm = [0] * (4)
    MpCanvas.cn = [0] * (4)
    MpCanvas.co = [0] * (4)
    MpCanvas.cp = [0] * (4)
    MpCanvas.cq = [0] * (4)
    MpCanvas.cr = [0] * (4)
    MpCanvas.cB = [0] * (4)
    MpCanvas.cH = [0] * (11)
    MpCanvas.cI = [0] * (11)
    MpCanvas.cJ = [0] * (12)
    MpCanvas.cK = [0] * (44)
    MpCanvas.dc = 100
    MpCanvas.dd = [None] * (6)
    MpCanvas.de = [None] * (4)
    MpCanvas.df = [None] * (57)
    MpCanvas.dg = [None] * (18)
    MpCanvas.dh = [None] * (8)
    MpCanvas.di = [None] * (2)
    MpCanvas.dj = [None] * (22)
    MpCanvas.du = [None] * (2)
    MpCanvas.dv = [None] * (3)
    MpCanvas.dw = [[None] * (2) for _ in range(10)]
    MpCanvas.dx = [[None] * (3) for _ in range(10)]
    MpCanvas.dy = [[None] * (2) for _ in range(2)]
    MpCanvas.dz = [[None] * (3) for _ in range(2)]
    MpCanvas.dA = [[None] * (2) for _ in range(2)]
    MpCanvas.dB = [[None] * (3) for _ in range(2)]
    MpCanvas.dC = [[None] * (2) for _ in range(2)]
    MpCanvas.dD = [[None] * (3) for _ in range(2)]
    MpCanvas.dE = [None] * (1)
    MpCanvas.dF = [None] * (2)
    MpCanvas.dG = [None] * (3)
    MpCanvas.dH = [None] * (2)
    MpCanvas.dI = [None] * (1)
    MpCanvas.dJ = [None] * (2)
    MpCanvas.dK = [None] * (1)
    MpCanvas.dL = [None] * (2)
    MpCanvas.dM = [None] * (1)
    MpCanvas.dN = [None] * (2)
    MpCanvas.dO = [None] * (1)
    MpCanvas.dU = [0] * (10)
    MpCanvas.dV = [0] * (10)
    MpCanvas.dW = 0
    MpCanvas.dX = False
    MpCanvas.dY = True
    MpCanvas.dZ = 0
    MpCanvas.ea = False
    MpCanvas.eb = False
    MpCanvas.ec = (-1)
    MpCanvas.ed = [None] * (10)


def _late_imports():
    global SpriteFrames, PlayerPool, NetThread, ResReader, Consts, Draw, Gfx, Font, Answer, FrameWriter, FrameReader, MpGame
    from pow_mp.sprite_frames import SpriteFrames
    from pow_mp.player_pool import PlayerPool
    from pow_mp.net_thread import NetThread
    from pow_mp.res_reader import ResReader
    from pow_mp.consts import Consts
    from pow_mp.draw import Draw
    from pow_mp.gfx import Gfx
    from pow_mp.font import Font
    from pow_mp.answer import Answer
    from pow_mp.frame_writer import FrameWriter
    from pow_mp.frame_reader import FrameReader
    from pow_mp.mp_game import MpGame
