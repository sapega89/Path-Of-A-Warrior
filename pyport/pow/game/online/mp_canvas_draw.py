"""g.java, part of MpCanvas: drawing primitives: text, rectangles, lines, images and halves, numbers, boxes, buttons, borders.

A mixin of MpCanvas (pow/game/online/mp_canvas.py); the methods keep their `# g.java:FROM-TO`
comments. The module names below are set by mp_canvas.py: `MpCanvas` once the class exists,
the others by its _late_imports().
"""
from pow.game.online.rt import (
    _js,
    i32,
    idiv,
    imod,
)

MpCanvas = None   # set by pow/game/online/mp_canvas.py
Consts = Draw = Gfx = None   # set by mp_canvas._late_imports


class DrawMixin:
    @staticmethod
    def draw_menu_cursor(graphics):  # g.java:348
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
        Draw.draw_image_part(graphics, MpCanvas.menu_icon_image, (idiv((((MpCanvas.canvas_w - (step * ((MpCanvas.menu_size - 1)))) - 11)), 2) + (step * MpCanvas.cursor_stack[MpCanvas.stack_depth])), ((MpCanvas.center_y + 6) + dy), 12, 15, 0, 0)

    def draw_text_centred_on(self, graphics, x, y, text, color):  # g.java:1471
        self.draw_text_colored(graphics, text, x, y, 1, color)

    def draw_text_centred(self, x, y, text, color):  # g.java:1475
        self.draw_text_colored(MpCanvas.screen_g, text, x, y, 1, color)

    def draw_text_left_on(self, graphics, x, y, text, color):  # g.java:1479
        self.draw_text_colored(graphics, text, x, y, 0, color)

    def draw_text_left(self, x, y, text, color):  # g.java:1483
        self.draw_text_colored(MpCanvas.screen_g, text, x, y, 0, color)

    def draw_text_colored(self, graphics, text, x, y, anchor, color):  # g.java:1487
        if color == 0xFFFFFF:
            Gfx.set_font(MpCanvas.font_white)
        elif color == 16400640:
            Gfx.set_font(MpCanvas.font_orange)
        elif color == 0x646464:
            Gfx.set_font(MpCanvas.font_gray)
        elif color == 0x41FF41:
            Gfx.set_font(MpCanvas.font_green)
        else:
            MpCanvas.log(_js("=======================drawString: No Color:", color))
        Gfx.draw_string_on(graphics, text, x, y, anchor)

    @staticmethod
    def draw_rect(x, y, w, h, color):  # g.java:1512
        Draw.draw_rect(MpCanvas.screen_g, x, y, w, h, color)

    @staticmethod
    def fill_rect(x, y, w, h, color):  # g.java:1516
        Draw.fill_rect(MpCanvas.screen_g, x, y, w, h, color)

    @staticmethod
    def fill_rect_on(graphics, x, y, w, h, color):  # g.java:1520
        Draw.fill_rect(graphics, x, y, w, h, color)

    @staticmethod
    def set_color(graphics, color):  # g.java:1524
        graphics.setColor(color)

    @staticmethod
    def draw_line_color(graphics, x1, y1, x2, y2, color):  # g.java:1528
        Draw.draw_line_color(graphics, x1, y1, x2, y2, color)

    @staticmethod
    def draw_line(graphics, x1, y1, x2, y2):  # g.java:1532
        Draw.draw_line(graphics, x1, y1, x2, y2)

    @staticmethod
    def draw_dot(graphics, x, y, color):  # g.java:1536
        Draw.fill_rect(graphics, x, y, 1, 1, color)

    @staticmethod
    def draw_image(x, y, image):  # g.java:1540
        Draw.draw_image(MpCanvas.screen_g, image, x, y, 0)

    @staticmethod
    def draw_image_on(graphics, x, y, image):  # g.java:1544
        Draw.draw_image(graphics, image, x, y, 0)

    @staticmethod
    def draw_right_half(x, y, image):  # g.java:1548
        half_w = (idiv(image.getWidth(), 2) + 1)
        h = image.getHeight()
        Draw.draw_image_part(MpCanvas.screen_g, image, (x - half_w), y, half_w, h, (half_w - 1), 0)

    @staticmethod
    def draw_right_half_on(graphics, x, y, image):  # g.java:1554
        half_w = (idiv(image.getWidth(), 2) + 1)
        h = image.getHeight()
        Draw.draw_image_part(graphics, image, (x - half_w), y, half_w, h, (half_w - 1), 0)

    @staticmethod
    def draw_right_half_h(graphics, x, y, h, image):  # g.java:1560
        half_w = (idiv(image.getWidth(), 2) + 1)
        Draw.draw_image_part(graphics, image, (x - half_w), y, half_w, h, (half_w - 1), 0)

    @staticmethod
    def draw_right_aligned(x, y, image, half):  # g.java:1565
        if half:
            half_w = (idiv(image.getWidth(), 2) + 1)
            h = image.getHeight()
            Draw.draw_image_part(MpCanvas.screen_g, image, (x - half_w), y, half_w, h, (half_w - 1), 0)
            return
        Draw.draw_image(MpCanvas.screen_g, image, (x - image.getWidth()), y, 0)

    @staticmethod
    def draw_left_half_row(graphics, x, y, image, h, row):  # g.java:1575
        half_w = (idiv(image.getWidth(), 2) + 1)
        Draw.draw_image_part(graphics, image, x, y, half_w, h, 0, (h * row))

    @staticmethod
    def draw_right_half_row1(graphics, x, y, h, image):  # g.java:1580
        half_w = (idiv(image.getWidth(), 2) + 1)
        Draw.draw_image_part(graphics, image, (x - half_w), y, half_w, h, (half_w - 1), h)

    @staticmethod
    def draw_left_half(x, y, image):  # g.java:1585
        half_w = (idiv(image.getWidth(), 2) + 1)
        h = image.getHeight()
        Draw.draw_image_part(MpCanvas.screen_g, image, x, y, half_w, h, 0, 0)

    @staticmethod
    def draw_left_half_on(graphics, x, y, image):  # g.java:1591
        half_w = (idiv(image.getWidth(), 2) + 1)
        h = image.getHeight()
        Draw.draw_image_part(graphics, image, x, y, half_w, h, 0, 0)

    @staticmethod
    def draw_left_half_h(graphics, x, y, h, image):  # g.java:1597
        half_w = (idiv(image.getWidth(), 2) + 1)
        Draw.draw_image_part(graphics, image, x, y, half_w, h, 0, 0)

    def draw_buffer(self):  # g.java:1602
        Draw.draw_image(MpCanvas.screen_g, MpCanvas.buffer, 0, 0, 0)
        if (MpCanvas.state >= 90) and (MpCanvas.state <= 105):
            MpCanvas.draw_hp_bars(MpCanvas.screen_g)

    def draw_box(self, graphics, x, y, w, h, style):  # g.java:3442
        edge_color = 0x525152
        corner_color = 0xFFFFFF
        if style in (0, 7):
            if imod(w, 2) == 1:
                w = w + 1
            if imod(h, 2) == 1:
                h = h + 1
            MpCanvas.win_x = (x - idiv(w, 2))
            MpCanvas.win_y = (y - idiv(h, 2))
            if style == 0:
                Draw.fill_rect(graphics, MpCanvas.win_x, MpCanvas.win_y, w, h, 0)
            Draw.draw_rect(graphics, (MpCanvas.win_x + 1), (MpCanvas.win_y + 1), (w - 2), (h - 2), 0xADAAAD)
            MpCanvas.draw_left_half_on(graphics, (MpCanvas.win_x + Consts.ui_dx[2]), (MpCanvas.win_y + Consts.ui_dy[2]), MpCanvas.ui_images[2])
            MpCanvas.draw_right_half_on(graphics, ((MpCanvas.win_x + w) + Consts.ui_dx[2]), (MpCanvas.win_y + Consts.ui_dy[2]), MpCanvas.ui_images[2])
            MpCanvas.draw_left_half_on(graphics, (MpCanvas.win_x + Consts.ui_dx[3]), ((((MpCanvas.win_y + h) - 2) - 5) + Consts.ui_dy[3]), MpCanvas.ui_images[3])
            MpCanvas.draw_right_half_on(graphics, ((MpCanvas.win_x + w) + Consts.ui_dx[3]), ((((MpCanvas.win_y + h) - 2) - 5) + Consts.ui_dy[3]), MpCanvas.ui_images[3])
            return
        if style == 1:
            MpCanvas.fill_rect_on(graphics, x, y, w, h, 0)
            MpCanvas.set_color(graphics, 0xBDBABD)
            MpCanvas.draw_line(graphics, (x + 14), y, (((x + w) - 14) - 1), y)
            MpCanvas.draw_line(graphics, (x + 14), ((y + h) - 1), (((x + w) - 14) - 1), ((y + h) - 1))
            MpCanvas.set_color(graphics, 0x949A94)
            MpCanvas.draw_line(graphics, (x + 1), y, (x + 13), y)
            MpCanvas.draw_line(graphics, ((x + w) - 14), y, ((x + w) - 2), y)
            MpCanvas.draw_line(graphics, (x + 1), ((y + h) - 1), (x + 13), ((y + h) - 1))
            MpCanvas.draw_line(graphics, ((x + w) - 14), ((y + h) - 1), ((x + w) - 2), ((y + h) - 1))
            MpCanvas.set_color(graphics, 0xADAAAD)
            MpCanvas.draw_line(graphics, (x + 5), y, (x + 8), y)
            MpCanvas.draw_line(graphics, ((x + w) - 9), y, ((x + w) - 6), y)
            MpCanvas.draw_line(graphics, (x + 5), ((y + h) - 1), (x + 8), ((y + h) - 1))
            MpCanvas.draw_line(graphics, ((x + w) - 9), ((y + h) - 1), ((x + w) - 6), ((y + h) - 1))
            MpCanvas.set_color(graphics, 0x949A94)
            MpCanvas.draw_line(graphics, x, (y + 1), x, ((y + h) - 2))
            MpCanvas.draw_line(graphics, ((x + w) - 1), (y + 1), ((x + w) - 1), ((y + h) - 2))
            MpCanvas.set_color(graphics, 0xADAAAD)
            MpCanvas.draw_line(graphics, x, (y + 4), x, ((y + h) - 5))
            MpCanvas.draw_line(graphics, ((x + w) - 1), (y + 4), ((x + w) - 1), ((y + h) - 5))
            return
        if style == 3:
            MpCanvas.set_color(graphics, corner_color)
            MpCanvas.draw_line(graphics, x, (y - 1), ((x + w) - 1), (y - 1))
            MpCanvas.draw_line(graphics, x, (y + h), ((x + w) - 1), (y + h))
            MpCanvas.draw_line(graphics, (x - 1), y, (x - 1), ((y + h) - 1))
            MpCanvas.draw_line(graphics, (x + w), y, (x + w), ((y + h) - 1))
            MpCanvas.draw_dot(graphics, x, y, corner_color)
            MpCanvas.draw_dot(graphics, ((x + w) - 1), y, corner_color)
            MpCanvas.draw_dot(graphics, x, ((y + h) - 1), corner_color)
            MpCanvas.draw_dot(graphics, ((x + w) - 1), ((y + h) - 1), corner_color)
            return
        Draw.fill_rect(graphics, x, (y + 1), 1, (h - 2), edge_color)
        Draw.fill_rect(graphics, ((x + w) - 1), (y + 1), 1, (h - 2), edge_color)
        MpCanvas.loop_j = 1
        while MpCanvas.loop_j < (w - 1):
            Draw.fill_rect(graphics, (x + MpCanvas.loop_j), y, 1, h, edge_color)
            Draw.fill_rect(graphics, (x + MpCanvas.loop_j), (y + 1), 1, (h - 2), 0)
            MpCanvas.loop_j = MpCanvas.loop_j + 1

    def draw_number1_on(self, graphics, x, y, value):  # g.java:4619
        MpCanvas.draw_number(graphics, x, y, value, 1)

    def draw_number2_on(self, graphics, x, y, value):  # g.java:4623
        MpCanvas.draw_number(graphics, x, y, value, 2)

    def draw_number3_on(self, graphics, x, y, value):  # g.java:4627
        MpCanvas.draw_number(graphics, x, y, value, 3)

    def draw_damage_number(self, graphics, x, y, value):  # g.java:4631
        MpCanvas.draw_number(graphics, x, y, value, 4)

    def draw_number5(self, x, y, value):  # g.java:4635
        MpCanvas.draw_number(MpCanvas.screen_g, x, y, value, 5)

    def draw_number0_on(self, graphics, x, y, value):  # g.java:4639
        MpCanvas.draw_number(graphics, x, y, value, 0)

    def draw_number0(self, x, y, value):  # g.java:4643
        MpCanvas.draw_number(MpCanvas.screen_g, x, y, value, 0)

    def draw_number1(self, x, y, value):  # g.java:4647
        MpCanvas.draw_number(MpCanvas.screen_g, x, y, value, 1)

    def draw_number0_b(self, x, y, value):  # g.java:4651
        MpCanvas.draw_number(MpCanvas.screen_g, x, y, value, 0)

    def draw_number1_b(self, x, y, value):  # g.java:4655
        MpCanvas.draw_number(MpCanvas.screen_g, x, y, value, 1)

    @staticmethod
    def draw_number(graphics, x, y, value, style):  # g.java:4659
        place = 1
        digits = 0
        if style in (0, 1, 7):
            while (idiv(value, place) > 0) or (place == 1):
                digit = idiv(imod(value, (place * 10)), place)
                Draw.draw_image_part(graphics, MpCanvas.number_images[style], x, y, 5, 8, (digit * 5), 0)
                x = (x - 6)
                place = (place * 10)
                if (imod((digits := i32(digits + 1)), 3) != 0) or (idiv(value, place) <= 0):
                    continue
                Draw.draw_image_part(graphics, MpCanvas.number_images[style], (x := (x + 2)), (y + 5), 2, 3, 50, 5)
                x = (x - 6)
        elif style == 5:
            Draw.draw_image_part(graphics, MpCanvas.number_images[6], (x - 3), (y - 1), 3, 10, 7, 0)
            x = (x - 9)
            while (idiv(value, place) > 0) or (place == 1):
                digit2 = idiv(imod(value, (place * 10)), place)
                Draw.draw_image_part(graphics, MpCanvas.number_images[style], x, y, 5, 8, (digit2 * 5), 16)
                x = (x - 6)
                place = (place * 10)
                if (imod((digits := i32(digits + 1)), 3) != 0) or (idiv(value, place) <= 0):
                    continue
                Draw.fill_rect(graphics, (x := (x + 2)), (y + 6), 1, 3, 65280)
                x = (x - 6)
            Draw.draw_image_part(graphics, MpCanvas.number_images[6], (x - 2), (y - 1), 7, 10, 0, 0)
        elif style == 2:
            while (idiv(value, place) > 0) or (place == 1):
                digit3 = idiv(imod(value, (place * 10)), place)
                Draw.draw_image_part(graphics, MpCanvas.number_images[style], x, y, 7, 11, (digit3 * 7), 0)
                x = (x - 8)
                place = (place * 10)
        elif style == 3:
            while (idiv(value, place) > 0) or (place == 1):
                digit4 = idiv(imod(value, (place * 10)), place)
                Draw.draw_image_part(graphics, MpCanvas.number_images[style], x, y, 12, 13, (digit4 * 12), 0)
                x = (x - 12)
                place = (place * 10)
        elif style == 4:
            if value < 0:
                value = (-value)
                MpCanvas.number_negative = True
            else:
                MpCanvas.number_negative = False
            while (idiv(value, place) > 0) or (place == 1):
                digit5 = idiv(imod(value, (place * 10)), place)
                Draw.draw_image_part(graphics, MpCanvas.number_images[style], x, y, 6, 10, (digit5 * 6), (10 if MpCanvas.number_negative else 0))
                x = (x - 7)
                place = (place * 10)

    def draw_button(self, graphics, text, x, y, w, h, selected, enabled):  # g.java:5730
        if selected:
            Draw.draw_frame(graphics, (x - 1), (y - 1), (w + 2), (h + 2), 1, 0xFFFFFF)
            Draw.draw_rect(graphics, x, y, w, h, 0xFFFFFF)
        MpCanvas.draw_panel(graphics, x, y, w, h)
        if not enabled:
            self.draw_text_centred((x + idiv(w, 2)), (y + idiv(((h - 11)), 2)), text, 0x646464)
            return
        self.draw_text_centred((x + idiv(w, 2)), (y + idiv(((h - 11)), 2)), text, 0xFFFFFF)

    @staticmethod
    def draw_panel(graphics, x, y, w, h):  # g.java:5743
        Draw.draw_frame(graphics, x, y, w, h, 1, 0x949694)
        Draw.fill_rect(graphics, (x + 1), (y + 1), (w - 2), (h - 2), 0)

    @staticmethod
    def draw_border_v(graphics, x, y, length, src_x):  # g.java:5783
        count = (idiv(length, 11) + 1)
        i = 0
        while i < count:
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, x, (y + (11 * i)), 5, 11, src_x, 8)
            i = i + 1

    @staticmethod
    def draw_back_tiles(graphics):  # g.java:5792
        cols = (idiv(MpCanvas.canvas_w, MpCanvas.back_image.getWidth()) + 1)
        rows = (idiv(MpCanvas.canvas_h, MpCanvas.back_image.getHeight()) + 1)
        col = 0
        while col < cols:
            row = 0
            while row < rows:
                if imod(row, 2) != 0:
                    Draw.draw_image(graphics, MpCanvas.back_image, (MpCanvas.back_image.getWidth() * col), (MpCanvas.back_image.getHeight() * row), 0)
                else:
                    Draw.draw_image_part(graphics, MpCanvas.back_image, (MpCanvas.back_image.getWidth() * col), (MpCanvas.back_image.getHeight() * row), 21, 24, 31, 0)
                    Draw.draw_image_part(graphics, MpCanvas.back_image, ((MpCanvas.back_image.getWidth() * col) + 21), (MpCanvas.back_image.getHeight() * row), 31, 24, 0, 0)
                row = row + 1
            col = col + 1

    @staticmethod
    def draw_border_h(graphics, x, y, length, src_y):  # g.java:5811
        count = (idiv(length, 11) + 1)
        i = 0
        while i < count:
            Draw.draw_image_part(graphics, MpCanvas.border_h_image, (x + (11 * i)), y, 11, 5, 10, src_y)
            i = i + 1

    def draw_softkeys(self, left, right):  # g.java:6220
        if left != (-1):
            MpCanvas.draw_image_on(MpCanvas.screen_g, 0, (MpCanvas.screen_h - 11), MpCanvas.softkey_image)
            self.draw_text_centred_on(MpCanvas.screen_g, 28, (MpCanvas.screen_h - 11), Consts.softkeys[left], 0xFFFFFF)
        if right != (-1):
            MpCanvas.draw_image_on(MpCanvas.screen_g, (MpCanvas.screen_w - 57), (MpCanvas.screen_h - 11), MpCanvas.softkey_image)
            self.draw_text_centred_on(MpCanvas.screen_g, (MpCanvas.screen_w - 28), (MpCanvas.screen_h - 11), Consts.softkeys[right], 0xFFFFFF)

    def draw_ok_button(self, y):  # g.java:6231
        self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 10), (y + 1), 18, 9, 3)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, y, Consts.softkeys[0], 0xFFFFFF)
