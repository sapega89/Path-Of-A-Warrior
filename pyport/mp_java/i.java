/*
 * Decompiled with CFR 0.152.
 * 
 * Could not load the following classes:
 *  javax.microedition.lcdui.Graphics
 *  javax.microedition.lcdui.Image
 */
import javax.microedition.lcdui.Graphics;
import javax.microedition.lcdui.Image;

public final class i {
    private static Graphics b;
    private static int c;
    private static int d;
    private static int e;
    private static int f;
    private static j g;
    static int[] a;

    public static void a(Graphics graphics) {
        b = graphics;
        c = b.getClipX();
        d = b.getClipY();
        e = b.getClipWidth();
        f = b.getClipHeight();
    }

    public static void a(Image image, int n2, int n3, int n4, int n5, int n6, int n7) {
        b.clipRect(n2, n3, n4, n5);
        b.drawImage(image, n2 - n6, n3 - n7, 20);
        b.setClip(c, d, e, f);
    }

    public static void a(int n2, int n3, int n4, int n5, int n6) {
        b.setColor(n6);
        b.fillRect(n2, n3, n4, n5);
    }

    public static void a(j j2) {
        g = j2;
    }

    private static void a(char[] cArray, int n2, int n3, int n4, int n5, int n6) {
        if ((n6 & 1) != 0) {
            n4 -= g.a(cArray, n2, n3) / 2;
        } else if ((n6 & 8) != 0) {
            n4 -= g.a(cArray, n2, n3);
        }
        int n7 = n2 + n3;
        int n8 = n4;
        int n9 = n2;
        while (n9 < n7) {
            char c2 = cArray[n9];
            int n10 = g.a(c2);
            g.a(c2, n8, n5);
            n8 += n10;
            ++n9;
        }
    }

    public static void a(String string, int n2, int n3, int n4) {
        i.a(string.toCharArray(), 0, string.length(), n2, n3, n4);
    }

    public static void a(Graphics graphics, String string, int n2, int n3, int n4) {
        Graphics graphics2 = b;
        b = graphics;
        i.a(string.toCharArray(), 0, string.length(), n2, n3, n4);
        b = graphics2;
    }

    private static void a() {
        a = new int[256];
        int n2 = 0;
        while (n2 < 256) {
            int n3 = n2;
            int n4 = 8;
            while (--n4 >= 0) {
                if ((n3 & 1) != 0) {
                    n3 = 0xEDB88320 ^ n3 >>> 1;
                    continue;
                }
                n3 >>>= 1;
            }
            i.a[n2] = n3;
            ++n2;
        }
    }

    static long a(byte[] byArray, int n2, int n3) {
        if (a == null) {
            i.a();
        }
        int n4 = -1;
        while (--n3 >= 0) {
            n4 = a[(n4 ^ byArray[n2++]) & 0xFF] ^ n4 >>> 8;
        }
        return (long)(~n4) & 0xFFFFFFFFL;
    }

    static {
        byte[] byArray = new byte[]{-119, 80, 78, 71, 13, 10, 26, 10, 0, 0, 0, 13, 73, 72, 68, 82, 0, 0, 0, 0, 0, 0, 0, 0, 8, 3, 0, 0, 0};
        byte[] byArray2 = new byte[]{0, 0, 0, 0, 73, 69, 78, 68, -82, 66, 96, -126};
    }
}

