"""k.java - sound manager (music snd0-2, SFX snd3-16). Literal port."""
from pow.game.game_canvas import GameCanvas
from pow.midp import system
from pow.game.player_pool import PlayerPool


class Sound(GameCanvas):
    players = None     # public static aq a = null;     k.java:2
    requested = -1       # requested sound                k.java:4
    music = -1      # current music                  k.java:6
    last = -1
    last_time = 0
    min_gap = [0] * 17

    def __init__(self, main):  # k.java:14-20
        super().__init__(main)
        for b in range(17):
            Sound.min_gap[b] = 0
        Sound.min_gap[9] = 500
        Sound.players = PlayerPool(17, 1, True, True)

    def play_sound(self, sound):  # k.java:22-33
        if Sound.players is None or not GameCanvas.sound_on:
            return
        l = system.currentTimeMillis() - Sound.last_time
        if Sound.last != -1 and Sound.min_gap[Sound.last] != 0 and l < Sound.min_gap[Sound.last]:
            return
        if sound > 2 and sound != 15 and sound != 16 and sound != 3 and sound != 4:
            Sound.stop_all()
        Sound.requested = sound
        Sound.last = sound
        Sound.last_time = system.currentTimeMillis()

    def tick_sound(self):  # k.java:35-59  (called once per tick from ag.run)
        if Sound.players is None or not GameCanvas.sound_on:
            return
        Sound.players.tick()
        bool1 = False
        bool2 = True
        i = Sound.requested
        Sound.requested = -1
        if GameCanvas.sound_on and i != -1:
            if i <= 2:
                if Sound.music == i:
                    bool2 = False
                else:
                    Sound.stop_all()
                Sound.music = i
                bool1 = True
            else:
                Sound.music = -1
                bool1 = False
            if bool2:
                self.play_now(i, bool1)

    def play_now(self, sound, loop):  # k.java:61-73
        Sound.players.set_volume(GameCanvas.volume)
        if GameCanvas.volume == 0:
            Sound.stop_all()
            return
        if sound <= 2:
            Sound.players.load("/snd" + str(sound) + ".mid", sound)
        else:
            Sound.players.load("/snd" + str(sound) + ".wav", sound)
        Sound.players.play(sound, loop)

    @staticmethod
    def stop_all():  # k.java:75-79
        Sound.requested = -1
        Sound.music = -1
        Sound.players.stop()
