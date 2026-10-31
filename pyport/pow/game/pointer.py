"""Mouse control (PORT-EXTRA: the phone had no pointer).

A click is translated into the phone keys a player would press, so the game logic stays
exactly the Java one. Hit zones follow what is drawn on each screen (coordinates 240x320):

  title "PRESS ANY KEY"      click anywhere            -> FIRE
  popup Yes/No               click on the left / right -> select Yes / No, then FIRE
  popup Ok / text            click                     -> FIRE
  Main Menu (cM[0] == 5)     caption strip: arrow ◄ / ► -> LEFT / RIGHT, caption -> FIRE
  Game Menu (cM[0] == 0)     small button above -> UP, big button -> FIRE, below -> DOWN
  Difficulty (cM[0] == 29)   click Hard / Normal -> select it, then FIRE
  Hero (cM[0] == 6)          left / right head -> LEFT / RIGHT, middle head -> FIRE
  Name (cM[0] == 7)          click a letter or OK -> arrow keys to it, then FIRE
  Stat points (cM[0] == 8)   click a stat row -> UP/DOWN to it, then FIRE (+1 point)
  soft key BACK (bottom right)                         -> BACK (-7)
  right mouse button anywhere                          -> BACK (-7)
  wheel: Main Menu = LEFT/RIGHT, Game Menu = UP/DOWN, Yes/No popup = switch,
         Difficulty / Stat points = UP/DOWN, Hero = LEFT/RIGHT
"""
import collections

from pow.game.ag import ag

UP, DOWN, LEFT, RIGHT, FIRE, BACK = -1, -2, -3, -4, -5, -7


def _popup_keys(x, y, kind):
    cs = ag.cS
    if cs.b == 2:                       # Yes / No  (l.O_I: Yes left of centre, No right)
        if kind != "click":
            return [LEFT]               # LEFT/RIGHT both toggle l.k
        want = 0 if x < ag.dd else 1
        return ([LEFT] if cs.k != want else []) + [FIRE]
    if kind != "click":
        return []
    return [FIRE]


def _name_step(p, key):
    """ag.r(int) on a cursor value (ag.java:1775-1792), without touching ag.bP."""
    if key == UP:
        p = (p + 28 - 14) % 28
    elif key == DOWN:
        p = (p + 28 + 14) % 28
    elif key == LEFT:
        p = (p + 28 - 1) % 28
    elif key == RIGHT:
        p = (p + 28 + 1) % 28
        if p == 27:
            p = 0
    return 26 if p == 27 else p


def _name_path(src, dst):
    """Shortest list of arrow keys that moves the name cursor from src to dst."""
    prev = {src: None}
    todo = collections.deque([src])
    while todo:
        p = todo.popleft()
        if p == dst:
            break
        for key in (LEFT, RIGHT, UP, DOWN):
            q = _name_step(p, key)
            if q not in prev:
                prev[q] = (p, key)
                todo.append(q)
    keys = []
    p = dst
    while prev.get(p) is not None:
        p, key = prev[p]
        keys.append(key)
    return keys[::-1]


def _name_cell(x, y):
    """Cell of the letter grid ag.f(int,int) under (x, y): 0..25 letters, 26 OK, None outside."""
    j_ = ag.bL - 71
    top = ag.de + 32 + ag.dc
    if not (j_ + 2 <= x < j_ + 142 and top <= y < top + 34):
        return None
    row = (y - top) // 17
    if row == 1 and x >= j_ + 123:
        return 26
    return min(row * 14 + (x - j_ - 2) // 10, 25)


def _new_game_keys(c0, x, y, kind):
    """Hero creation screens (e.aU, e.aK, ag.f, e.O)."""
    dd, de = ag.dd, ag.de
    if c0 == 29:                        # e.aU: buttons at y = de-60 + b*25, h 20
        if kind != "click":
            return [UP]
        for b in range(2):
            top = de - 60 + b * 25
            if dd - 80 <= x < dd + 80 and top - 2 <= y < top + 22:
                return ([UP] if ag.cM[1] != b else []) + [FIRE]
        return []
    if c0 == 6:                         # e.aK: heads at x = dd-94 + 69*b, y = de+9, 50x50
        if kind != "click":
            return [LEFT if kind == "wheel_up" else RIGHT]
        if de + 4 <= y < de + 64:
            if x < dd - 27:
                return [LEFT]
            if x >= dd + 25:
                return [RIGHT]
            return [FIRE]
        return []
    if c0 == 7:                         # ag.f: 2 x 14 letters + OK
        if kind != "click":
            return []
        cell = _name_cell(x, y)
        if cell is None:
            return []
        return _name_path(ag.bP, cell) + [FIRE]
    if c0 == 8:                         # e.O: rows HP MP ATK DEF at y = eN+108 + b*20, h 18
        if kind != "click":
            return [UP if kind == "wheel_up" else DOWN]
        for b in range(4):
            top = ag.eN + 108 + b * 20
            if ag.eM + 39 <= x < ag.eM + 160 and top <= y < top + 20:
                d = b - ag.cM[1]
                return ([DOWN] * d if d > 0 else [UP] * -d) + [FIRE]
        return []
    return None


def keys_for(x, y, kind="click"):
    """-> list of phone key codes for a click / wheel at (x, y) in screen coordinates."""
    from pow.game.af import af
    bv = ag.bV
    if bv == 12:                        # outro, quits by itself
        return []
    if bv == 0:
        if af.b == 0:                   # logo
            return []
        if af.b == 1:                   # "Would you like sound enabled?"
            return _popup_keys(x, y, kind)
        return [FIRE] if kind == "click" else []      # title: any key
    if bv == 2 and ag.cS.b != 0:
        return _popup_keys(x, y, kind)
    if bv == 2:
        c0 = ag.cM[0]
        soft_back = x >= ag.bJ - ag.bU.getWidth() and y >= ag.bK - ag.bU.getHeight()
        if c0 == 5:                     # Main Menu, e.aJ: strip at y = 320-65, x = dd-52 .. dd+64
            if kind == "wheel_up":
                return [LEFT]
            if kind == "wheel_down":
                return [RIGHT]
            top = ag.bZ.b - 65
            if top - 12 <= y < top + 33:
                left = ag.dd - 52
                if x < left:
                    return [LEFT]
                if x >= left + 116:
                    return [RIGHT]
                return [FIRE]
            return []
        if c0 == 0:                     # Game Menu, e.bf: buttons at y 164 / 200 / 244
            if kind == "wheel_up":
                return [UP]
            if kind == "wheel_down":
                return [DOWN]
            if soft_back:
                return [BACK]
            if ag.ck == 2:              # carousel still moving
                return []
            if 150 <= y < 197:
                return [UP]
            if 197 <= y < 232:
                return [FIRE]
            if 232 <= y < 285:
                return [DOWN]
            return []
        if soft_back:
            return [BACK]
        keys = _new_game_keys(c0, x, y, kind)
        if keys is not None:
            return keys
    return [FIRE] if kind == "click" else []
