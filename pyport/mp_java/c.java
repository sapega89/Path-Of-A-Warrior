/*
 * Decompiled with CFR 0.152.
 * 
 * Could not load the following classes:
 *  javax.microedition.media.Manager
 *  javax.microedition.media.Player
 *  javax.microedition.media.PlayerListener
 *  javax.microedition.media.control.VolumeControl
 */
import java.io.ByteArrayInputStream;
import java.io.InputStream;
import javax.microedition.media.Manager;
import javax.microedition.media.Player;
import javax.microedition.media.PlayerListener;
import javax.microedition.media.control.VolumeControl;

public final class c
extends b
implements PlayerListener {
    private boolean a = false;
    private Player[] b;
    private boolean c = false;
    private boolean d;
    private int e;
    private int f;
    private boolean g;
    private boolean[] h;
    private String[] i;
    private int j;
    private int[] k;
    private int l = -1;
    private boolean m = false;
    private int n = -1;
    private boolean o = false;

    public c(int n2, int n3, boolean bl, boolean bl2) {
        this.e = n2;
        this.b = new Player[this.e];
        this.f = n3;
        this.g = bl;
        this.d = bl2;
        this.h = new boolean[this.e];
        int n4 = 0;
        while (n4 < this.e) {
            this.h[n4] = false;
            ++n4;
        }
        this.k = new int[this.e];
        int n5 = 0;
        while (n5 < this.e) {
            this.a(n5, 0);
            ++n5;
        }
        this.j = 100;
        this.i = new String[this.e];
    }

    public final void playerUpdate(Player player, String string, Object object) {
        String cfr_ignored_0 = "-1.:" + this.l;
        if (string == "started") {
            this.a = true;
            String cfr_ignored_1 = "-Update START:" + this.n;
            return;
        }
        if (string == "endOfMedia" || string == "stopped") {
            String cfr_ignored_2 = "-Update " + string + ":" + this.n;
            if (this.o && string == "endOfMedia") {
                return;
            }
            if (!this.g) {
                this.c();
            }
            this.a = false;
            this.n = -1;
            this.o = false;
        }
    }

    private void c() {
        int n2 = 0;
        while (n2 < this.e) {
            this.b(n2);
            ++n2;
        }
    }

    private void b(int n2) {
        if (this.b[n2] != null) {
            this.b[n2].close();
            this.b[n2] = null;
        }
        this.h[n2] = false;
    }

    public final void a(int n2, boolean bl) {
        if (n2 < 0) {
            return;
        }
        if (this.j <= 0) {
            return;
        }
        this.b(n2, bl);
    }

    private synchronized boolean b(int n2, boolean bl) {
        this.l = n2;
        this.m = bl;
        if (this.a) {
            this.e();
            if (this.a) {
                return false;
            }
        }
        this.d(5);
        String cfr_ignored_0 = "---step 2:" + this.j;
        if (!this.h[n2] && !this.a(this.i[n2], n2)) {
            return false;
        }
        if (this.f == 0) {
            this.d();
        }
        if (!c.a(this.b[n2])) {
            return false;
        }
        if (bl) {
            try {
                this.b[n2].setLoopCount(-1);
            }
            catch (IllegalArgumentException illegalArgumentException) {
                this.b[n2].setLoopCount(0);
            }
        } else {
            this.b[n2].setLoopCount(1);
        }
        if (this.d) {
            try {
                this.b[n2].setMediaTime(1L);
            }
            catch (Exception exception) {
                String cfr_ignored_1 = "setMediaTime err:" + exception;
            }
        }
        if (this.b[n2].getState() == 300) {
            try {
                this.n = n2;
                this.o = bl;
                this.b[n2].start();
                this.l = -1;
                this.b(this.b[n2]);
                return true;
            }
            catch (Exception exception) {
                String cfr_ignored_2 = "Start err:" + exception;
                return false;
            }
        }
        return false;
    }

    private boolean a(String string, int n2, String string2) {
        try {
            if (!this.g) {
                this.e();
                if (this.b[n2] != null) {
                    this.b[n2].close();
                }
                this.b[n2] = null;
                this.h[n2] = false;
                this.a = false;
                this.n = -1;
                this.o = false;
                this.l = -1;
                this.m = false;
            }
            if (!this.h[n2]) {
                ByteArrayInputStream byteArrayInputStream = new ByteArrayInputStream(n.a(string));
                Player player = Manager.createPlayer((InputStream)byteArrayInputStream, (String)string2);
                player.addPlayerListener((PlayerListener)this);
                player.realize();
                if (this.f == 1 && !c.a(player)) {
                    return false;
                }
                this.b[n2] = player;
                this.i[n2] = string;
                if (this.b[n2] != null) {
                    this.h[n2] = true;
                }
            }
            return true;
        }
        catch (Exception exception) {
            String cfr_ignored_0 = "loading err:" + exception;
            return false;
        }
    }

    public final boolean a(String string, int n2) {
        return this.a(string, n2, c.a(string));
    }

    private static String a(String string) {
        String string2 = null;
        if (string.endsWith("wav")) {
            string2 = "audio/x-wav";
        } else if (string.endsWith("amr")) {
            string2 = "audio/amr";
        } else if (string.endsWith("mid")) {
            string2 = "audio/midi";
        } else if (string.endsWith("mp3")) {
            string2 = "audio/mpeg";
        }
        return string2;
    }

    private static boolean a(Player player) {
        if (player == null) {
            return false;
        }
        if (player.getState() == 200) {
            try {
                player.prefetch();
                return true;
            }
            catch (Exception exception) {
                String cfr_ignored_0 = "tryPrefetch err:" + exception;
                return false;
            }
        }
        return player.getState() == 300;
    }

    private void d() {
        int n2 = 0;
        while (n2 < this.e) {
            if (this.b[n2] != null && this.b[n2].getState() == 300) {
                this.b[n2].deallocate();
            }
            ++n2;
        }
    }

    public final void a() {
        this.l = -1;
        this.m = false;
        this.e();
        this.a = false;
        this.n = -1;
    }

    private void e() {
        try {
            if (this.n != -1 && this.b[this.n] != null) {
                this.b[this.n].stop();
                if (!this.d) {
                    this.b[this.n].deallocate();
                }
            }
            return;
        }
        catch (Exception exception) {
            String cfr_ignored_0 = "playingSoundStop err:" + exception;
            return;
        }
    }

    private void c(int n2) {
        if (n2 >= 0 && n2 <= 100) {
            this.j = n2;
        }
    }

    public final void a(int n2) {
        this.c(n2);
        int n3 = this.n;
        if (n3 != -1) {
            this.b(this.b[n3]);
        }
    }

    private void b(Player player) {
        VolumeControl volumeControl;
        if (player != null && (volumeControl = (VolumeControl)player.getControl("VolumeControl")) != null) {
            volumeControl.setLevel(this.j);
        }
    }

    private void a(int n2, int n3) {
        if (n2 < this.e && n2 >= 0) {
            this.k[n2] = n3;
        }
    }

    public final void b() {
        c c2 = this;
        synchronized (c2) {
            if (!this.c) {
                if (this.l != -1 && !this.a) {
                    if (this.m) {
                        this.a(this.l, this.m);
                    }
                } else if (this.a && this.b[this.n] != null && this.b[this.n].getState() != 400 && this.o) {
                    this.a = false;
                    this.a(this.n, this.o);
                }
            }
            return;
        }
    }

    private void d(int n2) {
        try {
            Thread.sleep(n2);
            Thread.yield();
            return;
        }
        catch (Exception exception) {
            return;
        }
    }
}

