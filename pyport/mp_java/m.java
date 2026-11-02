/*
 * Decompiled with CFR 0.152.
 */
final class m
extends g {
    public static c fb = null;
    public static int fc = -1;
    public static int fd = -1;

    public m(Main main) {
        super(main);
        fb = new c(7, 1, true, true);
    }

    public static void v(int n2) {
        fc = n2;
    }

    public final void ak() {
        fb.b();
        boolean bl = false;
        boolean bl2 = true;
        int n2 = fc;
        fc = -1;
        if (g.am != 0 && n2 != -1) {
            if (n2 == 1) {
                if (fd == n2) {
                    bl2 = false;
                } else {
                    this.ag();
                }
                fd = n2;
                bl = true;
            } else {
                fd = -1;
                bl = false;
            }
            if (bl2) {
                this.b(n2, bl);
            }
        }
    }

    private void b(int n2, boolean bl) {
        fb.a(g.am * 20);
        if (g.am == 0) {
            this.ag();
            return;
        }
        if (n2 == 1) {
            fb.a("/snd" + n2 + ".mid", n2);
        } else {
            fb.a("/snd" + n2 + ".wav", n2);
        }
        fb.a(n2, bl);
    }

    public final void ag() {
        fc = -1;
        fd = -1;
        fb.a();
    }
}

