"""af.java - boot screens: logo -> "sound enabled?" -> title. Literal port."""
from pow.game.game_canvas import GameCanvas
from pow.game.gfx import Gfx
from pow.midp import system


class Boot(GameCanvas):
    step = 0   # public static int b = 0;   af.java:4  (0 logo, 1 sound question, 2 title)
    start_time = 0   # public static long c;      af.java:6

    def __init__(self):  # af.java:2, 8-11
        super().__init__(GameCanvas.midlet)
        self.logo = self.load_image("logo1")    # Image a = d("logo1");   (instance initializer)
        Boot.start_time = system.currentTimeMillis()

    def draw_boot(self):  # af.java:15-36  (paint)
        from pow.game.midlet import Midlet
        if Boot.step == 0 and GameCanvas.midlet.resume_sound is not None:
            self.resume()
            return
        if Boot.step == 0:
            GameCanvas.fill_screen(16777215)
            if self.logo is not None:
                Gfx.draw_image_anchored(self.logo, GameCanvas.screen_cx, GameCanvas.screen_cy, 3)
            if system.currentTimeMillis() - Boot.start_time > 2500:
                self.logo = None
                Boot.step = 1
                GameCanvas.popups.setup_popup(40)
                return
        else:
            if Boot.step == 1:
                GameCanvas.fill_screen(0)
                Gfx.set_font(GameCanvas.font_white)
                GameCanvas.popups.draw_popup()
                return
            if Boot.step == 2:
                Midlet.canvas.draw_title()

    def boot_keys(self):  # af.java:38-64  (keys)
        if Boot.step == 0:
            return
        if Boot.step == 1:
            i = GameCanvas.popups.popup_keys()
            if i != -1:
                self.answer_sound(i == 0)
            return
        if Boot.step == 2 and Boot.is_any_key(GameCanvas.key):
            self.leave_title()

    def answer_sound(self, yes):  # af.java:44-55  (the YES / NO of "sound enabled?")
        GameCanvas.sound_on = yes
        if yes:
            if GameCanvas.volume == 0:
                GameCanvas.volume = 75
        else:
            GameCanvas.volume = 0
        self.play_sound(0)
        Boot.step = 2
        self.load_title_picture()

    def leave_title(self):  # af.java:57-63  (any key on the title -> Main Menu)
        GameCanvas.redraw = 1
        GameCanvas.title_press = None
        GameCanvas.title_logo = None
        GameCanvas.menus.load_title_images()
        self.tick_title()

    def resume(self):
        """PORT-EXTRA: back from the Multiplayer game (main.py) the single player starts again in
        the same process; the logo, the sound question and the title were already seen, so the
        answer given then is used and the game goes straight to the Main Menu."""
        self.logo = None
        self.answer_sound(GameCanvas.midlet.resume_sound)
        self.leave_title()

    @staticmethod
    def is_any_key(key):  # af.java:66-92  ("press any key": which keys count)
        return key in (-10, -8, -7, -6, -5, -4, -3, -2, -1, 35, 42, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57)
