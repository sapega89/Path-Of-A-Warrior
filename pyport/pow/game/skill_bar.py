"""PORT-EXTRA (config.SKILL_BAR, config.SKILL_CARD): the skill bar and the belt in combat, and the
skill card of the Skills menu (like the HUD of Dragon Nest).

The phone game has no skills on the screen (keys 1 3 7 9 0 only) and only 2 of the 5 belt slots
in combat (keys * and #, chosen in Assign Items). With config.SKILL_BAR a strip above the HUD
frame shows

    Z X C V B  the 5 belt slots (cz.Z): icon and count; the key or a click uses that slot
    1 2 3 4 5  the 5 skill slots (cz.V = phone keys 1 3 7 9 0): icon, grey when the skill is not
               learned or the hero lacks the MP; a click uses the skill

Belt keys are new key codes BELT_CODES (-101..-105 = slot 0..4) that only the map reads; they
use a slot exactly like * / # do (c.java, ag.u_I), so the combat logic stays the Java one.

With config.SKILL_CARD the Skills menu shows a card instead of the one-line strip: name, level,
MP, what the skill does at this level (damage, strikes, heal, buff) and at the next level. The
numbers come from the formulas of the combat (ar.java hero_hits_enemy, c.java hero actions).
Only the existing art is used: skill.png / skillgray.png, tool.png and the bitmap font.
"""
import config
from pow.game import consts
from pow.game.game_canvas import GameCanvas
from pow.game.gfx import Gfx
from pow.midp.jint import idiv

BELT_CODES = (-101, -102, -103, -104, -105)      # belt slot 0..4 (keys Z X C V B)
SKILL_KEYS = (49, 51, 55, 57, 48)                 # skill slot 0..4 = phone keys 1 3 7 9 0
BELT_LABELS = "ZXCVB"
SKILL_LABELS = "12345"

CELL = 23           # slot pitch: 1 px shared border + 22 px icon
ICON = 22           # visible part of a 28x28 icon (3 px cut on every side)
BAR_H = 24
GROUP_W = CELL * 5 + 1

_img = {}


def _image(name):
    """skill / skillgray / tool, loaded once (the menus free their own copies in ct[])."""
    if name not in _img:
        _img[name] = GameCanvas.scene.load_image(name)
    return _img[name]


def bar_top():
    return GameCanvas.canvas_size.y - 61 - BAR_H


def belt_x(i):
    return i * CELL


def skill_x(i):
    return GameCanvas.canvas_size.x - GROUP_W + i * CELL


def playing():
    """The hero is on the map and can act (no pause menu, no popup, no talk)."""
    return (config.SKILL_BAR and GameCanvas.state == 3 and GameCanvas.map_mode.mode == 0
            and GameCanvas.popups.kind == 0 and GameCanvas.hero is not None)


# ---- numbers of a skill ------------------------------------------------------------------------

_MP_BASE = [5, 6, 7, 10, 15, 7, 10, 10, 8, 9, 10, 5, 6, 7, 9, 12, 20, 20, 20]   # ar.java:743-757
_MP_STEP = [3, 4, 5, 3, 4, 3, 3, 5, 3, 4, 5, 3, 4, 5, 5, 6, 5, 5, 5]
_HIT_FRAME = {21: 5, 22: 6, 23: 5, 24: 5}         # c.java: frame of the one hit (arrayOfByte2)
_BUFF_DIV = {17: 20, 18: 20, 19: 25}              # c.java: ATK / DEF buff = stat * lv / div


def mp_need(skill, lv):
    """MP the skill costs at level lv (ar.skill_mp_cost without spending it)."""
    if not 12 <= skill <= 30:
        return 0
    return _MP_BASE[skill - 12] + (max(lv, 1) - 1) * _MP_STEP[skill - 12]


def anim_frames(skill):
    """Frames of the hero's action `skill` (the animation ends at the first value > 200)."""
    cz = GameCanvas.hero
    try:
        seq = cz.anims[skill][0]
    except (TypeError, IndexError):
        return 0
    n = 0
    while n < len(seq) and seq[n] <= 200:
        n += 1
    return n


def strikes(skill):
    """How many times the action calls hero_attack(0) (c.java hero actions 12-30)."""
    n = anim_frames(skill)
    frames = range(n if n else 30)
    if skill == 12:
        return sum(1 for f in frames if 2 < f < 6)
    if skill == 13:
        return sum(1 for f in frames if 4 < f < 8)
    if skill == 14:
        return sum(1 for f in frames if f in (2, 4, 6, 8))
    if skill in (20, 25):
        return sum(1 for f in frames if f & 1)
    if skill in _HIT_FRAME or skill in (26, 27, 28, 29, 30):
        return 1
    return 0


def skill_lines(skill, lv):
    """What the skill does at level lv, as short lines of the card."""
    cz = GameCanvas.hero
    i = skill - 12
    lines = []
    if skill in (12, 13, 14) or 20 <= skill <= 30:
        bonus = idiv(cz.attack * lv, consts.aU[i])
        n = strikes(skill)
        lines.append("DMG %d%s%s" % (cz.attack + cz.attack_buff + bonus, " x%d" % n if n > 1 else "",
                                      " all" if skill >= 28 else ""))
    elif skill == 15:
        lines.append("HP+%d" % idiv(cz.max_hp * (4 + lv), 25))
    elif skill == 16:
        lines.append("HP+%d" % idiv(cz.max_hp * (9 + lv), 20))
    elif skill in _BUFF_DIV:
        ticks = 50 if lv < 4 else 100 if lv < 8 else 150
        secs = idiv(ticks * consts.aQ[GameCanvas.speed], 1000)
        parts = []
        if skill != 18:
            parts.append("ATK+%d" % max(1, idiv(cz.attack * lv, _BUFF_DIV[skill])))
        if skill != 17:
            parts.append("DEF+%d" % max(1, idiv(cz.defense * lv, _BUFF_DIV[skill])))
        lines.append(" ".join(parts) + " %ds" % secs)
    return lines


# ---- the bar on the map ------------------------------------------------------------------------

def _slot_box(x, y, hot):
    Gfx.fill_rect(x, y, CELL + 1, BAR_H, 0)
    Gfx.draw_rect(x, y, CELL + 1, BAR_H, GameCanvas.rgb(255, 255, 255) if hot else GameCanvas.rgb(90, 90, 90))


def _label(text, x, y):
    Gfx.set_font(GameCanvas.font_black)
    Gfx.draw_string(text, x + 1, y + 1, 0)
    Gfx.set_font(GameCanvas.font_white)
    Gfx.draw_string(text, x, y, 0)


def draw_bar():
    """Called by ar.draw_hud every map frame (the strip is opaque, so nothing is left behind)."""
    cz = GameCanvas.hero
    if not config.SKILL_BAR or cz is None:
        return
    y = bar_top()
    Gfx.fill_rect(0, y, GameCanvas.canvas_size.x, BAR_H, 0)
    tool = _image("tool")
    for b in range(5):
        x = belt_x(b)
        z = cz.quick_slots[b]
        active = GameCanvas.effect.item != 0 and GameCanvas.effect.slot == b
        _slot_box(x, y, active)
        if z.item != 0 and tool is not None:
            GameCanvas.draw_region(x + 1, y + 1, ICON, ICON, tool, (z.item - 1) * 28 + 3, 3)
            if z.count > 1:
                GameCanvas.draw_region(x + CELL - 9, y + BAR_H - 13, 9, 12, GameCanvas.images[20], z.count * 9, 0)
        _label(BELT_LABELS[b], x + 2, y)
    skill_img, gray_img = _image("skill"), _image("skillgray")
    for b in range(5):
        x = skill_x(b)
        s = cz.hotkeys[b]
        _slot_box(x, y, s != 0 and cz.action[0] == s)
        if s != 0 and skill_img is not None:
            lv = cz.skill_levels[s - 12]
            ready = lv > 0 and mp_need(s, lv) <= cz.mp
            GameCanvas.draw_region(x + 1, y + 1, ICON, ICON, skill_img if ready else gray_img, (s - 12) * 28 + 3, 3)
        _label(SKILL_LABELS[b], x + 2, y)


def key_at(x, y):
    """Key code of the bar slot under a click at (x, y), or None."""
    if not config.SKILL_BAR:
        return None
    top = bar_top()
    if not top <= y < top + BAR_H:
        return None
    for b in range(5):
        if belt_x(b) <= x < belt_x(b) + CELL + 1:
            return BELT_CODES[b]
        if skill_x(b) <= x < skill_x(b) + CELL + 1:
            return SKILL_KEYS[b]
    return -999          # the gap between the two groups: nothing


# ---- the skill card of the Skills menu ---------------------------------------------------------

CARD_X, CARD_W = 20, 200


def card_rect():
    """x, y, w, h of the card: from under the skill tree down to the soft keys."""
    y = GameCanvas.canvas_size.y - 108
    return CARD_X, y, CARD_W, 84


def _width(text):
    """Drawn width of text in the white font (Gfx.draw_chars adds char_width per glyph)."""
    f = GameCanvas.font_white
    return f.chars_width(list(text), 0, len(text))


def _wrap(text, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = w if not cur else cur + " " + w
        if _width(t) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def card_lines(skill):
    """(text, colour) lines of the card of `skill` (12..30); colour 1 = orange, 0 = white."""
    if not 12 <= skill <= 30:
        return [("Empty slot", 0), ("OK: put a skill here", 0)]
    cz = GameCanvas.hero
    i = skill - 12
    lv = cz.skill_levels[i]
    width = CARD_W - 8
    head = GameCanvas.edat_string(54, i) + ("  Lv%d" % lv if lv else "")
    lines = [(t, 1) for t in _wrap(head, width)]
    lines += [(t, 0) for t in _wrap(GameCanvas.edat_string(54, i + 19), width)]
    if lv == 0:
        lines.append(("Not learned", 0))
        now = "Lv1: MP %d, " % mp_need(skill, 1) + ", ".join(skill_lines(skill, 1))
        return lines + [(t, 0) for t in _wrap(now, width)]
    now = "MP %d, " % mp_need(skill, lv) + ", ".join(skill_lines(skill, lv))
    lines += [(t, 0) for t in _wrap(now, width)]
    if lv < 10:
        nxt = "Lv%d: MP %d, " % (lv + 1, mp_need(skill, lv + 1)) + ", ".join(skill_lines(skill, lv + 1))
    else:
        nxt = "Max level"
    return lines + [(t, 0) for t in _wrap(nxt, width)]


LINE_H = 13


def draw_card(skill):
    """The card in place of the description strip of the Skills menu (cM[0] == 15)."""
    x, y, w, h = card_rect()
    GameCanvas.draw_frame_box(x + GameCanvas.view_x, y + GameCanvas.view_y, w, h, 0, 5263440, 16777215, False)
    fonts = (GameCanvas.font_white, GameCanvas.font_orange)
    ly = y + 1
    for text, kind in card_lines(skill)[:h // LINE_H]:
        Gfx.set_font(fonts[kind])
        GameCanvas.draw_view_text(text, x + 4, ly)
        ly += LINE_H
    Gfx.set_font(GameCanvas.font_white)
