"""Draw: image / rectangle helpers on a Graphics.
"""




class Draw:

    @staticmethod
    def draw_image(graphics, image, x, y, anchor):
        graphics.drawImage(image, x, y, anchor)

    @staticmethod
    def draw_image_part(graphics, image, x, y, w, h, src_x, src_y):
        old_x = graphics.getClipX()
        old_y = graphics.getClipY()
        old_w = graphics.getClipWidth()
        old_h = graphics.getClipHeight()
        graphics.clipRect(x, y, w, h)
        graphics.drawImage(image, (x - src_x), (y - src_y), 20)
        graphics.setClip(old_x, old_y, old_w, old_h)

    @staticmethod
    def draw_rect(graphics, x, y, w, h, color):
        graphics.setColor(color)
        graphics.drawRect(x, y, (w - 1), (h - 1))

    @staticmethod
    def draw_frame(graphics, x, y, w, h, corner, color):
        Draw.draw_hline(graphics, (x + corner), y, (w - (2 * corner)), color)
        Draw.draw_hline(graphics, (x + corner), ((y + h) - 1), (w - (2 * corner)), color)
        Draw.draw_vline(graphics, x, (y + corner), (h - (2 * corner)), color)
        Draw.draw_vline(graphics, ((x + w) - 1), (y + corner), (h - (2 * corner)), color)
        if corner == 2:
            Draw.fill_rect(graphics, (x + 1), (y + 1), 1, 1, color)
            Draw.fill_rect(graphics, ((x + w) - 2), (y + 1), 1, 1, color)
            Draw.fill_rect(graphics, (x + 1), ((y + h) - 2), 1, 1, color)
            Draw.fill_rect(graphics, ((x + w) - 2), ((y + h) - 2), 1, 1, color)

    @staticmethod
    def fill_rect(graphics, x, y, w, h, color):
        graphics.setColor(color)
        graphics.fillRect(x, y, w, h)

    @staticmethod
    def draw_hline(graphics, x, y, length, color):
        graphics.setColor(color)
        graphics.drawLine(x, y, ((x + length) - 1), y)

    @staticmethod
    def draw_vline(graphics, x, y, length, color):
        graphics.setColor(color)
        graphics.drawLine(x, y, x, ((y + length) - 1))

    @staticmethod
    def draw_line_color(graphics, x1, y1, x2, y2, color):
        graphics.setColor(color)
        graphics.drawLine(x1, y1, x2, y2)

    @staticmethod
    def draw_line(graphics, x1, y1, x2, y2):
        graphics.drawLine(x1, y1, x2, y2)


def _static_init():
    pass


def _late_imports():
    pass
