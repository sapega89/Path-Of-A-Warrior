"""g.java, part of MpCanvas: the non-battle screens: backgrounds, windows, records, attributes, skills, help, error, loading.

A mixin of MpCanvas (pow_mp/mp_canvas.py); the methods keep their `# g.java:FROM-TO`
comments. The module names below are set by mp_canvas.py: `MpCanvas` once the class exists,
the others by its _late_imports().
"""
from pow_mp.rt import (
    _js,
    idiv,
    imod,
)

MpCanvas = None   # set by pow_mp/mp_canvas.py
Consts = Draw = None   # set by mp_canvas._late_imports


class ScreensMixin:
    def draw_help(self):  # g.java:5351
        top = (MpCanvas.center_y - 57)
        self.draw_window(MpCanvas.screen_g)
        MpCanvas.fill_rect(((MpCanvas.center_x - 52) - 7), (top - 2), 118, 123, 0)
        MpCanvas.draw_rect(((MpCanvas.center_x - 52) - 7), (top - 2), 118, 123, 0x949694)
        MpCanvas.fill_rect(((MpCanvas.center_x - 52) - 6), (top - 1), 116, 13, 0x313431)
        MpCanvas.help_first_line = 0
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < MpCanvas.help_page:
            if MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 0:
                MpCanvas.help_first_line = (MpCanvas.help_first_line + Consts.help_controls_lines[MpCanvas.loop_i])
            elif MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 1:
                MpCanvas.help_first_line = (MpCanvas.help_first_line + Consts.help_menu_lines[MpCanvas.loop_i])
            elif MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 2:
                MpCanvas.help_first_line = (MpCanvas.help_first_line + Consts.help_duel_lines[MpCanvas.loop_i])
            elif MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 3:
                MpCanvas.help_first_line = (MpCanvas.help_first_line + Consts.help_mission_lines[MpCanvas.loop_i])
            elif MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 4:
                MpCanvas.help_first_line = (MpCanvas.help_first_line + Consts.help_about_lines[MpCanvas.loop_i])
            elif MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 5:
                MpCanvas.help_first_line = (MpCanvas.help_first_line + Consts.help_network_lines[MpCanvas.loop_i])
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        if MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 0:
            self.draw_text_centred(MpCanvas.center_x, top, Consts.help_controls[MpCanvas.help_first_line], 0xFFFFFF)
            MpCanvas.tmp = Consts.help_controls_lines[MpCanvas.help_page]
        elif MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 1:
            self.draw_text_centred(MpCanvas.center_x, top, Consts.help_menu[MpCanvas.help_first_line], 0xFFFFFF)
            MpCanvas.tmp = Consts.help_menu_lines[MpCanvas.help_page]
        elif MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 2:
            self.draw_text_centred(MpCanvas.center_x, top, Consts.help_duel[MpCanvas.help_first_line], 0xFFFFFF)
            MpCanvas.tmp = Consts.help_duel_lines[MpCanvas.help_page]
        elif MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 3:
            self.draw_text_centred(MpCanvas.center_x, top, Consts.help_mission[MpCanvas.help_first_line], 0xFFFFFF)
            MpCanvas.tmp = Consts.help_mission_lines[MpCanvas.help_page]
        elif MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 4:
            self.draw_text_centred(MpCanvas.center_x, top, Consts.help_about[MpCanvas.help_first_line], 0xFFFFFF)
            MpCanvas.tmp = Consts.help_about_lines[MpCanvas.help_page]
        elif MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 5:
            self.draw_text_centred(MpCanvas.center_x, top, Consts.help_network[MpCanvas.help_first_line], 0xFFFFFF)
            MpCanvas.tmp = Consts.help_network_lines[MpCanvas.help_page]
        MpCanvas.loop_i = 1
        while MpCanvas.loop_i < MpCanvas.tmp:
            while True:
                if MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 0:
                    self.draw_text_left((MpCanvas.center_x - 56), ((top + (MpCanvas.loop_i * 12)) + 1), Consts.help_controls[(MpCanvas.help_first_line + MpCanvas.loop_i)], 0xFFFFFF)
                elif MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 1:
                    self.draw_text_left((MpCanvas.center_x - 56), ((top + (MpCanvas.loop_i * 12)) + 1), Consts.help_menu[(MpCanvas.help_first_line + MpCanvas.loop_i)], 0xFFFFFF)
                elif MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 2:
                    self.draw_text_left((MpCanvas.center_x - 56), ((top + (MpCanvas.loop_i * 12)) + 1), Consts.help_duel[(MpCanvas.help_first_line + MpCanvas.loop_i)], 0xFFFFFF)
                elif MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 3:
                    self.draw_text_left((MpCanvas.center_x - 56), ((top + (MpCanvas.loop_i * 12)) + 1), Consts.help_mission[(MpCanvas.help_first_line + MpCanvas.loop_i)], 0xFFFFFF)
                elif MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 4:
                    self.draw_text_centred(MpCanvas.center_x, ((top + (MpCanvas.loop_i * 17)) + 9), Consts.help_about[(MpCanvas.help_first_line + MpCanvas.loop_i)], 0xFFFFFF)
                    if MpCanvas.loop_i != 3:
                        break
                    self.draw_text_centred(MpCanvas.center_x, ((top + (MpCanvas.loop_i * 17)) + 9), _js("v", MpCanvas.app_version), 0xFFFFFF)
                elif MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)] == 5:
                    self.draw_text_left((MpCanvas.center_x - 56), ((top + (MpCanvas.loop_i * 12)) + 1), Consts.help_network[(MpCanvas.help_first_line + MpCanvas.loop_i)], 0xFFFFFF)
                break
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        if Consts.help_pages[MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]] > 1:
            self.draw_text_centred(MpCanvas.center_x, ((top + 72) + 38), _js(_js((MpCanvas.help_page + 1), "/"), Consts.help_pages[MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]]), 0xFFFFFF)
            MpCanvas.draw_left_half((MpCanvas.center_x - 35), ((top + 72) + 39), MpCanvas.arrow_images[1])
            MpCanvas.draw_right_half((MpCanvas.center_x + 35), ((top + 72) + 39), MpCanvas.arrow_images[1])

    def draw_menu_icons(self):  # g.java:5456
        self.draw_window_bg(MpCanvas.buffer_g)
        step = idiv(80, MpCanvas.menu_size)
        if step > 30:
            step = 30
        elif step < 19:
            step = 19
        dy = 0
        if (MpCanvas.state in {162, 163}) or (MpCanvas.state == 164):
            dy = 15
        elif MpCanvas.state == 10:
            dy = 40
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < MpCanvas.menu_size:
            Draw.draw_image_part(MpCanvas.buffer_g, MpCanvas.menu_icon_image, (idiv((((MpCanvas.canvas_w - (step * ((MpCanvas.menu_size - 1)))) - 11)), 2) + (step * MpCanvas.loop_i)), ((MpCanvas.center_y + 6) + dy), 12, 15, 12, 0)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_background(self):  # g.java:5534
        i = 0
        horizon = 0
        Draw.fill_rect(MpCanvas.buffer_g, 0, 0, MpCanvas.canvas_w, MpCanvas.canvas_h, 0)
        horizon = (idiv(MpCanvas.screen_h, 2) - 95)
        tiles = (idiv(MpCanvas.screen_w, 30) + 1)
        sky = ((MpCanvas.room_bg >> 6) & 3)
        if sky == 0:
            self.load_bg(4)
            self.load_bg(5)
            self.load_bg(6)
            self.load_bg(7)
            self.load_bg(8)
            Draw.fill_rect(MpCanvas.buffer_g, 0, 0, MpCanvas.canvas_w, (horizon + 1), 11257599)
            i = 0
            while i < tiles:
                MpCanvas.draw_image_on(MpCanvas.buffer_g, (30 * i), horizon, MpCanvas.bg_images[4])
                MpCanvas.draw_image_on(MpCanvas.buffer_g, (30 * i), (horizon + 30), MpCanvas.bg_images[5])
                i = i + 1
            MpCanvas.draw_image_on(MpCanvas.buffer_g, (MpCanvas.screen_w - MpCanvas.bg_images[6].getWidth()), ((horizon - 2) - MpCanvas.bg_images[6].getHeight()), MpCanvas.bg_images[6])
            MpCanvas.draw_image_on(MpCanvas.buffer_g, 18, (horizon - 30), MpCanvas.bg_images[7])
            MpCanvas.draw_image_on(MpCanvas.buffer_g, 52, (horizon - 15), MpCanvas.bg_images[8])
        elif sky == 1:
            self.load_bg(9)
            self.load_bg(10)
            self.load_bg(11)
            self.load_bg(12)
            self.load_bg(13)
            Draw.fill_rect(MpCanvas.buffer_g, 0, 0, MpCanvas.canvas_w, (horizon + 1), 1645890)
            i = 0
            while i < tiles:
                MpCanvas.draw_image_on(MpCanvas.buffer_g, (30 * i), horizon, MpCanvas.bg_images[9])
                MpCanvas.draw_image_on(MpCanvas.buffer_g, (30 * i), (horizon + 30), MpCanvas.bg_images[10])
                i = i + 1
            MpCanvas.draw_image_on(MpCanvas.buffer_g, (MpCanvas.screen_w - MpCanvas.bg_images[6].getWidth()), ((horizon - 2) - MpCanvas.bg_images[6].getHeight()), MpCanvas.bg_images[11])
            MpCanvas.draw_image_on(MpCanvas.buffer_g, 18, (horizon - 30), MpCanvas.bg_images[12])
            MpCanvas.draw_image_on(MpCanvas.buffer_g, 52, (horizon - 15), MpCanvas.bg_images[13])
        ground = ((MpCanvas.room_bg >> 4) & 3)
        self.load_bg(14 + ground)
        i = 0
        while i < tiles:
            MpCanvas.draw_image_on(MpCanvas.buffer_g, (30 * i), (horizon + 83), MpCanvas.bg_images[(14 + ground)])
            i = i + 1
        front = (MpCanvas.room_bg & 3)
        front_y = 0
        front_dy = [3, 8, (-8), 16]
        self.load_bg(0 + front)
        front_y = (horizon + front_dy[front])
        MpCanvas.draw_image_on(MpCanvas.buffer_g, 0, front_y, MpCanvas.bg_images[(0 + front)])
        i = 0
        while i < len(MpCanvas.bg_images):
            MpCanvas.bg_images[i] = None
            i = i + 1
        MpCanvas.noop()

    def draw_window(self, graphics):  # g.java:5678
        self.draw_window_bg(graphics)

    def draw_window_bg(self, graphics):  # g.java:5682
        edge = 0
        rest = 0
        part = 0
        MpCanvas.draw_back_tiles(graphics)
        if MpCanvas.canvas_h <= 144:
            part = (78 - idiv(((144 - MpCanvas.canvas_h)), 2))
            rest = ((MpCanvas.canvas_h - 18) - part)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, 0, 5, 5, 8, 0, 0)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, 0, 13, 5, part, 0, (8 + (78 - part)))
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, 0, (13 + part), 5, rest, 0, (134 - rest))
            edge = (MpCanvas.canvas_w - 5)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, edge, 5, 5, 8, 5, 0)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, edge, 13, 5, part, 5, (8 + (78 - part)))
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, edge, (13 + part), 5, rest, 5, (134 - rest))
        else:
            part = idiv(((MpCanvas.canvas_h - 144)), 2)
            rest = ((MpCanvas.canvas_h - 144) - part)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, 0, 5, 5, 59, 0, 0)
            MpCanvas.draw_border_v(graphics, 0, 64, part, 0)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, 0, (64 + part), 5, 17, 0, 59)
            MpCanvas.draw_border_v(graphics, 0, ((64 + part) + 17), rest, 0)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, 0, ((MpCanvas.canvas_h - 5) - 58), 5, 58, 0, 76)
            edge = (MpCanvas.canvas_w - 5)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, edge, 5, 5, 59, 5, 0)
            MpCanvas.draw_border_v(graphics, edge, 64, part, 5)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, edge, (64 + part), 5, 17, 5, 59)
            MpCanvas.draw_border_v(graphics, edge, ((64 + part) + 17), part, 5)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, edge, ((MpCanvas.canvas_h - 5) - 58), 5, 58, 5, 76)
        part = idiv(((MpCanvas.canvas_w - 120)), 2)
        rest = ((MpCanvas.canvas_w - 120) - part)
        Draw.draw_image_part(graphics, MpCanvas.border_h_image, 0, 0, 21, 5, 0, 0)
        MpCanvas.draw_border_h(graphics, 21, 0, part, 0)
        Draw.draw_image_part(graphics, MpCanvas.border_h_image, (21 + part), 0, 77, 5, 21, 0)
        MpCanvas.draw_border_h(graphics, (98 + part), 0, rest, 0)
        Draw.draw_image_part(graphics, MpCanvas.border_h_image, (MpCanvas.canvas_w - 21), 0, 21, 5, 98, 0)
        edge = (MpCanvas.canvas_h - 5)
        Draw.draw_image_part(graphics, MpCanvas.border_h_image, 0, edge, 37, 5, 0, 5)
        MpCanvas.draw_border_h(graphics, 37, edge, part, 5)
        Draw.draw_image_part(graphics, MpCanvas.border_h_image, (37 + part), edge, 45, 5, 37, 5)
        MpCanvas.draw_border_h(graphics, (82 + part), edge, rest, 5)
        Draw.draw_image_part(graphics, MpCanvas.border_h_image, (MpCanvas.canvas_w - 37), edge, 37, 5, 82, 5)
        Draw.draw_image_part(graphics, MpCanvas.titlebox_image, (MpCanvas.center_x - 46), 0, 46, 15, 0, 0)
        Draw.draw_image_part(graphics, MpCanvas.titlebox_image, MpCanvas.center_x, 0, 46, 15, 17, 0)
        self.draw_text_colored(graphics, MpCanvas.title, idiv(MpCanvas.canvas_w, 2), 2, 1, 0xFFFFFF)

    def draw_options_bg(self, graphics):  # g.java:5820
        self.draw_window(graphics)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 3:
            self.draw_box(graphics, (MpCanvas.center_x - 58), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 19)), 61, 14, 2)
            self.draw_text_colored(graphics, Consts.option_texts[MpCanvas.loop_i], (MpCanvas.center_x - 28), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0x646464)
            self.draw_box(graphics, (MpCanvas.center_x + 13), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 19)), 39, 14, 2)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_records(self):  # g.java:5831
        self.draw_window(MpCanvas.screen_g)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 6:
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 60), ((MpCanvas.center_y - 47) + (MpCanvas.loop_i * 17)), 81, 14, 2)
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x + 23), ((MpCanvas.center_y - 47) + (MpCanvas.loop_i * 17)), 37, 14, 2)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[(46 + MpCanvas.loop_i)], (MpCanvas.center_x - 19), ((MpCanvas.center_y - 45) + (MpCanvas.loop_i * 17)), 1, 0xFFFFFF)
            if MpCanvas.loop_i == 0:
                self.draw_number1((MpCanvas.center_x + 52), ((MpCanvas.center_y - 44) + (MpCanvas.loop_i * 17)), MpCanvas.level)
            elif MpCanvas.loop_i == 1:
                self.draw_number1_b((MpCanvas.center_x + 52), ((MpCanvas.center_y - 44) + (MpCanvas.loop_i * 17)), MpCanvas.fame)
            elif MpCanvas.loop_i == 2:
                MpCanvas.stat_value = MpCanvas.duel_grade
            elif MpCanvas.loop_i == 3:
                MpCanvas.stat_value = MpCanvas.wins
            elif MpCanvas.loop_i == 4:
                MpCanvas.stat_value = MpCanvas.losses
            elif MpCanvas.loop_i == 5:
                MpCanvas.stat_value = MpCanvas.mission_grade
            if MpCanvas.loop_i > 1:
                self.draw_number0_b((MpCanvas.center_x + 52), ((MpCanvas.center_y - 44) + (MpCanvas.loop_i * 17)), MpCanvas.stat_value)
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        self.draw_records_order()          # PORT-EXTRA: the order row (pow_mp/mp_canvas_order.py)

    def draw_attributes(self):  # g.java:5870
        self.draw_window(MpCanvas.screen_g)
        bonus = 0
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 54), ((MpCanvas.center_y - 30) + (MpCanvas.loop_i * 17)), 39, 14, 2)
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 13), ((MpCanvas.center_y - 30) + (MpCanvas.loop_i * 17)), 67, 14, 2)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[(42 + MpCanvas.loop_i)], (MpCanvas.center_x - 35), ((MpCanvas.center_y - 28) + (MpCanvas.loop_i * 17)), 1, 0xFFFFFF)
            if MpCanvas.loop_i == 0:
                MpCanvas.stat_value = MpCanvas.attr_hp
                bonus = MpCanvas.attr_hp_bonus
            elif MpCanvas.loop_i == 1:
                MpCanvas.stat_value = MpCanvas.attr_mp
                bonus = MpCanvas.attr_mp_bonus
            elif MpCanvas.loop_i == 2:
                MpCanvas.stat_value = MpCanvas.attr_attack
                bonus = MpCanvas.attr_attack_bonus
            elif MpCanvas.loop_i == 3:
                MpCanvas.stat_value = MpCanvas.attr_defense
                bonus = MpCanvas.attr_defense_bonus
            self.draw_number0((MpCanvas.center_x + 9), ((MpCanvas.center_y - 27) + (MpCanvas.loop_i * 17)), MpCanvas.stat_value)
            self.draw_number5((MpCanvas.center_x + 52), ((MpCanvas.center_y - 27) + (MpCanvas.loop_i * 17)), bonus)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_skills_bg(self, graphics):  # g.java:5905
        self.draw_window(graphics)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 5:
            self.draw_box(graphics, (MpCanvas.center_x - 58), ((MpCanvas.center_y - 51) + (MpCanvas.loop_i * 16)), 91, 14, 2)
            self.draw_box(graphics, (MpCanvas.center_x + 43), ((MpCanvas.center_y - 51) + (MpCanvas.loop_i * 16)), 15, 14, 2)
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        self.draw_text_centred_on(graphics, (MpCanvas.center_x - 13), (MpCanvas.center_y - 49), "NAME", 0xFFFFFF)
        self.draw_text_centred_on(graphics, (MpCanvas.center_x + 51), (MpCanvas.center_y - 49), "LV", 0xFFFFFF)
        MpCanvas.fill_rect_on(graphics, (MpCanvas.center_x - 52), (MpCanvas.center_y + 31), 104, 27, 0)
        MpCanvas.draw_line_color(graphics, (MpCanvas.center_x - 52), (MpCanvas.center_y + 30), (MpCanvas.center_x + 51), (MpCanvas.center_y + 30), 0x804000)
        MpCanvas.draw_line_color(graphics, (MpCanvas.center_x - 52), (MpCanvas.center_y + 58), (MpCanvas.center_x + 51), (MpCanvas.center_y + 58), 0x804000)
        MpCanvas.draw_line_color(graphics, (MpCanvas.center_x - 53), (MpCanvas.center_y + 31), (MpCanvas.center_x - 53), (MpCanvas.center_y + 57), 0x804000)
        MpCanvas.draw_line_color(graphics, (MpCanvas.center_x + 52), (MpCanvas.center_y + 31), (MpCanvas.center_x + 52), (MpCanvas.center_y + 57), 0x804000)

    def draw_skill_slots(self):  # g.java:5922
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                if imod(MpCanvas.state_ticks, 4) < 2:
                    MpCanvas.draw_left_half((MpCanvas.center_x - 65), ((MpCanvas.center_y - 32) + (MpCanvas.loop_i * 16)), MpCanvas.arrow_images[1])
                    MpCanvas.draw_right_half((MpCanvas.center_x + 40), ((MpCanvas.center_y - 32) + (MpCanvas.loop_i * 16)), MpCanvas.arrow_images[1])
                self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 58), ((MpCanvas.center_y - 35) + (MpCanvas.loop_i * 16)), 91, 14, 3)
                self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x + 43), ((MpCanvas.center_y - 35) + (MpCanvas.loop_i * 16)), 15, 14, 3)
            if MpCanvas.skill_levels[(MpCanvas.skill_order[MpCanvas.loop_i] - 3)] == 99:
                self.draw_text_centred_on(MpCanvas.screen_g, (MpCanvas.center_x - 12), ((MpCanvas.center_y - 33) + (MpCanvas.loop_i * 16)), Consts.skill_names[(MpCanvas.skill_order[MpCanvas.loop_i] - 3)], 0x646464)
                if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                    self.draw_text_left((MpCanvas.center_x - 50), (MpCanvas.center_y + 32), Consts.texts[34], 0x646464)
            else:
                self.draw_text_centred_on(MpCanvas.screen_g, (MpCanvas.center_x - 12), ((MpCanvas.center_y - 33) + (MpCanvas.loop_i * 16)), Consts.skill_names[(MpCanvas.skill_order[MpCanvas.loop_i] - 3)], 0xFFFFFF)
                self.draw_number1((MpCanvas.center_x + 48), ((MpCanvas.center_y - 32) + (MpCanvas.loop_i * 16)), MpCanvas.skill_levels[(MpCanvas.skill_order[MpCanvas.loop_i] - 3)])
                if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                    self.draw_text_left((MpCanvas.center_x - 50), (MpCanvas.center_y + 32), Consts.skill_info[(((MpCanvas.skill_order[MpCanvas.loop_i] - 3)) * 2)], 0xFFFFFF)
                    self.draw_text_left((MpCanvas.center_x - 50), (MpCanvas.center_y + 45), Consts.skill_info[((((MpCanvas.skill_order[MpCanvas.loop_i] - 3)) * 2) + 1)], 0xFFFFFF)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_exp_fame_gold(self):  # g.java:5950
        self.draw_window(MpCanvas.screen_g)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 3:
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 50), ((MpCanvas.center_y - 45) + (MpCanvas.loop_i * 34)), 100, 14, 2)
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 50), ((MpCanvas.center_y - 32) + (MpCanvas.loop_i * 34)), 100, 14, 2)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[(52 + MpCanvas.loop_i)], MpCanvas.center_x, ((MpCanvas.center_y - 43) + (MpCanvas.loop_i * 34)), 1, 0xFFFFFF)
            if MpCanvas.loop_i == 0:
                MpCanvas.stat_value = MpCanvas.exp
            elif MpCanvas.loop_i == 1:
                MpCanvas.stat_value = MpCanvas.fame
            elif MpCanvas.loop_i == 2:
                MpCanvas.stat_value = MpCanvas.gold
            self.draw_number0_b((MpCanvas.center_x + 24), ((MpCanvas.center_y - 29) + (MpCanvas.loop_i * 34)), MpCanvas.stat_value)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_quote_bg(self, graphics):  # g.java:5975
        self.draw_window(graphics)
        self.draw_box(graphics, (MpCanvas.center_x - 62), (MpCanvas.center_y + 7), 126, 16, 6)

    def draw_quote_prompt(self, graphics):  # g.java:5980
        text = MpCanvas.input_text
        self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 44), _js(_js(Consts.texts[58], "."), (MpCanvas.quote_step + 1)), 16400640)
        if MpCanvas.quote_step == 0:
            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 32), Consts.texts[23], 0xFFFFFF)
            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 20), Consts.texts[24], 0xFFFFFF)
        else:
            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 32), Consts.texts[15], 0xFFFFFF)
            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 20), Consts.texts[16], 0xFFFFFF)
        self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 8), Consts.texts[25], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y + 9), text, 0x41FF41)
        if imod(MpCanvas.state_ticks, 4) < 2:
            text_w = MpCanvas.font_white.string_width(text)
            if len(text) == 20:
                text_w = (text_w - (MpCanvas.font_white.string_width("A") * 2))
            MpCanvas.draw_line_color(graphics, (MpCanvas.center_x + idiv(text_w, 2)), (MpCanvas.center_y + 20), ((MpCanvas.center_x + idiv(text_w, 2)) + 4), (MpCanvas.center_y + 20), 0xFFFFFF)
        MpCanvas.draw_letter_grid_space(MpCanvas.letter_cursor, (MpCanvas.center_y + 27))

    def draw_exit_confirm(self, graphics):  # g.java:6131
        self.draw_box(graphics, (MpCanvas.center_x - 53), (MpCanvas.center_y - 34), 106, 68, 5)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 22), Consts.texts[56], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 7), Consts.texts[57], 0xFFFFFF)
        i = 0
        while i < 2:
            self.draw_box(graphics, ((MpCanvas.center_x - 42) + (i * 55)), (MpCanvas.center_y + 15), 29, 14, (3 if (MpCanvas.popup_cursor == i) else 2))
            self.draw_text_colored(graphics, Consts.texts[(40 + i)], ((MpCanvas.center_x - 27) + (i * 55)), (MpCanvas.center_y + 17), 1, (0xFFFFFF if (MpCanvas.popup_cursor == i) else 0x646464))
            i = i + 1

    def draw_error(self):  # g.java:6143
        MpCanvas.msg_first_line = 0
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < MpCanvas.error_msg:
            MpCanvas.msg_first_line = (MpCanvas.msg_first_line + Consts.error_line_counts[MpCanvas.loop_i])
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.tmp = 0
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < Consts.error_line_counts[MpCanvas.error_msg]:
            MpCanvas.msg_copy_line = True
            if MpCanvas.msg_copy_line:
                MpCanvas.text_lines[MpCanvas.loop_i] = Consts.error_lines[(MpCanvas.msg_first_line + MpCanvas.loop_i)]
            MpCanvas.tmp = max(MpCanvas.tmp, len(MpCanvas.text_lines[MpCanvas.loop_i]))
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.loop_j = 0
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, (MpCanvas.tmp * 7), (((((Consts.error_line_counts[MpCanvas.error_msg] + 1)) * 15) + MpCanvas.loop_j) + 4), 0)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < Consts.error_line_counts[MpCanvas.error_msg]:
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((((MpCanvas.center_y - idiv((Consts.error_line_counts[MpCanvas.error_msg] * 15), 2)) + (MpCanvas.loop_i * 15)) - 4) - idiv(MpCanvas.loop_j, 3)), MpCanvas.text_lines[MpCanvas.loop_i], 0xFFFFFF)
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        self.draw_ok_button((MpCanvas.center_y + idiv((Consts.error_line_counts[MpCanvas.error_msg] * 15), 2)) - 5)

    def draw_challenge_bg(self, graphics):  # g.java:6172
        self.draw_window(graphics)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 2:
            self.draw_box(graphics, (MpCanvas.center_x - 56), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 20)), 111, 14, 2)
            self.draw_text_colored(graphics, Consts.texts[(38 + MpCanvas.loop_i)], idiv(MpCanvas.screen_w, 2), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 20)), 1, 0x646464)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_loading(self):  # g.java:6192
        dots = ""
        if imod(MpCanvas.state_ticks, 4) == 1:
            dots = "."
        elif imod(MpCanvas.state_ticks, 4) == 2:
            dots = ".."
        elif imod(MpCanvas.state_ticks, 4) == 3:
            dots = "..."
        text_w = (MpCanvas.font_white.string_width(Consts.loading_texts[MpCanvas.loading_msg]) + 14)
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, (text_w + 22), 30, 0)
        self.draw_text_left_on(MpCanvas.screen_g, (MpCanvas.center_x - idiv(text_w, 2)), ((MpCanvas.center_y - 7) + 2), _js(Consts.loading_texts[MpCanvas.loading_msg], dots), 0xFFFFFF)

    def draw_waiting(self):  # g.java:6206
        dots = ""
        if imod(MpCanvas.state_ticks, 4) == 1:
            dots = "."
        elif imod(MpCanvas.state_ticks, 4) == 2:
            dots = ".."
        elif imod(MpCanvas.state_ticks, 4) == 3:
            dots = "..."
        text_w = (MpCanvas.font_white.string_width(Consts.texts[7]) + 14)
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, (text_w + 22), 30, 0)
        self.draw_text_left_on(MpCanvas.screen_g, (MpCanvas.center_x - idiv(text_w, 2)), (MpCanvas.center_y - 6), _js(Consts.texts[7], dots), 0xFFFFFF)
