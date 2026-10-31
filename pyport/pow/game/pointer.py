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
  Prologue (bV == 10)        click -> FIRE (whole text / next page), soft key "Skip" -> LSOFT (-6)
  list menus (e.f: Management, Blacksmith, Etc, Help, Endings, ...)
                             click a row -> UP/DOWN to it, then FIRE
  Options (cM[0] == 9)       click a row -> select it; ◄ / ► half of the value box -> LEFT / RIGHT
  pages "◄ n / m ►" (Help, About, Endings)  click left / right of the centre -> LEFT / RIGHT
  Blacksmith grid (21..24)   click an item -> move the cursor to it; click it again -> FIRE
  Mission description (3)    ◄ / ► under the text -> pages, elsewhere -> FIRE (accept popup)
  Briefing (4)               click -> FIRE (whole line), soft key "SKIP" -> LSOFT (-6)
  Generals (19)              click a row -> UP/DOWN to it, then FIRE; ◄ / ► -> pages
  4-choice popup (talk topic)  click a topic -> UP/DOWN to it, then FIRE
  other screens (Skills, Gear, Inventory, Assign Items)  click -> FIRE, wheel -> UP/DOWN
  Map (bV == 3)              click beside the hero -> that direction (tap = start / stop
                             walking, two quick clicks = run); soft key PAUSE -> BACK (-7);
                             pause menu: click a row -> UP/DOWN to it, then FIRE
  soft key BACK (bottom right)                         -> BACK (-7)
  right mouse button anywhere                          -> BACK (-7)
  wheel: Main Menu = LEFT/RIGHT, Game Menu = UP/DOWN, Yes/No popup = switch,
         Difficulty / Stat points = UP/DOWN, Hero = LEFT/RIGHT
"""
import collections

from pow.game.ag import ag
from pow.midp.jint import idiv

UP, DOWN, LEFT, RIGHT, FIRE, BACK = -1, -2, -3, -4, -5, -7


def _popup_keys(x, y, kind):
    cs = ag.cS
    if cs.b == 2:                       # Yes / No  (l.O_I: Yes left of centre, No right)
        if kind != "click":
            return [LEFT]               # LEFT/RIGHT both toggle l.k
        want = 0 if x < ag.dd else 1
        return ([LEFT] if cs.k != want else []) + [FIRE]
    if cs.b == 3:                       # 4 choices (l.c: rows of 16 px below the text)
        if kind != "click":
            return [UP if kind == "wheel_up" else DOWN]
        top = ag.de - (cs.h >> 1) + 20 * cs.i + 5
        if top <= y < top + 64:
            want = (y - top) // 16
            return _steps(want - cs.k, UP, DOWN) + [FIRE]
        return []
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


def _steps(d, minus, plus):
    return [plus] * d if d > 0 else [minus] * -d


def _menu_keys(c0, x, y, kind):
    """Menu screens reached from the Game Menu (e.f, e.j, e.l, e.c(boolean))."""
    cM, dd, de, dc = ag.cM, ag.dd, ag.de, ag.dc
    if kind != "click":
        return [UP if kind == "wheel_up" else DOWN]
    if c0 == 3 and ag.de + 102 <= y < ag.de + 132:             # e.aH: pages at de+110
        return [LEFT if x < dd else RIGHT]
    if c0 == 19:                                               # e.aN: 4 rows of 22 px, 31 apart
        m = 20 + idiv(ag.bY.b - 30 - 177, 2) + 2
        top = m + 31
        pages = top + 4 * 31 + 6
        if pages - 8 <= y < pages + 22:
            return [LEFT if x < dd else RIGHT]
        if 18 <= x < 222 and top <= y < top + 4 * 31 and (y - top) % 31 < 22:
            want = cM[1] // 4 * 4 + (y - top) // 31
            if want < ag.cN:
                return _steps(want - cM[1], UP, DOWN) + [FIRE]
        return []
    if c0 in (25, 28) and ag.bZ.b - 43 <= y < ag.bZ.b - 13:   # e.a(int,int,int,boolean) at bZ.b-35      # e.a(int,int,int,boolean)
        return [LEFT if x < dd else RIGHT]
    if c0 in (1, 2, 10, 11, 12, 13, 25, 27):                   # e.f(): rows of 180x20, 30 apart
        rows = 5 if ag.cN > 5 else ag.cN
        if c0 == 25 and cM[2] >= 20:
            rows = 4
        top = de - (rows * 30 - 10) // 2 + dc
        if ag.bV == 3 or ag.bW == 3:                           # the map's pause menu: 30 px higher
            top -= 30
        if dd - 90 <= x < dd + 90 and top <= y < top + rows * 30 and (y - top) % 30 < 20:
            return _steps((y - top) // 30 - (cM[1] - cM[2]), UP, DOWN) + [FIRE]
        return []
    if c0 == 9:                                                # e.j(): rows 1, 2 at de-50 + 30*(b-1)
        for b in (1, 2):
            top = de - 50 + (b - 1) * 30 + dc
            if top <= y < top + 20 and dd - 100 <= x < dd + 100:
                keys = _steps(b - cM[1], UP, DOWN)
                if x >= dd - 10:
                    keys.append(LEFT if x < dd + 45 else RIGHT)
                return keys
        return []
    if c0 in (21, 22, 23, 24) and ag.fK[27] == 0:              # e.a(int, z[], int[]): 5 x fK[3] cells, 32 px
        fK = ag.fK
        x0, y0 = fK[5], fK[1] + 31
        if x0 <= x < x0 + 160 and y0 <= y < y0 + 32 * fK[3]:
            col, row = (x - x0) // 32, fK[8] + (y - y0) // 32
            if col == fK[9] and row == fK[10]:
                return [FIRE]
            return _steps(row - fK[10], UP, DOWN) + _steps(col - fK[9], LEFT, RIGHT)
        return []
    return [FIRE]


def _map_keys(x, y, kind):
    """The mission map (bV 3), the room scroll (4) and talks on the map (5)."""
    if ag.cS.b != 0:
        return _popup_keys(x, y, kind)
    if x >= ag.bJ - 60 and y >= ag.bK - 20:            # soft key PAUSE / BACK (bottom right)
        return [BACK]
    if ag.bV != 3:
        return [FIRE] if kind == "click" else []
    if ag.cR.a == 1:                                   # pause menu: e.f() list, cM[0] == 10
        return _menu_keys(10, x, y, kind)
    if ag.cR.a != 0:                                   # Assign Items / Options / Help of the pause
        if kind != "click":
            return [UP if kind == "wheel_up" else DOWN]
        return [FIRE]
    if kind != "click":
        return []
    # walking: a click beside the hero = a tap on that direction (start / stop walking)
    hx = ag.cz.a[0].a - ag.ca.a + ag.db
    hy = ag.cz.a[0].b - ag.ca.b + ag.dc - 20
    dx, dy = x - hx, y - hy
    if abs(dx) >= abs(dy):
        return [LEFT if dx < 0 else RIGHT]
    return [UP if dy < 0 else DOWN]


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
    if bv == 10:                        # story player ag.M(): FIRE shows the text, -6 skips
        if ag.cS.b != 0:
            return _popup_keys(x, y, kind)
        if kind != "click":
            return []
        if x < ag.bU.getWidth() and y >= ag.bK - ag.bU.getHeight():
            return [-6]
        return [FIRE]
    if bv in (3, 4, 5):
        return _map_keys(x, y, kind)
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
        if c0 == 4 and kind == "click" and x < ag.bU.getWidth() and y >= ag.bK - ag.bU.getHeight():
            return [-6]                 # briefing: soft key "SKIP"
        keys = _new_game_keys(c0, x, y, kind)
        if keys is not None:
            return keys
        return _menu_keys(c0, x, y, kind)
    return [FIRE] if kind == "click" else []
