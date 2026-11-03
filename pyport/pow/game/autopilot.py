"""Auto-hunt on the mission map (PORT-EXTRA, config.AUTO_HUNT: the phone game had no such thing).

The autopilot plays like a player: every tick it may hold a direction (the HOLD_TO_MOVE walk) and
press one phone key (attack, a skill key 1-5, the potion keys * / #), so the game logic stays the
Java one. Its choices:
  - potions: an HP potion below 30 % HP when no heal skill can be cast, an MP potion when the MP
    is too low for any skill while enemies are around;
  - heal (Medium / Maximum Heal) below 40 % HP; the MP of a heal is kept for it otherwise;
  - a soul when no aura is up and the fight is big (3+ enemies, or a general);
  - Thunder Storm / Dragon Breath / Meteor Strike on 3+ enemies, Flame Twister & co on 2+ near;
  - Lightning when the target stands about 60 px ahead, out of reach of the sword;
  - a strike skill (Wind Slasher, Tide Crasher ...) on a general, on 2+ enemies in reach or with
    the MP nearly full, else the attack combo;
  - it walks to the nearest living enemy, and around a wall when it stops moving;
  - a cleared room: out through an open exit, to a room it has not seen yet when it can.
Talks on the map, popups and the pause menu stay the player's.
"""
import config
from pow.game import consts
from pow.game.game_canvas import GameCanvas

TOGGLE = -100                          # the key code of Tab / the AUTO corner (game_canvas.key_down)
FIRE, STAR, POUND = -5, 42, 35
SKILL_KEYS = (49, 51, 55, 57, 48)      # hero.hotkeys[0..4]
DIR_KEY = {0: -2, 2: -3, 4: -1, 6: -4}  # facing -> direction key (map_scene._HELD_DIR)

HEALS = (15, 16)
SOULS = (17, 18, 19)
WHOLE = (28, 29, 30)                   # every enemy of the room
NEAR = (23, 24, 25)                    # a circle of 45 px
RANGED = (26, 27)                      # a point 60 px ahead, radius 35
STRIKES = (12, 13, 14, 20, 21, 22)     # in front, like the attack

# ar.e(int) (map_engine.skill_mp_cost) without spending the MP
MP_BASE = (5, 6, 7, 10, 15, 7, 10, 10, 8, 9, 10, 5, 6, 7, 9, 12, 20, 20, 20)
MP_INC = (3, 4, 5, 3, 4, 3, 3, 5, 3, 4, 5, 3, 4, 5, 5, 6, 5, 5, 5)

HP_POTIONS = (1, 2, 3, 7, 8, 9)        # draw_potion_effect: 1-3 HP, 4-6 MP, 7-9 both
MP_POTIONS = (4, 5, 6, 7, 8, 9)
MANUAL_PAUSE = 12                      # ticks the autopilot waits after a key of the player
STUCK_TICKS = 4                        # ticks without moving -> go around
DETOUR_TICKS = 8


def distance(a, b):
    from pow.game.map_engine import MapEngine
    return MapEngine.distance(a, b)


def dir4(a, b):
    from pow.game.map_engine import MapEngine
    return MapEngine.dir4(a, b)


class Autopilot:
    on = False
    direction = None                   # the direction key held now, or None
    manual = 0
    _last = None
    _still = 0
    _detour = None
    _detour_ticks = 0
    _map = None                        # the map whose rooms _seen holds
    _seen = set()
    _exit_cell = None
    _exit = None

    @classmethod
    def reset(cls):
        cls.on = config.AUTO_HUNT
        cls.direction = None
        cls.manual = 0
        cls._last = None
        cls._still = cls._detour_ticks = 0
        cls._detour = None
        cls._map = cls._exit_cell = cls._exit = None
        cls._seen = set()

    @classmethod
    def toggle(cls):
        cls.on = not cls.on
        cls.direction = None
        GameCanvas.redraw = 1          # the corner badge goes with a full redraw of the map

    @classmethod
    def player_key(cls):
        """The player pressed a key: hands off for a moment."""
        cls.manual = MANUAL_PAUSE
        cls.direction = None

    @staticmethod
    def playing():
        return (GameCanvas.state == 3 and GameCanvas.map_mode.mode == 0 and GameCanvas.popups.kind == 0
                and not GameCanvas.paused and GameCanvas.hero is not None
                and GameCanvas.hero.pos[0] is not None)

    @staticmethod
    def enemies():
        out = []
        for b in range(GameCanvas.actor_count):
            ex = GameCanvas.actors[GameCanvas.actor_slots[b]]
            if ex is not None and ex.hp > 0:
                out.append(ex)
        return out

    # --- one tick ---------------------------------------------------------------------------------
    @classmethod
    def tick(cls):
        """The key to press this tick (or None); sets `direction`."""
        if not cls.on or not cls.playing():
            cls.direction = None
            return None
        if cls.manual > 0:
            cls.manual -= 1
            cls.direction = None
            return None
        cz = GameCanvas.hero
        if cz.action[0] >= 2 or GameCanvas.effect.item != 0:     # busy: attack, skill, hurt, potion
            return None
        if GameCanvas.key_pressed != -999:     # a key of this tick is already there
            return None
        foes = cls.enemies()
        key = cls._potion(cz, foes)
        if key is not None:
            cls.direction = None
            return key
        key = cls._heal(cz)
        if key is not None:
            cls.direction = None
            return key
        if not foes:
            cls.direction = cls._to_exit(cz)
            return None
        target = min(foes, key=lambda ex: distance(cz.pos[0], ex.pos[0]))
        dist = distance(cz.pos[0], target.pos[0])
        reach = consts.aK[cz.weapon_kind] - 6
        key = cls._skill(cz, foes, target, dist, reach)
        if key is not None or dist <= reach:
            cls.direction = None
            cz.dir[0] = cz.facing = dir4(cz.pos[0], target.pos[0])     # as ar.f() turns the hero
            return key if key is not None else FIRE
        cls.direction = cls._walk(cz, target)
        return None

    @classmethod
    def _walk(cls, cz, target):
        pos = (cz.pos[0].x, cz.pos[0].y)
        cls._still = cls._still + 1 if pos == cls._last and cz.action[0] == 1 else 0
        cls._last = pos
        want = dir4(cz.pos[0], target.pos[0])
        if cls._detour_ticks > 0:
            cls._detour_ticks -= 1
            return DIR_KEY[cls._detour]
        if cls._still >= STUCK_TICKS:          # a wall: go along it, toward the target's other axis
            cls._still = 0
            dx, dy = target.pos[0].x - cz.pos[0].x, target.pos[0].y - cz.pos[0].y
            if want in (0, 4):
                cls._detour = 6 if dx > 0 else 2
            else:
                cls._detour = 0 if dy > 0 else 4
            cls._detour_ticks = DETOUR_TICKS
            return DIR_KEY[cls._detour]
        return DIR_KEY[want]

    # --- potions --------------------------------------------------------------------------------------
    @classmethod
    def _potion(cls, cz, foes):
        hp_low = cz.hp * 100 < cz.max_hp * 30
        if hp_low and cls._castable(cz, HEALS):
            hp_low = False                     # the heal skill comes first (_skill)
        mp_low = bool(foes) and cz.max_mp > 0 and not cls._castable(cz, [s for s in cz.hotkeys if s])
        mp_low = mp_low and any(12 <= s <= 30 for s in cz.hotkeys)
        for k, key in enumerate((STAR, POUND)):
            slot = cz.quick_slots[cz.quick_keys[k]]
            if slot is None or slot.count < 1:
                continue
            if hp_low and slot.item in HP_POTIONS:
                return key
            if mp_low and slot.item in MP_POTIONS and cz.mp * 100 < cz.max_mp * 50:
                return key
        return None

    # --- skills ---------------------------------------------------------------------------------------
    @staticmethod
    def cost(cz, sid):
        i = sid - 12
        return MP_BASE[i] + (cz.skill_levels[i] - 1) * MP_INC[i]

    @classmethod
    def _slots(cls, cz):
        return [(k, s) for k, s in enumerate(cz.hotkeys) if 12 <= s <= 30 and cz.skill_levels[s - 12] > 0]

    @classmethod
    def _castable(cls, cz, kinds):
        return [s for _, s in cls._slots(cz) if s in kinds and cls.cost(cz, s) <= cz.mp]

    @classmethod
    def _heal(cls, cz):
        """Medium Heal below 40 % HP, Maximum Heal first below 25 %."""
        hp_pct = cz.hp * 100 // max(1, cz.max_hp)
        if hp_pct >= 40:
            return None
        slots = cls._slots(cz)
        key_of = {s: SKILL_KEYS[k] for k, s in reversed(slots)}
        for s in ((16, 15) if hp_pct < 25 else (15, 16)):
            if s in key_of and cls.cost(cz, s) <= cz.mp:
                return key_of[s]
        return None

    # --- the next room ------------------------------------------------------------------------------
    @classmethod
    def _to_exit(cls, cz):
        """The room is clear and its exits open (room_phase 1, map_engine.keep_in_room): walk out,
        through an exit to a room not seen yet when there is one (exits: down, left, up, right)."""
        if GameCanvas.room_phase != 1 or GameCanvas.room_phase_timer >= 0:
            return None
        if cls._map is not GameCanvas.map:
            cls._map = GameCanvas.map
            cls._seen = set()
        cell = GameCanvas.cell
        cls._seen.add(cell)
        if cls._exit_cell != cell:
            cls._exit_cell = cell
            w = max(1, GameCanvas.map.size.w // 7)
            step = (w, -1, -w, 1)
            exits = [b for b in range(4) if GameCanvas.cells[cell].exits[b] != 0]
            if not exits:
                cls._exit = None
                return None
            new = [b for b in exits if cell + step[b] not in cls._seen]
            cls._exit = (new or exits)[GameCanvas.frame % len(new or exits)]
        if cls._exit is None:
            return None
        if cls._detour_ticks > 0:
            cls._detour_ticks -= 1
            return DIR_KEY[cls._detour]
        pos = (cz.pos[0].x, cz.pos[0].y)
        cls._still = cls._still + 1 if pos == cls._last and cz.action[0] == 1 else 0
        cls._last = pos
        want = (0, 2, 4, 6)[cls._exit]
        if cls._still >= STUCK_TICKS:
            cls._still = 0
            cls._detour = (want + 2 + 4 * (GameCanvas.frame & 1)) & 7
            cls._detour_ticks = DETOUR_TICKS
            return DIR_KEY[cls._detour]
        return DIR_KEY[want]

    @classmethod
    def _skill(cls, cz, foes, target, dist, reach):
        slots = cls._slots(cz)
        if not slots:
            return None
        key_of = {s: SKILL_KEYS[k] for k, s in reversed(slots)}

        def can(s):
            return s in key_of and cls.cost(cz, s) <= cz.mp

        heal_mp = min((cls.cost(cz, s) for s in HEALS if s in key_of), default=0)

        def usable(group):
            return [s for s in group if can(s) and cz.mp - cls.cost(cz, s) >= heal_mp]

        near = sum(1 for ex in foes if distance(cz.pos[0], ex.pos[0]) <= 45)
        general = any(ex.type < 200 for ex in foes)
        big = len(foes) >= 3 or general
        if big and cz.attack_buff_ticks <= 0 and cz.defense_buff_ticks <= 0:
            for s in usable((19, 17, 18)):
                return key_of[s]
        if len(foes) >= 3:
            for s in sorted(usable(WHOLE), key=lambda s: -cls.cost(cz, s)):
                return key_of[s]
        if near >= 2:
            for s in sorted(usable(NEAR), key=lambda s: -cls.cost(cz, s)):
                return key_of[s]
        if dist > reach:
            d = dir4(cz.pos[0], target.pos[0])
            ahead_x = cz.pos[0].x + consts.aA[d >> 1]
            ahead_y = cz.pos[0].y + consts.aB[d >> 1]
            if (ahead_x - target.pos[0].x) ** 2 + (ahead_y - target.pos[0].y) ** 2 <= 35 * 35:
                for s in usable(RANGED):
                    return key_of[s]
            return None
        # a strike skill on a general, on a crowd in reach, or when the MP is nearly full anyway
        crowd = sum(1 for ex in foes if distance(cz.pos[0], ex.pos[0]) <= reach) >= 2
        if (general and target.type < 200) or crowd or cz.mp * 100 >= cz.max_mp * 80:
            for s in sorted(usable(STRIKES), key=lambda s: -cls.cost(cz, s)):
                return key_of[s]
        return None


Autopilot.reset()
