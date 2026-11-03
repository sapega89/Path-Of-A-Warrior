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
from pow.midp import display, system
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
        self.read_screen_size()

    @staticmethod
    def reset_globals():  # ag.java:566-576
        GameCanvas.map_id = 1
        GameCanvas.key = -999
        GameCanvas.redraw = 1
        GameCanvas.chapter = 0
        GameCanvas.dir_history[4] = -1
        GameCanvas.dir_history[3] = -1
        GameCanvas.dir_history[2] = -1
        GameCanvas.dir_history[1] = -1
        GameCanvas.dir_history[0] = -1

    def read_screen_size(self):  # ag.java:578-583
        GameCanvas.screen_w = self.getWidth()
        GameCanvas.screen_h = self.getHeight()
        GameCanvas.screen_cx = GameCanvas.screen_w // 2
        GameCanvas.screen_cy = GameCanvas.screen_h // 2

    def init_game(self):  # ag.java:585-658
        from pow.game.menus import Menus
        from pow.game.sound import Sound
        from pow.game.map_scene import MapScene
        from pow.game.live import Live
        from pow.game.live_screen import LiveScreen
        from pow.game.map_engine import MapEngine
        from pow.midp.jrandom import Random
        self.read_screen_size()
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
        GameCanvas.reset_globals()
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
        GameCanvas.free_images()
        GameCanvas.state = 0
        GameCanvas.redraw = 1
        GameCanvas.lord_count = 0
        GameCanvas.load_options()
        GameCanvas.hero.reset_inventory()
        GameCanvas.rng = Random()
        GameCanvas.softkey_bg = self.load_image("softbg")
        GameCanvas.sound = Sound(GameCanvas.midlet)
        GameCanvas.live = Live()
        Live.screen = LiveScreen()
        GameCanvas.menus = Menus()
        GameCanvas.engine = MapEngine()               # ar.java: the map (phase 3); the combat parts raise NotPorted
        GameCanvas.scene = MapScene()                # c.java: story player, map; the combat parts raise NotPorted

    def keyPressed(self, paramInt):  # ag.java:660-662
        self.key_down(paramInt)

    def handle_key(self):  # ag.java:664-685
        if GameCanvas.key == -999:
            return
        if GameCanvas.paused:
            if GameCanvas.key == -5 or GameCanvas.key == 53:
                self.set_paused(False)
            GameCanvas.key = -999
            return
        if GameCanvas.state == 0:
            if GameCanvas.boot is not None:
                GameCanvas.boot.boot_keys()
                return
        elif GameCanvas.state == 11:
            from pow.game.live import Live
            if not Live.busy:
                GameCanvas.live.key_down(GameCanvas.key)

    @staticmethod
    def log(paramString):  # ag.java:687-689
        print(" " + paramString)

    def paint(self, paramGraphics):  # ag.java:691-706  (synchronized)
        GameCanvas.painted = False
        GameCanvas.screen_g = paramGraphics
        Gfx.set_graphics(paramGraphics)
        if GameCanvas.paused:
            Gfx.fill_rect(0, 0, GameCanvas.screen_w, GameCanvas.screen_h, 0)
            GameCanvas.popups.draw_popup_frame(10)
            Gfx.set_font(GameCanvas.font_white)
            j_ = GameCanvas.view_cy - 5 - 10
            Gfx.draw_string("RESUME", GameCanvas.screen_cx, j_ + GameCanvas.view_y + 7, 1)
            GameCanvas.painted = True
            return
        self.tick_state()
        GameCanvas.draw_auto_badge()
        GameCanvas.painted = True

    async def run(self):  # ag.java:708-760  (Thread.run -> async loop for pygbag)
        self.init_game()
        GameCanvas.tick_start = system.currentTimeMillis()
        while GameCanvas.running and not self.quit_requested:
            try:
                GameCanvas.tick_start = system.currentTimeMillis()
                if GameCanvas.paused:
                    self.handle_key()
                    self.repaint(0, 0, GameCanvas.screen_w, GameCanvas.screen_h)
                    self.serviceRepaints()
                    GameCanvas.key = -999
                    if GameCanvas.pause_pending:
                        self.apply_pause(GameCanvas.pause_pending_value)
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
                self.handle_key()
                if GameCanvas.sound is not None:
                    GameCanvas.sound.tick_sound()
                self.repaint_and_wait()
                GameCanvas.live.tick_live()
                GameCanvas.key = -999
                if GameCanvas.pause_pending:
                    self.apply_pause(GameCanvas.pause_pending_value)
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
                    self.open_menu(2)
                    self.load_menu_frames()
                    GameCanvas.menu[0] = 0
                    GameCanvas.menu_count = consts.v[0]
                    GameCanvas.menu_items = GameCanvas.game_menu_items
                    GameCanvas.state = 2
                    GameCanvas.menu_scroll = 0
                    GameCanvas.menu_anim = 0
                    GameCanvas.redraw = 1
                elif GameCanvas.state == 2:
                    GameCanvas.menu[0] = GameCanvas.menu_return if GameCanvas.menu[0] not in (0, 5) else GameCanvas.menu[0]
                    GameCanvas.restore_menu_cursor()
                GameCanvas.popups.show_text("3Not ported yet|(later phase)")
                await self.sleep_ms(20)
            except Exception as exception:
                GameCanvas.log("--run:" + repr(exception))
                if config.DEBUG:
                    traceback.print_exc()
                    raise
                await self.sleep_ms(20)

    def repaint_and_wait(self):  # ag.java:762-767
        self.repaint()
        self.serviceRepaints()
        while not GameCanvas.painted:
            GameCanvas.sleep(20)

    @staticmethod
    def sleep(paramInt):  # ag.java:769-777
        system.sleep(paramInt)

    def hideNotify(self):  # ag.java:779-781
        self.set_paused(True)

    def showNotify(self):  # ag.java:783-785
        self.set_paused(True)

    def set_paused(self, paramBoolean):  # ag.java:787-799
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

    def apply_pause(self, paramBoolean):  # ag.java:801-818
        from pow.game.sound import Sound
        GameCanvas.paused = paramBoolean
        if GameCanvas.paused:
            GameCanvas.key = -999
            if GameCanvas.sound is not None:
                Sound.players.pause()
                return
        else:
            GameCanvas.sleep(300)
            GameCanvas.redraw = 1
            if GameCanvas.live is not None:
                from pow.game.live import Live
                Live.request_redraw()
            Sound.players.resume()
            if GameCanvas.state == 2 and GameCanvas.menu[0] == 4:
                GameCanvas.redraw = 2

    @staticmethod
    def lock_keys():  # ag.java:820-822
        GameFields.key_lock = True

    @staticmethod
    def unlock_keys():  # ag.java:824-827
        GameFields.key_lock = False
        GameFields.key_delay = 3

    @staticmethod
    def free_images():  # ag.java:829-865
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
    def draw_text_left(paramInt1, paramInt2, paramString):  # ag.java:1144-1147
        if paramString is not None:
            Gfx.draw_string(paramString, paramInt1, paramInt2, 0)

    @staticmethod
    def draw_text_centred(paramInt1, paramInt2, paramString):  # ag.java:1149-1152
        if paramString is not None:
            Gfx.draw_string(paramString, paramInt1, paramInt2, 1)

    def load_title_picture(self):  # ag.java:1154-1163  (title picture = title_1..4 stacked)
        if GameCanvas.images[30] is None:
            GameCanvas.images[30] = Image.createImage(240, 320)
            graphics = GameCanvas.images[30].getGraphics()
            for b in range(4):
                image = self.load_image("title_" + str(b + 1))
                graphics.drawImage(image, 0, 80 * b, 20)

    def load_menu_frames(self):  # ag.java:1165-1172
        GameCanvas.anim_step = 0
        while GameCanvas.anim_step < 4:
            GameCanvas.images[26 + GameCanvas.anim_step] = self.load_image(GameCanvas.scr_ui.get(73 + GameCanvas.anim_step))
            GameCanvas.anim_step += 1
        self.load_menu_images()

    @staticmethod
    def load_options():  # ag.java:1174-1186
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
    def save_options():  # ag.java:1188-1201
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
    def clamp_menu_scroll():  # ag.java:1203-1210
        if GameCanvas.menu[1] < GameCanvas.menu[2]:
            GameCanvas.menu[2] = GameCanvas.menu[1]
            return
        if GameCanvas.menu[1] > GameCanvas.menu[2] + 4:
            GameCanvas.menu[2] = GameCanvas.menu[1] - 4

    def draw_view_region(self, paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # ag.java:1212-1214
        GameCanvas.draw_region(paramInt1, paramInt2, paramInt3, paramInt4, paramImage, paramInt5, paramInt6)

    @staticmethod
    def split_field(paramString, paramInt):  # ag.java:1216-1240  (field #paramInt of "a|b|c")
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
    def draw_text(paramInt1, paramInt2, paramString):  # ag.java:1242-1244
        Gfx.draw_string(paramString, paramInt1, paramInt2, 0)

    @staticmethod
    def u16(paramByte1, paramByte2):  # ag.java:1275-1277
        return i16(paramByte1 & 0xFF | (paramByte2 & 0xFF) << 8)

    def draw_view_background(self):  # ag.java:1418-1431
        if GameCanvas.screen_fill == 0:
            self.fill_view(0, 0, 0)
            self.draw_view_region(GameCanvas.images[7], GameCanvas.view_x, GameCanvas.view_y, GameCanvas.view_size.x, GameCanvas.view_size.y, GameCanvas.view_offset.x, GameCanvas.view_offset.y)
            return
        if GameCanvas.screen_fill == 1:
            self.fill_view(0, 0, 0)
            return
        if GameCanvas.screen_fill == 2:
            self.fill_view(255, 255, 255)

    def fill_view(self, paramInt1, paramInt2, paramInt3):  # ag.java:1433-1435
        Gfx.fill_rect(GameCanvas.view_x, GameCanvas.view_y, GameCanvas.view_size.x, GameCanvas.view_size.y, GameCanvas.rgb(paramInt1, paramInt2, paramInt3))

    def paint_state(self):  # ag.java:1522-1610
        # DECOMP-FIX F8: the decompiled switch at ag.java:1526-1546 has no `break`s, so every case
        # would fall through into the next (bV==0 would also run bb.a(1), bc.b(1), ...).
        # The original had one branch per state.
        if GameCanvas.redraw == 1:
            GameCanvas.redraw = 0
            v = GameCanvas.state
            if v == 12:
                self.draw_outro()
            elif v == 0:
                GameCanvas.start_boot()
            elif v == 2:
                GameCanvas.menus.draw_menu(1)
            elif v == 3:
                GameCanvas.engine.draw_map(1)
            elif v == 4:
                GameCanvas.engine.scroll_room()
            elif v == 5:
                self.draw_view_background()
                for b in range(81):
                    GameCanvas.dirty[b // 9][b % 9] = 1
                GameCanvas.scene.draw_frame()
                GameCanvas.menus.draw_map_talk()
            elif v in (6, 8, 9):
                return
            elif v == 10:
                if (GameCanvas.story_ending == 0 and GameCanvas.story_page < GameCanvas.story_pages[1] - GameCanvas.story_pages[0]) or (GameCanvas.story_ending != 0 and GameCanvas.story_page >= GameCanvas.story_pages[1] - GameCanvas.story_pages[0]):
                    from pow.game.menus import Menus
                    GameCanvas.menus.draw_menu_frame()
                    Gfx.set_font(GameCanvas.font_white)
                    if GameCanvas.story_ending != 0:
                        self.draw_text_at("Prologue", 2 - GameCanvas.view_y, 9)
                    else:
                        self.draw_text_at("Epilogue", 2 - GameCanvas.view_y, 9)
                    GameCanvas.menus.draw_story_portraits(GameCanvas.story_picture)
                    if GameCanvas.speech_pos[0] > 0:
                        Menus.type_speech(0, 0, 1)
                    if GameCanvas.speech_pos[1] > 0:
                        Menus.type_speech(1, 0, 1)
                    self.draw_skip_key(1)
                else:
                    self.draw_story()
                if GameCanvas.popups.kind != 0:
                    GameCanvas.popups.draw_popup()
            return
        if GameCanvas.redraw == 2:
            if GameCanvas.state == 2:
                GameCanvas.menus.draw_menu(2)
                return
            return
        v = GameCanvas.state
        if v == 0:
            GameCanvas.start_boot()
            return
        if v == 2:
            GameCanvas.menus.draw_menu(0)
            return
        if v == 3:
            GameCanvas.engine.draw_map(0)
            return
        if v == 4:
            GameCanvas.engine.scroll_room()
            GameCanvas.engine.draw_hud()
            return
        if v == 5:
            GameCanvas.menus.tick_dialogue()
            return
        if v in (6, 8, 9):
            return
        if v == 10:
            if GameCanvas.popups.kind != 0:
                if GameCanvas.popups.popup_redraw != 0:
                    GameCanvas.popups.draw_popup()
                    return
            self.tick_story()

    def play_sound(self, paramInt):  # ag.java:1882-1885
        if GameCanvas.sound is not None:
            GameCanvas.sound.play_sound(paramInt)

    def tick_state(self):  # ag.java:1887-1933
        from pow.game.sound import Sound
        v = GameCanvas.state
        if v == 12:
            self.paint_state()
            if system.currentTimeMillis() - GameCanvas.key_time > 3000:
                GameCanvas.midlet.destroyApp(True)
                GameCanvas.midlet.notifyDestroyed()
            return
        if v == 0:
            self.paint_state()
        elif v == 2:
            if GameCanvas.sound is not None and GameCanvas.menu[0] < 29 and Sound.music != consts.A[GameCanvas.menu[0]] and GameCanvas.menu[0] != 20 and not GameCanvas.in_live:
                self.play_sound(consts.A[GameCanvas.menu[0]])
            if GameCanvas.popups.kind != 0:
                GameCanvas.popups.popup_keys()
            else:
                GameCanvas.menus.menu_keys()
            self.paint_state()
        elif v == 3:
            GameCanvas.engine.tick_map()
        elif v in (4, 5):
            self.paint_state()
            GameCanvas.engine.tick_mission_clock(0)
        elif v == 10:
            if GameCanvas.popups.kind != 0:
                GameCanvas.popups.popup_keys()
            self.paint_state()
        elif v == 11:
            if GameCanvas.live is not None:
                from pow.game.live import Live
                Live.draw_screen()
        if GameCanvas.live is not None:
            from pow.game.live import Live
            if Live.busy:
                GameCanvas.live.draw_connecting()
        GameCanvas.key_held = -999

    @staticmethod
    def start_boot():  # ag.java:1935-1939
        from pow.game.boot import Boot
        if GameCanvas.boot is None:
            GameCanvas.boot = Boot()
        GameCanvas.boot.draw_boot()

    def key_down(self, paramInt):  # ag.java:1941-1961
        if paramInt == -10:
            return
        if paramInt == -100:               # PORT-EXTRA: Tab / the AUTO corner (pow/game/autopilot.py)
            from pow.game.autopilot import Autopilot
            Autopilot.toggle()
            return
        if GameCanvas.paused:
            GameCanvas.key = paramInt
            return
        GameCanvas.key_pressed = paramInt
        if paramInt in (-4, -3, -2, -1, 50, 52, 54, 56):
            GameCanvas.key_held = paramInt

    def load_image(self, paramString):  # ag.java:1963-1975
        GameCanvas.gc()
        str_ = "/" + paramString + ".png"
        image = None
        try:
            image = Image.createImage(str_)
        except Exception:
            print("======== createMixImage failuer :" + paramString)
            return None
        GameCanvas.gc()
        return image

    @staticmethod
    def gc():  # ag.java:1977-1979  (System.gc)
        pass

    @staticmethod
    def fill_screen(paramInt):  # ag.java:1981-1983
        Gfx.fill_rect(0, 0, GameCanvas.screen_w, GameCanvas.screen_h, paramInt)

    def draw_title(self):  # ag.java:1985-1996  (title screen)
        if GameCanvas.images[30] is None:
            return
        GameCanvas.draw_region(0, 0, GameCanvas.canvas_size.x, GameCanvas.canvas_size.y, GameCanvas.images[30], 0, 0)
        if GameCanvas.title_press is None:
            GameCanvas.title_press = self.load_image(GameCanvas.scr_ui.get(36))
        GameCanvas.draw_region(GameCanvas.view_cx - 66 + GameCanvas.view_x, GameCanvas.canvas_size.y - 20, 132, 14, GameCanvas.title_press, 0, 0)
        if GameCanvas.title_logo is None:
            GameCanvas.title_logo = self.load_image(GameCanvas.scr_ui.get(42))
        if GameCanvas.frame % 6 < 3 and GameCanvas.state == 0:
            GameCanvas.draw_region(GameCanvas.view_cx - 55 + GameCanvas.view_x, GameCanvas.canvas_size.y - 60, 110, 14, GameCanvas.title_logo, 0, 0)

    def draw_image_file(self, paramString, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # ag.java:1998-2002
        image = self.load_image(paramString)
        if image is not None:
            GameCanvas.draw_region(paramInt1, paramInt2, paramInt3, paramInt4, image, paramInt5, paramInt6)

    def tick_title(self):  # ag.java:2004-2124  (title -> Main Menu)
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
        self.load_ui_images()
        GameCanvas.reset_globals()
        self.play_sound(-1)
        GameCanvas.save_flag = 0
        self.open_menu(0)
        GameCanvas.menu[0] = 5
        GameCanvas.menu_count = 10
        GameCanvas.popups.extra = 0
        self.load_game()
        GameCanvas.state = 2
        if not GameCanvas.has_save():
            GameCanvas.menu[1] = 1

    def load_game(self):  # ag.java:2126-2214  (load save "gamevil_pow_data")
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
        save_end = GameCanvas.save_pos
        if GameCanvas.save_pos != 0:
            cF = GameCanvas.save_buf
            arrayOfByte1 = [0] * 16
            b2 = 0
            while b2 < 8 and cF[2 + b2] != 32:
                b2 += 1
            arrayOfByte2 = bytearray(b2)
            for b1 in range(b2):
                arrayOfByte2[b1] = cF[2 + b1]
            cz.name = GameCanvas.read_utf(arrayOfByte2, 0, b2)
            GameCanvas.save_flag = i8(cF[18])
            GameCanvas.save_pos = 19
            GameCanvas.lord = GameCanvas.read_byte()
            GameCanvas.mission = GameCanvas.read_byte()
            GameCanvas.rooms_visited = GameCanvas.read_byte()
            GameCanvas.missions_done = GameCanvas.read_long()
            GameCanvas.lords_done = GameCanvas.read_long()
            for b1 in range(8):
                GameCanvas.stats[b1] = GameCanvas.read_int()
            GameCanvas.mission_exp = GameCanvas.read_int()
            GameCanvas.score = GameCanvas.read_int()
            for b1 in range(44):
                GameCanvas.generals[0][b1] = GameCanvas.read_byte()
                GameCanvas.generals[1][b1] = GameCanvas.read_byte()
            GameCanvas.general_count = GameCanvas.read_byte()
            for b1 in range(25):
                GameCanvas.shop[b1] = self.read_item()
            GameCanvas.chapter = GameCanvas.read_byte()
            cz.pos[0].x = GameCanvas.read_short()
            cz.pos[0].y = GameCanvas.read_short()
            # Java int division (values are positions >= 0, so // == /)
            cz.pos[0].x = i16((cz.pos[0].x // 27 // 7 * 7 + 4) * 27 + 8)
            cz.pos[0].y = i16((cz.pos[0].y // 27 // 7 * 7 + 4) * 27 + 8)
            for b1 in range(22):
                cz.mission_progress[b1] = GameCanvas.read_byte()
            cz.live_stat1 = GameCanvas.read_byte()
            cz.live_stat2 = GameCanvas.read_byte()
            cz.level = GameCanvas.read_byte()
            if config.ORIG_BUG["B2"]:
                # ORIG-BUG B2: the level is one byte in the save (G(cz.l), ag.java:2908) read back
                # signed, so Lv128+ loaded as -128..; the rest of the game keeps it as an int
                cz.level &= 0xFF
            cz.base_attack = GameCanvas.read_short()
            cz.base_defense = GameCanvas.read_short()
            cz.base_hp = GameCanvas.read_short()
            cz.hp = GameCanvas.read_short()
            cz.base_mp = GameCanvas.read_short()
            cz.mp = GameCanvas.read_short()
            cz.gold = GameCanvas.read_int()
            if GameCanvas.cheat:
                cz.gold = 555000
            if config.GOLD is not None:   # PORT-EXTRA config.GOLD (POW_GOLD=N)
                cz.gold = i32(config.GOLD)
            cz.fame = GameCanvas.read_int()
            cz.exp = GameCanvas.read_int()
            cz.kills = GameCanvas.read_short()
            cz.stat_points = GameCanvas.read_short()
            cz.live_registered = GameCanvas.read_byte()
            for b1 in range(5):
                cz.hotkeys[b1] = GameCanvas.read_byte()
            for b1 in range(19):
                cz.skill_levels[b1] = GameCanvas.read_byte()
            for b1 in range(9):
                cz.equipped[b1] = self.read_item()
            for b1 in range(25):
                cz.backpack[b1] = self.read_item()
            for b1 in range(5):
                cz.quick_slots[b1].item = GameCanvas.read_short()
                cz.quick_slots[b1].count = GameCanvas.read_byte()
            cz.quick_keys[0] = GameCanvas.read_byte()
            cz.quick_keys[1] = GameCanvas.read_byte()
            cz.head = GameCanvas.read_byte()
            GameCanvas.play_time = GameCanvas.read_int()
            GameCanvas.live_time = GameCanvas.read_int()
            GameCanvas.live_gifts = GameCanvas.read_byte()
            GameCanvas.live_saved = GameCanvas.read_byte()
            GameCanvas.talk_count = GameCanvas.read_byte()
            GameCanvas.difficulty = GameCanvas.read_byte()
            for b1 in range(16):
                arrayOfByte1[b1] = GameCanvas.read_byte()
            GameCanvas.talk_points = GameCanvas.read_int()
            for b1 in range(4):
                GameCanvas.read_int()
            self.read_backpack_extra(save_end)
        self.compact_backpack()

    # PORT-EXTRA config.BACKPACK_SIZE: the backpack cells past the original 25 follow the original
    # save as {u8 'B', u8 n, n items}. A save without the block (an old one, or the original game's)
    # loads with those cells empty; the header length (save_buf[0..1]) tells where the save ends.
    BACKPACK_EXTRA_MARK = 0x42

    def read_backpack_extra(self, save_end):
        cz = GameCanvas.hero
        for b in range(25, config.BACKPACK_SIZE):
            cz.backpack[b] = Item()
        cF = GameCanvas.save_buf
        if GameCanvas.save_pos + 2 > save_end or cF[GameCanvas.save_pos] & 0xFF != GameCanvas.BACKPACK_EXTRA_MARK:
            return
        n = cF[GameCanvas.save_pos + 1] & 0xFF
        GameCanvas.save_pos += 2
        for b in range(n):
            if GameCanvas.save_pos + 11 > save_end:
                break
            it = self.read_item()
            if 25 + b < config.BACKPACK_SIZE:
                cz.backpack[25 + b] = it
            else:
                # a save of a bigger backpack than this build has: keep the item in the first free cell
                free = next((s for s in range(config.BACKPACK_SIZE) if cz.backpack[s].id == 0), None)
                if free is not None and it.id != 0:
                    cz.backpack[free] = it

    def write_backpack_extra(self):
        cz = GameCanvas.hero
        n = config.BACKPACK_SIZE - 25
        if n <= 0:
            return
        GameCanvas.write_byte(GameCanvas.BACKPACK_EXTRA_MARK)
        GameCanvas.write_byte(n)
        for b in range(25, config.BACKPACK_SIZE):
            self.write_item(cz.backpack[b])

    @staticmethod
    def read_long():  # ag.java:2216-2230  (u64 LE; bytes 4..7 are sign-extended then masked)
        cF, cG = GameCanvas.save_buf, GameCanvas.save_pos
        l1 = 0
        for k_ in range(8):
            l1 |= (cF[cG + k_] & 0xFF) << (8 * k_)
        GameCanvas.save_pos += 8
        return l1 - (1 << 64) if l1 & (1 << 63) else l1

    @staticmethod
    def read_int():  # ag.java:2232-2237
        cF, cG = GameCanvas.save_buf, GameCanvas.save_pos
        j_ = cF[cG] & 0xFF | cF[cG + 1] << 8 & 0xFF00 | cF[cG + 2] << 16 & 0xFF0000 | cF[cG + 3] << 24 & 0xFF000000
        GameCanvas.save_pos += 4
        return i32(j_)

    @staticmethod
    def read_short():  # ag.java:2239-2244
        s = i16(GameCanvas.save_buf[GameCanvas.save_pos] & 0xFF | GameCanvas.save_buf[GameCanvas.save_pos + 1] << 8 & 0xFF00)
        GameCanvas.save_pos += 2
        return s

    @staticmethod
    def read_byte():  # ag.java:2246-2250
        b = i8(GameCanvas.save_buf[GameCanvas.save_pos] & 0xFF)
        GameCanvas.save_pos += 1
        return b

    def read_item(self):  # ag.java:2252-2261
        z1 = Item()
        z1.id = GameCanvas.read_short()
        z1.attack = GameCanvas.read_short()
        z1.defense = GameCanvas.read_short()
        z1.hp = GameCanvas.read_short()
        z1.mp = GameCanvas.read_short()
        z1.enchant = GameCanvas.read_byte()
        return z1

    def load_ui_images(self):  # ag.java:2263-2269
        GameCanvas.images[34] = self.load_image(GameCanvas.scr_ui.get(22))
        GameCanvas.images[19] = self.load_image(GameCanvas.scr_ui.get(24))
        GameCanvas.images[20] = self.load_image(GameCanvas.scr_ui.get(25))
        GameCanvas.images[0] = self.load_image(GameCanvas.scr_ui.get(48))
        GameCanvas.images[32] = self.load_image(GameCanvas.scr_ui.get(37))

    @staticmethod
    def load_data_file(paramInt):  # ag.java:2283-2285
        return ResReader.read("/" + GameCanvas.scr_data.get(paramInt))

    def open_menu(self, paramInt):  # ag.java:2287-2304
        self.free_hero_sprites()
        self.free_menu_images()
        if GameCanvas.images[7] is None:
            GameCanvas.images[7] = Image.createImage(GameCanvas.canvas_size.x, GameCanvas.canvas_size.y)
        GameCanvas.buffer_g = GameCanvas.images[7].getGraphics()
        GameCanvas.save_flag = 0
        GameCanvas.menu[2] = 0
        GameCanvas.menu[1] = 0
        GameCanvas.popups.kind = 0
        GameCanvas.gear_data = GameCanvas.load_data_file(47)
        GameCanvas.rare_data = GameCanvas.load_data_file(49)
        GameCanvas.treasure_data = GameCanvas.load_data_file(51)
        GameCanvas.load_menu_texts()
        GameCanvas.images[17] = self.load_image(GameCanvas.scr_ui.get(27))
        self.draw_menu_background(paramInt)
        self.compact_backpack()

    def load_menu_images(self):  # ag.java:2306-2311
        GameCanvas.images[1] = self.load_image(GameCanvas.scr_ui.get(21))
        GameCanvas.images[2] = self.load_image(GameCanvas.scr_ui.get(46))
        GameCanvas.images[3] = self.load_image(GameCanvas.scr_ui.get(43))
        GameCanvas.sparkle = self.load_image(GameCanvas.scr_ui.get(38))

    def free_menu_images(self):  # ag.java:2313-2319
        GameCanvas.images[1] = None
        GameCanvas.images[2] = None
        GameCanvas.images[3] = None
        GameCanvas.sparkle = None
        GameCanvas.gc()

    @staticmethod
    def load_menu_texts():  # ag.java:2321-2343  (menu captions from uimenu.scr = edat[69])
        al1 = ScrTable("/" + GameCanvas.scr_data.get(69))
        for b in range(30):
            GameCanvas.menu_titles[b] = al1.get(b)
            if b < 7:
                GameCanvas.skill_names[b] = al1.get(b + 48)
            if b < 6:
                GameCanvas.main_menu_items[b] = al1.get(b + 30)
            if b < 5:
                GameCanvas.speed_names[b] = al1.get(b + 55)
            if b < 4:
                GameCanvas.option_names[b] = al1.get(b + 42)
            if b < 2:
                GameCanvas.on_off[b] = al1.get(b + 46)
        GameCanvas.game_menu_items[0] = al1.get(36)
        GameCanvas.yes_no_items[0] = al1.get(37)
        GameCanvas.help_items[0] = al1.get(38)
        GameCanvas.ok_items[0] = al1.get(39)
        GameCanvas.continue_items[0] = al1.get(40)
        GameCanvas.pause_items[0] = al1.get(41)
        al1.free()

    def draw_menu_background(self, paramInt):  # ag.java:2345-2370  (menu background into ct[7])
        if paramInt == 1:
            return
        Gfx.set_graphics(GameCanvas.buffer_g)
        GameCanvas.images[11] = self.load_image(GameCanvas.scr_ui.get(60))
        GameCanvas.images[12] = self.load_image(GameCanvas.scr_ui.get(61))
        GameCanvas.images[16] = self.load_image(GameCanvas.scr_ui.get(63))
        GameCanvas.images[9] = self.load_image(GameCanvas.scr_ui.get(59))
        j_ = GameCanvas.images[9].getWidth()
        m = GameCanvas.images[9].getHeight()
        b = 0
        while b * m < GameCanvas.canvas_size.y + m:
            for b1 in range(4):
                GameCanvas.draw_region_at(GameCanvas.images[9], 0, 0, (b & 0x1) * -31 + b1 * j_, b * m, j_, m)
            b += 1
        # Java: (W - w) * b / 2 and H / 2 * b % 2 - all operands >= 0, so // matches Java /
        for b in range(4):
            GameCanvas.draw_region_at(GameCanvas.images[12], 0, 0, (GameCanvas.canvas_size.x - GameCanvas.images[12].getWidth()) * b // 2, GameCanvas.canvas_size.y // 2 * b % 2,
                         GameCanvas.images[12].getWidth(), GameCanvas.images[12].getHeight())
        for b in range(4):
            GameCanvas.draw_region_at(GameCanvas.images[11], 0, 0, GameCanvas.canvas_size.x // 2 * b % 2, (GameCanvas.canvas_size.y - GameCanvas.images[11].getHeight()) * b // 2,
                         GameCanvas.images[11].getWidth(), GameCanvas.images[11].getHeight())
        GameCanvas.draw_region_at(GameCanvas.images[16], 0, 0, (GameCanvas.canvas_size.x >> 1) - GameCanvas.images[16].getWidth() // 2, 0,
                     GameCanvas.images[16].getWidth(), GameCanvas.images[16].getHeight())
        GameCanvas.images[11] = None
        GameCanvas.images[12] = None
        GameCanvas.images[16] = None
        GameCanvas.images[9] = None
        Gfx.set_graphics(GameCanvas.screen_g)

    def compact_backpack(self):  # ag.java:2372-2382  (compact inventory cz.Y)
        for b in range(config.BACKPACK_SIZE - 1):
            if GameCanvas.hero.backpack[b].id == 0:
                for j_ in range(b + 1, config.BACKPACK_SIZE):
                    if GameCanvas.hero.backpack[j_].id != 0:
                        self.swap_items(GameCanvas.hero.backpack[b], GameCanvas.hero.backpack[j_])
                        break

    def swap_items(self, paramz1, paramz2):  # ag.java:2384-2389
        z1 = Item()
        GameCanvas.copy_item(z1, paramz1)
        GameCanvas.copy_item(paramz1, paramz2)
        GameCanvas.copy_item(paramz2, z1)

    @staticmethod
    def copy_item(paramz1, paramz2):  # ag.java:2391-2398
        paramz1.id = paramz2.id
        paramz1.attack = paramz2.attack
        paramz1.defense = paramz2.defense
        paramz1.hp = paramz2.hp
        paramz1.mp = paramz2.mp
        paramz1.enchant = paramz2.enchant

    def free_hero_sprites(self):  # ag.java:2400-2436
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
    def draw_region(paramInt1, paramInt2, paramInt3, paramInt4, paramImage, paramInt5, paramInt6):  # ag.java:2438-2440
        Gfx.draw_image_part(paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6)

    def draw_map_region(self, paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # ag.java:2442-2457
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
            GameCanvas.draw_region(paramInt1 + GameCanvas.view_x - j_, paramInt2 - i1 + GameCanvas.view_y, paramInt3 + j_ + m, paramInt4 + i1 + i2,
                         paramImage, paramInt5 - j_, paramInt6 - i1)

    @staticmethod
    def draw_region_at(paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # ag.java:2459-2461
        Gfx.draw_image_part(paramImage, paramInt3, paramInt4, paramInt5, paramInt6, paramInt1, paramInt2)

    @staticmethod
    def stop_sound():  # ag.java:2463-2465
        from pow.game.sound import Sound
        Sound.stop_all()

    @staticmethod
    def free_hero_images():  # ag.java:2467-2472
        GameCanvas.hero.head_frames = None
        GameCanvas.hero.body_frames = None
        GameCanvas.hero.head_image = None
        GameCanvas.hero.body_image = None

    @staticmethod
    def set_menu_items():  # ag.java:2522-2546
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
    def restore_menu_cursor():  # ag.java:2728-2733
        GameCanvas.menu_count = consts.v[GameCanvas.menu[0]]
        GameCanvas.menu[1] = GameCanvas.menu_cursors[GameCanvas.menu[0]]
        GameCanvas.menu[2] = GameCanvas.menu_tops[GameCanvas.menu[0]]
        GameCanvas.redraw = 1

    @staticmethod
    def draw_text_centred_at(paramString, paramInt1, paramInt2):  # ag.java:2743-2746  (centred text)
        paramInt1 += 2
        Gfx.draw_string(paramString, GameCanvas.view_cx + GameCanvas.view_x + paramInt2, paramInt1 + GameCanvas.view_y, 1)

    def draw_text_at(self, paramString, paramInt1, paramInt2):  # ag.java:2748-2750
        GameCanvas.draw_text_centred_at(paramString, paramInt1, 0)

    @staticmethod
    def draw_view_text_centred(paramString, paramInt1, paramInt2):  # ag.java:2752-2754
        Gfx.draw_string(paramString, paramInt1 + GameCanvas.view_x, paramInt2 + GameCanvas.view_y, 1)

    @staticmethod
    def draw_view_text(paramString, paramInt1, paramInt2):  # ag.java:2756-2758
        Gfx.draw_string(paramString, paramInt1 + GameCanvas.view_x, paramInt2 + GameCanvas.view_y, 0)

    def draw_box(self, paramInt1, paramInt2, paramInt3, paramInt4, paramBoolean):  # ag.java:2760-2762
        GameCanvas.draw_frame_box(paramInt1, paramInt2, paramInt3, paramInt4, 0, 5263440, 16777215, paramBoolean)

    @staticmethod
    def draw_frame_box(paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7, paramBoolean):  # ag.java:2764-2791
        ac1 = Rect(0, 0, 0, 0)
        if paramBoolean:
            ac1.x = paramInt1 - 2
            ac1.w = paramInt3 + 4
            ac1.y = paramInt2 - 1
            ac1.h = paramInt4 + 2
            Gfx.draw_rect(ac1.x, ac1.y, ac1.w, ac1.h, paramInt7)
            ac1.x += 1
            ac1.w -= 2
            ac1.y -= 1
            ac1.h += 2
            Gfx.draw_rect(ac1.x, ac1.y, ac1.w, ac1.h, paramInt7)
        ac1.x = paramInt1 - 1
        ac1.w = paramInt3 + 2
        ac1.y = paramInt2
        ac1.h = paramInt4
        Gfx.draw_rect(ac1.x, ac1.y, ac1.w, ac1.h, paramInt6)
        ac1.x += 1
        ac1.w -= 2
        ac1.y -= 1
        ac1.h += 2
        Gfx.draw_rect(ac1.x, ac1.y, ac1.w, ac1.h, paramInt6)
        ac1.y += 1
        ac1.h -= 2
        Gfx.fill_rect(ac1.x, ac1.y, ac1.w, ac1.h, paramInt5)

    @staticmethod
    def rgb(paramInt1, paramInt2, paramInt3):  # ag.java:2857-2860
        return (paramInt1 & 0xFF) << 16 | (paramInt2 & 0xFF) << 8 | paramInt3 & 0xFF

    @staticmethod
    def has_save():  # ag.java:2862-2869  (is there a saved game?)
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_data", True)
            return not (recordStore.getNumRecords() == 0)
        except Exception:
            return False

    def start_exit(self):  # ag.java:3003-3009  (exit: show outro, quit after 3 s)
        GameCanvas.state = 12
        GameCanvas.redraw = 1
        GameCanvas.lord_count = 0
        GameCanvas.stop_sound()
        GameCanvas.key_time = system.currentTimeMillis()

    def draw_outro(self):  # ag.java:3011-3019  (outro picture)
        if GameCanvas.frame == 2 or GameCanvas.frame == 5:
            GameCanvas.stop_sound()
        GameCanvas.fill_screen(0)
        image = self.load_image(GameCanvas.scr_ui.get(0))
        j_ = image.getWidth()
        GameCanvas.draw_region(GameCanvas.screen_cx - j_ // 2, GameCanvas.screen_cy - 10, j_, 20, image, 0, 0)
        GameCanvas.draw_region(GameCanvas.screen_cx - j_ // 2, GameCanvas.screen_h - 24, j_, 22, image, 0, 20)

    @staticmethod
    def read_utf(paramArrayOfbyte, paramInt1, paramInt2):  # ag.java:3026-3043  (readUTF of bytes[from:to])
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
    def draw_auto_badge():
        """PORT-EXTRA (pow/game/autopilot.py): the AUTO button in the bottom-left corner of the map
        (the corner is empty on the map; a click on it, Tab or F toggles): white while the
        auto-hunt is on, grey while it is off (config.AUTO_BUTTON: only while it is on)."""
        from pow.game.autopilot import Autopilot
        if GameCanvas.state != 3 or GameCanvas.popups.kind != 0:
            return
        if not (Autopilot.on or config.AUTO_BUTTON):
            return
        Gfx.fill_rect(0, GameCanvas.screen_h - 17, 48, 17, 0)
        Gfx.set_font(GameCanvas.font_white if Autopilot.on else GameCanvas.font_gray)
        Gfx.draw_string("AUTO", 24, GameCanvas.screen_h - 17, 1)

    @staticmethod
    def draw_softkeys(paramInt1, paramInt2):  # ag.java:3045-3079  (soft-key captions)
        if GameCanvas.popups.kind != 0:
            return
        j_ = GameCanvas.softkey_bg.getWidth()
        m = GameCanvas.softkey_bg.getHeight()
        str_ = ""
        if paramInt1 != -1:
            Gfx.set_font(GameCanvas.font_white)
            Gfx.draw_image(GameCanvas.softkey_bg, 0, GameCanvas.screen_h - m)
            i1 = len(str_ + consts.t[paramInt1]) * 10
            i2 = i1 + 4 - GameCanvas.softkey_bg.getWidth()
            if i2 > 0:
                Gfx.fill_rect(j_ - 8, GameCanvas.screen_h - m + 2, 8, 13, 0)
                Gfx.draw_image(GameCanvas.softkey_bg, i2, GameCanvas.screen_h - m)
                Gfx.fill_rect(i2, GameCanvas.screen_h - m + 2, 8, 13, 0)
                Gfx.draw_string(str_ + consts.t[paramInt1], (j_ + i2) // 2, GameCanvas.screen_h - m, 1)
            else:
                Gfx.draw_string(str_ + consts.t[paramInt1], j_ // 2, GameCanvas.screen_h - m, 1)
        if paramInt2 != -1:
            Gfx.set_font(GameCanvas.font_white)
            Gfx.draw_image(GameCanvas.softkey_bg, GameCanvas.screen_w - j_ - 0, GameCanvas.screen_h - m)
            i1 = len(str_ + consts.t[paramInt2]) * 10
            i2 = i1 + 15 - GameCanvas.softkey_bg.getWidth()
            if i2 > 0:
                Gfx.fill_rect(GameCanvas.screen_w - j_ - 0, GameCanvas.screen_h - m + 2, 8, 13, 0)
                Gfx.draw_image(GameCanvas.softkey_bg, GameCanvas.screen_w - j_ - i2 - 0, GameCanvas.screen_h - m)
                Gfx.fill_rect(GameCanvas.screen_w - i2 - 0 - 8, GameCanvas.screen_h - m + 2, 8, 13, 0)
                Gfx.draw_string(str_ + consts.t[paramInt2], GameCanvas.screen_w - (j_ + i2) // 2 - 0, GameCanvas.screen_h - m, 1)
                return
            Gfx.draw_string(str_ + consts.t[paramInt2], GameCanvas.screen_w - j_ // 2 - 0, GameCanvas.screen_h - m, 1)

    def set_color(self, paramInt1, paramInt2, paramInt3):  # ag.java:3201-3203
        GameCanvas.fill_color = GameCanvas.rgb(paramInt1, paramInt2, paramInt3)

    @staticmethod
    def draw_line(paramInt1, paramInt2, paramInt3, paramInt4):  # ag.java:3205-3207
        Gfx.draw_line(paramInt1, paramInt2, paramInt3, paramInt4, GameCanvas.fill_color)

    def load_hero_images(self):  # ag.java:3459-3465
        GameCanvas.free_hero_images()
        GameCanvas.hero.head_image = self.load_image(GameCanvas.scr_char.get(46 + GameCanvas.hero.head))
        GameCanvas.hero.head_frames = self.load_frames(47 + GameCanvas.hero.head)
        GameCanvas.hero.body_image = self.load_image(GameCanvas.scr_char.get(44))
        GameCanvas.hero.body_frames = self.load_frames(45)

    def load_frames(self, paramInt):  # ag.java:3467-3482  (frame table from mdat_QVGA)
        b1 = 1
        arrayOfByte = ResReader.read("/" + GameCanvas.scr_maps.get(paramInt))
        n = arrayOfByte[0] & 0xFF
        arrayOfY = [None] * n
        for b2 in range(n):
            arrayOfY[b2] = SpriteFrame()
            arrayOfY[b2].src_x = GameCanvas.u16(arrayOfByte[b1], arrayOfByte[b1 + 1])
            arrayOfY[b2].src_y = GameCanvas.u16(arrayOfByte[b1 + 2], arrayOfByte[b1 + 3])
            arrayOfY[b2].w = GameCanvas.u16(arrayOfByte[b1 + 4], arrayOfByte[b1 + 5])
            arrayOfY[b2].h = GameCanvas.u16(arrayOfByte[b1 + 6], arrayOfByte[b1 + 7])
            arrayOfY[b2].ox = GameCanvas.u16(arrayOfByte[b1 + 8], arrayOfByte[b1 + 9])
            arrayOfY[b2].oy = GameCanvas.u16(arrayOfByte[b1 + 10], arrayOfByte[b1 + 11])
            b1 += 12
        return arrayOfY

    @staticmethod
    def gamestr(paramInt):  # ag.java:3538-3540
        return GameCanvas.scr_gamestr.get(paramInt)

    @staticmethod
    def key_digit(paramInt):  # ag.java:3549-3574  (key code '0'..'9' -> digit, else -1)
        if 48 <= paramInt <= 57:
            return paramInt - 48
        return -1

    @staticmethod
    def add_exp(paramInt):  # ag.java:3081-3098  (add exp; returns the levels gained)
        arrayOfInt = [0] * 10
        b = 0
        paramInt += GameCanvas.hero.exp
        while True:
            j = b % 10
            if j == 0:
                arrayOfInt = GameCanvas.menus.load_exp_table()
            j = arrayOfInt[j]
            if paramInt < j:
                GameCanvas.hero.exp = paramInt
                return b
            paramInt -= j
            GameCanvas.hero.level += 1
            GameCanvas.hero.stat_points += 3
            b += 1

    @staticmethod
    def trim_right(paramString):  # ag.java:3148-3153  (trim trailing spaces; sic: one char left -> "")
        m = len(paramString) - 1
        while m >= 0 and paramString[m] == ' ':
            m -= 1
        return "" if m == 0 else paramString[:m + 1]

    @staticmethod
    def cut_at_control(paramString):  # ag.java:3155-3160  (up to the first control character)
        b = 0
        while b < len(paramString) and paramString[b] >= ' ':
            b += 1
        return "" if b == 0 else paramString[:b]

    @staticmethod
    def cut_at_space(paramString):  # ag.java:3162-3167  (up to the first space)
        b = 0
        while b < len(paramString) and paramString[b] != ' ':
            b += 1
        return "" if b == 0 else paramString[:b]

    # ---- New Game: hero creation (screens 29 / 6 / 7 / 8) and the save writer ------------

    @staticmethod
    def now():  # ag.java:1039-1041
        return system.currentTimeMillis()

    @staticmethod
    def update_hero_stats():  # ag.java:1759-1773  (equipment bonuses -> derived stats)
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
    def move_letter_cursor(paramInt):  # ag.java:1775-1792  (name entry: move the cursor over the 2x14 letter grid)
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
    def draw_letter_grid(paramInt1, paramInt2):  # ag.java:1794-1819  (letter grid A..Z + OK)
        j_ = GameCanvas.screen_cx - 71
        arrayOfString = GameCanvas._F_LETTERS
        Gfx.fill_rect(j_, paramInt2, 142, 34, 0)
        Gfx.fill_rect(j_ + 123, paramInt2 + 18, 19, 15, 255)
        if GameCanvas.frame % 4 < 2:
            if paramInt1 == 26:
                Gfx.fill_rect(j_ + 123, paramInt2 + 18, 19, 15, 16711680)
            elif F10:
                # DECOMP-FIX F10: `10 * p % 14`, `17 * p / 14` -> `10 * (p % 14)`, `17 * (p / 14)`
                Gfx.fill_rect(j_ + 2 + 10 * (paramInt1 % 14), paramInt2 + 1 + 17 * (paramInt1 // 14), 10, 15, 16711680)
            else:
                Gfx.fill_rect(j_ + 2 + 10 * paramInt1 % 14, paramInt2 + 1 + 17 * paramInt1 // 14, 10, 15, 16711680)
        Gfx.set_font(GameCanvas.font_white)
        for b in range(len(arrayOfString)):
            if b == 8:
                b1 = 1
            elif b == 26:
                b1 = 1
            else:
                b1 = 0
            row = 17 * (b // 14) if F10 else 17 * b // 14   # DECOMP-FIX F10
            Gfx.draw_string(arrayOfString[b], j_ + 3 + b % 14 * 10 + b1, paramInt2 + row, 0)

    def draw_arrow(self, paramInt1, paramInt2, paramInt3):  # ag.java:1847-1880  (arrow from ct[17])
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
        GameCanvas.draw_region(paramInt2 + GameCanvas.view_x, paramInt3 + GameCanvas.view_y, b1, b2, GameCanvas.images[17], b3, b4)

    @staticmethod
    def rand_range(paramInt1, paramInt2):  # ag.java:2735-2737
        paramInt2 -= 1
        return paramInt1 + abs(imod(GameCanvas.rng.nextInt(), abs(paramInt2 - paramInt1) + 1))

    def rand(self, paramInt):  # ag.java:2739-2741
        return GameCanvas.rand_range(0, paramInt)

    def draw_big_number(self, paramInt1, paramInt2, paramInt3, paramInt4):  # ag.java:2810-2834  (number from ct[19])
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
                self.draw_map_region(GameCanvas.images[19], paramInt2, paramInt3, 5, 14, 100, 0)
            paramInt2 -= 9
            self.draw_map_region(GameCanvas.images[19], paramInt2, paramInt3, 10, 14, imod(paramInt1, 10) * 10, 0)
            b += 1
            paramInt1 = idiv(paramInt1, 10)
            if paramInt1 <= 0:
                return j_

    def save_game(self):  # ag.java:2871-2961  (write the save "gamevil_pow_data")
        cz = GameCanvas.hero
        arrayOfChar = [0] * 16
        arrayOfByte = cz.name.encode("latin-1")
        if len(GameCanvas.save_buf) < 2000:
            # PORT-EXTRA: a loaded save can be shorter than ag.cF (965 bytes, e.g. tools/shot.py's);
            # the backpack block written after it needs the room of the 2000-byte buffer
            GameCanvas.save_buf = bytearray(GameCanvas.save_buf) + bytearray(2000 - len(GameCanvas.save_buf))
        cF = GameCanvas.save_buf
        for b in range(8):
            if b < len(arrayOfByte):
                cF[2 + b] = arrayOfByte[b]
            else:
                cF[2 + b] = 32
        cF[18] = GameCanvas.save_flag & 0xFF
        GameCanvas.save_pos = 19
        GameCanvas.write_byte(GameCanvas.lord)
        GameCanvas.write_byte(GameCanvas.mission)
        GameCanvas.write_byte(GameCanvas.rooms_visited)
        GameCanvas.write_long(GameCanvas.missions_done)
        GameCanvas.write_long(GameCanvas.lords_done)
        for b in range(8):
            GameCanvas.write_int(i32(GameCanvas.stats[b]))
        GameCanvas.write_int(GameCanvas.mission_exp)
        GameCanvas.write_int(GameCanvas.score)
        for b in range(44):
            GameCanvas.write_byte(GameCanvas.generals[0][b])
            GameCanvas.write_byte(GameCanvas.generals[1][b])
        GameCanvas.write_byte(GameCanvas.general_count)
        for b in range(25):
            self.write_item(GameCanvas.shop[b])
        GameCanvas.write_byte(GameCanvas.chapter)
        GameCanvas.write_short((idiv(GameCanvas.view_tx + 2, 7) * 7 + 4) * 27)
        GameCanvas.write_short((idiv(GameCanvas.view_ty + 2, 7) * 7 + 4) * 27)
        for b in range(22):
            GameCanvas.write_byte(cz.mission_progress[b])
        GameCanvas.write_byte(cz.live_stat1)
        GameCanvas.write_byte(cz.live_stat2)
        GameCanvas.write_byte(cz.level)
        GameCanvas.write_short(cz.base_attack)
        GameCanvas.write_short(cz.base_defense)
        GameCanvas.write_short(cz.base_hp)
        GameCanvas.write_short(cz.hp)
        GameCanvas.write_short(cz.base_mp)
        GameCanvas.write_short(cz.mp)
        GameCanvas.write_int(cz.gold)
        GameCanvas.write_int(cz.fame)
        GameCanvas.write_int(cz.exp)
        GameCanvas.write_short(cz.kills)
        GameCanvas.write_short(cz.stat_points)
        GameCanvas.write_byte(cz.live_registered)
        for b in range(5):
            GameCanvas.write_byte(cz.hotkeys[b])
        for b in range(19):
            GameCanvas.write_byte(cz.skill_levels[b])
        for b in range(9):
            self.write_item(cz.equipped[b])
        for b in range(25):
            self.write_item(cz.backpack[b])
        for b in range(5):
            GameCanvas.write_short(cz.quick_slots[b].item)
            GameCanvas.write_byte(cz.quick_slots[b].count)
        GameCanvas.write_byte(cz.quick_keys[0])
        GameCanvas.write_byte(cz.quick_keys[1])
        GameCanvas.write_byte(cz.head)
        GameCanvas.write_int(i32(GameCanvas.clock[0] - GameCanvas.play_time))
        GameCanvas.write_int(i32(GameCanvas.live_time))
        GameCanvas.write_byte(GameCanvas.live_gifts)
        GameCanvas.write_byte(GameCanvas.live_saved)
        GameCanvas.write_byte(GameCanvas.talk_count)
        GameCanvas.write_byte(GameCanvas.difficulty)
        for b in range(16):
            GameCanvas.write_byte(arrayOfChar[b])
        GameCanvas.write_int(GameCanvas.talk_points)
        for b in range(4):
            GameCanvas.write_int(0)
        self.write_backpack_extra()
        cF[0] = GameCanvas.save_pos & 0xFF
        cF[1] = GameCanvas.save_pos >> 8 & 0xFF
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_data", True)
            if recordStore.getNumRecords() == 0:
                recordStore.addRecord(cF, 0, len(cF))
            recordStore.setRecord(1, cF, 0, len(cF))
        except Exception:
            pass
        return bool(GameCanvas.has_save())

    # cF holds Java bytes; the port stores them masked to 0..255 (RecordStore takes bytearray)
    @staticmethod
    def write_long(paramLong):  # ag.java:2963-2973
        for k_ in range(8):
            GameCanvas.save_buf[GameCanvas.save_pos + k_] = paramLong >> (8 * k_) & 0xFF
        GameCanvas.save_pos += 8

    @staticmethod
    def write_int(paramInt):  # ag.java:2975-2981
        GameCanvas.save_buf[GameCanvas.save_pos] = paramInt & 0xFF
        GameCanvas.save_buf[GameCanvas.save_pos + 1] = paramInt >> 8 & 0xFF
        GameCanvas.save_buf[GameCanvas.save_pos + 2] = paramInt >> 16 & 0xFF
        GameCanvas.save_buf[GameCanvas.save_pos + 3] = paramInt >> 24 & 0xFF
        GameCanvas.save_pos += 4

    @staticmethod
    def write_short(paramInt):  # ag.java:2983-2987
        GameCanvas.save_buf[GameCanvas.save_pos] = paramInt & 0xFF
        GameCanvas.save_buf[GameCanvas.save_pos + 1] = paramInt >> 8 & 0xFF
        GameCanvas.save_pos += 2

    @staticmethod
    def write_byte(paramInt):  # ag.java:2989-2992
        GameCanvas.save_buf[GameCanvas.save_pos] = paramInt & 0xFF
        GameCanvas.save_pos += 1

    def write_item(self, paramz):  # ag.java:2994-3001
        GameCanvas.write_short(paramz.id)
        GameCanvas.write_short(paramz.attack)
        GameCanvas.write_short(paramz.defense)
        GameCanvas.write_short(paramz.hp)
        GameCanvas.write_short(paramz.mp)
        GameCanvas.write_byte(paramz.enchant)

    def draw_rect_outline(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7):  # ag.java:3140-3146  (rectangle outline)
        self.set_color(paramInt5, paramInt6, paramInt7)
        GameCanvas.draw_line(paramInt1, paramInt2, paramInt1 + paramInt3 - 1, paramInt2)
        GameCanvas.draw_line(paramInt1, paramInt2 + 1, paramInt1, paramInt2 + paramInt4 - 1)
        GameCanvas.draw_line(paramInt1 + paramInt3 - 1, paramInt2, paramInt1 + paramInt3 - 1, paramInt2 + paramInt4 - 1)
        GameCanvas.draw_line(paramInt1 + 1, paramInt2 + paramInt4 - 1, paramInt1 + paramInt3 - 2, paramInt2 + paramInt4 - 1)

    def draw_round_outline(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7):  # ag.java:3181-3187  (outline, round corners)
        self.set_color(paramInt5, paramInt6, paramInt7)
        GameCanvas.draw_line(paramInt1 + 1, paramInt2, paramInt1 + paramInt3 - 2, paramInt2)
        GameCanvas.draw_line(paramInt1, paramInt2 + 1, paramInt1, paramInt2 + paramInt4 - 2)
        GameCanvas.draw_line(paramInt1 + paramInt3 - 1, paramInt2 + 1, paramInt1 + paramInt3 - 1, paramInt2 + paramInt4 - 2)
        GameCanvas.draw_line(paramInt1 + 1, paramInt2 + paramInt4 - 1, paramInt1 + paramInt3 - 2, paramInt2 + paramInt4 - 1)

    def draw_selection(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7):  # ag.java:3189-3199  (selection frame)
        self.draw_round_outline(paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7)
        self.draw_dot(paramInt1 + 1, paramInt2 + 1)
        self.draw_dot(paramInt1 + paramInt3 - 2, paramInt2 + 1)
        self.draw_dot(paramInt1 + 1, paramInt2 + paramInt4 - 2)
        self.draw_dot(paramInt1 + paramInt3 - 2, paramInt2 + paramInt4 - 2)

    def draw_dot(self, paramInt1, paramInt2):  # ag.java:3209-3211
        GameCanvas.draw_line(paramInt1, paramInt2, paramInt1 + 1, paramInt2 + 1)

    def start_new_game(self):  # ag.java:3213-3220  (New Game -> difficulty screen 29)
        GameCanvas.menus.enter_submenu()
        GameCanvas.menu[0] = 29
        GameCanvas.menu_count = consts.v[GameCanvas.menu[0]]
        GameCanvas.menu[1] = 1
        GameCanvas.hero.head = 0
        self.new_hero()

    def new_hero(self):  # ag.java:3222-3273  (fresh hero)
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
        GameCanvas.reset_base_stats()
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
            Item.clear(cz.equipped[b])
        for b in range(config.BACKPACK_SIZE):
            Item.clear(cz.backpack[b])
        self.give_item(116, 0)
        self.swap_items(cz.equipped[0], cz.backpack[0])
        cz.quick_keys[0] = 0
        cz.quick_keys[1] = 1

    @staticmethod
    def reset_base_stats():  # ag.java:3275-3284  (base stats, 5 free points)
        from pow.game import hero_classes
        cz = GameCanvas.hero
        # PORT-EXTRA: the stats of the chosen head (pow/game/hero_classes.py); the original
        # gave every head ATK 5 / DEF 4 / HP 30 / MP 10, which is still head 0
        hero_classes.set_base_stats(cz)
        cz.stat_points = 5
        GameCanvas.redraw = 1

    def give_item(self, paramInt1, paramInt2):  # ag.java:3286-3360  (give an item / potion / gold)
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
            while b < config.BACKPACK_SIZE and 0 != cz.backpack[b].id:
                b += 1
            if b > config.BACKPACK_SIZE - 1:
                return 0
            cz.backpack[b].id = i16(paramInt1)
            cz.backpack[b].attack = 0
            cz.backpack[b].defense = 0
            cz.backpack[b].hp = 0
            cz.backpack[b].mp = 0
            cz.backpack[b].enchant = 0
        if paramInt1 < 10000:
            GameCanvas.menus.load_item_def(paramInt1)
        if paramInt1 < 100:
            cz.quick_slots[b].item = i16(paramInt1)
            cz.quick_slots[b].count = i16(cz.quick_slots[b].count + 1)
        elif paramInt1 < 300:
            if paramInt2 != 0:
                s = i16(GameCanvas.gear_def.bonus + self.rand(GameCanvas.gear_def.bonus_range + 1))
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
    def reset_quick_items():  # ag.java:3362-3375  (starting quick items)
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

    def fill_shop(self):  # ag.java:3377-3398  (17 random shop items, sorted)
        arrayOfInt = [0] * 17
        GameCanvas.load_item_tables()
        for b in range(17):
            arrayOfInt[b] = 101 + 5 * GameCanvas.rand_range(0, 20) + GameCanvas.item_tier(GameCanvas.rand_range(0, 100))
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
            GameCanvas.shop[8 + b] = self.make_item(arrayOfInt[b])

    @staticmethod
    def load_item_tables():  # ag.java:3400-3412
        arrayOfInt = [47, 51, 49]
        if not GameCanvas.tables_loaded[1]:
            for b in range(3):
                if GameCanvas.item_tables[b] is None:
                    GameCanvas.item_tables[b] = ArrTable("/" + GameCanvas.scr_data.get(arrayOfInt[b]))
                if GameCanvas.item_tables[b] is None:
                    return False
            GameCanvas.tables_loaded[1] = True
        return True

    @staticmethod
    def item_tier(paramInt):  # ag.java:3414-3422  (item tier by hero level)
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

    def make_item(self, paramInt):  # ag.java:3424-3457  (make item paramInt with random bonus)
        z1 = Item()
        arrayOfInt = [0] * 5
        z1.id = i16(paramInt)
        z1.enchant = 0
        if paramInt < 300:
            for b in range(3):
                arrayOfInt[b] = GameCanvas.item_tables[0].get_int(paramInt - 101, 2 + b)
            if arrayOfInt[0] == 0:
                z1.attack = i16(arrayOfInt[1] + self.rand(arrayOfInt[2]))
            elif arrayOfInt[0] == 1:
                z1.defense = i16(arrayOfInt[1] + self.rand(arrayOfInt[2]))
            elif arrayOfInt[0] == 2:
                z1.hp = i16(arrayOfInt[1] + self.rand(arrayOfInt[2]))
            elif arrayOfInt[0] == 3:
                z1.mp = i16(arrayOfInt[1] + self.rand(arrayOfInt[2]))
        else:
            tbl = GameCanvas.item_tables[1] if paramInt < 500 else GameCanvas.item_tables[2]
            # ORIG-BUG B1: the original reads both tables at id - 301, so a Rare item (shinki.arr,
            # ids 501-518) gets row 200+ -> all 0; its own row is id - 501
            first = 501 if paramInt >= 500 and config.ORIG_BUG["B1"] else 301
            for b in range(4):
                arrayOfInt[b] = tbl.get_int(paramInt - first, 2 + b)
            z1.attack = i16(arrayOfInt[0])
            z1.defense = i16(arrayOfInt[1])
            z1.hp = i16(arrayOfInt[2])
            z1.mp = i16(arrayOfInt[3])
        return z1

    def start_story(self, paramInt1, paramInt2):  # ag.java:3488-3528  (start the story player, bV = 10)
        GameCanvas.story_id = i16(paramInt1)
        if paramInt1 < 100:
            GameCanvas.story_ending = 0
            b = 64 + paramInt1 // 6
            for b1 in range(3):
                GameCanvas.story_pages[b1] = consts.aV[(paramInt1 << 1) + b1] - consts.aV[paramInt1 // 6 * 12]
            if paramInt1 == 3 and paramInt2 != 0 and 0 == GameCanvas.backpack_slot_of(502):
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
            GameCanvas.scr_story = ScrTable("/" + GameCanvas.scr_data.get(b))
        GameCanvas.talk_lines[1] = ""
        GameCanvas.talk_lines[0] = ""
        GameCanvas.speech_pos[1] = 0
        GameCanvas.speech_pos[0] = 0
        GameCanvas.story_page = 0
        GameCanvas.wait_ticks = 0
        GameCanvas.speech_line = 0
        GameCanvas.scene.load_story_page(GameCanvas.story_page)
        if 0 == GameCanvas.story_ending:
            self.draw_menu_background(1)
        GameCanvas.state = 10
        self.play_sound(2)
        GameCanvas.redraw = 1

    @staticmethod
    def backpack_slot_of(paramInt):  # ag.java:3530-3536  (inventory slot of item, 1-based; 0 = none)
        for b in range(config.BACKPACK_SIZE):
            if GameCanvas.hero.backpack[b].id == paramInt:
                return b + 1
        return 0

    # ---- story player (bV == 10): prologue / epilogue -------------------------------------

    def tick_story(self):  # ag.java:1612-1692  (one tick of the story player)
        if GameCanvas.wait_ticks > 0:
            GameCanvas.wait_ticks = i16(GameCanvas.wait_ticks - 1)
            if GameCanvas.key != -999 and GameCanvas.wait_ticks > 3:
                GameCanvas.wait_ticks = 3
            if 0 == GameCanvas.wait_ticks:
                GameCanvas.story_page += 1
                if GameCanvas.story_page < GameCanvas.story_pages[2] - GameCanvas.story_pages[0]:
                    GameCanvas.scene.load_story_page(GameCanvas.story_page)
                elif 0 == GameCanvas.story_ending and GameCanvas.menu_return == 0 and GameCanvas.story_page == GameCanvas.story_pages[2] - GameCanvas.story_pages[0]:
                    if GameCanvas.reward_item != 0 or GameCanvas.reward_skill != 0:
                        GameCanvas.popups.setup_popup(27)
                    GameCanvas.scene.load_story_page(GameCanvas.story_page)
                else:
                    GameCanvas.scr_story.free()
                    GameCanvas.scr_story = None
                    GameCanvas.talk_lines[1] = ""
                    GameCanvas.talk_lines[0] = ""
                    self.load_menu_frames()
                    GameCanvas.menu[0] = GameCanvas.menu_return
                    GameCanvas.images[35] = None
                    GameCanvas.images[35] = None
                    GameCanvas.restore_menu_cursor()
                    if GameCanvas.menu[0] == 0:
                        GameCanvas.menu[1] = 0
                    GameCanvas.state = 2
                    GameCanvas.menu_scroll = 0
                    GameCanvas.menu_anim = 0
                GameCanvas.redraw = 1
        elif (0 == GameCanvas.story_ending and GameCanvas.story_page < GameCanvas.story_pages[1] - GameCanvas.story_pages[0]) or (GameCanvas.story_ending != 0 and GameCanvas.story_page >= GameCanvas.story_pages[1] - GameCanvas.story_pages[0]):
            from pow.game.menus import Menus
            Menus.type_speech(GameCanvas.speech_line, GameCanvas.speech_pos[GameCanvas.speech_line], 0)
            if len(GameCanvas.speech[GameCanvas.speech_line]) <= GameCanvas.speech_pos[GameCanvas.speech_line]:
                if GameCanvas.key != -999:
                    GameCanvas.wait_ticks = 0
                else:
                    GameCanvas.wait_ticks = 15
        else:
            self.draw_story()
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

    def fill_screen_rgb(self, paramInt1, paramInt2, paramInt3):  # ag.java:1694-1696  (fill the screen)
        Gfx.fill_rect(0, 0, GameCanvas.canvas_size.x, GameCanvas.canvas_size.y, GameCanvas.rgb(paramInt1, paramInt2, paramInt3))

    def draw_story(self):  # ag.java:1698-1737  (story picture + scrolling text)
        self.fill_screen_rgb(0, 0, 0)
        ct35 = GameCanvas.images[35]
        if GameCanvas.speech_line in (0, 2):
            if 0 < GameCanvas.story_fade < 4:
                self.draw_map_region(ct35, GameCanvas.view_cx - (ct35.getWidth() >> 1), GameCanvas.view_cy - (ct35.getHeight() >> 1),
                               ct35.getWidth(), ct35.getHeight(), 0, 0)
        elif GameCanvas.speech_line == 1:
            m = GameCanvas.speech_pos[0]
            if GameCanvas.story_page != GameCanvas.story_pages[2] - GameCanvas.story_pages[0]:
                self.draw_map_region(ct35, GameCanvas.view_cx - (ct35.getWidth() >> 1), GameCanvas.view_cy - (ct35.getHeight() >> 1),
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
                Gfx.set_font(GameCanvas.font_black)
                self.draw_text_at(GameCanvas.text_lines[0][j_], m + 1, 30)
                GameCanvas.draw_text_centred_at(GameCanvas.text_lines[0][j_], m - 1, 1)
                if c1 == 255:
                    Gfx.set_font(GameCanvas.font_white)
                elif c1 == 0:
                    Gfx.set_font(GameCanvas.font_black)
                else:
                    Gfx.set_font(GameCanvas.font_gray)
                self.draw_text_at(GameCanvas.text_lines[0][j_], m, 30)
                m += 22
                j_ += 1
        self.draw_skip_key(2)

    def draw_skip_key(self, paramInt):  # ag.java:1739-1741  (soft key "Skip")
        GameCanvas.draw_softkeys(0, -1)

    @staticmethod
    def char_width(paramByte):  # ag.java:3021-3024  (width of a character)
        return GameCanvas.font_white.char_width(chr(paramByte & 0xFFFF))

    def word_wrap(self, paramArrayOfbyte, paramInt1, paramInt2):  # ag.java:3100-3138  (word wrap into dp[paramInt2])
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
                i2 += GameCanvas.char_width(c)
                if (c == 32 or c == 124) and i2 - GameCanvas.char_width(c) >= paramInt1:
                    if i1 < m:
                        i1 = j_
                    dp[b] = GameCanvas.read_utf(paramArrayOfbyte, m, i1)
                    b += 1
                    m = i1 + 1
                    j_ = m - 1
                    i2 = 0
                elif c == 32:
                    i1 = j_
                elif c == 124:
                    dp[b] = GameCanvas.read_utf(paramArrayOfbyte, m, j_)
                    b += 1
                    m = i1 = j_ + 1
                    i2 = 0
            elif i2 > paramInt1:
                dp[b] = GameCanvas.read_utf(paramArrayOfbyte, m, i1)
                b += 1
                dp[b] = GameCanvas.read_utf(paramArrayOfbyte, i1 + 1, j_)
                b += 1
            elif i1 != n_ - 1:
                dp[b] = GameCanvas.read_utf(paramArrayOfbyte, m, j_)
                b += 1
            j_ += 1
        if b >= 1:
            GameCanvas.text_line_count[paramInt2] = i8(b - 1)
        return 1

    @staticmethod
    def parse_int(paramArrayOfchar):  # ag.java:3542-3547  (Integer.parseInt of the leading digits)
        str_ = ""
        b = 0
        while b < len(paramArrayOfchar) and '0' <= paramArrayOfchar[b] <= '9':
            str_ = str_ + paramArrayOfchar[b]
            b += 1
        return int(str_)

    # ---- menus: Options / Help / Endings helpers -------------------------------------------

    def edat_bytes(self, paramInt1, paramInt2):  # ag.java:1743-1745
        return GameCanvas.edat_string(paramInt1, paramInt2).encode("latin-1")

    @staticmethod
    def edat_string(paramInt1, paramInt2):  # ag.java:1747-1753  (string paramInt2 of edat file paramInt1)
        al1 = ScrTable("/" + GameCanvas.scr_data.get(paramInt1))
        str_ = al1.get(paramInt2)
        al1.free()
        return str_

    def draw_small_number(self, paramInt1, paramInt2, paramInt3):  # ag.java:1828-1830  (small number, ct[20])
        self.draw_image_part(paramInt1, paramInt2, paramInt3, 9, 12, GameCanvas.images[20], 0, 0, 0)

    def draw_image_part(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramImage,
                    paramInt6, paramInt7, paramInt8):  # ag.java:1832-1845  (number from a digit strip)
        if paramInt1 < 0 or paramImage is None:
            return
        paramInt2 -= paramInt4
        if paramInt1 > 0:
            while paramInt1 > 0:
                # DECOMP-FIX F10: `p6 + p4 * p1 % 10` -> `p6 + p4 * (p1 % 10)`
                sx = paramInt6 + paramInt4 * (paramInt1 % 10) if F10 else paramInt6 + paramInt4 * paramInt1 % 10
                GameCanvas.draw_region(paramInt2, paramInt3, paramInt4, paramInt5, paramImage, sx, paramInt7)
                paramInt1 //= 10
                paramInt2 -= paramInt4 + paramInt8
            return
        GameCanvas.draw_region(paramInt2, paramInt3, paramInt4, paramInt5, paramImage, paramInt6, paramInt7)

    def draw_empty_slot(self, paramInt1, paramInt2):  # ag.java:3169-3173  (empty 30x30 item slot)
        ac1 = Rect(paramInt1 + 1, paramInt2 + 1, 28, 28)
        self.draw_round_outline(paramInt1, paramInt2, 30, 30, 80, 80, 80)
        Gfx.fill_rect(ac1.x, ac1.y, ac1.w, ac1.h, 0)

    def draw_grey_frame(self, paramInt1, paramInt2, paramInt3, paramInt4):  # ag.java:3175-3179  (grey frame, black inside)
        ac1 = Rect(paramInt1 + 1, paramInt2 + 1, paramInt3 - 2, paramInt4 - 2)
        self.draw_round_outline(paramInt1, paramInt2, paramInt3, paramInt4, 152, 152, 152)
        Gfx.fill_rect(ac1.x, ac1.y, ac1.w, ac1.h, 0)

    def change_option(self, paramInt):  # ag.java:2474-2520  (Options: change the value of row cM[1])
        v = GameCanvas.menu[1]
        if v == 0:
            GameCanvas.sound_on = not GameCanvas.sound_on
            if GameCanvas.sound_on:
                self.play_sound(8)
            else:
                GameCanvas.stop_sound()
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
                GameCanvas.stop_sound()
            elif GameCanvas.volume > 0:
                GameCanvas.sound_on = True
                if system.currentTimeMillis() - GameCanvas.option_time > 300:
                    GameCanvas.option_time = system.currentTimeMillis()
                    self.play_sound(8)
        elif v == 2:
            if paramInt != 0:
                GameCanvas.speed = i16(GameCanvas.speed + 1)
                if GameCanvas.speed > 4:
                    GameCanvas.speed = 0
            else:
                GameCanvas.speed = i16(GameCanvas.speed - 1)
                if GameCanvas.speed < 0:
                    GameCanvas.speed = 4
        elif v == 3 and config.SCREEN_OPTION:      # PORT-EXTRA: Screen = full screen / window
            display.toggle_fullscreen()
            return
        GameCanvas.save_options()

    # ---- Management: items, descriptions ---------------------------------------------------

    @staticmethod
    def item_slot_type(paramInt):  # ag.java:867-870  (equipment slot type of an item)
        GameCanvas.menus.load_item_def(paramInt)
        if paramInt < 100:
            return 1
        if paramInt < 300:
            return i8(GameCanvas.gear_def.slot)
        if paramInt < 500:
            return GameCanvas.treasure_def.slot
        return GameCanvas.rare_def.slot

    @staticmethod
    def describe_shop_item(paramz, paramBoolean, paramInt):  # ag.java:1454-1457  (item description in the shop)
        # dF.a() (ak.java:10-17) - the method is shadowed by the field ak.a in Python
        dF = GameCanvas.info_box
        dF.shown = 0
        dF.rect.x = dF.rect.y = dF.rect.w = dF.rect.h = 0
        dF.text = ""
        GameCanvas.menus.draw_shop_description(paramz, 0, 0, 200, 22, paramInt, paramBoolean)

    @staticmethod
    def quick_slot_item(paramp):  # ag.java:1459-1465  (potion slot -> item)
        z1 = Item()
        Item.clear(z1)
        z1.id = paramp.item
        z1.attack = paramp.count
        return z1

    def item_under_cursor(self, paramInt):  # ag.java:1467-1492  (item under the cursor of the item grid)
        z1 = Item()
        if paramInt == -1:
            paramInt = GameCanvas.cursor[18]
        v = GameCanvas.cursor[0]
        if v == 0:
            z1 = GameCanvas.shop[paramInt]
        elif v == 1:
            if paramInt < 5:
                z1 = GameCanvas.quick_slot_item(GameCanvas.hero.quick_slots[paramInt])
            else:
                z1 = GameCanvas.hero.backpack[paramInt - 5]
        elif v in (2, 3):
            if GameCanvas.cursor[27] == 0:
                z1 = GameCanvas.hero.backpack[paramInt]
            else:
                z1 = GameCanvas.hero.equipped[paramInt]
        return z1

    @staticmethod
    def fill_rect(paramac, paramInt):  # ag.java:1507-1510  (fill rect)
        if paramac is not None:
            Gfx.fill_rect(paramac.x, paramac.y, paramac.w, paramac.h, paramInt)

    @staticmethod
    def outline_rect(paramac, paramInt):  # ag.java:1512-1515  (outline rect)
        if paramac is not None:
            Gfx.draw_rect(paramac.x, paramac.y, paramac.w, paramac.h, paramInt)

    @staticmethod
    def draw_filled_rect(paramac, paramInt1, paramInt2):  # ag.java:1517-1520
        Gfx.fill_rect(paramac.x, paramac.y, paramac.w, paramac.h, paramInt2)
        Gfx.draw_rect(paramac.x, paramac.y, paramac.w, paramac.h, paramInt1)

    @staticmethod
    def digit_count(paramInt):  # ag.java:1822-1826  (number of digits)
        arrayOfInt = [10, 100, 1000, 10000]
        b = 0
        while b < 4 and paramInt >= arrayOfInt[b]:
            b += 1
        return b + 1

    @staticmethod
    def measure_text(paramString):  # ag.java:1755-1757  (text width)
        return GameCanvas.font_white.string_width(paramString)

    def draw_small_digit(self, paramInt1, paramInt2, paramInt3):  # ag.java:1823-1825  (small digit from ct[20])
        self.draw_map_region(GameCanvas.images[20], paramInt1, paramInt2, 9, 12, paramInt3 * 9, 0)

    def draw_gold_box(self):  # ag.java:1279-1291  (gold box)
        arrayOfShort = [7, 14, 21, 32, 39, 46, 57, 64, 71, 82]
        j_ = GameCanvas.hero.gold
        self.draw_box(GameCanvas.view_cx - 70, GameCanvas.view_cy - 80 + GameCanvas.view_y, 140, 22, False)
        b = 0
        while b < 9:
            j_ = idiv(j_, 10)
            if 0 == j_:
                break
            b += 1
        self.draw_big_number(GameCanvas.hero.gold, GameCanvas.view_cx + (arrayOfShort[b] >> 1) + 16 - GameCanvas.view_x, GameCanvas.view_cy - 76, 0)
        self.draw_map_region(GameCanvas.images[32], GameCanvas.view_cx - 69 - GameCanvas.view_x, GameCanvas.view_cy - 80, GameCanvas.images[32].getWidth(), GameCanvas.images[32].getHeight(), 0, 0)

    def draw_description(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # ag.java:1293-1352  (description of item / skill)
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
                s6 = GameCanvas.set_item_name(it.id)
                s1 = it.attack
                s2 = it.defense
                s3 = it.hp
                s4 = it.mp
                s5 = i16(it.enchant)
                str_ = GameCanvas.special_suffix(it.id)
            elif paramInt1 < 2000:
                dF.text = GameCanvas.describe_potion(cz.quick_slots[paramInt1 - 1200].item)
            else:
                dF.text = self.describe_skill(paramInt1 - 2000)
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
            GameCanvas.text_width = GameCanvas.measure_text(dF.text)
            if GameCanvas.text_width > paramInt4 - 2:
                dF.shown = 1
                dF.text_x = i16(paramInt2 + 20)
                return
            dF.shown = 0
            dF.text_x = i16(paramInt2 + 1)

    def describe_skill(self, paramInt):  # ag.java:1354-1368  (skill description)
        str1 = ""
        paramInt -= 12
        if paramInt < 0 or paramInt > 18:
            return str1
        arrayOfByte = self.edat_bytes(54, paramInt)
        str2 = GameCanvas.read_utf(arrayOfByte, 0, len(arrayOfByte))
        if GameCanvas.hero.skill_levels[paramInt] != 0:
            arrayOfByte = self.edat_bytes(54, paramInt + 19)
            str1 = str2 + " / Lv" + str(GameCanvas.hero.skill_levels[paramInt]) + " " + GameCanvas.read_utf(arrayOfByte, 0, len(arrayOfByte))
        else:
            str1 = str2 + " / (Not Available)"
        return str1

    @staticmethod
    def describe_potion(paramInt):  # ag.java:1370-1381  (potion description)
        str_ = ""
        paramInt -= 1
        if paramInt < 0 or paramInt > 10:
            return str_
        if paramInt < 9:
            str_ = (consts.aN[paramInt] + " / Recover " + str(consts.aP[paramInt % 3]) + "% of total "
                    + consts.aO[paramInt // 3])
        else:
            arrayOfByte = GameCanvas.edat_string(54, 24 + paramInt).encode("latin-1")
            str_ = consts.aN[paramInt] + " / " + GameCanvas.read_utf(arrayOfByte, 0, len(arrayOfByte))
        return str_

    @staticmethod
    def special_suffix(paramInt):  # ag.java:1383-1399  (special item suffix)
        return {434: " / Hp 5 Increased", 435: " / MP 3 Increased", 436: " / DEF 1 Increased",
                437: " / ATK 1 Increased", 502: " / Catherine's scarf",
                504: " / all General Visiting"}.get(paramInt, "")

    @staticmethod
    def set_item_name(paramInt):  # ag.java:1401-1416  (item name -> dF.c, returns the level needed)
        GameCanvas.menus.load_item_def(paramInt)
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

    def draw_panel(self, paramInt1, paramInt2, paramInt3, paramInt4):  # ag.java:1246-1248
        GameCanvas.draw_frame_box(paramInt1 + 1, paramInt2 + 1, paramInt3 - 2, paramInt4 - 2, 0, 0, 10000536, True)

    def draw_centred_box(self, paramInt1, paramInt2, paramInt3):  # ag.java:1250-1254  (centred box, returns its x)
        j_ = 240 - paramInt2 >> 1
        self.draw_panel(j_, paramInt1, paramInt2, paramInt3)
        return j_

    def draw_gold_amount(self, paramInt1, paramInt2):  # ag.java:1256-1269  (gold box with amount paramInt1)
        j_ = self.draw_centred_box(paramInt2, 200, 22)
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
        self.draw_number_commas(paramInt1, j_ + m + 10, paramInt2)
        self.draw_map_region(GameCanvas.images[32], GameCanvas.view_cx - 69, paramInt2 - 5, GameCanvas.images[32].getWidth(), GameCanvas.images[32].getHeight(), 0, 0)

    def draw_hero_gold(self, paramInt):  # ag.java:1271-1273
        self.draw_gold_amount(GameCanvas.hero.gold, paramInt)

    def draw_number_commas(self, paramInt1, paramInt2, paramInt3):  # ag.java:2797-2808  (number with thousands commas)
        # DECOMP-FIX F12: the decompiled loop `do { if (!b || b % 3 != 0) continue; ... ++b; }`
        # skips every digit (the number is never drawn). Restored: comma before every 3rd digit.
        b = 0
        while True:
            if F12:
                if b != 0 and b % 3 == 0:
                    paramInt2 -= 4
                    GameCanvas.draw_region(paramInt2, paramInt3, 5, 14, GameCanvas.images[19], 100, 0)
                paramInt2 -= 10
                GameCanvas.draw_region(paramInt2, paramInt3, 10, 14, GameCanvas.images[19], imod(paramInt1, 10) * 10, 0)
                b += 1
            paramInt1 = idiv(paramInt1, 10)
            if not paramInt1 > 0:
                break

    @staticmethod
    def format_thousands(paramInt):  # ag.java:1437-1452  (12345 -> "12,345")
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
    def u8(paramByte):  # ag.java:3484-3486
        return i16(paramByte & 0xFF)

    def load_chapter_lords(self):  # ag.java:1043-1062  (lords of chapter cq -> ds/dt/du/dv, list dE = dt)
        j_ = 0
        arrayOfByte = GameCanvas.load_data_file(48)
        j_ = 38 * GameCanvas.chapter + 40
        GameCanvas.lord_count = 0
        for b in range(6):
            GameCanvas.lord_ids[b] = i8(arrayOfByte[j_ + b])
            if GameCanvas.lord_ids[b] > 0:
                m = 38 * GameCanvas.lord_ids[b] + 10
                b1 = 0
                while b1 < 30 and arrayOfByte[m + b1] != 0:
                    b1 += 1
                GameCanvas.lord_names[b] = GameCanvas.read_utf(arrayOfByte, m, m + b1)
                GameCanvas.lord_missions[b] = i8(arrayOfByte[m + 36])
                GameCanvas.lord_mission_counts[b] = i8(arrayOfByte[m + 37])
                GameCanvas.lord_count += 1
        GameCanvas.menu_count = GameCanvas.lord_count
        GameCanvas.menu_items = GameCanvas.lord_names

    def load_mission_text(self):  # ag.java:1064-1073  (mission description -> dp[0])
        GameCanvas.mission_name = GameCanvas.mission_names[GameCanvas.mission]
        arrayOfByte1 = GameCanvas.load_data_file(56)
        arrayOfByte2 = self.table_text(arrayOfByte1, GameCanvas.lord_missions[GameCanvas.lord] + GameCanvas.mission)
        b = 0
        while b < len(arrayOfByte2) and arrayOfByte2[b] != 0:
            b += 1
        arrayOfByte3 = bytearray(arrayOfByte2[:b])
        self.word_wrap(arrayOfByte3, 190, 0)

    def table_text(self, paramArrayOfbyte, paramInt):  # ag.java:1075-1124  (text paramInt of a table, "(..)" macros)
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
            m = GameCanvas.parse_int(arrayOfChar)
            _arraycopy(paramArrayOfbyte, arrayOfInt1[m], arrayOfByte2, 0, arrayOfInt1[m + 1] - arrayOfInt1[m])
        else:
            _arraycopy(arrayOfByte1, 0, arrayOfByte2, 0, 1500)
        while arrayOfByte2[arrayOfInt3[1]] != 0:
            if arrayOfByte2[arrayOfInt3[1]] == 40:
                arrayOfByte3 = GameCanvas.append_bytes(arrayOfByte3, arrayOfByte2, arrayOfInt2[1], arrayOfInt3[1])
                arrayOfInt2[1] = arrayOfInt3[1] + 1
                if b1 != 0:
                    arrayOfInt3[1] = GameCanvas.index_after(arrayOfByte2, arrayOfInt3[1], ')')
                    # DECOMP-FIX F15: the source is `arrayOfInt2[1] = arrayOfInt3[1] = a(.., ')')`
                    # (one call; JD split the dup_x2 into a second search). Literally the second
                    # search skips the next "(..)" and the copy length is negative: every mission
                    # description with a numbered template (Hellgate...) throws in arraycopy.
                    if config.DECOMP_FIX["F15"]:
                        arrayOfInt2[1] = arrayOfInt3[1]
                    else:
                        arrayOfInt2[1] = GameCanvas.index_after(arrayOfByte2, arrayOfInt3[1], ')')
                    arrayOfInt3[0] = GameCanvas.index_after(arrayOfByte1, arrayOfInt3[0], '|')
                    arrayOfByte3 = GameCanvas.append_bytes(arrayOfByte3, arrayOfByte1, arrayOfInt2[0], arrayOfInt3[0] - 1)
                    arrayOfInt2[0] = arrayOfInt3[0]
                    continue
                arrayOfInt3[1] = GameCanvas.index_after(arrayOfByte2, arrayOfInt3[1], ')')
                arrayOfByte3 = GameCanvas.append_bytes(arrayOfByte3, arrayOfByte2, arrayOfInt2[1], arrayOfInt3[1] - 1)
                arrayOfInt2[1] = arrayOfInt3[1]
                continue
            arrayOfInt3[1] = arrayOfInt3[1] + 1
        arrayOfByte3 = GameCanvas.append_bytes(arrayOfByte3, arrayOfByte2, arrayOfInt2[1], arrayOfInt3[1])
        return arrayOfByte3

    @staticmethod
    def append_bytes(paramArrayOfbyte1, paramArrayOfbyte2, paramInt1, paramInt2):  # ag.java:1126-1131  (append at the first 0)
        b = 0
        while b < len(paramArrayOfbyte1) and paramArrayOfbyte1[b] != 0:
            b += 1
        _arraycopy(paramArrayOfbyte2, paramInt1, paramArrayOfbyte1, b, paramInt2 - paramInt1)
        return paramArrayOfbyte1

    @staticmethod
    def index_after(paramArrayOfbyte, paramInt, paramChar):  # ag.java:1133-1142  (index after the next paramChar)
        c = ord(paramChar)
        b = 0
        while paramArrayOfbyte[paramInt + b] != c and paramArrayOfbyte[paramInt + b] != 0:
            if (paramArrayOfbyte[paramInt + b] & 0x80) != 0:
                b += 2
            b += 1
        return paramInt + b + 1

    def free_hud(self):  # ag.java:2277-2281
        for b in range(6):
            GameCanvas.hud_frame[b] = None
        GameCanvas.gc()

    def enter_map(self):  # ag.java:872-967  (enter the map: bV = 3)
        cz = GameCanvas.hero
        cz.weapon_kind = GameCanvas.item_slot_type(cz.equipped[0].id)
        GameCanvas.stop_sound()
        self.free_hero_sprites()
        GameCanvas.menus.free_shop_images()
        self.load_hud()
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
        GameCanvas.update_hero_stats()
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
                GameCanvas.enemy_frames[b] = self.load_frames(82 + b)
        self.load_lord_map(bool_)
        self.load_enemy_sprites()
        GameCanvas.hero_weapon_frames[cz.weapon_kind] = self.load_frames(87 + (cz.weapon_kind << 2))
        cz.head_frames2 = self.load_frames(51 + cz.head)
        cz.body_frames2 = self.load_frames(46)
        GameCanvas.hero_body_frames[cz.weapon_kind] = self.load_frames(89 + (cz.weapon_kind << 2))
        GameCanvas.images[40 + cz.weapon_kind] = self.load_image(GameCanvas.scr_char.get(42 + cz.weapon_kind))
        GameCanvas.trail_frames = self.load_frames(86)
        self.load_effect_image()
        GameCanvas.shadow_frames = self.load_frames(98)
        GameCanvas.shadow_image = self.load_image(GameCanvas.scr_effect.get(44))
        GameCanvas.spark_frames = self.load_frames(55)
        GameCanvas.images[43] = self.load_image(GameCanvas.scr_effect.get(0))
        GameCanvas.skill_frames = self.load_frames(56)
        GameCanvas.images[44] = self.load_image(GameCanvas.scr_effect.get(1))
        GameCanvas.images[31] = self.load_image(GameCanvas.scr_ui.get(52))
        GameCanvas.general_mark = self.load_image(GameCanvas.scr_char.get(45))
        GameCanvas.clock[1] = GameCanvas.now()
        GameCanvas.clock[0] = GameCanvas.now()
        GameCanvas.play_time = GameCanvas.clock[0] - GameCanvas.play_time
        GameCanvas.clock[1] = GameCanvas.now()
        GameCanvas.play_time = GameCanvas.clock[0] = GameCanvas.now()
        GameCanvas.save_flag = 1
        GameCanvas.mission_seconds = 0

    def load_effect_image(self):  # ag.java:969-971
        GameCanvas.images[42] = self.load_image(GameCanvas.scr_effect.get(2))

    def load_enemy_sprites(self):  # ag.java:973-988  (enemy sprites, recoloured by dz.d)
        arrayOfInt = [56, 57]
        for b in range(len(arrayOfInt)):
            if GameCanvas.lords[GameCanvas.mission].tint != 0:
                GameCanvas.enemy_images[b] = None
                GameCanvas.enemy_frames[b] = None
                GameCanvas.enemy_images[b] = GameCanvas.load_recoloured(GameCanvas.scr_char.get(arrayOfInt[b]), GameCanvas.lords[GameCanvas.mission].tint)
            else:
                GameCanvas.enemy_images[b] = None
                GameCanvas.enemy_frames[b] = None
                GameCanvas.enemy_images[b] = self.load_image(GameCanvas.scr_char.get(arrayOfInt[b]))
            if GameCanvas.enemy_frames[b] is None:
                GameCanvas.enemy_frames[b] = self.load_frames(82 + b)

    _PAL = [[[236, 211, 197], [205, 143, 128], [129, 81, 69], [104, 60, 49], [79, 39, 29]],
            [[226, 205, 178], [196, 179, 152], [180, 142, 122], [135, 111, 47], [93, 73, 49]],
            [[174, 225, 242], [101, 156, 195], [61, 102, 139], [43, 78, 115], [45, 45, 84]],
            [[162, 199, 159], [135, 156, 119], [86, 123, 98], [33, 98, 63], [51, 51, 51]]]

    @staticmethod
    def load_recoloured(paramString, paramInt):  # ag.java:990-1023  (PNG with palette 0 replaced by palette paramInt)
        str_ = "/" + paramString + ".png"
        arrayOfByte = bytearray(ResReader.read(str_))
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
        l1 = Gfx.crc32(arrayOfByte, i1, i2 + 4)
        arrayOfByte[i1 + i2 + 4] = l1 >> 24 & 0xFF
        arrayOfByte[i1 + i2 + 5] = l1 >> 16 & 0xFF
        arrayOfByte[i1 + i2 + 6] = l1 >> 8 & 0xFF
        arrayOfByte[i1 + i2 + 7] = l1 & 0xFF
        return Image.createImage(arrayOfByte, 0, len(arrayOfByte))

    def load_lord_map(self, paramInt):  # ag.java:1025-1037  (load the map of the current lord, room around the hero)
        from pow.game.map_scene import MapScene
        self.fill_screen_rgb(0, 0, 0)
        ct34 = GameCanvas.images[34]
        self.draw_view_region(ct34, GameCanvas.canvas_size.x // 2 - ct34.getWidth() // 2, GameCanvas.canvas_size.y // 2 - ct34.getHeight() // 2,
                       ct34.getWidth(), ct34.getHeight(), 0, 0)
        GameCanvas.redraw = 1
        MapScene.hero_cell()
        GameCanvas.view_tx = idiv(GameCanvas.hero.room_pos[0].x - 1, 7) * 7 + 4 - (GameCanvas.view_tiles.x >> 1)
        GameCanvas.view_ty = idiv(GameCanvas.hero.room_pos[0].y - 1, 7) * 7 + 4 - (GameCanvas.view_tiles.y >> 1)
        GameCanvas.hero.room_pos[1].x = GameCanvas.hero.room_pos[0].x
        GameCanvas.hero.room_pos[1].y = GameCanvas.hero.room_pos[0].y
        GameCanvas.map = GameCanvas.scene.load_map(GameCanvas.map_id)
        GameCanvas.scene.load_rooms(GameCanvas.lord_ids[GameCanvas.lord])
        GameCanvas.scene.draw_tiles(GameCanvas.view_tiles.x, GameCanvas.view_tiles.y, GameCanvas.view_tx, GameCanvas.view_ty, paramInt)

    def load_hud(self):  # ag.java:2271-2275  (HUD frame pieces)
        arrayOfInt = [79, 61, 82, 78, 83, 81]
        for b in range(6):
            GameCanvas.hud_frame[b] = self.load_image(GameCanvas.scr_ui.get(arrayOfInt[b]))

    def draw_digit(self, paramInt1, paramInt2, paramInt3):  # ag.java:2793-2795  (one digit of ct[19])
        self.draw_map_region(GameCanvas.images[19], paramInt2, paramInt3, 10, 14, 10 * paramInt1, 0)

    @staticmethod
    def decimal_digits(paramInt):  # ag.java:2842-2847  (number of decimal digits)
        b = 1
        j_ = 10
        while paramInt >= j_:
            b += 1
            j_ *= 10
        return b

    def draw_clock(self, paramInt1, paramInt2, paramInt3):  # ag.java:2849-2855  (mission clock mm:ss)
        arrayOfInt1 = [0, 9, 25, 34]
        arrayOfInt2 = [idiv(paramInt3, 600) % 10, idiv(paramInt3, 60) % 10, paramInt3 % 60 // 10, paramInt3 % 10]
        for b in range(4):
            self.draw_digit(arrayOfInt2[b], paramInt1 + arrayOfInt1[b] + 10, paramInt2)
        self.draw_map_region(GameCanvas.images[19], paramInt1 + 20 + 10, paramInt2, 4, 14, 115, 0)

    def free_map_images(self):  # ag.java:2548-2570  (free the map images; `al` would hide the al class)
        GameCanvas.free_hero_images()
        GameCanvas.images[4] = None
        if GameCanvas.tile_images is not None:
            for b1 in range(len(GameCanvas.tile_images)):
                GameCanvas.tile_images[b1] = None
            GameCanvas.tile_images = None
        GameCanvas.images[9] = None
        GameCanvas.images[11] = None
        GameCanvas.images[12] = None
        GameCanvas.images[16] = None
        GameCanvas.menus.free_shop_images()
        for b in range(5):
            GameCanvas.images[35 + b] = None
        for b in range(4):
            GameCanvas.images[21 + b] = None
        GameCanvas.view_size.x = GameCanvas.canvas_size.x
        GameCanvas.view_size.y = GameCanvas.canvas_size.y
        GameCanvas.view_x = 0
        GameCanvas.view_y = 0

    def start_dialogue(self):  # ag.java:2572-2582  (start a dialogue: briefing dG 0, map talk 1, general 2)
        GameCanvas.talk_box = 0
        GameCanvas.talk_row = 0
        GameCanvas.talk_rows = 0
        GameCanvas.talk_side = 0
        GameCanvas.wait_ticks = 0
        GameCanvas.next_speech_pos()
        self.start_dialogue_text()
        if GameCanvas.talk_line < 200:
            self.load_dialogue_line(GameCanvas.talk_line)

    def load_dialogue_line(self, paramInt):  # ag.java:2584-2637  (line paramInt of dialogue file 57+dG -> dp[dR])
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
                        self.set_general(GameCanvas.lords[GameCanvas.mission].general)
                    else:
                        self.set_general(GameCanvas.cells[GameCanvas.cell].general)
                str1 = GameCanvas.general.name
        else:
            str1 = GameCanvas.hero.name
        arrayOfByte2 = GameCanvas.load_data_file(57 + GameCanvas.talk_kind)
        j_ = arrayOfByte2[0] & 0xFF | arrayOfByte2[1] << 8 & 0xFF00
        for b1 in range(j_ + 1):
            arrayOfInt[b1] = arrayOfByte2[2 + b1 * 2] & 0xFF | arrayOfByte2[2 + b1 * 2 + 1] << 8 & 0xFF00
        arrayOfString[0] = GameCanvas.read_utf(arrayOfByte2, arrayOfInt[paramInt], arrayOfInt[paramInt + 1])
        arrayOfString[1] = "[" + str1 + "] "
        GameCanvas.text_width = len(arrayOfString[0])
        m = 0
        for b1 in range(GameCanvas.text_width):
            if arrayOfString[0][b1] == '&':
                if m != b1:
                    # System.arraycopy(String[], m, String, ...) would throw in Java; the game
                    # only prints this marker, so the texts never have '&' after other text
                    GameCanvas.log("=========================check this 96430jfds")
                arrayOfString[1] = arrayOfString[1] + str1
                m = b1 + 1
        str2 = ""
        for b2 in range(len(arrayOfString[0])):
            if arrayOfString[0][b2] != '&':
                str2 = str2 + arrayOfString[0][b2]
        arrayOfString[0] = str2
        if m < GameCanvas.text_width:
            arrayOfString[1] = arrayOfString[1] + arrayOfString[0]
        self.word_wrap(bytearray(arrayOfString[1].encode("utf-8")), 150, s)

    def start_dialogue_text(self):  # ag.java:2639-2681  (first line dI of the dialogue)
        from pow.game.menus import Menus
        v = GameCanvas.talk_kind
        if v == 0:
            if GameCanvas.talk_count > 10:
                GameCanvas.talk_count = 11
                GameCanvas.talk_line = i16(GameCanvas.rand_range(0, 18) + 10 << 1)
                return
            GameCanvas.talk_line = i16(GameCanvas.talk_count - 1 << 1)
            return
        if v == 1:
            j_ = 0
            Menus.add_friendship(GameCanvas.talk_general, -5)
            GameCanvas.talk_line = 21
            return
        if v == 2:
            if GameCanvas.boss_fight != 0:
                j_ = GameCanvas.lords[GameCanvas.mission].general
            else:
                j_ = GameCanvas.cells[GameCanvas.cell].general
            if 0 == j_:
                GameCanvas.redraw = 1
                self.open_menu(2)
                self.load_menu_frames()
                GameCanvas.menu[0] = 0
                GameCanvas.menu_count = consts.v[GameCanvas.menu[0]]
                GameCanvas.menu_items = GameCanvas.game_menu_items
                GameCanvas.talk_line = 200
                GameCanvas.state = 2
                GameCanvas.menu_scroll = 0
                GameCanvas.menu_anim = 0
                return
            Menus.add_friendship(j_, 5)
            GameCanvas.talk_points = j_
            j_ = GameCanvas.friendship(j_)
            if j_ >= 100:
                j_ = 95
            GameCanvas.talk_line = i16(j_ // 10 * 5)

    @staticmethod
    def friendship(paramInt):  # ag.java:2683-2687  (friendship points of general paramInt)
        b = 0
        while b < GameCanvas.general_count and GameCanvas.generals[0][b] != paramInt:
            b += 1
        return 0 if b == GameCanvas.general_count else GameCanvas.generals[1][b]

    @staticmethod
    def next_speech_pos():  # ag.java:2689-2703  (position of the next speech box)
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

    def set_general(self, paramInt):  # ag.java:2705-2726  (general paramInt -> dC)
        arrayOfByte = None
        j_ = 0
        arrayOfByte = GameCanvas.load_data_file(46)
        j_ = 23 * (paramInt - 1) + 14
        dC = GameCanvas.general
        dC.name = ""
        b = 0
        while b < 11 and arrayOfByte[j_ + b] != 0:
            b += 1
        dC.name = GameCanvas.read_utf(arrayOfByte, j_, j_ + b)
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

    def random_general_skill(self, paramInt):  # ag.java:1494-1505  (random skill of general dC)
        b = 0
        while b < 4 and 0 != GameCanvas.general.skills[b]:
            b += 1
        if paramInt != 0:
            while True:
                c1 = GameCanvas.general.skills[self.rand(b)]
                if not c1 > 0o20:
                    return c1
        return GameCanvas.general.skills[self.rand(b)]



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
