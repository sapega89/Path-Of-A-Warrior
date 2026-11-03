"""PORT-EXTRA (proposal 22, "clans as lord houses"): the hero's oath to a lord, offline.

Game Menu > Management > House (menu cM[0] == 30) lists the houses of the lords the hero can
serve (pow/house_data.py). Each row is the lord and the hero's loyalty to him, cz.ak[lord - 1],
the number the campaign already keeps (+5 per mission won for that lord) and that picks the
ending; the original never showed it. FIRE on a row swears allegiance to that lord (yes / no).

- The oath needs loyalty LOYALTY_TO_SWEAR: the lord must know the hero.
- Leaving a house for another halves the loyalty to the old lord (house_data.oath_break).
- The house bonus: the hero hits the foes of his house harder (house_data.foe_bonus_percent,
  5% .. 15% with the loyalty). The foes are the generals the hero fights for that lord, and on
  a mission for his own lord every general he meets.
- The oath is kept in the save, in the first of the four ints ag.ar() writes as 0 (ag.java:2961),
  so a save without an oath reads 0 = no house and the save keeps its size.

No new art: the rows are the boxes of the list menus (e.f()), the heraldry is the lord's name.
"""
from pow import house_data
from pow.game.game_canvas import GameCanvas
from pow.game.gfx import Gfx
from pow.game.res_reader import ResReader

MENU = 30                 # cM[0] of the House screen (menus 0..29 are the original ones)
ROWS = 5                  # rows on screen, as e.f()
ROW_W, ROW_H, ROW_STEP = 180, 20, 30
INFO_LINES = 4
TITLE = "House"
MENU_ITEM = "House"       # the 6th row of Management

_houses = None
_foe_names = None


def houses():
    """[house_data.House] of the game data, read once."""
    global _houses, _foe_names
    if _houses is None:
        mission = ResReader.read("/mission.arr")
        sideinfo = ResReader.read("/sideinfo.arr")
        ruler = ResReader.read("/ruler.arr")
        general = ResReader.read("/general.arr")
        if mission is None or sideinfo is None or ruler is None:
            _houses, _foe_names = [], []
        else:
            _houses = house_data.build_houses(mission, sideinfo, ruler)
            _foe_names = house_data.general_names(general) if general is not None else []
    return _houses


def foe_name(general_id):
    houses()
    if 1 <= general_id <= len(_foe_names):
        return _foe_names[general_id - 1]
    return "?"


def house_of(lord):
    for h in houses():
        if h.lord == lord:
            return h
    return None


def loyalty(lord):
    """cz.ak[lord - 1]: the loyalty the campaign keeps for that lord."""
    if not 1 <= lord <= house_data.RULER_COUNT:
        return 0
    return max(0, GameCanvas.hero.mission_progress[lord - 1])


def sworn():
    """The House the hero swore to, or None."""
    return house_of(GameCanvas.house) if GameCanvas.house else None


def can_swear(lord):
    return lord != GameCanvas.house and loyalty(lord) >= house_data.LOYALTY_TO_SWEAR


def swear(lord):
    """The oath. Leaving a house costs half the loyalty to the old lord. True when sworn."""
    if not can_swear(lord) or house_of(lord) is None:
        return False
    cz = GameCanvas.hero
    old = GameCanvas.house
    if old and 1 <= old <= house_data.RULER_COUNT:
        cz.mission_progress[old - 1] = house_data.oath_break(cz.mission_progress[old - 1])
    GameCanvas.house = lord
    return True


def is_foe(general_id):
    """Is the general (1-based id < 200, an ap.c of a duel) a foe of the hero's house?"""
    h = sworn()
    if h is None or not 1 <= general_id < 200:
        return False
    if general_id in h.foes:
        return True
    if GameCanvas.state in (3, 4, 5):      # on a mission for his own lord every general is a foe
        dz = GameCanvas.lords[GameCanvas.mission] if 0 <= GameCanvas.mission < len(GameCanvas.lords) else None
        return dz is not None and dz.id == h.lord
    return False


def extra_damage(general_id, dealt):
    """The house bonus on a hit of `dealt` HP against actor type general_id (ar.a(int, int))."""
    if dealt <= 0 or not is_foe(general_id):
        return 0
    return max(1, dealt * house_data.foe_bonus_percent(loyalty(GameCanvas.house)) // 100)


# --- the screen ------------------------------------------------------------------------------

def enter():
    """Management > House (after e.b() put cM[0] = 30 and cM[1] = cM[2] = 0)."""
    GameCanvas.menu_count = len(houses())
    cM = GameCanvas.menu
    if GameCanvas.house:                      # the cursor starts on the sworn house
        for i, h in enumerate(houses()):
            if h.lord == GameCanvas.house:
                cM[1] = i
                cM[2] = max(0, i - ROWS + 1)


def list_top():
    rows = min(ROWS, GameCanvas.menu_count)
    return GameCanvas.view_cy - (rows * ROW_STEP - 10) // 2 - 40


def row_at(x, y):
    """The house index under the screen point (x, y), or None (mouse, pointer.py)."""
    cM = GameCanvas.menu
    rows = min(ROWS, GameCanvas.menu_count)
    top = list_top() + GameCanvas.view_y
    left = GameCanvas.view_cx - ROW_W // 2
    if left <= x < left + ROW_W and top <= y < top + rows * ROW_STEP and (y - top) % ROW_STEP < ROW_H:
        return cM[2] + (y - top) // ROW_STEP
    return None


def info_lines(h):
    """The lines under the list for house h."""
    lv = loyalty(h.lord)
    lines = ["Loyalty %d/%d" % (lv, house_data.LOYALTY_MAX)]
    if h.lord == GameCanvas.house:
        lines[0] += " Sworn"
        lines.append("Foes take +%d%% damage" % house_data.foe_bonus_percent(lv))
    elif lv < house_data.LOYALTY_TO_SWEAR:
        lines.append("Serve him in a mission")
    else:
        lines.append("Select: swear allegiance")
    words = [foe_name(g) + ("," if i < len(h.foes) - 1 else "") for i, g in enumerate(h.foes)]
    line = "Foes:"
    for w in words:
        if len(line) + 1 + len(w) > 24:
            if len(lines) == INFO_LINES - 1:          # the last line: no room for the rest
                line = line.rstrip(",") + " ..."
                break
            lines.append(line)
            line = " "
        line += " " + w
    lines.append(line)
    return lines


def draw(menus):
    """cM[0] == 30 in e.a(int): rows like e.f(), then the lines of the house under the cursor."""
    cM = GameCanvas.menu
    hs = houses()
    left = GameCanvas.view_cx - ROW_W // 2
    j_ = list_top()
    k = j_
    rows = min(ROWS, len(hs))
    for b in range(rows):
        i = cM[2] + b
        if i >= len(hs):
            break
        h = hs[i]
        sel = cM[1] == i
        menus.draw_box(left, j_ + GameCanvas.view_y, ROW_W, ROW_H, sel)
        if sel:
            Gfx.set_font(GameCanvas.font_orange)
        elif loyalty(h.lord) < house_data.LOYALTY_TO_SWEAR and h.lord != GameCanvas.house:
            Gfx.set_font(GameCanvas.font_gray)
        else:
            Gfx.set_font(GameCanvas.font_white)
        mark = "*" if h.lord == GameCanvas.house else ""
        Gfx.draw_string(mark + h.name, left + 6 + GameCanvas.view_x, j_ + 1 + GameCanvas.view_y, 0)
        Gfx.draw_string(str(loyalty(h.lord)), left + ROW_W - 6 + GameCanvas.view_x, j_ + 1 + GameCanvas.view_y, 8)
        j_ += ROW_STEP
    if cM[2] != 0 or cM[2] + ROWS < len(hs):
        menus.draw_arrow(2, GameCanvas.view_cx - 8 - GameCanvas.view_x, k - 10 - 5)
        menus.draw_arrow(3, GameCanvas.view_cx - 8 - GameCanvas.view_x, j_ - 5)
    if 0 <= cM[1] < len(hs):
        Gfx.set_font(GameCanvas.font_white)
        y = j_ + 14
        for line in info_lines(hs[cM[1]]):
            Gfx.draw_string(line, 12 + GameCanvas.view_x, y + GameCanvas.view_y, 0)
            y += 17


def fire():
    """FIRE on a row: the yes / no popup of the oath, or why there is none."""
    cM = GameCanvas.menu
    hs = houses()
    if not 0 <= cM[1] < len(hs):
        return
    h = hs[cM[1]]
    p = GameCanvas.popups
    p.reset()
    p.from_gamestr = 0
    if h.lord == GameCanvas.house:
        p.show_text("3You serve|" + h.name + ".")
    elif not can_swear(h.lord):
        p.show_text("3" + h.name + "|does not know you.|Win a mission|for him first.")
    elif GameCanvas.house:
        p.show_text("2Leave " + sworn().name + "|and swear to|" + h.name + "?|Old loyalty halves.")
    else:
        p.show_text("2Swear allegiance|to " + h.name + "?")
    GameCanvas.redraw = 1


def on_yes():
    """YES of the oath popup (l.b(), cM[0] == 30)."""
    cM = GameCanvas.menu
    hs = houses()
    if 0 <= cM[1] < len(hs) and swear(hs[cM[1]].lord):
        GameCanvas.menus.save_game()
    GameCanvas.redraw = 1
