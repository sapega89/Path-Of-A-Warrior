/*
 * Decompiled with CFR 0.152.
 * 
 * Could not load the following classes:
 *  javax.microedition.io.Connector
 *  javax.microedition.io.StreamConnection
 */
import java.io.IOException;
import java.io.InterruptedIOException;
import javax.microedition.io.Connector;
import javax.microedition.io.StreamConnection;

public final class h
extends Thread {
    public static short a = 0;
    public static StreamConnection b = null;
    public static e c;
    public static d d;
    public static g e;
    public k f;
    public static boolean g;
    public static int h;
    public static int i;
    public static boolean j;
    public static boolean k;
    public static boolean l;
    public String m;
    public int n;

    public h() {
        g = true;
        j = false;
        k = true;
        l = false;
    }

    public final void a(String string, int n2) {
        this.m = string;
        this.n = n2;
        l = true;
    }

    public static void a() {
        h = 0;
        j = false;
        try {
            if (d != null) {
                d.a();
            }
        }
        catch (Exception exception) {}
        try {
            if (c != null) {
                c.a();
            }
        }
        catch (Exception exception) {}
        try {
            if (b != null) {
                b.close();
            }
        }
        catch (Exception exception) {}
        b = null;
        System.gc();
    }

    private void c() {
        try {
            b = (StreamConnection)Connector.open((String)("socket://" + this.m + ":" + this.n));
            d = new d(b.openInputStream());
            c = new e(b.openOutputStream());
            h = 0;
            j = true;
            e.l();
            return;
        }
        catch (Exception exception) {
            e.g(0);
            return;
        }
    }

    public static void a(g g2) {
        e = g2;
    }

    public final void run() {
        while (k) {
            if (j) {
                try {
                    this.f = d.b();
                    a = (short)((this.f.a[0] & 0xFF) << 0 | (this.f.a[1] & 0xFF) << 8);
                    e.a(this.f);
                    h = 0;
                    Thread.yield();
                }
                catch (InterruptedIOException interruptedIOException) {
                    e.g(1);
                }
                catch (IOException iOException) {
                    e.g(2);
                }
                catch (Exception exception) {
                    e.g(3);
                }
            } else {
                if (l) {
                    l = false;
                    this.c();
                } else if (j && ++i > Integer.MAX_VALUE) {
                    i = 300;
                }
                Thread.yield();
                h.c(100);
            }
            h.c(100);
        }
    }

    private static void c(int n2) {
        try {
            Thread.sleep(n2);
            return;
        }
        catch (Exception exception) {
            return;
        }
    }

    public final synchronized void a(int n2) {
        if (j) {
            while (!g) {
                h.c(50);
            }
            g = false;
            c.a(n2);
        }
    }

    public static void a(byte by) {
        if (j) {
            c.a(by);
        }
    }

    public static void b(int n2) {
        if (j) {
            c.b(n2);
        }
    }

    public static void b(String string, int n2) {
        if (j) {
            c.a(string, n2);
        }
    }

    public static void b() {
        h = 0;
        c.b();
        g = true;
    }

    static {
        g = true;
        j = false;
        k = true;
        l = false;
    }
}

