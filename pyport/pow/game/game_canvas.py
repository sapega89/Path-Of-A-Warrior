"""ag.java - the main Canvas class (game loop, state machine, shared helpers).

Method names follow pyport/NAMES.md (signature suffix when the Java name is overloaded).
Every method has a `# ag.java:FROM-TO` comment.
"""
import traceback

import config
from pow.game import canvas_assets, canvas_draw, canvas_items, canvas_save, canvas_story, canvas_text, consts
from pow.game.canvas_assets import AssetsMixin
from pow.game.canvas_draw import DrawMixin
from pow.game.canvas_items import ItemsMixin
from pow.game.canvas_save import SaveMixin
from pow.game.canvas_story import StoryMixin
from pow.game.canvas_text import TextMixin
from pow.game.font import Font
from pow.game.game_fields import GameFields
from pow.game.gfx import Gfx
from pow.game.scr_table import ScrTable
from pow.midp import display, system
from pow.midp.canvas import Canvas
from pow.midp.graphics import Image
from pow.midp.jint import i16, i32, imod

F13 = config.DECOMP_FIX["F13"]


class GameCanvas(SaveMixin, ItemsMixin, TextMixin, DrawMixin, StoryMixin, AssetsMixin, GameFields, Canvas):

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
        from pow.game.live import Live
        from pow.game.live_screen import LiveScreen
        from pow.game.map_engine import MapEngine
        from pow.game.map_scene import MapScene
        from pow.game.menus import Menus
        from pow.game.sound import Sound
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
        GameCanvas.engine = MapEngine()               # ar.java: map engine (movement, combat)
        GameCanvas.scene = MapScene()                # c.java: story player, map scene

    def keyPressed(self, key):  # ag.java:660-662
        self.key_down(key)

    def handle_key(self):  # ag.java:664-685
        if GameCanvas.key == -999:
            return
        if GameCanvas.paused:
            if GameCanvas.key in (-5, 53):
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
            box_y = GameCanvas.view_cy - 5 - 10
            Gfx.draw_string("RESUME", GameCanvas.screen_cx, box_y + GameCanvas.view_y + 7, 1)
            GameCanvas.painted = True
            return
        self.tick_state()
        GameCanvas.draw_auto_badge()
        GameCanvas.painted = True

    async def run(self):  # ag.java:708-760  (Thread.run -> async loop for pygbag)
        self.init_game()
        await self.loop()

    def suspend(self):
        """PORT-EXTRA: leave loop() with everything in memory; main.py runs the Multiplayer
        screens in the same window and then calls loop() again (Gamevil Live > Multiplayer)."""
        GameCanvas.stop_sound()
        GameCanvas.suspended = True
        GameCanvas.running = False

    async def loop(self):  # ag.java:714-760  (the frames; PORT-EXTRA: re-entered after suspend())
        GameCanvas.suspended = False
        GameCanvas.running = True
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
                GameCanvas.frame = max(GameCanvas.frame, 0)
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
                wait_ms = (consts.speed_frame_ms[GameCanvas.speed] if GameCanvas.state == 3 else consts.speed_frame_ms[2]) - int(now - GameCanvas.tick_start)
                if wait_ms > 20:
                    await self.sleep_ms(wait_ms)
                else:
                    await self.sleep_ms(20)
                if GameCanvas.frame > 2:
                    GameCanvas.started = True
                GameCanvas.last_state = GameCanvas.state
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
    def clamp_menu_scroll():  # ag.java:1203-1210
        if GameCanvas.menu[1] < GameCanvas.menu[2]:
            GameCanvas.menu[2] = GameCanvas.menu[1]
            return
        if GameCanvas.menu[1] > GameCanvas.menu[2] + 4:
            GameCanvas.menu[2] = GameCanvas.menu[1] - 4

    def paint_state(self):  # ag.java:1522-1610
        # DECOMP-FIX F8: the decompiled switch at ag.java:1526-1546 has no `break`s, so every case
        # would fall through into the next (bV==0 would also run bb.a(1), bc.b(1), ...).
        # The original had one branch per state.
        if GameCanvas.redraw == 1:
            GameCanvas.redraw = 0
            state = GameCanvas.state
            if state == 0:
                GameCanvas.start_boot()
            elif state == 2:
                GameCanvas.menus.draw_menu(1)
            elif state == 3:
                GameCanvas.engine.draw_map(1)
            elif state == 4:
                GameCanvas.engine.scroll_room()
            elif state == 5:
                self.draw_view_background()
                for b in range(81):
                    GameCanvas.dirty[b // 9][b % 9] = 1
                GameCanvas.scene.draw_frame()
                GameCanvas.menus.draw_map_talk()
            elif state in (6, 8, 9):
                return
            elif state == 10:
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
        state = GameCanvas.state
        if state == 0:
            GameCanvas.start_boot()
            return
        if state == 2:
            GameCanvas.menus.draw_menu(0)
            return
        if state == 3:
            GameCanvas.engine.draw_map(0)
            return
        if state == 4:
            GameCanvas.engine.scroll_room()
            GameCanvas.engine.draw_hud()
            return
        if state == 5:
            GameCanvas.menus.tick_dialogue()
            return
        if state in (6, 8, 9):
            return
        if state == 10:
            if GameCanvas.popups.kind != 0 and GameCanvas.popups.popup_redraw != 0:
                GameCanvas.popups.draw_popup()
                return
            self.tick_story()

    def play_sound(self, sound):  # ag.java:1882-1885
        if GameCanvas.sound is not None:
            GameCanvas.sound.play_sound(sound)

    def tick_state(self):  # ag.java:1887-1933
        from pow.game.sound import Sound
        if display.screen_changed():         # PORT-EXTRA: the browser went full screen / back later
            GameCanvas.redraw = 1            # (Options shows Screen: Full / Window)
        state = GameCanvas.state
        if state == 0:
            self.paint_state()
        elif state == 2:
            if GameCanvas.sound is not None and GameCanvas.menu[0] < 29 and Sound.music != consts.menu_music[GameCanvas.menu[0]] and GameCanvas.menu[0] != 20 and not GameCanvas.in_live:
                self.play_sound(consts.menu_music[GameCanvas.menu[0]])
            if GameCanvas.popups.kind != 0:
                GameCanvas.popups.popup_keys()
            else:
                GameCanvas.menus.menu_keys()
            self.paint_state()
        elif state == 3:
            GameCanvas.engine.tick_map()
        elif state in (4, 5):
            self.paint_state()
            GameCanvas.engine.tick_mission_clock(0)
        elif state == 10:
            if GameCanvas.popups.kind != 0:
                GameCanvas.popups.popup_keys()
            self.paint_state()
        elif state == 11 and GameCanvas.live is not None:
            from pow.game.live import Live
            Live.draw_screen()
        if GameCanvas.live is not None:
            from pow.game.live import Live
            if Live.busy and not Live.quiet_request():   # PORT-EXTRA: live_online.py
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

    def tick_title(self):  # ag.java:2004-2124  (title -> Main Menu)
        hero = GameCanvas.hero
        for b in range(8):
            dir4 = consts.dir8_to_dir4[b]
            hero.anim_0[b] = consts.hero_anim_0[dir4]
            hero.anim_1[b] = consts.hero_anim_1[dir4]
            hero.anim_2[b] = consts.hero_anim_2[dir4]
            hero.anim_9[b] = consts.hero_anim_9[dir4]
            hero.anim_3[b] = consts.hero_anim_3[dir4]
            hero.anim_4[b] = consts.hero_anim_4[dir4]
            hero.anim_5[b] = consts.hero_anim_5[dir4]
            hero.anim_6[b] = consts.hero_anim_6[dir4]
            hero.anim_7[b] = consts.hero_anim_7[dir4]
            hero.anim_8[b] = consts.hero_anim_8[dir4]
            hero.anim_10[b] = consts.hero_anim_10
            hero.anim_11[b] = consts.hero_anim_11[dir4]
            hero.anim_12[b] = consts.hero_anim_12[dir4]
            hero.anim_13[b] = consts.hero_anim_13[dir4]
            hero.anim_14[b] = consts.hero_anim_14[dir4]
            hero.anim_15_19[b] = consts.hero_anim_15_19
            hero.anim_20[b] = consts.hero_anim_20[dir4]
            hero.anim_21[b] = consts.hero_anim_21[dir4]
            hero.anim_22[b] = consts.hero_anim_22[dir4]
            hero.anim_23_24[b] = consts.hero_anim_23_24
            hero.anim_25[b] = consts.hero_anim_25[dir4]
            hero.anim_26_27[b] = consts.hero_anim_26_27[dir4]
            hero.anim_28[b] = consts.hero_anim_28
            hero.anim_29[b] = consts.hero_anim_29
            hero.anim_30[b] = consts.hero_anim_30
            GameCanvas.head_anim[b][0] = consts.head_anim_0[dir4]
            GameCanvas.head_anim[b][1] = consts.head_anim_1[dir4]
            GameCanvas.head_anim[b][2] = consts.head_anim_2[dir4]
            GameCanvas.head_anim[b][3] = consts.head_anim_3[dir4]
            GameCanvas.head_anims[b] = GameCanvas.head_anim[b]
            GameCanvas.body_anim[b][0] = consts.body_anim_0[dir4]
            GameCanvas.body_anim[b][1] = consts.body_anim_1[dir4]
            GameCanvas.body_anim[b][2] = consts.body_anim_2[dir4]
            GameCanvas.body_anim[b][3] = consts.body_anim_3[dir4]
            GameCanvas.body_anims[b] = GameCanvas.body_anim[b]
            GameCanvas.weapon_anim[b][0] = consts.head_anim_0[dir4]
            GameCanvas.weapon_anim[b][1] = consts.weapon_anim_1[dir4]
            GameCanvas.weapon_anim[b][2] = consts.weapon_anim_2[dir4]
            GameCanvas.weapon_anim[b][3] = consts.weapon_anim_3
            GameCanvas.weapon_anim[b][4] = consts.weapon_anim_1[dir4]
            GameCanvas.weapon_anim[b][5] = consts.weapon_anim_1[dir4]
            GameCanvas.weapon_anim[b][6] = consts.hero_anim_12[dir4]
            GameCanvas.weapon_anim[b][7] = consts.hero_anim_13[dir4]
            GameCanvas.weapon_anim[b][8] = consts.hero_anim_14[dir4]
            GameCanvas.weapon_anim[b][9] = consts.hero_anim_15_19
            GameCanvas.weapon_anim[b][10] = consts.hero_anim_15_19
            GameCanvas.weapon_anim[b][11] = consts.hero_anim_15_19
            GameCanvas.weapon_anim[b][12] = consts.hero_anim_15_19
            GameCanvas.weapon_anim[b][13] = consts.hero_anim_15_19
            GameCanvas.weapon_anim[b][14] = consts.hero_anim_20[dir4]
            GameCanvas.weapon_anim[b][15] = consts.hero_anim_21[dir4]
            GameCanvas.weapon_anim[b][16] = consts.hero_anim_22[dir4]
            GameCanvas.weapon_anim[b][17] = consts.hero_anim_23_24
            GameCanvas.weapon_anim[b][18] = consts.hero_anim_23_24
            GameCanvas.weapon_anim[b][19] = consts.hero_anim_25[dir4]
            GameCanvas.weapon_anim[b][20] = consts.hero_anim_26_27[dir4]
            GameCanvas.weapon_anim[b][21] = consts.hero_anim_26_27[dir4]
            GameCanvas.weapon_anims[b] = GameCanvas.weapon_anim[b]
        GameCanvas.char_anims[0] = GameCanvas.head_anims
        GameCanvas.char_anims[1] = GameCanvas.body_anims
        GameCanvas.char_anims[2] = GameCanvas.head_anims
        GameCanvas.char_anims[3] = GameCanvas.weapon_anims
        anims = hero.anims
        (anims[0], anims[1], anims[2], anims[3], anims[4], anims[5], anims[6], anims[7], anims[8], anims[9]) = (
            hero.anim_0, hero.anim_1, hero.anim_2, hero.anim_3, hero.anim_4, hero.anim_5, hero.anim_6, hero.anim_7, hero.anim_8, hero.anim_9)
        (anims[10], anims[11], anims[12], anims[13], anims[14]) = (hero.anim_10, hero.anim_11, hero.anim_12, hero.anim_13, hero.anim_14)
        (anims[15], anims[16], anims[17], anims[18], anims[19]) = (hero.anim_15_19, hero.anim_15_19, hero.anim_15_19, hero.anim_15_19, hero.anim_15_19)
        (anims[20], anims[21], anims[22], anims[23], anims[24]) = (hero.anim_20, hero.anim_21, hero.anim_22, hero.anim_23_24, hero.anim_23_24)
        (anims[25], anims[26], anims[27], anims[28], anims[29], anims[30]) = (hero.anim_25, hero.anim_26_27, hero.anim_26_27, hero.anim_28, hero.anim_29, hero.anim_30)
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

    @staticmethod
    def stop_sound():  # ag.java:2463-2465
        from pow.game.sound import Sound
        Sound.stop_all()

    @staticmethod
    def set_menu_items():  # ag.java:2522-2546
        menu = GameCanvas.menu[0]
        if menu == 0:
            GameCanvas.menu_items = GameCanvas.game_menu_items
        elif menu == 1:
            GameCanvas.menu_count = GameCanvas.lord_count
            GameCanvas.menu_items = GameCanvas.lord_names
        elif menu == 2:
            GameCanvas.menu_count = GameCanvas.lord_mission_counts[GameCanvas.lord]
            GameCanvas.menu_items = GameCanvas.mission_names
        elif menu == 7:
            GameCanvas.hero.name = None
        elif menu == 10:
            GameCanvas.menu_items = GameCanvas.yes_no_items
        elif menu == 13:
            GameCanvas.menu_items = GameCanvas.continue_items
            GameCanvas.images[39] = None

    @staticmethod
    def restore_menu_cursor():  # ag.java:2728-2733
        GameCanvas.menu_count = consts.menu_sizes[GameCanvas.menu[0]]
        GameCanvas.menu[1] = GameCanvas.menu_cursors[GameCanvas.menu[0]]
        GameCanvas.menu[2] = GameCanvas.menu_tops[GameCanvas.menu[0]]
        GameCanvas.redraw = 1

    def start_exit(self):  # ag.java:3003-3009  (exit)
        # PORT-EXTRA (asked by the player): no outro picture (state 12, ag.java:3011-3019, 3 s):
        # the game closes at once
        GameCanvas.stop_sound()
        GameCanvas.midlet.destroyApp(True)
        GameCanvas.midlet.notifyDestroyed()

    # ---- New Game: hero creation (screens 29 / 6 / 7 / 8) and the save writer ------------

    @staticmethod
    def now():  # ag.java:1039-1041
        return system.currentTimeMillis()

    @staticmethod
    def move_letter_cursor(key):  # ag.java:1775-1792  (name entry: move the cursor over the 2x14 letter grid)
        result = key
        if key not in (-7, -5, 53):
            if key in (-1, 50):
                GameCanvas.letter_cursor = (GameCanvas.letter_cursor + 28 - 14) % 28
            elif key in (-2, 56):
                GameCanvas.letter_cursor = (GameCanvas.letter_cursor + 28 + 14) % 28
            elif key in (-3, 52):
                GameCanvas.letter_cursor = (GameCanvas.letter_cursor + 28 - 1) % 28
            elif key in (-4, 54):
                GameCanvas.letter_cursor = (GameCanvas.letter_cursor + 28 + 1) % 28
                if GameCanvas.letter_cursor == 27:
                    GameCanvas.letter_cursor = 0
        if GameCanvas.letter_cursor == 27:
            GameCanvas.letter_cursor = 26
        return result

    @staticmethod
    def rand_range(lo, hi):  # ag.java:2735-2737
        hi -= 1
        return lo + abs(imod(GameCanvas.rng.nextInt(), abs(hi - lo) + 1))

    def rand(self, hi):  # ag.java:2739-2741
        return GameCanvas.rand_range(0, hi)

    def start_new_game(self):  # ag.java:3213-3220  (New Game -> difficulty screen 29)
        GameCanvas.menus.enter_submenu()
        GameCanvas.menu[0] = 29
        GameCanvas.menu_count = consts.menu_sizes[GameCanvas.menu[0]]
        GameCanvas.menu[1] = 1
        GameCanvas.hero.head = 0
        self.new_hero()

    def change_option(self, step):  # ag.java:2474-2520  (Options: change the value of row cM[1])
        row = GameCanvas.menu[1]
        if row == 0:
            GameCanvas.sound_on = not GameCanvas.sound_on
            if GameCanvas.sound_on:
                self.play_sound(8)
            else:
                GameCanvas.stop_sound()
        elif row == 1:
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
        elif row == 2:
            if step != 0:
                GameCanvas.speed = i16(GameCanvas.speed + 1)
                if GameCanvas.speed > 4:
                    GameCanvas.speed = 0
            else:
                GameCanvas.speed = i16(GameCanvas.speed - 1)
                if GameCanvas.speed < 0:
                    GameCanvas.speed = 4
        elif row == 3 and config.SCREEN_OPTION:      # PORT-EXTRA: Screen = full screen / window
            display.toggle_fullscreen()
            return
        GameCanvas.save_options()

    def enter_map(self):  # ag.java:872-967  (enter the map: bV = 3)
        hero = GameCanvas.hero
        hero.weapon_kind = GameCanvas.item_slot_type(hero.equipped[0].id)
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
            if F13 and hero.pos[1] is not hero.pos[0]:
                # DECOMP-FIX F13: the start position is written into cz.a[1], but the map
                # (c.f(), c.a(5 ints)) reads cz.a[0]. Both are the same object once ar.aC()
                # (cz.a[1] = cz.a[0]) has run; on the first map after start-up they are not,
                # and the hero would stand at (0, 0).
                hero.pos[1] = hero.pos[0]
            hero.pos[1].x = i16(GameCanvas.lords[GameCanvas.mission].start_x * 27 + 12)
            hero.pos[1].y = i16(GameCanvas.lords[GameCanvas.mission].start_y * 27 + 20)
            GameCanvas.rooms_visited = 1
            GameCanvas.mission_exp = 0
            bool_ = 0
        hero.dir[1] = hero.facing = 0
        hero.dir[0] = hero.facing = 0
        hero.action[1] = 0
        hero.action[0] = 0
        hero.frame[1] = 0
        hero.frame[0] = 0
        hero.hit_fx_kind = 0
        hero.idle_ticks = 20
        hero.sprite_frame = 0
        hero.on_fire = 0
        hero.kills = 0
        hero.kills_shown = 0
        hero.attack_buff = 0
        hero.defense_buff = 0
        hero.attack_buff_ticks = 0
        hero.defense_buff_ticks = 0
        hero.hurt_ticks = 0
        GameCanvas.update_hero_stats()
        if GameCanvas.cheat:
            hero.gold = 500000
            hero.max_hp = hero.hp = hero.base_hp = hero.base_attack = hero.attack = hero.base_defense = hero.defense = hero.max_mp = hero.mp = hero.base_mp = 2000
        GameCanvas.hero_fx_kind = 0
        GameCanvas.hero_fx_count = 1
        GameCanvas.map_mode.mode = 0
        GameCanvas.message.shown = 0
        GameCanvas.effect.item = 0
        GameCanvas.hero_picked_up = 0
        GameCanvas.boss_spawned = 0
        GameCanvas.hero_fx_data = None
        GameCanvas.enemy_fx_data = None
        if config.ORIG_BUG["B8"]:
            GameCanvas.enemy_fx_kind = 0   # ORIG-BUG B8: reset like hero_fx_kind above, or a general's effect outlives its data
        GameCanvas.fire_data = None
        for b in range(2):
            if GameCanvas.enemy_frames[b] is None:
                GameCanvas.enemy_frames[b] = self.load_frames(82 + b)
        self.load_lord_map(bool_)
        self.load_enemy_sprites()
        GameCanvas.hero_weapon_frames[hero.weapon_kind] = self.load_frames(87 + (hero.weapon_kind << 2))
        hero.head_frames2 = self.load_frames(51 + hero.head)
        hero.body_frames2 = self.load_frames(46)
        GameCanvas.hero_body_frames[hero.weapon_kind] = self.load_frames(89 + (hero.weapon_kind << 2))
        GameCanvas.images[40 + hero.weapon_kind] = self.load_image(GameCanvas.scr_char.get(42 + hero.weapon_kind))
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


def _late_init():
    """Static initialisers that create ag subclasses (ag.java:206  `cS = new l()`)."""
    from pow.game.popups import Popups
    GameCanvas.popups = Popups()


for _part in (canvas_save, canvas_items, canvas_text, canvas_draw, canvas_story, canvas_assets):
    _part.GameCanvas = GameCanvas
