"""Draw (f.java): image / rectangle helpers on a Graphics.

Generated once from pyport/mp_java/f.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""




class Draw(object):

    @staticmethod
    def a_GMIII(graphics, image, n2, n3, n4):  # f.java:12
        graphics.drawImage(image, n2, n3, n4)

    @staticmethod
    def a_GMIIIIII(graphics, image, n2, n3, n4, n5, n6, n7):  # f.java:16
        n8 = graphics.getClipX()
        n9 = graphics.getClipY()
        n10 = graphics.getClipWidth()
        n11 = graphics.getClipHeight()
        graphics.clipRect(n2, n3, n4, n5)
        graphics.drawImage(image, (n2 - n6), (n3 - n7), 20)
        graphics.setClip(n8, n9, n10, n11)

    @staticmethod
    def a_GIIIII(graphics, n2, n3, n4, n5, n6):  # f.java:26
        graphics.setColor(n6)
        graphics.drawRect(n2, n3, (n4 - 1), (n5 - 1))

    @staticmethod
    def a_GIIIIII(graphics, n2, n3, n4, n5, n6, n7):  # f.java:31
        Draw.a_GIIII(graphics, (n2 + n6), n3, (n4 - (2 * n6)), n7)
        Draw.a_GIIII(graphics, (n2 + n6), ((n3 + n5) - 1), (n4 - (2 * n6)), n7)
        Draw.b_GIIII(graphics, n2, (n3 + n6), (n5 - (2 * n6)), n7)
        Draw.b_GIIII(graphics, ((n2 + n4) - 1), (n3 + n6), (n5 - (2 * n6)), n7)
        if n6 == 2:
            Draw.b_GIIIII(graphics, (n2 + 1), (n3 + 1), 1, 1, n7)
            Draw.b_GIIIII(graphics, ((n2 + n4) - 2), (n3 + 1), 1, 1, n7)
            Draw.b_GIIIII(graphics, (n2 + 1), ((n3 + n5) - 2), 1, 1, n7)
            Draw.b_GIIIII(graphics, ((n2 + n4) - 2), ((n3 + n5) - 2), 1, 1, n7)

    @staticmethod
    def b_GIIIII(graphics, n2, n3, n4, n5, n6):  # f.java:44
        graphics.setColor(n6)
        graphics.fillRect(n2, n3, n4, n5)

    @staticmethod
    def a_GIIII(graphics, n2, n3, n4, n5):  # f.java:49
        graphics.setColor(n5)
        graphics.drawLine(n2, n3, ((n2 + n4) - 1), n3)

    @staticmethod
    def b_GIIII(graphics, n2, n3, n4, n5):  # f.java:54
        graphics.setColor(n5)
        graphics.drawLine(n2, n3, n2, ((n3 + n4) - 1))

    @staticmethod
    def c_GIIIII(graphics, n2, n3, n4, n5, n6):  # f.java:59
        graphics.setColor(n6)
        graphics.drawLine(n2, n3, n4, n5)

    @staticmethod
    def c_GIIII(graphics, n2, n3, n4, n5):  # f.java:64
        graphics.drawLine(n2, n3, n4, n5)


def _static_init():
    pass


def _late_imports():
    pass
