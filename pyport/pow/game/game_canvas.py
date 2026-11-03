"""ag.java - the main Canvas class (game loop, state machine, shared helpers).

Literal port, Phase 0 subset: everything on the path
logo -> "sound?" -> title -> Main Menu -> Game Menu.
Method names follow pyport/NAMES.md (signature suffix when the Java name is overloaded).
Every method has a `# ag.java:FROM-TO` comment. Methods that are not ported yet raise
NotPorted so a missing piece is loud, not silent.
"""
import traceback

import config
from pow.game import consts
from pow.game.game_fields import GameFields
from pow.game.scr_table import _read_utf, ScrTable
from pow.game.font import Font
from pow.game.res_reader import ResReader
from pow.game.structs import GearDef, Item, RareDef, Rect, SpriteFrame, TreasureDef
from pow.game.gfx import Gfx
from pow.midp import system
from pow.midp.canvas import Canvas
from pow.midp.graphics import Image
from pow.midp.jint import i8, i16, i32, idiv, imod
from pow.midp.rms import RecordStore
from pow.game.arr_table import ArrTable

F10 = config.DECOMP_FIX["F10"]
F12 = config.DECOMP_FIX["F12"]
F13 = config.DECOMP_FIX["F13"]


class NotPorted(NotImplementedError):
    pass


def not_ported(where):
    raise NotPorted(where + " is not ported yet (later phase)")


class GameCanvas(GameFields, Canvas):

    def __init__(self, paramMain):  # ag.java:560-564
        Canvas.__init__(self)
        GameCanvas.bs = paramMain
        self.gj = False  # public boolean gj = false;  ag.java:552 (instance field)
        self.setFullScreenMode(True)
        self.r_v()

    @staticmethod
    def q_v():  # ag.java:566-576
        GameCanvas.cg = 1
        GameCanvas.ch = -999
        GameCanvas.ck = 1
        GameCanvas.cq = 0
        GameCanvas.cs[4] = -1
        GameCanvas.cs[3] = -1
        GameCanvas.cs[2] = -1
        GameCanvas.cs[1] = -1
        GameCanvas.cs[0] = -1

    def r_v(self):  # ag.java:578-583
        GameCanvas.bJ = self.getWidth()
        GameCanvas.bK = self.getHeight()
        GameCanvas.bL = GameCanvas.bJ // 2
        GameCanvas.bM = GameCanvas.bK // 2

    def s_v(self):  # ag.java:585-658
        from pow.game.menus import Menus
        from pow.game.sound import Sound
        from pow.game.map_scene import MapScene
        from pow.game.live import Live
        from pow.game.live_screen import LiveScreen
        from pow.game.map_engine import MapEngine
        from pow.midp.jrandom import Random
        self.r_v()
        GameCanvas.bu = Font("/0_font.png", 8, 17, 9, 16777215)
        GameCanvas.bv = Font("/0_font.png", 8, 17, 9, 0)
        GameCanvas.bw = Font("/0_font.png", 8, 17, 9, 16400640)
        GameCanvas.bx = Font("/0_font.png", 8, 17, 9, 6579300)
        GameCanvas.bA = ScrTable("/imgui.scr")
        GameCanvas.bE = ScrTable("/edat.scr")
        GameCanvas.bF = ScrTable("/mdat_QVGA.scr")
        GameCanvas.bB = ScrTable("/imgchar.scr")
        GameCanvas.bC = ScrTable("/imgeff.scr")
        GameCanvas.bD = ScrTable("/imgtile.scr")
        GameCanvas.bG = ScrTable("/gamestr.scr")
        GameCanvas.q_v()
        GameCanvas.bh = GameCanvas.bs.getAppProperty("MIDlet-Version") or ""
        GameCanvas.bk = GameCanvas.bs.getAppProperty("GAMEVIL_SERVER") or "ur.gamevil.net"
        try:
            GameCanvas.bl = int(GameCanvas.bs.getAppProperty("GAMEVIL_PORT"))
        except Exception:
            GameCanvas.bl = 28230
        GameCanvas.bm = GameCanvas.bs.getAppProperty("GAMEVIL_MOREGAMES") or "http://usaapp1.gamevil.net/moregames/index2.php?bid=POW_"
        GameCanvas.bn = GameCanvas.bs.getAppProperty("GAMEVIL_MULTIPLAY") or "http://ur.gamevil.net/moregames/pow_multiplayer.php"
        GameCanvas.bi = GameCanvas.bs.getAppProperty("GAMEVIL_CHEAT") == "TRUE"
        GameCanvas.bj = False
        GameCanvas.bZ.a = i16(GameCanvas.bJ)
        GameCanvas.bZ.b = i16(GameCanvas.bK)
        GameCanvas.bY.a = i16(GameCanvas.bJ)
        GameCanvas.bY.b = i16(GameCanvas.bK)
        GameCanvas.db = 0
        GameCanvas.dc = 0
        GameCanvas.dd = GameCanvas.bY.a >> 1
        GameCanvas.de = GameCanvas.bY.b >> 1
        if GameCanvas.bK % 2 == 1:
            GameCanvas.de += 1
        GameCanvas.x_v()
        GameCanvas.bV = 0
        GameCanvas.ck = 1
        GameCanvas.dr = 0
        GameCanvas.G_v()
        GameCanvas.cz.a_v()
        GameCanvas.by = Random()
        GameCanvas.bU = self.d_T("softbg")
        GameCanvas.bg = Sound(GameCanvas.bs)
        GameCanvas.be = Live()
        Live.a = LiveScreen()
        GameCanvas.bb = Menus()
        GameCanvas.bc = MapEngine()               # ar.java: the map (phase 3); the combat parts raise NotPorted
        GameCanvas.bd = MapScene()                # c.java: story player, map; the combat parts raise NotPorted

    def keyPressed(self, paramInt):  # ag.java:660-662
        self.t_I(paramInt)

    def t_v(self):  # ag.java:664-685
        if GameCanvas.ch == -999:
            return
        if GameCanvas.bS:
            if GameCanvas.ch == -5 or GameCanvas.ch == 53:
                self.a_Z(False)
            GameCanvas.ch = -999
            return
        if GameCanvas.bV == 0:
            if GameCanvas.bf is not None:
                GameCanvas.bf.b_v()
                return
        elif GameCanvas.bV == 11:
            from pow.game.live import Live
            if not Live.gu:
                GameCanvas.be.t_I(GameCanvas.ch)

    @staticmethod
    def b_T(paramString):  # ag.java:687-689
        print(" " + paramString)

    def paint(self, paramGraphics):  # ag.java:691-706  (synchronized)
        GameCanvas.gg = False
        GameCanvas.br = paramGraphics
        Gfx.a_G(paramGraphics)
        if GameCanvas.bS:
            Gfx.b_IIIII(0, 0, GameCanvas.bJ, GameCanvas.bK, 0)
            GameCanvas.cS.b_I(10)
            Gfx.a_Lg(GameCanvas.bu)
            j_ = GameCanvas.de - 5 - 10
            Gfx.a_TIII("RESUME", GameCanvas.bL, j_ + GameCanvas.dc + 7, 1)
            GameCanvas.gg = True
            return
        self.P_v()
        GameCanvas.gg = True

    async def run(self):  # ag.java:708-760  (Thread.run -> async loop for pygbag)
        self.s_v()
        GameCanvas.gi = system.currentTimeMillis()
        while GameCanvas.gh and not self.quit_requested:
            try:
                GameCanvas.gi = system.currentTimeMillis()
                if GameCanvas.bS:
                    self.t_v()
                    self.repaint(0, 0, GameCanvas.bJ, GameCanvas.bK)
                    self.serviceRepaints()
                    GameCanvas.ch = -999
                    if GameCanvas.bQ:
                        self.b_Z(GameCanvas.bR)
                        GameCanvas.bQ = False
                    await self.sleep_ms(100)
                    continue
                if GameCanvas.bX != GameCanvas.bV:
                    GameCanvas.ch = -999
                else:
                    GameCanvas.ch = GameCanvas.ci
                GameCanvas.ci = -999
                GameCanvas.bN = i32(GameCanvas.bN + 1)
                if GameCanvas.bN < 0:
                    GameCanvas.bN = 0
                if GameFields.a > 0:   # private static int a  (ag.java:98)
                    GameFields.a -= 1
                self.t_v()
                if GameCanvas.bg is not None:
                    GameCanvas.bg.a_v()
                self.u_v()
                GameCanvas.be.i_v()
                GameCanvas.ch = -999
                if GameCanvas.bQ:
                    self.b_Z(GameCanvas.bR)
                    GameCanvas.bQ = False
                l1 = system.currentTimeMillis()
                j_ = (consts.aQ[GameCanvas.dh] if GameCanvas.bV == 3 else consts.aQ[2]) - int(l1 - GameCanvas.gi)
                if j_ > 20:
                    await self.sleep_ms(j_)
                else:
                    await self.sleep_ms(20)
                if GameCanvas.bN > 2:
                    GameCanvas.bq = True
                GameCanvas.bX = GameCanvas.bV
            except NotPorted as np_:
                # Spike convenience: a screen of a later phase shows a popup and returns
                # to the menu instead of killing the game (config.STRICT = re-raise).
                if config.STRICT:
                    raise
                print("NotPorted:", np_)
                if GameCanvas.bV in (3, 4, 5):
                    # the map / combat states have no screen yet: back to the Game Menu the
                    # way the game itself returns there (e.java:1288-1300)
                    self.w_I(2)
                    self.F_v()
                    GameCanvas.cM[0] = 0
                    GameCanvas.cN = consts.v[0]
                    GameCanvas.dE = GameCanvas.fU
                    GameCanvas.bV = 2
                    GameCanvas.cL = 0
                    GameCanvas.cK = 0
                    GameCanvas.ck = 1
                elif GameCanvas.bV == 2:
                    GameCanvas.cM[0] = GameCanvas.cO if GameCanvas.cM[0] not in (0, 5) else GameCanvas.cM[0]
                    GameCanvas.ap()
                GameCanvas.cS.a_T("3Not ported yet|(later phase)")
                await self.sleep_ms(20)
            except Exception as exception:
                GameCanvas.b_T("--run:" + repr(exception))
                if config.DEBUG:
                    traceback.print_exc()
                    raise
                await self.sleep_ms(20)

    def u_v(self):  # ag.java:762-767
        self.repaint()
        self.serviceRepaints()
        while not GameCanvas.gg:
            GameCanvas.f_I(20)

    @staticmethod
    def f_I(paramInt):  # ag.java:769-777
        system.sleep(paramInt)

    def hideNotify(self):  # ag.java:779-781
        self.a_Z(True)

    def showNotify(self):  # ag.java:783-785
        self.a_Z(True)

    def a_Z(self, paramBoolean):  # ag.java:787-799
        from pow.game.midlet import Midlet
        if paramBoolean and GameCanvas.bV == 3:
            self.gj = True
        elif not paramBoolean:
            self.gj = False
        if GameCanvas.bS == paramBoolean or GameFields.b or GameFields.a > 0:
            return
        if not Midlet.c or not GameCanvas.bq:
            return
        GameCanvas.bQ = True
        GameCanvas.bR = paramBoolean

    def b_Z(self, paramBoolean):  # ag.java:801-818
        from pow.game.sound import Sound
        GameCanvas.bS = paramBoolean
        if GameCanvas.bS:
            GameCanvas.ch = -999
            if GameCanvas.bg is not None:
                Sound.a.c_v()
                return
        else:
            GameCanvas.f_I(300)
            GameCanvas.ck = 1
            if GameCanvas.be is not None:
                from pow.game.live import Live
                Live.aJ()
            Sound.a.d_v()
            if GameCanvas.bV == 2 and GameCanvas.cM[0] == 4:
                GameCanvas.ck = 2

    @staticmethod
    def v_v():  # ag.java:820-822
        GameFields.b = True

    @staticmethod
    def w_v():  # ag.java:824-827
        GameFields.b = False
        GameFields.a = 3

    @staticmethod
    def x_v():  # ag.java:829-865
        for b in range(2):
            GameCanvas.er[b] = None
        for b in range(9):
            GameCanvas.et[b] = None
        for b in range(len(GameCanvas.ct)):
            GameCanvas.ct[b] = None
        GameCanvas.eT[1] = None
        GameCanvas.eT[0] = None
        GameCanvas.eS[1] = None
        GameCanvas.eS[0] = None
        GameCanvas.eU = None
        GameCanvas.eR = None
        GameCanvas.eV = None
        GameCanvas.eW = None
        GameCanvas.eY = None
        GameCanvas.fb = None
        GameCanvas.fe = None
        GameCanvas.cE.a = None
        GameCanvas.dU.g = None
        GameCanvas.dU.h = None
        GameCanvas.cz.aC = GameCanvas.cz.aE = None
        GameCanvas.cz.aG = None
        GameCanvas.cz.aH = None
        GameCanvas.cU = GameCanvas.cW = GameCanvas.cV = None
        GameCanvas.ep = 0
        GameCanvas.cS.b = 0
        GameCanvas.dh = 2
        for b in range(30):
            GameCanvas.cP[b] = 0
            GameCanvas.cQ[b] = 0
        GameCanvas.cX = GearDef()
        GameCanvas.cY = TreasureDef()
        GameCanvas.cZ = RareDef()

    @staticmethod
    def a_IIT(paramInt1, paramInt2, paramString):  # ag.java:1144-1147
        if paramString is not None:
            Gfx.a_TIII(paramString, paramInt1, paramInt2, 0)

    @staticmethod
    def b_IIT(paramInt1, paramInt2, paramString):  # ag.java:1149-1152
        if paramString is not None:
            Gfx.a_TIII(paramString, paramInt1, paramInt2, 1)

    def E_v(self):  # ag.java:1154-1163  (title picture = title_1..4 stacked)
        if GameCanvas.ct[30] is None:
            GameCanvas.ct[30] = Image.createImage(240, 320)
            graphics = GameCanvas.ct[30].getGraphics()
            for b in range(4):
                image = self.d_T("title_" + str(b + 1))
                graphics.drawImage(image, 0, 80 * b, 20)

    def F_v(self):  # ag.java:1165-1172
        GameCanvas.cy = 0
        while GameCanvas.cy < 4:
            GameCanvas.ct[26 + GameCanvas.cy] = self.d_T(GameCanvas.bA.a_I(73 + GameCanvas.cy))
            GameCanvas.cy += 1
        self.ad_v()

    @staticmethod
    def G_v():  # ag.java:1174-1186
        arrayOfByte = bytearray(2)
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_env", False)
            if recordStore is None or recordStore.getNumRecords() < 1:
                return
            arrayOfByte = recordStore.getRecord(1)
            GameCanvas.cG = len(arrayOfByte)
        except Exception:
            pass
        if GameCanvas.cG >= 2:
            GameCanvas.dg = i8(arrayOfByte[0])
            GameCanvas.dh = i8(arrayOfByte[1])

    @staticmethod
    def H_v():  # ag.java:1188-1201
        arrayOfByte = bytearray(2)
        arrayOfByte[0] = GameCanvas.dg & 0xFF
        arrayOfByte[1] = GameCanvas.dh & 0xFF
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_env", True)
            if recordStore.getNumRecords() == 0:
                recordStore.addRecord(arrayOfByte, 0, len(arrayOfByte))
            recordStore.setRecord(1, arrayOfByte, 0, len(arrayOfByte))
        except Exception:
            return

    @staticmethod
    def I_v():  # ag.java:1203-1210
        if GameCanvas.cM[1] < GameCanvas.cM[2]:
            GameCanvas.cM[2] = GameCanvas.cM[1]
            return
        if GameCanvas.cM[1] > GameCanvas.cM[2] + 4:
            GameCanvas.cM[2] = GameCanvas.cM[1] - 4

    def a_MIIIIII(self, paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # ag.java:1212-1214
        GameCanvas.a_IIIIMII(paramInt1, paramInt2, paramInt3, paramInt4, paramImage, paramInt5, paramInt6)

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
        Gfx.a_TIII(paramString, paramInt1, paramInt2, 0)

    @staticmethod
    def a_BB(paramByte1, paramByte2):  # ag.java:1275-1277
        return i16(paramByte1 & 0xFF | (paramByte2 & 0xFF) << 8)

    def K_v(self):  # ag.java:1418-1431
        if GameCanvas.cl == 0:
            self.c_III(0, 0, 0)
            self.a_MIIIIII(GameCanvas.ct[7], GameCanvas.db, GameCanvas.dc, GameCanvas.bY.a, GameCanvas.bY.b, GameCanvas.cc.a, GameCanvas.cc.b)
            return
        if GameCanvas.cl == 1:
            self.c_III(0, 0, 0)
            return
        if GameCanvas.cl == 2:
            self.c_III(255, 255, 255)

    def c_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:1433-1435
        Gfx.b_IIIII(GameCanvas.db, GameCanvas.dc, GameCanvas.bY.a, GameCanvas.bY.b, GameCanvas.k_III(paramInt1, paramInt2, paramInt3))

    def L_v(self):  # ag.java:1522-1610
        # DECOMP-FIX F8: the decompiled switch at ag.java:1526-1546 has no `break`s, so every case
        # would fall through into the next (bV==0 would also run bb.a(1), bc.b(1), ...).
        # The original had one branch per state.
        if GameCanvas.ck == 1:
            GameCanvas.ck = 0
            v = GameCanvas.bV
            if v == 12:
                self.at()
            elif v == 0:
                GameCanvas.Q_v()
            elif v == 2:
                GameCanvas.bb.a_I(1)
            elif v == 3:
                GameCanvas.bc.b_I(1)
            elif v == 4:
                GameCanvas.bc.k_v()
            elif v == 5:
                self.K_v()
                for b in range(81):
                    GameCanvas.eE[b // 9][b % 9] = 1
                GameCanvas.bd.c_v()
                GameCanvas.bb.h_v()
            elif v in (6, 8, 9):
                return
            elif v == 10:
                if (GameCanvas.ec == 0 and GameCanvas.fD < GameCanvas.eb[1] - GameCanvas.eb[0]) or (GameCanvas.ec != 0 and GameCanvas.fD >= GameCanvas.eb[1] - GameCanvas.eb[0]):
                    from pow.game.menus import Menus
                    GameCanvas.bb.e_v()
                    Gfx.a_Lg(GameCanvas.bu)
                    if GameCanvas.ec != 0:
                        self.b_TII("Prologue", 2 - GameCanvas.dc, 9)
                    else:
                        self.b_TII("Epilogue", 2 - GameCanvas.dc, 9)
                    GameCanvas.bb.b_I(GameCanvas.fE)
                    if GameCanvas.fA[0] > 0:
                        Menus.a_III(0, 0, 1)
                    if GameCanvas.fA[1] > 0:
                        Menus.a_III(1, 0, 1)
                    self.q_I(1)
                else:
                    self.N_v()
                if GameCanvas.cS.b != 0:
                    GameCanvas.cS.c_v()
            return
        if GameCanvas.ck == 2:
            if GameCanvas.bV == 2:
                GameCanvas.bb.a_I(2)
                return
            return
        v = GameCanvas.bV
        if v == 0:
            GameCanvas.Q_v()
            return
        if v == 2:
            GameCanvas.bb.a_I(0)
            return
        if v == 3:
            GameCanvas.bc.b_I(0)
            return
        if v == 4:
            GameCanvas.bc.k_v()
            GameCanvas.bc.n_v()
            return
        if v == 5:
            GameCanvas.bb.i_v()
            return
        if v in (6, 8, 9):
            return
        if v == 10:
            if GameCanvas.cS.b != 0:
                if GameCanvas.cS.j != 0:
                    GameCanvas.cS.c_v()
                    return
            self.M_v()

    def a__I(self, paramInt):  # ag.java:1882-1885
        if GameCanvas.bg is not None:
            GameCanvas.bg.a__I(paramInt)

    def P_v(self):  # ag.java:1887-1933
        from pow.game.sound import Sound
        v = GameCanvas.bV
        if v == 12:
            self.L_v()
            if system.currentTimeMillis() - GameCanvas.c > 3000:
                GameCanvas.bs.destroyApp(True)
                GameCanvas.bs.notifyDestroyed()
            return
        if v == 0:
            self.L_v()
        elif v == 2:
            if GameCanvas.bg is not None and GameCanvas.cM[0] < 29 and Sound.a_ != consts.A[GameCanvas.cM[0]] and GameCanvas.cM[0] != 20 and not GameCanvas.bp:
                self.a__I(consts.A[GameCanvas.cM[0]])
            if GameCanvas.cS.b != 0:
                GameCanvas.cS.b_v()
            else:
                GameCanvas.bb.a_v()
            self.L_v()
        elif v == 3:
            GameCanvas.bc.a_v()
        elif v in (4, 5):
            self.L_v()
            GameCanvas.bc.O_I(0)
        elif v == 10:
            if GameCanvas.cS.b != 0:
                GameCanvas.cS.b_v()
            self.L_v()
        elif v == 11:
            if GameCanvas.be is not None:
                from pow.game.live import Live
                Live.aK()
        if GameCanvas.be is not None:
            from pow.game.live import Live
            if Live.gu:
                GameCanvas.be.j_v()
        GameCanvas.cj = -999

    @staticmethod
    def Q_v():  # ag.java:1935-1939
        from pow.game.boot import Boot
        if GameCanvas.bf is None:
            GameCanvas.bf = Boot()
        GameCanvas.bf.a_v()

    def t_I(self, paramInt):  # ag.java:1941-1961
        if paramInt == -10:
            return
        if GameCanvas.bS:
            GameCanvas.ch = paramInt
            return
        GameCanvas.ci = paramInt
        if paramInt in (-4, -3, -2, -1, 50, 52, 54, 56):
            GameCanvas.cj = paramInt

    def d_T(self, paramString):  # ag.java:1963-1975
        GameCanvas.R_v()
        str_ = "/" + paramString + ".png"
        image = None
        try:
            image = Image.createImage(str_)
        except Exception:
            print("======== createMixImage failuer :" + paramString)
            return None
        GameCanvas.R_v()
        return image

    @staticmethod
    def R_v():  # ag.java:1977-1979  (System.gc)
        pass

    @staticmethod
    def u_I(paramInt):  # ag.java:1981-1983
        Gfx.b_IIIII(0, 0, GameCanvas.bJ, GameCanvas.bK, paramInt)

    def S_v(self):  # ag.java:1985-1996  (title screen)
        if GameCanvas.ct[30] is None:
            return
        GameCanvas.a_IIIIMII(0, 0, GameCanvas.bZ.a, GameCanvas.bZ.b, GameCanvas.ct[30], 0, 0)
        if GameCanvas.cv is None:
            GameCanvas.cv = self.d_T(GameCanvas.bA.a_I(36))
        GameCanvas.a_IIIIMII(GameCanvas.dd - 66 + GameCanvas.db, GameCanvas.bZ.b - 20, 132, 14, GameCanvas.cv, 0, 0)
        if GameCanvas.cw is None:
            GameCanvas.cw = self.d_T(GameCanvas.bA.a_I(42))
        if GameCanvas.bN % 6 < 3 and GameCanvas.bV == 0:
            GameCanvas.a_IIIIMII(GameCanvas.dd - 55 + GameCanvas.db, GameCanvas.bZ.b - 60, 110, 14, GameCanvas.cw, 0, 0)

    def a_TIIIIII(self, paramString, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # ag.java:1998-2002
        image = self.d_T(paramString)
        if image is not None:
            GameCanvas.a_IIIIMII(paramInt1, paramInt2, paramInt3, paramInt4, image, paramInt5, paramInt6)

    def T_v(self):  # ag.java:2004-2124  (title -> Main Menu)
        cz = GameCanvas.cz
        for b in range(8):
            q = consts.aT[b]
            cz.ac[b] = consts.B[q]
            cz.ad[b] = consts.C[q]
            cz.ak[b] = consts.D[q]
            cz.al[b] = consts.E[q]
            cz.ae[b] = consts.F[q]
            cz.af[b] = consts.G[q]
            cz.ag[b] = consts.H[q]
            cz.ah[b] = consts.I[q]
            cz.ai[b] = consts.J[q]
            cz.aj[b] = consts.K[q]
            cz.am[b] = consts.L
            cz.aA[b] = consts.M[q]
            cz.an[b] = consts.N[q]
            cz.ao[b] = consts.O[q]
            cz.ap[b] = consts.P[q]
            cz.aq[b] = consts.Q
            cz.ar[b] = consts.R[q]
            cz.as_[b] = consts.S[q]
            cz.at[b] = consts.T[q]
            cz.au[b] = consts.U
            cz.av[b] = consts.V[q]
            cz.aw[b] = consts.W[q]
            cz.ax[b] = consts.X
            cz.ay[b] = consts.Y
            cz.az[b] = consts.Z
            GameCanvas.eF[b][0] = consts.aa[q]
            GameCanvas.eF[b][1] = consts.ab[q]
            GameCanvas.eF[b][2] = consts.ac[q]
            GameCanvas.eF[b][3] = consts.ad[q]
            GameCanvas.eI[b] = GameCanvas.eF[b]
            GameCanvas.eG[b][0] = consts.ae[q]
            GameCanvas.eG[b][1] = consts.af[q]
            GameCanvas.eG[b][2] = consts.ag[q]
            GameCanvas.eG[b][3] = consts.ah[q]
            GameCanvas.eJ[b] = GameCanvas.eG[b]
            GameCanvas.eH[b][0] = consts.aa[q]
            GameCanvas.eH[b][1] = consts.ai[q]
            GameCanvas.eH[b][2] = consts.aj[q]
            GameCanvas.eH[b][3] = consts.ak
            GameCanvas.eH[b][4] = consts.ai[q]
            GameCanvas.eH[b][5] = consts.ai[q]
            GameCanvas.eH[b][6] = consts.N[q]
            GameCanvas.eH[b][7] = consts.O[q]
            GameCanvas.eH[b][8] = consts.P[q]
            GameCanvas.eH[b][9] = consts.Q
            GameCanvas.eH[b][10] = consts.Q
            GameCanvas.eH[b][11] = consts.Q
            GameCanvas.eH[b][12] = consts.Q
            GameCanvas.eH[b][13] = consts.Q
            GameCanvas.eH[b][14] = consts.R[q]
            GameCanvas.eH[b][15] = consts.S[q]
            GameCanvas.eH[b][16] = consts.T[q]
            GameCanvas.eH[b][17] = consts.U
            GameCanvas.eH[b][18] = consts.U
            GameCanvas.eH[b][19] = consts.V[q]
            GameCanvas.eH[b][20] = consts.W[q]
            GameCanvas.eH[b][21] = consts.W[q]
            GameCanvas.eK[b] = GameCanvas.eH[b]
        GameCanvas.eL[0] = GameCanvas.eI
        GameCanvas.eL[1] = GameCanvas.eJ
        GameCanvas.eL[2] = GameCanvas.eI
        GameCanvas.eL[3] = GameCanvas.eK
        ab = cz.ab
        (ab[0], ab[1], ab[2], ab[3], ab[4], ab[5], ab[6], ab[7], ab[8], ab[9]) = (
            cz.ac, cz.ad, cz.ak, cz.ae, cz.af, cz.ag, cz.ah, cz.ai, cz.aj, cz.al)
        (ab[10], ab[11], ab[12], ab[13], ab[14]) = (cz.am, cz.aA, cz.an, cz.ao, cz.ap)
        (ab[15], ab[16], ab[17], ab[18], ab[19]) = (cz.aq, cz.aq, cz.aq, cz.aq, cz.aq)
        (ab[20], ab[21], ab[22], ab[23], ab[24]) = (cz.ar, cz.as_, cz.at, cz.au, cz.au)
        (ab[25], ab[26], ab[27], ab[28], ab[29], ab[30]) = (cz.av, cz.aw, cz.aw, cz.ax, cz.ay, cz.az)
        GameCanvas.bY.a = 240
        GameCanvas.bY.b = 243
        GameCanvas.cb.a = i16(GameCanvas.bY.a // 27 + (1 if GameCanvas.bY.a % 27 > 0 else 0))
        GameCanvas.cb.a = i16(GameCanvas.cb.a + (0 if (GameCanvas.cb.a & 0x1) > 0 else 1))
        GameCanvas.cb.b = i16(GameCanvas.bY.b // 27 + (1 if GameCanvas.bY.b % 27 > 0 else 0))
        GameCanvas.cb.b = i16(GameCanvas.cb.b + (0 if (GameCanvas.cb.b & 0x1) > 0 else 1))
        GameCanvas.cc.a = i16(GameCanvas.cb.a * 27 - GameCanvas.bY.a >> 1)
        GameCanvas.cc.b = i16(GameCanvas.cb.b * 27 - GameCanvas.bY.b >> 1)
        GameCanvas.bY.a = GameCanvas.bZ.a
        GameCanvas.bY.b = GameCanvas.bZ.b
        GameCanvas.db = 0
        GameCanvas.dc = 0
        self.aa_v()
        GameCanvas.q_v()
        self.a__I(-1)
        GameCanvas.dj = 0
        self.w_I(0)
        GameCanvas.cM[0] = 5
        GameCanvas.cN = 10
        GameCanvas.cS.e = 0
        self.U_v()
        GameCanvas.bV = 2
        if not GameCanvas.aq():
            GameCanvas.cM[1] = 1

    def U_v(self):  # ag.java:2126-2214  (load save "gamevil_pow_data")
        cz = GameCanvas.cz
        GameCanvas.cG = 0
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_data", False)
            if recordStore is None or recordStore.getNumRecords() < 1:
                return
            GameCanvas.cF = recordStore.getRecord(1)
            GameCanvas.cG = GameCanvas.cF[0] & 0xFF | GameCanvas.cF[1] << 8 & 0xFF00
        except Exception:
            pass
        if GameCanvas.cG != 0:
            cF = GameCanvas.cF
            arrayOfByte1 = [0] * 16
            b2 = 0
            while b2 < 8 and cF[2 + b2] != 32:
                b2 += 1
            arrayOfByte2 = bytearray(b2)
            for b1 in range(b2):
                arrayOfByte2[b1] = cF[2 + b1]
            cz.k = GameCanvas.a_ABII(arrayOfByte2, 0, b2)
            GameCanvas.dj = i8(cF[18])
            GameCanvas.cG = 19
            GameCanvas.dk = GameCanvas.Y_v()
            GameCanvas.dm = GameCanvas.Y_v()
            GameCanvas.do = GameCanvas.Y_v()
            GameCanvas.dw = GameCanvas.V_v()
            GameCanvas.dx = GameCanvas.V_v()
            for b1 in range(8):
                GameCanvas.dy[b1] = GameCanvas.W_v()
            GameCanvas.dY = GameCanvas.W_v()
            GameCanvas.ed = GameCanvas.W_v()
            for b1 in range(44):
                GameCanvas.fn[0][b1] = GameCanvas.Y_v()
                GameCanvas.fn[1][b1] = GameCanvas.Y_v()
            GameCanvas.fo = GameCanvas.Y_v()
            for b1 in range(25):
                GameCanvas.fL[b1] = self.Z_v()
            GameCanvas.cq = GameCanvas.Y_v()
            cz.a[0].a = GameCanvas.X_v()
            cz.a[0].b = GameCanvas.X_v()
            # Java int division (values are positions >= 0, so // == /)
            cz.a[0].a = i16((cz.a[0].a // 27 // 7 * 7 + 4) * 27 + 8)
            cz.a[0].b = i16((cz.a[0].b // 27 // 7 * 7 + 4) * 27 + 8)
            for b1 in range(22):
                cz.g[b1] = GameCanvas.Y_v()
            cz.h = GameCanvas.Y_v()
            cz.i = GameCanvas.Y_v()
            cz.l = GameCanvas.Y_v()
            if config.ORIG_BUG["B2"]:
                # ORIG-BUG B2: the level is one byte in the save (G(cz.l), ag.java:2908) read back
                # signed, so Lv128+ loaded as -128..; the rest of the game keeps it as an int
                cz.l &= 0xFF
            cz.m = GameCanvas.X_v()
            cz.n = GameCanvas.X_v()
            cz.o = GameCanvas.X_v()
            cz.p = GameCanvas.X_v()
            cz.q = GameCanvas.X_v()
            cz.r = GameCanvas.X_v()
            cz.E = GameCanvas.W_v()
            if GameCanvas.bi:
                cz.E = 555000
            if config.GOLD is not None:   # PORT-EXTRA config.GOLD (POW_GOLD=N)
                cz.E = i32(config.GOLD)
            cz.F = GameCanvas.W_v()
            cz.G = GameCanvas.W_v()
            cz.H = GameCanvas.X_v()
            cz.J = GameCanvas.X_v()
            cz.S = GameCanvas.Y_v()
            for b1 in range(5):
                cz.V[b1] = GameCanvas.Y_v()
            for b1 in range(19):
                cz.W[b1] = GameCanvas.Y_v()
            for b1 in range(9):
                cz.X[b1] = self.Z_v()
            for b1 in range(25):
                cz.Y[b1] = self.Z_v()
            for b1 in range(5):
                cz.Z[b1].a = GameCanvas.X_v()
                cz.Z[b1].b = GameCanvas.Y_v()
            cz.aa[0] = GameCanvas.Y_v()
            cz.aa[1] = GameCanvas.Y_v()
            cz.aB = GameCanvas.Y_v()
            GameCanvas.dV = GameCanvas.W_v()
            GameCanvas.eo = GameCanvas.W_v()
            GameCanvas.fR = GameCanvas.Y_v()
            GameCanvas.fS = GameCanvas.Y_v()
            GameCanvas.dH = GameCanvas.Y_v()
            GameCanvas.ep = GameCanvas.Y_v()
            for b1 in range(16):
                arrayOfByte1[b1] = GameCanvas.Y_v()
            GameCanvas.fq = GameCanvas.W_v()
            for b1 in range(4):
                GameCanvas.W_v()
        self.ag()

    @staticmethod
    def V_v():  # ag.java:2216-2230  (u64 LE; bytes 4..7 are sign-extended then masked)
        cF, cG = GameCanvas.cF, GameCanvas.cG
        l1 = 0
        for k_ in range(8):
            l1 |= (cF[cG + k_] & 0xFF) << (8 * k_)
        GameCanvas.cG += 8
        return l1 - (1 << 64) if l1 & (1 << 63) else l1

    @staticmethod
    def W_v():  # ag.java:2232-2237
        cF, cG = GameCanvas.cF, GameCanvas.cG
        j_ = cF[cG] & 0xFF | cF[cG + 1] << 8 & 0xFF00 | cF[cG + 2] << 16 & 0xFF0000 | cF[cG + 3] << 24 & 0xFF000000
        GameCanvas.cG += 4
        return i32(j_)

    @staticmethod
    def X_v():  # ag.java:2239-2244
        s = i16(GameCanvas.cF[GameCanvas.cG] & 0xFF | GameCanvas.cF[GameCanvas.cG + 1] << 8 & 0xFF00)
        GameCanvas.cG += 2
        return s

    @staticmethod
    def Y_v():  # ag.java:2246-2250
        b = i8(GameCanvas.cF[GameCanvas.cG] & 0xFF)
        GameCanvas.cG += 1
        return b

    def Z_v(self):  # ag.java:2252-2261
        z1 = Item()
        z1.a = GameCanvas.X_v()
        z1.b = GameCanvas.X_v()
        z1.c = GameCanvas.X_v()
        z1.d = GameCanvas.X_v()
        z1.e = GameCanvas.X_v()
        z1.f = GameCanvas.Y_v()
        return z1

    def aa_v(self):  # ag.java:2263-2269
        GameCanvas.ct[34] = self.d_T(GameCanvas.bA.a_I(22))
        GameCanvas.ct[19] = self.d_T(GameCanvas.bA.a_I(24))
        GameCanvas.ct[20] = self.d_T(GameCanvas.bA.a_I(25))
        GameCanvas.ct[0] = self.d_T(GameCanvas.bA.a_I(48))
        GameCanvas.ct[32] = self.d_T(GameCanvas.bA.a_I(37))

    @staticmethod
    def v_I(paramInt):  # ag.java:2283-2285
        return ResReader.a("/" + GameCanvas.bE.a_I(paramInt))

    def w_I(self, paramInt):  # ag.java:2287-2304
        self.ah()
        self.ae_v()
        if GameCanvas.ct[7] is None:
            GameCanvas.ct[7] = Image.createImage(GameCanvas.bZ.a, GameCanvas.bZ.b)
        GameCanvas.cu = GameCanvas.ct[7].getGraphics()
        GameCanvas.dj = 0
        GameCanvas.cM[2] = 0
        GameCanvas.cM[1] = 0
        GameCanvas.cS.b = 0
        GameCanvas.cU = GameCanvas.v_I(47)
        GameCanvas.cW = GameCanvas.v_I(49)
        GameCanvas.cV = GameCanvas.v_I(51)
        GameCanvas.af_v()
        GameCanvas.ct[17] = self.d_T(GameCanvas.bA.a_I(27))
        self.x_I(paramInt)
        self.ag()

    def ad_v(self):  # ag.java:2306-2311
        GameCanvas.ct[1] = self.d_T(GameCanvas.bA.a_I(21))
        GameCanvas.ct[2] = self.d_T(GameCanvas.bA.a_I(46))
        GameCanvas.ct[3] = self.d_T(GameCanvas.bA.a_I(43))
        GameCanvas.fN = self.d_T(GameCanvas.bA.a_I(38))

    def ae_v(self):  # ag.java:2313-2319
        GameCanvas.ct[1] = None
        GameCanvas.ct[2] = None
        GameCanvas.ct[3] = None
        GameCanvas.fN = None
        GameCanvas.R_v()

    @staticmethod
    def af_v():  # ag.java:2321-2343  (menu captions from uimenu.scr = edat[69])
        al1 = ScrTable("/" + GameCanvas.bE.a_I(69))
        for b in range(30):
            GameCanvas.fT[b] = al1.a_I(b)
            if b < 7:
                GameCanvas.gd[b] = al1.a_I(b + 48)
            if b < 6:
                GameCanvas.fV[b] = al1.a_I(b + 30)
            if b < 5:
                GameCanvas.ge[b] = al1.a_I(b + 55)
            if b < 4:
                GameCanvas.gb[b] = al1.a_I(b + 42)
            if b < 2:
                GameCanvas.gc[b] = al1.a_I(b + 46)
        GameCanvas.fU[0] = al1.a_I(36)
        GameCanvas.fW[0] = al1.a_I(37)
        GameCanvas.ga[0] = al1.a_I(38)
        GameCanvas.fX[0] = al1.a_I(39)
        GameCanvas.fY[0] = al1.a_I(40)
        GameCanvas.fZ[0] = al1.a_I(41)
        al1.a_v()

    def x_I(self, paramInt):  # ag.java:2345-2370  (menu background into ct[7])
        if paramInt == 1:
            return
        Gfx.a_G(GameCanvas.cu)
        GameCanvas.ct[11] = self.d_T(GameCanvas.bA.a_I(60))
        GameCanvas.ct[12] = self.d_T(GameCanvas.bA.a_I(61))
        GameCanvas.ct[16] = self.d_T(GameCanvas.bA.a_I(63))
        GameCanvas.ct[9] = self.d_T(GameCanvas.bA.a_I(59))
        j_ = GameCanvas.ct[9].getWidth()
        m = GameCanvas.ct[9].getHeight()
        b = 0
        while b * m < GameCanvas.bZ.b + m:
            for b1 in range(4):
                GameCanvas.c_MIIIIII(GameCanvas.ct[9], 0, 0, (b & 0x1) * -31 + b1 * j_, b * m, j_, m)
            b += 1
        # Java: (W - w) * b / 2 and H / 2 * b % 2 - all operands >= 0, so // matches Java /
        for b in range(4):
            GameCanvas.c_MIIIIII(GameCanvas.ct[12], 0, 0, (GameCanvas.bZ.a - GameCanvas.ct[12].getWidth()) * b // 2, GameCanvas.bZ.b // 2 * b % 2,
                         GameCanvas.ct[12].getWidth(), GameCanvas.ct[12].getHeight())
        for b in range(4):
            GameCanvas.c_MIIIIII(GameCanvas.ct[11], 0, 0, GameCanvas.bZ.a // 2 * b % 2, (GameCanvas.bZ.b - GameCanvas.ct[11].getHeight()) * b // 2,
                         GameCanvas.ct[11].getWidth(), GameCanvas.ct[11].getHeight())
        GameCanvas.c_MIIIIII(GameCanvas.ct[16], 0, 0, (GameCanvas.bZ.a >> 1) - GameCanvas.ct[16].getWidth() // 2, 0,
                     GameCanvas.ct[16].getWidth(), GameCanvas.ct[16].getHeight())
        GameCanvas.ct[11] = None
        GameCanvas.ct[12] = None
        GameCanvas.ct[16] = None
        GameCanvas.ct[9] = None
        Gfx.a_G(GameCanvas.br)

    def ag(self):  # ag.java:2372-2382  (compact inventory cz.Y)
        for b in range(24):
            if GameCanvas.cz.Y[b].a == 0:
                for j_ in range(b + 1, 25):
                    if GameCanvas.cz.Y[j_].a != 0:
                        self.a_LzLz(GameCanvas.cz.Y[b], GameCanvas.cz.Y[j_])
                        break

    def a_LzLz(self, paramz1, paramz2):  # ag.java:2384-2389
        z1 = Item()
        GameCanvas.b_LzLz(z1, paramz1)
        GameCanvas.b_LzLz(paramz1, paramz2)
        GameCanvas.b_LzLz(paramz2, z1)

    @staticmethod
    def b_LzLz(paramz1, paramz2):  # ag.java:2391-2398
        paramz1.a = paramz2.a
        paramz1.b = paramz2.b
        paramz1.c = paramz2.c
        paramz1.d = paramz2.d
        paramz1.e = paramz2.e
        paramz1.f = paramz2.f

    def ah(self):  # ag.java:2400-2436
        GameCanvas.eS[0] = None
        GameCanvas.eS[1] = None
        GameCanvas.cz.aD = None
        GameCanvas.cz.aF = None
        GameCanvas.eT[0] = None
        GameCanvas.eT[1] = None
        GameCanvas.ct[40] = None
        GameCanvas.ct[41] = None
        if GameCanvas.bT is not None:
            for b1 in range(len(GameCanvas.bT)):
                GameCanvas.bT[b1] = None
            GameCanvas.bT = None
        GameCanvas.eU = None
        GameCanvas.ct[42] = None
        GameCanvas.eV = None
        GameCanvas.ct[43] = None
        GameCanvas.eR = None
        GameCanvas.eQ = None
        GameCanvas.eW = None
        GameCanvas.ct[44] = None
        GameCanvas.ct[31] = None
        GameCanvas.fe = None
        GameCanvas.eY = None
        GameCanvas.er[1] = None
        for b in range(2):
            GameCanvas.es[b] = None
        for b in range(9):
            GameCanvas.et[b] = None
        GameCanvas.eq = None
        GameCanvas.bY.a = GameCanvas.bZ.a
        GameCanvas.bY.b = GameCanvas.bZ.b
        GameCanvas.db = 0
        GameCanvas.dc = 0

    @staticmethod
    def a_IIIIMII(paramInt1, paramInt2, paramInt3, paramInt4, paramImage, paramInt5, paramInt6):  # ag.java:2438-2440
        Gfx.a_MIIIIII(paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6)

    def b_MIIIIII(self, paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # ag.java:2442-2457
        i1 = paramInt2
        if i1 > 0:
            i1 = 0
        i2 = GameCanvas.bY.b - paramInt2 - paramInt4
        if i2 > 0:
            i2 = 0
        j_ = paramInt1
        if j_ > 0:
            j_ = 0
        m = GameCanvas.bY.a - paramInt1 - paramInt3
        if m > 0:
            m = 0
        if paramInt4 + i1 + i2 > 0 and paramInt3 + j_ + m > 0:
            GameCanvas.a_IIIIMII(paramInt1 + GameCanvas.db - j_, paramInt2 - i1 + GameCanvas.dc, paramInt3 + j_ + m, paramInt4 + i1 + i2,
                         paramImage, paramInt5 - j_, paramInt6 - i1)

    @staticmethod
    def c_MIIIIII(paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # ag.java:2459-2461
        Gfx.a_MIIIIII(paramImage, paramInt3, paramInt4, paramInt5, paramInt6, paramInt1, paramInt2)

    @staticmethod
    def ai():  # ag.java:2463-2465
        from pow.game.sound import Sound
        Sound.b_v()

    @staticmethod
    def aj():  # ag.java:2467-2472
        GameCanvas.cz.aC = None
        GameCanvas.cz.aE = None
        GameCanvas.cz.aG = None
        GameCanvas.cz.aH = None

    @staticmethod
    def ak():  # ag.java:2522-2546
        v = GameCanvas.cM[0]
        if v == 0:
            GameCanvas.dE = GameCanvas.fU
        elif v == 1:
            GameCanvas.cN = GameCanvas.dr
            GameCanvas.dE = GameCanvas.dt
        elif v == 2:
            GameCanvas.cN = GameCanvas.dv[GameCanvas.dk]
            GameCanvas.dE = GameCanvas.dA
        elif v == 7:
            GameCanvas.cz.k = None
        elif v == 10:
            GameCanvas.dE = GameCanvas.fW
        elif v == 13:
            GameCanvas.dE = GameCanvas.fY
            GameCanvas.ct[39] = None

    @staticmethod
    def ap():  # ag.java:2728-2733
        GameCanvas.cN = consts.v[GameCanvas.cM[0]]
        GameCanvas.cM[1] = GameCanvas.cP[GameCanvas.cM[0]]
        GameCanvas.cM[2] = GameCanvas.cQ[GameCanvas.cM[0]]
        GameCanvas.ck = 1

    @staticmethod
    def a_TII(paramString, paramInt1, paramInt2):  # ag.java:2743-2746  (centred text)
        paramInt1 += 2
        Gfx.a_TIII(paramString, GameCanvas.dd + GameCanvas.db + paramInt2, paramInt1 + GameCanvas.dc, 1)

    def b_TII(self, paramString, paramInt1, paramInt2):  # ag.java:2748-2750
        GameCanvas.a_TII(paramString, paramInt1, 0)

    @staticmethod
    def c_TII(paramString, paramInt1, paramInt2):  # ag.java:2752-2754
        Gfx.a_TIII(paramString, paramInt1 + GameCanvas.db, paramInt2 + GameCanvas.dc, 1)

    @staticmethod
    def d_TII(paramString, paramInt1, paramInt2):  # ag.java:2756-2758
        Gfx.a_TIII(paramString, paramInt1 + GameCanvas.db, paramInt2 + GameCanvas.dc, 0)

    def a_IIIIZ(self, paramInt1, paramInt2, paramInt3, paramInt4, paramBoolean):  # ag.java:2760-2762
        GameCanvas.a_IIIIIIIZ(paramInt1, paramInt2, paramInt3, paramInt4, 0, 5263440, 16777215, paramBoolean)

    @staticmethod
    def a_IIIIIIIZ(paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7, paramBoolean):  # ag.java:2764-2791
        ac1 = Rect(0, 0, 0, 0)
        if paramBoolean:
            ac1.a = paramInt1 - 2
            ac1.c = paramInt3 + 4
            ac1.b = paramInt2 - 1
            ac1.d = paramInt4 + 2
            Gfx.a_IIIII(ac1.a, ac1.b, ac1.c, ac1.d, paramInt7)
            ac1.a += 1
            ac1.c -= 2
            ac1.b -= 1
            ac1.d += 2
            Gfx.a_IIIII(ac1.a, ac1.b, ac1.c, ac1.d, paramInt7)
        ac1.a = paramInt1 - 1
        ac1.c = paramInt3 + 2
        ac1.b = paramInt2
        ac1.d = paramInt4
        Gfx.a_IIIII(ac1.a, ac1.b, ac1.c, ac1.d, paramInt6)
        ac1.a += 1
        ac1.c -= 2
        ac1.b -= 1
        ac1.d += 2
        Gfx.a_IIIII(ac1.a, ac1.b, ac1.c, ac1.d, paramInt6)
        ac1.b += 1
        ac1.d -= 2
        Gfx.b_IIIII(ac1.a, ac1.b, ac1.c, ac1.d, paramInt5)

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
        GameCanvas.bV = 12
        GameCanvas.ck = 1
        GameCanvas.dr = 0
        GameCanvas.ai()
        GameCanvas.c = system.currentTimeMillis()

    def at(self):  # ag.java:3011-3019  (outro picture)
        if GameCanvas.bN == 2 or GameCanvas.bN == 5:
            GameCanvas.ai()
        GameCanvas.u_I(0)
        image = self.d_T(GameCanvas.bA.a_I(0))
        j_ = image.getWidth()
        GameCanvas.a_IIIIMII(GameCanvas.bL - j_ // 2, GameCanvas.bM - 10, j_, 20, image, 0, 0)
        GameCanvas.a_IIIIMII(GameCanvas.bL - j_ // 2, GameCanvas.bK - 24, j_, 22, image, 0, 20)

    @staticmethod
    def a_ABII(paramArrayOfbyte, paramInt1, paramInt2):  # ag.java:3026-3043  (readUTF of bytes[from:to])
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
        if GameCanvas.cS.b != 0:
            return
        j_ = GameCanvas.bU.getWidth()
        m = GameCanvas.bU.getHeight()
        str_ = ""
        if paramInt1 != -1:
            Gfx.a_Lg(GameCanvas.bu)
            Gfx.a_MII(GameCanvas.bU, 0, GameCanvas.bK - m)
            i1 = len(str_ + consts.t[paramInt1]) * 10
            i2 = i1 + 4 - GameCanvas.bU.getWidth()
            if i2 > 0:
                Gfx.b_IIIII(j_ - 8, GameCanvas.bK - m + 2, 8, 13, 0)
                Gfx.a_MII(GameCanvas.bU, i2, GameCanvas.bK - m)
                Gfx.b_IIIII(i2, GameCanvas.bK - m + 2, 8, 13, 0)
                Gfx.a_TIII(str_ + consts.t[paramInt1], (j_ + i2) // 2, GameCanvas.bK - m, 1)
            else:
                Gfx.a_TIII(str_ + consts.t[paramInt1], j_ // 2, GameCanvas.bK - m, 1)
        if paramInt2 != -1:
            Gfx.a_Lg(GameCanvas.bu)
            Gfx.a_MII(GameCanvas.bU, GameCanvas.bJ - j_ - 0, GameCanvas.bK - m)
            i1 = len(str_ + consts.t[paramInt2]) * 10
            i2 = i1 + 15 - GameCanvas.bU.getWidth()
            if i2 > 0:
                Gfx.b_IIIII(GameCanvas.bJ - j_ - 0, GameCanvas.bK - m + 2, 8, 13, 0)
                Gfx.a_MII(GameCanvas.bU, GameCanvas.bJ - j_ - i2 - 0, GameCanvas.bK - m)
                Gfx.b_IIIII(GameCanvas.bJ - i2 - 0 - 8, GameCanvas.bK - m + 2, 8, 13, 0)
                Gfx.a_TIII(str_ + consts.t[paramInt2], GameCanvas.bJ - (j_ + i2) // 2 - 0, GameCanvas.bK - m, 1)
                return
            Gfx.a_TIII(str_ + consts.t[paramInt2], GameCanvas.bJ - j_ // 2 - 0, GameCanvas.bK - m, 1)

    def l_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:3201-3203
        GameCanvas.bO = GameCanvas.k_III(paramInt1, paramInt2, paramInt3)

    @staticmethod
    def f_IIII(paramInt1, paramInt2, paramInt3, paramInt4):  # ag.java:3205-3207
        Gfx.c_IIIII(paramInt1, paramInt2, paramInt3, paramInt4, GameCanvas.bO)

    def aA(self):  # ag.java:3459-3465
        GameCanvas.aj()
        GameCanvas.cz.aG = self.d_T(GameCanvas.bB.a_I(46 + GameCanvas.cz.aB))
        GameCanvas.cz.aC = self.K_I(47 + GameCanvas.cz.aB)
        GameCanvas.cz.aH = self.d_T(GameCanvas.bB.a_I(44))
        GameCanvas.cz.aE = self.K_I(45)

    def K_I(self, paramInt):  # ag.java:3467-3482  (frame table from mdat_QVGA)
        b1 = 1
        arrayOfByte = ResReader.a("/" + GameCanvas.bF.a_I(paramInt))
        n = arrayOfByte[0] & 0xFF
        arrayOfY = [None] * n
        for b2 in range(n):
            arrayOfY[b2] = SpriteFrame()
            arrayOfY[b2].a = GameCanvas.a_BB(arrayOfByte[b1], arrayOfByte[b1 + 1])
            arrayOfY[b2].b = GameCanvas.a_BB(arrayOfByte[b1 + 2], arrayOfByte[b1 + 3])
            arrayOfY[b2].c = GameCanvas.a_BB(arrayOfByte[b1 + 4], arrayOfByte[b1 + 5])
            arrayOfY[b2].d = GameCanvas.a_BB(arrayOfByte[b1 + 6], arrayOfByte[b1 + 7])
            arrayOfY[b2].e = GameCanvas.a_BB(arrayOfByte[b1 + 8], arrayOfByte[b1 + 9])
            arrayOfY[b2].f = GameCanvas.a_BB(arrayOfByte[b1 + 10], arrayOfByte[b1 + 11])
            b1 += 12
        return arrayOfY

    @staticmethod
    def M_I(paramInt):  # ag.java:3538-3540
        return GameCanvas.bG.a_I(paramInt)

    @staticmethod
    def N_I(paramInt):  # ag.java:3549-3574  (key code '0'..'9' -> digit, else -1)
        if 48 <= paramInt <= 57:
            return paramInt - 48
        return -1

    @staticmethod
    def H_I(paramInt):  # ag.java:3081-3098  (add exp; returns the levels gained)
        arrayOfInt = [0] * 10
        b = 0
        paramInt += GameCanvas.cz.G
        while True:
            j = b % 10
            if j == 0:
                arrayOfInt = GameCanvas.bb.p_v()
            j = arrayOfInt[j]
            if paramInt < j:
                GameCanvas.cz.G = paramInt
                return b
            paramInt -= j
            GameCanvas.cz.l += 1
            GameCanvas.cz.J += 3
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
        cz = GameCanvas.cz
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
                GameCanvas.bP = (GameCanvas.bP + 28 - 14) % 28
            elif paramInt == -2 or paramInt == 56:
                GameCanvas.bP = (GameCanvas.bP + 28 + 14) % 28
            elif paramInt == -3 or paramInt == 52:
                GameCanvas.bP = (GameCanvas.bP + 28 - 1) % 28
            elif paramInt == -4 or paramInt == 54:
                GameCanvas.bP = (GameCanvas.bP + 28 + 1) % 28
                if GameCanvas.bP == 27:
                    GameCanvas.bP = 0
        if GameCanvas.bP == 27:
            GameCanvas.bP = 26
        return j_

    _F_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                  "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                  "U", "V", "W", "X", "Y", "Z", "OK"]

    @staticmethod
    def f_II(paramInt1, paramInt2):  # ag.java:1794-1819  (letter grid A..Z + OK)
        j_ = GameCanvas.bL - 71
        arrayOfString = GameCanvas._F_LETTERS
        Gfx.b_IIIII(j_, paramInt2, 142, 34, 0)
        Gfx.b_IIIII(j_ + 123, paramInt2 + 18, 19, 15, 255)
        if GameCanvas.bN % 4 < 2:
            if paramInt1 == 26:
                Gfx.b_IIIII(j_ + 123, paramInt2 + 18, 19, 15, 16711680)
            elif F10:
                # DECOMP-FIX F10: `10 * p % 14`, `17 * p / 14` -> `10 * (p % 14)`, `17 * (p / 14)`
                Gfx.b_IIIII(j_ + 2 + 10 * (paramInt1 % 14), paramInt2 + 1 + 17 * (paramInt1 // 14), 10, 15, 16711680)
            else:
                Gfx.b_IIIII(j_ + 2 + 10 * paramInt1 % 14, paramInt2 + 1 + 17 * paramInt1 // 14, 10, 15, 16711680)
        Gfx.a_Lg(GameCanvas.bu)
        for b in range(len(arrayOfString)):
            if b == 8:
                b1 = 1
            elif b == 26:
                b1 = 1
            else:
                b1 = 0
            row = 17 * (b // 14) if F10 else 17 * b // 14   # DECOMP-FIX F10
            Gfx.a_TIII(arrayOfString[b], j_ + 3 + b % 14 * 10 + b1, paramInt2 + row, 0)

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
        GameCanvas.a_IIIIMII(paramInt2 + GameCanvas.db, paramInt3 + GameCanvas.dc, b1, b2, GameCanvas.ct[17], b3, b4)

    @staticmethod
    def g_II(paramInt1, paramInt2):  # ag.java:2735-2737
        paramInt2 -= 1
        return paramInt1 + abs(imod(GameCanvas.by.nextInt(), abs(paramInt2 - paramInt1) + 1))

    def C_I(self, paramInt):  # ag.java:2739-2741
        return GameCanvas.g_II(0, paramInt)

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
                self.b_MIIIIII(GameCanvas.ct[19], paramInt2, paramInt3, 5, 14, 100, 0)
            paramInt2 -= 9
            self.b_MIIIIII(GameCanvas.ct[19], paramInt2, paramInt3, 10, 14, imod(paramInt1, 10) * 10, 0)
            b += 1
            paramInt1 = idiv(paramInt1, 10)
            if paramInt1 <= 0:
                return j_

    def ar(self):  # ag.java:2871-2961  (write the save "gamevil_pow_data")
        cz = GameCanvas.cz
        arrayOfChar = [0] * 16
        arrayOfByte = cz.k.encode("latin-1")
        cF = GameCanvas.cF
        for b in range(8):
            if b < len(arrayOfByte):
                cF[2 + b] = arrayOfByte[b]
            else:
                cF[2 + b] = 32
        cF[18] = GameCanvas.dj & 0xFF
        GameCanvas.cG = 19
        GameCanvas.G_I(GameCanvas.dk)
        GameCanvas.G_I(GameCanvas.dm)
        GameCanvas.G_I(GameCanvas.do)
        GameCanvas.a_J(GameCanvas.dw)
        GameCanvas.a_J(GameCanvas.dx)
        for b in range(8):
            GameCanvas.E_I(i32(GameCanvas.dy[b]))
        GameCanvas.E_I(GameCanvas.dY)
        GameCanvas.E_I(GameCanvas.ed)
        for b in range(44):
            GameCanvas.G_I(GameCanvas.fn[0][b])
            GameCanvas.G_I(GameCanvas.fn[1][b])
        GameCanvas.G_I(GameCanvas.fo)
        for b in range(25):
            self.a_Lz(GameCanvas.fL[b])
        GameCanvas.G_I(GameCanvas.cq)
        GameCanvas.F_I((idiv(GameCanvas.cd + 2, 7) * 7 + 4) * 27)
        GameCanvas.F_I((idiv(GameCanvas.ce + 2, 7) * 7 + 4) * 27)
        for b in range(22):
            GameCanvas.G_I(cz.g[b])
        GameCanvas.G_I(cz.h)
        GameCanvas.G_I(cz.i)
        GameCanvas.G_I(cz.l)
        GameCanvas.F_I(cz.m)
        GameCanvas.F_I(cz.n)
        GameCanvas.F_I(cz.o)
        GameCanvas.F_I(cz.p)
        GameCanvas.F_I(cz.q)
        GameCanvas.F_I(cz.r)
        GameCanvas.E_I(cz.E)
        GameCanvas.E_I(cz.F)
        GameCanvas.E_I(cz.G)
        GameCanvas.F_I(cz.H)
        GameCanvas.F_I(cz.J)
        GameCanvas.G_I(cz.S)
        for b in range(5):
            GameCanvas.G_I(cz.V[b])
        for b in range(19):
            GameCanvas.G_I(cz.W[b])
        for b in range(9):
            self.a_Lz(cz.X[b])
        for b in range(25):
            self.a_Lz(cz.Y[b])
        for b in range(5):
            GameCanvas.F_I(cz.Z[b].a)
            GameCanvas.G_I(cz.Z[b].b)
        GameCanvas.G_I(cz.aa[0])
        GameCanvas.G_I(cz.aa[1])
        GameCanvas.G_I(cz.aB)
        GameCanvas.E_I(i32(GameCanvas.dW[0] - GameCanvas.dV))
        GameCanvas.E_I(i32(GameCanvas.eo))
        GameCanvas.G_I(GameCanvas.fR)
        GameCanvas.G_I(GameCanvas.fS)
        GameCanvas.G_I(GameCanvas.dH)
        GameCanvas.G_I(GameCanvas.ep)
        for b in range(16):
            GameCanvas.G_I(arrayOfChar[b])
        GameCanvas.E_I(GameCanvas.fq)
        for b in range(4):
            GameCanvas.E_I(0)
        cF[0] = GameCanvas.cG & 0xFF
        cF[1] = GameCanvas.cG >> 8 & 0xFF
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_data", True)
            if recordStore.getNumRecords() == 0:
                recordStore.addRecord(cF, 0, len(cF))
            recordStore.setRecord(1, cF, 0, len(cF))
        except Exception:
            pass
        return bool(GameCanvas.aq())

    # cF holds Java bytes; the port stores them masked to 0..255 (RecordStore takes bytearray)
    @staticmethod
    def a_J(paramLong):  # ag.java:2963-2973
        for k_ in range(8):
            GameCanvas.cF[GameCanvas.cG + k_] = paramLong >> (8 * k_) & 0xFF
        GameCanvas.cG += 8

    @staticmethod
    def E_I(paramInt):  # ag.java:2975-2981
        GameCanvas.cF[GameCanvas.cG] = paramInt & 0xFF
        GameCanvas.cF[GameCanvas.cG + 1] = paramInt >> 8 & 0xFF
        GameCanvas.cF[GameCanvas.cG + 2] = paramInt >> 16 & 0xFF
        GameCanvas.cF[GameCanvas.cG + 3] = paramInt >> 24 & 0xFF
        GameCanvas.cG += 4

    @staticmethod
    def F_I(paramInt):  # ag.java:2983-2987
        GameCanvas.cF[GameCanvas.cG] = paramInt & 0xFF
        GameCanvas.cF[GameCanvas.cG + 1] = paramInt >> 8 & 0xFF
        GameCanvas.cG += 2

    @staticmethod
    def G_I(paramInt):  # ag.java:2989-2992
        GameCanvas.cF[GameCanvas.cG] = paramInt & 0xFF
        GameCanvas.cG += 1

    def a_Lz(self, paramz):  # ag.java:2994-3001
        GameCanvas.F_I(paramz.a)
        GameCanvas.F_I(paramz.b)
        GameCanvas.F_I(paramz.c)
        GameCanvas.F_I(paramz.d)
        GameCanvas.F_I(paramz.e)
        GameCanvas.G_I(paramz.f)

    def a_IIIIIII(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7):  # ag.java:3140-3146  (rectangle outline)
        self.l_III(paramInt5, paramInt6, paramInt7)
        GameCanvas.f_IIII(paramInt1, paramInt2, paramInt1 + paramInt3 - 1, paramInt2)
        GameCanvas.f_IIII(paramInt1, paramInt2 + 1, paramInt1, paramInt2 + paramInt4 - 1)
        GameCanvas.f_IIII(paramInt1 + paramInt3 - 1, paramInt2, paramInt1 + paramInt3 - 1, paramInt2 + paramInt4 - 1)
        GameCanvas.f_IIII(paramInt1 + 1, paramInt2 + paramInt4 - 1, paramInt1 + paramInt3 - 2, paramInt2 + paramInt4 - 1)

    def b_IIIIIII(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7):  # ag.java:3181-3187  (outline, round corners)
        self.l_III(paramInt5, paramInt6, paramInt7)
        GameCanvas.f_IIII(paramInt1 + 1, paramInt2, paramInt1 + paramInt3 - 2, paramInt2)
        GameCanvas.f_IIII(paramInt1, paramInt2 + 1, paramInt1, paramInt2 + paramInt4 - 2)
        GameCanvas.f_IIII(paramInt1 + paramInt3 - 1, paramInt2 + 1, paramInt1 + paramInt3 - 1, paramInt2 + paramInt4 - 2)
        GameCanvas.f_IIII(paramInt1 + 1, paramInt2 + paramInt4 - 1, paramInt1 + paramInt3 - 2, paramInt2 + paramInt4 - 1)

    def c_IIIIIII(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7):  # ag.java:3189-3199  (selection frame)
        self.b_IIIIIII(paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7)
        self.j_II(paramInt1 + 1, paramInt2 + 1)
        self.j_II(paramInt1 + paramInt3 - 2, paramInt2 + 1)
        self.j_II(paramInt1 + 1, paramInt2 + paramInt4 - 2)
        self.j_II(paramInt1 + paramInt3 - 2, paramInt2 + paramInt4 - 2)

    def j_II(self, paramInt1, paramInt2):  # ag.java:3209-3211
        GameCanvas.f_IIII(paramInt1, paramInt2, paramInt1 + 1, paramInt2 + 1)

    def au(self):  # ag.java:3213-3220  (New Game -> difficulty screen 29)
        GameCanvas.bb.c_v()
        GameCanvas.cM[0] = 29
        GameCanvas.cN = consts.v[GameCanvas.cM[0]]
        GameCanvas.cM[1] = 1
        GameCanvas.cz.aB = 0
        self.av()

    def av(self):  # ag.java:3222-3273  (fresh hero)
        cz = GameCanvas.cz
        GameCanvas.dj = 0
        GameCanvas.dH = 0
        GameCanvas.dw = 35113052110447
        GameCanvas.dx = 0
        GameCanvas.ed = 0
        GameCanvas.cq = 0
        cz.aB = 0
        cz.k = ""
        for b in range(45):
            GameCanvas.fn[1][b] = 0
            GameCanvas.fn[0][b] = 0
        GameCanvas.fo = 0
        for b in range(8):
            GameCanvas.dy[b] = 0
        cz.l = 1
        GameCanvas.aw()
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
        if GameCanvas.bi:
            for b in range(19):
                cz.W[b] = 1
            cz.W[18] = 1
        # z.a() is shadowed by the field z.a on instances -> call it through the class
        for b in range(9):
            Item.a(cz.X[b])
        for b in range(25):
            Item.a(cz.Y[b])
        self.k_II(116, 0)
        self.a_LzLz(cz.X[0], cz.Y[0])
        cz.aa[0] = 0
        cz.aa[1] = 1

    @staticmethod
    def aw():  # ag.java:3275-3284  (base stats, 5 free points)
        cz = GameCanvas.cz
        cz.m = 5
        cz.n = 4
        cz.o = 30
        cz.p = 30
        cz.q = 10
        cz.r = 10
        cz.J = 5
        GameCanvas.ck = 1

    def k_II(self, paramInt1, paramInt2):  # ag.java:3286-3360  (give an item / potion / gold)
        cz = GameCanvas.cz
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
                cz.Z[GameCanvas.dU.e].b = i16(cz.Z[GameCanvas.dU.e].b - 1)
                if cz.Z[GameCanvas.dU.e].b < 1:
                    cz.Z[GameCanvas.dU.e].a = 0
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
            GameCanvas.bb.e_I(paramInt1)
        if paramInt1 < 100:
            cz.Z[b].a = i16(paramInt1)
            cz.Z[b].b = i16(cz.Z[b].b + 1)
        elif paramInt1 < 300:
            if paramInt2 != 0:
                s = i16(GameCanvas.cX.d + self.C_I(GameCanvas.cX.e + 1))
            else:
                s = GameCanvas.cX.d
            if GameCanvas.cX.c == 0:
                cz.Y[b].b = s
            elif GameCanvas.cX.c == 1:
                cz.Y[b].c = s
            elif GameCanvas.cX.c == 2:
                cz.Y[b].d = s
            elif GameCanvas.cX.c == 3:
                cz.Y[b].e = s
        elif paramInt1 < 500:
            cz.Y[b].b = GameCanvas.cY.c
            cz.Y[b].c = i16(GameCanvas.cY.d)
            cz.Y[b].d = GameCanvas.cY.e
            cz.Y[b].e = i16(GameCanvas.cY.f)
        elif paramInt1 < 10000:
            cz.Y[b].b = GameCanvas.cZ.c
            cz.Y[b].c = i16(GameCanvas.cZ.d)
            cz.Y[b].d = GameCanvas.cZ.e
            cz.Y[b].e = i16(GameCanvas.cZ.f)
        else:
            cz.E += paramInt1 - 10000
        return 1

    @staticmethod
    def ax():  # ag.java:3362-3375  (starting quick items)
        for b in range(8):
            if GameCanvas.fL[b] is None:
                GameCanvas.fL[b] = Item()
        GameCanvas.fL[0].a = 1
        GameCanvas.fL[1].a = 2
        GameCanvas.fL[2].a = 3
        GameCanvas.fL[3].a = 4
        GameCanvas.fL[4].a = 5
        GameCanvas.fL[5].a = 6
        GameCanvas.fL[6].a = 10
        GameCanvas.fL[7].a = 11

    def ay(self):  # ag.java:3377-3398  (17 random shop items, sorted)
        arrayOfInt = [0] * 17
        GameCanvas.az()
        for b in range(17):
            arrayOfInt[b] = 101 + 5 * GameCanvas.g_II(0, 20) + GameCanvas.I_I(GameCanvas.g_II(0, 100))
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
            GameCanvas.fL[8 + b] = self.J_I(arrayOfInt[b])

    @staticmethod
    def az():  # ag.java:3400-3412
        arrayOfInt = [47, 51, 49]
        if not GameCanvas.fM[1]:
            for b in range(3):
                if GameCanvas.bH[b] is None:
                    GameCanvas.bH[b] = ArrTable("/" + GameCanvas.bE.a_I(arrayOfInt[b]))
                if GameCanvas.bH[b] is None:
                    return False
            GameCanvas.fM[1] = True
        return True

    @staticmethod
    def I_I(paramInt):  # ag.java:3414-3422  (item tier by hero level)
        m = 0
        b = 0
        while b < 5 and GameCanvas.cz.l >= consts.w[b]:
            b += 1
        j_ = consts.x[b - 1]
        b = 0
        while b < 4:
            m += j_ & 0xFF
            if not paramInt >= m:
                break
            j_ >>= 8
            b += 1
        return b

    def J_I(self, paramInt):  # ag.java:3424-3457  (make item paramInt with random bonus)
        z1 = Item()
        arrayOfInt = [0] * 5
        z1.a = i16(paramInt)
        z1.f = 0
        if paramInt < 300:
            for b in range(3):
                arrayOfInt[b] = GameCanvas.bH[0].a_II(paramInt - 101, 2 + b)
            if arrayOfInt[0] == 0:
                z1.b = i16(arrayOfInt[1] + self.C_I(arrayOfInt[2]))
            elif arrayOfInt[0] == 1:
                z1.c = i16(arrayOfInt[1] + self.C_I(arrayOfInt[2]))
            elif arrayOfInt[0] == 2:
                z1.d = i16(arrayOfInt[1] + self.C_I(arrayOfInt[2]))
            elif arrayOfInt[0] == 3:
                z1.e = i16(arrayOfInt[1] + self.C_I(arrayOfInt[2]))
        else:
            tbl = GameCanvas.bH[1] if paramInt < 500 else GameCanvas.bH[2]
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
        GameCanvas.ee = i16(paramInt1)
        if paramInt1 < 100:
            GameCanvas.ec = 0
            b = 64 + paramInt1 // 6
            for b1 in range(3):
                GameCanvas.eb[b1] = consts.aV[(paramInt1 << 1) + b1] - consts.aV[paramInt1 // 6 * 12]
            if paramInt1 == 3 and paramInt2 != 0 and 0 == GameCanvas.L_I(502):
                GameCanvas.eb[2] = 0
                GameCanvas.eb[1] = 0
                GameCanvas.eb[0] = 0
                GameCanvas.cq = 4
            GameCanvas.fE = -1
        else:
            GameCanvas.ec = 1
            b = 63
            GameCanvas.eb[0] = 0
            GameCanvas.eb[1] = 2
            GameCanvas.eb[2] = 13
            GameCanvas.fE = 0
            GameCanvas.dE = GameCanvas.fU
            GameCanvas.cO = 0
        if GameCanvas.bI is None:
            GameCanvas.bI = ScrTable("/" + GameCanvas.bE.a_I(b))
        GameCanvas.gf[1] = ""
        GameCanvas.gf[0] = ""
        GameCanvas.fA[1] = 0
        GameCanvas.fA[0] = 0
        GameCanvas.fD = 0
        GameCanvas.dS = 0
        GameCanvas.fG = 0
        GameCanvas.bd.c_I(GameCanvas.fD)
        if 0 == GameCanvas.ec:
            self.x_I(1)
        GameCanvas.bV = 10
        self.a__I(2)
        GameCanvas.ck = 1

    @staticmethod
    def L_I(paramInt):  # ag.java:3530-3536  (inventory slot of item, 1-based; 0 = none)
        for b in range(25):
            if GameCanvas.cz.Y[b].a == paramInt:
                return b + 1
        return 0

    # ---- story player (bV == 10): prologue / epilogue -------------------------------------

    def M_v(self):  # ag.java:1612-1692  (one tick of the story player)
        if GameCanvas.dS > 0:
            GameCanvas.dS = i16(GameCanvas.dS - 1)
            if GameCanvas.ch != -999 and GameCanvas.dS > 3:
                GameCanvas.dS = 3
            if 0 == GameCanvas.dS:
                GameCanvas.fD += 1
                if GameCanvas.fD < GameCanvas.eb[2] - GameCanvas.eb[0]:
                    GameCanvas.bd.c_I(GameCanvas.fD)
                elif 0 == GameCanvas.ec and GameCanvas.cO == 0 and GameCanvas.fD == GameCanvas.eb[2] - GameCanvas.eb[0]:
                    if GameCanvas.ef != 0 or GameCanvas.eg != 0:
                        GameCanvas.cS.e_I(27)
                    GameCanvas.bd.c_I(GameCanvas.fD)
                else:
                    GameCanvas.bI.a_v()
                    GameCanvas.bI = None
                    GameCanvas.gf[1] = ""
                    GameCanvas.gf[0] = ""
                    self.F_v()
                    GameCanvas.cM[0] = GameCanvas.cO
                    GameCanvas.ct[35] = None
                    GameCanvas.ct[35] = None
                    GameCanvas.ap()
                    if GameCanvas.cM[0] == 0:
                        GameCanvas.cM[1] = 0
                    GameCanvas.bV = 2
                    GameCanvas.cL = 0
                    GameCanvas.cK = 0
                GameCanvas.ck = 1
        elif (0 == GameCanvas.ec and GameCanvas.fD < GameCanvas.eb[1] - GameCanvas.eb[0]) or (GameCanvas.ec != 0 and GameCanvas.fD >= GameCanvas.eb[1] - GameCanvas.eb[0]):
            from pow.game.menus import Menus
            Menus.a_III(GameCanvas.fG, GameCanvas.fA[GameCanvas.fG], 0)
            if len(GameCanvas.fw[GameCanvas.fG]) <= GameCanvas.fA[GameCanvas.fG]:
                if GameCanvas.ch != -999:
                    GameCanvas.dS = 0
                else:
                    GameCanvas.dS = 15
        else:
            self.N_v()
            GameCanvas.eh = i16(GameCanvas.eh + 1)
            if GameCanvas.fG == 0:
                if GameCanvas.eh > 3:
                    GameCanvas.fG = i16(GameCanvas.fG + 1)
                    GameCanvas.eh = 0
            elif GameCanvas.fG == 2:
                if GameCanvas.eh > 4:
                    GameCanvas.dS = 3
            elif GameCanvas.fG == 1:
                GameCanvas.fA[0] = GameCanvas.fA[0] - 2
                if GameCanvas.fA[0] < -28:
                    GameCanvas.fA[0] = GameCanvas.fA[0] + 22
                    GameCanvas.fC[0] = GameCanvas.fC[0] + 1
                    if GameCanvas.dq[0] < GameCanvas.fC[0]:
                        if GameCanvas.fD == GameCanvas.eb[2] - GameCanvas.eb[0]:
                            GameCanvas.dS = 3
                        else:
                            GameCanvas.fG = i16(GameCanvas.fG + 1)
                    GameCanvas.eh = 1
        if GameCanvas.ch == -6:
            GameCanvas.dS = 1
            if GameCanvas.ec != 0:
                if GameCanvas.fD >= GameCanvas.eb[1] - GameCanvas.eb[0]:
                    GameCanvas.fD = 100
                    return
            elif GameCanvas.fD < GameCanvas.eb[1] - GameCanvas.eb[0]:
                GameCanvas.fD = GameCanvas.eb[1] - GameCanvas.eb[0] - 1

    def d_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:1694-1696  (fill the screen)
        Gfx.b_IIIII(0, 0, GameCanvas.bZ.a, GameCanvas.bZ.b, GameCanvas.k_III(paramInt1, paramInt2, paramInt3))

    def N_v(self):  # ag.java:1698-1737  (story picture + scrolling text)
        self.d_III(0, 0, 0)
        ct35 = GameCanvas.ct[35]
        if GameCanvas.fG in (0, 2):
            if 0 < GameCanvas.eh < 4:
                self.b_MIIIIII(ct35, GameCanvas.dd - (ct35.getWidth() >> 1), GameCanvas.de - (ct35.getHeight() >> 1),
                               ct35.getWidth(), ct35.getHeight(), 0, 0)
        elif GameCanvas.fG == 1:
            m = GameCanvas.fA[0]
            if GameCanvas.fD != GameCanvas.eb[2] - GameCanvas.eb[0]:
                self.b_MIIIIII(ct35, GameCanvas.dd - (ct35.getWidth() >> 1), GameCanvas.de - (ct35.getHeight() >> 1),
                               ct35.getWidth(), ct35.getHeight(), 0, 0)
            j_ = GameCanvas.fC[0]
            while j_ <= GameCanvas.dq[0] and m <= 230:
                # char arithmetic, as decompiled: `255 - (m - de + 72 << 4)` (only ==255 / ==0 matter)
                if m > GameCanvas.de + 72:
                    c1 = 255 - (m - GameCanvas.de + 72 << 4) & 0xFFFF
                elif m < GameCanvas.de - 72:
                    c1 = 255 - (GameCanvas.de - 72 - m << 4) & 0xFFFF
                else:
                    c1 = 255
                Gfx.a_Lg(GameCanvas.bv)
                self.b_TII(GameCanvas.dp[0][j_], m + 1, 30)
                GameCanvas.a_TII(GameCanvas.dp[0][j_], m - 1, 1)
                if c1 == 255:
                    Gfx.a_Lg(GameCanvas.bu)
                elif c1 == 0:
                    Gfx.a_Lg(GameCanvas.bv)
                else:
                    Gfx.a_Lg(GameCanvas.bx)
                self.b_TII(GameCanvas.dp[0][j_], m, 30)
                m += 22
                j_ += 1
        self.q_I(2)

    def q_I(self, paramInt):  # ag.java:1739-1741  (soft key "Skip")
        GameCanvas.h_II(0, -1)

    @staticmethod
    def a_B(paramByte):  # ag.java:3021-3024  (width of a character)
        return GameCanvas.bu.a_C(chr(paramByte & 0xFFFF))

    def b_ABII(self, paramArrayOfbyte, paramInt1, paramInt2):  # ag.java:3100-3138  (word wrap into dp[paramInt2])
        m = 0
        i1 = 0
        i2 = 0
        b = 0
        GameCanvas.dq[paramInt2] = 0
        dp = GameCanvas.dp[paramInt2] = [None] * 120
        n_ = len(paramArrayOfbyte)
        j_ = 0
        while j_ <= n_:
            if j_ != n_:
                c = paramArrayOfbyte[j_]
                i2 += GameCanvas.a_B(c)
                if (c == 32 or c == 124) and i2 - GameCanvas.a_B(c) >= paramInt1:
                    if i1 < m:
                        i1 = j_
                    dp[b] = GameCanvas.a_ABII(paramArrayOfbyte, m, i1)
                    b += 1
                    m = i1 + 1
                    j_ = m - 1
                    i2 = 0
                elif c == 32:
                    i1 = j_
                elif c == 124:
                    dp[b] = GameCanvas.a_ABII(paramArrayOfbyte, m, j_)
                    b += 1
                    m = i1 = j_ + 1
                    i2 = 0
            elif i2 > paramInt1:
                dp[b] = GameCanvas.a_ABII(paramArrayOfbyte, m, i1)
                b += 1
                dp[b] = GameCanvas.a_ABII(paramArrayOfbyte, i1 + 1, j_)
                b += 1
            elif i1 != n_ - 1:
                dp[b] = GameCanvas.a_ABII(paramArrayOfbyte, m, j_)
                b += 1
            j_ += 1
        if b >= 1:
            GameCanvas.dq[paramInt2] = i8(b - 1)
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
        return GameCanvas.e_II(paramInt1, paramInt2).encode("latin-1")

    @staticmethod
    def e_II(paramInt1, paramInt2):  # ag.java:1747-1753  (string paramInt2 of edat file paramInt1)
        al1 = ScrTable("/" + GameCanvas.bE.a_I(paramInt1))
        str_ = al1.a_I(paramInt2)
        al1.a_v()
        return str_

    def e_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:1828-1830  (small number, ct[20])
        self.a_IIIIIMIII(paramInt1, paramInt2, paramInt3, 9, 12, GameCanvas.ct[20], 0, 0, 0)

    def a_IIIIIMIII(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramImage,
                    paramInt6, paramInt7, paramInt8):  # ag.java:1832-1845  (number from a digit strip)
        if paramInt1 < 0 or paramImage is None:
            return
        paramInt2 -= paramInt4
        if paramInt1 > 0:
            while paramInt1 > 0:
                # DECOMP-FIX F10: `p6 + p4 * p1 % 10` -> `p6 + p4 * (p1 % 10)`
                sx = paramInt6 + paramInt4 * (paramInt1 % 10) if F10 else paramInt6 + paramInt4 * paramInt1 % 10
                GameCanvas.a_IIIIMII(paramInt2, paramInt3, paramInt4, paramInt5, paramImage, sx, paramInt7)
                paramInt1 //= 10
                paramInt2 -= paramInt4 + paramInt8
            return
        GameCanvas.a_IIIIMII(paramInt2, paramInt3, paramInt4, paramInt5, paramImage, paramInt6, paramInt7)

    def i_II(self, paramInt1, paramInt2):  # ag.java:3169-3173  (empty 30x30 item slot)
        ac1 = Rect(paramInt1 + 1, paramInt2 + 1, 28, 28)
        self.b_IIIIIII(paramInt1, paramInt2, 30, 30, 80, 80, 80)
        Gfx.b_IIIII(ac1.a, ac1.b, ac1.c, ac1.d, 0)

    def e_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # ag.java:3175-3179  (grey frame, black inside)
        ac1 = Rect(paramInt1 + 1, paramInt2 + 1, paramInt3 - 2, paramInt4 - 2)
        self.b_IIIIIII(paramInt1, paramInt2, paramInt3, paramInt4, 152, 152, 152)
        Gfx.b_IIIII(ac1.a, ac1.b, ac1.c, ac1.d, 0)

    def y_I(self, paramInt):  # ag.java:2474-2520  (Options: change the value of row cM[1])
        v = GameCanvas.cM[1]
        if v == 0:
            GameCanvas.df = not GameCanvas.df
            if GameCanvas.df:
                self.a__I(8)
            else:
                GameCanvas.ai()
        elif v == 1:
            if paramInt == 1:
                GameCanvas.dg = i16(GameCanvas.dg + 25)
                if GameCanvas.dg > 100:
                    GameCanvas.dg = 0
            elif paramInt == 0:
                GameCanvas.dg = i16(GameCanvas.dg - 25)
                if GameCanvas.dg < 0 or GameCanvas.dg > 100:
                    GameCanvas.dg = 100
            if GameCanvas.dg == 0:
                GameCanvas.df = False
                GameCanvas.ai()
            elif GameCanvas.dg > 0:
                GameCanvas.df = True
                if system.currentTimeMillis() - GameCanvas.di > 300:
                    GameCanvas.di = system.currentTimeMillis()
                    self.a__I(8)
        elif v == 2:
            if paramInt != 0:
                GameCanvas.dh = i16(GameCanvas.dh + 1)
                if GameCanvas.dh > 4:
                    GameCanvas.dh = 0
            else:
                GameCanvas.dh = i16(GameCanvas.dh - 1)
                if GameCanvas.dh < 0:
                    GameCanvas.dh = 4
        GameCanvas.H_v()

    # ---- Management: items, descriptions ---------------------------------------------------

    @staticmethod
    def g_I(paramInt):  # ag.java:867-870  (equipment slot type of an item)
        GameCanvas.bb.e_I(paramInt)
        if paramInt < 100:
            return 1
        if paramInt < 300:
            return i8(GameCanvas.cX.b)
        if paramInt < 500:
            return GameCanvas.cY.b
        return GameCanvas.cZ.b

    @staticmethod
    def a_LzZI(paramz, paramBoolean, paramInt):  # ag.java:1454-1457  (item description in the shop)
        # dF.a() (ak.java:10-17) - the method is shadowed by the field ak.a in Python
        dF = GameCanvas.dF
        dF.a = 0
        dF.b.a = dF.b.b = dF.b.c = dF.b.d = 0
        dF.c = ""
        GameCanvas.bb.a_LzIIIIIZ(paramz, 0, 0, 200, 22, paramInt, paramBoolean)

    @staticmethod
    def a_Lp(paramp):  # ag.java:1459-1465  (potion slot -> item)
        z1 = Item()
        Item.a(z1)
        z1.a = paramp.a
        z1.b = paramp.b
        return z1

    def o_I(self, paramInt):  # ag.java:1467-1492  (item under the cursor of the item grid)
        z1 = Item()
        if paramInt == -1:
            paramInt = GameCanvas.fK[18]
        v = GameCanvas.fK[0]
        if v == 0:
            z1 = GameCanvas.fL[paramInt]
        elif v == 1:
            if paramInt < 5:
                z1 = GameCanvas.a_Lp(GameCanvas.cz.Z[paramInt])
            else:
                z1 = GameCanvas.cz.Y[paramInt - 5]
        elif v in (2, 3):
            if GameCanvas.fK[27] == 0:
                z1 = GameCanvas.cz.Y[paramInt]
            else:
                z1 = GameCanvas.cz.X[paramInt]
        return z1

    @staticmethod
    def a_LacI(paramac, paramInt):  # ag.java:1507-1510  (fill rect)
        if paramac is not None:
            Gfx.b_IIIII(paramac.a, paramac.b, paramac.c, paramac.d, paramInt)

    @staticmethod
    def b_LacI(paramac, paramInt):  # ag.java:1512-1515  (outline rect)
        if paramac is not None:
            Gfx.a_IIIII(paramac.a, paramac.b, paramac.c, paramac.d, paramInt)

    @staticmethod
    def a_LacII(paramac, paramInt1, paramInt2):  # ag.java:1517-1520
        Gfx.b_IIIII(paramac.a, paramac.b, paramac.c, paramac.d, paramInt2)
        Gfx.a_IIIII(paramac.a, paramac.b, paramac.c, paramac.d, paramInt1)

    @staticmethod
    def s_I(paramInt):  # ag.java:1822-1826  (number of digits)
        arrayOfInt = [10, 100, 1000, 10000]
        b = 0
        while b < 4 and paramInt >= arrayOfInt[b]:
            b += 1
        return b + 1

    @staticmethod
    def c_T(paramString):  # ag.java:1755-1757  (text width)
        return GameCanvas.bu.a_T(paramString)

    def i_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:1823-1825  (small digit from ct[20])
        self.b_MIIIIII(GameCanvas.ct[20], paramInt1, paramInt2, 9, 12, paramInt3 * 9, 0)

    def J_v(self):  # ag.java:1279-1291  (gold box)
        arrayOfShort = [7, 14, 21, 32, 39, 46, 57, 64, 71, 82]
        j_ = GameCanvas.cz.E
        self.a_IIIIZ(GameCanvas.dd - 70, GameCanvas.de - 80 + GameCanvas.dc, 140, 22, False)
        b = 0
        while b < 9:
            j_ = idiv(j_, 10)
            if 0 == j_:
                break
            b += 1
        self.d_IIII(GameCanvas.cz.E, GameCanvas.dd + (arrayOfShort[b] >> 1) + 16 - GameCanvas.db, GameCanvas.de - 76, 0)
        self.b_MIIIIII(GameCanvas.ct[32], GameCanvas.dd - 69 - GameCanvas.db, GameCanvas.de - 80, GameCanvas.ct[32].getWidth(), GameCanvas.ct[32].getHeight(), 0, 0)

    def b_IIIII(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # ag.java:1293-1352  (description of item / skill)
        cz = GameCanvas.cz
        dF = GameCanvas.dF
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
                s6 = GameCanvas.m_I(it.a)
                s1 = it.b
                s2 = it.c
                s3 = it.d
                s4 = it.e
                s5 = i16(it.f)
                str_ = GameCanvas.l_I(it.a)
            elif paramInt1 < 2000:
                dF.c = GameCanvas.k_I(cz.Z[paramInt1 - 1200].a)
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
            GameCanvas.dD = GameCanvas.c_T(dF.c)
            if GameCanvas.dD > paramInt4 - 2:
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
        str2 = GameCanvas.a_ABII(arrayOfByte, 0, len(arrayOfByte))
        if GameCanvas.cz.W[paramInt] != 0:
            arrayOfByte = self.d_II(54, paramInt + 19)
            str1 = str2 + " / Lv" + str(GameCanvas.cz.W[paramInt]) + " " + GameCanvas.a_ABII(arrayOfByte, 0, len(arrayOfByte))
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
            str_ = (consts.aN[paramInt] + " / Recover " + str(consts.aP[paramInt % 3]) + "% of total "
                    + consts.aO[paramInt // 3])
        else:
            arrayOfByte = GameCanvas.e_II(54, 24 + paramInt).encode("latin-1")
            str_ = consts.aN[paramInt] + " / " + GameCanvas.a_ABII(arrayOfByte, 0, len(arrayOfByte))
        return str_

    @staticmethod
    def l_I(paramInt):  # ag.java:1383-1399  (special item suffix)
        return {434: " / Hp 5 Increased", 435: " / MP 3 Increased", 436: " / DEF 1 Increased",
                437: " / ATK 1 Increased", 502: " / Catherine's scarf",
                504: " / all General Visiting"}.get(paramInt, "")

    @staticmethod
    def m_I(paramInt):  # ag.java:1401-1416  (item name -> dF.c, returns the level needed)
        GameCanvas.bb.e_I(paramInt)
        if paramInt > 500:
            GameCanvas.dF.c = GameCanvas.cZ.a
            return GameCanvas.cZ.g
        if paramInt > 300:
            GameCanvas.dF.c = GameCanvas.cY.a
            return GameCanvas.cY.h
        if paramInt > 100:
            GameCanvas.dF.c = GameCanvas.cX.a
            return consts.aM[paramInt % 5]
        return 0

    # ---- Blacksmith helpers ----------------------------------------------------------------

    def c_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # ag.java:1246-1248
        GameCanvas.a_IIIIIIIZ(paramInt1 + 1, paramInt2 + 1, paramInt3 - 2, paramInt4 - 2, 0, 0, 10000536, True)

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
        self.b_MIIIIII(GameCanvas.ct[32], GameCanvas.dd - 69, paramInt2 - 5, GameCanvas.ct[32].getWidth(), GameCanvas.ct[32].getHeight(), 0, 0)

    def i_I(self, paramInt):  # ag.java:1271-1273
        self.c_II(GameCanvas.cz.E, paramInt)

    def h_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:2797-2808  (number with thousands commas)
        # DECOMP-FIX F12: the decompiled loop `do { if (!b || b % 3 != 0) continue; ... ++b; }`
        # skips every digit (the number is never drawn). Restored: comma before every 3rd digit.
        b = 0
        while True:
            if F12:
                if b != 0 and b % 3 == 0:
                    paramInt2 -= 4
                    GameCanvas.a_IIIIMII(paramInt2, paramInt3, 5, 14, GameCanvas.ct[19], 100, 0)
                paramInt2 -= 10
                GameCanvas.a_IIIIMII(paramInt2, paramInt3, 10, 14, GameCanvas.ct[19], imod(paramInt1, 10) * 10, 0)
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
        arrayOfByte = GameCanvas.v_I(48)
        j_ = 38 * GameCanvas.cq + 40
        GameCanvas.dr = 0
        for b in range(6):
            GameCanvas.ds[b] = i8(arrayOfByte[j_ + b])
            if GameCanvas.ds[b] > 0:
                m = 38 * GameCanvas.ds[b] + 10
                b1 = 0
                while b1 < 30 and arrayOfByte[m + b1] != 0:
                    b1 += 1
                GameCanvas.dt[b] = GameCanvas.a_ABII(arrayOfByte, m, m + b1)
                GameCanvas.du[b] = i8(arrayOfByte[m + 36])
                GameCanvas.dv[b] = i8(arrayOfByte[m + 37])
                GameCanvas.dr += 1
        GameCanvas.cN = GameCanvas.dr
        GameCanvas.dE = GameCanvas.dt

    def D_v(self):  # ag.java:1064-1073  (mission description -> dp[0])
        GameCanvas.dn = GameCanvas.dA[GameCanvas.dm]
        arrayOfByte1 = GameCanvas.v_I(56)
        arrayOfByte2 = self.a_ABI(arrayOfByte1, GameCanvas.du[GameCanvas.dk] + GameCanvas.dm)
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
            m = GameCanvas.a_AC(arrayOfChar)
            _arraycopy(paramArrayOfbyte, arrayOfInt1[m], arrayOfByte2, 0, arrayOfInt1[m + 1] - arrayOfInt1[m])
        else:
            _arraycopy(arrayOfByte1, 0, arrayOfByte2, 0, 1500)
        while arrayOfByte2[arrayOfInt3[1]] != 0:
            if arrayOfByte2[arrayOfInt3[1]] == 40:
                arrayOfByte3 = GameCanvas.a_ABABII(arrayOfByte3, arrayOfByte2, arrayOfInt2[1], arrayOfInt3[1])
                arrayOfInt2[1] = arrayOfInt3[1] + 1
                if b1 != 0:
                    arrayOfInt3[1] = GameCanvas.a_ABIC(arrayOfByte2, arrayOfInt3[1], ')')
                    # DECOMP-FIX F15: the source is `arrayOfInt2[1] = arrayOfInt3[1] = a(.., ')')`
                    # (one call; JD split the dup_x2 into a second search). Literally the second
                    # search skips the next "(..)" and the copy length is negative: every mission
                    # description with a numbered template (Hellgate...) throws in arraycopy.
                    if config.DECOMP_FIX["F15"]:
                        arrayOfInt2[1] = arrayOfInt3[1]
                    else:
                        arrayOfInt2[1] = GameCanvas.a_ABIC(arrayOfByte2, arrayOfInt3[1], ')')
                    arrayOfInt3[0] = GameCanvas.a_ABIC(arrayOfByte1, arrayOfInt3[0], '|')
                    arrayOfByte3 = GameCanvas.a_ABABII(arrayOfByte3, arrayOfByte1, arrayOfInt2[0], arrayOfInt3[0] - 1)
                    arrayOfInt2[0] = arrayOfInt3[0]
                    continue
                arrayOfInt3[1] = GameCanvas.a_ABIC(arrayOfByte2, arrayOfInt3[1], ')')
                arrayOfByte3 = GameCanvas.a_ABABII(arrayOfByte3, arrayOfByte2, arrayOfInt2[1], arrayOfInt3[1] - 1)
                arrayOfInt2[1] = arrayOfInt3[1]
                continue
            arrayOfInt3[1] = arrayOfInt3[1] + 1
        arrayOfByte3 = GameCanvas.a_ABABII(arrayOfByte3, arrayOfByte2, arrayOfInt2[1], arrayOfInt3[1])
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
            GameCanvas.cx[b] = None
        GameCanvas.R_v()

    def y_v(self):  # ag.java:872-967  (enter the map: bV = 3)
        cz = GameCanvas.cz
        cz.K = GameCanvas.g_I(cz.X[0].a)
        GameCanvas.ai()
        self.ah()
        GameCanvas.bb.d_v()
        self.ab_v()
        GameCanvas.bY.a = 240
        GameCanvas.bY.b = 243
        GameCanvas.db = 0
        GameCanvas.dc = 16
        GameCanvas.bV = 3
        GameCanvas.co = 2
        GameCanvas.cn = 1
        GameCanvas.cr = 0
        GameCanvas.cl = 0
        GameCanvas.fq = 0
        if GameCanvas.dj != 0:
            bool_ = 1
        else:
            if F13 and cz.a[1] is not cz.a[0]:
                # DECOMP-FIX F13: the start position is written into cz.a[1], but the map
                # (c.f(), c.a(5 ints)) reads cz.a[0]. Both are the same object once ar.aC()
                # (cz.a[1] = cz.a[0]) has run; on the first map after start-up they are not,
                # and the hero would stand at (0, 0).
                cz.a[1] = cz.a[0]
            cz.a[1].a = i16(GameCanvas.dz[GameCanvas.dm].b * 27 + 12)
            cz.a[1].b = i16(GameCanvas.dz[GameCanvas.dm].c * 27 + 20)
            GameCanvas.do = 1
            GameCanvas.dY = 0
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
        GameCanvas.O_v()
        if GameCanvas.bi:
            cz.E = 500000
            cz.y = cz.p = cz.o = cz.m = cz.w = cz.n = cz.x = cz.z = cz.r = cz.q = 2000
        GameCanvas.fh = 0
        GameCanvas.fg = 1
        GameCanvas.cR.a = 0
        GameCanvas.dT.a = 0
        GameCanvas.dU.a = 0
        GameCanvas.ek = 0
        GameCanvas.eB = 0
        GameCanvas.eX = None
        GameCanvas.fa = None
        GameCanvas.fd = None
        for b in range(2):
            if GameCanvas.et[b] is None:
                GameCanvas.et[b] = self.K_I(82 + b)
        self.h_I(bool_)
        self.A_v()
        GameCanvas.eS[cz.K] = self.K_I(87 + (cz.K << 2))
        cz.aD = self.K_I(51 + cz.aB)
        cz.aF = self.K_I(46)
        GameCanvas.eT[cz.K] = self.K_I(89 + (cz.K << 2))
        GameCanvas.ct[40 + cz.K] = self.d_T(GameCanvas.bB.a_I(42 + cz.K))
        GameCanvas.eU = self.K_I(86)
        self.z_v()
        GameCanvas.eQ = self.K_I(98)
        GameCanvas.eR = self.d_T(GameCanvas.bC.a_I(44))
        GameCanvas.eV = self.K_I(55)
        GameCanvas.ct[43] = self.d_T(GameCanvas.bC.a_I(0))
        GameCanvas.eW = self.K_I(56)
        GameCanvas.ct[44] = self.d_T(GameCanvas.bC.a_I(1))
        GameCanvas.ct[31] = self.d_T(GameCanvas.bA.a_I(52))
        GameCanvas.eq = self.d_T(GameCanvas.bB.a_I(45))
        GameCanvas.dW[1] = GameCanvas.B_v()
        GameCanvas.dW[0] = GameCanvas.B_v()
        GameCanvas.dV = GameCanvas.dW[0] - GameCanvas.dV
        GameCanvas.dW[1] = GameCanvas.B_v()
        GameCanvas.dV = GameCanvas.dW[0] = GameCanvas.B_v()
        GameCanvas.dj = 1
        GameCanvas.dX = 0

    def z_v(self):  # ag.java:969-971
        GameCanvas.ct[42] = self.d_T(GameCanvas.bC.a_I(2))

    def A_v(self):  # ag.java:973-988  (enemy sprites, recoloured by dz.d)
        arrayOfInt = [56, 57]
        for b in range(len(arrayOfInt)):
            if GameCanvas.dz[GameCanvas.dm].d != 0:
                GameCanvas.es[b] = None
                GameCanvas.et[b] = None
                GameCanvas.es[b] = GameCanvas.a_TI(GameCanvas.bB.a_I(arrayOfInt[b]), GameCanvas.dz[GameCanvas.dm].d)
            else:
                GameCanvas.es[b] = None
                GameCanvas.et[b] = None
                GameCanvas.es[b] = self.d_T(GameCanvas.bB.a_I(arrayOfInt[b]))
            if GameCanvas.et[b] is None:
                GameCanvas.et[b] = self.K_I(82 + b)

    _PAL = [[[236, 211, 197], [205, 143, 128], [129, 81, 69], [104, 60, 49], [79, 39, 29]],
            [[226, 205, 178], [196, 179, 152], [180, 142, 122], [135, 111, 47], [93, 73, 49]],
            [[174, 225, 242], [101, 156, 195], [61, 102, 139], [43, 78, 115], [45, 45, 84]],
            [[162, 199, 159], [135, 156, 119], [86, 123, 98], [33, 98, 63], [51, 51, 51]]]

    @staticmethod
    def a_TI(paramString, paramInt):  # ag.java:990-1023  (PNG with palette 0 replaced by palette paramInt)
        str_ = "/" + paramString + ".png"
        arrayOfByte = bytearray(ResReader.a(str_))
        if paramInt == 0:
            return Image.createImage(arrayOfByte, 0, len(arrayOfByte))
        arrayOfInt = GameCanvas._PAL
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
        l1 = Gfx.a_ABII(arrayOfByte, i1, i2 + 4)
        arrayOfByte[i1 + i2 + 4] = l1 >> 24 & 0xFF
        arrayOfByte[i1 + i2 + 5] = l1 >> 16 & 0xFF
        arrayOfByte[i1 + i2 + 6] = l1 >> 8 & 0xFF
        arrayOfByte[i1 + i2 + 7] = l1 & 0xFF
        return Image.createImage(arrayOfByte, 0, len(arrayOfByte))

    def h_I(self, paramInt):  # ag.java:1025-1037  (load the map of the current lord, room around the hero)
        from pow.game.map_scene import MapScene
        self.d_III(0, 0, 0)
        ct34 = GameCanvas.ct[34]
        self.a_MIIIIII(ct34, GameCanvas.bZ.a // 2 - ct34.getWidth() // 2, GameCanvas.bZ.b // 2 - ct34.getHeight() // 2,
                       ct34.getWidth(), ct34.getHeight(), 0, 0)
        GameCanvas.ck = 1
        MapScene.f_v()
        GameCanvas.cd = idiv(GameCanvas.cz.b[0].a - 1, 7) * 7 + 4 - (GameCanvas.cb.a >> 1)
        GameCanvas.ce = idiv(GameCanvas.cz.b[0].b - 1, 7) * 7 + 4 - (GameCanvas.cb.b >> 1)
        GameCanvas.cz.b[1].a = GameCanvas.cz.b[0].a
        GameCanvas.cz.b[1].b = GameCanvas.cz.b[0].b
        GameCanvas.cE = GameCanvas.bd.b_I(GameCanvas.cg)
        GameCanvas.bd.a_I(GameCanvas.ds[GameCanvas.dk])
        GameCanvas.bd.a_IIIII(GameCanvas.cb.a, GameCanvas.cb.b, GameCanvas.cd, GameCanvas.ce, paramInt)

    def ab_v(self):  # ag.java:2271-2275  (HUD frame pieces)
        arrayOfInt = [79, 61, 82, 78, 83, 81]
        for b in range(6):
            GameCanvas.cx[b] = self.d_T(GameCanvas.bA.a_I(arrayOfInt[b]))

    def g_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:2793-2795  (one digit of ct[19])
        self.b_MIIIIII(GameCanvas.ct[19], paramInt2, paramInt3, 10, 14, 10 * paramInt1, 0)

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
        self.b_MIIIIII(GameCanvas.ct[19], paramInt1 + 20 + 10, paramInt2, 4, 14, 115, 0)

    def al_(self):  # ag.java:2548-2570  (free the map images; `al` would hide the al class)
        GameCanvas.aj()
        GameCanvas.ct[4] = None
        if GameCanvas.bT is not None:
            for b1 in range(len(GameCanvas.bT)):
                GameCanvas.bT[b1] = None
            GameCanvas.bT = None
        GameCanvas.ct[9] = None
        GameCanvas.ct[11] = None
        GameCanvas.ct[12] = None
        GameCanvas.ct[16] = None
        GameCanvas.bb.d_v()
        for b in range(5):
            GameCanvas.ct[35 + b] = None
        for b in range(4):
            GameCanvas.ct[21 + b] = None
        GameCanvas.bY.a = GameCanvas.bZ.a
        GameCanvas.bY.b = GameCanvas.bZ.b
        GameCanvas.db = 0
        GameCanvas.dc = 0

    def am(self):  # ag.java:2572-2582  (start a dialogue: briefing dG 0, map talk 1, general 2)
        GameCanvas.dK = 0
        GameCanvas.dP = 0
        GameCanvas.dQ = 0
        GameCanvas.dR = 0
        GameCanvas.dS = 0
        GameCanvas.ao()
        self.an()
        if GameCanvas.dI < 200:
            self.z_I(GameCanvas.dI)

    def z_I(self, paramInt):  # ag.java:2584-2637  (line paramInt of dialogue file 57+dG -> dp[dR])
        str1 = ""
        arrayOfInt = [0] * 60
        arrayOfString = [None, None]
        s = GameCanvas.dR
        if (GameCanvas.dK & 0x1) != 0:
            if GameCanvas.dG == 0:
                str1 = GameCanvas.dA[GameCanvas.dm]
            elif GameCanvas.dG in (2, 1):
                if GameCanvas.dG == 2:          # case 2 falls through into case 1
                    if GameCanvas.cr != 0:
                        self.B_I(GameCanvas.dz[GameCanvas.dm].f)
                    else:
                        self.B_I(GameCanvas.eO[GameCanvas.eP].o)
                str1 = GameCanvas.dC.a
        else:
            str1 = GameCanvas.cz.k
        arrayOfByte2 = GameCanvas.v_I(57 + GameCanvas.dG)
        j_ = arrayOfByte2[0] & 0xFF | arrayOfByte2[1] << 8 & 0xFF00
        for b1 in range(j_ + 1):
            arrayOfInt[b1] = arrayOfByte2[2 + b1 * 2] & 0xFF | arrayOfByte2[2 + b1 * 2 + 1] << 8 & 0xFF00
        arrayOfString[0] = GameCanvas.a_ABII(arrayOfByte2, arrayOfInt[paramInt], arrayOfInt[paramInt + 1])
        arrayOfString[1] = "[" + str1 + "] "
        GameCanvas.dD = len(arrayOfString[0])
        m = 0
        for b1 in range(GameCanvas.dD):
            if arrayOfString[0][b1] == '&':
                if m != b1:
                    # System.arraycopy(String[], m, String, ...) would throw in Java; the game
                    # only prints this marker, so the texts never have '&' after other text
                    GameCanvas.b_T("=========================check this 96430jfds")
                arrayOfString[1] = arrayOfString[1] + str1
                m = b1 + 1
        str2 = ""
        for b2 in range(len(arrayOfString[0])):
            if arrayOfString[0][b2] != '&':
                str2 = str2 + arrayOfString[0][b2]
        arrayOfString[0] = str2
        if m < GameCanvas.dD:
            arrayOfString[1] = arrayOfString[1] + arrayOfString[0]
        self.b_ABII(bytearray(arrayOfString[1].encode("utf-8")), 150, s)

    def an(self):  # ag.java:2639-2681  (first line dI of the dialogue)
        from pow.game.menus import Menus
        v = GameCanvas.dG
        if v == 0:
            if GameCanvas.dH > 10:
                GameCanvas.dH = 11
                GameCanvas.dI = i16(GameCanvas.g_II(0, 18) + 10 << 1)
                return
            GameCanvas.dI = i16(GameCanvas.dH - 1 << 1)
            return
        if v == 1:
            j_ = 0
            Menus.b_II(GameCanvas.dJ, -5)
            GameCanvas.dI = 21
            return
        if v == 2:
            if GameCanvas.cr != 0:
                j_ = GameCanvas.dz[GameCanvas.dm].f
            else:
                j_ = GameCanvas.eO[GameCanvas.eP].o
            if 0 == j_:
                GameCanvas.ck = 1
                self.w_I(2)
                self.F_v()
                GameCanvas.cM[0] = 0
                GameCanvas.cN = consts.v[GameCanvas.cM[0]]
                GameCanvas.dE = GameCanvas.fU
                GameCanvas.dI = 200
                GameCanvas.bV = 2
                GameCanvas.cL = 0
                GameCanvas.cK = 0
                return
            Menus.b_II(j_, 5)
            GameCanvas.fq = j_
            j_ = GameCanvas.A_I(j_)
            if j_ >= 100:
                j_ = 95
            GameCanvas.dI = i16(j_ // 10 * 5)

    @staticmethod
    def A_I(paramInt):  # ag.java:2683-2687  (friendship points of general paramInt)
        b = 0
        while b < GameCanvas.fo and GameCanvas.fn[0][b] != paramInt:
            b += 1
        return 0 if b == GameCanvas.fo else GameCanvas.fn[1][b]

    @staticmethod
    def ao():  # ag.java:2689-2703  (position of the next speech box)
        GameCanvas.dK = i16(GameCanvas.dK + 1)
        if GameCanvas.dG != 0:
            GameCanvas.dL[GameCanvas.dR] = 60
            GameCanvas.dM[GameCanvas.dR] = i16(GameCanvas.bY.b - 39)
        elif (GameCanvas.dK & 0x1) != 0:
            GameCanvas.dL[GameCanvas.dR] = i16(GameCanvas.dd - 60 + 15 + 2)
            GameCanvas.dM[GameCanvas.dR] = i16(GameCanvas.de - 64)
        else:
            GameCanvas.dL[GameCanvas.dR] = i16(GameCanvas.dd - 60 + -40 + 2)
            GameCanvas.dM[GameCanvas.dR] = i16(GameCanvas.de - 73 + 107 + 2)
        GameCanvas.dO = 0
        GameCanvas.dN = GameCanvas.dL[GameCanvas.dR]

    def B_I(self, paramInt):  # ag.java:2705-2726  (general paramInt -> dC)
        arrayOfByte = None
        j_ = 0
        arrayOfByte = GameCanvas.v_I(46)
        j_ = 23 * (paramInt - 1) + 14
        dC = GameCanvas.dC
        dC.a = ""
        b = 0
        while b < 11 and arrayOfByte[j_ + b] != 0:
            b += 1
        dC.a = GameCanvas.a_ABII(arrayOfByte, j_, j_ + b)
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
        while b < 4 and 0 != GameCanvas.dC.d[b]:
            b += 1
        if paramInt != 0:
            while True:
                c1 = GameCanvas.dC.d[self.C_I(b)]
                if not c1 > 0o20:
                    return c1
        return GameCanvas.dC.d[self.C_I(b)]



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
    from pow.game.popups import Popups
    GameCanvas.cS = Popups()
