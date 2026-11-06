"""Regression: the cell-script hash ag.cH must never get a cycle.

Before the fix c.aC() kept the old links .b; after some map loads a_III() made a link to a lower
index (even a node to itself) and the next a_III() into that bucket looped forever: the game froze.
"""
import random


def _buckets_end():
    from pow.game.game_canvas import GameCanvas
    for head in range(8):
        i, seen = head, set()
        while GameCanvas.cell_scripts[i].next != 0:
            if i in seen:
                return False
            seen.add(i)
            i = GameCanvas.cell_scripts[i].next
    return True


def test_cell_script_hash_has_no_cycles():
    from pow.game.game_canvas import GameCanvas
    from pow.game.map_scene import MapScene
    rnd = random.Random(1)
    for _ in range(3000):              # 3000 map loads with random scripts
        MapScene.reset_cell_scripts()
        for k in range(rnd.randint(0, 30)):
            if GameCanvas.cell_script_next >= 49:
                break
            assert _buckets_end()
            MapScene.cell_script_slot(k, rnd.randrange(8), 0)
        assert _buckets_end()
