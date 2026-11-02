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
        GameCanvas.midlet = paramMain
        self.map_started = False  # public boolean gj = false;  ag.java:552 (instance field)
        self.setFullScreenMode(True)
        self.r_v()

    @staticmethod
    def q_v():  # ag.java:566-576
        GameCanvas.map_id = 1
        GameCanvas.key = -999
        GameCanvas.redraw = 1
        GameCanvas.chapter = 0
        GameCanvas.dir_history[4] = -1
        GameCanvas.dir_history[3] = -1
        GameCanvas.dir_history[2] = -1
        GameCanvas.dir_history[1] = -1
        GameCanvas.dir_history[0] = -1

    def r_v(self):  # ag.java:578-583
        GameCanvas.screen_w = self.getWidth()
        GameCanvas.screen_h = self.getHeight()
        GameCanvas.screen_cx = GameCanvas.screen_w // 2
        GameCanvas.screen_cy = GameCanvas.screen_h // 2

    def s_v(self):  # ag.java:585-658
        from pow.game.menus import Menus
        from pow.game.sound import Sound
        from pow.game.map_scene import MapScene
        from pow.game.live import Live
        from pow.game.live_screen import LiveScreen
        from pow.game.map_engine import MapEngine
        from pow.midp.jrandom import Random
        self.r_v()
        GameCanvas.font_white = Font("/0_font.png", 8, 17, 9, 16777215)
        GameCanvas.font_black = Font("/0_font.png", 8, 17, 9, 0)
        GameCanvas.font_orange = Font("/0_font.png", 8, 17, 9, 16400640)
        GameCanvas.font_gray = Font("/0_font.png", 8, 17, 9, 6579300)
        GameCanvas.scr_ui = ScrTable("/imgui.scr")
        GameCanvas.scr_data = ScrTable("/edat.scr")
        GameCanvas.scr_maps = ScrTable("/mdat_QVGA.scr")
        GameCanvas.scr_char = ScrTable("/imgchar.scr")
        GameCanvas.scr_effect = ScrTable("/imgeff.scr")
        GameCanvas.scr_tile = ScrTable("/imgtile.scr")
        GameCanvas.scr_gamestr = ScrTable("/gamestr.scr")
        GameCanvas.q_v()
        GameCanvas.app_version = GameCanvas.midlet.getAppProperty("MIDlet-Version") or ""
        GameCanvas.live_host = GameCanvas.midlet.getAppProperty("GAMEVIL_SERVER") or "ur.gamevil.net"
        try:
            GameCanvas.live_port = int(GameCanvas.midlet.getAppProperty("GAMEVIL_PORT"))
        except Exception:
            GameCanvas.live_port = 28230
        GameCanvas.more_games_url = GameCanvas.midlet.getAppProperty("GAMEVIL_MOREGAMES") or "http://usaapp1.gamevil.net/moregames/index2.php?bid=POW_"
        GameCanvas.multiplay_url = GameCanvas.midlet.getAppProperty("GAMEVIL_MULTIPLAY") or "http://ur.gamevil.net/moregames/pow_multiplayer.php"
        GameCanvas.cheat = GameCanvas.midlet.getAppProperty("GAMEVIL_CHEAT") == "TRUE"
        GameCanvas.debug_keys = False
        GameCanvas.canvas_size.x = i16(GameCanvas.screen_w)
        GameCanvas.canvas_size.y = i16(GameCanvas.screen_h)
        GameCanvas.view_size.x = i16(GameCanvas.screen_w)
        GameCanvas.view_size.y = i16(GameCanvas.screen_h)
        GameCanvas.view_x = 0
        GameCanvas.view_y = 0
        GameCanvas.view_cx = GameCanvas.view_size.x >> 1
        GameCanvas.view_cy = GameCanvas.view_size.y >> 1
        if GameCanvas.screen_h % 2 == 1:
            GameCanvas.view_cy += 1
        GameCanvas.x_v()
        GameCanvas.state = 0
        GameCanvas.redraw = 1
        GameCanvas.lord_count = 0
        GameCanvas.G_v()
        GameCanvas.hero.a_v()
        GameCanvas.rng = Random()
        GameCanvas.softkey_bg = self.d_T("softbg")
        GameCanvas.sound = Sound(GameCanvas.midlet)
        GameCanvas.live = Live()
        Live.screen = LiveScreen()
        GameCanvas.menus = Menus()
        GameCanvas.engine = MapEngine()               # ar.java: the map (phase 3); the combat parts raise NotPorted
        GameCanvas.scene = MapScene()                # c.java: story player, map; the combat parts raise NotPorted

    def keyPressed(self, paramInt):  # ag.java:660-662
        self.t_I(paramInt)

    def t_v(self):  # ag.java:664-685
        if GameCanvas.key == -999:
            return
        if GameCanvas.paused:
            if GameCanvas.key == -5 or GameCanvas.key == 53:
                self.a_Z(False)
            GameCanvas.key = -999
            return
        if GameCanvas.state == 0:
            if GameCanvas.boot is not None:
                GameCanvas.boot.b_v()
                return
        elif GameCanvas.state == 11:
            from pow.game.live import Live
            if not Live.busy:
                GameCanvas.live.t_I(GameCanvas.key)

    @staticmethod
    def b_T(paramString):  # ag.java:687-689
        print(" " + paramString)

    def paint(self, paramGraphics):  # ag.java:691-706  (synchronized)
        GameCanvas.painted = False
        GameCanvas.screen_g = paramGraphics
        Gfx.a_G(paramGraphics)
        if GameCanvas.paused:
            Gfx.b_IIIII(0, 0, GameCanvas.screen_w, GameCanvas.screen_h, 0)
            GameCanvas.popups.b_I(10)
            Gfx.a_Lg(GameCanvas.font_white)
            j_ = GameCanvas.view_cy - 5 - 10
            Gfx.a_TIII("RESUME", GameCanvas.screen_cx, j_ + GameCanvas.view_y + 7, 1)
            GameCanvas.painted = True
            return
        self.P_v()
        GameCanvas.painted = True

    async def run(self):  # ag.java:708-760  (Thread.run -> async loop for pygbag)
        self.s_v()
        GameCanvas.tick_start = system.currentTimeMillis()
        while GameCanvas.running and not self.quit_requested:
            try:
                GameCanvas.tick_start = system.currentTimeMillis()
                if GameCanvas.paused:
                    self.t_v()
                    self.repaint(0, 0, GameCanvas.screen_w, GameCanvas.screen_h)
                    self.serviceRepaints()
                    GameCanvas.key = -999
                    if GameCanvas.pause_pending:
                        self.b_Z(GameCanvas.pause_pending_value)
                        GameCanvas.pause_pending = False
                    await self.sleep_ms(100)
                    continue
                if GameCanvas.last_state != GameCanvas.state:
                    GameCanvas.key = -999
                else:
                    GameCanvas.key = GameCanvas.key_pressed
                GameCanvas.key_pressed = -999
                GameCanvas.frame = i32(GameCanvas.frame + 1)
                if GameCanvas.frame < 0:
                    GameCanvas.frame = 0
                if GameFields.key_delay > 0:   # private static int a  (ag.java:98)
                    GameFields.key_delay -= 1
                self.t_v()
                if GameCanvas.sound is not None:
                    GameCanvas.sound.a_v()
                self.u_v()
                GameCanvas.live.i_v()
                GameCanvas.key = -999
                if GameCanvas.pause_pending:
                    self.b_Z(GameCanvas.pause_pending_value)
                    GameCanvas.pause_pending = False
                l1 = system.currentTimeMillis()
                j_ = (consts.aQ[GameCanvas.speed] if GameCanvas.state == 3 else consts.aQ[2]) - int(l1 - GameCanvas.tick_start)
                if j_ > 20:
                    await self.sleep_ms(j_)
                else:
                    await self.sleep_ms(20)
                if GameCanvas.frame > 2:
                    GameCanvas.started = True
                GameCanvas.last_state = GameCanvas.state
            except NotPorted as np_:
                # Spike convenience: a screen of a later phase shows a popup and returns
                # to the menu instead of killing the game (config.STRICT = re-raise).
                if config.STRICT:
                    raise
                print("NotPorted:", np_)
                if GameCanvas.state in (3, 4, 5):
                    # the map / combat states have no screen yet: back to the Game Menu the
                    # way the game itself returns there (e.java:1288-1300)
                    self.w_I(2)
                    self.F_v()
                    GameCanvas.menu[0] = 0
                    GameCanvas.menu_count = consts.v[0]
                    GameCanvas.menu_items = GameCanvas.game_menu_items
                    GameCanvas.state = 2
                    GameCanvas.menu_scroll = 0
                    GameCanvas.menu_anim = 0
                    GameCanvas.redraw = 1
                elif GameCanvas.state == 2:
                    GameCanvas.menu[0] = GameCanvas.menu_return if GameCanvas.menu[0] not in (0, 5) else GameCanvas.menu[0]
                    GameCanvas.ap()
                GameCanvas.popups.a_T("3Not ported yet|(later phase)")
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
        while not GameCanvas.painted:
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
        if paramBoolean and GameCanvas.state == 3:
            self.map_started = True
        elif not paramBoolean:
            self.map_started = False
        if GameCanvas.paused == paramBoolean or GameFields.key_lock or GameFields.key_delay > 0:
            return
        if not Midlet.started or not GameCanvas.started:
            return
        GameCanvas.pause_pending = True
        GameCanvas.pause_pending_value = paramBoolean

    def b_Z(self, paramBoolean):  # ag.java:801-818
        from pow.game.sound import Sound
        GameCanvas.paused = paramBoolean
        if GameCanvas.paused:
            GameCanvas.key = -999
            if GameCanvas.sound is not None:
                Sound.players.c_v()
                return
        else:
            GameCanvas.f_I(300)
            GameCanvas.redraw = 1
            if GameCanvas.live is not None:
                from pow.game.live import Live
                Live.aJ()
            Sound.players.d_v()
            if GameCanvas.state == 2 and GameCanvas.menu[0] == 4:
                GameCanvas.redraw = 2

    @staticmethod
    def v_v():  # ag.java:820-822
        GameFields.key_lock = True

    @staticmethod
    def w_v():  # ag.java:824-827
        GameFields.key_lock = False
        GameFields.key_delay = 3

    @staticmethod
    def x_v():  # ag.java:829-865
        for b in range(2):
            GameCanvas.boss_images[b] = None
        for b in range(9):
            GameCanvas.enemy_frames[b] = None
        for b in range(len(GameCanvas.images)):
            GameCanvas.images[b] = None
        GameCanvas.hero_body_frames[1] = None
        GameCanvas.hero_body_frames[0] = None
        GameCanvas.hero_weapon_frames[1] = None
        GameCanvas.hero_weapon_frames[0] = None
        GameCanvas.trail_frames = None
        GameCanvas.shadow_image = None
        GameCanvas.spark_frames = None
        GameCanvas.skill_frames = None
        GameCanvas.hero_fx_frames = None
        GameCanvas.enemy_fx_frames = None
        GameCanvas.fire_frames = None
        GameCanvas.map.data = None
        GameCanvas.effect.frame_data = None
        GameCanvas.effect.frames = None
        GameCanvas.hero.head_frames = GameCanvas.hero.body_frames = None
        GameCanvas.hero.head_image = None
        GameCanvas.hero.body_image = None
        GameCanvas.gear_data = GameCanvas.rare_data = GameCanvas.treasure_data = None
        GameCanvas.difficulty = 0
        GameCanvas.popups.kind = 0
        GameCanvas.speed = 2
        for b in range(30):
            GameCanvas.menu_cursors[b] = 0
            GameCanvas.menu_tops[b] = 0
        GameCanvas.gear_def = GearDef()
        GameCanvas.treasure_def = TreasureDef()
        GameCanvas.rare_def = RareDef()

    @staticmethod
    def a_IIT(paramInt1, paramInt2, paramString):  # ag.java:1144-1147
        if paramString is not None:
            Gfx.a_TIII(paramString, paramInt1, paramInt2, 0)

    @staticmethod
    def b_IIT(paramInt1, paramInt2, paramString):  # ag.java:1149-1152
        if paramString is not None:
            Gfx.a_TIII(paramString, paramInt1, paramInt2, 1)

    def E_v(self):  # ag.java:1154-1163  (title picture = title_1..4 stacked)
        if GameCanvas.images[30] is None:
            GameCanvas.images[30] = Image.createImage(240, 320)
            graphics = GameCanvas.images[30].getGraphics()
            for b in range(4):
                image = self.d_T("title_" + str(b + 1))
                graphics.drawImage(image, 0, 80 * b, 20)

    def F_v(self):  # ag.java:1165-1172
        GameCanvas.anim_step = 0
        while GameCanvas.anim_step < 4:
            GameCanvas.images[26 + GameCanvas.anim_step] = self.d_T(GameCanvas.scr_ui.a_I(73 + GameCanvas.anim_step))
            GameCanvas.anim_step += 1
        self.ad_v()

    @staticmethod
    def G_v():  # ag.java:1174-1186
        arrayOfByte = bytearray(2)
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_env", False)
            if recordStore is None or recordStore.getNumRecords() < 1:
                return
            arrayOfByte = recordStore.getRecord(1)
            GameCanvas.save_pos = len(arrayOfByte)
        except Exception:
            pass
        if GameCanvas.save_pos >= 2:
            GameCanvas.volume = i8(arrayOfByte[0])
            GameCanvas.speed = i8(arrayOfByte[1])

    @staticmethod
    def H_v():  # ag.java:1188-1201
        arrayOfByte = bytearray(2)
        arrayOfByte[0] = GameCanvas.volume & 0xFF
        arrayOfByte[1] = GameCanvas.speed & 0xFF
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_env", True)
            if recordStore.getNumRecords() == 0:
                recordStore.addRecord(arrayOfByte, 0, len(arrayOfByte))
            recordStore.setRecord(1, arrayOfByte, 0, len(arrayOfByte))
        except Exception:
            return

    @staticmethod
    def I_v():  # ag.java:1203-1210
        if GameCanvas.menu[1] < GameCanvas.menu[2]:
            GameCanvas.menu[2] = GameCanvas.menu[1]
            return
        if GameCanvas.menu[1] > GameCanvas.menu[2] + 4:
            GameCanvas.menu[2] = GameCanvas.menu[1] - 4

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
        if GameCanvas.screen_fill == 0:
            self.c_III(0, 0, 0)
            self.a_MIIIIII(GameCanvas.images[7], GameCanvas.view_x, GameCanvas.view_y, GameCanvas.view_size.x, GameCanvas.view_size.y, GameCanvas.view_offset.x, GameCanvas.view_offset.y)
            return
        if GameCanvas.screen_fill == 1:
            self.c_III(0, 0, 0)
            return
        if GameCanvas.screen_fill == 2:
            self.c_III(255, 255, 255)

    def c_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:1433-1435
        Gfx.b_IIIII(GameCanvas.view_x, GameCanvas.view_y, GameCanvas.view_size.x, GameCanvas.view_size.y, GameCanvas.k_III(paramInt1, paramInt2, paramInt3))

    def L_v(self):  # ag.java:1522-1610
        # DECOMP-FIX F8: the decompiled switch at ag.java:1526-1546 has no `break`s, so every case
        # would fall through into the next (bV==0 would also run bb.a(1), bc.b(1), ...).
        # The original had one branch per state.
        if GameCanvas.redraw == 1:
            GameCanvas.redraw = 0
            v = GameCanvas.state
            if v == 12:
                self.at()
            elif v == 0:
                GameCanvas.Q_v()
            elif v == 2:
                GameCanvas.menus.a_I(1)
            elif v == 3:
                GameCanvas.engine.b_I(1)
            elif v == 4:
                GameCanvas.engine.k_v()
            elif v == 5:
                self.K_v()
                for b in range(81):
                    GameCanvas.dirty[b // 9][b % 9] = 1
                GameCanvas.scene.c_v()
                GameCanvas.menus.h_v()
            elif v in (6, 8, 9):
                return
            elif v == 10:
                if (GameCanvas.story_ending == 0 and GameCanvas.story_page < GameCanvas.story_pages[1] - GameCanvas.story_pages[0]) or (GameCanvas.story_ending != 0 and GameCanvas.story_page >= GameCanvas.story_pages[1] - GameCanvas.story_pages[0]):
                    from pow.game.menus import Menus
                    GameCanvas.menus.e_v()
                    Gfx.a_Lg(GameCanvas.font_white)
                    if GameCanvas.story_ending != 0:
                        self.b_TII("Prologue", 2 - GameCanvas.view_y, 9)
                    else:
                        self.b_TII("Epilogue", 2 - GameCanvas.view_y, 9)
                    GameCanvas.menus.b_I(GameCanvas.story_picture)
                    if GameCanvas.speech_pos[0] > 0:
                        Menus.a_III(0, 0, 1)
                    if GameCanvas.speech_pos[1] > 0:
                        Menus.a_III(1, 0, 1)
                    self.q_I(1)
                else:
                    self.N_v()
                if GameCanvas.popups.kind != 0:
                    GameCanvas.popups.c_v()
            return
        if GameCanvas.redraw == 2:
            if GameCanvas.state == 2:
                GameCanvas.menus.a_I(2)
                return
            return
        v = GameCanvas.state
        if v == 0:
            GameCanvas.Q_v()
            return
        if v == 2:
            GameCanvas.menus.a_I(0)
            return
        if v == 3:
            GameCanvas.engine.b_I(0)
            return
        if v == 4:
            GameCanvas.engine.k_v()
            GameCanvas.engine.n_v()
            return
        if v == 5:
            GameCanvas.menus.i_v()
            return
        if v in (6, 8, 9):
            return
        if v == 10:
            if GameCanvas.popups.kind != 0:
                if GameCanvas.popups.popup_redraw != 0:
                    GameCanvas.popups.c_v()
                    return
            self.M_v()

    def a__I(self, paramInt):  # ag.java:1882-1885
        if GameCanvas.sound is not None:
            GameCanvas.sound.a__I(paramInt)

    def P_v(self):  # ag.java:1887-1933
        from pow.game.sound import Sound
        v = GameCanvas.state
        if v == 12:
            self.L_v()
            if system.currentTimeMillis() - GameCanvas.key_time > 3000:
                GameCanvas.midlet.destroyApp(True)
                GameCanvas.midlet.notifyDestroyed()
            return
        if v == 0:
            self.L_v()
        elif v == 2:
            if GameCanvas.sound is not None and GameCanvas.menu[0] < 29 and Sound.music != consts.A[GameCanvas.menu[0]] and GameCanvas.menu[0] != 20 and not GameCanvas.in_live:
                self.a__I(consts.A[GameCanvas.menu[0]])
            if GameCanvas.popups.kind != 0:
                GameCanvas.popups.b_v()
            else:
                GameCanvas.menus.a_v()
            self.L_v()
        elif v == 3:
            GameCanvas.engine.a_v()
        elif v in (4, 5):
            self.L_v()
            GameCanvas.engine.O_I(0)
        elif v == 10:
            if GameCanvas.popups.kind != 0:
                GameCanvas.popups.b_v()
            self.L_v()
        elif v == 11:
            if GameCanvas.live is not None:
                from pow.game.live import Live
                Live.aK()
        if GameCanvas.live is not None:
            from pow.game.live import Live
            if Live.busy:
                GameCanvas.live.j_v()
        GameCanvas.key_held = -999

    @staticmethod
    def Q_v():  # ag.java:1935-1939
        from pow.game.boot import Boot
        if GameCanvas.boot is None:
            GameCanvas.boot = Boot()
        GameCanvas.boot.a_v()

    def t_I(self, paramInt):  # ag.java:1941-1961
        if paramInt == -10:
            return
        if GameCanvas.paused:
            GameCanvas.key = paramInt
            return
        GameCanvas.key_pressed = paramInt
        if paramInt in (-4, -3, -2, -1, 50, 52, 54, 56):
            GameCanvas.key_held = paramInt

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
        Gfx.b_IIIII(0, 0, GameCanvas.screen_w, GameCanvas.screen_h, paramInt)

    def S_v(self):  # ag.java:1985-1996  (title screen)
        if GameCanvas.images[30] is None:
            return
        GameCanvas.a_IIIIMII(0, 0, GameCanvas.canvas_size.x, GameCanvas.canvas_size.y, GameCanvas.images[30], 0, 0)
        if GameCanvas.title_press is None:
            GameCanvas.title_press = self.d_T(GameCanvas.scr_ui.a_I(36))
        GameCanvas.a_IIIIMII(GameCanvas.view_cx - 66 + GameCanvas.view_x, GameCanvas.canvas_size.y - 20, 132, 14, GameCanvas.title_press, 0, 0)
        if GameCanvas.title_logo is None:
            GameCanvas.title_logo = self.d_T(GameCanvas.scr_ui.a_I(42))
        if GameCanvas.frame % 6 < 3 and GameCanvas.state == 0:
            GameCanvas.a_IIIIMII(GameCanvas.view_cx - 55 + GameCanvas.view_x, GameCanvas.canvas_size.y - 60, 110, 14, GameCanvas.title_logo, 0, 0)

    def a_TIIIIII(self, paramString, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # ag.java:1998-2002
        image = self.d_T(paramString)
        if image is not None:
            GameCanvas.a_IIIIMII(paramInt1, paramInt2, paramInt3, paramInt4, image, paramInt5, paramInt6)

    def T_v(self):  # ag.java:2004-2124  (title -> Main Menu)
        cz = GameCanvas.hero
        for b in range(8):
            q = consts.aT[b]
            cz.anim_0[b] = consts.B[q]
            cz.anim_1[b] = consts.C[q]
            cz.anim_2[b] = consts.D[q]
            cz.anim_9[b] = consts.E[q]
            cz.anim_3[b] = consts.F[q]
            cz.anim_4[b] = consts.G[q]
            cz.anim_5[b] = consts.H[q]
            cz.anim_6[b] = consts.I[q]
            cz.anim_7[b] = consts.J[q]
            cz.anim_8[b] = consts.K[q]
            cz.anim_10[b] = consts.L
            cz.anim_11[b] = consts.M[q]
            cz.anim_12[b] = consts.N[q]
            cz.anim_13[b] = consts.O[q]
            cz.anim_14[b] = consts.P[q]
            cz.anim_15_19[b] = consts.Q
            cz.anim_20[b] = consts.R[q]
            cz.anim_21[b] = consts.S[q]
            cz.anim_22[b] = consts.T[q]
            cz.anim_23_24[b] = consts.U
            cz.anim_25[b] = consts.V[q]
            cz.anim_26_27[b] = consts.W[q]
            cz.anim_28[b] = consts.X
            cz.anim_29[b] = consts.Y
            cz.anim_30[b] = consts.Z
            GameCanvas.head_anim[b][0] = consts.aa[q]
            GameCanvas.head_anim[b][1] = consts.ab[q]
            GameCanvas.head_anim[b][2] = consts.ac[q]
            GameCanvas.head_anim[b][3] = consts.ad[q]
            GameCanvas.head_anims[b] = GameCanvas.head_anim[b]
            GameCanvas.body_anim[b][0] = consts.ae[q]
            GameCanvas.body_anim[b][1] = consts.af[q]
            GameCanvas.body_anim[b][2] = consts.ag[q]
            GameCanvas.body_anim[b][3] = consts.ah[q]
            GameCanvas.body_anims[b] = GameCanvas.body_anim[b]
            GameCanvas.weapon_anim[b][0] = consts.aa[q]
            GameCanvas.weapon_anim[b][1] = consts.ai[q]
            GameCanvas.weapon_anim[b][2] = consts.aj[q]
            GameCanvas.weapon_anim[b][3] = consts.ak
            GameCanvas.weapon_anim[b][4] = consts.ai[q]
            GameCanvas.weapon_anim[b][5] = consts.ai[q]
            GameCanvas.weapon_anim[b][6] = consts.N[q]
            GameCanvas.weapon_anim[b][7] = consts.O[q]
            GameCanvas.weapon_anim[b][8] = consts.P[q]
            GameCanvas.weapon_anim[b][9] = consts.Q
            GameCanvas.weapon_anim[b][10] = consts.Q
            GameCanvas.weapon_anim[b][11] = consts.Q
            GameCanvas.weapon_anim[b][12] = consts.Q
            GameCanvas.weapon_anim[b][13] = consts.Q
            GameCanvas.weapon_anim[b][14] = consts.R[q]
            GameCanvas.weapon_anim[b][15] = consts.S[q]
            GameCanvas.weapon_anim[b][16] = consts.T[q]
            GameCanvas.weapon_anim[b][17] = consts.U
            GameCanvas.weapon_anim[b][18] = consts.U
            GameCanvas.weapon_anim[b][19] = consts.V[q]
            GameCanvas.weapon_anim[b][20] = consts.W[q]
            GameCanvas.weapon_anim[b][21] = consts.W[q]
            GameCanvas.weapon_anims[b] = GameCanvas.weapon_anim[b]
        GameCanvas.char_anims[0] = GameCanvas.head_anims
        GameCanvas.char_anims[1] = GameCanvas.body_anims
        GameCanvas.char_anims[2] = GameCanvas.head_anims
        GameCanvas.char_anims[3] = GameCanvas.weapon_anims
        ab = cz.anims
        (ab[0], ab[1], ab[2], ab[3], ab[4], ab[5], ab[6], ab[7], ab[8], ab[9]) = (
            cz.anim_0, cz.anim_1, cz.anim_2, cz.anim_3, cz.anim_4, cz.anim_5, cz.anim_6, cz.anim_7, cz.anim_8, cz.anim_9)
        (ab[10], ab[11], ab[12], ab[13], ab[14]) = (cz.anim_10, cz.anim_11, cz.anim_12, cz.anim_13, cz.anim_14)
        (ab[15], ab[16], ab[17], ab[18], ab[19]) = (cz.anim_15_19, cz.anim_15_19, cz.anim_15_19, cz.anim_15_19, cz.anim_15_19)
        (ab[20], ab[21], ab[22], ab[23], ab[24]) = (cz.anim_20, cz.anim_21, cz.anim_22, cz.anim_23_24, cz.anim_23_24)
        (ab[25], ab[26], ab[27], ab[28], ab[29], ab[30]) = (cz.anim_25, cz.anim_26_27, cz.anim_26_27, cz.anim_28, cz.anim_29, cz.anim_30)
        GameCanvas.view_size.x = 240
        GameCanvas.view_size.y = 243
        GameCanvas.view_tiles.x = i16(GameCanvas.view_size.x // 27 + (1 if GameCanvas.view_size.x % 27 > 0 else 0))
        GameCanvas.view_tiles.x = i16(GameCanvas.view_tiles.x + (0 if (GameCanvas.view_tiles.x & 0x1) > 0 else 1))
        GameCanvas.view_tiles.y = i16(GameCanvas.view_size.y // 27 + (1 if GameCanvas.view_size.y % 27 > 0 else 0))
        GameCanvas.view_tiles.y = i16(GameCanvas.view_tiles.y + (0 if (GameCanvas.view_tiles.y & 0x1) > 0 else 1))
        GameCanvas.view_offset.x = i16(GameCanvas.view_tiles.x * 27 - GameCanvas.view_size.x >> 1)
        GameCanvas.view_offset.y = i16(GameCanvas.view_tiles.y * 27 - GameCanvas.view_size.y >> 1)
        GameCanvas.view_size.x = GameCanvas.canvas_size.x
        GameCanvas.view_size.y = GameCanvas.canvas_size.y
        GameCanvas.view_x = 0
        GameCanvas.view_y = 0
        self.aa_v()
        GameCanvas.q_v()
        self.a__I(-1)
        GameCanvas.save_flag = 0
        self.w_I(0)
        GameCanvas.menu[0] = 5
        GameCanvas.menu_count = 10
        GameCanvas.popups.extra = 0
        self.U_v()
        GameCanvas.state = 2
        if not GameCanvas.aq():
            GameCanvas.menu[1] = 1

    def U_v(self):  # ag.java:2126-2214  (load save "gamevil_pow_data")
        cz = GameCanvas.hero
        GameCanvas.save_pos = 0
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_data", False)
            if recordStore is None or recordStore.getNumRecords() < 1:
                return
            GameCanvas.save_buf = recordStore.getRecord(1)
            GameCanvas.save_pos = GameCanvas.save_buf[0] & 0xFF | GameCanvas.save_buf[1] << 8 & 0xFF00
        except Exception:
            pass
        if GameCanvas.save_pos != 0:
            cF = GameCanvas.save_buf
            arrayOfByte1 = [0] * 16
            b2 = 0
            while b2 < 8 and cF[2 + b2] != 32:
                b2 += 1
            arrayOfByte2 = bytearray(b2)
            for b1 in range(b2):
                arrayOfByte2[b1] = cF[2 + b1]
            cz.name = GameCanvas.a_ABII(arrayOfByte2, 0, b2)
            GameCanvas.save_flag = i8(cF[18])
            GameCanvas.save_pos = 19
            GameCanvas.lord = GameCanvas.Y_v()
            GameCanvas.mission = GameCanvas.Y_v()
            GameCanvas.rooms_visited = GameCanvas.Y_v()
            GameCanvas.missions_done = GameCanvas.V_v()
            GameCanvas.lords_done = GameCanvas.V_v()
            for b1 in range(8):
                GameCanvas.stats[b1] = GameCanvas.W_v()
            GameCanvas.mission_exp = GameCanvas.W_v()
            GameCanvas.score = GameCanvas.W_v()
            for b1 in range(44):
                GameCanvas.generals[0][b1] = GameCanvas.Y_v()
                GameCanvas.generals[1][b1] = GameCanvas.Y_v()
            GameCanvas.general_count = GameCanvas.Y_v()
            for b1 in range(25):
                GameCanvas.shop[b1] = self.Z_v()
            GameCanvas.chapter = GameCanvas.Y_v()
            cz.pos[0].x = GameCanvas.X_v()
            cz.pos[0].y = GameCanvas.X_v()
            # Java int division (values are positions >= 0, so // == /)
            cz.pos[0].x = i16((cz.pos[0].x // 27 // 7 * 7 + 4) * 27 + 8)
            cz.pos[0].y = i16((cz.pos[0].y // 27 // 7 * 7 + 4) * 27 + 8)
            for b1 in range(22):
                cz.mission_progress[b1] = GameCanvas.Y_v()
            cz.live_stat1 = GameCanvas.Y_v()
            cz.live_stat2 = GameCanvas.Y_v()
            cz.level = GameCanvas.Y_v()
            if config.ORIG_BUG["B2"]:
                # ORIG-BUG B2: the level is one byte in the save (G(cz.l), ag.java:2908) read back
                # signed, so Lv128+ loaded as -128..; the rest of the game keeps it as an int
                cz.level &= 0xFF
            cz.base_attack = GameCanvas.X_v()
            cz.base_defense = GameCanvas.X_v()
            cz.base_hp = GameCanvas.X_v()
            cz.hp = GameCanvas.X_v()
            cz.base_mp = GameCanvas.X_v()
            cz.mp = GameCanvas.X_v()
            cz.gold = GameCanvas.W_v()
            if GameCanvas.cheat:
                cz.gold = 555000
            if config.GOLD is not None:   # PORT-EXTRA config.GOLD (POW_GOLD=N)
                cz.gold = i32(config.GOLD)
            cz.fame = GameCanvas.W_v()
            cz.exp = GameCanvas.W_v()
            cz.kills = GameCanvas.X_v()
            cz.stat_points = GameCanvas.X_v()
            cz.live_registered = GameCanvas.Y_v()
            for b1 in range(5):
                cz.hotkeys[b1] = GameCanvas.Y_v()
            for b1 in range(19):
                cz.skill_levels[b1] = GameCanvas.Y_v()
            for b1 in range(9):
                cz.equipped[b1] = self.Z_v()
            for b1 in range(25):
                cz.backpack[b1] = self.Z_v()
            for b1 in range(5):
                cz.quick_slots[b1].item = GameCanvas.X_v()
                cz.quick_slots[b1].count = GameCanvas.Y_v()
            cz.quick_keys[0] = GameCanvas.Y_v()
            cz.quick_keys[1] = GameCanvas.Y_v()
            cz.head = GameCanvas.Y_v()
            GameCanvas.play_time = GameCanvas.W_v()
            GameCanvas.live_time = GameCanvas.W_v()
            GameCanvas.live_gifts = GameCanvas.Y_v()
            GameCanvas.live_saved = GameCanvas.Y_v()
            GameCanvas.talk_count = GameCanvas.Y_v()
            GameCanvas.difficulty = GameCanvas.Y_v()
            for b1 in range(16):
                arrayOfByte1[b1] = GameCanvas.Y_v()
            GameCanvas.talk_points = GameCanvas.W_v()
            for b1 in range(4):
                GameCanvas.W_v()
        self.ag()

    @staticmethod
    def V_v():  # ag.java:2216-2230  (u64 LE; bytes 4..7 are sign-extended then masked)
        cF, cG = GameCanvas.save_buf, GameCanvas.save_pos
        l1 = 0
        for k_ in range(8):
            l1 |= (cF[cG + k_] & 0xFF) << (8 * k_)
        GameCanvas.save_pos += 8
        return l1 - (1 << 64) if l1 & (1 << 63) else l1

    @staticmethod
    def W_v():  # ag.java:2232-2237
        cF, cG = GameCanvas.save_buf, GameCanvas.save_pos
        j_ = cF[cG] & 0xFF | cF[cG + 1] << 8 & 0xFF00 | cF[cG + 2] << 16 & 0xFF0000 | cF[cG + 3] << 24 & 0xFF000000
        GameCanvas.save_pos += 4
        return i32(j_)

    @staticmethod
    def X_v():  # ag.java:2239-2244
        s = i16(GameCanvas.save_buf[GameCanvas.save_pos] & 0xFF | GameCanvas.save_buf[GameCanvas.save_pos + 1] << 8 & 0xFF00)
        GameCanvas.save_pos += 2
        return s

    @staticmethod
    def Y_v():  # ag.java:2246-2250
        b = i8(GameCanvas.save_buf[GameCanvas.save_pos] & 0xFF)
        GameCanvas.save_pos += 1
        return b

    def Z_v(self):  # ag.java:2252-2261
        z1 = Item()
        z1.id = GameCanvas.X_v()
        z1.attack = GameCanvas.X_v()
        z1.defense = GameCanvas.X_v()
        z1.hp = GameCanvas.X_v()
        z1.mp = GameCanvas.X_v()
        z1.enchant = GameCanvas.Y_v()
        return z1

    def aa_v(self):  # ag.java:2263-2269
        GameCanvas.images[34] = self.d_T(GameCanvas.scr_ui.a_I(22))
        GameCanvas.images[19] = self.d_T(GameCanvas.scr_ui.a_I(24))
        GameCanvas.images[20] = self.d_T(GameCanvas.scr_ui.a_I(25))
        GameCanvas.images[0] = self.d_T(GameCanvas.scr_ui.a_I(48))
        GameCanvas.images[32] = self.d_T(GameCanvas.scr_ui.a_I(37))

    @staticmethod
    def v_I(paramInt):  # ag.java:2283-2285
        return ResReader.a("/" + GameCanvas.scr_data.a_I(paramInt))

    def w_I(self, paramInt):  # ag.java:2287-2304
        self.ah()
        self.ae_v()
        if GameCanvas.images[7] is None:
            GameCanvas.images[7] = Image.createImage(GameCanvas.canvas_size.x, GameCanvas.canvas_size.y)
        GameCanvas.buffer_g = GameCanvas.images[7].getGraphics()
        GameCanvas.save_flag = 0
        GameCanvas.menu[2] = 0
        GameCanvas.menu[1] = 0
        GameCanvas.popups.kind = 0
        GameCanvas.gear_data = GameCanvas.v_I(47)
        GameCanvas.rare_data = GameCanvas.v_I(49)
        GameCanvas.treasure_data = GameCanvas.v_I(51)
        GameCanvas.af_v()
        GameCanvas.images[17] = self.d_T(GameCanvas.scr_ui.a_I(27))
        self.x_I(paramInt)
        self.ag()

    def ad_v(self):  # ag.java:2306-2311
        GameCanvas.images[1] = self.d_T(GameCanvas.scr_ui.a_I(21))
        GameCanvas.images[2] = self.d_T(GameCanvas.scr_ui.a_I(46))
        GameCanvas.images[3] = self.d_T(GameCanvas.scr_ui.a_I(43))
        GameCanvas.sparkle = self.d_T(GameCanvas.scr_ui.a_I(38))

    def ae_v(self):  # ag.java:2313-2319
        GameCanvas.images[1] = None
        GameCanvas.images[2] = None
        GameCanvas.images[3] = None
        GameCanvas.sparkle = None
        GameCanvas.R_v()

    @staticmethod
    def af_v():  # ag.java:2321-2343  (menu captions from uimenu.scr = edat[69])
        al1 = ScrTable("/" + GameCanvas.scr_data.a_I(69))
        for b in range(30):
            GameCanvas.menu_titles[b] = al1.a_I(b)
            if b < 7:
                GameCanvas.skill_names[b] = al1.a_I(b + 48)
            if b < 6:
                GameCanvas.main_menu_items[b] = al1.a_I(b + 30)
            if b < 5:
                GameCanvas.speed_names[b] = al1.a_I(b + 55)
            if b < 4:
                GameCanvas.option_names[b] = al1.a_I(b + 42)
            if b < 2:
                GameCanvas.on_off[b] = al1.a_I(b + 46)
        GameCanvas.game_menu_items[0] = al1.a_I(36)
        GameCanvas.yes_no_items[0] = al1.a_I(37)
        GameCanvas.help_items[0] = al1.a_I(38)
        GameCanvas.ok_items[0] = al1.a_I(39)
        GameCanvas.continue_items[0] = al1.a_I(40)
        GameCanvas.pause_items[0] = al1.a_I(41)
        al1.a_v()

    def x_I(self, paramInt):  # ag.java:2345-2370  (menu background into ct[7])
        if paramInt == 1:
            return
        Gfx.a_G(GameCanvas.buffer_g)
        GameCanvas.images[11] = self.d_T(GameCanvas.scr_ui.a_I(60))
        GameCanvas.images[12] = self.d_T(GameCanvas.scr_ui.a_I(61))
        GameCanvas.images[16] = self.d_T(GameCanvas.scr_ui.a_I(63))
        GameCanvas.images[9] = self.d_T(GameCanvas.scr_ui.a_I(59))
        j_ = GameCanvas.images[9].getWidth()
        m = GameCanvas.images[9].getHeight()
        b = 0
        while b * m < GameCanvas.canvas_size.y + m:
            for b1 in range(4):
                GameCanvas.c_MIIIIII(GameCanvas.images[9], 0, 0, (b & 0x1) * -31 + b1 * j_, b * m, j_, m)
            b += 1
        # Java: (W - w) * b / 2 and H / 2 * b % 2 - all operands >= 0, so // matches Java /
        for b in range(4):
            GameCanvas.c_MIIIIII(GameCanvas.images[12], 0, 0, (GameCanvas.canvas_size.x - GameCanvas.images[12].getWidth()) * b // 2, GameCanvas.canvas_size.y // 2 * b % 2,
                         GameCanvas.images[12].getWidth(), GameCanvas.images[12].getHeight())
        for b in range(4):
            GameCanvas.c_MIIIIII(GameCanvas.images[11], 0, 0, GameCanvas.canvas_size.x // 2 * b % 2, (GameCanvas.canvas_size.y - GameCanvas.images[11].getHeight()) * b // 2,
                         GameCanvas.images[11].getWidth(), GameCanvas.images[11].getHeight())
        GameCanvas.c_MIIIIII(GameCanvas.images[16], 0, 0, (GameCanvas.canvas_size.x >> 1) - GameCanvas.images[16].getWidth() // 2, 0,
                     GameCanvas.images[16].getWidth(), GameCanvas.images[16].getHeight())
        GameCanvas.images[11] = None
        GameCanvas.images[12] = None
        GameCanvas.images[16] = None
        GameCanvas.images[9] = None
        Gfx.a_G(GameCanvas.screen_g)

    def ag(self):  # ag.java:2372-2382  (compact inventory cz.Y)
        for b in range(24):
            if GameCanvas.hero.backpack[b].id == 0:
                for j_ in range(b + 1, 25):
                    if GameCanvas.hero.backpack[j_].id != 0:
                        self.a_LzLz(GameCanvas.hero.backpack[b], GameCanvas.hero.backpack[j_])
                        break

    def a_LzLz(self, paramz1, paramz2):  # ag.java:2384-2389
        z1 = Item()
        GameCanvas.b_LzLz(z1, paramz1)
        GameCanvas.b_LzLz(paramz1, paramz2)
        GameCanvas.b_LzLz(paramz2, z1)

    @staticmethod
    def b_LzLz(paramz1, paramz2):  # ag.java:2391-2398
        paramz1.id = paramz2.id
        paramz1.attack = paramz2.attack
        paramz1.defense = paramz2.defense
        paramz1.hp = paramz2.hp
        paramz1.mp = paramz2.mp
        paramz1.enchant = paramz2.enchant

    def ah(self):  # ag.java:2400-2436
        GameCanvas.hero_weapon_frames[0] = None
        GameCanvas.hero_weapon_frames[1] = None
        GameCanvas.hero.head_frames2 = None
        GameCanvas.hero.body_frames2 = None
        GameCanvas.hero_body_frames[0] = None
        GameCanvas.hero_body_frames[1] = None
        GameCanvas.images[40] = None
        GameCanvas.images[41] = None
        if GameCanvas.tile_images is not None:
            for b1 in range(len(GameCanvas.tile_images)):
                GameCanvas.tile_images[b1] = None
            GameCanvas.tile_images = None
        GameCanvas.trail_frames = None
        GameCanvas.images[42] = None
        GameCanvas.spark_frames = None
        GameCanvas.images[43] = None
        GameCanvas.shadow_image = None
        GameCanvas.shadow_frames = None
        GameCanvas.skill_frames = None
        GameCanvas.images[44] = None
        GameCanvas.images[31] = None
        GameCanvas.fire_frames = None
        GameCanvas.hero_fx_frames = None
        GameCanvas.boss_images[1] = None
        for b in range(2):
            GameCanvas.enemy_images[b] = None
        for b in range(9):
            GameCanvas.enemy_frames[b] = None
        GameCanvas.general_mark = None
        GameCanvas.view_size.x = GameCanvas.canvas_size.x
        GameCanvas.view_size.y = GameCanvas.canvas_size.y
        GameCanvas.view_x = 0
        GameCanvas.view_y = 0

    @staticmethod
    def a_IIIIMII(paramInt1, paramInt2, paramInt3, paramInt4, paramImage, paramInt5, paramInt6):  # ag.java:2438-2440
        Gfx.a_MIIIIII(paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6)

    def b_MIIIIII(self, paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # ag.java:2442-2457
        i1 = paramInt2
        if i1 > 0:
            i1 = 0
        i2 = GameCanvas.view_size.y - paramInt2 - paramInt4
        if i2 > 0:
            i2 = 0
        j_ = paramInt1
        if j_ > 0:
            j_ = 0
        m = GameCanvas.view_size.x - paramInt1 - paramInt3
        if m > 0:
            m = 0
        if paramInt4 + i1 + i2 > 0 and paramInt3 + j_ + m > 0:
            GameCanvas.a_IIIIMII(paramInt1 + GameCanvas.view_x - j_, paramInt2 - i1 + GameCanvas.view_y, paramInt3 + j_ + m, paramInt4 + i1 + i2,
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
        GameCanvas.hero.head_frames = None
        GameCanvas.hero.body_frames = None
        GameCanvas.hero.head_image = None
        GameCanvas.hero.body_image = None

    @staticmethod
    def ak():  # ag.java:2522-2546
        v = GameCanvas.menu[0]
        if v == 0:
            GameCanvas.menu_items = GameCanvas.game_menu_items
        elif v == 1:
            GameCanvas.menu_count = GameCanvas.lord_count
            GameCanvas.menu_items = GameCanvas.lord_names
        elif v == 2:
            GameCanvas.menu_count = GameCanvas.lord_mission_counts[GameCanvas.lord]
            GameCanvas.menu_items = GameCanvas.mission_names
        elif v == 7:
            GameCanvas.hero.name = None
        elif v == 10:
            GameCanvas.menu_items = GameCanvas.yes_no_items
        elif v == 13:
            GameCanvas.menu_items = GameCanvas.continue_items
            GameCanvas.images[39] = None

    @staticmethod
    def ap():  # ag.java:2728-2733
        GameCanvas.menu_count = consts.v[GameCanvas.menu[0]]
        GameCanvas.menu[1] = GameCanvas.menu_cursors[GameCanvas.menu[0]]
        GameCanvas.menu[2] = GameCanvas.menu_tops[GameCanvas.menu[0]]
        GameCanvas.redraw = 1

    @staticmethod
    def a_TII(paramString, paramInt1, paramInt2):  # ag.java:2743-2746  (centred text)
        paramInt1 += 2
        Gfx.a_TIII(paramString, GameCanvas.view_cx + GameCanvas.view_x + paramInt2, paramInt1 + GameCanvas.view_y, 1)

    def b_TII(self, paramString, paramInt1, paramInt2):  # ag.java:2748-2750
        GameCanvas.a_TII(paramString, paramInt1, 0)

    @staticmethod
    def c_TII(paramString, paramInt1, paramInt2):  # ag.java:2752-2754
        Gfx.a_TIII(paramString, paramInt1 + GameCanvas.view_x, paramInt2 + GameCanvas.view_y, 1)

    @staticmethod
    def d_TII(paramString, paramInt1, paramInt2):  # ag.java:2756-2758
        Gfx.a_TIII(paramString, paramInt1 + GameCanvas.view_x, paramInt2 + GameCanvas.view_y, 0)

    def a_IIIIZ(self, paramInt1, paramInt2, paramInt3, paramInt4, paramBoolean):  # ag.java:2760-2762
        GameCanvas.a_IIIIIIIZ(paramInt1, paramInt2, paramInt3, paramInt4, 0, 5263440, 16777215, paramBoolean)

    @staticmethod
    def a_IIIIIIIZ(paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7, paramBoolean):  # ag.java:2764-2791
        ac1 = Rect(0, 0, 0, 0)
        if paramBoolean:
            ac1.x = paramInt1 - 2
            ac1.w = paramInt3 + 4
            ac1.y = paramInt2 - 1
            ac1.h = paramInt4 + 2
            Gfx.a_IIIII(ac1.x, ac1.y, ac1.w, ac1.h, paramInt7)
            ac1.x += 1
            ac1.w -= 2
            ac1.y -= 1
            ac1.h += 2
            Gfx.a_IIIII(ac1.x, ac1.y, ac1.w, ac1.h, paramInt7)
        ac1.x = paramInt1 - 1
        ac1.w = paramInt3 + 2
        ac1.y = paramInt2
        ac1.h = paramInt4
        Gfx.a_IIIII(ac1.x, ac1.y, ac1.w, ac1.h, paramInt6)
        ac1.x += 1
        ac1.w -= 2
        ac1.y -= 1
        ac1.h += 2
        Gfx.a_IIIII(ac1.x, ac1.y, ac1.w, ac1.h, paramInt6)
        ac1.y += 1
        ac1.h -= 2
        Gfx.b_IIIII(ac1.x, ac1.y, ac1.w, ac1.h, paramInt5)

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
        GameCanvas.state = 12
        GameCanvas.redraw = 1
        GameCanvas.lord_count = 0
        GameCanvas.ai()
        GameCanvas.key_time = system.currentTimeMillis()

    def at(self):  # ag.java:3011-3019  (outro picture)
        if GameCanvas.frame == 2 or GameCanvas.frame == 5:
            GameCanvas.ai()
        GameCanvas.u_I(0)
        image = self.d_T(GameCanvas.scr_ui.a_I(0))
        j_ = image.getWidth()
        GameCanvas.a_IIIIMII(GameCanvas.screen_cx - j_ // 2, GameCanvas.screen_cy - 10, j_, 20, image, 0, 0)
        GameCanvas.a_IIIIMII(GameCanvas.screen_cx - j_ // 2, GameCanvas.screen_h - 24, j_, 22, image, 0, 20)

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
        if GameCanvas.popups.kind != 0:
            return
        j_ = GameCanvas.softkey_bg.getWidth()
        m = GameCanvas.softkey_bg.getHeight()
        str_ = ""
        if paramInt1 != -1:
            Gfx.a_Lg(GameCanvas.font_white)
            Gfx.a_MII(GameCanvas.softkey_bg, 0, GameCanvas.screen_h - m)
            i1 = len(str_ + consts.t[paramInt1]) * 10
            i2 = i1 + 4 - GameCanvas.softkey_bg.getWidth()
            if i2 > 0:
                Gfx.b_IIIII(j_ - 8, GameCanvas.screen_h - m + 2, 8, 13, 0)
                Gfx.a_MII(GameCanvas.softkey_bg, i2, GameCanvas.screen_h - m)
                Gfx.b_IIIII(i2, GameCanvas.screen_h - m + 2, 8, 13, 0)
                Gfx.a_TIII(str_ + consts.t[paramInt1], (j_ + i2) // 2, GameCanvas.screen_h - m, 1)
            else:
                Gfx.a_TIII(str_ + consts.t[paramInt1], j_ // 2, GameCanvas.screen_h - m, 1)
        if paramInt2 != -1:
            Gfx.a_Lg(GameCanvas.font_white)
            Gfx.a_MII(GameCanvas.softkey_bg, GameCanvas.screen_w - j_ - 0, GameCanvas.screen_h - m)
            i1 = len(str_ + consts.t[paramInt2]) * 10
            i2 = i1 + 15 - GameCanvas.softkey_bg.getWidth()
            if i2 > 0:
                Gfx.b_IIIII(GameCanvas.screen_w - j_ - 0, GameCanvas.screen_h - m + 2, 8, 13, 0)
                Gfx.a_MII(GameCanvas.softkey_bg, GameCanvas.screen_w - j_ - i2 - 0, GameCanvas.screen_h - m)
                Gfx.b_IIIII(GameCanvas.screen_w - i2 - 0 - 8, GameCanvas.screen_h - m + 2, 8, 13, 0)
                Gfx.a_TIII(str_ + consts.t[paramInt2], GameCanvas.screen_w - (j_ + i2) // 2 - 0, GameCanvas.screen_h - m, 1)
                return
            Gfx.a_TIII(str_ + consts.t[paramInt2], GameCanvas.screen_w - j_ // 2 - 0, GameCanvas.screen_h - m, 1)

    def l_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:3201-3203
        GameCanvas.fill_color = GameCanvas.k_III(paramInt1, paramInt2, paramInt3)

    @staticmethod
    def f_IIII(paramInt1, paramInt2, paramInt3, paramInt4):  # ag.java:3205-3207
        Gfx.c_IIIII(paramInt1, paramInt2, paramInt3, paramInt4, GameCanvas.fill_color)

    def aA(self):  # ag.java:3459-3465
        GameCanvas.aj()
        GameCanvas.hero.head_image = self.d_T(GameCanvas.scr_char.a_I(46 + GameCanvas.hero.head))
        GameCanvas.hero.head_frames = self.K_I(47 + GameCanvas.hero.head)
        GameCanvas.hero.body_image = self.d_T(GameCanvas.scr_char.a_I(44))
        GameCanvas.hero.body_frames = self.K_I(45)

    def K_I(self, paramInt):  # ag.java:3467-3482  (frame table from mdat_QVGA)
        b1 = 1
        arrayOfByte = ResReader.a("/" + GameCanvas.scr_maps.a_I(paramInt))
        n = arrayOfByte[0] & 0xFF
        arrayOfY = [None] * n
        for b2 in range(n):
            arrayOfY[b2] = SpriteFrame()
            arrayOfY[b2].src_x = GameCanvas.a_BB(arrayOfByte[b1], arrayOfByte[b1 + 1])
            arrayOfY[b2].src_y = GameCanvas.a_BB(arrayOfByte[b1 + 2], arrayOfByte[b1 + 3])
            arrayOfY[b2].w = GameCanvas.a_BB(arrayOfByte[b1 + 4], arrayOfByte[b1 + 5])
            arrayOfY[b2].h = GameCanvas.a_BB(arrayOfByte[b1 + 6], arrayOfByte[b1 + 7])
            arrayOfY[b2].ox = GameCanvas.a_BB(arrayOfByte[b1 + 8], arrayOfByte[b1 + 9])
            arrayOfY[b2].oy = GameCanvas.a_BB(arrayOfByte[b1 + 10], arrayOfByte[b1 + 11])
            b1 += 12
        return arrayOfY

    @staticmethod
    def M_I(paramInt):  # ag.java:3538-3540
        return GameCanvas.scr_gamestr.a_I(paramInt)

    @staticmethod
    def N_I(paramInt):  # ag.java:3549-3574  (key code '0'..'9' -> digit, else -1)
        if 48 <= paramInt <= 57:
            return paramInt - 48
        return -1

    @staticmethod
    def H_I(paramInt):  # ag.java:3081-3098  (add exp; returns the levels gained)
        arrayOfInt = [0] * 10
        b = 0
        paramInt += GameCanvas.hero.exp
        while True:
            j = b % 10
            if j == 0:
                arrayOfInt = GameCanvas.menus.p_v()
            j = arrayOfInt[j]
            if paramInt < j:
                GameCanvas.hero.exp = paramInt
                return b
            paramInt -= j
            GameCanvas.hero.level += 1
            GameCanvas.hero.stat_points += 3
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
        cz = GameCanvas.hero
        cz.gear_attack = cz.gear_defense = cz.gear_hp = cz.gear_mp = 0
        for b in range(9):
            if cz.equipped[b].id != 0:
                cz.gear_attack += cz.equipped[b].attack
                cz.gear_defense += cz.equipped[b].defense
                cz.gear_hp += cz.equipped[b].hp
                cz.gear_mp += cz.equipped[b].mp
        cz.attack = cz.base_attack + cz.gear_attack
        cz.defense = cz.base_defense + cz.gear_defense
        cz.max_hp = cz.hp = cz.base_hp + cz.gear_hp
        cz.max_mp = cz.mp = cz.base_mp + cz.gear_mp

    @staticmethod
    def r_I(paramInt):  # ag.java:1775-1792  (name entry: move the cursor over the 2x14 letter grid)
        j_ = paramInt
        if paramInt != -7 and paramInt != -5 and paramInt != 53:
            if paramInt == -1 or paramInt == 50:
                GameCanvas.letter_cursor = (GameCanvas.letter_cursor + 28 - 14) % 28
            elif paramInt == -2 or paramInt == 56:
                GameCanvas.letter_cursor = (GameCanvas.letter_cursor + 28 + 14) % 28
            elif paramInt == -3 or paramInt == 52:
                GameCanvas.letter_cursor = (GameCanvas.letter_cursor + 28 - 1) % 28
            elif paramInt == -4 or paramInt == 54:
                GameCanvas.letter_cursor = (GameCanvas.letter_cursor + 28 + 1) % 28
                if GameCanvas.letter_cursor == 27:
                    GameCanvas.letter_cursor = 0
        if GameCanvas.letter_cursor == 27:
            GameCanvas.letter_cursor = 26
        return j_

    _F_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                  "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                  "U", "V", "W", "X", "Y", "Z", "OK"]

    @staticmethod
    def f_II(paramInt1, paramInt2):  # ag.java:1794-1819  (letter grid A..Z + OK)
        j_ = GameCanvas.screen_cx - 71
        arrayOfString = GameCanvas._F_LETTERS
        Gfx.b_IIIII(j_, paramInt2, 142, 34, 0)
        Gfx.b_IIIII(j_ + 123, paramInt2 + 18, 19, 15, 255)
        if GameCanvas.frame % 4 < 2:
            if paramInt1 == 26:
                Gfx.b_IIIII(j_ + 123, paramInt2 + 18, 19, 15, 16711680)
            elif F10:
                # DECOMP-FIX F10: `10 * p % 14`, `17 * p / 14` -> `10 * (p % 14)`, `17 * (p / 14)`
                Gfx.b_IIIII(j_ + 2 + 10 * (paramInt1 % 14), paramInt2 + 1 + 17 * (paramInt1 // 14), 10, 15, 16711680)
            else:
                Gfx.b_IIIII(j_ + 2 + 10 * paramInt1 % 14, paramInt2 + 1 + 17 * paramInt1 // 14, 10, 15, 16711680)
        Gfx.a_Lg(GameCanvas.font_white)
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
        GameCanvas.a_IIIIMII(paramInt2 + GameCanvas.view_x, paramInt3 + GameCanvas.view_y, b1, b2, GameCanvas.images[17], b3, b4)

    @staticmethod
    def g_II(paramInt1, paramInt2):  # ag.java:2735-2737
        paramInt2 -= 1
        return paramInt1 + abs(imod(GameCanvas.rng.nextInt(), abs(paramInt2 - paramInt1) + 1))

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
                self.b_MIIIIII(GameCanvas.images[19], paramInt2, paramInt3, 5, 14, 100, 0)
            paramInt2 -= 9
            self.b_MIIIIII(GameCanvas.images[19], paramInt2, paramInt3, 10, 14, imod(paramInt1, 10) * 10, 0)
            b += 1
            paramInt1 = idiv(paramInt1, 10)
            if paramInt1 <= 0:
                return j_

    def ar(self):  # ag.java:2871-2961  (write the save "gamevil_pow_data")
        cz = GameCanvas.hero
        arrayOfChar = [0] * 16
        arrayOfByte = cz.name.encode("latin-1")
        cF = GameCanvas.save_buf
        for b in range(8):
            if b < len(arrayOfByte):
                cF[2 + b] = arrayOfByte[b]
            else:
                cF[2 + b] = 32
        cF[18] = GameCanvas.save_flag & 0xFF
        GameCanvas.save_pos = 19
        GameCanvas.G_I(GameCanvas.lord)
        GameCanvas.G_I(GameCanvas.mission)
        GameCanvas.G_I(GameCanvas.rooms_visited)
        GameCanvas.a_J(GameCanvas.missions_done)
        GameCanvas.a_J(GameCanvas.lords_done)
        for b in range(8):
            GameCanvas.E_I(i32(GameCanvas.stats[b]))
        GameCanvas.E_I(GameCanvas.mission_exp)
        GameCanvas.E_I(GameCanvas.score)
        for b in range(44):
            GameCanvas.G_I(GameCanvas.generals[0][b])
            GameCanvas.G_I(GameCanvas.generals[1][b])
        GameCanvas.G_I(GameCanvas.general_count)
        for b in range(25):
            self.a_Lz(GameCanvas.shop[b])
        GameCanvas.G_I(GameCanvas.chapter)
        GameCanvas.F_I((idiv(GameCanvas.view_tx + 2, 7) * 7 + 4) * 27)
        GameCanvas.F_I((idiv(GameCanvas.view_ty + 2, 7) * 7 + 4) * 27)
        for b in range(22):
            GameCanvas.G_I(cz.mission_progress[b])
        GameCanvas.G_I(cz.live_stat1)
        GameCanvas.G_I(cz.live_stat2)
        GameCanvas.G_I(cz.level)
        GameCanvas.F_I(cz.base_attack)
        GameCanvas.F_I(cz.base_defense)
        GameCanvas.F_I(cz.base_hp)
        GameCanvas.F_I(cz.hp)
        GameCanvas.F_I(cz.base_mp)
        GameCanvas.F_I(cz.mp)
        GameCanvas.E_I(cz.gold)
        GameCanvas.E_I(cz.fame)
        GameCanvas.E_I(cz.exp)
        GameCanvas.F_I(cz.kills)
        GameCanvas.F_I(cz.stat_points)
        GameCanvas.G_I(cz.live_registered)
        for b in range(5):
            GameCanvas.G_I(cz.hotkeys[b])
        for b in range(19):
            GameCanvas.G_I(cz.skill_levels[b])
        for b in range(9):
            self.a_Lz(cz.equipped[b])
        for b in range(25):
            self.a_Lz(cz.backpack[b])
        for b in range(5):
            GameCanvas.F_I(cz.quick_slots[b].item)
            GameCanvas.G_I(cz.quick_slots[b].count)
        GameCanvas.G_I(cz.quick_keys[0])
        GameCanvas.G_I(cz.quick_keys[1])
        GameCanvas.G_I(cz.head)
        GameCanvas.E_I(i32(GameCanvas.clock[0] - GameCanvas.play_time))
        GameCanvas.E_I(i32(GameCanvas.live_time))
        GameCanvas.G_I(GameCanvas.live_gifts)
        GameCanvas.G_I(GameCanvas.live_saved)
        GameCanvas.G_I(GameCanvas.talk_count)
        GameCanvas.G_I(GameCanvas.difficulty)
        for b in range(16):
            GameCanvas.G_I(arrayOfChar[b])
        GameCanvas.E_I(GameCanvas.talk_points)
        for b in range(4):
            GameCanvas.E_I(0)
        cF[0] = GameCanvas.save_pos & 0xFF
        cF[1] = GameCanvas.save_pos >> 8 & 0xFF
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
            GameCanvas.save_buf[GameCanvas.save_pos + k_] = paramLong >> (8 * k_) & 0xFF
        GameCanvas.save_pos += 8

    @staticmethod
    def E_I(paramInt):  # ag.java:2975-2981
        GameCanvas.save_buf[GameCanvas.save_pos] = paramInt & 0xFF
        GameCanvas.save_buf[GameCanvas.save_pos + 1] = paramInt >> 8 & 0xFF
        GameCanvas.save_buf[GameCanvas.save_pos + 2] = paramInt >> 16 & 0xFF
        GameCanvas.save_buf[GameCanvas.save_pos + 3] = paramInt >> 24 & 0xFF
        GameCanvas.save_pos += 4

    @staticmethod
    def F_I(paramInt):  # ag.java:2983-2987
        GameCanvas.save_buf[GameCanvas.save_pos] = paramInt & 0xFF
        GameCanvas.save_buf[GameCanvas.save_pos + 1] = paramInt >> 8 & 0xFF
        GameCanvas.save_pos += 2

    @staticmethod
    def G_I(paramInt):  # ag.java:2989-2992
        GameCanvas.save_buf[GameCanvas.save_pos] = paramInt & 0xFF
        GameCanvas.save_pos += 1

    def a_Lz(self, paramz):  # ag.java:2994-3001
        GameCanvas.F_I(paramz.id)
        GameCanvas.F_I(paramz.attack)
        GameCanvas.F_I(paramz.defense)
        GameCanvas.F_I(paramz.hp)
        GameCanvas.F_I(paramz.mp)
        GameCanvas.G_I(paramz.enchant)

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
        GameCanvas.menus.c_v()
        GameCanvas.menu[0] = 29
        GameCanvas.menu_count = consts.v[GameCanvas.menu[0]]
        GameCanvas.menu[1] = 1
        GameCanvas.hero.head = 0
        self.av()

    def av(self):  # ag.java:3222-3273  (fresh hero)
        cz = GameCanvas.hero
        GameCanvas.save_flag = 0
        GameCanvas.talk_count = 0
        GameCanvas.missions_done = 35113052110447
        GameCanvas.lords_done = 0
        GameCanvas.score = 0
        GameCanvas.chapter = 0
        cz.head = 0
        cz.name = ""
        for b in range(45):
            GameCanvas.generals[1][b] = 0
            GameCanvas.generals[0][b] = 0
        GameCanvas.general_count = 0
        for b in range(8):
            GameCanvas.stats[b] = 0
        cz.level = 1
        GameCanvas.aw()
        cz.fame = 0
        cz.gold = 0
        cz.exp = 0
        cz.live_registered = 0
        for b in range(22):
            cz.mission_progress[b] = 0
        cz.live_stat1 = 0
        cz.live_stat2 = 0
        for b in range(5):
            cz.hotkeys[b] = 0
            cz.quick_slots[b].item = 0
            cz.quick_slots[b].count = 0
        for b in range(19):
            cz.skill_levels[b] = 0
        cz.skill_levels[0] = 1
        cz.skill_levels[5] = 1
        cz.hotkeys[0] = 12
        cz.hotkeys[1] = 17
        if GameCanvas.cheat:
            for b in range(19):
                cz.skill_levels[b] = 1
            cz.skill_levels[18] = 1
        # z.a(): called through the class (in Java the field z.a shadowed it)
        for b in range(9):
            Item.a(cz.equipped[b])
        for b in range(25):
            Item.a(cz.backpack[b])
        self.k_II(116, 0)
        self.a_LzLz(cz.equipped[0], cz.backpack[0])
        cz.quick_keys[0] = 0
        cz.quick_keys[1] = 1

    @staticmethod
    def aw():  # ag.java:3275-3284  (base stats, 5 free points)
        cz = GameCanvas.hero
        cz.base_attack = 5
        cz.base_defense = 4
        cz.base_hp = 30
        cz.hp = 30
        cz.base_mp = 10
        cz.mp = 10
        cz.stat_points = 5
        GameCanvas.redraw = 1

    def k_II(self, paramInt1, paramInt2):  # ag.java:3286-3360  (give an item / potion / gold)
        cz = GameCanvas.hero
        b = 0
        if paramInt1 < 100:
            if paramInt2 != 0:
                b1 = -1
                b = 0
                while b < 5:
                    if cz.quick_slots[b].item == paramInt1:
                        if cz.quick_slots[b].count > 4:
                            return 0
                        break
                    if 0 == cz.quick_slots[b].item and b1 < 0:
                        b1 = b
                    b += 1
                if b1 > -1 and b > 4:
                    b = b1
                if b > 4:
                    return 0
            else:
                cz.quick_slots[GameCanvas.effect.slot].count = i16(cz.quick_slots[GameCanvas.effect.slot].count - 1)
                if cz.quick_slots[GameCanvas.effect.slot].count < 1:
                    cz.quick_slots[GameCanvas.effect.slot].item = 0
                return 1
        elif paramInt1 < 10000:
            b = 0
            while b < 25 and 0 != cz.backpack[b].id:
                b += 1
            if b > 24:
                return 0
            cz.backpack[b].id = i16(paramInt1)
            cz.backpack[b].attack = 0
            cz.backpack[b].defense = 0
            cz.backpack[b].hp = 0
            cz.backpack[b].mp = 0
            cz.backpack[b].enchant = 0
        if paramInt1 < 10000:
            GameCanvas.menus.e_I(paramInt1)
        if paramInt1 < 100:
            cz.quick_slots[b].item = i16(paramInt1)
            cz.quick_slots[b].count = i16(cz.quick_slots[b].count + 1)
        elif paramInt1 < 300:
            if paramInt2 != 0:
                s = i16(GameCanvas.gear_def.bonus + self.C_I(GameCanvas.gear_def.bonus_range + 1))
            else:
                s = GameCanvas.gear_def.bonus
            if GameCanvas.gear_def.bonus_stat == 0:
                cz.backpack[b].attack = s
            elif GameCanvas.gear_def.bonus_stat == 1:
                cz.backpack[b].defense = s
            elif GameCanvas.gear_def.bonus_stat == 2:
                cz.backpack[b].hp = s
            elif GameCanvas.gear_def.bonus_stat == 3:
                cz.backpack[b].mp = s
        elif paramInt1 < 500:
            cz.backpack[b].attack = GameCanvas.treasure_def.attack
            cz.backpack[b].defense = i16(GameCanvas.treasure_def.defense)
            cz.backpack[b].hp = GameCanvas.treasure_def.hp
            cz.backpack[b].mp = i16(GameCanvas.treasure_def.mp)
        elif paramInt1 < 10000:
            cz.backpack[b].attack = GameCanvas.rare_def.attack
            cz.backpack[b].defense = i16(GameCanvas.rare_def.defense)
            cz.backpack[b].hp = GameCanvas.rare_def.hp
            cz.backpack[b].mp = i16(GameCanvas.rare_def.mp)
        else:
            cz.gold += paramInt1 - 10000
        return 1

    @staticmethod
    def ax():  # ag.java:3362-3375  (starting quick items)
        for b in range(8):
            if GameCanvas.shop[b] is None:
                GameCanvas.shop[b] = Item()
        GameCanvas.shop[0].id = 1
        GameCanvas.shop[1].id = 2
        GameCanvas.shop[2].id = 3
        GameCanvas.shop[3].id = 4
        GameCanvas.shop[4].id = 5
        GameCanvas.shop[5].id = 6
        GameCanvas.shop[6].id = 10
        GameCanvas.shop[7].id = 11

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
            GameCanvas.shop[8 + b] = self.J_I(arrayOfInt[b])

    @staticmethod
    def az():  # ag.java:3400-3412
        arrayOfInt = [47, 51, 49]
        if not GameCanvas.tables_loaded[1]:
            for b in range(3):
                if GameCanvas.item_tables[b] is None:
                    GameCanvas.item_tables[b] = ArrTable("/" + GameCanvas.scr_data.a_I(arrayOfInt[b]))
                if GameCanvas.item_tables[b] is None:
                    return False
            GameCanvas.tables_loaded[1] = True
        return True

    @staticmethod
    def I_I(paramInt):  # ag.java:3414-3422  (item tier by hero level)
        m = 0
        b = 0
        while b < 5 and GameCanvas.hero.level >= consts.w[b]:
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
        z1.id = i16(paramInt)
        z1.enchant = 0
        if paramInt < 300:
            for b in range(3):
                arrayOfInt[b] = GameCanvas.item_tables[0].a_II(paramInt - 101, 2 + b)
            if arrayOfInt[0] == 0:
                z1.attack = i16(arrayOfInt[1] + self.C_I(arrayOfInt[2]))
            elif arrayOfInt[0] == 1:
                z1.defense = i16(arrayOfInt[1] + self.C_I(arrayOfInt[2]))
            elif arrayOfInt[0] == 2:
                z1.hp = i16(arrayOfInt[1] + self.C_I(arrayOfInt[2]))
            elif arrayOfInt[0] == 3:
                z1.mp = i16(arrayOfInt[1] + self.C_I(arrayOfInt[2]))
        else:
            tbl = GameCanvas.item_tables[1] if paramInt < 500 else GameCanvas.item_tables[2]
            # ORIG-BUG B1: the original reads both tables at id - 301, so a Rare item (shinki.arr,
            # ids 501-518) gets row 200+ -> all 0; its own row is id - 501
            first = 501 if paramInt >= 500 and config.ORIG_BUG["B1"] else 301
            for b in range(4):
                arrayOfInt[b] = tbl.a_II(paramInt - first, 2 + b)
            z1.attack = i16(arrayOfInt[0])
            z1.defense = i16(arrayOfInt[1])
            z1.hp = i16(arrayOfInt[2])
            z1.mp = i16(arrayOfInt[3])
        return z1

    def l_II(self, paramInt1, paramInt2):  # ag.java:3488-3528  (start the story player, bV = 10)
        GameCanvas.story_id = i16(paramInt1)
        if paramInt1 < 100:
            GameCanvas.story_ending = 0
            b = 64 + paramInt1 // 6
            for b1 in range(3):
                GameCanvas.story_pages[b1] = consts.aV[(paramInt1 << 1) + b1] - consts.aV[paramInt1 // 6 * 12]
            if paramInt1 == 3 and paramInt2 != 0 and 0 == GameCanvas.L_I(502):
                GameCanvas.story_pages[2] = 0
                GameCanvas.story_pages[1] = 0
                GameCanvas.story_pages[0] = 0
                GameCanvas.chapter = 4
            GameCanvas.story_picture = -1
        else:
            GameCanvas.story_ending = 1
            b = 63
            GameCanvas.story_pages[0] = 0
            GameCanvas.story_pages[1] = 2
            GameCanvas.story_pages[2] = 13
            GameCanvas.story_picture = 0
            GameCanvas.menu_items = GameCanvas.game_menu_items
            GameCanvas.menu_return = 0
        if GameCanvas.scr_story is None:
            GameCanvas.scr_story = ScrTable("/" + GameCanvas.scr_data.a_I(b))
        GameCanvas.talk_lines[1] = ""
        GameCanvas.talk_lines[0] = ""
        GameCanvas.speech_pos[1] = 0
        GameCanvas.speech_pos[0] = 0
        GameCanvas.story_page = 0
        GameCanvas.wait_ticks = 0
        GameCanvas.speech_line = 0
        GameCanvas.scene.c_I(GameCanvas.story_page)
        if 0 == GameCanvas.story_ending:
            self.x_I(1)
        GameCanvas.state = 10
        self.a__I(2)
        GameCanvas.redraw = 1

    @staticmethod
    def L_I(paramInt):  # ag.java:3530-3536  (inventory slot of item, 1-based; 0 = none)
        for b in range(25):
            if GameCanvas.hero.backpack[b].id == paramInt:
                return b + 1
        return 0

    # ---- story player (bV == 10): prologue / epilogue -------------------------------------

    def M_v(self):  # ag.java:1612-1692  (one tick of the story player)
        if GameCanvas.wait_ticks > 0:
            GameCanvas.wait_ticks = i16(GameCanvas.wait_ticks - 1)
            if GameCanvas.key != -999 and GameCanvas.wait_ticks > 3:
                GameCanvas.wait_ticks = 3
            if 0 == GameCanvas.wait_ticks:
                GameCanvas.story_page += 1
                if GameCanvas.story_page < GameCanvas.story_pages[2] - GameCanvas.story_pages[0]:
                    GameCanvas.scene.c_I(GameCanvas.story_page)
                elif 0 == GameCanvas.story_ending and GameCanvas.menu_return == 0 and GameCanvas.story_page == GameCanvas.story_pages[2] - GameCanvas.story_pages[0]:
                    if GameCanvas.reward_item != 0 or GameCanvas.reward_skill != 0:
                        GameCanvas.popups.e_I(27)
                    GameCanvas.scene.c_I(GameCanvas.story_page)
                else:
                    GameCanvas.scr_story.a_v()
                    GameCanvas.scr_story = None
                    GameCanvas.talk_lines[1] = ""
                    GameCanvas.talk_lines[0] = ""
                    self.F_v()
                    GameCanvas.menu[0] = GameCanvas.menu_return
                    GameCanvas.images[35] = None
                    GameCanvas.images[35] = None
                    GameCanvas.ap()
                    if GameCanvas.menu[0] == 0:
                        GameCanvas.menu[1] = 0
                    GameCanvas.state = 2
                    GameCanvas.menu_scroll = 0
                    GameCanvas.menu_anim = 0
                GameCanvas.redraw = 1
        elif (0 == GameCanvas.story_ending and GameCanvas.story_page < GameCanvas.story_pages[1] - GameCanvas.story_pages[0]) or (GameCanvas.story_ending != 0 and GameCanvas.story_page >= GameCanvas.story_pages[1] - GameCanvas.story_pages[0]):
            from pow.game.menus import Menus
            Menus.a_III(GameCanvas.speech_line, GameCanvas.speech_pos[GameCanvas.speech_line], 0)
            if len(GameCanvas.speech[GameCanvas.speech_line]) <= GameCanvas.speech_pos[GameCanvas.speech_line]:
                if GameCanvas.key != -999:
                    GameCanvas.wait_ticks = 0
                else:
                    GameCanvas.wait_ticks = 15
        else:
            self.N_v()
            GameCanvas.story_fade = i16(GameCanvas.story_fade + 1)
            if GameCanvas.speech_line == 0:
                if GameCanvas.story_fade > 3:
                    GameCanvas.speech_line = i16(GameCanvas.speech_line + 1)
                    GameCanvas.story_fade = 0
            elif GameCanvas.speech_line == 2:
                if GameCanvas.story_fade > 4:
                    GameCanvas.wait_ticks = 3
            elif GameCanvas.speech_line == 1:
                GameCanvas.speech_pos[0] = GameCanvas.speech_pos[0] - 2
                if GameCanvas.speech_pos[0] < -28:
                    GameCanvas.speech_pos[0] = GameCanvas.speech_pos[0] + 22
                    GameCanvas.speech_done[0] = GameCanvas.speech_done[0] + 1
                    if GameCanvas.text_line_count[0] < GameCanvas.speech_done[0]:
                        if GameCanvas.story_page == GameCanvas.story_pages[2] - GameCanvas.story_pages[0]:
                            GameCanvas.wait_ticks = 3
                        else:
                            GameCanvas.speech_line = i16(GameCanvas.speech_line + 1)
                    GameCanvas.story_fade = 1
        if GameCanvas.key == -6:
            GameCanvas.wait_ticks = 1
            if GameCanvas.story_ending != 0:
                if GameCanvas.story_page >= GameCanvas.story_pages[1] - GameCanvas.story_pages[0]:
                    GameCanvas.story_page = 100
                    return
            elif GameCanvas.story_page < GameCanvas.story_pages[1] - GameCanvas.story_pages[0]:
                GameCanvas.story_page = GameCanvas.story_pages[1] - GameCanvas.story_pages[0] - 1

    def d_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:1694-1696  (fill the screen)
        Gfx.b_IIIII(0, 0, GameCanvas.canvas_size.x, GameCanvas.canvas_size.y, GameCanvas.k_III(paramInt1, paramInt2, paramInt3))

    def N_v(self):  # ag.java:1698-1737  (story picture + scrolling text)
        self.d_III(0, 0, 0)
        ct35 = GameCanvas.images[35]
        if GameCanvas.speech_line in (0, 2):
            if 0 < GameCanvas.story_fade < 4:
                self.b_MIIIIII(ct35, GameCanvas.view_cx - (ct35.getWidth() >> 1), GameCanvas.view_cy - (ct35.getHeight() >> 1),
                               ct35.getWidth(), ct35.getHeight(), 0, 0)
        elif GameCanvas.speech_line == 1:
            m = GameCanvas.speech_pos[0]
            if GameCanvas.story_page != GameCanvas.story_pages[2] - GameCanvas.story_pages[0]:
                self.b_MIIIIII(ct35, GameCanvas.view_cx - (ct35.getWidth() >> 1), GameCanvas.view_cy - (ct35.getHeight() >> 1),
                               ct35.getWidth(), ct35.getHeight(), 0, 0)
            j_ = GameCanvas.speech_done[0]
            while j_ <= GameCanvas.text_line_count[0] and m <= 230:
                # char arithmetic, as decompiled: `255 - (m - de + 72 << 4)` (only ==255 / ==0 matter)
                if m > GameCanvas.view_cy + 72:
                    c1 = 255 - (m - GameCanvas.view_cy + 72 << 4) & 0xFFFF
                elif m < GameCanvas.view_cy - 72:
                    c1 = 255 - (GameCanvas.view_cy - 72 - m << 4) & 0xFFFF
                else:
                    c1 = 255
                Gfx.a_Lg(GameCanvas.font_black)
                self.b_TII(GameCanvas.text_lines[0][j_], m + 1, 30)
                GameCanvas.a_TII(GameCanvas.text_lines[0][j_], m - 1, 1)
                if c1 == 255:
                    Gfx.a_Lg(GameCanvas.font_white)
                elif c1 == 0:
                    Gfx.a_Lg(GameCanvas.font_black)
                else:
                    Gfx.a_Lg(GameCanvas.font_gray)
                self.b_TII(GameCanvas.text_lines[0][j_], m, 30)
                m += 22
                j_ += 1
        self.q_I(2)

    def q_I(self, paramInt):  # ag.java:1739-1741  (soft key "Skip")
        GameCanvas.h_II(0, -1)

    @staticmethod
    def a_B(paramByte):  # ag.java:3021-3024  (width of a character)
        return GameCanvas.font_white.a_C(chr(paramByte & 0xFFFF))

    def b_ABII(self, paramArrayOfbyte, paramInt1, paramInt2):  # ag.java:3100-3138  (word wrap into dp[paramInt2])
        m = 0
        i1 = 0
        i2 = 0
        b = 0
        GameCanvas.text_line_count[paramInt2] = 0
        dp = GameCanvas.text_lines[paramInt2] = [None] * 120
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
            GameCanvas.text_line_count[paramInt2] = i8(b - 1)
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
        al1 = ScrTable("/" + GameCanvas.scr_data.a_I(paramInt1))
        str_ = al1.a_I(paramInt2)
        al1.a_v()
        return str_

    def e_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:1828-1830  (small number, ct[20])
        self.a_IIIIIMIII(paramInt1, paramInt2, paramInt3, 9, 12, GameCanvas.images[20], 0, 0, 0)

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
        Gfx.b_IIIII(ac1.x, ac1.y, ac1.w, ac1.h, 0)

    def e_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # ag.java:3175-3179  (grey frame, black inside)
        ac1 = Rect(paramInt1 + 1, paramInt2 + 1, paramInt3 - 2, paramInt4 - 2)
        self.b_IIIIIII(paramInt1, paramInt2, paramInt3, paramInt4, 152, 152, 152)
        Gfx.b_IIIII(ac1.x, ac1.y, ac1.w, ac1.h, 0)

    def y_I(self, paramInt):  # ag.java:2474-2520  (Options: change the value of row cM[1])
        v = GameCanvas.menu[1]
        if v == 0:
            GameCanvas.sound_on = not GameCanvas.sound_on
            if GameCanvas.sound_on:
                self.a__I(8)
            else:
                GameCanvas.ai()
        elif v == 1:
            if paramInt == 1:
                GameCanvas.volume = i16(GameCanvas.volume + 25)
                if GameCanvas.volume > 100:
                    GameCanvas.volume = 0
            elif paramInt == 0:
                GameCanvas.volume = i16(GameCanvas.volume - 25)
                if GameCanvas.volume < 0 or GameCanvas.volume > 100:
                    GameCanvas.volume = 100
            if GameCanvas.volume == 0:
                GameCanvas.sound_on = False
                GameCanvas.ai()
            elif GameCanvas.volume > 0:
                GameCanvas.sound_on = True
                if system.currentTimeMillis() - GameCanvas.option_time > 300:
                    GameCanvas.option_time = system.currentTimeMillis()
                    self.a__I(8)
        elif v == 2:
            if paramInt != 0:
                GameCanvas.speed = i16(GameCanvas.speed + 1)
                if GameCanvas.speed > 4:
                    GameCanvas.speed = 0
            else:
                GameCanvas.speed = i16(GameCanvas.speed - 1)
                if GameCanvas.speed < 0:
                    GameCanvas.speed = 4
        GameCanvas.H_v()

    # ---- Management: items, descriptions ---------------------------------------------------

    @staticmethod
    def g_I(paramInt):  # ag.java:867-870  (equipment slot type of an item)
        GameCanvas.menus.e_I(paramInt)
        if paramInt < 100:
            return 1
        if paramInt < 300:
            return i8(GameCanvas.gear_def.slot)
        if paramInt < 500:
            return GameCanvas.treasure_def.slot
        return GameCanvas.rare_def.slot

    @staticmethod
    def a_LzZI(paramz, paramBoolean, paramInt):  # ag.java:1454-1457  (item description in the shop)
        # dF.a() (ak.java:10-17) - the method is shadowed by the field ak.a in Python
        dF = GameCanvas.info_box
        dF.shown = 0
        dF.rect.x = dF.rect.y = dF.rect.w = dF.rect.h = 0
        dF.text = ""
        GameCanvas.menus.a_LzIIIIIZ(paramz, 0, 0, 200, 22, paramInt, paramBoolean)

    @staticmethod
    def a_Lp(paramp):  # ag.java:1459-1465  (potion slot -> item)
        z1 = Item()
        Item.a(z1)
        z1.id = paramp.item
        z1.attack = paramp.count
        return z1

    def o_I(self, paramInt):  # ag.java:1467-1492  (item under the cursor of the item grid)
        z1 = Item()
        if paramInt == -1:
            paramInt = GameCanvas.cursor[18]
        v = GameCanvas.cursor[0]
        if v == 0:
            z1 = GameCanvas.shop[paramInt]
        elif v == 1:
            if paramInt < 5:
                z1 = GameCanvas.a_Lp(GameCanvas.hero.quick_slots[paramInt])
            else:
                z1 = GameCanvas.hero.backpack[paramInt - 5]
        elif v in (2, 3):
            if GameCanvas.cursor[27] == 0:
                z1 = GameCanvas.hero.backpack[paramInt]
            else:
                z1 = GameCanvas.hero.equipped[paramInt]
        return z1

    @staticmethod
    def a_LacI(paramac, paramInt):  # ag.java:1507-1510  (fill rect)
        if paramac is not None:
            Gfx.b_IIIII(paramac.x, paramac.y, paramac.w, paramac.h, paramInt)

    @staticmethod
    def b_LacI(paramac, paramInt):  # ag.java:1512-1515  (outline rect)
        if paramac is not None:
            Gfx.a_IIIII(paramac.x, paramac.y, paramac.w, paramac.h, paramInt)

    @staticmethod
    def a_LacII(paramac, paramInt1, paramInt2):  # ag.java:1517-1520
        Gfx.b_IIIII(paramac.x, paramac.y, paramac.w, paramac.h, paramInt2)
        Gfx.a_IIIII(paramac.x, paramac.y, paramac.w, paramac.h, paramInt1)

    @staticmethod
    def s_I(paramInt):  # ag.java:1822-1826  (number of digits)
        arrayOfInt = [10, 100, 1000, 10000]
        b = 0
        while b < 4 and paramInt >= arrayOfInt[b]:
            b += 1
        return b + 1

    @staticmethod
    def c_T(paramString):  # ag.java:1755-1757  (text width)
        return GameCanvas.font_white.a_T(paramString)

    def i_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:1823-1825  (small digit from ct[20])
        self.b_MIIIIII(GameCanvas.images[20], paramInt1, paramInt2, 9, 12, paramInt3 * 9, 0)

    def J_v(self):  # ag.java:1279-1291  (gold box)
        arrayOfShort = [7, 14, 21, 32, 39, 46, 57, 64, 71, 82]
        j_ = GameCanvas.hero.gold
        self.a_IIIIZ(GameCanvas.view_cx - 70, GameCanvas.view_cy - 80 + GameCanvas.view_y, 140, 22, False)
        b = 0
        while b < 9:
            j_ = idiv(j_, 10)
            if 0 == j_:
                break
            b += 1
        self.d_IIII(GameCanvas.hero.gold, GameCanvas.view_cx + (arrayOfShort[b] >> 1) + 16 - GameCanvas.view_x, GameCanvas.view_cy - 76, 0)
        self.b_MIIIIII(GameCanvas.images[32], GameCanvas.view_cx - 69 - GameCanvas.view_x, GameCanvas.view_cy - 80, GameCanvas.images[32].getWidth(), GameCanvas.images[32].getHeight(), 0, 0)

    def b_IIIII(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # ag.java:1293-1352  (description of item / skill)
        cz = GameCanvas.hero
        dF = GameCanvas.info_box
        s1 = s2 = s3 = s4 = s5 = s6 = 0
        str_ = ""
        dF.rect.x = paramInt2
        dF.rect.y = paramInt3
        dF.rect.w = paramInt4
        dF.rect.h = paramInt5
        dF.text = ""
        if paramInt1 > 999:
            if paramInt1 < 1100:
                it = cz.equipped[paramInt1 - 1000]
            elif paramInt1 < 1200:
                it = cz.backpack[paramInt1 - 1100]
            else:
                it = None
            if it is not None:
                s6 = GameCanvas.m_I(it.id)
                s1 = it.attack
                s2 = it.defense
                s3 = it.hp
                s4 = it.mp
                s5 = i16(it.enchant)
                str_ = GameCanvas.l_I(it.id)
            elif paramInt1 < 2000:
                dF.text = GameCanvas.k_I(cz.quick_slots[paramInt1 - 1200].item)
            else:
                dF.text = self.j_I(paramInt1 - 2000)
        if dF.text != "":
            if str_ != "":
                dF.text += str_
            if s1 != 0:
                dF.text += " / ATK+" + str(s1)
            if s2 != 0:
                dF.text += " / DEF+" + str(s2)
            if s3 != 0:
                dF.text += " / HP+" + str(s3)
            if s4 != 0:
                dF.text += " / MP+" + str(s4)
            if s5 != 0:
                dF.text += " / Enchanted Lv" + str(s5)
            if s6 != 0:
                dF.text += " / Available at Lv" + str(s6)
            GameCanvas.text_width = GameCanvas.c_T(dF.text)
            if GameCanvas.text_width > paramInt4 - 2:
                dF.shown = 1
                dF.text_x = i16(paramInt2 + 20)
                return
            dF.shown = 0
            dF.text_x = i16(paramInt2 + 1)

    def j_I(self, paramInt):  # ag.java:1354-1368  (skill description)
        str1 = ""
        paramInt -= 12
        if paramInt < 0 or paramInt > 18:
            return str1
        arrayOfByte = self.d_II(54, paramInt)
        str2 = GameCanvas.a_ABII(arrayOfByte, 0, len(arrayOfByte))
        if GameCanvas.hero.skill_levels[paramInt] != 0:
            arrayOfByte = self.d_II(54, paramInt + 19)
            str1 = str2 + " / Lv" + str(GameCanvas.hero.skill_levels[paramInt]) + " " + GameCanvas.a_ABII(arrayOfByte, 0, len(arrayOfByte))
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
        GameCanvas.menus.e_I(paramInt)
        if paramInt > 500:
            GameCanvas.info_box.text = GameCanvas.rare_def.name
            return GameCanvas.rare_def.level
        if paramInt > 300:
            GameCanvas.info_box.text = GameCanvas.treasure_def.name
            return GameCanvas.treasure_def.level
        if paramInt > 100:
            GameCanvas.info_box.text = GameCanvas.gear_def.name
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
        self.b_MIIIIII(GameCanvas.images[32], GameCanvas.view_cx - 69, paramInt2 - 5, GameCanvas.images[32].getWidth(), GameCanvas.images[32].getHeight(), 0, 0)

    def i_I(self, paramInt):  # ag.java:1271-1273
        self.c_II(GameCanvas.hero.gold, paramInt)

    def h_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:2797-2808  (number with thousands commas)
        # DECOMP-FIX F12: the decompiled loop `do { if (!b || b % 3 != 0) continue; ... ++b; }`
        # skips every digit (the number is never drawn). Restored: comma before every 3rd digit.
        b = 0
        while True:
            if F12:
                if b != 0 and b % 3 == 0:
                    paramInt2 -= 4
                    GameCanvas.a_IIIIMII(paramInt2, paramInt3, 5, 14, GameCanvas.images[19], 100, 0)
                paramInt2 -= 10
                GameCanvas.a_IIIIMII(paramInt2, paramInt3, 10, 14, GameCanvas.images[19], imod(paramInt1, 10) * 10, 0)
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
        j_ = 38 * GameCanvas.chapter + 40
        GameCanvas.lord_count = 0
        for b in range(6):
            GameCanvas.lord_ids[b] = i8(arrayOfByte[j_ + b])
            if GameCanvas.lord_ids[b] > 0:
                m = 38 * GameCanvas.lord_ids[b] + 10
                b1 = 0
                while b1 < 30 and arrayOfByte[m + b1] != 0:
                    b1 += 1
                GameCanvas.lord_names[b] = GameCanvas.a_ABII(arrayOfByte, m, m + b1)
                GameCanvas.lord_missions[b] = i8(arrayOfByte[m + 36])
                GameCanvas.lord_mission_counts[b] = i8(arrayOfByte[m + 37])
                GameCanvas.lord_count += 1
        GameCanvas.menu_count = GameCanvas.lord_count
        GameCanvas.menu_items = GameCanvas.lord_names

    def D_v(self):  # ag.java:1064-1073  (mission description -> dp[0])
        GameCanvas.mission_name = GameCanvas.mission_names[GameCanvas.mission]
        arrayOfByte1 = GameCanvas.v_I(56)
        arrayOfByte2 = self.a_ABI(arrayOfByte1, GameCanvas.lord_missions[GameCanvas.lord] + GameCanvas.mission)
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
            GameCanvas.hud_frame[b] = None
        GameCanvas.R_v()

    def y_v(self):  # ag.java:872-967  (enter the map: bV = 3)
        cz = GameCanvas.hero
        cz.weapon_kind = GameCanvas.g_I(cz.equipped[0].id)
        GameCanvas.ai()
        self.ah()
        GameCanvas.menus.d_v()
        self.ab_v()
        GameCanvas.view_size.x = 240
        GameCanvas.view_size.y = 243
        GameCanvas.view_x = 0
        GameCanvas.view_y = 16
        GameCanvas.state = 3
        GameCanvas.room_phase = 2
        GameCanvas.room_phase_timer = 1
        GameCanvas.boss_fight = 0
        GameCanvas.screen_fill = 0
        GameCanvas.talk_points = 0
        if GameCanvas.save_flag != 0:
            bool_ = 1
        else:
            if F13 and cz.pos[1] is not cz.pos[0]:
                # DECOMP-FIX F13: the start position is written into cz.a[1], but the map
                # (c.f(), c.a(5 ints)) reads cz.a[0]. Both are the same object once ar.aC()
                # (cz.a[1] = cz.a[0]) has run; on the first map after start-up they are not,
                # and the hero would stand at (0, 0).
                cz.pos[1] = cz.pos[0]
            cz.pos[1].x = i16(GameCanvas.lords[GameCanvas.mission].start_x * 27 + 12)
            cz.pos[1].y = i16(GameCanvas.lords[GameCanvas.mission].start_y * 27 + 20)
            GameCanvas.rooms_visited = 1
            GameCanvas.mission_exp = 0
            bool_ = 0
        cz.dir[1] = cz.facing = 0
        cz.dir[0] = cz.facing = 0
        cz.action[1] = 0
        cz.action[0] = 0
        cz.frame[1] = 0
        cz.frame[0] = 0
        cz.hit_fx_kind = 0
        cz.idle_ticks = 20
        cz.sprite_frame = 0
        cz.on_fire = 0
        cz.kills = 0
        cz.kills_shown = 0
        cz.attack_buff = 0
        cz.defense_buff = 0
        cz.attack_buff_ticks = 0
        cz.defense_buff_ticks = 0
        cz.hurt_ticks = 0
        GameCanvas.O_v()
        if GameCanvas.cheat:
            cz.gold = 500000
            cz.max_hp = cz.hp = cz.base_hp = cz.base_attack = cz.attack = cz.base_defense = cz.defense = cz.max_mp = cz.mp = cz.base_mp = 2000
        GameCanvas.hero_fx_kind = 0
        GameCanvas.hero_fx_count = 1
        GameCanvas.map_mode.mode = 0
        GameCanvas.message.shown = 0
        GameCanvas.effect.item = 0
        GameCanvas.hero_picked_up = 0
        GameCanvas.boss_spawned = 0
        GameCanvas.hero_fx_data = None
        GameCanvas.enemy_fx_data = None
        GameCanvas.fire_data = None
        for b in range(2):
            if GameCanvas.enemy_frames[b] is None:
                GameCanvas.enemy_frames[b] = self.K_I(82 + b)
        self.h_I(bool_)
        self.A_v()
        GameCanvas.hero_weapon_frames[cz.weapon_kind] = self.K_I(87 + (cz.weapon_kind << 2))
        cz.head_frames2 = self.K_I(51 + cz.head)
        cz.body_frames2 = self.K_I(46)
        GameCanvas.hero_body_frames[cz.weapon_kind] = self.K_I(89 + (cz.weapon_kind << 2))
        GameCanvas.images[40 + cz.weapon_kind] = self.d_T(GameCanvas.scr_char.a_I(42 + cz.weapon_kind))
        GameCanvas.trail_frames = self.K_I(86)
        self.z_v()
        GameCanvas.shadow_frames = self.K_I(98)
        GameCanvas.shadow_image = self.d_T(GameCanvas.scr_effect.a_I(44))
        GameCanvas.spark_frames = self.K_I(55)
        GameCanvas.images[43] = self.d_T(GameCanvas.scr_effect.a_I(0))
        GameCanvas.skill_frames = self.K_I(56)
        GameCanvas.images[44] = self.d_T(GameCanvas.scr_effect.a_I(1))
        GameCanvas.images[31] = self.d_T(GameCanvas.scr_ui.a_I(52))
        GameCanvas.general_mark = self.d_T(GameCanvas.scr_char.a_I(45))
        GameCanvas.clock[1] = GameCanvas.B_v()
        GameCanvas.clock[0] = GameCanvas.B_v()
        GameCanvas.play_time = GameCanvas.clock[0] - GameCanvas.play_time
        GameCanvas.clock[1] = GameCanvas.B_v()
        GameCanvas.play_time = GameCanvas.clock[0] = GameCanvas.B_v()
        GameCanvas.save_flag = 1
        GameCanvas.mission_seconds = 0

    def z_v(self):  # ag.java:969-971
        GameCanvas.images[42] = self.d_T(GameCanvas.scr_effect.a_I(2))

    def A_v(self):  # ag.java:973-988  (enemy sprites, recoloured by dz.d)
        arrayOfInt = [56, 57]
        for b in range(len(arrayOfInt)):
            if GameCanvas.lords[GameCanvas.mission].tint != 0:
                GameCanvas.enemy_images[b] = None
                GameCanvas.enemy_frames[b] = None
                GameCanvas.enemy_images[b] = GameCanvas.a_TI(GameCanvas.scr_char.a_I(arrayOfInt[b]), GameCanvas.lords[GameCanvas.mission].tint)
            else:
                GameCanvas.enemy_images[b] = None
                GameCanvas.enemy_frames[b] = None
                GameCanvas.enemy_images[b] = self.d_T(GameCanvas.scr_char.a_I(arrayOfInt[b]))
            if GameCanvas.enemy_frames[b] is None:
                GameCanvas.enemy_frames[b] = self.K_I(82 + b)

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
        ct34 = GameCanvas.images[34]
        self.a_MIIIIII(ct34, GameCanvas.canvas_size.x // 2 - ct34.getWidth() // 2, GameCanvas.canvas_size.y // 2 - ct34.getHeight() // 2,
                       ct34.getWidth(), ct34.getHeight(), 0, 0)
        GameCanvas.redraw = 1
        MapScene.f_v()
        GameCanvas.view_tx = idiv(GameCanvas.hero.room_pos[0].x - 1, 7) * 7 + 4 - (GameCanvas.view_tiles.x >> 1)
        GameCanvas.view_ty = idiv(GameCanvas.hero.room_pos[0].y - 1, 7) * 7 + 4 - (GameCanvas.view_tiles.y >> 1)
        GameCanvas.hero.room_pos[1].x = GameCanvas.hero.room_pos[0].x
        GameCanvas.hero.room_pos[1].y = GameCanvas.hero.room_pos[0].y
        GameCanvas.map = GameCanvas.scene.b_I(GameCanvas.map_id)
        GameCanvas.scene.a_I(GameCanvas.lord_ids[GameCanvas.lord])
        GameCanvas.scene.a_IIIII(GameCanvas.view_tiles.x, GameCanvas.view_tiles.y, GameCanvas.view_tx, GameCanvas.view_ty, paramInt)

    def ab_v(self):  # ag.java:2271-2275  (HUD frame pieces)
        arrayOfInt = [79, 61, 82, 78, 83, 81]
        for b in range(6):
            GameCanvas.hud_frame[b] = self.d_T(GameCanvas.scr_ui.a_I(arrayOfInt[b]))

    def g_III(self, paramInt1, paramInt2, paramInt3):  # ag.java:2793-2795  (one digit of ct[19])
        self.b_MIIIIII(GameCanvas.images[19], paramInt2, paramInt3, 10, 14, 10 * paramInt1, 0)

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
        self.b_MIIIIII(GameCanvas.images[19], paramInt1 + 20 + 10, paramInt2, 4, 14, 115, 0)

    def al_(self):  # ag.java:2548-2570  (free the map images; `al` would hide the al class)
        GameCanvas.aj()
        GameCanvas.images[4] = None
        if GameCanvas.tile_images is not None:
            for b1 in range(len(GameCanvas.tile_images)):
                GameCanvas.tile_images[b1] = None
            GameCanvas.tile_images = None
        GameCanvas.images[9] = None
        GameCanvas.images[11] = None
        GameCanvas.images[12] = None
        GameCanvas.images[16] = None
        GameCanvas.menus.d_v()
        for b in range(5):
            GameCanvas.images[35 + b] = None
        for b in range(4):
            GameCanvas.images[21 + b] = None
        GameCanvas.view_size.x = GameCanvas.canvas_size.x
        GameCanvas.view_size.y = GameCanvas.canvas_size.y
        GameCanvas.view_x = 0
        GameCanvas.view_y = 0

    def am(self):  # ag.java:2572-2582  (start a dialogue: briefing dG 0, map talk 1, general 2)
        GameCanvas.talk_box = 0
        GameCanvas.talk_row = 0
        GameCanvas.talk_rows = 0
        GameCanvas.talk_side = 0
        GameCanvas.wait_ticks = 0
        GameCanvas.ao()
        self.an()
        if GameCanvas.talk_line < 200:
            self.z_I(GameCanvas.talk_line)

    def z_I(self, paramInt):  # ag.java:2584-2637  (line paramInt of dialogue file 57+dG -> dp[dR])
        str1 = ""
        arrayOfInt = [0] * 60
        arrayOfString = [None, None]
        s = GameCanvas.talk_side
        if (GameCanvas.talk_box & 0x1) != 0:
            if GameCanvas.talk_kind == 0:
                str1 = GameCanvas.mission_names[GameCanvas.mission]
            elif GameCanvas.talk_kind in (2, 1):
                if GameCanvas.talk_kind == 2:          # case 2 falls through into case 1
                    if GameCanvas.boss_fight != 0:
                        self.B_I(GameCanvas.lords[GameCanvas.mission].general)
                    else:
                        self.B_I(GameCanvas.cells[GameCanvas.cell].general)
                str1 = GameCanvas.general.name
        else:
            str1 = GameCanvas.hero.name
        arrayOfByte2 = GameCanvas.v_I(57 + GameCanvas.talk_kind)
        j_ = arrayOfByte2[0] & 0xFF | arrayOfByte2[1] << 8 & 0xFF00
        for b1 in range(j_ + 1):
            arrayOfInt[b1] = arrayOfByte2[2 + b1 * 2] & 0xFF | arrayOfByte2[2 + b1 * 2 + 1] << 8 & 0xFF00
        arrayOfString[0] = GameCanvas.a_ABII(arrayOfByte2, arrayOfInt[paramInt], arrayOfInt[paramInt + 1])
        arrayOfString[1] = "[" + str1 + "] "
        GameCanvas.text_width = len(arrayOfString[0])
        m = 0
        for b1 in range(GameCanvas.text_width):
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
        if m < GameCanvas.text_width:
            arrayOfString[1] = arrayOfString[1] + arrayOfString[0]
        self.b_ABII(bytearray(arrayOfString[1].encode("utf-8")), 150, s)

    def an(self):  # ag.java:2639-2681  (first line dI of the dialogue)
        from pow.game.menus import Menus
        v = GameCanvas.talk_kind
        if v == 0:
            if GameCanvas.talk_count > 10:
                GameCanvas.talk_count = 11
                GameCanvas.talk_line = i16(GameCanvas.g_II(0, 18) + 10 << 1)
                return
            GameCanvas.talk_line = i16(GameCanvas.talk_count - 1 << 1)
            return
        if v == 1:
            j_ = 0
            Menus.b_II(GameCanvas.talk_general, -5)
            GameCanvas.talk_line = 21
            return
        if v == 2:
            if GameCanvas.boss_fight != 0:
                j_ = GameCanvas.lords[GameCanvas.mission].general
            else:
                j_ = GameCanvas.cells[GameCanvas.cell].general
            if 0 == j_:
                GameCanvas.redraw = 1
                self.w_I(2)
                self.F_v()
                GameCanvas.menu[0] = 0
                GameCanvas.menu_count = consts.v[GameCanvas.menu[0]]
                GameCanvas.menu_items = GameCanvas.game_menu_items
                GameCanvas.talk_line = 200
                GameCanvas.state = 2
                GameCanvas.menu_scroll = 0
                GameCanvas.menu_anim = 0
                return
            Menus.b_II(j_, 5)
            GameCanvas.talk_points = j_
            j_ = GameCanvas.A_I(j_)
            if j_ >= 100:
                j_ = 95
            GameCanvas.talk_line = i16(j_ // 10 * 5)

    @staticmethod
    def A_I(paramInt):  # ag.java:2683-2687  (friendship points of general paramInt)
        b = 0
        while b < GameCanvas.general_count and GameCanvas.generals[0][b] != paramInt:
            b += 1
        return 0 if b == GameCanvas.general_count else GameCanvas.generals[1][b]

    @staticmethod
    def ao():  # ag.java:2689-2703  (position of the next speech box)
        GameCanvas.talk_box = i16(GameCanvas.talk_box + 1)
        if GameCanvas.talk_kind != 0:
            GameCanvas.talk_x[GameCanvas.talk_side] = 60
            GameCanvas.talk_y[GameCanvas.talk_side] = i16(GameCanvas.view_size.y - 39)
        elif (GameCanvas.talk_box & 0x1) != 0:
            GameCanvas.talk_x[GameCanvas.talk_side] = i16(GameCanvas.view_cx - 60 + 15 + 2)
            GameCanvas.talk_y[GameCanvas.talk_side] = i16(GameCanvas.view_cy - 64)
        else:
            GameCanvas.talk_x[GameCanvas.talk_side] = i16(GameCanvas.view_cx - 60 + -40 + 2)
            GameCanvas.talk_y[GameCanvas.talk_side] = i16(GameCanvas.view_cy - 73 + 107 + 2)
        GameCanvas.talk_chars = 0
        GameCanvas.talk_cursor_x = GameCanvas.talk_x[GameCanvas.talk_side]

    def B_I(self, paramInt):  # ag.java:2705-2726  (general paramInt -> dC)
        arrayOfByte = None
        j_ = 0
        arrayOfByte = GameCanvas.v_I(46)
        j_ = 23 * (paramInt - 1) + 14
        dC = GameCanvas.general
        dC.name = ""
        b = 0
        while b < 11 and arrayOfByte[j_ + b] != 0:
            b += 1
        dC.name = GameCanvas.a_ABII(arrayOfByte, j_, j_ + b)
        dC.look = _jchar(arrayOfByte[j_ + 11])
        dC.side = _jchar(arrayOfByte[j_ + 11 + 2])
        dC.skills[0] = _jchar(arrayOfByte[j_ + 11 + 3])
        dC.skills[1] = _jchar(arrayOfByte[j_ + 11 + 4])
        dC.skills[2] = _jchar(arrayOfByte[j_ + 11 + 5])
        dC.skills[3] = _jchar(arrayOfByte[j_ + 11 + 6])
        dC.portrait = _jchar(arrayOfByte[j_ + 11 + 7])
        dC.gift_table = _jchar(arrayOfByte[j_ + 11 + 8])
        dC.attack = _jchar(arrayOfByte[j_ + 11 + 9])
        dC.defense = _jchar(arrayOfByte[j_ + 11 + 10])
        dC.hp = _jchar(arrayOfByte[j_ + 11 + 11])
        dC.side = dC.side + 1 & 0x1

    def p_I(self, paramInt):  # ag.java:1494-1505  (random skill of general dC)
        b = 0
        while b < 4 and 0 != GameCanvas.general.skills[b]:
            b += 1
        if paramInt != 0:
            while True:
                c1 = GameCanvas.general.skills[self.C_I(b)]
                if not c1 > 0o20:
                    return c1
        return GameCanvas.general.skills[self.C_I(b)]



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
    GameCanvas.popups = Popups()
