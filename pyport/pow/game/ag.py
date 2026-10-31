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
from pow.game.j import j
from pow.game.structs import ac, ai, ao, t, z
from pow.game.x import x
from pow.midp import system
from pow.midp.canvas import Canvas
from pow.midp.graphics import Image
from pow.midp.jint import i8, i16, i32
from pow.midp.rms import RecordStore


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
        from pow.game.stubs import ar_stub, as_stub, c_stub, m_stub
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
        ag.be = as_stub()          # NOT-PORTED: as.java (Gamevil Live) - phase 7
        as_stub.a = m_stub()
        ag.bb = e()
        ag.bc = ar_stub()          # NOT-PORTED: ar.java (map logic) - phase 3
        ag.bd = c_stub()           # NOT-PORTED: c.java (map & combat) - phase 3/4

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
            not_ported("as.t (Gamevil Live keys)")

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
                ag.be.i()
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
                if ag.bV == 2:
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
            # if (be != null) as.aJ();   NOT-PORTED (Gamevil Live)
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
                not_ported("bc.b(1) (map)")
            elif v == 4:
                not_ported("bc.k() (map)")
            elif v == 5:
                not_ported("ag.L case 5 (map)")
            elif v in (6, 8, 9):
                return
            elif v == 10:
                not_ported("ag.L case 10 (story player)")
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
        if v in (3, 4, 5):
            not_ported("ag.L ck=0 bV=%d (map)" % v)
        if v in (6, 8, 9):
            return
        if v == 10:
            not_ported("ag.L ck=0 bV=10 (story player)")

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
        elif v in (3, 4, 5):
            not_ported("ag.P bV=%d (map/combat)" % v)
        elif v == 10:
            if ag.cS.b != 0:
                ag.cS.b_v()
            self.L_v()
        elif v == 11:
            not_ported("as.aK (Gamevil Live)")
        # if (be != null && as.gu) be.j();   - Gamevil Live overlay, as.gu is always false offline
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
            cz.m = ag.X_v()
            cz.n = ag.X_v()
            cz.o = ag.X_v()
            cz.p = ag.X_v()
            cz.q = ag.X_v()
            cz.r = ag.X_v()
            cz.E = ag.W_v()
            if ag.bi:
                cz.E = 555000
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
        ag.cz.aG = self.d_T(ag.bB.a_I(46 + ag.cz.aB))
        ag.cz.aC = self.K_I(47 + ag.cz.aB)
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


def _late_init():
    """Static initialisers that create ag subclasses (ag.java:206  `cS = new l()`)."""
    from pow.game.l import l
    ag.cS = l()
