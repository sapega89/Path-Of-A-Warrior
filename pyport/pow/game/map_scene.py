"""c.java - map, combat and the story player (bd). Literal port, partial:
c(int) (one page of a prologue / epilogue) and d(int) / g() (end of a mission) are ported;
the map and combat (phases 3-4) are not."""
from pow.game.game_canvas import GameCanvas
from pow.game import consts
from pow.game.res_reader import ResReader
from pow.game.gfx import Gfx
import config
from pow.midp.jint import i16, i32, i8, idiv
from pow.game.structs import Actor, Arrow, Breakable, Drop, MapData, MapSize, Point, Rect, RoomCell, ScriptSlot, SpawnSpot
from pow.game.font import Font

F14 = config.DECOMP_FIX["F14"]


# direction key -> cz.c, as c.i_v reads ag.cj (used by the PORT-EXTRA HOLD_TO_MOVE)
from pow.game.autopilot import Autopilot   # noqa: E402  PORT-EXTRA auto-hunt walks like HOLD_TO_MOVE

_HELD_DIR = {-1: 4, 50: 4, -3: 2, 52: 2, -4: 6, 54: 6, -2: 0, 56: 0}


class MapScene(GameCanvas):
    def __init__(self):  # c.java:4-6
        super().__init__(GameCanvas.midlet)

    def load_story_page(self, page):  # c.java:1393-1514  (load story page paramInt)
        digits = ['\0'] * 10
        picture = 0
        str_ = GameCanvas.scr_story.get(GameCanvas.story_pages[0] + page)
        if (GameCanvas.story_ending == 0 and page < GameCanvas.story_pages[1] - GameCanvas.story_pages[0]) or (GameCanvas.story_ending != 0 and page >= GameCanvas.story_pages[1] - GameCanvas.story_pages[0]):
            # dialogue page: "[Name] text" typed into one of the two speech boxes
            self.play_sound(0)
            line = ""
            if '/' < str_[0] < ':':
                GameCanvas.talk_lines[0] = ""
                if 0 == GameCanvas.story_id and page == 2:
                    GameCanvas.story_picture = 0
                    line = GameCanvas.gamestr(1)
                else:
                    b = 0
                    while b < 10:
                        if str_[b] == '|':
                            digits[b] = '\0'
                            break
                        digits[b] = str_[b]
                        b += 1
                    GameCanvas.story_picture = GameCanvas.parse_int(digits)
                    GameCanvas.text_width = len(str_) - b
                    line = str_[b + 1:]
                GameCanvas.speech[0] = line
                GameCanvas.speech_line = 0
                GameCanvas.speech_pos[0] = 0
            else:
                if GameCanvas.story_ending != 0 and 0 == (page & 0x1):
                    GameCanvas.speech_line = 0
                else:
                    GameCanvas.speech_line = 1
                GameCanvas.talk_lines[GameCanvas.speech_line] = line
                if GameCanvas.story_ending != 0 and 0 == (page & 0x1):
                    line = "[Master] " + str_
                else:
                    line = "[" + GameCanvas.hero.name + "] " + str_
                GameCanvas.speech[GameCanvas.speech_line] = line
                GameCanvas.speech_pos[GameCanvas.speech_line] = 0
                return
        else:
            if page == GameCanvas.story_pages[2] - GameCanvas.story_pages[0]:
                # last page of an epilogue: completion statistics
                mission_pct = hidden_pct = ending_pct = warrior_pct = 0
                for bit in range(225):
                    if (GameCanvas.stats[bit >> 5] & i32(1 << (bit & 0x1F))) != 0:
                        mission_pct += 1
                for b in range(45):
                    if b < 24 and (GameCanvas.score & 1 << b) != 0:
                        ending_pct += 1
                    if 0 == (0x1FEF64FF7E6F & 1 << b):
                        for bit in range(5):
                            stat_bit = b * 5 + bit
                            if (GameCanvas.stats[stat_bit >> 5] & i32(1 << (stat_bit & 0x1F))) != 0:
                                hidden_pct += 1
                mission_pct = mission_pct * 100 // 102
                hidden_pct = hidden_pct * 100 // 18
                ending_pct = ending_pct * 100 // 24
                warrior_pct = GameCanvas.general_count * 100 // 44
                dp = GameCanvas.text_lines[0]
                dp[0] = "Mission"
                dp[1] = "Accomplished"
                dp[2] = "" + str(mission_pct) + " %"
                dp[3] = "Hidden Mission"
                dp[4] = "Accomplished"
                dp[5] = "" + str(hidden_pct) + " %"
                dp[6] = "Ending Collected"
                dp[7] = "" + str(ending_pct) + " %"
                dp[8] = "Warrior Collected"
                dp[9] = "" + str(warrior_pct) + " %"
                dp[10] = "Total Accomplished"
                dp[11] = "" + str(mission_pct + hidden_pct + ending_pct + warrior_pct >> 2) + " %"
                GameCanvas.text_line_count[0] = 11
                GameCanvas.speech_line = 1
                GameCanvas.speech_pos[0] = GameCanvas.view_size.y
                GameCanvas.speech_done[0] = 0
                return
            # picture page: image + text scrolling up
            self.play_sound(2)
            GameCanvas.talk_lines[1] = ""
            GameCanvas.talk_lines[0] = ""
            if GameCanvas.story_ending != 0:
                b = -1
                if page != 0:
                    picture = 10
                else:
                    picture = 1
            elif 0 == GameCanvas.story_id and page == 5:
                picture = 0
                b = -1
                str_ = GameCanvas.gamestr(0)
            else:
                b = 0
                while b < 10:
                    if str_[b] == '|':
                        digits[b] = '\0'
                        break
                    digits[b] = str_[b]
                    b += 1
                picture = (GameCanvas.parse_int(digits) - 1) & 0xFFFF
            line = str_[b + 1:]
            self.word_wrap(line.encode("latin-1"), 200, 0)
            GameCanvas.images[35] = self.load_image(GameCanvas.scr_ui.get(2 + picture))
            GameCanvas.speech_pos[0] = GameCanvas.view_size.y
            GameCanvas.speech_pos[0] = 230
            GameCanvas.speech_done[0] = 0
            GameCanvas.speech_line = 0
            GameCanvas.story_fade = 0

    # ---- end of a mission (called by the combat when the mission is won / lost) -----------

    def finish_mission(self, won):  # c.java:1516-1607  (mission result: rewards, next chapter cq, ending)
        next_chapter = [0, 0, 0, 0, 0, 0, 11, 8, 0, 15,
                      15, 20, 17, 19, 19, 0, 30, 22, 35, 38,
                      39, 33, 33, 44]
        cz = GameCanvas.hero
        dz = GameCanvas.lords[GameCanvas.mission]
        if won != 0:
            cz.mission_progress[dz.id - 1] = i16(cz.mission_progress[dz.id - 1] + 5)
            if cz.mission_progress[dz.id - 1] > 100:
                cz.mission_progress[dz.id - 1] = 100
            GameCanvas.lords_done |= 1 << GameCanvas.lord_ids[GameCanvas.lord] - 1
            i = (GameCanvas.lord_ids[GameCanvas.lord] - 1) * 5 + GameCanvas.mission
            GameCanvas.stats[i >> 5] = GameCanvas.stats[i >> 5] | i32(1 << (i & 0x1F))
        GameCanvas.chapter = i8(GameCanvas.lord_ids[GameCanvas.lord])
        if dz.general < 200 and won != 0:
            self.start_victory_talk()
        else:
            if won != 0:
                i = dz.general - 200
            else:
                i = dz.reward - 200
            GameCanvas.redraw = 1
            self.free_hud()
            self.open_menu(2)
            GameCanvas.menu_items = GameCanvas.game_menu_items
            GameCanvas.menu_return = 0
            if i != 3 or 0 != GameCanvas.backpack_slot_of(502):
                GameCanvas.score |= 1 << i
            if 0 == i:
                b = 0
                best = cz.mission_progress[1]
                if cz.mission_progress[0] + cz.mission_progress[15] > best:
                    best = cz.mission_progress[0] + cz.mission_progress[15]
                    b = 1
                if cz.mission_progress[2] + cz.mission_progress[10] + cz.mission_progress[14] > best:
                    best = cz.mission_progress[2] + cz.mission_progress[10] + cz.mission_progress[14]
                    b = 2
                best = idiv(best - 20, 10)
                if best > 8:
                    best = 8
                elif best < 0:
                    best = 0
                cz.live_stat1 = i16(b)
                cz.live_stat2 = i16(best)
            GameCanvas.chapter = i8(next_chapter[i])
            if 0 == GameCanvas.chapter:
                for b in range(22):
                    cz.mission_progress[b] = 0
            if i == 2:
                GameCanvas.reward_item = 502
            elif self.rand(10) != 0:
                GameCanvas.reward_item = 0
            else:
                GameCanvas.reward_item = i16(101 + ((4 + 5 * self.rand(20)) if cz.level // 20 > 4 else (cz.level // 20 + 5 * self.rand(20))))
            left = 0
            GameCanvas.reward_skill = 0
            for mis in range(45):
                if 0 == (GameCanvas.missions_done & 1 << mis):
                    left += 1
            if left != 0:
                best = self.rand(left)
                b = 0
                for mis in range(45):
                    if 0 == (GameCanvas.missions_done & 1 << mis):
                        if best == b:
                            GameCanvas.missions_done |= 1 << mis
                            GameCanvas.reward_skill = i16(mis + 1)
                            break
                        b += 1
            if GameCanvas.reward_item != 0 and 0 == self.give_item(GameCanvas.reward_item, 1):
                GameCanvas.reward_item = 0
            self.start_story(i, 1)
        if GameCanvas.general_count != 0:
            cz.live_registered = 1
        cz.gold += dz.gold * 150 * (1 + (GameCanvas.difficulty ^ 0x1))
        self.fill_shop()
        GameCanvas.save_flag = 0
        self.save_game()

    def start_victory_talk(self):  # c.java:1609-1614  (after a won mission: talk with general dz.f, on the map)
        GameCanvas.talk_kind = 2
        GameCanvas.state = 5
        self.start_dialogue()
        GameCanvas.redraw = 1

    # =========================================================================================
    # The mission map (bV = 3) and its combat. With config.NO_ENEMIES (PORT-EXTRA, off by
    # default) no enemy is created: ez == 0 and every enemy loop below runs zero times.
    # =========================================================================================

    def draw_hud_balls(self):  # c.java:8-18  (HP / MP balls of the HUD: black cover from the top)
        cover = [idiv(35 * GameCanvas.hero.hp, GameCanvas.hero.max_hp), idiv(35 * GameCanvas.hero.mp, GameCanvas.hero.max_mp)]
        ball_pos = [[4, GameCanvas.canvas_size.y - 61], [201, GameCanvas.canvas_size.y - 61]]
        if GameCanvas.ball_cover is None:
            GameCanvas.ball_cover = self.load_image("ball_black")
        for b in range(2):
            if cover[b] != 0:
                cover[b] = 3 if cover[b] < 3 else cover[b]
            GameCanvas.draw_region(ball_pos[b][0], ball_pos[b][1], GameCanvas.ball_cover.getWidth(), GameCanvas.ball_cover.getHeight() - cover[b],
                         GameCanvas.ball_cover, 0, 0)

    @staticmethod
    def mark_dirty(x, y, w, h):  # c.java:20-37  (mark map cells dirty)
        col0 = idiv(x, 27) - GameCanvas.view_tx
        row0 = idiv(y, 27) - GameCanvas.view_ty
        col1 = idiv(x + w - 1, 27) - GameCanvas.view_tx
        row1 = idiv(y + h - 1, 27) - GameCanvas.view_ty
        if col0 < 0:
            col0 = 0
        if row0 < 0:
            row0 = 0
        if col1 > GameCanvas.view_tiles.x - 1:
            col1 = GameCanvas.view_tiles.x - 1
        if row1 > GameCanvas.view_tiles.y - 1:
            row1 = GameCanvas.view_tiles.y - 1
        for i in range(col0, col1 + 1):
            for row in range(row0, row1 + 1):
                GameCanvas.dirty[row][i] = 1

    def draw_hud_frame(self):  # c.java:39-46  (HUD frame)
        cx = GameCanvas.hud_frame
        GameCanvas.draw_region(0, 0, cx[1].getWidth(), cx[1].getHeight(), cx[1], 0, 0)
        GameCanvas.draw_region(GameCanvas.canvas_size.x - cx[1].getWidth(), 0, cx[1].getWidth(), cx[1].getHeight(), cx[1], 0, 0)
        GameCanvas.draw_region(0, 2, 120, 25, cx[3], 0, 0)
        GameCanvas.draw_region(GameCanvas.canvas_size.x - 120, 2, 120, 25, cx[4], 1, 0)
        GameCanvas.draw_region(GameCanvas.canvas_size.x // 2 - 120, GameCanvas.canvas_size.y - 61, 120, 61, cx[0], 0, 0)
        GameCanvas.draw_region(GameCanvas.canvas_size.x // 2, GameCanvas.canvas_size.y - 61, 120, 61, cx[2], 0, 0)

    def draw_frame(self):  # c.java:48-64  (draw one map frame)
        if 0 == GameCanvas.screen_fill:
            GameCanvas.engine.draw_object_layer()
        for b in range(81):
            GameCanvas.dirty[b // 9][b % 9] = 0
        if 0 == GameCanvas.screen_fill:
            GameCanvas.engine.draw_drops()
        self.draw_actors()
        self.draw_effects()
        if 0 == GameCanvas.screen_fill:
            self.draw_upper_layer()
        self.draw_arrows()
        self.draw_hud_frame()
        GameCanvas.engine.draw_hud()
        if GameCanvas.room_phase == 1:
            self.draw_exit_arrows()

    def draw_exit_arrows(self):  # c.java:66-79  (blinking exit arrows of the room)
        arrow_x = [GameCanvas.view_cx - 9, 5, GameCanvas.view_cx - 9, GameCanvas.view_size.x - 31]
        arrow_y = [GameCanvas.view_size.y - 31, GameCanvas.view_cy - 13, 5, GameCanvas.view_cy - 13]
        if GameCanvas.room_phase_timer < 1:
            GameCanvas.exit_blink = i16(GameCanvas.exit_blink + 1)
            if (GameCanvas.exit_blink & 0x2) != 0:
                for b in range(4):
                    if GameCanvas.cells[GameCanvas.cell].exits[b] != 0 and GameCanvas.images[21 + b] is not None:
                        img = GameCanvas.images[21 + b]
                        self.draw_map_region(img, arrow_x[b], arrow_y[b], img.getWidth(), img.getHeight(), 0, 0)
                        MapScene.mark_dirty(GameCanvas.camera.x + arrow_x[b], GameCanvas.camera.y + arrow_y[b], img.getWidth(), img.getHeight())

    def draw_arrows(self):  # c.java:81-122  (arrows flying: eC; only enemies shoot them)
        rect = Rect(0, 0, 0, 0)
        for b in range(3):
            eC = GameCanvas.arrows[b]
            if eC.active != 0:
                rect.x = i16(eC.pos[0].x - GameCanvas.camera.x + GameCanvas.view_x)
                rect.y = i16(eC.pos[0].y - GameCanvas.camera.y + GameCanvas.view_y) - 8
                rect.w = eC.w
                rect.h = eC.h
                GameCanvas.fill_rect(rect, GameCanvas.rgb(245, 206, 116))
                rect.w -= 1
                rect.h -= 1
                GameCanvas.fill_rect(rect, GameCanvas.rgb(240, 142, 53))
                rect.w += 1
                rect.h += 1
                MapScene.mark_dirty(eC.pos[0].x, eC.pos[0].y, eC.w, eC.h)
                bool_ = False
                if rect.x < GameCanvas.view_x:
                    rect.w = GameCanvas.view_x - rect.x
                    if rect.w > 0:
                        bool_ = True
                if rect.y < GameCanvas.view_y:
                    rect.h = GameCanvas.view_y - rect.y
                    if rect.h > 0:
                        bool_ = True
                if rect.x + rect.w >= GameCanvas.view_size.x + GameCanvas.view_x:
                    rect.x = GameCanvas.view_size.x + GameCanvas.view_x
                    rect.w = GameCanvas.view_x
                    bool_ = True
                if rect.y + rect.h >= GameCanvas.view_size.y + GameCanvas.view_y:
                    rect.y = GameCanvas.view_size.y + GameCanvas.view_y
                    rect.h = GameCanvas.view_y
                    bool_ = True
                if bool_:
                    GameCanvas.fill_rect(rect, 0)
                    MapScene.mark_dirty(eC.pos[0].x, eC.pos[0].y, eC.w, eC.h)

    def erase_arrows(self):  # c.java:124-141  (erase the arrows)
        for b in range(3):
            eC = GameCanvas.arrows[b]
            if eC.active != 0:
                i = eC.pos[1].x - GameCanvas.camera.x
                sy = eC.pos[1].y - GameCanvas.camera.y - 8
                if (eC.dir & 0x1) != 0:
                    w = 11
                    h = 3
                else:
                    w = 3
                    h = 11
                self.draw_map_region(GameCanvas.images[7], i, sy, w, h, i + GameCanvas.view_offset.x, sy + GameCanvas.view_offset.y)

    def draw_upper_layer(self):  # c.java:143-156  (upper tile layer over dirty cells)
        cE = GameCanvas.map
        for b in range(GameCanvas.view_tiles.x):
            for row in range(GameCanvas.view_tiles.y):
                if GameCanvas.dirty[row][b] != 0:
                    i = (GameCanvas.view_ty + row) * cE.size.w + GameCanvas.view_tx + b
                    if (cE.data[cE.layer_flags + i] & 0x2) != 0 and cE.data[cE.layer_upper + i] - 1 >= 0:
                        image = GameCanvas.tile_slots[cE.data[cE.layer_upper + i] - 1] - 1
                        self.draw_map_region(GameCanvas.tile_images[image], (GameCanvas.view_tx + b) * 27 - GameCanvas.camera.x, (GameCanvas.view_ty + row) * 27 - GameCanvas.camera.y, 27, 27, 0, 0)

    def draw_effects(self):  # c.java:158-226  (skill effects fh == 3 and potion / scroll effect dU)
        fx_dx = [3, -10, 10]
        fx_dy = [-6, 0, 5]
        cz = GameCanvas.hero
        if GameCanvas.hero_fx_kind == 3:
            i = cz.pos[0].x - GameCanvas.camera.x
            sy = cz.pos[0].y - GameCanvas.camera.y
            kind = cz.action[0]
            if kind == 27:
                if cz.frame[0] == 9:
                    i += consts.front_dx[cz.dir[1] >> 1]
                    sy += consts.front_dy[cz.dir[1] >> 1]
            elif kind in (28, 29, 30):
                i = GameCanvas.view_cx
                sy = GameCanvas.view_cy + 11
            fx_data = list(GameCanvas.hero_fx_data[GameCanvas.hero_fx_pos:GameCanvas.hero_fx_pos + GameCanvas.hero_fx_count])
            if len(fx_data) < GameCanvas.hero_fx_count:
                raise IndexError("System.arraycopy")
            self.draw_effect_frames(GameCanvas.hero_fx_parts, fx_data, GameCanvas.hero_fx_count, i, sy)
            for b in range(GameCanvas.hero_fx_count):
                MapScene.mark_dirty(cz.pos[0].x - GameCanvas.hero_fx_parts[b].ox, cz.pos[0].y - GameCanvas.hero_fx_parts[b].oy, GameCanvas.hero_fx_parts[b].w, GameCanvas.hero_fx_parts[b].h)
            GameCanvas.hero_fx_count = 1
        dU = GameCanvas.effect
        if dU.item != 0:
            part = 2
            kind = dU.item
            if kind == -2:
                fx_data = consts.fx_anim_27_end
                frames_file = 63
                dU.frame = dU.step
            elif kind == -1:
                fx_data = consts.fx_fire
                frames_file = 60
                dU.frame = dU.step
                part = 0
            elif kind in (10, 11):
                fx_data = consts.fx_item_10_11
                frames_file = 67
                if dU.step > 0:
                    dU.frame = i16(dU.step - 1 + (dU.dir << 2))
                else:
                    return
            else:
                fx_data = consts.fx_anim_17_19
                frames_file = 58
                dU.frame = i16(dU.step + 4)
            if dU.frame_data is None:
                dU.frame_data = fx_data
                dU.frames = self.load_frames(frames_file)
            while part < 3:
                i = dU.pos.x - GameCanvas.camera.x
                sy = dU.pos.y - GameCanvas.camera.y
                if dU.item == -1:
                    i += fx_dx[part]
                    sy += fx_dy[part]
                self.draw_effect_frame(dU.frames[dU.frame], dU.frame_data[dU.frame], i, sy)
                MapScene.mark_dirty(dU.pos.x - dU.frames[dU.frame].ox, dU.pos.y - dU.frames[dU.frame].oy, dU.frames[dU.frame].w, dU.frames[dU.frame].h)
                part += 1

    def draw_effect_frame(self, frame, image_id, x, y):  # c.java:228-234
        self.draw_effect_frames([frame], [image_id], 1, x, y)

    def draw_effect_frames(self, frames, image_ids, count, x, y):  # c.java:236-245
        loaded = 0
        image = None
        for b in range(count):
            if image_ids[b] != loaded:
                loaded = image_ids[b]
                if loaded != 0:
                    image = self.load_image(GameCanvas.scr_effect.get(loaded - 27))
            if loaded != 0:
                self.draw_map_region(image, x - frames[b].ox, y - frames[b].oy,
                               image.getWidth(), image.getHeight(), 0, 0)

    def draw_actors(self):  # c.java:247-260  (hero and enemies, sorted by y)
        bool_ = True
        cz = GameCanvas.hero
        cz.sprite_frame = cz.anims[cz.action[0]][cz.dir[0]][cz.frame[0]]
        for b in range(GameCanvas.actor_count):
            slot = GameCanvas.actor_slots[b]
            if bool_ and cz.pos[0].y < GameCanvas.actors[slot].pos[0].y:
                self.draw_hero()
                bool_ = False
            self.draw_enemy(slot)
        if bool_:
            self.draw_hero()
        self.draw_breaking()

    def draw_breaking(self):  # c.java:262-279  (breaking-object animation)
        for b in range(GameCanvas.breakable_count):
            cA = GameCanvas.breakables[b]
            if cA.active != 0 and cA.break_frame != 0:
                i = cA.pos.x - GameCanvas.camera.x
                sy = cA.pos.y - GameCanvas.camera.y
                spark = 2 - cA.break_frame
                if spark <= 3 and spark >= 0:
                    if GameCanvas.images[43] is None:
                        return
                    GameCanvas.engine.draw_spark(spark, i, sy)
                    MapScene.mark_dirty(cA.pos.x - GameCanvas.spark_frames[spark].ox, cA.pos.y - GameCanvas.spark_frames[spark].oy, GameCanvas.spark_frames[spark].w, GameCanvas.spark_frames[spark].h)
                else:
                    break

    def set_enemy_fx_parts(self, src, n):  # `fm = new y[src.length - n]; fm[b] = src[n + b]`
        if n > len(src):
            raise ValueError("NegativeArraySizeException")
        GameCanvas.enemy_fx_parts = src[n:]

    def draw_enemy(self, index):  # c.java:287-566  (draw an enemy: soldier 201-203 or general)
        ex = GameCanvas.actors[index]
        ex.action[0] = min(ex.action[0], len(ex.anims[ex.dir[0]]) - 1)
        i = ex.pos[0].x - GameCanvas.camera.x
        sy = ex.pos[0].y - GameCanvas.camera.y
        anim_frame = ex.anims[ex.dir[0]][ex.action[0]][ex.frame[0]]
        if ex.type > 200:
            if anim_frame < 100:
                if ex.type == 203:
                    ay = consts.squad_offsets[consts.dir8_to_dir4[ex.dir[0]]]
                    D = ex.frames[anim_frame]
                    for b in range(3):
                        self.draw_map_region(ex.image, i - D.ox + ay[b][0], sy - D.oy + ay[b][1], D.w, D.h, D.src_x, D.src_y)
                    az = consts.squad_dirty_box[consts.dir8_to_dir4[ex.dir[1]]]
                    MapScene.mark_dirty(ex.pos[0].x - D.ox + az[0], ex.pos[0].y - D.oy + az[1], D.w + az[2], D.h + az[3])
                else:
                    if ex.type == 202:
                        ex.image = GameCanvas.enemy_images[1]
                        ex.frames = GameCanvas.enemy_frames[1]
                    D = ex.frames[anim_frame]
                    self.draw_map_region(ex.image, i - D.ox, sy - D.oy, D.w, D.h, D.src_x, D.src_y)
                    MapScene.mark_dirty(ex.pos[0].x - D.ox, ex.pos[0].y - D.oy, D.w, D.h)
        else:
            if ex.action[0] < 6:
                bits = 1310732 if GameCanvas.general.side != 0 else 1053711
                weapon_front = bits >> anim_frame & 0x1
                head_set = GameCanvas.enemy_frames[4]
                body_set = GameCanvas.enemy_frames[3]
                weapon_set = GameCanvas.enemy_frames[5]
            else:
                b = 2 if GameCanvas.general.side != 0 else 3
                weapon_front = consts.general_frame_flags[(anim_frame >> 5 << 2) + b] >> (anim_frame & 0x1F) & 0x1
                head_set = GameCanvas.enemy_frames[7]
                body_set = GameCanvas.enemy_frames[6]
                weapon_set = GameCanvas.enemy_frames[8]
            action = ex.action[0]
            frame = ex.frame[0]
            if action == 6:
                if 2 < frame < 6:
                    GameCanvas.enemy_fx_kind = 1
                    GameCanvas.enemy_fx_image = GameCanvas.images[44]
                    self.set_enemy_fx_parts(GameCanvas.skill_frames, ex.dir[0] + (frame & 0x1))
            elif action == 7:
                if 4 < frame < 8:
                    GameCanvas.enemy_fx_kind = 1
                    GameCanvas.enemy_fx_image = GameCanvas.images[44]
                    self.set_enemy_fx_parts(GameCanvas.skill_frames, ex.dir[0] + (frame & 0x1))
            elif action == 8:
                if 0 < frame < 9:
                    GameCanvas.enemy_fx_kind = 1
                    GameCanvas.enemy_fx_image = GameCanvas.images[44]
                    self.set_enemy_fx_parts(GameCanvas.skill_frames, ex.dir[0] + (frame & 0x1))
            elif action in (9, 10):
                if frame > 3:
                    if frame == 4:
                        GameCanvas.enemy_fx_frames = self.load_frames(57)
                        GameCanvas.enemy_fx_data = consts.fx_anim_15_16
                    GameCanvas.enemy_fx_kind = 2
                    GameCanvas.enemy_fx_image = None
                    GameCanvas.enemy_fx_pos = i16(frame - 4)
                    self.set_enemy_fx_parts(GameCanvas.enemy_fx_frames, GameCanvas.enemy_fx_pos)
            elif action in (11, 12, 13):
                if 3 < frame < 10:
                    if frame == 4:
                        GameCanvas.enemy_fx_frames = self.load_frames(58)
                        GameCanvas.enemy_fx_data = consts.fx_anim_17_19
                    GameCanvas.enemy_fx_kind = 2
                    GameCanvas.enemy_fx_image = None
                    GameCanvas.enemy_fx_pos = i16(frame - 4)
                    self.set_enemy_fx_parts(GameCanvas.enemy_fx_frames, GameCanvas.enemy_fx_pos)
            elif action == 15:
                if frame == 5 or frame == 6:
                    if frame == 5:
                        GameCanvas.enemy_fx_frames = self.load_frames(59)
                        GameCanvas.enemy_fx_data = consts.fx_anim_21
                    GameCanvas.enemy_fx_kind = 1
                    GameCanvas.enemy_fx_image = None
                    GameCanvas.enemy_fx_pos = i16(frame - 5)
                    self.set_enemy_fx_parts(GameCanvas.enemy_fx_frames, GameCanvas.enemy_fx_pos)
            elif action == 16:
                if 1 < frame < 6:
                    GameCanvas.enemy_fx_kind = 1
                    GameCanvas.enemy_fx_image = GameCanvas.images[44]
                    self.set_enemy_fx_parts(GameCanvas.skill_frames, frame & 0x1)
            elif action == 17:
                if frame == 5 or frame == 6:
                    GameCanvas.enemy_fx_kind = 1
                    GameCanvas.enemy_fx_image = GameCanvas.images[44]
                    self.set_enemy_fx_parts(GameCanvas.skill_frames, frame - 5)
            elif action == 18:
                if frame == 5 or frame == 6:
                    if frame == 5:
                        GameCanvas.enemy_fx_frames = self.load_frames(61)
                        GameCanvas.enemy_fx_data = consts.fx_anim_24
                    GameCanvas.enemy_fx_kind = 1
                    GameCanvas.enemy_fx_image = None
                    GameCanvas.enemy_fx_pos = i16(frame - 5)
                    self.set_enemy_fx_parts(GameCanvas.enemy_fx_frames, GameCanvas.enemy_fx_pos)
            elif action in (20, 21):
                if action == 21 and frame == 9:        # case 21 falls through into case 20
                    GameCanvas.enemy_fx_frames = self.load_frames(63)
                    GameCanvas.enemy_fx_data = consts.fx_anim_27_end
                    GameCanvas.enemy_fx_pos = 2
                    GameCanvas.enemy_fx_kind = 2
                    self.set_enemy_fx_parts(GameCanvas.enemy_fx_frames, 1)
                if 1 < frame < 9:
                    if frame == 2:
                        GameCanvas.enemy_fx_frames = self.load_frames(62)
                        GameCanvas.enemy_fx_data = consts.fx_anim_26_27
                    GameCanvas.enemy_fx_kind = 2
                    GameCanvas.enemy_fx_image = None
                    GameCanvas.enemy_fx_pos = i16(frame - 2 + (ex.dir[0] >> 1) * 7)
                    self.set_enemy_fx_parts(GameCanvas.enemy_fx_frames, GameCanvas.enemy_fx_pos)
            if anim_frame < 180:
                body = body_set[anim_frame]
                self.draw_map_region(GameCanvas.general_mark, i - body.ox + idiv(body.w, 2) - 13, sy - body.oy + body.h - 5, GameCanvas.general_mark.getWidth(), GameCanvas.general_mark.getHeight(), 0, 0)
            if GameCanvas.enemy_fx_kind == 1:
                fx = GameCanvas.enemy_fx_parts[0]
                if GameCanvas.enemy_fx_image is not None:
                    self.draw_map_region(GameCanvas.enemy_fx_image, i - fx.ox, sy - fx.oy, fx.w, fx.h, fx.src_x, fx.src_y)
                else:
                    self.draw_effect_frames(GameCanvas.enemy_fx_parts, [GameCanvas.enemy_fx_data[GameCanvas.enemy_fx_pos]], 1, i, sy)
                MapScene.mark_dirty(ex.pos[0].x - fx.ox, ex.pos[0].y - fx.oy, fx.w, fx.h)
            GameCanvas.enemy_effect_drawn = 0
            GameCanvas.enemy_trail_drawn = 0
            if anim_frame < 180:
                if ex.defense_buff_ticks > 0 or ex.attack_buff_ticks > 0:
                    GameCanvas.enemy_effect_drawn = 1
                if GameCanvas.enemy_effect_drawn == 1:
                    bits = GameCanvas.frame % 3
                    shadow = GameCanvas.shadow_frames[bits]
                    self.draw_map_region(GameCanvas.shadow_image, i - shadow.ox, sy - shadow.oy + 3, shadow.w, shadow.h, shadow.src_x, shadow.src_y)
                    GameCanvas.enemy_trail_drawn = 1
                if weapon_front != 0:
                    self.draw_general_weapon(i, sy, weapon_set[anim_frame], index)
                body = body_set[anim_frame]
                head = head_set[anim_frame]
                self.draw_map_region(GameCanvas.hero.body_image, i - body.ox, sy - body.oy, body.w, body.h, body.src_x, body.src_y)
                self.draw_map_region(GameCanvas.boss_images[1], i - head.ox, sy - head.oy, head.w, head.h, head.src_x, head.src_y)
                MapScene.mark_dirty(ex.pos[0].x - body.ox, ex.pos[0].y - body.oy, body.w, body.h)
                if 0 == weapon_front:
                    self.draw_general_weapon(i, sy, weapon_set[anim_frame], index)
                if GameCanvas.enemy_effect_drawn == 1:
                    bits = 3 + GameCanvas.frame % 3
                    shadow = GameCanvas.shadow_frames[bits]
                    self.draw_map_region(GameCanvas.shadow_image, i - shadow.ox, sy - shadow.oy + 3, shadow.w, shadow.h, shadow.src_x, shadow.src_y)
                    GameCanvas.enemy_trail_drawn = 1
            ex.skill_fx = -1
            if ex.action[0] < 6:
                if 8 < anim_frame < 16 and (anim_frame & 0x1) != 0:
                    ex.skill_fx = i8(self.rand(3))
                    GameCanvas.engine.draw_weapon_trail(index, ex.skill_fx)
            else:
                action = ex.action[0]
                frame = ex.frame[0]
                if action == 6:
                    if 2 < frame < 6:
                        ex.skill_fx = 1
                elif action == 7:
                    if 4 < frame < 8:
                        ex.skill_fx = 1
                elif action == 8:
                    if frame in (2, 4, 6, 8):
                        ex.skill_fx = 1
                elif action == 14:
                    if (frame & 0x1) == 0:
                        ex.skill_fx = i8(self.rand(3))
                elif action == 15:
                    if frame == 5:
                        ex.skill_fx = 2
                elif action == 16:
                    if frame == 6:
                        ex.skill_fx = 2
                elif action == 19:
                    if (frame & 0x1) != 0:
                        ex.skill_fx = 2
                if -1 < ex.skill_fx < 100:
                    GameCanvas.engine.draw_weapon_trail(index, ex.skill_fx)
            if GameCanvas.enemy_fx_kind == 2:
                if ex.action[0] == 21 and ex.frame[0] == 9:
                    i += consts.front_dx[ex.dir[1] >> 1]
                    sy += consts.front_dy[ex.dir[1] >> 1]
                self.draw_effect_frames(GameCanvas.enemy_fx_parts, [GameCanvas.enemy_fx_data[GameCanvas.enemy_fx_pos]], 1, i, sy)
                MapScene.mark_dirty(ex.pos[0].x - GameCanvas.enemy_fx_parts[0].ox, ex.pos[0].y - GameCanvas.enemy_fx_parts[0].oy, GameCanvas.enemy_fx_parts[0].w, GameCanvas.enemy_fx_parts[0].h)
        if ex.on_fire != 0:
            fe = GameCanvas.fire_frames[ex.fire_frame]
            self.draw_effect_frame(fe, GameCanvas.fire_data[ex.fire_frame], i, sy)
            MapScene.mark_dirty(ex.pos[0].x - fe.ox, ex.pos[0].y - fe.oy, fe.w, fe.h)
        if ex.hit_fx_kind != 0:
            ex.hit_fx_frame = i8(ex.hit_fx_frame + 1)
            if ex.hit_fx_frame > 1:
                ex.hit_fx_kind = 0
                return
            i = ex.hit_fx_pos.x - GameCanvas.camera.x
            sy = ex.hit_fx_pos.y - GameCanvas.camera.y
            weapon_front = ex.hit_fx_frame + (ex.hit_fx_kind - 1 << 1)
            GameCanvas.engine.draw_spark(weapon_front, i, sy)
            spark = GameCanvas.spark_frames[weapon_front]
            MapScene.mark_dirty(ex.hit_fx_pos.x - spark.ox, ex.hit_fx_pos.y - spark.oy, spark.w, spark.h)

    def draw_general_weapon(self, x, y, frame, index):  # c.java:568-571  (a general's weapon)
        self.draw_map_region(GameCanvas.images[40 + GameCanvas.general.side], x - frame.ox, y - frame.oy, frame.w, frame.h, frame.src_x, frame.src_y)
        MapScene.mark_dirty(GameCanvas.actors[index].pos[0].x - frame.ox, GameCanvas.actors[index].pos[0].y - frame.oy, frame.w, frame.h)

    def set_hero_fx_parts(self, src, n):  # `fj = new y[src.length - n]; fj[b] = src[n + b]`
        if n > len(src):
            raise ValueError("NegativeArraySizeException")
        GameCanvas.hero_fx_parts = src[n:]

    def draw_hero(self):  # c.java:575-892  (draw the hero: shadow, body, weapon, effects)
        cz = GameCanvas.hero
        trail = -1
        fx_data = None
        if cz.action[0] < 12:
            bits = 5789684072952 if cz.weapon_kind != 0 else 8263870709823
            weapon_front = bits >> cz.sprite_frame & 0x1
            if 11 < cz.sprite_frame < 36 and (cz.sprite_frame & 0x1) != 0:
                trail = ((cz.sprite_frame - 12) & 0xFFFE) % 6 >> 1
            head_set = cz.head_frames
            body_set = cz.body_frames
            weapon_set = GameCanvas.hero_weapon_frames[cz.weapon_kind]
        else:
            bare = 0 if cz.weapon_kind != 0 else 1
            weapon_front = consts.general_frame_flags[(cz.sprite_frame >> 5 << 2) + bare] >> (cz.sprite_frame & 0x1F) & 0x1
            head_set = cz.head_frames2
            body_set = cz.body_frames2
            weapon_set = GameCanvas.hero_body_frames[cz.weapon_kind]
        action = cz.action[0]
        frame = cz.frame[0]
        # switch (cz.e[0]) - case 27 falls through into case 26 (no break in the original)
        if action == 2:
            GameCanvas.hero_fx_kind = 1
            GameCanvas.hero_fx_image = GameCanvas.images[44]
            self.set_hero_fx_parts(GameCanvas.skill_frames, cz.dir[0] + (frame & 0x1))
            if frame == 1:
                self.play_sound(7)
        elif action == 12:
            if 2 < frame < 6:
                trail = 1
                GameCanvas.hero_fx_kind = 1
                GameCanvas.hero_fx_image = GameCanvas.images[44]
                self.set_hero_fx_parts(GameCanvas.skill_frames, cz.dir[0] + (frame & 0x1))
        elif action == 13:
            if 4 < frame < 8:
                trail = 1
                GameCanvas.hero_fx_kind = 1
                GameCanvas.hero_fx_image = GameCanvas.images[44]
                self.set_hero_fx_parts(GameCanvas.skill_frames, cz.dir[0] + (frame & 0x1))
        elif action == 14:
            if 0 < frame < 9:
                if 0 == (frame & 0x1):
                    trail = 1
                GameCanvas.hero_fx_kind = 1
                GameCanvas.hero_fx_image = GameCanvas.images[44]
                self.set_hero_fx_parts(GameCanvas.skill_frames, cz.dir[0] + (frame & 0x1))
        elif action in (15, 16):
            if frame > 3:
                if GameCanvas.hero_fx_data is None:
                    GameCanvas.hero_fx_frames = self.load_frames(57)
                    GameCanvas.hero_fx_data = consts.fx_anim_15_16
                GameCanvas.hero_fx_kind = 2
                GameCanvas.hero_fx_image = None
                GameCanvas.hero_fx_pos = i16(frame - 4)
                self.set_hero_fx_parts(GameCanvas.hero_fx_frames, GameCanvas.hero_fx_pos)
        elif action in (17, 18, 19):
            if 3 < frame < 10:
                if GameCanvas.hero_fx_data is None:
                    GameCanvas.hero_fx_frames = self.load_frames(58)
                    GameCanvas.hero_fx_data = consts.fx_anim_17_19
                GameCanvas.hero_fx_kind = 3
                GameCanvas.hero_fx_image = None
                GameCanvas.hero_fx_pos = i16(frame - 4)
                self.set_hero_fx_parts(GameCanvas.hero_fx_frames, GameCanvas.hero_fx_pos)
        elif action == 20:
            if (frame & 0x1) != 0:
                trail = cz.combo
        elif action == 21:
            if frame == 5 or frame == 6:
                if frame == 5:
                    trail = 2
                    GameCanvas.hero_fx_frames = self.load_frames(59)
                    GameCanvas.hero_fx_data = consts.fx_anim_21
                GameCanvas.hero_fx_kind = 1
                GameCanvas.hero_fx_image = None
                GameCanvas.hero_fx_pos = i16(frame - 5)
                self.set_hero_fx_parts(GameCanvas.hero_fx_frames, GameCanvas.hero_fx_pos)
        elif action == 22:
            if 1 < frame < 6:
                GameCanvas.hero_fx_kind = 1
                GameCanvas.hero_fx_image = GameCanvas.images[44]
                self.set_hero_fx_parts(GameCanvas.skill_frames, frame & 0x1)
            elif frame == 6:
                trail = 2
        elif action == 23:
            if frame == 5 or frame == 6:
                GameCanvas.hero_fx_kind = 1
                GameCanvas.hero_fx_image = GameCanvas.images[44]
                self.set_hero_fx_parts(GameCanvas.skill_frames, frame - 5)
        elif action == 24:
            if frame == 5 or frame == 6:
                if GameCanvas.hero_fx_data is None:
                    GameCanvas.hero_fx_frames = self.load_frames(61)
                    GameCanvas.hero_fx_data = consts.fx_anim_24
                GameCanvas.hero_fx_kind = 1
                GameCanvas.hero_fx_image = None
                GameCanvas.hero_fx_pos = i16(frame - 5)
                self.set_hero_fx_parts(GameCanvas.hero_fx_frames, 1)
        elif action == 25:
            if (frame & 0x1) != 0:
                trail = 2
        elif action in (26, 27):
            if action == 27 and frame == 9:
                GameCanvas.hero_fx_frames = self.load_frames(63)
                GameCanvas.hero_fx_data = consts.fx_anim_27_end
                GameCanvas.hero_fx_kind = 3
                GameCanvas.hero_fx_pos = 1
                self.set_hero_fx_parts(GameCanvas.hero_fx_frames, 1)
            if 1 < frame < 9:
                if GameCanvas.hero_fx_data is None:
                    GameCanvas.hero_fx_frames = self.load_frames(62)
                    GameCanvas.hero_fx_data = consts.fx_anim_26_27
                GameCanvas.hero_fx_kind = 3
                GameCanvas.hero_fx_image = None
                GameCanvas.hero_fx_pos = i16(frame - 2 + (cz.dir[0] >> 1) * 7)
                self.set_hero_fx_parts(GameCanvas.hero_fx_frames, GameCanvas.hero_fx_pos)
        elif action == 28:
            if 3 < frame < 22:
                if GameCanvas.hero_fx_data is None:
                    GameCanvas.hero_fx_frames = self.load_frames(64)
                    GameCanvas.hero_fx_data = consts.fx_anim_28
                GameCanvas.hero_fx_kind = 3
                GameCanvas.hero_fx_image = None
                if frame > 9:
                    GameCanvas.hero_fx_pos = i16((frame - 10) * 3 + 6)
                    GameCanvas.hero_fx_count = 3
                else:
                    GameCanvas.hero_fx_pos = i16(frame - 4)
                self.set_hero_fx_parts(GameCanvas.hero_fx_frames, GameCanvas.hero_fx_pos)
        elif action == 29:
            if 6 < frame < 22:
                if GameCanvas.hero_fx_data is None:
                    GameCanvas.hero_fx_frames = self.load_frames(65)
                    GameCanvas.hero_fx_data = consts.fx_anim_29
                GameCanvas.hero_fx_kind = 3
                GameCanvas.hero_fx_image = None
                GameCanvas.hero_fx_pos = i16(frame - 7)
                self.set_hero_fx_parts(GameCanvas.hero_fx_frames, GameCanvas.hero_fx_pos)
        elif action == 30:
            if 3 < frame < 9:
                if GameCanvas.hero_fx_data is None:
                    GameCanvas.hero_fx_frames = self.load_frames(66)
                    GameCanvas.hero_fx_data = consts.fx_anim_30
                GameCanvas.hero_fx_kind = 3
                GameCanvas.hero_fx_image = None
                GameCanvas.hero_fx_pos = i16((frame - 4) * 5)
                self.set_hero_fx_parts(GameCanvas.hero_fx_frames, GameCanvas.hero_fx_pos)
                GameCanvas.hero_fx_count = 5
            elif 12 < frame < 15:
                if frame == 13:
                    GameCanvas.hero_fx_frames = self.load_frames(63)
                    GameCanvas.hero_fx_data = consts.fx_anim_27_end
                GameCanvas.hero_fx_kind = 3
                GameCanvas.hero_fx_image = None
                GameCanvas.hero_fx_pos = i16((frame - 13) * 5 + 2)
                self.set_hero_fx_parts(GameCanvas.hero_fx_frames, GameCanvas.hero_fx_pos)
                GameCanvas.hero_fx_count = 3
        i = cz.pos[0].x - GameCanvas.camera.x
        sy = cz.pos[0].y - GameCanvas.camera.y
        body = body_set[cz.sprite_frame]
        self.draw_map_region(GameCanvas.general_mark, i - body.ox + idiv(body.w, 2) - 13, sy - body.oy + body.h - 5, GameCanvas.general_mark.getWidth(), GameCanvas.general_mark.getHeight(), 0, 0)
        if GameCanvas.hero_fx_kind == 1:
            fx = GameCanvas.hero_fx_parts[0]
            if GameCanvas.hero_fx_image is not None:
                self.draw_map_region(GameCanvas.hero_fx_image, i - fx.ox, sy - fx.oy, fx.w, fx.h, fx.src_x, fx.src_y)
            else:
                fx_data = list(GameCanvas.hero_fx_data[GameCanvas.hero_fx_pos:])
                self.draw_effect_frames(GameCanvas.hero_fx_parts, fx_data, 1, i, sy)
            MapScene.mark_dirty(cz.pos[0].x - fx.ox, cz.pos[0].y - fx.oy, fx.w, fx.h)
        if GameCanvas.hero_picked_up == 1:
            shadow = GameCanvas.frame % 3
            shadow_frame = GameCanvas.shadow_frames[shadow]
            self.draw_map_region(GameCanvas.shadow_image, i - shadow_frame.ox, sy - shadow_frame.oy + 3, shadow_frame.w, shadow_frame.h, shadow_frame.src_x, shadow_frame.src_y)
            GameCanvas.hero_effect_drawn = 1
        if trail > -1:
            if 18 == (cz.dir[0] >> 1) * 6 + (trail << 1):
                GameCanvas.engine.draw_weapon_trail(-1, trail)
            elif cz.dir[0] == 4 and cz.action[0] != 25:
                GameCanvas.engine.draw_weapon_trail(-1, trail)
        if weapon_front != 0:
            GameCanvas.engine.draw_hero_weapon(i, sy, weapon_set[cz.sprite_frame])
        head = head_set[cz.sprite_frame]
        self.draw_map_region(cz.body_image, i - body.ox, sy - body.oy, body.w, body.h, body.src_x, body.src_y)
        self.draw_map_region(cz.head_image, i - head.ox, sy - head.oy, head.w, head.h, head.src_x, head.src_y)
        MapScene.mark_dirty(cz.pos[0].x - head.ox, cz.pos[0].y - head.oy, head.w, head.h)
        MapScene.mark_dirty(cz.pos[0].x - body.ox, cz.pos[0].y - body.oy, body.w, body.h)
        if 0 == weapon_front:
            GameCanvas.engine.draw_hero_weapon(i, sy, weapon_set[cz.sprite_frame])
        if trail > -1:
            if cz.action[0] == 25:
                GameCanvas.engine.draw_weapon_trail(-1, trail)
            elif 18 != (cz.dir[0] >> 1) * 6 + (trail << 1) and cz.dir[0] != 4:
                GameCanvas.engine.draw_weapon_trail(-1, trail)
        if GameCanvas.hero_picked_up == 1:
            shadow = 3 + GameCanvas.frame % 3
            shadow_frame = GameCanvas.shadow_frames[shadow]
            self.draw_map_region(GameCanvas.shadow_image, i - shadow_frame.ox, sy - shadow_frame.oy + 3, shadow_frame.w, shadow_frame.h, shadow_frame.src_x, shadow_frame.src_y)
        if GameCanvas.hero_fx_kind == 2:
            fx_data = list(GameCanvas.hero_fx_data[GameCanvas.hero_fx_pos:])
            self.draw_effect_frames(GameCanvas.hero_fx_parts, fx_data, 1, i, sy)
            MapScene.mark_dirty(cz.pos[0].x - GameCanvas.hero_fx_parts[0].ox, cz.pos[0].y - GameCanvas.hero_fx_parts[0].oy, GameCanvas.hero_fx_parts[0].w, GameCanvas.hero_fx_parts[0].h)
        elif cz.on_fire != 0:
            fx_data = list(GameCanvas.hero_fx_data[GameCanvas.hero_fx_pos:])
            fx_frames = GameCanvas.hero_fx_frames[cz.fire_frame:]
            self.draw_effect_frames(fx_frames, fx_data, 1, i, sy)
            fire = GameCanvas.hero_fx_frames[cz.fire_frame]
            MapScene.mark_dirty(cz.pos[0].x - fire.ox, cz.pos[0].y - fire.oy, fire.w, fire.h)
        if cz.hit_fx_kind != 0:
            cz.hit_fx_frame += 1
            if cz.hit_fx_frame > 1:
                cz.hit_fx_kind = 0
                return
            shadow = cz.hit_fx_frame
            i = cz.hit_fx_pos.x - GameCanvas.camera.x
            sy = cz.hit_fx_pos.y - GameCanvas.camera.y
            GameCanvas.engine.draw_spark(shadow, i, sy)
            spark = GameCanvas.spark_frames[shadow]
            MapScene.mark_dirty(cz.hit_fx_pos.x - spark.ox, cz.hit_fx_pos.y - spark.oy, spark.w, spark.h)

    def run_cell_scripts(self, tx, ty, tw, th):  # c.java:894-915  (run the scripts of cells)
        for b in range(th):
            for col in range(tw):
                i = tx + col + ty + b & 0x7
                while GameCanvas.cell_scripts[i].used != 0:
                    cell_x = GameCanvas.map.data[GameCanvas.cell_scripts[i].offset] & 0xFF
                    cell_y = GameCanvas.map.data[GameCanvas.cell_scripts[i].offset + 1] & 0xFF
                    if cell_x == tx + col and cell_y == ty + b:
                        offset = GameCanvas.cell_scripts[i].offset
                        end = i16(i16(GameCanvas.map.data[offset + 2] & 0xFF | (GameCanvas.map.data[offset + 3] & 0xFF) << 8) + 4)
                        pos = 4
                        while True:
                            pos += self.run_cell_script(GameCanvas.map.data[offset + pos], GameCanvas.map.data[offset + pos + 1], GameCanvas.map.data[offset + pos + 2], cell_x, cell_y)
                            if not pos < end:
                                break
                        break
                    i = GameCanvas.cell_scripts[i].next
                    if 0 == i:
                        break

    def run_cell_script(self, op, mission, enemy, tx, ty):  # c.java:917-926
        if op == 0:
            if GameCanvas.mission == mission - 1:
                self.create_enemy(enemy + 200, tx, ty, 4)
            return 3
        return 0

    def create_enemy(self, kind, tx, ty, dir):  # c.java:928-1015  (create an enemy)
        if config.NO_ENEMIES:
            # PORT-EXTRA (POW_NO_ENEMIES=1): the map without the combat - nobody is created
            return
        spawn_dx = [0, -56, 0, 56, 0]
        spawn_dy = [56, 0, -56, 0, 0]
        b = 0
        while b < GameCanvas.actor_count and 0 != GameCanvas.actors[b].active:
            b += 1
        ex = GameCanvas.actors[b]
        ex.active = 1
        if config.DECOMP_FIX["F16"] and ex.pos[1] is not ex.pos[0]:
            # DECOMP-FIX F16: the start position is written into ex.a[1], but the enemy AI
            # (ar.java:1340-1600) moves ex.a[0]. Both are the same object once ar.aC()
            # (ex.a[1] = ex.a[0], ar.java:1831) has run for this slot; a slot used for the
            # first time keeps a[0] at (0, 0), the enemy is pushed into the top-left corner
            # of the room and can stay stuck there behind a tent or a wall.
            ex.pos[1] = ex.pos[0]
        ex.pos[1].x = i16(tx * 27 + 12 + spawn_dx[dir])
        ex.pos[1].y = i16(ty * 27 + 20 + spawn_dy[dir])
        ex.target.x = ex.target.y = 0
        ex.dir[1] = ex.facing = i8((dir << 1) + 4 & 0x7)
        ex.dir[0] = ex.facing = i8((dir << 1) + 4 & 0x7)
        ex.action[1] = 0
        ex.action[0] = 0
        ex.frame[1] = 0
        ex.frame[0] = 0
        if kind == 201 and GameCanvas.rand_range(0, 2) != 0:
            kind = 203
        ex.type = i16(kind)
        ex.think_ticks = 14
        ex.alerted = 0
        ex.hit_fx_kind = 0
        ex.ai_mode = 0
        ex.skill_step = 0
        ex.on_fire = 0
        ex.skill_fx = 0
        ex.attack_buff = 0
        ex.defense_buff = 0
        ex.attack_buff_ticks = 0
        ex.defense_buff_ticks = 0
        if kind in (201, 202, 203):
            if kind == 202:            # case 202 falls through into case 201
                ex.alerted = 1
                ex.think_ticks = 15
            i = 0 if kind == 203 else kind - 201
            ex.anims = GameCanvas.char_anims[i]
            ex.image = GameCanvas.enemy_images[i]
            ex.frames = GameCanvas.enemy_frames[i]
            self.enemy_stats(kind - 201, b)
        else:
            if GameCanvas.lords[GameCanvas.mission].boss_type == kind:
                GameCanvas.boss_fight = 1
            GameCanvas.boss_spawned = 1
            GameCanvas.talk_kind = 1
            GameCanvas.talk_general = i16(kind)
            self.set_general(kind)
            self.start_dialogue()
            GameCanvas.redraw = 1
            GameCanvas.state = 5
            self.enemy_stats(4, b)
            ex.anims = GameCanvas.weapon_anims
            if GameCanvas.images[40 + GameCanvas.general.side] is None:
                GameCanvas.images[40 + GameCanvas.general.side] = self.load_image(GameCanvas.scr_char.get(42 + GameCanvas.general.side))
            if GameCanvas.boss_images[1] is None:
                GameCanvas.boss_images[1] = self.load_image(GameCanvas.scr_char.get(50 + GameCanvas.general.look - 1))
            GameCanvas.enemy_frames[3] = self.load_frames(68)
            GameCanvas.enemy_frames[4] = self.load_frames(70 + GameCanvas.general.look - 1)
            GameCanvas.enemy_frames[5] = self.load_frames(88 + (GameCanvas.general.side << 2))
            GameCanvas.enemy_frames[6] = self.load_frames(69)
            GameCanvas.enemy_frames[7] = self.load_frames(76 + GameCanvas.general.look - 1)
            GameCanvas.enemy_frames[8] = self.load_frames(90 + (GameCanvas.general.side << 2))
            ex.image = GameCanvas.hero.body_image
            ex.frames = GameCanvas.enemy_frames[2]
            GameCanvas.waves[1] = 1
        GameCanvas.actor_slots[GameCanvas.actor_count] = i16(b)
        GameCanvas.actor_count = i16(GameCanvas.actor_count + 1)
        if kind != 202:
            GameCanvas.enemies_alive = i16(GameCanvas.enemies_alive + 1)

    def enemy_stats(self, kind, index):  # c.java:1017-1041  (level, attack, defence, HP of a new enemy)
        attack_pct = [100, 100, 150]
        base_attack = [3, 2, 3]
        base_hp = [7, 5, 7]
        ex = GameCanvas.actors[index]
        if kind == 4:
            ex.level = i16(GameCanvas.hero.level + GameCanvas.waves[1])
            ex.attack = i16(idiv((GameCanvas.general.attack + ex.level - 1) * 6, 5))
            ex.defense = i16(idiv((GameCanvas.general.defense + ex.level - 1) * 6, 5))
            ex.hp = ex.max_hp = i16(GameCanvas.general.hp + (ex.level - 1) * 3)
            return
        if GameCanvas.hero.level < 21:
            i = GameCanvas.hero.level + GameCanvas.rand_range(0, 5) - 2
            ex.level = i16(i) if i > 0 else 1
        elif GameCanvas.hero.level < 41:
            ex.level = i16(GameCanvas.hero.level + self.rand(9) - 3)
        else:
            ex.level = i16(GameCanvas.hero.level + self.rand(16) - 5)
        ex.attack = i16(idiv((base_attack[kind] + ex.level) * attack_pct[kind], 100))
        ex.defense = i16(ex.level - 1)
        ex.hp = ex.max_hp = i16(base_hp[kind] + 3 * ex.level)

    @staticmethod
    def reset_actors():  # c.java:1043-1050
        GameCanvas.actor_count = 0
        GameCanvas.enemies_alive = 0
        for b in range(7):
            if GameCanvas.actors[b] is None:
                GameCanvas.actors[b] = Actor()
            GameCanvas.actors[b].active = 0

    def find_reachable(self, room_tx, room_ty, px, py):  # c.java:1052-1075  (reachable cells of the room)
        i = idiv(px, 27)
        ty = idiv(py, 27)
        if i < room_tx:
            i = room_tx
        elif i > room_tx + 6:
            i = room_tx + 6
        if ty < room_ty:
            ty = room_ty
        elif ty > room_ty + 6:
            ty = room_ty + 6
        for b in range(7):
            for row in range(7):
                GameCanvas.reachable[b][row] = 0
        for b in range(7):
            for row in range(7):
                cell = room_tx + b + (room_ty + row) * GameCanvas.map.size.w
                if (GameCanvas.map.data[GameCanvas.map.layer_flags + cell] & 0x1) != 0:
                    GameCanvas.reachable[b][row] = -1
        self.flood_fill(i - room_tx, ty - room_ty)

    def flood_fill(self, cx, cy):  # c.java:1077-1086  (flood fill)
        dx = [0, -1, 0, 1]
        dy = [1, 0, -1, 0]
        GameCanvas.reachable[cx][cy] = 1
        for b in range(4):
            nx = cx + dx[b]
            ny = cy + dy[b]
            if -1 < nx < 7 and -1 < ny < 7 and 0 == GameCanvas.reachable[nx][ny]:
                self.flood_fill(nx, ny)

    def load_rooms(self, map_no):  # c.java:1089-1115  (rooms of the map: exits, enemy waves)
        if config.DECOMP_FIX["F17"]:
            # DECOMP-FIX F17 (also here): `cE.b.a / 7 * cE.b.b / 7` is (width / 7) * (height / 7);
            # every N.arr holds exactly a whole number of missions of that many rooms. Literal,
            # maps 30 / 37 wide (Vengeance, ...) read past the end of the room data.
            room_count = idiv(GameCanvas.map.size.w, 7) * idiv(GameCanvas.map.size.h, 7)
        else:
            room_count = idiv(idiv(GameCanvas.map.size.w, 7) * GameCanvas.map.size.h, 7)
        data = GameCanvas.load_data_file(map_no - 1)
        i = 20 + room_count * GameCanvas.mission * 19
        B = GameCanvas.u8
        for b in range(room_count):
            if GameCanvas.cells[b] is None:
                GameCanvas.cells[b] = RoomCell()
            eO = GameCanvas.cells[b]
            eO.exits[0] = B(data[i])
            eO.exits[1] = B(data[i + 1])
            eO.exits[2] = B(data[i + 2])
            eO.exits[3] = B(data[i + 3])
            eO.max_enemies = B(data[i + 4])
            eO.wave_0 = B(data[i + 5])
            eO.wave_1 = B(data[i + 6])
            eO.wave_2 = B(data[i + 7])
            eO.wave_3 = B(data[i + 8])
            eO.wave_4 = B(data[i + 9])
            eO.wave_5 = B(data[i + 10])
            eO.wave_6 = B(data[i + 11])
            eO.wave_7 = B(data[i + 12])
            eO.wave_8 = B(data[i + 13])
            eO.wave_9 = B(data[i + 14])
            eO.wave_10 = B(data[i + 15])
            eO.wave_11 = B(data[i + 16])
            eO.general = B(data[i + 18])
            i += 19

    @staticmethod
    def hero_cell():  # c.java:1117-1120  (hero pixel position -> cell)
        GameCanvas.hero.room_pos[0].x = i16(idiv(GameCanvas.hero.pos[0].x, 27))
        GameCanvas.hero.room_pos[0].y = i16(idiv(GameCanvas.hero.pos[0].y - 6, 27))

    @staticmethod
    def free_map():  # c.java:1122-1125
        if GameCanvas.map is not None:
            GameCanvas.map.free()

    def load_map(self, map_no):  # c.java:1127-1162  (load map file #paramInt of mdat)
        map = MapData()
        MapScene.free_map()
        data = ResReader.read("/" + GameCanvas.scr_maps.get(map_no - 1))
        size = len(data)
        map.data = [b & 0xFF for b in data]
        if map.size is None:
            map.size = MapSize()
        map.size.w = map.data[0]
        map.size.h = map.data[1]
        map.size.extra = map.data[2]
        i = 3 + map.size.extra
        map.layer_ground = i
        layer_size = map.size.h * map.size.w
        i += layer_size
        map.layer_upper = i
        i += layer_size
        map.layer_objects = i
        i += layer_size
        map.layer_flags = i
        MapScene.reset_cell_scripts()
        i += layer_size
        if size > i:
            script_count = map.data[i]
            i += 1
            i += 2
            for b in range(script_count):
                op = map.data[i]
                arg = map.data[i + 1]
                script_len = map.data[i + 2] & 0xFF | map.data[i + 3] << 8 & 0xFF00
                MapScene.cell_script_slot(i, op, arg)
                i = i + 4 + script_len
        return map

    @staticmethod
    def reset_cell_scripts():  # c.java:1164-1171
        GameCanvas.cell_script_next = 8
        for b in range(50):
            if GameCanvas.cell_scripts[b] is None:
                GameCanvas.cell_scripts[b] = ScriptSlot()
            GameCanvas.cell_scripts[b].used = 0
            # PORT-EXTRA (hang fix): the original clears only .c and keeps the links .b of the
            # previous map. a_III() walks .b without looking at .c, so on a later map it can follow
            # an old link and set a node's .b to a lower index (even to itself): a cycle, and the
            # next a_III() into that bucket loops forever (the game freezes on a map load after
            # some missions; the Java code has the same bug). A cleared link ends every walk at a
            # node of this map, so a link always points to a higher index and cannot cycle.
            GameCanvas.cell_scripts[b].next = 0

    @staticmethod
    def cell_script_slot(offset, tx, ty):  # c.java:1173-1190  (hash of cell scripts by (x + y) & 7)
        i = tx + ty & 0x7
        if GameCanvas.cell_scripts[i] is None:
            GameCanvas.cell_scripts[i] = ScriptSlot()
        if GameCanvas.cell_scripts[i].used != 0:
            while GameCanvas.cell_scripts[i].next != 0:
                i = GameCanvas.cell_scripts[i].next
            GameCanvas.cell_scripts[GameCanvas.cell_script_next].used = 1
            GameCanvas.cell_scripts[GameCanvas.cell_script_next].offset = offset
            GameCanvas.cell_scripts[GameCanvas.cell_script_next].next = 0
            GameCanvas.cell_script_next = i16(GameCanvas.cell_script_next + 1)
            GameCanvas.cell_scripts[i].next = GameCanvas.cell_script_next
            return
        GameCanvas.cell_scripts[i].used = 1
        GameCanvas.cell_scripts[i].offset = offset
        GameCanvas.cell_scripts[i].next = 0
    # NOTE: in a_III the decompiled order sets cH[i].b = cI *after* cI++, so it points one past
    # the entry just filled and the second script of a bucket is never found by g_IIII (that
    # script's cell enemies are not spawned). Kept literal: it is the order of the bytecode.

    def draw_tiles(self, tiles_w, tiles_h, tx, ty, full):  # c.java:1197-1391
        # (draw the visible tiles into ct[7], load the tile images, set up the room the hero is in)
        cE = GameCanvas.map
        Gfx.set_graphics(GameCanvas.buffer_g)
        GameCanvas.breakable_count = 0
        for row in range(len(GameCanvas.breakables)):
            if GameCanvas.breakables[row] is None:
                GameCanvas.breakables[row] = Breakable()
            GameCanvas.breakables[row].active = 0
        for row in range(3):
            if GameCanvas.arrows[row] is None:
                GameCanvas.arrows[row] = Arrow()
            GameCanvas.arrows[row].active = 0
        GameCanvas.drop_count = 0
        for row in range(10):
            if GameCanvas.drops[row] is None:
                GameCanvas.drops[row] = Drop()
            GameCanvas.drops[row].item = 0
        GameCanvas.camera.x = i16(GameCanvas.view_tx * 27 + GameCanvas.view_offset.x)
        GameCanvas.camera.y = i16(GameCanvas.view_ty * 27 + GameCanvas.view_offset.y)
        GameCanvas.room_origin.x = i16(idiv(GameCanvas.view_tx, 7))
        GameCanvas.room_origin.y = i16(idiv(GameCanvas.view_ty, 7))
        row = 0
        for pass_no in range(2):
            k = 0
            for b in range(240):
                GameCanvas.tile_slots[b] = 0
            GameCanvas.images[4] = None
            if GameCanvas.tile_images is not None:
                for row in range(len(GameCanvas.tile_images)):
                    GameCanvas.tile_images[row] = None
                GameCanvas.tile_images = None
                GameCanvas.gc()
            for row in range(tiles_h):
                m = (ty + row) * cE.size.w + tx
                for col in range(tiles_w):
                    if pass_no != 0:
                        if (cE.data[cE.layer_flags + m + col] & 0x2) != 0 and cE.data[cE.layer_upper + m + col] != 0 and 0 == GameCanvas.tile_slots[cE.data[cE.layer_upper + m + col] - 1]:
                            k += 1
                            GameCanvas.tile_slots[cE.data[cE.layer_upper + m + col] - 1] = k
                        if cE.data[cE.layer_objects + m + col] != 0:
                            if 0 == GameCanvas.tile_slots[cE.data[cE.layer_objects + m + col] - 1]:
                                k += 1
                                GameCanvas.tile_slots[cE.data[cE.layer_objects + m + col] - 1] = k
                                k += 1
                                GameCanvas.tile_slots[cE.data[cE.layer_objects + m + col]] = k
                            if full != 0:
                                cE.data[cE.layer_objects + m + col] = 0
                            else:
                                if len(GameCanvas.breakables) <= GameCanvas.breakable_count:
                                    GameCanvas.breakables = GameCanvas.breakables + [None] * len(GameCanvas.breakables)
                                if GameCanvas.breakables[GameCanvas.breakable_count] is None:
                                    GameCanvas.breakables[GameCanvas.breakable_count] = Breakable()
                                cA = GameCanvas.breakables[GameCanvas.breakable_count]
                                cA.active = 1
                                cA.tile.x = i16(tx + col)
                                cA.tile.y = i16(ty + row)
                                cA.pos.x = i16(cA.tile.x * 27 + 12)
                                cA.pos.y = i16(cA.tile.y * 27 + 20)
                                cA.kind = cE.data[cE.layer_objects + m + col]
                                if cA.kind in (101, 113):
                                    cA.hp = 41
                                else:
                                    cA.hp = 21
                                cA.break_ticks = 0
                                cA.image = GameCanvas.tile_slots[cE.data[cE.layer_objects + m + col] - 1]
                                cA.break_frame = 0
                                GameCanvas.breakable_count = i16(GameCanvas.breakable_count + 1)
                    else:
                        if cE.data[cE.layer_ground + m + col] != 0 and 0 == GameCanvas.tile_slots[cE.data[cE.layer_ground + m + col] - 1]:
                            k += 1
                            GameCanvas.tile_slots[cE.data[cE.layer_ground + m + col] - 1] = k
                        if cE.data[cE.layer_upper + m + col] != 0 and 0 == GameCanvas.tile_slots[cE.data[cE.layer_upper + m + col] - 1]:
                            k += 1
                            GameCanvas.tile_slots[cE.data[cE.layer_upper + m + col] - 1] = k
            row = tiles_h if tiles_h > 0 else 0
            if GameCanvas.tile_images is not None:
                m = len(GameCanvas.tile_images)
                while row < m:
                    GameCanvas.tile_images[0] = None
                    row += 1
                GameCanvas.tile_images = None
            GameCanvas.gc()
            GameCanvas.tile_images = [None] * k
            for row in range(15):
                m = row << 4
                for col in range(16):
                    if GameCanvas.tile_slots[m + col] != 0:
                        GameCanvas.tile_images[GameCanvas.tile_slots[m + col] - 1] = self.load_image(GameCanvas.scr_tile.get(0 + row) + "_" + ("" if col >= 9 else "0") + str(col + 1))
            Gfx.set_graphics(GameCanvas.buffer_g)
            if 0 == pass_no:
                for row in range(tiles_h):
                    for col in range(tiles_w):
                        k = (ty + row) * cE.size.w + tx + col
                        if cE.data[cE.layer_ground + k] != 0:
                            m = GameCanvas.tile_slots[cE.data[cE.layer_ground + k] - 1] - 1
                            if m >= 0:
                                GameCanvas.draw_region_at(GameCanvas.tile_images[m], 0, 0, col * 27, row * 27, 27, 27)
                        if cE.data[cE.layer_upper + k] != 0:
                            m = GameCanvas.tile_slots[cE.data[cE.layer_upper + k] - 1] - 1
                            if m >= 0:
                                GameCanvas.draw_region_at(GameCanvas.tile_images[m], 0, 0, col * 27, row * 27, 27, 27)
        GameCanvas.images[4] = None
        if GameCanvas.state == 4 and GameCanvas.exit_blink < 7:
            Gfx.set_graphics(GameCanvas.screen_g)
            return
        exit_dx = [0, 0, 0, 6]
        exit_dy = [6, 0, 0, 0]
        exit_step = [1, -1, -1, 1]
        if config.DECOMP_FIX["F17"]:
            # DECOMP-FIX F17: lost parentheses, `(ce + 4) / 7 * cE.b.a / 7` is row * (width / 7),
            # as ar.X() steps the rows (eP +- width / 7). Literal, the 5th room row of a map
            # 9 wide gives eP 6 instead of 5: a room that does not exist (crash) or a stale
            # room of an earlier map.
            GameCanvas.cell = i16(idiv(GameCanvas.view_ty + 4, 7) * idiv(cE.size.w, 7) + idiv(GameCanvas.view_tx + 4, 7))
        else:
            GameCanvas.cell = i16(idiv(idiv(GameCanvas.view_ty + 4, 7) * cE.size.w, 7) + idiv(GameCanvas.view_tx + 4, 7))
        MapScene.reset_actors()
        for row in range(14):
            GameCanvas.waves[row] = 0
        eO = GameCanvas.cells[GameCanvas.cell]
        if 0 == full:
            GameCanvas.waves[0] = eO.wave_0
            GameCanvas.waves[1] = eO.wave_1
            GameCanvas.waves[2] = eO.wave_2
            GameCanvas.waves[3] = eO.wave_3
            GameCanvas.waves[4] = eO.wave_4
            GameCanvas.waves[5] = eO.wave_5
            GameCanvas.waves[6] = eO.wave_6
            GameCanvas.waves[7] = eO.wave_7
            GameCanvas.waves[8] = eO.wave_8
            GameCanvas.waves[9] = eO.wave_9
            GameCanvas.waves[10] = eO.wave_10
            GameCanvas.waves[11] = eO.wave_11
        GameCanvas.spawn_spot_count = 0
        i = idiv(GameCanvas.view_tx + 2, 7) * 7 + 1
        room_ty = idiv(GameCanvas.view_ty + 2, 7) * 7 + 1
        GameCanvas.scene.find_reachable(i, room_ty, GameCanvas.hero.pos[0].x, GameCanvas.hero.pos[0].y)
        for row in range(4):
            if eO.exits[row] != 0:
                k = i + exit_dx[row]
                m = room_ty + exit_dy[row]
                for b in range(7):
                    if (row & 0x1) != 0:
                        if GameCanvas.reachable[k - i][b] == 1:
                            cell = k + (m + b) * cE.size.w
                            if 0 == cE.data[cE.layer_objects + cell]:
                                cell += exit_step[row]
                                if (cE.data[cE.layer_flags + cell] & 0x1) == 0 and cE.data[cE.layer_objects + cell] == 0:
                                    if GameCanvas.spawn_spots[GameCanvas.spawn_spot_count] is None:
                                        GameCanvas.spawn_spots[GameCanvas.spawn_spot_count] = SpawnSpot()
                                    GameCanvas.spawn_spots[GameCanvas.spawn_spot_count].tx = k & 0xFFFF
                                    GameCanvas.spawn_spots[GameCanvas.spawn_spot_count].ty = (m + b) & 0xFFFF
                                    GameCanvas.spawn_spots[GameCanvas.spawn_spot_count].dir = row
                                    GameCanvas.spawn_spot_count = i16(GameCanvas.spawn_spot_count + 1)
                    elif GameCanvas.reachable[b][m - room_ty] == 1:
                        cell = k + b + m * cE.size.w
                        if 0 == cE.data[cE.layer_objects + cell]:
                            cell += exit_step[row] * cE.size.w
                            if (cE.data[cE.layer_flags + cell] & 0x1) == 0 and cE.data[cE.layer_objects + cell] == 0:
                                if GameCanvas.spawn_spots[GameCanvas.spawn_spot_count] is None:
                                    GameCanvas.spawn_spots[GameCanvas.spawn_spot_count] = SpawnSpot()
                                GameCanvas.spawn_spots[GameCanvas.spawn_spot_count].tx = (k + b) & 0xFFFF
                                GameCanvas.spawn_spots[GameCanvas.spawn_spot_count].ty = m & 0xFFFF
                                GameCanvas.spawn_spots[GameCanvas.spawn_spot_count].dir = row
                                GameCanvas.spawn_spot_count = i16(GameCanvas.spawn_spot_count + 1)
        if full != 0:
            GameCanvas.room_phase = 1
            GameCanvas.room_phase_timer = 5
        else:
            GameCanvas.scene.run_cell_scripts(idiv(GameCanvas.view_tx, 7) * 7 + 1, idiv(GameCanvas.view_ty, 7) * 7 + 1, 7, 7)
        for row in range(9):
            for b in range(9):
                GameCanvas.dirty[row][b] = 1
        Gfx.set_graphics(GameCanvas.screen_g)

    @staticmethod
    def make_exp_bars():  # c.java:1616-1641  (mission experience -> dZ bars)
        exp_table = GameCanvas.menus.load_exp_table()
        cz = GameCanvas.hero
        dz = GameCanvas.lords[GameCanvas.mission]
        cz.fame += GameCanvas.mission_exp
        GameCanvas.exp_bars[0] = i16(cz.exp * 100 // exp_table[0])
        for b in range(2):
            if b != 0 and GameCanvas.mission_seconds < dz.time_limit:
                GameCanvas.mission_exp += idiv((idiv(idiv(dz.time_limit - GameCanvas.mission_seconds, dz.time_limit), 10) + 1) * GameCanvas.mission_exp, 20)
            i = GameCanvas.mission_exp << 1 + (GameCanvas.difficulty ^ 0x1)
            total = 0
            for lv in range(10):
                total += exp_table[lv]
                if cz.exp + i < total:
                    rest = exp_table[lv] - total + cz.exp + i
                    GameCanvas.exp_bars[b + 1] = i16(idiv(rest * 100, exp_table[lv]) + lv * 100)
                    if GameCanvas.exp_bars[b + 1] < lv * 100 + 1:
                        GameCanvas.exp_bars[b + 1] = i16(lv * 100 + 1)
                    if b == 1:
                        cz.exp = rest
                    break
        GameCanvas.exp_bar_step = 0

    def tick_scene(self):  # c.java:1643-2136  (one map tick: erase, input, hero movement / actions)
        from pow.game.map_engine import MapEngine
        buff_div = [20, 20, 25]
        hit_frame = [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 6, 5, 5]
        i = -1
        skill = 0
        bool_ = True
        step_x = 0
        step_y = 0
        cz = GameCanvas.hero
        self.erase_breaking()
        self.erase_hero()
        self.erase_enemies()
        self.erase_drops()
        self.erase_hero_effects()
        self.erase_gold_and_clock()
        self.draw_potion_effect()
        if GameCanvas.room_phase == 1:
            self.erase_exit_arrows()
        key = GameCanvas.key_held
        if key in (-1, 50):
            i = 4
        elif key in (-3, 52):
            i = 2
        elif key in (-4, 54):
            i = 6
        elif key in (-2, 56):
            i = 0
        key = GameCanvas.key
        if config.NO_COMBAT and key in (49, 51, 55, 57, 48, -5, 53, 35, 42, -101, -102, -103, -104, -105):
            # PORT-EXTRA (POW_NO_COMBAT=1): attack, skill and potion keys do nothing
            key = None
        belt = -1
        if key in (-101, -102, -103, -104, -105) and config.SKILL_BAR:
            # PORT-EXTRA config.SKILL_BAR: Z X C V B (or a click on the belt) = belt slot 0..4,
            # used exactly like the slot of * / # below
            belt = -101 - key
            key = 42
        if key == 49:
            skill = cz.hotkeys[0]
        elif key == 51:
            skill = cz.hotkeys[1]
        elif key == 55:
            skill = cz.hotkeys[2]
        elif key == 57:
            skill = cz.hotkeys[3]
        elif key == 48:
            skill = cz.hotkeys[4]
        elif key in (-5, 53):
            skill = 3
        elif key in (35, 42):
            if 0 == GameCanvas.effect.item and cz.action[0] < 10:
                sel = belt if belt > -1 else cz.quick_keys[0 if GameCanvas.key == 42 else 1]
                GameCanvas.effect.item = cz.quick_slots[sel].item
                brk = False
                if GameCanvas.effect.item > 9:
                    if cz.action[0] > 1:
                        GameCanvas.effect.item = 0
                        brk = True
                    else:
                        cz.action[0] = 11
                elif GameCanvas.effect.item != 0:
                    self.play_sound(8)
                if not brk:
                    GameCanvas.effect.slot = i16(sel)
                    GameCanvas.effect.step = 0
                    GameCanvas.effect.pos.x = cz.pos[0].x
                    GameCanvas.effect.pos.y = cz.pos[0].y
                    GameCanvas.effect.dir = i16(consts.dir8_to_dir4[cz.dir[0]])
        elif key == -7:
            if GameCanvas.sound is not None:
                self.play_sound(-1)
                GameCanvas.stop_sound()
            GameCanvas.load_menu_texts()
            GameCanvas.map_mode.mode = 1
            GameCanvas.map_mode.sub = 0
            GameCanvas.menu[0] = 10
            GameCanvas.menu[2] = 0
            GameCanvas.menu[1] = 0
            GameCanvas.menu_count = 7
            GameCanvas.menu_items = GameCanvas.pause_items
            GameCanvas.redraw = 1
            GameCanvas.images[10] = self.load_image(GameCanvas.scr_ui.get(59))
            GameCanvas.images[17] = self.load_image(GameCanvas.scr_ui.get(27))
        if GameCanvas.effect.item > 0:
            if GameCanvas.effect.item > 9:
                cz.frame[0] = GameCanvas.effect.step
                return
            return
        GameCanvas.engine.spawn_next_enemy()
        cz.frame[0] = i16(cz.frame[0] + 1)
        GameCanvas.dir_history[0] = i
        if cz.anims[cz.action[0]][cz.dir[0]][cz.frame[0]] > 200:
            if cz.action[0] == 2:
                GameCanvas.dir_history[4] = GameCanvas.dir_history[3] = GameCanvas.dir_history[2] = GameCanvas.dir_history[1] = GameCanvas.dir_history[0] = -1
                i = -1
            elif cz.action[0] == 10:
                from pow.game.menus import Menus
                cz.frame[0] = 10
                if GameCanvas.talk_points != 0:
                    Menus.add_friendship(GameCanvas.talk_points, -5)
                GameCanvas.popups.setup_popup(22)
                GameCanvas.save_flag = 0
                self.save_game()
                return
            cz.frame[0] = 0
            GameCanvas.hero_fx_frames = None
            GameCanvas.hero_fx_data = None
            if cz.action[0] != 1:
                cz.action[0] = 0
        if (config.HOLD_TO_MOVE or Autopilot.on) and i == -1 and cz.action[0] < 2:
            # PORT-EXTRA (config.HOLD_TO_MOVE): the hero walks only while a direction key or the
            # mouse button is held; released = stand, still held after an attack = walk again
            from pow.game.midlet import Midlet
            held = Midlet.canvas.held_direction() if Midlet.canvas is not None else None
            if held is None:
                if cz.action[0] == 1:
                    cz.action[0] = 0
                    cz.frame[0] = 0
            else:
                hi = _HELD_DIR[held]
                if cz.action[0] == 0 or cz.facing != hi:
                    cz.dir[0] = cz.facing = hi
                    cz.action[0] = 1
                    cz.frame[0] = 0
        if cz.action[0] < 2:
            if i > -1:
                if MapEngine.check_run() != 0:
                    cz.action[0] = 2
                    cz.frame[0] = 0
                    cz.dir[0] = cz.facing = i
                    if GameCanvas.sound is not None:
                        GameCanvas.stop_sound()
                elif cz.facing == i:
                    cz.action[0] = cz.action[0] + 1 & 0x1
                    cz.frame[0] = 0
                else:
                    cz.dir[0] = cz.facing = i
                    cz.action[0] = 1
                    cz.frame[0] = 0
            if skill == 3:
                if cz.idle_ticks < 7:
                    cz.combo = (cz.combo + 1) % 3
                else:
                    cz.combo = 0
                cz.idle_ticks = 0
                cz.action[0] = 3 + cz.combo + (cz.weapon_kind ^ 0x1) * 3
                cz.frame[0] = 0
                cz.dir[0] = cz.facing = consts.dir8_to_dir4[cz.facing] << 1
            elif skill > 0 and MapEngine.skill_mp_cost(skill) != 0:
                cz.dir[0] = cz.facing = consts.dir8_to_dir4[cz.facing] << 1
                cz.action[0] = skill
                cz.frame[0] = 0
                if cz.action[0] in (15, 16, 21, 22, 23, 24, 25):
                    self.play_sound(11)
        move_dir = cz.facing
        action = cz.action[0]
        frame = cz.frame[0]
        if action == 1:
            step_x = consts.dir_dx8[move_dir]
            step_y = consts.dir_dy8[move_dir]
        elif action == 2:
            step_x = consts.dir_dx8[move_dir] << 2
            step_y = consts.dir_dy8[move_dir] << 2
        elif 3 <= action <= 8:
            step_x = idiv(consts.dir_dx8[move_dir], 3)
            step_y = idiv(consts.dir_dy8[move_dir], 3)
        elif action == 12:
            if 2 < frame < 6:
                step_x = consts.dir_dx8[move_dir] << 2
                step_y = consts.dir_dy8[move_dir] << 2
        elif action in (13, 14):
            fall14 = action == 14
            if action == 13:
                if 4 < frame < 8:
                    step_x = consts.dir_dx8[move_dir] << 2
                    step_y = consts.dir_dy8[move_dir] << 2
                    if step_x > 0:
                        step_x = GameCanvas.engine.step_until_free(cz.pos[0], step_x, 6)
                    elif step_x < 0:
                        step_x = GameCanvas.engine.step_until_free(cz.pos[0], step_x, 2)
                    if step_y > 0:
                        step_y = GameCanvas.engine.step_until_free(cz.pos[0], step_y, 0)
                    elif step_y < 0:
                        step_y = GameCanvas.engine.step_until_free(cz.pos[0], step_y, 4)
                    delta = GameCanvas.engine.keep_in_room(cz.pos[0], step_x, step_y)
                    step_x = delta[0]
                    step_y = delta[1]
                    cz.pos[0].x = i16(cz.pos[0].x + step_x)
                    cz.pos[0].y = i16(cz.pos[0].y + step_y)
                    fall14 = True       # no break: falls into case 14
            if fall14:
                if 0 < frame < 9:
                    step_x = consts.dir_dx8[move_dir]
                    step_y = consts.dir_dy8[move_dir]
        elif action == 10:
            if frame < 10:
                cz.pos[0].x = i16(cz.pos[0].x + (-1 if (frame & 0x1) != 0 else 1))
        elif action == 20:
            if 0 == (frame & 0x1):
                step_x = consts.dir_dx8[move_dir]
                step_y = consts.dir_dy8[move_dir]
        elif action == 9 and cz.hurt_ticks > 0:
            cz.hurt_ticks -= 1
            move_dir = cz.facing + 4 & 0x7
            step_x = consts.dir_dx8[move_dir] << 2
            step_y = consts.dir_dy8[move_dir] << 2
        elif action == 9 and frame == 1:
            move_dir = cz.facing + 4 & 0x7
            step_x = idiv(consts.dir_dx8[move_dir] * 3, 4)
            step_y = idiv(consts.dir_dy8[move_dir] * 3, 4)
        else:
            step_x = step_y = 0
        if step_x != 0 or step_y != 0:
            i = GameCanvas.engine.move(cz.pos[0], step_x, step_y, move_dir, -1)
            if cz.action[0] == 1:
                if cz.facing in (0, 2, 4, 6):
                    if F14:
                        # DECOMP-FIX F14: decompiled as `k = aw[i]; m = ax[i]; if (i == -1 &&
                        # (i = ar.c(..)) != -1 && (i = bc.a(.., k, m, i, -1)) > -1 && i < 8)`:
                        # aw[-1] when the hero walks into a wall. The step must use the new
                        # direction returned by ar.c() (slide around the corner).
                        if i == -1:
                            i = MapEngine.slide_corner(cz.pos[0], cz.dir[0], -1)
                            if i != -1:
                                step_x = consts.dir_dx8[i]
                                step_y = consts.dir_dy8[i]
                                i = GameCanvas.engine.move(cz.pos[0], step_x, step_y, i, -1)
                                if -1 < i < 8:
                                    cz.dir[0] = i
                    else:
                        if i < 0:
                            raise IndexError("ArrayIndexOutOfBoundsException: aw[%d]" % i)
                        step_x = consts.dir_dx8[i]
                        step_y = consts.dir_dy8[i]
                        if i == -1:
                            i = MapEngine.slide_corner(cz.pos[0], cz.dir[0], -1)
                            if i != -1:
                                i = GameCanvas.engine.move(cz.pos[0], step_x, step_y, i, -1)
                                if -1 < i < 8:
                                    cz.dir[0] = i
                elif cz.facing in (1, 3, 5, 7):
                    if i != -1 and i != 9:
                        cz.dir[0] = i
        action = cz.action[0]
        frame = cz.frame[0]
        if 3 <= action <= 8 or 21 <= action <= 24:
            if 3 <= action <= 8 and frame == hit_frame[action]:
                GameCanvas.engine.turn_to_nearest()
            if frame == hit_frame[action]:
                if action in (3, 4, 6, 7):
                    self.play_sound(15)
                elif action in (5, 8, 21, 22):
                    self.play_sound(16)
                elif action in (23, 24):
                    self.play_sound(9)
                GameCanvas.engine.hero_attack(0)
                GameCanvas.engine.hero_hits_breakables()
        elif action == 12:
            if 2 < frame < 6:
                if frame == 3:
                    self.play_sound(7)
                GameCanvas.engine.hero_attack(0)
                GameCanvas.engine.hero_hits_breakables()
        elif action == 13:
            if 4 < frame < 8:
                if frame == 5:
                    self.play_sound(7)
                GameCanvas.engine.hero_attack(0)
                GameCanvas.engine.hero_hits_breakables()
        elif action == 14:
            if frame in (2, 4, 6, 8):
                self.play_sound(15)
                GameCanvas.engine.hero_attack(0)
                GameCanvas.engine.hero_hits_breakables()
        elif action in (15, 16):
            if frame == 11:
                self.play_sound(8)
                if action == 15:
                    cz.hp += idiv(cz.max_hp * (4 + cz.skill_levels[3]), 25)
                else:
                    cz.hp += idiv(cz.max_hp * (9 + cz.skill_levels[4]), 20)
                MapEngine.clamp_hero_hp_mp()
        elif action in (17, 18, 19):
            if frame == 11:
                if action != 18:
                    cz.attack_buff = idiv(cz.attack * cz.skill_levels[action - 12], buff_div[action - 17])
                    if cz.attack_buff < 1:
                        cz.attack_buff = 1
                    if cz.skill_levels[action - 12] < 4:
                        cz.attack_buff_ticks = 50
                    elif cz.skill_levels[action - 12] < 8:
                        cz.attack_buff_ticks = 100
                    else:
                        cz.attack_buff_ticks = 150
                if action != 17:
                    cz.defense_buff = idiv(cz.defense * cz.skill_levels[action - 12], buff_div[action - 17])
                    if cz.defense_buff < 1:
                        cz.defense_buff = 1
                    if cz.skill_levels[action - 12] < 4:
                        cz.defense_buff_ticks = 50
                    elif cz.skill_levels[action - 12] < 8:
                        cz.defense_buff_ticks = 100
                    else:
                        cz.defense_buff_ticks = 150
            elif frame == 4:
                self.play_sound(12)
        elif action == 20:
            if (frame & 0x1) != 0:
                self.play_sound(15)
                if frame in (1, 5, 9):
                    cz.combo = 0
                else:
                    cz.combo = 2
                GameCanvas.engine.hero_attack(0)
                GameCanvas.engine.hero_hits_breakables()
        elif action == 25:
            if (frame & 0x1) != 0:
                self.play_sound(9)
                GameCanvas.engine.hero_attack(0)
                GameCanvas.engine.hero_hits_breakables()
        elif action in (26, 27):
            if frame == 8:
                if action == 27:
                    self.play_sound(9)
                GameCanvas.engine.hero_attack(0)
                GameCanvas.engine.hero_hits_breakables()
            if 1 < frame < 9:
                if frame == 2:
                    self.play_sound(13)
                bool_ = False
        elif action == 28:
            if frame == 22:
                GameCanvas.engine.hero_attack(0)
                GameCanvas.engine.hero_hits_breakables()
                GameCanvas.redraw = 1
            elif frame > 3:
                bool_ = False
                GameCanvas.redraw = 1
                GameCanvas.screen_fill = 1
                if frame == 6:
                    self.play_sound(13)
        elif action == 29:
            if frame == 22:
                GameCanvas.engine.hero_attack(0)
                GameCanvas.engine.hero_hits_breakables()
                GameCanvas.redraw = 1
            elif frame > 6:
                if frame == 7:
                    self.play_sound(14)
                bool_ = False
                GameCanvas.redraw = 1
                if frame == 12 or frame == 16:
                    GameCanvas.screen_fill = 2
                else:
                    GameCanvas.screen_fill = 1
        elif action == 30:
            if frame > 3:
                if frame == 4:
                    self.play_sound(11)
                elif frame == 13:
                    self.play_sound(9)
                if frame < 15:
                    bool_ = False
                    GameCanvas.screen_fill = 1
                GameCanvas.redraw = 1
                if frame == 9 or frame == 11:
                    GameCanvas.screen_fill = 2
                elif frame == 15:
                    GameCanvas.engine.hero_attack(0)
                    GameCanvas.engine.hero_hits_breakables()
        if bool_:
            GameCanvas.engine.tick_arrows()
            GameCanvas.scene.erase_arrows()
            GameCanvas.engine.pick_up_drops()
            GameCanvas.engine.tick_enemies()
            MapEngine.sort_actors()
        MapScene.hero_cell()

    def erase_breaking(self):  # c.java:2138-2148  (erase the breaking-object animation)
        for b in range(GameCanvas.breakable_count):
            cA = GameCanvas.breakables[b]
            if cA.active != 0 and cA.break_frame != 0:
                i = cA.pos.x - GameCanvas.camera.x
                sy = cA.pos.y - GameCanvas.camera.y
                spark = 2 - cA.break_frame
                cA.break_frame = i16(cA.break_frame - 1)
                self.erase_spark(spark, i, sy)

    def erase_spark(self, frame, x, y):  # c.java:2150-2152  (erase an eV frame from ct[7])
        spark = GameCanvas.spark_frames[frame]
        self.draw_map_region(GameCanvas.images[7], x - spark.ox, y - spark.oy, spark.w, spark.h,
                       x - spark.ox + GameCanvas.view_offset.x, y - spark.oy + GameCanvas.view_offset.y)

    def erase_exit_arrows(self):  # c.java:2154-2162  (erase the exit arrows)
        arrow_x = [GameCanvas.view_cx - 9, 5, GameCanvas.view_cx - 9, GameCanvas.view_size.x - 31]
        arrow_y = [GameCanvas.view_size.y - 31, GameCanvas.view_cy - 13, 5, GameCanvas.view_cy - 13]
        if GameCanvas.room_phase_timer < 1 and (GameCanvas.exit_blink & 0x2) != 0:
            for b in range(4):
                if GameCanvas.cells[GameCanvas.cell].exits[b] != 0 and GameCanvas.images[21 + b] is not None:
                    self.draw_map_region(GameCanvas.images[7], arrow_x[b], arrow_y[b], GameCanvas.images[21 + b].getWidth(),
                                   GameCanvas.images[21 + b].getHeight(), arrow_x[b] + GameCanvas.view_offset.x, arrow_y[b] + GameCanvas.view_offset.y)

    def erase_hero(self):  # c.java:2164-2253  (erase the hero at its previous position)
        cz = GameCanvas.hero
        if cz.action[1] < 12:
            head_set = cz.head_frames
            body_set = cz.body_frames
            weapon_set = GameCanvas.hero_weapon_frames[cz.weapon_kind]
        else:
            head_set = cz.head_frames2
            body_set = cz.body_frames2
            weapon_set = GameCanvas.hero_body_frames[cz.weapon_kind]
        i = cz.pos[1].x - GameCanvas.camera.x
        sy = cz.pos[1].y - GameCanvas.camera.y
        back = GameCanvas.images[7]
        ccx = GameCanvas.view_offset.x
        ccy = GameCanvas.view_offset.y
        head = head_set[cz.sprite_frame]
        body = body_set[cz.sprite_frame]
        weapon = weapon_set[cz.sprite_frame]
        self.draw_map_region(back, i - head.ox, sy - head.oy, head.w, head.h, i - head.ox + ccx, sy - head.oy + ccy)
        self.draw_map_region(back, i - body.ox, sy - body.oy, body.w, body.h, i - body.ox + ccx, sy - body.oy + ccy)
        self.draw_map_region(back, i - body.ox + idiv(body.w, 2) - 13, sy - body.oy + body.h - 5, 27, 11,
                       i - body.ox + ccx + idiv(body.w, 2) - 13, sy - body.oy + ccy + body.h - 5)
        self.draw_map_region(back, i - weapon.ox, sy - weapon.oy, weapon.w, weapon.h, i - weapon.ox + ccx, sy - weapon.oy + ccy)
        if GameCanvas.hero_picked_up == 1 or GameCanvas.hero_effect_drawn == 1:
            step = (GameCanvas.frame - 1) % 3
            shadow = GameCanvas.shadow_frames[step]
            self.draw_map_region(back, i - shadow.ox, sy - shadow.oy - 18, 40, 50, i - shadow.ox + ccx, sy - shadow.oy + ccy - 18)
            GameCanvas.hero_effect_drawn = 0
        if cz.action[1] < 12:
            if 11 < cz.sprite_frame < 36:
                step = cz.sprite_frame - 12
                if (step & 0x1) != 0:
                    step &= 0xFFFE
                    self.erase_weapon_trail(-1, step % 6 >> 1)
        else:
            step = -1
            action = cz.action[1]
            frame = cz.frame[1]
            if action == 12:
                if 2 < frame < 6:
                    step = 1
            elif action == 13:
                if 4 < frame < 8:
                    step = 1
            elif action == 14:
                if frame in (2, 4, 6, 8):
                    step = 1
            elif action == 20:
                if (frame & 0x1) != 0:
                    step = cz.combo
            elif action == 21:
                if frame == 5:
                    step = 2
            elif action == 22:
                if frame == 6:
                    step = 2
            elif action == 25:
                if (frame & 0x1) != 0:
                    step = 2
            if step > -1:
                self.erase_weapon_trail(-1, step)
        if cz.on_fire != 0:
            fire = GameCanvas.hero_fx_frames[cz.fire_frame]
            self.draw_map_region(back, i - fire.ox, sy - fire.oy, fire.w, fire.h, i - fire.ox + ccx, sy - fire.oy + ccy)
            cz.fire_frame += 1
            if cz.fire_frame > 5:
                cz.on_fire = 0
        if cz.hit_fx_kind != 0 and cz.hit_fx_frame > -1:
            i = cz.hit_fx_pos.x - GameCanvas.camera.x
            sy = cz.hit_fx_pos.y - GameCanvas.camera.y
            step = cz.hit_fx_frame
            self.erase_spark(step, i, sy)

    def erase_weapon_trail(self, index, step):  # c.java:2255-2281  (erase a weapon trail)
        if index > -1:
            pos = GameCanvas.actors[index].pos[1]
            if GameCanvas.actors[index].action[1] == 19:
                i = GameCanvas.actors[index].dir[1] + (GameCanvas.actors[index].frame[1] >> 1 << 1) & 0x7
            else:
                i = GameCanvas.actors[index].dir[1]
        else:
            pos = GameCanvas.hero.pos[1]
            if GameCanvas.hero.action[1] == 25:
                i = GameCanvas.hero.dir[1] + (GameCanvas.hero.frame[1] >> 1 << 1) & 0x7
            else:
                i = GameCanvas.hero.dir[1]
        frame = (i >> 1) * 6 + (step << 1)
        sx = pos.x - GameCanvas.camera.x
        sy = pos.y - GameCanvas.camera.y
        for b in range(2):
            part = GameCanvas.trail_frames[frame]
            self.draw_map_region(GameCanvas.images[7], sx - part.ox, sy - part.oy, part.w, part.h, sx - part.ox + GameCanvas.view_offset.x, sy - part.oy + GameCanvas.view_offset.y)
            frame += 1

    def erase_enemies(self):  # c.java:2283-2340  (erase the enemies)
        cc_a = GameCanvas.view_offset.x
        cc_b = GameCanvas.view_offset.y
        back = GameCanvas.images[7]
        for b in range(GameCanvas.actor_count):
            slot = GameCanvas.actor_slots[b]
            ex = GameCanvas.actors[slot]
            ex.action[0] = min(ex.action[0], len(ex.anims[ex.dir[0]]) - 1)
            anim_frame = ex.anims[ex.dir[1]][ex.action[1]][ex.frame[1]]
            i = ex.pos[1].x - GameCanvas.camera.x
            sy = ex.pos[1].y - GameCanvas.camera.y
            if ex.type > 200:
                if anim_frame < 180:
                    D = ex.frames[anim_frame]
                    if ex.type == 203:
                        az = consts.squad_dirty_box[consts.dir8_to_dir4[ex.dir[1]]]
                        self.draw_map_region(back, i - D.ox + az[0], sy - D.oy + az[1], D.w + az[2], D.h + az[3],
                                       i - D.ox + cc_a + az[0], sy - D.oy + cc_b + az[1])
                    else:
                        self.draw_map_region(back, i - D.ox, sy - D.oy, D.w, D.h, i - D.ox + cc_a, sy - D.oy + cc_b)
            else:
                if ex.action[1] < 6:
                    body_set = GameCanvas.enemy_frames[3]
                    head_set = GameCanvas.enemy_frames[4]
                    weapon_set = GameCanvas.enemy_frames[5]
                else:
                    body_set = GameCanvas.enemy_frames[6]
                    head_set = GameCanvas.enemy_frames[7]
                    weapon_set = GameCanvas.enemy_frames[8]
                if anim_frame < 180:
                    body = body_set[anim_frame]
                    self.draw_map_region(back, i - body.ox + idiv(body.w, 2) - 13, sy - body.oy + body.h - 4, 27, 11,
                                   i - body.ox + cc_a + idiv(body.w, 2) - 13, sy - body.oy + cc_b + body.h - 5)
                    if GameCanvas.enemy_effect_drawn == 1 or GameCanvas.enemy_trail_drawn == 1:
                        frame = (GameCanvas.frame - 1) % 3
                        shadow = GameCanvas.shadow_frames[frame]
                        self.draw_map_region(back, i - shadow.ox, sy - shadow.oy - 18, 40, 50, i - shadow.ox + cc_a, sy - shadow.oy + cc_b - 18)
                        GameCanvas.enemy_trail_drawn = 0
                else:
                    body = body_set[20]
                    self.draw_map_region(back, i - body.ox + idiv(body.w, 2) - 9, sy - body.oy + body.h - 4, 18, 7,
                                   i - body.ox + cc_a + idiv(body.w, 2) - 9, sy - body.oy + cc_b + body.h - 4)
                if anim_frame < 180:
                    for Y in (head_set[anim_frame], body_set[anim_frame], weapon_set[anim_frame]):
                        self.draw_map_region(back, i - Y.ox, sy - Y.oy, Y.w, Y.h, i - Y.ox + cc_a, sy - Y.oy + cc_b)
                self.erase_general_weapon(slot)
                if -1 < ex.skill_fx < 100:
                    self.erase_weapon_trail(slot, ex.skill_fx)
            if ex.on_fire != 0:
                fe = GameCanvas.fire_frames[ex.fire_frame]
                self.draw_map_region(back, i - fe.ox, sy - fe.oy, fe.w, fe.h, i - fe.ox + cc_a, sy - fe.oy + cc_b)
                ex.fire_frame = i8(ex.fire_frame + 1)
                if ex.fire_frame > 5:
                    ex.on_fire = 0
            if ex.hit_fx_kind != 0 and ex.hit_fx_frame > -1:
                i = ex.hit_fx_pos.x - GameCanvas.camera.x
                sy = ex.hit_fx_pos.y - GameCanvas.camera.y
                frame = ex.hit_fx_frame + (ex.hit_fx_kind - 1 << 1)
                self.erase_spark(frame, i, sy)

    def erase_general_weapon(self, index):  # c.java:2350-2421  (erase a general's weapon effect)
        ex = GameCanvas.actors[index]
        pos = ex.pos[1]          # (the same object: case 21 moves it, as in the original)
        GameCanvas.enemy_fx_kind = 0
        A = MapScene.frames_from
        action = ex.action[1]
        frame = ex.frame[1]
        if action == 6:
            if 2 < frame < 6:
                GameCanvas.enemy_fx_kind = 1
                GameCanvas.hero_fx_parts = A(GameCanvas.skill_frames, ex.dir[1] + (frame & 0x1))
        elif action == 7:
            if 4 < frame < 8:
                GameCanvas.enemy_fx_kind = 1
                GameCanvas.hero_fx_parts = A(GameCanvas.skill_frames, ex.dir[1] + (frame & 0x1))
        elif action == 8:
            if 0 < frame < 9:
                GameCanvas.enemy_fx_kind = 1
                GameCanvas.hero_fx_parts = A(GameCanvas.skill_frames, ex.dir[1] + (frame & 0x1))
        elif action in (9, 10):
            if frame > 3:
                GameCanvas.enemy_fx_kind = 1
                GameCanvas.hero_fx_parts = A(GameCanvas.enemy_fx_frames, frame - 4)
        elif action in (11, 12, 13):
            if 3 < frame < 10:
                GameCanvas.enemy_fx_kind = 3
                GameCanvas.hero_fx_parts = A(GameCanvas.enemy_fx_frames, frame - 4)
        elif action in (15, 18):
            if frame == 5 or frame == 6:
                GameCanvas.enemy_fx_kind = 1
                GameCanvas.hero_fx_parts = A(GameCanvas.enemy_fx_frames, frame - 5)
        elif action == 16:
            if 1 < frame < 6:
                GameCanvas.enemy_fx_kind = 1
                GameCanvas.hero_fx_parts = A(GameCanvas.skill_frames, frame & 0x1)
        elif action == 17:
            if frame == 5 or frame == 6:
                GameCanvas.enemy_fx_kind = 1
                GameCanvas.hero_fx_parts = A(GameCanvas.skill_frames, frame - 5)
        elif action in (20, 21):
            if action == 21 and frame == 9:        # case 21 falls through into case 20
                GameCanvas.enemy_fx_kind = 3
                GameCanvas.hero_fx_parts = A(GameCanvas.enemy_fx_frames, 1)
                pos.x = i16(pos.x + consts.front_dx[ex.dir[1] >> 1])
                pos.y = i16(pos.y + consts.front_dy[ex.dir[1] >> 1])
            if 1 < frame < 9:
                GameCanvas.enemy_fx_kind = 3
                GameCanvas.hero_fx_parts = A(GameCanvas.enemy_fx_frames, frame - 2 + (ex.dir[1] >> 1) * 7)
        if GameCanvas.enemy_fx_kind != 0:
            i = pos.x - GameCanvas.camera.x
            sy = pos.y - GameCanvas.camera.y
            GameCanvas.enemy_fx_kind = 0
            fj = GameCanvas.hero_fx_parts[0]
            self.draw_map_region(GameCanvas.images[7], i - fj.ox - 8, sy - fj.oy - 8, fj.w + 16, fj.h + 16,
                           i - fj.ox - 8 + GameCanvas.view_offset.x, sy - fj.oy - 8 + GameCanvas.view_offset.y)

    @staticmethod
    def frames_from(frames, start):  # c.java:2342-2348
        return frames[start:]

    def erase_drops(self):  # c.java:2423-2428  (erase the dropped items)
        for b in range(GameCanvas.drop_count):
            cC = GameCanvas.drops[b]
            if cC.item != 0:
                x = cC.pos.x - GameCanvas.camera.x - (cC.w >> 1)
                y = cC.pos.y - GameCanvas.camera.y - (cC.h >> 1)
                self.draw_map_region(GameCanvas.images[7], x, y, cC.w, cC.h, x + GameCanvas.view_offset.x, y + GameCanvas.view_offset.y)

    def erase_hero_effects(self):  # c.java:2430-2514  (erase the hero's weapon effects)
        cz = GameCanvas.hero
        pos = Point()
        pos.x = cz.pos[1].x
        pos.y = cz.pos[1].y
        GameCanvas.hero_fx_kind = 0
        action = cz.action[1]
        frame = cz.frame[1]
        A = MapScene.frames_from
        if action == 2:
            GameCanvas.hero_fx_kind = 1
            GameCanvas.hero_fx_parts = A(GameCanvas.skill_frames, cz.dir[1] + (frame & 0x1))
        elif action == 12:
            if 2 < frame < 6:
                GameCanvas.hero_fx_kind = 1
                GameCanvas.hero_fx_parts = A(GameCanvas.skill_frames, cz.dir[1] + (frame & 0x1))
        elif action == 13:
            if 4 < frame < 8:
                GameCanvas.hero_fx_kind = 1
                GameCanvas.hero_fx_parts = A(GameCanvas.skill_frames, cz.dir[1] + (frame & 0x1))
        elif action == 14:
            if 0 < frame < 9:
                GameCanvas.hero_fx_kind = 1
                GameCanvas.hero_fx_parts = A(GameCanvas.skill_frames, cz.dir[1] + (frame & 0x1))
        elif action in (15, 16):
            if frame > 3:
                GameCanvas.hero_fx_kind = 1
                GameCanvas.hero_fx_parts = A(GameCanvas.hero_fx_frames, frame - 4)
        elif action in (17, 18, 19):
            if 3 < frame < 10:
                GameCanvas.hero_fx_kind = 3
                GameCanvas.hero_fx_parts = A(GameCanvas.hero_fx_frames, frame - 4)
        elif action in (21, 24):
            if frame == 5 or frame == 6:
                GameCanvas.hero_fx_kind = 1
                GameCanvas.hero_fx_parts = A(GameCanvas.hero_fx_frames, frame - 5)
        elif action == 22:
            if 1 < frame < 6:
                GameCanvas.hero_fx_kind = 1
                GameCanvas.hero_fx_parts = A(GameCanvas.skill_frames, frame & 0x1)
        elif action == 23:
            if frame == 5 or frame == 6:
                GameCanvas.hero_fx_kind = 1
                GameCanvas.hero_fx_parts = A(GameCanvas.skill_frames, frame - 5)
        elif action in (26, 27):
            if action == 27 and frame == 9:        # case 27 falls through into case 26
                GameCanvas.hero_fx_kind = 3
                GameCanvas.hero_fx_parts = A(GameCanvas.hero_fx_frames, 1)
                pos.x = i16(pos.x + consts.front_dx[cz.dir[1] >> 1])
                pos.y = i16(pos.y + consts.front_dy[cz.dir[1] >> 1])
            if 1 < frame < 9:
                GameCanvas.hero_fx_kind = 3
                GameCanvas.hero_fx_parts = A(GameCanvas.hero_fx_frames, frame - 2 + (cz.dir[1] >> 1) * 7)
        if GameCanvas.hero_fx_kind != 0:
            i = pos.x - GameCanvas.camera.x
            sy = pos.y - GameCanvas.camera.y
            for b in range(GameCanvas.hero_fx_count):
                fj = GameCanvas.hero_fx_parts[b]
                self.draw_map_region(GameCanvas.images[7], i - fj.ox - 8, sy - fj.oy - 8, fj.w + 16, fj.h + 16,
                               i - fj.ox + GameCanvas.view_offset.x - 8, sy - fj.oy + GameCanvas.view_offset.y - 8)
            GameCanvas.hero_fx_kind = 0
            GameCanvas.hero_fx_count = 1

    def erase_message(self):  # c.java:2516-2523  (erase the message box dT)
        i = (Font.ascent() + Font.gap()) * len(GameCanvas.message.name) + 3
        self.draw_map_region(GameCanvas.images[7], GameCanvas.view_size.x - i - 7, 0, i + 7, 40, GameCanvas.view_size.x - i + GameCanvas.view_offset.x - 7, GameCanvas.view_offset.y)
        MapScene.mark_dirty(GameCanvas.camera.x + GameCanvas.view_size.x - i - 7, GameCanvas.camera.y, i + 7, 40)
        GameCanvas.message.ticks = i16(GameCanvas.message.ticks - 1)
        if GameCanvas.message.ticks < 1:
            GameCanvas.message.shown = 0

    def erase_gold_and_clock(self):  # c.java:2525-2537  (erase the gold counter and the clock)
        if GameCanvas.message.shown != 0:
            self.erase_message()
        else:
            i = GameCanvas.decimal_digits(GameCanvas.hero.kills_shown) * 10 + 1
            self.draw_map_region(GameCanvas.images[7], GameCanvas.view_size.x - 3 - i - 7, 1, i + 7, 29, GameCanvas.view_size.x - 3 - i + GameCanvas.view_offset.x - 7, 1 + GameCanvas.view_offset.y)
            MapScene.mark_dirty(GameCanvas.camera.x + GameCanvas.view_size.x - 3 - i - 7, GameCanvas.camera.y + 1, i + 7, 29)
            if GameCanvas.hero.kills > GameCanvas.hero.kills_shown:
                GameCanvas.hero.kills_shown += 1
        self.draw_map_region(GameCanvas.images[7], 0, 0, 60, 20, GameCanvas.view_offset.x, GameCanvas.view_offset.y)
        MapScene.mark_dirty(GameCanvas.camera.x, GameCanvas.camera.y, 60, 20)

    def draw_potion_effect(self):  # c.java:2539-2590  (potion / scroll effect dU)
        steps = [2, 10, 100, 2, 2, 2, 2, 2, 2, 2, 2, 2, 100, 100]
        frames_file = [63, 60]
        restores = [1, 1, 1, 2, 2, 2, 3, 3, 3]
        restore_pct = [30, 60, 100, 30, 60, 100, 30, 60, 100]
        dU = GameCanvas.effect
        if dU.item != 0:
            if dU.item <= 9 or dU.step != 0:
                hf = dU.frames[dU.frame]
                i = dU.pos.x - hf.ox - GameCanvas.camera.x
                sy = dU.pos.y - hf.oy - GameCanvas.camera.y
                w = hf.w
                h = hf.h
                if dU.item < 0:
                    if dU.item == -1:
                        i -= 10
                        sy -= 6
                        w = i16(w + 20)
                        h = i16(h + 11)
                        if dU.step in (1, 4, 7):
                            GameCanvas.engine.hero_attack(dU.item)
                    elif dU.step == 1:
                        GameCanvas.engine.hero_attack(dU.item)
                self.draw_map_region(GameCanvas.images[7], i, sy, w, h, i + GameCanvas.view_offset.x, sy + GameCanvas.view_offset.y)
            dU.step = i16(dU.step + 1)
            if dU.item > 9 and dU.step > 4:
                self.play_sound(9)
                dU.frame_data = None
                dU.frames = self.load_frames(frames_file[dU.item - 10])
                dU.pos.x = i16(dU.pos.x + consts.front_dx[dU.dir])
                dU.pos.y = i16(dU.pos.y + consts.front_dy[dU.dir])
                dU.item = i16(dU.item - 12)
                dU.step = 0
            if dU.step >= steps[dU.item + 2]:
                if dU.item > 0:
                    if (restores[dU.item - 1] & 0x1) != 0:
                        GameCanvas.hero.hp += idiv(GameCanvas.hero.max_hp * restore_pct[dU.item - 1], 100)
                    if (restores[dU.item - 1] & 0x2) != 0:
                        GameCanvas.hero.mp += idiv(GameCanvas.hero.max_mp * restore_pct[dU.item - 1], 100)
                    from pow.game.map_engine import MapEngine
                    MapEngine.clamp_hero_hp_mp()
                self.give_item(0, 0)
                dU.item = 0
                dU.frame_data = None
                dU.frames = None
