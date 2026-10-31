"""Mouse control (PORT-EXTRA: the phone had no pointer).

A click is translated into the phone keys a player would press, so the game logic stays
exactly the Java one. Hit zones follow what is drawn on each screen (coordinates 240x320):

  title "PRESS ANY KEY"      click anywhere            -> FIRE
  popup Yes/No               click on the left / right -> select Yes / No, then FIRE
  popup Ok / text            click                     -> FIRE
  Main Menu (cM[0] == 5)     caption strip: arrow ◄ / ► -> LEFT / RIGHT, caption -> FIRE
  Game Menu (cM[0] == 0)     small button above -> UP, big button -> FIRE, below -> DOWN
  soft key BACK (bottom right)                         -> BACK (-7)
  right mouse button anywhere                          -> BACK (-7)
  wheel: Main Menu = LEFT/RIGHT, Game Menu = UP/DOWN, Yes/No popup = switch
"""
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
    return [FIRE] if kind == "click" else []
