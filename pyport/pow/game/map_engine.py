"""ar.java - the map / combat engine (bc). Literal port: the frame loop, the hero's walls and
room exits, room scrolling, the HUD of the map, the pause menu, the enemy AI, hits, skills,
potions and scrolls, deaths and drops. config.NO_ENEMIES / NO_COMBAT (PORT-EXTRA, off by
default) give the map without enemies / without the attack keys."""
from pow.game import consts
from pow.game.game_canvas import GameCanvas
from pow.game.map_scene import MapScene
from pow.game.structs import Point, Rect
from pow.game.gfx import Gfx
import config
from pow.midp.jint import i8, i16, idiv

F6 = config.DECOMP_FIX["F6"]


class MapEngine(GameCanvas):
    def __init__(self):  # ar.java:2-4
        super().__init__(GameCanvas.midlet)

    def tick_map(self):  # ar.java:6-23  (one tick of the map)
        if GameCanvas.popups.kind != 0:
            GameCanvas.popups.popup_keys()
            self.paint_state()
        elif GameCanvas.map_mode.mode != 0:
            self.pause_menu_keys()
            self.paint_state()
        else:
            GameCanvas.scene.tick_scene()
            self.paint_state()
            self.end_tick()
            if not self.map_started:
                self.tick_mission_clock(1)
                return
        self.tick_mission_clock(0)

    def draw_map(self, paramInt):  # ar.java:25-93  (draw the map, its pause menu and popups)
        if paramInt == 1:
            self.draw_view_background()
            for b in range(9):
                for b1 in range(9):
                    GameCanvas.dirty[b][b1] = 1
            GameCanvas.scene.draw_frame()
            if GameCanvas.map_mode.mode != 0:
                GameCanvas.popups.draw_popup_frame(170)
                v = GameCanvas.map_mode.mode
                if v == 1:
                    GameCanvas.menus.draw_list_menu()
                elif v == 2:
                    GameCanvas.menus.draw_assign_items(0)
                    GameCanvas.menus.draw_description_strip()
                elif v == 3:
                    GameCanvas.menus.draw_options()
                elif v == 4:
                    GameCanvas.menus.draw_help_page()
            if GameCanvas.popups.kind != 0:
                GameCanvas.popups.draw_popup()
                GameCanvas.menus.draw_popup_extras()
            return
        if paramInt == 2:
            return
        if GameCanvas.popups.kind != 0:
            if GameCanvas.popups.popup_redraw != 0:
                GameCanvas.popups.draw_popup()
            GameCanvas.menus.draw_popup_extras()
            return
        if GameCanvas.map_mode.mode != 0:
            if GameCanvas.map_mode.sub != 0:
                v = GameCanvas.map_mode.mode
                if v == 1:
                    GameCanvas.popups.draw_popup_frame(170)
                    GameCanvas.menus.draw_list_menu()
                elif v == 2:
                    GameCanvas.menus.draw_assign_items(1)
                elif v == 3:
                    GameCanvas.popups.draw_popup_frame(170)
                    GameCanvas.menus.draw_options()
                elif v == 4:
                    GameCanvas.popups.draw_popup_frame(170)
                    GameCanvas.menus.draw_help_page()
                GameCanvas.map_mode.sub = 0
            if GameCanvas.map_mode.mode == 2:
                GameCanvas.menus.draw_description_strip()
                return
        else:
            GameCanvas.scene.draw_frame()

    def pause_menu_keys(self):  # ar.java:95-247  (keys of the pause menu cR.a: 1 menu, 2 items, 3 options, 4 help)
        arrayOfByte1 = [0, 3, 0, 2, 4, 0, 0]
        arrayOfByte2 = [0, consts.menu_sizes[9], 0, 5, 3, 0, 0]    # Options: 3 rows (+1 with config.SCREEN_OPTION)
        v = GameCanvas.key
        blocked = GameCanvas.actor_count > 0 or GameCanvas.boss_fight != 0 or GameCanvas.waves[0] != 0
        if v in (-1, 50):
            if GameCanvas.map_mode.mode in (1, 3):
                GameCanvas.menu[1] = GameCanvas.menu[1] - 1
                if (GameCanvas.menu[1] < 0) if F6 else (GameCanvas.menu[1] - 1 < 0):   # DECOMP-FIX F6
                    GameCanvas.menu[1] = GameCanvas.menu_count - 1
                if GameCanvas.menu[1] == 1 and GameCanvas.map_mode.mode == 3 and not GameCanvas.sound_on:
                    GameCanvas.menu[1] = 0
                if GameCanvas.menu[1] == 2 and GameCanvas.map_mode.mode == 1 and blocked:
                    GameCanvas.menu[1] = GameCanvas.menu[1] - 1
                GameCanvas.clamp_menu_scroll()
                GameCanvas.map_mode.sub = 1
            return
        if v in (-2, 56):
            if GameCanvas.map_mode.mode in (1, 3):
                GameCanvas.menu[1] = GameCanvas.menu[1] + 1
                if (GameCanvas.menu[1] >= GameCanvas.menu_count) if F6 else (GameCanvas.menu[1] + 1 >= GameCanvas.menu_count):   # DECOMP-FIX F6
                    GameCanvas.menu[1] = 0
                if GameCanvas.menu[1] == 1 and GameCanvas.map_mode.mode == 3 and not GameCanvas.sound_on:
                    GameCanvas.menu[1] = 2
                if GameCanvas.menu[1] == 2 and GameCanvas.map_mode.mode == 1 and blocked:
                    GameCanvas.menu[1] = GameCanvas.menu[1] + 1
                GameCanvas.clamp_menu_scroll()
                GameCanvas.map_mode.sub = 1
            return
        if v in (-3, 52):
            if GameCanvas.map_mode.mode in (2, 4):
                GameCanvas.menu[1] = GameCanvas.menu[1] - 1
                if (GameCanvas.menu[1] < 0) if F6 else (GameCanvas.menu[1] - 1 < 0):   # DECOMP-FIX F6
                    GameCanvas.menu[1] = GameCanvas.menu_count - 1
                GameCanvas.map_mode.sub = 1
            elif GameCanvas.map_mode.mode == 3:
                self.change_option(0)
                GameCanvas.map_mode.sub = 1
            return
        if v in (-4, 54):
            if GameCanvas.map_mode.mode in (2, 4):
                GameCanvas.menu[1] = GameCanvas.menu[1] + 1
                if (GameCanvas.menu[1] >= GameCanvas.menu_count) if F6 else (GameCanvas.menu[1] + 1 >= GameCanvas.menu_count):   # DECOMP-FIX F6
                    GameCanvas.menu[1] = 0
                GameCanvas.map_mode.sub = 1
            elif GameCanvas.map_mode.mode == 3:
                self.change_option(1)
                GameCanvas.map_mode.sub = 1
            return
        if v == 42:
            if GameCanvas.map_mode.mode == 2:
                GameCanvas.redraw = MapEngine.assign_quick_potion(0)
            return
        if v == 35:
            if GameCanvas.map_mode.mode == 2:
                GameCanvas.redraw = MapEngine.assign_quick_potion(1)
            return
        if v in (-5, 53):
            if GameCanvas.menu[0] == 10 and GameCanvas.menu[1] == 4:
                GameCanvas.menu[0] = 5
                GameCanvas.menu[1] = 3
                GameCanvas.prev_state = GameCanvas.state
                GameCanvas.state = 2
                GameCanvas.menus.key_fire()
                return
            if GameCanvas.map_mode.mode == 1:
                if arrayOfByte1[GameCanvas.menu[1]] != 0:
                    GameCanvas.map_mode.mode = arrayOfByte1[GameCanvas.menu[1]]
                    GameCanvas.menu_count = arrayOfByte2[GameCanvas.menu[1]]
                    GameCanvas.redraw = 1
                    GameCanvas.menu_cursors[0] = i16(GameCanvas.menu[1])
                    GameCanvas.menu_tops[0] = i16(GameCanvas.menu[2])
                    GameCanvas.menu[1] = 0
                    GameCanvas.help_topic = 3
                    return
                w = GameCanvas.menu[1]
                if w == 2:
                    if blocked:
                        GameCanvas.popups.setup_popup(7)
                    elif self.save_game() != 0:
                        GameCanvas.popups.setup_popup(0)
                elif w == 0:
                    GameCanvas.redraw = 1
                    GameCanvas.images[10] = None
                    GameCanvas.images[17] = None
                    GameCanvas.map_mode.mode = 0
                    self.play_sound(-1)
                elif w == 5:
                    GameCanvas.popups.setup_popup(5)
                elif w == 6:
                    GameCanvas.popups.setup_popup(28)
                    GameCanvas.redraw = 1
                return
            if GameCanvas.map_mode.mode == 3:
                self.change_option(1)
                GameCanvas.map_mode.sub = 1
                return
            return
        if v == -7:
            GameCanvas.redraw = 1
            if GameCanvas.map_mode.mode == 1:
                GameCanvas.images[10] = None
                GameCanvas.images[17] = None
                GameCanvas.map_mode.mode = 0
                self.play_sound(-1)
                return
            GameCanvas.map_mode.mode = 1
            GameCanvas.menu[1] = GameCanvas.menu_cursors[0]
            GameCanvas.menu[2] = GameCanvas.menu_tops[0]
            GameCanvas.menu_count = 7

    @staticmethod
    def assign_quick_potion(paramInt):  # ar.java:249-261  (assign the potion under the cursor to * / #)
        cz = GameCanvas.hero
        if cz.quick_slots[GameCanvas.menu[1]].item != 0 and cz.quick_keys[paramInt] != GameCanvas.menu[1]:
            if GameCanvas.menu[1] == cz.quick_keys[paramInt + 1 & 0x1]:
                i = cz.quick_keys[paramInt]
                cz.quick_keys[paramInt] = cz.quick_keys[paramInt + 1 & 0x1]
                cz.quick_keys[paramInt + 1 & 0x1] = i
            else:
                cz.quick_keys[paramInt] = GameCanvas.menu[1]
            return 1
        return 0

    @staticmethod
    def clamp_hero_hp_mp():  # ar.java:263-268
        if GameCanvas.hero.hp > GameCanvas.hero.max_hp:
            GameCanvas.hero.hp = GameCanvas.hero.max_hp
        if GameCanvas.hero.mp > GameCanvas.hero.max_mp:
            GameCanvas.hero.mp = GameCanvas.hero.max_mp

    @staticmethod
    def iabs(paramInt):  # ar.java:270-272
        return -paramInt if paramInt < 0 else paramInt

    def boxes_touch(self, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6, paramInt7, paramInt8):  # ar.java:274-282
        i = idiv(paramInt3 + paramInt7, 2)
        j_ = idiv(paramInt4 + paramInt8, 2)
        k = paramInt1 + idiv(paramInt3, 2) - paramInt5 + idiv(paramInt7, 2)
        m = paramInt2 + idiv(paramInt4, 2) - paramInt6 + idiv(paramInt8, 2)
        n = MapEngine.iabs(k)
        i1 = MapEngine.iabs(m)
        return n < i and i1 < j_

    @staticmethod
    def distance(paramh1, paramh2):  # ar.java:457-468  (distance, rounded)
        j_ = paramh1.x - paramh2.x
        k = paramh1.y - paramh2.y
        m = j_ * j_ + k * k
        j_ = -j_ if j_ < 0 else j_
        k = -k if k < 0 else k
        i = j_ if j_ > k else k
        while i * i < m:
            i += 2
        i -= 1
        if i * i < m:
            i += 1
        return i

    # ---- enemy waves of the room -------------------------------------------------------------

    def spawn_next_enemy(self):  # ar.java:726-741  (spawn the next enemy of the room's wave list eD)
        if config.NO_ENEMIES:
            # PORT-EXTRA (map without combat): the whole wave list of the room counts as
            # defeated at once, and the room is cleared exactly as when its last enemy dies
            # (ar.java:1326-1332): popup "Stage N Complete", then the exits open.
            # A room whose list holds a general (id < 200, c.java:986-1010: talk + duel) stays
            # closed: the mission is won only by defeating him, which is the combat.
            if any(0 < GameCanvas.waves[k] < 200 for k in range(0, 14, 2)):
                return
            if GameCanvas.room_phase == 0 and GameCanvas.waves[0] != 0:
                for b in range(14):
                    GameCanvas.waves[b] = 0
                if GameCanvas.boss_fight != 0:
                    GameCanvas.room_phase = 4
                    GameCanvas.room_phase_timer = 22
                else:
                    GameCanvas.room_phase = 3
                    GameCanvas.room_phase_timer = 5
            return
        if GameCanvas.enemies_alive < GameCanvas.cells[GameCanvas.cell].max_enemies:
            if GameCanvas.waves[0] == 0:
                return
            if (GameCanvas.waves[0] >= 200 or GameCanvas.boss_spawned == 0) and GameCanvas.spawn_spot_count != 0:
                i = self.rand(GameCanvas.spawn_spot_count)
                GameCanvas.scene.create_enemy(GameCanvas.waves[0], GameCanvas.spawn_spots[i].tx, GameCanvas.spawn_spots[i].ty, GameCanvas.spawn_spots[i].dir)
                GameCanvas.waves[1] = i16(GameCanvas.waves[1] - 1)
                if GameCanvas.waves[1] < 1:
                    for b in range(12):
                        GameCanvas.waves[b] = GameCanvas.waves[b + 2]

    @staticmethod
    def skill_mp_cost(paramInt):  # ar.java:743-757  (MP cost of skill paramInt; 0 = not enough MP)
        arrayOfByte1 = [5, 6, 7, 10, 15, 7, 10, 10, 8, 9, 10, 5, 6, 7, 9, 12, 20, 20, 20]
        arrayOfByte2 = [3, 4, 5, 3, 4, 3, 3, 5, 3, 4, 5, 3, 4, 5, 5, 6, 5, 5, 5]
        i = 0
        if 12 <= paramInt <= 30:
            i = arrayOfByte1[paramInt - 12] + (GameCanvas.hero.skill_levels[paramInt - 12] - 1) * arrayOfByte2[paramInt - 12]
        if i > GameCanvas.hero.mp:
            return 0
        GameCanvas.hero.mp -= i
        return i

    @staticmethod
    def check_run():  # ar.java:759-767  (direction pressed twice quickly -> run)
        if GameCanvas.dir_history[0] > -1:
            if GameCanvas.speed >= 3:
                return 1 if (GameCanvas.dir_history[0] == GameCanvas.dir_history[1] or GameCanvas.dir_history[0] == GameCanvas.dir_history[2] or GameCanvas.dir_history[0] == GameCanvas.dir_history[3]) else 0
            if GameCanvas.dir_history[0] == GameCanvas.dir_history[1] or GameCanvas.dir_history[0] == GameCanvas.dir_history[2]:
                return 1
        return 0

    # ---- walls -------------------------------------------------------------------------------

    def step_until_free(self, paramh, paramInt1, paramInt2):  # ar.java:769-815  (step paramInt1 towards paramInt2 until no wall)
        arrayOfInt1 = [0, 0]
        arrayOfInt2 = [0, 0]
        arrayOfInt3 = [0, 0]
        cE = GameCanvas.map
        n = len(cE.data) - 1
        while True:
            b2 = 0
            if paramInt2 == 2:
                arrayOfInt2[0] = idiv(paramh.y - 20, 27)
                arrayOfInt2[1] = idiv(paramh.y + 6, 27)
                arrayOfInt1[1] = arrayOfInt1[0] = idiv(paramh.x + paramInt1 - 12, 27)
            elif paramInt2 == 6:
                arrayOfInt2[0] = idiv(paramh.y - 20, 27)
                arrayOfInt2[1] = idiv(paramh.y + 6, 27)
                arrayOfInt1[1] = arrayOfInt1[0] = idiv(paramh.x + paramInt1 + 12, 27)
            elif paramInt2 == 4:
                arrayOfInt1[0] = idiv(paramh.x - 12, 27)
                arrayOfInt1[1] = idiv(paramh.x + 12, 27)
                arrayOfInt2[1] = arrayOfInt2[0] = idiv(paramh.y + paramInt1 - 20, 27)
            elif paramInt2 == 0:
                arrayOfInt1[0] = idiv(paramh.x - 12, 27)
                arrayOfInt1[1] = idiv(paramh.x + 12, 27)
                arrayOfInt2[1] = arrayOfInt2[0] = idiv(paramh.y + paramInt1 + 6, 27)
            for b1 in range(2):
                arrayOfInt3[b1] = arrayOfInt2[b1] * cE.size.w + arrayOfInt1[b1]
                if (cE.data[min(cE.layer_flags + arrayOfInt3[b1], n)] & 0x1) != 0 or cE.data[min(cE.layer_objects + arrayOfInt3[b1], n)] != 0:
                    b2 += 1
            if b2 != 0:
                paramInt1 = MapEngine.approach_zero(b2, paramInt1)[1]
                if 0 == paramInt1:
                    return 0
                continue
            return paramInt1

    @staticmethod
    def approach_zero(paramInt1, paramInt2):  # ar.java:817-832  (both one step closer to 0)
        if paramInt1 > 0:
            paramInt1 -= 1
        elif paramInt1 < 0:
            paramInt1 += 1
        if paramInt2 > 0:
            paramInt2 -= 1
        elif paramInt2 < 0:
            paramInt2 += 1
        return [paramInt1, paramInt2]

    def keep_in_room(self, paramh, paramInt1, paramInt2):  # ar.java:834-865  (keep inside the room; touching an edge = exit)
        arrayOfShort = [18, 144, 270, 396, 522, 648, 774, 900, 1026, 1152, 1278]
        for b in range(11):
            arrayOfShort[b] = i16(idiv(arrayOfShort[b] * 3, 2))
        h1 = Point()
        h1.x = i16(paramh.x + paramInt1)
        h1.y = i16(paramh.y + paramInt2)
        if h1.x < arrayOfShort[GameCanvas.room_origin.x] + 12:
            paramInt1 = arrayOfShort[GameCanvas.room_origin.x] + 12 - paramh.x
            if GameCanvas.room_phase == 1:
                MapEngine.leave_room(2)
        elif h1.x > arrayOfShort[GameCanvas.room_origin.x + 1] - 12:
            paramInt1 = arrayOfShort[GameCanvas.room_origin.x + 1] - 12 - paramh.x
            if GameCanvas.room_phase == 1:
                MapEngine.leave_room(4)
        if h1.y < arrayOfShort[GameCanvas.room_origin.y] + 10:
            paramInt2 = arrayOfShort[GameCanvas.room_origin.y] + 10 - paramh.y
            if GameCanvas.room_phase == 1:
                MapEngine.leave_room(3)
        elif h1.y > arrayOfShort[GameCanvas.room_origin.y + 1] + 10:
            paramInt2 = arrayOfShort[GameCanvas.room_origin.y + 1] + 10 - paramh.y
            if GameCanvas.room_phase == 1:
                MapEngine.leave_room(1)
        return [paramInt1, paramInt2]

    @staticmethod
    def leave_room(paramInt):  # ar.java:867-888  (leave the room through exit paramInt: 1 down 2 left 3 up 4 right)
        if GameCanvas.room_phase_timer < 0 and GameCanvas.cells[GameCanvas.cell].exits[paramInt - 1] != 0:
            GameCanvas.exit_dir = i16(paramInt)
            if paramInt == 1:
                GameCanvas.cell = i16(GameCanvas.cell + idiv(GameCanvas.map.size.w, 7))
            elif paramInt == 2:
                GameCanvas.cell = i16(GameCanvas.cell - 1)
            elif paramInt == 3:
                GameCanvas.cell = i16(GameCanvas.cell - idiv(GameCanvas.map.size.w, 7))
            elif paramInt == 4:
                GameCanvas.cell = i16(GameCanvas.cell + 1)
            for b in range(4):
                GameCanvas.images[21 + b] = None
            GameCanvas.exit_blink = 0

    @staticmethod
    def slide_corner(paramh, paramInt1, paramInt2):  # ar.java:890-1014  (slide around a corner: new direction or -1)
        cE = GameCanvas.map
        b1 = 0
        j_ = idiv(paramh.x, 27)
        k = idiv(paramh.y, 27)
        m = j_ + k * cE.size.w
        arrayOfInt1 = [0, 0]
        arrayOfInt2 = [1, 1]
        if paramInt2 == -1:
            h1 = GameCanvas.hero.slide_target
        else:
            h1 = GameCanvas.actors[paramInt2].target
        if paramInt1 in (0, 6):
            b1 = 1
        elif paramInt1 in (2, 4):
            b1 = -1
        def free(q):
            return 0 == (cE.data[cE.layer_flags + q] & 0x1) and 0 == cE.data[cE.layer_objects + q]

        if paramInt1 in (0, 4):
            i = m + cE.size.w * b1
            if free(i):
                h1.y = 0
                n = j_ * 27 + 8
                if paramh.x > n:
                    if paramh.x - n > 3:
                        h1.x = -3
                    else:
                        h1.x = i16(n - paramh.x)
                elif n - paramh.x > 3:
                    h1.x = 3
                else:
                    h1.x = i16(n - paramh.x)
                return 8
            for b in range(1, 6):
                if j_ + b < cE.size.w:
                    i = m + b
                    if free(i) and arrayOfInt2[0] != 0:
                        i = m + b + cE.size.w * b1
                        if free(i):
                            arrayOfInt1[0] = 1
                    else:
                        arrayOfInt2[0] = 0
                if j_ - b > -1:
                    i = m - b
                    if free(i) and arrayOfInt2[1] != 0:
                        i = m - b + cE.size.w * b1
                        if free(i):
                            arrayOfInt1[1] = 1
                    else:
                        arrayOfInt2[1] = 0
                if arrayOfInt1[0] != 0 and arrayOfInt1[1] != 0:
                    return 6 if paramh.x - j_ * 27 > 8 else 2
                if arrayOfInt1[0] != 0:
                    return 6
                if arrayOfInt1[1] != 0:
                    return 2
        elif paramInt1 in (2, 6):
            i = m + b1
            if free(i):
                h1.x = 0
                n = k * 27 + 20
                if paramh.y > n:
                    if paramh.y - n > 4:
                        h1.y = -4
                    else:
                        h1.y = i16(n - paramh.y)
                elif n - paramh.y > 4:
                    h1.y = 4
                else:
                    h1.y = i16(n - paramh.y)
                return 8
            for b in range(1, 6):
                if k + b < cE.size.h:
                    i = m + b * cE.size.w
                    if free(i) and arrayOfInt2[0] != 0:
                        i = m + b * cE.size.w + b1
                        if free(i):
                            arrayOfInt1[0] = 1
                    else:
                        arrayOfInt2[0] = 0
                if k - b > -1:
                    i = m - b * cE.size.w
                    if free(i) and arrayOfInt2[1] != 0:
                        i = m - b * cE.size.w + b1
                        if free(i):
                            arrayOfInt1[1] = 1
                    else:
                        arrayOfInt2[1] = 0
                if arrayOfInt1[0] != 0 and arrayOfInt1[1] != 0:
                    return 0 if paramh.y - k * 27 > 8 else 4
                if arrayOfInt1[0] != 0:
                    return 0
                if arrayOfInt1[1] != 0:
                    return 4
        return -1

    @staticmethod
    def straighten_step(paramInt1, paramInt2):  # ar.java:1016-1023  (diagonal step -> straight step)
        arrayOfByte = [[0, 1, 1, 2, 3, 4, 4, 5, 6, 7, 7, 8, 8, 9, 10, 10, 11],
                       [0, 2, 3, 4, 6, 7, 8, 9, 11, 13, 14, 16, 17, 18, 20, 21, 23]]
        if paramInt1 < 0:
            return -arrayOfByte[paramInt2][min(16, -paramInt1)]
        return arrayOfByte[paramInt2][min(16, paramInt1)]

    def move(self, paramh, paramInt1, paramInt2, paramInt3, paramInt4):  # ar.java:1025-1153  (move; returns the direction, -1 blocked, 9 stopped)
        i = 0
        j_ = 0
        if paramInt3 == 8:
            if paramInt4 < 0:
                paramInt1 = GameCanvas.hero.slide_target.x
                paramInt2 = GameCanvas.hero.slide_target.y
            else:
                paramInt1 = GameCanvas.actors[paramInt4].target.x
                paramInt2 = GameCanvas.actors[paramInt4].target.y
        else:
            if paramInt1 > 0:
                i = self.step_until_free(paramh, paramInt1, 6)
            elif paramInt1 < 0:
                i = self.step_until_free(paramh, paramInt1, 2)
            if paramInt2 > 0:
                j_ = self.step_until_free(paramh, paramInt2, 0)
            elif paramInt2 < 0:
                j_ = self.step_until_free(paramh, paramInt2, 4)
        u = MapEngine.straighten_step
        if paramInt3 in (2, 6):
            if 0 == i:
                return -1
        elif paramInt3 in (0, 4):
            if 0 == j_:
                return -1
        elif paramInt3 in (1, 3, 5, 7):
            # diagonal: if one axis is blocked, go straight along the other one
            hx, vy = {1: (2, 0), 3: (2, 4), 5: (6, 4), 7: (6, 0)}[paramInt3]
            if not (i != 0 and j_ != 0):
                if i != 0:
                    paramInt3 = hx
                    i = self.step_until_free(paramh, u(paramInt1, 1), hx)
                elif j_ != 0:
                    paramInt3 = vy
                    j_ = self.step_until_free(paramh, u(paramInt2, 1), vy)
                else:
                    return -1
        elif paramInt3 == 8:
            if paramInt4 == -1:
                h1 = GameCanvas.hero.slide_target
            else:
                h1 = GameCanvas.actors[paramInt4].target
            i = h1.x
            j_ = h1.y
            if h1.x > 0:
                paramInt3 = 6
            elif h1.x < 0:
                paramInt3 = 2
            elif h1.y > 0:
                paramInt3 = 0
            elif h1.y < 0:
                paramInt3 = 4
        arrayOfInt = self.keep_in_room(paramh, i, j_)
        i = arrayOfInt[0]
        j_ = arrayOfInt[1]
        if i != 0 or j_ != 0:
            arrayOfInt = self.blocked_by_actor(paramh, i, j_, paramInt4)
            i = arrayOfInt[0]
            j_ = arrayOfInt[1]
            if i == 0 and j_ == 0:
                return 9
        paramh.x = i16(paramh.x + i)
        paramh.y = i16(paramh.y + j_)
        return paramInt3

    def blocked_by_actor(self, paramh, paramInt1, paramInt2, paramInt3):  # ar.java:1155-1194  (do not walk into the hero / enemies)
        b = 0
        h1 = Point()
        h1.x = i16(paramh.x + paramInt1)
        h1.y = i16(paramh.y + paramInt2)
        if paramInt3 > -1:
            i = MapEngine.distance(h1, GameCanvas.hero.pos[0])
            j_ = MapEngine.distance(paramh, GameCanvas.hero.pos[0])
            if i < j_ and i < 20:
                while MapEngine.iabs(h1.x - GameCanvas.hero.pos[0].x) <= 27 and MapEngine.iabs(h1.y - GameCanvas.hero.pos[0].y) <= 27:
                    MapEngine.approach_zero(paramInt1, paramInt2)       # (result unused in the original)
                    h1.x = i16(paramh.x + paramInt1)
                    h1.y = i16(paramh.y + paramInt2)
                    b += 1
                    if b > 16:
                        break
        else:
            for b1 in range(GameCanvas.actor_count):
                s = GameCanvas.actor_slots[b1]
                if GameCanvas.actors[s].action[0] != 3:
                    i = MapEngine.distance(h1, GameCanvas.actors[s].pos[0])
                    j_ = MapEngine.distance(paramh, GameCanvas.actors[s].pos[0])
                    if i < j_ and i < 20:
                        b = 0
                        while MapEngine.iabs(h1.x - GameCanvas.actors[s].pos[0].x) <= 27 and MapEngine.iabs(h1.y - GameCanvas.actors[s].pos[0].y) <= 27:
                            MapEngine.approach_zero(paramInt1, paramInt2)
                            h1.x = i16(paramh.x + paramInt1)
                            h1.y = i16(paramh.y + paramInt2)
                            b += 1
                            if b > 16:
                                break
        return [paramInt1, paramInt2]

    # ---- the combat: hits ---------------------------------------------------------------------

    def hero_hits_enemy(self, paramInt1, paramInt2):  # ar.java:284-339  (the hero's action paramInt2 hits enemy paramInt1)
        ex = GameCanvas.actors[paramInt1]
        cz = GameCanvas.hero
        ex.hit_fx_kind = 1
        if paramInt2 > -1:
            ex.dir[0] = ex.facing = MapEngine.dir8(ex.pos[0], cz.pos[0])
        else:
            ex.dir[0] = ex.facing = MapEngine.dir8(ex.pos[0], GameCanvas.effect.pos)
        if 3 <= paramInt2 <= 8:
            i = cz.attack + cz.attack_buff - ex.defense - ex.defense_buff
            ex.hp = i16(ex.hp - (i if i > 0 else 1))
        elif paramInt2 in (12, 13, 14) or 20 <= paramInt2 <= 30:
            i = cz.attack + cz.attack_buff + idiv(cz.attack * cz.skill_levels[paramInt2 - 12], consts.skill_attack_div[paramInt2 - 12]) - ex.defense - ex.defense_buff
            ex.hp = i16(ex.hp - (i if i > 0 else 1))
        elif paramInt2 == -2:
            ex.ai_mode = 2
            ex.hp = i16(ex.hp - (50 if cz.level << 1 > 50 else cz.level << 1))
            self.play_sound(4)
        elif paramInt2 == -1:
            ex.hp = i16(ex.hp - (30 if cz.level > 30 else cz.level))
            self.play_sound(3)
        if ex.hp < 1:
            ex.hp = 0
            ex.frame[0] = 3
        else:
            ex.frame[0] = 0
        MapEngine.show_target_info(paramInt1)
        ex.hit_fx_pos = ex.pos[0]
        ex.hit_fx_frame = -1
        ex.action[0] = 2
        if ex.type < 200 and self.rand(1000) < 150 and ex.hp > 0:
            self.general_pick_skill(paramInt1, 1)

    def general_pick_skill(self, paramInt1, paramInt2):  # ar.java:341-368  (a general picks a skill)
        ex = GameCanvas.actors[paramInt1]
        ex.action[0] = i8(6 + GameCanvas.general.skills[self.rand(4)] - 1)
        if ex.action[0] < 6 and ex.action[0] > 21:
            ex.action[0] = 1
        else:
            if ex.action[0] in (9, 10):
                if ex.skill_step > 3:
                    ex.action[0] = 1
                elif ex.max_hp >> 1 > ex.hp:
                    ex.skill_step = i8(ex.skill_step + 1)
                else:
                    ex.action[0] = 1
            elif ex.action[0] in (11, 12, 13):
                if paramInt2 != 0:
                    ex.action[0] = 1
        ex.dir[0] = ex.facing = MapEngine.dir4(ex.pos[0], GameCanvas.hero.pos[0])

    def hero_hits_breakables(self):  # ar.java:370-408  (the hero's attack vs. breakable objects cA)
        cz = GameCanvas.hero
        h_ = Point()
        for b in range(GameCanvas.breakable_count):
            cA = GameCanvas.breakables[b]
            if cA.active != 0 and cA.hp > 0:
                e0 = cz.action[0]
                if e0 == 13:
                    q = cz.dir[0] >> 1
                    if self.boxes_touch(cz.pos[0].x + consts.hit_box_x[q], cz.pos[0].y + consts.hit_box_y[q], consts.hit_box_w[q], consts.hit_box_h[q], cA.pos.x - 8, cA.pos.y - 8, 18, 18):
                        self.hit_breakable(b)
                elif e0 == 22:
                    if MapEngine.is_in_front(cz.pos[0], cA.pos, cz.dir[0]) != 0:
                        self.breakable_hit_if_near(b, consts.weapon_reach[cz.weapon_kind])
                elif e0 in (23, 24):
                    self.breakable_hit_if_near(b, 45)
                elif e0 == 25:
                    if (cz.dir[0] + (cz.frame[0] >> 1 << 1) & 0x7) == MapEngine.dir4(cz.pos[0], cA.pos):
                        self.breakable_hit_if_near(b, consts.weapon_reach[cz.weapon_kind])
                elif e0 in (26, 27):
                    h_.x = i16(cz.pos[0].x + consts.front_dx[cz.dir[0] >> 1])
                    h_.y = i16(cz.pos[0].y + consts.front_dy[cz.dir[0] >> 1])
                    if MapEngine.distance(h_, cA.pos) <= 35:
                        self.hit_breakable(b)
                elif e0 in (28, 29, 30):
                    self.hit_breakable(b)
                else:
                    self.breakable_hit_if_facing(b, consts.weapon_reach[cz.weapon_kind])

    @staticmethod
    def show_target_info(paramInt):  # ar.java:410-421  (message box: enemy name and HP bar)
        ex = GameCanvas.actors[paramInt]
        GameCanvas.message.shown = 1
        GameCanvas.message.ticks = 10
        GameCanvas.message.level = ex.level
        GameCanvas.message.hp_bar = i16(idiv(ex.hp * 60, ex.max_hp))
        if ex.type < 200:
            GameCanvas.message.name = GameCanvas.general.name
            return
        GameCanvas.message.hp_bar = i16(GameCanvas.message.hp_bar >> 1)
        GameCanvas.message.name = consts.troop_names[ex.type - 201]

    @staticmethod
    def is_in_front(paramh1, paramh2, paramInt):  # ar.java:423-443  (is paramh2 in front of paramh1?)
        if paramInt == 2:
            if paramh1.x > paramh2.x:
                return 1
        elif paramInt == 6:
            if paramh1.x < paramh2.x:
                return 1
        elif paramInt == 0:
            if paramh1.y < paramh2.y:
                return 1
        elif paramInt == 4:
            if paramh1.y > paramh2.y:
                return 1
        return 0

    @staticmethod
    def dir4(paramh1, paramh2):  # ar.java:445-449  (direction 0/2/4/6 from paramh1 to paramh2)
        i = paramh2.x - paramh1.x
        j_ = paramh2.y - paramh1.y
        if j_ > i:
            return 0 if j_ > -i else 2
        return 6 if j_ > -i else 4

    @staticmethod
    def dir8(paramh1, paramh2):  # ar.java:451-455  (direction 0..7 from paramh1 to paramh2)
        i = paramh2.x - paramh1.x
        j_ = paramh2.y - paramh1.y
        if i + i < j_:
            if i + i > -j_:
                return 0
            if -i < j_ + j_:
                return 1
            if i < j_ + j_:
                return 2
            return 3
        if i + i < -j_:
            return 4
        if -i > j_ + j_:
            return 5
        if i > j_ + j_:
            return 6
        return 7

    def hero_strike_if_facing(self, paramInt1, paramInt2):  # ar.java:470-473
        if GameCanvas.hero.dir[0] == MapEngine.dir4(GameCanvas.hero.pos[0], GameCanvas.actors[paramInt1].pos[0]):
            self.hero_strike_if_near(paramInt1, paramInt2)

    def general_strike_if_facing(self, paramInt1, paramInt2):  # ar.java:475-478
        if GameCanvas.actors[paramInt1].dir[0] == MapEngine.dir4(GameCanvas.actors[paramInt1].pos[0], GameCanvas.hero.pos[0]):
            self.general_strike_if_near(paramInt1, paramInt2)

    def breakable_hit_if_facing(self, paramInt1, paramInt2):  # ar.java:480-483
        if GameCanvas.hero.dir[0] == MapEngine.dir4(GameCanvas.hero.pos[0], GameCanvas.breakables[paramInt1].pos):
            self.breakable_hit_if_near(paramInt1, paramInt2)

    def hero_strike_if_near(self, paramInt1, paramInt2):  # ar.java:485-488
        if MapEngine.distance(GameCanvas.hero.pos[0], GameCanvas.actors[paramInt1].pos[0]) <= paramInt2:
            self.strike_enemy(paramInt1)

    def general_strike_if_near(self, paramInt1, paramInt2):  # ar.java:490-493
        if MapEngine.distance(GameCanvas.hero.pos[0], GameCanvas.actors[paramInt1].pos[0]) <= paramInt2:
            self.general_skill_hits_hero(paramInt1)

    def breakable_hit_if_near(self, paramInt1, paramInt2):  # ar.java:495-498
        if MapEngine.distance(GameCanvas.hero.pos[0], GameCanvas.breakables[paramInt1].pos) <= paramInt2:
            self.hit_breakable(paramInt1)

    def strike_enemy(self, paramInt):  # ar.java:500-544  (the hero hits enemy paramInt: knock-back A, effects)
        cz = GameCanvas.hero
        ex = GameCanvas.actors[paramInt]
        h_ = Point()
        if ex.action[0] > 5:
            return
        self.hero_hits_enemy(paramInt, cz.action[0])
        if cz.combo > 1 and cz.action[0] < 12:
            ex.ai_mode = 1
        e0 = cz.action[0]
        if e0 == 12:
            cz.frame[0] = 5
            ex.ai_mode = 2
        elif e0 in (14, 22):
            ex.ai_mode = 2
        elif e0 == 20:
            ex.hit_fx_kind = i8(self.rand(2) + 1)
            ex.ai_mode = 0
        elif e0 == 21:
            ex.ai_mode = 5
        elif e0 in (23, 24):
            if e0 == 24:                    # case 24 falls through into case 23
                ex.ai_mode = 5
            self.set_enemy_on_fire(paramInt)
        elif e0 in (25, 26, 27):
            if e0 == 25:                    # 25 -> 27 -> 26 fall through
                ex.ai_mode = 2
            if e0 in (25, 27):
                ex.ai_mode = 5
            ex.hit_fx_kind = 2
            h_.x = i16(cz.pos[0].x + consts.front_dx[cz.dir[0] >> 1])
            h_.y = i16(cz.pos[0].y + consts.front_dy[cz.dir[0] >> 1])
            ex.dir[0] = ex.facing = MapEngine.dir8(ex.pos[0], h_)
        elif e0 == 29:
            self.set_enemy_on_fire(paramInt)
        self.play_sound(16)                       # (`if (A != 0);` - the sound plays always)

    def general_skill_hits_hero(self, paramInt):  # ar.java:546-578  (a general's skill hits the hero)
        cz = GameCanvas.hero
        f0 = GameCanvas.actors[paramInt].action[0]
        if f0 == 6:
            GameCanvas.actors[paramInt].frame[0] = 5
            cz.hurt_ticks = 2
        elif f0 in (8, 16):
            cz.hurt_ticks = 2
        elif f0 == 14:
            cz.hit_fx_kind = self.rand(2) + 1
        elif f0 == 15:
            cz.hurt_ticks = 5
        elif f0 in (17, 18):
            if f0 == 18:                    # case 18 falls through into case 17
                cz.hurt_ticks = 5
            self.set_hero_on_fire()
        elif f0 == 19:
            cz.hurt_ticks = 2
            self.set_hero_on_fire()
        elif f0 in (20, 21):
            if f0 == 21:                    # case 21 falls through into case 20
                cz.hurt_ticks = 5
            cz.hit_fx_kind = 2
        self.hero_is_hit(paramInt)

    def hero_is_hit(self, paramInt):  # ar.java:580-638  (the hero is hit by enemy paramInt, or by arrow paramInt + 3)
        cz = GameCanvas.hero
        if paramInt > -1:
            ex = GameCanvas.actors[paramInt]
            cz.dir[0] = cz.facing = MapEngine.dir8(cz.pos[0], ex.pos[0])
            if ex.action[0] in (6, 7, 8, 14, 15, 16, 17, 18, 19, 20, 21):
                i = ex.attack + ex.attack_buff + idiv(ex.attack, consts.skill_attack_div[ex.action[0] - 6]) - cz.defense - cz.defense_buff
            else:
                i = ex.attack + ex.attack_buff - cz.defense - cz.defense_buff
            i = i if i > 0 else 1
            if cz.hp > i:
                cz.hp -= i
            else:
                cz.hp = 0
        else:
            eC = GameCanvas.arrows[paramInt + 3]
            cz.dir[0] = cz.facing = (eC.dir << 1) + 4 & 0x7
            i = eC.attack - cz.defense - cz.defense_buff
            b = i8(i if i > 0 else 1)
            if cz.hp > b:
                cz.hp -= b
            else:
                cz.hp = 0
        if paramInt > -1:
            MapEngine.show_target_info(paramInt)
        cz.hit_fx_pos = cz.pos[0]
        cz.hit_fx_kind = 1
        cz.hit_fx_frame = -1
        cz.frame[0] = 0
        cz.action[0] = 9
        if cz.hurt_ticks != 0:
            self.play_sound(4)
        else:
            self.play_sound(16)
        if cz.hp < 1:
            cz.hp = 0
            cz.action[0] = 10

    def set_enemy_on_fire(self, paramInt):  # ar.java:640-651  (fire effect on an enemy)
        GameCanvas.actors[paramInt].on_fire = 1
        GameCanvas.actors[paramInt].fire_frame = 0
        GameCanvas.fire_ticks = 7
        self.play_sound(13)
        if GameCanvas.fire_data is None:
            GameCanvas.fire_frames = self.load_frames(60)
            GameCanvas.fire_data = list(consts.fx_fire)

    def set_hero_on_fire(self):  # ar.java:653-661  (fire effect on the hero)
        GameCanvas.hero.on_fire = 1
        GameCanvas.hero.fire_frame = 0
        self.play_sound(13)
        if GameCanvas.hero_fx_data is None:
            GameCanvas.hero_fx_frames = self.load_frames(60)
            GameCanvas.hero_fx_data = consts.fx_fire

    def hit_breakable(self, paramInt):  # ar.java:663-672  (hit a breakable object)
        cA = GameCanvas.breakables[paramInt]
        cA.hp = i16(cA.hp - GameCanvas.hero.attack + GameCanvas.hero.attack_buff)
        self.play_sound(3)
        cA.break_frame = 2
        if cA.hp < 1:
            cA.break_ticks = 12
            i = cA.tile.y * GameCanvas.map.size.w + cA.tile.x
            GameCanvas.map.data[GameCanvas.map.layer_objects + i] = 0

    def hero_attack(self, paramInt):  # ar.java:674-724  (the hero's attack (0) or a scroll (-1/-2) vs. enemies)
        cz = GameCanvas.hero
        h_ = Point()
        for b in range(GameCanvas.actor_count):
            s = GameCanvas.actor_slots[b]
            ex = GameCanvas.actors[s]
            if ex.hp > 0 and ex.alerted != 0 and ex.action[0] < 6:
                if paramInt == 0:
                    e0 = cz.action[0]
                    if e0 == 13:
                        q = cz.dir[0] >> 1
                        if self.boxes_touch(cz.pos[0].x + consts.hit_box_x[q], cz.pos[0].y + consts.hit_box_y[q], consts.hit_box_w[q], consts.hit_box_h[q], ex.pos[0].x - 8, ex.pos[0].y - 8, 17, 17):
                            self.hero_hits_enemy(s, cz.action[0])
                            self.play_sound(3)
                    elif e0 == 22:
                        if MapEngine.is_in_front(cz.pos[0], ex.pos[0], cz.dir[0]) != 0:
                            self.hero_strike_if_near(s, consts.weapon_reach[cz.weapon_kind])
                    elif e0 in (23, 24):
                        self.hero_strike_if_near(s, 45)
                    elif e0 == 25:
                        if (cz.dir[0] + (cz.frame[0] >> 1 << 1) & 0x7) == MapEngine.dir4(cz.pos[0], ex.pos[0]):
                            self.hero_strike_if_near(s, consts.weapon_reach[cz.weapon_kind])
                    elif e0 in (26, 27):
                        h_.x = i16(cz.pos[0].x + consts.front_dx[cz.dir[0] >> 1])
                        h_.y = i16(cz.pos[0].y + consts.front_dy[cz.dir[0] >> 1])
                        if MapEngine.distance(h_, ex.pos[0]) <= 35:
                            self.strike_enemy(s)
                    elif e0 in (28, 29, 30):
                        self.strike_enemy(s)
                    self.hero_strike_if_facing(s, consts.weapon_reach[cz.weapon_kind])
                elif paramInt in (-2, -1):
                    if MapEngine.distance(GameCanvas.effect.pos, ex.pos[0]) <= 35:
                        self.hero_hits_enemy(s, GameCanvas.effect.item)
                        self.play_sound(4)

    def turn_to_nearest(self):  # ar.java:1196-1200  (Normal difficulty, ep = 1: turn to the nearest enemy before the attack)
        if GameCanvas.difficulty != 0 or config.AUTO_AIM_HARD:   # PORT-EXTRA config.AUTO_AIM_HARD: also on Hard
            i = self.nearest_enemy()
            if i > -1:
                GameCanvas.hero.dir[0] = GameCanvas.hero.facing = MapEngine.dir4(GameCanvas.hero.pos[0], GameCanvas.actors[i].pos[0])

    def nearest_enemy(self):  # ar.java:1202-1214  (nearest living enemy closer than 50)
        s = -1
        j_ = 50
        for b in range(GameCanvas.actor_count):
            s1 = GameCanvas.actor_slots[b]
            i = MapEngine.distance(GameCanvas.actors[s1].pos[0], GameCanvas.hero.pos[0])
            if j_ > i and GameCanvas.actors[s1].hp > 0:
                j_ = i
                s = s1
        return s

    # ---- the combat: enemy AI ----------------------------------------------------------------

    def choose_enemy_action(self, paramInt):  # ar.java:1216-1278  (choose the next action of enemy paramInt)
        arrayOfByte = [-2, -1, 0, 0, 0, 0, 1, 2]
        cz = GameCanvas.hero
        ex = GameCanvas.actors[paramInt]
        i = MapEngine.distance(cz.pos[0], ex.pos[0])
        b = 1 if i < 90 else 0
        ex.frame[0] = 0
        j_ = self.rand(1000)
        b1 = MapEngine.dir_to_hero(ex.pos[0])
        if ex.type in (201, 203):
            if j_ < 150 + b * 300:
                ex.action[0] = 0
                ex.dir[0] = ex.facing = i8(b1 + arrayOfByte[j_ & 0x7] & 0x7)
                return
            if j_ < 850 - b * 100:
                if b != 0:
                    if i <= 45 and cz.action[0] != 9 and cz.action[0] != 10 and cz.action[0] < 12:
                        ex.action[0] = 1
                        ex.dir[0] = ex.facing = MapEngine.dir4(ex.pos[0], cz.pos[0])
                        self.hero_is_hit(paramInt)
                        return
                    ex.action[0] = 0
                    ex.dir[0] = ex.facing = i8(b1 + arrayOfByte[j_ & 0x7] & 0x7)
                    return
                ex.action[0] = 0
                ex.dir[0] = ex.facing = i8(ex.dir[0] + arrayOfByte[j_ & 0x7] & 0x7)
                return
            ex.action[0] = 0
            if b != 0:
                ex.dir[0] = ex.facing = i8(j_ & 0x7)
                return
            ex.dir[0] = ex.facing = i8(ex.dir[0] + arrayOfByte[j_ & 0x7] & 0x7)
            return
        if ex.type == 202:
            ex.action[0] = 1
            ex.think_ticks = 15
            MapEngine.shoot_arrow(paramInt)
            return
        if j_ < 150:
            self.general_pick_skill(paramInt, 0)
            return
        if j_ < 350:
            if i <= 60 and (cz.action[0] != 9 or cz.frame[0] >= 6) and cz.action[0] != 10 and cz.action[0] < 12:
                ex.action[0] = 1
                ex.dir[0] = ex.facing = MapEngine.dir4(ex.pos[0], cz.pos[0])
                return
        else:
            ex.dir[0] = ex.facing = b1

    @staticmethod
    def dir_to_hero(paramh):  # ar.java:1280-1284  (direction 0..7 from paramh to the hero, 27 px dead zone)
        i = GameCanvas.hero.pos[0].x - paramh.x
        j_ = GameCanvas.hero.pos[0].y - paramh.y
        if i > 27:
            return 7 if j_ > 27 else (5 if j_ < -27 else 6)
        if i < -27:
            return 1 if j_ > 27 else (3 if j_ < -27 else 2)
        return 0 if j_ > 0 else 4

    @staticmethod
    def shoot_arrow(paramInt):  # ar.java:1286-1308  (an archer shoots an arrow eC)
        arrayOfByte1 = [-1, -15, -1, 5]
        arrayOfByte2 = [-5, -13, -30, -13]
        ex = GameCanvas.actors[paramInt]
        i = ex.dir[0] >> 1
        for b in range(3):
            eC = GameCanvas.arrows[b]
            if eC.active == 0:
                eC.active = 1
                eC.pos[1].x = i16(ex.pos[0].x + arrayOfByte1[i])
                eC.pos[1].y = i16(ex.pos[0].y + arrayOfByte2[i])
                if config.DECOMP_FIX["F18"]:
                    # DECOMP-FIX F18: the start goes into eC.b[1] (the "previous" position used
                    # only for erasing, c.java:124-141), but ar.j() (ar.java:1734-1735) first
                    # copies b[0] -> b[1] and then hits / moves b[0] (ar.ad). b[0] is a separate
                    # h (f.java), so literally every arrow flies from (0, 0) or from where the
                    # previous arrow of this slot vanished: never from the archer, never into
                    # the hero. With F18 the arrow starts at the archer's bow.
                    eC.pos[0].x = eC.pos[1].x
                    eC.pos[0].y = eC.pos[1].y
                eC.dir = i8(i)
                eC.ticks = 0
                eC.attack = ex.attack
                if (i & 0x1) != 0:
                    eC.w = 11
                    eC.h = 2
                    return
                eC.w = 2
                eC.h = 11
                return

    _SHIFT203 = {3: (-10, 0), 1: (-10, 10), 2: (-10, 0), 0: (0, 10), 5: (10, 0), 7: (10, 10), 6: (10, 0)}

    def tick_enemies(self):  # ar.java:1310-1604  (enemy AI: one tick of every enemy)
        arrayOfByte = [20, 20, 25]
        i = 0
        cz = GameCanvas.hero
        # Java `for (b = 0; b < ag.ez; b++)` reads ez every time: ab() below removes the dead
        # enemy from ey and decrements ez inside the loop (and the next enemy is skipped this tick)
        b = -1
        while True:
            b += 1
            if b >= GameCanvas.actor_count:
                break
            s1 = GameCanvas.actor_slots[b]
            ex = GameCanvas.actors[s1]
            ex.action[0] = min(ex.action[0], len(ex.anims[ex.dir[0]]) - 1)
            ex.frame[0] = i8(ex.frame[0] + 1)
            ex.think_ticks = i8(ex.think_ticks - 1)
            s2 = ex.anims[ex.dir[0]][ex.action[0]][ex.frame[0]]
            if ex.attack_buff_ticks > 0:
                ex.attack_buff_ticks = i16(ex.attack_buff_ticks - 1)
                if ex.attack_buff_ticks < 1:
                    ex.attack_buff = 0
            if ex.defense_buff_ticks > 0:
                ex.defense_buff_ticks = i16(ex.defense_buff_ticks - 1)
                if ex.defense_buff_ticks < 1:
                    ex.defense_buff = 0
            if ex.action[0] == 3:
                if s2 > 200:
                    self.enemy_dies(s1)
                    if GameCanvas.enemies_alive < 1 and 0 == GameCanvas.waves[0] and ex.type != 202:
                        if GameCanvas.boss_fight != 0:
                            GameCanvas.room_phase = 4
                            GameCanvas.room_phase_timer = 22
                        else:
                            GameCanvas.room_phase = 3
                            GameCanvas.room_phase_timer = 5
                continue
            if s2 > 200:
                if ex.hp < 1:
                    ex.action[0] = 3
                else:
                    ex.action[0] = 0
                ex.frame[0] = 0
                if ex.type < 200:
                    GameCanvas.enemy_fx_frames = None
                    GameCanvas.enemy_fx_data = None
            if ex.think_ticks < 1:
                ex.alerted = 1
                ex.think_ticks = 6
                if ex.action[0] == 0:
                    self.choose_enemy_action(s1)
            if ex.type == 202:
                ex.dir[0] = ex.facing = MapEngine.dir4(ex.pos[0], cz.pos[0])
                continue
            j_ = ex.facing
            if ex.alerted == 0:
                ex.pos[0].x = i16(ex.pos[0].x + consts.dir_dx8[j_])
                ex.pos[0].y = i16(ex.pos[0].y + consts.dir_dy8[j_])
                continue
            k = m = 0
            f0 = ex.action[0]
            g0 = ex.frame[0]
            e0 = ex.dir[0]
            if f0 == 0:
                k = consts.dir_dx8[j_]
                m = consts.dir_dy8[j_]
            elif f0 in (1, 4, 5):
                k = idiv(consts.dir_dx8[e0], 3)
                m = idiv(consts.dir_dy8[e0], 3)
            elif f0 == 6:
                if 2 < g0 < 6:
                    k = consts.dir_dx8[e0] << 2
                    m = consts.dir_dy8[e0] << 2
            elif f0 in (7, 8):
                fall8 = f0 == 8
                if f0 == 7 and 4 < g0 < 8:
                    k = consts.dir_dx8[e0] << 2
                    m = consts.dir_dy8[e0] << 2
                    if k > 0:
                        k = self.step_until_free(ex.pos[0], k, 6)
                    elif k < 0:
                        k = self.step_until_free(ex.pos[0], k, 2)
                    if m > 0:
                        m = self.step_until_free(ex.pos[0], m, 0)
                    elif m < 0:
                        m = self.step_until_free(ex.pos[0], m, 4)
                    arrayOfInt = self.keep_in_room(ex.pos[0], k, m)
                    k = arrayOfInt[0]
                    m = arrayOfInt[1]
                    ex.pos[0].x = i16(ex.pos[0].x + k)
                    ex.pos[0].y = i16(ex.pos[0].y + m)
                    fall8 = True            # no break: falls into case 8
                if fall8 and 0 < g0 < 9:
                    k = consts.dir_dx8[e0]
                    m = consts.dir_dy8[e0]
            elif f0 == 14:
                if 0 == (g0 & 0x1):
                    k = consts.dir_dx8[e0]
                    m = consts.dir_dy8[e0]
            elif f0 == 2 and ex.ai_mode > 0:
                ex.ai_mode = i8(ex.ai_mode - 1)
                j_ = j_ + 4 & 0x7
                k = consts.dir_dx8[j_] << 2
                m = consts.dir_dy8[j_] << 2
            elif f0 == 2 and g0 == 1:
                j_ = ex.facing + 4 & 0x7
                k = idiv(consts.dir_dx8[j_] * 3, 4)
                m = idiv(consts.dir_dy8[j_] * 3, 4)
            if k != 0 or m != 0:
                if ex.type == 203:
                    arrayOfH = ex.pos
                    dx, dy = MapEngine._SHIFT203.get(j_, (0, 0))
                    arrayOfH[0].x = i16(arrayOfH[0].x + dx)
                    arrayOfH[1].x = i16(arrayOfH[1].x + dx)
                    arrayOfH[0].y = i16(arrayOfH[0].y + dy)
                    arrayOfH[1].y = i16(arrayOfH[1].y + dy)
                    i = self.move(arrayOfH[0], k, m, j_, s1)
                    arrayOfH[0].x = i16(arrayOfH[0].x - dx)
                    arrayOfH[1].x = i16(arrayOfH[1].x - dx)
                    arrayOfH[0].y = i16(arrayOfH[0].y - dy)
                    arrayOfH[1].y = i16(arrayOfH[1].y - dy)
                else:
                    i = self.move(ex.pos[0], k, m, j_, s1)
                if ex.action[0] == 0 and j_ in (0, 2, 4, 6):
                    if i == -1:
                        i = MapEngine.slide_corner(ex.pos[0], ex.facing, s1)
                        if i != -1:
                            self.move(ex.pos[0], consts.dir_dx8[i], consts.dir_dy8[i], i, s1)
            f0 = ex.action[0]
            g0 = ex.frame[0]
            if f0 in (1, 4, 5):
                if g0 == 1:
                    self.enemy_strikes_hero(s1)
            elif f0 == 6:
                if 2 < g0 < 6:
                    self.enemy_strikes_hero(s1)
            elif f0 == 7:
                if 4 < g0 < 8:
                    self.enemy_strikes_hero(s1)
            elif f0 == 8:
                if g0 in (2, 4, 6, 8):
                    self.enemy_strikes_hero(s1)
            elif f0 in (9, 10):
                if g0 == 11:
                    ex.hp = i16(ex.hp + idiv(ex.max_hp * (20 if f0 == 9 else 50), 100))
                    if ex.hp > ex.max_hp:
                        ex.hp = ex.max_hp
            elif f0 in (11, 12, 13):
                if g0 == 11:
                    if f0 != 12:
                        ex.attack_buff = i16(idiv(ex.attack, arrayOfByte[f0 - 11]))
                        if ex.attack_buff < 1:
                            ex.attack_buff = 1
                        ex.attack_buff_ticks = 50
                    if f0 != 11:
                        ex.defense_buff = i16(idiv(ex.defense, arrayOfByte[f0 - 11]))
                        if ex.defense_buff < 1:
                            ex.defense_buff = 1
                        ex.defense_buff_ticks = 50
            elif f0 == 14:
                if (g0 & 0x1) != 0:
                    self.enemy_strikes_hero(s1)
            elif f0 == 15:
                if g0 == 5:
                    self.enemy_strikes_hero(s1)
            elif f0 == 16:
                if g0 == 6:
                    self.enemy_strikes_hero(s1)
            elif f0 in (17, 18):
                if g0 == 5:
                    self.enemy_strikes_hero(s1)
            elif f0 == 19:
                if (g0 & 0x1) != 0:
                    self.enemy_strikes_hero(s1)
            elif f0 in (20, 21):
                if g0 == 8:
                    self.enemy_strikes_hero(s1)

    def enemy_strikes_hero(self, paramInt):  # ar.java:1606-1661  (enemy paramInt strikes the hero)
        cz = GameCanvas.hero
        ex = GameCanvas.actors[paramInt]
        h_ = Point()
        if cz.action[0] != 9 and cz.action[0] != 10:
            if cz.action[0] < 12:
                f0 = ex.action[0]
                if f0 == 7:
                    q = ex.dir[0] >> 1
                    if self.boxes_touch(ex.pos[0].x + consts.hit_box_x[q], ex.pos[0].y + consts.hit_box_y[q], consts.hit_box_w[q], consts.hit_box_h[q], cz.pos[0].x - 8, cz.pos[0].y - 8, 17, 17):
                        self.hero_is_hit(paramInt)
                    return
                if f0 == 16:
                    if MapEngine.is_in_front(ex.pos[0], cz.pos[0], ex.dir[0]) != 0:
                        self.general_strike_if_near(paramInt, consts.general_reach[GameCanvas.general.side])
                    return
                if f0 in (17, 18):
                    self.general_strike_if_near(paramInt, 45)
                    return
                if f0 == 19:
                    if (ex.dir[0] + (ex.frame[0] >> 1 << 1) & 0x7) == MapEngine.dir4(ex.pos[0], cz.pos[0]):
                        self.general_strike_if_near(paramInt, consts.general_reach[GameCanvas.general.side])
                    return
                if f0 in (20, 21):
                    h_.x = i16(ex.pos[0].x + consts.front_dx[ex.dir[0] >> 1])
                    h_.y = i16(ex.pos[0].y + consts.front_dy[ex.dir[0] >> 1])
                    if MapEngine.distance(h_, cz.pos[0]) <= 35:
                        self.general_skill_hits_hero(paramInt)
                    return
                self.general_strike_if_facing(paramInt, consts.general_reach[GameCanvas.general.side])
                return
        elif cz.action[0] == 9:
            f0 = ex.action[0]
            if f0 in (8, 14):
                self.general_strike_if_facing(paramInt, consts.general_reach[GameCanvas.general.side])
                return
            if f0 in (20, 21):
                h_.x = i16(ex.pos[0].x + consts.front_dx[cz.dir[0] >> 1])
                h_.y = i16(ex.pos[0].y + consts.front_dy[cz.dir[0] >> 1])
                if MapEngine.distance(h_, cz.pos[0]) <= 35:
                    self.general_skill_hits_hero(paramInt)

    def enemy_dies(self, paramInt):  # ar.java:1663-1698  (enemy paramInt is dead: exp, drop, remove)
        ex = GameCanvas.actors[paramInt]
        for b in range(GameCanvas.actor_count):
            if GameCanvas.actor_slots[b] == paramInt:
                if ex.type < 200:
                    b1 = 2 if GameCanvas.boss_fight != 0 else 1
                    GameCanvas.mission_exp += ex.level << 1
                    if GameCanvas.general.side != GameCanvas.hero.weapon_kind:
                        GameCanvas.images[40 + GameCanvas.general.side] = None
                    GameCanvas.boss_images[1] = None
                    for b2 in range(3, 9):
                        GameCanvas.enemy_frames[b2] = None
                    GameCanvas.boss_spawned = 0
                else:
                    b1 = 0
                    GameCanvas.mission_exp += ex.level
                self.drop_item(b1, ex.pos[0])
                if ex.type == 203:
                    GameCanvas.hero.kills += 3
                else:
                    GameCanvas.hero.kills += 1
                for b1 in range(b, 6):
                    GameCanvas.actor_slots[b1] = GameCanvas.actor_slots[b1 + 1]
                ex.active = 0
                GameCanvas.actor_count = i16(GameCanvas.actor_count - 1)
                if ex.type != 202:
                    GameCanvas.enemies_alive = i16(GameCanvas.enemies_alive - 1)
                return

    # ---- per-tick updates --------------------------------------------------------------------

    @staticmethod
    def sort_actors():  # ar.java:1700-1711  (sort enemies by y)
        if GameCanvas.actor_count != 0:
            for b in range(GameCanvas.actor_count - 1):
                for i in range(b + 1, GameCanvas.actor_count):
                    if GameCanvas.actors[GameCanvas.actor_slots[b]].pos[0].y > GameCanvas.actors[GameCanvas.actor_slots[i]].pos[0].y:
                        s = GameCanvas.actor_slots[b]
                        GameCanvas.actor_slots[b] = GameCanvas.actor_slots[i]
                        GameCanvas.actor_slots[i] = s

    def pick_up_drops(self):  # ar.java:1713-1729  (pick up dropped items)
        for b in range(GameCanvas.drop_count):
            cC = GameCanvas.drops[b]
            if cC.item != 0:
                if MapEngine.distance(GameCanvas.hero.pos[0], cC.pos) < 20 and self.give_item(cC.item, 1) != 0:
                    GameCanvas.hero_picked_up = 1
                    if 100 < cC.item < 10000:
                        GameCanvas.menus.load_item_def(cC.item)
                        GameCanvas.popups.setup_popup(13)
                    cC.item = 0
                cC.ticks = i16(cC.ticks - 1)
                if cC.ticks < 1:
                    cC.item = 0

    def tick_arrows(self):  # ar.java:1731-1749  (arrows: hit the hero or fly on)
        for b in range(3):
            eC = GameCanvas.arrows[b]
            if eC.active != 0:
                eC.pos[1].x = eC.pos[0].x
                eC.pos[1].y = eC.pos[0].y
                if self.boxes_touch(eC.pos[0].x, eC.pos[0].y + 8, eC.w, eC.h, GameCanvas.hero.pos[0].x - 12, GameCanvas.hero.pos[0].y - 20, 17, 18):
                    if GameCanvas.hero.action[0] < 12:
                        GameCanvas.scene.erase_arrows()
                        eC.active = 0
                        self.hero_is_hit(b - 3)
                    else:
                        self.hero_can_be_hit(b)
                else:
                    self.hero_can_be_hit(b)

    def hero_can_be_hit(self, paramInt):  # ar.java:1751-1772
        e1 = GameCanvas.hero.action[1]
        f1 = GameCanvas.hero.frame[1]
        if e1 in (26, 27):
            if 1 < f1 < 9:
                return
        elif e1 == 28:
            if f1 > 3:
                return
        elif e1 == 29:
            if f1 > 6:
                return
        elif e1 == 30:
            if 3 < f1 < 15:
                return
        MapEngine.move_arrow(paramInt)

    @staticmethod
    def move_arrow(paramInt):  # ar.java:1774-1793  (move an arrow)
        eC = GameCanvas.arrows[paramInt]
        eC.ticks = eC.ticks + 1
        if eC.ticks > 22:
            eC.active = 0
            return
        if eC.dir == 0:
            eC.pos[0].y = i16(eC.pos[0].y + 12)
        elif eC.dir == 1:
            eC.pos[0].x = i16(eC.pos[0].x - 12)
        elif eC.dir == 2:
            eC.pos[0].y = i16(eC.pos[0].y - 12)
        elif eC.dir == 3:
            eC.pos[0].x = i16(eC.pos[0].x + 12)

    def end_tick(self):  # ar.java:1795-1879  (end of tick: previous state, room-change timers)
        cz = GameCanvas.hero
        cz.pos[1] = cz.pos[0]
        cz.room_pos[1] = cz.room_pos[0]
        cz.dir[1] = cz.dir[0]
        cz.dir[0] = cz.facing
        cz.action[1] = cz.action[0]
        cz.frame[1] = cz.frame[0]
        cz.idle_ticks += 1
        GameCanvas.hero_picked_up = 0
        if cz.attack_buff_ticks > 0:
            cz.attack_buff_ticks -= 1
            if cz.attack_buff_ticks < 1:
                cz.attack_buff = 0
            GameCanvas.hero_picked_up = 1
        if cz.defense_buff_ticks > 0:
            cz.defense_buff_ticks -= 1
            if cz.defense_buff_ticks < 1:
                cz.defense_buff = 0
            GameCanvas.hero_picked_up = 1
        GameCanvas.dir_history[4] = GameCanvas.dir_history[3]
        GameCanvas.dir_history[3] = GameCanvas.dir_history[2]
        GameCanvas.dir_history[2] = GameCanvas.dir_history[1]
        GameCanvas.dir_history[1] = GameCanvas.dir_history[0]
        GameCanvas.dir_history[0] = -1
        GameCanvas.screen_fill = 0
        GameCanvas.hero_fx_kind = 0
        if GameCanvas.fire_data is not None:
            GameCanvas.fire_ticks = i16(GameCanvas.fire_ticks - 1)
            if GameCanvas.fire_ticks < 0:
                GameCanvas.fire_frames = None
                GameCanvas.fire_data = None
        for b in range(GameCanvas.actor_count):
            s = GameCanvas.actor_slots[b]
            GameCanvas.actors[s].pos[1] = GameCanvas.actors[s].pos[0]
            GameCanvas.actors[s].dir[1] = GameCanvas.actors[s].dir[0]
            GameCanvas.actors[s].action[1] = GameCanvas.actors[s].action[0]
            GameCanvas.actors[s].frame[1] = GameCanvas.actors[s].frame[0]
        if cz.action[0] in (28, 29, 30):
            if GameCanvas.room_phase != 0:
                GameCanvas.room_phase_timer = 0
            return
        if GameCanvas.room_phase != 0:
            if GameCanvas.room_phase_timer < 1:
                v = GameCanvas.room_phase
                if v == 1:
                    if GameCanvas.exit_dir != 0:
                        GameCanvas.state = 4
                        GameCanvas.room_phase = 0
                        GameCanvas.exit_blink = 1
                    if 0 == GameCanvas.room_phase_timer:
                        GameCanvas.exit_blink = 2
                        for b in range(4):
                            if GameCanvas.cells[GameCanvas.cell].exits[b] != 0:
                                GameCanvas.images[21 + b] = self.load_image(GameCanvas.scr_ui.get(17 + b))
                        GameCanvas.room_phase_timer = i16(GameCanvas.room_phase_timer - 1)
                        return
                elif v == 2:
                    GameCanvas.popups.setup_popup(8)
                    GameCanvas.room_phase = 0
                    return
                elif v == 3:
                    GameCanvas.popups.setup_popup(9)
                    GameCanvas.room_phase = 0
                    return
                elif v == 4:
                    GameCanvas.popups.setup_popup(10)
                    GameCanvas.room_phase = 0
                return
            GameCanvas.room_phase_timer = i16(GameCanvas.room_phase_timer - 1)
            if GameCanvas.room_phase == 3 and GameCanvas.room_phase_timer == 0 and GameCanvas.sound is not None:
                GameCanvas.stop_sound()

    def tick_mission_clock(self, paramInt):  # ar.java:1881-1890  (mission clock dX, paused while a popup / menu is open)
        GameCanvas.clock[0] = GameCanvas.now()
        if paramInt == 0 or GameCanvas.clock[0] - GameCanvas.clock[1] > 1000:
            GameCanvas.play_time += GameCanvas.clock[0] - GameCanvas.clock[1]
        else:
            l_ = GameCanvas.clock[0] - GameCanvas.play_time
            GameCanvas.mission_seconds = int(l_ // 1000)
        GameCanvas.clock[1] = GameCanvas.clock[0]

    def scroll_room(self):  # ar.java:1892-1932  (bV = 4: scroll to the next room, 6 steps)
        v = GameCanvas.exit_dir
        if v == 1:
            GameCanvas.view_ty += 7
        elif v == 2:
            GameCanvas.view_tx -= 7
        elif v == 3:
            GameCanvas.view_ty -= 7
        elif v == 4:
            GameCanvas.view_tx += 7
        if v in (1, 2, 3, 4):
            GameCanvas.exit_blink = i16(GameCanvas.exit_blink + 6)
            GameCanvas.scene.draw_tiles(GameCanvas.view_tiles.x, GameCanvas.view_tiles.y, GameCanvas.view_tx, GameCanvas.view_ty, 0)
        self.draw_view_region(GameCanvas.images[7], GameCanvas.view_x, GameCanvas.view_y, GameCanvas.view_size.x, GameCanvas.view_size.y, GameCanvas.view_offset.x, GameCanvas.view_offset.y)
        arrayOfInt = self.keep_in_room(GameCanvas.hero.pos[0], 0, 0)
        GameCanvas.hero.pos[0].x = i16(GameCanvas.hero.pos[0].x + arrayOfInt[0])
        GameCanvas.hero.pos[0].y = i16(GameCanvas.hero.pos[0].y + arrayOfInt[1])
        GameCanvas.scene.draw_actors()
        if GameCanvas.exit_blink > 1:
            self.play_sound(-1)
        if GameCanvas.exit_blink > 6:
            GameCanvas.state = 3
            GameCanvas.redraw = 1
            GameCanvas.exit_dir = 0
            GameCanvas.rooms_visited = i16(GameCanvas.rooms_visited + 1)
            GameCanvas.room_phase = 2
            GameCanvas.room_phase_timer = 1
            self.load_enemy_sprites()
        GameCanvas.exit_blink = i16(GameCanvas.exit_blink + 1)

    # ---- drawing helpers ---------------------------------------------------------------------

    def draw_spark(self, paramInt1, paramInt2, paramInt3):  # ar.java:1934-1936  (hit spark eV)
        v_ = GameCanvas.spark_frames[paramInt1]
        self.draw_map_region(GameCanvas.images[43], paramInt2 - v_.ox, paramInt3 - v_.oy, v_.w, v_.h, v_.src_x, v_.src_y)

    def draw_hero_weapon(self, paramInt1, paramInt2, paramy):  # ar.java:1938-1941  (the hero's weapon)
        self.draw_map_region(GameCanvas.images[40 + GameCanvas.hero.weapon_kind], paramInt1 - paramy.ox, paramInt2 - paramy.oy, paramy.w, paramy.h, paramy.src_x, paramy.src_y)
        MapScene.mark_dirty(GameCanvas.hero.pos[0].x - paramy.ox, GameCanvas.hero.pos[0].y - paramy.oy, paramy.w, paramy.h)

    def draw_weapon_trail(self, paramInt1, paramInt2):  # ar.java:1943-1969  (weapon trail of the hero (-1) or an enemy)
        if paramInt1 > -1:
            h_ = GameCanvas.actors[paramInt1].pos[0]
            if GameCanvas.actors[paramInt1].action[0] == 19:
                i = GameCanvas.actors[paramInt1].dir[0] + (GameCanvas.actors[paramInt1].frame[0] >> 1 << 1) & 0x7
            else:
                i = GameCanvas.actors[paramInt1].dir[0]
        else:
            h_ = GameCanvas.hero.pos[0]
            if GameCanvas.hero.action[0] == 25:
                i = GameCanvas.hero.dir[0] + (GameCanvas.hero.frame[0] >> 1 << 1) & 0x7
            else:
                i = GameCanvas.hero.dir[0]
        j_ = (i >> 1) * 6 + (paramInt2 << 1)
        k = h_.x - GameCanvas.camera.x
        m = h_.y - GameCanvas.camera.y
        for b in range(2):
            u = GameCanvas.trail_frames[j_]
            self.draw_map_region(GameCanvas.images[42], k - u.ox, m - u.oy, u.w, u.h, u.src_x, u.src_y)
            MapScene.mark_dirty(h_.x - u.ox, h_.y - u.oy, u.w, u.h)
            j_ += 1

    def draw_object_layer(self):  # ar.java:1971-1983  (object layer over dirty cells)
        cE = GameCanvas.map
        for b in range(GameCanvas.view_tiles.x):
            for b1 in range(GameCanvas.view_tiles.y):
                if GameCanvas.dirty[b1][b] != 0:
                    i = (GameCanvas.view_ty + b1) * cE.size.w + GameCanvas.view_tx + b
                    if cE.data[cE.layer_objects + i] != 0:
                        j_ = GameCanvas.tile_slots[cE.data[cE.layer_objects + i] - 1] - 1
                        self.draw_map_region(GameCanvas.tile_images[j_], (GameCanvas.view_tx + b) * 27 - GameCanvas.camera.x, (GameCanvas.view_ty + b1) * 27 - GameCanvas.camera.y, 27, 27, 0, 0)

    def draw_drops(self):  # ar.java:1985-2015  (dropped items; objects being broken)
        for b in range(GameCanvas.drop_count):
            cC = GameCanvas.drops[b]
            if cC.item != 0:
                self.draw_map_region(cC.image, cC.pos.x - GameCanvas.camera.x - (cC.w >> 1), cC.pos.y - GameCanvas.camera.y - (cC.h >> 1), cC.w, cC.h, cC.w * cC.frame, 0)
                MapScene.mark_dirty(cC.pos.x - (cC.w >> 1), cC.pos.y - (cC.h >> 1), cC.w, cC.h)
        for b in range(GameCanvas.breakable_count):
            cA = GameCanvas.breakables[b]
            if cA.active != 0 and cA.break_ticks != 0:
                cA.break_ticks = i16(cA.break_ticks - 1)
                if (cA.break_ticks & 0x2) != 0:
                    self.draw_map_region(GameCanvas.tile_images[cA.image], cA.tile.x * 27 - GameCanvas.camera.x, cA.tile.y * 27 - GameCanvas.camera.y, 27, 27, 0, 0)
                else:
                    i = cA.tile.x * 27 - GameCanvas.camera.x
                    j_ = cA.tile.y * 27 - GameCanvas.camera.y
                    if GameCanvas.images[7] is not None and i + GameCanvas.view_offset.x >= 0:
                        if i + GameCanvas.view_offset.x > GameCanvas.images[7].getWidth():
                            return
                        self.draw_map_region(GameCanvas.images[7], i, j_, 27, 27, i + GameCanvas.view_offset.x, j_ + GameCanvas.view_offset.y)
                    else:
                        break
                if 0 == cA.break_ticks:
                    self.drop_item(3, cA.pos)
                    cA.active = 0

    def drop_item(self, paramInt, paramh):  # ar.java:2017-2053  (drop an item at paramh)
        s1 = paramh.x
        s2 = paramh.y
        if s2 <= GameCanvas.camera.y + 27 or s2 >= GameCanvas.camera.y + 162 or s1 <= GameCanvas.camera.x + 27 or s1 >= GameCanvas.camera.x + 162:
            return
        s3 = self.random_drop(paramInt)
        if s3 != 0:
            i = idiv(s2, 27) * GameCanvas.map.size.w + idiv(s1, 27)
            if 0 == (GameCanvas.map.data[GameCanvas.map.layer_flags + i] & 0x1):
                b = 0
                while b < 10 and GameCanvas.drops[b].item != 0:
                    b += 1
                if b > 9:
                    return
                cC = GameCanvas.drops[b]
                cC.item = s3
                if cC.pos is None:
                    cC.pos = Point()
                cC.pos.x = s1
                cC.pos.y = s2
                cC.ticks = 75
                cC.w = cC.h = 28
                if s3 > 10000:
                    cC.image = GameCanvas.images[32]
                    cC.frame = 0
                    cC.w = i16(GameCanvas.images[32].getWidth())
                    cC.h = i16(GameCanvas.images[32].getHeight())
                elif s3 > 100:
                    cC.image = GameCanvas.images[0]
                    cC.frame = 11
                else:
                    cC.image = GameCanvas.images[0]
                    cC.frame = i16(s3 - 1)
                if b >= GameCanvas.drop_count:
                    GameCanvas.drop_count = i16(GameCanvas.drop_count + 1)

    def random_drop(self, paramInt):  # ar.java:2055-2078  (random drop: item id, potion, or gold 10020/10040)
        C = self.rand
        arrayOfByte1 = [5, 10, 20, 5, 100]
        arrayOfByte2 = [10, 30, 60, 1, 100]
        arrayOfByte3 = [69, 44, 24, 9, 0]
        arrayOfByte = [[0, 0, 33, 77, 100], [5, 30, 55, 80, 100], [30, 60, 90, 100, 100],
                       [40, 80, 100, 100, 100], [80, 100, 100, 100, 100]]
        if C(100) < arrayOfByte1[paramInt]:
            i = C(100)
            if i < arrayOfByte2[paramInt]:
                # PORT-EXTRA config.DROPS_AFTER_69: row 0 (above Lv69: no Lv1 / Lv10 gear) is skipped,
                # so a hero above Lv69 keeps the odds of Lv45-69
                for b in range(1 if config.DROPS_AFTER_69 else 0, 5):
                    if GameCanvas.hero.level > arrayOfByte3[b]:
                        i = C(100)
                        for b1 in range(5):
                            if i < arrayOfByte[b][b1]:
                                return i16(101 + b1 + 5 * C(20))
            else:
                return i16(C(11) + 1)
        elif C(100) < 25:
            return i16(10020 + (GameCanvas.difficulty ^ 0x1) * 20)
        return 0

    def draw_quick_potions(self):  # ar.java:2081-2089  (the two quick potions * and # of the HUD)
        cz = GameCanvas.hero
        for b in range(2):
            z = cz.quick_slots[cz.quick_keys[b]]
            if z.item != 0:
                GameCanvas.draw_region(GameCanvas.view_cx + (2 * b - 1) * (44 + 28 * (1 - b) + 0), GameCanvas.canvas_size.y - 33 - 0 - 17, 28, 28, GameCanvas.images[0], (z.item - 1) * 28, 0)
                GameCanvas.draw_region(GameCanvas.view_cx + (2 * b - 1) * (38 + 11 * (1 - b) + 0), GameCanvas.canvas_size.y - 16 - 0 - 17, 11, 12, GameCanvas.images[20], 98, 0)
                self.draw_number_commas(z.count, GameCanvas.view_cx + (2 * b - 1) * (28 + 10 * b + 0), GameCanvas.canvas_size.y - 18 - 0 - 17)

    def draw_hud(self):  # ar.java:2091-2107  (HUD of the map: balls, gold, potions, clock, soft keys)
        GameCanvas.scene.draw_hud_balls()
        if GameCanvas.message.shown != 0:
            self.draw_message()
        else:
            self.draw_number_commas(GameCanvas.hero.kills_shown, GameCanvas.view_size.x - 4 - 7, 20)
        if config.SKILL_BAR:
            # PORT-EXTRA config.SKILL_BAR: the belt above shows all 5 slots, so the * / # boxes of
            # the frame stay empty (ar.aD is not drawn)
            from pow.game import skill_bar   # PORT-EXTRA config.SKILL_BAR: belt and skill slots
            skill_bar.draw_bar()
        else:
            self.draw_quick_potions()
        self.draw_clock(0, 5, GameCanvas.mission_seconds)
        if GameCanvas.state == 3 and GameCanvas.popups.kind == 0:
            if GameCanvas.map_mode.mode != 0:
                GameCanvas.draw_softkeys(-1, 9)
                return
            GameCanvas.draw_softkeys(-1, 1)

    def draw_message(self):  # ar.java:2109-2141  (message box dT: item picked up)
        GameCanvas.text_width = GameCanvas.measure_text(GameCanvas.message.name)
        i = GameCanvas.view_size.x - GameCanvas.font_white.chars_width(list(GameCanvas.message.name), 0, len(GameCanvas.message.name)) - 8
        Gfx.set_font(GameCanvas.font_black)
        GameCanvas.draw_view_text(GameCanvas.message.name, i, 3)
        GameCanvas.draw_view_text(GameCanvas.message.name, i - 1, 2)
        GameCanvas.draw_view_text(GameCanvas.message.name, i + 1, 2)
        GameCanvas.draw_view_text(GameCanvas.message.name, i, 1)
        Gfx.set_font(GameCanvas.font_white)
        GameCanvas.draw_view_text(GameCanvas.message.name, i, 2)
        GameCanvas.text_width = GameCanvas.digit_count(GameCanvas.message.level)
        ct31 = GameCanvas.images[31]
        self.draw_map_region(ct31, GameCanvas.view_size.x - ct31.getWidth() - 27 - 5 - 7, 2 + GameCanvas.font_white.height(), ct31.getWidth(), ct31.getHeight(), 0, 0)
        self.draw_image_part(GameCanvas.message.level, GameCanvas.view_size.x - 15, 1 + GameCanvas.font_white.height() + 17, 9, 12, GameCanvas.images[20], 0, 0, -1)
        if GameCanvas.message.hp_bar > 0:
            ac_ = Rect(GameCanvas.view_size.x - 62 + GameCanvas.view_x - 7, 2 + GameCanvas.font_white.height() + 12 + GameCanvas.view_y, 62 if GameCanvas.message.hp_bar > 62 else GameCanvas.message.hp_bar, 7)
            GameCanvas.fill_rect(ac_, GameCanvas.rgb(0, 0, 0))
            ac_.y += 1
            ac_.h = 5
            ac_.x += 1
            ac_.w -= 2
            GameCanvas.fill_rect(ac_, GameCanvas.rgb(107, 0, 0))
            ac_.y += 1
            ac_.h = 3
            GameCanvas.fill_rect(ac_, GameCanvas.rgb(181, 0, 0))
            ac_.y += 1
            ac_.h = 1
            GameCanvas.fill_rect(ac_, GameCanvas.rgb(255, 73, 0))
        MapScene.mark_dirty(GameCanvas.camera.x + 170, GameCanvas.camera.y, 68, 40)
