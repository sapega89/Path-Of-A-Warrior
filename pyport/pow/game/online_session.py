"""Asked by the player: the Multiplayer screens (pow/game/online, once the separate game
"Path of a Warrior Multiplayer") as a state of GameCanvas.

Live > Multiplayer calls enter(): the MpCanvas is made, its screens begin (no logo, no
sound question, no title: the single player answered those) and GameCanvas.state becomes
ONLINE. From then on GameCanvas.loop() runs one Multiplayer frame per tick (frame(): what
g.run() / g.c() did, pow/game/online/game.py) instead of its own: the Multiplayer code draws
on the same display and reads the keys itself, as before, only without a loop, an application shell and a
window of its own. Its Exit (BACK in its main menu) ends the frames: leave() closes its
connection, drops its modules (their static fields start clean on the next visit, as when the
phone started the other game), gives the hero what the battles earned (Live.after_multiplayer)
and the game goes on in the Live menu.
"""
import sys

ONLINE = 13             # GameCanvas.state while the Multiplayer screens run (the states of the
                        # single player stop at 12)
PACKAGE = "pow.game.online"


def _fresh():
    """Forget the Multiplayer modules: the next enter() imports them anew."""
    for m in list(sys.modules):
        if m == PACKAGE or m.startswith(PACKAGE + "."):
            del sys.modules[m]


class Session:
    def __init__(self, canvas):
        from pow.game.game_canvas import GameCanvas
        from pow.midp import canvas as midp_canvas
        import pygame
        self.canvas = canvas                          # the GameCanvas
        self.keymap = dict(midp_canvas.KEYMAP)        # the Multiplayer number row types digits
        from pow.game.online import sp_bridge
        from pow.game.online.midlet import Midlet
        from pow.game.online.mp_canvas import MpCanvas
        MpCanvas.sound_from_sp = GameCanvas.sound_on
        MpCanvas.embedded = sp_bridge.embedded = True
        self.midlet = Midlet()                        # loads the classes, makes the MpCanvas
        self.mp = Midlet.canvas
        pygame.display.set_caption("Path of a Warrior Multiplayer")
        self.mp.init_screen()

    async def frame(self):
        """One Multiplayer frame. False when its screens are over (their Exit, or the window)."""
        from pow.game.online import game
        return await game.frame(self.mp, self.midlet)

    def leave(self):
        """Back to the single player: its hero gets the rewards, the Live menu goes on."""
        from pow.game.game_canvas import GameCanvas
        from pow.midp import canvas as midp_canvas
        import pygame
        from pow.game.online import game
        rewards, closed = game.close(self.mp)
        midp_canvas.KEYMAP.clear()
        midp_canvas.KEYMAP.update(self.keymap)
        pygame.display.set_caption("Path of a Warrior")
        _fresh()
        GameCanvas.online = None
        if closed:                                    # the window was closed there
            self.canvas.quit_requested = True
            return
        GameCanvas.state = 11                         # Live, its menu as it was left
        GameCanvas.redraw = 1
        GameCanvas.live.after_multiplayer(rewards)


def enter(canvas):
    """Live > Multiplayer (Live.open_multiplayer)."""
    from pow.game.game_canvas import GameCanvas
    GameCanvas.stop_sound()
    GameCanvas.online = Session(canvas)
    GameCanvas.state = ONLINE
