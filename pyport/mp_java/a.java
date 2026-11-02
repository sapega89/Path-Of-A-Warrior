/*
 * Decompiled with CFR 0.152.
 */
final class a {
    byte a;
    byte[] b;
    public short[] c;
    public short[] d;
    public byte[] e;
    public byte[] f;
    public byte[] g;
    public byte[] h;

    public a(String string) {
        this.b = n.a(string);
        this.a = this.b[0];
        this.c = new short[this.a];
        this.d = new short[this.a];
        this.e = new byte[this.a];
        this.f = new byte[this.a];
        this.g = new byte[this.a];
        this.h = new byte[this.a];
        int n2 = 0;
        while (n2 < this.a) {
            this.c[n2] = (short)(this.b[1 + 6 * n2] & 0xFF);
            this.d[n2] = (short)(this.b[2 + 6 * n2] & 0xFF);
            this.e[n2] = this.b[3 + 6 * n2];
            this.f[n2] = this.b[4 + 6 * n2];
            this.g[n2] = this.b[5 + 6 * n2];
            this.h[n2] = this.b[6 + 6 * n2];
            ++n2;
        }
    }

    public final void a() {
        this.b = null;
        this.c = null;
        this.d = null;
        this.e = null;
        this.f = null;
        this.g = null;
        this.h = null;
    }
}

