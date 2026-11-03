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

    def draw_map(self, mode):  # ar.java:25-93  (draw the map, its pause menu and popups)
        if mode == 1:
            self.draw_view_background()
            for b in range(9):
                for row in range(9):
                    GameCanvas.dirty[b][row] = 1
            GameCanvas.scene.draw_frame()
            if GameCanvas.map_mode.mode != 0:
                GameCanvas.popups.draw_popup_frame(170)
                map_mode = GameCanvas.map_mode.mode
                if map_mode == 1:
                    GameCanvas.menus.draw_list_menu()
                elif map_mode == 2:
                    GameCanvas.menus.draw_assign_items(0)
                    GameCanvas.menus.draw_description_strip()
                elif map_mode == 3:
                    GameCanvas.menus.draw_options()
                elif map_mode == 4:
                    GameCanvas.menus.draw_help_page()
            if GameCanvas.popups.kind != 0:
                GameCanvas.popups.draw_popup()
                GameCanvas.menus.draw_popup_extras()
            return
        if mode == 2:
            return
        if GameCanvas.popups.kind != 0:
            if GameCanvas.popups.popup_redraw != 0:
                GameCanvas.popups.draw_popup()
            GameCanvas.menus.draw_popup_extras()
            return
        if GameCanvas.map_mode.mode != 0:
            if GameCanvas.map_mode.sub != 0:
                map_mode = GameCanvas.map_mode.mode
                if map_mode == 1:
                    GameCanvas.popups.draw_popup_frame(170)
                    GameCanvas.menus.draw_list_menu()
                elif map_mode == 2:
                    GameCanvas.menus.draw_assign_items(1)
                elif map_mode == 3:
                    GameCanvas.popups.draw_popup_frame(170)
                    GameCanvas.menus.draw_options()
                elif map_mode == 4:
                    GameCanvas.popups.draw_popup_frame(170)
                    GameCanvas.menus.draw_help_page()
                GameCanvas.map_mode.sub = 0
            if GameCanvas.map_mode.mode == 2:
                GameCanvas.menus.draw_description_strip()
                return
        else:
            GameCanvas.scene.draw_frame()

    def pause_menu_keys(self):  # ar.java:95-247  (keys of the pause menu cR.a: 1 menu, 2 items, 3 options, 4 help)
        sub_modes = [0, 3, 0, 2, 4, 0, 0]
        sub_sizes = [0, consts.menu_sizes[9], 0, 5, 3, 0, 0]    # Options: 3 rows (+1 with config.SCREEN_OPTION)
        key = GameCanvas.key
        blocked = GameCanvas.actor_count > 0 or GameCanvas.boss_fight != 0 or GameCanvas.waves[0] != 0
        if key in (-1, 50):
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
        if key in (-2, 56):
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
        if key in (-3, 52):
            if GameCanvas.map_mode.mode in (2, 4):
                GameCanvas.menu[1] = GameCanvas.menu[1] - 1
                if (GameCanvas.menu[1] < 0) if F6 else (GameCanvas.menu[1] - 1 < 0):   # DECOMP-FIX F6
                    GameCanvas.menu[1] = GameCanvas.menu_count - 1
                GameCanvas.map_mode.sub = 1
            elif GameCanvas.map_mode.mode == 3:
                self.change_option(0)
                GameCanvas.map_mode.sub = 1
            return
        if key in (-4, 54):
            if GameCanvas.map_mode.mode in (2, 4):
                GameCanvas.menu[1] = GameCanvas.menu[1] + 1
                if (GameCanvas.menu[1] >= GameCanvas.menu_count) if F6 else (GameCanvas.menu[1] + 1 >= GameCanvas.menu_count):   # DECOMP-FIX F6
                    GameCanvas.menu[1] = 0
                GameCanvas.map_mode.sub = 1
            elif GameCanvas.map_mode.mode == 3:
                self.change_option(1)
                GameCanvas.map_mode.sub = 1
            return
        if key == 42:
            if GameCanvas.map_mode.mode == 2:
                GameCanvas.redraw = MapEngine.assign_quick_potion(0)
            return
        if key == 35:
            if GameCanvas.map_mode.mode == 2:
                GameCanvas.redraw = MapEngine.assign_quick_potion(1)
            return
        if key in (-5, 53):
            if GameCanvas.menu[0] == 10 and GameCanvas.menu[1] == 4:
                GameCanvas.menu[0] = 5
                GameCanvas.menu[1] = 3
                GameCanvas.prev_state = GameCanvas.state
                GameCanvas.state = 2
                GameCanvas.menus.key_fire()
                return
            if GameCanvas.map_mode.mode == 1:
                if sub_modes[GameCanvas.menu[1]] != 0:
                    GameCanvas.map_mode.mode = sub_modes[GameCanvas.menu[1]]
                    GameCanvas.menu_count = sub_sizes[GameCanvas.menu[1]]
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
        if key == -7:
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
    def assign_quick_potion(key_slot):  # ar.java:249-261  (assign the potion under the cursor to * / #)
        cz = GameCanvas.hero
        if cz.quick_slots[GameCanvas.menu[1]].item != 0 and cz.quick_keys[key_slot] != GameCanvas.menu[1]:
            if GameCanvas.menu[1] == cz.quick_keys[key_slot + 1 & 0x1]:
                i = cz.quick_keys[key_slot]
                cz.quick_keys[key_slot] = cz.quick_keys[key_slot + 1 & 0x1]
                cz.quick_keys[key_slot + 1 & 0x1] = i
            else:
                cz.quick_keys[key_slot] = GameCanvas.menu[1]
            return 1
        return 0

    @staticmethod
    def clamp_hero_hp_mp():  # ar.java:263-268
        if GameCanvas.hero.hp > GameCanvas.hero.max_hp:
            GameCanvas.hero.hp = GameCanvas.hero.max_hp
        if GameCanvas.hero.mp > GameCanvas.hero.max_mp:
            GameCanvas.hero.mp = GameCanvas.hero.max_mp

    @staticmethod
    def iabs(value):  # ar.java:270-272
        return -value if value < 0 else value

    def boxes_touch(self, x1, y1, w1, h1, x2, y2, w2, h2):  # ar.java:274-282
        max_dx = idiv(w1 + w2, 2)
        max_dy = idiv(h1 + h2, 2)
        dx = x1 + idiv(w1, 2) - x2 + idiv(w2, 2)
        dy = y1 + idiv(h1, 2) - y2 + idiv(h2, 2)
        abs_dx = MapEngine.iabs(dx)
        abs_dy = MapEngine.iabs(dy)
        return abs_dx < max_dx and abs_dy < max_dy

    @staticmethod
    def distance(a, b):  # ar.java:457-468  (distance, rounded)
        dx = a.x - b.x
        dy = a.y - b.y
        dist2 = dx * dx + dy * dy
        dx = -dx if dx < 0 else dx
        dy = -dy if dy < 0 else dy
        i = dx if dx > dy else dy
        while i * i < dist2:
            i += 2
        i -= 1
        if i * i < dist2:
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
    def skill_mp_cost(skill):  # ar.java:743-757  (MP cost of skill paramInt; 0 = not enough MP)
        base_cost = [5, 6, 7, 10, 15, 7, 10, 10, 8, 9, 10, 5, 6, 7, 9, 12, 20, 20, 20]
        cost_per_level = [3, 4, 5, 3, 4, 3, 3, 5, 3, 4, 5, 3, 4, 5, 5, 6, 5, 5, 5]
        i = 0
        if 12 <= skill <= 30:
            i = base_cost[skill - 12] + (GameCanvas.hero.skill_levels[skill - 12] - 1) * cost_per_level[skill - 12]
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

    def step_until_free(self, pos, step, dir):  # ar.java:769-815  (step paramInt1 towards paramInt2 until no wall)
        cols = [0, 0]
        rows = [0, 0]
        cells = [0, 0]
        cE = GameCanvas.map
        last = len(cE.data) - 1
        while True:
            walls = 0
            if dir == 2:
                rows[0] = idiv(pos.y - 20, 27)
                rows[1] = idiv(pos.y + 6, 27)
                cols[1] = cols[0] = idiv(pos.x + step - 12, 27)
            elif dir == 6:
                rows[0] = idiv(pos.y - 20, 27)
                rows[1] = idiv(pos.y + 6, 27)
                cols[1] = cols[0] = idiv(pos.x + step + 12, 27)
            elif dir == 4:
                cols[0] = idiv(pos.x - 12, 27)
                cols[1] = idiv(pos.x + 12, 27)
                rows[1] = rows[0] = idiv(pos.y + step - 20, 27)
            elif dir == 0:
                cols[0] = idiv(pos.x - 12, 27)
                cols[1] = idiv(pos.x + 12, 27)
                rows[1] = rows[0] = idiv(pos.y + step + 6, 27)
            for i in range(2):
                cells[i] = rows[i] * cE.size.w + cols[i]
                if (cE.data[min(cE.layer_flags + cells[i], last)] & 0x1) != 0 or cE.data[min(cE.layer_objects + cells[i], last)] != 0:
                    walls += 1
            if walls != 0:
                step = MapEngine.approach_zero(walls, step)[1]
                if 0 == step:
                    return 0
                continue
            return step

    @staticmethod
    def approach_zero(dx, dy):  # ar.java:817-832  (both one step closer to 0)
        if dx > 0:
            dx -= 1
        elif dx < 0:
            dx += 1
        if dy > 0:
            dy -= 1
        elif dy < 0:
            dy += 1
        return [dx, dy]

    def keep_in_room(self, pos, dx, dy):  # ar.java:834-865  (keep inside the room; touching an edge = exit)
        edges = [18, 144, 270, 396, 522, 648, 774, 900, 1026, 1152, 1278]
        for b in range(11):
            edges[b] = i16(idiv(edges[b] * 3, 2))
        dest = Point()
        dest.x = i16(pos.x + dx)
        dest.y = i16(pos.y + dy)
        if dest.x < edges[GameCanvas.room_origin.x] + 12:
            dx = edges[GameCanvas.room_origin.x] + 12 - pos.x
            if GameCanvas.room_phase == 1:
                MapEngine.leave_room(2)
        elif dest.x > edges[GameCanvas.room_origin.x + 1] - 12:
            dx = edges[GameCanvas.room_origin.x + 1] - 12 - pos.x
            if GameCanvas.room_phase == 1:
                MapEngine.leave_room(4)
        if dest.y < edges[GameCanvas.room_origin.y] + 10:
            dy = edges[GameCanvas.room_origin.y] + 10 - pos.y
            if GameCanvas.room_phase == 1:
                MapEngine.leave_room(3)
        elif dest.y > edges[GameCanvas.room_origin.y + 1] + 10:
            dy = edges[GameCanvas.room_origin.y + 1] + 10 - pos.y
            if GameCanvas.room_phase == 1:
                MapEngine.leave_room(1)
        return [dx, dy]

    @staticmethod
    def leave_room(exit_no):  # ar.java:867-888  (leave the room through exit paramInt: 1 down 2 left 3 up 4 right)
        if GameCanvas.room_phase_timer < 0 and GameCanvas.cells[GameCanvas.cell].exits[exit_no - 1] != 0:
            GameCanvas.exit_dir = i16(exit_no)
            if exit_no == 1:
                GameCanvas.cell = i16(GameCanvas.cell + idiv(GameCanvas.map.size.w, 7))
            elif exit_no == 2:
                GameCanvas.cell = i16(GameCanvas.cell - 1)
            elif exit_no == 3:
                GameCanvas.cell = i16(GameCanvas.cell - idiv(GameCanvas.map.size.w, 7))
            elif exit_no == 4:
                GameCanvas.cell = i16(GameCanvas.cell + 1)
            for b in range(4):
                GameCanvas.images[21 + b] = None
            GameCanvas.exit_blink = 0

    @staticmethod
    def slide_corner(pos, dir, actor):  # ar.java:890-1014  (slide around a corner: new direction or -1)
        cE = GameCanvas.map
        side_dir = 0
        tx = idiv(pos.x, 27)
        ty = idiv(pos.y, 27)
        cell = tx + ty * cE.size.w
        free_side = [0, 0]
        open_side = [1, 1]
        if actor == -1:
            slide = GameCanvas.hero.slide_target
        else:
            slide = GameCanvas.actors[actor].target
        if dir in (0, 6):
            side_dir = 1
        elif dir in (2, 4):
            side_dir = -1
        def free(q):
            return 0 == (cE.data[cE.layer_flags + q] & 0x1) and 0 == cE.data[cE.layer_objects + q]

        if dir in (0, 4):
            i = cell + cE.size.w * side_dir
            if free(i):
                slide.y = 0
                edge = tx * 27 + 8
                if pos.x > edge:
                    if pos.x - edge > 3:
                        slide.x = -3
                    else:
                        slide.x = i16(edge - pos.x)
                elif edge - pos.x > 3:
                    slide.x = 3
                else:
                    slide.x = i16(edge - pos.x)
                return 8
            for b in range(1, 6):
                if tx + b < cE.size.w:
                    i = cell + b
                    if free(i) and open_side[0] != 0:
                        i = cell + b + cE.size.w * side_dir
                        if free(i):
                            free_side[0] = 1
                    else:
                        open_side[0] = 0
                if tx - b > -1:
                    i = cell - b
                    if free(i) and open_side[1] != 0:
                        i = cell - b + cE.size.w * side_dir
                        if free(i):
                            free_side[1] = 1
                    else:
                        open_side[1] = 0
                if free_side[0] != 0 and free_side[1] != 0:
                    return 6 if pos.x - tx * 27 > 8 else 2
                if free_side[0] != 0:
                    return 6
                if free_side[1] != 0:
                    return 2
        elif dir in (2, 6):
            i = cell + side_dir
            if free(i):
                slide.x = 0
                edge = ty * 27 + 20
                if pos.y > edge:
                    if pos.y - edge > 4:
                        slide.y = -4
                    else:
                        slide.y = i16(edge - pos.y)
                elif edge - pos.y > 4:
                    slide.y = 4
                else:
                    slide.y = i16(edge - pos.y)
                return 8
            for b in range(1, 6):
                if ty + b < cE.size.h:
                    i = cell + b * cE.size.w
                    if free(i) and open_side[0] != 0:
                        i = cell + b * cE.size.w + side_dir
                        if free(i):
                            free_side[0] = 1
                    else:
                        open_side[0] = 0
                if ty - b > -1:
                    i = cell - b * cE.size.w
                    if free(i) and open_side[1] != 0:
                        i = cell - b * cE.size.w + side_dir
                        if free(i):
                            free_side[1] = 1
                    else:
                        open_side[1] = 0
                if free_side[0] != 0 and free_side[1] != 0:
                    return 0 if pos.y - ty * 27 > 8 else 4
                if free_side[0] != 0:
                    return 0
                if free_side[1] != 0:
                    return 4
        return -1

    @staticmethod
    def straighten_step(delta, row):  # ar.java:1016-1023  (diagonal step -> straight step)
        steps = [[0, 1, 1, 2, 3, 4, 4, 5, 6, 7, 7, 8, 8, 9, 10, 10, 11],
                       [0, 2, 3, 4, 6, 7, 8, 9, 11, 13, 14, 16, 17, 18, 20, 21, 23]]
        if delta < 0:
            return -steps[row][min(16, -delta)]
        return steps[row][min(16, delta)]

    def move(self, pos, dx, dy, dir, actor):  # ar.java:1025-1153  (move; returns the direction, -1 blocked, 9 stopped)
        i = 0
        step_y = 0
        if dir == 8:
            if actor < 0:
                dx = GameCanvas.hero.slide_target.x
                dy = GameCanvas.hero.slide_target.y
            else:
                dx = GameCanvas.actors[actor].target.x
                dy = GameCanvas.actors[actor].target.y
        else:
            if dx > 0:
                i = self.step_until_free(pos, dx, 6)
            elif dx < 0:
                i = self.step_until_free(pos, dx, 2)
            if dy > 0:
                step_y = self.step_until_free(pos, dy, 0)
            elif dy < 0:
                step_y = self.step_until_free(pos, dy, 4)
        straight = MapEngine.straighten_step
        if dir in (2, 6):
            if 0 == i:
                return -1
        elif dir in (0, 4):
            if 0 == step_y:
                return -1
        elif dir in (1, 3, 5, 7):
            # diagonal: if one axis is blocked, go straight along the other one
            hx, vy = {1: (2, 0), 3: (2, 4), 5: (6, 4), 7: (6, 0)}[dir]
            if not (i != 0 and step_y != 0):
                if i != 0:
                    dir = hx
                    i = self.step_until_free(pos, straight(dx, 1), hx)
                elif step_y != 0:
                    dir = vy
                    step_y = self.step_until_free(pos, straight(dy, 1), vy)
                else:
                    return -1
        elif dir == 8:
            if actor == -1:
                slide = GameCanvas.hero.slide_target
            else:
                slide = GameCanvas.actors[actor].target
            i = slide.x
            step_y = slide.y
            if slide.x > 0:
                dir = 6
            elif slide.x < 0:
                dir = 2
            elif slide.y > 0:
                dir = 0
            elif slide.y < 0:
                dir = 4
        delta = self.keep_in_room(pos, i, step_y)
        i = delta[0]
        step_y = delta[1]
        if i != 0 or step_y != 0:
            delta = self.blocked_by_actor(pos, i, step_y, actor)
            i = delta[0]
            step_y = delta[1]
            if i == 0 and step_y == 0:
                return 9
        pos.x = i16(pos.x + i)
        pos.y = i16(pos.y + step_y)
        return dir

    def blocked_by_actor(self, pos, dx, dy, actor):  # ar.java:1155-1194  (do not walk into the hero / enemies)
        b = 0
        dest = Point()
        dest.x = i16(pos.x + dx)
        dest.y = i16(pos.y + dy)
        if actor > -1:
            i = MapEngine.distance(dest, GameCanvas.hero.pos[0])
            dist_now = MapEngine.distance(pos, GameCanvas.hero.pos[0])
            if i < dist_now and i < 20:
                while MapEngine.iabs(dest.x - GameCanvas.hero.pos[0].x) <= 27 and MapEngine.iabs(dest.y - GameCanvas.hero.pos[0].y) <= 27:
                    MapEngine.approach_zero(dx, dy)       # (result unused in the original)
                    dest.x = i16(pos.x + dx)
                    dest.y = i16(pos.y + dy)
                    b += 1
                    if b > 16:
                        break
        else:
            for nth in range(GameCanvas.actor_count):
                slot = GameCanvas.actor_slots[nth]
                if GameCanvas.actors[slot].action[0] != 3:
                    i = MapEngine.distance(dest, GameCanvas.actors[slot].pos[0])
                    dist_now = MapEngine.distance(pos, GameCanvas.actors[slot].pos[0])
                    if i < dist_now and i < 20:
                        b = 0
                        while MapEngine.iabs(dest.x - GameCanvas.actors[slot].pos[0].x) <= 27 and MapEngine.iabs(dest.y - GameCanvas.actors[slot].pos[0].y) <= 27:
                            MapEngine.approach_zero(dx, dy)
                            dest.x = i16(pos.x + dx)
                            dest.y = i16(pos.y + dy)
                            b += 1
                            if b > 16:
                                break
        return [dx, dy]

    # ---- the combat: hits ---------------------------------------------------------------------

    def hero_hits_enemy(self, index, action):  # ar.java:284-339  (the hero's action paramInt2 hits enemy paramInt1)
        ex = GameCanvas.actors[index]
        cz = GameCanvas.hero
        ex.hit_fx_kind = 1
        if action > -1:
            ex.dir[0] = ex.facing = MapEngine.dir8(ex.pos[0], cz.pos[0])
        else:
            ex.dir[0] = ex.facing = MapEngine.dir8(ex.pos[0], GameCanvas.effect.pos)
        if 3 <= action <= 8:
            i = cz.attack + cz.attack_buff - ex.defense - ex.defense_buff
            ex.hp = i16(ex.hp - (i if i > 0 else 1))
        elif action in (12, 13, 14) or 20 <= action <= 30:
            i = cz.attack + cz.attack_buff + idiv(cz.attack * cz.skill_levels[action - 12], consts.skill_attack_div[action - 12]) - ex.defense - ex.defense_buff
            ex.hp = i16(ex.hp - (i if i > 0 else 1))
        elif action == -2:
            ex.ai_mode = 2
            ex.hp = i16(ex.hp - (50 if cz.level << 1 > 50 else cz.level << 1))
            self.play_sound(4)
        elif action == -1:
            ex.hp = i16(ex.hp - (30 if cz.level > 30 else cz.level))
            self.play_sound(3)
        if ex.hp < 1:
            ex.hp = 0
            ex.frame[0] = 3
        else:
            ex.frame[0] = 0
        MapEngine.show_target_info(index)
        ex.hit_fx_pos = ex.pos[0]
        ex.hit_fx_frame = -1
        ex.action[0] = 2
        if ex.type < 200 and self.rand(1000) < 150 and ex.hp > 0:
            self.general_pick_skill(index, 1)

    def general_pick_skill(self, index, force):  # ar.java:341-368  (a general picks a skill)
        ex = GameCanvas.actors[index]
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
                if force != 0:
                    ex.action[0] = 1
        ex.dir[0] = ex.facing = MapEngine.dir4(ex.pos[0], GameCanvas.hero.pos[0])

    def hero_hits_breakables(self):  # ar.java:370-408  (the hero's attack vs. breakable objects cA)
        cz = GameCanvas.hero
        front = Point()
        for b in range(GameCanvas.breakable_count):
            cA = GameCanvas.breakables[b]
            if cA.active != 0 and cA.hp > 0:
                action = cz.action[0]
                if action == 13:
                    side = cz.dir[0] >> 1
                    if self.boxes_touch(cz.pos[0].x + consts.hit_box_x[side], cz.pos[0].y + consts.hit_box_y[side], consts.hit_box_w[side], consts.hit_box_h[side], cA.pos.x - 8, cA.pos.y - 8, 18, 18):
                        self.hit_breakable(b)
                elif action == 22:
                    if MapEngine.is_in_front(cz.pos[0], cA.pos, cz.dir[0]) != 0:
                        self.breakable_hit_if_near(b, consts.weapon_reach[cz.weapon_kind])
                elif action in (23, 24):
                    self.breakable_hit_if_near(b, 45)
                elif action == 25:
                    if (cz.dir[0] + (cz.frame[0] >> 1 << 1) & 0x7) == MapEngine.dir4(cz.pos[0], cA.pos):
                        self.breakable_hit_if_near(b, consts.weapon_reach[cz.weapon_kind])
                elif action in (26, 27):
                    front.x = i16(cz.pos[0].x + consts.front_dx[cz.dir[0] >> 1])
                    front.y = i16(cz.pos[0].y + consts.front_dy[cz.dir[0] >> 1])
                    if MapEngine.distance(front, cA.pos) <= 35:
                        self.hit_breakable(b)
                elif action in (28, 29, 30):
                    self.hit_breakable(b)
                else:
                    self.breakable_hit_if_facing(b, consts.weapon_reach[cz.weapon_kind])

    @staticmethod
    def show_target_info(index):  # ar.java:410-421  (message box: enemy name and HP bar)
        ex = GameCanvas.actors[index]
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
    def is_in_front(a, b, dir):  # ar.java:423-443  (is paramh2 in front of paramh1?)
        if dir == 2:
            if a.x > b.x:
                return 1
        elif dir == 6:
            if a.x < b.x:
                return 1
        elif dir == 0:
            if a.y < b.y:
                return 1
        elif dir == 4:
            if a.y > b.y:
                return 1
        return 0

    @staticmethod
    def dir4(a, b):  # ar.java:445-449  (direction 0/2/4/6 from paramh1 to paramh2)
        i = b.x - a.x
        dy = b.y - a.y
        if dy > i:
            return 0 if dy > -i else 2
        return 6 if dy > -i else 4

    @staticmethod
    def dir8(a, b):  # ar.java:451-455  (direction 0..7 from paramh1 to paramh2)
        i = b.x - a.x
        dy = b.y - a.y
        if i + i < dy:
            if i + i > -dy:
                return 0
            if -i < dy + dy:
                return 1
            if i < dy + dy:
                return 2
            return 3
        if i + i < -dy:
            return 4
        if -i > dy + dy:
            return 5
        if i > dy + dy:
            return 6
        return 7

    def hero_strike_if_facing(self, index, reach):  # ar.java:470-473
        if GameCanvas.hero.dir[0] == MapEngine.dir4(GameCanvas.hero.pos[0], GameCanvas.actors[index].pos[0]):
            self.hero_strike_if_near(index, reach)

    def general_strike_if_facing(self, index, reach):  # ar.java:475-478
        if GameCanvas.actors[index].dir[0] == MapEngine.dir4(GameCanvas.actors[index].pos[0], GameCanvas.hero.pos[0]):
            self.general_strike_if_near(index, reach)

    def breakable_hit_if_facing(self, index, reach):  # ar.java:480-483
        if GameCanvas.hero.dir[0] == MapEngine.dir4(GameCanvas.hero.pos[0], GameCanvas.breakables[index].pos):
            self.breakable_hit_if_near(index, reach)

    def hero_strike_if_near(self, index, reach):  # ar.java:485-488
        if MapEngine.distance(GameCanvas.hero.pos[0], GameCanvas.actors[index].pos[0]) <= reach:
            self.strike_enemy(index)

    def general_strike_if_near(self, index, reach):  # ar.java:490-493
        if MapEngine.distance(GameCanvas.hero.pos[0], GameCanvas.actors[index].pos[0]) <= reach:
            self.general_skill_hits_hero(index)

    def breakable_hit_if_near(self, index, reach):  # ar.java:495-498
        if MapEngine.distance(GameCanvas.hero.pos[0], GameCanvas.breakables[index].pos) <= reach:
            self.hit_breakable(index)

    def strike_enemy(self, index):  # ar.java:500-544  (the hero hits enemy paramInt: knock-back A, effects)
        cz = GameCanvas.hero
        ex = GameCanvas.actors[index]
        front = Point()
        if ex.action[0] > 5:
            return
        self.hero_hits_enemy(index, cz.action[0])
        if cz.combo > 1 and cz.action[0] < 12:
            ex.ai_mode = 1
        action = cz.action[0]
        if action == 12:
            cz.frame[0] = 5
            ex.ai_mode = 2
        elif action in (14, 22):
            ex.ai_mode = 2
        elif action == 20:
            ex.hit_fx_kind = i8(self.rand(2) + 1)
            ex.ai_mode = 0
        elif action == 21:
            ex.ai_mode = 5
        elif action in (23, 24):
            if action == 24:                    # case 24 falls through into case 23
                ex.ai_mode = 5
            self.set_enemy_on_fire(index)
        elif action in (25, 26, 27):
            if action == 25:                    # 25 -> 27 -> 26 fall through
                ex.ai_mode = 2
            if action in (25, 27):
                ex.ai_mode = 5
            ex.hit_fx_kind = 2
            front.x = i16(cz.pos[0].x + consts.front_dx[cz.dir[0] >> 1])
            front.y = i16(cz.pos[0].y + consts.front_dy[cz.dir[0] >> 1])
            ex.dir[0] = ex.facing = MapEngine.dir8(ex.pos[0], front)
        elif action == 29:
            self.set_enemy_on_fire(index)
        self.play_sound(16)                       # (`if (A != 0);` - the sound plays always)

    def general_skill_hits_hero(self, index):  # ar.java:546-578  (a general's skill hits the hero)
        cz = GameCanvas.hero
        action = GameCanvas.actors[index].action[0]
        if action == 6:
            GameCanvas.actors[index].frame[0] = 5
            cz.hurt_ticks = 2
        elif action in (8, 16):
            cz.hurt_ticks = 2
        elif action == 14:
            cz.hit_fx_kind = self.rand(2) + 1
        elif action == 15:
            cz.hurt_ticks = 5
        elif action in (17, 18):
            if action == 18:                    # case 18 falls through into case 17
                cz.hurt_ticks = 5
            self.set_hero_on_fire()
        elif action == 19:
            cz.hurt_ticks = 2
            self.set_hero_on_fire()
        elif action in (20, 21):
            if action == 21:                    # case 21 falls through into case 20
                cz.hurt_ticks = 5
            cz.hit_fx_kind = 2
        self.hero_is_hit(index)

    def hero_is_hit(self, index):  # ar.java:580-638  (the hero is hit by enemy paramInt, or by arrow paramInt + 3)
        cz = GameCanvas.hero
        if index > -1:
            ex = GameCanvas.actors[index]
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
            eC = GameCanvas.arrows[index + 3]
            cz.dir[0] = cz.facing = (eC.dir << 1) + 4 & 0x7
            i = eC.attack - cz.defense - cz.defense_buff
            b = i8(i if i > 0 else 1)
            if cz.hp > b:
                cz.hp -= b
            else:
                cz.hp = 0
        if index > -1:
            MapEngine.show_target_info(index)
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

    def set_enemy_on_fire(self, index):  # ar.java:640-651  (fire effect on an enemy)
        GameCanvas.actors[index].on_fire = 1
        GameCanvas.actors[index].fire_frame = 0
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

    def hit_breakable(self, index):  # ar.java:663-672  (hit a breakable object)
        cA = GameCanvas.breakables[index]
        cA.hp = i16(cA.hp - GameCanvas.hero.attack + GameCanvas.hero.attack_buff)
        self.play_sound(3)
        cA.break_frame = 2
        if cA.hp < 1:
            cA.break_ticks = 12
            i = cA.tile.y * GameCanvas.map.size.w + cA.tile.x
            GameCanvas.map.data[GameCanvas.map.layer_objects + i] = 0

    def hero_attack(self, kind):  # ar.java:674-724  (the hero's attack (0) or a scroll (-1/-2) vs. enemies)
        cz = GameCanvas.hero
        front = Point()
        for b in range(GameCanvas.actor_count):
            slot = GameCanvas.actor_slots[b]
            ex = GameCanvas.actors[slot]
            if ex.hp > 0 and ex.alerted != 0 and ex.action[0] < 6:
                if kind == 0:
                    action = cz.action[0]
                    if action == 13:
                        side = cz.dir[0] >> 1
                        if self.boxes_touch(cz.pos[0].x + consts.hit_box_x[side], cz.pos[0].y + consts.hit_box_y[side], consts.hit_box_w[side], consts.hit_box_h[side], ex.pos[0].x - 8, ex.pos[0].y - 8, 17, 17):
                            self.hero_hits_enemy(slot, cz.action[0])
                            self.play_sound(3)
                    elif action == 22:
                        if MapEngine.is_in_front(cz.pos[0], ex.pos[0], cz.dir[0]) != 0:
                            self.hero_strike_if_near(slot, consts.weapon_reach[cz.weapon_kind])
                    elif action in (23, 24):
                        self.hero_strike_if_near(slot, 45)
                    elif action == 25:
                        if (cz.dir[0] + (cz.frame[0] >> 1 << 1) & 0x7) == MapEngine.dir4(cz.pos[0], ex.pos[0]):
                            self.hero_strike_if_near(slot, consts.weapon_reach[cz.weapon_kind])
                    elif action in (26, 27):
                        front.x = i16(cz.pos[0].x + consts.front_dx[cz.dir[0] >> 1])
                        front.y = i16(cz.pos[0].y + consts.front_dy[cz.dir[0] >> 1])
                        if MapEngine.distance(front, ex.pos[0]) <= 35:
                            self.strike_enemy(slot)
                    elif action in (28, 29, 30):
                        self.strike_enemy(slot)
                    self.hero_strike_if_facing(slot, consts.weapon_reach[cz.weapon_kind])
                elif kind in (-2, -1):
                    if MapEngine.distance(GameCanvas.effect.pos, ex.pos[0]) <= 35:
                        self.hero_hits_enemy(slot, GameCanvas.effect.item)
                        self.play_sound(4)

    def turn_to_nearest(self):  # ar.java:1196-1200  (Normal difficulty, ep = 1: turn to the nearest enemy before the attack)
        if GameCanvas.difficulty != 0 or config.AUTO_AIM_HARD:   # PORT-EXTRA config.AUTO_AIM_HARD: also on Hard
            i = self.nearest_enemy()
            if i > -1:
                GameCanvas.hero.dir[0] = GameCanvas.hero.facing = MapEngine.dir4(GameCanvas.hero.pos[0], GameCanvas.actors[i].pos[0])

    def nearest_enemy(self):  # ar.java:1202-1214  (nearest living enemy closer than 50)
        found = -1
        best = 50
        for b in range(GameCanvas.actor_count):
            slot = GameCanvas.actor_slots[b]
            i = MapEngine.distance(GameCanvas.actors[slot].pos[0], GameCanvas.hero.pos[0])
            if best > i and GameCanvas.actors[slot].hp > 0:
                best = i
                found = slot
        return found

    # ---- the combat: enemy AI ----------------------------------------------------------------

    def choose_enemy_action(self, index):  # ar.java:1216-1278  (choose the next action of enemy paramInt)
        turns = [-2, -1, 0, 0, 0, 0, 1, 2]
        cz = GameCanvas.hero
        ex = GameCanvas.actors[index]
        i = MapEngine.distance(cz.pos[0], ex.pos[0])
        b = 1 if i < 90 else 0
        ex.frame[0] = 0
        roll = self.rand(1000)
        to_hero = MapEngine.dir_to_hero(ex.pos[0])
        if ex.type in (201, 203):
            if roll < 150 + b * 300:
                ex.action[0] = 0
                ex.dir[0] = ex.facing = i8(to_hero + turns[roll & 0x7] & 0x7)
                return
            if roll < 850 - b * 100:
                if b != 0:
                    if i <= 45 and cz.action[0] != 9 and cz.action[0] != 10 and cz.action[0] < 12:
                        ex.action[0] = 1
                        ex.dir[0] = ex.facing = MapEngine.dir4(ex.pos[0], cz.pos[0])
                        self.hero_is_hit(index)
                        return
                    ex.action[0] = 0
                    ex.dir[0] = ex.facing = i8(to_hero + turns[roll & 0x7] & 0x7)
                    return
                ex.action[0] = 0
                ex.dir[0] = ex.facing = i8(ex.dir[0] + turns[roll & 0x7] & 0x7)
                return
            ex.action[0] = 0
            if b != 0:
                ex.dir[0] = ex.facing = i8(roll & 0x7)
                return
            ex.dir[0] = ex.facing = i8(ex.dir[0] + turns[roll & 0x7] & 0x7)
            return
        if ex.type == 202:
            ex.action[0] = 1
            ex.think_ticks = 15
            MapEngine.shoot_arrow(index)
            return
        if roll < 150:
            self.general_pick_skill(index, 0)
            return
        if roll < 350:
            if i <= 60 and (cz.action[0] != 9 or cz.frame[0] >= 6) and cz.action[0] != 10 and cz.action[0] < 12:
                ex.action[0] = 1
                ex.dir[0] = ex.facing = MapEngine.dir4(ex.pos[0], cz.pos[0])
                return
        else:
            ex.dir[0] = ex.facing = to_hero

    @staticmethod
    def dir_to_hero(pos):  # ar.java:1280-1284  (direction 0..7 from paramh to the hero, 27 px dead zone)
        i = GameCanvas.hero.pos[0].x - pos.x
        dy = GameCanvas.hero.pos[0].y - pos.y
        if i > 27:
            return 7 if dy > 27 else (5 if dy < -27 else 6)
        if i < -27:
            return 1 if dy > 27 else (3 if dy < -27 else 2)
        return 0 if dy > 0 else 4

    @staticmethod
    def shoot_arrow(index):  # ar.java:1286-1308  (an archer shoots an arrow eC)
        arrow_dx = [-1, -15, -1, 5]
        arrow_dy = [-5, -13, -30, -13]
        ex = GameCanvas.actors[index]
        i = ex.dir[0] >> 1
        for b in range(3):
            eC = GameCanvas.arrows[b]
            if eC.active == 0:
                eC.active = 1
                eC.pos[1].x = i16(ex.pos[0].x + arrow_dx[i])
                eC.pos[1].y = i16(ex.pos[0].y + arrow_dy[i])
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
        buff_div = [20, 20, 25]
        i = 0
        cz = GameCanvas.hero
        # Java `for (b = 0; b < ag.ez; b++)` reads ez every time: ab() below removes the dead
        # enemy from ey and decrements ez inside the loop (and the next enemy is skipped this tick)
        b = -1
        while True:
            b += 1
            if b >= GameCanvas.actor_count:
                break
            slot = GameCanvas.actor_slots[b]
            ex = GameCanvas.actors[slot]
            ex.action[0] = min(ex.action[0], len(ex.anims[ex.dir[0]]) - 1)
            ex.frame[0] = i8(ex.frame[0] + 1)
            ex.think_ticks = i8(ex.think_ticks - 1)
            anim_frame = ex.anims[ex.dir[0]][ex.action[0]][ex.frame[0]]
            if ex.attack_buff_ticks > 0:
                ex.attack_buff_ticks = i16(ex.attack_buff_ticks - 1)
                if ex.attack_buff_ticks < 1:
                    ex.attack_buff = 0
            if ex.defense_buff_ticks > 0:
                ex.defense_buff_ticks = i16(ex.defense_buff_ticks - 1)
                if ex.defense_buff_ticks < 1:
                    ex.defense_buff = 0
            if ex.action[0] == 3:
                if anim_frame > 200:
                    self.enemy_dies(slot)
                    if GameCanvas.enemies_alive < 1 and 0 == GameCanvas.waves[0] and ex.type != 202:
                        if GameCanvas.boss_fight != 0:
                            GameCanvas.room_phase = 4
                            GameCanvas.room_phase_timer = 22
                        else:
                            GameCanvas.room_phase = 3
                            GameCanvas.room_phase_timer = 5
                continue
            if anim_frame > 200:
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
                    self.choose_enemy_action(slot)
            if ex.type == 202:
                ex.dir[0] = ex.facing = MapEngine.dir4(ex.pos[0], cz.pos[0])
                continue
            move_dir = ex.facing
            if ex.alerted == 0:
                ex.pos[0].x = i16(ex.pos[0].x + consts.dir_dx8[move_dir])
                ex.pos[0].y = i16(ex.pos[0].y + consts.dir_dy8[move_dir])
                continue
            step_x = step_y = 0
            action = ex.action[0]
            frame = ex.frame[0]
            dir = ex.dir[0]
            if action == 0:
                step_x = consts.dir_dx8[move_dir]
                step_y = consts.dir_dy8[move_dir]
            elif action in (1, 4, 5):
                step_x = idiv(consts.dir_dx8[dir], 3)
                step_y = idiv(consts.dir_dy8[dir], 3)
            elif action == 6:
                if 2 < frame < 6:
                    step_x = consts.dir_dx8[dir] << 2
                    step_y = consts.dir_dy8[dir] << 2
            elif action in (7, 8):
                fall8 = action == 8
                if action == 7 and 4 < frame < 8:
                    step_x = consts.dir_dx8[dir] << 2
                    step_y = consts.dir_dy8[dir] << 2
                    if step_x > 0:
                        step_x = self.step_until_free(ex.pos[0], step_x, 6)
                    elif step_x < 0:
                        step_x = self.step_until_free(ex.pos[0], step_x, 2)
                    if step_y > 0:
                        step_y = self.step_until_free(ex.pos[0], step_y, 0)
                    elif step_y < 0:
                        step_y = self.step_until_free(ex.pos[0], step_y, 4)
                    delta = self.keep_in_room(ex.pos[0], step_x, step_y)
                    step_x = delta[0]
                    step_y = delta[1]
                    ex.pos[0].x = i16(ex.pos[0].x + step_x)
                    ex.pos[0].y = i16(ex.pos[0].y + step_y)
                    fall8 = True            # no break: falls into case 8
                if fall8 and 0 < frame < 9:
                    step_x = consts.dir_dx8[dir]
                    step_y = consts.dir_dy8[dir]
            elif action == 14:
                if 0 == (frame & 0x1):
                    step_x = consts.dir_dx8[dir]
                    step_y = consts.dir_dy8[dir]
            elif action == 2 and ex.ai_mode > 0:
                ex.ai_mode = i8(ex.ai_mode - 1)
                move_dir = move_dir + 4 & 0x7
                step_x = consts.dir_dx8[move_dir] << 2
                step_y = consts.dir_dy8[move_dir] << 2
            elif action == 2 and frame == 1:
                move_dir = ex.facing + 4 & 0x7
                step_x = idiv(consts.dir_dx8[move_dir] * 3, 4)
                step_y = idiv(consts.dir_dy8[move_dir] * 3, 4)
            if step_x != 0 or step_y != 0:
                if ex.type == 203:
                    pos = ex.pos
                    dx, dy = MapEngine._SHIFT203.get(move_dir, (0, 0))
                    pos[0].x = i16(pos[0].x + dx)
                    pos[1].x = i16(pos[1].x + dx)
                    pos[0].y = i16(pos[0].y + dy)
                    pos[1].y = i16(pos[1].y + dy)
                    i = self.move(pos[0], step_x, step_y, move_dir, slot)
                    pos[0].x = i16(pos[0].x - dx)
                    pos[1].x = i16(pos[1].x - dx)
                    pos[0].y = i16(pos[0].y - dy)
                    pos[1].y = i16(pos[1].y - dy)
                else:
                    i = self.move(ex.pos[0], step_x, step_y, move_dir, slot)
                if ex.action[0] == 0 and move_dir in (0, 2, 4, 6):
                    if i == -1:
                        i = MapEngine.slide_corner(ex.pos[0], ex.facing, slot)
                        if i != -1:
                            self.move(ex.pos[0], consts.dir_dx8[i], consts.dir_dy8[i], i, slot)
            action = ex.action[0]
            frame = ex.frame[0]
            if action in (1, 4, 5):
                if frame == 1:
                    self.enemy_strikes_hero(slot)
            elif action == 6:
                if 2 < frame < 6:
                    self.enemy_strikes_hero(slot)
            elif action == 7:
                if 4 < frame < 8:
                    self.enemy_strikes_hero(slot)
            elif action == 8:
                if frame in (2, 4, 6, 8):
                    self.enemy_strikes_hero(slot)
            elif action in (9, 10):
                if frame == 11:
                    ex.hp = i16(ex.hp + idiv(ex.max_hp * (20 if action == 9 else 50), 100))
                    if ex.hp > ex.max_hp:
                        ex.hp = ex.max_hp
            elif action in (11, 12, 13):
                if frame == 11:
                    if action != 12:
                        ex.attack_buff = i16(idiv(ex.attack, buff_div[action - 11]))
                        if ex.attack_buff < 1:
                            ex.attack_buff = 1
                        ex.attack_buff_ticks = 50
                    if action != 11:
                        ex.defense_buff = i16(idiv(ex.defense, buff_div[action - 11]))
                        if ex.defense_buff < 1:
                            ex.defense_buff = 1
                        ex.defense_buff_ticks = 50
            elif action == 14:
                if (frame & 0x1) != 0:
                    self.enemy_strikes_hero(slot)
            elif action == 15:
                if frame == 5:
                    self.enemy_strikes_hero(slot)
            elif action == 16:
                if frame == 6:
                    self.enemy_strikes_hero(slot)
            elif action in (17, 18):
                if frame == 5:
                    self.enemy_strikes_hero(slot)
            elif action == 19:
                if (frame & 0x1) != 0:
                    self.enemy_strikes_hero(slot)
            elif action in (20, 21):
                if frame == 8:
                    self.enemy_strikes_hero(slot)

    def enemy_strikes_hero(self, index):  # ar.java:1606-1661  (enemy paramInt strikes the hero)
        cz = GameCanvas.hero
        ex = GameCanvas.actors[index]
        front = Point()
        if cz.action[0] != 9 and cz.action[0] != 10:
            if cz.action[0] < 12:
                action = ex.action[0]
                if action == 7:
                    side = ex.dir[0] >> 1
                    if self.boxes_touch(ex.pos[0].x + consts.hit_box_x[side], ex.pos[0].y + consts.hit_box_y[side], consts.hit_box_w[side], consts.hit_box_h[side], cz.pos[0].x - 8, cz.pos[0].y - 8, 17, 17):
                        self.hero_is_hit(index)
                    return
                if action == 16:
                    if MapEngine.is_in_front(ex.pos[0], cz.pos[0], ex.dir[0]) != 0:
                        self.general_strike_if_near(index, consts.general_reach[GameCanvas.general.side])
                    return
                if action in (17, 18):
                    self.general_strike_if_near(index, 45)
                    return
                if action == 19:
                    if (ex.dir[0] + (ex.frame[0] >> 1 << 1) & 0x7) == MapEngine.dir4(ex.pos[0], cz.pos[0]):
                        self.general_strike_if_near(index, consts.general_reach[GameCanvas.general.side])
                    return
                if action in (20, 21):
                    front.x = i16(ex.pos[0].x + consts.front_dx[ex.dir[0] >> 1])
                    front.y = i16(ex.pos[0].y + consts.front_dy[ex.dir[0] >> 1])
                    if MapEngine.distance(front, cz.pos[0]) <= 35:
                        self.general_skill_hits_hero(index)
                    return
                self.general_strike_if_facing(index, consts.general_reach[GameCanvas.general.side])
                return
        elif cz.action[0] == 9:
            action = ex.action[0]
            if action in (8, 14):
                self.general_strike_if_facing(index, consts.general_reach[GameCanvas.general.side])
                return
            if action in (20, 21):
                front.x = i16(ex.pos[0].x + consts.front_dx[cz.dir[0] >> 1])
                front.y = i16(ex.pos[0].y + consts.front_dy[cz.dir[0] >> 1])
                if MapEngine.distance(front, cz.pos[0]) <= 35:
                    self.general_skill_hits_hero(index)

    def enemy_dies(self, index):  # ar.java:1663-1698  (enemy paramInt is dead: exp, drop, remove)
        ex = GameCanvas.actors[index]
        for b in range(GameCanvas.actor_count):
            if GameCanvas.actor_slots[b] == index:
                if ex.type < 200:
                    drop_kind = 2 if GameCanvas.boss_fight != 0 else 1
                    GameCanvas.mission_exp += ex.level << 1
                    if GameCanvas.general.side != GameCanvas.hero.weapon_kind:
                        GameCanvas.images[40 + GameCanvas.general.side] = None
                    GameCanvas.boss_images[1] = None
                    for i in range(3, 9):
                        GameCanvas.enemy_frames[i] = None
                    GameCanvas.boss_spawned = 0
                else:
                    drop_kind = 0
                    GameCanvas.mission_exp += ex.level
                self.drop_item(drop_kind, ex.pos[0])
                if ex.type == 203:
                    GameCanvas.hero.kills += 3
                else:
                    GameCanvas.hero.kills += 1
                for drop_kind in range(b, 6):
                    GameCanvas.actor_slots[drop_kind] = GameCanvas.actor_slots[drop_kind + 1]
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
                        slot = GameCanvas.actor_slots[b]
                        GameCanvas.actor_slots[b] = GameCanvas.actor_slots[i]
                        GameCanvas.actor_slots[i] = slot

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

    def hero_can_be_hit(self, index):  # ar.java:1751-1772
        action = GameCanvas.hero.action[1]
        frame = GameCanvas.hero.frame[1]
        if action in (26, 27):
            if 1 < frame < 9:
                return
        elif action == 28:
            if frame > 3:
                return
        elif action == 29:
            if frame > 6:
                return
        elif action == 30:
            if 3 < frame < 15:
                return
        MapEngine.move_arrow(index)

    @staticmethod
    def move_arrow(index):  # ar.java:1774-1793  (move an arrow)
        eC = GameCanvas.arrows[index]
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
            slot = GameCanvas.actor_slots[b]
            GameCanvas.actors[slot].pos[1] = GameCanvas.actors[slot].pos[0]
            GameCanvas.actors[slot].dir[1] = GameCanvas.actors[slot].dir[0]
            GameCanvas.actors[slot].action[1] = GameCanvas.actors[slot].action[0]
            GameCanvas.actors[slot].frame[1] = GameCanvas.actors[slot].frame[0]
        if cz.action[0] in (28, 29, 30):
            if GameCanvas.room_phase != 0:
                GameCanvas.room_phase_timer = 0
            return
        if GameCanvas.room_phase != 0:
            if GameCanvas.room_phase_timer < 1:
                phase = GameCanvas.room_phase
                if phase == 1:
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
                elif phase == 2:
                    GameCanvas.popups.setup_popup(8)
                    GameCanvas.room_phase = 0
                    return
                elif phase == 3:
                    GameCanvas.popups.setup_popup(9)
                    GameCanvas.room_phase = 0
                    return
                elif phase == 4:
                    GameCanvas.popups.setup_popup(10)
                    GameCanvas.room_phase = 0
                return
            GameCanvas.room_phase_timer = i16(GameCanvas.room_phase_timer - 1)
            if GameCanvas.room_phase == 3 and GameCanvas.room_phase_timer == 0 and GameCanvas.sound is not None:
                GameCanvas.stop_sound()

    def tick_mission_clock(self, running):  # ar.java:1881-1890  (mission clock dX, paused while a popup / menu is open)
        GameCanvas.clock[0] = GameCanvas.now()
        if running == 0 or GameCanvas.clock[0] - GameCanvas.clock[1] > 1000:
            GameCanvas.play_time += GameCanvas.clock[0] - GameCanvas.clock[1]
        else:
            elapsed = GameCanvas.clock[0] - GameCanvas.play_time
            GameCanvas.mission_seconds = int(elapsed // 1000)
        GameCanvas.clock[1] = GameCanvas.clock[0]

    def scroll_room(self):  # ar.java:1892-1932  (bV = 4: scroll to the next room, 6 steps)
        exit_dir = GameCanvas.exit_dir
        if exit_dir == 1:
            GameCanvas.view_ty += 7
        elif exit_dir == 2:
            GameCanvas.view_tx -= 7
        elif exit_dir == 3:
            GameCanvas.view_ty -= 7
        elif exit_dir == 4:
            GameCanvas.view_tx += 7
        if exit_dir in (1, 2, 3, 4):
            GameCanvas.exit_blink = i16(GameCanvas.exit_blink + 6)
            GameCanvas.scene.draw_tiles(GameCanvas.view_tiles.x, GameCanvas.view_tiles.y, GameCanvas.view_tx, GameCanvas.view_ty, 0)
        self.draw_view_region(GameCanvas.images[7], GameCanvas.view_x, GameCanvas.view_y, GameCanvas.view_size.x, GameCanvas.view_size.y, GameCanvas.view_offset.x, GameCanvas.view_offset.y)
        delta = self.keep_in_room(GameCanvas.hero.pos[0], 0, 0)
        GameCanvas.hero.pos[0].x = i16(GameCanvas.hero.pos[0].x + delta[0])
        GameCanvas.hero.pos[0].y = i16(GameCanvas.hero.pos[0].y + delta[1])
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

    def draw_spark(self, frame, x, y):  # ar.java:1934-1936  (hit spark eV)
        spark = GameCanvas.spark_frames[frame]
        self.draw_map_region(GameCanvas.images[43], x - spark.ox, y - spark.oy, spark.w, spark.h, spark.src_x, spark.src_y)

    def draw_hero_weapon(self, x, y, frame):  # ar.java:1938-1941  (the hero's weapon)
        self.draw_map_region(GameCanvas.images[40 + GameCanvas.hero.weapon_kind], x - frame.ox, y - frame.oy, frame.w, frame.h, frame.src_x, frame.src_y)
        MapScene.mark_dirty(GameCanvas.hero.pos[0].x - frame.ox, GameCanvas.hero.pos[0].y - frame.oy, frame.w, frame.h)

    def draw_weapon_trail(self, index, step):  # ar.java:1943-1969  (weapon trail of the hero (-1) or an enemy)
        if index > -1:
            pos = GameCanvas.actors[index].pos[0]
            if GameCanvas.actors[index].action[0] == 19:
                i = GameCanvas.actors[index].dir[0] + (GameCanvas.actors[index].frame[0] >> 1 << 1) & 0x7
            else:
                i = GameCanvas.actors[index].dir[0]
        else:
            pos = GameCanvas.hero.pos[0]
            if GameCanvas.hero.action[0] == 25:
                i = GameCanvas.hero.dir[0] + (GameCanvas.hero.frame[0] >> 1 << 1) & 0x7
            else:
                i = GameCanvas.hero.dir[0]
        frame = (i >> 1) * 6 + (step << 1)
        sx = pos.x - GameCanvas.camera.x
        sy = pos.y - GameCanvas.camera.y
        for b in range(2):
            part = GameCanvas.trail_frames[frame]
            self.draw_map_region(GameCanvas.images[42], sx - part.ox, sy - part.oy, part.w, part.h, part.src_x, part.src_y)
            MapScene.mark_dirty(pos.x - part.ox, pos.y - part.oy, part.w, part.h)
            frame += 1

    def draw_object_layer(self):  # ar.java:1971-1983  (object layer over dirty cells)
        cE = GameCanvas.map
        for b in range(GameCanvas.view_tiles.x):
            for row in range(GameCanvas.view_tiles.y):
                if GameCanvas.dirty[row][b] != 0:
                    i = (GameCanvas.view_ty + row) * cE.size.w + GameCanvas.view_tx + b
                    if cE.data[cE.layer_objects + i] != 0:
                        image = GameCanvas.tile_slots[cE.data[cE.layer_objects + i] - 1] - 1
                        self.draw_map_region(GameCanvas.tile_images[image], (GameCanvas.view_tx + b) * 27 - GameCanvas.camera.x, (GameCanvas.view_ty + row) * 27 - GameCanvas.camera.y, 27, 27, 0, 0)

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
                    sy = cA.tile.y * 27 - GameCanvas.camera.y
                    if GameCanvas.images[7] is not None and i + GameCanvas.view_offset.x >= 0:
                        if i + GameCanvas.view_offset.x > GameCanvas.images[7].getWidth():
                            return
                        self.draw_map_region(GameCanvas.images[7], i, sy, 27, 27, i + GameCanvas.view_offset.x, sy + GameCanvas.view_offset.y)
                    else:
                        break
                if 0 == cA.break_ticks:
                    self.drop_item(3, cA.pos)
                    cA.active = 0

    def drop_item(self, kind, pos):  # ar.java:2017-2053  (drop an item at paramh)
        x = pos.x
        y = pos.y
        if y <= GameCanvas.camera.y + 27 or y >= GameCanvas.camera.y + 162 or x <= GameCanvas.camera.x + 27 or x >= GameCanvas.camera.x + 162:
            return
        item = self.random_drop(kind)
        if item != 0:
            i = idiv(y, 27) * GameCanvas.map.size.w + idiv(x, 27)
            if 0 == (GameCanvas.map.data[GameCanvas.map.layer_flags + i] & 0x1):
                b = 0
                while b < 10 and GameCanvas.drops[b].item != 0:
                    b += 1
                if b > 9:
                    return
                cC = GameCanvas.drops[b]
                cC.item = item
                if cC.pos is None:
                    cC.pos = Point()
                cC.pos.x = x
                cC.pos.y = y
                cC.ticks = 75
                cC.w = cC.h = 28
                if item > 10000:
                    cC.image = GameCanvas.images[32]
                    cC.frame = 0
                    cC.w = i16(GameCanvas.images[32].getWidth())
                    cC.h = i16(GameCanvas.images[32].getHeight())
                elif item > 100:
                    cC.image = GameCanvas.images[0]
                    cC.frame = 11
                else:
                    cC.image = GameCanvas.images[0]
                    cC.frame = i16(item - 1)
                if b >= GameCanvas.drop_count:
                    GameCanvas.drop_count = i16(GameCanvas.drop_count + 1)

    def random_drop(self, kind):  # ar.java:2055-2078  (random drop: item id, potion, or gold 10020/10040)
        C = self.rand
        drop_odds = [5, 10, 20, 5, 100]
        potion_odds = [10, 30, 60, 1, 100]
        tier_min_level = [69, 44, 24, 9, 0]
        tier_odds = [[0, 0, 33, 77, 100], [5, 30, 55, 80, 100], [30, 60, 90, 100, 100],
                       [40, 80, 100, 100, 100], [80, 100, 100, 100, 100]]
        if C(100) < drop_odds[kind]:
            i = C(100)
            if i < potion_odds[kind]:
                # PORT-EXTRA config.DROPS_AFTER_69: row 0 (above Lv69: no Lv1 / Lv10 gear) is skipped,
                # so a hero above Lv69 keeps the odds of Lv45-69
                for b in range(1 if config.DROPS_AFTER_69 else 0, 5):
                    if GameCanvas.hero.level > tier_min_level[b]:
                        i = C(100)
                        for tier in range(5):
                            if i < tier_odds[b][tier]:
                                return i16(101 + tier + 5 * C(20))
            else:
                return i16(C(11) + 1)
        elif C(100) < 25:
            return i16(10020 + (GameCanvas.difficulty ^ 0x1) * 20)
        return 0

    def draw_quick_potions(self):  # ar.java:2081-2089  (the two quick potions * and # of the HUD)
        cz = GameCanvas.hero
        for b in range(2):
            slot = cz.quick_slots[cz.quick_keys[b]]
            if slot.item != 0:
                GameCanvas.draw_region(GameCanvas.view_cx + (2 * b - 1) * (44 + 28 * (1 - b) + 0), GameCanvas.canvas_size.y - 33 - 0 - 17, 28, 28, GameCanvas.images[0], (slot.item - 1) * 28, 0)
                GameCanvas.draw_region(GameCanvas.view_cx + (2 * b - 1) * (38 + 11 * (1 - b) + 0), GameCanvas.canvas_size.y - 16 - 0 - 17, 11, 12, GameCanvas.images[20], 98, 0)
                self.draw_number_commas(slot.count, GameCanvas.view_cx + (2 * b - 1) * (28 + 10 * b + 0), GameCanvas.canvas_size.y - 18 - 0 - 17)

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
        box = GameCanvas.images[31]
        self.draw_map_region(box, GameCanvas.view_size.x - box.getWidth() - 27 - 5 - 7, 2 + GameCanvas.font_white.height(), box.getWidth(), box.getHeight(), 0, 0)
        self.draw_image_part(GameCanvas.message.level, GameCanvas.view_size.x - 15, 1 + GameCanvas.font_white.height() + 17, 9, 12, GameCanvas.images[20], 0, 0, -1)
        if GameCanvas.message.hp_bar > 0:
            bar = Rect(GameCanvas.view_size.x - 62 + GameCanvas.view_x - 7, 2 + GameCanvas.font_white.height() + 12 + GameCanvas.view_y, 62 if GameCanvas.message.hp_bar > 62 else GameCanvas.message.hp_bar, 7)
            GameCanvas.fill_rect(bar, GameCanvas.rgb(0, 0, 0))
            bar.y += 1
            bar.h = 5
            bar.x += 1
            bar.w -= 2
            GameCanvas.fill_rect(bar, GameCanvas.rgb(107, 0, 0))
            bar.y += 1
            bar.h = 3
            GameCanvas.fill_rect(bar, GameCanvas.rgb(181, 0, 0))
            bar.y += 1
            bar.h = 1
            GameCanvas.fill_rect(bar, GameCanvas.rgb(255, 73, 0))
        MapScene.mark_dirty(GameCanvas.camera.x + 170, GameCanvas.camera.y, 68, 40)
