"""Regression: the cell-script hash ag.cH must never get a cycle (c.aC / c.a_III).

Before the fix c.aC() kept the old links .b; after some map loads a_III() made a link to a lower
index (even a node to itself) and the next a_III() into that bucket looped forever: the game froze.
"""
import random


def _buckets_end():
    from pow.game.ag import ag
    for head in range(8):
        i, seen = head, set()
        while ag.cH[i].b != 0:
            if i in seen:
                return False
            seen.add(i)
            i = ag.cH[i].b
    return True


def test_cell_script_hash_has_no_cycles():
    from pow.game.ag import ag
    from pow.game.c import c
    rnd = random.Random(1)
    for _ in range(3000):              # 3000 map loads with random scripts
        c.aC()
        for k in range(rnd.randint(0, 30)):
            if ag.cI >= 49:
                break
            assert _buckets_end()
            c.a_III(k, rnd.randrange(8), 0)
        assert _buckets_end()
