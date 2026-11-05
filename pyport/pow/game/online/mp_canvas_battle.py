"""g.java, part of MpCanvas: the battle: turns, fighters and their animations, timing bar, damage, HP bars, action cards.

A mixin of MpCanvas (pow/game/online/mp_canvas.py); the methods keep their `# g.java:FROM-TO`
comments. The module names below are set by mp_canvas.py: `MpCanvas` once the class exists,
the others by its _late_imports().
"""
from pow.game.online.rt import (
    _js,
    idiv,
    imod,
)

MpCanvas = None   # set by pow/game/online/mp_canvas.py
SpriteFrames = Consts = Draw = None   # set by mp_canvas._late_imports


class BattleMixin:
    @staticmethod
    def update_bars():  # g.java:3263
        MpCanvas.fighter_hp_delta[MpCanvas.loop_i] = (MpCanvas.fighter_hp_target[MpCanvas.loop_i] - MpCanvas.fighter_hp[MpCanvas.loop_i])
        MpCanvas.fighter_hp_step[MpCanvas.loop_i] = idiv(MpCanvas.fighter_hp_delta[MpCanvas.loop_i], 5)
        if MpCanvas.fighter_hp_step[MpCanvas.loop_i] == 0:
            if MpCanvas.fighter_hp_target[MpCanvas.loop_i] > MpCanvas.fighter_hp[MpCanvas.loop_i]:
                MpCanvas.fighter_hp_step[MpCanvas.loop_i] = 1
            elif MpCanvas.fighter_hp_target[MpCanvas.loop_i] < MpCanvas.fighter_hp[MpCanvas.loop_i]:
                MpCanvas.fighter_hp_step[MpCanvas.loop_i] = (-1)
        MpCanvas.fighter_mp_step[MpCanvas.loop_i] = idiv(((MpCanvas.fighter_mp_target[MpCanvas.loop_i] - MpCanvas.fighter_mp[MpCanvas.loop_i])), 5)
        if MpCanvas.fighter_mp_step[MpCanvas.loop_i] == 0:
            if MpCanvas.fighter_mp_target[MpCanvas.loop_i] > MpCanvas.fighter_mp[MpCanvas.loop_i]:
                MpCanvas.fighter_mp_step[MpCanvas.loop_i] = 1
                return
            if MpCanvas.fighter_mp_target[MpCanvas.loop_i] < MpCanvas.fighter_mp[MpCanvas.loop_i]:
                MpCanvas.fighter_mp_step[MpCanvas.loop_i] = (-1)

    def reset_turn(self):  # g.java:3285
        MpCanvas.anim_frame = 0
        MpCanvas.target2 = (-1)
        MpCanvas.damage_tick = (-1)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                MpCanvas.fighter_anim[MpCanvas.loop_i] = 0
                MpCanvas.fighter_anim_tick[MpCanvas.loop_i] = 0
                MpCanvas.fighter_anim_len[MpCanvas.loop_i] = 0
                MpCanvas.fighter_hp_delta[MpCanvas.loop_i] = 0
                if MpCanvas.fighter_slot[MpCanvas.loop_i] == MpCanvas.turn_bytes[(0 + MpCanvas.turn_rec)]:
                    MpCanvas.attacker = MpCanvas.loop_i
                    MpCanvas.fighter_hp_target[MpCanvas.loop_i] = MpCanvas.turn_hps[(0 + MpCanvas.turn_rec)]
                    MpCanvas.fighter_mp_target[MpCanvas.loop_i] = MpCanvas.turn_bytes[(8 + MpCanvas.turn_rec)]
                    MpCanvas.update_bars()
                if MpCanvas.fighter_slot[MpCanvas.loop_i] == MpCanvas.turn_bytes[(12 + MpCanvas.turn_rec)]:
                    MpCanvas.target = MpCanvas.loop_i
                    MpCanvas.fighter_hp_target[MpCanvas.loop_i] = MpCanvas.turn_hps[(4 + MpCanvas.turn_rec)]
                    MpCanvas.fighter_mp_target[MpCanvas.loop_i] = MpCanvas.turn_bytes[(20 + MpCanvas.turn_rec)]
                    MpCanvas.update_bars()
                    while True:
                        if MpCanvas.turn_bytes[(16 + MpCanvas.turn_rec)] == 1:
                            if MpCanvas.turn_actions[MpCanvas.target] == 1:
                                MpCanvas.target_reaction = 4
                                break
                            MpCanvas.target_reaction = 1
                        elif MpCanvas.turn_bytes[(16 + MpCanvas.turn_rec)] == 2:
                            MpCanvas.target_reaction = 5
                        break
                if (MpCanvas.turn_bytes[(24 + MpCanvas.turn_rec)] > 0) and (MpCanvas.fighter_slot[MpCanvas.loop_i] == MpCanvas.turn_bytes[(32 + MpCanvas.turn_rec)]):
                    MpCanvas.target2 = MpCanvas.loop_i
                    MpCanvas.fighter_hp_target[MpCanvas.loop_i] = MpCanvas.turn_hps[(8 + MpCanvas.turn_rec)]
                    MpCanvas.fighter_mp_target[MpCanvas.loop_i] = MpCanvas.turn_bytes[(40 + MpCanvas.turn_rec)]
                    MpCanvas.update_bars()
                    while True:
                        if MpCanvas.turn_bytes[(36 + MpCanvas.turn_rec)] == 1:
                            if MpCanvas.turn_actions[MpCanvas.target2] == 1:
                                MpCanvas.target2_reaction = 4
                                break
                            MpCanvas.target2_reaction = 1
                        elif MpCanvas.turn_bytes[(36 + MpCanvas.turn_rec)] == 2:
                            MpCanvas.target2_reaction = 5
                        break
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        if MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] in (3, 4, 5, 6, 7, 8):
            MpCanvas.fighter_anim[MpCanvas.attacker] = 8
        elif MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] in (2, 9, 10):
            MpCanvas.fighter_anim[MpCanvas.attacker] = 12
        elif MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] in (11, 12, 13):
            MpCanvas.fighter_anim[MpCanvas.attacker] = 13
        elif MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] == 0:
            MpCanvas.fighter_anim[MpCanvas.attacker] = 2
            MpCanvas.run_dx = idiv((((MpCanvas.canvas_w - 67) - 42)), Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]])
            MpCanvas.run_dy = (0 if (MpCanvas.room_mode == 0) else (0 if (idiv(MpCanvas.fighter_slot[MpCanvas.attacker], 2) == idiv(MpCanvas.turn_bytes[(12 + MpCanvas.turn_rec)], 2)) else (idiv(46, Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]]) if (idiv(MpCanvas.fighter_slot[MpCanvas.attacker], 2) == 0) else idiv((-46), Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]]))))
        MpCanvas.anim_length = Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]]

    def draw_notice(self):  # g.java:3746
        self.draw_buffer()
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 116, 76, 0)
        i = 0
        while i < 4:
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 31) + (12 * i)), MpCanvas.notice_lines[i], 0xFFFFFF)
            i = i + 1
        self.draw_ok_button(MpCanvas.center_y + 22)

    def draw_turn_fighters(self):  # g.java:3757
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i] and (MpCanvas.loop_i != MpCanvas.attacker):
                if MpCanvas.fighter_anim[MpCanvas.loop_i] == 0:
                    self.draw_fighter_idle(MpCanvas.screen_g)
                elif MpCanvas.fighter_anim[MpCanvas.loop_i] in (1, 4):
                    self.draw_fighter_hit()
                elif MpCanvas.fighter_anim[MpCanvas.loop_i] == 5:
                    self.draw_fighter_evade()
                elif MpCanvas.fighter_anim[MpCanvas.loop_i] == 6:
                    self.draw_fighter_dying()
                else:
                    self.draw_fighter_anim()
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.loop_i = MpCanvas.attacker
        if MpCanvas.fighter_anim[MpCanvas.attacker] in (2, 28):
            self.draw_fighter_run()
            return
        if MpCanvas.fighter_anim[MpCanvas.attacker] == 6:
            self.draw_fighter_dying()
            return
        self.draw_fighter_anim()

    def draw_fighter_hit(self):  # g.java:3801
        MpCanvas.anim_id = MpCanvas.fighter_anim[MpCanvas.loop_i]
        if MpCanvas.fighter_kind[MpCanvas.loop_i] == 2:
            MpCanvas.anim_id = (MpCanvas.anim_id + 21)
        MpCanvas.fighter_frame[MpCanvas.loop_i] = Consts.anim_first_frame[MpCanvas.anim_id]
        MpCanvas.fighter_x[MpCanvas.loop_i] -= 2
        MpCanvas.fighter_fx_frame[MpCanvas.loop_i] = (-1)
        self.draw_fighter(MpCanvas.screen_g, MpCanvas.loop_i)

    def draw_fighter_evade(self):  # g.java:3813
        MpCanvas.anim_id = (26 if (MpCanvas.fighter_kind[MpCanvas.loop_i] == 2) else 5)
        MpCanvas.fighter_frame[MpCanvas.loop_i] = Consts.anim_first_frame[MpCanvas.anim_id]
        if MpCanvas.fighter_anim_tick[MpCanvas.loop_i] == 0:
            MpCanvas.fighter_x[MpCanvas.loop_i] -= 6
            self.start_sound(3)
        elif MpCanvas.fighter_anim_tick[MpCanvas.loop_i] == 1:
            MpCanvas.fighter_x[MpCanvas.loop_i] -= 2
        MpCanvas.fighter_fx_frame[MpCanvas.loop_i] = (-1)
        self.draw_fighter(MpCanvas.screen_g, MpCanvas.loop_i)

    def draw_fighter_dying(self):  # g.java:3828
        MpCanvas.anim_id = (27 if (MpCanvas.fighter_kind[MpCanvas.loop_i] == 2) else 6)
        MpCanvas.fighter_frame[MpCanvas.loop_i] = (Consts.anim_first_frame[MpCanvas.anim_id] + MpCanvas.anim_frame)
        MpCanvas.fighter_fx_frame[MpCanvas.loop_i] = (-1)
        self.draw_fighter(MpCanvas.screen_g, MpCanvas.loop_i)

    def draw_fighter_run(self):  # g.java:3835
        MpCanvas.fighter_frame[MpCanvas.loop_i] = (Consts.anim_first_frame[23] if (MpCanvas.fighter_kind[MpCanvas.loop_i] == 2) else Consts.anim_first_frame[2])
        MpCanvas.fighter_x[MpCanvas.loop_i] += MpCanvas.run_dx
        MpCanvas.fighter_y[MpCanvas.loop_i] += MpCanvas.run_dy
        MpCanvas.fighter_fx_frame[MpCanvas.loop_i] = (-1)
        self.draw_fighter(MpCanvas.screen_g, MpCanvas.loop_i)

    def draw_fighter_anim(self):  # g.java:3845
        MpCanvas.anim_id = MpCanvas.fighter_anim[MpCanvas.loop_i]
        if (MpCanvas.fighter_kind[MpCanvas.loop_i] == 2) and (MpCanvas.anim_id == 3):
            MpCanvas.anim_id = 24
        if (MpCanvas.anim_id == 12) and (MpCanvas.anim_frame >= 4):
            MpCanvas.saved_anim_frame = MpCanvas.anim_frame
            MpCanvas.anim_frame = 4
        MpCanvas.fighter_frame[MpCanvas.loop_i] = (Consts.anim_first_frame[MpCanvas.anim_id] + MpCanvas.anim_frame)
        MpCanvas.tmp = Consts.anim_steps[MpCanvas.anim_id][((3 * MpCanvas.anim_frame) + 1)]
        MpCanvas.fighter_x[MpCanvas.loop_i] += ((((-1) if (((MpCanvas.tmp & 0x80)) > 0) else 1)) * (MpCanvas.tmp & 0x7F))
        MpCanvas.tmp = Consts.anim_steps[MpCanvas.anim_id][((3 * MpCanvas.anim_frame) + 2)]
        MpCanvas.fighter_y[MpCanvas.loop_i] += ((((-1) if (((MpCanvas.tmp & 0x80)) > 0) else 1)) * (MpCanvas.tmp & 0x7F))
        self.draw_fighter(MpCanvas.screen_g, MpCanvas.loop_i)
        if (MpCanvas.anim_id == 12) and (MpCanvas.anim_frame >= 4):
            MpCanvas.anim_frame = MpCanvas.saved_anim_frame

    def draw_fighter_idle(self, graphics):  # g.java:3867
        if MpCanvas.fighter_hp[MpCanvas.loop_i] > 0:
            if (((MpCanvas.state in {104, 105})) and (MpCanvas.fighter_kind[MpCanvas.loop_i] != 2)) and (MpCanvas.battle_won == 1):
                if MpCanvas.state_ticks < 3:
                    MpCanvas.fighter_frame[MpCanvas.loop_i] = (Consts.anim_first_frame[MpCanvas.anim_id] + MpCanvas.state_ticks)
                    MpCanvas.fighter_x[MpCanvas.loop_i] += ((((-1) if (((MpCanvas.tmp & 0x80)) > 0) else 1)) * (MpCanvas.tmp & 0x7F))
                    MpCanvas.fighter_y[MpCanvas.loop_i] += ((((-1) if (((MpCanvas.tmp & 0x80)) > 0) else 1)) * (MpCanvas.tmp & 0x7F))
            else:
                if imod(MpCanvas.state_ticks, 4) == MpCanvas.fighter_blink[MpCanvas.loop_i]:
                    MpCanvas.fighter_frame[MpCanvas.loop_i] = imod(idiv(MpCanvas.state_ticks, 4), 2)
                if (MpCanvas.fighter_frame[MpCanvas.loop_i] != 0) and (MpCanvas.fighter_frame[MpCanvas.loop_i] != 1):
                    MpCanvas.fighter_frame[MpCanvas.loop_i] = 0
        else:
            MpCanvas.fighter_frame[MpCanvas.loop_i] = (Consts.anim_first_frame[6] + 1)
        MpCanvas.fighter_fx_frame[MpCanvas.loop_i] = (-1)
        if ((MpCanvas.fighter_anim[MpCanvas.attacker] == 12) and (MpCanvas.loop_i == MpCanvas.target)) and (MpCanvas.anim_frame >= 4):
            MpCanvas.fighter_fx_frame[MpCanvas.loop_i] = ((10 + MpCanvas.anim_frame) - 4)
        self.draw_fighter(graphics, MpCanvas.loop_i)

    def draw_quotes(self, graphics, side):  # g.java:3895
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i] and (
                    imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == side or (side == 2 and ((imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == MpCanvas.fighter_slot[0]) if (MpCanvas.battle_won == 1) else (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) != MpCanvas.fighter_slot[0])))):
                self.draw_box(graphics, (0 if (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (MpCanvas.canvas_w - 60)), (12 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_h - 12) - 15)), 60, 15, 1)
                self.draw_text_centred((30 if (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (MpCanvas.canvas_w - 30)), (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), MpCanvas.fighter_name[MpCanvas.loop_i], 16400640)
                MpCanvas.box_x = MpCanvas.center_x
                MpCanvas.box_y = (38 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) - 11))
                self.draw_box(graphics, MpCanvas.box_x, MpCanvas.box_y, MpCanvas.canvas_w, 22, 0)
                self.draw_text_centred(MpCanvas.box_x, (MpCanvas.box_y - 5), (MpCanvas.fighter_quote_win[MpCanvas.loop_i] if (side == 2) else MpCanvas.fighter_quote_start[MpCanvas.loop_i]), 0xFFFFFF)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_fighter_record(self):  # g.java:3917
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 78, 86, 0)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 34), MpCanvas.fighter_name[MpCanvas.cur_slot], 0xFFFFFF)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 20), _js(_js(Consts.texts[27], "."), MpCanvas.fighter_level[MpCanvas.cur_slot]), 0xFFFFFF)
        self.draw_number0_on(MpCanvas.screen_g, (MpCanvas.center_x + 22), (MpCanvas.center_y + 12), MpCanvas.fighter_wins[MpCanvas.cur_slot])
        self.draw_text_left_on(MpCanvas.screen_g, (MpCanvas.center_x - 27), (MpCanvas.center_y + 11), Consts.texts[49], 0xFFFFFF)
        self.draw_number0_on(MpCanvas.screen_g, (MpCanvas.center_x + 22), (MpCanvas.center_y + 24), MpCanvas.fighter_losses[MpCanvas.cur_slot])
        self.draw_text_left_on(MpCanvas.screen_g, (MpCanvas.center_x - 27), (MpCanvas.center_y + 23), Consts.texts[50], 0xFFFFFF)

    def draw_fighters(self, graphics):  # g.java:3927
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                self.draw_fighter_idle(graphics)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_target_marker(self, graphics):  # g.java:3937
        if imod(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2) == 0:
            self.draw_text_centred_on(graphics, 30, (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), (MpCanvas.fighter_name[MpCanvas.target_cursor] if ((len(MpCanvas.fighter_alt_name[MpCanvas.target_cursor]) == 0) or (imod(MpCanvas.round_no, 2) == 0)) else MpCanvas.fighter_alt_name[MpCanvas.target_cursor]), 16400640)
            if imod(MpCanvas.state_ticks, 2) == 0:
                MpCanvas.draw_left_half_h(graphics, Consts.ui_dx[48], (((19 if (idiv(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2) == 0) else (MpCanvas.canvas_h - 19))) + Consts.ui_dy[48]), 12, MpCanvas.ui_images[48])
                return
            MpCanvas.draw_left_half_row(graphics, (Consts.ui_dx[48] + 1), (((19 if (idiv(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2) == 0) else (MpCanvas.canvas_h - 19))) + Consts.ui_dy[48]), MpCanvas.ui_images[48], 12, 1)
            return
        self.draw_text_centred_on(graphics, (MpCanvas.canvas_w - 30), (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), (MpCanvas.fighter_name[MpCanvas.target_cursor] if ((len(MpCanvas.fighter_alt_name[MpCanvas.target_cursor]) == 0) or (imod(MpCanvas.round_no, 2) == 0)) else MpCanvas.fighter_alt_name[MpCanvas.target_cursor]), 16400640)
        if imod(MpCanvas.state_ticks, 2) == 0:
            MpCanvas.draw_right_half_h(graphics, (MpCanvas.canvas_w - (1 + Consts.ui_dx[48])), (((19 if (idiv(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2) == 0) else (MpCanvas.canvas_h - 19))) + Consts.ui_dy[48]), 12, MpCanvas.ui_images[48])
            return
        MpCanvas.draw_right_half_row1(graphics, (MpCanvas.canvas_w - (2 + Consts.ui_dx[48])), (((19 if (idiv(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2) == 0) else (MpCanvas.canvas_h - 19))) + Consts.ui_dy[48]), 12, MpCanvas.ui_images[48])

    def draw_stage_intro(self):  # g.java:3955
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 102, 86, 0)
        self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 30), MpCanvas.stage_title, 0xFFFFFF)
        self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 15), _js(_js(_js(Consts.texts[26], MpCanvas.stage), "/"), MpCanvas.stage_count), 0xFFFFFF)
        MpCanvas.loop_i = 1
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                if MpCanvas.fighter_slot[MpCanvas.loop_i] == 1:
                    self.draw_text_centred((MpCanvas.center_x - 24), (MpCanvas.center_y + 4), MpCanvas.fighter_name[MpCanvas.loop_i], 0xFFFFFF)
                    self.draw_text_left((MpCanvas.center_x + 4), (MpCanvas.center_y + 4), _js(_js(Consts.texts[27], ""), MpCanvas.fighter_level[MpCanvas.loop_i]), 0xFFFFFF)
                elif MpCanvas.fighter_slot[MpCanvas.loop_i] == 3:
                    self.draw_text_centred((MpCanvas.center_x - 24), (MpCanvas.center_y + 20), MpCanvas.fighter_name[MpCanvas.loop_i], 0xFFFFFF)
                    self.draw_text_left((MpCanvas.center_x + 4), (MpCanvas.center_y + 20), _js(_js(Consts.texts[27], ""), MpCanvas.fighter_level[MpCanvas.loop_i]), 0xFFFFFF)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    @staticmethod
    def start_timing_bar():  # g.java:3974
        MpCanvas.tmp = imod(abs(MpCanvas.rng.nextInt()), 3)
        if MpCanvas.tmp == 0:
            MpCanvas.bar_speed = 4
        elif MpCanvas.tmp == 1:
            MpCanvas.bar_speed = 8
        else:
            MpCanvas.bar_speed = 5
        MpCanvas.set_timer(1)
        MpCanvas.bar_x = (MpCanvas.center_x - 44)
        MpCanvas.bar_shown = True

    def draw_timing_bar(self, graphics):  # g.java:3994
        if MpCanvas.bar_shown:
            bar_y = MpCanvas.center_y
            if MpCanvas.room_mode == 0:
                bar_y = (MpCanvas.screen_h - 26)
            self.draw_box(graphics, MpCanvas.center_x, (bar_y + 3), 110, 38, 0)
            Draw.draw_image(graphics, MpCanvas.ui_images[35], ((MpCanvas.center_x - 44) + Consts.ui_dx[35]), (bar_y + Consts.ui_dy[35]), 0)
            Draw.draw_image(graphics, MpCanvas.ui_images[36], ((MpCanvas.center_x - 44) + Consts.ui_dx[36]), (bar_y + Consts.ui_dy[36]), 0)
            Draw.draw_image(graphics, MpCanvas.ui_images[37], ((MpCanvas.center_x - 44) + Consts.ui_dx[37]), (bar_y + Consts.ui_dy[37]), 0)

    def draw_timing_cursor(self, graphics):  # g.java:4007
        bar_y = MpCanvas.center_y
        if MpCanvas.room_mode == 0:
            bar_y = (MpCanvas.screen_h - 26)
        if MpCanvas.state == 98:
            if MpCanvas.hit_score == 100:
                Draw.draw_image(graphics, MpCanvas.ui_images[52], (((MpCanvas.center_x - 44) + 72) + Consts.ui_dx[52]), (bar_y + Consts.ui_dy[52]), 0)
                self.start_sound(0)
            elif MpCanvas.hit_score == 20:
                Draw.draw_image(graphics, MpCanvas.ui_images[53], (((MpCanvas.center_x - 44) + 72) + Consts.ui_dx[53]), (bar_y + Consts.ui_dy[53]), 0)
            else:
                Draw.draw_image(graphics, MpCanvas.ui_images[49], ((MpCanvas.bar_x - 20) + Consts.ui_dx2[35]), ((bar_y - 11) + Consts.ui_dy2[35]), 0)
                self.start_sound(0)
        if imod(MpCanvas.state_ticks, 2) == 0:
            Draw.draw_image(graphics, MpCanvas.ui_images[38], (((MpCanvas.center_x - 44) + 72) + Consts.ui_dx[38]), (bar_y + Consts.ui_dy[38]), 0)
        Draw.draw_image(graphics, MpCanvas.ui_images[34], (MpCanvas.bar_x + Consts.ui_dx[34]), (bar_y + Consts.ui_dy[34]), 0)
        if (MpCanvas.state == 97) and (MpCanvas.bar_x > ((MpCanvas.center_x - 44) + 72)):
            self.stop_timing()

    def start_timing(self):  # g.java:4032
        MpCanvas.timer_ticks = 0
        MpCanvas.set_state(97)

    def stop_timing(self):  # g.java:4037
        MpCanvas.timer_ticks = 0
        if MpCanvas.chosen_action > 2:
            MpCanvas.hit_score = 0
        else:
            if (MpCanvas.bar_speed in {6, 7}) and (abs(((MpCanvas.center_x - 44) + 72) - MpCanvas.bar_x) <= idiv(MpCanvas.bar_speed, 2)):
                MpCanvas.bar_x = ((MpCanvas.center_x - 44) + 72)
            MpCanvas.hit_score = ((((20 + MpCanvas.bar_x) - MpCanvas.center_x) + 44) if (MpCanvas.bar_x < ((MpCanvas.center_x - 44) + 72)) else (100 if (MpCanvas.bar_x == ((MpCanvas.center_x - 44) + 72)) else 20))
        MpCanvas.set_state(98)

    @staticmethod
    def draw_sprite_frame(graphics, images, sets, frame):  # g.java:4050
        frames = sets[0]
        idx = 0
        if frame >= 400:
            idx = (frame - 400)
        elif frame >= 300:
            idx = (frame - 300)
        elif frame >= 200:
            idx = (frame - 200)
            frames = sets[2]
        elif frame >= 100:
            idx = (frame - 100)
            frames = sets[1]
        else:
            idx = frame
        if MpCanvas.draw_mirrored:
            Draw.draw_image_part(graphics, images[1], (MpCanvas.canvas_w - ((MpCanvas.draw_x - frames.anchor_x[idx]) + frames.w[idx])), (MpCanvas.draw_y - frames.anchor_y[idx]), frames.w[idx], frames.h[idx], frames.src_x[idx], frames.src_y[idx])
            return
        Draw.draw_image_part(graphics, images[0], (MpCanvas.draw_x - frames.anchor_x[idx]), (MpCanvas.draw_y - frames.anchor_y[idx]), frames.w[idx], frames.h[idx], frames.src_x[idx], frames.src_y[idx])

    def draw_fighter(self, graphics, index):  # g.java:4073
        pose = 0
        MpCanvas.draw_mirrored = (imod(MpCanvas.fighter_slot[index], 2) != 0)
        MpCanvas.draw_x = MpCanvas.fighter_x[index]
        MpCanvas.draw_y = MpCanvas.fighter_y[index]
        self.draw_fighter_effects(index, True)
        if MpCanvas.fighter_kind[index] != 2:
            self.load_sprite(MpCanvas.shadow_images, MpCanvas.shadow_frames, "sprshadow")
            MpCanvas.draw_sprite_frame(graphics, MpCanvas.shadow_images, MpCanvas.shadow_frames, MpCanvas.fighter_frame[index])
        weapon_behind = False
        if MpCanvas.fighter_kind[index] == 2:
            weapon_behind = Consts.mon_weapon_behind[imod(MpCanvas.fighter_frame[index], 100)]
            if weapon_behind:
                self.load_sprite_dir(MpCanvas.mon_weapon_images, MpCanvas.mon_weapon_frames, "spr_wp_mon", 0)
                MpCanvas.draw_sprite_frame(graphics, MpCanvas.mon_weapon_images, MpCanvas.mon_weapon_frames, MpCanvas.fighter_frame[index])
        else:
            pose = idiv(MpCanvas.fighter_frame[index], 100)
            if MpCanvas.fighter_weapon[index] == 0:
                if pose == 2:
                    weapon_behind = Consts.bare_weapon_behind_pose2[imod(MpCanvas.fighter_frame[index], 100)]
            else:
                weapon_behind = (Consts.weapon_behind_pose1[imod(MpCanvas.fighter_frame[index], 100)] if (pose == 1) else (Consts.weapon_behind_pose2[imod(MpCanvas.fighter_frame[index], 100)] if (pose == 2) else Consts.weapon_behind_pose0[imod(MpCanvas.fighter_frame[index], 100)]))
            if weapon_behind:
                self.load_sprite(MpCanvas.weapon_images[MpCanvas.fighter_weapon[index]], MpCanvas.weapon_frames[MpCanvas.fighter_weapon[index]], _js("sprwp", (MpCanvas.fighter_weapon[index] + 1)))
                MpCanvas.draw_sprite_frame(graphics, MpCanvas.weapon_images[MpCanvas.fighter_weapon[index]], MpCanvas.weapon_frames[MpCanvas.fighter_weapon[index]], MpCanvas.fighter_frame[index])
        if MpCanvas.fighter_kind[index] == 2:
            self.load_sprite_dir(MpCanvas.monster_images, MpCanvas.monster_frames, "spr_mon", 0)
            MpCanvas.draw_sprite_frame(graphics, MpCanvas.monster_images, MpCanvas.monster_frames, MpCanvas.fighter_frame[index])
        else:
            self.load_sprite(MpCanvas.shadow_images, MpCanvas.shadow_frames, "sprshadow")
            MpCanvas.draw_sprite_frame(graphics, MpCanvas.shadow_images, MpCanvas.shadow_frames, MpCanvas.fighter_frame[index])
            self.load_sprite(MpCanvas.body_images, MpCanvas.body_frames, "sprbody")
            MpCanvas.draw_sprite_frame(graphics, MpCanvas.body_images, MpCanvas.body_frames, MpCanvas.fighter_frame[index])
        pose = 0
        if MpCanvas.fighter_kind[index] != 2:
            if MpCanvas.fighter_kind[index] == 0:
                pose = MpCanvas.fighter_face[index]
            self.load_sprite(MpCanvas.head_images[pose], MpCanvas.head_frames[pose], _js("sprhead", (pose + 1)))
            MpCanvas.draw_sprite_frame(graphics, MpCanvas.head_images[pose], MpCanvas.head_frames[pose], MpCanvas.fighter_frame[index])
        if MpCanvas.fighter_present[index] and (MpCanvas.state != 105):
            if MpCanvas.fighter_status[index] == 11:
                self.load_status_effect()
                MpCanvas.draw_status_effect(graphics, 0)
            elif MpCanvas.fighter_status[index] == 12:
                self.load_status_effect()
                MpCanvas.draw_status_effect(graphics, 1)
            elif MpCanvas.fighter_status[index] == 13:
                self.load_status_effect()
                MpCanvas.draw_status_effect(graphics, 2)
        if not weapon_behind:
            if MpCanvas.fighter_kind[index] == 2:
                self.load_sprite_dir(MpCanvas.mon_weapon_images, MpCanvas.mon_weapon_frames, "spr_wp_mon", 0)
                MpCanvas.draw_sprite_frame(graphics, MpCanvas.mon_weapon_images, MpCanvas.mon_weapon_frames, MpCanvas.fighter_frame[index])
            else:
                self.load_sprite(MpCanvas.weapon_images[MpCanvas.fighter_weapon[index]], MpCanvas.weapon_frames[MpCanvas.fighter_weapon[index]], _js("sprwp", (MpCanvas.fighter_weapon[index] + 1)))
                MpCanvas.draw_sprite_frame(graphics, MpCanvas.weapon_images[MpCanvas.fighter_weapon[index]], MpCanvas.weapon_frames[MpCanvas.fighter_weapon[index]], MpCanvas.fighter_frame[index])
        self.draw_fighter_effects(index, False)

    def draw_fighter_effects(self, index, behind):  # g.java:4151
        if MpCanvas.fighter_kind[index] == 2:
            if not behind:
                self.load_sprite_dir(MpCanvas.mon_sword_images, MpCanvas.mon_sword_frames, "spr_sword_mon", 0)
                MpCanvas.draw_sprite_frame(MpCanvas.screen_g, MpCanvas.mon_sword_images, MpCanvas.mon_sword_frames, MpCanvas.fighter_frame[index])
                self.load_sprite_dir(MpCanvas.mon_effect_images, MpCanvas.mon_effect_frames, "spr_eff_mon", 0)
                MpCanvas.draw_sprite_frame(MpCanvas.screen_g, MpCanvas.mon_effect_images, MpCanvas.mon_effect_frames, MpCanvas.fighter_frame[index])
        else:
            pose = 0
            if not behind:
                self.load_sprite(MpCanvas.sword_images[MpCanvas.fighter_weapon[index]], MpCanvas.sword_frames[MpCanvas.fighter_weapon[index]], _js("sprsword", (MpCanvas.fighter_weapon[index] + 1)))
                MpCanvas.draw_sprite_frame(MpCanvas.screen_g, MpCanvas.sword_images[MpCanvas.fighter_weapon[index]], MpCanvas.sword_frames[MpCanvas.fighter_weapon[index]], MpCanvas.fighter_frame[index])
                self.load_sprite(MpCanvas.effect_images[0], MpCanvas.effect_frames[0], "spreff1")
                MpCanvas.draw_sprite_frame(MpCanvas.screen_g, MpCanvas.effect_images[0], MpCanvas.effect_frames[0], MpCanvas.fighter_frame[index])
            if behind == (Consts.eff2_behind_pose1[imod(MpCanvas.fighter_frame[index], 100)] if (((pose := idiv(MpCanvas.fighter_frame[index], 100))) == 1) else (Consts.eff2_behind_pose2[imod(MpCanvas.fighter_frame[index], 100)] if (pose == 2) else False)):
                self.load_sprite(MpCanvas.effect_images[1], MpCanvas.effect_frames[1], "spreff2")
                MpCanvas.draw_sprite_frame(MpCanvas.screen_g, MpCanvas.effect_images[1], MpCanvas.effect_frames[1], MpCanvas.fighter_frame[index])

    def step_turn_anim(self):  # g.java:4176
        if MpCanvas.damage_tick >= 5:
            MpCanvas.damage_tick = (-1)
            MpCanvas.loop_i = 0
            while MpCanvas.loop_i < 4:
                if MpCanvas.fighter_present[MpCanvas.loop_i] and ((MpCanvas.loop_i in (MpCanvas.attacker, MpCanvas.target)) or (MpCanvas.loop_i == MpCanvas.target2)):
                    if MpCanvas.fighter_hp[MpCanvas.loop_i] != MpCanvas.fighter_hp_target[MpCanvas.loop_i]:
                        MpCanvas.fighter_hp[MpCanvas.loop_i] = MpCanvas.fighter_hp_target[MpCanvas.loop_i]
                    if MpCanvas.fighter_mp[MpCanvas.loop_i] != MpCanvas.fighter_mp_target[MpCanvas.loop_i]:
                        MpCanvas.fighter_mp[MpCanvas.loop_i] = MpCanvas.fighter_mp_target[MpCanvas.loop_i]
                MpCanvas.loop_i = MpCanvas.loop_i + 1
        if MpCanvas.anim_frame >= MpCanvas.anim_length:
            MpCanvas.anim_frame = 0
            if MpCanvas.fighter_anim[MpCanvas.attacker] in (2, 17, 18, 19):
                self._anim_after_run_in()
            elif MpCanvas.fighter_anim[MpCanvas.attacker] == 8:
                self._anim_after_ready()
            elif MpCanvas.fighter_anim[MpCanvas.attacker] == 20:
                self._anim_after_charge()
            elif MpCanvas.fighter_anim[MpCanvas.attacker] in (3, 9, 10, 11, 14, 15, 16):
                self._anim_after_strike()
            elif MpCanvas.fighter_anim[MpCanvas.attacker] in (12, 13, 28):
                self._anim_after_run_back()
            elif MpCanvas.fighter_anim[MpCanvas.attacker] == 6:
                self._anim_after_dying()
            MpCanvas.anim_length = Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]]
        if MpCanvas.fighter_anim[MpCanvas.attacker] != 6:
            self.update_reactions()

    def _anim_after_run_in(self):  # step_turn_anim: the run to the target (2, 17-19) ended: start the action
        MpCanvas.fighter_x[MpCanvas.attacker] = (MpCanvas.canvas_w - 67)
        MpCanvas.fighter_y[MpCanvas.attacker] = (MpCanvas.center_y + 65)
        if MpCanvas.room_mode != 0:
            MpCanvas.fighter_y[MpCanvas.attacker] += ((((-1) if (idiv(MpCanvas.turn_bytes[(12 + MpCanvas.turn_rec)], 2) == 0) else 1)) * 23)
        if MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] == 3:
            MpCanvas.fighter_anim[MpCanvas.attacker] = 9
        elif MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] == 4:
            MpCanvas.fighter_anim[MpCanvas.attacker] = 10
        elif MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] == 5:
            MpCanvas.fighter_anim[MpCanvas.attacker] = 11
        elif MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] == 6:
            MpCanvas.fighter_anim[MpCanvas.attacker] = 14
        elif MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] == 7:
            MpCanvas.fighter_anim[MpCanvas.attacker] = 15
        elif MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] == 0:
            MpCanvas.fighter_anim[MpCanvas.attacker] = 3

    def _anim_after_ready(self):  # step_turn_anim: the ready pose (8) ended: run, cast or charge
        while True:
            if MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] in (3, 4, 5):
                MpCanvas.fighter_anim[MpCanvas.attacker] = 2
                MpCanvas.run_dx = idiv((((MpCanvas.canvas_w - 67) - 42)), Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]])
                if MpCanvas.room_mode == 0:
                    MpCanvas.run_dy = 0
                    break
                if idiv(MpCanvas.fighter_slot[MpCanvas.attacker], 2) == idiv(MpCanvas.turn_bytes[(12 + MpCanvas.turn_rec)], 2):
                    MpCanvas.run_dy = 0
                    break
                if idiv(MpCanvas.fighter_slot[MpCanvas.attacker], 2) == 0:
                    MpCanvas.run_dy = idiv(46, Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]])
                    break
                MpCanvas.run_dy = idiv((-46), Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]])
            elif MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] in (6, 7):
                if MpCanvas.room_mode == 0:
                    MpCanvas.fighter_anim[MpCanvas.attacker] = 17
                    break
                if idiv(MpCanvas.turn_bytes[(12 + MpCanvas.turn_rec)], 2) == idiv(MpCanvas.turn_bytes[(0 + MpCanvas.turn_rec)], 2):
                    MpCanvas.fighter_anim[MpCanvas.attacker] = 17
                    break
                if idiv(MpCanvas.turn_bytes[(12 + MpCanvas.turn_rec)], 2) == 1:
                    MpCanvas.fighter_anim[MpCanvas.attacker] = 18
                    break
                MpCanvas.fighter_anim[MpCanvas.attacker] = 19
            elif MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] == 8:
                MpCanvas.fighter_anim[MpCanvas.attacker] = 20
            break

    def _anim_after_charge(self):  # step_turn_anim: the charge (20) ended
        if MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] == 8:
            MpCanvas.fighter_anim[MpCanvas.attacker] = 16

    def _anim_after_strike(self):  # step_turn_anim: the strike (3, 9-11, 14-16) ended: counter-attack or run back
        if (MpCanvas.turn_bytes[(28 + MpCanvas.turn_rec)] == 3) and (MpCanvas.fighter_slot[MpCanvas.attacker] == MpCanvas.turn_bytes[(0 + MpCanvas.turn_rec)]):
            MpCanvas.tmp = MpCanvas.attacker
            MpCanvas.attacker = MpCanvas.target
            MpCanvas.target = MpCanvas.tmp
            MpCanvas.fighter_anim[MpCanvas.attacker] = 3
            MpCanvas.target_reaction = 1
            return
        MpCanvas.damage_tick = 0
        if MpCanvas.turn_bytes[(28 + MpCanvas.turn_rec)] == 3:
            MpCanvas.tmp = MpCanvas.attacker
            MpCanvas.attacker = MpCanvas.target
            MpCanvas.target = MpCanvas.tmp
            MpCanvas.fighter_anim[MpCanvas.target] = 0
            MpCanvas.place_fighter(MpCanvas.target)
        MpCanvas.fighter_anim[MpCanvas.attacker] = 28
        MpCanvas.run_dx = idiv(((42 - MpCanvas.fighter_x[MpCanvas.attacker])), Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]])
        if MpCanvas.room_mode == 0:
            MpCanvas.run_dy = 0
            return
        if idiv(MpCanvas.fighter_slot[MpCanvas.attacker], 2) == idiv(MpCanvas.turn_bytes[(12 + MpCanvas.turn_rec)], 2):
            MpCanvas.run_dy = 0
            return
        if idiv(MpCanvas.fighter_slot[MpCanvas.attacker], 2) == 0:
            MpCanvas.run_dy = idiv((-46), Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]])
            return
        MpCanvas.run_dy = idiv(46, Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]])

    def _anim_after_run_back(self):  # step_turn_anim: the run back (12, 13, 28) ended: deaths, next record
        MpCanvas.place_fighter(MpCanvas.attacker)
        MpCanvas.tmp = (-1)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                if (MpCanvas.fighter_anim[MpCanvas.attacker] == 13) and (imod(MpCanvas.fighter_slot[MpCanvas.attacker], 2) == imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2)):
                    MpCanvas.fighter_status[MpCanvas.loop_i] = MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)]
                    MpCanvas.fighter_status_ticks[MpCanvas.loop_i] = 3
                if (MpCanvas.fighter_hp[MpCanvas.loop_i] == 0) and (MpCanvas.fighter_hp_delta[MpCanvas.loop_i] != 0):
                    MpCanvas.tmp = MpCanvas.loop_i
                    MpCanvas.fighter_anim[MpCanvas.tmp] = 6
                    if imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == imod(MpCanvas.fighter_slot[0], 2):
                        MpCanvas.allies_alive = MpCanvas.allies_alive - 1
                    else:
                        MpCanvas.enemies_alive = MpCanvas.enemies_alive - 1
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        if MpCanvas.tmp > 0:
            if MpCanvas.fighter_anim[MpCanvas.attacker] != 6:
                MpCanvas.fighter_anim[MpCanvas.attacker] = 0
            MpCanvas.attacker = MpCanvas.tmp
            return
        MpCanvas.turn_rec = MpCanvas.turn_rec + 1
        self.next_turn_record()

    def _anim_after_dying(self):  # step_turn_anim: a dying fighter (6) ended: next record
        MpCanvas.turn_rec = MpCanvas.turn_rec + 1
        self.next_turn_record()

    def next_turn_record(self):  # g.java:4372
        if MpCanvas.turn_record_count == 0:
            MpCanvas.set_state(100)
            return
        if MpCanvas.turn_rec < MpCanvas.turn_record_count:
            MpCanvas.set_state(101)
            return
        MpCanvas.set_state(93)

    def update_reactions(self):  # g.java:4388
        if ((MpCanvas.fighter_anim[MpCanvas.attacker] != 12) and (MpCanvas.fighter_anim[MpCanvas.attacker] != 13)) and (MpCanvas.turn_bytes[(28 + MpCanvas.turn_rec)] != 3):
            if (MpCanvas.target != (-1)) and (MpCanvas.fighter_anim[MpCanvas.target] != 0):
                MpCanvas.fighter_anim_tick[MpCanvas.target] += 1
                if MpCanvas.fighter_anim_tick[MpCanvas.target] >= MpCanvas.fighter_anim_len[MpCanvas.target]:
                    MpCanvas.fighter_anim[MpCanvas.target] = 0
                    MpCanvas.place_fighter(MpCanvas.target)
            if (MpCanvas.target2 != (-1)) and (MpCanvas.fighter_anim[MpCanvas.target2] != 0):
                MpCanvas.fighter_anim_tick[MpCanvas.target2] += 1
                if MpCanvas.fighter_anim_tick[MpCanvas.target2] >= MpCanvas.fighter_anim_len[MpCanvas.target2]:
                    MpCanvas.fighter_anim[MpCanvas.target2] = 0
                    MpCanvas.place_fighter(MpCanvas.target2)
        if MpCanvas.fighter_anim[MpCanvas.attacker] in (3, 9, 10, 11, 14):
            if MpCanvas.target_reaction in (1, 4):
                if (MpCanvas.fighter_anim[MpCanvas.attacker] == 11) and (MpCanvas.anim_frame == 17):
                    self.start_reaction()
                    MpCanvas.fighter_anim_len[MpCanvas.target] = 3
                    return
                if imod(MpCanvas.anim_frame, 2) != 1:
                    return
                if (MpCanvas.fighter_anim[MpCanvas.attacker] == 11) and (MpCanvas.anim_frame > 10):
                    return
                self.start_reaction()
                MpCanvas.fighter_anim_len[MpCanvas.target] = 2
            elif MpCanvas.target_reaction == 5:
                if MpCanvas.turn_bytes[(28 + MpCanvas.turn_rec)] == 3:
                    if MpCanvas.anim_frame != 0:
                        return
                    MpCanvas.fighter_anim[MpCanvas.target] = 5
                    MpCanvas.fighter_anim_tick[MpCanvas.target] = 0
                    MpCanvas.fighter_anim_len[MpCanvas.target] = MpCanvas.anim_length
                else:
                    if imod(MpCanvas.anim_frame, 2) != 1:
                        return
                    self.start_reaction()
                    MpCanvas.fighter_anim_len[MpCanvas.target] = 2
            else:
                return
        elif MpCanvas.fighter_anim[MpCanvas.attacker] == 15:
            if MpCanvas.target_reaction in (1, 4):
                if MpCanvas.anim_frame != 2:
                    return
                self.start_reaction()
                MpCanvas.fighter_anim_len[MpCanvas.target] = 4
        elif MpCanvas.fighter_anim[MpCanvas.attacker] == 16:
            if MpCanvas.target_reaction in (1, 4):
                if MpCanvas.anim_frame != 8:
                    return
                self.start_reaction()
                MpCanvas.fighter_anim_len[MpCanvas.target] = 3
                if MpCanvas.target2 == (-1):
                    return
                MpCanvas.fighter_anim[MpCanvas.target2] = MpCanvas.target2_reaction
                MpCanvas.fighter_anim_tick[MpCanvas.target2] = 0
                MpCanvas.fighter_anim_len[MpCanvas.target2] = 3
        elif MpCanvas.fighter_anim[MpCanvas.attacker] == 12:
            if MpCanvas.anim_frame != 4:
                return
            MpCanvas.damage_tick = 0
            self.start_sound(6)
            if MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] == 2:
                return
        elif MpCanvas.fighter_anim[MpCanvas.attacker] == 13:
            if (MpCanvas.anim_frame == 4) and (MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] == 13):
                MpCanvas.loop_i = 0
                while MpCanvas.loop_i < 4:
                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                self.start_sound(5)
                return
            if MpCanvas.anim_frame == 7:
                MpCanvas.loop_i = 0
                while MpCanvas.loop_i < 4:
                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                self.start_sound(5)
                return
            if MpCanvas.anim_frame != 5:
                return
            MpCanvas.damage_tick = 0

    def start_reaction(self):  # g.java:4501
        MpCanvas.fighter_anim[MpCanvas.target] = MpCanvas.target_reaction
        MpCanvas.fighter_anim_tick[MpCanvas.target] = 0
        if (MpCanvas.fighter_anim[MpCanvas.attacker] == 16) or (MpCanvas.fighter_anim[MpCanvas.attacker] == 15):
            self.start_sound(2)
            return
        self.start_sound(0)

    def draw_stage_complete(self):  # g.java:4511
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 88, 72, 0)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 20), MpCanvas.stage_title, 0xFFFFFF)
        MpCanvas.stage_text = _js(_js(Consts.texts[26], " "), MpCanvas.stage)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 4), MpCanvas.stage_text, 0xFFFFFF)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y + 12), Consts.texts[28], 0xFFFFFF)

    def draw_damage(self):  # g.java:4519
        if MpCanvas.damage_tick < 0:
            return
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i] and ((MpCanvas.loop_i in (MpCanvas.attacker, MpCanvas.target)) or (MpCanvas.loop_i == MpCanvas.target2)):
                if MpCanvas.fighter_hp[MpCanvas.loop_i] != MpCanvas.fighter_hp_target[MpCanvas.loop_i]:
                    MpCanvas.fighter_hp[MpCanvas.loop_i] += MpCanvas.fighter_hp_step[MpCanvas.loop_i]
                    MpCanvas.fighter_hp[MpCanvas.loop_i] = max(MpCanvas.fighter_hp[MpCanvas.loop_i], 0)
                if MpCanvas.fighter_mp[MpCanvas.loop_i] != MpCanvas.fighter_mp_target[MpCanvas.loop_i]:
                    MpCanvas.fighter_mp[MpCanvas.loop_i] += MpCanvas.fighter_mp_step[MpCanvas.loop_i]
                    MpCanvas.fighter_mp[MpCanvas.loop_i] = max(MpCanvas.fighter_mp[MpCanvas.loop_i], 0)
                if MpCanvas.fighter_hp_delta[MpCanvas.loop_i] != 0:
                    MpCanvas.draw_mirrored = (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) != 0)
                    if not MpCanvas.draw_mirrored:
                        self.draw_damage_number(MpCanvas.screen_g, MpCanvas.fighter_x[MpCanvas.loop_i], ((MpCanvas.fighter_y[MpCanvas.loop_i] - 40) - (2 * MpCanvas.damage_tick)), MpCanvas.fighter_hp_delta[MpCanvas.loop_i])
                    else:
                        self.draw_damage_number(MpCanvas.screen_g, (MpCanvas.canvas_w - MpCanvas.fighter_x[MpCanvas.loop_i]), ((MpCanvas.fighter_y[MpCanvas.loop_i] - 40) - (2 * MpCanvas.damage_tick)), MpCanvas.fighter_hp_delta[MpCanvas.loop_i])
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.draw_hp_bars(MpCanvas.screen_g)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if (MpCanvas.fighter_present[MpCanvas.loop_i] and ((MpCanvas.loop_i in (MpCanvas.attacker, MpCanvas.target)) or (MpCanvas.loop_i == MpCanvas.target2))) and (MpCanvas.fighter_hp[MpCanvas.loop_i] == 0):
                MpCanvas.fighter_hp[MpCanvas.loop_i] = 1
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.damage_tick = MpCanvas.damage_tick + 1

    @staticmethod
    def draw_hp_bars(graphics):  # g.java:4562
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                gap = 0
                fill_w = idiv((MpCanvas.fighter_hp[MpCanvas.loop_i] * MpCanvas.hp_bar_w), MpCanvas.fighter_max_hp[MpCanvas.loop_i])
                if (fill_w == 0) and (MpCanvas.fighter_hp[MpCanvas.loop_i] > 0):
                    fill_w = 1
                bar_x = (28 if (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_w - 28) - MpCanvas.hp_bar_w))
                bar_y = (0 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_h - 3) - 6))
                fill_w = fill_w - 1
                if MpCanvas.fighter_hp[MpCanvas.loop_i] > 0:
                    if imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0:
                        Draw.draw_hline(graphics, bar_x, bar_y, fill_w, 0xB50000)
                        Draw.draw_hline(graphics, bar_x, (bar_y + 1), fill_w, 0xFF0000)
                        Draw.draw_hline(graphics, bar_x, (bar_y + 2), fill_w, 0xB50000)
                    else:
                        gap = (MpCanvas.hp_bar_w - fill_w)
                        Draw.draw_hline(graphics, (bar_x + gap), bar_y, fill_w, 0xB50000)
                        Draw.draw_hline(graphics, (bar_x + gap), (bar_y + 1), fill_w, 0xFF0000)
                        Draw.draw_hline(graphics, (bar_x + gap), (bar_y + 2), fill_w, 0xB50000)
                if (((fill_w := idiv((MpCanvas.fighter_mp[MpCanvas.loop_i] * MpCanvas.hp_bar_w), 100))) == 0) and (MpCanvas.fighter_mp[MpCanvas.loop_i] > 0):
                    fill_w = 1
                bar_x = (28 if (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_w - 28) - MpCanvas.hp_bar_w))
                bar_y = (6 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (MpCanvas.canvas_h - 3))
                fill_w = fill_w - 1
                if MpCanvas.fighter_mp[MpCanvas.loop_i] > 0:
                    if imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0:
                        Draw.draw_hline(graphics, bar_x, bar_y, fill_w, 3223675)
                        Draw.draw_hline(graphics, bar_x, (bar_y + 1), fill_w, 9216734)
                        Draw.draw_hline(graphics, bar_x, (bar_y + 2), fill_w, 3223675)
                    else:
                        gap = (MpCanvas.hp_bar_w - fill_w)
                        Draw.draw_hline(graphics, (bar_x + gap), bar_y, fill_w, 3223675)
                        Draw.draw_hline(graphics, (bar_x + gap), (bar_y + 1), fill_w, 9216734)
                        Draw.draw_hline(graphics, (bar_x + gap), (bar_y + 2), fill_w, 3223675)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    @staticmethod
    def clear_fighters():  # g.java:4609
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            MpCanvas.fighter_present[MpCanvas.loop_i] = False
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.allies_alive = 0
        MpCanvas.enemies_alive = 0

    @staticmethod
    def place_fighter(index):  # g.java:4726
        MpCanvas.fighter_x[index] = 42
        MpCanvas.fighter_y[index] = (MpCanvas.center_y + 65)
        if MpCanvas.room_mode != 0:
            MpCanvas.fighter_y[index] += ((((-1) if (idiv(MpCanvas.fighter_slot[index], 2) == 0) else 1)) * 23)

    def draw_skill_menu(self, graphics):  # g.java:5068
        self.draw_box(graphics, MpCanvas.center_x, (MpCanvas.center_y - 26), 110, 60, 0)
        Draw.fill_rect(graphics, (MpCanvas.center_x - 51), ((MpCanvas.center_y - 51) + (MpCanvas.skill_cursor * 12)), 102, 12, 12956683)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < MpCanvas.skill_slot_count:
            if MpCanvas.fighter_mp[0] < MpCanvas.skill_costs[(MpCanvas.skill_slots[MpCanvas.loop_i] - 3)]:
                self.draw_text_centred_on(graphics, MpCanvas.center_x, ((MpCanvas.center_y - 51) + (MpCanvas.loop_i * 12)), Consts.skill_names[(MpCanvas.skill_slots[MpCanvas.loop_i] - 3)], 0x646464)
                if (MpCanvas.skill_slots[MpCanvas.loop_i] != 9) and (MpCanvas.skill_slots[MpCanvas.loop_i] == 10):
                    pass
            else:
                self.draw_text_centred_on(graphics, MpCanvas.center_x, ((MpCanvas.center_y - 51) + (MpCanvas.loop_i * 12)), Consts.skill_names[(MpCanvas.skill_slots[MpCanvas.loop_i] - 3)], 0xFFFFFF)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_battle_result(self):  # g.java:5085
        if MpCanvas.room_mode in (0, 1):
            top = (MpCanvas.center_y - 62)
            self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 102, 124, 0)
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (top + 5), MpCanvas.fighter_name[0], 0xFFFFFF)
            verdict = (Consts.texts[5] if (MpCanvas.battle_won == 1) else Consts.texts[6])
            self.draw_text_colored(MpCanvas.screen_g, verdict, MpCanvas.center_x, (top + 19), 1, 16400640)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[49], (MpCanvas.center_x - 42), (top + 35), 0, 0xFFFFFF)
            self.draw_number0_on(MpCanvas.screen_g, (MpCanvas.center_x + 36), (top + 36), MpCanvas.wins)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[50], (MpCanvas.center_x - 42), (top + 50), 0, 0xFFFFFF)
            self.draw_number0_on(MpCanvas.screen_g, (MpCanvas.center_x + 36), (top + 51), MpCanvas.losses)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[29], (MpCanvas.center_x - 42), (top + 70), 0, 0xFFFFFF)
            self.draw_number1_on(MpCanvas.screen_g, (MpCanvas.center_x + 36), (top + 71), MpCanvas.reward_gold)
            self.draw_text_colored(MpCanvas.screen_g, Consts.rank_menu[0], (MpCanvas.center_x - 42), (top + 83), 0, 0xFFFFFF)
            self.draw_number1_on(MpCanvas.screen_g, (MpCanvas.center_x + 36), (top + 84), MpCanvas.reward_fame)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[4], (MpCanvas.center_x - 42), (top + 96), 0, 0x41FF41)
            self.draw_number0_on(MpCanvas.screen_g, (MpCanvas.center_x + 36), (top + 97), MpCanvas.reward_rank)
            self.draw_ok_button(top + 109)
        elif MpCanvas.room_mode == 2:
            top2 = (MpCanvas.center_y - 62)
            self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 102, 124, 0)
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (top2 + 3), MpCanvas.fighter_name[0], 0xFFFFFF)
            if MpCanvas.battle_won == 1:
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (top2 + 15), Consts.grades[MpCanvas.reward_grade], 16400640)
            else:
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (top2 + 15), Consts.texts[31], 16400640)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[29], (MpCanvas.center_x - 34), (top2 + 30), 0, 0xFFFFFF)
            self.draw_number1_on(MpCanvas.screen_g, (MpCanvas.center_x + 30), (top2 + 31), MpCanvas.reward_gold)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[32], (MpCanvas.center_x - 34), (top2 + 42), 0, 0xFFFFFF)
            self.draw_number1_on(MpCanvas.screen_g, (MpCanvas.center_x + 30), (top2 + 43), MpCanvas.reward_exp)
            self.draw_text_colored(MpCanvas.screen_g, Consts.rank_menu[0], (MpCanvas.center_x - 34), (top2 + 54), 0, 0xFFFFFF)
            self.draw_number1_on(MpCanvas.screen_g, (MpCanvas.center_x + 30), (top2 + 55), MpCanvas.reward_fame)
            if MpCanvas.loot != "NONE":
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (top2 + 69), MpCanvas.loot, 0xFFFFFF)
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (top2 + 81), _js(Consts.texts[33], "!!!"), 0xFFFFFF)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[4], (MpCanvas.center_x - 34), (top2 + 96), 0, 0x41FF41)
            self.draw_number1_on(MpCanvas.screen_g, (MpCanvas.center_x + 30), (top2 + 97), MpCanvas.reward_rank)
            self.draw_ok_button(top2 + 109)

    @staticmethod
    def tick_status_effects():  # g.java:5133
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                while True:
                    if MpCanvas.fighter_status[MpCanvas.loop_i] in (11, 12, 13):
                        MpCanvas.fighter_status_ticks[MpCanvas.loop_i] -= 1
                        if MpCanvas.fighter_status_ticks[MpCanvas.loop_i] > 0:
                            break
                        MpCanvas.fighter_status[MpCanvas.loop_i] = 99
                    break
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_action_cards(self):  # g.java:5152
        MpCanvas.box_x = 0
        if MpCanvas.state_ticks == 0:
            MpCanvas.box_x = (-40)
        elif MpCanvas.state_ticks == 1:
            MpCanvas.box_x = (-20)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if (MpCanvas.fighter_present[MpCanvas.loop_i] and (MpCanvas.fighter_hp[MpCanvas.loop_i] > 0)) and ((((MpCanvas.state == 99) or (MpCanvas.loop_i == MpCanvas.attacker)) or (MpCanvas.loop_i == MpCanvas.target)) or (MpCanvas.loop_i == MpCanvas.target2)):
                MpCanvas.box_y = (27 if (MpCanvas.room_mode == 0) else (27 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_h - 27) - 23)))
                if MpCanvas.fighter_kind[MpCanvas.loop_i] == 0:
                    MpCanvas.card_face = MpCanvas.fighter_face[MpCanvas.loop_i]
                    MpCanvas.card_half = True
                elif MpCanvas.fighter_kind[MpCanvas.loop_i] == 1:
                    MpCanvas.card_face = 4
                    MpCanvas.card_half = False
                elif MpCanvas.fighter_kind[MpCanvas.loop_i] == 2:
                    MpCanvas.card_face = 5
                    MpCanvas.card_half = False
                if MpCanvas.state == 99:
                    MpCanvas.tmp = MpCanvas.turn_actions[MpCanvas.loop_i]
                elif MpCanvas.loop_i == MpCanvas.attacker:
                    MpCanvas.tmp = MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)]
                elif MpCanvas.loop_i == MpCanvas.target:
                    MpCanvas.tmp = MpCanvas.turn_bytes[(16 + MpCanvas.turn_rec)]
                elif MpCanvas.loop_i == MpCanvas.target2:
                    MpCanvas.tmp = MpCanvas.turn_bytes[(36 + MpCanvas.turn_rec)]
                if imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0:
                    Draw.draw_rect(MpCanvas.screen_g, MpCanvas.box_x, MpCanvas.box_y, 60, 23, 0)
                    Draw.draw_rect(MpCanvas.screen_g, (MpCanvas.box_x + 1), (MpCanvas.box_y + 1), 58, 21, 16769990)
                    if MpCanvas.tmp in (0, 3, 4, 5, 6, 7, 8):
                        self.load_numbered_image(MpCanvas.act_images, "act", 0)
                        self.load_numbered_image(MpCanvas.act_images, "act", (6 + MpCanvas.card_face))
                        MpCanvas.draw_left_half((MpCanvas.box_x + Consts.act_dx[0]), (MpCanvas.box_y + Consts.act_dy[0]), MpCanvas.act_images[0])
                        MpCanvas.draw_left_half((MpCanvas.box_x + Consts.act_dx[(6 + MpCanvas.card_face)]), (MpCanvas.box_y + Consts.act_dy[(6 + MpCanvas.card_face)]), MpCanvas.act_images[(6 + MpCanvas.card_face)])
                    else:
                        self.load_numbered_image(MpCanvas.act_images, "act", 1)
                        self.load_numbered_image(MpCanvas.act_images, "act", (12 + MpCanvas.card_face))
                        MpCanvas.draw_left_half((MpCanvas.box_x + Consts.act_dx[1]), (MpCanvas.box_y + Consts.act_dy[1]), MpCanvas.act_images[1])
                        MpCanvas.draw_left_half((MpCanvas.box_x + Consts.act_dx[(12 + MpCanvas.card_face)]), (MpCanvas.box_y + Consts.act_dy[(12 + MpCanvas.card_face)]), MpCanvas.act_images[(12 + MpCanvas.card_face)])
                    MpCanvas.tmp = (3 if (MpCanvas.tmp > 2) else MpCanvas.tmp)
                    self.load_numbered_image(MpCanvas.act_images, "act", (2 + MpCanvas.tmp))
                    MpCanvas.draw_image((((MpCanvas.box_x + 60) - 19) + Consts.act_dx[(2 + MpCanvas.tmp)]), ((0 + MpCanvas.box_y) + Consts.act_dy[(2 + MpCanvas.tmp)]), MpCanvas.act_images[(2 + MpCanvas.tmp)])
                else:
                    MpCanvas.draw_rect(((MpCanvas.canvas_w - MpCanvas.box_x) - 60), MpCanvas.box_y, 60, 23, 0)
                    MpCanvas.draw_rect((((MpCanvas.canvas_w - MpCanvas.box_x) - 60) + 1), (MpCanvas.box_y + 1), 58, 21, 16769990)
                    if MpCanvas.tmp in (0, 3, 4, 5, 6, 7, 8):
                        self.load_numbered_image(MpCanvas.act_images, "act", (6 + MpCanvas.card_face))
                        MpCanvas.draw_right_half((MpCanvas.canvas_w - ((MpCanvas.box_x + Consts.act_dx[0]))), (MpCanvas.box_y + Consts.act_dy[0]), MpCanvas.act_images[0])
                        MpCanvas.draw_right_aligned((MpCanvas.canvas_w - ((MpCanvas.box_x + Consts.act_dx[(6 + MpCanvas.card_face)]))), (MpCanvas.box_y + Consts.act_dy[(6 + MpCanvas.card_face)]), MpCanvas.act_images[(6 + MpCanvas.card_face)], MpCanvas.card_half)
                    else:
                        self.load_numbered_image(MpCanvas.act_images, "act", (12 + MpCanvas.card_face))
                        MpCanvas.draw_right_half((MpCanvas.canvas_w - ((MpCanvas.box_x + Consts.act_dx[1]))), (MpCanvas.box_y + Consts.act_dy[1]), MpCanvas.act_images[1])
                        MpCanvas.draw_right_aligned((MpCanvas.canvas_w - ((MpCanvas.box_x + Consts.act_dx[(12 + MpCanvas.card_face)]))), (MpCanvas.box_y + Consts.act_dy[(12 + MpCanvas.card_face)]), MpCanvas.act_images[(12 + MpCanvas.card_face)], MpCanvas.card_half)
                    MpCanvas.tmp = (3 if (MpCanvas.tmp > 2) else MpCanvas.tmp)
                    self.load_numbered_image(MpCanvas.act_images, "act", (2 + MpCanvas.tmp))
                    MpCanvas.draw_image(((((MpCanvas.canvas_w - MpCanvas.box_x) - 60) + 10) + Consts.act_dx[(2 + MpCanvas.tmp)]), ((0 + MpCanvas.box_y) + Consts.act_dy[(2 + MpCanvas.tmp)]), MpCanvas.act_images[(2 + MpCanvas.tmp)])
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_round(self, graphics):  # g.java:5246
        if MpCanvas.round_no < 10:
            Draw.draw_image_part(graphics, MpCanvas.number_images[3], (MpCanvas.center_x - 33), (MpCanvas.center_y - 31), 52, 13, 120, 0)
            self.draw_number3_on(graphics, (MpCanvas.center_x + 21), (MpCanvas.center_y - 31), MpCanvas.round_no)
            return
        Draw.draw_image_part(graphics, MpCanvas.number_images[3], (MpCanvas.center_x - 39), (MpCanvas.center_y - 31), 52, 13, 120, 0)
        self.draw_number3_on(graphics, (MpCanvas.center_x + 27), (MpCanvas.center_y - 31), MpCanvas.round_no)

    @staticmethod
    def draw_action_pad(graphics):  # g.java:5256
        MpCanvas.box_x = MpCanvas.center_x
        MpCanvas.box_y = (MpCanvas.center_y - 40)
        if MpCanvas.room_mode == 0:
            MpCanvas.box_y = (MpCanvas.box_y - 6)
        Draw.draw_image(graphics, MpCanvas.ui_images[17], (MpCanvas.box_x - 12), MpCanvas.box_y, 0)
        Draw.draw_image(graphics, MpCanvas.ui_images[16], ((MpCanvas.box_x - 36) - 1), (MpCanvas.box_y + 16), 0)
        Draw.draw_image(graphics, MpCanvas.ui_images[15], ((MpCanvas.box_x + 12) + 1), (MpCanvas.box_y + 16), 0)
        MpCanvas.skill_ready = False
        if MpCanvas.skill_slot_count > 0:
            MpCanvas.loop_k = 0
            while MpCanvas.loop_k < MpCanvas.skill_slot_count:
                if MpCanvas.fighter_mp[0] >= MpCanvas.skill_costs[(MpCanvas.skill_slots[MpCanvas.loop_k] - 3)]:
                    MpCanvas.skill_ready = True
                MpCanvas.loop_k = MpCanvas.loop_k + 1
        Draw.draw_image(graphics, MpCanvas.ui_images[(18 + (0 if MpCanvas.skill_ready else 1))], (MpCanvas.box_x - 12), (MpCanvas.box_y + 30), 0)
        if MpCanvas.chosen_action != 99:
            pad_y = 0
            pad_x = 0
            if MpCanvas.chosen_action == 0:
                pad_x = ((MpCanvas.box_x + 12) + 1)
                pad_y = (MpCanvas.box_y + 16)
            elif MpCanvas.chosen_action == 1:
                pad_x = ((MpCanvas.box_x - 36) - 1)
                pad_y = (MpCanvas.box_y + 16)
            elif MpCanvas.chosen_action == 2:
                pad_x = (MpCanvas.box_x - 12)
                pad_y = MpCanvas.box_y
            else:
                pad_x = (MpCanvas.box_x - 12)
                pad_y = (MpCanvas.box_y + 30)
            Draw.draw_rect(graphics, (pad_x - 1), (pad_y - 1), 24, 24, 15721306)
            Draw.draw_rect(graphics, pad_x, pad_y, 23, 23, 15721306)

    def draw_battle_prompt(self, graphics, kind):  # g.java:5297
        dy = 0
        if MpCanvas.room_mode == 0:
            dy = 25
        if kind == 0:
            if MpCanvas.choose_secs > 5:
                self.draw_box(graphics, MpCanvas.center_x, ((MpCanvas.center_y + 28) + dy), 120, 27, 0)
                self.draw_text_centred(MpCanvas.center_x, ((MpCanvas.center_y + 17) + dy), Consts.texts[0], 0xFFFFFF)
                self.draw_text_centred(MpCanvas.center_x, ((MpCanvas.center_y + 28) + dy), Consts.texts[1], (0x646464 if MpCanvas.exit_asked else 0xFFFFFF))
                return
            self.draw_box(graphics, MpCanvas.center_x, ((MpCanvas.center_y + 28) + dy), 26, 26, 0)
            self.draw_number2_on(graphics, (MpCanvas.center_x - 4), ((MpCanvas.center_y + 22) + dy), MpCanvas.choose_secs)
        elif kind == 1:
            self.draw_box(graphics, MpCanvas.center_x, ((MpCanvas.center_y + 28) + dy), 120, 27, 0)
            self.draw_text_centred(MpCanvas.center_x, ((MpCanvas.center_y + 23) + dy), Consts.texts[17], 0xFFFFFF)
        elif kind == 2:
            dots = ""
            if imod(MpCanvas.state_ticks, 4) == 1:
                dots = "."
            elif imod(MpCanvas.state_ticks, 4) == 2:
                dots = ".."
            elif imod(MpCanvas.state_ticks, 4) == 3:
                dots = "..."
            self.draw_box(graphics, MpCanvas.center_x, ((MpCanvas.center_y + 28) + dy), 80, 24, 0)
            self.draw_text_left((MpCanvas.center_x - 30), ((MpCanvas.center_y + 23) + dy), _js(Consts.texts[7], dots), 0xFFFFFF)

    def load_status_effect(self):  # g.java:5477
        if MpCanvas.draw_mirrored:
            self.load_named_image(MpCanvas.effect_images[1], "spreff2_r", 1)
        else:
            self.load_named_image(MpCanvas.effect_images[1], "spreff2", 0)
        if MpCanvas.effect3_frames[0] is None:
            MpCanvas.effect3_frames[0] = SpriteFrames("/spreff3.SP2")

    @staticmethod
    def draw_status_effect(graphics, kind):  # g.java:5488
        frame = ((kind * 2) + imod(MpCanvas.state_ticks, 2))
        if MpCanvas.draw_mirrored:
            Draw.draw_image_part(graphics, MpCanvas.effect_images[1][1], (MpCanvas.canvas_w - ((MpCanvas.draw_x - MpCanvas.effect3_frames[0].anchor_x[frame]) + MpCanvas.effect3_frames[0].w[frame])), (MpCanvas.draw_y - MpCanvas.effect3_frames[0].anchor_y[frame]), MpCanvas.effect3_frames[0].w[frame], MpCanvas.effect3_frames[0].h[frame], MpCanvas.effect3_frames[0].src_x[frame], MpCanvas.effect3_frames[0].src_y[frame])
            return
        Draw.draw_image_part(graphics, MpCanvas.effect_images[1][0], (MpCanvas.draw_x - MpCanvas.effect3_frames[0].anchor_x[frame]), (MpCanvas.draw_y - MpCanvas.effect3_frames[0].anchor_y[frame]), MpCanvas.effect3_frames[0].w[frame], MpCanvas.effect3_frames[0].h[frame], MpCanvas.effect3_frames[0].src_x[frame], MpCanvas.effect3_frames[0].src_y[frame])

    def draw_hp_bar_frames(self):  # g.java:5609
        Draw.fill_rect(MpCanvas.buffer_g, 0, 0, MpCanvas.canvas_w, 12, 0)
        MpCanvas.draw_hp_bar_frame(0)
        x = 0
        Draw.draw_hline(MpCanvas.buffer_g, 28, 4, (MpCanvas.hp_bar_w - 1), 8429760)
        Draw.draw_hline(MpCanvas.buffer_g, 28, 10, (MpCanvas.hp_bar_w - 1), 8429760)
        Draw.draw_hline(MpCanvas.buffer_g, 31, 4, ((MpCanvas.hp_bar_w - 1) - 6), 0x808080)
        Draw.draw_hline(MpCanvas.buffer_g, 31, 10, ((MpCanvas.hp_bar_w - 1) - 6), 0x808080)
        x = (28 + MpCanvas.hp_bar_w)
        Draw.draw_vline(MpCanvas.buffer_g, x, 0, 10, 0x808080)
        Draw.draw_vline(MpCanvas.buffer_g, x, 3, 1, 8429760)
        Draw.draw_vline(MpCanvas.buffer_g, x, 4, 1, 0)
        Draw.draw_vline(MpCanvas.buffer_g, x, 5, 1, 8429760)
        Draw.draw_vline(MpCanvas.buffer_g, x, 9, 1, 8429760)
        MpCanvas.draw_hp_bar_frame(1)
        x = (((MpCanvas.canvas_w - 28) - MpCanvas.hp_bar_w) + 1)
        Draw.draw_hline(MpCanvas.buffer_g, x, 4, (MpCanvas.hp_bar_w - 1), 8429760)
        Draw.draw_hline(MpCanvas.buffer_g, x, 10, (MpCanvas.hp_bar_w - 1), 8429760)
        Draw.draw_hline(MpCanvas.buffer_g, (x + 3), 4, ((MpCanvas.hp_bar_w - 1) - 6), 0x808080)
        Draw.draw_hline(MpCanvas.buffer_g, (x + 3), 10, ((MpCanvas.hp_bar_w - 1) - 6), 0x808080)
        x = (((MpCanvas.canvas_w - 28) - 1) - MpCanvas.hp_bar_w)
        Draw.draw_vline(MpCanvas.buffer_g, x, 0, 10, 0x808080)
        Draw.draw_vline(MpCanvas.buffer_g, x, 3, 1, 8429760)
        Draw.draw_vline(MpCanvas.buffer_g, x, 4, 1, 0)
        Draw.draw_vline(MpCanvas.buffer_g, x, 5, 1, 8429760)
        Draw.draw_vline(MpCanvas.buffer_g, x, 9, 1, 8429760)
        if MpCanvas.room_mode != 0:
            Draw.fill_rect(MpCanvas.buffer_g, 0, (MpCanvas.canvas_h - 12), MpCanvas.canvas_w, 12, 0)
            MpCanvas.draw_hp_bar_frame(2)
            Draw.draw_hline(MpCanvas.buffer_g, 28, (MpCanvas.canvas_h - 5), (MpCanvas.hp_bar_w - 1), 8429760)
            Draw.draw_hline(MpCanvas.buffer_g, 28, (MpCanvas.canvas_h - 11), (MpCanvas.hp_bar_w - 1), 8429760)
            Draw.draw_hline(MpCanvas.buffer_g, 31, (MpCanvas.canvas_h - 5), (MpCanvas.hp_bar_w - 6), 0x808080)
            Draw.draw_hline(MpCanvas.buffer_g, 31, (MpCanvas.canvas_h - 11), (MpCanvas.hp_bar_w - 6), 0x808080)
            x = ((28 + MpCanvas.hp_bar_w) + 1)
            Draw.draw_vline(MpCanvas.buffer_g, (x - 1), (MpCanvas.canvas_h - 9), 9, 0x808080)
            Draw.draw_vline(MpCanvas.buffer_g, (x - 1), (MpCanvas.canvas_h - 4), 1, 8429760)
            Draw.draw_vline(MpCanvas.buffer_g, (x - 1), (MpCanvas.canvas_h - 5), 1, 0)
            Draw.draw_vline(MpCanvas.buffer_g, (x - 1), (MpCanvas.canvas_h - 6), 1, 8429760)
            Draw.draw_vline(MpCanvas.buffer_g, (x - 1), (MpCanvas.canvas_h - 10), 1, 8429760)
            MpCanvas.draw_hp_bar_frame(3)
            x = (((MpCanvas.canvas_w - 28) - MpCanvas.hp_bar_w) + 1)
            Draw.draw_hline(MpCanvas.buffer_g, x, (MpCanvas.canvas_h - 5), (MpCanvas.hp_bar_w - 1), 8429760)
            Draw.draw_hline(MpCanvas.buffer_g, x, (MpCanvas.canvas_h - 11), (MpCanvas.hp_bar_w - 1), 8429760)
            Draw.draw_hline(MpCanvas.buffer_g, (x + 3), (MpCanvas.canvas_h - 5), ((MpCanvas.hp_bar_w - 1) - 6), 0x808080)
            Draw.draw_hline(MpCanvas.buffer_g, (x + 3), (MpCanvas.canvas_h - 11), ((MpCanvas.hp_bar_w - 1) - 6), 0x808080)
            x = (((MpCanvas.canvas_w - 28) - 1) - MpCanvas.hp_bar_w)
            Draw.draw_vline(MpCanvas.buffer_g, x, (MpCanvas.canvas_h - 9), 10, 0x808080)
            Draw.draw_vline(MpCanvas.buffer_g, x, (MpCanvas.canvas_h - 4), 1, 8429760)
            Draw.draw_vline(MpCanvas.buffer_g, x, (MpCanvas.canvas_h - 5), 1, 0)
            Draw.draw_vline(MpCanvas.buffer_g, x, (MpCanvas.canvas_h - 6), 1, 8429760)
            Draw.draw_vline(MpCanvas.buffer_g, x, (MpCanvas.canvas_h - 10), 1, 8429760)

    @staticmethod
    def draw_hp_bar_frame(slot):  # g.java:5663
        x = (28 if (imod(slot, 2) == 0) else ((((MpCanvas.canvas_w - 28) - 1) - MpCanvas.hp_bar_w) + 2))
        y = (0 if (idiv(slot, 2) == 0) else ((MpCanvas.canvas_h - 3) - 6))
        i = 0
        while i < 2:
            if i == 1:
                y = (y + 6)
            Draw.draw_hline(MpCanvas.buffer_g, x, y, (MpCanvas.hp_bar_w - 1), 0x808080)
            Draw.draw_hline(MpCanvas.buffer_g, x, (y + 1), (MpCanvas.hp_bar_w - 1), 0xFFFFFF)
            Draw.draw_hline(MpCanvas.buffer_g, x, (y + 2), (MpCanvas.hp_bar_w - 1), 0xC0C0C0)
            i = i + 1

    def draw_battle_hud(self, graphics):  # g.java:5748
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                if imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0:
                    if MpCanvas.fighter_kind[MpCanvas.loop_i] == 0:
                        self.load_numbered_image(MpCanvas.face_images, "face", MpCanvas.fighter_face[MpCanvas.loop_i])
                        MpCanvas.draw_left_half_on(graphics, 0, (0 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (MpCanvas.canvas_h - 12)), MpCanvas.face_images[MpCanvas.fighter_face[MpCanvas.loop_i]])
                        MpCanvas.face_images[MpCanvas.fighter_face[MpCanvas.loop_i]] = None
                    self.draw_box(graphics, 0, (12 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_h - 12) - 15)), 60, 15, 1)
                    if (len(MpCanvas.fighter_alt_name[MpCanvas.loop_i]) == 0) or (imod(MpCanvas.round_no, 2) == 0):
                        self.draw_text_centred_on(graphics, 30, (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), MpCanvas.fighter_name[MpCanvas.loop_i], 0xFFFFFF)
                    else:
                        self.draw_text_centred_on(graphics, 30, (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), MpCanvas.fighter_alt_name[MpCanvas.loop_i], 0xFFFFFF)
                else:
                    if MpCanvas.fighter_kind[MpCanvas.loop_i] == 0:
                        self.load_numbered_image(MpCanvas.face_images, "face", MpCanvas.fighter_face[MpCanvas.loop_i])
                        MpCanvas.draw_right_half_on(graphics, MpCanvas.canvas_w, (0 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (MpCanvas.canvas_h - 12)), MpCanvas.face_images[MpCanvas.fighter_face[MpCanvas.loop_i]])
                        MpCanvas.face_images[MpCanvas.fighter_face[MpCanvas.loop_i]] = None
                    self.draw_box(graphics, (MpCanvas.canvas_w - 60), (12 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_h - 12) - 15)), 60, 15, 1)
                    if (len(MpCanvas.fighter_alt_name[MpCanvas.loop_i]) == 0) or (imod(MpCanvas.round_no, 2) == 0):
                        self.draw_text_centred_on(graphics, (MpCanvas.canvas_w - 30), (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), MpCanvas.fighter_name[MpCanvas.loop_i], 0xFFFFFF)
                    else:
                        self.draw_text_centred_on(graphics, (MpCanvas.canvas_w - 30), (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), MpCanvas.fighter_alt_name[MpCanvas.loop_i], 0xFFFFFF)
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.noop()
