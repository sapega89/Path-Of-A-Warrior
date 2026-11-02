/*
 * Decompiled with CFR 0.152.
 * 
 * Could not load the following classes:
 *  javax.microedition.lcdui.Image
 */
import javax.microedition.lcdui.Image;

public final class j {
    private Image a;
    private int b;
    private int c;
    private int d;
    private int e = 0;

    public j(String string, int n2, int n3, int n4, int n5) {
        this.b = n2;
        this.c = n3;
        this.d = n4;
        try {
            byte[] byArray = n.a(string);
            byte by = (byte)(n5 >> 16 & 0xFF);
            byte by2 = (byte)(n5 >> 8 & 0xFF);
            byte by3 = (byte)(n5 & 0xFF);
            int n6 = 0;
            while (n6 < 100) {
                if (byArray[n6] == 80 && byArray[n6 + 1] == 76 && byArray[n6 + 2] == 84 && byArray[n6 + 3] == 69) {
                    this.e = n6;
                    break;
                }
                ++n6;
            }
            if (byArray[this.e + 4] != by || byArray[this.e + 5] != by2 || byArray[this.e + 6] != by3) {
                byArray[this.e + 4] = by;
                byArray[this.e + 5] = by2;
                byArray[this.e + 6] = by3;
                long l2 = i.a(byArray, this.e, 10);
                byArray[this.e + 10] = (byte)(l2 >> 24 & 0xFFL);
                byArray[this.e + 11] = (byte)(l2 >> 16 & 0xFFL);
                byArray[this.e + 12] = (byte)(l2 >> 8 & 0xFFL);
                byArray[this.e + 13] = (byte)(l2 & 0xFFL);
            }
            this.a = Image.createImage((byte[])byArray, (int)0, (int)byArray.length);
            System.gc();
            return;
        }
        catch (Exception exception) {
            System.out.println("font fail : " + string);
            return;
        }
    }

    final void a(char c2, int n2, int n3) {
        if (c2 == ' ') {
            return;
        }
        i.a(this.a, n2, n3, this.b, this.c, j.b(c2) * this.b, 0);
    }

    private static int b(char c2) {
        int n2 = 0;
        if (c2 >= 'A' && c2 <= 'Z') {
            n2 = 32 + (c2 - 65);
        } else if (c2 >= 'a' && c2 <= 'z') {
            n2 = 64 + (c2 - 97);
        } else if (c2 >= '0' && c2 <= '9') {
            n2 = 15 + (c2 - 48);
        } else if (c2 == '!') {
            n2 = 0;
        } else if (c2 == '\"') {
            n2 = 1;
        } else if (c2 == '#') {
            n2 = 2;
        } else if (c2 == '$') {
            n2 = 3;
        } else if (c2 == '%') {
            n2 = 4;
        } else if (c2 == '&') {
            n2 = 5;
        } else if (c2 == '\'') {
            n2 = 6;
        } else if (c2 == '(') {
            n2 = 7;
        } else if (c2 == ')') {
            n2 = 8;
        } else if (c2 == '*') {
            n2 = 9;
        } else if (c2 == '+') {
            n2 = 10;
        } else if (c2 == ',') {
            n2 = 11;
        } else if (c2 == '-') {
            n2 = 12;
        } else if (c2 == '.') {
            n2 = 13;
        } else if (c2 == '/') {
            n2 = 14;
        } else if (c2 == ':') {
            n2 = 25;
        } else if (c2 == ';') {
            n2 = 26;
        } else if (c2 == '<') {
            n2 = 27;
        } else if (c2 == '=') {
            n2 = 28;
        } else if (c2 == '>') {
            n2 = 29;
        } else if (c2 == '?') {
            n2 = 30;
        } else if (c2 == '@') {
            n2 = 31;
        } else if (c2 == '[') {
            n2 = 58;
        } else if (c2 == ']') {
            n2 = 60;
        } else if (c2 == '^') {
            n2 = 61;
        } else if (c2 == '_') {
            n2 = 62;
        } else if (c2 == '`') {
            n2 = 63;
        } else if (c2 == '{') {
            n2 = 90;
        } else if (c2 == '|') {
            n2 = 91;
        } else if (c2 == '}') {
            n2 = 92;
        } else if (c2 == '~') {
            n2 = 93;
        } else if (c2 == ' ') {
            n2 = 99;
        }
        return n2;
    }

    public final int a(char c2) {
        if (c2 == ' ') {
            return this.d;
        }
        return this.b + 1 - 0;
    }

    public final int a(char[] cArray, int n2, int n3) {
        int n4 = 0;
        int n5 = n2 + n3;
        int n6 = n2;
        while (n6 < n5) {
            n4 += this.a(cArray[n6]);
            ++n6;
        }
        return n4;
    }

    public final int a(String string) {
        char[] cArray = string.toCharArray();
        return this.a(cArray, 0, cArray.length);
    }
}

