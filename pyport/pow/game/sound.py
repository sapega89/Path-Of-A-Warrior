"""Sound manager (music snd0-2, SFX snd3-16)."""
from pow.game.game_canvas import GameCanvas
from pow.game.player_pool import PlayerPool
from pow.midp import system


class Sound(GameCanvas):
    players = None
    requested = -1       # requested sound
    music = -1      # current music
    last = -1
    last_time = 0
    min_gap = [0] * 17

    def __init__(self, main):
        super().__init__(main)
        for b in range(17):
            Sound.min_gap[b] = 0
        Sound.min_gap[9] = 500
        Sound.players = PlayerPool(17, 1, True, True)

    def play_sound(self, sound):
        if Sound.players is None or not GameCanvas.sound_on:
            return
        since = system.currentTimeMillis() - Sound.last_time
        if Sound.last != -1 and Sound.min_gap[Sound.last] != 0 and since < Sound.min_gap[Sound.last]:
            return
        if sound > 2 and sound not in {15, 16, 3, 4}:
            Sound.stop_all()
        Sound.requested = sound
        Sound.last = sound
        Sound.last_time = system.currentTimeMillis()

    def tick_sound(self):  # called once per tick
        if Sound.players is None or not GameCanvas.sound_on:
            return
        Sound.players.tick()
        loop = False
        start = True
        i = Sound.requested
        Sound.requested = -1
        if GameCanvas.sound_on and i != -1:
            if i <= 2:
                if Sound.music == i:
                    start = False
                else:
                    Sound.stop_all()
                Sound.music = i
                loop = True
            else:
                Sound.music = -1
                loop = False
            if start:
                self.play_now(i, loop)

    def play_now(self, sound, loop):
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
    def stop_all():
        Sound.requested = -1
        Sound.music = -1
        Sound.players.stop()
