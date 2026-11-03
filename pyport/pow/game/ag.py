"""ag.java - the main Canvas class (game loop, state machine, shared helpers).

Literal port, Phase 0 subset: everything on the path
logo -> "sound?" -> title -> Main Menu -> Game Menu.
Method names follow tools/java_names.txt (signature suffix when the Java name is overloaded).
Every method has a `# ag.java:FROM-TO` comment. Methods that are not ported yet raise
NotPorted so a missing piece is loud, not silent.
"""
import sys
import traceback

import config
from pow.game import ae
from pow.game._ag_fields import AgFields
from pow.game.al import al
from pow.game.g import g
from pow.game import heroes
from pow.game.j import j
from pow.game.structs import ac, ai, ao, t, z
from pow.game.x import x
from pow.midp import system
from pow.midp.canvas import Canvas
from pow.midp.graphics import Image
from pow.midp.jint import i8, i16, i32, idiv, imod
from pow.midp.rms import RecordStore

F10 = config.DECOMP_FIX["F10"]
F12 = config.DECOMP_FIX["F12"]
F13 = config.DECOMP_FIX["F13"]


class NotPorted(NotImplementedError):
    pass


def not_ported(where):
    raise NotPorted(where + " is not ported yet (later phase)")


class ag(AgFields, Canvas):

    def __init__(self, paramMain):  # ag.java:560-564
        Canvas.__init__(self)
        ag.bs = paramMain
        self.gj = False  # public boolean gj = false;  ag.java:552 (instance field)
        self.setFullScreenMode(True)
        self.r_v()

    @staticmethod
    def q_v():  # ag.java:566-576
        ag.cg = 1
        ag.ch = -999
        ag.ck = 1
        ag.cq = 0
        ag.cs[4] = -1
        ag.cs[3] = -1
        ag.cs[2] = -1
        ag.cs[1] = -1
        ag.cs[0] = -1

    def r_v(self):  # ag.java:578-583
        ag.bJ = self.getWidth()
        ag.bK = self.getHeight()
        ag.bL = ag.bJ // 2
        ag.bM = ag.bK // 2

    def s_v(self):  # ag.java:585-658
        from pow.game.e import e
        from pow.game.k import k
        from pow.game.c import c
        from pow.game.as_ import as_
        from pow.game.m import m
        from pow.game.ar import ar
        from pow.midp.jrandom import Random
        self.r_v()
        ag.bu = g("/0_font.png", 8, 17, 9, 16777215)
        ag.bv = g("/0_font.png", 8, 17, 9, 0)
        ag.bw = g("/0_font.png", 8, 17, 9, 16400640)
        ag.bx = g("/0_font.png", 8, 17, 9, 6579300)
        ag.bA = al("/imgui.scr")
        ag.bE = al("/edat.scr")
        ag.bF = al("/mdat_QVGA.scr")
        ag.bB = al("/imgchar.scr")
        ag.bC = al("/imgeff.scr")
        ag.bD = al("/imgtile.scr")
        ag.bG = al("/gamestr.scr")
        ag.q_v()
        ag.bh = ag.bs.getAppProperty("MIDlet-Version") or ""
        ag.bk = ag.bs.getAppProperty("GAMEVIL_SERVER") or "ur.gamevil.net"
        try:
            ag.bl = int(ag.bs.getAppProperty("GAMEVIL_PORT"))
        except Exception:
            ag.bl = 28230
        ag.bm = ag.bs.getAppProperty("GAMEVIL_MOREGAMES") or "http://usaapp1.gamevil.net/moregames/index2.php?bid=POW_"
        ag.bn = ag.bs.getAppProperty("GAMEVIL_MULTIPLAY") or "http://ur.gamevil.net/moregames/pow_multiplayer.php"
        ag.bi = ag.bs.getAppProperty("GAMEVIL_CHEAT") == "TRUE"
        ag.bj = False
        ag.bZ.a = i16(ag.bJ)
        ag.bZ.b = i16(ag.bK)
        ag.bY.a = i16(ag.bJ)
        ag.bY.b = i16(ag.bK)
        ag.db = 0
        ag.dc = 0
        ag.dd = ag.bY.a >> 1
        ag.de = ag.bY.b >> 1
        if ag.bK % 2 == 1:
            ag.de += 1
        ag.x_v()
        ag.bV = 0
        ag.ck = 1
        ag.dr = 0
        ag.G_v()
        ag.cz.a_v()
        ag.by = Random()
        ag.bU = self.d_T("softbg")
        ag.bg = k(ag.bs)
        ag.be = as_()
        as_.a = m()
        ag.bb = e()
        ag.bc = ar()               # ar.java: the map (phase 3); the combat parts raise NotPorted
        ag.bd = c()                # c.java: story player, map; the combat parts raise NotPorted

    def keyPressed(self, paramInt):  # ag.java:660-662
        self.t_I(paramInt)

    def t_v(self):  # ag.java:664-685
        if ag.ch == -999:
            return
        if ag.bS:
            if ag.ch == -5 or ag.ch == 53:
                self.a_Z(False)
            ag.ch = -999
            return
        if ag.bV == 0:
            if ag.bf is not None:
                ag.bf.b_v()
                return
        elif ag.bV == 11:
            from pow.game.as_ import as_
            if not as_.gu:
                ag.be.t_I(ag.ch)

    @staticmethod
    def b_T(paramString):  # ag.java:687-689
        print(" " + paramString)

    def paint(self, paramGraphics):  # ag.java:691-706  (synchronized)
        ag.gg = False
        ag.br = paramGraphics
        x.a_G(paramGraphics)
        if ag.bS:
            x.b_IIIII(0, 0, ag.bJ, ag.bK, 0)
            ag.cS.b_I(10)
            x.a_Lg(ag.bu)
            j_ = ag.de - 5 - 10
            x.a_TIII("RESUME", ag.bL, j_ + ag.dc + 7, 1)
            ag.gg = True
            return
        self.P_v()
        ag.gg = True

    async def run(self):  # ag.java:708-760  (Thread.run -> async loop for pygbag)
        self.s_v()
        ag.gi = system.currentTimeMillis()
        while ag.gh and not self.quit_requested:
            try:
                ag.gi = system.currentTimeMillis()
                if ag.bS:
                    self.t_v()
                    self.repaint(0, 0, ag.bJ, ag.bK)
                    self.serviceRepaints()
                    ag.ch = -999
                    if ag.bQ:
                        self.b_Z(ag.bR)
                        ag.bQ = False
                    await self.sleep_ms(100)
                    continue
                if ag.bX != ag.bV:
                    ag.ch = -999
                else:
                    ag.ch = ag.ci
                ag.ci = -999
                ag.bN = i32(ag.bN + 1)
                if ag.bN < 0:
                    ag.bN = 0
                if AgFields.a > 0:   # private static int a  (ag.java:98)
                    AgFields.a -= 1
                self.t_v()
                if ag.bg is not None:
                    ag.bg.a_v()
                self.u_v()
                ag.be.i_v()
                ag.ch = -999
                if ag.bQ:
                    self.b_Z(ag.bR)
                    ag.bQ = False
                l1 = system.currentTimeMillis()
                j_ = (ae.aQ[ag.dh] if ag.bV == 3 else ae.aQ[2]) - int(l1 - ag.gi)
                if j_ > 20:
                    await self.sleep_ms(j_)
                else:
                    await self.sleep_ms(20)
                if ag.bN > 2:
                    ag.bq = True
                ag.bX = ag.bV
            except NotPorted as np_:
                # Spike convenience: a screen of a later phase shows a popup and returns
                # to the menu instead of killing the game (config.STRICT = re-raise).
                if config.STRICT:
                    raise
                print("NotPorted:", np_)
                if ag.bV in (3, 4, 5):
                    # the map / combat states have no screen yet: back to the Game Menu the
                    # way the game itself returns there (e.java:1288-1300)
                    self.w_I(2)
                    self.F_v()
                    ag.cM[0] = 0
                    ag.cN = ae.v[0]
                    ag.dE = ag.fU
                    ag.bV = 2
                    ag.cL = 0
                    ag.cK = 0
                    ag.ck = 1
                elif ag.bV == 2:
                    ag.cM[0] = ag.cO if ag.cM[0] not in (0, 5) else ag.cM[0]
                    ag.ap()
                ag.cS.a_T("3Not ported yet|(later phase)")
                await self.sleep_ms(20)
            except Exception as exception:
                ag.b_T("--run:" + repr(exception))
                if config.DEBUG:
                    traceback.print_exc()
                    raise
                await self.sleep_ms(20)

    def u_v(self):  # ag.java:762-767
        self.repaint()
        self.serviceRepaints()
        while not ag.gg:
            ag.f_I(20)

    @staticmethod
    def f_I(paramInt):  # ag.java:769-777
        system.sleep(paramInt)

    def hideNotify(self):  # ag.java:779-781
        self.a_Z(True)

    def showNotify(self):  # ag.java:783-785
        self.a_Z(True)

    def a_Z(self, paramBoolean):  # ag.java:787-799
        from pow.game.Main import Main
        if paramBoolean and ag.bV == 3:
            self.gj = True
        elif not paramBoolean:
            self.gj = False
        if ag.bS == paramBoolean or AgFields.b or AgFields.a > 0:
            return
        if not Main.c or not ag.bq:
            return
        ag.bQ = True
        ag.bR = paramBoolean

    def b_Z(self, paramBoolean):  # ag.java:801-818
        from pow.game.k import k
        ag.bS = paramBoolean
        if ag.bS:
            ag.ch = -999
            if ag.bg is not None:
                k.a.c_v()
                return
        else:
            ag.f_I(300)
            ag.ck = 1
            if ag.be is not None:
                from pow.game.as_ import as_
                as_.aJ()
            k.a.d_v()
            if ag.bV == 2 and ag.cM[0] == 4:
                ag.ck = 2

    @staticmethod
    def v_v():  # ag.java:820-822
        AgFields.b = True

    @staticmethod
    def w_v():  # ag.java:824-827
        AgFields.b = False
        AgFields.a = 3

    @staticmethod
    def x_v():  # ag.java:829-865
        for b in range(2):
            ag.er[b] = None
        for b in range(9):
            ag.et[b] = None
        for b in range(len(ag.ct)):
            ag.ct[b] = None
        ag.eT[1] = None
        ag.eT[0] = None
        ag.eS[1] = None
        ag.eS[0] = None
        ag.eU = None
        ag.eR = None
        ag.eV = None
        ag.eW = None
        ag.eY = None
        ag.fb = None
        ag.fe = None
        ag.cE.a = None
        ag.dU.g = None
        ag.dU.h = None
        ag.cz.aC = ag.cz.aE = None
        ag.cz.aG = None
        ag.cz.aH = None
        ag.cU = ag.cW = ag.cV = None
        ag.ep = 0
        ag.cS.b = 0
        ag.dh = 2
        for b in range(30):
            ag.cP[b] = 0
            ag.cQ[b] = 0
        ag.cX = ai()
        ag.cY = t()
        ag.cZ = ao()

    @staticmethod
    def a_IIT(paramInt1, paramInt2, paramString):  # ag.java:1144-1147
        if paramString is not None:
            x.a_TIII(paramString, paramInt1, paramInt2, 0)

    @staticmethod
    def b_IIT(paramInt1, paramInt2, paramString):  # ag.java:1149-1152
        if paramString is not None:
            x.a_TIII(paramString, paramInt1, paramInt2, 1)

    def E_v(self):  # ag.java:1154-1163  (title picture = title_1..4 stacked)
        if ag.ct[30] is None:
            ag.ct[30] = Image.createImage(240, 320)
            graphics = ag.ct[30].getGraphics()
            for b in range(4):
                image = self.d_T("title_" + str(b + 1))
                graphics.drawImage(image, 0, 80 * b, 20)

    def F_v(self):  # ag.java:1165-1172
        ag.cy = 0
        while ag.cy < 4:
            ag.ct[26 + ag.cy] = self.d_T(ag.bA.a_I(73 + ag.cy))
            ag.cy += 1
        self.ad_v()

    @staticmethod
    def G_v():  # ag.java:1174-1186
        arrayOfByte = bytearray(2)
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_env", False)
            if recordStore is None or recordStore.getNumRecords() < 1:
                return
            arrayOfByte = recordStore.getRecord(1)
            ag.cG = len(arrayOfByte)
        except Exception:
            pass
        if ag.cG >= 2:
            ag.dg = i8(arrayOfByte[0])
            ag.dh = i8(arrayOfByte[1])

    @staticmethod
    def H_v():  # ag.java:1188-1201
        arrayOfByte = bytearray(2)
        arrayOfByte[0] = ag.dg & 0xFF
        arrayOfByte[1] = ag.dh & 0xFF
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_env", True)
            if recordStore.getNumRecords() == 0:
                recordStore.addRecord(arrayOfByte, 0, len(arrayOfByte))
            recordStore.setRecord(1, arrayOfByte, 0, len(arrayOfByte))
        except Exception:
            return

    @staticmethod
    def I_v():  # ag.java:1203-1210
        if ag.cM[1] < ag.cM[2]:
            ag.cM[2] = ag.cM[1]
            return
        if ag.cM[1] > ag.cM[2] + 4:
            ag.cM[2] = ag.cM[1] - 4

    def a_MIIIIII(self, paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # ag.java:1212-1214
        ag.a_IIIIMII(paramInt1, paramInt2, paramInt3, paramInt4, paramImage, paramInt5, paramInt6)

    @staticmethod
    def b_TI(paramString, paramInt):  # ag.java:1216-1240  (field #paramInt of "a|b|c")
        if paramString is None:
            return None
        bool_ = False
        j_ = 0
        b1 = 0
        b2 = 0
        paramString = paramString + "|"
        for b3 in range(len(paramString)):
            if paramString[b3] == '|':
                b2 += 1
            if not bool_ and b2 == paramInt:
                if b2 == 0:
                    j_ = b3
                else:
                    j_ = b3 + 1
                bool_ = True
            elif bool_ and b2 == paramInt + 1:
                b1 = b3
                break
        return paramString[j_:b1]

    @staticmethod
    def c_IIT(paramInt1, paramInt2, paramString):  # ag.java:1242-1244
        x.a_TIII(paramString, paramInt1, paramInt2, 0)

    @staticmethod
    def a_BB(paramByte1, paramByte2):  # ag.java:1275-1277
        return i16(paramByte1 & 0xFF | (paramByte2 & 0xFF) << 8)

    def K_v(self):  # ag.java:1418-1431
        if ag.cl == 0:
            self.c_III(0, 0, 0)
            self.a_MIIIIII(ag.ct[7], ag.db, ag.dc, ag.bY.a, ag.bY.b, ag.cc.a, ag.cc.b)
            return
        if ag.cl == 1:
            self.c_III(0, 0, 0)
            return
        if ag.cl == 2:
            self.c_III(255, 255, 255)

    def c_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:1433-1435
        x.b_IIIII(ag.db, ag.dc, ag.bY.a, ag.bY.b, ag.k_III(paramInt1, paramInt2, paramInt3))

    def L_v(self):  # ag.java:1522-1610
        # DECOMP-FIX F8: the decompiled switch at ag.java:1526-1546 has no `break`s, so every case
        # would fall through into the next (bV==0 would also run bb.a(1), bc.b(1), ...).
        # The original had one branch per state.
        if ag.ck == 1:
            ag.ck = 0
            v = ag.bV
            if v == 12:
                self.at()
            elif v == 0:
                ag.Q_v()
            elif v == 2:
                ag.bb.a_I(1)
            elif v == 3:
                ag.bc.b_I(1)
            elif v == 4:
                ag.bc.k_v()
            elif v == 5:
                self.K_v()
                for b in range(81):
                    ag.eE[b // 9][b % 9] = 1
                ag.bd.c_v()
                ag.bb.h_v()
            elif v in (6, 8, 9):
                return
            elif v == 10:
                if (ag.ec == 0 and ag.fD < ag.eb[1] - ag.eb[0]) or (ag.ec != 0 and ag.fD >= ag.eb[1] - ag.eb[0]):
                    from pow.game.e import e
                    ag.bb.e_v()
                    x.a_Lg(ag.bu)
                    if ag.ec != 0:
                        self.b_TII("Prologue", 2 - ag.dc, 9)
                    else:
                        self.b_TII("Epilogue", 2 - ag.dc, 9)
                    ag.bb.b_I(ag.fE)
                    if ag.fA[0] > 0:
                        e.a_III(0, 0, 1)
                    if ag.fA[1] > 0:
                        e.a_III(1, 0, 1)
                    self.q_I(1)
                else:
                    self.N_v()
                if ag.cS.b != 0:
                    ag.cS.c_v()
            return
        if ag.ck == 2:
            if ag.bV == 2:
                ag.bb.a_I(2)
                return
            return
        v = ag.bV
        if v == 0:
            ag.Q_v()
            return
        if v == 2:
            ag.bb.a_I(0)
            return
        if v == 3:
            ag.bc.b_I(0)
            return
        if v == 4:
            ag.bc.k_v()
            ag.bc.n_v()
            return
        if v == 5:
            ag.bb.i_v()
            return
        if v in (6, 8, 9):
            return
        if v == 10:
            if ag.cS.b != 0:
                if ag.cS.j != 0:
                    ag.cS.c_v()
                    return
            self.M_v()

    def a__I(self, paramInt):  # ag.java:1882-1885
        if ag.bg is not None:
            ag.bg.a__I(paramInt)

    def P_v(self):  # ag.java:1887-1933
        from pow.game.k import k
        v = ag.bV
        if v == 12:
            self.L_v()
            if system.currentTimeMillis() - ag.c > 3000:
                ag.bs.destroyApp(True)
                ag.bs.notifyDestroyed()
            return
        if v == 0:
            self.L_v()
        elif v == 2:
            if ag.bg is not None and ag.cM[0] < 29 and k.a_ != ae.A[ag.cM[0]] and ag.cM[0] != 20 and not ag.bp:
                self.a__I(ae.A[ag.cM[0]])
            if ag.cS.b != 0:
                ag.cS.b_v()
            else:
                ag.bb.a_v()
            self.L_v()
        elif v == 3:
            ag.bc.a_v()
        elif v in (4, 5):
            self.L_v()
            ag.bc.O_I(0)
        elif v == 10:
            if ag.cS.b != 0:
                ag.cS.b_v()
            self.L_v()
        elif v == 11:
            if ag.be is not None:
                from pow.game.as_ import as_
                as_.aK()
        if ag.be is not None:
            from pow.game.as_ import as_
            if as_.gu:
                ag.be.j_v()
        ag.cj = -999

    @staticmethod
    def Q_v():  # ag.java:1935-1939
        from pow.game.af import af
        if ag.bf is None:
            ag.bf = af()
        ag.bf.a_v()

    def t_I(self, paramInt):  # ag.java:1941-1961
        if paramInt == -10:
            return
        if ag.bS:
            ag.ch = paramInt
            return
        ag.ci = paramInt
        if paramInt in (-4, -3, -2, -1, 50, 52, 54, 56):
            ag.cj = paramInt

    def d_T(self, paramString):  # ag.java:1963-1975
        ag.R_v()
        str_ = "/" + paramString + ".png"
        image = None
        try:
            image = Image.createImage(str_)
        except Exception:
            print("======== createMixImage failuer :" + paramString)
            return None
        ag.R_v()
        return image

    @staticmethod
    def R_v():  # ag.java:1977-1979  (System.gc)
        pass

    @staticmethod
    def u_I(paramInt):  # ag.java:1981-1983
        x.b_IIIII(0, 0, ag.bJ, ag.bK, paramInt)

    def S_v(self):  # ag.java:1985-1996  (title screen)
        if ag.ct[30] is None:
            return
        ag.a_IIIIMII(0, 0, ag.bZ.a, ag.bZ.b, ag.ct[30], 0, 0)
        if ag.cv is None:
            ag.cv = self.d_T(ag.bA.a_I(36))
        ag.a_IIIIMII(ag.dd - 66 + ag.db, ag.bZ.b - 20, 132, 14, ag.cv, 0, 0)
        if ag.cw is None:
            ag.cw = self.d_T(ag.bA.a_I(42))
        if ag.bN % 6 < 3 and ag.bV == 0:
            ag.a_IIIIMII(ag.dd - 55 + ag.db, ag.bZ.b - 60, 110, 14, ag.cw, 0, 0)

    def a_TIIIIII(self, paramString, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # ag.java:1998-2002
        image = self.d_T(paramString)
        if image is not None:
            ag.a_IIIIMII(paramInt1, paramInt2, paramInt3, paramInt4, image, paramInt5, paramInt6)

    def T_v(self):  # ag.java:2004-2124  (title -> Main Menu)
        cz = ag.cz
        for b in range(8):
            q = ae.aT[b]
            cz.ac[b] = ae.B[q]
            cz.ad[b] = ae.C[q]
            cz.ak[b] = ae.D[q]
            cz.al[b] = ae.E[q]
            cz.ae[b] = ae.F[q]
            cz.af[b] = ae.G[q]
            cz.ag[b] = ae.H[q]
            cz.ah[b] = ae.I[q]
            cz.ai[b] = ae.J[q]
            cz.aj[b] = ae.K[q]
            cz.am[b] = ae.L
            cz.aA[b] = ae.M[q]
            cz.an[b] = ae.N[q]
            cz.ao[b] = ae.O[q]
            cz.ap[b] = ae.P[q]
            cz.aq[b] = ae.Q
            cz.ar[b] = ae.R[q]
            cz.as_[b] = ae.S[q]
            cz.at[b] = ae.T[q]
            cz.au[b] = ae.U
            cz.av[b] = ae.V[q]
            cz.aw[b] = ae.W[q]
            cz.ax[b] = ae.X
            cz.ay[b] = ae.Y
            cz.az[b] = ae.Z
            ag.eF[b][0] = ae.aa[q]
            ag.eF[b][1] = ae.ab[q]
            ag.eF[b][2] = ae.ac[q]
            ag.eF[b][3] = ae.ad[q]
            ag.eI[b] = ag.eF[b]
            ag.eG[b][0] = ae.ae[q]
            ag.eG[b][1] = ae.af[q]
            ag.eG[b][2] = ae.ag[q]
            ag.eG[b][3] = ae.ah[q]
            ag.eJ[b] = ag.eG[b]
            ag.eH[b][0] = ae.aa[q]
            ag.eH[b][1] = ae.ai[q]
            ag.eH[b][2] = ae.aj[q]
            ag.eH[b][3] = ae.ak
            ag.eH[b][4] = ae.ai[q]
            ag.eH[b][5] = ae.ai[q]
            ag.eH[b][6] = ae.N[q]
            ag.eH[b][7] = ae.O[q]
            ag.eH[b][8] = ae.P[q]
            ag.eH[b][9] = ae.Q
            ag.eH[b][10] = ae.Q
            ag.eH[b][11] = ae.Q
            ag.eH[b][12] = ae.Q
            ag.eH[b][13] = ae.Q
            ag.eH[b][14] = ae.R[q]
            ag.eH[b][15] = ae.S[q]
            ag.eH[b][16] = ae.T[q]
            ag.eH[b][17] = ae.U
            ag.eH[b][18] = ae.U
            ag.eH[b][19] = ae.V[q]
            ag.eH[b][20] = ae.W[q]
            ag.eH[b][21] = ae.W[q]
            ag.eK[b] = ag.eH[b]
        ag.eL[0] = ag.eI
        ag.eL[1] = ag.eJ
        ag.eL[2] = ag.eI
        ag.eL[3] = ag.eK
        ab = cz.ab
        (ab[0], ab[1], ab[2], ab[3], ab[4], ab[5], ab[6], ab[7], ab[8], ab[9]) = (
            cz.ac, cz.ad, cz.ak, cz.ae, cz.af, cz.ag, cz.ah, cz.ai, cz.aj, cz.al)
        (ab[10], ab[11], ab[12], ab[13], ab[14]) = (cz.am, cz.aA, cz.an, cz.ao, cz.ap)
        (ab[15], ab[16], ab[17], ab[18], ab[19]) = (cz.aq, cz.aq, cz.aq, cz.aq, cz.aq)
        (ab[20], ab[21], ab[22], ab[23], ab[24]) = (cz.ar, cz.as_, cz.at, cz.au, cz.au)
        (ab[25], ab[26], ab[27], ab[28], ab[29], ab[30]) = (cz.av, cz.aw, cz.aw, cz.ax, cz.ay, cz.az)
        ag.bY.a = 240
        ag.bY.b = 243
        ag.cb.a = i16(ag.bY.a // 27 + (1 if ag.bY.a % 27 > 0 else 0))
        ag.cb.a = i16(ag.cb.a + (0 if (ag.cb.a & 0x1) > 0 else 1))
        ag.cb.b = i16(ag.bY.b // 27 + (1 if ag.bY.b % 27 > 0 else 0))
        ag.cb.b = i16(ag.cb.b + (0 if (ag.cb.b & 0x1) > 0 else 1))
        ag.cc.a = i16(ag.cb.a * 27 - ag.bY.a >> 1)
        ag.cc.b = i16(ag.cb.b * 27 - ag.bY.b >> 1)
        ag.bY.a = ag.bZ.a
        ag.bY.b = ag.bZ.b
        ag.db = 0
        ag.dc = 0
        self.aa_v()
        ag.q_v()
        self.a__I(-1)
        ag.dj = 0
        self.w_I(0)
        ag.cM[0] = 5
        ag.cN = 10
        ag.cS.e = 0
        self.U_v()
        ag.bV = 2
        if not ag.aq():
            ag.cM[1] = 1

    def U_v(self):  # ag.java:2126-2214  (load save "gamevil_pow_data")
        cz = ag.cz
        ag.cG = 0
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_data", False)
            if recordStore is None or recordStore.getNumRecords() < 1:
                return
            ag.cF = recordStore.getRecord(1)
            ag.cG = ag.cF[0] & 0xFF | ag.cF[1] << 8 & 0xFF00
        except Exception:
            pass
        if ag.cG != 0:
            cF = ag.cF
            arrayOfByte1 = [0] * 16
            b2 = 0
            while b2 < 8 and cF[2 + b2] != 32:
                b2 += 1
            arrayOfByte2 = bytearray(b2)
            for b1 in range(b2):
                arrayOfByte2[b1] = cF[2 + b1]
            cz.k = ag.a_ABII(arrayOfByte2, 0, b2)
            ag.dj = i8(cF[18])
            ag.cG = 19
            ag.dk = ag.Y_v()
            ag.dm = ag.Y_v()
            ag.do = ag.Y_v()
            ag.dw = ag.V_v()
            ag.dx = ag.V_v()
            for b1 in range(8):
                ag.dy[b1] = ag.W_v()
            ag.dY = ag.W_v()
            ag.ed = ag.W_v()
            for b1 in range(44):
                ag.fn[0][b1] = ag.Y_v()
                ag.fn[1][b1] = ag.Y_v()
            ag.fo = ag.Y_v()
            for b1 in range(25):
                ag.fL[b1] = self.Z_v()
            ag.cq = ag.Y_v()
            cz.a[0].a = ag.X_v()
            cz.a[0].b = ag.X_v()
            # Java int division (values are positions >= 0, so // == /)
            cz.a[0].a = i16((cz.a[0].a // 27 // 7 * 7 + 4) * 27 + 8)
            cz.a[0].b = i16((cz.a[0].b // 27 // 7 * 7 + 4) * 27 + 8)
            for b1 in range(22):
                cz.g[b1] = ag.Y_v()
            cz.h = ag.Y_v()
            cz.i = ag.Y_v()
            cz.l = ag.Y_v()
            if config.ORIG_BUG["B2"]:
                # ORIG-BUG B2: the level is one byte in the save (G(cz.l), ag.java:2908) read back
                # signed, so Lv128+ loaded as -128..; the rest of the game keeps it as an int
                cz.l &= 0xFF
            cz.m = ag.X_v()
            cz.n = ag.X_v()
            cz.o = ag.X_v()
            cz.p = ag.X_v()
            cz.q = ag.X_v()
            cz.r = ag.X_v()
            cz.E = ag.W_v()
            if ag.bi:
                cz.E = 555000
            if config.GOLD is not None:   # PORT-EXTRA config.GOLD (POW_GOLD=N)
                cz.E = i32(config.GOLD)
            cz.F = ag.W_v()
            cz.G = ag.W_v()
            cz.H = ag.X_v()
            cz.J = ag.X_v()
            cz.S = ag.Y_v()
            for b1 in range(5):
                cz.V[b1] = ag.Y_v()
            for b1 in range(19):
                cz.W[b1] = ag.Y_v()
            for b1 in range(9):
                cz.X[b1] = self.Z_v()
            for b1 in range(25):
                cz.Y[b1] = self.Z_v()
            for b1 in range(5):
                cz.Z[b1].a = ag.X_v()
                cz.Z[b1].b = ag.Y_v()
            cz.aa[0] = ag.Y_v()
            cz.aa[1] = ag.Y_v()
            cz.aB = ag.Y_v()
            if not 0 <= cz.aB < heroes.HERO_COUNT:   # PORT-EXTRA: 10 heroes, a broken byte -> hero 1
                cz.aB = 0
            ag.dV = ag.W_v()
            ag.eo = ag.W_v()
            ag.fR = ag.Y_v()
            ag.fS = ag.Y_v()
            ag.dH = ag.Y_v()
            ag.ep = ag.Y_v()
            for b1 in range(16):
                arrayOfByte1[b1] = ag.Y_v()
            ag.fq = ag.W_v()
            for b1 in range(4):
                ag.W_v()
        self.ag()

    @staticmethod
    def V_v():  # ag.java:2216-2230  (u64 LE; bytes 4..7 are sign-extended then masked)
        cF, cG = ag.cF, ag.cG
        l1 = 0
        for k_ in range(8):
            l1 |= (cF[cG + k_] & 0xFF) << (8 * k_)
        ag.cG += 8
        return l1 - (1 << 64) if l1 & (1 << 63) else l1

    @staticmethod
    def W_v():  # ag.java:2232-2237
        cF, cG = ag.cF, ag.cG
        j_ = cF[cG] & 0xFF | cF[cG + 1] << 8 & 0xFF00 | cF[cG + 2] << 16 & 0xFF0000 | cF[cG + 3] << 24 & 0xFF000000
        ag.cG += 4
        return i32(j_)

    @staticmethod
    def X_v():  # ag.java:2239-2244
        s = i16(ag.cF[ag.cG] & 0xFF | ag.cF[ag.cG + 1] << 8 & 0xFF00)
        ag.cG += 2
        return s

    @staticmethod
    def Y_v():  # ag.java:2246-2250
        b = i8(ag.cF[ag.cG] & 0xFF)
        ag.cG += 1
        return b

    def Z_v(self):  # ag.java:2252-2261
        z1 = z()
        z1.a = ag.X_v()
        z1.b = ag.X_v()
        z1.c = ag.X_v()
        z1.d = ag.X_v()
        z1.e = ag.X_v()
        z1.f = ag.Y_v()
        return z1

    def aa_v(self):  # ag.java:2263-2269
        ag.ct[34] = self.d_T(ag.bA.a_I(22))
        ag.ct[19] = self.d_T(ag.bA.a_I(24))
        ag.ct[20] = self.d_T(ag.bA.a_I(25))
        ag.ct[0] = self.d_T(ag.bA.a_I(48))
        ag.ct[32] = self.d_T(ag.bA.a_I(37))

    @staticmethod
    def v_I(paramInt):  # ag.java:2283-2285
        return j.a("/" + ag.bE.a_I(paramInt))

    def w_I(self, paramInt):  # ag.java:2287-2304
        self.ah()
        self.ae_v()
        if ag.ct[7] is None:
            ag.ct[7] = Image.createImage(ag.bZ.a, ag.bZ.b)
        ag.cu = ag.ct[7].getGraphics()
        ag.dj = 0
        ag.cM[2] = 0
        ag.cM[1] = 0
        ag.cS.b = 0
        ag.cU = ag.v_I(47)
        ag.cW = ag.v_I(49)
        ag.cV = ag.v_I(51)
        ag.af_v()
        ag.ct[17] = self.d_T(ag.bA.a_I(27))
        self.x_I(paramInt)
        self.ag()

    def ad_v(self):  # ag.java:2306-2311
        ag.ct[1] = self.d_T(ag.bA.a_I(21))
        ag.ct[2] = self.d_T(ag.bA.a_I(46))
        ag.ct[3] = self.d_T(ag.bA.a_I(43))
        ag.fN = self.d_T(ag.bA.a_I(38))

    def ae_v(self):  # ag.java:2313-2319
        ag.ct[1] = None
        ag.ct[2] = None
        ag.ct[3] = None
        ag.fN = None
        ag.R_v()

    @staticmethod
    def af_v():  # ag.java:2321-2343  (menu captions from uimenu.scr = edat[69])
        al1 = al("/" + ag.bE.a_I(69))
        for b in range(30):
            ag.fT[b] = al1.a_I(b)
            if b < 7:
                ag.gd[b] = al1.a_I(b + 48)
            if b < 6:
                ag.fV[b] = al1.a_I(b + 30)
            if b < 5:
                ag.ge[b] = al1.a_I(b + 55)
            if b < 4:
                ag.gb[b] = al1.a_I(b + 42)
            if b < 2:
                ag.gc[b] = al1.a_I(b + 46)
        ag.fU[0] = al1.a_I(36)
        ag.fW[0] = al1.a_I(37)
        ag.ga[0] = al1.a_I(38)
        ag.fX[0] = al1.a_I(39)
        ag.fY[0] = al1.a_I(40)
        ag.fZ[0] = al1.a_I(41)
        al1.a_v()

    def x_I(self, paramInt):  # ag.java:2345-2370  (menu background into ct[7])
        if paramInt == 1:
            return
        x.a_G(ag.cu)
        ag.ct[11] = self.d_T(ag.bA.a_I(60))
        ag.ct[12] = self.d_T(ag.bA.a_I(61))
        ag.ct[16] = self.d_T(ag.bA.a_I(63))
        ag.ct[9] = self.d_T(ag.bA.a_I(59))
        j_ = ag.ct[9].getWidth()
        m = ag.ct[9].getHeight()
        b = 0
        while b * m < ag.bZ.b + m:
            for b1 in range(4):
                ag.c_MIIIIII(ag.ct[9], 0, 0, (b & 0x1) * -31 + b1 * j_, b * m, j_, m)
            b += 1
        # Java: (W - w) * b / 2 and H / 2 * b % 2 - all operands >= 0, so // matches Java /
        for b in range(4):
            ag.c_MIIIIII(ag.ct[12], 0, 0, (ag.bZ.a - ag.ct[12].getWidth()) * b // 2, ag.bZ.b // 2 * b % 2,
                         ag.ct[12].getWidth(), ag.ct[12].getHeight())
        for b in range(4):
            ag.c_MIIIIII(ag.ct[11], 0, 0, ag.bZ.a // 2 * b % 2, (ag.bZ.b - ag.ct[11].getHeight()) * b // 2,
                         ag.ct[11].getWidth(), ag.ct[11].getHeight())
        ag.c_MIIIIII(ag.ct[16], 0, 0, (ag.bZ.a >> 1) - ag.ct[16].getWidth() // 2, 0,
                     ag.ct[16].getWidth(), ag.ct[16].getHeight())
        ag.ct[11] = None
        ag.ct[12] = None
        ag.ct[16] = None
        ag.ct[9] = None
        x.a_G(ag.br)

    def ag(self):  # ag.java:2372-2382  (compact inventory cz.Y)
        for b in range(24):
            if ag.cz.Y[b].a == 0:
                for j_ in range(b + 1, 25):
                    if ag.cz.Y[j_].a != 0:
                        self.a_LzLz(ag.cz.Y[b], ag.cz.Y[j_])
                        break

    def a_LzLz(self, paramz1, paramz2):  # ag.java:2384-2389
        z1 = z()
        ag.b_LzLz(z1, paramz1)
        ag.b_LzLz(paramz1, paramz2)
        ag.b_LzLz(paramz2, z1)

    @staticmethod
    def b_LzLz(paramz1, paramz2):  # ag.java:2391-2398
        paramz1.a = paramz2.a
        paramz1.b = paramz2.b
        paramz1.c = paramz2.c
        paramz1.d = paramz2.d
        paramz1.e = paramz2.e
        paramz1.f = paramz2.f

    def ah(self):  # ag.java:2400-2436
        ag.eS[0] = None
        ag.eS[1] = None
        ag.cz.aD = None
        ag.cz.aF = None
        ag.eT[0] = None
        ag.eT[1] = None
        ag.ct[40] = None
        ag.ct[41] = None
        if ag.bT is not None:
            for b1 in range(len(ag.bT)):
                ag.bT[b1] = None
            ag.bT = None
        ag.eU = None
        ag.ct[42] = None
        ag.eV = None
        ag.ct[43] = None
        ag.eR = None
        ag.eQ = None
        ag.eW = None
        ag.ct[44] = None
        ag.ct[31] = None
        ag.fe = None
        ag.eY = None
        ag.er[1] = None
        for b in range(2):
            ag.es[b] = None
        for b in range(9):
            ag.et[b] = None
        ag.eq = None
        ag.bY.a = ag.bZ.a
        ag.bY.b = ag.bZ.b
        ag.db = 0
        ag.dc = 0

    @staticmethod
    def a_IIIIMII(paramInt1, paramInt2, paramInt3, paramInt4, paramImage, paramInt5, paramInt6):  # ag.java:2438-2440
        x.a_MIIIIII(paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6)

    def b_MIIIIII(self, paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # ag.java:2442-2457
        i1 = paramInt2
        if i1 > 0:
            i1 = 0
        i2 = ag.bY.b - paramInt2 - paramInt4
        if i2 > 0:
            i2 = 0
        j_ = paramInt1
        if j_ > 0:
            j_ = 0
        m = ag.bY.a - paramInt1 - paramInt3
        if m > 0:
            m = 0
        if paramInt4 + i1 + i2 > 0 and paramInt3 + j_ + m > 0:
            ag.a_IIIIMII(paramInt1 + ag.db - j_, paramInt2 - i1 + ag.dc, paramInt3 + j_ + m, paramInt4 + i1 + i2,
                         paramImage, paramInt5 - j_, paramInt6 - i1)

    @staticmethod
    def c_MIIIIII(paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # ag.java:2459-2461
        x.a_MIIIIII(paramImage, paramInt3, paramInt4, paramInt5, paramInt6, paramInt1, paramInt2)

    @staticmethod
    def ai():  # ag.java:2463-2465
        from pow.game.k import k
        k.b_v()

    @staticmethod
    def aj():  # ag.java:2467-2472
        ag.cz.aC = None
        ag.cz.aE = None
        ag.cz.aG = None
        ag.cz.aH = None

    @staticmethod
    def ak():  # ag.java:2522-2546
        v = ag.cM[0]
        if v == 0:
            ag.dE = ag.fU
        elif v == 1:
            ag.cN = ag.dr
            ag.dE = ag.dt
        elif v == 2:
            ag.cN = ag.dv[ag.dk]
            ag.dE = ag.dA
        elif v == 7:
            ag.cz.k = None
        elif v == 10:
            ag.dE = ag.fW
        elif v == 13:
            ag.dE = ag.fY
            ag.ct[39] = None

    @staticmethod
    def ap():  # ag.java:2728-2733
        ag.cN = ae.v[ag.cM[0]]
        ag.cM[1] = ag.cP[ag.cM[0]]
        ag.cM[2] = ag.cQ[ag.cM[0]]
        ag.ck = 1

    @staticmethod
    def a_TII(paramString, paramInt1, paramInt2):  # ag.java:2743-2746  (centred text)
        paramInt1 += 2
        x.a_TIII(paramString, ag.dd + ag.db + paramInt2, paramInt1 + ag.dc, 1)

    def b_TII(self, paramString, paramInt1, paramInt2):  # ag.java:2748-2750
        ag.a_TII(paramString, paramInt1, 0)

    @staticmethod
    def c_TII(paramString, paramInt1, paramInt2):  # ag.java:2752-2754
        x.a_TIII(paramString, paramInt1 + ag.db, paramInt2 + ag.dc, 1)

    @staticmethod
    def d_TII(paramString, paramInt1, paramInt2):  # ag.java:2756-2758
        x.a_TIII(paramString, paramInt1 + ag.db, paramInt2 + ag.dc, 0)

    def a_IIIIZ(self, paramInt1, paramInt2, paramInt3, paramInt4, paramBoolean):  # ag.java:2760-2762
        ag.a_IIIIIIIZ(paramInt1, paramInt2, paramInt3, paramInt4, 0, 5263440, 16777215, paramBoolean)

    @staticmethod
    def a_IIIIIIIZ(paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7, paramBoolean):  # ag.java:2764-2791
        ac1 = ac(0, 0, 0, 0)
        if paramBoolean:
            ac1.a = paramInt1 - 2
            ac1.c = paramInt3 + 4
            ac1.b = paramInt2 - 1
            ac1.d = paramInt4 + 2
            x.a_IIIII(ac1.a, ac1.b, ac1.c, ac1.d, paramInt7)
            ac1.a += 1
            ac1.c -= 2
            ac1.b -= 1
            ac1.d += 2
            x.a_IIIII(ac1.a, ac1.b, ac1.c, ac1.d, paramInt7)
        ac1.a = paramInt1 - 1
        ac1.c = paramInt3 + 2
        ac1.b = paramInt2
        ac1.d = paramInt4
        x.a_IIIII(ac1.a, ac1.b, ac1.c, ac1.d, paramInt6)
        ac1.a += 1
        ac1.c -= 2
        ac1.b -= 1
        ac1.d += 2
        x.a_IIIII(ac1.a, ac1.b, ac1.c, ac1.d, paramInt6)
        ac1.b += 1
        ac1.d -= 2
        x.b_IIIII(ac1.a, ac1.b, ac1.c, ac1.d, paramInt5)

    @staticmethod
    def k_III(paramInt1, paramInt2, paramInt3):  # ag.java:2857-2860
        return (paramInt1 & 0xFF) << 16 | (paramInt2 & 0xFF) << 8 | paramInt3 & 0xFF

    @staticmethod
    def aq():  # ag.java:2862-2869  (is there a saved game?)
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_data", True)
            return not (recordStore.getNumRecords() == 0)
        except Exception:
            return False

    def as_(self):  # ag.java:3003-3009  (exit: show outro, quit after 3 s)
        ag.bV = 12
        ag.ck = 1
        ag.dr = 0
        ag.ai()
        ag.c = system.currentTimeMillis()

    def at(self):  # ag.java:3011-3019  (outro picture)
        if ag.bN == 2 or ag.bN == 5:
            ag.ai()
        ag.u_I(0)
        image = self.d_T(ag.bA.a_I(0))
        j_ = image.getWidth()
        ag.a_IIIIMII(ag.bL - j_ // 2, ag.bM - 10, j_, 20, image, 0, 0)
        ag.a_IIIIMII(ag.bL - j_ // 2, ag.bK - 24, j_, 22, image, 0, 20)

    @staticmethod
    def a_ABII(paramArrayOfbyte, paramInt1, paramInt2):  # ag.java:3026-3043  (readUTF of bytes[from:to])
        from pow.game.al import _read_utf
        j_ = paramInt1
        m = paramInt2
        str_ = None
        try:
            i1 = m - j_
            arrayOfByte = bytearray(i1 + 2)
            arrayOfByte[0] = i1 >> 8 & 0xFF
            arrayOfByte[1] = i1 & 0xFF
            arrayOfByte[2:] = paramArrayOfbyte[j_:j_ + i1]
            str_ = _read_utf(arrayOfByte)
        except Exception:
            pass
        return str_

    @staticmethod
    def h_II(paramInt1, paramInt2):  # ag.java:3045-3079  (soft-key captions)
        if ag.cS.b != 0:
            return
        j_ = ag.bU.getWidth()
        m = ag.bU.getHeight()
        str_ = ""
        if paramInt1 != -1:
            x.a_Lg(ag.bu)
            x.a_MII(ag.bU, 0, ag.bK - m)
            i1 = len(str_ + ae.t[paramInt1]) * 10
            i2 = i1 + 4 - ag.bU.getWidth()
            if i2 > 0:
                x.b_IIIII(j_ - 8, ag.bK - m + 2, 8, 13, 0)
                x.a_MII(ag.bU, i2, ag.bK - m)
                x.b_IIIII(i2, ag.bK - m + 2, 8, 13, 0)
                x.a_TIII(str_ + ae.t[paramInt1], (j_ + i2) // 2, ag.bK - m, 1)
            else:
                x.a_TIII(str_ + ae.t[paramInt1], j_ // 2, ag.bK - m, 1)
        if paramInt2 != -1:
            x.a_Lg(ag.bu)
            x.a_MII(ag.bU, ag.bJ - j_ - 0, ag.bK - m)
            i1 = len(str_ + ae.t[paramInt2]) * 10
            i2 = i1 + 15 - ag.bU.getWidth()
            if i2 > 0:
                x.b_IIIII(ag.bJ - j_ - 0, ag.bK - m + 2, 8, 13, 0)
                x.a_MII(ag.bU, ag.bJ - j_ - i2 - 0, ag.bK - m)
                x.b_IIIII(ag.bJ - i2 - 0 - 8, ag.bK - m + 2, 8, 13, 0)
                x.a_TIII(str_ + ae.t[paramInt2], ag.bJ - (j_ + i2) // 2 - 0, ag.bK - m, 1)
                return
            x.a_TIII(str_ + ae.t[paramInt2], ag.bJ - j_ // 2 - 0, ag.bK - m, 1)

    def l_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:3201-3203
        ag.bO = ag.k_III(paramInt1, paramInt2, paramInt3)

    @staticmethod
    def f_IIII(paramInt1, paramInt2, paramInt3, paramInt4):  # ag.java:3205-3207
        x.c_IIIII(paramInt1, paramInt2, paramInt3, paramInt4, ag.bO)

    def aA(self):  # ag.java:3459-3465
        ag.aj()
        # PORT-EXTRA heroes 4..9 (pow/game/heroes.py): g_head1..6 and their frame tables
        ag.cz.aG = self.d_T(ag.bB.a_I(heroes.head_image_index(ag.cz.aB)))
        ag.cz.aC = heroes.head_frames(self, ag.cz.aB, 0)
        ag.cz.aH = self.d_T(ag.bB.a_I(44))
        ag.cz.aE = self.K_I(45)

    def K_I(self, paramInt):  # ag.java:3467-3482  (frame table from mdat_QVGA)
        from pow.game.structs import y
        b1 = 1
        arrayOfByte = j.a("/" + ag.bF.a_I(paramInt))
        n = arrayOfByte[0] & 0xFF
        arrayOfY = [None] * n
        for b2 in range(n):
            arrayOfY[b2] = y()
            arrayOfY[b2].a = ag.a_BB(arrayOfByte[b1], arrayOfByte[b1 + 1])
            arrayOfY[b2].b = ag.a_BB(arrayOfByte[b1 + 2], arrayOfByte[b1 + 3])
            arrayOfY[b2].c = ag.a_BB(arrayOfByte[b1 + 4], arrayOfByte[b1 + 5])
            arrayOfY[b2].d = ag.a_BB(arrayOfByte[b1 + 6], arrayOfByte[b1 + 7])
            arrayOfY[b2].e = ag.a_BB(arrayOfByte[b1 + 8], arrayOfByte[b1 + 9])
            arrayOfY[b2].f = ag.a_BB(arrayOfByte[b1 + 10], arrayOfByte[b1 + 11])
            b1 += 12
        return arrayOfY

    @staticmethod
    def M_I(paramInt):  # ag.java:3538-3540
        return ag.bG.a_I(paramInt)

    @staticmethod
    def N_I(paramInt):  # ag.java:3549-3574  (key code '0'..'9' -> digit, else -1)
        if 48 <= paramInt <= 57:
            return paramInt - 48
        return -1

    @staticmethod
    def H_I(paramInt):  # ag.java:3081-3098  (add exp; returns the levels gained)
        arrayOfInt = [0] * 10
        b = 0
        paramInt += ag.cz.G
        while True:
            j = b % 10
            if j == 0:
                arrayOfInt = ag.bb.p_v()
            j = arrayOfInt[j]
            if paramInt < j:
                ag.cz.G = paramInt
                return b
            paramInt -= j
            ag.cz.l += 1
            ag.cz.J += 3
            b += 1

    @staticmethod
    def e_T(paramString):  # ag.java:3148-3153  (trim trailing spaces; sic: one char left -> "")
        m = len(paramString) - 1
        while m >= 0 and paramString[m] == ' ':
            m -= 1
        return "" if m == 0 else paramString[:m + 1]

    @staticmethod
    def f_T(paramString):  # ag.java:3155-3160  (up to the first control character)
        b = 0
        while b < len(paramString) and paramString[b] >= ' ':
            b += 1
        return "" if b == 0 else paramString[:b]

    @staticmethod
    def g_T(paramString):  # ag.java:3162-3167  (up to the first space)
        b = 0
        while b < len(paramString) and paramString[b] != ' ':
            b += 1
        return "" if b == 0 else paramString[:b]

    # ---- New Game: hero creation (screens 29 / 6 / 7 / 8) and the save writer ------------

    @staticmethod
    def B_v():  # ag.java:1039-1041
        return system.currentTimeMillis()

    @staticmethod
    def O_v():  # ag.java:1759-1773  (equipment bonuses -> derived stats)
        cz = ag.cz
        cz.s = cz.t = cz.u = cz.v = 0
        for b in range(9):
            if cz.X[b].a != 0:
                cz.s += cz.X[b].b
                cz.t += cz.X[b].c
                cz.u += cz.X[b].d
                cz.v += cz.X[b].e
        cz.w = cz.m + cz.s
        cz.x = cz.n + cz.t
        cz.y = cz.p = cz.o + cz.u
        cz.z = cz.r = cz.q + cz.v

    @staticmethod
    def r_I(paramInt):  # ag.java:1775-1792  (name entry: move the cursor over the 2x14 letter grid)
        j_ = paramInt
        if paramInt != -7 and paramInt != -5 and paramInt != 53:
            if paramInt == -1 or paramInt == 50:
                ag.bP = (ag.bP + 28 - 14) % 28
            elif paramInt == -2 or paramInt == 56:
                ag.bP = (ag.bP + 28 + 14) % 28
            elif paramInt == -3 or paramInt == 52:
                ag.bP = (ag.bP + 28 - 1) % 28
            elif paramInt == -4 or paramInt == 54:
                ag.bP = (ag.bP + 28 + 1) % 28
                if ag.bP == 27:
                    ag.bP = 0
        if ag.bP == 27:
            ag.bP = 26
        return j_

    _F_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                  "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                  "U", "V", "W", "X", "Y", "Z", "OK"]

    @staticmethod
    def f_II(paramInt1, paramInt2):  # ag.java:1794-1819  (letter grid A..Z + OK)
        j_ = ag.bL - 71
        arrayOfString = ag._F_LETTERS
        x.b_IIIII(j_, paramInt2, 142, 34, 0)
        x.b_IIIII(j_ + 123, paramInt2 + 18, 19, 15, 255)
        if ag.bN % 4 < 2:
            if paramInt1 == 26:
                x.b_IIIII(j_ + 123, paramInt2 + 18, 19, 15, 16711680)
            elif F10:
                # DECOMP-FIX F10: `10 * p % 14`, `17 * p / 14` -> `10 * (p % 14)`, `17 * (p / 14)`
                x.b_IIIII(j_ + 2 + 10 * (paramInt1 % 14), paramInt2 + 1 + 17 * (paramInt1 // 14), 10, 15, 16711680)
            else:
                x.b_IIIII(j_ + 2 + 10 * paramInt1 % 14, paramInt2 + 1 + 17 * paramInt1 // 14, 10, 15, 16711680)
        x.a_Lg(ag.bu)
        for b in range(len(arrayOfString)):
            if b == 8:
                b1 = 1
            elif b == 26:
                b1 = 1
            else:
                b1 = 0
            row = 17 * (b // 14) if F10 else 17 * b // 14   # DECOMP-FIX F10
            x.a_TIII(arrayOfString[b], j_ + 3 + b % 14 * 10 + b1, paramInt2 + row, 0)

    def f_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:1847-1880  (arrow from ct[17])
        if paramInt1 == 0:
            b3 = b4 = 0
            b1, b2 = 10, 16
        elif paramInt1 == 1:
            b3, b4 = 9, 0
            b1, b2 = 10, 16
        elif paramInt1 == 2:
            b3, b4 = 20, 0
            b1, b2 = 16, 10
        elif paramInt1 == 3:
            b3, b4 = 20, 9
            b1, b2 = 16, 10
        else:
            return
        ag.a_IIIIMII(paramInt2 + ag.db, paramInt3 + ag.dc, b1, b2, ag.ct[17], b3, b4)

    @staticmethod
    def g_II(paramInt1, paramInt2):  # ag.java:2735-2737
        paramInt2 -= 1
        return paramInt1 + abs(imod(ag.by.nextInt(), abs(paramInt2 - paramInt1) + 1))

    def C_I(self, paramInt):  # ag.java:2739-2741
        return ag.g_II(0, paramInt)

    def d_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # ag.java:2810-2834  (number from ct[19])
        if paramInt4 != 0:
            b1 = 0
            m = idiv(paramInt1, 10)
            paramInt2 += 9
            while m > 0:
                m = idiv(m, 10)
                b1 += 1
                paramInt2 += 9
                if b1 % 3 == 0:
                    paramInt2 += 4
        j_ = paramInt2
        b = 0
        while True:
            if b % 3 == 0 and b != 0:
                paramInt2 -= 4
                self.b_MIIIIII(ag.ct[19], paramInt2, paramInt3, 5, 14, 100, 0)
            paramInt2 -= 9
            self.b_MIIIIII(ag.ct[19], paramInt2, paramInt3, 10, 14, imod(paramInt1, 10) * 10, 0)
            b += 1
            paramInt1 = idiv(paramInt1, 10)
            if paramInt1 <= 0:
                return j_

    def ar(self):  # ag.java:2871-2961  (write the save "gamevil_pow_data")
        cz = ag.cz
        arrayOfChar = [0] * 16
        arrayOfByte = cz.k.encode("latin-1")
        cF = ag.cF
        for b in range(8):
            if b < len(arrayOfByte):
                cF[2 + b] = arrayOfByte[b]
            else:
                cF[2 + b] = 32
        cF[18] = ag.dj & 0xFF
        ag.cG = 19
        ag.G_I(ag.dk)
        ag.G_I(ag.dm)
        ag.G_I(ag.do)
        ag.a_J(ag.dw)
        ag.a_J(ag.dx)
        for b in range(8):
            ag.E_I(i32(ag.dy[b]))
        ag.E_I(ag.dY)
        ag.E_I(ag.ed)
        for b in range(44):
            ag.G_I(ag.fn[0][b])
            ag.G_I(ag.fn[1][b])
        ag.G_I(ag.fo)
        for b in range(25):
            self.a_Lz(ag.fL[b])
        ag.G_I(ag.cq)
        ag.F_I((idiv(ag.cd + 2, 7) * 7 + 4) * 27)
        ag.F_I((idiv(ag.ce + 2, 7) * 7 + 4) * 27)
        for b in range(22):
            ag.G_I(cz.g[b])
        ag.G_I(cz.h)
        ag.G_I(cz.i)
        ag.G_I(cz.l)
        ag.F_I(cz.m)
        ag.F_I(cz.n)
        ag.F_I(cz.o)
        ag.F_I(cz.p)
        ag.F_I(cz.q)
        ag.F_I(cz.r)
        ag.E_I(cz.E)
        ag.E_I(cz.F)
        ag.E_I(cz.G)
        ag.F_I(cz.H)
        ag.F_I(cz.J)
        ag.G_I(cz.S)
        for b in range(5):
            ag.G_I(cz.V[b])
        for b in range(19):
            ag.G_I(cz.W[b])
        for b in range(9):
            self.a_Lz(cz.X[b])
        for b in range(25):
            self.a_Lz(cz.Y[b])
        for b in range(5):
            ag.F_I(cz.Z[b].a)
            ag.G_I(cz.Z[b].b)
        ag.G_I(cz.aa[0])
        ag.G_I(cz.aa[1])
        ag.G_I(cz.aB)
        ag.E_I(i32(ag.dW[0] - ag.dV))
        ag.E_I(i32(ag.eo))
        ag.G_I(ag.fR)
        ag.G_I(ag.fS)
        ag.G_I(ag.dH)
        ag.G_I(ag.ep)
        for b in range(16):
            ag.G_I(arrayOfChar[b])
        ag.E_I(ag.fq)
        for b in range(4):
            ag.E_I(0)
        cF[0] = ag.cG & 0xFF
        cF[1] = ag.cG >> 8 & 0xFF
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_data", True)
            if recordStore.getNumRecords() == 0:
                recordStore.addRecord(cF, 0, len(cF))
            recordStore.setRecord(1, cF, 0, len(cF))
        except Exception:
            pass
        return bool(ag.aq())

    # cF holds Java bytes; the port stores them masked to 0..255 (RecordStore takes bytearray)
    @staticmethod
    def a_J(paramLong):  # ag.java:2963-2973
        for k_ in range(8):
            ag.cF[ag.cG + k_] = paramLong >> (8 * k_) & 0xFF
        ag.cG += 8

    @staticmethod
    def E_I(paramInt):  # ag.java:2975-2981
        ag.cF[ag.cG] = paramInt & 0xFF
        ag.cF[ag.cG + 1] = paramInt >> 8 & 0xFF
        ag.cF[ag.cG + 2] = paramInt >> 16 & 0xFF
        ag.cF[ag.cG + 3] = paramInt >> 24 & 0xFF
        ag.cG += 4

    @staticmethod
    def F_I(paramInt):  # ag.java:2983-2987
        ag.cF[ag.cG] = paramInt & 0xFF
        ag.cF[ag.cG + 1] = paramInt >> 8 & 0xFF
        ag.cG += 2

    @staticmethod
    def G_I(paramInt):  # ag.java:2989-2992
        ag.cF[ag.cG] = paramInt & 0xFF
        ag.cG += 1

    def a_Lz(self, paramz):  # ag.java:2994-3001
        ag.F_I(paramz.a)
        ag.F_I(paramz.b)
        ag.F_I(paramz.c)
        ag.F_I(paramz.d)
        ag.F_I(paramz.e)
        ag.G_I(paramz.f)

    def a_IIIIIII(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7):  # ag.java:3140-3146  (rectangle outline)
        self.l_III(paramInt5, paramInt6, paramInt7)
        ag.f_IIII(paramInt1, paramInt2, paramInt1 + paramInt3 - 1, paramInt2)
        ag.f_IIII(paramInt1, paramInt2 + 1, paramInt1, paramInt2 + paramInt4 - 1)
        ag.f_IIII(paramInt1 + paramInt3 - 1, paramInt2, paramInt1 + paramInt3 - 1, paramInt2 + paramInt4 - 1)
        ag.f_IIII(paramInt1 + 1, paramInt2 + paramInt4 - 1, paramInt1 + paramInt3 - 2, paramInt2 + paramInt4 - 1)

    def b_IIIIIII(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7):  # ag.java:3181-3187  (outline, round corners)
        self.l_III(paramInt5, paramInt6, paramInt7)
        ag.f_IIII(paramInt1 + 1, paramInt2, paramInt1 + paramInt3 - 2, paramInt2)
        ag.f_IIII(paramInt1, paramInt2 + 1, paramInt1, paramInt2 + paramInt4 - 2)
        ag.f_IIII(paramInt1 + paramInt3 - 1, paramInt2 + 1, paramInt1 + paramInt3 - 1, paramInt2 + paramInt4 - 2)
        ag.f_IIII(paramInt1 + 1, paramInt2 + paramInt4 - 1, paramInt1 + paramInt3 - 2, paramInt2 + paramInt4 - 1)

    def c_IIIIIII(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7):  # ag.java:3189-3199  (selection frame)
        self.b_IIIIIII(paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7)
        self.j_II(paramInt1 + 1, paramInt2 + 1)
        self.j_II(paramInt1 + paramInt3 - 2, paramInt2 + 1)
        self.j_II(paramInt1 + 1, paramInt2 + paramInt4 - 2)
        self.j_II(paramInt1 + paramInt3 - 2, paramInt2 + paramInt4 - 2)

    def j_II(self, paramInt1, paramInt2):  # ag.java:3209-3211
        ag.f_IIII(paramInt1, paramInt2, paramInt1 + 1, paramInt2 + 1)

    def au(self):  # ag.java:3213-3220  (New Game -> difficulty screen 29)
        ag.bb.c_v()
        ag.cM[0] = 29
        ag.cN = ae.v[ag.cM[0]]
        ag.cM[1] = 1
        ag.cz.aB = 0
        self.av()

    def av(self):  # ag.java:3222-3273  (fresh hero)
        cz = ag.cz
        ag.dj = 0
        ag.dH = 0
        ag.dw = 35113052110447
        ag.dx = 0
        ag.ed = 0
        ag.cq = 0
        cz.aB = 0
        cz.k = ""
        for b in range(45):
            ag.fn[1][b] = 0
            ag.fn[0][b] = 0
        ag.fo = 0
        for b in range(8):
            ag.dy[b] = 0
        cz.l = 1
        ag.aw()
        cz.F = 0
        cz.E = 0
        cz.G = 0
        cz.S = 0
        for b in range(22):
            cz.g[b] = 0
        cz.h = 0
        cz.i = 0
        for b in range(5):
            cz.V[b] = 0
            cz.Z[b].a = 0
            cz.Z[b].b = 0
        for b in range(19):
            cz.W[b] = 0
        cz.W[0] = 1
        cz.W[5] = 1
        cz.V[0] = 12
        cz.V[1] = 17
        if ag.bi:
            for b in range(19):
                cz.W[b] = 1
            cz.W[18] = 1
        # z.a() is shadowed by the field z.a on instances -> call it through the class
        for b in range(9):
            z.a(cz.X[b])
        for b in range(25):
            z.a(cz.Y[b])
        self.k_II(116, 0)
        self.a_LzLz(cz.X[0], cz.Y[0])
        cz.aa[0] = 0
        cz.aa[1] = 1

    @staticmethod
    def aw():  # ag.java:3275-3284  (base stats, 5 free points)
        cz = ag.cz
        cz.m = 5
        cz.n = 4
        cz.o = 30
        cz.p = 30
        cz.q = 10
        cz.r = 10
        cz.J = 5
        ag.ck = 1

    def k_II(self, paramInt1, paramInt2):  # ag.java:3286-3360  (give an item / potion / gold)
        cz = ag.cz
        b = 0
        if paramInt1 < 100:
            if paramInt2 != 0:
                b1 = -1
                b = 0
                while b < 5:
                    if cz.Z[b].a == paramInt1:
                        if cz.Z[b].b > 4:
                            return 0
                        break
                    if 0 == cz.Z[b].a and b1 < 0:
                        b1 = b
                    b += 1
                if b1 > -1 and b > 4:
                    b = b1
                if b > 4:
                    return 0
            else:
                cz.Z[ag.dU.e].b = i16(cz.Z[ag.dU.e].b - 1)
                if cz.Z[ag.dU.e].b < 1:
                    cz.Z[ag.dU.e].a = 0
                return 1
        elif paramInt1 < 10000:
            b = 0
            while b < 25 and 0 != cz.Y[b].a:
                b += 1
            if b > 24:
                return 0
            cz.Y[b].a = i16(paramInt1)
            cz.Y[b].b = 0
            cz.Y[b].c = 0
            cz.Y[b].d = 0
            cz.Y[b].e = 0
            cz.Y[b].f = 0
        if paramInt1 < 10000:
            ag.bb.e_I(paramInt1)
        if paramInt1 < 100:
            cz.Z[b].a = i16(paramInt1)
            cz.Z[b].b = i16(cz.Z[b].b + 1)
        elif paramInt1 < 300:
            if paramInt2 != 0:
                s = i16(ag.cX.d + self.C_I(ag.cX.e + 1))
            else:
                s = ag.cX.d
            if ag.cX.c == 0:
                cz.Y[b].b = s
            elif ag.cX.c == 1:
                cz.Y[b].c = s
            elif ag.cX.c == 2:
                cz.Y[b].d = s
            elif ag.cX.c == 3:
                cz.Y[b].e = s
        elif paramInt1 < 500:
            cz.Y[b].b = ag.cY.c
            cz.Y[b].c = i16(ag.cY.d)
            cz.Y[b].d = ag.cY.e
            cz.Y[b].e = i16(ag.cY.f)
        elif paramInt1 < 10000:
            cz.Y[b].b = ag.cZ.c
            cz.Y[b].c = i16(ag.cZ.d)
            cz.Y[b].d = ag.cZ.e
            cz.Y[b].e = i16(ag.cZ.f)
        else:
            cz.E += paramInt1 - 10000
        return 1

    @staticmethod
    def ax():  # ag.java:3362-3375  (starting quick items)
        for b in range(8):
            if ag.fL[b] is None:
                ag.fL[b] = z()
        ag.fL[0].a = 1
        ag.fL[1].a = 2
        ag.fL[2].a = 3
        ag.fL[3].a = 4
        ag.fL[4].a = 5
        ag.fL[5].a = 6
        ag.fL[6].a = 10
        ag.fL[7].a = 11

    def ay(self):  # ag.java:3377-3398  (17 random shop items, sorted)
        arrayOfInt = [0] * 17
        ag.az()
        for b in range(17):
            arrayOfInt[b] = 101 + 5 * ag.g_II(0, 20) + ag.I_I(ag.g_II(0, 100))
        for b in range(16, 0, -1):
            bool_ = False
            for b1 in range(b):
                if arrayOfInt[b1] > arrayOfInt[b1 + 1]:
                    j_ = arrayOfInt[b1]
                    arrayOfInt[b1] = arrayOfInt[b1 + 1]
                    arrayOfInt[b1 + 1] = j_
                    bool_ = True
            if not bool_:
                break
        for b in range(17):
            ag.fL[8 + b] = self.J_I(arrayOfInt[b])

    @staticmethod
    def az():  # ag.java:3400-3412
        from pow.game.d import d
        arrayOfInt = [47, 51, 49]
        if not ag.fM[1]:
            for b in range(3):
                if ag.bH[b] is None:
                    ag.bH[b] = d("/" + ag.bE.a_I(arrayOfInt[b]))
                if ag.bH[b] is None:
                    return False
            ag.fM[1] = True
        return True

    @staticmethod
    def I_I(paramInt):  # ag.java:3414-3422  (item tier by hero level)
        m = 0
        b = 0
        while b < 5 and ag.cz.l >= ae.w[b]:
            b += 1
        j_ = ae.x[b - 1]
        b = 0
        while b < 4:
            m += j_ & 0xFF
            if not paramInt >= m:
                break
            j_ >>= 8
            b += 1
        return b

    def J_I(self, paramInt):  # ag.java:3424-3457  (make item paramInt with random bonus)
        z1 = z()
        arrayOfInt = [0] * 5
        z1.a = i16(paramInt)
        z1.f = 0
        if paramInt < 300:
            for b in range(3):
                arrayOfInt[b] = ag.bH[0].a_II(paramInt - 101, 2 + b)
            if arrayOfInt[0] == 0:
                z1.b = i16(arrayOfInt[1] + self.C_I(arrayOfInt[2]))
            elif arrayOfInt[0] == 1:
                z1.c = i16(arrayOfInt[1] + self.C_I(arrayOfInt[2]))
            elif arrayOfInt[0] == 2:
                z1.d = i16(arrayOfInt[1] + self.C_I(arrayOfInt[2]))
            elif arrayOfInt[0] == 3:
                z1.e = i16(arrayOfInt[1] + self.C_I(arrayOfInt[2]))
        else:
            tbl = ag.bH[1] if paramInt < 500 else ag.bH[2]
            # ORIG-BUG B1: the original reads both tables at id - 301, so a Rare item (shinki.arr,
            # ids 501-518) gets row 200+ -> all 0; its own row is id - 501
            first = 501 if paramInt >= 500 and config.ORIG_BUG["B1"] else 301
            for b in range(4):
                arrayOfInt[b] = tbl.a_II(paramInt - first, 2 + b)
            z1.b = i16(arrayOfInt[0])
            z1.c = i16(arrayOfInt[1])
            z1.d = i16(arrayOfInt[2])
            z1.e = i16(arrayOfInt[3])
        return z1

    def l_II(self, paramInt1, paramInt2):  # ag.java:3488-3528  (start the story player, bV = 10)
        ag.ee = i16(paramInt1)
        if paramInt1 < 100:
            ag.ec = 0
            b = 64 + paramInt1 // 6
            for b1 in range(3):
                ag.eb[b1] = ae.aV[(paramInt1 << 1) + b1] - ae.aV[paramInt1 // 6 * 12]
            if paramInt1 == 3 and paramInt2 != 0 and 0 == ag.L_I(502):
                ag.eb[2] = 0
                ag.eb[1] = 0
                ag.eb[0] = 0
                ag.cq = 4
            ag.fE = -1
        else:
            ag.ec = 1
            b = 63
            ag.eb[0] = 0
            ag.eb[1] = 2
            ag.eb[2] = 13
            ag.fE = 0
            ag.dE = ag.fU
            ag.cO = 0
        if ag.bI is None:
            ag.bI = al("/" + ag.bE.a_I(b))
        ag.gf[1] = ""
        ag.gf[0] = ""
        ag.fA[1] = 0
        ag.fA[0] = 0
        ag.fD = 0
        ag.dS = 0
        ag.fG = 0
        ag.bd.c_I(ag.fD)
        if 0 == ag.ec:
            self.x_I(1)
        ag.bV = 10
        self.a__I(2)
        ag.ck = 1

    @staticmethod
    def L_I(paramInt):  # ag.java:3530-3536  (inventory slot of item, 1-based; 0 = none)
        for b in range(25):
            if ag.cz.Y[b].a == paramInt:
                return b + 1
        return 0

    # ---- story player (bV == 10): prologue / epilogue -------------------------------------

    def M_v(self):  # ag.java:1612-1692  (one tick of the story player)
        if ag.dS > 0:
            ag.dS = i16(ag.dS - 1)
            if ag.ch != -999 and ag.dS > 3:
                ag.dS = 3
            if 0 == ag.dS:
                ag.fD += 1
                if ag.fD < ag.eb[2] - ag.eb[0]:
                    ag.bd.c_I(ag.fD)
                elif 0 == ag.ec and ag.cO == 0 and ag.fD == ag.eb[2] - ag.eb[0]:
                    if ag.ef != 0 or ag.eg != 0:
                        ag.cS.e_I(27)
                    ag.bd.c_I(ag.fD)
                else:
                    ag.bI.a_v()
                    ag.bI = None
                    ag.gf[1] = ""
                    ag.gf[0] = ""
                    self.F_v()
                    ag.cM[0] = ag.cO
                    ag.ct[35] = None
                    ag.ct[35] = None
                    ag.ap()
                    if ag.cM[0] == 0:
                        ag.cM[1] = 0
                    ag.bV = 2
                    ag.cL = 0
                    ag.cK = 0
                ag.ck = 1
        elif (0 == ag.ec and ag.fD < ag.eb[1] - ag.eb[0]) or (ag.ec != 0 and ag.fD >= ag.eb[1] - ag.eb[0]):
            from pow.game.e import e
            e.a_III(ag.fG, ag.fA[ag.fG], 0)
            if len(ag.fw[ag.fG]) <= ag.fA[ag.fG]:
                if ag.ch != -999:
                    ag.dS = 0
                else:
                    ag.dS = 15
        else:
            self.N_v()
            ag.eh = i16(ag.eh + 1)
            if ag.fG == 0:
                if ag.eh > 3:
                    ag.fG = i16(ag.fG + 1)
                    ag.eh = 0
            elif ag.fG == 2:
                if ag.eh > 4:
                    ag.dS = 3
            elif ag.fG == 1:
                ag.fA[0] = ag.fA[0] - 2
                if ag.fA[0] < -28:
                    ag.fA[0] = ag.fA[0] + 22
                    ag.fC[0] = ag.fC[0] + 1
                    if ag.dq[0] < ag.fC[0]:
                        if ag.fD == ag.eb[2] - ag.eb[0]:
                            ag.dS = 3
                        else:
                            ag.fG = i16(ag.fG + 1)
                    ag.eh = 1
        if ag.ch == -6:
            ag.dS = 1
            if ag.ec != 0:
                if ag.fD >= ag.eb[1] - ag.eb[0]:
                    ag.fD = 100
                    return
            elif ag.fD < ag.eb[1] - ag.eb[0]:
                ag.fD = ag.eb[1] - ag.eb[0] - 1

    def d_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:1694-1696  (fill the screen)
        x.b_IIIII(0, 0, ag.bZ.a, ag.bZ.b, ag.k_III(paramInt1, paramInt2, paramInt3))

    def N_v(self):  # ag.java:1698-1737  (story picture + scrolling text)
        self.d_III(0, 0, 0)
        ct35 = ag.ct[35]
        if ag.fG in (0, 2):
            if 0 < ag.eh < 4:
                self.b_MIIIIII(ct35, ag.dd - (ct35.getWidth() >> 1), ag.de - (ct35.getHeight() >> 1),
                               ct35.getWidth(), ct35.getHeight(), 0, 0)
        elif ag.fG == 1:
            m = ag.fA[0]
            if ag.fD != ag.eb[2] - ag.eb[0]:
                self.b_MIIIIII(ct35, ag.dd - (ct35.getWidth() >> 1), ag.de - (ct35.getHeight() >> 1),
                               ct35.getWidth(), ct35.getHeight(), 0, 0)
            j_ = ag.fC[0]
            while j_ <= ag.dq[0] and m <= 230:
                # char arithmetic, as decompiled: `255 - (m - de + 72 << 4)` (only ==255 / ==0 matter)
                if m > ag.de + 72:
                    c1 = 255 - (m - ag.de + 72 << 4) & 0xFFFF
                elif m < ag.de - 72:
                    c1 = 255 - (ag.de - 72 - m << 4) & 0xFFFF
                else:
                    c1 = 255
                x.a_Lg(ag.bv)
                self.b_TII(ag.dp[0][j_], m + 1, 30)
                ag.a_TII(ag.dp[0][j_], m - 1, 1)
                if c1 == 255:
                    x.a_Lg(ag.bu)
                elif c1 == 0:
                    x.a_Lg(ag.bv)
                else:
                    x.a_Lg(ag.bx)
                self.b_TII(ag.dp[0][j_], m, 30)
                m += 22
                j_ += 1
        self.q_I(2)

    def q_I(self, paramInt):  # ag.java:1739-1741  (soft key "Skip")
        ag.h_II(0, -1)

    @staticmethod
    def a_B(paramByte):  # ag.java:3021-3024  (width of a character)
        return ag.bu.a_C(chr(paramByte & 0xFFFF))

    def b_ABII(self, paramArrayOfbyte, paramInt1, paramInt2):  # ag.java:3100-3138  (word wrap into dp[paramInt2])
        m = 0
        i1 = 0
        i2 = 0
        b = 0
        ag.dq[paramInt2] = 0
        dp = ag.dp[paramInt2] = [None] * 120
        n_ = len(paramArrayOfbyte)
        j_ = 0
        while j_ <= n_:
            if j_ != n_:
                c = paramArrayOfbyte[j_]
                i2 += ag.a_B(c)
                if (c == 32 or c == 124) and i2 - ag.a_B(c) >= paramInt1:
                    if i1 < m:
                        i1 = j_
                    dp[b] = ag.a_ABII(paramArrayOfbyte, m, i1)
                    b += 1
                    m = i1 + 1
                    j_ = m - 1
                    i2 = 0
                elif c == 32:
                    i1 = j_
                elif c == 124:
                    dp[b] = ag.a_ABII(paramArrayOfbyte, m, j_)
                    b += 1
                    m = i1 = j_ + 1
                    i2 = 0
            elif i2 > paramInt1:
                dp[b] = ag.a_ABII(paramArrayOfbyte, m, i1)
                b += 1
                dp[b] = ag.a_ABII(paramArrayOfbyte, i1 + 1, j_)
                b += 1
            elif i1 != n_ - 1:
                dp[b] = ag.a_ABII(paramArrayOfbyte, m, j_)
                b += 1
            j_ += 1
        if b >= 1:
            ag.dq[paramInt2] = i8(b - 1)
        return 1

    @staticmethod
    def a_AC(paramArrayOfchar):  # ag.java:3542-3547  (Integer.parseInt of the leading digits)
        str_ = ""
        b = 0
        while b < len(paramArrayOfchar) and '0' <= paramArrayOfchar[b] <= '9':
            str_ = str_ + paramArrayOfchar[b]
            b += 1
        return int(str_)

    # ---- menus: Options / Help / Endings helpers -------------------------------------------

    def d_II(self, paramInt1, paramInt2):  # ag.java:1743-1745
        return ag.e_II(paramInt1, paramInt2).encode("latin-1")

    @staticmethod
    def e_II(paramInt1, paramInt2):  # ag.java:1747-1753  (string paramInt2 of edat file paramInt1)
        al1 = al("/" + ag.bE.a_I(paramInt1))
        str_ = al1.a_I(paramInt2)
        al1.a_v()
        return str_

    def e_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:1828-1830  (small number, ct[20])
        self.a_IIIIIMIII(paramInt1, paramInt2, paramInt3, 9, 12, ag.ct[20], 0, 0, 0)

    def a_IIIIIMIII(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramImage,
                    paramInt6, paramInt7, paramInt8):  # ag.java:1832-1845  (number from a digit strip)
        if paramInt1 < 0 or paramImage is None:
            return
        paramInt2 -= paramInt4
        if paramInt1 > 0:
            while paramInt1 > 0:
                # DECOMP-FIX F10: `p6 + p4 * p1 % 10` -> `p6 + p4 * (p1 % 10)`
                sx = paramInt6 + paramInt4 * (paramInt1 % 10) if F10 else paramInt6 + paramInt4 * paramInt1 % 10
                ag.a_IIIIMII(paramInt2, paramInt3, paramInt4, paramInt5, paramImage, sx, paramInt7)
                paramInt1 //= 10
                paramInt2 -= paramInt4 + paramInt8
            return
        ag.a_IIIIMII(paramInt2, paramInt3, paramInt4, paramInt5, paramImage, paramInt6, paramInt7)

    def i_II(self, paramInt1, paramInt2):  # ag.java:3169-3173  (empty 30x30 item slot)
        ac1 = ac(paramInt1 + 1, paramInt2 + 1, 28, 28)
        self.b_IIIIIII(paramInt1, paramInt2, 30, 30, 80, 80, 80)
        x.b_IIIII(ac1.a, ac1.b, ac1.c, ac1.d, 0)

    def e_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # ag.java:3175-3179  (grey frame, black inside)
        ac1 = ac(paramInt1 + 1, paramInt2 + 1, paramInt3 - 2, paramInt4 - 2)
        self.b_IIIIIII(paramInt1, paramInt2, paramInt3, paramInt4, 152, 152, 152)
        x.b_IIIII(ac1.a, ac1.b, ac1.c, ac1.d, 0)

    def y_I(self, paramInt):  # ag.java:2474-2520  (Options: change the value of row cM[1])
        v = ag.cM[1]
        if v == 0:
            ag.df = not ag.df
            if ag.df:
                self.a__I(8)
            else:
                ag.ai()
        elif v == 1:
            if paramInt == 1:
                ag.dg = i16(ag.dg + 25)
                if ag.dg > 100:
                    ag.dg = 0
            elif paramInt == 0:
                ag.dg = i16(ag.dg - 25)
                if ag.dg < 0 or ag.dg > 100:
                    ag.dg = 100
            if ag.dg == 0:
                ag.df = False
                ag.ai()
            elif ag.dg > 0:
                ag.df = True
                if system.currentTimeMillis() - ag.di > 300:
                    ag.di = system.currentTimeMillis()
                    self.a__I(8)
        elif v == 2:
            if paramInt != 0:
                ag.dh = i16(ag.dh + 1)
                if ag.dh > 4:
                    ag.dh = 0
            else:
                ag.dh = i16(ag.dh - 1)
                if ag.dh < 0:
                    ag.dh = 4
        ag.H_v()

    # ---- Management: items, descriptions ---------------------------------------------------

    @staticmethod
    def g_I(paramInt):  # ag.java:867-870  (equipment slot type of an item)
        ag.bb.e_I(paramInt)
        if paramInt < 100:
            return 1
        if paramInt < 300:
            return i8(ag.cX.b)
        if paramInt < 500:
            return ag.cY.b
        return ag.cZ.b

    @staticmethod
    def a_LzZI(paramz, paramBoolean, paramInt):  # ag.java:1454-1457  (item description in the shop)
        # dF.a() (ak.java:10-17) - the method is shadowed by the field ak.a in Python
        dF = ag.dF
        dF.a = 0
        dF.b.a = dF.b.b = dF.b.c = dF.b.d = 0
        dF.c = ""
        ag.bb.a_LzIIIIIZ(paramz, 0, 0, 200, 22, paramInt, paramBoolean)

    @staticmethod
    def a_Lp(paramp):  # ag.java:1459-1465  (potion slot -> item)
        z1 = z()
        z.a(z1)
        z1.a = paramp.a
        z1.b = paramp.b
        return z1

    def o_I(self, paramInt):  # ag.java:1467-1492  (item under the cursor of the item grid)
        z1 = z()
        if paramInt == -1:
            paramInt = ag.fK[18]
        v = ag.fK[0]
        if v == 0:
            z1 = ag.fL[paramInt]
        elif v == 1:
            if paramInt < 5:
                z1 = ag.a_Lp(ag.cz.Z[paramInt])
            else:
                z1 = ag.cz.Y[paramInt - 5]
        elif v in (2, 3):
            if ag.fK[27] == 0:
                z1 = ag.cz.Y[paramInt]
            else:
                z1 = ag.cz.X[paramInt]
        return z1

    @staticmethod
    def a_LacI(paramac, paramInt):  # ag.java:1507-1510  (fill rect)
        if paramac is not None:
            x.b_IIIII(paramac.a, paramac.b, paramac.c, paramac.d, paramInt)

    @staticmethod
    def b_LacI(paramac, paramInt):  # ag.java:1512-1515  (outline rect)
        if paramac is not None:
            x.a_IIIII(paramac.a, paramac.b, paramac.c, paramac.d, paramInt)

    @staticmethod
    def a_LacII(paramac, paramInt1, paramInt2):  # ag.java:1517-1520
        x.b_IIIII(paramac.a, paramac.b, paramac.c, paramac.d, paramInt2)
        x.a_IIIII(paramac.a, paramac.b, paramac.c, paramac.d, paramInt1)

    @staticmethod
    def s_I(paramInt):  # ag.java:1822-1826  (number of digits)
        arrayOfInt = [10, 100, 1000, 10000]
        b = 0
        while b < 4 and paramInt >= arrayOfInt[b]:
            b += 1
        return b + 1

    @staticmethod
    def c_T(paramString):  # ag.java:1755-1757  (text width)
        return ag.bu.a_T(paramString)

    def i_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:1823-1825  (small digit from ct[20])
        self.b_MIIIIII(ag.ct[20], paramInt1, paramInt2, 9, 12, paramInt3 * 9, 0)

    def J_v(self):  # ag.java:1279-1291  (gold box)
        arrayOfShort = [7, 14, 21, 32, 39, 46, 57, 64, 71, 82]
        j_ = ag.cz.E
        self.a_IIIIZ(ag.dd - 70, ag.de - 80 + ag.dc, 140, 22, False)
        b = 0
        while b < 9:
            j_ = idiv(j_, 10)
            if 0 == j_:
                break
            b += 1
        self.d_IIII(ag.cz.E, ag.dd + (arrayOfShort[b] >> 1) + 16 - ag.db, ag.de - 76, 0)
        self.b_MIIIIII(ag.ct[32], ag.dd - 69 - ag.db, ag.de - 80, ag.ct[32].getWidth(), ag.ct[32].getHeight(), 0, 0)

    def b_IIIII(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # ag.java:1293-1352  (description of item / skill)
        cz = ag.cz
        dF = ag.dF
        s1 = s2 = s3 = s4 = s5 = s6 = 0
        str_ = ""
        dF.b.a = paramInt2
        dF.b.b = paramInt3
        dF.b.c = paramInt4
        dF.b.d = paramInt5
        dF.c = ""
        if paramInt1 > 999:
            if paramInt1 < 1100:
                it = cz.X[paramInt1 - 1000]
            elif paramInt1 < 1200:
                it = cz.Y[paramInt1 - 1100]
            else:
                it = None
            if it is not None:
                s6 = ag.m_I(it.a)
                s1 = it.b
                s2 = it.c
                s3 = it.d
                s4 = it.e
                s5 = i16(it.f)
                str_ = ag.l_I(it.a)
            elif paramInt1 < 2000:
                dF.c = ag.k_I(cz.Z[paramInt1 - 1200].a)
            else:
                dF.c = self.j_I(paramInt1 - 2000)
        if dF.c != "":
            if str_ != "":
                dF.c += str_
            if s1 != 0:
                dF.c += " / ATK+" + str(s1)
            if s2 != 0:
                dF.c += " / DEF+" + str(s2)
            if s3 != 0:
                dF.c += " / HP+" + str(s3)
            if s4 != 0:
                dF.c += " / MP+" + str(s4)
            if s5 != 0:
                dF.c += " / Enchanted Lv" + str(s5)
            if s6 != 0:
                dF.c += " / Available at Lv" + str(s6)
            ag.dD = ag.c_T(dF.c)
            if ag.dD > paramInt4 - 2:
                dF.a = 1
                dF.d = i16(paramInt2 + 20)
                return
            dF.a = 0
            dF.d = i16(paramInt2 + 1)

    def j_I(self, paramInt):  # ag.java:1354-1368  (skill description)
        str1 = ""
        paramInt -= 12
        if paramInt < 0 or paramInt > 18:
            return str1
        arrayOfByte = self.d_II(54, paramInt)
        str2 = ag.a_ABII(arrayOfByte, 0, len(arrayOfByte))
        if ag.cz.W[paramInt] != 0:
            arrayOfByte = self.d_II(54, paramInt + 19)
            str1 = str2 + " / Lv" + str(ag.cz.W[paramInt]) + " " + ag.a_ABII(arrayOfByte, 0, len(arrayOfByte))
        else:
            str1 = str2 + " / (Not Available)"
        return str1

    @staticmethod
    def k_I(paramInt):  # ag.java:1370-1381  (potion description)
        str_ = ""
        paramInt -= 1
        if paramInt < 0 or paramInt > 10:
            return str_
        if paramInt < 9:
            str_ = (ae.aN[paramInt] + " / Recover " + str(ae.aP[paramInt % 3]) + "% of total "
                    + ae.aO[paramInt // 3])
        else:
            arrayOfByte = ag.e_II(54, 24 + paramInt).encode("latin-1")
            str_ = ae.aN[paramInt] + " / " + ag.a_ABII(arrayOfByte, 0, len(arrayOfByte))
        return str_

    @staticmethod
    def l_I(paramInt):  # ag.java:1383-1399  (special item suffix)
        return {434: " / Hp 5 Increased", 435: " / MP 3 Increased", 436: " / DEF 1 Increased",
                437: " / ATK 1 Increased", 502: " / Catherine's scarf",
                504: " / all General Visiting"}.get(paramInt, "")

    @staticmethod
    def m_I(paramInt):  # ag.java:1401-1416  (item name -> dF.c, returns the level needed)
        ag.bb.e_I(paramInt)
        if paramInt > 500:
            ag.dF.c = ag.cZ.a
            return ag.cZ.g
        if paramInt > 300:
            ag.dF.c = ag.cY.a
            return ag.cY.h
        if paramInt > 100:
            ag.dF.c = ag.cX.a
            return ae.aM[paramInt % 5]
        return 0

    # ---- Blacksmith helpers ----------------------------------------------------------------

    def c_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # ag.java:1246-1248
        ag.a_IIIIIIIZ(paramInt1 + 1, paramInt2 + 1, paramInt3 - 2, paramInt4 - 2, 0, 0, 10000536, True)

    def b_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:1250-1254  (centred box, returns its x)
        j_ = 240 - paramInt2 >> 1
        self.c_IIII(j_, paramInt1, paramInt2, paramInt3)
        return j_

    def c_II(self, paramInt1, paramInt2):  # ag.java:1256-1269  (gold box with amount paramInt1)
        j_ = self.b_III(paramInt2, 200, 22)
        b = 0
        i1 = paramInt1
        while True:
            b += 1
            i1 = idiv(i1, 10)
            if not i1 > 0:
                break
        j_ += 100
        m = b * 7 + (b - 1) // 3 * 4 + 12 + 3
        j_ -= m >> 1
        paramInt2 += 6
        self.h_III(paramInt1, j_ + m + 10, paramInt2)
        self.b_MIIIIII(ag.ct[32], ag.dd - 69, paramInt2 - 5, ag.ct[32].getWidth(), ag.ct[32].getHeight(), 0, 0)

    def i_I(self, paramInt):  # ag.java:1271-1273
        self.c_II(ag.cz.E, paramInt)

    def h_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:2797-2808  (number with thousands commas)
        # DECOMP-FIX F12: the decompiled loop `do { if (!b || b % 3 != 0) continue; ... ++b; }`
        # skips every digit (the number is never drawn). Restored: comma before every 3rd digit.
        b = 0
        while True:
            if F12:
                if b != 0 and b % 3 == 0:
                    paramInt2 -= 4
                    ag.a_IIIIMII(paramInt2, paramInt3, 5, 14, ag.ct[19], 100, 0)
                paramInt2 -= 10
                ag.a_IIIIMII(paramInt2, paramInt3, 10, 14, ag.ct[19], imod(paramInt1, 10) * 10, 0)
                b += 1
            paramInt1 = idiv(paramInt1, 10)
            if not paramInt1 > 0:
                break

    @staticmethod
    def n_I(paramInt):  # ag.java:1437-1452  (12345 -> "12,345")
        str_ = str(paramInt)
        j_ = len(str_)
        arrayOfInt = [0] * j_
        for b1 in range(j_):
            arrayOfInt[j_ - b1 - 1] = imod(paramInt, 10)
            paramInt = idiv(paramInt, 10)
        str_ = ""
        for b2 in range(j_):
            str_ = str_ + str(arrayOfInt[b2])
            if j_ % 3 == (b2 + 1) % 3 and b2 != j_ - 1:
                str_ = str_ + ","
        return str_

    # ---- Missions: lords, mission list, briefing text, general data ------------------------

    @staticmethod
    def b_B(paramByte):  # ag.java:3484-3486
        return i16(paramByte & 0xFF)

    def C_v(self):  # ag.java:1043-1062  (lords of chapter cq -> ds/dt/du/dv, list dE = dt)
        j_ = 0
        arrayOfByte = ag.v_I(48)
        j_ = 38 * ag.cq + 40
        ag.dr = 0
        for b in range(6):
            ag.ds[b] = i8(arrayOfByte[j_ + b])
            if ag.ds[b] > 0:
                m = 38 * ag.ds[b] + 10
                b1 = 0
                while b1 < 30 and arrayOfByte[m + b1] != 0:
                    b1 += 1
                ag.dt[b] = ag.a_ABII(arrayOfByte, m, m + b1)
                ag.du[b] = i8(arrayOfByte[m + 36])
                ag.dv[b] = i8(arrayOfByte[m + 37])
                ag.dr += 1
        ag.cN = ag.dr
        ag.dE = ag.dt

    def D_v(self):  # ag.java:1064-1073  (mission description -> dp[0])
        ag.dn = ag.dA[ag.dm]
        arrayOfByte1 = ag.v_I(56)
        arrayOfByte2 = self.a_ABI(arrayOfByte1, ag.du[ag.dk] + ag.dm)
        b = 0
        while b < len(arrayOfByte2) and arrayOfByte2[b] != 0:
            b += 1
        arrayOfByte3 = bytearray(arrayOfByte2[:b])
        self.b_ABII(arrayOfByte3, 190, 0)

    def a_ABI(self, paramArrayOfbyte, paramInt):  # ag.java:1075-1124  (text paramInt of a table, "(..)" macros)
        arrayOfInt1 = [0] * 110
        arrayOfByte1 = bytearray(1500)
        arrayOfByte2 = bytearray(1500)
        arrayOfByte3 = bytearray(1500)
        arrayOfChar = ['\0'] * 3
        b1 = 0
        arrayOfInt2 = [0, 0]
        arrayOfInt3 = [0, 0]
        j_ = paramArrayOfbyte[0] & 0xFF | paramArrayOfbyte[1] << 8 & 0xFF00
        for b2 in range(j_ + 1):
            arrayOfInt1[b2] = paramArrayOfbyte[2 + b2 * 2] & 0xFF | paramArrayOfbyte[2 + b2 * 2 + 1] << 8 & 0xFF00
        _arraycopy(paramArrayOfbyte, arrayOfInt1[paramInt], arrayOfByte1, 0,
                   arrayOfInt1[paramInt + 1] - arrayOfInt1[paramInt])
        b2 = 0
        while b2 < 3 and 48 <= arrayOfByte1[b2] <= 57:
            arrayOfChar[b2] = chr(arrayOfByte1[b2])
            b1 += 1
            b2 += 1
        if b1 != 0:
            arrayOfInt3[0] = b1 + 1
            arrayOfInt2[0] = b1 + 1
            m = ag.a_AC(arrayOfChar)
            _arraycopy(paramArrayOfbyte, arrayOfInt1[m], arrayOfByte2, 0, arrayOfInt1[m + 1] - arrayOfInt1[m])
        else:
            _arraycopy(arrayOfByte1, 0, arrayOfByte2, 0, 1500)
        while arrayOfByte2[arrayOfInt3[1]] != 0:
            if arrayOfByte2[arrayOfInt3[1]] == 40:
                arrayOfByte3 = ag.a_ABABII(arrayOfByte3, arrayOfByte2, arrayOfInt2[1], arrayOfInt3[1])
                arrayOfInt2[1] = arrayOfInt3[1] + 1
                if b1 != 0:
                    arrayOfInt3[1] = ag.a_ABIC(arrayOfByte2, arrayOfInt3[1], ')')
                    # DECOMP-FIX F15: the source is `arrayOfInt2[1] = arrayOfInt3[1] = a(.., ')')`
                    # (one call; JD split the dup_x2 into a second search). Literally the second
                    # search skips the next "(..)" and the copy length is negative: every mission
                    # description with a numbered template (Hellgate...) throws in arraycopy.
                    if config.DECOMP_FIX["F15"]:
                        arrayOfInt2[1] = arrayOfInt3[1]
                    else:
                        arrayOfInt2[1] = ag.a_ABIC(arrayOfByte2, arrayOfInt3[1], ')')
                    arrayOfInt3[0] = ag.a_ABIC(arrayOfByte1, arrayOfInt3[0], '|')
                    arrayOfByte3 = ag.a_ABABII(arrayOfByte3, arrayOfByte1, arrayOfInt2[0], arrayOfInt3[0] - 1)
                    arrayOfInt2[0] = arrayOfInt3[0]
                    continue
                arrayOfInt3[1] = ag.a_ABIC(arrayOfByte2, arrayOfInt3[1], ')')
                arrayOfByte3 = ag.a_ABABII(arrayOfByte3, arrayOfByte2, arrayOfInt2[1], arrayOfInt3[1] - 1)
                arrayOfInt2[1] = arrayOfInt3[1]
                continue
            arrayOfInt3[1] = arrayOfInt3[1] + 1
        arrayOfByte3 = ag.a_ABABII(arrayOfByte3, arrayOfByte2, arrayOfInt2[1], arrayOfInt3[1])
        return arrayOfByte3

    @staticmethod
    def a_ABABII(paramArrayOfbyte1, paramArrayOfbyte2, paramInt1, paramInt2):  # ag.java:1126-1131  (append at the first 0)
        b = 0
        while b < len(paramArrayOfbyte1) and paramArrayOfbyte1[b] != 0:
            b += 1
        _arraycopy(paramArrayOfbyte2, paramInt1, paramArrayOfbyte1, b, paramInt2 - paramInt1)
        return paramArrayOfbyte1

    @staticmethod
    def a_ABIC(paramArrayOfbyte, paramInt, paramChar):  # ag.java:1133-1142  (index after the next paramChar)
        c = ord(paramChar)
        b = 0
        while paramArrayOfbyte[paramInt + b] != c and paramArrayOfbyte[paramInt + b] != 0:
            if (paramArrayOfbyte[paramInt + b] & 0x80) != 0:
                b += 2
            b += 1
        return paramInt + b + 1

    def ac_v(self):  # ag.java:2277-2281
        for b in range(6):
            ag.cx[b] = None
        ag.R_v()

    def y_v(self):  # ag.java:872-967  (enter the map: bV = 3)
        cz = ag.cz
        cz.K = ag.g_I(cz.X[0].a)
        ag.ai()
        self.ah()
        ag.bb.d_v()
        self.ab_v()
        ag.bY.a = 240
        ag.bY.b = 243
        ag.db = 0
        ag.dc = 16
        ag.bV = 3
        ag.co = 2
        ag.cn = 1
        ag.cr = 0
        ag.cl = 0
        ag.fq = 0
        if ag.dj != 0:
            bool_ = 1
        else:
            if F13 and cz.a[1] is not cz.a[0]:
                # DECOMP-FIX F13: the start position is written into cz.a[1], but the map
                # (c.f(), c.a(5 ints)) reads cz.a[0]. Both are the same object once ar.aC()
                # (cz.a[1] = cz.a[0]) has run; on the first map after start-up they are not,
                # and the hero would stand at (0, 0).
                cz.a[1] = cz.a[0]
            cz.a[1].a = i16(ag.dz[ag.dm].b * 27 + 12)
            cz.a[1].b = i16(ag.dz[ag.dm].c * 27 + 20)
            ag.do = 1
            ag.dY = 0
            bool_ = 0
        cz.d[1] = cz.c = 0
        cz.d[0] = cz.c = 0
        cz.e[1] = 0
        cz.e[0] = 0
        cz.f[1] = 0
        cz.f[0] = 0
        cz.O = 0
        cz.N = 20
        cz.L = 0
        cz.T = 0
        cz.H = 0
        cz.I = 0
        cz.A = 0
        cz.B = 0
        cz.C = 0
        cz.D = 0
        cz.R = 0
        ag.O_v()
        if ag.bi:
            cz.E = 500000
            cz.y = cz.p = cz.o = cz.m = cz.w = cz.n = cz.x = cz.z = cz.r = cz.q = 2000
        ag.fh = 0
        ag.fg = 1
        ag.cR.a = 0
        ag.dT.a = 0
        ag.dU.a = 0
        ag.ek = 0
        ag.eB = 0
        ag.eX = None
        ag.fa = None
        ag.fd = None
        for b in range(2):
            if ag.et[b] is None:
                ag.et[b] = self.K_I(82 + b)
        self.h_I(bool_)
        self.A_v()
        ag.eS[cz.K] = self.K_I(87 + (cz.K << 2))
        cz.aD = heroes.head_frames(self, cz.aB, 1)    # PORT-EXTRA heroes 4..9
        cz.aF = self.K_I(46)
        ag.eT[cz.K] = self.K_I(89 + (cz.K << 2))
        ag.ct[40 + cz.K] = self.d_T(ag.bB.a_I(42 + cz.K))
        ag.eU = self.K_I(86)
        self.z_v()
        ag.eQ = self.K_I(98)
        ag.eR = self.d_T(ag.bC.a_I(44))
        ag.eV = self.K_I(55)
        ag.ct[43] = self.d_T(ag.bC.a_I(0))
        ag.eW = self.K_I(56)
        ag.ct[44] = self.d_T(ag.bC.a_I(1))
        ag.ct[31] = self.d_T(ag.bA.a_I(52))
        ag.eq = self.d_T(ag.bB.a_I(45))
        ag.dW[1] = ag.B_v()
        ag.dW[0] = ag.B_v()
        ag.dV = ag.dW[0] - ag.dV
        ag.dW[1] = ag.B_v()
        ag.dV = ag.dW[0] = ag.B_v()
        ag.dj = 1
        ag.dX = 0

    def z_v(self):  # ag.java:969-971
        ag.ct[42] = self.d_T(ag.bC.a_I(2))

    def A_v(self):  # ag.java:973-988  (enemy sprites, recoloured by dz.d)
        arrayOfInt = [56, 57]
        for b in range(len(arrayOfInt)):
            if ag.dz[ag.dm].d != 0:
                ag.es[b] = None
                ag.et[b] = None
                ag.es[b] = ag.a_TI(ag.bB.a_I(arrayOfInt[b]), ag.dz[ag.dm].d)
            else:
                ag.es[b] = None
                ag.et[b] = None
                ag.es[b] = self.d_T(ag.bB.a_I(arrayOfInt[b]))
            if ag.et[b] is None:
                ag.et[b] = self.K_I(82 + b)

    _PAL = [[[236, 211, 197], [205, 143, 128], [129, 81, 69], [104, 60, 49], [79, 39, 29]],
            [[226, 205, 178], [196, 179, 152], [180, 142, 122], [135, 111, 47], [93, 73, 49]],
            [[174, 225, 242], [101, 156, 195], [61, 102, 139], [43, 78, 115], [45, 45, 84]],
            [[162, 199, 159], [135, 156, 119], [86, 123, 98], [33, 98, 63], [51, 51, 51]]]

    @staticmethod
    def a_TI(paramString, paramInt):  # ag.java:990-1023  (PNG with palette 0 replaced by palette paramInt)
        str_ = "/" + paramString + ".png"
        arrayOfByte = bytearray(j.a(str_))
        if paramInt == 0:
            return Image.createImage(arrayOfByte, 0, len(arrayOfByte))
        arrayOfInt = ag._PAL
        m = len(arrayOfByte)
        i1 = 0
        for j_ in range(0, m - 4 + 1):
            if arrayOfByte[j_] == 80 and arrayOfByte[j_ + 1] == 76 and arrayOfByte[j_ + 2] == 84 and arrayOfByte[j_ + 3] == 69:
                i1 = j_
                break
        i2 = arrayOfByte[i1 - 1] & 0xFF | arrayOfByte[i1 - 2] << 8 & 0xFF00
        for b in range(5):
            for j_ in range(i1 + 4, i1 + i2 - 3 + 1):
                if (arrayOfByte[j_] == arrayOfInt[0][b][0] and arrayOfByte[j_ + 1] == arrayOfInt[0][b][1]
                        and arrayOfByte[j_ + 2] == arrayOfInt[0][b][2]):
                    arrayOfByte[j_] = arrayOfInt[paramInt][b][0]
                    arrayOfByte[j_ + 1] = arrayOfInt[paramInt][b][1]
                    arrayOfByte[j_ + 2] = arrayOfInt[paramInt][b][2]
                    break
        l1 = x.a_ABII(arrayOfByte, i1, i2 + 4)
        arrayOfByte[i1 + i2 + 4] = l1 >> 24 & 0xFF
        arrayOfByte[i1 + i2 + 5] = l1 >> 16 & 0xFF
        arrayOfByte[i1 + i2 + 6] = l1 >> 8 & 0xFF
        arrayOfByte[i1 + i2 + 7] = l1 & 0xFF
        return Image.createImage(arrayOfByte, 0, len(arrayOfByte))

    def h_I(self, paramInt):  # ag.java:1025-1037  (load the map of the current lord, room around the hero)
        from pow.game.c import c
        self.d_III(0, 0, 0)
        ct34 = ag.ct[34]
        self.a_MIIIIII(ct34, ag.bZ.a // 2 - ct34.getWidth() // 2, ag.bZ.b // 2 - ct34.getHeight() // 2,
                       ct34.getWidth(), ct34.getHeight(), 0, 0)
        ag.ck = 1
        c.f_v()
        ag.cd = idiv(ag.cz.b[0].a - 1, 7) * 7 + 4 - (ag.cb.a >> 1)
        ag.ce = idiv(ag.cz.b[0].b - 1, 7) * 7 + 4 - (ag.cb.b >> 1)
        ag.cz.b[1].a = ag.cz.b[0].a
        ag.cz.b[1].b = ag.cz.b[0].b
        ag.cE = ag.bd.b_I(ag.cg)
        ag.bd.a_I(ag.ds[ag.dk])
        ag.bd.a_IIIII(ag.cb.a, ag.cb.b, ag.cd, ag.ce, paramInt)

    def ab_v(self):  # ag.java:2271-2275  (HUD frame pieces)
        arrayOfInt = [79, 61, 82, 78, 83, 81]
        for b in range(6):
            ag.cx[b] = self.d_T(ag.bA.a_I(arrayOfInt[b]))

    def g_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:2793-2795  (one digit of ct[19])
        self.b_MIIIIII(ag.ct[19], paramInt2, paramInt3, 10, 14, 10 * paramInt1, 0)

    @staticmethod
    def D_I(paramInt):  # ag.java:2842-2847  (number of decimal digits)
        b = 1
        j_ = 10
        while paramInt >= j_:
            b += 1
            j_ *= 10
        return b

    def j_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:2849-2855  (mission clock mm:ss)
        arrayOfInt1 = [0, 9, 25, 34]
        arrayOfInt2 = [idiv(paramInt3, 600) % 10, idiv(paramInt3, 60) % 10, paramInt3 % 60 // 10, paramInt3 % 10]
        for b in range(4):
            self.g_III(arrayOfInt2[b], paramInt1 + arrayOfInt1[b] + 10, paramInt2)
        self.b_MIIIIII(ag.ct[19], paramInt1 + 20 + 10, paramInt2, 4, 14, 115, 0)

    def al_(self):  # ag.java:2548-2570  (free the map images; `al` would hide the al class)
        ag.aj()
        ag.ct[4] = None
        if ag.bT is not None:
            for b1 in range(len(ag.bT)):
                ag.bT[b1] = None
            ag.bT = None
        ag.ct[9] = None
        ag.ct[11] = None
        ag.ct[12] = None
        ag.ct[16] = None
        ag.bb.d_v()
        for b in range(5):
            ag.ct[35 + b] = None
        for b in range(4):
            ag.ct[21 + b] = None
        ag.bY.a = ag.bZ.a
        ag.bY.b = ag.bZ.b
        ag.db = 0
        ag.dc = 0

    def am(self):  # ag.java:2572-2582  (start a dialogue: briefing dG 0, map talk 1, general 2)
        ag.dK = 0
        ag.dP = 0
        ag.dQ = 0
        ag.dR = 0
        ag.dS = 0
        ag.ao()
        self.an()
        if ag.dI < 200:
            self.z_I(ag.dI)

    def z_I(self, paramInt):  # ag.java:2584-2637  (line paramInt of dialogue file 57+dG -> dp[dR])
        arrayOfByte1 = None
        str1 = ""
        arrayOfInt = [0] * 60
        arrayOfString = [None, None]
        s = ag.dR
        if (ag.dK & 0x1) != 0:
            if ag.dG == 0:
                str1 = ag.dA[ag.dm]
            elif ag.dG in (2, 1):
                if ag.dG == 2:          # case 2 falls through into case 1
                    if ag.cr != 0:
                        self.B_I(ag.dz[ag.dm].f)
                    else:
                        self.B_I(ag.eO[ag.eP].o)
                str1 = ag.dC.a
        else:
            str1 = ag.cz.k
        arrayOfByte2 = arrayOfByte1 = ag.v_I(57 + ag.dG)
        j_ = arrayOfByte2[0] & 0xFF | arrayOfByte2[1] << 8 & 0xFF00
        for b1 in range(j_ + 1):
            arrayOfInt[b1] = arrayOfByte2[2 + b1 * 2] & 0xFF | arrayOfByte2[2 + b1 * 2 + 1] << 8 & 0xFF00
        arrayOfString[0] = ag.a_ABII(arrayOfByte2, arrayOfInt[paramInt], arrayOfInt[paramInt + 1])
        arrayOfString[1] = "[" + str1 + "] "
        ag.dD = len(arrayOfString[0])
        m = 0
        for b1 in range(ag.dD):
            if arrayOfString[0][b1] == '&':
                if m != b1:
                    # System.arraycopy(String[], m, String, ...) would throw in Java; the game
                    # only prints this marker, so the texts never have '&' after other text
                    ag.b_T("=========================check this 96430jfds")
                arrayOfString[1] = arrayOfString[1] + str1
                m = b1 + 1
        str2 = ""
        for b2 in range(len(arrayOfString[0])):
            if arrayOfString[0][b2] != '&':
                str2 = str2 + arrayOfString[0][b2]
        arrayOfString[0] = str2
        if m < ag.dD:
            arrayOfString[1] = arrayOfString[1] + arrayOfString[0]
        self.b_ABII(bytearray(arrayOfString[1].encode("utf-8")), 150, s)

    def an(self):  # ag.java:2639-2681  (first line dI of the dialogue)
        from pow.game.e import e
        v = ag.dG
        if v == 0:
            if ag.dH > 10:
                ag.dH = 11
                ag.dI = i16(ag.g_II(0, 18) + 10 << 1)
                return
            ag.dI = i16(ag.dH - 1 << 1)
            return
        if v == 1:
            j_ = 0
            e.b_II(ag.dJ, -5)
            ag.dI = 21
            return
        if v == 2:
            if ag.cr != 0:
                j_ = ag.dz[ag.dm].f
            else:
                j_ = ag.eO[ag.eP].o
            if 0 == j_:
                ag.ck = 1
                self.w_I(2)
                self.F_v()
                ag.cM[0] = 0
                ag.cN = ae.v[ag.cM[0]]
                ag.dE = ag.fU
                ag.dI = 200
                ag.bV = 2
                ag.cL = 0
                ag.cK = 0
                return
            e.b_II(j_, 5)
            ag.fq = j_
            j_ = ag.A_I(j_)
            if j_ >= 100:
                j_ = 95
            ag.dI = i16(j_ // 10 * 5)

    @staticmethod
    def A_I(paramInt):  # ag.java:2683-2687  (friendship points of general paramInt)
        b = 0
        while b < ag.fo and ag.fn[0][b] != paramInt:
            b += 1
        return 0 if b == ag.fo else ag.fn[1][b]

    @staticmethod
    def ao():  # ag.java:2689-2703  (position of the next speech box)
        ag.dK = i16(ag.dK + 1)
        if ag.dG != 0:
            ag.dL[ag.dR] = 60
            ag.dM[ag.dR] = i16(ag.bY.b - 39)
        elif (ag.dK & 0x1) != 0:
            ag.dL[ag.dR] = i16(ag.dd - 60 + 15 + 2)
            ag.dM[ag.dR] = i16(ag.de - 64)
        else:
            ag.dL[ag.dR] = i16(ag.dd - 60 + -40 + 2)
            ag.dM[ag.dR] = i16(ag.de - 73 + 107 + 2)
        ag.dO = 0
        ag.dN = ag.dL[ag.dR]

    def B_I(self, paramInt):  # ag.java:2705-2726  (general paramInt -> dC)
        arrayOfByte = None
        j_ = 0
        arrayOfByte = ag.v_I(46)
        j_ = 23 * (paramInt - 1) + 14
        dC = ag.dC
        dC.a = ""
        b = 0
        while b < 11 and arrayOfByte[j_ + b] != 0:
            b += 1
        dC.a = ag.a_ABII(arrayOfByte, j_, j_ + b)
        dC.b = _jchar(arrayOfByte[j_ + 11])
        dC.c = _jchar(arrayOfByte[j_ + 11 + 2])
        dC.d[0] = _jchar(arrayOfByte[j_ + 11 + 3])
        dC.d[1] = _jchar(arrayOfByte[j_ + 11 + 4])
        dC.d[2] = _jchar(arrayOfByte[j_ + 11 + 5])
        dC.d[3] = _jchar(arrayOfByte[j_ + 11 + 6])
        dC.e = _jchar(arrayOfByte[j_ + 11 + 7])
        dC.f = _jchar(arrayOfByte[j_ + 11 + 8])
        dC.g = _jchar(arrayOfByte[j_ + 11 + 9])
        dC.h = _jchar(arrayOfByte[j_ + 11 + 10])
        dC.i = _jchar(arrayOfByte[j_ + 11 + 11])
        dC.c = dC.c + 1 & 0x1

    def p_I(self, paramInt):  # ag.java:1494-1505  (random skill of general dC)
        b = 0
        while b < 4 and 0 != ag.dC.d[b]:
            b += 1
        if paramInt != 0:
            while True:
                c1 = ag.dC.d[self.C_I(b)]
                if not c1 > 0o20:
                    return c1
        return ag.dC.d[self.C_I(b)]



def _arraycopy(src, srcPos, dest, destPos, length):
    """System.arraycopy (throws on a negative length or out-of-range, like Java)."""
    if length < 0 or srcPos < 0 or destPos < 0 or srcPos + length > len(src) or destPos + length > len(dest):
        raise IndexError("arraycopy %d %d %d" % (srcPos, destPos, length))
    dest[destPos:destPos + length] = src[srcPos:srcPos + length]


def _jchar(b):
    """(char) of a Java byte: sign-extended to 16 bits."""
    return i8(b) & 0xFFFF


def _late_init():
    """Static initialisers that create ag subclasses (ag.java:206  `cS = new l()`)."""
    from pow.game.l import l
    ag.cS = l()
