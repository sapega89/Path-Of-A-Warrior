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

    def __init__(self, main):  # ag.java:560-564
        Canvas.__init__(self)
        GameCanvas.midlet = main
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

    def keyPressed(self, key):  # ag.java:660-662
        self.key_down(key)

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
    def log(text):  # ag.java:687-689
        print(" " + text)

    def paint(self, graphics):  # ag.java:691-706  (synchronized)
        GameCanvas.painted = False
        GameCanvas.screen_g = graphics
        Gfx.set_graphics(graphics)
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
                now = system.currentTimeMillis()
                j_ = (consts.speed_frame_ms[GameCanvas.speed] if GameCanvas.state == 3 else consts.speed_frame_ms[2]) - int(now - GameCanvas.tick_start)
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
                    GameCanvas.menu_count = consts.menu_sizes[0]
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
    def sleep(ms):  # ag.java:769-777
        system.sleep(ms)

    def hideNotify(self):  # ag.java:779-781
        self.set_paused(True)

    def showNotify(self):  # ag.java:783-785
        self.set_paused(True)

    def set_paused(self, paused):  # ag.java:787-799
        from pow.game.midlet import Midlet
        if paused and GameCanvas.state == 3:
            self.map_started = True
        elif not paused:
            self.map_started = False
        if GameCanvas.paused == paused or GameFields.key_lock or GameFields.key_delay > 0:
            return
        if not Midlet.started or not GameCanvas.started:
            return
        GameCanvas.pause_pending = True
        GameCanvas.pause_pending_value = paused

    def apply_pause(self, paused):  # ag.java:801-818
        from pow.game.sound import Sound
        GameCanvas.paused = paused
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
    def draw_text_left(x, y, text):  # ag.java:1144-1147
        if text is not None:
            Gfx.draw_string(text, x, y, 0)

    @staticmethod
    def draw_text_centred(x, y, text):  # ag.java:1149-1152
        if text is not None:
            Gfx.draw_string(text, x, y, 1)

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
        record = bytearray(2)
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_env", False)
            if recordStore is None or recordStore.getNumRecords() < 1:
                return
            record = recordStore.getRecord(1)
            GameCanvas.save_pos = len(record)
        except Exception:
            pass
        if GameCanvas.save_pos >= 2:
            GameCanvas.volume = i8(record[0])
            GameCanvas.speed = i8(record[1])

    @staticmethod
    def save_options():  # ag.java:1188-1201
        record = bytearray(2)
        record[0] = GameCanvas.volume & 0xFF
        record[1] = GameCanvas.speed & 0xFF
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_env", True)
            if recordStore.getNumRecords() == 0:
                recordStore.addRecord(record, 0, len(record))
            recordStore.setRecord(1, record, 0, len(record))
        except Exception:
            return

    @staticmethod
    def clamp_menu_scroll():  # ag.java:1203-1210
        if GameCanvas.menu[1] < GameCanvas.menu[2]:
            GameCanvas.menu[2] = GameCanvas.menu[1]
            return
        if GameCanvas.menu[1] > GameCanvas.menu[2] + 4:
            GameCanvas.menu[2] = GameCanvas.menu[1] - 4

    def draw_view_region(self, image, x, y, w, h, src_x, src_y):  # ag.java:1212-1214
        GameCanvas.draw_region(x, y, w, h, image, src_x, src_y)

    @staticmethod
    def split_field(text, index):  # ag.java:1216-1240  (field #paramInt of "a|b|c")
        if text is None:
            return None
        bool_ = False
        j_ = 0
        end = 0
        field = 0
        text = text + "|"
        for pos in range(len(text)):
            if text[pos] == '|':
                field += 1
            if not bool_ and field == index:
                if field == 0:
                    j_ = pos
                else:
                    j_ = pos + 1
                bool_ = True
            elif bool_ and field == index + 1:
                end = pos
                break
        return text[j_:end]

    @staticmethod
    def draw_text(x, y, text):  # ag.java:1242-1244
        Gfx.draw_string(text, x, y, 0)

    @staticmethod
    def u16(lo, hi):  # ag.java:1275-1277
        return i16(lo & 0xFF | (hi & 0xFF) << 8)

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

    def fill_view(self, r, g, b):  # ag.java:1433-1435
        Gfx.fill_rect(GameCanvas.view_x, GameCanvas.view_y, GameCanvas.view_size.x, GameCanvas.view_size.y, GameCanvas.rgb(r, g, b))

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

    def play_sound(self, sound):  # ag.java:1882-1885
        if GameCanvas.sound is not None:
            GameCanvas.sound.play_sound(sound)

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
            if GameCanvas.sound is not None and GameCanvas.menu[0] < 29 and Sound.music != consts.menu_music[GameCanvas.menu[0]] and GameCanvas.menu[0] != 20 and not GameCanvas.in_live:
                self.play_sound(consts.menu_music[GameCanvas.menu[0]])
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

    def key_down(self, key):  # ag.java:1941-1961
        if key == -10:
            return
        if key == -100:               # PORT-EXTRA: Tab / the AUTO corner (pow/game/autopilot.py)
            from pow.game.autopilot import Autopilot
            Autopilot.toggle()
            return
        if GameCanvas.paused:
            GameCanvas.key = key
            return
        GameCanvas.key_pressed = key
        if key in (-4, -3, -2, -1, 50, 52, 54, 56):
            GameCanvas.key_held = key

    def load_image(self, name):  # ag.java:1963-1975
        GameCanvas.gc()
        str_ = "/" + name + ".png"
        image = None
        try:
            image = Image.createImage(str_)
        except Exception:
            print("======== createMixImage failuer :" + name)
            return None
        GameCanvas.gc()
        return image

    @staticmethod
    def gc():  # ag.java:1977-1979  (System.gc)
        pass

    @staticmethod
    def fill_screen(color):  # ag.java:1981-1983
        Gfx.fill_rect(0, 0, GameCanvas.screen_w, GameCanvas.screen_h, color)

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

    def draw_image_file(self, name, x, y, w, h, src_x, src_y):  # ag.java:1998-2002
        image = self.load_image(name)
        if image is not None:
            GameCanvas.draw_region(x, y, w, h, image, src_x, src_y)

    def tick_title(self):  # ag.java:2004-2124  (title -> Main Menu)
        cz = GameCanvas.hero
        for b in range(8):
            q = consts.dir8_to_dir4[b]
            cz.anim_0[b] = consts.hero_anim_0[q]
            cz.anim_1[b] = consts.hero_anim_1[q]
            cz.anim_2[b] = consts.hero_anim_2[q]
            cz.anim_9[b] = consts.hero_anim_9[q]
            cz.anim_3[b] = consts.hero_anim_3[q]
            cz.anim_4[b] = consts.hero_anim_4[q]
            cz.anim_5[b] = consts.hero_anim_5[q]
            cz.anim_6[b] = consts.hero_anim_6[q]
            cz.anim_7[b] = consts.hero_anim_7[q]
            cz.anim_8[b] = consts.hero_anim_8[q]
            cz.anim_10[b] = consts.hero_anim_10
            cz.anim_11[b] = consts.hero_anim_11[q]
            cz.anim_12[b] = consts.hero_anim_12[q]
            cz.anim_13[b] = consts.hero_anim_13[q]
            cz.anim_14[b] = consts.hero_anim_14[q]
            cz.anim_15_19[b] = consts.hero_anim_15_19
            cz.anim_20[b] = consts.hero_anim_20[q]
            cz.anim_21[b] = consts.hero_anim_21[q]
            cz.anim_22[b] = consts.hero_anim_22[q]
            cz.anim_23_24[b] = consts.hero_anim_23_24
            cz.anim_25[b] = consts.hero_anim_25[q]
            cz.anim_26_27[b] = consts.hero_anim_26_27[q]
            cz.anim_28[b] = consts.hero_anim_28
            cz.anim_29[b] = consts.hero_anim_29
            cz.anim_30[b] = consts.hero_anim_30
            GameCanvas.head_anim[b][0] = consts.head_anim_0[q]
            GameCanvas.head_anim[b][1] = consts.head_anim_1[q]
            GameCanvas.head_anim[b][2] = consts.head_anim_2[q]
            GameCanvas.head_anim[b][3] = consts.head_anim_3[q]
            GameCanvas.head_anims[b] = GameCanvas.head_anim[b]
            GameCanvas.body_anim[b][0] = consts.body_anim_0[q]
            GameCanvas.body_anim[b][1] = consts.body_anim_1[q]
            GameCanvas.body_anim[b][2] = consts.body_anim_2[q]
            GameCanvas.body_anim[b][3] = consts.body_anim_3[q]
            GameCanvas.body_anims[b] = GameCanvas.body_anim[b]
            GameCanvas.weapon_anim[b][0] = consts.head_anim_0[q]
            GameCanvas.weapon_anim[b][1] = consts.weapon_anim_1[q]
            GameCanvas.weapon_anim[b][2] = consts.weapon_anim_2[q]
            GameCanvas.weapon_anim[b][3] = consts.weapon_anim_3
            GameCanvas.weapon_anim[b][4] = consts.weapon_anim_1[q]
            GameCanvas.weapon_anim[b][5] = consts.weapon_anim_1[q]
            GameCanvas.weapon_anim[b][6] = consts.hero_anim_12[q]
            GameCanvas.weapon_anim[b][7] = consts.hero_anim_13[q]
            GameCanvas.weapon_anim[b][8] = consts.hero_anim_14[q]
            GameCanvas.weapon_anim[b][9] = consts.hero_anim_15_19
            GameCanvas.weapon_anim[b][10] = consts.hero_anim_15_19
            GameCanvas.weapon_anim[b][11] = consts.hero_anim_15_19
            GameCanvas.weapon_anim[b][12] = consts.hero_anim_15_19
            GameCanvas.weapon_anim[b][13] = consts.hero_anim_15_19
            GameCanvas.weapon_anim[b][14] = consts.hero_anim_20[q]
            GameCanvas.weapon_anim[b][15] = consts.hero_anim_21[q]
            GameCanvas.weapon_anim[b][16] = consts.hero_anim_22[q]
            GameCanvas.weapon_anim[b][17] = consts.hero_anim_23_24
            GameCanvas.weapon_anim[b][18] = consts.hero_anim_23_24
            GameCanvas.weapon_anim[b][19] = consts.hero_anim_25[q]
            GameCanvas.weapon_anim[b][20] = consts.hero_anim_26_27[q]
            GameCanvas.weapon_anim[b][21] = consts.hero_anim_26_27[q]
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
            reserved = [0] * 16
            name_len = 0
            while name_len < 8 and cF[2 + name_len] != 32:
                name_len += 1
            name_utf = bytearray(name_len)
            for i in range(name_len):
                name_utf[i] = cF[2 + i]
            cz.name = GameCanvas.read_utf(name_utf, 0, name_len)
            GameCanvas.save_flag = i8(cF[18])
            GameCanvas.save_pos = 19
            GameCanvas.lord = GameCanvas.read_byte()
            GameCanvas.mission = GameCanvas.read_byte()
            GameCanvas.rooms_visited = GameCanvas.read_byte()
            GameCanvas.missions_done = GameCanvas.read_long()
            GameCanvas.lords_done = GameCanvas.read_long()
            for i in range(8):
                GameCanvas.stats[i] = GameCanvas.read_int()
            GameCanvas.mission_exp = GameCanvas.read_int()
            GameCanvas.score = GameCanvas.read_int()
            for i in range(44):
                GameCanvas.generals[0][i] = GameCanvas.read_byte()
                GameCanvas.generals[1][i] = GameCanvas.read_byte()
            GameCanvas.general_count = GameCanvas.read_byte()
            for i in range(25):
                GameCanvas.shop[i] = self.read_item()
            GameCanvas.chapter = GameCanvas.read_byte()
            cz.pos[0].x = GameCanvas.read_short()
            cz.pos[0].y = GameCanvas.read_short()
            # Java int division (values are positions >= 0, so // == /)
            cz.pos[0].x = i16((cz.pos[0].x // 27 // 7 * 7 + 4) * 27 + 8)
            cz.pos[0].y = i16((cz.pos[0].y // 27 // 7 * 7 + 4) * 27 + 8)
            for i in range(22):
                cz.mission_progress[i] = GameCanvas.read_byte()
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
            for i in range(5):
                cz.hotkeys[i] = GameCanvas.read_byte()
            for i in range(19):
                cz.skill_levels[i] = GameCanvas.read_byte()
            for i in range(9):
                cz.equipped[i] = self.read_item()
            for i in range(25):
                cz.backpack[i] = self.read_item()
            for i in range(5):
                cz.quick_slots[i].item = GameCanvas.read_short()
                cz.quick_slots[i].count = GameCanvas.read_byte()
            cz.quick_keys[0] = GameCanvas.read_byte()
            cz.quick_keys[1] = GameCanvas.read_byte()
            cz.head = GameCanvas.read_byte()
            GameCanvas.play_time = GameCanvas.read_int()
            GameCanvas.live_time = GameCanvas.read_int()
            GameCanvas.live_gifts = GameCanvas.read_byte()
            GameCanvas.live_saved = GameCanvas.read_byte()
            GameCanvas.talk_count = GameCanvas.read_byte()
            GameCanvas.difficulty = GameCanvas.read_byte()
            for i in range(16):
                reserved[i] = GameCanvas.read_byte()
            GameCanvas.talk_points = GameCanvas.read_int()
            for i in range(4):
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
        value = 0
        for k_ in range(8):
            value |= (cF[cG + k_] & 0xFF) << (8 * k_)
        GameCanvas.save_pos += 8
        return value - (1 << 64) if value & (1 << 63) else value

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
        item = Item()
        item.id = GameCanvas.read_short()
        item.attack = GameCanvas.read_short()
        item.defense = GameCanvas.read_short()
        item.hp = GameCanvas.read_short()
        item.mp = GameCanvas.read_short()
        item.enchant = GameCanvas.read_byte()
        return item

    def load_ui_images(self):  # ag.java:2263-2269
        GameCanvas.images[34] = self.load_image(GameCanvas.scr_ui.get(22))
        GameCanvas.images[19] = self.load_image(GameCanvas.scr_ui.get(24))
        GameCanvas.images[20] = self.load_image(GameCanvas.scr_ui.get(25))
        GameCanvas.images[0] = self.load_image(GameCanvas.scr_ui.get(48))
        GameCanvas.images[32] = self.load_image(GameCanvas.scr_ui.get(37))

    @staticmethod
    def load_data_file(index):  # ag.java:2283-2285
        return ResReader.read("/" + GameCanvas.scr_data.get(index))

    def open_menu(self, mode):  # ag.java:2287-2304
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
        self.draw_menu_background(mode)
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
        table = ScrTable("/" + GameCanvas.scr_data.get(69))
        for b in range(30):
            GameCanvas.menu_titles[b] = table.get(b)
            if b < 7:
                GameCanvas.skill_names[b] = table.get(b + 48)
            if b < 6:
                GameCanvas.main_menu_items[b] = table.get(b + 30)
            if b < 5:
                GameCanvas.speed_names[b] = table.get(b + 55)
            if b < 4:
                GameCanvas.option_names[b] = table.get(b + 42)
            if b < 2:
                GameCanvas.on_off[b] = table.get(b + 46)
        GameCanvas.game_menu_items[0] = table.get(36)
        GameCanvas.yes_no_items[0] = table.get(37)
        GameCanvas.help_items[0] = table.get(38)
        GameCanvas.ok_items[0] = table.get(39)
        GameCanvas.continue_items[0] = table.get(40)
        GameCanvas.pause_items[0] = table.get(41)
        table.free()

    def draw_menu_background(self, mode):  # ag.java:2345-2370  (menu background into ct[7])
        if mode == 1:
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
            for col in range(4):
                GameCanvas.draw_region_at(GameCanvas.images[9], 0, 0, (b & 0x1) * -31 + col * j_, b * m, j_, m)
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

    def swap_items(self, a, b):  # ag.java:2384-2389
        tmp = Item()
        GameCanvas.copy_item(tmp, a)
        GameCanvas.copy_item(a, b)
        GameCanvas.copy_item(b, tmp)

    @staticmethod
    def copy_item(dst, src):  # ag.java:2391-2398
        dst.id = src.id
        dst.attack = src.attack
        dst.defense = src.defense
        dst.hp = src.hp
        dst.mp = src.mp
        dst.enchant = src.enchant

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
            for i in range(len(GameCanvas.tile_images)):
                GameCanvas.tile_images[i] = None
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
    def draw_region(x, y, w, h, image, src_x, src_y):  # ag.java:2438-2440
        Gfx.draw_image_part(image, x, y, w, h, src_x, src_y)

    def draw_map_region(self, image, x, y, w, h, src_x, src_y):  # ag.java:2442-2457
        clip_top = y
        if clip_top > 0:
            clip_top = 0
        clip_bottom = GameCanvas.view_size.y - y - h
        if clip_bottom > 0:
            clip_bottom = 0
        j_ = x
        if j_ > 0:
            j_ = 0
        m = GameCanvas.view_size.x - x - w
        if m > 0:
            m = 0
        if h + clip_top + clip_bottom > 0 and w + j_ + m > 0:
            GameCanvas.draw_region(x + GameCanvas.view_x - j_, y - clip_top + GameCanvas.view_y, w + j_ + m, h + clip_top + clip_bottom,
                         image, src_x - j_, src_y - clip_top)

    @staticmethod
    def draw_region_at(image, src_x, src_y, x, y, w, h):  # ag.java:2459-2461
        Gfx.draw_image_part(image, x, y, w, h, src_x, src_y)

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
        GameCanvas.menu_count = consts.menu_sizes[GameCanvas.menu[0]]
        GameCanvas.menu[1] = GameCanvas.menu_cursors[GameCanvas.menu[0]]
        GameCanvas.menu[2] = GameCanvas.menu_tops[GameCanvas.menu[0]]
        GameCanvas.redraw = 1

    @staticmethod
    def draw_text_centred_at(text, y, dx):  # ag.java:2743-2746  (centred text)
        y += 2
        Gfx.draw_string(text, GameCanvas.view_cx + GameCanvas.view_x + dx, y + GameCanvas.view_y, 1)

    def draw_text_at(self, text, y, unused):  # ag.java:2748-2750
        GameCanvas.draw_text_centred_at(text, y, 0)

    @staticmethod
    def draw_view_text_centred(text, x, y):  # ag.java:2752-2754
        Gfx.draw_string(text, x + GameCanvas.view_x, y + GameCanvas.view_y, 1)

    @staticmethod
    def draw_view_text(text, x, y):  # ag.java:2756-2758
        Gfx.draw_string(text, x + GameCanvas.view_x, y + GameCanvas.view_y, 0)

    def draw_box(self, x, y, w, h, selected):  # ag.java:2760-2762
        GameCanvas.draw_frame_box(x, y, w, h, 0, 5263440, 16777215, selected)

    @staticmethod
    def draw_frame_box(x, y, w, h, fill, outer, inner, framed):  # ag.java:2764-2791
        rect = Rect(0, 0, 0, 0)
        if framed:
            rect.x = x - 2
            rect.w = w + 4
            rect.y = y - 1
            rect.h = h + 2
            Gfx.draw_rect(rect.x, rect.y, rect.w, rect.h, inner)
            rect.x += 1
            rect.w -= 2
            rect.y -= 1
            rect.h += 2
            Gfx.draw_rect(rect.x, rect.y, rect.w, rect.h, inner)
        rect.x = x - 1
        rect.w = w + 2
        rect.y = y
        rect.h = h
        Gfx.draw_rect(rect.x, rect.y, rect.w, rect.h, outer)
        rect.x += 1
        rect.w -= 2
        rect.y -= 1
        rect.h += 2
        Gfx.draw_rect(rect.x, rect.y, rect.w, rect.h, outer)
        rect.y += 1
        rect.h -= 2
        Gfx.fill_rect(rect.x, rect.y, rect.w, rect.h, fill)

    @staticmethod
    def rgb(r, g, b):  # ag.java:2857-2860
        return (r & 0xFF) << 16 | (g & 0xFF) << 8 | b & 0xFF

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
    def read_utf(data, start, end):  # ag.java:3026-3043  (readUTF of bytes[from:to])
        j_ = start
        m = end
        str_ = None
        try:
            size = m - j_
            utf = bytearray(size + 2)
            utf[0] = size >> 8 & 0xFF
            utf[1] = size & 0xFF
            utf[2:] = data[j_:j_ + size]
            str_ = _read_utf(utf)
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
    def draw_softkeys(left, right):  # ag.java:3045-3079  (soft-key captions)
        if GameCanvas.popups.kind != 0:
            return
        j_ = GameCanvas.softkey_bg.getWidth()
        m = GameCanvas.softkey_bg.getHeight()
        str_ = ""
        if left != -1:
            Gfx.set_font(GameCanvas.font_white)
            Gfx.draw_image(GameCanvas.softkey_bg, 0, GameCanvas.screen_h - m)
            text_w = len(str_ + consts.softkey_labels[left]) * 10
            extra = text_w + 4 - GameCanvas.softkey_bg.getWidth()
            if extra > 0:
                Gfx.fill_rect(j_ - 8, GameCanvas.screen_h - m + 2, 8, 13, 0)
                Gfx.draw_image(GameCanvas.softkey_bg, extra, GameCanvas.screen_h - m)
                Gfx.fill_rect(extra, GameCanvas.screen_h - m + 2, 8, 13, 0)
                Gfx.draw_string(str_ + consts.softkey_labels[left], (j_ + extra) // 2, GameCanvas.screen_h - m, 1)
            else:
                Gfx.draw_string(str_ + consts.softkey_labels[left], j_ // 2, GameCanvas.screen_h - m, 1)
        if right != -1:
            Gfx.set_font(GameCanvas.font_white)
            Gfx.draw_image(GameCanvas.softkey_bg, GameCanvas.screen_w - j_ - 0, GameCanvas.screen_h - m)
            text_w = len(str_ + consts.softkey_labels[right]) * 10
            extra = text_w + 15 - GameCanvas.softkey_bg.getWidth()
            if extra > 0:
                Gfx.fill_rect(GameCanvas.screen_w - j_ - 0, GameCanvas.screen_h - m + 2, 8, 13, 0)
                Gfx.draw_image(GameCanvas.softkey_bg, GameCanvas.screen_w - j_ - extra - 0, GameCanvas.screen_h - m)
                Gfx.fill_rect(GameCanvas.screen_w - extra - 0 - 8, GameCanvas.screen_h - m + 2, 8, 13, 0)
                Gfx.draw_string(str_ + consts.softkey_labels[right], GameCanvas.screen_w - (j_ + extra) // 2 - 0, GameCanvas.screen_h - m, 1)
                return
            Gfx.draw_string(str_ + consts.softkey_labels[right], GameCanvas.screen_w - j_ // 2 - 0, GameCanvas.screen_h - m, 1)

    def set_color(self, r, g, b):  # ag.java:3201-3203
        GameCanvas.fill_color = GameCanvas.rgb(r, g, b)

    @staticmethod
    def draw_line(x1, y1, x2, y2):  # ag.java:3205-3207
        Gfx.draw_line(x1, y1, x2, y2, GameCanvas.fill_color)

    def load_hero_images(self):  # ag.java:3459-3465
        GameCanvas.free_hero_images()
        GameCanvas.hero.head_image = self.load_image(GameCanvas.scr_char.get(46 + GameCanvas.hero.head))
        GameCanvas.hero.head_frames = self.load_frames(47 + GameCanvas.hero.head)
        GameCanvas.hero.body_image = self.load_image(GameCanvas.scr_char.get(44))
        GameCanvas.hero.body_frames = self.load_frames(45)

    def load_frames(self, index):  # ag.java:3467-3482  (frame table from mdat_QVGA)
        pos = 1
        data = ResReader.read("/" + GameCanvas.scr_maps.get(index))
        n = data[0] & 0xFF
        frames = [None] * n
        for i in range(n):
            frames[i] = SpriteFrame()
            frames[i].src_x = GameCanvas.u16(data[pos], data[pos + 1])
            frames[i].src_y = GameCanvas.u16(data[pos + 2], data[pos + 3])
            frames[i].w = GameCanvas.u16(data[pos + 4], data[pos + 5])
            frames[i].h = GameCanvas.u16(data[pos + 6], data[pos + 7])
            frames[i].ox = GameCanvas.u16(data[pos + 8], data[pos + 9])
            frames[i].oy = GameCanvas.u16(data[pos + 10], data[pos + 11])
            pos += 12
        return frames

    @staticmethod
    def gamestr(index):  # ag.java:3538-3540
        return GameCanvas.scr_gamestr.get(index)

    @staticmethod
    def key_digit(key):  # ag.java:3549-3574  (key code '0'..'9' -> digit, else -1)
        if 48 <= key <= 57:
            return key - 48
        return -1

    @staticmethod
    def add_exp(exp):  # ag.java:3081-3098  (add exp; returns the levels gained)
        exp_table = [0] * 10
        b = 0
        exp += GameCanvas.hero.exp
        while True:
            j = b % 10
            if j == 0:
                exp_table = GameCanvas.menus.load_exp_table()
            j = exp_table[j]
            if exp < j:
                GameCanvas.hero.exp = exp
                return b
            exp -= j
            GameCanvas.hero.level += 1
            GameCanvas.hero.stat_points += 3
            b += 1

    @staticmethod
    def trim_right(text):  # ag.java:3148-3153  (trim trailing spaces; sic: one char left -> "")
        m = len(text) - 1
        while m >= 0 and text[m] == ' ':
            m -= 1
        return "" if m == 0 else text[:m + 1]

    @staticmethod
    def cut_at_control(text):  # ag.java:3155-3160  (up to the first control character)
        b = 0
        while b < len(text) and text[b] >= ' ':
            b += 1
        return "" if b == 0 else text[:b]

    @staticmethod
    def cut_at_space(text):  # ag.java:3162-3167  (up to the first space)
        b = 0
        while b < len(text) and text[b] != ' ':
            b += 1
        return "" if b == 0 else text[:b]

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
    def move_letter_cursor(key):  # ag.java:1775-1792  (name entry: move the cursor over the 2x14 letter grid)
        j_ = key
        if key != -7 and key != -5 and key != 53:
            if key == -1 or key == 50:
                GameCanvas.letter_cursor = (GameCanvas.letter_cursor + 28 - 14) % 28
            elif key == -2 or key == 56:
                GameCanvas.letter_cursor = (GameCanvas.letter_cursor + 28 + 14) % 28
            elif key == -3 or key == 52:
                GameCanvas.letter_cursor = (GameCanvas.letter_cursor + 28 - 1) % 28
            elif key == -4 or key == 54:
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
    def draw_letter_grid(cursor, y):  # ag.java:1794-1819  (letter grid A..Z + OK)
        j_ = GameCanvas.screen_cx - 71
        letters = GameCanvas._F_LETTERS
        Gfx.fill_rect(j_, y, 142, 34, 0)
        Gfx.fill_rect(j_ + 123, y + 18, 19, 15, 255)
        if GameCanvas.frame % 4 < 2:
            if cursor == 26:
                Gfx.fill_rect(j_ + 123, y + 18, 19, 15, 16711680)
            elif F10:
                # DECOMP-FIX F10: `10 * p % 14`, `17 * p / 14` -> `10 * (p % 14)`, `17 * (p / 14)`
                Gfx.fill_rect(j_ + 2 + 10 * (cursor % 14), y + 1 + 17 * (cursor // 14), 10, 15, 16711680)
            else:
                Gfx.fill_rect(j_ + 2 + 10 * cursor % 14, y + 1 + 17 * cursor // 14, 10, 15, 16711680)
        Gfx.set_font(GameCanvas.font_white)
        for b in range(len(letters)):
            if b == 8:
                dx = 1
            elif b == 26:
                dx = 1
            else:
                dx = 0
            row = 17 * (b // 14) if F10 else 17 * b // 14   # DECOMP-FIX F10
            Gfx.draw_string(letters[b], j_ + 3 + b % 14 * 10 + dx, y + row, 0)

    def draw_arrow(self, dir, x, y):  # ag.java:1847-1880  (arrow from ct[17])
        if dir == 0:
            src_x = src_y = 0
            w, h = 10, 16
        elif dir == 1:
            src_x, src_y = 9, 0
            w, h = 10, 16
        elif dir == 2:
            src_x, src_y = 20, 0
            w, h = 16, 10
        elif dir == 3:
            src_x, src_y = 20, 9
            w, h = 16, 10
        else:
            return
        GameCanvas.draw_region(x + GameCanvas.view_x, y + GameCanvas.view_y, w, h, GameCanvas.images[17], src_x, src_y)

    @staticmethod
    def rand_range(lo, hi):  # ag.java:2735-2737
        hi -= 1
        return lo + abs(imod(GameCanvas.rng.nextInt(), abs(hi - lo) + 1))

    def rand(self, hi):  # ag.java:2739-2741
        return GameCanvas.rand_range(0, hi)

    def draw_big_number(self, value, x, y, with_commas):  # ag.java:2810-2834  (number from ct[19])
        if with_commas != 0:
            digits = 0
            m = idiv(value, 10)
            x += 9
            while m > 0:
                m = idiv(m, 10)
                digits += 1
                x += 9
                if digits % 3 == 0:
                    x += 4
        j_ = x
        b = 0
        while True:
            if b % 3 == 0 and b != 0:
                x -= 4
                self.draw_map_region(GameCanvas.images[19], x, y, 5, 14, 100, 0)
            x -= 9
            self.draw_map_region(GameCanvas.images[19], x, y, 10, 14, imod(value, 10) * 10, 0)
            b += 1
            value = idiv(value, 10)
            if value <= 0:
                return j_

    def save_game(self):  # ag.java:2871-2961  (write the save "gamevil_pow_data")
        cz = GameCanvas.hero
        reserved = [0] * 16
        name = cz.name.encode("latin-1")
        if len(GameCanvas.save_buf) < 2000:
            # PORT-EXTRA: a loaded save can be shorter than ag.cF (965 bytes, e.g. tools/shot.py's);
            # the backpack block written after it needs the room of the 2000-byte buffer
            GameCanvas.save_buf = bytearray(GameCanvas.save_buf) + bytearray(2000 - len(GameCanvas.save_buf))
        cF = GameCanvas.save_buf
        for b in range(8):
            if b < len(name):
                cF[2 + b] = name[b]
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
            GameCanvas.write_byte(reserved[b])
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
    def write_long(value):  # ag.java:2963-2973
        for k_ in range(8):
            GameCanvas.save_buf[GameCanvas.save_pos + k_] = value >> (8 * k_) & 0xFF
        GameCanvas.save_pos += 8

    @staticmethod
    def write_int(value):  # ag.java:2975-2981
        GameCanvas.save_buf[GameCanvas.save_pos] = value & 0xFF
        GameCanvas.save_buf[GameCanvas.save_pos + 1] = value >> 8 & 0xFF
        GameCanvas.save_buf[GameCanvas.save_pos + 2] = value >> 16 & 0xFF
        GameCanvas.save_buf[GameCanvas.save_pos + 3] = value >> 24 & 0xFF
        GameCanvas.save_pos += 4

    @staticmethod
    def write_short(value):  # ag.java:2983-2987
        GameCanvas.save_buf[GameCanvas.save_pos] = value & 0xFF
        GameCanvas.save_buf[GameCanvas.save_pos + 1] = value >> 8 & 0xFF
        GameCanvas.save_pos += 2

    @staticmethod
    def write_byte(value):  # ag.java:2989-2992
        GameCanvas.save_buf[GameCanvas.save_pos] = value & 0xFF
        GameCanvas.save_pos += 1

    def write_item(self, item):  # ag.java:2994-3001
        GameCanvas.write_short(item.id)
        GameCanvas.write_short(item.attack)
        GameCanvas.write_short(item.defense)
        GameCanvas.write_short(item.hp)
        GameCanvas.write_short(item.mp)
        GameCanvas.write_byte(item.enchant)

    def draw_rect_outline(self, x, y, w, h, r, g, b):  # ag.java:3140-3146  (rectangle outline)
        self.set_color(r, g, b)
        GameCanvas.draw_line(x, y, x + w - 1, y)
        GameCanvas.draw_line(x, y + 1, x, y + h - 1)
        GameCanvas.draw_line(x + w - 1, y, x + w - 1, y + h - 1)
        GameCanvas.draw_line(x + 1, y + h - 1, x + w - 2, y + h - 1)

    def draw_round_outline(self, x, y, w, h, r, g, b):  # ag.java:3181-3187  (outline, round corners)
        self.set_color(r, g, b)
        GameCanvas.draw_line(x + 1, y, x + w - 2, y)
        GameCanvas.draw_line(x, y + 1, x, y + h - 2)
        GameCanvas.draw_line(x + w - 1, y + 1, x + w - 1, y + h - 2)
        GameCanvas.draw_line(x + 1, y + h - 1, x + w - 2, y + h - 1)

    def draw_selection(self, x, y, w, h, r, g, b):  # ag.java:3189-3199  (selection frame)
        self.draw_round_outline(x, y, w, h, r, g, b)
        self.draw_dot(x + 1, y + 1)
        self.draw_dot(x + w - 2, y + 1)
        self.draw_dot(x + 1, y + h - 2)
        self.draw_dot(x + w - 2, y + h - 2)

    def draw_dot(self, x, y):  # ag.java:3209-3211
        GameCanvas.draw_line(x, y, x + 1, y + 1)

    def start_new_game(self):  # ag.java:3213-3220  (New Game -> difficulty screen 29)
        GameCanvas.menus.enter_submenu()
        GameCanvas.menu[0] = 29
        GameCanvas.menu_count = consts.menu_sizes[GameCanvas.menu[0]]
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

    def give_item(self, item_id, count):  # ag.java:3286-3360  (give an item / potion / gold)
        cz = GameCanvas.hero
        b = 0
        if item_id < 100:
            if count != 0:
                free_slot = -1
                b = 0
                while b < 5:
                    if cz.quick_slots[b].item == item_id:
                        if cz.quick_slots[b].count > 4:
                            return 0
                        break
                    if 0 == cz.quick_slots[b].item and free_slot < 0:
                        free_slot = b
                    b += 1
                if free_slot > -1 and b > 4:
                    b = free_slot
                if b > 4:
                    return 0
            else:
                cz.quick_slots[GameCanvas.effect.slot].count = i16(cz.quick_slots[GameCanvas.effect.slot].count - 1)
                if cz.quick_slots[GameCanvas.effect.slot].count < 1:
                    cz.quick_slots[GameCanvas.effect.slot].item = 0
                return 1
        elif item_id < 10000:
            b = 0
            while b < config.BACKPACK_SIZE and 0 != cz.backpack[b].id:
                b += 1
            if b > config.BACKPACK_SIZE - 1:
                return 0
            cz.backpack[b].id = i16(item_id)
            cz.backpack[b].attack = 0
            cz.backpack[b].defense = 0
            cz.backpack[b].hp = 0
            cz.backpack[b].mp = 0
            cz.backpack[b].enchant = 0
        if item_id < 10000:
            GameCanvas.menus.load_item_def(item_id)
        if item_id < 100:
            cz.quick_slots[b].item = i16(item_id)
            cz.quick_slots[b].count = i16(cz.quick_slots[b].count + 1)
        elif item_id < 300:
            if count != 0:
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
        elif item_id < 500:
            cz.backpack[b].attack = GameCanvas.treasure_def.attack
            cz.backpack[b].defense = i16(GameCanvas.treasure_def.defense)
            cz.backpack[b].hp = GameCanvas.treasure_def.hp
            cz.backpack[b].mp = i16(GameCanvas.treasure_def.mp)
        elif item_id < 10000:
            cz.backpack[b].attack = GameCanvas.rare_def.attack
            cz.backpack[b].defense = i16(GameCanvas.rare_def.defense)
            cz.backpack[b].hp = GameCanvas.rare_def.hp
            cz.backpack[b].mp = i16(GameCanvas.rare_def.mp)
        else:
            cz.gold += item_id - 10000
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
        ids = [0] * 17
        GameCanvas.load_item_tables()
        for b in range(17):
            ids[b] = 101 + 5 * GameCanvas.rand_range(0, 20) + GameCanvas.item_tier(GameCanvas.rand_range(0, 100))
        for b in range(16, 0, -1):
            bool_ = False
            for i in range(b):
                if ids[i] > ids[i + 1]:
                    j_ = ids[i]
                    ids[i] = ids[i + 1]
                    ids[i + 1] = j_
                    bool_ = True
            if not bool_:
                break
        for b in range(17):
            GameCanvas.shop[8 + b] = self.make_item(ids[b])

    @staticmethod
    def load_item_tables():  # ag.java:3400-3412
        files = [47, 51, 49]
        if not GameCanvas.tables_loaded[1]:
            for b in range(3):
                if GameCanvas.item_tables[b] is None:
                    GameCanvas.item_tables[b] = ArrTable("/" + GameCanvas.scr_data.get(files[b]))
                if GameCanvas.item_tables[b] is None:
                    return False
            GameCanvas.tables_loaded[1] = True
        return True

    @staticmethod
    def item_tier(roll):  # ag.java:3414-3422  (item tier by hero level)
        m = 0
        b = 0
        while b < 5 and GameCanvas.hero.level >= consts.tier_levels[b]:
            b += 1
        j_ = consts.tier_drop_odds[b - 1]
        b = 0
        while b < 4:
            m += j_ & 0xFF
            if not roll >= m:
                break
            j_ >>= 8
            b += 1
        return b

    def make_item(self, item_id):  # ag.java:3424-3457  (make item paramInt with random bonus)
        item = Item()
        stats = [0] * 5
        item.id = i16(item_id)
        item.enchant = 0
        if item_id < 300:
            for b in range(3):
                stats[b] = GameCanvas.item_tables[0].get_int(item_id - 101, 2 + b)
            if stats[0] == 0:
                item.attack = i16(stats[1] + self.rand(stats[2]))
            elif stats[0] == 1:
                item.defense = i16(stats[1] + self.rand(stats[2]))
            elif stats[0] == 2:
                item.hp = i16(stats[1] + self.rand(stats[2]))
            elif stats[0] == 3:
                item.mp = i16(stats[1] + self.rand(stats[2]))
        else:
            tbl = GameCanvas.item_tables[1] if item_id < 500 else GameCanvas.item_tables[2]
            # ORIG-BUG B1: the original reads both tables at id - 301, so a Rare item (shinki.arr,
            # ids 501-518) gets row 200+ -> all 0; its own row is id - 501
            first = 501 if item_id >= 500 and config.ORIG_BUG["B1"] else 301
            for b in range(4):
                stats[b] = tbl.get_int(item_id - first, 2 + b)
            item.attack = i16(stats[0])
            item.defense = i16(stats[1])
            item.hp = i16(stats[2])
            item.mp = i16(stats[3])
        return item

    def start_story(self, story, ending):  # ag.java:3488-3528  (start the story player, bV = 10)
        GameCanvas.story_id = i16(story)
        if story < 100:
            GameCanvas.story_ending = 0
            b = 64 + story // 6
            for i in range(3):
                GameCanvas.story_pages[i] = consts.story_offsets[(story << 1) + i] - consts.story_offsets[story // 6 * 12]
            if story == 3 and ending != 0 and 0 == GameCanvas.backpack_slot_of(502):
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
    def backpack_slot_of(item_id):  # ag.java:3530-3536  (inventory slot of item, 1-based; 0 = none)
        for b in range(config.BACKPACK_SIZE):
            if GameCanvas.hero.backpack[b].id == item_id:
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

    def fill_screen_rgb(self, r, g, b):  # ag.java:1694-1696  (fill the screen)
        Gfx.fill_rect(0, 0, GameCanvas.canvas_size.x, GameCanvas.canvas_size.y, GameCanvas.rgb(r, g, b))

    def draw_story(self):  # ag.java:1698-1737  (story picture + scrolling text)
        self.fill_screen_rgb(0, 0, 0)
        picture = GameCanvas.images[35]
        if GameCanvas.speech_line in (0, 2):
            if 0 < GameCanvas.story_fade < 4:
                self.draw_map_region(picture, GameCanvas.view_cx - (picture.getWidth() >> 1), GameCanvas.view_cy - (picture.getHeight() >> 1),
                               picture.getWidth(), picture.getHeight(), 0, 0)
        elif GameCanvas.speech_line == 1:
            m = GameCanvas.speech_pos[0]
            if GameCanvas.story_page != GameCanvas.story_pages[2] - GameCanvas.story_pages[0]:
                self.draw_map_region(picture, GameCanvas.view_cx - (picture.getWidth() >> 1), GameCanvas.view_cy - (picture.getHeight() >> 1),
                               picture.getWidth(), picture.getHeight(), 0, 0)
            j_ = GameCanvas.speech_done[0]
            while j_ <= GameCanvas.text_line_count[0] and m <= 230:
                # char arithmetic, as decompiled: `255 - (m - de + 72 << 4)` (only ==255 / ==0 matter)
                if m > GameCanvas.view_cy + 72:
                    alpha = 255 - (m - GameCanvas.view_cy + 72 << 4) & 0xFFFF
                elif m < GameCanvas.view_cy - 72:
                    alpha = 255 - (GameCanvas.view_cy - 72 - m << 4) & 0xFFFF
                else:
                    alpha = 255
                Gfx.set_font(GameCanvas.font_black)
                self.draw_text_at(GameCanvas.text_lines[0][j_], m + 1, 30)
                GameCanvas.draw_text_centred_at(GameCanvas.text_lines[0][j_], m - 1, 1)
                if alpha == 255:
                    Gfx.set_font(GameCanvas.font_white)
                elif alpha == 0:
                    Gfx.set_font(GameCanvas.font_black)
                else:
                    Gfx.set_font(GameCanvas.font_gray)
                self.draw_text_at(GameCanvas.text_lines[0][j_], m, 30)
                m += 22
                j_ += 1
        self.draw_skip_key(2)

    def draw_skip_key(self, unused):  # ag.java:1739-1741  (soft key "Skip")
        GameCanvas.draw_softkeys(0, -1)

    @staticmethod
    def char_width(ch):  # ag.java:3021-3024  (width of a character)
        return GameCanvas.font_white.char_width(chr(ch & 0xFFFF))

    def word_wrap(self, text, width, slot):  # ag.java:3100-3138  (word wrap into dp[paramInt2])
        m = 0
        break_at = 0
        line_w = 0
        b = 0
        GameCanvas.text_line_count[slot] = 0
        dp = GameCanvas.text_lines[slot] = [None] * 120
        n_ = len(text)
        j_ = 0
        while j_ <= n_:
            if j_ != n_:
                c = text[j_]
                line_w += GameCanvas.char_width(c)
                if (c == 32 or c == 124) and line_w - GameCanvas.char_width(c) >= width:
                    if break_at < m:
                        break_at = j_
                    dp[b] = GameCanvas.read_utf(text, m, break_at)
                    b += 1
                    m = break_at + 1
                    j_ = m - 1
                    line_w = 0
                elif c == 32:
                    break_at = j_
                elif c == 124:
                    dp[b] = GameCanvas.read_utf(text, m, j_)
                    b += 1
                    m = break_at = j_ + 1
                    line_w = 0
            elif line_w > width:
                dp[b] = GameCanvas.read_utf(text, m, break_at)
                b += 1
                dp[b] = GameCanvas.read_utf(text, break_at + 1, j_)
                b += 1
            elif break_at != n_ - 1:
                dp[b] = GameCanvas.read_utf(text, m, j_)
                b += 1
            j_ += 1
        if b >= 1:
            GameCanvas.text_line_count[slot] = i8(b - 1)
        return 1

    @staticmethod
    def parse_int(chars):  # ag.java:3542-3547  (Integer.parseInt of the leading digits)
        str_ = ""
        b = 0
        while b < len(chars) and '0' <= chars[b] <= '9':
            str_ = str_ + chars[b]
            b += 1
        return int(str_)

    # ---- menus: Options / Help / Endings helpers -------------------------------------------

    def edat_bytes(self, file, index):  # ag.java:1743-1745
        return GameCanvas.edat_string(file, index).encode("latin-1")

    @staticmethod
    def edat_string(file, index):  # ag.java:1747-1753  (string paramInt2 of edat file paramInt1)
        table = ScrTable("/" + GameCanvas.scr_data.get(file))
        str_ = table.get(index)
        table.free()
        return str_

    def draw_small_number(self, value, x, y):  # ag.java:1828-1830  (small number, ct[20])
        self.draw_image_part(value, x, y, 9, 12, GameCanvas.images[20], 0, 0, 0)

    def draw_image_part(self, value, x, y, w, h, image,
                    src_x, src_y, gap):  # ag.java:1832-1845  (number from a digit strip)
        if value < 0 or image is None:
            return
        x -= w
        if value > 0:
            while value > 0:
                # DECOMP-FIX F10: `p6 + p4 * p1 % 10` -> `p6 + p4 * (p1 % 10)`
                sx = src_x + w * (value % 10) if F10 else src_x + w * value % 10
                GameCanvas.draw_region(x, y, w, h, image, sx, src_y)
                value //= 10
                x -= w + gap
            return
        GameCanvas.draw_region(x, y, w, h, image, src_x, src_y)

    def draw_empty_slot(self, x, y):  # ag.java:3169-3173  (empty 30x30 item slot)
        rect = Rect(x + 1, y + 1, 28, 28)
        self.draw_round_outline(x, y, 30, 30, 80, 80, 80)
        Gfx.fill_rect(rect.x, rect.y, rect.w, rect.h, 0)

    def draw_grey_frame(self, x, y, w, h):  # ag.java:3175-3179  (grey frame, black inside)
        rect = Rect(x + 1, y + 1, w - 2, h - 2)
        self.draw_round_outline(x, y, w, h, 152, 152, 152)
        Gfx.fill_rect(rect.x, rect.y, rect.w, rect.h, 0)

    def change_option(self, step):  # ag.java:2474-2520  (Options: change the value of row cM[1])
        v = GameCanvas.menu[1]
        if v == 0:
            GameCanvas.sound_on = not GameCanvas.sound_on
            if GameCanvas.sound_on:
                self.play_sound(8)
            else:
                GameCanvas.stop_sound()
        elif v == 1:
            if step == 1:
                GameCanvas.volume = i16(GameCanvas.volume + 25)
                if GameCanvas.volume > 100:
                    GameCanvas.volume = 0
            elif step == 0:
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
            if step != 0:
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
    def item_slot_type(item_id):  # ag.java:867-870  (equipment slot type of an item)
        GameCanvas.menus.load_item_def(item_id)
        if item_id < 100:
            return 1
        if item_id < 300:
            return i8(GameCanvas.gear_def.slot)
        if item_id < 500:
            return GameCanvas.treasure_def.slot
        return GameCanvas.rare_def.slot

    @staticmethod
    def describe_shop_item(item, with_name, price):  # ag.java:1454-1457  (item description in the shop)
        # dF.a() (ak.java:10-17) - the method is shadowed by the field ak.a in Python
        dF = GameCanvas.info_box
        dF.shown = 0
        dF.rect.x = dF.rect.y = dF.rect.w = dF.rect.h = 0
        dF.text = ""
        GameCanvas.menus.draw_shop_description(item, 0, 0, 200, 22, price, with_name)

    @staticmethod
    def quick_slot_item(slot):  # ag.java:1459-1465  (potion slot -> item)
        item = Item()
        Item.clear(item)
        item.id = slot.item
        item.attack = slot.count
        return item

    def item_under_cursor(self, index):  # ag.java:1467-1492  (item under the cursor of the item grid)
        item = Item()
        if index == -1:
            index = GameCanvas.cursor[18]
        v = GameCanvas.cursor[0]
        if v == 0:
            item = GameCanvas.shop[index]
        elif v == 1:
            if index < 5:
                item = GameCanvas.quick_slot_item(GameCanvas.hero.quick_slots[index])
            else:
                item = GameCanvas.hero.backpack[index - 5]
        elif v in (2, 3):
            if GameCanvas.cursor[27] == 0:
                item = GameCanvas.hero.backpack[index]
            else:
                item = GameCanvas.hero.equipped[index]
        return item

    @staticmethod
    def fill_rect(rect, color):  # ag.java:1507-1510  (fill rect)
        if rect is not None:
            Gfx.fill_rect(rect.x, rect.y, rect.w, rect.h, color)

    @staticmethod
    def outline_rect(rect, color):  # ag.java:1512-1515  (outline rect)
        if rect is not None:
            Gfx.draw_rect(rect.x, rect.y, rect.w, rect.h, color)

    @staticmethod
    def draw_filled_rect(rect, outline, fill):  # ag.java:1517-1520
        Gfx.fill_rect(rect.x, rect.y, rect.w, rect.h, fill)
        Gfx.draw_rect(rect.x, rect.y, rect.w, rect.h, outline)

    @staticmethod
    def digit_count(value):  # ag.java:1822-1826  (number of digits)
        powers = [10, 100, 1000, 10000]
        b = 0
        while b < 4 and value >= powers[b]:
            b += 1
        return b + 1

    @staticmethod
    def measure_text(text):  # ag.java:1755-1757  (text width)
        return GameCanvas.font_white.string_width(text)

    def draw_small_digit(self, x, y, digit):  # ag.java:1823-1825  (small digit from ct[20])
        self.draw_map_region(GameCanvas.images[20], x, y, 9, 12, digit * 9, 0)

    def draw_gold_box(self):  # ag.java:1279-1291  (gold box)
        widths = [7, 14, 21, 32, 39, 46, 57, 64, 71, 82]
        j_ = GameCanvas.hero.gold
        self.draw_box(GameCanvas.view_cx - 70, GameCanvas.view_cy - 80 + GameCanvas.view_y, 140, 22, False)
        b = 0
        while b < 9:
            j_ = idiv(j_, 10)
            if 0 == j_:
                break
            b += 1
        self.draw_big_number(GameCanvas.hero.gold, GameCanvas.view_cx + (widths[b] >> 1) + 16 - GameCanvas.view_x, GameCanvas.view_cy - 76, 0)
        self.draw_map_region(GameCanvas.images[32], GameCanvas.view_cx - 69 - GameCanvas.view_x, GameCanvas.view_cy - 80, GameCanvas.images[32].getWidth(), GameCanvas.images[32].getHeight(), 0, 0)

    def draw_description(self, what, x, y, w, h):  # ag.java:1293-1352  (description of item / skill)
        cz = GameCanvas.hero
        dF = GameCanvas.info_box
        attack = defense = hp = mp = enchant = min_level = 0
        str_ = ""
        dF.rect.x = x
        dF.rect.y = y
        dF.rect.w = w
        dF.rect.h = h
        dF.text = ""
        if what > 999:
            if what < 1100:
                it = cz.equipped[what - 1000]
            elif what < 1200:
                it = cz.backpack[what - 1100]
            else:
                it = None
            if it is not None:
                min_level = GameCanvas.set_item_name(it.id)
                attack = it.attack
                defense = it.defense
                hp = it.hp
                mp = it.mp
                enchant = i16(it.enchant)
                str_ = GameCanvas.special_suffix(it.id)
            elif what < 2000:
                dF.text = GameCanvas.describe_potion(cz.quick_slots[what - 1200].item)
            else:
                dF.text = self.describe_skill(what - 2000)
        if dF.text != "":
            if str_ != "":
                dF.text += str_
            if attack != 0:
                dF.text += " / ATK+" + str(attack)
            if defense != 0:
                dF.text += " / DEF+" + str(defense)
            if hp != 0:
                dF.text += " / HP+" + str(hp)
            if mp != 0:
                dF.text += " / MP+" + str(mp)
            if enchant != 0:
                dF.text += " / Enchanted Lv" + str(enchant)
            if min_level != 0:
                dF.text += " / Available at Lv" + str(min_level)
            GameCanvas.text_width = GameCanvas.measure_text(dF.text)
            if GameCanvas.text_width > w - 2:
                dF.shown = 1
                dF.text_x = i16(x + 20)
                return
            dF.shown = 0
            dF.text_x = i16(x + 1)

    def describe_skill(self, skill):  # ag.java:1354-1368  (skill description)
        text = ""
        skill -= 12
        if skill < 0 or skill > 18:
            return text
        utf = self.edat_bytes(54, skill)
        name = GameCanvas.read_utf(utf, 0, len(utf))
        if GameCanvas.hero.skill_levels[skill] != 0:
            utf = self.edat_bytes(54, skill + 19)
            text = name + " / Lv" + str(GameCanvas.hero.skill_levels[skill]) + " " + GameCanvas.read_utf(utf, 0, len(utf))
        else:
            text = name + " / (Not Available)"
        return text

    @staticmethod
    def describe_potion(potion):  # ag.java:1370-1381  (potion description)
        str_ = ""
        potion -= 1
        if potion < 0 or potion > 10:
            return str_
        if potion < 9:
            str_ = (consts.potion_names[potion] + " / Recover " + str(consts.potion_percents[potion % 3]) + "% of total "
                    + consts.potion_kinds[potion // 3])
        else:
            utf = GameCanvas.edat_string(54, 24 + potion).encode("latin-1")
            str_ = consts.potion_names[potion] + " / " + GameCanvas.read_utf(utf, 0, len(utf))
        return str_

    @staticmethod
    def special_suffix(item_id):  # ag.java:1383-1399  (special item suffix)
        return {434: " / Hp 5 Increased", 435: " / MP 3 Increased", 436: " / DEF 1 Increased",
                437: " / ATK 1 Increased", 502: " / Catherine's scarf",
                504: " / all General Visiting"}.get(item_id, "")

    @staticmethod
    def set_item_name(item_id):  # ag.java:1401-1416  (item name -> dF.c, returns the level needed)
        GameCanvas.menus.load_item_def(item_id)
        if item_id > 500:
            GameCanvas.info_box.text = GameCanvas.rare_def.name
            return GameCanvas.rare_def.level
        if item_id > 300:
            GameCanvas.info_box.text = GameCanvas.treasure_def.name
            return GameCanvas.treasure_def.level
        if item_id > 100:
            GameCanvas.info_box.text = GameCanvas.gear_def.name
            return consts.tier_req_level[item_id % 5]
        return 0

    # ---- Blacksmith helpers ----------------------------------------------------------------

    def draw_panel(self, x, y, w, h):  # ag.java:1246-1248
        GameCanvas.draw_frame_box(x + 1, y + 1, w - 2, h - 2, 0, 0, 10000536, True)

    def draw_centred_box(self, y, w, h):  # ag.java:1250-1254  (centred box, returns its x)
        j_ = 240 - w >> 1
        self.draw_panel(j_, y, w, h)
        return j_

    def draw_gold_amount(self, gold, y):  # ag.java:1256-1269  (gold box with amount paramInt1)
        j_ = self.draw_centred_box(y, 200, 22)
        b = 0
        rest = gold
        while True:
            b += 1
            rest = idiv(rest, 10)
            if not rest > 0:
                break
        j_ += 100
        m = b * 7 + (b - 1) // 3 * 4 + 12 + 3
        j_ -= m >> 1
        y += 6
        self.draw_number_commas(gold, j_ + m + 10, y)
        self.draw_map_region(GameCanvas.images[32], GameCanvas.view_cx - 69, y - 5, GameCanvas.images[32].getWidth(), GameCanvas.images[32].getHeight(), 0, 0)

    def draw_hero_gold(self, y):  # ag.java:1271-1273
        self.draw_gold_amount(GameCanvas.hero.gold, y)

    def draw_number_commas(self, value, x, y):  # ag.java:2797-2808  (number with thousands commas)
        # DECOMP-FIX F12: the decompiled loop `do { if (!b || b % 3 != 0) continue; ... ++b; }`
        # skips every digit (the number is never drawn). Restored: comma before every 3rd digit.
        b = 0
        while True:
            if F12:
                if b != 0 and b % 3 == 0:
                    x -= 4
                    GameCanvas.draw_region(x, y, 5, 14, GameCanvas.images[19], 100, 0)
                x -= 10
                GameCanvas.draw_region(x, y, 10, 14, GameCanvas.images[19], imod(value, 10) * 10, 0)
                b += 1
            value = idiv(value, 10)
            if not value > 0:
                break

    @staticmethod
    def format_thousands(value):  # ag.java:1437-1452  (12345 -> "12,345")
        str_ = str(value)
        j_ = len(str_)
        digits = [0] * j_
        for i in range(j_):
            digits[j_ - i - 1] = imod(value, 10)
            value = idiv(value, 10)
        str_ = ""
        for j in range(j_):
            str_ = str_ + str(digits[j])
            if j_ % 3 == (j + 1) % 3 and j != j_ - 1:
                str_ = str_ + ","
        return str_

    # ---- Missions: lords, mission list, briefing text, general data ------------------------

    @staticmethod
    def u8(value):  # ag.java:3484-3486
        return i16(value & 0xFF)

    def load_chapter_lords(self):  # ag.java:1043-1062  (lords of chapter cq -> ds/dt/du/dv, list dE = dt)
        j_ = 0
        data = GameCanvas.load_data_file(48)
        j_ = 38 * GameCanvas.chapter + 40
        GameCanvas.lord_count = 0
        for b in range(6):
            GameCanvas.lord_ids[b] = i8(data[j_ + b])
            if GameCanvas.lord_ids[b] > 0:
                m = 38 * GameCanvas.lord_ids[b] + 10
                name_len = 0
                while name_len < 30 and data[m + name_len] != 0:
                    name_len += 1
                GameCanvas.lord_names[b] = GameCanvas.read_utf(data, m, m + name_len)
                GameCanvas.lord_missions[b] = i8(data[m + 36])
                GameCanvas.lord_mission_counts[b] = i8(data[m + 37])
                GameCanvas.lord_count += 1
        GameCanvas.menu_count = GameCanvas.lord_count
        GameCanvas.menu_items = GameCanvas.lord_names

    def load_mission_text(self):  # ag.java:1064-1073  (mission description -> dp[0])
        GameCanvas.mission_name = GameCanvas.mission_names[GameCanvas.mission]
        table = GameCanvas.load_data_file(56)
        text = self.table_text(table, GameCanvas.lord_missions[GameCanvas.lord] + GameCanvas.mission)
        b = 0
        while b < len(text) and text[b] != 0:
            b += 1
        line = bytearray(text[:b])
        self.word_wrap(line, 190, 0)

    def table_text(self, table, index):  # ag.java:1075-1124  (text paramInt of a table, "(..)" macros)
        offsets = [0] * 110
        src = bytearray(1500)
        macro = bytearray(1500)
        out = bytearray(1500)
        digits = ['\0'] * 3
        digit_count = 0
        copied = [0, 0]
        pos = [0, 0]
        j_ = table[0] & 0xFF | table[1] << 8 & 0xFF00
        for i in range(j_ + 1):
            offsets[i] = table[2 + i * 2] & 0xFF | table[2 + i * 2 + 1] << 8 & 0xFF00
        _arraycopy(table, offsets[index], src, 0,
                   offsets[index + 1] - offsets[index])
        i = 0
        while i < 3 and 48 <= src[i] <= 57:
            digits[i] = chr(src[i])
            digit_count += 1
            i += 1
        if digit_count != 0:
            pos[0] = digit_count + 1
            copied[0] = digit_count + 1
            m = GameCanvas.parse_int(digits)
            _arraycopy(table, offsets[m], macro, 0, offsets[m + 1] - offsets[m])
        else:
            _arraycopy(src, 0, macro, 0, 1500)
        while macro[pos[1]] != 0:
            if macro[pos[1]] == 40:
                out = GameCanvas.append_bytes(out, macro, copied[1], pos[1])
                copied[1] = pos[1] + 1
                if digit_count != 0:
                    pos[1] = GameCanvas.index_after(macro, pos[1], ')')
                    # DECOMP-FIX F15: the source is `arrayOfInt2[1] = arrayOfInt3[1] = a(.., ')')`
                    # (one call; JD split the dup_x2 into a second search). Literally the second
                    # search skips the next "(..)" and the copy length is negative: every mission
                    # description with a numbered template (Hellgate...) throws in arraycopy.
                    if config.DECOMP_FIX["F15"]:
                        copied[1] = pos[1]
                    else:
                        copied[1] = GameCanvas.index_after(macro, pos[1], ')')
                    pos[0] = GameCanvas.index_after(src, pos[0], '|')
                    out = GameCanvas.append_bytes(out, src, copied[0], pos[0] - 1)
                    copied[0] = pos[0]
                    continue
                pos[1] = GameCanvas.index_after(macro, pos[1], ')')
                out = GameCanvas.append_bytes(out, macro, copied[1], pos[1] - 1)
                copied[1] = pos[1]
                continue
            pos[1] = pos[1] + 1
        out = GameCanvas.append_bytes(out, macro, copied[1], pos[1])
        return out

    @staticmethod
    def append_bytes(dst, src, start, end):  # ag.java:1126-1131  (append at the first 0)
        b = 0
        while b < len(dst) and dst[b] != 0:
            b += 1
        _arraycopy(src, start, dst, b, end - start)
        return dst

    @staticmethod
    def index_after(data, start, ch):  # ag.java:1133-1142  (index after the next paramChar)
        c = ord(ch)
        b = 0
        while data[start + b] != c and data[start + b] != 0:
            if (data[start + b] & 0x80) != 0:
                b += 2
            b += 1
        return start + b + 1

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
        sprites = [56, 57]
        for b in range(len(sprites)):
            if GameCanvas.lords[GameCanvas.mission].tint != 0:
                GameCanvas.enemy_images[b] = None
                GameCanvas.enemy_frames[b] = None
                GameCanvas.enemy_images[b] = GameCanvas.load_recoloured(GameCanvas.scr_char.get(sprites[b]), GameCanvas.lords[GameCanvas.mission].tint)
            else:
                GameCanvas.enemy_images[b] = None
                GameCanvas.enemy_frames[b] = None
                GameCanvas.enemy_images[b] = self.load_image(GameCanvas.scr_char.get(sprites[b]))
            if GameCanvas.enemy_frames[b] is None:
                GameCanvas.enemy_frames[b] = self.load_frames(82 + b)

    _PAL = [[[236, 211, 197], [205, 143, 128], [129, 81, 69], [104, 60, 49], [79, 39, 29]],
            [[226, 205, 178], [196, 179, 152], [180, 142, 122], [135, 111, 47], [93, 73, 49]],
            [[174, 225, 242], [101, 156, 195], [61, 102, 139], [43, 78, 115], [45, 45, 84]],
            [[162, 199, 159], [135, 156, 119], [86, 123, 98], [33, 98, 63], [51, 51, 51]]]

    @staticmethod
    def load_recoloured(name, palette):  # ag.java:990-1023  (PNG with palette 0 replaced by palette paramInt)
        str_ = "/" + name + ".png"
        png = bytearray(ResReader.read(str_))
        if palette == 0:
            return Image.createImage(png, 0, len(png))
        palettes = GameCanvas._PAL
        m = len(png)
        plte = 0
        for j_ in range(0, m - 4 + 1):
            if png[j_] == 80 and png[j_ + 1] == 76 and png[j_ + 2] == 84 and png[j_ + 3] == 69:
                plte = j_
                break
        plte_len = png[plte - 1] & 0xFF | png[plte - 2] << 8 & 0xFF00
        for b in range(5):
            for j_ in range(plte + 4, plte + plte_len - 3 + 1):
                if (png[j_] == palettes[0][b][0] and png[j_ + 1] == palettes[0][b][1]
                        and png[j_ + 2] == palettes[0][b][2]):
                    png[j_] = palettes[palette][b][0]
                    png[j_ + 1] = palettes[palette][b][1]
                    png[j_ + 2] = palettes[palette][b][2]
                    break
        crc = Gfx.crc32(png, plte, plte_len + 4)
        png[plte + plte_len + 4] = crc >> 24 & 0xFF
        png[plte + plte_len + 5] = crc >> 16 & 0xFF
        png[plte + plte_len + 6] = crc >> 8 & 0xFF
        png[plte + plte_len + 7] = crc & 0xFF
        return Image.createImage(png, 0, len(png))

    def load_lord_map(self, full):  # ag.java:1025-1037  (load the map of the current lord, room around the hero)
        from pow.game.map_scene import MapScene
        self.fill_screen_rgb(0, 0, 0)
        map_image = GameCanvas.images[34]
        self.draw_view_region(map_image, GameCanvas.canvas_size.x // 2 - map_image.getWidth() // 2, GameCanvas.canvas_size.y // 2 - map_image.getHeight() // 2,
                       map_image.getWidth(), map_image.getHeight(), 0, 0)
        GameCanvas.redraw = 1
        MapScene.hero_cell()
        GameCanvas.view_tx = idiv(GameCanvas.hero.room_pos[0].x - 1, 7) * 7 + 4 - (GameCanvas.view_tiles.x >> 1)
        GameCanvas.view_ty = idiv(GameCanvas.hero.room_pos[0].y - 1, 7) * 7 + 4 - (GameCanvas.view_tiles.y >> 1)
        GameCanvas.hero.room_pos[1].x = GameCanvas.hero.room_pos[0].x
        GameCanvas.hero.room_pos[1].y = GameCanvas.hero.room_pos[0].y
        GameCanvas.map = GameCanvas.scene.load_map(GameCanvas.map_id)
        GameCanvas.scene.load_rooms(GameCanvas.lord_ids[GameCanvas.lord])
        GameCanvas.scene.draw_tiles(GameCanvas.view_tiles.x, GameCanvas.view_tiles.y, GameCanvas.view_tx, GameCanvas.view_ty, full)

    def load_hud(self):  # ag.java:2271-2275  (HUD frame pieces)
        pieces = [79, 61, 82, 78, 83, 81]
        for b in range(6):
            GameCanvas.hud_frame[b] = self.load_image(GameCanvas.scr_ui.get(pieces[b]))

    def draw_digit(self, digit, x, y):  # ag.java:2793-2795  (one digit of ct[19])
        self.draw_map_region(GameCanvas.images[19], x, y, 10, 14, 10 * digit, 0)

    @staticmethod
    def decimal_digits(value):  # ag.java:2842-2847  (number of decimal digits)
        b = 1
        j_ = 10
        while value >= j_:
            b += 1
            j_ *= 10
        return b

    def draw_clock(self, x, y, secs):  # ag.java:2849-2855  (mission clock mm:ss)
        digit_x = [0, 9, 25, 34]
        digits = [idiv(secs, 600) % 10, idiv(secs, 60) % 10, secs % 60 // 10, secs % 10]
        for b in range(4):
            self.draw_digit(digits[b], x + digit_x[b] + 10, y)
        self.draw_map_region(GameCanvas.images[19], x + 20 + 10, y, 4, 14, 115, 0)

    def free_map_images(self):  # ag.java:2548-2570  (free the map images; `al` would hide the al class)
        GameCanvas.free_hero_images()
        GameCanvas.images[4] = None
        if GameCanvas.tile_images is not None:
            for i in range(len(GameCanvas.tile_images)):
                GameCanvas.tile_images[i] = None
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

    def load_dialogue_line(self, line):  # ag.java:2584-2637  (line paramInt of dialogue file 57+dG -> dp[dR])
        speaker = ""
        offsets = [0] * 60
        parts = [None, None]
        s = GameCanvas.talk_side
        if (GameCanvas.talk_box & 0x1) != 0:
            if GameCanvas.talk_kind == 0:
                speaker = GameCanvas.mission_names[GameCanvas.mission]
            elif GameCanvas.talk_kind in (2, 1):
                if GameCanvas.talk_kind == 2:          # case 2 falls through into case 1
                    if GameCanvas.boss_fight != 0:
                        self.set_general(GameCanvas.lords[GameCanvas.mission].general)
                    else:
                        self.set_general(GameCanvas.cells[GameCanvas.cell].general)
                speaker = GameCanvas.general.name
        else:
            speaker = GameCanvas.hero.name
        data = GameCanvas.load_data_file(57 + GameCanvas.talk_kind)
        j_ = data[0] & 0xFF | data[1] << 8 & 0xFF00
        for i in range(j_ + 1):
            offsets[i] = data[2 + i * 2] & 0xFF | data[2 + i * 2 + 1] << 8 & 0xFF00
        parts[0] = GameCanvas.read_utf(data, offsets[line], offsets[line + 1])
        parts[1] = "[" + speaker + "] "
        GameCanvas.text_width = len(parts[0])
        m = 0
        for i in range(GameCanvas.text_width):
            if parts[0][i] == '&':
                if m != i:
                    # System.arraycopy(String[], m, String, ...) would throw in Java; the game
                    # only prints this marker, so the texts never have '&' after other text
                    GameCanvas.log("=========================check this 96430jfds")
                parts[1] = parts[1] + speaker
                m = i + 1
        clean = ""
        for j in range(len(parts[0])):
            if parts[0][j] != '&':
                clean = clean + parts[0][j]
        parts[0] = clean
        if m < GameCanvas.text_width:
            parts[1] = parts[1] + parts[0]
        self.word_wrap(bytearray(parts[1].encode("utf-8")), 150, s)

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
                GameCanvas.menu_count = consts.menu_sizes[GameCanvas.menu[0]]
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
    def friendship(general):  # ag.java:2683-2687  (friendship points of general paramInt)
        b = 0
        while b < GameCanvas.general_count and GameCanvas.generals[0][b] != general:
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

    def set_general(self, general):  # ag.java:2705-2726  (general paramInt -> dC)
        data = None
        j_ = 0
        data = GameCanvas.load_data_file(46)
        j_ = 23 * (general - 1) + 14
        dC = GameCanvas.general
        dC.name = ""
        b = 0
        while b < 11 and data[j_ + b] != 0:
            b += 1
        dC.name = GameCanvas.read_utf(data, j_, j_ + b)
        dC.look = _jchar(data[j_ + 11])
        dC.side = _jchar(data[j_ + 11 + 2])
        dC.skills[0] = _jchar(data[j_ + 11 + 3])
        dC.skills[1] = _jchar(data[j_ + 11 + 4])
        dC.skills[2] = _jchar(data[j_ + 11 + 5])
        dC.skills[3] = _jchar(data[j_ + 11 + 6])
        dC.portrait = _jchar(data[j_ + 11 + 7])
        dC.gift_table = _jchar(data[j_ + 11 + 8])
        dC.attack = _jchar(data[j_ + 11 + 9])
        dC.defense = _jchar(data[j_ + 11 + 10])
        dC.hp = _jchar(data[j_ + 11 + 11])
        dC.side = dC.side + 1 & 0x1

    def random_general_skill(self, force):  # ag.java:1494-1505  (random skill of general dC)
        b = 0
        while b < 4 and 0 != GameCanvas.general.skills[b]:
            b += 1
        if force != 0:
            while True:
                skill = GameCanvas.general.skills[self.rand(b)]
                if not skill > 0o20:
                    return skill
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
