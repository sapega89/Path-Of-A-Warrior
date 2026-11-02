/*
 * Decompiled with CFR 0.152.
 * 
 * Could not load the following classes:
 *  javax.microedition.lcdui.Graphics
 *  javax.microedition.lcdui.Image
 */
import javax.microedition.lcdui.Graphics;
import javax.microedition.lcdui.Image;

public final class f {
    public static void a(Graphics graphics, Image image, int n2, int n3, int n4) {
        graphics.drawImage(image, n2, n3, n4);
    }

    public static void a(Graphics graphics, Image image, int n2, int n3, int n4, int n5, int n6, int n7) {
        int n8 = graphics.getClipX();
        int n9 = graphics.getClipY();
        int n10 = graphics.getClipWidth();
        int n11 = graphics.getClipHeight();
        graphics.clipRect(n2, n3, n4, n5);
        graphics.drawImage(image, n2 - n6, n3 - n7, 20);
        graphics.setClip(n8, n9, n10, n11);
    }

    public static void a(Graphics graphics, int n2, int n3, int n4, int n5, int n6) {
        graphics.setColor(n6);
        graphics.drawRect(n2, n3, n4 - 1, n5 - 1);
    }

    public static void a(Graphics graphics, int n2, int n3, int n4, int n5, int n6, int n7) {
        f.a(graphics, n2 + n6, n3, n4 - 2 * n6, n7);
        f.a(graphics, n2 + n6, n3 + n5 - 1, n4 - 2 * n6, n7);
        f.b(graphics, n2, n3 + n6, n5 - 2 * n6, n7);
        f.b(graphics, n2 + n4 - 1, n3 + n6, n5 - 2 * n6, n7);
        if (n6 == 2) {
            f.b(graphics, n2 + 1, n3 + 1, 1, 1, n7);
            f.b(graphics, n2 + n4 - 2, n3 + 1, 1, 1, n7);
            f.b(graphics, n2 + 1, n3 + n5 - 2, 1, 1, n7);
            f.b(graphics, n2 + n4 - 2, n3 + n5 - 2, 1, 1, n7);
        }
    }

    public static void b(Graphics graphics, int n2, int n3, int n4, int n5, int n6) {
        graphics.setColor(n6);
        graphics.fillRect(n2, n3, n4, n5);
    }

    public static void a(Graphics graphics, int n2, int n3, int n4, int n5) {
        graphics.setColor(n5);
        graphics.drawLine(n2, n3, n2 + n4 - 1, n3);
    }

    public static void b(Graphics graphics, int n2, int n3, int n4, int n5) {
        graphics.setColor(n5);
        graphics.drawLine(n2, n3, n2, n3 + n4 - 1);
    }

    public static void c(Graphics graphics, int n2, int n3, int n4, int n5, int n6) {
        graphics.setColor(n6);
        graphics.drawLine(n2, n3, n4, n5);
    }

    public static void c(Graphics graphics, int n2, int n3, int n4, int n5) {
        graphics.drawLine(n2, n3, n4, n5);
    }
}

